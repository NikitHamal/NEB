//! `--screenshots <dir>`: a scripted tour of every screen that saves a PNG of
//! each one using egui's own framebuffer screenshot, then quits. This is how the
//! images in `desktop/screenshots/` are produced (headless, under Xvfb).
use std::path::PathBuf;

use eframe::egui::{self, Context, ViewportCommand};

use crate::app::NebApp;
use crate::data::models::{ChapterKind, ChapterRef};
use crate::data::store::ThemeMode;
use crate::router::Route;

type Setup = fn(&mut NebApp, &Context);

struct Step {
    name: &'static str,
    settle: u32,
    setup: Setup,
}

#[derive(PartialEq)]
enum Phase {
    Setup,
    Wait,
    Shot,
}

pub struct Tour {
    dir: PathBuf,
    idx: usize,
    frames: u32,
    phase: Phase,
    steps: Vec<Step>,
}

fn go(app: &mut NebApp, r: Route) {
    app.router.replace(r);
}

fn profile(app: &mut NebApp) {
    let s = &mut app.env.store.s;
    s.onboarded = true;
    s.guest = true;
    s.profile.role = "student".into();
    s.profile.display_name = "Aarav Sharma".into();
    s.profile.handle = "aarav_sharma".into();
    s.profile.level = "Class 12".into();
    s.profile.subjects = vec!["Physics".into(), "Chemistry".into(), "Mathematics".into()];
    s.profile.pradesh = "Bagmati".into();
    s.profile.district = "Lalitpur".into();
    s.profile.school = "Budhanilkantha School".into();
    s.profile.bio = "Preparing for IOE 2083. Happy to help with Physics.".into();
    s.profile.avatar_tone = 0;
    s.prefs.show_toc = true;
}

fn light(a: &mut NebApp) {
    a.env.store.s.prefs.theme = ThemeMode::Light;
    a.env.refresh_theme();
}

fn signed(app: &mut NebApp) {
    use crate::data::store::Session;
    app.env.store.s.guest = false;
    app.env.store.s.session = Some(Session { email: "aarav@example.com".into(), username: "aarav_sharma".into(), token: "tour".into(), user_id: "tour".into(), display_name: "Aarav Sharma".into(), photo_url: String::new(), provider: "email".into() });
    app.env.store.s.profile.display_name = "Aarav Sharma".into();
    app.env.store.s.profile.handle = "aarav_sharma".into();
}

fn size(ctx: &Context, w: f32, h: f32) {
    ctx.send_viewport_cmd(ViewportCommand::InnerSize(egui::vec2(w, h)));
}

