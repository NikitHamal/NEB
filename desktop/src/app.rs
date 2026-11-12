//! Application state + routing: the eframe `App`, global keyboard shortcuts,
//! the shell (menu bar + sidebar/rail/bottom bar), window-size persistence and
//! the `Action` dispatcher.
use std::sync::Arc;

use eframe::egui::{self, Context, Frame, Key, Modifiers, ViewportCommand};

use crate::actions::Action;
use crate::config::{Cli, DEFAULT_WINDOW, MIN_WINDOW};
use crate::data::store::{PersistedState, Store, ThemeMode, WindowGeom};
use crate::devtools::Tour;
use crate::env::Env;
use crate::router::{Route, Router};
use crate::screens::{self, Screens};
use crate::theme::fonts;
use crate::ui::{self, LayoutMode};

pub struct NebApp {
    pub(crate) env: Env,
    pub(crate) router: Router,
    pub(crate) screens: Screens,
    show_shortcuts: bool,
    pub(crate) legal_sheet: Option<String>,
    last_geom: Option<(f32, f32)>,
    pub(crate) tour: Option<Tour>,
}

pub fn run(cli: Cli) -> eframe::Result<()> {
    let config_dir = cli.config_dir.clone().unwrap_or_else(Store::default_dir);
    let store = Store::load(&config_dir, cli.reset);
    let geom = store.s.window.filter(|_| store.s.prefs.remember_window && cli.screenshots.is_none());
    let size = cli.size.map(|s| [s[0].max(MIN_WINDOW[0]), s[1].max(MIN_WINDOW[1])]).or(geom.map(|g| [g.w.max(MIN_WINDOW[0]), g.h.max(MIN_WINDOW[1])])).unwrap_or(DEFAULT_WINDOW);

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
            let env = Env::new(cc.egui_ctx.clone(), store, system_dark, config_dir);
            Ok(Box::new(NebApp::new(env, &cli2)))
        }),
    )
}

