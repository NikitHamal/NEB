// Plant parts for the physiology and botany practicals, at true size (1 unit = 10 cm): leaves with
// net or parallel venation (a glossy upper face and a paler lower face), stems swept along a
// curve, simple five-petalled flowers, buds and seedlings that can bend.
import { THREE } from '../../engine.js';
import { mesh, canvasTexture, wet } from '../kit.js';

/** Leaf outline in the XY plane, base at the origin, tip at +Y. */
function outline(len, wid, shape) {
  const s = new THREE.Shape(); const w = wid / 2;
  if (shape === 'linear') {
    s.moveTo(-w * 0.9, 0); s.quadraticCurveTo(-w, len * 0.6, 0, len); s.quadraticCurveTo(w, len * 0.6, w * 0.9, 0); s.lineTo(-w * 0.9, 0);
  } else if (shape === 'lanceolate') {
    s.moveTo(0, 0); s.bezierCurveTo(-w * 1.1, len * 0.2, -w * 0.8, len * 0.7, 0, len); s.bezierCurveTo(w * 0.8, len * 0.7, w * 1.1, len * 0.2, 0, 0);
  } else if (shape === 'cordate') {
    s.moveTo(0, len * 0.08); s.bezierCurveTo(-w * 0.6, -len * 0.08, -w * 1.25, len * 0.3, -w * 0.7, len * 0.62); s.quadraticCurveTo(-w * 0.3, len * 0.9, 0, len);
    s.quadraticCurveTo(w * 0.3, len * 0.9, w * 0.7, len * 0.62); s.bezierCurveTo(w * 1.25, len * 0.3, w * 0.6, -len * 0.08, 0, len * 0.08);
  } else {
    s.moveTo(0, 0); s.bezierCurveTo(-w * 1.3, len * 0.15, -w * 1.0, len * 0.75, 0, len); s.bezierCurveTo(w * 1.0, len * 0.75, w * 1.3, len * 0.15, 0, 0);
  }
  return s;
}
function veinTexture(kind, base, vein, pts, len, wid) {
  return canvasTexture(`leafv:${kind}:${base}:${vein}:${len}:${wid}:${pts.length}:${pts[3].x.toFixed(3)}`, 256, 512, (g, w, h) => {
    const X = (x) => (0.5 + x / (wid * 1.3)) * w; const Y = (y) => (1 - y / len) * h;
    g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(X(p.x), Y(p.y)) : g.moveTo(X(p.x), Y(p.y)))); g.closePath(); g.clip();
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    g.strokeStyle = vein; g.lineCap = 'round';
    if (kind === 'parallel') {
      for (let i = -6; i <= 6; i++) { g.lineWidth = i === 0 ? 5 : 1.6; g.beginPath(); g.moveTo(w / 2 + i * 16, h); g.quadraticCurveTo(w / 2 + i * 15, h * 0.4, w / 2 + i * 3, 0); g.stroke(); }
    } else {
      g.lineWidth = 7; g.beginPath(); g.moveTo(w / 2, h); g.lineTo(w / 2, 0); g.stroke();
      for (let i = 1; i < 9; i++) {
        const y = h - i * h / 9.5; g.lineWidth = 3;
        for (const s of [-1, 1]) {
          g.beginPath(); g.moveTo(w / 2, y); g.quadraticCurveTo(w / 2 + s * w * 0.25, y - 26, w / 2 + s * w * 0.48, y - 70); g.stroke();
          g.lineWidth = 1; for (let k = 0; k < 4; k++) { g.beginPath(); const x0 = w / 2 + s * (20 + k * 22); g.moveTo(x0, y - 8 - k * 9); g.lineTo(x0 + s * 6, y - 40 - k * 6); g.stroke(); }
          g.lineWidth = 3;
        }
      }
    }
    g.strokeStyle = 'rgba(0,0,0,0.25)'; g.lineWidth = 3; g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(X(p.x), Y(p.y)) : g.moveTo(X(p.x), Y(p.y)))); g.closePath(); g.stroke();
  });
}

