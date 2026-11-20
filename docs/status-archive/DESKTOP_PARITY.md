# Android / web → desktop parity

Source of truth: `app/src/main/java/com/neb/ians/ui/Navigation.kt` (`sealed class Screen`) and `ui/screens/*`.

| Android screen (route) | Desktop | Status / how |
|---|---|---|
| Splash (`splash`) | `screens/splash.rs` | Same timeline as `SplashScreen.kt` (80 ms paper, 520 ms fade+settle 94→100 %, hold, push-forward fade). Always light. Honours *Reduce motion*. |
| Login (`login`) | `screens/login.rs` | "Welcome to **NEBians**", tagline copied from Android, *Continue with email*, *Continue as guest*, Terms/Privacy links. Google/GitHub sign-in need OS-browser OAuth callbacks → not in v0.1 (see LIMITATIONS). |
| EmailAuth / EmailVerification / ForgotPassword | `screens/email_auth.rs` | Sign in, create account, verify code, resend, forgot password — **live calls** to `api/auth/email/*` on `nebians.consica.com.np` (same endpoints/JSON as `ApiService.kt`). Server errors are surfaced verbatim. |
| CompleteProfile / Onboarding (13 steps) | `screens/onboarding.rs` | Welcome → Role → Name → Handle → Birthday → Gender → Level → Subjects → Place → Campus → Portrait → Bio → Finish, role-dependent step list identical to `stepsForRole()`, same copy, province + 75 districts. Stored locally. |
| Home | `screens/home.rs` | Greeting hero + search pill, quick actions, *Continue studying*, *Featured study guide* (rotates daily), *Browse by level*, *New in Library*. Feed/forum posts are server data → replaced by local study content. |
| Library (+ subject filter) | `screens/library.rs` | Categories (Class 8/10/11/12, CEE, IOE) + filterable all-subjects grid; category page groups subjects (compulsory/optional/science/entrance). |
| StudyReader (`study/{grade}/{subject}/{kind}/{no}`) | `screens/subject.rs`, `screens/reader.rs` | Subject page (units, question banks, exam guide, syllabus tab with topics & chapter summaries, progress). Reader renders the exported chapter HTML natively: callout boxes, tables, SVG/WebP figures, LaTeX maths, code, collapsible answers, **interactive MCQs with score**, TOC with live highlight, text size, reading width, bookmarks, mark-as-read, resume position, prev/next, timed-test clock for IOE model papers. |
| Search | `screens/search.rs` | Instant index of subjects/units/topics + cancellable full-text scan of all ~750 chapters; keyboard navigable; highlighted snippets. |
| Bookmarks | `screens/bookmarks.rs` | Saved chapters + reading history. |
| Downloads | `screens/downloads.rs` | Offline library: footprint of the local content, built study-book PDFs (42 in repo): open, save copy, reveal. |
| Settings | `screens/settings.rs` | Account, Preferences (theme, text size, width, TOC, Nepali names, reduce motion, remember window), Content folder, Keyboard, About (privacy/terms/version), Account control (sign out / reset). |
| Profile / EditProfile | `screens/profile.rs` | View + inline edit, avatar tone, stats. |
| (web) About | `screens/about.rs` | Version, library stats, links. |
| PdfViewer | — | PDFs open in the system viewer (no in-app PDF renderer). |
| Forum, News, Notifications, People, Neby AI, Study Lab/Space, Canvas, Marketplace, Upload, Analytics, Results, Tools, Credits, Avatar | — | Server-backed (accounts, uploads, AI). Not re-implemented; the *Web app* tile and About page link to them. |

Design language mirrored: paper-white/graphite mono palette with brand blue `#004AC6` (dark `#B4C5FF`), Poppins, 14/18 dp radii, pill buttons, hairline separators, static empty states, no ripples, no shadows (docs/DESIGN.md).
