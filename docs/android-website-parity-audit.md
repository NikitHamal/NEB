# Android Website Parity Audit

Date: 2026-06-04

## Scope

This pass updated the Android app toward the current NEBians web experience and fixed API contract gaps found while comparing Android Retrofit models with the Django API.

## Website Design Tokens Applied

- Primary blue: `#004AC6`
- Light app surface: `#F8F9FF`
- Dark app surface: `#0B1C30`
- Surface containers and outline colors now follow `backend_python/web/static/web/css/material3.css`
- Cards use 8dp corners to match the web resource/post cards
- Subject resource art colors now mirror the web `.subject-*` CSS classes
- Poppins remains the app font, with zero letter spacing for more stable mobile layout

## Android UI Changes

- Added `NebiansWebComponents.kt` with shared web-matched components:
  - `WebResourceCard`
  - `WebPostCard`
  - `NebiansAvatar`
  - `StatBlock`
- Home now uses shared resource/post cards and opens forum posts from the activity section.
- Library now uses the shared resource cards.
- Forum now uses shared post cards and a primary filled "New Post" action.
- Forum search now calls the backend `search` query parameter instead of only changing local state.
- Search now renders both resources and forum posts, with navigation to post detail.
- Profile was rebuilt with banner/avatar, role/private chips, stats, bio, academic details, and edit/follow actions.
- Login was moved from a custom gray gradient style to the same Material 3 surface, border, and pill-button system as the web.
- Post detail now uses bordered 8dp content/reply cards and shared avatars.

## Android API Fixes

- Like responses now decode both `thumbsUpCount`/`isThumbedUp` and `thumbs_up_count`/`is_thumbed_up`.
- Resource like responses now decode both `likeCount`/`isLiked` and `like_count`/`is_liked`.
- Bookmark responses now decode both `isBookmarked` and `is_bookmarked`.
- Resource comments now decode both web-service camelCase and older snake_case fields.
- Bookmark listing now expects the backend paginated shape.
- Locked/restricted profiles no longer crash Android if the backend omits `id`.
- Home loads resources independently from forum posts so a protected or failing post endpoint does not blank the resource feed.

## Backend API Changes

- `GET /api/posts/` and `GET /api/posts/<id>/replies/` are explicitly public while writes still require auth.
- `POST /api/posts/<id>/replies/` accepts both `parentReplyId` and `parent_reply_id`.
- `GET|POST /api/bookmarks/check/` accepts query params or a JSON body.
- `GET /api/resources/` now honors `sort=newest`, `sort=relevant`, `sort=popular`, `sort=likes`, `sort=viewed`, `sort=views`, and `sort=oldest`.
- Added Android-ready resource social endpoints:
  - `POST /api/resources/<resource_id>/like/`
  - `GET|POST /api/resources/<resource_id>/comments/`
  - `DELETE /api/resources/<resource_id>/comments/<comment_id>/`
- `GET /api/users/profile/<username>/` now includes profile stats and relationship flags for unlocked profiles.

## Verification

- `python3 -m py_compile backend_python/api/views.py backend_python/api/urls.py` passed.
- `git diff --check` passed.
- Android Gradle compile could not run in this container because no JDK is installed and `JAVA_HOME` is not set.
- Django `manage.py check` could not run because Django is not installed in this container.

## Follow-Up Needed

- Run `./gradlew :app:compileModernDebugKotlin` and `./gradlew assembleModernDebug` in an environment with JDK 17.
- Run backend checks in the project virtualenv: `python manage.py check`.
- Deploy backend changes with `backend_python/scratch/deploy.ps1` from the documented Windows path.
- After deployment, verify live unauthenticated:
  - `GET /api/posts/`
  - `GET /api/search/?q=physics`
  - `GET /api/resources/?sort=popular`
- Add Android UI screenshot tests once a device/emulator build environment is available.
