// Electrical bench parts shared by the circuit practicals, at true size (1 unit = 10 cm): brass
// binding posts, flexible leads that sag between terminals, a centre-zero pointer galvanometer, a
// plug-type resistance box whose brass plugs come out to add resistance, a plug key, a cell, and a
// small linear solver for the circuits themselves (nodal analysis, Gaussian elimination).
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture } from '../bio-handson/kit.js';

const BRASS = () => new THREE.MeshStandardMaterial({ color: 0xd4a94a, metalness: 1, roughness: 0.28 });
let brassMat = null;
export function brass() { if (!brassMat) { brassMat = BRASS(); brassMat.userData.sharedFx = true; } return brassMat; }

export function bindingPost() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.CylinderGeometry(0.06, 0.07, 0.05, 16), brass(), [0, 0.025, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.12, 10), brass(), [0, 0.1, 0]));
  const knob = mesh(new THREE.CylinderGeometry(0.055, 0.05, 0.06, 16), MAT.gloss(0x111827), [0, 0.16, 0]); g.add(knob);
  g.userData.top = new THREE.Vector3(0, 0.09, 0);
  return g;
}

/** A flexible lead between two points (local to `parent`), sagging under its own weight. */
export function lead(parent, a, b, color = 0xd32f2f, { sag = 0.25, radius = 0.014 } = {}) {
  const mat = MAT.gloss(color);
  const m = new THREE.Mesh(new THREE.BufferGeometry(), mat); m.castShadow = true; parent.add(m);
  const pa = new THREE.Vector3(); const pb = new THREE.Vector3(); const mid = new THREE.Vector3();
  const api = {
    mesh: m,
    set(A, B) {
      pa.copy(A); pb.copy(B);
      const d = pa.distanceTo(pb);
      mid.lerpVectors(pa, pb, 0.5); mid.y = Math.min(pa.y, pb.y) - sag * Math.min(1.5, d * 0.35) + 0.02;
      const curve = new THREE.CatmullRomCurve3([pa.clone(), pa.clone().lerp(mid, 0.5).setY(pa.y + 0.08), mid.clone(), pb.clone().lerp(mid, 0.5).setY(pb.y + 0.08), pb.clone()]);
      m.geometry.dispose(); m.geometry = new THREE.TubeGeometry(curve, 28, radius, 7);
    },
  };
  api.set(a, b);
  return api;
}

function galvoDial() {
  return canvasTexture('ho-galvo-dial', 512, 320, (g, w, h) => {
    g.fillStyle = '#fbfaf4'; g.fillRect(0, 0, w, h);
    const cx = w / 2; const cy = h - 36; const R = 230;
    g.strokeStyle = '#111827'; g.fillStyle = '#111827';
    g.lineWidth = 3; g.beginPath(); g.arc(cx, cy, R - 34, Math.PI * 1.25, Math.PI * 1.75); g.stroke();
    for (let i = -30; i <= 30; i++) {
      const a = -Math.PI / 2 + i / 30 * Math.PI / 4; const big = i % 10 === 0; const mid = i % 5 === 0;
      const r0 = R - 34; const r1 = r0 + (big ? 30 : mid ? 20 : 12);
      g.lineWidth = big ? 3.5 : 2; g.beginPath(); g.moveTo(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0); g.lineTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1); g.stroke();
      if (big) { g.font = '700 26px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(String(Math.abs(i)), cx + Math.cos(a) * (R + 14), cy + Math.sin(a) * (R + 14) + 8); }
    }
    g.font = '800 46px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText('G', cx, cy - 70);
    g.font = '600 18px system-ui, sans-serif'; g.fillStyle = '#475569'; g.fillText('CENTRE ZERO · 30-0-30', cx, cy - 36);
  });
}

