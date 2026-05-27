# NEBians

A modern Material 3 Android app for Nepali students. Study resources, ebooks, notes, past papers, and a discussion forum — all in one place.

## Features

- **Resource Library** — Browse and filter ebooks, notes, past papers by subject, grade level, and type
- **PDF Viewer** — Built-in viewer with annotation tools (highlight, underline, sticky notes), bookmarks, and zoom
- **Discussion Forum** — Ask questions, share tips, and help fellow students
- **Offline Access** — All resources cached locally with Room database
- **Dark Mode** — Clean dark theme toggle
- **Push Notifications** — Stay updated on announcements and forum activity

## Tech Stack

- Kotlin + Jetpack Compose
- Material 3 with Poppins typography
- Room Database + DataStore
- Hilt Dependency Injection
- Navigation Compose
- WorkManager

## Building

```bash
# Modern APK (Android 9+)
./gradlew assembleModernRelease

# Legacy APK (Android 7+)
./gradlew assembleLegacyRelease
```

## Package

`com.neb.ians`
