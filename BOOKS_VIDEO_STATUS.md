# NEBians books announcement film: status

Read this before touching the books film or re-rendering it. One doc, update it in place.

## What exists (`v1`, `v2`, and `v3` in `dist/`)
All three versions of the books announcement film (9:16 and 16:9 only, no 1:1) are preserved side-by-side in `NikitHamal/Video` under `neb/tools/video/books-launch/dist/`:
- **v1 (`nebians-books-v1-Film9x16.mp4`, `nebians-books-v1-Film16x9.mp4`):** 38 s original launch film recovered from commit `1285d66b`.
- **v2 (`nebians-books-v2-Film9x16.mp4`, `nebians-books-v2-Film16x9.mp4`):** 46 s v2 film preserved from commit `9face976`.
- **v3 (`nebians-books-v3-Film9x16.mp4`, `nebians-books-v3-Film16x9.mp4`):** 46 s complete motion & sound overhaul:
  1. **Hook (`0.0–4.5 s`):** High-speed 14-page **Riffle Blitz** flipping through real content pages across 14 books (Physics 12, CEE Zoology, IOE Physics, Chemistry 12, Mathematics 10, BCA Data Structures, CEE Botany, Mathematics 12, IOE Chemistry, Biology 12, Science 10, Computer Science 12, CEE Chemistry, Question Bank 12) with live stream/page chips and a tabular counter climbing to `19,874 pages.`, followed by `92 books.` (`36 School · 15 Entrance · 41 Bachelors`) and an electric blue M3E cookie burst into `Rs 0.` (`Every single book. Free.`).
  2. **Wall (`4.5–9.5 s`):** Tilted 92-cover matrix decelerating while all **8 stream spotlight cards** (`Class 8`, `Class 10 · SEE`, `Class 11`, `Class 12`, `CEE Entrance`, `IOE Entrance`, `BCA Entrance`, `BCA Semesters`) pop in — each displaying 3 real 16:9 covers from that stream — before the `Physics 12` hero cover rises.
  3. **Class 12 / School Showcase (`9.5–17.5 s`):** Uncropped 1:1 page deck (zero zoom-in on pages) with a live progress pill bar across `Physics 12` (`contents` — the **only** Table of Contents page shown in the entire film, followed by `opener` Unit 1 Rotational Dynamics), `Mathematics 12` (`worked`), `Chemistry 12` (`figure`), `Biology 12` (`figure`), and `Question Bank 12` (`practice`, 1,010 pages).
  4. **IOE Showcase (`17.5–24.5 s`):** Bento title card displaying all **5 IOE covers** (`5 books · 293 pages`), followed by 1:1 content pages for `IOE Physics` (`figure`), `IOE Mathematics` (`worked`), `IOE Chemistry` (`figure`), and `IOE Mock Tests` (`practice`).
  5. **CEE Showcase (`24.5–31.5 s`):** Bento title card displaying all **6 CEE covers** (`6 books · 2,246 pages`), followed by 1:1 content pages for `CEE Physics` (`figure`), `CEE Chemistry` (`figure`), `CEE Zoology` (`figure`), and `CEE Botany` (`figure`).
  6. **Count (`31.5–36.5 s`):** 3 M3E Bento cards (`36 School books · Class 8 to 12`, `15 Entrance prep · CEE · IOE · BCA`, `41 BCA semesters · Semester 1 to 8`), each with 3 fanned book covers, resolving to `19,874 pages.` and `Class 8 to Bachelors.`.
  7. **Get (`36.5–41.0 s`):** `Read it.` -> `Download PDF` button tap (`Keep it.`) with pages flying into the `Mathematics 12` cover -> `Saved` -> `Free.` (`Rs 0 · No login wall`).
  8. **End (`41.0–46.0 s`):** The **official 4-facet isometric NEBians `N` logo** (`public/brand/n.svg`) assembles facet-by-facet on `C.paper`, followed by `NEBians`, `Study materials. Study mates.`, and `nebians.consica.com.np`.

## Sound (`audio/score.py`, stereo 48 kHz, -14 LUFS)
Warm, soothing **F Major / D Minor** (`Fmaj9 / Dm11 / Bbmaj9 / C13sus4`). Acoustic felt-piano / Rhodes voicings, 5-voice detuned PolyBLEP analog pad, modal wooden marimba arpeggio, warm sub bass, soft felt kick + modal wooden clave rim + brushed pink-brown shaker, and dual-room stereo convolution reverb (`room` 0.42 s + `hall` 2.5 s).
100% modal & foley sound effects: state-continuous time-varying filter sweeps (`sweep` with carried filter state `zi` on $1/f^{1.65}$ pink-brown noise) for paper riffles and silk scene whooshes, damped free-bar modal wooden taps climbing the F-major pentatonic scale, delicate escapement watch ticks, tactile double-transient UI button press/release, and a warm `Fmaj9` felt-piano confirmation arpeggio and resolve chord.

## Where it lives & source of truth
- **Repo:** private repo `NikitHamal/Video`, `neb/tools/video/books-launch/`.
- **Source of truth for numbers and pictures:** this repo (`NikitHamal/NEB`). `tools/publish/manifest.json` (counts, pages), `tools/publish/covers/*.jpg`, and the 19 featured PDFs in `notes/pdf/`, `ioe/pdfs/`, `bca/entrance/pdfs/`, and `bca/course/semester-3/pdfs/` (`scripts/pages.py <NEB checkout>` picks and renders `opener`, `worked`, `figure`, `practice`, plus `contents` only for `phy12`).

## Rules the film follows (same as the product)
Poppins, M3X blue/navy/sky/paper, flat fills only, no shadows, no gradients, no emoji, no live badge, no strokes on frames, no sharp-corner morphs, no zoom-in on book pages, Table of Contents shown only once (`phy12`), and the official 4-facet NEBians `N` logo at the end.

## Security note
The GitHub PAT and the molab token were provided in chat (used via an out-of-repo `/tmp` askpass helper and token file that were never committed). Rotate the PAT, and treat the molab notebook token as burned once the box is released.

## Deliverables (Video repo `main`)
- **v1 recovery + v2 preservation:** commit `281dbd96` (`nebians-books-v1-Film9x16.mp4`, `nebians-books-v1-Film16x9.mp4`, `nebians-books-v2-Film9x16.mp4`, `nebians-books-v2-Film16x9.mp4`).
- **v3 source & audio overhaul:** commits `97bf6559` and `e428c5cb`.
- **v3 final renders (46.0 s, 60 fps motion blur, H.264 + AAC, -14 LUFS):**
  * `nebians-books-v3-Film9x16.mp4` (1080x1920, 49,232,280 bytes, sha256 `4d3b67e57df1b783b2147a30a1ca0ee8a0082b672cc3becef65aa898d753f61a`, commit `d638212f`)
  * `nebians-books-v3-Film16x9.mp4` (1920x1080, 42,784,172 bytes, sha256 `3ab6bc29e4e80574c06aea214f61c706b6f247cfe5ed23a3fbe0ba3565663ff0`, commit `80ee4d8d`)
- Visual checks completed on 24-frame still contact sheets (`v3_9x16_b.jpg`, `v3_16x9_b.jpg`) and final encode contact sheets (`fin_v3_9x16.jpg`, `fin_v3_16x9.jpg`).
