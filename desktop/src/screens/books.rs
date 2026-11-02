//! Study books — the PDF editions of the notes, listed by the server and downloaded on demand
//! (resumable), then opened in the system PDF viewer.
use egui::{vec2, Color32, Frame, Margin, RichText, Rounding, Sense, Stroke, Ui};

use super::common::*;
use crate::actions::Action;
use crate::data::content::Book;
use crate::data::downloads::book_key;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::theme::{fonts, spacing};
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct BooksState {
    task: Option<Task<Result<Vec<Book>>>>,
    books: Option<Vec<Book>>,
    error: Option<String>,
    filter: String,
    query: String,
    asked: bool,
}

pub fn track_label(t: &str) -> String {
    if t.chars().all(|c| c.is_ascii_digit()) && !t.is_empty() {
        format!("Class {t}")
    } else {
        t.to_uppercase()
    }
}

fn load(st: &mut BooksState, env: &Env) {
    let repo = env.repo.clone();
    st.task = Some(Task::spawn(&env.ctx, move || repo.books()));
    st.error = None;
    st.asked = true;
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut BooksState) {
    if !st.asked {
        load(st, env);
    }
    if let Some(t) = st.task.as_mut() {
        if let Some(res) = t.poll() {
            st.task = None;
            match res {
                Ok(mut b) => {
                    b.sort_by(|a, c| {
                        let key = |x: &Book| (x.grade.parse::<u32>().map(|n| (0, n)).unwrap_or((1, 0)), x.title.to_lowercase());
                        key(a).cmp(&key(c))
                    });
                    st.books = Some(b);
                }
                Err(e) => st.error = Some(e.to_string()),
            }
        }
    }
    scroll_page(ui, env, "books", |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Study books", Some("Print-quality PDF editions of every subject. Download once, read anywhere."));
        let Some(books) = st.books.clone() else {
            match st.error.clone() {
                Some(e) => load_state(ui, &th, Some(e), || st.asked = false),
                None => load_state(ui, &th, None, || {}),
            }
            return;
        };
        let w = ui.available_width();
        widgets::text_field(ui, &th, &mut st.query, "Filter books by subject", Some(Icon::Search), w.min(560.0), false);
        ui.add_space(12.0);
        let mut groups: Vec<String> = vec![];
        for b in &books {
            if !groups.contains(&b.track) {
                groups.push(b.track.clone());
            }
        }
        widgets::flow(ui, |ui| {
            if widgets::chip(ui, &th, "All", st.filter.is_empty()).clicked() {
                st.filter.clear();
            }
            for g in &groups {
                if widgets::chip(ui, &th, &track_label(g), st.filter == *g).clicked() {
                    st.filter = g.clone();
                }
            }
        });
        ui.add_space(18.0);
        let q = st.query.trim().to_lowercase();
        let shown: Vec<&Book> = books.iter().filter(|b| (st.filter.is_empty() || b.track == st.filter) && (q.is_empty() || b.title.to_lowercase().contains(&q))).collect();
        if shown.is_empty() {
            widgets::empty_state(ui, &th, Icon::Article, "No books match", "Try another category or clear the filter.");
            return;
        }
        widgets::grid(ui, 330.0, spacing::GRID_GAP, shown.len(), |ui, i, w| book_card(ui, env, shown[i], w));
    });
}

