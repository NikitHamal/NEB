//! The NEBians "N" mark. Uses the same artwork the web favicon / Android launcher
//! use (`n-logo-512.png`, rendered from the facet paths in `NebLogoMark.kt`).
use egui::{Color32, ColorImage, Context, Rect, TextureHandle, TextureOptions, Ui};

pub const LOGO_PNG: &[u8] = include_bytes!("../../assets/img/n-logo-512.png");
pub const ICON_PNG: &[u8] = include_bytes!("../../assets/img/n-logo-48.png");

pub struct Logo {
    tex: TextureHandle,
}

impl Logo {
    pub fn load(ctx: &Context) -> Self {
        let img = image::load_from_memory(LOGO_PNG).expect("embedded logo").to_rgba8();
        let size = [img.width() as usize, img.height() as usize];
        let ci = ColorImage::from_rgba_unmultiplied(size, img.as_raw());
        Self { tex: ctx.load_texture("neb-logo", ci, TextureOptions::LINEAR) }
    }

    /// Draw the mark in `rect` with an overall opacity (for the splash fade).
    pub fn paint(&self, ui: &Ui, rect: Rect, alpha: f32) {
        let tint = Color32::from_white_alpha((alpha.clamp(0.0, 1.0) * 255.0) as u8);
        ui.painter().image(self.tex.id(), rect, Rect::from_min_max(egui::pos2(0.0, 0.0), egui::pos2(1.0, 1.0)), tint);
    }

    pub fn show(&self, ui: &mut Ui, size: f32) {
        let (rect, _) = ui.allocate_exact_size(egui::vec2(size, size), egui::Sense::hover());
        self.paint(ui, rect, 1.0);
    }
}

pub fn window_icon() -> egui::IconData {
    let img = image::load_from_memory(ICON_PNG).expect("embedded icon").to_rgba8();
    egui::IconData { width: img.width(), height: img.height(), rgba: img.into_raw() }
}
