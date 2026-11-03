//! Welcome tour: the desktop twin of the landing page. One big shape morphs between slides,
//! satellites orbit it, and a live mock of the real screen plays inside the stage. The text side
//! carries a step counter, the headline, feature chips and live library numbers; a subject ticker
//! scrolls underneath. Everything moves on the same springs as the rest of the app.
mod scenes;

use egui::{pos2, vec2, Align, Color32, Key, Layout, Rect, Rounding, Ui, UiBuilder};

use crate::actions::Action;
use crate::env::Env;
use crate::theme::{fonts, mix, motion, Theme};
use crate::ui::icons::{self, Icon};
use crate::ui::shapes::{self, Kind};
use crate::ui::theme_toggle;
use crate::ui::widgets::{self, BtnKind};

struct Slide {
    head: &'static str,
    #[allow(dead_code)]
    icon: Icon,
    kind: Kind,
    chips: [(Icon, &'static str); 3],
    tags: [(Icon, &'static str); 2],
}

const SLIDES: [Slide; 4] = [
    Slide { head: "Read every chapter.", icon: Icon::Library, kind: Kind::Cookie, chips: [(Icon::Article, "Notes"), (Icon::Bolt, "Diagrams"), (Icon::Text, "Maths")], tags: [(Icon::BookmarkFilled, "Saved"), (Icon::Clock, "12 min read")] },
    Slide { head: "Practice every paper.", icon: Icon::Quiz, kind: Kind::Flower, chips: [(Icon::Quiz, "Model papers"), (Icon::List, "Question banks"), (Icon::Clock, "Timed tests")], tags: [(Icon::Done, "3 correct"), (Icon::Star, "Top score")] },
    Slide { head: "Find it in seconds.", icon: Icon::Search, kind: Kind::Sunny, chips: [(Icon::Library, "Chapters"), (Icon::Tag, "Topics"), (Icon::Help, "Questions")], tags: [(Icon::Bolt, "Instant"), (Icon::Keyboard, "Ctrl K")] },
    Slide { head: "Study anywhere, offline.", icon: Icon::Download, kind: Kind::Clover, chips: [(Icon::Article, "Study books"), (Icon::Cloud, "Offline"), (Icon::Sync, "Synced")], tags: [(Icon::Cloud, "Offline"), (Icon::Check, "Ready")] },
];

const SUBJECTS: [&str; 12] = ["Physics", "Chemistry", "Mathematics", "Biology", "English", "Nepali", "Accountancy", "Economics", "Computer Science", "Social Studies", "Optional Maths", "Business Studies"];

#[derive(Default)]
pub struct IntroState {
    cur: usize,
    /// Clock time when the current slide appeared (drives the scene animation).
    since: f64,
}

impl IntroState {
    /// Jump to a slide (screenshot tour).
    pub fn goto(&mut self, i: usize) {
        self.cur = i.min(SLIDES.len() - 1);
        self.since = 0.0;
    }

    fn set(&mut self, i: usize, now: f64) {
        if self.cur != i {
            self.cur = i;
            self.since = now;
        }
    }
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
    let now = ctx.input(|i| i.time);
    let time = now as f32;
    let last = SLIDES.len() - 1;
    if st.since == 0.0 {
        st.since = now;
    }

    if !ctx.wants_keyboard_input() {
        let (next, prev, esc) = ctx.input(|i| (i.key_pressed(Key::ArrowRight) || i.key_pressed(Key::Enter) || i.key_pressed(Key::Space), i.key_pressed(Key::ArrowLeft), i.key_pressed(Key::Escape)));
        if next {
            if st.cur == last {
                finish(env);
            } else {
                st.set(st.cur + 1, now);
            }
        }
        if prev && st.cur > 0 {
            st.set(st.cur - 1, now);
        }
        if esc {
            finish(env);
        }
    }

    let compact = rect.width() < 760.0;
    let m = if compact { 20.0 } else { 44.0 };
    let body = rect.shrink2(vec2(m, 18.0));
    let id = ui.id().with("intro");
    let e_top = motion::enter(&ctx, id.with("top"), 0.0, 0.6);
    let e_stage = motion::enter(&ctx, id.with("stage"), 0.08, 0.9);
    let e_head = motion::enter(&ctx, id.with("head"), 0.22, 0.7);
    let e_bot = motion::enter(&ctx, id.with("bot"), 0.34, 0.7);
    let e_stats = motion::enter(&ctx, id.with("stats"), 0.5, 1.4);

    backdrop(ui, &th, rect, time, e_stage);

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

    // ---- regions
    let bottom_h = 64.0;
    let ticker_h = if compact { 0.0 } else { 44.0 };
    let content = Rect::from_min_max(pos2(body.min.x, top.max.y + 8.0), pos2(body.max.x, body.max.y - bottom_h - ticker_h - 16.0));
    let (stage, text) = if compact {
        let sh = (content.height() * 0.5).min(content.width());
        (Rect::from_min_size(content.min, vec2(content.width(), sh)), Rect::from_min_max(pos2(content.min.x, content.min.y + sh), content.max))
    } else {
        let split = content.min.x + content.width() * 0.48;
        (Rect::from_min_max(pos2(split, content.min.y), content.max), Rect::from_min_max(content.min, pos2(split - 24.0, content.max.y)))
    };

    stage_art(ui, &th, st, stage, time, now, e_stage);
    text_block(ui, env, &th, st, text, compact, e_head, e_stats);
    if !compact {
        ticker(ui, &th, Rect::from_min_size(pos2(body.min.x - m, body.max.y - bottom_h - ticker_h - 8.0), vec2(rect.width(), ticker_h)), time, e_bot);
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
                        st.set(st.cur + 1, now);
                    }
                }
                if st.cur > 0 && widgets::icon_button_sized(ui, &th, Icon::Back, "Back", false, 48.0).clicked() {
                    st.set(st.cur - 1, now);
                }
            });
        });
    });
    ctx.request_repaint();
}

