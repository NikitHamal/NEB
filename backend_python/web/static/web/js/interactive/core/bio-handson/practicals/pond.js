// A pond ecosystem survey, botany and zoology versions. At the pond: read the water temperature,
// test the pH with indicator paper, lower a Secchi disc until it vanishes (and raise it until it
// reappears) for transparency, read dissolved oxygen (zoology), sweep a plankton net, and sort
// the large plants by habit or the animals by what they eat. Back in the lab: a drop of the
// catch under the microscope, where living phytoplankton and zooplankton are found and named;
// then the student builds the pond's food chain or food web.
import { THREE } from '../../engine.js';
import { buildPond, animatePond, PC, PR } from '../specimens/pondscene.js';
import { createPondField, POND_KINDS } from '../fields/pond.js';
import { buildStation, stepDrop, stepCoverslip, stepToStage, createScopeView } from '../slideprep.js';
import { ask, sheet, chipDrop, outdoors, tag } from '../bench.js';
import { mesh, MAT, rng, clamp } from '../kit.js';
import { thermometer, thermoReader } from '../../handson/thermo.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const PH_COL = { 5: '#f08a24', 6: '#f2c83a', 7: '#5bbf3a', 8: '#1f9d8a', 9: '#2b6cb0' };
const HABIT = {
  'Typha (cattail)': ['emergent', 'Amphibious (emergent): rooted in the mud at the edge, leaves standing above the water.'],
  'Lotus (Nelumbo)': ['rooted-floating', 'Rooted with floating leaves: rhizome in the mud, broad waxy leaves on long petioles.'],
  'Water hyacinth (Eichhornia)': ['free-floating', 'Free-floating: swollen spongy petioles full of air keep it afloat; roots hang in the water.'],
  'Duckweed (Lemna)': ['free-floating', 'Free-floating: the smallest flowering plant, a tiny frond with one root.'],
  Hydrilla: ['submerged', 'Submerged: wholly under water, thin leaves in whorls, no cuticle or stomata needed.'],
};
const DIET = {
  Frog: ['carnivore', 'Frog: eats insects — a secondary (or tertiary) consumer.'], 'Snail (Pila)': ['herbivore', 'Snail: grazes on algae and water plants — a primary consumer.'],
  Fish: ['carnivore', 'Small fish: eat zooplankton and insect larvae — secondary consumers.'], 'Water strider': ['carnivore', 'Water strider: catches insects trapped on the surface film — a carnivore.'],
  Dragonfly: ['carnivore', 'Dragonfly: a hunter, both as aquatic nymph and as adult.'], Tadpoles: ['herbivore', 'Tadpoles: scrape algae — primary consumers (they turn carnivorous as frogs).'],
};

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools } = ctx;
  const zoo = ctx.config.slug.endsWith('zoology');
  const R = rng((Date.now() & 0xffff) || 13);
  const hud = createHud(ctx); const chip = hud.chip('ho-chip-read');
  let restore = outdoors(ctx, { sky: 0xc7e0f2 });
  const pond = buildPond(5); world.add(pond.group);
  const truth = { T: Math.round((19 + R() * 6) * 2) / 2, pH: 7 + Math.round(R() * 1.4), SD: 30 + Math.round(R() * 25), DO: +(5.2 + R() * 2.6).toFixed(1) };
  // field kit at the bank
  const th = thermometer({ min: 0, max: 50, div: 0.5, len: 2.4 }); th.group.position.set(-2.6, 0.06, 5.6); th.group.rotation.z = Math.PI / 2; world.add(th.group); th.set(26, true);
  const reader = thermoReader(ctx, th);
  const bottle = new THREE.Group(); bottle.position.set(-1.0, 0, 5.9); world.add(bottle); bottle.add(mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.8, 18), MAT.glass(), [0, 0.4, 0], { cast: false })); const bw = mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.5, 18), MAT.liquid(0x7fa58a, 0.6), [0, 0.27, 0], { cast: false }); bw.visible = false; bottle.add(bw); const bt = tag('sample bottle', { h: 0.1 }); bt.position.set(0, 1.0, 0); bottle.add(bt);
  const plank = mesh(new THREE.BoxGeometry(1.4, 0.2, 7), MAT.matte(0x8b5a2b), [3.5, 0.3, PC.z + PR - 1.5]); world.add(plank);
  const disc = new THREE.Group(); disc.position.set(3.5, 0.5, PC.z + PR - 4.6); world.add(disc);
  const dface = new THREE.Group(); disc.add(dface);
  const dmat = [0, 1, 2, 3].map((q) => new THREE.MeshStandardMaterial({ color: q % 2 ? 0x111111 : 0xf8fafc, transparent: true }));
  dmat.forEach((m, q) => { const s = mesh(new THREE.CircleGeometry(1.0, 16, q * Math.PI / 2, Math.PI / 2), m); s.rotation.x = -Math.PI / 2; dface.add(s); });
  const rope = mesh(new THREE.CylinderGeometry(0.03, 0.03, 1, 6), MAT.matte(0xe7e5e4), [0, 0.5, 0]); disc.add(rope);
  const dt0 = tag('Secchi disc', { h: 0.16 }); dt0.position.set(0, 1.6, 0); disc.add(dt0);
  const net = new THREE.Group(); net.position.set(1.4, 0, 7.4); world.add(net); net.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 6, 8), MAT.matte(0x8b5a2b), [0, 0.15, 0]).rotateX(Math.PI / 2 - 0.15)); const ring = mesh(new THREE.TorusGeometry(0.6, 0.04, 6, 24), MAT.steel(), [0, 0.35, -3.2]); net.add(ring); const bag = mesh(new THREE.ConeGeometry(0.58, 1.6, 16, 1, true), new THREE.MeshStandardMaterial({ color: 0xf1f5f9, transparent: true, opacity: 0.7, side: THREE.DoubleSide }), [0, 0.35, -2.4]); bag.rotation.x = -Math.PI / 2; net.add(bag);
  const nt = tag('plankton net', { h: 0.14 }); nt.position.set(0, 1.0, -1); net.add(nt);
  const meter = new THREE.Group(); meter.position.set(0.2, 0, 6.0); meter.visible = zoo; world.add(meter); meter.add(mesh(new THREE.BoxGeometry(0.7, 0.25, 1.1), MAT.gloss(0x1e293b), [0, 0.13, 0])); const mt = tag('DO meter', { h: 0.1 }); mt.position.set(0, 0.6, 0); meter.add(mt);
  const BANK = S([0, 9, 15], [0, -0.5, -4], 26, 14);
  const THS = S([-1.9, 1.6, 7.6], [-2.1, 0.1, 5.5], 2.4);
  let depth = 0; let reads = []; let sh = null; let view = null; const found = new Set();

  const stepTemp = {
    title: 'Water temperature', text: 'Tap the thermometer to dip its bulb in the pond for a minute, then tap its scale where the mercury ends to read it.', tool: null, autoTool: 'hand', hideBelt: true, shot: THS,
    skip() { reads.T = truth.T; ui.observe('Water temperature', `${truth.T} °C`); },
    handler: { down() {
      if (!this.dipped) { if (!input.pick([th.group], true)) return false; this.dipped = true; sfx.play('drop'); th.set(truth.T); th.group.rotation.set(-0.35, 0, 0); th.group.position.set(-2.4, -0.55, 3.75); ctx.rig.go(S([-2.1, 1.3, 5.4], [-2.4, 0.9, 3.5], 1.2, 1.4), 0.8); return true; }
      const v = reader.tap(); if (v === null) return false; if (Math.abs(v - th.reading) > 0.5) { ctx.mistake(`Read again with your eye level with the end of the mercury thread (you read ${v} °C).`, 2); return true; }
      reads.T = v; ui.observe('Water temperature', `${v} °C`); sfx.play('ok'); ctx.next(); return true;
    } },
  };
  const stepPH = {
    title: 'pH of the water', text: 'Tap the sample bottle to fill it with pond water, then with the <b>forceps</b> dip a strip of pH paper in it (tap the bottle again).', tool: 'forceps', hideBelt: false, shot: S([-0.8, 2.0, 8.4], [-1.0, 0.3, 5.9], 2.5),
    skip() { bw.visible = true; reads.pH = truth.pH; ui.observe('pH', String(truth.pH)); },
    handler: { down() {
      if (!input.pick([bottle], true)) return false;
      if (!bw.visible) { bw.visible = true; sfx.play('pour'); return true; }
      if (!ctx.requireTool('forceps', 'Hold pH paper with <b>forceps</b>.')) return true;
      sfx.play('drop'); const card = sheet(ctx, { title: 'pH paper in pond water' }); card.set(`<div style="display:flex;gap:8px;align-items:center"><span style="width:26px;height:70px;border-radius:4px;background:${PH_COL[truth.pH]}"></span><div style="display:flex;gap:3px">${Object.entries(PH_COL).map(([p, c]) => `<span style="text-align:center;font-size:.7rem"><i style="display:block;width:30px;height:30px;border-radius:4px;background:${c}"></i>${p}</span>`).join('')}</div></div>`);
      ask(ctx, 'The strip matches pH…', Object.keys(PH_COL).map((p) => ({ label: p, value: +p })), truth.pH, { delay: 0.3, wrong: 'Hold the strip beside the chart.', then() { card.remove(); reads.pH = truth.pH; ui.observe('pH', String(truth.pH)); ctx.next(truth.pH >= 8 ? 'Slightly alkaline: algae using CO₂ for photosynthesis raise the pH by day.' : 'Close to neutral — good for most pond life.'); } });
      return true;
    } },
    exit() { ui.clearChooser(); ui.root.querySelectorAll('.bh-sheet').forEach((n) => n.remove()); },
  };
  function setDepth(d) { depth = clamp(d, 0, 120); disc.position.y = 0.5 - 0.8 - depth / 10; rope.scale.y = 0.8 + depth / 10 + 0.3; rope.position.y = rope.scale.y / 2; const vis = clamp((truth.SD * 1.12 - depth) / (truth.SD * 0.35)); dmat.forEach((m, q) => { m.opacity = vis; m.color.setHex(q % 2 ? 0x111111 : 0xf8fafc).lerp(new THREE.Color(0x4f7f5a), 1 - vis); }); }
  const secchi = { down: null, up: null };
  const stepSecchi = {
    title: 'Transparency with a Secchi disc', text: 'From the plank, <b>drag down</b> to lower the disc. Let go the moment it disappears. Then drag up slowly and let go when it just reappears.', tool: null, autoTool: 'hand', hideBelt: true,
    shot: S([7.0, 3.0, PC.z + PR + 3.5], [3.5, -2.8, PC.z + PR - 4.6], 5, 7.5),
    enter() { setDepth(0); secchi.down = secchi.up = null; },
    exit() { chip.show(false); },
    skip() { secchi.down = truth.SD + 2; secchi.up = truth.SD - 3; },
    handler: {
      down(p) { this.y = p.y; this.d0 = depth; return true; },
      move(p) { if (this.y === undefined) return; setDepth(this.d0 + (p.y - this.y) * 0.25); chip.at.copy(rope.getWorldPosition(new THREE.Vector3())).setY(ctx.BENCH_Y + 0.7); chip.set(`rope mark <b>${Math.round(depth)}</b> cm`).show(true); },
      up() {
        this.y = undefined; const d = Math.round(depth);
        if (secchi.down === null) { if (d < 8) return; secchi.down = d; ui.observe('Disc disappears at', `${d} cm`); ctx.say('Now raise it slowly until it just reappears.', 'info', 2500); return; }
        if (d >= secchi.down) return; secchi.up = d; ui.observe('Disc reappears at', `${d} cm`);
        const sd = (secchi.down + secchi.up) / 2; ui.observe('Secchi depth', `${sd.toFixed(1)} cm`);
        ctx.next(sd < 40 ? `Secchi depth ${sd.toFixed(0)} cm: turbid water, rich in plankton and silt.` : `Secchi depth ${sd.toFixed(0)} cm: moderately clear water.`);
      },
    },
  };
  const stepDO = {
    title: 'Dissolved oxygen', text: 'Tap the DO meter to put its probe in the water and wait for the reading to settle.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0.6, 2.0, 8.6], [0.2, 0.3, 6.0], 2.6),
    skip() { reads.DO = truth.DO; ui.observe('Dissolved O₂', `${truth.DO} mg/L`); },
    handler: { down() { if (!input.pick([meter], true)) return false; sfx.play('click'); let v = 0; meter.getWorldPosition(chip.at); chip.at.y += 0.4; anim.add(2.5, (k) => { v = truth.DO * (1 - Math.exp(-4 * k)); chip.set(`<b>${v.toFixed(1)}</b> mg/L O₂`).show(true); }, { done: () => { reads.DO = truth.DO; ui.observe('Dissolved O₂', `${truth.DO} mg/L`); anim.wait(1.0, () => { chip.show(false); ask(ctx, `${truth.DO} mg/L of oxygen: is this healthy for fish?`, [{ label: 'Yes — above about 5 mg/L', value: 'y' }, { label: 'No — fish need over 15 mg/L', value: 'n' }], 'y', { delay: 0.1, ok: 'Most fish need more than 5 mg/L. Oxygen comes from the air and from photosynthesis of plants and algae; decomposers use it up.', wrong: 'Water at 20–25 °C holds at most about 8–9 mg/L when saturated.' }); }); } }); return true; } },
    exit() { ui.clearChooser(); chip.show(false); },
  };
  const stepNet = {
    title: 'Sweep the plankton net', text: 'Drag the plankton net through the water in a long sweep. The fine mesh strains out the tiny plankton.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([1.5, 5, 13], [1.0, -0.3, 1.5], 11),
    skip() { bw.visible = true; bw.material.color.setHex(0x6a9a70); },
    handler: {
      down(p) { this.last = [p.x, p.y]; this.d = 0; net.position.y = -0.3; return true; },
      move(p) { if (!this.last) return; this.d += Math.hypot(p.x - this.last[0], p.y - this.last[1]); this.last = [p.x, p.y]; net.rotation.y = Math.sin(this.d / 160) * 0.5; ctx.progress(clamp(this.d / 700)); if (this.d > 700 && !this.fin) { this.fin = true; sfx.play('pour'); net.position.y = 0; bw.visible = true; ctx.next('The net is rinsed into the sample bottle: green, cloudy, faintly moving.'); } },
      up() { this.last = null; if (!this.fin) net.position.y = 0; },
    },
  };
  const ORG = zoo ? DIET : HABIT; const OPTS = zoo ? [['herbivore', 'Herbivore (primary consumer)'], ['carnivore', 'Carnivore (secondary/tertiary consumer)']] : [['emergent', 'Amphibious / emergent'], ['rooted-floating', 'Rooted, leaves floating'], ['free-floating', 'Free-floating'], ['submerged', 'Submerged']];
  const objOf = (name) => Object.values(pond.org).find((o) => o.name === name);
  const stepOrg = {
    title: zoo ? 'Pond animals and what they eat' : 'Pond plants and their habits', text: zoo ? 'Tap each animal (frog, snails on the stone, fish, water strider, dragonfly, tadpoles) and say what it eats.' : 'Tap each plant (cattail, lotus, water hyacinth, duckweed, Hydrilla below the surface) and choose its habit.',
    tool: null, autoTool: 'hand', hideBelt: true, shot: BANK,
    skip() { Object.keys(ORG).forEach((n) => found.add(n)); },
    handler: { down(p) {
      const objs = Object.keys(ORG).map(objOf).filter(Boolean); const h = input.pick(objs, true); if (!h) return false;
      let o = h.object; while (o && !ORG[o.name]) o = o.parent; if (!o) return false; const name = o.name; if (found.has(name)) { ctx.say(`${name}: done.`, 'hint', 900); return true; }
      ui.choose(p.x, p.y, name, OPTS.map(([v, l]) => ({ label: l, value: v })), (v) => {
        if (v !== ORG[name][0]) { ctx.mistake(`Not quite. ${zoo ? 'Think about what it feeds on.' : 'Where are its roots, and where are its leaves?'}`, 2); return; }
        found.add(name); sfx.play('ok'); ctx.say(ORG[name][1], 'good', 4200); ui.observe(name, OPTS.find((q) => q[0] === v)[1]); ctx.progress(found.size / Object.keys(ORG).length);
        if (found.size === Object.keys(ORG).length) anim.wait(1.2, () => ctx.next());
      });
      return true;
    } },
    exit() { ui.clearChooser(); },
  };
  // ---- back in the lab ---------------------------------------------------------------------------
  const lab = Object.create(ctx); const labWorld = new THREE.Group(); world.add(labWorld); lab.world = labWorld; labWorld.visible = false;
  const station = buildStation(lab, { stainColor: 0x7fa58a, tileX: 0.0, scopeX: 1.95 });
  const stepBack = {
    title: 'Back in the lab', text: 'Tap the sample bottle on the bench to begin examining the plankton.', tool: null, autoTool: 'hand', shot: S([0.8, 2.6, 3.6], [0.9, 0.4, 0.0], 4.0),
    enter() { goIndoors(); },
    skip() { goIndoors(); },
    handler: { down() { if (!input.pick([labBottle], true)) return false; sfx.play('glass'); ctx.next('Shake gently and take a drop from near the bottom, where the plankton settle.'); return true; } },
  };
  let labBottle = null;
  function goIndoors() {
    if (labWorld.visible) return; if (restore) { restore(); restore = null; }
    pond.group.visible = false; [th.group, bottle, plank, disc, net, meter].forEach((o) => { o.visible = false; }); labWorld.visible = true;
    labBottle = bottle.clone(); labBottle.visible = true; labBottle.scale.setScalar(0.5); labBottle.position.set(-1.1, 0, 0.2); labWorld.add(labBottle);
  }
  const field = createPondField(R() * 1000 | 0);
  const want = zoo ? ['Paramecium', 'Rotifer', 'Cyclops', 'Daphnia', 'Volvox', 'Diatom'] : ['Spirogyra', 'Diatom', 'Volvox', 'Chlamydomonas', 'Oscillatoria', 'Daphnia'];
  const scope = (fn) => { if (!view) { view = createScopeView(lab, station, field, { objective: 4, focus: -40, onTap: (it, e) => { if (ctx.step && ctx.step.onTap) ctx.step.onTap(it, e); } }); ctx.debug.view = view; } fn(view); };
  const stepLook = {
    title: 'Find the plankton', text: '', tool: null, hideBelt: true,
    handler: { down() { if (station && input.pick(station.scope.pickables || [], true)) { scope((v) => v.open()); return true; } return false; } },
    enter() { scope((v) => v.open()); this.k = 0; this.prompt(); },
    prompt() { const k = found2.size; ui.setText(`Drag the field to search, change objectives, and tap each of: <b>${want.filter((w) => !found2.has(w)).join(', ')}</b>. (${k} of ${want.length})`); ctx.progress(k / want.length); },
    skip() { want.forEach((w) => found2.add(w)); },
    onTap(it, e) {
      if (!it) { ctx.say('Nothing there — just water.', 'hint', 900); return; }
      if (found2.has(it.kind)) { ctx.say(`${it.kind} — already recorded.`, 'hint', 1000); return; }
      if (!want.includes(it.kind)) { ctx.say(`${it.kind} (${POND_KINDS[it.kind]}). Interesting, but find the ones listed.`, 'info', 1800); return; }
      found2.add(it.kind); sfx.play('ok'); view.eye.mark(e.x, e.y, it.kind); ui.observe(it.kind, POND_KINDS[it.kind] === 'producer' ? 'phytoplankton (producer)' : 'zooplankton (consumer)');
      ctx.say(NOTE[it.kind], 'good', 4200); this.prompt(); if (found2.size === want.length) ctx.anim.wait(1.5, () => { view.close(); ctx.next(); });
    },
  };
  const found2 = new Set();
  const NOTE = {
    Spirogyra: 'Spirogyra: unbranched green filament; each cell has ribbon-shaped spiral chloroplasts.', Diatom: 'Diatom: golden-brown, boat-shaped, in a two-part silica shell (frustule).', Volvox: 'Volvox: a hollow ball of hundreds of flagellate cells, with daughter colonies inside; it rolls.',
    Chlamydomonas: 'Chlamydomonas: one green cell with two flagella, a cup-shaped chloroplast and a red eyespot.', Oscillatoria: 'Oscillatoria: blue-green filament (cyanobacterium) that glides and sways.', Euglena: 'Euglena: green, flagellate, with a red eyespot — both plant-like and animal-like.',
    Paramecium: 'Paramecium: slipper-shaped ciliate, covered in beating cilia, with contractile vacuoles.', Rotifer: 'Rotifer: a tiny multicellular animal; the beating corona at its head looks like turning wheels.',
    Cyclops: 'Cyclops: a copepod with one median eye and, in females, a pair of egg sacs.', Daphnia: 'Daphnia (water flea): transparent carapace, a beating heart, eggs in the brood pouch; swims with its big antennae.',
  };
  const stepWeb = {
    title: zoo ? 'Build the pond food web' : 'Build the pond food chain', text: 'Drag each organism into its trophic level (or tap it, then tap the level).', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0.8, 2.6, 3.6], [0.9, 0.4, 0.0], 4.0),
    enter() {
      const LV = [['p', 'Producers'], ['c1', 'Primary consumers'], ['c2', 'Secondary consumers'], ['c3', 'Tertiary consumers'], ['d', 'Decomposers']];
      const CH = zoo ? [['Phytoplankton', 'p'], ['Hydrilla', 'p'], ['Daphnia', 'c1'], ['Snail', 'c1'], ['Tadpole', 'c1'], ['Small fish', 'c2'], ['Dragonfly nymph', 'c2'], ['Frog', 'c2'], ['Kingfisher', 'c3'], ['Water snake', 'c3'], ['Bacteria and fungi', 'd']] : [['Phytoplankton (Spirogyra)', 'p'], ['Zooplankton (Daphnia)', 'c1'], ['Small fish', 'c2'], ['Kingfisher', 'c3'], ['Bacteria and fungi', 'd']];
      sh = sheet(ctx, { title: zoo ? 'Food web of the pond' : 'Food chain of the pond', cls: 'wide' });
      if (view && view.eye) view.eye.show(false);
      sh.set(`<div class="bh-dtray"></div><div style="display:flex;flex-direction:column;gap:5px">${LV.map(([id, l]) => `<div><b style="font-size:.7rem;color:#475569">${l}</b><div class="bh-slot" data-slot="${id}"></div></div>`).join('')}</div>`);
      let n = 0; this.dz = chipDrop(ctx, sh.body.querySelector('.bh-dtray'), CH.map(([nm]) => ({ id: nm, html: nm })), sh.body, (id, slot, chipEl, slotEl) => {
        const want2 = CH.find((c) => c[0] === id)[1]; if (want2 !== slot) { ctx.mistake(`${id} does not belong with the ${LV.find((l) => l[0] === slot)[1].toLowerCase()}.`, 1); return false; }
        slotEl.appendChild(chipEl); n += 1; if (n === CH.length) anim.wait(0.6, () => ask(ctx, 'About how much energy passes from one trophic level to the next?', [{ label: 'About 10 %', value: 10 }, { label: 'About 50 %', value: 50 }, { label: 'All of it', value: 100 }], 10, { delay: 0.2, ok: 'About 10 % (Lindeman): the rest is lost as heat in respiration — which is why pond food chains rarely have more than four or five links, and producers are by far the most abundant.', wrong: 'Most of the energy each level takes in is used in its own respiration.' }));
        return true;
      });
    },
    exit() { ui.clearChooser(); if (this.dz) this.dz.dispose(); if (sh) { sh.remove(); sh = null; } },
  };
  const steps = [stepTemp, stepPH, stepSecchi, ...(zoo ? [stepDO] : []), stepNet, stepOrg, stepBack,
    stepDrop(lab, station, { title: 'A drop of pond water', text: 'With the <b>dropper</b>, put one drop of the plankton sample in the middle of the slide.', color: 0x7fa58a, shot: S([0.3, 1.2, 1.4], [0.35, 0.05, 0.5], 1.4) }),
    stepCoverslip(lab, station, { shot: S([0.3, 1.0, 1.2], [0.35, 0.05, 0.5], 1.2) }),
    stepToStage(lab, station, { shotStart: S([0.6, 1.9, 2.4], [0.5, 0.2, 0.3], 2.4) }), stepLook, stepWeb];
  ctx.debug = { pond, truth, field, disc, th, get station() { return station; } };
  return {
    tools: ['hand', 'forceps', 'dropper', 'needle'],
    steps,
    update(dt, t) { animatePond(pond, t); th.update(dt, 1.2); hud.update(); if (view) view.update(t); },
    result() {
      const sd = secchi.down !== null && secchi.up !== null ? (secchi.down + secchi.up) / 2 : truth.SD;
      return { title: zoo ? 'Pond ecosystem: zoology survey' : 'Pond ecosystem: biotic and abiotic factors', rows: [['Water temperature', `${reads.T ?? truth.T} °C`], ['pH', String(truth.pH)], ['Secchi depth', `${sd.toFixed(1)} cm (true ${truth.SD} cm)`], ...(zoo ? [['Dissolved O₂', `${truth.DO} mg/L`]] : []), ['Plankton identified', [...found2].join(', ')], [zoo ? 'Animals classified' : 'Plants classified', `${found.size}`]], conclusion: zoo ? 'A pond is a self-sustaining ecosystem. Phytoplankton and water plants are the producers; zooplankton (Daphnia, Cyclops, rotifers, Paramecium), snails and tadpoles are primary consumers; insects, fish and frogs secondary consumers; birds such as the kingfisher top carnivores; bacteria and fungi decompose the dead. Temperature, pH, light (transparency) and dissolved oxygen control which organisms can live there.' : 'The pond\'s abiotic factors (temperature, pH, transparency) and its biotic community are linked: emergent, rooted-floating, free-floating and submerged plants and phytoplankton are the producers; zooplankton, fish and birds are consumers; bacteria and fungi decompose dead matter and return nutrients.' };
    },
    dispose() { if (restore) restore(); if (view) view.dispose(); hud.dispose(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}
