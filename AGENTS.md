# AGENTS.md — NEBians

Persistent knowledge base for autonomous agents working on this repository.

## Project at a glance

- **App:** NEBians — modern, minimalist Material 3 Android app for Nepali board (NEB) students.
- **Package:** `com.neb.ians`
- **Stack:** Kotlin 2.0, Jetpack Compose, Material 3, Hilt, Room, DataStore, Coroutines/Flow, Firebase Messaging.
- **Min SDK:** 24 (legacy flavor) / 29 (modern flavor) · **Target/Compile SDK:** 35.
- **JDK:** 17.
- **AGP:** 8.7.3 · **Gradle:** 8.10.2.

## App structure

```
app/
├── build.gradle.kts          # AGP config, signing, flavors, output naming
├── proguard-rules.pro
└── src/main/
    ├── AndroidManifest.xml   # Activities (incl. standalone Forum/Reply/NewThread/Thread/PdfViewer), FCM service
    ├── kotlin/com/neb/ians/
    │   ├── NEBiansApp.kt           # @HiltAndroidApp, notification channel
    │   ├── MainActivity.kt         # Compose host, NEBiansTheme
    │   ├── data/
    │   │   ├── model/Categories.kt  # Subject / Grade / ResourceType enums
    │   │   ├── db/                  # Entities, DAOs, NebDatabase
    │   │   ├── prefs/SettingsRepository.kt  # DataStore (dark mode, push pref)
    │   │   └── repo/                # ResourceRepository, ForumRepository, SeedData
    │   ├── di/AppModule.kt           # Hilt providers (DB & DAOs)
    │   ├── notifications/NebFcmService.kt
    │   └── ui/
    │       ├── AppNavHost.kt         # Compose nav: home → resources → detail / settings
    │       ├── theme/                # Color.kt, Type.kt (Poppins), Theme.kt (dynamic + brand)
    │       ├── components/Common.kt  # NebSearchField, ChipRow
    │       ├── home/                 # HomeScreen + HomeViewModel
    │       ├── resources/            # List, detail, view models
    │       ├── pdf/                  # PdfViewerActivity, screen, renderer state + annotations VM
    │       ├── forum/                # Standalone activities: Forum, Thread, Reply, NewThread
    │       └── settings/             # Settings screen + VM
    └── res/                # values, values-night, mipmap-anydpi(-v26), drawable, xml
```

## Key architectural decisions

1. **Single-Activity Compose for primary flows, standalone Activities for forum.** The user explicitly required Forum, Thread, Reply, NewThread screens to be standalone Activities — not fragments or Navigation destinations.
2. **No external PDF library.** Built-in `android.graphics.pdf.PdfRenderer` is used with a small LRU bitmap cache (`PdfRendererState`) to keep startup and memory predictable. Annotations are drawn as a Canvas overlay above each page.
3. **Annotations as JSON in Room.** Each `AnnotationEntity` stores a normalized rect list as JSON in `rectsJson` (0..1 page coordinates) keyed by `resourceId` + `page`, plus kind (`HIGHLIGHT` / `UNDERLINE` / `NOTE`), color, and optional note text.
4. **Offline-first caching.** PDFs download to `cacheDir/pdf/<id>.pdf`; `ResourceRepository.downloadToCache()` emits progress; resource entity is updated with `localPath` on success.
5. **Poppins everywhere via Compose downloadable fonts** (`androidx.compose.ui.ui-text-google-fonts`). Google Play Services fonts provider with the standard cert hashes.
6. **Dark mode toggle via DataStore.** `SettingsViewModel` is hoisted into every Activity to drive `NEBiansTheme(darkTheme = …)`. Dynamic color enabled on Android 12+.
7. **Thumb-up over heart**, as requested. Outlined and filled thumb icons are used for both thread- and post-level reactions.
8. **No excessive shadows or gradients.** All Surfaces/Cards use `tonalElevation = 0.dp`, `shadowElevation = 0.dp`, and rely on `surfaceVariant` for separation. FABs also use 0-elevation defaults.
9. **Two release APKs in CI** via product flavors `legacy` (minSdk 24) and `modern` (minSdk 29), each signed with the committed `release.keystore` and named `NEBians-<versionName-flavor>-<commitShort>.apk`.

## Actions taken (initial scaffold)

- Bootstrapped Gradle project, version catalog, AGP/Kotlin/Compose/Hilt/Room wiring.
- Wrote data layer (entities, DAOs, repos, seed data).
- Built Compose UI: home, resources list with chip filters + search, resource detail with download progress, settings.
- Built standalone Activities for Forum, Thread, Reply, NewThread.
- Built a PdfViewer Activity with annotation toolbar (Pan / Highlight / Underline / Note) and overlay rendering.
- Wrote `release.keystore` (committed per explicit user instruction) and `keystore.properties`.
- Added `.github/workflows/release.yml` building both flavor APKs with Gradle/Setup-Gradle caches, configuration cache, parallel build; uploads artifacts and creates a GitHub Release on `v*` tags.

## Audit findings / known limitations

- **FCM stub only.** `NebFcmService` is wired in the manifest, but no `google-services.json` is bundled. Push works once a real Firebase config is added — no code change required beyond dropping the JSON into `app/`.
- **Seed source URLs are illustrative.** The seeded resources point at typical CDC paths but those exact URLs may not resolve; replace with real CDN endpoints in production.
- **PDF text-selection.** Annotation rects are drawn from finger drag, not OS text-selection, because `PdfRenderer` doesn't expose text. Good enough for "highlight a region" / "underline a region" / sticky notes.
- **Adaptive icons** use vector fallbacks in `mipmap-anydpi/`. Replace with proper PNG densities before public release.

## Deployment notes

- CI: `.github/workflows/release.yml`
  - Triggers: push to `main` / `tembo/**`, PRs to `main`, tags `v*`, manual.
  - Caches: Gradle (`gradle/actions/setup-gradle@v4`), Konan/Kotlin/build cache, Android SDK build cache.
  - Build cmd: `:app:assembleLegacyRelease :app:assembleModernRelease --build-cache --parallel --configuration-cache`.
  - Output naming: `NEBians-<version>-<commit>.apk`, controlled by `androidComponents.onVariants` in `app/build.gradle.kts`.
  - Signed with `release.keystore` (alias `nebians`, both passwords `nebians`).
- Releases: on `v*` tags, `softprops/action-gh-release@v2` uploads both APKs.
