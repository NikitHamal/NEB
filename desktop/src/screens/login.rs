//! Welcome / sign-in chooser (Android `LoginScreen.kt`): brand mark, "Welcome to
//! NEBians", the community tagline, email sign-in or a guest path.
use egui::text::{LayoutJob, TextFormat};
use egui::{Align, Frame, Layout, Ui};

use crate::actions::Action;
use crate::config::SITE_URL;
use crate::env::Env;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

pub fn show(ui: &mut Ui, env: &mut Env) {
    let th = env.theme.clone();
    let compact = ui.available_width() < 560.0;
    egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| {
        let avail = ui.available_size();
        let w = (avail.x - 48.0).clamp(280.0, 420.0);
        ui.allocate_ui_with_layout(avail, Layout::top_down(Align::Center), |ui| {
            ui.add_space((avail.y * 0.5 - 250.0).max(24.0));
            ui.set_width(w);
            env.logo.show(ui, if compact { 60.0 } else { 76.0 });
            ui.add_space(26.0);

            let mut job = LayoutJob::default();
            job.halign = Align::Center;
            let big = if compact { 26.0 } else { 32.0 };
            job.append("Welcome to ", 0.0, TextFormat { font_id: fonts::bold(big), color: th.p.ink, ..Default::default() });
            job.append("NEBians", 0.0, TextFormat { font_id: fonts::bold(big), color: th.p.accent, ..Default::default() });
            ui.add(egui::Label::new(job).selectable(false));
            ui.add_space(10.0);
            let mut sub = LayoutJob::default();
            sub.halign = Align::Center;
            sub.append(
                "The open learning community for Nepal. Connect, learn, share study materials, and explore together.",
                0.0,
                TextFormat { font_id: fonts::regular(15.0), color: th.p.ink_muted, ..Default::default() },
            );
            ui.add(egui::Label::new(sub).selectable(false));
            ui.add_space(34.0);

            if widgets::button(ui, &th, "Continue with email", BtnKind::Primary, Some(Icon::Mail), Some(w)).clicked() {
                env.go(Route::EmailAuth);
            }
            ui.add_space(10.0);
            if widgets::button(ui, &th, "Continue as guest", BtnKind::Secondary, Some(Icon::Eye), Some(w)).clicked() {
                env.store.s.guest = true;
                if env.store.s.profile.role.is_empty() {
                    env.store.s.profile.role = "explorer".into();
                }
                env.store.touch();
                env.act(Action::Replace(Route::Onboarding));
            }
            ui.add_space(22.0);
            Frame::none().show(ui, |ui| {
                ui.set_width(w);
                ui.vertical_centered(|ui| {
                    ui.add(egui::Label::new(egui::RichText::new("By continuing you agree to the").font(fonts::regular(12.5)).color(th.p.ink_faint)).selectable(false));
                    ui.horizontal(|ui| {
                        ui.add_space(((w - 210.0) / 2.0).max(0.0));
                        ui.spacing_mut().item_spacing.x = 4.0;
                        if ui.link(egui::RichText::new("Terms of Service").font(fonts::medium(12.5)).color(th.p.accent)).clicked() {
                            env.open_url(&format!("{SITE_URL}/terms/"));
                        }
                        ui.add(egui::Label::new(egui::RichText::new("and").font(fonts::regular(12.5)).color(th.p.ink_faint)).selectable(false));
                        if ui.link(egui::RichText::new("Privacy Policy").font(fonts::medium(12.5)).color(th.p.accent)).clicked() {
                            env.open_url(&format!("{SITE_URL}/privacy/"));
                        }
                    });
                });
            });
        });
    });
}
