//! Home — mirrors Android's `HomeDashboardComponents.kt`: greeting hero with a
//! search pill, quick actions, continue studying, featured study guide,
//! browse-by-level and "New in Library".
use egui::{vec2, Frame, Margin, RichText, Rounding, Sense, Stroke, Ui};

use super::common::*;
use crate::data::models::ChapterKind;
use crate::env::Env;
use crate::router::Route;
use crate::theme::{fonts, spacing};
use crate::ui::icons::{self, Icon};
use crate::ui::widgets::{self, BtnKind};
use crate::ui::LayoutMode;

pub fn show(ui: &mut Ui, env: &mut Env) {
    scroll_page(ui, env, "home", |ui, env| {
        if env.tracks.is_empty() {
            content_missing(ui, env);
            return;
        }
        hero(ui, env);
        ui.add_space(spacing::SECTION_GAP - 8.0);
        quick_actions(ui, env);
        continue_studying(ui, env);
        featured(ui, env);
        browse(ui, env);
        new_in_library(ui, env);
        ui.add_space(8.0);
    });
}

fn hero(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    let name = env.store.display_name();
    let w = ui.available_width();
    let compact = env.layout == LayoutMode::Compact;
    Frame::none().fill(th.p.accent_soft).rounding(Rounding::same(spacing::PANEL_RADIUS)).inner_margin(Margin::same(if compact { 18.0 } else { 28.0 })).show(ui, |ui| {
        ui.set_width(w - if compact { 36.0 } else { 56.0 });
        widgets::label(ui, RichText::new(format!("Ready to learn, {name}?")).font(fonts::bold(if compact { 22.0 } else { 30.0 })).color(th.p.ink));
        ui.add_space(4.0);
        ui.add(egui::Label::new(RichText::new("Find notes, continue studying, or jump into a question bank without leaving NEBians.").font(fonts::regular(15.0)).color(th.p.ink_muted)));
        ui.add_space(16.0);
        // search pill (opens Search, like Android)
        let h = 50.0;
        let (rect, resp) = ui.allocate_exact_size(vec2(ui.available_width().min(640.0), h), Sense::click());
        let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.12);
        ui.painter().rect(rect, Rounding::same(999.0), th.p.card, Stroke::new(1.0, crate::theme::mix(th.p.hairline_strong, th.p.accent, hover)));
        icons::paint(ui.painter(), egui::Rect::from_center_size(egui::pos2(rect.min.x + 26.0, rect.center().y), vec2(20.0, 20.0)), Icon::Search, th.p.ink_muted);
        ui.painter().text(egui::pos2(rect.min.x + 48.0, rect.center().y), egui::Align2::LEFT_CENTER, "Search notes, topics and question banks", fonts::regular(15.0), th.p.ink_faint);
        if !compact {
            ui.painter().text(egui::pos2(rect.max.x - 18.0, rect.center().y), egui::Align2::RIGHT_CENTER, "Ctrl K", fonts::medium(12.0), th.p.ink_faint);
        }
        if resp.hovered() {
            ui.ctx().set_cursor_icon(egui::CursorIcon::Text);
        }
        if resp.clicked() {
            env.go(Route::Search);
        }
        ui.add_space(16.0);
        ui.horizontal_wrapped(|ui| {
            if widgets::button(ui, &th, "Open Library", BtnKind::Primary, Some(Icon::Library), None).clicked() {
                env.go(Route::Library);
            }
            if let Some(r) = env.store.s.recent.first().cloned() {
                let label = format!("Resume · {}", crate::util::truncate(&r.title, 30));
                if widgets::button(ui, &th, &label, BtnKind::Secondary, Some(Icon::Play), None).clicked() {
                    open_chapter(env, r.chapter);
                }
            }
        });
    });
}

fn quick_actions(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    let bm = env.store.s.bookmarks.len();
    let pdfs = env.content.as_ref().map(|c| c.list_pdfs().len()).unwrap_or(0);
    let items: Vec<(Icon, &str, String, Route)> = vec![
        (Icon::Library, "Library", format!("{} chapters ready", env.total_chapters()), Route::Library),
        (Icon::Bookmark, "Bookmarks", if bm == 0 { "Nothing saved yet".into() } else { format!("{bm} saved") }, Route::Bookmarks),
        (Icon::Download, "Downloads", if pdfs == 0 { "Offline library".into() } else { format!("{pdfs} study book PDFs") }, Route::Downloads),
        (Icon::Globe, "Web app", "Forum, Neby AI, Canvas".into(), Route::About),
    ];
    widgets::grid(ui, 210.0, spacing::GRID_GAP, items.len(), |ui, i, w| {
        let (icon, title, sub, route) = &items[i];
        let resp = widgets::card(ui, &th, vec2(w, 78.0), 14.0, |ui| {
            ui.horizontal(|ui| {
                let (rect, _) = ui.allocate_exact_size(vec2(44.0, 44.0), Sense::hover());
                ui.painter().rect_filled(rect, 12.0, th.p.accent_soft);
                icons::paint(ui.painter(), egui::Rect::from_center_size(rect.center(), vec2(22.0, 22.0)), *icon, th.p.accent);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 1.0;
                    widgets::label_trunc(ui, RichText::new(*title).font(fonts::bold(15.0)).color(th.p.ink));
                    widgets::label_trunc(ui, RichText::new(sub).font(fonts::regular(12.5)).color(th.p.ink_muted));
                });
            });
        });
        if resp.clicked() {
            if *icon == Icon::Globe {
                env.open_url(crate::config::SITE_URL);
            } else {
                env.go(route.clone());
            }
        }
    });
    ui.add_space(spacing::SECTION_GAP);
}

