# tools/svgart

The NEBians art library: illustrations drawn in code as SVG, in the aesthetics of
[issue #62](https://github.com/NikitHamal/NEB/issues/62).

| look | what it is |
| --- | --- |
| `riso` | risograph grain: flat monumental shapes lit in stipple, stippled glows, paper grain; periwinkle, lemon, salmon, plum |
| `flat` | warm editorial vector: cream ground, two-tone shapes, hairline veins and folds; lavender, mustard, coral, olive |
| `pixel` | the flat scene redrawn as pixel art: rendered small, ordered dithering on gradients, 1 px outlines, written back as SVG runs |

| file | |
| --- | --- |
| `kit.py` | the SVG writer, filters (stipple, paper grain), palettes, shape helpers |
| `painter.py` | one drawing vocabulary (`form`, `glow`, `sky`, `ground`, `mountains` ...) painted by `RisoPainter` or `FlatPainter` |
| `props.py` | characters (the glowing figure, Neby's orb) and props (books, flask, atom, prism, school, prayer flags ...) |
| `scenes.py` | the scenes: profile covers (7 account types), resource banners (12 subject families), onboarding (6), empty states (8), backgrounds (4) |
| `build.py` | writes `backend_python/web/static/web/art/<set>/<name>-<look>.svg` and `manifest.json` |
| `pixel.py` | makes the pixel versions from the flat ones (needs Playwright's Chromium and Pillow) |

```sh
python3 tools/svgart/build.py && python3 tools/svgart/pixel.py && python3 tools/svgart/build.py
```

Everything is seeded, so a rebuild writes the same files. The admin panel shows the library at
`/admin/art/`; nothing on the site or in the app uses it yet.
