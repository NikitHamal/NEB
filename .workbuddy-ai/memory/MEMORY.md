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
