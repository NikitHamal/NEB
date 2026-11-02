//! Everything the app remembers between launches: preferences, profile,
//! session, bookmarks, reading progress, window size. Plain JSON in the OS
//! config directory, written atomically.
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

use serde::{Deserialize, Serialize};

use crate::data::models::ChapterRef;
use crate::util::now_secs;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum ThemeMode {
    System,
    Light,
    Dark,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum ReadingWidth {
    Compact,
    Comfortable,
    Wide,
}

impl ReadingWidth {
    pub fn px(self) -> f32 {
        match self {
            ReadingWidth::Compact => 620.0,
            ReadingWidth::Comfortable => 740.0,
            ReadingWidth::Wide => 900.0,
        }
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(default)]
pub struct Prefs {
    pub theme: ThemeMode,
    pub font_scale: f32,
    pub reading_width: ReadingWidth,
    pub reduce_motion: bool,
    pub nepali_names: bool,
    pub remember_window: bool,
    pub show_toc: bool,
    pub content_dir: Option<String>,
}

impl Default for Prefs {
    fn default() -> Self {
        Self {
            theme: ThemeMode::System,
            font_scale: 1.0,
            reading_width: ReadingWidth::Comfortable,
            reduce_motion: false,
            nepali_names: false,
            remember_window: true,
            show_toc: true,
            content_dir: None,
        }
    }
}

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
#[serde(default)]
pub struct Profile {
    pub role: String,
    pub display_name: String,
    pub handle: String,
    pub dob: String,
    pub gender: String,
    pub level: String,
    pub subjects: Vec<String>,
    pub pradesh: String,
    pub district: String,
    pub school: String,
    pub institution_type: String,
    pub avatar_tone: usize,
    pub bio: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Session {
    pub email: String,
    pub username: String,
    pub token: String,
    #[serde(default)]
    pub user_id: String,
    #[serde(default)]
    pub display_name: String,
    #[serde(default)]
    pub photo_url: String,
    /// "email" | "browser" (Google / GitHub through the website)
    #[serde(default)]
    pub provider: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Bookmark {
    pub chapter: ChapterRef,
    pub title: String,
    pub subject_name: String,
    pub ts: u64,
}

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct Progress {
    pub scroll: f32,
    pub done: bool,
    pub ts: u64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Recent {
    pub chapter: ChapterRef,
    pub title: String,
    pub subject_name: String,
    pub color: String,
    pub ts: u64,
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct WindowGeom {
    pub w: f32,
    pub h: f32,
    pub x: Option<f32>,
    pub y: Option<f32>,
}

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
#[serde(default)]
pub struct PersistedState {
    pub prefs: Prefs,
    pub profile: Profile,
    pub onboarded: bool,
    pub guest: bool,
    pub session: Option<Session>,
    pub bookmarks: Vec<Bookmark>,
    pub progress: HashMap<String, Progress>,
    pub recent: Vec<Recent>,
    pub window: Option<WindowGeom>,
}

pub struct Store {
    pub s: PersistedState,
    path: PathBuf,
    dirty: bool,
    last_save: Instant,
}

impl Store {
    pub fn load(dir: &Path, reset: bool) -> Self {
        let path = dir.join("desktop-state.json");
        let s = if reset {
            PersistedState::default()
        } else {
            std::fs::read_to_string(&path).ok().and_then(|t| serde_json::from_str(&t).ok()).unwrap_or_default()
        };
        Self { s, path, dirty: false, last_save: Instant::now() }
    }

    pub fn default_dir() -> PathBuf {
        dirs::config_dir().unwrap_or_else(|| PathBuf::from(".")).join("NEBians")
    }

    pub fn touch(&mut self) {
        self.dirty = true;
    }

    pub fn flush_if_due(&mut self) {
        if self.dirty && self.last_save.elapsed() > Duration::from_millis(1500) {
            self.save();
        }
    }

    pub fn save(&mut self) {
        if let Some(parent) = self.path.parent() {
            let _ = std::fs::create_dir_all(parent);
        }
        if let Ok(txt) = serde_json::to_string_pretty(&self.s) {
            let tmp = self.path.with_extension("json.tmp");
            if std::fs::write(&tmp, txt).is_ok() {
                let _ = std::fs::rename(&tmp, &self.path);
            }
        }
        self.dirty = false;
        self.last_save = Instant::now();
    }

    pub fn path(&self) -> &Path {
        &self.path
    }

    // ---- bookmarks ----
    pub fn is_bookmarked(&self, c: &ChapterRef) -> bool {
        self.s.bookmarks.iter().any(|b| &b.chapter == c)
    }

    /// Returns `true` when the chapter is now bookmarked.
    pub fn toggle_bookmark(&mut self, c: &ChapterRef, title: &str, subject_name: &str) -> bool {
        self.touch();
        if let Some(i) = self.s.bookmarks.iter().position(|b| &b.chapter == c) {
            self.s.bookmarks.remove(i);
            false
        } else {
            self.s.bookmarks.insert(0, Bookmark { chapter: c.clone(), title: title.into(), subject_name: subject_name.into(), ts: now_secs() });
            true
        }
    }

    // ---- progress ----
    pub fn progress(&self, c: &ChapterRef) -> Option<&Progress> {
        self.s.progress.get(&c.key())
    }

    pub fn set_scroll(&mut self, c: &ChapterRef, scroll: f32) {
        let e = self.s.progress.entry(c.key()).or_default();
        if (e.scroll - scroll).abs() > 4.0 {
            e.scroll = scroll;
            e.ts = now_secs();
            self.dirty = true;
        }
    }

    pub fn set_done(&mut self, c: &ChapterRef, done: bool) {
        let e = self.s.progress.entry(c.key()).or_default();
        e.done = done;
        e.ts = now_secs();
        self.dirty = true;
    }

    pub fn done_count_in(&self, track: &str, subject: &str) -> u32 {
        let prefix = format!("{track}-{subject}/unit-");
        self.s.progress.iter().filter(|(k, p)| p.done && k.starts_with(&prefix)).count() as u32
    }

    pub fn total_done(&self) -> usize {
        self.s.progress.values().filter(|p| p.done).count()
    }

    pub fn push_recent(&mut self, c: &ChapterRef, title: &str, subject_name: &str, color: &str) {
        self.s.recent.retain(|r| &r.chapter != c);
        self.s.recent.insert(0, Recent { chapter: c.clone(), title: title.into(), subject_name: subject_name.into(), color: color.into(), ts: now_secs() });
        self.s.recent.truncate(12);
        self.dirty = true;
    }

    pub fn display_name(&self) -> String {
        let n = self.s.profile.display_name.trim();
        if n.is_empty() {
            "Student".into()
        } else {
            n.split_whitespace().next().unwrap_or(n).to_string()
        }
    }
}
