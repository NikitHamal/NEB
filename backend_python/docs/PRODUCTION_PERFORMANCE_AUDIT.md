# NEBians Production Performance Audit & Free Next Steps

This audit is based on the uploaded Django project structure and source files.

## Highest-impact changes already included

1. **NEB simulations are now shared-runtime 3D instead of duplicated 2D logic.**
   - One shared 3D engine powers all Class 11/12 practicals.
   - Individual lesson JS files are now tiny wrappers.
   - This reduces long-term maintenance and keeps future improvements centralized.

2. **Renderer quality adapts to real devices.**
   - Save-data users, reduced-motion users and lower-power/mobile devices get a lighter render tier.
   - Pixel ratio is capped to avoid massive mobile GPU cost.

3. **Database hot-path indexes added.**
   - Added migration `0066_performance_indexes_hot_paths.py` for forum ranking, replies, resource comments, resource requests, study spaces and study documents.
   - These match common query shapes seen in the code: profile timelines, ranked replies, public spaces, document status lists and admin request queues.

## Main performance risks found

### 1. Runtime files are present in the project ZIP

The uploaded ZIP contains runtime artifacts such as:

- `db.sqlite3`
- `logs/nebians.log`
- `__pycache__` / `.pyc`
- `.env`
- `firebase-service-account.json`

These should not be deployed inside source bundles or public repos. They increase ZIP size and can expose secrets or private data.

**Free fix:** keep only `.env.example` in source. Store real secrets in your host control panel or environment variables.

### 2. Some templates are very large

Largest templates observed include:

- `web/templates/web/result_checker.html`
- `web/templates/web/forum_post.html`
- `web/templates/web/profile.html`
- `web/templates/web/subject_page.html`
- `web/templates/web/create_post.html`

Large templates often include inline JavaScript and page-specific CSS. This slows first response, makes browser parsing heavier and makes caching less effective.

**Free fix:** move page JS into `web/static/web/js/pages/...` and page CSS into `web/static/web/css/pages/...`, then serve through WhiteNoise compressed manifest static files.

### 3. Some Python view files are very large

Largest view modules include:

- `web/views_study_lab.py`
- `web/views_arena.py`
- `web/views_admin.py`
- `web/views_public.py`
- `web/views_profile.py`

Large modules are harder to optimize and test. They often accumulate duplicated query patterns.

**Free fix:** split into services/selectors/actions:

```text
web/selectors/resources.py
web/selectors/forum.py
web/actions/study_lab.py
web/actions/profile.py
```

Keep views thin: parse request, call selector/action, render/return JSON.

### 4. Search and filtering need query-plan verification

The code already has several indexes, and this pass adds more. However, production query plans depend on the real database size and MySQL/MariaDB version.

**Free fix:** run `EXPLAIN` on these routes' querysets in production/staging:

- Library/resource search
- Forum home sorted by latest/trending
- Forum post detail replies sorted by top/latest
- Profile activity tabs
- Notifications list
- Study Lab document list and parse-status polling
- Resource request list

### 5. Static assets should be aggressively cached

The project already uses WhiteNoise `CompressedManifestStaticFilesStorage`, which is good.

**Free fix:** after every deploy run:

```bash
python manage.py collectstatic --noinput
```

Then verify that static files are served with long cache headers and compressed variants (`.br`/`.gz`) where available.

### 6. Interactive pages should not block the main app

3D simulations are fun but can be heavy on weak phones.

**Already included:** quality tiers, capped pixel ratio, no external 3D model downloads, visibility-aware animation.

**Free next step:** add a `?lite=1` or user setting to force 2D/static fallback for very weak devices.

### 7. Polling endpoints may become expensive

Study Lab and Study Space JS contains repeated `fetch(...parse-status...)` style calls. These can become expensive with many users.

**Free fixes:**

- Increase polling interval with exponential backoff.
- Stop polling when tab is hidden using `document.visibilityState`.
- Cache unchanged JSON responses for a few seconds.
- Consider WebSocket push for parse completion later, since Channels is already present.

## Free optimization checklist

### Database

- Apply migration `0066_performance_indexes_hot_paths.py`.
- Run `python manage.py dbshell` and verify slow queries with `EXPLAIN`.
- Set MySQL slow query log temporarily during peak use.
- Use `select_related()` for every FK shown in templates.
- Use `prefetch_related()` for reverse relations shown in loops.
- Avoid `count()` inside loops; use denormalized counters already present in models.
- Keep pagination hard limits; avoid unbounded `.all()` in user-facing views.

### Django / server

- Keep `DEBUG=False`.
- Use Redis cache by setting:

```text
CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
CACHE_LOCATION=redis://127.0.0.1:6379/0
SESSION_ENGINE=django.contrib.sessions.backends.cached_db
```

- Use Gunicorn/Daphne process counts based on RAM, not guesswork.
- Enable HTTP/2 and Brotli/Gzip at the reverse proxy if available.
- Keep logs rotated; do not ship `logs/` in deploy artifacts.

### Static/frontend

- Run `collectstatic` on deploy.
- Move inline JS out of large templates.
- Defer non-critical scripts.
- Use `loading="lazy"` for images below the fold.
- Add explicit width/height to images to reduce layout shift.
- Keep Three.js local and cached. Do not add CDN dependencies.
- Consider splitting page-specific JS modules for heavy pages.

### APIs

- Add response caching to anonymous GET endpoints that render stable lists.
- Add ETags or short cache timeouts for unchanged JSON.
- Rate-limit expensive AI/generation endpoints separately from normal reads.
- Add per-endpoint timing logs in middleware for requests over 500 ms.

### Observability without paid tools

- Browser: Lighthouse, Chrome Performance panel, Coverage tab.
- Server: Django Debug Toolbar locally only, `EXPLAIN`, MySQL slow query log.
- Static: `python manage.py collectstatic --noinput -v 2` to inspect output.
- Network: Chrome DevTools Network tab; test Slow 4G and low-end mobile throttling.

## Production release checklist

1. Pull this ZIP into a branch.
2. Install requirements in a clean virtualenv.
3. Run:

```bash
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

4. Smoke-test all 30 NEB practicals.
5. Run Lighthouse on:
   - homepage
   - library interactive tab
   - one 3D physics practical
   - one 3D chemistry practical
   - forum home
   - study lab
6. Enable slow query logging for one real traffic window.
7. Fix top 5 slow queries first, not random micro-optimizations.
