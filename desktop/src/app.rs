//! Application state + routing: the eframe `App`, global keyboard shortcuts,
//! the shell (menu bar + sidebar/rail/bottom bar), window-size persistence and
//! the `Action` dispatcher.
use std::sync::Arc;

use eframe::egui::{self, Context, Frame, Key, Modifiers, ViewportCommand};

use crate::actions::Action;
use crate::config::{Cli, DEFAULT_WINDOW, MIN_WINDOW};
use crate::data::content::ContentRoot;
use crate::data::models::ChapterRef;
use crate::data::store::{PersistedState, Store, ThemeMode, WindowGeom};
use crate::devtools::Tour;
use crate::env::Env;
use crate::router::{Route, Router};
use crate::screens::{self, Screens};
use crate::theme::fonts;
use crate::ui::{self, menu::MenuState, LayoutMode};

pub struct NebApp {
    pub(crate) env: Env,
    pub(crate) router: Router,
    pub(crate) screens: Screens,
    show_shortcuts: bool,
    last_geom: Option<(f32, f32)>,
    pub(crate) tour: Option<Tour>,
    cli_content: Option<std::path::PathBuf>,
}

pub fn run(cli: Cli) -> eframe::Result<()> {
    let config_dir = cli.config_dir.clone().unwrap_or_else(Store::default_dir);
    let store = Store::load(&config_dir, cli.reset);
    let geom = store.s.window.filter(|_| store.s.prefs.remember_window && cli.screenshots.is_none());
    let size = geom.map(|g| [g.w.max(MIN_WINDOW[0]), g.h.max(MIN_WINDOW[1])]).unwrap_or(DEFAULT_WINDOW);

    let mut vp = egui::ViewportBuilder::default()
        .with_title("NEBians")
        .with_app_id("np.com.nebians.desktop")
        .with_inner_size(size)
        .with_min_inner_size(MIN_WINDOW)
        .with_icon(Arc::new(ui::logo::window_icon()));
    if let Some(g) = geom {
        if let (Some(x), Some(y)) = (g.x, g.y) {
            vp = vp.with_position([x.max(0.0), y.max(0.0)]);
        }
    }
    let options = eframe::NativeOptions { viewport: vp, centered: geom.is_none(), ..Default::default() };

    let cli2 = cli.clone();
    let mut store_opt = Some(store);
    eframe::run_native(
        "NEBians",
        options,
        Box::new(move |cc| {
            fonts::install(&cc.egui_ctx);
            egui_extras::install_image_loaders(&cc.egui_ctx);
            let system_dark = cc.egui_ctx.input(|i| i.raw.system_theme) == Some(egui::Theme::Dark);
            let store = store_opt.take().expect("store");
            let saved = store.s.prefs.content_dir.clone().map(std::path::PathBuf::from);
            let content = ContentRoot::detect(cli2.content.as_deref(), saved.as_deref());
            let env = Env::new(cc.egui_ctx.clone(), store, content, system_dark, config_dir);
            Ok(Box::new(NebApp::new(env, &cli2)))
        }),
    )
}

impl NebApp {
    fn new(env: Env, cli: &Cli) -> Self {
        let tour = cli.screenshots.clone().map(Tour::new);
        Self {
            env,
            router: Router::new(Route::Splash),
            screens: Screens::default(),
            show_shortcuts: false,
            last_geom: None,
            tour,
            cli_content: cli.content.clone(),
        }
    }

