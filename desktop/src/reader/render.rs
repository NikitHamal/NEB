//! Paints a parsed chapter with native egui widgets.
use std::collections::HashMap;

use egui::text::{LayoutJob, TextFormat};
use egui::{
    vec2, Align, Color32, CursorIcon, FontFamily, FontId, Frame, Label, Layout, Margin, Rect, RichText, Rounding, Sense, Shape, Stroke, TextWrapMode, Ui,
};

use super::model::*;
use crate::actions::Action;
use crate::data::content::ContentRoot;
use crate::theme::{fonts, mix, Theme};
use crate::ui::icons::{self, Icon};

pub struct RenderCx<'a> {
    pub th: &'a Theme,
    /// Reading text scale (Settings ▸ text size).
    pub scale: f32,
    pub content: Option<&'a ContentRoot>,
    /// Heading id the TOC asked us to scroll to.
    pub jump: &'a mut Option<String>,
    /// (heading id, screen y) of every heading drawn this frame — drives TOC highlighting.
    pub heads: &'a mut Vec<(String, f32)>,
    /// Selected option per MCQ index.
    pub mcq: &'a mut HashMap<usize, char>,
    pub mcq_idx: usize,
    pub uid: u64,
    pub actions: &'a mut Vec<Action>,
}

impl RenderCx<'_> {
    fn next_uid(&mut self) -> u64 {
        self.uid += 1;
        self.uid
    }
}

const BODY: f32 = 16.5;

pub fn layout(cx: &RenderCx, spans: &[Span], size: f32, color: Color32, bold: bool, halign: Align) -> LayoutJob {
    let th = cx.th;
    let mut job = LayoutJob::default();
    job.halign = halign;
    let size = size * cx.scale;
    for s in spans {
        let mut fsize = size;
        let mut fam = if bold || s.bold { fonts::bold_family() } else { FontFamily::Proportional };
        let mut col = color;
        let mut fmt = TextFormat { italics: s.italic, ..Default::default() };
        if s.code {
            fam = FontFamily::Monospace;
            fsize *= 0.9;
            fmt.background = th.p.field;
            col = th.p.ink;
        }
        if s.sup || s.sub {
            fsize *= 0.72;
            fmt.valign = if s.sup { Align::TOP } else { Align::BOTTOM };
        }
        if s.marks {
            fsize *= 0.82;
            col = th.p.ink_faint;
        }
        if s.math && s.italic && !s.bold {
            col = mix(col, th.p.accent, if th.dark { 0.0 } else { 0.0 });
        }
        if s.link.is_some() {
            col = th.p.accent;
            fmt.underline = Stroke::new(1.0, th.p.accent);
        }
        if s.underline {
            fmt.underline = Stroke::new(1.0, col);
        }
        fmt.font_id = FontId::new(fsize, fam);
        fmt.color = col;
        job.append(&s.text, 0.0, fmt);
    }
    job
}

fn box_style(th: &Theme, kind: &str) -> (Color32, Color32, &'static str) {
    let p = &th.p;
    match kind {
        "key" => (p.accent, p.accent_soft, "Key points"),
        "definition" => (p.violet, p.violet_soft, "Definition"),
        "example" => (p.teal, p.teal_soft, "Worked example"),
        "caution" => (p.danger, p.danger_soft, "Caution"),
        "tip" => (p.ok, p.ok_soft, "Tip"),
        "derivation" => (p.accent, p.field, "Derivation"),
        "memory" => (p.warn, p.warn_soft, "Memory aid"),
        _ => (p.ink_muted, p.field, "Note"),
    }
}

pub fn blocks(ui: &mut Ui, cx: &mut RenderCx, list: &[Block]) {
    for b in list {
        block(ui, cx, b);
    }
}

fn gap(ui: &mut Ui, cx: &RenderCx, v: f32) {
    ui.add_space(v * cx.scale.sqrt());
}

