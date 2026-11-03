//! Notifications — `api/notifications/` with unread styling, mark-all-read, and deep links
//! into the community thread a notification refers to.
#![allow(dead_code)] // wire/icon sets mirror the server and Material font in full
use egui::{vec2, Align, Layout, Rounding, Sense, Stroke, Ui};
use serde_json::{json, Value};

use super::common::*;
use super::community::time_ago;
use crate::data::api::{b, n, s};
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::{self, Icon};
use crate::ui::widgets::{self, BtnKind};

#[derive(Clone)]
struct Item {
    id: String,
    message: String,
    verb: String,
    target_type: String,
    target_id: String,
    read: bool,
    created: i64,
    actor: String,
    photo: String,
}

#[derive(Default)]
pub struct NotificationsState {
    items: Vec<Item>,
    loaded: bool,
    load: Option<Task<Result<Vec<Item>>>>,
    mark: Option<Task<Result<Value>>>,
    error: Option<String>,
}

fn icon_for(verb: &str) -> Icon {
    match verb {
        v if v.contains("like") => Icon::ThumbUpFilled,
        v if v.contains("reply") || v.contains("comment") || v.contains("mention") => Icon::Chat,
        v if v.contains("follow") => Icon::PersonAdd,
        v if v.contains("resource") || v.contains("approved") => Icon::File,
        _ => Icon::Bell,
    }
}

