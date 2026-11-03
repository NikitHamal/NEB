//! Search (Ctrl+K): instant structural results (subjects, units, topics) plus a
//! debounced, cancellable full-text scan of every chapter on disk. ↑/↓/Enter
//! navigate results from the keyboard.
use std::time::{Duration, Instant};

use egui::text::{LayoutJob, TextFormat};
use egui::{vec2, Align, Key, RichText, Ui};

use super::common::*;
use crate::data::search::{remote, HitKind, SearchHit};
use crate::errors::Result;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::router::Route;
use crate::theme::{fonts, spacing};
use crate::ui::icons::Icon;
use crate::ui::widgets;

#[derive(Default)]
pub struct SearchState {
    pub query: String,
    pub focus: bool,
    structural: Vec<SearchHit>,
    text_hits: Vec<SearchHit>,
    text_task: Option<Task<Result<Vec<SearchHit>>>>,
    error: Option<String>,
    last_run: String,
    changed_at: Option<Instant>,
    selected: usize,
}

fn open_hit(env: &mut Env, h: &SearchHit) {
    match (&h.kind, &h.chapter) {
        (HitKind::Subject, _) | (_, None) => open_subject(env, &h.track, &h.subject),
        (_, Some(c)) => open_chapter(env, c.clone()),
    }
}

