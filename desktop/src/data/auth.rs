//! Email auth against the real NEBians API (same endpoints as the Android app:
//! `api/auth/email/{login,signup,verify,resend,forgot}/`).
use serde_json::{json, Value};

use crate::config::API_BASE;
use crate::data::store::Session;
use crate::errors::{AppError, Result};

fn post(path: &str, body: Value) -> Result<Value> {
    let url = format!("{API_BASE}{path}");
    let agent = ureq::AgentBuilder::new().timeout(std::time::Duration::from_secs(15)).build();
    match agent.post(&url).set("Accept", "application/json").send_json(body) {
        Ok(resp) => resp.into_json::<Value>().map_err(|e| AppError::Network(format!("Unexpected server reply: {e}"))),
        Err(ureq::Error::Status(code, resp)) => {
            let v: Value = resp.into_json().unwrap_or(Value::Null);
            let msg = v
                .get("error")
                .or_else(|| v.get("message"))
                .or_else(|| v.get("detail"))
                .and_then(|m| m.as_str())
                .map(str::to_owned)
                .unwrap_or_else(|| format!("The server answered with status {code}."));
            Err(AppError::Network(msg))
        }
        Err(e) => Err(AppError::Network(format!("Could not reach NEBians. Check your connection. ({e})"))),
    }
}

fn session_from(v: &Value, email: &str) -> Result<Session> {
    let token = v.get("authToken").and_then(Value::as_str).unwrap_or_default().to_string();
    let user = v.get("user").cloned().unwrap_or(Value::Null);
    let pick = |keys: &[&str]| keys.iter().find_map(|k| user.get(*k).and_then(Value::as_str)).unwrap_or_default().to_string();
    let username = pick(&["username", "handle", "displayName", "name"]);
    if token.is_empty() && username.is_empty() {
        return Err(AppError::Network("The server did not return a session.".into()));
    }
    Ok(Session { email: email.to_string(), username, token })
}

pub fn login(email: &str, password: &str) -> Result<Session> {
    let v = post("api/auth/email/login/", json!({ "email": email, "password": password }))?;
    session_from(&v, email)
}

/// Returns the server's message ("verification code sent …").
pub fn signup(email: &str, password: &str, username: &str, role: &str) -> Result<String> {
    let v = post("api/auth/email/signup/", json!({ "email": email, "password": password, "username": username, "role": role }))?;
    Ok(v.get("message").and_then(Value::as_str).unwrap_or("Check your inbox for a verification code.").to_string())
}

pub fn verify(email: &str, code: &str) -> Result<Session> {
    let v = post("api/auth/email/verify/", json!({ "email": email, "code": code }))?;
    session_from(&v, email)
}

pub fn resend(email: &str) -> Result<String> {
    let v = post("api/auth/email/resend/", json!({ "email": email }))?;
    Ok(v.get("message").and_then(Value::as_str).unwrap_or("A new code is on its way.").to_string())
}

pub fn forgot(email: &str) -> Result<String> {
    let v = post("api/auth/email/forgot/", json!({ "email": email }))?;
    Ok(v.get("message").and_then(Value::as_str).unwrap_or("If that address has an account, a reset code is on its way.").to_string())
}
