import { THREE, makeLabelSprite } from './engine.js';

// Scan-grade biology renderer
// This does not fake downloadable photogrammetry files. It upgrades the live Three.js models
// with PBR materials, deterministic micro-displacement, high-frequency texture maps,
// specimen-specific micro details and optimizer-aware detail counts.

const TEXTURE_CACHE = new Map();
const MATERIAL_CACHE = new Map();
const Y_AXIS = new THREE.Vector3(0, 1, 0);
const TMP_V = new THREE.Vector3();
const TMP_N = new THREE.Vector3();

function intColor(color) {
  if (color instanceof THREE.Color) return color.getHex();
  if (typeof color === 'number') return color;
  try { return new THREE.Color(color || 0xffffff).getHex(); } catch (e) { return 0xffffff; }
}
function colorStyle(hex, mul = 1, add = 0) {
  const c = new THREE.Color(hex);
  c.r = Math.max(0, Math.min(1, c.r * mul + add));
  c.g = Math.max(0, Math.min(1, c.g * mul + add));
  c.b = Math.max(0, Math.min(1, c.b * mul + add));
  return `rgb(${Math.round(c.r * 255)},${Math.round(c.g * 255)},${Math.round(c.b * 255)})`;
}
function hashString(text) {
  const s = String(text || 'bio');
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h >>> 0;
}
function seeded(seed) {
  let s = hashString(seed) || 1;
  return () => {
    s = Math.imul(s ^ (s >>> 15), 2246822507) >>> 0;
    s = Math.imul(s ^ (s >>> 13), 3266489909) >>> 0;
    return ((s ^ (s >>> 16)) >>> 0) / 4294967296;
  };
}
function clamp(v, a = 0, b = 1) { return Math.max(a, Math.min(b, v)); }
function smoothstep(edge0, edge1, x) {
  const t = clamp((x - edge0) / Math.max(1e-6, edge1 - edge0));
  return t * t * (3 - 2 * t);
}
function noise3(x, y, z, seed = 1) {
  const n = Math.sin(x * 12.9898 + y * 78.233 + z * 37.719 + seed * 0.12345) * 43758.5453123;
  return n - Math.floor(n);
}
function fbm(x, y, z, seed = 1) {
  let value = 0;
  let amp = 0.55;
  let freq = 1;
  let norm = 0;
  for (let i = 0; i < 4; i++) {
    value += noise3(x * freq, y * freq, z * freq, seed + i * 17) * amp;
    norm += amp;
    amp *= 0.52;
    freq *= 2.13;
  }
  return value / Math.max(1e-6, norm);
}
function canvasTexture(key, factory, opts = {}) {
  const cacheKey = JSON.stringify([key, opts.kind || 'map', opts.size || 256]);
  if (TEXTURE_CACHE.has(cacheKey)) return TEXTURE_CACHE.get(cacheKey);
  const size = opts.size || 256;
  if (typeof document === 'undefined' || !document.createElement) {
    const data = new Uint8Array(size * size * 4);
    for (let i = 0; i < size * size; i++) {
      const v = opts.kind === 'normal' ? 128 : 180;
      data[i * 4] = v;
      data[i * 4 + 1] = v;
      data[i * 4 + 2] = opts.kind === 'normal' ? 255 : v;
      data[i * 4 + 3] = 255;
    }
    const tex = new THREE.DataTexture(data, size, size, THREE.RGBAFormat);
    tex.needsUpdate = true;
    TEXTURE_CACHE.set(cacheKey, tex);
    return tex;
  }
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) {
    const data = new Uint8Array(size * size * 4);
    for (let i = 0; i < size * size; i++) {
      const v = opts.kind === 'normal' ? 128 : 180;
      data[i * 4] = v;
      data[i * 4 + 1] = v;
      data[i * 4 + 2] = opts.kind === 'normal' ? 255 : v;
      data[i * 4 + 3] = 255;
    }
    const tex = new THREE.DataTexture(data, size, size, THREE.RGBAFormat);
    tex.needsUpdate = true;
    TEXTURE_CACHE.set(cacheKey, tex);
    return tex;
  }
  factory(ctx, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.wrapS = opts.wrapS || THREE.RepeatWrapping;
  tex.wrapT = opts.wrapT || THREE.RepeatWrapping;
  const repeat = opts.repeat || 1;
  tex.repeat.set(repeat, repeat);
  tex.anisotropy = opts.anisotropy || 4;
  if (opts.colorSpace && tex.colorSpace !== undefined) tex.colorSpace = opts.colorSpace;
  tex.needsUpdate = true;
  TEXTURE_CACHE.set(cacheKey, tex);
  return tex;
}
function makeAlbedoTexture(seedKey, baseColor, family = 'tissue', size = 256) {
  const hex = intColor(baseColor);
  const rand = seeded(`${seedKey}:albedo:${hex}:${family}`);
  return canvasTexture(`${seedKey}:${hex}:${family}:albedo`, (ctx, s) => {
    const grad = ctx.createRadialGradient(s * 0.44, s * 0.38, 4, s * 0.50, s * 0.50, s * 0.80);
    grad.addColorStop(0, colorStyle(hex, 1.22, 0.02));
    grad.addColorStop(0.62, colorStyle(hex, 0.98));
    grad.addColorStop(1, colorStyle(hex, 0.70));
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, s, s);

    const strokeCount = family === 'leaf' ? 120 : family === 'chitin' ? 170 : family === 'bone' ? 90 : family === 'fur' ? 190 : 140;
    for (let i = 0; i < strokeCount; i++) {
      const x = rand() * s;
      const y = rand() * s;
      const len = (family === 'leaf' ? 28 : family === 'fur' ? 18 : 9) * (0.35 + rand());
      const a = family === 'leaf' ? (Math.PI / 2 + (rand() - 0.5) * 0.9) : rand() * Math.PI * 2;
      ctx.strokeStyle = colorStyle(hex, 0.72 + rand() * 0.62, rand() * 0.04);
      ctx.globalAlpha = 0.08 + rand() * 0.18;
      ctx.lineWidth = family === 'bone' ? 0.7 : 0.4 + rand() * 1.2;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.quadraticCurveTo(x + Math.cos(a + 0.35) * len * 0.45, y + Math.sin(a + 0.35) * len * 0.45, x + Math.cos(a) * len, y + Math.sin(a) * len);
      ctx.stroke();
    }
    if (family === 'leaf') {
      ctx.globalAlpha = 0.22;
      ctx.strokeStyle = colorStyle(hex, 0.52);
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.moveTo(s * 0.5, 0);
      ctx.lineTo(s * 0.5, s);
      ctx.stroke();
      for (let i = 0; i < 16; i++) {
        const y = i * s / 16;
        const side = i % 2 ? 1 : -1;
        ctx.beginPath();
        ctx.moveTo(s * 0.5, y);
        ctx.lineTo(s * (0.5 + side * (0.22 + rand() * 0.25)), y + s * (0.04 + rand() * 0.08));
        ctx.stroke();
      }
    }
    if (family === 'chitin') {
      ctx.globalAlpha = 0.18;
      ctx.strokeStyle = colorStyle(hex, 0.45);
      ctx.lineWidth = 2;
      for (let i = 0; i < 14; i++) {
        const y = (i + 0.5) * s / 14;
        ctx.beginPath();
        ctx.moveTo(0, y + Math.sin(i) * 4);
        ctx.bezierCurveTo(s * 0.25, y - 10, s * 0.72, y + 10, s, y);
        ctx.stroke();
      }
    }
    ctx.globalAlpha = 0.12;
    for (let i = 0; i < 900; i++) {
      const v = Math.floor(160 + rand() * 70);
      ctx.fillStyle = `rgba(${v},${v},${v},${0.05 + rand() * 0.18})`;
      ctx.fillRect(rand() * s, rand() * s, 1, 1);
    }
    ctx.globalAlpha = 1;
  }, { kind: 'albedo', size, repeat: family === 'fur' ? 2 : 1, colorSpace: THREE.SRGBColorSpace });
}
function makeReliefTexture(seedKey, family = 'tissue', size = 256) {
  const rand = seeded(`${seedKey}:relief:${family}`);
  return canvasTexture(`${seedKey}:${family}:relief`, (ctx, s) => {
    ctx.fillStyle = 'rgb(128,128,255)';
    ctx.fillRect(0, 0, s, s);
    const count = family === 'leaf' ? 170 : family === 'bone' ? 95 : family === 'chitin' ? 210 : family === 'fur' ? 260 : 220;
    for (let i = 0; i < count; i++) {
      const x = rand() * s;
      const y = rand() * s;
      const w = family === 'fur' ? 1 + rand() * 2 : 2 + rand() * 7;
      const h = family === 'fur' ? 18 + rand() * 36 : 3 + rand() * 14;
      const a = family === 'leaf' ? Math.PI * 0.5 + (rand() - 0.5) * 0.7 : rand() * Math.PI;
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(a);
      ctx.globalAlpha = 0.06 + rand() * 0.28;
      ctx.fillStyle = rand() > 0.5 ? 'rgb(160,160,255)' : 'rgb(96,96,245)';
      ctx.beginPath();
      ctx.ellipse(0, 0, w, h, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
    ctx.globalAlpha = 0.18;
    ctx.strokeStyle = 'rgb(174,174,255)';
    ctx.lineWidth = family === 'leaf' ? 2 : 0.8;
    for (let i = 0; i < (family === 'leaf' ? 20 : 12); i++) {
      const y = rand() * s;
      ctx.beginPath();
      ctx.moveTo(rand() * s, y);
      ctx.bezierCurveTo(rand() * s, y + rand() * 20, rand() * s, y - rand() * 20, rand() * s, y + (rand() - 0.5) * 28);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }, { kind: 'normal', size, repeat: family === 'fur' ? 2 : 1 });
}
function makeRoughnessTexture(seedKey, family = 'tissue', size = 128) {
  const rand = seeded(`${seedKey}:rough:${family}`);
  return canvasTexture(`${seedKey}:${family}:rough`, (ctx, s) => {
    const base = family === 'wet' ? 80 : family === 'chitin' ? 135 : family === 'bone' ? 170 : 150;
    ctx.fillStyle = `rgb(${base},${base},${base})`;
    ctx.fillRect(0, 0, s, s);
    for (let i = 0; i < 1800; i++) {
      const v = Math.floor(base - 45 + rand() * 90);
      ctx.fillStyle = `rgb(${v},${v},${v})`;
      ctx.fillRect(rand() * s, rand() * s, 1 + Math.floor(rand() * 2), 1 + Math.floor(rand() * 2));
    }
  }, { kind: 'roughness', size, repeat: 1 });
}
function materialFamilyFromColor(color, material) {
  if (!material) return 'tissue';
  if ((material.metalness || 0) > 0.35) return 'metal';
  if (material.transparent && (material.opacity || 1) < 0.34) return 'glass';
  const c = new THREE.Color(intColor(color));
  const hsl = { h: 0, s: 0, l: 0 };
  c.getHSL(hsl);
  if (hsl.s < 0.15 && hsl.l > 0.68) return 'bone';
  if (hsl.h > 0.18 && hsl.h < 0.45 && hsl.s > 0.22) return 'leaf';
  if (hsl.h > 0.03 && hsl.h < 0.13 && hsl.s > 0.25) return 'chitin';
  if (hsl.h > 0.95 || hsl.h < 0.04) return 'tissue';
  if (hsl.h > 0.83 && hsl.h < 0.98) return 'tissue';
  return 'tissue';
}
export function makeScanMaterial(key, baseColor, opts = {}) {
  const hex = intColor(baseColor);
  const family = opts.family || materialFamilyFromColor(hex, opts);
  const cacheKey = JSON.stringify([key, hex, family, opts.opacity ?? 1, opts.side || 0, opts.transparent || false]);
  if (MATERIAL_CACHE.has(cacheKey)) return MATERIAL_CACHE.get(cacheKey).clone();
  const Ctor = THREE.MeshPhysicalMaterial || THREE.MeshStandardMaterial;
  const familyWet = opts.wet || family === 'tissue' || family === 'leaf';
  const mat = new Ctor({
    color: hex,
    map: opts.map === false ? null : makeAlbedoTexture(key, hex, family, opts.textureSize || 256),
    normalMap: opts.normalMap === false ? null : makeReliefTexture(key, family, opts.textureSize || 256),
    roughnessMap: opts.roughnessMap === false ? null : makeRoughnessTexture(key, family === 'glass' ? 'wet' : family, 128),
    roughness: opts.roughness ?? (family === 'bone' ? 0.72 : family === 'chitin' ? 0.48 : familyWet ? 0.38 : 0.66),
    metalness: opts.metalness ?? 0.0,
    transparent: opts.transparent || (opts.opacity !== undefined && opts.opacity < 1),
    opacity: opts.opacity ?? 1,
    side: opts.side ?? THREE.FrontSide,
    emissive: opts.emissive ?? 0x000000,
    emissiveIntensity: opts.emissiveIntensity ?? 0,
    clearcoat: opts.clearcoat ?? (familyWet ? 0.18 : family === 'chitin' ? 0.22 : 0.04),
    clearcoatRoughness: opts.clearcoatRoughness ?? 0.42,
    sheen: opts.sheen ?? (family === 'fur' ? 0.45 : 0),
    sheenRoughness: opts.sheenRoughness ?? 0.72,
  });
  if (mat.normalScale) mat.normalScale.set(opts.normalScaleX ?? 0.38, opts.normalScaleY ?? 0.38);
  mat.userData.scanGrade = true;
  MATERIAL_CACHE.set(cacheKey, mat);
  return mat.clone();
}
function shouldSkipMesh(obj) {
  if (!obj || !obj.isMesh || !obj.geometry || !obj.geometry.attributes || !obj.geometry.attributes.position) return true;
  const type = obj.geometry.type || '';
  if (type.includes('BoxGeometry') || type.includes('PlaneGeometry') || type.includes('CircleGeometry')) return true;
  if (obj.userData && obj.userData.noScan) return true;
  const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
  if (mats.some((m) => m && ((m.metalness || 0) > 0.42 || (m.transparent && (m.opacity || 1) < 0.23)))) return true;
  return false;
}
export function applyOrganicDisplacement(object, opts = {}) {
  const seed = hashString(opts.seed || opts.kind || 'bio');
  const baseIntensity = opts.intensity ?? 0.018;
  const freq = opts.frequency ?? 1.35;
  object.traverse((obj) => {
    if (shouldSkipMesh(obj)) return;
    const type = obj.geometry.type || '';
    const intensity = type.includes('Sphere') ? baseIntensity : baseIntensity * 0.72;
    if (intensity <= 0) return;
    const geo = obj.geometry.clone();
    if (!geo.attributes.normal) geo.computeVertexNormals();
    const pos = geo.attributes.position;
    const normal = geo.attributes.normal;
    const localSeed = (seed ^ hashString(obj.uuid || obj.name || type)) >>> 0;
    for (let i = 0; i < pos.count; i++) {
      TMP_V.set(pos.getX(i), pos.getY(i), pos.getZ(i));
      TMP_N.set(normal.getX(i), normal.getY(i), normal.getZ(i)).normalize();
      const ridge = fbm(TMP_V.x * freq + 3.7, TMP_V.y * freq - 2.2, TMP_V.z * freq + 0.91, localSeed);
      const pore = fbm(TMP_V.x * freq * 5.0, TMP_V.y * freq * 5.0, TMP_V.z * freq * 5.0, localSeed + 93);
      const band = Math.sin((TMP_V.y + TMP_V.x * 0.18) * 18.0 + localSeed * 0.0001) * 0.5 + 0.5;
      const disp = ((ridge - 0.5) * 1.15 + (pore - 0.5) * 0.40 + (band - 0.5) * 0.22) * intensity;
      TMP_V.addScaledVector(TMP_N, disp);
      pos.setXYZ(i, TMP_V.x, TMP_V.y, TMP_V.z);
    }
    pos.needsUpdate = true;
    geo.computeVertexNormals();
    obj.geometry = geo;
    obj.userData.scanDisplaced = true;
  });
}
function maybeUpgradeMaterial(mesh, opts = {}) {
  const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
  const upgraded = materials.map((m, idx) => {
    if (!m || m.userData?.scanGrade) return m;
    if ((m.metalness || 0) > 0.35 || (m.transparent && (m.opacity || 1) < 0.28)) return m;
    const color = m.color ? m.color.getHex() : 0xffffff;
    const family = opts.family || materialFamilyFromColor(color, m);
    if (family === 'glass' || family === 'metal') return m;
    const u = makeScanMaterial(`${opts.seed || 'bio'}:${family}:${color.toString(16)}:${idx}`, color, {
      family,
      opacity: m.opacity ?? 1,
      transparent: m.transparent || ((m.opacity ?? 1) < 1),
      roughness: Math.min(0.92, Math.max(0.24, m.roughness ?? 0.56)),
      metalness: m.metalness ?? 0,
      side: m.side ?? THREE.FrontSide,
      emissive: m.emissive ? m.emissive.getHex() : 0x000000,
      emissiveIntensity: m.emissiveIntensity ?? 0,
      textureSize: opts.textureSize || 256,
    });
    u.__shared = false;
    return u;
  });
  mesh.material = Array.isArray(mesh.material) ? upgraded : upgraded[0];
}
export function upgradeSceneMaterials(root, opts = {}) {
  root.traverse((obj) => {
    if (obj.isMesh) maybeUpgradeMaterial(obj, opts);
  });
}
function line(points, color = 0xffffff, opacity = 0.7) {
  const geo = new THREE.BufferGeometry().setFromPoints(points.map((p) => Array.isArray(p) ? new THREE.Vector3(...p) : p));
  const mat = new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity });
  const l = new THREE.Line(geo, mat);
  l.userData.noScan = true;
  return l;
}
function tube(points, radius, material, tubularSegments = 32, radialSegments = 6) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => Array.isArray(p) ? new THREE.Vector3(...p) : p));
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, tubularSegments, radius, radialSegments, false), material);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}
function cylBetween(a, b, radius, material, radial = 8) {
  const va = Array.isArray(a) ? new THREE.Vector3(...a) : a.clone();
  const vb = Array.isArray(b) ? new THREE.Vector3(...b) : b.clone();
  const mid = va.clone().add(vb).multiplyScalar(0.5);
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, va.distanceTo(vb), radial), material);
  mesh.position.copy(mid);
  mesh.quaternion.setFromUnitVectors(Y_AXIS, vb.clone().sub(va).normalize());
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}
function sphere(radius, material, pos, seg = 16) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(radius, seg, Math.max(8, Math.floor(seg / 2))), material);
  m.position.set(...pos);
  m.castShadow = true;
  m.receiveShadow = true;
  return m;
}
function ellipsoid(rx, ry, rz, material, pos, seg = 20) {
  const m = sphere(1, material, pos, seg);
  m.scale.set(rx, ry, rz);
  return m;
}
function addSpriteLabel(group, text, pos, opts = {}) {
  const s = makeLabelSprite(text, { scale: opts.scale || 0.16, fontSize: opts.fontSize || 22, bg: opts.bg || 'rgba(15,23,42,.72)', color: opts.color });
  s.position.set(...pos);
  s.userData.noScan = true;
  group.add(s);
  return s;
}
function qualityCount(quality, high, medium, low) {
  if (!quality) return medium;
  if (quality.tier === 'low' || quality.mobile) return low;
  if (quality.tier === 'medium') return medium;
  return high;
}
function addScanPlaque(root, kind) {
  const plaque = new THREE.Group();
  plaque.name = 'scan-grade-plaque';
  plaque.userData.noScan = true;
  plaque.position.set(-2.70, 1.06, 1.82);
  plaque.rotation.y = 0.46;
  const backing = new THREE.Mesh(new THREE.BoxGeometry(1.98, 0.66, 0.05), new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.42, transparent: true, opacity: 0.88 }));
  backing.userData.noScan = true;
  plaque.add(backing);
  addSpriteLabel(plaque, 'scan-grade PBR', [0, 0.21, 0.07], { scale: 0.075, fontSize: 16, bg: 'rgba(88,28,135,.82)' });
  addSpriteLabel(plaque, 'micro texture + displaced mesh', [0, -0.02, 0.07], { scale: 0.055, fontSize: 13, bg: 'rgba(15,23,42,.70)' });
  addSpriteLabel(plaque, String(kind || 'biology model'), [0, -0.22, 0.07], { scale: 0.047, fontSize: 12, bg: 'rgba(15,23,42,.58)' });
  root.add(plaque);
}
function addCompoundEye(group, pos, side = 1, scale = 1) {
  const eye = new THREE.Group();
  eye.position.set(...pos);
  eye.scale.setScalar(scale);
  const eyeMat = makeScanMaterial(`compound-eye-${side}`, 0x1f1208, { family: 'chitin', roughness: 0.34, clearcoat: 0.5, textureSize: 128 });
  eye.add(ellipsoid(0.13, 0.10, 0.13, eyeMat, [0, 0, 0], 24));
  const facetMat = new THREE.MeshStandardMaterial({ color: 0x050505, roughness: 0.22, metalness: 0.05, transparent: true, opacity: 0.72 });
  for (let r = 0; r < 5; r++) {
    for (let c = 0; c < 6; c++) {
      const a = c / 6 * Math.PI * 2;
      const rr = 0.022 + r * 0.017;
      const facet = new THREE.Mesh(new THREE.CircleGeometry(0.010, 6), facetMat);
      facet.position.set(Math.cos(a) * rr, 0.010 + (r - 2) * 0.015, Math.sin(a) * rr);
      facet.lookAt(new THREE.Vector3(Math.cos(a) * 2, facet.position.y, Math.sin(a) * 2));
      eye.add(facet);
    }
  }
  group.add(eye);
}
function addCockroachMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'cockroach-scan-detail';
  const rand = seeded(`${seedKey}:roach`);
  const chitin = makeScanMaterial('cockroach-sclerite-pbr', 0x7c2d12, { family: 'chitin', roughness: 0.42, clearcoat: 0.28, textureSize: 256 });
  const spine = makeScanMaterial('cockroach-leg-spines', 0x111111, { family: 'chitin', roughness: 0.55, textureSize: 128 });
  for (let i = 0; i < 9; i++) {
    const x = -0.30 + i * 0.12;
    const band = new THREE.Mesh(new THREE.TorusGeometry(0.23 + Math.sin(i) * 0.012, 0.006, 5, 28), chitin);
    band.position.set(0.46 + x, 1.47 - Math.abs(i - 4) * 0.012, 0);
    band.rotation.x = Math.PI / 2;
    band.scale.set(1.55 - Math.abs(i - 4) * 0.05, 0.46, 0.25);
    g.add(band);
  }
  [-1, 1].forEach((side) => {
    addCompoundEye(g, [-1.03, 1.45, side * 0.16], side, 0.72);
    g.add(tube([[-1.05, 1.54, side * 0.10], [-1.45, 1.82, side * 0.34], [-1.78, 1.76, side * 0.50]], 0.008, spine, 36, 6));
    for (let leg = 0; leg < 3; leg++) {
      for (let i = 0; i < qualityCount(quality, 8, 5, 3); i++) {
        const x = -0.26 + leg * 0.38 + (rand() - 0.5) * 0.08;
        const z = side * (0.53 + rand() * 0.26);
        g.add(cylBetween([x, 1.26, z], [x + (rand() - 0.45) * 0.16, 1.30 + rand() * 0.12, z + side * (0.12 + rand() * 0.10)], 0.004, spine, 5));
      }
    }
  });
  addSpriteLabel(g, 'faceted compound eyes + leg spines', [0, 2.48, 0.95], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addFlowerMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'flower-scan-detail';
  const rand = seeded(`${seedKey}:flower`);
  const veinMat = makeScanMaterial('petal-raised-veins', 0xfbcfe8, { family: 'leaf', roughness: 0.52, textureSize: 128 });
  const pollenMat = makeScanMaterial('pollen-grains', 0xfacc15, { family: 'bone', roughness: 0.78, textureSize: 128 });
  [-1, 1].forEach((side) => {
    for (let i = 0; i < qualityCount(quality, 18, 12, 7); i++) {
      const a = (i / 18) * Math.PI * 2;
      const base = [Math.cos(a) * 0.22, 2.01, Math.sin(a) * 0.22];
      const tip = [Math.cos(a) * (0.80 + rand() * 0.16), 2.08 + (rand() - 0.5) * 0.10, Math.sin(a) * (0.80 + rand() * 0.16)];
      g.add(tube([base, [(base[0] + tip[0]) / 2, 2.13 + rand() * 0.08, (base[2] + tip[2]) / 2], tip], 0.0045, veinMat, 18, 4));
    }
    for (let i = 0; i < qualityCount(quality, 65, 42, 24); i++) {
      const a = rand() * Math.PI * 2;
      const r = 0.16 + rand() * 0.26;
      g.add(sphere(0.008 + rand() * 0.008, pollenMat, [Math.cos(a) * r, 2.22 + rand() * 0.10, Math.sin(a) * r], 7));
    }
  });
  addSpriteLabel(g, 'raised petal veins + pollen grains', [0.20, 2.72, 0.88], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addLeafMicro(root, quality, seedKey, yBase = 1.2) {
  const g = new THREE.Group();
  g.name = 'leaf-scan-detail';
  const rand = seeded(`${seedKey}:leaf`);
  const vein = makeScanMaterial('leaf-secondary-veins', 0x14532d, { family: 'leaf', roughness: 0.64, textureSize: 128 });
  const pore = makeScanMaterial('stomatal-pores', 0x052e16, { family: 'leaf', roughness: 0.44, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 42, 26, 15); i++) {
    const t = rand();
    const x = (rand() - 0.5) * (2.8 - t * 1.4);
    const y = yBase + t * 1.8;
    const z = (rand() - 0.5) * 0.18;
    g.add(tube([[0, y, z], [x * 0.50, y + 0.06, z + 0.015], [x, y + 0.12, z]], 0.004, vein, 12, 4));
    if (i % 2 === 0) {
      const stoma = ellipsoid(0.030, 0.011, 0.017, pore, [x + (rand() - 0.5) * 0.10, y + 0.05, z + 0.03], 10);
      stoma.rotation.z = rand() * Math.PI;
      g.add(stoma);
    }
  }
  addSpriteLabel(g, 'cuticle, veins and stomata', [1.55, yBase + 2.05, 0.35], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addMushroomMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'mushroom-scan-detail';
  const rand = seeded(`${seedKey}:mushroom`);
  const gill = makeScanMaterial('mushroom-gills-pbr', 0xffedd5, { family: 'bone', roughness: 0.82, textureSize: 128 });
  const spot = makeScanMaterial('mushroom-cap-speckles', 0xf8fafc, { family: 'bone', roughness: 0.75, textureSize: 128 });
  for (let cap = 0; cap < 4; cap++) {
    const x = -1.25 + cap * 0.82;
    const h = 0.45 + cap * 0.10;
    for (let i = 0; i < qualityCount(quality, 20, 14, 8); i++) {
      const a = i / 20 * Math.PI * 2;
      g.add(cylBetween([x, 1.31 + h, 0], [x + Math.cos(a) * 0.30, 1.30 + h, Math.sin(a) * 0.30], 0.003, gill, 4));
    }
    for (let i = 0; i < qualityCount(quality, 22, 14, 6); i++) {
      const a = rand() * Math.PI * 2;
      const r = Math.sqrt(rand()) * 0.27;
      g.add(ellipsoid(0.014 + rand() * 0.012, 0.006, 0.014 + rand() * 0.012, spot, [x + Math.cos(a) * r, 1.53 + h + rand() * 0.04, Math.sin(a) * r], 8));
    }
  }
  addSpriteLabel(g, 'individual gills, ring/volva texture', [0, 2.47, 0.96], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addSkeletonMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'skeleton-scan-detail';
  const suture = new THREE.LineBasicMaterial({ color: 0x6b5f4a, transparent: true, opacity: 0.68 });
  const disc = makeScanMaterial('intervertebral-discs', 0xf5d0c5, { family: 'tissue', roughness: 0.62, textureSize: 128 });
  for (let i = 0; i < 3; i++) {
    const pts = [];
    for (let k = 0; k < 36; k++) {
      const a = k / 35 * Math.PI * 2;
      pts.push(new THREE.Vector3(Math.cos(a) * (0.12 + i * 0.045), 3.10 + Math.sin(a * 2 + i) * 0.018, Math.sin(a) * (0.18 + i * 0.03)));
    }
    const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), suture);
    l.userData.noScan = true;
    g.add(l);
  }
  for (let i = 0; i < qualityCount(quality, 12, 9, 6); i++) {
    const y = 2.75 - i * 0.12;
    const d = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.007, 5, 24), disc);
    d.position.set(0, y, 0);
    d.rotation.x = Math.PI / 2;
    g.add(d);
  }
  addSpriteLabel(g, 'cranial sutures + disc surfaces', [0.70, 2.96, 0.70], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addMicrographDetails(root, quality, seedKey, kind) {
  const g = new THREE.Group();
  g.name = 'micrograph-scan-detail';
  const rand = seeded(`${seedKey}:micro:${kind}`);
  const membrane = makeScanMaterial('cell-membrane-relief', 0xa7f3d0, { family: 'leaf', roughness: 0.70, textureSize: 128 });
  const nucleus = makeScanMaterial('nucleus-chromatin', 0x7c3aed, { family: 'tissue', roughness: 0.58, textureSize: 128 });
  const count = qualityCount(quality, 52, 32, 18);
  for (let i = 0; i < count; i++) {
    const x = 1.18 + rand() * 1.32;
    const y = 1.48 + rand() * 1.10;
    const r = 0.035 + rand() * 0.045;
    const cell = ellipsoid(r * (1.2 + rand() * 0.9), r * (0.7 + rand() * 0.7), 0.005, membrane, [x, y, -0.640 - rand() * 0.010], 10);
    cell.rotation.z = rand() * Math.PI;
    g.add(cell);
    if (i % 3 === 0) g.add(ellipsoid(r * 0.32, r * 0.22, 0.007, nucleus, [x + (rand() - 0.5) * r, y + (rand() - 0.5) * r, -0.625], 8));
  }
  const scaleLine = line([[1.15, 1.35, -0.61], [1.65, 1.35, -0.61]], 0xffffff, 0.86);
  g.add(scaleLine);
  addSpriteLabel(g, '50 um', [1.40, 1.28, -0.56], { scale: 0.052, fontSize: 12, bg: 'rgba(0,0,0,.66)' });
  addSpriteLabel(g, 'irregular cell walls + chromatin', [2.62, 2.73, -0.50], { scale: 0.082, fontSize: 15 });
  root.add(g);
}
function addPondMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'pond-scan-detail';
  const rand = seeded(`${seedKey}:pond`);
  const algae = makeScanMaterial('algae-filaments', 0x22c55e, { family: 'leaf', roughness: 0.56, textureSize: 128 });
  const daphnia = makeScanMaterial('zooplankton-translucent', 0xdbeafe, { family: 'tissue', roughness: 0.35, opacity: 0.58, transparent: true, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 34, 22, 12); i++) {
    const x = (rand() - 0.5) * 2.4;
    const z = (rand() - 0.5) * 2.4;
    g.add(tube([[x, 1.13, z], [x + (rand() - 0.5) * 0.20, 1.25 + rand() * 0.18, z + (rand() - 0.5) * 0.20]], 0.004, algae, 10, 4));
    if (i % 4 === 0) g.add(ellipsoid(0.035, 0.016, 0.026, daphnia, [x + rand() * 0.08, 1.22 + rand() * 0.14, z + rand() * 0.08], 10));
  }
  addSpriteLabel(g, 'algae filaments + plankton', [0.90, 2.20, 1.00], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addAnimalMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'animal-scan-detail';
  const rand = seeded(`${seedKey}:animal`);
  const fur = makeScanMaterial('animal-fur-strands', 0xd6d3d1, { family: 'fur', roughness: 0.92, textureSize: 128 });
  const vessel = makeScanMaterial('dissection-vessels', 0xb91c1c, { family: 'tissue', roughness: 0.42, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 80, 48, 24); i++) {
    const x = (rand() - 0.5) * 1.6;
    const z = (rand() - 0.5) * 0.9;
    const y = 1.45 + (rand() - 0.5) * 0.46;
    g.add(cylBetween([x, y, z], [x + (rand() - 0.5) * 0.05, y + 0.04 + rand() * 0.06, z + (rand() - 0.5) * 0.05], 0.003, fur, 4));
  }
  for (let i = 0; i < 8; i++) {
    const x = -0.35 + i * 0.10;
    g.add(tube([[x, 1.58, -0.10], [x + 0.14, 1.66 + rand() * 0.04, 0.05], [x + 0.24, 1.58, 0.16]], 0.006, vessel, 14, 5));
  }
  addSpriteLabel(g, 'skin follicles + exposed vessels', [0.58, 2.20, 0.82], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addSeedMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'seed-scan-detail';
  const rand = seeded(`${seedKey}:seed`);
  const coat = makeScanMaterial('seed-coat-ridges', 0x6b3a1e, { family: 'chitin', roughness: 0.88, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 46, 30, 16); i++) {
    const x = -1.50 + rand() * 3.0;
    const z = -0.90 + rand() * 1.8;
    const y = 1.11 + rand() * 0.08;
    const r = ellipsoid(0.025 + rand() * 0.025, 0.006, 0.010 + rand() * 0.012, coat, [x, y, z], 8);
    r.rotation.y = rand() * Math.PI;
    g.add(r);
  }
  root.add(g);
}


function addSoilMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'soil-scan-detail';
  const rand = seeded(`${seedKey}:soil`);
  const sand = makeScanMaterial('soil-sand-grains', 0xc68b59, { family: 'chitin', roughness: 0.94, textureSize: 128 });
  const clay = makeScanMaterial('soil-clay-platelets', 0x7c4a24, { family: 'chitin', roughness: 0.98, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 130, 78, 34); i++) {
    const x = -1.35 + rand() * 2.70;
    const z = -0.55 + rand() * 1.25;
    const y = 1.27 + rand() * 0.18;
    const m = rand() > 0.45 ? sand : clay;
    const grain = ellipsoid(0.010 + rand() * 0.025, 0.006 + rand() * 0.012, 0.010 + rand() * 0.025, m, [x, y, z], 7);
    grain.rotation.set(rand() * Math.PI, rand() * Math.PI, rand() * Math.PI);
    g.add(grain);
  }
  addSpriteLabel(g, 'sand/silt/clay grains resolved', [0.65, 2.08, 0.94], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addFossilMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'fossil-scan-detail';
  const rand = seeded(`${seedKey}:fossil`);
  const mineral = makeScanMaterial('mineralized-fossil-pits', 0x78716c, { family: 'bone', roughness: 0.96, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 70, 42, 20); i++) {
    const a = rand() * Math.PI * 2;
    const r = 0.12 + rand() * 0.74;
    const pit = ellipsoid(0.012 + rand() * 0.018, 0.004, 0.010 + rand() * 0.015, mineral, [Math.cos(a) * r, 1.25 + rand() * 0.18, Math.sin(a) * r * 0.72], 7);
    pit.rotation.y = a;
    g.add(pit);
  }
  addSpriteLabel(g, 'mineral pits + chamber seams', [0.84, 2.22, 0.86], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addLabLiquidMicro(root, quality, seedKey, kind) {
  const g = new THREE.Group();
  g.name = 'lab-liquid-scan-detail';
  const rand = seeded(`${seedKey}:liquid:${kind}`);
  const bubble = makeScanMaterial('liquid-bubbles-meniscus', 0xdbeafe, { family: 'tissue', roughness: 0.18, opacity: 0.42, transparent: true, textureSize: 128 });
  const precip = makeScanMaterial('biochemical-precipitate', 0xfacc15, { family: 'bone', roughness: 0.78, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 48, 28, 14); i++) {
    const x = -1.05 + rand() * 2.10;
    const z = -0.38 + rand() * 0.76;
    const y = 1.02 + rand() * 0.70;
    g.add(sphere(0.010 + rand() * 0.018, rand() > 0.65 ? precip : bubble, [x, y, z], 8));
  }
  for (let i = 0; i < 3; i++) {
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.12 + i * 0.05, 0.0035, 5, 28), bubble);
    ring.position.set(-0.82 + i * 0.82, 1.25, 0);
    ring.rotation.x = Math.PI / 2;
    g.add(ring);
  }
  addSpriteLabel(g, 'meniscus, bubbles and precipitate', [0.80, 2.16, 0.86], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addFieldPlantMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'field-plant-scan-detail';
  const rand = seeded(`${seedKey}:field`);
  const blade = makeScanMaterial('field-grass-blades', 0x22c55e, { family: 'leaf', roughness: 0.70, textureSize: 128 });
  const flower = makeScanMaterial('tiny-field-flowers', 0xf472b6, { family: 'tissue', roughness: 0.55, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 96, 58, 24); i++) {
    const x = -2.10 + rand() * 4.20;
    const z = -1.35 + rand() * 2.70;
    const h = 0.08 + rand() * 0.22;
    g.add(cylBetween([x, 0.92, z], [x + (rand() - 0.5) * 0.05, 0.92 + h, z + (rand() - 0.5) * 0.05], 0.0035, blade, 4));
    if (rand() > 0.84) g.add(sphere(0.018 + rand() * 0.012, flower, [x, 0.96 + h, z], 8));
  }
  addSpriteLabel(g, 'individual leaves in quadrat', [1.05, 1.90, 0.96], { scale: 0.10, fontSize: 17 });
  root.add(g);
}
function addSpecimenShelfMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'specimen-shelf-scan-detail';
  const rand = seeded(`${seedKey}:specimen`);
  const biofilm = makeScanMaterial('preserved-specimen-biofilm', 0x84cc16, { family: 'leaf', roughness: 0.62, opacity: 0.75, transparent: true, textureSize: 128 });
  for (let jar = 0; jar < 6; jar++) {
    const x = -1.55 + jar * 0.62;
    for (let i = 0; i < qualityCount(quality, 16, 10, 5); i++) {
      g.add(sphere(0.006 + rand() * 0.012, biofilm, [x + (rand() - 0.5) * 0.28, 1.18 + rand() * 0.35, (rand() - 0.5) * 0.18], 7));
    }
  }
  addSpriteLabel(g, 'preserved specimen surface detail', [0.55, 2.18, 0.86], { scale: 0.10, fontSize: 17 });
  root.add(g);
}

function addHumanMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'human-scan-detail';
  const rand = seeded(`${seedKey}:human`);
  const capillary = makeScanMaterial('human-capillary-web', 0xe11d48, { family: 'tissue', roughness: 0.38, textureSize: 128 });
  const nerve = makeScanMaterial('human-nerve-filaments', 0xfacc15, { family: 'bone', roughness: 0.62, textureSize: 128 });
  const skinPore = makeScanMaterial('skin-pores', 0xe7a982, { family: 'tissue', roughness: 0.70, textureSize: 128 });
  for (let i = 0; i < qualityCount(quality, 46, 30, 14); i++) {
    const a = rand() * Math.PI * 2;
    const y = -1.9 + rand() * 5.4;
    const radius = y > 3.0 ? 0.55 : y > 0.2 ? 1.06 : 0.50;
    const x = Math.cos(a) * radius * (0.75 + rand() * 0.22);
    const z = Math.sin(a) * 0.26;
    const pore = ellipsoid(0.010 + rand() * 0.008, 0.004, 0.008 + rand() * 0.006, skinPore, [x, y, z], 7);
    pore.rotation.y = rand() * Math.PI;
    g.add(pore);
  }
  [-1, 1].forEach((side) => {
    for (let i = 0; i < 8; i++) {
      const y = 2.00 - i * 0.28;
      g.add(tube([[0.12 * side, y, 0.34], [0.34 * side, y - 0.08, 0.32], [0.62 * side, y - 0.18, 0.26]], 0.006, capillary, 16, 5));
      g.add(tube([[0.02 * side, y, -0.12], [0.28 * side, y - 0.16, -0.12], [0.66 * side, y - 0.26, -0.10]], 0.004, nerve, 16, 4));
    }
  });
  addSpriteLabel(g, 'skin pores, capillaries and nerves', [1.42, 3.30, 0.88], { scale: 0.11, fontSize: 18 });
  root.add(g);
}
function addHeartLungMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'heart-lung-scan-detail';
  const rand = seeded(`${seedKey}:heart-lung`);
  const capillary = makeScanMaterial('alveolar-capillary-net', 0xd946ef, { family: 'tissue', roughness: 0.42, textureSize: 128 });
  const alveolus = makeScanMaterial('alveoli-surface-pbr', 0xf7b2c4, { family: 'tissue', roughness: 0.48, opacity: 0.78, transparent: true, textureSize: 128 });
  [-1, 1].forEach((side) => {
    for (let i = 0; i < qualityCount(quality, 54, 34, 18); i++) {
      const a = rand() * Math.PI * 2;
      const r = 0.16 + rand() * 0.34;
      const y = -0.08 + rand() * 1.35;
      const p = [side * (0.92 + Math.cos(a) * r * 0.34), y, Math.sin(a) * r];
      g.add(sphere(0.018 + rand() * 0.012, alveolus, p, 8));
      if (i % 2 === 0) {
        g.add(tube([p, [p[0] + side * 0.07, p[1] + 0.04, p[2] + 0.05], [p[0] + side * 0.12, p[1] - 0.03, p[2] - 0.04]], 0.0035, capillary, 10, 4));
      }
    }
  });
  const coronary = makeScanMaterial('coronary-arteries', 0xef4444, { family: 'tissue', roughness: 0.36, textureSize: 128 });
  for (let i = 0; i < 7; i++) {
    const a = i / 7 * Math.PI * 2;
    g.add(tube([[0.20, 0.92, 0.22], [0.20 + Math.cos(a) * 0.23, 0.55 + Math.sin(a) * 0.16, 0.26], [0.20 + Math.cos(a) * 0.34, 0.22 + Math.sin(a) * 0.12, 0.20]], 0.006, coronary, 16, 5));
  }
  addSpriteLabel(g, 'alveoli + coronary vessels', [1.42, 2.36, 0.86], { scale: 0.11, fontSize: 18 });
  root.add(g);
}
function addButterflyMicro(root, quality, seedKey) {
  const g = new THREE.Group();
  g.name = 'butterfly-scan-detail';
  const rand = seeded(`${seedKey}:butterfly`);
  const scalePink = makeScanMaterial('butterfly-wing-scales-pink', 0xf472b6, { family: 'chitin', roughness: 0.58, textureSize: 128 });
  const scaleViolet = makeScanMaterial('butterfly-wing-scales-violet', 0xc084fc, { family: 'chitin', roughness: 0.58, textureSize: 128 });
  const seta = makeScanMaterial('caterpillar-setae', 0x111111, { family: 'chitin', roughness: 0.76, textureSize: 128 });
  [-1, 1].forEach((side) => {
    for (let i = 0; i < qualityCount(quality, 120, 72, 32); i++) {
      const upper = rand() > 0.42;
      const x = side * (0.14 + rand() * 1.15);
      const y = upper ? 0.23 + rand() * 0.56 : -0.36 + rand() * 0.30;
      const z = 0.030 + rand() * 0.018;
      const sc = ellipsoid(0.022 + rand() * 0.014, 0.005, 0.010 + rand() * 0.010, upper ? scalePink : scaleViolet, [x, 1.19 + y, z], 7);
      sc.rotation.z = side * 0.25 + (rand() - 0.5) * 0.45;
      g.add(sc);
    }
  });
  for (let i = 0; i < qualityCount(quality, 42, 24, 10); i++) {
    const x = -1.10 + rand() * 2.6;
    const y = 1.02 + rand() * 0.22;
    const z = (rand() - 0.5) * 0.22;
    g.add(cylBetween([x, y, z], [x + (rand() - 0.5) * 0.05, y + 0.08 + rand() * 0.06, z + (rand() - 0.5) * 0.04], 0.0035, seta, 4));
  }
  addSpriteLabel(g, 'individual wing scales + larval setae', [0.60, 2.45, 0.88], { scale: 0.11, fontSize: 18 });
  root.add(g);
}

export function addSpecimenMicroDetails(root, opts = {}) {
  const kind = opts.kind || 'biology';
  const seedKey = opts.seed || kind;
  const quality = opts.quality || { tier: 'medium' };
  if (['humanBody'].includes(kind)) addHumanMicro(root, quality, seedKey);
  else if (['heartLungs'].includes(kind)) addHeartLungMicro(root, quality, seedKey);
  else if (['butterflyLifeCycle'].includes(kind)) addButterflyMicro(root, quality, seedKey);
  else if (['cockroach'].includes(kind)) addCockroachMicro(root, quality, seedKey);
  else if (['flower', 'inflorescence'].includes(kind)) addFlowerMicro(root, quality, seedKey);
  else if (['herbarium', 'photosynthesis', 'stomata', 'plasmolysis', 'transpiration', 'suction', 'phototropism', 'apicalBud'].includes(kind)) addLeafMicro(root, quality, seedKey, kind === 'photosynthesis' ? 0.45 : 1.15);
  else if (kind === 'mushroom') addMushroomMicro(root, quality, seedKey);
  else if (['skeleton', 'skeletonHealth'].includes(kind)) addSkeletonMicro(root, quality, seedKey);
  else if (['microscope', 'mitosis', 'animalMitosis', 'animalTissue', 'anatomyTS', 'frogDev', 'microscopeParts'].includes(kind)) addMicrographDetails(root, quality, seedKey, kind);
  else if (['pond', 'pondZoo', 'culture', 'biofertilizer'].includes(kind)) addPondMicro(root, quality, seedKey);
  else if (['animals', 'dissection'].includes(kind)) addAnimalMicro(root, quality, seedKey);
  else if (['genetics', 'imbibition'].includes(kind)) addSeedMicro(root, quality, seedKey);
  else if (kind === 'soil') addSoilMicro(root, quality, seedKey);
  else if (kind === 'fossil') addFossilMicro(root, quality, seedKey);
  else if (['osmosis', 'respiration', 'anaerobic', 'amylase', 'bloodSugar', 'starchTest', 'proteinTest', 'urine'].includes(kind)) addLabLiquidMicro(root, quality, seedKey, kind);
  else if (['quadrat', 'quadrat2', 'conservation'].includes(kind)) addFieldPlantMicro(root, quality, seedKey);
  else if (kind === 'specimens') addSpecimenShelfMicro(root, quality, seedKey);
  else addFieldPlantMicro(root, quality, seedKey);
}
export function addScanGradeEnhancement(root, opts = {}) {
  const quality = opts.quality || { tier: 'medium' };
  const seed = opts.seed || opts.kind || 'biology';
  upgradeSceneMaterials(root, { seed, textureSize: quality.tier === 'low' ? 128 : 256 });
  applyOrganicDisplacement(root, { seed, kind: opts.kind, intensity: quality.tier === 'low' ? 0.008 : quality.tier === 'medium' ? 0.014 : 0.020, frequency: opts.frequency || 1.28 });
  addSpecimenMicroDetails(root, { kind: opts.kind, seed, state: opts.state, quality });
  if (opts.plaque !== false) addScanPlaque(root, opts.kind || 'biology');
  return root;
}
export function disposeScanGradeAssets() {
  MATERIAL_CACHE.forEach((m) => m.dispose());
  MATERIAL_CACHE.clear();
  TEXTURE_CACHE.forEach((t) => t.dispose());
  TEXTURE_CACHE.clear();
}
