## Goal (incl. success criteria):
- Build a complete native Android app named NEBians for Nepali students with package `com.neb.ians`.
- Success criteria: modern minimalist Material 3 UI, Poppins font, categorized resources with search/filtering, local/offline PDF caching, inbuilt PDF viewer with highlight/underline/sticky-note annotations saved per PDF, standalone forum/answer/reply screens, dark mode toggle, notifications, and GitHub Actions producing two signed release APKs named with version and commit hash.

## Constraints/Assumptions:
- Repository started nearly empty (`README.md` only).
- Do not create/switch branches, commit, push, or open PR; Tembo handles git operations.
- User explicitly requested a default keystore committed to the repo and reused for builds.
- Local container has Gradle but no Android SDK exposed; CI workflow must provide the Android build environment.
- Remote real-time push infrastructure is UNCONFIRMED; implement Android notification channels/local notification hooks and keep the app push-ready without requiring external secrets.

## Key Decisions:
- Scaffold a native Kotlin + Jetpack Compose Android app.
- Use Material 3 Compose with dynamic color where available and restrained surfaces/elevation.
- Implement forum, answer, and reply as separate `Activity` classes rather than fragments.
- Use Android `PdfRenderer` + local file cache for PDFs and JSON files for offline per-PDF annotations.
- Create two product flavors for different Android API ranges: `minApi23` and `minApi26`.

## State:
- Done:
  - Inspected repo and tooling.
  - Confirmed repo is effectively empty.
  - Checked current Android Gradle plugin compatibility docs before selecting modern build versions.
  - Created Gradle project scaffold, manifest/resources, Material 3 theme, bundled Poppins fonts, app data layer, notification helpers, PDF cache/renderer/annotation storage.
  - Implemented main Compose app, categorized resource filters/search, announcements, standalone forum/answer/reply activities, and PDF viewer with annotation tools.
  - Added committed default release keystore, Gradle wrapper, and GitHub Actions signed dual-APK workflow.
  - Installed temporary Android SDK under `/tmp/android-sdk` and verified both release APK builds locally.
  - Verified APK signatures with Android `apksigner`.
- Now:
  - Final repository sanity check.
- Next:
  - Report completed work and verification.

## Open Questions (UNCONFIRMED if needed):
- No remote backend/Firebase project details were supplied, so external real-time remote push delivery cannot be fully wired.

## Working Set (files/ids/commands):
- `AGENTS.md`, `CONTINUITY.md`
- `settings.gradle.kts`, `build.gradle.kts`, `gradle/libs.versions.toml`, `app/build.gradle.kts`
- `app/src/main/**`
- `.github/workflows/android-release.yml`
- `keystores/nebians-release.jks`
- Verification: `./gradlew --no-daemon --parallel --build-cache :app:assembleMinApi23Release :app:assembleMinApi26Release`
