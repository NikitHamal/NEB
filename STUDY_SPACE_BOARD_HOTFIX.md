# Study Space / Collaborative Board Hotfix

Patched on 2026-07-10.

## Issues fixed

1. Realtime board did not sync until refresh
   - Fixed StudySpace WebSocket permission checks in `backend_python/api/consumers_ws.py`.
   - Owners, members/admins/moderators, public spaces, and specifically shared users can now subscribe to `studyspace.<id>`.
   - Fixed `yjs-provider.js` to answer server heartbeat pings and buffer early/offline Yjs updates.

2. Add existing document returned 400: `Document is already in another space`
   - `ajax_space_add_document` now clones an existing StudyDocument into the target space instead of trying to move it or failing.
   - If the document is already in the same space, the endpoint returns success.

3. Board file picker upload returned 500 / file placement did nothing
   - `ajax_space_upload` now returns flat `fileUrl`, `file_url`, `fileName`, and `fileSize` fields needed by the board picker.
   - Upload storage and parse-start failures are handled safely with JSON responses.

4. Board drawing cursor offset
   - Fixed HiDPI / browser zoom coordinate mismatch in `collab-board.js` by drawing in CSS pixels with DPR-aware transforms.

5. Board text/sticky typing reliability
   - Text editor overlay now allows text selection/typing inside the non-selectable board container.
   - Text edits now update locally and sync while typing using a small debounce, instead of only on blur.

6. Add existing file modal UI/UX
   - Existing docs from other spaces now show “Copy” / “Will copy from another space”.
   - Docs already in the current space show “Added”.
   - Modal selection is scoped so board file-picker selections do not pollute StudyDocument selection state.
   - Cache versions bumped to `v=1.3`.

## Files changed

- `backend_python/api/consumers_ws.py`
- `backend_python/web/views_study_lab.py`
- `backend_python/web/static/web/js/yjs-provider.js`
- `backend_python/web/static/web/js/collab-board.js`
- `backend_python/web/static/web/js/study-space.js`
- `backend_python/web/static/web/css/pages/study-space.css`
- `backend_python/web/static/web/css/pages/collab-board.css`
- `backend_python/web/templates/web/study_space.html`

## Validation run

```bash
python -m py_compile backend_python/web/views_study_lab.py backend_python/api/consumers_ws.py
node --check backend_python/web/static/web/js/collab-board.js
node --check backend_python/web/static/web/js/study-space.js
node --check backend_python/web/static/web/js/yjs-provider.js
```

All checks passed.

## Deploy checklist

```bash
cd backend_python
python manage.py collectstatic --noinput
# restart ASGI/Daphne/Uvicorn/Passenger workers
```

For production realtime reliability, ensure Redis-backed Channels is enabled:

```env
CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
CACHE_LOCATION=redis://127.0.0.1:6379/0
```
