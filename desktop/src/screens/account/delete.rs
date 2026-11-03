//! Delete account — files a deletion request (30-day window, like the website), shows its
//! schedule and lets the user cancel it, all inside the app.
use egui::{RichText, Ui};

use super::security::row;
use super::{poll, Job, Out};
use crate::data::account::{self, Deletion};
use crate::data::tasks::Task;
use crate::env::Env;
use crate::theme::fonts;
use crate::ui::dialog;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

const WHAT_HAPPENS: [&str; 3] = [
    "Your profile, posts, replies, bookmarks and activity are erased after 30 days.",
    "Study resources you uploaded stay in the library, credited to Anonymous.",
    "Cancel any time during the 30 days and nothing is lost.",
];

#[derive(Default)]
pub struct DeleteState {
    want: bool,
    status: Option<Deletion>,
    job: Option<Job>,
    error: Option<String>,
    reason: String,
    confirm: Option<String>,
}

impl DeleteState {
    pub fn refresh(&mut self) {
        self.want = true;
    }
    pub fn demo_confirm(&mut self) {
        self.confirm = Some("DEL".into());
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut DeleteState) {
    let th = env.theme.clone();
    if st.want && st.job.is_none() {
        st.want = false;
        if env.demo {
            st.status = Some(Deletion::default());
        } else {
            let api = env.api();
            st.job = Some(Task::spawn(&env.ctx, move || account::deletion_status(&api).map(Out::Del)));
        }
    }
    if let Some(r) = poll(env, &mut st.job) {
        match r {
            Ok(Out::Del(d)) => {
                st.status = Some(d);
                st.error = None;
            }
            Ok(Out::Done) => {
                st.status = Some(Deletion::default());
                env.toast("Deletion cancelled");
            }
            Ok(_) => {}
            Err(e) => st.error = Some(e),
        }
    }
    let busy = st.job.is_some();
    let status = st.status.clone();

    match status {
        None if busy => {
            widgets::muted(ui, &th, "Checking your account…");
        }
        Some(d) if d.pending => {
            widgets::panel_frame(&th).fill(th.p.danger_soft).show(ui, |ui| {
                ui.set_width(ui.available_width());
                let when = crate::util::fmt_date_ms(d.scheduled_ms);
                row(ui, &th, Icon::Warning, "Deletion scheduled", &format!("Your account will be erased on {when}."), |ui| {
                    ui.add_enabled_ui(!busy, |ui| {
                        if widgets::button(ui, &th, "Cancel deletion", BtnKind::Primary, Some(Icon::Refresh), None).clicked() {
                            let api = env.api();
                            st.job = Some(Task::spawn(&env.ctx, move || account::cancel_deletion(&api).map(|_| Out::Done)));
                        }
                    });
                });
            });
        }
        _ => {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                for line in WHAT_HAPPENS {
                    ui.horizontal_top(|ui| {
                        let (r, _) = ui.allocate_exact_size(egui::vec2(8.0, 20.0), egui::Sense::hover());
                        ui.painter().circle_filled(r.center(), 3.0, th.p.accent);
                        ui.add(egui::Label::new(RichText::new(line).font(fonts::regular(14.5)).color(th.p.ink)).wrap());
                    });
                    ui.add_space(4.0);
                }
                ui.add_space(10.0);
                let w = ui.available_width().min(560.0);
                widgets::text_area(ui, &th, &mut st.reason, "Reason (optional)", w, 3);
                ui.add_space(14.0);
                if widgets::button(ui, &th, "Delete my account", BtnKind::Danger, Some(Icon::Trash), None).clicked() {
                    st.confirm = Some(String::new());
                }
            });
        }
    }
    if let Some(e) = &st.error {
        ui.add_space(10.0);
        dialog::error_line(ui, &th, e);
    }

    if let Some(typed) = st.confirm.as_mut() {
        let mut go = false;
        let mut close = false;
        let dismissed = dialog::show(ui.ctx(), &th, "delete-account", 460.0, |ui| {
            dialog::title(ui, &th, "Delete your account?");
            dialog::body(ui, &th, "Type DELETE to confirm. You can still cancel during the 30-day window.");
            let w = ui.available_width();
            widgets::field(ui, &th, typed, "Type DELETE", Some(Icon::Warning), w, false, false);
            match dialog::confirm_row(ui, &th, "Delete account", BtnKind::Danger, typed.trim() == "DELETE") {
                Some(true) => go = true,
                Some(false) => close = true,
                None => {}
            }
        });
        if go {
            if env.demo {
                st.status = Some(Deletion { pending: true, scheduled_ms: crate::util::now_secs() as i64 * 1000 + 30 * 86_400_000 });
            } else {
                let (api, reason) = (env.api(), st.reason.trim().to_string());
                st.job = Some(Task::spawn(&env.ctx, move || account::request_deletion(&api, &reason).map(Out::Del)));
            }
            env.toast("Deletion requested");
        }
        if go || close || dismissed {
            st.confirm = None;
        }
    }
}
