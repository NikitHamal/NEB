# Biology 3D Scan-Grade Pass v8

This pass upgrades the Biology interactive models and NEB Biology practicals with a scan-grade procedural PBR layer.

## Included changes

- New `bio3d-scan-grade.js` renderer helper for PBR albedo, relief, roughness, micro-displacement and specimen-specific details.
- NEB Biology lab3D practicals now receive per-practical scan-grade enhancements through `buildBiologyModel`.
- Beginner Biology lessons upgraded:
  - Human Body Explorer: pores, capillary/nerve micro detail, PBR organs and displaced tissue surfaces.
  - Heart & Lungs: alveoli, coronary vessels, tissue relief and PBR membranes.
  - Photosynthesis: PBR leaf cuticle, veins, stomata and micro-displaced leaf surface.
  - Butterfly Life Cycle: wing scales, larval setae, PBR chitin/wing surfaces.
- Static and collected-static copies were both updated so the patch works whether deployment serves from `web/static` or `staticfiles`.
- Runtime HUD/panel now exposes the visual standard as scan-grade PBR plus calibrated scientific readings.

## Important note

No third-party scanned meshes were bundled. The upgrade is a high-detail procedural/PBR scan-grade pass designed to run fast in the browser and avoid unlicensed photogrammetry assets. If you later obtain licensed GLB/GLTF scans, this layer can sit underneath a true mesh asset loader.
