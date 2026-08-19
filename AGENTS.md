# NEBians - Project Knowledge Base

## Coding Conventions

### Modular Approach (MANDATORY)
- **Keep files under 500-600 lines** where possible. Split large files into focused modules.
- **One responsibility per file.** If a file handles multiple concerns (e.g., job queue + job execution), split them.
- **New features get their own module files.** Don't stuff new logic into existing catch-all files.
- Examples of good modular splits: `api/generation.py` (queue) + `api/generation_executors.py` (per-type handlers) + `api/management/commands/run_generation_worker.py` (daemon).
- When a file exceeds ~600 lines, consider extracting helpers/utilities/sub-features into separate files.

### General
- **No comments** unless explicitly requested.
- Follow existing code style in each file.
- Use existing libraries already in the codebase; don't assume third-party packages exist.
- Always check `requirements.txt` before adding new dependencies.
- **Django 5.2 templates:** `{% endblock %}`, `{% else %}`, and similar block tags MUST be on a single line. Multi-line splits (`{% endblock\n%}` or `{%\nendblock %}`) cause cryptic "Unclosed tag" errors.

## Overview

NEBians is a Material 3 Android app for Nepali students (NEB curriculum). It provides study resources (ebooks, PDFs, notes), a discussion forum, and an advanced PDF viewer with annotation tools.

**Package:** `com.neb.ians`
**Min SDK:** 24 (legacy) / 28 (modern)
**Target SDK:** 36

---

## Architecture Decisions

### Tech Stack
- **Language:** Kotlin
- **UI:** Jetpack Compose with Material 3
- **DI:** Hilt (Dagger)
- **Database:** Room (local-first, offline-ready)
- **State Management:** StateFlow + ViewModel
- **Navigation:** Navigation Compose (single Activity)
- **Preferences:** DataStore
- **Background Work:** WorkManager (Hilt-injected workers)
- **Image Loading:** Coil
- **PDF Rendering:** Android PdfRenderer API (no third-party dependency)
- **Fonts:** Poppins (Google Fonts, bundled as TTF)

### Why Local-First
All data is stored in Room. The app seeds sample data on first launch via a WorkManager one-time task. This makes the app fully functional offline. A backend can be added later by syncing with the local Room database.

### Why PdfRenderer over Third-Party
Android's built-in PdfRenderer avoids large APK size increases from libraries like PDFium. It handles basic rendering well. Annotations are stored as Room entities overlaid on the PDF canvas via Compose Canvas.

### Product Flavors
Two flavors in "target" dimension:
- `modern` (minSdk 28) â€” for newer Android devices
- `legacy` (minSdk 24) â€” broader compatibility

Both use the same release signing config.

### Navigation Architecture
- Bottom navigation: Home, Library, Forum, Settings
- Standalone screens (full-screen, not fragments): ForumPostDetail, CreatePost, Reply, PdfReader, Search
- Forum screens are standalone to match the requirement of not being fragments or nav items

---

## App Structure

```
com.neb.ians/
â”œâ”€â”€ NEBiansApp.kt          # Application class (Hilt, WorkManager, notification channels)
â”œâ”€â”€ MainActivity.kt        # Single activity with Compose + dark mode
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ local/
â”‚   â”‚   â”œâ”€â”€ dao/           # Room DAOs (Resource, Annotation, Forum, Bookmark)
â”‚   â”‚   â”œâ”€â”€ entity/        # Room entities (5 tables)
â”‚   â”‚   â””â”€â”€ database/      # NEBiansDatabase
â”‚   â”œâ”€â”€ model/
â”‚   â”‚   â””â”€â”€ SampleData.kt  # Seed data (20 resources, 6 forum posts, 5 replies)
â”‚   â””â”€â”€ repository/        # Repository layer (Resource, Forum, Annotation, Bookmark, Settings)
â”œâ”€â”€ di/
â”‚   â”œâ”€â”€ AppModule.kt       # DataStore provider
â”‚   â””â”€â”€ DatabaseModule.kt  # Room database + DAO providers
â”œâ”€â”€ ui/
â”‚   â”œâ”€â”€ Navigation.kt      # NavHost, Screen routes, bottom nav
â”‚   â”œâ”€â”€ theme/             # M3 theme (Color, Type with Poppins, Theme)
â”‚   â””â”€â”€ screens/
â”‚       â”œâ”€â”€ home/          # HomeScreen + HomeViewModel
â”‚       â”œâ”€â”€ library/       # LibraryScreen + LibraryViewModel (categorization + filters)
â”‚       â”œâ”€â”€ forum/         # ForumScreen, PostDetail, CreatePost, Reply + ViewModels
â”‚       â”œâ”€â”€ reader/        # PdfReaderScreen, AnnotationOverlay, ReaderViewModel
â”‚       â”œâ”€â”€ search/        # SearchScreen + SearchViewModel
â”‚       â””â”€â”€ settings/      # SettingsScreen + SettingsViewModel
â”œâ”€â”€ util/
â”‚   â”œâ”€â”€ TimeUtils.kt       # formatTimeAgo(), getSubjectColor()
â”‚   â””â”€â”€ NotificationHelper.kt  # WorkManager scheduling helpers
â””â”€â”€ worker/
    â”œâ”€â”€ DataSeederWorker.kt      # Seeds sample data on first launch
    â””â”€â”€ NotificationWorker.kt   # Push notification worker
```

---

## Actions Taken

### Initial Build
1. Created full Android project structure with Gradle (Kotlin DSL)
2. Set up Gradle wrapper (8.5), build configs, proguard rules
3. Generated release keystore (`nebians-release.keystore`) â€” committed to repo for CI
4. Downloaded Poppins font files (Regular, Medium, SemiBold, Bold, Light)
5. Created adaptive icon (book shape foreground)

### Database Layer
1. Designed 5 Room entities: Resources, Annotations, ForumPosts, ForumReplies, Bookmarks
2. Created 4 DAOs with Flow-based queries, search, filtering, sync queries
3. Set up Room database with fallback destructive migration

### DI & Repository
1. Hilt modules for Database and DataStore
2. 5 repository classes wrapping DAOs with business logic
3. Settings repository with DataStore preferences (dark mode, username, notifications, wifi-only)

### UI Screens (all Jetpack Compose + M3)
1. **Home:** Greeting, search bar, subject chips, recent/popular resource carousels, forum activity
2. **Library:** 3-tier filter system (subject, grade, type), grid of resource cards
3. **Search:** Auto-focus search bar, suggestion chips, result list
4. **Forum:** Category filter chips, post list with thumbs-up, FAB for new post
5. **Post Detail:** Full post view, replies with nested thumbs-up, reply FAB
6. **Create Post:** Title, content fields, category dropdown
7. **Reply:** Context card, content field, submit
8. **PDF Reader:** Bitmap rendering, annotation overlay (highlight/underline/sticky note), color picker, page navigation, bookmarks, zoom
9. **Settings:** Profile, dark mode toggle, notifications, downloads, about

### CI/CD
1. GitHub Actions workflow for signed release APK builds (2 flavors)
2. APK naming: `NEBians-{flavor}-v{version}-{commitHash}.apk`
3. Gradle caching, parallel execution, JVM optimizations
4. Separate lint workflow for PRs

---

## Audit Findings

### Design Consistency
- All screens use M3 components (no legacy Material)
- Thumb up icon (ThumbUp) used instead of heart/love throughout
- Outlined icons for inactive states, filled for active
- No excessive shadows or gradients â€” flat M3 design
- Poppins font applied to all typography styles

### Potential Improvements
- Add network layer (Retrofit/Ktor) for remote resource fetching
- Implement actual PDF file downloading with progress
- Add user authentication for forum
- Room database migration strategy for version 2+
- Add unit tests and UI tests

---

## Known Issues

1. **PDF rendering fallback:** When no actual PDF file exists at the resource's localPath, the reader shows a placeholder page. A sample PDF is generated but may not render correctly on all devices.
2. **Keystore in repo:** The release keystore is committed directly to the repo per requirement. In production, this should be moved to CI secrets.
3. **No backend:** All data is local. Forum posts and resources are seeded from SampleData and don't sync.

---

## Deployment Notes

### GitHub Actions
- **build-release.yml:** Triggers on push to any branch, PRs to main, and manual dispatch
- **lint.yml:** Triggers on PRs to main only
- Keystore is at repo root: `nebians-release.keystore` (alias: nebians, password: ***REMOVED***)
- Artifacts retained for 30 days

### Building Locally
```bash
./gradlew assembleModernRelease    # Modern APK (minSdk 28)
./gradlew assembleLegacyRelease    # Legacy APK (minSdk 24)
```

---

## Web Backend â€” Server & SSH Deployment

### Server Details
- **Host:** `192.250.235.158` (cPanel / CloudLinux / LiteSpeed + LSAPI)
- **Username:** `consicac`
- **SSH Key:** Stored in `.ssh_deploy_info.json` (RSA private key)
- **Remote Project Dir:** `/home/consicac/nebians_api/`
- **Virtualenv:** `/home/consicac/virtualenv/nebians_api/3.13/`
- **Python:** 3.13
- **Web Server:** LiteSpeed + LSAPI (NOT Phusion Passenger, NOT gunicorn). The cPanel Python Selector wraps LiteSpeed, which runs `lswsgi -m /home/consicac/nebians_api/passenger_wsgi.py`. Restart by `touch /home/consicac/nebians_api/tmp/restart.txt`.
- **WSGI Entry Point:** `passenger_wsgi.py` (kept for historical reasons; actually loaded by LSAPI)
- **Log File:** `/home/consicac/nebians_api/logs/nebians.log`
- **Domain:** `nebians.consica.com.np` (also `www.nebians.consica.com.np`)
- **Daphne (WebSocket server):** `127.0.0.1:8001` (background, managed via crontab `@reboot`). Log: `/home/consicac/nebians_api/logs/daphne.log`
- **Cloudflared (WS tunnel):** Background process; `~/.local/bin/cloudflared --protocol http2 --url http://127.0.0.1:8001`. Log: `/home/consicac/nebians_api/logs/cloudflared.log`

### CRITICAL: How to Deploy
**ALWAYS use the local deploy script â€” NEVER use manual SCP/SSH commands.**

```powershell
# From the backend_python/scratch/ directory:
cd F:\NEB\backend_python\scratch
.\deploy.ps1
```

The deploy script (`backend_python/scratch/deploy.ps1`) handles:
1. Reading SSH key from `.ssh_deploy_info.json`
2. Creating a ZIP of all deployment files (api/, nebians/, web/, manage.py, requirements.txt, passenger_wsgi.py)
3. Uploading ZIP via SCP
4. Running remote commands: unzip, pip install, collectstatic, migrate, copy static files to public/, restart LiteSpeed (touch tmp/restart.txt)

**Do NOT manually SCP individual files or run SSH commands for deployment.** Use `deploy.ps1` instead. Manual SCP/SSH should only be used for quick debugging (e.g., checking logs, running Django shell queries).

### CRITICAL: .env File Overrides settings.py Defaults
The `.env` file at `/home/consicac/nebians_api/.env` is loaded by `dotenv` in `settings.py`. **Environment variables override `settings.py` defaults.** If you change a default value in `settings.py` but the `.env` still has the old value, the `.env` wins.

**Always check the `.env` file on the server after changing `settings.py`:**
```bash
ssh ... consicac@192.250.235.158 "cat /home/consicac/nebians_api/.env"
```

**The `load_dotenv()` call uses `override=True`** so `.env` values will override system env vars. But if a system-level env var is set (e.g., in cPanel), it still takes precedence. When in doubt, update both `.env` AND `settings.py`.

### CRITICAL: LiteSpeed/LSAPI vs Gunicorn
The server uses **LiteSpeed + LSAPI** (cPanel Python app), NOT gunicorn, NOT vanilla Phusion Passenger. Do NOT try to start/stop gunicorn. To restart the Django app:
```bash
rm -rf /home/consicac/nebians_api/tmp/*
touch /home/consicac/nebians_api/tmp/restart.txt
```
LiteSpeed picks up changes after this. If env vars don't update, you may need to wait 30-60 seconds for LSAPI to fully respawn workers.

