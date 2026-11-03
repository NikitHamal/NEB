//! Settings — Android's grouped settings (Account / Tools / Preferences / About /
//! Account control) adapted for desktop, plus Content location and Shortcuts.
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::actions::Action;
use crate::config::VERSION;
use crate::data::store::{ReadingWidth, ThemeMode};
use crate::env::Env;
use crate::router::{AccountTab, Route};
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct SettingsState {
    stats: crate::data::content::CacheStats,
    stats_at: Option<std::time::Instant>,
    confirm_reset: bool,
}

fn group(ui: &mut Ui, th: &crate::theme::Theme, title: &str, f: impl FnOnce(&mut Ui)) {
    widgets::label(ui, RichText::new(title.to_uppercase()).font(fonts::bold(12.0)).color(th.p.ink_muted));
    ui.add_space(6.0);
    widgets::panel_frame(th).inner_margin(egui::Margin::symmetric(18.0, 8.0)).show(ui, |ui| {
        ui.set_width(ui.available_width());
        ui.spacing_mut().item_spacing.y = 0.0;
        f(ui);
    });
    ui.add_space(22.0);
}

/// A tappable row with a trailing chevron.
fn link_row(ui: &mut Ui, th: &crate::theme::Theme, title: &str, sub: &str, icon: Icon) -> bool {
    let (rect, resp) = ui.allocate_exact_size(vec2(ui.available_width(), 62.0), egui::Sense::click());
    if resp.hovered() {
        ui.painter().rect_filled(rect.expand2(vec2(10.0, 0.0)), 10.0, th.p.field);
        ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
    }
    crate::ui::icons::paint(ui.painter(), egui::Rect::from_center_size(egui::pos2(rect.min.x + 14.0, rect.center().y), vec2(20.0, 20.0)), icon, th.p.ink_muted);
    ui.painter().text(egui::pos2(rect.min.x + 44.0, rect.center().y - 9.0), egui::Align2::LEFT_CENTER, title, fonts::medium(15.0), th.p.ink);
    ui.painter().text(egui::pos2(rect.min.x + 44.0, rect.center().y + 11.0), egui::Align2::LEFT_CENTER, sub, fonts::regular(12.5), th.p.ink_muted);
    crate::ui::icons::paint(ui.painter(), egui::Rect::from_center_size(egui::pos2(rect.max.x - 12.0, rect.center().y), vec2(16.0, 16.0)), Icon::ChevronRight, th.p.ink_faint);
    resp.clicked()
}

