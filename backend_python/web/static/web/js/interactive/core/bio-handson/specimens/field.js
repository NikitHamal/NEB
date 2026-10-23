// A school field plot for quadrat work, at true size (1 unit = 10 cm): a 6 m × 6 m patch of
// trampled grassland pegged out with string, and the herbs counted in it — dubo grass tufts
// (Cynodon dactylon, random), chari amilo (Oxalis corniculata, in clumps), gandhe (Ageratum
// conyzoides, random) and the invasive Parthenium hysterophorus (sparse). Each species is one
// instanced mesh, so hundreds of plants cost a handful of draw calls and can be picked one by one.
import { THREE } from '../../engine.js';
import { mesh, MAT, canvasTexture, rng } from '../kit.js';
import { mergeGeos } from '../bench.js';

export const HALF = 30;
export const SPECIES = [
  { id: 'cyn', name: 'Cynodon dactylon (dubo)', short: 'Cynodon', density: 3.2, clumped: false, color: '#65a30d' },
  { id: 'oxa', name: 'Oxalis corniculata (chari amilo)', short: 'Oxalis', density: 3.0, clumped: true, color: '#16a34a' },
  { id: 'age', name: 'Ageratum conyzoides (gandhe)', short: 'Ageratum', density: 1.4, clumped: false, color: '#7c3aed' },
  { id: 'par', name: 'Parthenium hysterophorus', short: 'Parthenium', density: 0.55, clumped: false, color: '#e5e7eb' },
];

const T = (g, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, s = 1) => { if (Array.isArray(s)) g.scale(s[0], s[1], s[2]); else g.scale(s, s, s); g.rotateX(rx); g.rotateY(ry); g.rotateZ(rz); g.translate(x, y, z); return g; };
function geoFor(id) {
  if (id === 'cyn') {
    const parts = []; for (let i = 0; i < 9; i++) { const a = i / 9 * Math.PI * 2; parts.push([T(new THREE.ConeGeometry(0.03, 0.75, 3), Math.cos(a) * 0.06, 0.34, Math.sin(a) * 0.06, Math.sin(a) * 0.35, 0, -Math.cos(a) * 0.35), i % 2 ? 0x4d7c0f : 0x65a30d]); }
    parts.push([T(new THREE.CylinderGeometry(0.004, 0.004, 0.5, 4), 0, 0.85, 0), 0x84cc16]);
    for (let i = 0; i < 4; i++) { const a = i / 4 * Math.PI * 2; parts.push([T(new THREE.CylinderGeometry(0.006, 0.004, 0.22, 4), Math.cos(a) * 0.08, 1.12, Math.sin(a) * 0.08, Math.sin(a) * 0.7, 0, -Math.cos(a) * 0.7), 0x7c2d12]); }
    return mergeGeos(parts);
  }
  if (id === 'oxa') {
    const parts = [];
    for (let k = 0; k < 4; k++) {
      const a = k * 1.7; const r = 0.16; const cx = Math.cos(a) * r; const cz = Math.sin(a) * r;
      parts.push([T(new THREE.CylinderGeometry(0.006, 0.006, 0.2, 4), cx / 2, 0.08, cz / 2, Math.sin(a) * 0.9, 0, -Math.cos(a) * 0.9), 0x15803d]);
      for (let j = 0; j < 3; j++) { const b = j / 3 * Math.PI * 2 + a; parts.push([T(new THREE.CircleGeometry(0.055, 8), cx + Math.cos(b) * 0.05, 0.17, cz + Math.sin(b) * 0.05, -Math.PI / 2 + 0.25, 0, 0), j % 2 ? 0x22a148 : 0x16a34a]); }
    }
    parts.push([T(new THREE.SphereGeometry(0.025, 6, 4), 0.05, 0.2, 0.05), 0xfacc15]);
    return mergeGeos(parts);
  }
  if (id === 'age') {
    const parts = [[T(new THREE.CylinderGeometry(0.014, 0.02, 1.4, 5), 0, 0.7, 0), 0x6b8e23]];
    for (let i = 0; i < 6; i++) { const a = i * 2.3; const y = 0.3 + i * 0.17; parts.push([T(new THREE.SphereGeometry(0.11, 6, 4), Math.cos(a) * 0.12, y, Math.sin(a) * 0.12, 0, -a, 0, [1, 0.2, 0.7]), 0x3f7d20]); }
    for (let i = 0; i < 7; i++) { const a = i * 0.9; parts.push([T(new THREE.SphereGeometry(0.045, 6, 5), Math.cos(a) * 0.08, 1.42 + (i % 2) * 0.04, Math.sin(a) * 0.08), 0x8b5cf6]); }
    return mergeGeos(parts);
  }
  const parts = [[T(new THREE.CylinderGeometry(0.016, 0.022, 2.0, 5), 0, 1.0, 0), 0x65a30d]];
  for (let i = 0; i < 8; i++) { const a = i * 2.1; const y = 0.25 + i * 0.2; parts.push([T(new THREE.BoxGeometry(0.26, 0.01, 0.05), Math.cos(a) * 0.13, y, Math.sin(a) * 0.13, 0, -a, 0.3), 0x4d7c0f]); parts.push([T(new THREE.BoxGeometry(0.06, 0.01, 0.14), Math.cos(a) * 0.18, y, Math.sin(a) * 0.18, 0, -a, 0.3), 0x4d7c0f]); }
  for (let i = 0; i < 9; i++) { const a = i * 0.7; parts.push([T(new THREE.SphereGeometry(0.035, 6, 4), Math.cos(a) * 0.14, 2.0 + (i % 3) * 0.05, Math.sin(a) * 0.14), 0xf8fafc]); }
  return mergeGeos(parts);
}

