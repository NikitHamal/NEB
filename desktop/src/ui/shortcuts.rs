//! Keyboard-shortcut reference dialog (Help ▸ Keyboard shortcuts, or F1 / Ctrl+/).
use egui::{Align2, Context, RichText};

use crate::theme::{fonts, Theme};

pub const SHORTCUTS: &[(&str, &str)] = &[
    ("Ctrl + K", "Search everything"),
    ("Ctrl + 1 … 8", "Home · Library · Community · Notifications · Bookmarks · Books · People · Offline"),
    ("Ctrl + ,", "Settings"),
    ("Esc", "Close dialog / go back"),
    ("Alt + ←  /  Alt + →", "Back / forward"),
    ("Ctrl + B", "Bookmark the open chapter"),
    ("Ctrl + D", "Offline downloads"),
    ("Ctrl + H", "Reading history"),
    ("Ctrl + Shift + D", "Toggle dark mode"),
    ("Tab  /  Shift + Tab", "Move focus between buttons, cards and fields"),
    ("Enter  /  Space", "Activate the focused item"),
    ("Ctrl + +  /  Ctrl + −  /  Ctrl + 0", "Zoom the interface in / out / reset"),
    ("[   and   ]", "Previous / next chapter (reader)"),
    ("Space · PageDown · PageUp", "Scroll the reader by a page"),
    ("Home · End", "Jump to start / end of the chapter"),
    ("T", "Show / hide the table of contents (reader)"),
    ("F11", "Full screen"),
    ("F1  or  Ctrl + /", "This list"),
    ("Ctrl + Q", "Quit"),
];

pub fn show(ctx: &Context, th: &Theme, open: &mut bool) {
    if !*open {
        return;
    }
    let mut keep = true;
    egui::Window::new(RichText::new("Keyboard shortcuts").font(fonts::bold(17.0)))
        .open(&mut keep)
        .collapsible(false)
        .resizable(false)
        .anchor(Align2::CENTER_CENTER, egui::vec2(0.0, 0.0))
        .show(ctx, |ui| {
            egui::Grid::new("shortcuts").num_columns(2).spacing([28.0, 10.0]).show(ui, |ui| {
                for (k, d) in SHORTCUTS {
                    ui.label(RichText::new(*k).font(fonts::medium(13.5)).color(th.p.accent));
                    ui.label(RichText::new(*d).color(th.p.ink_muted));
                    ui.end_row();
                }
            });
        });
    *open = keep;
}
