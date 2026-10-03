# NEBians launch film

A 15-second motion-graphics film for the NEBians launch, built as code. Every frame is computed from a timeline, rendered by headless Chrome, encoded by ffmpeg and scored by a small synthesiser, so **any agent can change the film by editing a spec and re-running one command**. Nothing is edited by hand in a video editor and the pipeline has **zero npm dependencies**.

Everything lives in `tools/video/`. This document is the maintenance guide; `tools/video/README.md` is the CLI reference.

## Deliverables

| File | What it is |
| --- | --- |
| `tools/video/dist/nebians-launch-16x9.mp4` | Master. 1920x1080, 60 fps, H.264 + AAC, 15.000 s, -14 LUFS |
| `tools/video/dist/nebians-launch-16x9-poster.png` | Poster frame (the end card) |
| `tools/video/dist/nebians-launch-16x9-contact.png` | 12-frame contact sheet of the master |
| `tools/video/dist/qa-report-16x9.json` | Machine-readable QA result for the master |

`dist/` holds the last known-good render and is committed. `tools/video/out/` is scratch (git-ignored).

## The 60-second orientation

```bash
cd tools/video            # every command below is relative to this folder
node cli.mjs doctor       # toolchain, spec, fonts, icons, scenes, captures
node cli.mjs drift        # is the film still TRUE against the repo and the live site?
#  ...edit spec/launch.spec.json and/or stage/scenes/*.js ...
node cli.mjs contact --count 12    # look at the film as a contact sheet (out/contact-sheet.png)
node cli.mjs all --draft  # ~3 minute preview with sound in out/
node cli.mjs all          # final render into dist/ (about 20 minutes on 2 vCPUs)
```

Requirements: Node 22+, ffmpeg + ffprobe (with libx264 and aac), Google Chrome or Chromium. Set `CHROME_PATH` if Chrome is not on the PATH. Set `CHROME_SANDBOX=1` to keep Chrome's sandbox on (it is off by default because containers usually cannot run it).

## How it works

```
                      spec/launch.spec.json  <-- single source of truth (copy, timing, colours, cues)
                               |
   NEBians repo ---- sync ---> +--> stage/ (HTML + JS scenes, a pure function of time t)
   (CSS tokens, hero,          |          |
    nav, logo SVG,             |          |  window.__seek(t)  ->  Chrome screenshot  ->  PNG
    blobatar.js,               |          v
    neb-art.js)                |    render.mjs: N sub-frame samples per output frame
   live site --- capture ----> +          |
   (library screenshot)                   v
                                    ffmpeg: tmix (motion blur) -> bt709 -> x264 -> video.mp4
   cues in the spec ---------> audio/score.mjs -> WAV -> loudnorm -> AAC  ----+
                                                                                v
                                                     mux -> dist/*.mp4 + poster ; qa -> report + contact sheet
```

Design rules that make this reliable:

1. **Every frame is a pure function of time.** `window.__seek(t)` sets every element from `t`. There are no CSS animations, no `Date.now()`, no `Math.random()` (use `engine/rng.js`), no video elements. That is why renders are reproducible and can be split across workers.
2. **Real motion blur.** Each output frame is the average of 3 renders spread across a 180-degree shutter (`tmix` in ffmpeg), not a fake blur filter.
3. **The film reuses the product's own code.** Avatars are drawn by `backend_python/web/static/web/js/blobatar.js`, the library card banners by `neb-art.js`, the logo by `img/n-logo-master.svg`, and the library screen is a real capture of the live site. When those change, the film changes on the next render.
4. **One timeline, two clients.** The `cues` list in the spec drives both the visual reactions (flash, shake, chromatic split, beat pulse) and the sound effects, so picture and sound cannot drift apart.
5. **The film checks itself against the site.** `drift` compares the spec with the repo and probes the live site for every claim the film makes.

## The film (128 BPM, 32 beats, 8 bars, 0.46875 s per beat)

