import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { makeScanMaterial } from '../core/bio3d-scan-grade.js';
import { batchStaticGeometry } from '../core/bio3d-batch.js';
import {
  Particles, skyDome, applyEnvironmentLighting, lightShafts,
  glowTexture, moleculeTexture,
} from '../core/bio-fx.js';

// Limiting-factor photosynthesis model (light saturation, water stress,
// CO2 response, enzyme temperature curve) driving a cinematic 3D canopy.
const INPUTS = [
  { id: 'light', label: 'Sunlight', color: 0xffd54a, info: 'Light energy, captured by chlorophyll, powers the whole reaction. More light → faster photosynthesis — up to a limit.' },
  { id: 'water', label: 'Water (H₂O)', color: 0x4aa3ff, info: 'Roots draw water up the stem to the leaves. The hydrogen from water goes into glucose; the oxygen is released.' },
  { id: 'co2', label: 'Carbon dioxide', color: 0x9aa6b2, info: 'CO₂ enters through tiny pores called stomata. Its carbon and oxygen atoms become the backbone of the sugar molecule.' },
  { id: 'temperature', label: 'Temperature', color: 0xff9f43, info: 'Photosynthesis is enzyme-controlled. Most crop leaves work best near warm room temperature; cold slows enzymes and excessive heat damages the system.' },
];

function clamp(value, min = 0, max = 1) { return Math.max(min, Math.min(max, value)); }
function pct(value) { return `${Math.round(value * 100)}%`; }
function temperatureResponse(celsius) {
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
    formula: `rate = min(light saturation ${pct(light)}, water ${pct(water)}, CO₂ ${pct(co2)}, enzyme temp ${pct(temperature)})`,
  };
}

