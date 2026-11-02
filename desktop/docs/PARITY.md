# Android / web → desktop parity

Android navigation is `ui/Navigation.kt` (`NavHost`). Status: ✅ implemented and functional · 🌐 handed to the website on purpose · ⛔ not in the desktop app (see LIMITATIONS.md).

| Android screen | Desktop | Notes |
|---|---|---|
| Splash | ✅ `screens/splash.rs` | brand mark, routes to Login / Onboarding / Home from saved state |
| Login (Google · GitHub · email · guest) | ✅ `screens/login.rs` | Google/GitHub via **browser hand-off** (`data/browser_auth.rs`, backend `api/desktop_auth.py`) — same accounts as Android/web; desktop split layout + compact layout |
| EmailAuth (sign in / sign up) | ✅ `screens/email_auth.rs` | real `auth/email/*` calls |
| EmailVerification | ✅ same screen, Verify mode | code + resend |
| ForgotPassword | ✅ same screen, Forgot → Reset modes | emails a code, then `reset-password/` |
| CompleteProfile | ✅ `screens/complete_profile.rs` | after first Google/GitHub sign-up; live username availability |
| Onboarding | ✅ `screens/onboarding.rs` | role / level / subjects / place / school / avatar |
| Home | ✅ `screens/home.rs` | greeting, search, continue studying, shortcuts |
| Library / syllabus hub / category / subject | ✅ `library.rs`, `subject.rs` | reads the repo's content |
| StudyReader | ✅ `reader.rs` + `reader/` | HTML→native renderer, maths, MCQ practice, TOC, zoom |
| Search | ✅ `search.rs` | local index over all chapters (Ctrl+K) |
| Bookmarks | ✅ `bookmarks.rs` | local chapters; community posts are saved to the account via `bookmarks/toggle/` |
| Downloads | ✅ `downloads.rs` | study-book PDFs, offline |
| Forum (feed, post detail, replies, composer) | ✅ `community.rs` | live `posts/`, like, bookmark, reply, anonymous posting, categories, pagination |
| Notifications | ✅ `notifications.rs` | live list, unread badge (polled), mark-all-read, opens the referenced thread |
| Profile / EditProfile | ✅ `profile.rs` | local + synced: pulled after sign-in, pushed on "Done" |
| Settings | ✅ `settings.rs` | theme, reader prefs, content folder, **change password**, sign-out (revokes token), reset |
| AccountSecurity / DeleteAccount | 🌐 | opens the website (needs email-change & deletion confirmation UX) |
| Legal / About | ✅ `about.rs`, links | |
| Neby AI, StudyLab/Space, Canvas, Marketplace, Upload, People, Results, Analytics, Credits, Interactive lessons | ⛔ / 🌐 | web app tile + About open the website |

Navigation model: Android's bottom bar (Home · Library · Canvas) + profile → desktop **navigation rail** (≥1000 px: labelled; ≥760 px: compact) and **bottom bar** below 760 px, with the same pill indicator.