/// (headline, optional detail) — the server's message when it has one, otherwise a sentence built from the verb.
fn describe(it: &Item, who: &str) -> (String, String) {
    let msg = it.message.trim();
    let sentence = match it.verb.as_str() {
        v if v.contains("reply") => format!("{who} replied to your post"),
        v if v.contains("comment") => format!("{who} commented on your resource"),
        v if v.contains("like") => format!("{who} liked your {}", if it.target_type.contains("reply") { "reply" } else { "post" }),
        v if v.contains("follow") => format!("{who} started following you"),
        v if v.contains("mention") => format!("{who} mentioned you"),
        "resource_approved" => "Your resource was approved — it is now visible to everyone".to_string(),
        "resource_rejected" => "Your resource wasn't approved".to_string(),
        other => {
            let t = other.replace('_', " ");
            if it.actor.is_empty() { t } else { format!("{who} · {t}") }
        }
    };
    if msg.is_empty() {
        (sentence, String::new())
    } else if msg.to_lowercase().contains(&who.to_lowercase()) || it.actor.is_empty() {
        (msg.to_string(), String::new())
    } else {
        (sentence, crate::util::truncate(msg, 140))
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut NotificationsState) {
    let th = env.theme.clone();
    if env.signed_in() && !st.loaded && st.load.is_none() && !env.demo {
        let api = env.api();
        st.load = Some(Task::spawn(&env.ctx, move || {
            let v = api.get("api/notifications/", &[])?;
            Ok(v.get("notifications")
                .and_then(Value::as_array)
                .map(|a| {
                    a.iter()
                        .map(|x| Item {
                            id: s(x, "id"),
                            message: s(x, "message"),
                            verb: s(x, "verb"),
                            target_type: if s(x, "targetType").is_empty() { s(x, "referenceType") } else { s(x, "targetType") },
                            target_id: if s(x, "targetId").is_empty() { s(x, "referenceId") } else { s(x, "targetId") },
                            read: b(x, "isRead"),
                            created: n(x, "createdAt"),
                            actor: s(x, "actorName"),
                            photo: s(x, "actorPhotoUrl"),
                        })
                        .collect()
                })
                .unwrap_or_default())
        }));
    }
    if let Some(t) = st.load.as_mut() {
        if let Some(r) = t.poll() {
            st.load = None;
            st.loaded = true;
            match r {
                Ok(items) => {
                    st.items = items;
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
    if let Some(t) = st.mark.as_mut() {
        if let Some(r) = t.poll() {
            st.mark = None;
            if let Err(e) = r {
                env.handle_api_error(&e);
            }
        }
    }
    scroll_page(ui, env, "notifications", |ui, env| {
        let w = ui.available_width();
        ui.horizontal(|ui| {
            ui.vertical(|ui| {
                widgets::heading(ui, &th, "Notifications", 30.0);
                let unread = st.items.iter().filter(|i| !i.read).count();
                widgets::muted(ui, &th, &if unread > 0 { format!("{unread} unread") } else { "You're all caught up".to_string() });
            });
            right(ui, |ui| {
                if env.signed_in() {
                    if widgets::icon_button(ui, &th, Icon::Refresh, "Refresh", false).clicked() {
                        st.loaded = false;
                        env.srv.refresh_unread_soon();
                    }
                    if st.items.iter().any(|i| !i.read) && widgets::button(ui, &th, "Mark all read", BtnKind::Tonal, Some(Icon::Done), None).clicked() {
                        for i in st.items.iter_mut() {
                            i.read = true;
                        }
                        env.srv.unread = 0;
                        let api = env.api();
                        st.mark = Some(Task::spawn(&env.ctx, move || api.post("api/notifications/mark-read/", json!({ "mark_all": true }))));
                    }
                }
            });
        });
        ui.add_space(16.0);
        if !env.signed_in() {
            widgets::empty_state(ui, &th, Icon::BellOff, "Sign in to see notifications", "Replies, likes and follows from the community show up here.");
            ui.vertical_centered(|ui| {
                if widgets::button(ui, &th, "Sign in", BtnKind::Primary, Some(Icon::Login), None).clicked() {
                    env.act(crate::actions::Action::Replace(Route::Login));
                }
            });
            return;
        }
        if let Some(e) = st.error.clone() {
            crate::screens::login::error_banner(ui, &th, &e, w);
            return;
        }
        if st.load.is_some() && st.items.is_empty() {
            ui.vertical_centered(|ui| {
                ui.add_space(40.0);
                ui.add(egui::Spinner::new().size(28.0).color(th.p.accent));
            });
            return;
        }
        if st.items.is_empty() {
            widgets::empty_state(ui, &th, Icon::Bell, "No notifications yet", "When someone replies to you or likes your post, you'll see it here.");
            return;
        }
        let mut open: Option<Route> = None;
        let text_w = (w - 150.0).max(160.0);
        for it in st.items.clone() {
            let who = if it.actor.is_empty() { "Someone".to_string() } else { it.actor.clone() };
            let (title, detail) = describe(&it, &who);
            let font = if it.read { fonts::regular(14.5) } else { fonts::medium(14.5) };
            let galley = ui.painter().layout(title, font, th.p.ink, text_w);
            let detail_g = (!detail.is_empty()).then(|| ui.painter().layout(detail, fonts::regular(13.0), th.p.ink_muted, text_w));
            let body_h = galley.size().y + detail_g.as_ref().map(|g| g.size().y + 4.0).unwrap_or(0.0) + 6.0 + 16.0;
            let h = (body_h + 28.0).max(78.0);
            let (rect, resp) = ui.allocate_exact_size(vec2(w, h), Sense::click());
            let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
            let fill = if it.read { th.p.card } else { crate::theme::mix(th.p.card, th.p.accent_soft, 0.55) };
            ui.painter().rect(rect, Rounding::same(18.0), fill, Stroke::new(1.0_f32, th.p.hairline));
            ui.painter().rect_filled(rect, Rounding::same(18.0), th.p.ink.gamma_multiply(0.05 * hover));
            let av = egui::Rect::from_min_size(egui::pos2(rect.min.x + 16.0, rect.center().y - 22.0), vec2(44.0, 44.0));
            if it.photo.is_empty() || it.actor.is_empty() {
                ui.painter().rect_filled(av, Rounding::same(22.0), if it.read { th.p.field } else { th.p.accent_soft });
                icons::paint(ui.painter(), egui::Rect::from_center_size(av.center(), vec2(22.0, 22.0)), icon_for(&it.verb), if it.read { th.p.ink_muted } else { th.p.on_accent_soft });
            } else {
                let mut child = ui.new_child(egui::UiBuilder::new().max_rect(av));
                crate::ui::remote_image::avatar(&mut child, &th, &it.actor, 0, 44.0, &it.photo);
                let badge = egui::Rect::from_center_size(av.right_bottom() - vec2(4.0, 4.0), vec2(20.0, 20.0));
                ui.painter().circle_filled(badge.center(), 10.0, th.p.card);
                ui.painter().circle_filled(badge.center(), 9.0, th.p.accent_soft);
                icons::paint(ui.painter(), egui::Rect::from_center_size(badge.center(), vec2(12.0, 12.0)), icon_for(&it.verb), th.p.on_accent_soft);
            }
            let x = rect.min.x + 76.0;
            let top = rect.center().y - body_h / 2.0;
            let mut y = top;
            let gh = galley.size().y;
            ui.painter().galley(egui::pos2(x, y), galley, th.p.ink);
            y += gh + 4.0;
            if let Some(g) = detail_g {
                let dh = g.size().y;
                ui.painter().galley(egui::pos2(x, y), g, th.p.ink_muted);
                y += dh + 4.0;
            }
            ui.painter().text(egui::pos2(x, y + 8.0), egui::Align2::LEFT_CENTER, time_ago(it.created), fonts::regular(12.0), th.p.ink_faint);
            if !it.read {
                ui.painter().circle_filled(rect.right_center() - vec2(22.0, 0.0), 5.0, th.p.accent);
            }
            if resp.hovered() {
                ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
            }
            if resp.clicked() {
                if it.target_type.to_lowercase().contains("post") && !it.target_id.is_empty() {
                    open = Some(Route::Post(it.target_id.clone()));
                } else if it.verb.contains("follow") && !it.actor.is_empty() {
                    open = Some(Route::User(it.actor.clone()));
                }
            }
            ui.add_space(10.0);
        }
        if let Some(r) = open {
            env.go(r);
        }
        ui.add_space(24.0);
    });
    let _ = Layout::top_down(Align::Min);
}

impl NotificationsState {
    /// Sample items for the screenshot tour only (see `Env::demo`).
    pub fn demo(&mut self) {
        let now = crate::util::now_secs() as i64 * 1000;
        let mk = |id: &str, msg: &str, verb: &str, read: bool, ago: i64| Item { id: id.into(), message: msg.into(), verb: verb.into(), target_type: "post".into(), target_id: "d1".into(), read, created: now - ago * 60_000, actor: String::new(), photo: String::new() };
        self.items = vec![
            mk("n1", "Anish Karki replied to your post: \"How do you approach projectile-motion MCQs in IOE?\"", "reply", false, 6),
            mk("n2", "Sita Rai and 3 others liked your post", "like", false, 55),
            mk("n3", "Prabin Shrestha started following you", "follow", false, 240),
            mk("n4", "Your uploaded resource \"Physics model set 4\" was approved", "approved", true, 2900),
            mk("n5", "Welcome to NEBians! Complete your profile to get better suggestions.", "welcome", true, 9000),
        ];
        self.loaded = true;
    }
}
