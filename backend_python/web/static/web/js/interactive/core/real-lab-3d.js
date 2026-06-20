import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from './engine.js';
import { createPanel, createHud, showInfoCard } from './sim-ui.js';
import { ANION_RESULTS, CATION_COLORS, GAS_RESULTS, GROUP_RESULTS, PRESETS, SUBJECT } from './lab3d-data.js';
import { addObservationTable, currentProcedureText, indicatorColor, indicatorColorName, lassaigneResult, procedureSteps, recordObservation, titrationStatus } from './lab3d-science.js';
import { buildPrecisionCaliper, buildPrecisionMicrometer, buildPrecisionSpherometer } from './lab3d-precision.js';

function makeScaleTexture({ length = 100, major = 10, minor = 1, label = 'cm', width = 1024, height = 128, dark = false } = {}) {
  const canvas = document.createElement('canvas');
  canvas.width = width; canvas.height = height;
  const ctx = canvas.getContext('2d');
  const bg = dark ? '#111827' : '#f8fafc';
  ctx.fillStyle = bg; ctx.fillRect(0, 0, width, height);
  ctx.fillStyle = dark ? '#e5e7eb' : '#020617';
  ctx.strokeStyle = dark ? 'rgba(241,245,249,.95)' : 'rgba(15,23,42,.92)';
  ctx.lineWidth = 2;
  const pad = 22; const usable = width - pad * 2;
  for (let i = 0; i <= length; i += minor) {
    const x = pad + usable * (i / length);
    const isMajor = i % major === 0;
    const isHalf = i % (major / 2) === 0;
    const h = isMajor ? height * 0.60 : isHalf ? height * 0.42 : height * 0.26;
    ctx.beginPath(); ctx.moveTo(x, height - 5); ctx.lineTo(x, height - h); ctx.stroke();
    if (isMajor) {
      ctx.font = '700 26px system-ui, sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'top';
      ctx.fillText(String(i / major), x, 9);
    }
  }
  ctx.font = '700 18px system-ui, sans-serif'; ctx.textAlign = 'right'; ctx.textBaseline = 'top';
  ctx.fillText(label, width - 18, 10);
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

function makeScalePlane(lengthWorld = 8, heightWorld = 0.55, opts = {}) {
  const tex = makeScaleTexture(opts);
  const material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(lengthWorld, heightWorld), material);
  mesh.userData.texture = tex;
  return mesh;
}

function addBenchDetails(group, subject) {
  const accent = subject === 'chemistry' ? 0x10b981 : 0xf59e0b;
  for (let i = -4; i <= 4; i++) {
    const l1 = makeLine([new THREE.Vector3(i, 0.815, -3.2), new THREE.Vector3(i, 0.815, 3.2)], 0xffffff, 0.055);
    const l2 = makeLine([new THREE.Vector3(-5.0, 0.816, i * 0.7), new THREE.Vector3(5.0, 0.816, i * 0.7)], 0xffffff, 0.055);
    group.add(l1, l2);
  }
  const edge = makeBox(10.4, 0.06, 0.08, mat(accent, { opacity: 0.72, emissive: accent, emissiveIntensity: 0.18 }), [0, 0.85, -3.22]);
  group.add(edge);
}

function makeNeedleGauge(label, value, max, accent = 0x38bdf8) {
  const g = new THREE.Group();
  const face = makeCylinder(0.48, 0.48, 0.08, mat(0xf8fafc), [0, 0, 0], 64);
  face.rotation.x = Math.PI / 2; g.add(face);
  for (let i = 0; i <= 10; i++) {
    const a = -Math.PI * 0.72 + i * Math.PI * 1.44 / 10;
    const r1 = 0.34, r2 = i % 5 === 0 ? 0.45 : 0.41;
    g.add(makeLine([new THREE.Vector3(Math.cos(a)*r1, Math.sin(a)*r1, 0.06), new THREE.Vector3(Math.cos(a)*r2, Math.sin(a)*r2, 0.06)], 0x111827, 1));
  }
  const needle = makeBox(0.035, 0.38, 0.018, mat(accent, { emissive: accent, emissiveIntensity: 0.18 }), [0, 0.17, 0.09]);
  needle.geometry.translate(0, 0.19, 0); needle.rotation.z = -0.75 + Math.min(1, value / max) * 1.5; g.add(needle);
  addLabel(g, label, [0, -0.62, 0.1], { scale: 0.13, fontSize: 26, bg: false, color: '#111827' });
  return { group: g, needle };
}

function initState(config) {
  const state = {
    running: true,
    sample: Math.random(),
    stepIndex: 0,
    observations: [],
    lastRecordedAt: 0,
  };
  config.controls.forEach((control) => { state[control.id] = control.value; });
  return state;
}

function fmtControl(control, value) {
  if (control.type === 'select') return String(value);
  const decimals = String(control.step || 1).includes('.') ? Math.min(3, String(control.step).split('.')[1].length) : 0;
  return `${Number(value).toFixed(decimals)}${control.unit || ''}`;
}

function randomValue(control) {
  const min = Number(control.min ?? 0);
  const max = Number(control.max ?? 1);
  const step = Number(control.step || 1);
  const raw = min + Math.random() * (max - min);
  return Math.round(raw / step) * step;
}


function cameraViewFor(kind, quality) {
  const mobile = quality && quality.mobile;
  const distanceBoost = mobile ? 1.32 : 1;
  const heightBoost = mobile ? 1.08 : 1;
  const views = {
    caliper: { position: [0.4, 6.4 * heightBoost, 8.8 * distanceBoost], target: [0.0, 1.62, 0.16], min: 4.6, max: 16 },
    micrometer: { position: [3.6 * distanceBoost, 3.3 * heightBoost, 6.4 * distanceBoost], target: [0.25, 1.82, 0.12], min: 3.8, max: 15 },
    spherometer: { position: [4.1 * distanceBoost, 4.6 * heightBoost, 6.6 * distanceBoost], target: [0, 1.7, 0.1], min: 3.8, max: 14 },
    circuit: { position: [5.6 * distanceBoost, 4.8 * heightBoost, 7.2 * distanceBoost], target: [0, 1.10, 0], min: 4, max: 17 },
    meterbridge: { position: [0.0, 6.1 * heightBoost, 8.8 * distanceBoost], target: [0, 1.08, 0], min: 5, max: 18 },
    titration: { position: [4.4 * distanceBoost, 4.2 * heightBoost, 7.4 * distanceBoost], target: [0, 1.75, 0], min: 4, max: 15 },
    apparatus: { position: [5.8 * distanceBoost, 4.5 * heightBoost, 8.4 * distanceBoost], target: [0, 1.45, 0], min: 4.5, max: 18 },
  };
  return views[kind] || { position: [6.2 * distanceBoost, 5.1 * heightBoost, 10.8 * distanceBoost], target: [0, 1.25, 0], min: 5, max: 20 };
}

function resetCameraView(camera, controls, view) {
  const pos = new THREE.Vector3(...view.position);
  const target = new THREE.Vector3(...view.target);
  if (controls.setView) controls.setView(pos, target);
  else {
    camera.position.copy(pos);
    controls.setTarget(target);
    camera.lookAt(target);
  }
}

function disposeObject(obj) {
  if (!obj) return;
  obj.traverse((child) => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      const mats = Array.isArray(child.material) ? child.material : [child.material];
      mats.forEach((m) => {
        Object.keys(m).forEach((k) => { if (m[k] && m[k].isTexture) m[k].dispose(); });
        m.dispose();
      });
    }
  });
}

