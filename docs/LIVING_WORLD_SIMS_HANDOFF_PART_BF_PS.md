# Living World sims — Butterfly life cycle & Photosynthesis (handoff)

Course `living-world`, lessons `become-a-butterfly` (sim `biology/butterfly-life-cycle`) and `plant-power` (sim `biology/photosynthesis`). Both were rebuilt from scratch as three.js scenes with no new dependencies, no binary assets and no CDN imports. Every texture is drawn procedurally on a canvas or in a shader.

## What was built

### Butterfly life cycle — plain tiger (Danaus chrysippus) on aak (Calotropis)
- **Host plant:** a woody, corky stem with two branches; opposite, decussate leaves with short petioles; and three umbels of crown flowers (reflexed lavender petals, a white and purple corona, a staminal column) plus inflated buds. Each leaf is an analytic surface (`leafSurface`). The leaf texture has a midrib, arching secondary veins, a tertiary net and wax speckle, with a separate pale underside, a bump map, a tiled micro-detail layer, sheen and clearcoat, and backlit translucency. Leaves sway in the breeze (instanced matrices updated each frame).
- **Every stage is attached to the plant.** The egg (ribbed, pearly, micropyle at the tip) is glued to the underside of a young leaf. The caterpillar crawls on the upper surface of a mature leaf. It is skinned to a 24-frame spine in the vertex shader, so it follows the curved leaf, sends a peristaltic wave from tail to head, has prolegs on the leaf and three pairs of wiggling filaments, and sweeps its head while it eats. The chewed notch grows in a per-leaf alpha mask. The chrysalis hangs from a silk pad and cremaster under a branch, sways, and goes clear before emergence (a shader blend to a mature map; the gold dots come from a metalness map). The adult stands on four legs (the forelegs are folded, as in all brush-footed butterflies) on the hero flower, opens and closes its wings to bask, and uncoils its proboscis into the corona. It moves with the umbel.
- **Wings:** canvas texture (1024 on high, 512 medium, 256 low) with a separate upper and under side chosen per face in the shader, alpha-cut outlines, nymphalid venation, the black apex with its white band, a black margin with white spots, three hindwing spots and a scale grain. Material: sheen, translucency, alpha-to-coverage. Wings have camber, a hinge at the thorax and offset fore/hind pivots, so they overlap without z-fighting.
- **Sequences:** smooth camera fly-tos between stages; *Watch it emerge* (the case clears, the adult slides out, hangs, and its crumpled wings expand in a shader); *Take flight* (a spline flight with flapping and banking that lands back on the flower; it never hovers aimlessly); *Watch the whole cycle* (a time-lapse covering egg development and hatching, five instars of growth with the notch growing, J-hang, pupation, darkening, eclosion and first flight). A day and instar counter is shown in the HUD.
- **Look:** sky dome with a sun, outdoor PMREM environment, a ring of bokeh tree line, soft foliage cards, instanced swaying grass, pebbles, dust motes, contact shadow, PCF shadows on the high tier, and a depth-of-field post pass (macro-lens look) on medium and high.

### Photosynthesis lab — three zoom levels
1. **Lab bench:** the classic Hydrilla bubble experiment in a darkened lab. A desk lamp slides along a cm ruler. It is a physical SpotLight with decay 2, so illumination really falls as 1/d², and it has a beam cone. Also on the bench: a beaker with graduations, transmissive glass and water (medium and high tiers), a waterline meniscus, an inverted funnel on feet, and an inverted test tube in a clamp stand. Oxygen gas collects at the top of the tube and pushes the water column down. There is a thermometer whose red column tracks the temperature, ice cubes below 12 °C, and a NaHCO₃ dish whose powder heap scales with the CO₂ setting. Instanced bubbles leave the cut stem, wobble and are funnelled into the tube.
2. **Inside a leaf:** a 3D block diagram. Waxy cuticle, upper epidermis, palisade cells and spongy mesophyll with air spaces. Chloroplasts stream around each cell in a shader (cytoplasmic streaming), and glow brighter as light increases. A vein has ringed xylem, phloem and a bundle sheath, and lower-epidermis stomata have guard cells that open and close with water and light. Ball-and-stick CO₂ molecules diffuse in through the stomata to the palisade, and O₂ and H₂O vapour diffuse out.
3. **Chloroplast:** a cut-away double envelope, stroma, about 12 grana stacks of thylakoid discs joined by stroma lamellae, starch grains, plastoglobuli and ribosomes. Photons strike the grana; water is split and O₂ leaves (one O₂ for every two H₂O); ATP/NADPH beads travel to a Calvin-cycle ring that fixes CO₂; every 6 CO₂ fixed release one glucose ring.
- **Model** (`photosynthesis/model.js`): Blackman limiting factors, `rate = min(light, water, CO₂, temperature)`. Light uses PPFD = 2000·(10/d)² with a saturating response, CO₂ uses Michaelis–Menten on the bicarbonate level, and temperature uses an asymmetric enzyme curve that peaks at 25 °C. Water is not limiting for the submerged pondweed on the bench (a panel note says so); it drives the stomata and the rate at the leaf and chloroplast scales. The maximum is 60 bubbles/min.
- **Panel:** zoom chips, lamp distance (with % light), lamp on/off, CO₂ (NaHCO₃ g/100 mL), temperature, soil water, a live rate graph (bubbles/min over the last 2 minutes, with a marker for each change), stats (rate, bubbles counted in the last minute, limiting factor, stomata), light at the plant, O₂ collected, glucose and the equation 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Tapping any part opens an info card.

