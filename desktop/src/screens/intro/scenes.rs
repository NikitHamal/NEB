//! The four animated product scenes behind the welcome tour. Each is a small, live mock of the
//! real screen it introduces — reading, practising, searching, studying offline — painted with
//! the same tokens as the app, driven by one clock (`t` = seconds since the slide appeared).
use egui::{pos2, vec2, Align2, Color32, FontId, Painter, Rect, Rounding, Stroke, Ui};

use crate::theme::{fonts, mix, motion, Theme};
use crate::ui::icons::{self, Icon};

fn a(c: Color32, v: f32) -> Color32 {
    c.gamma_multiply(v.clamp(0.0, 1.0))
}

fn text(p: &Painter, pos: egui::Pos2, al: Align2, s: &str, f: FontId, c: Color32) {
    p.text(pos, al, s, f, c);
}

/// A grey bar standing in for a line of text; `frac` is how much of it has been "typed".
fn bar(p: &Painter, x: f32, y: f32, w: f32, h: f32, col: Color32, frac: f32) {
    let w = w * frac.clamp(0.0, 1.0);
    if w > 1.0 {
        p.rect_filled(Rect::from_min_size(pos2(x, y), vec2(w, h)), Rounding::same(h / 2.0), col);
    }
}

fn pill(p: &Painter, r: Rect, fill: Color32, stroke: Option<Color32>) {
    p.rect(r, Rounding::same(r.height() / 2.0), fill, Stroke::new(1.0_f32, stroke.unwrap_or(Color32::TRANSPARENT)));
}

/// Eased 0..1 progress of something that starts `delay` s in and lasts `dur` s.
fn prog(t: f32, delay: f32, dur: f32) -> f32 {
    motion::ease_out(((t - delay) / dur).clamp(0.0, 1.0))
}

/// The surface every scene sits on.
pub fn surface(p: &Painter, th: &Theme, r: Rect, alpha: f32) {
    p.rect(r, Rounding::same(r.width() * 0.07), a(th.p.card, alpha), Stroke::new(1.0_f32, a(th.p.hairline_strong, alpha)));
}

/// Paint scene `i` inside `r`. `al` fades the whole scene, `t` is the slide clock.
pub fn paint(ui: &Ui, th: &Theme, i: usize, r: Rect, t: f32, al: f32) {
    let p = ui.painter();
    surface(p, th, r, al);
    let u = r.width() / 400.0;
    let pad = 26.0 * u;
    let inner = r.shrink(pad);
    match i {
        0 => read(ui, th, inner, u, t, al),
        1 => practice(ui, th, inner, u, t, al),
        2 => search(ui, th, inner, u, t, al),
        _ => offline(ui, th, inner, u, t, al),
    }
}