    // ------------------------------------------------------------------ keys
    fn handle_keys(&mut self, ctx: &Context) {
        let shell = self.router.current.has_shell();
        let cmd = Modifiers::COMMAND;
        let mut acts: Vec<Action> = vec![];
        ctx.input_mut(|i| {
            if i.consume_key(cmd, Key::Q) {
                acts.push(Action::Quit);
            }
            if i.consume_key(Modifiers::NONE, Key::F11) {
                acts.push(Action::Fullscreen);
            }
            if i.consume_key(Modifiers::NONE, Key::F1) || i.consume_key(cmd, Key::Slash) {
                acts.push(Action::ShowShortcuts);
            }
            if !shell {
                return;
            }
            if i.consume_key(cmd, Key::K) {
                acts.push(Action::Go(Route::Search));
            }
            if i.consume_key(cmd, Key::Comma) {
                acts.push(Action::Go(Route::Settings));
            }
            for (k, r) in [(Key::Num1, Route::Home), (Key::Num2, Route::Library), (Key::Num3, Route::Search), (Key::Num4, Route::Bookmarks), (Key::Num5, Route::Downloads)] {
                if i.consume_key(cmd, k) {
                    acts.push(Action::Go(r));
                }
            }
            if i.consume_key(cmd, Key::D) {
                acts.push(Action::ToggleDark);
            }
            if i.consume_key(Modifiers::ALT, Key::ArrowLeft) || i.pointer.button_pressed(egui::PointerButton::Extra1) {
                acts.push(Action::Back);
            }
            if i.consume_key(Modifiers::ALT, Key::ArrowRight) || i.pointer.button_pressed(egui::PointerButton::Extra2) {
                acts.push(Action::Forward);
            }
        });
        if shell && ctx.input_mut(|i| i.consume_key(cmd, Key::B)) {
            if let Route::Reader(c) = self.router.current.clone() {
                self.env.toggle_bookmark(&c);
            }
        }
        // Esc: close dialog → leave text field → go back
        if ctx.input(|i| i.key_pressed(Key::Escape)) {
            if self.show_shortcuts {
                self.show_shortcuts = false;
            } else if ctx.memory(|m| m.focused().is_some()) && ctx.wants_keyboard_input() {
                ctx.memory_mut(|m| m.stop_text_input());
                if let Some(id) = ctx.memory(|m| m.focused()) {
                    ctx.memory_mut(|m| m.surrender_focus(id));
                }
            } else if shell {
                acts.push(Action::Back);
            } else if matches!(self.router.current, Route::EmailAuth) {
                acts.push(Action::Replace(Route::Login));
            }
        }
        self.env.actions.extend(acts);
    }

    // --------------------------------------------------------------- actions
    fn apply_actions(&mut self, ctx: &Context) {
        let mut guard = 0;
        while !self.env.actions.is_empty() && guard < 16 {
            guard += 1;
            let batch: Vec<Action> = std::mem::take(&mut self.env.actions);
            for a in batch {
                self.apply(ctx, a);
            }
        }
    }

    fn apply(&mut self, ctx: &Context, a: Action) {
        match a {
            Action::Go(r) => {
                if r == Route::Search {
                    self.screens.search.focus = true;
                }
                self.router.navigate(r);
            }
            Action::Replace(r) => self.router.replace(r),
            Action::Back => {
                self.router.back();
            }
            Action::Forward => {
                self.router.forward();
            }
            Action::ToggleDark => {
                let dark = self.env.theme.dark;
                self.env.store.s.prefs.theme = if dark { ThemeMode::Light } else { ThemeMode::Dark };
                self.env.store.touch();
                self.env.refresh_theme();
            }
            Action::ZoomIn => ctx.set_zoom_factor((ctx.zoom_factor() + 0.1).min(2.0)),
            Action::ZoomOut => ctx.set_zoom_factor((ctx.zoom_factor() - 0.1).max(0.6)),
            Action::ZoomReset => ctx.set_zoom_factor(1.0),
            Action::Fullscreen => {
                let fs = ctx.input(|i| i.viewport().fullscreen.unwrap_or(false));
                ctx.send_viewport_cmd(ViewportCommand::Fullscreen(!fs));
            }
            Action::ShowShortcuts => self.show_shortcuts = !self.show_shortcuts,
            Action::OpenUrl(u) => {
                if open::that(&u).is_err() {
                    self.env.toast("Could not open your browser");
                }
            }
            Action::OpenPath(p) => {
                if open::that(&p).is_err() {
                    self.env.toast("Could not open it — no default application found");
                }
            }
            Action::Toast(m) => self.env.toast(m),
            Action::SignOut => {
                self.env.store.s.session = None;
                self.env.store.s.guest = false;
                self.env.store.s.onboarded = false;
                self.env.store.s.profile = Default::default();
                self.env.store.touch();
                self.screens.onboarding = Default::default();
                self.router.replace(Route::Login);
            }
            Action::ResetAll => {
                let window = self.env.store.s.window;
                self.env.store.s = PersistedState { window, ..Default::default() };
                self.env.store.touch();
                self.env.store.save();
                self.env.refresh_theme();
                self.screens = Screens::default();
                self.router.replace(Route::Login);
            }
            Action::ReloadContent => {
                let saved = self.env.store.s.prefs.content_dir.clone().map(std::path::PathBuf::from);
                let root = ContentRoot::detect(self.cli_content.as_deref(), saved.as_deref());
                self.env.set_content(root);
                self.env.toast("Content reloaded");
            }
            Action::Quit => ctx.send_viewport_cmd(ViewportCommand::Close),
        }
    }

