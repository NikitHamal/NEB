import { THREE, getSoftDotTexture } from '../../core/engine.js';
import { rng, patchMaterial } from '../butterfly/kit.js';
import { MoleculeSwarm } from './molecules.js';

const RX = 16; const RY = 6.2; const RZ = 9;
const CALVIN = { c: new THREE.Vector3(7.5, -1.2, 2.2), r: 3.2 };

function rim(material, color, power, key, extra = {}) {
  return patchMaterial(material, {
    ...extra,
    fragDecl: 'uniform vec3 uRim;\n',
    uniforms: { uRim: { value: new THREE.Color(color) }, ...(extra.uniforms || {}) },
    fragEnd: `float rimK = pow(1.0 - abs(dot(normalize(normal), normalize(vViewPosition))), ${power.toFixed(1)}); gl_FragColor.rgb += uRim * rimK * 0.45;`,
    key,
  });
}

function discGeometry(seg) {
  const pts = [];
  const R = 1.7; const h = 0.17; const b = 0.12;
  pts.push(new THREE.Vector2(0.001, -h));
  for (let i = 0; i <= 6; i++) { const a = -Math.PI / 2 + (i / 6) * Math.PI; pts.push(new THREE.Vector2(R - b + Math.cos(a) * b, Math.sin(a) * h)); }
  pts.push(new THREE.Vector2(0.001, h));
  return new THREE.LatheGeometry(pts, seg);
}

