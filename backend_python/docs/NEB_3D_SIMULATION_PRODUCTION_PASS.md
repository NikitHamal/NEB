# NEBians Interactive: 3D Simulation Production Pass

## What changed

This pass replaces the NEB Class 11/12 Physics and Chemistry practical simulation entrypoints with a shared optimized Three.js 3D virtual-lab runtime.

### Covered practicals

**Physics Class 11**
- Vernier Calipers
- Micrometer Screw Gauge
- Spherometer
- Simple Pendulum: Measuring g
- Parallelogram Law of Forces
- Coefficient of Friction
- Hooke's Law & Spring Constant
- Specific Heat by Method of Mixtures

**Physics Class 12**
- Resonance Tube
- Sonometer
- Ohm's Law & Resistivity
- Meter Bridge
- Potentiometer
- Galvanometer Figure of Merit
- Focal Length of Mirrors & Lenses
- Prism Minimum Deviation

**Chemistry Class 11**
- Lab Apparatus & Safety
- Separation Techniques
- Acid-Base Titration
- Flame Tests
- Anion Tests
- Gas Preparation
- Water of Crystallization

**Chemistry Class 12**
- KMnO4 Redox Titration
- Full Salt Analysis
- Electrolysis of CuSO4
- pH & Indicators
- Organic Functional Group Tests
- Heat of Neutralization
- Lassaigne's Test

## Implementation details

- Added `web/static/web/js/interactive/core/real-lab-3d.js`.
- Reused the existing local `three.module.min.js` dependency, so the upgrade is free and has no new CDN dependency.
- Converted NEB practical simulation modules into small wrappers that call the shared 3D runtime.
- Added lab-specific formulas and readings for every NEB lesson.
- Added realistic 3D apparatus: glassware, burettes, flasks, test tubes, stands, optical benches, wires, meters, springs, pendulums, prisms, calorimeters, resonance tube, sonometer and electrolysis cell.
- Added live scientific measurement readouts: least count, zero error correction, endpoint status, formula output, vector/resultant values, current/voltage/resistance values, calorimetry, Faraday law and indicator colours.
- Updated NEB catalogs to use `sim_type = 'lab3d'`.
- Updated the lesson template to show `3D virtual lab` and proper 3D interaction hints.
- Added responsive visual CSS in `12-production-lab3d.css`.
- Copied changed static files into `staticfiles/` too, so the ZIP works even before a fresh `collectstatic` run.

## Performance safeguards added

- The Three.js runtime now respects `navigator.connection.saveData` and `prefers-reduced-motion`.
- Low-memory/mobile devices get lower pixel ratio and segment counts automatically.
- WebGL renderer now disables stencil and preserveDrawingBuffer to reduce GPU memory.
- Renderer uses sRGB output and ACES tone mapping where supported.
- Simulation loops remain tied to visibility through the existing engine IntersectionObserver.
- The 3D runtime avoids external models/textures and builds procedural low-poly/medium-poly apparatus to stay fast.
- Control panels are scroll-contained on small screens.

## Validation performed

- JavaScript syntax checked with `node --check` for the shared 3D engine, base engine and all NEB wrappers.
- Python syntax checked with `py_compile` for changed catalogs, models and migration.
- Verified the NEB catalog exposes 30 `lab3d` lessons.

Full Django runtime validation could not be run in this sandbox because Django is not installed in the execution environment. Run the production verification commands below after installing requirements.

## Recommended deployment steps

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py test api.test_security_hardening
```

Then open these lesson URLs and test on desktop + mobile:

```text
/library/interactive/neb-physics-practical-11/vernier-calipers/
/library/interactive/neb-physics-practical-12/ohms-law-resistivity/
/library/interactive/neb-chemistry-practical-11/acid-base-titration/
/library/interactive/neb-chemistry-practical-12/electrolysis-cuso4/
```

Adjust URL prefixes if your deployed route names differ.
