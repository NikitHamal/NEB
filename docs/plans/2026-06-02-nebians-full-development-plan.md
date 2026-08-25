# NEBians Full Development Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform NEBians from a functional MVP into a production-grade platform with a polished website, professional admin panel, improved Android app, and hardened backend.

**Architecture:** Django web backend (Phusion Passenger + Redis), Android app (Jetpack Compose + Room), REST API (DRF). Changes are incremental — each phase ships independently.

**Tech Stack:** Django 5.2, DRF 3.15, MySQL/MariaDB, Redis, Jetpack Compose, Material 3, Room, Hilt, Retrofit

---

## Audit Summary

| Domain | Critical | High | Medium | Low |
|--------|----------|------|--------|-----|
| Backend API | 6 | 8 | 5 | 2 |
| Web Frontend | 4 | 6 | 15 | 7 |
| Admin Panel | 3 | 5 | 10 | 5 |
| Android App | 4 | 6 | 8 | 6 |

**Total: 82 issues identified across 4 domains.**

---

## Phase 1: Critical Security & Data Integrity Fixes (Week 1)

> Fixes that prevent data loss, security breaches, or production crashes. Ship these before any feature work.

### Task 1.1: Fix auth token regeneration bug
**Files:**
- Modify: `backend_python/api/views.py:967` (auth_email_login)

**Problem:** `auth_email_login` regenerates the auth token on every login, invalidating all other sessions (Android, web). AGENTS.md says tokens should NOT regenerate on login.

**Step 1:** Change `auth_email_login` to reuse existing token instead of regenerating

```python
# In auth_email_login, replace:
user.auth_token = User.generate_token()
user.save(update_fields=['auth_token'])

# With:
if not user.auth_token:
    user.auth_token = User.generate_token()
    user.save(update_fields=['auth_token'])
```

**Step 2:** Verify the fix by checking that `auth_google` already does this pattern correctly (it should)

**Step 3:** Commit

```bash
git add backend_python/api/views.py
git commit -m "fix: auth_email_login no longer regenerates token on every login"
```

---

### Task 1.2: Fix verification code purpose bypass
**Files:**
- Modify: `backend_python/api/views.py:134-140`

**Problem:** `_verify_user_code` with `purpose=None` skips the purpose check, allowing a signup code to reset a password.

**Step 1:** Make purpose mandatory in verification code verification

```python
# In _verify_user_code, change:
if purpose is not None and user.verification_code_purpose != purpose:

# To:
if user.verification_code_purpose != purpose:
    return False
```

Remove the cross-purpose allowance at lines 135-138 entirely.

**Step 2:** Update all callers to always pass purpose explicitly

**Step 3:** Test email signup, verify, login, forgot password flows

**Step 4:** Commit

---

### Task 1.3: Add rate limiting to OAuth auth endpoints
**Files:**
- Modify: `backend_python/api/views.py:187,341`
- Modify: `backend_python/api/throttles.py`

**Problem:** `auth_google` and `auth_github` have no rate limiting. An attacker can brute-force tokens.

**Step 1:** Add `AuthRateThrottle` to both endpoints decorators

```python
@throttle_classes([AuthRateThrottle])
def auth_google(request):
    ...

@throttle_classes([AuthRateThrottle])
def auth_github(request):
    ...
```

**Step 2:** Commit

---

### Task 1.4: Fix posts_endpoint and replies_endpoint missing counter increments
**Files:**
- Modify: `backend_python/api/views.py:1315-1326` (posts_endpoint POST)
- Modify: `backend_python/api/views.py:1370-1372` (replies_endpoint POST)

**Problem:** The dispatcher-based `posts_endpoint` POST handler and `replies_endpoint` POST handler skip counter increments and Neby mention checks that the dedicated `posts_create`/`replies_create` handlers perform.

**Step 1:** Add counter increments to `posts_endpoint` POST

```python
from api import counters as _counters
from api import neby as _neby

# After post creation in posts_endpoint POST:
_counters.increment_user_post_count(user.id)
_counters.increment_user_contribution_score(user.id, 'post')
_neby.enqueue_if_post_mention(post)
```

**Step 2:** Add Neby mention check to `replies_endpoint` POST

```python
# After reply creation in replies_endpoint POST:
_neby.enqueue_if_reply_mention(reply)
```

