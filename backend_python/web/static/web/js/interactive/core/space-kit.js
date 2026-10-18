// The space kit: every body in the space lessons drawn from one procedural model, so the Earth
// in "Tour the Solar System" is the Earth in "Phases of the Moon". Surfaces are fractal noise
// sampled on the sphere itself (no seam at the date line, no pinching at the poles), coloured by
// what each world is actually made of: Earth's oceans, continents, deserts and ice caps under
// a separate drifting cloud deck; the Moon's maria and craters; Mars's dark plains and polar
// cap; the belts and the Great Red Spot of Jupiter; Saturn's pale bands and its ring system
// with the Cassini division. Atmospheres are a fresnel rim shader, the Sun a granulated disc
// with a layered corona, the sky a starfield with the Milky Way across it. Textures are drawn
// once per page at a size that suits the device and shared by every sim that asks.
import { THREE } from './engine.js';

// ---- noise -----------------------------------------------------------------------------------
const P = new Uint8Array(512);
(function seedPerm() {
  const p = new Uint8Array(256); for (let i = 0; i < 256; i++) p[i] = i;
  let s = 1337; for (let i = 255; i > 0; i--) { s = (s * 16807) % 2147483647; const j = s % (i + 1); const t = p[i]; p[i] = p[j]; p[j] = t; }
  for (let i = 0; i < 512; i++) P[i] = p[i & 255];
})();
const fade = (t) => t * t * t * (t * (t * 6 - 15) + 10);
const lerp = (a, b, t) => a + (b - a) * t;
function grad(h, x, y, z) { const u = h < 8 ? x : y; const v = h < 4 ? y : h === 12 || h === 14 ? x : z; return ((h & 1) ? -u : u) + ((h & 2) ? -v : v); }
export function noise3(x, y, z) {
  const X = Math.floor(x) & 255, Y = Math.floor(y) & 255, Z = Math.floor(z) & 255;
  x -= Math.floor(x); y -= Math.floor(y); z -= Math.floor(z);
  const u = fade(x), v = fade(y), w = fade(z);
  const A = P[X] + Y, AA = P[A] + Z, AB = P[A + 1] + Z, B = P[X + 1] + Y, BA = P[B] + Z, BB = P[B + 1] + Z;
  return lerp(lerp(lerp(grad(P[AA] & 15, x, y, z), grad(P[BA] & 15, x - 1, y, z), u), lerp(grad(P[AB] & 15, x, y - 1, z), grad(P[BB] & 15, x - 1, y - 1, z), u), v),
    lerp(lerp(grad(P[AA + 1] & 15, x, y, z - 1), grad(P[BA + 1] & 15, x - 1, y, z - 1), u), lerp(grad(P[AB + 1] & 15, x, y - 1, z - 1), grad(P[BB + 1] & 15, x - 1, y - 1, z - 1), u), v), w);
}
export function fbm(x, y, z, oct = 5, lac = 2.0, gain = 0.5) {
  let a = 0.5, f = 1, s = 0;
  for (let i = 0; i < oct; i++) { s += a * noise3(x * f, y * f, z * f); f *= lac; a *= gain; }
  return s;
}

// ---- equirect painter -------------------------------------------------------------------------
const CACHE = new Map();
export function textureSize(quality) { return quality && quality.tier === 'low' ? 256 : 512; }

