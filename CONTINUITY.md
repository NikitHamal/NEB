## Goal (incl. success criteria):
Build full modern minimalist M3-themed Android app **NEBians** (package `com.neb.ians`) in Kotlin + Compose for Nepali students. Features: resource library (eBooks/PDFs/notes) with subject/grade/type categorization + search, advanced inbuilt PDF viewer with annotations (highlight, underline, sticky notes) saved locally, minimal discussion forum with **standalone** screens (not fragments/nav items), Poppins font, dark-mode toggle, FCM push notifications, thumb icon over heart, modern Material icons, no excessive shadows/gradients, high-performance offline caching. Plus: GitHub Actions workflow producing two signed release APKs (different minSdk targets) named `<commit>-<version>.apk`, default keystore committed to repo, with build caching.

## Constraints/Assumptions:
- Sandbox has no Android SDK — cannot build/run; CI compiles & validates.
- AGP 8.7.3, Kotlin 2.0.21, Compose BOM 2024.12.01, JDK 17, Gradle 8.10.2.
- Single Gradle module `app`.
- Local persistence: Room + DataStore. PDF: built-in `android.graphics.pdf.PdfRenderer` (no external libs) with Compose overlay for annotations.
- FCM stub (no google-services.json bundled — wired but optional).
- Two flavors `legacy` (minSdk 24) and `modern` (minSdk 29) → both signed with `release.keystore`.

## Key Decisions:
- Single-Activity + Compose Navigation for Home/Resources/Settings; **Forum, Thread, Reply, NewThread, PdfViewer are standalone Activities** as user requested.
- Material 3 with dynamic color on Android 12+; brand fallback palette otherwise.
- Annotations as JSON in Room (`rectsJson`, normalized 0..1 coords) keyed by resourceId + page.
- Keystore committed (`release.keystore`, alias `nebians`, password `nebians`) per explicit user instruction.
- Poppins via Compose downloadable fonts (Google Fonts) — no bundled TTF.
- All Surfaces/Cards/FABs at 0dp shadow/tonal elevation; reliance on `surfaceVariant` for separation.

## State:
- Done: full project scaffold, data layer, DI, UI (home/resources/detail/settings + standalone forum/PDF), annotation toolbar (highlight/underline/note), FCM stub, keystore, gradle wrapper, CI workflow, AGENTS.md, README.
- Now: ready for CI to validate.
- Next: pushed via platform.

## Open Questions (UNCONFIRMED if needed):
- None.

## Working Set (files/ids/commands):
- `app/build.gradle.kts`, root `build.gradle.kts`, `settings.gradle.kts`, `gradle/libs.versions.toml`, `gradle.properties`
- `app/src/main/AndroidManifest.xml`
- `app/src/main/kotlin/com/neb/ians/**`
- `app/src/main/res/{values,values-night,xml,drawable,mipmap-anydpi*}/**`
- `.github/workflows/release.yml`
- `release.keystore`, `keystore.properties`
- `AGENTS.md`, `README.md`
