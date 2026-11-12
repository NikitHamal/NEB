//! Help — getting started, offline use, account questions, and the keyboard reference.
use egui::{RichText, Ui};

use super::common::*;
use crate::env::Env;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::shortcuts::SHORTCUTS;
use crate::ui::widgets::{self, BtnKind};

const FAQ: &[(&str, &str)] = &[
    ("Where does the content come from?", "Everything is loaded from the NEBians server and saved on this computer as you read, so chapters you have opened keep working with no connection. Use Offline (Ctrl+D) to download whole subjects and study books ahead of time."),
    ("How do I read without internet?", "Open the Offline screen and choose Save offline on a subject, or download a study book. Anything you opened before is already cached. A banner appears when the server cannot be reached; your library, bookmarks and progress still work."),
    ("How do I sign in?", "Sign in or create an account with email on the sign-in screen. Google and GitHub briefly open your browser for approval, then the app continues by itself."),
    ("Why don't I see my profile picture?", "Pictures are fetched from your NEBians account and cached. If you are offline the first time, initials are shown until the picture can be downloaded. "),
    ("Where are my bookmarks and progress stored?", "On this computer, in the app's settings folder. Signing in also syncs your profile and community bookmarks with your account."),
    ("How do I search?", "Press Ctrl+K from anywhere. Search covers every chapter, topic and question bank."),
];

pub fn show(ui: &mut Ui, env: &mut Env) {
    scroll_page(ui, env, "help", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Help");
        widgets::flow(ui, |ui| {
            if widgets::button(ui, &th, "Keyboard shortcuts", BtnKind::Secondary, Some(Icon::Keyboard), None).clicked() {
                env.act(crate::actions::Action::ShowShortcuts);
            }
            if widgets::button(ui, &th, "Copy support email", BtnKind::Secondary, Some(Icon::Mail), None).clicked() {
                env.copy("support@nebians.consica.com.np");
            }
            if widgets::button(ui, &th, "Privacy", BtnKind::Ghost, Some(Icon::Lock), None).clicked() {
                env.go(crate::router::Route::Legal("privacy".into()));
            }
            if widgets::button(ui, &th, "Terms", BtnKind::Ghost, Some(Icon::File), None).clicked() {
                env.go(crate::router::Route::Legal("terms".into()));
            }
        });
        ui.add_space(20.0);
        widgets::section_header(ui, &th, "Common questions", None);
        for (q, a) in FAQ {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                widgets::heading(ui, &th, q, 15.5);
                ui.add_space(4.0);
                ui.add(egui::Label::new(RichText::new(*a).font(fonts::regular(14.0)).color(th.p.ink_muted)));
            });
            ui.add_space(10.0);
        }
        ui.add_space(12.0);
        widgets::section_header(ui, &th, "Keyboard shortcuts", None);
        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            egui::Grid::new("help-shortcuts").num_columns(2).spacing([32.0, 12.0]).show(ui, |ui| {
                for (k, d) in SHORTCUTS {
                    ui.label(RichText::new(*k).font(fonts::medium(13.5)).color(th.p.accent));
                    ui.label(RichText::new(*d).font(fonts::regular(13.5)).color(th.p.ink_muted));
                    ui.end_row();
                }
            });
        });
    });
}