/** Paints an equirect texture by calling shade(x, y, z, lat) for each texel's point on the unit sphere. */
function paint(key, W, shade, { alpha = false } = {}) {
  const ck = `${key}:${W}`;
  if (CACHE.has(ck)) return CACHE.get(ck);
  const H = W >> 1;
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d');
  const img = g.createImageData(W, H); const d = img.data;
  const out = [0, 0, 0, 255];
  for (let j = 0; j < H; j++) {
    const lat = (0.5 - (j + 0.5) / H) * Math.PI;
    const cl = Math.cos(lat), sl = Math.sin(lat);
    for (let i = 0; i < W; i++) {
      const lon = ((i + 0.5) / W) * Math.PI * 2;
      shade(cl * Math.cos(lon), sl, cl * Math.sin(lon), lat, out);
      const p = (j * W + i) * 4;
      d[p] = out[0]; d[p + 1] = out[1]; d[p + 2] = out[2]; d[p + 3] = alpha ? out[3] : 255;
    }
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  if (t.colorSpace !== undefined && !key.endsWith('bump')) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  t.userData = { sharedFx: true };
  CACHE.set(ck, t);
  return t;
}
function mix3(a, b, t, out) { out[0] = a[0] + (b[0] - a[0]) * t; out[1] = a[1] + (b[1] - a[1]) * t; out[2] = a[2] + (b[2] - a[2]) * t; return out; }
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

// ---- the bodies ---------------------------------------------------------------------------
const SHADERS = {
  earth(x, y, z, lat, o) {
    const h = fbm(x * 1.6 + 3, y * 1.6, z * 1.6, 6) + 0.12 * fbm(x * 6, y * 6, z * 6, 3);
    const polar = Math.abs(lat) / (Math.PI / 2);
    if (polar > 0.86 + h * 0.15) { o[0] = 236; o[1] = 242; o[2] = 248; return; }
    if (h < 0.04) {
      // ocean: deeper water darker, a turquoise shelf near the coast
      const t = clamp01((h + 0.35) / 0.39);
      mix3([12, 38, 92], t > 0.85 ? [38, 116, 160] : [22, 74, 140], t > 0.85 ? (t - 0.85) / 0.15 : t, o);
      return;
    }
    const m = fbm(x * 3 + 9, y * 3, z * 3, 4); // moisture
    const dry = clamp01(0.5 - m * 1.6 - (Math.abs(Math.abs(lat) - 0.42) < 0.18 ? 0.25 : 0));
    const cold = clamp01((polar - 0.55) / 0.3);
    const forest = [52, 96, 48], savanna = [148, 140, 82], desert = [204, 176, 120], tundra = [128, 124, 108], peak = [200, 196, 190];
    mix3(forest, dry > 0.55 ? desert : savanna, dry > 0.55 ? (dry - 0.55) / 0.45 : dry / 0.55, o);
    if (cold > 0) mix3(o, tundra, cold, o);
    if (h > 0.34) mix3(o, peak, clamp01((h - 0.34) / 0.12), o);
  },
  earthClouds(x, y, z, lat, o) {
    const c = fbm(x * 2.4 + 20, y * 3.2, z * 2.4, 6) + 0.3 * fbm(x * 9, y * 9, z * 9, 2);
    const band = 0.12 * Math.cos(lat * 6);
    const a = clamp01((c + band - 0.02) * 2.4);
    o[0] = 255; o[1] = 255; o[2] = 255; o[3] = a * 235;
  },
  moon(x, y, z, lat, o) {
    const h = fbm(x * 2.2, y * 2.2, z * 2.2, 5);
    const mare = clamp01((fbm(x * 1.1 + 5, y * 1.1, z * 1.1, 3) + 0.05) * 3);
    let v = 150 + h * 70 - mare * 55;
    v += crater(x, y, z, 7, 0.12) * 60;
    o[0] = v; o[1] = v * 0.98; o[2] = v * 0.95;
  },
  mercury(x, y, z, lat, o) {
    let v = 128 + fbm(x * 2.5, y * 2.5, z * 2.5, 5) * 70 + crater(x, y, z, 9, 0.1) * 55;
    o[0] = v * 1.02; o[1] = v * 0.96; o[2] = v * 0.9;
  },
  venus(x, y, z, lat, o) {
    const w = fbm(x * 1.5, y * 4, z * 1.5, 5);
    const v = fbm(x * 2 + w * 2, y * 6, z * 2 + w * 2, 5);
    mix3([214, 178, 120], [244, 222, 176], clamp01(v + 0.55), o);
  },
  mars(x, y, z, lat, o) {
    const h = fbm(x * 2, y * 2, z * 2, 6);
    const dark = clamp01((fbm(x * 1.3 + 7, y * 1.3, z * 1.3, 4) + 0.05) * 2.5);
    mix3([196, 98, 54], [120, 62, 40], dark, o);
    mix3(o, [226, 150, 100], clamp01(h * 1.4), o);
    if (Math.abs(lat) > 1.32 + h * 0.1) { o[0] = 236; o[1] = 230; o[2] = 222; }
    const cr = crater(x, y, z, 6, 0.08); o[0] += cr * 30; o[1] += cr * 22; o[2] += cr * 18;
  },
  jupiter(x, y, z, lat, o) {
    const turb = fbm(x * 3, y * 3, z * 3, 5) * 0.35;
    const b = Math.sin((lat + turb * 0.25) * 22);
    const palette = [[236, 222, 196], [196, 150, 108], [168, 116, 78], [226, 204, 170]];
    const k = (b + 1) / 2;
    mix3(palette[0], palette[1], k, o);
    if (Math.abs(lat) > 0.95) mix3(o, [150, 132, 118], clamp01((Math.abs(lat) - 0.95) * 2), o);
    // the Great Red Spot, 22 degrees south, stretched along the bands
    const lon = Math.atan2(z, x);
    const dl = (lon - 1.1), dt = (lat + 0.38);
    const spot = Math.exp(-(dl * dl * 26 + dt * dt * 180));
    mix3(o, [186, 92, 64], clamp01(spot * 1.4), o);
  },
  saturn(x, y, z, lat, o) {
    const turb = fbm(x * 2, y * 2, z * 2, 4) * 0.2;
    const b = Math.sin((lat + turb * 0.2) * 18);
    mix3([234, 216, 170], [204, 176, 124], (b + 1) / 2, o);
    if (Math.abs(lat) > 1.2) mix3(o, [176, 170, 150], 0.5, o);
  },
  uranus(x, y, z, lat, o) { const b = Math.sin(lat * 10) * 0.5 + fbm(x * 2, y * 2, z * 2, 3) * 0.3; mix3([160, 218, 226], [126, 196, 210], clamp01(b + 0.5), o); },
  neptune(x, y, z, lat, o) {
    const b = Math.sin((lat + fbm(x * 2, y * 2, z * 2, 4) * 0.1) * 14);
    mix3([52, 86, 206], [34, 62, 170], (b + 1) / 2, o);
    const lon = Math.atan2(z, x); const dl = lon + 0.6, dt = lat + 0.35;
    mix3(o, [18, 30, 96], clamp01(Math.exp(-(dl * dl * 30 + dt * dt * 160)) * 1.3), o);
  },
  sun(x, y, z, lat, o) {
    const g = fbm(x * 9, y * 9, z * 9, 4) + 0.4 * fbm(x * 30, y * 30, z * 30, 2);
    mix3([255, 170, 60], [255, 236, 170], clamp01(g * 0.9 + 0.55), o);
  },
};
function crater(x, y, z, freq, size) {
  // cellular craters: bright rims, dark floors, a few per cell
  const fx = x * freq, fy = y * freq, fz = z * freq;
  const ix = Math.floor(fx), iy = Math.floor(fy), iz = Math.floor(fz);
  let v = 0;
  for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) for (let dz = -1; dz <= 1; dz++) {
    const cx = ix + dx, cy = iy + dy, cz = iz + dz;
    const hsh = P[(P[(P[cx & 255] + cy) & 255] + cz) & 255];
    if (hsh % 3) continue;
    const px = cx + (hsh / 255), py = cy + (P[hsh] / 255), pz = cz + (P[(hsh + 7) & 255] / 255);
    const r = (0.2 + (P[(hsh + 3) & 255] / 255) * 0.5) * size * freq;
    const dist = Math.hypot(fx - px, fy - py, fz - pz) / r;
    if (dist < 1) v -= 0.6 * (1 - dist * dist);
    else if (dist < 1.25) v += 0.8 * (1 - (dist - 1) / 0.25);
  }
  return v;
}

