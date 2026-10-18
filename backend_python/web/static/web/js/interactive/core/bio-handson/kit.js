// Shared building blocks for the hands-on biology practicals: easing curves, critically damped
// springs, a tiny tween runner, seeded randomness, cached canvas textures and the wet, waxy,
// steel and glass materials the specimens and instruments are made of.
import { THREE } from '../engine.js';

export const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
export const lerp = (a, b, t) => a + (b - a) * t;
export const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
export const ease = {
  inOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  out: (t) => 1 - Math.pow(1 - t, 3),
  in: (t) => t * t * t,
  outBack: (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  outElastic: (t) => (t === 0 || t === 1 ? t : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * (2 * Math.PI) / 3) + 1),
  quint: (t) => (t < 0.5 ? 16 * t ** 5 : 1 - Math.pow(-2 * t + 2, 5) / 2),
};

/** A critically damped (or springy, with zeta < 1) scalar spring. No allocation per step. */
export class Spring {
  constructor(value = 0, stiffness = 180, zeta = 1) { this.v = value; this.target = value; this.vel = 0; this.k = stiffness; this.z = zeta; }
  step(dt) {
    const w = Math.sqrt(this.k); const n = Math.max(1, Math.ceil(dt / 0.008)); const h = dt / n;
    for (let i = 0; i < n; i++) { const a = -this.k * (this.v - this.target) - 2 * this.z * w * this.vel; this.vel += a * h; this.v += this.vel * h; }
    return this.v;
  }
  snap(v) { this.v = v; this.target = v; this.vel = 0; }
}
const AXES = ['x', 'y', 'z'];
export class SpringV3 {
  constructor(stiffness = 220, zeta = 0.9) { this.v = new THREE.Vector3(); this.target = new THREE.Vector3(); this.vel = new THREE.Vector3(); this.k = stiffness; this.z = zeta; }
  step(dt) {
    const w = Math.sqrt(this.k); const n = Math.max(1, Math.ceil(dt / 0.008)); const h = dt / n;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < 3; j++) {
        const c = AXES[j];
        const a = -this.k * (this.v[c] - this.target[c]) - 2 * this.z * w * this.vel[c];
        this.vel[c] += a * h; this.v[c] += this.vel[c] * h;
      }
    }
    return this.v;
  }
  snap(p) { this.v.copy(p); this.target.copy(p); this.vel.set(0, 0, 0); }
}

/** Fire-and-forget tweens. Closures are created when a motion starts, never per frame. */
export function createAnimator() {
  const list = [];
  return {
    add(dur, update, opts = {}) {
      const a = { t: -(opts.delay || 0), dur: Math.max(1e-4, dur), update, ease: opts.ease || ease.inOut, done: opts.done, id: opts.id };
      if (opts.id) for (let i = list.length - 1; i >= 0; i--) if (list[i].id === opts.id) list.splice(i, 1);
      list.push(a);
      return a;
    },
    wait(dur, done) { return this.add(dur, () => {}, { done, ease: (t) => t }); },
    cancel(id) { for (let i = list.length - 1; i >= 0; i--) if (list[i].id === id || list[i] === id) list.splice(i, 1); },
    busy(id) { return list.some((a) => a.id === id); },
    update(dt) {
      for (let i = 0; i < list.length; i++) {
        const a = list[i];
        a.t += dt;
        if (a.t < 0) continue;
        const k = Math.min(1, a.t / a.dur);
        a.update(a.ease(k), k);
        if (k >= 1) { list.splice(i, 1); i--; if (a.done) a.done(); }
      }
    },
    clear() { list.length = 0; },
  };
}

export function rng(seed = 1) {
  let s = (seed >>> 0) || 1;
  return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
}
export function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 16777619); return h >>> 0; }

