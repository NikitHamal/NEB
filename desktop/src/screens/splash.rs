//! Splash — "the mark, and nothing else" (Android `SplashScreen.kt`):
//! 80 ms of empty paper, the mark fades in and settles from 94 % → 100 %,
//! holds, then pushes forward slightly while fading into the next screen.
use std::time::Instant;

use egui::{vec2, Color32, Rect, Sense, Ui};

use crate::actions::Action;
use crate::env::Env;
use crate::router::Route;

#[derive(Default)]
pub struct SplashState {
    start: Option<Instant>,
    done: bool,
}

impl SplashState {
    /// Freeze the animation `secs` in (screenshot tour only).
    pub fn hold(&mut self, secs: f32) {
        self.start = Some(Instant::now() - std::time::Duration::from_secs_f32(secs));
    }
}

pub fn next_route(env: &Env) -> Route {
    let s = &env.store.s;
    if s.onboarded {
        Route::Home
    } else if s.session.is_some() || s.guest {
        Route::Onboarding
    } else {
        Route::Login
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut SplashState) {
    let start = *st.start.get_or_insert_with(Instant::now);
    let t = start.elapsed().as_secs_f32();
    let (lead, fade_in, hold, exit) = if env.motion() { (0.08, 0.52, 0.40, 0.25) } else { (0.0, 0.0, 0.45, 0.0) };
    let enter = if fade_in > 0.0 { ((t - lead) / fade_in).clamp(0.0, 1.0) } else { 1.0 };
    let enter = 1.0 - (1.0 - enter).powi(3);
    let leaving = if exit > 0.0 { ((t - lead - fade_in - hold) / exit).clamp(0.0, 1.0) } else { 0.0 };
    let total = lead + fade_in + hold + exit;

    // The splash is always light, like the rest of the sign-in journey.
    let (rect, _) = ui.allocate_exact_size(ui.available_size(), Sense::hover());
    ui.painter().rect_filled(rect, 0.0, Color32::WHITE);
    let size = 132.0 * (0.94 + 0.06 * enter) * (1.0 + 0.06 * leaving);
    let alpha = enter * (1.0 - leaving);
    let logo_rect = Rect::from_center_size(rect.center(), vec2(size, size));
    env.logo.paint(ui, logo_rect, alpha);

    if t >= total && !st.done {
        st.done = true;
        let next = next_route(env);
        env.act(Action::Replace(next));
    } else {
        ui.ctx().request_repaint();
    }
}
