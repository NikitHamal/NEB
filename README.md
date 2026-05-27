# NEBians

A modern Material 3 Android app for Nepali NEB students. Built with Kotlin and Jetpack Compose.

## Features

- **Resource Library** - Ebooks, PDFs, notes organized by subject, grade, and type
- **Content Search** - Full-text search across all resources
- **PDF Viewer** - Built-in viewer with annotation tools (highlight, underline, sticky notes)
- **Discussion Forum** - Ask questions, reply, and engage with the community
- **Dark Mode** - System, light, and dark theme options
- **Offline Access** - Local caching with Room database
- **Push Notifications** - Announcements and community activity alerts

## Tech Stack

- Kotlin + Jetpack Compose
- Material 3 with dynamic colors
- Room Database
- DataStore Preferences
- Navigation Compose
- Poppins Typography

## Build

```bash
./gradlew assembleApi24Release  # Android 7+ APK
./gradlew assembleApi31Release  # Android 12+ APK
```

## Package

`com.neb.ians`
