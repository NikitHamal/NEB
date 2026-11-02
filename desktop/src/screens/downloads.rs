//! Offline library: save whole subjects for reading without a connection, manage downloaded books and
//! see what the app keeps on this computer.
use egui::{RichText, Ui};

use super::common::*;
use crate::actions::Action;
use crate::data::downloads::subject_key;
use crate::env::Env;
use crate::router::Route;
use crate::theme::{fonts, spacing};
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct DownloadsState {
    stats: crate::data::content::CacheStats,
    stats_at: Option<std::time::Instant>,
    open_track: Option<String>,
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut DownloadsState) {
    if st.stats_at.map(|t| t.elapsed().as_secs() >= 2).unwrap_or(true) {
        st.stats = env.repo.stats();
        st.stats_at = Some(std::time::Instant::now());
    }
    scroll_page(ui, env, "downloads", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Offline library", Some("Save subjects and books to read without a connection."));

        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            ui.horizontal(|ui| {
                widgets::icon_tile(ui, &th, Icon::Download, 44.0);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 2.0;
                    widgets::label(ui, RichText::new(format!("{} saved on this computer", crate::util::fmt_bytes(st.stats.content_bytes + st.stats.book_bytes))).font(fonts::bold(16.0)).color(th.p.ink));
                    widgets::label(ui, RichText::new(format!("{} subjects offline · {} books", env.dl.offline.len(), st.stats.book_files)).font(fonts::regular(13.0)).color(th.p.ink_muted));
                });
                right(ui, |ui| {
                    if widgets::button(ui, &th, "Storage settings", BtnKind::Secondary, Some(Icon::Settings), None).clicked() {
                        env.go(Route::Settings);
                    }
                });
            });
        });
        ui.add_space(spacing::SECTION_GAP);

        let books = env.repo.downloaded_books();
        widgets::section_header(ui, &th, "Downloaded books", None);
        if books.is_empty() {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                widgets::muted(ui, &th, "No books downloaded yet.");
                ui.add_space(8.0);
                if widgets::button(ui, &th, "Browse study books", BtnKind::Primary, Some(Icon::Article), None).clicked() {
                    env.go(Route::Books);
                }
            });
        }
        for (slug, path, size) in books {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                ui.horizontal(|ui| {
                    widgets::icon_tile(ui, &th, Icon::File, 38.0);
                    ui.vertical(|ui| {
                        ui.spacing_mut().item_spacing.y = 1.0;
                        let title = slug.trim_start_matches("nebians-").replace('-', " ");
                        widgets::label(ui, RichText::new(title).font(fonts::medium(14.5)).color(th.p.ink));
                        widgets::label(ui, RichText::new(crate::util::fmt_bytes(size)).font(fonts::regular(12.5)).color(th.p.ink_muted));
                    });
                    right(ui, |ui| {
                        if widgets::icon_button(ui, &th, Icon::Trash, "Delete", false).clicked() {
                            env.repo.delete_book(&slug);
                            st.stats_at = None;
                        }
                        if widgets::button(ui, &th, "Open", BtnKind::Primary, Some(Icon::External), None).clicked() {
                            env.act(Action::OpenPath(path.clone()));
                        }
                    });
                });
            });
            ui.add_space(8.0);
        }
        ui.add_space(spacing::SECTION_GAP);

        widgets::section_header(ui, &th, "Subjects for offline reading", None);
        if env.tracks.is_empty() {
            content_missing(ui, env);
            return;
        }
        let tracks = env.tracks.clone();
        widgets::flow(ui, |ui| {
            for t in &tracks {
                let on = st.open_track.as_deref().map(|g| g == t.grade).unwrap_or_else(|| tracks.first().map(|f| f.grade == t.grade).unwrap_or(false));
                if widgets::chip(ui, &th, &t.short, on).clicked() {
                    st.open_track = Some(t.grade.clone());
                }
            }
        });
        ui.add_space(12.0);
        let cur = st.open_track.clone().or_else(|| tracks.first().map(|t| t.grade.clone())).unwrap_or_default();
        let Some(t) = tracks.iter().find(|t| t.grade == cur) else { return };
        for s in &t.subjects {
            let key = subject_key(&t.grade, &s.subject);
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                ui.horizontal(|ui| {
                    widgets::subject_badge(ui, &th, &s.name, &s.color, 38.0);
                    ui.vertical(|ui| {
                        ui.spacing_mut().item_spacing.y = 1.0;
                        widgets::label(ui, RichText::new(env.subject_name(s)).font(fonts::medium(14.5)).color(th.p.ink));
                        let sub = match env.dl.job(&key) {
                            Some(j) => format!("Saving… {} of {} chapters", j.progress.done.load(std::sync::atomic::Ordering::Relaxed), j.progress.total.load(std::sync::atomic::Ordering::Relaxed)),
                            None if env.dl.is_offline(&t.grade, &s.subject) => "Available offline".to_string(),
                            None => format!("{} chapters", s.notes_ready),
                        };
                        widgets::label(ui, RichText::new(sub).font(fonts::regular(12.5)).color(th.p.ink_muted));
                    });
                    right(ui, |ui| {
                        if env.dl.job(&key).is_some() {
                            if widgets::button(ui, &th, "Cancel", BtnKind::Secondary, Some(Icon::Close), None).clicked() {
                                env.dl.cancel(&key);
                            }
                        } else if env.dl.is_offline(&t.grade, &s.subject) {
                            if widgets::button(ui, &th, "Remove", BtnKind::Secondary, Some(Icon::Trash), None).clicked() {
                                let repo = env.repo.clone();
                                env.dl.remove_subject(&repo, &t.grade, &s.subject);
                                env.forget_subject(&t.grade, &s.subject);
                                st.stats_at = None;
                            }
                        } else if widgets::button(ui, &th, "Save offline", BtnKind::Secondary, Some(Icon::Download), None).clicked() {
                            let repo = env.repo.clone();
                            env.dl.start_subject(&env.ctx.clone(), &repo, &t.grade, &s.subject, &s.name);
                        }
                    });
                });
                if let Some(j) = env.dl.job(&key) {
                    ui.add_space(8.0);
                    widgets::progress_bar(ui, &th, j.progress.frac(), 5.0, Some(th.p.accent));
                }
            });
            ui.add_space(8.0);
        }
    });
}