/// Slow drifting shapes in the corners so the page never feels empty.
fn backdrop(ui: &Ui, th: &Theme, rect: Rect, time: f32, enter: f32) {
    let big = rect.width().max(rect.height()) * 0.5;
    let c1 = rect.min + vec2(rect.width() * 0.04 + (time * 0.15).sin() * 20.0, rect.height() * 0.95 + (time * 0.2).cos() * 16.0);
    shapes::paint_morph(ui.painter(), Rect::from_center_size(c1, vec2(big, big)), Kind::Flower, Kind::Cookie, 0.5 + 0.5 * (time * 0.3).sin(), time * 0.05, th.p.accent_soft.gamma_multiply(0.45 * enter));
    let c2 = rect.max - vec2(rect.width() * 0.02 + (time * 0.12).cos() * 18.0, rect.height() * 0.96 + (time * 0.17).sin() * 14.0);
    shapes::paint_morph(ui.painter(), Rect::from_center_size(c2, vec2(big * 0.7, big * 0.7)), Kind::Burst, Kind::Sunny, 0.5 + 0.5 * (time * 0.25).cos(), -time * 0.06, th.p.secondary_container.gamma_multiply(0.55 * enter));
}

fn text_block(ui: &mut Ui, env: &Env, th: &Theme, st: &IntroState, text: Rect, compact: bool, e_head: f32, e_stats: f32) {
    let ctx = ui.ctx().clone();
    let id = ui.id().with("intro-text");
    let size = if compact { 34.0 } else { (text.width() / 9.0).clamp(42.0, 62.0) };
    let head_h = ui.painter().layout(SLIDES[st.cur].head.to_owned(), fonts::bold(size), th.p.ink, text.width()).size().y;
    let show_stats = !compact && env.total_chapters() > 0;
    let block_h = 34.0 + head_h + 22.0 + 44.0 + if show_stats { 36.0 + 76.0 } else { 0.0 };
    let top = (text.center().y - block_h / 2.0).max(text.min.y);

    // step counter: 01 ──── 04
    let ce = e_head;
    let num = format!("{:02}", st.cur + 1);
    ui.painter().text(pos2(text.min.x, top + 8.0), egui::Align2::LEFT_CENTER, num, fonts::bold(15.0), th.p.accent.gamma_multiply(ce));
    let track = Rect::from_min_size(pos2(text.min.x + 34.0, top + 6.0), vec2(96.0, 4.0));
    ui.painter().rect_filled(track, 2.0, th.p.hairline.gamma_multiply(ce));
    let prog = motion::spring_to(&ctx, id.with("prog"), (st.cur + 1) as f32 / SLIDES.len() as f32, motion::SPATIAL).clamp(0.0, 1.0);
    ui.painter().rect_filled(Rect::from_min_size(track.min, vec2(track.width() * prog, 4.0)), 2.0, th.p.accent.gamma_multiply(ce));
    ui.painter().text(pos2(track.max.x + 12.0, top + 8.0), egui::Align2::LEFT_CENTER, format!("{:02}", SLIDES.len()), fonts::medium(15.0), th.p.ink_faint.gamma_multiply(ce));

    // headline + chips per slide, each springing in/out as the slide changes
    for (i, s) in SLIDES.iter().enumerate() {
        let v = motion::spring_bool(&ctx, id.with(("h", i)), st.cur == i, motion::SPATIAL).clamp(0.0, 1.0);
        if v < 0.01 {
            continue;
        }
        let dir = if i >= st.cur { 1.0 } else { -1.0 };
        let galley = ui.painter().layout(s.head.to_owned(), fonts::bold(size), th.p.ink.gamma_multiply(v * e_head), text.width());
        let y = top + 34.0 + (1.0 - v) * 36.0 * dir + (1.0 - e_head) * 24.0;
        ui.painter().galley(pos2(text.min.x, y), galley, th.p.ink);

        let mut x = text.min.x;
        let cy = top + 34.0 + head_h + 22.0 + 22.0;
        for (k, (icon, label)) in s.chips.iter().enumerate() {
            let cv = motion::spring_bool(&ctx, id.with(("c", i, k)), st.cur == i, motion::FAST).clamp(0.0, 1.0) * v;
            let g = ui.painter().layout_no_wrap((*label).to_owned(), fonts::medium(14.0), th.p.on_accent_soft.gamma_multiply(cv));
            let w = g.size().x + 50.0;
            let r = Rect::from_center_size(pos2(x + w / 2.0, cy + (1.0 - cv) * 18.0 * dir), vec2(w, 40.0));
            ui.painter().rect_filled(r, Rounding::same(20.0), mix(th.p.accent_soft, tone(th, i), 0.0).gamma_multiply(cv));
            icons::paint(ui.painter(), Rect::from_center_size(pos2(r.min.x + 22.0, r.center().y), vec2(20.0, 20.0)), *icon, th.p.on_accent_soft.gamma_multiply(cv));
            ui.painter().galley(pos2(r.min.x + 38.0, r.center().y - g.size().y / 2.0), g, th.p.on_accent_soft);
            x += w + 10.0;
        }
    }

    // live library numbers that count up once
    if show_stats {
        let y = top + 34.0 + head_h + 22.0 + 44.0 + 36.0;
        let books = env.manifest.as_ref().map(|m| m.books).unwrap_or(0) as f32;
        let stats = [(env.total_chapters() as f32, "chapters"), (env.tracks.len() as f32, "levels"), (books, "study books")];
        let mut x = text.min.x;
        for (v, label) in stats.iter().filter(|(v, _)| *v > 0.0) {
            let shown = (v * e_stats).round() as u32;
            ui.painter().text(pos2(x, y), egui::Align2::LEFT_TOP, shown.to_string(), fonts::bold(34.0), th.p.ink.gamma_multiply(e_stats));
            ui.painter().text(pos2(x, y + 44.0), egui::Align2::LEFT_TOP, *label, fonts::regular(13.0), th.p.ink_muted.gamma_multiply(e_stats));
            x += 150.0;
        }
    }
}

