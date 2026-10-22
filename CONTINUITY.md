# NEBians - Continuity Notes

**Last updated:** October 21, 2026

> **Android UI work lives in [`ANDROID_UI_CONTINUITY.md`](ANDROID_UI_CONTINUITY.md).** This file covers the Django/web side only.

---

## Current Status

### Explainer lesson videos (branch `videos/explainers`, Oct 21, 2026)

Pipeline and rules: `tools/lessons/README.md`, `tools/lessons/AUTHORING.md`. Scripts are code-only; the owner renders
full videos locally (`python3 build.py scripts/<book>/unit_NN.py`). Agents only render cheap contact sheets with
`frames.py` and commit scripts + synthesised narration (`.cache/tts`). Push with `python3 tools/lessons/push.py push "msg" files…`
(git push is read-only from agent pods). Never delete other agents' commits on this branch (festival video/photo work included).

| Book | Status |
|---|---|
| phy12 | units 1–15 scripted, narrated, frame-checked |
| chem12 | units 1–12 scripted, narrated, frame-checked |
| bio12 | units 1–10 all scripted, narrated, frame-checked (helpers `_bio.py`, `_phys2.py`, `_gen.py`, `_emb.py`, `_hum.py`) |
| math12 | units 1–3 pushed (helpers `_m.py`); 4–6 scripted, in frame review; 7–17 to do |
| then | eng12? (English-medium only), cs12 → class 11 → class 10 → class 8. Skip Nepali-medium books (nep, soc, health) for now: TTS is poor |

- `scripts/bio12/_bio.py` is the biology drawing kit: one colour per tissue (XYL, PHL, CAMB, CORK, SCL, COL, PAR…), tissues
  (parenchyma/collenchyma/sclerenchyma/meristem), conducting elements, `RootTS`, `DicotStemTS`, `MonocotStemTS`,
  `DicotLeafTS`, `MonocotLeafTS`, `Flow` (moving dots), `Captions` (single caption slot — use it instead of stacking labels).
- Do not use `.set_opacity(1)` to un-dim groups that contain stroke-only circles: it fills them with Manim's default red.
  Use `save_state()` + `fade()` + `Restore`.
- A CPU box (molab marimo kernel, 20 cores) may be used for frame checks; it is shared with a festival-reel agent, so run
  renders under `nice` with at most a few parallel jobs.
- Next step if interrupted: math12 — review unit_04 (Sequence and Series), unit_05 (Matrices), unit_06 (Triangle) sheets, push each with `ttskeys.py` file lists, then unit_07 Solution of Triangles … unit_17 (notes/content/math12/unit-NN.md); then eng12, cs12; then class 11.
- `python3 tools/lessons/ttskeys.py <script>` (from the repo root) dry-runs a lesson and prints exactly the `.cache/tts` files it uses: push those with the unit.
- Kit: `recap` now slides a long list left so Neby never covers the last line.
- Molab box workflow: `/root/neb` clone + `/root/neb/venv`; `render.sh <script> "parts"` runs prefetch then frames.py with xargs -P 4 under nice; unset the kernel's PYTHONPATH/VIRTUAL_ENV first (they leak from marimo).
- Notes errata found so far: bio12 unit-03 'lethal genes give 2 green : 1 white-carrier' is wrong (white seedlings die; survivors 1 GG : 2 Gg, all green; the 2 : 1 phenotypic ratio is the dominant-lethal yellow mouse).

### Landing page, /app, site themes, query budgets, self-hosted fonts (Oct 18, 2026)

- **`/` is a standalone landing page** (`web/views_landing.py`, `templates/landing/landing.html`,
  `static/web/css/landing.css`, `static/web/js/landing.js`). It does not load material3.css or
  the app shell. The app lives under **`/app/`** (`/app/library/`, `/app/forum/`, ...). Old page
  URLs answer **308** to the `/app/` equivalent via `views_landing.legacy_redirect` (method and
  query kept). `ajax/`, `api/`, `auth/`, `login/`, legal pages, sitemap and robots stay at the root.
