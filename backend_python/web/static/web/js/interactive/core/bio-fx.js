import { THREE } from './engine.js';

// Shared biology FX toolkit: cached soft-glow textures, pooled GPU particle
// systems, gradient sky domes and image-based environment lighting.
// Everything is preallocated, cached and disposed cleanly per simulation.

const TEX_CACHE = new Map();

function makeCanvas(size) {
  const c = document.createElement('canvas');
  c.width = size;
  c.height = size;
  return c;
}

export function glowTexture(key = 'soft', opts = {}) {
  const size = opts.size || 128;
  const ck = `glow:${key}:${size}`;
  if (TEX_CACHE.has(ck)) return TEX_CACHE.get(ck);
  const c = makeCanvas(size);
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  g.addColorStop(0, opts.inner || 'rgba(255,255,255,1)');
  g.addColorStop(0.4, opts.mid || 'rgba(255,255,255,0.55)');
  g.addColorStop(1, opts.outer || 'rgba(255,255,255,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(c);
  if (THREE.SRGBColorSpace) tex.colorSpace = THREE.SRGBColorSpace;
  TEX_CACHE.set(ck, tex);
  return tex;
}

export function cellTexture(opts = {}) {
  const size = opts.size || 96;
  const ck = `cell:${opts.center || '#7a0e12'}:${opts.edge || '#ff4d4d'}:${size}`;
  if (TEX_CACHE.has(ck)) return TEX_CACHE.get(ck);
  const c = makeCanvas(size);
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(size / 2, size / 2, size * 0.05, size / 2, size / 2, size / 2);
  g.addColorStop(0, opts.center || '#7a0e12');
  g.addColorStop(0.55, opts.mid || opts.edge || '#ff4d4d');
  g.addColorStop(0.85, opts.edge || '#ff4d4d');
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
  ctx.fill();
  const tex = new THREE.CanvasTexture(c);
  if (THREE.SRGBColorSpace) tex.colorSpace = THREE.SRGBColorSpace;
  TEX_CACHE.set(ck, tex);
  return tex;
}

export function moleculeTexture(label, colorCss, opts = {}) {
  const size = opts.size || 128;
  const ck = `mol:${label}:${colorCss}:${size}`;
  if (TEX_CACHE.has(ck)) return TEX_CACHE.get(ck);
  const c = makeCanvas(size);
  const ctx = c.getContext('2d');
  const cx = size / 2;
  const cy = size / 2;
  const r = size * 0.42;
  const glow = ctx.createRadialGradient(cx, cy, r * 0.2, cx, cy, r);
  glow.addColorStop(0, colorCss + 'cc');
  glow.addColorStop(0.75, colorCss + '55');
  glow.addColorStop(1, colorCss + '00');
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, size, size);
  ctx.beginPath();
  ctx.arc(cx, cy, r * 0.72, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(8,14,22,0.78)';
  ctx.fill();
  ctx.lineWidth = Math.max(2, size * 0.03);
  ctx.strokeStyle = colorCss;
  ctx.stroke();
  ctx.fillStyle = '#ffffff';
  ctx.font = `700 ${Math.round(size * (opts.fontScale || 0.30))}px Poppins, system-ui, sans-serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(label, cx, cy + size * 0.01);
  const tex = new THREE.CanvasTexture(c);
  if (THREE.SRGBColorSpace) tex.colorSpace = THREE.SRGBColorSpace;
  TEX_CACHE.set(ck, tex);
  return tex;
}

export function ringTexture(colorCss = '#ffffff', size = 128) {
  const ck = `ring:${colorCss}:${size}`;
  if (TEX_CACHE.has(ck)) return TEX_CACHE.get(ck);
  const c = makeCanvas(size);
  const ctx = c.getContext('2d');
  ctx.strokeStyle = colorCss;
  ctx.lineWidth = size * 0.06;
  ctx.beginPath();
  ctx.arc(size / 2, size / 2, size * 0.40, 0, Math.PI * 2);
  ctx.stroke();
  ctx.strokeStyle = colorCss + '66';
  ctx.lineWidth = size * 0.02;
  ctx.beginPath();
  ctx.arc(size / 2, size / 2, size * 0.46, 0, Math.PI * 2);
  ctx.stroke();
  const tex = new THREE.CanvasTexture(c);
  if (THREE.SRGBColorSpace) tex.colorSpace = THREE.SRGBColorSpace;
  TEX_CACHE.set(ck, tex);
  return tex;
}

export function shaftTexture(colorCss = 'rgba(255,236,170,', size = 128) {
  const ck = `shaft:${colorCss}:${size}`;
  if (TEX_CACHE.has(ck)) return TEX_CACHE.get(ck);
  const c = makeCanvas(size);
  const ctx = c.getContext('2d');
  const g = ctx.createLinearGradient(0, 0, 0, size);
  g.addColorStop(0, colorCss + '0.85)');
  g.addColorStop(0.55, colorCss + '0.28)');
  g.addColorStop(1, colorCss + '0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, size, size);
  const h = ctx.createLinearGradient(0, 0, size, 0);
  h.addColorStop(0, 'rgba(0,0,0,1)');
  h.addColorStop(0.25, 'rgba(0,0,0,0)');
  h.addColorStop(0.75, 'rgba(0,0,0,0)');
  h.addColorStop(1, 'rgba(0,0,0,1)');
  ctx.globalCompositeOperation = 'destination-out';
  ctx.fillStyle = h;
  ctx.fillRect(0, 0, size, size);
  ctx.globalCompositeOperation = 'source-over';
  const tex = new THREE.CanvasTexture(c);
  if (THREE.SRGBColorSpace) tex.colorSpace = THREE.SRGBColorSpace;
  TEX_CACHE.set(ck, tex);
  return tex;
}

// Pooled round-sprite particle system. One draw call per pool; colours fade by
// scaling toward black which reads as alpha under AdditiveBlending.
export class Particles {
  constructor(parent, opts = {}) {
    this.max = opts.max || 160;
    this.pos = new Float32Array(this.max * 3);
    this.vel = new Float32Array(this.max * 3);
    this.col = new Float32Array(this.max * 3);
    this.base = new Float32Array(this.max * 3);
    this.life = new Float32Array(this.max);
    this.decay = new Float32Array(this.max);
    this.count = 0;
    this.geo = new THREE.BufferGeometry();
    this.geo.setAttribute('position', new THREE.BufferAttribute(this.pos, 3));
    this.geo.setAttribute('color', new THREE.BufferAttribute(this.col, 3));
    this.mat = new THREE.PointsMaterial({
      size: opts.size || 0.4,
      map: opts.texture || glowTexture(),
      vertexColors: true,
      transparent: true,
      opacity: opts.opacity ?? 1,
      depthWrite: false,
      blending: opts.blending ?? THREE.AdditiveBlending,
      sizeAttenuation: true,
    });
    this.mat.userData.sharedFx = true;
    this.points = new THREE.Points(this.geo, this.mat);
    this.points.frustumCulled = false;
    this.points.renderOrder = opts.renderOrder || 5;
    parent.add(this.points);
    this.onUpdate = null;
  }
  spawn(x, y, z, vx, vy, vz, lifeSeconds, color) {
    if (this.count >= this.max) return;
    const i = this.count++;
    this.pos[i * 3] = x; this.pos[i * 3 + 1] = y; this.pos[i * 3 + 2] = z;
    this.vel[i * 3] = vx; this.vel[i * 3 + 1] = vy; this.vel[i * 3 + 2] = vz;
    this.life[i] = 1;
    this.decay[i] = 1 / Math.max(0.05, lifeSeconds);
    const c = color || WHITE;
    this.base[i * 3] = c.r; this.base[i * 3 + 1] = c.g; this.base[i * 3 + 2] = c.b;
    this.col[i * 3] = c.r; this.col[i * 3 + 1] = c.g; this.col[i * 3 + 2] = c.b;
  }
  update(dt, time) {
    let w = 0;
    for (let i = 0; i < this.count; i++) {
      this.life[i] -= this.decay[i] * dt;
      if (this.life[i] <= 0) continue;
      if (this.onUpdate) this.onUpdate(i, dt, time, this.life[i]);
      this.pos[i * 3] += this.vel[i * 3] * dt;
      this.pos[i * 3 + 1] += this.vel[i * 3 + 1] * dt;
      this.pos[i * 3 + 2] += this.vel[i * 3 + 2] * dt;
      const f = this.life[i];
      this.col[w * 3] = this.base[i * 3] * f;
      this.col[w * 3 + 1] = this.base[i * 3 + 1] * f;
      this.col[w * 3 + 2] = this.base[i * 3 + 2] * f;
      if (w !== i) {
        this.pos[w * 3] = this.pos[i * 3]; this.pos[w * 3 + 1] = this.pos[i * 3 + 1]; this.pos[w * 3 + 2] = this.pos[i * 3 + 2];
        this.vel[w * 3] = this.vel[i * 3]; this.vel[w * 3 + 1] = this.vel[i * 3 + 1]; this.vel[w * 3 + 2] = this.vel[i * 3 + 2];
        this.life[w] = this.life[i]; this.decay[w] = this.decay[i];
        this.base[w * 3] = this.base[i * 3]; this.base[w * 3 + 1] = this.base[i * 3 + 1]; this.base[w * 3 + 2] = this.base[i * 3 + 2];
      }
      w++;
    }
    this.count = w;
    this.geo.setDrawRange(0, w);
    this.geo.attributes.position.needsUpdate = true;
    this.geo.attributes.color.needsUpdate = true;
  }
  clear() { this.count = 0; this.geo.setDrawRange(0, 0); }
  dispose() {
    this.geo.dispose();
    this.mat.dispose();
    if (this.points.parent) this.points.parent.remove(this.points);
  }
}

const WHITE = new THREE.Color(0xffffff);

// Vertical-gradient sky dome (BackSide sphere, vertex colours — one draw call).
export function skyDome(scene, opts = {}) {
  const radius = opts.radius || 70;
  const geo = new THREE.SphereGeometry(radius, 24, 18);
  const top = new THREE.Color(opts.top ?? 0x0d2b3e);
  const mid = new THREE.Color(opts.mid ?? opts.top ?? 0x123a2c);
  const bottom = new THREE.Color(opts.bottom ?? 0x05080c);
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  const tmp = new THREE.Color();
  for (let i = 0; i < pos.count; i++) {
    const t = Math.max(-1, Math.min(1, pos.getY(i) / radius));
    if (t >= 0) tmp.copy(mid).lerp(top, Math.pow(t, 0.8));
    else tmp.copy(mid).lerp(bottom, Math.pow(-t, 0.7));
    colors[i * 3] = tmp.r; colors[i * 3 + 1] = tmp.g; colors[i * 3 + 2] = tmp.b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false, depthWrite: false });
  mat.userData.sharedFx = true;
  const mesh = new THREE.Mesh(geo, mat);
  mesh.renderOrder = -10;
  scene.add(mesh);
  return mesh;
}

// Cheap image-based lighting: tiny equirect gradient run through PMREM so
// MeshStandard/Physical materials get believable ambient reflections.
export function applyEnvironmentLighting(renderer, scene, opts = {}) {
  try {
    const c = document.createElement('canvas');
    c.width = 64; c.height = 32;
    const ctx = c.getContext('2d');
    const g = ctx.createLinearGradient(0, 0, 0, 32);
    g.addColorStop(0, opts.sky || '#cfe8ff');
    g.addColorStop(0.55, opts.horizon || '#8fae9b');
    g.addColorStop(1, opts.ground || '#241a12');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 64, 32);
    const eq = new THREE.CanvasTexture(c);
    eq.mapping = THREE.EquirectangularReflectionMapping;
    if (THREE.SRGBColorSpace) eq.colorSpace = THREE.SRGBColorSpace;
    const pmrem = new THREE.PMREMGenerator(renderer);
    const rt = pmrem.fromEquirectangular(eq);
    scene.environment = rt.texture;
    eq.dispose();
    pmrem.dispose();
    return () => {
      if (scene.environment === rt.texture) scene.environment = null;
      rt.dispose();
    };
  } catch (e) {
    return () => {};
  }
}

// Volumetric-style sun shafts: crossed additive gradient planes.
export function lightShafts(scene, opts = {}) {
  const group = new THREE.Group();
  const tex = shaftTexture(opts.colorCss || 'rgba(255,236,170,');
  const count = opts.count || 5;
  const height = opts.height || 16;
  const width = opts.width || 3.2;
  const mat = new THREE.MeshBasicMaterial({
    map: tex, transparent: true, opacity: opts.opacity ?? 0.35,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, fog: false,
  });
  mat.userData.sharedFx = true;
  for (let i = 0; i < count; i++) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(width * (0.6 + (i % 3) * 0.35), height), mat);
    const a = (i / count) * Math.PI;
    p.position.set(Math.cos(a) * 1.2, height * 0.34, Math.sin(a) * 1.2);
    p.rotation.y = a;
    p.rotation.z = 0.10 + (i % 2) * 0.06;
    group.add(p);
  }
  group.userData.material = mat;
  scene.add(group);
  return group;
}

export function disposeCachedTextures() {
  TEX_CACHE.forEach((t) => t.dispose());
  TEX_CACHE.clear();
}
