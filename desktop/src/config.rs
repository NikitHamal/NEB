//! Compile-time constants and command-line options.
use std::path::PathBuf;

pub const APP_NAME: &str = "NEBians";
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const SITE_URL: &str = "https://nebians.consica.com.np";
pub const API_BASE: &str = "https://nebians.consica.com.np/";

/// The API root. Override with `NEB_API_BASE` to point the app at a self-hosted / staging backend
/// (always ends in `/`).
pub fn api_base() -> String {
    let mut b = std::env::var("NEB_API_BASE").ok().filter(|v| v.starts_with("http")).unwrap_or_else(|| API_BASE.to_string());
    if !b.ends_with('/') {
        b.push('/');
    }
    b
}

pub const DEFAULT_WINDOW: [f32; 2] = [1180.0, 780.0];
pub const MIN_WINDOW: [f32; 2] = [640.0, 480.0];

/// Below this width the labelled sidebar collapses to an icon rail.
pub const BREAKPOINT_RAIL: f32 = 1000.0;
/// Below this width the rail becomes a bottom navigation bar.
pub const BREAKPOINT_COMPACT: f32 = 760.0;
/// Reader shows the table-of-contents pane only when the window is at least this wide.
pub const BREAKPOINT_TOC: f32 = 1060.0;

/// Options understood by the binary.
///
/// * `--config <dir>`       where to keep `desktop-state.json` (default: OS config dir)
/// * `--screenshots <dir>`  scripted tour that saves PNGs of every screen, then exits
/// * `--reset`              ignore any saved state
#[derive(Debug, Default, Clone)]
pub struct Cli {
    pub config_dir: Option<PathBuf>,
    pub screenshots: Option<PathBuf>,
    pub reset: bool,
}

impl Cli {
    pub fn parse() -> Self {
        let mut cli = Cli::default();
        let mut args = std::env::args().skip(1);
        while let Some(a) = args.next() {
            match a.as_str() {
                "--config" => cli.config_dir = args.next().map(PathBuf::from),
                "--screenshots" => cli.screenshots = args.next().map(PathBuf::from),
                "--reset" => cli.reset = true,
                "--version" | "-V" => {
                    println!("NEBians Desktop {VERSION}");
                    std::process::exit(0);
                }
                "--help" | "-h" => {
                    println!("NEBians Desktop {VERSION}\n\nUSAGE: nebians [--config DIR] [--reset] [--screenshots DIR]");
                    std::process::exit(0);
                }
                _ => {}
            }
        }
        if cli.config_dir.is_none() {
            cli.config_dir = std::env::var_os("NEB_CONFIG_DIR").map(PathBuf::from);
        }
        cli
    }
}
