import { THREE, createEngine, createOrbitControls, basicLights, makeContactShadow } from './engine.js';
import { createPanel, createHud, showInfoCard } from './sim-ui.js';
import { getBiologyPractical } from './bio3d-data.js';
import { buildBiologyModel } from './bio3d-models.js';
import { getBiologyMetricRows, getBiologyFormula, getBiologyBadge, getBiologyConclusion } from './bio3d-science.js';

function initialState(config) {
  const state = { running: true };
  (config.controls || []).forEach((control) => {
    state[control.id] = control.value ?? (control.type === 'select' ? control.options?.[0] : control.min ?? 0);
  });
  return state;
}
function numeric(v, fallback = 0) {
  const parsed = parseFloat(v);
  return Number.isFinite(parsed) ? parsed : fallback;
}
function getMetricRows(config, state, recordCount = 0) {
  return getBiologyMetricRows(config, state, recordCount);
}
function cameraViewFor(kind, mobile) {
  if (['microscope','mitosis','plasmolysis','stomata','anatomyTS','animalTissue','animalMitosis','frogDev','microscopeParts'].includes(kind)) {
    return { pos: mobile ? [3.8, 3.2, 6.8] : [4.8, 3.7, 7.2], target: [0.35, 1.65, -0.18], min: 3.4, max: 12 };
  }
  if (['skeleton','skeletonHealth','cockroach','flower','inflorescence'].includes(kind)) return { pos: [4.2, 3.2, 6.1], target: [0, 1.65, 0], min: 3, max: 12 };
  return { pos: mobile ? [4.8, 3.8, 6.4] : [5.6, 4.2, 7.1], target: [0, 1.35, 0], min: 3.2, max: 13 };
}
function makeTable(container) {
  const card = document.createElement('div');
  card.className = 'ix-lab-data-card bio3d-book';
  card.innerHTML = '<div class="ix-lab-data-title">Student observation book</div><div class="ix-lab-table-scroll"><table class="ix-lab-data-table"><thead><tr><th>Trial</th><th>Observation</th><th>Result</th></tr></thead><tbody></tbody></table></div>';
  container.appendChild(card);
  const tbody = card.querySelector('tbody');
  return {
    add(record) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${record.trial}</td><td>${record.observation}</td><td>${record.result}</td>`;
      tbody.appendChild(tr);
      while (tbody.children.length > 6) tbody.firstElementChild.remove();
    },
    clear() { tbody.innerHTML = ''; },
  };
}
function setReadouts(readouts, rows) {
  rows.slice(0, 5).forEach((row, i) => {
    if (readouts[i]) readouts[i].set(row[1]);
  });
}
function disposeObject(root) {
  root.traverse((obj) => {
    if (obj.geometry) obj.geometry.dispose();
    if (obj.material && !obj.material.__shared) {
      const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
      mats.forEach((m) => {
        if (!m.userData?.scanGrade) Object.keys(m).forEach((k) => { if (m[k] && m[k].isTexture) m[k].dispose(); });
      });
    }
  });
}
function randomize(config, state, handles) {
  (config.controls || []).forEach((control) => {
    if (control.type === 'select') {
      const opts = control.options || [];
      const next = opts[Math.floor(Math.random() * opts.length)] ?? control.value;
      state[control.id] = next;
      handles.get(control.id)?.set?.(next);
    } else {
      const min = numeric(control.min, 0), max = numeric(control.max, 100), step = numeric(control.step, 1);
      const raw = min + Math.random() * (max - min);
      const v = Math.round(raw / step) * step;
      state[control.id] = Number(v.toFixed(step < 1 ? 2 : 0));
      handles.get(control.id)?.set?.(state[control.id]);
    }
  });
}

export function initBio3DLab(stage, opts = {}) {
  const config = getBiologyPractical(opts.lessonSlug);
  stage.classList.add('bio3d-stage');
  stage.dataset.bioKind = config.kind;
  const engine = createEngine(stage, { fov: 44, shadows: true, environment: true, exposure: 1.05 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  scene.background = new THREE.Color(0x050816);
  scene.fog = new THREE.Fog(0x050816, 8, 24);
  basicLights(scene, { ambient: 0.45, key: 1.9, fill: 0.65, keyPos: [4, 8, 6], rim: 0.55, rimPos: [-5, 5, -7] });
  // Grounding contact occlusion under the bench, for one draw call and no extra render pass.
  const contactShadow = makeContactShadow({ y: 0.715, width: 6.2, depth: 4.4, opacity: 0.66 });
  scene.add(contactShadow);
  const view = cameraViewFor(config.kind, quality.mobile);
  camera.position.set(...view.pos);
  const target = new THREE.Vector3(...view.target);
  const controls = createOrbitControls(camera, engine.canvas, { target, minDistance: view.min, maxDistance: view.max, autoRotate: quality.reducedMotion ? 0 : 0.04, damping: 0.11 });
  controls.setView(new THREE.Vector3(...view.pos), target);

  const state = initialState(config);
  const hud = createHud(stage);
  const badge1 = hud.badge(`Class ${config.grade} Biology`, '#22c55e');
  const badge2 = hud.badge(getBiologyBadge(config, state), '#93c5fd');
  const badge3 = hud.badge('scan-grade PBR model', '#c084fc');
  let stepIndex = 0;
  let records = [];
  let group = null;
  let needsRebuild = true;
  let readoutsDirty = true;
  let builtStateKey = null;
  let lastRebuildAt = -Infinity;

  const panel = createPanel(stage, { title: config.title, compact: true, collapseOnMobile: true, startCollapsed: window.innerWidth < 720 });
  panel.info(config.aim);
  const stepInfo = panel.readout({ label: 'Step', value: `1/${config.steps.length}: ${config.steps[0]}` });
  const handles = new Map();
  // Readouts are no longer recomputed every frame, so every state mutation flags them.
  function markDirty() { needsRebuild = true; readoutsDirty = true; }
  (config.controls || []).slice(0, 3).forEach((control) => {
    if (control.type === 'select') {
      const h = panel.select({ label: control.label, options: control.options, value: control.value, onChange: (v) => { state[control.id] = v; markDirty(); } });
      handles.set(control.id, h);
    } else {
      const h = panel.slider({ label: control.label, min: control.min, max: control.max, step: control.step, value: control.value, unit: control.unit || '', format: (v) => `${v}${control.unit || ''}`, onChange: (v) => { state[control.id] = v; markDirty(); } });
      handles.set(control.id, h);
    }
  });
  panel.buttonRow([
    { label: 'Step', icon: 'skip_next', onClick: () => { stepIndex = (stepIndex + 1) % config.steps.length; stepInfo.set(`${stepIndex + 1}/${config.steps.length}: ${config.steps[stepIndex]}`); } },
    { label: 'Record', icon: 'playlist_add', onClick: () => recordCurrent() },
    { label: 'Trial', icon: 'experiment', onClick: () => { randomize(config, state, handles); markDirty(); updateReadouts(); } },
  ]);
  panel.buttonRow([
    { label: 'View', icon: 'center_focus_strong', onClick: resetView },
    { label: 'Clear', icon: 'delete_sweep', onClick: () => { records = []; table.clear(); readoutsDirty = true; updateReadouts(); } },
    { label: 'Help', icon: 'help', onClick: () => showInfoCard(stage, { title: config.record, body: `${config.aim} Scientific model: ${getBiologyFormula(config, state)}. Record observations with units, compare against the result, then write a reasoned conclusion.`, color: '#22c55e' }) },
  ]);
  panel.section('Live readings');
  const seedRows = getMetricRows(config, state, records.length);
  const readouts = seedRows.slice(0, 5).map((row) => panel.readout({ label: row[0], value: row[1] }));
  panel.section('Scientific formula');
  const formulaOut = panel.readout({ label: 'Model rule', value: getBiologyFormula(config, state) });
  panel.section('Model fidelity');
  panel.readout({ label: 'Visual standard', value: quality.tier === 'low' ? 'optimized PBR textures' : 'scan-grade PBR + micro displacement' });
  panel.readout({ label: 'Scientific labels', value: 'calibrated morphology + live readings' });
  const table = makeTable(panel.body);

  function resetView() { controls.setView(new THREE.Vector3(...view.pos), target); }
  function stateKey() { return JSON.stringify(state); }
  function rebuild() {
    if (group) { scene.remove(group); disposeObject(group); }
    group = new THREE.Group();
    buildBiologyModel(group, config, state, { quality });
    scene.add(group);
    needsRebuild = false;
    readoutsDirty = true;
    builtStateKey = stateKey();
  }
  function updateReadouts() {
    const rows = getMetricRows(config, state, records.length);
    setReadouts(readouts, rows);
    badge1.set(`Class ${config.grade} Biology`);
    badge2.set(getBiologyBadge(config, state));
    badge3.set(quality.tier === 'low' ? 'optimized PBR model' : 'scan-grade PBR model');
    formulaOut.set(getBiologyFormula(config, state));
  }
  function recordCurrent() {
    const rows = getMetricRows(config, state, records.length);
    const main = rows[0] ? `${rows[0][0]}: ${rows[0][1]}` : config.record;
    const result = getBiologyConclusion(config, state);
    const record = { trial: records.length + 1, observation: main, result };
    records.push(record);
    table.add(record);
    updateReadouts();
    showInfoCard(stage, { title: 'Observation recorded', body: `${main}. ${result}.`, color: '#22c55e' });
  }

  // Rebuilding the model costs real time, so a dragging slider must not trigger a rebuild on
  // every input event. Coalesce to at most one rebuild per REBUILD_INTERVAL and skip entirely
  // when the state has not actually changed (e.g. re-picking the current dropdown option).
  const REBUILD_INTERVAL = 0.12;
  engine.setUpdate((dt, t) => {
    controls.update(dt);
    if (needsRebuild && t - lastRebuildAt >= REBUILD_INTERVAL) {
      if (stateKey() !== builtStateKey) {
        lastRebuildAt = t;
        rebuild();
      } else {
        needsRebuild = false;
      }
    }
    if (group && state.running) group.rotation.y += Math.sin(t * 0.5) * dt * 0.008;
    if (readoutsDirty) { readoutsDirty = false; updateReadouts(); }
  });
  rebuild();
  engine.start();

  return {
    dispose() {
      if (group) disposeObject(group);
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
