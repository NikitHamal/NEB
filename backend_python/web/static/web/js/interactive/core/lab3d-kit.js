// The virtual lab's apparatus kit: every piece of glassware, metalwork and instrument the
// NEB practicals use, modelled once at real proportions (1 world unit = 10 cm) and shared by
// all thirty practicals. Glass is lathe-turned from a measured profile with a wall thickness,
// liquids sit inside with a meniscus, metals and plastics are PBR and lit by the engine's
// studio environment, and every texture (wood grain, scales, dials) is drawn once on a canvas
// and cached. Geometry is cached too, so rebuilding an apparatus when a slider moves costs
// almost nothing.
import { THREE, makeLabelSprite } from './engine.js';

// ---- materials -----------------------------------------------------------------------------
const MATS = new Map();
function cached(key, make) { let m = MATS.get(key); if (!m) { m = make(); m.userData.sharedFx = true; MATS.set(key, m); } return m; }

export const M = {
  glass: () => cached('glass', () => new THREE.MeshPhysicalMaterial({
    color: 0xf4fbff, roughness: 0.04, metalness: 0, transparent: true, opacity: 0.2, clearcoat: 1, clearcoatRoughness: 0.04,
    envMapIntensity: 1.6, side: THREE.DoubleSide, depthWrite: false, specularIntensity: 1,
  })),
  glassEdge: () => cached('glassEdge', () => new THREE.MeshPhysicalMaterial({ color: 0xdff3ff, roughness: 0.05, transparent: true, opacity: 0.55, clearcoat: 1, envMapIntensity: 1.4, depthWrite: false })),
  liquid: (color, opacity = 0.78) => cached(`liq${color}:${opacity}`, () => new THREE.MeshPhysicalMaterial({
    color, roughness: 0.08, metalness: 0, transparent: true, opacity, clearcoat: 0.6, envMapIntensity: 1.1, depthWrite: false,
  })),
  steel: () => cached('steel', () => new THREE.MeshStandardMaterial({ color: 0xc9d0d8, metalness: 0.92, roughness: 0.28, envMapIntensity: 1.2 })),
  chrome: () => cached('chrome', () => new THREE.MeshStandardMaterial({ color: 0xeef2f6, metalness: 1, roughness: 0.12, envMapIntensity: 1.4 })),
  brass: () => cached('brass', () => new THREE.MeshStandardMaterial({ color: 0xd8b25a, metalness: 0.95, roughness: 0.3, envMapIntensity: 1.2 })),
  copper: () => cached('copper', () => new THREE.MeshStandardMaterial({ color: 0xd4835a, metalness: 0.95, roughness: 0.32, envMapIntensity: 1.2 })),
  castIron: () => cached('castIron', () => new THREE.MeshStandardMaterial({ color: 0x2d3436, metalness: 0.35, roughness: 0.62 })),
  paint: (color) => cached(`paint${color}`, () => new THREE.MeshStandardMaterial({ color, metalness: 0.1, roughness: 0.42, envMapIntensity: 0.9 })),
  plastic: (color) => cached(`plastic${color}`, () => new THREE.MeshStandardMaterial({ color, metalness: 0, roughness: 0.38, envMapIntensity: 0.8 })),
  rubber: (color = 0x1f2326) => cached(`rubber${color}`, () => new THREE.MeshStandardMaterial({ color, metalness: 0, roughness: 0.9 })),
  porcelain: () => cached('porcelain', () => new THREE.MeshPhysicalMaterial({ color: 0xf6f4ef, roughness: 0.25, clearcoat: 0.8, clearcoatRoughness: 0.2 })),
  wood: (tone = 'oak') => cached(`wood${tone}`, () => new THREE.MeshStandardMaterial({ map: woodTexture(tone), roughness: 0.62, metalness: 0 })),
  glow: (color, intensity = 1.6) => cached(`glow${color}:${intensity}`, () => new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: intensity, roughness: 0.4 })),
  // flames blend normally, not additively: on a bright room additive layers saturate to white,
  // and a flame test is only worth anything if the colour reads true
  flame: (color, opacity = 0.62) => cached(`flame${color}:${opacity}`, () => new THREE.MeshBasicMaterial({ color, transparent: true, opacity, depthWrite: false, side: THREE.DoubleSide })),
  ink: (color = 0x1f2937) => cached(`ink${color}`, () => new THREE.MeshBasicMaterial({ color })),
};

