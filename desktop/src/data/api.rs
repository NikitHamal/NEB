//! Authenticated JSON client for the NEBians API (`API_BASE`), the same endpoints the Android
//! app uses. Blocking `ureq` calls — always run them inside a `data::tasks::Task`.
//!
//! * Bearer token goes in the `Authorization` header only (never a URL).
//! * `401` becomes `AppError::Unauthorized` so the UI can drop a dead session.
//! * Server error bodies (`{"error": "..."}`) are surfaced verbatim to the user.
use std::time::Duration;

use serde_json::Value;

use crate::config::{api_base, VERSION};
use crate::errors::{AppError, Result};

#[derive(Clone, Default)]
pub struct Api {
    token: Option<String>,
}

impl Api {
    pub fn new(token: Option<String>) -> Self {
        Self { token: token.filter(|t| !t.is_empty()) }
    }

    pub fn anon() -> Self {
        Self { token: None }
    }

    fn agent() -> ureq::Agent {
        ureq::AgentBuilder::new()
            .timeout(Duration::from_secs(20))
            .user_agent(&format!("NEBians-Desktop/{VERSION}"))
            .build()
    }

    fn request(&self, method: &str, path: &str, query: &[(&str, &str)]) -> ureq::Request {
        let mut r = Self::agent().request(method, &format!("{}{path}", api_base())).set("Accept", "application/json");
        if let Some(t) = &self.token {
            r = r.set("Authorization", &format!("Bearer {t}"));
        }
        for (k, v) in query {
            r = r.query(k, v);
        }
        r
    }

    fn finish(res: std::result::Result<ureq::Response, ureq::Error>) -> Result<Value> {
        match res {
            Ok(resp) => {
                let text = resp.into_string().map_err(|e| AppError::Network(format!("Unexpected server reply: {e}")))?;
                if text.trim().is_empty() {
                    return Ok(Value::Null);
                }
                serde_json::from_str(&text).map_err(|e| AppError::Network(format!("Unexpected server reply: {e}")))
            }
            Err(ureq::Error::Status(code, resp)) => {
                let v: Value = resp.into_json().unwrap_or(Value::Null);
                let msg = ["error", "message", "detail"]
                    .iter()
                    .find_map(|k| v.get(*k).and_then(Value::as_str))
                    .map(str::to_owned)
                    .unwrap_or_else(|| format!("The server answered with status {code}."));
                match code {
                    401 => Err(AppError::Unauthorized),
                    410 => Err(AppError::Gone(msg)),
                    _ => Err(AppError::Network(msg)),
                }
            }
            Err(e) => Err(AppError::Network(format!("Could not reach NEBians. Check your connection. ({e})"))),
        }
    }

    pub fn get(&self, path: &str, query: &[(&str, &str)]) -> Result<Value> {
        Self::finish(self.request("GET", path, query).call())
    }

    pub fn post(&self, path: &str, body: Value) -> Result<Value> {
        Self::finish(self.request("POST", path, &[]).send_json(body))
    }
}

/// `v[a][b]…` as a string, or "".
pub fn s(v: &Value, key: &str) -> String {
    v.get(key).and_then(Value::as_str).unwrap_or_default().to_string()
}
pub fn n(v: &Value, key: &str) -> i64 {
    v.get(key).and_then(Value::as_i64).unwrap_or(0)
}
pub fn b(v: &Value, key: &str) -> bool {
    v.get(key).and_then(Value::as_bool).unwrap_or(false)
}
