//! Screen routing with a back/forward history, mirroring Android's NavHost.
use crate::data::models::ChapterRef;

/// Sections of the in-app account centre.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Default)]
pub enum AccountTab {
    #[default]
    Profile,
    Security,
    Privacy,
    Delete,
}

impl AccountTab {
    pub const ALL: [AccountTab; 4] = [AccountTab::Profile, AccountTab::Security, AccountTab::Privacy, AccountTab::Delete];
    pub fn index(self) -> usize {
        Self::ALL.iter().position(|t| *t == self).unwrap_or(0)
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum Route {
    Splash,
    Intro,
    Login,
    EmailAuth,
    Onboarding,
    Home,
    Library,
    Category(String),
    Subject { track: String, subject: String },
    Reader(ChapterRef),
    /// In-app PDF viewer for a downloaded book.
    Pdf(std::path::PathBuf),
    Search,
    Bookmarks,
    Downloads,
    History,
    Help,
    Legal(String),
    Account(AccountTab),
    Books,
    People,
    User(String),
    Settings,
    Profile,
    About,
    Community,
    Post(String),
    Notifications,
    CompleteProfile,
}

impl Route {
    /// Routes that show the app shell (menu + navigation). Splash and the
    /// sign-in journey run full-bleed, like on Android.
    pub fn has_shell(&self) -> bool {
        !matches!(self, Route::Splash | Route::Intro | Route::Login | Route::EmailAuth | Route::Onboarding | Route::CompleteProfile)
    }

    /// Which top-level destination should be highlighted.
    pub fn nav_root(&self) -> Route {
        match self {
            Route::Library | Route::Category(_) | Route::Subject { .. } | Route::Reader(_) => Route::Library,
            Route::Community | Route::Post(_) | Route::User(_) => Route::Community,
            Route::Profile | Route::Account(_) => Route::Profile,
            Route::About | Route::Help | Route::Legal(_) => Route::Settings,
            Route::History => Route::Bookmarks,
            Route::Pdf(_) => Route::Books,
            other => other.clone(),
        }
    }

    /// Entry/exit points of the journey are never put in history.
    fn transient(&self) -> bool {
        !self.has_shell()
    }
}

#[derive(Debug)]
pub struct Router {
    pub current: Route,
    back: Vec<Route>,
    forward: Vec<Route>,
}

impl Router {
    pub fn new(start: Route) -> Self {
        Self { current: start, back: vec![], forward: vec![] }
    }

    pub fn navigate(&mut self, to: Route) {
        if to == self.current {
            return;
        }
        if !self.current.transient() {
            self.back.push(self.current.clone());
            if self.back.len() > 64 {
                self.back.remove(0);
            }
        }
        self.forward.clear();
        self.current = to;
    }

    /// Replace the current route without touching history (splash, sign-in hand-offs).
    pub fn replace(&mut self, to: Route) {
        self.current = to;
        self.back.clear();
        self.forward.clear();
    }

    pub fn back(&mut self) -> bool {
        if let Some(prev) = self.back.pop() {
            let cur = std::mem::replace(&mut self.current, prev);
            if !cur.transient() {
                self.forward.push(cur);
            }
            true
        } else {
            false
        }
    }

    pub fn forward(&mut self) -> bool {
        if let Some(next) = self.forward.pop() {
            let cur = std::mem::replace(&mut self.current, next);
            self.back.push(cur);
            true
        } else {
            false
        }
    }
}