/** A centre-zero galvanometer; setDivisions(n) swings the needle with a damped spring. */
export function galvanometer() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.BoxGeometry(0.95, 0.42, 0.62), MAT.gloss(0x1f2933), [0, 0.21, 0]));
  const face = new THREE.Mesh(new THREE.PlaneGeometry(0.78, 0.49), new THREE.MeshStandardMaterial({ map: galvoDial(), roughness: 0.5 }));
  face.rotation.x = -Math.PI / 2 + 0.5; face.position.set(0, 0.4575, 0.0296); g.add(face);
  const frame = mesh(new THREE.BoxGeometry(0.88, 0.03, 0.6), MAT.gloss(0x111827), [0, 0.43, 0.02]); frame.rotation.x = 0.5; g.add(frame);
  const glass = mesh(new THREE.PlaneGeometry(0.8, 0.51), MAT.glass(), null, { cast: false }); glass.rotation.x = -Math.PI / 2 + 0.5; glass.position.set(0, 0.48, 0.042); g.add(glass);
  const pivot = new THREE.Group(); pivot.position.set(0, 0.3675, 0.1996); pivot.rotation.x = 0.5 - Math.PI / 2; g.add(pivot);
  const needle = new THREE.Group(); pivot.add(needle);
  needle.add(mesh(new THREE.BoxGeometry(0.006, 0.31, 0.004), MAT.ink(0x111827), [0, 0.155, 0.012]));
  needle.add(mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.012, 14), MAT.gloss(0x991b1b), [0, 0, 0.012]).rotateX(Math.PI / 2));
  const posts = [-0.3, 0.3].map((x) => { const p = bindingPost(); p.position.set(x, 0.42, -0.2); g.add(p); return p; });
  let div = 0; let vel = 0; let target = 0;
  return {
    group: g, needle, posts,
    setDivisions(n) { target = Math.max(-33, Math.min(33, n)); },
    get divisions() { return div; },
    update(dt) {
      const n = Math.max(1, Math.ceil(dt / 0.008)); const h = dt / n;
      for (let i = 0; i < n; i++) { const a = -90 * (div - target) - 2 * 0.55 * Math.sqrt(90) * vel; vel += a * h; div += vel * h; }
      needle.rotation.z = -div / 30 * Math.PI / 4;
    },
  };
}

/** A plug-type resistance box. Pulling a plug adds its coil in series; total() is the resistance. */
export function resistanceBox(values = [1, 2, 2, 5, 10, 20, 20, 50]) {
  const g = new THREE.Group();
  const W = values.length * 0.2 + 0.4;
  g.add(mesh(new THREE.BoxGeometry(W, 0.32, 0.6), MAT.gloss(0x6b3f1f), [0, 0.16, 0]));
  g.add(mesh(new THREE.BoxGeometry(W - 0.02, 0.02, 0.58), MAT.gloss(0x111827), [0, 0.33, 0]));
  const bar = mesh(new THREE.BoxGeometry(W - 0.3, 0.025, 0.09), brass(), [0, 0.352, 0]); g.add(bar);
  const plugs = values.map((v, i) => {
    const x = -W / 2 + 0.3 + i * 0.2;
    const lbl = mesh(new THREE.PlaneGeometry(0.16, 0.08), new THREE.MeshBasicMaterial({ map: canvasTexture(`ho-rb:${v}`, 64, 32, (c, w, h) => { c.fillStyle = '#111827'; c.fillRect(0, 0, w, h); c.fillStyle = '#fef3c7'; c.font = '700 22px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText(`${v}Ω`, w / 2, 24); }) }), [x + 0.1, 0.342, 0.17]);
    lbl.rotation.x = -Math.PI / 2; g.add(lbl);
    const plug = new THREE.Group(); plug.position.set(x + 0.1, 0.36, 0);
    plug.add(mesh(new THREE.CylinderGeometry(0.03, 0.022, 0.1, 12), brass(), [0, 0.02, 0]));
    plug.add(mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.1, 14), MAT.gloss(0x111827), [0, 0.11, 0]));
    g.add(plug);
    return { plug, value: v, out: false };
  });
  const posts = [-1, 1].map((s) => { const p = bindingPost(); p.position.set(s * (W / 2 - 0.12), 0.33, -0.18); g.add(p); return p; });
  return {
    group: g, plugs, posts,
    total() { return plugs.reduce((a, p) => a + (p.out ? p.value : 0), 0); },
    toggle(i, anim) {
      const p = plugs[i]; p.out = !p.out;
      const y0 = p.plug.position.y; const y1 = p.out ? 0.52 : 0.36; const z1 = p.out ? 0.32 : 0;
      const z0 = p.plug.position.z;
      if (anim) anim.add(0.35, (k) => { p.plug.position.y = y0 + (y1 - y0) * k + Math.sin(k * Math.PI) * 0.08; p.plug.position.z = z0 + (z1 - z0) * k; });
      else { p.plug.position.y = y1; p.plug.position.z = z1; }
    },
  };
}

export function plugKey() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.BoxGeometry(0.5, 0.06, 0.3), MAT.gloss(0x111827), [0, 0.03, 0]));
  [-0.09, 0.09].forEach((x) => g.add(mesh(new THREE.BoxGeometry(0.14, 0.05, 0.12), brass(), [x, 0.085, 0])));
  const plug = new THREE.Group(); plug.position.set(0, 0.16, 0.26);
  plug.add(mesh(new THREE.CylinderGeometry(0.028, 0.02, 0.1, 12), brass(), [0, -0.04, 0]));
  plug.add(mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.1, 14), MAT.gloss(0x111827), [0, 0.05, 0]));
  g.add(plug);
  const posts = [-0.2, 0.2].map((x) => { const p = bindingPost(); p.scale.setScalar(0.8); p.position.set(x, 0.06, -0.08); g.add(p); return p; });
  let closed = false;
  return {
    group: g, plug, posts,
    get closed() { return closed; },
    set(on, anim) {
      closed = on; const from = plug.position.clone(); const to = on ? new THREE.Vector3(0, 0.12, 0) : new THREE.Vector3(0, 0.16, 0.26);
      if (anim) anim.add(0.4, (k) => { plug.position.lerpVectors(from, to, k); plug.position.y += Math.sin(k * Math.PI) * 0.1; }); else plug.position.copy(to);
    },
  };
}

