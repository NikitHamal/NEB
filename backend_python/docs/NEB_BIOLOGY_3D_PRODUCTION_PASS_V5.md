# NEB Biology 3D Production Pass V5

## Scope
This pass fixes the Biology gap by separating NEB Biology practicals into Class 11 and Class 12 courses and converting the practical lessons to a shared real-time 3D biology lab runtime.

## Catalog changes
- Replaced the old mixed `NEB Biology Practicals — Class 11 & 12` course with two separate courses:
  - `neb-biology-practical-class-11` with 18 practical lessons.
  - `neb-biology-practical-class-12` with 25 practical lesson simulations.
- Class 12 practical item 8, which contains four observation setups, was split into four separate 3D labs: anaerobic respiration, phototropism, apical bud removal, and suction due to transpiration.
- The repeated skeleton/joints curriculum entry is preserved as two separate learning contexts: anatomy and health-disorder/joint mobility context.

## Runtime changes
- Added `web/static/web/js/interactive/biology/neb-bio3d.js` as the Biology 3D entrypoint.
- Added modular core files:
  - `bio3d-data.js` — metadata and control definitions for all Biology practicals.
  - `bio3d-models.js` — 3D apparatus/specimen builders.
  - `bio3d-runtime.js` — WebGL setup, controls, observation book, live readings, trial handling.
- All NEB Biology practical lessons now use `sim_type='lab3d'` and share the optimized 3D runtime.

## UX and responsiveness
- Uses compact controls by default on mobile.
- Collapses the Biology 3D control panel on small screens.
- Limits observation-book scrolling inside the panel instead of expanding the entire panel.
- Reuses v4 safe-area and `svh` mobile sizing fixes.
- Adds `View`, `Step`, `Record`, `Trial`, `Clear`, and `Help` buttons with short labels to avoid control bloat.

## Simulation realism added
- Compound microscope with objective turret, stage, slide, light source and focus controls.
- Microscope field boards for plant tissues, mitosis, stomata, plasmolysis, animal tissues, animal mitosis and frog development.
- Herbarium sheet, mushroom morphology, flower dissection, inflorescence comparison, soil culture plate, pond ecosystem, quadrat grid, soil analysis, fossil specimen, animal specimen tray and guided dissection tray.
- Plant physiology apparatus for potato osmometer, transpiration pull, respiration, anaerobic fermentation, phototropism and apical bud removal.
- Genetics seed tray and real ratio readouts.
- Food/clinical tests for starch, protein, urine and blood sugar.
- Human skeleton/joint models and cockroach external morphology model.

## Validation performed
- JavaScript syntax check passed for new Biology 3D modules.
- Python syntax check passed for the updated Biology catalog and existing interactive runtime files.
- ZIP integrity checks passed for full and changes-only deliverables.

## Local checks still needed
The sandbox does not have the Django project dependencies installed. Run locally:

```bash
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```
