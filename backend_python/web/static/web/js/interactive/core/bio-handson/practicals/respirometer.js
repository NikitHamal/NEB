// Rate of respiration of germinating seeds with a simple respirometer. KOH solution at the bottom of
// a boiling tube absorbs the CO2 the seeds give out, so the oxygen they take in shows as a fall in
// gas volume: a coloured index drop in a capillary (2 mm bore) creeps toward the tube along a
// millimetre scale. The student pours KOH, sets the gauze, weighs 10 g of germinating seeds (and
// 10 g of boiled seeds for the control), fits the bungs, lets the tubes come to the water-bath
// temperature, introduces the index, then reads the scale every two minutes. The rate in
// µL O2 g⁻¹ min⁻¹ is worked out from the student's own readings.
import { THREE } from '../../engine.js';
import { reagentBottle } from '../props.js';
import { glassBeaker, timelapse, ask, sheet, table, tag, enamelTray } from '../bench.js';
import { mesh, MAT, canvasTexture, rng, wet, ease } from '../kit.js';
import { createHud } from '../../handson/hud.js';
import { createGraph, fitLine } from '../../handson/stopwatch.js';
import { balance as makeBalance } from '../../handson/thermo.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const BZ = -0.42; const BORE_R = 1.0; const AREA = Math.PI * BORE_R * BORE_R; // mm, mm²
const ROWS = [{ y: 1.478, label: 'germinating seeds' }, { y: 1.281, label: 'boiled seeds (control)' }];