fn read(ui: &Ui, th: &Theme, r: Rect, u: f32, t: f32, al: f32) {
    let p = ui.painter();
    let c = &th.p;
    // header: subject pill + bookmark
    pill(p, Rect::from_min_size(r.min, vec2(104.0 * u, 26.0 * u)), a(c.accent_soft, al), None);
    text(p, pos2(r.min.x + 52.0 * u, r.min.y + 13.0 * u), Align2::CENTER_CENTER, "Physics", fonts::medium(13.0 * u), a(c.on_accent_soft, al));
    let bm = prog(t, 1.4, 0.4);
    icons::paint(p, Rect::from_center_size(pos2(r.max.x - 12.0 * u, r.min.y + 13.0 * u), vec2(24.0 * u, 24.0 * u)), if bm > 0.5 { Icon::BookmarkFilled } else { Icon::Bookmark }, mix(c.ink_faint, c.accent, bm).gamma_multiply(al));
    // title
    let ty = r.min.y + 50.0 * u;
    text(p, pos2(r.min.x, ty), Align2::LEFT_TOP, "Projectile motion", fonts::bold(25.0 * u), a(c.ink, al * prog(t, 0.1, 0.5)));
    // paragraph lines typing in
    let line = mix(c.hairline_strong, c.card, 0.35);
    for (k, f) in [1.0, 0.92, 0.97, 0.6].iter().enumerate() {
        bar(p, r.min.x, ty + 52.0 * u + k as f32 * 18.0 * u, r.width() * f, 9.0 * u, a(line, al), prog(t, 0.35 + 0.18 * k as f32, 0.5));
    }
    // callout
    let cy = ty + 138.0 * u;
    let co = Rect::from_min_size(pos2(r.min.x, cy), vec2(r.width(), 74.0 * u));
    let ce = prog(t, 0.95, 0.5);
    p.rect_filled(co.translate(vec2(0.0, (1.0 - ce) * 14.0 * u)), Rounding::same(18.0 * u), a(c.secondary_container, al * ce));
    p.rect_filled(Rect::from_min_size(co.min + vec2(14.0 * u, 16.0 * u + (1.0 - ce) * 14.0 * u), vec2(5.0 * u, 42.0 * u)), Rounding::same(3.0 * u), a(c.accent, al * ce));
    text(p, co.min + vec2(34.0 * u, 20.0 * u + (1.0 - ce) * 14.0 * u), Align2::LEFT_TOP, "Key idea", fonts::bold(14.0 * u), a(c.on_secondary_container, al * ce));
    bar(p, co.min.x + 34.0 * u, co.min.y + 46.0 * u + (1.0 - ce) * 14.0 * u, co.width() - 60.0 * u, 8.0 * u, a(c.on_secondary_container.gamma_multiply(0.45), al * ce), 1.0);
    // equation chip
    let ee = prog(t, 1.3, 0.5);
    let eq = Rect::from_min_size(pos2(r.min.x, co.max.y + 16.0 * u + (1.0 - ee) * 12.0 * u), vec2(168.0 * u, 40.0 * u));
    pill(p, eq, a(c.field, al * ee), Some(a(c.hairline, al * ee)));
    text(p, eq.center(), Align2::CENTER_CENTER, "s = ut + ½at²", fonts::medium(16.0 * u), a(c.ink, al * ee));
}

fn practice(ui: &Ui, th: &Theme, r: Rect, u: f32, t: f32, al: f32) {
    let p = ui.painter();
    let c = &th.p;
    text(p, r.min, Align2::LEFT_TOP, "Question 3", fonts::medium(13.5 * u), a(c.ink_muted, al));
    // score
    let sc = Rect::from_min_size(pos2(r.max.x - 76.0 * u, r.min.y - 4.0 * u), vec2(76.0 * u, 26.0 * u));
    pill(p, sc, a(c.accent_soft, al), None);
    let shown = if t > 1.6 { 3 } else { 2 };
    text(p, sc.center(), Align2::CENTER_CENTER, &format!("{shown} / 4"), fonts::bold(13.0 * u), a(c.on_accent_soft, al));
    text(p, r.min + vec2(0.0, 30.0 * u), Align2::LEFT_TOP, "Which unit measures force?", fonts::bold(21.0 * u), a(c.ink, al * prog(t, 0.05, 0.5)));
    let opts = ["Joule", "Newton", "Watt", "Pascal"];
    let correct = 1;
    let sel = prog(t, 1.2, 0.35);
    for (k, o) in opts.iter().enumerate() {
        let e = prog(t, 0.25 + 0.12 * k as f32, 0.45);
        let y = r.min.y + 84.0 * u + k as f32 * 54.0 * u + (1.0 - e) * 18.0 * u;
        let row = Rect::from_min_size(pos2(r.min.x, y), vec2(r.width(), 44.0 * u));
        let hit = k == correct;
        let fill = if hit { mix(c.field, c.ok_soft, sel) } else { c.field };
        let stroke = if hit { mix(c.hairline, c.ok, sel) } else { c.hairline };
        p.rect(row, Rounding::same(22.0 * u), a(fill, al * e), Stroke::new((1.0 + sel * f32::from(hit)) * 1.0_f32, a(stroke, al * e)));
        let badge = Rect::from_center_size(pos2(row.min.x + 24.0 * u, row.center().y), vec2(26.0 * u, 26.0 * u));
        p.circle_filled(badge.center(), 13.0 * u, a(if hit { mix(c.card, c.ok, sel) } else { c.card }, al * e));
        text(p, badge.center(), Align2::CENTER_CENTER, &((b'A' + k as u8) as char).to_string(), fonts::bold(12.5 * u), a(if hit && sel > 0.5 { c.on_accent } else { c.ink_muted }, al * e));
        text(p, pos2(row.min.x + 50.0 * u, row.center().y), Align2::LEFT_CENTER, o, fonts::medium(15.5 * u), a(c.ink, al * e));
        if hit && sel > 0.05 {
            icons::paint(p, Rect::from_center_size(pos2(row.max.x - 24.0 * u, row.center().y), vec2(22.0 * u * sel, 22.0 * u * sel)), Icon::Check, a(c.ok, al));
        }
    }
}

