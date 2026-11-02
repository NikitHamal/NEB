//! The house widgets: pill buttons, chips, cards, toggles, segmented control,
//! progress bars, subject badges, section headers, empty states.
//! Every interactive widget has a hover animation, a pointer cursor and a focus ring.
use egui::{
    vec2, Align, Color32, CursorIcon, FontId, Label, Layout, Rect, Response, RichText, Rounding, Sense, Stroke, Ui, UiBuilder, Vec2,
};

use super::icons::{self, Icon};
use crate::theme::{fonts, spacing, Theme};

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum BtnKind {
    Primary,
    Secondary,
    Ghost,
    Danger,
}

fn focus_ring(ui: &Ui, th: &Theme, rect: Rect, rounding: f32) {
    ui.painter().rect_stroke(rect.expand(2.5), Rounding::same(rounding + 2.5), Stroke::new(2.0, th.p.accent));
}

/// Non-selectable label (safe to put inside clickable cards).
pub fn label(ui: &mut Ui, text: RichText) -> Response {
    ui.add(Label::new(text).selectable(false))
}

pub fn label_trunc(ui: &mut Ui, text: RichText) -> Response {
    ui.add(Label::new(text).selectable(false).truncate())
}

pub fn heading(ui: &mut Ui, th: &Theme, text: &str, size: f32) -> Response {
    label(ui, RichText::new(text).font(fonts::bold(size)).color(th.p.ink))
}

pub fn muted(ui: &mut Ui, th: &Theme, text: &str) -> Response {
    ui.add(Label::new(RichText::new(text).color(th.p.ink_muted)))
}

