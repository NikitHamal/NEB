// Soil from two sites — A, garden soil under trees; B, roadside soil — compared for moisture,
// water-holding capacity, pH, texture and humus. Weigh the fresh soil, dry it at 105 °C and
// reweigh until the mass is constant; pour 100 mL of water through 50 g of dry soil in a funnel
// and read what drains through; dip pH paper in a 1 : 2.5 soil suspension and match the colour;
// shake soil in water, let the particles settle into sand, silt and clay and measure the layers;
// and drop hydrogen peroxide on each to see the humus fizz. Every figure comes from the student's
// own readings.
import { THREE } from '../../engine.js';
import { watchGlass, reagentBottle } from '../props.js';
import { makeTube, makeRack } from '../glassware.js';
import { incubator } from '../specimens/microbe.js';
import { crucible, glassBeaker, timelapse, ask, sheet, table, tag, soilTexture } from '../bench.js';
import { mesh, MAT, rng, clamp, canvasTexture } from '../kit.js';
import { balance as makeBalance } from '../../handson/thermo.js';
import { measuringCylinder } from '../../handson/vessels.js';
import { funnel } from '../../handson/glass.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const PH_COL = { 4: '#e5482b', 5: '#f08a24', 6: '#f2c83a', 7: '#5bbf3a', 8: '#1f9d8a', 9: '#2b6cb0' };
function texClass(sa, si, cl) { if (cl >= 40) return 'Clay'; if (si >= 50 && cl < 27) return 'Silt loam'; if (sa >= 70 && cl < 15) return 'Loamy sand'; if (sa > 52 && cl < 20) return 'Sandy loam'; if (cl >= 27) return 'Clay loam'; return 'Loam'; }

