//! One module per screen. Each exposes `show(ui, env, state)` and keeps its own
//! local state struct; shared plumbing lives in `common`.
pub mod about;
pub mod auth_flow;
pub mod bookmarks;
pub mod common;
pub mod community;
pub mod complete_profile;
pub mod downloads;
pub mod email_auth;
pub mod home;
pub mod library;
pub mod login;
pub mod notifications;
pub mod onboarding;
pub mod profile;
pub mod reader;
pub mod search;
pub mod settings;
pub mod splash;
pub mod subject;

/// Per-screen state, owned by `NebApp`.
#[derive(Default)]
pub struct Screens {
    pub splash: splash::SplashState,
    pub login: login::LoginState,
    pub complete: complete_profile::CompleteState,
    pub community: community::CommunityState,
    pub notifications: notifications::NotificationsState,
    pub email: email_auth::EmailState,
    pub onboarding: onboarding::OnboardingState,
    pub library: library::LibraryState,
    pub subject: subject::SubjectState,
    pub reader: reader::ReaderState,
    pub search: search::SearchState,
    pub downloads: downloads::DownloadsState,
    pub settings: settings::SettingsState,
    pub profile: profile::ProfileState,
}