/// Pill button. `width = None` hugs the label; `Some(w)` forces a width.
pub fn button(ui: &mut Ui, th: &Theme, text: &str, kind: BtnKind, icon: Option<Icon>, width: Option<f32>) -> Response {
    let enabled = ui.is_enabled();
    let font = fonts::medium(14.5);
    let galley = ui.painter().layout_no_wrap(text.to_owned(), font, Color32::PLACEHOLDER);
    let icon_w = if icon.is_some() { 26.0 } else { 0.0 };
    let w = width.unwrap_or(galley.size().x + icon_w + 40.0);
    let h = 42.0;
    let (rect, resp) = ui.allocate_exact_size(vec2(w, h), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered() && enabled, 0.12);
    let (bg, fg, border) = match kind {
        BtnKind::Primary => (th.p.accent, th.p.on_accent, th.p.accent),
        BtnKind::Secondary => (th.p.card, th.p.ink, th.p.hairline_strong),
        BtnKind::Ghost => (Color32::TRANSPARENT, th.p.ink, Color32::TRANSPARENT),
        BtnKind::Danger => (th.p.danger_soft, th.p.danger, th.p.danger_soft),
    };
    let hover_bg = match kind {
        BtnKind::Primary => crate::theme::mix(bg, if th.dark { Color32::WHITE } else { Color32::BLACK }, 0.12),
        BtnKind::Danger => crate::theme::mix(bg, th.p.danger, 0.12),
        _ => th.p.field,
    };
    let fill = crate::theme::mix(bg, hover_bg, hover);
    let fill = if bg == Color32::TRANSPARENT && hover < 0.01 { Color32::TRANSPARENT } else { fill };
    let mut r = rect;
    if resp.is_pointer_button_down_on() {
        r = r.shrink(1.5);
    }
    let fade = if enabled { 1.0 } else { 0.45 };
    ui.painter().rect(r, Rounding::same(spacing::PILL), fill.gamma_multiply(fade), Stroke::new(1.0, border.gamma_multiply(fade)));
    if resp.has_focus() {
        focus_ring(ui, th, r, h / 2.0);
    }
    let total = galley.size().x + icon_w;
    let mut x = r.center().x - total / 2.0;
    if let Some(ic) = icon {
        icons::paint(ui.painter(), Rect::from_center_size(egui::pos2(x + 9.0, r.center().y), vec2(18.0, 18.0)), ic, fg.gamma_multiply(fade));
        x += icon_w;
    }
    ui.painter().galley(egui::pos2(x, r.center().y - galley.size().y / 2.0), galley, fg.gamma_multiply(fade));
    if resp.hovered() && enabled {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp
}

/// Square icon-only button (toolbar). `active` draws the soft accent background.
pub fn icon_button(ui: &mut Ui, th: &Theme, icon: Icon, tip: &str, active: bool) -> Response {
    let enabled = ui.is_enabled();
    let (rect, resp) = ui.allocate_exact_size(vec2(38.0, 38.0), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered() && enabled, 0.1);
    let bg = if active { th.p.accent_soft } else { crate::theme::mix(Color32::TRANSPARENT, th.p.field, hover) };
    let bg = if active || hover > 0.01 { if active { bg } else { th.p.field.gamma_multiply(hover) } } else { Color32::TRANSPARENT };
    ui.painter().rect_filled(rect, Rounding::same(11.0), bg);
    if resp.has_focus() {
        focus_ring(ui, th, rect, 11.0);
    }
    let col = if !enabled {
        th.p.ink_faint
    } else if active {
        th.p.accent
    } else {
        th.p.ink
    };
    icons::paint(ui.painter(), Rect::from_center_size(rect.center(), vec2(20.0, 20.0)), icon, col);
    if resp.hovered() && enabled {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp.on_hover_text(tip)
}

/// Selectable pill (onboarding options, filters).
pub fn chip(ui: &mut Ui, th: &Theme, text: &str, selected: bool) -> Response {
    let galley = ui.painter().layout_no_wrap(text.to_owned(), fonts::medium(14.0), Color32::PLACEHOLDER);
    let h = 36.0;
    let (rect, resp) = ui.allocate_exact_size(vec2(galley.size().x + 32.0, h), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered(), 0.1);
    let (fill, fg, border) = if selected {
        (th.p.accent, th.p.on_accent, th.p.accent)
    } else {
        (crate::theme::mix(th.p.card, th.p.field, hover), th.p.ink, th.p.hairline_strong)
    };
    ui.painter().rect(rect, Rounding::same(spacing::PILL), fill, Stroke::new(1.0, border));
    if resp.has_focus() {
        focus_ring(ui, th, rect, h / 2.0);
    }
    ui.painter().galley(egui::pos2(rect.center().x - galley.size().x / 2.0, rect.center().y - galley.size().y / 2.0), galley, fg);
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp
}

/// Small non-interactive tag.
pub fn badge(ui: &mut Ui, text: &str, fg: Color32, bg: Color32) {
    let galley = ui.painter().layout_no_wrap(text.to_owned(), fonts::medium(11.5), Color32::PLACEHOLDER);
    let (rect, _) = ui.allocate_exact_size(vec2(galley.size().x + 16.0, 22.0), Sense::hover());
    ui.painter().rect_filled(rect, Rounding::same(spacing::PILL), bg);
    ui.painter().galley(egui::pos2(rect.min.x + 8.0, rect.center().y - galley.size().y / 2.0), galley, fg);
}

/// Clickable card with a fixed size. Contents are laid out inside; the whole
/// surface reacts to hover and keyboard focus.
pub fn card(ui: &mut Ui, th: &Theme, size: Vec2, pad: f32, contents: impl FnOnce(&mut Ui)) -> Response {
    let (rect, resp) = ui.allocate_exact_size(size, Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered(), 0.12);
    let fill = crate::theme::mix(th.p.card, th.p.field, hover * 0.8);
    let border = crate::theme::mix(th.p.hairline, th.p.hairline_strong, hover);
    ui.painter().rect(rect, Rounding::same(spacing::CARD_RADIUS), fill, Stroke::new(1.0, border));
    if resp.has_focus() {
        focus_ring(ui, th, rect, spacing::CARD_RADIUS);
    }
    let inner = rect.shrink(pad);
    let mut child = ui.new_child(UiBuilder::new().max_rect(inner).layout(Layout::top_down(Align::Min)));
    child.set_clip_rect(inner.expand(2.0).intersect(ui.clip_rect()));
    contents(&mut child);
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp
}

/// A non-interactive surface (settings groups, info panels).
pub fn panel_frame(th: &Theme) -> egui::Frame {
    egui::Frame::none()
        .fill(th.p.card)
        .stroke(Stroke::new(1.0, th.p.hairline))
        .rounding(Rounding::same(spacing::CARD_RADIUS))
        .inner_margin(egui::Margin::same(18.0))
}

/// Lay `count` equal-width cards into as many columns as fit.
pub fn grid(ui: &mut Ui, min_w: f32, gap: f32, count: usize, mut cell: impl FnMut(&mut Ui, usize, f32)) {
    let avail = ui.available_width();
    let cols = (((avail + gap) / (min_w + gap)).floor() as usize).max(1);
    let w = (avail - gap * (cols as f32 - 1.0)) / cols as f32;
    let mut i = 0;
    while i < count {
        ui.horizontal_top(|ui| {
            ui.spacing_mut().item_spacing.x = gap;
            for _ in 0..cols {
                if i < count {
                    cell(ui, i, w);
                    i += 1;
                }
            }
        });
        if i < count {
            ui.add_space(gap);
        }
    }
}

/// "Section title ········ See all" row. Returns true when the action was clicked.
pub fn section_header(ui: &mut Ui, th: &Theme, title: &str, action: Option<&str>) -> bool {
    let mut clicked = false;
    ui.horizontal(|ui| {
        heading(ui, th, title, 19.0);
        if let Some(a) = action {
            ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                let g = ui.painter().layout_no_wrap(a.to_owned(), fonts::medium(13.5), th.p.accent);
                let (rect, resp) = ui.allocate_exact_size(vec2(g.size().x + 8.0, 26.0), Sense::click());
                let col = if resp.hovered() { th.p.ink } else { th.p.accent };
                ui.painter().galley(egui::pos2(rect.min.x + 4.0, rect.center().y - g.size().y / 2.0), g, col);
                if resp.hovered() {
                    ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
                }
                clicked = resp.clicked();
            });
        }
    });
    ui.add_space(10.0);
    clicked
}

