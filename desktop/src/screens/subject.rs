//! Subject screen: header + progress, then Units / Question banks / Syllabus tabs
//! built from `syllabus/<track>-<subject>.json` and `study/<dir>/index.json`.
use egui::{vec2, Frame, Margin, RichText, Rounding, Sense, Ui};

use super::common::*;
use crate::actions::Action;
use crate::data::models::{ChapterKind, ChapterRef};
use crate::env::Env;
use crate::theme::{fonts, spacing};
use crate::ui::icons::{self, Icon};
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct SubjectState {
    tab: usize,
    last: Option<(String, String)>,
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut SubjectState, track: &str, subject: &str) {
    let key = (track.to_string(), subject.to_string());
    if st.last.as_ref() != Some(&key) {
        st.last = Some(key);
        st.tab = 0;
    }
    let (track, subject) = (track.to_string(), subject.to_string());
    scroll_page(ui, env, &format!("subject-{track}-{subject}"), |ui, env| {
        let th = env.theme.clone();
        let (Some(sum), Some(track_info)) = (env.subject(&track, &subject).cloned(), env.track(&track).cloned()) else {
            widgets::empty_state(ui, &th, Icon::Library, "Subject not found", "Pick one from the Library.");
            return;
        };
        let syl = env.syllabus(&track, &subject);
        let idx = env.study_index(&track, &subject);
        let color = th.subject_color(&sum.color);
        let done = env.store.done_count_in(&track, &subject);
        let ready: Vec<u32> = idx.as_ref().map(|i| i.units.iter().map(|u| u.no).collect()).unwrap_or_default();

        ui.horizontal(|ui| {
            if widgets::icon_button(ui, &th, Icon::Back, "Back", false).clicked() {
                env.act(Action::Back);
            }
            ui.add(egui::Label::new(RichText::new(format!("{} › {}", track_info.label, env.subject_name(&sum))).font(fonts::regular(13.0)).color(th.p.ink_muted)).selectable(false));
        });
        ui.add_space(6.0);

        let w = ui.available_width();
        Frame::none().fill(th.wash(color)).rounding(Rounding::same(spacing::PANEL_RADIUS)).inner_margin(Margin::same(22.0)).show(ui, |ui| {
            ui.set_width(w - 44.0);
            ui.horizontal(|ui| {
                widgets::subject_badge(ui, &th, &sum.name, &sum.color, 68.0);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 2.0;
                    widgets::label(ui, RichText::new(env.subject_name(&sum)).font(fonts::bold(26.0)).color(th.p.ink));
                    if !sum.name_ne.is_empty() {
                        let alt = if env.store.s.prefs.nepali_names { &sum.name } else { &sum.name_ne };
                        widgets::label(ui, RichText::new(alt).font(fonts::regular(14.0)).color(th.p.ink_muted));
                    }
                });
            });
            ui.add_space(12.0);
            ui.horizontal_wrapped(|ui| {
                widgets::badge(ui, &format!("{} chapters", sum.notes_ready), color, th.p.card);
                widgets::badge(ui, &format!("{} topics", sum.topic_count), th.p.ink_muted, th.p.card);
                if let Some(h) = sum.hours.filter(|h| *h > 0) {
                    widgets::badge(ui, &format!("{h} hours"), th.p.ink_muted, th.p.card);
                }
                if let Some(s) = &syl {
                    if !s.code.is_empty() {
                        widgets::badge(ui, &s.code, th.p.ink_muted, th.p.card);
                    }
                }
            });
            ui.add_space(14.0);
            widgets::progress_bar(ui, &th, if sum.unit_count > 0 { done as f32 / sum.unit_count as f32 } else { 0.0 }, 6.0, Some(color));
            ui.add_space(6.0);
            widgets::label(ui, RichText::new(format!("{done} of {} chapters finished", sum.unit_count)).font(fonts::regular(12.5)).color(th.p.ink_muted));
            ui.add_space(12.0);
            ui.horizontal_wrapped(|ui| {
                let resume = env.store.s.recent.iter().find(|r| r.chapter.track == track && r.chapter.subject == subject).map(|r| r.chapter.clone());
                let first = ready.first().copied().map(|n| unit_ref(&track, &subject, n));
                if let Some(c) = resume.clone().or(first.clone()) {
                    let label = if resume.is_some() { "Continue reading" } else { "Start first chapter" };
                    if widgets::button(ui, &th, label, BtnKind::Primary, Some(Icon::Play), None).clicked() {
                        open_chapter(env, c);
                    }
                }
                if let Some(i) = &idx {
                    if !i.guide.is_empty() && widgets::button(ui, &th, "Exam guide", BtnKind::Secondary, Some(Icon::File), None).clicked() {
                        open_chapter(env, ChapterRef::new(&track, &subject, ChapterKind::Guide, 0));
                    }
                }
            });
        });
        ui.add_space(20.0);

        let n_banks = idx.as_ref().map(|i| i.banks.len() + usize::from(!i.guide.is_empty())).unwrap_or(0);
        ui.horizontal_wrapped(|ui| {
            for (i, label) in [format!("Units ({})", syl.as_ref().map(|s| s.units.len()).unwrap_or(0)), format!("Question banks ({n_banks})"), "Syllabus".to_string()].iter().enumerate() {
                if widgets::chip(ui, &th, label, st.tab == i).clicked() {
                    st.tab = i;
                }
            }
        });
        ui.add_space(14.0);

        match st.tab {
            0 => units_tab(ui, env, &track, &subject, syl.as_deref(), idx.as_deref(), &ready, color),
            1 => banks_tab(ui, env, &track, &subject, idx.as_deref()),
            _ => syllabus_tab(ui, env, syl.as_deref()),
        }
    });
}

