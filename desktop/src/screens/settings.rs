//! Settings — Android's grouped settings (Account / Tools / Preferences / About /
//! Account control) adapted for desktop, plus Content location and Shortcuts.
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::actions::Action;
use crate::config::{SITE_URL, VERSION};
use crate::data::store::{ReadingWidth, ThemeMode};
use crate::env::Env;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct SettingsState {
    stats: crate::data::content::CacheStats,
    stats_at: Option<std::time::Instant>,
    confirm_reset: bool,
    pw: Option<PwDialog>,
}

#[derive(Default)]
struct PwDialog {
    current: String,
    new: String,
    busy: Option<crate::data::tasks::Task<crate::errors::Result<String>>>,
    error: Option<String>,
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
            if env.signed_in() {
                if link_row(ui, &th, "Change password", "Other devices are signed out when you change it", Icon::Key) {
                    st.pw = Some(PwDialog::default());
                }
                widgets::hairline(ui, &th);
            }
            if link_row(ui, &th, "Account security", "Email address, sessions and account deletion — opens the NEBians website", Icon::Lock) {
                env.open_url(SITE_URL);
            }
            if env.signed_in() {
                widgets::hairline(ui, &th);
                let server = crate::config::api_base();
                if link_row(ui, &th, "Server", &format!("{server}  (set NEB_API_BASE to change)"), Icon::Cloud) {
                    env.open_url(SITE_URL);
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
            if link_row(ui, &th, "Privacy policy", "How we protect your data", Icon::Lock) {
                env.go(Route::Legal("privacy".into()));
            }
            widgets::hairline(ui, &th);
            if link_row(ui, &th, "Terms of service", "Rules and guidelines for usage", Icon::File) {
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
                if env.signed_in() || env.store.s.guest {
                    if widgets::button(ui, &th, "Sign out", BtnKind::Secondary, Some(Icon::Logout), None).clicked() {
                        env.act(Action::SignOut);
                    }
                } else if widgets::button(ui, &th, "Sign in", BtnKind::Primary, Some(Icon::Login), None).clicked() {
                    env.act(Action::Replace(Route::Login));
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

    password_dialog(ui.ctx(), env, st);
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

fn password_dialog(ctx: &egui::Context, env: &mut Env, st: &mut SettingsState) {
    let Some(d) = st.pw.as_mut() else { return };
    let th = env.theme.clone();
    if let Some(t) = d.busy.as_mut() {
        if let Some(r) = t.poll() {
            d.busy = None;
            match r {
                Ok(m) => {
                    env.toast(m);
                    st.pw = None;
                    // the server revokes every token on change; sign in again
                    env.act(Action::SignOut);
                    return;
                }
                Err(e) => {
                    if env.handle_api_error(&e) {
                        st.pw = None;
                        return;
                    }
                    d.error = Some(e.to_string());
                }
            }
        }
    }
    let d = st.pw.as_mut().unwrap();
    let mut close = false;
    let mut submit = false;
    egui::Window::new("Change password")
        .title_bar(false)
        .collapsible(false)
        .resizable(false)
        .anchor(egui::Align2::CENTER_CENTER, [0.0, 0.0])
        .fixed_size([ctx.screen_rect().width().min(460.0) - 40.0, 0.0])
        .frame(egui::Frame::none().fill(th.p.card).rounding(egui::Rounding::same(28.0)).stroke(egui::Stroke::new(1.0, th.p.hairline)).shadow(ctx.style().visuals.window_shadow).inner_margin(egui::Margin::same(24.0)))
        .show(ctx, |ui| {
            let w = ui.available_width();
            widgets::heading(ui, &th, "Change password", 22.0);
            widgets::muted(ui, &th, "You will be signed out everywhere and asked to sign in again.");
            ui.add_space(14.0);
            widgets::field(ui, &th, &mut d.current, "Current password", Some(Icon::Lock), w, true, false);
            ui.add_space(10.0);
            widgets::field(ui, &th, &mut d.new, "New password (8+ characters)", Some(Icon::Key), w, true, false);
            if let Some(e) = d.error.clone() {
                ui.add_space(10.0);
                crate::screens::login::error_banner(ui, &th, &e, w);
            }
            ui.add_space(16.0);
            ui.horizontal(|ui| {
                right(ui, |ui| {
                    ui.add_enabled_ui(d.busy.is_none() && !d.current.is_empty() && d.new.len() >= 8, |ui| {
                        if widgets::button(ui, &th, if d.busy.is_some() { "Saving…" } else { "Change password" }, BtnKind::Primary, None, None).clicked() {
                            submit = true;
                        }
                    });
                    if widgets::button(ui, &th, "Cancel", BtnKind::Ghost, None, None).clicked() {
                        close = true;
                    }
                });
            });
        });
    if submit {
        let (cur, new, tok) = (d.current.clone(), d.new.clone(), env.token().unwrap_or_default());
        d.error = None;
        d.busy = Some(crate::data::tasks::Task::spawn(ctx, move || crate::data::auth::change_password(&tok, &cur, &new)));
    }
    if close || ctx.input(|i| i.key_pressed(egui::Key::Escape)) {
        st.pw = None;
    }
}
