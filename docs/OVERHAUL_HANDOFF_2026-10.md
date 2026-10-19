# Overhaul handoff — October 2026

Each agent appends its own section.

## Agent BIO — hands-on biology practicals

**What exists.** `backend_python/web/static/web/js/interactive/core/bio-handson/` is a framework for
procedure-driven, hands-on biology labs. `bio3d-runtime.js` checks `bio-handson/index.js`
(`hasHandsOn(slug)`) and hands those lessons to `runtime.js`; every other NEB biology lesson still
uses the old parametric viewer.

- `runtime.js` — engine + school lab room, camera rig, tool rig, steps, score, mistakes, hints,
  result card. A practical module exports `create(ctx)` → `{ tools, steps, update, result, dispose }`.
  A step: `{ title, text, hint, tool, shot, autoTool, hideBelt, enter, update, exit, skip, aim,
  handler: { down, move, up, hover, tap } }`. `ctx.next(msg)`, `ctx.mistake(msg, penalty)`,
  `ctx.requireTool(id)`, `ctx.progress(0..1)`, `ctx.skipTo(i)` (uses each step's `skip()`; tests use it).
- `input.js` (camera shots with `fit`/`fitH`, lean/pinch; pointer input), `tools.js` (held
  instruments), `cut.js` (guided incisions, screen-space tolerant), `labelquiz.js`, `lens.js`
  (render-to-texture hand lens), `fx.js`, `sound.js` (synth, muted by default), `ui.js` (card,
  belt, toast, dock checklist, choosers, result), `kit.js`.
- Microscope: `microscope.js` (3D instrument), `eyepiece.js` (focus with true depth of field,
  objectives, diaphragm, panning, taps, action buttons), `slideprep.js` (drop, coverslip with
  bubbles, blot, slide to stage, `createScopeView`). Fields in micrometres in `fields/`
  (onion squash, epidermis/plasmolysis, stem/root sections, blood, epithelium, muscle, frog embryos, letter e).
- Practicals (24 lessons): earthworm dissection; onion root tip ×2; flower families; plasmolysis;
  stomata; T.S. stem/root; animal tissues; plant tissues; grasshopper mitosis; frog development;
  microscope parts; starch, protein, urine, amylase, blood sugar; potato osmometer; imbibition.

**Testing.** Playwright drivers used: `/tmp/bio/drive2.py` pattern — wait for `#sim-stage.__bh`
(the runtime ctx), set `window.__bhTimeScale = 3`, then `BH().skipTo(n)`; practicals expose
`ctx.debug` for positions. SwiftShader runs at ~3–9 fps, so wait on `!BH().rig.moving`.

**Left to do.** Still on the old viewer: herbarium, mushroom, inflorescence, soil culture, pond (×2),
quadrats (×2), soil analysis, vegetation/animal specimen ID, fossils, conservation, transpiration,
respiration, anaerobic respiration, phototropism, apical bud, suction, Mendelian seeds,
biofertilizer, skeleton (×2), cockroach. The frog/rabbit options of the alimentary canal lesson
are not hands-on (earthworm only). Ideas: cockroach with hand lens + label quiz; Mendel seed
sorting; transpiration with a potometer bubble timed by a stopwatch.

**Tooling note.** `git fetch` has no credentials here, so after the first API push the base check
in `/workspace/tools/ghpush.py` failed for everyone. I added a small, backward-compatible fallback:
`/workspace/tools/.pushed.json` remembers which local commit the remote head mirrors.

## Hands-on physics and chemistry practicals (Oct 19, 2026)

**Where.** `backend_python/web/static/web/js/interactive/core/handson/`. `real-lab-3d.js` checks
`handson/index.js` (`hasHandsOn(slug)`) and hands those lessons to the biology agent's runtime
(`bio-handson/runtime.js`, which now builds the room for `config.subject`). Everything else in the
NEB physics/chemistry course still runs on the slider labs (`lab3d-*.js`). `opts.freeLab` skips
the hands-on version if a free mode is ever wanted.

**Done (9 slugs):** `acid-base-titration`, `redox-titration-kmno4` (both `practicals/titration.js`,
mode chosen by slug), `flame-tests`, `simple-pendulum-g`, `vernier-calipers`, `screw-gauge`,
`meter-bridge`, `anion-tests`, `resonance-air-column`.

**Shared modules.**
- `glass.js`: conical flask (liquid re-turned from the flask's own inner profile, so level follows
  volume), 50 mL burette (0 at top, printed 0.1 mL scale, concave meniscus), bulb pipette, drops,
  funnel, beaker, white tile. `reading.js`: the drag-a-hairline meniscus reader.
- `chem-model.js`: acid-base flask (pH from charge balance, indicator colour via Beer–Lambert, an
  unmixed "plume" that swirling folds in) and the redox flask (1:5, permanganate excess colour).
- `flame.js` + `burner.js`: shader flames; flame-test colours from emission lines → RGB (cobalt
  glass filters per line; `drawSpectrum` for the hand spectroscope). `wet-tests.js`: anion test
  rules (order of addition matters).
- `circuit.js`: binding posts, sagging leads, centre-zero galvanometer, plug resistance box, plug
  key, cell, and a Gaussian-elimination `solve()` for nodal analysis.
- `caliper.js`, `micrometer.js`: true-size instruments with pixel-accurate scales (the thimble
  texture compensates its anisotropic pixels; numbers count down past the datum).
- `hud.js` (action bar, chips pinned to 3D points, `hits()`/`screenDist()` with touch slack),
  `stopwatch.js` (reflex stopwatch, least-squares graph panel). CSS: `css/pages/interactive/14-handson.css`.
- Sounds: `bio-handson/sound.js` now exports `tone`, `noise` and `sfx.register(name, fn)`.

**Conventions.** World units are 10 cm; `world` sits at bench height `BY = 0.8`, so camera shots
(scene coordinates) add `BY` to y — every practical has a `shot()` helper for that. Each
practical sets `ctx.debug` for tests.

**Testing.** Static harness: `/workspace/harness/lab.html` (served on :8765, `static/` symlinked to
the web static dir). `drive.py sim lesson outprefix "n|js:...|w2000|sNAME"` skips to step n,
runs JS, waits, screenshots (SwiftShader, slow). Kill other memory hogs before Gradle builds.

**Next practicals, in order of value.** Ohm's law (circuit.js + rheostat), sonometer (WebAudio like
resonance.js), potentiometer, specific heat (thermometer + stopwatch), focal length (optics bench:
move screen to sharpen), prism (spectrometer), separation, gas preparation, electrolysis
(Faraday: weigh cathode), pH, functional groups (reuse wet-tests pattern), heat of
neutralisation, Lassaigne, water of crystallisation, salt analysis (anion-tests + flame-tests).