**Step 3:** Commit

---

### Task 1.5: Fix _link_oauth_user_model PK change danger
**Files:**
- Modify: `backend_python/api/views.py:326-332`

**Problem:** `existing.pk = user_pk` changes the primary key of a user row, which can cascade-delete FK references.

**Step 1:** Replace PK change with account merge pattern — update the OAuth fields on the existing account instead of changing PK

```python
# Instead of: existing.pk = user_pk; existing.save()
# Do: transfer OAuth data to the existing account
existing.google_id = user.google_id
existing.github_id = user.github_id
existing.photo_url = user.photo_url or existing.photo_url
existing.save(update_fields=['google_id', 'github_id', 'photo_url'])
# Then delete the duplicate: user.delete()
```

**Step 2:** Test Google and GitHub login flows

**Step 3:** Commit

---

### Task 1.6: Add select_for_update to toggle endpoints
**Files:**
- Modify: `backend_python/api/views.py:1516` (follow toggle)
- Modify: `backend_python/api/views.py:1175` (bookmark toggle)

**Problem:** Race conditions can create duplicate follows/bookmarks despite unique_together constraints.

**Step 1:** Wrap toggle logic in `transaction.atomic()` with `select_for_update()`

```python
from django.db import transaction

@transaction.atomic
def toggle_follow(request, user_id):
    existing = Follow.objects.select_for_update().filter(
        follower=request.user, following=target
    ).first()
    ...
```

**Step 2:** Same for bookmark_toggle

**Step 3:** Commit

---

### Task 1.7: Android — Fix critical security issues
**Files:**
- Modify: `app/build.gradle.kts:30-33` (keystore passwords)
- Modify: `app/src/main/java/com/neb/ians/data/api/ApiService.kt:706-708` (logging interceptor)
- Modify: `app/src/main/java/com/neb/ians/data/repository/AuthRepository.kt:27` (token storage)
- Modify: `app/src/main/java/com/neb/ians/di/AppModule.kt:38-44` (runBlocking)

**Problem:** Four P0 issues: keystore passwords in build config, HTTP BODY logging in production, auth token in unencrypted DataStore, runBlocking deadlock risk.

**Step 1:** Move keystore passwords to `local.properties` or environment variables

```kotlin
// build.gradle.kts
val keystorePassword = System.getenv("KEYSTORE_PASSWORD") 
    ?: project.findProperty("KEYSTORE_PASSWORD") as? String 
    ?: throw GradleException("KEYSTORE_PASSWORD not set")
```

**Step 2:** Set logging level to NONE in release builds

```kotlin
val logger = HttpLoggingInterceptor().apply {
    level = if (BuildConfig.DEBUG) HttpLoggingInterceptor.Level.BODY 
            else HttpLoggingInterceptor.Level.NONE
}
```

**Step 3:** Replace `runBlocking` in AppModule token provider with an OkHttp Interceptor

```kotlin
class AuthInterceptor(private val dataStore: DataStore<Preferences>) : Interceptor {
    override fun intercept(chain: Chain): Response {
        val token = runCatching { 
            runBlocking { dataStore.data.map { it[stringPreferencesKey("auth_token")] }.first() }
        }.getOrNull()
        val request = if (token != null) {
            chain.request().newBuilder().header("Authorization", "Bearer $token").build()
        } else chain.request()
        return chain.proceed(request)
    }
}
```

**Step 4:** Migrate auth token to EncryptedSharedPreferences (or accept DataStore risk for now with a TODO)

**Step 5:** Commit

---

## Phase 2: Admin Panel Redesign (Weeks 2-3)

> Transform the admin panel from a collection of inline-styled pages into a composed, professional M3 admin dashboard.

### Task 2.1: Create admin.css — extract all inline styles
**Files:**
- Create: `backend_python/web/static/web/css/admin.css`
- Modify: All 10 admin templates

**Problem:** 212+ inline `style=` attributes across admin templates. Two different toggle switch implementations. Hardcoded hex colors. No responsive grid system.

**Step 1:** Create `admin.css` with extracted utility classes

