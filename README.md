# NEBians

Modern, minimalist Material 3 Android app for Nepali board (NEB) students. Curated eBooks, PDFs, notes & past papers; a built-in PDF viewer with highlight / underline / sticky-note annotations; a small discussion forum; dark mode; offline cache; push notifications.

## Tech

Kotlin · Jetpack Compose · Material 3 · Hilt · Room · DataStore · Firebase Messaging (optional) · Poppins via Compose downloadable fonts.

## Build

```bash
./gradlew :app:assembleLegacyRelease :app:assembleModernRelease
```

Two flavors are produced:

| Flavor   | minSdk | Output                                          |
|----------|--------|-------------------------------------------------|
| legacy   | 24     | `NEBians-<version-legacy>-<commit>.apk`         |
| modern   | 29     | `NEBians-<version-modern>-<commit>.apk`         |

Both are signed with the bundled `release.keystore`. CI does this automatically on every push (see `.github/workflows/release.yml`).

## Project knowledge

See `AGENTS.md` for architecture, structure, and decisions.