// ---- procedural textures -------------------------------------------------------------------
const TEX = new Map();
function canvasTex(key, w, h, draw, repeat) {
  let t = TEX.get(key);
  if (t) return t;
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  t = new THREE.CanvasTexture(c);
  if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
  t.userData = { sharedFx: true };
  TEX.set(key, t);
  return t;
}

function rand(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 10000) / 10000; }; }

export function woodTexture(tone = 'oak') {
  const tones = { oak: ['#b98a57', '#a0723f', '#c99a64'], teak: ['#8a5a33', '#74482a', '#9c6a3e'], pale: ['#d9b98c', '#c9a575', '#e6c89c'] };
  const [base, dark, light] = tones[tone] || tones.oak;
  return canvasTex(`wood:${tone}`, 512, 512, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    const r = rand(tone.length * 977);
    // long grain lines with slow waves, a few knots
    for (let i = 0; i < 140; i++) {
      const y0 = r() * h; const amp = 2 + r() * 7; const f = 0.004 + r() * 0.01;
      g.strokeStyle = r() < 0.5 ? dark : light; g.globalAlpha = 0.12 + r() * 0.22; g.lineWidth = 0.6 + r() * 2.2;
      g.beginPath();
      for (let x = 0; x <= w; x += 8) g.lineTo(x, y0 + Math.sin(x * f + i) * amp);
      g.stroke();
    }
    g.globalAlpha = 0.18;
    for (let k = 0; k < 3; k++) { const x = r() * w, y = r() * h; for (let j = 8; j > 0; j--) { g.strokeStyle = dark; g.beginPath(); g.ellipse(x, y, j * 3.2, j * 1.4, 0, 0, Math.PI * 2); g.stroke(); } }
    g.globalAlpha = 1;
  }, [2, 1]);
}

