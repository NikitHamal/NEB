# NEBians launch film (cinetic, Remotion)

37 s, 1920x1080 @ 60 fps, 100 BPM, calm pace; 9:16 and 1:1 re-layouts from the same timeline.
Built with the [cinetic](https://github.com/Leonxlnx/cinetic) skill. Brief: `BRIEF.md`. Concept,
drawn techniques and beat sheet: `TREATMENT.md`.

**Idea.** One stuck page travels through NEBians and becomes the N. The device is the logo's own
light facet: the exercise page in the hook, the post's header in the forum, the header of every
library resource, the reader's page, the gradesheet, the uploaded notes, and at the end it flies
into the mark as the light facet and the rest of the N assembles round it.

**Acts** (`src/acts/`): Hook (inside "Stuck", pull back; the line becomes the Ask bar) · Ask (the
post lands, replies bloom, the teacher's is the answer; tip-back into blue) · Learn (the page
multiplies into the library; every level; ink columns close) · Reader (zoom-out hop to the
phone; Ask Neby; the real Neby lands and explains) · Pass (A+ in close-up, pull back, GPA locks)
· Pass on (Uploaded → Checked → Published → read by 1,240) · Lockup.

**Neby** is the product's own avatar, baked per frame from `neby-avatar.js` through
`tools/video/neby/neby_rig.mjs`:

    node tools/bake-neby.mjs ../neby/neby_rig.mjs <neby-avatar.js> public/neby/reader.json

**Build** (Node 22+, ffmpeg, the cinetic Python deps; earshot in its own venv for the sound kit):

    npm install
    npm run check                      # tsc + lint-film + grid-check
    EARSHOT_PYTHON=<earshot venv>/bin/python npm run cues && npm run kit && npm run audio
    npm run render:preview             # ~3 min on 2 vCPU
    bash scripts/render.sh Film out/film.mp4 --blur --budget 3 --audio public/audio/soundtrack.wav \
      --accept-fast 360-380 --accept-fast 710-730 --accept-fast 950-975 --accept-fast 1292-1310 --accept-fast 1500-1520 --accept-cut 1008-1030
    bash scripts/deliver.sh out/film.mp4 --variants Film9x16,Film1x1

The accepted fast ranges are frame-filling edges (the Ask bar opening, the forum tipping back, the
ink columns, the paper wipe, the gradesheet pull-back), checked at full size; the accepted cut is
the reader rising out of the ink (a designed fade from the stage colour).

Not in git (regenerated): `node_modules`, `out/`, `public/neby/reader.json`, `public/audio/`, `audio/kit/`.
