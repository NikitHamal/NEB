# NEBians M3X art library (concept)

Flat tonal SVG art, no gradients, no pixels, no emoji. Live gallery: `NEBians-Art.html` (GitHub Pages: `art.html`).

- `art-core.js` seeded random, palettes (12 families, light and dark), expressive shapes
- `art-layouts-a.js`, `art-layouts-b.js` 18 compositions
- `art-make.js` kinds (cover, school, thumb, book, post, bg, tile, sticker), 26 subjects, `NebArt.make()`
- `art-catalog.js` the named set (725 pieces, stable ids)
- `glyphs.js` Material Symbols paths (Apache 2.0)
- `svg/{light,dark}/<kind>/<id>.svg` exported set, regenerate with the catalog

Same seed gives the same picture on web and Android. Nothing here is wired into the app yet.