/**
 * A leaf lying along +Z from its base, upper face up (+Y), gently arched. opts: len, wid, shape
 * ('ovate' | 'lanceolate' | 'linear' | 'cordate'), vein ('net' | 'parallel'), upper, lower colours.
 * The blade is a fine grid cut to the outline by its texture, so it bends smoothly.
 */
export function leaf(opts = {}) {
  const { len = 0.8, wid = 0.45, shape = 'ovate', vein = 'net', upper = '#2f7d32', lower = '#7fb069', arch = 0.08 } = opts;
  const W = wid * 1.3;
  const geo = new THREE.PlaneGeometry(W, len, 6, 14); geo.translate(0, len / 2, 0);
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i); const y = pos.getY(i);
    const t = y / len; pos.setXYZ(i, x, y, Math.sin(Math.PI * t) * arch * len * 0.5 - (x * x) / (wid * wid) * 0.06 * len);
  }
  geo.rotateX(-Math.PI / 2); geo.rotateY(Math.PI); geo.computeVertexNormals();
  const pts = outline(len, wid, shape).getPoints(24);
  const g = new THREE.Group();
  const up = mesh(geo, wet(upper, { map: veinTexture(vein, upper, 'rgba(210,240,180,0.55)', pts, len, wid), roughness: 0.42, clearcoat: 0.6, sheen: 0.1 }));
  up.material.alphaTest = 0.5; up.material.transparent = false;
  const loGeo = geo.clone(); const idx = loGeo.index.array; for (let i = 0; i < idx.length; i += 3) { const a = idx[i]; idx[i] = idx[i + 2]; idx[i + 2] = a; }
  loGeo.translate(0, -0.002, 0); loGeo.computeVertexNormals();
  const lo = mesh(loGeo, new THREE.MeshStandardMaterial({ color: 0xffffff, map: veinTexture(vein, lower, 'rgba(240,250,220,0.7)', pts, len, wid), roughness: 0.75, alphaTest: 0.5 }));
  up.castShadow = lo.castShadow = false;
  g.add(up, lo);
  g.userData.upper = up; g.userData.lower = lo; g.userData.len = len; g.userData.wid = wid; g.userData.arch = arch;
  g.userData.surfaceY = (z) => Math.sin(Math.PI * Math.min(1, Math.max(0, z / len))) * arch * len * 0.5;
  return g;
}

/** A stem swept along points [[x,y,z]...] with radius r (tapering to tipR). */
export function stem(points, r = 0.03, color = 0x4d7c0f, tipR) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(p[0], p[1], p[2])));
  const geo = new THREE.TubeGeometry(curve, Math.max(8, points.length * 6), r, 10, false);
  if (tipR !== undefined) {
    const pos = geo.attributes.position; const segs = geo.parameters.tubularSegments; const rad = geo.parameters.radialSegments;
    const p = new THREE.Vector3(); const c = new THREE.Vector3();
    for (let i = 0; i <= segs; i++) { const t = i / segs; curve.getPointAt(t, c); const k = (r + (tipR - r) * t) / r; for (let j = 0; j <= rad; j++) { const n = i * (rad + 1) + j; p.fromBufferAttribute(pos, n).sub(c).multiplyScalar(k).add(c); pos.setXYZ(n, p.x, p.y, p.z); } }
    geo.computeVertexNormals();
  }
  const m = mesh(geo, wet(color, { roughness: 0.55, clearcoat: 0.3 }));
  m.userData.curve = curve;
  return m;
}

