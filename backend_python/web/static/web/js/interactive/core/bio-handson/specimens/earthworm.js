// Pheretima posthuma, the Indian earthworm of the NEB practical, for dissection: about 100
// segments, a pointed prostomium, the clitellum on segments 14-16, a darker dorsal surface
// with the dorsal blood vessel showing as a line, and on the ventral side the female pore (14),
// the paired male pores (18) and genital papillae (17, 19). Inside: buccal cavity (1-3),
// pharynx (4), oesophagus (5-7), gizzard (8-9), stomach (9-14), intestine (15 to the anus)
// coated in yellow-brown chloragogen cells, paired intestinal caeca from segment 26 reaching
// forward to 22, the dorsal blood vessel, four pairs of hearts (7, 9, 12, 13) and the septa.
// The body wall is built as a base and two flaps either side of the mid-dorsal incision, so it
// can be cut, peeled back and pinned. 1 unit = 10 cm; length 2.0 (20 cm), radius 0.45 cm.
import { THREE } from '../../engine.js';
import { canvasTexture, wet, mesh, clamp, smooth, rng } from '../kit.js';

export const N_SEG = 100;
export const LENGTH = 2.0;
export const R0 = 0.045;
const SEG = LENGTH / N_SEG;
const GUT_Y = -0.1 * R0;
export const CUT_THETA = -0.16; // the incision runs just to the left of the mid-dorsal line

/** x of the centre of segment s (1-based); anterior is -x. */
export const segX = (s) => -LENGTH / 2 + (s - 0.5) * SEG;
export const xSeg = (x) => (x + LENGTH / 2) / SEG + 0.5;

function profile(u) {
  let r;
  if (u < 0.07) r = 0.22 + 0.78 * Math.sin((u / 0.07) * Math.PI / 2);
  else if (u < 0.3) r = 1 + 0.04 * smooth(0.12, 0.16, u) * (1 - smooth(0.16, 0.2, u));
  else r = 1 - 0.16 * smooth(0.3, 0.92, u);
  if (u > 0.955) r *= Math.sqrt(Math.max(0.02, 1 - Math.pow((u - 0.955) / 0.045, 2)));
  return r;
}
export function smoothRadiusAt(x) { return R0 * profile(clamp((x + LENGTH / 2) / LENGTH, 0, 1)); }
/** Body radius at x, with the intersegmental grooves (none across the clitellum). */
export function radiusAt(x) {
  const u = clamp((x + LENGTH / 2) / LENGTH, 0, 1);
  const s = u * N_SEG; const f = s - Math.round(s);
  const seg = Math.floor(s) + 1;
  const clit = seg >= 14 && seg <= 16 ? 0.15 : 1;
  const groove = Math.exp(-(f * f) / 0.012) * 0.07 * clit;
  return R0 * profile(u) * (1 - groove);
}
const flat = (y, r) => (y < 0 ? y * 0.78 : y);
const OPEN_ANGLE = -0.32;
const FLOOR = -R0 * 0.95;

