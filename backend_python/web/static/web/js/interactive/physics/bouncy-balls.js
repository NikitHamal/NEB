/**
 * Bouncing balls in 3D, on a little court on the school field. Tap the ground to drop a ball from the
 * set height there (or use Drop). Free flight is integrated exactly (constant gravity), each floor
 * impact is found at its true instant and the rebound speed is e × the impact speed, so every bounce
 * peaks at e² of the one before. Balls collide with each other and the boards with the same
 * coefficient of restitution, squash on impact, and the last one's height is traced in the panel.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createField, label, THREE } from './physics3d/field.js';

const WORLDS = [{ value: 'moon', label: 'Moon', g: 1.62 }, { value: 'earth', label: 'Earth', g: 9.81 }, { value: 'jupiter', label: 'Jupiter', g: 24.79 }];
const BALLS = [
  { value: 'super', label: 'Super ball', e: 0.9, r: 0.06 },
  { value: 'tennis', label: 'Tennis', e: 0.75, r: 0.067 },
  { value: 'basket', label: 'Basketball', e: 0.8, r: 0.12 },
  { value: 'clay', label: 'Clay', e: 0.15, r: 0.08 },
];
const MAX = (navigator.hardwareConcurrency || 4) <= 4 ? 10 : 18;
const HALF = 2.4;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function ballMaterial(kind) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 256; const g = c.getContext('2d');
  if (kind === 'tennis') { g.fillStyle = '#c9df3c'; g.fillRect(0, 0, 512, 256); g.strokeStyle = '#f6f8ee'; g.lineWidth = 14; g.beginPath(); for (let x = 0; x <= 512; x += 4) { const y = 128 + Math.sin(x / 512 * Math.PI * 4) * 70; if (x) g.lineTo(x, y); else g.moveTo(x, y); } g.stroke(); }
  else if (kind === 'basket') { g.fillStyle = '#d9692a'; g.fillRect(0, 0, 512, 256); g.strokeStyle = '#2a1408'; g.lineWidth = 6; g.beginPath(); g.moveTo(0, 128); g.lineTo(512, 128); [128, 384].forEach((x) => { g.moveTo(x, 0); g.lineTo(x, 256); }); g.stroke(); for (const x0 of [0, 256]) { g.beginPath(); for (let y = 0; y <= 256; y += 4) { const x = x0 + 64 + Math.sin(y / 256 * Math.PI) * 50; if (y) g.lineTo(x, y); else g.moveTo(x, y); } g.stroke(); } }
  else if (kind === 'super') { const gr = g.createLinearGradient(0, 0, 512, 0); ['#e5484d', '#f59e0b', '#22c55e', '#3b82f6', '#a855f7', '#e5484d'].forEach((col, i) => gr.addColorStop(i / 5, col)); g.fillStyle = gr; g.fillRect(0, 0, 512, 256); }
  else { g.fillStyle = '#9c7656'; g.fillRect(0, 0, 512, 256); for (let i = 0; i < 400; i++) { g.fillStyle = `rgba(60,40,25,${Math.random() * 0.25})`; g.fillRect(Math.random() * 512, Math.random() * 256, 3, 3); } }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return new THREE.MeshPhysicalMaterial({ map: t, roughness: kind === 'super' ? 0.15 : kind === 'tennis' ? 0.95 : kind === 'basket' ? 0.6 : 0.9, clearcoat: kind === 'super' ? 0.5 : 0, sheen: kind === 'tennis' ? 1 : 0, sheenColor: new THREE.Color(0xeef5c0) });
}

export default function init(stage) {
  const F = createField(stage, { camera: [3.4, 1.3, 5.0], target: [0, 1.0, 0], maxDistance: 30 });
  if (!F) return null;
  const { engine, scene, camera, controls } = F;
  { const c = F.key.shadow.camera; c.left = -6; c.right = 6; c.top = 6; c.bottom = -6; c.updateProjectionMatrix(); }
  const hud = createHud(stage);
  const badge = hud.badge('Tap the ground to drop a ball there', '#2563eb');

  let g = 9.81; let eSlider = 0.75; let kind = BALLS[1]; let dropH = 2; let slow = false;
  const B = []; let tracked = null; let simT = 0;
  const peaks = []; const trace = [];
  const mats = Object.fromEntries(BALLS.map((b) => [b.value, ballMaterial(b.value)]));
  const sphereGeo = new THREE.SphereGeometry(1, 32, 20);

  // the court: a mat, low boards and a 3.2 m height pole
  const mat = new THREE.Mesh(new THREE.BoxGeometry(HALF * 2, 0.02, HALF * 2), new THREE.MeshStandardMaterial({ color: 0x5b6f86, roughness: 0.7 })); mat.position.y = 0.01; mat.receiveShadow = true; scene.add(mat);
  const wood = new THREE.MeshStandardMaterial({ color: 0xb48552, roughness: 0.7 });
  for (const [x, z, w, d] of [[0, -HALF, HALF * 2, 0.06], [0, HALF, HALF * 2, 0.06], [-HALF, 0, 0.06, HALF * 2], [HALF, 0, 0.06, HALF * 2]]) { const b = new THREE.Mesh(new THREE.BoxGeometry(w, 0.18, d), wood); b.position.set(x, 0.09, z); b.castShadow = true; scene.add(b); }
  const poleTex = (() => { const c = document.createElement('canvas'); c.width = 64; c.height = 1024; const x = c.getContext('2d'); for (let i = 0; i < 32; i++) { x.fillStyle = i % 2 ? '#f8fafc' : '#dc2626'; x.fillRect(0, 1024 - (i + 1) * 32, 64, 32); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const pole = new THREE.Mesh(new THREE.BoxGeometry(0.08, 3.2, 0.08), new THREE.MeshStandardMaterial({ map: poleTex, roughness: 0.6 })); pole.position.set(-HALF + 0.15, 1.6, -HALF + 0.15); pole.castShadow = true; scene.add(pole);
  const mark = new THREE.Mesh(new THREE.RingGeometry(0.14, 0.17, 40), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8, side: THREE.DoubleSide })); mark.rotation.x = -Math.PI / 2; scene.add(mark);
  const peakLine = new THREE.Mesh(new THREE.PlaneGeometry(HALF * 2, 0.006), new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.8 })); scene.add(peakLine);
  const nextLine = new THREE.Mesh(new THREE.PlaneGeometry(HALF * 2, 0.006), new THREE.MeshBasicMaterial({ color: 0x22c55e, transparent: true, opacity: 0.8 })); scene.add(nextLine);
  const hLbl = label(stage, camera); const nLbl = label(stage, camera);

  const panel = createPanel(stage, { title: 'Bouncing balls' });
  panel.chips({ label: 'Ball', options: BALLS.map((b) => ({ value: b.value, label: b.label })), value: kind.value, onChange: (v) => { kind = BALLS.find((b) => b.value === v); eS.set(kind.e); eSlider = kind.e; } });
  const eS = panel.slider({ label: 'Bounciness e (restitution)', min: 0.05, max: 0.95, step: 0.05, value: kind.e, format: (v) => v.toFixed(2), onChange: (v) => { eSlider = v; B.forEach((b) => { b.e = v; }); } });
  panel.slider({ label: 'Drop height', min: 0.3, max: 3.0, step: 0.1, value: dropH, format: (v) => `${v.toFixed(1)} m`, onChange: (v) => { dropH = v; } });
  panel.chips({ label: 'World', options: WORLDS.map((w) => ({ value: w.value, label: `${w.label} · ${w.g} m/s²` })), value: 'earth', onChange: (v) => { g = WORLDS.find((w) => w.value === v).g; } });
  panel.toggle({ label: 'Slow motion (¼×)', value: false, onChange: (v) => { slow = v; } });
  panel.buttonRow([{ label: `Drop`, icon: 'south', onClick: () => spawn(0, 0) }, { label: 'Clear', icon: 'delete_sweep', variant: 'ghost', onClick: () => { B.forEach((b) => scene.remove(b.mesh)); B.length = 0; tracked = null; peaks.length = 0; trace.length = 0; } }]);
  const graph = canvasCard(panel.body, 1.8);
  const st = panel.stats([{ key: 'h', label: 'Start height' }, { key: 'next', label: 'Next peak (e²h)' }, { key: 'last', label: 'Last peak' }, { key: 'ratio', label: 'Peak ratio' }]);
  panel.info('Each bounce keeps a fraction e of the speed, so it rises to e² of the height before. On the Moon the same ball falls slowly but bounces to the same fraction.');

  function spawn(x, z) {
    if (B.length >= MAX) { const old = B.shift(); scene.remove(old.mesh); }
    const mesh = new THREE.Mesh(sphereGeo, mats[kind.value]); mesh.castShadow = true; mesh.scale.setScalar(kind.r); scene.add(mesh);
    const b = { x: Math.max(-HALF + kind.r, Math.min(HALF - kind.r, x)), y: dropH + kind.r, z: Math.max(-HALF + kind.r, Math.min(HALF - kind.r, z)), vx: 0, vy: 0, vz: 0, r: kind.r, e: eSlider, mesh, sq: 0, spin: new THREE.Vector3() };
    B.push(b); tracked = b; peaks.length = 0; peaks.push(dropH); trace.length = 0; simT = 0;
    return b;
  }

  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const ground = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); const hit = new THREE.Vector3();
  let down = null;
  engine.canvas.addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY }; });
  engine.canvas.addEventListener('pointerup', (e) => {
    if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 8) { down = null; return; }
    down = null;
    const r = engine.canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    if (ray.ray.intersectPlane(ground, hit) && Math.abs(hit.x) < HALF && Math.abs(hit.z) < HALF) spawn(hit.x, hit.z);
  });

  function advance(b, h) {
    let rem = h; let guard = 0;
    while (rem > 1e-9 && guard++ < 8) {
      const y0 = b.y - b.r;
      const tHit = b.vy < 0 || y0 > 0 ? (b.vy + Math.sqrt(Math.max(0, b.vy * b.vy + 2 * g * Math.max(0, y0)))) / g : Infinity;
      const step = Math.min(rem, tHit);
      b.x += b.vx * step; b.z += b.vz * step; b.y += b.vy * step - 0.5 * g * step * step; b.vy -= g * step; rem -= step;
      if (step === tHit) {
        b.y = b.r; const vi = -b.vy; b.vy = vi * b.e; b.vx *= 0.9; b.vz *= 0.9; b.sq = Math.min(0.45, vi * 0.05 * (1 - b.e * 0.4));
        if (b === tracked) { const apex = (b.vy * b.vy) / (2 * g); if (apex > 0.004) peaks.push(apex); }
        if (vi < 0.05) { b.vy = 0; rem = 0; }
      }
    }
    for (const [axis, v] of [['x', 'vx'], ['z', 'vz']]) {
      if (b[axis] > HALF - b.r) { b[axis] = HALF - b.r; b[v] = -Math.abs(b[v]) * b.e; }
      if (b[axis] < -HALF + b.r) { b[axis] = -HALF + b.r; b[v] = Math.abs(b[v]) * b.e; }
    }
  }
  function collide() {
    for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) {
      const a = B[i]; const c = B[j]; const dx = c.x - a.x; const dy = c.y - a.y; const dz = c.z - a.z; const d = Math.hypot(dx, dy, dz); const m = a.r + c.r;
      if (d >= m || d < 1e-6) continue;
      const nx = dx / d; const ny = dy / d; const nz = dz / d; const ov = (m - d) / 2;
      a.x -= nx * ov; a.y -= ny * ov; a.z -= nz * ov; c.x += nx * ov; c.y += ny * ov; c.z += nz * ov;
      const rel = (c.vx - a.vx) * nx + (c.vy - a.vy) * ny + (c.vz - a.vz) * nz;
      if (rel > 0) continue;
      const ma = a.r ** 3; const mc = c.r ** 3; const e = Math.min(a.e, c.e); const J = -(1 + e) * rel / (1 / ma + 1 / mc);
      a.vx -= J / ma * nx; a.vy -= J / ma * ny; a.vz -= J / ma * nz; c.vx += J / mc * nx; c.vy += J / mc * ny; c.vz += J / mc * nz;
    }
  }

  function drawGraph() {
    const { g: c, w, h } = graph.ctx();
    const ix = 32; const iy = 22; const iw = w - 42; const ih = h - 42;
    const t1 = Math.max(6, simT); const t0 = Math.max(0, t1 - 6);
    const X = (t) => ix + (t - t0) / 6 * iw; const Y = (v) => iy + ih - v / 3.2 * ih;
    c.font = '700 11px Poppins, system-ui, sans-serif'; c.fillStyle = '#e8eefb'; c.textAlign = 'left'; c.fillText('Height of the last ball', 10, 14);
    c.strokeStyle = 'rgba(160,190,255,0.18)'; c.strokeRect(ix, iy, iw, ih);
    c.strokeStyle = '#f59e0b'; c.lineWidth = 2; c.beginPath(); let f = true;
    for (const [t, v] of trace) { if (t < t0) continue; if (f) { c.moveTo(X(t), Y(v)); f = false; } else c.lineTo(X(t), Y(v)); }
    c.stroke();
    c.font = '600 9px Poppins, system-ui, sans-serif'; c.fillStyle = '#8ea0c2'; c.textAlign = 'center'; c.fillText('t / s', ix + iw / 2, h - 6);
    c.textAlign = 'right'; c.fillText('3 m', ix - 4, iy + 8); c.fillText('0', ix - 4, iy + ih);
  }

  const v3 = new THREE.Vector3(); const up = new THREE.Vector3(0, 1, 0); let tick = 0;
  engine.setUpdate((dt) => {
    controls.update(dt);
    const h = dt * (slow ? 0.25 : 1);
    const sub = 4;
    for (let s = 0; s < sub; s++) { B.forEach((b) => advance(b, h / sub)); collide(); }
    simT += h;
    for (const b of B) {
      b.sq *= Math.exp(-h * 18);
      b.mesh.position.set(b.x, b.y - b.sq * b.r * 0.5, b.z);
      b.mesh.scale.set(b.r * (1 + b.sq * 0.5), b.r * (1 - b.sq), b.r * (1 + b.sq * 0.5));
      b.mesh.rotation.x += b.vz * h / b.r; b.mesh.rotation.z -= b.vx * h / b.r;
    }
    if (tracked) { trace.push([simT, tracked.y - tracked.r]); if (trace.length > 900) trace.shift(); }
    mark.position.set(tracked ? tracked.x : 0, dropH, tracked ? tracked.z : 0); mark.visible = !!tracked;
    const last = peaks[peaks.length - 1] || dropH; const e = tracked ? tracked.e : eSlider;
    peakLine.position.set(0, last, -HALF + 0.01); peakLine.visible = !!tracked;
    nextLine.position.set(0, last * e * e, -HALF + 0.01); nextLine.visible = !!tracked && last > 0.02;
    hLbl.el.textContent = `peak ${fmt(last, 2)} m`; hLbl.at(v3.set(HALF - 0.5, last + 0.12, -HALF));
    nLbl.el.textContent = `next e²h = ${fmt(last * e * e, 2)} m`; nLbl.at(v3.set(HALF - 0.5, last * e * e + 0.12, -HALF));
    if (!tracked) { hLbl.el.style.opacity = '0'; nLbl.el.style.opacity = '0'; }
    if ((tick++ & 3) === 0) drawGraph();
    st.h.set(`${fmt(peaks[0] || dropH, 2)} m`); st.next.set(`${fmt(last * e * e, 2)} m`); st.last.set(`${fmt(last, 2)} m`);
    st.ratio.set(peaks.length > 1 ? `${fmt(peaks[peaks.length - 1] / peaks[peaks.length - 2], 3)} (e² = ${fmt(e * e, 3)})` : '—');
    badge.set(tracked ? (peaks.length > 1 ? `Each peak is e² = ${fmt(e * e, 2)} of the one before` : 'Falling…') : 'Tap the ground to drop a ball there');
    void up;
  });
  engine.start();

  stage.__bounce = { spawn, peaks: () => peaks.slice() };
  return { dispose() { panel.dispose(); hud.dispose(); hLbl.remove(); nLbl.remove(); controls.dispose(); engine.dispose(); } };
}
