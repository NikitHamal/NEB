//! Welcome / sign-in chooser (Android `LoginScreen.kt`): Google, GitHub, email, or guest.
//! Google and GitHub run through the browser hand-off in `data::browser_auth`; this screen
//! drives that little state machine (start → open browser → poll → session).
use std::sync::Arc;
use std::time::{Duration, Instant};

use egui::text::{LayoutJob, TextFormat};
use egui::{vec2, Align, Layout, Rect, RichText, Rounding, Ui, UiBuilder};

use super::auth_flow;
use crate::config::SITE_URL;
use crate::data::browser_auth::{self, Handoff, Poll};
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::{AppError, Result};
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

const GOOGLE_SVG: &[u8] = include_bytes!("../../assets/img/auth/google.svg");
const GITHUB_SVG: &[u8] = include_bytes!("../../assets/img/auth/github.svg");
const GITHUB_DARK_SVG: &[u8] = include_bytes!("../../assets/img/auth/github-dark.svg");

#[derive(Clone, Copy, PartialEq, Eq)]
enum Provider {
    Google,
    GitHub,
}

impl Provider {
    fn name(self) -> &'static str {
        match self {
            Provider::Google => "Google",
            Provider::GitHub => "GitHub",
        }
    }
}

struct Wait {
    provider: Provider,
    start: Option<Task<Result<Handoff>>>,
    handoff: Option<Arc<Handoff>>,
    poll: Option<Task<Result<Poll>>>,
    next_poll: Instant,
    began: Instant,
    failures: u8,
}

#[derive(Default)]
pub struct LoginState {
    wait: Option<Wait>,
    error: Option<String>,
}

fn begin(env: &Env, st: &mut LoginState, provider: Provider) {
    st.error = None;
    st.wait = Some(Wait {
        provider,
        start: Some(Task::spawn(&env.ctx, browser_auth::start)),
        handoff: None,
        poll: None,
        next_poll: Instant::now(),
        began: Instant::now(),
        failures: 0,
    });
}

/// Advance the browser hand-off. Returns a finished sign-in, if any.
fn drive(env: &mut Env, st: &mut LoginState) {
    let Some(w) = st.wait.as_mut() else { return };
    env.ctx.request_repaint_after(Duration::from_millis(400));
    let mut fail: Option<String> = None;
    let mut done: Option<(crate::data::store::Session, bool)> = None;

    if let Some(t) = w.start.as_mut() {
        if let Some(r) = t.poll() {
            w.start = None;
            match r {
                Ok(h) => {
                    env.open_url(&h.login_url);
                    w.next_poll = Instant::now() + Duration::from_secs(h.interval_secs);
                    w.began = Instant::now();
                    w.handoff = Some(Arc::new(h));
                }
                Err(e) => fail = Some(e.to_string()),
            }
        }
    }
    if let Some(t) = w.poll.as_mut() {
        if let Some(r) = t.poll() {
            w.poll = None;
            let secs = w.handoff.as_ref().map(|h| h.interval_secs).unwrap_or(2);
            w.next_poll = Instant::now() + Duration::from_secs(secs);
            match r {
                Ok(Poll::Done { session, is_new }) => done = Some((session, is_new)),
                Ok(Poll::Pending) => w.failures = 0,
                Err(AppError::Gone(m)) => fail = Some(m),
                Err(AppError::Network(m)) => {
                    w.failures += 1;
                    if w.failures >= 6 {
                        fail = Some(m);
                    }
                }
                Err(e) => fail = Some(e.to_string()),
            }
        }
    }
    if let Some(h) = w.handoff.clone() {
        if w.began.elapsed().as_secs() > h.expires_secs {
            fail = Some("The sign-in request expired. Please try again.".into());
        } else if w.poll.is_none() && done.is_none() && fail.is_none() && Instant::now() >= w.next_poll {
            w.poll = Some(Task::spawn(&env.ctx, move || browser_auth::poll(&h)));
        }
    }
    if let Some((session, is_new)) = done {
        st.wait = None;
        auth_flow::complete_sign_in(env, session, is_new);
    } else if let Some(m) = fail {
        st.wait = None;
        st.error = Some(m);
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut LoginState) {
    drive(env, st);
    split_layout(ui, env, |ui, env, with_logo| form(ui, env, st, with_logo));
}

/// The sign-in journey's shared frame: a brand panel on the left (wide windows) and the form on the right.
pub fn split_layout(ui: &mut Ui, env: &mut Env, add: impl FnOnce(&mut Ui, &mut Env, bool)) {
    let th = env.theme.clone();
    let full = ui.available_rect_before_wrap();
    let split = full.width() >= 900.0;
    let left_w = if split { (full.width() * 0.44).min(600.0) } else { 0.0 };
    if split {
        let panel = Rect::from_min_size(full.min, vec2(left_w, full.height())).shrink(14.0);
        ui.painter().rect_filled(panel, Rounding::same(36.0), th.p.accent_soft);
        brand_panel(ui, env, panel.shrink2(vec2(44.0, 44.0)));
    }
    let right = Rect::from_min_max(egui::pos2(full.min.x + left_w, full.min.y), full.max);
    ui.allocate_new_ui(UiBuilder::new().max_rect(right), |ui| add(ui, env, !split));
}

fn brand_panel(ui: &mut Ui, env: &mut Env, rect: Rect) {
    let th = env.theme.clone();
    ui.allocate_new_ui(UiBuilder::new().max_rect(rect).layout(Layout::top_down(Align::Min)), |ui| {
        ui.horizontal(|ui| {
            env.logo.show(ui, 44.0);
            widgets::label(ui, RichText::new("NEBians").font(fonts::bold(26.0)).color(th.p.on_accent_soft));
        });
        ui.add_space((rect.height() * 0.16).max(24.0));
        ui.add(egui::Label::new(RichText::new("Study smarter,\ntogether.").font(fonts::bold(46.0)).color(th.p.on_accent_soft)).selectable(false));
        ui.add_space(14.0);
        ui.add(egui::Label::new(RichText::new("The open learning community for Nepal — notes, syllabus and question banks from Class 8 to Bachelor.").font(fonts::regular(16.5)).color(th.p.on_accent_soft)).selectable(false));
        ui.add_space(34.0);
        for (icon, title, body) in [
            (Icon::Library, "A full library", "Chapters, practice sets and model papers, readable offline."),
            (Icon::Forum, "A community that answers", "Ask questions, share what you know, follow classmates."),
            (Icon::Cloud, "One account everywhere", "Your profile, bookmarks and progress follow you across devices."),
        ] {
            ui.horizontal(|ui| {
                let (r, _) = ui.allocate_exact_size(vec2(48.0, 48.0), egui::Sense::hover());
                ui.painter().rect_filled(r, Rounding::same(16.0), th.p.card.gamma_multiply(0.75));
                crate::ui::icons::paint(ui.painter(), Rect::from_center_size(r.center(), vec2(24.0, 24.0)), icon, th.p.accent);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 1.0;
                    widgets::label(ui, RichText::new(title).font(fonts::bold(15.0)).color(th.p.on_accent_soft));
                    ui.add(egui::Label::new(RichText::new(body).font(fonts::regular(13.5)).color(th.p.on_accent_soft)).selectable(false).wrap());
                });
            });
            ui.add_space(14.0);
        }
    });
}

