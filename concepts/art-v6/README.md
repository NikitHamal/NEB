# M3X Art Library v6

Open `NEBians-Art-v6.html` (published as `art-v6.html` on GitHub Pages).

- 3,442 named pieces, each rendered live in Light and Dark (6,884 SVGs). Same id, same art, in the browser, in `export-svg.js` and in later Kotlin ports.
- 17 kinds: cover, school, thumb, book, post, bg, tile, spot (empty states), sticker (achievements), avatar, pathway, story, pattern, wide, strip, wall (phone wallpapers), icon.
- 11 new scene engines (no landscapes): `truchet`, `bauhaus`, `voronoi` (stained glass), `lowpoly` (facets), `silk`, `vortex` (twisted echoes), `bento` (M3 shape tiles with glyphs), `dotwave`, `packing`, `morphGrid`, `doodle`.
- Compositions: `show` (a scene behind a hero object on a card, shape or ring plate), `empty` (a pal and a prop, four layouts), `scenic` (scene plus a paper-edged calm panel for profile covers).
- Profile pictures: 420 refined people (ears, neck shade, brows, nose, ten hair styles with back and front layers, eight outfits, glasses, headphones, topi, grad cap, hijab, bindi), 200 pals (expressive-shape characters with faces), 120 subject marks. Frameless squares, no ring. The gallery shows them clipped to expressive shapes.
- Colour: v3 OKLCH families (no purple, no `sun`) plus a partner family per palette for one warm or cool accent; every scene has a calm and a deep scheme.
- Never drawn (owner ban): mountains, forests, trees, ships or boats, rows of buildings, moon, sun. Flat fills only, no gradients, shadows, filters, text, emoji or pixel art.
- Check: `node concepts/art-v6/export-svg.js` (fails on NaN, undefined, gradients, filters, images, text). Add `--svg` to write `svg/` (git-ignored).
- Builds on `art-v3/v3-core.js` (palettes, shapes, noise) and `art-v4` (flat helpers, 36 hero objects, subject table). v1 to v5 are untouched (v5 is a separate library by another session, `art-v5/`). No scattered dots, sparkles or stacked icon chips: removed on owner feedback recorded in session 70.
