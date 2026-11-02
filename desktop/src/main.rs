//! NEBians Desktop — thin entrypoint. Everything real lives in the modules below.
#![cfg_attr(all(not(debug_assertions), target_os = "windows"), windows_subsystem = "windows")]

mod actions;
mod app;
mod config;
mod data;
mod devtools;
mod env;
mod errors;
mod reader;
mod router;
mod screens;
mod theme;
mod ui;
mod util;

fn main() -> eframe::Result<()> {
    let cli = config::Cli::parse();
    app::run(cli)
}
