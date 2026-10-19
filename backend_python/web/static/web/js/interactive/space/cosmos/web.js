import { THREE } from '../../core/engine.js';
import { NOISE, shader, pointsMaterial, makePoints } from './shaders.js';
import { rng, gauss, galLB, CLUSTERS } from './astro.js';

function webPoints({ seed, radius, nodes, fixed = [], count, width, clusterR, colorFn }) {
  const r = rng(seed);
  const N = [];
  fixed.forEach((f) => N.push({ p: f.p, rich: f.rich }));
  while (N.length < nodes) {
    const u = r() * 2 - 1; const th = r() * Math.PI * 2; const s = Math.sqrt(1 - u * u);
    const d = radius * Math.cbrt(r());
    N.push({ p: new THREE.Vector3(s * Math.cos(th) * d, u * d, s * Math.sin(th) * d), rich: Math.pow(r(), 3) });
  }
  const edges = [];
  const seen = new Set();
  N.forEach((a, i) => {
    const near = [[-1, Infinity], [-1, Infinity], [-1, Infinity]];
    for (let j = 0; j < N.length; j++) {
      if (j === i) continue;
      const d2 = a.p.distanceToSquared(N[j].p);
      if (d2 < near[2][1]) { near[2] = [j, d2]; near.sort((x, y) => x[1] - y[1]); }
    }
    near.forEach(([j, d2]) => {
      if (j < 0) return;
      const key = i < j ? `${i}-${j}` : `${j}-${i}`;
      if (seen.has(key) || d2 > Math.pow(radius * 0.55, 2)) return;
      seen.add(key);
      edges.push([a.p, N[j].p, Math.sqrt(d2)]);
    });
  });
  const pos = new Float32Array(count * 3); const col = new Float32Array(count * 3); const size = new Float32Array(count);
  const tmp = new THREE.Vector3();
  const totalLen = edges.reduce((s, e) => s + e[2], 0);
  for (let i = 0; i < count; i++) {
    const kind = r();
    if (kind < 0.55 && edges.length) {
      let pick = r() * totalLen; let e = edges[0];
      for (const ed of edges) { pick -= ed[2]; if (pick <= 0) { e = ed; break; } }
      const t = r();
      tmp.copy(e[0]).lerp(e[1], t);
      const w = width * (0.6 + Math.sin(t * Math.PI) * 0.6);
      tmp.x += gauss(r) * w; tmp.y += gauss(r) * w; tmp.z += gauss(r) * w;
    } else if (kind < 0.9) {
      const n = N[Math.floor(Math.pow(r(), 1.6) * N.length)];
      const cr = clusterR * (0.4 + n.rich * 1.6);
      tmp.copy(n.p);
      tmp.x += gauss(r) * cr; tmp.y += gauss(r) * cr; tmp.z += gauss(r) * cr;
    } else {
      const u = r() * 2 - 1; const th = r() * Math.PI * 2; const s = Math.sqrt(1 - u * u);
      const d = radius * Math.cbrt(r());
      tmp.set(s * Math.cos(th) * d, u * d, s * Math.sin(th) * d);
    }
    pos[i * 3] = tmp.x; pos[i * 3 + 1] = tmp.y; pos[i * 3 + 2] = tmp.z;
    const c = colorFn(tmp, r);
    col[i * 3] = c[0]; col[i * 3 + 1] = c[1]; col[i * 3 + 2] = c[2];
    size[i] = width * (0.35 + r() * 0.6);
  }
  return { pos, col, size, nodes: N };
}

