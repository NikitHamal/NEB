import { THREE } from '../../core/engine.js';
import { rng, patchMaterial, makeCanvas, canvasTexture, clamp, lerp } from '../butterfly/kit.js';
import { MoleculeSwarm } from './molecules.js';

const W = 40; const D = 22;
const Y = { lowEpi: [0.6, 3.2], spongy: [3.2, 10.6], palisade: [10.8, 19.6], upEpi: [19.8, 22.4], cuticle: 22.4 };
const STOMATA = [new THREE.Vector3(-12, 1.9, -3.5), new THREE.Vector3(13, 1.9, 4.5), new THREE.Vector3(-1, 1.9, 7.5)];
const VEIN = new THREE.Vector3(5, 7.2, 0);

function rimPatch(material, color, power, key, extra = {}) {
  return patchMaterial(material, {
    ...extra,
    fragDecl: `uniform vec3 uRim;\n${extra.fragDecl || ''}`,
    uniforms: { uRim: { value: new THREE.Color(color) }, ...(extra.uniforms || {}) },
    fragEnd: `float rimK = pow(1.0 - abs(dot(normalize(normal), normalize(vViewPosition))), ${power.toFixed(1)}); gl_FragColor.rgb += uRim * rimK * 0.3;`,
    key,
  });
}

// Chloroplasts circulate along the cell wall (cytoplasmic streaming). Each instance carries its cell
// and phase; the vertex shader places and orients it, so the CPU does no per-frame work.
function chloroplastInstances(cells, perCellFn, tier, time) {
  const geo = new THREE.SphereGeometry(1, tier === 'low' ? 8 : 12, tier === 'low' ? 6 : 8);
  geo.scale(0.6, 0.42, 0.24);
  const n = cells.reduce((a, c) => a + perCellFn(c), 0);
  const aCell = new Float32Array(n * 4); const aShape = new Float32Array(n * 4);
  let k = 0;
  cells.forEach((c) => {
    const perCell = perCellFn(c);
    for (let i = 0; i < perCell; i++) {
      aCell[k * 4] = c.x; aCell[k * 4 + 1] = c.y; aCell[k * 4 + 2] = c.z; aCell[k * 4 + 3] = c.r;
      aShape[k * 4] = (i / perCell) * Math.PI * 2 + Math.random() * 0.4;
      aShape[k * 4 + 1] = c.h;
      aShape[k * 4 + 2] = Math.random() * 6.28;
      aShape[k * 4 + 3] = c.round ? 1 : 0;
      k++;
    }
  });
  geo.setAttribute('aCell', new THREE.InstancedBufferAttribute(aCell, 4));
  geo.setAttribute('aShape', new THREE.InstancedBufferAttribute(aShape, 4));
  const mat = new THREE.MeshStandardMaterial({ color: 0x2a9a1c, roughness: 0.28, emissive: 0x1a6a0e, emissiveIntensity: 0.45 });
  const glow = { value: 0.4 };
  patchMaterial(mat, {
    uniforms: { uTime: time, uGlow: glow },
    vertDecl: 'uniform float uTime;\nattribute vec4 aCell;\nattribute vec4 aShape;\n',
    vertNormal: `
      float ang = aShape.x + uTime * (0.35 + 0.1 * sin(aShape.z));
      float vy = aShape.w > 0.5 ? sin(aShape.z + uTime * 0.21) * 0.8 : sin(ang * 1.0 + aShape.z * 3.0) * 0.85;
      vec3 R = vec3(cos(ang), 0.0, sin(ang));
      float rr = aCell.w * (aShape.w > 0.5 ? sqrt(max(0.0, 1.0 - vy * vy)) : 1.0) * 0.97 + 0.06;
      vec3 Tg = vec3(-sin(ang), 0.0, cos(ang));
      vec3 objectNormal = normalize(Tg * normal.x + vec3(0.0, 1.0, 0.0) * normal.y + R * normal.z);
      #ifdef USE_TANGENT
      vec3 objectTangent = vec3(tangent.xyz);
      #endif`,
    vertBegin: `
      vec3 center = aCell.xyz + vec3(0.0, vy * (aShape.w > 0.5 ? aCell.w : aShape.y), 0.0) + R * rr;
      vec3 transformed = center + Tg * position.x + vec3(0.0, 1.0, 0.0) * position.y + R * position.z;`,
    fragDecl: 'uniform float uGlow;\n',
    fragEnd: 'gl_FragColor.rgb += vec3(0.25, 0.65, 0.12) * uGlow * 0.35;',
    key: 'chloro',
  });
  const mesh = new THREE.InstancedMesh(geo, mat, n);
  mesh.frustumCulled = false;
  return { mesh, glow };
}

