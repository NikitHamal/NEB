//! Data layer: models, the content loader (reads the repo's existing
//! `backend_python/web/data` JSON), persistence, background tasks, search, auth.
pub mod auth;
pub mod content;
pub mod models;
pub mod search;
pub mod store;
pub mod tasks;