function flowLines(ga, radius, count, seed) {
  const r = rng(seed);
  const verts = []; const alphas = [];
  for (let i = 0; i < count; i++) {
    const u = r() * 2 - 1; const th = r() * Math.PI * 2; const s = Math.sqrt(1 - u * u);
    const d = radius * (0.45 + 0.55 * r());
    const p = new THREE.Vector3(s * Math.cos(th) * d, u * d * 0.6, s * Math.sin(th) * d).add(ga);
    const swirl = new THREE.Vector3(gauss(r), gauss(r), gauss(r)).normalize();
    const steps = 40;
    let prev = p.clone();
    for (let k = 1; k <= steps; k++) {
      const to = ga.clone().sub(prev);
      const dist = to.length();
      if (dist < radius * 0.04) break;
      to.normalize();
      const side = new THREE.Vector3().crossVectors(to, swirl).multiplyScalar(0.45 * Math.min(1, dist / radius));
      const next = prev.clone().addScaledVector(to.add(side).normalize(), radius * 0.035);
      verts.push(prev.x, prev.y, prev.z, next.x, next.y, next.z);
      const a0 = (k - 1) / steps; const a1 = k / steps;
      alphas.push(a0, a1);
      prev = next;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
  geo.setAttribute('alpha', new THREE.Float32BufferAttribute(alphas, 1));
  const mat = shader({
    uniforms: { uTime: { value: 0 } },
    vertexHead: 'attribute float alpha; varying float vA;',
    vertex: 'vA = alpha; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
    fragmentHead: 'uniform float uTime; varying float vA;',
    fragment: `float pulse = 0.55 + 0.45 * sin(vA * 30.0 - uTime * 2.0);
      gl_FragColor = vec4(vec3(0.75, 0.88, 1.0) * vA * pulse * 0.55 * uOpacity, 1.0);`,
    blending: THREE.AdditiveBlending,
  });
  const lines = new THREE.LineSegments(geo, mat);
  lines.frustumCulled = false;
  return lines;
}

export function createCosmicWeb(quality) {
  const group = new THREE.Group();
  const count = quality.tier === 'low' ? 40000 : quality.tier === 'medium' ? 80000 : 130000;
  const fixed = CLUSTERS.map((c) => ({ p: galLB(c.l, c.b, c.d / 1e6), rich: Math.min(1, c.n / 1000) }));
  fixed.push({ p: new THREE.Vector3(), rich: 0.05 });
  const ga = fixed[3].p.clone();
  const w = webPoints({
    seed: 404, radius: 650, nodes: 260, fixed, count, width: 4.5, clusterR: 3.5,
    colorFn: (p, r) => {
      const inL = p.distanceTo(ga) < 260 ? 1 : 0;
      const k = 0.35 + r() * 0.5;
      return inL ? [1.0 * k, 0.86 * k, 0.62 * k] : [0.72 * k, 0.8 * k, 1.0 * k];
    },
  });
  const pts = makePoints(w.pos, w.col, w.size, pointsMaterial({ min: 1.0, max: 4, gain: 0.85, core: 0.1 }));
  group.add(pts);
  const flow = flowLines(ga, 250, quality.tier === 'low' ? 60 : 140, 9);
  group.add(flow);
  const labels = CLUSTERS.map((c, i) => ({
    text: c.name, sub: `${Math.round(c.d / 1e6)} million light-years`, get: (v) => v.copy(fixed[i].p), min: i < 2 ? 23.6 : 24.2, max: 25.6, minor: i > 3,
  }));
  labels.push({ text: 'Laniakea Supercluster', sub: '520 million light-years · 100 000 galaxies', get: (v) => v.copy(ga).add(new THREE.Vector3(0, 140, 0)), min: 24.4, max: 25.7 });
  labels.push({ text: 'Local Group', sub: 'us', get: (v) => v.set(0, 0, 0), min: 23.4, max: 24.6, cls: 'here' });
  return {
    group,
    labels,
    update(t, logW) {
      flow.material.uniforms.uTime.value = t;
      flow.visible = logW > 24.0 && logW < 26.0;
      flow.material.uniforms.uOpacity.value *= Math.min(1, Math.max(0, (logW - 24.0) / 0.6)) * Math.min(1, Math.max(0, (26.0 - logW) / 0.5));
    },
    setPx(uPx, scale) { pts.material.uniforms.uPx.value = uPx; pts.material.uniforms.uScale.value = scale; },
  };
}

export function createObservableUniverse(quality) {
  const group = new THREE.Group();
  const R = 46.5;
  const count = quality.tier === 'low' ? 50000 : quality.tier === 'medium' ? 90000 : 150000;
  const w = webPoints({
    seed: 1337, radius: R * 0.985, nodes: quality.tier === 'low' ? 700 : 1400, count, width: 0.35, clusterR: 0.18,
    colorFn: (p, r) => {
      const z = p.length() / R;
      const k = (0.35 + r() * 0.55) * (1 - z * 0.55);
      return [k * (0.85 + z * 0.3), k * (0.88 - z * 0.25), k * (1.0 - z * 0.6)];
    },
  });
  const pts = makePoints(w.pos, w.col, w.size, pointsMaterial({ min: 1.3, max: 3.5, gain: 1.25, core: 0.2 }));
  group.add(pts);
  const seg = quality.tier === 'low' ? 96 : 160;
  const cmbMat = shader({
    uniforms: { uCut: { value: 0.25 } },
    vertexHead: 'varying vec3 vN; varying vec3 vV; varying vec3 vWN;',
    vertex: `vec4 wp = modelMatrix * vec4(position, 1.0); vN = normalize(position); vWN = normalize(mat3(modelMatrix) * position); vV = normalize(cameraPosition - wp.xyz);
      gl_Position = projectionMatrix * viewMatrix * wp;`,
    fragmentHead: `uniform float uCut; varying vec3 vN; varying vec3 vV; varying vec3 vWN; ${NOISE}
      vec3 planck(float t){ t = clamp(t, 0.0, 1.0);
        vec3 a = vec3(0.0, 0.08, 0.55); vec3 b = vec3(0.25, 0.75, 0.98); vec3 c = vec3(1.0, 0.97, 0.88); vec3 d = vec3(1.0, 0.62, 0.14); vec3 e = vec3(0.72, 0.08, 0.04);
        if (t < 0.25) return mix(a, b, t / 0.25); if (t < 0.5) return mix(b, c, (t - 0.25) / 0.25); if (t < 0.75) return mix(c, d, (t - 0.5) / 0.25); return mix(d, e, (t - 0.75) / 0.25); }`,
    fragment: `
      vec3 n = normalize(vN);
      float facing = dot(normalize(vWN), normalize(vV));
      if (gl_FrontFacing && facing > 0.42) discard;
      float t = fbm3(n * 9.0) * 0.6 + fbm3(n * 26.0 + 4.0) * 0.4;
      t = (t - 0.5) * 2.4 + 0.5;
      vec3 col = planck(t);
      float edge = gl_FrontFacing ? 1.0 : 0.42;
      gl_FragColor = vec4(col * edge, uOpacity * (gl_FrontFacing ? 1.0 : 0.95));`,
    side: THREE.DoubleSide,
    transparent: true,
    depthWrite: false,
  });
  const cmb = new THREE.Mesh(new THREE.SphereGeometry(R, seg, seg / 2), cmbMat);
  cmb.renderOrder = 1;
  pts.renderOrder = 2;
  group.add(cmb);
  const here = makePoints(new Float32Array(3), new Float32Array([1, 0.9, 0.6]), new Float32Array([0.6]), pointsMaterial({ min: 4, max: 6, gain: 1.2, core: 1 }));
  group.add(here);
  return {
    group,
    labels: [
      { text: 'Observable universe', sub: '93 billion light-years across · 2 trillion galaxies', get: (v) => v.set(0, R * 1.02, 0), min: 26.2, max: 28 },
      { text: 'Cosmic microwave background', sub: 'light from 380 000 years after the Big Bang', get: (v) => v.set(R * 0.72, -R * 0.69, 0), min: 26.4, max: 28, minor: true },
      { text: 'You are here', sub: 'every observer is at the centre of their own observable universe', get: (v) => v.set(0, 0, 0), min: 26.0, max: 28, cls: 'here' },
    ],
    update() {},
    setPx(uPx, scale) {
      pts.material.uniforms.uPx.value = uPx; pts.material.uniforms.uScale.value = scale;
      here.material.uniforms.uPx.value = uPx; here.material.uniforms.uScale.value = scale;
    },
  };
}
