import { THREE } from '../../core/engine.js';
import { toGeometry } from '../anatomy/mesher.js';
import { createTissue } from '../anatomy/tissue.js';
import { buildHeart } from './heart-model.js';
import { buildLungs, buildAirway, bronchialTree, buildDiaphragm } from './lung-model.js';

const HEART_COLOR = `
  float n1 = tFbm(vObj * 1.6);
  float fib = sin(dot(vObj, vec3(0.62, 0.48, 0.62)) * 19.0 + tNoise(vObj * 2.6) * 5.0) * 0.5 + 0.5;
  vec3 muscle = vec3(0.26, 0.045, 0.04) * (0.8 + 0.4 * n1) * (0.92 + fib * 0.14);
  vec2 cl = tCell(vObj * 3.2);
  vec3 fatC = vec3(0.74, 0.58, 0.30) * (0.86 + 0.24 * smoothstep(0.0, 0.25, cl.y - cl.x)) * (0.9 + 0.2 * tNoise(vObj * 7.0));
  vec3 c = mix(muscle, fatC, smoothstep(0.25, 0.8, vFat) * 0.9 * (1.0 - smoothstep(0.0, 0.5, vKind)));
  vec3 cor = mix(vec3(0.55, 0.16, 0.13), vec3(0.85, 0.12, 0.08), uTextbook);
  c = mix(c, cor, smoothstep(0.93, 0.985, vFat) * (1.0 - smoothstep(0.0, 0.5, vKind)) * 0.85);
  vec3 vessel = mix(vCR, vCB, uTextbook) * (0.88 + 0.2 * n1);
  vec2 tr = tCell(vObj * 2.2);
  vec3 inner = vec3(0.48, 0.07, 0.065) * (0.75 + 0.5 * smoothstep(0.0, 0.18, tr.y - tr.x));
  float mus = 1.0 - smoothstep(0.0, 0.5, vKind);
  c = mix(vessel, c, mus);
  c = mix(c, inner, vInr);
  if (!gl_FrontFacing) c = vec3(0.56, 0.12, 0.10) * (0.8 + 0.3 * fib);
  diffuseColor.rgb = c;`;

const LUNG_COLOR = `
  vec2 cl = tCell(vObj * 1.5);
  float edge = smoothstep(0.0, 0.07, cl.y - cl.x);
  float n1 = tFbm(vObj * 0.7);
  vec3 c = mix(vec3(0.52, 0.22, 0.26), vec3(0.80, 0.44, 0.46), 0.3 + 0.7 * n1);
  c *= 0.74 + 0.26 * edge;
  float spot = step(0.93, tHash(floor(vObj * 6.0))) * (1.0 - edge);
  c = mix(c, vec3(0.22, 0.16, 0.18), spot * 0.35);
  c = mix(c, c * vec3(1.05, 0.9, 0.92), uHiAmt * step(abs(vPart - uHi), 0.5));
  if (!gl_FrontFacing) c = vec3(0.62, 0.30, 0.33);
  diffuseColor.rgb = c;`;

const AIRWAY_COLOR = `
  float ring = smoothstep(0.15, 0.35, sin(vObj.y * 5.6 + vObj.x * 1.6) * 0.5 + 0.5);
  float back = smoothstep(-1.75, -2.15, vObj.z + 0.0 * vObj.y);
  vec3 cart = vec3(0.86, 0.80, 0.74);
  vec3 memb = vec3(0.74, 0.46, 0.46);
  vec3 c = mix(memb, cart, ring * (1.0 - back));
  if (!gl_FrontFacing) c = vec3(0.78, 0.42, 0.42);
  diffuseColor.rgb = c * (0.9 + 0.15 * tNoise(vObj * 6.0));`;

const DIAPH_COLOR = `
  float r = length(vObj.xz * vec2(0.8, 1.2));
  float tendon = 1.0 - smoothstep(3.2, 4.6, r + tFbm(vObj * 1.4) * 1.2);
  float fib = sin(atan(vObj.z, vObj.x) * 70.0 + tNoise(vObj * 2.0) * 3.0) * 0.5 + 0.5;
  vec3 m = vec3(0.50, 0.12, 0.10) * (0.85 + 0.25 * fib);
  vec3 t = vec3(0.84, 0.82, 0.80) * (0.9 + 0.1 * fib);
  diffuseColor.rgb = mix(m, t, tendon);`;

