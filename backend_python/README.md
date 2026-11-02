# NEBians backend (`backend_python/`)

Django 5 + Django REST Framework service behind the NEBians website, the Android app and the **native desktop app** (`../desktop`). It serves the study library (syllabus, chapters, books, search), accounts, community, notifications and profile pictures.

## What the desktop app needs from it

| Purpose | Endpoint | Auth | Notes |
|---|---|---|---|
| Content manifest + app update hints | `GET /api/content/manifest/` | public | `version` changes whenever content changes (desktop re-syncs); `desktop.{latest,minimum,downloadUrl}` come from env |
| Catalogue index | `GET /api/content/index/` | public | tracks → subjects |
| Syllabus of a subject | `GET /api/content/syllabus/<key>/` | public | e.g. `11-physics` |
| Study chapter / subject index | `GET /api/content/study/<key>/<name>/` | public | `name` = `index` or a chapter id |
| Full-text search | `GET /api/content/search/?q=…` | public | throttled `90/minute` per IP |
| Study-book PDFs | `GET /api/content/books/` · `GET /api/content/books/<slug>/file/` | public | supports `Range` → resumable offline downloads |
| Static assets (figures, avatars) | `GET /static/web/…`, `/avatar/<id>/`, `/media/…` | public | clients cache by URL |
| Sign-in (Google / GitHub) | `POST /api/auth/desktop/start/` → browser consent page → `POST /api/auth/desktop/poll/` | PKCE | token is the same bearer token Android uses |
| Email sign-in/up/verify/reset | `/api/auth/email/*` | – | same as Android |
| Profile | `GET/PUT /api/users/me/…`, `GET /api/users/<username>/` | bearer | `photo_url` is a URL the client downloads |
| Avatar style | `GET /api/users/me/avatar/`, `POST …/customize/` | bearer | |
| Community, notifications, bookmarks | `/api/posts/…`, `/api/notifications/…`, `/api/bookmarks/toggle/` | bearer for writes | |

Content endpoints are read-only, unauthenticated, throttled (`DRF_CONTENT_*`), send `ETag`/`Last-Modified`/`Cache-Control` and never touch paths outside the content directories (`api/content_api.py::_safe_child`). Nothing in a response is a server filesystem path.

## Quick start (local, SQLite)

```bash
cd backend_python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then set DEBUG=True for local work
export DB_ENGINE=sqlite DEBUG=True
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
curl http://127.0.0.1:8000/api/content/manifest/
```

Point the desktop app at it: `NEB_API_BASE=http://127.0.0.1:8000/ ./nebians` (Windows: `set NEB_API_BASE=http://127.0.0.1:8000/`).

## Environment variables

Copy `.env.example` → `.env` (loaded automatically; **never commit it**).

| Variable | Required | Meaning |
|---|---|---|
| `DEBUG` | – | `False` in production (default). With `False` the three secrets below are mandatory |
| `SECRET_KEY` | prod | Django secret |
| `ADMIN_API_SALT` | prod | salt for admin API tokens |
| `CONSICA_BRIDGE_KEY` | prod | shared key for the sibling bridge service |
| `ALLOWED_HOSTS`, `ALLOWED_HOSTS_GLOB` | prod | comma-separated hosts; glob entries starting with `.` match suffixes |
| `CSRF_TRUSTED_ORIGINS`, `CORS_ALLOWED_ORIGINS` | prod | `https://…` origins |
| `DB_ENGINE` | – | `sqlite` (file `db.sqlite3`) or anything else = MySQL/MariaDB |
| `DB_NAME` `DB_USER` `DB_PASSWORD` `DB_HOST` `DB_PORT` | MySQL | defaults `nebians_db`/`nebians_user`/``/`localhost`/`3306` |
| `GOOGLE_CLIENT_ID/SECRET`, `GITHUB_CLIENT_ID/SECRET` | for social login | desktop hand-off reuses the website login |
| `EMAIL_HOST/PORT/HOST_USER/HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | for email codes | SMTP |
| `DESKTOP_LATEST_VERSION`, `DESKTOP_MIN_VERSION`, `DESKTOP_DOWNLOAD_URL`, `DESKTOP_RELEASE_NOTES` | – | surfaced in `/api/content/manifest/` |
| `DRF_CONTENT_THROTTLE`, `DRF_CONTENT_SEARCH_THROTTLE`, `DRF_CONTENT_BOOK_THROTTLE` | – | default `1200/hour`, `90/minute`, `120/hour` |
| `REDIS_URL`, `CACHE_BACKEND` | – | shared cache for throttling across workers (default: local memory) |
| `MEILISEARCH_URL`, `MEILISEARCH_API_KEY` | – | optional site-search index (content search works without it) |
| `PROFILE_PHOTO_MAX_BYTES` | – | avatar upload cap, default 5 MB |

Content lives in the repo: `web/data/{syllabus,study}` (JSON) and `web/static/web/study` (figures); books are PDFs found by `content_api.list_books()`. Ship the whole `backend_python/` directory (or the repo) so these exist next to the code.

## Tests

```bash
cd backend_python
DB_ENGINE=sqlite DEBUG=True python manage.py test api.test_content_api api.test_desktop_auth api.test_avatar_profile
```

## Docker

```bash
cd backend_python
cp .env.example .env            # set SECRET_KEY, ADMIN_API_SALT, CONSICA_BRIDGE_KEY, ALLOWED_HOSTS
docker compose up --build -d    # backend on :8000 + MariaDB
docker compose logs -f backend
```
Single container with SQLite: `docker build -t nebians-backend . && docker run -p 8000:8000 --env-file .env -e DB_ENGINE=sqlite nebians-backend`.
The image runs `migrate` then `daphne` (ASGI, WebSockets for community). Health check: `GET /api/content/manifest/`.

## Deploy me

1. Provision a Linux VM (1 GB RAM is enough) with Docker, and a DNS name, e.g. `api.example.com`.
2. `git clone https://github.com/NikitHamal/NEB.git && cd NEB/backend_python && cp .env.example .env`; fill in the secrets, `ALLOWED_HOSTS=api.example.com`, `CSRF_TRUSTED_ORIGINS=https://api.example.com`.
3. `docker compose up --build -d`.
4. Put a TLS reverse proxy in front (Caddy: `api.example.com { reverse_proxy localhost:8000 }`; nginx must pass `Upgrade`/`Connection` headers for WebSockets).
5. `docker compose exec backend python manage.py createsuperuser` (optional, for `/admin/`).
6. Verify: `curl https://api.example.com/api/content/manifest/` returns JSON with `chapters > 0`.
7. Desktop builds point at production by default; for a self-hosted API set `NEB_API_BASE=https://api.example.com/`.
8. Updating: `git pull && docker compose up --build -d` (migrations run on boot). To publish new notes just pull — the manifest `version` changes and desktop clients re-sync.

Without Docker: `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py collectstatic`, run `daphne -b 127.0.0.1 -p 8000 nebians.asgi:application` under systemd, or use `passenger_wsgi.py` on cPanel.

## Security notes
- Rotate any token that has ever been pasted into chat or CI logs.
- Keep `DEBUG=False`; the settings module refuses to start without real secrets in that mode.
- Content API is public by design (it is the same material as the public website); account data is bearer-token only.
