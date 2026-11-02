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
    /// Filled-tonal (secondaryContainer).
    Tonal,
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
    button_sized(ui, th, text, kind, icon, width, 48.0)
}

/// Material 3 Expressive button: pill at rest, state layers on hover/press, and the shape
/// morphs towards a squarer corner while pressed (the spring is approximated with a short ease).
pub fn button_sized(ui: &mut Ui, th: &Theme, text: &str, kind: BtnKind, icon: Option<Icon>, width: Option<f32>, h: f32) -> Response {
    let enabled = ui.is_enabled();
    let font = fonts::medium(if h >= 52.0 { 16.0 } else { 14.5 });
    let galley = ui.painter().layout_no_wrap(text.to_owned(), font, Color32::PLACEHOLDER);
    let icon_w = if icon.is_some() { 30.0 } else { 0.0 };
    let w = width.unwrap_or(galley.size().x + icon_w + 48.0);
    let (rect, resp) = ui.allocate_exact_size(vec2(w, h), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered() && enabled, 0.12);
    let press = ui.ctx().animate_bool_with_time(resp.id.with("press"), resp.is_pointer_button_down_on() && enabled, 0.09);
    let p = &th.p;
    let (bg, fg, border) = match kind {
        BtnKind::Primary => (p.accent, p.on_accent, Color32::TRANSPARENT),
        BtnKind::Tonal => (p.secondary_container, p.on_secondary_container, Color32::TRANSPARENT),
        BtnKind::Secondary => (Color32::TRANSPARENT, p.ink, p.hairline_strong),
        BtnKind::Ghost => (Color32::TRANSPARENT, p.accent, Color32::TRANSPARENT),
        BtnKind::Danger => (p.danger_soft, if th.dark { p.on_accent_soft } else { p.danger }, Color32::TRANSPARENT),
    };
    // state layer: fg at 8% (hover) / 12% (press) over the container
    let layer = fg.gamma_multiply(0.08 * hover + 0.06 * press);
    let radius = lerp(h / 2.0, spacing::PRESSED_RADIUS, press);
    let fade = if enabled { 1.0 } else { 0.38 };
    let r = rect;
    if bg != Color32::TRANSPARENT {
        ui.painter().rect_filled(r, Rounding::same(radius), bg.gamma_multiply(fade));
    }
    ui.painter().rect_filled(r, Rounding::same(radius), layer);
    if border != Color32::TRANSPARENT {
        ui.painter().rect_stroke(r, Rounding::same(radius), Stroke::new(1.0, border.gamma_multiply(fade)));
    }
    if resp.has_focus() {
        focus_ring(ui, th, r, radius);
    }
    let total = galley.size().x + icon_w;
    let mut x = r.center().x - total / 2.0;
    if let Some(ic) = icon {
        icons::paint(ui.painter(), Rect::from_center_size(egui::pos2(x + 10.0, r.center().y), vec2(20.0, 20.0)), ic, fg.gamma_multiply(fade));
        x += icon_w;
    }
    ui.painter().galley(egui::pos2(x, r.center().y - galley.size().y / 2.0), galley, fg.gamma_multiply(fade));
    if resp.hovered() && enabled {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

/// Square icon-only button (toolbar). `active` draws the soft accent background.
pub fn icon_button(ui: &mut Ui, th: &Theme, icon: Icon, tip: &str, active: bool) -> Response {
    icon_button_sized(ui, th, icon, tip, active, 44.0)
}

/// Round icon button with a state layer (48dp touch target on Android; 44 here).
pub fn icon_button_sized(ui: &mut Ui, th: &Theme, icon: Icon, tip: &str, active: bool, size: f32) -> Response {
    let enabled = ui.is_enabled();
    let (rect, resp) = ui.allocate_exact_size(vec2(size, size), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered() && enabled, 0.1);
    let press = ui.ctx().animate_bool_with_time(resp.id.with("press"), resp.is_pointer_button_down_on() && enabled, 0.08);
    let fg = if !enabled { th.p.ink_faint } else if active { th.p.on_accent_soft } else { th.p.ink };
    if active {
        ui.painter().rect_filled(rect, Rounding::same(size / 2.0), th.p.accent_soft);
    }
    ui.painter().rect_filled(rect, Rounding::same(lerp(size / 2.0, 12.0, press)), fg.gamma_multiply(0.08 * hover + 0.06 * press));
    if resp.has_focus() {
        focus_ring(ui, th, rect, size / 2.0);
    }
    icons::paint(ui.painter(), Rect::from_center_size(rect.center(), vec2(size * 0.52, size * 0.52)), icon, fg);
    if resp.hovered() && enabled {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp.on_hover_text(tip)
}

/// Selectable pill (onboarding options, filters).
pub fn chip(ui: &mut Ui, th: &Theme, text: &str, selected: bool) -> Response {
    let galley = ui.painter().layout_no_wrap(text.to_owned(), fonts::medium(14.0), Color32::PLACEHOLDER);
    let h = 38.0;
    let lead = if selected { 24.0 } else { 0.0 };
    let (rect, resp) = ui.allocate_exact_size(vec2(galley.size().x + 34.0 + lead, h), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered(), 0.1);
    let sel = ui.ctx().animate_bool_with_time(resp.id.with("sel"), selected, 0.14);
    let p = &th.p;
    let fill = p.secondary_container.gamma_multiply(sel);
    let fg = if selected { p.on_secondary_container } else { p.ink };
    let radius = h / 2.0;
    ui.painter().rect_filled(rect, Rounding::same(radius), fill);
    ui.painter().rect_filled(rect, Rounding::same(radius), fg.gamma_multiply(0.08 * hover));
    if !selected {
        ui.painter().rect_stroke(rect, Rounding::same(radius), Stroke::new(1.0, p.hairline_strong));
    }
    if resp.has_focus() {
        focus_ring(ui, th, rect, radius);
    }
    let mut x = rect.min.x + 17.0;
    if selected {
        icons::paint(ui.painter(), Rect::from_center_size(egui::pos2(x + 8.0, rect.center().y), vec2(18.0, 18.0)), Icon::Check, fg);
        x += lead;
    }
    ui.painter().galley(egui::pos2(x, rect.center().y - galley.size().y / 2.0), galley, fg);
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
        .inner_margin(egui::Margin::same(20.0))
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
        let (rect, _) = ui.allocate_exact_size(vec2(88.0, 88.0), Sense::hover());
        ui.painter().rect_filled(rect, Rounding::same(32.0), th.p.secondary_container);
        icons::paint(ui.painter(), Rect::from_center_size(rect.center(), vec2(38.0, 38.0)), icon, th.p.on_secondary_container);
        ui.add_space(18.0);
        heading(ui, th, title, 19.0);
        ui.add_space(4.0);
        ui.add(Label::new(RichText::new(subtitle).color(th.p.ink_muted)).selectable(false));
        ui.add_space(24.0);
    });
}

/// Single-line text field with a leading icon, styled like the Android search pill.
/// Single-line pill field with a leading icon and a visible placeholder (Android search / auth pill).
/// The background is painted *before* the editor, so typed text is always on top of it.
pub fn text_field(ui: &mut Ui, th: &Theme, text: &mut String, hint: &str, icon: Option<Icon>, width: f32, password: bool) -> Response {
    let h = 52.0;
    let (rect, _) = ui.allocate_exact_size(vec2(width, h), Sense::hover());
    let id = ui.make_persistent_id(("pill", hint, rect.min.x as i32, rect.min.y as i32));
    let edit_id = id.with("edit");
    let focused = ui.memory(|m| m.has_focus(edit_id));
    let hover = ui.rect_contains_pointer(rect);
    let bg = if focused { th.p.card } else { crate::theme::mix(th.p.field, th.p.ink, if hover { 0.04 } else { 0.0 }) };
    let border = if focused { th.p.accent } else { Color32::TRANSPARENT };
    ui.painter().rect(rect, Rounding::same(spacing::PILL), bg, Stroke::new(if focused { 2.0 } else { 1.0 }, border));
    if ui.interact(rect, id.with("bg"), Sense::click()).clicked() {
        ui.memory_mut(|m| m.request_focus(edit_id));
    }
    if let Some(ic) = icon {
        icons::paint(ui.painter(), Rect::from_center_size(egui::pos2(rect.min.x + 26.0, rect.center().y), vec2(22.0, 22.0)), ic, if focused { th.p.accent } else { th.p.ink_muted });
    }
    let left = if icon.is_some() { 50.0 } else { 20.0 };
    let edit_rect = Rect::from_min_max(egui::pos2(rect.min.x + left, rect.min.y + 6.0), egui::pos2(rect.max.x - 18.0, rect.max.y - 6.0));
    ui.put(
        edit_rect,
        egui::TextEdit::singleline(text)
            .id(edit_id)
            .hint_text(RichText::new(hint).color(th.p.ink_faint))
            .frame(false)
            .password(password)
            .text_color(th.p.ink)
            .vertical_align(Align::Center)
            .desired_width(edit_rect.width())
            .font(fonts::regular(15.5)),
    )
}

/// Material 3 text field with a floating label, optional leading icon, error state and — for
/// passwords — a show/hide toggle. Background first, then label, then the editor on top.
pub fn field(ui: &mut Ui, th: &Theme, text: &mut String, label: &str, icon: Option<Icon>, width: f32, password: bool, error: bool) -> Response {
    let h = 60.0;
    let (rect, _) = ui.allocate_exact_size(vec2(width, h), Sense::hover());
    let id = ui.make_persistent_id(("field", label, rect.min.y as i32));
    let edit_id = id.with("edit");
    let focused = ui.memory(|m| m.has_focus(edit_id));
    let up = ui.ctx().animate_bool_with_time(id.with("float"), focused || !text.is_empty(), 0.13);
    let show_pw = password && ui.data(|d| d.get_temp::<bool>(id.with("pw")).unwrap_or(false));
    let p = &th.p;
    let border = if error { p.danger } else if focused { p.accent } else { p.hairline_strong };
    let fill = if focused { p.card } else { p.field };
    // 1. background
    ui.painter().rect(rect, Rounding::same(18.0), fill, Stroke::new(if focused || error { 2.0 } else { 1.0 }, border));
    if ui.interact(rect, id.with("bg"), Sense::click()).clicked() {
        ui.memory_mut(|m| m.request_focus(edit_id));
    }
    // 2. icon + label
    let lx = if icon.is_some() { 54.0 } else { 18.0 };
    if let Some(ic) = icon {
        icons::paint(ui.painter(), Rect::from_center_size(egui::pos2(rect.min.x + 28.0, rect.center().y), vec2(22.0, 22.0)), ic, if focused { p.accent } else { p.ink_muted });
    }
    let label_col = if error { p.danger } else if focused { p.accent } else { p.ink_muted };
    let size = lerp(15.5, 11.5, up);
    let ly = lerp(rect.center().y, rect.min.y + 14.0, up);
    ui.painter().text(egui::pos2(rect.min.x + lx, ly), egui::Align2::LEFT_CENTER, label, fonts::medium(size), label_col);
    // 3. trailing show/hide
    let mut right_pad = 14.0;
    if password {
        right_pad = 50.0;
        let tr = Rect::from_center_size(egui::pos2(rect.max.x - 28.0, rect.center().y), vec2(36.0, 36.0));
        let r = ui.interact(tr, id.with("eye"), Sense::click());
        if r.hovered() {
            ui.painter().rect_filled(tr, Rounding::same(18.0), p.ink.gamma_multiply(0.08));
            ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
        }
        icons::paint(ui.painter(), Rect::from_center_size(tr.center(), vec2(20.0, 20.0)), if show_pw { Icon::EyeOff } else { Icon::Eye }, p.ink_muted);
        if r.on_hover_text(if show_pw { "Hide password" } else { "Show password" }).clicked() {
            ui.data_mut(|d| d.insert_temp(id.with("pw"), !show_pw));
        }
    }
    // 4. the editor, last so it is drawn above everything
    let edit_rect = Rect::from_min_max(egui::pos2(rect.min.x + lx, rect.min.y + 25.0), egui::pos2(rect.max.x - right_pad, rect.max.y - 6.0));
    ui.put(
        edit_rect,
        egui::TextEdit::singleline(text)
            .id(edit_id)
            .frame(false)
            .password(password && !show_pw)
            .text_color(p.ink)
            .desired_width(edit_rect.width())
            .vertical_align(Align::Center)
            .font(fonts::regular(15.5)),
    )
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

/// Outlined provider button ("Continue with Google") with the provider's SVG mark.
pub fn provider_button(ui: &mut Ui, th: &Theme, text: &str, uri: &'static str, svg: &'static [u8], width: f32) -> Response {
    let h = 56.0;
    let (rect, resp) = ui.allocate_exact_size(vec2(width, h), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("hover"), resp.hovered(), 0.12);
    let press = ui.ctx().animate_bool_with_time(resp.id.with("press"), resp.is_pointer_button_down_on(), 0.09);
    let radius = lerp(h / 2.0, spacing::PRESSED_RADIUS, press);
    ui.painter().rect_filled(rect, Rounding::same(radius), th.p.card);
    ui.painter().rect_filled(rect, Rounding::same(radius), th.p.ink.gamma_multiply(0.06 * hover + 0.06 * press));
    ui.painter().rect_stroke(rect, Rounding::same(radius), Stroke::new(1.0, th.p.hairline_strong));
    if resp.has_focus() {
        focus_ring(ui, th, rect, radius);
    }
    let galley = ui.painter().layout_no_wrap(text.to_owned(), fonts::medium(16.0), th.p.ink);
    let total = galley.size().x + 34.0;
    let x = rect.center().x - total / 2.0;
    let img = egui::Image::new(egui::ImageSource::Bytes { uri: uri.into(), bytes: egui::load::Bytes::Static(svg) });
    img.paint_at(ui, Rect::from_center_size(egui::pos2(x + 11.0, rect.center().y), vec2(22.0, 22.0)));
    ui.painter().galley(egui::pos2(x + 34.0, rect.center().y - galley.size().y / 2.0), galley, th.p.ink);
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp
}

/// "──── or ────" divider.
pub fn or_divider(ui: &mut Ui, th: &Theme, text: &str, width: f32) {
    let (rect, _) = ui.allocate_exact_size(vec2(width, 22.0), Sense::hover());
    let g = ui.painter().layout_no_wrap(text.to_owned(), fonts::regular(13.0), th.p.ink_faint);
    let gw = g.size().x;
    let y = rect.center().y;
    ui.painter().line_segment([egui::pos2(rect.min.x, y), egui::pos2(rect.center().x - gw / 2.0 - 12.0, y)], Stroke::new(1.0, th.p.hairline_strong));
    ui.painter().line_segment([egui::pos2(rect.center().x + gw / 2.0 + 12.0, y), egui::pos2(rect.max.x, y)], Stroke::new(1.0, th.p.hairline_strong));
    ui.painter().galley(egui::pos2(rect.center().x - gw / 2.0, y - g.size().y / 2.0), g, th.p.ink_faint);
}

/// A tonal icon tile (rounded square) — used for list rows, empty states, feature rows.
pub fn icon_tile(ui: &mut Ui, th: &Theme, icon: Icon, size: f32) {
    let (rect, _) = ui.allocate_exact_size(vec2(size, size), Sense::hover());
    ui.painter().rect_filled(rect, Rounding::same(size * 0.32), th.p.accent_soft);
    icons::paint(ui.painter(), Rect::from_center_size(rect.center(), vec2(size * 0.52, size * 0.52)), icon, th.p.on_accent_soft);
}

/// Multi-line editor with a visible text colour and the same M3 container as `field`.
pub fn text_area(ui: &mut Ui, th: &Theme, text: &mut String, hint: &str, width: f32, rows: usize) -> Response {
    let id = ui.make_persistent_id(("area", hint));
    let focused = ui.memory(|m| m.has_focus(id));
    let frame = egui::Frame::none()
        .fill(if focused { th.p.card } else { th.p.field })
        .stroke(Stroke::new(if focused { 2.0 } else { 1.0 }, if focused { th.p.accent } else { th.p.hairline_strong }))
        .rounding(Rounding::same(18.0))
        .inner_margin(egui::Margin::symmetric(16.0, 12.0));
    frame
        .show(ui, |ui| {
            ui.add(
                egui::TextEdit::multiline(text)
                    .id(id)
                    .frame(false)
                    .hint_text(RichText::new(hint).color(th.p.ink_faint))
                    .text_color(th.p.ink)
                    .desired_rows(rows)
                    .desired_width(width - 34.0)
                    .font(fonts::regular(15.5)),
            )
        })
        .inner
}

/// Wrapping row with room to breathe: chips and tags never touch, wrapped rows keep a real gap.
pub fn flow(ui: &mut Ui, add: impl FnOnce(&mut Ui)) {
    ui.horizontal_wrapped(|ui| {
        ui.spacing_mut().item_spacing = vec2(10.0, 12.0);
        add(ui);
    });
}
