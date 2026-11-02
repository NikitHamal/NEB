//! Settings — Android's grouped settings (Account / Tools / Preferences / About /
//! Account control) adapted for desktop, plus Content location and Shortcuts.
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::actions::Action;
use crate::config::{SITE_URL, VERSION};
use crate::data::content::ContentRoot;
use crate::data::store::{ReadingWidth, ThemeMode};
use crate::env::Env;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct SettingsState {
    path_input: String,
    path_msg: Option<(String, bool)>,
    confirm_reset: bool,
    inited: bool,
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
    if !st.inited {
        st.inited = true;
        st.path_input = env.content.as_ref().map(|c| c.base.display().to_string()).unwrap_or_default();
    }
    scroll_page(ui, env, "settings", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Settings", Some("Preferences are saved on this computer."));
        ui.set_max_width(ui.available_width().min(760.0));

        group(ui, &th, "Account", |ui| {
            let who = match (&env.store.s.session, env.store.s.guest) {
                (Some(s), _) => format!("Signed in as {}", s.email),
                (None, true) => "Browsing as a guest".to_string(),
                _ => "Not signed in".to_string(),
            };
            if link_row(ui, &th, "Profile", &who, Icon::User) {
                env.go(Route::Profile);
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "Bookmarks", "Saved chapters", Icon::Bookmark) {
                env.go(Route::Bookmarks);
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "Account security", "Password and sessions — opens the NEBians website", Icon::Lock) {
                env.open_url(SITE_URL);
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

        group(ui, &th, "Content", |ui| {
            ui.add_space(10.0);
            widgets::label(ui, RichText::new("Study content folder").font(fonts::medium(15.0)).color(th.p.ink));
            widgets::label(ui, RichText::new("Your NEB checkout (contains backend_python/web/data) or a bundled content/ folder.").font(fonts::regular(12.5)).color(th.p.ink_muted));
            ui.add_space(8.0);
            let w = ui.available_width();
            widgets::text_field(ui, &th, &mut st.path_input, "/path/to/NEB", Some(Icon::Folder), w, false);
            ui.add_space(8.0);
            ui.horizontal_wrapped(|ui| {
                if widgets::button(ui, &th, "Apply", BtnKind::Primary, Some(Icon::Check), None).clicked() {
                    match ContentRoot::from_dir(std::path::Path::new(st.path_input.trim())) {
                        Some(root) => {
                            env.store.s.prefs.content_dir = Some(root.base.display().to_string());
                            env.store.touch();
                            env.set_content(Some(root));
                            st.path_msg = Some((format!("Loaded {} subjects.", env.tracks.iter().map(|t| t.subjects.len()).sum::<usize>()), true));
                        }
                        None => st.path_msg = Some(("That folder has no backend_python/web/data/syllabus/index.json (or data/syllabus/index.json).".into(), false)),
                    }
                }
                if widgets::button(ui, &th, "Auto-detect", BtnKind::Secondary, None, None).clicked() {
                    match ContentRoot::detect(None, None) {
                        Some(root) => {
                            st.path_input = root.base.display().to_string();
                            env.store.s.prefs.content_dir = None;
                            env.store.touch();
                            env.set_content(Some(root));
                            st.path_msg = Some(("Found content next to the app.".into(), true));
                        }
                        None => st.path_msg = Some(("Nothing found next to the app or in its parent folders.".into(), false)),
                    }
                }
            });
            if let Some((m, ok)) = &st.path_msg {
                ui.add_space(6.0);
                ui.add(egui::Label::new(RichText::new(m).color(if *ok { th.p.ok } else { th.p.danger })));
            }
            ui.add_space(10.0);
        });

        group(ui, &th, "Keyboard", |ui| {
            if link_row(ui, &th, "Keyboard shortcuts", "Ctrl+K search, Esc back, Ctrl+, settings and more", Icon::Keyboard) {
                env.act(Action::ShowShortcuts);
            }
        });

        group(ui, &th, "About", |ui| {
            if link_row(ui, &th, "Privacy policy", "How we protect your data", Icon::Lock) {
                env.open_url(&format!("{SITE_URL}/privacy/"));
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "Terms of service", "Rules and guidelines for usage", Icon::File) {
                env.open_url(&format!("{SITE_URL}/terms/"));
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "About NEBians", &format!("Version {VERSION}"), Icon::Info) {
                env.go(Route::About);
            }
        });

        group(ui, &th, "Account control", |ui| {
            ui.add_space(10.0);
            ui.horizontal_wrapped(|ui| {
                if widgets::button(ui, &th, "Sign out", BtnKind::Secondary, Some(Icon::Logout), None).clicked() {
                    env.act(Action::SignOut);
                }
                if widgets::button(ui, &th, "Reset all local data", BtnKind::Danger, Some(Icon::Trash), None).clicked() {
                    st.confirm_reset = true;
                }
            });
            ui.add_space(6.0);
            widgets::label(ui, RichText::new("Resetting removes your profile, bookmarks and reading progress from this computer. Study content is not touched.").font(fonts::regular(12.5)).color(th.p.ink_muted));
            ui.add_space(10.0);
        });
    });

    if st.confirm_reset {
        let th = env.theme.clone();
        let mut open = true;
        egui::Window::new("Reset all local data?").open(&mut open).collapsible(false).resizable(false).anchor(egui::Align2::CENTER_CENTER, [0.0, 0.0]).show(ui.ctx(), |ui| {
            ui.add(egui::Label::new("This permanently deletes your profile, bookmarks and progress on this computer."));
            ui.add_space(10.0);
            ui.horizontal(|ui| {
                if widgets::button(ui, &th, "Reset", BtnKind::Danger, None, None).clicked() {
                    st.confirm_reset = false;
                    env.act(Action::ResetAll);
                }
                if widgets::button(ui, &th, "Cancel", BtnKind::Secondary, None, None).clicked() {
                    st.confirm_reset = false;
                }
            });
        });
        if !open {
            st.confirm_reset = false;
        }
    }
}
