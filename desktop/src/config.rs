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
pub const MIN_WINDOW: [f32; 2] = [820.0, 560.0];

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
    /// `--size 1440x900`: open at this inner size (used for screenshots / testing layouts).
    pub size: Option<[f32; 2]>,
    /// `nebians book.pdf` or `--open-pdf book.pdf`: open straight into the PDF viewer.
    pub open_pdf: Option<PathBuf>,
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
                "--open-pdf" => cli.open_pdf = args.next().map(PathBuf::from),
                other if other.to_ascii_lowercase().ends_with(".pdf") => cli.open_pdf = Some(PathBuf::from(other)),
                "--size" => {
                    cli.size = args.next().and_then(|v| {
                        let (w, h) = v.split_once('x')?;
                        Some([w.parse().ok()?, h.parse().ok()?])
                    })
                }
                "--version" | "-V" => {
                    println!("NEBians Desktop {VERSION}");
                    std::process::exit(0);
                }
                "--help" | "-h" => {
                    println!("NEBians Desktop {VERSION}\n\nUSAGE: nebians [--config DIR] [--reset] [--size WxH] [--screenshots DIR]\n\nEnvironment: NEB_API_BASE=https://your-backend/  (default: the NEBians production API)");
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
