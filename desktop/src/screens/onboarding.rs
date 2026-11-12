//! Profile-completion journey — the same 13 steps and copy as Android's
//! `OnboardingFlow.kt` (Welcome → Role → Name → Handle → Birthday → Gender →
//! Level → Subjects → Place → Campus → Portrait → Bio → Finish). The profile is
//! stored locally.
use egui::{vec2, Align, Layout, RichText, Sense, Ui};

use crate::actions::Action;
use crate::env::Env;
use crate::router::Route;
use crate::theme::fonts;
use crate::ui::avatar::{avatar, tone, TONES};
use crate::ui::icons::{self, Icon};
use crate::ui::widgets::{self, BtnKind};

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Step {
    Welcome,
    Role,
    Name,
    Handle,
    Birthday,
    Gender,
    Level,
    Subjects,
    Place,
    Campus,
    Portrait,
    Bio,
    Finish,
}

const ROLES: [(&str, &str, &str, Icon); 4] = [
    ("student", "Student", "Learn, ask questions, save resources", Icon::School),
    ("teacher", "Teacher", "Teach, guide, publish resources", Icon::Library),
    ("institution", "Institution", "Represent a school, college or academy", Icon::Folder),
    ("explorer", "Explorer", "Look around first, fill this in later", Icon::Globe),
];
pub(crate) const GENDERS: [&str; 3] = ["Male", "Female", "Other"];
pub(crate) const PRADESH: [&str; 7] = ["Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"];
pub(crate) const SUBJECTS: [&str; 10] = ["English", "Nepali", "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science", "Accountancy", "Economics", "Social Studies"];
pub(crate) const STUDENT_LEVELS: [&str; 11] = ["Class 8", "Class 9", "Class 10 / SEE", "Class 11", "Class 12", "+2 Passout", "Diploma", "Bachelors", "Masters", "PhD", "Other"];
const TEACHER_LEVELS: [&str; 7] = ["Class 11", "Class 12", "+2 Passout", "Diploma", "Bachelors", "Masters", "Other"];
const INSTITUTION_TYPES: [&str; 4] = ["school", "college", "academy", "other"];
pub(crate) const MONTHS: [&str; 12] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
pub(crate) const DISTRICTS: [&str; 75] = [
    "Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura", "Banke", "Bara", "Bardiya", "Bhaktapur", "Bhojpur", "Chitwan", "Dadeldhura", "Dailekh",
    "Dang", "Darchula", "Dhading", "Dhankuta", "Dhanusha", "Dolakha", "Dolpa", "Doti", "Gorkha", "Gulmi", "Humla", "Ilam", "Jajarkot", "Jhapa", "Jumla", "Kailali",
    "Kalikot", "Kanchanpur", "Kapilvastu", "Kaski", "Kathmandu", "Kavrepalanchok", "Khotang", "Lalitpur", "Lamjung", "Mahottari", "Makwanpur", "Manang", "Mustang",
    "Myagdi", "Nawalpur", "Nuwakot", "Okhaldhunga", "Palpa", "Panchthar", "Parasi", "Parbat", "Parsa", "Pyuthan", "Ramechhap", "Rasuwa", "Rautahat", "Rolpa",
    "Rukum East", "Rukum West", "Rupandehi", "Salyan", "Sankhuwasabha", "Saptari", "Sarlahi", "Sindhuli", "Sindhupalchok", "Siraha", "Solukhumbu", "Sunsari",
    "Surkhet", "Syangja", "Tanahun", "Taplejung", "Terhathum", "Udayapur",
];

pub fn steps_for(role: &str) -> Vec<Step> {
    let mut v = vec![Step::Welcome, Step::Role, Step::Name, Step::Handle, Step::Birthday, Step::Gender];
    match role {
        "student" | "teacher" => v.extend([Step::Level, Step::Subjects, Step::Place, Step::Campus]),
        "institution" => v.extend([Step::Place, Step::Campus]),
        _ => v.push(Step::Place),
    }
    v.extend([Step::Portrait, Step::Bio, Step::Finish]);
    v
}

#[derive(Default)]
pub struct OnboardingState {
    idx: usize,
    day: u32,
    month: usize,
    year: i32,
    inited: bool,
    shown: Option<usize>,
}