export function surfaceTexture(name, quality) {
  // Earth is the world students look at closest, so it gets twice the detail on capable devices
  const W = textureSize(quality) * ((name === 'earth' || name === 'earthClouds') && quality && quality.tier === 'high' ? 2 : 1);
  const shade = SHADERS[name];
  if (!shade) return null;
  return paint(name, name === 'earthClouds' ? W : W, shade, { alpha: name === 'earthClouds' });
}

/** A material for a body: its surface map, and on capable devices a bump map from the same noise. */
export function bodyMaterial(name, quality, opts = {}) {
  const map = surfaceTexture(name, quality);
  if (name === 'sun') return new THREE.MeshBasicMaterial({ map, toneMapped: false });
  const m = new THREE.MeshStandardMaterial({ map, roughness: name === 'earth' ? 0.72 : 0.92, metalness: 0 });
  if (quality && quality.tier !== 'low' && (name === 'moon' || name === 'mercury' || name === 'mars' || name === 'earth')) {
    m.bumpMap = map; m.bumpScale = name === 'earth' ? 0.015 : 0.03;
  }
  if (opts.emissiveNight) { m.emissive = new THREE.Color(0x000000); }
  return m;
}

const SEG = (q) => (q && q.tier === 'low' ? 32 : q && q.tier === 'medium' ? 48 : 72);
export function body(name, radius, quality) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(radius, SEG(quality), SEG(quality) >> 1), bodyMaterial(name, quality));
  m.name = name;
  return m;
}

