# Changelog (desktop/claude branch)

1. `ENV.md` — real probes: git OK, repo is private (PAT required), Rust missing → installed, mingw + `x86_64-pc-windows-gnu` installed.
2. Native Rust/egui app: theme (Android palette + Poppins), data layer (models, content loader, store, search, auth), reader engine (HTML→blocks, LaTeX typesetting, renderer), widgets, nav, menu, all screens (splash, login, email auth, 13-step onboarding, home, library/category, subject, reader, search, bookmarks, downloads, settings, profile, about), shell + shortcuts.
3. Reader jump fix (late-loading figures), 22 screenshots from the running binary, `.cargo/config.toml` for mingw.
4. Build scripts (`build.sh`, `build-windows.ps1/.bat`, `bundle-content.sh`, `screenshots.sh`), GitHub Actions workflow, docs.
5. Windows `.exe` cross-built, fresh-clone verification (see BUILD.md).
