import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

export default function init(stage, opts) {
  const engine = createEngine(stage, {});
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 6, 10);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 20,
    target: new THREE.Vector3(0, 0, 0),
  });
  controls.setTarget(new THREE.Vector3(0, 0, 0));

  basicLights(scene, { ambient: 0.55, key: 1.3 });
  scene.background = new THREE.Color(0x0b1c30);

  // Circuit board base
  const boardGeo = new THREE.BoxGeometry(10, 0.15, 6);
  const boardMat = new THREE.MeshStandardMaterial({ color: 0x0d3320, roughness: 0.8 });
  const board = new THREE.Mesh(boardGeo, boardMat);
  board.position.y = -0.3;
  scene.add(board);

  // Component materials
  const wireMat = new THREE.MeshStandardMaterial({ color: 0xc7d4ea, metalness: 0.6, roughness: 0.3 });
  const battMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, metalness: 0.4, roughness: 0.4 });
  const resistMat = new THREE.MeshStandardMaterial({ color: 0x9ec1ff, roughness: 0.7 });

  // Layout constants
  const LX = -4, RX = 4, TY = 2, BY = -2;
  const MX = 0; // midpoint X for parallel split

  // Wire segments (rebuilt per mode)
  const wireGroup = new THREE.Group();
  scene.add(wireGroup);

  // Electron particles system
  const MAX_DOTS = 80;
  const dotsGeo = new THREE.BufferGeometry();
  const dotsPos = new Float32Array(MAX_DOTS * 3);
  dotsGeo.setAttribute('position', new THREE.BufferAttribute(dotsPos, 3));
  dotsGeo.setDrawRange(0, 0);
  const dotsMat = new THREE.PointsMaterial({ color: 0x60a5fa, size: 0.15, sizeAttenuation: true });
  const dots = new THREE.Points(dotsGeo, dotsMat);
  scene.add(dots);

  // Component meshes
  const battGroup = new THREE.Group();
  scene.add(battGroup);
  // Battery cylinder
  const battBody = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 1.0, 16), battMat);
  battBody.rotation.z = Math.PI / 2;
  battGroup.add(battBody);
  const battPlus = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.08, 12), new THREE.MeshStandardMaterial({ color: 0xff4040 }));
  battPlus.rotation.z = Math.PI / 2;
  battPlus.position.x = 0.54;
  battGroup.add(battPlus);
  const battLabel = makeLabelSprite('12 V', { scale: 0.8, fontSize: 30 });
  battLabel.position.set(0, 0.5, 0);
  battGroup.add(battLabel);
  battGroup.position.set(LX, 0, 0);

  // Resistor mesh factory
  function makeResistor(label) {
    const grp = new THREE.Group();
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.65, 0.3), resistMat);
    grp.add(body);
    // Zigzag wire symbol (simple cylinders stacked)
    for (let i = 0; i < 5; i++) {
      const zz = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.12, 8), wireMat);
      zz.position.set((i % 2 === 0 ? 0.1 : -0.1), -0.25 + i * 0.12, 0);
      grp.add(zz);
    }
    const lbl = makeLabelSprite(label, { scale: 0.8, fontSize: 28 });
    lbl.position.set(0.5, 0, 0);
    grp.add(lbl);
    return grp;
  }

  const res1Group = makeResistor('R₁');
  scene.add(res1Group);
  const res2Group = makeResistor('R₂');
  scene.add(res2Group);
  res2Group.visible = false;

  // Bulb
  function makeBulb() {
    const grp = new THREE.Group();
    const glass = new THREE.Mesh(new THREE.SphereGeometry(0.25, seg, seg), new THREE.MeshStandardMaterial({ color: 0xfff2c8, transparent: true, opacity: 0.4, emissive: 0xffd060, emissiveIntensity: 0 }));
    grp.add(glass);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.15, 0.2, 12), new THREE.MeshStandardMaterial({ color: 0x8aa3c8, metalness: 0.6 }));
    base.position.y = -0.22;
    grp.add(base);
    grp._glass = glass;
    return grp;
  }
  const bulbGroup = makeBulb();
  bulbGroup.position.set(0, BY - 0.3, 0);
  scene.add(bulbGroup);

  // Ammeter
  const amMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.12, 16), new THREE.MeshStandardMaterial({ color: 0x16233a, metalness: 0.3 }));
  amMesh.rotation.x = Math.PI / 2;
  scene.add(amMesh);
  const amLabel = makeLabelSprite('A', { scale: 0.7, fontSize: 28 });
  scene.add(amLabel);

  // Path data for electrons
  let paths = [];

  function makeWire(p1, p2) {
    const dir = new THREE.Vector3().subVectors(p2, p1);
    const len = dir.length();
    if (len < 0.01) return null;
    const geo = new THREE.CylinderGeometry(0.04, 0.04, len, 8);
    const mesh = new THREE.Mesh(geo, wireMat);
    mesh.position.copy(p1).add(p2).multiplyScalar(0.5);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
    wireGroup.add(mesh);
    return mesh;
  }

  function buildLayout(mode, V, R1, R2) {
    wireGroup.clear();

    const tl = new THREE.Vector3(LX, TY, 0);
    const tr = new THREE.Vector3(RX, TY, 0);
    const bl = new THREE.Vector3(LX, BY, 0);
    const br = new THREE.Vector3(RX, BY, 0);
    const tm = new THREE.Vector3(MX, TY, 0);
    const bm = new THREE.Vector3(MX, BY, 0);

    paths = [];

    if (mode === 'parallel') {
      makeWire(tl, tm); makeWire(tm, tr);
      makeWire(bl, bm); makeWire(bm, br);
      makeWire(tl, bl);
      makeWire(tr, br);
      makeWire(tm, bm);
      // R1 on left branch, R2 on right
      res1Group.position.set(MX - 2, 0, 0);
      res2Group.position.set(RX, 0, 0);
      res2Group.visible = true;
      // Paths
      const pathPts1 = [tl, tm, new THREE.Vector3(MX - 2, TY, 0), new THREE.Vector3(MX - 2, BY, 0), bm, bl, tl];
      const pathPts2 = [tl, tm, tr, br, bm, bl, tl];
      paths.push({ pts: toSegments(pathPts1), dots: initDots(pathPts1) });
      paths.push({ pts: toSegments(pathPts2), dots: initDots(pathPts2) });
    } else {
      makeWire(tl, tr);
      makeWire(br, bl);
      makeWire(tl, bl);
      makeWire(tr, br);
      res1Group.position.set(RX, mode === 'series' ? TY * 0.6 : 0, 0);
      res2Group.position.set(RX, mode === 'series' ? BY * 0.6 : 0, 0);
      res2Group.visible = mode === 'series';
      const pathPts = [tl, tr, br, bl, tl];
      paths.push({ pts: toSegments(pathPts), dots: initDots(pathPts) });
    }

    battGroup.position.set(LX, 0, 0);
    amMesh.position.set(LX + (RX - LX) * 0.35, TY, 0);
    amLabel.position.set(LX + (RX - LX) * 0.35, TY + 0.35, 0);
    bulbGroup.position.set(MX, BY - 0.4, 0);
  }

  function toSegments(pts) {
    const segs = [];
    let len = 0;
    for (let i = 0; i < pts.length - 1; i++) {
      const d = pts[i].distanceTo(pts[i + 1]);
      segs.push({ a: pts[i].clone(), b: pts[i + 1].clone(), start: len, len: d });
      len += d;
    }
    return { segs, total: len };
  }

  function initDots(pts) {
    const seg = toSegments(pts);
    const n = Math.max(5, Math.floor(seg.total / 0.9));
    const d = [];
    for (let i = 0; i < n && i < MAX_DOTS; i++) d.push((i / n) * seg.total);
    return d;
  }

  function posOnPath(path, s) {
    s = ((s % path.segs.total) + path.segs.total) % path.segs.total;
    for (const seg of path.segs.segs) {
      if (s <= seg.start + seg.len) {
        const t = (s - seg.start) / seg.len;
        return seg.a.clone().lerp(seg.b, t);
      }
    }
    return path.segs.segs[0].a.clone();
  }

  // Solve circuit
  function solve(V, R1, R2, mode) {
    let rTot, i1, i2, vr1, vr2;
    if (mode === 'single') {
      rTot = R1; i1 = V / R1; i2 = 0; vr1 = V; vr2 = 0;
    } else if (mode === 'series') {
      rTot = R1 + R2; i1 = V / rTot; i2 = i1; vr1 = i1 * R1; vr2 = i2 * R2;
    } else {
      rTot = (R1 * R2) / (R1 + R2);
      vr1 = V; vr2 = V; i1 = V / R1; i2 = V / R2;
    }
    return { rTot, iTot: V / rTot, i1, i2, vr1, vr2 };
  }

  // State
  let V = 12, R1 = 6, R2 = 6, mode = 'single';
  buildLayout(mode, V, R1, R2);

  function updateBattLabel(vv) {
    const ns = makeLabelSprite(`${vv.toFixed(1)} V`, { scale: 0.8, fontSize: 30 });
    battLabel.material.map.dispose();
    battLabel.material = ns.material;
    battLabel.scale.copy(ns.scale);
    scene.remove(ns);
  }

  // Panel
  const panel = createPanel(stage, { title: 'Circuit 3D' });
  panel.slider({
    label: 'Battery voltage', min: 0, max: 24, step: 0.5, value: V,
    format: (v) => `${v.toFixed(1)} V`,
    onChange: (v) => { V = v; updateBattLabel(v); },
  });
  panel.slider({
    label: 'Resistance R₁', min: 1, max: 20, step: 0.5, value: R1,
    format: (v) => `${v.toFixed(1)} Ω`, onChange: (v) => { R1 = v; },
  });
  panel.select({
    label: 'Circuit layout',
    options: [
      { value: 'single', label: 'R₁ only' },
      { value: 'series', label: 'Series R₁ + R₂' },
      { value: 'parallel', label: 'Parallel R₁ ∥ R₂' },
    ],
    value: mode,
    onChange: (v) => { mode = v; r2Slider.el.style.display = v === 'single' ? 'none' : ''; buildLayout(mode, V, R1, R2); },
  });
  const r2Slider = panel.slider({
    label: 'Resistance R₂', min: 1, max: 20, step: 0.5, value: R2,
    format: (v) => `${v.toFixed(1)} Ω`, onChange: (v) => { R2 = v; },
  });
  r2Slider.el.style.display = 'none';
  panel.divider();
  const rTotOut = panel.readout({ label: 'Total resistance', value: '—' });
  const iTotOut = panel.readout({ label: 'Current (total)', value: '—' });
  const v1Out = panel.readout({ label: 'V across R₁', value: '—' });
  const v2Out = panel.readout({ label: 'V across R₂', value: '—' });
  panel.info('Blue dots are electrons — they flow along the wires. The bulb glows with power P = VI. Orbit to see the 3D layout.');

  const hud = createHud(stage);
  const currentBadge = hud.badge('I = 0 A', '#F59E0B');

  // Resistor label updaters
  function updateResLabel(grp, label, vDrop, iThru) {
    const txt = `${label}\n${vDrop.toFixed(1)} V  ${iThru.toFixed(2)} A`;
    // find the sprite in grp
    grp.traverse((c) => {
      if (c.isSprite) {
        const ns = makeLabelSprite(`${label}  ${vDrop.toFixed(1)}V`, { scale: 0.8, fontSize: 28 });
        c.material.map.dispose();
        c.material = ns.material;
        c.scale.copy(ns.scale);
        scene.remove(ns);
      }
    });
  }

  let dotOffset = 0;
  let totalDots = 0;

  engine.setUpdate((dt) => {
    controls.update(dt);

    const sol = solve(V, R1, R2, mode);
    const speed = Math.min(4, 0.6 * Math.sqrt(Math.max(0, sol.iTot)));
    dotOffset += speed * dt;

    // Move electron dots along paths
    let dotCount = 0;
    for (let pi = 0; pi < paths.length; pi++) {
      const path = paths[pi];
      const pathI = pi === 0 ? sol.i1 : sol.i2;
      const pathSpeed = Math.min(4, 0.6 * Math.sqrt(Math.max(0, pathI)));
      for (let di = 0; di < path.dots.length && dotCount < MAX_DOTS; di++) {
        path.dots[di] = (path.dots[di] + pathSpeed * dt) % path.segs.total;
        const p = posOnPath(path, path.dots[di]);
        dotsPos[dotCount * 3] = p.x;
        dotsPos[dotCount * 3 + 1] = p.y;
        dotsPos[dotCount * 3 + 2] = p.z;
        dotCount++;
      }
    }
    dotsGeo.setDrawRange(0, dotCount);
    dotsGeo.attributes.position.needsUpdate = true;

    // Bulb brightness
    const brightness = Math.min(1, sol.iTot / 4);
    bulbGroup._glass.material.emissiveIntensity = brightness * 1.5;
    bulbGroup._glass.material.opacity = 0.2 + brightness * 0.5;

    // Update readouts
    currentBadge.set(`I = ${sol.iTot.toFixed(2)} A`);
    rTotOut.set(`${sol.rTot.toFixed(2)} Ω`);
    iTotOut.set(`${sol.iTot.toFixed(2)} A`);
    v1Out.set(`${sol.vr1.toFixed(1)} V · ${sol.i1.toFixed(2)} A`);
    v2Out.set(mode === 'single' ? '—' : `${sol.vr2.toFixed(1)} V · ${sol.i2.toFixed(2)} A`);
  });

  engine.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