fn para(ui: &mut Ui, cx: &mut RenderCx, spans: &[Span], size: f32, color: Color32, bold: bool) {
    let job = layout(cx, spans, size, color, bold, Align::LEFT);
    let link = spans.iter().find_map(|s| s.link.clone());
    let resp = ui.add(Label::new(job).sense(if link.is_some() { Sense::click() } else { Sense::hover() }));
    if let Some(url) = link {
        if resp.hovered() {
            ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
        }
        if resp.clicked() {
            cx.actions.push(Action::OpenUrl(url));
        }
    }
}

fn block(ui: &mut Ui, cx: &mut RenderCx, b: &Block) {
    let th = cx.th;
    match b {
        Block::Heading { level, id, spans } => {
            let (size, before, after) = match level {
                1 | 2 => (24.0, 22.0, 8.0),
                3 => (19.5, 14.0, 4.0),
                _ => (16.5, 10.0, 2.0),
            };
            gap(ui, cx, before);
            let job = layout(cx, spans, size, th.p.ink, true, Align::LEFT);
            let r = ui.add(Label::new(job));
            if !id.is_empty() {
                cx.heads.push((id.clone(), r.rect.top()));
                if cx.jump.as_deref() == Some(id.as_str()) {
                    ui.scroll_to_rect(r.rect.expand2(vec2(0.0, 14.0)), Some(Align::TOP));
                    *cx.jump = None;
                }
            }
            if *level <= 2 {
                ui.add_space(4.0);
                let (rect, _) = ui.allocate_exact_size(vec2(ui.available_width(), 1.0), Sense::hover());
                ui.painter().rect_filled(rect, 0.0, th.p.hairline);
            }
            gap(ui, cx, after);
        }
        Block::Para(spans) => {
            para(ui, cx, spans, BODY, th.p.ink, false);
            gap(ui, cx, 9.0);
        }
        Block::Math(spans) => {
            let w = ui.available_width();
            Frame::none().fill(th.p.field).rounding(Rounding::same(10.0)).inner_margin(Margin::symmetric(14.0, 10.0)).show(ui, |ui| {
                ui.set_width(w - 28.0);
                ui.vertical_centered(|ui| {
                    let job = layout(cx, spans, BODY + 1.0, th.p.ink, false, Align::Center);
                    ui.add(Label::new(job));
                });
            });
            gap(ui, cx, 10.0);
        }
        Block::Box { kind, title, blocks: inner } => {
            let (fg, bg, kind_label) = box_style(th, kind);
            let w = ui.available_width();
            let r = Frame::none().fill(bg).rounding(Rounding::same(12.0)).inner_margin(Margin { left: 20.0, right: 16.0, top: 12.0, bottom: 6.0 }).show(ui, |ui| {
                ui.set_width(w - 36.0);
                ui.horizontal_wrapped(|ui| {
                    ui.spacing_mut().item_spacing.x = 8.0;
                    ui.add(Label::new(RichText::new(kind_label.to_uppercase()).font(fonts::bold(11.5)).color(fg)).selectable(false));
                    if let Some(t) = title {
                        let job = layout(cx, t, 15.5, fg, true, Align::LEFT);
                        ui.add(Label::new(job));
                    }
                });
                ui.add_space(4.0);
                blocks(ui, cx, inner);
            });
            let rect = r.response.rect;
            ui.painter().rect_filled(
                Rect::from_min_size(rect.min, vec2(4.0, rect.height())),
                Rounding { nw: 12.0, sw: 12.0, ne: 0.0, se: 0.0 },
                fg,
            );
            gap(ui, cx, 8.0);
        }
        Block::List { ordered, items } => {
            for (i, item) in items.iter().enumerate() {
                ui.horizontal_top(|ui| {
                    ui.spacing_mut().item_spacing.x = 6.0;
                    let mark = if *ordered { format!("{}.", i + 1) } else { "•".to_string() };
                    ui.allocate_ui_with_layout(vec2(26.0, 0.0), Layout::right_to_left(Align::Min), |ui| {
                        ui.add(Label::new(RichText::new(mark).font(fonts::bold(BODY * cx.scale)).color(th.p.ink_muted)).selectable(false));
                    });
                    ui.vertical(|ui| {
                        ui.spacing_mut().item_spacing.y = 4.0;
                        blocks(ui, cx, item);
                    });
                });
                ui.add_space(3.0);
            }
            gap(ui, cx, 6.0);
        }
        Block::Table { head, rows } => {
            table(ui, cx, head, rows);
            gap(ui, cx, 12.0);
        }
        Block::Figure { src, caption, width_pct } => {
            figure(ui, cx, src, caption, *width_pct);
            gap(ui, cx, 12.0);
        }
        Block::Code { lang, text } => {
            let uid = cx.next_uid();
            Frame::none().fill(th.p.field).rounding(Rounding::same(10.0)).inner_margin(Margin::same(12.0)).show(ui, |ui| {
                ui.set_width(ui.available_width() - 24.0);
                if lang != "text" {
                    ui.add(Label::new(RichText::new(lang.to_uppercase()).font(fonts::medium(11.0)).color(th.p.ink_faint)).selectable(false));
                }
                ui.push_id(uid, |ui| {
                    egui::ScrollArea::horizontal().auto_shrink([false, true]).show(ui, |ui| {
                        ui.add(Label::new(RichText::new(text).monospace().size(13.5 * cx.scale)).wrap_mode(TextWrapMode::Extend));
                    });
                });
            });
            gap(ui, cx, 10.0);
        }
        Block::Quote(inner) => {
            let w = ui.available_width();
            let r = Frame::none().inner_margin(Margin { left: 18.0, right: 4.0, top: 2.0, bottom: 2.0 }).show(ui, |ui| {
                ui.set_width(w - 22.0);
                blocks(ui, cx, inner);
            });
            let rect = r.response.rect;
            ui.painter().rect_filled(Rect::from_min_size(rect.min, vec2(3.0, rect.height())), Rounding::same(2.0), th.p.hairline_strong);
        }
        Block::Rule => {
            gap(ui, cx, 6.0);
            let (rect, _) = ui.allocate_exact_size(vec2(ui.available_width(), 1.0), Sense::hover());
            ui.painter().rect_filled(rect, 0.0, th.p.hairline_strong);
            gap(ui, cx, 10.0);
        }
        Block::Details { summary, blocks: inner } => {
            let uid = cx.next_uid();
            let title = {
                let t = plain_text(summary);
                if t.is_empty() { "Show answer".to_string() } else { t }
            };
            ui.push_id(uid, |ui| {
                egui::CollapsingHeader::new(RichText::new(title).font(fonts::medium(14.5)).color(th.p.accent)).default_open(false).show(ui, |ui| {
                    ui.add_space(2.0);
                    blocks(ui, cx, inner);
                });
            });
            gap(ui, cx, 8.0);
        }
        Block::Mcq(items) => {
            for item in items {
                mcq_item(ui, cx, item);
                ui.add_space(10.0);
            }
        }
        Block::Group(inner) => blocks(ui, cx, inner),
    }
}

