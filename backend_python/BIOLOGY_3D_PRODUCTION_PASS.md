# Biology 3D production pass — v7

This package contains a focused production pass for the Biology models and simulations exposed through Library → Interactive.

## Scope covered

- Beginner Biology course: 4 real-time 3D lessons.
  - Human Body Explorer
  - Plant Power: Photosynthesis
  - Butterfly Life Cycle
  - Heart & Lungs
- NEB Biology practical courses: all 43 lab3D practical lessons across Class 11 and Class 12.

## What changed

### Shared scientific runtime for the 43 NEB practicals

- Added `web/static/web/js/interactive/core/bio3d-science.js` as the single calculation source for live readings, formula text, HUD badges and recorded conclusions.
- Reworked `bio3d-runtime.js` so the control panel, observation book, trial randomizer, help text and recorded observations use the same scientific model output.
- Extended `bio3d-models.js` with an in-scene verified-readings plaque and calibration references so the 3D canvas itself shows measured values and the formula context.
- Kept the models procedural and lightweight: no external GLB/texture dependency, no new licensing exposure, and no bundle-heavy asset pipeline.

### Beginner 3D Biology upgrades

- `human-body.js`: added major arterial/venous routes, spinal/limb nerve overlays, activity-linked heart rate, breathing rate, cardiac output and minute ventilation readings, plus live organ pulsation.
- `photosynthesis.js`: replaced the old toy linear minimum with a limiting-factor model using light saturation, water/stomatal stress, CO2 response and enzyme temperature; added visible stomata, temperature control, formula readout and stoichiometric glucose/O2 counters.
- `butterfly-life-cycle.js`: added stage durations, biological timeline, active 3D timeline bar, adult proboscis and six legs, plus stage-specific process readouts.
- `heart-lungs.js`: added diaphragm anatomy and motion, stroke volume, cardiac output, tidal volume and minute ventilation calculations.
- `08-biology.css`: added responsive production styling for the four beginner 3D Biology scenes.

### UI/readability polish

- Updated `12-production-lab3d.css` for the denser scientific readouts and observation tables.
- Kept mobile control panels collapsible and constrained so the 3D canvas remains usable on phones.

## Validation performed

- `node --check` passed for every JavaScript file under `web/static/web/js/interactive`.
- `python -m py_compile` passed for the Biology catalog/runtime/view Python files that can be compiled without installing Django.
- Catalog coverage check confirmed 47 Biology interactive lessons total: 4 beginner `3d` lessons and 43 `lab3d` NEB practical lessons.
- Lab3D key coverage check confirmed all 43 NEB practical lesson slugs have matching entries in `bio3d-data.js`.
- A Node smoke test built all 43 procedural NEB Biology lab3D scenes with the new science layer and model plaque enabled: `BIO3D_SMOKE_OK 43`.

## Environment note

- `python manage.py check` could not be executed in this container because Django is not installed here. The source-level Python compile checks above did run successfully.
