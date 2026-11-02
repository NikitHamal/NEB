//! Profile — the data collected in onboarding, editable in place, plus study stats.
use egui::{vec2, RichText, Ui};

use super::common::*;
use crate::actions::Action;
use crate::env::Env;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::avatar::{avatar, tone, TONES};
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct ProfileState {
    editing: bool,
}

fn stat(ui: &mut Ui, env: &Env, w: f32, value: String, label: &str) {
    let th = &env.theme;
    widgets::card(ui, th, vec2(w, 84.0), 14.0, |ui| {
        widgets::label(ui, RichText::new(value).font(fonts::bold(24.0)).color(th.p.ink));
        widgets::label(ui, RichText::new(label).font(fonts::regular(12.5)).color(th.p.ink_muted));
    });
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut ProfileState) {
    scroll_page(ui, env, "profile", |ui, env| {
        let th = env.theme.clone();
        let p = env.store.s.profile.clone();
        let who = match (&env.store.s.session, env.store.s.guest) {
            (Some(s), _) => format!("Signed in · {}", if s.email.is_empty() { "NEBians account" } else { &s.email }),
            (None, true) => "Guest — your data stays on this computer".to_string(),
            _ => "Local profile".to_string(),
        };
        ui.horizontal(|ui| {
            let photo = env.store.s.session.as_ref().map(|s| s.photo_url.clone()).unwrap_or_default();
            crate::ui::remote_image::avatar(ui, &th, &p.display_name, p.avatar_tone, 84.0, &photo);
            ui.add_space(6.0);
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 2.0;
                widgets::heading(ui, &th, if p.display_name.is_empty() { "Your name" } else { &p.display_name }, 26.0);
                widgets::muted(ui, &th, &format!("@{}", if p.handle.is_empty() { "handle" } else { &p.handle }));
                widgets::muted(ui, &th, &who);
            });
        });
        ui.add_space(14.0);
        crate::ui::widgets::flow(ui, |ui| {
            let label = if st.editing { "Done" } else { "Edit profile" };
            if widgets::button(ui, &th, label, if st.editing { BtnKind::Primary } else { BtnKind::Secondary }, Some(if st.editing { Icon::Check } else { Icon::Edit }), None).clicked() {
                if st.editing {
                    env.push_profile();
                    if env.signed_in() {
                        env.toast("Profile saved to your account");
                    }
                }
                st.editing = !st.editing;
            }
            if widgets::button(ui, &th, "Settings", BtnKind::Ghost, Some(Icon::Settings), None).clicked() {
                env.go(Route::Settings);
            }
        });
        ui.add_space(22.0);

        let total: u32 = env.tracks.iter().map(|t| t.chapter_total()).sum();
        widgets::grid(ui, 160.0, 12.0, 4, |ui, i, w| match i {
            0 => stat(ui, env, w, env.store.total_done().to_string(), "chapters finished"),
            1 => stat(ui, env, w, env.store.s.bookmarks.len().to_string(), "bookmarks"),
            2 => stat(ui, env, w, env.store.s.recent.len().to_string(), "recently opened"),
            _ => stat(ui, env, w, total.to_string(), "chapters in the library"),
        });
        ui.add_space(24.0);

        if st.editing {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                let w = ui.available_width();
                let mut name = p.display_name.clone();
                widgets::label(ui, RichText::new("Display name").font(fonts::medium(13.0)).color(th.p.ink_muted));
                widgets::text_field(ui, &th, &mut name, "Your name", Some(Icon::User), w.min(460.0), false);
                ui.add_space(10.0);
                let mut handle = p.handle.clone();
                widgets::label(ui, RichText::new("Handle").font(fonts::medium(13.0)).color(th.p.ink_muted));
                widgets::text_field(ui, &th, &mut handle, "handle", Some(Icon::User), w.min(460.0), false);
                ui.add_space(10.0);
                let mut school = p.school.clone();
                widgets::label(ui, RichText::new("School or college").font(fonts::medium(13.0)).color(th.p.ink_muted));
                widgets::text_field(ui, &th, &mut school, "Campus", Some(Icon::School), w.min(460.0), false);
                ui.add_space(10.0);
                let mut bio = p.bio.clone();
                widgets::label(ui, RichText::new("Bio").font(fonts::medium(13.0)).color(th.p.ink_muted));
                ui.add(egui::TextEdit::multiline(&mut bio).desired_rows(3).desired_width(w.min(460.0)).char_limit(160));
                ui.add_space(10.0);
                widgets::label(ui, RichText::new("Avatar colour").font(fonts::medium(13.0)).color(th.p.ink_muted));
                crate::ui::widgets::flow(ui, |ui| {
                    for i in 0..TONES.len() {
                        let (rect, resp) = ui.allocate_exact_size(vec2(34.0, 34.0), egui::Sense::click());
                        ui.painter().circle_filled(rect.center(), 14.0, tone(i));
                        if p.avatar_tone == i {
                            ui.painter().circle_stroke(rect.center(), 17.0, egui::Stroke::new(2.5, th.p.accent));
                        }
                        if resp.hovered() {
                            ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
                        }
                        if resp.clicked() {
                            env.store.s.profile.avatar_tone = i;
                            env.store.touch();
                        }
                    }
                });
                let pr = &mut env.store.s.profile;
                if pr.display_name != name || pr.handle != handle.to_lowercase() || pr.school != school || pr.bio != bio {
                    pr.display_name = name;
                    pr.handle = handle.to_lowercase();
                    pr.school = school;
                    pr.bio = bio;
                    env.store.touch();
                }
            });
        } else {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                let rows: Vec<(&str, String)> = vec![
                    ("Role", crate::util::truncate(&p.role, 20)),
                    ("Level", p.level.clone()),
                    ("Subjects", p.subjects.join(", ")),
                    ("Place", [p.district.as_str(), p.pradesh.as_str()].iter().filter(|s| !s.is_empty()).cloned().collect::<Vec<_>>().join(", ")),
                    ("Campus", p.school.clone()),
                    ("Born", p.dob.clone()),
                    ("Bio", p.bio.clone()),
                ];
                egui::Grid::new("profile_grid").num_columns(2).spacing([24.0, 10.0]).show(ui, |ui| {
                    for (k, v) in rows.into_iter().filter(|(_, v)| !v.is_empty()) {
                        widgets::label(ui, RichText::new(k).font(fonts::medium(13.0)).color(th.p.ink_muted));
                        ui.add(egui::Label::new(RichText::new(v).color(th.p.ink)).wrap());
                        ui.end_row();
                    }
                });
            });
        }
        ui.add_space(20.0);
        if env.store.s.session.is_none() {
            widgets::panel_frame(&th).show(ui, |ui| {
                ui.set_width(ui.available_width());
                widgets::heading(ui, &th, "Sign in to sync with the community", 16.0);
                widgets::muted(ui, &th, "Guests can read everything. Sign in with Google, GitHub or email to post, reply and keep your profile on every device.");
                ui.add_space(10.0);
                if widgets::button(ui, &th, "Sign in or join", BtnKind::Primary, Some(Icon::Login), None).clicked() {
                    env.act(Action::Replace(Route::Login));
                }
            });
        }
    });
}
