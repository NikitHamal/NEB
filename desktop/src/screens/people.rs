//! People — find members by name or username, or browse suggestions; opens their public profile.
use std::time::{Duration, Instant};

use egui::{vec2, RichText, Ui};
use serde_json::Value;

use super::common::*;
use crate::data::api::s;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Clone)]
pub struct Person {
    pub username: String,
    pub name: String,
    pub photo: String,
    pub bio: String,
}

#[derive(Default)]
pub struct PeopleState {
    query: String,
    last: String,
    changed: Option<Instant>,
    task: Option<Task<Result<Vec<Person>>>>,
    people: Vec<Person>,
    error: Option<String>,
    suggested: bool,
}

fn parse(v: &Value) -> Vec<Person> {
    let arr = v.as_array().cloned().or_else(|| ["users", "results", "suggestions"].iter().find_map(|k| v.get(*k).and_then(Value::as_array).cloned())).unwrap_or_default();
    arr.iter()
        .filter(|x| !s(x, "username").is_empty())
        .map(|x| Person { username: s(x, "username"), name: if s(x, "display_name").is_empty() { s(x, "username") } else { s(x, "display_name") }, photo: s(x, "photo_url"), bio: s(x, "bio") })
        .collect()
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut PeopleState) {
    let th = env.theme.clone();
    let signed = env.signed_in();
    if st.query != st.last {
        st.last = st.query.clone();
        st.changed = Some(Instant::now());
    }
    let q = st.query.trim().to_string();
    let fire = |st: &mut PeopleState, env: &mut Env, q: String| {
        let api = env.api();
        st.task = Some(Task::spawn(&env.ctx, move || {
            let v = if q.is_empty() { api.get("api/users/suggestions/", &[])? } else { api.get("api/users/search/", &[("q", q.as_str())])? };
            Ok(parse(&v))
        }));
    };
    if let Some(t0) = st.changed {
        if t0.elapsed() > Duration::from_millis(300) {
            st.changed = None;
            if q.is_empty() || q.chars().count() >= 2 {
                fire(st, env, q.clone());
            }
        } else {
            ui.ctx().request_repaint_after(Duration::from_millis(100));
        }
    }
    if !st.suggested && signed && st.task.is_none() {
        st.suggested = true;
        fire(st, env, String::new());
    }
    if let Some(t) = st.task.as_mut() {
        if let Some(r) = t.poll() {
            st.task = None;
            match r {
                Ok(p) => {
                    st.people = p;
                    st.error = None;
                }
                Err(e) => {
                    if !env.handle_api_error(&e) {
                        st.error = Some(e.to_string());
                    }
                }
            }
        }
    }
    scroll_page(ui, env, "people", |ui, env| {
        widgets::screen_header(ui, &th, "People", Some("Find classmates, teachers and contributors."));
        let w = ui.available_width();
        widgets::text_field(ui, &th, &mut st.query, "Search by name or username", Some(Icon::Search), w.min(560.0), false);
        ui.add_space(16.0);
        if !signed {
            widgets::empty_state(ui, &th, Icon::User, "Sign in to find people", "Profiles, follows and the community need a NEBians account.");
            ui.vertical_centered(|ui| {
                if widgets::button(ui, &th, "Sign in", BtnKind::Primary, Some(Icon::Login), None).clicked() {
                    env.act(crate::actions::Action::Replace(Route::Login));
                }
            });
            return;
        }
        if let Some(e) = &st.error {
            crate::screens::login::error_banner(ui, &th, e, w);
            return;
        }
        if st.task.is_some() && st.people.is_empty() {
            ui.add(egui::Spinner::new().size(26.0).color(th.p.accent));
            return;
        }
        if st.people.is_empty() {
            widgets::empty_state(ui, &th, Icon::User, "Nobody found", "Try a different name or username.");
            return;
        }
        widgets::section_header(ui, &th, if q.is_empty() { "Suggested for you" } else { "Results" }, None);
        widgets::grid(ui, 320.0, 12.0, st.people.len(), |ui, i, w| {
            let p = &st.people[i];
            let resp = widgets::card(ui, &th, vec2(w, 84.0), 14.0, |ui| {
                ui.horizontal(|ui| {
                    crate::ui::remote_image::avatar(ui, &th, &p.name, i, 50.0, &p.photo);
                    ui.vertical(|ui| {
                        ui.spacing_mut().item_spacing.y = 2.0;
                        ui.add(egui::Label::new(RichText::new(&p.name).font(fonts::bold(15.0)).color(th.p.ink)).truncate());
                        ui.add(egui::Label::new(RichText::new(format!("@{}", p.username)).font(fonts::regular(12.5)).color(th.p.ink_muted)).truncate());
                        if !p.bio.is_empty() {
                            ui.add(egui::Label::new(RichText::new(crate::util::truncate(&p.bio, 60)).font(fonts::regular(12.0)).color(th.p.ink_faint)).truncate());
                        }
                    });
                });
            });
            if resp.clicked() {
                env.go(Route::User(p.username.clone()));
            }
        });
    });
}

impl PeopleState {
    /// Sample members for the screenshot tour only (see `Env::demo`).
    pub fn demo(&mut self) {
        let mk = |u: &str, n: &str, b: &str| Person { username: u.into(), name: n.into(), photo: String::new(), bio: b.into() };
        self.people = vec![
            mk("anish_karki", "Anish Karki", "IOE 2083 · Physics and Maths tutor"),
            mk("sita_rai", "Sita Rai", "Class 12 Science, Pokhara"),
            mk("prabin_s", "Prabin Shrestha", "BCA first year — happy to help with C"),
            mk("mina_gurung", "Mina Gurung", "Biology teacher · CEE prep"),
            mk("rohan_t", "Rohan Thapa", "Class 11 · Chemistry notes"),
            mk("kabita_p", "Kabita Paudel", "Accountancy, Grade 10"),
        ];
        self.suggested = true;
    }
}
