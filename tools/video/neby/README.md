# Neby — the NEBians launch film (18 s)

A minimal, vector, mascot-led motion film. Every frame is a pure function of time,
drawn with Skia; the score and every sound effect are synthesised from the same cue
list, so picture and sound cannot drift apart.

```
pip install skia-python numpy scipy pillow     # plus ffmpeg on PATH
cd tools/video/neby
python3 stills.py /tmp/sheet.png 1.5 5.8 9.6 13.6 17.3   # look at any moments
python3 render.py /tmp/draft.mp4 --draft                 # 30 fps, no blur, ~1 min
python3 render.py ../dist/nebians-neby-launch-16x9.mp4   # 60 fps master, ~4 min on 2 vCPU
```

Master: 1920×1080, 60 fps, H.264 (CRF 16, bt709), AAC 192 kb/s, loudness-normalised
to −14 LUFS / −1 dBTP. Motion blur is real: three renders per frame across a
180° shutter, averaged.

## Files

| File | What it holds |
|---|---|
| `kit.py` | canvas size, brand palette (from the site CSS), easing, drawing helpers |
| `characters.py` | **Neby** (the mascot), the classmate blobs, and the real five-facet N logo (`n-logo-tight-no-outline.svg` geometry) |
| `film.py` | the timeline: `CUES`, Neby's path through the film (`neby_track`), and one function per scene |
| `score.py` | synthesiser: 120 BPM groove (kick, snap, hats, bass, marimba over C–Am–F–G), end chord, and one generator per cue kind |
| `render.py` | frames → ffmpeg, with the score muxed in |
| `stills.py` | contact sheet of chosen times, for reviewing without rendering |

## The film (120 BPM, 0.5 s per beat)

| Seconds | Scene | What happens |
|---|---|---|
| 0.0–2.0 | hello | A blue drop falls, squashes on the floor, bounces and opens its eyes: Neby. "Hi, I'm Neby!" |
| 2.0–5.0 | materials | Neby hops aside; "Study **materials.**" (the site's own hero device) types up while four cards — Notes, Diagrams, Solutions, Model papers — fly out of Neby and fan out, each drawing its own glyph. |
| 5.0–8.5 | books | A shelf draws itself; six subject books thud down on the beat; Neby leaps onto the tallest one and a graduation cap drops onto its head. "Full books." Grade 8 · 10 · 11 · 12, a counter rolls to **6,000+ pages**, "All free". |
| 8.5–11.5 | book | A book opens: "Explained." (text lines write themselves, a highlight sweeps), "Drawn." (bar chart grows, a right triangle draws), "Solved." (three ticks). |
| 11.5–14.5 | together | Six classmate blobs pop in around Neby, network lines draw, a "?" is answered by a "!". "Study together." |
| 14.5–15.0 | leap | Neby leaps at the camera; its blue body fills the frame and becomes the end card. |
| 15.0–18.0 | end | App tile pops in, the real N assembles facet by facet inside it, "NEBians" rises letter by letter, tagline, URL pill, "Free on the web · Android app on Google Play". Neby peeks from the corner and winks. |

## Claims the film makes (keep them true)

- **Grades 8, 10, 11 and 12** — the books in `notes/pdf/`.
- **6,000+ pages, all free** — sum of the page counts of the grade 8, 10, 11 and 12 books in
  `notes/pdf/` (about 6,170 at the time of the render: grade 8 ≈ 1,210, grade 10 ≈ 2,140, grades 11–12 ≈ 2,820). If books are removed, re-check.
- **nebians.consica.com.np**, free on the web, Android app on Google Play — as in `../spec/launch.spec.json`.

## Changing it

- Copy, colours, timings: `film.py` (scene functions read `t` in seconds). Move a sound with
  its picture by editing the matching entry in `CUES`.
- Neby's look: `characters.neby()` — body colours, eye size, cheeks, cap.
- Sound: `score.sfx(kind)` for effects, `score.arrange()` for the music.