export function buildChloroplast({ tier }) {
  const rand = rng(12);
  const group = new THREE.Group();
  const rich = tier !== 'low';
  const seg = tier === 'low' ? 20 : 40;

  const outer = new THREE.SphereGeometry(1, seg + 8, seg, Math.PI / 2 + 0.75, Math.PI * 2 - 1.5, 0, Math.PI);
  outer.scale(RX, RY, RZ);
  const memMat = new THREE.MeshPhysicalMaterial({ color: 0x7fc56a, roughness: 0.3, transparent: true, opacity: 0.42, side: THREE.DoubleSide, depthWrite: true, clearcoat: rich ? 1 : 0 });
  rim(memMat, 0xa8f08a, 2.0, 'membrane');
  const outerMesh = new THREE.Mesh(outer, memMat);
  outerMesh.renderOrder = 4;
  const innerGeo = new THREE.SphereGeometry(1, seg + 8, seg, Math.PI / 2 + 0.62, Math.PI * 2 - 1.24, 0, Math.PI);
  innerGeo.scale(RX - 0.7, RY - 0.55, RZ - 0.7);
  const innerMesh = new THREE.Mesh(innerGeo, memMat.clone());
  rim(innerMesh.material, 0x8fe07a, 2.2, 'membrane2');
  innerMesh.renderOrder = 4;
  group.add(outerMesh, innerMesh);
  const stromaMat = new THREE.MeshBasicMaterial({ color: 0x6fae62, transparent: true, opacity: 0.22, side: THREE.BackSide, depthWrite: true });
  const stroma = new THREE.Mesh(new THREE.SphereGeometry(1, seg, seg / 2), stromaMat);
  stroma.scale.set(RX - 0.9, RY - 0.8, RZ - 0.9);
  stroma.renderOrder = 1;
  group.add(stroma);

  const backMat = new THREE.MeshStandardMaterial({ color: 0x2f6a36, roughness: 0.8, transparent: true, opacity: 0.55, depthWrite: false });
  [[-38, 8, -60, 14], [34, -10, -70, 16], [6, 20, -95, 18], [-20, -18, -85, 13], [52, 16, -110, 20]].forEach(([x, y, z, r]) => {
    const b = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 14), backMat);
    b.scale.set(r, r * 0.42, r * 0.6); b.position.set(x, y, z); b.rotation.z = (x % 3) * 0.2;
    group.add(b);
  });

  const stacks = [];
  const nStacks = tier === 'low' ? 8 : 12;
  let tries = 0;
  while (stacks.length < nStacks && tries < 3000) {
    tries++;
    const x = (rand() * 2 - 1) * (RX - 3.5); const z = (rand() * 2 - 1) * (RZ - 3);
    if ((x / (RX - 2.5)) ** 2 + (z / (RZ - 2.2)) ** 2 > 1) continue;
    if (Math.hypot(x - CALVIN.c.x, z - CALVIN.c.z) < CALVIN.r + 1.6) continue;
    if (stacks.some((s) => Math.hypot(s.x - x, s.z - z) < 4.0)) continue;
    const maxH = RY * Math.sqrt(Math.max(0.05, 1 - (x / RX) ** 2 - (z / RZ) ** 2)) * 1.4;
    const n = Math.max(4, Math.min(11, Math.floor(maxH / 0.5)));
    stacks.push({ x, z, n, y0: -(n * 0.46) / 2 + (rand() - 0.5) * 0.8, tilt: (rand() - 0.5) * 0.2 });
  }
  const discs = [];
  stacks.forEach((s) => { for (let i = 0; i < s.n; i++) discs.push({ x: s.x, y: s.y0 + i * 0.46, z: s.z, s: 0.92 + rand() * 0.16, tilt: s.tilt }); });
  const thyMat = new THREE.MeshPhysicalMaterial({ color: 0x2f8f2a, roughness: 0.32, clearcoat: rich ? 0.7 : 0, clearcoatRoughness: 0.25, emissive: 0x0d3a0a, emissiveIntensity: 0.6 });
  rim(thyMat, 0x7dff6a, 2.4, 'thylakoid');
  const discMesh = new THREE.InstancedMesh(discGeometry(tier === 'low' ? 16 : 28), thyMat, discs.length);
  const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const e = new THREE.Euler(); const s = new THREE.Vector3(); const p = new THREE.Vector3();
  discs.forEach((d, i) => { m4.compose(p.set(d.x, d.y, d.z), q.setFromEuler(e.set(d.tilt, 0, d.tilt * 0.5)), s.set(d.s, 1, d.s)); discMesh.setMatrixAt(i, m4); });
  group.add(discMesh);

  const lamMat = new THREE.MeshPhysicalMaterial({ color: 0x3f9c36, roughness: 0.4, side: THREE.DoubleSide, transparent: true, opacity: 0.85 });
  const links = [];
  stacks.forEach((a, i) => {
    const near = stacks.map((b, j) => ({ b, j, d: Math.hypot(a.x - b.x, a.z - b.z) })).filter((o) => o.j > i).sort((u, v) => u.d - v.d).slice(0, 2);
    near.forEach(({ b, d }) => { if (d < 9) for (let k = 0; k < 2; k++) links.push({ a, b, d, y: (rand() - 0.5) * 1.6 }); });
  });
  const lam = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.1, 0.9), lamMat, Math.max(1, links.length));
  links.forEach((l, i) => {
    const mid = p.set((l.a.x + l.b.x) / 2, l.y, (l.a.z + l.b.z) / 2);
    q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), -Math.atan2(l.b.z - l.a.z, l.b.x - l.a.x));
    m4.compose(mid, q, s.set(l.d, 1, 1)); lam.setMatrixAt(i, m4);
  });
  lam.count = links.length;
  group.add(lam);

  const starchMat = new THREE.MeshPhysicalMaterial({ color: 0xf3ecd8, roughness: 0.6, sheen: 0.5, sheenColor: new THREE.Color(0xffffff) });
  [[-9, -2.2, -3, 2.2], [-3, 2.6, 4.5, 1.5]].forEach(([x, y, z, r]) => { const st = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), starchMat); st.scale.set(1.4, 0.8, 1); st.position.set(x, y, z); group.add(st); });
  const globMat = new THREE.MeshPhysicalMaterial({ color: 0xe8c547, roughness: 0.25, clearcoat: 1 });
  const globs = new THREE.InstancedMesh(new THREE.SphereGeometry(0.35, 10, 8), globMat, 14);
  for (let i = 0; i < 14; i++) { m4.compose(p.set((rand() * 2 - 1) * (RX - 3), (rand() * 2 - 1) * (RY - 2.5), (rand() * 2 - 1) * (RZ - 3)), q.identity(), s.setScalar(0.6 + rand() * 0.8)); globs.setMatrixAt(i, m4); }
  group.add(globs);
  const ribN = tier === 'low' ? 120 : 320;
  const ribPos = new Float32Array(ribN * 3);
  for (let i = 0; i < ribN; i++) {
    let x; let y; let z;
    do { x = rand() * 2 - 1; y = rand() * 2 - 1; z = rand() * 2 - 1; } while (x * x + y * y + z * z > 1);
    ribPos[i * 3] = x * (RX - 1.2); ribPos[i * 3 + 1] = y * (RY - 1.2); ribPos[i * 3 + 2] = z * (RZ - 1.2);
  }
  const ribGeo = new THREE.BufferGeometry(); ribGeo.setAttribute('position', new THREE.BufferAttribute(ribPos, 3));
  const ribs = new THREE.Points(ribGeo, new THREE.PointsMaterial({ color: 0x3a5a2a, size: 0.22, sizeAttenuation: true, map: getSoftDotTexture(), transparent: true, depthWrite: false }));
  ribs.material.userData.sharedFx = true;
  group.add(ribs);

  const track = new THREE.Mesh(new THREE.TorusGeometry(CALVIN.r, 0.12, 8, 64), new THREE.MeshBasicMaterial({ color: 0xffd36a, transparent: true, opacity: 0.35, depthWrite: false }));
  track.position.copy(CALVIN.c); track.rotation.x = Math.PI / 2 - 0.35;
  group.add(track);
  const cycN = 10;
  const cycMesh = new THREE.InstancedMesh(new THREE.SphereGeometry(0.42, 14, 10), new THREE.MeshPhysicalMaterial({ color: 0xffc34d, emissive: 0x6b3a00, emissiveIntensity: 0.8, roughness: 0.3, clearcoat: 1 }), cycN);
  group.add(cycMesh);
  let cycPhase = 0;

  const photonN = tier === 'low' ? 20 : 40;
  const photons = [];
  const photonGeo = new THREE.CylinderGeometry(0.06, 0.06, 2.6, 6); photonGeo.translate(0, 1.3, 0);
  const photonMesh = new THREE.InstancedMesh(photonGeo, new THREE.MeshBasicMaterial({ color: 0xffe58a, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }), photonN);
  photonMesh.count = 0; photonMesh.frustumCulled = false;
  group.add(photonMesh);
  const flashN = 24; const flashes = [];
  const flashPos = new Float32Array(flashN * 3); const flashGeo = new THREE.BufferGeometry();
  flashGeo.setAttribute('position', new THREE.BufferAttribute(flashPos, 3)); flashGeo.setDrawRange(0, 0);
  const flashPts = new THREE.Points(flashGeo, new THREE.PointsMaterial({ color: 0xc9ff7a, size: 2.4, map: getSoftDotTexture(), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }));
  flashPts.material.userData.sharedFx = true; flashPts.frustumCulled = false;
  group.add(flashPts);

  const mol = {
    h2o: new MoleculeSwarm(group, 'h2o', tier === 'low' ? 14 : 26, { scale: 0.9 }),
    o2: new MoleculeSwarm(group, 'o2', tier === 'low' ? 14 : 26, { scale: 0.9 }),
    co2: new MoleculeSwarm(group, 'co2', tier === 'low' ? 14 : 26, { scale: 0.9 }),
    atp: new MoleculeSwarm(group, 'atp', tier === 'low' ? 12 : 24, { scale: 0.7, glow: 0.4 }),
    glu: new MoleculeSwarm(group, 'glucose', 8, { scale: 1.0 }),
  };
  const outside = (dir) => dir.clone().normalize().multiply(new THREE.Vector3(RX + 9, RY + 9, RZ + 9));
  const randDir = () => new THREE.Vector3(rand() * 2 - 1, rand() * 1.2 - 0.3, rand() * 2 - 1);
  const stackTop = (st) => new THREE.Vector3(st.x, st.y0 + st.n * 0.46 + 0.2, st.z);
  const stackSide = (st) => new THREE.Vector3(st.x + 1.8, st.y0 + st.n * 0.23, st.z + (rand() - 0.5));
  const ringPt = (a) => new THREE.Vector3(Math.cos(a) * CALVIN.r, 0, Math.sin(a) * CALVIN.r).applyEuler(track.rotation).add(CALVIN.c);
  const acc = { ph: 0, h2o: 0, co2: 0 };
  const counters = { co2: 0, glucose: 0, o2: 0 };

  function update(dt, t, metrics, levels) {
    const r = metrics.rate;
    thyMat.emissiveIntensity = 0.3 + levels.lightK * 0.9;
    acc.ph += dt * levels.lightK * 16;
    while (acc.ph >= 1 && photons.length < photonN) {
      acc.ph -= 1;
      const st = stacks[(rand() * stacks.length) | 0];
      const end = stackTop(st);
      const dir = new THREE.Vector3(-0.35 + rand() * 0.2, -1, -0.15 + rand() * 0.3).normalize();
      photons.push({ end, dir, d: 22 + rand() * 6 });
    }
    if (acc.ph >= 1) acc.ph = 0;
    let n = 0;
    for (let i = photons.length - 1; i >= 0; i--) {
      const ph = photons[i];
      ph.d -= dt * 34;
      if (ph.d <= 0) {
        if (flashes.length < flashN) flashes.push({ p: ph.end.clone(), life: 1 });
        photons.splice(i, 1);
        if (rand() < r * 1.2) {
          const st = stacks[(rand() * stacks.length) | 0];
          mol.atp.spawn([stackSide(st), CALVIN.c.clone().add(new THREE.Vector3((rand() - 0.5) * 2, 0.6, (rand() - 0.5) * 2))], 5, { jitter: 0.15 });
        }
      }
    }
    photons.forEach((ph) => {
      p.copy(ph.end).addScaledVector(ph.dir, -ph.d);
      q.setFromUnitVectors(new THREE.Vector3(0, 1, 0), ph.dir.clone().negate());
      m4.compose(p, q, s.set(1, 1, 1));
      photonMesh.setMatrixAt(n++, m4);
    });
    photonMesh.count = n; photonMesh.instanceMatrix.needsUpdate = true;
    let fn = 0;
    for (let i = flashes.length - 1; i >= 0; i--) { flashes[i].life -= dt * 2.5; if (flashes[i].life <= 0) flashes.splice(i, 1); }
    flashes.forEach((f) => { flashPos[fn * 3] = f.p.x; flashPos[fn * 3 + 1] = f.p.y; flashPos[fn * 3 + 2] = f.p.z; fn++; });
    flashGeo.setDrawRange(0, fn); flashGeo.attributes.position.needsUpdate = true;

    acc.h2o += dt * r * 3.2;
    while (acc.h2o >= 1) {
      acc.h2o -= 1;
      const st = stacks[(rand() * stacks.length) | 0];
      const side = stackSide(st);
      mol.h2o.spawn([outside(randDir().setY(-1.2)), side], 6, {
        jitter: 0.2,
        onEnd: () => { counters.o2 += 0.5; if (counters.o2 % 1 === 0) mol.o2.spawn([side.clone(), side.clone().add(new THREE.Vector3(0, 2, 0)), outside(randDir().setY(1.2))], 5.5, { jitter: 0.2 }); },
      });
    }
    acc.co2 += dt * r * 3.0;
    while (acc.co2 >= 1) {
      acc.co2 -= 1;
      const a = rand() * Math.PI * 2;
      mol.co2.spawn([outside(new THREE.Vector3(1, rand() - 0.2, rand() * 2 - 1)), ringPt(a)], 6, {
        jitter: 0.2,
        onEnd: () => {
          counters.co2 += 1;
          if (counters.co2 % 6 === 0) { counters.glucose += 1; const o = ringPt(rand() * 6.28); mol.glu.spawn([o, o.clone().add(new THREE.Vector3(2, 3, 1)), outside(new THREE.Vector3(1, 0.6, 0.6))], 3.6, { jitter: 0.1 }); }
        },
      });
    }
    cycPhase += dt * (0.25 + r * 1.6);
    for (let i = 0; i < cycN; i++) {
      m4.compose(ringPt(cycPhase + (i / cycN) * Math.PI * 2), q.identity(), s.setScalar(0.8 + 0.25 * Math.sin(t * 4 + i)));
      cycMesh.setMatrixAt(i, m4);
    }
    cycMesh.instanceMatrix.needsUpdate = true;
    Object.values(mol).forEach((m) => m.update(dt, t));
    group.rotation.y = Math.sin(t * 0.05) * 0.04;
  }

  return {
    group, update, counters,
    focus: new THREE.Vector3(0, 0, 0),
    hotspots: () => [
      { id: 'envelope', pos: () => group.localToWorld(new THREE.Vector3(0, RY - 0.4, -2)), r: 3 },
      { id: 'granum', pos: () => group.localToWorld(new THREE.Vector3(stacks[0].x, 0, stacks[0].z)), r: 3 },
      { id: 'granum', pos: () => group.localToWorld(new THREE.Vector3(stacks[1].x, 0, stacks[1].z)), r: 3 },
      { id: 'calvin', pos: () => group.localToWorld(CALVIN.c.clone()), r: 4 },
      { id: 'starch', pos: () => group.localToWorld(new THREE.Vector3(-9, -2.2, -3)), r: 3 },
    ],
    dispose() {},
  };
}
