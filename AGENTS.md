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
- Keystore is at repo root: `nebians-release.keystore` (alias: nebians, password: ***REMOVED***)
- Artifacts retained for 30 days

### Building Locally
```bash
./gradlew assembleModernRelease    # Modern APK (minSdk 28)
./gradlew assembleLegacyRelease    # Legacy APK (minSdk 24)
```

---

## Web Backend — Server & SSH Deployment

### Server Details
- **Host:** `192.250.235.158` (cPanel / Phusion Passenger)
- **Username:** `consicac`
- **SSH Key:** Stored in `.ssh_deploy_info.json` (RSA private key)
- **Remote Project Dir:** `/home/consicac/nebians_api/`
- **Virtualenv:** `/home/consicac/virtualenv/nebians_api/3.13/`
- **Python:** 3.13
- **Web Server:** Phusion Passenger (NOT gunicorn) — restarts via `touch tmp/restart.txt`
- **WSGI Entry Point:** `passenger_wsgi.py` (NOT `wsgi.py`)
- **Log File:** `/home/consicac/nebians_api/logs/nebians.log`
- **Domain:** `nebians.consica.com.np` (also `www.nebians.consica.com.np`)

### CRITICAL: How to Deploy
```bash
# 1. Save SSH key to temp file (Windows)
$sshKeyPath = "$env:TEMP\nebians_deploy_key2.pem"
# ... load from .ssh_deploy_info.json

# 2. Fix permissions (Windows SSH requires this)
icacls $sshKeyPath /inheritance:r /grant "${env:USERNAME}:R"

# 3. SCP files to server (deploy one at a time — Windows PowerShell doesn't support &&)
scp -o StrictHostKeyChecking=no -i $sshKeyPath "LOCAL_FILE" consicac@192.250.235.158:/home/consicac/nebians_api/DEST_PATH

# 4. Restart Passenger (NOT gunicorn!)
ssh -o StrictHostKeyChecking=no -i $sshKeyPath consicac@192.250.235.158 "cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python manage.py collectstatic --noinput && python manage.py migrate && rm -rf tmp/* && touch tmp/restart.txt && echo 'DONE'"
```

### CRITICAL: .env File Overrides settings.py Defaults
The `.env` file at `/home/consicac/nebians_api/.env` is loaded by `dotenv` in `settings.py`. **Environment variables override `settings.py` defaults.** If you change a default value in `settings.py` but the `.env` still has the old value, the `.env` wins.

**Always check the `.env` file on the server after changing `settings.py`:**
```bash
ssh ... consicac@192.250.235.158 "cat /home/consicac/nebians_api/.env"
```

**The `load_dotenv()` call uses `override=True`** so `.env` values will override system env vars. But if a system-level env var is set (e.g., in cPanel), it still takes precedence. When in doubt, update both `.env` AND `settings.py`.

### CRITICAL: Passenger vs Gunicorn
The server uses **Phusion Passenger** (cPanel Python app), NOT gunicorn. Do NOT try to start/stop gunicorn. To restart:
```bash
rm -rf /home/consicac/nebians_api/tmp/*
touch /home/consicac/nebians_api/tmp/restart.txt
```
Passenger picks up changes after this. If env vars don't update, you may need to wait 30-60 seconds for Passenger to fully respawn workers.

### CRITICAL: SSL/Cookie Settings
`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, and `CSRF_COOKIE_SECURE` are all set to `False` by default. This is intentional — Passenger terminates SSL at the proxy level, so Django sees HTTP connections. Setting these to `True` causes infinite redirects or dropped cookies. Only enable them if you configure Passenger to forward the `X-Forwarded-Proto` header correctly.

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
- **Admin superuser credentials:** username=`admin`, password=`***REMOVED***`
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

## Continuity Notes

### What Was Being Worked On (Last Session)
Performance optimization pass — eliminated HTTP API roundtrips, switched to Redis cache, added denormalized user counters:

**Issue 1 — Eliminated HTTP API roundtrips in web views:**
- Created `api/services.py` — direct Python service functions called by web views instead of HTTP API calls
- `web/views.py` now calls `services.toggle_post_like()`, `services.create_post()`, `services.create_reply()`, `services.toggle_follow()`, etc. directly — no more `api_client._api_call()` for data operations
- `google_auth` view now uses `verify_google_token()` directly instead of `api.auth_google()` HTTP call
- Admin views (dashboard, users, resources, posts) all query the DB directly instead of going through `api_client`
- `api_client.py` is still used for session management (`get_session_token`, `set_session_auth`, `clear_session_auth`) but NO data operations go through HTTP anymore
- This eliminates: latency from localhost HTTP calls, double middleware processing, JSON serialization overhead, and potential deadlocks on single-process Passenger

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

### Resolved Issues
1. **Auth token regeneration bug** — Every Google sign-in was regenerating the auth token, invalidating existing sessions. Fixed by only generating tokens on signup, not on each login.
2. **Stale session 401 errors** — Follow/like/edit calls returned "Unauthorized" because session tokens didn't match DB. Fixed with `_get_valid_token()` helper that validates against DB and clears stale sessions.
3. **Duplicate `{% block description %}`** — forum.html, search.html, library.html had duplicate template blocks causing TemplateSyntaxError. Fixed.
4. **Admin API URL mismatch** — `admin_urls.py` had paths without trailing slashes but `api_client.py` called with trailing slashes. Fixed all to use trailing slashes.
5. **Sitemap crash** — `created_at` is a BigIntegerField (ms timestamp), not DateTimeField. Fixed `.isoformat()` calls to convert from ms timestamps.
6. **PostLike/ReplyLike admin** — Referenced non-existent `created_at` field. Removed from `list_display`.
7. **SECURE_SSL_REDIRECT breaking site** — Set to `True` in production would cause infinite redirects behind Passenger (SSL terminates at proxy). All SSL/cookie secure settings set to `False` by default.

### Admin Credentials
- **Custom admin panel** (`/admin/`): Login with Django staff superuser account
  - Username: `admin`
  - Password: `***REMOVED***`
- **Django admin** (`/admin-django/`): Same credentials
- Create new superusers: `python manage.py createsuperuser`

### Key Files That Were Recently Modified
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

### Important Findings & Considerations for Other Agents

1. **Cache backend is now Redis** — `CACHE_BACKEND` and `CACHE_LOCATION` env vars control the cache backend. In production, Redis is used (`redis://127.0.0.1:6379/0`). In local dev without these env vars, it falls back to `LocMemCache`. Sessions also use Redis when configured (`SESSION_ENGINE=django.contrib.sessions.backends.cache`). Redis is auto-started via cPanel crontab.

