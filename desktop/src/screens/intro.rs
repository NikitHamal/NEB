//! Welcome tour: the desktop twin of the landing page. One big shape morphs between slides
//! (same polygons and springs as the website), satellites orbit it, the headline springs in and
//! the page indicator stretches. No taglines: a headline and the picture are the whole slide.
use egui::{pos2, vec2, Align, Align2, Color32, Key, Layout, Rect, Ui, UiBuilder};

use crate::actions::Action;
use crate::env::Env;
use crate::theme::{fonts, mix, motion, Theme};
use crate::ui::icons::{self, Icon};
use crate::ui::shapes::{self, Kind};
use crate::ui::widgets::{self, BtnKind};
use crate::ui::theme_toggle;

struct Slide {
    head: &'static str,
    icon: Icon,
    kind: Kind,
}

const SLIDES: [Slide; 4] = [
    Slide { head: "Read every chapter.", icon: Icon::Library, kind: Kind::Cookie },
    Slide { head: "Practice every paper.", icon: Icon::Quiz, kind: Kind::Flower },
    Slide { head: "Find it in seconds.", icon: Icon::Search, kind: Kind::Sunny },
    Slide { head: "Study anywhere, offline.", icon: Icon::Download, kind: Kind::Clover },
];

#[derive(Default)]
pub struct IntroState {
    cur: usize,
}

fn tone(th: &Theme, i: usize) -> Color32 {
    match i {
        0 => th.p.accent,
        1 => th.p.teal,
        2 => th.p.ok,
        _ => th.p.violet,
    }
}

fn finish(env: &mut Env) {
    env.store.s.intro_done = true;
    env.store.touch();
    let next = super::splash::next_route(env);
    env.act(Action::Replace(next));
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut IntroState) {
    let th = env.theme.clone();
    let ctx = ui.ctx().clone();
    let rect = ui.available_rect_before_wrap();
    ui.allocate_rect(rect, egui::Sense::hover());
    let time = ctx.input(|i| i.time) as f32;
    let last = SLIDES.len() - 1;

    // keys
    if !ctx.wants_keyboard_input() {
        let (next, prev, esc) = ctx.input(|i| (i.key_pressed(Key::ArrowRight) || i.key_pressed(Key::Enter) || i.key_pressed(Key::Space), i.key_pressed(Key::ArrowLeft), i.key_pressed(Key::Escape)));
        if next {
            if st.cur == last {
                finish(env);
            } else {
                st.cur += 1;
            }
        }
        if prev && st.cur > 0 {
            st.cur -= 1;
        }
        if esc {
            finish(env);
        }
    }

    let compact = rect.width() < 760.0;
    let m = if compact { 20.0 } else { 40.0 };
    let body = rect.shrink2(vec2(m, 18.0));
    let id = ui.id().with("intro");
    let e_top = motion::enter(&ctx, id.with("top"), 0.0, 0.6);
    let e_stage = motion::enter(&ctx, id.with("stage"), 0.08, 0.9);
    let e_head = motion::enter(&ctx, id.with("head"), 0.22, 0.7);
    let e_bot = motion::enter(&ctx, id.with("bot"), 0.34, 0.7);

    // ---- top bar
    let top = Rect::from_min_size(body.min + vec2(0.0, (1.0 - e_top) * -16.0), vec2(body.width(), 48.0));
    ui.allocate_new_ui(UiBuilder::new().max_rect(top), |ui| {
        ui.set_opacity(e_top);
        ui.horizontal(|ui| {
            env.logo.show(ui, 40.0);
            widgets::label(ui, egui::RichText::new("NEBians").font(fonts::bold(22.0)).color(th.p.ink));
            ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                if theme_toggle::show(ui, &th).clicked() {
                    env.act(Action::ToggleDark);
                }
                if st.cur < last && widgets::button_sized(ui, &th, "Skip", BtnKind::Ghost, None, None, 44.0).clicked() {
                    finish(env);
                }
            });
        });
    });

    // ---- layout regions
    let bottom_h = 64.0;
    let content = Rect::from_min_max(pos2(body.min.x, top.max.y + 8.0), pos2(body.max.x, body.max.y - bottom_h - 8.0));
    let (stage, text) = if compact {
        let sh = (content.height() * 0.52).min(content.width());
        (Rect::from_min_size(content.min, vec2(content.width(), sh)), Rect::from_min_max(pos2(content.min.x, content.min.y + sh), content.max))
    } else {
        let split = content.min.x + content.width() * 0.5;
        (Rect::from_min_max(pos2(split, content.min.y), content.max), Rect::from_min_max(content.min, pos2(split - 24.0, content.max.y)))
    };

    stage_art(ui, &th, st, stage, time, e_stage);

    // ---- headline (every slide is laid out; only the current one is visible)
    let size = if compact { 36.0 } else { (text.width() / 9.0).clamp(44.0, 64.0) };
    for (i, s) in SLIDES.iter().enumerate() {
        let v = motion::spring_bool(&ctx, id.with(("h", i)), st.cur == i, motion::SPATIAL).clamp(0.0, 1.0);
        if v < 0.01 {
            continue;
        }
        let dir = if i >= st.cur { 1.0 } else { -1.0 };
        let galley = ui.painter().layout(s.head.to_owned(), fonts::bold(size), th.p.ink.gamma_multiply(v * e_head), text.width());
        let h = galley.size().y;
        let y = text.center().y - h / 2.0 + (1.0 - v) * 36.0 * dir + (1.0 - e_head) * 24.0;
        ui.painter().galley(pos2(text.min.x, y), galley, th.p.ink);
    }

    // ---- bottom: dots + actions
    let bot = Rect::from_min_size(pos2(body.min.x, body.max.y - bottom_h + (1.0 - e_bot) * 24.0), vec2(body.width(), bottom_h));
    ui.allocate_new_ui(UiBuilder::new().max_rect(bot), |ui| {
        ui.set_opacity(e_bot);
        ui.horizontal_centered(|ui| {
            dots(ui, &th, st.cur);
            ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                let label = if st.cur == last { "Get started" } else { "Next" };
                let icon = if st.cur == last { Icon::Check } else { Icon::Forward };
                if widgets::button_sized(ui, &th, label, BtnKind::Primary, Some(icon), None, 56.0).clicked() {
                    if st.cur == last {
                        finish(env);
                    } else {
                        st.cur += 1;
                    }
                }
                if st.cur > 0 && widgets::icon_button_sized(ui, &th, Icon::Back, "Back", false, 48.0).clicked() {
                    st.cur -= 1;
                }
            });
        });
    });
    ctx.request_repaint();
}

