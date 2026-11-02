//! One error type for the whole app, so screens can show a readable message.
use std::fmt;

#[derive(Debug)]
pub enum AppError {
    Io(std::io::Error),
    Json(serde_json::Error),
    /// Study content missing or malformed.
    Content(String),
    /// Talking to the NEBians server failed.
    Network(String),
    /// 401 — the bearer token is missing, expired or revoked.
    Unauthorized,
    /// 410 — the thing asked for is gone (expired sign-in request, deleted post).
    Gone(String),
}

pub type Result<T> = std::result::Result<T, AppError>;

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::Io(e) => write!(f, "File error: {e}"),
            AppError::Json(e) => write!(f, "Data error: {e}"),
            AppError::Content(m) => write!(f, "{m}"),
            AppError::Network(m) | AppError::Gone(m) => write!(f, "{m}"),
            AppError::Unauthorized => write!(f, "Your session has expired. Please sign in again."),
        }
    }
}

impl std::error::Error for AppError {}

impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self {
        AppError::Io(e)
    }
}

impl From<serde_json::Error> for AppError {
    fn from(e: serde_json::Error) -> Self {
        AppError::Json(e)
    }
}
