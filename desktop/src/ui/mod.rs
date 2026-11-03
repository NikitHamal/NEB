//! Reusable widgets: icons, buttons, cards, navigation, menu bar, toasts.
pub mod avatar;
pub mod dialog;
pub mod icons;
pub mod logo;
pub mod remote_image;
pub mod nav;
pub mod shapes;
pub mod shapes_data;
pub mod shortcuts;
pub mod tabs;
pub mod theme_toggle;
pub mod toast;
pub mod widgets;

use crate::config::{BREAKPOINT_COMPACT, BREAKPOINT_RAIL};

/// How much chrome fits. Recomputed every frame from the window width.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum LayoutMode {
    /// Labelled sidebar.
    Wide,
    /// Icon-only rail.
    Rail,
    /// Bottom navigation bar.
    Compact,
}

impl LayoutMode {
    pub fn from_width(w: f32) -> Self {
        if w >= BREAKPOINT_RAIL {
            LayoutMode::Wide
        } else if w >= BREAKPOINT_COMPACT {
            LayoutMode::Rail
        } else {
            LayoutMode::Compact
        }
    }
}
