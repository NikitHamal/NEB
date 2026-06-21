import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { addScanGradeEnhancement, makeScanMaterial } from '../core/bio3d-scan-grade.js';

// Inputs are modelled with saturation/limiting-factor curves rather than a toy linear minimum.
const INPUTS = [
  { id: 'light', label: 'Sunlight', color: 0xffd54a, emoji: '☀️', info: 'Light energy, captured by chlorophyll, powers the whole reaction. More light → faster photosynthesis — up to a limit.' },
  { id: 'water', label: 'Water (H₂O)', color: 0x4aa3ff, emoji: '💧', info: 'Roots draw water up the stem to the leaves. The hydrogen from water goes into glucose; the oxygen is released.' },
  { id: 'co2', label: 'Carbon dioxide', color: 0x9aa6b2, emoji: '🌫️', info: 'CO₂ enters through tiny pores called stomata. Its carbon and oxygen atoms become the backbone of the sugar molecule.' },
  { id: 'temperature', label: 'Temperature', color: 0xff9f43, emoji: '🌡️', info: 'Photosynthesis is enzyme-controlled. Most crop leaves work best near warm room temperature; cold slows enzymes and excessive heat damages the system.' },
];

function clamp(value, min = 0, max = 1) { return Math.max(min, Math.min(max, value)); }
function pct(value) { return `${Math.round(value * 100)}%`; }
function temperatureResponse(celsius) {
  // Broad teaching model: enzyme rate peaks around 25 C and falls on both sides.
  return clamp(1 - ((celsius - 25) / 18) ** 2);
}
function photosynthesisMetrics(levels) {
  const light = clamp(1 - Math.exp(-3.0 * levels.light));
  const water = clamp((levels.water - 0.12) / 0.78);
  const co2 = clamp(levels.co2 / (0.28 + levels.co2));
  const temperature = temperatureResponse(levels.temperature);
  const responses = { light, water, co2, temperature };
  const limiting = Object.entries(responses).sort((a, b) => a[1] - b[1])[0];
  return {
    rate: clamp(limiting[1]),
    limiting: INPUTS.find((x) => x.id === limiting[0])?.label || limiting[0],
    responses,
    formula: `rate = min(light saturation ${pct(light)}, water ${pct(water)}, CO₂ ${pct(co2)}, enzyme temp ${pct(temperature)})`,
  };
}


