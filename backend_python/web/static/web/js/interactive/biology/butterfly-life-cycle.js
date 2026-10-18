import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { makeScanMaterial } from '../core/bio3d-scan-grade.js';
import { batchStaticGeometry } from '../core/bio3d-batch.js';
import { Particles, skyDome, applyEnvironmentLighting, glowTexture } from '../core/bio-fx.js';

const STAGES = [
  {
    id: 'egg', name: 'Egg', color: '#fde68a', duration: '3-5 days', dayRange: 'day 0-4', key: 'embryo develops inside chorion',
    info: 'The journey begins as a tiny egg, no bigger than a pinhead, glued to the underside of a leaf by the mother butterfly. She chooses the leaf carefully — it must be a plant her caterpillars can eat. Inside, a tiny embryo grows.',
  },
  {
    id: 'caterpillar', name: 'Caterpillar', color: '#86efac', duration: '10-14 days', dayRange: 'day 4-18', key: 'larva feeds, moults through instars',
    info: 'Out hatches the larva — a caterpillar whose only job is to eat. It can grow to 100 times its birth weight in two weeks, shedding its skin several times as it outgrows it, storing energy for the transformation ahead.',
  },
  {
    id: 'chrysalis', name: 'Chrysalis', color: '#c4b5fd', duration: '7-14 days', dayRange: 'day 18-30', key: 'pupa remodels tissues into adult organs',
    info: 'The caterpillar anchors to a twig and becomes a pupa. It looks still, but inside, enzymes break the body into a nutrient soup and special cells rebuild the wings, legs and eyes of the adult. A total rebuild.',
  },
  {
    id: 'butterfly', name: 'Adult Butterfly', color: '#f9a8d4', duration: '2-6 weeks', dayRange: 'adult phase', key: 'wings expand; feeding and reproduction',
    info: 'The adult emerges, pumps haemolymph into its crumpled wings, and flies off to find a mate and lay the next generation of eggs. It no longer eats leaves — it sips liquid nectar through a long tube called a proboscis.',
  },
];