export function initRealLab3D(stage, opts = {}) {
  const slug = opts.preset || opts.lessonSlug;
  const config = PRESETS[slug] || PRESETS['lab-apparatus-safety'];
  const subject = SUBJECT[config.subject] || SUBJECT.physics;
  const engine = createEngine(stage, { shadows: true, fov: 45, far: 260 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;

  scene.background = new THREE.Color(config.subject === 'chemistry' ? 0x061a16 : 0x0b1020);
  scene.fog = new THREE.Fog(scene.background, 18, 52);
  if (engine.renderer.toneMapping !== undefined) engine.renderer.toneMapping = THREE.ACESFilmicToneMapping;
  if (engine.renderer.outputColorSpace !== undefined && THREE.SRGBColorSpace) engine.renderer.outputColorSpace = THREE.SRGBColorSpace;

  stage.dataset.labKind = config.kind;
  const view = cameraViewFor(config.kind, quality);
  camera.position.set(...view.position);
  const controls = createOrbitControls(camera, engine.canvas, {
    target: new THREE.Vector3(...view.target),
    minDistance: view.min, maxDistance: view.max,
    maxPolar: Math.PI * 0.78, minPolar: Math.PI * 0.08,
  });
  resetCameraView(camera, controls, view);
  controls.setAutoRotate(quality.tier === 'high' ? 0.012 : 0);
  basicLights(scene, { ambient: config.subject === 'chemistry' ? 0.62 : 0.56, key: 1.45, fill: 0.55, keyPos: [5, 10, 7] });

  const state = initState(config);
  let currentLab = null;
  let needsRefresh = true;
  let readouts = [];
  const hud = createHud(stage);
  const status = hud.badge('3D calibrated · real formula active', config.accent || subject.color);
  const perf = hud.badge(`${quality.tier} quality · DPR ${quality.pixelRatio}`, '#60a5fa');

  const panel = createPanel(stage, { title: config.title, compact: true });
  panel.info(config.subtitle || 'Interactive 3D virtual practical with live readings.');
  const controlHandles = new Map();
  config.controls.forEach((control) => {
    if (control.type === 'select') {
      const handle = panel.select({
        label: control.label,
        value: control.value,
        options: control.options.map((o) => ({ value: o[0], label: o[1] })),
        onChange: (v) => { state[control.id] = v; requestRefresh(); updateReadouts(); },
      });
      controlHandles.set(control.id, handle);
    } else {
      const handle = panel.slider({
        label: control.label,
        min: control.min,
        max: control.max,
        step: control.step || 1,
        value: control.value,
        format: (v) => fmtControl(control, v),
        onChange: (v) => { state[control.id] = v; requestRefresh(); updateReadouts(); },
      });
      controlHandles.set(control.id, handle);
    }
  });
  panel.buttonRow([
    { label: 'Trial', icon: 'science', onClick: () => randomizeTrial(config, state, controlHandles, requestRefresh, updateReadouts) },
    { label: 'View', icon: 'center_focus_strong', variant: 'ghost', onClick: () => { resetCameraView(camera, controls, view); status.set('view reset · instrument fitted to screen'); } },
    { label: 'Steps', icon: 'menu_book', variant: 'ghost', onClick: () => showInfoCard(stage, { title: config.title, body: `${currentProcedureText(config, state)}\n\n${config.explain}`, color: config.accent || subject.color }) },
  ]);
  const stepReadout = panel.readout({ label: 'Practical step', value: currentProcedureText(config, state) });
  const dataTable = addObservationTable(panel, config, state);
  dataTable.render();
  panel.buttonRow([
    { label: 'Next', icon: 'skip_next', variant: 'ghost', onClick: () => { const steps = procedureSteps(config); state.stepIndex = (state.stepIndex + 1) % steps.length; updateReadouts(); } },
    { label: 'Record', icon: 'edit_note', onClick: () => { recordObservation(config, state); dataTable.render(true); status.set('reading recorded · observation book updated'); } },
    { label: 'Clear', icon: 'restart_alt', variant: 'ghost', onClick: () => { state.observations = []; dataTable.render(true); status.set('records cleared · live readings active'); } },
  ]);
  panel.toggle({ label: 'Animate apparatus', value: true, onChange: (v) => { state.running = v; status.set(v ? 'animation on · readings live' : 'animation paused · readings live'); } });
  panel.divider();
  panel.section('Live calibrated readouts');
  (config.metrics(state) || []).forEach(([label, value]) => readouts.push(panel.readout({ label, value })));

  function requestRefresh() { needsRefresh = true; }

  function updateReadouts() {
    stepReadout.set(currentProcedureText(config, state));
    const values = config.metrics(state) || [];
    values.forEach(([label, value], i) => {
      if (!readouts[i]) readouts[i] = panel.readout({ label, value });
      else readouts[i].set(value);
    });
    dataTable.render();
  }

  function refreshLab() {
    if (currentLab) {
      scene.remove(currentLab.group);
      disposeObject(currentLab.group);
      currentLab = null;
    }
    currentLab = buildLabScene(config, state, quality);
    scene.add(currentLab.group);
    needsRefresh = false;
  }

  engine.setUpdate((dt, t) => {
    controls.update(dt);
    if (needsRefresh) refreshLab();
    if (currentLab && currentLab.update && state.running) currentLab.update(dt, t, state);
    updateReadouts();
  });
  engine.start();

  return {
    dispose() {
      if (currentLab) disposeObject(currentLab.group);
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}

function randomizeTrial(config, state, handles, requestRefresh, updateReadouts) {
  config.controls.forEach((control) => {
    if (control.randomize && control.type !== 'select') {
      const v = randomValue(control);
      state[control.id] = v;
      const handle = handles.get(control.id);
      if (handle && handle.set) handle.set(v);
    }
  });
  state.sample = Math.random();
  state.observations = [];
  state.stepIndex = 0;
  requestRefresh();
  updateReadouts();
}

function buildLabScene(config, state, quality) {
  const group = new THREE.Group();
  const actors = {};
  addRoom(group, config);
  addTitle(group, config);
  switch (config.kind) {
    case 'caliper': buildPrecisionCaliper(group, state, config); break;
    case 'micrometer': buildPrecisionMicrometer(group, state, config); break;
    case 'spherometer': buildPrecisionSpherometer(group, state, config); break;
    case 'pendulum': buildPendulum(group, actors, state, config); break;
    case 'forceboard': buildForceBoard(group, state, config); break;
    case 'incline': buildIncline(group, actors, state, config); break;
    case 'spring': buildSpring(group, actors, state, config); break;
    case 'calorimeter': buildCalorimeter(group, actors, state, config); break;
    case 'resonance': buildResonance(group, actors, state, config); break;
    case 'sonometer': buildSonometer(group, actors, state, config); break;
    case 'circuit': buildCircuit(group, actors, state, config); break;
    case 'meterbridge': buildMeterBridge(group, state, config); break;
    case 'potentiometer': buildPotentiometer(group, state, config); break;
    case 'galvanometer': buildGalvanometer(group, actors, state, config); break;
    case 'optics': buildOptics(group, state, config); break;
    case 'prism': buildPrism(group, state, config); break;
    case 'apparatus': buildApparatus(group, state, config); break;
    case 'separation': buildSeparation(group, actors, state, config); break;
    case 'titration': buildTitration(group, actors, state, config); break;
    case 'flame': buildFlame(group, actors, state, config); break;
    case 'testtubes': buildTestTubes(group, actors, state, config); break;
    case 'gasprep': buildGasPrep(group, actors, state, config); break;
    case 'crystallization': buildCrystallization(group, actors, state, config); break;
    case 'saltanalysis': buildSaltAnalysis(group, actors, state, config); break;
    case 'electrolysis': buildElectrolysis(group, actors, state, config); break;
    case 'ph': buildPH(group, actors, state, config); break;
    case 'functional': buildFunctional(group, actors, state, config); break;
    case 'thermochemistry': buildThermo(group, actors, state, config); break;
    case 'lassaigne': buildLassaigne(group, actors, state, config); break;
    default: buildApparatus(group, state, config);
  }
  return { group, update: (dt, t) => updateActors(actors, dt, t, state, config) };
}

function mat(color, opts = {}) {
  return new THREE.MeshStandardMaterial({
    color, roughness: opts.roughness ?? 0.48, metalness: opts.metalness ?? 0.05,
    transparent: opts.opacity !== undefined && opts.opacity < 1, opacity: opts.opacity ?? 1,
    emissive: opts.emissive || 0x000000, emissiveIntensity: opts.emissiveIntensity || 0,
    side: opts.side || THREE.FrontSide,
  });
}
function glass(color = 0xbed7ff, opacity = 0.32) { return mat(color, { opacity, roughness: 0.05, metalness: 0, side: THREE.DoubleSide }); }
function metal(color = 0xa7b0bf) { return mat(color, { metalness: 0.75, roughness: 0.28 }); }
function wood(color = 0x8a5a34) { return mat(color, { roughness: 0.7 }); }
function rubber(color = 0x111827) { return mat(color, { roughness: 0.85 }); }
function makeBox(w, h, d, material, pos = [0, 0, 0]) { const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material); mesh.position.set(...pos); mesh.castShadow = true; mesh.receiveShadow = true; return mesh; }
function makeCylinder(r1, r2, h, material, pos = [0, 0, 0], seg = 48) { const mesh = new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), material); mesh.position.set(...pos); mesh.castShadow = true; mesh.receiveShadow = true; return mesh; }
function makeSphere(r, material, pos = [0, 0, 0], seg = 48) { const mesh = new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(12, Math.round(seg / 2))), material); mesh.position.set(...pos); mesh.castShadow = true; mesh.receiveShadow = true; return mesh; }
function makeLine(points, color = 0xffffff, opacity = 1) { const geo = new THREE.BufferGeometry().setFromPoints(points); const material = new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity }); return new THREE.Line(geo, material); }
function addLabel(group, text, pos, opts = {}) {
  const sprite = makeLabelSprite(text, {
    fontSize: opts.fontSize || 28,
    scale: opts.scale || 0.22,
    bg: opts.bg ?? true,
    color: opts.color || '#f8fafc',
    bgColor: opts.bgColor || 'rgba(2,6,23,.72)',
  });
  sprite.position.set(...pos);
  sprite.renderOrder = 10;
  group.add(sprite);
  return sprite;
}
function addTitle(group, config) {
  addLabel(group, config.title, [0, 4.35, -3.45], { scale: 0.30, fontSize: 34, bgColor: 'rgba(2,6,23,.55)' });
  addLabel(group, config.subtitle || 'Live 3D practical', [0, 3.93, -3.45], { scale: 0.18, fontSize: 27, color: '#dbeafe', bgColor: 'rgba(2,6,23,.42)' });
}
function addRoom(group, config) {
  const subject = config.subject;
  const floor = makeBox(15, 0.08, 10, mat(subject === 'chemistry' ? 0x0f2e2a : 0x172033, { roughness: 0.94 }), [0, -0.08, 0]);
  floor.receiveShadow = true; group.add(floor);
  const bench = makeBox(12.6, 0.34, 5.9, wood(subject === 'chemistry' ? 0x6b4426 : 0x6f4e37), [0, 0.15, 0]);
  const top = makeBox(12.8, 0.10, 6.1, mat(0x263548, { roughness: 0.74 }), [0, 0.40, 0]);
  group.add(bench, top);
  addBenchDetails(group, subject);
  const grid = new THREE.GridHelper(13.5, 27, subject === 'chemistry' ? 0x0f766e : 0x64748b, 0x1f2937);
  grid.position.y = 0.465;
  (Array.isArray(grid.material) ? grid.material : [grid.material]).forEach((m) => { m.opacity = 0.16; m.transparent = true; });
  group.add(grid);
  const back = makeBox(15, 5.7, 0.08, mat(subject === 'chemistry' ? 0x052e2b : 0x0b1020, { roughness: 0.86 }), [0, 2.78, -4.25]);
  back.receiveShadow = true; group.add(back);
  const notice = makeBox(3.7, 1.1, 0.04, mat(subject === 'chemistry' ? 0x064e3b : 0x1e293b, { roughness: 0.65, opacity: 0.68 }), [-4.1, 3.0, -4.18]);
  group.add(notice);
  addLabel(group, subject === 'chemistry' ? 'Safety: goggles · small quantities · clean glassware' : 'Measurement: avoid parallax · repeat · average', [-4.1, 3.04, -4.12], { scale: 0.16, fontSize: 24, bg: false, color: '#e2e8f0' });
}
function addRuler(group, length = 8, pos = [0, 0, 0], labelEvery = 1) {
  const ruler = new THREE.Group();
  ruler.position.set(...pos);
  const base = makeBox(length + 0.15, 0.06, 0.54, metal(0xdbe3ec), [0, 0, 0]);
  ruler.add(base);
  const scale = makeScalePlane(length, 0.42, { length: length * 10, major: 10, minor: 1, label: 'cm', dark: false });
  scale.rotation.x = -Math.PI / 2;
  scale.position.set(0, 0.04, 0.02);
  ruler.add(scale);
  for (let i = 0; i <= length * 10; i++) {
    const x = -length / 2 + (i / 10);
    const h = i % 10 === 0 ? 0.26 : i % 5 === 0 ? 0.20 : 0.12;
    const tick = makeBox(0.009, 0.045, h, mat(0x020617), [x, 0.065, -0.18 + h / 2]);
    ruler.add(tick);
  }
  group.add(ruler);
  return ruler;
}