fn search(ui: &Ui, th: &Theme, r: Rect, u: f32, t: f32, al: f32) {
    let p = ui.painter();
    let c = &th.p;
    let bar_r = Rect::from_min_size(r.min, vec2(r.width(), 48.0 * u));
    pill(p, bar_r, a(c.field, al), Some(a(c.accent, al)));
    icons::paint(p, Rect::from_center_size(pos2(bar_r.min.x + 26.0 * u, bar_r.center().y), vec2(22.0 * u, 22.0 * u)), Icon::Search, a(c.accent, al));
    let word = "projectile";
    let n = ((t - 0.3) * 9.0).clamp(0.0, word.len() as f32) as usize;
    let typed = &word[..n];
    let tx = pos2(bar_r.min.x + 50.0 * u, bar_r.center().y);
    let g = p.layout_no_wrap(typed.to_owned(), fonts::regular(16.0 * u), a(c.ink, al));
    let w = g.size().x;
    p.galley(pos2(tx.x, tx.y - g.size().y / 2.0), g, c.ink);
    if (t * 2.2).fract() < 0.6 {
        p.rect_filled(Rect::from_min_size(pos2(tx.x + w + 2.0 * u, tx.y - 10.0 * u), vec2(2.0 * u, 20.0 * u)), 1.0, a(c.accent, al));
    }
    let hits = [("Physics", "Projectile motion", c.violet), ("Mathematics", "Parabola and its properties", c.warn), ("Physics", "Motion in two dimensions", c.violet)];
    for (k, (sub, title, col)) in hits.iter().enumerate() {
        let e = prog(t, 1.2 + 0.16 * k as f32, 0.5);
        let y = bar_r.max.y + 18.0 * u + k as f32 * 64.0 * u + (1.0 - e) * 16.0 * u;
        let row = Rect::from_min_size(pos2(r.min.x, y), vec2(r.width(), 54.0 * u));
        p.rect(row, Rounding::same(20.0 * u), a(c.card, al * e), Stroke::new(1.0_f32, a(c.hairline, al * e)));
        let sq = Rect::from_center_size(pos2(row.min.x + 30.0 * u, row.center().y), vec2(34.0 * u, 34.0 * u));
        p.rect_filled(sq, Rounding::same(11.0 * u), a(mix(c.card, *col, 0.2), al * e));
        text(p, sq.center(), Align2::CENTER_CENTER, &sub[..1], fonts::bold(15.0 * u), a(*col, al * e));
        text(p, pos2(row.min.x + 56.0 * u, row.center().y - 9.0 * u), Align2::LEFT_CENTER, title, fonts::medium(14.5 * u), a(c.ink, al * e));
        text(p, pos2(row.min.x + 56.0 * u, row.center().y + 11.0 * u), Align2::LEFT_CENTER, sub, fonts::regular(12.0 * u), a(c.ink_muted, al * e));
    }
}

