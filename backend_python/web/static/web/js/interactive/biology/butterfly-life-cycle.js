import { THREE, createEngine } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { createRig, updateSunUniforms } from './butterfly/kit.js';
import { buildEnvironment, SUN_DIR } from './butterfly/environment.js';
import { buildPlant } from './butterfly/plant.js';
import { buildCaterpillar } from './butterfly/caterpillar.js';
import { buildAdult } from './butterfly/adult.js';
import { STAGES, buildEgg, buildChrysalis } from './butterfly/stages.js';
import { createDirector } from './butterfly/director.js';
import { createDof } from './butterfly/dof.js';

const ICONS = { egg: 'egg', caterpillar: 'pest_control', chrysalis: 'spa', adult: 'flutter_dash' };
const PART_INFO = {
  flower: { title: 'Aak flower (Calotropis)', color: '#c4b5fd', body: 'The crown-shaped flowers of aak (Calotropis) hold nectar deep inside a ring of five fleshy lobes called the corona. Butterflies uncoil their proboscis to reach it. Aak grows wild along roads and dry fields across Nepal’s Terai and inner valleys.' },
  leaf: { title: 'Host-plant leaf', color: '#86efac', body: 'Thick, waxy, grey-green leaves full of bitter milky latex. Most animals avoid them, but plain tiger caterpillars eat them and store the poisons (cardenolides) in their bodies, so birds learn to leave them alone. See the bite marks along the edge: a caterpillar has been feeding here.' },
};

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-butterfly-stage');
  const engine = createEngine(stage, { lite: true, shadows: true, fov: 38, near: 0.05, far: 3000, environment: false, exposure: 1.0 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const tier = quality.tier;

  const env = buildEnvironment(engine);
  const dof = createDof(engine, { aperture: 1 });
  const plant = buildPlant({ tier });
  scene.add(plant.group);
  const egg = buildEgg({ tier });
  const cat = buildCaterpillar({ tier });
  const chry = buildChrysalis({ tier });
  const adult = buildAdult({ tier, antialias: quality.antialias });

  const panel = createPanel(stage, { title: 'Butterfly Life Cycle' });
  const hud = createHud(stage);
  const stageBadge = hud.badge('Adult butterfly', STAGES[3].color);
  const dayBadge = hud.badge('Day 30', '#fbbf24');

  let currentStage = 'adult';
  let readouts = null;
  let slider = null;
  let playBtn = null;
  let stageBtns = [];
  let instar = 0;

  function reflectStage(id) {
    currentStage = id;
    const idx = STAGES.findIndex((s) => s.id === id);
    const s = STAGES[idx];
    stageBadge.set(s.name);
    stageBadge.el.style.setProperty('--ix-hud-color', s.color);
    if (slider) slider.set(idx);
    stageBtns.forEach((b, i) => b.el.classList.toggle('is-on', i === idx));
    if (readouts) {
      readouts.duration.set(s.duration); readouts.days.set(s.days); readouts.size.set(s.size);
      readouts.food.set(s.food); readouts.process.set(s.process);
    }
    if (emergeBtn) emergeBtn.el.style.display = id === 'chrysalis' ? '' : 'none';
    if (flyBtn) flyBtn.el.style.display = id === 'adult' ? '' : 'none';
  }
  function setDay(d) {
    const day = Math.floor(d);
    dayBadge.set(instar ? `Day ${day} · instar ${instar}` : `Day ${day}`);
  }

  const director = createDirector({
    plant, egg, cat, chry, adult, scene, tier,
    rig: null,
    onStatus: (s) => {
      if (s.stage) reflectStage(s.stage);
      if (s.instar !== undefined) instar = s.instar;
      if (s.day !== undefined) setDay(s.day);
      if (s.done && playBtn) { playBtn.setLabel('Watch the whole cycle'); playBtn.el.querySelector('.material-symbols-outlined').textContent = 'play_circle'; instar = 0; setDay(30); }
    },
  });

  const rig = createRig(camera, engine.canvas, { minY: 1.5, onTap: (ndc) => pick(ndc) });

  panel.info('A plain tiger (Danaus chrysippus) grows up on an aak plant. It lives four completely different lives — complete metamorphosis. Tap a stage, or watch the whole month as a time-lapse.');
  slider = panel.slider({
    label: 'Stage', min: 0, max: 3, step: 1, value: 3,
    format: (v) => STAGES[v].name,
    onChange: (v) => goStage(STAGES[v].id),
  });
  const rowA = panel.buttonRow(STAGES.slice(0, 2).map((s) => ({ label: s.name, icon: ICONS[s.id], variant: 'ghost', onClick: () => { goStage(s.id); showCard(s.id); } })));
  const rowB = panel.buttonRow(STAGES.slice(2).map((s) => ({ label: s.id === 'adult' ? 'Adult' : s.name, icon: ICONS[s.id], variant: 'ghost', onClick: () => { goStage(s.id); showCard(s.id); } })));
  stageBtns = [...rowA, ...rowB];
  playBtn = panel.button({ label: 'Watch the whole cycle', icon: 'play_circle', onClick: () => {
    if (director.state.cycle) {
      director.stopCycle(); playBtn.setLabel('Watch the whole cycle'); playBtn.el.querySelector('.material-symbols-outlined').textContent = 'play_circle'; instar = 0;
    } else {
      director.playCycle(); playBtn.setLabel('Stop time-lapse'); playBtn.el.querySelector('.material-symbols-outlined').textContent = 'stop_circle';
    }
  } });
  const emergeBtn = panel.button({ label: 'Watch it emerge', icon: 'auto_awesome', variant: 'ghost', onClick: () => { stopCycleUi(); director.emerge(); } });
  const flyBtn = panel.button({ label: 'Take flight', icon: 'flight', variant: 'ghost', onClick: () => director.takeFlight() });
  panel.button({ label: 'See the whole plant', icon: 'zoom_out_map', variant: 'ghost', onClick: () => director.overview() });
  panel.divider();
  readouts = {
    duration: panel.readout({ label: 'Stage lasts', value: '' }),
    days: panel.readout({ label: 'When', value: '' }),
    size: panel.readout({ label: 'Size', value: '' }),
    food: panel.readout({ label: 'Food', value: '' }),
    process: panel.readout({ label: 'Main job', value: '' }),
  };
  panel.readout({ label: 'Whole cycle', value: '≈ 4–5 weeks egg to adult (warm season)' });
  panel.readout({ label: 'Type', value: 'complete metamorphosis' });
  panel.toggle({ label: 'Breeze', value: true, onChange: (v) => { wind = v ? 1 : 0; } });

  function stopCycleUi() {
    if (director.state.cycle) director.stopCycle();
    playBtn.setLabel('Watch the whole cycle'); playBtn.el.querySelector('.material-symbols-outlined').textContent = 'play_circle';
    instar = 0;
  }
  function goStage(id) {
    stopCycleUi();
    director.showStage(id);
    reflectStage(id);
    const s = STAGES.find((x) => x.id === id);
    setDay(id === 'egg' ? 1 : id === 'caterpillar' ? 15 : id === 'chrysalis' ? 21 : 30);
    return s;
  }
  function showCard(id, force) {
    if (!force && stage.clientWidth < 520) return;
    const s = STAGES.find((x) => x.id === id);
    showInfoCard(stage, { title: s.name, body: s.info, color: s.color });
  }

  const ray = new THREE.Raycaster();
  function pick(ndc) {
    ray.setFromCamera(ndc, camera);
    let best = null; let bestD = Infinity;
    director.hotspots().forEach((h) => {
      if (!h.visible) return;
      const p = h.pos();
      const d = ray.ray.distanceToPoint(p);
      const along = p.clone().sub(ray.ray.origin).dot(ray.ray.direction);
      if (along > 0 && d < h.r && along < bestD) { best = h; bestD = along; }
    });
    if (!best) return;
    if (PART_INFO[best.id]) showInfoCard(stage, PART_INFO[best.id]);
    else showCard(best.id, true);
  }

  director.bindRig(rig);
  reflectStage('adult');
  setDay(30);
  rig.jump(director.shot('overview'));
  director.showStage('adult');

  let wind = 1;
  let time = 0;
  const sunColor = new THREE.Color(0xfff0d6);
  let shadowTick = 0;
  engine.renderer.shadowMap.autoUpdate = false;
  engine.renderer.shadowMap.needsUpdate = true;
  engine.setUpdate((dt) => {
    if ((shadowTick++ & 1) === 0) engine.renderer.shadowMap.needsUpdate = true;
    time += dt;
    plant.update(time, wind);
    director.update(dt, time);
    env.update(time);
    rig.update(dt);
    if (dof) dof.focus = camera.position.distanceTo(rig.target);
    camera.updateMatrixWorld();
    updateSunUniforms(camera, SUN_DIR, sunColor, 1.6);
  });
  engine.start();

  return {
    dispose() {
      engine.stop();
      if (dof) dof.dispose();
      rig.dispose();
      director.dispose();
      env.dispose(); plant.dispose(); adult.dispose(); chry.dispose();
      panel.dispose(); hud.dispose();
      engine.dispose();
    },
  };
}
