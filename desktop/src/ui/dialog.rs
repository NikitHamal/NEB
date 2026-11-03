//! M3 Expressive dialog: the scrim fades in, the panel rises on the same ease as every other
//! entrance. Tone + outline separate it from the page (no shadows). One implementation serves
//! confirmations, forms and the in-app legal sheet.
use egui::{Align, Align2, Area, Color32, Context, Frame, Id, Key, Layout, Margin, Order, RichText, Rounding, Sense, Stroke, Ui};

use super::widgets::{self, BtnKind};
use crate::theme::{fonts, motion, spacing, Theme};

fn flag_id() -> Id {
    Id::new("neb-modal-open")
}

/// True when a dialog was drawn this frame or the last one (the app uses it to keep Esc local).
pub fn is_open(ctx: &Context) -> bool {
    let n = ctx.data(|d| d.get_temp::<u64>(flag_id()).unwrap_or(0));
    let now = ctx.cumulative_pass_nr();
    n + 2 >= now
}

/// Draw a modal dialog. Returns `true` when the user dismissed it (scrim click or Esc).
pub fn show(ctx: &Context, th: &Theme, key: &str, width: f32, add: impl FnOnce(&mut Ui)) -> bool {
    let id = Id::new(("dialog", key));
    let pass = ctx.cumulative_pass_nr();
    ctx.data_mut(|d| d.insert_temp(flag_id(), pass));
    let t = motion::enter(ctx, id.with("t"), 0.0, 0.32);
    let screen = ctx.screen_rect();
    let mut dismissed = ctx.input(|i| i.key_pressed(Key::Escape));

    Area::new(id.with("scrim")).order(Order::Foreground).fixed_pos(screen.min).show(ctx, |ui| {
        let (rect, resp) = ui.allocate_exact_size(screen.size(), Sense::click());
        ui.painter().rect_filled(rect, 0.0, Color32::from_black_alpha(((if th.dark { 170.0 } else { 120.0 }) * t) as u8));
        if resp.clicked() {
            dismissed = true;
        }
    });

    let w = width.min(screen.width() - 32.0).max(260.0);
    Area::new(id.with("panel")).order(Order::Tooltip).anchor(Align2::CENTER_CENTER, [0.0, (1.0 - t) * 28.0]).show(ctx, |ui| {
        ui.set_opacity(t);
        Frame::none()
            .fill(th.p.surface_high)
            .stroke(Stroke::new(1.0_f32, th.p.hairline))
            .rounding(Rounding::same(spacing::PANEL_RADIUS))
            .inner_margin(Margin::same(26.0))
            .show(ui, |ui| {
                ui.set_width(w - 52.0);
                ui.spacing_mut().item_spacing.y = 10.0;
                add(ui);
            });
    });
    dismissed
}

pub fn title(ui: &mut Ui, th: &Theme, text: &str) {
    widgets::label(ui, RichText::new(text).font(fonts::bold(21.0)).color(th.p.ink));
}

pub fn body(ui: &mut Ui, th: &Theme, text: &str) {
    ui.add(egui::Label::new(RichText::new(text).font(fonts::regular(14.5)).color(th.p.ink_muted)));
}

/// Right-aligned action row. Put the primary action first in call order (it sits rightmost).
pub fn actions(ui: &mut Ui, add: impl FnOnce(&mut Ui)) {
    ui.add_space(8.0);
    ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
        ui.spacing_mut().item_spacing.x = 10.0;
        add(ui);
    });
}

/// Confirm / cancel pair. Returns `Some(true)` on confirm, `Some(false)` on cancel.
pub fn confirm_row(ui: &mut Ui, th: &Theme, confirm: &str, kind: BtnKind, enabled: bool) -> Option<bool> {
    let mut out = None;
    actions(ui, |ui| {
        ui.add_enabled_ui(enabled, |ui| {
            if widgets::button(ui, th, confirm, kind, None, None).clicked() {
                out = Some(true);
            }
        });
        if widgets::button(ui, th, "Cancel", BtnKind::Ghost, None, None).clicked() {
            out = Some(false);
        }
    });
    out
}

/// Inline error line for dialogs and forms.
pub fn error_line(ui: &mut Ui, th: &Theme, msg: &str) {
    ui.add(egui::Label::new(RichText::new(msg).font(fonts::medium(13.5)).color(th.p.danger)));
}
