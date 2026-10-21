/**
 * Magnet magic in 3D, on the physics bench. Two bar magnets modelled as pairs of magnetic poles
 * (inverse-square, Gilbert's model), so the field, the forces and the turning effects all come from
 * one formula. Drag a magnet by its middle to carry it or by an end to turn it; let go and it is pulled
 * or pushed by the other. Iron paperclips are induced magnets pulled up the gradient of B², so the
 * pull grows sharply near the poles; they swing to line up with the field and cling to the ends.
 * A copper coin, a pencil and an eraser ignore the magnets. Iron filings lie along the field.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const NCLIP = 10; const LINE_STEPS = 200; const MAXLINES = 32; const S = 0.01; const W = 900; const H = 520; const Q = 9000;
const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function poleTexture(letter, color) {
  const c = document.createElement('canvas'); c.width = 128; c.height = 128; const g = c.getContext('2d');
  g.fillStyle = color; g.fillRect(0, 0, 128, 128); g.fillStyle = '#ffffff'; g.font = '800 84px Poppins, system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(letter, 64, 70);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Magnet magic', aim: 'Poles, forces and magnetic fields', subject: 'physics', target: [0, 0, 0], camera: [0, 6.2, 4.4], minDistance: 3, maxDistance: 14 });
  if (!L) return null;
  const { engine, world, camera, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Drag a magnet towards the other one', '#2563eb');

  let showLines = true; let showFilings = true;
  const mags = [{ x: 270, y: 234, a: 0, vx: 0, vy: 0, w: 0, len: 130, th: 36, held: false }, { x: 612, y: 286, a: 0, vx: 0, vy: 0, w: 0, len: 130, th: 36, held: false }];
  const cx = new Float64Array(NCLIP); const cy = new Float64Array(NCLIP); const cvx = new Float64Array(NCLIP); const cvy = new Float64Array(NCLIP); const crot = new Float64Array(NCLIP); const stuck = new Uint8Array(NCLIP);
  const others = [{ kind: 'coin', x: 135, y: 416 }, { kind: 'pencil', x: 450, y: 447 }, { kind: 'eraser', x: 774, y: 114 }];
  const B = { x: 0, y: 0 };
  const P0 = new Float64Array(4); const P1 = new Float64Array(4);
  const toW = (x, y, h = 0) => new THREE.Vector3((x - W / 2) * S, h, (y - H / 2) * S);

  // a felt mat marks the table area
  const mat = new THREE.Mesh(new THREE.BoxGeometry(W * S, 0.02, H * S), new THREE.MeshStandardMaterial({ color: 0x2f4a3a, roughness: 1 })); mat.position.y = 0.01; mat.receiveShadow = true; world.add(mat);
  const red = poleTexture('N', '#d62828'); const blue = poleTexture('S', '#1d4ed8');
  const magMeshes = mags.map((m) => {
    const g = new THREE.Group();
    const half = (tex, color, sx) => { const mtl = [new THREE.MeshStandardMaterial({ color, roughness: 0.35, metalness: 0.2 }), new THREE.MeshStandardMaterial({ color, roughness: 0.35, metalness: 0.2 }), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.35 }), new THREE.MeshStandardMaterial({ color, roughness: 0.35 }), new THREE.MeshStandardMaterial({ color, roughness: 0.35 }), new THREE.MeshStandardMaterial({ color, roughness: 0.35 })]; const b = new THREE.Mesh(new THREE.BoxGeometry(m.len * S / 2, 0.24, m.th * S), mtl); b.position.set(sx * m.len * S / 4, 0.12, 0); b.castShadow = true; g.add(b); };
    half(red, 0xd62828, 1); half(blue, 0x1d4ed8, -1);
    world.add(g); return g;
  });
  const clipGeo = (() => { const pts = []; const shape = [[0, -0.06], [0.018, -0.06], [0.018, 0.05], [-0.012, 0.05], [-0.012, -0.04], [0.008, -0.04], [0.008, 0.03]]; shape.forEach(([x, z]) => pts.push(new THREE.Vector3(x, 0, z))); return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.2), 60, 0.004, 6, false); })();
  const clipMat = new THREE.MeshStandardMaterial({ color: 0xc8ced6, metalness: 0.95, roughness: 0.25 });
  const clips = Array.from({ length: NCLIP }, () => { const m = new THREE.Mesh(clipGeo, clipMat); m.scale.setScalar(2.4); m.castShadow = true; world.add(m); return m; });
  const otherMeshes = others.map((o) => {
    let m;
    if (o.kind === 'coin') m = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.02, 32), new THREE.MeshStandardMaterial({ color: 0xb87333, metalness: 0.9, roughness: 0.3 }));
    else if (o.kind === 'pencil') { m = new THREE.Group(); const b = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.9, 6), new THREE.MeshStandardMaterial({ color: 0xf2c230, roughness: 0.6 })); b.rotation.z = Math.PI / 2; const tip = new THREE.Mesh(new THREE.ConeGeometry(0.035, 0.12, 6), new THREE.MeshStandardMaterial({ color: 0xe8c39e })); tip.rotation.z = -Math.PI / 2; tip.position.x = 0.51; m.add(b, tip); }
    else m = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.1, 0.14), new THREE.MeshStandardMaterial({ color: 0xf29bb5, roughness: 0.9 }));
    m.position.copy(toW(o.x, o.y, 0.05)); m.castShadow = true; world.add(m); return m;
  });
  // field lines and iron filings
  const lineGeo = new THREE.BufferGeometry(); const linePos = new Float32Array(MAXLINES * LINE_STEPS * 2 * 3); lineGeo.setAttribute('position', new THREE.BufferAttribute(linePos, 3));
  const lines = new THREE.LineSegments(lineGeo, new THREE.LineBasicMaterial({ color: 0x9ae6ff, transparent: true, opacity: 0.75 })); lines.frustumCulled = false; world.add(lines);
  const FS = 24; const FC = Math.ceil(W / FS); const FR = Math.ceil(H / FS);
  const filings = new THREE.InstancedMesh(new THREE.BoxGeometry(0.11, 0.008, 0.012), new THREE.MeshStandardMaterial({ color: 0x3a3f46, metalness: 0.6, roughness: 0.5 }), FC * FR); world.add(filings);

  const panel = createPanel(stage, { title: 'Magnets' });
  panel.buttonRow([{ label: 'Flip left', icon: 'swap_horiz', variant: 'ghost', onClick: () => { mags[0].a += Math.PI; dirty = true; } }, { label: 'Flip right', icon: 'swap_horiz', variant: 'ghost', onClick: () => { mags[1].a += Math.PI; dirty = true; } }]);
  panel.toggle({ label: 'Field lines', value: true, onChange: (v) => { showLines = v; } });
  panel.toggle({ label: 'Iron filings', value: true, onChange: (v) => { showFilings = v; } });
  panel.button({ label: 'Scatter the objects', icon: 'shuffle', variant: 'ghost', onClick: scatter });
  const st = panel.stats([{ key: 'gap', label: 'Gap' }, { key: 'force', label: 'Force' }, { key: 'rule', label: 'Facing poles' }, { key: 'clips', label: 'Clips held' }]);
  panel.info('Opposite poles (N and S) attract, like poles repel. The pull fades fast with distance, so bring the magnet close. Only iron feels it: the copper coin, the pencil and the eraser stay put.');

  function poles(m, out) { const c = Math.cos(m.a); const s = Math.sin(m.a); const h = m.len / 2 - 10; out[0] = m.x + c * h; out[1] = m.y + s * h; out[2] = m.x - c * h; out[3] = m.y - s * h; }
  function field(x, y, skip, out) {
    let bx = 0; let by = 0;
    for (let i = 0; i < 2; i++) { if (i === skip) continue; const P = i === 0 ? P0 : P1; for (let j = 0; j < 2; j++) { const q = j === 0 ? Q : -Q; const dx = x - P[j * 2]; const dy = y - P[j * 2 + 1]; const r2 = dx * dx + dy * dy + 120; const inv = q / (r2 * Math.sqrt(r2)); bx += dx * inv; by += dy * inv; } }
    out.x = bx; out.y = by; return out;
  }
  function scatter() {
    for (let i = 0; i < NCLIP; i++) {
      let tries = 0;
      do { cx[i] = 30 + Math.random() * (W - 60); cy[i] = 40 + Math.random() * (H - 80); tries++; } while (tries < 30 && mags.some((m) => Math.hypot(cx[i] - m.x, cy[i] - m.y) < m.len / 2 + 150));
      cvx[i] = 0; cvy[i] = 0; crot[i] = Math.random() * Math.PI; stuck[i] = 0;
    }
  }
  scatter();
  const tmp = { x: 0, y: 0 }; const tmp2 = { x: 0, y: 0 };
  function segClosest(m, px, py, out) { const c = Math.cos(m.a); const s = Math.sin(m.a); const h = m.len / 2 - m.th / 2; const t = clamp((px - m.x) * c + (py - m.y) * s, -h, h); out.x = m.x + c * t; out.y = m.y + s * t; return out; }

  // drag a magnet: the middle carries it, an end turns it
  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -0.8); const hit = new THREE.Vector3();
  let drag = null;
  const tableAt = (e) => { const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); if (!ray.ray.intersectPlane(plane, hit)) return null; const p = world.worldToLocal(hit.clone()); return { x: p.x / S + W / 2, y: p.z / S + H / 2 }; };
  engine.canvas.addEventListener('pointerdown', (e) => {
    const p = tableAt(e); if (!p) return;
    for (let i = 0; i < 2; i++) {
      const m = mags[i]; const c = Math.cos(m.a); const s = Math.sin(m.a); const u = (p.x - m.x) * c + (p.y - m.y) * s; const v = -(p.x - m.x) * s + (p.y - m.y) * c;
      if (Math.abs(u) < m.len / 2 + 10 && Math.abs(v) < m.th / 2 + 14) { drag = { i, turn: Math.abs(u) > m.len * 0.32, dx: m.x - p.x, dy: m.y - p.y }; m.held = true; m.vx = m.vy = m.w = 0; controls.enabled = false; e.stopImmediatePropagation(); return; }
    }
  }, true);
  engine.canvas.addEventListener('pointermove', (e) => {
    if (!drag) return; const p = tableAt(e); if (!p) return; const m = mags[drag.i];
    if (drag.turn) { const a = Math.atan2(p.y - m.y, p.x - m.x); const c0 = Math.cos(m.a) * (p.x - m.x) + Math.sin(m.a) * (p.y - m.y); m.a = c0 >= 0 ? a : a + Math.PI; }
    else { m.x = clamp(p.x + drag.dx, 40, W - 40); m.y = clamp(p.y + drag.dy, 40, H - 40); }
    dirty = true;
  });
  const up = () => { if (drag) { mags[drag.i].held = false; drag = null; controls.enabled = true; } };
  engine.canvas.addEventListener('pointerup', up); engine.canvas.addEventListener('pointercancel', up);

  let dirty = true; let lastF = 0;
  function stepMagnets(dt) {
    poles(mags[0], P0); poles(mags[1], P1);
    lastF = 0;
    for (let i = 0; i < 2; i++) {
      const m = mags[i]; if (m.held) continue;
      const P = i === 0 ? P0 : P1; let fx = 0; let fy = 0; let tq = 0;
      for (let j = 0; j < 2; j++) { field(P[j * 2], P[j * 2 + 1], i, B); const q = j === 0 ? Q : -Q; const Fx = q * B.x * 0.02; const Fy = q * B.y * 0.02; fx += Fx; fy += Fy; tq += (P[j * 2] - m.x) * Fy - (P[j * 2 + 1] - m.y) * Fx; }
      lastF = Math.max(lastF, Math.hypot(fx, fy));
      const I = m.len * m.len / 12; const fric = 40; const fmag = Math.hypot(fx, fy);
      if (fmag > fric || Math.hypot(m.vx, m.vy) > 1) { m.vx += fx * dt; m.vy += fy * dt; const sp = Math.hypot(m.vx, m.vy); const dec = Math.min(sp, fric * dt * 2.5); if (sp > 0) { m.vx -= m.vx / sp * dec; m.vy -= m.vy / sp * dec; } }
      if (Math.abs(tq) > fric * 20 || Math.abs(m.w) > 0.02) { m.w += tq / I * dt; m.w *= Math.exp(-dt * 6); }
      m.x += m.vx * dt; m.y += m.vy * dt; m.a += m.w * dt; m.x = clamp(m.x, 40, W - 40); m.y = clamp(m.y, 40, H - 40);
      if (Math.abs(m.vx) + Math.abs(m.vy) + Math.abs(m.w) > 0.01) dirty = true;
    }
    const a = mags[0]; const b = mags[1];
    for (let it = 0; it < 3; it++) {
      segClosest(a, b.x, b.y, tmp); segClosest(b, tmp.x, tmp.y, tmp2); segClosest(a, tmp2.x, tmp2.y, tmp);
      const dx = tmp2.x - tmp.x; const dy = tmp2.y - tmp.y; const d = Math.hypot(dx, dy) || 1e-6; const minD = (a.th + b.th) / 2;
      if (d < minD) { const push = minD - d; const nx = dx / d; const ny = dy / d; const wa = a.held ? 0 : b.held ? 1 : 0.5; const wb = 1 - wa; a.x -= nx * push * wa; a.y -= ny * push * wa; b.x += nx * push * wb; b.y += ny * push * wb; const rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny; if (rv < 0) { a.vx += nx * rv * wa; a.vy += ny * rv * wa; b.vx -= nx * rv * wb; b.vy -= ny * rv * wb; } dirty = true; }
    }
  }
  function stepClips(dt) {
    for (let i = 0; i < NCLIP; i++) {
      const e = 2;
      field(cx[i] + e, cy[i], -1, B); const b1 = B.x * B.x + B.y * B.y; field(cx[i] - e, cy[i], -1, B); const b2 = B.x * B.x + B.y * B.y;
      field(cx[i], cy[i] + e, -1, B); const b3 = B.x * B.x + B.y * B.y; field(cx[i], cy[i] - e, -1, B); const b4 = B.x * B.x + B.y * B.y; field(cx[i], cy[i], -1, B);
      let fx = 6e4 * (b1 - b2) / (2 * e); let fy = 6e4 * (b3 - b4) / (2 * e); const fm = Math.hypot(fx, fy);
      if (fm < 25 && Math.hypot(cvx[i], cvy[i]) < 2) { cvx[i] = 0; cvy[i] = 0; stuck[i] = 0; continue; }
      if (fm > 4000) { fx *= 4000 / fm; fy *= 4000 / fm; }
      cvx[i] += fx * dt; cvy[i] += fy * dt; const damp = Math.exp(-dt * 7); cvx[i] *= damp; cvy[i] *= damp; cx[i] += cvx[i] * dt; cy[i] += cvy[i] * dt;
      const ta = Math.atan2(B.y, B.x); let da = ta - crot[i]; da = Math.atan2(Math.sin(2 * da), Math.cos(2 * da)) / 2; crot[i] += da * Math.min(1, dt * 8);
      stuck[i] = 0;
      for (const m of mags) { segClosest(m, cx[i], cy[i], tmp); const dx = cx[i] - tmp.x; const dy = cy[i] - tmp.y; const d = Math.hypot(dx, dy) || 1e-6; const minD = m.th / 2 + 5; if (d < minD) { cx[i] = tmp.x + dx / d * minD; cy[i] = tmp.y + dy / d * minD; const vn = cvx[i] * dx / d + cvy[i] * dy / d; if (vn < 0) { cvx[i] -= vn * dx / d; cvy[i] -= vn * dy / d; } cvx[i] *= 0.6; cvy[i] *= 0.6; stuck[i] = 1; } }
      for (let j = 0; j < i; j++) { const dx = cx[i] - cx[j]; const dy = cy[i] - cy[j]; const d = Math.hypot(dx, dy) || 1e-6; if (d < 12) { const p = (12 - d) / 2; cx[i] += dx / d * p; cy[i] += dy / d * p; cx[j] -= dx / d * p; cy[j] -= dy / d * p; } }
      cx[i] = clamp(cx[i], 10, W - 10); cy[i] = clamp(cy[i], 10, H - 10);
    }
  }
  function traceLines() {
    let n = 0; let o = 0;
    for (let mi = 0; mi < 2 && n < MAXLINES; mi++) {
      const P = mi === 0 ? P0 : P1;
      for (let k = 0; k < 16 && n < MAXLINES; k++) {
        const an = k / 16 * Math.PI * 2; let x = P[0] + Math.cos(an) * 8; let y = P[1] + Math.sin(an) * 8;
        let px = x; let py = y;
        for (let s = 0; s < LINE_STEPS; s++) {
          field(x, y, -1, B); const bm = Math.hypot(B.x, B.y) || 1e-9;
          x += B.x / bm * 7; y += B.y / bm * 7;
          if (x < 0 || x > W || y < 0 || y > H) break;
          const v0 = toW(px, py, 0.03); const v1 = toW(x, y, 0.03);
          linePos.set([v0.x, v0.y, v0.z, v1.x, v1.y, v1.z], o); o += 6; px = x; py = y;
          if (Math.hypot(x - P0[2], y - P0[3]) < 10 || Math.hypot(x - P1[2], y - P1[3]) < 10) break;
        }
        n++;
      }
    }
    lineGeo.setDrawRange(0, o / 3); lineGeo.attributes.position.needsUpdate = true;
    const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const sc = new THREE.Vector3(); const e3 = new THREE.Euler();
    let fi = 0;
    for (let r = 0; r < FR; r++) for (let c = 0; c < FC; c++) {
      const x = (c + 0.5) * FS + ((r * 7 + c * 13) % 9 - 4); const y = (r + 0.5) * FS + ((r * 11 + c * 5) % 9 - 4);
      field(x, y, -1, B); const bm = Math.hypot(B.x, B.y); const k = clamp(Math.log10(bm * 400 + 1) * 0.7, 0, 1);
      const inside = mags.some((m) => { const cc = Math.cos(m.a); const ss = Math.sin(m.a); return Math.abs((x - m.x) * cc + (y - m.y) * ss) < m.len / 2 + 4 && Math.abs(-(x - m.x) * ss + (y - m.y) * cc) < m.th / 2 + 4; });
      e3.set(0, -Math.atan2(B.y, B.x), 0); q.setFromEuler(e3);
      m4.compose(toW(x, y, 0.025), q, sc.set(0.3 + 0.7 * k, 1, 1).multiplyScalar(inside ? 0 : 1)); filings.setMatrixAt(fi++, m4);
    }
    filings.instanceMatrix.needsUpdate = true;
  }

  const v3 = new THREE.Vector3();
  engine.setUpdate((dt) => {
    controls.update(dt);
    const h = Math.min(dt, 1 / 30);
    for (let s = 0; s < 2; s++) { stepMagnets(h / 2); stepClips(h / 2); }
    if (dirty) { traceLines(); dirty = false; }
    lines.visible = showLines; filings.visible = showFilings;
    mags.forEach((m, i) => { magMeshes[i].position.copy(toW(m.x, m.y, 0.02)); magMeshes[i].rotation.y = -m.a; magMeshes[i].position.y = m.held ? 0.08 : 0.02; });
    for (let i = 0; i < NCLIP; i++) { clips[i].position.copy(toW(cx[i], cy[i], 0.03)); clips[i].rotation.y = -crot[i] + Math.PI / 2; }
    const a = mags[0]; const b = mags[1]; segClosest(a, b.x, b.y, tmp); segClosest(b, tmp.x, tmp.y, tmp2);
    const gap = Math.max(0, Math.hypot(tmp2.x - tmp.x, tmp2.y - tmp.y) - (a.th + b.th) / 2);
    poles(a, P0); poles(b, P1);
    let best = 1e9; let pair = '';
    for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) { const d = Math.hypot(P0[i * 2] - P1[j * 2], P0[i * 2 + 1] - P1[j * 2 + 1]); if (d < best) { best = d; pair = `${i ? 'S' : 'N'}–${j ? 'S' : 'N'}`; } }
    const attract = pair === 'N–S' || pair === 'S–N';
    st.gap.set(`${fmt(gap * 0.1, 1)} cm`); st.force.set(`${fmt(lastF * 0.0015, 2)} N`); st.rule.set(`${pair} · ${attract ? 'attract' : 'repel'}`); st.clips.set(String(stuck.reduce((s, x) => s + x, 0)));
    badge.set(gap < 60 ? (attract ? 'Opposite poles: they pull together' : 'Like poles: they push apart') : 'Drag a magnet towards the other one');
    void v3;
  });
  engine.start();

  stage.__magnets = { move: (i, x, y, a) => { mags[i].x = x; mags[i].y = y; if (a !== undefined) mags[i].a = a; dirty = true; }, state: () => mags.map((m) => ({ x: m.x, y: m.y, a: m.a })) };
  return { dispose() { panel.dispose(); hud.dispose(); L.dispose(); } };
}
