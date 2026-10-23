import { THREE } from '../../core/engine.js';
import { canvasTexture, patchMaterial, mergeGeos, paintVertices, taperedTube, texSize, lerp } from './kit.js';
import { wingCanvases, FORE, HIND } from './textures.js';

const WING_SCALE = 3.7;

function wingGeometry(spec, side, segs) {
  const [x0, x1, y0, y1] = spec.box;
  const nx = segs; const ny = Math.round(segs * (y1 - y0) / (x1 - x0));
  const pos = []; const uv = []; const idx = [];
  for (let j = 0; j <= ny; j++) {
    for (let i = 0; i <= nx; i++) {
      const u = i / nx; const v = j / ny;
      const x = (x0 + (x1 - x0) * u) * WING_SCALE; const y = (y0 + (y1 - y0) * v) * WING_SCALE;
      const camber = -0.05 * (x * x) / WING_SCALE + 0.04 * Math.sin(Math.PI * u) * Math.cos(v * 2);
      pos.push(side * x, camber, y);
      uv.push(u, v);
    }
  }
  for (let j = 0; j < ny; j++) {
    for (let i = 0; i < nx; i++) {
      const a = j * (nx + 1) + i; const b = a + 1; const c = a + nx + 1; const d = c + 1;
      if (side > 0) idx.push(a, c, b, b, c, d); else idx.push(a, b, c, b, d, c);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

function bodyGeometry(seg) {
  const parts = [];
  const black = new THREE.Color(0x141110); const white = new THREE.Color(0xf2efe6); const brown = new THREE.Color(0x5a3a22);
  const thorax = new THREE.SphereGeometry(1, seg + 4, seg);
  thorax.scale(0.24, 0.25, 0.42); thorax.translate(0, 0, 0.42);
  paintVertices(thorax, (x, y, z, c) => {
    const spot = (Math.abs(x) > 0.17 && Math.sin(z * 30) > 0.75) || (y > 0.2 && Math.abs(Math.sin(z * 22 + x * 30)) > 0.97);
    c.copy(spot ? white : black);
  });
  parts.push(thorax);
  const abPts = [];
  for (let i = 0; i <= 16; i++) { const t = i / 16; abPts.push(new THREE.Vector3(0, -0.03 - Math.sin(t * Math.PI) * 0.04 - t * t * 0.08, 0.1 - t * 1.55)); }
  const abCurve = new THREE.CatmullRomCurve3(abPts);
  const ab = taperedTube(abCurve, 28, seg + 2, (t) => (0.2 * Math.pow(Math.sin(Math.PI * Math.min(1, 0.12 + t * 0.92)), 0.6) + 0.02) * (1 - 0.06 * Math.pow(Math.abs(Math.cos(t * Math.PI * 7)), 6)), { capEnd: true });
  const tawny = new THREE.Color(0x6b3416); const cream = new THREE.Color(0xd2c3a2);
  paintVertices(ab, (x, y, z, c) => {
    const ring = Math.pow(Math.abs(Math.cos(z * 14)), 8);
    c.copy(y < -0.18 ? cream : tawny).lerp(black, ring * 0.5 + (y > 0.04 ? 0.25 : 0));
    if (Math.abs(x) > 0.14 && y > -0.12 && y < 0.02 && Math.sin(z * 14 + 1.2) > 0.85) c.copy(white);
  });
  parts.push(ab);
  const head = new THREE.SphereGeometry(0.17, seg + 2, seg);
  head.scale(1, 0.95, 0.85); head.translate(0, 0.02, 0.92);
  paintVertices(head, (x, y, z, c) => c.copy(Math.abs(x) < 0.05 && y > 0.05 ? white : black));
  parts.push(head);
  [-1, 1].forEach((s) => {
    const eye = new THREE.SphereGeometry(0.115, seg + 2, seg);
    eye.translate(s * 0.11, 0.04, 0.95);
    paintVertices(eye, (x, y, z, c) => c.set(0x2a1a12).lerp(white, Math.sin(x * 140) * Math.sin(y * 140) > 0.82 ? 0.25 : 0));
    parts.push(eye);
    const palp = new THREE.ConeGeometry(0.05, 0.32, 6);
    palp.rotateX(Math.PI / 2 + 0.6); palp.translate(s * 0.035, -0.06, 1.1);
    paintVertices(palp, (x, y, z, c) => c.copy(y < -0.05 ? white : black));
    parts.push(palp);
    const ant = new THREE.CatmullRomCurve3([new THREE.Vector3(s * 0.06, 0.15, 0.98), new THREE.Vector3(s * 0.35, 0.65, 1.55), new THREE.Vector3(s * 0.62, 0.95, 2.15)]);
    const ag = taperedTube(ant, 14, 5, (t) => (t > 0.86 ? 0.022 + Math.sin((t - 0.86) / 0.14 * Math.PI) * 0.035 : 0.022), { capEnd: true });
    paintVertices(ag, (x, y, z, c) => c.copy(z > 2.08 ? white : black));
    parts.push(ag);
    const fore = new THREE.CatmullRomCurve3([new THREE.Vector3(s * 0.1, -0.16, 0.7), new THREE.Vector3(s * 0.16, -0.24, 0.85), new THREE.Vector3(s * 0.12, -0.16, 0.95)]);
    const fg = taperedTube(fore, 6, 4, () => 0.035, {});
    paintVertices(fg, (x, y, z, c) => c.set(0x3a2a1e));
    parts.push(fg);
  });
  parts.forEach((g) => { if (!g.attributes.uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); });
  return mergeGeos(parts);
}

const LEGS = [
  { side: 1, z: 0.52, rest: [[0.7, -0.62, 0.85]], fly: [0.3, -0.35, 0.65] },
  { side: -1, z: 0.52, rest: [[-0.7, -0.62, 0.85]], fly: [-0.3, -0.35, 0.65] },
  { side: 1, z: 0.32, rest: [[0.62, -0.62, -0.3]], fly: [0.28, -0.35, -0.25] },
  { side: -1, z: 0.32, rest: [[-0.62, -0.62, -0.3]], fly: [-0.28, -0.35, -0.25] },
];

export function buildAdult(opts) {
  const { tier } = opts;
  const seg = tier === 'low' ? 8 : tier === 'medium' ? 12 : 16;
  const root = new THREE.Group();
  const body = new THREE.Group();
  root.add(body);
  const rich = tier !== 'low';

  const bodyMat = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.7, sheen: rich ? 0.35 : 0, sheenColor: new THREE.Color(0x8a847c), sheenRoughness: 0.6 });
  const bodyMesh = new THREE.Mesh(bodyGeometry(seg), bodyMat);
  bodyMesh.castShadow = true;
  body.add(bodyMesh);

  const W = texSize(tier, 1024);
  const wc = wingCanvases(W);
  const tex = {};
  Object.entries(wc).forEach(([k, c]) => { tex[k] = canvasTexture(c, { anisotropy: 8 }); });
  const crumple = { value: 0 };
  const wingTime = { value: 0 };
  const vertDecl = 'uniform float uCrumple;\nuniform float uWingTime;\n';
  const vertBegin = `#include <begin_vertex>
    float cr = uCrumple;
    float rr = length(transformed.xz);
    transformed.xz *= mix(1.0, 0.36 + 0.1 * sin(rr * 3.0), cr);
    transformed.y += cr * (0.09 * sin(position.x * 9.0 + position.z * 4.0) * sin(position.z * 11.0) + 0.05 * sin(position.x * 23.0) * rr);
    transformed.y += cr * rr * -0.25;
    transformed.y += sin(uWingTime * 2.0 + rr * 2.0) * 0.01 * rr;`;
  const wingMat = (upper, under, key) => {
    const m = new THREE.MeshPhysicalMaterial({
      map: upper, side: THREE.DoubleSide, alphaTest: 0.5, roughness: 0.58, metalness: 0,
      sheen: rich ? 1 : 0, sheenColor: new THREE.Color(0xffd7a8), sheenRoughness: 0.32,
    });
    if (opts.antialias) m.alphaToCoverage = true;
    patchMaterial(m, { backMap: under, translucency: 0.7, transTint: 0xffb25a, uniforms: { uCrumple: crumple, uWingTime: wingTime }, vertDecl, vertBegin, key });
    return m;
  };
  const foreMat = wingMat(tex.fore_upper, tex.fore_under, 'wing-fore');
  const hindMat = wingMat(tex.hind_upper, tex.hind_under, 'wing-hind');
  const ws = tier === 'low' ? 14 : 24;
  const pivots = {};
  [1, -1].forEach((side) => {
    const name = side > 0 ? 'right' : 'left';
    const fore = new THREE.Group(); const hind = new THREE.Group();
    fore.position.set(side * 0.13, 0.12, 0.55);
    hind.position.set(side * 0.16, 0.09, 0.3);
    const fm = new THREE.Mesh(wingGeometry(FORE, side, ws), foreMat);
    const hm = new THREE.Mesh(wingGeometry(HIND, side, ws), hindMat);
    fm.rotation.y = side * 0.12; hm.rotation.y = side * -0.05;
    fm.castShadow = true; hm.castShadow = true;
    const depth = new THREE.MeshDepthMaterial({ alphaTest: 0.5, map: tex.fore_upper });
    fm.customDepthMaterial = depth;
    hm.customDepthMaterial = new THREE.MeshDepthMaterial({ alphaTest: 0.5, map: tex.hind_upper });
    fore.add(fm); hind.add(hm);
    body.add(fore, hind);
    pivots[name] = { fore, hind, side };
  });

  const legMat = new THREE.MeshStandardMaterial({ color: 0x1e1814, roughness: 0.6 });
  const legGeo = new THREE.CylinderGeometry(1, 0.8, 1, 5, 1);
  legGeo.translate(0, 0.5, 0); legGeo.rotateX(Math.PI / 2);
  const legs = new THREE.InstancedMesh(legGeo, legMat, LEGS.length * 3);
  legs.castShadow = true;
  legs.frustumCulled = false;
  body.add(legs);

  const probSeg = 36; const probRad = 5;
  const probGeo = new THREE.BufferGeometry();
  const probPos = new Float32Array((probSeg + 1) * (probRad + 1) * 3);
  probGeo.setAttribute('position', new THREE.BufferAttribute(probPos, 3));
  const pidx = [];
  for (let i = 0; i < probSeg; i++) for (let j = 0; j < probRad; j++) { const a = i * (probRad + 1) + j; const b = a + probRad + 1; pidx.push(a, b, a + 1, b, b + 1, a + 1); }
  probGeo.setIndex(pidx);
  const prob = new THREE.Mesh(probGeo, new THREE.MeshStandardMaterial({ color: 0x2a1d14, roughness: 0.45 }));
  prob.frustumCulled = false;
  body.add(prob);
  const probPts = Array.from({ length: probSeg + 1 }, () => new THREE.Vector3());

  function setProboscis(extend, reach, length) {
    const Lp = length ?? 1.45;
    let ang = -1.15 + extend * 0.15; let y = -0.12; let z = 1.03;
    for (let i = 0; i <= probSeg; i++) {
      const l = (i / probSeg) * Lp;
      probPts[i].set(0, y, z);
      const k = (1 - extend) * (3.5 + 16 * Math.pow(l / Lp, 1.4));
      ang -= k * (Lp / probSeg);
      const step = Lp / probSeg;
      const a2 = lerp(ang, reach ?? -1.35, extend * 0.75);
      y += Math.sin(a2) * step; z += Math.cos(a2) * step;
    }
    const n = new THREE.Vector3(); const b = new THREE.Vector3(); const t = new THREE.Vector3(); const X = new THREE.Vector3(1, 0, 0);
    for (let i = 0; i <= probSeg; i++) {
      t.subVectors(probPts[Math.min(probSeg, i + 1)], probPts[Math.max(0, i - 1)]).normalize();
      n.crossVectors(t, X).normalize(); b.crossVectors(t, n);
      const r = 0.022 * (1 - i / probSeg * 0.5);
      for (let j = 0; j <= probRad; j++) {
        const a = (j / probRad) * Math.PI * 2;
        const o = ((i * (probRad + 1)) + j) * 3;
        probPos[o] = probPts[i].x + (n.x * Math.cos(a) + b.x * Math.sin(a)) * r;
        probPos[o + 1] = probPts[i].y + (n.y * Math.cos(a) + b.y * Math.sin(a)) * r;
        probPos[o + 2] = probPts[i].z + (n.z * Math.cos(a) + b.z * Math.sin(a)) * r;
      }
    }
    probGeo.attributes.position.needsUpdate = true;
    probGeo.computeVertexNormals();
  }

  const m4 = new THREE.Matrix4(); const qq = new THREE.Quaternion(); const sc = new THREE.Vector3();
  const Z = new THREE.Vector3(0, 0, 1);
  function segment(i, a, b, r) {
    const d = new THREE.Vector3().subVectors(b, a); const len = d.length();
    qq.setFromUnitVectors(Z, d.normalize());
    m4.compose(a, qq, sc.set(r, r, len));
    legs.setMatrixAt(i, m4);
  }
  function setLegs(perch, grip = 0) {
    LEGS.forEach((L, li) => {
      const hip = new THREE.Vector3(L.side * 0.12, -0.16, L.z);
      const footRest = new THREE.Vector3(...L.rest[0]);
      const footFly = new THREE.Vector3(...L.fly);
      const foot = footFly.clone().lerp(footRest, perch);
      if (grip) foot.lerp(new THREE.Vector3(L.side * 0.2, -0.32, L.z > 0.4 ? 1.45 : 1.2), grip);
      const knee = hip.clone().lerp(foot, 0.42).add(new THREE.Vector3(L.side * 0.14, 0.32 * perch + 0.12, 0));
      const ankle = knee.clone().lerp(foot, 0.72);
      segment(li * 3, hip, knee, 0.035);
      segment(li * 3 + 1, knee, ankle, 0.028);
      segment(li * 3 + 2, ankle, foot, 0.02);
    });
    legs.instanceMatrix.needsUpdate = true;
  }

  function setWings(open, flapOffset = 0, sweep = 0) {
    const a = Math.PI / 2 * (1 - open) + flapOffset;
    pivots.right.fore.rotation.z = a + 0.02; pivots.right.hind.rotation.z = a;
    pivots.left.fore.rotation.z = -(a + 0.02); pivots.left.hind.rotation.z = -a;
    const tuck = Math.max(0, 1 - open * 3) * 0.18;
    pivots.right.fore.rotation.x = -tuck - sweep; pivots.left.fore.rotation.x = -tuck - sweep;
    pivots.right.hind.rotation.x = -sweep; pivots.left.hind.rotation.x = -sweep;
  }

  setLegs(1); setWings(0.6); setProboscis(0);

  return {
    root, body, pivots,
    setWings, setLegs, setProboscis,
    setCrumple(v) { crumple.value = v; },
    tick(time) { wingTime.value = time; },
    textures: [tex.fore_under, tex.hind_under],
    dispose() { tex.fore_under.dispose(); tex.hind_under.dispose(); },
  };
}