## Module layout
```
biology/butterfly-life-cycle.js   entry: engine, panel/HUD, picking, update loop
biology/butterfly/kit.js          shared helpers: rig (orbit + fly-to + tap), patchMaterial (back map, translucency, shader hooks),
                                  taperedTube, mergeGeos, paintVertices, skyDome, outdoorEnvironment, rng, easing
biology/butterfly/dof.js          depth-of-field post pass (wraps renderer.render; restored on dispose); also used by photosynthesis
biology/butterfly/textures.js     canvas textures: leaf (front/back/bump/detail), bark, wings, caterpillar, chrysalis, ground, bokeh
biology/butterfly/plant.js        Calotropis: stems, leaves (instanced + hero leaves), umbels, anchors (egg/caterpillar leaf, chrysalis, perch)
biology/butterfly/caterpillar.js  spine-skinned larva
biology/butterfly/adult.js        body, wings, legs (instanced), proboscis
biology/butterfly/stages.js       STAGES data, egg, chrysalis
biology/butterfly/environment.js  sky, sun/shadows, ground, grass, background, motes
biology/butterfly/director.js     stage states, time-lapse, emergence, flight, bites, camera shots, hotspots
biology/photosynthesis.js         entry: worlds, scale transitions (fly-in + fade), panel, graph, picking
biology/photosynthesis/model.js   limiting-factor model
biology/photosynthesis/bench.js   lab-bench world
biology/photosynthesis/leaf-section.js
biology/photosynthesis/chloroplast.js
biology/photosynthesis/molecules.js  instanced ball-and-stick molecules and the path swarm
biology/photosynthesis/graph.js   panel rate graph (2D canvas)
biology/photosynthesis/info.js    info-card text
```
Performance notes: shared geometries and materials; InstancedMesh for leaves, flowers, buds, grass, legs, cells, chloroplasts, discs, molecules and bubbles. Chloroplast streaming and caterpillar deformation run on the GPU. Shadows only on the high tier; transmission and DOF only on medium and high; particle and instance counts are capped per tier. Everything is disposed in `dispose()`.

## How to test
- Desktop and phone: `/app/interactive/living-world/become-a-butterfly/` and `/app/interactive/living-world/plant-power/`.
- Butterfly: try each stage button (or the slider), *Watch it emerge* (Chrysalis), *Take flight* (Adult), *Watch the whole cycle*, *See the whole plant*, and tap the flower, leaf or animal for info cards.
- Photosynthesis: move the lamp from 10 to 80 cm and watch the bubbles, graph and limiting factor change. Set CO₂ to 0, temperature to 5 °C (ice appears) and 45 °C, and soil water to 0 on the leaf scale (stomata close). Switch zoom levels and use *Empty tube*.
- The screenshots were taken with headless SwiftShader (medium tier on 2 cores; high and low were forced through navigator overrides). No console errors.

## Ideas not done
- Egg hatching with a visible first-instar larva chewing the shell (it is currently a darkened egg and then a cut to the leaf); moult skins left behind between instars.
- A mother butterfly laying the egg (the first scene of the cycle) and courtship.
- Wings that flex during flight (they are currently rigid apart from a slight shader ripple); scale iridescence, and a male sex-brand variant.
- A true volumetric light cone and caustics through the beaker; a proper bokeh-shaped DOF instead of a Gaussian.
- Photosynthesis: a "rate vs lamp distance" plot built from the student's own trials; a starch-iodine test mini-activity; and coloured filters for the lamp (to show the action spectrum).
- The shared helpers in `biology/butterfly/kit.js` and `dof.js` could move to `core/` if other sims want them; they were kept local to avoid touching core.