### CRITICAL: SSL/Cookie Settings
`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, and `CSRF_COOKIE_SECURE` are all set to `False` by default. This is intentional â€” LiteSpeed terminates SSL at the proxy level, so Django sees HTTP connections. Setting these to `True` causes infinite redirects or dropped cookies. Only enable them if you configure LiteSpeed to forward the `X-Forwarded-Proto` header correctly.

### Checking Logs
```bash
ssh ... consicac@192.250.235.158 "tail -50 /home/consicac/nebians_api/logs/nebians.log"
# Auth-related errors:
ssh ... consicac@192.250.235.158 "grep -i 'auth\|login\|token\|google\|error' /home/consicac/nebians_api/logs/nebians.log | tail -30"
# cPanel error log:
ssh ... consicac@192.250.235.158 "tail -50 /home/consicac/logs/error_log"
```

### GitHub Actions Auto-Deploy
The `.github/workflows/deploy-backend.yml` workflow auto-deploys on push to `main` when files under `backend_python/` change. It:
1. SCPs files to `/home/consicac/nebians_api/`
2. Runs `pip install -r requirements.txt`
3. Runs `collectstatic` and `migrate`
4. Touches `tmp/restart.txt`

**BUT** it does NOT update the `.env` file. If you change env-dependent settings, manually update `.env` on the server.

### CRITICAL: Static Files Deployment â€” WhiteNoise Serves From staticfiles/, NOT public/static/
**Verified Aug 2026:** The domain's document root (`/home/consicac/nebians.consica.com.np/`) contains **NO `static/` directory** â€” only Passenger `.htaccess`, `api/`, `cgi-bin/`, and a `media` symlink. Static files are served by the **WhiteNoise middleware** (`whitenoise.middleware.WhiteNoiseMiddleware`, position 0 in MIDDLEWARE) straight from Django's `STATIC_ROOT = /home/consicac/nebians_api/staticfiles/`. Files that exist ONLY in `public/static/` return 404 (proven with test files). The `public/static/` copies in `deploy.ps1` are harmless but NOT what serves traffic.

**CRITICAL â€” stale WhiteNoise index:** WhiteNoise builds an in-memory file index when the lswsgi worker process starts. If you deploy new static files (or edit existing ones) and the worker does NOT actually respawn, requests for those files fall through to Django's 404 handler â€” the response carries Django's security headers (`content-security-policy`, `set-cookie: csrftoken`, `permissions-policy`). Diagnosis: a 404 on a file that EXISTS in `staticfiles/`, with Django CSP headers (not LiteSpeed's plain 404). Fix â€” force a worker respawn and WAIT:

```bash
cd /home/consicac/nebians_api
rm -rf tmp/*
touch tmp/restart.txt
sleep 45   # LSAPI respawn takes 30-60s; verify with: ps -eo pid,lstart,cmd | grep lswsgi
curl -sI https://nebians.consica.com.np/static/web/css/pages/<new-file>.css | head -3   # expect 200
```

**NEVER do these:**
- Do NOT change `STATICFILES_STORAGE` from `whitenoise.storage.CompressedManifestStaticFilesStorage` â€” note Django 5.1+ `STORAGES['staticfiles']` also exists in settings.py and must stay consistent
- Do NOT delete `.gz` files or hashed manifest files from `staticfiles/`
- Do NOT change `STATIC_ROOT` â€” it must stay as `BASE_DIR / 'staticfiles'`

### CRITICAL: Background Agent Worker Must Restart After Deploy
Model resolution (LLM provider switching, BYOK keys, custom providers) lives in the **worker process**, not the LSAPI web process. After deploying new backend code:

```bash
# Restart both the web process AND the worker
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
cd /home/consicac/nebians_api

# Kill old workers
pkill -f run_background_agent_worker 2>/dev/null
pkill -f run_autofix_watch 2>/dev/null

# Start fresh
nohup python manage.py run_background_agent_worker >> logs/worker.log 2>&1 & disown
nohup python manage.py run_autofix_watch >> logs/autofix.log 2>&1 & disown

# Restart LSAPI web process
rm -rf tmp/* && touch tmp/restart.txt
```

**If the website is restarted but the worker isn't, the old worker keeps falling back to Qwen 3.7 Plus** â€” model picks from the UI "don't work" because the old worker's LLM resolution code is stale. **Always restart both.**

Verify with:
```bash
ps aux | grep -E 'run_background_agent_worker|run_autofix_watch' | grep -v grep
```

---

## Web Backend â€” Architecture

### Django Project Structure
```
backend_python/
â”œâ”€â”€ nebians/               # Django project settings
â”‚   â”œâ”€â”€ settings.py        # Main settings (loads .env with dotenv override=True)
â”‚   â”œâ”€â”€ middleware.py       # SecurityHeadersMiddleware (CSP, Permissions-Policy, COOP)
â”‚   â”œâ”€â”€ urls.py            # Root URL config (admin at /admin/, Django admin at /admin-django/)
â”‚   â””â”€â”€ wsgi.py            # WSGI entry point
â”œâ”€â”€ api/                   # REST API app
â”‚   â”œâ”€â”€ models.py          # User, Resource, Post, Reply, Follow, Report, etc.
â”‚   â”œâ”€â”€ views.py           # API endpoints (paginated, rate-limited)
â”‚   â”œâ”€â”€ authentication.py  # Token auth + Google token verification
â”‚   â”œâ”€â”€ security.py        # Password hashing, verification code hashing, URL validation, image upload validation
â”‚   â”œâ”€â”€ throttles.py       # AuthRateThrottle, VerificationRateThrottle
â”‚   â”œâ”€â”€ admin.py           # Django admin registrations (at /admin-django/)
â”‚   â”œâ”€â”€ admin_views.py     # Custom admin API views (staff auth + signed internal headers)
â”‚   â”œâ”€â”€ serializers.py     # DRF serializers
â”‚   â””â”€â”€ management/
â”‚       â””â”€â”€ commands/
â”‚           â””â”€â”€ cleanup_stale_data.py  # Expired codes, stale FCM tokens, old sessions
â”œâ”€â”€ web/                   # Web frontend app (Django templates)
â”‚   â”œâ”€â”€ views.py           # Page views + AJAX endpoints
â”‚   â”œâ”€â”€ api_client.py      # Internal API client (uses signed internal headers for admin calls)
â”‚   â”œâ”€â”€ urls.py             # URL routing
â”‚   â”œâ”€â”€ templates/          # HTML templates (base.html, web/*.html)
â”‚   â””â”€â”€ static/web/css/
â”‚       â”œâ”€â”€ material3.css   # M3 design system (CSS custom properties)
â”‚       â””â”€â”€ app.css         # App-specific styles
â”œâ”€â”€ .env                   # Environment variables (DEPLOYED TO SERVER)
â””â”€â”€ manage.py
```

### Authentication Flow
1. **Google Sign-In:** Uses Google Identity Services (GIS) â€” `accounts.google.com/gsi/client`
   - GIS `initialize()` + `renderButton()` renders the Google button
   - On sign-in, GIS sends a JWT `credential` to `handleCredentialResponse()`
   - Frontend POSTs the credential to `/auth/google/` as `{ idToken: credential }`
   - Backend verifies via `google.oauth2.id_token.verify_oauth2_token()` against both `GOOGLE_CLIENT_ID` and `FIREBASE_PROJECT_ID`
   - On success, creates/updates User in DB and sets session cookie
   - **Auth tokens are NOT regenerated on each login** â€” only created on first signup. This prevents session invalidation.

2. **Email Auth:** Direct email/password signup with verification codes
   - POSTs to `/api/auth/email/signup/`, `/api/auth/email/verify/`, `/api/auth/email/login/`
   - Verification codes are hashed with Django's password hasher (not stored as plaintext)
   - Rate-limited: 6 verification attempts per hour, 20 auth requests per minute
   - Passwords hashed with Django's `make_password` (bcrypt/argon2), not raw SHA-256
   - Legacy SHA-256 passwords are transparently migrated on successful login

### CRITICAL: Session-Based Auth (NOT Bearer Tokens in JS)
- Auth tokens are **no longer exposed in page HTML**. The template context does NOT include `auth_token`.
- Frontend JS uses `IS_AUTHENTICATED` (boolean) instead of `AUTH_TOKEN` (secret string).
- All authenticated AJAX calls use `credentials: 'same-origin'` to send the session cookie.
- The `_get_valid_token()` helper in `web/views.py` reads from the session first, falls back to `Authorization: Bearer` header, and validates against the DB. If the token is stale, it clears the session and returns 401.
- Admin API calls use a short-lived signed `X-Internal-Admin-Signature` header (Django `TimestampSigner`), NOT the old shared `ADMIN_TOKEN` bearer.

### CRITICAL: Admin Panel Auth
- The custom admin panel at `/admin/` now uses **Django's built-in staff user authentication** (login/logout sessions).
- The old shared `ADMIN_TOKEN`/`ADMIN_PASSWORD` system is removed.
- Server-side admin API calls use `X-Internal-Admin-Signature` headers generated by `api.security.make_internal_admin_signature()`.
- Django's built-in admin is at `/admin-django/` (for database management).
- **Admin superuser credentials:** username=`admin`, password=`***REMOVED***`
- Create new superusers with: `python manage.py createsuperuser`

### CRITICAL: Google Auth Configuration
- **OAuth Client ID:** `68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com`
- **Firebase Project:** `nebiansnepal`
- **Authorized JavaScript Origins** (in Google Cloud Console â†’ Credentials):
  - `http://localhost`
  - `http://localhost:8000`
  - `https://nebiansnepal.firebaseapp.com`
  - `https://nebians.consica.com.np`
  - `https://www.nebians.consica.com.np`
- **OAuth Consent Screen:** Must be in **Production** mode (not Testing) or users outside the test list will be blocked

### CRITICAL: GIS Implementation Notes
- **DO NOT use Firebase Auth (`signInWithRedirect`, `signInWithPopup`)** â€” it causes `redirect_uri_mismatch` errors
- **DO NOT use `google.accounts.oauth2.initTokenClient()`** â€” it returns access tokens, NOT ID tokens
- **DO NOT use `google.accounts.id.prompt()`** â€” causes FedCM errors and double-initialize warnings
- **DO use `google.accounts.id.initialize()` + `google.accounts.id.renderButton()`** â€” this is the correct GIS approach
- The `handleCredentialResponse` callback receives a `response.credential` (JWT) which is sent to the backend
- Use plain `function` declarations (not `const` arrow functions) for callbacks that GIS calls â€” they must be globally accessible
- The GIS script must be loaded BEFORE calling `initialize()` â€” use the `window.addEventListener('load', ...)` + polling pattern
- **Never call `initialize()` more than once** â€” it causes "called multiple times" warnings

### Security Model
- **Passwords:** Django's `make_password` (bcrypt/argon2). Legacy SHA-256 hashes are transparently migrated on login.
- **Verification codes:** Hashed with Django's password hasher. Not stored as plaintext. Includes purpose field, attempt tracking (max 5), and resend cooldown (60s).
- **Auth tokens:** Not regenerated on each login (only on signup). Prevents session invalidation.
- **Rate limiting:** Auth endpoints: 20/min. Verification endpoints: 6/hour. Post creation, follow toggle, FCM registration: 20/min. General: 100/hour anon, 1000/hour authenticated.
- **Profile photos:** Uploaded images validated with PIL (format check, size limit 5MB, metadata stripped). URLs validated for HTTPS-only, no private/local hosts.
- **Resource URLs:** Must be HTTPS, no private/local hosts.
- **XSS protection:** `escapeHtml()` and `safeClientUrl()` helpers in base.html for all user-submitted content in JS templates.
- **Security headers:** CSP, Permissions-Policy, COOP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy set via `SecurityHeadersMiddleware`.
- **Admin auth:** Django staff sessions + signed internal API headers. No shared bearer tokens.
- **Locked profiles:** When `is_locked=True`, personal data (email, DOB, school, etc.), stats, posts, and follower lists are hidden from non-owners.

### CSS Hover Fix (Light Mode)
In light mode, text buttons and outlined buttons had solid blue (`var(--md-primary-container)` = `#2563EB`) hover backgrounds. Fixed by using subtle transparent overlays:
- `.md-btn-text:hover` â†’ `rgba(0, 74, 198, 0.08)` (was `var(--md-primary-container)`)
- `.md-btn-outlined:hover` â†’ `rgba(0, 74, 198, 0.08)` (was `var(--md-primary-container)`)
- `.auth-text-btn:hover` â†’ `rgba(0, 74, 198, 0.08)` (was `var(--md-primary-container)`)
- `.auth-link-btn:hover` â†’ `rgba(0, 74, 198, 0.08)` with `color: var(--md-primary)` (was solid fill)

---

## Community Chat Proxies (Neby AI on Android + web)

The "Neby AI" chat (Android `NebyAiViewModel`, web `subject_page.html` chat panel, admin bot panel) talks to a set of free, keyless web-chat proxies through a shared Django session store. **The AI4Bharat Arena proxy was removed (Aug 2026)** â€” no code, UI, or docs references remain (except in applied historical migrations). Sessions use `ArenaChatSession`/`ArenaChatMessage` rows with a `provider` discriminator:

| Provider slug | Proxy module | Default model | Notes |
|---|---|---|---|
| `qwen` | `api/qwen_proxy.py` + `api/qwen_utils/` | `qwen3.8-max` | Text + file upload (multipart), the default for web chat and Android |
| `k2think` | `api/k2think_proxy.py` | `MBZUAI-IFM/K2-Think-v2` | Stateless, history replayed from DB |
| `poolside` | `api/poolside_proxy.py` | `laguna-s-2.1` | Stateless |
| `motiftech` | `api/motiftech_proxy.py` | `motif-102b` | Stateless; conversation id kept in `arena_token_id` |
| `egov` | `api/egov_proxy.py` | `AI1` | Scraper |
| `deepai` | `api/deepai_proxy.py` | `standard` | Scraper |
| `inception` | `api/inception_proxy.py` | `mercury-2` | Scraper, `reasoning_effort` kwarg |

Community/stateless sessions (`k2think`, `poolside`, `motiftech`) are streamed through `_stream_community` in `api/arena_views.py` â€” history is replayed from the session rows so send and regenerate both work without upstream session state. Qwen/egov/deepai/inception have their own send endpoints under `/ajax/neby-arena/<slug>/...` (web) and `/api/neby-arena/<slug>/...` (mobile).

### Endpoints (DRF, require `Authorization: Bearer <auth_token>`)
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/neby-arena/models/` | List community LLM models (Redis-cached 5 min) |
| GET/POST | `/api/neby-arena/sessions/` | List / create chat sessions (community models only) |
| GET/PATCH/DELETE | `/api/neby-arena/sessions/<id>/` | Session detail / update / delete |
| POST | `/api/neby-arena/sessions/<id>/messages/` | Send message (community) â€” **SSE streaming** |
| POST | `/api/neby-arena/messages/<id>/regenerate/` | Regenerate last assistant reply â€” **SSE streaming** |
| GET/POST | `/api/neby-arena/{qwen,egov,deepai,inception,k2think,poolside}/models/` + `/sessions/` + `/sessions/<id>/messages/` | Per-provider endpoints |

### SSE wire format (OpenAI-compatible)
```
data: {"choices":[{"index":0,"delta":{"role":"assistant","messageId":"...","userMessageId":"..."}}]}

data: {"choices":[{"index":0,"delta":{"content":"chunk"}}]}

...
data: {"choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```
On error mid-stream:
```
data: {"error":{"message":"...","code":"upstream|server|not_found"}}

data: [DONE]
```

### Gotchas
- **Streaming generator uses pre-insert + finalise** â€” we save the assistant row in `pending` state at request start, then update with content on completion. If the client disconnects mid-stream, the partial content is still in the DB.
- **Regenerate reuses the assistant row's id** â€” so the client doesn't need to re-render. The `preinsert_assistant=False` flag in `_stream_regenerate` is critical, and the target message id is passed as `assistant_message_id` so `_build_history(stop_at_msg_id=...)` cuts off the answer being replaced.
- **Unknown/legacy providers** (e.g. old `ai4bharat` sessions) are rejected with a clean SSE error on send/regenerate.
- **No `is_active` field on `User` model** â€” use `is_locked` for block checks (the User model uses `is_locked`, not Django's default `is_active`).

### Related files
- `backend_python/api/arena_views.py` â€” community DRF views (models, sessions CRUD, send/regenerate SSE)
- `backend_python/api/arena_urls.py` â€” URL routes mounted under `/api/neby-arena/`
- `backend_python/api/migrations/0031_arena_chat_models.py` â€” `ArenaChatSession` + `ArenaChatMessage` tables
- `backend_python/web/views_arena.py` â€” web AJAX wrappers (`/ajax/neby-arena/...`)
- `backend_python/web/views_public.py` â€” subject page passes `default_model='qwen3.8-max'`
- `backend_python/api/throttles.py` â€” `ArenaChatRateThrottle` (60/min, env-overridable via `DRF_ARENA_CHAT_THROTTLE`) and `ArenaListRateThrottle` (120/min)

---

## Real-Time WebSockets (Channels + Daphne + Cloudflare Tunnel)

The NEBians web frontend (and any future client) gets live updates â€” new posts, replies, likes, notifications, follow changes, message events â€” over a single WebSocket connection. No polling, no FCM for the web.

### Architecture
```
Browser / Mobile
   â”‚  wss://<host>/ws/
   â–¼
Cloudflare (CF edge)        â† free, proxies WS through any port
   â”‚
   â–¼
Cloudflared quick tunnel    â† ~/.local/bin/cloudflared --protocol http2 --url http://127.0.0.1:8001
   â”‚
   â–¼
Daphne (ASGI) on 127.0.0.1:8001
   â”‚
   â–¼
RealtimeConsumer (Channels)
   â”‚
   â”œâ”€â†’ Database (Postgres/MySQL) for auth + permissions
   â””â”€â†’ Redis channel layer (cross-worker fanout)
```

### Why a tunnel, not LiteSpeed proxy
**LiteSpeed + LSAPI cannot proxy WebSockets reliably.** Even when the upgrade reaches daphne (101 Switching Protocols) and daphne logs a successful `WSCONNECT`, LiteSpeed buffers the response and never returns it to the client. Tried `RewriteRule [P]` and `ProxyPass` â€” both hung the WS connection. **Use Cloudflare Tunnel instead.**

Cloudflare's free tier proxies WebSockets through any outbound HTTPS port. No firewall changes, no DNS changes (for the trycloudflare quick tunnel â€” a named tunnel requires CF-hosted DNS).

### How to start / restart
Both daphne and cloudflared auto-start via crontab `@reboot`:
```bash
@reboot /home/consicac/virtualenv/nebians_api/3.13/bin/daphne \
    -b 127.0.0.1 -p 8001 -v 2 \
    /home/consicac/nebians_api/nebians.asgi:application \
    >> /home/consicac/nebians_api/logs/daphne.log 2>&1

@reboot /usr/bin/env PATH=$HOME/.local/bin:/usr/bin:/bin \
    /home/consicac/.local/bin/cloudflared tunnel --no-autoupdate --protocol http2 \
    --url http://127.0.0.1:8001 \
    >> /home/consicac/nebians_api/logs/cloudflared.log 2>&1
```

**Manual start** (e.g. after `kill`):
```bash
cd /home/consicac/nebians_api
nohup /home/consicac/virtualenv/nebians_api/3.13/bin/daphne \
    -b 127.0.0.1 -p 8001 -v 2 nebians.asgi:application \
    >> logs/daphne.log 2>&1 & disown
nohup ~/.local/bin/cloudflared tunnel --no-autoupdate --protocol http2 \
    --url http://127.0.0.1:8001 \
    >> logs/cloudflared.log 2>&1 & disown
```

**Check status:**
```bash
pgrep -af daphne               # should show daphne running on 8001
pgrep -af cloudflared          # should show cloudflared quick tunnel
tail -20 logs/daphne.log       # WS connections, broadcasts
tail -20 logs/cloudflared.log  # trycloudflare URL is logged on first run
```

### Why `--protocol http2`
Server blocks outbound UDP (CloudLinux firewall). The default QUIC protocol fails â€” cloudflared must use HTTP/2 transport.

### The public URL is dynamic
The trycloudflare quick tunnel URL **rotates every time cloudflared starts**. The deployed code handles this automatically:
- `web/views.py::_get_ws_public_url()` reads `WS_PUBLIC_URL` env var if set
- Otherwise it scrapes `logs/cloudflared.log` for the latest `https://<random>.trycloudflare.com` line and converts to `wss://<random>.trycloudflare.com/ws/`
- The URL is injected into every page as `window.WS_CONFIG.url` via `web/templates/base.html`
- The JS client (`realtime.js`) reads from `window.WS_CONFIG.url` first, falls back to deriving from `window.location`

**For a stable URL** (no rotation), set up a named Cloudflare Tunnel (free):
1. Move `nebians.consica.com.np` DNS to Cloudflare
2. `cloudflared tunnel login`
3. `cloudflared tunnel create nebians-ws`
4. Create `~/.cloudflared/config.yml`:
   ```yaml
   tunnel: nebians-ws
   credentials-file: /home/consicac/.cloudflared/<UUID>.json
   ingress:
     - hostname: ws.nebians.consica.com.np
       service: http://127.0.0.1:8001
     - service: http_status:404
   ```
5. Add CNAME in Cloudflare DNS: `ws` â†’ `<UUID>.cfargotunnel.com` (proxied)
6. Set env var: `WS_PUBLIC_URL=wss://ws.nebians.consica.com.np/ws/` in `nebians_api/.env`
7. Restart cloudflared with: `cloudflared --config ~/.cloudflared/config.yml tunnel run nebians-ws`

### Trycloudflare wildcard via middleware rewrite
A trycloudflare URL looks like `https://abc123.trycloudflare.com` â€” different every restart. Django's `ALLOWED_HOSTS` check would reject these. Fix: `nebians.middleware.AllowedHostMiddleware` runs BEFORE `CommonMiddleware` and rewrites `HTTP_HOST` to `nebians.consica.com.np` when the request comes through a trycloudflare subdomain. This way:
- `ALLOWED_HOSTS` stays strict
- CSRF cookie uses the canonical origin
- URL reversal works correctly
- The middleware also sets `ALLOWED_HOSTS_GLOB` / `ALLOWED_HOST_SUFFIXES` from env vars for custom domains

### Files added
- `nebians/asgi.py` â€” `ProtocolTypeRouter` combining `django_asgi_app` (HTTP) and `websocket` (WS)
- `api/routing_ws.py` â€” single route `^ws/?$` â†’ `RealtimeConsumer`
- `api/consumers_ws.py` â€” `RealtimeConsumer` (auth, heartbeat, batching, permission checks, rate limiting)
- `api/middleware_ws.py` â€” `JWTAuthMiddleware` (Bearer token auth for WS) + `OriginValidatorMiddleware`
- `api/realtime.py` â€” broadcast helpers: `broadcast_post_created/updated/deleted/like_changed`, `broadcast_reply_*`, `broadcast_notification`, `broadcast_follow_changed`, `broadcast_unread_count`, `get_health_snapshot`

### Files modified
- `nebians/settings.py` â€” `INSTALLED_APPS += ['daphne', 'channels']`; `ASGI_APPLICATION = 'nebians.asgi.application'`; `CHANNEL_LAYERS` (Redis or InMemory); `ALLOWED_HOSTS_GLOB` + `ALLOWED_HOST_SUFFIXES` env support
- `nebians/middleware.py` â€” added `AllowedHostMiddleware` (trycloudflare host rewriting)
- `api/services.py`, `api/views.py`, `api/notifications.py`, `api/neby.py` â€” broadcast calls on create/update/delete/like/follow/notification triggers
- `web/views.py` â€” `_get_ws_public_url()` helper; `ws_url` in `_ctx()` for all templates
- `web/templates/base.html` â€” `<body data-ws-url=...>` + `<script>window.WS_CONFIG = ...</script>` + `<script src="/static/web/js/realtime.js">` + `showNotifToast` JS
- `web/templates/web/forum_post.html`, `forum.html`, `home.html`, `notifications.html`, `library.html`, `profile.html` â€” WS subscriptions + live DOM updates
- `web/static/web/js/realtime.js` â€” WS client (auto-reconnect, heartbeat, tab-visibility, polling fallback, wildcard event dispatch, optimistic-update dedup)
- `web/static/web/css/app.css` â€” `.toastIn` animation, `.ws-state-dot` styles
- `requirements.txt` â€” `channels==4.2.0`, `channels-redis==4.2.1`, `daphne==4.1.2`, `websockets>=12` (test only)

### Wire format
**Client â†’ Server** (JSON over WS):
```json
{ "action": "subscribe", "channel": "forum.public" }
{ "action": "subscribe", "channel": "forum.post.<id>" }
{ "action": "unsubscribe", "channel": "forum.public" }
{ "action": "ping" }
{ "action": "mark_read", "notification_id": 123 }
```

**Server â†’ Client** (JSON over WS):
```json
{ "type": "ready", "user_id": "...", "server_time": 1780549377388, "heartbeat_interval": 25 }
{ "type": "subscribed", "channel": "forum.public" }
{ "type": "unsubscribed", "channel": "forum.public" }
{ "type": "pong" }
{ "type": "event", "channel": "user", "event": "notification.created", "data": { ... } }
{ "type": "event", "channel": "forum.public", "event": "post.like_changed", "data": { "post_id": "...", "thumbs_up_count": 12, "isThumbedUp": true } }
{ "type": "error", "code": "rate_limited", "message": "..." }
```

### Channel names
| Channel | Who can subscribe | Events |
|---|---|---|
| `user` | Only the authenticated user (auto-subscribed on connect) | `notification.created`, `unread_count.changed`, `account.updated` |
| `forum.public` | Anyone | `post.created`, `post.updated`, `post.deleted`, `post.like_changed` |
| `forum.post.<id>` | Anyone | `reply.created`, `reply.updated`, `reply.deleted`, `reply.like_changed` |
| `user.<id>.profile` | Authenticated (own only) | `follow.changed`, `profile.updated` |
| `admin` | Staff only (auto-checked) | `report.created`, `user.locked`, `user.unlocked` |

### Auth flow
- Browser sends session cookie via standard `AuthMiddlewareStack` (Django Channels)
- Mobile / external clients send `Authorization: Bearer <auth_token>` â€” handled by `JWTAuthMiddleware` which sits **inside** `AuthMiddlewareStack` so session auth runs first
- Token is resolved via `User.objects.get(auth_token=token)` (NOT `UserAuthToken` which stores a hash) â€” see **AGENTS.md Â§ Auth token cache invalidation**
- Locked users (`is_locked=True`) and bot users (`is_bot=True`) are rejected with `websocket.close(4401)` (custom code) at connect time
- After auth, the user's own `user` channel is auto-subscribed (no need to send a subscribe message)
- For staff users, the `admin` channel is auto-subscribed

### Client behavior (`realtime.js`)
- **Auto-reconnect** with exponential backoff: 1s â†’ 2s â†’ 4s â†’ 8s â†’ 16s (capped at 30s)
- **Heartbeat** every 25s â€” sends `{"action":"ping"}`, expects `{"type":"pong"}` within 5s, otherwise reconnects
- **Tab visibility** â€” pauses heartbeat when tab is hidden for >5 min, reconnects on focus
- **Polling fallback** â€” if WS doesn't connect within 6s, falls back to 60s polling for unread count
- **Batched events** â€” server flushes events every 50ms (so a reply + 3 likes arrive as one `event` packet)
- **Optimistic-update dedup** â€” DOM updates optimistically on user action; ignores WS events for the same `client_request_id` to avoid double-rendering
- **Per-channel permission** â€” server checks permissions per subscribe (e.g. user 123 can't subscribe to `user.456.profile`)

### Performance
- **Server-side per-message size limit:** 4 KB
- **Server-side per-connection rate limit:** 30 messages / 10s (configurable)
- **Server-side per-user cap:** 5 concurrent connections
- **Server-side idle timeout:** 5 min (heartbeat must be received)
- **Event batching:** 50ms window
- **Per-channel permission check** in `database_sync_to_async` to avoid blocking the event loop
- **Lazy group subscribe** â€” clients only join Redis groups they actually subscribe to (not the whole world)

### Gotchas
- **WS field name is `action`, not `type`** â€” the client sends `{"action": "subscribe", ...}`; the server checks `msg.get('action')`
- **Origin validation** â€” `OriginValidatorMiddleware` validates the `Origin` header against `nebians.consica.com.np` and `localhost:8000` (dev). Mismatch â†’ `websocket.close(1008)`. CF tunnel adds the `Origin: https://nebians.consica.com.np` automatically since the client connects to nebians.consica.com.np first.
- **CSRF** â€” WS auth bypasses CSRF (no `csrf_exempt` needed) because Channels has its own middleware stack. The session cookie is validated server-side.
- **Static files for `realtime.js`** â€” remember to copy `realtime.js` to `public/static/web/js/` after editing (see "Static Files Deployment" above)
- **If daphne is down** â€” the client falls back to polling after 6s. No data loss because the unread-count endpoint still works via HTTP.
- **If cloudflared is down** â€” WS doesn't work at all (no public path to daphne). The page still loads via LiteSpeed, just no live updates.

### Production checklist
- [x] daphne running on 127.0.0.1:8001
- [x] cloudflared running with `--protocol http2 --url http://127.0.0.1:8001`
- [x] @reboot cron entries for both
- [x] Redis channel layer configured (shares Redis used for cache)
- [x] `database_sync_to_async` imported in `middleware_ws.py` (was missing in dev â€” caused 403 on bearer auth)
- [x] AllowedHostMiddleware deployed (handles trycloudflare wildcard)
- [x] window.WS_CONFIG.url injected in base.html
- [x] realtime.js copied to public/static/web/js/
- [x] **Decided to stay on trycloudflare** (named tunnel deferred â€” requires registrar/partner action at babal.host)

---

## Continuity Notes

### What Was Worked On (Current Session)
**Anonymous-content privacy + avatar-contrast fixes (deployed + verified live)**

**Bug 1 — anonymous posts/replies leaked onto identity surfaces:** anonymous content was only anonymized at serialization time, so it leaked back: profile posts/replies tabs (`web/views_profile.py` `profile()` at :199/:202, `ajax_profile_activity` :773/:776, `ajax_profile_replies` :808/:811) listed the owner's anonymous posts and replies for EVERY visitor; `ajax_instant_search` (`web/views_public.py:622`) returned the real username for anonymous posts (DB fallback too); the Meilisearch index `api/search.py:88 _serialize_post` stored and searchable'd the real username; profile-stats counts inflated with anonymous activity. **Fix (commit `5643e9f`):** added `is_anonymous=False` filters everywhere (profile listings, both ajax paginators + total_count, instant search meili + DB fallback, main search meili + DB fallback), `_serialize_post` stores empty username + `is_anonymous` for anon and `sync_posts` skips them, `search_posts` adds `is_anonymous = false` + filterable attr; `api/views_users.py::user_profile_stats` post/reply counts exclude anon; `web/views_ajax.py::ajax_user_popup` counts exclude anon; `web/view_helpers.py::_build_local_stats(user, exclude_anonymous=False)` new param (True at profile() and profile_achievements()). Decision: hide anon content from ALL viewers incl. owner; exclude anon posts from search entirely; denormalized counters/leaderboard/contribution_score left unchanged (separate product decision); study-lab analytics (:2185-2186) is owner-only → untouched. Tests: `web/test_anonymous_privacy.py` (9 tests). **NOTE: Meilisearch is NOT configured in production** (`MEILISEARCH_URL` empty in .env/settings) — the live path is the DB fallback, which is fixed; `sync_search_index` reports "not configured" and nothing needs syncing. Serialization already hid author id ('' / "Anonymous Nebian") — those paths were safe.

**Bug 2 — custom avatar bg color made the face invisible:** `api/blobatar/render.py::resolve` and `web/static/web/js/blobatar.js::resolveOpts` applied palette overrides (color/bgcolor/eyecolor query params) WITHOUT re-enforcing the contrast floors, so a blue background circle (`bgcolor=%230000ff`) + hue-derived light-blue head (#85cdff at hue 240) rendered blue-on-blue. Default bg plate is near-white for all hues (bg L=0.965; hue 240 → #eef5fa). **Fix (commit `e32e606`):** added `_FLOORS = (("head","bg",1.25),("eye","head",4.5))`; after `merged.update(overrides)`, re-run floors via `ensure_contrast` in both render.py and blobatar.js (line 735 server/local). AVATAR_CACHE = `public, max-age=86400, stale-while-revalidate=2592000` — stale SVGs refresh within a day.

**Verified live:** avatar `?bgcolor=%230000ff&anim=bob` → head now #cf1746, contrast 1.581 ≥ 1.25; profile `/profile/prashantchataut/` cache-busted → anon post "Question Paper of first terminal examination, Grade XII" GONE, visible posts present (a plain request hit a STALE Cloudflare/CDN cache page — cache-bust with `?t=<ms>` shows the fix; CF revalidates on next pass); `/ajax/search/?q=Question Paper of first terminal` → only the resource result, no anon post, no username leak. Server files match local (md5 identical for blobatar.js; grep confirms is_anonymous=False counts). Full suite 37 tests OK (`api.test_avatar_use_pp` + `web.test_avatar_session` + `web.test_anonymous_privacy` + `api.test_background_agent`), `manage.py check` clean, `node --check blobatar.js` clean. Deployed via scratch/deploy.ps1. Git: local == origin at `91835f0`.

**Bug 3 — blue letter-fallback circle showed through transparent avatar SVGs (commit `91835f0`, deployed + verified live):** the blobatar SVG has a transparent plate by default (`api/blobatar/styles.py:260 background=False`), and every avatar container that paints `--md-primary`/`--md-primary-container` (topbar `.avatar-ring`, dropdown `.profile-dropdown-avatar`, forum/comment threads `.fp-*avatar`, news `.comment-avatar`, post cards `.post-card-avatar`/`.act-avatar`, follow menus `.profile-avatar`, search `.user-search-avatar`, study spaces `.ss-member-avatar`, leaderboard `.contributor-avatar-container`, attribution/mention `.behalf-*`/`.mention-result-avatar`, resource cards `.suggest-post-avatar`/`.resource-card-avatar`) was designed as a blue circle for the LETTER fallback only — so the blue leaked behind every avatar image, and in dark mode the light-blue circle (`--md-primary` #B4C5FF) made some heads nearly invisible. **Fix:** new CSS module `web/static/web/css/app/11-avatar-image-backgrounds.css` gives every avatar `<img>` `background: var(--md-surface-container-lowest, #fff)` (white in light, near-black #060F1B in dark) so avatars float on a surface disc; letter fallbacks keep the blue container circle. Imported from `app.css`. No Python changes. Verified: module file served 200 after LSAPI respawn (WhiteNoise stale-index gotcha — `rm -rf tmp/* && touch tmp/restart.txt` + 45s wait), forum + post-detail pages' avatar containers all covered. **Follow-up (commit `dfcfebe`):** the surface disc alone read as invisible against the page surface, so the same module now strokes every avatar container holding an image with `border: 1.5px solid var(--md-outline)` (via `:has(img)` — overrides the old letter-fallback border on `.post-card-avatar`/`.contributor-avatar-container` so all circles match). `.fp-thread-avatar` stacks keep their own overlap separator border; `.pf-avatar-circle` keeps its 4px photo ring; the Neby 3D avatar keeps its brand blue. Verified: served module md5 == local, 18 `:has(img)` selectors live.

### Previous Session (session-clobber hotfix)
**Session-clobber hotfix (production bug): homepage redirecting to edit_profile with empty fields**

**Root cause:** `web/views_avatar.py` `ajax_avatar_change_username`/`ajax_avatar_customize` replaced the ENTIRE session `user_data` dict with `_session_user_dict(db_user)` (avatar-only: username/photo_url/avatar_*; no email/gender/class_level/school/bio/dob). Homepage `web/views_public.py:60-65` redirects to edit_profile when the session dict lacks display_name/gender/class_level; the edit form fills from the session dict → fields appeared empty. **DB data was never touched** (verified server-side: no users with empty display_name/gender/class_level; nikithamal row intact). Trigger: any avatar customize/username save while logged in (e.g. toggling "Use avatar everywhere").

**Fix (commit `9f2a0fe`, pushed + deployed):** (1) both endpoints now MERGE `_session_user_dict(db_user)` into the existing session dict (`user_data = dict(api.get_session_user(request) or {}); user_data.update(...)`) instead of replacing; (2) `web/api_client.py::get_session_user` self-heals already-clobbered sessions — if `user_data` is a dict lacking the `'gender'` key, it resolves the user via `get_user_by_auth_token` (api/security.py:107) and rebuilds with `_normalize_user_data(UserSerializer(user).data)` + session write-back (lazy imports inside the function to avoid api_client↔view_helpers circular import). New tests: `web/test_avatar_session.py` (3 tests; combined suite api.test_avatar_use_pp + web.test_avatar_session + api.test_background_agent = 28 tests OK). Note: `auth_token` is stored HASHED — tests/sessions use the RAW token; the heal swallows exceptions and returns the stale dict on failure. Do NOT submit the stale empty edit_profile form (bio/school_username have no DB fallback in `web/views_profile.py:919` — would clear them).

### Previous Session (avatar feature)
**"Use avatar instead of profile photo" everywhere (web) — deployed + verified + pushed**

Feature: `User.avatar_use_pp` flag (BooleanField, migration `0115_avatar_use_pp`) â€” when ON, the generated blobatar (incl. `?anim=`) replaces the uploaded profile photo EVERYWHERE on the web: topbar, forum posts/replies, news comments, contributors/leaderboard, search, resources, study lab, profile page. Web-only; the toggle exists only on my_avatar (`web/templates/web/my_avatar.html` "Use avatar everywhere" checkbox â†’ POST `/ajax/avatar/customize/` with `use_pp`; enabling with no stored anim sends `anim='bob'`). Android gets the avatar URL through the normal API when the flag is on (acceptable â€” no web toggle for Android users to flip).

Implementation: `_avatar_url(u)` chokepoint (`web/view_helpers.py`) â†’ ORM users via `avatar_or_photo_url()` (`api/services.py`); dict users with `avatar_use_pp` â†’ `_blobatar_url_for`; then photo; then blobatar. `_ctx()` topbar + `_normalize_user_data` handle the flag. `api/notifications.py` actor_photo_url and `api/serializers.py` FollowSerializer/EditHistorySerializer use `avatar_or_photo_url` via **lazy function-level import** (`from .services import avatar_or_photo_url` inside the function) â€” `api/services.py` imports `api.notifications` at module level (line 19), so a top-level services import in notifications/serializers causes a circular import. Also added `eyecolor` to the dict branch of `_avatar_prefs_from`. New test file: `api/test_avatar_use_pp.py` (7 tests). Pushed as `c077761` (+ Android LinkifyText fix `f5eb874`, rebased on top of merged PRs #33-#38, origin main now `f5eb874`).

**Deployed + verified live:** avatar endpoint `?anim=bob` â†’ 200 svg; `_avatar_url` returns blobatar URL with flag on, photo with flag off; e2e: flag on for `prashantchataut` â†’ home + forum render `src="/avatar/prashantchataut/"` (flag restored after). **Migration history surgery done on the server** (see CRITICAL note below).

**CRITICAL â€” migration chain is now LINEAR 0113â†’0114â†’0115 (do NOT reorder):** During the AI4Bharat-removal deploy, `migrate` failed with `InconsistentMigrationHistory` because the UNCOMMITTED local `0114_botconfig_fallback_chain.py` depended on `0115_avatar_use_pp` while the server already had 0114 applied and 0115 not. Fixed by rewiring: `0114_botconfig_fallback_chain.py` depends on `0113_avatar_eye_color`, `0115_avatar_use_pp.py` depends on `0114`. Server history now `...0113, 0114, 0115` â€” all applied. Both 0114 (fallback_chain field) and 0115 (avatar_use_pp) are deployed and live. If you ever re-run `migrate` on a fresh DB, apply in order 0113 â†’ 0114 â†’ 0115. The only remaining "drift" is a harmless index rename (`makemigrations --check` wants `0116_rename_ai_fb_surf_created_idx_...`) which is intentionally not generated â€” `migrate` itself is clean.

**SSH/deploy gotchas learned this session:**
- Key JSON property is `ssh_private_key` (NOT `private_key`). Re-extract to a NEW temp filename each time (old key file becomes read-only from `icacls /inheritance:r`; grant `:RW` to current user after creating).
- `scp` silently fails sometimes (sftp subsystem starts but no transfer); fall back to `echo <base64> | base64 -d > file` over ssh.
- Piping scripts to `ssh ... "bash -s"` mangles heredocs (CRLF + heredoc-in-`$()` from stdin). **Reliable pattern: scp script to /tmp, then `ssh host "tr -d '\r' < /tmp/script.sh | bash"`** â€” the `tr -d '\r'` is mandatory.
- PowerShell pipes into ssh can also append stray `\r` to lines even after `-replace "`r`n","`n"` â€” always use the scp+tr pattern for anything with heredocs.

**Git state:** local main == origin main (`f5eb874`), clean of my changes. Uncommitted WIP (untouched, per user): `api/ai4bharat_proxy.py` (deleted), `api/background_agent/runner.py`, `api/llm/registry.py`, `api/llm/runtime.py`, `api/neby.py`, `web/templates/admin_panel/bot_edit.html` + `bot_config.html`, `web/views_admin.py`, `api/metaai_proxy.py` (untracked), `api/migrations/0114_botconfig_fallback_chain.py` (untracked, deps 0113), `neby_cli/` (untracked), arena_* views/urls, coding_agent/*, qwen_utils/client.py, throttles.py, api/urls.py, subject_page.html, views_arena/views_public/views_study_lab, docs/*, ApiService.kt, AGENTS.md (these notes), `.agnes` cache deletion. All 5 PRs (#33-#38) merged to main. PR #37's `benchmark_poll_creation.py` lives at repo root (cosmetic inconsistency vs `backend_python/benchmarks/`).

### Previous Session
**Reusable AI widgets + live streaming for the background agent**

**Shared widget library:** new `web/static/web/js/ai-widgets.js` + `web/static/web/css/ai-widgets.css` expose `window.AIWidgets` (each widget returns `{ el, destroy, ... }` and carries `.ai-widget` token vars with fallbacks so they render inside Neby chat, the background agent panel, or any future AI UI):
- `AIWidgets.PixelLoader.create({label, variant: 'drive'|'dots'|'orbit', timer})` â†’ `{el, setLabel, destroy}` â€” 3Ã—3 pixel grid + shimmer label + elapsed timer
- `AIWidgets.Trace.create(opts)` â†’ `{el, settle, setRows, destroy}` â€” ThinkingState port (steps/reasoning/search/coding variants, expandable rail). `setRows(rows)` re-renders rows live while still working (added for BA live thought streaming). Rows container honors `--ai-rows-max` (scroll cap, thin scrollbar) so long reasoning lists scroll instead of growing forever.
- `AIWidgets.StreamingText.create({text, wordMs, sources, citeAfter, actions, onCopy/onRetry/onVote, onDone})` â€” word-by-word blur resolve (55ms/word), inline citation chips, copy/retry/up/down action row, expandable sources panel. NO follow-up suggestions (per user).
- `AIWidgets.streamSSE(url, {method, body, headers, credentials, onText, onThought, onEvent, onDone, onError})` â†’ `{abort}` â€” fetch + ReadableStream SSE reader (avatar-lab technique); now accepts POST/FormData for admin chat
- `AIWidgets.ApprovalCard.create({questions: [{q, type:'radio'|'check', options, allowCustom}], title, subtitle, onSubmit(answers, custom), onDismiss})` â†’ `{el, destroy, open, close, reset, sent}` â€” vanilla port of the React ApprovalCard (pager dots, prev/next, send arrow disabled until answered, radio auto-advance 480ms, custom "Otherâ€¦" input, sent state with "Start over", dismiss â†’ "Open approval" pill, Material Symbols icons)
- `AIWidgets.actionRow({text, onCopy, onRetry, onVote})` â†’ actions element (shared with StreamingText via internal `buildActions`; copy works by default, up/down flash `.ai-stream-action-on` and call `onVote(1|-1)`)
- `AIWidgets.ToolChips.create({rows: [{icon:'think'|'write'|'run'|'read', label, chip, mono, detailMono, detail: [{text, tone:'add'}], error}], diffs: [{file, add, del}], more, header: {calls, messages}, reveal: 'stagger'|'instant', stepMs})` â†’ `{el, destroy, addRow, addRows, setDiffs, setHeader, open, close, toggle, revealAll}` â€” vanilla port of the React ToolChips: collapsible run header ("N tool calls, M messages"), staggered row reveal (700ms), hover reveals chevron, rows expand to detail lines (green `+` add tone, mono), file-diff chips pop in at the end (+adds/âˆ’dels, "+N more" button). Token colors via `--ai-*` (adds `--ai-green`/`--ai-red` fallbacks).

**Neby assistant refactor:** `neby-assist.js` now consumes `AIWidgets` (loader + trace); `neby-trace.js` deleted; `base.html` loads `ai-widgets.js`+`ai-widgets.css` (L95/L869); old `.neby-pixel-*`/`.neby-trace-*` CSS removed from `neby-assist.css`; chat-area gap 12pxâ†’16px (4px more between messages); cloud `chat` replies render through `AIWidgets.StreamingText` (â‰¥40 chars).

**Backend streaming (`api/llm/client.py`):** `chat_stream()` generator â€” same validation as `chat()`, yields `{'type':'reasoning'|'text'|'done', ...}` deltas for OpenAI-compat (incl. `reasoning_content`), Anthropic (incl. `thinking_delta`), Gemini (`streamGenerateContent?alt=sse`). `api/llm/runtime.py::call_session_provider_stream()` wraps it for sessions.

**Runner live streaming (`api/background_agent/runner.py`):** official providers now call `_call_official_provider_stream()` â€” publishes every delta to Redis pub/sub channel `ba:stream:<session_id>` (frames `kind=thought|text|done|error`, `fatal:true` on terminal failure; retry errors are non-fatal). Fully best-effort: no Redis â†’ call still completes, UI falls back to polling. Redis URL: `BACKGROUND_AGENT_STREAM_REDIS` env or `CACHE_LOCATION`, else localhost:6379.

**SSE endpoint (`web/views_background_agent.py`):** `background_agent_session_stream` at `backgroundagent/api/sessions/<id>/stream/` (session-cookie auth, same as events). First frame is a `snapshot` (events since `?after=` â€” same shape as events endpoint) for reconnect catch-up; then relays pub/sub frames as `data: {json}`; `: ping` keepalive every 15s; closes on `fatal` error, or when the session leaves running/queued/preparing (checked on `done` + every 10s), or after 1h cap. No Redis â†’ sends `close` immediately.

**BA frontend (`background-agent-session.js`):** opens the SSE stream when session is active (reopens with 2.5s backoff on disconnect while active, stops when inactive). `thought`/`text` deltas render into live nodes (`.ba-thought.live` + `.ba-message.assistant.live` with blinking `.ba-live-cursor`), throttled markdown re-render every 140ms; on `done`/`end`/fatal the live nodes are swapped for the durable DB rows via `loadDetail()` (polling at 2.5s stays as the sync/fallback layer). `session.html` got `data-stream-url` + ai-widgets includes; `background_agent/base.html` loads ai-widgets.css.

**User directives:** loader grid + text side-by-side (row), label ellipsis, NO avatar icon / NO bubble bg on Neby AI messages, AI messages full width, loader uses **drive** variant (not orbit), reusable components also applied in background agent, **no suggested replies/follow-ups** in the streaming widget.

**Admin AI chat (`admin_panel/chat.html` + `views_admin_chat.py`):** now consumes `AIWidgets` â€” `PixelLoader` ("Waiting for response", drive variant, elapsed timer) inside the assistant bubble until the first token, `AIWidgets.streamSSE` (POST + FormData + `X-CSRFToken`) replaces the hand-rolled reader, and `AIWidgets.actionRow` (copy/retry/up/down) is appended on completion. Retry re-sends the same query; up/down POST to the new feedback endpoint. Includes `ai-widgets.js` + `ai-widgets.css`. Live chunk-by-chunk text rendering is kept (it's a provider test tool â€” word-blur would hide streaming latency).

**Action buttons + feedback endpoint:** new `POST /ajax/ai-feedback/` (`web/views_ajax.py::ajax_ai_feedback`) stores `AiFeedback` rows (`api/models.py` + migration `0108_ai_feedback.py` â€” `user_id` is a plain CharField, NO FK to users, so no charset-mismatch table pain; rate-limited 30/min). StreamingText actions now actually work: Neby cloud replies (`neby-assist.js::appendStreamingAi`) wire `onRetry` â†’ `runQuery(lastQuery)` and `onVote` â†’ `/ajax/ai-feedback/` with `surface:'neby'`; admin chat uses `surface:'admin-chat'` + provider/model. Copy works by default (clipboard).

**Bug fix:** `.ai-stream-actions { display: flex }` was overriding the `hidden` attribute â€” action rows were visible during streaming everywhere. Fixed with `.ai-stream-actions[hidden] { display: none; }` in ai-widgets.css (same fix applied to `.ai-chips-diffs[hidden]`).

**BA tool calls â†’ ToolChips (`background-agent-session.js`):** the bulky per-tool `<details class="ba-tool-event">` bubbles in the conversation are replaced by grouped `AIWidgets.ToolChips` runs (`reveal:'instant'`, `.ba-message.tool-group` wrapper, max-width 20rem, token-mapped to `--ba-*` vars incl. `--ai-green/--ai-red` â†’ `--ba-success/--ba-danger`). Run lifecycle: an assistant text (non-thought) message closes the previous run and flags the next tool group as a new run (header "N tool calls, 1 message"); tool rows map via TOOL_VERBS (mirror of `labels.py::TOOL_VERBS`) + `meta.args` (icon: think/write/run/read; chip: file basename / command / query; detail: writeâ†’`+` content lines (green), readâ†’file lines, run_commandâ†’stdout+exit, error rows red "failed â€” â€¦"); file-diff chips at run end from `runFiles` (writeâ†’line count, deleteâ†’del). `endRun()` also fires on user messages, terminal events (`session.completed/failed/cancelled`) and when the session leaves active status. Full tool results remain viewable in the Files/Diff review tabs. `.ba-tool-event`/`.ba-message.tool` CSS removed.

**BA thought cards â†’ Trace:** the old `<details class="ba-thought">` reasoning cards (durable "Thought for N seconds" + live "Thinkingâ€¦") are replaced by `AIWidgets.Trace` (variant 'reasoning') inside `.ba-trace-wrap` (margin 2px 0 8px 36px, token-mapped to `--ba-*` incl. `--ai-rows-max: 340px` for the scroll-capped rows). Durable cards create with `settleDelay: 0` + immediate `trace.settle(label)`; the live node uses `settleDelay: 86400000` (never auto-settles) and feeds rows via the new `setRows()` every throttled render (content split into non-empty lines via `thoughtRows()`). Both have a plain-text fallback if `window.AIWidgets` is missing. `.ba-thought*` CSS removed; `psychology`/`chevron_right` icons gone from the conversation.

**Status:** all `node --check` + `py_compile` + `manage.py check` pass. **Not committed / not deployed** â€” user hasn't given the go-ahead.

### Previous Session
**Needle 2 on-device assistant ("Neby Local") â€” persisted runtime + Android**

DECISION RECORD (2026-08-13): An earlier v3 attempt (IDB asset caching only â€”
commit 57e91be on main) was **reverted** (`git reset main 830f2f0` + force-push)
in favor of this snapshot-based implementation on branch `arena/019ffa43-neb`
(commit f5e559c). Snapshot restore is 49 ms vs v3's ~3.9 s (which still
recompiled the tool grammar every refresh). Live server re-deployed to match.
Notable gap vs v3: no AbortController fetch timeout/retry and no 90 s load
watchdog in neby-assist.js â€” port over if load hangs ever recur.

The 45M-parameter Needle 2 integration uses the official CQ2 model and WASM
engine. The web model remains 13.10 MiB; Android packages only 0.375 MiB of
engine/glue/license/bootstrap assets and downloads the model after explicit
user opt-in.

**Runtime optimization:** `web/static/web/js/needle2/needle.worker.js` now saves
the initialized 32.63 MiB WASM heap in versioned, tool-schema-keyed 2 MiB
IndexedDB chunks. A repeat launch restores it instead of loading the model and
recompiling the tool grammar. Corrupt/missing/quota-rejected snapshots fall back
to cold init. Keep `RUNTIME_VERSION`, web cact URL, Android expected size/hash,
and Android `snapshotNamespace` in sync whenever the model changes.

**Measured on the sandbox (Node 22):** cold load+tool init 5.12 s; snapshot
restore including disk read 49 ms (99.0% reduction); restored semantic output
7/7 identical; expected route and key arguments 7/7; decode avg/p50/p95
819/727/1,529 ms. Full reproducible output is under `backend_python/benchmarks/`.
The previous synthetic warmup was removed because it added about 1.1 s without
improving first-query decode.

**Web:** progress distinguishes download, model load, tool preparation, and
snapshot restore. The assistant displays Needle reasoning/confidence/device
latency when the engine emits a trace and handles every returned tool call.
Slow/save-data connections do not auto-download during idle preload.

**Android:** Settings â†’ Neby Local opens a dedicated Compose chat/setup screen.
`NeedleModelManager` provides resumable SHA-256-verified cloud download into
`noBackupFilesDir`; `NeedleWebRuntime` runs the same exact engine in a locked
local WebView worker; chat and compact reasoning persist offline; users can
pause setup, clear chat, or remove model/runtime. The `.cact` is never in the
APK.

**Deploy note:** deploy backend/static files normally. The Android model URL
currently points to the deployed web cact and verifies size 13,737,679 bytes and
SHA-256 `ca7950ac8aef26ed22d17f92c733c9374aa7f59f6c2abb0fe2ac320a04f3c3d8`.
After replacing the model, follow `backend_python/docs/NEEDLE_FINETUNE_PLAN.md`.

### Previous Session
**Blog comment system (web + backend) + Android UI cleanup (library/forum/news screens)**

**Blog Comment System (Web):**
- Added `BlogComment` model in `api/models.py` â€” links to `Announcement` + `User`, stores text/created_at
- Migration `0080_blog_comment_model.py` creates `blog_comments` table
- `web/views_news.py`: `news_detail()` now serializes comments via `_serialize_comments()`; added `ajax_blog_comment` POST endpoint (auth-only)
- `web/urls.py`: added `/ajax/news/comment/` route
- `web/templates/web/news_detail.html`: complete rewrite â€” removed content card wrapper, removed markdown rendering, added 3-dot bottom sheet menu (share/bookmark/report), share at bottom, comment section with AJAX submission (`fetch()` + `showSnackbar()`), `escapeHtml()` sanitization

**Android UI Changes:**
- **LibraryScreen:** Removed upload FAB icon, removed "Digital Library" headline title
- **ForumScreen:** Removed category chips below topbar, added filter icon button in topbar
- **NewsScreen:** Removed results/practice CTA button, removed topbar entirely, added back navigation with `ArrowBack` icon
- **NewsDetailScreen:** Removed topbar, added 3-dot `MoreVert` overflow menu with Share/Bookmark/Report options, removed content card wrapper, removed markdown, share button at bottom, comment section UI (avatar + input + list)

**Files modified (Android):**
- `app/.../Navigation.kt` â€” router updates for NewsScreen/NewsDetailScreen
- `app/.../LibraryScreen.kt` â€” removed icon + title
- `app/.../ForumScreen.kt` â€” removed chips, added filter icon
- `app/.../NewsScreen.kt` â€” removed topbar/CTA, added back nav
- `app/.../NewsDetailScreen.kt` â€” 3-dot menu, share bottom, comments

**Files modified (Web):**
- `api/models.py` â€” added `BlogComment` model
- `api/migrations/0080_blog_comment_model.py` â€” new migration
- `web/views_news.py` â€” comment serialization + AJAX endpoint
- `web/urls.py` â€” comment route
- `web/templates/web/news_detail.html` â€” full rewrite

**Not deployed yet.**

### Previous Session
**Async AI Generation with Job Queue + Live Progress** (NEXT_LEVEL_IDEAS.md point #5)

**Problem:** Generation endpoints (summary, mindmap, quiz, flashcards) block an LSAPI worker for up to 2Ã—120s. Under public load this is the #1 scaling bottleneck.

**Architecture:**
- `GenerationJob` model (`api/models.py`) â€” DB-backed job queue with statuses: queued â†’ processing â†’ completed/failed/cancelled
- `api/generation.py` â€” enqueue, get_job, serialize_job, mark_* helpers, WS broadcast on status changes
- `api/generation_executors.py` â€” per-type handlers (summary, mindmap, quiz, flashcard) extracted from `views_study_lab.py`
- `api/management/commands/run_generation_worker.py` â€” daemon that polls for pending jobs and processes them
- `api/realtime.py` â€” added `broadcast_generation_event()` for WS push on studyspace channel
- Views return HTTP 202 with `jobId` when worker is alive, fall back to synchronous processing when no worker is detected
- Frontend (`study-space.js`) polls `GET /ajax/study-space/generation/<jobId>/` for status updates, shows progress text during generation

**New files:**
- `api/generation.py` â€” job queue module (enqueue, status, broadcast)
- `api/generation_executors.py` â€” per-type generation handlers
- `api/management/commands/run_generation_worker.py` â€” background daemon
- `api/migrations/0061_generation_job.py` â€” GenerationJob model

**Modified files:**
- `api/models.py` â€” added `GenerationJob` model
- `api/realtime.py` â€” added `broadcast_generation_event()`
- `web/views_study_lab.py` â€” 4 generation views now use `_enqueue_or_process()`, added `ajax_generation_status` and `_job_result` helpers
- `web/urls.py` â€” added `/ajax/study-space/generation/<job_id>/` route
- `web/static/web/js/study-space.js` â€” added `pollGenerationJob()`, `cancelAllGenerationPolls()`, `handleSummaryResult()`, `handleMindmapResult()`, `handleQuizResult()`, `handleFlashcardResult()`; all 4 generation functions now handle async 202 responses

**Worker deployment:** Run `python manage.py run_generation_worker` as a background process (cron `@reboot` or systemd). If no worker is running, views process synchronously (backward compatible).

**Not deployed yet.**

### Previous Session (Earlier)
**Fixed double teacher/institution badge + added role-themed profile banners ("TUTOR" and "NEBIAN") + better teacher icon**

**Problem 1 â€” Double badge:** `badge_info` (from `_user_badge_info`) already returns a role badge for teacher/institution/explorer (added last session), but `profile.html` had a duplicate `{% if profile_user.role == 'teacher' %}` block that added a second badge next to the username.

**Problem 2 â€” Better teacher icon:** `person_book` looked like a generic "person" icon. Switched to `history_edu` (scholar with graduation cap) â€” semantically closer to "teacher".

**Problem 3 â€” Role-themed banners:** Teachers and institutions got the default blue "nebian" banner, which didn't match their identity. Added two new role-themed banner presets.

**Changes:**

**`web/templates/web/profile.html` (line 75-83):**
- Removed the duplicate `{% if profile_user.role == 'teacher' %}` / `institution` / `explorer` block (13 lines)
- Now only the dynamic `badge_info` block renders the badge

**`web/view_helpers.py` (line 125):**
- Teacher icon: `person_book` â†’ `history_edu` (Material Symbol "scholar" â€” character with graduation cap)

**`web/templates/web/login.html` (line 150):**
- Teacher signup card icon: `person_book` â†’ `history_edu`

**`web/templates/web/edit_profile.html` (line 61):**
- Teacher role card icon: `person_book` â†’ `history_edu`

**`web/views_profile.py` (line 37-44):**
- Added two new branches in the default-banner logic:
  - `role == 'teacher'` â†’ `banner_type = 'gradient-tutor'`, `banner_deco_text = 'tutor'` (CSS uppercases to "TUTOR")
  - `role == 'institution'` â†’ `banner_type = 'gradient-institution'`, `banner_deco_text = 'nebian'` (CSS uppercases to "NEBIAN")
- Both fall back to the default blue banner if `banner_url` is set
- These are placed AFTER the admin/mod/verified branches so admin teachers and verified teachers still get their higher-priority banner

**`web/static/web/css/app/07-profile-banner.css` (line 383-461):**
- **`gradient-tutor` preset** (emerald green): radial+linear gradients using `#064e3b â†’ #047857 â†’ #10b981 â†’ #34d399`; deco text is bigger (`3.5rem`) and wider letter-spacing (`0.30em`) to fill the short "TUTOR" string better
- **`gradient-institution` preset** (indigo): gradients using `#312e81 â†’ #4338ca â†’ #6366f1 â†’ #818cf8`; deco text uses default `2.5rem` for the 6-letter "NEBIAN" string
- Both have light + dark variants and a `@media (max-width: 600px)` rule for mobile

**Design decisions:**
- Teachers get a `TUTOR` deco text (not `TEACHER`) â€” shorter, more brand-like, matches the visual weight of other deco texts (`MODERATOR`, `NEBIAN`, `NEBY AI`)
- Institution deco text stays `nebian` (rendered as `NEBIAN` by `text-transform: uppercase`) per user request â€” the only change is the indigo gradient theme matching the institution badge
- The badge priority order is unchanged: bot â†’ admin â†’ moderator â†’ role â†’ verified â†’ None. So an admin teacher still gets the admin gold crown, not the teacher green badge

**Files modified:**
- `web/templates/web/profile.html` (line 75-83)
- `web/view_helpers.py` (line 125)
- `web/templates/web/login.html` (line 150)
- `web/templates/web/edit_profile.html` (line 61)
- `web/views_profile.py` (line 37-44)
- `web/static/web/css/app/07-profile-banner.css` (lines 383-461, +78 lines)

**Not deployed yet â€” user hasn't given the go-ahead.**

### Previous Session
**Added "explorer" role (just exploring) â€” fourth user role alongside student/teacher/institution**

**Goal:** Let users sign up without committing to a role â€” they can explore the platform first and upgrade later.

**Changes:**
- Added `User.ROLE_EXPLORER = 'explorer'` and new tuple `(ROLE_EXPLORER, 'Explorer')` in `api/models.py:14-19`
- Created migration `api/migrations/0042_alter_user_role.py` to add the new choice to the `role` field's `choices`
- Updated role allowlist in `api/views_auth.py:213` (signup) and `web/views_profile.py:290` (edit profile) to accept `'explorer'`
- `_profile_incomplete()` in `api/view_helpers.py:86` â€” explorers have no role-specific required fields (no class_level, teaching_subjects, or school)
- `_user_badge_info()` in `web/view_helpers.py:135-140` â€” returns `{type: 'explorer', icon: 'travel_explore', color: '#F59E0B', label: 'Explorer'}` badge (amber, Material `travel_explore` icon)
- Added `.role-badge-explorer` CSS in `02-badges-actions.css` (light + dark mode variants, amber)
- Added `.pf-explorer-tagline` CSS in `02-profile-modals-photo-bot.css` (amber/orange, mirrors `pf-bot-tagline` pattern)
- Added `.role-radio-card-explorer` + `.auth-role-card-explorer` dashed-border style (visually distinguishes the "casual" option from the three core role cards)
- Added `.auth-role-divider` divider CSS for the "Or just exploring?" line in the signup card

**Signup card (`web/templates/web/login.html`):**
- Added a `<div class="auth-role-divider"><span>Or just exploring?</span></div>` after the three core role cards
- Added a fourth `<button class="auth-role-card auth-role-card-explorer" data-role="explorer">` card with `travel_explore` icon, "Just browsing for now" description
- Updated `roleLabels` map in the `select-role` action handler (line 506) to include `explorer: 'Explorer'`

**Edit profile (`web/templates/web/edit_profile.html`):**
- Added fourth role card `<label class="role-radio-card role-radio-card-explorer">` with `value="explorer"`
- Added `<div id="role-fields-explorer" class="role-fields">` info block â€” friendly hint: "You're exploring NEBians for now. You can update your role to Student, Teacher, or Institution anytime from this page."
- Updated `fieldSections` map (line 631) to include `explorer: document.getElementById('role-fields-explorer')`
- Updated `schoolLabels`, `schoolPlaceholders`, `classLabels` maps to include 'explorer' entries (so school/class labels render sensibly when explorer is selected)

**Profile page (`web/templates/web/profile.html`):**
- Added explorer branch to the role badge duplication block (line 91) â€” third conditional now includes explorer
- Added `{% elif profile_user.role == 'explorer' %}` branch in `pf-card-headline` â€” shows `ðŸ§­ Exploring NEBians` tagline + optional class_level/school

**Topbar dropdown (`web/templates/base.html:131`):**
- **Fixed pre-existing bug:** `<span class="profile-dropdown-role">Student</span>` was hardcoded as literal "Student" â€” now renders the actual role: Teacher / Institution / Explorer / Student

**Mock user seeder (`api/management/commands/create_mock_users.py`):**
- Added `mock_explorer_001` account: `explorer_demo / demo1234`, "Curious Learner", based in Bhaktapur, "Just exploring NEBiansâ€¦"

**No new migrations strictly required for explorer-specific fields** â€” the migration `0042_alter_user_role.py` only updates the `choices` list on the existing field. No new columns.

**Files modified:**
- `api/models.py` (line 14-19)
- `api/migrations/0042_alter_user_role.py` (NEW)
- `api/views_auth.py` (line 213)
- `api/view_helpers.py` (lines 86-99)
- `web/view_helpers.py` (lines 135-140)
- `web/views_profile.py` (line 290)
- `web/templates/web/login.html` (line 159-164, 506, plus CSS at lines 47-71)
- `web/templates/web/edit_profile.html` (lines 69-72, 162-168, 631-641)
- `web/templates/web/profile.html` (lines 91-93, 105-114)
- `web/templates/base.html` (line 131)
- `web/static/web/css/app/02-badges-actions.css` (lines 26-28)
- `web/static/web/css/pages/profile/02-profile-modals-photo-bot.css` (lines 88-100)
- `web/static/web/css/pages/web-edit-profile.css` (lines 70-84)
- `api/management/commands/create_mock_users.py` (lines 8, 61-74, 85)

**Not deployed yet â€” user hasn't given the go-ahead.**

### Previous Session
**HTMX â€” no-reload page transitions** â€” added HTMX (14KB, zero dependencies) to eliminate full-page reloads on sort/filter/pagination actions. Pages now swap content fragments in-place with `history.pushState` for URL updates.

**Changes:**
- Added `django-htmx==1.23.0` to `requirements.txt` and `INSTALLED_APPS`/`MIDDLEWARE`
- Downloaded `htmx.min.js` to `web/static/web/js/`
- Added HTMX script + config meta tag + loading bar + CSRF header setup to `base.html`
- Added `.htmx-loading-bar` CSS animation to `app.css`
- Created partial templates: `_forum_posts.html`, `_forum_post_replies.html`, `_library_content.html`
- Modified views: `forum()`, `library()`, `forum_post()` â€” when `request.htmx` is True, render the partial template instead of full page

**Forum page (`/forum/`) â€” HTMX:**
- Sort tabs (Hot/New/Top/Discussed): `hx-get` â†’ `#forum-posts-list` â†’ `hx-push-url="true"`
- Category chips (mobile + sidebar): `hx-get` â†’ `#forum-posts-list` â†’ `hx-push-url="true"`
- Search input: `hx-trigger="keyup changed delay:400ms, search"` for debounced live search
- Active filter chip remove links: `hx-get` â†’ `#forum-posts-list`
- Pagination prev/next: `hx-get` â†’ `#forum-posts-list` â†’ `hx-push-url="true"`
- Clear search button: uses `htmx.ajax()` instead of form submit

**Library page (`/library/`) â€” HTMX:**
- Sort dropdown: `hx-trigger="change"` â†’ `#library-content` â†’ `hx-push-url="true"`
- Filter chip remove links: `hx-get` â†’ `#library-content` â†’ `hx-push-url="true"`
- "Clear all" link: `hx-get` â†’ `#library-content`
- Pagination links: `hx-get` â†’ `#library-content` â†’ `hx-push-url="true"`
- Apply filters: uses `htmx.ajax()` + `history.pushState()` instead of `window.location.href`

**Forum post detail (`/forum/post/<id>/`) â€” HTMX:**
- Reply sort buttons (Oldest/Newest/Top): `hx-get` â†’ `#replies-list` â†’ `hx-push-url="true"`
- Replies wrapped in `<div id="replies-list">` for HTMX targeting

**Global HTMX setup:**
- `htmx:beforeRequest` â†’ shows top loading bar
- `htmx:afterRequest` â†’ hides loading bar
- `htmx:responseError` â†’ hides loading bar + shows snackbar error
- CSRF token injected via `hx-headers` on `<body>`

**Previous session:**
- Added **Most Liked** sort option: `order_by('-like_count', '-added_at')`
- Sort dropdown now has: Most Relevant, Trending, Newest, Most Liked, Oldest

**Home page (`/`):**
- "Forum Activity" section renamed to **"Trending Discussions"**
- Posts now sorted by hot score algorithm instead of just `created_at`
- "View all" link points to `/forum/?sort=hot`
- CTA button text changed from "Start a Discussion" to "Join the Discussion"

**Files modified:**
- `web/views.py` â€” `_compute_hot_score()`, `forum()` (sort/search/filter/pagination), `forum_post()` (reply sort), `library()` (trending/liked sort), `home()` (hot-scored posts)
- `web/templates/web/forum.html` â€” search bar, sort tabs, active filter chips, pagination, updated category links
- `web/templates/web/forum_post.html` â€” reply sort buttons (Oldest/Newest/Top)
- `web/templates/web/home.html` â€” "Trending Discussions" section with hot-scored posts
- `web/templates/web/library.html` â€” Trending and Most Liked sort options

**No new migrations or model changes.**

---

### Previous Session
**Community chat proxies for "Neby AI" (Android + web)** â€” built Django proxies in front of free keyless web-chat services (Qwen, K2 Think, Poolside, Motif, eGov, DeepAI, Inception). Sessions are stored in `ArenaChatSession`/`ArenaChatMessage` rows with a provider discriminator; streaming is OpenAI-style SSE. See the **"Community Chat Proxies"** section above for the full architecture.

### Previous Session
UI/UX revamp â€” home page, library, search, and design system consistency pass:

**Home page revamp:**
- Hero section: gradient background (`surface-container â†’ transparent`), rounded corners, tighter heading (800 weight, -0.02em tracking), "Hello, Student!" â†’ "Welcome to NEBians" for guests, "Join Forum" button changed from `md-btn-outlined` to `md-btn-tonal`
- Forum post meta: simplified "started a discussion" â†’ "posted", removed class wrappers (`post-card-meta-top`/`post-card-meta-bottom`), standardized dot separator opacity to 0.3
- Resource cards: colored header strip (`background: color-mix(8%, subject-color, transparent)`), subject label colored with `var(--subject-color)`, tighter padding, `overflow: hidden`
- Section headers: `align-items: center` â†’ `align-items: baseline`

**Library page revamp (concept UI implementation):**
- Sidebar filter layout on desktop (260px sticky sidebar with collapsible sections for Grade/Subject/Type)
- Mobile: filter button opens modal dialog (same as before)
- Sort bar: "Showing Xâ€“Y of Z resources" + sort dropdown (Most Relevant/Newest/Oldest)
- Featured card: first resource on page 1 with no filters gets a landscape card with subject icon, type badge, author, date, and stats
- Standard resource cards: same `.resource-card` component with colored subject header
- "More coming soon" dashed card at end of grid
- Pagination controls at bottom (page numbers, prev/next arrows)
- Badge colors by type: `.badge-notes` (primary), `.badge-paper` (pink), `.badge-model` (teal), `.badge-textbook` (purple)
- View function now supports `sort` param (`relevant`/`newest`/`oldest`) and pagination (`page` param, 12 per page)
- `page_obj` passed to template for pagination rendering

**Search page revamp (complete rewrite):**
- Search bar is a proper M3 pill-shaped bar with search icon, input, close button, and `tune` filter icon inside the bar (right side)
- Filter icon turns blue when filters are active (`.has-filters`)
- Active filter chips appear below the search bar as removable pills
- Filter dialog (modal) replaces collapsible panel â€” same pattern as library
- Tab switcher: All / Resources / Posts â€” only visible after a query
- "All" tab shows combined results: resources in grid cards, posts in post cards
- Search view now queries both `Resource` and `Post` models
- Subject filter applies to `Post.category` when searching posts
- Grade and Type filters hidden on Posts tab (not applicable)

**Search view (`views.py`) changes:**
- Accepts `tab` param: `all` (default), `resources`, `posts`
- Accepts `subject`, `grade`, `type` filter params
- Returns `resource_results`, `post_results`, `all_subjects`, `all_grades`, `all_types`, `current_subject/grade/type`
- `all_subjects/grades/types` always populated (even without query) for filter panel on landing page

**Design system consistency pass:**
- **Horizontal scrollbar**: Hidden (`scrollbar-width: none` + `::-webkit-scrollbar { display: none }`) â€” was a visible thin bar that looked bad. Added `padding-bottom: 16px` for swipe room.
- **Shared CSS utility classes added to `app.css`:**
  - `.post-meta-line` â€” flex row for post author/badge/follow (replaces 6+ inline style instances across templates)
  - `.post-meta-sub` â€” flex row for post metadata line (replaces 6+ inline style instances)
  - `.dot-sep` â€” `opacity: 0.3` for `Â·` separators (standardized from mixed 0.3/0.4)
  - `.icon-sm` / `.material-symbols-outlined.icon-sm` â€” 14px icon size (replaces `style="font-size:14px"`)
  - `.md-btn .material-symbols-outlined` â€” 18px icon size in buttons (replaces `style="font-size:18px"`)
  - `.md-tab .material-symbols-outlined` â€” 18px icon size in tabs
  - `.back-link` â€” shared back button style
  - `.site-main` / `.site-footer` / `.site-footer-links` â€” replaced inline styles on `<main>` and `<footer>` in base.html
  - `.filter-overlay` / `.filter-dialog` / `.filter-section` / `.filter-section-label` / `.filter-dialog-actions` / `.search-filter-chip` â€” extracted from template `extra_css` blocks into shared `app.css`
  - `.md-btn-icon.has-filters` â€” blue tint on filter icon when filters active
- **Hardcoded colors fixed in `app.css`:**
  - `.follow-btn-inline.following` and `.follow-btn-small.following`: `#fff` â†’ `var(--md-on-primary)`
  - `.post-card-category-link`: `rgba(27,110,243,0.08)` â†’ `var(--md-secondary-container)`, `#004ac6` â†’ `var(--md-on-secondary-container)`, `rgba(27,110,243,0.15)` â†’ `var(--md-outline-variant)`
  - `.post-card-category-link:hover`: `rgba(27,110,243,0.15)` â†’ `var(--md-primary-container)`
  - `.post-card`: removed `#ffffff` and `#e2e8f0` fallbacks, using plain `var()` values
  - `.post-card-avatar`, `.act-avatar`: removed `#dbeafe` and `#004ac6` fallbacks
- **Inline styles cleaned up across templates:**
  - `home.html`: Removed `style="font-size:18px"` on button icons, `style="font-size:14px"` on footer icons, replaced inline post-meta flex styles with `.post-meta-line`/`.post-meta-sub`, replaced `opacity:0.3` dots with `.dot-sep`
  - `search.html`: Same cleanup â€” removed all inline font-size/icon styles, replaced inline post-meta styles with classes
  - `library.html`: Removed duplicated filter dialog CSS from `extra_css` block (now in `app.css`), replaced `style="font-size:14px"` with `.icon-sm`
  - `base.html`: Replaced inline styles on `<main>` and `<footer>` with `.site-main` and `.site-footer` classes
- **Removed duplicated CSS:**
  - Filter dialog CSS removed from both `library.html` and `search.html` `extra_css` blocks (now shared in `app.css`)
  - `.search-filter-pill` class removed from `app.css` (replaced by `.search-filter-chip`)
  - `#filter-panel` / `#search-filter-panel` collapsible panel styles removed
  - `.filter-active-dot` style removed

**Issue 1 â€” Eliminated HTTP API roundtrips in web views:**
- Created `api/services.py` â€” direct Python service functions called by web views instead of HTTP API calls
- `web/views.py` now calls `services.toggle_post_like()`, `services.create_post()`, `services.create_reply()`, `services.toggle_follow()`, etc. directly â€” no more `api_client._api_call()` for data operations
- `google_auth` view now uses `verify_google_token()` directly instead of `api.auth_google()` HTTP call
- Admin views (dashboard, users, resources, posts) all query the DB directly instead of going through `api_client`
- `api_client.py` is still used for session management (`get_session_token`, `set_session_auth`, `clear_session_auth`) but NO data operations go through HTTP anymore
- This eliminates: latency from localhost HTTP calls, double middleware processing, JSON serialization overhead, and potential deadlocks on single-process LSAPI

**Issue 2 â€” Switched from LocMemCache to Redis:**
- Added `redis==5.2.1` to `requirements.txt`
- `settings.py` now supports `CACHE_BACKEND` and `CACHE_LOCATION` env vars for Redis configuration
- `SESSION_ENGINE` automatically switches to `django.contrib.sessions.backends.cache` when Redis is configured
- `.env` on server now has: `CACHE_BACKEND=django.core.cache.backends.redis.RedisCache`, `CACHE_LOCATION=redis://127.0.0.1:6379/0`, `SESSION_ENGINE=django.contrib.sessions.backends.cache`
- Redis is auto-started via cPanel crontab (`/home/consicac/.cpanel/redis/redis.conf`)
- Falls back to `LocMemCache` if env vars not set (for local dev)

**Issue 3 â€” Denormalized counters on User model:**
- Added 7 fields to User model: `post_count`, `reply_count`, `follower_count`, `following_count`, `likes_given_count`, `likes_received_count`, `contribution_score`
- Migration 0012: adds the fields (default=0)
- Migration 0013: backfills all existing data using batch aggregation queries
- Created `api/counters.py` with `increment_*`/`decrement_*` helper functions using `F()` expressions for atomic updates
- Counter updates called from: `api/views.py` (like toggle, follow toggle, post/reply create/delete) and `api/services.py` (same operations for web views)
- `_build_stats()` and `_build_local_stats()` now use denormalized counters when available (>0), fall back to aggregate queries for safety
- `_build_contributors_batch()` now uses denormalized counters â€” drops from ~10 aggregation queries to 1 User table scan
- Profile page (`profile` view) now uses `user.follower_count` / `user.following_count` instead of COUNT queries

**Issue 4 â€” Improved cache TTL and invalidation:**
- Forum contributors cache: 120s â†’ 300s (5 minutes)
- Home resources cache: 120s â†’ 300s
- Home posts cache: 60s â†’ 120s
- `_clear_page_cache()` now also clears `admin_stats` and `sitemap_xml`
- Counter increments/decrements happen atomically on write, so cached pages are always consistent

**Previous session also completed:**
- Added `banner_url` field to User model with HTTPS URL validation
- Added `Report` model for content moderation + admin report management endpoints
- Fixed CSP `unsafe-eval` for PDF viewer embeds
- Removed `sandbox` attribute from PDF iframe (was blocking external PDF viewers)
- Fixed `user_profile_create_or_update` to use DRF auth
- Added rate limiting to post creation, follow toggle, FCM registration
- FCM token format validation (10-512 chars)
- Filtered archived posts from public listings
- Paginated `search_all` endpoint
- Removed dead `posts_list`/`replies_list` endpoints
- Created `cleanup_stale_data` management command
- Migration 0008 (banner_url + Report model), Migration 0009 (performance indexes)

**Reverted broken frontend production pass:**
- Another AI agent made CSS/template refactoring changes (design tokens, utility classes, inline style extraction) that broke UI/UX and introduced JS syntax errors
- Reverted 30+ template/CSS files to pre-agent state via `git checkout b91a5a8 --`
- Committed as `f7d390f`
- All performance backend changes (services.py, Redis, counters) were preserved

### Resolved Issues
1. **Auth token regeneration bug** â€” Every Google sign-in was regenerating the auth token, invalidating existing sessions. Fixed by only generating tokens on signup, not on each login.
2. **Stale session 401 errors** â€” Follow/like/edit calls returned "Unauthorized" because session tokens didn't match DB. Fixed with `_get_valid_token()` helper that validates against DB and clears stale sessions.
3. **Duplicate `{% block description %}`** â€” forum.html, search.html, library.html had duplicate template blocks causing TemplateSyntaxError. Fixed.
4. **Admin API URL mismatch** â€” `admin_urls.py` had paths without trailing slashes but `api_client.py` called with trailing slashes. Fixed all to use trailing slashes.
5. **Sitemap crash** â€” `created_at` is a BigIntegerField (ms timestamp), not DateTimeField. Fixed `.isoformat()` calls to convert from ms timestamps.
6. **PostLike/ReplyLike admin** â€” Referenced non-existent `created_at` field. Removed from `list_display`.
7. **SECURE_SSL_REDIRECT breaking site** â€” Set to `True` in production would cause infinite redirects behind LiteSpeed (SSL terminates at proxy). All SSL/cookie secure settings set to `False` by default.

### Admin Credentials
- **Custom admin panel** (`/admin/`): Login with Django staff superuser account
  - Username: `admin`
  - Password: `***REMOVED***`
- **Django admin** (`/admin-django/`): Same credentials
- Create new superusers: `python manage.py createsuperuser`

### Key Files That Were Recently Modified
- `backend_python/web/views.py` â€” `forum()` and `library()` and `forum_post()` now detect `request.htmx` and render partial templates; `_compute_hot_score()` for Reddit-style hot ranking; `forum()` supports sort/search/filter/pagination; `forum_post()` supports reply sort; `library()` supports trending/liked sort; `home()` uses hot-score algorithm
- `backend_python/web/templates/web/_forum_posts.html` â€” NEW: partial template for forum posts list (used by HTMX and full page include)
- `backend_python/web/templates/web/_forum_post_replies.html` â€” NEW: partial template for forum post replies (used by HTMX and full page include)
- `backend_python/web/templates/web/_library_content.html` â€” NEW: partial template for library resource grid (used by HTMX and full page include)
- `backend_python/web/templates/web/forum.html` â€” HTMX attributes on sort tabs, category chips, search, pagination, sidebar links; includes `_forum_posts.html`; search input has debounced `hx-trigger`
- `backend_python/web/templates/web/forum_post.html` â€” HTMX attributes on reply sort buttons; includes `_forum_post_replies.html`; wrapped replies in `#replies-list`
- `backend_python/web/templates/web/library.html` â€” HTMX attributes on sort dropdown, filter chips, pagination; includes `_library_content.html`; JS uses `htmx.ajax()` for filter apply and sort change
- `backend_python/web/templates/web/base.html` â€” Added HTMX script, config meta tag, loading bar div, CSRF header injection, `htmx:beforeRequest`/`htmx:afterRequest`/`htmx:responseError` event handlers
- `backend_python/web/static/web/js/htmx.min.js` â€” NEW: HTMX 1.9.12 library (48KB)
- `backend_python/web/static/web/css/app.css` â€” Added `.htmx-loading-bar` animation CSS
- `backend_python/nebians/settings.py` â€” Added `django_htmx` to `INSTALLED_APPS` and `HtmxMiddleware` to `MIDDLEWARE`
- `backend_python/requirements.txt` â€” Added `django-htmx==1.23.0`
- `backend_python/api/models.py` â€” Added 7 denormalized counter fields to User model (`post_count`, `reply_count`, `follower_count`, `following_count`, `likes_given_count`, `likes_received_count`, `contribution_score`), `banner_url` field, `Report` model, verification_code CharField(128)
- `backend_python/api/views.py` â€” Counter increment/decrement calls on like toggle, follow toggle, post/reply create/delete; `_build_stats()` uses denormalized counters; follower_count in follow toggle uses denormalized counter
- `backend_python/api/services.py` â€” NEW: Direct Python service functions for web views (replaces HTTP API roundtrips). Includes `toggle_post_like`, `toggle_reply_like`, `create_reply`, `create_post`, `toggle_follow`, `check_username_available`, `set_password`, `change_password`, `activate_photo`. All call counter helpers.
- `backend_python/api/counters.py` â€” NEW: `increment_*`/`decrement_*` helper functions for denormalized User counters using `F()` expressions
- `backend_python/api/serializers.py` â€” Added `banner_url` to UserSerializer/UserPublicSerializer, ReportSerializer, `isThumbedUp` uses batch-prefetched context keys
- `backend_python/api/authentication.py` â€” Auth token caching with 5-minute TTL
- `backend_python/api/admin_views.py` â€” Admin report management endpoints, `banner_url` in user PATCH
- `backend_python/api/admin_urls.py` â€” Report admin URL patterns
- `backend_python/api/admin.py` â€” Registered Report model in Django admin
- `backend_python/api/security.py` â€” Password hashing, verification code hashing, URL validation, image upload validation, admin signature signing
- `backend_python/api/throttles.py` â€” AuthRateThrottle, VerificationRateThrottle
- `backend_python/api/migrations/0010_rename_api_edithistory_target_idx_...py` â€” Auto-generated RenameIndex operations (placeholder for server migration)
- `backend_python/api/migrations/0011_reply_count_and_index.py` â€” Adds `reply_count` field + `parent_reply_id/created_at` index
- `backend_python/api/migrations/0012_add_denormalized_user_counters.py` â€” Adds 7 counter fields to User model
- `backend_python/api/migrations/0013_backfill_user_counters.py` â€” Backfills counter data from aggregate queries
- `backend_python/nebians/settings.py` â€” Redis cache support via `CACHE_BACKEND`/`CACHE_LOCATION` env vars, `SESSION_ENGINE` auto-switch, `CONN_MAX_AGE=60`, `CONN_HEALTH_CHECKS=True`
- `backend_python/nebians/middleware.py` â€” SecurityHeadersMiddleware (CSP with `unsafe-eval`, Permissions-Policy, COOP)
- `backend_python/web/views.py` â€” Replaced all HTTP API calls with direct DB queries and `services.*` calls; admin views query DB directly; denormalized counters in `_build_local_stats()`, `_build_contributors_batch()`, profile views; `_clear_page_cache()` clears admin_stats/sitemap_xml; increased cache TTLs
- `backend_python/web/api_client.py` â€” Only used for session management now (`get_session_token`, `set_session_auth`, `clear_session_auth`). No data operations use HTTP anymore.
- `backend_python/requirements.txt` â€” Added `redis==5.2.1`
- `backend_python/web/templates/web/forum_post.html` â€” Three-dot menu on post/reply headers, bookmark/share buttons in action bars, `renderMarkdown()` JS for bold/italic/line-break rendering, `mention_links` template filter with markdown support
- `backend_python/web/templates/web/forum.html` â€” Three-dot menu on post cards (bookmark/share/report)
- `backend_python/web/templates/web/home.html` â€” Three-dot menu on forum activity items (bookmark/share)
- `backend_python/web/templates/web/search.html` â€” Three-dot menu on search result post cards
- `backend_python/api/models.py` â€” Added `Bookmark` model (user, target_type, target_id), `Reply.is_archived` field
- `backend_python/api/migrations/0016_bookmarks_and_reply_archive.py` â€” Creates `bookmarks` table (manual creation via mariadb CLI needed due to charset mismatch), adds `is_archived` to `replies`
- `backend_python/api/views.py` â€” Added `bookmark_toggle`, `bookmark_list`, `bookmark_check` API endpoints
- `backend_python/web/views.py` â€” Added `ajax_bookmark_toggle`, `ajax_bookmark_check`, `ajax_archive_reply`; `ajax_delete_post`/`ajax_delete_reply` now cascade-delete bookmarks, likes, edit history, reports, child replies; all serializers include `isBookmarked` field
- `backend_python/web/urls.py` â€” Added `/ajax/bookmark/toggle/`, `/ajax/bookmark/check/`, `/ajax/archive/reply/<id>/`
- `backend_python/api/urls.py` â€” Added `/api/bookmarks/toggle/`, `/api/bookmarks/`, `/api/bookmarks/check/`
- `backend_python/web/static/web/css/app.css` â€” Added `.more-btn`, `.more-menu`, `.more-menu-wrapper`, `.more-menu-item`, `.more-menu-divider`, `.bookmark-active` CSS components
- `backend_python/web/templatetags/web_extras.py` â€” `mention_links` filter now renders **bold**, *italic*, and line breaks

### Important Findings & Considerations for Other Agents

1. **Cache backend is now Redis** â€” `CACHE_BACKEND` and `CACHE_LOCATION` env vars control the cache backend. In production, Redis is used (`redis://127.0.0.1:6379/0`). In local dev without these env vars, it falls back to `LocMemCache`. Sessions also use Redis when configured (`SESSION_ENGINE=django.contrib.sessions.backends.cache`). Redis is auto-started via cPanel crontab.

2. **Auth token cache invalidation** â€” When a user changes their password (`auth_change_password`), their auth token is regenerated. The old token's cache entry (`auth_user:{old_token}` and `valid_token:{old_token}`) will linger for up to 5 minutes. This is acceptable because the old token is also invalidated in the DB. But if you need instant invalidation, add `cache.delete(f'auth_user:{old_token}')` and `cache.delete(f'valid_token:{old_token}')` in the password change handler.

3. **`_build_local_stats()` now uses denormalized counters** â€” When User counters are >0, it reads from the User model fields directly (0 queries). Falls back to aggregate queries for legacy rows where counters haven't been backfilled yet. Profile pages now do ~3 queries instead of ~12.

4. **`_build_contributors_batch()` uses denormalized counters** â€” Drops from ~10 aggregation queries to 1 User table scan. The leaderboard only shows `contribution_score`. If you need follower counts in the leaderboard, they're available via `follower_count`/`following_count` fields.

5. **Database indexes created by migration 0009** â€” These are B-tree indexes. MySQL's `__icontains` queries (LIKE '%term%') CANNOT use B-tree indexes â€” they always do a full table scan. For true full-text search, you'd need MySQL FULLTEXT indexes or a search service like Meilisearch. The current `icontains` approach is fine for <10k rows but will degrade with scale.

6. **CSP `script-src` includes `'unsafe-eval'`** â€” This was added because external PDF viewers (government PDF sites) use `eval()` internally. The `sandbox` attribute was also removed from the PDF iframe. If you want to re-harden CSP, you'd need to either proxy PDF content through your own server or use a PDF.js viewer that doesn't need eval.

7. **`CONN_MAX_AGE=60`** â€” This keeps MySQL connections alive for 60 seconds between requests. If LiteSpeed kills a worker after idle time, the connection may be stale. `CONN_HEALTH_CHECKS=True` handles this by checking connection health before reuse.

8. **Like toggle response uses computed count** â€” `post_like` and `reply_like` now compute `thumbs_up_count` locally (old value Â± 1) instead of `refresh_from_db()`. This means if two users like simultaneously, the count is still correct because `F()` expressions are atomic in the DB. The locally computed value may be off by 1 for the non-winning request, but the DB value is always correct.

9. **Migration 0009 added 15 indexes** â€” On a large table, `CREATE INDEX` can lock the table for minutes. On the current small dataset (<1000 rows), this completed instantly. If you add indexes to large tables in the future, use `ALTER TABLE ... ALGORITHM=INPLACE` or create indexes concurrently in a separate migration.

10. **`user_profile_create_or_update` now uses DRF auth** â€” Previously it manually parsed the `Authorization: Bearer` header. Now it uses `_require_user()` which goes through `AuthTokenAuthentication`. This means the auth token cache applies to profile updates too. If a user's token is cached and they regenerate it (e.g., password change), they'll get 401 until the cache expires (5 min) or they re-login.

11. **Cleanup management command** â€” `python manage.py cleanup_stale_data` clears expired verification codes, stale FCM tokens (90+ days), old Django sessions (30+ days), and abandoned unverified accounts (365+ days). Run this via cron or manually. Use `--dry-run` to preview what would be deleted.

12. **The `Report` model is available but not integrated into the web UI** â€” The API endpoint `POST /api/reports/` exists, and admin endpoints exist at `/api/admin/reports/` and `/api/admin/reports/<id>/`, but there's no "Report" button in the web templates yet. An agent would need to add report buttons to forum posts, replies, and user profiles.

13. **`banner_url` is in the User model and serializer but not in the web edit_profile template** â€” The Android app can send `bannerUrl` in profile updates, but the web edit profile page doesn't have a banner URL field yet.

14. **Redis cache is persistent across LSAPI workers** â€” Unlike LocMemCache, Redis is shared between all LSAPI workers and persists across restarts. This means cached pages, auth tokens, and sessions survive worker respawns. However, Redis is configured without persistence (`--save ''` on manual start, but the crontab config has `save` directives). If Redis restarts, the cache will be empty but will regenerate.

15. **CRITICAL: Static files are served from TWO locations â€” do NOT change STATICFILES_STORAGE** â€” LiteSpeed/LSAPI serves static files from `public/static/`, but Django's `STATIC_ROOT` points to `staticfiles/`. These are DIFFERENT directories. The `CompressedManifestStaticFilesStorage` (WhiteNoise) generates hashed filenames (e.g., `app.7d01927028c0.css`) and a `staticfiles.json` manifest. **Never switch to `StaticFilesStorage`** â€” it will break the manifest, delete hashed files, and cause UI corruption.

16. **CRITICAL: How to deploy CSS/JS changes correctly** â€” After editing files in `web/static/`, you MUST do BOTH of these:
    - Run `python manage.py collectstatic --noinput` (writes to `staticfiles/`)
    - Manually copy changed files to `public/static/web/css/` and `public/static/web/js/`:
      ```bash
      cp /home/consicac/nebians_api/web/static/web/css/app.css /home/consicac/nebians_api/public/static/web/css/app.css
      cp /home/consicac/nebians_api/web/static/web/css/material3.css /home/consicac/nebians_api/public/static/web/css/material3.css
      ```
    - **Do NOT delete `.gz` files or hashed files from `public/static/`** â€” they are needed by the web server for compression and manifest-based serving.

17. **MySQL charset mismatch blocks FK creation** â€” The `users` table uses `latin1_swedish_ci` charset but new Django tables default to `utf8mb4`. FK constraints fail because charset/collation must match. To create a table referencing `users`, either use `SET FOREIGN_KEY_CHECKS=0` and create the table manually with `DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci`, or convert the `users` table to `utf8mb4` first. The `bookmarks` table (Migration 0016) was created manually via mariadb CLI for this reason.

18. **Unicode escapes in post content** â€” When updating post content via `manage.py shell` piped from PowerShell, Python unicode escapes (`\\u000A`, `\\u0027`) get stored as literal strings instead of actual characters. Always verify post content after shell-based updates. If literal escapes appear, fix with:
    ```python
    content = content.replace('\\u000A', '\n').replace('\\u0027', "'")
    ```

19. **Three-dot menu + Bookmark system (Migration 0016)** â€” Added `Bookmark` model (user, target_type, target_id) and `Reply.is_archived` field. All post/reply cards across home, forum, search, and forum_post pages now have a three-dot `more-btn` â†’ `more-menu` dropdown. The menu is wrapped in `.more-menu-wrapper` for proper `position: absolute` containment. Menu options: Bookmark, Share, Report (non-author), Edit/Archive/Delete (author only). Bookmark toggle hits `/ajax/bookmark/toggle/`. Post/reply delete now cascades to bookmarks, likes, edit history, and child replies.

20. **Post delete cascade is thorough** â€” `ajax_delete_post` deletes: bookmarks for the post, bookmarks for all replies, PostLikes, ReplyLikes, EditHistory for post and replies, all replies, and the post itself. `ajax_delete_reply` deletes: bookmarks for the reply and its children, ReplyLikes, EditHistory, child replies, and the reply. Both use `transaction.atomic()`.

21. **Django 5.2 template tag multi-line pitfall** â€” The template parser treats `{% endblock %}` as invalid when the keyword and closing `%}` are on different lines. Both `{% endblock\n%}` (keyword on one line, `%}` on next) AND `{%\nendblock %}` (`{%` on one line, `endblock %}` on next) fail with `Unclosed tag on line N: 'block'`. This applies to all block tags (`{% endblock %}`, `{% else %}`, `{% elif %}`, `{% endif %}`, etc.) inside `{% block %}` regions. Always keep the entire tag on a single line. This bug was hit on `library.html` after a deploy and took 3 rounds of fixes to fully resolve.

---

## Long-Term Platform Vision â€” The SaaS Transition

### Orientation for AI Agents

All AI agents working on this codebase must maintain a forward-looking, production-ready vision. We are transitioning NEBians from a passive content hub (viewing, downloading, reading forums) into an **active Web Software / SaaS (Software as a Service)**. This means:
1. **Interactive Utilities:** Shifting from just file downloads to real-time collaboration features, automated active recall quizzes, interactive mock testing, and pomodoro study rooms.
2. **Role-Based Onboarding:** Custom workspaces and dashboards for three core personas: **Students** (trackers, flashcards, profiles), **Teachers** (verified accounts, resource publishing metrics, grading dashboards), and **Schools** (notice boards, managed classrooms).
3. **Gamification & Quests:** Redefining traditional Q&A forum sections as interactive **Academic Quests** with bounties, where students post challenges and peers/teachers earn contribution points for solving them.

**CRITICAL REFERENCE:** A separate, highly detailed product specification and architecture document is available in `docs/SAAS_VISION.md`. Review it to understand the technical plans, DB model adjustments, and UI requirements before designing features related to user roles, quizzing, collaboration rooms, or dashboards.