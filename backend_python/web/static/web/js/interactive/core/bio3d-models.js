import { THREE, makeLabelSprite } from './engine.js';
import { getBiologyMetricRows, getBiologyFormula } from './bio3d-science.js';
import { addScanGradeEnhancement, disposeScanGradeAssets } from './bio3d-scan-grade.js';
import { batchStaticGeometry } from './bio3d-batch.js';

// Production-grade procedural biology models for NEB practicals.
// No external meshes are required: every model is generated from optimized Three.js primitives,
// deterministic seeded layouts, anatomical proportions, and labelled scientific landmarks.

const MATERIAL_CACHE = new Map();
const Y_AXIS = new THREE.Vector3(0, 1, 0);

function mat(color, opts = {}) {
  const key = JSON.stringify([color, opts]);
  if (MATERIAL_CACHE.has(key)) return MATERIAL_CACHE.get(key);
  const m = new THREE.MeshStandardMaterial({
    color,
    roughness: opts.roughness ?? 0.62,
    metalness: opts.metalness ?? 0.02,
    transparent: opts.opacity !== undefined && opts.opacity < 1,
    opacity: opts.opacity ?? 1,
    emissive: opts.emissive ?? 0x000000,
    emissiveIntensity: opts.emissiveIntensity ?? 0,
    side: opts.side ?? THREE.FrontSide,
    flatShading: opts.flatShading ?? false,
  });
  m.__shared = true;
  MATERIAL_CACHE.set(key, m);
  return m;
}
function glass(color = 0xdbeafe, opacity = 0.28) { return mat(color, { opacity, roughness: 0.04, metalness: 0.0, side: THREE.DoubleSide }); }
function metal(color = 0x94a3b8) { return mat(color, { roughness: 0.26, metalness: 0.78 }); }
function organic(color = 0x3f8f2f) { return mat(color, { roughness: 0.86, metalness: 0.0 }); }
function tissue(color = 0xc43b59) { return mat(color, { roughness: 0.48, metalness: 0.0, emissive: color, emissiveIntensity: 0.025 }); }
function boneMaterial() { return mat(0xf1ead8, { roughness: 0.72, metalness: 0.0 }); }

