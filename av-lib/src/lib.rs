use clamav_client::{ping, Tcp};
use pyo3::prelude::*;
use rayon::prelude::*;
use runas::Command as RCommand;
use std::io;
use thiserror::Error;

static CLAMD_SOCKET: Tcp<&'static str> = Tcp {
    host_address: "localhost:3310",
};

#[derive(Error, Debug)]
enum FileScanError {
    #[error("io error occured while calling clamd's scan: {0}")]
    IoError(#[from] io::Error),
    #[error("utf8 error occured while getting clean data: {0}")]
    Utf8Error(#[from] std::str::Utf8Error),
}

#[derive(Error, Debug)]
enum AvLibError {
    #[error("an error occured file scanning a file: ({0})")]
    FileScanError(#[from] FileScanError),
    #[error("an error occured while walking through the filesystem: ({0})")]
    WalkError(#[from] jwalk::Error),
}

type AvResult<T> = Result<T, AvLibError>;

impl std::convert::From<AvLibError> for PyErr {
    fn from(err: AvLibError) -> PyErr {
        pyo3::exceptions::PyOSError::new_err(err.to_string())
    }
}
#[cfg(windows)]
fn activate_clamd() -> io::Result<()> {
    RCommand::new("net.exe")
        .arg("start")
        .arg("clamd")
        .status()?;
    Ok(())
}

#[cfg(linux)]
fn activate_clamd() -> io::Result<()> {
    use std::process::Command;
    Command::new("systemctl")
        .arg("start")
        .arg("clamd")
        .status()?;

    Ok(())
}

/// Formats the sum of two numbers as string.
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

/// Scans a single file, with a bool result if it is clean
#[pyfunction]
fn scan_file(path: PathBuf) -> AvResult<(bool, Option<String>)> {
    let res = match clamav_client::scan_file(path, CLAMD_SOCKET, None) {
        Ok(v) => AvResult::Ok(v),
        Err(err) => AvResult::Err(AvLibError::FileScanError(FileScanError::IoError(err))),
    }?;

    let out = match std::str::from_utf8(&res) {
        Ok(v) => AvResult::Ok(v),
        Err(err) => AvResult::Err(AvLibError::FileScanError(FileScanError::Utf8Error(err))),
    }?;
    let mut name = None;
    if out.contains("FOUND") {
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
    let bad_paths: Arc<Mutex<Vec<(PathBuf, String)>>> = Arc::new(Mutex::new(vec![]));
    let mut threads = vec![];
    for entry in WalkDir::new(path) {
        let entry = entry?.path();
        //println!("{entry:#?}");
        let paths_mutex_clone = Arc::clone(&bad_paths);
        threads.push(thread::spawn(move || -> AvResult<()> {
            let scan = scan_file(entry.to_owned())?;
            if entry.is_file() && !scan.0 {
                paths_mutex_clone
                    .lock()
                    .unwrap()
                    .push((entry.to_owned(), scan.1.unwrap()))
            }
            Ok(())
        }));
    }

    threads.into_par_iter().for_each(|thread| {
        thread
            .join()
            .expect("The thread creating or execution failed !")
            .unwrap()
    });
    let x = bad_paths.lock().unwrap().to_vec();
    Ok(x)
}

/// A Python module implemented in Rust.
#[pymodule]
fn av_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ensure_running, m)?)?;
    m.add_function(wrap_pyfunction!(scan_dir, m)?)?;
    m.add_function(wrap_pyfunction!(scan_file, m)?)?;
    Ok(())
}
