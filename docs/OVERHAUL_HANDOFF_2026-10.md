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

**Done (15 slugs):** `acid-base-titration`, `redox-titration-kmno4` (both `practicals/titration.js`,
mode chosen by slug), `flame-tests`, `simple-pendulum-g`, `vernier-calipers`, `screw-gauge`,
`meter-bridge`, `anion-tests`, `resonance-air-column`, `ohms-law-resistivity`, `hookes-law-spring`,
`focal-length-mirror-lens` (convex lens), `sonometer-laws` (law of length), `potentiometer-emf`,
`electrolysis-cuso4`.

**Shared modules.**
- `glass.js`: conical flask (liquid re-turned from the flask's own inner profile, so level follows
  volume), 50 mL burette (0 at top, printed 0.1 mL scale, concave meniscus), bulb pipette, drops,
  funnel, beaker, white tile. `reading.js`: the drag-a-hairline meniscus reader.
- `chem-model.js`: acid-base flask (pH from charge balance, indicator colour via Beer–Lambert, an
  unmixed "plume" that swirling folds in) and the redox flask (1:5, permanganate excess colour).
- `flame.js` + `burner.js`: shader flames; flame-test colours from emission lines → RGB (cobalt
  glass filters per line; `drawSpectrum` for the hand spectroscope). `wet-tests.js`: anion test
  rules (order of addition matters).
- `circuit.js`: binding posts, sagging leads, centre-zero galvanometer, `dialMeter` (ammeter /
  voltmeter), slide-wire `rheostat`, plug resistance box, plug key, cell, and a Gaussian-elimination `solve()` for nodal analysis.
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

**Next practicals, in order of value.** specific heat (thermometer + stopwatch), focal length (optics bench:
move screen to sharpen), prism (spectrometer), separation, gas preparation, pH, functional groups (reuse wet-tests pattern), heat of
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


## Android native simulations (Oct 19, 2026)

`app/.../ui/sim/`: `NativeSims` maps `courseSlug/lessonSlug` to a native sim;
`InteractiveLessonScreen` hands those lessons to `NativeLessonScreen` (sim + lesson text + quiz from
`getInteractiveLessonDetail`), everything else stays in the WebView. `gl/` is a dependency-free
OpenGL ES 3 renderer (`GlMesh` lathe/sphere/cylinder/box/torus, `GlScene`/`GlNode`/`OrbitCamera`,
`GlRenderer` PBR shader + backdrop + floor + blob shadows, `GlStage` Compose wrapper with touch:
orbit, pinch, `GlSim.pointerDown` ray picking). Shaders are GLSL ES 3.00 and were validated with
WebGL2. Native so far: pendulum lab, molecule gallery, Earth-Moon-Sun (3D); projectile motion,
waves, concave mirror (2D Canvas). To add one: write a `GlSim` (or a Canvas composable) plus its
Compose controls (`SimKit.kt`), and map its lesson in `NativeSims`.

**Owner preferences (also in workspace memory):** library PDFs are read only inside the app (no
share/open-with/copy-text); do not build Android locally in the sandbox — push and let CI build.

## Biology hands-on input (Oct 19, 2026)

Tool tips follow the pointer exactly (`bio-handson/tools.js` lifts along the view ray; stiff
spring), `runtime.aimDefault` aims at the object under the pointer, a DOM reticle marks the action
point and the cursor hides while a tool is held, and `input.pick` has a fuzzy second pass (eight
offset rays). Flower dissection: tap-to-pluck, 20 px tug, forgiving box drops.

## Sounds and themes (Oct 19, 2026)

- `static/web/audio/sfx/`: 26 CC0 Kenney samples (licence file alongside). `bio-handson/sound.js`
  maps events to samples (`SAMPLES`), loads them only once sound is turned on, varies pitch, and
  falls back to the synth until loaded.
- Android read the theme from a 404 path (`site-theme/`); it is `api/site-theme/`. `NebyDress`
  makes every Neby sprite wear the server's look; the API sends the festival `greet` state.
- The landing `<html>` carries `data-neby-look`/`data-neby-greet` like `base.html`. The Play
  Store banner in `base.html` was removed at the owner's request.
- Pushing large files: `ghpush.py` calls the actl `ApiClient` from Python (run with
  `/app/py/.venv/bin/python`) because a CLI argument is limited to 128 KB.

