import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/DRACOLoader.js';
import { createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard, hideInfoCard } from '../core/sim-ui.js';
import { addScanGradeEnhancement } from '../core/bio3d-scan-grade.js';
import { mergeWithPickMap, pickSource } from '../core/bio3d-batch.js';

const LAYERS = ['skin', 'muscle', 'skeleton', 'organs'];
const LAYER_LABEL = { skin: 'Skin', muscle: 'Muscles', skeleton: 'Skeleton', organs: 'Organs' };

const MUSCLE_INFO = 'Red ropes that can only pull, never push. Over 600 of them work in opposing pairs across your joints to move you. To bend the elbow, the biceps pulls; to straighten it, the triceps takes its turn.';
const SKELETON_INFO = 'Your frame of 206 bones. It holds you upright, protects soft organs like the brain and heart, and works with muscles as levers to let you move. Bone is living tissue — it rebuilds itself constantly.';
const SKIN_INFO = "Your body's largest organ and its waterproof suit. Skin keeps water in, germs out, and lets you feel the world through millions of nerve endings. It also cools you by sweating.";

const ORGANS = [
  { id: 'brain', name: 'Brain', color: 0xf2b3c5, pos: [0, 4.2, 0],
    info: 'Your control centre. The brain processes your senses, stores memories, and sends the signals that move every muscle. Wrapped safely in the skull, it uses about 20% of your energy even though it is only 2% of your weight.' },
  { id: 'heart', name: 'Heart', color: 0xc0392b, pos: [0.16, 1.56, 0.34],
    info: 'A muscular pump the size of your fist. It beats around 100,000 times a day, pushing blood through a network of vessels that would wrap around the Earth more than twice.' },
  { id: 'lungs', name: 'Lungs', color: 0xe08aa8, pos: [-0.48, 1.92, 0.12], second: [0.48, 1.92, 0.12],
    info: 'Your breathing organs. They take in the oxygen every cell needs and breathe out waste carbon dioxide. Unfolded, their air sacs would cover about half a tennis court.' },
  { id: 'liver', name: 'Liver', color: 0x7c3a23, pos: [0.34, 0.58, 0.26],
    info: "The body's chemical factory. The liver cleans the blood, stores energy, and helps turn food into fuel. It does over 500 different jobs — the busiest organ you have." },
  { id: 'stomach', name: 'Stomach', color: 0xd98b5f, pos: [-0.43, 0.38, 0.34],
    info: 'A stretchy muscular bag that churns food into a soup with strong acid and squeezing waves. The soup then flows into the intestines, where the goodness is absorbed.' },
  { id: 'intestines', name: 'Intestines', color: 0xc9a86b, pos: [0, -0.78, 0.30],
    info: 'A long coiled tube — about 7 metres if stretched out. The small intestine soaks up nutrients from food; the large intestine reclaims water and packs up what is left.' },
];

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-human-body-stage');
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(16, quality.segments / 2);

  camera.position.set(0, 1.5, 12);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 22, enablePan: false, maxPolar: Math.PI * 0.62, minPolar: Math.PI * 0.18,
  });
  controls.setTarget(new THREE.Vector3(0, 1, 0));

  scene.background = new THREE.Color(0x0e1424);
  scene.fog = new THREE.Fog(0x0e1424, 18, 36);
  basicLights(scene, { key: 1.7, ambient: 0.5 });
  const rim = new THREE.DirectionalLight(0x88aaff, 0.6); rim.position.set(-6, 3, -8); scene.add(rim);

  const groundGeo = new THREE.CircleGeometry(7, 48);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a2336, roughness: 0.95 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2; ground.position.y = -3.4; ground.receiveShadow = true;
  scene.add(ground);

  const root = new THREE.Group();
  scene.add(root);

  const layerGroups = {
    skin: new THREE.Group(),
    muscle: new THREE.Group(),
    skeleton: new THREE.Group(),
    organs: new THREE.Group(),
    vascular: new THREE.Group(),
    nerves: new THREE.Group(),
  };
  Object.values(layerGroups).forEach(g => { g.visible = false; root.add(g); });

  let clickableMeshes = [];
  const organMeshes = [];
  const organObjects = new Map();
  let modelLoaded = false;

  function organMat(o, rough) {
    const m = new THREE.MeshStandardMaterial({ color: o.color, roughness: rough ?? 0.55, metalness: 0.03 });
    m.emissive = new THREE.Color(o.color);
    m.emissiveIntensity = 0;
    return m;
  }

  function addOrganMesh(mesh, o) {
    mesh.castShadow = true; mesh.receiveShadow = true; mesh.userData.organ = o;
    layerGroups.organs.add(mesh); organMeshes.push(mesh); clickableMeshes.push(mesh);
    if (!organObjects.has(o.id)) organObjects.set(o.id, []);
    organObjects.get(o.id).push(mesh);
    return mesh;
  }

  function ellipsoid(o, rx, ry, rz, x, y, z, material, detail) {
    const geo = new THREE.SphereGeometry(1, detail || seg, Math.max(12, Math.floor((detail || seg) / 2)));
    geo.scale(rx, ry, rz);
    const mesh = new THREE.Mesh(geo, material || organMat(o));
    mesh.position.set(x, y, z);
    return addOrganMesh(mesh, o);
  }

  function cylBetween(o, a, b, r, material, radial) {
    const va = new THREE.Vector3(...a); const vb = new THREE.Vector3(...b);
    const mid = va.clone().add(vb).multiplyScalar(0.5);
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(r, r, va.distanceTo(vb), radial || 12), material || organMat(o));
    mesh.position.copy(mid);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), vb.clone().sub(va).normalize());
    return addOrganMesh(mesh, o);
  }

  function tubeOrgan(o, pts, r, material, tubularSeg) {
    const curve = new THREE.CatmullRomCurve3(pts.map(v => new THREE.Vector3(...v)));
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, tubularSeg || 48, r, 8, false), material || organMat(o));
    return addOrganMesh(mesh, o);
  }

  function addTube(target, pts, r, material, tubularSeg) {
    const curve = new THREE.CatmullRomCurve3(pts.map(v => new THREE.Vector3(...v)));
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, tubularSeg || 42, r, 8, false), material);
    mesh.castShadow = true; mesh.receiveShadow = true;
    target.add(mesh);
    return mesh;
  }

  function buildProceduralOrgans() {
    ORGANS.forEach(o => {
      const m = organMat(o);
      if (o.id === 'brain') {
        ellipsoid(o, 0.42, 0.30, 0.34, -0.22, 4.22, 0.02, m);
        ellipsoid(o, 0.42, 0.30, 0.34, 0.22, 4.22, 0.02, m);
        ellipsoid(o, 0.22, 0.15, 0.18, 0.00, 4.00, -0.10, organMat(o, 0.7), 24);
        for (let i = -3; i <= 3; i++) {
          const ridge = tubeOrgan(o, [[i * 0.08, 4.34, 0.28], [i * 0.10, 4.24, 0.35], [i * 0.08, 4.12, 0.25]], 0.009, new THREE.MeshStandardMaterial({ color: 0xd987a6, roughness: 0.8 }), 12);
          ridge.userData.organ = o;
        }
      } else if (o.id === 'lungs') {
        const lm = organMat(o, 0.66);
        ellipsoid(o, 0.34, 0.78, 0.26, o.pos[0], o.pos[1], o.pos[2], lm);
        ellipsoid(o, 0.34, 0.78, 0.26, o.second[0], o.second[1], o.second[2], lm);
        const trachea = new THREE.MeshStandardMaterial({ color: 0xf3e7d7, roughness: 0.58 });
        cylBetween(o, [0, 2.98, 0.06], [0, 2.12, 0.08], 0.055, trachea, 16);
        cylBetween(o, [0, 2.14, 0.08], [-0.36, 1.88, 0.10], 0.035, trachea, 12);
        cylBetween(o, [0, 2.14, 0.08], [0.36, 1.88, 0.10], 0.035, trachea, 12);
      } else if (o.id === 'heart') {
        const hm = organMat(o, 0.42);
        ellipsoid(o, 0.28, 0.34, 0.24, o.pos[0] - 0.09, o.pos[1] + 0.05, o.pos[2], hm);
        ellipsoid(o, 0.26, 0.32, 0.24, o.pos[0] + 0.12, o.pos[1] + 0.02, o.pos[2], hm);
        const apex = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.42, 24), hm);
        apex.position.set(o.pos[0] + 0.04, o.pos[1] - 0.35, o.pos[2]); apex.rotation.x = Math.PI; addOrganMesh(apex, o);
        cylBetween(o, [o.pos[0], o.pos[1] + 0.34, o.pos[2]], [o.pos[0] - 0.04, o.pos[1] + 0.72, o.pos[2]], 0.055, new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.48 }), 16);
        cylBetween(o, [o.pos[0] + 0.15, o.pos[1] + 0.28, o.pos[2]], [o.pos[0] + 0.40, o.pos[1] + 0.55, o.pos[2] + 0.02], 0.045, new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.48 }), 16);
      } else if (o.id === 'liver') {
        const liverMesh = ellipsoid(o, 0.72, 0.28, 0.34, o.pos[0], o.pos[1], o.pos[2], organMat(o, 0.62));
        liverMesh.rotation.z = -0.10;
        ellipsoid(o, 0.14, 0.09, 0.09, o.pos[0] - 0.36, o.pos[1] - 0.03, o.pos[2] + 0.20, new THREE.MeshStandardMaterial({ color: 0x236b38, roughness: 0.62 }), 16);
      } else if (o.id === 'stomach') {
        const st = ellipsoid(o, 0.30, 0.46, 0.22, o.pos[0], o.pos[1], o.pos[2], organMat(o, 0.55));
        st.rotation.z = -0.45;
        tubeOrgan(o, [[o.pos[0] + .12, o.pos[1] + .30, o.pos[2]], [o.pos[0] + .32, o.pos[1] + .12, o.pos[2]], [o.pos[0] + .18, o.pos[1] - .25, o.pos[2]]], .055, organMat(o, 0.58), 28);
      } else if (o.id === 'intestines') {
        const im = organMat(o, 0.78);
        for (let row = 0; row < 4; row++) {
          tubeOrgan(o, [[-0.50, -0.47 - row * 0.18, o.pos[2]], [-0.20, -0.58 - row * 0.18, o.pos[2]], [0.20, -0.44 - row * 0.18, o.pos[2]], [0.50, -0.56 - row * 0.18, o.pos[2]]], 0.055, im, 28);
        }
        tubeOrgan(o, [[-0.66, -0.36, o.pos[2] - .02], [-0.70, -1.20, o.pos[2] - .02], [0.70, -1.20, o.pos[2] - .02], [0.66, -0.36, o.pos[2] - .02]], 0.080, new THREE.MeshStandardMaterial({ color: 0xb99054, roughness: 0.76 }), 52);
      }
    });
  }

  function buildVascularAndNerves() {
    const arteryMat = new THREE.MeshStandardMaterial({ color: 0xe11d48, roughness: 0.42, emissive: 0x7f1d1d, emissiveIntensity: 0.10 });
    const veinMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.45, emissive: 0x1e3a8a, emissiveIntensity: 0.08 });
    const nerveMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.50, emissive: 0xf59e0b, emissiveIntensity: 0.12 });
    addTube(layerGroups.vascular, [[0.10,2.10,0.32],[0.12,1.52,0.34],[0.04,0.55,0.22],[0,-0.60,0.12]], 0.035, arteryMat, 54);
    addTube(layerGroups.vascular, [[-0.08,2.00,0.20],[-0.10,1.36,0.22],[-0.05,0.45,0.13],[0,-0.64,0.06]], 0.032, veinMat, 54);
    [-1, 1].forEach(side => {
      addTube(layerGroups.vascular, [[0.08,1.60,0.28],[side*0.50,1.54,0.22],[side*1.28,1.05,0.10],[side*1.70,-0.36,0.04]], 0.022, arteryMat, 44);
      addTube(layerGroups.vascular, [[-0.04,1.34,0.18],[side*0.42,1.38,0.14],[side*1.20,0.82,0.02],[side*1.62,-0.50,-0.02]], 0.020, veinMat, 44);
      addTube(layerGroups.vascular, [[0.02,-0.55,0.12],[side*0.34,-0.85,0.08],[side*0.50,-2.10,0.02],[side*0.52,-3.85,0.00]], 0.026, arteryMat, 48);
      addTube(layerGroups.vascular, [[-0.02,-0.55,0.06],[side*0.25,-0.90,0.00],[side*0.42,-2.10,-0.02],[side*0.45,-3.82,-0.06]], 0.022, veinMat, 48);
      addTube(layerGroups.nerves, [[0,3.82,-0.12],[side*0.42,2.70,-0.10],[side*1.22,1.24,-0.08],[side*1.70,-0.72,-0.04]], 0.014, nerveMat, 48);
      addTube(layerGroups.nerves, [[0,1.40,-0.12],[side*0.34,0.50,-0.10],[side*0.54,-1.54,-0.10],[side*0.56,-3.82,-0.10]], 0.014, nerveMat, 48);
    });
    addTube(layerGroups.nerves, [[0,4.00,-0.12],[0,2.80,-0.14],[0,1.35,-0.16],[0,-0.60,-0.12]], 0.020, nerveMat, 64);
    const vLabel = makeLabelSprite('arteries + veins', { scale: 0.42, fontSize: 28, bg: 'rgba(127,29,29,.72)' });
    vLabel.position.set(0.92, 2.78, 0.30); layerGroups.vascular.add(vLabel);
    const nLabel = makeLabelSprite('spinal cord + nerves', { scale: 0.42, fontSize: 28, bg: 'rgba(113,63,18,.72)' });
    nLabel.position.set(-1.00, 3.05, -0.22); layerGroups.nerves.add(nLabel);
  }

  function buildSkinOverlay() {
    const skinMat = new THREE.MeshStandardMaterial({ color: 0xe7a982, roughness: 0.7, transparent: true, opacity: 0.15 });
    const sR = 0.95;
    function part(mat, geo, x, y, z) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; return m; }
    layerGroups.skin.add(part(skinMat, new THREE.SphereGeometry(sR, seg, seg), 0, 4.2, 0));
    const torsoGeo = new THREE.SphereGeometry(1.35, seg, seg); torsoGeo.scale(1, 1.45, 0.72);
    layerGroups.skin.add(part(skinMat, torsoGeo, 0, 1.6, 0));
    const upperArmGeo = new THREE.SphereGeometry(0.45, seg, seg); upperArmGeo.scale(1, 2.3, 1);
    const foreArmGeo = new THREE.SphereGeometry(0.38, seg, seg); foreArmGeo.scale(1, 2.0, 1);
    layerGroups.skin.add(part(skinMat, upperArmGeo, 1.55, 1.9, 0)); layerGroups.skin.add(part(skinMat, upperArmGeo, -1.55, 1.9, 0));
    layerGroups.skin.add(part(skinMat, foreArmGeo, 1.7, -0.5, 0)); layerGroups.skin.add(part(skinMat, foreArmGeo, -1.7, -0.5, 0));
    const thighGeo = new THREE.SphereGeometry(0.55, seg, seg); thighGeo.scale(1, 2.4, 1);
    const shinGeo = new THREE.SphereGeometry(0.45, seg, seg); shinGeo.scale(1, 2.2, 1);
    layerGroups.skin.add(part(skinMat, thighGeo, 0.55, -0.8, 0)); layerGroups.skin.add(part(skinMat, thighGeo, -0.55, -0.8, 0));
    layerGroups.skin.add(part(skinMat, shinGeo, 0.55, -3.0, 0)); layerGroups.skin.add(part(skinMat, shinGeo, -0.55, -3.0, 0));
  }

  const labels = ORGANS.map(o => {
    const s = makeLabelSprite(o.name, { scale: 0.6, fontSize: 34 });
    s.position.set(o.pos[0], o.pos[1] + (o.id === 'brain' ? 0.95 : 0.75), o.pos[2]);
    s.visible = false; return s;
  });

  let currentLayer = 'organs';
  function setLayer(layer) {
    currentLayer = layer;
    layerGroups.skin.visible = (layer === 'skin');
    layerGroups.muscle.visible = (layer === 'muscle');
    layerGroups.skeleton.visible = (layer === 'skeleton' || layer === 'organs');
    layerGroups.organs.visible = (layer === 'organs');
    layerGroups.vascular.visible = (layer === 'organs');
    layerGroups.nerves.visible = (layer === 'organs' || layer === 'skeleton');
    labels.forEach(l => { l.visible = (layer === 'organs'); });
    if (layer !== 'skin') {
      layerGroups.skin.visible = true;
      layerGroups.skin.children.forEach(c => { if (c.material) c.material.opacity = layer === 'muscle' ? 0.10 : 0.05; });
    }
    layerBadge.set(LAYER_LABEL[layer]);
    layerBadge.el.style.setProperty('--ix-hud-color', '#84CC16');
  }

  const hud = createHud(stage);
  const layerBadge = hud.badge('Organs', '#84CC16');
  const partBadge = hud.badge('Tap a body part!', '#a3e635');
  let activity = 20;
  function bodyHeartRate() { return Math.round(70 + activity * 0.9); }
  function bodyBreathingRate() { return Math.round(12 + activity * 0.28); }
  function bodyCardiacOutput() { return (bodyHeartRate() * (70 + activity * 0.45)) / 1000; }
  function bodyVentilation() { return (bodyBreathingRate() * (500 + activity * 14)) / 1000; }

  let selected = null;
  function highlight(obj) {
    clickableMeshes.forEach(m => {
      if (m.material && m.material.emissiveIntensity !== undefined) m.material.emissiveIntensity = 0;
      if (m.material && m.material.emissive) m.material.emissive.setHex(0x000000);
    });
    if (obj && obj.material) {
      if (obj.material.emissive) obj.material.emissive.setHex(0xff0000);
      obj.material.emissiveIntensity = 0.35;
    }
  }

  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let downPos = null;

  function getLayerInfo(layer) {
    if (layer === 'skin') return { title: 'Skin', body: SKIN_INFO };
    if (layer === 'muscle') return { title: 'Muscles', body: MUSCLE_INFO };
    if (layer === 'skeleton') return { title: 'Skeleton', body: SKELETON_INFO };
    return null;
  }

  function onDown(e) { downPos = { x: e.clientX, y: e.clientY }; }

  function onUp(e) {
    if (!downPos || Math.hypot(e.clientX - downPos.x, e.clientY - downPos.y) > 8) return;
    if (!modelLoaded) return;
    if (currentLayer !== 'organs') {
      const info = getLayerInfo(currentLayer);
      if (info) showInfoCard(stage, { title: info.title, body: info.body, color: '#84CC16' });
      return;
    }
    const rect = engine.canvas.getBoundingClientRect();
    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(clickableMeshes, false);
    if (hits.length) {
      // Merged anatomy buffers keep a face->source table, so a tap still resolves to the
      // individual bone or muscle that produced the hit rather than the whole merged mesh.
      const obj = pickSource(hits[0].object, hits[0].faceIndex) || hits[0].object;
      selected = obj;
      highlight(obj);

      const organ = obj.userData.organ;
      const name = obj.userData.name || obj.userData.organ?.name || obj.name || 'Body part';
      const desc = obj.userData.nameDetail || '';

      if (organ) {
        partBadge.set(organ.name);
        if (selectedOut) selectedOut.set(organ.name);
        showInfoCard(stage, {
          title: organ.name, body: `${organ.info} Live physiology: at the current activity setting, heart rate is ${bodyHeartRate()} bpm and estimated cardiac output is ${bodyCardiacOutput().toFixed(1)} L/min.`,
          color: '#84CC16',
        });
      } else {
        partBadge.set(name);
        if (selectedOut) selectedOut.set(name);
        const infoText = desc ? `${name} — ${desc}` : `You selected: ${name}. This is part of the ${currentLayer} layer.`;
        showInfoCard(stage, { title: name, body: infoText, color: '#84CC16' });
      }
    }
  }

  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);

  let heartRateOut, breathRateOut, cardiacOut, ventilationOut, selectedOut;
  function updatePhysiologyReadouts() {
    if (!heartRateOut) return;
    heartRateOut.set(`${bodyHeartRate()} bpm`);
    breathRateOut.set(`${bodyBreathingRate()} /min`);
    cardiacOut.set(`${bodyCardiacOutput().toFixed(1)} L/min`);
    ventilationOut.set(`${bodyVentilation().toFixed(1)} L/min`);
  }

  const panel = createPanel(stage, { title: 'Human Body Explorer' });
  panel.info('Drag to rotate the anatomical model. Use the layer slider to explore muscles, skeleton and organs. Tap any part to learn its name.');
  const slider = panel.slider({
    label: 'Body layer', min: 0, max: LAYERS.length - 1, step: 1, value: LAYERS.indexOf(currentLayer),
    format: v => LAYER_LABEL[LAYERS[v]],
    onChange: v => { setLayer(LAYERS[v]); selected = null; highlight(null); partBadge.set('Tap a body part!'); if (selectedOut) selectedOut.set(LAYER_LABEL[LAYERS[v]]); hideInfoCard(stage); },
  });
  panel.slider({
    label: 'Physiology activity', min: 0, max: 100, step: 1, value: activity,
    format: v => v < 25 ? 'Rest' : v < 60 ? 'Active' : v < 85 ? 'Running' : 'Sprinting',
    onChange: v => { activity = v; updatePhysiologyReadouts(); },
  });
  panel.divider();
  selectedOut = panel.readout({ label: 'Selected part', value: 'Whole body' });
  heartRateOut = panel.readout({ label: 'Heart rate', value: `${bodyHeartRate()} bpm` });
  breathRateOut = panel.readout({ label: 'Breathing rate', value: `${bodyBreathingRate()} /min` });
  cardiacOut = panel.readout({ label: 'Cardiac output', value: `${bodyCardiacOutput().toFixed(1)} L/min` });
  ventilationOut = panel.readout({ label: 'Minute ventilation', value: `${bodyVentilation().toFixed(1)} L/min` });
  panel.readout({ label: 'Bones', value: '206' });
  panel.readout({ label: 'Muscles', value: '600+' });
  panel.toggle({ label: 'Slow spin', value: true, onChange: v => { spin = v; } });

  let spin = true;

  engine.setUpdate(dt => {
    if (spin) root.rotation.y += dt * 0.18;
    const t = performance.now() * 0.001;
    const breath = Math.sin(t * (bodyBreathingRate() / 60) * Math.PI * 2) * 0.5 + 0.5;
    if (modelLoaded) {
      layerGroups.organs.scale.setScalar(1 + Math.sin(t * 1.2) * 0.008);
      (organObjects.get('lungs') || []).forEach(m => { m.scale.setScalar(1 + breath * 0.055); });
      const beat = Math.sin(t * (bodyHeartRate() / 60) * Math.PI * 2);
      (organObjects.get('heart') || []).forEach(m => {
        const s = 1 + Math.max(0, beat) * 0.075;
        m.scale.setScalar(s);
        m.material.emissiveIntensity = 0.04 + Math.max(0, beat) * 0.24;
      });
      layerGroups.vascular.children.forEach(child => {
        if (child.material && child.material.emissiveIntensity !== undefined)
          child.material.emissiveIntensity = 0.06 + Math.max(0, beat) * 0.16;
      });
    }
    if (selected && selected.material) selected.material.emissiveIntensity = 0.25 + Math.sin(t * 4) * 0.12;
    controls.update(dt);
  });

  const loading = document.getElementById('ix-sim-loading');
  if (loading) loading.style.display = '';

  const loader = new GLTFLoader();
  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath('/static/web/js/vendor/draco/');
  loader.setDRACOLoader(dracoLoader);
  loader.load(
    '/static/web/js/interactive/biology/models/body.glb',
    gltf => {
      const model = gltf.scene || (gltf.scenes && gltf.scenes[0]);
      if (!model) {
        console.error('GLTF scene is undefined - model may be empty or DRACO decompression failed');
        if (onError) onError(new Error('Scene undefined'));
        return;
      }
      const box = new THREE.Box3().setFromObject(model);
      const center = box.getCenter(new THREE.Vector3());
      model.position.sub(center);

      const meshesToProcess = [];
      model.traverse(child => {
        if (child.isMesh) {
          meshesToProcess.push(child);
        }
      });

      // The anatomy model ships as 826 separate meshes sharing just 2 materials, so it costs
      // 826 draw calls a frame. They are parked in one temporary group per anatomical layer
      // and merged after every other enhancement has run - merging first would make the
      // scan-grade pass operate on a handful of huge buffers instead of the original parts.
      const gltfBuckets = new Map();
      meshesToProcess.forEach(child => {
        const type = child.userData.type;
        let layer = layerGroups.organs;
        if (type === 'bone') layer = layerGroups.skeleton;
        else if (type === 'muscle') layer = layerGroups.muscle;
        let bucket = gltfBuckets.get(layer);
        if (!bucket) { bucket = new THREE.Group(); layer.add(bucket); gltfBuckets.set(layer, bucket); }
        bucket.add(child);
        child.castShadow = true;
        child.receiveShadow = true;
        if (!child.userData.originalMaterial) {
          child.userData.originalMaterial = child.material;
        }
      });

      buildProceduralOrgans();
      buildVascularAndNerves();
      buildSkinOverlay();

      labels.forEach(l => layerGroups.organs.add(l));

      addScanGradeEnhancement(root, { kind: 'humanBody', quality, seed: 'human-body-explorer' });

      // Merge each layer once the model has been fully enhanced. Procedural organs sit
      // outside these buckets on purpose: the heart and lungs are animated individually.
      for (const bucket of gltfBuckets.values()) {
        try {
          mergeWithPickMap(bucket, { mergeLines: true });
        } catch (e) {
          // A merge failure must never cost the student the model: parts stay unmerged, which
          // is slow but renders correctly.
          console.error('Anatomy merge failed, rendering unmerged:', e);
        }
        for (const child of bucket.children) if (child.isMesh) clickableMeshes.push(child);
      }

      labels.forEach(l => { l.visible = false; });
      modelLoaded = true;
      setLayer('organs');
      updatePhysiologyReadouts();
      engine.renderOnce();

      if (loading) loading.style.display = 'none';
    },
    xhr => {
      if (loading && xhr.total) {
        const pct = Math.round((xhr.loaded / xhr.total) * 100);
        if (pct < 100) loading.innerHTML = `<div class="ix-spinner md-loader md-loader-screen"></div><p>Loading anatomy model… ${pct}%</p>`;
      }
    },
    err => {
      console.error('Failed to load anatomy model:', err);
      buildProceduralOrgans();
      buildVascularAndNerves();
      buildSkinOverlay();
      labels.forEach(l => layerGroups.organs.add(l));
      addScanGradeEnhancement(root, { kind: 'humanBody', quality, seed: 'human-body-explorer' });
      modelLoaded = true;
      setLayer('organs');
      updatePhysiologyReadouts();
      engine.renderOnce();
      if (loading) loading.innerHTML = '<p>3D model loaded in fallback mode.</p>';
      setTimeout(() => { if (loading && loading.parentNode) loading.remove(); }, 2000);
    },
  );

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown);
      engine.canvas.removeEventListener('pointerup', onUp);
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