function buildCaliper(group, s) {
  const y = 0.86;
  const body = new THREE.Group();
  body.rotation.y = -0.02;

  const observed = Math.max(0.2, Math.min(8.2, s.sizeCm + s.zeroErrorCm));
  const fixedX = -4.15;
  const trueGap = Math.max(0.2, Math.min(8.2, s.sizeCm));
  const sliderX = fixedX + trueGap;
  const objectCenterX = fixedX + trueGap / 2;
  const specimenHeight = Math.max(0.58, Math.min(1.95, trueGap * 0.46));
  const jawFaceY = y + 1.48;
  const jawMat = metal(0xe9eef5);
  const darkEtch = mat(0x020617, { roughness: 0.65 });
  const blueEtch = mat(0x38bdf8, { opacity: 0.78, emissive: 0x38bdf8, emissiveIntensity: 0.18 });

  const beam = addRuler(body, 8.8, [0, y, 0], 1);
  beam.scale.z = 0.78;
  body.add(makeBox(8.75, 0.07, 0.08, metal(0xb8c2cc), [0, y + 0.17, -0.31]));
  body.add(makeBox(8.75, 0.05, 0.05, metal(0x94a3b8), [0, y - 0.14, 0.30]));

  function makeExternalJaw(x, dir, label) {
    const jaw = new THREE.Group();
    jaw.add(makeBox(0.22, 2.22, 0.26, jawMat, [x, y + 0.92, -0.03]));
    jaw.add(makeBox(0.76, 0.22, 0.24, jawMat, [x + dir * 0.27, jawFaceY + 0.80, -0.03]));
    jaw.add(makeBox(0.60, 0.16, 0.24, jawMat, [x + dir * 0.22, jawFaceY + 0.56, -0.03]));
    jaw.add(makeBox(0.82, 0.20, 0.28, jawMat, [x + dir * 0.30, jawFaceY - 0.88, -0.03]));
    jaw.add(makeBox(0.54, 0.16, 0.28, jawMat, [x + dir * 0.22, jawFaceY - 1.12, -0.03]));
    jaw.add(makeBox(0.025, 2.0, 0.035, darkEtch, [x + dir * 0.13, jawFaceY - 0.20, 0.16]));
    addLabel(jaw, label, [x + dir * 0.34, y + 2.52, -0.33], { scale: 0.105, fontSize: 20 });
    return jaw;
  }

  const fixedJaw = makeExternalJaw(fixedX, 1, 'fixed jaw');
  body.add(fixedJaw);

  const slider = new THREE.Group();
  slider.position.x = sliderX;
  slider.add(makeBox(1.28, 0.50, 0.46, metal(0xb9c4cf), [0.48, y + 0.02, 0.00]));
  slider.add(makeBox(0.42, 0.72, 0.48, metal(0xaab6c3), [-0.04, y + 0.20, 0.00]));
  slider.add(makeExternalJaw(0, -1, 'vernier jaw'));
  const vernierScale = makeScalePlane(1.18, 0.24, { length: 10, major: 1, minor: 1, label: '0.01 cm', width: 640, height: 112, dark: true });
  vernierScale.rotation.x = -Math.PI / 2;
  vernierScale.position.set(0.50, y + 0.36, 0.265);
  slider.add(vernierScale);
  const lock = makeCylinder(0.12, 0.12, 0.18, metal(0x64748b), [0.16, y + 0.72, 0.27], 32);
  lock.rotation.x = Math.PI / 2;
  slider.add(lock);
  slider.add(makeBox(0.10, 0.70, 0.055, blueEtch, [0.00, y + 0.35, 0.31]));
  body.add(slider);

  const specimen = makeSphere(0.5, metal(0x111827), [objectCenterX, jawFaceY - 0.12, 0.47], 72);
  specimen.scale.set(Math.max(0.32, trueGap / 1.0), specimenHeight, 0.62);
  body.add(specimen);
  body.add(makeLine([new THREE.Vector3(fixedX, jawFaceY - 0.12, 0.88), new THREE.Vector3(fixedX + trueGap, jawFaceY - 0.12, 0.88)], 0x38bdf8, 0.82));
  body.add(makeBox(0.025, specimenHeight * 2.05, 0.035, blueEtch, [fixedX, jawFaceY - 0.12, 0.88]));
  body.add(makeBox(0.025, specimenHeight * 2.05, 0.035, blueEtch, [fixedX + trueGap, jawFaceY - 0.12, 0.88]));

  const mainReading = Math.floor(observed * 10) / 10;
  const vernier = Math.max(0, Math.min(9, Math.round((observed - mainReading) / 0.01)));
  addLabel(body, `${s.sizeCm.toFixed(2)} cm corrected`, [objectCenterX, jawFaceY + specimenHeight + 0.58, 0.78], { scale: 0.18, fontSize: 26, bgColor: 'rgba(0,0,0,.66)' });
  addLabel(body, `MSR ${mainReading.toFixed(1)} cm + VSD ${vernier} × 0.01`, [0.20, y + 1.02, 0.54], { scale: 0.145, fontSize: 22, color: '#dbeafe', bgColor: 'rgba(15,23,42,.62)' });
  addLabel(body, 'zero check', [fixedX + 0.36, y + 0.54, 0.44], { scale: 0.105, fontSize: 20, color: '#fef3c7' });

  const depthRod = makeBox(0.06, 0.04, 2.6, metal(0xdbe3ec), [fixedX + observed + 0.88, y - 0.08, -1.42]);
  depthRod.rotation.y = Math.PI / 2;
  body.add(depthRod);
  group.add(body);
}
function buildMicrometer(group, s) {
  const baseY = 1.0;
  const frame = new THREE.TorusGeometry(1.55, 0.09, 18, 80, Math.PI * 1.45);
  const mesh = new THREE.Mesh(frame, metal(0xcbd5e1)); mesh.rotation.z = Math.PI * 0.75; mesh.position.set(-1.2, baseY + 0.2, 0); group.add(mesh);
  group.add(makeCylinder(0.18, 0.18, 2.2, metal(0xe5e7eb), [0.5, baseY + 0.2, 0])); group.children[group.children.length - 1].rotation.z = Math.PI / 2;
  const thimble = makeCylinder(0.55, 0.55, 1.1, metal(0x94a3b8), [1.85, baseY + 0.2, 0]); thimble.rotation.z = Math.PI / 2; group.add(thimble);
  const wire = makeCylinder(Math.max(0.03, s.diameterMm / 20), Math.max(0.03, s.diameterMm / 20), 1.1, metal(0x334155), [-0.2, baseY + 0.2, 0]); wire.rotation.x = Math.PI / 2; group.add(wire);
  addLabel(group, `LC 0.01 mm · reading ${(s.diameterMm + s.zeroErrorMm).toFixed(2)} mm`, [0, 2.55, 0], { scale: 0.25 });
  addLabel(group, 'ratchet thimble', [2.15, 1.9, 0], { scale: 0.2 });
}
function buildSpherometer(group, s) {
  const baseY = 0.65;
  const plate = makeCylinder(2.4, 2.4, 0.08, glass(0x93c5fd, 0.24), [0, baseY, 0], 72); plate.scale.y = 0.15; group.add(plate);
  const legR = s.legCm / 6;
  const legPts = [[0, 0, legR], [-legR * 0.866, 0, -legR / 2], [legR * 0.866, 0, -legR / 2]];
  legPts.forEach((p, i) => { const leg = makeCylinder(0.045, 0.045, 1.05, metal(0xcbd5e1), [p[0], baseY + 0.55, p[2]]); group.add(leg); group.add(makeSphere(0.1, metal(0xe2e8f0), [p[0], baseY + 0.02, p[2]])); addLabel(group, `leg ${i + 1}`, [p[0], baseY + 1.25, p[2]], { scale: 0.13, bg: false }); });
  group.add(makeCylinder(0.08, 0.08, 1.35, metal(0xe5e7eb), [0, baseY + 0.75, 0]));
  const dial = makeCylinder(0.62, 0.62, 0.05, metal(0x94a3b8), [0, baseY + 1.45, 0]); group.add(dial);
  addLabel(group, `h = ${s.sagittaMm.toFixed(2)} mm`, [0, 2.7, 0], { scale: 0.24 });
}
function buildPendulum(group, actors, s) {
  group.add(makeBox(0.12, 3.2, 0.12, metal(0x94a3b8), [-2.2, 2.0, 0]));
  group.add(makeBox(3.2, 0.12, 0.12, metal(0x94a3b8), [-0.65, 3.55, 0]));
  const L = s.lengthCm / 55;
  const pivot = new THREE.Vector3(-0.2, 3.5, 0);
  const bob = makeSphere(0.23, metal(0xd97706), [pivot.x, pivot.y - L, 0]);
  const string = makeLine([pivot, bob.position.clone()], 0xe5e7eb, 0.9);
  group.add(string, bob);
  actors.pendulum = { pivot, bob, string, L, amp: THREE.MathUtils.degToRad(s.amplitude) };
  addLabel(group, `L = ${s.lengthCm.toFixed(0)} cm`, [1.65, 2.7, 0], { scale: 0.22 });
  addLabel(group, 'photogate / stopwatch', [-2.2, 0.85, 0.8], { scale: 0.18 });
}
function buildForceBoard(group, s) {
  group.add(makeBox(5.6, 3.2, 0.12, mat(0xf5deb3, { roughness: 0.8 }), [0, 2.0, -0.25]));
  const center = new THREE.Vector3(0, 2, -0.15);
  const p = new THREE.Vector3(s.pN * 0.32, 0, 0);
  const a = THREE.MathUtils.degToRad(s.angleDeg);
  const q = new THREE.Vector3(Math.cos(a) * s.qN * 0.32, Math.sin(a) * s.qN * 0.32, 0);
  addArrow(group, center, center.clone().add(p), 0x3b82f6, 'P');
  addArrow(group, center, center.clone().add(q), 0x10b981, 'Q');
  addArrow(group, center, center.clone().add(p).add(q), 0xf59e0b, 'R');
  group.add(makeSphere(0.11, metal(0xe5e7eb), center.toArray()));
  addLabel(group, 'Gravesand board: resultant is diagonal', [0, 3.85, 0], { scale: 0.24 });
}
function addArrow(group, from, to, color, label) {
  const dir = new THREE.Vector3().subVectors(to, from); const len = dir.length(); dir.normalize();
  const arrow = new THREE.ArrowHelper(dir, from, len, color, 0.2, 0.12); group.add(arrow);
  addLabel(group, label, to.toArray(), { scale: 0.16, bg: true });
}
function buildIncline(group, actors, s) {
  const angle = THREE.MathUtils.degToRad(s.angleDeg);
  const ramp = makeBox(4.6, 0.14, 1.9, mat(0x855a35), [0, 1.0, 0]); ramp.rotation.z = angle; group.add(ramp);
  const x = Math.min(1.2, Math.max(-1.2, Math.tan(angle) - s.muStatic)) * 0.6;
  const block = makeBox(0.72, 0.5, 0.72, mat(0xd97706), [x, 1.38 + x * Math.tan(angle), 0]); block.rotation.z = angle; group.add(block); actors.slidingBlock = { block, angle, sliding: Math.tan(angle) >= s.muStatic };
  addLabel(group, `θ = ${s.angleDeg.toFixed(1)}° · μ = tanθ at repose`, [0, 3.25, 0], { scale: 0.24 });
}
function buildSpring(group, actors, s) {
  group.add(makeBox(0.14, 3.0, 0.14, metal(0x94a3b8), [-1.8, 2.0, 0]));
  group.add(makeBox(2.4, 0.13, 0.13, metal(0x94a3b8), [-0.65, 3.42, 0]));
  const F = s.loadG / 1000 * 9.81; const x = F / s.kNm;
  const top = new THREE.Vector3(0, 3.35, 0); const bottom = new THREE.Vector3(0, 2.45 - x * 2.2, 0);
  const spring = makeSpringMesh(top, bottom, 0.18, 12, metal(0xcbd5e1)); group.add(spring);
  const mass = makeBox(0.7, 0.5, 0.7, mat(0xd97706), [0, bottom.y - 0.35, 0]); group.add(mass); actors.mass = mass;
  addRuler(group, 2.6, [1.15, 2.1, 0], 1); group.children[group.children.length - 1].rotation.z = Math.PI / 2;
  addLabel(group, `extension ${(x * 100).toFixed(1)} cm`, [1.8, 2.55, 0], { scale: 0.22 });
}
function makeSpringMesh(top, bottom, radius, coils, material) {
  const points = []; const height = top.y - bottom.y;
  for (let i = 0; i <= coils * 24; i++) { const t = i / (coils * 24); const a = t * coils * Math.PI * 2; points.push(new THREE.Vector3(Math.cos(a) * radius, top.y - height * t, Math.sin(a) * radius)); }
  const curve = new THREE.CatmullRomCurve3(points); return new THREE.Mesh(new THREE.TubeGeometry(curve, coils * 24, 0.025, 8, false), material);
}
function buildCalorimeter(group, actors, s) {
  const cup = makeBeaker(1.1, 1.4, 0.55, 0x60a5fa, 'water'); cup.position.set(0, 1.15, 0); group.add(cup);
  const metalObj = makeSphere(0.28, metal(0xb45309), [-0.35, 1.9, 0]); group.add(metalObj);
  const therm = makeThermometer(2.2, s.waterTemp); therm.position.set(0.75, 1.55, 0); therm.rotation.z = -0.14; group.add(therm);
  actors.thermometer = therm; addLabel(group, 'insulated calorimeter + thermometer', [0, 3.3, 0], { scale: 0.24 });
}
function buildResonance(group, actors, s) {
  const tube = makeCylinder(0.35, 0.35, 3.4, glass(0x93c5fd, 0.28), [0, 2.05, 0], 48); group.add(tube);
  const waterH = 3.4 - s.lengthCm / 10;
  const water = makeCylinder(0.32, 0.32, Math.max(0.05, waterH), mat(0x38bdf8, { opacity: 0.45 }), [0, 0.35 + waterH / 2, 0], 48); group.add(water);
  const fork = makeTuningFork(); fork.position.set(-1.25, 3.95, 0); group.add(fork); actors.fork = fork;
  addLabel(group, `air column ${s.lengthCm.toFixed(1)} cm`, [1.35, 2.7, 0], { scale: 0.22 });
}
function makeTuningFork() { const g = new THREE.Group(); g.add(makeCylinder(0.04, 0.04, 0.8, metal(0xcbd5e1), [0, -0.35, 0])); const p1 = makeCylinder(0.04, 0.04, 1.05, metal(0xcbd5e1), [-0.18, 0.45, 0]); const p2 = makeCylinder(0.04, 0.04, 1.05, metal(0xcbd5e1), [0.18, 0.45, 0]); g.add(p1, p2); return g; }
function buildSonometer(group, actors, s) {
  group.add(makeBox(5.6, 0.55, 1.0, wood(0x8b5a2b), [0, 0.9, 0]));
  const L = s.lengthCm / 20; const x1 = -L / 2; const x2 = L / 2;
  group.add(makeLine([new THREE.Vector3(-2.7, 1.28, 0), new THREE.Vector3(2.7, 1.28, 0)], 0xe5e7eb, 1));
  group.add(makeBox(0.12, 0.55, 0.85, metal(0xcbd5e1), [x1, 1.16, 0])); group.add(makeBox(0.12, 0.55, 0.85, metal(0xcbd5e1), [x2, 1.16, 0]));
  actors.stringWave = { length: L, y: 1.28, material: null };
  addLabel(group, `vibrating length ${s.lengthCm.toFixed(0)} cm`, [0, 2.0, 0], { scale: 0.23 });
  group.add(makeCylinder(0.26, 0.26, 0.5, metal(0xd97706), [3.05, 0.4, 0]));
}
function buildCircuit(group, actors, s) {
  group.add(makeBox(5.6, 0.08, 3.4, mat(0x1e293b), [0, 0.75, 0]));
  addMeter(group, [-1.7, 1.03, -0.7], 'A', s.voltage / s.resistance, 1.5, actors, 'ammeter');
  addMeter(group, [1.7, 1.03, -0.7], 'V', s.voltage, 10, actors, 'voltmeter');
  group.add(makeBox(1.2, 0.2, 0.26, mat(0xfbbf24), [0, 1.05, 0.8])); addLabel(group, `${s.resistance.toFixed(1)} Ω`, [0, 1.55, 0.8], { scale: 0.19 });
  addWireLoop(group, 0x60a5fa);
}
function addMeter(group, pos, label, value, max, actors, key) {
  const g = new THREE.Group();
  g.position.set(...pos);
  const gauge = makeNeedleGauge(label, value, max, label === 'A' ? 0xef4444 : 0x2563eb);
  g.add(gauge.group);
  const body = makeBox(1.25, 0.34, 0.55, mat(0x111827, { roughness: 0.55 }), [0, -0.18, -0.04]);
  g.add(body);
  group.add(g);
  actors[key] = { needle: gauge.needle, value, max };
}
function addWireLoop(group, color) {
  const pts = [[-2.5, 1.04, -1.3], [-2.5, 1.04, 1.3], [2.5, 1.04, 1.3], [2.5, 1.04, -1.3], [-2.5, 1.04, -1.3]].map((p) => new THREE.Vector3(...p));
  group.add(makeLine(pts, color, 0.95));
  pts.forEach((p) => group.add(makeSphere(0.055, mat(color, { emissive: color, emissiveIntensity: 0.1 }), p.toArray(), 12)));
}
function buildMeterBridge(group, s) {
  group.add(makeBox(10.6, 0.18, 1.45, wood(0x8b5a2b), [0, 0.78, 0]));
  addRuler(group, 10, [0, 1.02, 0], 1);
  const x = -5 + s.balanceCm / 10;
  group.add(makeBox(0.09, 0.13, 1.52, metal(0xb45309), [-2.75, 1.18, 0]));
  group.add(makeBox(0.09, 0.13, 1.52, metal(0xb45309), [2.75, 1.18, 0]));
  group.add(makeSphere(0.11, mat(0xef4444, { emissive: 0xef4444, emissiveIntensity: 0.12 }), [x, 1.34, 0]));
  addLabel(group, `null point ${s.balanceCm.toFixed(1)} cm`, [x, 1.82, 0], { scale: 0.16 });
  addWireLoop(group, 0x22d3ee);
}
function buildPotentiometer(group, s) {
  group.add(makeBox(10.6, 0.18, 1.45, wood(0x8b5a2b), [0, 0.78, 0]));
  addRuler(group, 10, [0, 1.02, 0], 1);
  const x1 = -5 + s.l1 / 10, x2 = -5 + s.l2 / 10;
  group.add(makeSphere(0.09, mat(0x60a5fa, { emissive: 0x60a5fa, emissiveIntensity: 0.16 }), [x1, 1.32, 0.32]));
  group.add(makeSphere(0.09, mat(0xf59e0b, { emissive: 0xf59e0b, emissiveIntensity: 0.16 }), [x2, 1.32, -0.32]));
  addLabel(group, `standard l₁ ${s.l1.toFixed(1)} cm`, [x1, 1.82, 0.45], { scale: 0.14 });
  addLabel(group, `unknown l₂ ${s.l2.toFixed(1)} cm`, [x2, 1.82, -0.45], { scale: 0.14 });
  addWireLoop(group, 0x22d3ee);
}
function buildGalvanometer(group, actors, s) {
  group.add(makeBox(2.8, 0.16, 1.75, mat(0x1e293b), [0, 0.80, 0]));
  addMeter(group, [0, 1.55, 0], 'G', s.deflection, 35, actors, 'galvanometer');
  addLabel(group, `${s.currentUa.toFixed(0)} µA gives ${s.deflection.toFixed(0)} divisions`, [0, 2.55, 0], { scale: 0.18 });
  addWireLoop(group, 0xf59e0b);
}
function buildOptics(group, s) { addRuler(group, 9, [0, 0.95, 0], 1); const lens = makeCylinder(0.7, 0.7, 0.08, glass(0x93c5fd, 0.45), [0, 1.75, 0], 64); lens.rotation.x = Math.PI / 2; lens.scale.x = 0.38; group.add(lens); const u = -s.objectCm / 14; const v = Math.min(4.2, Math.max(0.6, (1 / (1 / s.focalCm - 1 / s.objectCm)) / 14)); group.add(makeBox(0.08, 0.8, 0.08, mat(0xf97316), [u, 1.42, 0])); group.add(makeBox(0.12, 1.2, 1.0, mat(0xe2e8f0), [v, 1.55, 0])); addOpticRay(group, u, v); addLabel(group, `screen at v ≈ ${(v * 14).toFixed(1)} cm`, [v, 2.45, 0], { scale: 0.18 }); }
function addOpticRay(group, u, v) { group.add(makeLine([new THREE.Vector3(u, 1.8, 0.03), new THREE.Vector3(0, 1.8, 0.03), new THREE.Vector3(v, 1.25, 0.03)], 0xfacc15, 0.9)); group.add(makeLine([new THREE.Vector3(u, 1.8, -0.03), new THREE.Vector3(0, 1.45, -0.03), new THREE.Vector3(v, 1.25, -0.03)], 0xfacc15, 0.9)); }
function buildPrism(group, s) { const shape = new THREE.Shape(); shape.moveTo(0, 0.85); shape.lineTo(-0.8, -0.55); shape.lineTo(0.8, -0.55); shape.lineTo(0, 0.85); const geo = new THREE.ExtrudeGeometry(shape, { depth: 0.9, bevelEnabled: false }); const prism = new THREE.Mesh(geo, glass(0x93c5fd, 0.42)); prism.position.set(0, 1.7, -0.45); group.add(prism); group.add(makeLine([new THREE.Vector3(-3.5, 1.65, 0), new THREE.Vector3(-0.5, 1.65, 0), new THREE.Vector3(0.6, 1.28, 0), new THREE.Vector3(3.2, 1.05, 0)], 0xfacc15, 1)); addLabel(group, `A=${s.angleA.toFixed(1)}°  D=${s.devD.toFixed(1)}°`, [0, 3.05, 0], { scale: 0.24 }); }

