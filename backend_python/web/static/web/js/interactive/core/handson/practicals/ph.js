// pH and indicators. Eight solutions are spotted on a white tile; the student dabs litmus on each,
// then adds universal indicator and matches each colour against the chart (the pH of each spot is
// computed: strong acid and base fully ionised, ethanoic acid and ammonia from Ka and Kb,
// bicarbonate amphiprotic). Then a pH meter: rinse, calibrate in pH 7.00 and 4.00 buffers, and
// measure three solutions to 0.01 (an uncalibrated meter is precisely wrong). Last, drops of acid
// into water and into a bicarbonate buffer show what a buffer does (Henderson–Hasselbalch).
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { reagentBottle, washBottle } from '../../bio-handson/props.js';
import { makeSpotTile } from '../../bio-handson/glassware.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { beaker } from '../glass.js';
import { createGraph } from '../stopwatch.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const weakAcid = (c, pKa) => { const Ka = 10 ** -pKa; return -Math.log10((-Ka + Math.sqrt(Ka * Ka + 4 * Ka * c)) / 2); };
const SOLS = [
  { name: '0.1 M HCl', pH: 1.0 }, { name: 'lemon juice', pH: 2.4 }, { name: '0.1 M CH₃COOH', pH: weakAcid(0.1, 4.76) }, { name: 'distilled water', pH: 7.0 },
  { name: 'NaHCO₃ soln', pH: (6.35 + 10.33) / 2 }, { name: 'soap solution', pH: 10.0 }, { name: '0.1 M NH₃', pH: 14 - weakAcid(0.1, 4.75) }, { name: '0.1 M NaOH', pH: 13.0 },
];
const UI_STOPS = [[1, 0xd7191c], [2, 0xe8452c], [3, 0xf47a31], [4, 0xfdae61], [5, 0xfee08b], [6, 0xd9ef8b], [7, 0x66bd63], [8, 0x1a9850], [9, 0x2b9a9a], [10, 0x2c7fb8], [11, 0x253494], [12, 0x54278f], [13, 0x6a1b9a], [14, 0x4a148c]];
const BANDS = [['1–2  red', 1, 2.5], ['3–4  orange', 2.5, 4.5], ['5–6  yellow', 4.5, 6.5], ['7  green', 6.5, 7.5], ['8–9  blue-green', 7.5, 9.5], ['10–11  blue', 9.5, 11.5], ['12–14  violet', 11.5, 14.1]];
function uiColour(pH, out) {
  const p = Math.max(1, Math.min(14, pH)); let i = 0; while (i < UI_STOPS.length - 2 && UI_STOPS[i + 1][0] < p) i++;
  const [a, ca] = UI_STOPS[i]; const [b, cb] = UI_STOPS[i + 1]; return out.set(ca).lerp(new THREE.Color(cb), (p - a) / (b - a));
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'pH as acid is added: <span style="color:#dc2626">water</span> · <span style="color:#2563eb">buffer</span>', xLabel: 'drops of 0.1 M HCl', yLabel: 'pH' }); graph.el.classList.add('ho-side');
  const order = SOLS.map((_, i) => i).sort(() => Math.random() - 0.5);
  world.add(mesh(new THREE.BoxGeometry(5.6, 0.02, 2.6), MAT.matte(0x2f3640), [0.2, 0.01, 0]));
  const tile = makeSpotTile(12); tile.group.scale.setScalar(1.5); tile.group.position.set(-1.45, 0.02, 0.2); world.add(tile.group);
  const spots = order.map((si, j) => { const s = tile.spots[j]; s.drop.visible = true; s.drop.material.color.set(si === 1 ? 0xf6f0c8 : 0xeef4f8); s.drop.material.opacity = 0.55; return { si, s, litmus: null, ui: false }; });
  const chips = spots.map((sp) => { const c = hud.chip('ho-tag').set(SOLS[sp.si].name).show(true); sp.s.drop.getWorldPosition(c.at); c.at.y += 0.04; c.dx = -30; c.dy = -26; return c; });
  world.updateMatrixWorld(true); spots.forEach((sp, j) => sp.s.drop.getWorldPosition(chips[j].at));
  const uiBottle = reagentBottle('Univ. ind.', 0x5fa35a); uiBottle.scale.setScalar(0.8); uiBottle.position.set(-0.4, 0, -0.45); world.add(uiBottle);
  const litmusBox = mesh(new THREE.BoxGeometry(0.4, 0.06, 0.25), MAT.gloss(0x7c3aed), [-0.4, 0.03, 0.75]); world.add(litmusBox);
  const strips = new THREE.Group(); world.add(strips);
  // the pH meter
  const meter = new THREE.Group(); meter.position.set(-0.15, 0, -0.55); world.add(meter);
  meter.add(mesh(new THREE.BoxGeometry(0.8, 0.22, 0.55), MAT.gloss(0x1f2937), [0, 0.11, 0]));
  const cv = document.createElement('canvas'); cv.width = 256; cv.height = 96; const g2 = cv.getContext('2d'); const tex = new THREE.CanvasTexture(cv); if (tex.colorSpace !== undefined) tex.colorSpace = THREE.SRGBColorSpace;
  const disp = mesh(new THREE.PlaneGeometry(0.5, 0.19), new THREE.MeshBasicMaterial({ map: tex }), [0, 0.223, 0.05]); disp.rotation.x = -Math.PI / 2 + 0.35; meter.add(disp);
  meter.add(mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.6, 8), MAT.steel(), [-0.55, 0.8, -0.1]));
  const probe = new THREE.Group(); world.add(probe);
  probe.add(mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.9, 14), MAT.gloss(0xe5e7eb), [0, 0.45, 0]));
  probe.add(mesh(new THREE.SphereGeometry(0.04, 14, 10), MAT.glass(), [0, 0, 0], { cast: false }));
  const PHOME = new THREE.Vector3(0.35, 0.85, -0.2); probe.position.copy(PHOME);
  const wash = washBottle(); wash.position.set(2.6, 0, -0.7); world.add(wash);
  const cups = [['pH 7.00', 7.0, 0xf3e7a0], ['pH 4.00', 4.0, 0xf5c2c2], [SOLS[0].name, SOLS[0].pH, 0xeef4f8], [SOLS[2].name, SOLS[2].pH, 0xeef4f8], [SOLS[6].name, SOLS[6].pH, 0xeef4f8]].map(([n, p, c], i) => {
    const b = beaker(40, c); b.group.position.set(0.55 + i * 0.58, 0, 0.6); world.add(b.group); const ch = hud.chip('ho-tag').set(n).show(true); ch.at.set(b.group.position.x, BY + 0.95, b.group.position.z); ch.dx = -26; return { name: n, pH: p, b, chip: ch };
  });

  const st = { phase: 'litmus', uiDone: 0, answers: 0, cal7: false, cal4: false, inCup: null, rinsed: true, last: null, meas: {}, offset: 0.38, slope: 0.93, drops: { water: 0, buffer: 0 }, pts: { water: [], buffer: [] } };
  let shown = ''; function paint(v) { const s = v === null ? '— — . — —' : v.toFixed(2); if (s === shown) return; shown = s; g2.fillStyle = '#9fb59a'; g2.fillRect(0, 0, 256, 96); g2.fillStyle = '#0f1a0f'; g2.font = '700 54px ui-monospace, Menlo, monospace'; g2.textAlign = 'right'; g2.fillText(s, 236, 66); g2.font = '700 20px system-ui'; g2.textAlign = 'left'; g2.fillText(st.cal7 && st.cal4 ? 'pH  CAL' : 'pH', 14, 26); tex.needsUpdate = true; }
  paint(null);
  const mChip = hud.chip('ho-chip-read'); mChip.dx = 20; mChip.dy = -40;
  const meterReads = (pH) => (st.cal7 && st.cal4 ? pH : 7 + (pH - 7) * st.slope + (st.cal7 ? 0 : st.offset));
  let reading = null; let target = null;
  function dip(cup) {
    if (!st.rinsed && st.inCup && st.inCup !== cup) ctx.mistake('Rinse the electrode with distilled water between solutions, or the last one is carried over into the next.', 2);
    st.inCup = cup; st.rinsed = false; const to = new THREE.Vector3(cup.b.group.position.x, 0.25, cup.b.group.position.z); const from = probe.position.clone();
    anim.add(0.8, (k) => { probe.position.lerpVectors(from, to, k); probe.position.y += Math.sin(k * Math.PI) * 0.5; }, { done: () => { target = meterReads(cup.pH) + (Math.random() - 0.5) * 0.02; reading = 7; sfx.play('glass'); } });
  }
  function rinse() { const from = probe.position.clone(); anim.add(0.6, (k) => probe.position.lerpVectors(from, PHOME, k), { done: () => { sfx.play('pour'); st.rinsed = true; st.inCup = null; target = null; ui.say('Electrode rinsed with distilled water and blotted.', 'info', 1600); } }); }

  const SHOT_TILE = shot({ pos: [-1.1, 2.5, 2.2], target: [-1.05, 0.1, 0.15], fit: 2.5, fitH: 1.7 });
  const SHOT_METER = shot({ pos: [1.0, 2.9, 3.4], target: [0.9, 0.3, 0.0], fit: 4.0, fitH: 2.0 });

  const steps = [
    {
      title: 'Litmus', text: 'Tap the <b>litmus papers</b>, then tap each spot to touch a strip of red and of blue litmus to it.', hint: 'Acids turn blue litmus red; alkalis turn red litmus blue; neutral leaves both.', shot: SHOT_TILE, hideBelt: true,
      enter() { st.litmus = false; },
      skip() { spots.forEach((sp) => { sp.litmus = true; }); },
      handler: { down(p) {
        if (hits(ctx, litmusBox, p, 50)) { st.litmus = true; sfx.play('pick'); ctx.say('Strips of red and blue litmus in hand.', 'info', 1400); return true; }
        const j = spots.findIndex((sp) => hits(ctx, sp.s.drop, p, 30)); if (j < 0) return false;
        if (!st.litmus) { ctx.say('Pick up the litmus papers first.', 'hint', 1500); return true; }
        const sp = spots[j]; if (sp.litmus) return true; sp.litmus = true; const pH = SOLS[sp.si].pH;
        const pos = new THREE.Vector3(); sp.s.drop.getWorldPosition(pos); world.worldToLocal(pos);
        [[pH < 8 ? 0xd94b4b : 0x3b6fd1, -0.05], [pH < 5 ? 0xd94b4b : 0x3b6fd1, 0.05]].forEach(([c, dx]) => { const m = mesh(new THREE.BoxGeometry(0.035, 0.004, 0.16), MAT.matte(c), [pos.x + dx, 0.1, pos.z + 0.2]); strips.add(m); });
        sfx.play('place');
        if (spots.every((s) => s.litmus)) anim.wait(0.8, () => ui.chooseMany(ctx.stage.clientWidth / 2, 40, 'Which are acidic (blue litmus turned red)?', spots.map((s) => ({ label: SOLS[s.si].name, value: s.si })), (v) => {
          const truth = spots.filter((s) => SOLS[s.si].pH < 5).map((s) => s.si);
          if (v.length !== truth.length || !v.every((x) => truth.includes(x))) ctx.mistake(`The acids are ${truth.map((x) => SOLS[x].name).join(', ')}: blue litmus went red. Litmus says only acid or alkali, not how strong.`, 3);
          ui.observe('Litmus: acidic', String(truth.length)); ctx.next(null, 0.6);
        }));
        return true;
      } },
    },
    {
      title: 'Universal indicator', text: 'Tap the <b>universal indicator</b>, then each spot to add a drop. Then tap each spot and match its colour with the chart.', hint: 'Red is strongly acidic, green neutral, violet strongly alkaline.', shot: SHOT_TILE, hideBelt: true,
      enter() { strips.visible = false; st.uiHeld = false; },
      skip() { spots.forEach((sp) => { uiColour(SOLS[sp.si].pH, sp.s.drop.material.color); sp.ui = true; sp.matched = true; }); },
      handler: { down(p) {
        if (hits(ctx, uiBottle, p, 50, 0.3)) { st.uiHeld = true; sfx.play('pick'); return true; }
        const j = spots.findIndex((sp) => hits(ctx, sp.s.drop, p, 30)); if (j < 0) return false; const sp = spots[j];
        if (!sp.ui) { if (!st.uiHeld) { ctx.say('Take the universal indicator first.', 'hint', 1500); return true; } sp.ui = true; const c0 = sp.s.drop.material.color.clone(); const c1 = uiColour(SOLS[sp.si].pH, new THREE.Color()); anim.add(1.0, (k) => sp.s.drop.material.color.copy(c0).lerp(c1, k)); sp.s.drop.material.opacity = 0.85; sfx.play('drip'); return true; }
        if (sp.matched) return true;
        ui.choose(p.x, p.y, `${SOLS[sp.si].name}: the colour matches pH…`, BANDS.map((b, i) => ({ label: b[0], value: i })), (v) => {
          const pH = SOLS[sp.si].pH; const right = BANDS.findIndex((b) => pH >= b[1] && pH < b[2]);
          if (v !== right && Math.abs(v - right) > 0) { ctx.mistake(`Look again: that colour is ${BANDS[right][0].replace(/\s+/g, ' ')}.`, 1); return; }
          sp.matched = true; ui.observe(SOLS[sp.si].name, `UI ≈ pH ${BANDS[right][0].split(' ')[0]}`);
          if (spots.every((s) => s.matched)) ctx.next('All eight placed on the pH scale.', 0.8);
        });
        return true;
      } },
    },
    {
      title: 'pH meter', text: 'Calibrate first: dip the electrode in the <b>pH 7.00</b> buffer and press <b>CAL 7</b>, rinse (tap the <b>wash bottle</b>), dip in <b>pH 4.00</b> and press <b>CAL 4</b>. Then measure the three solutions, rinsing between each, and record each reading.', hint: 'Rinse every time the electrode leaves a solution.', shot: SHOT_METER, hideBelt: true,
      enter() { chips.forEach((c) => c.show(false)); hud.actions([{ id: 'c7', label: 'CAL 7', onClick: () => cal(7) }, { id: 'c4', label: 'CAL 4', onClick: () => cal(4) }, { id: 'rec', label: 'Record', primary: true, onClick: recordMeter }]); },
      exit() { hud.actions([]); },
      skip() { st.cal7 = st.cal4 = true; cups.slice(2).forEach((c) => { st.meas[c.name] = Math.round(c.pH * 100) / 100; }); },
      handler: { down(p) {
        if (hits(ctx, wash, p, 60, 0.4)) { rinse(); return true; }
        const c = cups.find((cu) => hits(ctx, cu.b.group, p, 50, 0.4)); if (c) { dip(c); return true; }
        return false;
      } },
    },
    {
      title: 'What a buffer does', text: 'Two beakers: <b>distilled water</b> and a <b>bicarbonate buffer</b> like blood (pH 7.4). Tap each beaker to add drops of 0.1 M HCl and watch the pH meter and the graph. Add at least ten drops to each.', hint: 'In the buffer, HCO₃⁻ mops up the added H⁺ as H₂CO₃, so the ratio barely changes.', shot: SHOT_METER, hideBelt: true,
      enter() {
        cups.forEach((c, i) => { c.b.group.visible = i < 2; c.chip.show(i < 2); }); cups[0].name = 'water'; cups[1].name = 'buffer'; cups[0].chip.set('distilled water'); cups[1].chip.set('HCO₃⁻ buffer (blood)');
        cups[0].b.material.color.set(0xeef4f8); cups[1].b.material.color.set(0xf6e9e9); graph.show(true); drawBuf();
        hud.actions([{ id: 'go', label: 'Compare', primary: true, disabled: true, onClick: () => { hud.actions([]); graph.show(false); ctx.next(); } }]);
      },
      exit() { hud.actions([]); graph.show(false); },
      skip() { for (let i = 0; i < 10; i++) { addAcid('water'); addAcid('buffer'); } },
      handler: { down(p) { const c = cups.slice(0, 2).find((cu) => hits(ctx, cu.b.group, p, 60, 0.4)); if (!c) return false; addAcid(c.name); sfx.play('drip'); hud.enable('go', st.drops.water >= 10 && st.drops.buffer >= 10); return true; } },
    },
  ];
  function cal(n) {
    const cup = st.inCup; if (!cup || !/buffer|pH/.test(cup.name)) { ctx.say('Dip the electrode in the right buffer first.', 'hint', 1800); return; }
    if (cup.pH !== n) { ctx.mistake(`The electrode is in the pH ${cup.pH.toFixed(2)} buffer, not ${n}.00.`, 2); return; }
    if (n === 4 && !st.cal7) { ctx.say('Set the zero with the pH 7.00 buffer first, then the slope with pH 4.00.', 'hint', 2200); return; }
    if (n === 7) st.cal7 = true; else st.cal4 = true; target = cup.pH; sfx.play('click'); ui.observe(`CAL ${n}`, 'done');
  }
  function recordMeter() {
    const cup = st.inCup; if (!cup || cup.name.startsWith('pH')) { ctx.say('Measure the solutions, not the buffers.', 'hint', 1800); return; }
    if (reading === null || Math.abs(reading - target) > 0.02) { ctx.say('Wait for the reading to settle.', 'hint', 1500); return; }
    if (!(st.cal7 && st.cal4)) { ctx.mistake(`An uncalibrated meter: it reads ${reading.toFixed(2)}, but the true pH is ${cup.pH.toFixed(2)}. Calibrate with the buffers first.`, 3); return; }
    st.meas[cup.name] = Math.round(reading * 100) / 100; ui.observe(`meter: ${cup.name}`, `<b>pH ${reading.toFixed(2)}</b>`); sfx.play('ok');
    if (cups.slice(2).every((c) => st.meas[c.name] !== undefined)) { hud.actions([]); ctx.next('Three measured.', 0.8); }
  }
  function bufPH(n) { const h = n * 5e-6; const V = 0.05; const a = 0.024 * V; const b = 0.0012 * V; return 6.1 + Math.log10(Math.max(1e-9, a - h) / (b + h)); }
  function waterPH(n) { const h = n * 5e-6 / 0.05; return n === 0 ? 7.0 : -Math.log10(h + 1e-7); }
  function addAcid(which) { st.drops[which] += 1; const n = st.drops[which]; const pH = which === 'water' ? waterPH(n) : bufPH(n); st.pts[which].push([n, pH, which === 'water' ? '#dc2626' : '#2563eb']); const cup = cups[which === 'water' ? 0 : 1]; if (st.inCup !== cup) { st.inCup = cup; probe.position.set(cup.b.group.position.x, 0.25, cup.b.group.position.z); } target = pH; reading = pH; drawBuf(); }
  function drawBuf() { const pts = st.pts.water.concat(st.pts.buffer); graph.draw(pts.length ? pts : [[0, 7]], null, { xMax: Math.max(12, st.drops.water, st.drops.buffer) + 1, yMin: 2, yMax: 8 }); }

  ctx.debug = { st, spots, cups, dip, cal, rinse };
  return {
    tools: [], steps,
    update(dt) { if (target !== null && reading !== null) reading += (target - reading) * (1 - Math.exp(-dt / 0.8)); paint(target === null ? null : reading); disp.getWorldPosition(mChip.at); mChip.set(`pH <b>${target === null ? '—' : reading.toFixed(2)}</b>`); mChip.show(ctx.stepIndex >= 2); hud.update(); },
    result() {
      const w = st.pts.water.length ? st.pts.water[st.pts.water.length - 1][1] : 7; const b = st.pts.buffer.length ? st.pts.buffer[st.pts.buffer.length - 1][1] : 7.4;
      return {
        title: 'pH and indicators',
        rows: [['0.1 M HCl (meter)', `${(st.meas[SOLS[0].name] ?? 0).toFixed(2)}`], ['0.1 M CH₃COOH (meter)', `${(st.meas[SOLS[2].name] ?? 0).toFixed(2)}`], ['0.1 M NH₃ (meter)', `${(st.meas[SOLS[6].name] ?? 0).toFixed(2)}`], ['Water + 10 drops HCl', `pH ${w.toFixed(2)}`], ['Buffer + 10 drops HCl', `pH ${b.toFixed(2)}`]],
        conclusion: `Litmus only says acid or alkali; universal indicator places a solution to about one unit; a calibrated meter gives two decimals. 0.1 M HCl (pH 1.0) and 0.1 M ethanoic acid (pH ${SOLS[2].pH.toFixed(1)}) have the same concentration but the weak acid is barely ionised. Ten drops of acid moved the water by ${(7 - w).toFixed(1)} units but the buffer by only ${(7.4 - b).toFixed(2)}: HCO₃⁻ takes up the H⁺.`,
      };
    },
    dispose() { hud.dispose(); graph.dispose(); },
  };
}