function ringTexture() {
  const c = makeCanvas(64, 256); const g = c.getContext('2d');
  g.fillStyle = '#d9e7c4'; g.fillRect(0, 0, 64, 256);
  g.strokeStyle = '#8a6b3a'; g.lineWidth = 5;
  for (let y = 4; y < 256; y += 16) { g.beginPath(); g.moveTo(0, y); g.lineTo(64, y + 6); g.stroke(); }
  return c;
}

export function buildLeafSection({ tier }) {
  const rand = rng(5);
  const group = new THREE.Group();
  const time = { value: 0 };
  const rich = tier !== 'low';

  const cellMat = new THREE.MeshPhysicalMaterial({ color: 0xb4dc96, roughness: 0.38, transparent: false, sheen: rich ? 0.6 : 0, sheenColor: new THREE.Color(0xe8ffd0), clearcoat: rich ? 0.4 : 0, clearcoatRoughness: 0.3 });
  rimPatch(cellMat, 0x6fbf4a, 2.5, 'cell-rim', { translucency: 0.5, transTint: 0xb8f080 });
  const epiMat = new THREE.MeshPhysicalMaterial({ color: 0xd9ecc4, roughness: 0.3, clearcoat: rich ? 0.6 : 0, transparent: true, opacity: 0.7, depthWrite: true });
  rimPatch(epiMat, 0x9ad8b0, 2.0, 'epi-rim');

  const palCells = [];
  const nx = tier === 'low' ? 9 : 12; const nz = tier === 'low' ? 5 : 7;
  for (let i = 0; i < nx; i++) {
    for (let j = 0; j < nz; j++) {
      const x = -W / 2 + (i + 0.5 + (j % 2) * 0.35) * (W / nx) + (rand() - 0.5) * 0.4;
      const z = -D / 2 + (j + 0.5) * (D / nz) + (rand() - 0.5) * 0.3;
      if (x > W / 2 - 1.2) continue;
      palCells.push({ x, y: (Y.palisade[0] + Y.palisade[1]) / 2, z, r: Math.min(W / nx, D / nz) * 0.46, h: (Y.palisade[1] - Y.palisade[0]) / 2 - 0.4 });
    }
  }
  const palGeo = new THREE.CapsuleGeometry(1, 1, 6, tier === 'low' ? 10 : 16);
  const pal = new THREE.InstancedMesh(palGeo, cellMat, palCells.length);
  const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const s = new THREE.Vector3(); const p = new THREE.Vector3(); const e = new THREE.Euler();
  palCells.forEach((c, i) => {
    const len = c.h * 2 - c.r * 2;
    m4.compose(p.set(c.x, c.y, c.z), q.setFromEuler(e.set((rand() - 0.5) * 0.06, rand() * 3, (rand() - 0.5) * 0.06)), s.set(c.r, Math.max(0.1, len), c.r));
    pal.setMatrixAt(i, m4);
  });
  group.add(pal);

  const spCells = [];
  const avoid = (x, y, z) => STOMATA.some((st) => Math.hypot(x - st.x, z - st.z) < 3 && y < 7) || Math.hypot(x - VEIN.x, y - VEIN.y) < 4.6;
  let tries = 0;
  while (spCells.length < (tier === 'low' ? 26 : 44) && tries < 2000) {
    tries++;
    const r = 1.4 + rand() * 0.9;
    const x = -W / 2 + r + rand() * (W - 2 * r); const z = -D / 2 + r + rand() * (D - 2 * r); const y = Y.spongy[0] + r + rand() * (Y.spongy[1] - Y.spongy[0] - 2 * r);
    if (avoid(x, y, z)) continue;
    if (spCells.some((c) => Math.hypot(c.x - x, c.y - y, c.z - z) < (c.r + r) * 0.98)) continue;
    spCells.push({ x, y, z, r, h: r, round: true });
  }
  const blob = new THREE.IcosahedronGeometry(1, tier === 'low' ? 2 : 3);
  const bp = blob.attributes.position;
  for (let i = 0; i < bp.count; i++) { p.fromBufferAttribute(bp, i); p.multiplyScalar(1 + 0.12 * Math.sin(p.x * 3.1) * Math.cos(p.y * 2.7 + p.z * 2)); bp.setXYZ(i, p.x, p.y, p.z); }
  const bn = new Float32Array(bp.count * 3);
  for (let i = 0; i < bp.count; i++) { p.fromBufferAttribute(bp, i).normalize(); bn[i * 3] = p.x; bn[i * 3 + 1] = p.y; bn[i * 3 + 2] = p.z; }
  blob.setAttribute('normal', new THREE.BufferAttribute(bn, 3));
  const sponge = new THREE.InstancedMesh(blob, cellMat, spCells.length);
  spCells.forEach((c, i) => { m4.compose(p.set(c.x, c.y, c.z), q.setFromEuler(e.set(rand() * 3, rand() * 3, rand() * 3)), s.set(c.r, c.r * 0.85, c.r * 1.1)); sponge.setMatrixAt(i, m4); });
  group.add(sponge);

  const chl = chloroplastInstances([...palCells, ...spCells.map((c) => ({ ...c }))], (c) => (c.round ? (tier === 'low' ? 4 : 7) : (tier === 'low' ? 8 : tier === 'medium' ? 12 : 18)), tier, time);
  group.add(chl.mesh);

  const epiGeo = new THREE.BoxGeometry(1, 1, 1, 2, 2, 2);
  const ep = epiGeo.attributes.position;
  for (let i = 0; i < ep.count; i++) { p.fromBufferAttribute(ep, i); const k = 1 - 0.18 * (Math.abs(p.x * 2) ** 4 + Math.abs(p.z * 2) ** 4) * 0.5; ep.setXYZ(i, p.x * k, p.y, p.z * k); }
  epiGeo.computeVertexNormals();
  const epiCells = [];
  [['up', Y.upEpi], ['low', Y.lowEpi]].forEach(([which, [y0, y1]]) => {
    const cw = 3.4; const cd = 3.1;
    for (let x = -W / 2 + cw / 2; x < W / 2; x += cw) {
      for (let z = -D / 2 + cd / 2; z < D / 2; z += cd) {
        if (which === 'low' && STOMATA.some((st) => Math.abs(x - st.x) < 2.4 && Math.abs(z - st.z) < 2.2)) continue;
        epiCells.push({ x: x + (rand() - 0.5) * 0.3, y: (y0 + y1) / 2, z, w: cw * 0.96, h: (y1 - y0) * 0.94, d: cd * 0.95 });
      }
    }
  });
  const epi = new THREE.InstancedMesh(epiGeo, epiMat, epiCells.length);
  epiCells.forEach((c, i) => { m4.compose(p.set(c.x, c.y, c.z), q.identity(), s.set(c.w, c.h, c.d)); epi.setMatrixAt(i, m4); });
  epi.renderOrder = 2;
  group.add(epi);

  const cuticleMat = new THREE.MeshPhysicalMaterial({ color: 0xe9f7c9, roughness: 0.12, clearcoat: 1, transparent: true, opacity: 0.45, depthWrite: false });
  const cuticle = new THREE.Mesh(new THREE.BoxGeometry(W + 0.2, 0.45, D + 0.2), cuticleMat);
  cuticle.position.y = Y.cuticle + 0.22; cuticle.renderOrder = 3;
  const lowCut = cuticle.clone(); lowCut.position.y = Y.lowEpi[0] - 0.22; lowCut.scale.y = 0.6;
  group.add(cuticle, lowCut);

  const sheathMat = new THREE.MeshPhysicalMaterial({ color: 0xc6e3a2, roughness: 0.4 });
  rimPatch(sheathMat, 0x8fcf6a, 2.5, 'sheath-rim');
  const ringCount = 12; const rows = tier === 'low' ? 6 : 9;
  const sheath = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 12, 10), sheathMat, ringCount * rows);
  let si = 0;
  for (let r = 0; r < rows; r++) {
    const z = -D / 2 + (r + 0.5) * (D / rows);
    for (let k = 0; k < ringCount; k++) {
      const a = (k / ringCount) * Math.PI * 2 + r * 0.26;
      m4.compose(p.set(VEIN.x + Math.cos(a) * 3.5, VEIN.y + Math.sin(a) * 3.2, z), q.identity(), s.set(0.95, 0.95, D / rows * 0.55));
      sheath.setMatrixAt(si++, m4);
    }
  }
  group.add(sheath);
  const ringTex = canvasTexture(ringTexture(), { anisotropy: 4 });
  ringTex.wrapT = THREE.RepeatWrapping; ringTex.repeat.set(1, 6);
  const xylemMat = new THREE.MeshPhysicalMaterial({ map: ringTex, roughness: 0.4, side: THREE.DoubleSide, clearcoat: 0.4 });
  const phloemMat = new THREE.MeshPhysicalMaterial({ color: 0xa7c98a, roughness: 0.5 });
  const vessel = new THREE.CylinderGeometry(1, 1, D, 18, 1, true); vessel.rotateX(Math.PI / 2);
  [[-1.1, 1.1, 0.95], [0.9, 1.3, 0.8], [0.0, 2.0, 0.7], [-0.2, 0.2, 0.55]].forEach(([dx, dy, r]) => {
    const v = new THREE.Mesh(vessel, xylemMat); v.position.set(VEIN.x + dx, VEIN.y + dy - 0.6, 0); v.scale.set(r, r, 1); group.add(v);
  });
  [[-1.2, -1.5, 0.45], [0, -1.8, 0.5], [1.2, -1.4, 0.42], [-0.5, -0.9, 0.35], [0.7, -0.7, 0.35]].forEach(([dx, dy, r]) => {
    const v = new THREE.Mesh(vessel, phloemMat); v.position.set(VEIN.x + dx, VEIN.y + dy, 0); v.scale.set(r, r, 1); group.add(v);
  });
  const waterFlow = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, D, 10, 1, true).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0x5ab8ff, transparent: true, opacity: 0.55, depthWrite: false }));
  waterFlow.position.set(VEIN.x - 1.1, VEIN.y + 0.5, 0); waterFlow.scale.set(1.5, 1.5, 0.999);
  group.add(waterFlow);

  const guardMat = new THREE.MeshPhysicalMaterial({ color: 0x7ccf5a, roughness: 0.35, clearcoat: 0.5 });
  rimPatch(guardMat, 0x9cff7a, 2.2, 'guard-rim');
  const poreMat = new THREE.MeshBasicMaterial({ color: 0x0a1a10 });
  const guards = [];
  STOMATA.forEach((st) => {
    const sg = new THREE.Group();
    sg.position.copy(st);
    const cells = [-1, 1].map((sd) => {
      const t = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.6, 12, 24, Math.PI), guardMat);
      t.rotation.x = Math.PI / 2; t.rotation.z = sd > 0 ? -Math.PI / 2 : Math.PI / 2;
      sg.add(t);
      return t;
    });
    const pore = new THREE.Mesh(new THREE.CircleGeometry(1, 20), poreMat);
    pore.rotation.x = Math.PI / 2; pore.position.y = -0.2;
    sg.add(pore);
    const chamber = new THREE.Mesh(new THREE.SphereGeometry(2.4, 16, 10, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0x0d2618, transparent: true, opacity: 0.5, depthWrite: false, side: THREE.BackSide }));
    chamber.position.y = 0.6;
    sg.add(chamber);
    group.add(sg);
    guards.push({ group: sg, cells, pore });
  });

  const farMat = new THREE.MeshStandardMaterial({ color: 0x3d7a3a, roughness: 0.7, transparent: true, opacity: 0.5, depthWrite: false });
  [[-60, 14, -70, 10], [55, 4, -80, 12], [10, 30, -110, 14], [-30, -12, -90, 9]].forEach(([x, y, z, r]) => {
    const b = new THREE.Mesh(new THREE.CapsuleGeometry(r * 0.5, r * 1.6, 6, 16), farMat);
    b.position.set(x, y, z);
    group.add(b);
  });

  const lightTex = canvasTexture((() => { const c = makeCanvas(64, 256); const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, 'rgba(255,240,180,0)'); gr.addColorStop(0.3, 'rgba(255,240,180,0.5)'); gr.addColorStop(1, 'rgba(255,240,180,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 256); const sx = g.createLinearGradient(0, 0, 64, 0); sx.addColorStop(0, 'rgba(0,0,0,1)'); sx.addColorStop(0.5, 'rgba(0,0,0,0)'); sx.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-out'; g.fillStyle = sx; g.fillRect(0, 0, 64, 256); return c; })());
  const rayMat = new THREE.MeshBasicMaterial({ map: lightTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
  const rays = new THREE.Group();
  for (let i = 0; i < 6; i++) {
    const r = new THREE.Mesh(new THREE.PlaneGeometry(4 + rand() * 3, 26), rayMat);
    r.position.set(-15 + i * 6, 30, -4 + rand() * 8); r.rotation.set(0, rand() * 3, 0.25);
    rays.add(r);
  }
  group.add(rays);

  const co2 = new MoleculeSwarm(group, 'co2', tier === 'low' ? 18 : 36, { scale: 1.5 });
  const o2 = new MoleculeSwarm(group, 'o2', tier === 'low' ? 18 : 36, { scale: 1.5 });
  const h2o = new MoleculeSwarm(group, 'h2o', tier === 'low' ? 12 : 24, { scale: 1.5 });
  const pickPal = () => palCells[(rand() * palCells.length) | 0];
  const pickSto = () => STOMATA[(rand() * STOMATA.length) | 0];
  const below = (st) => st.clone().add(new THREE.Vector3((rand() - 0.5) * 8, -9 - rand() * 4, (rand() - 0.5) * 6));
  const chamberPt = (st) => st.clone().add(new THREE.Vector3((rand() - 0.5) * 3, 3 + rand() * 2.5, (rand() - 0.5) * 3));
  const cellEdge = (c) => new THREE.Vector3(c.x + (rand() - 0.5) * c.r, Y.palisade[0] - 0.2, c.z + (rand() - 0.5) * c.r);
  let acc = { co2: 0, o2: 0, h2o: 0 };

  function update(dt, t, metrics, levels) {
    time.value = t;
    chl.glow.value = 0.2 + metrics.rate * 1.2;
    const ap = metrics.stomata;
    guards.forEach((gd) => {
      gd.cells[0].position.x = -(0.55 + ap * 0.45); gd.cells[1].position.x = 0.55 + ap * 0.45;
      gd.cells.forEach((c) => { c.scale.set(1, 1 + ap * 0.15, 1); });
      gd.pore.scale.set(0.12 + ap * 0.55, 1.1, 1);
    });
    const open = ap > 0.08;
    acc.co2 += dt * (1.2 + 4 * metrics.rate) * (open ? 1 : 0) * Math.min(1, levels.bicarb * 2 + 0.2);
    acc.o2 += dt * 5 * metrics.rate * (open ? 1 : 0.2);
    acc.h2o += dt * 3 * ap * levels.water;
    while (acc.co2 >= 1) { acc.co2 -= 1; const st = pickSto(); const c = pickPal(); co2.spawn([below(st), st.clone().add(new THREE.Vector3(0, -0.5, 0)), chamberPt(st), cellEdge(c), new THREE.Vector3(c.x, c.y - c.h * 0.5, c.z)], 3.2); }
    while (acc.o2 >= 1) { acc.o2 -= 1; const st = pickSto(); const c = pickPal(); o2.spawn([new THREE.Vector3(c.x, c.y - c.h * 0.3, c.z), cellEdge(c), chamberPt(st), st.clone(), below(st)], 3.4); }
    while (acc.h2o >= 1) { acc.h2o -= 1; const st = pickSto(); h2o.spawn([new THREE.Vector3(VEIN.x + (rand() - 0.5) * 2, VEIN.y + 3.8, (rand() - 0.5) * D * 0.8), chamberPt(st), st.clone(), below(st)], 3.6); }
    co2.update(dt, t); o2.update(dt, t); h2o.update(dt, t);
    rayMat.opacity = 0.15 + levels.lightK * 0.85;
    waterFlow.material.opacity = 0.2 + 0.5 * levels.water;
  }

  return {
    group, update,
    focus: new THREE.Vector3(0, 10, 0),
    hotspots: () => [
      { id: 'cuticle', pos: () => group.localToWorld(new THREE.Vector3(-8, Y.cuticle + 0.3, D / 2)), r: 1.6 },
      { id: 'upperEpidermis', pos: () => group.localToWorld(new THREE.Vector3(6, (Y.upEpi[0] + Y.upEpi[1]) / 2, D / 2)), r: 2.2 },
      { id: 'palisade', pos: () => group.localToWorld(new THREE.Vector3(-4, 15, D / 2)), r: 4.5 },
      { id: 'spongy', pos: () => group.localToWorld(new THREE.Vector3(-10, 7, D / 2)), r: 3.5 },
      { id: 'vein', pos: () => group.localToWorld(new THREE.Vector3(VEIN.x, VEIN.y, D / 2)), r: 4 },
      { id: 'stoma', pos: () => group.localToWorld(STOMATA[2].clone()), r: 3 },
      { id: 'stoma', pos: () => group.localToWorld(STOMATA[1].clone()), r: 3 },
    ],
    dispose() {},
  };
}
