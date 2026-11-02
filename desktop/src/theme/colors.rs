//! Material 3 palettes (Android `ui/theme/Palette.kt`: md_theme_light_* / md_theme_dark_*).
//! Field names are the app's own vocabulary; each maps to an M3 colour role (see comments).
//! Legacy notes: Light/dark values are copied from the Android app's
//! `ui/theme/NebAuthPalette.kt` (page, card, field, ink, hairlines, brand #004AC6 /
//! #B4C5FF). The semantic greens/ambers are the Android `Color.kt` accent pairs.
use egui::Color32;

#[derive(Clone, Debug)]
pub struct Palette {
    pub page: Color32,
    pub card: Color32,
    pub field: Color32,
    pub ink: Color32,
    pub ink_muted: Color32,
    pub ink_faint: Color32,
    pub hairline: Color32,
    pub hairline_strong: Color32,
    pub accent: Color32,
    pub accent_soft: Color32,
    pub on_accent: Color32,
    pub danger: Color32,
    pub danger_soft: Color32,
    pub ok: Color32,
    pub ok_soft: Color32,
    pub warn: Color32,
    pub warn_soft: Color32,
    pub violet: Color32,
    pub violet_soft: Color32,
    pub teal: Color32,
    pub teal_soft: Color32,
    // --- Material 3 roles added for the expressive redesign ---
    pub on_accent_soft: Color32,        // onPrimaryContainer
    pub secondary_container: Color32,   // secondaryContainer (nav indicator, selected chips, tonal buttons)
    pub on_secondary_container: Color32,
    pub surface_high: Color32,          // surfaceContainerHigh
    pub surface_highest: Color32,       // surfaceContainerHighest
    pub inverse: Color32,               // inverseSurface (snackbars)
    pub on_inverse: Color32,            // inverseOnSurface
}

const fn rgb(hex: u32) -> Color32 {
    Color32::from_rgb((hex >> 16) as u8, (hex >> 8) as u8, hex as u8)
}

impl Palette {
    pub fn light() -> Self {
        Self {
            page: rgb(0xF3F4F6),
            card: rgb(0xFFFFFF),
            field: rgb(0xE7E9ED),
            ink: rgb(0x1D1F25),
            ink_muted: rgb(0x525663),
            ink_faint: rgb(0x6B707D),
            hairline: rgb(0xE0E2E7),
            hairline_strong: rgb(0xB7BCC6),
            accent: rgb(0x004AC6),
            accent_soft: rgb(0xDBE1FF),
            on_accent: rgb(0xFFFFFF),
            danger: rgb(0xBA1A1A),
            danger_soft: rgb(0xFFDAD6),
            ok: rgb(0x15803D),
            ok_soft: rgb(0xDCFCE7),
            warn: rgb(0x9A6206),
            warn_soft: rgb(0xFEF3C7),
            violet: rgb(0x6D45C4),
            violet_soft: rgb(0xEBE6FE),
            teal: rgb(0x0F766E),
            teal_soft: rgb(0xCCFBF1),
            on_accent_soft: rgb(0x00174B),
            secondary_container: rgb(0xDCE2EB),
            on_secondary_container: rgb(0x111A28),
            surface_high: rgb(0xE7E9ED),
            surface_highest: rgb(0xE0E2E7),
            inverse: rgb(0x2B2D35),
            on_inverse: rgb(0xEFF0F3),
        }
    }

    pub fn dark() -> Self {
        Self {
            page: rgb(0x191B20),
            card: rgb(0x212329),
            field: rgb(0x2B2D35),
            ink: rgb(0xE7E9ED),
            ink_muted: rgb(0xA9AEB9),
            ink_faint: rgb(0x878C99),
            hairline: rgb(0x31343C),
            hairline_strong: rgb(0x4B4F5A),
            accent: rgb(0xB4C5FF),
            accent_soft: rgb(0x003EA8),
            on_accent: rgb(0x002D78),
            danger: rgb(0xFFB4AB),
            danger_soft: rgb(0x93000A),
            ok: rgb(0x7CD9A0),
            ok_soft: rgb(0x14301F),
            warn: rgb(0xE8B457),
            warn_soft: rgb(0x32260E),
            violet: rgb(0xC4B5FD),
            violet_soft: rgb(0x4C2A93),
            teal: rgb(0x5FD3C4),
            teal_soft: rgb(0x10302D),
            on_accent_soft: rgb(0xDBE1FF),
            secondary_container: rgb(0x20293B),
            on_secondary_container: rgb(0xDCE2EB),
            surface_high: rgb(0x2B2D35),
            surface_highest: rgb(0x31343C),
            inverse: rgb(0xE7E9ED),
            on_inverse: rgb(0x1D1F25),
        }
    }
}