/** A printed scale: ticks every [minor], numbers every [major], on a white or dark strip. */
export function scaleTexture({ length = 100, major = 10, minor = 1, unit = 'cm', dark = false, numbers = true, w = 2048, h = 160 } = {}) {
  return canvasTex(`scale:${length}:${major}:${minor}:${unit}:${dark}:${numbers}`, w, h, (g, W, H) => {
    g.fillStyle = dark ? '#151b24' : '#fbfaf6'; g.fillRect(0, 0, W, H);
    g.strokeStyle = dark ? '#e8edf3' : '#111827'; g.fillStyle = g.strokeStyle;
    const pad = 24; const usable = W - pad * 2;
    for (let i = 0; i <= length; i += minor) {
      const x = pad + usable * (i / length);
      const isMajor = Math.abs(i % major) < 1e-6; const isHalf = Math.abs(i % (major / 2)) < 1e-6;
      const len = isMajor ? H * 0.5 : isHalf ? H * 0.34 : H * 0.2;
      g.lineWidth = isMajor ? 3 : 1.8;
      g.beginPath(); g.moveTo(x, H); g.lineTo(x, H - len); g.stroke();
      if (numbers && isMajor) { g.font = '600 34px system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'top'; g.fillText(String(Math.round(i / (major / (major >= 10 ? 10 : 1)) * (major >= 10 ? 1 : 1))), x, 10); }
    }
    g.font = '600 24px system-ui, sans-serif'; g.textAlign = 'right'; g.fillText(unit, W - 14, 12);
  });
}

/** An analog meter face: arc, ticks, numbers and the instrument letter. */
export function dialTexture(letter, max, unit = '') {
  return canvasTex(`dial:${letter}:${max}:${unit}`, 512, 512, (g, W, H) => {
    g.fillStyle = '#f7f5ef'; g.fillRect(0, 0, W, H);
    const cx = W / 2, cy = H * 0.72, R = W * 0.4;
    g.strokeStyle = '#1f2937'; g.lineWidth = 4;
    g.beginPath(); g.arc(cx, cy, R, Math.PI * 1.2, Math.PI * 1.8); g.stroke();
    g.strokeStyle = '#c0392b'; g.lineWidth = 10; g.globalAlpha = 0.85;
    g.beginPath(); g.arc(cx, cy, R - 10, Math.PI * 1.7, Math.PI * 1.8); g.stroke(); g.globalAlpha = 1;
    g.fillStyle = '#1f2937'; g.textAlign = 'center'; g.textBaseline = 'middle';
    for (let i = 0; i <= 50; i++) {
      const a = Math.PI * 1.2 + (i / 50) * Math.PI * 0.6;
      const len = i % 10 === 0 ? 34 : i % 5 === 0 ? 24 : 14;
      g.lineWidth = i % 10 === 0 ? 4 : 2; g.strokeStyle = '#1f2937';
      g.beginPath(); g.moveTo(cx + Math.cos(a) * R, cy + Math.sin(a) * R); g.lineTo(cx + Math.cos(a) * (R - len), cy + Math.sin(a) * (R - len)); g.stroke();
      if (i % 10 === 0) { g.font = '600 30px system-ui, sans-serif'; g.fillText(String(+(max * i / 50).toFixed(max < 5 ? 1 : 0)), cx + Math.cos(a) * (R - 62), cy + Math.sin(a) * (R - 62)); }
    }
    g.font = '700 84px system-ui, sans-serif'; g.fillText(letter, cx, cy - 70);
    g.font = '500 26px system-ui, sans-serif'; g.fillStyle = '#4b5563'; g.fillText(unit, cx, cy - 20);
    g.font = '500 20px system-ui, sans-serif'; g.fillText('NEB LAB · CLASS 1.0', cx, H * 0.9);
  });
}

// ---- geometry helpers ----------------------------------------------------------------------
const GEO = new Map();
function geo(key, make) { let g = GEO.get(key); if (!g) { g = make(); g.userData = { sharedFx: true }; GEO.set(key, g); } return g; }
function mesh(g, m, pos, opts = {}) {
  const o = new THREE.Mesh(g, m);
  if (pos) o.position.set(pos[0], pos[1], pos[2]);
  o.castShadow = opts.cast !== false; o.receiveShadow = opts.receive !== false;
  if (m.transparent) { o.castShadow = false; o.renderOrder = opts.renderOrder ?? 2; }
  return o;
}
export function box(w, h, d, m, pos, r = 0) {
  const g = geo(`box${w}:${h}:${d}:${r}`, () => (r > 0 ? roundedBox(w, h, d, r) : new THREE.BoxGeometry(w, h, d)));
  return mesh(g, m, pos);
}
export function cyl(rt, rb, h, m, pos, seg = 40) { return mesh(geo(`cyl${rt}:${rb}:${h}:${seg}`, () => new THREE.CylinderGeometry(rt, rb, h, seg)), m, pos); }
export function sphere(r, m, pos, seg = 32) { return mesh(geo(`sph${r}:${seg}`, () => new THREE.SphereGeometry(r, seg, Math.max(10, seg >> 1))), m, pos); }
export function torus(r, t, m, pos, arc = Math.PI * 2) { return mesh(geo(`tor${r}:${t}:${arc}`, () => new THREE.TorusGeometry(r, t, 12, 48, arc)), m, pos); }

/** Rotates a child before it is added (Object3D.add returns the parent, not the child). */
export function rot(o, axis, v) { o.rotation[axis] = v; return o; }

function roundedBox(w, h, d, r) {
  const shape = new THREE.Shape();
  const x = -w / 2, y = -d / 2;
  shape.moveTo(x + r, y); shape.lineTo(x + w - r, y); shape.quadraticCurveTo(x + w, y, x + w, y + r);
  shape.lineTo(x + w, y + d - r); shape.quadraticCurveTo(x + w, y + d, x + w - r, y + d);
  shape.lineTo(x + r, y + d); shape.quadraticCurveTo(x, y + d, x, y + d - r); shape.lineTo(x, y + r); shape.quadraticCurveTo(x, y, x + r, y);
  const g = new THREE.ExtrudeGeometry(shape, { depth: h - r * 2, bevelEnabled: true, bevelThickness: r, bevelSize: r * 0.6, bevelSegments: 3, curveSegments: 6 });
  g.rotateX(-Math.PI / 2); g.translate(0, -h / 2 + r, 0);
  return g;
}

/** Lathe a profile [[r, y], ...] (outer wall bottom to top) into a vessel with a wall thickness. */
function vessel(key, profile, wall = 0.012, seg = 48) {
  return geo(`ves${key}`, () => {
    const outer = profile.map(([r, y]) => new THREE.Vector2(r, y));
    const inner = profile.slice().reverse().map(([r, y]) => new THREE.Vector2(Math.max(0.001, r - wall), Math.max(wall, y)));
    const pts = [new THREE.Vector2(0.001, 0)].concat(outer, [new THREE.Vector2(outer[outer.length - 1].x - wall * 0.5, outer[outer.length - 1].y + wall * 0.4)], inner, [new THREE.Vector2(0.001, wall)]);
    return new THREE.LatheGeometry(pts, seg);
  });
}
/** A liquid body following the inside of a profile up to [level] (world units from the base). */
function liquidGeo(key, profile, level, wall = 0.014, seg = 40) {
  const q = Math.round(level * 200) / 200;
  return geo(`liq${key}:${q}`, () => {
    const pts = [new THREE.Vector2(0.001, wall)];
    for (let i = 0; i < profile.length; i++) {
      const [r, y] = profile[i];
      if (y >= q) {
        const [r0, y0] = profile[Math.max(0, i - 1)];
        const t = y === y0 ? 1 : (q - y0) / (y - y0);
        pts.push(new THREE.Vector2(Math.max(0.002, r0 + (r - r0) * t - wall * 1.4), q));
        break;
      }
      pts.push(new THREE.Vector2(Math.max(0.002, r - wall * 1.4), Math.max(wall, y)));
    }
    const top = pts[pts.length - 1];
    // a meniscus: the surface curls up a hair at the glass
    pts.push(new THREE.Vector2(top.x * 0.92, q - 0.006), new THREE.Vector2(0.001, q - 0.008));
    return new THREE.LatheGeometry(pts, seg);
  });
}

const PROFILES = {
  beaker250: [[0.36, 0.0], [0.375, 0.02], [0.375, 0.95], [0.39, 0.975], [0.4, 0.99]],
  beaker100: [[0.26, 0.0], [0.275, 0.02], [0.275, 0.7], [0.29, 0.73]],
  conical: [[0.36, 0.0], [0.38, 0.03], [0.36, 0.2], [0.14, 0.82], [0.12, 0.9], [0.12, 1.08], [0.14, 1.11]],
  roundBottom: [[0.05, 0.0], [0.24, 0.05], [0.38, 0.2], [0.42, 0.38], [0.38, 0.58], [0.22, 0.74], [0.12, 0.8], [0.12, 1.22], [0.14, 1.25]],
  testTube: [[0.0, 0.0], [0.06, 0.02], [0.085, 0.07], [0.09, 0.13], [0.09, 1.4], [0.105, 1.43]],
  boilingTube: [[0.0, 0.0], [0.09, 0.03], [0.12, 0.1], [0.125, 0.18], [0.125, 1.5], [0.14, 1.53]],
  gasJar: [[0.34, 0.0], [0.36, 0.03], [0.36, 1.5], [0.4, 1.53]],
  measuring: [[0.17, 0.12], [0.18, 0.14], [0.18, 2.4], [0.2, 2.44]],
  funnel: [[0.035, 0.0], [0.035, 0.55], [0.05, 0.6], [0.42, 1.02], [0.45, 1.05]],
  calorimeter: [[0.4, 0.0], [0.42, 0.02], [0.42, 0.9], [0.44, 0.93]],
  dish: [[0.0, 0.0], [0.3, 0.02], [0.52, 0.1], [0.62, 0.2], [0.66, 0.22]],
  crucible: [[0.16, 0.0], [0.2, 0.02], [0.3, 0.42], [0.32, 0.44]],
};
export function profileOf(name) { return PROFILES[name]; }

// ---- labels ----------------------------------------------------------------------------------
/** A small floating tag with a hairline leader to the thing it names. Kept sparse on purpose. */
export function tag(group, text, at, opts = {}) {
  const off = opts.offset || [0, 0.55, 0];
  const base = makeLabelSprite(text, { fontSize: 34, weight: 600, scale: 1, bg: 'rgba(15,23,42,0.82)', color: opts.color || '#f8fafc' });
  // constant size on screen, whatever the zoom: a label that shrinks to nothing when you step
  // back, or covers the apparatus when you lean in, is worse than none
  const mat = base.material.clone();
  mat.sizeAttenuation = false; mat.depthTest = false; mat.userData.sharedFx = false;
  const s = new THREE.Sprite(mat);
  const h = (opts.scale ? opts.scale / 0.2 : 1) * 0.042;
  s.scale.set(base.scale.x * h, h, 1);
  s.center.set(0.5, 0);
  s.position.set(at[0] + off[0], at[1] + off[1], at[2] + off[2]);
  s.renderOrder = 20;
  group.add(s);
  if (opts.leader !== false) {
    const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(at[0], at[1], at[2]), new THREE.Vector3(at[0] + off[0], at[1] + off[1], at[2] + off[2])]);
    const l = new THREE.Line(g, cached('leader', () => new THREE.LineBasicMaterial({ color: 0x0f172a, transparent: true, opacity: 0.55, depthTest: false })));
    l.renderOrder = 19;
    group.add(l);
  }
  return s;
}