## PHYCHEM pass 2: fifteen more hands-on physics and chemistry practicals (Oct 19, 2026)

**Done (15 slugs, all registered in `core/handson/index.js`, 30 hands-on phy/chem lessons in total):**

| Slug | File | What the student does |
|---|---|---|
| `spherometer` | `practicals/spherometer.js` (+ `spherometer.js` instrument) | turn the disc through one revolution for the least count; prick the legs on paper and read l with a rule; turn the screw on plane glass and on a watch glass until the tip meets its reflection (tip close-up, rock test); tap the pitch scale and rim graduations; R = l²/6h + h/2 |
| `parallelogram-of-forces` | `practicals/parallelogram.js` | load hangers; the knot settles from summed forces with pulley friction; drag it away and release; dot the threads; construct the parallelogram to scale on a drawing sheet (`drawsheet.js`) from the student's own dots |
| `coefficient-of-friction` | `practicals/friction.js` | lift a hinged plank by hand until the block slips (per-trial μ scatter, lifting too fast caught), read the quadrant; then pull with a spring balance with a max marker (stick-slip physics), three loads, F–N slope |
| `specific-heat-mixtures` | `practicals/specific-heat.js` | tare/weigh, hold to pour water, steam heater over a burner (metal needs minutes to reach θ₂), carry it across (cools in air), stir, catch the peak; heat exchange integrated |
| `galvanometer-figure-of-merit` | `practicals/galvanometer.js` | pull plugs on a high-resistance box (closing the key at low R slams the needle), tap the dial; k = E/((R+G)θ) and 1/θ–R graph |
| `prism-minimum-deviation` | `practicals/prism.js` | drag P1 to set i, look through the second face and swing P3/P4 to hide the images (Snell at both faces, TIR); D–i curve, Dm, n |
| `lab-apparatus-safety` | `practicals/apparatus-safety.js` | name ten pieces of apparatus, find the right one for jobs, light a Bunsen in the safe order, fix four hazards, acid into water |
| `separation-techniques` | `practicals/separation.js` (+ `separation-kit.js`) | fold filter paper and pour without overflowing; evaporate to the crystallisation point; sublimation; distillation (bulb at side arm, water in at the bottom); chromatography and Rf |
| `gas-preparation` | `practicals/gas-preparation.js` | H₂, O₂, CO₂ in one generator: right solid, liquid down the thistle funnel (stem must dip), collection method, let the air bubbles go, test |
| `water-of-crystallization` | `practicals/crystallization.js` | crucible on a balance, heat gently/strongly (CuO if overdone), desiccator, weigh to constant mass; x from the student's masses |
| `salt-analysis-scheme` | `practicals/salt-analysis.js` (+ `salt-chem.js`) | appearance, dry heating, flame; NH₄⁺; group reagents in order with real out-of-order traps; confirmatory tests; anion tests (`wet-tests.js`); name the salt |
| `ph-and-indicators` | `practicals/ph.js` | litmus and universal indicator on a spot tile (pH from Ka/Kb), calibrate a pH meter (7 then 4, rinse), buffer vs water with live graph |
| `organic-functional-groups` | `practicals/organic.js` | four unknowns × Na, NaHCO₃, FeCl₃, Br₂ water, Tollens', Fehling's, 2,4-DNP, ester test (warm in the water bath) |
| `heat-of-neutralization` | `practicals/neutralization.js` | measuring cylinder by hold-to-pour + dropper, tap-read meniscus, rinse, two temperatures, pour/lid/stir with live T–t graph, ΔH = −mcΔT/n; repeat with ethanoic acid |
| `lassaigne-test` | `practicals/lassaigne.js` | sodium fusion held in the flame until red (glow follows temperature, short fusion = weak extract), plunge, then N/S/halogen tests whose order matters (HCN, AgCN/Ag₂S traps) |

