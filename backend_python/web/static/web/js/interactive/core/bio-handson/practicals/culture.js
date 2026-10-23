// Culturing soil microorganisms by serial dilution and the spread-plate method. Work beside a
// spirit-lamp flame: 1 g of soil into 9 mL of sterile water (10⁻¹), transfer 1 mL down the tubes
// to 10⁻⁴, pour molten nutrient agar into three plates, pipette 0.1 mL of the 10⁻³ and 10⁻⁴
// dilutions onto two of them (the third is the uninoculated control), dip the spreader in
// alcohol, flame it and spread. Incubate for 48 h, choose the plate in the countable range, mark
// every colony with a pen, tell bacteria, moulds and actinomycetes apart and work out the
// colony-forming units per gram of soil from the student's own count.
import { THREE } from '../../engine.js';
import { spiritLamp, watchGlass } from '../props.js';
import { makeTube, makeRack } from '../glassware.js';
import { plate, scatter, incubator } from '../specimens/microbe.js';
import { timelapse, ask, tag, glassBeaker } from '../bench.js';
import { mesh, MAT, rng, clamp, ease } from '../kit.js';
import { conicalFlask } from '../../handson/glass.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const SUP = ['10⁻¹', '10⁻²', '10⁻³', '10⁻⁴'];

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const seed = (Date.now() & 0xffff) || 41; const R = rng(seed);
  const hud = createHud(ctx);
  const cfuTrue = (4.2 + R() * 2.4) * 1e5; // per gram
  const lamp = spiritLamp(); lamp.position.set(-0.2, 0, -0.45); world.add(lamp);
  const rack = makeRack(4); rack.group.position.set(-1.55, 0, -0.35); world.add(rack.group);
  const tubes = SUP.map((s, i) => { const t = makeTube(s, { color: 0xeef6ff, fill: 0.55 }); t.group.position.copy(rack.slots[i]); rack.group.add(t.group); return t; });
  const soil = watchGlass(); soil.position.set(-1.6, 0, 0.55); world.add(soil);
  const soilHeap = mesh(new THREE.SphereGeometry(0.16, 16, 10), new THREE.MeshStandardMaterial({ color: 0x5b3a22, roughness: 1 }), [0, 0.05, 0]); soilHeap.scale.y = 0.4; soil.add(soilHeap);
  const soilTag = tag('1 g soil', { h: 0.06 }); soilTag.position.set(0, 0.25, 0); soil.add(soilTag);
  const agarF = conicalFlask({ color: 0xf2dfa6, opacity: 0.7 }); agarF.setVolume(150); agarF.group.position.set(1.95, 0, -0.55); world.add(agarF.group);
  const agTag = tag('nutrient agar, 45 °C', { h: 0.07 }); agTag.position.set(1.95, 1.65, -0.55); world.add(agTag);
  const alc = glassBeaker(0.14, 0.32, 0xf1f5f9, 0.6); alc.group.position.set(0.45, 0, -0.55); world.add(alc.group);
  const alTag = tag('70% alcohol', { h: 0.06 }); alTag.position.set(0.45, 0.45, -0.55); world.add(alTag);
  const NAMES = ['10⁻³', '10⁻⁴', 'control'];
  const plates = NAMES.map((n, i) => { const p = plate(); p.group.position.set(-0.55 + i * 1.0, 0, 0.55); world.add(p.group); const t = tag(n, { h: 0.07 }); t.position.set(0, 0.25, 0.45); p.group.add(t); return Object.assign(p, { name: n, inoc: false, spread: 0, contam: false }); });
  const inc = incubator('30 °C'); inc.group.position.set(2.9, 0, 0.2); inc.group.rotation.y = -0.5; world.add(inc.group);
  const S_ALL = S([0.2, 2.3, 3.4], [0.15, 0.5, 0.0], 4.6);
  const S_TUBES = S([-1.2, 1.7, 1.8], [-1.35, 0.5, 0.0], 1.9);
  const S_PLATES = S([0.0, 1.8, 2.1], [0.0, 0.1, 0.4], 2.8);
  const PLATE_TOP = (p) => { const v = p.group.position; return S([v.x, 1.25, v.z + 0.12], [v.x, 0.02, v.z], 0.95, 0.95); };
  let loaded = null; let spreaderClean = false; let spreaderHot = 0; let marked = new Set(); let chosen = null; let count = 0;
  const tmp = new THREE.Vector3();

  const stepLamp = {
    title: 'Light the spirit lamp', text: 'Microbiology is done close to a flame: the rising hot air keeps dust and spores away. Tap the spirit lamp.', tool: null, autoTool: 'hand', shot: S_ALL,
    skip() { lamp.userData.flame.visible = true; },
    handler: { down() { if (!input.pick([lamp], true)) return false; lamp.userData.flame.visible = true; sfx.play('click'); ctx.next(); return true; } },
  };
  const stepSoil = {
    title: 'Make the 10⁻¹ suspension', text: 'Tap the weighed <b>1 g of soil</b> to tip it into the first tube of 9 mL sterile water, and shake well.', tool: null, autoTool: 'hand', shot: S_TUBES,
    skip() { soilHeap.visible = false; tubes[0].material.color.setHex(0xb59a76); },
    handler: { down() { if (!input.pick([soil], true)) return false; soilHeap.visible = false; sfx.play('pour'); tubes[0].to(anim, { color: 0xb59a76, dur: 1.2 }); anim.add(0.6, (k) => { tubes[0].group.rotation.z = Math.sin(k * Math.PI * 6) * 0.15; }, { done: () => { tubes[0].group.rotation.z = 0; ctx.next('1 g in 10 mL in total: a 10⁻¹ dilution.'); } }); return true; } },
  };
  let nextFrom = 0;
  const stepDilute = {
    title: 'Serial dilution to 10⁻⁴', text: 'With the sterile <b>pipette</b>, take 1 mL from the 10⁻¹ tube into the 10⁻² tube, mix, then 10⁻² into 10⁻³, and 10⁻³ into 10⁻⁴.', tool: 'dropper', shot: S_TUBES,
    skip() { tubes.forEach((t, i) => t.material.color.setHex([0xb59a76, 0xd6c6ad, 0xe6ddd0, 0xeee8e0][i])); nextFrom = 3; },
    handler: { down() {
      const i = tubes.findIndex((t) => input.pick([t.group], true)); if (i < 0) return false; if (!ctx.requireTool('dropper', 'Use the sterile <b>pipette</b> (dropper) to measure 1 mL.')) return true;
      if (loaded === null) { if (i !== nextFrom) { ctx.mistake(`Draw from the ${SUP[nextFrom]} tube: each dilution is made from the one before it.`, 2); return true; } loaded = i; tools.action(1); sfx.play('pick'); return true; }
      if (i !== loaded + 1) { ctx.mistake(`1 mL from ${SUP[loaded]} must go into the next tube, ${SUP[loaded + 1]}.`, 2); return true; }
      tools.action(0); sfx.play('drip'); tubes[i].to(anim, { color: [0xb59a76, 0xd6c6ad, 0xe6ddd0, 0xeee8e0][i], dur: 0.8 }); loaded = null; nextFrom = i;
      ctx.progress(i / 3); if (i === 3) ctx.next('Each tube is ten times more dilute than the last.'); return true;
    } },
  };
  let poured = 0;
  const stepPour = {
    title: 'Pour the plates', text: 'Lift each lid a little and pour about 15 mL of molten nutrient agar: tap the agar flask, then a plate. Do all three.', tool: null, autoTool: 'hand', shot: S_PLATES,
    skip() { plates.forEach((p) => p.pour()); poured = 3; },
    handler: { down() {
      if (input.pick([agarF.group], true)) { this.ready = true; sfx.play('glass'); return true; }
      const p = plates.find((q) => input.pick([q.group], true)); if (!p) return false;
      if (!this.ready) { ctx.say('Tap the agar flask first.', 'hint', 1400); return true; }
      if (p.agar.visible) return true; this.ready = false; sfx.play('pour'); const l0 = p.lid.position.y; anim.add(0.9, (k) => { p.lid.position.y = l0 + Math.sin(Math.PI * k) * 0.25; }, { done: () => { p.pour(); poured += 1; agarF.setVolume(150 - poured * 15); if (poured === 3) ctx.next('Three plates of agar, set firm.'); } });
      return true;
    } },
  };
  let inocNext = 0;
  const stepInoc = {
    title: 'Pipette 0.1 mL onto the plates', text: 'Take 0.1 mL from the <b>10⁻³</b> tube onto the plate marked 10⁻³, then 0.1 mL from <b>10⁻⁴</b> onto the 10⁻⁴ plate. Leave the control plate alone.', tool: 'dropper', shot: S([-0.5, 1.9, 2.2], [-0.6, 0.2, 0.15], 2.8),
    skip() { plates[0].inoc = plates[1].inoc = true; plates[0].setWet(1); plates[1].setWet(1); },
    handler: { down() {
      const ti = tubes.findIndex((t) => input.pick([t.group], true));
      if (ti >= 0) { if (!ctx.requireTool('dropper')) return true; loaded = ti; tools.action(1); sfx.play('pick'); return true; }
      const p = plates.find((q) => input.pick([q.group], true)); if (!p) return false; if (!ctx.requireTool('dropper')) return true;
      if (loaded === null) { ctx.say('Draw 0.1 mL from a dilution tube first.', 'hint', 1500); return true; }
      if (p.name === 'control') { ctx.mistake('The control plate gets no soil: it shows whether the agar and your technique were sterile.', 3); return true; }
      if (SUP[loaded] !== p.name) { ctx.mistake(`That drop is from ${SUP[loaded]}; the plate is marked ${p.name}. A mix-up would make the count meaningless.`, 3); return true; }
      tools.action(0); sfx.play('drip'); p.inoc = true; p.setWet(1); loaded = null; inocNext += 1;
      if (plates[0].inoc && plates[1].inoc) ctx.next('A drop of 0.1 mL sits on each of the two plates.'); return true;
    } },
  };
  function spreadStep(pi) {
    const p = plates[pi];
    return {
      title: `Spread the ${p.name} plate`, text: 'Pick up the <b>spreader</b>, dip it in the alcohol, pass it through the flame, let the alcohol burn off, then spread the drop all over the agar with circular strokes.', tool: 'spreader', shot: S([p.group.position.x + 0.4, 1.6, 1.9], [p.group.position.x, 0.1, 0.1], 2.1),
      enter() { spreaderClean = false; },
      skip() { p.spread = 1; p.setWet(0); },
      handler: {
        down(ptr) {
          if (!ctx.requireTool('spreader')) return !!input.pick([alc.group, lamp, p.group], true);
          if (input.pick([alc.group], true)) { this.dipped = true; spreaderClean = false; sfx.play('drop'); ctx.say('Dipped in alcohol. Now flame it.', 'info', 1400); return true; }
          if (input.pick([lamp], true)) { if (!this.dipped) { ctx.say('Dip it in alcohol first, then flame.', 'hint', 1500); return true; } fx.burst(lamp.getWorldPosition(tmp).add(new THREE.Vector3(0, 0.55, 0)), 0xfb923c, 10, 0.15, ctx.BENCH_Y + 0.3); sfx.play('switch'); spreaderClean = true; spreaderHot = 1.0; this.dipped = false; ctx.say('The alcohol flares and burns off. Let the glass cool a moment.', 'info', 1800); return true; }
          if (!input.pick([p.group], true)) return false;
          if (!spreaderClean && !p.contam) { p.contam = true; ctx.mistake('Unflamed spreader: microbes from the bench and air go onto the plate. Expect contaminant colonies.', 4); }
          if (spreaderHot > 0.2) { ctx.mistake('Too hot! A hot spreader kills the very microbes you want to count. Wait a moment after flaming.', 2); return true; }
          this.last = [ptr.x, ptr.y]; tools.press(1); return true;
        },
        move(ptr) { if (!this.last) return; p.spread = clamp(p.spread + Math.hypot(ptr.x - this.last[0], ptr.y - this.last[1]) / 1400); this.last = [ptr.x, ptr.y]; p.setWet(1 - p.spread); ctx.progress(p.spread); if (p.spread >= 1 && !this.fin) { this.fin = true; this.last = null; tools.press(0); ctx.next('Spread evenly over the whole surface.'); } },
        up() { this.last = null; tools.press(0); },
      },
    };
  }
  function seedColonies() {
    const N3 = Math.round(cfuTrue * 0.1 * 1e-3 * (0.9 + R() * 0.2)); const N4 = Math.max(2, Math.round(N3 / 10 + (R() - 0.5) * 3));
    const mk = (n, s) => scatter(n, s, 0.04).map(([u, v]) => { const r = R(); const kind = r < 0.1 ? 'fungus' : r < 0.2 ? 'actino' : 'bacterium'; return { kind, u, v, rmax: kind === 'fungus' ? 3.5 + R() * 2.5 : kind === 'actino' ? 0.8 + R() * 0.4 : 0.9 + R() * 1.3, t0: kind === 'fungus' ? 14 + R() * 8 : kind === 'actino' ? 20 + R() * 8 : 6 + R() * 8, tau: kind === 'fungus' ? 24 : 16, col: kind === 'bacterium' ? [[238, 226, 190], [245, 236, 210], [236, 200, 120], [250, 245, 235]][Math.floor(R() * 4)] : null, seed: R() * 6 }; });
    plates[0].seed(mk(N3, seed + 1)); plates[1].seed(mk(N4, seed + 2));
    plates.forEach((p, i) => { if (p.contam || (i === 2 && plates.some((q) => q.contam) && R() < 0.5)) p.seed(scatter(3, seed + 9 + i, 0.08).map(([u, v]) => ({ kind: 'fungus', u, v, rmax: 6, t0: 10, tau: 20, col: 'rgba(60,90,60,0.95)', seed: 1 }))); });
  }
  let incClock = null; let incDone = false;
  const stepInc = {
    title: 'Incubate for 48 hours', text: 'Tap the plates to put them, upside down, in the incubator at 30 °C, then run the clock.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([1.4, 1.9, 3.0], [1.4, 0.5, 0.2], 3.6),
    enter() { seedColonies(); },
    skip() { plates.forEach((p) => p.setTime(48)); },
    handler: { down() {
      if (incClock || !input.pick(plates.map((p) => p.group), true)) return false;
      sfx.play('door'); inc.open(1); plates.forEach((p, i) => { const from = p.group.position.clone(); const to = new THREE.Vector3(2.65 + i * 0.25, 0.4, 0.4 - i * 0.12); anim.add(1.0, (k) => { p.group.position.lerpVectors(from, to, k); p.group.position.y += Math.sin(Math.PI * k) * 0.5; p.group.scale.setScalar(1 - k * 0.6); }, { done: () => { p.group.visible = false; p.group.position.copy(from); p.group.scale.setScalar(1); } }); });
      anim.wait(1.2, () => { inc.open(0); incClock = timelapse(ctx, { step: 12, unit: 'h', onTick: (h, done) => { plates.forEach((p) => p.setTime(h)); if (done && h >= 48 && !incDone) { incDone = true; incClock.show(false); plates.forEach((p) => { p.group.visible = true; }); ctx.next('48 hours: colonies have grown where single cells (or spores) landed.'); } } }); });
      return true;
    } },
    exit() { if (incClock) { incClock.remove(); incClock = null; } plates.forEach((p) => { p.group.visible = true; }); },
  };
  const stepChoose = {
    title: 'Which plate do you count?', text: 'Look at the three plates.', tool: null, autoTool: 'hand', hideBelt: true, shot: S_PLATES,
    enter() {
      const n3 = plates[0].visible().length; const n4 = plates[1].visible().length; const nc = plates[2].visible().length;
      ui.observe('Plate 10⁻³', `${n3 > 30 ? '30–300' : 'few'} colonies`); ui.observe('Plate 10⁻⁴', `${n4} colonies`); ui.observe('Control', nc ? `${nc} contaminants` : 'no growth');
      ask(ctx, 'Count the plate with…', [{ label: '30 to 300 colonies (10⁻³)', value: 0 }, { label: 'The fewest colonies (10⁻⁴)', value: 1 }, { label: 'The control', value: 2 }], 0, { wrong: (v) => (v === 1 ? 'Fewer than 30 colonies give a statistically unreliable count.' : 'The control only checks sterility.'), ok: nc ? 'The 10⁻³ plate. (Growth on the control shows contamination — in a real lab you would repeat.)' : 'The 10⁻³ plate: between 30 and 300 colonies, separate and countable. The clear control shows the technique was sterile.' });
    },
    exit() { ui.clearChooser(); chosen = plates[0]; },
  };
  const stepCount = {
    title: 'Count the colonies', text: 'With the <b>marker pen</b>, put a dot on every colony on the 10⁻³ plate (tap each one). Then press Done.', tool: 'marker', autoTool: 'marker', hideBelt: true, shot: PLATE_TOP(plates[0]),
    aim(p, out) { const h = input.pick([plates[0].agar], false, false); if (h) return out.copy(h.point); return ctx.aimDefault(p, out); },
    enter() { chosen = plates[0]; marked = new Set(); count = 0; hud.actions([{ id: 'd', label: 'Done counting', primary: true, onClick: () => this.done() }]); },
    done() {
      const all = plates[0].visible(); const missed = all.filter((c) => !marked.has(c));
      if (missed.length > Math.max(1, all.length * 0.04)) { ctx.mistake(`About ${missed.length} colonies have no dot yet. Work across the plate in strips so none is missed.`, 2); return; }
      count = marked.size; ui.observe('Colonies counted', String(count)); hud.actions([]); ctx.next(`${count} colonies on the 10⁻³ plate.`);
    },
    exit() { hud.actions([]); },
    skip() { count = plates[0].visible().length; ui.observe('Colonies counted', String(count)); },
    handler: { down() {
      const h = input.pick([plates[0].agar], false, false); if (!h) return false; if (!ctx.requireTool('marker')) return true;
      const c = plates[0].colonyAt(h.uv); if (!c) { ctx.say('No colony there.', 'hint', 900); return true; }
      if (marked.has(c)) { ctx.say('Already marked — counting it twice would inflate the result.', 'hint', 1400); return true; }
      marked.add(c); plates[0].mark(c.u + 0.012, c.v - 0.012); sfx.play('click'); ui.setText(`Marked: <b>${marked.size}</b>. Tap every colony, then press Done.`); return true;
    } },
  };
  const stepKinds = {
    title: 'Bacteria, moulds and actinomycetes', text: 'Tap a <b>mould</b> (fungal) colony on the plate.', tool: null, autoTool: 'hand', hideBelt: true, shot: PLATE_TOP(plates[0]),
    enter() { this.want = 'fungus'; },
    handler: { down() {
      const h = input.pick([plates[0].agar], false, false); if (!h) return false; const c = plates[0].colonyAt(h.uv); if (!c) return true;
      const W = { fungus: 'a mould', actino: 'an actinomycete', bacterium: 'a bacterial colony' };
      if (c.kind !== this.want) { ctx.mistake(`That is ${W[c.kind]}. ${this.want === 'fungus' ? 'Moulds are large, fuzzy and cottony with a spreading edge.' : 'Actinomycetes are small, dry, chalky-white and stick firmly to the agar.'}`, 1); return true; }
      sfx.play('ok');
      if (this.want === 'fungus') { this.want = 'actino'; ui.setText('Good. Now tap an <b>actinomycete</b> colony: small, chalky, powdery.'); ctx.say('Mould: a mycelium of hyphae spreading out from one spore, fuzzy and often coloured by spores.', 'good', 3600); }
      else ctx.next('Bacterial colonies are smooth, moist, round and shiny; actinomycetes (which give soil its earthy smell) are dry and chalky; moulds are fuzzy.');
      return true;
    } },
  };
  const stepCFU = {
    title: 'Colony-forming units per gram', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: S_PLATES,
    enter() {
      const right = count * 1e4; const fmt = (v) => `${(v / 10 ** Math.floor(Math.log10(v))).toFixed(2)} × 10^${Math.floor(Math.log10(v))}`.replace(/\^(\d+)/, (m, d) => `<sup>${d}</sup>`);
      const plain = (v) => { const e = Math.floor(Math.log10(v)); return `${(v / 10 ** e).toFixed(2)} × 10${String(e).replace(/\d/g, (d) => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d])}`; };
      void fmt;
      ui.setText(`CFU per g = colonies ÷ (volume plated × dilution) = ${count} ÷ (0.1 mL × 10⁻³)`);
      const opts = [right, count * 1e3, count * 1e5, count * 10].map((v) => ({ label: `${plain(v)} CFU/g`, value: v }));
      ask(ctx, 'Colony-forming units per gram of soil', opts.sort(() => R() - 0.5), right, { y: 0.08, wrong: 'Dividing by 0.1 mL multiplies by 10; dividing by 10⁻³ multiplies by 1000.', ok: `${plain(right)} CFU per gram of soil (true value in this sample ${plain(cfuTrue)}).` });
      res.cfu = right; res.plain = plain;
    },
    exit() { ui.clearChooser(); },
  };
  const res = {};
  const steps = [stepLamp, stepSoil, stepDilute, stepPour, stepInoc, spreadStep(0), spreadStep(1), stepInc, stepChoose, stepCount, stepKinds, stepCFU];
  ctx.debug = { plates, tubes, get marked() { return marked; } };
  void ease;
  return {
    tools: ['hand', 'dropper', 'spreader', 'marker'],
    steps,
    update(dt) { if (spreaderHot > 0) spreaderHot = Math.max(0, spreaderHot - dt * 0.5); hud.update(); },
    result() {
      const plain = res.plain || ((v) => v.toExponential(2)); const cfu = res.cfu || count * 1e4; const err = Math.abs(cfu - cfuTrue) / cfuTrue * 100;
      return { title: 'Soil microorganisms by dilution plating', rows: [['Colonies on 10⁻³ plate', String(count)], ['CFU per g of soil', `${plain(cfu)} (true ${plain(cfuTrue)}, ${err.toFixed(0)} % off)`], ['Control plate', plates[2].visible().length ? 'contaminated' : 'no growth (sterile)']], conclusion: 'Soil holds hundreds of thousands to millions of living microbes per gram — mostly bacteria, with actinomycetes and moulds. Serial dilution spreads them thin enough that each colony grows from a single cell or spore, so colonies × dilution factor ÷ volume plated estimates the colony-forming units per gram. Aseptic technique (flame, alcohol, control plate) keeps outside microbes from spoiling the count.' };
    },
    dispose() { plates.forEach((p) => p.dispose()); hud.dispose(); ui.clearChooser(); },
  };
}
