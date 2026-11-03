//! Security — email address (change with a code sent to the new address), password (set or
//! change) and signing out this device. Every request goes to the NEBians API.
use egui::{Align, Layout, RichText, Ui};

use super::{poll, Job, Out};
use crate::actions::Action;
use crate::data::account::{self, Security};
use crate::data::tasks::Task;
use crate::env::Env;
use crate::theme::{fonts, Theme};
use crate::ui::dialog;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct SecurityState {
    want: bool,
    info: Option<Security>,
    load: Option<Job>,
    load_err: Option<String>,
    dlg: Dlg,
}

#[derive(Default)]
enum Dlg {
    #[default]
    None,
    Email(EmailDlg),
    Password(PwDlg),
}

#[derive(Default)]
struct EmailDlg {
    code_step: bool,
    new: String,
    password: String,
    code: String,
    job: Option<Job>,
    error: Option<String>,
}

#[derive(Default)]
struct PwDlg {
    set_mode: bool,
    current: String,
    new: String,
    confirm: String,
    job: Option<Job>,
    error: Option<String>,
}

impl SecurityState {
    pub fn refresh(&mut self) {
        self.want = true;
    }
    pub fn demo_password(&mut self) {
        self.dlg = Dlg::Password(PwDlg { new: "studyhard".into(), ..Default::default() });
    }
}

/// Icon tile + title/subtitle on the left, actions on the right.
pub(super) fn row(ui: &mut Ui, th: &Theme, icon: Icon, title: &str, sub: &str, right: impl FnOnce(&mut Ui)) {
    ui.horizontal(|ui| {
        widgets::icon_tile(ui, th, icon, 46.0);
        ui.add_space(6.0);
        ui.vertical(|ui| {
            ui.spacing_mut().item_spacing.y = 2.0;
            widgets::label(ui, RichText::new(title).font(fonts::medium(15.5)).color(th.p.ink));
            if !sub.is_empty() {
                widgets::label(ui, RichText::new(sub).font(fonts::regular(13.0)).color(th.p.ink_muted));
            }
        });
        ui.with_layout(Layout::right_to_left(Align::Center), right);
    });
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut SecurityState) {
    let th = env.theme.clone();
    if st.want && st.load.is_none() {
        st.want = false;
        if env.demo {
            st.info = Some(Security { email: "aarav@example.com".into(), email_verified: true, has_password: true, pending_email: String::new() });
        } else {
            let api = env.api();
            st.load = Some(Task::spawn(&env.ctx, move || account::security(&api).map(Out::Sec)));
        }
    }
    if let Some(r) = poll(env, &mut st.load) {
        match r {
            Ok(Out::Sec(s)) => {
                st.info = Some(s);
                st.load_err = None;
            }
            Ok(_) => {}
            Err(e) => st.load_err = Some(e),
        }
    }
    let loading = st.load.is_some();
    let info = st.info.clone().unwrap_or_default();
    let session_email = env.store.s.session.as_ref().map(|s| s.email.clone()).unwrap_or_default();
    let email = if info.email.is_empty() { session_email } else { info.email.clone() };

    widgets::panel_frame(&th).show(ui, |ui| {
        ui.set_width(ui.available_width());
        row(ui, &th, Icon::Mail, if email.is_empty() { "Email address" } else { &email }, "", |ui| {
            if widgets::button(ui, &th, "Change", BtnKind::Tonal, Some(Icon::Edit), None).clicked() {
                st.dlg = Dlg::Email(EmailDlg::default());
            }
            if st.info.is_some() {
                let (t, fg, bg) = if info.email_verified { ("Verified", th.p.ok, th.p.ok_soft) } else { ("Unverified", th.p.warn, th.p.warn_soft) };
                widgets::badge(ui, t, fg, bg);
            }
        });
        if !info.pending_email.is_empty() {
            ui.add_space(14.0);
            egui::Frame::none().fill(th.p.secondary_container).rounding(18.0).inner_margin(egui::Margin::symmetric(16.0, 12.0)).show(ui, |ui| {
                ui.set_width(ui.available_width());
                ui.horizontal(|ui| {
                    ui.add(egui::Label::new(RichText::new(format!("Waiting for the code sent to {}", info.pending_email)).font(fonts::medium(14.0)).color(th.p.on_secondary_container)).wrap());
                    ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                        if widgets::button_sized(ui, &th, "Enter code", BtnKind::Primary, None, None, 40.0).clicked() {
                            st.dlg = Dlg::Email(EmailDlg { code_step: true, ..Default::default() });
                        }
                        if widgets::button_sized(ui, &th, "Cancel", BtnKind::Ghost, None, None, 40.0).clicked() {
                            let api = env.api();
                            st.load = Some(Task::spawn(&env.ctx, move || {
                                account::cancel_email_change(&api)?;
                                account::security(&api).map(Out::Sec)
                            }));
                        }
                    });
                });
            });
        }
    });
    ui.add_space(14.0);
    widgets::panel_frame(&th).show(ui, |ui| {
        ui.set_width(ui.available_width());
        let has = info.has_password || st.info.is_none();
        row(ui, &th, Icon::Key, "Password", "", |ui| {
            let label = if has { "Change password" } else { "Set password" };
            if widgets::button(ui, &th, label, BtnKind::Tonal, Some(Icon::Key), None).clicked() {
                st.dlg = Dlg::Password(PwDlg { set_mode: !has, ..Default::default() });
            }
        });
    });
    ui.add_space(14.0);
    widgets::panel_frame(&th).show(ui, |ui| {
        ui.set_width(ui.available_width());
        row(ui, &th, Icon::Logout, "This device", "", |ui| {
            if widgets::button(ui, &th, "Sign out", BtnKind::Secondary, Some(Icon::Logout), None).clicked() {
                env.act(Action::SignOut);
            }
        });
    });
    if loading {
        ui.add_space(12.0);
        widgets::muted(ui, &th, "Checking your account…");
    } else if let Some(e) = &st.load_err {
        ui.add_space(12.0);
        dialog::error_line(ui, &th, e);
    }

    dialogs(ui.ctx(), env, st);
}

