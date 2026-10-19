import { THREE } from '../../core/engine.js';
import { rng, taperedTube, basisQuaternion, mergeGeos, paintVertices, canvasTexture, patchMaterial, texSize } from './kit.js';
import { leafHalfWidth, leafTextures, barkTexture, detailCanvas, LEAF_TEX_SPAN } from './textures.js';

const UP = new THREE.Vector3(0, 1, 0);

// A Calotropis leaf as an analytic surface, so eggs, caterpillars and bites can be placed exactly on it.
export function leafSurface(L, p) {
  const surf = (u, v, out = new THREE.Vector3()) => {
    const hw = leafHalfWidth(u) * L;
    const x = v * hw; const y = u * L;
    let z = p.cup * x * x / L - p.arch * L * u * u + p.rise * L * u;
    z += p.wave * L * 0.02 * Math.abs(v * v * v) * Math.sin(u * 22 + p.phase);
    z += p.twist * x * u;
    z -= 0.004 * L * Math.exp(-((x / (0.012 * L)) ** 2)) * (1 - u);
    return out.set(x, y, z);
  };
  const a = new THREE.Vector3(); const b = new THREE.Vector3(); const c = new THREE.Vector3(); const d = new THREE.Vector3();
  const normal = (u, v, out = new THREE.Vector3()) => {
    const e = 0.01;
    surf(u, Math.min(1, v + e), a); surf(u, Math.max(-1, v - e), b);
    surf(Math.min(1, u + e), v, c); surf(Math.max(0, u - e), v, d);
    return out.crossVectors(a.sub(b), c.sub(d)).normalize();
  };
  const geometry = (segU, segV) => {
    const pos = []; const uv = []; const idx = [];
    const P = new THREE.Vector3();
    for (let i = 0; i <= segU; i++) {
      const u = Math.pow(i / segU, 0.92);
      for (let j = 0; j <= segV; j++) {
        const v = (j / segV) * 2 - 1;
        surf(u, v, P);
        pos.push(P.x, P.y, P.z);
        uv.push(0.5 + P.x / (L * LEAF_TEX_SPAN), u);
      }
    }
    for (let i = 0; i < segU; i++) {
      for (let j = 0; j < segV; j++) {
        const q = i * (segV + 1) + j; const r = q + segV + 1;
        idx.push(q, q + 1, r, r, q + 1, r + 1);
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
    g.setIndex(idx);
    g.computeVertexNormals();
    return g;
  };
  return { L, surf, normal, geometry };
}

const LEAF_VARIANTS = [
  { cup: 0.55, arch: 0.16, rise: 0.08, wave: 0.6, phase: 0.4, twist: 0.04 },
  { cup: 0.8, arch: 0.24, rise: 0.12, wave: 1.0, phase: 2.1, twist: -0.06 },
];

function flowerGeometry(seg) {
  const parts = [];
  const lav = new THREE.Color(0xc7b2e2); const tip = new THREE.Color(0x6f45a0); const white = new THREE.Color(0xf0eaf8);
  for (let k = 0; k < 5; k++) {
    const g = new THREE.PlaneGeometry(1, 1, 6, 3);
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const s = p.getX(i) + 0.5; const w = p.getY(i);
      const r = 0.26 + s * 1.5;
      const half = 0.42 * Math.sin(Math.PI * Math.pow(s, 0.7)) * (1 - s * 0.45) + 0.07 * (1 - s);
      const x = w * half * 2 * 0.9;
      const y = -1.0 * s * s + 0.1 * s - 0.1 * (w * w) * (1 + s);
      p.setXYZ(i, r, y, x);
    }
    paintVertices(g, (x, y, z, col) => { const s = (x - 0.26) / 1.5; col.copy(lav).lerp(tip, Math.pow(Math.max(0, s - 0.45) / 0.55, 1.4) * 0.9).lerp(white, Math.max(0, 0.3 - s)); });
    g.rotateY((k / 5) * Math.PI * 2 + Math.PI / 10);
    parts.push(g);
  }
  for (let k = 0; k < 5; k++) {
    const g = new THREE.SphereGeometry(0.2, seg, Math.max(6, seg - 2));
    g.scale(0.5, 1.25, 0.62);
    g.translate(0.36, 0.36, 0);
    g.rotateZ(-0.08);
    g.rotateZ(-0.12);
    const spur = new THREE.TorusGeometry(0.13, 0.05, 5, 10, Math.PI * 1.2);
    spur.rotateY(Math.PI / 2); spur.rotateX(-0.3);
    spur.translate(0.5, 0.12, 0);
    [g, spur].forEach((geo) => {
      paintVertices(geo, (x, y, z, col) => col.set(0xf6f2fa).lerp(new THREE.Color(0x7a4aa8), Math.min(1, Math.max(0, 0.36 - y) * 2.6)));
      geo.rotateY((k / 5) * Math.PI * 2 + Math.PI / 10);
      parts.push(geo);
    });
  }
  const col = new THREE.CylinderGeometry(0.3, 0.26, 0.6, 5, 1);
  col.translate(0, 0.32, 0);
  paintVertices(col, (x, y, z, c) => c.set(y > 0.55 ? 0xfbf8ff : 0xe5dcef));
  parts.push(col);
  const calyx = new THREE.ConeGeometry(0.32, 0.4, 5, 1, true);
  calyx.rotateX(Math.PI); calyx.translate(0, -0.12, 0);
  paintVertices(calyx, (x, y, z, c) => c.set(0x86a273));
  parts.push(calyx);
  return mergeGeos(parts.map((g) => (g.index ? g : g)).map((g) => { if (!g.attributes.uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); return g; }));
}

function budGeometry(seg) {
  const pts = [];
  for (let i = 0; i <= 12; i++) { const t = i / 12; pts.push(new THREE.Vector2(Math.sin(Math.PI * t) * 0.62 * (1 - 0.15 * t) + 0.001, -Math.cos(Math.PI * t) * 0.55 + 0.55)); }
  const g = new THREE.LatheGeometry(pts, seg * 2);
  const p = g.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i); const z = p.getZ(i); const a = Math.atan2(z, x);
    const k = 1 + 0.13 * Math.cos(5 * a);
    p.setX(i, x * k); p.setZ(i, z * k);
  }
  g.computeVertexNormals();
  paintVertices(g, (x, y, z, c) => c.set(0xbac7a6).lerp(new THREE.Color(0xc4afd8), Math.min(1, Math.max(0, y - 0.5) * 1.6)));
  return g;
}

