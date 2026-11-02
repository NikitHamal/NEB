//! Everything that ties the local app to the NEBians account: the bearer token, the unread
//! notification badge, pulling/pushing the profile, and signing out. Implemented as an
//! `impl Env` block so screens just call `env.api()`, `env.signed_in()`, …
use std::time::{Duration, Instant};

use serde_json::{json, Value};

use crate::actions::Action;
use crate::data::api::{s, Api};
use crate::data::auth;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::{AppError, Result};
use crate::router::Route;

#[derive(Default)]
pub struct ServerState {
    pub unread: u32,
    unread_task: Option<Task<Result<u32>>>,
    unread_at: Option<Instant>,
    pull_task: Option<Task<Result<Value>>>,
    push_task: Option<Task<Result<Value>>>,
}

impl ServerState {
    pub fn refresh_unread_soon(&mut self) {
        self.unread_at = None;
    }
}

impl Env {
    pub fn token(&self) -> Option<String> {
        self.store.s.session.as_ref().map(|s| s.token.clone()).filter(|t| !t.is_empty())
    }

    pub fn signed_in(&self) -> bool {
        self.token().is_some()
    }

    pub fn api(&self) -> Api {
        Api::new(self.token())
    }

    /// The signed-in user's handle (what the API calls `username`).
    pub fn my_username(&self) -> String {
        match &self.store.s.session {
            Some(sess) if !sess.username.is_empty() => sess.username.clone(),
            _ => self.store.s.profile.handle.clone(),
        }
    }

    /// Per-frame: finish background jobs and schedule the periodic unread-count refresh.
    pub fn server_poll(&mut self) {
        if !self.signed_in() {
            self.srv = Default::default();
            return;
        }
        if self.demo {
            return;
        }
        let mut err: Option<AppError> = None;
        if let Some(t) = self.srv.unread_task.as_mut() {
            if let Some(r) = t.poll() {
                self.srv.unread_task = None;
                match r {
                    Ok(n) => self.srv.unread = n,
                    Err(e) => err = Some(e),
                }
            }
        }
        if let Some(t) = self.srv.pull_task.as_mut() {
            if let Some(r) = t.poll() {
                self.srv.pull_task = None;
                match r {
                    Ok(v) => self.merge_profile(&v),
                    Err(e) => err = Some(e),
                }
            }
        }
        if let Some(t) = self.srv.push_task.as_mut() {
            if let Some(r) = t.poll() {
                self.srv.push_task = None;
                match r {
                    Ok(_) => {}
                    Err(AppError::Unauthorized) => err = Some(AppError::Unauthorized),
                    Err(e) => self.toast(format!("Profile not saved to your account: {e}")),
                }
            }
        }
        if let Some(e) = err {
            self.handle_api_error(&e);
            return;
        }
        let due = self.srv.unread_at.map(|t| t.elapsed() > Duration::from_secs(60)).unwrap_or(true);
        if due && self.srv.unread_task.is_none() {
            self.srv.unread_at = Some(Instant::now());
            let api = self.api();
            self.srv.unread_task = Some(Task::spawn(&self.ctx, move || {
                let v = api.get("api/notifications/unread-count/", &[])?;
                Ok(v.get("count").and_then(Value::as_u64).unwrap_or(0) as u32)
            }));
        }
        self.ctx.request_repaint_after(Duration::from_secs(30));
    }

    /// `true` when `e` was an expired session (it has been dropped and the user sent to sign in).
    pub fn handle_api_error(&mut self, e: &AppError) -> bool {
        if matches!(e, AppError::Unauthorized) && self.store.s.session.is_some() {
            self.store.s.session = None;
            self.store.touch();
            self.srv = Default::default();
            self.toast("Your session expired. Please sign in again.");
            self.act(Action::Replace(Route::Login));
            return true;
        }
        false
    }

    /// Download the account's profile and merge it into the local one.
    pub fn pull_profile(&mut self) {
        if !self.signed_in() || self.demo || self.srv.pull_task.is_some() {
            return;
        }
        let api = self.api();
        let user = self.my_username();
        if user.is_empty() {
            return;
        }
        self.srv.pull_task = Some(Task::spawn(&self.ctx, move || api.get(&format!("api/users/profile/{user}/"), &[])));
    }

    fn merge_profile(&mut self, v: &Value) {
        let p = &mut self.store.s.profile;
        let set = |dst: &mut String, src: String| {
            if !src.is_empty() {
                *dst = src;
            }
        };
        set(&mut p.display_name, s(v, "display_name"));
        set(&mut p.handle, s(v, "username"));
        set(&mut p.role, s(v, "role"));
        set(&mut p.bio, s(v, "bio"));
        set(&mut p.level, s(v, "class"));
        set(&mut p.pradesh, s(v, "pradesh"));
        set(&mut p.district, s(v, "district"));
        set(&mut p.school, s(v, "school"));
        set(&mut p.institution_type, s(v, "institution_type"));
        set(&mut p.dob, s(v, "dob"));
        set(&mut p.gender, s(v, "gender"));
        let subs = s(v, "subjects");
        if !subs.is_empty() {
            p.subjects = subs.split(',').map(|x| x.trim().to_string()).filter(|x| !x.is_empty()).collect();
        }
        if let Some(sess) = self.store.s.session.as_mut() {
            let name = s(v, "username");
            if !name.is_empty() {
                sess.username = name;
            }
            let photo = s(v, "photo_url");
            if !photo.is_empty() {
                sess.photo_url = photo;
            }
        }
        self.store.touch();
    }

    /// Upload the local profile to the account (best effort, silent on success).
    pub fn push_profile(&mut self) {
        if !self.signed_in() || self.demo {
            return;
        }
        let p = self.store.s.profile.clone();
        let username = self.my_username();
        if username.is_empty() {
            return;
        }
        let mut body = json!({ "username": username });
        let mut put = |k: &str, val: String| {
            if !val.is_empty() {
                body[k] = Value::String(val);
            }
        };
        put("display_name", p.display_name);
        put("role", p.role);
        put("bio", p.bio);
        put("class_level", p.level);
        put("subjects", p.subjects.join(","));
        put("pradesh", p.pradesh);
        put("district", p.district);
        put("school", p.school);
        put("institution_type", p.institution_type);
        put("dob", p.dob);
        put("gender", p.gender);
        let api = self.api();
        self.srv.push_task = Some(Task::spawn(&self.ctx, move || api.post("api/users/profile/", body)));
    }

    /// Revoke the token server-side (fire and forget) and forget the account locally.
    pub fn sign_out(&mut self) {
        if let Some(t) = self.token() {
            std::thread::spawn(move || auth::logout(&t));
        }
        self.store.s.session = None;
        self.store.s.guest = false;
        self.store.s.onboarded = false;
        self.store.s.profile = Default::default();
        self.store.touch();
        self.srv = Default::default();
    }
}
