//! The content reader engine: chapter HTML → block model → native egui widgets.
//!
//! * `model`  — `Block` / `Span` data structures
//! * `html`   — parses the exporter's HTML subset (via `scraper`) into blocks
//! * `math`   — converts the LaTeX in `span.m` / `div.dm` into styled spans
//!              (italic variables, real super/subscripts, Greek, operators)
//! * `render` — paints blocks: callout boxes, tables, figures, interactive MCQs …
pub mod html;
pub mod math;
pub mod model;
pub mod render;