function box(w, h, d, material, pos = [0, 0, 0]) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material); m.position.set(...pos); m.castShadow = true; m.receiveShadow = true; return m; }
function cyl(r1, r2, h, material, pos = [0, 0, 0], seg = 32) { const m = new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), material); m.position.set(...pos); m.castShadow = true; m.receiveShadow = true; return m; }
function sphere(r, material, pos = [0, 0, 0], seg = 32) { const m = new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(12, Math.floor(seg / 2))), material); m.position.set(...pos); m.castShadow = true; m.receiveShadow = true; return m; }
function ellipsoid(rx, ry, rz, material, pos = [0, 0, 0], seg = 32) { const m = sphere(1, material, pos, seg); m.scale.set(rx, ry, rz); return m; }
function cone(r, h, material, pos = [0, 0, 0], seg = 32) { const m = new THREE.Mesh(new THREE.ConeGeometry(r, h, seg), material); m.position.set(...pos); m.castShadow = true; m.receiveShadow = true; return m; }
function torus(R, r, material, pos = [0, 0, 0], seg = 48, tube = 10) { const m = new THREE.Mesh(new THREE.TorusGeometry(R, r, tube, seg), material); m.position.set(...pos); m.castShadow = true; m.receiveShadow = true; return m; }
function line(points, color = 0xe5e7eb, width = 1, opacity = 0.85) {
  const geo = new THREE.BufferGeometry().setFromPoints(points);
  const material = new THREE.LineBasicMaterial({ color, linewidth: width, transparent: true, opacity });
  return new THREE.Line(geo, material);
}
function tube(points, radius, material, seg = 48) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => Array.isArray(p) ? new THREE.Vector3(...p) : p));
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, seg, radius, 8, false), material);
  mesh.castShadow = true; mesh.receiveShadow = true;
  return mesh;
}
function cylBetween(a, b, radius, material, seg = 16) {
  const va = Array.isArray(a) ? new THREE.Vector3(...a) : a.clone();
  const vb = Array.isArray(b) ? new THREE.Vector3(...b) : b.clone();
  const mid = va.clone().add(vb).multiplyScalar(0.5);
  const len = va.distanceTo(vb);
  const mesh = cyl(radius, radius, len, material, [mid.x, mid.y, mid.z], seg);
  const dir = vb.clone().sub(va).normalize();
  mesh.quaternion.setFromUnitVectors(Y_AXIS, dir);
  return mesh;
}
function label(group, text, pos, opts = {}) {
  const s = makeLabelSprite(String(text), { scale: opts.scale || 0.22, fontSize: opts.fontSize || 30, bg: opts.bg, color: opts.color });
  s.position.set(...pos); group.add(s); return s;
}
function leader(group, text, from, to, opts = {}) {
  group.add(line([new THREE.Vector3(...from), new THREE.Vector3(...to)], opts.color || 0x93c5fd, 1, 0.75));
  label(group, text, from, { scale: opts.scale || 0.105, fontSize: opts.fontSize || 20, bg: opts.bg || 'rgba(15,23,42,.78)' });
}
function seeded(seed = 1) { let s = Math.abs(Math.floor(seed)) || 1; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
function hashSeed(...items) { return items.join('|').split('').reduce((a, c) => ((a * 31 + c.charCodeAt(0)) >>> 0), 2166136261); }
function addStamp(group, text = 'real-scale virtual model') { label(group, text, [2.8, 2.65, -2.0], { scale: 0.12, fontSize: 20, bg: 'rgba(15,23,42,.62)' }); }
function addDimensionBar(group, text, a, b, y = 0.96) {
  const start = new THREE.Vector3(a, y, -1.45), end = new THREE.Vector3(b, y, -1.45);
  group.add(line([start, end], 0x38bdf8, 1, 0.95));
  group.add(cylBetween([a, y - 0.05, -1.45], [a, y + 0.05, -1.45], 0.006, mat(0x38bdf8), 6));
  group.add(cylBetween([b, y - 0.05, -1.45], [b, y + 0.05, -1.45], 0.006, mat(0x38bdf8), 6));
  label(group, text, [(a + b) / 2, y + 0.16, -1.45], { scale: 0.09, fontSize: 18, bg: 'rgba(15,23,42,.72)' });
}

function addBench(group) {
  const top = box(8.8, 0.28, 5.2, mat(0x243244, { roughness: 0.78 }), [0, 0.55, 0]); group.add(top);
  group.add(box(9.2, 0.16, 5.55, mat(0x5b321c, { roughness: 0.82 }), [0, 0.34, 0]));
  for (let i = -5; i <= 5; i += 1) {
    const a = line([new THREE.Vector3(i * 0.75, 0.705, -2.6), new THREE.Vector3(i * 0.75, 0.705, 2.6)], 0xffffff, 1, 0.045);
    const b = line([new THREE.Vector3(-4.4, 0.707, i * 0.52), new THREE.Vector3(4.4, 0.707, i * 0.52)], 0xffffff, 1, 0.045);
    group.add(a, b);
  }
  label(group, 'NEB Biology 3D practical bench', [-2.95, 0.96, -2.18], { scale: 0.15, fontSize: 24, bg: 'rgba(0,0,0,.58)' });
}
function addTray(group, name = 'specimen tray') {
  group.add(box(4.12, 0.10, 2.35, mat(0xe7edf4, { roughness: 0.66 }), [0, 0.83, 0]));
  group.add(box(4.28, 0.18, 0.12, mat(0x64748b, { roughness: 0.52 }), [0, 0.95, -1.19]));
  group.add(box(4.28, 0.18, 0.12, mat(0x64748b, { roughness: 0.52 }), [0, 0.95, 1.19]));
  group.add(box(0.12, 0.18, 2.36, mat(0x64748b, { roughness: 0.52 }), [-2.14, 0.95, 0]));
  group.add(box(0.12, 0.18, 2.36, mat(0x64748b, { roughness: 0.52 }), [2.14, 0.95, 0]));
  label(group, name, [-1.35, 1.17, -1.07], { scale: 0.125, fontSize: 22, bg: 'rgba(15,23,42,.72)' });
}
function addSlide(group, x = 0, z = 0, tint = 0xfbcfe8) {
  const slide = box(1.95, 0.026, 0.78, glass(0xffffff, 0.32), [x, 1.17, z]);
  group.add(slide);
  group.add(box(0.72, 0.029, 0.50, mat(tint, { opacity: 0.56, roughness: 0.36 }), [x, 1.195, z]));
  group.add(box(0.84, 0.014, 0.60, glass(0xffffff, 0.24), [x, 1.225, z]));
  return slide;
}
function addMicroscope(group, state = {}, opts = {}) {
  const g = new THREE.Group();
  g.position.set(-1.6, 0.72, 0);
  g.add(box(1.55, 0.16, 1.15, metal(0x263241), [0, 0.16, 0]));
  g.add(cyl(0.15, 0.15, 1.55, metal(0x475569), [-0.48, 0.92, 0], 32));
  const arm = tube([[-0.55, 0.58, 0], [-0.40, 1.48, 0], [0.12, 2.15, 0]], 0.075, metal(0x64748b), 32); g.add(arm);
  const tubeBody = cyl(0.16, 0.16, 1.05, metal(0x111827), [0.18, 2.34, 0], 32); tubeBody.rotation.z = -0.34; g.add(tubeBody);
  const eye = cyl(0.22, 0.18, 0.42, metal(0x020617), [0.37, 2.83, 0], 32); eye.rotation.z = -0.34; g.add(eye);
  const nose = cyl(0.27, 0.27, 0.16, metal(0x94a3b8), [0.02, 1.90, 0], 32); nose.rotation.x = Math.PI / 2; g.add(nose);
  for (let i = 0; i < 4; i++) { const a = i / 4 * Math.PI * 2; const obj = cyl(0.052, 0.085, 0.48, metal(0xd7dee8), [0.02 + Math.cos(a) * 0.12, 1.67, Math.sin(a) * 0.20], 24); obj.rotation.x = Math.PI / 2; g.add(obj); }
  g.add(box(1.25, 0.08, 1.0, metal(0x111827), [0.18, 1.05, 0]));
  g.add(box(0.20, 0.02, 0.85, metal(0xcbd5e1), [-0.18, 1.13, 0]));
  addSlide(g, 0.20, 0, opts.tint || 0xf9a8d4);
  g.add(cyl(0.20, 0.16, 0.12, mat(0xfef3c7, { emissive: 0xfacc15, emissiveIntensity: 0.48 }), [0.18, 0.62, 0], 32));
  const knobL = cyl(0.18, 0.18, 0.15, metal(0x94a3b8), [-0.76, 1.25, 0.48], 24); knobL.rotation.x = Math.PI / 2; g.add(knobL);
  const knobR = cyl(0.12, 0.12, 0.14, metal(0x94a3b8), [-0.76, 1.25, -0.48], 24); knobR.rotation.x = Math.PI / 2; g.add(knobR);
  label(g, 'compound microscope', [0.2, 3.25, 0], { scale: 0.14, fontSize: 24 });
  group.add(g); return g;
}

function addMicroscopeBoard(group, title = 'microscope field') {
  const board = box(3.0, 2.0, 0.055, mat(0x020617, { opacity: 0.96 }), [1.88, 2.04, -0.88]); board.rotation.x = -0.04; group.add(board);
  const rim = cyl(0.80, 0.80, 0.035, metal(0xe5e7eb), [1.88, 2.06, -0.82], 96); rim.rotation.x = Math.PI / 2; group.add(rim);
  const field = cyl(0.745, 0.745, 0.038, mat(0xf8d7e8, { roughness: 0.82 }), [1.88, 2.07, -0.785], 96); field.rotation.x = Math.PI / 2; group.add(field);
  label(group, title, [1.88, 3.20, -0.82], { scale: 0.14, fontSize: 22, bg: 'rgba(15,23,42,.72)' });
}
function addPlantTissueField(group, state = {}) {
  addMicroscopeBoard(group, 'palisade / xylem / phloem cells');
  const cx = 1.88, cy = 2.07, z = -0.735;
  const cellWall = mat(0x65a30d, { roughness: 0.8, opacity: 0.78 });
  for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) {
    const x = cx - 0.48 + c * 0.24; const y = cy - 0.36 + r * 0.20;
    const cell = box(0.20, 0.13, 0.012, mat(0xb7e39e, { opacity: 0.72 }), [x, y, z]);
    group.add(cell);
    group.add(box(0.205, 0.012, 0.014, cellWall, [x, y + 0.065, z + 0.004]));
    group.add(box(0.205, 0.012, 0.014, cellWall, [x, y - 0.065, z + 0.004]));
    group.add(box(0.012, 0.13, 0.014, cellWall, [x - 0.102, y, z + 0.004]));
    group.add(box(0.012, 0.13, 0.014, cellWall, [x + 0.102, y, z + 0.004]));
    group.add(sphere(0.018, mat(0x166534), [x + 0.035, y, z + 0.018], 10));
  }
  for (let i = 0; i < 4; i++) { const x = cx - 0.44 + i * 0.29; const v = cyl(0.055, 0.055, 0.86, mat(0x8b5a2b, { roughness: 0.6 }), [x, cy, z + 0.06], 24); v.rotation.z = Math.PI / 2; group.add(v); for (let k = -3; k <= 3; k++) group.add(line([new THREE.Vector3(x - 0.025, cy + k * 0.09, z + 0.10), new THREE.Vector3(x + 0.025, cy + k * 0.09, z + 0.10)], 0xfef3c7, 1, 0.5)); }
  leader(group, 'thick xylem wall', [2.78, 2.55, -0.55], [2.15, 2.27, -0.70]);
  leader(group, 'chloroplasts', [2.80, 1.67, -0.55], [1.98, 1.91, -0.70]);
}
function addMitosisField(group, state = {}, animal = false) {
  addMicroscopeBoard(group, animal ? 'animal mitosis permanent slide' : 'onion root tip mitosis');
  const rand = seeded(hashSeed('mitosis', animal, state.field || 1));
  const phases = ['interphase','prophase','metaphase','anaphase','telophase'];
  const colors = { interphase: 0xb7e4a2, prophase: 0xf59e0b, metaphase: 0x38bdf8, anaphase: 0xf43f5e, telophase: 0xa78bfa };
  for (let i = 0; i < 34; i++) {
    const a = rand() * Math.PI * 2; const r = Math.sqrt(rand()) * 0.62;
    const x = 1.88 + Math.cos(a) * r; const y = 2.07 + Math.sin(a) * r; const p = phases[i % phases.length];
    const cell = ellipsoid(animal ? 0.055 : 0.075, animal ? 0.046 : 0.055, 0.015, mat(animal ? 0xf8b4c4 : 0xf6ffd1, { opacity: 0.82 }), [x, y, -0.723], 18);
    group.add(cell);
    if (p === 'interphase') group.add(sphere(0.020, mat(colors[p]), [x, y, -0.692], 12));
    if (p === 'prophase') for (let k = 0; k < 4; k++) group.add(cylBetween([x - 0.026 + k * 0.016, y - 0.020, -0.690], [x + 0.020 - k * 0.010, y + 0.020, -0.690], 0.004, mat(colors[p]), 6));
    if (p === 'metaphase') { group.add(line([new THREE.Vector3(x - 0.045, y, -0.690), new THREE.Vector3(x + 0.045, y, -0.690)], 0x38bdf8)); for (let k = -1; k <= 1; k++) group.add(box(0.008, 0.055, 0.006, mat(colors[p]), [x + k * 0.014, y, -0.685])); }
    if (p === 'anaphase') { group.add(cone(0.018, 0.045, mat(colors[p]), [x - 0.024, y, -0.686], 8)); group.add(cone(0.018, 0.045, mat(colors[p]), [x + 0.024, y, -0.686], 8)); }
    if (p === 'telophase') { group.add(sphere(0.018, mat(colors[p]), [x - 0.026, y, -0.690], 12)); group.add(sphere(0.018, mat(colors[p]), [x + 0.026, y, -0.690], 12)); }
  }
  ['I','P','M','A','T'].forEach((n, i) => label(group, n, [1.20 + i * 0.34, 1.26, -0.55], { scale: 0.07, fontSize: 16 }));
}
function addStomataField(group, state = {}) {
  addMicroscopeBoard(group, `${state.surface || 'lower'} epidermis: stomata`);
  const rand = seeded(hashSeed('stomata', state.surface || 'lower'));
  for (let i = 0; i < 24; i++) {
    const a = rand() * Math.PI * 2; const r = Math.sqrt(rand()) * 0.62;
    const x = 1.88 + Math.cos(a) * r; const y = 2.07 + Math.sin(a) * r;
    const cell = ellipsoid(0.16 + rand()*0.035, 0.085 + rand()*0.02, 0.010, mat(0xc9f7b2, { opacity: 0.66 }), [x, y, -0.727], 18); cell.rotation.z = rand() * Math.PI; group.add(cell);
  }
  const density = state.surface === 'upper' ? 5 : 11;
  for (let i = 0; i < density; i++) {
    const a = i / density * Math.PI * 2 + 0.2; const r = 0.18 + (i % 3) * 0.16;
    const x = 1.88 + Math.cos(a) * r; const y = 2.07 + Math.sin(a) * r;
    const pair = new THREE.Group(); pair.position.set(x, y, -0.69); pair.rotation.z = a + Math.PI / 2;
    pair.add(ellipsoid(0.028, 0.070, 0.012, organic(0x159447), [-0.035, 0, 0], 16));
    pair.add(ellipsoid(0.028, 0.070, 0.012, organic(0x159447), [0.035, 0, 0], 16));
    pair.add(box(0.018, 0.090, 0.006, mat(0x062e1a), [0, 0, 0.010]));
    group.add(pair);
  }
  leader(group, 'guard cells + pore', [2.82, 2.72, -0.55], [2.10, 2.35, -0.68]);
}
function addPlasmolysisField(group, state = {}) {
  addMicroscopeBoard(group, 'Rhoeo peel plasmolysis');
  const salt = Math.max(0, Number(state.salt || 3));
  const shrink = Math.max(0.35, 1 - salt * 0.08);
  for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) {
    const x = 1.40 + c * 0.24; const y = 1.78 + r * 0.18;
    group.add(box(0.20, 0.13, 0.012, mat(0xd8b4fe, { opacity: 0.50 }), [x, y, -0.724]));
    group.add(box(0.205, 0.012, 0.014, mat(0x7c3aed, { opacity: 0.7 }), [x, y + 0.066, -0.714]));
    group.add(box(0.205, 0.012, 0.014, mat(0x7c3aed, { opacity: 0.7 }), [x, y - 0.066, -0.714]));
    group.add(box(0.012, 0.13, 0.014, mat(0x7c3aed, { opacity: 0.7 }), [x - 0.102, y, -0.714]));
    group.add(box(0.012, 0.13, 0.014, mat(0x7c3aed, { opacity: 0.7 }), [x + 0.102, y, -0.714]));
    group.add(ellipsoid(0.078 * shrink, 0.045 * shrink, 0.012, mat(0xbe185d, { opacity: 0.74 }), [x + 0.015, y, -0.686], 14));
  }
  leader(group, 'protoplast pulled from wall', [2.82, 1.48, -0.54], [2.11, 1.90, -0.68]);
}
function addAnatomyTSField(group, state = {}) {
  addMicroscopeBoard(group, state.section || 'T.S. root/stem');
  const center = [1.88, 2.07, -0.70];
  const sec = String(state.section || 'dicot stem').toLowerCase();
  group.add(cyl(0.61, 0.61, 0.018, mat(0xb7e4a2, { opacity: 0.80 }), center, 80).rotateX?.(Math.PI/2));
  const ring = torus(0.44, 0.025, mat(0x65a30d), center, 72, 8); ring.rotation.x = Math.PI / 2; group.add(ring);
  const bundles = sec.includes('monocot') ? 18 : 10;
  for (let i = 0; i < bundles; i++) {
    const a = i / bundles * Math.PI * 2; const r = sec.includes('root') ? 0.27 : (sec.includes('monocot') ? 0.14 + (i % 3) * 0.11 : 0.42);
    const x = 1.88 + Math.cos(a) * r; const y = 2.07 + Math.sin(a) * r;
    const b = new THREE.Group(); b.position.set(x, y, -0.678); b.rotation.z = a;
    b.add(ellipsoid(0.040, 0.075, 0.012, mat(0xd97706), [0, 0.028, 0], 12));
    b.add(ellipsoid(0.035, 0.060, 0.012, mat(0x15803d), [0, -0.040, 0], 12));
    group.add(b);
  }
  group.add(sphere(0.070, mat(0xfef3c7, { opacity: 0.8 }), [1.88, 2.07, -0.675], 16));
  leader(group, 'vascular bundles', [2.82, 2.38, -0.55], [2.25, 2.20, -0.66]);
}
function addAnimalTissueField(group, state = {}) {
  const tissueName = state.tissue || 'blood smear';
  addMicroscopeBoard(group, tissueName);
  const rand = seeded(hashSeed('animalTissue', tissueName));
  if (String(tissueName).toLowerCase().includes('muscle')) {
    for (let i = 0; i < 9; i++) {
      const y = 1.55 + i * 0.12; group.add(box(1.25, 0.055, 0.012, mat(i % 2 ? 0xfca5a5 : 0xf87171, { opacity: 0.82 }), [1.88, y, -0.70]));
      for (let k = 0; k < 10; k++) group.add(line([new THREE.Vector3(1.28 + k * 0.13, y - 0.027, -0.68), new THREE.Vector3(1.31 + k * 0.13, y + 0.027, -0.68)], 0x7f1d1d, 1, 0.42));
    }
  } else if (String(tissueName).toLowerCase().includes('epithelial')) {
    for (let r = 0; r < 6; r++) for (let c = 0; c < 7; c++) {
      const x = 1.22 + c * 0.20; const y = 1.54 + r * 0.15;
      group.add(ellipsoid(0.084, 0.062, 0.012, mat(0xfbcfe8, { opacity: 0.78 }), [x, y, -0.70], 14));
      group.add(sphere(0.018, mat(0x9333ea), [x, y, -0.675], 10));
    }
  } else {
    for (let i = 0; i < 56; i++) { const a = rand()*Math.PI*2; const r = Math.sqrt(rand())*0.62; const x = 1.88 + Math.cos(a)*r; const y = 2.07 + Math.sin(a)*r; const rb = ellipsoid(0.040, 0.028, 0.006, mat(0xdc2626, { opacity: 0.82 }), [x, y, -0.685], 12); rb.rotation.z = rand()*Math.PI; group.add(rb); }
    for (let i = 0; i < 5; i++) { const a = rand()*Math.PI*2; const r = Math.sqrt(rand())*0.45; group.add(sphere(0.040, mat(0xf3e8ff), [1.88 + Math.cos(a)*r, 2.07 + Math.sin(a)*r, -0.675], 14)); }
  }
}
function addFrogDevField(group, state = {}) {
  addMicroscopeBoard(group, state.stage || 'frog embryo');
  const stage = state.stage || 'cleavage'; const cx = 1.88, cy = 2.07;
  if (stage === 'fertilized egg') { group.add(sphere(0.34, mat(0xfef3c7, { opacity: 0.82 }), [cx, cy, -0.68], 48)); group.add(sphere(0.09, mat(0x92400e), [cx - 0.05, cy + 0.03, -0.62], 24)); }
  else if (stage === 'cleavage') { for (let i = 0; i < 8; i++) { const a = i/8*Math.PI*2; group.add(sphere(0.13, mat(0xfef3c7, { opacity: 0.86 }), [cx + Math.cos(a)*0.18, cy + Math.sin(a)*0.18, -0.65], 24)); } }
  else if (stage === 'blastula') { const shell = torus(0.30, 0.085, mat(0xfef3c7, { opacity: 0.82 }), [cx, cy, -0.66], 72, 16); shell.rotation.x = Math.PI / 2; group.add(shell); group.add(sphere(0.15, glass(0x93c5fd, 0.20), [cx, cy, -0.64], 24)); }
  else { const g = torus(0.31, 0.09, mat(0xfef3c7, { opacity: 0.84 }), [cx, cy, -0.66], 72, 16); g.rotation.x = Math.PI/2; group.add(g); group.add(ellipsoid(0.18, 0.09, 0.03, mat(0x7c2d12), [cx+0.08, cy-0.03, -0.62], 24)); }
  leader(group, 'developmental stage', [2.82, 2.60, -0.55], [2.00, 2.24, -0.62]);
}
function addMicroscopeField(group, kind, state = {}) {
  if (kind === 'microscope') return addPlantTissueField(group, state);
  if (kind === 'mitosis') return addMitosisField(group, state, false);
  if (kind === 'animalMitosis') return addMitosisField(group, state, true);
  if (kind === 'stomata') return addStomataField(group, state);
  if (kind === 'plasmolysis') return addPlasmolysisField(group, state);
  if (kind === 'anatomyTS') return addAnatomyTSField(group, state);
  if (kind === 'frogDev') return addFrogDevField(group, state);
  if (kind === 'animalTissue') return addAnimalTissueField(group, state);
  return addPlantTissueField(group, state);
}

