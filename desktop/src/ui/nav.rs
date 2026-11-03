//! App navigation, Material 3 style: an expanded rail with labels (wide), a compact rail with
//! pill indicators (medium) and a bottom navigation bar (narrow) — all share the same pill
//! "active indicator" that grows in with a short spring-like ease.
use egui::{vec2, Align, Align2, Color32, Context, CursorIcon, Frame, Layout, Margin, Rect, Rounding, Sense, Stroke, Ui};

use super::icons::{self, Icon};
use super::LayoutMode;
use crate::env::Env;
use crate::router::Route;
use crate::theme::{fonts, Theme};

pub const BOTTOM_BAR_H: f32 = 76.0;

pub struct NavEntry {
    pub label: &'static str,
    pub icon: Icon,
    pub route: Route,
    pub hint: &'static str,
}

fn entry(label: &'static str, icon: Icon, route: Route, hint: &'static str) -> NavEntry {
    NavEntry { label, icon, route, hint }
}

pub fn main_entries() -> Vec<NavEntry> {
    vec![
        entry("Home", Icon::Home, Route::Home, "Ctrl+1"),
        entry("Library", Icon::Library, Route::Library, "Ctrl+2"),
        entry("Community", Icon::Forum, Route::Community, "Ctrl+3"),
        entry("Notifications", Icon::Bell, Route::Notifications, "Ctrl+4"),
    ]
}

pub fn study_entries() -> Vec<NavEntry> {
    vec![
        entry("Search", Icon::Search, Route::Search, "Ctrl+K"),
        entry("Bookmarks", Icon::Bookmark, Route::Bookmarks, "Ctrl+5"),
        entry("Books", Icon::Article, Route::Books, "Ctrl+6"),
        entry("People", Icon::User, Route::People, "Ctrl+7"),
        entry("Offline", Icon::Download, Route::Downloads, "Ctrl+8"),
    ]
}

fn badge_dot(ui: &Ui, th: &Theme, center: egui::Pos2, count: u32) {
    if count == 0 {
        return;
    }
    let text = if count > 99 { "99+".to_string() } else { count.to_string() };
    let w = if text.len() > 1 { 22.0 } else { 16.0 };
    let r = Rect::from_center_size(center, vec2(w, 16.0));
    ui.painter().rect_filled(r, Rounding::same(8.0), th.p.danger);
    let fg = if th.dark { Color32::from_rgb(0x69, 0x00, 0x05) } else { Color32::WHITE };
    ui.painter().text(r.center(), Align2::CENTER_CENTER, text, fonts::bold(10.0), fg);
}

fn ease(t: f32) -> f32 {
    // slight overshoot, like the Android spatial spring
    let t = t.clamp(0.0, 1.0);
    let c1 = 1.2;
    let c3 = c1 + 1.0;
    1.0 + c3 * (t - 1.0).powi(3) + c1 * (t - 1.0).powi(2)
}

/// Expanded-rail row: 52dp pill, icon + label.
fn wide_item(ui: &mut Ui, th: &Theme, e: &NavEntry, selected: bool, width: f32, badge: u32) -> bool {
    let (rect, resp) = ui.allocate_exact_size(vec2(width, 52.0), Sense::click());
    let sel = ui.ctx().animate_bool_with_time(resp.id.with("sel"), selected, 0.2);
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
    let p = &th.p;
    let ind = Rect::from_min_size(rect.min, vec2(width * (0.55 + 0.45 * ease(sel)), 52.0));
    if sel > 0.01 {
        ui.painter().rect_filled(ind, Rounding::same(26.0), p.secondary_container.gamma_multiply(sel.min(1.0)));
    }
    ui.painter().rect_filled(rect, Rounding::same(26.0), p.ink.gamma_multiply(0.07 * hover * (1.0 - sel)));
    if resp.has_focus() {
        ui.painter().rect_stroke(rect.expand(2.0), Rounding::same(28.0), Stroke::new(2.0_f32, p.accent));
    }
    let col = if selected { p.on_secondary_container } else { p.ink_muted };
    let col = crate::theme::mix(col, p.ink, hover * 0.6);
    let ic = egui::pos2(rect.min.x + 30.0, rect.center().y);
    icons::paint(ui.painter(), Rect::from_center_size(ic, vec2(24.0, 24.0)), e.icon, col);
    badge_dot(ui, th, ic + vec2(10.0, -9.0), badge);
    let font = if selected { fonts::bold(15.0) } else { fonts::medium(15.0) };
    ui.painter().text(egui::pos2(rect.min.x + 58.0, rect.center().y), Align2::LEFT_CENTER, e.label, font, col);
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    resp.clicked()
}