fn continue_studying(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    let recent: Vec<_> = env.store.s.recent.iter().take(6).cloned().collect();
    if recent.is_empty() {
        return;
    }
    widgets::section_header(ui, &th, "Continue studying", None);
    widgets::grid(ui, 300.0, spacing::GRID_GAP, recent.len(), |ui, i, w| {
        let r = &recent[i];
        let scroll = env.store.progress(&r.chapter).map(|p| p.scroll).unwrap_or(0.0);
        let done = env.store.progress(&r.chapter).map(|p| p.done).unwrap_or(false);
        let resp = widgets::card(ui, &th, vec2(w, 92.0), 14.0, |ui| {
            ui.horizontal(|ui| {
                widgets::subject_badge(ui, &th, &r.subject_name, &r.color, 44.0);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 2.0;
                    widgets::label_trunc(ui, RichText::new(&r.title).font(fonts::bold(14.5)).color(th.p.ink));
                    widgets::label_trunc(ui, RichText::new(&r.subject_name).font(fonts::regular(12.5)).color(th.p.ink_muted));
                    let status = if done { "Finished" } else if scroll > 20.0 { "In progress" } else { "Opened" };
                    widgets::label(ui, RichText::new(status).font(fonts::medium(11.5)).color(if done { th.p.ok } else { th.p.accent }));
                });
            });
        });
        if resp.clicked() {
            open_chapter(env, r.chapter.clone());
        }
    });
    ui.add_space(spacing::SECTION_GAP);
}

fn featured(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    let all: Vec<(String, usize)> = env.tracks.iter().enumerate().flat_map(|(ti, t)| (0..t.subjects.len()).filter(move |si| t.subjects[*si].notes_ready > 0).map(move |si| (t.grade.clone(), ti * 1000 + si))).collect();
    if all.is_empty() {
        return;
    }
    let pick = &all[(crate::util::day_number() as usize) % all.len()];
    let (ti, si) = (pick.1 / 1000, pick.1 % 1000);
    let track = env.tracks[ti].clone();
    let s = track.subjects[si].clone();
    widgets::section_header(ui, &th, "Featured study guide", Some("See all"));
    let color = th.subject_color(&s.color);
    let w = ui.available_width();
    let r = Frame::none().fill(th.wash(color)).rounding(Rounding::same(spacing::PANEL_RADIUS)).inner_margin(Margin::same(22.0)).show(ui, |ui| {
        ui.set_width(w - 44.0);
        ui.horizontal(|ui| {
            widgets::subject_badge(ui, &th, &s.name, &s.color, 64.0);
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 3.0;
                widgets::label(ui, RichText::new(format!("{} · {}", track.label, track.exam)).font(fonts::medium(12.5)).color(th.p.ink_muted));
                widgets::label(ui, RichText::new(env.subject_name(&s)).font(fonts::bold(22.0)).color(th.p.ink));
                widgets::label(ui, RichText::new(format!("{} chapters · {} topics · notes, practice questions and answers", s.notes_ready, s.topic_count)).font(fonts::regular(13.5)).color(th.p.ink_muted));
            });
        });
        ui.add_space(14.0);
        if widgets::button(ui, &th, "Open subject", BtnKind::Primary, Some(Icon::ChevronRight), None).clicked() {
            open_subject(env, &track.grade, &s.subject);
        }
    });
    let _ = r;
    ui.add_space(spacing::SECTION_GAP);
}

fn browse(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    if widgets::section_header(ui, &th, "Browse by level", Some("See all")) {
        env.go(Route::Library);
    }
    let tracks = env.tracks.clone();
    widgets::grid(ui, 220.0, spacing::GRID_GAP, tracks.len(), |ui, i, w| {
        let t = &tracks[i];
        let resp = widgets::card(ui, &th, vec2(w, 112.0), 16.0, |ui| {
            widgets::label_trunc(ui, RichText::new(&t.label).font(fonts::bold(16.5)).color(th.p.ink));
            widgets::label_trunc(ui, RichText::new(&t.exam).font(fonts::regular(12.5)).color(th.p.ink_muted));
            ui.add_space(8.0);
            ui.horizontal(|ui| {
                widgets::badge(ui, &format!("{} subjects", t.subjects.len()), th.p.accent, th.p.accent_soft);
                widgets::badge(ui, &format!("{} chapters", t.ready_total()), th.p.ink_muted, th.p.field);
            });
        });
        if resp.clicked() {
            env.go(Route::Category(t.grade.clone()));
        }
    });
    ui.add_space(spacing::SECTION_GAP);
}

fn new_in_library(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    let entrance: Vec<_> = env.tracks.iter().filter(|t| t.is_entrance()).cloned().collect();
    if entrance.is_empty() {
        return;
    }
    if widgets::section_header(ui, &th, "New in Library", Some("See All")) {
        env.go(Route::Library);
    }
    let mut items = vec![];
    for t in entrance.iter().rev() {
        for s in &t.subjects {
            items.push((t.grade.clone(), s.clone()));
        }
    }
    items.truncate(9);
    widgets::grid(ui, 260.0, spacing::GRID_GAP, items.len(), |ui, i, w| {
        let (track, s) = &items[i];
        if subject_card(ui, env, track, s, w) {
            open_subject(env, track, &s.subject);
        }
    });
    let _ = ChapterKind::Unit;
}
