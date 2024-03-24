// rust library imports
use clamav_client::{ping, Tcp};
use pyo3::prelude::*;
use rayon::prelude::*;
use runas::Command as RCommand;
use std::io;
use thiserror::Error;

/// Default socket path
static CLAMD_SOCKET: Tcp<&'static str> = Tcp {
    host_address: "localhost:3310",
};

/// Error type describing possible errors when scanning a file
#[derive(Error, Debug)]
enum FileScanError {
    #[error("io error occured while calling clamd's scan: {0}")]
    IoError(#[from] io::Error),
    #[error("utf8 error occured while getting clean data: {0}")]
    Utf8Error(#[from] std::str::Utf8Error),
}

/// Error type describing all possible errors in this library
#[derive(Error, Debug)]
enum AvLibError {
    #[error("an error occured file scanning a file: ({0})")]
    FileScanError(#[from] FileScanError),
    #[error("an error occured while walking through the filesystem: ({0})")]
    WalkError(#[from] jwalk::Error),
}

/// Result type to return from functions
type AvResult<T> = Result<T, AvLibError>;

// Implements error conversion from rust error to python error
impl std::convert::From<AvLibError> for PyErr {
    fn from(err: AvLibError) -> PyErr {
        pyo3::exceptions::PyOSError::new_err(err.to_string())
    }
}

/// Activates clamd service on windows (requires UAC)
#[cfg(windows)]
fn activate_clamd() -> io::Result<()> {
    RCommand::new("net.exe")
        .arg("start")
        .arg("clamd")
        .status()?;
    Ok(())
}

/// Activates clamd service on linux (requires polkit)
#[cfg(linux)]
fn activate_clamd() -> io::Result<()> {
    use std::process::Command;
    Command::new("pkexec")
        .arg("systemctl start clamd")
        .status()?;

    Ok(())
}

/// Ensures the clamd service is running
#[pyfunction]
fn ensure_running() {
    match ping(CLAMD_SOCKET) {
        Ok(v) => {
            if v == clamav_client::PONG {
            } else {
                panic!("server will never not return PONG")
            }
        }
        Err(_) => activate_clamd().expect("Server should've started: "),
    };
    println!("server is working");
}

use std::path::PathBuf;

/// Scans a single file, with a tuple result, w/ a bool if clean, and a Optional name if not clean
#[pyfunction]
fn scan_file(path: PathBuf) -> AvResult<(bool, Option<String>)> {
    let res = match clamav_client::scan_file(path, CLAMD_SOCKET, None) {
        // funny error conversion :P
        Ok(v) => AvResult::Ok(v),
        Err(err) => AvResult::Err(AvLibError::FileScanError(FileScanError::IoError(err))),
    }?;

    let out = match std::str::from_utf8(&res) {
        // funny error conversion :P
        Ok(v) => AvResult::Ok(v),
        Err(err) => AvResult::Err(AvLibError::FileScanError(FileScanError::Utf8Error(err))),
    }?;
    let mut name = None; // initialized to None, so if its found it can set it to Some(*)
    if out.contains("FOUND") {
        // string parsing X_x
        let first_end = out.split_at(8).1;
        name = Some(first_end.split_at(first_end.len() - 7).0.to_owned());
    };
    Ok((out.contains("OK") && !out.contains("FOUND"), name))
}

use std::thread;

#[pyfunction]
fn scan_dir(path: PathBuf) -> AvResult<Vec<(PathBuf, String)>> {
    use jwalk::WalkDir;
    use std::sync::{Arc, Mutex};
    // initialized thread safe shared vector, so threads can write to w/o deadlock
    let bad_paths: Arc<Mutex<Vec<(PathBuf, String)>>> = Arc::new(Mutex::new(vec![]));
    // vector of join handles, so it can join all the threads at the end
    let mut threads = vec![];
    // loops over all members of directory recursively
    for entry in WalkDir::new(path) {
        let entry = entry?.path(); // gets path from entry
        let paths_mutex_clone = Arc::clone(&bad_paths); // makes a clone of the shared pointer for the thread, cuz the thread takes ownership
                                                        // adds threads to thread pool, where they can all be joined to main thread
        threads.push(thread::spawn(move || -> AvResult<()> {
            if entry.is_file() {
                let scan = scan_file(entry.to_owned())?;

                if !scan.0 {
                    paths_mutex_clone
                        .lock()
                        .expect("failed to get a lock from the mutex (poisioned mutex)")
                        .push((
                            entry.to_owned(),
                            match scan.1 {
                                Some(v) => v,
                                None => unreachable!(),
                            },
                        ))
                }
            }
            Ok(())
        }));
    }
    // Joins the threads, requiring for all of them to complete before execution can continue
    threads.into_par_iter().for_each(|thread| {
        thread
            .join()
            .expect("The thread creating or execution failed")
            .expect("an error occured in a thread:");
    });
    // assigns to `x` because `.to_vec()` cannot be done in temp value (i think, i dont remember it was something like that)
    let x = bad_paths
        .lock()
        .expect("failed to aquire lock (poisoned mutex)")
        .to_vec();
    Ok(x)
}

/// A Python module implemented in Rust.
#[pymodule]
fn av_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    // adds rust functions to python module
    m.add_function(wrap_pyfunction!(ensure_running, m)?)?;
    m.add_function(wrap_pyfunction!(scan_dir, m)?)?;
    m.add_function(wrap_pyfunction!(scan_file, m)?)?;
    Ok(())
}
