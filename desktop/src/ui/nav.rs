//! App navigation: labelled sidebar (wide), icon rail (medium), bottom bar (narrow).
use egui::{vec2, Align, Color32, Context, CursorIcon, Frame, Layout, Margin, Rect, Rounding, Sense, Stroke, Ui};

use super::avatar::avatar;
use super::icons::{self, Icon};
use super::LayoutMode;
use crate::env::Env;
use crate::router::Route;
use crate::theme::{fonts, Theme};

pub struct NavEntry {
    pub label: &'static str,
    pub icon: Icon,
    pub route: Route,
    pub hint: &'static str,
}

pub fn entries() -> Vec<NavEntry> {
    vec![
        NavEntry { label: "Home", icon: Icon::Home, route: Route::Home, hint: "Ctrl+1" },
        NavEntry { label: "Library", icon: Icon::Library, route: Route::Library, hint: "Ctrl+2" },
        NavEntry { label: "Search", icon: Icon::Search, route: Route::Search, hint: "Ctrl+K" },
        NavEntry { label: "Bookmarks", icon: Icon::Bookmark, route: Route::Bookmarks, hint: "Ctrl+4" },
        NavEntry { label: "Downloads", icon: Icon::Download, route: Route::Downloads, hint: "Ctrl+5" },
    ]
}

fn nav_item(ui: &mut Ui, th: &Theme, e: &NavEntry, selected: bool, with_label: bool, width: f32) -> bool {
    let (rect, resp) = ui.allocate_exact_size(vec2(width, 44.0), Sense::click());
    let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
    let fill = if selected { th.p.accent_soft } else { th.p.field.gamma_multiply(hover) };
    ui.painter().rect_filled(rect, Rounding::same(12.0), fill);
    if resp.has_focus() {
        ui.painter().rect_stroke(rect.expand(1.5), Rounding::same(13.0), Stroke::new(2.0, th.p.accent));
    }
    let col = if selected { th.p.accent } else if hover > 0.0 { th.p.ink } else { th.p.ink_muted };
    let icon_c = if with_label { egui::pos2(rect.min.x + 26.0, rect.center().y) } else { rect.center() };
    icons::paint(ui.painter(), Rect::from_center_size(icon_c, vec2(21.0, 21.0)), e.icon, col);
    if with_label {
        let font = if selected { fonts::bold(14.5) } else { fonts::medium(14.5) };
        ui.painter().text(egui::pos2(rect.min.x + 48.0, rect.center().y), egui::Align2::LEFT_CENTER, e.label, font, col);
    }
    if resp.hovered() {
        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
    }
    let resp = if with_label { resp } else { resp.on_hover_text(format!("{}  ({})", e.label, e.hint)) };
    resp.clicked()
}

