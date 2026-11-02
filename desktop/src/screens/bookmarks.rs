//! Bookmarks (saved chapters) and reading history — Android's `BookmarksScreen`.
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::env::Env;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

pub fn show(ui: &mut Ui, env: &mut Env) {
    scroll_page(ui, env, "bookmarks", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Bookmarks", Some("Chapters you saved. Press Ctrl+B in the reader to save one."));
        let items = env.store.s.bookmarks.clone();
        if items.is_empty() {
            widgets::empty_state(ui, &th, Icon::Bookmark, "No bookmarks yet", "Open a chapter and tap the bookmark icon.");
        }
        let mut remove = None;
        for (i, b) in items.iter().enumerate() {
            let color = env.subject(&b.chapter.track, &b.chapter.subject).map(|s| s.color.clone()).unwrap_or_default();
            let track = env.track(&b.chapter.track).map(|t| t.short.clone()).unwrap_or_default();
            let w = ui.available_width();
            let resp = widgets::card(ui, &th, vec2(w, 74.0), 14.0, |ui| {
                ui.horizontal(|ui| {
                    widgets::subject_badge(ui, &th, &b.subject_name, &color, 44.0);
                    ui.vertical(|ui| {
                        ui.set_width((w - 140.0).max(100.0));
                        ui.spacing_mut().item_spacing.y = 2.0;
                        widgets::label_trunc(ui, RichText::new(&b.title).font(fonts::bold(15.0)).color(th.p.ink));
                        widgets::label_trunc(ui, RichText::new(format!("{} · {track} · {}", b.subject_name, b.chapter.kind.label())).font(fonts::regular(12.5)).color(th.p.ink_muted));
                    });
                });
            });
            // remove button floats over the card's right edge
            let btn_rect = egui::Rect::from_center_size(egui::pos2(resp.rect.max.x - 34.0, resp.rect.center().y), vec2(38.0, 38.0));
            let mut child = ui.new_child(egui::UiBuilder::new().max_rect(btn_rect));
            let trash = widgets::icon_button(&mut child, &th, Icon::Trash, "Remove bookmark", false);
            if trash.clicked() {
                remove = Some(i);
            } else if resp.clicked() && !btn_rect.contains(resp.interact_pointer_pos().unwrap_or_default()) {
                open_chapter(env, b.chapter.clone());
            }
            ui.add_space(8.0);
        }
        if let Some(i) = remove {
            env.store.s.bookmarks.remove(i);
            env.store.touch();
            env.toast("Bookmark removed");
        }

        ui.add_space(24.0);
        widgets::section_header(ui, &th, "Reading history", None);
        let recent = env.store.s.recent.clone();
        if recent.is_empty() {
            widgets::muted(ui, &th, "Chapters you open will show up here.");
        }
        for r in &recent {
            let done = env.store.progress(&r.chapter).map(|p| p.done).unwrap_or(false);
            let resp = widgets::card(ui, &th, vec2(ui.available_width(), 62.0), 12.0, |ui| {
                ui.horizontal(|ui| {
                    widgets::subject_badge(ui, &th, &r.subject_name, &r.color, 36.0);
                    ui.vertical(|ui| {
                        ui.spacing_mut().item_spacing.y = 1.0;
                        widgets::label_trunc(ui, RichText::new(&r.title).font(fonts::medium(14.5)).color(th.p.ink));
                        widgets::label_trunc(ui, RichText::new(format!("{}{}", r.subject_name, if done { "  ·  finished" } else { "" })).font(fonts::regular(12.0)).color(th.p.ink_muted));
                    });
                });
            });
            if resp.clicked() {
                open_chapter(env, r.chapter.clone());
            }
            ui.add_space(6.0);
        }
        if !recent.is_empty() {
            ui.add_space(8.0);
            if widgets::button(ui, &th, "Clear reading history", BtnKind::Ghost, Some(Icon::Trash), None).clicked() {
                env.store.s.recent.clear();
                env.store.touch();
                env.toast("Reading history cleared");
            }
        }
    });
}
