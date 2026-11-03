//! Spacing and shape tokens: Android `NEBiansShapes` (6/10/14/20/28dp) — cards use 20, panels 28,
//! pills 999.
/// The web scale (`--md-shape-*`): 8 / 12 / 16 / 24 / 32 / 44, pill = 28 (finite on purpose so a
/// spring overshoot never collapses a pill to a square).
pub const SHAPE_XS: f32 = 8.0;
pub const SHAPE_SM: f32 = 12.0;
pub const SHAPE_MD: f32 = 16.0;
pub const SHAPE_LG: f32 = 24.0;
pub const SHAPE_XL: f32 = 32.0;
pub const CARD_RADIUS: f32 = SHAPE_LG;
pub const PANEL_RADIUS: f32 = SHAPE_XL;
/// Shape a pressed button morphs towards (Material 3 Expressive).
pub const PRESSED_RADIUS: f32 = 14.0;
pub const PILL: f32 = 999.0;

pub const PAGE_PAD: f32 = 28.0;
pub const PAGE_PAD_COMPACT: f32 = 16.0;
pub const SECTION_GAP: f32 = 28.0;
pub const GRID_GAP: f32 = 14.0;
/// Pages never stretch beyond this, even on ultra-wide monitors.
pub const MAX_CONTENT_W: f32 = 1120.0;
