/**
 * Quadratic graph (NEB class 10) in 3D — y = ax² + bx + c on a large graph board standing on the bench.
 * Drag the vertex to move the parabola, the shape handle (one unit right of the vertex) to change a,
 * the y-intercept to change c, or a root to slide the zeros: every drag rewrites a, b and c exactly.
 * The curve is a solid tube with the table of values as beads, the axis of symmetry is a pane through
 * the vertex, and a ball rolls along the curve and settles at a minimum (it rolls off a maximum). The
 * vertex (−b/2a, c − b²/4a), the discriminant and the roots are computed live.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const R = 10; const U = 0.26; const Y0 = 3.3;
const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);
function num(v) { const r = Math.round(v * 100) / 100; return Number.isInteger(r) ? String(r) : r.toFixed(2).replace(/0$/, ''); }
function poly(a, b, c) {
  let s = (a === 1 ? '' : a === -1 ? '−' : (a < 0 ? '−' : '') + num(Math.abs(a))) + 'x²';
  if (Math.abs(b) > 1e-9) s += (b < 0 ? ' − ' : ' + ') + (Math.abs(b) === 1 ? '' : num(Math.abs(b))) + 'x';
  if (Math.abs(c) > 1e-9) s += (c < 0 ? ' − ' : ' + ') + num(Math.abs(c));
  return 'y = ' + s;
}
const factor = (r) => (Math.abs(r) < 1e-9 ? 'x' : `(x ${r > 0 ? '−' : '+'} ${num(Math.abs(r))})`);

function gridTexture() {
  const N = 1024; const c = document.createElement('canvas'); c.width = N; c.height = N; const g = c.getContext('2d');
  g.fillStyle = '#fbfdf7'; g.fillRect(0, 0, N, N);
  const s = N / (2 * R + 1); const o = s / 2;
  for (let i = 0; i <= (2 * R + 1) * 5; i++) { const x = i * s / 5; g.strokeStyle = i % 5 === 0 ? 'rgba(37,99,235,0.35)' : 'rgba(37,99,235,0.12)'; g.lineWidth = i % 5 === 0 ? 2 : 1; g.beginPath(); g.moveTo(x, 0); g.lineTo(x, N); g.moveTo(0, x); g.lineTo(N, x); g.stroke(); }
  g.strokeStyle = '#0f172a'; g.lineWidth = 3; g.beginPath(); g.moveTo(N / 2, 0); g.lineTo(N / 2, N); g.moveTo(0, N / 2); g.lineTo(N, N / 2); g.stroke();
  g.fillStyle = '#334155'; g.font = '600 18px Poppins, system-ui, sans-serif'; g.textAlign = 'center';
  for (let v = -R; v <= R; v += 2) { if (!v) continue; g.fillText(String(v), N / 2 + v * s, N / 2 + 22); g.fillText(String(v), N / 2 - 16, N / 2 - v * s + 6); }
  void o;
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

export default function init(stage) {
  const S = createChemLab(stage, { title: 'Quadratic graphs', aim: 'y = ax² + bx + c', subject: 'physics', target: [0, Y0, 0], camera: [1.6, Y0 + 0.6, 9.5], minDistance: 3, maxDistance: 16 });
  if (!S) return null;
  const { engine, world, camera, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Drag the vertex, a root or the shape handle', '#2563eb');

  let a = 1; let b = -2; let c = -3; let A = a; let B = b; let C = c;
  const W = (2 * R + 1) * U;
  const board = new THREE.Mesh(new THREE.BoxGeometry(W + 0.2, W + 0.2, 0.08), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 })); board.position.set(0, Y0, -0.06); board.castShadow = true; world.add(board);
  const paper = new THREE.Mesh(new THREE.PlaneGeometry(W, W), new THREE.MeshStandardMaterial({ map: gridTexture(), roughness: 0.85 })); paper.position.set(0, Y0, -0.015); world.add(paper);
  for (const x of [-1.6, 1.6]) { const leg = new THREE.Mesh(new THREE.BoxGeometry(0.12, Y0 + 0.4, 0.12), new THREE.MeshStandardMaterial({ color: 0x6b4a2b, roughness: 0.8 })); leg.position.set(x, (Y0 - W / 2) / 2, -0.15); world.add(leg); }
  const P = (x, y, z = 0.06) => new THREE.Vector3(x * U, Y0 + y * U, z);
  const tubeMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.3, metalness: 0.2 });
  let tube = new THREE.Mesh(new THREE.BufferGeometry(), tubeMat); tube.castShadow = true; world.add(tube);
  const beads = new THREE.InstancedMesh(new THREE.SphereGeometry(0.07, 14, 10), new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4 }), 21); world.add(beads);
  const axisPane = new THREE.Mesh(new THREE.PlaneGeometry(0.02, W), new THREE.MeshBasicMaterial({ color: 0xa855f7, transparent: true, opacity: 0.7 })); world.add(axisPane);
  const mk = (color, r = 0.13) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), new THREE.MeshStandardMaterial({ color, roughness: 0.3, emissive: color, emissiveIntensity: 0.2 })); m.castShadow = true; world.add(m); return m; };
  const hV = mk(0x7c3aed, 0.16); const hS = mk(0xf97316); const hC = mk(0x0d9488); const hR = [mk(0xdc2626), mk(0xdc2626)];
  const ball = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 16), new THREE.MeshPhysicalMaterial({ color: 0xe5e7eb, metalness: 0.9, roughness: 0.15 })); ball.castShadow = true; world.add(ball);
  let bx = 2; let bv = 0;
  const lbl = { v: S.label(), eq: S.label() };
  lbl.eq.el.style.font = '700 15px Poppins,system-ui,sans-serif';

  const panel = createPanel(stage, { title: 'y = ax² + bx + c' });
  const aS = panel.slider({ label: 'a', min: -3, max: 3, step: 0.1, value: a, format: (v) => v.toFixed(1), onChange: (v) => { a = Math.abs(v) < 0.05 ? (v < 0 ? -0.1 : 0.1) : v; } });
  const bS = panel.slider({ label: 'b', min: -10, max: 10, step: 0.5, value: b, format: (v) => v.toFixed(1), onChange: (v) => { b = v; } });
  const cS = panel.slider({ label: 'c', min: -10, max: 10, step: 0.5, value: c, format: (v) => v.toFixed(1), onChange: (v) => { c = v; } });
  panel.buttonRow([{ label: 'Two roots', variant: 'ghost', onClick: () => set(1, -2, -3) }, { label: 'One root', variant: 'ghost', onClick: () => set(1, -6, 9) }, { label: 'No roots', variant: 'ghost', onClick: () => set(1, 0, 4) }]);
  panel.button({ label: 'Roll the ball again', icon: 'replay', variant: 'ghost', onClick: () => { bx = vx() + 4; bv = 0; } });
  const st = panel.stats([{ key: 'v', label: 'Vertex' }, { key: 'axis', label: 'Axis of symmetry' }, { key: 'D', label: 'D = b² − 4ac' }, { key: 'roots', label: 'Roots' }]);
  const fact = panel.readout({ label: 'Factorised', value: '—' });
  const table = document.createElement('div'); table.style.cssText = 'display:grid;grid-template-columns:repeat(8,1fr);gap:2px 6px;font:600 11px ui-monospace,Menlo,monospace;color:#cbd5e1;padding:8px 10px;border-radius:12px;background:rgba(255,255,255,0.04);flex-shrink:0;text-align:center'; panel.body.appendChild(table);
  panel.info('a > 0 opens upwards (a minimum), a < 0 downwards (a maximum); a bigger |a| is narrower. D > 0: two roots, D = 0: one repeated root (the vertex touches the x-axis), D < 0: no real roots.');

  function set(na, nb, nc) { a = na; b = nb; c = nc; sync(); }
  function sync() { aS.set(Math.round(a * 10) / 10); bS.set(Math.round(b * 2) / 2); cS.set(Math.round(c * 2) / 2); }
  const vx = () => -b / (2 * a); const vy = () => c - b * b / (4 * a);
  const snap = (v, s) => Math.round(v / s) * s;
  const roots = () => { const D = b * b - 4 * a * c; if (D < -1e-9) return null; const s2 = Math.sqrt(Math.max(0, D)); return [(-b - s2) / (2 * a), (-b + s2) / (2 * a)]; };

  // drag handles in the board's plane
  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -0.06); const hit = new THREE.Vector3();
  let drag = null;
  const at = (e) => { const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); };
  engine.canvas.addEventListener('pointerdown', (e) => {
    at(e); const hs = [['v', hV], ['s', hS], ['c', hC], ['r0', hR[0]], ['r1', hR[1]]].filter(([, m]) => m.visible);
    const h = ray.intersectObjects(hs.map(([, m]) => m))[0]; if (!h) return;
    drag = hs.find(([, m]) => m === h.object)[0]; controls.enabled = false; e.stopImmediatePropagation();
  }, true);
  engine.canvas.addEventListener('pointermove', (e) => {
    if (!drag) return; at(e); if (!ray.ray.intersectPlane(plane, hit)) return;
    const p = world.worldToLocal(hit.clone()); const x = clamp(p.x / U, -R, R); const y = clamp((p.y - Y0) / U, -R, R);
    if (drag === 'v') { const h0 = snap(x, 0.5); const k0 = snap(y, 0.5); b = -2 * a * h0; c = a * h0 * h0 + k0; }
    else if (drag === 's') { const h0 = vx(); const k0 = vy(); let na = clamp(snap(y - k0, 0.1), -3, 3); if (Math.abs(na) < 0.1) na = na < 0 ? -0.1 : 0.1; a = na; b = -2 * a * h0; c = a * h0 * h0 + k0; }
    else if (drag === 'c') c = snap(y, 0.5);
    else { const r = roots(); if (!r) return; const ri = drag === 'r0' ? 0 : 1; const other = r[1 - ri]; const nr = snap(x, 0.5); b = -a * (nr + other); c = a * nr * other; }
    sync();
  });
  const up = () => { if (drag) { drag = null; controls.enabled = true; } };
  engine.canvas.addEventListener('pointerup', up); engine.canvas.addEventListener('pointercancel', up);

  let key = '';
  engine.setUpdate((dt) => {
    controls.update(dt);
    const k = 1 - Math.exp(-dt * 12); A += (a - A) * k; B += (b - B) * k; C += (c - C) * k;
    const f = (x) => A * x * x + B * x + C;
    const kk = `${A.toFixed(4)}|${B.toFixed(4)}|${C.toFixed(4)}`;
    if (kk !== key) {
      key = kk;
      const pts = []; for (let i = 0; i <= 240; i++) { const x = -R + 2 * R * i / 240; const y = f(x); if (Math.abs(y) <= R + 0.5) pts.push(P(x, clamp(y, -R - 0.3, R + 0.3))); }
      tube.geometry.dispose(); tube.geometry = pts.length > 1 ? new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), Math.max(8, pts.length), 0.045, 8) : new THREE.BufferGeometry();
      const m4 = new THREE.Matrix4(); let n = 0;
      for (let x = -R; x <= R; x++) { const y = f(x); if (Math.abs(y) <= R) { m4.makeTranslation(x * U, Y0 + y * U, 0.06); beads.setMatrixAt(n++, m4); } }
      beads.count = n; beads.instanceMatrix.needsUpdate = true;
      const hv = -B / (2 * A); const kv = C - B * B / (4 * A);
      axisPane.position.set(hv * U, Y0, 0.02); axisPane.visible = Math.abs(hv) <= R;
      hV.position.copy(P(hv, kv, 0.12)); hS.position.copy(P(hv + 1, kv + A, 0.12)); hC.position.copy(P(0, C, 0.12));
      [hV, hS, hC].forEach((m) => { m.visible = Math.abs((m.position.x) / U) <= R && Math.abs((m.position.y - Y0) / U) <= R; });
      const r = roots(); hR.forEach((m, i) => { m.visible = !!r && Math.abs(r[i]) <= R; if (r) m.position.copy(P(r[i], 0, 0.12)); });
      if (r && Math.abs(r[0] - r[1]) < 1e-6) hR[1].visible = false;
      const D = b * b - 4 * a * c;
      st.v.set(`(${num(vx())}, ${num(vy())})`); st.axis.set(`x = ${num(vx())}`); st.D.set(num(D)); st.roots.set(!r ? 'none (D < 0)' : Math.abs(r[0] - r[1]) < 1e-6 ? `x = ${num(r[0])} (twice)` : `x = ${num(r[0])}, ${num(r[1])}`);
      fact.set(!r ? 'no real factors' : `${a === 1 ? '' : num(a)}${factor(r[0])}${factor(r[1])}`);
      table.innerHTML = [-3, -2, -1, 0, 1, 2, 3].map((x) => `<span style="color:#94a3b8">${x}</span>`).join('').replace(/^/, '<b style="color:#94a3b8">x</b>') + '<b style="color:#94a3b8">y</b>' + [-3, -2, -1, 0, 1, 2, 3].map((x) => `<span>${num(a * x * x + b * x + c)}</span>`).join('');
      lbl.eq.el.textContent = poly(Math.round(a * 10) / 10, Math.round(b * 2) / 2, Math.round(c * 2) / 2);
      badge.set(D > 0 ? `D = ${num(D)} > 0: two roots` : Math.abs(D) < 1e-9 ? 'D = 0: the vertex touches the x-axis' : `D = ${num(D)} < 0: no real roots`);
    }
    // the ball rolls along the curve under gravity: s'' = -g sin(angle)
    const slope = 2 * A * bx + B; const acc = -9.81 * 0.06 * slope / Math.sqrt(1 + slope * slope);
    bv += acc * dt * 6; bv *= Math.exp(-dt * 0.6); bx += bv * dt; if (Math.abs(bx) > R) { bx = clamp(bx, -R, R); bv = 0; }
    const by = f(bx); ball.visible = Math.abs(by) <= R; ball.position.copy(P(bx, by + 0.75, 0.12));
    lbl.v.el.textContent = `vertex (${num(vx())}, ${num(vy())})`; lbl.v.at(hV.position.clone().add(new THREE.Vector3(0, 0.8 - 0.35 * Math.sign(a), 0)));
    lbl.eq.at(new THREE.Vector3(0, 0.8 + Y0 + W / 2 + 0.35, 0));
  });
  engine.start();

  stage.__quad = { set, state: () => ({ a, b, c }) };
  return { dispose() { panel.dispose(); hud.dispose(); Object.values(lbl).forEach((l) => l.remove()); S.dispose(); } };
}
