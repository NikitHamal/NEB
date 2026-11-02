//! Downloads / offline library — Android's `DownloadsScreen`. On desktop every
//! chapter is already on disk, so this screen reports the offline footprint and
//! manages the built study-book PDFs (open, save a copy, reveal in folder).
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::actions::Action;
use crate::data::content::PdfEntry;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};
use crate::util::fmt_bytes;

#[derive(Default)]
pub struct DownloadsState {
    pdfs: Option<Vec<PdfEntry>>,
    footprint: Option<(u64, u64)>,
    task: Option<Task<(u64, u64)>>,
    for_base: Option<std::path::PathBuf>,
    filter: String,
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut DownloadsState) {
    let base = env.content.as_ref().map(|c| c.base.clone());
    if st.for_base != base {
        st.for_base = base;
        st.pdfs = None;
        st.footprint = None;
        st.task = None;
    }
    if st.pdfs.is_none() {
        st.pdfs = Some(env.content.as_ref().map(|c| c.list_pdfs()).unwrap_or_default());
    }
    if st.footprint.is_none() && st.task.is_none() {
        if let Some(root) = env.content.clone() {
            st.task = Some(Task::spawn(&env.ctx, move || root.footprint()));
        }
    }
    if let Some(t) = st.task.as_mut() {
        if let Some(f) = t.poll() {
            st.footprint = Some(f);
            st.task = None;
        }
    }
    scroll_page(ui, env, "downloads", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Downloads", Some("Your offline library. Nothing here needs an internet connection."));

        // offline status card
        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            ui.horizontal(|ui| {
                let (rect, _) = ui.allocate_exact_size(vec2(44.0, 44.0), egui::Sense::hover());
                ui.painter().rect_filled(rect, 12.0, th.p.ok_soft);
                crate::ui::icons::paint(ui.painter(), egui::Rect::from_center_size(rect.center(), vec2(22.0, 22.0)), Icon::Check, th.p.ok);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 2.0;
                    match &env.content {
                        Some(_) => {
                            widgets::label(ui, RichText::new("All study material is available offline").font(fonts::bold(15.5)).color(th.p.ink));
                            let txt = match st.footprint {
                                Some((files, bytes)) => format!("{} chapters across {} subjects · {} files · {} on disk", env.total_chapters(), env.tracks.iter().map(|t| t.subjects.len()).sum::<usize>(), files, fmt_bytes(bytes)),
                                None => "Measuring…".to_string(),
                            };
                            widgets::label(ui, RichText::new(txt).font(fonts::regular(13.0)).color(th.p.ink_muted));
                        }
                        None => {
                            widgets::label(ui, RichText::new("No content folder found").font(fonts::bold(15.5)).color(th.p.danger));
                        }
                    }
                });
            });
            if let Some(c) = &env.content {
                ui.add_space(10.0);
                widgets::label(ui, RichText::new(format!("Location: {}", c.base.display())).font(fonts::regular(12.5)).color(th.p.ink_faint));
            }
            ui.add_space(10.0);
            ui.horizontal_wrapped(|ui| {
                if widgets::button(ui, &th, "Change content folder", BtnKind::Secondary, Some(Icon::Folder), None).clicked() {
                    env.go(Route::Settings);
                }
                if let Some(c) = env.content.clone() {
                    if widgets::button(ui, &th, "Show in file manager", BtnKind::Ghost, Some(Icon::External), None).clicked() {
                        env.act(Action::OpenPath(c.base));
                    }
                }
            });
        });

        ui.add_space(24.0);
        let pdfs = st.pdfs.clone().unwrap_or_default();
        widgets::section_header(ui, &th, &format!("Study book PDFs ({})", pdfs.len()), None);
        if pdfs.is_empty() {
            widgets::empty_state(ui, &th, Icon::File, "No PDFs found", "The built NEBians study books live in notes/pdf of your NEB checkout.");
            return;
        }
        widgets::text_field(ui, &th, &mut st.filter, "Filter books", Some(Icon::Search), ui.available_width().min(420.0), false);
        ui.add_space(12.0);
        let f = st.filter.to_lowercase();
        for p in pdfs.iter().filter(|p| f.is_empty() || p.name.to_lowercase().contains(&f)) {
            let w = ui.available_width();
            let resp = widgets::card(ui, &th, vec2(w, 74.0), 14.0, |ui| {
                ui.horizontal(|ui| {
                    let (rect, _) = ui.allocate_exact_size(vec2(44.0, 44.0), egui::Sense::hover());
                    ui.painter().rect_filled(rect, 12.0, th.p.danger_soft);
                    crate::ui::icons::paint(ui.painter(), egui::Rect::from_center_size(rect.center(), vec2(22.0, 22.0)), Icon::File, th.p.danger);
                    ui.vertical(|ui| {
                        ui.set_width((w - 300.0).max(120.0));
                        ui.spacing_mut().item_spacing.y = 2.0;
                        widgets::label_trunc(ui, RichText::new(p.name.replace("NEBians-", "").replace('-', " ")).font(fonts::bold(14.5)).color(th.p.ink));
                        widgets::label(ui, RichText::new(format!("PDF · {}", fmt_bytes(p.size))).font(fonts::regular(12.5)).color(th.p.ink_muted));
                    });
                });
            });
            let r = resp.rect;
            let mut child = ui.new_child(egui::UiBuilder::new().max_rect(egui::Rect::from_min_size(egui::pos2(r.max.x - 250.0, r.min.y + 14.0), vec2(240.0, 44.0))).layout(egui::Layout::right_to_left(egui::Align::Center)));
            child.spacing_mut().item_spacing.x = 6.0;
            let mut clicked_btn = false;
            if widgets::icon_button(&mut child, &th, Icon::External, "Open in your PDF viewer", false).clicked() {
                env.act(Action::OpenPath(p.path.clone()));
                clicked_btn = true;
            }
            if widgets::icon_button(&mut child, &th, Icon::Download, "Save a copy to your Downloads folder", false).clicked() {
                clicked_btn = true;
                let dest_dir = dirs::download_dir().unwrap_or_else(|| std::path::PathBuf::from("."));
                let dest = dest_dir.join(p.path.file_name().unwrap_or_default());
                match std::fs::copy(&p.path, &dest) {
                    Ok(_) => env.toast(format!("Saved to {}", dest.display())),
                    Err(e) => env.toast(format!("Could not save: {e}")),
                }
            }
            if widgets::icon_button(&mut child, &th, Icon::Folder, "Show in folder", false).clicked() {
                clicked_btn = true;
                if let Some(parent) = p.path.parent() {
                    env.act(Action::OpenPath(parent.to_path_buf()));
                }
            }
            if resp.clicked() && !clicked_btn {
                env.act(Action::OpenPath(p.path.clone()));
            }
            ui.add_space(8.0);
        }
    });
}