/// Rounded-square monogram used for subjects (the web/Android tiles use an icon
/// on a tinted tile; we use the subject's data colour + its initial).
pub fn subject_badge(ui: &mut Ui, th: &Theme, name: &str, color_hex: &str, size: f32) {
    let c = th.subject_color(color_hex);
    let (rect, _) = ui.allocate_exact_size(vec2(size, size), Sense::hover());
    ui.painter().rect_filled(rect, Rounding::same(size * 0.28), th.wash(c));
    let letter: String = crate::util::initials(name).chars().take(1).collect();
    ui.painter().text(rect.center(), egui::Align2::CENTER_CENTER, letter, fonts::bold(size * 0.46), c);
}

pub fn progress_bar(ui: &mut Ui, th: &Theme, frac: f32, height: f32, color: Option<Color32>) {
    let w = ui.available_width();
    let (rect, _) = ui.allocate_exact_size(vec2(w, height), Sense::hover());
    ui.painter().rect_filled(rect, Rounding::same(height / 2.0), th.p.hairline);
    let f = frac.clamp(0.0, 1.0);
    if f > 0.0 {
        let mut r = rect;
        r.set_width((rect.width() * f).max(height));
        ui.painter().rect_filled(r, Rounding::same(height / 2.0), color.unwrap_or(th.p.accent));
    }
}

/// Animated switch. Returns the response; flips `on` when clicked.
pub fn toggle(ui: &mut Ui, th: &Theme, on: &mut bool) -> Response {
    let (rect, mut resp) = ui.allocate_exact_size(vec2(46.0, 26.0), Sense::click());
    if resp.clicked() {
        *on = !*on;
        resp.mark_changed();
    }
    let t = ui.ctx().animate_bool_with_time(resp.id.with("on"), *on, 0.14);
    let track = crate::theme::mix(th.p.hairline_strong, th.p.accent, t);
    ui.painter().rect_filled(rect, Rounding::same(13.0), track);
    if resp.has_focus() {
        focus_ring(ui, th, rect, 13.0);
    }
    let knob_x = rect.min.x + 13.0 + t * 20.0;
    let knob = crate::theme::mix(Color32::WHITE, th.p.on_accent, 0.0);
    ui.painter().circle_filled(egui::pos2(knob_x, rect.center().y), 10.0, if *on && th.dark { th.p.on_accent } else { knob });
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp
}

