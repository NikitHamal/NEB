# NEBians App Gap Report and Production Notes

## Completed in this pass
- Added a native Result Checker screen instead of the previous WebView-backed version.
- Added native Result Checker support for Class 12, SEE, regular/re-exam, single lookup, bulk lookup, progress, CSV export/share, result detail, GPA display, subject table, and unofficial gradesheet preview.
- Added native News Detail screen instead of a WebView article route.
- Added a separate Admin Android app module that exposes the complete live web admin panel pixel-perfectly through a hardened WebView.
- Updated the provided release workflow to build both student and admin modern APK/AAB artifacts and optional legacy APK artifacts.

## Still not fully native in the student app
The student app is much closer to site parity, but these screens are still not fully native one-to-one implementations:
- Results Guide at `/results/`
- Resource Requests at `/requests/`
- Forum Categories at `/forum/categories/`
- Forum Leaderboard at `/forum/leaderboard/`
- Subject landing pages at `/subject/<grade>/<subject>/`
- Profile achievements at `/profile/<username>/achievements/`
- Copyright takedown page
- Some Study Lab shared/join token flows

## Admin app design decision
The admin panel has many server-rendered controls and permissions-sensitive forms. The separate admin app intentionally uses a production WebView pointed at `/admin/` so every current web control remains available without duplicating admin business logic in Android. This gives pixel-perfect parity with the web admin surface and keeps future web admin changes automatically available in the admin app.

## Build note
The uploaded app archive is an app module, not the complete Gradle root. To build the admin module in the real repo, add `include(":admin")` to `settings.gradle.kts`, place the included `admin/` directory beside `app/`, and replace `.github/workflows/build-release.yml` with the updated workflow.
