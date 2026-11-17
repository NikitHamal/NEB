# NEBians M3X art library v7 (from v1)

Built only from v1 (`concepts/art/`): its seeded engine, expressive shapes, 6-tone flat palettes and 15 of its 18 compositions
(hills, sunset and rays are dropped: they read as mountain and sun). v2 to v6 code is not used.
Live gallery: `NEBians-Art-v7.html` (GitHub Pages: `art-v7.html`).

- `v7-core.js` 18 families (v1's 12 + sage, clay, ocean, citrine, cherry, lagoon), 8 tones tuned for Light and Dark, helpers
- `v7-lay-c.js`, `v7-lay-d.js` 17 new compositions (pinwheel, mondrian, halftone, capsules, cascade, swirl, ripple, venn, truchet, contour, blobs, rings, bento, diamonds, segments, bands, petalfield) and a calmer `waves`
- `v7-make.js` 15 kinds, 34 subjects. Book cover = spine, medallion, bookmark ribbon; the v1 text card (bubble look) is gone
- `v7-scenes.js` empty states (4 layouts) and profile pictures (8 frameless looks, no faces)
- `v7-catalog.js` 2,340 named pieces, stable ids; `catalog.json` is its index
- `export-svg.js` check (`node export-svg.js`), `--svg` writes Light and Dark SVGs (not committed), `--android DIR` writes the Android note covers
- `build-glyphs.js` rebuilds `v7-glyphs.js` (188 Material Symbols paths; no tree, sun, moon, mountain or ship icons)

Android: 72 note covers ship as WebP in `app/src/main/assets/note_covers/{light,dark}` (cover index 41 to 112, `NoteArtCover.kt`).
Never change the order inside a kind: ids and note cover indexes depend on it. Append only.