fn table(ui: &mut Ui, cx: &RenderCx, head: &[Vec<Span>], rows: &[Vec<Vec<Span>>]) {
    let th = cx.th;
    let n = rows.iter().map(|r| r.len()).chain(std::iter::once(head.len())).max().unwrap_or(0);
    if n == 0 {
        return;
    }
    let total = ui.available_width() - 2.0;
    let weights: Vec<f32> = (0..n)
        .map(|c| {
            let longest = rows
                .iter()
                .map(|r| r.get(c).map(|s| plain_text(s).chars().count()).unwrap_or(0))
                .chain(std::iter::once(head.get(c).map(|s| plain_text(s).chars().count()).unwrap_or(0)))
                .max()
                .unwrap_or(1);
            longest.clamp(6, 42) as f32
        })
        .collect();
    let sum: f32 = weights.iter().sum();
    let widths: Vec<f32> = weights.iter().map(|w| total * w / sum).collect();

    let mut draw_row = |ui: &mut Ui, cells: &[Vec<Span>], header: bool, idx: usize| {
        let bg = ui.painter().add(Shape::Noop);
        let resp = ui.horizontal_top(|ui| {
            ui.spacing_mut().item_spacing.x = 0.0;
            for (c, w) in widths.iter().enumerate() {
                ui.allocate_ui_with_layout(vec2(*w, 0.0), Layout::top_down(Align::Min), |ui| {
                    ui.set_width(*w);
                    Frame::none().inner_margin(Margin::symmetric(10.0, 7.0)).show(ui, |ui| {
                        ui.set_width(*w - 20.0);
                        if let Some(spans) = cells.get(c) {
                            let job = layout(cx, spans, 14.5, th.p.ink, header, Align::LEFT);
                            ui.add(Label::new(job));
                        }
                    });
                });
            }
        });
        let rect = resp.response.rect;
        let fill = if header {
            th.p.accent_soft
        } else if idx % 2 == 1 {
            th.p.field.gamma_multiply(0.6)
        } else {
            Color32::TRANSPARENT
        };
        ui.painter().set(bg, Shape::rect_filled(rect, 0.0, fill));
        ui.painter().hline(rect.x_range(), rect.bottom(), Stroke::new(1.0, th.p.hairline));
    };
    ui.spacing_mut().item_spacing.y = 0.0;
    let start = ui.cursor().min;
    if !head.is_empty() {
        draw_row(ui, head, true, 0);
    }
    for (i, r) in rows.iter().enumerate() {
        draw_row(ui, r, false, i);
    }
    let end = ui.cursor().min;
    let outline = Rect::from_min_max(start, egui::pos2(start.x + total, end.y));
    ui.painter().rect_stroke(outline, Rounding::same(8.0), Stroke::new(1.0, th.p.hairline_strong));
    ui.spacing_mut().item_spacing.y = 8.0;
}

