# NEBians - Project Knowledge Base

## Overview

NEBians is a Material 3 Android app for Nepali students (NEB curriculum). It provides study resources (ebooks, PDFs, notes), a discussion forum, and an advanced PDF viewer with annotation tools.

**Package:** `com.neb.ians`
**Min SDK:** 24 (legacy) / 28 (modern)
**Target SDK:** 34

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
- `modern` (minSdk 28) — for newer Android devices
- `legacy` (minSdk 24) — broader compatibility

Both use the same release signing config.

### Navigation Architecture
- Bottom navigation: Home, Library, Forum, Settings
- Standalone screens (full-screen, not fragments): ForumPostDetail, CreatePost, Reply, PdfReader, Search
- Forum screens are standalone to match the requirement of not being fragments or nav items

---

## App Structure

```
com.neb.ians/
├── NEBiansApp.kt          # Application class (Hilt, WorkManager, notification channels)
├── MainActivity.kt        # Single activity with Compose + dark mode
├── data/
│   ├── local/
│   │   ├── dao/           # Room DAOs (Resource, Annotation, Forum, Bookmark)
│   │   ├── entity/        # Room entities (5 tables)
│   │   └── database/      # NEBiansDatabase
│   ├── model/
│   │   └── SampleData.kt  # Seed data (20 resources, 6 forum posts, 5 replies)
│   └── repository/        # Repository layer (Resource, Forum, Annotation, Bookmark, Settings)
├── di/
│   ├── AppModule.kt       # DataStore provider
│   └── DatabaseModule.kt  # Room database + DAO providers
├── ui/
│   ├── Navigation.kt      # NavHost, Screen routes, bottom nav
│   ├── theme/             # M3 theme (Color, Type with Poppins, Theme)
│   └── screens/
│       ├── home/          # HomeScreen + HomeViewModel
│       ├── library/       # LibraryScreen + LibraryViewModel (categorization + filters)
│       ├── forum/         # ForumScreen, PostDetail, CreatePost, Reply + ViewModels
│       ├── reader/        # PdfReaderScreen, AnnotationOverlay, ReaderViewModel
│       ├── search/        # SearchScreen + SearchViewModel
│       └── settings/      # SettingsScreen + SettingsViewModel
├── util/
│   ├── TimeUtils.kt       # formatTimeAgo(), getSubjectColor()
│   └── NotificationHelper.kt  # WorkManager scheduling helpers
└── worker/
    ├── DataSeederWorker.kt      # Seeds sample data on first launch
    └── NotificationWorker.kt   # Push notification worker
```

---

## Actions Taken

### Initial Build
1. Created full Android project structure with Gradle (Kotlin DSL)
2. Set up Gradle wrapper (8.5), build configs, proguard rules
3. Generated release keystore (`nebians-release.keystore`) — committed to repo for CI
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
- No excessive shadows or gradients — flat M3 design
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
- Keystore is at repo root: `nebians-release.keystore` (alias: nebians, password: nebians123)
- Artifacts retained for 30 days

### Building Locally
```bash
./gradlew assembleModernRelease    # Modern APK (minSdk 28)
./gradlew assembleLegacyRelease    # Legacy APK (minSdk 24)
```

---

## Web Backend — Server & SSH Deployment

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
**ALWAYS use the local deploy script — NEVER use manual SCP/SSH commands.**

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
`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, and `CSRF_COOKIE_SECURE` are all set to `False` by default. This is intentional — LiteSpeed terminates SSL at the proxy level, so Django sees HTTP connections. Setting these to `True` causes infinite redirects or dropped cookies. Only enable them if you configure LiteSpeed to forward the `X-Forwarded-Proto` header correctly.

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

### CRITICAL: Static Files Deployment (Two-Location Problem)
LiteSpeed/LSAPI serves static files from `public/static/`, but Django's `STATIC_ROOT` points to `staticfiles/`. These are **DIFFERENT directories**. After editing CSS/JS in `web/static/`, you MUST update BOTH:

```bash
# 1. Run collectstatic (writes to staticfiles/)
cd /home/consicac/nebians_api
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
python manage.py collectstatic --noinput

