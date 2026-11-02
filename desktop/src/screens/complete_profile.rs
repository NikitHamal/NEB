//! First-run step after Google / GitHub sign-up (Android `CompleteProfile`): pick a public
//! username (checked live against the server), a display name and what you are.
use std::time::{Duration, Instant};

use egui::{Align, Layout, RichText, Ui};
use serde_json::json;

use crate::actions::Action;
use crate::data::api::b;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct CompleteState {
    init: bool,
    username: String,
    display: String,
    role: String,
    checked: String,
    available: Option<bool>,
    typed_at: Option<Instant>,
    check: Option<Task<Result<bool>>>,
    save: Option<Task<Result<()>>>,
    error: Option<String>,
}

fn valid_handle(h: &str) -> bool {
    (3..=24).contains(&h.len()) && h.chars().all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '_' || c == '.')
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut CompleteState) {
    let th = env.theme.clone();
    if !st.init {
        st.init = true;
        let me = env.my_username();
        let temp = me.starts_with("user_") || me.starts_with("github_");
        st.username = if temp { String::new() } else { me };
        st.display = env.store.s.profile.display_name.clone();
        st.role = if env.store.s.profile.role.is_empty() { "student".into() } else { env.store.s.profile.role.clone() };
    }
    // live availability check, debounced
    if let Some(t) = st.check.as_mut() {
        if let Some(r) = t.poll() {
            st.check = None;
            if let Ok(a) = r {
                st.available = Some(a);
            }
        }
    }
    let handle = st.username.trim().to_lowercase();
    if handle != st.checked && valid_handle(&handle) && st.check.is_none() && st.typed_at.map(|t| t.elapsed() > Duration::from_millis(450)).unwrap_or(false) {
        st.checked = handle.clone();
        let q = handle.clone();
        let api = env.api();
        st.check = Some(Task::spawn(&env.ctx, move || {
            let v = api.get("api/users/check-username/", &[("username", &q)])?;
            Ok(b(&v, "available"))
        }));
    }
    if let Some(t) = st.save.as_mut() {
        if let Some(r) = t.poll() {
            st.save = None;
            match r {
                Ok(()) => {
                    let p = &mut env.store.s.profile;
                    p.handle = handle.clone();
                    p.display_name = st.display.trim().to_string();
                    p.role = st.role.clone();
                    if let Some(s) = env.store.s.session.as_mut() {
                        s.username = handle.clone();
                    }
                    env.store.touch();
                    let next = if env.store.s.onboarded { Route::Home } else { Route::Onboarding };
                    env.act(Action::Replace(next));
                }
                Err(e) => {
                    if !env.handle_api_error(&e) {
                        st.error = Some(e.to_string());
                    }
                }
            }
        }
    }
    let busy = st.save.is_some();
    egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| {
        let avail = ui.available_size();
        let w = (avail.x - 48.0).clamp(300.0, 440.0);
        ui.allocate_ui_with_layout(avail, Layout::top_down(Align::Center), |ui| {
            ui.set_width(w);
            ui.add_space(((avail.y - 560.0) / 2.0).max(24.0));
            env.logo.show(ui, 56.0);
            ui.add_space(18.0);
            widgets::label(ui, RichText::new("Finish your profile").font(fonts::bold(28.0)).color(th.p.ink));
            ui.add_space(6.0);
            ui.add(egui::Label::new(RichText::new("Pick the name people will see in the community.").font(fonts::regular(15.0)).color(th.p.ink_muted)).selectable(false));
            ui.add_space(24.0);
            ui.add_enabled_ui(!busy, |ui| {
                let bad = !handle.is_empty() && (!valid_handle(&handle) || st.available == Some(false) && st.checked == handle);
                let before = st.username.clone();
                widgets::field(ui, &th, &mut st.username, "Username", Some(Icon::Tag), w, false, bad);
                if st.username != before {
                    st.typed_at = Some(Instant::now());
                    st.available = None;
                    st.error = None;
                }
                let (msg, col) = if handle.is_empty() {
                    ("Lowercase letters, numbers, dots and underscores.".to_string(), th.p.ink_faint)
                } else if !valid_handle(&handle) {
                    ("3–24 characters: a–z, 0–9, dot or underscore.".to_string(), th.p.danger)
                } else if st.checked == handle && st.available == Some(true) {
                    (format!("@{handle} is available"), th.p.ok)
                } else if st.checked == handle && st.available == Some(false) {
                    (format!("@{handle} is taken"), th.p.danger)
                } else {
                    ("Checking availability…".to_string(), th.p.ink_faint)
                };
                ui.add(egui::Label::new(RichText::new(msg).font(fonts::regular(12.5)).color(col)));
                ui.add_space(10.0);
                widgets::field(ui, &th, &mut st.display, "Display name", Some(Icon::Badge), w, false, false);
                ui.add_space(16.0);
                widgets::label(ui, RichText::new("I am a").font(fonts::medium(13.5)).color(th.p.ink_muted));
                ui.add_space(6.0);
                ui.horizontal_wrapped(|ui| {
                    for (key, label) in [("student", "Student"), ("teacher", "Teacher"), ("explorer", "Explorer")] {
                        if widgets::chip(ui, &th, label, st.role == key).clicked() {
                            st.role = key.into();
                        }
                    }
                });
            });
            if let Some(e) = st.error.clone() {
                ui.add_space(12.0);
                super::login::error_banner(ui, &th, &e, w);
            }
            ui.add_space(22.0);
            let ready = valid_handle(&handle) && st.available != Some(false) && !st.display.trim().is_empty();
            ui.add_enabled_ui(ready && !busy, |ui| {
                if widgets::button_sized(ui, &th, if busy { "Saving…" } else { "Continue" }, BtnKind::Primary, None, Some(w), 56.0).clicked() {
                    let api = env.api();
                    let body = json!({ "username": handle, "display_name": st.display.trim(), "role": st.role });
                    st.save = Some(Task::spawn(&env.ctx, move || api.post("api/users/profile/", body).map(|_| ())));
                }
            });
        });
    });
}
