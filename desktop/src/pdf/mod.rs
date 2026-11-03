//! Native PDF engine. `hayro` (pure Rust, CPU) rasterises pages on a small pool of worker threads
//! that each own a parsed copy of the document, so the UI thread never parses or draws a page.
//!
//! * The viewer states which (page, scale) tiles it wants each frame; the queue is REPLACED, so
//!   scrolling fast never builds a backlog of stale pages.
//! * Finished pages are uploaded as GPU textures (max a few per frame) into an LRU cache.
//! * While a sharp tile is rendering, the best tile already cached for that page is stretched in
//!   its place, so zooming and scrolling never flash blank pages.
use std::collections::{HashMap, HashSet};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc::{channel, Receiver, Sender};
use std::sync::{Arc, Condvar, Mutex};

use egui::{ColorImage, Context, TextureHandle, TextureOptions};
use hayro::hayro_interpret::InterpreterSettings;
use hayro::hayro_syntax::Pdf;
use hayro::vello_cpu::color::palette::css::WHITE;
use hayro::{render, PixmapSettings, RenderCache, RenderSettings};

/// One rasterised tile: a page at a scale, in light or night colours.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Key {
    pub page: u32,
    /// Scale in 1/20 steps (pixels per PDF point).
    pub q: u16,
    pub night: bool,
}

impl Key {
    pub fn scale(&self) -> f32 {
        self.q as f32 / 20.0
    }
    /// Quantise a wanted pixels-per-point value. Reading tiles snap to quarter steps so a smooth
    /// zoom does not render a new tile on every frame.
    pub fn reading(page: u32, ppp: f32, night: bool) -> Key {
        let q = ((ppp * 4.0).ceil().clamp(1.0, 24.0) * 5.0) as u16;
        Key { page, q, night }
    }
    pub fn thumb(page: u32, night: bool) -> Key {
        Key { page, q: 7, night }
    }
}

enum Done {
    Meta(Result<Vec<(f32, f32)>, String>),
    Tile(Key, Option<ColorImage>),
}

struct Shared {
    queue: Mutex<Vec<Key>>,
    cv: Condvar,
    inflight: Mutex<HashSet<Key>>,
    stop: AtomicBool,
}

pub struct PdfEngine {
    pub path: PathBuf,
    /// Page sizes in PDF points, once the document has been parsed.
    pub pages: Vec<(f32, f32)>,
    pub error: Option<String>,
    sh: Arc<Shared>,
    rx: Receiver<Done>,
    tiles: HashMap<Key, (TextureHandle, u64)>,
    failed: HashSet<Key>,
    tick: u64,
}

impl PdfEngine {
    pub fn open(ctx: &Context, path: PathBuf) -> Self {
        let sh = Arc::new(Shared { queue: Mutex::new(vec![]), cv: Condvar::new(), inflight: Mutex::new(HashSet::new()), stop: AtomicBool::new(false) });
        let (tx, rx) = channel::<Done>();
        let data = std::fs::read(&path).map(Arc::new);
        match data {
            Err(e) => {
                let _ = tx.send(Done::Meta(Err(format!("Could not read the file: {e}"))));
            }
            Ok(data) => {
                // Metadata thread: page sizes only.
                {
                    let (data, tx, ctx) = (data.clone(), tx.clone(), ctx.clone());
                    std::thread::spawn(move || {
                        let r = catch_unwind(AssertUnwindSafe(|| match Pdf::new(data) {
                            Ok(pdf) => Ok(pdf.pages().iter().map(|p| p.render_dimensions()).collect::<Vec<_>>()),
                            Err(e) => Err(format!("This PDF could not be opened ({e:?})")),
                        }))
                        .unwrap_or_else(|_| Err("This PDF could not be read".into()));
                        let _ = tx.send(Done::Meta(r));
                        ctx.request_repaint();
                    });
                }
                let n = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(2).saturating_sub(1).clamp(1, 3);
                for _ in 0..n {
                    let (data, sh, tx, ctx) = (data.clone(), sh.clone(), tx.clone(), ctx.clone());
                    std::thread::spawn(move || worker(data, sh, tx, ctx));
                }
            }
        }
        Self { path, pages: vec![], error: None, sh, rx, tiles: HashMap::new(), failed: HashSet::new(), tick: 0 }
    }

    pub fn ready(&self) -> bool {
        !self.pages.is_empty()
    }

    /// Drain finished work. Uploads at most `budget` textures per call to keep frames short.
    pub fn poll(&mut self, ctx: &Context) {
        self.tick += 1;
        let mut budget = 3;
        while budget > 0 {
            let Ok(msg) = self.rx.try_recv() else { break };
            match msg {
                Done::Meta(Ok(p)) if p.is_empty() => self.error = Some("This PDF has no pages".into()),
                Done::Meta(Ok(p)) => self.pages = p,
                Done::Meta(Err(e)) => self.error = Some(e),
                Done::Tile(key, img) => {
                    self.sh.inflight.lock().unwrap().remove(&key);
                    match img {
                        Some(img) => {
                            let h = ctx.load_texture(format!("pdf-{}-{}-{}", key.page, key.q, key.night), img, TextureOptions::LINEAR);
                            self.tiles.insert(key, (h, self.tick));
                            budget -= 1;
                        }
                        None => {
                            self.failed.insert(key);
                        }
                    }
                }
            }
        }
        if budget == 0 {
            ctx.request_repaint();
        }
        self.evict();
    }