pub fn sidebar(ctx: &Context, env: &mut Env, current: &Route) {
    let wide = env.layout == LayoutMode::Wide;
    let th = env.theme.clone();
    let width = if wide { 236.0 } else { 76.0 };
    egui::SidePanel::left("nav")
        .exact_width(width)
        .resizable(false)
        .frame(Frame::none().fill(th.p.page).stroke(Stroke::new(1.0, th.p.hairline)).inner_margin(Margin::symmetric(12.0, 16.0)))
        .show(ctx, |ui| {
            let inner_w = width - 24.0;
            // brand
            ui.horizontal(|ui| {
                ui.add_space(if wide { 6.0 } else { (inner_w - 34.0) / 2.0 });
                env.logo.show(ui, 34.0);
                if wide {
                    super::widgets::label(ui, egui::RichText::new("NEBians").font(fonts::bold(20.0)).color(th.p.ink));
                }
            });
            ui.add_space(22.0);
            let root = current.nav_root();
            for e in entries() {
                if nav_item(ui, &th, &e, root == e.route, wide, inner_w) {
                    env.act(crate::actions::Action::Go(e.route.clone()));
                }
                ui.add_space(4.0);
            }
            ui.with_layout(Layout::bottom_up(Align::Min), |ui| {
                // profile chip
                let name = env.store.s.profile.display_name.clone();
                let sub = match &env.store.s.session {
                    Some(s) if !s.username.is_empty() => format!("@{}", s.username),
                    _ if env.store.s.guest => "Guest".to_string(),
                    _ => format!("@{}", env.store.s.profile.handle),
                };
                let h = 54.0;
                let (rect, resp) = ui.allocate_exact_size(vec2(inner_w, h), Sense::click());
                let hover = ui.ctx().animate_bool_with_time(resp.id.with("h"), resp.hovered(), 0.1);
                let selected = matches!(current, Route::Profile);
                ui.painter().rect_filled(rect, Rounding::same(12.0), if selected { th.p.accent_soft } else { th.p.field.gamma_multiply(hover) });
                let mut child = ui.new_child(egui::UiBuilder::new().max_rect(rect.shrink2(vec2(8.0, 7.0))).layout(Layout::left_to_right(Align::Center)));
                avatar(&mut child, &th, if name.is_empty() { "Guest" } else { &name }, env.store.s.profile.avatar_tone, 38.0);
                if wide {
                    child.vertical(|ui| {
                        ui.spacing_mut().item_spacing.y = 0.0;
                        super::widgets::label_trunc(ui, egui::RichText::new(if name.is_empty() { "Guest" } else { &name }).font(fonts::medium(13.5)).color(th.p.ink));
                        super::widgets::label_trunc(ui, egui::RichText::new(sub).font(fonts::regular(12.0)).color(th.p.ink_muted));
                    });
                }
                if resp.hovered() {
                    ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
                }
                if resp.on_hover_text("Profile").clicked() {
                    env.go(Route::Profile);
                }
                ui.add_space(4.0);
                let settings = NavEntry { label: "Settings", icon: Icon::Settings, route: Route::Settings, hint: "Ctrl+," };
                if nav_item(ui, &th, &settings, root == Route::Settings, wide, inner_w) {
                    env.go(Route::Settings);
                }
            });
        });
}

pub fn bottom_bar(ctx: &Context, env: &mut Env, current: &Route) {
    let th = env.theme.clone();
    egui::TopBottomPanel::bottom("bottom_nav")
        .exact_height(62.0)
        .frame(Frame::none().fill(th.p.page).stroke(Stroke::new(1.0, th.p.hairline)).inner_margin(Margin::symmetric(8.0, 6.0)))
        .show(ctx, |ui| {
            let mut items = entries();
            items.push(NavEntry { label: "Settings", icon: Icon::Settings, route: Route::Settings, hint: "Ctrl+," });
            let w = ui.available_width() / items.len() as f32;
            let root = current.nav_root();
            ui.horizontal(|ui| {
                ui.spacing_mut().item_spacing.x = 0.0;
                for e in &items {
                    let selected = root == e.route;
                    let (rect, resp) = ui.allocate_exact_size(vec2(w, 48.0), Sense::click());
                    let col = if selected { th.p.accent } else { th.p.ink_muted };
                    if selected {
                        let pill = Rect::from_center_size(egui::pos2(rect.center().x, rect.min.y + 14.0), vec2(48.0, 26.0));
                        ui.painter().rect_filled(pill, Rounding::same(13.0), th.p.accent_soft);
                    }
                    icons::paint(ui.painter(), Rect::from_center_size(egui::pos2(rect.center().x, rect.min.y + 14.0), vec2(20.0, 20.0)), e.icon, col);
                    ui.painter().text(egui::pos2(rect.center().x, rect.max.y - 8.0), egui::Align2::CENTER_CENTER, e.label, fonts::medium(11.0), col);
                    if resp.hovered() {
                        ui.ctx().set_cursor_icon(CursorIcon::PointingHand);
                    }
                    if resp.clicked() {
                        env.go(e.route.clone());
                    }
                }
            });
        });
    let _ = Color32::TRANSPARENT;
}
