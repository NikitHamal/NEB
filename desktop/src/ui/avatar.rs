//! Monogram avatars. Android lets people pick shape/colour; on desktop the
//! profile keeps a tone index into this ramp.
use egui::{vec2, Color32, Sense, Ui};

use crate::theme::Theme;

pub const TONES: [u32; 8] = [0x004AC6, 0x4F46E5, 0x7C3AED, 0x0F766E, 0x15803D, 0x9A6206, 0xB3261E, 0x3F3F46];

pub fn tone(i: usize) -> Color32 {
    let n = TONES[i % TONES.len()];
    Color32::from_rgb((n >> 16) as u8, (n >> 8) as u8, n as u8)
}

pub fn avatar(ui: &mut Ui, _th: &Theme, name: &str, tone_idx: usize, size: f32) {
    let (rect, _) = ui.allocate_exact_size(vec2(size, size), Sense::hover());
    ui.painter().circle_filled(rect.center(), size / 2.0, tone(tone_idx));
    ui.painter().text(rect.center(), egui::Align2::CENTER_CENTER, crate::util::initials(name), crate::theme::fonts::bold(size * 0.38), Color32::WHITE);
}
