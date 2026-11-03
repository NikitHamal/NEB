//! In-app PDF viewer: continuous scroll, spring-smoothed zoom anchored on the viewport centre,
//! fit width / fit page, thumbnail rail, night reading, page jump, keyboard control and
//! per-book resume. Rendering happens on worker threads (`crate::pdf`), so scrolling never waits.
use std::path::{Path, PathBuf};

use egui::{pos2, vec2, Align, Color32, CursorIcon, Frame, Key, Layout, Margin, Rect, RichText, Rounding, ScrollArea, Sense, Stroke, Ui, UiBuilder, Vec2};

use crate::actions::Action;
use crate::env::Env;
use crate::pdf::{Key as Tile, PdfEngine};
use crate::theme::{fonts, motion, Theme};
use crate::ui::icons::Icon;
use crate::ui::shapes::{self, Kind};
use crate::ui::widgets;

const PAD: f32 = 24.0;
const GAP: f32 = 14.0;
const THUMBS_W: f32 = 168.0;

#[derive(Clone, Copy, PartialEq, Default)]
enum Mode {
    #[default]
    Width,
    Page,
    Custom,
}

enum Cmd {
    Zoom(f32),
    Fit(Mode),
    Goto(usize),
    Thumbs,
    Night,
}

#[derive(Default)]
pub struct PdfState {
    path: Option<PathBuf>,
    engine: Option<PdfEngine>,
    mode: Mode,
    z: f32,
    target_z: f32,
    night: Option<bool>,
    thumbs: bool,
    offset: Vec2,
    scroll_to: Option<f32>,
    force: Option<Vec2>,
    goto: Option<usize>,
    cur: usize,
    page_text: String,
    resume: Option<usize>,
    thumb_off: f32,
    thumb_force: Option<f32>,
    thumb_seen: usize,
}

impl PdfState {
    fn open(&mut self, ctx: &egui::Context, path: &Path, env: &Env) {
        *self = PdfState { path: Some(path.to_path_buf()), thumbs: true, ..Default::default() };
        self.resume = env.store.s.pdf_pos.get(&key_of(path)).copied();
        self.cur = self.resume.unwrap_or(0);
        self.engine = Some(PdfEngine::open(ctx, path.to_path_buf()));
    }
}

fn key_of(p: &Path) -> String {
    p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default()
}

fn title_of(p: &Path) -> String {
    let s = p.file_stem().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    s.trim_start_matches("NEBians-").replace(['-', '_'], " ")
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut PdfState, path: &Path) {
    let outer = ui.available_rect_before_wrap().shrink2(vec2(14.0, 10.0));
    ui.allocate_new_ui(UiBuilder::new().max_rect(outer), |ui| show_inner(ui, env, st, path));
}

fn show_inner(ui: &mut Ui, env: &mut Env, st: &mut PdfState, path: &Path) {
    let th = env.theme.clone();
    let ctx = ui.ctx().clone();
    if st.path.as_deref() != Some(path) {
        st.open(&ctx, path, env);
    }
    let night = st.night.unwrap_or(th.dark);
    if let Some(e) = st.engine.as_mut() {
        e.poll(&ctx);
    }
    let pages = st.engine.as_ref().map(|e| e.pages.len()).unwrap_or(0);
    let mut cmds: Vec<Cmd> = vec![];
    let page = ui.available_rect_before_wrap();
    let wide = page.width() > 900.0;
    toolbar(ui, env, &th, st, path, pages, night, wide, &mut cmds);
    apply(st, cmds, &ctx, night);
    ui.add_space(8.0);

    let area = ui.available_rect_before_wrap();
    let Some(mut eng) = st.engine.take() else { return };
    if let Some(err) = eng.error.clone() {
        ui.painter().rect_filled(area, Rounding::same(24.0), th.p.surface_low);
        ui.allocate_new_ui(UiBuilder::new().max_rect(area), |ui| {
            ui.add_space(area.height() * 0.28);
            widgets::empty_state(ui, &th, Icon::Error, "Can't open this book", &err);
        });
        st.engine = Some(eng);
        return;
    }
    if !eng.ready() {
        ui.painter().rect_filled(area, Rounding::same(24.0), th.p.surface_low);
        loader(ui, &th, area.center());
        st.engine = Some(eng);
        return;
    }

    handle_keys(&ctx, st, area.height(), night);
    let thumbs_t = motion::spring_bool(&ctx, ui.id().with("thumbs"), st.thumbs && wide, motion::SPATIAL).clamp(0.0, 1.05);
    let tw = THUMBS_W * thumbs_t;
    let gap = if tw > 4.0 { 10.0 } else { 0.0 };
    let (trect, vrect) = (Rect::from_min_size(area.min, vec2(tw, area.height())), Rect::from_min_max(pos2(area.min.x + tw + gap, area.min.y), area.max));

    let mut wants = reader(ui, &th, st, &mut eng, vrect, night);
    if tw > 40.0 {
        wants.extend(thumbs(ui, &th, st, &mut eng, trect, night));
    }
    eng.want(&wants);

    // resume position, persisted lazily
    if pages > 0 && st.cur < pages {
        let key = key_of(path);
        if env.store.s.pdf_pos.get(&key) != Some(&st.cur) {
            env.store.s.pdf_pos.insert(key, st.cur);
            env.store.touch();
        }
    }
    st.engine = Some(eng);
    ui.advance_cursor_after_rect(area);
}

