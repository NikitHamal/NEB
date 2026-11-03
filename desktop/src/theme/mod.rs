//! Theme: colour palette (mirrored from Android's `NebAuthPalette`), fonts, spacing,
//! and the translation of all of that into egui `Visuals` / `Style`.
pub mod colors;
pub mod fonts;
pub mod motion;
pub mod spacing;

use egui::{Color32, Context, FontFamily, FontId, Rounding, Stroke, TextStyle};

pub use colors::Palette;

#[derive(Clone, Debug)]
pub struct Theme {
    pub p: Palette,
    pub dark: bool,
}

impl Theme {
    pub fn new(dark: bool) -> Self {
        Self { p: if dark { Palette::dark() } else { Palette::light() }, dark }
    }

    /// Push the palette into egui's global style. Called whenever the theme flips.
    pub fn apply(&self, ctx: &Context) {
        let p = &self.p;
        let mut v = if self.dark { egui::Visuals::dark() } else { egui::Visuals::light() };
        v.panel_fill = p.page;
        v.window_fill = p.surface_high;
        v.extreme_bg_color = p.field;
        v.faint_bg_color = p.field;
        v.code_bg_color = p.field;
        v.override_text_color = Some(p.ink);
        v.hyperlink_color = p.accent;
        v.window_stroke = Stroke::new(1.0, p.hairline);
        v.window_rounding = Rounding::same(spacing::PANEL_RADIUS);
        v.menu_rounding = Rounding::same(spacing::SHAPE_MD);
        // No shadows anywhere: separation is tone + outline (same rule as the web).
        v.window_shadow = egui::epaint::Shadow::NONE;
        v.popup_shadow = egui::epaint::Shadow::NONE;
        v.selection.bg_fill = if self.dark { mix(p.page, p.accent, 0.40) } else { mix(p.page, p.accent, 0.28) };
        v.selection.stroke = Stroke::new(1.0, p.accent);
        let r = Rounding::same(spacing::SHAPE_SM);
        for w in [&mut v.widgets.noninteractive, &mut v.widgets.inactive, &mut v.widgets.hovered, &mut v.widgets.active, &mut v.widgets.open] {
            w.rounding = r;
        }
        v.widgets.noninteractive.bg_fill = p.card;
        v.widgets.noninteractive.bg_stroke = Stroke::new(1.0, p.hairline);
        v.widgets.noninteractive.fg_stroke = Stroke::new(1.0, p.ink);
        v.widgets.inactive.bg_fill = p.field;
        v.widgets.inactive.weak_bg_fill = p.field;
        v.widgets.inactive.bg_stroke = Stroke::new(1.0, p.hairline);
        v.widgets.inactive.fg_stroke = Stroke::new(1.0, p.ink);
        let hov = mix(p.field, p.ink, 0.06);
        v.widgets.hovered.bg_fill = hov;
        v.widgets.hovered.weak_bg_fill = hov;
        v.widgets.hovered.bg_stroke = Stroke::new(1.0, p.hairline_strong);
        v.widgets.hovered.fg_stroke = Stroke::new(1.0, p.ink);
        v.widgets.active.bg_fill = mix(p.field, p.ink, 0.12);
        v.widgets.active.weak_bg_fill = mix(p.field, p.ink, 0.12);
        v.widgets.active.bg_stroke = Stroke::new(1.0, p.accent);
        v.widgets.active.fg_stroke = Stroke::new(1.0, p.ink);
        v.widgets.open.bg_fill = p.accent_soft;
        v.widgets.open.weak_bg_fill = p.accent_soft;
        ctx.set_visuals(v);

        let mut s = (*ctx.style()).clone();
        s.spacing.item_spacing = egui::vec2(10.0, 8.0);
        s.spacing.button_padding = egui::vec2(14.0, 8.0);
        s.spacing.interact_size.y = 34.0;
        s.spacing.menu_margin = egui::Margin::same(8.0);
        s.spacing.scroll = egui::style::ScrollStyle::floating();
        s.interaction.selectable_labels = true;
        s.text_styles = [
            (TextStyle::Heading, FontId::new(28.0, FontFamily::Name(fonts::BOLD.into()))),
            (TextStyle::Body, FontId::new(15.0, FontFamily::Proportional)),
            (TextStyle::Button, FontId::new(14.5, FontFamily::Name(fonts::MEDIUM.into()))),
            (TextStyle::Small, FontId::new(12.5, FontFamily::Proportional)),
            (TextStyle::Monospace, FontId::new(13.5, FontFamily::Monospace)),
        ]
        .into();
        ctx.set_style(s);
    }
}

/// Parse `#RRGGBB`.
pub fn parse_hex(hex: &str) -> Option<Color32> {
    let h = hex.trim().trim_start_matches('#');
    if h.len() != 6 {
        return None;
    }
    let n = u32::from_str_radix(h, 16).ok()?;
    Some(Color32::from_rgb((n >> 16) as u8, (n >> 8) as u8, n as u8))
}

/// Mix `a` towards `b` by `t` (0..1).
pub fn mix(a: Color32, b: Color32, t: f32) -> Color32 {
    let f = |x: u8, y: u8| (x as f32 + (y as f32 - x as f32) * t).round() as u8;
    Color32::from_rgb(f(a.r(), b.r()), f(a.g(), b.g()), f(a.b(), b.b()))
}

impl Theme {
    /// A subject's data colour, made readable on the current surface.
    pub fn subject_color(&self, hex: &str) -> Color32 {
        let c = parse_hex(hex).unwrap_or(self.p.accent);
        if self.dark {
            mix(c, Color32::WHITE, 0.38)
        } else {
            c
        }
    }

    /// A very light wash of `c` on the page colour (tile backgrounds).
    pub fn wash(&self, c: Color32) -> Color32 {
        mix(self.p.card, c, if self.dark { 0.20 } else { 0.10 })
    }
}