function makePetal(material, pos, angle, scale = 1) { const p = ellipsoid(0.26*scale, 0.055*scale, 0.55*scale, material, pos, 32); p.rotation.y = -angle; p.rotation.z = Math.sin(angle) * 0.08; return p; }
function addFlower(group, state = {}) {
  addTray(group, 'botanical dissection tray');
  const family = state.family || 'Solanaceae';
  const petalColor = family === 'Liliaceae' ? 0xf7f3e8 : family === 'Fabaceae' ? 0xe879a8 : 0x9b5bd5;
  group.add(cyl(0.045, 0.060, 1.25, organic(0x166534), [0, 1.24, 0], 18));
  group.add(sphere(0.18, organic(0x2e7d32), [0, 1.62, 0], 24));
  const petals = family === 'Liliaceae' ? 6 : 5;
  for (let i = 0; i < petals; i++) { const a = i / petals * Math.PI * 2; const p = makePetal(mat(petalColor, { roughness: 0.54 }), [Math.cos(a)*0.48, 1.94, Math.sin(a)*0.48], a, family==='Liliaceae'?1.1:1); p.rotation.x = 0.18; group.add(p); }
  for (let i = 0; i < petals; i++) { const a = i / petals * Math.PI * 2; const s = makePetal(organic(0x2f855a), [Math.cos(a)*0.38, 1.67, Math.sin(a)*0.38], a, 0.62); s.scale.y = 0.045; group.add(s); }
  const stamens = family === 'Liliaceae' ? 6 : family === 'Fabaceae' ? 10 : 5;
  for (let i = 0; i < stamens; i++) { const a = i / stamens * Math.PI * 2; const f = cylBetween([Math.cos(a)*0.14,1.72,Math.sin(a)*0.14], [Math.cos(a)*0.27,2.22,Math.sin(a)*0.27], 0.012, mat(0xfef3c7), 10); group.add(f); group.add(ellipsoid(0.045,0.035,0.070,mat(0xd97706),[Math.cos(a)*0.30,2.25,Math.sin(a)*0.30],16)); }
  group.add(cyl(0.024, 0.030, 0.74, mat(0xfef08a), [0, 2.02, 0], 18)); group.add(sphere(0.055, mat(0xfacc15), [0, 2.43, 0], 18)); group.add(ellipsoid(0.13,0.16,0.13,organic(0x65a30d),[0,1.70,0],24));
  const section = new THREE.Group(); section.position.set(1.33,1.30,0.45); section.scale.setScalar(0.85); section.add(ellipsoid(0.26,0.10,0.26,organic(0x65a30d),[0,0,0],24)); section.add(cyl(0.20,0.20,0.025,mat(0xfef3c7),[0,0.08,0],32)); for(let i=0;i<(family==='Fabaceae'?1:family==='Liliaceae'?3:2);i++){ const a=i*Math.PI*2/(family==='Fabaceae'?1:family==='Liliaceae'?3:2); section.add(sphere(0.035,mat(0xf59e0b),[Math.cos(a)*0.08,0.105,Math.sin(a)*0.08],12)); } group.add(section);
  leader(group, 'stigma', [0.86,2.68,0.35], [0,2.43,0]); leader(group, 'anther', [-1.1,2.42,0.48], [-0.30,2.25,0.02]); leader(group, 'ovary T.S.', [1.85,1.78,0.95], [1.33,1.38,0.45]);
  label(group, `${family}: realistic floral whorls`, [0, 2.92, 0], { scale: 0.16, fontSize: 24 });
}
function addInflorescence(group, state = {}) {
  addTray(group, 'inflorescence morphology');
  const type = state.type || 'raceme';
  const stem = organic(0x166534); group.add(cyl(0.030,0.040,2.0,stem,[0,1.78,0],16));
  const flowerMat = mat(0xf472b6,{roughness:0.58}); const count = type === 'capitulum' ? 34 : 12;
  for(let i=0;i<count;i++){
    let x=0,y=1.05+i*.13,z=0, base=[0,y,0];
    if(type==='umbel'){const a=i/count*Math.PI*2; x=Math.cos(a)*.86; z=Math.sin(a)*.86; y=2.45; base=[0,1.62,0]; group.add(cylBetween(base,[x,y,z],.008,stem,8));}
    else if(type==='capitulum'){const a=i/count*Math.PI*2; const r=.10+(i%6)*.055; x=Math.cos(a)*r; z=Math.sin(a)*r; y=2.36+(i%2)*.02;}
    else if(type==='spike'){x=.12*(i%2?1:-1); y=1.02+i*.13;}
    else if(type==='cyme'){x=(i-5.5)*.15; y=2.42-Math.abs(i-5.5)*.06; z=(i%2-.5)*.48; group.add(cylBetween([0,1.72,0],[x,y,z],.009,stem,8));}
    else {x=(i%2?.38:-.38); y=1.10+i*.13; group.add(cylBetween([0,y,0],[x,y+.06,z],.009,stem,8));}
    for(let p=0;p<5;p++){const a=p/5*Math.PI*2; const pet=ellipsoid(.035,.014,.070,flowerMat,[x+Math.cos(a)*.035,y,z+Math.sin(a)*.035],12); pet.rotation.y=-a; group.add(pet);}
  }
  label(group, `${type}: ${type === 'cyme' ? 'cymose' : 'racemose'} pattern`, [0, 2.95, 0], { scale: 0.16 });
}
function addHerbarium(group, state = {}) {
  group.add(box(3.2, 0.035, 4.35, mat(0xf8fafc), [0, 0.89, 0]));
  group.add(box(1.18, 0.035, 0.64, mat(0xe2e8f0), [0.86, 0.94, 1.56]));
  group.add(box(0.42,0.012,0.075,mat(0xfde68a,{opacity:.78}),[-0.38,1.01,-0.72])); group.add(box(0.45,0.012,0.075,mat(0xfde68a,{opacity:.78}),[0.24,1.01,0.54]));
  const stemPts=[[-.35,1.00,-1.25],[-.15,1.02,-.50],[.05,1.02,.25],[.22,1.02,1.02]]; group.add(tube(stemPts,.012,organic(0x31572c),24));
  for(let i=0;i<12;i++){const a=-1.1+i*.20; const side=i%2?1:-1; const leaf=ellipsoid(.10,.012,.26,organic(0x3f6212),[-.10+side*.20,1.035,-1.05+i*.18],18); leaf.rotation.y=side*.85; leaf.rotation.z=a*.18; group.add(leaf);}
  label(group, 'species, date, locality, collector', [0.88,1.14,1.58], { scale:.09, fontSize:17, bg:'rgba(226,232,240,.88)', color:'#0f172a' });
  label(group, `pressed/dried: ${state.dryness || 82}%`, [-0.65, 1.35, -1.62], { scale: 0.14 });
}
function addMushroom(group, state = {}) {
  addTray(group, 'mushroom identification key');
  for (let i = 0; i < 4; i++) {
    const x = -1.25 + i * 0.82; const h = 0.45 + i * 0.10; const poisonous = i === 2 && state.volva === 'yes';
    group.add(cyl(0.075, 0.12, h, mat(0xf5e7c8), [x, 1.06 + h/2, 0], 24));
    const cap = ellipsoid(0.33, 0.16, 0.33, mat(poisonous ? 0xef4444 : 0x9a5b2f, { roughness: 0.74 }), [x, 1.38+h, 0], 32); group.add(cap);
    for(let g=0; g<12; g++){ const a=g/12*Math.PI*2; const rib = cylBetween([x,1.31+h,0],[x+Math.cos(a)*.26,1.32+h,Math.sin(a)*.26],.004,mat(0xffedd5),6); group.add(rib); }
    if(i===1 || poisonous) group.add(torus(.14,.012,mat(0xfff7ed),[x,1.19+h*.55,0],32,6));
    if(poisonous) group.add(cyl(.20,.28,.13,mat(0xf8fafc),[x,1.02,0],24));
  }
  group.add(box(1.25,.025,.70,mat({ white:0xf8fafc,brown:0x8b5a2b,black:0x111827,pink:0xf9a8d4 }[state.sporePrint]||0x8b5a2b),[1.30,1.01,.58]));
  label(group, `spore print: ${state.sporePrint || 'brown'} | volva: ${state.volva || 'no'}`, [0, 2.72, 0], { scale: 0.15 });
}
function addCulture(group, state = {}) {
  addTray(group, 'sterile soil culture plate');
  const plate = cyl(0.88, 0.88, 0.12, glass(0xffffff, 0.34), [0, 1.08, 0], 72); group.add(plate);
  group.add(cyl(0.80, 0.80, 0.030, mat(0xfef3c7, { opacity: 0.76 }), [0, 1.15, 0], 72));
  const rand=seeded(hashSeed('culture',state.colonies||54,state.dilution||3)); const colonies=Math.min(88,Math.max(8,state.colonies||54));
  for(let i=0;i<colonies;i++){ const a=rand()*Math.PI*2; const r=Math.sqrt(rand())*.70; const c=[0xfde68a,0xfca5a5,0xd9f99d,0xf8fafc,0xe0e7ff][i%5]; group.add(ellipsoid(.020+rand()*.032,.009+rand()*.010,.020+rand()*.032,mat(c),[Math.cos(a)*r,1.195,Math.sin(a)*r],10)); }
  group.add(cyl(.010,.010,1.25,metal(0x94a3b8),[-1.15,1.65,.75],8)); group.add(sphere(.035,mat(0xfef3c7,{emissive:0xf59e0b,emissiveIntensity:.6}),[-1.15,2.33,.75],10));
  label(group, `${colonies} colonies on dilution 10^-${state.dilution || 3}`, [0, 2.30, 0], { scale: 0.15 });
}
function addPond(group, state = {}, zoo = false) {
  const dish = cyl(1.78, 1.78, 0.22, mat(0x334155), [0, .91, 0], 72); group.add(dish);
  group.add(cyl(1.66, 1.66, .045, mat(0x0ea5e9, { opacity: .68, roughness: .18 }), [0, 1.08, 0], 72));
  const rand=seeded(hashSeed('pond',zoo,state.pH||7.2,state.oxygen||6.8));
  for(let i=0;i<22;i++){ const a=rand()*Math.PI*2; const r=Math.sqrt(rand())*1.45; const h=.25+rand()*.55; const p=cyl(.012,.030,h,organic(0x15803d),[Math.cos(a)*r,1.12+h/2,Math.sin(a)*r],8); p.rotation.z=(rand()-.5)*.4; group.add(p); if(rand()>.45){const leaf=ellipsoid(.11,.015,.045,organic(0x22c55e),[Math.cos(a)*r+.07,1.14+h,Math.sin(a)*r],12); group.add(leaf);} }
  const fishCount=zoo?8:3; for(let i=0;i<fishCount;i++){ const x=(rand()-.5)*2.4,z=(rand()-.5)*2.2; const fish=ellipsoid(.13,.04,.06,mat(i%2?0xf97316:0x38bdf8),[x,1.19,z],16); fish.rotation.y=rand()*Math.PI*2; group.add(fish); group.add(cone(.055,.10,fish.material,[x-.12,1.19,z],12)); }
  group.add(cyl(.018,.018,1.05,glass(0xffffff,.36),[1.55,1.58,-.86],16)); for(let t=0;t<5;t++) group.add(line([new THREE.Vector3(1.50,1.15+t*.17,-.86),new THREE.Vector3(1.60,1.15+t*.17,-.86)],0xe0f2fe,1,.8));
  label(group, zoo ? `DO ${state.oxygen || 6.8} mg/L | zooplankton/fish` : `pH ${state.pH || 7.2}, turbidity ${state.turbidity || 32} NTU`, [0, 2.40, 0], { scale: 0.16 });
}
function addQuadrat(group, state = {}, frequency = false) {
  group.add(box(4.8,.07,3.2,organic(0x365314),[0,.82,0]));
  for(let i=-2;i<=2;i++) group.add(cylBetween([i*.72,.93,-1.55],[i*.72,.93,1.55],.006,mat(0xf8fafc),6));
  for(let j=-2;j<=2;j++) group.add(cylBetween([-1.8,.94,j*.72],[1.8,.94,j*.72],.006,mat(0xf8fafc),6));
  const rand=seeded(hashSeed('quadrat',frequency,state.plants||22,state.hits||7)); const plants=frequency?(state.hits||7)*4:(state.plants||22);
  for(let i=0;i<plants;i++){ const x=(rand()-.5)*3.5,z=(rand()-.5)*2.9,h=.18+rand()*.26; group.add(cyl(.010,.014,h,organic(0x22c55e),[x,1.01+h/2,z],8)); group.add(ellipsoid(.065,.018,.045,organic(0x84cc16),[x+.035,1.04+h,z],10)); group.add(ellipsoid(.060,.018,.043,organic(0x16a34a),[x-.035,1.00+h,z],10)); }
  label(group, frequency ? `frequency ${Math.round((state.hits || 7)/(state.total || 10)*100)}%` : `density ${((state.plants || 22)/(state.area || 1)).toFixed(1)} plants/m2`, [0, 2.04, 0], { scale: .16 });
}
function addSoil(group, state = {}) {
  addTray(group, 'soil texture / moisture station'); const colors=[0xc68b59,0x7c4a24,0x5c3318];
  for(let i=0;i<3;i++){ const x=-1+i; group.add(cyl(.38,.32,.42,glass(0xffffff,.25),[x,1.12,0],32)); group.add(cyl(.33,.29,.25,mat(colors[i]),[x,1.13,0],32)); for(let g=0;g<18;g++){const rr=seeded(i*200+g)(); group.add(sphere(.010+rr*.020,mat(colors[i]),[x+(seeded(g)()-.5)*.55,1.28,(seeded(g+4)()-.5)*.45],8));} label(group,['sandy','loamy','clayey'][i],[x,1.74,0],{scale:.09,fontSize:18}); }
  group.add(box(.85,.04,.46,mat(0xe5e7eb),[1.38,1.06,.75])); group.add(cyl(.012,.012,.55,mat(0xef4444),[1.68,1.35,.75],8));
  const moisture=((state.wetMass-state.dryMass)/state.dryMass*100)||29; label(group, `moisture ${moisture.toFixed(1)}% | pH comparison`, [0,2.18,0], { scale:.15 });
}
function addSpecimens(group, state = {}) {
  addTray(group, 'vegetation specimen shelf'); const names=['Bacteria','Spirogyra','Moss','Fern','Pine','Lichen'];
  names.forEach((n,i)=>{ const x=-1.55+i*.62; group.add(cyl(.22,.22,.72,glass(0xdbeafe,.30),[x,1.25,0],28)); group.add(cyl(.23,.23,.035,metal(0x64748b),[x,1.62,0],28)); if(n==='Spirogyra'){ for(let k=0;k<4;k++) group.add(tube([[x-.12,1.18,-.05+k*.03],[x,1.28,.02+k*.03],[x+.12,1.21,-.03+k*.03]],.006,organic(0x16a34a),16)); } else if(n==='Fern'){ for(let k=0;k<5;k++) group.add(ellipsoid(.035,.010,.12,organic(0x15803d),[x+(k-2)*.035,1.25+k*.04,0],8)); } else group.add(sphere(.12,organic(i%2?0x16a34a:0x84cc16),[x,1.25,0],16)); label(group,n,[x,1.88,0],{scale:.07,fontSize:16}); });
  label(group, `selected: ${state.specimen || 'Spirogyra'} | diagnostic characters shown`, [0,2.46,0], { scale:.145 });
}
function addFossil(group, state={}) {
  addTray(group, 'Saligram / ammonite fossil'); const shell=new THREE.Group();
  for(let i=0;i<18;i++){ const r=.06+i*.033; const a=i*.62; const chamber=ellipsoid(.055+i*.006,.028,.048+i*.004,mat(i%2?0x57534e:0x78716c),[Math.cos(a)*r,0,Math.sin(a)*r],16); shell.add(chamber); if(i>0) shell.add(cylBetween([Math.cos((i-1)*.62)*(.06+(i-1)*.033),0,Math.sin((i-1)*.62)*(.06+(i-1)*.033)],[Math.cos(a)*r,0,Math.sin(a)*r],.009,mat(0x44403c),8)); }
  shell.position.set(0,1.16,0); shell.scale.set(1.65,.20,1.65); group.add(shell); group.add(cyl(.82,.82,.025,mat(0x1f2937),[0,1.02,0],64));
  label(group, `visible fossil chambers: ${state.chambers || 9}`, [0,2.08,0], { scale:.155 });
}

