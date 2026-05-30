## Goal (incl. success criteria):
Build a full modern minimalist M3-themed Android app called NEBians (com.neb.ians) for Nepali students with:
- Ebooks/PDF resources with categorization (subject, grade, type)
- Advanced PDF viewer with annotation tools (highlight, underline, sticky notes)
- Discussion forum with standalone screens
- Dark mode toggle, push notifications
- Poppins fonts, Google-style M3 UI/UX
- GitHub Actions workflow for 2 signed release APKs
- Keystore committed to repo
- Email signup with verification (6-digit code)
- Email login and password reset
- Google sign-in (existing)

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
- Email auth: 6-digit verification code sent via Django email backend
- Password hashing: SHA-256 (simple, matches existing pattern)
- Email verification required before email login

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
  - Email signup with verification (backend + Android + web)
  - Email login (backend + Android + web)
  - Password reset with verification code (backend + Android + web)
  - Email auth data models, API endpoints, repository methods
  - New screens: EmailSignupScreen, EmailLoginScreen, EmailVerificationScreen, ForgotPasswordScreen
  - Web templates: email_signup, email_login, email_verify, email_forgot
- Now: Email auth feature complete
- Next: Testing and deployment

## Open Questions (UNCONFIRMED if needed):
- Email SMTP configuration needed for production (currently defaults to console backend)
- SHA-256 password hashing — consider upgrading to bcrypt in future

## Working Set (files/ids/commands):
- 51+ Kotlin source files
- Django backend with email auth endpoints
- 4 new web templates for email auth
- 1 new migration for email auth fields
- email_utils.py for sending verification emails