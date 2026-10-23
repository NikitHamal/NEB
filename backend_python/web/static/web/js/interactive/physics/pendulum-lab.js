/**
 * Pendulum lab in 3D — a simple pendulum on a tall stand over the physics bench, solved exactly
 * (θ'' = −(g/L) sin θ − bθ', RK4 at 480 Hz). Drag the bob in its plane to set both the angle and the
 * length; release and it swings. The period is timed from the motion itself (interpolated zero
 * crossings) and compared with the small-angle formula 2π√(L/g) and the exact large-amplitude period
 * (via the arithmetic–geometric mean).
 */
import { makeRK4 } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const WORLDS = [
  { value: 'moon', label: 'Moon', g: 1.62 }, { value: 'mars', label: 'Mars', g: 3.71 },
  { value: 'earth', label: 'Earth', g: 9.81 }, { value: 'jupiter', label: 'Jupiter', g: 24.79 },
];
const DEG = Math.PI / 180; const H = 1 / 480; const U = 10; const PIVOT = 23;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });
function agm(a, b) { for (let i = 0; i < 12; i++) { const an = (a + b) / 2; b = Math.sqrt(a * b); a = an; } return a; }

function protractorTexture() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 512;
  const g = c.getContext('2d'); const cx = 512; const cy = 0;
  g.fillStyle = 'rgba(236,244,255,0.55)'; g.beginPath(); g.arc(cx, cy, 500, 0, Math.PI); g.fill();
  g.strokeStyle = '#1e3a5f'; g.fillStyle = '#1e3a5f'; g.font = '700 26px Poppins, system-ui, sans-serif'; g.textAlign = 'center';
  for (let a = -90; a <= 90; a += 1) {
    const t = (90 + a) * DEG; const l = a % 10 === 0 ? 46 : a % 5 === 0 ? 30 : 16;
    g.lineWidth = a % 10 === 0 ? 3 : 1.5;
    g.beginPath(); g.moveTo(cx + Math.cos(t) * 500, cy + Math.sin(t) * 500); g.lineTo(cx + Math.cos(t) * (500 - l), cy + Math.sin(t) * (500 - l)); g.stroke();
    if (a % 30 === 0) g.fillText(`${Math.abs(a)}°`, cx + Math.cos(t) * 420, cy + Math.sin(t) * 420 + 10);
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}

