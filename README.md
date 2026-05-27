# NEBians

A modern, Material 3 Android app for Nepali NEB students. Browse curriculum resources
(ebooks, PDFs, past papers, notes), read with a built-in annotating PDF viewer, and
discuss with peers in a minimal forum — all with offline caching, Poppins typography,
and a clean M3 light/dark theme.

> Package: `com.neb.ians` · Kotlin · Jetpack Compose · Material 3

## Features

- **Library** — search and filter resources by **Subject**, **Grade**, and **Type**.
- **PDF reader** — built-in offline viewer with **Highlight**, **Underline**, and **Sticky Note**
  annotations, persisted locally per resource and per page.
- **Forum** — list, thread, reply, and new-thread screens (standalone routes, not fragments)
  with **thumbs-up** reactions.
- **Settings** — dark / light / system theme, dynamic color (Android 12+), display name.
- **Offline-first** — Room + DataStore. PDFs cached to internal storage; pages rendered into
  an LRU bitmap cache.
- **Push notifications** — FCM scaffolding ready for announcements.

## Build

```bash
./gradlew :app:assembleLegacyRelease   # signed APK, minSdk 24
./gradlew :app:assembleModernRelease   # signed APK, minSdk 26
```

Both variants are signed with the default keystore at `app/keystore/nebians.keystore`.
APK filenames are `NEBians-<flavor>-<versionName>-<gitSha>.apk`.

## CI

GitHub Actions builds and signs both APKs on every push. See `.github/workflows/build.yml`.

## Adding real resources

Drop your PDFs into `app/src/main/assets/samples/` and update `Seeder.seedResources()`
in `app/src/main/java/com/neb/ians/data/Seeder.kt` to point at them via `asset://samples/<name>.pdf`.