    // ---------------------------------------------------------------- window
    fn track_window(&mut self, ctx: &Context) {
        if !self.env.store.s.prefs.remember_window || self.tour.is_some() {
            return;
        }
        let (inner, outer, fs) = ctx.input(|i| {
            let v = i.viewport();
            (v.inner_rect, v.outer_rect, v.fullscreen.unwrap_or(false) || v.maximized.unwrap_or(false))
        });
        if fs {
            return;
        }
        if let Some(r) = inner {
            let cur = (r.width().round(), r.height().round());
            if self.last_geom != Some(cur) {
                self.last_geom = Some(cur);
                self.env.store.s.window = Some(WindowGeom { w: cur.0, h: cur.1, x: outer.map(|o| o.min.x), y: outer.map(|o| o.min.y) });
                self.env.store.touch();
            }
        }
    }

    pub(crate) fn is_busy(&self) -> bool {
        self.screens.reader.is_loading() || self.env.search_index.is_none() && self.env.content.is_some()
    }

    // ---------------------------------------------------------------- screens
    fn shell(&mut self, ctx: &Context) {
        let route = self.router.current.clone();
        let th = self.env.theme.clone();
        if route.has_shell() {
            let st = MenuState { can_back: self.router.can_back(), can_forward: self.router.can_forward() };
            egui::TopBottomPanel::top("menu_bar").frame(Frame::none().fill(th.p.page).inner_margin(egui::Margin::symmetric(8.0, 2.0)).stroke(egui::Stroke::new(1.0, th.p.hairline))).show(ctx, |ui| {
                ui::menu::menu_bar(ui, &mut self.env, &st);
            });
            match self.env.layout {
                LayoutMode::Compact => ui::nav::bottom_bar(ctx, &mut self.env, &route),
                _ => ui::nav::sidebar(ctx, &mut self.env, &route),
            }
        }
        egui::CentralPanel::default().frame(Frame::none().fill(th.p.page)).show(ctx, |ui| {
            let env = &mut self.env;
            let sc = &mut self.screens;
            match &route {
                Route::Splash => screens::splash::show(ui, env, &mut sc.splash),
                Route::Login => screens::login::show(ui, env),
                Route::EmailAuth => screens::email_auth::show(ui, env, &mut sc.email),
                Route::Onboarding => screens::onboarding::show(ui, env, &mut sc.onboarding),
                Route::Home => screens::home::show(ui, env),
                Route::Library => screens::library::show_library(ui, env, &mut sc.library),
                Route::Category(g) => screens::library::show_category(ui, env, g),
                Route::Subject { track, subject } => screens::subject::show(ui, env, &mut sc.subject, track, subject),
                Route::Reader(c) => screens::reader::show(ui, env, &mut sc.reader, c),
                Route::Search => screens::search::show(ui, env, &mut sc.search),
                Route::Bookmarks => screens::bookmarks::show(ui, env),
                Route::Downloads => screens::downloads::show(ui, env, &mut sc.downloads),
                Route::Settings => screens::settings::show(ui, env, &mut sc.settings),
                Route::Profile => screens::profile::show(ui, env, &mut sc.profile),
                Route::About => screens::about::show(ui, env),
            }
        });
    }
}

impl eframe::App for NebApp {
    fn update(&mut self, ctx: &Context, _frame: &mut eframe::Frame) {
        self.env.layout = LayoutMode::from_width(ctx.screen_rect().width());
        if let Some(t) = ctx.input(|i| i.raw.system_theme) {
            let dark = t == egui::Theme::Dark;
            if dark != self.env.system_dark {
                self.env.system_dark = dark;
                self.env.refresh_theme();
            }
        }
        self.env.poll();
        self.handle_keys(ctx);
        self.shell(ctx);
        let bottom = if self.env.layout == LayoutMode::Compact && self.router.current.has_shell() { 62.0 } else { 0.0 };
        let th = self.env.theme.clone();
        self.env.toasts.show(ctx, &th, bottom);
        ui::shortcuts::show(ctx, &th, &mut self.show_shortcuts);
        self.apply_actions(ctx);
        self.track_window(ctx);
        self.env.store.flush_if_due();
        if let Some(mut tour) = self.tour.take() {
            tour.tick(self, ctx);
            self.tour = Some(tour);
        }
    }

    fn on_exit(&mut self, _gl: Option<&eframe::glow::Context>) {
        self.env.store.save();
    }
}

#[allow(dead_code)]
pub fn chapter_route(c: ChapterRef) -> Route {
    Route::Reader(c)
}