// ---- glassware -------------------------------------------------------------------------------
export function glassVessel(kind, { fill = 0, color = 0x9cc9ff, opacity = 0.75, scale = 1 } = {}) {
  const p = PROFILES[kind];
  const g = new THREE.Group();
  g.add(mesh(vessel(kind, p), M.glass(), null, { renderOrder: 3 }));
  if (fill > 0) {
    const top = p[p.length - 1][1];
    const level = Math.max(0.03, Math.min(top * 0.97, fill * top));
    const liq = mesh(liquidGeo(kind, p, level), M.liquid(color, opacity), null, { renderOrder: 2 });
    g.add(liq);
    g.userData.liquid = liq;
  }
  // graduation marks on beakers and cylinders, printed white enamel
  if (kind.startsWith('beaker') || kind === 'measuring') {
    const r = p[1][0] + 0.002; const top = p[p.length - 2][1];
    const n = kind === 'measuring' ? 20 : 5;
    for (let i = 1; i <= n; i++) {
      const y = 0.1 + (top - 0.15) * i / n;
      const len = i % (kind === 'measuring' ? 5 : 1) === 0 ? 0.09 : 0.05;
      const tick = box(len, 0.006, 0.004, M.ink(0xf8fafc), [0, y, r]);
      tick.position.x = -len / 2 + 0.02;
      g.add(tick);
    }
  }
  g.scale.setScalar(scale);
  return g;
}

