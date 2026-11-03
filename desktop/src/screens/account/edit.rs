//! Edit profile — a draft you can save or discard; saving writes to the account.
use egui::{vec2, Align, Layout, RichText, Ui};

use super::{poll, Job, Out};
use crate::data::store::Profile;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::screens::onboarding::{DISTRICTS, GENDERS, PRADESH, STUDENT_LEVELS};
use crate::theme::fonts;
use crate::ui::avatar::{tone, TONES};
use crate::ui::dialog;
use crate::ui::icons::Icon;
use crate::ui::widgets::{self, BtnKind};

#[derive(Default)]
pub struct EditState {
    draft: Option<Profile>,
    job: Option<Job>,
    error: Option<String>,
}

fn caption(ui: &mut Ui, env: &Env, text: &str) {
    widgets::label(ui, RichText::new(text).font(fonts::medium(13.0)).color(env.theme.p.ink_muted));
}

fn choice(ui: &mut Ui, env: &Env, options: &[&str], current: &mut String) {
    widgets::flow(ui, |ui| {
        for o in options {
            if widgets::chip(ui, &env.theme, o, current == o).clicked() {
                *current = if current == o { String::new() } else { (*o).to_string() };
            }
        }
    });
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut EditState) {
    let th = env.theme.clone();
    if let Some(r) = poll(env, &mut st.job) {
        match r {
            Ok(_) => {
                if let Some(d) = st.draft.clone() {
                    env.store.s.profile = d;
                    env.store.touch();
                }
                st.error = None;
                env.toast("Profile saved");
            }
            Err(e) => st.error = Some(e),
        }
    }
    let saved = env.store.s.profile.clone();
    let mut draft = st.draft.take().unwrap_or_else(|| saved.clone());
    let mut discard = false;
    let dirty = draft != saved;
    let busy = st.job.is_some();

    // identity header
    let photo = env.store.s.session.as_ref().map(|s| s.photo_url.clone()).unwrap_or_default();
    let email = env.store.s.session.as_ref().map(|s| s.email.clone()).unwrap_or_default();
    widgets::panel_frame(&th).show(ui, |ui| {
        ui.set_width(ui.available_width());
        ui.horizontal(|ui| {
            crate::ui::remote_image::avatar(ui, &th, &draft.display_name, draft.avatar_tone, 72.0, &photo);
            ui.add_space(6.0);
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 2.0;
                widgets::heading(ui, &th, if draft.display_name.is_empty() { "Your name" } else { &draft.display_name }, 22.0);
                widgets::muted(ui, &th, &format!("@{}", if draft.handle.is_empty() { "handle" } else { &draft.handle }));
                if !email.is_empty() {
                    widgets::muted(ui, &th, &email);
                }
            });
        });
        ui.add_space(12.0);
        caption(ui, env, "Avatar colour");
        widgets::flow(ui, |ui| {
            for i in 0..TONES.len() {
                let (rect, resp) = ui.allocate_exact_size(vec2(36.0, 36.0), egui::Sense::click());
                let on = crate::theme::motion::spring_bool(ui.ctx(), resp.id.with("on"), draft.avatar_tone == i, crate::theme::motion::FAST).clamp(0.0, 1.0);
                ui.painter().circle_filled(rect.center(), 14.0 + 2.0 * on, tone(i));
                ui.painter().circle_stroke(rect.center(), 18.0, egui::Stroke::new(2.5 * on, th.p.accent));
                if resp.hovered() {
                    ui.ctx().set_cursor_icon(egui::CursorIcon::PointingHand);
                }
                if resp.clicked() {
                    draft.avatar_tone = i;
                }
            }
        });
    });
    ui.add_space(16.0);

    widgets::panel_frame(&th).show(ui, |ui| {
        ui.set_width(ui.available_width());
        let w = ui.available_width().min(520.0);
        widgets::field(ui, &th, &mut draft.display_name, "Display name", Some(Icon::User), w, false, false);
        ui.add_space(8.0);
        widgets::field(ui, &th, &mut draft.school, "School or college", Some(Icon::School), w, false, false);
        ui.add_space(8.0);
        caption(ui, env, "Bio");
        widgets::text_area(ui, &th, &mut draft.bio, "A line or two about you", w, 3);
        ui.add_space(10.0);
        caption(ui, env, "Level");
        choice(ui, env, &STUDENT_LEVELS, &mut draft.level);
        ui.add_space(10.0);
        caption(ui, env, "Gender");
        choice(ui, env, &GENDERS, &mut draft.gender);
        ui.add_space(10.0);
        caption(ui, env, "Province");
        choice(ui, env, &PRADESH, &mut draft.pradesh);
        ui.add_space(10.0);
        caption(ui, env, "District");
        egui::ComboBox::from_id_salt("acct-district").width(w.min(280.0)).selected_text(if draft.district.is_empty() { "Choose a district" } else { &draft.district }).show_ui(ui, |ui| {
            for d in DISTRICTS.iter() {
                ui.selectable_value(&mut draft.district, (*d).to_string(), *d);
            }
        });
    });
    ui.add_space(16.0);

    if let Some(e) = &st.error {
        dialog::error_line(ui, &th, e);
        ui.add_space(6.0);
    }
    ui.with_layout(Layout::left_to_right(Align::Center), |ui| {
        ui.spacing_mut().item_spacing.x = 10.0;
        ui.add_enabled_ui(dirty && !busy, |ui| {
            let label = if busy { "Saving…" } else { "Save changes" };
            if widgets::button(ui, &th, label, BtnKind::Primary, Some(Icon::Check), None).clicked() {
                if env.demo || !env.signed_in() {
                    env.store.s.profile = draft.clone();
                    env.store.touch();
                    env.toast("Profile saved");
                } else {
                    let body = env.profile_payload(&draft);
                    let api = env.api();
                    st.job = Some(Task::spawn(&env.ctx, move || api.post("api/users/profile/", body).map(|_| Out::Done)));
                }
            }
        });
        if dirty && !busy && widgets::button(ui, &th, "Discard", BtnKind::Ghost, None, None).clicked() {
            discard = true;
            st.error = None;
        }
    });
    st.draft = Some(if discard { saved } else { draft });
}
