//! Profile — who you are in NEBians plus your study stats. Editing lives in the account centre.
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::env::Env;
use crate::router::{AccountTab, Route};
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

fn stat(ui: &mut Ui, env: &Env, w: f32, value: String, label: &str) {
    let th = &env.theme;
    widgets::card(ui, th, vec2(w, 100.0), 16.0, |ui| {
        widgets::label(ui, RichText::new(value).font(fonts::bold(26.0)).color(th.p.ink));
        ui.add_space(4.0);
        widgets::label(ui, RichText::new(label).font(fonts::regular(12.5)).color(th.p.ink_muted));
    });
}

pub fn show(ui: &mut Ui, env: &mut Env) {
    scroll_page(ui, env, "profile", |ui, env| {
        let th = env.theme.clone();
        rise(ui, egui::Id::new("profile-rise"));
        let p = env.store.s.profile.clone();
        let email = env.store.s.session.as_ref().map(|s| s.email.clone()).unwrap_or_default();
        ui.horizontal(|ui| {
            let photo = env.store.s.session.as_ref().map(|s| s.photo_url.clone()).unwrap_or_default();
            crate::ui::remote_image::avatar(ui, &th, &p.display_name, p.avatar_tone, 84.0, &photo);
            ui.add_space(6.0);
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 2.0;
                widgets::heading(ui, &th, if p.display_name.is_empty() { "Your name" } else { &p.display_name }, 26.0);
                widgets::muted(ui, &th, &format!("@{}", if p.handle.is_empty() { "handle" } else { &p.handle }));
                if !email.is_empty() {
                    widgets::muted(ui, &th, &email);
                }
            });
        });
        ui.add_space(14.0);
        widgets::flow(ui, |ui| {
            if widgets::button(ui, &th, "Edit profile", BtnKind::Primary, Some(Icon::Edit), None).clicked() {
                env.go(Route::Account(AccountTab::Profile));
            }
            if widgets::button(ui, &th, "Security", BtnKind::Tonal, Some(Icon::Lock), None).clicked() {
                env.go(Route::Account(AccountTab::Security));
            }
            if widgets::button(ui, &th, "Settings", BtnKind::Ghost, Some(Icon::Settings), None).clicked() {
                env.go(Route::Settings);
            }
        });
        ui.add_space(22.0);

        let total: u32 = env.tracks.iter().map(|t| t.chapter_total()).sum();
        widgets::grid(ui, 160.0, 12.0, 4, |ui, i, w| match i {
            0 => stat(ui, env, w, env.store.total_done().to_string(), "chapters finished"),
            1 => stat(ui, env, w, env.store.s.bookmarks.len().to_string(), "bookmarks"),
            2 => stat(ui, env, w, env.store.s.recent.len().to_string(), "recently opened"),
            _ => stat(ui, env, w, total.to_string(), "chapters in the library"),
        });
        ui.add_space(24.0);

        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            let rows: Vec<(&str, String)> = vec![
                ("Role", crate::util::truncate(&p.role, 20)),
                ("Level", p.level.clone()),
                ("Subjects", p.subjects.join(", ")),
                ("Place", [p.district.as_str(), p.pradesh.as_str()].iter().filter(|s| !s.is_empty()).cloned().collect::<Vec<_>>().join(", ")),
                ("Campus", p.school.clone()),
                ("Born", p.dob.clone()),
                ("Bio", p.bio.clone()),
            ];
            egui::Grid::new("profile_grid").num_columns(2).spacing([24.0, 10.0]).show(ui, |ui| {
                for (k, v) in rows.into_iter().filter(|(_, v)| !v.is_empty()) {
                    widgets::label(ui, RichText::new(k).font(fonts::medium(13.0)).color(th.p.ink_muted));
                    ui.add(egui::Label::new(RichText::new(v).color(th.p.ink)).wrap());
                    ui.end_row();
                }
            });
        });
    });
}
