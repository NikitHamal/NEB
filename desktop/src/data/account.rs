//! Account management against the real NEBians API — everything the website's account pages do,
//! driven from native screens: security overview, email change (request → code → confirm),
//! set/change password, availability of a handle, and the 30-day account deletion request.
use serde_json::{json, Value};

use crate::data::api::{b, n, s, Api};
use crate::data::store::Session;
use crate::errors::Result;

#[derive(Clone, Debug, Default)]
pub struct Security {
    pub email: String,
    pub email_verified: bool,
    pub has_password: bool,
    pub pending_email: String,
}

#[derive(Clone, Debug, Default)]
pub struct Deletion {
    pub pending: bool,
    /// Unix milliseconds the account is scheduled to be erased.
    pub scheduled_ms: i64,
}

fn msg(v: &Value, default: &str) -> String {
    let m = s(v, "message");
    if m.is_empty() { default.to_string() } else { m }
}

pub fn security(api: &Api) -> Result<Security> {
    let v = api.get("api/auth/account-security/", &[])?;
    Ok(Security { email: s(&v, "email"), email_verified: b(&v, "emailVerified"), has_password: b(&v, "hasPassword"), pending_email: s(&v, "pendingEmail") })
}

pub fn request_email_change(api: &Api, new_email: &str, password: &str) -> Result<String> {
    let v = api.post("api/auth/email/change/request/", json!({ "newEmail": new_email, "password": password }))?;
    Ok(msg(&v, "A code is on its way to the new address."))
}

/// On success the server revokes every other token and hands back a fresh one.
pub fn confirm_email_change(api: &Api, code: &str, old: &Session) -> Result<Session> {
    let v = api.post("api/auth/email/change/confirm/", json!({ "code": code }))?;
    let mut sess = Session::from_reply(&v, &old.email, &old.provider)?;
    if sess.photo_url.is_empty() {
        sess.photo_url = old.photo_url.clone();
    }
    Ok(sess)
}

pub fn cancel_email_change(api: &Api) -> Result<String> {
    let v = api.post("api/auth/email/change/cancel/", json!({}))?;
    Ok(msg(&v, "Email change cancelled."))
}

pub fn set_password(api: &Api, password: &str) -> Result<String> {
    let v = api.post("api/auth/set-password/", json!({ "password": password }))?;
    Ok(msg(&v, "Password set."))
}

pub fn deletion_status(api: &Api) -> Result<Deletion> {
    let v = api.get("api/users/me/delete-account/", &[])?;
    let req = v.get("request").cloned().unwrap_or(Value::Null);
    Ok(Deletion { pending: b(&v, "hasPending"), scheduled_ms: n(&req, "scheduledDeleteAt") })
}

pub fn request_deletion(api: &Api, reason: &str) -> Result<Deletion> {
    let v = api.post("api/users/me/delete-account/", json!({ "reason": reason }))?;
    let req = v.get("request").cloned().unwrap_or(Value::Null);
    Ok(Deletion { pending: true, scheduled_ms: n(&req, "scheduledDeleteAt") })
}

pub fn cancel_deletion(api: &Api) -> Result<()> {
    api.delete("api/users/me/delete-account/")?;
    Ok(())
}
