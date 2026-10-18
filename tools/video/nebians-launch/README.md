# NEBians launch film — Dashain release (20 s)

The launch film for NEBians, released on Dashain together with the class 8, 10, 11 and 12
notes and question banks in `notes/`. Minimal vector motion design, starring the **real
Neby**: the product's own avatar geometry (`backend_python/web/static/web/js/neby-avatar.js`),
animated by `../neby/rig.py` — eased blends between Neby's own expressions, blinks, eye-lines and
squash/stretch on every hop (the performance is `PERF` in `neby_player.py`).

```
pip install skia-python numpy scipy pillow     # PIL must have raqm (Devanagari shaping); node 18+ and ffmpeg on PATH
cd tools/video/nebians-launch
python3 stills.py /tmp/sheet.png 1.9 4.6 8.4 12.9 14.9 19.5   # review any moments
python3 render.py /tmp/draft.mp4 --draft                        # 30 fps preview, ~40 s
python3 render.py ../dist/nebians-launch-dashain-16x9.mp4       # 60 fps master, ~6 min on 2 vCPU
```

Set `NEBY_AVATAR_JS` if the repo's web static files are
not checked out, and `NEBY_DEVA_FONT` to a Noto Sans Devanagari Bold file for "शुभ दशैँ".

Master: 1920×1080, 60 fps, H.264 CRF 16 bt709, 7-sample motion blur, AAC 192 kb/s at −14 LUFS.

## The film (120 BPM)

| Seconds | Scene | What happens |
|---|---|---|
| 0–3 | hook | Dashain sky: kites, clouds, hills. Neby rises and plays its own cinematic reveal. "This Dashain, your **books** are here." |
| 3–7 | notes & question banks | Class 8, 10, 11 and 12 books swoop in like kites and land on the beat, each tagged *Notes* and *Question bank*; a counter rolls to **6,000+ pages**, *All free*. |
| 7–10.5 | inside a book | A book opens and flips: worked example, formula box, a diagram drawing itself, ticked answers. "Every chapter." → "Every answer **worked out**." Twelve subject chips (incl. नेपाली, सामाजिक) pop in. Neby scans the page. |
| 10.5–13.5 | community | "Ask. Answer. **Study together.**" A forum thread types itself out, likes pop. Neby laughs. |
| 13.5–16 | Android app | "Read anywhere." A phone rises with a PDF page; *Ask Neby* is tapped and a sheet slides up with the real Neby speaking. (This is the only AI feature in the film — Ask Neby in the Android PDF reader.) |
| 16–20 | end card | Blue wipe, confetti, Neby celebrates then winks; app tile with the real N assembling facet by facet; NEBians; "Notes & question banks · Class 8, 10, 11, 12"; URL; "Free on the web · Android app on Google Play"; **शुभ दशैँ**. |

## Sound

`score.py` — a Dashain fusion, all synthesised: madal strokes (*dhin* low, *ta* slap) in a
groove with a modern kick, snap, hats and sub; a breathy bansuri-style flute playing a D-major
pentatonic theme (intro phrase, two groove phrases, a closing flourish); pads and bells. Every
sound effect (kite flutter, landing thuds, page turns, pencil, ticks, pops, likes, tap, sheet,
riser, boom, confetti) comes from `film.CUES`, so picture and sound stay locked.

## Claims (keep them true)

- Class 8, 10, 11, 12 notes and question banks — the books in `notes/pdf/` (published on Dashain).
- 6,000+ pages, all free — about 6,170 pages across those books at render time.
- Ask Neby in the Android app's PDF reader — the only AI feature shown.
- nebians.consica.com.np, free on the web, Android app on Google Play.
