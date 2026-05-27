## Goal (incl. success criteria):
Build a full modern minimalist M3-themed Android app named NEBians for Nepali NEB students with:
- Resources (ebooks/PDFs/notes) with categorization by subject, grade, type
- Discussion forum with standalone screens
- PDF viewer with annotation tools (highlight, underline, sticky notes)
- Dark mode toggle, push notifications, Poppins fonts
- GitHub Actions CI/CD producing 2 signed release APKs
- Package name: com.neb.ians

## Constraints/Assumptions:
- Kotlin + Jetpack Compose only
- Material 3 theming, Google-style clean UI
- No excessive shadows, gradients
- Thumb icon preferred over heart/love icon
- Forum screens are standalone (not fragments or nav items)
- Keystore committed directly to repo (as requested)
- Poppins font family throughout

## Key Decisions:
- No Hilt/DI - manual singleton via Application class
- Room for all local storage (offline-first)
- Canvas-based PDF viewer for annotation overlay support
- Product flavors: api24 (Android 7+) and api31 (Android 12+)
- DataStore for theme preferences
- Gradle 8.9 with version catalog

## State:
- Done:
  - Full project structure with Gradle build system
  - M3 theme with Poppins typography and dark mode toggle
  - Bottom navigation (Home, Resources, Forum, Profile)
  - Resource categorization with subject/grade/type filters
  - Search functionality
  - PDF viewer with highlight, underline, sticky note annotations
  - Discussion forum with post creation, replies, thumb up
  - Notification channels and helper
  - GitHub Actions workflow for 2 signed APKs
  - Keystore generation and configuration
  - Sample data seeding
  - AGENTS.md and CONTINUITY.md documentation
- Now: Final verification and cleanup
- Next: Build verification if Gradle/Android SDK available

## Open Questions (UNCONFIRMED if needed):
- None

## Working Set (files/ids/commands):
- `app/build.gradle.kts` - Main app build config
- `settings.gradle.kts` - Project settings
- `gradle/libs.versions.toml` - Version catalog
- `.github/workflows/build-release.yml` - CI/CD
- `keystore/nebians-release.jks` - Signing keystore
- `app/src/main/java/com/neb/ians/` - All Kotlin sources
- `app/src/main/res/` - Resources (fonts, themes, icons)