impl NebApp {
    fn new(env: Env, cli: &Cli) -> Self {
        let tour = cli.screenshots.clone().map(Tour::new);
        let mut env = env;
        env.demo = tour.is_some();
        Self {
            env,
            router: Router::new(match &cli.open_pdf {
                Some(p) => Route::Pdf(p.clone()),
                None => Route::Splash,
            }),
            screens: Screens::default(),
            show_shortcuts: false,
            legal_sheet: None,
            last_geom: None,
            tour,
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
            for (k, r) in [(Key::Num1, Route::Home), (Key::Num2, Route::Library), (Key::Num3, Route::Community), (Key::Num4, Route::Notifications), (Key::Num5, Route::Bookmarks), (Key::Num6, Route::Books), (Key::Num7, Route::People), (Key::Num8, Route::Downloads)] {
                if i.consume_key(cmd, k) {
                    acts.push(Action::Go(r));
                }
            }
            if i.consume_key(cmd, Key::D) {
                acts.push(Action::Go(Route::Downloads));
            }
            if i.consume_key(cmd, Key::H) {
                acts.push(Action::Go(Route::History));
            }
            if i.consume_key(Modifiers::COMMAND | Modifiers::SHIFT, Key::D) {
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
            if ui::dialog::is_open(ctx) {
                // the dialog closes itself on Esc
            } else if self.show_shortcuts {
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
            Action::Fullscreen => {
                let fs = ctx.input(|i| i.viewport().fullscreen.unwrap_or(false));
                ctx.send_viewport_cmd(ViewportCommand::Fullscreen(!fs));
            }
            Action::ShowShortcuts => self.show_shortcuts = !self.show_shortcuts,
            Action::ShowLegal(k) => self.legal_sheet = Some(k),
            Action::Copy(text) => {
                ctx.copy_text(text);
                self.env.toast("Copied to the clipboard");
            }
            Action::OpenPath(p) if p.extension().is_some_and(|e| e.eq_ignore_ascii_case("pdf")) => self.router.navigate(Route::Pdf(p)),
            Action::OpenPath(p) => {
                if open::that(&p).is_err() {
                    self.env.toast("Could not open it — no default application found");
                }
            }
            Action::SignOut => {
                self.env.sign_out();
                self.screens = Screens::default();
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
                self.env.reload_content();
                self.env.toast("Refreshing the library…");
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
        self.screens.reader.is_loading() || matches!(self.env.status, crate::env::ContentStatus::Loading)
    }

    // ---------------------------------------------------------------- screens
    fn shell(&mut self, ctx: &Context) {
        // Only people with an account get in: every in-app screen needs a session.
        if self.router.current.has_shell() && !self.env.signed_in() {
            self.router.replace(Route::Login);
        }
        let route = self.router.current.clone();
        let th = self.env.theme.clone();
        if route.has_shell() {
            if crate::data::content::is_offline() {
                let mut retry = false;
                egui::TopBottomPanel::top("offline_banner")
                    .exact_height(40.0)
                    .frame(Frame::none().fill(th.p.secondary_container).inner_margin(egui::Margin::symmetric(16.0, 0.0)))
                    .show(ctx, |ui| {
                        ui.horizontal_centered(|ui| {
                            ui.label(egui::RichText::new("You're offline — showing what's saved on this computer.").font(fonts::medium(13.5)).color(th.p.on_secondary_container));
                            ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                                if ui::widgets::button(ui, &th, "Retry", ui::widgets::BtnKind::Ghost, Some(ui::icons::Icon::Refresh), None).clicked() {
                                    retry = true;
                                }
                            });
                        });
                    });
                if retry {
                    self.env.act(Action::ReloadContent);
                }
            }
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
                Route::Intro => screens::intro::show(ui, env, &mut sc.intro),
                Route::Pdf(p) => screens::pdf::show(ui, env, &mut sc.pdf, p),
                Route::Login => screens::login::show(ui, env, &mut sc.login),
                Route::EmailAuth => screens::email_auth::show(ui, env, &mut sc.email),
                Route::CompleteProfile => screens::complete_profile::show(ui, env, &mut sc.complete),
                Route::Community => screens::community::show(ui, env, &mut sc.community),
                Route::Post(id) => screens::community::show_post(ui, env, &mut sc.community, id),
                Route::Notifications => screens::notifications::show(ui, env, &mut sc.notifications),
                Route::Onboarding => screens::onboarding::show(ui, env, &mut sc.onboarding),
                Route::Home => screens::home::show(ui, env),
                Route::Library => screens::library::show_library(ui, env, &mut sc.library),
                Route::Category(g) => screens::library::show_category(ui, env, g),
                Route::Subject { track, subject } => screens::subject::show(ui, env, &mut sc.subject, track, subject),
                Route::Reader(c) => screens::reader::show(ui, env, &mut sc.reader, c),
                Route::Search => screens::search::show(ui, env, &mut sc.search),
                Route::Bookmarks => screens::bookmarks::show(ui, env),
                Route::Downloads => screens::downloads::show(ui, env, &mut sc.downloads),
                Route::Books => screens::books::show(ui, env, &mut sc.books),
                Route::People => screens::people::show(ui, env, &mut sc.people),
                Route::User(name) => screens::user::show(ui, env, &mut sc.user, name),
                Route::Settings => screens::settings::show(ui, env, &mut sc.settings),
                Route::Profile => screens::profile::show(ui, env),
                Route::Account(tab) => screens::account::show(ui, env, &mut sc.account, *tab),
                Route::About => screens::about::show(ui, env),
                Route::History => screens::history::show(ui, env),
                Route::Help => screens::help::show(ui, env),
                Route::Legal(k) => screens::legal::show(ui, env, k),
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
        crate::theme::motion::set_reduced(!self.env.motion());
        self.env.poll();
        self.handle_keys(ctx);
        self.shell(ctx);
        let bottom = if self.env.layout == LayoutMode::Compact && self.router.current.has_shell() { ui::nav::BOTTOM_BAR_H } else { 0.0 };
        let th = self.env.theme.clone();
        self.env.toasts.show(ctx, &th, bottom);
        ui::shortcuts::show(ctx, &th, &mut self.show_shortcuts);
        if let Some(mut key) = self.legal_sheet.take() {
            if !screens::legal::sheet(ctx, &self.env, &mut key) {
                self.legal_sheet = Some(key);
            }
        }
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