/// Page indicator: the active dot stretches into a pill on a spring.
fn dots(ui: &mut Ui, th: &Theme, cur: usize) {
    ui.spacing_mut().item_spacing.x = 8.0;
    for i in 0..SLIDES.len() {
        let v = motion::spring_bool(ui.ctx(), ui.id().with(("dot", i)), cur == i, motion::FAST);
        let w = 12.0 + 28.0 * v.clamp(0.0, 1.2);
        let (r, _) = ui.allocate_exact_size(vec2(w, 12.0), egui::Sense::hover());
        let col = mix(th.p.hairline, th.p.accent, v.clamp(0.0, 1.0));
        ui.painter().rect_filled(r, 6.0, col);
    }
}

fn stage_art(ui: &mut Ui, th: &Theme, st: &IntroState, stage: Rect, time: f32, enter: f32) {
    let ctx = ui.ctx().clone();
    let last = SLIDES.len() - 1;
    let t = motion::spring_to(&ctx, ui.id().with("shape_t"), st.cur as f32, motion::SLOW);
    let i0 = (t.floor().max(0.0) as usize).min(last);
    let i1 = (i0 + 1).min(last);
    let frac = if i0 == i1 { 0.0 } else { (t - i0 as f32).clamp(-0.06, 1.06) };
    let d = (stage.width().min(stage.height()) * 0.74).clamp(180.0, 470.0) * (0.7 + 0.3 * enter);
    let c = stage.center();
    let main = Rect::from_center_size(c, vec2(d, d));
    let color = mix(tone(th, i0), tone(th, i1), frac.clamp(0.0, 1.0));
    let rot = time * 0.18 + t * 0.7;

    // satellites
    let sats = [(Kind::Burst, 0.21, th.p.accent_soft), (Kind::Pebble, 0.15, th.p.secondary_container), (Kind::Clover, 0.11, th.p.teal_soft)];
    for (k, (kind, size, col)) in sats.iter().enumerate() {
        let a = k as f32 * 2.1 + 0.6 + t * 0.9 + time * 0.12;
        let r = d * (0.66 + 0.035 * (time * 1.3 + k as f32 * 2.0).sin());
        let p = c + vec2(a.cos(), a.sin()) * r * vec2(1.0, 0.86);
        let sd = d * size * (0.5 + 0.5 * enter);
        shapes::paint_morph(ui.painter(), Rect::from_center_size(p, vec2(sd, sd)), *kind, SLIDES[(k + i0) % 4].kind, 0.5 + 0.5 * (time * 0.8 + k as f32).sin(), -rot * 1.4, *col);
    }

    shapes::paint_morph(ui.painter(), main, SLIDES[i0].kind, SLIDES[i1].kind, frac, rot, color);

    // icons cross-fade with a spring scale
    for (i, s) in SLIDES.iter().enumerate() {
        let v = motion::spring_bool(&ctx, ui.id().with(("ic", i)), st.cur == i, motion::SPATIAL);
        let a = v.clamp(0.0, 1.0);
        if a < 0.01 {
            continue;
        }
        let sz = d * 0.36 * (0.55 + 0.45 * v);
        let r = Rect::from_center_size(c, vec2(sz, sz));
        icons::paint(ui.painter(), r, s.icon, th.p.page.gamma_multiply(a));
    }
    let _ = Align2::CENTER_CENTER;
}
