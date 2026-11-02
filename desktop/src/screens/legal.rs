//! Privacy Policy / Terms of Service — the same text as the Android app, readable offline.
use egui::{RichText, Ui};

use super::common::*;
use super::legal_data::{Doc, PRIVACY, TERMS};
use crate::env::Env;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

pub fn doc_for(key: &str) -> &'static Doc {
    if key == "terms" {
        &TERMS
    } else {
        &PRIVACY
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, key: &str) {
    let d = doc_for(key);
    scroll_page(ui, env, &format!("legal-{key}"), |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, d.title, Some(&format!("NEBians Learning Platform · Nepal  ·  {}", d.updated)));
        ui.horizontal(|ui| {
            ui.spacing_mut().item_spacing.x = 10.0;
            let other = if key == "terms" { ("Privacy Policy", "privacy") } else { ("Terms of Service", "terms") };
            if widgets::button(ui, &th, other.0, BtnKind::Secondary, Some(Icon::File), None).clicked() {
                env.go(crate::router::Route::Legal(other.1.into()));
            }
            if widgets::button(ui, &th, "Open on the web", BtnKind::Ghost, Some(Icon::Globe), None).clicked() {
                env.open_url(d.url);
            }
        });
        ui.add_space(18.0);
        for s in d.sections {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                ui.horizontal(|ui| {
                    widgets::badge(ui, s.n, th.p.accent, th.p.accent_soft);
                    widgets::heading(ui, &th, s.title, 16.5);
                });
                ui.add_space(8.0);
                for p in s.paras {
                    ui.add(egui::Label::new(RichText::new(p.replace("**", "")).font(fonts::regular(14.5)).color(th.p.ink)).selectable(true));
                    ui.add_space(6.0);
                }
            });
            ui.add_space(12.0);
        }
        widgets::muted(ui, &th, "Questions? support@nebians.consica.com.np");
    });
}
