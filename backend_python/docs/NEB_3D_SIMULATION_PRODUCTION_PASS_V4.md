# NEB 3D Simulation Production Pass v4

This pass directly addresses the reported issues from mobile screenshots:

- right-side cutoff on small screens
- controls feeling too large and covering the apparatus
- low-contrast/invisible `3D virtual lab` chip
- micrometer/screw-gauge model looking unrealistic and badly framed
- precision instruments needing more real practical detail

## UI/UX fixes

1. **No mobile overflow**
   - Added strict `min-width: 0`, `max-width: 100%`, and `overflow-x: clip` containment for lab3d pages.
   - The 3D canvas and simulation shell now stay inside the phone viewport.
   - The control panel uses safe-area insets and left/right anchoring on mobile.

2. **Compact mobile control drawer**
   - The measurement panel collapses by default on small screens.
   - Buttons were shortened from `New trial / Reset view / Procedure` to `Trial / View / Steps` and from `Next step / Record reading / Clear records` to `Next / Record / Clear`.
   - On very small screens, secondary animation toggle and data-card clutter are hidden to protect the apparatus view.
   - Observation tables now have tighter cells and their own internal scroll.

3. **Readable chips**
   - The `3D virtual lab` chip now has a solid light-theme contrast pair and a separate dark-theme pair.
   - This fixes the pale-green-on-white visibility issue.

4. **Better camera framing**
   - New per-apparatus camera targets for caliper, micrometer and spherometer.
   - The micrometer no longer opens behind the bench edge or too far away.

## Model upgrades

Added a new dedicated precision-instrument module:

- `web/static/web/js/interactive/core/lab3d-precision.js`

It replaces the previous generic caliper/micrometer/spherometer builders with individually tuned builders:

### Vernier calipers
- Main scale texture with centimeter and millimeter divisions.
- Separate fixed jaw and moving vernier slider.
- Vernier scale plate with 0.01 cm least-count label.
- Contact line between jaws and specimen.
- True diameter label plus formula label: MSR + VSD × LC.

### Micrometer screw gauge
- Proper U-frame using a curved tube geometry instead of a simple broken ring.
- Anvil, spindle, sleeve, thimble, ratchet and lock screw.
- Ribbed thimble for realistic grip.
- Sleeve scale and circular-scale reading label.
- Contact line at the wire and computed observed reading.

### Spherometer
- Three legs on curved/plane glass plate.
- Central screw and dial head.
- Dial tick marks and needle.
- Sagitta label tied to the simulation reading.

## Scientific/runtime fixes

- Added missing `indicatorColorName` import in `real-lab-3d.js`; this prevents the pH indicator lab from failing when rendered.
- Kept all numerical formulas from the previous production pass active.
- `Reset view` remains available for all labs, now labelled `View` in the compact UI.

## Validation performed

```bash
node --check web/static/web/js/interactive/core/real-lab-3d.js
node --check web/static/web/js/interactive/core/lab3d-precision.js
node --check web/static/web/js/interactive/core/lab3d-science.js
node --check web/static/web/js/interactive/core/lab3d-data.js
node --check web/static/web/js/interactive/core/sim-ui.js
python3 -m py_compile web/views_interactive.py web/interactive/runtime.py api/migrations/0066_performance_indexes_hot_paths.py
unzip -t nebians_full_production_pass_v4.zip
unzip -t nebians_changes_only_production_pass_v4.zip
```

Full Django runtime validation still requires project dependencies to be installed locally.
