use clamav_client::{ping, Tcp};
use pyo3::prelude::*;
use std::io;
use std::sync::OnceLock;

static CLAMD_SOCKET: Tcp<&'static str> = Tcp {
    host_address: "localhost:3310",
};

#[cfg(windows)]
fn activate_clamd() -> io::Result<()> {
    use windows_service::service_dispatcher::start;

    Ok(())
}

#[cfg(unix)]
fn activate_clamd() -> io::Result<()> {
    Ok(())
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn initiate_scan() {
    match ping(CLAMD_SOCKET) {
        Ok(v) => {
            if (v == clamav_client::PONG) {
            } else {
                panic!("server will never not return PONG")
            }
        }
        Err(err) => activate_clamd().expect("Server should've started"),
    };
    println!("server is working");
}

/// A Python module implemented in Rust.
#[pymodule]
fn av_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(initiate_scan, m)?)?;
    Ok(())
}
