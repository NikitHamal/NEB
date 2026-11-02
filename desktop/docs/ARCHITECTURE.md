# Architecture

```
src/
  main.rs        thin entry: parse CLI → app::run
  app.rs         NebApp (eframe::App): shell, global shortcuts, Action dispatcher, window persistence
  env.rs         Env — services shared by all screens (theme, Store, ContentRoot, caches, actions, toasts)
  actions.rs     Action enum (UI → app commands); router.rs Route + back/forward history
  config.rs errors.rs util.rs devtools.rs (screenshot tour)
  theme/         colors, fonts, spacing, egui Visuals/Style application
  ui/            widgets (buttons, chips, cards, toggle, grid…), icons (painter-drawn), nav, menu, logo, avatar, toast, shortcuts
  data/          models (serde), content (locate + load repo JSON), store (persisted state), search, auth (ureq), tasks
  reader/        html (scraper → Block model), math (LaTeX → styled spans), model, render (egui widgets)
  screens/       splash login email_auth onboarding home library subject reader search bookmarks downloads settings profile about
```

**Data flow.** `NebApp::update` → input → `shell()` draws menu/nav and dispatches the current `Route` to a screen's `show(ui, env, state)`. Screens never mutate the router; they push `Action`s on `env.actions`, applied after the frame. Persisted state (`Store`) is JSON in the OS config dir, written atomically, throttled to 1.5 s.

**Content loading.** `ContentRoot::detect` (flag → saved path → `content/` beside the exe → ancestors of exe/cwd) accepts a repo checkout (`backend_python/web/{data,static/web}`, `notes/pdf`) or a bundled folder. `syllabus/index.json` gives tracks→subjects at startup; per-subject syllabus and `study/<track>-<subject>/index.json` load lazily and are cached. A chapter (`unit-NN|bank-NN|guide.json`) is read and parsed **on a worker thread** (`Task`) into `Doc { blocks, mcq_keys }`; images are referenced as `file://` URIs (`/static/web/study/<hash>.svg`) and decoded by `egui_extras` loaders. `forget_all_images()` runs on chapter change to bound memory.

**Reader.** `html::parse` walks the exporter's HTML subset with `scraper` and builds `Block`/`Span`. `math::to_spans` linearises LaTeX (italic variables, real raised/lowered text, Greek, operators, `\frac`→`a/b`, `\sqrt`→`√`). `render::blocks` paints them (callouts with accent bars, equal-height-row tables, white figure cards, collapsible answers, MCQ cards with correct/incorrect reveal).

**Search.** `SearchIndex::build` runs once in the background from all syllabus files; `fulltext` scans every chapter JSON on demand with an `AtomicBool` cancel flag.

**Testing.** `cargo test` covers the LaTeX converter; the `--screenshots` tour drives every screen headlessly as an end-to-end smoke test.

---

## Session 2 additions

```
src/
  server.rs            impl Env: token, unread polling, profile pull/push, 401 handling, sign-out
  data/api.rs          authenticated JSON client (Bearer header, 401→Unauthorized, 410→Gone, server messages verbatim)
  data/auth.rs         email auth + reset + change-password + logout; Session::from_reply
  data/browser_auth.rs PKCE hand-off client (start / poll) + live e2e test
  screens/auth_flow.rs what happens after any sign-in (profile merge, next route)
  screens/login.rs     Google / GitHub / email / guest + hand-off state machine
  screens/complete_profile.rs, community.rs, notifications.rs
  ui/icons.rs          Material icon font glyphs; ui/nav.rs rail + bottom bar
```
**Data flow for server features.** A screen spawns a `data::tasks::Task` (thread + repaint wake-up) that calls `Api`; the screen polls the task each frame and updates its own state. Any `AppError::Unauthorized` goes through `Env::handle_api_error`, which drops the session and routes to Login. Likes and bookmarks are optimistic and roll back on failure. The unread badge refreshes every 60 s while signed in.