fn highlight(th: &crate::theme::Theme, text: &str, q: &str, size: f32, base: egui::Color32) -> LayoutJob {
    let mut job = LayoutJob::default();
    job.wrap.max_rows = 2;
    job.wrap.break_anywhere = false;
    let lower = text.to_lowercase();
    let needles: Vec<String> = q.to_lowercase().split_whitespace().map(str::to_owned).collect();
    let mut i = 0;
    let norm = TextFormat { font_id: fonts::regular(size), color: base, ..Default::default() };
    let hot = TextFormat { font_id: fonts::bold(size), color: th.p.accent, ..Default::default() };
    // lower-casing can change byte lengths for exotic chars; fall back to plain text then
    if lower.len() != text.len() {
        job.append(text, 0.0, norm);
        return job;
    }
    while i < text.len() {
        let next = needles.iter().filter_map(|n| lower[i..].find(n.as_str()).map(|p| (p + i, n.len()))).min_by_key(|(p, _)| *p);
        match next {
            Some((p, l)) if l > 0 && text.is_char_boundary(p) && text.is_char_boundary(p + l) => {
                if p > i {
                    job.append(&text[i..p], 0.0, norm.clone());
                }
                job.append(&text[p..p + l], 0.0, hot.clone());
                i = p + l;
            }
            _ => {
                job.append(&text[i..], 0.0, norm.clone());
                break;
            }
        }
    }
    job
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut SearchState) {
    let th = env.theme.clone();

    if st.query != st.last_run {
        st.last_run = st.query.clone();
        st.selected = 0;
        st.changed_at = Some(Instant::now());
        if st.query.trim().chars().count() < 2 {
            st.structural.clear();
            st.text_hits.clear();
            st.error = None;
            st.text_task = None;
            st.changed_at = None;
        }
    }
    if let (Some(t0), true) = (st.changed_at, st.query.trim().chars().count() >= 2) {
        if t0.elapsed() > Duration::from_millis(250) {
            st.changed_at = None;
            let q = st.query.trim().to_string();
            st.text_task = Some(Task::spawn(&env.ctx, move || remote(&q)));
        } else {
            ui.ctx().request_repaint_after(Duration::from_millis(100));
        }
    }
    if let Some(t) = st.text_task.as_mut() {
        if let Some(res) = t.poll() {
            st.text_task = None;
            match res {
                Ok(h) => {
                    st.structural = h.iter().filter(|x| x.kind != HitKind::Text).cloned().collect();
                    st.text_hits = h.into_iter().filter(|x| x.kind == HitKind::Text).collect();
                    st.error = None;
                }
                Err(e) => st.error = Some(e.to_string()),
            }
        }
    }

    // flattened list for keyboard navigation
    let mut flat: Vec<SearchHit> = vec![];
    flat.extend(st.structural.iter().filter(|h| h.kind == HitKind::Subject).cloned());
    flat.extend(st.structural.iter().filter(|h| h.kind != HitKind::Subject).take(25).cloned());
    flat.extend(st.text_hits.iter().take(30).cloned());
    let (down, up, enter) = ui.input(|i| (i.key_pressed(Key::ArrowDown), i.key_pressed(Key::ArrowUp), i.key_pressed(Key::Enter)));
    if down && st.selected + 1 < flat.len() {
        st.selected += 1;
    }
    if up && st.selected > 0 {
        st.selected -= 1;
    }

    scroll_page(ui, env, "search", |ui, env| {
        widgets::screen_header(ui, &th, "Search");
        let w = ui.available_width();
        let r = widgets::text_field(ui, &th, &mut st.query, "Search notes, topics and question banks", Some(Icon::Search), w.min(720.0), false);
        if st.focus {
            r.request_focus();
            st.focus = false;
        }
        if r.has_focus() && enter {
            if let Some(h) = flat.get(st.selected).cloned() {
                open_hit(env, &h);
            }
        }
        ui.add_space(14.0);

        let q = st.query.trim().to_string();
        if q.is_empty() {
            widgets::section_header(ui, &th, "Try searching for", None);
            crate::ui::widgets::flow(ui, |ui| {
                for s in ["projectile motion", "Ohm's law", "vectors", "accountancy", "photosynthesis", "matrix", "IOE model paper"] {
                    if widgets::chip(ui, &th, s, false).clicked() {
                        st.query = s.to_string();
                        st.focus = true;
                    }
                }
            });
            if !env.store.s.recent.is_empty() {
                ui.add_space(spacing::SECTION_GAP);
                widgets::section_header(ui, &th, "Recently opened", None);
                let recent: Vec<_> = env.store.s.recent.iter().take(5).cloned().collect();
                for r in recent {
                    let resp = widgets::card(ui, &th, vec2(ui.available_width(), 62.0), 12.0, |ui| {
                        ui.horizontal(|ui| {
                            widgets::subject_badge(ui, &th, &r.subject_name, &r.color, 36.0);
                            ui.vertical(|ui| {
                                ui.spacing_mut().item_spacing.y = 1.0;
                                widgets::label_trunc(ui, RichText::new(&r.title).font(fonts::medium(14.5)).color(th.p.ink));
                                widgets::label_trunc(ui, RichText::new(&r.subject_name).font(fonts::regular(12.0)).color(th.p.ink_muted));
                            });
                        });
                    });
                    if resp.clicked() {
                        open_chapter(env, r.chapter.clone());
                    }
                    ui.add_space(6.0);
                }
            }
            return;
        }
        if let Some(e) = &st.error {
            widgets::empty_state(ui, &th, Icon::Warning, "Search is unavailable", e);
            return;
        }
        if st.text_task.is_some() && flat.is_empty() {
            ui.horizontal(|ui| {
                ui.spinner();
                widgets::muted(ui, &th, "Searching the library…");
            });
            return;
        }
        if flat.is_empty() && st.changed_at.is_none() && st.text_task.is_none() {
            if q.chars().count() < 2 {
                widgets::muted(ui, &th, "Keep typing — two letters or more.");
            } else {
                widgets::empty_state(ui, &th, Icon::Search, "No results", &format!("Nothing matched “{q}”. Try a shorter or different word."));
            }
            return;
        }
        let mut n = 0usize;
        let section = |ui: &mut Ui, env: &mut Env, st: &SearchState, title: &str, hits: Vec<SearchHit>, n: &mut usize| {
            if hits.is_empty() {
                return;
            }
            widgets::section_header(ui, &th, title, None);
            for h in hits {
                let selected = *n == st.selected;
                let color = th.subject_color(&h.color);
                let resp = widgets::card(ui, &th, vec2(ui.available_width(), 80.0), 12.0, |ui| {
                    ui.horizontal(|ui| {
                        widgets::subject_badge(ui, &th, &h.subject_name, &h.color, 38.0);
                        ui.vertical(|ui| {
                            ui.spacing_mut().item_spacing.y = 2.0;
                            ui.horizontal(|ui| {
                                ui.add(egui::Label::new(highlight(&th, &h.title, &q, 14.5, th.p.ink)).selectable(false).truncate());
                                widgets::badge(ui, &h.track_label, color, th.wash(color));
                            });
                            ui.add(egui::Label::new(highlight(&th, &h.snippet, &q, 12.5, th.p.ink_muted)).selectable(false));
                        });
                    });
                });
                if selected {
                    ui.painter().rect_stroke(resp.rect, spacing::CARD_RADIUS, egui::Stroke::new(2.0_f32, th.p.accent));
                    if down || up {
                        ui.scroll_to_rect(resp.rect, Some(Align::Center));
                    }
                }
                if resp.clicked() {
                    open_hit(env, &h);
                }
                *n += 1;
                ui.add_space(6.0);
            }
            ui.add_space(12.0);
        };
        let subjects: Vec<_> = st.structural.iter().filter(|h| h.kind == HitKind::Subject).cloned().collect();
        let units: Vec<_> = st.structural.iter().filter(|h| h.kind != HitKind::Subject).take(25).cloned().collect();
        section(ui, env, st, "Subjects", subjects, &mut n);
        section(ui, env, st, "Units & topics", units, &mut n);
        let texts: Vec<_> = st.text_hits.iter().take(30).cloned().collect();
        if st.text_task.is_some() {
            ui.horizontal(|ui| {
                ui.spinner();
                widgets::muted(ui, &th, "Searching the text of every chapter…");
            });
        }
        section(ui, env, st, "In the text", texts, &mut n);
    });
    let _ = Route::Search;
}
