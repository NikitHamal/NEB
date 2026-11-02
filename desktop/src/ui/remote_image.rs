//! Server images (avatars) with a disk cache: fetched on a worker thread, painted once they land.
use std::collections::HashMap;
use std::sync::{Arc, Mutex, OnceLock};

use egui::{vec2, Color32, Sense, Ui};

use crate::data::content::ContentRepo;
use crate::theme::Theme;

enum Slot {
    Loading,
    Ready(Arc<[u8]>),
    Failed,
}

struct Cache {
    repo: ContentRepo,
    map: HashMap<String, Slot>,
}

static CACHE: OnceLock<Mutex<Cache>> = OnceLock::new();

pub fn init(repo: ContentRepo) {
    let _ = CACHE.set(Mutex::new(Cache { repo, map: HashMap::new() }));
}

pub fn clear() {
    if let Some(c) = CACHE.get() {
        if let Ok(mut c) = c.lock() {
            c.map.retain(|_, s| matches!(s, Slot::Ready(_)));
        }
    }
}

fn bytes(ctx: &egui::Context, url: &str) -> Option<Arc<[u8]>> {
    let cache = CACHE.get()?;
    let mut c = cache.lock().ok()?;
    match c.map.get(url) {
        Some(Slot::Ready(b)) => return Some(b.clone()),
        Some(_) => return None,
        None => {}
    }
    c.map.insert(url.to_string(), Slot::Loading);
    let repo = c.repo.clone();
    let (u, ctx) = (url.to_string(), ctx.clone());
    drop(c);
    std::thread::spawn(move || {
        let slot = match repo.image_bytes(&u) {
            Ok(b) if !b.is_empty() => Slot::Ready(Arc::from(b.into_boxed_slice())),
            _ => Slot::Failed,
        };
        if let Some(cache) = CACHE.get() {
            if let Ok(mut c) = cache.lock() {
                c.map.insert(u, slot);
            }
        }
        ctx.request_repaint();
    });
    None
}

fn ext(b: &[u8]) -> &'static str {
    let head = String::from_utf8_lossy(&b[..b.len().min(200)]).to_lowercase();
    if head.contains("<svg") || head.starts_with("<?xml") {
        "svg"
    } else if b.starts_with(&[0x89, b'P', b'N', b'G']) {
        "png"
    } else if b.starts_with(&[0xFF, 0xD8]) {
        "jpg"
    } else {
        "webp"
    }
}

/// Round avatar: the server image when there is one (and it has loaded), otherwise the monogram.
pub fn avatar(ui: &mut Ui, th: &Theme, name: &str, tone_idx: usize, size: f32, url: &str) {
    if !url.is_empty() {
        if let Some(b) = bytes(ui.ctx(), url) {
            use sha2::{Digest, Sha256};
            let id: String = Sha256::digest(url.as_bytes()).iter().take(8).map(|x| format!("{x:02x}")).collect();
            let uri = format!("bytes://avatar/{id}.{}", ext(&b));
            let (rect, _) = ui.allocate_exact_size(vec2(size, size), Sense::hover());
            ui.painter().circle_filled(rect.center(), size / 2.0, th.p.field);
            egui::Image::from_bytes(uri, egui::load::Bytes::Shared(b)).fit_to_exact_size(vec2(size, size)).rounding(size / 2.0).tint(Color32::WHITE).paint_at(ui, rect);
            ui.painter().circle_stroke(rect.center(), size / 2.0 - 0.5, egui::Stroke::new(1.0, th.p.hairline));
            return;
        }
    }
    crate::ui::avatar::avatar(ui, th, name, tone_idx, size);
}
