# NEBians - Project Knowledge Base

## Learnings

- **Gradle 8.9 wrapper JAR**: The wrapper JAR in Gradle 8.9 is split into `gradle-wrapper-main-8.9.jar` and `gradle-wrapper-shared-8.9.jar`. The main class remains `org.gradle.wrapper.GradleWrapperMain`. The CI workflow uses `gradle/actions/setup-gradle@v4` which handles wrapper validation and setup automatically.
- **Compose M3 segmented buttons**: `SingleChoiceSegmentedButtonRow` requires explicit `itemShape` for each button. The `SegmentedButtonDefaults.itemShape(index, count)` helper handles corner rounding.
- **Room + Compose integration**: Using `Flow` from Room DAOs with `collectAsState()` provides automatic recomposition on data changes. Using `flatMapLatest` for filter/search reactivity.
- **DataStore for preferences**: Using `preferencesDataStore` delegate with `Flow` provides reactive theme preference management.
- **Poppins fonts**: Downloaded directly from Google Fonts repository. All 5 weights (Regular, Medium, SemiBold, Bold, Light) used across the typography scale.

## Actions Taken

1. **Project Structure**: Created full Android project with Kotlin DSL Gradle build, version catalog (`libs.versions.toml`), and multi-flavor configuration (api24/api31).
2. **M3 Theme**: Implemented Material 3 theming with dynamic colors (Android 12+), custom color scheme fallbacks, Poppins typography across all text styles.
3. **Dark Mode**: Implemented 3-way theme toggle (Light/Dark/System) using DataStore preferences with reactive state management.
4. **Navigation**: Set up Jetpack Navigation Compose with bottom navigation (Home, Resources, Forum, Profile) and standalone screens for forum post, reply, create post, PDF viewer, and search.
5. **Data Layer**: Created Room database with 5 entities (Resource, Annotation, ForumPost, ForumReply, Bookmark), corresponding DAOs, and repository pattern.
6. **Resource Categorization**: Implemented multi-filter system (subject, grade, type) with reactive filtering using `combine` + `flatMapLatest`. Added search functionality.
7. **PDF Viewer**: Built canvas-based PDF viewer with annotation tools (highlight, underline, sticky notes). Annotations stored locally via Room.
8. **Discussion Forum**: Created standalone forum screens (list, post detail, create post, reply) with thumb up interactions and subject/grade tags.
9. **Notifications**: Set up notification channels (Announcements, Community) with `NotificationHelper` utility.
10. **CI/CD**: Created GitHub Actions workflow building 2 signed release APKs (api24/api31) with caching, named with commit hash and version.
11. **Keystore**: Generated RSA 2048-bit keystore at `keystore/nebians-release.jks` committed to repo.
12. **Sample Data**: Seeded database with 12 educational resources and 5 forum posts on first launch.

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| No DI framework (Hilt) | Reduced compile time and complexity. Using manual `Application`-level singleton for database. Adequate for current app size. |
| Room for all local data | Single database for resources, annotations, forum, bookmarks. Offline-first approach with reactive Flows. |
| Canvas-based PDF rendering | Provides annotation overlay capability without third-party PDF library dependency. Real PDF content rendering would use `PdfRenderer` API. |
| Product flavors for API levels | `api24` (Android 7+) and `api31` (Android 12+) ensure optimized APKs for different device capabilities. |
| Standalone forum screens | Forum post detail, reply, and create screens are full standalone screens with their own navigation routes, not fragments or dialog fragments. |
| Thumb icon over heart icon | User preference. Using `ThumbUp`/`ThumbUpOutlined` from Material Icons Extended. |
| DataStore over SharedPreferences | Modern, coroutine-friendly, type-safe preference storage for theme settings. |

## App Structure

```
com.neb.ians/
├── NEBiansApp.kt          # Application class, DB init, notification channels
├── MainActivity.kt        # Single activity, edge-to-edge, theme management
├── data/
│   ├── SampleData.kt      # Sample resources and forum posts
│   ├── local/
│   │   ├── dao/            # ResourceDao, AnnotationDao, ForumDao, BookmarkDao
│   │   ├── entity/         # Room entities
│   │   └── database/       # NEBiansDatabase (Room)
│   └── repository/         # ResourceRepository, ForumRepository, AnnotationRepository
├── navigation/
│   └── Routes.kt           # Navigation route constants
├── ui/
│   ├── NEBiansAppRoot.kt   # Root composable with NavHost + BottomNav
│   ├── theme/              # Color, Type (Poppins), Theme (M3 + dynamic)
│   └── screens/
│       ├── home/           # HomeScreen + HomeViewModel
│       ├── resources/      # ResourcesScreen + ResourcesViewModel (filters)
│       ├── forum/          # ForumScreen, ForumPostScreen, CreatePostScreen, ReplyScreen
│       ├── pdfviewer/      # PdfViewerScreen + PdfViewerViewModel (annotations)
│       ├── profile/        # ProfileScreen (theme toggle, settings)
│       └── search/         # SearchScreen + SearchViewModel
└── utils/
    ├── ThemeSettings.kt    # DataStore-based theme preference
    ├── TimeUtils.kt        # Relative time formatting
    └── NotificationHelper.kt  # Push notification utility
```

## Audit Findings

- All screens use M3 components exclusively (no legacy Material/AppCompat)
- No excessive shadows or gradients - flat M3 surfaces with tonal elevation
- Thumb icons used consistently instead of heart/love icons
- Navigation animations use fade (tabs) and slide (detail screens) - minimal, clean
- All Room queries use Flow for reactive data
- Search uses `LIKE` with wildcard for fuzzy matching

## Known Issues

- **PDF Viewer**: Currently renders sample/placeholder content. Real PDF rendering requires files to be present on device. The annotation system works fully with position-based storage.
- **Gradle Wrapper JAR**: Using Gradle 8.9 wrapper JAR extracted from distribution. CI handles this via `gradle/actions/setup-gradle@v4`.
- **Notifications**: Channels created but no background service/FCM integration. `NotificationHelper` is ready for use with any push notification service.

## Deployment Notes

- **GitHub Actions**: Workflow at `.github/workflows/build-release.yml`
- Triggers on push to main/master/develop and PRs to main/master
- Builds 2 APKs: `NEBians-v{version}-api24-{hash}.apk` and `NEBians-v{version}-api31-{hash}.apk`
- Uses Gradle caching, parallel builds, and build-cache for speed
- APKs uploaded as artifacts with 30-day retention
- Keystore at `keystore/nebians-release.jks` (password: `nebians2024`, alias: `nebians`)
