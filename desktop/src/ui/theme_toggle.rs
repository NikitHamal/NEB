//! The theme button: one component for every screen, same look and motion as the website's
//! `.theme-btn` (44px, radius 22 -> 15 on hover -> 13 + scale .9 on press; the sun spins out as
//! the moon spins in on a spring).
use egui::{pos2, vec2, Color32, CursorIcon, Painter, Pos2, Rect, Response, Rounding, Sense, Shape, Stroke, Ui};

use crate::theme::{motion, Theme};

fn sun(p: &Painter, c: Pos2, rot: f32, scale: f32, alpha: f32, col: Color32) {
    if alpha <= 0.01 {
        return;
    }
    let col = col.gamma_multiply(alpha.clamp(0.0, 1.0));
    let st = Stroke::new(2.0, col);
    p.circle_stroke(c, 4.0 * scale, st);
    for i in 0..8 {
        let a = rot + i as f32 * std::f32::consts::FRAC_PI_4;
        let (s, co) = a.sin_cos();
        p.line_segment([c + vec2(co, s) * 7.2 * scale, c + vec2(co, s) * 9.6 * scale], st);
    }
}

fn moon(p: &Painter, c: Pos2, scale: f32, alpha: f32, col: Color32, cut: Color32) {
    if alpha <= 0.01 {
        return;
    }
    // crescent = disc with an offset disc cut out in the button colour
    p.circle_filled(c, 8.2 * scale, col.gamma_multiply(alpha.clamp(0.0, 1.0)));
    p.circle_filled(c + vec2(4.4, -3.8) * scale, 7.0 * scale, cut);
}

/// Draws the toggle at the cursor and flips `dark` via the returned response's `clicked()`.
pub fn show(ui: &mut Ui, th: &Theme) -> Response {
    let (rect, resp) = ui.allocate_exact_size(vec2(44.0, 44.0), Sense::click());
    paint(ui, th, rect, &resp);
    resp.on_hover_cursor(CursorIcon::PointingHand)
}

pub fn paint(ui: &Ui, th: &Theme, rect: Rect, resp: &Response) {
    let ctx = ui.ctx();
    let hover = motion::spring_bool(ctx, resp.id.with("h"), resp.hovered(), motion::FAST);
    let press = motion::spring_bool(ctx, resp.id.with("p"), resp.is_pointer_button_down_on(), motion::FAST);
    let mode = motion::spring_bool(ctx, resp.id.with("m"), th.dark, motion::SLOW);
    let radius = (22.0 - 7.0 * hover - 2.0 * press).max(12.0);
    let r = Rect::from_center_size(rect.center(), rect.size() * (1.0 - 0.1 * press));
    let bg = crate::theme::mix(th.p.surface_high, th.p.surface_highest, hover);
    ui.painter().rect_filled(r, Rounding::same(radius), bg);
    if resp.has_focus() {
        ui.painter().rect_stroke(r.expand(2.5), Rounding::same(radius + 2.5), Stroke::new(2.0, th.p.accent));
    }
    let c = r.center();
    let tau = std::f32::consts::TAU;
    // sun: fully visible at mode 0, spins out to +90deg; moon: rotates in from -90deg
    sun(ui.painter(), c, mode * tau * 0.25, 1.0 - 0.6 * mode.clamp(0.0, 1.0), 1.0 - mode.clamp(0.0, 1.0) * 1.4, th.p.ink);
    moon(ui.painter(), c + vec2(-1.0, 1.0), 0.4 + 0.6 * mode.clamp(0.0, 1.0), (mode * 1.4 - 0.4).clamp(0.0, 1.0), th.p.ink, bg);
    let _ = pos2(0.0, 0.0);
}