```css
/* Layout */
.admin-header-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.admin-stat-bar { display: flex; align-items: center; gap: 12px; }
.admin-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.admin-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
@media (max-width: 768px) { .admin-grid-2, .admin-grid-3 { grid-template-columns: 1fr; } }

/* Form elements */
.admin-form-input { width: 100%; padding: 10px 12px; border-radius: 8px; border: 1px solid var(--md-outline); background: var(--md-surface); color: var(--md-on-surface); font-family: var(--md-font); font-size: 0.875rem; }
.admin-form-input:focus { border-color: var(--md-primary); outline: none; }

/* Status badges */
.admin-status-active { color: var(--md-primary); }
.admin-status-locked { color: var(--md-error); }
.admin-status-verified { color: #00897B; } /* teal */
.admin-status-moderator { color: #F59E0B; } /* amber */
.admin-status-admin { color: #7B1FA2; } /* purple */
.admin-status-bot { color: #1B9AF0; } /* blue */

/* Search input */
.admin-search-input { border: none; background: transparent; outline: none; color: var(--md-on-surface); font-family: var(--md-font); font-size: 0.875rem; padding: 8px 0; }
```

**Step 2:** Replace inline styles in all 10 admin templates with these classes

**Step 3:** Commit

---

### Task 2.2: Add pagination to all admin list views
**Files:**
- Modify: `backend_python/web/views.py` (admin_users, admin_resources, admin_posts)
- Modify: `backend_python/web/templates/admin_panel/users.html`
- Modify: `backend_python/web/templates/admin_panel/resources.html`
- Modify: `backend_python/web/templates/admin_panel/posts.html`

**Problem:** Admin list views load ALL records. No pagination, no search filters by role/status.

**Step 1:** Add Django Paginator to admin views (20 items per page)

```python
from django.core.paginator import Paginator

def admin_users(request):
    users = User.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 20)
    users_page = paginator.get_page(page)
    return render(request, 'admin_panel/users.html', {
        'users': users_page,
        'page_obj': users_page,
    })
```

**Step 2:** Add pagination controls to each template (prev/next, page numbers)

**Step 3:** Add search/filter controls (by role, status, verification level)

**Step 4:** Commit

---

### Task 2.3: Fix admin panel accessibility
**Files:**
- Modify: `backend_python/web/templates/admin_panel/base.html`
- Modify: `backend_python/web/static/web/css/admin.css`

**Problem:** No keyboard navigation on mobile nav, no skip-to-content link, toggle switches not accessible, focus-visible outlines removed on form elements, tables lack ARIA labels.

**Step 1:** Add focus trap to mobile nav overlay (Escape key handler, focus lock)

**Step 2:** Add `aria-label` to all tables, `aria-checked` to toggle switches

**Step 3:** Restore `:focus-visible` on form elements (remove `outline: none` override)

**Step 4:** Add skip-to-content link at top of base template

**Step 5:** Commit

---

### Task 2.4: Unify toggle switch implementation
**Files:**
- Modify: `backend_python/web/templates/admin_panel/bot_config.html`
- Modify: `backend_python/web/static/web/css/admin.css`

**Problem:** `bot_config.html` has a custom inline toggle switch that duplicates the `.md-switch` component in `app.css`.

**Step 1:** Replace custom toggle in bot_config.html with `.md-switch` component

**Step 2:** Remove the duplicate toggle CSS from `bot_config.html` extra_css block

**Step 3:** Remove the dead JS event listener from bot_config.html extra_js block

**Step 4:** Commit

---

### Task 2.5: Add resource type filter, bulk actions, and form validation to admin
**Files:**
- Modify: `backend_python/web/templates/admin_panel/resources.html`
- Modify: `backend_python/web/templates/admin_panel/resource_edit.html`
- Modify: `backend_python/web/views.py`

**Problem:** Resource type options are hardcoded and inconsistent between add and edit forms. No bulk actions. No client-side validation.

**Step 1:** Create a shared `RESOURCE_TYPES` constant in views.py and pass it to both add and edit templates

**Step 2:** Add checkbox column for bulk selection + "Delete Selected" action

**Step 3:** Add `required` attributes to edit form fields (title, subject, file_url)

**Step 4:** Add a "Delete Resource" danger zone to the edit page

**Step 5:** Commit

---

### Task 2.6: Add admin dashboard enhancements
**Files:**
- Modify: `backend_python/web/templates/admin_panel/dashboard.html`
- Modify: `backend_python/web/views.py`

