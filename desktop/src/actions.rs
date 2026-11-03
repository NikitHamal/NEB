//! UI → app commands. Screens never mutate the router or window directly; they
//! push an `Action` and `NebApp` applies it once per frame.
use crate::router::Route;

#[derive(Clone, Debug)]
pub enum Action {
    Go(Route),
    /// Jump to a route and drop the history (sign-in hand-offs).
    Replace(Route),
    Back,
    Forward,
    ToggleDark,
    Fullscreen,
    ShowShortcuts,
    /// Open the in-app Privacy / Terms sheet (works before sign-in).
    ShowLegal(String),
    /// Copy a link or address to the clipboard.
    Copy(String),
    OpenPath(std::path::PathBuf),
    SignOut,
    ResetAll,
    ReloadContent,
    Quit,
}