/** Builds the plot. Returns { group, plants: [{ sp, x, z, i }], meshes: { id: InstancedMesh }, R }. */
export function buildField(seed = 1) {
  const R = rng(seed);
  const g = new THREE.Group();
  const grass = canvasTexture('field-grass', 512, 512, (c, w, h) => {
    c.fillStyle = '#8aa65a'; c.fillRect(0, 0, w, h);
    for (let i = 0; i < 9000; i++) { const v = Math.random(); c.strokeStyle = v < 0.4 ? 'rgba(90,120,50,0.6)' : v < 0.75 ? 'rgba(150,170,90,0.5)' : 'rgba(120,95,60,0.45)'; c.lineWidth = 1 + Math.random(); const x = Math.random() * w; const y = Math.random() * h; c.beginPath(); c.moveTo(x, y); c.lineTo(x + (Math.random() - 0.5) * 6, y - 3 - Math.random() * 7); c.stroke(); }
  }, { repeat: [14, 14] });
  const ground = mesh(new THREE.PlaneGeometry(HALF * 2 + 40, HALF * 2 + 40), new THREE.MeshStandardMaterial({ map: grass, roughness: 1 }), [0, 0, 0]);
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; ground.castShadow = false; g.add(ground); g.userData.ground = ground;
  // pegs and string round the plot
  const peg = MAT.matte(0x92400e);
  [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([a, b]) => g.add(mesh(new THREE.CylinderGeometry(0.06, 0.05, 1.2, 6), peg, [a * HALF, 0.5, b * HALF])));
  const str = MAT.matte(0xf8fafc);
  [[0, -HALF, HALF * 2, 0], [0, HALF, HALF * 2, 0], [-HALF, 0, HALF * 2, Math.PI / 2], [HALF, 0, HALF * 2, Math.PI / 2]].forEach(([x, z, L, r]) => { const m = mesh(new THREE.CylinderGeometry(0.02, 0.02, L, 4), str, [x, 0.6, z]); m.rotation.set(0, r, Math.PI / 2); g.add(m); });
  const plants = []; const meshes = {};
  SPECIES.forEach((sp) => {
    const n = Math.round(sp.density * (HALF * 2 / 10) ** 2 * (0.9 + R() * 0.2));
    const pts = [];
    if (sp.clumped) {
      const nc = 7; const centres = Array.from({ length: nc }, () => [(R() * 2 - 1) * (HALF - 4), (R() * 2 - 1) * (HALF - 4)]);
      for (let i = 0; i < n; i++) { const c = centres[i % nc]; const r = Math.sqrt(-2 * Math.log(Math.max(1e-6, R()))) * 2.6; const a = R() * Math.PI * 2; pts.push([Math.max(-HALF + 0.3, Math.min(HALF - 0.3, c[0] + Math.cos(a) * r)), Math.max(-HALF + 0.3, Math.min(HALF - 0.3, c[1] + Math.sin(a) * r))]); }
    } else for (let i = 0; i < n; i++) pts.push([(R() * 2 - 1) * (HALF - 0.3), (R() * 2 - 1) * (HALF - 0.3)]);
    const im = new THREE.InstancedMesh(geoFor(sp.id), new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.75, side: THREE.DoubleSide }), pts.length);
    const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const s = new THREE.Vector3(); const p = new THREE.Vector3();
    pts.forEach(([x, z], i) => { q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), R() * 6.28); const k = 0.75 + R() * 0.5; s.set(k, k, k); p.set(x, 0, z); m4.compose(p, q, s); im.setMatrixAt(i, m4); plants.push({ sp, x, z, i, k }); });
    im.castShadow = true; im.receiveShadow = false; im.userData.sp = sp; g.add(im); meshes[sp.id] = im;
  });
  return { group: g, plants, meshes, R };
}

/** A 1 m × 1 m quadrat frame of white PVC pipe, corner at the origin's centre. */
export function quadratFrame() {
  const g = new THREE.Group(); const m = MAT.gloss(0xf8fafc); const L = 10;
  [[0, -5, 0], [0, 5, 0], [-5, 0, 1], [5, 0, 1]].forEach(([x, z, r]) => { const p = mesh(new THREE.CylinderGeometry(0.11, 0.11, L + 0.2, 10), m, [x, 0.12, z]); if (r) p.rotation.set(Math.PI / 2, 0, 0); else p.rotation.set(0, 0, Math.PI / 2); g.add(p); });
  [[-5, -5], [5, -5], [5, 5], [-5, 5]].forEach(([x, z]) => g.add(mesh(new THREE.SphereGeometry(0.16, 10, 8), m, [x, 0.12, z])));
  return g;
}