- **Site themes replace the hero background SVGs.** `web/site_themes.py` owns the themes
  (everyday, dashain, tihar, holi, new-year, monsoon, winter, exams): CSS tokens, decor,
  greeting. Admins force or schedule one at `/admin/themes/` (`SiteTheme` model, migration
  0146). `resolve()` picks forced > scheduled window (Kathmandu date) > everyday; cached 300 s,
  `invalidate()` on save. Context processor `web.site_themes.context`.
- **Query budgets** (`web/test_query_budget.py`) pin forum, leaderboard, search, resources and
  the suggested feed. Helpers: `api.services.AVATAR_FIELDS`, `web.view_helpers._request_db_user`,
  `api.view_helpers.prime_for_serializers`. Probe: `backend_python/scratch/perf_probe.py`.
- **Fonts are self-hosted** (`static/web/css/fonts.css`, `static/web/fonts/app/`). The icon font
  is a **subset**: an icon not in `fonts/app/material-symbols-outlined.txt` renders as its name.
  `web/test_icon_font.py` catches literal names; after adding an icon run
  `python scripts/build_icon_font.py` (needs fonttools + brotli). Admin, coding-agent and
  background-agent templates still use Google's full font.

### Creator page themes, templates and the rebuilt studio (COMPLETE, Sep 28, 2026)

