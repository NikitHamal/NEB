# NEB 3D Simulation Production Pass V3

## Scope
This pass focuses on the issues visible in the latest screenshot: right control-panel overflow, poor mobile fit, oversized/awkward instrument framing, and large monolithic runtime files.

## What changed

### 1. Responsiveness and control-panel fit
- Rebuilt the `lab3d` responsive CSS layer so the 3D stage gets a taller, realistic workspace on desktop and mobile.
- Fixed the right-side control panel so it no longer creates horizontal page/panel overflow.
- Converted crowded button rows to responsive CSS grids.
- Added mobile-specific bottom-sheet behavior for the controls.
- Added horizontal scrolling only inside the observation table, not the whole control panel.
- Added `box-sizing`, min-width protection, wrapping, and readout overflow guards.

### 2. Instrument framing and camera UX
- Added per-apparatus camera presets.
- Added a `Reset view` control in every 3D practical so students can instantly return to a fitted apparatus view.
- Reduced auto-rotation speed to prevent the instrument from drifting away while students are reading measurements.
- Added an OrbitControls `setView()` method for accurate camera reset without recreating the renderer.

### 3. Vernier calipers model enhancement
- Rebuilt the vernier calipers scene with a better real-life layout:
  - fixed jaw and moving vernier jaw,
  - main scale beam,
  - dark vernier scale plate,
  - locking screw,
  - zero-check marker,
  - contact/reference measurement line,
  - specimen aligned exactly between jaws,
  - corrected reading label plus MSR/VSD formula label.
- The visual jaw gap now matches the true specimen size, while the reading logic still supports zero-error correction.

### 4. Student practical workflow preserved and improved
- Kept the guided step workflow, observation book, record-reading button, clear-records button, and formula-based readouts.
- Observation table rendering now uses an internal scroll container, so long values remain usable on small screens.

### 5. Modularization/refactor
- Split the former monolithic `real-lab-3d.js` runtime:
  - `core/lab3d-data.js` — presets, constants, subject/color data, formulas tied to practical definitions.
  - `core/lab3d-science.js` — procedures, scientific observations, indicators, titration status, and observation-book generation.
  - `core/real-lab-3d.js` — runtime orchestration and 3D model builders.
- Refactored the interactive lesson template:
  - extracted the simulation shell into `web/templates/web/interactive/_sim_shell.html`.
- Refactored interactive Django views:
  - added `web/interactive/runtime.py` for view-facing context builders.
  - removed wildcard imports from `web/views_interactive.py` and made imports explicit.

## Validation performed
- `node --check` passed for all files under `web/static/web/js/interactive`.
- `python3 -m py_compile` passed for the refactored Python files and the performance-index migration.
- Verified that all 30 NEB physics/chemistry practical modules route through the shared 3D lab runtime.
- ZIP integrity checks passed after rebuild.

## Could not validate in sandbox
- `python manage.py check` could not run because Django is not installed in this sandbox environment.

Run this locally after download:

```bash
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```
