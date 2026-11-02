//! Transient bottom-centre messages ("Bookmarked", "Saved a copy …").
use std::time::{Duration, Instant};

use egui::{Align2, Area, Context, Frame, Id, Margin, RichText, Rounding};

use crate::theme::{fonts, Theme};

#[derive(Default)]
pub struct Toasts {
    items: Vec<(String, Instant)>,
}

impl Toasts {
    pub fn push(&mut self, msg: impl Into<String>) {
        self.items.push((msg.into(), Instant::now()));
    }

    pub fn show(&mut self, ctx: &Context, th: &Theme, bottom_offset: f32) {
        self.items.retain(|(_, t)| t.elapsed() < Duration::from_millis(2600));
        if self.items.is_empty() {
            return;
        }
        ctx.request_repaint_after(Duration::from_millis(120));
        for (i, (msg, t)) in self.items.iter().enumerate() {
            let age = t.elapsed().as_secs_f32();
            let alpha = ((2.6 - age) / 0.3).clamp(0.0, 1.0).min((age / 0.12).clamp(0.0, 1.0));
            Area::new(Id::new(("toast", i)))
                .anchor(Align2::CENTER_BOTTOM, egui::vec2(0.0, -(bottom_offset + 18.0 + i as f32 * 48.0)))
                .interactable(false)
                .order(egui::Order::Tooltip)
                .show(ctx, |ui| {
                    ui.set_opacity(alpha);
                    Frame::none()
                        .fill(th.p.ink)
                        .rounding(Rounding::same(999.0))
                        .inner_margin(Margin::symmetric(18.0, 10.0))
                        .show(ui, |ui| {
                            ui.add(egui::Label::new(RichText::new(msg).font(fonts::medium(14.0)).color(th.p.page)).selectable(false));
                        });
                });
        }
    }
}
