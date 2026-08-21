import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { makeScanMaterial } from '../core/bio3d-scan-grade.js';
import {
  Particles, skyDome, applyEnvironmentLighting,
  cellTexture, glowTexture, ringTexture,
} from '../core/bio-fx.js';

const Y_AXIS = new THREE.Vector3(0, 1, 0);

function tubeFromPoints(points, radius, material, tubular = 32, radial = 8) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p)));
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, tubular, radius, radial, false), material);
  mesh.castShadow = true;
  return mesh;
}

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-heart-lungs-stage');
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  const low = quality.tier === 'low';

  camera.position.set(0.6, 1.4, 9.2);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4, maxDistance: 16, enablePan: false, maxPolar: Math.PI * 0.72, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 0.7, 0));

  const disposeEnv = applyEnvironmentLighting(renderer, scene, { sky: '#5c2733', horizon: '#3a1520', ground: '#12060a' });
  skyDome(scene, { top: 0x34101c, mid: 0x1d0910, bottom: 0x080204 });
  scene.fog = new THREE.Fog(0x160810, 14, 34);
  basicLights(scene, { ambient: 0.42, key: 1.35 });

  // ---- Ribcage: paired curved rib tubes + sternum ----
  const boneMat = makeScanMaterial('rib-bone-pbr', 0xe6d3ba, { family: 'bone', roughness: 0.66, textureSize: low ? 128 : 256 });
  const ribcage = new THREE.Group();
  for (let i = 0; i < 7; i++) {
    const y = 2.15 - i * 0.33;
    const spread = 1.28 - i * 0.05;
    [-1, 1].forEach((side) => {
      const pts = [];
      for (let k = 0; k <= 8; k++) {
        const t = k / 8;
        const a = Math.PI * (0.16 + t * 0.68);
        pts.push([
          side * Math.sin(a) * spread,
          y - Math.cos(a * 1.4) * 0.10 + t * t * 0.22,
          -Math.cos(a) * spread * 0.62 + 0.18,
        ]);
      }
      const rib = tubeFromPoints(pts, 0.038, boneMat, 24, 6);
      ribcage.add(rib);
    });
  }
  const sternum = new THREE.Mesh(new THREE.BoxGeometry(0.30, 1.55, 0.10), boneMat);
  sternum.position.set(0, 1.45, 0.86);
  sternum.rotation.x = -0.12;
  ribcage.add(sternum);
  scene.add(ribcage);

  const root = new THREE.Group();
  scene.add(root);

  // ---- Heart: ventricle mass + atria + great vessels ----
  const heart = new THREE.Group();
  heart.position.set(0.22, 0.62, 0.28);
  const myocardium = makeScanMaterial('heart-myocardium-pbr', 0xb23330, {
    family: 'tissue', roughness: 0.42, emissive: 0x5c1210, emissiveIntensity: 0.22,
    textureSize: low ? 128 : 256,
  });
  const ventGeo = new THREE.SphereGeometry(0.56, 28, 24); ventGeo.scale(1.0, 1.14, 0.88);
  const ventricle = new THREE.Mesh(ventGeo, myocardium);
  ventricle.castShadow = true;
  heart.add(ventricle);
  const apex = new THREE.Mesh(new THREE.ConeGeometry(0.30, 0.52, 18), myocardium);
  apex.position.set(-0.06, -0.72, 0.02);
  apex.rotation.z = 0.22;
  heart.add(apex);
  const atriumMat = makeScanMaterial('heart-atria-pbr', 0x8f2626, { family: 'tissue', roughness: 0.5, textureSize: 128 });
  [[-0.30, 0.48, -0.06], [0.34, 0.44, -0.10]].forEach((p) => {
    const g = new THREE.SphereGeometry(0.24, 18, 14); g.scale(1.1, 0.85, 0.9);
    const a = new THREE.Mesh(g, atriumMat);
    a.position.set(...p);
    a.castShadow = true;
    heart.add(a);
  });
  const groove = new THREE.Mesh(new THREE.TorusGeometry(0.46, 0.035, 8, 28), atriumMat);
  groove.position.set(0, 0.30, 0);
  groove.rotation.x = Math.PI / 2.4;
  heart.add(groove);

  const vesselMat = makeScanMaterial('great-vessels-pbr', 0xa8322c, { family: 'tissue', roughness: 0.44, textureSize: 128 });
  const veinBlueMat = makeScanMaterial('vena-cava-pbr', 0x37507e, { family: 'tissue', roughness: 0.48, textureSize: 128 });
  heart.add(tubeFromPoints([[0.10, 0.55, -0.05], [0.16, 1.15, -0.10], [0.02, 1.55, -0.28], [-0.30, 1.50, -0.42], [-0.52, 1.28, -0.40]], 0.115, vesselMat, 36, 10));
  heart.add(tubeFromPoints([[-0.08, 0.55, 0.10], [-0.16, 1.05, 0.16], [-0.34, 1.30, 0.10]], 0.095, vesselMat, 28, 9));
  heart.add(tubeFromPoints([[0.42, 0.45, -0.05], [0.58, 0.95, -0.12], [0.60, 1.35, -0.18]], 0.085, veinBlueMat, 28, 9));
  heart.add(tubeFromPoints([[0.30, -0.45, -0.05], [0.38, -0.95, -0.10], [0.42, -1.45, -0.12]], 0.095, veinBlueMat, 28, 9));
  const coronary = makeScanMaterial('coronary-arteries-pbr', 0xe0473d, { family: 'tissue', roughness: 0.36, textureSize: 128 });
  for (let i = 0; i < 4; i++) {
    const a0 = -0.6 + i * 0.5;
    heart.add(tubeFromPoints(
      [[Math.cos(a0) * 0.30, 0.25, Math.sin(a0) * 0.30 + 0.18],
       [Math.cos(a0 + 0.5) * 0.48, -0.12, Math.sin(a0 + 0.5) * 0.40 + 0.20],
       [Math.cos(a0 + 0.9) * 0.40, -0.48, Math.sin(a0 + 0.9) * 0.34 + 0.16]],
      0.017, coronary, 20, 6
    ));
  }
  root.add(heart);

  // ---- Lungs with internal bronchial tree ----
  function buildLung(x) {
    const lung = new THREE.Group();
    const mat = makeScanMaterial(`lung-pleura-${x}`, 0xdb8fa6, {
      family: 'tissue', roughness: 0.55, transparent: true, opacity: 0.86,
      emissive: 0x521f31, emissiveIntensity: 0.10, textureSize: low ? 128 : 256,
    });
    const upper = new THREE.SphereGeometry(0.62, 26, 20); upper.scale(0.80, 1.15, 0.74);
    const um = new THREE.Mesh(upper, mat);
    um.position.y = 0.55;
    um.castShadow = true;
    lung.add(um);
    const lower = new THREE.SphereGeometry(0.68, 26, 20); lower.scale(0.86, 1.05, 0.80);
    const lm = new THREE.Mesh(lower, mat);
    lm.position.y = -0.42;
    lm.castShadow = true;
    lung.add(lm);
    const fissureMat = new THREE.LineBasicMaterial({ color: 0x6e1d38, transparent: true, opacity: 0.45 });
    for (let i = 0; i < 2; i++) {
      const pts = [];
      for (let k = 0; k <= 14; k++) {
        const t = k / 14;
        pts.push(new THREE.Vector3(Math.sin(t * 2.6) * 0.30, 0.05 - i * 0.16 + Math.sin(t * 3.1) * 0.05, 0.50 - t * 0.1));
      }
      const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), fissureMat);
      line.userData.noScan = true;
      lung.add(line);
    }
    const airwayMat = makeScanMaterial('bronchial-tree-pbr', 0xd9c4ae, { family: 'tissue', roughness: 0.6, textureSize: 128 });
    function branch(origin, dir, len, radius, depth) {
      const end = [origin[0] + dir[0] * len, origin[1] + dir[1] * len, origin[2] + dir[2] * len];
      const seg = tubeFromPoints([origin, [(origin[0] + end[0]) / 2 + dir[2] * 0.03, (origin[1] + end[1]) / 2, (origin[2] + end[2]) / 2], end], radius, airwayMat, 12, 6);
      lung.add(seg);
      if (depth <= 0) {
        alveoliTips.push(end);
        return;
      }
      branch(end, [dir[0] * 0.7 + (x > 0 ? 0.16 : -0.16), dir[1] * 0.55 - 0.28, dir[2] * 0.5 + 0.14], len * 0.72, radius * 0.68, depth - 1);
      branch(end, [dir[0] * 0.7, dir[1] * 0.55 - 0.30, dir[2] * 0.5 - 0.16], len * 0.70, radius * 0.66, depth - 1);
    }
    const alveoliTips = [];
    branch([x * 0.42, 1.55, 0.02], [x > 0 ? 0.30 : -0.30, -0.65, 0.05], 0.55, 0.062, low ? 1 : 2);
    const alvMat = new THREE.SpriteMaterial({
      map: glowTexture('alveolus', { inner: 'rgba(255,214,228,0.95)', mid: 'rgba(240,150,180,0.4)' }),
      transparent: true, opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending,
    });
    alvMat.userData.sharedFx = true;
    const alveoli = [];
    alveoliTips.forEach((p) => {
      const s = new THREE.Sprite(alvMat.clone());
      s.material.userData.sharedFx = true;
      s.position.set(...p);
      s.scale.setScalar(0.34);
      lung.add(s);
      alveoli.push(s);
    });
    lung.position.set(x, 0.78, -0.05);
    return { lung, meshes: [um, lm], alveoli };
  }
  const left = buildLung(-1.02);
  const right = buildLung(1.02);
  root.add(left.lung);
  root.add(right.lung);

  // Trachea with cartilage rings
  const tracheaMat = makeScanMaterial('trachea-pbr', 0xd7c3b0, { family: 'tissue', roughness: 0.58, textureSize: 128 });
  const trachea = new THREE.Mesh(new THREE.CylinderGeometry(0.105, 0.105, 1.15, 14), tracheaMat);
  trachea.position.set(0, 2.15, 0.02);
  root.add(trachea);
  for (let i = 0; i < 7; i++) {
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.108, 0.011, 6, 20), tracheaMat);
    ring.rotation.x = Math.PI / 2;
    ring.position.set(0, 1.68 + i * 0.155, 0.02);
    root.add(ring);
  }

  // Diaphragm dome
  const diaphragmGeo = new THREE.SphereGeometry(1, 36, 14, 0, Math.PI * 2, 0, Math.PI / 2);
  diaphragmGeo.scale(1.9, 0.44, 0.74);
  const diaphragm = new THREE.Mesh(
    diaphragmGeo,
    new THREE.MeshStandardMaterial({ color: 0xd96b77, roughness: 0.55, transparent: true, opacity: 0.55, side: THREE.DoubleSide })
  );
  diaphragm.position.set(0, -0.62, 0);
  diaphragm.rotation.x = Math.PI;
  root.add(diaphragm);

  // Beat pulse ring at the chest wall
  const beatRing = new THREE.Sprite(new THREE.SpriteMaterial({
    map: ringTexture('#ff6b6b'), transparent: true, opacity: 0, depthWrite: false,
    blending: THREE.AdditiveBlending,
  }));
  beatRing.material.userData.sharedFx = true;
  beatRing.position.set(0.55, 0.85, 1.15);
  scene.add(beatRing);

  // ---- Blood cells on a full circulation loop ----
  const MAX_BLOOD = low ? 90 : 150;
  const blood = new Particles(scene, {
    max: MAX_BLOOD, size: 0.17,
    texture: cellTexture({ center: '#6e0d10', edge: '#ff5252' }),
    blending: THREE.NormalBlending, opacity: 0.95,
  });
  blood.points.renderOrder = 6;
  const RED = new THREE.Color(0xff4444);
  const BLUE = new THREE.Color(0x4d6fff);
  const seeds = [];
  for (let i = 0; i < MAX_BLOOD; i++) {
    seeds.push(Math.random());
    blood.spawn(0, 0, 0, 0, 0, 0, 1e9, RED);
    blood.life[i] = 1; blood.decay[i] = 0;
  }
  // Path: body -> heart -> lungs (pick a side) -> heart -> body arc.
  function loopPoint(t, out) {
    if (t < 0.18) {
      const u = t / 0.18;
      out[0] = 0.22 - u * 0.5; out[1] = -1.2 + u * 1.7; out[2] = -0.1 + u * 0.3;
    } else if (t < 0.30) {
      const u = (t - 0.18) / 0.12;
      const side = u < 0.5 ? -1 : 1;
      const lu = (u % 0.5) * 2;
      const ang = lu * Math.PI * 2;
      out[0] = side * 1.0 + Math.cos(ang) * 0.30;
      out[1] = 0.85 + Math.sin(ang) * 0.55;
      out[2] = Math.sin(ang * 2) * 0.12;
    } else if (t < 0.42) {
      const u = (t - 0.30) / 0.12;
      out[0] = 0.5 - u * 0.3; out[1] = 1.4 - u * 0.8; out[2] = 0.1 + u * 0.15;
    } else {
      const u = (t - 0.42) / 0.58;
      const ang = u * Math.PI * 2;
      out[0] = Math.cos(ang) * 1.55;
      out[1] = 0.55 + Math.sin(ang * 2) * 0.55 - u * 0.35;
      out[2] = Math.sin(ang) * 0.85;
    }
  }
  const tmpP = [0, 0, 0];

  // ---- Physiology ----
  let activity = 0.0;
  function bpm() { return 70 + activity * 90; }
  function breathsPerMin() { return 12 + activity * 32; }
  function strokeVolumeMl() { return 70 + activity * 45; }
  function cardiacOutputLMin() { return (bpm() * strokeVolumeMl()) / 1000; }
  function tidalVolumeMl() { return 500 + activity * 1700; }
  function minuteVentilationLMin() { return (breathsPerMin() * tidalVolumeMl()) / 1000; }

  const hud = createHud(stage);
  const heartBadge = hud.badge('♥ 70 bpm', '#ef4444');
  const lungBadge = hud.badge('🫁 12 breaths/min', '#60a5fa');

  const panel = createPanel(stage, { title: 'Heart & Lungs' });
  panel.info('The heart-lung model links heart rate, stroke volume, breathing rate, tidal volume and diaphragm motion. Raise activity to see cardiac output and minute ventilation increase together.');
  panel.slider({
    label: 'Activity level', min: 0, max: 100, step: 1, value: 0,
    format: (v) => v < 25 ? 'Resting' : v < 60 ? 'Walking' : v < 85 ? 'Running' : 'Sprinting',
    onChange: (v) => { activity = v / 100; refreshBadges(); },
  });
  panel.divider();
  const bpmOut = panel.readout({ label: 'Heart rate', value: '70 bpm' });
  const breathOut = panel.readout({ label: 'Breathing rate', value: '12 /min' });
  const strokeOut = panel.readout({ label: 'Stroke volume', value: '70 mL/beat' });
  const coOut = panel.readout({ label: 'Cardiac output', value: '4.9 L/min' });
  const tidalOut = panel.readout({ label: 'Tidal volume', value: '500 mL' });
  const ventOut = panel.readout({ label: 'Minute ventilation', value: '6.0 L/min' });
  panel.readout({ label: 'Alveoli (air sacs)', value: '~480 million' });
  panel.button({ label: 'Why does exercise make you puff?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Eat now, breathe faster',
      body: 'Exercise raises ATP demand. Cardiac output = heart rate × stroke volume, and minute ventilation = breathing rate × tidal volume. The diaphragm contracts downward to expand the thoracic cavity, bringing in more oxygen and removing more CO₂.',
      color: '#ef4444',
    });
  } });

  let beatPhase = 0; let breathPhase = 0; let lastBeat = false;
  let ringT = 1;
  function refreshBadges() {
    const b = Math.round(bpm()); const br = Math.round(breathsPerMin());
    heartBadge.set(`♥ ${b} bpm`); lungBadge.set(`🫁 ${br} breaths/min`);
    bpmOut.set(`${b} bpm`); breathOut.set(`${br} /min`);
    strokeOut.set(`${Math.round(strokeVolumeMl())} mL/beat`);
    coOut.set(`${cardiacOutputLMin().toFixed(1)} L/min`);
    tidalOut.set(`${Math.round(tidalVolumeMl())} mL`);
    ventOut.set(`${minuteVentilationLMin().toFixed(1)} L/min`);
  }
  refreshBadges();

  let time = 0;
  engine.setUpdate((dt) => {
    time += dt;
    controls.update(dt);
    const b = bpm(); const br = breathsPerMin();

    beatPhase += dt * (b / 60);
    const cyc = beatPhase % 1;
    const beatStrength = cyc < 0.12 ? Math.sin((cyc / 0.12) * Math.PI) * 0.16
      : cyc < 0.18 ? 0
        : cyc < 0.30 ? Math.sin(((cyc - 0.18) / 0.12) * Math.PI) * 0.11 : 0;
    heart.scale.setScalar(1 + beatStrength);
    myocardium.emissiveIntensity = 0.22 + beatStrength * 2.2;
    if (cyc < 0.12 && !lastBeat) {
      lastBeat = true;
      ringT = 0;
      refreshBadges();
    } else if (cyc >= 0.12) lastBeat = false;
    ringT = Math.min(1, ringT + dt * 1.8);
    beatRing.material.opacity = (1 - ringT) * 0.55;
    beatRing.scale.setScalar(0.6 + ringT * 2.6);

    breathPhase += dt * (br / 60) * Math.PI * 2;
    const inflate = Math.sin(breathPhase) * 0.5 + 0.5;
    const lungScale = 0.86 + inflate * 0.42;
    left.lung.scale.set(lungScale, lungScale * 0.96, lungScale);
    right.lung.scale.set(lungScale, lungScale * 0.96, lungScale);
    left.meshes[0].material.emissiveIntensity = 0.10 + inflate * 0.28;
    const alvGlow = 0.25 + inflate * 0.55;
    left.alveoli.forEach((s) => { s.material.opacity = alvGlow; });
    right.alveoli.forEach((s) => { s.material.opacity = alvGlow; });
    trachea.position.y = 2.15 + inflate * 0.05;
    diaphragm.position.y = -0.44 - inflate * 0.34;
    diaphragm.scale.y = 1.10 - inflate * 0.40;

    const speed = (b / 70) * 0.16;
    for (let i = 0; i < MAX_BLOOD; i++) {
      seeds[i] = (seeds[i] + dt * speed) % 1;
      loopPoint(seeds[i], tmpP);
      const ix = i * 3;
      blood.pos[ix] += (tmpP[0] - blood.pos[ix]) * 0.3;
      blood.pos[ix + 1] += (tmpP[1] - blood.pos[ix + 1]) * 0.3;
      blood.pos[ix + 2] += (tmpP[2] - blood.pos[ix + 2]) * 0.3;
      const oxy = seeds[i] > 0.36 ? 1 : 0;
      blood.base[ix] += ((RED.r * oxy + BLUE.r * (1 - oxy)) - blood.base[ix]) * 0.08;
      blood.base[ix + 1] += ((RED.g * oxy + BLUE.g * (1 - oxy)) - blood.base[ix + 1]) * 0.08;
      blood.base[ix + 2] += ((RED.b * oxy + BLUE.b * (1 - oxy)) - blood.base[ix + 2]) * 0.08;
      blood.col[ix] = blood.base[ix]; blood.col[ix + 1] = blood.base[ix + 1]; blood.col[ix + 2] = blood.base[ix + 2];
    }
    blood.geo.attributes.position.needsUpdate = true;
    blood.geo.attributes.color.needsUpdate = true;
  });

  engine.start();

  return {
    dispose() {
      disposeEnv();
      blood.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