**Problem:** Dashboard has no time range selector, no interactive charts, emoji instead of icons, division-by-zero risk, no "view all" links.

**Step 1:** Replace emoji (👍💬) with Material Symbols icons

**Step 2:** Add "View All" links on Recent Users and Top Posts cards

**Step 3:** Fix division-by-zero in resource type bar chart (add `max(total_resources, 1)`)

**Step 4:** Add simple date range filter (Last 7 days / 30 days / All time) for stats

**Step 5:** Commit

---

## Phase 3: Website UX Improvements (Weeks 3-4)

> Polish the public-facing website for better user experience, accessibility, and performance.

### Task 3.1: Fix keyboard accessibility on base template
**Files:**
- Modify: `backend_python/web/templates/base.html`

**Problem:** Profile dropdown has no keyboard nav, notification badge has no aria-label, theme toggle has no aria-pressed, no skip-to-content link.

**Step 1:** Add Escape key handler to close profile dropdown

**Step 2:** Add `aria-pressed` to theme toggle button

**Step 3:** Add `aria-label` to notification badge ("X unread notifications")

**Step 4:** Add skip-to-content link (`<a href="#main" class="skip-link">Skip to content</a>`)

**Step 5:** Move `style="display:none"` toggles to CSS classes (`.hidden`)

**Step 6:** Commit

---

### Task 3.2: Fix notification polling performance
**Files:**
- Modify: `backend_python/web/templates/base.html`

**Problem:** Notification polling runs every 60s even when tab is backgrounded.

**Step 1:** Add Page Visibility API check

```javascript
let notifInterval;
function startNotifPolling() {
    notifInterval = setInterval(fetchNotifCount, 60000);
}
function stopNotifPolling() {
    clearInterval(notifInterval);
}
document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopNotifPolling();
    else { fetchNotifCount(); startNotifPolling(); }
});
startNotifPolling();
```

**Step 2:** Commit

---

### Task 3.3: Fix XSS risk in post content rendering
**Files:**
- Modify: `backend_python/web/templatetags/web_extras.py`
- Modify: `backend_python/web/templates/admin_panel/post_detail.html`

**Problem:** Post content uses `white-space:pre-wrap` with `mention_links` filter. Need to verify that the filter properly escapes HTML before rendering markdown.

**Step 1:** Audit `mention_links` filter for HTML escaping

**Step 2:** Add `escapeHtml()` call before markdown rendering in the filter

**Step 3:** Use `{{ post.content|escape|mention_links }}` in templates (or ensure the filter escapes first)

**Step 4:** Commit

---

### Task 3.4: Refactor web/views.py into modules
**Files:**
- Create: `backend_python/web/views/pages.py` (page rendering views)
- Create: `backend_python/web/views/ajax.py` (AJAX endpoint views)
- Create: `backend_python/web/views/auth.py` (Google/GitHub/email auth views)
- Create: `backend_python/web/views/admin.py` (admin panel views)
- Create: `backend_python/web/views/serializers.py` (_serialize_* functions)
- Modify: `backend_python/web/views.py` (re-export all for backward compat)
- Modify: `backend_python/web/urls.py` (update imports if needed)

**Problem:** `web/views.py` is 2955 lines. It should be split for maintainability.

**Step 1:** Create the 5 new module files, moving functions to appropriate modules

**Step 2:** Keep `web/views.py` as a re-export shim for backward compatibility

```python
from web.views.pages import *
from web.views.ajax import *
from web.views.auth import *
from web.views.admin import *
from web.views.serializers import *
```

**Step 3:** Verify all URL patterns still resolve

**Step 4:** Commit

---

### Task 3.5: Eliminate code duplication between views.py and services.py
**Files:**
- Modify: `backend_python/api/views.py`
- Modify: `backend_python/api/services.py`

**Problem:** `toggle_post_like`, `toggle_reply_like`, `create_reply`, `create_post`, `toggle_follow` are implemented in both files with nearly identical logic.

**Step 1:** Move all shared logic to `services.py` as the single source of truth

**Step 2:** Have `views.py` call `services.py` functions instead of reimplementing

**Step 3:** Have `web/views.py` already calls `services.py` — no change needed there

**Step 4:** Commit

---

