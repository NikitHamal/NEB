# Android App Revamp — Changes & Outstanding Gaps

Reference design: the live website (https://nebians.consica.com.np/) and its
Material 3 design tokens in `backend_python/web/static/web/css/material3.css`.
Goal: bring the Kotlin/Compose Android app to parity with the website's design
system and fix/extend the backend APIs the app depends on.

This document records what was changed and what still needs doing, so the work
can be continued or deployed deliberately.

---

## 1. Theme tokens — `app/.../ui/theme/Color.kt`

Aligned the Compose color scheme with `material3.css` custom properties.

- **Light scheme** secondary/tertiary groups matched to the web tokens
  (`secondary #004AC6`, `secondaryContainer #DBE1FF`, `onSecondaryContainer #00174B`,
  `primaryContainer #DBE1FF`, `tertiary #56545A`, `tertiaryContainer #E5E1E8`, …).
- **Dark scheme** secondary group matched (`secondary #B4C5FF`, `onSecondary #002D78`,
  `secondaryContainer #003EA8`, `onSecondaryContainer #DBE1FF`).
- **Subject themes** rewritten via a `subjectTheme(color)` helper that derives a
  `container` (12% alpha tint) and `onContainer` (full color) from the base subject
  color — matching the web's `color-mix(8–12%, subject-color, transparent)` card headers.
  Keys: Physics, Chemistry, Mathematics/Math, Biology, English, Nepali,
  Computer Science, Economics, Accountancy, Exam Tips, General.
- **Badge themes** rewritten (`admin` crown, `moderator-blue/teal/purple`,
  `verified-blue/green/gold/black`) with `getBadgeKey(profile)` mapping from
  `isAdmin` / `moderatorLevel` / `verificationLevel`. Mirrors web `_user_badge_info()`.

---

## 2. API contract fixes — `app/.../data/api/ApiService.kt`

The backend mixes camelCase and snake_case per serializer. Android models were
aligned field-by-field against the actual Django serializers/views.

**Request bodies switched to camelCase** (to match backend expectations):
`ChangePasswordRequest`, `EmailResetPasswordRequest`, `UserProfileRequest`,
`ReplyCreateRequest`.

**Response models switched to camelCase**: `LikeResponse(thumbsUpCount, isThumbedUp)`,
`BookmarkResponse(isBookmarked)`, `ResourceLikeResponse(likeCount, isLiked)`.

**New / corrected models**: `ApiPaginatedReplies`, `ApiPaginatedNotifications`,
`ApiPaginatedBookmarks`, `ApiPaginatedFollows`, `ApiFollow` (snake_case),
`ApiUserStats` (snake_case), `NotificationsMarkReadRequest`.

**Interface changes**: `getReplies` → paginated; `getProfileStats` added
(`GET users/profile/{username}/stats/`); `getFollowers`/`getFollowing` paginated;
`getBookmarks` paginated; `getNotifications` paginated (+`unread_only`);
`markNotificationsRead` posts `NotificationsMarkReadRequest(markAll=true)`.

> Note: `UserProfileResponse` / `ApiFollow` use snake_case fields — verified correct
> against backend `UserSerializer` / `FollowSerializer`. Do **not** "fix" these to camelCase.

### Repository wiring
- `ForumRepository.getReplies` reads `.replies` off the paginated response.
- `AuthRepository.refreshProfile` now fetches stats separately via `getProfileStats`
  (the profile endpoint carries no counters) and populates follower/following/post/
  reply/contribution counters from `stats`.

---

## 3. Backend routes/views added — `backend_python/api/{urls,views}.py`

The app called these but they returned 404. Added, reusing existing services/logic:

- `POST resources/<id>/like/` → `resource_like` (uses `services.toggle_resource_like`).
- `POST posts/<id>/archive/` → `post_archive` (author-only; toggles `is_archived`;
  broadcasts `post_deleted`).
- `POST replies/<id>/archive/` → `reply_archive` (analogous).
- Wired the existing notification views: `notifications/`, `notifications/mark-read/`,
  `notifications/unread-count/`.

---

## 4. Screen revamp (this pass)

### New shared component — `ui/components/UserAvatar.kt`
Circular avatar that loads `photoUrl` via Coil (`SubcomposeAsyncImage`) and falls back
to the author's initial on a tinted circle while loading / on error / when no photo.
The backend already returns `authorPhotoUrl` (posts/replies) and `photoUrl` (users),
but every screen previously rendered initials only. Now wired into:

- **HomeScreen** — forum activity list items.
- **ForumScreen** — post cards.
- **ForumPostDetailScreen** — post header + reply items (replies use the
  secondaryContainer tint).
- **ProfileScreen** — 96dp header avatar.
- **NotificationsScreen** — actor avatars.
- **SettingsScreen** — account header.

### ProfileScreen + ProfileViewModel
Was a bare text stub. Now:
- Fetches `getProfileStats` alongside the profile (counters previously showed 0).
- Renders avatar, display name, `@username`, bio, a stats row
  (Followers / Following / Posts / Score), and a **Follow / Following** toggle
  (or **Edit Profile** when viewing your own profile via `isSelf`).
- `toggleFollow()` (previously unused) is now wired to the button.

### NotificationsScreen
- Added a **Mark all read** top-bar action (wired to the previously-unused
  `markAllRead()`).
- Notification rows show the actor avatar, bold the message when unread, and are
  clickable: post notifications open the post; others open the actor's profile.

---

## 5. Outstanding gaps / recommendations

These were identified but **not** changed (either out of safe scope, or they need a
product decision). Listed so they can be picked up deliberately.

1. **Forum author badges not exposed via API.** `PostSerializer` / `ReplySerializer`
   return `authorPhotoUrl` but not a badge. The web computes badges in the view layer
   (`_user_badge_info`). The Android `ApiPost.authorBadge` / `ApiReply.authorBadge`
   fields exist but are always null. *Recommendation:* add an `authorBadge`
   `SerializerMethodField` (string key, e.g. `admin`/`moderator`/`verified`/`teacher`/`bot`)
   to both serializers — additive and safe for web (which doesn't use these serializers).

2. **No extended Material icons dependency.** `material-icons-extended` is intentionally
   absent (APK size). Rendering verified/shield/crown/bot badge glyphs needs either that
   dependency or small bundled vector drawables. Until then, badges aren't rendered on
   Android even where the data is available.

3. **Post/reply bookmark state not exposed via API.** Serializers don't return
   `isBookmarked`; the Android fields are always null. Forum cards therefore can't show
   bookmark/share/report/follow actions like the web does. Needs serializer fields +
   Compose action bar work.

4. **Search returns no users.** `search_all` returns only `{resources, posts}`.
   `ApiSearchResponse.users` stays empty. The web search has no users tab either, so this
   is consistent — revisit only if a users tab is wanted on mobile.

5. **`/api/users/search/` does not exist.** `ApiService.searchUsers` has no backend route
   and no caller. Leave as-is or remove.

6. **Resource comments mismatch.** No `createResourceComment` route is wired, and
   `services._serialize_resource_comment` returns camelCase while Android
   `ApiResourceComment` expects snake_case. Reconcile before using resource comments.

7. **ProfileScreen is still partial vs web.** No banner image and no user-posts list/tab
   yet (`onPostClick`/`onFollowerClick` callbacks are currently unused). Add when the
   posts-by-user endpoint usage is wired.

---

## 6. Verification status

- Backend Python changes validated with `py_compile` (syntax OK).
- Android changes were **not** compiled in this environment (no Android SDK). Kotlin was
  written conservatively (local vals for smart-casts, standard Compose/Coil APIs only).
  Run `./gradlew assembleModernDebug` before shipping.
