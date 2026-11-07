# Notifications and analytics: status

Single status doc for the autopilot / push console / resource analytics task. Read it first, update it in place.
Earlier shipped work is described in `PUSH_AUTOPILOT_STATUS.md` (engine, reach tables, Android insights); this file tracks what this task added on top.
Design rules: M3 Expressive, no shadows, no emoji, no gradients, no backgrounds on role badges, no helper text.

## Found already shipped (do not rebuild)

* `PushCampaign`, `PushDelivery`, `PushSettings`, `ResourceAlert` (`api/models.py`), `api/push_engine.py`, `api/push_audience.py`, `api/resource_alerts.py`.
* Smart coalescing: autopilot settles for N quiet minutes, then one digest per person per round; daily cap per person; quiet hours; opt-out `User.notify_new_resources` (default True) on web Settings and Android Settings, API `GET/PATCH /api/me/notification-prefs/`.
* Resources that predate the autopilot have no `ResourceAlert` row, so the 92 earlier uploads are never auto-fired.
* Open tracking: inbox open (web) via `mark_opened`, push tap (Android) via `POST /api/push/opened/`, resource open with `?src=push` marks the delivery clicked. First open wins (deduplicated).
* Resource reach: `ResourceReach` one row per viewer per local day, `ResourceImpression`, `api/resource_insights.py`, web sheet `resource-insights.js`, Android `ResourceInsightsScreen`.

## Milestone 1: autopilot and opt-out

Done this task:

* `resource_alerts.announce_unnotified()` and `unannounced_ids()`: one tap batch over every live, never announced resource (digest per person, no cap, no quiet hours).
* Admin Push > Autopilot: "Announce unnotified library uploads" card with confirm dialog (`action=announce_unnotified`).
* Digest copy names the level: "6 new Physics resources added for Class 12".
* Tests: `api.test_push_autopilot` (batch announce, digest title, backlog never auto sent).

## Milestone 2: console and history

Done this task:

* Compose (`admin_panel/push_notifications.html`, `js/admin-push.js`): audience modes All users, Class or level, Subject, Platform (Android app / Web only), Unnotified library. Hidden mode fields are disabled so they are never sent; live recipient tiles (people, Android, web only) update on every change; the unnotified mode shows the unannounced resource count and a sample digest, and its button reads Announce. No inline styles, no helper text.
* Trigger labels: `manual` Manual Admin, `library` Batch Digest, `autopilot` Autopilot Library (`push_stats.KIND_LABEL`).
* History (`push_history.html`): per campaign time, trigger, target class and subject, targeted, sent, delivered, failed, opened, clicked, CTR, resource views, status. Numbers come from `push_stats.rollup()` over `PushDelivery` rows. Sent = push or inbox row handed over, delivered = push accepted or inbox row present, CTR = clicked over delivered, views = notification-surface opens of the campaign's resources after it started.
* Tracking: Android tap `POST /api/push/opened/`; web inbox read marks opened; web inbox links for campaign rows now carry `?src=push` so the resource open counts as a notification view and marks the delivery clicked. Opens and clicks are first-write-wins per person.
* Tests: `web.test_admin_push_pages` (modes, platform split, batch, history, source link).

## Milestone 3: resource analytics

Done this task:

* Android sends library list impressions (`POST /api/resources/impressions/`) from the Library grid: `ui/components/PostReach.kt` has one shared batcher
  (`collectImpressions`, an id counts once per list session and only if still on screen after 1.2 s) behind `TrackPostImpressions` (feeds) and the new
  `TrackGridImpressions` (library). `LibraryViewModel.reportImpressions` to `ResourceRepository.reportImpressions`. This closes the open item in
  `PUSH_AUTOPILOT_STATUS.md`: the uploader's "Seen in lists" and the list-to-open funnel now include app traffic.
* Admin push history: axis end label fixed (it printed a raw dict), target column no longer wraps; autopilot rules lost a helper line.
* Visual check: admin Compose, History and Autopilot rendered with seeded data in light (1366) and dark (420) widths, no shadows, no emoji, no gradients.
* Not built locally (Android): the GitHub Actions run is the check.

## Android: notification taps

* Root cause of the splash on Back: the deep link navigated as soon as the session was signed in, which is before the splash finishes, so the target
  sat on top of `splash` in the back stack.
* Fix (`ui/Navigation.kt`): the link waits until the app is on a real screen (not splash, intro, sign-in, email auth, complete profile). On a cold start the
  splash hand-off to Home calls `openDeepLink()` right away (Home, then the target in one go). The target is pushed with `popUpTo(Home)` so the back stack is
  always Home then target, and Back goes Home, then out of the app.
* `worker/NotificationWorker.kt`: foreground taps use `NEW_TASK | SINGLE_TOP` (no more `CLEAR_TASK`), so a tap reuses the running app through `onNewIntent`
  instead of tearing it down and replaying the splash.

## Android: local voices reverted, lighter APK

* The ONNX Runtime voices (commit 3e4f5b6) took the APK from about 22 MB to 70 MB+ (multi-ABI `onnxruntime-android`), so the commit is reverted: no
  `LocalTts.kt`, no `onnxruntime-android`, the Voice screen is back to Phonon and Whistle only. Do not add an ONNX dependency to the app again; a new
  voice has to run on the existing native engine or be an optional download that ships its own runtime outside the APK.
* Size work with no behaviour change (`app/build.gradle.kts`): native libraries are compressed inside the APK (`useLegacyPackaging`, the 7 MB Phonon
  library is the biggest single file), duplicate KaTeX fonts removed (the CSS asks for woff2 first, so only woff2 stays), packaging excludes for
  license, version and debug-probe files.
* Gradle wrapper 8.14.6 to 9.4.1 (AGP stays 8.13.2: Gradle 9.6 removes an internal API AGP 8 still uses, so do not go above 9.5 without moving AGP).
  CI green on 9.4.1 (run 42415199219: modern APK 9.5 MB, AAB 21.8 MB, down from 30.1 / 47.3 MB with the ONNX voices). Gradle 9.9.0 was tried and
  fails with AGP 8.13.2 (run 42416454594), so 9.4.1 stays. The setup-gradle notice only compares against the newest Gradle, so some notice will remain until
  the app moves to AGP 9 (needs the Material3 Expressive call sites migrated, see AGENTS.md "Android toolchain").

## Verify

```
cd backend_python
export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x PYTHONPATH=.
python3 manage.py test api.test_push_autopilot api.test_resource_reach web.test_admin_push_pages
```
