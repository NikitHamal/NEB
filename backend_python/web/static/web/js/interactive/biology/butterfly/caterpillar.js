import { THREE } from '../../core/engine.js';
import { canvasTexture, patchMaterial, smooth } from './kit.js';
import { caterpillarCanvas } from './textures.js';

const N = 24;
const BODY_END = 0.92;
const SEGS = 13;
export const CAT_LENGTH = 4.4;

// Plain tiger larva. Every vertex is stored relative to a spine (arc position + offset in the
// tangent/normal/side frame); the vertex shader bends it along 24 spine frames updated each frame,
// so the body can crawl over a curved leaf or hang in a J without rebuilding geometry.
function radiusAt(s) {
  const tail = Math.min(1, Math.sqrt(Math.max(0, s) / 0.06));
  const head = s > 0.84 ? 1 - ((s - 0.84) / (BODY_END - 0.84)) * 0.22 : 1;
  const segPhase = (s / BODY_END) * SEGS;
  const fold = Math.pow(Math.abs(Math.cos(Math.PI * segPhase)), 14);
  return 0.27 * tail * head * (1 - 0.17 * fold) * (1 + 0.04 * Math.sin(s * 3));
}
const CENTER = 0.26;
const segCenter = (i) => BODY_END - (i + 0.5) * (BODY_END / SEGS);

function builder() {
  const pos = []; const nor = []; const uv = []; const aS = []; const aOff = []; const col = []; const wig = []; const idx = [];
  const push = (s, t, n, b, nt, nn, nb, u, v, c, w = 0) => {
    aS.push(s); aOff.push(t, n, b); nor.push(nt, nn, nb); pos.push(0, 0, 0); uv.push(u, v);
    col.push(c ? c.r : 1, c ? c.g : 1, c ? c.b : 1); wig.push(w);
  };
  const geo = () => {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.setAttribute('aS', new THREE.Float32BufferAttribute(aS, 1));
    g.setAttribute('aOff', new THREE.Float32BufferAttribute(aOff, 3));
    g.setAttribute('aWig', new THREE.Float32BufferAttribute(wig, 1));
    g.setIndex(idx);
    g.boundingSphere = new THREE.Sphere(new THREE.Vector3(), 1e4);
    return g;
  };
  return { push, idx, geo, count: () => aS.length };
}

function bodyGeometry(rings, radial) {
  const B = builder();
  for (let i = 0; i <= rings; i++) {
    const s = (i / rings) * BODY_END;
    const r = radiusAt(s);
    for (let j = 0; j <= radial; j++) {
      const th = (j / radial) * Math.PI * 2;
      const cy = Math.cos(th); const sy = Math.sin(th);
      const flat = cy < 0 ? 0.62 : 1;
      B.push(s, 0, CENTER + r * cy * flat, r * sy * 1.02, 0, cy, sy, s / BODY_END, 0.5 + th / (Math.PI * 2), null);
    }
  }
  for (let i = 0; i < rings; i++) {
    for (let j = 0; j < radial; j++) {
      const a = i * (radial + 1) + j; const b = a + radial + 1;
      B.idx.push(a, a + 1, b, b, a + 1, b + 1);
    }
  }
  return B.geo();
}

function addTube(B, s, pts, radii, radial, color, wigFn) {
  const base = B.count();
  const n = pts.length;
  for (let i = 0; i < n; i++) {
    const p = pts[i];
    const t = pts[Math.min(n - 1, i + 1)].clone().sub(pts[Math.max(0, i - 1)]).normalize();
    const a = Math.abs(t.y) < 0.9 ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(1, 0, 0);
    const u = new THREE.Vector3().crossVectors(t, a).normalize(); const w = new THREE.Vector3().crossVectors(t, u);
    const c = typeof color === 'function' ? color(i / (n - 1)) : color;
    for (let j = 0; j <= radial; j++) {
      const th = (j / radial) * Math.PI * 2;
      const d = u.clone().multiplyScalar(Math.cos(th)).addScaledVector(w, Math.sin(th));
      B.push(s, p.x + d.x * radii(i / (n - 1)), p.y + d.y * radii(i / (n - 1)), p.z + d.z * radii(i / (n - 1)), d.x, d.y, d.z, 0, 0, c, wigFn ? wigFn(i / (n - 1)) : 0);
    }
  }
  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < radial; j++) {
      const a = base + i * (radial + 1) + j; const b = a + radial + 1;
      B.idx.push(a, b, a + 1, b, b + 1, a + 1);
    }
  }
}

