import { THREE, createEngine, createOrbitControls, basicLights } from './engine.js';
import { createPanel, createHud, showInfoCard } from './sim-ui.js';
import { getBiologyPractical } from './bio3d-data.js';
import { buildBiologyModel } from './bio3d-models.js';

function initialState(config) {
  const state = { running: true };
  (config.controls || []).forEach((control) => {
    state[control.id] = control.value ?? (control.type === 'select' ? control.options?.[0] : control.min ?? 0);
  });
  return state;
}
function numeric(v, fallback = 0) { const n = parseFloat(v); return Number.isFinite(n) ? n : fallback; }
function fmt(n, digits = 2) { return Number.isFinite(n) ? Number(n).toFixed(digits) : '--'; }
function getMetricRows(config, state, recordCount = 0) {
  const kind = config.kind;
  const rows = [];
  if (['microscope','anatomyTS','animalTissue','frogDev','microscopeParts'].includes(kind)) {
    const mag = numeric(String(state.magnification || state.objective || '400').replace('x', ''), 400);
    const fieldMm = 18 / Math.max(1, mag);
    rows.push(['Total magnification', `${mag}x`], ['Field diameter', `${fmt(fieldMm, 3)} mm`], ['Observation quality', `${state.focus ?? state.diaphragm ?? 80}%`]);
  } else if (kind === 'mitosis' || kind === 'animalMitosis') {
    const cells = numeric(state.cells, 100);
    const dividing = Math.round(cells * (kind === 'animalMitosis' ? 0.11 : 0.09));
    rows.push(['Total cells', cells], ['Dividing cells', dividing], ['Mitotic index', `${fmt(dividing / cells * 100, 1)}%`]);
  } else if (kind === 'herbarium') {
    rows.push(['Dryness', `${state.dryness}%`], ['Label completeness', `${state.labelScore}%`], ['Preservation status', state.dryness > 75 && state.labelScore > 70 ? 'acceptable' : 'needs correction']);
  } else if (kind === 'mushroom') {
    rows.push(['Spore print', state.sporePrint], ['Volva present', state.volva], ['Warning', state.volva === 'yes' && state.sporePrint === 'white' ? 'poison-risk features' : 'identify with full key']);
  } else if (kind === 'flower') {
    const ovary = state.family === 'Liliaceae' ? 'tricarpellary' : state.family === 'Fabaceae' ? 'monocarpellary' : 'bicarpellary';
    rows.push(['Family', state.family], ['Whorl opened', `${state.whorl}/4`], ['Ovary character', ovary]);
  } else if (kind === 'inflorescence') {
    rows.push(['Inflorescence', state.type], ['Pedicel length', `${state.pedicel} mm`], ['Category', ['cyme'].includes(state.type) ? 'cymose' : 'racemose/head']);
  } else if (kind === 'culture') {
    const cfu = numeric(state.colonies, 54) * Math.pow(10, numeric(state.dilution, 3));
    rows.push(['Colonies', state.colonies], ['Dilution', `10^-${state.dilution}`], ['Estimated CFU/mL', cfu.toExponential(2)]);
  } else if (kind === 'pond') {
    rows.push(['Water pH', state.pH], ['Turbidity', `${state.turbidity} NTU`], ['Condition', state.pH >= 6.5 && state.pH <= 8.5 ? 'suitable' : 'stressed']);
  } else if (kind === 'pondZoo') {
    rows.push(['Water pH', state.pH], ['Dissolved oxygen', `${state.oxygen} mg/L`], ['Faunal condition', state.oxygen >= 5 ? 'good oxygenation' : 'low oxygen stress']);
  } else if (kind === 'quadrat') {
    const density = numeric(state.plants, 22) / numeric(state.area, 1);
    rows.push(['Individuals', state.plants], ['Quadrat area', `${state.area} m2`], ['Density', `${fmt(density, 1)} plants/m2`]);
  } else if (kind === 'quadrat2') {
    const freq = numeric(state.hits, 7) / numeric(state.total, 10) * 100;
    rows.push(['Quadrats present', state.hits], ['Total quadrats', state.total], ['Frequency', `${fmt(freq, 1)}%`]);
  } else if (kind === 'soil') {
    const wet = numeric(state.wetMass, 80), dry = numeric(state.dryMass, 62);
    rows.push(['Wet mass', `${wet} g`], ['Dry mass', `${dry} g`], ['Moisture content', `${fmt((wet - dry) / dry * 100, 1)}%`]);
  } else if (kind === 'specimens') {
    rows.push(['Selected specimen', state.specimen], ['Confidence', `${state.confidence}%`], ['Conclusion', `${state.specimen}: identify by diagnostic characters`]);
  } else if (kind === 'fossil') {
    rows.push(['Visible chambers', state.chambers], ['Preservation', `${state.ageScore}%`], ['Evidence type', 'paleontological evidence']);
  } else if (kind === 'animals') {
    rows.push(['Specimen', state.animal], ['Characters matched', `${state.featureScore}/5`], ['Level', 'phylum/class identification']);
  } else if (kind === 'dissection') {
    rows.push(['Model', state.model], ['Opened', `${state.opened}%`], ['Canal traced', state.opened > 60 ? 'mouth to anus visible' : 'open further']);
  } else if (kind === 'conservation') {
    const score = numeric(state.habitat, 62) * 0.6 + numeric(state.corridor, 45) * 0.4;
    rows.push(['Habitat intactness', `${state.habitat}%`], ['Corridor strength', `${state.corridor}%`], ['Conservation score', `${fmt(score, 0)}/100`]);
  } else if (kind === 'osmosis') {
    const rise = numeric(state.sucrose, 20) * numeric(state.time, 45) / 1200;
    rows.push(['Sucrose', `${state.sucrose}%`], ['Time', `${state.time} min`], ['Liquid rise', `${fmt(rise, 2)} cm`]);
  } else if (kind === 'plasmolysis') {
    const plasm = Math.min(100, Math.max(0, numeric(state.salt, 3) * 12));
    rows.push(['Salt concentration', `${state.salt}%`], ['Cells observed', state.cells], ['Plasmolysed cells', `${Math.round(numeric(state.cells, 60) * plasm / 100)} (${fmt(plasm, 1)}%)`]);
  } else if (kind === 'stomata') {
    const fieldArea = 0.16;
    rows.push(['Surface', state.surface], ['Stomata counted', state.stomata], ['Density', `${fmt(numeric(state.stomata, 42) / fieldArea, 0)} stomata/mm2`]);
  } else if (kind === 'transpiration') {
    const rate = 60 / numeric(state.time, 75);
    rows.push(['Surface', state.surface], ['Time', `${state.time} s`], ['Relative rate', `${fmt(rate, 2)} units/min`]);
  } else if (kind === 'respiration') {
    const rate = numeric(state.movement, 18) / numeric(state.mass, 20);
    rows.push(['Seed mass', `${state.mass} g`], ['Movement', `${state.movement} mm`], ['Rate', `${fmt(rate, 2)} mm/g`]);
  } else if (kind === 'anaerobic') {
    const bubbles = numeric(state.yeast, 70) * numeric(state.time, 25) / 100;
    rows.push(['Yeast activity', `${state.yeast}%`], ['Time', `${state.time} min`], ['CO2 output', `${fmt(bubbles, 1)} bubble units`]);
  } else if (kind === 'phototropism') {
    const curve = Math.min(70, numeric(state.light, 70) * numeric(state.hours, 36) / 90);
    rows.push(['Light intensity', `${state.light}%`], ['Exposure', `${state.hours} h`], ['Curvature', `${fmt(curve, 0)} deg toward light`]);
  } else if (kind === 'apicalBud') {
    const growth = (100 - numeric(state.auxin, 35)) * numeric(state.days, 10) / 100;
    rows.push(['Days', state.days], ['Auxin level', `${state.auxin}%`], ['Lateral growth', `${fmt(growth, 1)} cm`]);
  } else if (kind === 'suction') {
    const move = numeric(state.leafArea, 60) * numeric(state.minutes, 30) / 1000;
    rows.push(['Leaf area', `${state.leafArea} cm2`], ['Time', `${state.minutes} min`], ['Water column movement', `${fmt(move, 2)} cm`]);
  } else if (kind === 'genetics') {
    const d = numeric(state.dominant, 90), r = numeric(state.recessive, 32);
    rows.push(['Dominant', d], ['Recessive', r], ['Observed ratio', `${fmt(d / Math.max(r, 1), 2)}:1`]);
  } else if (kind === 'imbibition') {
    const init = numeric(state.initial, 20), fin = numeric(state.final, 32);
    rows.push(['Initial mass', `${init} g`], ['Final mass', `${fin} g`], ['Water uptake', `${fmt((fin - init) / init * 100, 1)}%`]);
  } else if (kind === 'biofertilizer') {
    rows.push(['Moisture', `${state.moisture}%`], ['Incubation', `${state.days} days`], ['Batch status', state.moisture >= 35 && state.moisture <= 60 ? 'good carrier moisture' : 'adjust moisture']);
  } else if (kind === 'frogDev') {
    rows.push(['Stage', state.stage], ['Magnification', `${state.magnification}x`], ['Comment', stageComment(state.stage)]);
  } else if (kind === 'starchTest') {
    const positive = ['potato', 'rice water'].includes(state.sample);
    rows.push(['Sample', state.sample], ['Iodine drops', state.iodine], ['Result', positive ? 'blue-black positive' : 'brown negative']);
  } else if (kind === 'proteinTest') {
    const positive = ['egg albumin', 'milk'].includes(state.sample);
    rows.push(['Sample', state.sample], ['Biuret drops', state.biuret], ['Result', positive ? 'violet positive' : 'blue negative']);
  } else if (kind === 'amylase') {
    const activity = Math.max(0, 100 - Math.abs(numeric(state.temperature, 37) - 37) * 3 - Math.abs(numeric(state.pH, 7) - 7) * 18);
    rows.push(['Temperature', `${state.temperature} C`], ['pH', state.pH], ['Relative activity', `${fmt(activity, 0)}%`]);
  } else if (kind === 'urine') {
    rows.push(['Test', state.test], ['Intensity', `${state.intensity}%`], ['Observation', urineObservation(state.test, state.intensity)]);
  } else if (kind === 'bloodSugar') {
    const g = numeric(state.glucose, 96);
    rows.push(['Read time', `${state.time} s`], ['Glucose', `${g} mg/dL`], ['Range', g < 70 ? 'low' : g < 140 ? 'normal/random acceptable' : 'high']);
  } else if (kind === 'skeleton') {
    rows.push(['Joint', state.joint], ['Movement angle', `${state.angle} deg`], ['Joint type', jointType(state.joint)]);
  } else if (kind === 'skeletonHealth') {
    rows.push(['Joint', state.joint], ['Mobility', `${state.mobility}%`], ['Comment', state.mobility < 50 ? 'restricted movement' : 'functional range']);
  } else if (kind === 'cockroach') {
    rows.push(['View', state.view], ['Focus part', state.zoomPart], ['Diagnostic feature', 'head, thorax, abdomen; three pairs of legs']);
  } else {
    rows.push(['Trial', recordCount + 1], ['Observation', 'recorded'], ['Conclusion', 'state reason']);
  }
  return rows;
}
function stageComment(stage) {
  return { 'fertilized egg': 'single zygote', cleavage: 'many blastomeres', blastula: 'blastocoel visible', gastrula: 'germ layers forming' }[stage] || 'developmental stage';
}
function urineObservation(test, intensity) {
  const level = intensity > 60 ? 'strong positive' : intensity > 20 ? 'weak positive' : 'negative';
  return `${level} for ${test}`;
}
function jointType(joint) {
  if (String(joint).includes('suture')) return 'fixed/immovable';
  if (String(joint).includes('hinge')) return 'hinge synovial';
  if (String(joint).includes('ball')) return 'ball-and-socket';
  if (String(joint).includes('pivot')) return 'pivot';
  return 'movable joint';
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
        Object.keys(m).forEach((k) => { if (m[k] && m[k].isTexture) m[k].dispose(); });
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
  const engine = createEngine(stage, { fov: 44, shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  scene.background = new THREE.Color(0x050816);
  scene.fog = new THREE.Fog(0x050816, 8, 24);
  basicLights(scene, { ambient: 0.65, key: 1.9, fill: 0.65, keyPos: [4, 8, 6] });
  const view = cameraViewFor(config.kind, quality.mobile);
  camera.position.set(...view.pos);
  const target = new THREE.Vector3(...view.target);
  const controls = createOrbitControls(camera, engine.canvas, { target, minDistance: view.min, maxDistance: view.max, autoRotate: quality.reducedMotion ? 0 : 0.04, damping: 0.11 });
  controls.setView(new THREE.Vector3(...view.pos), target);

  const hud = createHud(stage);
  const badge1 = hud.badge(`Class ${config.grade} Biology`, '#22c55e');
  const badge2 = hud.badge(config.record, '#93c5fd');
  const state = initialState(config);
  let stepIndex = 0;
  let records = [];
  let group = null;
  let needsRebuild = true;

  const panel = createPanel(stage, { title: config.title, compact: true, collapseOnMobile: true, startCollapsed: window.innerWidth < 720 });
  panel.info(config.aim);
  const stepInfo = panel.readout({ label: 'Step', value: `1/${config.steps.length}: ${config.steps[0]}` });
  const handles = new Map();
  (config.controls || []).slice(0, 3).forEach((control) => {
    if (control.type === 'select') {
      const h = panel.select({ label: control.label, options: control.options, value: control.value, onChange: (v) => { state[control.id] = v; needsRebuild = true; } });
      handles.set(control.id, h);
    } else {
      const h = panel.slider({ label: control.label, min: control.min, max: control.max, step: control.step, value: control.value, unit: control.unit || '', format: (v) => `${v}${control.unit || ''}`, onChange: (v) => { state[control.id] = v; needsRebuild = true; } });
      handles.set(control.id, h);
    }
  });
  panel.buttonRow([
    { label: 'Step', icon: 'skip_next', onClick: () => { stepIndex = (stepIndex + 1) % config.steps.length; stepInfo.set(`${stepIndex + 1}/${config.steps.length}: ${config.steps[stepIndex]}`); } },
    { label: 'Record', icon: 'playlist_add', onClick: () => recordCurrent() },
    { label: 'Trial', icon: 'experiment', onClick: () => { randomize(config, state, handles); needsRebuild = true; updateReadouts(); } },
  ]);
  panel.buttonRow([
    { label: 'View', icon: 'center_focus_strong', onClick: resetView },
    { label: 'Clear', icon: 'delete_sweep', onClick: () => { records = []; table.clear(); updateReadouts(); } },
    { label: 'Help', icon: 'help', onClick: () => showInfoCard(stage, { title: config.record, body: `${config.aim} Follow steps, change variables, record observations and write a reasoned conclusion.`, color: '#22c55e' }) },
  ]);
  panel.section('Live readings');
  const seedRows = getMetricRows(config, state, records.length);
  const readouts = seedRows.slice(0, 5).map((row) => panel.readout({ label: row[0], value: row[1] }));
  const table = makeTable(panel.body);

  function resetView() { controls.setView(new THREE.Vector3(...view.pos), target); }
  function rebuild() {
    if (group) { scene.remove(group); disposeObject(group); }
    group = new THREE.Group();
    buildBiologyModel(group, config, state, {});
    scene.add(group);
    needsRebuild = false;
  }
  function updateReadouts() {
    const rows = getMetricRows(config, state, records.length);
    setReadouts(readouts, rows);
    badge1.set(`Class ${config.grade} Biology`);
    badge2.set(rows[rows.length - 1]?.[1] || config.record);
  }
  function recordCurrent() {
    const rows = getMetricRows(config, state, records.length);
    const main = rows[0] ? `${rows[0][0]}: ${rows[0][1]}` : config.record;
    const result = rows[rows.length - 1] ? `${rows[rows.length - 1][0]}: ${rows[rows.length - 1][1]}` : 'recorded';
    const record = { trial: records.length + 1, observation: main, result };
    records.push(record);
    table.add(record);
    updateReadouts();
    showInfoCard(stage, { title: 'Observation recorded', body: `${main}. ${result}.`, color: '#22c55e' });
  }

  engine.setUpdate((dt, t) => {
    controls.update(dt);
    if (needsRebuild) rebuild();
    if (group && state.running) group.rotation.y += Math.sin(t * 0.5) * dt * 0.008;
    updateReadouts();
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
