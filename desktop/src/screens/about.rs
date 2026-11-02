//! About — version, what NEBians is, content stats, and links to the web app.
use egui::{RichText, Ui};

use super::common::*;
use crate::config::{SITE_URL, VERSION};
use crate::env::Env;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

pub fn show(ui: &mut Ui, env: &mut Env) {
    scroll_page(ui, env, "about", |ui, env| {
        let th = env.theme.clone();
        ui.vertical_centered(|ui| {
            ui.add_space(8.0);
            env.logo.show(ui, 84.0);
            ui.add_space(14.0);
            widgets::heading(ui, &th, "NEBians", 32.0);
            widgets::muted(ui, &th, &format!("Desktop · version {VERSION}"));
            ui.add_space(8.0);
            ui.set_max_width(560.0);
            ui.add(egui::Label::new(RichText::new("The open learning community for Nepal. Notes, syllabus-aligned chapters, question banks and model papers for Class 8–12, CEE and IOE — free, and readable offline.").font(fonts::regular(15.0)).color(th.p.ink_muted)));
        });
        ui.add_space(24.0);
        let subjects: usize = env.tracks.iter().map(|t| t.subjects.len()).sum();
        let chapters = env.total_chapters();
        let tracks = env.tracks.len();
        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            widgets::heading(ui, &th, "In this library", 16.0);
            ui.add_space(6.0);
            ui.horizontal_wrapped(|ui| {
                widgets::badge(ui, &format!("{tracks} categories"), th.p.accent, th.p.accent_soft);
                widgets::badge(ui, &format!("{subjects} subjects"), th.p.accent, th.p.accent_soft);
                widgets::badge(ui, &format!("{chapters} chapters"), th.p.accent, th.p.accent_soft);
            });
            ui.add_space(8.0);
            if let Some(c) = &env.content {
                widgets::label(ui, RichText::new(format!("Reading from {}", c.base.display())).font(fonts::regular(12.5)).color(th.p.ink_faint));
            }
        });
        ui.add_space(14.0);
        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            widgets::heading(ui, &th, "On the web and Android", 16.0);
            widgets::muted(ui, &th, "The community forum, Neby AI, Canvas and the marketplace need an account and live in the web app and the Android app.");
            ui.add_space(8.0);
            ui.horizontal_wrapped(|ui| {
                if widgets::button(ui, &th, "Open NEBians web", BtnKind::Primary, Some(Icon::Globe), None).clicked() {
                    env.open_url(SITE_URL);
                }
                if widgets::button(ui, &th, "Privacy", BtnKind::Secondary, Some(Icon::Lock), None).clicked() {
                    env.open_url(&format!("{SITE_URL}/privacy/"));
                }
                if widgets::button(ui, &th, "Terms", BtnKind::Secondary, Some(Icon::File), None).clicked() {
                    env.open_url(&format!("{SITE_URL}/terms/"));
                }
            });
        });
        ui.add_space(14.0);
        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            widgets::heading(ui, &th, "Built with", 16.0);
            widgets::muted(ui, &th, "Rust · egui / eframe (native OpenGL, no webview) · Poppins · scraper · serde. Maths is typeset from the notes' LaTeX; figures are the repo's own SVG/WebP renders.");
        });
    });
}