function scaleTexture() {
  return canvasTexture('resp-scale', 2048, 512, (g, w, h) => {
    g.fillStyle = '#fbfaf3'; g.fillRect(0, 0, w, h);
    const px = (mm) => (mm + 8) / 166 * w; // board spans -8..158 mm
    ROWS.forEach((r, i) => {
      const yy = i === 0 ? 150 : 390; g.fillStyle = '#111827';
      for (let mm = 0; mm <= 150; mm++) { const t = mm % 10 === 0 ? 46 : mm % 5 === 0 ? 32 : 20; g.fillRect(px(mm) - 1.5, yy - 10 - t, 3, t); if (mm % 10 === 0) { g.font = '600 26px system-ui'; g.textAlign = 'center'; g.fillText(String(mm), px(mm), yy - 66); } }
      g.font = '700 30px system-ui'; g.textAlign = 'left'; g.fillStyle = '#166534'; g.fillText(`${r.label}  (mm)`, px(2), yy + 52);
    });
  });
}

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const R = rng((Date.now() & 0xffff) || 3);
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'Index movement', xLabel: 'time (min)', yLabel: 'distance moved (mm)' });
  graph.el.classList.add('ho-side', 'bh-under-clock');
  const mass = 10 + Math.round((R() - 0.5) * 40) / 100;
  const trueRate = 2.6 + R() * 0.8; // µL O2 g⁻¹ min⁻¹ at 25 °C
  const v = [trueRate * mass / AREA, 0.04 + R() * 0.05]; // mm min⁻¹ (control: a little thermal drift)
  const start = [135 + Math.round(R() * 8), 138 + Math.round(R() * 6)];

  const bath = glassBeaker(0.62, 1.0, 0xcfe8f5, 0.62); bath.group.position.set(-1.35, 0, -0.2); world.add(bath.group);
  const bathTag = tag('water bath 25 °C', { h: 0.09 }); bathTag.position.set(-1.35, 1.12, 0.25); world.add(bathTag);
  const tubes = [0, 1].map((i) => {
    const g = new THREE.Group(); g.position.set(-1.35, 0.08, i ? -0.38 : -0.02); world.add(g);
    const prof = [[0.001, 0], [0.08, 0.01], [0.115, 0.07], [0.125, 0.14], [0.125, 1.45], [0.135, 1.47]].map(([a, b]) => new THREE.Vector2(a, b));
    const glass = mesh(new THREE.LatheGeometry(prof, 28), MAT.glass(), null, { cast: false }); glass.renderOrder = 5; g.add(glass);
    const koh = mesh(new THREE.CylinderGeometry(0.112, 0.112, 1, 22), MAT.liquid(0xeef2ff, 0.65), [0, 0.05, 0], { cast: false }); koh.scale.y = 0.001; koh.visible = false; g.add(koh);
    const gauze = mesh(new THREE.CylinderGeometry(0.118, 0.118, 0.008, 22), new THREE.MeshStandardMaterial({ color: 0x9ca3af, metalness: 0.8, roughness: 0.5, wireframe: true }), [0, 1.9, 0]); gauze.visible = false; g.add(gauze);
    const seeds = new THREE.Group(); g.add(seeds);
    const sm = wet(i ? 0xc8b48a : 0xd8c66a, { roughness: 0.6, clearcoat: 0.3 });
    for (let k = 0; k < 26; k++) { const s = mesh(new THREE.SphereGeometry(0.035, 10, 8), sm, [(R() - 0.5) * 0.15, 0.32 + Math.floor(k / 6) * 0.06 + R() * 0.02, (R() - 0.5) * 0.15]); if (!i) { const r = mesh(new THREE.CylinderGeometry(0.006, 0.003, 0.06, 5), wet(0xfef3c7), [0, -0.04, 0]); r.rotation.z = R() * 2; s.add(r); } seeds.add(s); }
    seeds.visible = false;
    const bung = mesh(new THREE.CylinderGeometry(0.14, 0.115, 0.14, 22), MAT.gloss(0x7f1d1d), [0, 2.4, 0]); bung.visible = false; g.add(bung);
    const y = ROWS[i].y - 0.08; const zTo = BZ + 0.06 - g.position.z;
    const capPts = [[0, 1.4, 0], [0, y - 0.1, 0], [0.02, y - 0.02, zTo * 0.6], [0.12, y, zTo], [1.35 + 0.95, y, zTo]].map((p) => new THREE.Vector3(...p));
    const cap = mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(capPts, false, 'catmullrom', 0.1), 60, 0.018, 8, false), MAT.glassEdge(), null, { cast: false }); cap.visible = false; cap.renderOrder = 6; g.add(cap);
    const drop = mesh(new THREE.CylinderGeometry(0.011, 0.011, 0.045, 10), MAT.liquid(0xdc2626, 0.95), null, { cast: false }); drop.rotation.z = Math.PI / 2; drop.visible = false; drop.renderOrder = 7; world.add(drop);
    const label = tag(i ? 'B: boiled seeds' : 'A: germinating', { h: 0.09 }); label.position.set(-1.35 - 0.3, 1.1 + (i ? 0.1 : 0), i ? -0.4 : 0.1); world.add(label);
    return { g, koh, gauze, seeds, bung, cap, drop, kohLevel: 0, pos: start[i], reads: [] };
  });
  const board = new THREE.Group(); board.position.set(0.15, 0, BZ); world.add(board);
  const card = mesh(new THREE.PlaneGeometry(1.66, 0.42), new THREE.MeshStandardMaterial({ map: scaleTexture(), roughness: 0.8 }), [0, 1.395, -0.01]);
  board.add(card); board.add(mesh(new THREE.BoxGeometry(1.7, 0.46, 0.02), MAT.gloss(0x334155), [0, 1.395, -0.025]));
  [-0.8, 0.8].forEach((x) => board.add(mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.2, 10), MAT.steel(), [x, 0.6, -0.03])));
  board.add(mesh(new THREE.BoxGeometry(1.9, 0.03, 0.4), MAT.gloss(0x1f2937), [0, 0.015, -0.03]));
  const xOf = (mm) => board.position.x - 0.83 + (mm + 8) / 166 * 1.66;
  const mmOf = (x) => (x - board.position.x + 0.83) / 1.66 * 166 - 8;

  const bal = makeBalance(); bal.group.position.set(1.55, 0, 0.85); world.add(bal.group);
  const trays = [0, 1].map((i) => { const t = enamelTray(0.55, 0.4); t.position.set(i ? 0.25 : 0.85, 0, 1.0); t.scale.setScalar(1); world.add(t); const s = new THREE.Group(); for (let k = 0; k < 30; k++) s.add(mesh(new THREE.SphereGeometry(0.035, 8, 6), wet(i ? 0xc8b48a : 0xd8c66a, { roughness: 0.6 }), [(R() - 0.5) * 0.4, 0.04, (R() - 0.5) * 0.26])); t.add(s); const l = tag(i ? 'boiled seeds' : 'germinating seeds', { h: 0.06 }); l.position.set(0, 0.22, 0.2); t.add(l); return { t, s }; });
  const koh = reagentBottle('KOH', 0xeef2ff, '15% solution'); koh.position.set(-0.75, 0, 0.75); world.add(koh);
  const eosin = reagentBottle('Eosin', 0xdc2626, 'index liquid'); eosin.position.set(-0.35, 0, 0.75); world.add(eosin);
  const gauzeDish = new THREE.Group(); gauzeDish.position.set(-1.25, 0, 0.75); world.add(gauzeDish);
  const gauzes = [0, 1].map((k) => { const m = mesh(new THREE.CylinderGeometry(0.118, 0.118, 0.008, 22), new THREE.MeshStandardMaterial({ color: 0x9ca3af, metalness: 0.8, roughness: 0.5, wireframe: true }), [k * 0.28 - 0.14, 0.01, 0]); gauzeDish.add(m); return m; });

  const tmp = new THREE.Vector3();
  const SET = S([0.1, 2.3, 3.4], [-0.2, 0.75, 0.1], 3.9);
  const TUBES = S([-0.6, 2.2, 2.6], [-1.0, 0.6, 0.25], 2.5);
  const BAL = S([1.0, 1.9, 2.6], [1.05, 0.2, 0.9], 2.0);
  const READ = (i, mm) => S([xOf(mm) + 0.05, ROWS[i].y + 0.05, BZ + 0.8], [xOf(mm), ROWS[i].y - 0.05, BZ], 0.55);
  let loaded = null; let timer = null; let elapsed = 0; let sh = null;
  const truthAt = (i, t) => tubes[i].pos;

  function setKOH(tb, f) { tb.kohLevel = f; tb.koh.visible = f > 0.01; tb.koh.scale.y = Math.max(0.001, f * 0.2); tb.koh.position.y = 0.02 + tb.koh.scale.y / 2; }
  function placeDrop(i) { const tb = tubes[i]; tb.drop.visible = true; tb.drop.position.set(xOf(tb.pos) + 0.0225, ROWS[i].y, BZ + 0.06); }

  const stepKOH = {
    title: 'KOH into both tubes', text: 'Fill the <b>dropper</b> from the <b>KOH</b> bottle and run about 2 mL into the bottom of each boiling tube (three dropperfuls each). KOH absorbs the carbon dioxide the seeds give out.',
    tool: 'dropper', shot: TUBES,
    skip() { tubes.forEach((t) => setKOH(t, 1)); },
    handler: { down() {
      if (input.pick([koh])) { if (!ctx.requireTool('dropper')) return true; loaded = 'koh'; sfx.play('pick'); ctx.say('Dropper full of KOH.', 'info', 1200); return true; }
      const tb = tubes.find((t) => input.pick([t.g], true)); if (!tb) return false;
      if (!ctx.requireTool('dropper')) return true;
      if (loaded !== 'koh') { ctx.say('Fill the dropper from the KOH bottle first.', 'hint', 1800); return true; }
      if (tb.kohLevel >= 1) { ctx.say('That tube has enough; too much KOH may wet the seeds.', 'hint', 2000); return true; }
      loaded = null; tools.action(1); anim.wait(0.2, () => tools.action(0)); sfx.play('drip'); const f0 = tb.kohLevel; anim.add(0.5, (k) => setKOH(tb, Math.min(1, f0 + k / 3)));
      ctx.progress(tubes.reduce((a, t) => a + Math.min(1, t.kohLevel + 1 / 3), 0) / 2);
      if (tubes.every((t) => t.kohLevel + 0.34 >= 1)) anim.wait(0.7, () => ctx.next('About 2 mL of KOH in each tube.'));
      return true;
    } },
  };
  const stepGauze = {
    title: 'Set the gauze platform', text: 'Tap each wire-gauze disc to push it down the tube to just above the KOH, so the seeds will never touch the alkali.',
    tool: null, autoTool: 'hand', shot: TUBES,
    skip() { tubes.forEach((t, i) => { t.gauze.visible = true; t.gauze.position.y = 0.25; gauzes[i].visible = false; }); },
    handler: { down() {
      const gz = gauzes.find((m) => m.visible && input.pick([m])); if (!gz) return false;
      const i = gauzes.indexOf(gz); gz.visible = false; const tb = tubes[i]; tb.gauze.visible = true; sfx.play('glass');
      anim.add(0.8, (k) => { tb.gauze.position.y = 1.9 - k * 1.65; }, { done: () => { if (tubes.every((t) => t.gauze.visible)) ctx.next('Gauze platforms in place, clear of the KOH.'); } });
      return true;
    } },
  };
  function seedStep(i) {
    return {
      title: i ? 'Weigh 10 g of boiled seeds (control)' : 'Weigh 10 g of germinating seeds',
      text: `Tap the <b>${i ? 'boiled' : 'germinating'}</b> seeds to put them on the balance pan, read the mass, then tap the pan to tip them into tube <b>${i ? 'B' : 'A'}</b>.`,
      tool: null, autoTool: 'hand', shot: BAL,
      skip() { trays[i].s.visible = false; tubes[i].seeds.visible = true; ui.observe(`Seeds ${i ? 'B' : 'A'}`, `${mass.toFixed(2)} g`); },
      handler: { down() {
        if (!this.onPan) { if (!input.pick([trays[i].t])) return false; this.onPan = true; trays[i].s.visible = false; bal.set(mass + (i ? 0.03 : 0)); sfx.play('place'); return true; }
        if (!input.pick([bal.group])) return false;
        bal.set(0); tubes[i].seeds.visible = true; ui.observe(`Seeds ${i ? 'B' : 'A'}`, `${(mass + (i ? 0.03 : 0)).toFixed(2)} g`); sfx.play('pour');
        ctx.next(i ? 'Boiled (dead) seeds of the same mass in tube B: the control.' : `${mass.toFixed(2)} g of germinating seeds in tube A, resting on the gauze.`); return true;
      } },
    };
  }
  const stepBung = {
    title: 'Fit the bungs and capillaries', text: 'Tap each tube to push in its rubber bung carrying the bent capillary tube that runs along the scale. The joint must be airtight.',
    tool: null, autoTool: 'hand', shot: SET,
    skip() { tubes.forEach((t) => { t.bung.visible = true; t.bung.position.y = 1.47; t.cap.visible = true; }); },
    handler: { down() {
      const tb = tubes.find((t) => !t.bung.visible && input.pick([t.g], true)); if (!tb) return false;
      tb.bung.visible = true; tb.cap.visible = true; sfx.play('squish'); anim.add(0.6, (k) => { tb.bung.position.y = 2.4 - k * 0.93; tb.cap.position.y = (1 - k) * 0.93; }, { ease: ease.out, done: () => { if (tubes.every((t) => t.bung.visible)) ctx.next('Both tubes sealed, capillaries lying along the scale.'); } });
      return true;
    } },
  };
  const stepEquil = {
    title: 'Let the tubes reach bath temperature', text: 'Gas expands as it warms, so a reading taken now would mean nothing. Run the clock 5 minutes for the tubes to reach 25 °C.',
    tool: null, autoTool: 'hand', hideBelt: true, shot: SET,
    enter() { timer = timelapse(ctx, { step: 5, unit: 'min', onTick: (m, done) => { if (done && !this.done) { this.done = true; timer.remove(); timer = null; ctx.next('Temperature steady: the bath holds it constant.'); } } }); },
    exit() { if (timer) { timer.remove(); timer = null; } },
  };
  const stepIndex = {
    title: 'Introduce the index drop', text: 'Fill the <b>dropper</b> with <b>eosin</b> and touch it to the open end of each capillary: a short red drop is drawn in to act as the index.',
    tool: 'dropper', shot: S([0.75, 1.75, BZ + 1.35], [0.85, 1.35, BZ], 1.0),
    skip() { placeDrop(0); placeDrop(1); },
    handler: { down(p) {
      if (input.pick([eosin])) { if (!ctx.requireTool('dropper')) return true; loaded = 'eosin'; sfx.play('pick'); return true; }
      const i = [0, 1].find((k) => { tmp.set(xOf(150) + 0.06, ROWS[k].y, BZ + 0.06); world.localToWorld(tmp); input.project(tmp, tmp, ctx.stage.clientWidth, ctx.stage.clientHeight); return Math.hypot(tmp.x - p.x, tmp.y - p.y) < 50 && !tubes[k].drop.visible; });
      if (i === undefined) return false;
      if (!ctx.requireTool('dropper')) return true;
      if (loaded !== 'eosin') { ctx.say('Fill the dropper from the eosin bottle first.', 'hint', 1800); return true; }
      loaded = null; const tb = tubes[i]; sfx.play('drip'); const p0 = 152; tb.drop.visible = true;
      anim.add(0.9, (k) => { tb.pos = p0 + (start[i] - p0) * k; placeDrop(i); }, { done: () => { if (tubes.every((t) => t.drop.visible)) ctx.next('Index drops in both capillaries.'); } });
      return true;
    } },
  };
  function readHandler(onRead) {
    return { down() {
      tmp.set(0, 0, 1); const plane = new THREE.Plane().setFromNormalAndCoplanarPoint(tmp, card.getWorldPosition(new THREE.Vector3()));
      const hit = input.ptr.ray.intersectPlane(plane, new THREE.Vector3()); if (!hit) return false;
      world.worldToLocal(hit); const mm = mmOf(hit.x); if (mm < -5 || mm > 155) return false;
      const i = Math.abs(hit.y - ROWS[0].y) < Math.abs(hit.y - ROWS[1].y) ? 0 : 1;
      onRead(i, Math.round(mm * 2) / 2); return true;
    } };
  }
  let need = []; let readsAt = 0;
  function nextRead() {
    if (!need.length) return false;
    const i = need[0]; ctx.rig.go(READ(i, tubes[i].pos), 0.9);
    ui.setText(`Tap the scale at the <b>left (inner) edge</b> of the index in tube <b>${i ? 'B' : 'A'}</b>${readsAt ? ` at ${readsAt} min` : ''}.`);
    return true;
  }
  function takeRead(i, mm, done) {
    if (i !== need[0]) { ctx.say(`Read tube ${need[0] ? 'B' : 'A'} now.`, 'hint', 1600); return; }
    const truth = tubes[i].pos; const err = Math.abs(mm - truth);
    if (err > 1.0) { ctx.mistake(`Read again: line your eye up with the inner edge of the drop; your tap was ${err.toFixed(1)} mm off.`, 2); return; }
    sfx.play('ok'); tubes[i].reads.push([readsAt, mm]); need.shift();
    ui.observe(`${i ? 'B' : 'A'} at ${readsAt} min`, `${mm.toFixed(1)} mm`);
    if (!nextRead()) done();
  }
  const stepStart = {
    title: 'Read the starting positions', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: READ(0, start[0]),
    enter() { readsAt = 0; need = [0, 1]; nextRead(); },
    skip() { tubes.forEach((t) => t.reads.push([0, t.pos])); need = []; },
    handler: readHandler((i, mm) => takeRead(i, mm, () => ctx.next('Starting positions recorded.'))),
  };
  const stepRun = {
    title: 'Read every 2 minutes for 10 minutes', text: 'Run the clock 2 minutes, then read both index drops. Five sets.', tool: null, autoTool: 'hand', hideBelt: true, shot: SET,
    enter() {
      graph.show(ctx.stage.clientWidth > 640); drawGraph();
      timer = timelapse(ctx, { step: 2, unit: 'min', onTick: (m, done) => {
        const dt = m - elapsed; elapsed = m;
        tubes.forEach((t, i) => { t.pos -= v[i] * dt * (1 + (R() - 0.5) * 0.12); placeDrop(i); });
        if (done) { readsAt = Math.round(m); need = [0, 1]; timer.enable(false); nextRead(); }
      } });
    },
    skip() { for (let m = 2; m <= 10; m += 2) tubes.forEach((t, i) => { t.pos -= v[i] * 2 * (1 + (R() - 0.5) * 0.12); t.reads.push([m, Math.round(t.pos * 2) / 2]); placeDrop(i); }); elapsed = 10; },
    exit() { if (timer) { timer.remove(); timer = null; } graph.show(false); },
    handler: readHandler((i, mm) => takeRead(i, mm, () => {
      drawGraph(); ctx.progress(readsAt / 10);
      if (readsAt >= 10) ctx.next('Five sets of readings.'); else { ctx.rig.go(SET, 0.9); timer.enable(true); ui.setText('Run the clock another 2 minutes, then read both drops.'); }
    })),
  };
  function series(i) { const r = tubes[i].reads; const s0 = r.length ? r[0][1] : 0; return r.map(([t, mm]) => [t, s0 - mm]); }
  function drawGraph() { const a = series(0); const b = series(1); const pts = a.map(([x, y]) => [x, y, '#dc2626']).concat(b.map(([x, y]) => [x, y, '#2563eb'])); graph.draw(pts.length ? pts : [[0, 0]], a.length > 1 ? fitLine(a) : null, { xMax: 10, yMax: Math.max(10, Math.ceil(v[0] * 11 / 10) * 10) }); }
  const stepRate = {
    title: 'Work out the rate', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: SET,
    enter() {
      const fa = fitLine(series(0)); const fb = fitLine(series(1)); const slope = fa.b - fb.b; const rate = slope * AREA / mass;
      res.slope = slope; res.rate = rate;
      sh = sheet(ctx, { title: 'Readings (mm on the scale)' });
      sh.set(table(['t (min)', 'A', 'B'], tubes[0].reads.map(([t, mm], k) => [t, mm.toFixed(1), (tubes[1].reads[k] || [0, 0])[1].toFixed(1)])) + `<p>Slope A ${fa.b.toFixed(2)} mm/min, control B ${fb.b.toFixed(2)} mm/min.<br>Corrected movement ${slope.toFixed(2)} mm/min. Bore radius 1.0 mm, area πr² = ${AREA.toFixed(3)} mm².<br>O₂ uptake = ${slope.toFixed(2)} × ${AREA.toFixed(3)} ÷ ${mass.toFixed(2)} g</p>`);
      ui.setText('Volume of O₂ = distance × cross-section of the bore (1 mm³ = 1 µL). Subtract the control and divide by the mass of seeds.');
      const right = Math.round(rate * 100) / 100;
      const opts = [right, Math.round(slope * 100) / 100, Math.round(slope * AREA * 100) / 100, Math.round(rate * 4 * 100) / 100].filter((x, k, a) => a.indexOf(x) === k).sort(() => R() - 0.5);
      ask(ctx, 'Rate of O₂ uptake (µL g⁻¹ min⁻¹)', opts.map((x) => ({ label: x.toFixed(2), value: x })), right, { y: 0.08, wrong: 'Multiply the corrected distance per minute by the bore area (mm³ = µL), then divide by the seed mass in grams.', then() { ui.observe('O₂ uptake', `${right.toFixed(2)} µL g⁻¹ min⁻¹`); ask(ctx, 'Why must the tube contain KOH?', [{ label: 'It absorbs CO₂, so the drop moves only by the O₂ used', value: 'ok' }, { label: 'It supplies oxygen to the seeds', value: 'o' }, { label: 'It kills microbes on the seeds', value: 'm' }], 'ok', { delay: 0.3, y: 0.08, ok: 'Seeds respiring glucose give out about as much CO₂ as the O₂ they take in (RQ ≈ 1). Without KOH the volume would hardly change; with it, the fall in volume is the oxygen absorbed. The boiled seeds do not respire, so their drop stays put apart from small temperature drift.', wrong: 'Think about the two gases exchanged in respiration and what KOH does to one of them.' }); } });
    },
    exit() { ui.clearChooser(); },
  };
  const res = {};
  const steps = [stepKOH, stepGauze, seedStep(0), seedStep(1), stepBung, stepEquil, stepIndex, stepStart, stepRun, stepRate];
  ctx.debug = { tubes, v, xOf, ROWS, READ };
  void fx; void truthAt;
  return {
    tools: ['hand', 'dropper'],
    steps,
    update(dt) { bal.update(dt); hud.update(); },
    result() {
      const rate = res.rate ?? trueRate; const err = Math.abs(rate - trueRate) / trueRate * 100;
      return {
        title: 'Respiration rate of germinating seeds',
        rows: [['Seed mass', `${mass.toFixed(2)} g`], ['Index movement (corrected)', `${(res.slope ?? 0).toFixed(2)} mm min⁻¹`], ['O₂ uptake', `${rate.toFixed(2)} µL g⁻¹ min⁻¹`], ['True rate in this run', `${trueRate.toFixed(2)} µL g⁻¹ min⁻¹ (error ${err.toFixed(1)} %)`]],
        conclusion: 'Germinating seeds respire actively: they absorb oxygen, and with the CO₂ removed by KOH the gas volume falls, pulling the index toward the tube at a steady rate. The boiled seeds showed almost no movement, so the change is due to respiration of living cells.',
      };
    },
    dispose() { if (timer) timer.remove(); if (sh) sh.remove(); hud.dispose(); ui.clearChooser(); },
  };
}