/// Subject names drifting right to left, fading at both ends.
fn ticker(ui: &Ui, th: &Theme, area: Rect, time: f32, enter: f32) {
    let p = ui.painter().with_clip_rect(area);
    let gap = 12.0;
    let h = 38.0;
    let widths: Vec<f32> = SUBJECTS.iter().map(|s| p.layout_no_wrap((*s).to_owned(), fonts::medium(14.0), Color32::WHITE).size().x + 34.0).collect();
    let total: f32 = widths.iter().sum::<f32>() + gap * SUBJECTS.len() as f32;
    let off = (time * 36.0) % total;
    let y = area.center().y - h / 2.0;
    for rep in 0..3 {
        let mut x = area.min.x - off + total * rep as f32;
        for (i, s) in SUBJECTS.iter().enumerate() {
            let w = widths[i];
            if x + w > area.min.x && x < area.max.x {
                let edge = ((x - area.min.x) / 120.0).clamp(0.0, 1.0).min(((area.max.x - x - w) / 120.0).clamp(0.0, 1.0));
                let al = edge * enter;
                let r = Rect::from_min_size(pos2(x, y), vec2(w, h));
                p.rect(r, Rounding::same(h / 2.0), th.p.card.gamma_multiply(al), egui::Stroke::new(1.0_f32, th.p.hairline_strong.gamma_multiply(al)));
                p.text(r.center(), egui::Align2::CENTER_CENTER, *s, fonts::medium(14.0), th.p.ink.gamma_multiply(al));
            }
            x += w + gap;
        }
    }
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

fn stage_art(ui: &mut Ui, th: &Theme, st: &IntroState, stage: Rect, time: f32, now: f64, enter: f32) {
    let ctx = ui.ctx().clone();
    let last = SLIDES.len() - 1;
    let t = motion::spring_to(&ctx, ui.id().with("shape_t"), st.cur as f32, motion::SLOW);
    let i0 = (t.floor().max(0.0) as usize).min(last);
    let i1 = (i0 + 1).min(last);
    let frac = if i0 == i1 { 0.0 } else { (t - i0 as f32).clamp(-0.06, 1.06) };
    let d = (stage.width().min(stage.height()) * 0.92).clamp(200.0, 560.0) * (0.7 + 0.3 * enter);
    let c = stage.center();
    let main = Rect::from_center_size(c + vec2(d * 0.1, -d * 0.02), vec2(d, d));
    let color = mix(tone(th, i0), tone(th, i1), frac.clamp(0.0, 1.0));
    let rot = time * 0.18 + t * 0.7;

    // satellites
    let sats = [(Kind::Burst, 0.17, th.p.accent_soft), (Kind::Pebble, 0.12, th.p.secondary_container), (Kind::Clover, 0.09, th.p.teal_soft)];
    for (k, (kind, size, col)) in sats.iter().enumerate() {
        let a = k as f32 * 2.1 + 0.6 + t * 0.9 + time * 0.12;
        let r = d * (0.62 + 0.035 * (time * 1.3 + k as f32 * 2.0).sin());
        let p = c + vec2(a.cos(), a.sin()) * r * vec2(1.05, 0.86);
        let sd = d * size * (0.5 + 0.5 * enter);
        shapes::paint_morph(ui.painter(), Rect::from_center_size(p, vec2(sd, sd)), *kind, SLIDES[(k + i0) % 4].kind, 0.5 + 0.5 * (time * 0.8 + k as f32).sin(), -rot * 1.4, *col);
    }
    shapes::paint_morph(ui.painter(), main, SLIDES[i0].kind, SLIDES[i1].kind, frac, rot, color);

    // the live scene card, sliding in from the direction of travel
    let sw = (stage.width() * 0.72).min(stage.height() * 0.98).clamp(240.0, 440.0);
    let scene = Rect::from_center_size(c + vec2(0.0, (time * 0.9).sin() * 5.0), vec2(sw, sw * 0.98));
    for (i, s) in SLIDES.iter().enumerate() {
        let v = motion::spring_bool(&ctx, ui.id().with(("sc", i)), st.cur == i, motion::SPATIAL).clamp(0.0, 1.0);
        if v < 0.01 {
            continue;
        }
        let dir = if i >= st.cur { 1.0 } else { -1.0 };
        let clock = if i == st.cur { ((now - st.since) as f32).max(0.0) } else { 9.0 };
        let r = scene.translate(vec2((1.0 - v) * 70.0 * dir, (1.0 - v) * 24.0)).shrink((1.0 - v) * 14.0);
        scenes::paint(ui, th, i, r, clock * enter, v * enter);
        for (k, (icon, label)) in s.tags.iter().enumerate() {
            let anchor = if k == 0 { r.left_top() + vec2(10.0, 8.0) } else { r.right_bottom() - vec2(30.0, 6.0) };
            let tv = motion::spring_bool(&ctx, ui.id().with(("tg", i, k)), st.cur == i && clock > 0.5 + 0.5 * k as f32, motion::FAST).clamp(0.0, 1.0) * v;
            let bob = (time * 1.4 + k as f32 * 2.4).sin() * 5.0 + (1.0 - tv) * 16.0;
            scenes::tag(ui, th, anchor, *icon, label, tv, bob);
        }
    }
}
