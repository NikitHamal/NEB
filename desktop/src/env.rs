//! `Env` — the shared services every screen receives: theme, persisted store,
//! content root, cached syllabus data, the action queue and toasts.
//! Screens keep their own local state and talk to the rest of the app through `Env`.
use std::path::PathBuf;
use std::sync::Arc;

use egui::Context;

use crate::actions::Action;
use crate::data::content::{ContentRepo, Manifest};
use crate::data::lazy::{Lazy, View};
use crate::errors::Result;
use crate::data::models::*;
use crate::data::store::{Store, ThemeMode};
use crate::data::tasks::Task;
use crate::router::Route;
use crate::theme::{Palette, Theme};
use crate::ui::logo::Logo;
use crate::ui::toast::Toasts;
use crate::ui::LayoutMode;

pub enum ContentStatus {
    Loading,
    Ready,
    Failed(String),
}

pub struct Env {
    pub ctx: Context,
    pub theme: Theme,
    pub store: Store,
    pub repo: ContentRepo,
    pub status: ContentStatus,
    pub manifest: Option<Manifest>,
    pub tracks: Vec<Track>,
    pub actions: Vec<Action>,
    pub layout: LayoutMode,
    pub toasts: Toasts,
    pub logo: Logo,
    pub system_dark: bool,
    theme_from: crate::theme::Palette,
    theme_to: crate::theme::Palette,
    theme_t: f32,
    pub srv: crate::server::ServerState,
    /// Screenshot tour: never talk to the server, use bundled sample data for signed-in screens.
    pub demo: bool,
    pub config_dir: PathBuf,
    pub dl: crate::data::downloads::Downloads,
    boot: Option<Task<Result<(Vec<Track>, Option<Manifest>)>>>,
    syllabi: Lazy<Syllabus>,
    study_idx: Lazy<StudyIndex>,
}

impl Env {
    pub fn new(ctx: Context, store: Store, system_dark: bool, config_dir: PathBuf) -> Self {
        let dark = Self::resolve_dark(&store, system_dark);
        let theme = Theme::new(dark);
        theme.apply(&ctx);
        let logo = Logo::load(&ctx);
        let repo = ContentRepo::new(&config_dir);
        crate::ui::remote_image::init(repo.clone());
        let mut env = Self {
            ctx,
            theme,
            store,
            repo,
            status: ContentStatus::Loading,
            manifest: None,
            tracks: vec![],
            actions: vec![],
            layout: LayoutMode::Wide,
            toasts: Toasts::default(),
            logo,
            system_dark,
            theme_from: Palette::light(),
            theme_to: Palette::light(),
            theme_t: 1.0,
            srv: Default::default(),
            demo: false,
            config_dir,
            dl: Default::default(),
            boot: None,
            syllabi: Lazy::default(),
            study_idx: Lazy::default(),
        };
        env.reload_content();
        env
    }

    fn resolve_dark(store: &Store, system_dark: bool) -> bool {
        match store.s.prefs.theme {
            ThemeMode::Dark => true,
            ThemeMode::Light => false,
            ThemeMode::System => system_dark,
        }
    }

    /// (Re)load the catalogue from the server (or the cache when offline).
    pub fn reload_content(&mut self) {
        self.syllabi.retry_failed();
        self.study_idx.retry_failed();
        self.status = ContentStatus::Loading;
        let repo = self.repo.clone();
        self.boot = Some(Task::spawn(&self.ctx, move || repo.bootstrap()));
    }

    /// Forget everything in memory too (after clearing the cache).
    pub fn drop_content_memory(&mut self) {
        self.syllabi.clear();
        self.study_idx.clear();
        crate::ui::remote_image::clear();
    }

    pub fn refresh_theme(&mut self) {
        let dark = Self::resolve_dark(&self.store, self.system_dark);
        if dark != self.theme.dark {
            // tween the palette instead of snapping (same switch the web does)
            self.theme_from = self.theme.p.clone();
            self.theme_to = Theme::new(dark).p;
            self.theme.dark = dark;
            self.theme_t = 0.0;
        }
    }

