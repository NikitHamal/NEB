//! `Env` — the shared services every screen receives: theme, persisted store,
//! content root, cached syllabus data, the action queue and toasts.
//! Screens keep their own local state and talk to the rest of the app through `Env`.
use std::collections::HashMap;
use std::path::PathBuf;
use std::sync::Arc;

use egui::Context;

use crate::actions::Action;
use crate::data::content::ContentRoot;
use crate::data::models::*;
use crate::data::search::SearchIndex;
use crate::data::store::{Store, ThemeMode};
use crate::data::tasks::Task;
use crate::router::Route;
use crate::theme::Theme;
use crate::ui::logo::Logo;
use crate::ui::toast::Toasts;
use crate::ui::LayoutMode;

pub struct Env {
    pub ctx: Context,
    pub theme: Theme,
    pub store: Store,
    pub content: Option<ContentRoot>,
    pub content_error: Option<String>,
    pub tracks: Vec<Track>,
    pub actions: Vec<Action>,
    pub layout: LayoutMode,
    pub toasts: Toasts,
    pub logo: Logo,
    pub system_dark: bool,
    pub config_dir: PathBuf,
    pub search_index: Option<Arc<SearchIndex>>,
    search_task: Option<Task<SearchIndex>>,
    syllabi: HashMap<String, Option<Arc<Syllabus>>>,
    study_idx: HashMap<String, Option<Arc<StudyIndex>>>,
}

impl Env {
    pub fn new(ctx: Context, store: Store, content: Option<ContentRoot>, system_dark: bool, config_dir: PathBuf) -> Self {
        let dark = Self::resolve_dark(&store, system_dark);
        let theme = Theme::new(dark);
        theme.apply(&ctx);
        let logo = Logo::load(&ctx);
        let mut env = Self {
            ctx,
            theme,
            store,
            content: None,
            content_error: None,
            tracks: vec![],
            actions: vec![],
            layout: LayoutMode::Wide,
            toasts: Toasts::default(),
            logo,
            system_dark,
            config_dir,
            search_index: None,
            search_task: None,
            syllabi: HashMap::new(),
            study_idx: HashMap::new(),
        };
        env.set_content(content);
        env
    }

    fn resolve_dark(store: &Store, system_dark: bool) -> bool {
        match store.s.prefs.theme {
            ThemeMode::Dark => true,
            ThemeMode::Light => false,
            ThemeMode::System => system_dark,
        }
    }

    /// (Re)load the track index from a content root and start building the search index.
    pub fn set_content(&mut self, content: Option<ContentRoot>) {
        self.syllabi.clear();
        self.study_idx.clear();
        self.search_index = None;
        self.search_task = None;
        self.tracks.clear();
        self.content_error = None;
        match content {
            Some(root) => match root.tracks() {
                Ok(t) => {
                    let r2 = root.clone();
                    let t2 = t.clone();
                    self.search_task = Some(Task::spawn(&self.ctx, move || SearchIndex::build(&r2, &t2)));
                    self.tracks = t;
                    self.content = Some(root);
                }
                Err(e) => {
                    self.content_error = Some(format!("Found the content folder but could not read it: {e}"));
                    self.content = Some(root);
                }
            },
            None => {
                self.content_error = Some("NEBians could not find its study content. Point it at your NEB checkout in Settings.".into());
                self.content = None;
            }
        }
    }

    pub fn refresh_theme(&mut self) {
        let dark = Self::resolve_dark(&self.store, self.system_dark);
        if dark != self.theme.dark {
            self.theme = Theme::new(dark);
            self.theme.apply(&self.ctx);
        }
    }

    /// Per-frame housekeeping: finish background jobs.
    pub fn poll(&mut self) {
        if let Some(t) = self.search_task.as_mut() {
            if let Some(idx) = t.poll() {
                self.search_index = Some(Arc::new(idx));
                self.search_task = None;
            }
        }
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

    pub fn syllabus(&mut self, track: &str, subject: &str) -> Option<Arc<Syllabus>> {
        let key = format!("{track}-{subject}");
        if !self.syllabi.contains_key(&key) {
            let v = self.content.as_ref().and_then(|c| c.syllabus(track, subject).ok()).map(Arc::new);
            self.syllabi.insert(key.clone(), v);
        }
        self.syllabi.get(&key).cloned().flatten()
    }

    pub fn study_index(&mut self, track: &str, subject: &str) -> Option<Arc<StudyIndex>> {
        let key = format!("{track}-{subject}");
        if !self.study_idx.contains_key(&key) {
            let v = self.content.as_ref().and_then(|c| c.study_index(track, subject).ok()).map(Arc::new);
            self.study_idx.insert(key.clone(), v);
        }
        self.study_idx.get(&key).cloned().flatten()
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
