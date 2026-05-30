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

## Continuity Notes

### What Was Being Worked On (Last Session)
Improvement pass addressing 10+ edge cases and technical debt:
- Added `banner_url` field to User model with HTTPS URL validation (same as `photo_url`)
- Added `Report` model for content/user moderation (spam, abuse, inappropriate, misinformation, other)
- Added `POST /api/reports/` endpoint for authenticated users to submit reports
- Added admin report management: `GET /api/admin/reports/` and `GET/PATCH /api/admin/reports/<id>/`
- Fixed `user_profile_create_or_update` to use DRF authentication instead of manual Bearer header parsing
- Added rate limiting (`AuthRateThrottle`) to post creation, follow toggle, and FCM registration
- Added FCM token format validation (length 10-512)
- Filtered archived posts (`is_archived=True`) from public listings
- Added pagination to `search_all` endpoint (was hard-limited to 25 results)
- Removed dead code: `posts_list` and `replies_list` standalone endpoints (dispatchers handle both)
- Created `cleanup_stale_data` management command for expired verification codes, stale FCM tokens, old sessions, abandoned unverified accounts
- Migration 0008 adds `banner_url` field and `Report` model
- Improved test coverage: profile, posts, replies, follow, FCM, search, reports, email auth
- Registered `Report` model in Django admin

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
  - Password: `-0IQkyTlzLCAJdlyNdHrvA`
- **Django admin** (`/admin-django/`): Same credentials
- Create new superusers: `python manage.py createsuperuser`

### Key Files That Were Recently Modified
- `backend_python/api/models.py` — Added `banner_url` field to User, `Report` model, verification_code CharField(128)
- `backend_python/api/views.py` — Fixed auth on profile update, added Report endpoint, pagination on search, filtered archived posts, rate limiting on posts/follow/FCM, FCM token validation, removed dead endpoints
- `backend_python/api/serializers.py` — Added `banner_url` to UserSerializer/UserPublicSerializer, ReportSerializer
- `backend_python/api/admin_views.py` — Added admin report management endpoints, `banner_url` in user PATCH
- `backend_python/api/admin_urls.py` — Added report admin URL patterns
- `backend_python/api/admin.py` — Registered Report model in Django admin
- `backend_python/api/security.py` — Password hashing, verification code hashing, URL validation, image upload validation, admin signature signing
- `backend_python/api/throttles.py` — AuthRateThrottle, VerificationRateThrottle
- `backend_python/api/migrations/0008_banner_url_and_reports.py` — NEW: Adds banner_url field and Report model
- `backend_python/api/management/commands/cleanup_stale_data.py` — NEW: Management command for data cleanup
- `backend_python/api/test_security_hardening.py` — Expanded tests: profile, posts, replies, follow, FCM, search, reports, email auth
- `backend_python/nebians/settings.py` — Django 5.2, env_bool/env_list helpers, security settings, throttling config
- `backend_python/nebians/middleware.py` — SecurityHeadersMiddleware (CSP, Permissions-Policy, COOP)
- `backend_python/web/views.py` — `_get_valid_token()`, locked profile support, Django auth for admin
- `backend_python/web/api_client.py` — Admin calls use `internal_admin=True` for signed headers
- `backend_python/web/templates/base.html` — `IS_AUTHENTICATED` replaces `AUTH_TOKEN`, XSS helpers