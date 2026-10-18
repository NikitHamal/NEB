# Dashain and Tihar with NEBians (cinetic, Remotion, pixel art)

34.6 s, 1920x1080 @ 60 fps, 100 BPM, every on-screen word in Nepali; 9:16 and 1:1 re-layouts from
the same timeline. Brief: `BRIEF.md`. Picks and beat sheet: `TREATMENT.md`.

**Idea.** One kite carries the season: it leaves a rooftop at dawn as jamara sprouts, rises among
the valley's kites, holds its place while day drains into night (दशैं becomes तिहार), and its string
lights up as Tihar's string of lamps. Diyos light one per beat, a rising scale of bells; a rangoli
fills in; the dog in its marigold garland looks up; a student reads NEBians by diyo light; the N
assembles over the night town: शुभ दशैं, शुभ तिहार.

**Pixel art.** Every scene is drawn per frame by code (`src/pixel/`): a small framebuffer
(320x180 art pixels in 16:9, 180x320 in 9:16) scaled exactly 6x with no smoothing. The festival
palette lives in `src/brand/tokens.ts` (P), marked culture-supplied.

**Build**

    npm install    # or link the launch film's node_modules
    npm run check
    EARSHOT_PYTHON=<earshot venv>/bin/python npm run cues && npm run kit && npm run audio
    bash scripts/render.sh Film out/film.mp4 --audio public/audio/soundtrack.wav   # sharp: pixel art is not motion-blurred
    bash scripts/deliver.sh out/film.mp4 --variants Film9x16,Film1x1

**QA.** tsc, lint-film, grid-check, probe and sync pass. Forensics passes except for small one-frame
changes where pixel art steps by a whole art pixel (jamara growing, a kite's tail, the string
lights): the medium's own grain, checked at full size. The chapter cuts are declared
(`--cuts 288,576,864,1152,1440,1728`).
