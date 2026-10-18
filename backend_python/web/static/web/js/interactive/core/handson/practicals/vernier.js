// Vernier calipers: find the least count, close the jaws and find the zero error, grip a brass
// cylinder and read its diameter the way the student will in the exam: the main-scale mark just
// before the vernier zero, plus the vernier division that lines up exactly with a main-scale mark,
// times the least count, minus the zero error. Each reading is made by tapping the two marks.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { caliper } from '../caliper.js';
import { createHud, screenDist } from '../hud.js';

const BY = 0.8;
const LC = 0.1;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const e = [-0.4, -0.3, -0.2, 0.2, 0.3, 0.4, 0.5][Math.floor(Math.random() * 7)];
  const Dmm = Math.round((17 + Math.random() * 9) * 10) / 10;
  const cal = caliper({ zeroErrMm: e }); cal.group.position.set(-0.7, 0.03, 0.2); world.add(cal.group);
  const mat = mesh(new THREE.BoxGeometry(2.8, 0.03, 1.3), MAT.matte(0x1f6f5c), [0.05, 0.015, 0.35]); world.add(mat);
  const cylMat = new THREE.MeshStandardMaterial({ color: 0xc9a24a, metalness: 1, roughness: 0.28 });
  const cyl = new THREE.Group(); world.add(cyl);
  const body = mesh(new THREE.CylinderGeometry(Dmm / 200, Dmm / 200, 0.45, 48), cylMat); body.rotation.x = Math.PI / 2; cyl.add(body);
  const CYL_REST = new THREE.Vector3(0.9, Dmm / 200 + 0.03, 0.75); cyl.position.copy(CYL_REST);
  ctx.surfaces.push(mat);

  const st = { gap: 0, gripped: false, readings: [], zero: null, ms: null, vs: null, mode: null };
  const marks = new THREE.Group(); world.add(marks);
  const mkMat = (c) => new THREE.MeshBasicMaterial({ color: c, depthTest: false, transparent: true });
  const msMark = mesh(new THREE.ConeGeometry(0.006, 0.014, 3), mkMat(0x2563eb), null, { cast: false }); msMark.rotation.x = Math.PI / 2; msMark.renderOrder = 20; msMark.visible = false; marks.add(msMark);
  const vsMark = mesh(new THREE.ConeGeometry(0.006, 0.014, 3), mkMat(0xdc2626), null, { cast: false }); vsMark.rotation.x = -Math.PI / 2; vsMark.renderOrder = 20; vsMark.visible = false; marks.add(vsMark);
  const v = new THREE.Vector3(); const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);

  function setGap(mm) {
    const min = st.gripped ? Dmm : 0;
    const was = cal.gap; cal.setGap(Math.max(min, mm));
    if (st.gripped && was > Dmm + 0.05 && cal.gap <= Dmm + 0.001) sfx.play('click');
    if (Math.abs(was - cal.gap) > 0.6) sfx.play('knob');
  }
  function calX(p) { plane.constant = -(BY + 0.03 + cal.TOP); if (!ctx.input.ptr.ray.intersectPlane(plane, v)) return null; return v.x - (cal.group.position.x); }

  const slideHandler = {
    down(p) { if (screenDist(ctx, cal.slider, p) > (p.touch ? 110 : 80) && !ctx.input.pick([cal.slider])) return false; const x = calX(p); if (x === null) return false; this.d = { x, g: cal.gap }; return true; },
    move(p) { if (!this.d) return; const x = calX(p); if (x === null) return; setGap(this.d.g + (x - this.d.x) / cal.MM); },
    up() { this.d = null; if (ctx.step && ctx.step.onSlid) ctx.step.onSlid(); },
  };
  const READ_SHOT = () => { const x = cal.group.position.x + cal.vernierZeroX() + 0.045; return shot({ pos: [x, 0.42, 0.24], target: [x, 0.06, 0.2], fov: 30, limits: { yaw: 0.15, pitch: 0.12, zMin: 0.6, zMax: 1.4 } }); };

  function readHandler(onDone) {
    return {
      down(p) {
        const x = calX(p); if (x === null) return false;
        plane.constant = -(BY + 0.03 + cal.TOP);
        const z = v.z - cal.group.position.z;
        const vz = cal.vernierZeroX();
        if (z < 0.036) { const mm = Math.round(x / cal.MM); st.ms = mm; msMark.visible = true; msMark.position.set(cal.group.position.x + mm * cal.MM, 0.03 + cal.TOP + 0.002, cal.group.position.z - 0.068); }
        else { const n = clamp(Math.round((x - vz) / (0.9 * cal.MM)), 0, 10); st.vs = n; vsMark.visible = true; vsMark.position.set(cal.group.position.x + vz + n * 0.9 * cal.MM, 0.03 + cal.TOP + 0.03, cal.group.position.z + 0.092); }
        sfx.play('click'); refreshChip();
        hud.enable('rec', st.ms !== null && st.vs !== null);
        return true;
      },
    };
  }
  function refreshChip() {
    const a = st.ms === null ? '—' : `${(st.ms / 10).toFixed(1)} cm`; const b = st.vs === null ? '—' : `${st.vs}`;
    hud.relabel('rec', `Record · MSR ${a} · VSD ${b}`);
  }
  function startReading(cb) {
    st.ms = null; st.vs = null; msMark.visible = vsMark.visible = false;
    ctx.rig.go(READ_SHOT(), 1.2);
    hud.actions([{ id: 'rec', label: 'Record reading', primary: true, disabled: true, onClick: () => cb(st.ms, st.vs) }]); refreshChip();
  }
  function stopReading() { hud.actions([]); msMark.visible = vsMark.visible = false; }
  function truth() { const r = cal.reading; const ms = Math.floor(r + 1e-6); const n = Math.round((r - ms) / LC); return { ms: n === 10 ? ms + 1 : ms, vs: n % 10, r }; }

  const SHOT_ALL = shot({ pos: [0.2, 1.7, 2.2], target: [0.05, 0.05, 0.35], fit: 2.4 });
  const SHOT_JAWS = shot({ pos: [-0.5, 0.95, 1.35], target: [-0.45, 0.04, 0.35], fov: 32 });

  const steps = [
    {
      title: 'Find the least count', text: 'Ten vernier divisions span nine main-scale millimetres. What is the least count?', hideBelt: true, shot: SHOT_ALL,
      enter() { anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 60, '1 MSD = 1 mm, 10 VSD = 9 MSD. Least count = 1 MSD − 1 VSD =', [{ label: '0.1 mm = 0.01 cm', value: 1 }, { label: '0.9 mm', value: 0 }, { label: '1 mm', value: 2 }, { label: '0.01 mm', value: 3 }], (x) => { if (x !== 1) ctx.mistake('1 VSD = 9/10 MSD = 0.9 mm, so LC = 1 − 0.9 = 0.1 mm.', 3); ui.observe('Least count', '0.01 cm'); ctx.next('LC = 0.1 mm = 0.01 cm.'); })); },
      exit() { ui.clearChooser(); },
    },
    {
      title: 'Close the jaws', text: 'Drag the <b>slider</b> (or its thumb wheel) all the way left until the jaws touch.', shot: SHOT_JAWS,
      skip() { setGap(0); },
      enter() { setGap(12); },
      onSlid() { if (cal.gap < 0.001 && !this.done) { this.done = true; ctx.next('Jaws closed. Does the vernier zero sit on the main-scale zero?'); } },
      handler: slideHandler,
    },
    {
      title: 'Zero error', text: 'Tap the <b>vernier division that lines up</b> with a main-scale mark (and the main-scale mark just before the vernier zero), then record.', hint: 'Zero right of the main zero: positive error = n × LC. Left of it: negative error = −(10 − n) × LC.', shot: null,
      enter() { startReading((ms, vs) => {
        stopReading();
        const pos = e > 0; const n = vs;
        const opts = [{ label: `+${(n * LC / 10).toFixed(2)} cm`, value: n * LC }, { label: `−${(((10 - n) % 10) * LC / 10).toFixed(2)} cm`, value: -((10 - n) % 10) * LC }, { label: `−${(n * LC / 10).toFixed(2)} cm`, value: -n * LC }]
          .filter((o, i, a) => a.findIndex((b) => b.label === o.label) === i);
        if (vs !== truth().vs) ctx.mistake(`Look again: division ${truth().vs} is the one that lines up exactly.`, 3);
        ui.choose(ctx.stage.clientWidth / 2, 60, `Vernier zero is ${pos ? 'right' : 'left'} of the main zero; division ${n} coincides. Zero error =`, opts, (val) => {
          if (Math.abs(val - e) > 1e-6) ctx.mistake(`The zero error is ${e > 0 ? '+' : '−'}${Math.abs(e / 10).toFixed(2)} cm: ${e > 0 ? 'right of zero, so +n × LC' : 'left of zero, so −(10 − n) × LC'}.`, 3);
          st.zero = e; ui.observe('Zero error', `${e > 0 ? '+' : '−'}${Math.abs(e / 10).toFixed(2)} cm`); ctx.next(`Zero error ${e > 0 ? '+' : '−'}${Math.abs(e / 10).toFixed(2)} cm: subtract it from every reading.`);
        });
      }); },
      exit() { stopReading(); ui.clearChooser(); },
      skip() { st.zero = e; },
      handler: readHandler(),
    },
    {
      title: 'Grip the cylinder', text: 'Open the jaws wider than the cylinder, tap the <b>cylinder</b> to put it between them, then slide the jaw back until it <b>just touches</b>. Do not force it.', shot: SHOT_JAWS,
      enter() { this.placed = false; },
      skip() { st.gripped = true; cyl.position.set(cal.group.position.x + Dmm / 200, CYL_REST.y, cal.group.position.z + 0.3); setGap(Dmm); },
      onSlid() { if (this.placed && cal.gap <= Dmm + 0.001 && !this.done) { this.done = true; ctx.next('Gripped: firm, not squeezed.'); } },
      handler: {
        down(p) {
          if (!this.placedRef && screenDist(ctx, cyl, p) < 70) {
            const s = ctx.step; if (s.placed) return true;
            if (cal.gap < Dmm + 1) { ctx.say('Open the jaws wider first.', 'hint', 1600); return true; }
            s.placed = true; st.gripped = true; const from = cyl.position.clone(); const to = new THREE.Vector3(cal.group.position.x + Dmm / 200, CYL_REST.y, cal.group.position.z + 0.3);
            anim.add(0.9, (k) => { cyl.position.lerpVectors(from, to, k); cyl.position.y += Math.sin(k * Math.PI) * 0.15; }, { done: () => sfx.play('place') });
            return true;
          }
          return slideHandler.down.call(slideHandler, p);
        },
        move(p) { slideHandler.move.call(slideHandler, p); },
        up(p) { slideHandler.up.call(slideHandler, p); },
      },
    },
  ];
  for (let k = 0; k < 2; k++) {
    steps.push({
      title: k === 0 ? 'Read the diameter' : 'Turn and read again', text: k === 0 ? 'Tap the <b>main-scale mark just before</b> the vernier zero, then the <b>vernier division that coincides</b>. Record.' : 'The cylinder was turned through 90°. Read it again the same way.', hint: 'Reading = MSR + (coinciding VSD × LC). The vernier zero itself is the pointer.', shot: null,
      enter() {
        if (k === 1) { cyl.rotation.z = Math.PI / 2; }
        startReading((ms, vs) => {
          const t = truth();
          if (ms !== t.ms) ctx.mistake(`The main-scale reading is ${(t.ms / 10).toFixed(1)} cm: the last mark the vernier zero has passed.`, 4);
          else if (vs !== t.vs) ctx.mistake(`Division ${t.vs} is the one that lines up exactly with a main-scale mark.`, 3);
          const R = ms + vs * LC; st.readings.push(R);
          ui.observe(`Reading ${k + 1}`, `${(ms / 10).toFixed(1)} + ${vs} × 0.01 = <b>${(R / 10).toFixed(2)} cm</b>`);
          stopReading(); ctx.next(`Observed ${(R / 10).toFixed(2)} cm.`);
        });
      },
      exit() { stopReading(); },
      skip() { const t = truth(); st.readings.push(t.ms + t.vs * LC); },
      handler: readHandler(),
    });
  }
  steps.push({
    title: 'Correct for the zero error', text: 'Mean observed reading minus the zero error.', hideBelt: true, shot: SHOT_ALL,
    enter() {
      const mean = st.readings.reduce((a, b) => a + b, 0) / st.readings.length; const right = mean - e; st.result = right;
      const opts = [[right, 'mean − zero error'], [mean + e, 'mean + zero error'], [mean, 'mean only']].map(([val, w]) => ({ label: `${(val / 10).toFixed(3)} cm  (${w})`, value: val })).sort(() => Math.random() - 0.5);
      anim.wait(0.7, () => ui.choose(ctx.stage.clientWidth / 2, 60, `Mean observed = ${(mean / 10).toFixed(3)} cm, zero error = ${e > 0 ? '+' : '−'}${Math.abs(e / 10).toFixed(2)} cm. Corrected diameter?`, opts, (val) => {
        if (Math.abs(val - right) > 1e-9) ctx.mistake('Corrected reading = observed − zero error (with its sign).', 3);
        ui.observe('Diameter', `<b>${(right / 10).toFixed(3)} cm</b>`); ctx.next(`D = ${(right / 10).toFixed(3)} cm.`, 1.2);
      }));
    },
    exit() { ui.clearChooser(); },
  });

  ctx.debug = { cal, st, e, Dmm, setGap };
  return {
    tools: [], steps,
    update() { hud.update(); },
    result() {
      return { title: 'Vernier calipers', rows: [['Least count', '0.01 cm'], ['Zero error', `${e > 0 ? '+' : '−'}${Math.abs(e / 10).toFixed(2)} cm`], ['Your diameter', `${((st.result || 0) / 10).toFixed(3)} cm`], ['True diameter', `${(Dmm / 10).toFixed(3)} cm`]],
        conclusion: `The diameter of the cylinder is ${((st.result || 0) / 10).toFixed(2)} cm. A vernier lets a 1 mm scale be read to 0.1 mm because the vernier divisions are each 0.1 mm shorter than the main-scale ones: the one that lines up tells you how far past the last millimetre the zero has gone.` };
    },
    dispose() { hud.dispose(); },
  };
}