    /// Per-frame housekeeping: finish background jobs.
    pub fn poll(&mut self) {
        if self.theme_t < 1.0 {
            let dt = self.ctx.input(|i| i.stable_dt).clamp(0.001, 0.05);
            self.theme_t = if crate::theme::motion::reduced() { 1.0 } else { (self.theme_t + dt / 0.45).min(1.0) };
            self.theme.p = self.theme_from.lerp(&self.theme_to, crate::theme::motion::ease_io(self.theme_t));
            self.theme.apply(&self.ctx);
            self.ctx.request_repaint();
        }
        if let Some(t) = self.boot.as_mut() {
            if let Some(res) = t.poll() {
                self.boot = None;
                match res {
                    Ok((tracks, manifest)) => {
                        self.tracks = tracks;
                        self.manifest = manifest.or(self.manifest.take());
                        self.status = ContentStatus::Ready;
                        self.dl.scan(&self.ctx, &self.repo, &self.tracks);
                    }
                    Err(e) => self.status = ContentStatus::Failed(e.to_string()),
                }
            }
        }
        if !self.dl.jobs.is_empty() {
            self.ctx.request_repaint_after(std::time::Duration::from_millis(150));
        }
        for m in self.dl.poll() {
            self.toasts.push(m);
        }
        self.server_poll();
    }

    pub fn go(&mut self, r: Route) {
        self.actions.push(Action::Go(r));
    }
    pub fn act(&mut self, a: Action) {
        self.actions.push(a);
    }
    pub fn toast(&mut self, m: impl Into<String>) {
        self.toasts.push(m);
    }
    pub fn open_url(&mut self, url: &str) {
        self.actions.push(Action::OpenUrl(url.to_string()));
    }

    pub fn track(&self, grade: &str) -> Option<&Track> {
        self.tracks.iter().find(|t| t.grade == grade)
    }

    pub fn subject(&self, track: &str, subject: &str) -> Option<&SubjectSummary> {
        self.track(track)?.subjects.iter().find(|s| s.subject == subject)
    }

    /// Subject name, honouring the "Nepali names" preference.
    pub fn subject_name(&self, s: &SubjectSummary) -> String {
        if self.store.s.prefs.nepali_names && !s.name_ne.is_empty() {
            s.name_ne.clone()
        } else {
            s.name.clone()
        }
    }

    pub fn syllabus_view(&mut self, track: &str, subject: &str) -> View<Syllabus> {
        let (repo, t, sb) = (self.repo.clone(), track.to_string(), subject.to_string());
        self.syllabi.get(&self.ctx, &format!("{track}-{subject}"), move || repo.syllabus(&t, &sb))
    }

    pub fn study_index_view(&mut self, track: &str, subject: &str) -> View<StudyIndex> {
        let (repo, t, sb) = (self.repo.clone(), track.to_string(), subject.to_string());
        self.study_idx.get(&self.ctx, &format!("{track}-{subject}"), move || repo.study_index(&t, &sb))
    }

    pub fn syllabus(&mut self, track: &str, subject: &str) -> Option<Arc<Syllabus>> {
        match self.syllabus_view(track, subject) {
            View::Ready(v) => Some(v),
            _ => None,
        }
    }

    pub fn study_index(&mut self, track: &str, subject: &str) -> Option<Arc<StudyIndex>> {
        match self.study_index_view(track, subject) {
            View::Ready(v) => Some(v),
            _ => None,
        }
    }

    pub fn forget_subject(&mut self, track: &str, subject: &str) {
        let key = format!("{track}-{subject}");
        self.syllabi.forget(&key);
        self.study_idx.forget(&key);
    }

    /// Total number of readable chapters across the whole library.
    pub fn total_chapters(&self) -> u32 {
        self.tracks.iter().map(|t| t.ready_total()).sum()
    }

    /// Human title of a chapter (unit title from the syllabus, bank title from the study index).
    pub fn chapter_title(&mut self, c: &ChapterRef) -> String {
        match c.kind {
            ChapterKind::Unit => self.syllabus(&c.track, &c.subject).and_then(|s| s.units.iter().find(|u| u.no == c.no).map(|u| u.title.clone())).unwrap_or_else(|| format!("Unit {}", c.no)),
            ChapterKind::Bank => self.study_index(&c.track, &c.subject).and_then(|i| i.banks.iter().find(|b| b.no == c.no).map(|b| b.title.clone())).unwrap_or_else(|| "Question bank".into()),
            ChapterKind::Guide => self.study_index(&c.track, &c.subject).map(|i| i.guide.clone()).filter(|g| !g.is_empty()).unwrap_or_else(|| "Exam guide".into()),
        }
    }

    /// Toggle a bookmark and tell the user. Returns whether it is now bookmarked.
    pub fn toggle_bookmark(&mut self, c: &ChapterRef) -> bool {
        let title = self.chapter_title(c);
        let sname = self.subject(&c.track, &c.subject).map(|s| s.name.clone()).unwrap_or_default();
        let on = self.store.toggle_bookmark(c, &title, &sname);
        self.toast(if on { "Bookmarked" } else { "Bookmark removed" });
        on
    }

    pub fn motion(&self) -> bool {
        !self.store.s.prefs.reduce_motion
    }
}