#[allow(clippy::too_many_arguments)]
fn toolbar(ui: &mut Ui, env: &mut Env, th: &Theme, st: &mut PdfState, path: &Path, pages: usize, night: bool, wide: bool, cmds: &mut Vec<Cmd>) {
    Frame::none().fill(th.p.surface_high).rounding(Rounding::same(28.0)).inner_margin(Margin::symmetric(8.0, 6.0)).show(ui, |ui| {
        ui.set_width(ui.available_width());
        ui.horizontal(|ui| {
            ui.spacing_mut().item_spacing.x = 6.0;
            if widgets::icon_button(ui, th, Icon::Back, "Back", false).clicked() {
                env.act(Action::Back);
            }
            let controls_w = if wide { 560.0 } else { 300.0 };
            let tw = (ui.available_width() - controls_w).max(0.0);
            if tw > 60.0 {
                ui.allocate_ui_with_layout(vec2(tw, 40.0), Layout::left_to_right(Align::Center), |ui| {
                    widgets::label_trunc(ui, RichText::new(title_of(path)).font(fonts::medium(15.0)).color(th.p.ink));
                });
            }
            ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                ui.spacing_mut().item_spacing.x = 6.0;
                if widgets::icon_button(ui, th, Icon::Contrast, "Night reading  (N)", night).clicked() {
                    cmds.push(Cmd::Night);
                }
                if wide && widgets::icon_button(ui, th, Icon::List, "Thumbnails  (T)", st.thumbs).clicked() {
                    cmds.push(Cmd::Thumbs);
                }
                if wide {
                    if widgets::chip(ui, th, "Page", st.mode == Mode::Page).clicked() {
                        cmds.push(Cmd::Fit(Mode::Page));
                    }
                    if widgets::chip(ui, th, "Width", st.mode == Mode::Width).clicked() {
                        cmds.push(Cmd::Fit(Mode::Width));
                    }
                }
                if widgets::icon_button(ui, th, Icon::Plus, "Zoom in  (+)", false).clicked() {
                    cmds.push(Cmd::Zoom(1.25));
                }
                let pct = (st.z.max(0.01) / (96.0 / 72.0) * 100.0).round() as i32;
                widgets::label(ui, RichText::new(format!("{pct}%")).font(fonts::medium(13.5)).color(th.p.ink_muted));
                if widgets::icon_button(ui, th, Icon::Minus, "Zoom out  (-)", false).clicked() {
                    cmds.push(Cmd::Zoom(0.8));
                }
                ui.add_space(8.0);
                // page jump
                if pages > 0 {
                    if widgets::icon_button(ui, th, Icon::ChevronDown, "Next page  (Right)", false).clicked() {
                        cmds.push(Cmd::Goto((st.cur + 1).min(pages - 1)));
                    }
                    widgets::label(ui, RichText::new(format!("/ {pages}")).font(fonts::medium(13.5)).color(th.p.ink_muted));
                    let id = ui.id().with("page_box");
                    let editing = ui.ctx().memory(|m| m.has_focus(id));
                    if !editing {
                        st.page_text = (st.cur + 1).to_string();
                    }
                    let r = Frame::none().fill(th.p.field).rounding(Rounding::same(16.0)).inner_margin(Margin::symmetric(10.0, 6.0)).show(ui, |ui| {
                        ui.add(egui::TextEdit::singleline(&mut st.page_text).id(id).desired_width(40.0).horizontal_align(Align::Center).frame(false).font(fonts::medium(14.0)))
                    });
                    let te = r.inner;
                    if te.lost_focus() && ui.input(|i| i.key_pressed(Key::Enter)) {
                        if let Ok(n) = st.page_text.trim().parse::<usize>() {
                            cmds.push(Cmd::Goto(n.clamp(1, pages) - 1));
                        }
                    }
                    if widgets::icon_button(ui, th, Icon::ChevronUp, "Previous page  (Left)", false).clicked() {
                        cmds.push(Cmd::Goto(st.cur.saturating_sub(1)));
                    }
                }
            });
        });
    });
}