export function earthWithClouds(radius, quality) {
  const earth = body('earth', radius, quality);
  const clouds = new THREE.Mesh(new THREE.SphereGeometry(radius * 1.012, SEG(quality), SEG(quality) >> 1), new THREE.MeshStandardMaterial({ map: surfaceTexture('earthClouds', quality), transparent: true, depthWrite: false, roughness: 1 }));
  clouds.name = 'clouds';
  earth.add(clouds);
  earth.add(atmosphere(radius, 0x6fb7ff, 1.12, 3.2));
  earth.userData.clouds = clouds;
  return earth;
}

/** A fresnel rim: transparent face-on, glowing at the limb, like a real atmosphere seen from space. */
export function atmosphere(radius, color = 0x6fb7ff, scale = 1.1, power = 3.0, intensity = 1.0) {
  const mat = new THREE.ShaderMaterial({
    uniforms: { c: { value: new THREE.Color(color) }, p: { value: power }, k: { value: intensity } },
    vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }',
    fragmentShader: 'uniform vec3 c; uniform float p; uniform float k; varying vec3 vN; varying vec3 vV; void main(){ float f = pow(1.0 - abs(dot(vN, vV)), p); gl_FragColor = vec4(c, f * k); }',
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.FrontSide,
  });
  const m = new THREE.Mesh(new THREE.SphereGeometry(radius * scale, 48, 24), mat);
  m.name = 'atmosphere';
  return m;
}

// ---- the Sun ---------------------------------------------------------------------------------
let GLOW = null;
export function glowTexture() {
  if (GLOW) return GLOW;
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d'); const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.18, 'rgba(255,244,214,0.85)'); gr.addColorStop(0.42, 'rgba(255,190,90,0.28)'); gr.addColorStop(1, 'rgba(255,140,40,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  GLOW = new THREE.CanvasTexture(c); if (GLOW.colorSpace !== undefined) GLOW.colorSpace = THREE.SRGBColorSpace; GLOW.userData = { sharedFx: true };
  return GLOW;
}
export function sun(radius, quality) {
  const s = body('sun', radius, quality);
  const layers = quality && quality.tier === 'low' ? [[3.2, 0.9]] : [[2.6, 0.95], [5.0, 0.5], [9.0, 0.18]];
  for (const [k, op] of layers) {
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTexture(), color: 0xffd28a, transparent: true, opacity: op, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }));
    sp.scale.setScalar(radius * k);
    s.add(sp);
  }
  return s;
}

