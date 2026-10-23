/**
 * Statistics explorer (NEB class 10) in 3D. Every value is a ball on a wooden number line that rests
 * on a fulcrum: the fulcrum slides to the mean (the balance point of the data) and the beam tips while
 * it is off balance. Drag a ball along the beam, tap the beam to add a value, drag a ball off it to
 * remove it. The median and mode are flagged, and a histogram with the class width you choose stands
 * beside it as 3D bars with the modal class highlighted.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const SETS = {
  marks: { name: 'Marks of 12 students (out of 100)', unit: 'marks', lo: 0, hi: 100, step: 1, cw: 10, data: [45, 62, 71, 58, 62, 80, 39, 62, 74, 55, 68, 50] },
  rain: { name: 'Monthly rainfall in Kathmandu (mm)', unit: 'mm', lo: 0, hi: 400, step: 1, cw: 50, data: [12, 18, 34, 61, 148, 284, 342, 296, 187, 62, 9, 6] },
  heights: { name: 'Heights of 15 students (cm)', unit: 'cm', lo: 140, hi: 170, step: 1, cw: 5, data: [148, 152, 155, 151, 160, 149, 154, 158, 152, 150, 156, 153, 157, 151, 154] },
  family: { name: 'Family size in 20 homes', unit: 'people', lo: 0, hi: 12, step: 1, cw: 2, data: [4, 5, 6, 4, 4, 7, 3, 5, 4, 6, 8, 4, 5, 4, 6, 4, 5, 3, 4, 5] },
};
const LEN = 7.2; const BY = 1.6; const MAXB = 60;
const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const S = createChemLab(stage, { title: 'Statistics', aim: 'Mean, median and mode', subject: 'physics', target: [0, 1.4, 0.6], camera: [0.4, 3.6, 7.4], minDistance: 3, maxDistance: 14 });
  if (!S) return null;
  const { engine, world, camera, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Drag a ball, tap the beam to add one', '#2563eb');

  let set = SETS.marks; let vals = set.data.slice(); let cw = set.cw; let held = -1; let pivot = 0; let tilt = 0; let tiltV = 0;
  const X = (v) => (v - set.lo) / (set.hi - set.lo) * LEN - LEN / 2;
  const V = (x) => clamp(Math.round((set.lo + (x + LEN / 2) / LEN * (set.hi - set.lo)) / set.step) * set.step, set.lo, set.hi);

  const beamG = new THREE.Group(); beamG.position.y = BY; world.add(beamG);
  const scaleTex = () => { const c = document.createElement('canvas'); c.width = 2048; c.height = 96; const g = c.getContext('2d'); g.fillStyle = '#e8c48f'; g.fillRect(0, 0, 2048, 96); g.fillStyle = '#3b2a17'; g.font = '700 30px Poppins, system-ui, sans-serif'; g.textAlign = 'center'; const step = (set.hi - set.lo) / 10; for (let i = 0; i <= 10; i++) { const x = 24 + i / 10 * 2000; g.fillRect(x - 2, 0, 4, 34); g.fillText(String(Math.round(set.lo + i * step)), x, 76); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };
  const beamMat = [new THREE.MeshStandardMaterial({ color: 0xc89a5a, roughness: 0.6 }), new THREE.MeshStandardMaterial({ color: 0xc89a5a, roughness: 0.6 }), new THREE.MeshStandardMaterial({ color: 0xc89a5a, roughness: 0.6 }), new THREE.MeshStandardMaterial({ color: 0xc89a5a }), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.6 }), new THREE.MeshStandardMaterial({ color: 0xc89a5a })];
  const beam = new THREE.Mesh(new THREE.BoxGeometry(LEN + 0.4, 0.12, 0.5), beamMat); beam.castShadow = true; beamG.add(beam);
  const fulcrum = new THREE.Mesh(new THREE.ConeGeometry(0.32, BY - 0.06, 3), new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.4, roughness: 0.5 })); fulcrum.castShadow = true; world.add(fulcrum);
  const balls = new THREE.InstancedMesh(new THREE.SphereGeometry(0.12, 20, 14), new THREE.MeshPhysicalMaterial({ roughness: 0.25, clearcoat: 0.6 }), MAXB); balls.castShadow = true; beamG.add(balls);
  const flag = (color) => { const g = new THREE.Group(); const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.4, 8), new THREE.MeshStandardMaterial({ color: 0x334155 })); pole.position.y = 0.7; const cl = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.2), new THREE.MeshStandardMaterial({ color, side: THREE.DoubleSide })); cl.position.set(0.15, 1.3, 0); g.add(pole, cl); g.position.z = -0.32; beamG.add(g); return g; };
  const fMed = flag(0x16a34a); const fMode = flag(0xf59e0b);
  const histG = new THREE.Group(); histG.position.set(0, 0, 1.5); world.add(histG);
  const barMat = new THREE.MeshStandardMaterial({ color: 0x60a5fa, roughness: 0.5 }); const barHot = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.5 });
  let bars = [];
  const lbl = { mean: S.label(), med: S.label(), mode: S.label() };
  lbl.med.el.style.color = '#86efac'; lbl.mode.el.style.color = '#fcd34d';

  const panel = createPanel(stage, { title: 'Statistics' });
  panel.chips({ label: 'Data', options: Object.keys(SETS).map((key) => ({ value: key, label: SETS[key].name.split(' (')[0] })), value: 'marks', onChange: (v) => { set = SETS[v]; vals = set.data.slice(); cw = set.cw; cwS.set(cw); beamMat[4].map.dispose(); beamMat[4].map = scaleTex(); beamMat[4].needsUpdate = true; rebuild(); } });
  const cwS = panel.slider({ label: 'Class width', min: 1, max: 100, step: 1, value: cw, format: (v) => `${v}`, onChange: (v) => { cw = v; rebuild(); } });
  panel.buttonRow([{ label: 'Add an outlier', icon: 'add', variant: 'ghost', onClick: () => { vals.push(set.lo + (set.hi - set.lo) * (Math.random() < 0.5 ? 0.02 : 0.98)); rebuild(); } }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: () => { vals = set.data.slice(); rebuild(); } }]);
  const st = panel.stats([{ key: 'mean', label: 'Mean x̄ = Σx/n' }, { key: 'median', label: 'Median' }, { key: 'mode', label: 'Mode' }, { key: 'range', label: 'Range' }]);
  const work = panel.readout({ label: 'Working', value: '' });
  panel.info('The mean is the balance point: drag one ball far out and watch the fulcrum slide after it, while the median hardly moves. That is why the median suits skewed data such as rainfall or incomes.');

  function stats() {
    const n = vals.length; const s = vals.slice().sort((x, y) => x - y);
    const sum = vals.reduce((p, v) => p + v, 0); const mean = n ? sum / n : 0;
    const med = n ? (n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2) : 0;
    const cnt = new Map(); let best = 0; for (const v of vals) { const r = Math.round(v); const c = (cnt.get(r) || 0) + 1; cnt.set(r, c); best = Math.max(best, c); }
    const modes = best > 1 ? [...cnt.entries()].filter((e) => e[1] === best).map((e) => e[0]).sort((x, y) => x - y) : [];
    return { n, sum, mean, med, modes, best, min: s[0], max: s[n - 1] };
  }
  function rebuild() {
    bars.forEach((b) => { histG.remove(b); b.geometry.dispose(); }); bars = [];
    const c0 = Math.floor(set.lo / cw) * cw; const nb = Math.ceil((set.hi - c0) / cw) || 1;
    const counts = []; for (let i = 0; i < nb; i++) { const lo = c0 + i * cw; const hi = lo + cw; counts.push(vals.filter((v) => v >= lo && (v < hi || (i === nb - 1 && v <= hi))).length); }
    const top = Math.max(...counts, 1);
    counts.forEach((cnt, i) => { const lo = c0 + i * cw; const x0 = X(lo); const x1 = X(Math.min(set.hi, lo + cw)); const h = cnt * 0.22; const m = new THREE.Mesh(new THREE.BoxGeometry(Math.max(0.02, x1 - x0 - 0.02), Math.max(0.001, h), 0.4), cnt === top && cnt > 0 ? barHot : barMat); m.position.set((x0 + x1) / 2, h / 2 + 0.01, 0); m.castShadow = true; histG.add(m); bars.push(m); });
  }
  rebuild();

  // drag balls along the beam; tap the beam to add
  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0); const hit = new THREE.Vector3();
  const stackY = new Float32Array(MAXB);
  const at = (e) => { const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); };
  let down = null;
  engine.canvas.addEventListener('pointerdown', (e) => {
    at(e); down = { x: e.clientX, y: e.clientY };
    const h = ray.intersectObject(balls)[0];
    if (h && h.instanceId !== undefined) { held = h.instanceId; controls.enabled = false; e.stopImmediatePropagation(); }
  }, true);
  engine.canvas.addEventListener('pointermove', (e) => {
    if (held < 0) return; at(e); if (!ray.ray.intersectPlane(plane, hit)) return;
    const p = beamG.worldToLocal(hit.clone()); vals[held] = V(p.x); out = p.y < -0.9; rebuild();
  });
  let out = false;
  engine.canvas.addEventListener('pointerup', (e) => {
    if (held >= 0) { if (out && vals.length > 2) vals.splice(held, 1); held = -1; out = false; controls.enabled = true; rebuild(); return; }
    if (down && Math.hypot(e.clientX - down.x, e.clientY - down.y) < 6) { at(e); const h = ray.intersectObject(beam)[0]; if (h && vals.length < MAXB) { vals.push(V(beamG.worldToLocal(h.point.clone()).x)); rebuild(); } }
    down = null;
  });

  const m4 = new THREE.Matrix4(); const col = new THREE.Color(); const v3 = new THREE.Vector3();
  engine.setUpdate((dt) => {
    controls.update(dt);
    const s = stats();
    const mx = X(s.mean);
    // the fulcrum chases the mean; the beam tips by the torque about where the fulcrum is now
    const torque = vals.reduce((p, v) => p + (X(v) - pivot), 0) / Math.max(1, vals.length);
    pivot += (mx - pivot) * (1 - Math.exp(-dt * 1.6));
    tiltV += (-torque * 0.9 - tilt * 6) * dt; tiltV *= Math.exp(-dt * 4); tilt = clamp(tilt + tiltV * dt, -0.18, 0.18);
    beamG.position.x = pivot; beam.position.x = -pivot; beamG.rotation.z = tilt;
    balls.position.x = -pivot; fMed.position.x = X(s.med) - pivot; fMode.position.x = s.modes.length ? X(s.modes[0]) - pivot : 0; fMode.visible = s.modes.length > 0;
    fulcrum.position.set(pivot, (BY - 0.06) / 2, 0); fulcrum.rotation.y = Math.PI / 6;
    const order = vals.map((v, i) => i).sort((p, q) => vals[p] - vals[q]); const buckets = new Map();
    for (const i of order) { const key = Math.round(X(vals[i]) / 0.24); const c = buckets.get(key) || 0; buckets.set(key, c + 1); stackY[i] = c; }
    vals.forEach((v, i) => { m4.makeTranslation(X(v), 0.18 + stackY[i] * 0.235 + (i === held ? 0.15 : 0), 0); balls.setMatrixAt(i, m4); balls.setColorAt(i, col.setHex(i === held ? 0xf43f5e : 0x2563eb)); });
    balls.count = vals.length; balls.instanceMatrix.needsUpdate = true; if (balls.instanceColor) balls.instanceColor.needsUpdate = true;
    lbl.mean.el.textContent = `mean ${fmt(s.mean, 1)}`; lbl.mean.at(v3.set(pivot, 0.8 + 0.25, 0.4));
    lbl.med.el.textContent = `median ${fmt(s.med, 1)}`; lbl.med.at(beamG.localToWorld(v3.set(fMed.position.x, 1.55, -0.32)));
    lbl.mode.el.textContent = s.modes.length ? `mode ${s.modes.join(', ')}` : ''; if (s.modes.length) lbl.mode.at(beamG.localToWorld(v3.set(fMode.position.x, 1.8, -0.32))); else lbl.mode.el.style.opacity = '0';
    st.mean.set(fmt(s.mean, 2)); st.median.set(fmt(s.med, 1)); st.mode.set(s.modes.length ? s.modes.join(', ') : 'none'); st.range.set(`${fmt(s.max - s.min, 0)} ${set.unit}`);
    work.set(`Σx = ${fmt(s.sum, 0)}, n = ${s.n} → x̄ = ${fmt(s.mean, 2)}`);
    badge.set(Math.abs(mx - pivot) > 0.05 ? 'Off balance: the fulcrum slides to the new mean' : `Balanced at the mean, ${fmt(s.mean, 1)} ${set.unit}`);
  });
  engine.start();

  stage.__stats = { add: (v) => { vals.push(v); rebuild(); }, state: () => stats() };
  return { dispose() { panel.dispose(); hud.dispose(); Object.values(lbl).forEach((l) => l.remove()); S.dispose(); } };
}
