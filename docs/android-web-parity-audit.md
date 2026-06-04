# Android/Web Parity Audit

## Scope

This pass focused on production-impact parity between the live NEBians website and the Android Compose app:

- Material color tokens now mirror `backend_python/web/static/web/css/material3.css`.
- Home, Library, Forum, and Forum detail now use shared website-matched Compose components for resource cards, post cards, avatars, category pills, and action stats.
- Android API models were made tolerant of the backend's mixed camelCase/snake_case response fields.
- Broken Android/backend contracts were corrected for profile updates, replies, bookmarks, likes, notifications, and resource sorting.

## API Fixes

- Android profile update requests now send the camelCase keys the backend reads: `photoUrl`, `displayName`, `classLevel`, `bannerUrl`, and `isLocked`.
- Android nested replies now send `parentReplyId`, matching the current backend dispatcher.
- Android reply lists now parse the backend's paginated `results` wrapper instead of expecting a raw array.
- Android like/bookmark responses now accept both legacy snake_case and current camelCase fields.
- Android notification lists now parse paginated `results`, and mark-read calls send `{ "mark_all": true }`.
- Backend API routes now mount:
  - `/api/notifications/`
  - `/api/notifications/mark-read/`
  - `/api/notifications/unread-count/`
- Backend `/api/resources/` now honors `sort=newest`, `sort=oldest`, `sort=popular`, and `sort=relevant`.
- Backend profile serialization now includes counters and follow state expected by Android profile screens.
- Android forum search now forwards the query to `/api/posts/?search=...`.

## UI Parity Notes

The new Android shared components intentionally mirror the website's current visual language:

- 8dp bordered cards with no heavy elevation.
- Resource art headers with subject-specific palette, type pill, and circular subject icon.
- Uppercase subject chips using website subject badge colors.
- Forum cards with avatar, compact author metadata, category pill, rich-text-stripped preview, and flat action chips.
- Avatar photos render when available via Coil; otherwise the initial fallback matches the website behavior.

## Verification

Completed:

- `python -m py_compile backend_python/api/views.py backend_python/api/urls.py backend_python/api/serializers.py`

Blocked in this sandbox:

- `./gradlew :app:compileModernDebugKotlin` could not run because Java/JDK is not installed.
- `python manage.py check` could not run because Django is not installed in the sandbox Python environment.

Before release, run these in the normal Android/backend development environment:

```bash
./gradlew :app:compileModernDebugKotlin :app:assembleModernDebug
cd backend_python
python manage.py check
python manage.py test api
```