#[allow(clippy::too_many_arguments)]
fn units_tab(ui: &mut Ui, env: &mut Env, track: &str, subject: &str, syl: Option<&crate::data::models::Syllabus>, idx: Option<&crate::data::models::StudyIndex>, ready: &[u32], color: egui::Color32) {
    let th = env.theme.clone();
    let Some(syl) = syl else {
        widgets::empty_state(ui, &th, Icon::List, "No syllabus data", "This subject has no syllabus file yet.");
        return;
    };
    for u in &syl.units {
        let meta = idx.and_then(|i| i.units.iter().find(|m| m.no == u.no));
        let available = ready.contains(&u.no);
        let c = unit_ref(track, subject, u.no);
        let prog = env.store.progress(&c).cloned();
        let w = ui.available_width();
        let resp = widgets::card(ui, &th, vec2(w, 84.0), 14.0, |ui| {
            ui.horizontal(|ui| {
                let (rect, _) = ui.allocate_exact_size(vec2(44.0, 44.0), Sense::hover());
                let finished = prog.as_ref().is_some_and(|p| p.done);
                ui.painter().rect_filled(rect, 12.0, if finished { th.p.ok_soft } else { th.wash(color) });
                if finished {
                    icons::paint(ui.painter(), egui::Rect::from_center_size(rect.center(), vec2(20.0, 20.0)), Icon::Check, th.p.ok);
                } else {
                    ui.painter().text(rect.center(), egui::Align2::CENTER_CENTER, u.no.to_string(), fonts::bold(16.0), color);
                }
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 2.0;
                    widgets::label_trunc(ui, RichText::new(&u.title).font(fonts::bold(15.0)).color(if available { th.p.ink } else { th.p.ink_faint }));
                    let mut parts = vec![];
                    if !u.area.is_empty() {
                        parts.push(u.area.clone());
                    }
                    if let Some(h) = u.hours.filter(|h| *h > 0) {
                        parts.push(format!("{h} h"));
                    }
                    if let Some(m) = meta {
                        parts.push(format!("{} min read", m.read_min));
                        if m.figures > 0 {
                            parts.push(format!("{} figures", m.figures));
                        }
                    }
                    if !available {
                        parts.push("coming soon".to_string());
                    }
                    widgets::label_trunc(ui, RichText::new(parts.join("  ·  ")).font(fonts::regular(12.5)).color(th.p.ink_muted));
                    let topics = u.topics.iter().take(2).cloned().collect::<Vec<_>>().join(" · ");
                    if !topics.is_empty() {
                        widgets::label_trunc(ui, RichText::new(topics).font(fonts::regular(12.0)).color(th.p.ink_faint));
                    }
                });
            });
        });
        if resp.clicked() && available {
            open_chapter(env, c);
        } else if resp.clicked() {
            env.toast("This chapter is not published yet");
        }
        ui.add_space(8.0);
    }
}