### Task 3.6: Add content length limits and rate limiting
**Files:**
- Modify: `backend_python/api/views.py`
- Modify: `backend_python/api/throttles.py`

**Problem:** No content length limits on posts/replies. No rate limiting on content creation.

**Step 1:** Add `ContentCreateThrottle` (20/hour for authenticated users)

```python
class ContentCreateThrottle(UserRateThrottle):
    rate = '20/hour'
```

**Step 2:** Add throttle to `posts_create`, `replies_create`, `user_profile_create_or_update`

**Step 3:** Add content length validation in views

```python
MAX_POST_CONTENT_LENGTH = 50000  # 50KB
MAX_REPLY_CONTENT_LENGTH = 20000  # 20KB
if len(content) > MAX_POST_CONTENT_LENGTH:
    return Response({'error': 'Content too long'}, status=400)
```

**Step 4:** Commit

---

## Phase 4: Android App Improvements (Weeks 4-6)

> Fix critical bugs, add missing features, improve performance and UX.

### Task 4.1: Fix HomeViewModel parallel API calls
**Files:**
- Modify: `app/src/main/java/com/neb/ians/ui/screens/home/HomeViewModel.kt:48-64`

**Problem:** Three independent API calls are made sequentially, doubling/tripling load time.

**Step 1:** Convert to parallel calls with `async`/`awaitAll`

```kotlin
val deferredResources = async { apiService.getResources(token, sort = "newest", page = 1) }
val deferredPopular = async { apiService.getResources(token, sort = "relevant", page = 1) }
val deferredPosts = async { apiService.getPosts(token) }
val resourcesResult = deferredResources.await()
val popularResult = deferredPopular.await()
val postsResult = deferredPosts.await()
```

**Step 2:** Commit

---

### Task 4.2: Make HomeScreen forum posts clickable
**Files:**
- Modify: `app/src/main/java/com/neb/ians/ui/screens/home/HomeScreen.kt:368-438`
- Modify: `app/src/main/java/com/neb/ians/ui/Navigation.kt`

**Problem:** ForumPostItem on HomeScreen has no click handler. `onPostClick` callback is never passed.

**Step 1:** Add `onPostClick: (String) -> Unit` parameter to HomeScreen composable

**Step 2:** Wire it through Navigation.kt to navigate to forum post detail

**Step 3:** Add `Modifier.clickable { onPostClick(post.id) }` to ForumPostItem

**Step 4:** Commit

---

### Task 4.3: Add pull-to-refresh on Home, Forum, and Notifications screens
**Files:**
- Modify: `HomeScreen.kt`, `ForumScreen.kt`, `NotificationsScreen.kt`
- Modify: `HomeViewModel.kt`, `ForumViewModel.kt`, `NotificationsViewModel.kt`

**Problem:** No swipe-to-refresh on any screen.

**Step 1:** Wrap each screen's content in `PullToRefreshBox` (Material 3)

```kotlin
val isRefreshing by viewModel.isRefreshing.collectAsState()
PullToRefreshBox(isRefreshing = isRefreshing, onRefresh = { viewModel.refresh() }) {
    // existing content
}
```

**Step 2:** Add `isRefreshing` state and `refresh()` function to each ViewModel

**Step 3:** Commit

---

### Task 4.4: Add pagination to Forum and Library screens
**Files:**
- Modify: `ForumViewModel.kt`, `ForumScreen.kt`
- Modify: `LibraryViewModel.kt`, `LibraryScreen.kt`

**Problem:** Only the first page of posts/resources is ever loaded.

**Step 1:** Add `page` and `hasMore` fields to ForumUiState and LibraryUiState

**Step 2:** Add `loadMore()` function to ViewModels that increments page and appends results

**Step 3:** Add `item { }` at end of LazyColumn that triggers `loadMore()` when visible

**Step 4:** Commit

---

### Task 4.5: Implement FCM push notifications
**Files:**
- Create: `app/src/main/java/com/neb/ians/util/NEBiansFCMService.kt` (stub exists, implement fully)
- Modify: `AndroidManifest.xml` (add service declaration)

**Problem:** Firebase Messaging dependency exists but no `FirebaseMessagingService` implementation.

**Step 1:** Implement `onMessageReceived()` to show notification with post/reply deep link

**Step 2:** Implement `onNewToken()` to call `apiService.registerFcmToken()`

