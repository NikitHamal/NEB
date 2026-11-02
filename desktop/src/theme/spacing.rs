//! Spacing and shape tokens: Android `NEBiansShapes` (6/10/14/20/28dp) — cards use 20, panels 28,
//! pills 999.
pub const CARD_RADIUS: f32 = 20.0;
pub const PANEL_RADIUS: f32 = 28.0;
/// Shape a pressed button morphs towards (Material 3 Expressive).
pub const PRESSED_RADIUS: f32 = 14.0;
pub const PILL: f32 = 999.0;

pub const PAGE_PAD: f32 = 28.0;
pub const PAGE_PAD_COMPACT: f32 = 16.0;
pub const SECTION_GAP: f32 = 28.0;
pub const GRID_GAP: f32 = 14.0;
/// Pages never stretch beyond this, even on ultra-wide monitors.
pub const MAX_CONTENT_W: f32 = 1120.0;
