# NEBians - Continuity Notes

**Last updated:** October 22, 2026

> **Android UI work lives in [`ANDROID_UI_CONTINUITY.md`](ANDROID_UI_CONTINUITY.md).** This file covers the Django/web side only.

---

## Current Status

### API speed pass + people suggestions endpoint (branch `perf/backend`, Oct 22, 2026)

Same responses, fewer queries; measured with `backend_python/scripts/perf_seed.py` (600 users,
4000 posts, 2600 resources, follows, notifications, news; fixed clock) and
`scripts/perf_probe.py` (every app endpoint, anonymous and Bearer; `--compare` diffs bodies).

- **New: `GET /api/users/suggestions/?limit=12`** (`api/people_suggestions.py`) replaces the ~43
  requests of the app's `PeopleSuggestionRepository`: followers, followees' followees (exact mutual
  counts), schoolmates, classmates (`map_profile_grade` spellings), recent forum authors; excludes
  self/followed/requested/locked/unverified/banned/bots; <= 9 queries. Signed out -> `{"results": []}`.
- **N+1s gone:** followers/following (53 -> 3), `users/me/analytics/` (109 -> 18 conditional
  aggregates), paid resource cards (`web.view_helpers.prefetch_resource_purchases`), resource
  detail like/bookmark, news detail related authors. Search and notifications no longer COUNT(*)
  (`api.view_helpers._page_rows`/`_page_results`, same 404 for bad pages).
- **Feed pools** are reused per process while their stamp matches the shared cache entry
  (`api/views_feed._candidate_pools`); decks get copies. `realtime/config` re-reads tunnel logs only
  when they change. No more write-only `auth_user:` cache SET per API call.
- **Migrations to apply:** `api 0149_perf_list_sort_indexes` (resource sort indexes replace
  `res_appr_lead_added_idx`/`_views_idx`, posts discussed, follows newest-first, users school/class)
  and `0150_perf_author_count_indexes`.
- **Budgets:** `api/test_api_query_budget.py`, `api/test_people_suggestions.py`, `api/test_feed_pools.py`.
- **Found, not fixed (behaviour):** `GET /api/resources/<id>/comments/` answers 400 "Content required"
  since 79720b2d dropped its `return Response({'comments': ...})`; `api/users/search/` does not exist
  (app @mentions get 404); the app's `news/` calls pay a 308 to `/app/news/`.

### Syllabus with the books' chapters; marketplace switched off (Oct 22, 2026)

Branch **`syllabus/revamp`**, based on `resources/grade8-10-polish-syllabus` (which carries the
polished Class 8 and 10 books and the v2 syllabus export). Pushed with
`task/tools/ghpush.py <repo> NikitHamal/NEB syllabus/revamp` (first push needed `--base`).

- **Marketplace off, code kept.** `nebians/features.py`: `MARKETPLACE_ENABLED` (env, default off)
  404s every marketplace page/ajax/API route (`marketplace_gate` in `web/urls.py`, `api/urls.py`),
  hides the Library shelf (`marketplace_enabled` in templates), `/api/app/features/` reports it.
  Android: `AppFeatures.MARKETPLACE = false` drops the tab and never builds `MarketplaceViewModel`.
  Paid resources (price on upload) are not the marketplace and are unchanged.
- **Chapters and question banks for Class 8, 10, 11, 12.** `notes/tools/export_study.py` reuses
  `notes/pipeline/md2html.py` with maths left as TeX (KaTeX on the client), media by content hash in
  `web/static/web/study/` (111 MB), documents in `web/data/study/<grade>-<subject>/`
  (`unit-NN.json`, `bank-NN.json`, `guide.json`, `index.json`). Answers fold into `<details class="ans">`;
  MCQs carry `data-key` from the book's key (Nepali paragraph questions too, `.mcq-p`). Re-run after
  any chapter changes: `python3 notes/tools/export_study.py [book ...]` (needs matplotlib, Pillow;
  ~25 min for all with 2 cores). `web/study_data.py` reads it for web and API.
