# NEBians books announcement film: status

Read this before touching the books film or re-rendering it. One doc, update it in place.

## What exists
A 38 s motion film announcing the books library for social posts: **92 books, 19,874 pages, Rs 0**, then the covers, a real book opened,
the three groups (36 school, 15 entrance prep, 41 BCA semester books), Download PDF, and the NEBians lockup with `nebians.consica.com.np`.
Formats: `Film9x16` (post this), `Film1x1`, `Film16x9`; 60 fps with motion blur, scored, -14 LUFS.

- **Where it lives:** private repo `NikitHamal/Video`, `neb/tools/video/books-launch/` (Remotion project, `README.md` has the story and the build).
  MP4s: `neb/tools/video/books-launch/dist/nebians-books-<Format>.mp4`. Nothing for it lives in this repo (same rule as the launch films).
- **Source of truth for numbers and pictures:** this repo. `tools/publish/manifest.json` (counts, pages), `tools/publish/covers/*.jpg`,
  `notes/pdf/NEBians-Physics-Grade-12.pdf` (the five pages shown), `css/m3x/tokens.css` (palette), `n-logo-square-icon.svg`, Poppins woff2.
  `books-launch/scripts/assets.py <NEB checkout>` re-imports all of it.

## When to re-render
After books are added or removed, a cover is redrawn, or the Physics 12 PDF is rebuilt: run `assets.py`, check `src/data.ts`
(`HERO`, `GET`) and the covers named in `scenes/Count.tsx` still exist, run `drift`-style sanity by eye on a draft
(`render.sh Film9x16 out/draft.mp4 --draft`, ~1 min), then the final. After a brand palette change, update `src/theme.ts` too.

## How it was rendered (molab, not the VM)
The 1 GB checkout never leaves this VM; the box only gets a 3 MB project tarball and the assets. The box (20 cores, 160 GB, ffmpeg 7,
Node 22, no Chrome until `npx remotion browser ensure`) is driven with `marimo pair execute`; helpers are in
`books-launch/scripts/molab/` and the lessons learned (5-minute idle reclaim, `Python-urllib` 403, detached jobs, stdout cap) are in
`neb/docs/RENDER_RIGS.md` in the Video repo. A keeper GETting `/api/status` every 20 s kept the sandbox alive for the whole job.
A final 120 fps motion-blur render takes ~8 min per format on that box; a 30 fps draft ~1 min.

## Rules the film follows (same as the product)
Poppins, M3X blue/navy/sky/paper, flat fills only, no shadows, no gradients, no emoji, no live badge, no strokes on frames,
no sharp-corner morphs, fragments of 1-4 words. The scene change is a rotating M3E cookie shape that grows from the middle.

## Security note
The GitHub PAT and the molab token were pasted into a chat. Neither is stored in any repo or in the sandbox. Rotate the PAT, and
treat the molab notebook token as burned once the box is released.

## Deliverables (Video repo `main`, commits d50fbd7d source, 1285d66b renders)
`neb/tools/video/books-launch/dist/`: `nebians-books-Film9x16.mp4` (43 MB, 1080x1920), `-Film1x1.mp4` (23 MB), `-Film16x9.mp4` (1920x1080), each 38.0 s, 60 fps, H.264 + AAC.
Visual checks done on contact sheets cut from the final encodes: 9:16 (all scenes), 1:1 (all scenes), 16:9 (all scenes; its Get title and End lockup
were fixed after the first sheet and that final render was not re-sheeted, look at it before posting). Not done: a listen-through (the score is checked
by loudness only: LRA 4 LU, true peak under -2 dBFS), real-device preview.
