//! Screen routing with a back/forward history, mirroring Android's NavHost.
use crate::data::models::ChapterRef;

#[derive(Clone, Debug, PartialEq)]
pub enum Route {
    Splash,
    Login,
    EmailAuth,
    Onboarding,
    Home,
    Library,
    Category(String),
    Subject { track: String, subject: String },
    Reader(ChapterRef),
    Search,
    Bookmarks,
    Downloads,
    History,
    Help,
    Legal(String),
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
        !matches!(self, Route::Splash | Route::Login | Route::EmailAuth | Route::Onboarding | Route::CompleteProfile)
    }

    /// Which top-level destination should be highlighted.
    pub fn nav_root(&self) -> Route {
        match self {
            Route::Library | Route::Category(_) | Route::Subject { .. } | Route::Reader(_) => Route::Library,
            Route::Community | Route::Post(_) | Route::User(_) => Route::Community,
            Route::Profile => Route::Profile,
            Route::About | Route::Help | Route::Legal(_) => Route::Settings,
            Route::History => Route::Bookmarks,
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

    pub fn can_back(&self) -> bool {
        !self.back.is_empty()
    }
    pub fn can_forward(&self) -> bool {
        !self.forward.is_empty()
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