function addEarthworm(group, pos=[0,1.2,0], scale=1, dissect=false) {
  const g=new THREE.Group(); g.position.set(...pos); g.scale.setScalar(scale); const bodyMat=tissue(0x8e1236);
  for(let i=0;i<26;i++){ const x=-1.15+i*.092; const seg=ellipsoid(.075,.050,.060,bodyMat,[x,0,0],16); seg.scale.x=1.25; g.add(seg); if(i%3===0) g.add(torus(.065,.004,mat(0x5f0f2a,{opacity:.6}),[x,0,0],16,4).rotateY?.(Math.PI/2)); }
  g.add(sphere(.045,mat(0x1f2937),[-1.24,.012,0],10));
  if(dissect){ g.add(box(1.78,.012,.030,mat(0xf8d7da),[-.05,.063,0])); g.add(tube([[-1.16,.09,0],[-.90,.12,0],[-.70,.08,0],[-.48,.12,0],[-.25,.08,0],[.72,.10,0],[1.14,.08,0]],.016,mat(0xfde68a),36)); }
  group.add(g); return g;
}
function addFrog(group,pos=[0,1.35,0],scale=1, dissect=false){ const g=new THREE.Group(); g.position.set(...pos); g.scale.setScalar(scale); const skin=mat(0x2f9e44,{roughness:.72}); g.add(ellipsoid(.45,.18,.32,skin,[0,0,0],32)); g.add(ellipsoid(.24,.16,.22,skin,[-.47,.08,0],24)); for(let side of [-1,1]){ g.add(cylBetween([-.12,-.06,side*.22],[.34,-.22,side*.44],.035,skin,12)); g.add(cylBetween([.34,-.22,side*.44],[.76,-.40,side*.68],.030,skin,12)); g.add(cylBetween([-.35,-.02,side*.18],[-.68,-.22,side*.38],.024,skin,12)); } g.add(sphere(.045,mat(0x020617),[-.58,.16,.12],10)); g.add(sphere(.045,mat(0x020617),[-.58,.16,-.12],10)); if(dissect){ g.add(ellipsoid(.28,.040,.20,mat(0xf8d7da),[.04,.20,0],24)); g.add(sphere(.08,tissue(0xb91c1c),[-.08,.25,0],16)); g.add(tube([[.10,.24,.02],[.22,.25,.08],[.20,.25,-.08],[.00,.25,-.05]],.018,mat(0xd97706),20)); } group.add(g); return g; }
function addRabbit(group,pos=[0,1.35,0],scale=1,dissect=false){ const g=new THREE.Group(); g.position.set(...pos); g.scale.setScalar(scale); const fur=mat(0xd6d3d1,{roughness:.92}); g.add(ellipsoid(.62,.24,.32,fur,[.05,0,0],32)); g.add(ellipsoid(.24,.18,.18,fur,[-.55,.12,0],24)); g.add(ellipsoid(.055,.24,.040,fur,[-.65,.38,.08],12)); g.add(ellipsoid(.055,.24,.040,fur,[-.65,.38,-.08],12)); for(let side of [-1,1]){g.add(cylBetween([-.18,-.10,side*.16],[-.44,-.44,side*.24],.035,fur,12)); g.add(cylBetween([.28,-.10,side*.16],[.52,-.45,side*.25],.038,fur,12));} if(dissect){ g.add(ellipsoid(.38,.05,.20,mat(0xf8d7da),[.07,.22,0],24)); g.add(sphere(.08,tissue(0xb91c1c),[-.12,.27,0],16)); g.add(tube([[.02,.27,0],[.18,.29,.08],[.32,.26,-.05],[.12,.25,-.10]],.020,mat(0xc2410c),24)); } group.add(g); return g; }
function addCockroachLike(group,pos=[0,1.2,0],scale=1,color=0x7c2d12){ const g=new THREE.Group(); g.position.set(...pos); g.scale.setScalar(scale); const body=mat(color,{roughness:.72}); g.add(ellipsoid(.28,.10,.20,body,[-.43,.02,0],24)); g.add(ellipsoid(.34,.12,.25,body,[-.08,0,0],32)); g.add(ellipsoid(.58,.13,.30,body,[.45,0,0],40)); g.add(ellipsoid(.52,.012,.26,mat(0xbf8f5a,{opacity:.55,roughness:.42}),[.42,.12,.12],24)); g.add(ellipsoid(.52,.012,.26,mat(0xbf8f5a,{opacity:.55,roughness:.42}),[.42,.12,-.12],24)); for(let i=0;i<3;i++){[-1,1].forEach(side=>{const x=-.25+i*.28; group.add(cylBetween([pos[0]+(x)*scale,pos[1],pos[2]+side*.18*scale],[pos[0]+(x+.15)*scale,pos[1]-.10*scale,pos[2]+side*.54*scale],.010*scale,mat(0x111827),6)); group.add(cylBetween([pos[0]+(x+.15)*scale,pos[1]-.10*scale,pos[2]+side*.54*scale],[pos[0]+(x+.42)*scale,pos[1]+.02*scale,pos[2]+side*.78*scale],.008*scale,mat(0x111827),6));});}
  g.add(cylBetween([-.62,.07,.08],[-1.15,.25,.43],.006,mat(0x111827),6)); g.add(cylBetween([-.62,.07,-.08],[-1.15,.25,-.43],.006,mat(0x111827),6)); group.add(g); return g; }
