//! Privacy Policy / Terms of Service — the same text as the Android app, readable offline and
//! entirely inside the app: as a page, as a tab of the account centre, and as a sheet over sign-in.
use egui::{RichText, Ui};

use super::common::*;
use super::legal_data::{Doc, PRIVACY, TERMS};
use crate::env::Env;
use crate::theme::{fonts, motion, Theme};
use crate::ui::dialog;
use crate::ui::widgets::{self, BtnKind};

pub fn doc_for(key: &str) -> &'static Doc {
    if key == "terms" {
        &TERMS
    } else {
        &PRIVACY
    }
}

/// The numbered sections of one document. Each card rises in with a short stagger.
pub fn body(ui: &mut Ui, th: &Theme, d: &Doc) {
    widgets::label(ui, RichText::new(d.updated).font(fonts::regular(13.0)).color(th.p.ink_muted));
    ui.add_space(12.0);
    for (i, s) in d.sections.iter().enumerate() {
        let e = motion::enter(ui.ctx(), ui.id().with((d.key, i)), 0.04 * i as f32, 0.4);
        ui.scope(|ui| {
            ui.set_opacity(e);
            widgets::panel_frame(th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                ui.horizontal(|ui| {
                    widgets::badge(ui, s.n, th.p.on_accent_soft, th.p.accent_soft);
                    widgets::heading(ui, th, s.title, 16.5);
                });
                ui.add_space(8.0);
                for p in s.paras {
                    ui.add(egui::Label::new(RichText::new(p.replace("**", "")).font(fonts::regular(14.5)).color(th.p.ink)).selectable(true));
                    ui.add_space(6.0);
                }
            });
        });
        ui.add_space(12.0);
    }
}

/// Standalone page (Settings → Privacy / Terms, Help links).
pub fn show(ui: &mut Ui, env: &mut Env, key: &str) {
    let d = doc_for(key);
    scroll_page(ui, env, &format!("legal-{key}"), |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, d.title);
        let mut idx = usize::from(key == "terms");
        if widgets::segmented(ui, &th, &["Privacy Policy", "Terms of Service"], &mut idx) {
            env.go(crate::router::Route::Legal(if idx == 1 { "terms" } else { "privacy" }.into()));
        }
        ui.add_space(16.0);
        body(ui, &th, d);
    });
}

/// Modal sheet for places without the app shell (sign-in). Returns true when closed.
pub fn sheet(ctx: &egui::Context, env: &Env, key: &mut String) -> bool {
    let th = env.theme.clone();
    let height = (ctx.screen_rect().height() * 0.68).max(240.0);
    let mut close = false;
    let dismissed = dialog::show(ctx, &th, "legal-sheet", 720.0, |ui| {
        let mut idx = usize::from(key == "terms");
        dialog::title(ui, &th, doc_for(key).title);
        if widgets::segmented(ui, &th, &["Privacy Policy", "Terms of Service"], &mut idx) {
            *key = if idx == 1 { "terms" } else { "privacy" }.into();
        }
        egui::ScrollArea::vertical().id_salt(("legal-sheet", key.as_str())).max_height(height).auto_shrink([false, true]).show(ui, |ui| {
            body(ui, &th, doc_for(key));
        });
        dialog::actions(ui, |ui| {
            if widgets::button(ui, &th, "Close", BtnKind::Primary, None, None).clicked() {
                close = true;
            }
        });
    });
    close || dismissed
}