## Web landing (Oct 19, 2026)

`templates/landing/landing.html`, `static/web/css/landing.css`, `static/web/js/landing.js`.
Pixel-key buttons (stepped 8-bit clip-path face over an edge layer, `.lp-btn > span` is the
face; variants `-cream`, `-dark`, `-soft`, `-sm`), a floating glass topbar (`.is-solid` compact,
`.lp-ind` sliding pill with scroll-spy, `--sp` scroll progress hairline, `.is-menu` inversion),
circle-reveal mobile menu with focus trap, pixel Neby (`neby-pixel.js`) standing on the "B" of the
wordmark (`.lp-word .lp-neby`, em-sized) with a speech bubble, and a peeking Neby in the topbar.
Run locally: `DB_ENGINE=sqlite DEBUG=True python manage.py runserver` (restart it to see template
edits; the cached loader holds them).

## Android: PDF reader and chat (Oct 19, 2026)

See `ANDROID_UI_CONTINUITY.md` §13.

## Tooling for agents in this sandbox

- Push: there are no git credentials. `/workspace/tools/commit_push.sh "msg" paths...` commits only
  those paths and mirrors the commit to GitHub through the Git Data API (`ghpush.py`, with the
  `.pushed.json` state file because `git fetch` cannot authenticate).
- Android build: JDK 17 + SDK in `/workspace/tools`; the sandbox proxy needs the mitmproxy CA in
  the JDK truststore and proxy flags for sdkmanager/Gradle (`~/.gradle/gradle.properties`).
  `/workspace/tools/build_android.sh :app:compileModernDebugKotlin`. With 8 GB RAM, kill stale
  Kotlin daemons before assembling; use `-Pkotlin.compiler.execution.strategy=in-process`.
- CI artifact uploads were failing on "Artifact storage quota has been hit" (account-wide). A
  side-by-side preview APK (`com.neb.ians.preview`) can be built locally with the init script
  `/workspace/tools/preview-release.gradle` and a throwaway keystore at the gitignored
  `nebians-release.keystore` path.