/** A five-petalled open flower facing +Y, radius r. */
export function flower(color = 0xf472b6, r = 0.08, petals = 5, centre = 0xfacc15) {
  const g = new THREE.Group();
  const pm = wet(color, { roughness: 0.5, clearcoat: 0.3, sheen: 0.5, side: THREE.DoubleSide });
  for (let i = 0; i < petals; i++) {
    const p = mesh(new THREE.SphereGeometry(r * 0.5, 10, 6), pm); p.scale.set(0.75, 0.18, 1.2);
    const a = (i / petals) * Math.PI * 2; p.position.set(Math.cos(a) * r * 0.55, 0, Math.sin(a) * r * 0.55); p.rotation.y = -a + Math.PI / 2; p.rotation.x = -0.2;
    g.add(p);
  }
  g.add(mesh(new THREE.SphereGeometry(r * 0.22, 10, 8), wet(centre, { roughness: 0.7 }), [0, r * 0.05, 0]));
  return g;
}

/** A closed bud (ovoid), length h. */
export function bud(color = 0x65a30d, h = 0.05) {
  const m = mesh(new THREE.SphereGeometry(h * 0.35, 10, 8), wet(color, { roughness: 0.5 })); m.scale.set(1, 1.5, 1); m.position.y = h * 0.45;
  const g = new THREE.Group(); g.add(m); return g;
}

/**
 * A seedling standing in soil, height h, that can bend: setBend(angle) curves the upper part
 * toward +X (radians at the tip). Optional two cotyledon leaves (dicot) or a sheathed coleoptile.
 */
export function seedling(h = 0.7, opts = {}) {
  const { monocot = false, color = 0x84cc16 } = opts;
  const g = new THREE.Group();
  const N = 10; const geo = new THREE.CylinderGeometry(0.012, 0.016, h, 8, N); geo.translate(0, h / 2, 0);
  const base = geo.attributes.position.array.slice();
  const m = mesh(geo, wet(color, { roughness: 0.5, clearcoat: 0.3 })); g.add(m);
  const top = new THREE.Group(); g.add(top);
  if (monocot) top.add(mesh(new THREE.ConeGeometry(0.014, 0.05, 8), wet(0xd9f99d), [0, 0.02, 0]));
  else {
    [-1, 1].forEach((s) => { const l = leaf({ len: 0.16, wid: 0.1, upper: '#4d9a2a', lower: '#86c06a', arch: 0.05 }); l.rotation.y = s > 0 ? Math.PI / 2 : -Math.PI / 2; l.rotation.x = -0.35; top.add(l); });
  }
  let bend = 0;
  const cap = mesh(new THREE.CylinderGeometry(0.02, 0.022, 0.06, 10, 1, true), new THREE.MeshStandardMaterial({ color: 0x9ca3af, metalness: 0.9, roughness: 0.3, side: THREE.DoubleSide }), [0, 0.0, 0]);
  cap.visible = false; top.add(cap);
  function apply() {
    const pos = geo.attributes.position; const start = 0.45 * h; const L = h - start;
    const R = Math.abs(bend) > 1e-3 ? L / Math.abs(bend) : 1e9; const s = Math.sign(bend) || 1;
    for (let i = 0; i < pos.count; i++) {
      const x = base[i * 3]; const y = base[i * 3 + 1]; const z = base[i * 3 + 2];
      if (y <= start || R > 1e8) { pos.setXYZ(i, x, y, z); continue; }
      const th = (y - start) / R; const cx = s * (R - (R - s * x) * Math.cos(th)); const cy = start + (R - s * x) * Math.sin(th);
      pos.setXYZ(i, cx, cy, z);
    }
    pos.needsUpdate = true; geo.computeVertexNormals();
    const th = bend; const tx = R > 1e8 ? 0 : s * (R - R * Math.cos(Math.abs(th))); const ty = R > 1e8 ? h : start + R * Math.sin(Math.abs(th));
    top.position.set(tx, ty, 0); top.rotation.z = -th;
  }
  apply();
  return { group: g, top, cap, get bend() { return bend; }, setBend(a) { bend = a; apply(); }, h };
}
