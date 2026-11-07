# NEBians books announcement film: status

Read this before touching the books film or re-rendering it. One doc, update it in place.

## What exists (v2, replaces the 38 s v1)
A 46 s motion film announcing the books library: hook (**92 books, 19,874 pages, Rs 0**), the cover wall with per-class counts, then **three slow
page showcases with real pages held ~1.4 s each**: Class 12 (Physics, Mathematics, Chemistry, Question Bank 12), **IOE** (all 5 books on a title card, then
Physics, Mathematics, Chemistry, Mock Tests pages) and **CEE** (all 6 books, then Physics, Chemistry, Zoology, Mock Tests pages); then the
36/15/41 count, a tapped Download PDF button (`Saved`), `Free.` and the NEBians lockup with `nebians.consica.com.np`.
Formats: `Film9x16` (post this) and `Film16x9` only, 60 fps with motion blur, -14 LUFS. No 1:1.
The score and SFX are new and procedural (D major pads, kalimba and bells, felt drums, paper swishes, UI taps, glass chime on `Saved`, plate reverb),
placed from the same `timeline.json` as the picture.

- **Where it lives:** private repo `NikitHamal/Video`, `neb/tools/video/books-launch/` (Remotion project, `README.md` has the story and the build).
  MP4s: `neb/tools/video/books-launch/dist/nebians-books-<Format>.mp4`. Nothing for it lives in this repo (same rule as the launch films).
- **Source of truth for numbers and pictures:** this repo. `tools/publish/manifest.json` (counts, pages), `tools/publish/covers/*.jpg`,
  the 12 featured PDFs in `notes/pdf/` and `ioe/pdfs/` (`scripts/pages.py <NEB checkout>` picks and renders 4 pages of each: contents, worked example,
  figure, practice), `css/m3x/tokens.css` (palette), Poppins woff2. `scripts/assets.py <NEB checkout>` re-imports covers, books.json and fonts.

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
The GitHub PAT and the molab token were pasted into a chat (again for v2, via a `/tmp` out-of-repo askpass helper and token file that were never committed). Neither is stored in any repo or in the sandbox. Rotate the PAT, and
treat the molab notebook token as burned once the box is released.

## Deliverables (Video repo `main`)
Source commit 006759ec (v2 film), renders 9face976 (both on Video `main`; sha256 of the pulled MP4s was checked against the box). 46.0 s, 60 fps, H.264 + AAC,
`nebians-books-Film9x16.mp4` (1080x1920) and `nebians-books-Film16x9.mp4` (1920x1080); a final render takes ~4 min per format on the molab box.
Visual checks were done on contact sheets cut from stills of the composition and from the final encodes (see the Video repo commit message).
Not done: a listen-through (the score is checked by spectrum, RMS and clipping only) and a real-device preview.
