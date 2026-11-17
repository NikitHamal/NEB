# M3X Art Library v4

Open `NEBians-Art-v4.html` (published as `art-v4.html` on GitHub Pages).

- 2,464 named pieces, each rendered live in Light and Dark (4,928 SVGs). Same id, same art, in the browser, in `export-svg.js` and in later Kotlin ports.
- 15 kinds: cover, school, thumb, book, post, bg, tile, spot (empty states), sticker (achievements), avatar, pathway, lab, story, pattern, wide (hero).
- 35 engines: 28 abstract scenes and patterns, `stage` (hero objects on 6 backdrops), `person`, `buddy`, `critter`, `glyphTile`.
- 36 hero objects, drawn in a 100 unit box (`v4-objects-a.js`, `v4-objects-b.js`), 40 empty states x 4 looks, 24 achievements x 4 looks.
- Profile pictures: 240 people (10 hairstyles, 6 skin tones, 7 outfits, topi, glasses, headphones, grad cap), 60 buddies, 72 critters, glyph tiles, object avatars. Frameless squares; the gallery shows them clipped to eight expressive shapes. No ring, no border.
- Never drawn (owner ban): mountains, forests, trees, ships or boats, rows of buildings, moon, sun. Flat fills only, no gradients, shadows, filters, text, emoji or pixel art. No purple family.
- Check: `node concepts/art-v4/export-svg.js` (fails on NaN, undefined, gradients, filters, images, text). Add `--svg` to write `svg/` (git-ignored).
- Builds on `art-v3/v3-core.js` (OKLCH palettes, expressive shapes, noise). v1 to v3 are untouched.