**Step 3:** Add `<service>` declaration in AndroidManifest.xml

**Step 4:** Commit

---

### Task 4.6: Add error body parsing from API responses
**Files:**
- Modify: `app/src/main/java/com/neb/ians/data/api/ApiService.kt`
- Modify: All ViewModels

**Problem:** When server returns 4xx/5xx, ViewModels show generic "Something went wrong" instead of the actual server error message.

**Step 1:** Create a `ApiResult<T>` sealed class that parses error bodies

```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val message: String, val code: Int) : ApiResult<Nothing>()
}
```

**Step 2:** Create an extension function on `Response<T>` to extract error messages

```kotlin
fun <T> Response<T>.toApiResult(): ApiResult<T> {
    return if (isSuccessful) {
        ApiResult.Success(body()!!)
    } else {
        val errorBody = errorBody()?.charStream()?.readText()
        val message = try {
            JSONObject(errorBody ?: "").optString("error", message())
        } catch (_: Exception) { message() }
        ApiResult.Error(message, code())
    }
}
```

**Step 3:** Update ViewModels to use `ApiResult` and show server error messages

**Step 4:** Commit

---

### Task 4.7: Add bookmark UI to forum posts
**Files:**
- Modify: `ForumPostDetailScreen.kt`
- Modify: `ForumRepository.kt`

**Problem:** API has bookmark endpoints but app has no bookmark UI.

**Step 1:** Add bookmark icon button to post action bar

**Step 2:** Call `apiService.toggleBookmark()` on tap, update UI state

**Step 3:** Show filled bookmark icon when `isBookmarked` is true

**Step 4:** Commit

---

### Task 4.8: Fix nested scrollable containers
**Files:**
- Modify: `HomeScreen.kt:115-242`
- Modify: `ForumScreen.kt:127-221`

**Problem:** HomeScreen uses `Column { verticalScroll() }` containing `LazyRow`s. This forces all children to compose even when off-screen.

**Step 1:** Replace outer `Column + verticalScroll` with `LazyColumn` in HomeScreen

**Step 2:** Use `item { }` blocks for static content and `items { }` for lists

**Step 3:** Same fix for ForumScreen error+content layout

**Step 4:** Commit

---

### Task 4.9: Add PDF reader pinch-to-zoom
**Files:**
- Modify: `PdfReaderScreen.kt:321-328`

**Problem:** PDF pages render as fixed `Image` with no zoom/pan support.

**Step 1:** Add `rememberTransformableState` for zoom/pan

```kotlin
var scale by remember { mutableFloatStateOf(1f) }
var offset by remember { mutableStateOf(Offset.Zero) }
val transformableState = rememberTransformableState { zoomChange, panChange, _ ->
    scale = (scale * zoomChange).coerceIn(1f, 5f)
    offset = offset + panChange
}
Image(
    bitmap = bitmap!!, 
    contentDescription = "Page $currentPage",
    modifier = Modifier.pointerInput(Unit) { detectTransformGestures { _, pan, zoom -> ... } }
        .graphicsLayer { scaleX = scale; scaleY = scale; translationX = offset.x; translationY = offset.y }
)
```

**Step 2:** Add double-tap to reset zoom

**Step 3:** Commit

---

### Task 4.10: Remove hardcoded version and add BuildConfig reference
**Files:**
- Modify: `app/src/main/java/com/neb/ians/ui/screens/settings/SettingsScreen.kt:244`

**Problem:** Version string is hardcoded as "1.0.0 (Stable Release)".

**Step 1:** Replace with `BuildConfig.VERSION_NAME`

```kotlin
supportingContent = { Text("${BuildConfig.VERSION_NAME} (${BuildConfig.BUILD_TYPE})") }
```

**Step 2:** Commit

---

## Phase 5: Backend Performance & Quality (Week 6)

> Fix N+1 queries, add missing indexes, improve API consistency.

### Task 5.1: Fix _build_stats_batch to use denormalized counters
**Files:**
- Modify: `backend_python/api/views.py:1413-1460`

**Problem:** `_build_stats_batch` always runs 6 aggregate queries, ignoring denormalized counters.

**Step 1:** Modify to check `user.post_count > 0` first (like `_build_stats` does)

