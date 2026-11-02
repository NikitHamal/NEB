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
    ZoomIn,
    ZoomOut,
    ZoomReset,
    Fullscreen,
    ShowShortcuts,
    OpenUrl(String),
    OpenPath(std::path::PathBuf),
    Toast(String),
    SignOut,
    ResetAll,
    ReloadContent,
    Quit,
}
