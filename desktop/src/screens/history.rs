//! Reading history — every chapter you opened, newest first, with finished markers.
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::env::Env;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

pub fn show(ui: &mut Ui, env: &mut Env) {
    scroll_page(ui, env, "history", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Reading history", Some("Chapters you opened recently. Stored on this computer."));
        let recent = env.store.s.recent.clone();
        if recent.is_empty() {
            widgets::empty_state(ui, &th, Icon::History, "Nothing here yet", "Chapters you open will show up here so you can pick up where you left off.");
            if widgets::button(ui, &th, "Browse the library", BtnKind::Primary, Some(Icon::Library), None).clicked() {
                env.go(crate::router::Route::Library);
            }
            return;
        }
        let finished = recent.iter().filter(|r| env.store.progress(&r.chapter).map(|p| p.done).unwrap_or(false)).count();
        widgets::flow(ui, |ui| {
            widgets::badge(ui, &format!("{} opened", recent.len()), th.p.accent, th.p.accent_soft);
            widgets::badge(ui, &format!("{finished} finished"), th.p.on_secondary_container, th.p.secondary_container);
        });
        ui.add_space(14.0);
        for r in &recent {
            let done = env.store.progress(&r.chapter).map(|p| p.done).unwrap_or(false);
            let pct = env.store.progress(&r.chapter).map(|p| (p.scroll * 100.0).round() as i32).unwrap_or(0);
            let w = ui.available_width();
            let resp = widgets::card(ui, &th, vec2(w, 70.0), 13.0, |ui| {
                ui.horizontal(|ui| {
                    widgets::subject_badge(ui, &th, &r.subject_name, &r.color, 42.0);
                    ui.vertical(|ui| {
                        ui.set_width((w - 90.0).max(100.0));
                        ui.spacing_mut().item_spacing.y = 2.0;
                        widgets::label_trunc(ui, RichText::new(&r.title).font(fonts::bold(15.0)).color(th.p.ink));
                        let status = if done { "Finished".to_string() } else if pct > 0 { format!("{pct}% read") } else { "Opened".to_string() };
                        widgets::label_trunc(ui, RichText::new(format!("{} · {status}", r.subject_name)).font(fonts::regular(12.5)).color(th.p.ink_muted));
                    });
                });
            });
            if resp.clicked() {
                open_chapter(env, r.chapter.clone());
            }
            ui.add_space(8.0);
        }
        ui.add_space(8.0);
        if widgets::button(ui, &th, "Clear reading history", BtnKind::Ghost, Some(Icon::Trash), None).clicked() {
            env.store.s.recent.clear();
            env.store.touch();
            env.toast("Reading history cleared");
        }
    });
}
