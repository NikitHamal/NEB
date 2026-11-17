# M3X Art Library v3

Open `NEBians-Art-v3.html` (published as `art-v3.html` on GitHub Pages).

- 1,530 named pieces, each as Light and Dark SVG in `svg/{light,dark}/<kind>/<id>.svg` (3,060 files). `catalog.json` lists ids, names, subjects.
- 14 kinds: cover, school, thumb, book, post, bg, tile, spot, sticker, avatar, pathway, lab, story, pattern.
- 34 engines: 14 layered scenes (depth ramp), 15 patterns, 1 still-life engine (36 study objects), 4 avatar engines.
- `v3-core.js`: OKLCH palettes (20 families, no purple), depth ramp, expressive shapes, seeded noise. Flat fills only: no gradients, shadows, filters, text, emoji or pixel art. Avatars are frameless squares to clip to any shape.
- Deterministic: the same `id` gives the same art in the browser, in `export-svg.js` and later in Kotlin ports.
- Regenerate: `node concepts/art-v3/export-svg.js` (fails on NaN, undefined, gradients, filters, images, text).