export function create(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const R = rng((Date.now() & 0xffff) || 29);
  const hud = createHud(ctx); const balChip = hud.chip('ho-chip-read');
  const SITES = [
    { id: 'A', name: 'A: garden, under trees', tint: '#3d2a1c', m: 0.18 + R() * 0.06, whc: 0.46 + R() * 0.1, pH: 6.1 + R() * 0.7, tex: [38 + R() * 8, 38 + R() * 6], humus: 1 },
    { id: 'B', name: 'B: roadside', tint: '#9a7b56', m: 0.05 + R() * 0.03, whc: 0.21 + R() * 0.07, pH: 7.6 + R() * 0.6, tex: [76 + R() * 6, 11 + R() * 4], humus: 0.15 },
  ];
  SITES.forEach((s) => { s.tex.push(100 - s.tex[0] - s.tex[1]); s.W1 = +(20 + (R() - 0.5) * 0.4).toFixed(2); s.W2 = +(s.W1 * (1 - s.m)).toFixed(2); });
  const bal = makeBalance(); bal.group.position.set(1.6, 0, 0.6); world.add(bal.group);
  const oven = incubator('105 °C'); oven.group.position.set(2.9, 0, -0.7); oven.group.rotation.y = -0.5; world.add(oven.group);
  const ovT = tag('hot-air oven', { h: 0.08 }); ovT.position.set(2.9, 1.5, -0.7); world.add(ovT);
  const crus = SITES.map((s, i) => { const c = crucible(0.17); c.position.set(0.55 + i * 0.45, 0, 0.75); c.userData.fill.visible = true; c.userData.fill.material = new THREE.MeshStandardMaterial({ map: soilTexture(s.tint), roughness: 1 }); world.add(c); const t = tag(s.id, { h: 0.07 }); t.position.set(0, 0.32, 0); c.add(t); c.userData.home = c.position.clone(); return c; });
  // water-holding capacity: two funnels on measuring cylinders
  const cyl = SITES.map((s, i) => { const m = measuringCylinder({ cap: 100, color: 0xc9b48a }); m.group.position.set(-2.2 + i * 0.7, 0, -0.35); world.add(m.group); const f = funnel(); f.position.set(0, m.topY - 0.05, 0); m.group.add(f); const soilC = mesh(new THREE.ConeGeometry(0.2, 0.18, 24, 1, true), new THREE.MeshStandardMaterial({ map: soilTexture(s.tint), roughness: 1, side: THREE.DoubleSide }), [0, m.topY + 0.38, 0]); soilC.rotation.x = Math.PI; m.group.add(soilC); const t = tag(s.id, { h: 0.08 }); t.position.set(0, m.topY + 0.72, 0); m.group.add(t); return Object.assign(m, { reader: m.reader(ctx), read: null }); });
  const jug = glassBeaker(0.24, 0.55, 0xcfe8f5, 0.75); jug.group.position.set(-1.85, 0, 0.55); world.add(jug.group); const jT = tag('water 100 mL ×2', { h: 0.06 }); jT.position.set(-1.85, 0.7, 0.55); world.add(jT);
  // pH: suspension tubes and paper
  const rack = makeRack(2); rack.group.position.set(-0.6, 0, 0.7); world.add(rack.group);
  const tubes = SITES.map((s, i) => { const t = makeTube(s.id, { color: s.id === 'A' ? 0x6b5440 : 0xb59a76, fill: 0.5 }); t.group.position.copy(rack.slots[i]); rack.group.add(t.group); t.material.opacity = 0.85; return t; });
  const phBook = new THREE.Group(); phBook.position.set(0.0, 0, 0.95); world.add(phBook);
  phBook.add(mesh(new THREE.BoxGeometry(0.3, 0.03, 0.2), MAT.gloss(0x1e3a8a), [0, 0.015, 0]));
  const phT = tag('pH paper', { h: 0.055 }); phT.position.set(0, 0.16, 0); phBook.add(phT);
  const strips = SITES.map((s, i) => { const m = mesh(new THREE.BoxGeometry(0.03, 0.002, 0.16), new THREE.MeshStandardMaterial({ color: 0xf5e6a8, roughness: 0.9 }), [0.05 + i * 0.05, 0.035, 0]); phBook.add(m); return m; });
  // texture jars
  const jars = SITES.map((s, i) => {
    const j = glassBeaker(0.22, 0.95, 0x9a7b56, 0.25); j.group.position.set(0.55 + i * 0.6, 0, -0.85); world.add(j.group); j.material.opacity = 0.75;
    const layers = [0, 1, 2].map((k) => { const m = mesh(new THREE.CylinderGeometry(0.212, 0.212, 1, 28), new THREE.MeshStandardMaterial({ color: [0xd8c08c, 0x8c7a62, 0x5b4636][k], roughness: 0.95 }), null); m.visible = false; j.group.add(m); return m; });
    const sc = mesh(new THREE.PlaneGeometry(0.06, 0.8), new THREE.MeshBasicMaterial({ map: canvasTexture('soil-jar-scale', 64, 1024, (g, w, h) => { g.fillStyle = '#fbfaf3'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827'; for (let mm = 0; mm <= 80; mm++) { const y = h - mm * h / 80; g.fillRect(0, y - 1.5, mm % 10 === 0 ? 40 : mm % 5 === 0 ? 28 : 16, 3); if (mm % 10 === 0 && mm) { g.font = '700 22px system-ui'; g.fillText(String(mm), 34, y + 8); } } }) }), [0.27, 0.4 + 0.012, 0.0]); j.group.add(sc);
    const t = tag(s.id, { h: 0.08 }); t.position.set(0, 1.1, 0); j.group.add(t);
    return Object.assign(j, { layers, settled: 0, scale: sc, reads: [] });
  });
  const h2o2 = reagentBottle('H₂O₂', 0xf1f5f9, '6%'); h2o2.position.set(-0.75, 0, -0.45); world.add(h2o2);
  const wg = SITES.map((s, i) => { const w = watchGlass(); w.position.set(-0.3 + i * 0.45, 0, -0.25); world.add(w); const heap = mesh(new THREE.SphereGeometry(0.15, 14, 8), new THREE.MeshStandardMaterial({ map: soilTexture(s.tint), roughness: 1 }), [0, 0.04, 0]); heap.scale.y = 0.35; w.add(heap); const t = tag(s.id, { h: 0.06 }); t.position.set(0, 0.2, 0); w.add(t); return w; });
  const foam = []; const tmp = new THREE.Vector3();
  const rec = { W1: {}, W2: {}, mass: { A: [], B: [] }, V: {}, pH: {}, tex: { A: [], B: [] } };
  const BAL = S([1.2, 1.7, 2.5], [1.2, 0.2, 0.65], 2.2);
  const CYL = S([-1.85, 2.0, 2.2], [-1.85, 1.0, -0.35], 2.0, 2.4);
  const PH = S([-0.25, 1.4, 2.0], [-0.25, 0.4, 0.75], 1.6);
  const JAR = S([0.85, 1.3, 1.1], [0.85, 0.45, -0.85], 1.7, 1.2);
  const HUM = S([-0.15, 2.0, 0.85], [-0.1, 0.1, -0.3], 1.5);

  function onPan(c, on, done) {
    const to = on ? new THREE.Vector3(bal.group.position.x, bal.panY, bal.group.position.z - 0.08) : c.userData.home;
    const from = c.position.clone(); sfx.play('pick');
    anim.add(0.6, (k) => { c.position.lerpVectors(from, to, k); c.position.y += Math.sin(Math.PI * k) * 0.25; }, { done: () => { sfx.play('place'); if (done) done(); } });
  }
  const stepWeigh = {
    title: 'Weigh the fresh soil', text: 'The balance has been tared with an empty crucible. Tap crucible <b>A</b> to weigh it, tap it again to take it off, then do <b>B</b>.', tool: null, autoTool: 'hand', shot: BAL,
    skip() { SITES.forEach((s) => { rec.W1[s.id] = s.W1; ui.observe(`Fresh soil ${s.id}`, `${s.W1.toFixed(2)} g`); }); },
    handler: { down() {
      const i = crus.findIndex((c) => input.pick([c], true)); if (i < 0) return false; const c = crus[i]; const s = SITES[i];
      if (this.on === c) { bal.set(0); onPan(c, false, () => { this.on = null; if (Object.keys(rec.W1).length === 2) ctx.next(); }); return true; }
      if (this.on) { ctx.say('Take the other crucible off the pan first.', 'hint', 1500); return true; }
      this.on = c; onPan(c, true, () => { bal.set(s.W1); anim.wait(1.0, () => { rec.W1[s.id] = s.W1; ui.observe(`Fresh soil ${s.id}`, `${s.W1.toFixed(2)} g`); }); }); return true;
    } },
  };
  let hours = 0; let ovenClock = null;
  const massAt = (s, h) => +(s.W2 + (s.W1 - s.W2) * Math.exp(-h / 1.4)).toFixed(2);
  const stepOven = {
    title: 'Dry to constant mass at 105 °C', text: 'Both crucibles are in the oven. Run the clock 2 hours, then press <b>Weigh</b>. Repeat until two weighings agree — that is constant mass.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([2.0, 1.8, 2.6], [2.0, 0.5, 0.1], 3.0),
    enter() {
      oven.open(0.6); crus.forEach((c, i) => { c.position.set(2.7 + i * 0.2, 0.4, -0.5); }); anim.wait(0.8, () => oven.open(0));
      ovenClock = timelapse(ctx, { step: 2, unit: 'h', onTick: (h, done) => { hours = h; if (done) { ovenClock.enable(false); hud.enable('w', true); } } });
      hud.actions([{ id: 'w', label: 'Weigh', primary: true, disabled: true, onClick: () => { SITES.forEach((s) => { const m = massAt(s, hours); rec.mass[s.id].push([hours, m]); ui.observe(`${s.id} after ${hours} h`, `${m.toFixed(2)} g`); }); sfx.play('place'); hud.enable('w', false); ovenClock.enable(true); } }, { id: 'c', label: 'Constant mass reached', onClick: () => {
        const ok = SITES.every((s) => { const m = rec.mass[s.id]; return m.length >= 2 && Math.abs(m[m.length - 1][1] - m[m.length - 2][1]) <= 0.01; });
        if (!ok) { ctx.mistake('Not yet: the last two weighings must agree (within 0.01 g). Water is still leaving the soil.', 2); return; }
        SITES.forEach((s) => { rec.W2[s.id] = rec.mass[s.id][rec.mass[s.id].length - 1][1]; }); hud.actions([]); ctx.next('Constant mass: all the water has gone.');
      } }]);
    },
    skip() { SITES.forEach((s) => { rec.W2[s.id] = s.W2; rec.mass[s.id].push([8, s.W2]); }); },
    exit() { if (ovenClock) ovenClock.remove(); ovenClock = null; hud.actions([]); crus.forEach((c) => c.position.copy(c.userData.home)); },
  };
  const stepMoist = {
    title: 'Moisture content', text: 'Moisture % = (fresh mass − dry mass) ÷ fresh mass × 100.', tool: null, autoTool: 'hand', hideBelt: true, shot: BAL,
    enter() {
      const m = (id) => (rec.W1[id] - rec.W2[id]) / rec.W1[id] * 100; const right = Math.round(m('A') * 10) / 10;
      ask(ctx, `Soil A: (${rec.W1.A.toFixed(2)} − ${rec.W2.A.toFixed(2)}) ÷ ${rec.W1.A.toFixed(2)} × 100 =`, [right, Math.round((rec.W1.A - rec.W2.A) / rec.W2.A * 1000) / 10, Math.round(rec.W2.A / rec.W1.A * 1000) / 10, Math.round(m('B') * 10) / 10].filter((v, i, a) => a.indexOf(v) === i).sort(() => R() - 0.5).map((v) => ({ label: `${v} %`, value: v })), right, { wrong: 'Water lost = fresh − dry; divide by the fresh mass.', ok: `A holds ${right} % water, B only ${(Math.round(m('B') * 10) / 10)} %.`, then() { ui.observe('Moisture A / B', `${right} % / ${Math.round(m('B') * 10) / 10} %`); ctx.next(); } });
    },
    exit() { ui.clearChooser(); },
  };
  let poured = 0; let whcClock = null;
  const stepWHC = {
    title: 'Water-holding capacity', text: 'Each funnel holds 50 g of oven-dry soil on filter paper. Tap the water jug, then a funnel, to pour 100 mL onto each soil.', tool: null, autoTool: 'hand', shot: CYL,
    skip() { SITES.forEach((s, i) => { cyl[i].set(100 - s.whc * 50); }); poured = 2; },
    handler: { down() {
      if (input.pick([jug.group], true)) { this.ready = true; sfx.play('glass'); return true; }
      const i = cyl.findIndex((c) => input.pick([c.group], true)); if (i < 0) return false;
      if (!this.ready) { ctx.say('Tap the water jug first.', 'hint', 1400); return true; }
      if (cyl[i].poured) return true; this.ready = false; cyl[i].poured = true; poured += 1; sfx.play('pour');
      if (poured === 2) { anim.wait(0.6, () => { whcClock = timelapse(ctx, { step: 10, unit: 'min', onTick: (m, done) => { SITES.forEach((s, k) => { cyl[k].set((100 - s.whc * 50) * clamp(1 - Math.exp(-m / 6))); }); if (done && m >= 30) { whcClock.remove(); whcClock = null; ctx.next('Dripping has stopped.'); } } }); }); }
      return true;
    } },
    exit() { if (whcClock) whcClock.remove(); whcClock = null; },
  };
  const stepReadCyl = {
    title: 'Read the drained water', text: 'Tap each measuring cylinder at the bottom of the meniscus to read how much water drained through.', tool: null, autoTool: 'hand', hideBelt: true, shot: CYL,
    skip() { SITES.forEach((s, i) => { rec.V[s.id] = Math.round((100 - s.whc * 50) * 2) / 2; }); },
    handler: { down() {
      const i = cyl.findIndex((c) => input.pick([c.group], true)); if (i < 0) return false; const v = cyl[i].reader.tap(); if (v === null) return true;
      const truth = cyl[i].volume; if (Math.abs(v - truth) > 1) { ctx.mistake(`Read again at eye level, at the bottom of the meniscus (you read ${v} mL).`, 2); return true; }
      rec.V[SITES[i].id] = v; sfx.play('ok'); ui.observe(`Drained ${SITES[i].id}`, `${v} mL`);
      if (rec.V.A !== undefined && rec.V.B !== undefined) { const w = (id) => (100 - rec.V[id]) / 50 * 100; ui.observe('WHC A / B', `${w('A').toFixed(0)} % / ${w('B').toFixed(0)} %`); ctx.next(`WHC = water retained ÷ dry soil × 100: A ${w('A').toFixed(0)} %, B ${w('B').toFixed(0)} %.`); }
      return true;
    } },
  };
  let phNext = 0;
  const stepPH = {
    title: 'Soil pH', text: 'With the <b>forceps</b>, take a strip of pH paper and dip it in suspension <b>A</b> (tap the strip, then the tube); then a fresh strip in <b>B</b>.', tool: 'forceps', shot: PH,
    skip() { SITES.forEach((s) => { rec.pH[s.id] = Math.round(s.pH); }); },
    handler: { down() {
      const si = strips.findIndex((m) => m.visible && input.pick([m, phBook], true));
      if (si >= 0 && !this.holding) { if (!ctx.requireTool('forceps', 'Hold pH paper with <b>forceps</b>: fingers are acidic with sweat.')) return true; this.holding = true; strips[si].visible = false; sfx.play('pick'); return true; }
      const i = tubes.findIndex((t) => input.pick([t.group], true)); if (i < 0) return false;
      if (!this.holding) { ctx.say('Take a pH strip first.', 'hint', 1300); return true; }
      if (i !== phNext) { ctx.say(`Do tube ${SITES[phNext].id} now.`, 'hint', 1300); return true; }
      this.holding = false; sfx.play('drop'); const s = SITES[i]; const col = PH_COL[Math.round(s.pH)];
      const card = sheet(ctx, { title: `pH paper in suspension ${s.id}` }); card.set(`<div style="display:flex;gap:8px;align-items:center"><span style="width:26px;height:70px;border-radius:4px;background:${col};box-shadow:inset 0 0 0 1px rgba(0,0,0,.2)"></span><div style="display:flex;gap:3px">${Object.entries(PH_COL).map(([p, c]) => `<span style="text-align:center;font-size:.7rem"><i style="display:block;width:30px;height:30px;border-radius:4px;background:${c}"></i>${p}</span>`).join('')}</div></div>`);
      ask(ctx, `Match the strip for ${s.id}: pH ≈`, Object.keys(PH_COL).map((p) => ({ label: p, value: +p })), Math.round(s.pH), { delay: 0.4, wrong: 'Compare the strip with the colour chart under good light.', then() { card.remove(); rec.pH[s.id] = Math.round(s.pH); ui.observe(`pH ${s.id}`, String(Math.round(s.pH))); phNext += 1; if (phNext === 2) ctx.next(`A is ${s.pH < 7 && SITES[0].pH < 7 ? 'slightly acidic' : 'near neutral'} (humus and leaf litter), B alkaline (dust, cement and little organic matter).`); } });
      return true;
    } },
    exit() { ui.clearChooser(); ctx.ui.root.querySelectorAll('.bh-sheet').forEach((n) => n.remove()); },
  };
  let jarClock = null;
  function setJar(j, s, k) {
    const H = 0.62; let y = 0.02; const tot = 100;
    s.tex.forEach((p, q) => { const h = H * p / tot * k; const m = j.layers[q]; m.visible = h > 0.002; m.scale.y = Math.max(0.001, h); m.position.y = y + h / 2; y += h; });
    j.material.opacity = 0.75 - 0.5 * k; j.material.color.set(s.id === 'A' ? 0x9a8a72 : 0xbfae90).lerp(new THREE.Color(0xcfe2ea), k);
  }
  const stepShake = {
    title: 'Texture: shake and settle', text: 'Each jar holds soil, water and a pinch of dispersing salt. Tap each jar to shake it hard, then run the clock while the particles settle.', tool: null, autoTool: 'hand', hideBelt: true, shot: JAR,
    enter() { this.shaken = new Set(); },
    skip() { jars.forEach((j, i) => setJar(j, SITES[i], 1)); },
    handler: { down() {
      const i = jars.findIndex((j) => input.pick([j.group], true)); if (i < 0) return false; const st = stepShake; if (st.shaken.has(i)) return true;
      st.shaken.add(i); sfx.play('pour'); anim.add(0.8, (k) => { jars[i].group.rotation.z = Math.sin(k * Math.PI * 8) * 0.2; }, { done: () => { jars[i].group.rotation.z = 0; } });
      if (st.shaken.size === 2) anim.wait(1, () => { jarClock = timelapse(ctx, { step: 6, unit: 'h', onTick: (h, done) => { const k = clamp(h / 24); jars.forEach((j, q) => setJar(j, SITES[q], k)); if (done && h >= 24) { jarClock.remove(); jarClock = null; ctx.next('Settled: sand at the bottom (falls first), then silt, then clay on top; the water has cleared.'); } } }); });
      return true;
    } },
    exit() { if (jarClock) jarClock.remove(); jarClock = null; },
  };
  const BOUND = ['top of the sand', 'top of the silt', 'top of the clay'];
  const stepLayers = {
    title: 'Measure the layers of jar A', text: 'Tap the scale at the <b>top of the sand</b> layer of jar A.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0.72, 0.62, 0.15], [0.66, 0.36, -0.85], 0.75, 0.75),
    skip() { SITES.forEach((s) => { let c = 0; rec.tex[s.id] = s.tex.map((p) => Math.round((c += p * 0.62) * 2) / 2); }); },
    handler: { down() {
      const j = jars[0]; const plane = new THREE.Plane(); j.scale.getWorldPosition(tmp); plane.setFromNormalAndCoplanarPoint(new THREE.Vector3(0, 0, 1), tmp);
      const hit = input.ptr.ray.intersectPlane(plane, new THREE.Vector3()); if (!hit) return false; j.group.worldToLocal(hit); if (hit.x < -0.3 || hit.x > 0.4) return false;
      const mm = Math.round((hit.y - 0.012) / 0.8 * 80 * 2) / 2; const k = rec.tex.A.length; const s = SITES[0];
      const truth = s.tex.slice(0, k + 1).reduce((a, p) => a + p, 0) * 0.62 / 100 * 100;
      if (Math.abs(mm - truth) > 2) { ctx.mistake(`Look again for the ${BOUND[k]}: that tap is ${mm} mm, the boundary is near ${Math.round(truth / 5) * 5} mm.`, 1); return true; }
      rec.tex.A.push(mm); sfx.play('ok'); ui.observe(`Jar A, ${BOUND[k]}`, `${mm} mm`);
      if (rec.tex.A.length < 3) { ui.setText(`Now tap the scale at the <b>${BOUND[rec.tex.A.length]}</b>.`); return true; }
      let c = 0; rec.tex.B = SITES[1].tex.map((p) => Math.round((c += p * 0.62) * 2) / 2);
      ctx.next(); return true;
    } },
  };
  const stepTexture = {
    title: 'Classify the texture', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: JAR,
    enter() {
      const pct = (arr) => { const [a, b, c] = arr; return [a / c * 100, (b - a) / c * 100, (c - b) / c * 100]; };
      const A = pct(rec.tex.A); const B = pct(rec.tex.B); res.A = A; res.B = B;
      const sh2 = sheet(ctx, { title: 'Particle sizes (% of sediment)' }); res.sh = sh2;
      sh2.set(table(['Soil', 'Sand', 'Silt', 'Clay'], [['A', ...A.map((v) => v.toFixed(0))], ['B (same method)', ...B.map((v) => v.toFixed(0))]]));
      const right = texClass(...A);
      ask(ctx, `Soil A — sand ${A[0].toFixed(0)} %, silt ${A[1].toFixed(0)} %, clay ${A[2].toFixed(0)} % — is a…`, ['Loam', 'Sandy loam', 'Loamy sand', 'Clay', 'Silt loam'].map((v) => ({ label: v, value: v })), right, { y: 0.06, wrong: 'Use the texture triangle: a loam has sand, silt and clay in balance (clay about 7–27 %); sandy soils are mostly sand.', ok: `${right}. Soil B (${texClass(...B).toLowerCase()}) is much sandier.`, then() { ui.observe('Texture A / B', `${right} / ${texClass(...B)}`); ctx.next(); } });
    },
    exit() { ui.clearChooser(); if (res.sh) res.sh.remove(); },
  };
  const res = {};
  const stepHumus = {
    title: 'Humus: hydrogen peroxide test', text: 'Fill the <b>dropper</b> with H₂O₂ and add a few drops to each soil sample. Organic matter (humus) froths as H₂O₂ breaks down.', tool: 'dropper', shot: HUM,
    skip() { },
    handler: { down() {
      if (input.pick([h2o2], true)) { if (!ctx.requireTool('dropper')) return true; this.loaded = true; sfx.play('pick'); return true; }
      const i = wg.findIndex((w) => input.pick([w], true)); if (i < 0) return false; if (!ctx.requireTool('dropper')) return true;
      if (!this.loaded) { ctx.say('Fill the dropper from the H₂O₂ bottle.', 'hint', 1400); return true; }
      this.loaded = false; sfx.play('drip'); fizz(wg[i], SITES[i].humus); (this.done2 = this.done2 || new Set()).add(i);
      if (this.done2.size === 2) anim.wait(1.8, () => ask(ctx, 'Which soil has more humus?', [{ label: 'A (vigorous froth)', value: 'A' }, { label: 'B (a few bubbles)', value: 'B' }], 'A', { delay: 0.1, ok: 'A: the dark garden soil under trees, rich in decaying leaves. Humus binds particles into crumbs, holds water and nutrients and lowers pH slightly.', wrong: 'Watch which one frothed up.' }));
      return true;
    } },
    exit() { ui.clearChooser(); },
  };
  function fizz(w, k) {
    const n = Math.round(4 + k * 24);
    for (let q = 0; q < n; q++) { const b = mesh(new THREE.SphereGeometry(0.012 + Math.random() * 0.012, 8, 6), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.85, roughness: 0.1 }), [(Math.random() - 0.5) * 0.22, 0.05 + Math.random() * 0.06 * k, (Math.random() - 0.5) * 0.22]); b.scale.setScalar(0.01); w.add(b); foam.push(b); anim.add(0.6 + Math.random(), (t) => b.scale.setScalar(t), { delay: Math.random() * 0.8 }); }
  }
  const stepRelate = {
    title: 'Soil and vegetation', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0.2, 2.4, 3.4], [-0.2, 0.5, -0.1], 4.6),
    enter() { ask(ctx, 'Why does site A carry thick vegetation and site B only sparse weeds?', [{ label: 'A holds more water and humus, with a loam texture and slightly acid pH', value: 'ok' }, { label: 'B has more clay, which plants dislike', value: 'c' }, { label: 'Soil has no effect on vegetation', value: 'n' }], 'ok', { ok: 'Moisture, water-holding capacity, humus, texture and pH all favour plant growth at A; the sandy, alkaline, humus-poor soil of B dries out fast and supports only hardy weeds — and the vegetation in turn adds humus to the soil.', wrong: 'Look back at your table: which soil held more water and organic matter?' }); },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepWeigh, stepOven, stepMoist, stepWHC, stepReadCyl, stepPH, stepShake, stepLayers, stepTexture, stepHumus, stepRelate];
  ctx.debug = { cyl, jars, crus, rec, SITES };
  return {
    tools: ['hand', 'forceps', 'dropper'],
    steps,
    update(dt) {
      bal.update(dt); bal.display.getWorldPosition(balChip.at); balChip.set(`<b>${bal.shown.toFixed(2)}</b> g`).show(ctx.stepIndex === 0); hud.update();
    },
    result() {
      const m = (id) => (rec.W1[id] && rec.W2[id] ? ((rec.W1[id] - rec.W2[id]) / rec.W1[id] * 100).toFixed(1) : '—'); const w = (id) => (rec.V[id] !== undefined ? ((100 - rec.V[id]) / 50 * 100).toFixed(0) : '—');
      return { title: 'Soil analysis of two sites', rows: [['Moisture A / B', `${m('A')} % / ${m('B')} % (true ${(SITES[0].m * 100).toFixed(1)} / ${(SITES[1].m * 100).toFixed(1)})`], ['WHC A / B', `${w('A')} % / ${w('B')} % (true ${(SITES[0].whc * 100).toFixed(0)} / ${(SITES[1].whc * 100).toFixed(0)})`], ['pH A / B', `${rec.pH.A ?? '—'} / ${rec.pH.B ?? '—'}`], ['Texture A / B', res.A ? `${texClass(...res.A)} / ${texClass(...res.B)}` : '—'], ['Humus', 'A high, B low']], conclusion: 'The garden soil under trees (A) is a moist, humus-rich loam with high water-holding capacity and slightly acid pH; the roadside soil (B) is sandy, dry, alkaline and poor in humus. Such differences in the soil explain the difference in vegetation between the two sites.' };
    },
    dispose() { hud.dispose(); ui.clearChooser(); if (res.sh) res.sh.remove(); },
  };
}