```python
def _build_stats_batch(user_ids):
    users = User.objects.filter(pk__in=user_ids)
    stats = {}
    for user in users:
        if user.post_count > 0:  # use denormalized counters
            stats[user.id] = {
                'post_count': user.post_count,
                'reply_count': user.reply_count,
                'follower_count': user.follower_count,
                'following_count': user.following_count,
                'likes_given': user.likes_given_count,
                'likes_received': user.likes_received_count,
            }
        else:
            stats[user.id] = _build_stats_fallback(user.id)
    return stats
```

**Step 2:** Commit

---

### Task 5.2: Fix N+1 queries in web serializers
**Files:**
- Modify: `backend_python/web/views.py:142-281`

**Problem:** `_serialize_posts` and `_serialize_replies` call `_user_badge_info()` per item, and replies don't `select_related('post')`.

**Step 1:** Batch-prefetch badge info for all users in one query

```python
def _serialize_posts(posts, user=None):
    # Batch load badge info for all post authors
    user_ids = set(p.user_id for p in posts)
    badge_map = {}
    for uid in user_ids:
        u = User.objects.get(pk=uid)  # or batch query
        badge_map[uid] = _user_badge_info(u)
    ...
```

**Step 2:** Add `select_related('post')` to reply querysets

**Step 3:** Commit

---

### Task 5.3: Add database index for email lookups
**Files:**
- Create: new migration file

**Problem:** `User.objects.get(email__iexact=email)` cannot use B-tree index for case-insensitive search.

**Step 1:** Create migration adding a `LowerEmail` index

```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('api', '0023_rename_neby_tasks_status_created_idx_...')]
    operations = [
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='email_lower_idx', opclasses=['varchar_pattern_ops']),
        ),
    ]
```

**Step 2:** For MySQL, also add a `LOWER(email)` virtual column with index (or use `LIKE 'exact@email.com'` with case-insensitive collation)

**Step 3:** Commit

---

### Task 5.4: Standardize API response format
**Files:**
- Modify: `backend_python/api/views.py`

**Problem:** Inconsistent response formats — some use `{'status': 'success'}`, some use `{'success': True}`, some use `{'error': 'message'}`.

**Step 1:** Create a standard response helper

```python
def api_response(data=None, message=None, status=200):
    response = {}
    if data is not None:
        response.update(data)
    if message:
        response['message'] = message
    return Response(response, status=status)

def api_error(message, status=400):
    return Response({'error': message}, status=status)
```

**Step 2:** Gradually replace individual `JsonResponse`/`Response` calls with these helpers (can be done incrementally)

**Step 3:** Commit

---

### Task 5.5: Add health check endpoint
**Files:**
- Modify: `backend_python/api/urls.py`
- Create: `backend_python/api/health.py`

**Step 1:** Create health check view

```python
def health_check(request):
    from django.db import connection
    from django.core.cache import cache
    checks = {'database': False, 'cache': False}
    try:
        connection.ensure_connection()
        checks['database'] = True
    except Exception:
        pass
    try:
        cache.set('health', 'ok', 1)
        checks['cache'] = cache.get('health') == 'ok'
    except Exception:
        pass
    status = 200 if all(checks.values()) else 503
    return JsonResponse({'status': 'ok' if status == 200 else 'degraded', 'checks': checks}, status=status)
```

**Step 2:** Add URL pattern `/api/health/`

**Step 3:** Commit

---

## Phase 6: Missing Features (Weeks 7-8)

> Features present in the web version but missing from the app, or present in the API but missing from both UIs.

### Task 6.1: Add Report Content UI (Web + App)
**Problem:** Report model and API endpoint exist but no "Report" button in any UI.

**Web:**
- Add "Report" option to the three-dot menu on posts, replies, and user profiles
- Create report modal with reason selection (spam/abuse/inappropriate/misinformation/other)
- POST to `/api/reports/`

**App:**
- Add report bottom sheet on post/reply overflow menu
- Call `apiService.createReport()`

---

### Task 6.2: Add Edit Post/Reply UI (Web + App)
**Problem:** API supports PATCH for posts and replies. Web has edit functionality. App has none.

**App:**
- Add "Edit" option to post/reply overflow menu
- Create edit screen with pre-filled content
- Call `apiService.editPost()` / `apiService.editReply()`

---