fn book_card(ui: &mut Ui, env: &mut Env, b: &Book, w: f32) {
    let th = env.theme.clone();
    let key = book_key(&b.slug);
    let file = env.repo.book_file(&b.slug);
    let hue = [0x004AC6u32, 0x7C3AED, 0x0F766E, 0x9A6206, 0xB3261E, 0x15803D];
    let n = b.slug.bytes().fold(0usize, |a, c| a.wrapping_add(c as usize));
    let col = {
        let c = hue[n % hue.len()];
        Color32::from_rgb((c >> 16) as u8, (c >> 8) as u8, c as u8)
    };
    Frame::none().fill(th.p.card).stroke(Stroke::new(1.0, th.p.hairline)).rounding(Rounding::same(spacing::CARD_RADIUS)).inner_margin(Margin::same(16.0)).show(ui, |ui| {
        ui.vertical(|ui| {
        ui.set_width(w - 34.0);
        ui.horizontal(|ui| {
            let (rect, _) = ui.allocate_exact_size(vec2(58.0, 76.0), Sense::hover());
            ui.painter().rect_filled(rect, Rounding::same(8.0), th.wash(col));
            ui.painter().rect_filled(egui::Rect::from_min_size(rect.min, vec2(6.0, rect.height())), Rounding { nw: 8.0, sw: 8.0, ..Default::default() }, col);
            ui.painter().text(rect.center() + vec2(2.0, -6.0), egui::Align2::CENTER_CENTER, "PDF", fonts::bold(13.0), col);
            ui.painter().text(rect.center() + vec2(2.0, 12.0), egui::Align2::CENTER_CENTER, track_label(&b.track), fonts::medium(10.0), th.p.ink_muted);
            ui.add_space(6.0);
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 3.0;
                ui.add(egui::Label::new(RichText::new(&b.subject).font(fonts::bold(16.0)).color(th.p.ink)).truncate());
                ui.add(egui::Label::new(RichText::new(&b.title).font(fonts::regular(12.5)).color(th.p.ink_muted)).truncate());
                ui.add_space(4.0);
                widgets::flow(ui, |ui| {
                    widgets::badge(ui, &crate::util::fmt_bytes(b.size), th.p.ink_muted, th.p.field);
                    if file.is_some() {
                        widgets::badge(ui, "On this computer", th.p.ok, th.p.ok_soft);
                    }
                });
            });
        });
        ui.add_space(12.0);
        if let Some(j) = env.dl.job(&key) {
            let frac = j.progress.frac();
            let (done, total) = (j.progress.done.load(std::sync::atomic::Ordering::Relaxed), j.progress.total.load(std::sync::atomic::Ordering::Relaxed));
            widgets::progress_bar(ui, &th, frac, 6.0, Some(th.p.accent));
            ui.add_space(6.0);
            ui.horizontal(|ui| {
                widgets::label(ui, RichText::new(format!("{} of {}", crate::util::fmt_bytes(done), crate::util::fmt_bytes(total))).font(fonts::regular(12.5)).color(th.p.ink_muted));
                right(ui, |ui| {
                    if widgets::button(ui, &th, "Pause", BtnKind::Secondary, Some(Icon::Close), None).clicked() {
                        env.dl.cancel(&key);
                    }
                });
            });
        } else if let Some(path) = file {
            ui.horizontal(|ui| {
                if widgets::button(ui, &th, "Open", BtnKind::Primary, Some(Icon::External), None).clicked() {
                    env.act(Action::OpenPath(path.clone()));
                }
                if widgets::icon_button(ui, &th, Icon::Trash, "Delete the downloaded copy", false).clicked() {
                    env.repo.delete_book(&b.slug);
                    env.toast("Deleted the downloaded copy");
                }
            });
        } else {
            let failed = env.dl.failed.iter().find(|(k, _)| *k == key).map(|(_, e)| e.clone());
            ui.horizontal(|ui| {
                let label = if failed.is_some() { "Retry download" } else { "Download" };
                if widgets::button(ui, &th, label, BtnKind::Secondary, Some(Icon::Download), None).clicked() {
                    let repo = env.repo.clone();
                    env.dl.start_book(&env.ctx.clone(), &repo, &b.slug, &b.subject);
                }
            });
            if let Some(e) = failed {
                ui.add_space(4.0);
                ui.add(egui::Label::new(RichText::new(crate::util::truncate(&e, 90)).font(fonts::regular(12.0)).color(th.p.danger)));
            }
        }
    });
    });
}
