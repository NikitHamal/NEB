# NEB 3D Simulation Enhancement Pass

This pass upgrades the shared NEB 3D lab runtime from a visual 3D replacement into a more student-ready practical simulator.

## What was enhanced

- Added guided practical workflow steps for every lab category: setup, measurement, observation and calculation.
- Added an in-panel student observation book with live trial rows, concordant readings and calculated outcomes.
- Added Record Reading, Next Step and Clear Records controls so students can actually perform a virtual practical instead of only watching a model.
- Added high-resolution canvas-based scale textures for rulers/vernier scales, with minor and major divisions.
- Rebuilt the vernier calipers scene to be cleaner and more realistic: fixed jaw, sliding vernier, scale texture, specimen alignment and smaller labels.
- Improved lab environment lighting, bench details, safety/measurement notice board and less intrusive 3D labels.
- Improved chemistry glassware: lips, meniscus-like surfaces, graduation marks, transparent material and stronger liquid read clarity.
- Improved titration apparatus: 50 mL burette scale, clamp, tap, white tile, conical flask, visible drops, endpoint guidance and required titre display.
- Improved electrical meters with analog gauge faces and calibrated needles.
- Improved meter bridge/potentiometer visuals with better wire board, null/contact points and clearer read labels.
- Added CSS for the observation table, responsive panel behaviour, sharper HUD badges and better mobile ergonomics.

## Simulation behaviour

The app still uses the existing optimized Three.js module and no external paid 3D assets. Readouts remain formula-driven. Observation rows are derived from the current practical variables and include realistic repeated trials or live reading rows depending on the experiment.

## Files changed in this enhancement pass

- `web/static/web/js/interactive/core/real-lab-3d.js`
- `web/static/web/css/pages/interactive/12-production-lab3d.css`
- `docs/NEB_3D_SIMULATION_ENHANCEMENT_PASS.md`

## Validation

- `node --check` passed for all interactive JavaScript files.
- Python migration syntax check passed with `py_compile`.
- Full Django runtime validation still needs to be run in the target environment after installing project requirements.