### Task 6.3: Add Resource Comments UI (Web)
**Problem:** API has resource comment/like endpoints. Web `resource_detail.html` may have partial support.

**Web:**
- Add comment section to resource detail page
- Implement comment creation, reply, like toggle
- Add resource like toggle button

---

### Task 6.4: Add Follower/Following Lists (App)
**Problem:** API supports follower/following lists. App has empty callback.

**App:**
- Create FollowersScreen / FollowingScreen
- Add navigation routes
- Call `apiService.getFollowers()` / `apiService.getFollowing()`

---

### Task 6.5: Add User Profile Photo Upload (App)
**Problem:** API has photo upload/activate endpoints. App has no UI.

**App:**
- Add "Change Photo" button in EditProfileScreen
- UseActivityResult for gallery/camera picker
- Upload via multipart form data
- Call `apiService.activatePhoto()`

---

## Phase 7: Testing & Quality (Ongoing)

### Task 7.1: Add backend unit tests
**Files:**
- Create: `backend_python/api/tests/` directory
- Create: `backend_python/api/tests/test_auth.py`
- Create: `backend_python/api/tests/test_posts.py`
- Create: `backend_python/api/tests/test_counters.py`
- Create: `backend_python/api/tests/test_bookmarks.py`

**Priority tests:**
1. Auth flow (signup, verify, login, password reset)
2. Post CRUD (create, like, edit, delete, archive)
3. Counter increment/decrement atomicity
4. Bookmark toggle race condition
5. Verification code purpose enforcement

---

### Task 7.2: Add Android UI tests
**Files:**
- Create: `app/src/androidTest/java/com/neb/ians/`

**Priority tests:**
1. Login flow (Google + Email)
2. Home screen loads resources and posts
3. Forum post detail navigation
4. Settings screen logout

---

### Task 7.3: Set up CI test pipeline
**Files:**
- Modify: `.github/workflows/build-release.yml`

**Add:**
- Backend test step: `python manage.py test`
- Android test step: `./gradlew testModernDebugUnitTest`
- Lint step: `./gradlew lintModernDebug`

---

## Priority Matrix

| Phase | Tasks | Est. Time | Impact |
|-------|-------|-----------|--------|
| Phase 1 | 7 tasks | 1 week | Critical security + data integrity |
| Phase 2 | 6 tasks | 2 weeks | Admin panel professional quality |
| Phase 3 | 6 tasks | 2 weeks | Website UX polish + performance |
| Phase 4 | 10 tasks | 3 weeks | Android app critical fixes + features |
| Phase 5 | 5 tasks | 1 week | Backend performance + API quality |
| Phase 6 | 5 tasks | 2 weeks | Missing features parity |
| Phase 7 | 3 tasks | Ongoing | Testing + CI |

**Total: 42 tasks across 7 phases, ~12 weeks estimated**

---

## Key Decisions Made

1. **Admin panel stays in Django templates** — No React/Vue rewrite. Extract inline styles to CSS classes, add pagination, fix accessibility. Incremental improvement over big-bang rewrite.

2. **Android app uses existing architecture** — No MVVM refactor. Fix critical bugs first (runBlocking, logging, sequential API calls), then add missing features.

3. **Backend code duplication resolved by making services.py the single source of truth** — views.py calls services.py, web/views.py already calls services.py.

4. **Denormalized counters are kept** — They're the right approach. The bug is that `_build_stats_batch` ignores them. Fix the bug, don't remove the optimization.

5. **API versioning deferred** — Adding `/api/v1/` prefix is a breaking change for the Android app. Defer until we have a proper migration plan.

6. **Offline support deferred** — Room caching for resources/posts is a Phase 8+ effort. Current priority is fixing what's broken before adding new architecture.

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Auth token fix may invalidate existing sessions | Medium | Deploy during low-traffic; existing tokens still work, just not regenerated |
| Admin CSS extraction may break existing styles | Low | Deploy to staging first; visual diff testing |
| `select_for_update` may increase DB lock contention | Low | Only used on toggle endpoints with low write volume |
| Android `ApiResult` refactor touches all ViewModels | High | Phase 4, do incrementally per ViewModel |
| `_link_oauth_user_model` fix changes account merge behavior | High | Test thoroughly with Google and GitHub flows; add rollback migration |