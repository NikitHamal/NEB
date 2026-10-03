# NEBians launch film: pipeline

Deterministic motion-graphics pipeline for the 15-second NEBians launch film. Headless Chrome renders an HTML/JS stage frame by frame, ffmpeg encodes it, a small synthesiser scores it. **No npm dependencies.** The maintenance guide (storyboard, spec reference, what to do when the site changes) is [`docs/LAUNCH_VIDEO.md`](../../docs/LAUNCH_VIDEO.md).

```bash
cd tools/video
node cli.mjs doctor            # check everything
node cli.mjs drift             # is the film still true?
node cli.mjs all --draft       # quick preview with sound -> out/
node cli.mjs all               # final render -> dist/
```

Needs Node 22+, ffmpeg/ffprobe (libx264, aac) and Chrome or Chromium. `CHROME_PATH` overrides discovery; `CHROME_SANDBOX=1` keeps Chrome's sandbox on.

## Commands

| Command | Does | Useful flags |
| --- | --- | --- |
| `doctor` | Checks Node, ffmpeg, Chrome, spec, fonts, icons, scenes, captures | |
| `sync` | Reads brand tokens and copy from the repo into `spec/facts.generated.json` | `--write` rewrites sourced palette values in the spec |
| `drift` | Compares spec with repo and live site; exits 1 on drift | `--offline`, `--base <url>` |
| `icons` | Rebuilds the Material Symbols subset from `spec.icons` | |
| `capture` | Screenshots live pages into `assets/captures` | `--only <id>`, `--base <url>` |
| `still` | Single frames to `out/stills/` | `--t 0,1.5`, `--beats 4,8`, `--scene <id> --count 8`, `--aspect`, `--scale` |
| `contact` | Labelled contact sheet `out/contact-sheet.png` | same as `still`, plus `--cols`, `--width`, `--count` |
| `render` | Video track only (`out/video-*.mp4`) | `--draft`, `--aspect`, `--fps`, `--samples`, `--shutter`, `--workers`, `--scale`, `--from`, `--to`, `--grain`, `--crf`, `--preset`, `--out` |
| `audio` | Synthesises and normalises `out/audio.wav` (+ `audio-analysis.png`) | `--track <wav>` to use your own music |
| `mux` | Video + audio -> `dist/nebians-launch-<aspect>.mp4` + poster | `--draft`, `--aspect`, `--out` |
| `qa` | Verifies the deliverable, writes report and contact sheet | `--draft`, `--aspect`, `--file` |
| `all` | `doctor`, `render`, `audio`, `mux`, `qa` in order | any flag above, for example `--draft` |

`npm test` (or `node --test "test/*.test.mjs"`) runs the unit tests.

## Layout

```
cli.mjs                 command router
lib/                    cdp.mjs (Chrome DevTools client), chrome.mjs, server.mjs, session.mjs, ffmpeg.mjs, spec.mjs, args.mjs, paths.mjs
pipeline/               one file per command (render, audio, mux, qa, capture, sync, drift, doctor, icons, stills, all) + facts.mjs
stage/                  the film itself: index.html, main.js, stage.css
  engine/               math, ease, tl, rng, noise, color, dom, text, ui, fx, bg, ambient, burst, hills, chrome, transition, logo, stage
  scenes/               hook, logo, materials, mates, smarter, end + index.js registry
audio/                  dsp.mjs, instruments.mjs, score.mjs
spec/launch.spec.json   single source of truth; facts.generated.json is written by sync
assets/                 fonts (Poppins + icon subset), captures (live-site screenshots + manifest.json)
test/                   node:test suites
dist/                   committed deliverables (last known-good render)
out/                    scratch (git-ignored)
```