fn banks_tab(ui: &mut Ui, env: &mut Env, track: &str, subject: &str, idx: Option<&crate::data::models::StudyIndex>) {
    let th = env.theme.clone();
    let Some(idx) = idx.filter(|i| !i.banks.is_empty() || !i.guide.is_empty()) else {
        widgets::empty_state(ui, &th, Icon::File, "No question banks", "Practice questions live inside each chapter for this subject.");
        return;
    };
    let mut rows: Vec<(ChapterRef, String, String, u32)> = vec![];
    if !idx.guide.is_empty() {
        rows.push((ChapterRef::new(track, subject, ChapterKind::Guide, 0), idx.guide.clone(), "Exam guide".into(), 0));
    }
    for b in &idx.banks {
        rows.push((ChapterRef::new(track, subject, ChapterKind::Bank, b.no), b.title.clone(), b.kind.clone(), b.read_min));
    }
    for (c, title, kind, mins) in rows {
        let w = ui.available_width();
        let resp = widgets::card(ui, &th, vec2(w, 74.0), 14.0, |ui| {
            ui.horizontal(|ui| {
                let (rect, _) = ui.allocate_exact_size(vec2(44.0, 44.0), Sense::hover());
                ui.painter().rect_filled(rect, 12.0, th.p.accent_soft);
                icons::paint(ui.painter(), egui::Rect::from_center_size(rect.center(), vec2(22.0, 22.0)), Icon::File, th.p.accent);
                ui.vertical(|ui| {
                    ui.spacing_mut().item_spacing.y = 2.0;
                    widgets::label_trunc(ui, RichText::new(&title).font(fonts::bold(15.0)).color(th.p.ink));
                    let mut s = capitalize(&kind);
                    if mins > 0 {
                        s.push_str(&format!("  ·  {mins} min read"));
                    }
                    widgets::label_trunc(ui, RichText::new(s).font(fonts::regular(12.5)).color(th.p.ink_muted));
                });
            });
        });
        if resp.clicked() {
            open_chapter(env, c);
        }
        ui.add_space(8.0);
    }
}

fn capitalize(s: &str) -> String {
    let mut c = s.chars();
    c.next().map(|f| f.to_uppercase().collect::<String>() + c.as_str()).unwrap_or_default()
}

fn syllabus_tab(ui: &mut Ui, env: &mut Env, syl: Option<&crate::data::models::Syllabus>) {
    let th = env.theme.clone();
    let Some(syl) = syl else {
        widgets::empty_state(ui, &th, Icon::List, "No syllabus data", "This subject has no syllabus file yet.");
        return;
    };
    if !syl.exam.is_empty() {
        widgets::panel_frame(&th).show(ui, |ui| {
            ui.set_width(ui.available_width());
            widgets::label(ui, RichText::new("Exam pattern").font(fonts::bold(14.0)).color(th.p.ink_muted));
            ui.add(egui::Label::new(RichText::new(&syl.exam).font(fonts::regular(15.0)).color(th.p.ink)));
            if !syl.areas.is_empty() {
                ui.add_space(8.0);
                ui.horizontal_wrapped(|ui| {
                    for a in &syl.areas {
                        widgets::badge(ui, a, th.p.accent, th.p.accent_soft);
                    }
                });
            }
        });
        ui.add_space(12.0);
    }
    for u in &syl.units {
        ui.push_id(("syl", u.no), |ui| {
            egui::CollapsingHeader::new(RichText::new(format!("{}. {}", u.no, u.title)).font(fonts::medium(15.0)).color(th.p.ink)).show(ui, |ui| {
                for t in &u.topics {
                    ui.add(egui::Label::new(RichText::new(format!("•  {t}")).color(th.p.ink_muted)));
                }
                if !u.summary.is_empty() {
                    ui.add_space(6.0);
                    widgets::label(ui, RichText::new("Chapter summary").font(fonts::medium(12.5)).color(th.p.accent));
                    for s in &u.summary {
                        ui.add(egui::Label::new(RichText::new(s).font(fonts::regular(13.5)).color(th.p.ink_muted)));
                    }
                }
                ui.add_space(6.0);
            });
        });
    }
}