- **Web.** `/app/syllabus/` hub (continue card, cross-class search into chapters), subject page
  (next/revise suggestions, tabs chapters / question bank / exam), reader at
  `/app/syllabus/<g>/<s>/unit-<n>/`, `bank-<n>/`, `exam-guide/` (`templates/web/syllabus/reader.html`,
  `css/pages/study-reader.css`, `js/study-reader.js`, KaTeX in `static/web/vendor/katex/`).
  Progress is on the device (`localStorage['neb.study.v1']`, `window.NebStudy` in `js/syllabus.js`);
  reading credit grows with time on the page (a quarter of the reading time minimum).
- **API.** `/api/syllabus/v2/<g>/<s>/` adds `read_min`, `has_chapter`, `banks`, `guide`;
  `.../unit/<n>/`, `.../bank/<n>/`, `.../guide/` return `{title, toc, html, prev, next, ...}`.
- **Android.** `SyllabusSubject.kt` rewritten (chapters, question bank, exam tabs; next/revise cards),
  `StudyReader.kt` (route `study/{grade}/{subject}/{kind}/{no}`, WebView + bundled KaTeX, JS bridge
  `NebStudy`), `data/repository/StudyProgress.kt` (same keys as the web). Not compiled locally:
  check the `Build Student Release APKs & AAB` run for the branch.
- **The old content.** Every grade/subject of 8/10/11/12 already redirects old subject pages and
  legacy APIs to the new syllabus, so the DB `SyllabusContent` English/Nepali rows are no longer
  shown anywhere (rows left in the database).
- **Content fixed.** `notes/content/qbank12/unit-04.md` held a stale copy of the Chemistry model
  sets on every branch; it is now *Physics: Model Question Sets and Predicted Questions* (two worked
  model papers, 39 ranked predicted questions) and `notes/pdf/NEBians-Question-Bank-Grade-12.pdf` is
  rebuilt (787 pages, same fonts as before).
- **Fonts before any build or export.** `notes/pipeline/fonts/install.sh`, plus `fonts-dejavu-core`
  for WeasyPrint's fallback glyphs and `libpango-1.0-0 libpangoft2-1.0-0` for WeasyPrint. Without
  them matplotlib and WeasyPrint fall back silently (Nepali figure labels turn into boxes);
  `export_study.py` now refuses to run if Inter or Noto Sans Devanagari is missing. After installing,
  clear `notes/figures/_fig/` (the figure cache is keyed by code, not by font).
- Tests: `web/test_syllabus.py` (reader pages, APIs, every subject has all chapters and a bank),
  `api/tests_marketplace.py` (runs with the switch on; one test checks it off).

### Interactive sims: performance + 3D revamp (DONE on branch, Oct 21, 2026)

Branch **`sims/perf-cosmos-3d`** (from `main` @ `49b20ab7`). Pushed through the GitHub connector
(`task/tools/ghpush.py <repo> NikitHamal/NEB <branch>`; git itself has no credentials here).

**Done and pushed**
- `core/engine.js`: drawing-buffer budget (2.6/1.6/0.9 MP by tier), MSAA only below 1.5x DPR,
  refresh-aware resolution governor that also climbs back (probe + backoff), 4-tap hardware-PCF
  shadow filter (was 17), shadow maps re-rendered only when a caster/light/geometry changes
  (`obj.userData.dynamicShadow` forces it; `createEngine({ shadowCache: false })` opts out),
  `stage.__engine` for tests.
- Atom Builder: orbital density baked into a 3D texture per configuration; 4-5x faster, same look.
- Heart & Lungs / Human Body: SDF organ meshing and skin growth run in module workers
  (`heartlungs/models-worker.js`, `anatomy/envelope-worker.js`), sync fallback.
- Butterfly / Photosynthesis: no MSAA canvas under the DOF pass.
- Scale of the Universe (`space/cosmos/`): shared single-scattering atmosphere (`shaders.js`
  `SCATTER`, `RA`) used by the globe (aerial perspective + limb sky) and the summit sky;
  `milky.js` (Milky Way in galactic coords); `climber-model.js` + `climber-worker.js` (SDF
  climber); `cloudsea.js` (cloud deck from the regional DEM); new Sun photosphere + corona in
  `solar.js`; deep galaxy field in `galaxy.js`; CMB only once outside it (`web.js`).
  Harness tip: focus fly-tos blend over 1.6 s of sim time; at SwiftShader fps wait ~40 s.
- Lifecycle of Stars is 3D (`space/star-lifecycle.js` + `space/stars3d/`), catalog `sim_type` 3d.

