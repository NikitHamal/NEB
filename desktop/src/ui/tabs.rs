//! M3 tab row: a tonal track with an indicator pill that slides between labels on the SPATIAL
//! spring. Collapses to icon-only when the row is too narrow.
use egui::{pos2, vec2, CursorIcon, Rect, Rounding, Sense, Ui};

use super::icons::{self, Icon};
use crate::theme::{fonts, mix, motion, Theme};

pub fn show(ui: &mut Ui, th: &Theme, tabs: &[(&str, Icon)], selected: &mut usize) -> bool {
    let avail = ui.available_width();
    let h = 52.0;
    let (track, _) = ui.allocate_exact_size(vec2(avail, h), Sense::hover());
    let n = tabs.len().max(1);
    let gap = 4.0;
    let w = (track.width() - gap * (n as f32 + 1.0)) / n as f32;
    let icon_only = w < 112.0;
    ui.painter().rect_filled(track, Rounding::same(h / 2.0), th.p.field);

    let id = ui.id().with("tabs");
    let x = motion::spring_to(ui.ctx(), id, *selected as f32, motion::SPATIAL);
    let ind = Rect::from_min_size(pos2(track.min.x + gap + x * (w + gap), track.min.y + gap), vec2(w, h - gap * 2.0));
    ui.painter().rect_filled(ind, Rounding::same((h - gap * 2.0) / 2.0), th.p.accent_soft);

    let mut changed = false;
    for (i, (label, icon)) in tabs.iter().enumerate() {
        let r = Rect::from_min_size(pos2(track.min.x + gap + i as f32 * (w + gap), track.min.y + gap), vec2(w, h - gap * 2.0));
        let resp = ui.interact(r, id.with(i), Sense::click());
        let hover = ui.ctx().animate_bool_with_time(id.with(("h", i)), resp.hovered() && *selected != i, 0.12);
        if hover > 0.0 {
            ui.painter().rect_filled(r, Rounding::same(r.height() / 2.0), th.p.ink.gamma_multiply(0.06 * hover));
        }
        let on = (1.0 - (x - i as f32).abs()).clamp(0.0, 1.0);
        let col = mix(th.p.ink_muted, th.p.on_accent_soft, on);
        if icon_only {
            icons::paint(ui.painter(), Rect::from_center_size(r.center(), vec2(22.0, 22.0)), *icon, col);
        } else {
            let galley = ui.painter().layout_no_wrap((*label).to_owned(), fonts::medium(14.5), col);
            let total = galley.size().x + 30.0;
            let sx = r.center().x - total / 2.0;
            icons::paint(ui.painter(), Rect::from_center_size(pos2(sx + 10.0, r.center().y), vec2(20.0, 20.0)), *icon, col);
            ui.painter().galley(pos2(sx + 30.0, r.center().y - galley.size().y / 2.0), galley, col);
        }
        if resp.hovered() {
            ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
        }
        if icon_only {
            resp.clone().on_hover_text(*label);
        }
        if resp.clicked() && *selected != i {
            *selected = i;
            changed = true;
        }
    }
    changed
}