# 2. Manually copy to public/static/ (where LiteSpeed serves from)
cp /home/consicac/nebians_api/web/static/web/css/app.css /home/consicac/nebians_api/public/static/web/css/app.css
cp /home/consicac/nebians_api/web/static/web/css/material3.css /home/consicac/nebians_api/public/static/web/css/material3.css
# ... repeat for any other changed static files
```

**NEVER do these:**
- Do NOT change `STATICFILES_STORAGE` from `CompressedManifestStaticFilesStorage` to `StaticFilesStorage` — it breaks the manifest and corrupts cached hashed files
- Do NOT delete `.gz` files from `public/static/` — the web server uses them for compression
- Do NOT delete hashed files (e.g., `app.7d01927028c0.css`) from `public/static/` — they are part of the WhiteNoise manifest
- Do NOT change `STATIC_ROOT` — it must stay as `BASE_DIR / 'staticfiles'`

---

## Web Backend — Architecture

### Django Project Structure
```
backend_python/
├── nebians/               # Django project settings
│   ├── settings.py        # Main settings (loads .env with dotenv override=True)
│   ├── middleware.py       # SecurityHeadersMiddleware (CSP, Permissions-Policy, COOP)
│   ├── urls.py            # Root URL config (admin at /admin/, Django admin at /admin-django/)
│   └── wsgi.py            # WSGI entry point
├── api/                   # REST API app
│   ├── models.py          # User, Resource, Post, Reply, Follow, Report, etc.
│   ├── views.py           # API endpoints (paginated, rate-limited)
│   ├── authentication.py  # Token auth + Google token verification
│   ├── security.py        # Password hashing, verification code hashing, URL validation, image upload validation
│   ├── throttles.py       # AuthRateThrottle, VerificationRateThrottle
│   ├── admin.py           # Django admin registrations (at /admin-django/)
│   ├── admin_views.py     # Custom admin API views (staff auth + signed internal headers)
│   ├── serializers.py     # DRF serializers
│   └── management/
│       └── commands/
│           └── cleanup_stale_data.py  # Expired codes, stale FCM tokens, old sessions
├── web/                   # Web frontend app (Django templates)
│   ├── views.py           # Page views + AJAX endpoints
│   ├── api_client.py      # Internal API client (uses signed internal headers for admin calls)
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates (base.html, web/*.html)
│   └── static/web/css/
│       ├── material3.css   # M3 design system (CSS custom properties)
│       └── app.css         # App-specific styles
├── .env                   # Environment variables (DEPLOYED TO SERVER)
└── manage.py
```

### Authentication Flow
1. **Google Sign-In:** Uses Google Identity Services (GIS) — `accounts.google.com/gsi/client`
   - GIS `initialize()` + `renderButton()` renders the Google button
   - On sign-in, GIS sends a JWT `credential` to `handleCredentialResponse()`
   - Frontend POSTs the credential to `/auth/google/` as `{ idToken: credential }`
   - Backend verifies via `google.oauth2.id_token.verify_oauth2_token()` against both `GOOGLE_CLIENT_ID` and `FIREBASE_PROJECT_ID`
   - On success, creates/updates User in DB and sets session cookie
   - **Auth tokens are NOT regenerated on each login** — only created on first signup. This prevents session invalidation.

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
- **Admin superuser credentials:** username=`admin`, password=`-0IQkyTlzLCAJdlyNdHrvA`
- Create new superusers with: `python manage.py createsuperuser`

### CRITICAL: Google Auth Configuration
- **OAuth Client ID:** `68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com`
- **Firebase Project:** `nebiansnepal`
- **Authorized JavaScript Origins** (in Google Cloud Console → Credentials):
  - `http://localhost`
  - `http://localhost:8000`
  - `https://nebiansnepal.firebaseapp.com`
  - `https://nebians.consica.com.np`
  - `https://www.nebians.consica.com.np`
- **OAuth Consent Screen:** Must be in **Production** mode (not Testing) or users outside the test list will be blocked

### CRITICAL: GIS Implementation Notes
- **DO NOT use Firebase Auth (`signInWithRedirect`, `signInWithPopup`)** — it causes `redirect_uri_mismatch` errors
- **DO NOT use `google.accounts.oauth2.initTokenClient()`** — it returns access tokens, NOT ID tokens
- **DO NOT use `google.accounts.id.prompt()`** — causes FedCM errors and double-initialize warnings
- **DO use `google.accounts.id.initialize()` + `google.accounts.id.renderButton()`** — this is the correct GIS approach
- The `handleCredentialResponse` callback receives a `response.credential` (JWT) which is sent to the backend
- Use plain `function` declarations (not `const` arrow functions) for callbacks that GIS calls — they must be globally accessible
- The GIS script must be loaded BEFORE calling `initialize()` — use the `window.addEventListener('load', ...)` + polling pattern
- **Never call `initialize()` more than once** — it causes "called multiple times" warnings

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
- `.md-btn-text:hover` → `rgba(0, 74, 198, 0.08)` (was `var(--md-primary-container)`)
- `.md-btn-outlined:hover` → `rgba(0, 74, 198, 0.08)` (was `var(--md-primary-container)`)
- `.auth-text-btn:hover` → `rgba(0, 74, 198, 0.08)` (was `var(--md-primary-container)`)
- `.auth-link-btn:hover` → `rgba(0, 74, 198, 0.08)` with `color: var(--md-primary)` (was solid fill)

---

## AI4Bharat Arena Proxy (Neby AI on Android)

The Android "Neby AI" tab uses a Django proxy in front of the public AI4Bharat Arena (`https://backend.arena.ai4bharat.co` — note `.co`, not `.org`). The arena is reverse-engineered from the SPA's source map at `https://arena.ai4bharat.org/static/js/main.ca5f343c.js.map`.

### How it works
- The arena is a free public chatbot arena. It exposes a Django/DRF backend that lets you mint an anonymous guest token via `POST /auth/anonymous/` and then call chat completions with no rate-limit login.
- **Per-anon-token limits:** 20 messages / 3 sessions. After that the token returns 401.
- To scale beyond those limits, we maintain a **pool of anon tokens** in the Redis cache (shared across LSAPI workers) and round-robin across them. Pool size default = 12. When a token is at 15/20 messages we stop handing it out for new sessions; at 20 it's marked dead and never reused.
- Streaming format is **custom** (not SSE): each line is `a0:"<json-stringified text>"` or `ad:{"finishReason":"stop"}`. Our proxy converts that to **OpenAI-style SSE** so any Android chat client can consume it.
- `modelId` goes **inside** the assistant message object, not at the top of the body. The arena resolves multi-turn threading via the bound `arena_session_id` and `parent_message_ids`.

### New files
- `backend_python/api/ai4bharat_proxy.py` — anonymous-token pool, low-level client, streaming translator, `pool_stats()` diagnostic
- `backend_python/api/arena_views.py` — DRF function-based views (auth required): models list, sessions CRUD, send message (SSE), regenerate
- `backend_python/api/arena_urls.py` — URL routes mounted under `/api/neby-arena/`
- `backend_python/api/migrations/0031_arena_chat_models.py` — `ArenaChatSession` + `ArenaChatMessage` tables
- `backend_python/api/management/commands/arena_smoke_test.py` — `python manage.py arena_smoke_test` — verifies upstream reachability + multi-turn threading
- `backend_python/api/management/commands/arena_e2e_test.py` — `python manage.py arena_e2e_test` — in-process E2E test of all 9 endpoints (creates a `testarena` user, runs real chat against the live arena)

### Modified files
- `backend_python/api/models.py` — added `ArenaChatSession` and `ArenaChatMessage` models
- `backend_python/api/throttles.py` — added `ArenaChatRateThrottle` (60/min, env-overridable via `DRF_ARENA_CHAT_THROTTLE`) and `ArenaListRateThrottle` (120/min)
- `backend_python/api/urls.py` — mounted `api.arena_urls` under `/api/neby-arena/`
- `backend_python/nebians/settings.py` — added two new throttle scopes

### Endpoints (all require `Authorization: Bearer <auth_token>`)
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/neby-arena/models/` | List active LLM models (Redis-cached 5 min) |
| GET | `/api/neby-arena/sessions/` | List user's chat sessions |
| POST | `/api/neby-arena/sessions/` | Create session — body: `{ "modelId": "...", "title": "..." }` |
| GET | `/api/neby-arena/sessions/<id>/` | Session + full message history |
| PATCH | `/api/neby-arena/sessions/<id>/` | Update title / isActive |
| DELETE | `/api/neby-arena/sessions/<id>/` | Hard delete (cascades to messages) |
| POST | `/api/neby-arena/sessions/<id>/messages/` | Send message — body: `{ "content": "..." }` — **SSE streaming response** |
| POST | `/api/neby-arena/messages/<id>/regenerate/` | Regenerate last assistant reply — **SSE streaming** |
| GET | `/api/neby-arena/pool-stats/` | Pool snapshot (staff only) |

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
- **Pool is in Redis cache** — keys `arena:pool:index` (set of tokens) and `arena:token:<token>` (JSON metadata). Survives LSAPI worker restarts.
- **`ARENA_TENANT` is empty by default** — the arena's tenant routing is optional for the public site.
- **`X-Anonymous-Token` header** is what we send to the arena, NOT `Authorization: Bearer`. The arena uses either, but anonymous tokens are easier to pool than JWTs.
- **Streaming generator uses pre-insert + finalise** — we save the assistant row in `pending` state at request start, then update with content on completion. If the client disconnects mid-stream, the partial content is still in the DB.
- **Regenerate reuses the assistant row's id** — so the client doesn't need to re-render. The `preinsert_assistant=False` flag in `_stream_assistant` is critical.
- **If the bound token dies mid-conversation**, the next send returns an `error: code=upstream` SSE event. The client should start a new session. (Auto-recovery with history replay is on the roadmap.)
- **No `is_active` field on `User` model** — use `is_locked` for block checks (the User model uses `is_locked`, not Django's default `is_active`).

### Operational notes
- The proxy depends only on the standard `requests` library — no extra PyPI deps needed.
- Upstream API can be flaky during arena maintenance windows. Throttle is 60/min; pool is 12 tokens → ~720 msgs/hour theoretical max.
- For high-traffic scenarios, increase `TOKEN_POOL_SIZE` in `ai4bharat_proxy.py`.

---

## Real-Time WebSockets (Channels + Daphne + Cloudflare Tunnel)

The NEBians web frontend (and any future client) gets live updates — new posts, replies, likes, notifications, follow changes, message events — over a single WebSocket connection. No polling, no FCM for the web.

### Architecture
```
Browser / Mobile
   │  wss://<host>/ws/
   ▼
Cloudflare (CF edge)        ← free, proxies WS through any port
   │
   ▼
Cloudflared quick tunnel    ← ~/.local/bin/cloudflared --protocol http2 --url http://127.0.0.1:8001
   │
   ▼
Daphne (ASGI) on 127.0.0.1:8001
   │
   ▼
RealtimeConsumer (Channels)
   │
   ├─→ Database (Postgres/MySQL) for auth + permissions
   └─→ Redis channel layer (cross-worker fanout)
```

### Why a tunnel, not LiteSpeed proxy
**LiteSpeed + LSAPI cannot proxy WebSockets reliably.** Even when the upgrade reaches daphne (101 Switching Protocols) and daphne logs a successful `WSCONNECT`, LiteSpeed buffers the response and never returns it to the client. Tried `RewriteRule [P]` and `ProxyPass` — both hung the WS connection. **Use Cloudflare Tunnel instead.**

Cloudflare's free tier proxies WebSockets through any outbound HTTPS port. No firewall changes, no DNS changes (for the trycloudflare quick tunnel — a named tunnel requires CF-hosted DNS).

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
Server blocks outbound UDP (CloudLinux firewall). The default QUIC protocol fails — cloudflared must use HTTP/2 transport.

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
5. Add CNAME in Cloudflare DNS: `ws` → `<UUID>.cfargotunnel.com` (proxied)
6. Set env var: `WS_PUBLIC_URL=wss://ws.nebians.consica.com.np/ws/` in `nebians_api/.env`
7. Restart cloudflared with: `cloudflared --config ~/.cloudflared/config.yml tunnel run nebians-ws`

### Trycloudflare wildcard via middleware rewrite
A trycloudflare URL looks like `https://abc123.trycloudflare.com` — different every restart. Django's `ALLOWED_HOSTS` check would reject these. Fix: `nebians.middleware.AllowedHostMiddleware` runs BEFORE `CommonMiddleware` and rewrites `HTTP_HOST` to `nebians.consica.com.np` when the request comes through a trycloudflare subdomain. This way:
- `ALLOWED_HOSTS` stays strict
- CSRF cookie uses the canonical origin
- URL reversal works correctly
- The middleware also sets `ALLOWED_HOSTS_GLOB` / `ALLOWED_HOST_SUFFIXES` from env vars for custom domains

### Files added
- `nebians/asgi.py` — `ProtocolTypeRouter` combining `django_asgi_app` (HTTP) and `websocket` (WS)
- `api/routing_ws.py` — single route `^ws/?$` → `RealtimeConsumer`
- `api/consumers_ws.py` — `RealtimeConsumer` (auth, heartbeat, batching, permission checks, rate limiting)
- `api/middleware_ws.py` — `JWTAuthMiddleware` (Bearer token auth for WS) + `OriginValidatorMiddleware`
- `api/realtime.py` — broadcast helpers: `broadcast_post_created/updated/deleted/like_changed`, `broadcast_reply_*`, `broadcast_notification`, `broadcast_follow_changed`, `broadcast_unread_count`, `get_health_snapshot`

### Files modified
- `nebians/settings.py` — `INSTALLED_APPS += ['daphne', 'channels']`; `ASGI_APPLICATION = 'nebians.asgi.application'`; `CHANNEL_LAYERS` (Redis or InMemory); `ALLOWED_HOSTS_GLOB` + `ALLOWED_HOST_SUFFIXES` env support
- `nebians/middleware.py` — added `AllowedHostMiddleware` (trycloudflare host rewriting)
- `api/services.py`, `api/views.py`, `api/notifications.py`, `api/neby.py` — broadcast calls on create/update/delete/like/follow/notification triggers
- `web/views.py` — `_get_ws_public_url()` helper; `ws_url` in `_ctx()` for all templates
- `web/templates/base.html` — `<body data-ws-url=...>` + `<script>window.WS_CONFIG = ...</script>` + `<script src="/static/web/js/realtime.js">` + `showNotifToast` JS
- `web/templates/web/forum_post.html`, `forum.html`, `home.html`, `notifications.html`, `library.html`, `profile.html` — WS subscriptions + live DOM updates
- `web/static/web/js/realtime.js` — WS client (auto-reconnect, heartbeat, tab-visibility, polling fallback, wildcard event dispatch, optimistic-update dedup)
- `web/static/web/css/app.css` — `.toastIn` animation, `.ws-state-dot` styles
- `requirements.txt` — `channels==4.2.0`, `channels-redis==4.2.1`, `daphne==4.1.2`, `websockets>=12` (test only)

### Wire format
**Client → Server** (JSON over WS):
```json
{ "action": "subscribe", "channel": "forum.public" }
{ "action": "subscribe", "channel": "forum.post.<id>" }
{ "action": "unsubscribe", "channel": "forum.public" }
{ "action": "ping" }
{ "action": "mark_read", "notification_id": 123 }
```

**Server → Client** (JSON over WS):
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
- Mobile / external clients send `Authorization: Bearer <auth_token>` — handled by `JWTAuthMiddleware` which sits **inside** `AuthMiddlewareStack` so session auth runs first
- Token is resolved via `User.objects.get(auth_token=token)` (NOT `UserAuthToken` which stores a hash) — see **AGENTS.md § Auth token cache invalidation**
- Locked users (`is_locked=True`) and bot users (`is_bot=True`) are rejected with `websocket.close(4401)` (custom code) at connect time
- After auth, the user's own `user` channel is auto-subscribed (no need to send a subscribe message)
- For staff users, the `admin` channel is auto-subscribed

### Client behavior (`realtime.js`)
- **Auto-reconnect** with exponential backoff: 1s → 2s → 4s → 8s → 16s (capped at 30s)
- **Heartbeat** every 25s — sends `{"action":"ping"}`, expects `{"type":"pong"}` within 5s, otherwise reconnects
- **Tab visibility** — pauses heartbeat when tab is hidden for >5 min, reconnects on focus
- **Polling fallback** — if WS doesn't connect within 6s, falls back to 60s polling for unread count
- **Batched events** — server flushes events every 50ms (so a reply + 3 likes arrive as one `event` packet)
- **Optimistic-update dedup** — DOM updates optimistically on user action; ignores WS events for the same `client_request_id` to avoid double-rendering
- **Per-channel permission** — server checks permissions per subscribe (e.g. user 123 can't subscribe to `user.456.profile`)

### Performance
- **Server-side per-message size limit:** 4 KB
- **Server-side per-connection rate limit:** 30 messages / 10s (configurable)
- **Server-side per-user cap:** 5 concurrent connections
- **Server-side idle timeout:** 5 min (heartbeat must be received)
- **Event batching:** 50ms window
- **Per-channel permission check** in `database_sync_to_async` to avoid blocking the event loop
- **Lazy group subscribe** — clients only join Redis groups they actually subscribe to (not the whole world)

### Gotchas
- **WS field name is `action`, not `type`** — the client sends `{"action": "subscribe", ...}`; the server checks `msg.get('action')`
- **Origin validation** — `OriginValidatorMiddleware` validates the `Origin` header against `nebians.consica.com.np` and `localhost:8000` (dev). Mismatch → `websocket.close(1008)`. CF tunnel adds the `Origin: https://nebians.consica.com.np` automatically since the client connects to nebians.consica.com.np first.
- **CSRF** — WS auth bypasses CSRF (no `csrf_exempt` needed) because Channels has its own middleware stack. The session cookie is validated server-side.
- **Static files for `realtime.js`** — remember to copy `realtime.js` to `public/static/web/js/` after editing (see "Static Files Deployment" above)
- **If daphne is down** — the client falls back to polling after 6s. No data loss because the unread-count endpoint still works via HTTP.
- **If cloudflared is down** — WS doesn't work at all (no public path to daphne). The page still loads via LiteSpeed, just no live updates.

### Production checklist
- [x] daphne running on 127.0.0.1:8001
- [x] cloudflared running with `--protocol http2 --url http://127.0.0.1:8001`
- [x] @reboot cron entries for both
- [x] Redis channel layer configured (shares Redis used for cache)
- [x] `database_sync_to_async` imported in `middleware_ws.py` (was missing in dev — caused 403 on bearer auth)
- [x] AllowedHostMiddleware deployed (handles trycloudflare wildcard)
- [x] window.WS_CONFIG.url injected in base.html
- [x] realtime.js copied to public/static/web/js/
- [ ] Named Cloudflare tunnel (stable URL — currently trycloudflare which rotates)

---

## Continuity Notes

### What Was Being Worked On (Last Session)
**Real-time WebSockets for NEBians web** — added a full WS layer (Channels + Daphne + Cloudflare Tunnel) so the web frontend gets live updates for posts, replies, likes, notifications, follows. See the **"Real-Time WebSockets"** section above for the full architecture. Verified end-to-end through the public Cloudflare URL (auth, subscribe, broadcast roundtrip all pass).

Also fixed: AI4Bharat Arena mojibake — encoding was being double-decoded, garbling Nepali text in assistant responses. Fixed in `api/ai4bharat_proxy.py` `stream_chat()` and `regenerate()`. 0 corrupted rows remain in DB.

### Previous Session
**Admin panel: BotConfig provider switcher** — added a `provider` dropdown to `/admin/bot/` so the admin can flip the Neby AI bot between three backends without code changes:

- **`qwen`** (default) — Qwen web chat via `qwen_proxy.call_qwen`
- **`ai4bharat`** — Indic LLM Arena via the new `ai4bharat_proxy.simple_chat()` (anon-token pool, non-streaming)
- **`custom`** — any OpenAI-compatible `/chat/completions` endpoint via the new `api/custom_provider.py`

The model picker swaps options based on provider (7 Qwen models / 11 AI4Bharat UUIDs / free-form text). The URL field changes its default + help text per provider, and is "sticky" — if the admin types a custom URL, switching providers won't overwrite it. The "API Key" field is always shown (Qwen ignores it, AI4Bharat ignores it, custom may need it).

**Files added:**
- `api/custom_provider.py` — generic OpenAI-compatible client (`call_custom(api_url, api_key, model, ...)`)
- `api/management/commands/test_bot_providers.py` — spins up a fake OpenAI server, exercises all 3 providers, restores config on exit

**Files modified:**
- `api/models.py` — added `BotConfig.provider` (choices: qwen/ai4bharat/custom, default qwen) + widened `model` to 200 chars
- `api/neby.py` — `call_ai_api()` now dispatches to the right provider; renamed docstring
- `web/views.py` — `admin_bot_config()` reads + validates the new `provider` field
- `web/templates/admin_panel/bot_config.html` — provider dropdown, dynamic model picker, JS-driven UI swap
- `api/migrations/0032_botconfig_provider.py` — adds `provider` column + backfills existing rows to 'qwen'

**Verified end-to-end** (all 3 providers returned text via the same `call_ai_api` dispatcher):
- `qwen` → 'OK'
- `ai4bharat` (live) → 'OK' via Gemini 3.5 Flash
- `custom` (fake OpenAI server) → 'Hello from custom!' with correct system+user roles in request

Deployed to production. Migration 0032 applied. `/admin/bot/` returns 302 to login as expected.

---

### Previous Session
**AI4Bharat Arena proxy for "Neby AI" on Android** — reverse-engineered https://arena.ai4bharat.org/ (Indic LLM Arena) and built a Django proxy in front of it. See the **"AI4Bharat Arena Proxy"** section above for the full architecture.

### Previous Session
UI/UX revamp — home page, library, search, and design system consistency pass:

**Home page revamp:**
- Hero section: gradient background (`surface-container → transparent`), rounded corners, tighter heading (800 weight, -0.02em tracking), "Hello, Student!" → "Welcome to NEBians" for guests, "Join Forum" button changed from `md-btn-outlined` to `md-btn-tonal`
- Forum post meta: simplified "started a discussion" → "posted", removed class wrappers (`post-card-meta-top`/`post-card-meta-bottom`), standardized dot separator opacity to 0.3
- Resource cards: colored header strip (`background: color-mix(8%, subject-color, transparent)`), subject label colored with `var(--subject-color)`, tighter padding, `overflow: hidden`
- Section headers: `align-items: center` → `align-items: baseline`

**Library page revamp (concept UI implementation):**
- Sidebar filter layout on desktop (260px sticky sidebar with collapsible sections for Grade/Subject/Type)
- Mobile: filter button opens modal dialog (same as before)
- Sort bar: "Showing X–Y of Z resources" + sort dropdown (Most Relevant/Newest/Oldest)
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
- Filter dialog (modal) replaces collapsible panel — same pattern as library
- Tab switcher: All / Resources / Posts — only visible after a query
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
- **Horizontal scrollbar**: Hidden (`scrollbar-width: none` + `::-webkit-scrollbar { display: none }`) — was a visible thin bar that looked bad. Added `padding-bottom: 16px` for swipe room.
- **Shared CSS utility classes added to `app.css`:**
  - `.post-meta-line` — flex row for post author/badge/follow (replaces 6+ inline style instances across templates)
  - `.post-meta-sub` — flex row for post metadata line (replaces 6+ inline style instances)
  - `.dot-sep` — `opacity: 0.3` for `·` separators (standardized from mixed 0.3/0.4)
  - `.icon-sm` / `.material-symbols-outlined.icon-sm` — 14px icon size (replaces `style="font-size:14px"`)
  - `.md-btn .material-symbols-outlined` — 18px icon size in buttons (replaces `style="font-size:18px"`)
  - `.md-tab .material-symbols-outlined` — 18px icon size in tabs
  - `.back-link` — shared back button style
  - `.site-main` / `.site-footer` / `.site-footer-links` — replaced inline styles on `<main>` and `<footer>` in base.html
  - `.filter-overlay` / `.filter-dialog` / `.filter-section` / `.filter-section-label` / `.filter-dialog-actions` / `.search-filter-chip` — extracted from template `extra_css` blocks into shared `app.css`
  - `.md-btn-icon.has-filters` — blue tint on filter icon when filters active
- **Hardcoded colors fixed in `app.css`:**
  - `.follow-btn-inline.following` and `.follow-btn-small.following`: `#fff` → `var(--md-on-primary)`
  - `.post-card-category-link`: `rgba(27,110,243,0.08)` → `var(--md-secondary-container)`, `#004ac6` → `var(--md-on-secondary-container)`, `rgba(27,110,243,0.15)` → `var(--md-outline-variant)`
  - `.post-card-category-link:hover`: `rgba(27,110,243,0.15)` → `var(--md-primary-container)`
  - `.post-card`: removed `#ffffff` and `#e2e8f0` fallbacks, using plain `var()` values
  - `.post-card-avatar`, `.act-avatar`: removed `#dbeafe` and `#004ac6` fallbacks
- **Inline styles cleaned up across templates:**
  - `home.html`: Removed `style="font-size:18px"` on button icons, `style="font-size:14px"` on footer icons, replaced inline post-meta flex styles with `.post-meta-line`/`.post-meta-sub`, replaced `opacity:0.3` dots with `.dot-sep`
  - `search.html`: Same cleanup — removed all inline font-size/icon styles, replaced inline post-meta styles with classes
  - `library.html`: Removed duplicated filter dialog CSS from `extra_css` block (now in `app.css`), replaced `style="font-size:14px"` with `.icon-sm`
  - `base.html`: Replaced inline styles on `<main>` and `<footer>` with `.site-main` and `.site-footer` classes
- **Removed duplicated CSS:**
  - Filter dialog CSS removed from both `library.html` and `search.html` `extra_css` blocks (now shared in `app.css`)
  - `.search-filter-pill` class removed from `app.css` (replaced by `.search-filter-chip`)
  - `#filter-panel` / `#search-filter-panel` collapsible panel styles removed
  - `.filter-active-dot` style removed

**Issue 1 — Eliminated HTTP API roundtrips in web views:**
- Created `api/services.py` — direct Python service functions called by web views instead of HTTP API calls
- `web/views.py` now calls `services.toggle_post_like()`, `services.create_post()`, `services.create_reply()`, `services.toggle_follow()`, etc. directly — no more `api_client._api_call()` for data operations
- `google_auth` view now uses `verify_google_token()` directly instead of `api.auth_google()` HTTP call
- Admin views (dashboard, users, resources, posts) all query the DB directly instead of going through `api_client`
- `api_client.py` is still used for session management (`get_session_token`, `set_session_auth`, `clear_session_auth`) but NO data operations go through HTTP anymore
- This eliminates: latency from localhost HTTP calls, double middleware processing, JSON serialization overhead, and potential deadlocks on single-process LSAPI

**Issue 2 — Switched from LocMemCache to Redis:**
- Added `redis==5.2.1` to `requirements.txt`
- `settings.py` now supports `CACHE_BACKEND` and `CACHE_LOCATION` env vars for Redis configuration
- `SESSION_ENGINE` automatically switches to `django.contrib.sessions.backends.cache` when Redis is configured
- `.env` on server now has: `CACHE_BACKEND=django.core.cache.backends.redis.RedisCache`, `CACHE_LOCATION=redis://127.0.0.1:6379/0`, `SESSION_ENGINE=django.contrib.sessions.backends.cache`
- Redis is auto-started via cPanel crontab (`/home/consicac/.cpanel/redis/redis.conf`)
- Falls back to `LocMemCache` if env vars not set (for local dev)

**Issue 3 — Denormalized counters on User model:**
- Added 7 fields to User model: `post_count`, `reply_count`, `follower_count`, `following_count`, `likes_given_count`, `likes_received_count`, `contribution_score`
- Migration 0012: adds the fields (default=0)
- Migration 0013: backfills all existing data using batch aggregation queries
- Created `api/counters.py` with `increment_*`/`decrement_*` helper functions using `F()` expressions for atomic updates
- Counter updates called from: `api/views.py` (like toggle, follow toggle, post/reply create/delete) and `api/services.py` (same operations for web views)
- `_build_stats()` and `_build_local_stats()` now use denormalized counters when available (>0), fall back to aggregate queries for safety
- `_build_contributors_batch()` now uses denormalized counters — drops from ~10 aggregation queries to 1 User table scan
- Profile page (`profile` view) now uses `user.follower_count` / `user.following_count` instead of COUNT queries

**Issue 4 — Improved cache TTL and invalidation:**
- Forum contributors cache: 120s → 300s (5 minutes)
- Home resources cache: 120s → 300s
- Home posts cache: 60s → 120s
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
1. **Auth token regeneration bug** — Every Google sign-in was regenerating the auth token, invalidating existing sessions. Fixed by only generating tokens on signup, not on each login.
2. **Stale session 401 errors** — Follow/like/edit calls returned "Unauthorized" because session tokens didn't match DB. Fixed with `_get_valid_token()` helper that validates against DB and clears stale sessions.
3. **Duplicate `{% block description %}`** — forum.html, search.html, library.html had duplicate template blocks causing TemplateSyntaxError. Fixed.
4. **Admin API URL mismatch** — `admin_urls.py` had paths without trailing slashes but `api_client.py` called with trailing slashes. Fixed all to use trailing slashes.
5. **Sitemap crash** — `created_at` is a BigIntegerField (ms timestamp), not DateTimeField. Fixed `.isoformat()` calls to convert from ms timestamps.
6. **PostLike/ReplyLike admin** — Referenced non-existent `created_at` field. Removed from `list_display`.
7. **SECURE_SSL_REDIRECT breaking site** — Set to `True` in production would cause infinite redirects behind LiteSpeed (SSL terminates at proxy). All SSL/cookie secure settings set to `False` by default.

### Admin Credentials
- **Custom admin panel** (`/admin/`): Login with Django staff superuser account
  - Username: `admin`
  - Password: `-0IQkyTlzLCAJdlyNdHrvA`
- **Django admin** (`/admin-django/`): Same credentials
- Create new superusers: `python manage.py createsuperuser`

### Key Files That Were Recently Modified
- `backend_python/web/templates/web/home.html` — Hero gradient, "Welcome to NEBians" for guests, `md-btn-tonal` for Join Forum, `.post-meta-line`/`.post-meta-sub`/`.dot-sep`/`.icon-sm` classes, removed inline styles
- `backend_python/web/templates/web/library.html` — Complete redesign: sidebar filter layout on desktop (260px sticky sidebar with collapsible Grade/Subject/Type sections), mobile filter dialog, sort bar with pagination (Most Relevant/Newest/Oldest, page numbers), featured card for first resource, standard resource cards, "More coming soon" dashed card, badge colors by type, pagination controls at bottom
- `backend_python/web/views.py` — Library view now supports `sort` param (relevant/newest/oldest) and pagination (`page` param, 12 per page) via Django Paginator; search view queries both Resource and Post models with filters and tabs
- `backend_python/web/templates/web/search.html` — Complete rewrite: search bar with filter icon, filter dialog modal, tab switcher (All/Resources/Posts), combined resource+post search, `.post-meta-line`/`.post-meta-sub`/`.dot-sep` classes
- `backend_python/web/templates/base.html` — `.site-main` and `.site-footer` classes replacing inline styles
- `backend_python/web/static/web/css/app.css` — Hero gradient, resource card colored header (`color-mix`), post-card tighter padding/radius, hscroll hidden scrollbar, `.post-meta-line`/`.post-meta-sub`/`.dot-sep`/`.icon-sm`/`.back-link`/`.site-main`/`.site-footer`/`.site-footer-links`/`.filter-overlay`/`.filter-dialog`/`.filter-section`/`.filter-section-label`/`.filter-dialog-actions`/`.search-filter-chip`/`.md-btn-icon.has-filters` utility classes, hardcoded color fixes, removed duplicated CSS
- `backend_python/web/static/web/css/material3.css` — `.subject-icon` size 48→40px, lighter background tint (12% vs 15%), `.md-tab .material-symbols-outlined` 18px rule
- `backend_python/web/views.py` — Search view now accepts `tab` param, `subject/grade/type` filter params, queries both Resource and Post models, returns `all_subjects/grades/types` even without query
- `backend_python/api/models.py` — Added 7 denormalized counter fields to User model (`post_count`, `reply_count`, `follower_count`, `following_count`, `likes_given_count`, `likes_received_count`, `contribution_score`), `banner_url` field, `Report` model, verification_code CharField(128)
- `backend_python/api/views.py` — Counter increment/decrement calls on like toggle, follow toggle, post/reply create/delete; `_build_stats()` uses denormalized counters; follower_count in follow toggle uses denormalized counter
- `backend_python/api/services.py` — NEW: Direct Python service functions for web views (replaces HTTP API roundtrips). Includes `toggle_post_like`, `toggle_reply_like`, `create_reply`, `create_post`, `toggle_follow`, `check_username_available`, `set_password`, `change_password`, `activate_photo`. All call counter helpers.
- `backend_python/api/counters.py` — NEW: `increment_*`/`decrement_*` helper functions for denormalized User counters using `F()` expressions
- `backend_python/api/serializers.py` — Added `banner_url` to UserSerializer/UserPublicSerializer, ReportSerializer, `isThumbedUp` uses batch-prefetched context keys
- `backend_python/api/authentication.py` — Auth token caching with 5-minute TTL
- `backend_python/api/admin_views.py` — Admin report management endpoints, `banner_url` in user PATCH
- `backend_python/api/admin_urls.py` — Report admin URL patterns
- `backend_python/api/admin.py` — Registered Report model in Django admin
- `backend_python/api/security.py` — Password hashing, verification code hashing, URL validation, image upload validation, admin signature signing
- `backend_python/api/throttles.py` — AuthRateThrottle, VerificationRateThrottle
- `backend_python/api/migrations/0010_rename_api_edithistory_target_idx_...py` — Auto-generated RenameIndex operations (placeholder for server migration)
- `backend_python/api/migrations/0011_reply_count_and_index.py` — Adds `reply_count` field + `parent_reply_id/created_at` index
- `backend_python/api/migrations/0012_add_denormalized_user_counters.py` — Adds 7 counter fields to User model
- `backend_python/api/migrations/0013_backfill_user_counters.py` — Backfills counter data from aggregate queries
- `backend_python/nebians/settings.py` — Redis cache support via `CACHE_BACKEND`/`CACHE_LOCATION` env vars, `SESSION_ENGINE` auto-switch, `CONN_MAX_AGE=60`, `CONN_HEALTH_CHECKS=True`
- `backend_python/nebians/middleware.py` — SecurityHeadersMiddleware (CSP with `unsafe-eval`, Permissions-Policy, COOP)
- `backend_python/web/views.py` — Replaced all HTTP API calls with direct DB queries and `services.*` calls; admin views query DB directly; denormalized counters in `_build_local_stats()`, `_build_contributors_batch()`, profile views; `_clear_page_cache()` clears admin_stats/sitemap_xml; increased cache TTLs
- `backend_python/web/api_client.py` — Only used for session management now (`get_session_token`, `set_session_auth`, `clear_session_auth`). No data operations use HTTP anymore.
- `backend_python/requirements.txt` — Added `redis==5.2.1`
- `backend_python/web/templates/web/forum_post.html` — Three-dot menu on post/reply headers, bookmark/share buttons in action bars, `renderMarkdown()` JS for bold/italic/line-break rendering, `mention_links` template filter with markdown support
- `backend_python/web/templates/web/forum.html` — Three-dot menu on post cards (bookmark/share/report)
- `backend_python/web/templates/web/home.html` — Three-dot menu on forum activity items (bookmark/share)
- `backend_python/web/templates/web/search.html` — Three-dot menu on search result post cards
- `backend_python/api/models.py` — Added `Bookmark` model (user, target_type, target_id), `Reply.is_archived` field
- `backend_python/api/migrations/0016_bookmarks_and_reply_archive.py` — Creates `bookmarks` table (manual creation via mariadb CLI needed due to charset mismatch), adds `is_archived` to `replies`
- `backend_python/api/views.py` — Added `bookmark_toggle`, `bookmark_list`, `bookmark_check` API endpoints
- `backend_python/web/views.py` — Added `ajax_bookmark_toggle`, `ajax_bookmark_check`, `ajax_archive_reply`; `ajax_delete_post`/`ajax_delete_reply` now cascade-delete bookmarks, likes, edit history, reports, child replies; all serializers include `isBookmarked` field
- `backend_python/web/urls.py` — Added `/ajax/bookmark/toggle/`, `/ajax/bookmark/check/`, `/ajax/archive/reply/<id>/`
- `backend_python/api/urls.py` — Added `/api/bookmarks/toggle/`, `/api/bookmarks/`, `/api/bookmarks/check/`
- `backend_python/web/static/web/css/app.css` — Added `.more-btn`, `.more-menu`, `.more-menu-wrapper`, `.more-menu-item`, `.more-menu-divider`, `.bookmark-active` CSS components
- `backend_python/web/templatetags/web_extras.py` — `mention_links` filter now renders **bold**, *italic*, and line breaks

### Important Findings & Considerations for Other Agents

1. **Cache backend is now Redis** — `CACHE_BACKEND` and `CACHE_LOCATION` env vars control the cache backend. In production, Redis is used (`redis://127.0.0.1:6379/0`). In local dev without these env vars, it falls back to `LocMemCache`. Sessions also use Redis when configured (`SESSION_ENGINE=django.contrib.sessions.backends.cache`). Redis is auto-started via cPanel crontab.

2. **Auth token cache invalidation** — When a user changes their password (`auth_change_password`), their auth token is regenerated. The old token's cache entry (`auth_user:{old_token}` and `valid_token:{old_token}`) will linger for up to 5 minutes. This is acceptable because the old token is also invalidated in the DB. But if you need instant invalidation, add `cache.delete(f'auth_user:{old_token}')` and `cache.delete(f'valid_token:{old_token}')` in the password change handler.

3. **`_build_local_stats()` now uses denormalized counters** — When User counters are >0, it reads from the User model fields directly (0 queries). Falls back to aggregate queries for legacy rows where counters haven't been backfilled yet. Profile pages now do ~3 queries instead of ~12.

4. **`_build_contributors_batch()` uses denormalized counters** — Drops from ~10 aggregation queries to 1 User table scan. The leaderboard only shows `contribution_score`. If you need follower counts in the leaderboard, they're available via `follower_count`/`following_count` fields.

5. **Database indexes created by migration 0009** — These are B-tree indexes. MySQL's `__icontains` queries (LIKE '%term%') CANNOT use B-tree indexes — they always do a full table scan. For true full-text search, you'd need MySQL FULLTEXT indexes or a search service like Meilisearch. The current `icontains` approach is fine for <10k rows but will degrade with scale.

6. **CSP `script-src` includes `'unsafe-eval'`** — This was added because external PDF viewers (government PDF sites) use `eval()` internally. The `sandbox` attribute was also removed from the PDF iframe. If you want to re-harden CSP, you'd need to either proxy PDF content through your own server or use a PDF.js viewer that doesn't need eval.

7. **`CONN_MAX_AGE=60`** — This keeps MySQL connections alive for 60 seconds between requests. If LiteSpeed kills a worker after idle time, the connection may be stale. `CONN_HEALTH_CHECKS=True` handles this by checking connection health before reuse.

8. **Like toggle response uses computed count** — `post_like` and `reply_like` now compute `thumbs_up_count` locally (old value ± 1) instead of `refresh_from_db()`. This means if two users like simultaneously, the count is still correct because `F()` expressions are atomic in the DB. The locally computed value may be off by 1 for the non-winning request, but the DB value is always correct.

9. **Migration 0009 added 15 indexes** — On a large table, `CREATE INDEX` can lock the table for minutes. On the current small dataset (<1000 rows), this completed instantly. If you add indexes to large tables in the future, use `ALTER TABLE ... ALGORITHM=INPLACE` or create indexes concurrently in a separate migration.

10. **`user_profile_create_or_update` now uses DRF auth** — Previously it manually parsed the `Authorization: Bearer` header. Now it uses `_require_user()` which goes through `AuthTokenAuthentication`. This means the auth token cache applies to profile updates too. If a user's token is cached and they regenerate it (e.g., password change), they'll get 401 until the cache expires (5 min) or they re-login.

11. **Cleanup management command** — `python manage.py cleanup_stale_data` clears expired verification codes, stale FCM tokens (90+ days), old Django sessions (30+ days), and abandoned unverified accounts (365+ days). Run this via cron or manually. Use `--dry-run` to preview what would be deleted.

12. **The `Report` model is available but not integrated into the web UI** — The API endpoint `POST /api/reports/` exists, and admin endpoints exist at `/api/admin/reports/` and `/api/admin/reports/<id>/`, but there's no "Report" button in the web templates yet. An agent would need to add report buttons to forum posts, replies, and user profiles.

13. **`banner_url` is in the User model and serializer but not in the web edit_profile template** — The Android app can send `bannerUrl` in profile updates, but the web edit profile page doesn't have a banner URL field yet.

14. **Redis cache is persistent across LSAPI workers** — Unlike LocMemCache, Redis is shared between all LSAPI workers and persists across restarts. This means cached pages, auth tokens, and sessions survive worker respawns. However, Redis is configured without persistence (`--save ''` on manual start, but the crontab config has `save` directives). If Redis restarts, the cache will be empty but will regenerate.

15. **CRITICAL: Static files are served from TWO locations — do NOT change STATICFILES_STORAGE** — LiteSpeed/LSAPI serves static files from `public/static/`, but Django's `STATIC_ROOT` points to `staticfiles/`. These are DIFFERENT directories. The `CompressedManifestStaticFilesStorage` (WhiteNoise) generates hashed filenames (e.g., `app.7d01927028c0.css`) and a `staticfiles.json` manifest. **Never switch to `StaticFilesStorage`** — it will break the manifest, delete hashed files, and cause UI corruption.

16. **CRITICAL: How to deploy CSS/JS changes correctly** — After editing files in `web/static/`, you MUST do BOTH of these:
    - Run `python manage.py collectstatic --noinput` (writes to `staticfiles/`)
    - Manually copy changed files to `public/static/web/css/` and `public/static/web/js/`:
      ```bash
      cp /home/consicac/nebians_api/web/static/web/css/app.css /home/consicac/nebians_api/public/static/web/css/app.css
      cp /home/consicac/nebians_api/web/static/web/css/material3.css /home/consicac/nebians_api/public/static/web/css/material3.css
      ```
    - **Do NOT delete `.gz` files or hashed files from `public/static/`** — they are needed by the web server for compression and manifest-based serving.

17. **MySQL charset mismatch blocks FK creation** — The `users` table uses `latin1_swedish_ci` charset but new Django tables default to `utf8mb4`. FK constraints fail because charset/collation must match. To create a table referencing `users`, either use `SET FOREIGN_KEY_CHECKS=0` and create the table manually with `DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci`, or convert the `users` table to `utf8mb4` first. The `bookmarks` table (Migration 0016) was created manually via mariadb CLI for this reason.

18. **Unicode escapes in post content** — When updating post content via `manage.py shell` piped from PowerShell, Python unicode escapes (`\\u000A`, `\\u0027`) get stored as literal strings instead of actual characters. Always verify post content after shell-based updates. If literal escapes appear, fix with:
    ```python
    content = content.replace('\\u000A', '\n').replace('\\u0027', "'")
    ```

19. **Three-dot menu + Bookmark system (Migration 0016)** — Added `Bookmark` model (user, target_type, target_id) and `Reply.is_archived` field. All post/reply cards across home, forum, search, and forum_post pages now have a three-dot `more-btn` → `more-menu` dropdown. The menu is wrapped in `.more-menu-wrapper` for proper `position: absolute` containment. Menu options: Bookmark, Share, Report (non-author), Edit/Archive/Delete (author only). Bookmark toggle hits `/ajax/bookmark/toggle/`. Post/reply delete now cascades to bookmarks, likes, edit history, and child replies.

20. **Post delete cascade is thorough** — `ajax_delete_post` deletes: bookmarks for the post, bookmarks for all replies, PostLikes, ReplyLikes, EditHistory for post and replies, all replies, and the post itself. `ajax_delete_reply` deletes: bookmarks for the reply and its children, ReplyLikes, EditHistory, child replies, and the reply. Both use `transaction.atomic()`.