const COL = {
  sun: new THREE.Color(0xffe08a),
  water: new THREE.Color(0x5fb2ff),
  co2: new THREE.Color(0xcfd8e3),
  o2: new THREE.Color(0xfff8e1),
  sugar: new THREE.Color(0xffc94a),
};

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-photosynthesis-stage');
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  const low = quality.tier === 'low';

  camera.position.set(4.4, 2.6, 10.5);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 20, enablePan: false, maxPolar: Math.PI * 0.68, minPolar: Math.PI * 0.18,
  });
  controls.setTarget(new THREE.Vector3(0, 0.9, 0));

  const disposeEnv = applyEnvironmentLighting(renderer, scene, { sky: '#bfe0ff', horizon: '#7fa98c', ground: '#241a12' });
  skyDome(scene, { top: 0x0e3550, mid: 0x14503a, bottom: 0x07130c });
  scene.fog = new THREE.Fog(0x0d2f26, 18, 46);

  basicLights(scene, { ambient: 0.38, key: 1.25 });
  const sunLight = scene.children.find((o) => o.isDirectionalLight);
  if (sunLight) { sunLight.position.set(6, 11, 4); sunLight.color.set(0xfff1c4); }

  // ---- Ground: layered soil mound ----
  const soilMat = new THREE.MeshStandardMaterial({ color: 0x40301d, roughness: 1 });
  soilMat.userData.sharedFx = true;
  const mound = new THREE.Mesh(new THREE.SphereGeometry(7.5, 40, 20, 0, Math.PI * 2, 0, Math.PI / 2), soilMat);
  mound.scale.set(1, 0.34, 1);
  mound.position.y = -3.45;
  mound.receiveShadow = true;
  scene.add(mound);
  const mulch = new THREE.Mesh(
    new THREE.CircleGeometry(2.1, 36),
    new THREE.MeshStandardMaterial({ color: 0x2b1d10, roughness: 1 })
  );
  mulch.rotation.x = -Math.PI / 2;
  mulch.position.y = -3.42 + 2.55 + 0.02;
  scene.add(mulch);

  // ---- Plant: curved stem + phyllotaxis leaf spiral ----
  const plant = new THREE.Group();
  scene.add(plant);

  const stemCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(0, -0.9, 0),
    new THREE.Vector3(0.12, 0.2, 0.05),
    new THREE.Vector3(-0.08, 1.3, -0.04),
    new THREE.Vector3(0.05, 2.4, 0.03),
  ]);
  const stemMat = makeScanMaterial('photo-stem-pbr', 0x3f8f3a, { family: 'leaf', roughness: 0.62, textureSize: low ? 128 : 256 });
  const stemMesh = new THREE.Mesh(new THREE.TubeGeometry(stemCurve, 32, 0.13, 10, false), stemMat);
  stemMesh.castShadow = true;
  plant.add(stemMesh);

  function buildLeaf(scale, tilt, roll) {
    const g = new THREE.Group();
    const shape = new THREE.Shape();
    shape.moveTo(0, 0);
    shape.bezierCurveTo(1.15, 0.28, 1.42, 1.05, 0.95, 1.85);
    shape.bezierCurveTo(0.55, 2.35, 0.18, 2.5, 0, 2.55);
    shape.bezierCurveTo(-0.18, 2.5, -0.55, 2.35, -0.95, 1.85);
    shape.bezierCurveTo(-1.42, 1.05, -1.15, 0.28, 0, 0);
    const geo = new THREE.ShapeGeometry(shape, 26);
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i), y = pos.getY(i);
      const edge = Math.min(1, Math.abs(x) / 1.15);
      pos.setZ(i, Math.sin(y * 0.9) * 0.10 - edge * edge * 0.34 - Math.abs(x) * 0.06);
    }
    geo.computeVertexNormals();
    const mat = makeScanMaterial(`photo-leaf-${scale.toFixed(2)}`, 0x49a742, {
      family: 'leaf', roughness: 0.46, side: THREE.DoubleSide,
      emissive: 0x123f14, emissiveIntensity: 0.12, transparent: true, opacity: 0.96,
      textureSize: low ? 128 : 256,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.castShadow = true;
    g.add(mesh);
    const veinMat = new THREE.LineBasicMaterial({ color: 0x1d5a22, transparent: true, opacity: 0.5 });
    for (let s = -1; s <= 1; s += 2) {
      for (let i = 1; i <= 4; i++) {
        const y0 = 0.35 + i * 0.48;
        const pts = [new THREE.Vector3(0, y0, 0.02)];
        for (let k = 1; k <= 3; k++) {
          pts.push(new THREE.Vector3(s * (0.28 * k) * (1.15 - y0 / 4), y0 + 0.16 * k, 0.05 + k * 0.012));
        }
        const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), veinMat);
        line.userData.noScan = true;
        g.add(line);
      }
    }
    g.scale.setScalar(scale);
    g.rotation.set(tilt, 0, roll);
    return { group: g, mesh };
  }

  const leaves = [];
  const leafDefs = [
    { h: 0.35, ang: 0.4, scale: 0.78, tilt: -1.05 },
    { h: 0.95, ang: 2.4, scale: 0.92, tilt: -0.95 },
    { h: 1.5, ang: 4.3, scale: 1.0, tilt: -0.85 },
    { h: 2.0, ang: 0.9, scale: 0.88, tilt: -0.75 },
    { h: 2.35, ang: 3.4, scale: 0.66, tilt: -0.55 },
  ];
  const haloTex = glowTexture('warmHalo', { inner: 'rgba(190,255,150,0.95)', mid: 'rgba(120,220,90,0.35)' });
  leafDefs.forEach((def, idx) => {
    const p = stemCurve.getPoint(Math.min(0.98, def.h / 2.6));
    const { group } = buildLeaf(def.scale, def.tilt, 0);
    group.position.copy(p);
    group.rotation.y = def.ang;
    plant.add(group);
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({
      map: haloTex, transparent: true, opacity: 0, depthWrite: false,
      blending: THREE.AdditiveBlending,
    }));
    halo.material.userData.sharedFx = true;
    halo.scale.setScalar(3.4 * def.scale);
    halo.position.set(0, 1.2, 0.1);
    group.add(halo);
    leaves.push({ group, halo, phase: idx * 1.7, baseRotY: def.ang });
  });

  // Chloroplast organelles clustered on leaf surfaces.
  // One shared material (the previous build cloned it per mesh, which both cost 35 draw
  // calls and disconnected the rate-driven glow below - it animated a material nothing used).
  const chloroGeo = new THREE.SphereGeometry(0.09, 10, 8);
  chloroGeo.scale(1.5, 0.75, 0.6);
  const chloroMat = new THREE.MeshStandardMaterial({ color: 0x7bd66a, emissive: 0x3f9142, emissiveIntensity: 0.2, roughness: 0.4 });
  const chloroplasts = [];
  leaves.forEach(({ group }, li) => {
    const n = low ? 4 : 7;
    for (let i = 0; i < n; i++) {
      const m = new THREE.Mesh(chloroGeo, chloroMat);
      const t = 0.3 + (i / n) * 1.7;
      const side = i % 2 ? 1 : -1;
      m.position.set(side * (0.35 + (i % 3) * 0.22) * (1.2 - t / 3), t, 0.10 + Math.sin(t) * 0.06);
      m.rotation.z = side * 0.5;
      group.add(m);
      chloroplasts.push(m);
    }
  });

  // Stomata with guard cells on leaf undersides
  const guardMat = new THREE.MeshStandardMaterial({ color: 0x2f9e44, roughness: 0.48, emissive: 0x14532d, emissiveIntensity: 0.06 });
  const poreMat = new THREE.MeshStandardMaterial({ color: 0x052e16, roughness: 0.4, side: THREE.DoubleSide });
  const stomata = [];
  leaves.forEach(({ group }) => {
    for (let i = 0; i < 3; i++) {
      const stoma = new THREE.Group();
      stoma.position.set((i - 1) * 0.5, 0.7 + i * 0.55, 0.12);
      [-1, 1].forEach((sx) => {
        const gg = new THREE.SphereGeometry(0.05, 8, 6); gg.scale(0.75, 1.85, 0.28);
        const cell = new THREE.Mesh(gg, guardMat);
        cell.position.x = sx * 0.055;
        stoma.add(cell);
      });
      const pore = new THREE.Mesh(new THREE.CircleGeometry(0.045, 10), poreMat);
      pore.scale.set(0.4, 1, 1);
      // Pores open and shut with the stomatal aperture, so they must stay individually
      // addressable - the guard cells around them are static and get merged.
      pore.userData.noBatch = true;
      stoma.add(pore);
      group.add(stoma);
      stomata.push({ group: stoma, pore });
    }
  });

  // Each leaf carries 7 chloroplasts, 6 guard cells and 8 vein strands. Merging them inside
  // the leaf group collapses ~21 draw calls per leaf into 4 while keeping the leaf sway,
  // because the merged buffers stay children of the same swaying group.
  for (const { group } of leaves) batchStaticGeometry(group, { mergeLines: true });

  // ---- Sun disc + volumetric shafts ----
  const sunSprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTexture('sunDisc', { inner: 'rgba(255,250,225,1)', mid: 'rgba(255,214,110,0.65)', outer: 'rgba(255,180,60,0)' }),
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  sunSprite.material.userData.sharedFx = true;
  sunSprite.position.set(9, 12, -6);
  sunSprite.scale.setScalar(7);
  scene.add(sunSprite);
  const shafts = lightShafts(scene, { count: low ? 3 : 5, height: 17, width: 3.4, opacity: 0.3 });
  shafts.position.set(2.5, 0, 0);

  // ---- Particle pools (round soft sprites, one draw call each) ----
  const sunMotes = new Particles(scene, { max: low ? 50 : 90, size: 0.34, texture: glowTexture('mote') });
  const waterP = new Particles(scene, { max: low ? 40 : 70, size: 0.30, texture: glowTexture('drop', { inner: 'rgba(210,236,255,1)', mid: 'rgba(95,178,255,0.6)' }) });
  const co2P = new Particles(scene, { max: low ? 26 : 44, size: 1.05, texture: moleculeTexture('CO₂', '#aab8c6'), blending: THREE.NormalBlending, opacity: 0.95 });
  const o2P = new Particles(scene, { max: low ? 26 : 44, size: 0.95, texture: moleculeTexture('O₂', '#ffd54d'), blending: THREE.AdditiveBlending });
  const sugarP = new Particles(scene, { max: low ? 22 : 36, size: 1.0, texture: moleculeTexture('C₆H₁₂O₆', '#ffb300', { fontScale: 0.2 }), blending: THREE.NormalBlending, opacity: 0.95 });

  // Sugar behaviour: drift to the stem axis, then flow down to the roots.
  sugarP.onUpdate = (i) => {
    const ix = i * 3;
    const dx = sugarP.pos[ix];
    if (Math.abs(dx) > 0.14) sugarP.vel[ix] = -Math.sign(dx) * 0.9;
    else { sugarP.vel[ix] = 0; sugarP.vel[ix + 1] = -2.0; }
  };
  // O2 wiggle while rising
  o2P.onUpdate = (i, dt, time) => {
    o2P.vel[i * 3] = Math.sin(time * 3.1 + i * 1.7) * 0.5;
  };

  // ---- State + HUD ----
  const levels = { light: 0.8, water: 0.8, co2: 0.8, temperature: 25 };
  function rate() { return photosynthesisMetrics(levels).rate; }

  const hud = createHud(stage);
  const rateBadge = hud.badge('Photosynthesising', '#84CC16');
  const rateOut = hud.badge('Rate 74%', '#a3e635');

  const panel = createPanel(stage, { title: 'Photosynthesis Lab' });
  panel.info('Plants make glucose from CO₂ and water using light captured by chlorophyll. The live rate follows limiting-factor biology: light saturation, stomatal water stress, CO₂ response and enzyme temperature.');
  panel.slider({ label: '☀️ Sunlight', min: 0, max: 100, step: 1, value: 80, format: (v) => `${v}%`, onChange: (v) => { levels.light = v / 100; refresh(); } });
  panel.slider({ label: '💧 Water', min: 0, max: 100, step: 1, value: 80, format: (v) => `${v}%`, onChange: (v) => { levels.water = v / 100; refresh(); } });
  panel.slider({ label: '🌫️ CO₂', min: 0, max: 100, step: 1, value: 80, format: (v) => `${v}%`, onChange: (v) => { levels.co2 = v / 100; refresh(); } });
  panel.slider({ label: '🌡️ Temperature', min: 5, max: 45, step: 1, value: 25, format: (v) => `${v}°C`, onChange: (v) => { levels.temperature = v; refresh(); } });
  panel.divider();
  const limiterOut = panel.readout({ label: 'Limiting factor', value: 'Carbon dioxide' });
  const stomataOut = panel.readout({ label: 'Stomatal aperture', value: '66% aperture' });
  const formulaOut = panel.readout({ label: 'Model rule', value: photosynthesisMetrics(levels).formula });
  const sugarOut = panel.readout({ label: 'Glucose made', value: '0 glucose units' });
  const o2Out = panel.readout({ label: 'O₂ released', value: '0 O₂ units' });
  panel.button({ label: 'What is the recipe?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'The recipe of life',
      body: '6 CO₂ + 6 H₂O + light energy → C₆H₁₂O₆ + 6 O₂. The 3D readout uses a limiting-factor model: a shortage in light, water, CO₂ or suitable temperature caps the whole reaction even when the other inputs are high.',
      color: '#84CC16',
    });
  } });

  let sugarTotal = 0, o2Total = 0;

  function refresh() {
    const metrics = photosynthesisMetrics(levels);
    const r = metrics.rate;
    chloroMat.emissiveIntensity = 0.15 + r * 1.1;
    leaves.forEach(({ halo }) => { halo.material.opacity = r * 0.34; });
    shafts.userData.material.opacity = 0.06 + levels.light * 0.34;
    sunSprite.material.opacity = 0.35 + levels.light * 0.65;
    const aperture = clamp(Math.min(levels.water, 1 - levels.co2 * 0.18));
    stomata.forEach(({ pore }) => { pore.scale.x = 0.22 + aperture * 1.15; });
    rateOut.set(`Rate ${Math.round(r * 100)}%`);
    limiterOut.set(metrics.limiting);
    formulaOut.set(metrics.formula);
    stomataOut.set(`${Math.round(aperture * 100)}% aperture`);
    if (r < 0.05) rateBadge.set('Leaf is idle');
    else if (r < 0.4) rateBadge.set('Slow photosynthesis');
    else rateBadge.set('Photosynthesising');
  }
  refresh();

  let spawnAcc = 0;
  let time = 0;

  engine.setUpdate((dt) => {
    time += dt;
    controls.update(dt);
    const r = rate();

    // gentle leaf sway
    leaves.forEach(({ group, phase, baseRotY }) => {
      group.rotation.y = baseRotY + Math.sin(time * 0.7 + phase) * 0.05;
      group.rotation.z = Math.sin(time * 0.5 + phase * 1.3) * 0.03;
    });
    shafts.rotation.y += dt * 0.03;
    sunSprite.material.rotation += dt * 0.02;

    spawnAcc += dt;
    if (spawnAcc > 0.055) {
      spawnAcc = 0;
      const burst = Math.max(1, Math.round(r * 4));
      if (r > 0.02 && levels.light > 0.03) {
        for (let i = 0; i < burst; i++) {
          sunMotes.spawn(2 + Math.random() * 5, 6 + Math.random() * 4, -1 + Math.random() * 3,
            -1.4 - Math.random(), -2.2 - levels.light * 1.6, 0.4, 2.4, COL.sun);
        }
      }
      if (r > 0.02 && levels.water > 0.14) {
        for (let i = 0; i < burst; i++) {
          waterP.spawn((Math.random() - 0.5) * 0.12, -3.2, (Math.random() - 0.5) * 0.12,
            0, 2.6 + levels.water * 1.6, 0, 2.2, COL.water);
        }
      }
      if (r > 0.02 && levels.co2 > 0.05) {
        for (let i = 0; i < burst; i++) {
          const side = Math.random() < 0.5 ? -1 : 1;
          co2P.spawn(side * 5.5, 0.6 + Math.random() * 2.6, (Math.random() - 0.5) * 2.4,
            -side * (1.1 + levels.co2 * 1.2), 0.12, 0, 3.4, COL.co2);
        }
      }
      const outs = Math.round(r * 4);
      for (let i = 0; i < outs; i++) {
        const lx = (Math.random() - 0.5) * 2.6;
        const ly = 1.2 + Math.random() * 2.2;
        o2P.spawn(lx, ly, 0.3, (Math.random() - 0.5) * 0.3, 1.1 + r, 0.1, 2.6, COL.o2);
        o2Total += 6;
        sugarP.spawn(lx * 0.6, ly - 0.2, 0.25, 0, -0.3, 0, 3.2, COL.sugar);
        sugarTotal += 1;
      }
      o2Out.set(`${o2Total} O₂ units`);
      sugarOut.set(`${sugarTotal} glucose units`);
    }

    sunMotes.update(dt, time);
    waterP.update(dt, time);
    co2P.update(dt, time);
    o2P.update(dt, time);
    sugarP.update(dt, time);

    const shimmer = 0.6 + Math.sin(time * 3) * 0.25;
    chloroMat.emissiveIntensity = (0.15 + r * 1.1) * shimmer;
  });

  engine.start();

  return {
    dispose() {
      disposeEnv();
      [sunMotes, waterP, co2P, o2P, sugarP].forEach((p) => p.dispose());
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
