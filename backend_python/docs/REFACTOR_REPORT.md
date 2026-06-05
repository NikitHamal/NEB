# NEBians Refactor Report

## Scope completed

This refactor keeps the existing Django URL contracts intact while breaking the largest monolithic files into focused modules. The public import paths `web.views` and `api.views` remain compatibility export modules, so existing URL configs and external imports continue to work.

## Backend modularization

### `web` app

The previous `web/views.py` monolith was split into:

- `web/view_helpers.py` — shared serializers, request helpers, context helpers, admin checks, cache helpers, syllabus parsing helpers.
- `web/views_public.py` — public pages, library/search/resource pages, SEO endpoints, error handlers.
- `web/views_forum.py` — forum pages and discussion pages.
- `web/views_profile.py` — profile pages and profile activity endpoints.
- `web/views_auth.py` — login, OAuth, email/password auth pages.
- `web/views_ajax.py` — AJAX mutation/read endpoints.
- `web/views_notifications.py` — notification pages and AJAX notification endpoints.
- `web/views_admin.py` — custom admin dashboard/resource/post/user/bot/syllabus pages.
- `web/views_arena.py` — Neby Arena AJAX bridge endpoints.
- `web/views.py` — compatibility re-export layer.

### `api` app

The previous `api/views.py` monolith was split into:

- `api/view_helpers.py` — shared auth, pagination, validation, verification-code, and stats helpers.
- `api/views_auth.py` — OAuth, email auth, password, and logout endpoints.
- `api/views_users.py` — profile, follow, stats, and user-photo endpoints.
- `api/views_resources.py` — resources and resource-request endpoints.
- `api/views_forum.py` — posts, replies, edit history, and dispatchers.
- `api/views_misc.py` — bookmarks, search, FCM, reports, and notifications.
- `api/views.py` — compatibility re-export layer.

## Template/static cleanup

Large inline CSS blocks were extracted from templates into page-level static stylesheets under:

```text
web/static/web/css/pages/
```

This reduces template size, improves browser/cache behavior, and makes page styling easier to maintain without changing template logic. Inline JavaScript was intentionally left inside templates when it contained Django template variables or nonce-dependent runtime values.

## Runtime/dead artifact cleanup

Generated and runtime-only files were removed from the refactored package:

- Python bytecode and `__pycache__` directories.
- Runtime cache files.
- Local log files.
- Local SQLite database dump.
- Sample uploaded media.
- The local `.env` file.
- Unreferenced temporary icon files.

The repository keeps `.env.example`, migrations, static assets, source code, templates, and deployment-relevant files.

## Validation performed

- Python syntax validation was run with `python -m compileall`.
- URL references were statically checked against the new split view modules.
- Function extraction was mechanically verified against the original uploaded files; all original functions were preserved exactly, including decorators.

`python manage.py check` could not be completed in this sandbox because Django is not installed in the execution environment. Run it in your production-like virtual environment before deployment:

```bash
python -m pip install -r requirements.txt
python manage.py check --deploy
python manage.py collectstatic --noinput
```

## Deployment notes

Because CSS was moved to static files, run `collectstatic` before deploying the refactored code. The project already uses WhiteNoise manifest static storage, so missing `collectstatic` can cause static-file lookup errors in production.

Use your real production `.env` on the server. Do not commit or upload `.env`.
