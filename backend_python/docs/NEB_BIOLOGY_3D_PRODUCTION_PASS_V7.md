# NEBians Biology 3D production pass v7

## Target

Raise the Biology Library → Interactive 3D/simulation experience from decorative demos to structured, scientifically grounded, production-ready learning tools.

## Coverage

| Area | Count | Status |
| --- | ---: | --- |
| Beginner Biology 3D lessons | 4 | Updated |
| NEB Class 11 Biology lab3D practicals | 18 | Updated through shared runtime/model layer |
| NEB Class 12 Biology lab3D practicals | 25 | Updated through shared runtime/model layer |
| Total Biology interactive 3D/lab3D lessons | 47 | Covered |

## Core implementation decisions

1. **One source of scientific truth.** The new `bio3d-science.js` module computes metric rows, formula text, result badges and conclusion text. This prevents the 3D labels, HUD and observation table from drifting apart.
2. **Procedural model quality without large assets.** The lab scenes remain generated from optimized Three.js primitives so they load quickly and stay deployable on the current static pipeline.
3. **Real readings over placeholder labels.** Practical readings now include formulas such as mitotic index, CFU estimate, quadrat density/frequency, soil moisture, stomatal density, respiration index, osmosis rise, enzyme optimum response, chi-square comparison and glucose range classification.
4. **Canvas-level scientific context.** Each NEB lab3D model now includes a 3D readings plaque and relevant calibration reference where useful.
5. **Beginner lessons get actual physiology/ecology mechanics.** The four beginner lessons now expose scientific variables rather than static sliders and decorative animations.

## Files changed or added

See `docs/CHANGED_FILES_BIOLOGY_V7.txt` and root `CHANGES_ONLY_MANIFEST.md`.

## Validation

- JavaScript syntax check: all interactive JS files passed `node --check`.
- Python compile check: Biology catalog/runtime/view files passed `python -m py_compile`.
- Catalog coverage: 4 beginner Biology 3D lessons and 43 NEB Biology lab3D lessons verified.
- Lab3D data coverage: all 43 practical slugs matched in `bio3d-data.js`.
- Procedural scene smoke test: all 43 NEB lab3D models built successfully.

## Remaining limitation

The upgraded models are high-quality procedural Three.js models, not photogrammetry scans or externally authored medical GLB assets. That choice keeps the package lightweight and deployable, but it means “pixel-perfect realism” is approximated through anatomy-aware procedural geometry, labels and formula-accurate readings rather than scanned meshes.
