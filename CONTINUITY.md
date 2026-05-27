## Goal (incl. success criteria):
Build a full modern minimalist M3-themed Android app called NEBians (com.neb.ians) for Nepali students with:
- Ebooks/PDF resources with categorization (subject, grade, type)
- Advanced PDF viewer with annotation tools (highlight, underline, sticky notes)
- Discussion forum with standalone screens
- Dark mode toggle, push notifications
- Poppins fonts, Google-style M3 UI/UX
- GitHub Actions workflow for 2 signed release APKs
- Keystore committed to repo

## Constraints/Assumptions:
- Package name: com.neb.ians
- Forum screens are standalone (not fragments/nav items)
- Thumb icon over love icon
- No excessive shadows/gradients
- Performance optimized, clean minimal M3
- Keystore directly in repo (per requirement)
- Local-first (no backend, Room database)

## Key Decisions:
- Jetpack Compose + Material 3 (no XML layouts)
- Room for all local data storage
- Hilt for DI, WorkManager for background tasks
- Android PdfRenderer API (no third-party PDF library)
- Two product flavors: modern (minSdk 28) and legacy (minSdk 24)
- DataStore for preferences (dark mode, username, notifications)
- Sample data seeded via WorkManager on first launch

## State:
- Done:
  - Full project structure with Gradle (Kotlin DSL)
  - 5 Room entities, 4 DAOs, database
  - 5 repositories + 2 Hilt modules
  - M3 theme with Poppins fonts, light/dark color schemes
  - All 9 screens fully implemented (Home, Library, Search, Forum, PostDetail, CreatePost, Reply, PdfReader, Settings)
  - Navigation with bottom bar (4 tabs) + standalone screens
  - PDF viewer with annotation overlay (highlight, underline, sticky notes)
  - Content categorization (subject, grade, type filters)
  - Sample data (20 resources, 6 forum posts, 5 replies)
  - GitHub Actions workflows (build-release + lint)
  - Release keystore generated and committed
  - Poppins font files downloaded
  - Notification workers (DataSeeder + NotificationWorker)
  - AGENTS.md and CONTINUITY.md documentation
- Now: Final verification and cleanup
- Next: N/A - all tasks complete

## Open Questions (UNCONFIRMED if needed):
- None

## Working Set (files/ids/commands):
- 47 Kotlin source files (5,651 lines total)
- 9 resource/config XML files
- 2 GitHub Actions workflows
- 5 Poppins TTF font files
- 1 release keystore
- Gradle wrapper (8.5) + build configs
