# M3X Art Library v5

Open `NEBians-Art-v5.html` (published as `art-v5.html` on GitHub Pages). Concept only: no app, backend or database file is touched.

- 2,484 named pieces, each rendered live in Light and Dark (4,968 SVGs). Same id gives the same art in the browser, `export-svg.js` and later Kotlin ports.
- 15 kinds: avatar, cover, school, thumb, book, post, bg, tile, spot (empty states), sticker (achievement badges), pathway, lab, story, pattern, wide.
- Rule set that separates v5 from v4: one hue per piece (tonal ramp + paper + ink, optional analogous second hue on banners), one hero per piece, at most one small status mark, no scattered dots, plus signs or sparkles, no stacked icon chips, no rainbow palettes in empty states or badges.
- Faces: 480 people. Almond eyes with iris and highlight, lid line, tapered brows, nose, ears, neck shadow, 8 skin tones, 12 hair styles (crop, sweep, buzz, curly, long, wavy, bob, bun, braid, pixie, elder, scarf), 9 outfits (tee, hoodie, blazer, daura, lab coat, cardigan, turtleneck, kurta, v-neck), glasses, headphones, Dhaka topi, grad cap, bindi, earrings, beard, 4 expressions. Frameless squares, no ring.
- 43 hero objects (100 unit box, tone roles only), 14 calm scenes, 45 empty states x 4 looks, 28 achievements x 5 tiers/shapes (seal, shield, hex, round, bloom; gold, silver, bronze, blue, emerald, each one hue).
- Never drawn (owner ban): mountains, forests, trees, ships, building rows, moon, sun. No gradients, shadows, filters, text, emoji or pixel art.
- Gallery: Library (lazy, kind rail, subject filter, search, detail dialog with copy, SVG, 2x PNG and avatar in clip shapes), In-app, Studio (avatar builder and banner builder).
- Check: `node concepts/art-v5/export-svg.js` (fails on NaN, undefined, gradients, filters, images, text, duplicate ids). Add `--svg` to write `svg/` (git-ignored). Self-contained: no v1 to v4 code is used.