export function testTube(color, fill = 0.4, opts = {}) {
  return glassVessel(opts.boiling ? 'boilingTube' : 'testTube', { fill, color, opacity: opts.opacity ?? 0.82 });
}

export function burette({ fillMl = 50, color = 0xdbeafe, opacity = 0.6 } = {}) {
  // 50 mL burette, 0.1 mL divisions: a tall bore, a PTFE stopcock and a drawn tip
  const g = new THREE.Group();
  const H = 5.4; const r = 0.065;
  g.add(cyl(r, r, H, M.glass(), [0, H / 2 + 0.5, 0], 28));
  const lvl = Math.max(0.05, (fillMl / 50) * (H - 0.4));
  g.add(cyl(r - 0.012, r - 0.012, lvl, M.liquid(color, opacity), [0, 0.5 + 0.2 + lvl / 2, 0], 24));
  // scale: a strip of printed graduations facing the camera
  const strip = new THREE.Mesh(new THREE.PlaneGeometry(0.1, H - 0.5), new THREE.MeshBasicMaterial({ map: scaleTexture({ length: 50, major: 10, minor: 1, unit: 'mL', w: 2048, h: 96 }), transparent: true, opacity: 0.85 }));
  strip.material.map.center.set(0.5, 0.5); strip.material.map.rotation = Math.PI / 2;
  strip.position.set(0, 0.5 + H / 2 + 0.1, r + 0.002);
  g.add(strip);
  // stopcock: a glass barrel, a white key
  g.add(cyl(0.05, 0.05, 0.22, M.glassEdge(), [0, 0.42, 0], 20));
  const key = box(0.32, 0.05, 0.05, M.plastic(0xf3f4f6), [0, 0.42, 0], 0.012);
  g.add(key);
  g.add(cyl(0.03, 0.008, 0.36, M.glass(), [0, 0.13, 0], 16));
  g.userData.key = key;
  g.userData.tipY = -0.05;
  return g;
}

export function thermometer(tempC, { height = 3.0, range = 110 } = {}) {
  const g = new THREE.Group();
  g.add(cyl(0.035, 0.035, height, M.glass(), [0, height / 2, 0], 16));
  g.add(sphere(0.055, M.liquid(0xe11d48, 0.95), [0, 0.02, 0], 16));
  const col = Math.max(0.05, Math.min(height * 0.92, (tempC + 10) / (range + 10) * height * 0.92));
  g.add(cyl(0.012, 0.012, col, M.glow(0xe11d48, 0.25), [0, col / 2, 0], 8));
  for (let i = 0; i <= 12; i++) g.add(box(i % 2 ? 0.035 : 0.06, 0.004, 0.004, M.ink(0x111827), [0.02, 0.15 + (height * 0.85) * i / 12, 0.036]));
  return g;
}

