# tools/art

The app draws its resource banners and profile covers procedurally: 67 banner
arts in `ResourceBannerArt.kt`, 7 cover motifs in `ProfileCoverArt.kt`, all
seeded so the same resource always gets the same picture. The website needs the
*same* pictures — a resource that looks like a prism in the app and a flat
gradient on the web is two products.

Rather than hand-transcribe ~4,400 lines of Compose drawing code into
JavaScript (which would be wrong within a week), these scripts transpile the
shipping Kotlin.

| file | what it is |
| --- | --- |
| `render.py` | parses the Kotlin and transpiles it to Python; renders PNGs for design review |
| `tojs.py` | the JavaScript backend for the same parser |
| `genjs.py` | emits `backend_python/web/static/web/js/neb-art.js` |
| `gensubjects.py` | emits the web's subject colour tokens (CSS module + `templatetags/subject_tokens.py`) from `Color.kt` |
| `cmpsubjects.py` | asserts the art and the CSS class route a subject to the same hue |
| `rec.js`, `recpy.py`, `cmp.py` | record each art's draw-call stream on both platforms and diff them |
| `smoke.js` | runs the generated file through a stubbed DOM, exercising `scan`/`paint`/`prepare` |
| `genglassmap.py` | emits the liquid-glass refraction maps from the same SDF the AGSL uses, and checks every pixel against a scalar transcription of the shader |
| `checkglass.py` | asserts the glass CSS, the SVG filters, the maps and the app's style values all still agree |
| `verify.sh` | all of the above, in order |

```sh
tools/art/verify.sh
```

Everything these scripts write is checked in, so none of it updates itself.
Change `ResourceBannerArt.kt`, `ProfileCoverArt.kt`, `Color.kt` or
`NebLiquidGlass.kt` and you must re-run this, or the web will keep drawing the
old art with the old colours behind the old glass.

## Liquid glass

The app refracts its backdrop in AGSL (`NEB_GLASS_AGSL`). CSS has no per-pixel
shader, but SVG's `feDisplacementMap` offsets each pixel by a vector read out of
a second image — so `genglassmap.py` moves the shader's arithmetic into that
image. Same signed-distance function, same central-difference normal, same cubic
falloff into the outer 21px. The result is two PNGs under
`web/static/web/img/glass/`, consumed by the filters in `base.html` and the rules
in `material3/08-liquid-glass.css`.

`checkglass.py` is the standing assertion that the four pieces still line up: a
renamed filter id, a map that was never regenerated, or a `scale` that drifted
from the app's refraction and dispersion all fail it.

## The Kotlin has to stay transpilable

`render.py` reads a deliberately small subset of Kotlin. Inside a
`fun DrawScope.artSomething(...)` body:

* locals only — no helper functions, no lambdas except transform blocks
* `for (x in 0 until n) {`, `if (c) {`, `} else {`, `} else if (c) {`
* explicit receivers on path builders (`path.moveTo(...)`, not `moveTo(...)`)
* no bitwise infix (`shl`, `and`, ...)
* no local named `d`, `p`, `r`, `math`, `Path`, `Offset`, `Size`, `Stroke`
* multi-line expressions wrapped in parentheses

`verify.sh` fails loudly if you step outside it, which is the point.