function attrGeo(mesh, extra) {
  const n = mesh.count;
  const base = { kind: [new Float32Array(n), 1], fat: [new Float32Array(n), 1], part: [new Float32Array(n), 1] };
  return toGeometry(THREE, mesh, Object.assign(base, extra));
}

function mergeTubes(branches) {
  const geos = branches.map((b) => {
    const a = new THREE.Vector3(...b.a); const c = new THREE.Vector3(...b.b);
    const len = a.distanceTo(c);
    const g = new THREE.CylinderGeometry(b.r * 0.8, b.r, len, 8, 1, true);
    g.translate(0, len / 2, 0);
    const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), c.clone().sub(a).normalize());
    g.applyQuaternion(q); g.translate(a.x, a.y, a.z);
    const s = new THREE.SphereGeometry(b.r * 0.8, 8, 6); s.translate(c.x, c.y, c.z);
    return [g, s];
  }).flat();
  let total = 0; let itot = 0;
  geos.forEach((g) => { total += g.attributes.position.count; itot += g.index.count; });
  const pos = new Float32Array(total * 3); const nor = new Float32Array(total * 3); const idx = new Uint32Array(itot);
  let o = 0; let io = 0;
  geos.forEach((g) => {
    pos.set(g.attributes.position.array, o * 3); nor.set(g.attributes.normal.array, o * 3);
    for (let i = 0; i < g.index.count; i++) idx[io + i] = g.index.array[i] + o;
    o += g.attributes.position.count; io += g.index.count; g.dispose();
  });
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  geo.setIndex(new THREE.BufferAttribute(idx, 1));
  return geo;
}

function buildModelsNow(quality) {
  return { H: buildHeart(quality), L: buildLungs(quality), A: buildAirway(quality), D: buildDiaphragm(quality) };
}

// The organs are meshed from signed distance fields, a few hundred milliseconds to seconds of pure
// arithmetic. It runs in a worker so the page keeps scrolling and the loader keeps spinning; the main
// thread only wraps the finished arrays in geometry.
export function buildModels(quality) {
  const q = { tier: quality.tier };
  return new Promise((resolve) => {
    let worker;
    try { worker = new Worker(new URL('./models-worker.js', import.meta.url), { type: 'module' }); } catch (e) { resolve(buildModelsNow(q)); return; }
    worker.onmessage = (e) => { worker.terminate(); resolve(e.data); };
    worker.onerror = (e) => { e.preventDefault && e.preventDefault(); worker.terminate(); resolve(buildModelsNow(q)); };
    worker.postMessage({ quality: q });
  });
}

