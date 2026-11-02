//! The menu bar (File / View / Go / Help) — keeps every shortcut discoverable.
use egui::{Button, Ui};

use crate::actions::Action;
use crate::config::SITE_URL;
use crate::env::Env;
use crate::router::Route;

pub struct MenuState {
    pub can_back: bool,
    pub can_forward: bool,
}

fn item(ui: &mut Ui, env: &mut Env, label: &str, shortcut: &str, enabled: bool, a: Action) {
    let mut b = Button::new(label);
    if !shortcut.is_empty() {
        b = b.shortcut_text(shortcut);
    }
    if ui.add_enabled(enabled, b).clicked() {
        env.act(a);
        ui.close_menu();
    }
}

pub fn menu_bar(ui: &mut Ui, env: &mut Env, st: &MenuState) {
    egui::menu::bar(ui, |ui| {
        ui.menu_button("File", |ui| {
            item(ui, env, "Settings", "Ctrl+,", true, Action::Go(Route::Settings));
            item(ui, env, "Profile", "", true, Action::Go(Route::Profile));
            ui.separator();
            item(ui, env, "Reload content", "", true, Action::ReloadContent);
            item(ui, env, "Sign out", "", true, Action::SignOut);
            ui.separator();
            item(ui, env, "Quit", "Ctrl+Q", true, Action::Quit);
        });
        ui.menu_button("View", |ui| {
            item(ui, env, "Toggle dark mode", "Ctrl+D", true, Action::ToggleDark);
            ui.separator();
            item(ui, env, "Zoom in", "Ctrl++", true, Action::ZoomIn);
            item(ui, env, "Zoom out", "Ctrl+−", true, Action::ZoomOut);
            item(ui, env, "Actual size", "Ctrl+0", true, Action::ZoomReset);
            ui.separator();
            item(ui, env, "Full screen", "F11", true, Action::Fullscreen);
        });
        ui.menu_button("Go", |ui| {
            item(ui, env, "Back", "Alt+←", st.can_back, Action::Back);
            item(ui, env, "Forward", "Alt+→", st.can_forward, Action::Forward);
            ui.separator();
            item(ui, env, "Home", "Ctrl+1", true, Action::Go(Route::Home));
            item(ui, env, "Library", "Ctrl+2", true, Action::Go(Route::Library));
            item(ui, env, "Search", "Ctrl+K", true, Action::Go(Route::Search));
            item(ui, env, "Bookmarks", "Ctrl+4", true, Action::Go(Route::Bookmarks));
            item(ui, env, "Downloads", "Ctrl+5", true, Action::Go(Route::Downloads));
        });
        ui.menu_button("Help", |ui| {
            item(ui, env, "Keyboard shortcuts", "F1", true, Action::ShowShortcuts);
            item(ui, env, "NEBians website", "", true, Action::OpenUrl(SITE_URL.to_string()));
            ui.separator();
            item(ui, env, "About NEBians", "", true, Action::Go(Route::About));
        });
    });
}
