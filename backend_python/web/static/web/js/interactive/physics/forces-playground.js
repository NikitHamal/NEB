/**
 * Pushes and pulls in 3D. A box, a crate or a fridge on a long strip of ice, wood, carpet or grass:
 * grab it and pull like a rope (the pull grows with the stretch), or hold the push buttons. Newton's
 * second law with static and sliding friction (μs > μk): a box at rest only moves once the push beats
 * μs·m·g, and friction always opposes the motion. Applied force, friction, net force and velocity are
 * drawn as arrows to scale above the load, with a free-body card and a speed trace in the panel.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { canvasCard, makeArrow } from '../space/space3d/kit.js';
import { createField, label, THREE } from './physics3d/field.js';

const SURFACES = [
  { value: 'ice', label: 'Ice', ms: 0.05, mk: 0.03, color: 0xdff3ff, rough: 0.05 },
  { value: 'wood', label: 'Wood', ms: 0.4, mk: 0.3, color: 0xc9995f, rough: 0.55 },
  { value: 'carpet', label: 'Carpet', ms: 0.7, mk: 0.55, color: 0x8c6ca8, rough: 1 },
  { value: 'grass', label: 'Grass', ms: 0.9, mk: 0.7, color: 0x6a9c4d, rough: 1 },
];
const LOADS = [
  { value: '10', label: 'Small box · 10 kg', m: 10, size: [0.5, 0.4, 0.4], color: 0xc89a5a },
  { value: '40', label: 'Crate · 40 kg', m: 40, size: [0.8, 0.8, 0.8], color: 0xa0703c },
  { value: '100', label: 'Fridge · 100 kg', m: 100, size: [0.75, 1.8, 0.7], color: 0xeef2f6 },
];
const G = 9.81; const LEN = 30; const AS = 1 / 250;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function loadMesh(l) {
  const g = new THREE.Group();
  const [w, h, d] = l.size;
  const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ color: l.color, roughness: l.value === '100' ? 0.3 : 0.8, metalness: l.value === '100' ? 0.1 : 0 }));
  body.position.y = h / 2; body.castShadow = true; g.add(body);
  if (l.value === '10') { const tape = new THREE.Mesh(new THREE.BoxGeometry(w + 0.002, 0.06, d * 0.3), new THREE.MeshStandardMaterial({ color: 0x8b5a2b, roughness: 0.4 })); tape.position.y = h; g.add(tape); }
  if (l.value === '40') for (let i = -1; i <= 1; i += 2) { const slat = new THREE.Mesh(new THREE.BoxGeometry(w + 0.01, 0.08, d + 0.01), new THREE.MeshStandardMaterial({ color: 0x7a5228, roughness: 0.8 })); slat.position.y = h / 2 + i * h * 0.3; g.add(slat); }
  if (l.value === '100') { const handle = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.5, 0.04), new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.9, roughness: 0.3 })); handle.position.set(w / 2 - 0.08, h * 0.62, d / 2 + 0.03); g.add(handle); const seam = new THREE.Mesh(new THREE.BoxGeometry(w + 0.002, 0.01, d + 0.002), new THREE.MeshStandardMaterial({ color: 0x9aa3ad })); seam.position.y = h * 0.66; g.add(seam); }
  return g;
}

export default function init(stage) {
  const F = createField(stage, { camera: [1.5, 2.2, 6.2], target: [1, 0.7, 0], maxDistance: 40 });
  if (!F) return null;
  const { engine, scene, camera, controls } = F;
  { const c = F.key.shadow.camera; c.left = -20; c.right = 20; c.top = 20; c.bottom = -20; c.updateProjectionMatrix(); }
  const hud = createHud(stage);
  const badge = hud.badge('Grab the load and pull, or hold a push button', '#2563eb');

  let surf = SURFACES[1]; let load = LOADS[1]; let frictionOn = true; let pushSet = 200;
  let x = 0; let v = 0; let Fapp = 0; let Ff = 0; let held = false; let btnDir = 0; let simT = 0; let pull = 0;
  const trace = [];
  const stripMat = new THREE.MeshStandardMaterial({ color: surf.color, roughness: surf.rough });
  const strip = new THREE.Mesh(new THREE.BoxGeometry(LEN, 0.04, 2.4), stripMat); strip.position.set(LEN / 2 - 4, 0.02, 0); strip.receiveShadow = true; scene.add(strip);
  for (let m = 0; m <= LEN - 6; m += 1) { const t = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.002, m % 5 === 0 ? 0.5 : 0.2), new THREE.MeshBasicMaterial({ color: 0xffffff })); t.position.set(m, 0.042, 1.05); scene.add(t); }
  let mesh = loadMesh(load); scene.add(mesh);
  const rope = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1, 8), new THREE.MeshStandardMaterial({ color: 0xf5e9c8, roughness: 0.9 })); scene.add(rope);
  const handle = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.018, 8, 20), new THREE.MeshStandardMaterial({ color: 0x1f2937 })); scene.add(handle);
  const arrows = { F: makeArrow(0x2563eb, 0.02), f: makeArrow(0xdc2626, 0.02), net: makeArrow(0x16a34a, 0.02), v: makeArrow(0xf59e0b, 0.02) };
  Object.values(arrows).forEach((a) => scene.add(a.group));
  const L = { F: label(stage, camera), f: label(stage, camera), net: label(stage, camera), v: label(stage, camera) };
  L.F.el.style.color = '#93c5fd'; L.f.el.style.color = '#fca5a5'; L.net.el.style.color = '#86efac'; L.v.el.style.color = '#fcd34d';

  const panel = createPanel(stage, { title: 'Pushes and pulls' });
  panel.chips({ label: 'Surface', options: SURFACES.map((s) => ({ value: s.value, label: s.label })), value: surf.value, onChange: (val) => { surf = SURFACES.find((s) => s.value === val); stripMat.color.setHex(surf.color); stripMat.roughness = surf.rough; } });
  panel.chips({ label: 'What to push', options: LOADS.map((l) => ({ value: l.value, label: l.label })), value: load.value, onChange: (val) => { load = LOADS.find((l) => l.value === val); scene.remove(mesh); mesh = loadMesh(load); scene.add(mesh); } });
  panel.slider({ label: 'Button push strength', min: 20, max: 600, step: 10, value: pushSet, format: (val) => `${val} N`, onChange: (val) => { pushSet = val; } });
  const row = document.createElement('div'); row.style.cssText = 'display:grid;grid-template-columns:1fr 1fr;gap:8px;flex-shrink:0';
  const mk = (txt, d) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'md-btn md-btn-filled'; b.textContent = txt; b.style.cssText = 'padding:10px;border-radius:12px;touch-action:none'; const on = (e) => { e.preventDefault(); btnDir = d; }; const off = () => { btnDir = 0; }; b.addEventListener('pointerdown', on); b.addEventListener('pointerup', off); b.addEventListener('pointerleave', off); b.addEventListener('pointercancel', off); return b; };
  row.append(mk('◀ Hold to push', -1), mk('Hold to push ▶', 1)); panel.body.appendChild(row);
  panel.toggle({ label: 'Friction', value: true, onChange: (val) => { frictionOn = val; } });
  panel.button({ label: 'Back to start', icon: 'replay', variant: 'ghost', onClick: () => { x = 0; v = 0; simT = 0; trace.length = 0; } });
  const fbd = canvasCard(panel.body, 1.9);
  const st = panel.stats([{ key: 'F', label: 'Your push' }, { key: 'f', label: 'Friction' }, { key: 'a', label: 'Acceleration' }, { key: 'v', label: 'Speed' }]);
  panel.info('A load at rest stays put until your push beats the grip of the surface (μs·m·g). Once it slides, friction is a little smaller. With friction off, one shove keeps it gliding forever.');

  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -0.5); const hit = new THREE.Vector3();
  function pointer(e) { const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); return ray.ray.intersectPlane(plane, hit); }
  engine.canvas.addEventListener('pointerdown', (e) => {
    ray.setFromCamera(ndc.set(((e.clientX - engine.canvas.getBoundingClientRect().left) / engine.canvas.clientWidth) * 2 - 1, -((e.clientY - engine.canvas.getBoundingClientRect().top) / engine.canvas.clientHeight) * 2 + 1), camera);
    if (ray.intersectObject(mesh, true).length || ray.intersectObject(handle).length) { held = true; controls.enabled = false; e.stopImmediatePropagation(); if (pointer(e)) pull = hit.x; }
  }, true);
  engine.canvas.addEventListener('pointermove', (e) => { if (held && pointer(e)) pull = hit.x; });
  const up = () => { if (held) { held = false; controls.enabled = true; } };
  engine.canvas.addEventListener('pointerup', up); engine.canvas.addEventListener('pointercancel', up);

  function drawFBD() {
    const { g, w, h } = fbd.ctx();
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('Free-body diagram', 10, 14);
    const cx = w * 0.3; const cy = h * 0.56; const s = 36;
    g.fillStyle = '#334155'; g.fillRect(cx - s / 2, cy - s / 2, s, s);
    const N = load.m * G; const k = (h * 0.32) / Math.max(N, 1);
    const ar = (dx, dy, col, txt) => { if (Math.abs(dx) + Math.abs(dy) < 2) return; g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 3; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + dx, cy + dy); g.stroke(); const a = Math.atan2(dy, dx); g.beginPath(); g.moveTo(cx + dx, cy + dy); g.lineTo(cx + dx - 9 * Math.cos(a - 0.4), cy + dy - 9 * Math.sin(a - 0.4)); g.lineTo(cx + dx - 9 * Math.cos(a + 0.4), cy + dy - 9 * Math.sin(a + 0.4)); g.fill(); g.font = '600 10px Poppins, system-ui, sans-serif'; g.fillText(txt, cx + dx + (dx >= 0 ? 6 : -6 - g.measureText(txt).width), cy + dy + (dy > 0 ? 12 : -4)); };
    ar(0, -N * k, '#94a3b8', `N ${fmt(N, 0)} N`); ar(0, N * k, '#94a3b8', `W ${fmt(N, 0)} N`);
    ar(Fapp * k, 0, '#60a5fa', `F ${fmt(Math.abs(Fapp), 0)} N`); ar(Ff * k, 4, '#f87171', `friction ${fmt(Math.abs(Ff), 0)} N`);
    const net = Fapp + Ff; g.fillStyle = '#86efac'; g.font = '700 11px Poppins, system-ui, sans-serif'; g.textAlign = 'left';
    g.fillText(`net ${fmt(net, 0)} N`, w * 0.6, h * 0.28); g.fillText(`a = ${fmt(net / load.m, 2)} m/s²`, w * 0.6, h * 0.28 + 15);
    g.fillStyle = '#8ea0c2'; g.font = '600 10px Poppins, system-ui, sans-serif'; g.fillText(`μs ${surf.ms} · μk ${surf.mk}`, w * 0.6, h * 0.28 + 32);
    g.fillText(`grip ${fmt(surf.ms * load.m * G, 0)} N`, w * 0.6, h * 0.28 + 47);
  }

  const v3 = new THREE.Vector3(); const d3 = new THREE.Vector3(); let tick = 0;
  engine.setUpdate((dt) => {
    const [w, hh] = load.size;
    const front = x + w / 2;
    const back = x - w / 2;
    Fapp = !held ? btnDir * pushSet : Math.max(-900, Math.min(900, pull > front ? (pull - front) * 220 : pull < back ? (pull - back) * 220 : 0));
    const N = load.m * G;
    if (Math.abs(v) < 1e-3) {
      const grip = frictionOn ? surf.ms * N : 0;
      if (Math.abs(Fapp) <= grip) { Ff = -Fapp; v = 0; } else Ff = -Math.sign(Fapp) * (frictionOn ? surf.mk * N : 0);
    } else Ff = -Math.sign(v) * (frictionOn ? surf.mk * N : 0);
    const a = (Fapp + Ff) / load.m;
    const vOld = v; v += a * dt;
    if (vOld !== 0 && Math.sign(v) !== Math.sign(vOld) && Math.abs(Fapp) <= (frictionOn ? surf.ms * N : 0)) v = 0;
    x = Math.max(0, Math.min(LEN - 6 - w, x + v * dt));
    if (x === 0 || x === LEN - 6 - w) v = 0;
    simT += dt; if ((tick & 1) === 0) { trace.push([simT, Math.abs(v)]); if (trace.length > 500) trace.shift(); }
    mesh.position.set(x, 0.04, 0);
    const top = 0.04 + hh + 0.35;
    arrows.F.set(v3.set(x, top + 0.3, 0), d3.set(Fapp * AS, 0, 0)); arrows.f.set(v3.set(x, top, 0), d3.set(Ff * AS, 0, 0));
    arrows.net.set(v3.set(x, top + 0.6, 0), d3.set((Fapp + Ff) * AS, 0, 0)); arrows.v.set(v3.set(x, top + 0.9, 0), d3.set(v * 0.4, 0, 0));
    L.F.el.textContent = `push ${fmt(Math.abs(Fapp), 0)} N`; L.F.at(v3.set(x + Fapp * AS + Math.sign(Fapp || 1) * 0.5, top + 0.3, 0));
    L.f.el.textContent = `friction ${fmt(Math.abs(Ff), 0)} N`; L.f.at(v3.set(x + Ff * AS - Math.sign(Fapp || 1) * 0.6, top, 0));
    L.net.el.textContent = `net ${fmt(Fapp + Ff, 0)} N`; L.net.at(v3.set(x + (Fapp + Ff) * AS + 0.5, top + 0.6, 0));
    L.v.el.textContent = `${fmt(v, 2)} m/s`; L.v.at(v3.set(x + v * 0.4 + 0.45, top + 0.9, 0));
    [L.F, L.f, L.net].forEach((l, i) => { if (Math.abs([Fapp, Ff, Fapp + Ff][i]) < 1) l.el.style.opacity = '0'; });
    if (Math.abs(v) < 0.005) L.v.el.style.opacity = '0';
    rope.visible = handle.visible = held;
    if (held) {
      const ax = Fapp >= 0 ? x + w / 2 : x - w / 2; const p0 = v3.set(ax, 0.5, 0); const p1 = new THREE.Vector3(pull, 0.5, 0);
      const len = p0.distanceTo(p1); rope.scale.y = Math.max(0.01, len); rope.position.copy(p0).lerp(p1, 0.5); rope.rotation.set(0, 0, Math.PI / 2);
      handle.position.copy(p1);
    }
    controls.setTarget(v3.set(x + 1, 0.7, 0));
    controls.update(dt);
    if ((tick++ & 3) === 0) drawFBD();
    st.F.set(`${fmt(Math.abs(Fapp), 0)} N`); st.f.set(`${fmt(Math.abs(Ff), 0)} N`); st.a.set(`${fmt(a, 2)} m/s²`); st.v.set(`${fmt(v, 2)} m/s`);
    const grip = surf.ms * N;
    badge.set(Math.abs(v) < 1e-3 && Math.abs(Fapp) > 0 && Math.abs(Fapp) <= grip && frictionOn ? `Not enough: static friction matches your ${fmt(Math.abs(Fapp), 0)} N (it can grip up to ${fmt(grip, 0)} N)` : Math.abs(v) > 0.01 && Fapp === 0 && !frictionOn ? 'No friction: it glides on with no force at all (Newton’s first law)' : Math.abs(v) > 0.01 ? `Sliding: friction ${fmt(Math.abs(Ff), 0)} N is less than the grip was` : 'Grab the load and pull, or hold a push button');
  });
  engine.start();

  stage.__forces = { push: (d) => { btnDir = d; }, state: () => ({ x, v, Fapp, Ff }) };
  return { dispose() { panel.dispose(); hud.dispose(); Object.values(L).forEach((l) => l.remove()); Object.values(arrows).forEach((a) => a.dispose()); controls.dispose(); engine.dispose(); } };
}