// ---- rings ------------------------------------------------------------------------------------
export function saturnRings(inner, outer) {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 8;
  const g = c.getContext('2d');
  for (let i = 0; i < 1024; i++) {
    const r = i / 1023;
    let a = 0.55 + 0.35 * Math.sin(r * 90) * Math.sin(r * 23) + (Math.random() - 0.5) * 0.25;
    if (r > 0.62 && r < 0.68) a *= 0.08; // Cassini division
    if (r < 0.12) a *= r / 0.12 * 0.4; // faint C ring
    if (r > 0.96) a *= (1 - r) / 0.04;
    const b = 200 + 40 * Math.sin(r * 31);
    g.fillStyle = `rgba(${b},${b * 0.9 | 0},${b * 0.72 | 0},${clamp01(a).toFixed(3)})`;
    g.fillRect(i, 0, 1, 8);
  }
  const tex = new THREE.CanvasTexture(c); if (tex.colorSpace !== undefined) tex.colorSpace = THREE.SRGBColorSpace;
  const geo = new THREE.RingGeometry(inner, outer, 128, 1);
  // map u to the radius so the texture runs across the rings, not around them
  const pos = geo.attributes.position; const uv = geo.attributes.uv; const v = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) { v.fromBufferAttribute(pos, i); uv.setXY(i, (v.length() - inner) / (outer - inner), 0.5); }
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex, color: 0xe8e2d4, transparent: true, side: THREE.DoubleSide, depthWrite: false }));
  m.rotation.x = -Math.PI / 2;
  return m;
}

// ---- the sky ------------------------------------------------------------------------------
/** Stars of real colours and brightnesses, with the band of the Milky Way across the sky. */
export function starfield(quality, radius = 1500) {
  const n = quality && quality.tier === 'low' ? 1800 : quality && quality.tier === 'medium' ? 5000 : 9000;
  const pos = new Float32Array(n * 3), col = new Float32Array(n * 3), size = new Float32Array(n);
  const tints = [[0.62, 0.72, 1], [0.86, 0.9, 1], [1, 1, 1], [1, 0.95, 0.82], [1, 0.82, 0.62]];
  const tilt = new THREE.Matrix4().makeRotationX(1.05).multiply(new THREE.Matrix4().makeRotationZ(0.4));
  const v = new THREE.Vector3();
  for (let i = 0; i < n; i++) {
    const band = i < n * 0.55;
    const th = Math.random() * Math.PI * 2;
    const y = band ? (Math.random() + Math.random() + Math.random() - 1.5) * 0.18 : Math.random() * 2 - 1;
    const r = Math.sqrt(1 - y * y);
    v.set(r * Math.cos(th), y, r * Math.sin(th));
    if (band) v.applyMatrix4(tilt);
    v.multiplyScalar(radius);
    pos[i * 3] = v.x; pos[i * 3 + 1] = v.y; pos[i * 3 + 2] = v.z;
    const t = tints[(Math.random() * tints.length) | 0];
    const b = band ? 0.45 + Math.random() * 0.4 : 0.6 + Math.random() * 0.4;
    col[i * 3] = t[0] * b; col[i * 3 + 1] = t[1] * b; col[i * 3 + 2] = t[2] * b;
    size[i] = Math.pow(Math.random(), 6) * 5 + (band ? 0.8 : 1.1);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.setAttribute('size', new THREE.BufferAttribute(size, 1));
  const m = new THREE.ShaderMaterial({
    uniforms: { pr: { value: Math.min(window.devicePixelRatio || 1, 2) } },
    vertexShader: 'attribute float size; varying vec3 vC; uniform float pr; void main(){ vC = color; vec4 mv = modelViewMatrix*vec4(position,1.0); gl_PointSize = size*pr; gl_Position = projectionMatrix*mv; }',
    fragmentShader: 'varying vec3 vC; void main(){ vec2 d = gl_PointCoord-0.5; float r = length(d); float a = smoothstep(0.5,0.0,r); gl_FragColor = vec4(vC, a); }',
    vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  const pts = new THREE.Points(g, m);
  pts.frustumCulled = false;
  pts.renderOrder = -10;
  pts.name = 'starfield';
  return pts;
}