fn apply(st: &mut PdfState, cmds: Vec<Cmd>, ctx: &egui::Context, night: bool) {
    for c in cmds {
        match c {
            Cmd::Zoom(f) => {
                st.mode = Mode::Custom;
                st.target_z = (st.target_z * f).clamp(0.3, 6.0);
            }
            Cmd::Fit(m) => st.mode = m,
            Cmd::Goto(p) => st.goto = Some(p),
            Cmd::Thumbs => st.thumbs = !st.thumbs,
            Cmd::Night => st.night = Some(!night),
        }
    }
    ctx.request_repaint();
}

fn handle_keys(ctx: &egui::Context, st: &mut PdfState, vp_h: f32, night: bool) {
    if ctx.wants_keyboard_input() {
        return;
    }
    let (pgdn, pgup, home, end, left, right, up, down, plus, minus, w, p, t, n, space, shift) = ctx.input(|i| {
        (
            i.key_pressed(Key::PageDown),
            i.key_pressed(Key::PageUp),
            i.key_pressed(Key::Home),
            i.key_pressed(Key::End),
            i.key_pressed(Key::ArrowLeft) && !i.modifiers.alt,
            i.key_pressed(Key::ArrowRight) && !i.modifiers.alt,
            i.key_down(Key::ArrowUp),
            i.key_down(Key::ArrowDown),
            i.key_pressed(Key::Plus) || i.key_pressed(Key::Equals),
            i.key_pressed(Key::Minus),
            i.key_pressed(Key::W),
            i.key_pressed(Key::P),
            i.key_pressed(Key::T),
            i.key_pressed(Key::N),
            i.key_pressed(Key::Space),
            i.modifiers.shift,
        )
    });
    let base = st.scroll_to.unwrap_or(st.offset.y);
    if pgdn || (space && !shift) {
        st.scroll_to = Some(base + vp_h * 0.9);
    }
    if pgup || (space && shift) {
        st.scroll_to = Some((base - vp_h * 0.9).max(0.0));
    }
    if home {
        st.scroll_to = Some(0.0);
    }
    if end {
        st.scroll_to = Some(f32::MAX / 4.0);
    }
    if right {
        st.goto = Some(st.cur + 1);
    }
    if left {
        st.goto = Some(st.cur.saturating_sub(1));
    }
    if up || down {
        let dt = ctx.input(|i| i.stable_dt).min(0.05);
        let d = 900.0 * dt * if down { 1.0 } else { -1.0 };
        st.scroll_to = None;
        st.force = Some(vec2(st.offset.x, (st.offset.y + d).max(0.0)));
        ctx.request_repaint();
    }
    if plus {
        st.mode = Mode::Custom;
        st.target_z = (st.target_z * 1.25).clamp(0.3, 6.0);
    }
    if minus {
        st.mode = Mode::Custom;
        st.target_z = (st.target_z * 0.8).clamp(0.3, 6.0);
    }
    if w {
        st.mode = Mode::Width;
    }
    if p {
        st.mode = Mode::Page;
    }
    if t {
        st.thumbs = !st.thumbs;
    }
    if n {
        st.night = Some(!night);
    }
}

