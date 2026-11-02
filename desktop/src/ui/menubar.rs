//! Application menu bar (File · View · Go · Help). Everything is server/app backed — no file paths.
use egui::{Button, Context, Frame, Margin, Stroke, Ui};

use crate::actions::Action;
use crate::env::Env;
use crate::router::{Route, Router};
use crate::theme::fonts;

fn item(ui: &mut Ui, label: &str, shortcut: &str) -> bool {
    let mut b = Button::new(egui::RichText::new(label).font(fonts::regular(13.5)));
    if !shortcut.is_empty() {
        b = b.shortcut_text(egui::RichText::new(shortcut).font(fonts::regular(12.5)));
    }
    let clicked = ui.add(b).clicked();
    if clicked {
        ui.close_menu();
    }
    clicked
}

pub fn show(ctx: &Context, env: &mut Env, current: &Route, router: &Router) {
    let th = env.theme.clone();
    egui::TopBottomPanel::top("menubar")
        .exact_height(30.0)
        .frame(Frame::none().fill(th.p.card).stroke(Stroke::new(1.0, th.p.hairline)).inner_margin(Margin::symmetric(8.0, 0.0)))
        .show(ctx, |ui| {
            egui::menu::bar(ui, |ui| {
                ui.spacing_mut().button_padding = egui::vec2(10.0, 4.0);
                ui.menu_button(egui::RichText::new("File").font(fonts::medium(13.5)), |ui| {
                    ui.set_min_width(230.0);
                    if item(ui, "Search…", "Ctrl+K") {
                        env.act(Action::Go(Route::Search));
                    }
                    if item(ui, "Offline downloads", "Ctrl+D") {
                        env.act(Action::Go(Route::Downloads));
                    }
                    if item(ui, "Settings", "Ctrl+,") {
                        env.act(Action::Go(Route::Settings));
                    }
                    ui.separator();
                    if item(ui, "Refresh library from server", "") {
                        env.act(Action::ReloadContent);
                    }
                    if env.signed_in() {
                        if item(ui, "Sign out", "") {
                            env.act(Action::SignOut);
                        }
                    } else if item(ui, "Sign in…", "") {
                        env.act(Action::Replace(Route::Login));
                    }
                    ui.separator();
                    if item(ui, "Quit", "Ctrl+Q") {
                        env.act(Action::Quit);
                    }
                });
                ui.menu_button(egui::RichText::new("View").font(fonts::medium(13.5)), |ui| {
                    ui.set_min_width(230.0);
                    let dark = env.theme.dark;
                    if item(ui, if dark { "Switch to light theme" } else { "Switch to dark theme" }, "Ctrl+Shift+D") {
                        env.act(Action::ToggleDark);
                    }
                    ui.separator();
                    if item(ui, "Zoom in", "Ctrl++") {
                        env.act(Action::ZoomIn);
                    }
                    if item(ui, "Zoom out", "Ctrl+−") {
                        env.act(Action::ZoomOut);
                    }
                    if item(ui, "Actual size", "Ctrl+0") {
                        env.act(Action::ZoomReset);
                    }
                    ui.separator();
                    if item(ui, "Full screen", "F11") {
                        env.act(Action::Fullscreen);
                    }
                });
                ui.menu_button(egui::RichText::new("Go").font(fonts::medium(13.5)), |ui| {
                    ui.set_min_width(230.0);
                    ui.add_enabled_ui(router.can_back(), |ui| {
                        if item(ui, "Back", "Alt+←") {
                            env.act(Action::Back);
                        }
                    });
                    ui.add_enabled_ui(router.can_forward(), |ui| {
                        if item(ui, "Forward", "Alt+→") {
                            env.act(Action::Forward);
                        }
                    });
                    ui.separator();
                    for (label, key, route) in [
                        ("Home", "Ctrl+1", Route::Home),
                        ("Library", "Ctrl+2", Route::Library),
                        ("Community", "Ctrl+3", Route::Community),
                        ("Notifications", "Ctrl+4", Route::Notifications),
                        ("Bookmarks", "Ctrl+5", Route::Bookmarks),
                        ("Study books", "Ctrl+6", Route::Books),
                        ("People", "Ctrl+7", Route::People),
                        ("Reading history", "Ctrl+H", Route::History),
                        ("Profile", "", Route::Profile),
                    ] {
                        if item(ui, label, key) && *current != route {
                            env.act(Action::Go(route));
                        }
                    }
                });
                ui.menu_button(egui::RichText::new("Help").font(fonts::medium(13.5)), |ui| {
                    ui.set_min_width(230.0);
                    if item(ui, "Help & FAQ", "") {
                        env.act(Action::Go(Route::Help));
                    }
                    if item(ui, "Keyboard shortcuts", "F1") {
                        env.act(Action::ShowShortcuts);
                    }
                    ui.separator();
                    if item(ui, "Privacy policy", "") {
                        env.act(Action::Go(Route::Legal("privacy".into())));
                    }
                    if item(ui, "Terms of service", "") {
                        env.act(Action::Go(Route::Legal("terms".into())));
                    }
                    if item(ui, "Open NEBians website", "") {
                        env.act(Action::OpenUrl(crate::config::SITE_URL.into()));
                    }
                    ui.separator();
                    if item(ui, "About NEBians", "") {
                        env.act(Action::Go(Route::About));
                    }
                });
            });
        });
}
