//! Account centre — everything the website's account pages offer, built natively:
//! edit profile, security (email, password), privacy & terms viewer, and account deletion.
mod delete;
mod edit;
mod security;

use egui::Ui;

use super::common::*;
use crate::data::account::{Deletion, Security};
use crate::data::store::Session;
use crate::data::tasks::Task;
use crate::env::Env;
use crate::errors::Result;
use crate::router::{AccountTab, Route};
use crate::theme::motion;
use crate::ui::icons::Icon;
use crate::ui::{tabs, widgets};

/// What a background account request resolves to.
pub enum Out {
    Msg(String),
    Session(Session),
    Sec(Security),
    Del(Deletion),
    Done,
}
pub type Job = Task<Result<Out>>;

/// Poll a job; session expiry is handled centrally. `Some(Ok|Err(text))` once it finishes.
pub fn poll(env: &mut Env, job: &mut Option<Job>) -> Option<std::result::Result<Out, String>> {
    let r = job.as_mut()?.poll()?;
    *job = None;
    match r {
        Ok(o) => Some(Ok(o)),
        Err(e) => {
            if env.handle_api_error(&e) {
                None
            } else {
                Some(Err(e.to_string()))
            }
        }
    }
}

#[derive(Default)]
pub struct AccountState {
    edit: edit::EditState,
    security: security::SecurityState,
    delete: delete::DeleteState,
    legal_doc: usize,
    last: Option<AccountTab>,
}

impl AccountState {
    /// Open the delete-confirmation dialog (screenshot tour).
    pub fn demo_delete_dialog(&mut self) {
        self.delete.demo_confirm();
    }
    /// Open the change-password dialog (screenshot tour).
    pub fn demo_password_dialog(&mut self) {
        self.security.demo_password();
    }
}

pub fn show(ui: &mut Ui, env: &mut Env, st: &mut AccountState, tab: AccountTab) {
    let key = egui::Id::new(("account-tab", tab));
    if st.last != Some(tab) {
        st.last = Some(tab);
        motion::reset_enter(ui.ctx(), key);
        match tab {
            AccountTab::Security => st.security.refresh(),
            AccountTab::Delete => st.delete.refresh(),
            _ => {}
        }
    }
    scroll_page(ui, env, &format!("account-{tab:?}"), |ui, env| {
        let th = env.theme.clone();
        widgets::screen_header(ui, &th, "Account");
        let mut sel = tab.index();
        let items = [("Profile", Icon::User), ("Security", Icon::Lock), ("Privacy", Icon::Shield), ("Delete", Icon::Trash)];
        if tabs::show(ui, &th, &items, &mut sel) {
            env.go(Route::Account(AccountTab::ALL[sel]));
        }
        ui.add_space(22.0);
        rise(ui, key);
        match tab {
            AccountTab::Profile => edit::show(ui, env, &mut st.edit),
            AccountTab::Security => security::show(ui, env, &mut st.security),
            AccountTab::Privacy => {
                let mut i = st.legal_doc;
                if widgets::segmented(ui, &th, &["Privacy Policy", "Terms of Service"], &mut i) {
                    st.legal_doc = i;
                }
                ui.add_space(16.0);
                super::legal::body(ui, &th, super::legal::doc_for(if st.legal_doc == 1 { "terms" } else { "privacy" }));
            }
            AccountTab::Delete => delete::show(ui, env, &mut st.delete),
        }
    });
}
