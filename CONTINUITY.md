## Goal (incl. success criteria):

Build a complete modern Material 3 Android app named **NEBians** (`com.neb.ians`) for Nepali students with:
- Categorized resources (ebooks/PDFs/notes) with offline Room caching
- Advanced inbuilt PDF viewer with highlight, underline, and sticky note annotations saved locally
- Minimal discussion forum with standalone Activities (not fragments)
- Dark mode toggle, real-time push notification channels, Poppins fonts throughout
- GitHub Actions workflow producing 2 signed release APKs (api24 + api29) renamed with commit hash + version
- Keystore committed to repo, Gradle caching enabled, ProGuard enabled

**Success criteria**: All source files created, project builds in CI, APKs are signed and renamed, docs (`AGENTS.md`, `CONTINUITY.md`) exist.

## Constraints/Assumptions:

- No Java/Android SDK in local sandbox; CI (GitHub Actions) handles actual APK builds.
- Third-party PDF libraries avoided to keep app lightweight; use Android `PdfRenderer`.
- Forum is local-only (no backend server).
- User explicitly requested keystore in repo with hardcoded credentials.
- M3 UI: no excessive shadows/gradients, thumb icon instead of heart, modern material icons.

## Key Decisions:

- **Architecture**: MVVM + Room + Coroutines + ViewBinding
- **Navigation**: Bottom nav in MainActivity launches standalone Activities for Forum/Settings/Resources
- **PDF annotations**: Custom `PdfPageView` with touch-drag selection overlay + Room persistence
- **Product flavors**: `api24` (minSdk 24) and `api29` (minSdk 29) for dual APK builds
- **Keystore**: Generated with OpenSSL as PKCS12 (`keystore.p12`) because `keytool` was unavailable locally
- **Fonts**: Poppins downloaded from google/fonts GitHub repo into `res/font/`

## State:

- Done:
  - Project skeleton (Gradle, manifest, themes, colors, layouts)
  - All Kotlin source files (Application, DB, DAOs, Repositories, ViewModels, Activities, Adapters, Custom Views, Services)
  - Poppins font files and font-family XML
  - Vector drawables for all icons (M3 style, no gradients)
  - GitHub Actions workflow with caching, dual-flavor builds, artifact upload, APK rename
  - Keystore generated and committed
  - `AGENTS.md` and `CONTINUITY.md` created

- Now:
  - Final review for consistency and any remaining compilation risks

- Next:
  - Hand off to CI for actual build verification
  - Address any build failures discovered in GitHub Actions

## Open Questions (UNCONFIRMED if needed):

- None at this time.

## Working Set (files/ids/commands):

- Root build: `build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`
- App build: `app/build.gradle.kts`, `app/proguard-rules.pro`
- Manifest: `app/src/main/AndroidManifest.xml`
- Sources: `app/src/main/java/com/neb/ians/...`
- Resources: `app/src/main/res/...`
- CI: `.github/workflows/build.yml`
- Keystore: `keystore.p12`
- Docs: `AGENTS.md`, `CONTINUITY.md`
