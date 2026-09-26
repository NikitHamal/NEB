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
| `rec.js`, `recpy.py`, `cmp.py` | record each art's draw-call stream on both platforms and diff them |
| `smoke.js` | runs the generated file through a stubbed DOM, exercising `scan`/`paint`/`prepare` |
| `verify.sh` | all of the above, in order |

```sh
tools/art/verify.sh
```

The generated file is checked in, so it does not update itself. Change any of
the three Kotlin sources and you must re-run this, or the web will keep drawing
the old art.

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