function addEllipsoid(B, s, center, radii, wS, hS, color) {
  const base = B.count();
  for (let i = 0; i <= hS; i++) {
    const v = i / hS; const phi = v * Math.PI;
    for (let j = 0; j <= wS; j++) {
      const th = (j / wS) * Math.PI * 2;
      const nx = Math.sin(phi) * Math.cos(th); const ny = Math.cos(phi); const nz = Math.sin(phi) * Math.sin(th);
      const c = typeof color === 'function' ? color(nx, ny, nz) : color;
      B.push(s, center.x + nx * radii.x, center.y + ny * radii.y, center.z + nz * radii.z, nx, ny, nz, 0, 0, c);
    }
  }
  for (let i = 0; i < hS; i++) {
    for (let j = 0; j < wS; j++) {
      const a = base + i * (wS + 1) + j; const b = a + wS + 1;
      B.idx.push(a, b, a + 1, b, b + 1, a + 1);
    }
  }
}

function partsGeometry(q) {
  const B = builder();
  const black = new THREE.Color(0x0f0f0f); const grey = new THREE.Color(0x3b3b36); const white = new THREE.Color(0xeeeae0); const red = new THREE.Color(0x7a2a1c);
  const V = (t, n, b) => new THREE.Vector3(t, n, b);
  const sHead = BODY_END;
  addEllipsoid(B, sHead, V(0.1, CENTER - 0.02, 0), V(0.2, 0.23, 0.23), q * 2, q, (x, y, z) => {
    const band = Math.sin((y * 0.9 + x * 0.5) * 7);
    return band > 0.72 && x > -0.1 ? white : black;
  });
  [-1, 1].forEach((side) => {
    for (const i of [5, 6, 7, 8, 12]) {
      const s = segCenter(i);
      const b = side * radiusAt(s) * 0.55;
      const pts = [V(0, CENTER - 0.06, b * 0.8), V(0, CENTER * 0.5, b * 1.05), V(0, 0.03, b * 1.12)];
      addTube(B, s, pts, (t) => 0.085 - t * 0.02, q, grey);
      addEllipsoid(B, s, V(0, 0.025, b * 1.12), V(0.07, 0.025, 0.06), q, 3, black);
    }
    for (const i of [0, 1, 2]) {
      const s = segCenter(i);
      const b = side * radiusAt(s) * 0.45;
      addTube(B, s, [V(0, CENTER - 0.08, b), V(0.04, 0.1, b * 1.2), V(0.08, 0.02, b * 1.15)], (t) => 0.035 - t * 0.02, Math.max(4, q - 2), black);
    }
    [[1, 1.25, 1], [4, 0.6, 0], [10, 0.8, -1]].forEach(([i, len, dir]) => {
      const s = segCenter(i);
      const r = radiusAt(s);
      const a = 0.62;
      const base = V(0, CENTER + Math.cos(a) * r * 0.95, side * Math.sin(a) * r * 0.95);
      const pts = [];
      for (let k = 0; k <= 8; k++) {
        const t = k / 8;
        pts.push(V(base.x + dir * len * 0.6 * t * t, base.y + len * (0.9 * t - 0.3 * t * t * (dir === 0 ? 0.2 : 1)), base.z + side * len * 0.22 * t));
      }
      addTube(B, s, pts, (t) => 0.05 * (1 - t * 0.75), Math.max(4, q - 2), (t) => (t < 0.15 ? red : black), (t) => t * t);
    });
  });
  return B.geo();
}

const VERT_DECL = `
uniform vec3 uSpP[${N}]; uniform vec3 uSpT[${N}]; uniform vec3 uSpN[${N}];
uniform float uScale; uniform float uTime; uniform float uGirth;
attribute float aS; attribute vec3 aOff; attribute float aWig;
void spineFrame(float s, out vec3 P, out vec3 T, out vec3 Nn) {
  float f = clamp(s, 0.0, 1.0) * ${(N - 1).toFixed(1)};
  int i = int(min(floor(f), ${(N - 2).toFixed(1)}));
  float k = f - float(i);
  P = mix(uSpP[i], uSpP[i + 1], k);
  T = normalize(mix(uSpT[i], uSpT[i + 1], k));
  Nn = normalize(mix(uSpN[i], uSpN[i + 1], k));
}
`;
const VERT_NORMAL = `
vec3 spP; vec3 spT; vec3 spN;
spineFrame(aS, spP, spT, spN);
vec3 spB = normalize(cross(spT, spN));
vec3 objectNormal = normalize(spT * normal.x + spN * normal.y + spB * normal.z);
#ifdef USE_TANGENT
vec3 objectTangent = vec3(tangent.xyz);
#endif
`;
const VERT_BEGIN = `
vec3 off = aOff;
off.yz = vec2(${CENTER.toFixed(3)}, 0.0) + (off.yz - vec2(${CENTER.toFixed(3)}, 0.0)) * mix(1.0, uGirth, step(aWig, 0.0001));
off += aWig * vec3(0.0, 0.0, 1.0) * sin(uTime * 2.3 + aS * 17.0) * 0.12;
off += aWig * vec3(1.0, 0.0, 0.0) * sin(uTime * 1.7 + aS * 11.0) * 0.08;
vec3 transformed = spP + (spT * off.x + spN * off.y + spB * off.z) * uScale;
`;

