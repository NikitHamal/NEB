//! What happens after *any* successful sign-in (email, Google, GitHub): persist the session,
//! sync the profile from the account and choose the next screen.
use crate::actions::Action;
use crate::data::store::Session;
use crate::env::Env;
use crate::router::Route;

pub fn complete_sign_in(env: &mut Env, s: Session, is_new: bool) {
    {
        let p = &mut env.store.s.profile;
        if p.handle.is_empty() {
            p.handle = s.username.clone();
        }
        if p.display_name.is_empty() {
            p.display_name = if s.display_name.is_empty() { s.username.clone() } else { s.display_name.clone() };
        }
    }
    env.store.s.session = Some(s);
    env.store.s.guest = false;
    env.store.touch();
    env.srv.refresh_unread_soon();
    env.pull_profile();
    let next = if is_new {
        Route::CompleteProfile
    } else if !env.store.s.onboarded {
        Route::Onboarding
    } else {
        Route::Home
    };
    env.toast("Signed in");
    env.act(Action::Replace(next));
}

/// Continue without an account (Android's "Continue as guest").
pub fn continue_as_guest(env: &mut Env) {
    env.store.s.guest = true;
    if env.store.s.profile.role.is_empty() {
        env.store.s.profile.role = "explorer".into();
    }
    env.store.touch();
    let next = if env.store.s.onboarded { Route::Home } else { Route::Onboarding };
    env.act(Action::Replace(next));
}