fn form(ui: &mut Ui, env: &mut Env, st: &mut LoginState, with_logo: bool) {
    let th = env.theme.clone();
    egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| {
        let avail = ui.available_size();
        let w = (avail.x - 48.0).clamp(280.0, 420.0);
        ui.allocate_ui_with_layout(avail, Layout::top_down(Align::Center), |ui| {
            ui.set_width(w);
            let est = if st.wait.is_some() { 470.0 } else { 600.0 };
            ui.add_space(((avail.y - est) / 2.0).max(20.0));
            if st.wait.is_some() {
                waiting(ui, env, st, w);
                return;
            }
            if with_logo {
                env.logo.show(ui, 64.0);
                ui.add_space(22.0);
            }
            let big = if with_logo { 28.0 } else { 32.0 };
            let mut job = LayoutJob::default();
            job.halign = Align::Center;
            job.append("Welcome to ", 0.0, TextFormat { font_id: fonts::bold(big), color: th.p.ink, ..Default::default() });
            job.append("NEBians", 0.0, TextFormat { font_id: fonts::bold(big), color: th.p.accent, ..Default::default() });
            ui.add(egui::Label::new(job).selectable(false));
            ui.add_space(8.0);
            ui.add(egui::Label::new(RichText::new("Sign in to sync your profile, join the community and keep your progress on every device.").font(fonts::regular(15.0)).color(th.p.ink_muted)).selectable(false));
            ui.add_space(28.0);

            if let Some(e) = st.error.clone() {
                error_banner(ui, &th, &e, w);
                ui.add_space(14.0);
            }
            if widgets::provider_button(ui, &th, "Continue with Google", "bytes://google.svg", GOOGLE_SVG, w).clicked() {
                begin(env, st, Provider::Google);
            }
            ui.add_space(10.0);
            let (gh_uri, gh_svg) = if th.dark { ("bytes://github-dark.svg", GITHUB_DARK_SVG) } else { ("bytes://github.svg", GITHUB_SVG) };
            if widgets::provider_button(ui, &th, "Continue with GitHub", gh_uri, gh_svg, w).clicked() {
                begin(env, st, Provider::GitHub);
            }
            ui.add_space(18.0);
            widgets::or_divider(ui, &th, "or", w);
            ui.add_space(18.0);
            if widgets::button_sized(ui, &th, "Continue with email", BtnKind::Primary, Some(Icon::Mail), Some(w), 56.0).clicked() {
                env.go(Route::EmailAuth);
            }
            ui.add_space(8.0);
            if widgets::button_sized(ui, &th, "Continue as guest", BtnKind::Ghost, None, Some(w), 52.0).clicked() {
                auth_flow::continue_as_guest(env);
            }
            ui.add_space(18.0);
            legal(ui, env, w);
        });
    });
}

