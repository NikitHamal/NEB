# Design

## GUI framework: egui / eframe 0.29 (glow backend)
Candidates: egui, iced, slint, fltk-rs.

| | Why / why not |
|---|---|
| **egui (chosen)** | Immediate mode makes a long, heavily custom reader (callouts, tables, inline maths, interactive MCQs, figures) straightforward; painter-level control to reproduce NEBians' flat, hairline-and-pill look; one pure-Rust dependency tree that cross-compiles to `x86_64-pc-windows-gnu` with plain mingw; `egui_extras` gives SVG (resvg) + WebP loaders — the repo's 2,466 SVG and 760 WebP figures render with zero conversion; ~13 MB stripped binary, idle CPU near zero (repaints only on input/animation). |
| iced | Elm-style retained UI is nicer for forms, but rich-text with inline styled spans (super/subscripts in a wrapping paragraph) is much harder; fewer ready loaders. |
| slint | Excellent for fixed-layout UIs; its `.slint` DSL would split the codebase in two languages and its licence is a consideration for a community project. |
| fltk-rs | Native widgets but dated look; custom painting of the NEBians style would fight the toolkit. |

Trade-offs accepted: egui draws its own widgets (not OS-native controls) and text is not shaped with HarfBuzz, so complex Devanagari conjuncts rely on Poppins' precomposed glyphs; accessibility (AccessKit) is not wired in v0.1.

## Theme mapping
`src/theme/colors.rs` copies Android's `NebAuthPalette.kt`: page `#FFFFFF`/`#0C0C0D`, card, field `#F4F4F5`/`#17171A`, ink, muted/faint ink, hairlines, brand `#004AC6` / `#B4C5FF`, danger. Semantic greens/ambers/violets come from `Color.kt` accent pairs. Subject tiles use the `color` field of the syllabus JSON (lightened 38 % in dark mode). `theme/spacing.rs`: `WebCardShape` 14, `WebPanelShape` 18, pill 999. `theme/fonts.rs`: Poppins Regular/Medium/Bold + Poppins Devanagari (woff2 from `static/web/fonts/app` converted to TTF) with egui's bundled fonts as fallback for maths glyphs. The logo is the repo's `n-logo-512.png`.

Android rules honoured: mono chrome (blue only for action/brand), no shadows/glows, no bullet prefixes in UI copy, minimal static empty states (one icon + a line), no ripple (colour/hover transitions only), brand blue used for "NEBians" in the welcome headline.

## Layout system
`LayoutMode::from_width` (recomputed each frame): **Wide** ≥ 1000 px — 236 px labelled sidebar; **Rail** 760–1000 — 76 px icon rail; **Compact** < 760 — bottom navigation bar (min window 640×480). Pages are centred columns capped at 1120 px with `ui::widgets::grid` reflowing cards into as many columns as fit. The reader adds a 272 px TOC pane when ≥ 880 px of content width is free, and caps the text column at 620/740/900 px × √(text scale).

## Desktop behaviours
Native title bar (OS decorations) + in-app menu bar; window size/position remembered; Tab-focus rings on every control; hover animation + pointing-hand cursor; mouse back/forward buttons; smooth keyboard scrolling in the reader; system dark-mode detection.
