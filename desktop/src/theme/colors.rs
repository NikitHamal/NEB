//! Palettes. Light/dark values are copied from the Android app's
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
}

const fn rgb(hex: u32) -> Color32 {
    Color32::from_rgb((hex >> 16) as u8, (hex >> 8) as u8, hex as u8)
}

impl Palette {
    pub fn light() -> Self {
        Self {
            page: rgb(0xFFFFFF),
            card: rgb(0xFFFFFF),
            field: rgb(0xF4F4F5),
            ink: rgb(0x0A0A0B),
            ink_muted: rgb(0x5C5C61),
            ink_faint: rgb(0x9B9BA1),
            hairline: rgb(0xE9E9EB),
            hairline_strong: rgb(0xD5D5D9),
            accent: rgb(0x004AC6),
            accent_soft: rgb(0xEDF0FF),
            on_accent: rgb(0xFFFFFF),
            danger: rgb(0xB3261E),
            danger_soft: rgb(0xFBEDEC),
            ok: rgb(0x15803D),
            ok_soft: rgb(0xDCFCE7),
            warn: rgb(0x9A6206),
            warn_soft: rgb(0xFEF3C7),
            violet: rgb(0x6D28D9),
            violet_soft: rgb(0xEDE9FE),
            teal: rgb(0x0F766E),
            teal_soft: rgb(0xCCFBF1),
        }
    }

    pub fn dark() -> Self {
        Self {
            page: rgb(0x0C0C0D),
            card: rgb(0x131315),
            field: rgb(0x17171A),
            ink: rgb(0xF5F5F6),
            ink_muted: rgb(0xA1A1A8),
            ink_faint: rgb(0x6E6E75),
            hairline: rgb(0x222225),
            hairline_strong: rgb(0x313136),
            accent: rgb(0xB4C5FF),
            accent_soft: rgb(0x16233F),
            on_accent: rgb(0x002D78),
            danger: rgb(0xF2716A),
            danger_soft: rgb(0x2A1614),
            ok: rgb(0x7CD9A0),
            ok_soft: rgb(0x14301F),
            warn: rgb(0xE8B457),
            warn_soft: rgb(0x32260E),
            violet: rgb(0xC4B5FD),
            violet_soft: rgb(0x261C46),
            teal: rgb(0x5FD3C4),
            teal_soft: rgb(0x10302D),
        }
    }
}