impl Tour {
    pub fn new(dir: PathBuf) -> Self {
        let _ = std::fs::create_dir_all(&dir);
        let steps = vec![
            Step { name: "splash", settle: 20, setup: |a, _| { a.env.store.s.onboarded = false; a.env.store.s.guest = false; go(a, Route::Splash) } },
            Step { name: "login", settle: 24, setup: |a, _| { a.screens.login.clear(); go(a, Route::Login) } },
            Step { name: "login-browser-handoff", settle: 24, setup: |a, _| { a.screens.login.demo_waiting(); go(a, Route::Login) } },
            Step { name: "email-signin", settle: 24, setup: |a, _| { a.screens.login.clear(); go(a, Route::EmailAuth) } },
            Step { name: "complete-profile", settle: 24, setup: |a, _| { signed(a); a.screens.complete = Default::default(); go(a, Route::CompleteProfile) } },
            Step { name: "onboarding-role", settle: 20, setup: |a, _| { a.env.store.s.profile.role = "student".into(); a.screens.onboarding = Default::default(); a.screens.onboarding.goto(1); go(a, Route::Onboarding) } },
            Step { name: "onboarding-subjects", settle: 20, setup: |a, _| { a.env.store.s.profile.subjects = vec!["Physics".into(), "Mathematics".into()]; a.screens.onboarding.goto(7); go(a, Route::Onboarding) } },
            Step { name: "home", settle: 30, setup: |a, _| { profile(a); signed(a); light(a); recent(a); go(a, Route::Home) } },
            Step { name: "library", settle: 20, setup: |a, _| go(a, Route::Library) },
            Step { name: "category-class-11", settle: 20, setup: |a, _| go(a, Route::Category("11".into())) },
            Step { name: "subject-physics", settle: 20, setup: |a, _| go(a, Route::Subject { track: "11".into(), subject: "physics".into() }) },
            Step { name: "reader-notes", settle: 140, setup: |a, _| go(a, Route::Reader(ChapterRef::new("11", "physics", ChapterKind::Unit, 1))) },
            Step { name: "reader-math-figures", settle: 160, setup: |a, _| { a.screens.reader.set_jump("s2"); go(a, Route::Reader(ChapterRef::new("11", "physics", ChapterKind::Unit, 3))) } },
            Step { name: "reader-practice-mcq", settle: 160, setup: |a, _| {
                a.screens.reader.preanswer(&[(0, 'b'), (1, 'a'), (2, 'a'), (3, 'd')]);
                a.screens.reader.set_jump("s4");
                go(a, Route::Reader(ChapterRef::new("11", "physics", ChapterKind::Unit, 1)))
            } },
            Step { name: "community-feed", settle: 24, setup: |a, _| { a.screens.community.demo(); go(a, Route::Community) } },
            Step { name: "community-thread", settle: 24, setup: |a, _| go(a, Route::Post("d1".into())) },
            Step { name: "notifications", settle: 24, setup: |a, _| { a.env.srv.unread = 3; a.screens.notifications.demo(); go(a, Route::Notifications) } },
            Step { name: "search", settle: 90, setup: |a, _| { a.screens.search.query = "projectile".into(); go(a, Route::Search) } },
            Step { name: "bookmarks", settle: 20, setup: |a, _| {
                for (t, s, n, title, sn) in [("11", "physics", 1, "Physical Quantities", "Physics"), ("cee", "chemistry", 2, "Atomic Structure", "Chemistry"), ("12", "mathematics", 3, "Differentiation", "Mathematics")] {
                    let c = ChapterRef::new(t, s, ChapterKind::Unit, n);
                    if !a.env.store.is_bookmarked(&c) { a.env.store.toggle_bookmark(&c, title, sn); }
                }
                go(a, Route::Bookmarks)
            } },
            Step { name: "books", settle: 90, setup: |a, _| go(a, Route::Books) },
            Step { name: "people", settle: 30, setup: |a, _| { a.screens.people.demo(); go(a, Route::People) } },
            Step { name: "member-profile", settle: 40, setup: |a, _| { a.screens.user.demo(); go(a, Route::User("anish_karki".into())) } },
            Step { name: "offline-library", settle: 60, setup: |a, _| go(a, Route::Downloads) },
            Step { name: "settings", settle: 24, setup: |a, _| go(a, Route::Settings) },
            Step { name: "profile", settle: 24, setup: |a, _| go(a, Route::Profile) },
            Step { name: "about", settle: 20, setup: |a, _| go(a, Route::About) },
            Step { name: "home-dark", settle: 30, setup: |a, _| { a.env.store.s.prefs.theme = ThemeMode::Dark; a.env.refresh_theme(); go(a, Route::Home) } },
            Step { name: "community-dark", settle: 24, setup: |a, _| go(a, Route::Community) },
            Step { name: "login-dark", settle: 24, setup: |a, _| go(a, Route::Login) },
            Step { name: "reader-dark", settle: 150, setup: |a, _| { a.screens.reader.set_jump("s2"); go(a, Route::Reader(ChapterRef::new("11", "physics", ChapterKind::Unit, 1))) } },
        ];
        Self { dir, idx: 0, frames: 0, phase: Phase::Setup, steps }
    }

    pub fn tick(&mut self, app: &mut NebApp, ctx: &Context) {
        ctx.request_repaint();
        let Some(step) = self.steps.get(self.idx) else {
            ctx.send_viewport_cmd(ViewportCommand::Close);
            return;
        };
        match self.phase {
            Phase::Setup => {
                (step.setup)(app, ctx);
                self.frames = 0;
                self.phase = Phase::Wait;
            }
            Phase::Wait => {
                self.frames += 1;
                if step.name == "splash" {
                    app.screens.splash.hold(0.55);
                }
                if self.frames >= step.settle && !app.is_busy() {
                    ctx.send_viewport_cmd(ViewportCommand::Screenshot);
                    self.phase = Phase::Shot;
                    self.frames = 0;
                }
            }
            Phase::Shot => {
                self.frames += 1;
                let shot = ctx.input(|i| {
                    i.events.iter().find_map(|e| match e {
                        egui::Event::Screenshot { image, .. } => Some(image.clone()),
                        _ => None,
                    })
                });
                if let Some(img) = shot {
                    let path = self.dir.join(format!("{:02}-{}.png", self.idx + 1, step.name));
                    let rgba: Vec<u8> = img.pixels.iter().flat_map(|c| c.to_array()).collect();
                    if let Some(buf) = image::RgbaImage::from_raw(img.width() as u32, img.height() as u32, rgba) {
                        match buf.save(&path) {
                            Ok(_) => eprintln!("saved {}", path.display()),
                            Err(e) => eprintln!("could not save {}: {e}", path.display()),
                        }
                    }
                    self.idx += 1;
                    self.phase = Phase::Setup;
                } else if self.frames > 120 {
                    eprintln!("screenshot for {} never arrived — skipping", step.name);
                    self.idx += 1;
                    self.phase = Phase::Setup;
                }
            }
        }
        let _ = Phase::Shot == Phase::Wait;
    }
}

fn recent(app: &mut NebApp) {
    for (t, s, n, title, sn, col) in [
        ("11", "physics", 1, "Physical Quantities", "Physics", "#4A42D6"),
        ("12", "mathematics", 3, "Differentiation", "Mathematics", "#8F5507"),
        ("cee", "chemistry", 2, "Atomic Structure", "Chemistry", "#0B6A62"),
    ] {
        let c = ChapterRef::new(t, s, ChapterKind::Unit, n);
        app.env.store.push_recent(&c, title, sn, col);
    }
}
