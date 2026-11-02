//! Library (all categories) and Category (one track's subjects, grouped).
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::env::Env;
use crate::router::Route;
use crate::theme::{fonts, spacing};
use crate::ui::widgets;

#[derive(Default)]
pub struct LibraryState {
    /// 0 = All, otherwise 1-based index into `env.tracks`.
    filter: usize,
}

pub fn show_library(ui: &mut Ui, env: &mut Env, st: &mut LibraryState) {
    scroll_page(ui, env, "library", |ui, env| {
        let th = env.theme.clone();
        if env.tracks.is_empty() {
            content_missing(ui, env);
            return;
        }
        widgets::screen_header(ui, &th, "Library", Some("Every note, syllabus and question bank — available offline."));
        widgets::section_header(ui, &th, "Categories", None);
        let tracks = env.tracks.clone();
        widgets::grid(ui, 300.0, spacing::GRID_GAP, tracks.len(), |ui, i, w| {
            let t = &tracks[i];
            let resp = widgets::card(ui, &th, vec2(w, 118.0), 16.0, |ui| {
                widgets::label_trunc(ui, RichText::new(&t.label).font(fonts::bold(17.0)).color(th.p.ink));
                widgets::label_trunc(ui, RichText::new(&t.exam).font(fonts::regular(12.5)).color(th.p.ink_muted));
                ui.add_space(8.0);
                ui.horizontal(|ui| {
                    widgets::badge(ui, &format!("{} subjects", t.subjects.len()), th.p.accent, th.p.accent_soft);
                    widgets::badge(ui, &format!("{} chapters", t.ready_total()), th.p.ink_muted, th.p.field);
                });
                if !t.label_ne.is_empty() && env.store.s.prefs.nepali_names {
                    widgets::label(ui, RichText::new(&t.label_ne).font(fonts::regular(12.5)).color(th.p.ink_faint));
                }
            });
            if resp.clicked() {
                env.go(Route::Category(t.grade.clone()));
            }
        });
        ui.add_space(spacing::SECTION_GAP);
        widgets::section_header(ui, &th, "All subjects", None);
        ui.horizontal_wrapped(|ui| {
            if widgets::chip(ui, &th, "All", st.filter == 0).clicked() {
                st.filter = 0;
            }
            for (i, t) in tracks.iter().enumerate() {
                if widgets::chip(ui, &th, &t.short, st.filter == i + 1).clicked() {
                    st.filter = i + 1;
                }
            }
        });
        ui.add_space(14.0);
        let mut items = vec![];
        for (i, t) in tracks.iter().enumerate() {
            if st.filter == 0 || st.filter == i + 1 {
                for s in &t.subjects {
                    items.push((t.grade.clone(), s.clone()));
                }
            }
        }
        widgets::grid(ui, 270.0, spacing::GRID_GAP, items.len(), |ui, i, w| {
            let (track, s) = &items[i];
            if subject_card(ui, env, track, s, w) {
                open_subject(env, track, &s.subject);
            }
        });
    });
}

fn group_title(g: &str) -> String {
    match g {
        "compulsory" => "Compulsory subjects".into(),
        "optional" => "Optional subjects".into(),
        "science" => "Science stream".into(),
        "entrance" => "Entrance subjects".into(),
        "management" => "Management stream".into(),
        other => {
            let mut c = other.chars();
            c.next().map(|f| f.to_uppercase().collect::<String>() + c.as_str()).unwrap_or_default()
        }
    }
}

pub fn show_category(ui: &mut Ui, env: &mut Env, grade: &str) {
    let grade = grade.to_string();
    scroll_page(ui, env, &format!("category-{grade}"), |ui, env| {
        let th = env.theme.clone();
        let Some(track) = env.track(&grade).cloned() else {
            widgets::empty_state(ui, &th, crate::ui::icons::Icon::Library, "Category not found", "Pick one from the Library.");
            return;
        };
        ui.horizontal(|ui| {
            if widgets::icon_button(ui, &th, crate::ui::icons::Icon::Back, "Back", false).clicked() {
                env.act(crate::actions::Action::Back);
            }
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 0.0;
                widgets::heading(ui, &th, &track.label, 26.0);
                widgets::muted(ui, &th, &track.exam);
            });
        });
        ui.add_space(8.0);
        ui.horizontal_wrapped(|ui| {
            widgets::badge(ui, &format!("{} subjects", track.subjects.len()), th.p.accent, th.p.accent_soft);
            widgets::badge(ui, &format!("{} chapters", track.ready_total()), th.p.ink_muted, th.p.field);
            let done: u32 = track.subjects.iter().map(|s| env.store.done_count_in(&track.grade, &s.subject)).sum();
            widgets::badge(ui, &format!("{done} finished"), th.p.ok, th.p.ok_soft);
        });
        ui.add_space(spacing::SECTION_GAP - 8.0);
        let mut groups: Vec<String> = vec![];
        for s in &track.subjects {
            if !groups.contains(&s.group) {
                groups.push(s.group.clone());
            }
        }
        for g in groups {
            widgets::section_header(ui, &th, &group_title(&g), None);
            let items: Vec<_> = track.subjects.iter().filter(|s| s.group == g).cloned().collect();
            widgets::grid(ui, 270.0, spacing::GRID_GAP, items.len(), |ui, i, w| {
                if subject_card(ui, env, &track.grade, &items[i], w) {
                    open_subject(env, &track.grade, &items[i].subject);
                }
            });
            ui.add_space(spacing::SECTION_GAP - 6.0);
        }
    });
}
