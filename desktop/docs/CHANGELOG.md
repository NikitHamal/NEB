# Changelog (desktop/claude branch)

1. `ENV.md` — real probes: git OK, repo is private (PAT required), Rust missing → installed, mingw + `x86_64-pc-windows-gnu` installed.
2. Native Rust/egui app: theme (Android palette + Poppins), data layer (models, content loader, store, search, auth), reader engine (HTML→blocks, LaTeX typesetting, renderer), widgets, nav, menu, all screens (splash, login, email auth, 13-step onboarding, home, library/category, subject, reader, search, bookmarks, downloads, settings, profile, about), shell + shortcuts.
3. Reader jump fix (late-loading figures), 22 screenshots from the running binary, `.cargo/config.toml` for mingw.
4. Build scripts (`build.sh`, `build-windows.ps1/.bat`, `bundle-content.sh`, `screenshots.sh`), GitHub Actions workflow, docs.
5. Windows `.exe` cross-built, fresh-clone verification (see BUILD.md).


## Session 2 — Material 3 Expressive rebuild + real accounts (v0.2.0)
- `backend: desktop browser hand-off sign-in` — PKCE-style start/poll API, `/desktop-auth/` consent page, 10 tests.
- `desktop: Material 3 Expressive redesign` — Material Icons Rounded font (official codepoints), Android M3 palette (light/dark roles), 20/28dp shapes, pill buttons that morph on press, tonal chips, floating-label text fields, nav rail / compact rail / bottom bar with spring pill indicators and unread badge.
- **Fixed invisible input text**: the old `text_field` painted its background *after* the editor, covering the text. New fields paint background → label → editor, with an explicit text colour.
- Login rebuilt like Android: Google, GitHub, email, guest; desktop split layout with brand panel; "waiting for your browser" state with countdown / reopen / cancel.
- Email flow restyled; added the missing password-reset step (`auth/email/reset-password/`).
- Complete-profile step (live `check-username`) after first Google/GitHub sign-in.
- Community (live feed, category filters, pagination, like, bookmark, thread with replies, composer incl. anonymous), Notifications (unread badge polling, mark-all-read, deep links), profile pull/push to the account, change-password dialog, server-side sign-out. 401 anywhere drops the dead session and returns to sign-in.
- `NEB_API_BASE` override; `--screenshots` tour now covers 31 screens (signed-in screens use clearly-marked sample data, see LIMITATIONS).

## 0.4.0
- Guest mode removed everywhere; only signed-in accounts enter the app.
- New in-app account centre: edit profile, security (change email with code, set/change password, sign out), privacy and terms viewer, account deletion with 30-day cancel window.
- Privacy / Terms open as an in-app sheet from sign-in; no screen opens the website. Chapter links copy to the clipboard.
- Shared M3 dialog (scrim + rise) and animated tab row replace ad-hoc windows.
- Welcome tour rebuilt: live product scenes, step counter, chips, library numbers, subject ticker, drifting backdrop.
- Helper subtitles removed from headers and profile setup; page/step entrance motion unified.
- Dead code removed (old menu bar, duplicated password dialog, unused helpers); 0 compiler warnings.