impl OnboardingState {
    /// Jump to a step (used by the screenshot tour and by "edit profile").
    pub fn goto(&mut self, idx: usize) {
        self.idx = idx;
    }
}

fn handle_ok(h: &str) -> bool {
    h.len() >= 3 && h.len() <= 24 && h.chars().all(|c| c.is_ascii_alphanumeric() || c == '_')
}

fn complete(step: Step, p: &crate::data::store::Profile) -> bool {
    match step {
        Step::Welcome | Step::Portrait | Step::Bio | Step::Finish => true,
        Step::Role => !p.role.is_empty(),
        Step::Name => p.display_name.trim().chars().count() >= 2,
        Step::Handle => handle_ok(&p.handle),
        Step::Birthday => !p.dob.is_empty(),
        Step::Gender => !p.gender.is_empty(),
        Step::Level => !p.level.is_empty(),
        Step::Subjects => !p.subjects.is_empty(),
        Step::Place => !p.pradesh.is_empty() && !p.district.is_empty(),
        Step::Campus => !p.school.trim().is_empty() && (p.role != "institution" || !p.institution_type.is_empty()),
    }
}

fn copy(step: Step, role: &str) -> &'static str {
    let teacher = role == "teacher";
    match step {
        Step::Welcome => "Welcome to NEBians",
        Step::Role => "Which path is yours?",
        Step::Name => "What should we call you?",
        Step::Handle => "Claim your handle",
        Step::Birthday => "When were you born?",
        Step::Gender => "How do you identify?",
        Step::Level => if teacher { "Which levels do you teach?" } else { "Where are you right now?" },
        Step::Subjects => if teacher { "What do you teach?" } else { "What are you studying?" },
        Step::Place => "Where do you study from?",
        Step::Campus => if role == "institution" { "Tell us about your institution" } else { "Where do you study?" },
        Step::Portrait => "Put a face to the name",
        Step::Bio => "Say something about you",
        Step::Finish => "That's your profile",
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut OnboardingState) {
    let th = env.theme.clone();
    if !st.inited {
        st.inited = true;
        st.day = 1;
        st.month = 0;
        st.year = 2008;
        if let Some(s) = &env.store.s.session {
            if env.store.s.profile.handle.is_empty() {
                env.store.s.profile.handle = s.username.clone();
            }
        }
    }
    let role = env.store.s.profile.role.clone();
    let steps = steps_for(&role);
    st.idx = st.idx.min(steps.len() - 1);
    let step = steps[st.idx];
    let title = copy(step, &role);

    // top bar: back + progress
    let w = (ui.available_width() - 48.0).clamp(300.0, 560.0);
    let side = ((ui.available_width() - w) / 2.0).max(0.0);
    ui.add_space(18.0);
    ui.horizontal(|ui| {
        ui.add_space(side);
        ui.allocate_ui_with_layout(vec2(w, 40.0), Layout::left_to_right(Align::Center), |ui| {
            ui.add_enabled_ui(st.idx > 0, |ui| {
                if widgets::icon_button(ui, &th, Icon::Back, "Back", false).clicked() {
                    st.idx -= 1;
                }
            });
            let pw = ui.available_width() - 60.0;
            ui.allocate_ui(vec2(pw, 8.0), |ui| widgets::progress_bar(ui, &th, (st.idx + 1) as f32 / steps.len() as f32, 6.0, None));
            ui.add(egui::Label::new(RichText::new(format!("{}/{}", st.idx + 1, steps.len())).font(fonts::medium(12.5)).color(th.p.ink_muted)).selectable(false));
        });
    });
    ui.add_space(8.0);

    // footer is reserved first so the content can scroll above it
    let can_continue = complete(step, &env.store.s.profile);
    egui::TopBottomPanel::bottom("onb_footer").frame(egui::Frame::none().fill(th.p.page).inner_margin(egui::Margin::symmetric(0.0, 14.0))).show_inside(ui, |ui| {
        ui.horizontal(|ui| {
            ui.add_space(side);
            let label = match step {
                Step::Welcome => "Let's begin",
                Step::Finish => "Enter NEBians",
                _ => "Continue",
            };
            ui.add_enabled_ui(can_continue, |ui| {
                if widgets::button(ui, &th, label, BtnKind::Primary, None, Some(if matches!(step, Step::Portrait | Step::Bio) { w - 120.0 } else { w })).clicked() {
                    if step == Step::Finish {
                        env.store.s.onboarded = true;
                        env.store.touch();
                        env.push_profile();
                        env.act(Action::Replace(Route::Home));
                    } else {
                        st.idx += 1;
                    }
                }
            });
            if matches!(step, Step::Portrait | Step::Bio) && widgets::button(ui, &th, "Skip", BtnKind::Ghost, None, Some(110.0)).clicked() {
                st.idx += 1;
            }
        });
    });

    egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| {
        ui.horizontal_top(|ui| {
            ui.add_space(side);
            ui.vertical(|ui| {
                ui.set_width(w);
                ui.add_space(20.0);
                ui.add(egui::Label::new(RichText::new(title).font(fonts::bold(if w < 420.0 { 25.0 } else { 30.0 })).color(th.p.ink)).selectable(false));
                ui.add_space(26.0);
                let key = egui::Id::new("onb-step");
                if st.shown != Some(st.idx) {
                    st.shown = Some(st.idx);
                    crate::theme::motion::reset_enter(ui.ctx(), key);
                }
                super::common::rise(ui, key);
                step_body(ui, env, st, step, w);
            });
        });
    });
}