The first storefronts worked but looked the same as each other and the builder
was hostile on a phone (issue #52). This pass gave a creator something to
actually design with, on both surfaces.

- **A style vocabulary, decided once.** `api/creator_themes.py` owns every
  choice a creator can make -- palettes, colour schemes, hero treatments, fonts,
  page textures, card styles, corner radii, densities, page widths, and the
  per-section tone/align/width sets -- and `theme_vocabulary()` is what both
  clients build their controls from. The server *resolves* the palette to eight
  hex values and ships them; neither client owns a colour table, because the day
  one hex is nudged in Python is the day the same page looks different on a
  phone.
- **Ten templates.** `api/creator_templates.py` + `apply_template(page,
  template_id, mode)` with three modes: `page` (look and sections), `theme`
  (look only), `sections` (structure only). `page`/`theme` also move
  `accent_hex` onto the new palette's accent, so a palette change never leaves
  a teal card in front of a violet page.
- **Fifteen new section types** on top of the original ten: `pricing`, `video`,
  `team`, `logos`, `timeline`, `steps`, `quote`, `banner`, `richtext`,
  `divider` and friends. Each one is described by `api/creator_pages_schema.py`
  (`editor_schema`), so a section added on the server is editable in both
  studios with no client change.
- **Per-section settings.** `tone` (plain/soft/accent/contrast), `align`,
  `width` and `columns`, sanitized in `creator_pages_sanitize.py`. Note the
  sanitizer drops any value equal to its default -- both clients mirror that
  when they build their payloads.
- **CSS.** Two new partials, `pages/marketplace/theme.css` (the `--creator-*`
  custom properties and the `.mkt-font-*` / `.mkt-tone-*` / pattern classes) and
  `pages/marketplace/sections.css` (the fifteen new sections). Remember the
  bundle: edit the partial, list it in `pages/marketplace.src.css`, then run
  `python3 ../tools/css/bundle.py` from `backend_python/`.
- **Web studio.** `static/web/js/marketplace_studio_look.js` adds the template
  gallery with live silhouette thumbnails, the look controls, and the
  drag-to-reorder section list.

**Two rules that will bite whoever touches this next:**
1. `style` is replaced **wholesale** on save -- a client that cannot carry a key
   silently erases it. The Kotlin `savePage()` sends all thirteen.
2. `resource_ids` treats an empty list as "detach all", unlike every other
   field, where an absent key means "leave alone" (`_has()` in
   `creator_pages.py`).

**Still to do:** apply `0145_creator_page_layouts` on the server and re-run
`collectstatic`.

**Verified by** `python3 manage.py test api.tests_marketplace` -- now 72 tests
over six classes; `CreatorThemeTests` covers the vocabulary, template
application in all three modes, and section sanitizing.

---

### Creator Marketplace + paid notes, end to end (COMPLETE, Sep 27, 2026)
- **Backend.** New `CreatorPage` / `CreatorCourse` / `CreatorCourseResource` /
  `CreatorPost` models (migration `0143_creator_marketplace_pages_courses_posts`),
  a shared data layer in `api/creator_pages.py`, and a REST surface in
  `api/views_marketplace.py`: creators list, creator detail, course detail,
  the course shelf, `marketplace/me/*` for the owner, and `marketplace/dashboard/`.
- **Buying a course** reuses the resource checkout: `PaymentVerification` now
  carries a nullable `course` next to a now-nullable `resource`, and
  `api/marketplace.record_purchase()` writes one pending row per (buyer, target).
- **Commission** is read from `PaymentConfig` (default 2.5%) everywhere. The
  hardcoded 10% in `views_resources.resource_purchase` and in
  `web/views_public.submit_payment_proof` was wrong and is gone.
- **Web.** `/marketplace/` directory, `/marketplace/<slug>/` storefront rendered
  from the owner's blocks, `/marketplace/course/<id>/` with the QR checkout, and
  `/marketplace/studio/` for the owner. The library page gained a **Marketplace
  tab between Library and Syllabus** (`?tab=marketplace`).
- **App.** The same tab in `LibraryScreen.kt`, plus storefront, course and
  studio screens under `ui/screens/marketplace/` and
  `data/repository/MarketplaceRepository.kt`.
- **One price control, both platforms.** `_price_setter.html` +
  `static/web/js/marketplace_price.js` on the web, `ui/components/NebPriceField.kt` in
  the app: free/paid with the consequence written under each answer, price
  presets, and a live "you receive Rs. X after the Y% fee" line. Used by
  upload, edit-resource and the studio's course form.

**Bugs found and fixed while wiring this up (all in the paid-content path):**
1. `_notif.create_notification` was called by the admin panel but **did not
   exist** — every payment approval/rejection raised `AttributeError` after the
   seller had been credited, so the admin saw a 500 and the buyer was never
   notified. Added (object → `target_type`/`target_id` mapping).
2. The admin payment queue and template assumed `payment.resource` was always
   set, so a course purchase would break the queue
   (`{% url 'web:reader' resource_id=None %}`). Both are course-aware now.
3. `api/realtime._send` resolved the channel layer **outside** its try/except:
   a broken Redis layer turned a successful write into a 500. Resolving is part
   of the attempt now.
4. `web/views_admin.admin_pending_payments` credited the wallet by hand —
   balance only, no Nebians points, no `total_spent`. It calls
   `marketplace.grant_purchase_rewards()` now.

**Still to do:** apply `0143` on the server and `collectstatic` (the new pages
ship CSS + JS). The pre-existing `botconfig.system_prompt` model/migration drift
is untouched; `makemigrations` will still offer `0144` for it.

**Verified by** `python3 manage.py test api.tests_marketplace` — these four of
the six classes (creator-page API, courses and checkout, web pages + studio, and
the admin payment queue). Run it with `DEBUG=True DB_ENGINE=sqlite`; see the
Marketplace section of AGENTS.md for the command and what each class covers.


### Google Sign-In Migration (IN PROGRESS)
- **Status:** GIS button renders, but "origin not allowed" error from Google
- **What was done:**
  - Removed Firebase Auth (`signInWithRedirect`, `signInWithPopup`) from `login.html`
  - Replaced with Google Identity Services (GIS) using `google.accounts.id.initialize()` + `renderButton()`
  - Updated `views.py` to pass `google_client_id` instead of 6 Firebase config vars
  - Updated `authentication.py` to verify tokens against both `GOOGLE_CLIENT_ID` and `FIREBASE_PROJECT_ID`
  - Updated `.env` on server with correct `GOOGLE_CLIENT_ID`
  - Fixed `settings.py` to use `load_dotenv(override=True)` so `.env` values take effect
  - Rewrote `login.html` JS to use `.then()` callbacks (no `async/await`) to avoid syntax errors
  - Added all helper functions back (`showPanel`, `togglePassword`, `handleEmailLogin`, etc.)
- **What's blocked:**
  - Google returns "origin not allowed" error for client ID `68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com`
  - This client ID was created on May 30, 2026 — new OAuth clients can take hours to propagate
  - Authorized JavaScript origins ARE configured correctly in Google Cloud Console
  - OAuth consent screen IS in Production mode
- **How to test:**
  1. Go to `https://nebians.consica.com.np/login/` or `http://localhost:8000/login/`
  2. The Google "Continue with Google" button should render via GIS
  3. If Google still says "origin not allowed", wait a few more hours or verify the Google Cloud Console settings
  4. Check server logs: `ssh ... consicac@192.250.235.158 "grep -i 'auth\|google\|token' /home/consicac/nebians_api/logs/nebians.log | tail -20"`

### Light Mode Hover Fix (COMPLETE)
- Text buttons, outlined buttons, auth buttons in light mode had solid blue hover backgrounds
- Changed from `var(--md-primary-container)` (#2563EB) to `rgba(0, 74, 198, 0.08)` across:
  - `material3.css`: `.md-btn-text:hover`, `.md-btn-outlined:hover`
  - `app.css`: `.auth-text-btn:hover`, `.auth-link-btn:hover`

---

## Key Configuration Values

### Server
- **Host:** 192.250.235.158
- **User:** consicac
- **Project Dir:** /home/consicac/nebians_api/
- **Virtualenv:** /home/consicac/virtualenv/nebians_api/3.13/
- **Web Server:** Phusion Passenger (NOT gunicorn)
- **Restart:** `touch tmp/restart.txt` (NOT gunicorn restart)
- **Log:** `/home/consicac/nebians_api/logs/nebians.log`

### OAuth / Auth
- **Google OAuth Client ID:** `68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com`
- **Firebase Project ID:** `nebiansnepal`
- **Firebase Web App ID:** `1:68143624035:web:f04129d04b128b92e4ed56`
- **Firebase Sender ID:** `68143624035`

### .env on Server (as of May 30, 2026)
```
DEBUG=True
SECRET_KEY=local-dev-key-change-in-production
DB_ENGINE=mysql
GOOGLE_CLIENT_ID=68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com
WEB_API_BASE_URL=https://nebians.consica.com.np/api
ALLOWED_HOSTS=nebians.consica.com.np,www.nebians.consica.com.np,localhost,127.0.0.1
```

---

## Things That Broke Before & How They Were Fixed

### 1. Firebase `redirect_uri_mismatch`
- **Cause:** Firebase Auth uses `signInWithRedirect` which requires redirect URIs configured in Firebase Console
- **Fix:** Replaced Firebase Auth with Google Identity Services (GIS) popup-based flow — no redirect URIs needed

### 2. GIS `initTokenClient` returned access_token, not ID token
- **Cause:** `initTokenClient()` returns OAuth access tokens, not JWT ID tokens
- **Fix:** Switched to `google.accounts.id.initialize()` + `renderButton()` which returns `response.credential` (JWT)

### 3. GIS "called multiple times" warning
- **Cause:** `initialize()` was called on page load AND on button click
- **Fix:** Only call `initialize()` once during `window.load` event

### 4. FedCM errors and "signal is aborted"
- **Cause:** Using `google.accounts.id.prompt()` triggers FedCM which has compatibility issues
- **Fix:** Removed `prompt()`, only use `renderButton()` for the button

### 5. `handleCredentialResponse` not found / "callback is not a function"
- **Cause:** GIS HTML `data-callback` attribute couldn't find the function, and `g_id_onload` HTML attribute conflicted with JS initialize
- **Fix:** Removed `g_id_onload` div, only use JS-based `initialize()` with `callback: handleCredentialResponse`

### 6. `await` syntax error in non-async function
- **Cause:** `handleCredentialResponse` called `await sendTokenToBackend()` but wasn't declared `async`
- **Fix:** Rewrote all auth JS using `.then()` callback pattern instead of `async/await`

### 7. `showPanel is not a function`
- **Cause:** During multiple edits, the `showPanel`, `togglePassword`, and email auth functions were accidentally deleted from the script block
- **Fix:** Rewrote entire `login.html` from scratch with all functions present

### 8. `.env` overriding `settings.py` with old values
- **Cause:** `load_dotenv()` without `override=True` doesn't override existing env vars. The `.env` on the server had the old `GOOGLE_CLIENT_ID` which took precedence over the new default in `settings.py`
- **Fix:** Changed to `load_dotenv(BASE_DIR / '.env', override=True)` and updated the `.env` file on the server

### 9. Passenger not picking up `.env` changes
- **Cause:** Phusion Passenger caches environment variables. `touch tmp/restart.txt` restarts the app but may use cached env
- **Fix:** Had to update `.env` file content AND use `override=True` in `load_dotenv()`. For stubborn cases, kill Passenger processes and let them respawn

### 10. `ALLOWED_HOSTS` missing `www` subdomain
- **Cause:** Server logs showed `Invalid HTTP_HOST header: 'www.nebians.consica.com.np'`
- **Fix:** Added `www.nebians.consica.com.np` to `ALLOWED_HOSTS` in both `settings.py` default and `.env`

---

## Deployment Checklist

When deploying changes to the backend:
1. SCP changed files to `/home/consicac/nebians_api/`
2. If you changed `settings.py` or `.env`, ALSO update the `.env` file on the server manually
3. Run: `collectstatic --noinput && migrate && touch tmp/restart.txt`
4. Verify by checking logs: `tail -20 /home/consicac/nebians_api/logs/nebians.log`
5. If auth changes, test login at `/login/`
6. If CSS changes, `collectstatic` is required (Passenger serves static files from `staticfiles/`)

### Quick Deploy Commands (PowerShell)
```powershell
$sshKey = "$env:TEMP\nebians_deploy_key.pem"
# Fix permissions (run once per session)
icacls $sshKey /inheritance:r /grant "${env:USERNAME}:R"

# Deploy a single file
scp -o StrictHostKeyChecking=no -i $sshKey "LOCAL_FILE" consicac@192.250.235.158:/home/consicac/nebians_api/REMOTE_PATH

# Full deploy
ssh -o StrictHostKeyChecking=no -i $sshKey consicac@192.250.235.158 "cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python manage.py collectstatic --noinput && python manage.py migrate && rm -rf tmp/* && touch tmp/restart.txt && echo 'DONE'"
```

---

## What NOT to Do

1. **NEVER use `signInWithRedirect` or `signInWithPopup` from Firebase Auth** — causes redirect_uri_mismatch
2. **NEVER use `google.accounts.oauth2.initTokenClient()`** — returns access tokens, not ID tokens
3. **NEVER use `google.accounts.id.prompt()`** — causes FedCM errors
4. **NEVER call `google.accounts.id.initialize()` more than once** — causes "called multiple times" warnings
5. **NEVER use `async/await` in GIS callback handlers** — use `.then()` pattern instead
6. **NEVER start/stop gunicorn** — server uses Phusion Passenger
7. **NEVER forget to update `.env` on server** — it overrides `settings.py` defaults
8. **NEVER forget `collectstatic --noinput`** — static files won't update without it
9. **NEVER use `var(--md-primary-container)` for hover backgrounds in light mode** — it's too saturated (#2563EB). Use `rgba(0, 74, 198, 0.08)` instead