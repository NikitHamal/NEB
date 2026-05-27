# NEBians — Agent Knowledge Base

This file is the persistent knowledge base for the agent working on the NEBians Android app.
It is intentionally kept terse and is updated after each significant milestone.

---

## Project Snapshot

NEBians is a Material 3, Jetpack Compose Android app for Nepali NEB students.
Package: **`com.neb.ians`** · Kotlin 2.0 · AGP 8.5 · compileSdk 34 · minSdk 24/26 (variant-split).

Top-level features:
- Browse curriculum resources (PDFs, ebooks, notes) categorized by **Subject**, **Grade**, **Type**.
- Search + multi-axis filtering of resources.
- Built-in modern PDF viewer with offline caching and **annotations** (highlight, underline, sticky notes).
- Minimal discussion forum (list / thread / reply / new-thread) as **standalone full-screen routes**.
- Dark mode toggle (System/Light/Dark) + Material You dynamic color on Android 12+.
- Poppins font everywhere via downloadable Google Fonts (with bundled certs).
- Thumbs-up reaction (no hearts) for forum likes.
- Real-time push notifications via Firebase Cloud Messaging (FCM) for announcements.
- Local-first storage via Room + DataStore. Seeded curriculum on first launch.

---

## Architecture Decisions

- **MVVM with Hilt** — `@HiltAndroidApp` Application, `@HiltViewModel` per screen, Hilt DI module
  for Room/DAO/Repos. Keeps the dependency graph trivial to extend.
- **Compose + M3 only** — no Views, no fragments. Forum sub-screens are full Compose destinations
  on the same `NavHost`, not nested fragments / bottom-sheet dialogs.
- **Two product flavors `legacy` (minSdk 24) and `modern` (minSdk 26)** — gives CI two distinct
  release APKs without maintaining two source trees. Each gets a unique version suffix
  (`-legacy` / `-modern`) and is renamed to `NEBians-<flavor>-<versionName>-<gitSha>.apk`.
- **`PdfRenderer` over external libs** — zero new licenses, modest binary footprint, fully offline.
  Pages are LRU-cached as bitmaps (~24 MB) keyed by `path|page|width` for smooth scrolling.
- **Annotations stored in Room** — `AnnotationEntity` keyed by `resourceId + page`, percentage
  coordinates so they stay locked to the page regardless of viewport size.
- **Theme** — color schemes hand-derived from Google's M3 baseline (deep purple seed). Dynamic
  color overrides on Android 12+.
- **Push notifications** — `FirebaseMessagingService` scaffolding wired. The gms plugin is
  applied **conditionally** (only if `google-services.json` is present), so CI builds succeed
  without secrets while still leaving messaging functional when a `google-services.json` is added.

---

## App Structure

```
app/
├── build.gradle.kts            # Variants, signing, APK renaming, deps
├── keystore/nebians.keystore   # Checked-in default keystore (per project requirement)
└── src/main/
    ├── AndroidManifest.xml
    ├── res/                    # M3 colors, themes, font_certs, launcher icons
    └── java/com/neb/ians/
        ├── NebiansApp.kt       # HiltAndroidApp, FCM channel, Seeder bootstrap
        ├── MainActivity.kt     # NEBians theme + NebRoot
        ├── data/
        │   ├── local/          # Room entities, DAOs, NebDatabase, type converters
        │   ├── model/          # Subject, Grade, ResourceType enums
        │   ├── prefs/          # DataStore UserPrefsRepository
        │   ├── Repository.kt   # ResourceRepository, AnnotationRepository, ForumRepository
        │   └── Seeder.kt       # Curriculum seed for fresh installs
        ├── di/DataModule.kt    # Hilt module: Room + DAOs + AppScope
        ├── pdf/PdfPageCache.kt # Offline file copy + LRU bitmap renderer
        ├── push/NebPushService.kt
        └── ui/
            ├── NebRoot.kt              # Bottom nav + NavHost
            ├── NebDestinations.kt
            ├── theme/                  # Color.kt, Type.kt (Poppins), Theme.kt
            ├── common/Components.kt    # SearchField, FilterChipRow, EmptyState
            ├── home/                   # HomeScreen + ViewModel
            ├── library/                # LibraryScreen + ResourceCard + ViewModel
            ├── forum/                  # ForumScreen, ThreadScreen, ReplyScreen, NewThreadScreen
            ├── reader/                 # PdfReaderScreen + ViewModel (annotations)
            └── settings/               # SettingsScreen + ViewModel
```