function addAnimals(group, state={}) {
  addTray(group, 'animal specimen identification'); const animal=state.animal || 'Earthworm';
  if(animal==='Earthworm'||animal==='Leech'||animal==='Ascaris') addEarthworm(group,[0,1.30,0], animal==='Ascaris'?1.05:.95, false);
  else if(animal==='Honeybee') { addCockroachLike(group,[0,1.35,0],.75,0xf59e0b); for(let s of [-1,1]) group.add(ellipsoid(.34,.012,.18,glass(0xe0f2fe,.36),[-.1,1.53,s*.30],24)); }
  else if(animal==='Prawn') { addCockroachLike(group,[0,1.35,0],.9,0xf97316); group.add(tube([[-.72,1.40,.10],[-1.1,1.62,.35]],.007,mat(0xfef3c7),16)); group.add(tube([[-.72,1.40,-.10],[-1.1,1.62,-.35]],.007,mat(0xfef3c7),16)); }
  else if(animal==='Frog') addFrog(group,[0,1.35,0],1.25,false); else if(animal==='Rabbit') addRabbit(group,[0,1.35,0],1.15,false); else addFrog(group,[0,1.35,0],1.1,false);
  label(group, `identify: ${animal} | visible diagnostic characters`, [0,2.56,0], { scale:.15 });
}
function addDissection(group, state={}) {
  addTray(group, 'scientific dissection model'); const model=state.model || 'Earthworm'; const opened=(state.opened||70)/100;
  if(model==='Frog') addFrog(group,[0,1.40,0],1.45,true); else if(model==='Rabbit') addRabbit(group,[0,1.38,0],1.25,true); else addEarthworm(group,[0,1.33,0],1.25,true);
  const labels = model === 'Earthworm' ? [['mouth',[-1.20,1.80,-.55],[-1.32,1.42,0]],['pharynx',[-.75,1.96,.52],[-.82,1.45,0]],['crop',[-.35,1.84,-.55],[-.42,1.45,0]],['gizzard',[.10,1.96,.52],[.02,1.45,0]],['intestine',[.78,1.84,-.55],[.55,1.43,0]],['anus',[1.40,1.92,.50],[1.28,1.40,0]]] : [['heart',[-.60,2.06,-.58],[-.12,1.65,0]],['lungs',[.10,2.06,.58],[.10,1.65,.06]],['liver',[.74,1.86,-.58],[.20,1.58,-.02]],['stomach',[1.12,1.78,.52],[.36,1.55,.08]]];
  labels.forEach(([n, from, to]) => leader(group, n, from, to, { scale:.085, fontSize:17 })); addDimensionBar(group, `${model} opened ${(opened*100).toFixed(0)}%`, -1.45*opened, 1.45*opened, .98);
  label(group, `${model} alimentary canal - anatomically labelled`, [0,2.50,0], { scale:.15 });
}
function addConservation(group,state={}) { group.add(box(4.8,.08,3.2,organic(0x14532d),[0,.82,0])); const rand=seeded(hashSeed('forest',state.habitat||62)); for(let i=0;i<34;i++){ const x=(rand()-.5)*4.2,z=(rand()-.5)*2.8,h=.28+rand()*.45; group.add(cyl(.018,.045,h,organic(0x4a2e18),[x,1.00+h/2,z],8)); group.add(cone(.12+rand()*.08,.34,organic(0x166534),[x,1.20+h,z],10)); } group.add(box(.70,.10,1.18,mat(0x94a3b8),[-1.65,.96,0])); group.add(box(.18,.12,3.05,mat(0xfacc15),[0,.98,0])); group.add(tube([[-1.7,1.03,-.75],[-.55,1.05,-.15],[.75,1.04,.32],[1.72,1.05,.78]],.035,organic(0x84cc16),36)); label(group,`habitat ${state.habitat||62}% / corridor ${state.corridor||45}%`,[0,2.22,0],{scale:.15}); }
function addOsmosis(group,state={}) { addTray(group,'potato osmometer with capillary scale'); const potato=ellipsoid(.72,.33,.55,mat(0xb45309,{roughness:.8}),[0,1.17,0],40); group.add(potato); group.add(cyl(.25,.29,.42,glass(0xfef3c7,.32),[0,1.45,0],32)); const rise=((state.sucrose||20)*(state.time||45)/1200); group.add(cyl(.045,.045,1.28,glass(0xffffff,.35),[0,2.02,0],20)); group.add(cyl(.036,.036,.20+rise,mat(0x38bdf8,{opacity:.68}),[0,1.42+(.20+rise)/2,0],20)); for(let i=0;i<8;i++) group.add(line([new THREE.Vector3(.08,1.46+i*.13,0),new THREE.Vector3(.20,1.46+i*.13,0)],0x0f172a,1,.8)); label(group,`liquid rise ${rise.toFixed(2)} cm`,[0,2.72,0],{scale:.15}); }
function addPhysiology(group,state={},kind='respiration') { addTray(group, kind); if(kind==='transpiration'||kind==='suction'){ group.add(cyl(.030,.040,1.45,organic(0x166534),[-.55,1.45,0],12)); for(let i=0;i<10;i++){ const y=1.25+i*.09; const side=i%2?1:-1; const leaf=ellipsoid(.19,.025,.08,organic(0x22c55e),[-.55+side*.18,y,side*.10],16); leaf.rotation.z=side*.55; group.add(leaf); } group.add(cylBetween([-.10,1.02,0],[1.40,1.02,0],.018,glass(0xdbeafe,.35),16)); const move=kind==='suction'?((state.leafArea||60)*(state.minutes||30)/1000):(.60/(state.time||75)); group.add(cyl(.030,.030,.08,mat(0x38bdf8),[.25+move*.22,1.02,0],16)); for(let i=0;i<8;i++) group.add(line([new THREE.Vector3(.0+i*.18,1.12,0),new THREE.Vector3(.0+i*.18,1.20,0)],0x38bdf8,1,.65)); }
  else if(kind==='respiration'||kind==='anaerobic'){ const flask=cyl(.50,.36,.90,glass(0xdbeafe,.28),[-.70,1.24,0],48); group.add(flask); group.add(cyl(.36,.32,.26,mat(kind==='anaerobic'?0xfde68a:0x92400e,{opacity:.65}),[-.70,1.02,0],48)); for(let i=0;i<8;i++) group.add(sphere(.045,mat(0x7c2d12),[-.85+(i%4)*.10,1.18+Math.floor(i/4)*.06,(i%2-.5)*.10],10)); group.add(tube([[-.35,1.65,0],[.45,1.90,0],[1.18,1.32,0]],.025,glass(0xdbeafe,.35),32)); const tubeA=cyl(.28,.28,.62,glass(0xdbeafe,.28),[1.25,1.17,0],32); group.add(tubeA); group.add(cyl(.22,.22,.18,mat(0x38bdf8,{opacity:.58}),[1.25,.98,0],32)); if(kind==='anaerobic') for(let i=0;i<6;i++) group.add(sphere(.025,glass(0xffffff,.45),[1.12+i*.04,1.15+i*.08,0],10)); }
  else if(kind==='phototropism'){ group.add(box(2.9,.12,1.3,mat(0x78350f),[0,.90,0])); const curve=Math.min(.72,((state.light||70)*(state.hours||36)/900)); for(let i=0;i<7;i++){ const x=-1.15+i*.38; group.add(tube([[x,1.00,0],[x+.08+curve*.35,1.35,0],[x+.18+curve*.55,1.78,0]],.018,organic(0x22c55e),24)); group.add(ellipsoid(.09,.025,.05,organic(0x84cc16),[x+.20+curve*.55,1.82,0],12)); } group.add(sphere(.26,mat(0xfacc15,{emissive:0xfacc15,emissiveIntensity:.72}),[2.0,2.25,0],32)); group.add(line([new THREE.Vector3(1.75,2.05,0),new THREE.Vector3(.90,1.70,0)],0xfef08a,1,.55)); }
  else if(kind==='apicalBud'){ for(let i=0;i<2;i++){ const x=-.65+i*1.3; group.add(cyl(.025,.035,1.18,organic(0x166534),[x,1.45,0],10)); for(let b=0;b<5;b++){ const dx=i?-.32:.32; group.add(cylBetween([x,1.12+b*.16,0],[x+dx,1.18+b*.18,.10],.012,organic(0x22c55e),8)); group.add(ellipsoid(.08,.018,.045,organic(0x84cc16),[x+dx,1.18+b*.18,.10],10)); } if(i===0) group.add(sphere(.075,organic(0x84cc16),[x,2.08,0],12)); else group.add(box(.22,.022,.022,mat(0xef4444),[x,2.07,0])); label(group,i===0?'intact':'apex removed',[x,2.32,0],{scale:.09,fontSize:18}); } }
  label(group, physiologyLabel(kind,state), [0,2.70,0], { scale:.15 }); }