export function buildCaterpillar(opts) {
  const { tier } = opts;
  const q = tier === 'low' ? 8 : tier === 'medium' ? 10 : 14;
  const uniforms = {
    uSpP: { value: Array.from({ length: N }, () => new THREE.Vector3()) },
    uSpT: { value: Array.from({ length: N }, () => new THREE.Vector3(0, 0, 1)) },
    uSpN: { value: Array.from({ length: N }, () => new THREE.Vector3(0, 1, 0)) },
    uScale: { value: 1 }, uTime: { value: 0 }, uGirth: { value: 1 },
  };
  const map = canvasTexture(caterpillarCanvas(512, 128));
  map.wrapT = THREE.RepeatWrapping;
  const bodyMat = new THREE.MeshPhysicalMaterial({ map, roughness: 0.42, clearcoat: tier === 'low' ? 0 : 0.55, clearcoatRoughness: 0.35, sheen: tier === 'low' ? 0 : 0.3, sheenColor: new THREE.Color(0xffffff) });
  const partMat = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.5, clearcoat: tier === 'low' ? 0 : 0.3, clearcoatRoughness: 0.4, envMapIntensity: 0.6 });
  [bodyMat, partMat].forEach((m, i) => patchMaterial(m, { uniforms, vertDecl: VERT_DECL, vertNormal: VERT_NORMAL, vertBegin: VERT_BEGIN, key: `cat${i}` }));
  const group = new THREE.Group();
  const body = new THREE.Mesh(bodyGeometry(tier === 'low' ? 60 : 110, q * 2), bodyMat);
  const parts = new THREE.Mesh(partsGeometry(q), partMat);
  body.frustumCulled = false; parts.frustumCulled = false;
  group.add(body, parts);

  const P = Array.from({ length: N }, () => new THREE.Vector3());
  const Nn = Array.from({ length: N }, () => new THREE.Vector3());
  const tmp = new THREE.Vector3();
  const crawl = { phase: -1, stride: 0.35, duration: 1.4, onDone: null };
  let headSwing = 0; let headNod = 0;

  // path(d, swing, outP, outN): d is the distance from the tail along the body, swing a sideways head offset.
  function update(time, scale, path) {
    uniforms.uScale.value = scale;
    uniforms.uTime.value = time;
    const Lb = CAT_LENGTH * scale;
    const w = crawl.phase;
    for (let i = 0; i < N; i++) {
      const s = i / (N - 1);
      let moved = 0; let lift = 0;
      if (w >= 0) {
        const wavePos = w * 1.25 - 0.1;
        moved = crawl.stride * scale * (1 - smooth((s - wavePos + 0.08) / 0.16));
        lift = 0.22 * scale * Math.exp(-(((s - wavePos) / 0.085) ** 2));
      }
      const headK = smooth((s - 0.78) / 0.22);
      path(s * Lb + moved, headK * headSwing * scale, P[i], Nn[i]);
      P[i].addScaledVector(Nn[i], lift + headK * headNod * scale);
    }
    for (let i = 0; i < N; i++) {
      const a = P[Math.max(0, i - 1)]; const b = P[Math.min(N - 1, i + 1)];
      tmp.subVectors(b, a).normalize();
      const n = Nn[i];
      n.addScaledVector(tmp, -n.dot(tmp)).normalize();
      uniforms.uSpP.value[i].copy(P[i]);
      uniforms.uSpT.value[i].copy(tmp);
      uniforms.uSpN.value[i].copy(n);
    }
  }

  return {
    group, crawl, uniforms,
    setHead(swing, nod) { headSwing = swing; headNod = nod; },
    startCrawl(onDone) { if (crawl.phase < 0) { crawl.phase = 0; crawl.onDone = onDone; } },
    tickCrawl(dt) {
      if (crawl.phase < 0) return;
      crawl.phase += dt / crawl.duration;
      if (crawl.phase >= 1) { crawl.phase = -1; if (crawl.onDone) crawl.onDone(crawl.stride); }
    },
    get crawling() { return crawl.phase >= 0; },
    update,
    headPosition(out) { return out.copy(uniforms.uSpP.value[N - 1]); },
    dispose() {},
  };
}
