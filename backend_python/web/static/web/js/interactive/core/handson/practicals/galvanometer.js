// Figure of merit of a galvanometer. A cell, a plug key, a high-resistance box and the
// galvanometer are in series. The student pulls plugs to choose R (closing the key with too
// little resistance slams the needle against its stop), closes the key, waits for the needle to
// settle and taps the dial where it points. The deflection follows θ = E / (k (R + G + r)), with the
// cell's small internal resistance; k = E / ((R + G) θ) is worked out from the student's readings
// and checked on a graph of 1/θ against R.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { M as KIT } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { createGraph, fitLine } from '../stopwatch.js';
import { lead, galvanometer, resistanceBox, plugKey, cell, postTop } from '../circuit.js';

const BY = 0.8; const E = 2.0; const RG = 100; const RI = 1.5;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: '1/θ against R', xLabel: 'R (kΩ)', yLabel: '1/θ (div⁻¹)' });
  graph.el.classList.add('ho-side');
  const K = Math.round((1.9 + Math.random() * 1.3) * 100) / 100 * 1e-5;

  world.add(mesh(new THREE.BoxGeometry(7.2, 0.06, 3.0), KIT.wood('teak'), [0, 0.03, 0]));
  const box = resistanceBox([100, 200, 200, 500, 1000, 2000, 2000, 5000]); box.group.scale.setScalar(1.4); box.group.position.set(0, 0.06, -0.6); world.add(box.group);
  const galvo = galvanometer(); galvo.group.scale.setScalar(1.7); galvo.group.position.set(2.3, 0.06, 0.5); world.add(galvo.group);
  const key = plugKey(); key.group.scale.setScalar(1.3); key.group.position.set(-1.9, 0.06, 0.8); world.add(key.group);
  const bat = cell('2 V'); bat.group.position.set(-2.6, 0.06, -0.6); world.add(bat.group);
  const tmpA = new THREE.Vector3(); const tmpB = new THREE.Vector3();
  const wire = (a, b, c) => { postTop(a, world, tmpA); postTop(b, world, tmpB); lead(world, tmpA, tmpB, c, { sag: 0.05 }); };
  world.updateMatrixWorld(true);
  wire(bat.posts[1], key.posts[0], 0xb91c1c); wire(key.posts[1], galvo.posts[0], 0xb91c1c); wire(galvo.posts[1], box.posts[1], 0x111827); wire(box.posts[0], bat.posts[0], 0x111827);

  const st = { readings: [], tap: null, slammed: false, settleT: 0 };
  const Rbox = () => box.total();
  const current = () => (key.closed ? E / (Rbox() + RG + RI) : 0);
  const theta = () => current() / K;
  function drive() { const t = theta(); galvo.setDivisions(Math.min(33, t)); if (t > 33 && !st.slammed) { st.slammed = true; sfx.play('bad'); ctx.mistake(`The needle slammed against its stop: with R = ${Rbox()} Ω the current is ${(current() * 1000).toFixed(2)} mA, ${(t / 30).toFixed(0)}× full scale. Take out plugs for a high resistance BEFORE closing the key.`, 5); anim.wait(0.6, () => { key.set(false, anim); drive(); }); } if (t <= 33) st.slammed = false; }

  const dialMark = mesh(new THREE.ConeGeometry(0.012, 0.04, 3), new THREE.MeshBasicMaterial({ color: 0x2563eb, depthTest: false }), null, { cast: false }); dialMark.renderOrder = 20; dialMark.visible = false; galvo.face.add(dialMark);
  function tapDial() {
    const h = ctx.input.pick([galvo.face]); if (!h || !h.uv) return false;
    const px = h.uv.x * 512; const py = (1 - h.uv.y) * 320; const a = Math.atan2(py - (320 - 36), px - 256);
    const d = Math.round((a + Math.PI / 2) / (Math.PI / 4) * 30 * 2) / 2; if (Math.abs(d) > 31) return false;
    st.tap = d; const aa = -Math.PI / 2 + d / 30 * Math.PI / 4; dialMark.visible = true; dialMark.position.set((256 + Math.cos(aa) * 186) / 512 * 0.78 - 0.39, 0.245 - (284 + Math.sin(aa) * 186) / 320 * 0.49, 0.01); dialMark.rotation.z = aa + Math.PI / 2;
    hud.relabel('rec', `Record θ = ${Math.abs(d)} div`); hud.enable('rec', true); sfx.play('click'); return true;
  }
  function record() {
    if (!key.closed) { ctx.say('Close the key first.', 'hint', 1500); return; }
    if (Math.abs(galvo.divisions - theta()) > 0.4) { ctx.say('Wait for the needle to settle.', 'hint', 1500); return; }
    const t = theta();
    if (Math.abs(Math.abs(st.tap) - t) > 0.6) { ctx.mistake(`The needle points to ${t.toFixed(1)} divisions, not ${Math.abs(st.tap)}. Look straight down at the needle.`, 2); return; }
    if (t > 30) { ctx.say('Off the scale: more resistance.', 'hint', 1800); return; }
    if (t < 5) ctx.say('A small deflection is hard to read accurately: aim for 10–30 divisions.', 'hint', 2600);
    if (st.readings.some((r) => r.R === Rbox())) { ctx.say('You already have that R. Choose another.', 'hint', 1800); return; }
    st.readings.push({ R: Rbox(), th: Math.abs(st.tap) }); ui.observe(`R = ${Rbox()} Ω`, `θ = <b>${Math.abs(st.tap)}</b> div`); sfx.play('ok');
    st.tap = null; dialMark.visible = false; hud.relabel('rec', `Record (${st.readings.length})`); hud.enable('rec', false);
    key.set(false, anim); drive(); ctx.say('Key opened between readings, so the coil does not heat. Change R and close it again.', 'info', 2600);
    if (st.readings.length >= 5) hud.enable('done', true);
  }

  const SHOT = shot({ pos: [0, 4.0, 5.6], target: [0, 0.3, 0], fit: 6.6, fitH: 2.8 });
  const SHOT_DIAL = shot({ pos: [2.3, 2.0, 1.75], target: [2.3, 0.75, 0.55], fit: 1.6, fitH: 1.1 });

  const steps = [
    {
      title: 'Choose a high resistance', text: 'All the plugs are in: R = 0. Before you close the key, <b>pull plugs</b> (tap them) to put a few thousand ohms in series. Then tap the <b>key</b> to close it.', hint: 'With E = 2 V and R + G of a few thousand ohms, the current is a few hundred microamps: the galvanometer\'s range.', shot: SHOT, hideBelt: true,
      skip() { [4, 5, 6].forEach((i) => { if (!box.plugs[i].out) box.toggle(i); }); key.set(true); drive(); },
      handler: { down(p) {
        for (let i = 0; i < box.plugs.length; i++) if (hits(ctx, box.plugs[i].plug, p, 26, 0.05)) { box.toggle(i, anim); sfx.play('click'); drive(); ctx.say(`R = ${Rbox()} Ω`, 'info', 1200); return true; }
        if (hits(ctx, key.group, p, 50, 0.1)) { key.set(!key.closed, anim); sfx.play('click'); drive(); if (key.closed && !st.slammed) { ui.observe('E, G', `${E} V, ${RG} Ω`); ctx.next('The needle swings and settles.', 1.4); } return true; }
        return false;
      } },
    },
    {
      title: 'Deflection for several R', text: 'Read the deflection: tap the <b>dial</b> where the needle points and record. Then open the key, change R (pull or push plugs) and close it again. Take <b>at least five</b> readings between 10 and 30 divisions.', hint: 'Look straight down on the needle. Bigger R, smaller deflection.', shot: SHOT, hideBelt: true,
      enter() { hud.actions([{ id: 'look', label: 'Look at dial', onClick: () => ctx.rig.go(SHOT_DIAL, 0.8) }, { id: 'all', label: 'Whole circuit', onClick: () => ctx.rig.go(SHOT, 0.8) }, { id: 'rec', label: 'Record (0)', primary: true, disabled: true, onClick: record }, { id: 'done', label: 'Done', disabled: true, onClick: () => { hud.actions([]); ctx.next(); } }]); ctx.rig.go(SHOT_DIAL, 1.2); },
      exit() { hud.actions([]); dialMark.visible = false; },
      skip() { st.readings = []; [3000, 4000, 5000, 6000, 8000].forEach((R) => { st.readings.push({ R, th: Math.round(E / (K * (R + RG + RI)) * 2) / 2 }); }); },
      handler: { down(p) {
        if (tapDial()) return true;
        for (let i = 0; i < box.plugs.length; i++) if (hits(ctx, box.plugs[i].plug, p, 26, 0.05)) { box.toggle(i, anim); sfx.play('click'); drive(); ctx.say(`R = ${Rbox()} Ω`, 'info', 1200); return true; }
        if (hits(ctx, key.group, p, 50, 0.1)) { key.set(!key.closed, anim); sfx.play('click'); drive(); return true; }
        return false;
      } },
    },
    {
      title: 'Figure of merit', text: 'For each reading k = E / ((R + G) θ). The graph of 1/θ against R is a straight line of slope k/E.', shot: SHOT, hideBelt: true,
      enter() {
        const ks = st.readings.map((r) => E / ((r.R + RG) * r.th)); const kMean = ks.reduce((a, b) => a + b, 0) / ks.length; st.k = kMean;
        const pts = st.readings.map((r) => [r.R / 1000, 1 / r.th]); const fit = fitLine(pts); st.kGraph = fit.b / 1000 * E;
        graph.draw(pts, fit, { xMax: Math.max(...pts.map((q) => q[0])) * 1.15, yMax: Math.max(...pts.map((q) => q[1])) * 1.2 }); graph.show(true);
        const opts = [[kMean, 'E / (R + G)θ'], [E / (st.readings[0].R * st.readings[0].th), 'G left out'], [kMean * 1e6 * 1e-3, 'in mA'], [1 / kMean * 1e-10, 'θ(R + G) / E']].map(([v, w]) => ({ label: `${(v * 1e6).toFixed(1)} µA/div  (${w})`, value: w })).sort(() => Math.random() - 0.5);
        anim.wait(1.0, () => ui.choose(ctx.stage.clientWidth / 2, 40, `Mean k from your ${ks.length} readings =`, opts, (v) => {
          if (v !== 'E / (R + G)θ') ctx.mistake('k = I/θ with I = E/(R + G): include the galvanometer\'s own resistance.', 3);
          ui.observe('k', `<b>${(kMean * 1e6).toFixed(2)} µA/div</b>`); ctx.next(`k = ${(kMean * 1e6).toFixed(2)} µA per division; full scale (30 div) is ${(kMean * 30 * 1e6).toFixed(0)} µA.`, 1.4);
        }));
      },
      exit() { ui.clearChooser(); graph.show(false); },
    },
  ];

  ctx.debug = { st, K, box, key, theta, drive, galvo };
  return {
    tools: [], steps,
    update(dt) { galvo.update(dt); hud.update(); },
    result() {
      const err = ((st.k || 0) - K) / K * 100;
      return {
        title: 'Figure of merit',
        rows: [['Readings', String(st.readings.length)], ['k (mean)', `${((st.k || 0) * 1e6).toFixed(2)} µA/div`], ['k (graph slope × E)', `${((st.kGraph || 0) * 1e6).toFixed(2)} µA/div`], ['Galvanometer', `${(K * 1e6).toFixed(2)} µA/div`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`], ['Full-scale current', `${((st.k || 0) * 30 * 1e6).toFixed(0)} µA`]],
        conclusion: `One division of this galvanometer is about ${((st.k || 0) * 1e6).toFixed(1)} µA, so it reaches full scale at well under a milliamp. Readings are only to the nearest half division, so large deflections give the best k; the cell's internal resistance (about ${RI} Ω) is negligible beside thousands of ohms.`,
      };
    },
    dispose() { hud.dispose(); graph.dispose(); },
  };
}