export default function init(stage) {
  const S = createChemLab(stage, { title: 'Pendulum lab', aim: 'The period of a simple pendulum', subject: 'physics', target: [0, 16, 0], camera: [3, 15, 22], minDistance: 3, maxDistance: 60 });
  if (!S) return null;
  const { engine, world, camera, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Drag the bob, then let go', '#2563eb');

  let L = 1.0; let g = 9.81; let mass = 0.2; let damping = false; let paused = false; let dragging = false;
  const y = new Float64Array(2); y[0] = 20 * DEG;
  let amp0 = y[0]; let simT = 0; let acc = 0; let lastCross = -1; let measuredT = 0; let crossings = 0;
  const trace = [];
  const rk = makeRK4(2, (t, s, out) => { out[0] = s[1]; out[1] = -(g / L) * Math.sin(s[0]) - (damping ? 0.18 : 0) * s[1]; });

  const steel = new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.85, roughness: 0.3 });
  const upper = new THREE.Mesh(new THREE.PlaneGeometry(80, 30), new THREE.MeshStandardMaterial({ color: 0xeceae4, roughness: 0.92 }));
  upper.position.set(0, 17.8 + 15 - 0.8 - 0.05, -4.2 - 0.01); upper.receiveShadow = true; world.add(upper);
  const base = new THREE.Mesh(new THREE.BoxGeometry(5, 0.4, 3), new THREE.MeshStandardMaterial({ color: 0x2b2f36, roughness: 0.6 })); base.position.set(-3, 0.2, -1); base.castShadow = true; world.add(base);
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, PIVOT + 1.5, 20), steel); rod.position.set(-4.5, (PIVOT + 1.5) / 2, -1.5); rod.castShadow = true; world.add(rod);
  const boss = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.6, 0.7), steel); boss.position.set(-4.5, PIVOT, -1.5); world.add(boss);
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 4.9, 12), steel); arm.rotation.z = Math.PI / 2; arm.position.set(-2.1, PIVOT, -1.5); arm.rotation.y = -0.55; world.add(arm);
  const cork = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.36, 0.7, 20), new THREE.MeshStandardMaterial({ color: 0xb98552, roughness: 0.95 })); cork.position.set(0, PIVOT + 0.25, 0); world.add(cork);
  const prot = new THREE.Mesh(new THREE.PlaneGeometry(9, 4.5), new THREE.MeshStandardMaterial({ map: protractorTexture(), transparent: true, side: THREE.DoubleSide, depthWrite: false, roughness: 0.3 }));
  prot.position.set(0, PIVOT - 2.25, -0.06); prot.renderOrder = 3; world.add(prot);
  const string = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 1, 6), new THREE.MeshStandardMaterial({ color: 0xf5f0e6, roughness: 0.9 }));
  world.add(string);
  const bob = new THREE.Mesh(new THREE.SphereGeometry(1, 40, 24), new THREE.MeshStandardMaterial({ color: 0xd4a843, metalness: 0.9, roughness: 0.22 }));
  bob.castShadow = true; world.add(bob);
  const hook = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.03, 6, 16), steel); world.add(hook);
  const ghostMat = new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.18, depthWrite: false });
  const ghosts = [new THREE.Mesh(new THREE.SphereGeometry(1, 20, 12), ghostMat), new THREE.Mesh(new THREE.SphereGeometry(1, 20, 12), ghostMat)];
  ghosts.forEach((m) => world.add(m));
  const trailN = 64; const trailPos = new Float32Array(trailN * 3); const trailA = new Float32Array(trailN);
  const trailGeo = new THREE.BufferGeometry(); trailGeo.setAttribute('position', new THREE.BufferAttribute(trailPos, 3)); trailGeo.setAttribute('a', new THREE.BufferAttribute(trailA, 1));
  const trail = new THREE.Line(trailGeo, new THREE.ShaderMaterial({ vertexShader: 'attribute float a; varying float vA; void main() { vA = a; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }', fragmentShader: 'varying float vA; void main() { gl_FragColor = vec4(0.38, 0.65, 0.98, vA * 0.8); }', transparent: true, depthWrite: false }));
  trail.frustumCulled = false; world.add(trail);
  const trailPts = [];
  const angleLbl = S.label(); const lenLbl = S.label();

  const panel = createPanel(stage, { title: 'Pendulum' });
  const lenS = panel.slider({ label: 'Length L', min: 0.2, max: 2, step: 0.05, value: L, format: (v) => `${v.toFixed(2)} m`, onChange: (v) => { L = v; restart(y[0]); } });
  panel.chips({ label: 'Where is the lab?', options: WORLDS.map((w) => ({ value: w.value, label: w.label })), value: 'earth', onChange: (v) => { g = WORLDS.find((w) => w.value === v).g; restart(y[0]); } });
  panel.slider({ label: 'Bob mass', min: 0.05, max: 1, step: 0.05, value: mass, format: (v) => `${(v * 1000).toFixed(0)} g`, onChange: (v) => { mass = v; } });
  panel.toggle({ label: 'Air damping', value: false, onChange: (v) => { damping = v; } });
  const [playB] = panel.buttonRow([
    { label: 'Pause', icon: 'pause', onClick: () => { paused = !paused; playB.setLabel(paused ? 'Play' : 'Pause'); } },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: () => restart(20 * DEG) },
  ]);
  const graph = canvasCard(panel.body, 1.8);
  const st = panel.stats([{ key: 'meas', label: 'Measured T' }, { key: 'small', label: '2π√(L/g)' }, { key: 'exact', label: 'Exact T' }, { key: 'swings', label: 'Swings' }]);
  panel.info('Drag the bob sideways to set the angle and up or down to change the length. Try 10° and 60°: only the big swing is slower than 2π√(L/g). The mass makes no difference.');

  function restart(a) { y[0] = a; y[1] = 0; amp0 = Math.abs(a); simT = 0; acc = 0; lastCross = -1; measuredT = 0; crossings = 0; trace.length = 0; trailPts.length = 0; }

  // drag the bob in its swing plane (z = 0)
  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0); const hit = new THREE.Vector3();
  const pivotW = new THREE.Vector3();
  function planeAt(e) {
    const r = engine.canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    return ray.ray.intersectPlane(plane, hit);
  }
  function onDown(e) {
    const r = engine.canvas.getBoundingClientRect(); const v = bob.getWorldPosition(new THREE.Vector3()).project(camera);
    const px = (v.x + 1) / 2 * r.width + r.left; const py = (1 - v.y) / 2 * r.height + r.top;
    const rad = Math.max(24, bob.scale.x / camera.position.distanceTo(bob.getWorldPosition(new THREE.Vector3())) * r.height * 1.2);
    if (Math.hypot(px - e.clientX, py - e.clientY) > rad) return;
    dragging = true; controls.enabled = false; e.stopImmediatePropagation(); engine.canvas.setPointerCapture && engine.canvas.setPointerCapture(e.pointerId);
  }
  function onMove(e) {
    if (!dragging) return;
    if (!planeAt(e)) return;
    world.localToWorld(pivotW.set(0, PIVOT, 0));
    const dx = (hit.x - pivotW.x) / U; const dy = (pivotW.y - hit.y) / U;
    L = Math.min(2, Math.max(0.2, Math.round(Math.hypot(dx, dy) * 20) / 20)); lenS.set(L);
    y[0] = Math.max(-80 * DEG, Math.min(80 * DEG, Math.atan2(dx, Math.max(0.01, dy)))); y[1] = 0;
  }
  function onUp() { if (dragging) { dragging = false; controls.enabled = true; restart(y[0]); } }
  engine.canvas.addEventListener('pointerdown', onDown, true);
  engine.canvas.addEventListener('pointermove', onMove);
  engine.canvas.addEventListener('pointerup', onUp);

  function drawGraph() {
    const { g: c, w, h } = graph.ctx();
    const ix = 32; const iy = 22; const iw = w - 42; const ih = h - 42;
    const t1 = Math.max(10, simT); const t0 = Math.max(0, t1 - 10);
    const X = (t) => ix + (t - t0) / 10 * iw; const Y = (a) => iy + ih / 2 - a / 90 * ih / 2;
    c.font = '700 11px Poppins, system-ui, sans-serif'; c.fillStyle = '#e8eefb'; c.textAlign = 'left'; c.fillText('Angle θ against time', 10, 14);
    c.strokeStyle = 'rgba(160,190,255,0.18)'; c.strokeRect(ix, iy, iw, ih); c.beginPath(); c.moveTo(ix, Y(0)); c.lineTo(ix + iw, Y(0)); c.stroke();
    c.strokeStyle = '#60a5fa'; c.lineWidth = 2; c.beginPath(); let first = true;
    for (const [t, a] of trace) { if (t < t0) continue; if (first) { c.moveTo(X(t), Y(a)); first = false; } else c.lineTo(X(t), Y(a)); }
    c.stroke();
    c.font = '600 9px Poppins, system-ui, sans-serif'; c.fillStyle = '#8ea0c2'; c.textAlign = 'center'; c.fillText('t / s', ix + iw / 2, h - 6);
    c.textAlign = 'right'; c.fillText('90°', ix - 4, iy + 8); c.fillText('−90°', ix - 4, iy + ih);
  }

  const v3 = new THREE.Vector3(); let tick = 0; let camDist = 22;
  engine.setUpdate((dt) => {
    if (!paused && !dragging) {
      acc += dt;
      while (acc >= H) {
        const prev = y[0]; rk(y, simT, H); simT += H; acc -= H;
        if (prev < 0 && y[0] >= 0) { const tc = simT - H * (y[0] / (y[0] - prev)); if (lastCross >= 0) { measuredT = tc - lastCross; crossings++; } lastCross = tc; }
      }
      if ((tick & 1) === 0) { trace.push([simT, y[0] / DEG]); if (trace.length > 1500) trace.shift(); }
    }
    tick++;
    const r = L * U;
    const bx = Math.sin(y[0]) * r; const by = PIVOT - Math.cos(y[0]) * r;
    const bobR = 0.35 + Math.cbrt(mass) * 0.55;
    bob.scale.setScalar(bobR); bob.position.set(bx, by, 0);
    hook.position.set(bx * (1 - (bobR + 0.1) / r), PIVOT - Math.cos(y[0]) * (r - bobR - 0.1), 0);
    string.position.set(bx / 2 * (r - bobR) / r, PIVOT - Math.cos(y[0]) * (r - bobR) / 2, 0);
    string.scale.y = r - bobR; string.rotation.z = y[0];
    ghosts.forEach((m, i) => { const s = i ? 1 : -1; m.visible = amp0 > 2 * DEG && !dragging; m.scale.setScalar(bobR); m.position.set(Math.sin(s * amp0) * r, PIVOT - Math.cos(s * amp0) * r, 0); });
    trailPts.push(bx, by, 0); if (trailPts.length > trailN * 3) trailPts.splice(0, 3);
    const n = trailPts.length / 3;
    for (let i = 0; i < n; i++) { trailPos[i * 3] = trailPts[i * 3]; trailPos[i * 3 + 1] = trailPts[i * 3 + 1]; trailPos[i * 3 + 2] = trailPts[i * 3 + 2]; trailA[i] = i / n; }
    trailGeo.setDrawRange(0, n); trailGeo.attributes.position.needsUpdate = true; trailGeo.attributes.a.needsUpdate = true;
    // keep the whole swing in view as the length changes
    const want = Math.max(16, r * 1.9 + 8);
    camDist += (want - camDist) * (1 - Math.exp(-dt * 2));
    controls.setTarget(v3.set(0, 0.8 * U / 10 * 0 + 0.8 + PIVOT - r * 0.55, 0));
    if (!dragging && Math.abs(want - camDist) > 0.2) controls.setDistance(camDist);
    controls.update(dt);
    angleLbl.el.textContent = `${fmt(y[0] / DEG, 0)}°`; angleLbl.at(v3.set(Math.sin(y[0] / 2) * 3.2, 0.8 + PIVOT - Math.cos(y[0] / 2) * 3.2, 0.2));
    lenLbl.el.textContent = `L = ${L.toFixed(2)} m`; lenLbl.at(v3.set(bx + 1.4, 0.8 + by, 0.2));
    if ((tick & 3) === 0) drawGraph();
    const T0 = 2 * Math.PI * Math.sqrt(L / g); const Tex = T0 / agm(1, Math.cos(amp0 / 2));
    st.meas.set(measuredT ? `${fmt(measuredT, 3)} s` : '…'); st.small.set(`${fmt(T0, 3)} s`); st.exact.set(`${fmt(Tex, 3)} s`); st.swings.set(String(crossings));
    badge.set(dragging ? `${fmt(Math.abs(y[0]) / DEG, 0)}°, L = ${L.toFixed(2)} m: let go to swing` : amp0 > 30 * DEG ? `A ${fmt(amp0 / DEG, 0)}° swing takes ${fmt((Tex / T0 - 1) * 100, 1)} % longer than 2π√(L/g)` : `Period ${fmt(T0, 2)} s: try a longer string, or a lab on the Moon`);
  });
  engine.start();

  stage.__pendulum = { set: (deg, len) => { L = len; lenS.set(len); restart(deg * DEG); }, state: () => ({ theta: y[0] / DEG, measuredT, L }) };
  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown, true); engine.canvas.removeEventListener('pointermove', onMove); engine.canvas.removeEventListener('pointerup', onUp);
      panel.dispose(); hud.dispose(); angleLbl.remove(); lenLbl.remove(); S.dispose();
    },
  };
}
