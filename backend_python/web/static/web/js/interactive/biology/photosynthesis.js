import { THREE, createEngine } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { createRig, updateSunUniforms, outdoorEnvironment } from './butterfly/kit.js';
import { createDof } from './butterfly/dof.js';
import { evaluate, EQUATION, lightAt } from './photosynthesis/model.js';
import { createRateGraph } from './photosynthesis/graph.js';
import { buildBench } from './photosynthesis/bench.js';
import { buildLeafSection } from './photosynthesis/leaf-section.js';
import { buildChloroplast } from './photosynthesis/chloroplast.js';
import { PART_INFO, SCALE_INFO } from './photosynthesis/info.js';

const SCALES = [
  { value: 'bench', label: 'Lab bench' },
  { value: 'leaf', label: 'Inside a leaf' },
  { value: 'chloroplast', label: 'Chloroplast' },
];
const OFFSETS = { bench: new THREE.Vector3(0, 0, 0), leaf: new THREE.Vector3(4000, 0, 0), chloroplast: new THREE.Vector3(8000, 0, 0) };

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-photosynthesis-stage');
  const engine = createEngine(stage, { lite: true, shadows: true, fov: 40, near: 0.1, far: 2500, environment: false, exposure: 1.0 });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  const tier = quality.tier;

  const envBench = outdoorEnvironment(renderer, {
    zenith: '#3a4a5e', horizon: '#5d6b7c', horizonLow: '#3a3128', ground: '#1c1712', sunU: 0.75, sunV: 0.42,
    paint: (g, w, h) => {
      g.fillStyle = 'rgba(220,235,255,0.95)'; g.fillRect(w * 0.52, h * 0.18, w * 0.1, h * 0.2);
      g.fillStyle = 'rgba(255,240,210,0.9)'; g.fillRect(w * 0.05, h * 0.08, w * 0.3, h * 0.04);
      g.fillStyle = 'rgba(255,230,190,0.9)'; g.beginPath(); g.arc(w * 0.75, h * 0.42, 6, 0, Math.PI * 2); g.fill();
    },
  });
  const envMicro = outdoorEnvironment(renderer, { zenith: '#b8d6c4', horizon: '#6f9c84', horizonLow: '#2f4a3a', ground: '#14261c', sunU: 0.25, sunV: 0.12 });
  const backgrounds = { bench: new THREE.Color(0x1d2733), leaf: new THREE.Color(0x0c2420), chloroplast: new THREE.Color(0x0a1d14) };

  const worlds = {
    bench: buildBench({ tier }),
    leaf: buildLeafSection({ tier }),
    chloroplast: buildChloroplast({ tier }),
  };
  Object.entries(worlds).forEach(([k, w]) => { w.group.position.copy(OFFSETS[k]); scene.add(w.group); });
  worlds.leaf.group.scale.setScalar(1);

  const lights = {};
  lights.bench = new THREE.Group();
  lights.bench.add(new THREE.HemisphereLight(0xa8bcd4, 0x3a2c20, 1.1));
  const win = new THREE.DirectionalLight(0xb9d0ff, 1.1); win.position.set(40, 50, -50); lights.bench.add(win);
  const rimL = new THREE.DirectionalLight(0xdfe9ff, 0.7); rimL.position.set(-20, 30, 60); lights.bench.add(rimL);
  lights.leaf = new THREE.Group();
  const leafSun = new THREE.DirectionalLight(0xfff1cf, 2.6); leafSun.position.set(4000 - 10, 60, 30); leafSun.target.position.copy(OFFSETS.leaf);
  lights.leaf.add(leafSun, leafSun.target, new THREE.HemisphereLight(0xcfeede, 0x1d3324, 0.9));
  const leafFill = new THREE.DirectionalLight(0x9fd0ff, 0.5); leafFill.position.set(4000 + 40, -20, 40); leafFill.target.position.copy(OFFSETS.leaf); lights.leaf.add(leafFill, leafFill.target);
  lights.chloroplast = new THREE.Group();
  const chSun = new THREE.DirectionalLight(0xfff0c8, 2.2); chSun.position.set(8000 - 20, 60, 30); chSun.target.position.copy(OFFSETS.chloroplast);
  lights.chloroplast.add(chSun, chSun.target, new THREE.HemisphereLight(0xd8ffe0, 0x10261a, 1.0));
  Object.values(lights).forEach((g) => scene.add(g));

  const dof = createDof(engine, { aperture: 0.8, vignette: 0.28 });
  const panel = createPanel(stage, { title: 'Photosynthesis Lab' });
  const hud = createHud(stage);
  const scaleBadge = hud.badge('Lab bench', '#84cc16');
  const rateBadge = hud.badge('— bubbles/min', '#a3e635');

  const levels = { distance: 20, lamp: true, bicarb: 0.5, temperature: 25, water: 0.8, lightK: 1 };
  let scale = 'bench';
  let metrics = evaluate(levels, { submerged: true });

  const shots = {
    bench: { target: new THREE.Vector3(-5, 9, 0), r: 50, theta: 0.38, phi: 1.24, limits: { minR: 14, maxR: 140, minPhi: 0.3, maxPhi: 1.5 } },
    benchClose: { target: new THREE.Vector3(0, 6, 0), r: 20, theta: 0.3, phi: 1.3 },
    leaf: { target: new THREE.Vector3(4000, 11.5, 0), r: 58, theta: 0.5, phi: 1.34, limits: { minR: 22, maxR: 140, minPhi: 0.25, maxPhi: 2.6 } },
    chloroplast: { target: new THREE.Vector3(8000, 0, 0), r: 36, theta: 0.15, phi: 1.1, limits: { minR: 16, maxR: 110, minPhi: 0.2, maxPhi: 2.8 } },
  };
  const portals = {
    bench: () => ({ target: worlds.bench.leafPoint(), r: 4, theta: 0.3, phi: 1.3 }),
    leaf: () => ({ target: new THREE.Vector3(4000 - 4, 15, 11), r: 8, theta: 0.2, phi: 1.3 }),
  };

  const rig = createRig(camera, engine.canvas, { onTap: (ndc) => pick(ndc) });
  rig.jump(shots.bench);

  const fader = document.createElement('div');
  fader.style.cssText = 'position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .38s ease;background:radial-gradient(circle at 50% 50%, rgba(214,255,190,0.95), rgba(10,40,24,1));z-index:3';
  stage.appendChild(fader);
  let transition = null;

  function applyScale(id) {
    scale = id;
    Object.entries(worlds).forEach(([k, w]) => { w.group.visible = k === id; lights[k].visible = k === id; });
    scene.environment = id === 'bench' ? envBench.texture : envMicro.texture;
    scene.background = backgrounds[id];
    scaleBadge.set(SCALES.find((s) => s.value === id).label);
    waterNote.el.style.display = id === 'bench' ? '' : 'none';
    refresh();
  }

  function goScale(id) {
    if (id === scale || transition) return;
    const order = SCALES.map((s) => s.value);
    const deeper = order.indexOf(id) > order.indexOf(scale);
    if (deeper && portals[scale]) rig.flyTo(portals[scale](), 1.1);
    else rig.flyTo({ ...shots[scale], r: shots[scale].r * 1.8 }, 0.9);
    transition = { t: 0, phase: 0, to: id, deeper };
  }
  function tickTransition(dt) {
    if (!transition) return;
    transition.t += dt;
    if (transition.phase === 0 && transition.t > 0.85) { fader.style.opacity = '1'; transition.phase = 1; transition.t = 0; }
    else if (transition.phase === 1 && transition.t > 0.42) {
      applyScale(transition.to);
      const s = shots[transition.to];
      rig.jump({ ...s, r: transition.deeper ? s.r * 2.4 : s.r * 0.45 });
      rig.flyTo(s, 1.5);
      fader.style.opacity = '0';
      transition.phase = 2; transition.t = 0;
    } else if (transition.phase === 2 && transition.t > 0.4) transition = null;
  }

  panel.info('Plants turn light energy into food. Change the conditions and watch the rate change: count the oxygen bubbles from pondweed, then zoom into a leaf and a chloroplast to see where it happens.');
  const scaleChips = panel.chips({ label: 'Zoom level', options: SCALES, value: 'bench', onChange: (v) => goScale(v) });
  panel.section('Conditions');
  const fmtLamp = (d) => `${d} cm · ${Math.round(lightAt(d) / lightAt(10) * 100)}% light`;
  panel.slider({ label: 'Lamp distance', min: 10, max: 80, step: 1, value: levels.distance, format: fmtLamp, onChange: (v) => { levels.distance = v; changed('#facc15'); } });
  panel.toggle({ label: 'Lamp on', value: true, onChange: (v) => { levels.lamp = v; changed('#facc15'); } });
  panel.slider({ label: 'CO₂ (sodium bicarbonate)', min: 0, max: 1, step: 0.05, value: levels.bicarb, format: (v) => `${v.toFixed(2)} g / 100 mL`, onChange: (v) => { levels.bicarb = v; changed('#d4d4d8'); } });
  panel.slider({ label: 'Temperature', min: 5, max: 45, step: 1, value: levels.temperature, format: (v) => `${v} °C`, onChange: (v) => { levels.temperature = v; changed('#fb923c'); } });
  panel.slider({ label: 'Water in the soil', min: 0, max: 100, step: 1, value: 80, format: (v) => `${v}%`, onChange: (v) => { levels.water = v / 100; changed('#38bdf8'); } });
  const waterNote = panel.info('Pondweed lives under water, so water never runs short on the bench. Zoom into a land leaf to see dry soil close the stomata.');
  const graph = createRateGraph(panel.body, { max: 60, span: 120 });
  const out = panel.stats([
    { key: 'rate', label: 'Rate', value: '—' },
    { key: 'counted', label: 'Bubbles (last min)', value: '0' },
    { key: 'limit', label: 'Limiting factor', value: '—' },
    { key: 'stomata', label: 'Stomata open', value: '—' },
  ]);
  const lightOut = panel.readout({ label: 'Light at the plant', value: '' });
  const o2Out = panel.readout({ label: 'Oxygen collected', value: '' });
  const sugarOut = panel.readout({ label: 'Glucose made', value: '' });
  panel.readout({ label: 'Equation', value: EQUATION });
  panel.buttonRow([
    { label: 'Empty tube', icon: 'replay', variant: 'ghost', onClick: () => { worlds.bench.resetGas(); collected = 0; } },
    { label: 'Recipe', icon: 'menu_book', variant: 'ghost', onClick: () => showInfoCard(stage, PART_INFO.recipe) },
  ]);

  let collected = 0; let glucose = 0;
  const bubbleTimes = [];
  let simT = 0;
  worlds.bench.state.onBubble = () => { bubbleTimes.push(simT); collected += 0.012; };

  function changed(color) { refresh(); graph.mark(color); }
  function refresh() {
    metrics = evaluate(levels, { submerged: scale === 'bench' });
    levels.lightK = metrics.responses.light;
    worlds.bench.setLevels(levels);
    out.rate.set(`${Math.round(metrics.bubbles)} /min`);
    out.limit.set(metrics.limiting ? metrics.limiting.label : 'none — near maximum');
    out.stomata.set(`${Math.round(metrics.stomata * 100)}%`);
    lightOut.set(levels.lamp ? `${Math.round(metrics.ppfd)} µmol photons/m²/s (∝ 1/d²)` : 'lamp off — only dim room light');
    rateBadge.set(`${Math.round(metrics.bubbles)} bubbles/min`);
  }

  const ray = new THREE.Raycaster();
  function pick(ndc) {
    ray.setFromCamera(ndc, camera);
    let best = null; let bestD = Infinity;
    worlds[scale].hotspots().forEach((h) => {
      const p = h.pos();
      const d = ray.ray.distanceToPoint(p);
      const along = p.clone().sub(ray.ray.origin).dot(ray.ray.direction);
      if (along > 0 && d < h.r && along < bestD) { best = h; bestD = along; }
    });
    if (best && PART_INFO[best.id]) showInfoCard(stage, PART_INFO[best.id]);
    else showInfoCard(stage, SCALE_INFO[scale]);
  }

  applyScale('bench');
  rig.jump({ ...shots.bench, r: shots.bench.r * 1.25, theta: 0.7 });
  rig.flyTo(shots.bench, 2.4);

  let time = 0;
  const sunDir = new THREE.Vector3(0, 1, 0.3).normalize();
  const sunCol = new THREE.Color(0xfff0d0);
  let statAcc = 0;
  engine.setUpdate((dt) => {
    time += dt; simT += dt;
    tickTransition(dt);
    const w = worlds[scale];
    if (scale === 'bench') w.update(dt, time, metrics);
    else w.update(dt, time, metrics, levels);
    rig.update(dt);
    camera.updateMatrixWorld();
    updateSunUniforms(camera, scale === 'bench' ? new THREE.Vector3(-1, 0.3, 0) : sunDir, sunCol, scale === 'bench' ? (levels.lamp ? 1.2 * metrics.responses.light : 0.05) : 1.4);
    if (dof) dof.focus = camera.position.distanceTo(rig.target);
    glucose += dt * metrics.rate * 0.05;
    graph.push(dt, metrics.bubbles);
    statAcc += dt;
    if (statAcc > 0.25) {
      statAcc = 0;
      while (bubbleTimes.length && bubbleTimes[0] < simT - 60) bubbleTimes.shift();
      out.counted.set(String(bubbleTimes.length));
      o2Out.set(`${collected.toFixed(2)} mL in the tube`);
      sugarOut.set(scale === 'chloroplast' ? `${worlds.chloroplast.counters.glucose} molecules (6 CO₂ each)` : `${glucose.toFixed(2)} µmol (model)`);
    }
  });
  engine.start();

  return {
    dispose() {
      engine.stop();
      if (dof) dof.dispose();
      rig.dispose();
      Object.values(worlds).forEach((w) => w.dispose());
      envBench.dispose(); envMicro.dispose();
      graph.dispose(); panel.dispose(); hud.dispose(); fader.remove();
      scaleChips.el.remove();
      engine.dispose();
    },
  };
}