**New shared modules (core/handson/):** `thermo.js` (tap-read thermometer + `thermoReader`, copper calorimeter, foam cup, top-pan balance with TARE and settling display, steam puffs), `vessels.js` (100 mL measuring cylinder with tap reader, `createPour` that lands a vessel's lip on a target), `tube-bench.js` (rack, labelled bottles with chips, `showOnly`, drops, tube looks: ppt/mirror/layer/ring/fizz, flame or water bath), `drawsheet.js` (2D construction sheet with constrained handles), `salt-chem.js`, `separation-kit.js`, `spherometer.js`. Small additions: `stopwatch.js` graphs take `yMin`, per-point colours and expose `el`; `hud.js` chips hide when their point is off screen; `index.js` re-frames the opening shot once a phone stage has settled its size. CSS in `14-handson.css`: `.ho-tight` action bars, `.ho-sheet`, `.ho-graph.ho-side`, `.ho-tag`.

**Testing.** Each was driven with Playwright at 1400×900 and 390×844 (`/tmp/pc/drive.py`: adds `dj:` JS-computed mouse drags and `c:` clicks to the harness driver) with at least one real mouse interaction (disc turned, knot dragged, plank lifted, balance tared, bottles tapped, pours held, fusion held in the flame…), and every one skips through to its result card without console errors. Note: in a `drive.py` token, `|` splits tokens, so avoid `||` in inline JS.

**Not done / ideas.** Sound effects for the new practicals are synth (`sfx.register`: hiss, pop, whoof, drip). The flame test in salt analysis uses the burner's emission tint without a wire loop. Possible polish: spherometer second set of readings at another spot, gas preparation tests done with the jar lifted out of the trough.

## BIO pass 2: the remaining 24 biology practicals made hands-on (Oct 19, 2026)

All 24 lessons below are registered in `core/bio-handson/index.js` (43 hands-on biology lessons
in total). Every practical uses the existing runtime (steps, teacher toasts, score, mistakes,
result card with error vs truth where there is a true value) and was driven with Playwright at
1400×900 and 390×844 (`/tmp/bio2/drive.py`: adds `dj:` JS-computed mouse drags/taps and `hj:` press-and-hold), with
at least one real mouse interaction each, and skipped through to its result card with no console
errors (`/tmp/bio2/smoke.py`).

| Slug(s) | File | What the student does |
|---|---|---|
| `transpiration-upper-lower-rate` | `practicals/transpiration.js` | dry cobalt chloride papers over a spirit lamp (hold; scorching caught), forceps them onto both leaf faces, clamp with slides, stopwatch; tap each paper when fully pink (early taps caught); repeat on maize; ratio from own times |
| `respiration-rate-germinating-seeds` | `practicals/respirometer.js` | KOH by dropper, gauze, weigh 10 g germinating/boiled seeds, bungs + capillaries, equilibrate, eosin index; tap the mm scale at the drop every 2 min; graph, slope, µL O₂ g⁻¹ min⁻¹ |
| `anaerobic-respiration-setup` | `practicals/anaerobic.js` | boil glucose on a Bunsen, cool in a trough watching the thermometer, yeast at ~35 °C (too hot kills it), paraffin seal, delivery tubes to lime water, test vs boiled-yeast control, 1 h time-lapse, smell, equation |
| `phototropism-setup`, `apical-bud-removal-setup` | `practicals/tropism.js` | foil caps, box with slit turned to a lamp, 4-day bending, drag a protractor; snip apices, brush plain or IAA lanolin, 14-day lateral growth, measure laterals |
| `suction-due-transpiration-setup` | `practicals/suction.js` | fill tube, cut twig under water (cut in air = embolism), rubber + vaseline, mercury beaker, read the column every 15 min, lamp and fan |
| `mendelian-inheritance-seeds` | `practicals/mendel.js` | sort F₂ seeds into dishes by tapping (random Mendelian samples), χ² vs 3:1 and 9:3:3:1 from own counts, drag-in Punnett square |
| `quadrat-density-plant`, `quadrat-frequency-field` | `practicals/quadrat.js` + `specimens/field.js` | outdoor 6 × 6 m plot (instanced plants), flick the quadrat, tap every plant rooted inside, density / frequency / abundance, Raunkiaer class, Whitford A/F |
| `cockroach-external-morphology` | `practicals/cockroach.js` + `specimens/cockroach.js` | chloroform jar, tray, lens regions, spread tegmen and hind wing with forceps, label quiz, sex from the tail, flip and remove mouthparts in order |
| `human-skeleton-joints`, `skeleton-joints-health-disorders` | `practicals/skeleton.js` + `specimens/skeleton.js` | full-size articulated skeleton; drag loose bones into place, classify 9 joints, flex elbow / circumduct shoulder / turn head; disorder case cards (tap the site, name, care), healthy vs arthritic knee ROM on a goniometer |
| `soil-microorganism-culture` | `practicals/culture.js` + `specimens/microbe.js` | lamp, 10⁻¹…10⁻⁴ dilution, pour agar, 0.1 mL plating, alcohol + flame the spreader, 48 h colonies painted on the agar, choose the 30–300 plate, dot colonies with a marker, colony types, CFU/g |
| `biofertilizer-preparation` | `practicals/biofert.js` | uproot pea, wash, pick pink nodules, HgCl₂ + 5 rinses, crush, flame loop and streak YEMA–Congo red, 5 days, broth, hold-pour to 40 % carrier moisture, jaggery seed coating, shade drying |
| `soil-analysis-sites` | `practicals/soil.js` | two sites: fresh/dry weighing to constant mass, WHC funnels read at the meniscus, pH paper vs chart, jar-test layers measured and classified, H₂O₂ humus |
| `pond-ecosystem-botany`, `pond-ecosystem-zoology` | `practicals/pond.js` + `specimens/pondscene.js` + `fields/pond.js` | outdoor pond; thermometer, pH paper, Secchi disc down/up, DO meter (zoology), plankton net, classify plants by habit / animals by diet; back in the lab a living plankton field under the microscope; food chain / web by dragging |
| `mushroom-identification` | `practicals/mushroom.js` | Agaricus vs Amanita: lens on every part, label quiz, cut caps, spore prints on black/white paper overnight, danger signs, formalin |
| `inflorescence-identification` | `practicals/inflorescence.js` + `specimens/inflor.js` | six specimens whose flowers carry ages; tap the oldest, racemose/cymose, name the type |
| `fossil-evolution-evidence` | `practicals/fossil.js` | trilobite, Devonian fish, Glossopteris, saligram ammonite, Archaeopteryx; lens, name, drop into periods of the time scale, conclusions |
| `biodiversity-conservation-nepal` | `practicals/conservation.js` | raised relief map of Nepal with park pins; drag species to parks, in-situ/ex-situ sort, threats → remedies, census % increase |
| `vegetation-specimen-identification`, `animal-specimen-identification` | `practicals/specimen-id.js` + `specimens/vegkey.js`, `specimens/animkey.js` | 6 of 12 specimens per run on a turntable (slides with micrographs for micro-organisms); dichotomous key couplet by couplet, wrong leads explained |
| `plant-collection-herbarium` | `practicals/herbarium.js` | snip a flowering twig, blotters and press, flatten leaves and flip one, a week of drying with blotter changes (mould if skipped), HgCl₂, gummed strips, label |

**New shared modules.** `bench.js` (time-lapse clock in min/h/days, `ask` until right, notebook
`sheet`, `chipDrop` drag-or-tap-tap chips into `[data-slot]`s, sprite `tag`, glass beaker, clay pot,
crucible, enamel tray, `outdoors()` which hides the lab furniture and opens the sky, `mergeGeos` for
vertex-coloured composites), `specimens/plants.js` (alpha-cut grid leaves that bend smoothly, swept
stems, flowers, buds, bendable seedlings). New held tools in `tools.js`/`ui.js`/`icons.js`:
inoculating loop, glass spreader, marker pen. `sound.js`: paper, latch and door samples (CC0 Kenney).
CSS (in `08-biology.css`): `.bh-sheet` (+ `.wide`, `.left`), `.bh-dchip`, `.bh-slot`, `.bh-tab`,
`.bh-key`, `.bh-tally`, `.bh-jdot`/`.bh-jlayer`, `.bh-park`, `.bh-key-mwrap`, `.bh-under-clock`.

**Notes for whoever continues.** A step's `skip()` must never call `ctx.next()` (it re-enters the
step during `skipTo` and leaks overlays). Objects at the bottom centre of a shot sit under the tool
belt and cannot be tapped — use `hideBelt` or frame them higher. Practicals that seed randomness
from time accept `window.__bhSeed` in `specimen-id.js` for repeatable tests. Graphs (`createGraph`)
are hidden on phones where they would cover the apparatus.

**Not done / ideas.** Quadrat and seed sorting offer a "partner" shortcut after enough hand counting
(the counts stay real). The pond and soil labs use colour-chart pH (no meter). Possible polish: more
specimen variety per run, a Secchi disc reading from a boat, and a monochasial cyme specimen.