export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-photosynthesis-stage');
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(14, quality.segments / 2);

  camera.position.set(0, 1.5, 11);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 20, enablePan: false, maxPolar: Math.PI * 0.7, minPolar: Math.PI * 0.15,
  });
  controls.setTarget(new THREE.Vector3(0, 0.5, 0));

  scene.background = new THREE.Color(0x0b1f14);
  scene.fog = new THREE.Fog(0x0b1f14, 16, 32);
  basicLights(scene, { ambient: 0.45, key: 1.4 });
  const sunFill = new THREE.DirectionalLight(0xfff0b0, 0.5); sunFill.position.set(4, 8, 4); scene.add(sunFill);

  // Ground (soil)
  const soil = new THREE.Mesh(
    new THREE.CircleGeometry(8, 48),
    new THREE.MeshStandardMaterial({ color: 0x3a2818, roughness: 1 })
  );
  soil.rotation.x = -Math.PI / 2; soil.position.y = -3.4; soil.receiveShadow = true; scene.add(soil);

  // ---- The leaf: a curved paddle ----
  const leaf = new THREE.Group(); scene.add(leaf);
  const leafMat = makeScanMaterial('photosynthesis-leaf-scan-surface', 0x4caf50, {
    family: 'leaf', roughness: 0.50, side: THREE.DoubleSide,
    emissive: 0x1b5e20, emissiveIntensity: 0.15, transparent: true, opacity: 0.94,
    textureSize: quality.tier === 'low' ? 128 : 256,
  });
  const leafShape = new THREE.Shape();
  leafShape.moveTo(0, 0);
  leafShape.bezierCurveTo(2.4, 0.7, 2.6, 2.6, 0, 3.3);
  leafShape.bezierCurveTo(-2.6, 2.6, -2.4, 0.7, 0, 0);
  const leafGeo = new THREE.ShapeGeometry(leafShape, 48);
  leafGeo.scale(1, 1, 1);
  // give it a gentle curve by displacing z
  const pos = leafGeo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i);
    pos.setZ(i, Math.sin(x * 0.6) * 0.25 + (y * 0.05));
  }
  leafGeo.computeVertexNormals();
  const leafMesh = new THREE.Mesh(leafGeo, leafMat);
  leafMesh.castShadow = true; leaf.add(leafMesh);

  // Stem
  const stem = new THREE.Mesh(
    new THREE.CylinderGeometry(0.12, 0.16, 3.2, 12),
    new THREE.MeshStandardMaterial({ color: 0x2e7d32, roughness: 0.7 })
  );
  stem.position.set(0, -1.8, 0); stem.castShadow = true; leaf.add(stem);

  // Veins on the leaf
  const veinMat = new THREE.LineBasicMaterial({ color: 0x2e7d32, transparent: true, opacity: 0.6 });
  const midVein = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(0, 0.05, 0.02), new THREE.Vector3(0, 3.25, 0.05)]);
  leaf.add(new THREE.Line(midVein, veinMat));
  for (let i = 1; i <= 5; i++) {
    const y = 0.4 + i * 0.5;
    const w = 2.0 - i * 0.25;
    const side = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, y, 0.03), new THREE.Vector3(w, y + 0.3, 0.05)]);
    leaf.add(new THREE.Line(side, veinMat));
    const side2 = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, y, 0.03), new THREE.Vector3(-w, y + 0.3, 0.05)]);
    leaf.add(new THREE.Line(side2, veinMat));
  }

  // ---- Chloroplasts and stomata: visible subcellular structures on the leaf ----
  const chloroplasts = [];
  const stomata = [];
  const chloroGeo = new THREE.SphereGeometry(0.13, 12, 12);
  for (let i = 0; i < 16; i++) {
    const t = Math.random();
    const y = 0.4 + t * 2.6;
    const maxW = 2.3 - t * 1.6;
    const x = (Math.random() - 0.5) * 2 * maxW;
    const mat = new THREE.MeshStandardMaterial({
      color: 0x66bb6a, emissive: 0x66bb6a, emissiveIntensity: 0.0, roughness: 0.4,
    });
    const m = new THREE.Mesh(chloroGeo, mat);
    m.position.set(x, y, 0.06 + Math.sin(x * 0.6) * 0.2);
    leaf.add(m); chloroplasts.push(m);
  }

  // Stomata with paired guard cells; aperture responds to water stress and CO2 demand.
  const guardMat = new THREE.MeshStandardMaterial({ color: 0x2f9e44, roughness: 0.48, emissive: 0x14532d, emissiveIntensity: 0.06 });
  const poreMat = new THREE.MeshStandardMaterial({ color: 0x052e16, roughness: 0.4, side: THREE.DoubleSide });
  for (let i = 0; i < 10; i++) {
    const t = (i + 0.5) / 10;
    const y = 0.45 + t * 2.45;
    const side = i % 2 === 0 ? -1 : 1;
    const x = side * (0.38 + (i % 5) * 0.24);
    const stoma = new THREE.Group();
    stoma.position.set(x, y, 0.105 + Math.sin(x * 0.6) * 0.2);
    stoma.rotation.z = side * 0.32;
    [-1, 1].forEach((sx) => {
      const g = new THREE.SphereGeometry(0.055, 10, 8); g.scale(0.75, 1.85, 0.28);
      const cell = new THREE.Mesh(g, guardMat);
      cell.position.x = sx * 0.055;
      stoma.add(cell);
    });
    const pore = new THREE.Mesh(new THREE.CircleGeometry(0.045, 12), poreMat);
    pore.scale.set(0.38, 1.0, 1);
    stoma.add(pore);
    leaf.add(stoma);
    stomata.push({ group: stoma, pore });
  }
  addScanGradeEnhancement(leaf, { kind: 'photosynthesis', quality, seed: 'photosynthesis-leaf', plaque: false });

  // ---- Particle systems: input atoms drifting in, output molecules drifting out ----
  const MAX_P = 180;
  function makeParticles(color, size) {
    const positions = new Float32Array(MAX_P * 3);
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.PointsMaterial({ color, size, transparent: true, opacity: 0.85, depthWrite: false });
    const pts = new THREE.Points(geo, mat);
    scene.add(pts);
    return { pts, geo, positions, velocities: new Float32Array(MAX_P * 3), life: new Float32Array(MAX_P), count: 0 };
  }
  const lightP = makeParticles(0xffe082, 0.18);     // sunlight motes from above
  const waterP = makeParticles(0x64b5f6, 0.16);     // water up the stem
  const co2P = makeParticles(0xb0bec5, 0.16);       // CO2 from sides
  const o2P = makeParticles(0xfffde7, 0.18);        // oxygen out
  const sugarP = makeParticles(0xffd54a, 0.16);     // glucose out

  // each particle pool owns its own velocity and lifetime arrays; no cross-pool state corruption.
  function spawn(pool, x, y, z, vx, vy, vz) {
    const i = pool.count;
    if (i >= MAX_P) return;
    pool.positions[i * 3] = x; pool.positions[i * 3 + 1] = y; pool.positions[i * 3 + 2] = z;
    pool.velocities[i * 3] = vx; pool.velocities[i * 3 + 1] = vy; pool.velocities[i * 3 + 2] = vz;
    pool.life[i] = 1; pool.count++;
  }
  function updatePool(pool, dt, onArrive) {
    let w = 0;
    for (let i = 0; i < pool.count; i++) {
      pool.life[i] -= dt * 0.5;
      if (pool.life[i] <= 0) { if (onArrive) onArrive(i); continue; }
      pool.positions[i * 3] += pool.velocities[i * 3] * dt;
      pool.positions[i * 3 + 1] += pool.velocities[i * 3 + 1] * dt;
      pool.positions[i * 3 + 2] += pool.velocities[i * 3 + 2] * dt;
      // shift into the write slot
      pool.positions[w * 3] = pool.positions[i * 3];
      pool.positions[w * 3 + 1] = pool.positions[i * 3 + 1];
      pool.positions[w * 3 + 2] = pool.positions[i * 3 + 2];
      pool.velocities[w * 3] = pool.velocities[i * 3]; pool.velocities[w * 3 + 1] = pool.velocities[i * 3 + 1]; pool.velocities[w * 3 + 2] = pool.velocities[i * 3 + 2];
      pool.life[w] = pool.life[i]; w++;
    }
    pool.count = w;
    pool.geo.setDrawRange(0, w);
    pool.geo.attributes.position.needsUpdate = true;
  }

  // ---- State + HUD ----
  const levels = { light: 0.8, water: 0.8, co2: 0.8, temperature: 25 };
  function rate() { return photosynthesisMetrics(levels).rate; }

  const hud = createHud(stage);
  const rateBadge = hud.badge('Photosynthesising', '#84CC16');
  const rateOut = hud.badge('Rate 74%', '#a3e635');
  let limiterOut = null;
  let formulaOut = null;
  let stomataOut = null;

  function refresh() {
    const metrics = photosynthesisMetrics(levels);
    const r = metrics.rate;
    chloroplasts.forEach((c) => { c.material.emissiveIntensity = r * 0.9; });
    leafMat.emissiveIntensity = 0.1 + r * 0.4;
    const aperture = clamp(Math.min(levels.water, 1 - levels.co2 * 0.18));
    stomata.forEach(({ group, pore }, i) => {
      const open = 0.22 + aperture * 1.15;
      pore.scale.x = open;
      group.scale.setScalar(0.9 + r * 0.45 + Math.sin(i) * 0.015);
    });
    rateOut.set(`Rate ${Math.round(r * 100)}%`);
    if (limiterOut) limiterOut.set(metrics.limiting);
    if (formulaOut) formulaOut.set(metrics.formula);
    if (stomataOut) stomataOut.set(`${Math.round(aperture * 100)}% aperture`);
    if (r < 0.05) rateBadge.set('Leaf is idle');
    else if (r < 0.4) rateBadge.set('Slow photosynthesis');
    else rateBadge.set('Photosynthesising');
  }

  const panel = createPanel(stage, { title: 'Photosynthesis Lab' });
  panel.info('Plants make glucose from CO₂ and water using light captured by chlorophyll. The live rate now follows limiting-factor biology with light saturation, stomatal water stress, CO₂ response and enzyme temperature.');
  panel.slider({
    label: '☀️ Sunlight', min: 0, max: 100, step: 1, value: 80,
    format: (v) => `${v}%`,
    onChange: (v) => { levels.light = v / 100; refresh(); },
  });
  panel.slider({
    label: '💧 Water', min: 0, max: 100, step: 1, value: 80,
    format: (v) => `${v}%`,
    onChange: (v) => { levels.water = v / 100; refresh(); },
  });
  panel.slider({
    label: '🌫️ CO₂', min: 0, max: 100, step: 1, value: 80,
    format: (v) => `${v}%`,
    onChange: (v) => { levels.co2 = v / 100; refresh(); },
  });
  panel.slider({
    label: '🌡️ Temperature', min: 5, max: 45, step: 1, value: 25,
    format: (v) => `${v}°C`,
    onChange: (v) => { levels.temperature = v; refresh(); },
  });
  panel.divider();
  limiterOut = panel.readout({ label: 'Limiting factor', value: 'Carbon dioxide' });
  stomataOut = panel.readout({ label: 'Stomatal aperture', value: '66% aperture' });
  formulaOut = panel.readout({ label: 'Model rule', value: photosynthesisMetrics(levels).formula });
  const sugarOut = panel.readout({ label: 'Glucose made', value: '0 glucose units' });
  const o2Out = panel.readout({ label: 'O₂ released', value: '0 O₂ units' });
  panel.button({ label: 'What is the recipe?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'The recipe of life',
      body: '6 CO₂ + 6 H₂O + light energy → C₆H₁₂O₆ + 6 O₂. The 3D readout uses a limiting-factor model: a shortage in light, water, CO₂ or suitable temperature caps the whole reaction even when the other inputs are high.',
      color: '#84CC16',
    });
  } });

  refresh();

  // Spawn timers
  let sugarTotal = 0, o2Total = 0;
  let spawnAcc = 0;

  engine.setUpdate((dt) => {
    controls.update(dt);
    const r = rate();
    spawnAcc += dt;
    if (spawnAcc > 0.05) {
      spawnAcc = 0;
      const burst = Math.max(1, Math.round(r * 5));
      // sunlight from above toward leaf
      for (let i = 0; i < burst && r > 0.02; i++) {
        spawn(lightP, (Math.random() - 0.5) * 4, 5, (Math.random() - 0.5) * 2,
          (Math.random() - 0.5) * 0.3, -3 * (0.6 + levels.light), 0);
      }
      // water up the stem
      for (let i = 0; i < burst && r > 0.02; i++) {
        spawn(waterP, (Math.random() - 0.5) * 0.2, -3, 0,
          (Math.random() - 0.5) * 0.1, 3 * (0.6 + levels.water), 0);
      }
      // CO2 drifting in from sides
      for (let i = 0; i < burst && r > 0.02; i++) {
        const side = Math.random() < 0.5 ? -1 : 1;
        spawn(co2P, side * 4, 0.5 + Math.random() * 2.5, (Math.random() - 0.5) * 2,
          -side * (0.8 + levels.co2), 0.1, 0);
      }
      // outputs: O2 and sugar leaving the leaf surface
      const outs = Math.round(r * 6);
      for (let i = 0; i < outs; i++) {
        spawn(o2P, (Math.random() - 0.5) * 3, 1.5 + Math.random() * 1.5, 0.2,
          (Math.random() - 0.5) * 0.4, 1.2, 0);
        o2Total += 6;
      }
      for (let i = 0; i < outs; i++) {
        spawn(sugarP, (Math.random() - 0.5) * 2, 0.6 + Math.random() * 1.8, 0.2,
          (Math.random() - 0.5) * 0.2, -0.4, 0);
        sugarTotal += 1;
      }
      o2Out.set(`${o2Total} O₂ units`); sugarOut.set(`${sugarTotal} glucose units`);
    }
    updatePool(lightP, dt);
    updatePool(waterP, dt);
    updatePool(co2P, dt);
    updatePool(o2P, dt);
    updatePool(sugarP, dt);

    // chloroplast shimmer
    chloroplasts.forEach((c, i) => {
      const t = performance.now() * 0.001;
      c.material.emissiveIntensity = r * (0.6 + Math.sin(t * 3 + i) * 0.25);
    });
  });

  engine.start();

  return {
    dispose() {
      [lightP, waterP, co2P, o2P, sugarP].forEach((p) => { p.geo.dispose(); p.pts.material.dispose(); });
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
