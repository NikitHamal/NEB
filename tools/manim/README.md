# The Manim video pipeline

Videos for the class 11 and 12 science stream are written as Python and rendered
with [Manim Community](https://www.manim.community/).  Nothing is edited by hand:
every pixel on screen comes from `videos/*.py`, and the voice-over is cut from
the same file the picture is, so the two cannot drift apart.

```
tools/manim/
├── bootstrap.sh            create the toolchain from scratch
├── requirements.txt        the Python side of it
├── make_gl_stubs.sh        stub libEGL/libGL so skia-python imports
├── make_narration.py       the voice-over, one string per beat
├── neb/                    the shared library
│   ├── theme.py            palette, type scale, NebEpisode scene base
│   ├── components.py       cards, tables, quizzes, diagrams, vernier, target
│   └── mathtext.py         NebMathTex, maths without LaTeX
├── shims/
│   ├── cairo/              pycairo stand-in drawn with skia-python
│   └── manimpango/         manimpango stand-in drawn with FreeType
├── videos/                 one file per episode
├── audio/                  the recorded narration groups
├── assets/fonts/           Poppins
└── scripts/
    ├── build.py            the whole pipeline in one command
    ├── render.sh           manim with the environment the shims need
    ├── layout.py           replay the scene: bounds audit and beat clock
    ├── mux.py              drop the narration onto the beat clock
    └── qa.py               container, level, and a contact sheet
```

## Set up

```sh
tools/manim/bootstrap.sh
```

That builds a virtualenv at `/home/user/.nebvideo-venv`, installs the packages
in `requirements.txt`, compiles the `libEGL`/`libGL` stubs that `skia-python`
demands at import time, and links an ffmpeg onto `PATH`.  It is safe to re-run.

There is no `pycairo` and no `manimpango` on this machine, and neither can be
built here — no cairo headers, no pkg-config, no working apt mirror.  Manim only
uses two things from each: rasterising paths, and laying out glyphs.  `shims/`
provides exactly those two, backed by `skia-python` and `freetype-py`, so manim
runs unmodified.

## Make a video

```sh
tools/manim/scripts/build.py videos/phy11_unit01.py PhysicalQuantities --out out/phy11_unit01.mp4
```

In order:

1. **`layout.py beats`** replays `construct()` against a recording scene that
   advances a clock instead of a camera, and writes `build/beats.json` — the
   scene time at which each line of narration starts.
2. **`render.sh`** renders the picture at 1080p30.
3. **`mux.py`** delays each recorded narration group by its first beat's clock
   time, mixes them onto one track, loudness-normalises it, and muxes it with
   the video.
4. **`qa.py`** reports container, duration, resolution and level, and leaves a
   contact sheet of frames spread through the episode.

## The narration

`make_narration.py` holds the voice-over as one string per beat, grouped the way
it is recorded (one group per synthesis call, each inside the character limit).

```sh
tools/manim/make_narration.py script                      # read it back
tools/manim/make_narration.py timings tools/manim/audio   # measure it
```

`timings` writes `videos/timings.json`, and `NebEpisode.beat` reads that file to
hold each picture for exactly as long as its own line of voice-over runs.  So
re-cutting the narration is a matter of re-recording and re-running
`make_narration.py timings`; the scene never changes.

`NEB_TIMING_SCALE=0.1` shrinks every hold, which renders the whole episode in a
couple of minutes for a layout check.

## Checking a layout without rendering

```sh
tools/manim/scripts/layout.py videos/phy11_unit01.py
```

Replays the scene and prints the bounding box of everything on screen at every
beat, flagging anything outside the theme margins or up into the section header.
`beats` mode does the same replay but writes the clock instead.

## The design system

All colour, type and spacing come from `neb/theme.py`, which mirrors
`tools/design/palette.py` — the same palette the notes use.  Nothing in
`videos/` hard-codes a colour.

Stroke widths are the one place to be careful: manim's camera multiplies every
`stroke_width` by `cairo_line_width_multiple = 0.01`, so the value is in
*hundredths of a frame unit*, not frame units.  `C.stroke(px)` converts pixels at
1080p.  Writing a raw `0.04` produces ink two percent of the width you meant.