pub fn error_banner(ui: &mut Ui, th: &crate::theme::Theme, msg: &str, w: f32) {
    egui::Frame::none()
        .fill(th.p.danger_soft)
        .rounding(Rounding::same(16.0))
        .inner_margin(egui::Margin::symmetric(14.0, 10.0))
        .show(ui, |ui| {
            ui.set_width(w - 28.0);
            ui.horizontal_top(|ui| {
                let c = if th.dark { th.p.on_accent_soft } else { th.p.danger };
                ui.add(egui::Label::new(crate::ui::icons::text(Icon::Error, 20.0).color(c)).selectable(false));
                ui.add(egui::Label::new(RichText::new(msg).font(fonts::regular(14.0)).color(c)).wrap());
            });
        });
}

fn waiting(ui: &mut Ui, env: &mut Env, st: &mut LoginState, w: f32) {
    let th = env.theme.clone();
    let (provider, url, left) = {
        let wt = st.wait.as_ref().unwrap();
        let left = wt.handoff.as_ref().map(|h| h.expires_secs.saturating_sub(wt.began.elapsed().as_secs()));
        (wt.provider, wt.handoff.as_ref().map(|h| h.login_url.clone()), left)
    };
    widgets::icon_tile(ui, &th, Icon::Globe, 72.0);
    ui.add_space(20.0);
    widgets::label(ui, RichText::new(format!("Continue with {} in your browser", provider.name())).font(fonts::bold(22.0)).color(th.p.ink));
    ui.add_space(8.0);
    let text = match &url {
        Some(_) => format!("We opened NEBians in your browser. Sign in with {}, then tap Allow. This window continues by itself.", provider.name()),
        None => "Contacting NEBians…".to_string(),
    };
    ui.add(egui::Label::new(RichText::new(text).font(fonts::regular(15.0)).color(th.p.ink_muted)).selectable(false));
    ui.add_space(22.0);
    ui.horizontal(|ui| {
        ui.add(egui::Spinner::new().size(22.0).color(th.p.accent));
        let msg = match left {
            Some(s) => format!("Waiting for approval · {}:{:02} left", s / 60, s % 60),
            None => "Starting…".into(),
        };
        widgets::label(ui, RichText::new(msg).font(fonts::medium(14.0)).color(th.p.ink_muted));
    });
    ui.add_space(22.0);
    if let Some(u) = &url {
        if widgets::button_sized(ui, &th, "Open browser again", BtnKind::Tonal, Some(Icon::External), Some(w), 52.0).clicked() {
            env.open_url(u);
        }
        ui.add_space(6.0);
        ui.add(egui::Label::new(RichText::new(u).font(fonts::regular(11.5)).color(th.p.ink_faint)).wrap());
        ui.add_space(14.0);
    }
    if widgets::button_sized(ui, &th, "Cancel", BtnKind::Ghost, None, Some(w), 52.0).clicked() {
        st.wait = None;
    }
}

fn legal(ui: &mut Ui, env: &mut Env, w: f32) {
    let th = env.theme.clone();
    ui.vertical_centered(|ui| {
        ui.add(egui::Label::new(RichText::new("By continuing you agree to the").font(fonts::regular(12.5)).color(th.p.ink_faint)).selectable(false));
        ui.horizontal(|ui| {
            ui.add_space(((w - 215.0) / 2.0).max(0.0));
            ui.spacing_mut().item_spacing.x = 4.0;
            if ui.link(RichText::new("Terms of Service").font(fonts::medium(12.5)).color(th.p.accent)).clicked() {
                env.open_url(&format!("{SITE_URL}/terms/"));
            }
            ui.add(egui::Label::new(RichText::new("and").font(fonts::regular(12.5)).color(th.p.ink_faint)).selectable(false));
            if ui.link(RichText::new("Privacy Policy").font(fonts::medium(12.5)).color(th.p.accent)).clicked() {
                env.open_url(&format!("{SITE_URL}/privacy/"));
            }
        });
    });
}

impl LoginState {
    /// Show the "waiting for your browser" card without contacting the server (screenshot tour).
    pub fn demo_waiting(&mut self) {
        self.wait = Some(Wait { provider: Provider::Google, start: None, handoff: Some(Arc::new(Handoff::demo())), poll: None, next_poll: Instant::now() + Duration::from_secs(3600), began: Instant::now(), failures: 0 });
    }
    pub fn clear(&mut self) {
        self.wait = None;
    }
}
