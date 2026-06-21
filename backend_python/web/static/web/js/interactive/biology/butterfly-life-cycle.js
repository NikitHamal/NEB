import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { addScanGradeEnhancement } from '../core/bio3d-scan-grade.js';

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

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-butterfly-stage');
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(14, quality.segments / 2);

  camera.position.set(0, 1.5, 11);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4, maxDistance: 18, enablePan: false, maxPolar: Math.PI * 0.7, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 1, 0));

  scene.background = new THREE.Color(0x0c1426);
  scene.fog = new THREE.Fog(0x0c1426, 16, 32);
  basicLights(scene, { ambient: 0.5, key: 1.6 });
  const fill = new THREE.DirectionalLight(0xffd9a8, 0.4); fill.position.set(-5, 3, -5); scene.add(fill);

  // Twig / ground
  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(7, 48),
    new THREE.MeshStandardMaterial({ color: 0x1a2e1a, roughness: 1 })
  );
  ground.rotation.x = -Math.PI / 2; ground.position.y = -2.2; ground.receiveShadow = true; scene.add(ground);

  // A branch for the chrysalis / butterfly to rest on
  const branch = new THREE.Mesh(
    new THREE.CylinderGeometry(0.08, 0.1, 5, 10),
    new THREE.MeshStandardMaterial({ color: 0x5d4037, roughness: 0.9 })
  );
  branch.position.set(0, -0.5, 0); branch.rotation.z = 0.15; branch.castShadow = true; scene.add(branch);
  // leaf on the branch
  const leafMat = new THREE.MeshStandardMaterial({ color: 0x4caf50, side: THREE.DoubleSide, roughness: 0.6 });
  const leafGeo = new THREE.CircleGeometry(0.7, 24);
  leafGeo.scale(1, 0.5, 1);
  const leafMesh = new THREE.Mesh(leafGeo, leafMat);
  leafMesh.position.set(1.2, 0.4, 0); leafMesh.rotation.set(-0.5, 0, 0.4); leafMesh.castShadow = true; scene.add(leafMesh);
  const leafVeinMat = new THREE.LineBasicMaterial({ color: 0x1b5e20, transparent: true, opacity: 0.55 });
  for (let i = -2; i <= 2; i++) {
    const vein = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(1.2, 0.43, 0.025),
      new THREE.Vector3(1.2 + i * 0.18, 0.46 + Math.abs(i) * 0.05, 0.025),
    ]);
    const line = new THREE.Line(vein, leafVeinMat); line.rotation.set(-0.5, 0, 0.4); scene.add(line);
  }

  const root = new THREE.Group(); scene.add(root);

  // ---- Build each stage as a group; toggle visibility ----
  const builders = {};

  // EGG: cluster of tiny ovals on the leaf
  builders.egg = new THREE.Group();
  const eggMat = new THREE.MeshStandardMaterial({ color: 0xfde68a, roughness: 0.35 });
  for (let i = 0; i < 9; i++) {
    const g = new THREE.SphereGeometry(0.13, 14, 14); g.scale(0.8, 1.1, 0.8);
    const m = new THREE.Mesh(g, eggMat);
    const a = (i / 9) * Math.PI * 2;
    m.position.set(1.2 + Math.cos(a) * 0.18, 0.42, Math.sin(a) * 0.18);
    m.castShadow = true; builders.egg.add(m);
  }

  // CATERPILLAR: segmented body on the leaf
  builders.caterpillar = new THREE.Group();
  const catGroup = new THREE.Group();
  const segMat = new THREE.MeshStandardMaterial({ color: 0x66bb6a, roughness: 0.55 });
  const stripeMat = new THREE.MeshStandardMaterial({ color: 0x2e7d32, roughness: 0.55 });
  for (let i = 0; i < 8; i++) {
    const r = 0.22 + Math.sin(i * 0.5) * 0.03;
    const g = new THREE.SphereGeometry(r, 16, 16);
    const m = new THREE.Mesh(g, i % 2 === 0 ? segMat : stripeMat);
    m.position.set(0.4 + i * 0.32, 0.55, 0); m.castShadow = true; catGroup.add(m);
  }
  // head + eyes
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.26, 16, 16), segMat);
  head.position.set(0.05, 0.55, 0); head.castShadow = true; catGroup.add(head);
  [-0.08, 0.08].forEach((dz) => {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), new THREE.MeshStandardMaterial({ color: 0x111111 }));
    eye.position.set(-0.05, 0.6, dz); catGroup.add(eye);
  });
  // true larval detail: thoracic legs plus abdominal prolegs
  const legMat = new THREE.MeshStandardMaterial({ color: 0x1b4332, roughness: 0.75 });
  for (let i = 1; i < 8; i++) {
    [-1, 1].forEach((side) => {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.010, 0.22, 6), legMat);
      leg.position.set(0.18 + i * 0.32, 0.36, side * 0.10);
      leg.rotation.x = side * 0.65; leg.rotation.z = i < 4 ? -0.25 : 0.18;
      catGroup.add(leg);
    });
  }
  // antennae
  [-0.08, 0.08].forEach((dz) => {
    const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.3, 6), new THREE.MeshStandardMaterial({ color: 0x222222 }));
    ant.position.set(-0.12, 0.78, dz); ant.rotation.z = 0.5; catGroup.add(ant);
  });
  builders.caterpillar.add(catGroup);

  // CHRYSALIS: hanging pod from branch
  builders.chrysalis = new THREE.Group();
  const chryGeo = new THREE.SphereGeometry(0.5, 24, 24); chryGeo.scale(0.55, 1.5, 0.55);
  const chryMat = new THREE.MeshStandardMaterial({
    color: 0xc4b5fd, roughness: 0.3, metalness: 0.2, transparent: true, opacity: 0.85,
    emissive: 0x7c3aed, emissiveIntensity: 0.08,
  });
  const chry = new THREE.Mesh(chryGeo, chryMat);
  chry.position.set(0.1, 0.2, 0); chry.castShadow = true; builders.chrysalis.add(chry);
  // gold band detail
  const band = new THREE.Mesh(
    new THREE.TorusGeometry(0.22, 0.03, 8, 24),
    new THREE.MeshStandardMaterial({ color: 0xffd54a, metalness: 0.7, roughness: 0.2 })
  );
  band.position.set(0.1, 0.55, 0); band.rotation.x = Math.PI / 2; builders.chrysalis.add(band);
  // silk thread
  const silk = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.5, 6), new THREE.MeshStandardMaterial({ color: 0xeeeeee }));
  silk.position.set(0.1, 0.85, 0); builders.chrysalis.add(silk);

  // BUTTERFLY: body + 4 wings
  builders.butterfly = new THREE.Group();
  const bfGroup = new THREE.Group();
  bfGroup.position.set(0.1, 0.6, 0);
  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.6 });
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.1, 12), bodyMat);
  body.rotation.z = Math.PI / 2; bfGroup.add(body);
  const wingMatUpper = new THREE.MeshStandardMaterial({ color: 0xf472b6, side: THREE.DoubleSide, roughness: 0.4 });
  const wingMatLower = new THREE.MeshStandardMaterial({ color: 0xc084fc, side: THREE.DoubleSide, roughness: 0.4 });
  function makeWing(side, upper) {
    const shape = new THREE.Shape();
    shape.moveTo(0, 0);
    shape.bezierCurveTo(side * 1.2, upper ? 0.9 : -0.6, side * 1.6, upper ? 0.4 : -0.2, side * 0.1, upper ? 0.1 : -0.4);
    shape.bezierCurveTo(side * -0.2, upper ? 0.4 : -0.1, side * -0.1, upper ? 0.6 : -0.3, 0, 0);
    const geo = new THREE.ShapeGeometry(shape, 24);
    const m = new THREE.Mesh(geo, upper ? wingMatUpper : wingMatLower);
    m.castShadow = true;
    m.position.set(0, upper ? 0.05 : -0.05, upper ? 0.0 : 0.0);
    return m;
  }
  const wings = [];
  const wlUp = makeWing(-1, true); const wrUp = makeWing(1, true);
  const wlDn = makeWing(-1, false); const wrDn = makeWing(1, false);
  [wlUp, wrUp, wlDn, wrDn].forEach((w) => { bfGroup.add(w); wings.push(w); });
  // realistic wing veins and eyespots
  const veinMat = new THREE.LineBasicMaterial({ color: 0x24111d, transparent: true, opacity: 0.55 });
  [-1, 1].forEach((side) => {
    for (let i = 0; i < 5; i++) {
      const y = -0.25 + i * 0.22;
      const vein = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, 0.018), new THREE.Vector3(side * (0.58 + i * 0.13), y, 0.018)]);
      bfGroup.add(new THREE.Line(vein, veinMat));
    }
    [[0.72,0.45,0.14,0xffeb3b],[1.08,0.18,0.09,0x111827],[0.58,-0.28,0.10,0xfff7ed]].forEach(([x,y,r,c]) => {
      const spot = new THREE.Mesh(new THREE.CircleGeometry(r, 18), new THREE.MeshStandardMaterial({ color: c, side: THREE.DoubleSide }));
      spot.position.set(side * x, y, 0.024); bfGroup.add(spot);
    });
  });
  // antennae
  [-1, 1].forEach((side) => {
    const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.45, 6), bodyMat);
    ant.position.set(0.55, 0.18, side * 0.06); ant.rotation.z = -0.8; bfGroup.add(ant);
    const tip = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), bodyMat);
    tip.position.set(0.75, 0.35, side * 0.1); bfGroup.add(tip);
  });
  // coiled proboscis and six legs, so the adult model reads as an insect rather than a decorative icon.
  const probPts = [];
  for (let i = 0; i < 34; i++) {
    const a = i * 0.36; const r = 0.22 - i * 0.0035;
    probPts.push(new THREE.Vector3(0.52 + Math.cos(a) * r, -0.05 + Math.sin(a) * r, 0.03));
  }
  const prob = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(probPts), 44, 0.010, 6, false), bodyMat);
  bfGroup.add(prob);
  [-1, 1].forEach((side) => {
    for (let i = 0; i < 3; i++) {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.45, 6), bodyMat);
      leg.position.set(-0.20 + i * 0.18, -0.12, side * 0.08);
      leg.rotation.x = side * 0.95; leg.rotation.z = 0.55 - i * 0.30;
      bfGroup.add(leg);
    }
  });
  builders.butterfly.add(bfGroup);

  // Add all stage groups
  Object.values(builders).forEach((g) => { root.add(g); g.visible = false; });
  addScanGradeEnhancement(root, { kind: 'butterflyLifeCycle', quality, seed: 'butterfly-life-cycle' });

  // 3D timeline with one segment per life stage. The active segment glows in showStage().
  const timeline = new THREE.Group();
  const timelineSegments = [];
  const stageColors = STAGES.map((s) => new THREE.Color(s.color).getHex());
  STAGES.forEach((s, i) => {
    const mat = new THREE.MeshStandardMaterial({ color: stageColors[i], roughness: 0.42, emissive: stageColors[i], emissiveIntensity: 0.05 });
    const bar = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.07, 0.12), mat);
    bar.position.set(-1.35 + i * 0.90, -1.72, 0.05);
    timeline.add(bar);
    const tag = makeLabelSprite(s.name, { scale: 0.22, fontSize: 20, bg: 'rgba(15,23,42,.70)' });
    tag.position.set(bar.position.x, -1.50, 0.08);
    timeline.add(tag);
    timelineSegments.push(bar);
  });
  scene.add(timeline);

  // Labels (sprite) for current stage
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
    labelSprite = makeLabelSprite(s.name, { scale: 0.7, fontSize: 40 });
    labelSprite.position.set(0, 2.4, 0);
    root.add(labelSprite);
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

  engine.setUpdate((dt) => {
    if (spin) root.rotation.y += dt * 0.25;
    if (current === 'butterfly') {
      wingPhase += dt * 8;
      const flap = Math.sin(wingPhase) * 0.5 + 0.2;
      // flap wings: scale x to fold
      wings[0].scale.x = 0.4 + Math.abs(Math.sin(wingPhase)) * 0.6; // left up
      wings[1].scale.x = 0.4 + Math.abs(Math.sin(wingPhase)) * 0.6; // right up
      wings[2].scale.x = 0.5 + Math.abs(Math.sin(wingPhase + 0.4)) * 0.5;
      wings[3].scale.x = 0.5 + Math.abs(Math.sin(wingPhase + 0.4)) * 0.5;
      // hover
      bfGroup.position.y = 0.6 + Math.sin(performance.now() * 0.002) * 0.15;
    } else if (current === 'caterpillar') {
      // wiggle
      catGroup.rotation.z = Math.sin(performance.now() * 0.003) * 0.05;
    } else if (current === 'chrysalis') {
      chry.material.emissiveIntensity = 0.08 + Math.sin(performance.now() * 0.002) * 0.06;
    }
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