The concept is the site's own hero device, "Study **materials**. Study **mates**.", extended with a third line and bracketed by the brand blue.

| Beats | Seconds | Scene id | What happens |
| --- | --- | --- | --- |
| 0-4 | 0.00-1.88 | `hook` | Four full-bleed words slam on the beat: Notes. Papers. Books. Answers. The stack implodes into a dot. |
| 4-8 | 1.88-3.75 | `logo` | Flash and shockwave. The real logo's five facets fly in and lock, the wordmark slides out, the tagline types up, the lockup flies into the header. |
| 8-14 | 3.75-6.56 | `materials` | "Study [materials]." A browser frame scrolls the real library page while library cards (real NebArt banners) float around it. |
| 14-20 | 6.56-9.38 | `mates` | "Study [mates]." A forum thread types itself out among live-avatar faces (real blobatars). |
| 20-27 | 9.38-12.66 | `smarter` | "Study [smarter]." Neby AI helper answers a question while four tool tiles pop in. |
| 27-32 | 12.66-15.00 | `end` | Blue circle wipe, Himalayan ridgelines rise, app-icon tile, "Live now.", URL, "Free on the web. Android app on Google Play." |

The persistent header (`engine/chrome.js`) mirrors the real site header: the nav pill highlights Library, then Forum, then swaps to the subject-page tabs with "Neby AI helper" active.

Reserved sync points: the drop lands on beat 4 (1.875 s), the last chord on beat 28 (13.125 s), and the film ends on beat 32 (15.000 s).

### What is real and what is illustrative

Real: brand colours (read from the site CSS), logo, hero wording and chips, nav labels, the Library screenshot, the banner art, avatars, tool names, category names, and the Google Play availability.
Illustrative: resource titles on the floating cards, the forum thread and its names (Aarav, Sita, Bikash, ...), and the Neby AI exchange. Nothing in them is a claim about a specific real file or person. The library capture has real uploaders' avatars and names **blurred at capture time**.

## The spec: `spec/launch.spec.json`

| Key | Meaning |
| --- | --- |
| `meta` | `duration` (s), `fps`, `bpm`, `beatsPerBar`, `poster` (s), `aspects`. Duration x BPM must equal the timeline length in beats (validated). |
| `brand` | `name`, `url`, `tagline`, `subline`. The URL is also the base for `capture` and `drift`. |
| `palette` | Named colours. An entry with a `source` (`file` + `token`, or `file` + `rule` + `prop`) is checked by `drift` and rewritten by `sync --write`. Entries without a source are creative choices. |
| `timeline` | Ordered scenes in **beats**: `{ id, from, to }`. Must be contiguous and end at the last beat. The `id` selects an implementation in `stage/scenes/index.js`. |
| `background` | Keyframed gradient-mesh colours by beat (six blobs each). A colour blend starts one beat before each key. |
| `chrome` | Header: nav labels, subject tabs, CTA text, and which item is active from which beat. |
| `scenes` | Per-scene copy and data, keyed by scene id (words, chips, cards, thread, AI exchange, tool tiles, end card). |
| `cues` | The sync bus: `{ beat, kind, beats? }`. Kinds: `hit boom riser whoosh pop tick type swell sparkle chord sting thud`. |
| `icons` | Material Symbols names. `icons` rebuilds the font subset from this list. |
| `captures` | Live-site screenshots to take (URL, viewport, blur/hide selectors). |
| `claims` | Statements the film makes about the live site, with the URL and text that must still be there. A claim with `"watch": true` reports when a feature that is NOT in the film goes live. |

## Keeping the film true when NEBians changes

Run `node cli.mjs drift` first. It exits non-zero and says what to change. The mapping:

| You changed in NEBians | The film depends on | Do this |
| --- | --- | --- |
| Brand colours (`material3.css`, `pages/home/landing.css`) | `palette` entries with a `source` | `node cli.mjs sync --write`, then re-render |
| Hero headline, chips or their icons (`_home_hero.html`) | `scenes.materials`, `scenes.mates` (`lead`, `chip`, `icon`) | Edit those fields (run `icons` if the icon is new) |
| Header nav labels (`base.html`) | `chrome.nav` | Edit `chrome.nav` |
| Logo (`img/n-logo-master.svg`) | Read straight from the repo | Nothing, unless `drift` says the facet count is no longer 5. Then rework `FLY` in `stage/scenes/logo.js` |
| Library or blob-avatar or NebArt code | Read straight from the repo | Nothing. Re-render to pick it up |
| Library page redesigned | `captures.library` | `node cli.mjs capture`, inspect `assets/captures/library.jpg` for leaked names, re-render |
| A tool or category renamed, a page moved | `claims` | `drift` fails naming the claim. Update the tile or claim text |
| A new feature goes live (for example the marketplace at `/marketplace/`) | The `watch` claim flips | Add a beat: see "Add or replace a chapter" |
| Domain change | `brand.url` | Edit it. `capture` and `drift` follow it |
| App leaves or changes on Google Play | `brand.subline`, `claims` | Edit both |

Marketplace note: the creator marketplace is in the repo but returned 404 on the live site on 2026-09-29, so it is deliberately not in the film.

## Recipes

**Change words.** Edit `scenes.*` in the spec. Text is measured at build time, so long strings reflow on their own. Then `contact --scene <id>` to look.

**Change how long or how fast.** Keep `duration x bpm / 60` equal to the last `timeline.to`. Cue beats and scene beats scale with the BPM; sub-second animation timings inside scenes are in seconds and do not.

**Add or replace a chapter.**
1. Copy `stage/scenes/mates.js` to `stage/scenes/<name>.js` and adapt it. Use `applyPush` for the slide in and out.
2. Register it in `stage/scenes/index.js`.
3. Add it to `timeline` (keep it contiguous), add `scenes.<name>` copy, and a `background` key at its first beat.
4. Add a `chrome.active` entry if the header highlight should move.
5. Add `pop`, `whoosh` and `type` cues at the moments things land. `doctor` checks that every timeline id has an implementation and every icon exists.

**Add an icon.** Add the Material Symbols name to `icons`, run `node cli.mjs icons` (downloads a ~7 KB font subset from Google Fonts), then use it as `icon: "name"`.

**Change the music.** The bed is procedural (`audio/score.mjs`: chords per bar in `BARS`, instruments in `audio/instruments.mjs`). To use licensed music instead, drop a 15-second WAV in and run `node cli.mjs audio --track path/to/track.wav`. It is loudness-normalised to -14 LUFS the same way.

**Take a screenshot of a different page.** Add an entry to `captures` (`url`, `viewport`, `hide`, `redact`, `fullPage` or `selector`), run `capture --only <id>`, and read the image with `S.capture('<id>')` in a scene (see `stage/engine/ui.js` `browserFrame`).

**Other aspect ratios.** `9:16` and `1:1` are defined in `meta.aspects` and every scene has a portrait branch, but only 16:9 was designed, reviewed and shipped. Treat the others as a starting point and review them with `contact --aspect 9:16` before publishing.

## Rendering and performance

| Mode | Command | Output | Time on 2 vCPUs |
| --- | --- | --- | --- |
| Stills | `still --t 1.2,4.5` or `still --beats 4,8` | PNGs in `out/stills/` | seconds |
| Contact sheet | `contact --count 12`, `--scene mates`, `--beats 0,4,8` | `out/contact-sheet.png` with time labels | ~10 s |
| Draft | `render --draft` | 960x540, 30 fps, 1 sample | ~2.5 minutes |
| Final | `render` | 1920x1080, 60 fps, 3 samples, grain 1.5, CRF 15 | ~20 minutes |

Other flags: `--from/--to` (render a slice), `--samples`, `--shutter` (0.5 = 180 degrees), `--workers`, `--fps`, `--crf`, `--preset`, `--aspect`. Screenshots dominate the cost (about 0.2-0.5 s each at 1080p), not scene code.