function makeGraduationMarks(group, radius, height, sideX = 1) {
  for (let i = 1; i <= 5; i++) {
    const y = (height * i) / 6;
    const tick = makeBox(0.18, 0.006, 0.012, mat(0xe2e8f0, { opacity: 0.55 }), [sideX * radius * 0.86, y, radius * 0.26]);
    group.add(tick);
  }
}
function makeBeaker(radius, height, fill, color, label) {
  const g = new THREE.Group();
  const wall = makeCylinder(radius, radius * 0.93, height, glass(0xc7ddff, 0.25), [0, height / 2, 0], 64);
  g.add(wall);
  const lip = makeCylinder(radius * 1.02, radius * 1.02, 0.035, glass(0xe0f2fe, 0.34), [0, height + 0.02, 0], 64);
  g.add(lip);
  if (fill > 0) {
    const liquid = makeCylinder(radius * 0.9, radius * 0.84, height * fill, mat(color, { opacity: 0.60, roughness: 0.08 }), [0, height * fill / 2 + 0.03, 0], 64);
    g.add(liquid);
    const surface = makeCylinder(radius * 0.9, radius * 0.9, 0.018, mat(color, { opacity: 0.72, roughness: 0.02 }), [0, height * fill + 0.05, 0], 64);
    g.add(surface);
  }
  makeGraduationMarks(g, radius, height);
  if (label) addLabel(g, label, [0, height + 0.30, 0], { scale: 0.13, fontSize: 22 });
  return g;
}
function makeFlask(label, fillColor = 0x93c5fd, fill = 0.45) {
  const g = new THREE.Group();
  const neck = makeCylinder(0.21, 0.21, 1.08, glass(0xc7ddff, 0.27), [0, 1.18, 0], 48);
  const mouth = makeCylinder(0.28, 0.28, 0.045, glass(0xe0f2fe, 0.36), [0, 1.74, 0], 48);
  const bulb = makeSphere(0.72, glass(0xc7ddff, 0.24), [0, 0.62, 0], 64);
  bulb.scale.y = 0.92;
  g.add(neck, mouth, bulb);
  const liq = makeSphere(0.64, mat(fillColor, { opacity: 0.58, roughness: 0.08 }), [0, 0.44, 0], 64);
  liq.scale.y = Math.max(0.08, fill * 0.82);
  g.add(liq);
  const surface = makeCylinder(0.48, 0.48, 0.018, mat(fillColor, { opacity: 0.70 }), [0, 0.55 + fill * 0.18, 0], 48);
  g.add(surface);
  if (label) addLabel(g, label, [0, 2.00, 0], { scale: 0.13, fontSize: 22 });
  return g;
}
function makeThermometer(height, temp) {
  const g = new THREE.Group();
  g.add(makeCylinder(0.045, 0.045, height, glass(0xf8fafc, 0.40), [0, height / 2, 0], 16));
  const redH = Math.max(0.18, Math.min(height * 0.9, height * (temp / 110)));
  g.add(makeCylinder(0.025, 0.025, redH, mat(0xef4444, { emissive: 0xef4444, emissiveIntensity: 0.05 }), [0, redH / 2, 0], 12));
  g.add(makeSphere(0.11, mat(0xef4444), [0, 0, 0], 18));
  for (let i = 1; i <= 5; i++) g.add(makeBox(0.12, 0.006, 0.006, mat(0x111827), [0.075, i * height / 6, 0.02]));
  return g;
}
function buildApparatus(group, s) {
  const flask = makeFlask('conical flask', 0x93c5fd, 0.35); flask.position.set(-1.2, 0.55, 0); group.add(flask);
  const beaker = makeBeaker(0.55, 1.1, 0.45, 0x60a5fa, 'beaker'); beaker.position.set(1.1, 0.55, 0); group.add(beaker);
  makeBuretteStand(group, 0, 0.7, 0xbae6fd, '50 mL burette');
  buildBurner(group, {}, 0, [-2.6, 0.55, 0]);
  addLabel(group, `focus: ${s.focus}`, [0, 3.25, 0], { scale: 0.18 });
}
function makeBuretteStand(group, x, y, color = 0xbae6fd, label = 'burette') {
  group.add(makeBox(0.10, 2.9, 0.10, metal(0x94a3b8), [x - 0.72, y + 1.15, 0]));
  group.add(makeBox(1.0, 0.07, 0.07, metal(0x94a3b8), [x - 0.28, y + 2.28, 0]));
  group.add(makeBox(0.42, 0.10, 0.10, rubber(0x111827), [x - 0.18, y + 1.45, 0]));
  const tube = makeCylinder(0.075, 0.075, 2.38, glass(0xc7ddff, 0.31), [x, y + 1.32, 0], 32);
  group.add(tube);
  const liqH = 1.85;
  const liq = makeCylinder(0.054, 0.054, liqH, mat(color, { opacity: 0.66, roughness: 0.05 }), [x, y + 1.43, 0], 32);
  group.add(liq);
  for (let i = 0; i <= 10; i++) {
    const tick = makeBox(i % 5 === 0 ? 0.20 : 0.12, 0.006, 0.006, mat(0xe2e8f0, { opacity: 0.72 }), [x + 0.085, y + 0.25 + i * 0.21, 0.08]);
    group.add(tick);
  }
  const tap = makeBox(0.36, 0.06, 0.06, metal(0xe5e7eb), [x, y + 0.18, 0]);
  group.add(tap);
  const tip = makeCylinder(0.025, 0.008, 0.32, glass(0xc7ddff, 0.34), [x, y - 0.05, 0], 24);
  group.add(tip);
  addLabel(group, label, [x + 0.52, y + 2.63, 0], { scale: 0.13, fontSize: 22 });
}
function buildSeparation(group, actors, s) { if (s.method === 'distillation') { const flask = makeFlask('boiling flask', 0x60a5fa, 0.38); flask.position.set(-1.6, 0.55, 0); group.add(flask); buildBurner(group, actors, 0, [-1.6, 0.44, 0]); group.add(makeLine([new THREE.Vector3(-1.05, 2.1, 0), new THREE.Vector3(0.7, 2.35, 0), new THREE.Vector3(2.1, 1.25, 0)], 0xc7ddff, 1)); const recv = makeBeaker(0.45, 0.85, s.temperature > 78 ? 0.35 : 0.08, 0x93c5fd, 'distillate'); recv.position.set(2.2, 0.55, 0); group.add(recv); } else if (s.method === 'filtration') { const beaker = makeBeaker(0.55, 0.9, 0.45, 0x60a5fa, 'filtrate'); beaker.position.set(0, 0.55, 0); group.add(beaker); const funnel = makeCylinder(0.65, 0.18, 0.9, glass(0xc7ddff, 0.3), [0, 1.65, 0], 48); funnel.rotation.x = Math.PI; group.add(funnel); addLabel(group, 'filter paper + residue', [0.9, 2.15, 0], { scale: 0.17 }); } else if (s.method === 'chromatography') { group.add(makeBox(1.1, 1.6, 0.04, mat(0xf8fafc), [0, 1.5, 0])); ['#ef4444', '#22c55e', '#3b82f6'].forEach((c, i) => group.add(makeSphere(0.08, mat(parseInt(c.slice(1), 16)), [-0.25 + i * 0.25, 1.0 + i * 0.23, 0.04], 16))); addLabel(group, 'solvent front + separated spots', [0, 2.6, 0], { scale: 0.19 }); } else { const dish = makeCylinder(0.85, 0.75, 0.16, glass(0xc7ddff, 0.28), [0, 0.85, 0], 64); group.add(dish); buildBurner(group, actors, 0, [0, 0.45, 0]); addLabel(group, 'evaporating dish: crystals form', [0, 2.15, 0], { scale: 0.2 }); } }
function buildTitration(group, actors, s, config) {
  const isRedox = config.title.includes('KMnO');
  makeBuretteStand(group, 0, 0.76, isRedox ? 0x7c3aed : 0x38bdf8, isRedox ? 'KMnO₄ burette' : 'HCl burette');
  const req = isRedox ? (s.fasM * 25.0) / (5 * s.kmno4M) : s.unknownM * 25.0 / 0.10;
  let color = 0xec4899;
  if (isRedox) color = s.titreMl > req ? 0xd946ef : 0xf8fafc;
  else if (s.indicator === 'methyl') color = s.titreMl < req ? 0xfacc15 : s.titreMl - req > 0.3 ? 0xef4444 : 0xf97316;
  else color = s.titreMl < req ? 0xec4899 : 0xe5e7eb;
  const tile = makeBox(2.1, 0.035, 1.55, mat(0xf8fafc, { roughness: 0.38 }), [0, 0.81, 0]);
  group.add(tile);
  const flask = makeFlask('25.0 mL conical flask', color, 0.36); flask.position.set(0, 0.58, 0); group.add(flask);
  const dropColor = isRedox ? 0xa855f7 : 0x38bdf8;
  for (let i = 0; i < 3; i++) {
    const d = makeSphere(0.035 - i * 0.005, mat(dropColor, { opacity: 0.78, emissive: dropColor, emissiveIntensity: 0.12 }), [0, 2.08 - i * 0.22, 0], 14);
    group.add(d);
  }
  actors.drops = { x: 0, y: 2.0, color: dropColor };
  addLabel(group, titrationStatus(s.titreMl, req), [1.55, 2.58, 0], { scale: 0.16 });
  addLabel(group, `required ≈ ${req.toFixed(2)} mL`, [-1.45, 2.56, 0], { scale: 0.15 });
}
function buildBurner(group, actors, key = 0, pos = [0, 0.55, 0], flameColor = 0x60a5fa) { const g = new THREE.Group(); g.position.set(...pos); g.add(makeCylinder(0.35, 0.35, 0.08, metal(0x475569), [0, 0, 0], 32)); g.add(makeCylinder(0.08, 0.08, 0.55, metal(0x64748b), [0, 0.28, 0], 24)); const flame = makeFlame(flameColor); flame.position.y = 0.72; g.add(flame); group.add(g); actors[`flame${key}`] = flame; return g; }
function makeFlame(color = 0x60a5fa) { const g = new THREE.Group(); const outer = makeSphere(0.35, mat(color, { opacity: 0.55, emissive: color, emissiveIntensity: 0.65 }), [0, 0.1, 0], 32); outer.scale.y = 1.75; const inner = makeSphere(0.18, mat(0xffffff, { opacity: 0.75, emissive: 0xffffff, emissiveIntensity: 0.8 }), [0, -0.05, 0], 24); inner.scale.y = 1.25; g.add(outer, inner); return g; }
function buildFlame(group, actors, s) { const c = CATION_COLORS[s.cation] || CATION_COLORS.Na; buildBurner(group, actors, 0, [0, 0.55, 0], c.flame); group.add(makeCylinder(0.025, 0.025, 1.6, metal(0xcbd5e1), [-0.7, 1.6, 0])); group.add(makeSphere(0.08, mat(c.flame, { emissive: c.flame, emissiveIntensity: 0.8 }), [-0.3, 1.62, 0], 16)); addLabel(group, c.result, [0.2, 2.95, 0], { scale: 0.2 }); }
function makeTestTube(color = 0x93c5fd, fill = 0.45, label = '') {
  const g = new THREE.Group();
  const tube = makeCylinder(0.17, 0.15, 1.18, glass(0xc7ddff, 0.29), [0, 0.62, 0], 32);
  g.add(tube);
  const rim = makeCylinder(0.19, 0.19, 0.025, glass(0xe0f2fe, 0.38), [0, 1.22, 0], 32);
  g.add(rim);
  const liq = makeCylinder(0.135, 0.125, 1.03 * fill, mat(color, { opacity: 0.60, roughness: 0.07 }), [0, 0.13 + fill * 0.5, 0], 32);
  g.add(liq);
  const surface = makeCylinder(0.132, 0.132, 0.012, mat(color, { opacity: 0.72 }), [0, 0.14 + 1.03 * fill, 0], 32);
  g.add(surface);
  if (label) addLabel(g, label, [0, 1.48, 0], { scale: 0.10, fontSize: 20 });
  return g;
}
function buildTestTubes(group, actors, s) {
  const colors = { carbonate: 0xe5e7eb, chloride: 0xffffff, sulfate: 0xffffff, nitrate: 0x7c2d12, sulfide: 0x111827 };
  group.add(makeBox(4.7, 0.20, 0.55, wood(0x8b5a2b), [0, 0.76, 0]));
  group.add(makeBox(4.7, 0.12, 0.12, wood(0x6b4426), [0, 1.08, -0.28]));
  for (let i = 0; i < 5; i++) {
    const active = i === 2;
    const tube = makeTestTube(active ? colors[s.anion] || 0x93c5fd : 0x93c5fd, 0.35 + i * 0.05, active ? s.anion : `test ${i + 1}`);
    tube.position.set(-1.6 + i * 0.8, 0.76, 0);
    tube.rotation.z = (i - 2) * 0.025;
    group.add(tube);
  }
  addLabel(group, ANION_RESULTS[s.anion], [0, 3.02, 0], { scale: 0.14, fontSize: 22 });
}
function buildGasPrep(group, actors, s) { const flask = makeFlask('reaction flask', 0x93c5fd, 0.38); flask.position.set(-1.4, 0.52, 0); group.add(flask); group.add(makeLine([new THREE.Vector3(-0.9, 2.0, 0), new THREE.Vector3(0.6, 2.15, 0), new THREE.Vector3(1.4, 1.2, 0)], 0xc7ddff, 1)); const jar = makeCylinder(0.5, 0.5, 1.35, glass(0xc7ddff, 0.24), [1.7, 1.25, 0], 48); group.add(jar); actors.bubbles = { root: jar, rate: s.rate / 100 }; addLabel(group, GAS_RESULTS[s.gas], [0, 3.15, 0], { scale: 0.18 }); }
function buildCrystallization(group, actors, s) { const dish = makeCylinder(0.85, 0.75, 0.15, glass(0xc7ddff, 0.32), [0, 1.05, 0], 64); group.add(dish); buildBurner(group, actors, 0, [0, 0.52, 0]); for (let i = 0; i < 18; i++) group.add(makeSphere(0.04 + Math.random() * 0.035, mat(0x93c5fd), [(Math.random() - 0.5) * 1.0, 1.18, (Math.random() - 0.5) * 0.7], 10)); addLabel(group, `mass lost ${(s.hydrateMass - s.residueMass).toFixed(2)} g`, [0, 2.45, 0], { scale: 0.23 }); }
function buildSaltAnalysis(group, actors, s) { buildTestTubes(group, actors, { anion: s.anion, drops: 5 }); const flameCfg = CATION_COLORS[s.cation] || CATION_COLORS.Cu; buildBurner(group, actors, 1, [2.6, 0.55, 0], flameCfg.flame); addLabel(group, `${flameCfg.label} + ${s.anion}`, [0, 3.35, 0], { scale: 0.22 }); }
function buildElectrolysis(group, actors, s) { const beaker = makeBeaker(0.9, 1.45, 0.7, 0x2563eb, 'CuSO₄'); beaker.position.set(0, 0.65, 0); group.add(beaker); const cathode = makeBox(0.1, 1.1, 0.38, metal(0xb45309), [-0.35, 1.4, 0]); const anode = makeBox(0.1, 1.1, 0.38, metal(0xb45309), [0.35, 1.4, 0]); group.add(cathode, anode); addWireLoop(group, 0xef4444); actors.electrolysis = { cathode, current: s.currentA }; addLabel(group, `${s.currentA.toFixed(2)} A for ${s.timeMin.toFixed(0)} min`, [0, 3.05, 0], { scale: 0.23 }); }
function buildPH(group, actors, s) { for (let i = 0; i < 5; i++) { const pH = Math.max(1, Math.min(14, s.pH + (i - 2) * 1.2)); const tube = makeTestTube(indicatorColor(s.indicator, pH), 0.5, `pH ${pH.toFixed(1)}`); tube.position.set(-1.6 + i * 0.8, 0.65, 0); group.add(tube); } group.add(makeBox(4.6, 0.18, 0.5, wood(0x8b5a2b), [0, 0.75, 0])); addLabel(group, `${s.indicator}: ${indicatorColorName(s.indicator, s.pH)}`, [0, 3.0, 0], { scale: 0.23 }); }
function buildFunctional(group, actors, s) { buildTestTubes(group, actors, { anion: 'chloride', drops: s.reagentDrops }); const tube = makeTestTube(groupColor(s.group), 0.5, s.group); tube.position.set(0, 0.72, 0.6); group.add(tube); addLabel(group, GROUP_RESULTS[s.group], [0, 3.05, 0], { scale: 0.18 }); }
function groupColor(group) { return { alcohol: 0xe5e7eb, aldehyde: 0xb45309, ketone: 0xfacc15, carboxylic: 0xf8fafc, phenol: 0x8b5cf6 }[group] || 0x93c5fd; }
function buildThermo(group, actors, s) { const cup = makeBeaker(0.95, 1.35, 0.65, 0x60a5fa, 'calorimeter'); cup.position.set(0, 0.65, 0); group.add(cup); const therm = makeThermometer(2.2, 25 + s.deltaT); therm.position.set(0.68, 1.2, 0); group.add(therm); addLabel(group, `ΔT = ${s.deltaT.toFixed(1)} °C`, [0, 2.95, 0], { scale: 0.24 }); }
function buildLassaigne(group, actors, s) { buildBurner(group, actors, 0, [-1.3, 0.55, 0]); const fusion = makeTestTube(0xf97316, 0.25, 'sodium fusion'); fusion.position.set(-1.3, 1.45, 0); fusion.rotation.z = -0.85; group.add(fusion); const result = makeTestTube(lassaigneColor(s.element), 0.5, s.element); result.position.set(1.0, 0.65, 0); group.add(result); addLabel(group, lassaigneResult(s.element), [0, 3.05, 0], { scale: 0.18 }); }
function lassaigneColor(element) { return { nitrogen: 0x1d4ed8, sulfur: 0x581c87, chlorine: 0xffffff, bromine: 0xfacc15, iodine: 0xf59e0b }[element] || 0x93c5fd; }

