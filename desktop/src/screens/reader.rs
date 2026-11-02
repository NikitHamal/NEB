//! Content reader — the heart of the app. Loads a chapter JSON from the repo's
//! study data on a worker thread, parses its HTML into blocks, and renders them
//! natively with a table of contents, reading progress, bookmarks, text size,
//! keyboard paging, interactive MCQs and (for IOE model papers) a timed-test clock.
use std::collections::HashMap;
use std::time::{Duration, Instant};

use egui::{vec2, Align, Frame, Key, Layout, Margin, RichText, Sense, Ui};

use super::common::*;
use crate::actions::Action;
use crate::data::models::{ChapterKind, ChapterRef, ExamMeta, TocItem};
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::{AppError, Result};
use crate::reader::model::Doc;
use crate::reader::{html, render};
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

pub struct ChMeta {
    title: String,
    area: String,
    read_min: u32,
    words: u32,
    figures: u32,
    toc: Vec<TocItem>,
    exam: Option<ExamMeta>,
}

type Loaded = Result<(ChMeta, Doc)>;

#[derive(Default)]
pub struct ReaderState {
    current: Option<ChapterRef>,
    loaded: Option<(ChMeta, Doc)>,
    task: Option<Task<Loaded>>,
    error: Option<String>,
    jump: Option<String>,
    scroll_goal: Option<f32>,
    restore: Option<f32>,
    offset: f32,
    content_h: f32,
    view_h: f32,
    heads: Vec<(String, f32)>,
    current_head: Option<String>,
    mcq: HashMap<usize, char>,
    timer: Option<Instant>,
    pending_jump: Option<String>,
    jump_age: u32,
    pending_answers: Vec<(usize, char)>,
}

impl ReaderState {
    fn start(&mut self, env: &mut Env, c: &ChapterRef) {
        let (pj, pa) = (self.pending_jump.take(), std::mem::take(&mut self.pending_answers));
        *self = ReaderState { current: Some(c.clone()), pending_jump: pj, pending_answers: pa, ..Default::default() };
        env.ctx.forget_all_images();
        let repo = env.repo.clone();
        let r = c.clone();
        self.restore = env.store.progress(c).map(|p| p.scroll).filter(|s| *s > 40.0);
        self.task = Some(Task::spawn(&env.ctx, move || -> Loaded {
            let ch = repo.chapter(&r)?;
            repo.prefetch_assets(&ch.html);
            let doc = html::parse(&ch.html);
            Ok((ChMeta { title: ch.title, area: ch.area, read_min: ch.read_min, words: ch.words, figures: ch.figures, toc: ch.toc, exam: ch.exam }, doc))
        }));
    }

    pub fn set_jump(&mut self, id: &str) {
        self.pending_jump = Some(id.to_string());
    }

    pub fn preanswer(&mut self, answers: &[(usize, char)]) {
        self.pending_answers = answers.to_vec();
    }

    pub fn is_loading(&self) -> bool {
        self.task.is_some()
    }

    /// Called by the app-level key handler for chapter-relative paging.
    pub fn scroll_by(&mut self, dy: f32) {
        let max = (self.content_h - self.view_h).max(0.0);
        let base = self.scroll_goal.unwrap_or(self.offset);
        self.scroll_goal = Some((base + dy).clamp(0.0, max));
    }

    fn score(&self, doc: &Doc) -> (usize, usize) {
        let correct = self.mcq.iter().filter(|(i, c)| doc.mcq_keys.get(**i) == Some(c)).count();
        (self.mcq.len(), correct)
    }
}