export function cell(label = '2 V') {
  const g = new THREE.Group();
  g.add(mesh(new THREE.BoxGeometry(0.55, 0.5, 0.36), MAT.gloss(0x0f172a), [0, 0.25, 0]));
  g.add(mesh(new THREE.BoxGeometry(0.56, 0.12, 0.37), MAT.gloss(0xb91c1c), [0, 0.44, 0]));
  const lbl = mesh(new THREE.PlaneGeometry(0.4, 0.14), new THREE.MeshBasicMaterial({ map: canvasTexture(`ho-cell:${label}`, 128, 48, (c, w, h) => { c.fillStyle = '#0f172a'; c.fillRect(0, 0, w, h); c.fillStyle = '#e2e8f0'; c.font = '800 26px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText(label, w / 2, 33); }) }), [0, 0.24, 0.181]);
  g.add(lbl);
  const posts = [-0.15, 0.15].map((x, i) => { const p = bindingPost(); p.position.set(x, 0.5, 0); p.children[2].material = MAT.gloss(i ? 0xb91c1c : 0x111827); g.add(p); return p; });
  return { group: g, posts };
}

/** Solves A x = b in place (small dense systems). */
export function solve(A, b) {
  const n = b.length;
  for (let i = 0; i < n; i++) {
    let p = i; for (let r = i + 1; r < n; r++) if (Math.abs(A[r][i]) > Math.abs(A[p][i])) p = r;
    [A[i], A[p]] = [A[p], A[i]]; [b[i], b[p]] = [b[p], b[i]];
    for (let r = i + 1; r < n; r++) { const f = A[r][i] / A[i][i]; for (let c = i; c < n; c++) A[r][c] -= f * A[i][c]; b[r] -= f * b[i]; }
  }
  const x = new Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) { let s = b[i]; for (let c = i + 1; c < n; c++) s -= A[i][c] * x[c]; x[i] = s / A[i][i]; }
  return x;
}

/** World-space top of a binding post, expressed in `space`'s local frame. */
export function postTop(post, space, out = new THREE.Vector3()) {
  out.copy(post.userData.top); post.localToWorld(out); return space.worldToLocal(out);
}
