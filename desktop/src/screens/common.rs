//! Helpers shared by several screens: the scrolling page wrapper, subject and
//! chapter cards, the "content missing" banner.
use egui::{vec2, Align, Layout, RichText, Ui};

use crate::actions::Action;
use crate::data::models::{ChapterKind, ChapterRef, SubjectSummary};
use crate::env::Env;
use crate::router::Route;
use crate::theme::{fonts, spacing};
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};
use crate::ui::LayoutMode;

/// Vertical scroll area with a centred, max-width column and responsive padding.
pub fn scroll_page(ui: &mut Ui, env: &mut Env, id: &str, add: impl FnOnce(&mut Ui, &mut Env)) {
    let pad = if env.layout == LayoutMode::Compact { spacing::PAGE_PAD_COMPACT } else { spacing::PAGE_PAD };
    egui::ScrollArea::vertical().id_salt(id).auto_shrink([false, false]).show(ui, |ui| {
        let avail = ui.available_width();
        let w = (avail - 2.0 * pad).clamp(240.0, spacing::MAX_CONTENT_W);
        let side = ((avail - w) / 2.0).max(0.0);
        ui.horizontal_top(|ui| {
            ui.spacing_mut().item_spacing.x = 0.0;
            ui.add_space(side);
            ui.vertical(|ui| {
                ui.set_width(w);
                ui.add_space(pad * 0.8);
                add(ui, env);
                ui.add_space(48.0);
            });
        });
    });
}

/// Full subject card used on Home, Library, Category. Returns true when clicked.
pub fn subject_card(ui: &mut Ui, env: &Env, track: &str, s: &SubjectSummary, w: f32) -> bool {
    let th = &env.theme;
    let name = env.subject_name(s);
    let track_short = env.track(track).map(|t| t.short.clone()).unwrap_or_default();
    let done = env.store.done_count_in(track, &s.subject);
    let resp = widgets::card(ui, th, vec2(w, 96.0), 14.0, |ui| {
        ui.horizontal(|ui| {
            widgets::subject_badge(ui, th, &s.name, &s.color, 44.0);
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 2.0;
                widgets::label_trunc(ui, RichText::new(&name).font(fonts::bold(15.0)).color(th.p.ink));
                widgets::label_trunc(ui, RichText::new(format!("{track_short} · {} chapters", s.notes_ready)).font(fonts::regular(12.5)).color(th.p.ink_muted));
                ui.add_space(4.0);
                if s.unit_count > 0 {
                    widgets::progress_bar(ui, th, done as f32 / s.unit_count as f32, 4.0, Some(th.subject_color(&s.color)));
                }
            });
        });
    });
    resp.clicked()
}

/// Open a subject (called from cards).
pub fn open_subject(env: &mut Env, track: &str, subject: &str) {
    env.go(Route::Subject { track: track.to_string(), subject: subject.to_string() });
}

/// Shown while the catalogue loads, or when it can't be reached and nothing is cached yet.
pub fn content_missing(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    match &env.status {
        crate::env::ContentStatus::Failed(msg) => {
            let msg = msg.clone();
            load_state(ui, &th, Some(msg), || env.act(Action::ReloadContent));
        }
        _ => load_state(ui, &th, None, || {}),
    }
}

/// A loading placeholder, or — with `failed` — an error card with a Retry button.
pub fn load_state(ui: &mut Ui, th: &crate::theme::Theme, failed: Option<String>, retry: impl FnOnce()) {
    widgets::panel_frame(th).show(ui, |ui| {
        ui.set_width(ui.available_width());
        match failed {
            None => {
                ui.add_space(8.0);
                ui.horizontal(|ui| {
                    ui.spinner();
                    ui.add_space(6.0);
                    widgets::label(ui, RichText::new("Loading from NEBians…").font(fonts::medium(15.0)).color(th.p.ink_muted));
                });
                ui.add_space(8.0);
            }
            Some(msg) => {
                widgets::heading(ui, th, "Can't load this right now", 18.0);
                ui.add_space(4.0);
                ui.add(egui::Label::new(RichText::new(msg).color(th.p.ink_muted)));
                ui.add_space(12.0);
                if widgets::button(ui, th, "Try again", BtnKind::Primary, Some(Icon::Refresh), None).clicked() {
                    retry();
                }
            }
        }
    });
}

/// Start/resume a chapter; used by "Continue" buttons.
pub fn open_chapter(env: &mut Env, c: ChapterRef) {
    env.go(Route::Reader(c));
}

pub fn unit_ref(track: &str, subject: &str, no: u32) -> ChapterRef {
    ChapterRef::new(track, subject, ChapterKind::Unit, no)
}

/// Right-aligned container helper.
pub fn right(ui: &mut Ui, f: impl FnOnce(&mut Ui)) {
    ui.with_layout(Layout::right_to_left(Align::Center), f);
}

pub fn push_toast(env: &mut Env, m: &str) {
    env.act(Action::Toast(m.to_string()));
}