fn offline(ui: &Ui, th: &Theme, r: Rect, u: f32, t: f32, al: f32) {
    let p = ui.painter();
    let c = &th.p;
    let items = [("Physics", "Class 11", 0.0, 2.6, c.violet), ("Chemistry", "Class 12", 0.5, 3.4, c.teal), ("Mathematics", "Class 10", 1.0, 4.2, c.warn)];
    for (k, (name, lvl, delay, dur, col)) in items.iter().enumerate() {
        let e = prog(t, 0.1 * k as f32, 0.5);
        let y = r.min.y + k as f32 * 94.0 * u + (1.0 - e) * 18.0 * u;
        let row = Rect::from_min_size(pos2(r.min.x, y), vec2(r.width(), 80.0 * u));
        p.rect(row, Rounding::same(24.0 * u), a(c.card, al * e), Stroke::new(1.0_f32, a(c.hairline, al * e)));
        let sq = Rect::from_center_size(pos2(row.min.x + 38.0 * u, row.center().y), vec2(44.0 * u, 44.0 * u));
        p.rect_filled(sq, Rounding::same(14.0 * u), a(mix(c.card, *col, 0.2), al * e));
        text(p, sq.center(), Align2::CENTER_CENTER, &name[..1], fonts::bold(19.0 * u), a(*col, al * e));
        text(p, pos2(row.min.x + 74.0 * u, row.min.y + 24.0 * u), Align2::LEFT_CENTER, name, fonts::bold(15.5 * u), a(c.ink, al * e));
        text(p, pos2(row.min.x + 74.0 * u, row.min.y + 44.0 * u), Align2::LEFT_CENTER, lvl, fonts::regular(12.0 * u), a(c.ink_muted, al * e));
        let f = (((t - 0.6 - delay) / dur).clamp(0.0, 1.0)).powf(0.8);
        let track = Rect::from_min_size(pos2(row.min.x + 74.0 * u, row.max.y - 20.0 * u), vec2(row.width() - 74.0 * u - 62.0 * u, 7.0 * u));
        p.rect_filled(track, Rounding::same(4.0 * u), a(c.field, al * e));
        if f > 0.0 {
            p.rect_filled(Rect::from_min_size(track.min, vec2(track.width() * f, track.height())), Rounding::same(4.0 * u), a(*col, al * e));
        }
        let done = f >= 1.0;
        let badge = Rect::from_center_size(pos2(row.max.x - 30.0 * u, row.center().y), vec2(36.0 * u, 36.0 * u));
        p.circle_filled(badge.center(), 18.0 * u, a(if done { c.ok_soft } else { c.field }, al * e));
        icons::paint(p, Rect::from_center_size(badge.center(), vec2(20.0 * u, 20.0 * u)), if done { Icon::Check } else { Icon::Download }, a(if done { c.ok } else { c.ink_muted }, al * e));
    }
}

/// A floating tag that overlaps a scene corner.
pub fn tag(ui: &Ui, th: &Theme, centre: egui::Pos2, icon: Icon, label: &str, alpha: f32, bob: f32) {
    let p = ui.painter();
    let g = p.layout_no_wrap(label.to_owned(), fonts::medium(13.5), a(th.p.on_secondary_container, alpha));
    let w = g.size().x + 54.0;
    let r = Rect::from_center_size(centre + vec2(0.0, bob), vec2(w, 40.0));
    pill(p, r, a(th.p.secondary_container, alpha), Some(a(th.p.hairline, alpha)));
    icons::paint(p, Rect::from_center_size(pos2(r.min.x + 22.0, r.center().y), vec2(20.0, 20.0)), icon, a(th.p.on_secondary_container, alpha));
    p.galley(pos2(r.min.x + 38.0, r.center().y - g.size().y / 2.0), g, th.p.on_secondary_container);
}