function skinTexture(ventralUp) {
  return canvasTexture('worm-skin', 2048, 256, (g, w, h) => {
    const R = rng(7);
    for (let y = 0; y < h; y++) {
      const th = (y / h) * Math.PI * 2 - Math.PI; // v -> theta, dorsal at the middle
      const dors = (Math.cos(th) + 1) / 2;
      const r = 92 + 92 * (1 - dors); const gg = 52 + 66 * (1 - dors); const b = 48 + 58 * (1 - dors);
      g.fillStyle = `rgb(${r | 0},${gg | 0},${b | 0})`; g.fillRect(0, y, w, 1);
    }
    const sw = w / N_SEG;
    for (let s = 0; s < N_SEG; s++) {
      const x = s * sw;
      const seg = s + 1;
      if (seg >= 14 && seg <= 16) {
        g.fillStyle = 'rgba(120,52,40,0.92)'; g.fillRect(x, 0, sw + 1, h);
        for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(80,30,24,${0.2 + R() * 0.3})`; g.fillRect(x + R() * sw, R() * h, 2, 2); }
        continue;
      }
      const gr = g.createLinearGradient(x, 0, x + sw, 0);
      gr.addColorStop(0, 'rgba(30,14,12,0.45)'); gr.addColorStop(0.18, 'rgba(255,230,220,0.05)'); gr.addColorStop(0.5, 'rgba(255,235,225,0.10)'); gr.addColorStop(0.85, 'rgba(0,0,0,0.04)'); gr.addColorStop(1, 'rgba(30,14,12,0.45)');
      g.fillStyle = gr; g.fillRect(x, 0, sw, h);
      // setae: a ring of tiny pale points around the middle of each segment
      if (seg > 1 && seg < N_SEG) { g.fillStyle = 'rgba(240,220,200,0.35)'; for (let k = 0; k < 16; k++) g.fillRect(x + sw * 0.5, (k / 16) * h + R() * 4, 1.5, 1.5); }
    }
    // dorsal blood vessel seen through the skin, the mid-dorsal line
    const dy = h / 2;
    const dg = g.createLinearGradient(0, dy - 6, 0, dy + 6);
    dg.addColorStop(0, 'rgba(60,10,25,0)'); dg.addColorStop(0.5, 'rgba(70,8,28,0.75)'); dg.addColorStop(1, 'rgba(60,10,25,0)');
    g.fillStyle = dg; g.fillRect(sw * 1, dy - 6, w - sw * 2, 12);
    // ventral: female pore (14), male pores (18), genital papillae (17, 19)
    const vy = [h * 0.02, h * 0.98];
    const pore = (seg, off, rad, col) => { vy.forEach((yy) => { g.fillStyle = col; g.beginPath(); g.ellipse((seg - 0.5) * sw, (yy + off + h) % h, rad, rad * 0.8, 0, 0, Math.PI * 2); g.fill(); }); };
    pore(14, 0, 3, 'rgba(40,12,10,0.9)');
    [18].forEach((s) => { pore(s, 14, 4, 'rgba(70,24,20,0.85)'); pore(s, -14, 4, 'rgba(70,24,20,0.85)'); });
    [17, 19].forEach((s) => { pore(s, 10, 3.5, 'rgba(225,180,160,0.9)'); pore(s, -10, 3.5, 'rgba(225,180,160,0.9)'); });
    void ventralUp;
  }, { anisotropy: 8 });
}
function bumpTexture() {
  return canvasTexture('worm-bump', 1024, 32, (g, w, h) => {
    const sw = w / N_SEG;
    g.fillStyle = '#888'; g.fillRect(0, 0, w, h);
    for (let s = 0; s < N_SEG; s++) {
      if (s + 1 >= 14 && s + 1 <= 16) continue;
      const gr = g.createLinearGradient(s * sw, 0, s * sw + sw, 0);
      gr.addColorStop(0, '#222'); gr.addColorStop(0.25, '#9a9a9a'); gr.addColorStop(0.5, '#b0b0b0'); gr.addColorStop(0.75, '#9a9a9a'); gr.addColorStop(1, '#222');
      g.fillStyle = gr; g.fillRect(s * sw, 0, sw, h);
    }
  }, { color: false });
}
function innerTexture() {
  return canvasTexture('worm-inner', 1024, 128, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, '#e6b8ae'); gr.addColorStop(0.5, '#eec6bc'); gr.addColorStop(1, '#e3b2a8');
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    const R = rng(3);
    for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(214,140,135,${0.05 + R() * 0.1})`; g.fillRect(R() * w, R() * h, 3 + R() * 14, 1); }
    const sw = w / N_SEG;
    for (let s = 1; s < N_SEG; s++) { g.fillStyle = 'rgba(205,130,125,0.22)'; g.fillRect(s * sw - 0.5, 0, 1, h); }
    for (let i = 0; i < 60; i++) { g.strokeStyle = 'rgba(180,60,70,0.18)'; g.lineWidth = 0.8; g.beginPath(); let x = R() * w; let y = R() * h; g.moveTo(x, y); for (let k = 0; k < 5; k++) { x += (R() - 0.5) * 20; y += (R() - 0.5) * 14; g.lineTo(x, y); } g.stroke(); }
  });
}

/** Builds a closed-tube patch: rows along x, columns over theta from a to b. */
function shellGeometry(rings, cols, a, b, inset = 0) {
  const pos = new Float32Array((rings + 1) * (cols + 1) * 3); const uv = new Float32Array((rings + 1) * (cols + 1) * 2);
  for (let i = 0; i <= rings; i++) {
    const x = -LENGTH / 2 + (i / rings) * LENGTH; const r = inset > 0 ? smoothRadiusAt(x) - inset : radiusAt(x);
    for (let j = 0; j <= cols; j++) {
      const th = a + (b - a) * (j / cols); const k = (i * (cols + 1) + j);
      pos[k * 3] = x; pos[k * 3 + 1] = flat(r * Math.cos(th), r); pos[k * 3 + 2] = r * Math.sin(th);
      uv[k * 2] = i / rings; uv[k * 2 + 1] = (th + Math.PI) / (Math.PI * 2);
    }
  }
  const idx = [];
  for (let i = 0; i < rings; i++) for (let j = 0; j < cols; j++) { const p = i * (cols + 1) + j; const q = p + cols + 1; idx.push(p, p + 1, q, q, p + 1, q + 1); }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

/**
 * A body-wall flap from the incision (theta = CUT_THETA) to the lateral hinge (theta = side*pi/2).
 * Its cross-section unrolls about the hinge: an arc of curvature (1-t)/r whose start tangent turns
 * from straight up (closed) to lying flat on the wax (open). open(t, grabX) re-poses the vertices.
 */
function makeFlap(side, rings, cols, outerMat, innerMat, thick) {
  const a = side > 0 ? CUT_THETA : -Math.PI / 2; const b = side > 0 ? Math.PI / 2 : CUT_THETA;
  const outer = shellGeometry(rings, cols, a, b, 0);
  const inner = shellGeometry(rings, cols, a, b, thick);
  const group = new THREE.Group();
  const mo = mesh(outer, outerMat); const mi = mesh(inner, innerMat);
  mi.material.side = THREE.BackSide;
  group.add(mo, mi);
  const arc = new Float32Array((rings + 1) * (cols + 1)); // arc length from the hinge, per vertex
  const xs = new Float32Array(rings + 1); const rs = new Float32Array(rings + 1); const rsm = new Float32Array(rings + 1);
  for (let i = 0; i <= rings; i++) { xs[i] = -LENGTH / 2 + (i / rings) * LENGTH; rs[i] = radiusAt(xs[i]); rsm[i] = smoothRadiusAt(xs[i]); }
  for (let i = 0; i <= rings; i++) for (let j = 0; j <= cols; j++) {
    const th = a + (b - a) * (j / cols);
    arc[i * (cols + 1) + j] = rs[i] * (Math.PI / 2 - side * th);
  }
  let lastT = -1; let lastG = 0;
  function pose(T, grabX = 0, spread = 0.5) {
    if (Math.abs(T - lastT) < 1e-4 && Math.abs(grabX - lastG) < 1e-4) return;
    lastT = T; lastG = grabX;
    const po = outer.attributes.position.array; const pi = inner.attributes.position.array;
    for (let i = 0; i <= rings; i++) {
      const x = xs[i]; const r = rs[i];
      const t = clamp(T * 1.35 - Math.abs(x - grabX) * spread * (1 - T), 0, 1) * smooth(segX(2.2), segX(5), x) * (1 - smooth(segX(95), segX(97.8), x));
      const th0 = (Math.PI / 2) * (1 - t) + OPEN_ANGLE * t;
      for (let j = 0; j <= cols; j++) {
        const k = i * (cols + 1) + j;
        for (let pass = 0; pass < 2; pass++) {
          const rr = pass ? rsm[i] : r; const kk = (1 - t) / rr; const s = arc[k] * rr / r;
          let u; let v; let th;
          if (kk > 1e-4) { th = th0 + kk * s; u = rr + (Math.sin(th) - Math.sin(th0)) / kk; v = -(Math.cos(th) - Math.cos(th0)) / kk; }
          else { th = th0; u = rr + s * Math.cos(th0); v = s * Math.sin(th0); }
          if (pass === 0) { v = Math.max(v, FLOOR); po[k * 3] = x; po[k * 3 + 1] = flat(v, r); po[k * 3 + 2] = side * u; }
          else {
            const nu = -Math.sin(th); const nv = Math.cos(th);
            pi[k * 3] = x; pi[k * 3 + 1] = flat(Math.max(v + nv * thick, FLOOR + thick), r); pi[k * 3 + 2] = side * (u + nu * thick);
          }
        }
      }
    }
    outer.attributes.position.needsUpdate = true; inner.attributes.position.needsUpdate = true;
    outer.computeVertexNormals(); inner.computeVertexNormals();
    outer.computeBoundingSphere(); inner.computeBoundingSphere();
  }
  /** World-ish (worm-local) point on the flap at arc fraction f of the free edge, at x, for t. */
  function edgePoint(x, f, T, out) {
    const r = radiusAt(x); const S = r * (Math.PI / 2 - side * CUT_THETA) * f;
    const th0 = (Math.PI / 2) * (1 - T) + OPEN_ANGLE * T; const kc = (1 - T) / r;
    let u; let v;
    if (kc > 1e-4) { const th = th0 + kc * S; u = r + (Math.sin(th) - Math.sin(th0)) / kc; v = -(Math.cos(th) - Math.cos(th0)) / kc; }
    else { u = r + S * Math.cos(th0); v = S * Math.sin(th0); }
    return out.set(x, flat(Math.max(v, FLOOR), r), side * u);
  }
  pose(0);
  return { group, outer: mo, inner: mi, pose, edgePoint };
}

const GUT = [
  // [from segment, to segment, radius factor, colour, name]
  [0.6, 3.5, 0.24, 0xd99a95, 'Buccal cavity'],
  [3.5, 4.9, 0.56, 0xe7a3a6, 'Pharynx'],
  [4.9, 7.6, 0.22, 0xd98f8f, 'Oesophagus'],
  [7.6, 9.4, 0.53, 0xf0ddd2, 'Gizzard'],
  [9.4, 14.5, 0.3, 0xd6857f, 'Stomach'],
  [14.5, 100, 0.5, 0xb38a42, 'Intestine'],
];
function gutRadius(s) {
  let r = 0.24;
  for (let i = 0; i < GUT.length; i++) {
    const [a, b, rr] = GUT[i];
    if (s >= a && s < b) {
      r = rr;
      if (i === 1 || i === 3) { const m = (s - a) / (b - a); r = rr * (0.55 + 0.45 * Math.sin(m * Math.PI)); }
      if (i === 5) { const f = s - Math.floor(s); r = rr * (0.92 + 0.08 * Math.sin(f * Math.PI)) * (1 - 0.3 * smooth(90, 100, s)); }
      break;
    }
  }
  const prev = GUT.find((g) => s >= g[0] - 0.4 && s < g[0]);
  return r * (prev ? 0.9 : 1);
}
export function organAt(s) { for (const g of GUT) if (s >= g[0] && s < g[1]) return g[4]; return null; }

function gutGeometry(rings, radial) {
  const pos = []; const col = []; const idx = [];
  const c = new THREE.Color(); const R = rng(11);
  for (let i = 0; i <= rings; i++) {
    const s = 0.6 + (i / rings) * 99.3; const x = segX(s);
    const gr = gutRadius(s) * R0 * (1 - 0.5 * smooth(99.3, 99.9, s)); const yc = GUT_Y;
    const g = GUT.find((q) => s >= q[0] && s < q[1]) || GUT[GUT.length - 1];
    for (let j = 0; j <= radial; j++) {
      const th = (j / radial) * Math.PI * 2;
      pos.push(x, yc + gr * Math.cos(th) * 0.92, gr * Math.sin(th));
      c.setHex(g[3]);
      if (g[4] === 'Intestine') { const m = 0.9 + R() * 0.16 + 0.06 * Math.sin(th * 3 + s * 1.7); c.r *= m; c.g *= m * 0.98; c.b *= m * 0.88; }
      else { const m = 0.95 + R() * 0.08; c.r *= m; c.g *= m; c.b *= m; }
      col.push(c.r, c.g, c.b);
    }
  }
  for (let i = 0; i < rings; i++) for (let j = 0; j < radial; j++) { const p = i * (radial + 1) + j; const q = p + radial + 1; idx.push(p, p + 1, q, q, p + 1, q + 1); }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); geo.setIndex(idx);
  geo.computeVertexNormals();
  return geo;
}

export function buildEarthworm(quality) {
  const low = quality.tier === 'low';
  const rings = low ? 200 : 300; const cols = low ? 8 : 12;
  const root = new THREE.Group(); root.name = 'earthworm';
  const body = new THREE.Group(); root.add(body);
  const skin = skinTexture(); const bump = bumpTexture();
  const skinMat = () => {
    const m = wet(0xffffff, { map: skin, bumpMap: bump, bumpScale: 1.4, roughness: 0.42, clearcoat: 0.8, ccr: 0.18, sheen: 0.2, sheenColor: 0x9db4ff });
    if (!low) { m.iridescence = 0.35; m.iridescenceIOR = 1.6; m.iridescenceThicknessRange = [200, 520]; }
    return m;
  };
  const innerMat = () => wet(0xffffff, { map: innerTexture(), roughness: 0.5, clearcoat: 0.9, ccr: 0.15, sheen: 0.3 });
  const thick = R0 * 0.12;
  const baseOuter = mesh(shellGeometry(rings, cols * 2, Math.PI / 2, Math.PI * 1.5, 0), skinMat());
  const baseInner = mesh(shellGeometry(rings, cols * 2, Math.PI / 2, Math.PI * 1.5, thick), innerMat());
  baseInner.material.side = THREE.BackSide;
  body.add(baseOuter, baseInner);
  const right = makeFlap(1, rings, cols, skinMat(), innerMat(), thick);
  const left = makeFlap(-1, rings, cols, skinMat(), innerMat(), thick);
  body.add(right.group, left.group);

  // inside: the gut with its regions, caeca, dorsal vessel, hearts and septa
  const inside = new THREE.Group(); inside.visible = false; body.add(inside);
  const gutMat = wet(0xffffff, { roughness: 0.38, clearcoat: 0.9, ccr: 0.12, sheen: 0.25 });
  gutMat.vertexColors = true;
  const gut = mesh(gutGeometry(rings, low ? 12 : 18), gutMat, null, { name: 'gut' });
  inside.add(gut);
  const caecumMat = wet(0xd2b277, { roughness: 0.4 });
  [1, -1].forEach((side) => {
    const c = mesh(new THREE.ConeGeometry(R0 * 0.2, segX(26) - segX(21.5), 12), caecumMat, null, { name: 'caecum' });
    c.rotation.z = Math.PI / 2; c.position.set((segX(26) + segX(21.5)) / 2, GUT_Y + R0 * 0.05, side * R0 * 0.56);
    c.rotation.y = -side * 0.12;
    inside.add(c);
  });
  const vesselMat = wet(0x9b1022, { roughness: 0.3, clearcoat: 1, emissive: 0x200000 });
  const vpts = []; for (let s = 1.2; s <= 99; s += 1) vpts.push(new THREE.Vector3(segX(s), GUT_Y + gutRadius(s) * R0 * 0.92 + R0 * 0.03, 0));
  inside.add(mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(vpts), 200, R0 * 0.045, 6), vesselMat, null, { name: 'dorsal vessel' }));
  const heartMat = wet(0xb3142c, { roughness: 0.3, clearcoat: 1 });
  [7, 9, 12, 13].forEach((s) => {
    const gr = gutRadius(s) * R0;
    const h = mesh(new THREE.TorusGeometry(gr + R0 * 0.12, R0 * 0.06, 8, 20, Math.PI * 1.1), heartMat, null, { name: 'heart' });
    h.rotation.y = Math.PI / 2; h.rotation.z = -Math.PI * 0.05; h.position.set(segX(s), GUT_Y, 0);
    inside.add(h);
  });
  // septa: thin membranes at the segment boundaries (none in 1-4 and between 9 and 10)
  const septumGeo = new THREE.RingGeometry(0.35, 1, 18, 1);
  septumGeo.rotateY(Math.PI / 2);
  const septumMat = new THREE.MeshPhysicalMaterial({ color: 0xf3c9c2, roughness: 0.35, transparent: true, opacity: 0.55, side: THREE.DoubleSide, depthWrite: false, clearcoat: 0.6 });
  const septaIdx = []; for (let s = 4; s < 99; s++) if (s !== 9) septaIdx.push(s);
  const septa = new THREE.InstancedMesh(septumGeo, septumMat, septaIdx.length);
  septa.userData.noPick = true;
  const sm = new THREE.Matrix4(); const sq = new THREE.Quaternion(); const ss = new THREE.Vector3(); const sp = new THREE.Vector3();
  const septumState = new Float32Array(septaIdx.length).fill(1);
  function setSeptum(i, k) {
    septumState[i] = k;
    const x = segX(septaIdx[i] + 0.5); const r = radiusAt(x) * 0.93;
    sp.set(x, -0.08 * R0, 0); ss.set(1, r * (0.45 + 0.55 * k), r * (0.45 + 0.55 * k) * (k < 1 ? 0.92 : 1));
    sm.compose(sp, sq, ss); septa.setMatrixAt(i, sm);
  }
  septaIdx.forEach((_, i) => setSeptum(i, 1));
  septa.instanceMatrix.needsUpdate = true;
  inside.add(septa);

  // the worm lies with its flattened ventral surface on the wax
  const restY = R0 * 0.78;
  root.position.y = restY;
  return {
    root, body, inside, gut, left, right, septa, septaIdx, septumState, restY,
    tearSeptum(i, k) { setSeptum(i, k); septa.instanceMatrix.needsUpdate = true; },
    pickables: [baseOuter, right.outer, left.outer],
    flapMeshes: [right.outer, right.inner, left.outer, left.inner],
    organParts: inside,
    anchors: {
      'Buccal cavity': new THREE.Vector3(segX(2), R0 * 0.05, 0),
      Pharynx: new THREE.Vector3(segX(4.2), R0 * 0.35, 0),
      Oesophagus: new THREE.Vector3(segX(6.2), R0 * 0.08, 0),
      Gizzard: new THREE.Vector3(segX(8.5), R0 * 0.38, 0),
      Stomach: new THREE.Vector3(segX(12), R0 * 0.12, 0),
      'Intestinal caeca': new THREE.Vector3(segX(24), -0.05 * R0, R0 * 0.55),
      Intestine: new THREE.Vector3(segX(29), R0 * 0.3, 0),
      Hearts: new THREE.Vector3(segX(13), -0.1 * R0, -R0 * 0.5),
    },
  };
}
