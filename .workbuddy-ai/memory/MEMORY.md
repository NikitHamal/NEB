# NEBians - Project Memory

## Interactive 3D simulations

**Architecture:** the interactive 3D sims are server-side three.js r160 modules under
`backend_python/web/static/web/js/interactive/`, served into a remote WebView at
`https://nebians.consica.com.np/interactive/{course}/{lesson}/`. The Android app needs **no
changes** to pick up edits.

**Deploy pipeline:** edit under `web/static/` -> `backend_python/.venv/Scripts/python.exe
manage.py collectstatic --noinput` -> served from `backend_python/staticfiles/`
(`staticfiles/` is gitignored). Bare `python manage.py` fails; Django is only in `.venv`.

**Catalog = source of truth for what ships:** `backend_python/web/interactive/catalog_*.py`.
Any module not listed there is dead code. The bare `three` / `three/addons/` specifiers come
from an importmap in `web/templates/web/interactive/lesson.html`.

**Verification harness:** `backend_python/scratch/sim3d_verify/` (gitignored).
`bash sync.sh [base]` mirrors the live tree (or git HEAD) into `./mod` for headless Node
measurement; `check.sh` syntax-checks all modules; `run.mjs` / `run-ai.mjs` / `run-bio.mjs`
measure draw calls, triangles, build time and leaks; `test-pick.mjs` / `test-glb.mjs` cover
the merge and pick-map logic.

## Draw-call batching rules (`core/bio3d-batch.js`)

- Batch **within** one anatomical/stage group, never across groups - groups have independent
  visibility and transforms, and a merged buffer spanning two can do neither.
- Tag per-frame-animated meshes `userData.noBatch` before batching.
- Merge **after** every enhancement pass (scan-grade displacement, scatter) has run.
- `mergeWithPickMap` + `pickSource(mesh, faceIndex)` keeps tap-to-identify working on merged
  buffers; essential for the 826-mesh `human-body` GLB.
- Geometry is grouped by material signature **plus** a flat/curved class, because the
  scan-grade displacement pass deliberately never displaces flat panels.
- See the 2026-08-30 daily log for measured before/after numbers.

## Web templates & CSS traps

**`_ctx()` passes `user` as a plain dict, not a Django `User`.** In templates use the
top-level `is_authenticated` context var (which `_ctx()` sets to `bool(token)`), never
`user.is_authenticated` — the latter is a failed dict-key lookup that silently evaluates
falsy, so the page renders its signed-out branch even when the user is signed in. That var
is what `base.html` and `_comment_cards.html` use. Only `news_detail.html` had the bug
(fixed 2026-09-14).

**Shared partials do not carry their CSS.** `web/_comment_cards.html` emits `.fp-reply*`
markup, but those rules live only in `pages/forum-post.css`, which only `forum_post.html`
loads. Any other page including that partial must supply its own `.fp-reply*` styling, or
the comment cards render completely unstyled.

**`inline-media.js` auto-enhances every `<textarea>` on the page.** It swaps the textarea
for a `contenteditable` div, sets the original to `display:none`, and proxies `.value`.
A bespoke textarea silently vanishes. Opt-outs: `[data-neb-skip]`, `.reply-input-wrapper`,
`.fp-compose`. For a new comment box, use `.reply-input-wrapper` + `.reply-send-btn` — the
site-wide composer pill.

**`color-mix()` in the existing CSS omits `in srgb`** (e.g.
`color-mix(10%, var(--md-primary), transparent)`), which is invalid and silently dropped by
the browser. Write `color-mix(in srgb, COLOR N%, transparent)` in new code.

**Page CSS layout:** `.md-container` owns the horizontal gutter, so page-level classes must
use `padding-block`, not `padding: Xpx 0 Ypx` — the zero overrides the gutter and the card
touches the screen edge on mobile. `staticfiles/` is served by WhiteNoise with
`CompressedStaticFilesStorage` (unhashed filenames + `.gz`/`.br`), not the Manifest storage
that AGENTS.md claims.

## Headless visual verification (Chrome, Windows)

`backend_python/scratch/news_preview/` (gitignored): renders a template against real DB rows
into static HTML, `serve.py` maps `/static/` -> `staticfiles/`, Chrome
`--headless=new --screenshot` captures it. Two gotchas:

- Chrome headless on Windows enforces a **~500px minimum window width**, so
  `--window-size=390` actually renders a ~489px viewport and clips the screenshot. Wrap the
  page in a 390px-wide `<iframe>` to get a true mobile viewport.
- `--dump-dom` excludes iframe content — have the child write into `parent.document.body`
  (same-origin) to read measurements back.