fn dialogs(ctx: &egui::Context, env: &mut Env, st: &mut SecurityState) {
    let th = env.theme.clone();
    let api = env.api();
    let task_ctx = env.ctx.clone();
    let sess = env.store.s.session.clone();
    let demo = env.demo;
    let mut close = false;
    let mut refresh = false;
    let mut new_session = None;
    let mut sign_out = false;
    let mut toast: Option<String> = None;

    match &mut st.dlg {
        Dlg::None => {}
        Dlg::Email(d) => {
            if let Some(r) = poll(env, &mut d.job) {
                match r {
                    Ok(Out::Msg(m)) => {
                        d.code_step = true;
                        d.error = None;
                        toast = Some(m);
                        refresh = true;
                    }
                    Ok(Out::Session(s)) => {
                        new_session = Some(s);
                        toast = Some("Email address updated".into());
                        close = true;
                        refresh = true;
                    }
                    Ok(_) => {}
                    Err(e) => d.error = Some(e),
                }
            }
            let busy = d.job.is_some();
            let dismissed = dialog::show(ctx, &th, "email", 460.0, |ui| {
                dialog::title(ui, &th, if d.code_step { "Enter the code" } else { "Change email" });
                let w = ui.available_width();
                if d.code_step {
                    widgets::field(ui, &th, &mut d.code, "6-digit code", Some(Icon::Key), w, false, false);
                } else {
                    widgets::field(ui, &th, &mut d.new, "New email address", Some(Icon::Mail), w, false, false);
                    widgets::field(ui, &th, &mut d.password, "Current password", Some(Icon::Lock), w, true, false);
                }
                if let Some(e) = &d.error {
                    dialog::error_line(ui, &th, e);
                }
                let ready = !busy && if d.code_step { d.code.trim().len() >= 4 } else { d.new.contains('@') };
                match dialog::confirm_row(ui, &th, if busy { "Working…" } else if d.code_step { "Confirm" } else { "Send code" }, BtnKind::Primary, ready) {
                    Some(true) => {
                        d.error = None;
                        let (api, sess) = (api.clone(), sess.clone());
                        if demo {
                            close = true;
                        } else if d.code_step {
                            let code = d.code.trim().to_string();
                            d.job = Some(Task::spawn(&task_ctx, move || {
                                let old = sess.unwrap_or_else(|| crate::data::store::Session { email: String::new(), username: String::new(), token: String::new(), user_id: String::new(), display_name: String::new(), photo_url: String::new(), provider: "email".into() });
                                account::confirm_email_change(&api, &code, &old).map(Out::Session)
                            }));
                        } else {
                            let (new, pw) = (d.new.trim().to_string(), d.password.clone());
                            d.job = Some(Task::spawn(&task_ctx, move || account::request_email_change(&api, &new, &pw).map(Out::Msg)));
                        }
                    }
                    Some(false) => close = true,
                    None => {}
                }
            });
            close |= dismissed;
        }
        Dlg::Password(d) => {
            if let Some(r) = poll(env, &mut d.job) {
                match r {
                    Ok(Out::Msg(m)) => {
                        toast = Some(m);
                        close = true;
                        // changing a password revokes every token — sign in again with the new one
                        sign_out = !d.set_mode;
                        refresh = true;
                    }
                    Ok(_) => {}
                    Err(e) => d.error = Some(e),
                }
            }
            let busy = d.job.is_some();
            let mismatch = !d.confirm.is_empty() && d.confirm != d.new;
            let dismissed = dialog::show(ctx, &th, "password", 460.0, |ui| {
                dialog::title(ui, &th, if d.set_mode { "Set a password" } else { "Change password" });
                let w = ui.available_width();
                if !d.set_mode {
                    widgets::field(ui, &th, &mut d.current, "Current password", Some(Icon::Lock), w, true, false);
                }
                widgets::field(ui, &th, &mut d.new, "New password", Some(Icon::Key), w, true, false);
                widgets::field(ui, &th, &mut d.confirm, "Repeat new password", Some(Icon::Key), w, true, mismatch);
                if mismatch {
                    dialog::error_line(ui, &th, "The passwords do not match.");
                } else if let Some(e) = &d.error {
                    dialog::error_line(ui, &th, e);
                }
                let ready = !busy && d.new.len() >= 8 && d.new == d.confirm && (d.set_mode || !d.current.is_empty());
                match dialog::confirm_row(ui, &th, if busy { "Working…" } else { "Save" }, BtnKind::Primary, ready) {
                    Some(true) => {
                        d.error = None;
                        let api = api.clone();
                        let (cur, new, set) = (d.current.clone(), d.new.clone(), d.set_mode);
                        if demo {
                            close = true;
                        } else {
                            d.job = Some(Task::spawn(&task_ctx, move || {
                                if set {
                                    account::set_password(&api, &new)
                                } else {
                                    crate::data::auth::change_password(api_token(&api), &cur, &new)
                                }
                                .map(Out::Msg)
                            }));
                        }
                    }
                    Some(false) => close = true,
                    None => {}
                }
            });
            close |= dismissed;
        }
    }

    if close {
        st.dlg = Dlg::None;
    }
    if refresh {
        st.want = true;
    }
    if let Some(s) = new_session {
        env.store.s.session = Some(s);
        env.store.touch();
    }
    if let Some(m) = toast {
        env.toast(m);
    }
    if sign_out {
        env.act(Action::SignOut);
    }
}

fn api_token(api: &crate::data::api::Api) -> &str {
    api.token().unwrap_or_default()
}