    /// Keep the most recently used tiles: thumbnails are tiny so they stay; reading tiles are capped.
    fn evict(&mut self) {
        const MAX_READING: usize = 14;
        let mut reading: Vec<(Key, u64)> = self.tiles.iter().filter(|(k, _)| k.q > 7).map(|(k, v)| (*k, v.1)).collect();
        if reading.len() > MAX_READING {
            reading.sort_by_key(|(_, t)| *t);
            for (k, _) in reading.iter().take(reading.len() - MAX_READING) {
                self.tiles.remove(k);
            }
        }
    }

    /// Ask for these tiles, most important first. Replaces anything still queued.
    pub fn want(&mut self, keys: &[Key]) {
        let inflight = self.sh.inflight.lock().unwrap().clone();
        let todo: Vec<Key> = keys.iter().copied().filter(|k| !self.tiles.contains_key(k) && !inflight.contains(k) && !self.failed.contains(k)).collect();
        let mut q = self.sh.queue.lock().unwrap();
        if *q != todo {
            *q = todo;
            self.sh.cv.notify_all();
        }
    }

    pub fn exact(&mut self, key: Key) -> Option<egui::TextureId> {
        let t = self.tick;
        self.tiles.get_mut(&key).map(|(h, used)| {
            *used = t;
            h.id()
        })
    }

    /// The sharpest tile available for `page` in this colour mode (any scale).
    pub fn best(&mut self, page: u32, night: bool) -> Option<egui::TextureId> {
        let t = self.tick;
        let k = self.tiles.keys().filter(|k| k.page == page && k.night == night).max_by_key(|k| k.q).copied()?;
        let e = self.tiles.get_mut(&k)?;
        e.1 = t;
        Some(e.0.id())
    }

    pub fn has_failed(&self, page: u32, night: bool) -> bool {
        self.failed.iter().any(|k| k.page == page && k.night == night) && !self.tiles.keys().any(|k| k.page == page && k.night == night)
    }

    pub fn clear_night_variants(&mut self) {
        self.failed.clear();
    }
}

impl Drop for PdfEngine {
    fn drop(&mut self) {
        self.sh.stop.store(true, Ordering::Relaxed);
        self.sh.cv.notify_all();
    }
}

fn worker(data: Arc<Vec<u8>>, sh: Arc<Shared>, tx: Sender<Done>, ctx: Context) {
    let Ok(pdf) = Pdf::new(data) else { return };
    let settings = InterpreterSettings::default();
    let mut cache = RenderCache::new();
    loop {
        let key = {
            let mut q = sh.queue.lock().unwrap();
            loop {
                if sh.stop.load(Ordering::Relaxed) {
                    return;
                }
                if !q.is_empty() {
                    let k = q.remove(0);
                    sh.inflight.lock().unwrap().insert(k);
                    break k;
                }
                q = sh.cv.wait(q).unwrap();
            }
        };
        let img = catch_unwind(AssertUnwindSafe(|| rasterise(&pdf, &cache, &settings, key)));
        let img = match img {
            Ok(i) => i,
            Err(_) => {
                cache = RenderCache::new();
                None
            }
        };
        let _ = tx.send(Done::Tile(key, img));
        ctx.request_repaint();
    }
}

fn rasterise<'a>(pdf: &'a Pdf, cache: &RenderCache<'a>, settings: &InterpreterSettings, key: Key) -> Option<ColorImage> {
    let page = pdf.pages().get(key.page as usize)?;
    let (w, h) = page.render_dimensions();
    // Never exceed a texture the GPU can hold.
    let scale = key.scale().min(4096.0 / w.max(h).max(1.0));
    let pm = render(page, cache, settings, &RenderSettings::default(), &PixmapSettings { x_scale: scale, y_scale: scale, bg_color: WHITE });
    let (pw, ph) = (pm.width() as usize, pm.height() as usize);
    let mut bytes = pm.data_as_u8_slice().to_vec();
    if key.night {
        night_map(&mut bytes);
    }
    Some(ColorImage::from_rgba_premultiplied([pw, ph], &bytes))
}

/// Night reading: invert luminance into the app's dark surface and soft text colour (page is opaque).
fn night_map(px: &mut [u8]) {
    const BG: [f32; 3] = [15.0, 22.0, 38.0]; // between surface and surface-container in dark theme
    const FG: [f32; 3] = [222.0, 228.0, 244.0];
    for p in px.chunks_exact_mut(4) {
        for c in 0..3 {
            let t = 1.0 - p[c] as f32 / 255.0;
            p[c] = (BG[c] + (FG[c] - BG[c]) * t) as u8;
        }
        p[3] = 255;
    }
}