fn figure(ui: &mut Ui, cx: &mut RenderCx, src: &str, caption: &[Span], pct: Option<f32>) {
    let th = cx.th;
    let avail = ui.available_width();
    let max_w = (avail * pct.unwrap_or(100.0).clamp(20.0, 100.0) / 100.0).min(avail).min(760.0);
    ui.vertical_centered(|ui| {
        Frame::none().fill(Color32::WHITE).rounding(Rounding::same(10.0)).stroke(Stroke::new(1.0, th.p.hairline)).inner_margin(Margin::same(10.0)).show(ui, |ui| {
            match cx.content.and_then(|c| c.asset_uri(src)) {
                Some(uri) => {
                    ui.add(egui::Image::new(uri).fit_to_original_size(1.3).max_width((max_w - 20.0).max(80.0)));
                }
                None => {
                    ui.add(Label::new(RichText::new("Figure not available offline").color(Color32::GRAY)).selectable(false));
                }
            }
        });
        if !caption.is_empty() {
            ui.add_space(6.0);
            ui.set_max_width(max_w.max(320.0));
            let job = layout(cx, caption, 13.5, th.p.ink_muted, false, Align::Center);
            ui.add(Label::new(job));
        }
    });
}

fn mcq_item(ui: &mut Ui, cx: &mut RenderCx, item: &McqItem) {
    let th = cx.th;
    let idx = cx.mcq_idx;
    cx.mcq_idx += 1;
    let chosen = cx.mcq.get(&idx).copied();
    let w = ui.available_width();
    ui.push_id(("mcq", idx), |ui| {
        Frame::none().fill(th.p.card).stroke(Stroke::new(1.0, th.p.hairline_strong)).rounding(Rounding::same(12.0)).inner_margin(Margin::same(14.0)).show(ui, |ui| {
            ui.set_width(w - 28.0);
            ui.horizontal_top(|ui| {
                ui.spacing_mut().item_spacing.x = 8.0;
                ui.allocate_ui_with_layout(vec2(30.0, 0.0), Layout::right_to_left(Align::Min), |ui| {
                    ui.add(Label::new(RichText::new(format!("{}.", idx + 1)).font(fonts::bold(BODY * cx.scale)).color(th.p.accent)).selectable(false));
                });
                ui.vertical(|ui| {
                    let mut spans = item.question.clone();
                    if let Some(m) = &item.marks {
                        spans.push(Span::plain(" "));
                        spans.push(Span { text: m.clone(), marks: true, ..Default::default() });
                    }
                    let job = layout(cx, &spans, BODY, th.p.ink, false, Align::LEFT);
                    ui.add(Label::new(job));
                });
            });
            ui.add_space(8.0);
            let cols = if item.cols >= 2 && item.options.len() >= 2 && ui.available_width() > 460.0 { 2 } else { 1 };
            let gapx = 8.0;
            let colw = (ui.available_width() - gapx * (cols as f32 - 1.0)) / cols as f32;
            for row in item.options.chunks(cols) {
                ui.horizontal_top(|ui| {
                    ui.spacing_mut().item_spacing.x = gapx;
                    for (label, spans) in row {
                        option(ui, cx, idx, item.key, *label, spans, chosen, colw);
                    }
                });
                ui.add_space(6.0);
            }
            if let Some(c) = chosen {
                let (txt, col) = if c == item.key {
                    ("Correct".to_string(), th.p.ok)
                } else {
                    (format!("Not quite — the answer is {}.", item.key), th.p.danger)
                };
                ui.add(Label::new(RichText::new(txt).font(fonts::medium(13.5)).color(col)).selectable(false));
            }
        });
    });
}