function physiologyLabel(kind,state){ if(kind==='transpiration')return `${state.surface||'lower'} surface: ${(60/(state.time||75)).toFixed(2)} units/min`; if(kind==='suction')return `water column movement ${(((state.leafArea||60)*(state.minutes||30))/1000).toFixed(2)} cm`; if(kind==='respiration')return `rate ${((state.movement||18)/(state.mass||20)).toFixed(2)} mm/g`; if(kind==='anaerobic')return `CO2 bubbling: ${Math.round((state.yeast||70)*(state.time||25)/100)} units`; if(kind==='phototropism')return `curvature ${Math.min(70,((state.light||70)*(state.hours||36)/90)).toFixed(0)} deg`; if(kind==='apicalBud')return `lateral growth ${(((100-(state.auxin||35))*(state.days||10))/100).toFixed(1)} cm`; return 'plant physiology setup'; }
function addGenetics(group,state={}){ addTray(group,'Mendelian seed tray'); const dom=state.dominant||90, rec=state.recessive||32, total=Math.min(dom+rec,150); for(let i=0;i<total;i++){ const row=Math.floor(i/15), col=i%15; const color=i<dom?0xfacc15:0x16a34a; const seed=ellipsoid(.055,.035,.045,mat(color,{roughness:.78}),[-1.6+col*.23,1.05,-.88+row*.18],12); seed.rotation.y=(i%7)*.4; group.add(seed); } label(group,`observed ratio ${(dom/Math.max(rec,1)).toFixed(2)}:1`,[0,2.25,0],{scale:.15}); }
function addImbibition(group,state={}){ addTray(group,'imbibition in seeds/raisins'); const init=state.initial||20, fin=state.final||32; for(let i=0;i<18;i++){ const swollen=i<9; const s=ellipsoid(swollen?.12:.08,swollen?.08:.052,swollen?.09:.06,mat(0x6b3a1e,{roughness:.92}),[-1.15+(i%9)*.29,1.08,swollen?.38:-.38],16); group.add(s); } group.add(cyl(.38,.38,.34,glass(0xdbeafe,.24),[1.45,1.13,0],32)); group.add(cyl(.34,.34,.18,mat(0x38bdf8,{opacity:.48}),[1.45,1.04,0],32)); label(group,`water uptake ${(((fin-init)/init)*100).toFixed(1)}%`,[0,2.08,0],{scale:.15}); }
function addBiofertilizer(group,state={}){ addTray(group,'biofertilizer carrier culture'); const bag=box(1.25,.72,1.0,mat(0x78350f,{opacity:.76,roughness:.88}),[-.40,1.24,0]); group.add(bag); const rand=seeded(hashSeed('biofertilizer',state.days||7)); for(let i=0;i<46;i++) group.add(sphere(.018+rand()*.020,organic(i%2?0x16a34a:0x84cc16),[-.9+rand()*1.0,1.63+rand()*.10,(rand()-.5)*.70],8)); ['Rhizobium','Azotobacter'].forEach((n,i)=>{const x=.98+i*.44; group.add(cyl(.14,.14,.62,glass(0xdbeafe,.30),[x,1.28,0],20)); label(group,n,[x,1.78,0],{scale:.065,fontSize:15});}); label(group,`moisture ${state.moisture||45}% / day ${state.days||7}`,[0,2.25,0],{scale:.145}); }
function addFrogDev(group,state={}){ addMicroscope(group,state,{tint:0xfde68a}); addMicroscopeField(group,'frogDev',state); }
function addBiochemical(group,state={},kind='starchTest'){ addTray(group,kind); const samples=['control','sample','reagent']; samples.forEach((n,i)=>{ const x=-.82+i*.82; const positive=biochemPositive(kind,state); const color=i===1?(positive?biochemColor(kind,state):0x93c5fd):i===2?0xfacc15:0xe0f2fe; const tubeM=glass(0xdbeafe,.28); group.add(cyl(.18,.15,.96,tubeM,[x,1.25,0],32)); group.add(cyl(.13,.12,.42,mat(color,{opacity:.72}),[x,1.04,0],32)); group.add(cyl(.16,.16,.025,metal(0x94a3b8),[x,1.75,0],24)); label(group,n,[x,1.98,0],{scale:.08,fontSize:16}); }); if(kind==='starchTest') group.add(sphere(.16,mat(0xb45309),[1.35,1.12,.55],16)); if(kind==='proteinTest') group.add(cyl(.22,.22,.32,glass(0xffffff,.28),[1.35,1.14,.55],24)); label(group,biochemLabel(kind,state),[0,2.48,0],{scale:.145}); }
function biochemPositive(kind,state){ if(kind==='starchTest')return ['potato','rice water'].includes(state.sample); if(kind==='proteinTest')return ['egg albumin','milk'].includes(state.sample); if(kind==='urine')return (state.intensity||0)>20; if(kind==='amylase')return true; return true; }
function biochemColor(kind,state){ if(kind==='starchTest')return 0x111827; if(kind==='proteinTest')return 0x7c3aed; if(kind==='urine')return {urea:0xfacc15,sugar:0xb45309,albumin:0xf8fafc,'bile salts':0x22c55e}[state.test]||0xb45309; if(kind==='amylase') return 0xf59e0b; return 0xf97316; }
function biochemLabel(kind,state){ if(kind==='starchTest')return `${state.sample||'sample'}: ${biochemPositive(kind,state)?'blue-black positive':'brown negative'}`; if(kind==='proteinTest')return `${state.sample||'sample'}: ${biochemPositive(kind,state)?'violet positive':'blue negative'}`; if(kind==='urine')return `${state.test||'sugar'} test intensity ${state.intensity||55}%`; return 'biochemical test'; }
function addAmylase(group,state={}){ addTray(group,'salivary amylase water bath'); const temp=state.temperature||37, pH=state.pH||7; const activity=Math.max(0,100-Math.abs(temp-37)*3-Math.abs(pH-7)*18); group.add(box(2.2,.42,1.1,glass(0xdbeafe,.26),[0,1.12,0])); group.add(box(2.0,.20,.92,mat(0x38bdf8,{opacity:.42}),[0,1.03,0])); for(let i=0;i<4;i++){ const x=-.75+i*.50; group.add(cyl(.12,.10,.62,glass(0xdbeafe,.3),[x,1.42,0],20)); group.add(cyl(.09,.08,.30,mat(i<activity/25?0xf59e0b:0x111827,{opacity:.72}),[x,1.24,0],20)); } label(group,`amylase activity ${activity.toFixed(0)}% at ${temp} C / pH ${pH}`,[0,2.35,0],{scale:.145}); }
function addBloodSugar(group,state={}){ addTray(group,'blood glucose meter'); const g=state.glucose||96; group.add(box(1.05,.16,.70,mat(0x111827,{roughness:.42}),[-.35,1.12,0])); group.add(box(.62,.035,.32,mat(0xdbeafe,{emissive:0x38bdf8,emissiveIntensity:.35}),[-.35,1.23,0])); label(group,`${g} mg/dL`,[-.35,1.55,0],{scale:.13,bg:'rgba(219,234,254,.82)',color:'#0f172a'}); group.add(box(1.35,.035,.18,mat(0xf8fafc),[.75,1.10,0])); const color=g<70?0x60a5fa:g<140?0x22c55e:g<200?0xf97316:0xef4444; group.add(box(.35,.04,.14,mat(color),[1.28,1.14,0])); group.add(sphere(.07,tissue(0xb91c1c),[1.58,1.20,0],16)); label(group,`range: ${g<70?'low':g<140?'normal/random acceptable':g<200?'elevated':'high'}`,[0,2.03,0],{scale:.15}); }

