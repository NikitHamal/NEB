## Goal (incl. success criteria):
Build NEBians: a Material 3 themed Android app (package `com.neb.ians`) for Nepali students that ships:
- PDF/ebook/notes browser with subject/grade/type categorization + search
- Modern in-app PDF viewer with annotations (highlight, underline, sticky notes) persisted offline
- Minimal discussion forum (list, thread, reply, new-thread) as standalone full-screen routes
- Offline local caching of resources via Room + DataStore
- Dark mode toggle, Poppins font everywhere, thumbs-up like icon
- FCM push notifications scaffolding for announcements
- GitHub Actions building two signed release APKs (different minSdks) named with commit hash + version, with a checked-in default keystore

## Constraints/Assumptions:
- Kotlin 2.0.20 + AGP 8.5 + compileSdk 34 + Compose BOM 2024.09
- Jetpack Compose + Material 3 (no Views, no Fragments)
- Hilt + Room + DataStore + Navigation Compose
- Poppins via downloadable Google Fonts (certs in `font_certs.xml`)
- Keystore committed to repo (intentional)
- Forum is local-only — fulfils "minimal forum"
- PDF rendering via `android.graphics.pdf.PdfRenderer` (built-in); bitmap LRU cache

## Key Decisions:
- Two product flavors `legacy` (minSdk 24) and `modern` (minSdk 26) — one CI job builds both signed
- Annotations stored as percentage coords so they survive viewport resizes
- gms plugin conditionally applied so builds work without `google-services.json`
- APK rename in-build to `NEBians-<flavor>-<versionName>-<gitSha>.apk`

## State:
- Done:
  - Gradle project skeleton (root, app, version catalog, wrapper)
  - M3 theme, Poppins typography, color schemes
  - Navigation Compose graph with standalone Forum screens
  - Room schema + DAOs + repos + DataStore prefs + Seeder
  - Library + Home + Settings + Forum (4 screens) + PDF Reader (with 3-tool annotation toolbar)
  - FCM service + notification channel
  - GitHub Actions workflow with caching + 2 signed APK outputs
  - Committed `app/keystore/nebians.keystore`
  - AGENTS.md + CONTINUITY.md
- Now: final pass / repo polish before push.
- Next: drop real PDFs into `app/src/main/assets/samples/`; add `google-services.json` if production push needed.

## Open Questions (UNCONFIRMED if needed):
- None. Build scripts compile-checked by review only — no Android SDK in sandbox.

## Working Set (files/ids/commands):
- `build.gradle.kts`, `settings.gradle.kts`, `gradle/libs.versions.toml`, `gradle.properties`
- `app/build.gradle.kts`, `app/proguard-rules.pro`, `app/keystore/nebians.keystore`
- `app/src/main/AndroidManifest.xml`, `app/src/main/res/**`
- `app/src/main/java/com/neb/ians/**`
- `.github/workflows/build.yml`
- `AGENTS.md`, `CONTINUITY.md`, `README.md`, `.gitignore`