function updateActors(actors, dt, t, state) {
  if (actors.pendulum) {
    const p = actors.pendulum; const theta = p.amp * Math.sin(t * Math.sqrt(9.81 / (state.lengthCm / 100)));
    const bobPos = new THREE.Vector3(p.pivot.x + Math.sin(theta) * p.L, p.pivot.y - Math.cos(theta) * p.L, 0);
    p.bob.position.copy(bobPos); p.string.geometry.dispose(); p.string.geometry = new THREE.BufferGeometry().setFromPoints([p.pivot, bobPos]);
  }
  if (actors.slidingBlock && actors.slidingBlock.sliding) actors.slidingBlock.block.position.x += Math.sin(t * 1.4) * dt * 0.22;
  Object.keys(actors).forEach((k) => { if (k.startsWith('flame') && actors[k]) { actors[k].scale.setScalar(1 + Math.sin(t * 12) * 0.035); actors[k].rotation.y += dt * 0.8; } });
  ['ammeter', 'voltmeter', 'galvanometer'].forEach((key) => {
    const m = actors[key]; if (!m) return; const a = -0.75 + Math.min(1, m.value / m.max) * 1.5; m.needle.rotation.z = -a;
  });
  if (actors.fork) actors.fork.rotation.z = Math.sin(t * 75) * 0.015;
  if (actors.electrolysis) actors.electrolysis.cathode.scale.y = 1 + Math.sin(t * 2) * 0.01 + actors.electrolysis.current * 0.02;
}