// ---- stands and heat ---------------------------------------------------------------------------
export function retortStand({ rod = 6.0, base = [1.6, 0.1, 1.0] } = {}) {
  const g = new THREE.Group();
  g.add(box(base[0], base[1], base[2], M.paint(0x24323a), [0, base[1] / 2, 0], 0.02));
  g.add(cyl(0.045, 0.045, rod, M.steel(), [-base[0] * 0.3, rod / 2 + base[1], 0], 16));
  g.userData.rodX = -base[0] * 0.3;
  return g;
}
/** A boss head and a clamp reaching out from the rod at height y to hold something at x. */
export function clamp(group, rodX, y, x, grip = 0.09) {
  group.add(box(0.12, 0.12, 0.12, M.castIron(), [rodX, y, 0], 0.01));
  group.add(rot(cyl(0.022, 0.022, Math.abs(x - rodX), M.steel(), [(rodX + x) / 2, y, 0], 12), 'z', Math.PI / 2));
  const jaw = new THREE.Group(); jaw.position.set(x, y, 0);
  jaw.add(box(0.05, 0.08, grip * 2 + 0.06, M.steel(), [-0.02, 0, 0]));
  jaw.add(box(0.06, 0.07, 0.03, M.rubber(0x8a2d2d), [0.02, 0, grip]));
  jaw.add(box(0.06, 0.07, 0.03, M.rubber(0x8a2d2d), [0.02, 0, -grip]));
  group.add(jaw);
  return jaw;
}

export function bunsen({ lit = true, color = 0x3b82f6, air = 1 } = {}) {
  const g = new THREE.Group();
  g.add(cyl(0.32, 0.36, 0.08, M.castIron(), [0, 0.04, 0], 32));
  g.add(cyl(0.065, 0.075, 1.1, M.chrome(), [0, 0.63, 0], 24));
  g.add(cyl(0.085, 0.085, 0.16, M.brass(), [0, 0.3, 0], 24));
  g.add(rot(cyl(0.03, 0.03, 0.4, M.brass(), [0.22, 0.14, 0], 12), 'z', Math.PI / 2));
  g.add(rot(cyl(0.035, 0.035, 0.6, M.rubber(0xd97706), [0.62, 0.1, 0], 12), 'z', Math.PI / 2.2));
  if (lit) {
    const f = flame(color, air);
    f.position.y = 1.18;
    g.add(f);
    g.userData.flame = f;
  }
  return g;
}

export function flame(color = 0x3b82f6, air = 1) {
  // a blue body with a pale inner cone, and a faint mantle; yellow and lazy when the air is shut
  const g = new THREE.Group();
  const yellow = air < 0.4;
  const outerCol = yellow ? 0xffa726 : color;
  const outer = mesh(geo('flameOuter', () => new THREE.ConeGeometry(0.1, 0.62, 24, 1, true).translate(0, 0.31, 0)), M.flame(outerCol, 0.55));
  const inner = mesh(geo('flameInner', () => new THREE.ConeGeometry(0.055, 0.26, 18, 1, true).translate(0, 0.13, 0)), M.flame(yellow ? 0xfff3c4 : 0xbfe3ff, 0.8));
  const halo = mesh(geo('flameHalo', () => new THREE.SphereGeometry(0.13, 16, 12).scale(1, 2.5, 1).translate(0, 0.3, 0)), M.flame(outerCol, 0.16));
  outer.renderOrder = 6; inner.renderOrder = 7; halo.renderOrder = 5;
  g.add(halo, outer, inner);
  return g;
}

export function tripodWithGauze() {
  const g = new THREE.Group();
  for (let i = 0; i < 3; i++) {
    const a = i * Math.PI * 2 / 3;
    const leg = cyl(0.025, 0.025, 1.45, M.castIron(), [Math.cos(a) * 0.36, 0.7, Math.sin(a) * 0.36], 8);
    leg.rotation.set(Math.sin(a) * 0.12, 0, -Math.cos(a) * 0.12);
    g.add(leg);
  }
  g.add(rot(torus(0.42, 0.025, M.castIron(), [0, 1.42, 0]), 'x', Math.PI / 2));
  const gauze = box(1.0, 0.012, 1.0, cached('gauze', () => new THREE.MeshStandardMaterial({ map: canvasTex('gauze', 256, 256, (c, w, h) => { c.fillStyle = '#9aa3ad'; c.fillRect(0, 0, w, h); c.strokeStyle = '#59616b'; c.lineWidth = 2; for (let i = 0; i < w; i += 8) { c.beginPath(); c.moveTo(i, 0); c.lineTo(i, h); c.stroke(); c.beginPath(); c.moveTo(0, i); c.lineTo(w, i); c.stroke(); } c.fillStyle = '#e8e2d6'; c.beginPath(); c.arc(w / 2, h / 2, w * 0.28, 0, Math.PI * 2); c.fill(); }), metalness: 0.5, roughness: 0.6 })), [0, 1.46, 0]);
  g.add(gauze);
  g.userData.top = 1.47;
  return g;
}

