# NEBians - Project Knowledge Base

## Overview

NEBians is a Material 3 Android app for Nepali students (NEB curriculum). It provides study resources (ebooks, PDFs, notes), a discussion forum, and an advanced PDF viewer with annotation tools.

**Package:** `com.neb.ians`
**Min SDK:** 24 (legacy) / 28 (modern)
**Target SDK:** 34

---

## Architecture Decisions

### Tech Stack
- **Language:** Kotlin
- **UI:** Jetpack Compose with Material 3
- **DI:** Hilt (Dagger)
- **Database:** Room (local-first, offline-ready)
- **State Management:** StateFlow + ViewModel
- **Navigation:** Navigation Compose (single Activity)
- **Preferences:** DataStore
- **Background Work:** WorkManager (Hilt-injected workers)
- **Image Loading:** Coil
- **PDF Rendering:** Android PdfRenderer API (no third-party dependency)
- **Fonts:** Poppins (Google Fonts, bundled as TTF)

### Why Local-First
All data is stored in Room. The app seeds sample data on first launch via a WorkManager one-time task. This makes the app fully functional offline. A backend can be added later by syncing with the local Room database.

### Why PdfRenderer over Third-Party
Android's built-in PdfRenderer avoids large APK size increases from libraries like PDFium. It handles basic rendering well. Annotations are stored as Room entities overlaid on the PDF canvas via Compose Canvas.

### Product Flavors
Two flavors in "target" dimension:
- `modern` (minSdk 28) — for newer Android devices
- `legacy` (minSdk 24) — broader compatibility

Both use the same release signing config.

### Navigation Architecture
- Bottom navigation: Home, Library, Forum, Settings
- Standalone screens (full-screen, not fragments): ForumPostDetail, CreatePost, Reply, PdfReader, Search
- Forum screens are standalone to match the requirement of not being fragments or nav items

---

## App Structure

```
com.neb.ians/
├── NEBiansApp.kt          # Application class (Hilt, WorkManager, notification channels)
├── MainActivity.kt        # Single activity with Compose + dark mode
├── data/
│   ├── local/
│   │   ├── dao/           # Room DAOs (Resource, Annotation, Forum, Bookmark)
│   │   ├── entity/        # Room entities (5 tables)
│   │   └── database/      # NEBiansDatabase
│   ├── model/
│   │   └── SampleData.kt  # Seed data (20 resources, 6 forum posts, 5 replies)
│   └── repository/        # Repository layer (Resource, Forum, Annotation, Bookmark, Settings)
├── di/
│   ├── AppModule.kt       # DataStore provider
│   └── DatabaseModule.kt  # Room database + DAO providers
├── ui/
│   ├── Navigation.kt      # NavHost, Screen routes, bottom nav
│   ├── theme/             # M3 theme (Color, Type with Poppins, Theme)
│   └── screens/
│       ├── home/          # HomeScreen + HomeViewModel
│       ├── library/       # LibraryScreen + LibraryViewModel (categorization + filters)
│       ├── forum/         # ForumScreen, PostDetail, CreatePost, Reply + ViewModels
│       ├── reader/        # PdfReaderScreen, AnnotationOverlay, ReaderViewModel
│       ├── search/        # SearchScreen + SearchViewModel
│       └── settings/      # SettingsScreen + SettingsViewModel
├── util/
│   ├── TimeUtils.kt       # formatTimeAgo(), getSubjectColor()
│   └── NotificationHelper.kt  # WorkManager scheduling helpers
└── worker/
    ├── DataSeederWorker.kt      # Seeds sample data on first launch
    └── NotificationWorker.kt   # Push notification worker
```

---

## Actions Taken

### Initial Build
1. Created full Android project structure with Gradle (Kotlin DSL)
2. Set up Gradle wrapper (8.5), build configs, proguard rules
3. Generated release keystore (`nebians-release.keystore`) — committed to repo for CI
4. Downloaded Poppins font files (Regular, Medium, SemiBold, Bold, Light)
5. Created adaptive icon (book shape foreground)

### Database Layer
1. Designed 5 Room entities: Resources, Annotations, ForumPosts, ForumReplies, Bookmarks
2. Created 4 DAOs with Flow-based queries, search, filtering, sync queries
3. Set up Room database with fallback destructive migration

### DI & Repository
1. Hilt modules for Database and DataStore
2. 5 repository classes wrapping DAOs with business logic
3. Settings repository with DataStore preferences (dark mode, username, notifications, wifi-only)

### UI Screens (all Jetpack Compose + M3)
1. **Home:** Greeting, search bar, subject chips, recent/popular resource carousels, forum activity
2. **Library:** 3-tier filter system (subject, grade, type), grid of resource cards
3. **Search:** Auto-focus search bar, suggestion chips, result list
4. **Forum:** Category filter chips, post list with thumbs-up, FAB for new post
5. **Post Detail:** Full post view, replies with nested thumbs-up, reply FAB
6. **Create Post:** Title, content fields, category dropdown
7. **Reply:** Context card, content field, submit
8. **PDF Reader:** Bitmap rendering, annotation overlay (highlight/underline/sticky note), color picker, page navigation, bookmarks, zoom
9. **Settings:** Profile, dark mode toggle, notifications, downloads, about

### CI/CD
1. GitHub Actions workflow for signed release APK builds (2 flavors)
2. APK naming: `NEBians-{flavor}-v{version}-{commitHash}.apk`
3. Gradle caching, parallel execution, JVM optimizations
4. Separate lint workflow for PRs

---

## Audit Findings

### Design Consistency
- All screens use M3 components (no legacy Material)
- Thumb up icon (ThumbUp) used instead of heart/love throughout
- Outlined icons for inactive states, filled for active
- No excessive shadows or gradients — flat M3 design
- Poppins font applied to all typography styles

### Potential Improvements
- Add network layer (Retrofit/Ktor) for remote resource fetching
- Implement actual PDF file downloading with progress
- Add user authentication for forum
- Room database migration strategy for version 2+
- Add unit tests and UI tests

---

## Known Issues

1. **PDF rendering fallback:** When no actual PDF file exists at the resource's localPath, the reader shows a placeholder page. A sample PDF is generated but may not render correctly on all devices.
2. **Keystore in repo:** The release keystore is committed directly to the repo per requirement. In production, this should be moved to CI secrets.
3. **No backend:** All data is local. Forum posts and resources are seeded from SampleData and don't sync.

---

## Deployment Notes

### GitHub Actions
- **build-release.yml:** Triggers on push to any branch, PRs to main, and manual dispatch
- **lint.yml:** Triggers on PRs to main only
- Keystore is at repo root: `nebians-release.keystore` (alias: nebians, password: nebians123)
- Artifacts retained for 30 days

### Building Locally
```bash
./gradlew assembleModernRelease    # Modern APK (minSdk 28)
./gradlew assembleLegacyRelease    # Legacy APK (minSdk 24)
```
