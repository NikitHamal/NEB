//! M3 Expressive colour roles: the SAME values as the website's `m3x/tokens.css`
//! (light = `:root`, dark = `[data-theme="dark"]`). Everything is a tonal ramp of the
//! NEBians logo blue, so a surface is never a neutral grey.
//!
//! Field names are the app's own vocabulary; the comment on each is the M3 role it maps to.
use egui::Color32;

macro_rules! palette {
    ($($f:ident),* $(,)?) => {
        #[derive(Clone, Debug)]
        pub struct Palette { $(pub $f: Color32),* }
        impl Palette {
            /// Component-wise blend, used for the animated light/dark switch.
            pub fn lerp(&self, to: &Palette, t: f32) -> Palette {
                Palette { $($f: super::mix(self.$f, to.$f, t)),* }
            }
        }
    };
}

palette!(
    page,                   // surface / background
    card,                   // surfaceContainerLowest (light) / surfaceContainer (dark)
    field,                  // surfaceContainerHigh
    ink,                    // onSurface
    ink_muted,              // onSurfaceVariant
    ink_faint,              // onSurfaceTertiary
    hairline,               // outlineVariant
    hairline_strong,        // outline
    accent,                 // primary
    accent_soft,            // primaryContainer
    on_accent,              // onPrimary
    danger,                 // error
    danger_soft,            // errorContainer
    ok,                     // aqua-d
    ok_soft,                // aqua-c
    warn,
    warn_soft,
    violet,                 // peri-d
    violet_soft,            // peri-c
    teal,                   // sky-d
    teal_soft,              // sky-c
    on_accent_soft,         // onPrimaryContainer
    secondary_container,
    on_secondary_container,
    surface_low,            // surfaceContainerLow
    surface_high,           // surfaceContainerHigh
    surface_highest,        // surfaceContainerHighest
    inverse,                // inverseSurface
    on_inverse,             // inverseOnSurface
    ink_brand,              // --ink: the deep logo blue used for hero panels
    on_ink_brand,           // --on-ink
);

const fn rgb(hex: u32) -> Color32 {
    Color32::from_rgb((hex >> 16) as u8, (hex >> 8) as u8, hex as u8)
}

impl Palette {
    pub fn light() -> Self {
        Self {
            page: rgb(0xF6F8FF),
            card: rgb(0xFFFFFF),
            field: rgb(0xE2E8F7),
            ink: rgb(0x0B1530),
            ink_muted: rgb(0x414B66),
            ink_faint: rgb(0x4F5976),
            hairline: rgb(0xC6D0EA),
            hairline_strong: rgb(0x707A96),
            accent: rgb(0x0058DF),
            accent_soft: rgb(0xDBE4FF),
            on_accent: rgb(0xFFFFFF),
            danger: rgb(0xBA1A1A),
            danger_soft: rgb(0xFFDAD6),
            ok: rgb(0x0A6A62),
            ok_soft: rgb(0xC6F3EB),
            warn: rgb(0x8A5A00),
            warn_soft: rgb(0xFFE9B8),
            violet: rgb(0x2A47A3),
            violet_soft: rgb(0xE3E9FF),
            teal: rgb(0x00598A),
            teal_soft: rgb(0xCDEEFF),
            on_accent_soft: rgb(0x001A52),
            secondary_container: rgb(0xDFE7FA),
            on_secondary_container: rgb(0x0F1C3B),
            surface_low: rgb(0xF0F4FE),
            surface_high: rgb(0xE2E8F7),
            surface_highest: rgb(0xDAE1F3),
            inverse: rgb(0x1F2840),
            on_inverse: rgb(0xEDF1FC),
            ink_brand: rgb(0x06235F),
            on_ink_brand: rgb(0xE6EEFF),
        }
    }

    pub fn dark() -> Self {
        Self {
            page: rgb(0x121318),
            card: rgb(0x1F1F25),
            field: rgb(0x292A2F),
            ink: rgb(0xE3E8F7),
            ink_muted: rgb(0xAAB4CE),
            ink_faint: rgb(0x8590AC),
            hairline: rgb(0x45464F),
            hairline_strong: rgb(0x79839F),
            accent: rgb(0xB2C5FF),
            accent_soft: rgb(0x003FA6),
            on_accent: rgb(0x002A78),
            danger: rgb(0xFFB4AB),
            danger_soft: rgb(0x93000A),
            ok: rgb(0x8AE9DA),
            ok_soft: rgb(0x0B3B37),
            warn: rgb(0xE8B457),
            warn_soft: rgb(0x32260E),
            violet: rgb(0xC1CCFF),
            violet_soft: rgb(0x25306A),
            teal: rgb(0x8FDCFF),
            teal_soft: rgb(0x0B3A52),
            on_accent_soft: rgb(0xDBE4FF),
            secondary_container: rgb(0x2A3858),
            on_secondary_container: rgb(0xDFE7FA),
            surface_low: rgb(0x1B1B21),
            surface_high: rgb(0x292A2F),
            surface_highest: rgb(0x2E2F36),
            inverse: rgb(0xE3E8F7),
            on_inverse: rgb(0x1F2840),
            ink_brand: rgb(0x16397F),
            on_ink_brand: rgb(0xE6EEFF),
        }
    }
}
