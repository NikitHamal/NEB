//! Motion tokens. The web uses three spatial springs (`--md-motion-spatial-fast/-/-slow`) and one
//! emphasized easing; this is the same set, integrated per frame so every widget (button press,
//! nav indicator, switch, page transition, shape morph) moves the same way.
use std::sync::atomic::{AtomicBool, Ordering};

use egui::{Context, Id};

static REDUCE: AtomicBool = AtomicBool::new(false);

/// Set once per frame from the user's "Reduce motion" preference.
pub fn set_reduced(on: bool) {
    REDUCE.store(on, Ordering::Relaxed);
}
pub fn reduced() -> bool {
    REDUCE.load(Ordering::Relaxed)
}

#[derive(Clone, Copy)]
pub struct Spring {
    pub k: f32,
    pub c: f32,
}
/// Small, snappy controls (buttons, chips, switches). Slight overshoot.
pub const FAST: Spring = Spring { k: 620.0, c: 32.0 };
/// Layout-level movement (indicators, cards, slides).
pub const SPATIAL: Spring = Spring { k: 340.0, c: 26.0 };
/// Large shapes and page transitions.
pub const SLOW: Spring = Spring { k: 170.0, c: 20.0 };

#[derive(Clone, Copy)]
struct State {
    x: f32,
    v: f32,
}

/// Spring `id` towards `target` and return the current value. Starts AT the target (no entrance
/// unless the target changes), and stops requesting repaints once settled.
pub fn spring_to(ctx: &Context, id: Id, target: f32, sp: Spring) -> f32 {
    if reduced() {
        return target;
    }
    let dt = ctx.input(|i| i.stable_dt).clamp(0.001, 0.05);
    let mut s = ctx.data_mut(|d| *d.get_temp_mut_or_insert_with(id, || State { x: target, v: 0.0 }));
    let n = 6;
    let h = dt / n as f32;
    for _ in 0..n {
        let a = sp.k * (target - s.x) - sp.c * s.v;
        s.v += a * h;
        s.x += s.v * h;
    }
    if (target - s.x).abs() < 0.0005 && s.v.abs() < 0.005 {
        s = State { x: target, v: 0.0 };
    } else {
        ctx.request_repaint();
    }
    ctx.data_mut(|d| d.insert_temp(id, s));
    s.x
}

pub fn spring_bool(ctx: &Context, id: Id, on: bool, sp: Spring) -> f32 {
    spring_to(ctx, id, if on { 1.0 } else { 0.0 }, sp)
}

/// Emphasized ease (same curve as `--ease-io`) for time-based tweens.
pub fn ease_io(t: f32) -> f32 {
    let t = t.clamp(0.0, 1.0);
    if t < 0.5 {
        4.0 * t * t * t
    } else {
        1.0 - (-2.0 * t + 2.0).powi(3) / 2.0
    }
}
pub fn ease_out(t: f32) -> f32 {
    1.0 - (1.0 - t.clamp(0.0, 1.0)).powi(3)
}

/// Entrance progress 0..1 for something that appears when first shown (cards, list rows).
/// `delay` staggers siblings. Resets when `key` changes, e.g. when the route changes.
pub fn enter(ctx: &Context, id: Id, delay: f32, dur: f32) -> f32 {
    if reduced() {
        return 1.0;
    }
    let now = ctx.input(|i| i.time);
    let t0 = ctx.data_mut(|d| *d.get_temp_mut_or_insert_with(id, || now));
    let p = ((now - t0) as f32 - delay) / dur;
    if p < 1.0 {
        ctx.request_repaint();
    }
    ease_out(p)
}

/// Forget entrance timers so the next screen animates in again.
pub fn reset_enter(ctx: &Context, id: Id) {
    ctx.data_mut(|d| d.remove::<f64>(id));
}

pub fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}