// ---- physics instruments -------------------------------------------------------------------
export function meterRule(lengthM = 1, { dark = false } = {}) {
  const L = lengthM * 10;
  const g = new THREE.Group();
  g.add(box(L + 0.1, 0.04, 0.32, M.wood('pale'), [0, 0.02, 0]));
  const face = new THREE.Mesh(new THREE.PlaneGeometry(L, 0.3), new THREE.MeshStandardMaterial({ map: scaleTexture({ length: lengthM * 100, major: 10, minor: 1, unit: 'cm', dark, w: 4096, h: 160 }), roughness: 0.6 }));
  face.rotation.x = -Math.PI / 2; face.position.y = 0.0405;
  g.add(face);
  return g;
}

export function analogMeter(letter, max, unit = '') {
  const g = new THREE.Group();
  g.add(box(1.0, 0.7, 0.42, M.plastic(0x1f2937), [0, 0.35, 0], 0.04));
  const face = new THREE.Mesh(new THREE.PlaneGeometry(0.84, 0.56), new THREE.MeshStandardMaterial({ map: dialTexture(letter, max, unit), roughness: 0.5 }));
  face.position.set(0, 0.38, 0.212);
  g.add(face);
  g.add(box(0.86, 0.58, 0.02, M.glass(), [0, 0.38, 0.226]));
  const pivot = new THREE.Group(); pivot.position.set(0, 0.215, 0.218);
  const needle = box(0.008, 0.36, 0.004, M.ink(0x111111), [0, 0.18, 0]);
  pivot.add(needle);
  g.add(pivot);
  for (const [x, col] of [[-0.3, 0xd32f2f], [0.3, 0x111827]]) g.add(rot(cyl(0.045, 0.045, 0.1, M.plastic(col), [x, 0.05, 0.25], 16), 'x', Math.PI / 2));
  g.userData.setValue = (v) => { pivot.rotation.z = -(-0.94 + Math.max(0, Math.min(1, v / max)) * 1.88) + 0; };
  g.userData.setValue(0);
  // bench meters sit tilted back so the dial faces whoever is reading it
  g.rotation.x = -0.55;
  return g;
}

/** A wire or rubber tube from a to b, drooping under its own weight like a real lead. */
export function wire(a, b, color = 0xd32f2f, sag = 0.25, radius = 0.022) {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b);
  const pts = [];
  const span = A.distanceTo(B);
  const droop = sag * Math.min(1.5, 0.4 + span * 0.25);
  for (let i = 0; i <= 16; i++) {
    const t = i / 16;
    const p = A.clone().lerp(B, t);
    p.y -= Math.sin(Math.PI * t) * droop;
    pts.push(p);
  }
  return mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 48, radius, 8, false), M.plastic(color));
}

export function cell() {
  const g = new THREE.Group();
  g.add(cyl(0.17, 0.17, 0.6, M.paint(0x1f2937), [0, 0.3, 0], 24));
  g.add(cyl(0.171, 0.171, 0.2, M.paint(0xd97706), [0, 0.5, 0], 24));
  g.add(cyl(0.05, 0.05, 0.05, M.chrome(), [0, 0.625, 0], 12));
  return g;
}

export function resistor(label = '') {
  const g = new THREE.Group();
  g.add(box(0.9, 0.12, 0.4, M.wood('pale'), [0, 0.06, 0], 0.02));
  const coil = cyl(0.09, 0.09, 0.62, M.paint(0xc9a227), [0, 0.22, 0], 20); coil.rotation.z = Math.PI / 2; g.add(coil);
  for (let i = 0; i < 4; i++) g.add(rot(cyl(0.092, 0.092, 0.03, M.paint([0x8b4513, 0x111111, 0xd32f2f, 0xd4af37][i]), [-0.18 + i * 0.1, 0.22, 0], 20), 'z', Math.PI / 2));
  for (const x of [-0.38, 0.38]) g.add(cyl(0.04, 0.04, 0.1, M.brass(), [x, 0.16, 0], 12));
  if (label) g.userData.label = label;
  return g;
}

