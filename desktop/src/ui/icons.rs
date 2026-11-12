//! Material Icons (Rounded) — Google's official icon font, embedded and drawn as glyphs.
//! The codepoints below come straight from `assets/fonts/MaterialIconsRound-Regular.codepoints`,
//! so every icon is the same artwork the Android app's `material-icons` set ships.
#![allow(dead_code)] // wire/icon sets mirror the server and Material font in full
use egui::{Align2, Color32, FontFamily, FontId, Painter, Rect};

pub const FAMILY: &str = "material-icons";

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Icon {
    Home,
    Library,
    Search,
    Bookmark,
    BookmarkFilled,
    Download,
    Settings,
    Back,
    Forward,
    ChevronRight,
    ChevronDown,
    ChevronUp,
    Check,
    Close,
    Plus,
    Minus,
    User,
    Info,
    Clock,
    Contrast,
    External,
    Folder,
    Trash,
    Eye,
    EyeOff,
    Keyboard,
    Globe,
    Lock,
    Bolt,
    File,
    Menu,
    Play,
    School,
    Edit,
    Mail,
    Logout,
    List,
    Text,
    Forum,
    Chat,
    Bell,
    BellOff,
    ThumbUp,
    ThumbUpFilled,
    Send,
    Share,
    More,
    Refresh,
    DarkMode,
    LightMode,
    Key,
    Verified,
    Shield,
    History,
    Star,
    Trending,
    Article,
    Warning,
    Error,
    Done,
    Sort,
    Tag,
    Palette,
    Storage,
    Help,
    Person,
    Login,
    Cloud,
    Sync,
    Flag,
    Add,
    Stories,
    Quiz,
    Calendar,
    Bar,
    Archive,
    Compose,
    Reply,
    PersonAdd,
    Badge,
    Dashboard,
    Tune,
}

impl Icon {
    /// The Unicode private-use codepoint of this icon in the Material font.
    pub const fn glyph(self) -> char {
        match self {
            Icon::Home => '\u{e88a}', // home
            Icon::Library => '\u{ea19}', // menu_book
            Icon::Search => '\u{e8b6}', // search
            Icon::Bookmark => '\u{e867}', // bookmark_border
            Icon::BookmarkFilled => '\u{e866}', // bookmark
            Icon::Download => '\u{f090}', // download
            Icon::Settings => '\u{e8b8}', // settings
            Icon::Back => '\u{e5c4}', // arrow_back
            Icon::Forward => '\u{e5c8}', // arrow_forward
            Icon::ChevronRight => '\u{e5cc}', // chevron_right
            Icon::ChevronDown => '\u{e5cf}', // expand_more
            Icon::ChevronUp => '\u{e5ce}', // expand_less
            Icon::Check => '\u{e5ca}', // check
            Icon::Close => '\u{e5cd}', // close
            Icon::Plus => '\u{e145}', // add
            Icon::Minus => '\u{e15b}', // remove
            Icon::User => '\u{e7fd}', // person
            Icon::Info => '\u{e88e}', // info
            Icon::Clock => '\u{e8b5}', // schedule
            Icon::Contrast => '\u{eb37}', // contrast
            Icon::External => '\u{e89e}', // open_in_new
            Icon::Folder => '\u{e2c8}', // folder_open
            Icon::Trash => '\u{e872}', // delete
            Icon::Eye => '\u{e8f4}', // visibility
            Icon::EyeOff => '\u{e8f5}', // visibility_off
            Icon::Keyboard => '\u{e312}', // keyboard
            Icon::Globe => '\u{e894}', // language
            Icon::Lock => '\u{e897}', // lock
            Icon::Bolt => '\u{ea0b}', // bolt
            Icon::File => '\u{e873}', // description
            Icon::Menu => '\u{e5d2}', // menu
            Icon::Play => '\u{e037}', // play_arrow
            Icon::School => '\u{e80c}', // school
            Icon::Edit => '\u{e3c9}', // edit
            Icon::Mail => '\u{e158}', // mail
            Icon::Logout => '\u{e9ba}', // logout
            Icon::List => '\u{e896}', // list
            Icon::Text => '\u{e262}', // text_fields
            Icon::Forum => '\u{e0bf}', // forum
            Icon::Chat => '\u{e0cb}', // chat_bubble_outline
            Icon::Bell => '\u{e7f4}', // notifications
            Icon::BellOff => '\u{e7f6}', // notifications_off
            Icon::ThumbUp => '\u{e9f3}', // thumb_up_off_alt
            Icon::ThumbUpFilled => '\u{e8dc}', // thumb_up
            Icon::Send => '\u{e163}', // send
            Icon::Share => '\u{e80d}', // share
            Icon::More => '\u{e5d4}', // more_vert
            Icon::Refresh => '\u{e5d5}', // refresh
            Icon::DarkMode => '\u{e51c}', // dark_mode
            Icon::LightMode => '\u{e518}', // light_mode
            Icon::Key => '\u{e73c}', // key
            Icon::Verified => '\u{ef76}', // verified
            Icon::Shield => '\u{e9e0}', // shield
            Icon::History => '\u{e889}', // history
            Icon::Star => '\u{e838}', // star
            Icon::Trending => '\u{e8e5}', // trending_up
            Icon::Article => '\u{ef42}', // article
            Icon::Warning => '\u{e002}', // warning
            Icon::Error => '\u{e000}', // error
            Icon::Done => '\u{e877}', // done_all
            Icon::Sort => '\u{e164}', // sort
            Icon::Tag => '\u{f05b}', // sell
            Icon::Palette => '\u{e40a}', // palette
            Icon::Storage => '\u{e1db}', // storage
            Icon::Help => '\u{e887}', // help
            Icon::Person => '\u{e853}', // account_circle
            Icon::Login => '\u{ea77}', // login
            Icon::Cloud => '\u{e2bf}', // cloud_done
            Icon::Sync => '\u{e627}', // sync
            Icon::Flag => '\u{e153}', // flag
            Icon::Add => '\u{e147}', // add_circle
            Icon::Stories => '\u{e666}', // auto_stories
            Icon::Quiz => '\u{f04c}', // quiz
            Icon::Calendar => '\u{e878}', // event
            Icon::Bar => '\u{e26b}', // bar_chart
            Icon::Archive => '\u{e1a1}', // inventory_2
            Icon::Compose => '\u{e745}', // edit_note
            Icon::Reply => '\u{e15e}', // reply
            Icon::PersonAdd => '\u{e7fe}', // person_add
            Icon::Badge => '\u{ea67}', // badge
            Icon::Dashboard => '\u{e871}', // dashboard
            Icon::Tune => '\u{e429}', // tune
        }
    }
}

pub fn family() -> FontFamily {
    FontFamily::Name(FAMILY.into())
}

/// Draw `icon` centred in `r`, sized to fit.
pub fn paint(p: &Painter, r: Rect, icon: Icon, color: Color32) {
    let size = r.width().min(r.height());
    p.text(r.center(), Align2::CENTER_CENTER, icon.glyph(), FontId::new(size, family()), color);
}

/// The glyph as text, for use inside `RichText` / `Button` labels.
pub fn text(icon: Icon, size: f32) -> egui::RichText {
    egui::RichText::new(icon.glyph().to_string()).font(FontId::new(size, family()))
}