fn toggle_row(ui: &mut Ui, th: &crate::theme::Theme, title: &str, sub: &str, on: &mut bool) -> bool {
    let mut changed = false;
    ui.add_space(10.0);
    widgets::setting_row(ui, th, title, Some(sub), |ui| {
        changed = widgets::toggle(ui, th, on).changed();
    });
    ui.add_space(10.0);
    changed
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut SettingsState) {
    scroll_page(ui, env, "settings", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Settings");
        ui.set_max_width(ui.available_width().min(760.0));

        group(ui, &th, "Account", |ui| {
            let who = env.store.s.session.as_ref().map(|s| s.email.clone()).unwrap_or_default();
            let rows = [
                ("Edit profile", who.as_str(), Icon::User, Route::Account(AccountTab::Profile)),
                ("Security", "", Icon::Lock, Route::Account(AccountTab::Security)),
                ("Privacy and terms", "", Icon::Shield, Route::Account(AccountTab::Privacy)),
                ("Delete account", "", Icon::Trash, Route::Account(AccountTab::Delete)),
                ("Bookmarks", "", Icon::Bookmark, Route::Bookmarks),
            ];
            for (i, (title, sub, icon, route)) in rows.into_iter().enumerate() {
                if i > 0 {
                    widgets::hairline(ui, &th);
                }
                if link_row(ui, &th, title, sub, icon) {
                    env.go(route);
                }
            }
        });

        group(ui, &th, "Preferences", |ui| {
            ui.add_space(10.0);
            let mut idx = match env.store.s.prefs.theme {
                ThemeMode::System => 0,
                ThemeMode::Light => 1,
                ThemeMode::Dark => 2,
            };
            widgets::setting_row(ui, &th, "Theme", Some("Follow the system, or force light / dark"), |_| {});
            ui.add_space(6.0);
            if widgets::segmented(ui, &th, &["System", "Light", "Dark"], &mut idx) {
                env.store.s.prefs.theme = [ThemeMode::System, ThemeMode::Light, ThemeMode::Dark][idx];
                env.store.touch();
                env.refresh_theme();
            }
            ui.add_space(14.0);
            widgets::hairline(ui, &th);
            ui.add_space(10.0);
            widgets::setting_row(ui, &th, "Reading text size", Some("Scales chapter text, tables and equations"), |ui| {
                let mut v = env.store.s.prefs.font_scale;
                ui.add(egui::Slider::new(&mut v, 0.8..=1.6).show_value(false));
                widgets::label(ui, RichText::new(format!("{:.0}%", v * 100.0)).font(fonts::medium(13.0)).color(th.p.ink_muted));
                if (v - env.store.s.prefs.font_scale).abs() > f32::EPSILON {
                    env.store.s.prefs.font_scale = v;
                    env.store.touch();
                }
            });
            ui.add_space(10.0);
            widgets::hairline(ui, &th);
            ui.add_space(10.0);
            widgets::setting_row(ui, &th, "Reading width", Some("How wide the chapter column may grow"), |_| {});
            ui.add_space(6.0);
            let mut w = match env.store.s.prefs.reading_width {
                ReadingWidth::Compact => 0,
                ReadingWidth::Comfortable => 1,
                ReadingWidth::Wide => 2,
            };
            if widgets::segmented(ui, &th, &["Compact", "Comfortable", "Wide"], &mut w) {
                env.store.s.prefs.reading_width = [ReadingWidth::Compact, ReadingWidth::Comfortable, ReadingWidth::Wide][w];
                env.store.touch();
            }
            ui.add_space(14.0);
            widgets::hairline(ui, &th);
            let mut v = env.store.s.prefs.show_toc;
            if toggle_row(ui, &th, "Table of contents in the reader", "Show the section list beside the chapter", &mut v) {
                env.store.s.prefs.show_toc = v;
                env.store.touch();
            }
            widgets::hairline(ui, &th);
            let mut v = env.store.s.prefs.nepali_names;
            if toggle_row(ui, &th, "Nepali subject names", "Show नेपाली names first where available", &mut v) {
                env.store.s.prefs.nepali_names = v;
                env.store.touch();
            }
            widgets::hairline(ui, &th);
            let mut v = env.store.s.prefs.reduce_motion;
            if toggle_row(ui, &th, "Reduce motion", "Skip the splash animation and smooth scrolling", &mut v) {
                env.store.s.prefs.reduce_motion = v;
                env.store.touch();
            }
            widgets::hairline(ui, &th);
            let mut v = env.store.s.prefs.remember_window;
            if toggle_row(ui, &th, "Remember window size", "Reopen at the size you left it", &mut v) {
                env.store.s.prefs.remember_window = v;
                env.store.touch();
            }
        });

        group(ui, &th, "Storage & sync", |ui| {
            if st.stats_at.map(|t| t.elapsed().as_secs() >= 3).unwrap_or(true) {
                st.stats = env.repo.stats();
                st.stats_at = Some(std::time::Instant::now());
            }
            let server = crate::config::api_base();
            ui.add_space(10.0);
            widgets::setting_row(ui, &th, "Library server", Some(&server), |ui| {
                widgets::badge(ui, if matches!(env.status, crate::env::ContentStatus::Ready) { "Connected" } else { "Offline" }, th.p.ok, th.p.ok_soft);
            });
            ui.add_space(10.0);
            widgets::hairline(ui, &th);
            ui.add_space(10.0);
            let (cb, bb) = (st.stats.content_bytes, st.stats.book_bytes);
            widgets::setting_row(ui, &th, "Saved study content", Some(&format!("{} on this computer — chapters and figures you opened or saved offline", crate::util::fmt_bytes(cb))), |ui| {
                if widgets::button(ui, &th, "Clear", BtnKind::Secondary, Some(Icon::Trash), None).clicked() {
                    env.repo.clear_content();
                    env.dl.offline.clear();
                    env.drop_content_memory();
                    env.reload_content();
                    st.stats_at = None;
                    env.toast("Saved study content cleared");
                }
            });
            ui.add_space(10.0);
            widgets::hairline(ui, &th);
            ui.add_space(10.0);
            widgets::setting_row(ui, &th, "Downloaded books", Some(&format!("{} in {} PDF files", crate::util::fmt_bytes(bb), st.stats.book_files)), |ui| {
                if widgets::button(ui, &th, "Delete all", BtnKind::Secondary, Some(Icon::Trash), None).clicked() {
                    env.repo.clear_books();
                    st.stats_at = None;
                    env.toast("Downloaded books deleted");
                }
            });
            ui.add_space(10.0);
            widgets::hairline(ui, &th);
            ui.add_space(10.0);
            widgets::setting_row(ui, &th, "Refresh the library", Some("Check the server for new notes and question banks"), |ui| {
                if widgets::button(ui, &th, "Refresh", BtnKind::Secondary, Some(Icon::Refresh), None).clicked() {
                    env.act(crate::actions::Action::ReloadContent);
                }
            });
            ui.add_space(10.0);
        });

        group(ui, &th, "Keyboard", |ui| {
            if link_row(ui, &th, "Keyboard shortcuts", "Ctrl+K search, Esc back, Ctrl+, settings and more", Icon::Keyboard) {
                env.act(Action::ShowShortcuts);
            }
        });

        group(ui, &th, "About", |ui| {
            if link_row(ui, &th, "Help", "Questions, offline use and support", Icon::Info) {
                env.go(Route::Help);
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "Reading history", "Chapters you opened recently", Icon::History) {
                env.go(Route::History);
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "Privacy policy", "", Icon::Lock) {
                env.go(Route::Legal("privacy".into()));
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "Terms of service", "", Icon::File) {
                env.go(Route::Legal("terms".into()));
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "About NEBians", &format!("Version {VERSION}"), Icon::Info) {
                env.go(Route::About);
            }
        });

        group(ui, &th, "Account control", |ui| {
            ui.add_space(10.0);
            crate::ui::widgets::flow(ui, |ui| {
                if widgets::button(ui, &th, "Sign out", BtnKind::Secondary, Some(Icon::Logout), None).clicked() {
                    env.act(Action::SignOut);
                }
                if widgets::button(ui, &th, "Reset all local data", BtnKind::Danger, Some(Icon::Trash), None).clicked() {
                    st.confirm_reset = true;
                }
            });
            ui.add_space(10.0);
        });
    });

    if st.confirm_reset {
        let th = env.theme.clone();
        let mut act = None;
        let dismissed = crate::ui::dialog::show(ui.ctx(), &th, "reset-local", 440.0, |ui| {
            crate::ui::dialog::title(ui, &th, "Reset local data?");
            crate::ui::dialog::body(ui, &th, "Your profile, bookmarks and reading progress on this computer are removed and you are signed out.");
            act = crate::ui::dialog::confirm_row(ui, &th, "Reset", BtnKind::Danger, true);
        });
        if act == Some(true) {
            env.act(Action::ResetAll);
        }
        if act.is_some() || dismissed {
            st.confirm_reset = false;
        }
    }
}
