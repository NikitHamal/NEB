//! A member's public profile: `users/profile/<name>/` + `…/stats/`, with follow / unfollow.
use egui::{vec2, RichText, Ui};
use serde_json::Value;

use super::common::*;
use crate::actions::Action;
use crate::config::SITE_URL;
use crate::data::api::{b, n, s};
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Clone, Default)]
struct Member {
    id: String,
    username: String,
    name: String,
    photo: String,
    bio: String,
    role: String,
    school: String,
    verified: bool,
    followers: i64,
    following: i64,
    posts: i64,
    replies: i64,
    likes: i64,
    score: i64,
    is_following: bool,
    is_self: bool,
    private: bool,
}

#[derive(Default)]
pub struct UserState {
    for_user: String,
    task: Option<Task<Result<Member>>>,
    member: Option<Member>,
    error: Option<String>,
    follow: Option<Task<Result<Value>>>,
}

fn fetch(st: &mut UserState, env: &mut Env, username: &str) {
    st.for_user = username.to_string();
    st.member = None;
    st.error = None;
    let api = env.api();
    let name = username.to_string();
    st.task = Some(Task::spawn(&env.ctx, move || {
        let p = api.get(&format!("api/users/profile/{name}/"), &[])?;
        let stats = api.get(&format!("api/users/profile/{name}/stats/"), &[]).unwrap_or(Value::Null);
        let display = s(&p, "display_name");
        Ok(Member {
            id: s(&p, "id"),
            username: s(&p, "username"),
            name: if display.is_empty() { s(&p, "username") } else { display },
            photo: s(&p, "photo_url"),
            bio: s(&p, "bio"),
            role: s(&p, "role"),
            school: s(&p, "school"),
            verified: n(&p, "verification_level") > 0 || b(&p, "teacher_verified"),
            followers: n(&stats, "follower_count"),
            following: n(&stats, "following_count"),
            posts: n(&stats, "post_count"),
            replies: n(&stats, "reply_count"),
            likes: n(&stats, "likes_received"),
            score: n(&stats, "contribution_score"),
            is_following: b(&stats, "is_following"),
            is_self: b(&stats, "is_self"),
            private: b(&stats, "is_private"),
        })
    }));
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut UserState, username: &str) {
    let th = env.theme.clone();
    if st.for_user != username {
        fetch(st, env, username);
    }
    if let Some(t) = st.task.as_mut() {
        if let Some(r) = t.poll() {
            st.task = None;
            match r {
                Ok(m) => st.member = Some(m),
                Err(e) => {
                    if !env.handle_api_error(&e) {
                        st.error = Some(e.to_string());
                    }
                }
            }
        }
    }
    if let Some(t) = st.follow.as_mut() {
        if let Some(r) = t.poll() {
            st.follow = None;
            match r {
                Ok(v) => {
                    if let Some(m) = st.member.as_mut() {
                        let now = v.get("following").and_then(Value::as_bool).unwrap_or(!m.is_following);
                        if now != m.is_following {
                            m.followers += if now { 1 } else { -1 };
                        }
                        m.is_following = now;
                    }
                }
                Err(e) => {
                    env.handle_api_error(&e);
                    env.toast(e.to_string());
                }
            }
        }
    }
    scroll_page(ui, env, &format!("user-{username}"), |ui, env| {
        ui.horizontal(|ui| {
            if widgets::icon_button(ui, &th, Icon::Back, "Back", false).clicked() {
                env.act(Action::Back);
            }
            widgets::muted(ui, &th, "Profile");
        });
        ui.add_space(8.0);
        if !env.signed_in() {
            widgets::empty_state(ui, &th, Icon::User, "Sign in to view profiles", "Member profiles are visible to signed-in NEBians.");
            return;
        }
        if let Some(e) = st.error.clone() {
            let u = username.to_string();
            load_state(ui, &th, Some(e), || st.for_user = format!("~{u}"));
            return;
        }
        let Some(m) = st.member.clone() else {
            load_state(ui, &th, None, || {});
            return;
        };
        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            ui.horizontal(|ui| {
                crate::ui::remote_image::avatar(ui, &th, &m.name, 0, 92.0, &m.photo);
                ui.add_space(8.0);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 4.0;
                    ui.horizontal(|ui| {
                        widgets::label(ui, RichText::new(&m.name).font(fonts::bold(24.0)).color(th.p.ink));
                        if m.verified {
                            ui.label(crate::ui::icons::text(Icon::Verified, 20.0).color(th.p.accent));
                        }
                    });
                    widgets::muted(ui, &th, &format!("@{}", m.username));
                    widgets::flow(ui, |ui| {
                        if !m.role.is_empty() {
                            widgets::badge(ui, &m.role, th.p.accent, th.p.accent_soft);
                        }
                        if !m.school.is_empty() {
                            widgets::badge(ui, &m.school, th.p.ink_muted, th.p.field);
                        }
                    });
                });
            });
            if !m.bio.is_empty() {
                ui.add_space(12.0);
                ui.add(egui::Label::new(RichText::new(&m.bio).font(fonts::regular(14.5)).color(th.p.ink)));
            }
            ui.add_space(14.0);
            widgets::flow(ui, |ui| {
                if m.is_self {
                    if widgets::button(ui, &th, "Edit my profile", BtnKind::Secondary, Some(Icon::Edit), None).clicked() {
                        env.go(Route::Profile);
                    }
                } else {
                    let (label, kind, icon) = if m.is_following { ("Following", BtnKind::Secondary, Icon::Check) } else { ("Follow", BtnKind::Primary, Icon::Plus) };
                    if widgets::button(ui, &th, label, kind, Some(icon), None).clicked() && st.follow.is_none() && !m.id.is_empty() {
                        let api = env.api();
                        let id = m.id.clone();
                        st.follow = Some(Task::spawn(&env.ctx, move || api.post(&format!("api/users/{id}/follow/"), serde_json::json!({}))));
                    }
                }
                if widgets::button(ui, &th, "Open on the web", BtnKind::Secondary, Some(Icon::External), None).clicked() {
                    env.open_url(&format!("{SITE_URL}/profile/{}/", m.username));
                }
            });
        });
        ui.add_space(16.0);
        if m.private {
            widgets::empty_state(ui, &th, Icon::Lock, "This profile is private", "Follow them to see their activity once they accept.");
            return;
        }
        let stats = [("Followers", m.followers), ("Following", m.following), ("Posts", m.posts), ("Replies", m.replies), ("Likes received", m.likes), ("Contribution", m.score)];
        widgets::grid(ui, 150.0, 12.0, stats.len(), |ui, i, w| {
            widgets::card(ui, &th, vec2(w, 84.0), 14.0, |ui| {
                widgets::label(ui, RichText::new(stats[i].1.to_string()).font(fonts::bold(24.0)).color(th.p.ink));
                widgets::label(ui, RichText::new(stats[i].0).font(fonts::regular(12.5)).color(th.p.ink_muted));
            });
        });
    });
}

impl UserState {
    /// A sample member for the screenshot tour only (see `Env::demo`).
    pub fn demo(&mut self) {
        self.for_user = "anish_karki".into();
        self.member = Some(Member {
            id: "d".into(),
            username: "anish_karki".into(),
            name: "Anish Karki".into(),
            bio: "IOE 2083 aspirant. I write short Physics and Maths explainers and answer MCQ questions in the community.".into(),
            role: "student".into(),
            school: "Pulchowk Campus".into(),
            verified: true,
            followers: 148,
            following: 64,
            posts: 23,
            replies: 211,
            likes: 590,
            score: 1320,
            ..Default::default()
        });
    }
}
