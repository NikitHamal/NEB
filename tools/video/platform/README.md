# NEBians platform launch film (22 s)

The main launch film for the NEBians platform — replaces the older browser-rendered
`dist/nebians-launch-16x9.mp4`. Built around the site's own hero line, "Study **materials**.
Study **mates**.", hosted by the real Neby.

```
pip install skia-python numpy scipy pillow     # node 18+ and ffmpeg on PATH
cd tools/video/platform
python3 stills.py /tmp/sheet.png 1.3 3.9 8.2 10.9 14.9 16.9 21.0
python3 render.py /tmp/draft.mp4 --draft
python3 render.py ../dist/nebians-launch-16x9.mp4      # 60 fps master, ~8 min on 2 vCPU
```

Set `NEBY_AVATAR_JS` if `backend_python/web/static/web/js/neby-avatar.js` is not checked out.

## Neby

Neby is the product's own avatar geometry (`neby-avatar.js`), driven by `../neby/rig.py`
through `../neby/neby_rig.mjs`: expressions from Neby's own library are blended with layered,
eased crossfades (no timer steps), blinks are cosine dips, eye-lines follow what Neby is
looking at, ambient breathing/bobbing is blended between expressions, and hops carry
anticipation, stretch, lean and a damped landing squash. Its performance is the `PERF` list
in `film.py`.

## The film (120 BPM)

| Seconds | Scene | What happens |
|---|---|---|
| 0–2.5 | hook | Four full-bleed word slams on the beat — Notes. Past papers. Textbooks. Questions. — the colour field implodes and Neby pops out. |
| 2.5–5 | hello | Neby hops aside; app tile, the real N assembling facet by facet, "NEBians", "Nepal's learning community". |
| 5–9 | study materials | Search types "class 12 physics notes"; level chips Class 8 → Masters; six resource cards (PDF, past paper, notes, textbook, model questions) draw their banners. |
| 9–12.5 | study mates | A discussion types out, likes tick up, replies from a student and a teacher, a poll fills. |
| 12.5–15.5 | share, earn, climb | A PDF drops into the upload zone, progress ring, *Top contributor* badge, the leaderboard reorders as you climb to #2. |
| 15.5–18 | handy tools | Result Checker (gradesheet bars, GPA counter), PDF tools (pages merging), Android app with *Ask Neby* in the PDF reader — the only AI mention. |
| 18–22 | end card | Blue wipe from Neby, confetti, Neby celebrates and winks; tile + N, NEBians, "Study materials. Study mates.", URL, "Free on the web · Android app on Google Play", "Class 8 to Masters". |

Names in the forum and leaderboard (Asha, Rohan, Ms. Pandey, Prashant, …) and the resource
titles are illustrative of what is on the site, not specific records.

## Sound

`score.py` — bright modern groove (kick, snap, hats, bass, marimba arpeggio over C–G–Am–F),
with madal accents (*ta*, *dhin*) from bar 4 and a bansuri phrase on the end card; slams,
implode, pops, ticks, typing, likes, upload rise, badge bells, swaps, riser and boom from
`film.CUES`. Loudness −14 LUFS.

## Vertical (9:16) cut

`FILM_ASPECT=9x16 python3 render.py ../dist/nebians-launch-9x16.mp4` renders a 1080×1920 version for
TikTok, Instagram Reels and Stories. It is not a crop: every scene has its own portrait layout
(stacked headlines, 2-column grids, stacked panels, end card stacked under Neby), chosen in the
code with `VERT` from `../neby/kit.py`.

## Type

Everything is set in Poppins (`../assets/fonts`), including the Nepali lines — Poppins ships a
full Devanagari set, shaped with HarfBuzz (PIL + raqm) so conjuncts and matras render correctly.