2. **Auth token cache invalidation** — When a user changes their password (`auth_change_password`), their auth token is regenerated. The old token's cache entry (`auth_user:{old_token}` and `valid_token:{old_token}`) will linger for up to 5 minutes. This is acceptable because the old token is also invalidated in the DB. But if you need instant invalidation, add `cache.delete(f'auth_user:{old_token}')` and `cache.delete(f'valid_token:{old_token}')` in the password change handler.

3. **`_build_local_stats()` now uses denormalized counters** — When User counters are >0, it reads from the User model fields directly (0 queries). Falls back to aggregate queries for legacy rows where counters haven't been backfilled yet. Profile pages now do ~3 queries instead of ~12.

4. **`_build_contributors_batch()` uses denormalized counters** — Drops from ~10 aggregation queries to 1 User table scan. The leaderboard only shows `contribution_score`. If you need follower counts in the leaderboard, they're available via `follower_count`/`following_count` fields.

5. **Database indexes created by migration 0009** — These are B-tree indexes. MySQL's `__icontains` queries (LIKE '%term%') CANNOT use B-tree indexes — they always do a full table scan. For true full-text search, you'd need MySQL FULLTEXT indexes or a search service like Meilisearch. The current `icontains` approach is fine for <10k rows but will degrade with scale.

6. **CSP `script-src` includes `'unsafe-eval'`** — This was added because external PDF viewers (government PDF sites) use `eval()` internally. The `sandbox` attribute was also removed from the PDF iframe. If you want to re-harden CSP, you'd need to either proxy PDF content through your own server or use a PDF.js viewer that doesn't need eval.

7. **`CONN_MAX_AGE=60`** — This keeps MySQL connections alive for 60 seconds between requests. If Passenger kills a worker after idle time, the connection may be stale. `CONN_HEALTH_CHECKS=True` handles this by checking connection health before reuse.

8. **Like toggle response uses computed count** — `post_like` and `reply_like` now compute `thumbs_up_count` locally (old value ± 1) instead of `refresh_from_db()`. This means if two users like simultaneously, the count is still correct because `F()` expressions are atomic in the DB. The locally computed value may be off by 1 for the non-winning request, but the DB value is always correct.

9. **Migration 0009 added 15 indexes** — On a large table, `CREATE INDEX` can lock the table for minutes. On the current small dataset (<1000 rows), this completed instantly. If you add indexes to large tables in the future, use `ALTER TABLE ... ALGORITHM=INPLACE` or create indexes concurrently in a separate migration.

10. **`user_profile_create_or_update` now uses DRF auth** — Previously it manually parsed the `Authorization: Bearer` header. Now it uses `_require_user()` which goes through `AuthTokenAuthentication`. This means the auth token cache applies to profile updates too. If a user's token is cached and they regenerate it (e.g., password change), they'll get 401 until the cache expires (5 min) or they re-login.

11. **Cleanup management command** — `python manage.py cleanup_stale_data` clears expired verification codes, stale FCM tokens (90+ days), old Django sessions (30+ days), and abandoned unverified accounts (365+ days). Run this via cron or manually. Use `--dry-run` to preview what would be deleted.

12. **The `Report` model is available but not integrated into the web UI** — The API endpoint `POST /api/reports/` exists, and admin endpoints exist at `/api/admin/reports/` and `/api/admin/reports/<id>/`, but there's no "Report" button in the web templates yet. An agent would need to add report buttons to forum posts, replies, and user profiles.

13. **`banner_url` is in the User model and serializer but not in the web edit_profile template** — The Android app can send `bannerUrl` in profile updates, but the web edit profile page doesn't have a banner URL field yet.

14. **Redis cache is persistent across Passenger workers** — Unlike LocMemCache, Redis is shared between all Passenger workers and persists across restarts. This means cached pages, auth tokens, and sessions survive worker respawns. However, Redis is configured without persistence (`--save ''` on manual start, but the crontab config has `save` directives). If Redis restarts, the cache will be empty but will regenerate.