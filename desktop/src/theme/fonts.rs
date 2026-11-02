//! Fonts. Poppins (the brand face on web + Android) is embedded from
//! `assets/fonts`; Poppins' Devanagari subset (converted from the repo's woff2)
//! covers Nepali labels. egui's bundled fonts remain as fallbacks for maths
//! symbols (Greek, arrows, operators) that Poppins does not contain.
use egui::{Context, FontData, FontDefinitions, FontFamily, FontId};

pub const MEDIUM: &str = "medium";
pub const BOLD: &str = "bold";

pub fn regular(size: f32) -> FontId {
    FontId::new(size, FontFamily::Proportional)
}
pub fn medium(size: f32) -> FontId {
    FontId::new(size, FontFamily::Name(MEDIUM.into()))
}
pub fn bold(size: f32) -> FontId {
    FontId::new(size, FontFamily::Name(BOLD.into()))
}
pub fn medium_family() -> FontFamily {
    FontFamily::Name(MEDIUM.into())
}
pub fn bold_family() -> FontFamily {
    FontFamily::Name(BOLD.into())
}

pub fn install(ctx: &Context) {
    let mut fonts = FontDefinitions::default();
    let add = |fonts: &mut FontDefinitions, name: &str, bytes: &'static [u8]| {
        fonts.font_data.insert(name.to_owned(), FontData::from_static(bytes));
    };
    add(&mut fonts, "poppins-regular", include_bytes!("../../assets/fonts/poppins_regular.ttf"));
    add(&mut fonts, "poppins-medium", include_bytes!("../../assets/fonts/poppins_medium.ttf"));
    add(&mut fonts, "poppins-bold", include_bytes!("../../assets/fonts/poppins_bold.ttf"));
    add(&mut fonts, "poppins-deva-400", include_bytes!("../../assets/fonts/poppins-devanagari-400.ttf"));
    add(&mut fonts, "poppins-deva-600", include_bytes!("../../assets/fonts/poppins-devanagari-600.ttf"));

    let fallbacks: Vec<String> = fonts.families.get(&FontFamily::Proportional).cloned().unwrap_or_default();
    let mono_fallback: Vec<String> = fonts.families.get(&FontFamily::Monospace).cloned().unwrap_or_default();
    let tail = |extra: &[&str]| -> Vec<String> {
        let mut v: Vec<String> = extra.iter().map(|s| s.to_string()).collect();
        v.extend(fallbacks.iter().cloned());
        v.extend(mono_fallback.iter().filter(|m| !fallbacks.contains(m)).cloned());
        v
    };
    fonts.families.insert(FontFamily::Proportional, tail(&["poppins-regular", "poppins-deva-400"]));
    fonts.families.insert(FontFamily::Name(MEDIUM.into()), tail(&["poppins-medium", "poppins-deva-600"]));
    fonts.families.insert(FontFamily::Name(BOLD.into()), tail(&["poppins-bold", "poppins-deva-600"]));
    ctx.set_fonts(fonts);
}