export function buildScene(quality, models = null) {
  const M = models || buildModelsNow(quality);
  const shared = { uTime: { value: 0 }, uBeatV: { value: 0 }, uBeatA: { value: 0 }, uBreath: { value: 0 }, uTextbook: { value: 0 }, uHi: { value: -1 }, uHiAmt: { value: 0 } };
  const own = () => Object.fromEntries(Object.entries(shared).map(([k, v]) => [k, v]).concat([['uXray', { value: 0 }]]));
  const root = new THREE.Group();
  root.scale.setScalar(0.1);

  const H = M.H;
  const heartGeo = attrGeo(H.mesh, {
    kind: [Float32Array.from(H.kind, (k) => (k === 0 ? 0 : 1)), 1], fat: [H.fat, 1], part: [Float32Array.from(H.partIdx), 1], dispV: [H.dispV, 3], dispA: [H.dispA, 3],
    cR: [H.cR, 3], cB: [H.cB, 3], inr: [H.inr, 1],
  });
  const heartMat = createTissue({
    key: 'heart', uniforms: own(), color_fragment: HEART_COLOR, vertexAttrs: 'attribute vec3 dispV; attribute vec3 dispA; attribute vec3 cR; attribute vec3 cB; attribute float inr; varying vec3 vCR; varying vec3 vCB; varying float vInr;',
    fragmentHead: 'varying vec3 vCR; varying vec3 vCB; varying float vInr;',
    vertex: 'transformed += dispV * uBeatV + dispA * uBeatA; vCR = cR; vCB = cB; vInr = inr;',
    cap: 'vec3(0.34, 0.06, 0.05) * (0.88 + 0.16 * (sin(dot(vObj, vec3(0.6, 0.5, 0.6)) * 26.0 + tNoise(vObj * 4.0) * 5.0) * 0.5 + 0.5))', bumpAmt: 0.01, bump: 'tFbm(vObj * 2.4) * 0.7 + tNoise(vObj * 11.0) * 0.3',
  });
  const heart = new THREE.Mesh(heartGeo, heartMat);
  heart.userData.partNames = H.partNames;
  const heartGroup = new THREE.Group();
  heartGroup.add(heart);
  root.add(heartGroup);

  const L = M.L;
  const lungMat = createTissue({
    key: 'lung', uniforms: own(), color_fragment: LUNG_COLOR, roughness: 0.55, clearcoat: 0.55, clearcoatRoughness: 0.25, sheen: 0.3, sheenColor: 0xffc8c8,
    vertex: `float s = sign(position.x);
      float lat = max(0.0, abs(position.x) - 1.7);
      float down = smoothstep(11.0, -9.0, position.y);
      transformed.x += s * lat * 0.075 * uBreath;
      transformed.z += (position.z + 0.5) * 0.06 * uBreath;
      transformed.y -= down * 2.1 * uBreath;`,
    bumpAmt: 0.006, bump: 'tFbm(vObj * 1.2) * 0.5 + (1.0 - smoothstep(0.0, 0.1, tCell(vObj * 1.5).y - tCell(vObj * 1.5).x)) * 0.5',
    sss: 'vec3(0.7, 0.2, 0.2)', side: THREE.FrontSide,
  });
  const lungs = {};
  for (const side of ['right', 'left']) {
    const geo = attrGeo(L[side].mesh, { part: [L[side].lobe, 1] });
    const m = new THREE.Mesh(geo, lungMat);
    lungs[side] = m;
    root.add(m);
  }

  const airMesh = M.A;
  const airMat = createTissue({ key: 'airway', uniforms: own(), color_fragment: AIRWAY_COLOR, side: THREE.FrontSide, roughness: 0.38, sss: 'vec3(0.5, 0.25, 0.22)', bumpAmt: 0.004 });
  const airway = new THREE.Mesh(attrGeo(airMesh, {}), airMat);
  root.add(airway);

  const branches = bronchialTree(L);
  const treeMat = new THREE.MeshPhysicalMaterial({ color: 0xf0d4cc, roughness: 0.4, clearcoat: 0.6, emissive: 0x3a1a18, transparent: true, opacity: 0.95 });
  const tree = new THREE.Mesh(mergeTubes(branches), treeMat);
  tree.visible = false;
  root.add(tree);

  const dMesh = M.D;
  const diaMat = createTissue({
    key: 'diaphragm', uniforms: own(), side: THREE.FrontSide, color_fragment: DIAPH_COLOR, roughness: 0.5,
    vertex: 'float rr = length(position.xz); transformed.y -= (1.0 - smoothstep(4.0, 11.5, rr)) * 2.2 * uBreath;',
  });
  const diaphragm = new THREE.Mesh(attrGeo(dMesh, {}), diaMat);
  root.add(diaphragm);

  return {
    root, heartGroup, heart, lungs, airway, tree, diaphragm, branches, lungData: L,
    materials: { heart: heartMat, lung: lungMat, airway: airMat, diaphragm: diaMat, tree: treeMat },
    uniforms: shared,
    dispose() {
      [heart, lungs.right, lungs.left, airway, tree, diaphragm].forEach((m) => m.geometry.dispose());
      [heartMat, lungMat, airMat, diaMat, treeMat].forEach((m) => m.dispose());
    },
  };
}

export function backdrop() {
  const mat = new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `varying vec3 vP; void main(){
      float h = vP.y * 0.5 + 0.5;
      vec3 top = vec3(0.075, 0.09, 0.12); vec3 mid = vec3(0.13, 0.15, 0.19); vec3 bot = vec3(0.035, 0.04, 0.055);
      vec3 c = mix(bot, mid, smoothstep(0.1, 0.55, h)); c = mix(c, top, smoothstep(0.6, 1.0, h));
      gl_FragColor = vec4(pow(c, vec3(1.0 / 2.2)), 1.0); }`,
  });
  mat.toneMapped = false;
  const m = new THREE.Mesh(new THREE.SphereGeometry(60, 32, 16), mat);
  m.renderOrder = -10;
  return m;
}
