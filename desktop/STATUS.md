# Desktop status — session 3 (audit first, then finish)

## 1. What was actually on the remote when this session started
The task brief assumed the crashed session's work was lost. **It was not.** `origin/main` at `d61169a` already contained:

| Item | State on remote |
|---|---|
| `backend_python/api/content_api.py` (+ `views_content.py`, `content_search.py`, routes `api/content/*`) | present — manifest, syllabus, chapters, search, books with HTTP Range, safe path resolution, throttling, ETag |
| `backend_python/api/test_content_api.py` | present (8 tests) |
| `desktop/src/data/content.rs` | present — server fetch + disk cache + offline downloads |
| `desktop/src/ui/remote_image.rs` | present — but only wired into People / User / Notifications |
| `desktop/src/ui/menu.rs` (local-folder menu) | removed |
| Content-folder picker / `--content` | removed from UI + CLI (`store.content_dir` is a dead, ignored field kept for state-file compatibility) |
| Screens: books, downloads, people, user profile, notifications | present |
| Android parity gaps | History, Help/shortcuts, Legal (privacy/terms) not in app |
| `.github/workflows/desktop-windows.yml` | **still bundled `content/` and uploaded a folder artifact** |
| `backend_python/README.md` | **missing** |
| Screenshots | 31 from the *previous* build (old menu bar + "Choose content folder" — the images shared in the brief are from the v0.2.0 .exe) |

## 2. What was missing (and is done this session — see CHANGELOG)
- Avatars not shown in sidebar, profile, community feed/replies → fixed.
- CI workflow → now builds/attaches only the `.exe` + `.sha256`.
- Backend README (env vars, DB, seed, run, Docker, deploy).
- Missing screens, UI/UX polish, multi-size screenshots, offline + keyboard passes.

## 3. Plan
1. Audit + push (done). 2. Avatars + CI. 3. Backend README + tests. 4. New screens. 5. UI polish passes with real screenshots. 6. Fresh-clone verification, docs, report.
