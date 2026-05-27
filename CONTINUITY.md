## Goal (incl. success criteria):
Build and deliver a complete modern Material 3 Android app "NEBians" (com.neb.ians) for Nepali students with:
1. Inbuilt PDF viewer + annotations (highlight, underline, sticky notes) persisted offline.
2. Content library categorized by Subject, Grade, Type with search/filter.
3. Standalone Forum/Answer/Reply screens (not nav fragments).
4. Dark mode toggle, push notifications, Poppins font, minimal clean M3 UI.
5. GitHub Actions CI that builds two signed release APK variants (minSdk 24 & 26) using an embedded keystore, renamed with commit hash + version.
6. AGENTS.md and CONTINUITY.md maintained.

## Constraints/Assumptions:
- No excessive shadows/gradients; pure M3 surfaces and colors.
- Thumb icon used instead of heart/love.
- All fonts are Poppins (res/font).
- Keystore is embedded in repo at `keystore/nebians.keystore`.
- Single-activity Compose architecture.
- Environment may not have Android SDK for local compilation; we rely on CI for build verification.

## Key Decisions:
- Use Android PdfRenderer + Compose Canvas overlay for PDF & annotations.
- Room DB for offline persistence of content, annotations, forum.
- DataStore for dark mode and notification preferences.
- Forum screens are full-screen destinations in NavHost but NOT bottom nav items.
- CI uses Gradle caching, Java setup caching, and builds two APK splits by minSdk flavor.
- Keystore generated via OpenSSL as PKCS12 and embedded.
- Poppins variable font downloaded from GitHub and placed in res/font.

## State:
- Done: All core source files written (models, DAOs, DB, repositories, DI, themes, screens, services, utils).
- Done: AGENTS.md and CONTINUITY.md created and updated.
- Done: GitHub Actions workflow written with setup-gradle, Java 17, caching, dual flavor builds, artifact upload.
- Done: Keystore generated and placed in `keystore/nebians.keystore`.
- Done: Poppins font files added.
- Done: AndroidManifest, XML resources, launcher icons, notification icon created.
- Done: All M3 screens (Home, Library, PDF, Forum, Answer, Reply, Settings) implemented with minimal, clean UI.
- Now: Final verification pass for imports and consistency.
- Next: Push and let CI validate build.

## Open Questions (UNCONFIRMED if needed):
- UNCONFIRMED: Whether we need Firebase project setup for FCM; we include stub service + manifest entries.
- UNCONFIRMED: Exact list of Nepali curriculum subjects; we seed common NEB (Grade 11/12) subjects.

## Working Set (files/ids/commands):
- Root build files: `build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`
- App module: `app/build.gradle.kts`, `app/src/main/AndroidManifest.xml`
- Source package: `app/src/main/java/com/neb/ians/`
- Resources: `app/src/main/res/values/`, `app/src/main/res/font/`, `app/src/main/res/xml/`, `app/src/main/res/drawable/`
- Workflow: `.github/workflows/build-release.yml`
- Keystore: `keystore/nebians.keystore`
- Docs: `AGENTS.md`, `CONTINUITY.md`