fn loader(ui: &mut Ui, th: &Theme, c: egui::Pos2) {
    let time = ui.input(|i| i.time) as f32;
    let t = 0.5 + 0.5 * (time * 2.4).sin();
    let r = Rect::from_center_size(c, vec2(64.0, 64.0));
    shapes::paint_morph(ui.painter(), r, Kind::Cookie, Kind::Flower, t, time * 0.9, th.p.accent);
    ui.ctx().request_repaint();
}

fn reader(ui: &mut Ui, th: &Theme, st: &mut PdfState, eng: &mut PdfEngine, rect: Rect, night: bool) -> Vec<Tile> {
    let ctx = ui.ctx().clone();
    let ppp = ctx.pixels_per_point();
    let n = eng.pages.len();
    let maxw = eng.pages.iter().map(|p| p.0).fold(1.0, f32::max);
    ui.painter().rect_filled(rect, Rounding::same(24.0), if night { th.p.surface_low } else { th.p.surface_highest });
    let inner = rect.shrink(8.0);

    // ---- zoom
    let fit_w = ((inner.width() - 2.0 * PAD) / maxw).clamp(0.2, 6.0);
    let cd = eng.pages[st.cur.min(n - 1)];
    let fit_p = ((inner.width() - 2.0 * PAD) / cd.0).min((inner.height() - 2.0 * PAD) / cd.1).clamp(0.2, 6.0);
    if st.z <= 0.0 {
        st.z = match st.mode {
            Mode::Page => fit_p,
            _ => fit_w,
        };
        st.target_z = st.z;
    }
    if ctx.input(|i| i.pointer.hover_pos()).is_some_and(|p| inner.contains(p)) {
        let zd = ctx.input(|i| i.zoom_delta());
        if (zd - 1.0).abs() > 1e-3 {
            st.mode = Mode::Custom;
            st.target_z = (st.z * zd).clamp(0.3, 6.0);
        }
    }
    let target = match st.mode {
        Mode::Width => fit_w,
        Mode::Page => fit_p,
        Mode::Custom => st.target_z,
    };
    st.target_z = target;
    let dt = ctx.input(|i| i.stable_dt).min(0.05);
    let z_new = if motion::reduced() || (st.z - target).abs() < 1e-3 { target } else { st.z + (target - st.z) * (1.0 - (-dt * 16.0).exp()) };

    let layout = |z: f32| -> (Vec<f32>, f32) {
        let mut tops = Vec::with_capacity(n);
        let mut y = PAD;
        for p in &eng.pages {
            tops.push(y);
            y += p.1 * z + GAP;
        }
        (tops, y - GAP + PAD)
    };
    let (tops_old, _) = layout(st.z);
    let (tops, total) = layout(z_new);
    let cw_old = (maxw * st.z + 2.0 * PAD).max(inner.width());
    let cw = (maxw * z_new + 2.0 * PAD).max(inner.width());
    if (z_new - st.z).abs() > 1e-6 {
        let cy = st.offset.y + inner.height() / 2.0;
        let i = tops_old.partition_point(|t| *t <= cy).saturating_sub(1).min(n - 1);
        let h_old = eng.pages[i].1 * st.z;
        let frac = ((cy - tops_old[i]) / h_old.max(1.0)).clamp(-0.2, 1.2);
        let y = tops[i] + frac * eng.pages[i].1 * z_new - inner.height() / 2.0;
        let cx = (st.offset.x + inner.width() / 2.0) / cw_old;
        st.force = Some(vec2((cx * cw - inner.width() / 2.0).max(0.0), y.max(0.0)));
        st.z = z_new;
    }
    let max_y = (total - inner.height()).max(0.0);
    if let Some(p) = st.resume.take() {
        let p = p.min(n - 1);
        st.force = Some(vec2(st.offset.x, (tops[p] - 10.0).clamp(0.0, max_y)));
        st.scroll_to = None;
    }
    if let Some(p) = st.goto.take() {
        st.scroll_to = Some(tops[p.min(n - 1)] - 10.0);
    }
    if let Some(t) = st.scroll_to {
        let t = t.clamp(0.0, max_y);
        let cur = st.offset.y;
        let next = if motion::reduced() { t } else { cur + (t - cur) * (1.0 - (-dt * 14.0).exp()) };
        if (t - next).abs() < 0.6 {
            st.scroll_to = None;
            st.force = Some(vec2(st.offset.x, t));
        } else {
            st.force = Some(vec2(st.offset.x, next));
            ctx.request_repaint();
        }
    }

    // ---- paint
    let mut sa = ScrollArea::both().id_salt("pdf_scroll").auto_shrink([false, false]);
    if let Some(f) = st.force.take() {
        sa = sa.scroll_offset(f);
    }
    let bg = if night { Color32::from_rgb(15, 22, 38) } else { Color32::WHITE };
    let mut visible: Vec<(usize, f32)> = vec![];
    let ppp_want = target * ppp;
    let out = ui
        .allocate_new_ui(UiBuilder::new().max_rect(inner), |ui| {
            sa.show_viewport(ui, |ui, vp| {
                let origin = ui.cursor().min;
                ui.allocate_exact_size(vec2(cw, total), Sense::hover());
                let snap = |v: f32| (v * ppp).round() / ppp;
                let centre = vp.center().y;
                for i in 0..n {
                    let (pw, ph) = (eng.pages[i].0 * z_new, eng.pages[i].1 * z_new);
                    let top = tops[i];
                    if top > vp.max.y + vp.height() || top + ph < vp.min.y - vp.height() {
                        continue;
                    }
                    visible.push((i, ((top + ph / 2.0) - centre).abs()));
                    if top > vp.max.y || top + ph < vp.min.y {
                        continue;
                    }
                    let r = Rect::from_min_size(pos2(snap(origin.x + (cw - pw) / 2.0), snap(origin.y + top)), vec2(snap(pw), snap(ph)));
                    ui.painter().rect_filled(r, 0.0, bg);
                    let exact = eng.exact(Tile::reading(i as u32, ppp_want, night));
                    let tex = exact.or_else(|| eng.best(i as u32, night));
                    match tex {
                        Some(id) => {
                            let a = if exact.is_some() { 1.0 } else { 0.97 };
                            ui.painter().image(id, r, Rect::from_min_max(pos2(0.0, 0.0), pos2(1.0, 1.0)), Color32::WHITE.gamma_multiply(a));
                        }
                        None if eng.has_failed(i as u32, night) => {
                            ui.painter().text(r.center(), egui::Align2::CENTER_CENTER, "This page can't be drawn", fonts::medium(14.0), th.p.ink_faint);
                        }
                        None => {
                            let time = ui.input(|i| i.time) as f32;
                            let pulse = 0.55 + 0.45 * (time * 3.0 + i as f32).sin();
                            ui.painter().rect_filled(r, 0.0, th.p.surface_high.gamma_multiply(pulse));
                            let m = Rect::from_center_size(r.center(), vec2(44.0, 44.0));
                            shapes::paint_morph(ui.painter(), m, Kind::Cookie, Kind::Flower, 0.5 + 0.5 * (time * 2.4).sin(), time, th.p.accent);
                            ui.ctx().request_repaint();
                        }
                    }
                    ui.painter().rect_stroke(r, 0.0, Stroke::new(1.0_f32, th.p.hairline));
                }
                vp
            })
        })
        .inner;
    st.offset = out.state.offset;
    let vp = out.inner;
    let centre = vp.center().y;
    st.cur = tops.partition_point(|t| *t <= centre + GAP).saturating_sub(1).min(n - 1);
    let _ = ui.interact(inner, ui.id().with("pdf_hand"), Sense::hover()).on_hover_cursor(CursorIcon::Grab);

    visible.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    let mut wants: Vec<Tile> = visible.iter().map(|(i, _)| Tile::reading(*i as u32, ppp_want, night)).collect();
    // prefetch one page each side of the visible band
    if let (Some(lo), Some(hi)) = (visible.iter().map(|v| v.0).min(), visible.iter().map(|v| v.0).max()) {
        if hi + 1 < n {
            wants.push(Tile::reading((hi + 1) as u32, ppp_want, night));
        }
        if lo > 0 {
            wants.push(Tile::reading((lo - 1) as u32, ppp_want, night));
        }
    }
    wants
}