// ---- textures --------------------------------------------------------------------------------
const TEX = new Map();
export function canvasTexture(key, w, h, draw, opts = {}) {
  if (key && TEX.has(key)) return TEX.get(key);
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  if (opts.color !== false && t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = opts.anisotropy || 4;
  if (opts.repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(opts.repeat[0], opts.repeat[1]); }
  if (opts.wrapS) t.wrapS = THREE.RepeatWrapping;
  t.userData.sharedFx = !!key;
  if (key) TEX.set(key, t);
  return t;
}
export function disposeTextures() { TEX.forEach((t) => t.dispose()); TEX.clear(); }

// ---- materials ---------------------------------------------------------------------------------
const MATS = new Map();
function cached(key, make) { let m = MATS.get(key); if (!m) { m = make(); m.userData.sharedFx = true; MATS.set(key, m); } return m; }
export function disposeMaterials() { MATS.forEach((m) => m.dispose()); MATS.clear(); }

/** Living tissue: a wet sheen (clearcoat) over a soft, slightly translucent-looking base. */
export function wet(color, opts = {}) {
  return new THREE.MeshPhysicalMaterial({
    color, roughness: opts.roughness ?? 0.48, metalness: 0, clearcoat: opts.clearcoat ?? 0.7, clearcoatRoughness: opts.ccr ?? 0.22,
    sheen: opts.sheen ?? 0.35, sheenColor: new THREE.Color(opts.sheenColor ?? 0xffd6d6), sheenRoughness: 0.5,
    emissive: opts.emissive ?? 0x000000, map: opts.map || null, bumpMap: opts.bumpMap || null, bumpScale: opts.bumpScale ?? 1,
    side: opts.side ?? THREE.FrontSide, transparent: !!opts.transparent, opacity: opts.opacity ?? 1,
  });
}
export const MAT = {
  steel: () => cached('steel', () => new THREE.MeshStandardMaterial({ color: 0xd5dbe1, metalness: 1, roughness: 0.22, envMapIntensity: 1.3 })),
  blade: () => cached('blade', () => new THREE.MeshStandardMaterial({ color: 0xf1f4f7, metalness: 1, roughness: 0.1, envMapIntensity: 1.6 })),
  brushed: () => cached('brushed', () => new THREE.MeshStandardMaterial({ color: 0xb9c1c9, metalness: 0.9, roughness: 0.38 })),
  plastic: (c) => cached(`pl${c}`, () => new THREE.MeshStandardMaterial({ color: c, roughness: 0.42, metalness: 0 })),
  gloss: (c) => cached(`gl${c}`, () => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.3, clearcoat: 0.8, clearcoatRoughness: 0.15 })),
  matte: (c) => cached(`mt${c}`, () => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, metalness: 0 })),
  wax: () => cached('wax', () => new THREE.MeshPhysicalMaterial({ color: 0x2b2420, roughness: 0.55, clearcoat: 0.35, clearcoatRoughness: 0.5 })),
  glass: () => cached('glass', () => new THREE.MeshPhysicalMaterial({ color: 0xf2fbff, roughness: 0.03, transparent: true, opacity: 0.22, clearcoat: 1, clearcoatRoughness: 0.03, envMapIntensity: 1.6, depthWrite: false, side: THREE.DoubleSide })),
  glassEdge: () => cached('glassEdge', () => new THREE.MeshPhysicalMaterial({ color: 0xcdeee6, roughness: 0.05, transparent: true, opacity: 0.6, clearcoat: 1, envMapIntensity: 1.3, depthWrite: false })),
  paper: () => cached('paper', () => new THREE.MeshStandardMaterial({ color: 0xfbfaf6, roughness: 0.95 })),
  ink: (c) => cached(`ink${c}`, () => new THREE.MeshBasicMaterial({ color: c })),
  liquid: (c, o = 0.6) => cached(`liq${c}:${o}`, () => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.06, transparent: true, opacity: o, clearcoat: 1, clearcoatRoughness: 0.05, depthWrite: false })),
};

export function mesh(geometry, material, pos, opts = {}) {
  const m = new THREE.Mesh(geometry, material);
  if (pos) m.position.set(pos[0], pos[1], pos[2]);
  m.castShadow = opts.cast !== false && !material.transparent;
  m.receiveShadow = opts.receive !== false;
  if (opts.name) m.name = opts.name;
  return m;
}

/** A rounded rectangle extruded to a slab; the shape of slides, trays and boards. */
export function roundedSlab(w, d, h, r, bevel = 0) {
  const s = new THREE.Shape(); const x = -w / 2, y = -d / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + d - r);
  s.quadraticCurveTo(x + w, y + d, x + w - r, y + d); s.lineTo(x + r, y + d); s.quadraticCurveTo(x, y + d, x, y + d - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  const g = new THREE.ExtrudeGeometry(s, { depth: h, bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 2, curveSegments: 6 });
  g.rotateX(-Math.PI / 2);
  return g;
}

/** Draws a soft round brush dot; used for blood drops, stain splashes and glows. */
export function radial(g, x, y, r, inner, outer) {
  const gr = g.createRadialGradient(x, y, 0, x, y, r);
  gr.addColorStop(0, inner); gr.addColorStop(1, outer);
  g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
}

export function disposeTree(root) {
  root.traverse((o) => {
    if (o.geometry && !o.geometry.userData?.shared) o.geometry.dispose();
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    mats.forEach((m) => { if (!m.userData?.sharedFx) { ['map', 'bumpMap', 'normalMap', 'alphaMap', 'roughnessMap'].forEach((k) => { if (m[k] && !m[k].userData?.sharedFx) m[k].dispose(); }); m.dispose(); } });
  });
}