/// Segmented control (Light / Dark / System). Returns true if the selection changed.
pub fn segmented(ui: &mut Ui, th: &Theme, options: &[&str], selected: &mut usize) -> bool {
    let mut changed = false;
    ui.horizontal(|ui| {
        ui.spacing_mut().item_spacing.x = 6.0;
        for (i, o) in options.iter().enumerate() {
            if chip(ui, th, o, *selected == i).clicked() {
                *selected = i;
                changed = true;
            }
        }
    });
    changed
}

/// Settings-style row: title + optional subtitle on the left, `right` content on the right.
pub fn setting_row(ui: &mut Ui, th: &Theme, title: &str, subtitle: Option<&str>, right: impl FnOnce(&mut Ui)) {
    ui.horizontal(|ui| {
        ui.vertical(|ui| {
            label(ui, RichText::new(title).font(fonts::medium(15.0)).color(th.p.ink));
            if let Some(s) = subtitle {
                label(ui, RichText::new(s).font(FontId::proportional(12.8)).color(th.p.ink_muted));
            }
        });
        ui.with_layout(Layout::right_to_left(Align::Center), right);
    });
}

pub fn hairline(ui: &mut Ui, th: &Theme) {
    let (rect, _) = ui.allocate_exact_size(vec2(ui.available_width(), 1.0), Sense::hover());
    ui.painter().rect_filled(rect, 0.0, th.p.hairline);
}

/// A single static icon + a line of text — the Android empty-state contract.
pub fn empty_state(ui: &mut Ui, th: &Theme, icon: Icon, title: &str, subtitle: &str) {
    ui.vertical_centered(|ui| {
        ui.add_space(48.0);
        let (rect, _) = ui.allocate_exact_size(vec2(64.0, 64.0), Sense::hover());
        ui.painter().circle_filled(rect.center(), 32.0, th.p.field);
        icons::paint(ui.painter(), Rect::from_center_size(rect.center(), vec2(28.0, 28.0)), icon, th.p.ink_muted);
        ui.add_space(14.0);
        heading(ui, th, title, 17.0);
        ui.add_space(2.0);
        ui.add(Label::new(RichText::new(subtitle).color(th.p.ink_muted)).selectable(false));
        ui.add_space(24.0);
    });
}

/// Single-line text field with a leading icon, styled like the Android search pill.
pub fn text_field(ui: &mut Ui, th: &Theme, text: &mut String, hint: &str, icon: Option<Icon>, width: f32, password: bool) -> Response {
    let h = 46.0;
    let (rect, _) = ui.allocate_exact_size(vec2(width, h), Sense::hover());
    let inner_left = if icon.is_some() { 42.0 } else { 16.0 };
    let edit_rect = Rect::from_min_max(egui::pos2(rect.min.x + inner_left, rect.min.y + 4.0), egui::pos2(rect.max.x - 12.0, rect.max.y - 4.0));
    let mut child = ui.new_child(UiBuilder::new().max_rect(edit_rect).layout(Layout::left_to_right(Align::Center)));
    let resp = child.add_sized(
        edit_rect.size(),
        egui::TextEdit::singleline(text)
            .hint_text(RichText::new(hint).color(th.p.ink_faint))
            .frame(false)
            .password(password)
            .font(fonts::regular(15.5)),
    );
    let focused = resp.has_focus();
    let border = if focused { th.p.accent } else { th.p.hairline_strong };
    ui.painter().rect(rect, Rounding::same(spacing::PILL), th.p.field, Stroke::new(if focused { 2.0 } else { 1.0 }, border));
    if let Some(ic) = icon {
        icons::paint(ui.painter(), Rect::from_center_size(egui::pos2(rect.min.x + 22.0, rect.center().y), vec2(18.0, 18.0)), ic, th.p.ink_muted);
    }
    resp
}

/// Back-arrow + two-line title, the "house screen" header used by Android screens.
pub fn screen_header(ui: &mut Ui, th: &Theme, title: &str, subtitle: Option<&str>) {
    ui.vertical(|ui| {
        heading(ui, th, title, 26.0);
        if let Some(s) = subtitle {
            ui.add(Label::new(RichText::new(s).color(th.p.ink_muted)));
        }
    });
    ui.add_space(18.0);
}