---

## Actions Taken

- Created Gradle project skeleton (root + app modules, version catalog, wrapper for Gradle 8.9).
- Built M3 theme with hand-tuned light/dark schemes and Poppins typography via downloadable fonts.
- Wrote Room schema for resources / annotations / forum threads & replies + DataStore preferences.
- Implemented search/categorization, library screen, home screen with recent + favorites + carousel.
- Implemented PDF reader with offline caching, bitmap LRU, and three annotation tools.
- Implemented forum as four standalone Compose destinations (list, thread, reply, new thread).
- Wrote settings screen with theme toggle, dynamic-color switch, and handle editor.
- Added FCM service stub, manifest entries, and notification channel creation.
- Created GitHub Actions workflow that builds two signed release APKs with Gradle / build / KSP caches.
- Generated default keystore at `app/keystore/nebians.keystore` and committed it (per project requirement).
- Authored `AGENTS.md` (this file) and `CONTINUITY.md` for session continuity.

---

## Audit Findings / Known Issues

- **Bundled PDFs are placeholders**: `seedResources()` references `asset://samples/...` paths.
  Until the actual PDFs are dropped into `app/src/main/assets/samples/`, the cache falls back to
  a tiny built-in valid PDF so the reader does not crash. Drop real PDFs in to replace.
- **FCM needs `google-services.json`**: present-day builds compile and run without it; push
  notifications activate as soon as the file is committed. The gms plugin is conditionally applied.
- **Compose Compiler version**: pinned via `kotlin-compose` plugin (Kotlin 2.0.20). If bumping
  Kotlin, bump KSP too — they are coupled.
- **Keystore in repo**: the project intentionally commits the default keystore for hermetic CI
  signing. Anyone who clones the repo can sign as NEBians — this is **only acceptable** for an
  unmonetised student-app; if app-store distribution is added later, rotate the key.

---

## Deployment Notes

- **CI workflow**: `.github/workflows/build.yml`
  - Triggers on push to any branch, PRs into `main`, and `workflow_dispatch`.
  - Builds two signed release APKs (`assembleLegacyRelease`, `assembleModernRelease`).
  - APKs are renamed in-build to `NEBians-<flavor>-<versionName>-<gitSha>.apk` (logic in `app/build.gradle.kts`).
  - Caches Gradle / KSP / intermediate Android build outputs.
  - Uploads APK artifacts named `NEBians-<version>-<sha>`.
  - On `v*` tag pushes, also publishes a GitHub Release with the APKs attached.
- **Keystore**: `app/keystore/nebians.keystore` (alias `nebians`, store/key password `nebians123`).
  Wired into both `debug` and `release` build types so locally-built and CI-built APKs are signed
  the same way (per project requirement).
- **GitHub Pages**: not configured. Add a workflow under `.github/workflows/` if a docs site is needed.

---

## Continuity / Handover

If a future agent picks this up:
1. Read `CONTINUITY.md` first — it is the canonical session briefing.
2. Confirm the keystore at `app/keystore/nebians.keystore` is still present before pushing CI changes.
3. Real PDF assets should be dropped into `app/src/main/assets/samples/` and matched to entries in
   `Seeder.seedResources()`.
4. If push notifications are needed in production, commit `app/google-services.json` — the build
   system will activate the gms plugin automatically.
