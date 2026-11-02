//! Google / GitHub sign-in through the user's browser, using the backend's PKCE-style hand-off
//! (`api/auth/desktop/{start,poll}/` + the `/desktop-auth/` consent page).
//!
//! 1. We generate a random `verifier` that never leaves this process and send only
//!    `challenge = base64url(sha256(verifier))`.
//! 2. The server returns `state` + a `loginUrl`; we open that URL in the browser. There the user
//!    signs in with Google / GitHub / email (the website's normal login) and taps *Allow*.
//! 3. We poll with `{state, verifier}`. Only the holder of the verifier can collect the one-time
//!    bearer token, so nobody watching the URL or the browser can steal the session.
use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};

use crate::config::VERSION;
use crate::data::api::{b, n, s, Api};
use crate::data::store::Session;
use crate::errors::{AppError, Result};

pub struct Handoff {
    pub state: String,
    pub login_url: String,
    verifier: String,
    pub interval_secs: u64,
    pub expires_secs: u64,
}

impl Handoff {
    /// A made-up hand-off for the screenshot tour (never sent anywhere).
    pub fn demo() -> Self {
        Handoff { state: "demo".into(), login_url: "https://nebians.consica.com.np/desktop-auth/?state=Xk3mQ9vT2pLwR8aZ".into(), verifier: String::new(), interval_secs: 2, expires_secs: 600 }
    }
}

pub enum Poll {
    Pending,
    Done { session: Session, is_new: bool },
}

fn device_name() -> String {
    let os = match std::env::consts::OS {
        "windows" => "Windows",
        "macos" => "macOS",
        "linux" => "Linux",
        other => other,
    };
    format!("{os} · NEBians Desktop {VERSION}")
}

pub fn start() -> Result<Handoff> {
    let mut raw = [0u8; 32];
    getrandom::getrandom(&mut raw).map_err(|e| AppError::Network(format!("No secure random source available: {e}")))?;
    let verifier = URL_SAFE_NO_PAD.encode(raw); // 43 chars, RFC 7636 charset
    let challenge = URL_SAFE_NO_PAD.encode(Sha256::digest(verifier.as_bytes()));
    let v = Api::anon().post("api/auth/desktop/start/", json!({ "challenge": challenge, "device": device_name() }))?;
    let state = s(&v, "state");
    let login_url = s(&v, "loginUrl");
    if state.is_empty() || !login_url.starts_with("http") {
        return Err(AppError::Network("The server did not start a sign-in request.".into()));
    }
    Ok(Handoff {
        state,
        login_url,
        verifier,
        interval_secs: (n(&v, "interval").max(1) as u64).min(10),
        expires_secs: n(&v, "expiresIn").max(60) as u64,
    })
}

pub fn poll(h: &Handoff) -> Result<Poll> {
    let v = Api::anon().post("api/auth/desktop/poll/", json!({ "state": h.state, "verifier": h.verifier }))?;
    if s(&v, "status") == "success" {
        let session = Session::from_reply(&v, "", "browser")?;
        return Ok(Poll::Done { session, is_new: b(&v, "isNewUser") });
    }
    Ok(Poll::Pending)
}

#[allow(dead_code)]
pub fn user_of(v: &Value) -> Value {
    v.get("user").cloned().unwrap_or(Value::Null)
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Live end-to-end test against a running backend (`NEB_API_BASE=http://127.0.0.1:8765/`).
    /// Another process (scripts/e2e-handoff.py) plays the browser: it reads the login URL from
    /// /tmp/handoff_url, signs in on the website and presses *Allow*.
    #[test]
    #[ignore]
    fn live_handoff() {
        let h = start().expect("start");
        std::fs::write("/tmp/handoff_url", &h.login_url).unwrap();
        for _ in 0..60 {
            match poll(&h).expect("poll") {
                Poll::Done { session, is_new } => {
                    assert!(!session.token.is_empty());
                    println!("SESSION user={} is_new={} provider={}", session.username, is_new, session.provider);
                    let api = Api::new(Some(session.token.clone()));
                    let v = api.get("api/notifications/unread-count/", &[]).expect("bearer works");
                    println!("AUTHED unread-count reply: {v}");
                    assert!(Api::new(Some("not-a-token".into())).get("api/notifications/unread-count/", &[]).is_err());
                    // the one-time record is gone: polling again must fail
                    assert!(poll(&h).is_err(), "second redemption must be refused");
                    return;
                }
                Poll::Pending => std::thread::sleep(std::time::Duration::from_secs(1)),
            }
        }
        panic!("approval never arrived");
    }
}
