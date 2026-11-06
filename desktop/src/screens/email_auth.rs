//! Email sign-in / create account / verify / forgot password — talks to the real
//! NEBians API (`data::auth`), exactly the endpoints the Android app uses.
use egui::{Align, Layout, RichText, Ui};

use crate::actions::Action;
use crate::data::auth;
use crate::data::store::Session;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Clone, Copy, PartialEq, Eq, Default)]
pub enum Mode {
    #[default]
    SignIn,
    SignUp,
    Verify,
    Forgot,
    Reset,
}

enum Reply {
    Session(Session),
    Message(String),
    SignedUp(String),
}

#[derive(Default)]
pub struct EmailState {
    mode: Mode,
    email: String,
    password: String,
    username: String,
    code: String,
    new_password: String,
    busy: Option<Task<Result<Reply>>>,
    error: Option<String>,
    info: Option<String>,
}

fn finish(env: &mut Env, s: Session) {
    super::auth_flow::complete_sign_in(env, s, false);
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut EmailState) {
    let th = env.theme.clone();
    if let Some(t) = st.busy.as_mut() {
        if let Some(res) = t.poll() {
            st.busy = None;
            match res {
                Ok(Reply::Session(s)) => finish(env, s),
                Ok(Reply::Message(m)) => {
                    if st.mode == Mode::Forgot {
                        st.mode = Mode::Reset;
                    }
                    st.info = Some(m);
                    st.error = None;
                }
                Ok(Reply::SignedUp(m)) => {
                    st.mode = Mode::Verify;
                    st.info = Some(m);
                    st.error = None;
                }
                Err(e) => {
                    st.error = Some(e.to_string());
                    st.info = None;
                }
            }
        }
    }
    let busy = st.busy.is_some();
    super::login::split_layout(ui, env, |ui, env, with_logo| {
    egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| {
        let avail = ui.available_size();
        let w = (avail.x - 48.0).clamp(280.0, 420.0);
        ui.allocate_ui_with_layout(avail, Layout::top_down(Align::Center), |ui| {
            ui.set_width(w);
            ui.add_space(24.0);
            ui.horizontal(|ui| {
                if widgets::icon_button(ui, &th, Icon::Back, "Back", false).clicked() {
                    env.act(Action::Replace(Route::Login));
                }
            });
            let est = match st.mode { Mode::SignUp => 640.0, Mode::Reset => 600.0, _ => 520.0 };
            ui.add_space(((avail.y - est) / 2.0 - 40.0).max(8.0));
            if with_logo {
                env.logo.show(ui, 52.0);
                ui.add_space(18.0);
            }
            if matches!(st.mode, Mode::SignIn | Mode::SignUp) {
                let mut sel = usize::from(st.mode == Mode::SignUp);
                ui.scope(|ui| {
                    ui.set_width(w);
                    if widgets::segmented(ui, &th, &["Sign in", "Create account"], &mut sel) {
                        st.mode = if sel == 1 { Mode::SignUp } else { Mode::SignIn };
                        st.error = None;
                        st.info = None;
                    }
                });
                ui.add_space(24.0);
            }
            let (title, sub) = match st.mode {
                Mode::SignIn => ("Sign in", "Use the email you registered with."),
                Mode::SignUp => ("Create your account", "A verification code will be emailed to you."),
                Mode::Verify => ("Check your email", "Enter the 6-digit code we sent you."),
                Mode::Forgot => ("Reset your password", "We will email a reset code to your address."),
                Mode::Reset => ("Choose a new password", "Enter the code we emailed you and a new password."),
            };
            ui.add(egui::Label::new(RichText::new(title).font(fonts::bold(28.0)).color(th.p.ink)).selectable(false));
            ui.add_space(4.0);
            ui.add(egui::Label::new(RichText::new(sub).font(fonts::regular(15.0)).color(th.p.ink_muted)).selectable(false));
            ui.add_space(22.0);

            ui.add_enabled_ui(!busy, |ui| {
                if !matches!(st.mode, Mode::Verify) {
                    widgets::field(ui, &th, &mut st.email, "Email address", Some(Icon::Mail), w, false, false);
                    ui.add_space(10.0);
                }
                if st.mode == Mode::SignUp {
                    widgets::field(ui, &th, &mut st.username, "Username", Some(Icon::User), w, false, false);
                    ui.add_space(10.0);
                }
                if matches!(st.mode, Mode::SignIn | Mode::SignUp) {
                    let r = widgets::field(ui, &th, &mut st.password, "Password", Some(Icon::Lock), w, true, false);
                    if st.mode == Mode::SignUp {
                        let n = st.password.chars().count();
                        let (msg, col) = if n == 0 { ("Use 8 or more characters.", th.p.ink_faint) } else if n < 8 { ("A little longer — 8 characters minimum.", th.p.warn) } else { ("Looks good.", th.p.ok) };
                        ui.add_space(4.0);
                        widgets::label(ui, RichText::new(msg).font(fonts::regular(12.5)).color(col));
                    }
                    if r.lost_focus() && ui.input(|i| i.key_pressed(egui::Key::Enter)) && st.mode == Mode::SignIn {
                        submit(env, st);
                    }
                    ui.add_space(10.0);
                }
                if matches!(st.mode, Mode::Verify | Mode::Reset) {
                    widgets::field(ui, &th, &mut st.code, "Verification code", Some(Icon::Key), w, false, false);
                    ui.add_space(10.0);
                }
                if st.mode == Mode::Reset {
                    let r = widgets::field(ui, &th, &mut st.new_password, "New password", Some(Icon::Lock), w, true, false);
                    if r.lost_focus() && ui.input(|i| i.key_pressed(egui::Key::Enter)) {
                        submit(env, st);
                    }
                    ui.add_space(10.0);
                }
            });
            if let Some(e) = &st.error {
                super::login::error_banner(ui, &th, e, w);
                ui.add_space(10.0);
            }
            if let Some(i) = &st.info {
                ui.add(egui::Label::new(RichText::new(i).font(fonts::regular(14.0)).color(th.p.ink_muted)));
                ui.add_space(10.0);
            }
            let label = match st.mode {
                Mode::SignIn => "Sign in",
                Mode::SignUp => "Create account",
                Mode::Verify => "Verify",
                Mode::Forgot => "Send reset code",
                Mode::Reset => "Set new password",
            };
            ui.add_space(4.0);
            ui.add_enabled_ui(!busy, |ui| {
                if widgets::button_sized(ui, &th, if busy { "Please wait…" } else { label }, BtnKind::Primary, None, Some(w), 56.0).clicked() {
                    submit(env, st);
                }
            });
            if busy {
                ui.add_space(8.0);
                ui.spinner();
            }
            ui.add_space(14.0);
            crate::ui::widgets::flow(ui, |ui| {
                let go = |ui: &mut Ui, text: &str, mode: Mode, st: &mut EmailState| {
                    if ui.link(RichText::new(text).font(fonts::medium(13.5)).color(th.p.accent)).clicked() {
                        st.mode = mode;
                        st.error = None;
                        st.info = None;
                    }
                };
                match st.mode {
                    Mode::SignIn => go(ui, "Forgot your password?", Mode::Forgot, st),
                    Mode::SignUp => {}
                    Mode::Forgot | Mode::Reset => go(ui, "Back to sign in", Mode::SignIn, st),
                    Mode::Verify => {
                        if ui.link(RichText::new("Resend code").font(fonts::medium(13.5)).color(th.p.accent)).clicked() && !st.email.is_empty() {
                            let email = st.email.clone();
                            st.busy = Some(Task::spawn(&env.ctx, move || auth::resend(&email).map(Reply::Message)));
                        }
                        go(ui, "Back to sign in", Mode::SignIn, st);
                    }
                }
            });
        });
    });
    });
}

