// Hooke's law: a steel spring hangs from a stand beside a vertical metre scale, with a pointer
// at its lower end and a 50 g hanger. The student adds slotted 50 g masses one at a time (tap the
// stack), lets the bounce settle (the spring really oscillates, ω = √(k/m), lightly damped), reads
// the pointer on the scale by tapping it, and records. Loading then unloading checks the elastic
// limit; F against extension gives k from the slope.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { createGraph, fitLine } from '../stopwatch.js';

const BY = 0.8; const G = 9.8;
const TOP = 6.0; const L0 = 1.2; const HANGER = 0.05;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

function scaleTex() {
  return canvasTexture('ho-hooke-scale', 160, 4096, (g, w, h) => {
    g.fillStyle = '#f6edd2'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827';
    for (let mm = 0; mm <= 500; mm++) {
      const y = 20 + (h - 40) * mm / 500; const cm = mm % 10 === 0; const five = mm % 5 === 0;
      g.fillRect(0, Math.round(y - (cm ? 1.5 : 0.8)), cm ? 70 : five ? 46 : 28, cm ? 3 : 1.6);
      if (cm) { g.font = '700 34px system-ui, sans-serif'; g.textBaseline = 'middle'; g.fillText(String(mm / 10), 80, y); }
    }
  }, { anisotropy: 16 });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'Load against extension', xLabel: 'extension x (cm)', yLabel: 'F (N)' });
  const k = Math.round(15 + Math.random() * 15);

  world.add(mesh(new THREE.BoxGeometry(1.4, 0.08, 1.0), MAT.matte(0x2b3138), [0, 0.04, 0]));
  world.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 6.4, 16), MAT.steel(), [-0.55, 3.2, -0.2]));
  const arm = mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.65, 10), MAT.steel(), [-0.25, TOP, -0.2]); arm.rotation.z = Math.PI / 2; world.add(arm);
  world.add(mesh(new THREE.BoxGeometry(0.12, 0.12, 0.12), MAT.matte(0x30363d), [-0.55, TOP, -0.2]));
  const scale = mesh(new THREE.BoxGeometry(0.2, 5.0, 0.03), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.6 }), [0.32, TOP - 0.3 - 2.5, -0.18]); world.add(scale);
  const springMat = MAT.steel();
  const spring = new THREE.Mesh(new THREE.BufferGeometry(), springMat); world.add(spring);
  const pointer = mesh(new THREE.BoxGeometry(0.34, 0.012, 0.012), MAT.ink(0xb91c1c), [0.12, 0, -0.1]); world.add(pointer);
  const hanger = new THREE.Group(); world.add(hanger);
  hanger.add(mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.5, 8), MAT.brushed(), [0, -0.25, 0]));
  hanger.add(mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.025, 28), MAT.brushed(), [0, -0.5, 0]));
  const slot = (y) => mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.05, 28), MAT.gloss(0x9a7b3a), [0, y, 0]);
  const onHanger = [];
  const shelf = mesh(new THREE.BoxGeometry(0.6, 0.05, 0.5), MAT.gloss(0x8a5a33), [1.0, TOP - 3.05, 0.3]); world.add(shelf);
  world.add(mesh(new THREE.CylinderGeometry(0.025, 0.025, TOP - 3.05, 10), MAT.steel(), [1.0, (TOP - 3.05) / 2, 0.3]));
  const stack = new THREE.Group(); stack.position.set(1.0, TOP - 3.02, 0.3); world.add(stack);
  const stackDiscs = []; for (let i = 0; i < 8; i++) { const d = slot(0.025 + i * 0.052); stack.add(d); stackDiscs.push(d); }

  const st = { m: HANGER, y: 0, v: 0, readings: [], unloading: false, prevLoads: new Set() };
  const restY = () => TOP - 0.06 - L0 - (st.m * G / k) * 10;
  st.y = restY();
  function build() {
    const top = TOP - 0.06; const bot = st.y; const coils = 22; const r = 0.07; const pts = [];
    pts.push(new THREE.Vector3(0, top + 0.06, 0));
    for (let i = 0; i <= coils * 12; i++) { const t = i / (coils * 12); const a = t * coils * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(a) * r, top - (top - bot) * (0.04 + 0.92 * t), Math.sin(a) * r)); }
    pts.push(new THREE.Vector3(0, bot, 0));
    spring.geometry.dispose(); spring.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), coils * 14, 0.008, 6);
    pointer.position.y = bot; hanger.position.set(0, bot, 0);
  }
  function addMass(sign) {
    if (sign > 0 && onHanger.length >= 8) { ctx.say('That is all the slotted masses (450 g with the hanger).', 'hint', 2000); return; }
    if (sign < 0 && !onHanger.length) return;
    sfx.play('place');
    if (sign > 0) { const d = stackDiscs[7 - onHanger.length]; d.visible = false; const s = slot(-0.5 + 0.04 + onHanger.length * 0.052); hanger.add(s); onHanger.push(s); }
    else { const s = onHanger.pop(); hanger.remove(s); stackDiscs[7 - onHanger.length].visible = true; }
    st.m = HANGER + onHanger.length * 0.05;
    st.v += sign * 0.25;
  }
  const readingAt = () => (TOP - 0.3 - st.y) * 10; // cm on the scale, 0 at its top
  const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0.165); const hit = new THREE.Vector3();
  const marker = mesh(new THREE.BoxGeometry(0.24, 0.006, 0.006), new THREE.MeshBasicMaterial({ color: 0x2563eb, depthTest: false }), null, { cast: false }); marker.renderOrder = 20; marker.visible = false; world.add(marker);
  let tapped = null;

  const SHOT = shot({ pos: [1.5, TOP - 1.6, 5.4], target: [0.1, TOP - 2.2, 0], fitH: 5.4 });
  const READ = () => shot({ pos: [0.2, st.y, 1.1], target: [0.2, st.y, -0.1], fov: 22, limits: { yaw: 0.2, pitch: 0.12, zMin: 0.7, zMax: 1.4 } });

  const steps = [
    {
      title: 'Read the unloaded position', text: 'Only the 50 g hanger is on. When it is still, tap the <b>scale</b> exactly where the <b>red pointer</b> is, then record.', hideBelt: true, shot: null,
      enter() { ctx.rig.go(READ(), 1.2); startRead(); },
      exit() { hud.actions([]); marker.visible = false; },
      skip() { st.readings.push({ m: st.m, r: readingAt() }); },
      handler: readHandler(),
    },
    {
      title: 'Load the spring', text: 'Tap the <b>stack of slotted masses</b> to add 50 g at a time. After each one, wait for the bounce to die away, tap the scale at the pointer and record. Take at least <b>five loadings</b>; then take masses off again (tap the hanger) and check it returns.', hint: 'Read at eye level, when the pointer is still.', shot: SHOT, hideBelt: true,
      enter() { startRead(true); },
      exit() { hud.actions([]); marker.visible = false; },
      skip() { while (onHanger.length < 6) { addMass(1); st.y = restY(); st.v = 0; st.readings.push({ m: st.m, r: readingAt() }); } },
      handler: Object.assign(readHandler(), {
        down(p) {
          if (hits(ctx, stack, p, 60, 0.2)) { addMass(1); tapped = null; marker.visible = false; refresh(); return true; }
          if (hits(ctx, hanger, p, 50, -0.3)) { addMass(-1); tapped = null; marker.visible = false; refresh(); return true; }
          return readHandler().down(p);
        },
      }),
    },
    {
      title: 'F against x, and k', text: 'Plot load F = mg against extension x. A straight line through the origin is Hooke\'s law; its slope is the spring constant.', hideBelt: true, shot: SHOT,
      enter() {
        const base = st.readings.find((r) => Math.abs(r.m - HANGER) < 1e-6) || st.readings[0];
        const pts = st.readings.filter((r) => r.m > HANGER + 1e-6).map((r) => [r.r - base.r, (r.m - HANGER) * G]);
        const fit = fitLine(pts); graph.draw(pts, fit, { xMax: Math.max(4, ...pts.map((q) => q[0])) * 1.15, yMax: 4.5 }); graph.show(true);
        const kk = fit.b * 100; st.k = kk;
        const opts = [[kk, 'slope × 100 (cm → m)'], [fit.b, 'slope as it is'], [1 / fit.b * 100, '100 / slope']].map(([v, w]) => ({ label: `${v.toFixed(1)} N/m  (${w})`, value: v })).sort(() => Math.random() - 0.5);
        anim.wait(1.0, () => ui.choose(ctx.stage.clientWidth / 2, 40, `Slope = ${fit.b.toFixed(3)} N per cm. Spring constant k =`, opts, (v) => {
          if (Math.abs(v - kk) > 1e-6) ctx.mistake('k = F / x with x in metres: N per cm × 100 = N per m.', 3);
          ui.observe('k', `<b>${kk.toFixed(1)} N/m</b>`); ctx.next(`k = ${kk.toFixed(1)} N/m.`, 1.2);
        }));
      },
      exit() { ui.clearChooser(); graph.show(false); },
    },
  ];

  function refresh() { hud.relabel('rec', tapped === null ? `Record (${st.readings.length})` : `Record ${tapped.toFixed(1)} cm (${st.readings.length})`); }
  function startRead(multi) {
    tapped = null; marker.visible = false;
    const b = [{ id: 'rec', label: 'Record (0)', primary: true, onClick: () => {
      if (tapped === null) { ctx.say('Tap the scale where the pointer is.', 'hint', 1600); return; }
      if (Math.abs(st.v) > 0.03) { ctx.say('Wait for the bounce to stop before reading.', 'hint', 1800); return; }
      const truth = readingAt();
      if (Math.abs(tapped - truth) > 0.15) { ctx.mistake(`The pointer is at ${truth.toFixed(1)} cm, not ${tapped.toFixed(1)} cm. Read at eye level, level with the pointer.`, 3); return; }
      st.readings.push({ m: st.m, r: tapped }); sfx.play('ok');
      ui.observe(`${Math.round(st.m * 1000)} g`, `${tapped.toFixed(1)} cm`);
      tapped = null; marker.visible = false; refresh();
      if (!multi) { hud.actions([]); ctx.next('Zero reading recorded.'); }
      else if (st.readings.length >= 6) hud.enable('done', true);
    } }];
    if (multi) b.push({ id: 'done', label: 'Plot the graph', disabled: st.readings.length < 6, onClick: () => { hud.actions([]); ctx.next(); } });
    hud.actions(b); refresh();
  }
  function readHandler() {
    return {
      down() {
        if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return false;
        world.worldToLocal(hit);
        if (Math.abs(hit.x - 0.32) > 0.25) return false;
        tapped = Math.round((TOP - 0.3 - hit.y) * 100) / 10; marker.visible = true; marker.position.set(0.32, TOP - 0.3 - tapped / 10, -0.15);
        sfx.play('click'); refresh(); return true;
      },
    };
  }

  ctx.debug = { st, k, addMass };
  build();
  return {
    tools: [], steps,
    update(dt) {
      const m = st.m; const target = restY();
      const n = Math.max(1, Math.ceil(dt / 0.004)); const h = dt / n;
      for (let i = 0; i < n; i++) { const a = -(k / m) * (st.y - target) - 1.6 * st.v; st.v += a * h; st.y += st.v * h; }
      st.y = clamp(st.y, TOP - 6, TOP); build();
      hud.update();
    },
    result() {
      const err = ((st.k || 0) - k) / k * 100;
      return { title: "Hooke's law", rows: [['Readings', String(st.readings.length)], ['Your k', `${(st.k || 0).toFixed(1)} N/m`], ['Spring', `${k} N/m`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: 'Within the elastic limit the extension is proportional to the load (F = kx): the line is straight and goes through the origin, and unloading retraces it.' };
    },
    dispose() { hud.dispose(); graph.dispose(); },
  };
}