/// Compact-rail / bottom-bar item: 64x32 pill indicator, icon, small label beneath.
fn stacked_item(ui: &mut Ui, th: &Theme, label: &str, icon: Icon, selected: bool, size: egui::Vec2, badge: u32, tip: Option<String>) -> bool {
    let (rect, resp) = ui.allocate_exact_size(size, Sense::click());
    let sel = ui.ctx().animate_bool_with_time(resp.id.with("sel"), selected, 0.2);
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
    let p = &th.p;
    let top = rect.min.y + 8.0;
    let ind_full = vec2(60.0, 32.0);
    let ind_c = egui::pos2(rect.center().x, top + 16.0);
    let ind = Rect::from_center_size(ind_c, vec2(ind_full.x * (0.35 + 0.65 * ease(sel)), 32.0));
    if sel > 0.01 {
        ui.painter().rect_filled(ind, Rounding::same(16.0), p.secondary_container.gamma_multiply(sel.min(1.0)));
    }
    ui.painter().rect_filled(Rect::from_center_size(ind_c, ind_full), Rounding::same(16.0), p.ink.gamma_multiply(0.07 * hover * (1.0 - sel)));
    if resp.has_focus() {
        ui.painter().rect_stroke(Rect::from_center_size(ind_c, ind_full).expand(2.0), Rounding::same(18.0), Stroke::new(2.0_f32, p.accent));
    }
    let col = if selected { p.on_secondary_container } else { p.ink_muted };
    icons::paint(ui.painter(), Rect::from_center_size(ind_c, vec2(24.0, 24.0)), icon, col);
    badge_dot(ui, th, ind_c + vec2(13.0, -9.0), badge);
    let font = if selected { fonts::bold(11.5) } else { fonts::medium(11.5) };
    ui.painter().text(egui::pos2(rect.center().x, top + 46.0), Align2::CENTER_CENTER, label, font, col);
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    let resp = match tip {
        Some(t) => resp.on_hover_text(t),
        None => resp,
    };
    resp.clicked()
}

pub fn sidebar(ctx: &Context, env: &mut Env, current: &Route) {
    let wide = env.layout == LayoutMode::Wide;
    let th = env.theme.clone();
    let width = if wide { 268.0 } else { 88.0 };
    let unread = env.srv.unread;
    egui::SidePanel::left("nav")
        .exact_width(width)
        .resizable(false)
        .frame(Frame::none().fill(th.p.page).stroke(Stroke::new(1.0_f32, th.p.hairline)).inner_margin(Margin::symmetric(if wide { 14.0 } else { 6.0 }, 16.0)))
        .show(ctx, |ui| {
            let inner_w = width - if wide { 28.0 } else { 12.0 };
            ui.horizontal(|ui| {
                ui.add_space(if wide { 8.0 } else { (inner_w - 36.0) / 2.0 });
                env.logo.show(ui, 36.0);
                if wide {
                    ui.add_space(4.0);
                    super::widgets::label(ui, egui::RichText::new("NEBians").font(fonts::bold(21.0)).color(th.p.ink));
                    ui.with_layout(Layout::right_to_left(Align::Center), |ui| {
                        if super::theme_toggle::show(ui, &th).clicked() {
                            env.act(crate::actions::Action::ToggleDark);
                        }
                    });
                }
            });
            ui.add_space(if wide { 20.0 } else { 14.0 });
            let root = current.nav_root();
            ui.spacing_mut().item_spacing.y = if wide { 4.0 } else { 2.0 };
            for e in main_entries() {
                let badge = if e.route == Route::Notifications { unread } else { 0 };
                let hit = if wide {
                    wide_item(ui, &th, &e, root == e.route, inner_w, badge)
                } else {
                    stacked_item(ui, &th, short(e.label), e.icon, root == e.route, vec2(inner_w, 66.0), badge, Some(format!("{}  ({})", e.label, e.hint)))
                };
                if hit {
                    env.act(crate::actions::Action::Go(e.route.clone()));
                }
            }
            ui.add_space(if wide { 16.0 } else { 8.0 });
            for e in study_entries() {
                let hit = if wide {
                    wide_item(ui, &th, &e, root == e.route, inner_w, 0)
                } else {
                    stacked_item(ui, &th, short(e.label), e.icon, root == e.route, vec2(inner_w, 66.0), 0, Some(format!("{}  ({})", e.label, e.hint)))
                };
                if hit {
                    env.act(crate::actions::Action::Go(e.route.clone()));
                }
            }
            ui.with_layout(Layout::bottom_up(Align::Min), |ui| {
                let settings = entry("Settings", Icon::Settings, Route::Settings, "Ctrl+,");
                let hit = if wide {
                    wide_item(ui, &th, &settings, root == Route::Settings, inner_w, 0)
                } else {
                    stacked_item(ui, &th, "Settings", Icon::Settings, root == Route::Settings, vec2(inner_w, 66.0), 0, Some("Settings  (Ctrl+,)".into()))
                };
                if hit {
                    env.go(Route::Settings);
                }
                ui.add_space(4.0);
                account_chip(ui, env, &th, current, inner_w, wide);
                if !wide {
                    ui.add_space(4.0);
                    ui.allocate_ui_with_layout(vec2(inner_w, 44.0), Layout::top_down(Align::Center), |ui| {
                        if super::theme_toggle::show(ui, &th).clicked() {
                            env.act(crate::actions::Action::ToggleDark);
                        }
                    });
                }
            });
        });
}