#[allow(clippy::too_many_arguments)]
fn option(ui: &mut Ui, cx: &mut RenderCx, idx: usize, key: char, label: char, spans: &[Span], chosen: Option<char>, width: f32) {
    let th = cx.th;
    // 0 neutral, 1 correct, 2 wrong, 3 dimmed
    let state = match chosen {
        None => 0,
        Some(_) if label == key => 1,
        Some(c) if c == label => 2,
        Some(_) => 3,
    };
    let (fill, stroke, badge_bg, badge_fg) = match state {
        1 => (th.p.ok_soft, th.p.ok, th.p.ok, th.p.page),
        2 => (th.p.danger_soft, th.p.danger, th.p.danger, th.p.page),
        3 => (th.p.card, th.p.hairline, th.p.field, th.p.ink_faint),
        _ => (th.p.card, th.p.hairline_strong, th.p.field, th.p.ink_muted),
    };
    let r = Frame::none().fill(fill).stroke(Stroke::new(1.0, stroke)).rounding(Rounding::same(10.0)).inner_margin(Margin::symmetric(10.0, 7.0)).show(ui, |ui| {
        ui.set_width(width - 22.0);
        ui.horizontal_top(|ui| {
            ui.spacing_mut().item_spacing.x = 10.0;
            let (rect, _) = ui.allocate_exact_size(vec2(24.0, 24.0), Sense::hover());
            ui.painter().circle_filled(rect.center(), 12.0, badge_bg);
            match state {
                1 => icons::paint(ui.painter(), Rect::from_center_size(rect.center(), vec2(14.0, 14.0)), Icon::Check, badge_fg),
                2 => icons::paint(ui.painter(), Rect::from_center_size(rect.center(), vec2(12.0, 12.0)), Icon::Close, badge_fg),
                _ => {
                    ui.painter().text(rect.center(), egui::Align2::CENTER_CENTER, label.to_ascii_uppercase(), fonts::bold(12.0), badge_fg);
                }
            }
            let col = if state == 3 { th.p.ink_muted } else { th.p.ink };
            let mut job = layout(cx, spans, 15.0, col, false, Align::LEFT);
            if job.sections.is_empty() {
                job.append("—", 0.0, TextFormat::default());
            }
            ui.add(Label::new(job).selectable(false));
        });
    });
    let id = ui.id().with(("opt", idx, label));
    let resp = ui.interact(r.response.rect, id, Sense::click());
    if chosen.is_none() {
        if resp.hovered() {
            ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
            ui.painter().rect_filled(r.response.rect, Rounding::same(10.0), th.p.accent.gamma_multiply(0.07));
        }
        if resp.has_focus() {
            ui.painter().rect_stroke(r.response.rect.expand(2.0), Rounding::same(12.0), Stroke::new(2.0, th.p.accent));
        }
        if resp.clicked() {
            cx.mcq.insert(idx, label);
        }
    }
}