function makeBone(length, radius) { const g=new THREE.Group(); g.add(cyl(radius,radius,length-radius*2.2,boneMaterial(),[0,-length/2,0],12)); g.add(sphere(radius*1.45,boneMaterial(),[0,-radius,0],12)); g.add(sphere(radius*1.45,boneMaterial(),[0,-length+radius,0],12)); return g; }
function addSkeleton(group, state = {}, health = false) {
  const angle = state.angle !== undefined ? state.angle : 110; const mobility = state.mobility !== undefined ? state.mobility : 72; const rad=angle*Math.PI/180; const bone=boneMaterial(); const hi=mat(health?0xef4444:0x60a5fa,{emissive:health?0xef4444:0x3b82f6,emissiveIntensity:.55,roughness:.3});
  const root=new THREE.Group(); root.position.set(0,0.75,0); group.add(root);
  const skull=sphere(.24,bone,[0,2.35,0],32); skull.scale.set(.88,1.12,.98); root.add(skull); root.add(ellipsoid(.14,.07,.10,bone,[0,2.18,.035],20)); for(let i=0;i<18;i++){ const y=1.90-i*.06; const rib=torus(.43-i*.010,.010,bone,[0,y,0],48,6); rib.scale.z=.45; rib.rotation.x=Math.PI/2; rib.rotation.z=Math.PI; root.add(rib);} root.add(cyl(.035,.045,1.55,bone,[0,1.47,0],16)); root.add(box(.72,.05,.10,bone,[0,1.95,0])); root.add(box(.48,.12,.18,bone,[0,.82,0]));
  function limb(anchor, l1, l2, bend=0, side=1){ const upper=makeBone(l1,.035); upper.position.set(...anchor); upper.rotation.z=side*.12; root.add(upper); const elbow=new THREE.Group(); elbow.position.set(anchor[0]+side*.10,anchor[1]-l1,anchor[2]); elbow.rotation.x=bend; const lower=makeBone(l2,.030); elbow.add(lower); root.add(elbow); return elbow; }
  const elbowBend=(state.joint==='elbow hinge'&&!health)?-rad*.8:0; const kneeBend=(state.joint==='knee hinge'&&!health)?rad*.55:(health&&state.joint==='knee'?(100-mobility)*.012:0);
  limb([-.55,1.84,0],.62,.55,elbowBend,-1); limb([.55,1.84,0],.62,.55,elbowBend,1); limb([-.24,.76,0],.82,.76,kneeBend,-1); limb([.24,.76,0],.82,.76,kneeBend,1);
  [['neck pivot',[0,2.15,0]],['shoulder ball',[-.55,1.84,0]],['elbow hinge',[-.45,1.20,0]],['hip',[-.24,.76,0]],['knee hinge',[-.16,-.05,0]],['spine',[0,1.40,0]],['wrist',[-.34,.64,0]]].forEach(([n,p])=>{ const active=String(state.joint||'').includes(n.split(' ')[0]) || (!health&&state.joint===n); if(active){ const ring=torus(.13,.020,hi,p,32,8); ring.rotation.x=Math.PI/2; root.add(ring);} });
  label(group, health ? `mobility ${mobility}% | disorder context` : `joint angle ${angle} deg`, [0,2.98,0], { scale:.16 });
}
function addCockroach(group,state={}){ addTray(group,'cockroach external morphology'); addCockroachLike(group,[0,1.32,0],1.40,0x7c2d12); leader(group,'head',[-1.35,2.18,-.50],[-.78,1.42,0]); leader(group,'thorax',[-.35,2.28,.55],[-.10,1.34,0]); leader(group,'abdomen',[.86,2.18,-.55],[.68,1.32,0]); leader(group,'three pairs of legs',[1.55,1.68,.75],[.20,1.22,.72]); leader(group,'antennae',[-1.65,2.55,.44],[-1.08,1.66,.36]); label(group,`view: ${state.view||'dorsal'} / focus ${state.zoomPart||'thorax'}`,[0,2.76,0],{scale:.145}); }