fn submit(env: &mut Env, st: &mut EmailState) {
    st.error = None;
    st.info = None;
    let email = st.email.trim().to_string();
    let pw = st.password.clone();
    let ctx = env.ctx.clone();
    match st.mode {
        Mode::SignIn => {
            if email.is_empty() || pw.is_empty() {
                st.error = Some("Enter your email and password.".into());
                return;
            }
            st.busy = Some(Task::spawn(&ctx, move || auth::login(&email, &pw).map(Reply::Session)));
        }
        Mode::SignUp => {
            let user = st.username.trim().to_string();
            if !email.contains('@') || pw.len() < 8 || user.len() < 3 {
                st.error = Some("Use a valid email, a username of 3+ characters and a password of 8+ characters.".into());
                return;
            }
            let role = if env.store.s.profile.role.is_empty() { "student".to_string() } else { env.store.s.profile.role.clone() };
            st.busy = Some(Task::spawn(&ctx, move || auth::signup(&email, &pw, &user, &role).map(Reply::SignedUp)));
        }
        Mode::Verify => {
            let code = st.code.trim().to_string();
            if code.is_empty() {
                st.error = Some("Enter the verification code.".into());
                return;
            }
            st.busy = Some(Task::spawn(&ctx, move || auth::verify(&email, &code).map(Reply::Session)));
        }
        Mode::Reset => {
            let code = st.code.trim().to_string();
            let np = st.new_password.clone();
            if email.is_empty() || code.is_empty() || np.len() < 8 {
                st.error = Some("Enter your email, the emailed code and a new password of 8+ characters.".into());
                return;
            }
            st.busy = Some(Task::spawn(&ctx, move || auth::reset_password(&email, &code, &np).map(Reply::Session)));
        }
        Mode::Forgot => {
            if !email.contains('@') {
                st.error = Some("Enter the email address of your account.".into());
                return;
            }
            st.busy = Some(Task::spawn(&ctx, move || auth::forgot(&email).map(Reply::Message)));
        }
    }
}