// The plain tiger, Danaus chrysippus, common across Nepal's hills and Terai: tawny orange wings
// with dark veins, a black forewing tip crossed by a white band, and black margins dotted with
// white. Painted in wing space: u runs from the body (0) to the wing edge (1), v bottom to top.
function wingTexture(kind) {
  const size = 512;
  const c = document.createElement('canvas');
  c.width = size; c.height = size;
  const g = c.getContext('2d');
  const base = g.createLinearGradient(0, 0, size, 0);
  base.addColorStop(0, '#b7561d'); base.addColorStop(0.35, '#e98a2c'); base.addColorStop(1, '#f2a13f');
  g.fillStyle = base; g.fillRect(0, 0, size, size);
  // dark scaling near the body
  const root = g.createLinearGradient(0, 0, size * 0.25, 0); root.addColorStop(0, 'rgba(60,24,10,0.55)'); root.addColorStop(1, 'rgba(60,24,10,0)');
  g.fillStyle = root; g.fillRect(0, 0, size * 0.25, size);
  if (kind === 'upper') {
    // the black apex with its white diagonal band
    g.fillStyle = '#17110f';
    g.beginPath(); g.moveTo(size * 0.5, 0); g.lineTo(size, 0); g.lineTo(size, size * 0.72); g.quadraticCurveTo(size * 0.78, size * 0.5, size * 0.5, 0); g.fill(); // canvas y runs down: v = 1 is the top
    g.fillStyle = '#fbf7ef';
    [[0.68, 0.86, 22], [0.75, 0.78, 20], [0.82, 0.7, 18], [0.88, 0.62, 15], [0.72, 0.93, 14]].forEach(([x, y, r]) => { g.beginPath(); g.ellipse(x * size, size - y * size, r, r * 0.7, -0.6, 0, Math.PI * 2); g.fill(); });
  } else {
    // three small black spots on the hindwing
    g.fillStyle = '#17110f';
    [[0.42, 0.62, 9], [0.5, 0.5, 8], [0.56, 0.68, 7]].forEach(([x, y, r]) => { g.beginPath(); g.arc(x * size, size - y * size, r, 0, Math.PI * 2); g.fill(); });
  }
  // veins radiate from the body
  g.strokeStyle = 'rgba(28,16,10,0.85)'; g.lineWidth = 3.2;
  for (let i = 0; i < 8; i++) {
    const t = i / 7;
    g.beginPath(); g.moveTo(0, size * (0.5 + (kind === 'upper' ? -0.1 : 0.1)));
    g.quadraticCurveTo(size * 0.45, size * (0.2 + t * 0.6), size, size * (t * 1.05 - 0.02));
    g.stroke();
  }
  // the black margin with its row of white dots, along the outer edge
  g.lineWidth = 34; g.strokeStyle = '#17110f';
  g.beginPath(); g.moveTo(size * 0.98, 0); g.lineTo(size * 0.98, size); g.stroke();
  g.lineWidth = 22; g.beginPath(); g.moveTo(0, kind === 'upper' ? size * 0.99 : size * 0.01); g.lineTo(size, kind === 'upper' ? size * 0.99 : size * 0.01); g.stroke();
  g.fillStyle = '#fbf7ef';
  for (let i = 0; i < 12; i++) { g.beginPath(); g.arc(size * 0.975, size * (0.05 + i * 0.08), 4.5, 0, Math.PI * 2); g.fill(); }
  const tex = new THREE.CanvasTexture(c);
  if (THREE.SRGBColorSpace) tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  return tex;
}

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-butterfly-stage');
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  const low = quality.tier === 'low';

  camera.position.set(1.5, 4.2, 7.5);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4, maxDistance: 18, enablePan: false, maxPolar: Math.PI * 0.7, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 1, 0));

  const disposeEnv = applyEnvironmentLighting(renderer, scene, { sky: '#9fc7ef', horizon: '#5f8f6a', ground: '#131c12' });
  skyDome(scene, { top: 0x5d8fc4, mid: 0x6f9a74, bottom: 0x1f3320 });
  scene.fog = new THREE.Fog(0x5c7f62, 18, 44);
  basicLights(scene, { ambient: 0.6, key: 2.0 });
  const fill = new THREE.DirectionalLight(0xffd9a8, 0.4); fill.position.set(-5, 3, -5); scene.add(fill);

  // Ground + branch
  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(8, 44),
    new THREE.MeshStandardMaterial({ color: 0x1c3320, roughness: 1 })
  );
  ground.rotation.x = -Math.PI / 2; ground.position.y = -2.2; ground.receiveShadow = true; scene.add(ground);

  const branchCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-2.4, -1.15, -0.3), new THREE.Vector3(-0.8, -0.75, 0.1),
    new THREE.Vector3(0.6, -0.55, 0), new THREE.Vector3(2.2, -0.35, -0.25),
  ]);
  const branch = new THREE.Mesh(
    new THREE.TubeGeometry(branchCurve, 28, 0.09, 9, false),
    makeScanMaterial('branch-bark-pbr', 0x5d4037, { family: 'chitin', roughness: 0.9, textureSize: low ? 128 : 256 })
  );
  branch.castShadow = true;
  scene.add(branch);

  const leafMat = makeScanMaterial('branch-leaf-pbr', 0x4caf50, { family: 'leaf', side: THREE.DoubleSide, roughness: 0.58, textureSize: 128 });
  const leafGeo = new THREE.CircleGeometry(0.72, 22);
  leafGeo.scale(1, 0.52, 1);
  const leafMesh = new THREE.Mesh(leafGeo, leafMat);
  leafMesh.position.set(1.35, -0.28, 0.05);
  leafMesh.rotation.set(-0.5, 0, 0.4);
  leafMesh.castShadow = true;
  scene.add(leafMesh);

  const root = new THREE.Group(); scene.add(root);
  const builders = {};

  // EGG cluster
  builders.egg = new THREE.Group();
  const eggMat = makeScanMaterial('egg-chorion-pbr', 0xfde68a, { family: 'bone', roughness: 0.35, textureSize: 128 });
  for (let i = 0; i < 9; i++) {
    const g = new THREE.SphereGeometry(0.13, 14, 12); g.scale(0.8, 1.1, 0.8);
    const m = new THREE.Mesh(g, eggMat);
    const a = (i / 9) * Math.PI * 2;
    m.position.set(1.35 + Math.cos(a) * 0.17, -0.26, Math.sin(a) * 0.17);
    m.castShadow = true; builders.egg.add(m);
  }

  // CATERPILLAR
  builders.caterpillar = new THREE.Group();
  const catGroup = new THREE.Group();
  catGroup.position.set(1.1, -0.14, 0);
  const segMat = makeScanMaterial('cat-segment-pbr', 0x66bb6a, { family: 'leaf', roughness: 0.55, textureSize: 128 });
  const stripeMat = makeScanMaterial('cat-stripe-pbr', 0x2e7d32, { family: 'leaf', roughness: 0.55, textureSize: 128 });
  for (let i = 0; i < 8; i++) {
    const r = 0.22 + Math.sin(i * 0.5) * 0.03;
    const m = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 14), i % 2 === 0 ? segMat : stripeMat);
    m.position.set(0.4 + i * 0.32, 0.42, 0); m.castShadow = true; catGroup.add(m);
  }
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.26, 16, 14), segMat);
  head.position.set(0.05, 0.42, 0); head.castShadow = true; catGroup.add(head);
  const eyeMat = new THREE.MeshStandardMaterial({ color: 0x111111 });
  [-0.08, 0.08].forEach((dz) => {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), eyeMat);
    eye.position.set(-0.05, 0.47, dz); catGroup.add(eye);
  });
  const legMat = new THREE.MeshStandardMaterial({ color: 0x1b4332, roughness: 0.75 });
  for (let i = 1; i < 8; i++) {
    [-1, 1].forEach((side) => {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.010, 0.22, 6), legMat);
      leg.position.set(0.18 + i * 0.32, 0.23, side * 0.10);
      leg.rotation.x = side * 0.65; leg.rotation.z = i < 4 ? -0.25 : 0.18;
      catGroup.add(leg);
    });
  }
  [-0.08, 0.08].forEach((dz) => {
    const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.3, 6), legMat);
    ant.position.set(-0.12, 0.65, dz); ant.rotation.z = 0.5; catGroup.add(ant);
  });
  builders.caterpillar.add(catGroup);

  // CHRYSALIS
  builders.chrysalis = new THREE.Group();
  const chryGeo = new THREE.SphereGeometry(0.5, 24, 20); chryGeo.scale(0.55, 1.5, 0.55);
  const chryMat = makeScanMaterial('chrysalis-pbr', 0xc4b5fd, {
    family: 'chitin', roughness: 0.3, metalness: 0.2, transparent: true, opacity: 0.88,
    emissive: 0x7c3aed, emissiveIntensity: 0.08, textureSize: 128,
  });
  const chry = new THREE.Mesh(chryGeo, chryMat);
  chry.position.set(0.1, 0.05, 0); chry.castShadow = true; builders.chrysalis.add(chry);
  const band = new THREE.Mesh(
    new THREE.TorusGeometry(0.22, 0.03, 8, 24),
    new THREE.MeshStandardMaterial({ color: 0xffd54a, metalness: 0.75, roughness: 0.2 })
  );
  band.position.set(0.1, 0.40, 0); band.rotation.x = Math.PI / 2; builders.chrysalis.add(band);
  const silk = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.5, 6), new THREE.MeshStandardMaterial({ color: 0xeeeeee }));
  silk.position.set(0.1, 0.70, 0); builders.chrysalis.add(silk);

  // BUTTERFLY with textured wings on hinge pivots
  builders.butterfly = new THREE.Group();
  const bfGroup = new THREE.Group();
  bfGroup.position.set(0.1, 0.75, 0);
  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.55 });
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.1, 12), bodyMat);
  body.rotation.z = Math.PI / 2; bfGroup.add(body);
  const headB = new THREE.Mesh(new THREE.SphereGeometry(0.09, 12, 10), bodyMat);
  headB.position.x = 0.60; bfGroup.add(headB);

  const upperTex = wingTexture('upper');
  const lowerTex = wingTexture('lower');
  const wingMatUpper = new THREE.MeshPhysicalMaterial({ map: upperTex, side: THREE.DoubleSide, roughness: 0.55, sheen: 0.25, sheenColor: new THREE.Color(0xffd7a0) });
  const wingMatLower = new THREE.MeshPhysicalMaterial({ map: lowerTex, side: THREE.DoubleSide, roughness: 0.58, sheen: 0.25, sheenColor: new THREE.Color(0xffd7a0) });

  function makeWing(side, upper) {
    // real outlines: a long forewing with a rounded apex, a broad rounded hindwing
    const P = upper
      ? [[0, 0.04], [0.3, 0.5], [0.85, 0.9], [1.22, 0.98], [1.36, 0.82], [1.28, 0.5], [1.08, 0.22], [0.62, 0.04], [0, -0.04]]
      : [[0, -0.02], [0.55, 0.02], [0.98, -0.18], [1.06, -0.52], [0.86, -0.86], [0.45, -0.98], [0.14, -0.7], [0, -0.3]];
    // the outline is drawn as (along the body, out from the body); the forewing reaches
    // forward, the hindwing back. Rotated so "out" is world Z: the wings spread sideways from the
    // body (which runs along X) and flap about it.
    const shape = new THREE.Shape();
    shape.moveTo(P[0][1] * 0.9, 0);
    shape.splineThru(P.slice(1).map(([o, a]) => new THREE.Vector2(a * 0.9, side * o)));
    shape.lineTo(P[0][1] * 0.9, 0);
    const geo = new THREE.ShapeGeometry(shape, 32);
    geo.rotateX(Math.PI / 2);
    geo.computeBoundingBox();
    const bb = geo.boundingBox; const pos = geo.attributes.position; const uv = geo.attributes.uv;
    const maxOut = Math.max(Math.abs(bb.min.z), Math.abs(bb.max.z));
    for (let i = 0; i < pos.count; i++) {
      uv.setXY(i, Math.abs(pos.getZ(i)) / maxOut, (pos.getX(i) - bb.min.x) / (bb.max.x - bb.min.x));
    }
    const m = new THREE.Mesh(geo, upper ? wingMatUpper : wingMatLower);
    m.castShadow = true;
    return m;
  }
  const pivots = {};
  [['left', -1], ['right', 1]].forEach(([name, side]) => {
    const pivot = new THREE.Group();
    pivot.add(makeWing(side, true));
    pivot.add(makeWing(side, false));
    bfGroup.add(pivot);
    pivots[name] = pivot;
  });
  [-1, 1].forEach((side) => {
    const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.006, 0.45, 6), bodyMat);
    ant.position.set(0.72, 0.16, side * 0.06); ant.rotation.z = -0.9; bfGroup.add(ant);
    const tip = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 8), bodyMat);
    tip.position.set(0.90, 0.30, side * 0.09); bfGroup.add(tip);
  });
  const probPts = [];
  for (let i = 0; i < 34; i++) {
    const a = i * 0.36; const r = 0.20 - i * 0.0035;
    probPts.push(new THREE.Vector3(0.66 + Math.cos(a) * r, -0.10 + Math.sin(a) * r, 0.03));
  }
  bfGroup.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(probPts), 44, 0.010, 6, false), bodyMat));
  [-1, 1].forEach((side) => {
    for (let i = 0; i < 3; i++) {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.45, 6), bodyMat);
      leg.position.set(-0.20 + i * 0.18, -0.16, side * 0.08);
      leg.rotation.x = side * 0.95; leg.rotation.z = 0.55 - i * 0.30;
      bfGroup.add(leg);
    }
  });
  builders.butterfly.add(bfGroup);

  // Each stage is a self-contained body built from dozens of individually placed primitives.
  // They are merged per stage group rather than across the whole root, because stage
  // visibility is toggled per group - a merged buffer spanning two stages could never hide.
  Object.values(builders).forEach((g) => {
    batchStaticGeometry(g, { mergeLines: true });
    root.add(g);
    g.visible = false;
  });

  // Ambient pollen motes
  const pollen = new Particles(scene, { max: low ? 26 : 48, size: 0.16, texture: glowTexture('pollen', { inner: 'rgba(255,244,200,1)', mid: 'rgba(250,220,130,0.4)' }) });
  let pollenAcc = 0;

  const timeline = new THREE.Group();
  const timelineSegments = [];
  const stageColors = STAGES.map((s) => new THREE.Color(s.color).getHex());
  STAGES.forEach((s, i) => {
    const mat = new THREE.MeshStandardMaterial({ color: stageColors[i], roughness: 0.42, emissive: stageColors[i], emissiveIntensity: 0.05 });
    const bar = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.07, 0.12), mat);
    bar.position.set(-1.35 + i * 0.90, -1.72, 0.05);
    timeline.add(bar);
    timelineSegments.push(bar);
  });
  scene.add(timeline);

  let labelSprite = null;
  const hud = createHud(stage);
  const stageBadge = hud.badge('Adult Butterfly', '#f9a8d4');
  const hintBadge = hud.badge('Drag the slider to change stage', '#a3e635');

  let current = 'butterfly';
  let durationOut = null;
  let timelineOut = null;
  let keyOut = null;
  function showStage(id) {
    current = id;
    Object.entries(builders).forEach(([k, g]) => { g.visible = (k === id); });
    const s = STAGES.find((x) => x.id === id);
    stageBadge.set(s.name);
    stageBadge.el.style.setProperty('--ix-hud-color', s.color);
    timelineSegments.forEach((bar, i) => {
      bar.material.emissiveIntensity = STAGES[i].id === id ? 0.55 : 0.05;
      bar.scale.y = STAGES[i].id === id ? 1.8 : 1.0;
    });
    if (durationOut) durationOut.set(s.duration);
    if (timelineOut) timelineOut.set(s.dayRange);
    if (keyOut) keyOut.set(s.key);
    if (labelSprite) root.remove(labelSprite);
    labelSprite = null;
  }

  const panel = createPanel(stage, { title: 'Butterfly Life Cycle' });
  panel.info('A butterfly transforms through four completely different bodies — complete metamorphosis. Drag the slider or tap a stage button to explore each one.');
  panel.slider({
    label: 'Stage', min: 0, max: STAGES.length - 1, step: 1, value: STAGES.length - 1,
    format: (v) => STAGES[v].name,
    onChange: (v) => { showStage(STAGES[v].id); },
  });
  panel.divider();
  STAGES.forEach((s) => {
    panel.button({
      label: s.name, icon: s.id === 'egg' ? 'circle' : s.id === 'caterpillar' ? 'pest_control' : s.id === 'chrysalis' ? 'spa' : 'flutter_dash',
      variant: 'ghost',
      onClick: () => { showStage(s.id); showInfoCard(stage, { title: s.name, body: s.info, color: s.color }); },
    });
  });
  panel.divider();
  durationOut = panel.readout({ label: 'Stage duration', value: STAGES[3].duration });
  timelineOut = panel.readout({ label: 'Timeline', value: STAGES[3].dayRange });
  keyOut = panel.readout({ label: 'Main process', value: STAGES[3].key });
  panel.readout({ label: 'Stages', value: '4 (complete metamorphosis)' });
  panel.readout({ label: 'Caterpillar growth', value: 'up to 100× birth weight' });
  panel.readout({ label: 'Model rule', value: 'egg → larva → pupa → adult' });
  panel.toggle({ label: 'Gentle spin', value: true, onChange: (v) => { spin = v; } });

  let spin = true;
  let wingPhase = 0;
  showStage('butterfly');

  let time = 0;
  engine.setUpdate((dt) => {
    time += dt;
    if (spin) root.rotation.y += dt * 0.25;
    if (current === 'butterfly') {
      wingPhase += dt * 9;
      // wings sweep from nearly flat to raised over the back
      const flap = 0.15 + Math.abs(Math.sin(wingPhase)) * 1.0;
      pivots.left.rotation.x = flap;
      pivots.right.rotation.x = -flap;
      bfGroup.position.y = 0.75 + Math.sin(time * 2.0) * 0.15;
      bfGroup.rotation.z = Math.sin(time * 1.3) * 0.06;
    } else if (current === 'caterpillar') {
      catGroup.rotation.z = Math.sin(time * 3.0) * 0.05;
    } else if (current === 'chrysalis') {
      chry.rotation.z = Math.sin(time * 1.4) * 0.05;
      chryMat.emissiveIntensity = 0.08 + Math.sin(time * 2.0) * 0.06;
    }
    pollenAcc += dt;
    if (pollenAcc > 0.4) {
      pollenAcc = 0;
      pollen.spawn((Math.random() - 0.5) * 7, -2 + Math.random() * 1.5, (Math.random() - 0.5) * 5,
        (Math.random() - 0.5) * 0.3, 0.35 + Math.random() * 0.3, (Math.random() - 0.5) * 0.2,
        6, new THREE.Color(0xffedb0));
    }
    pollen.update(dt, time);
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      disposeEnv();
      pollen.dispose();
      upperTex.dispose(); lowerTex.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
