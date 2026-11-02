# Limitations (honest list)

**Verified for real this session**
- Rust client ↔ Django: browser hand-off end to end against a local server (see BACKEND.md / BUILD.md).
- Backend: 10 new tests pass (`api.test_desktop_auth`).
- UI: 31 screenshots from the running Linux build.

**Not verified / not done**
- **Google and GitHub buttons have not been exercised against the production site** with a real Google/GitHub account — I have no such account here, and the hand-off relies on the website's existing login. The hand-off, consent page, token issue and API use *were* tested with a session established through the site's own `token-login`. If the production site's Google/GitHub login works in a browser, this works; deploy the backend commit first, otherwise `auth/desktop/start/` returns 404 and the app shows that error.
- **Authenticated screenshots use sample data.** Community / Notifications / Profile screenshots are rendered with bundled fixtures (`Env::demo`, only reachable via `--screenshots`) because the sandbox has no user account. The live code paths (requests, parsing, error handling) are the same functions; the Community *guest* feed and the whole hand-off were checked against real servers only for the hand-off.
- **Community response shapes** come from the Android DTOs; parsing is tolerant, but replies/likes were not exercised against production data.
- **Remote images** (profile photos, post images, attachments) are not loaded — no HTTP image loader is enabled; avatars are monograms. Polls, attachments and voice notes in posts aren't rendered.
- **Not in the desktop app:** Neby AI, Study Lab/Space, Canvas, marketplace, uploads, People/follow, result checker, credits, analytics, interactive lessons (the Web app tile opens them). Account deletion and email change open the website.
- **Maths is linearised**, not 2-D typeset (`\frac{a}{b}` → `a/b`). No in-app PDF viewer (PDFs open in the system viewer). No HarfBuzz shaping; AccessKit (screen reader) not enabled.
- **Windows `.exe`:** cross-compiled with mingw; it could not be launched here (no Windows/wine). CI workflow `desktop-windows.yml` builds natively. The app needs OpenGL 2+.
- **Content is read from the repo layout** (or a bundled `content/` folder) and isn't embedded in the binary.
- Mac builds untested. Session tokens are stored in the per-user state file (`desktop-state.json`) in plain text, like the Android app's preferences; OS keychain storage is not implemented.
