## Goal (incl. success criteria):
- Build a full native Android app named NEBians in Kotlin + Jetpack Compose, package `com.neb.ians`.
- Include Nepali student resources, categorized/searchable content, offline PDF caching, advanced in-app PDF viewing with highlight/underline/sticky-note annotations saved locally per PDF, dark mode toggle, minimal discussion forum with standalone screens, push notification plumbing, Poppins typography, M3 minimalist UI.
- Add signed release build setup with committed default keystore and GitHub Actions workflow producing two renamed release APKs for different Android-version flavors.

## Constraints/Assumptions:
- Repo started nearly empty (`README.md` only).
- Do not run git commit/push/PR commands; Tembo platform handles them.
- Container has Gradle 8.12.1 through a bundled JDK but no Android SDK, so local APK build may not be possible.
- User explicitly requested a committed default keystore despite normal security concerns.
- Firebase/real push delivery still requires a real Firebase project config outside this sandbox; app includes FCM-compatible service and local notification handling.

## Key Decisions:
- Use a single Android app module with Compose Material 3 and standalone NavHost destinations, not fragments.
- Use generated local PDFs plus a cache manager for offline-ready sample resources; remote URL support is included at the cache layer.
- Use Android `PdfRenderer` for native PDF page rendering and JSON files in internal storage for per-PDF annotations.
- Use product flavors `legacy` and `modern` to produce two signed release APKs for different Android minSdk targets while keeping the package name.

## State:
- Done:
  - Repository inspected; greenfield Android scaffold confirmed.
  - Documentation ledgers created and updated.
  - Full Android Kotlin/Compose project scaffolded.
  - App implemented with Material 3 UI, Poppins fonts, library categorization/search/sort, offline PDF cache, PDF viewer, annotations, forum/answer/reply screens, announcements, settings/dark mode, and notification plumbing.
  - Default release keystore generated at `keystore/nebians-release.jks`.
  - GitHub Actions workflow added for signed `legacyRelease` and `modernRelease` APKs renamed with short commit SHA and version.
  - `.gitignore` and README added/updated.
  - Temporary Android SDK installed under `/tmp/android-sdk` for local verification.
  - Verified `:app:assembleLegacyDebug` succeeds.
  - Verified `assembleLegacyRelease assembleModernRelease` succeeds with build cache/configuration cache.
  - Verified release APK outputs are signed with `apksigner`.
  - Verified workflow-style rename produces `NEBians-legacy-<hash>-v1.0.0.apk` and `NEBians-modern-<hash>-v1.0.0.apk`.
  - Replaced deprecated mirrored Material icons with AutoMirrored variants.
- Now:
  - Final cleanup and status check.
- Next:
  - Report concise completion summary.

## Open Questions (UNCONFIRMED if needed):
- UNCONFIRMED: Actual Firebase project credentials are not available, so push delivery cannot be proven end-to-end here.

## Working Set (files/ids/commands):
- Files: `settings.gradle.kts`, `build.gradle.kts`, `app/build.gradle.kts`, `app/src/main/**`, `.github/workflows/release-apks.yml`, `AGENTS.md`, `CONTINUITY.md`, `keystore/nebians-release.jks`.
- Commands used/expected: `gradle wrapper`, `./gradlew :app:assembleLegacyDebug`, `./gradlew --build-cache --configuration-cache assembleLegacyRelease assembleModernRelease`, `apksigner verify`, GitHub Actions release workflow.