fn neighbors(env: &mut Env, c: &ChapterRef) -> (Option<ChapterRef>, Option<ChapterRef>) {
    let Some(idx) = env.study_index(&c.track, &c.subject) else { return (None, None) };
    let mk = |kind, no| Some(ChapterRef::new(&c.track, &c.subject, kind, no));
    match c.kind {
        ChapterKind::Unit => {
            let nos: Vec<u32> = idx.units.iter().map(|u| u.no).collect();
            let i = nos.iter().position(|n| *n == c.no);
            let prev = i.and_then(|i| i.checked_sub(1)).and_then(|i| nos.get(i)).and_then(|n| mk(ChapterKind::Unit, *n));
            let next = i.and_then(|i| nos.get(i + 1)).and_then(|n| mk(ChapterKind::Unit, *n));
            (prev, next)
        }
        ChapterKind::Bank => {
            let nos: Vec<u32> = idx.banks.iter().map(|b| b.no).collect();
            let i = nos.iter().position(|n| *n == c.no);
            let prev = i.and_then(|i| i.checked_sub(1)).and_then(|i| nos.get(i)).and_then(|n| mk(ChapterKind::Bank, *n));
            let next = i.and_then(|i| nos.get(i + 1)).and_then(|n| mk(ChapterKind::Bank, *n));
            (prev, next)
        }
        ChapterKind::Guide => (None, idx.units.first().and_then(|u| mk(ChapterKind::Unit, u.no))),
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut ReaderState, c: &ChapterRef) {
    let th = env.theme.clone();
    if st.current.as_ref() != Some(c) {
        st.start(env, c);
    }
    if let Some(t) = st.task.as_mut() {
        if let Some(res) = t.poll() {
            st.task = None;
            match res {
                Ok((meta, doc)) => {
                    let (sname, color) = env.subject(&c.track, &c.subject).map(|s| (s.name.clone(), s.color.clone())).unwrap_or_default();
                    env.store.push_recent(c, &meta.title, &sname, &color);
                    st.loaded = Some((meta, doc));
                    st.jump = st.pending_jump.take();
                    for (i, k) in std::mem::take(&mut st.pending_answers) {
                        st.mcq.insert(i, k);
                    }
                    if st.jump.is_some() {
                        st.restore = None;
                    }
                }
                Err(e) => st.error = Some(e.to_string()),
            }
        }
    }
    let (prev, next) = neighbors(env, c);
    handle_keys(ui, env, st, &prev, &next);

    let sub = env.subject(&c.track, &c.subject).cloned();
    let sname = sub.as_ref().map(|s| env.subject_name(s)).unwrap_or_default();
    let compact = env.layout == crate::ui::LayoutMode::Compact;
    let bookmarked = env.store.is_bookmarked(c);
    let done = env.store.progress(c).map(|p| p.done).unwrap_or(false);
    let title = st.loaded.as_ref().map(|(m, _)| m.title.clone()).unwrap_or_else(|| c.kind.label().to_string());
    let pad = if compact { 12.0 } else { 20.0 };

    // ---- top bar ----
    ui.add_space(8.0);
    let bar_w = ui.available_width() - pad * 2.0;
    ui.horizontal(|ui| {
        ui.add_space(pad);
        if widgets::icon_button(ui, &th, Icon::Back, "Back (Esc)", false).clicked() {
            env.act(Action::Back);
        }
        let ctrl_w = 38.0 * 5.0 + 4.0 * 6.0;
        ui.allocate_ui_with_layout(vec2((bar_w - ctrl_w - 52.0).max(80.0), 40.0), Layout::top_down(Align::Min), |ui| {
            ui.spacing_mut().item_spacing.y = 0.0;
            let sub_label = format!("{} · {}", sname, match c.kind {
                ChapterKind::Unit => format!("Unit {}", c.no),
                k => k.label().to_string(),
            });
            widgets::label_trunc(ui, RichText::new(sub_label).font(fonts::regular(12.5)).color(th.p.ink_muted));
            widgets::label_trunc(ui, RichText::new(&title).font(fonts::bold(16.5)).color(th.p.ink));
        });
        ui.allocate_ui_with_layout(vec2(ctrl_w, 40.0), Layout::left_to_right(Align::Center), |ui| {
            ui.spacing_mut().item_spacing.x = 6.0;
            let show_toc = env.store.s.prefs.show_toc;
            if widgets::icon_button(ui, &th, Icon::List, "Table of contents (T)", show_toc).clicked() {
                env.store.s.prefs.show_toc = !show_toc;
                env.store.touch();
            }
            if widgets::icon_button(ui, &th, Icon::Minus, "Smaller text", false).clicked() {
                env.store.s.prefs.font_scale = (env.store.s.prefs.font_scale - 0.05).clamp(0.8, 1.6);
                env.store.touch();
            }
            if widgets::icon_button(ui, &th, Icon::Plus, "Larger text", false).clicked() {
                env.store.s.prefs.font_scale = (env.store.s.prefs.font_scale + 0.05).clamp(0.8, 1.6);
                env.store.touch();
            }
            if widgets::icon_button(ui, &th, if bookmarked { Icon::BookmarkFilled } else { Icon::Bookmark }, if bookmarked { "Remove bookmark (Ctrl+B)" } else { "Bookmark (Ctrl+B)" }, bookmarked).clicked() {
                env.toggle_bookmark(c);
            }
            if widgets::icon_button(ui, &th, Icon::Check, if done { "Marked as read — click to undo" } else { "Mark as read" }, done).clicked() {
                env.store.set_done(c, !done);
            }
        });
    });
    // reading progress hairline
    let frac = if st.content_h > st.view_h + 1.0 { (st.offset / (st.content_h - st.view_h)).clamp(0.0, 1.0) } else { 0.0 };
    ui.add_space(6.0);
    ui.scope(|ui| {
        ui.spacing_mut().item_spacing.y = 0.0;
        widgets::progress_bar(ui, &th, frac, 3.0, None);
    });

    // ---- body ----
    if st.task.is_some() {
        ui.vertical_centered(|ui| {
            ui.add_space(120.0);
            ui.spinner();
            ui.add_space(10.0);
            widgets::muted(ui, &th, "Opening chapter…");
        });
        return;
    }
    if let Some(e) = st.error.clone() {
        widgets::empty_state(ui, &th, Icon::File, "Couldn't open this chapter", &e);
        ui.vertical_centered(|ui| {
            if widgets::button(ui, &th, "Back to subject", BtnKind::Primary, None, None).clicked() {
                env.go(Route::Subject { track: c.track.clone(), subject: c.subject.clone() });
            }
        });
        return;
    }
    let Some((meta, doc)) = st.loaded.take() else { return };

    let show_toc = env.store.s.prefs.show_toc && ui.available_width() > 880.0 && !meta.toc.is_empty();
    if show_toc {
        egui::SidePanel::right("reader_toc")
            .exact_width(272.0)
            .resizable(false)
            .frame(Frame::none().inner_margin(Margin { left: 8.0, right: 18.0, top: 14.0, bottom: 8.0 }))
            .show_inside(ui, |ui| toc_panel(ui, env, st, &meta, &doc));
    }

    egui::CentralPanel::default().frame(Frame::none()).show_inside(ui, |ui| {
        let mut sa = egui::ScrollArea::vertical().id_salt(("reader", c.key())).auto_shrink([false, false]);
        if let Some(y) = st.restore.take() {
            sa = sa.vertical_scroll_offset(y);
        } else if let Some(goal) = st.scroll_goal {
            let cur = st.offset;
            let mut n = cur + (goal - cur) * if env.motion() { 0.3 } else { 1.0 };
            if (goal - n).abs() < 1.0 {
                n = goal;
                st.scroll_goal = None;
            }
            ui.ctx().request_repaint();
            sa = sa.vertical_scroll_offset(n);
        }
        let scale = env.store.s.prefs.font_scale;
        let col_max = env.store.s.prefs.reading_width.px() * scale.sqrt();
        st.heads.clear();
        let out = sa.show(ui, |ui| {
            let avail = ui.available_width();
            let col_w = (avail - pad * 2.0).clamp(240.0, col_max);
            let side = ((avail - col_w) / 2.0).max(0.0);
            ui.horizontal_top(|ui| {
                ui.spacing_mut().item_spacing.x = 0.0;
                ui.add_space(side);
                ui.vertical(|ui| {
                    ui.set_width(col_w);
                    ui.spacing_mut().item_spacing.y = 8.0;
                    ui.add_space(18.0);
                    chapter_header(ui, env, st, &meta, c);
                    let mut cx = render::RenderCx {
                        th: &th,
                        scale,
                        content: Some(&env.repo),
                        jump: &mut st.jump,
                        heads: &mut st.heads,
                        mcq: &mut st.mcq,
                        mcq_idx: 0,
                        uid: 0,
                        actions: &mut env.actions,
                    };
                    render::blocks(ui, &mut cx, &doc.blocks);
                    ui.add_space(24.0);
                    footer(ui, env, c, done, &prev, &next);
                    ui.add_space(56.0);
                });
            });
        });
        if st.jump.is_some() {
            st.jump_age += 1;
            ui.ctx().request_repaint();
            if st.jump_age > 30 {
                st.jump = None;
                st.jump_age = 0;
            }
        }
        st.offset = out.state.offset.y;
        st.content_h = out.content_size.y;
        st.view_h = out.inner_rect.height();
        let top = out.inner_rect.top() + 90.0;
        st.current_head = st.heads.iter().filter(|(_, y)| *y <= top).last().map(|(id, _)| id.clone()).or_else(|| st.heads.first().map(|(id, _)| id.clone()));
        env.store.set_scroll(c, st.offset);
    });
    st.loaded = Some((meta, doc));
}

fn chapter_header(ui: &mut Ui, env: &mut Env, st: &mut ReaderState, meta: &ChMeta, c: &ChapterRef) {
    let th = env.theme.clone();
    crate::ui::widgets::flow(ui, |ui| {
        if !meta.area.is_empty() {
            widgets::badge(ui, &meta.area, th.p.accent, th.p.accent_soft);
        }
        widgets::badge(ui, &match c.kind {
            ChapterKind::Unit => format!("Unit {}", c.no),
            k => k.label().to_string(),
        }, th.p.ink_muted, th.p.field);
    });
    ui.add_space(4.0);
    ui.add(egui::Label::new(RichText::new(&meta.title).font(fonts::bold(32.0 * env.store.s.prefs.font_scale.sqrt())).color(th.p.ink)));
    ui.add(egui::Label::new(
        RichText::new(format!("{} min read  ·  {} words  ·  {} figures", meta.read_min, meta.words, meta.figures)).font(fonts::regular(13.0)).color(th.p.ink_muted),
    ));
    if let Some(ex) = &meta.exam {
        ui.add_space(8.0);
        widgets::panel_frame(&th).inner_margin(Margin::symmetric(16.0, 12.0)).show(ui, |ui| {
            ui.set_width(ui.available_width());
            crate::ui::widgets::flow(ui, |ui| {
                widgets::label(ui, RichText::new("Timed test").font(fonts::bold(14.5)).color(th.p.ink));
                widgets::label(ui, RichText::new(format!("{} minutes · −{} per wrong answer", ex.minutes, ex.negative)).font(fonts::regular(13.0)).color(th.p.ink_muted));
            });
            ui.add_space(6.0);
            ui.horizontal(|ui| match st.timer {
                None => {
                    if widgets::button(ui, &th, "Start the clock", BtnKind::Primary, Some(Icon::Clock), None).clicked() {
                        st.timer = Some(Instant::now());
                    }
                }
                Some(t0) => {
                    let total = Duration::from_secs(ex.minutes as u64 * 60);
                    let left = total.saturating_sub(t0.elapsed());
                    let secs = left.as_secs();
                    let txt = if secs == 0 { "Time is up".to_string() } else { format!("{:02}:{:02} remaining", secs / 60, secs % 60) };
                    widgets::label(ui, RichText::new(txt).font(fonts::bold(18.0)).color(if secs < 300 { th.p.danger } else { th.p.accent }));
                    if widgets::button(ui, &th, "Reset", BtnKind::Ghost, None, None).clicked() {
                        st.timer = None;
                    }
                    ui.ctx().request_repaint_after(Duration::from_millis(500));
                }
            });
        });
    }
    ui.add_space(6.0);
}

fn toc_panel(ui: &mut Ui, env: &mut Env, st: &mut ReaderState, meta: &ChMeta, doc: &Doc) {
    let th = env.theme.clone();
    egui::ScrollArea::vertical().id_salt("toc_scroll").auto_shrink([false, false]).show(ui, |ui| {
        widgets::label(ui, RichText::new("On this page").font(fonts::bold(13.0)).color(th.p.ink_muted));
        ui.add_space(8.0);
        for t in &meta.toc {
            let current = st.current_head.as_deref() == Some(t.id.as_str());
            let g = ui.painter().layout(t.title.clone(), if current { fonts::medium(13.5) } else { fonts::regular(13.5) }, if current { th.p.accent } else { th.p.ink_muted }, ui.available_width() - 20.0);
            let (rect, resp) = ui.allocate_exact_size(vec2(ui.available_width(), g.size().y + 12.0), Sense::click());
            if current {
                ui.painter().rect_filled(rect, 8.0, th.p.accent_soft);
            } else if resp.hovered() {
                ui.painter().rect_filled(rect, 8.0, th.p.field);
            }
            ui.painter().galley(egui::pos2(rect.min.x + 10.0, rect.min.y + 6.0), g, th.p.ink);
            if resp.hovered() {
                ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
            }
            if resp.clicked() {
                st.jump = Some(t.id.clone());
                st.jump_age = 0;
            }
        }
        if !doc.mcq_keys.is_empty() {
            ui.add_space(16.0);
            let (answered, correct) = st.score(doc);
            widgets::panel_frame(&th).inner_margin(Margin::symmetric(14.0, 12.0)).show(ui, |ui| {
                ui.set_width(ui.available_width());
                widgets::label(ui, RichText::new("Practice score").font(fonts::bold(13.0)).color(th.p.ink_muted));
                widgets::label(ui, RichText::new(format!("{correct} / {answered} correct")).font(fonts::bold(20.0)).color(th.p.ink));
                widgets::label(ui, RichText::new(format!("{} multiple-choice questions", doc.mcq_keys.len())).font(fonts::regular(12.0)).color(th.p.ink_faint));
                if answered > 0 {
                    ui.add_space(6.0);
                    if widgets::button(ui, &th, "Reset answers", BtnKind::Ghost, None, None).clicked() {
                        st.mcq.clear();
                    }
                }
            });
        }
    });
}

fn footer(ui: &mut Ui, env: &mut Env, c: &ChapterRef, done: bool, prev: &Option<ChapterRef>, next: &Option<ChapterRef>) {
    let th = env.theme.clone();
    widgets::hairline(ui, &th);
    ui.add_space(14.0);
    crate::ui::widgets::flow(ui, |ui| {
        if let Some(p) = prev {
            if widgets::button(ui, &th, "Previous", BtnKind::Secondary, Some(Icon::Back), None).clicked() {
                open_chapter(env, p.clone());
            }
        }
        let label = if done { "Marked as read" } else { "Mark as read" };
        if widgets::button(ui, &th, label, if done { BtnKind::Secondary } else { BtnKind::Primary }, Some(Icon::Check), None).clicked() {
            env.store.set_done(c, !done);
            if !done {
                env.toast("Chapter marked as read");
            }
        }
        if let Some(n) = next {
            if widgets::button(ui, &th, "Next chapter", BtnKind::Secondary, Some(Icon::Forward), None).clicked() {
                open_chapter(env, n.clone());
            }
        }
    });
}

fn handle_keys(ui: &mut Ui, env: &mut Env, st: &mut ReaderState, prev: &Option<ChapterRef>, next: &Option<ChapterRef>) {
    if ui.ctx().wants_keyboard_input() {
        return;
    }
    let page = (st.view_h * 0.88).max(200.0);
    let (space, shift, pgdn, pgup, home, end, down, up, lb, rb, t) = ui.input(|i| {
        (
            i.key_pressed(Key::Space),
            i.modifiers.shift,
            i.key_pressed(Key::PageDown),
            i.key_pressed(Key::PageUp),
            i.key_pressed(Key::Home),
            i.key_pressed(Key::End),
            i.key_pressed(Key::ArrowDown),
            i.key_pressed(Key::ArrowUp),
            i.key_pressed(Key::OpenBracket),
            i.key_pressed(Key::CloseBracket),
            i.key_pressed(Key::T) && !i.modifiers.command,
        )
    });
    if (space && !shift) || pgdn {
        st.scroll_by(page);
    }
    if (space && shift) || pgup {
        st.scroll_by(-page);
    }
    if down {
        st.scroll_by(70.0);
    }
    if up {
        st.scroll_by(-70.0);
    }
    if home {
        st.scroll_by(-1.0e6);
    }
    if end {
        st.scroll_by(1.0e6);
    }
    if lb {
        if let Some(p) = prev {
            open_chapter(env, p.clone());
        }
    }
    if rb {
        if let Some(n) = next {
            open_chapter(env, n.clone());
        }
    }
    if t {
        env.store.s.prefs.show_toc = !env.store.s.prefs.show_toc;
        env.store.touch();
    }
}
