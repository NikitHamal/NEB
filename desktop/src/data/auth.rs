//! Email auth against the real NEBians API (same endpoints as the Android app):
//! `api/auth/email/{login,signup,verify,resend,forgot,reset-password}/`, plus logout.
use serde_json::{json, Value};

use crate::data::api::{s, Api};
use crate::data::store::Session;
use crate::errors::{AppError, Result};

impl Session {
    /// Build a session from any auth reply (`{authToken, user:{…}}`).
    pub fn from_reply(v: &Value, email: &str, provider: &str) -> Result<Session> {
        let token = s(v, "authToken");
        let user = v.get("user").cloned().unwrap_or(Value::Null);
        let pick = |keys: &[&str]| keys.iter().map(|k| s(&user, k)).find(|x| !x.is_empty()).unwrap_or_default();
        let username = pick(&["username", "handle"]);
        if token.is_empty() {
            return Err(AppError::Network("The server did not return a session.".into()));
        }
        let mail = pick(&["email"]);
        Ok(Session {
            email: if mail.is_empty() { email.to_string() } else { mail },
            username,
            token,
            user_id: pick(&["id", "uid"]),
            display_name: pick(&["display_name", "displayName", "name"]),
            photo_url: pick(&["photo_url", "photoUrl"]),
            provider: provider.to_string(),
        })
    }
}

fn msg(v: &Value, default: &str) -> String {
    let m = s(v, "message");
    if m.is_empty() { default.to_string() } else { m }
}

pub fn login(email: &str, password: &str) -> Result<Session> {
    let v = Api::anon().post("api/auth/email/login/", json!({ "email": email, "password": password }))?;
    Session::from_reply(&v, email, "email")
}

/// Returns the server's message ("verification code sent …").
pub fn signup(email: &str, password: &str, username: &str, role: &str) -> Result<String> {
    let v = Api::anon().post("api/auth/email/signup/", json!({ "email": email, "password": password, "username": username, "role": role }))?;
    Ok(msg(&v, "Check your inbox for a verification code."))
}

pub fn verify(email: &str, code: &str) -> Result<Session> {
    let v = Api::anon().post("api/auth/email/verify/", json!({ "email": email, "code": code }))?;
    Session::from_reply(&v, email, "email")
}

pub fn resend(email: &str) -> Result<String> {
    let v = Api::anon().post("api/auth/email/resend/", json!({ "email": email }))?;
    Ok(msg(&v, "A new code is on its way."))
}

pub fn forgot(email: &str) -> Result<String> {
    let v = Api::anon().post("api/auth/email/forgot/", json!({ "email": email }))?;
    Ok(msg(&v, "If that address has an account, a reset code is on its way."))
}

pub fn reset_password(email: &str, code: &str, new_password: &str) -> Result<Session> {
    let v = Api::anon().post(
        "api/auth/email/reset-password/",
        json!({ "email": email, "code": code, "newPassword": new_password, "confirmPassword": new_password }),
    )?;
    Session::from_reply(&v, email, "email")
}

pub fn change_password(token: &str, current: &str, new_password: &str) -> Result<String> {
    let v = Api::new(Some(token.to_string())).post("api/auth/change-password/", json!({ "currentPassword": current, "newPassword": new_password }))?;
    Ok(msg(&v, "Password changed. Other devices were signed out."))
}

/// Revoke the bearer token on the server. Best effort — the local session is dropped regardless.
pub fn logout(token: &str) {
    let _ = Api::new(Some(token.to_string())).post("api/auth/logout/", json!({}));
}