fn short(label: &str) -> &str {
    if label == "Notifications" { "Alerts" } else { label }
}

fn account_chip(ui: &mut Ui, env: &mut Env, th: &Theme, current: &Route, inner_w: f32, wide: bool) {
    let signed = env.signed_in();
    if !signed {
        if wide {
            if super::widgets::button_sized(ui, th, "Sign in or join", super::widgets::BtnKind::Primary, Some(Icon::Login), Some(inner_w), 48.0).clicked() {
                env.act(crate::actions::Action::Replace(Route::Login));
            }
        } else if stacked_item(ui, th, "Sign in", Icon::Login, false, vec2(inner_w, 66.0), 0, Some("Sign in or create an account".into())) {
            env.act(crate::actions::Action::Replace(Route::Login));
        }
        return;
    }
    let name = env.store.s.profile.display_name.clone();
    let name = if name.is_empty() { env.my_username() } else { name };
    let sub = format!("@{}", env.my_username());
    let h = if wide { 60.0 } else { 56.0 };
    let (rect, resp) = ui.allocate_exact_size(vec2(inner_w, h), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
    let selected = matches!(current, Route::Profile);
    let fill = if selected { th.p.secondary_container } else { th.p.card };
    ui.painter().rect(rect, Rounding::same(22.0), fill, Stroke::new(1.0_f32, th.p.hairline));
    ui.painter().rect_filled(rect, Rounding::same(22.0), th.p.ink.gamma_multiply(0.06 * hover));
    let mut child = ui.new_child(egui::UiBuilder::new().max_rect(rect.shrink2(vec2(if wide { 10.0 } else { 0.0 }, 8.0))).layout(if wide { Layout::left_to_right(Align::Center) } else { Layout::top_down(Align::Center) }));
    let photo = env.store.s.session.as_ref().map(|s| s.photo_url.clone()).unwrap_or_default();
    super::remote_image::avatar(&mut child, th, &name, env.store.s.profile.avatar_tone, 40.0, &photo);
    if wide {
        child.vertical(|ui| {
            ui.spacing_mut().item_spacing.y = 0.0;
            super::widgets::label_trunc(ui, egui::RichText::new(&name).font(fonts::medium(14.0)).color(th.p.ink));
            super::widgets::label_trunc(ui, egui::RichText::new(sub).font(fonts::regular(12.0)).color(th.p.ink_muted));
        });
    }
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    if resp.on_hover_text("Your profile").clicked() {
        env.go(Route::Profile);
    }
}

pub fn bottom_bar(ctx: &Context, env: &mut Env, current: &Route) {
    let th = env.theme.clone();
    let unread = env.srv.unread;
    egui::TopBottomPanel::bottom("bottom_nav")
        .exact_height(BOTTOM_BAR_H)
        .frame(Frame::none().fill(th.p.card).stroke(Stroke::new(1.0_f32, th.p.hairline)).inner_margin(Margin::symmetric(4.0, 0.0)))
        .show(ctx, |ui| {
            let mut items = main_entries();
            items.push(entry("You", Icon::Person, Route::Profile, ""));
            let w = ui.available_width() / items.len() as f32;
            let root = current.nav_root();
            ui.horizontal(|ui| {
                ui.spacing_mut().item_spacing.x = 0.0;
                for e in &items {
                    let badge = if e.route == Route::Notifications { unread } else { 0 };
                    if stacked_item(ui, &th, short(e.label), e.icon, root == e.route, vec2(w, BOTTOM_BAR_H - 2.0), badge, None) {
                        let r = if e.route == Route::Profile && !env.signed_in() { Route::Settings } else { e.route.clone() };
                        env.act(crate::actions::Action::Go(r));
                    }
                }
            });
        });
}