fn thumbs(ui: &mut Ui, th: &Theme, st: &mut PdfState, eng: &mut PdfEngine, rect: Rect, night: bool) -> Vec<Tile> {
    ui.painter().rect_filled(rect, Rounding::same(24.0), th.p.surface_low);
    let inner = rect.shrink2(vec2(12.0, 10.0));
    let tw = inner.width();
    let n = eng.pages.len();
    let heights: Vec<f32> = eng.pages.iter().map(|p| tw * p.1 / p.0.max(1.0) + 30.0).collect();
    let item_h = |i: usize| heights[i];
    let mut tops = Vec::with_capacity(n);
    let mut y = 4.0;
    for i in 0..n {
        tops.push(y);
        y += item_h(i) + 4.0;
    }
    if st.thumb_seen != st.cur {
        st.thumb_seen = st.cur;
        let (lo, hi) = (st.thumb_off, st.thumb_off + inner.height());
        let (t, b) = (tops[st.cur], tops[st.cur] + item_h(st.cur));
        if t < lo || b > hi {
            st.thumb_force = Some((t - inner.height() / 2.0 + item_h(st.cur) / 2.0).max(0.0));
        }
    }
    let mut sa = ScrollArea::vertical().id_salt("pdf_thumbs").auto_shrink([false, false]);
    if let Some(f) = st.thumb_force.take() {
        sa = sa.vertical_scroll_offset(f);
    }
    let mut wants = vec![];
    let mut clicked = None;
    let out = ui
        .allocate_new_ui(UiBuilder::new().max_rect(inner), |ui| {
            sa.show_viewport(ui, |ui, vp| {
                let origin = ui.cursor().min;
                ui.allocate_exact_size(vec2(tw, y), Sense::hover());
                for i in 0..n {
                    let ih = item_h(i);
                    if tops[i] > vp.max.y || tops[i] + ih < vp.min.y {
                        continue;
                    }
                    let ph = ih - 30.0;
                    let r = Rect::from_min_size(pos2(origin.x, origin.y + tops[i]), vec2(tw, ph));
                    let cell = Rect::from_min_size(r.min, vec2(tw, ih));
                    let resp = ui.interact(cell, ui.id().with(("thumb", i)), Sense::click()).on_hover_cursor(CursorIcon::PointingHand);
                    let sel = i == st.cur;
                    let k = Tile::thumb(i as u32, night);
                    wants.push(k);
                    let hov = motion::spring_bool(ui.ctx(), resp.id.with("h"), resp.hovered(), motion::FAST);
                    let selv = motion::spring_bool(ui.ctx(), resp.id.with("s"), sel, motion::SPATIAL);
                    ui.painter().rect_filled(r, 0.0, if night { Color32::from_rgb(15, 22, 38) } else { Color32::WHITE });
                    let tex = eng.exact(k).or_else(|| eng.best(i as u32, night));
                    if let Some(id) = tex {
                        ui.painter().image(id, r, Rect::from_min_max(pos2(0.0, 0.0), pos2(1.0, 1.0)), Color32::WHITE);
                    }
                    let ring = r.expand(3.0 + 1.0 * selv);
                    let col = crate::theme::mix(th.p.hairline, th.p.accent, selv.clamp(0.0, 1.0));
                    ui.painter().rect_stroke(ring, Rounding::same(6.0), Stroke::new(1.0 + 1.5 * selv.max(hov * 0.5), if sel { th.p.accent } else { col }));
                    ui.painter().text(
                        pos2(r.center().x, r.max.y + 15.0),
                        egui::Align2::CENTER_CENTER,
                        (i + 1).to_string(),
                        if sel { fonts::bold(12.5) } else { fonts::medium(12.5) },
                        if sel { th.p.accent } else { th.p.ink_muted },
                    );
                    if resp.clicked() {
                        clicked = Some(i);
                    }
                }
            })
        })
        .inner;
    st.thumb_off = out.state.offset.y;
    if let Some(i) = clicked {
        st.goto = Some(i);
    }
    wants
}