export function buildPlant(opts) {
  const { tier } = opts;
  const rand = rng(17);
  const group = new THREE.Group();
  const seg = tier === 'low' ? 6 : tier === 'medium' ? 8 : 12;
  const tex = leafTextures(texSize(tier, 1024), 3);
  const leafMap = canvasTexture(tex.front, { anisotropy: 8 });
  const leafBack = canvasTexture(tex.back, { anisotropy: 8 });
  const leafBump = canvasTexture(tex.bump, { color: false });
  const rich = tier !== 'low';
  const leafParams = {
    map: leafMap, side: THREE.DoubleSide, roughness: 0.58, metalness: 0,
    bumpMap: rich ? leafBump : null, bumpScale: 1.2,
  };
  const leafMat = rich
    ? new THREE.MeshPhysicalMaterial({ ...leafParams, sheen: 0.25, sheenColor: new THREE.Color(0xc4d8b8), sheenRoughness: 0.5, clearcoat: 0.25, clearcoatRoughness: 0.42 })
    : new THREE.MeshStandardMaterial(leafParams);
  const detail = canvasTexture(detailCanvas(256), { color: false, repeat: 1 });
  const leafPatch = {
    backMap: leafBack, translucency: 0.6, transTint: 0xd0f070,
    uniforms: { detailMap: { value: detail } },
    fragDecl: 'uniform sampler2D detailMap;\n',
    fragMap: '#ifdef USE_MAP\n vec4 sampledDiffuseColor = gl_FrontFacing ? texture2D( map, vMapUv ) : texture2D( backMap, vMapUv );\n float dtl = texture2D( detailMap, vMapUv * 16.0 ).r * 0.6 + texture2D( detailMap, vMapUv * 61.0 ).r * 0.4;\n sampledDiffuseColor.rgb *= 0.78 + 0.44 * dtl;\n diffuseColor *= sampledDiffuseColor;\n#endif',
  };
  patchMaterial(leafMat, { ...leafPatch, key: 'leaf' });

  const barkCanvas = barkTexture(texSize(tier, 512), 5);
  const barkMap = canvasTexture(barkCanvas);
  barkMap.wrapS = barkMap.wrapT = THREE.RepeatWrapping;
  const barkMat = new THREE.MeshStandardMaterial({ map: barkMap, roughness: 0.85, bumpMap: rich ? barkMap : null, bumpScale: 0.6, color: 0xf0f2e8 });

  const axes = {
    main: { pts: [[0, 0, 0], [0.6, 12, 0.3], [1.0, 26, 0], [0.5, 40, -0.6], [0.3, 50, 0.2]], r0: 1.25, r1: 0.42 },
    a: { pts: [[0.6, 23.5, 0.2], [6, 26.8, 2.8], [13, 28.6, 4.6], [19.5, 30.8, 5.4]], r0: 0.62, r1: 0.26 },
    b: { pts: [[0.7, 31, -0.3], [-4.6, 34.6, -2.8], [-9.6, 39.6, -4.6], [-12.6, 45, -5.2]], r0: 0.5, r1: 0.22 },
  };
  const stemGeos = [];
  Object.values(axes).forEach((ax) => {
    ax.curve = new THREE.CatmullRomCurve3(ax.pts.map((p) => new THREE.Vector3(...p)));
    const len = ax.curve.getLength();
    const radius = (t) => ax.r0 + (ax.r1 - ax.r0) * Math.pow(t, 0.8) + (t < 0.03 && ax === axes.main ? (0.03 - t) * 8 : 0);
    ax.radius = radius;
    stemGeos.push(taperedTube(ax.curve, Math.round(len * 1.2), seg + 2, radius, { vRepeat: len / 6, capEnd: true }));
  });

  const leaves = [];
  const nodes = [
    { ax: 'main', ts: [0.22, 0.36, 0.5, 0.63, 0.75, 0.86], L: [15, 15.5, 14, 12, 10, 7] },
    { ax: 'a', ts: [0.3, 0.55, 0.78, 0.96], L: [14, 12.5, 9.5, 6] },
    { ax: 'b', ts: [0.35, 0.6, 0.82, 0.97], L: [12, 10, 7.5, 5] },
  ];
  const T = new THREE.Vector3(); const P = new THREE.Vector3();
  nodes.forEach(({ ax, ts, L }) => {
    const axis = axes[ax];
    ts.forEach((t, ni) => {
      axis.curve.getPointAt(t, P); axis.curve.getTangentAt(t, T);
      const r = axis.radius(t);
      const side = new THREE.Vector3().crossVectors(T, Math.abs(T.y) > 0.9 ? new THREE.Vector3(1, 0, 0) : UP).normalize();
      const other = new THREE.Vector3().crossVectors(T, side).normalize();
      const rot = (ni % 2) * Math.PI / 2 + (ax === 'main' ? 0.35 : 0);
      [0, Math.PI].forEach((off, k) => {
        const a = rot + off;
        const perp = side.clone().multiplyScalar(Math.cos(a)).addScaledVector(other, Math.sin(a));
        const dir = perp.clone().addScaledVector(T, 0.45).addScaledVector(UP, 0.22).normalize();
        if (dir.y < -0.25) { dir.y = -0.25; dir.normalize(); }
        const upHint = UP.clone().addScaledVector(T, 0.35).addScaledVector(dir, -0.2).normalize();
        const quat = basisQuaternion(dir, upHint);
        const len = L[ni] * (0.92 + rand() * 0.16);
        const pet = 0.25 + len * 0.03;
        const base = P.clone().addScaledVector(perp, r * 0.8).addScaledVector(dir, pet);
        const petCurve = new THREE.QuadraticBezierCurve3(P.clone(), P.clone().addScaledVector(perp, r + pet * 0.5).addScaledVector(UP, 0.1), base.clone());
        stemGeos.push(taperedTube(petCurve, 5, seg, (q) => 0.14 + len * 0.009 - q * 0.05, {}));
        leaves.push({ ax, ni, k, len, base, quat, dir, variant: (ni + k) % 2, phase: rand() * 6.28, amp: 0.035 + 0.02 * (len < 9 ? 1 : 0), yellow: ax === 'main' && ni === 0 && k === 1 });
      });
    });
  });

  const stem = new THREE.Mesh(mergeGeos(stemGeos), barkMat);
  stem.castShadow = true; stem.receiveShadow = true;
  stem.name = 'stem';
  group.add(stem);

  const pick = (fn) => leaves.reduce((best, l) => (fn(l) > fn(best) ? l : best), leaves[0]);
  const catLeaf = pick((l) => (l.ax === 'a' && l.ni === 1 ? 10 + l.dir.z : -99));
  const eggLeaf = pick((l) => (l.ax === 'main' && l.ni === 4 ? 10 + l.dir.z + l.dir.x * 0.4 : -99));
  catLeaf.hero = 'caterpillar'; eggLeaf.hero = 'egg';

  const heroes = {};
  const instancedSets = LEAF_VARIANTS.map(() => []);
  leaves.forEach((l) => {
    if (l.hero) {
      const surface = leafSurface(l.len, { ...LEAF_VARIANTS[l.variant], arch: l.hero === 'caterpillar' ? 0.1 : LEAF_VARIANTS[l.variant].arch, wave: l.hero === 'caterpillar' ? 0.25 : 0.6 });
      const mat = l.hero === 'caterpillar' ? leafMat.clone() : leafMat;
      if (mat !== leafMat) patchMaterial(mat, { ...leafPatch, key: 'leaf-hero' });
      const mesh = new THREE.Mesh(surface.geometry(tier === 'low' ? 26 : 40, tier === 'low' ? 12 : 20), mat);
      mesh.castShadow = true; mesh.receiveShadow = true;
      const holder = new THREE.Group();
      holder.position.copy(l.base); holder.quaternion.copy(l.quat);
      holder.add(mesh);
      group.add(holder);
      l.holder = holder;
      heroes[l.hero] = { leaf: l, holder, mesh, surface, material: mat };
    } else {
      instancedSets[l.variant].push(l);
    }
  });
  const unitSurfaces = LEAF_VARIANTS.map((v) => leafSurface(1, v));
  const instanced = instancedSets.map((set, vi) => {
    const geo = unitSurfaces[vi].geometry(tier === 'low' ? 16 : 26, tier === 'low' ? 8 : 12);
    const im = new THREE.InstancedMesh(geo, leafMat, set.length);
    im.castShadow = true; im.receiveShadow = true;
    const c = new THREE.Color();
    set.forEach((l, i) => {
      c.setRGB(0.92 + rand() * 0.14, 0.95 + rand() * 0.1, 0.9 + rand() * 0.12);
      if (l.yellow) c.setRGB(1.45, 1.25, 0.55);
      im.setColorAt(i, c);
    });
    group.add(im);
    return { im, set };
  });

  const flowerGeo = flowerGeometry(seg);
  const budGeo = budGeometry(seg);
  const flowerMat = new THREE.MeshPhysicalMaterial({ vertexColors: true, color: 0xd8d8d8, roughness: 0.5, sheen: rich ? 0.8 : 0, sheenColor: new THREE.Color(0xf6eaff), sheenRoughness: 0.4, side: THREE.DoubleSide });
  patchMaterial(flowerMat, { translucency: 0.35, transTint: 0xf0e0ff, key: 'flower' });
  const budMat = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.4, sheen: rich ? 0.5 : 0, sheenColor: new THREE.Color(0xffffff), clearcoat: 0.2 });
  const pedMat = new THREE.MeshStandardMaterial({ color: 0x9cb38c, roughness: 0.6 });
  const umbels = [];
  const dummy = new THREE.Object3D();
  function umbel(axisName, t, dirHint, nFlowers, nBuds, pedLen) {
    const ax = axes[axisName];
    const base = ax.curve.getPointAt(t);
    const g = new THREE.Group();
    g.position.copy(base);
    const dir = dirHint.clone().normalize();
    const tip = dir.clone().multiplyScalar(pedLen);
    const pedCurve = new THREE.QuadraticBezierCurve3(new THREE.Vector3(), dir.clone().multiplyScalar(pedLen * 0.5).add(new THREE.Vector3(0, pedLen * 0.15, 0)), tip.clone());
    const geos = [taperedTube(pedCurve, 10, seg, (q) => 0.24 - q * 0.08, {})];
    const flowers = []; const buds = [];
    const total = nFlowers + nBuds;
    for (let i = 0; i < total; i++) {
      const isBud = i >= nFlowers;
      const theta = i === 0 ? 0.12 : 0.35 + rand() * 0.95 + (isBud ? 0.15 : 0);
      const phi = i * 2.399 + rand() * 0.3;
      const d = new THREE.Vector3(Math.sin(theta) * Math.cos(phi), Math.cos(theta), Math.sin(theta) * Math.sin(phi));
      const q = new THREE.Quaternion().setFromUnitVectors(UP, dir);
      d.applyQuaternion(q);
      const len = 2.6 + rand() * 0.9 - (isBud ? 0.5 : 0);
      const end = tip.clone().addScaledVector(d, len);
      const c = new THREE.QuadraticBezierCurve3(tip.clone(), tip.clone().addScaledVector(d, len * 0.5).add(new THREE.Vector3(0, len * 0.12, 0)), end.clone());
      geos.push(taperedTube(c, 6, Math.max(4, seg - 4), () => 0.07, {}));
      const ft = c.getTangentAt(1);
      const m = new THREE.Matrix4().compose(end, new THREE.Quaternion().setFromUnitVectors(UP, ft), new THREE.Vector3(1, 1, 1).multiplyScalar(isBud ? 0.8 + rand() * 0.4 : 0.95 + rand() * 0.1));
      (isBud ? buds : flowers).push({ m, end, axis: ft.clone() });
    }
    const ped = new THREE.Mesh(mergeGeos(geos), pedMat); ped.castShadow = true;
    g.add(ped);
    const fim = new THREE.InstancedMesh(flowerGeo, flowerMat, flowers.length);
    flowers.forEach((f, i) => fim.setMatrixAt(i, f.m));
    fim.castShadow = true;
    const bim = new THREE.InstancedMesh(budGeo, budMat, buds.length);
    buds.forEach((b, i) => bim.setMatrixAt(i, b.m));
    bim.castShadow = true;
    g.add(fim, bim);
    group.add(g);
    const u = { group: g, flowers, buds, phase: rand() * 6.28 };
    umbels.push(u);
    return u;
  }
  const mainUmbel = umbel('main', 0.93, new THREE.Vector3(0.18, 1, 0.32), 11, 7, 6);
  umbel('a', 0.9, new THREE.Vector3(0.5, 1, 0.2), 6, 8, 4.5);
  umbel('b', 0.92, new THREE.Vector3(-0.4, 1, -0.3), 4, 6, 4);

  const chrysAxis = axes.a;
  const chrysT = 0.42;
  const cp = chrysAxis.curve.getPointAt(chrysT);
  const chrysalisAnchor = { position: cp.clone().add(new THREE.Vector3(0, -chrysAxis.radius(chrysT) * 0.92, 0)), tangent: chrysAxis.curve.getTangentAt(chrysT) };

  const heroFlower = mainUmbel.flowers[0];
  const perch = { group: mainUmbel.group, position: heroFlower.end.clone().addScaledVector(heroFlower.axis, 0.7), axis: heroFlower.axis.clone() };

  const q = new THREE.Quaternion(); const qa = new THREE.Quaternion(); const s = new THREE.Vector3(); const xAxis = new THREE.Vector3(1, 0, 0); const yAxis = new THREE.Vector3(0, 1, 0);
  const mtx = new THREE.Matrix4();
  function swayQuat(l, time, wind, out) {
    const a = Math.sin(time * 1.3 + l.phase) * l.amp * wind + Math.sin(time * 3.1 + l.phase * 2) * l.amp * 0.35 * wind;
    const b = Math.sin(time * 0.9 + l.phase * 1.7) * l.amp * 0.6 * wind;
    out.copy(l.quat).multiply(qa.setFromAxisAngle(xAxis, a)).multiply(q.setFromAxisAngle(yAxis, b));
    return out;
  }
  const out = new THREE.Quaternion();
  function update(time, wind = 1) {
    instanced.forEach(({ im, set }) => {
      set.forEach((l, i) => {
        swayQuat(l, time, wind, out);
        s.setScalar(l.len);
        mtx.compose(l.base, out, s);
        im.setMatrixAt(i, mtx);
      });
      im.instanceMatrix.needsUpdate = true;
    });
    Object.values(heroes).forEach(({ leaf, holder }) => { swayQuat(leaf, time, wind * (leaf.hero === 'egg' ? 0.6 : 0.35), holder.quaternion); });
    umbels.forEach((u) => {
      u.group.rotation.x = Math.sin(time * 0.8 + u.phase) * 0.025 * wind;
      u.group.rotation.z = Math.sin(time * 1.1 + u.phase * 1.3) * 0.03 * wind;
    });
  }
  update(0, 0);

  return {
    group, heroes, chrysalisAnchor, perch, umbels, axes, update,
    textures: [leafMap, leafBack, leafBump, barkMap],
    leafCanvas: tex,
    dispose() { [leafBack, detail].forEach((t) => t.dispose()); },
  };
}