## Sound

A four-layer procedural score at 128 BPM in C major / A minor: `Am | C | G | Am | F | C | G | C`. Kick, sidechain-ducked pad, bass and arpeggio, hats, claps, a bell motif, and FX. All FX come from `cues`. The mix uses a Freeverb-style reverb, a ping-pong delay, a tanh soft clip, a 0.35 s fade at the end, and two-pass `loudnorm` to -14 LUFS / -1.5 dBTP.

The score was checked by **measurement** (structure on a spectrogram, per-band and per-second levels, loudness, peak, no dead air) but **not auditioned by ear**. Listen before you publish, and swap in a licensed track with `audio --track` if you prefer.

`audio` also writes `out/audio-analysis.png` (spectrogram over waveform) so an agent without ears can still check the structure.

## QA and "done"

`node cli.mjs qa` verifies the muxed file: streams, duration within 50 ms of the spec, 1080p60, H.264 yuv420p tagged bt709, stereo 48 kHz, size under 25 MB, no black frames, no frozen picture, loudness near -14 LUFS, true peak under -1 dBFS, no dead air. It writes `dist/qa-report-16x9.json` and the contact sheet. Also run `npm test` in `tools/video` (57 tests: spec validation, easing, timing, encoder arguments, CSS token extraction, audio composition).

Done means: `drift` clean, `qa` green, and you have looked at the contact sheet.

## Rules for editing scenes

- Animate only through `update(lt, t)`; `lt` is seconds since the scene's first beat and may be negative during `pre` (the slide-in).
- Use `place(node, { x, y, s, rz, o })` from `engine/dom.js` (it skips redundant writes) and easings from `engine/ease.js`.
- Never measure layout inside `update`. Measure once in `build`.
- Toggle visibility with `show()`, and keep `pre`/`post` small: an invisible scene costs nothing.
- Do not reuse SVG gradient ids across instances (`engine/logo.js` namespaces them). A gradient defined inside a `display:none` subtree silently paints nothing.
- The repo rule applies: no code comments, files under about 500 lines, one responsibility per file.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `Chrome not found` | Set `CHROME_PATH`. |
| Chrome exits at start in a container | Leave `CHROME_SANDBOX` unset (default is `--no-sandbox`). |
| Stage fails to boot | The error lists the page's console errors. A missing scene, a bad icon name or a JSON typo is the usual cause. Run `doctor`. |
| An icon shows its name as text | It is not in the font subset. Add it to `icons`, run `icons`. |
| Library frame is a grey skeleton | No capture. Run `capture`. |
| A capture times out | The live site can take 10-25 s per page. Retry, or `capture --base http://localhost:8000` against a local server. |
| Colours look washed in players | The encode tags bt709; check `qa`'s colour line and do not re-encode without `-colorspace bt709`. |
| Banding in gradients | Increase `--grain` (default 1.5). |
| Everything is slow | Use `--draft`, `--from/--to`, `contact --scene`, and `--workers 1` on a loaded machine. |

## Credits and licences

- Poppins (SIL OFL 1.1, `tools/video/assets/fonts/OFL.txt`). It carries the Devanagari glyphs too.
- Material Symbols Outlined (Apache 2.0), subset downloaded from Google Fonts.
- NEBians logo, palette, `blobatar.js` and `neb-art.js` belong to the project and are read from the repo.
- Music and effects are synthesised by `tools/video/audio/`; no samples are used.

## Findings from production (2026-09-29)

- `https://nebians.consica.com.np/marketplace/` is 404 on the live site while the code exists in the repo (not deployed).
- `https://nebians.consica.com.np/past-papers/` renders the heading as `NEB Past Papers (Class 11 &amp; 12)`, a double-escaped ampersand in the page `<h1>`.
- The live pages are slow (10-25 s to first byte at times), so captures use generous timeouts.
