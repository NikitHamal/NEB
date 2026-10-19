// Ohm's law and resistivity. A cell, a plug key, a slide-wire rheostat, an ammeter in series and a
// voltmeter across a coil of constantan wire. The student closes the key, slides the rheostat to
// change the current, reads the two needles at several settings, opens the key between readings,
// and finds R from the slope of the V-I graph, then the resistivity from the wire's length and
// diameter. The meters are real: the ammeter's resistance and the voltmeter's finite one are in
// the circuit, and a key left in warms the wire, whose resistance creeps up.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, screenDist } from '../hud.js';
import { createGraph, fitLine } from '../stopwatch.js';
import { bindingPost, lead, dialMeter, plugKey, cell, postTop, rheostat } from '../circuit.js';

const BY = 0.8;
const E = 3.0; const RI = 0.4; const RA = 0.1; const RV = 2000;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'V against I', xLabel: 'I (A)', yLabel: 'V (V)' });
  const R0 = Math.round((2.5 + Math.random() * 3.5) * 100) / 100;
  const L = 100; const dmm = Math.round(Math.sqrt(4 * 4.9e-7 * (L / 100) / (Math.PI * R0)) * 1e3 * 1000) / 1000;

  const bat = cell('3 V'); bat.group.position.set(-2.4, 0, -1.2); world.add(bat.group);
  const key = plugKey(); key.group.position.set(-1.3, 0, -1.25); world.add(key.group);
  const rh = rheostat(20); rh.group.position.set(0.6, 0, -1.25); world.add(rh.group); rh.set(1);
  const am = dialMeter('A', 1, 'A', 0.02); am.group.position.set(-1.5, 0, 0.45); am.group.scale.setScalar(1.3); world.add(am.group);
  const vm = dialMeter('V', 3, 'V', 0.05); vm.group.position.set(1.6, 0, 0.45); vm.group.scale.setScalar(1.3); world.add(vm.group);
  const board = new THREE.Group(); board.position.set(0.05, 0, 1.55); world.add(board);
  board.add(mesh(new THREE.BoxGeometry(2.4, 0.08, 0.45), MAT.gloss(0x8a5a33), [0, 0.04, 0]));
  const wire = mesh(new THREE.CylinderGeometry(0.008, 0.008, 2.0, 8), new THREE.MeshStandardMaterial({ color: 0xc0c6cc, metalness: 1, roughness: 0.3 }), [0, 0.13, 0]); wire.rotation.z = Math.PI / 2; board.add(wire);
  const wp = [-1.05, 1.05].map((x) => { const p = bindingPost(); p.position.set(x, 0.08, 0); board.add(p); return p; });
  const tag = mesh(new THREE.PlaneGeometry(0.6, 0.12), new THREE.MeshBasicMaterial({ map: canvasTexture('ho-ohm-tag', 256, 52, (c, w, h) => { c.fillStyle = '#fef3c7'; c.fillRect(0, 0, w, h); c.fillStyle = '#111827'; c.font = '700 24px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText('constantan  L = 100 cm', w / 2, 34); }) }), [0, 0.081, 0.16]); tag.rotation.x = -Math.PI / 2; board.add(tag);
  const tA = new THREE.Vector3(); const tB = new THREE.Vector3();
  const link = (a, b, col) => { postTop(a, world, tA); postTop(b, world, tB); lead(world, tA, tB, col); };
  link(bat.posts[1], key.posts[0], 0xb91c1c); link(key.posts[1], rh.posts[0], 0xb91c1c); link(rh.posts[2], am.posts[1], 0xb91c1c);
  link(am.posts[0], wp[0], 0xb91c1c); link(wp[1], bat.posts[0], 0x111827);
  link(vm.posts[0], wp[0], 0x1d4ed8); link(vm.posts[1], wp[1], 0x1d4ed8);

  const st = { heat: 0, readings: [], keyT: 0, warned: false };
  const Rx = () => R0 * (1 + 0.004 * st.heat);
  function solve() {
    if (!key.closed) return { I: 0, V: 0 };
    const rp = Rx() * RV / (Rx() + RV);
    const I = E / (RI + rh.ohms + RA + rp);
    return { I, V: I * rp };
  }
  const SHOT = shot({ pos: [0, 3.6, 4.6], target: [0, 0.3, 0.1], fit: 6.2, fitH: 3.6 });
  const SHOT_METERS = shot({ pos: [0, 2.4, 3.2], target: [0, 0.5, 0.6], fit: 4.4 });

  const rhHandler = {
    down(p) {
      if (screenDist(ctx, rh.slider.children[0], p) < (p.touch ? 70 : 50) || ctx.input.pick([rh.slider])) { this.d = { x: p.x, f: rh.fraction }; return true; }
      if (screenDist(ctx, key.group, p, 0.12) < 60) { key.set(!key.closed, anim); sfx.play('click'); return true; }
      return false;
    },
    move(p) { if (!this.d) return; rh.set(this.d.f + (p.x - this.d.x) / (ctx.stage.clientWidth * 0.32)); sfx.play('knob'); },
    up() { this.d = null; },
  };
  function record() {
    if (!key.closed) { ctx.say('Insert the key: no current flows.', 'hint', 1600); return; }
    const { I, V } = solve();
    const Ir = Math.round(I / 0.02) * 0.02; const Vr = Math.round(V / 0.05) * 0.05;
    if (st.readings.some((r) => Math.abs(r.I - Ir) < 0.03)) { ctx.say('Move the rheostat to a clearly different current for each reading.', 'hint', 2400); return; }
    st.readings.push({ I: Ir, V: Vr }); sfx.play('ok');
    ui.observe(`Reading ${st.readings.length}`, `I = ${Ir.toFixed(2)} A, V = ${Vr.toFixed(2)} V`);
    hud.relabel('rec', `Record (${st.readings.length})`);
    if (st.readings.length >= 5) hud.enable('done', true);
  }

  const steps = [
    {
      title: 'Read the meters', text: 'Before switching on, know your meters: the ammeter reads to 1 A in 50 divisions, the voltmeter to 3 V in 60.', hideBelt: true, shot: SHOT_METERS,
      enter() { anim.wait(0.7, () => ui.choose(ctx.stage.clientWidth / 2, 60, 'The least count of the ammeter is', [{ label: '0.02 A', value: 1 }, { label: '0.1 A', value: 0 }, { label: '0.2 A', value: 2 }], (v) => { if (v !== 1) ctx.mistake('1 A over 50 divisions: 0.02 A per division.', 2); ui.observe('Least counts', '0.02 A, 0.05 V'); ctx.next('Ammeter in series, voltmeter across the wire.'); })); },
      exit() { ui.clearChooser(); },
    },
    {
      title: 'Close the key', text: 'The rheostat is at its full 20 Ω, so the current starts small. Insert the <b>plug key</b> (tap it).', shot: SHOT,
      skip() { key.set(true); },
      handler: { down(p) { if (screenDist(ctx, key.group, p, 0.12) > 70) return false; key.set(true, anim); sfx.play('click'); anim.wait(0.8, () => ctx.next('Both needles move.')); return true; } },
    },
    {
      title: 'Take readings', text: 'Slide the <b>rheostat</b> contact (drag it) to change the current, wait for the needles to settle, and <b>record</b>. Take at least <b>five readings</b> spread over the range. Open the key between readings if you take your time.', hint: 'Tap the key to open or close it.', shot: SHOT,
      enter() { hud.actions([{ id: 'rec', label: 'Record (0)', primary: true, onClick: record }, { id: 'done', label: 'Enough readings', disabled: st.readings.length < 5, onClick: () => { hud.actions([]); ctx.next(); } }]); },
      exit() { hud.actions([]); },
      skip() { [1, 0.7, 0.45, 0.25, 0.1, 0].forEach((f) => { rh.set(f); const { I, V } = solve(); st.readings.push({ I: Math.round(I / 0.02) * 0.02, V: Math.round(V / 0.05) * 0.05 }); }); },
      handler: rhHandler,
    },
    {
      title: 'Open the key', text: 'Take the <b>plug key</b> out so the wire cools.', shot: SHOT,
      skip() { key.set(false); },
      handler: { down(p) { if (screenDist(ctx, key.group, p, 0.12) > 70) return false; key.set(false, anim); sfx.play('click'); anim.wait(0.6, () => ctx.next('Key out.')); return true; } },
    },
    {
      title: 'V–I graph, R and resistivity', text: 'A straight line through the origin is Ohm\'s law; its slope is the resistance.', hideBelt: true, shot: SHOT,
      enter() {
        const pts = st.readings.map((r) => [r.I, r.V]); const fit = fitLine(pts); const R = fit.b; st.R = R;
        graph.draw(pts, fit, { xMax: 0.8, yMax: 3 }); graph.show(true);
        const rho = R * Math.PI * (dmm / 1000) ** 2 / 4 / (L / 100); st.rho = rho;
        const ask1 = () => ui.choose(ctx.stage.clientWidth / 2, 40, `Slope of V against I = ${R.toFixed(2)} V/A. Resistance R =`, [{ label: `${R.toFixed(2)} Ω`, value: 1 }, { label: `${(1 / R).toFixed(3)} Ω`, value: 0 }], (v) => {
          if (v !== 1) ctx.mistake('R = V / I, the slope of V against I.', 3);
          ui.observe('R', `<b>${R.toFixed(2)} Ω</b>`);
          const opts = [[rho, 'R π d² / 4L'], [R * Math.PI * (dmm / 1000) ** 2 / (L / 100), 'R π d² / L'], [R * (L / 100) / (Math.PI * (dmm / 1000) ** 2 / 4), 'R L / A']].map(([x, w]) => ({ label: `${x.toExponential(2)} Ω m  (${w})`, value: x })).sort(() => Math.random() - 0.5);
          ui.choose(ctx.stage.clientWidth / 2, 40, `L = 1.00 m, d = ${dmm.toFixed(3)} mm (screw gauge). Resistivity ρ =`, opts, (x) => {
            if (Math.abs(x - rho) / rho > 1e-6) ctx.mistake('R = ρL/A with A = πd²/4, so ρ = RA/L = Rπd²/4L.', 3);
            ui.observe('ρ', `<b>${rho.toExponential(2)} Ω m</b>`); ctx.next(`ρ = ${rho.toExponential(2)} Ω m: constantan.`, 1.2);
          });
        });
        anim.wait(1.0, ask1);
      },
      exit() { ui.clearChooser(); graph.show(false); },
    },
  ];

  const ampChip = hud.chip('ho-chip-read'); ampChip.dx = -40; ampChip.dy = -120;
  ctx.debug = { st, rh, key, solve, R0 };
  return {
    tools: [], steps,
    update(dt) {
      const { I, V } = solve();
      am.set(I); vm.set(V); am.update(dt); vm.update(dt);
      if (key.closed) {
        st.keyT += dt; st.heat = Math.min(6, st.heat + dt * I * I * 0.02);
        if (st.keyT > 90 && !st.warned) { st.warned = true; ctx.say('The key has been in a long time: the wire is warming and its resistance creeping up. Open it between readings.', 'hint', 4200); }
      } else { st.keyT = 0; st.heat = Math.max(0, st.heat - dt * 0.05); }
      ampChip.at.set(rh.group.position.x + rh.slider.position.x, BY + 0.9, rh.group.position.z);
      ampChip.set(`Rh <b>${rh.ohms.toFixed(1)}</b> Ω`).show(ctx.stepIndex === 2);
      hud.update();
    },
    result() {
      const err = ((st.R || 0) - R0) / R0 * 100;
      return { title: "Ohm's law", rows: [['Readings', String(st.readings.length)], ['Your R', `${(st.R || 0).toFixed(2)} Ω`], ['Coil (cold)', `${R0.toFixed(2)} Ω`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`], ['Resistivity', `${(st.rho || 0).toExponential(2)} Ω m`]],
        conclusion: 'V is proportional to I for a metal wire at constant temperature: Ohm\'s law. The voltmeter draws a little current of its own, and a wire left carrying current warms and reads high — which is why the key comes out between readings.' };
    },
    dispose() { hud.dispose(); graph.dispose(); },
  };
}
