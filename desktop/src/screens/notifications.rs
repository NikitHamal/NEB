//! Notifications — `api/notifications/` with unread styling, mark-all-read, and deep links
//! into the community thread a notification refers to.
use egui::{vec2, Align, Layout, RichText, Rounding, Sense, Stroke, Ui};
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
        for it in st.items.clone() {
            let (rect, resp) = ui.allocate_exact_size(vec2(w, 74.0), Sense::click());
            let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
            let fill = if it.read { th.p.card } else { crate::theme::mix(th.p.card, th.p.accent_soft, 0.55) };
            ui.painter().rect(rect, Rounding::same(20.0), fill, Stroke::new(1.0, th.p.hairline));
            ui.painter().rect_filled(rect, Rounding::same(20.0), th.p.ink.gamma_multiply(0.05 * hover));
            let tile = egui::Rect::from_min_size(rect.min + vec2(14.0, 15.0), vec2(44.0, 44.0));
            ui.painter().rect_filled(tile, Rounding::same(15.0), if it.read { th.p.field } else { th.p.accent_soft });
            icons::paint(ui.painter(), egui::Rect::from_center_size(tile.center(), vec2(22.0, 22.0)), icon_for(&it.verb), if it.read { th.p.ink_muted } else { th.p.on_accent_soft });
            let galley = ui.painter().layout(it.message.clone(), if it.read { fonts::regular(14.5) } else { fonts::medium(14.5) }, th.p.ink, rect.width() - 100.0);
            ui.painter().galley(rect.min + vec2(72.0, 14.0), galley, th.p.ink);
            ui.painter().text(rect.min + vec2(72.0, 54.0), egui::Align2::LEFT_CENTER, time_ago(it.created), fonts::regular(12.0), th.p.ink_faint);
            if !it.read {
                ui.painter().circle_filled(rect.right_center() - vec2(20.0, 0.0), 5.0, th.p.accent);
            }
            if resp.hovered() {
                ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
            }
            if resp.clicked() && it.target_type.to_lowercase().contains("post") && !it.target_id.is_empty() {
                open = Some(Route::Post(it.target_id.clone()));
            }
            ui.add_space(8.0);
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
        let mk = |id: &str, msg: &str, verb: &str, read: bool, ago: i64| Item { id: id.into(), message: msg.into(), verb: verb.into(), target_type: "post".into(), target_id: "d1".into(), read, created: now - ago * 60_000 };
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
