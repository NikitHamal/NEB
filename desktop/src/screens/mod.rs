//! One module per screen. Each exposes `show(ui, env, state)` and keeps its own
//! local state struct; shared plumbing lives in `common`.
pub mod about;
pub mod account;
pub mod auth_flow;
pub mod bookmarks;
pub mod books;
pub mod common;
pub mod community;
pub mod complete_profile;
pub mod downloads;
pub mod email_auth;
pub mod help;
pub mod history;
pub mod home;
pub mod legal;
pub mod legal_data;
pub mod library;
pub mod login;
pub mod notifications;
pub mod intro;
pub mod onboarding;
pub mod pdf;
pub mod people;
pub mod profile;
pub mod reader;
pub mod search;
pub mod settings;
pub mod splash;
pub mod subject;
pub mod user;

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
    pub books: books::BooksState,
    pub people: people::PeopleState,
    pub pdf: pdf::PdfState,
    pub intro: intro::IntroState,
    pub user: user::UserState,
    pub settings: settings::SettingsState,
    pub account: account::AccountState,
}