fn step_body(ui: &mut Ui, env: &mut Env, st: &mut OnboardingState, step: Step, w: f32) {
    let th = env.theme.clone();
    let role = env.store.s.profile.role.clone();
    match step {
        Step::Welcome => {
            for (t, d) in [("Who you are", "Role, name and a handle"), ("What you study", "Level, subjects and where"), ("Your face", "An avatar and a short bio")] {
                widgets::panel_frame(&th).inner_margin(egui::Margin::symmetric(16.0, 12.0)).show(ui, |ui| {
                    ui.set_width(w - 34.0);
                    widgets::label(ui, RichText::new(t).font(fonts::medium(15.0)).color(th.p.ink));
                    widgets::label(ui, RichText::new(d).font(fonts::regular(13.0)).color(th.p.ink_muted));
                });
                ui.add_space(8.0);
            }
        }
        Step::Role => {
            for (key, name, desc, icon) in ROLES {
                let selected = role == key;
                let resp = widgets::card(ui, &th, vec2(w, 74.0), 14.0, |ui| {
                    ui.horizontal(|ui| {
                        let (rect, _) = ui.allocate_exact_size(vec2(44.0, 44.0), Sense::hover());
                        ui.painter().rect_filled(rect, 12.0, if selected { th.p.accent } else { th.p.field });
                        icons::paint(ui.painter(), egui::Rect::from_center_size(rect.center(), vec2(22.0, 22.0)), icon, if selected { th.p.on_accent } else { th.p.ink });
                        ui.vertical(|ui| {
                            ui.spacing_mut().item_spacing.y = 1.0;
                            widgets::label(ui, RichText::new(name).font(fonts::bold(15.5)).color(th.p.ink));
                            widgets::label(ui, RichText::new(desc).font(fonts::regular(13.0)).color(th.p.ink_muted));
                        });
                    });
                });
                if selected {
                    ui.painter().rect_stroke(resp.rect, crate::theme::spacing::CARD_RADIUS, egui::Stroke::new(2.0_f32, th.p.accent));
                }
                if resp.clicked() {
                    env.store.s.profile.role = key.to_string();
                    env.store.touch();
                    // switching role changes the step list; stay on this step
                }
                ui.add_space(8.0);
            }
        }
        Step::Name => {
            let mut v = env.store.s.profile.display_name.clone();
            widgets::text_field(ui, &th, &mut v, "Your name", Some(Icon::User), w, false);
            if v != env.store.s.profile.display_name {
                if env.store.s.profile.handle.is_empty() || env.store.s.profile.handle == slug(&env.store.s.profile.display_name) {
                    env.store.s.profile.handle = slug(&v);
                }
                env.store.s.profile.display_name = v;
                env.store.touch();
            }
        }
        Step::Handle => {
            let mut v = env.store.s.profile.handle.clone();
            widgets::text_field(ui, &th, &mut v, "handle", Some(Icon::User), w, false);
            let v = v.to_lowercase();
            if v != env.store.s.profile.handle {
                env.store.s.profile.handle = v;
                env.store.touch();
            }
            ui.add_space(8.0);
            let h = &env.store.s.profile.handle;
            let (msg, col) = if h.is_empty() {
                ("Pick 3–24 letters, numbers or underscores.".to_string(), th.p.ink_muted)
            } else if handle_ok(h) {
                (format!("@{h} looks good."), th.p.ok)
            } else {
                ("Only letters, numbers and underscores, 3–24 characters.".to_string(), th.p.danger)
            };
            ui.add(egui::Label::new(RichText::new(msg).color(col)));
        }
        Step::Birthday => {
            ui.horizontal(|ui| {
                egui::ComboBox::from_id_salt("dob_day").selected_text(st.day.to_string()).width(80.0).show_ui(ui, |ui| {
                    for d in 1..=31 {
                        ui.selectable_value(&mut st.day, d, d.to_string());
                    }
                });
                egui::ComboBox::from_id_salt("dob_month").selected_text(MONTHS[st.month]).width(150.0).show_ui(ui, |ui| {
                    for (i, m) in MONTHS.iter().enumerate() {
                        ui.selectable_value(&mut st.month, i, *m);
                    }
                });
                egui::ComboBox::from_id_salt("dob_year").selected_text(st.year.to_string()).width(100.0).show_ui(ui, |ui| {
                    for y in (1950..=2020).rev() {
                        ui.selectable_value(&mut st.year, y, y.to_string());
                    }
                });
            });
            let dob = format!("{:04}-{:02}-{:02}", st.year, st.month + 1, st.day);
            if env.store.s.profile.dob != dob {
                env.store.s.profile.dob = dob;
                env.store.touch();
            }
            ui.add_space(8.0);
            ui.add(egui::Label::new(RichText::new(format!("{} {}, {}", MONTHS[st.month], st.day, st.year)).color(th.p.ink_muted)));
        }
        Step::Gender => {
            crate::ui::widgets::flow(ui, |ui| {
                for g in GENDERS {
                    if widgets::chip(ui, &th, g, env.store.s.profile.gender == g).clicked() {
                        env.store.s.profile.gender = g.to_string();
                        env.store.touch();
                    }
                }
            });
        }
        Step::Level => {
            let levels: &[&str] = if role == "teacher" { &TEACHER_LEVELS } else { &STUDENT_LEVELS };
            crate::ui::widgets::flow(ui, |ui| {
                for l in levels {
                    if widgets::chip(ui, &th, l, env.store.s.profile.level == *l).clicked() {
                        env.store.s.profile.level = l.to_string();
                        env.store.touch();
                    }
                }
            });
        }
        Step::Subjects => {
            crate::ui::widgets::flow(ui, |ui| {
                for s in SUBJECTS {
                    let on = env.store.s.profile.subjects.iter().any(|x| x == s);
                    if widgets::chip(ui, &th, s, on).clicked() {
                        let list = &mut env.store.s.profile.subjects;
                        if on {
                            list.retain(|x| x != s);
                        } else {
                            list.push(s.to_string());
                        }
                        env.store.touch();
                    }
                }
            });
        }
        Step::Place => {
            widgets::label(ui, RichText::new("Province").font(fonts::medium(13.5)).color(th.p.ink_muted));
            ui.add_space(4.0);
            crate::ui::widgets::flow(ui, |ui| {
                for p in PRADESH {
                    if widgets::chip(ui, &th, p, env.store.s.profile.pradesh == p).clicked() {
                        env.store.s.profile.pradesh = p.to_string();
                        env.store.touch();
                    }
                }
            });
            ui.add_space(14.0);
            widgets::label(ui, RichText::new("District").font(fonts::medium(13.5)).color(th.p.ink_muted));
            ui.add_space(4.0);
            let cur = if env.store.s.profile.district.is_empty() { "Select district".to_string() } else { env.store.s.profile.district.clone() };
            egui::ComboBox::from_id_salt("district").selected_text(cur).width(w.min(320.0)).height(320.0).show_ui(ui, |ui| {
                for d in DISTRICTS {
                    if ui.selectable_label(env.store.s.profile.district == d, d).clicked() {
                        env.store.s.profile.district = d.to_string();
                        env.store.touch();
                    }
                }
            });
        }
        Step::Campus => {
            let mut v = env.store.s.profile.school.clone();
            let hint = if role == "institution" { "Institution name" } else { "School or college" };
            widgets::text_field(ui, &th, &mut v, hint, Some(Icon::School), w, false);
            if v != env.store.s.profile.school {
                env.store.s.profile.school = v;
                env.store.touch();
            }
            if role == "institution" {
                ui.add_space(14.0);
                crate::ui::widgets::flow(ui, |ui| {
                    for t in INSTITUTION_TYPES {
                        if widgets::chip(ui, &th, t, env.store.s.profile.institution_type == t).clicked() {
                            env.store.s.profile.institution_type = t.to_string();
                            env.store.touch();
                        }
                    }
                });
            }
        }
        Step::Portrait => {
            let name = env.store.s.profile.display_name.clone();
            ui.vertical_centered(|ui| avatar(ui, &th, &name, env.store.s.profile.avatar_tone, 112.0));
            ui.add_space(20.0);
            crate::ui::widgets::flow(ui, |ui| {
                for i in 0..TONES.len() {
                    let (rect, resp) = ui.allocate_exact_size(vec2(40.0, 40.0), Sense::click());
                    ui.painter().circle_filled(rect.center(), 17.0, tone(i));
                    if env.store.s.profile.avatar_tone == i {
                        ui.painter().circle_stroke(rect.center(), 20.0, egui::Stroke::new(2.5_f32, th.p.accent));
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
        }
        Step::Bio => {
            let mut v = env.store.s.profile.bio.clone();
            ui.add(egui::TextEdit::multiline(&mut v).desired_rows(4).desired_width(w).hint_text("e.g. Preparing for CEE 2083, happy to help with Physics.").char_limit(160));
            if v != env.store.s.profile.bio {
                env.store.s.profile.bio = v;
                env.store.touch();
            }
            ui.add_space(4.0);
            ui.add(egui::Label::new(RichText::new(format!("{}/160", env.store.s.profile.bio.chars().count())).font(fonts::regular(12.0)).color(th.p.ink_faint)));
        }
        Step::Finish => {
            summary(ui, env, w);
        }
    }
}

pub fn slug(name: &str) -> String {
    let s: String = name.to_lowercase().chars().filter_map(|c| if c.is_ascii_alphanumeric() { Some(c) } else if c == ' ' || c == '_' { Some('_') } else { None }).collect();
    s.trim_matches('_').chars().take(24).collect()
}

fn summary(ui: &mut Ui, env: &mut Env, w: f32) {
    let th = env.theme.clone();
    let p = env.store.s.profile.clone();
    widgets::panel_frame(&th).show(ui, |ui| {
        ui.set_width(w - 38.0);
        ui.horizontal(|ui| {
            avatar(ui, &th, &p.display_name, p.avatar_tone, 64.0);
            ui.vertical(|ui| {
                widgets::label(ui, RichText::new(&p.display_name).font(fonts::bold(19.0)).color(th.p.ink));
                widgets::label(ui, RichText::new(format!("@{}", p.handle)).color(th.p.ink_muted));
            });
        });
        ui.add_space(12.0);
        widgets::hairline(ui, &th);
        ui.add_space(10.0);
        let role = ROLES.iter().find(|r| r.0 == p.role).map(|r| r.1).unwrap_or("Explorer");
        let rows: Vec<(&str, String)> = vec![
            ("Role", role.to_string()),
            ("Level", p.level.clone()),
            ("Subjects", p.subjects.join(", ")),
            ("Place", [p.district.as_str(), p.pradesh.as_str()].iter().filter(|s| !s.is_empty()).cloned().collect::<Vec<_>>().join(", ")),
            ("Campus", p.school.clone()),
            ("Bio", p.bio.clone()),
        ];
        egui::Grid::new("summary").num_columns(2).spacing([20.0, 8.0]).show(ui, |ui| {
            for (k, v) in rows.into_iter().filter(|(_, v)| !v.is_empty()) {
                widgets::label(ui, RichText::new(k).font(fonts::medium(13.0)).color(th.p.ink_muted));
                ui.add(egui::Label::new(RichText::new(v).color(th.p.ink)).wrap());
                ui.end_row();
            }
        });
    });
}
