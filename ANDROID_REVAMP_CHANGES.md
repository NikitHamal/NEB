# Android App Revamp — UI/UX + API Sync

This document records what was changed in the Android app to match the website
(https://nebians.consica.com.np/), the API contract fixes, and the remaining
backend/app work you can pick up later.

> Context: the container has no Android SDK / JDK, so the Kotlin code here was
> **not compiled**. Every edit was made against the verified backend contract in
> `backend_python/api/views.py` and `serializers.py`. Build the app locally
> (`./gradlew assembleModernDebug`) to confirm before release.

---

## 1. API contract fixes (`app/.../data/api/ApiService.kt`)

The app's serializers had drifted from the backend. These were corrected so the
JSON the server returns actually deserializes:

| Model / method | Was | Now (matches backend) |
|---|---|---|
| `ReplyCreateRequest` | `parent_reply_id` | `parentReplyId` (backend reads camelCase) |
| `LikeResponse` | `like_count` / `is_liked` | `thumbsUpCount` / `isThumbedUp` |
| `BookmarkResponse` | snake_case | `isBookmarked` |
| `ApiNotificationListResponse` | flat list | DRF paginated `{results,count,next,previous}` (+ `hasMore`) |
| `MarkReadRequest` | — | `{mark_all, notification_ids}` (added) |
| `ApiNotificationMarkReadResponse` | — | `{success, marked_count}` (added) |
| `getReplies` | returned `List` | returns `ApiPaginatedReplies` + `page` query param |
| `getUserStats` | did not exist | `GET api/users/profile/{username}/stats/` → `UserStatsResponse` (added) |
| `checkBookmark` | `@POST`+`@Body` | `@GET` with `target_type`/`target_id` query params |
| `markNotificationsRead` | empty body | default body `MarkReadRequest(markAll = true)` |

`ApiPaginatedReplies` and `UserStatsResponse` data classes were added.

### Repository
- `ForumRepository.getReplies(postId, page)` now unwraps `response.replies` from
  the paginated envelope.

---

## 2. Backend fix (`backend_python/api/views.py`)

- **`user_profile_stats`** was missing `@permission_classes([AllowAny])`, so it
  silently fell back to the project default `IsAuthenticated`. Its own docstring
  says "Public endpoint", and the website shows stats to guests — so guests were
  getting a 401. Added `@permission_classes([AllowAny])`.
- Notification routes (`notifications/`, `notifications/mark-read/`,
  `notifications/unread-count/`) were added to `api/urls.py` — the view functions
  existed but were never routed.

> **Deploy note:** `views.py` and `urls.py` changes must be deployed to the server
> (see CLAUDE.md → "How to Deploy"). No migration is involved.

---

## 3. UI/UX revamp

### New reusable component — `ui/components/UserAvatar.kt`
Coil-backed circular avatar: loads `photoUrl`, falls back to the first letter of
the name on a `primaryContainer` background (matching the website's avatar/initial
pattern). Configurable size + colors. Now used everywhere an avatar appears.

Applied to: ForumScreen post cards, ForumPostDetailScreen (post + replies),
HomeScreen forum-activity list, SettingsScreen profile row, NotificationsScreen,
ProfileScreen.

### ProfileScreen — full rebuild (`ui/screens/profile/`)
Was a bare stub (name + 3 numbers). Rebuilt to mirror the website profile page:
- Banner (banner_url image or `primaryContainer`)
- Overlapping circular avatar
- Display name + role badge chip (admin/moderator/verified, colors from `BadgeThemes`)
- `@username`
- Headline derived from `class_level` (`11`→Class 11, `Both`→Class 11 & 12,
  `Passout`→Graduate, `Teacher`→Teacher / Educator, `Bachelors`→Bachelors, bot→
  AI Study Companion, else "NEBians Member") + subjects
- Stats row (Followers / Following / Posts)
- Action buttons — self: Edit Profile + Share; other: Follow/Following + Share
- About / bio
- Meta rows (location = district+pradesh, school, joined date)
- Activity stats grid (Discussions, Replies, Followers, Likes Received,
  NEBian Score [highlighted], Following)

`ProfileViewModel` now fetches `getUserStats` alongside the profile (the profile
serializer does **not** include counters / follow-state), exposes `isSelf`,
`isFollowing`, `followerCount`, and a `followLoading` flag for the follow button.

### EditProfile — fixed routing (`ui/Navigation.kt`)
The `EditProfile` route rendered a "Coming Soon" stub. It now renders
`CompleteProfileScreen`, which already auto-detects edit mode and pre-fills the
cached profile. The stub file `EditProfileScreen.kt` was deleted.

### NotificationsScreen — polish
- "Mark all read" action in the top bar (only when unread exist)
- Actor avatar via `UserAvatar`
- Unread dot + semibold text for unread items
- Row is tappable → navigates to the related post, else to the actor's profile
- Divider between items, centered empty state

---

## 4. Verified-correct, left unchanged
- `BookmarkRepository` is local-only (Room) — the `checkBookmark` signature change
  has no broken callers.
- Theme/colors/typography (`ui/theme/`) already mirror `material3.css` exactly
  (primary `#004AC6` light / `#B4C5FF` dark, Poppins, subject + badge maps).
- `BASE_URL = https://nebians.consica.com.np/`.

---

## 5. Remaining / future work (not done here)
- **Share buttons** on Profile (self + other) are wired to no-op `onClick {}` —
  hook up an Android share `Intent` (share profile URL).
- **Mention button** from the website's "other user" profile is not ported
  (replaced with Share for now).
- **Followers/Following lists**: ProfileScreen's Followers stat calls
  `onFollowerClick(username)`; there is no dedicated followers/following list
  screen yet. APIs exist (`getFollowers`/`getFollowing`).
- **Role badge icons**: the app only bundles `material-icons-core`, which lacks
  `verified`/`shield`/`workspace_premium`. Badges currently use `Star`
  (admin/crown) and `CheckCircle` (verified/moderator) as approximations. Add the
  `material-icons-extended` dependency for exact icons.
- **Build verification**: compile + run on a device/emulator. Watch for unused
  imports left behind from the avatar refactor (warnings, not errors).