- 2D -> 3D done: space (orbital-sandbox, kepler-orbits, gravity-worlds, rocket-launch on
  `space/space3d/kit.js`), chemistry (density-tower, states-matter, melt-freeze, fizzy-reactions,
  acid-base, mixing-lab, reaction-balancer on `chemistry/chem3d/stage.js` + `particles.js`, using
  the hands-on glassware in `core/handson/glass.js`). Catalog `sim_type` updated (`3d` / `lab3d`).
  Each exposes a `stage.__<name>` debug hook for tests.
  Gotcha: `core/lite.js` turns transparent MeshPhysical with clearcoat > 0.5 and opacity < 0.75
  into near-invisible glass; liquids/ice use clearcoat 0.5.

- Physics 2D -> 3D done: pendulum-lab, optics-bench (now a builder: `createOpticsBench(stage,
  opts)`), circuit-lab, magnet-play on the lab bench (`chemistry/chem3d/stage.js`, `subject:
  'physics'`); projectile-motion, bouncy-balls, ramp-roller (three lanes), forces-playground,
  waves-lab on the outdoor field (`physics/physics3d/field.js`: grass, hills, scattering sky).
- Class 10 concave-mirror runs on the 3D optics bench.
- Regression: `task/harness/smoke.py sim...` loads each at 1440x900 and 390x844 and reports
  console errors; all converted sims load clean.

- Class 10 done in 3D: concave-mirror, indicators, food-tests, height-distance, ohms-law
  (`core/handson/circuit.js` meters need `update(dt)` every frame or the needles never move),
  quadratic-graph, statistics-explorer. No `'lab'` sim_type left in `catalog_neb_class10.py`.
- Robotics done in 3D on `core/robot-kit.js` `workshop()`: line-follower (`stage.__line`),
  pid-controller (`__pid`), state-machine (`__fsm`, DOCK now skirts furniture), robot-power
  (`__power`, DC motor with back-EMF). Wide screens: `fit()` in each frames the rig beside the
  ~310 px docked panel.

- AI done in 3D on `ai/ai3d/stage.js` (`createStudio`, `framer`, `slabCard`, `meshDrag`):
  what-is-ai (`__whatai`), how-ml-learns (`__ml`, probability landscape), perceptron (`__perc`,
  sum plane), image-classifier (`__digits`, pixel pillars), llm-intro (`__llm`), ethics
  (`__ethics`). Catalogs now have no `'2d'`/`'lab'` sims left; `coding/*` are code editors.
  `slabCard` draws in canvas pixels (fonts below ~1px vanish, never scale the context).

- Perf pass on the older 3D sims (SwiftShader, 1382x630, `prof.py`): solar-system 78 ms,
  earth-moon-sun 36, moon-phases 34, eclipses 56, milky-way 67, molecule-viewer 55, neuron 54,
  network-3d 79 — already light (the new 3D sims are 370-480 ms there, mostly env-map PBR on the
  full-screen floor, which SwiftShader overstates). Tried and reverted, no win: shrinking the
  Milky Way star sprites (33 -> 31 ms); the Lifecycle-of-Stars photosphere as the Sun in
  `core/space-kit.js` `sun()` (reads grey-white under these sims' exposure and loses the child
  label because the star group is scaled). Differential Drive's camera now follows the robot.

**Next**
- The list from the brief is done end to end. Candidates if more time: give the four old space
  sims their own exposure-matched Sun (needs label re-parenting + `noise: true` engines), and a
  real-device check of the AI studio / workshop floors on a low-end phone.

**Test harness** (`task/harness/`, served with `actl serve start 8765 --dir task/harness`):
`index.html?sim=<path>` mounts any sim without Django. Playwright venv at `/tmp/pw`
(`python3 -m venv /tmp/pw && /tmp/pw/bin/pip install playwright pillow && /tmp/pw/bin/playwright install chromium && sudo /tmp/pw/bin/playwright install-deps chromium`).
`shoot.py sim out.png [--phone] [--high] [--js EXPR] [--shot name]`, `prof.py sim [--high]` (per-object GPU ms
under SwiftShader, synchronous), `loadtime.py sim ms` (main-thread long tasks). SwiftShader overstates
texture-fetch cost; trust it for ALU-heavy shaders, triangle counts and pass counts.


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