export function rheostat() {
  const g = new THREE.Group();
  g.add(box(2.0, 0.1, 0.6, M.paint(0x37474f), [0, 0.05, 0], 0.02));
  for (const x of [-0.92, 0.92]) g.add(box(0.12, 0.5, 0.5, M.paint(0x37474f), [x, 0.35, 0], 0.02));
  const coil = cyl(0.2, 0.2, 1.7, cached('coil', () => new THREE.MeshStandardMaterial({ map: canvasTex('coil', 512, 64, (c, w, h) => { c.fillStyle = '#b98a4a'; c.fillRect(0, 0, w, h); c.strokeStyle = '#6d4c22'; c.lineWidth = 2; for (let x = 0; x < w; x += 6) { c.beginPath(); c.moveTo(x, 0); c.lineTo(x + 3, h); c.stroke(); } }), metalness: 0.7, roughness: 0.35 })), [0, 0.42, 0], 24);
  coil.rotation.z = Math.PI / 2; g.add(coil);
  g.add(rot(cyl(0.02, 0.02, 1.84, M.chrome(), [0, 0.7, 0], 8), 'z', Math.PI / 2));
  const slider = box(0.14, 0.12, 0.16, M.brass(), [0, 0.68, 0], 0.02); g.add(slider);
  g.userData.slider = slider;
  return g;
}

export function stopwatch(seconds = 0) {
  const g = new THREE.Group();
  g.add(rot(cyl(0.28, 0.28, 0.08, M.chrome(), [0, 0, 0], 32), 'x', Math.PI / 2));
  g.add(cyl(0.05, 0.05, 0.08, M.chrome(), [0, 0.32, 0], 12));
  const face = new THREE.Mesh(new THREE.CircleGeometry(0.25, 32), new THREE.MeshBasicMaterial({ map: canvasTex('stopwatch', 256, 256, (c, w, h) => { c.fillStyle = '#fbfaf7'; c.beginPath(); c.arc(w / 2, h / 2, w / 2, 0, Math.PI * 2); c.fill(); c.strokeStyle = '#111'; for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2; const r1 = i % 5 ? 112 : 100; c.lineWidth = i % 5 ? 2 : 4; c.beginPath(); c.moveTo(w / 2 + Math.sin(a) * r1, h / 2 - Math.cos(a) * r1); c.lineTo(w / 2 + Math.sin(a) * 122, h / 2 - Math.cos(a) * 122); c.stroke(); } }) }));
  face.position.z = 0.041; g.add(face);
  const hand = box(0.01, 0.2, 0.005, M.ink(0xd32f2f), [0, 0.1, 0.045]);
  const pivot = new THREE.Group(); pivot.add(hand); g.add(pivot);
  pivot.rotation.z = -(seconds % 60) / 60 * Math.PI * 2;
  g.userData.hand = pivot;
  return g;
}

export function slottedWeights(n = 3) {
  const g = new THREE.Group();
  g.add(cyl(0.012, 0.012, 0.5 + n * 0.06, M.steel(), [0, 0.25 + n * 0.03, 0], 8));
  g.add(cyl(0.12, 0.12, 0.03, M.steel(), [0, 0.015, 0], 24));
  for (let i = 0; i < n; i++) g.add(cyl(0.16, 0.16, 0.06, M.brass(), [0, 0.06 + i * 0.065, 0], 28));
  g.add(torus(0.04, 0.008, M.steel(), [0, 0.56 + n * 0.06, 0]));
  return g;
}

export function tuningFork() {
  const g = new THREE.Group();
  const shape = new THREE.Shape();
  shape.moveTo(-0.11, 0); shape.lineTo(-0.11, 1.0); shape.lineTo(-0.07, 1.0); shape.lineTo(-0.07, 0.12);
  shape.absarc(0, 0.12, 0.07, Math.PI, 0, true); shape.lineTo(0.07, 1.0); shape.lineTo(0.11, 1.0); shape.lineTo(0.11, 0);
  shape.absarc(0, 0, 0.11, 0, Math.PI, true);
  const prongs = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: 0.04, bevelEnabled: true, bevelSize: 0.006, bevelThickness: 0.006, bevelSegments: 2 }), M.chrome());
  prongs.position.z = -0.02; g.add(prongs);
  g.add(cyl(0.025, 0.025, 0.5, M.chrome(), [0, -0.33, 0], 12));
  return g;
}

export function glassSlab(w, h, d) { return box(w, h, d, M.glassEdge(), null); }