function addMetricPlaque(group, config, state) {
  const rows = getBiologyMetricRows(config, state, 0).slice(0, 4);
  const g = new THREE.Group();
  g.position.set(2.72, 1.18, 1.72);
  g.rotation.y = -0.48;
  g.add(box(1.92, 1.18, 0.055, mat(0x020617, { opacity: 0.88, roughness: 0.34 }), [0, 0, 0]));
  g.add(box(1.82, 0.055, 0.065, mat(0x22c55e, { emissive: 0x16a34a, emissiveIntensity: 0.24 }), [0, 0.49, 0.035]));
  label(g, 'verified live readings', [0, 0.72, 0.06], { scale: 0.075, fontSize: 16, bg: 'rgba(21,128,61,.82)' });
  rows.forEach((row, i) => {
    const y = 0.30 - i * 0.20;
    label(g, `${row[0]}: ${row[1]}`, [-0.02, y, 0.07], { scale: 0.061, fontSize: 14, bg: 'rgba(15,23,42,.72)' });
  });
  const formula = getBiologyFormula(config, state);
  label(g, formula.length > 48 ? `${formula.slice(0, 46)}...` : formula, [0, -0.62, 0.07], { scale: 0.052, fontSize: 13, bg: 'rgba(30,41,59,.82)' });
  group.add(g);
}
function addCalibrationReference(group, kind) {
  if (['microscope','mitosis','plasmolysis','stomata','anatomyTS','animalTissue','animalMitosis','frogDev','microscopeParts'].includes(kind)) {
    addDimensionBar(group, 'ocular field scale', 1.15, 2.62, 0.88);
    return;
  }
  if (['quadrat','quadrat2','pond','pondZoo','conservation'].includes(kind)) {
    addDimensionBar(group, 'field scale reference', -1.8, 1.8, 0.88);
    return;
  }
  if (['osmosis','transpiration','respiration','anaerobic','suction','amylase','bloodSugar'].includes(kind)) {
    addDimensionBar(group, 'graduated reading scale', -0.9, 1.25, 0.88);
  }
}

export function buildBiologyModel(root, config, state, actors = {}) {
  addBench(root);
  const kind = config.kind;
  if (['microscope','mitosis','plasmolysis','stomata','anatomyTS','animalTissue','animalMitosis'].includes(kind)) { addMicroscope(root, state, { tint: kind === 'stomata' ? 0xbbf7d0 : 0xf9a8d4 }); addMicroscopeField(root, kind, state); }
  else if (kind === 'microscopeParts') { addMicroscope(root, state); leader(root,'eyepiece',[1.36,2.72,.30],[-1.25,3.45,0]); leader(root,'objectives',[1.36,2.34,.30],[-1.45,2.38,0]); leader(root,'stage + slide',[1.36,1.96,.30],[-1.35,1.79,0]); leader(root,'mirror/lamp',[1.36,1.58,.30],[-1.42,1.34,0]); }
  else if (kind === 'flower') addFlower(root, state);
  else if (kind === 'inflorescence') addInflorescence(root, state);
  else if (kind === 'herbarium') addHerbarium(root, state);
  else if (kind === 'mushroom') addMushroom(root, state);
  else if (kind === 'culture') addCulture(root, state);
  else if (kind === 'pond') addPond(root, state, false);
  else if (kind === 'pondZoo') addPond(root, state, true);
  else if (kind === 'quadrat') addQuadrat(root, state, false);
  else if (kind === 'quadrat2') addQuadrat(root, state, true);
  else if (kind === 'soil') addSoil(root, state);
  else if (kind === 'specimens') addSpecimens(root, state);
  else if (kind === 'fossil') addFossil(root, state);
  else if (kind === 'animals') addAnimals(root, state);
  else if (kind === 'dissection') addDissection(root, state);
  else if (kind === 'conservation') addConservation(root, state);
  else if (kind === 'osmosis') addOsmosis(root, state);
  else if (['transpiration','respiration','anaerobic','phototropism','apicalBud','suction'].includes(kind)) addPhysiology(root, state, kind);
  else if (kind === 'genetics') addGenetics(root, state);
  else if (kind === 'imbibition') addImbibition(root, state);
  else if (kind === 'biofertilizer') addBiofertilizer(root, state);
  else if (kind === 'frogDev') addFrogDev(root, state);
  else if (['starchTest','proteinTest','urine'].includes(kind)) addBiochemical(root, state, kind);
  else if (kind === 'amylase') addAmylase(root, state);
  else if (kind === 'bloodSugar') addBloodSugar(root, state);
  else if (kind === 'skeleton') addSkeleton(root, state, false);
  else if (kind === 'skeletonHealth') addSkeleton(root, state, true);
  else if (kind === 'cockroach') addCockroach(root, state);
  else { addTray(root, 'biology practical model'); label(root, config.title, [0,2.3,0], { scale:.16 }); }
  addMetricPlaque(root, config, state);
  addCalibrationReference(root, kind);
  addStamp(root, 'scan-grade scientific PBR - responsive/optimized');
  // Collapse the hundreds of individually transformed primitives into one buffer per
  // material before the scan-grade pass, so material/texture generation and vertex
  // displacement run on a handful of meshes instead of several hundred.
  batchStaticGeometry(root, { mergeLines: true });
  addScanGradeEnhancement(root, { kind, config, state, quality: actors.quality, seed: config.slug || kind });
  // The scan-grade pass scatters many small micro-detail pieces; batch those too.
  batchStaticGeometry(root, { mergeLines: true });
}

export function disposeBioMaterials() {
  MATERIAL_CACHE.forEach((m) => m.dispose());
  MATERIAL_CACHE.clear();
  disposeScanGradeAssets();
}
