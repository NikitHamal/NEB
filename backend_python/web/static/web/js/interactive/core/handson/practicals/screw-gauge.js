// Screw gauge: find pitch and least count, close the gauge with the ratchet and read the zero
// error, then grip a copper wire and read its diameter: the last sleeve mark the thimble edge has
// uncovered (half millimetres count), plus the thimble division on the datum line times the least
// count, minus the zero error. Turning the thimble itself past contact squeezes the wire; the
// ratchet slips and clicks instead, which is why it is there.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { micrometer, PITCH, DIVS } from '../micrometer.js';
import { createHud, screenDist } from '../hud.js';

const BY = 0.8;
const LC = PITCH / DIVS;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const eDiv = [-4, -3, -2, 2, 3, 4, 5][Math.floor(Math.random() * 7)];
  const e = eDiv * LC;
  const Dmm = Math.round((0.32 + Math.random() * 0.9) * 100) / 100;
  const mic = micrometer({ zeroErrMm: e });
  mic.group.position.set(0, 0.16, 0.2); world.add(mic.group);
  const stand = mesh(new THREE.BoxGeometry(0.6, 0.02, 0.4), MAT.matte(0x1f6f5c), [0.05, 0.01, 0.2]); world.add(stand);
  const copper = new THREE.MeshStandardMaterial({ color: 0xc8794a, metalness: 1, roughness: 0.3 });
  const wire = mesh(new THREE.CylinderGeometry(Dmm * mic.MM / 2, Dmm * mic.MM / 2, 0.36, 12), copper); wire.rotation.x = Math.PI / 2;
  const WIRE_REST = new THREE.Vector3(0.12, 0.024, 0.48); wire.position.copy(WIRE_REST); wire.rotation.z = 0.25; world.add(wire);
  ctx.surfaces.push(stand);

  const st = { placed: false, gripped: false, squeezed: false, readings: [], ms: null, ts: null, ratchet: false, push: 0 };
  const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0); const hit = new THREE.Vector3();
  const contact = () => (st.placed ? Dmm : 0);

  function setGap(mm, viaRatchet) {
    const c = contact();
    if (mm < c) {
      if (!viaRatchet && cGapPrev() > c + 0.001) sfx.play('click');
      if (!viaRatchet) { st.push += (c - mm); if (st.push > 0.12 && !st.squeezed && st.placed) { st.squeezed = true; ctx.mistake('Turning the thimble past contact squeezes the wire. Close the last part with the ratchet: it slips and clicks at the right pressure.', 3); } }
      mm = c;
    } else st.push = 0;
    const was = mic.gap; mic.setGap(mm);
    if (Math.abs(mic.gap - was) > 0.02) sfx.play('knob');
    return mic.gap <= c + 1e-6;
  }
  function cGapPrev() { return mic.gap; }

  const thimbleHandler = {
    down(p) {
      if (screenDist(ctx, mic.ratchet, p) < (p.touch ? 40 : 28) || ctx.input.pick([mic.ratchet])) { st.ratchet = true; return true; }
      if (!ctx.input.pick([mic.thimble]) && screenDist(ctx, mic.thimble, p) > 70) return false;
      this.d = { x: p.x, y: p.y, g: mic.gap }; return true;
    },
    move(p) { if (!this.d) return; setGap(this.d.g + ((p.x - this.d.x) - (p.y - this.d.y)) * 0.012, false); },
    up() { this.d = null; st.ratchet = false; if (ctx.step && ctx.step.onTurned) ctx.step.onTurned(); },
    cancel() { this.d = null; st.ratchet = false; },
  };

  // reading: tap the sleeve's last visible mark and the thimble division on the datum
  const msMark = mesh(new THREE.ConeGeometry(0.004, 0.01, 3), new THREE.MeshBasicMaterial({ color: 0x2563eb, depthTest: false }), null, { cast: false }); msMark.renderOrder = 20; msMark.visible = false; world.add(msMark);
  const tsMark = mesh(new THREE.ConeGeometry(0.004, 0.01, 3), new THREE.MeshBasicMaterial({ color: 0xdc2626, depthTest: false }), null, { cast: false }); tsMark.renderOrder = 20; tsMark.visible = false; tsMark.rotation.z = Math.PI / 2; world.add(tsMark);
  const readHandler = {
    down() {
      const th = ctx.input.pick([mic.shell]);
      if (th && th.uv) {
        st.ts = mic.divisionAt(th.uv); tsMark.visible = true;
        tsMark.position.copy(th.point); world.worldToLocal(tsMark.position); tsMark.position.x -= 0.012; tsMark.position.z += 0.01;
        sfx.play('click'); refresh(); return true;
      }
      plane.constant = -(mic.group.position.z + 0.033);
      if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return false;
      world.worldToLocal(hit);
      const x = hit.x - mic.group.position.x;
      if (x < mic.S0 - 0.02 || x > mic.thimble.position.x + 0.005) return false;
      const half = Math.round((x - mic.S0) / mic.MM / 0.5) * 0.5;
      st.ms = Math.max(0, half); msMark.visible = true;
      msMark.position.set(mic.group.position.x + mic.S0 + st.ms * mic.MM, mic.group.position.y + 0.05, mic.group.position.z + 0.035);
      msMark.rotation.z = Math.PI;
      sfx.play('click'); refresh(); return true;
    },
  };
  function refresh() {
    const a = st.ms === null ? '—' : `${st.ms.toFixed(1)} mm`; const b = st.ts === null ? '—' : `${st.ts}`;
    hud.relabel('rec', `Record · MSR ${a} · CSR ${b}`); hud.enable('rec', st.ms !== null && st.ts !== null);
  }
  function startReading(cb) {
    st.ms = null; st.ts = null; msMark.visible = tsMark.visible = false;
    const x = mic.group.position.x + mic.thimble.position.x - 0.01;
    ctx.rig.go(shot({ pos: [x + 0.02, 0.19, 0.52], target: [x + 0.02, 0.16, 0.2], fov: 26, limits: { yaw: 0.35, pitch: 0.25, zMin: 0.6, zMax: 1.5 } }), 1.2);
    hud.actions([{ id: 'rec', label: 'Record reading', primary: true, disabled: true, onClick: () => cb(st.ms, st.ts) }]); refresh();
  }
  function stopReading() { hud.actions([]); msMark.visible = tsMark.visible = false; }
  function truth() { const r = mic.reading; const half = Math.floor((r + 1e-9) / 0.5) * 0.5; const ts = Math.round((r - half) / LC) % DIVS; return { ms: Math.max(0, half), ts: (ts + DIVS) % DIVS, r }; }

  const SHOT_ALL = shot({ pos: [0.1, 0.65, 1.15], target: [0.06, 0.12, 0.25], fit: 0.85 });

  const steps = [
    {
      title: 'Pitch and least count', text: 'One full turn of the thimble moves the spindle 0.5 mm, and the thimble has 50 divisions. What is the least count?', hideBelt: true, shot: SHOT_ALL,
      enter() { anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 60, 'Least count = pitch / number of thimble divisions =', [{ label: '0.01 mm', value: 1 }, { label: '0.5 mm', value: 0 }, { label: '0.1 mm', value: 2 }, { label: '0.05 mm', value: 3 }], (v) => { if (v !== 1) ctx.mistake('LC = 0.5 mm / 50 = 0.01 mm.', 3); ui.observe('Least count', '0.01 mm'); ctx.next('LC = 0.01 mm = 0.001 cm.'); })); },
      exit() { ui.clearChooser(); },
    },
    {
      title: 'Close the gauge with the ratchet', text: 'Turn the thimble (drag across it) to bring the spindle near the anvil, then <b>press and hold the ratchet</b> until it clicks.', hint: 'The ratchet is the small knob at the right end.', shot: SHOT_ALL,
      enter() { setGap(3.2, true); this.closed = false; },
      skip() { setGap(0, true); },
      onTurned() {},
      update(dt) {
        if (st.ratchet) { const done = setGap(mic.gap - 1.5 * dt, true); if (done && !this.closed) { this.closed = true; sfx.play('click'); anim.wait(0.15, () => sfx.play('click')); ctx.next('Click-click: closed at the right pressure. Is the thimble zero on the datum line?'); } }
      },
      handler: thimbleHandler,
    },
    {
      title: 'Read the zero error', text: 'Tap the <b>thimble division on the datum line</b> (and the sleeve mark at the thimble edge), then record.', hint: 'Zero below the datum (thimble edge past 0): positive, +n × LC. Zero above it: negative, −(50 − n) × LC.', shot: null,
      enter() { startReading((ms, ts) => {
        stopReading();
        const t = truth();
        if (ts !== t.ts) ctx.mistake(`Look again: division ${t.ts} is on the datum line.`, 3);
        const n = ts;
        ui.choose(ctx.stage.clientWidth / 2, 60, `Division ${n} is on the datum line. Zero error =`, [
          { label: `+${(n * LC).toFixed(2)} mm`, value: n * LC }, { label: `−${(((DIVS - n) % DIVS) * LC).toFixed(2)} mm`, value: -((DIVS - n) % DIVS) * LC }, { label: `−${(n * LC).toFixed(2)} mm`, value: -n * LC },
        ].filter((o, i, a) => a.findIndex((b) => b.label === o.label) === i), (v) => {
          if (Math.abs(v - e) > 1e-9) ctx.mistake(`The zero error is ${e > 0 ? '+' : '−'}${Math.abs(e).toFixed(2)} mm.`, 3);
          ui.observe('Zero error', `${e > 0 ? '+' : '−'}${Math.abs(e).toFixed(2)} mm`); ctx.next('Subtract it from every reading.');
        });
      }); },
      exit() { stopReading(); ui.clearChooser(); },
      handler: readHandler,
    },
    {
      title: 'Grip the wire', text: 'Open the gauge (drag the thimble), tap the <b>wire</b> to lay it on the anvil, then close with the <b>ratchet</b> until it clicks.', shot: SHOT_ALL,
      skip() { st.placed = true; wire.rotation.z = 0; wire.position.set(mic.group.position.x - 0.05 + Dmm * mic.MM / 2, mic.group.position.y, mic.group.position.z); setGap(Dmm, true); },
      update(dt) {
        if (st.ratchet) {
          const done = setGap(mic.gap - 1.5 * dt, true);
          if (done && st.placed && !this.done) { this.done = true; sfx.play('click'); anim.wait(0.15, () => sfx.play('click')); ctx.next('Gripped by the ratchet: firm, not squeezed.'); }
        }
      },
      handler: {
        down(p) {
          if (!st.placed && screenDist(ctx, wire, p) < 60) {
            if (mic.gap < Dmm + 0.3) { ctx.say('Open the gauge wider first.', 'hint', 1600); return true; }
            st.placed = true; const from = wire.position.clone(); const to = new THREE.Vector3(mic.group.position.x - 0.05 + Dmm * mic.MM / 2, mic.group.position.y, mic.group.position.z);
            anim.add(0.9, (k) => { wire.position.lerpVectors(from, to, k); wire.position.y += Math.sin(k * Math.PI) * 0.08; wire.rotation.z = 0.25 * (1 - k); }, { done: () => sfx.play('place') });
            return true;
          }
          return thimbleHandler.down.call(thimbleHandler, p);
        },
        move(p) { thimbleHandler.move.call(thimbleHandler, p); },
        up(p) { thimbleHandler.up.call(thimbleHandler, p); },
      },
    },
  ];
  for (let k = 0; k < 2; k++) {
    steps.push({
      title: k === 0 ? 'Read the diameter' : 'Turn the wire, read again', text: k === 0 ? 'Tap the <b>last sleeve mark</b> the thimble has uncovered (half millimetres count), then the <b>thimble division on the datum line</b>. Record.' : 'The wire was turned through 90° to catch any ovality. Read it again.', shot: null,
      enter() { startReading((ms, ts) => {
        const t = truth();
        if (Math.abs(ms - t.ms) > 1e-6) ctx.mistake(`The sleeve reads ${t.ms.toFixed(1)} mm: the last mark the thimble edge has uncovered, half millimetres included.`, 4);
        else if (ts !== t.ts) ctx.mistake(`Division ${t.ts} is on the datum line.`, 3);
        const R = ms + ts * LC; st.readings.push(R);
        ui.observe(`Reading ${k + 1}`, `${ms.toFixed(1)} + ${ts} × 0.01 = <b>${R.toFixed(2)} mm</b>`);
        stopReading(); ctx.next(`Observed ${R.toFixed(2)} mm.`);
      }); },
      exit() { stopReading(); },
      skip() { const t = truth(); st.readings.push(t.ms + t.ts * LC); },
      handler: readHandler,
    });
  }
  steps.push({
    title: 'Corrected diameter', text: 'Mean observed reading minus the zero error.', hideBelt: true, shot: SHOT_ALL,
    enter() {
      const mean = st.readings.reduce((a, b) => a + b, 0) / st.readings.length; const right = mean - e; st.result = right;
      const opts = [[right, 'mean − zero error'], [mean + e, 'mean + zero error'], [mean, 'mean only']].map(([v, w]) => ({ label: `${v.toFixed(3)} mm  (${w})`, value: v })).sort(() => Math.random() - 0.5);
      anim.wait(0.7, () => ui.choose(ctx.stage.clientWidth / 2, 60, `Mean observed ${mean.toFixed(3)} mm, zero error ${e > 0 ? '+' : '−'}${Math.abs(e).toFixed(2)} mm. Diameter =`, opts, (v) => {
        if (Math.abs(v - right) > 1e-9) ctx.mistake('Corrected = observed − zero error, with its sign.', 3);
        ui.observe('Diameter', `<b>${right.toFixed(3)} mm</b>`); ctx.next(`d = ${right.toFixed(3)} mm, so the cross-section is πd²/4 = ${(Math.PI * right * right / 4).toFixed(4)} mm².`, 1.2);
      }));
    },
    exit() { ui.clearChooser(); },
  });

  ctx.debug = { mic, st, e, Dmm, setGap };
  return {
    tools: [], steps,
    update() { hud.update(); },
    result() {
      return { title: 'Screw gauge', rows: [['Least count', '0.01 mm'], ['Zero error', `${e > 0 ? '+' : '−'}${Math.abs(e).toFixed(2)} mm`], ['Your diameter', `${(st.result || 0).toFixed(3)} mm`], ['True diameter', `${Dmm.toFixed(3)} mm`]],
        conclusion: `The wire is ${(st.result || 0).toFixed(2)} mm thick. One turn of the screw advances 0.5 mm, and 50 divisions split each turn, so the gauge reads to a hundredth of a millimetre: ten times finer than a vernier caliper.` };
    },
    dispose() { hud.dispose(); },
  };
}
