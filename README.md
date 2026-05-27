# NEBians

NEBians is a native Android app for Nepali students, built with Kotlin, Jetpack Compose, and Material 3.

## Features

- Searchable resource library for ebooks, PDFs, notes, past papers, formula sheets, and syllabus content.
- Category filters and sorting by subject, grade level, resource type, and title.
- Offline PDF cache with generated starter resources.
- Inbuilt PDF viewer using Android `PdfRenderer`.
- PDF annotation tools for highlights, underlines, and sticky notes, saved locally per PDF.
- Minimal standalone forum, answer, and reply screens.
- Dark mode toggle with persisted settings.
- FCM-compatible notification service plus local notification channel handling.
- Bundled Poppins fonts across the Compose theme.

## Package

`com.neb.ians`

## Build

The project uses the Gradle wrapper:

```bash
./gradlew assembleLegacyRelease assembleModernRelease
```

The release variants are signed with the committed default keystore at `keystore/nebians-release.jks`.

## CI Release APKs

`.github/workflows/release-apks.yml` builds:

- `legacyRelease` with minSdk 23
- `modernRelease` with minSdk 29

The workflow renames both APKs as:

```text
NEBians-<variant>-<short_commit_hash>-v<version>.apk
```
