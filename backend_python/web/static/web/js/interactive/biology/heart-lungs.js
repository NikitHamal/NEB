import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

export default function init(stage) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(14, quality.segments / 2);

  camera.position.set(0, 1, 9);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4, maxDistance: 16, enablePan: false, maxPolar: Math.PI * 0.72, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 0.6, 0));

  scene.background = new THREE.Color(0x140a14);
  scene.fog = new THREE.Fog(0x140a14, 14, 30);
  basicLights(scene, { ambient: 0.5, key: 1.5 });

  // Ribcage: faint arcs
  const ribMat = new THREE.MeshStandardMaterial({ color: 0xe8d9c5, transparent: true, opacity: 0.18, roughness: 0.6 });
  const ribcage = new THREE.Group();
  for (let i = 0; i < 8; i++) {
    const rib = new THREE.Mesh(new THREE.TorusGeometry(1.4 - i * 0.04, 0.05, 8, 28, Math.PI * 1.15), ribMat);
    rib.position.set(0, 2.2 - i * 0.32, 0); rib.rotation.x = Math.PI / 2; rib.rotation.z = -Math.PI * 0.575;
    ribcage.add(rib);
  }
  scene.add(ribcage);

  const root = new THREE.Group(); scene.add(root);

  // ---- Heart (4 chambers simplified) ----
  const heart = new THREE.Group();
  const heartMat = new THREE.MeshStandardMaterial({ color: 0xc0392b, roughness: 0.4, emissive: 0x7b1e12, emissiveIntensity: 0.2 });
  const heartGeo = new THREE.SphereGeometry(0.55, 24, 24); heartGeo.scale(1, 1.1, 0.9);
  const heartMesh = new THREE.Mesh(heartGeo, heartMat);
  heartMesh.castShadow = true; heart.add(heartMesh);
  // apex nub
  const apex = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.5, 16), heartMat);
  apex.position.set(0, -0.65, 0); apex.rotation.x = Math.PI; heart.add(apex);
  // aorta + pulmonary trunk
  const vesselMat = new THREE.MeshStandardMaterial({ color: 0x992b22, roughness: 0.5 });
  const aorta = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 1.1, 12), vesselMat);
  aorta.position.set(0.15, 0.75, 0); aorta.rotation.z = 0.2; heart.add(aorta);
  heart.position.set(0.2, 0.5, 0.2);
  root.add(heart);

  // ---- Lungs (left + right), each a group we can scale to "inflate" ----
  function makeLung(x) {
    const lung = new THREE.Group();
    const mat = new THREE.MeshStandardMaterial({ color: 0xe08aa8, roughness: 0.58, transparent: true, opacity: 0.88,
      emissive: 0x6a2a40, emissiveIntensity: 0.1 });
    const geo = new THREE.SphereGeometry(0.75, 32, 24); geo.scale(0.82, 1.54, 0.78);
    const mesh = new THREE.Mesh(geo, mat); mesh.castShadow = true; lung.add(mesh);
    // lobes/fissures as darker curved bands on the pleural surface
    const fissureMat = new THREE.LineBasicMaterial({ color: 0x7f1d3a, transparent: true, opacity: 0.42 });
    for (let i = 0; i < 3; i++) {
      const pts = [];
      for (let k = 0; k < 18; k++) {
        const t = -0.65 + k * 0.075;
        pts.push(new THREE.Vector3(Math.sin(t * 2.1) * 0.18, 0.36 - i * 0.42 + t * 0.25, 0.63));
      }
      lung.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), fissureMat));
    }
    lung.position.set(x, 0.7, 0);
    return { lung, mesh };
  }
  function cylBetween(a, b, r, material, radial = 10) {
    const va = new THREE.Vector3(...a); const vb = new THREE.Vector3(...b);
    const mid = va.clone().add(vb).multiplyScalar(0.5);
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(r, r, va.distanceTo(vb), radial), material);
    mesh.position.copy(mid);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), vb.clone().sub(va).normalize());
    mesh.castShadow = true; return mesh;
  }
  const left = makeLung(-0.95); const right = makeLung(0.95);
  root.add(left.lung); root.add(right.lung);

  // Trachea (windpipe) splitting into bronchi
  const trachea = new THREE.Mesh(
    new THREE.CylinderGeometry(0.1, 0.1, 1.1, 12),
    new THREE.MeshStandardMaterial({ color: 0xd7c3b0, roughness: 0.6 })
  );
  trachea.position.set(0, 2.1, 0); root.add(trachea);
  const airwayMat = new THREE.MeshStandardMaterial({ color: 0xd7c3b0, roughness: 0.6 });
  [-0.4, 0.4].forEach((bx, i) => {
    const side = i === 0 ? -1 : 1;
    const bronchus = new THREE.Mesh(
      new THREE.CylinderGeometry(0.07, 0.07, 0.6, 10),
      airwayMat
    );
    bronchus.position.set(bx * 1.2, 1.55, 0); bronchus.rotation.z = i === 0 ? 0.9 : -0.9; root.add(bronchus);
    for (let b = 0; b < 4; b++) {
      const y = 1.35 - b * 0.22;
      root.add(cylBetween([side * 0.47, y + 0.20, 0.02], [side * (0.62 + b * 0.07), y, 0.12], 0.026 - b * 0.003, airwayMat, 8));
      root.add(cylBetween([side * 0.47, y + 0.20, 0.02], [side * (0.74 + b * 0.04), y + 0.02, -0.14], 0.020 - b * 0.002, airwayMat, 8));
    }
  });
  const alveolusMat = new THREE.MeshStandardMaterial({ color: 0xf7b2c4, roughness: 0.65, transparent: true, opacity: 0.78 });
  [-1, 1].forEach((side) => {
    for (let i = 0; i < 18; i++) {
      const a = i * 2.399; const r = 0.10 + (i % 3) * 0.055;
      const alv = new THREE.Mesh(new THREE.SphereGeometry(0.035, 10, 8), alveolusMat);
      alv.position.set(side * (0.82 + Math.cos(a) * r), 0.06 + (i % 6) * 0.22, Math.sin(a) * 0.22);
      root.add(alv);
    }
  });

  // ---- Blood particle flow (oxygen-rich red, oxygen-poor blue) ----
  const MAX_BLOOD = 160;
  const bPos = new Float32Array(MAX_BLOOD * 3);
  const bCol = new Float32Array(MAX_BLOOD * 3);
  const bGeo = new THREE.BufferGeometry();
  bGeo.setAttribute('position', new THREE.BufferAttribute(bPos, 3));
  bGeo.setAttribute('color', new THREE.BufferAttribute(bCol, 3));
  const bMat = new THREE.PointsMaterial({ size: 0.1, vertexColors: true, transparent: true, opacity: 0.9, depthWrite: false });
  const blood = new THREE.Points(bGeo, bMat); scene.add(blood);
  const bv = new Float32Array(MAX_BLOOD * 3); // velocities
  const bPath = new Float32Array(MAX_BLOOD);  // progress 0..1 around loop
  const RED = new THREE.Color(0xff3b3b); const BLUE = new THREE.Color(0x3b6bff);
  for (let i = 0; i < MAX_BLOOD; i++) {
    bPath[i] = Math.random();
    const c = Math.random() < 0.5 ? RED : BLUE;
    bCol[i * 3] = c.r; bCol[i * 3 + 1] = c.g; bCol[i * 3 + 2] = c.b;
  }
  // Heart-lung loop path sampled: heart -> lung -> back to heart (figure-8-ish)
  function loopPoint(t, out) {
    // t in 0..1; first half lung (oxygen pickup), second half return
    const side = t < 0.5 ? -1 : 1;
    const lt = t < 0.5 ? t * 2 : (t - 0.5) * 2;
    const ang = lt * Math.PI * 2;
    const baseX = side * 0.95;
    const baseY = 0.7;
    out[0] = baseX + Math.cos(ang) * 0.35;
    out[1] = baseY + Math.sin(ang) * 0.9;
    out[2] = Math.sin(ang * 2) * 0.2;
    if (t < 0.02 || t > 0.98) { out[0] = 0.2; out[1] = 0.5; out[2] = 0.2; }
  }
  const tmp = [0, 0, 0];

  // ---- Activity + rates ----
  let activity = 0.0; // 0 = rest, 1 = hard exercise
  function bpm() { return 70 + activity * 90; }       // ~70 to ~160
  function breathsPerMin() { return 12 + activity * 32; } // ~12 to ~44

  const hud = createHud(stage);
  const heartBadge = hud.badge('♥ 70 bpm', '#ef4444');
  const lungBadge = hud.badge('🫁 12 breaths/min', '#60a5fa');

  const panel = createPanel(stage, { title: 'Heart & Lungs' });
  panel.info('Your heart pumps blood to the lungs to collect oxygen, then out to the body. Raise the activity to watch both heartbeat and breathing speed up.');
  const actSlider = panel.slider({
    label: 'Activity level', min: 0, max: 100, step: 1, value: 0,
    format: (v) => v < 25 ? 'Resting' : v < 60 ? 'Walking' : v < 85 ? 'Running' : 'Sprinting',
    onChange: (v) => { activity = v / 100; },
  });
  panel.divider();
  const bpmOut = panel.readout({ label: 'Heart rate', value: '70 bpm' });
  const breathOut = panel.readout({ label: 'Breathing rate', value: '12 /min' });
  panel.readout({ label: 'Blood pumped/day', value: '~7,000 litres' });
  panel.readout({ label: 'Alveoli (air sacs)', value: '~480 million' });
  panel.button({ label: 'Why does exercise make you puff?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Eat now, breathe faster',
      body: 'When you run, your muscles burn glucose for energy faster, needing more oxygen and producing more CO₂. Sensors in your body tell the heart to beat faster and the lungs to breathe deeper, so more oxygen reaches every working cell.',
      color: '#ef4444',
    });
  } });

  // Animation state
  let beatPhase = 0; let breathPhase = 0; let lastBeat = false;
  function refreshBadges() {
    const b = Math.round(bpm()); const br = Math.round(breathsPerMin());
    heartBadge.set(`♥ ${b} bpm`); lungBadge.set(`🫁 ${br} breaths/min`);
    bpmOut.set(`${b} bpm`); breathOut.set(`${br} /min`);
  }
  refreshBadges();

  engine.setUpdate((dt) => {
    controls.update(dt);
    const b = bpm(); const br = breathsPerMin();
    // Heartbeat: two quick thumps per cycle (lub-dub)
    beatPhase += dt * (b / 60);
    const cyc = beatPhase % 1;
    const beatStrength = cyc < 0.12 ? Math.sin((cyc / 0.12) * Math.PI) * 0.18
      : cyc < 0.18 ? 0
        : cyc < 0.30 ? Math.sin(((cyc - 0.18) / 0.12) * Math.PI) * 0.12 : 0;
    const scale = 1 + beatStrength;
    heart.scale.setScalar(scale);
    heartMesh.material.emissiveIntensity = 0.2 + beatStrength * 1.8;
    if (cyc < 0.12 && !lastBeat) { lastBeat = true; refreshBadges(); }
    else if (cyc >= 0.12) lastBeat = false;

    // Breathing: sinusoidal inflation
    breathPhase += dt * (br / 60) * Math.PI * 2;
    const inflate = (Math.sin(breathPhase) * 0.5 + 0.5); // 0..1
    const lungScale = 0.85 + inflate * 0.45;
    left.lung.scale.set(lungScale, lungScale * 0.95, lungScale);
    right.lung.scale.set(lungScale, lungScale * 0.95, lungScale);
    left.mesh.material.emissiveIntensity = 0.1 + inflate * 0.25;
    right.mesh.material.emissiveIntensity = 0.1 + inflate * 0.25;
    // trachea subtly rises with breath
    trachea.position.y = 2.1 + inflate * 0.06;

    // Blood flow: speed scales with heart rate
    const speed = (b / 70) * 0.25;
    for (let i = 0; i < MAX_BLOOD; i++) {
      bPath[i] = (bPath[i] + dt * speed) % 1;
      loopPoint(bPath[i], tmp);
      bPos[i * 3] += (tmp[0] - bPos[i * 3]) * 0.25;
      bPos[i * 3 + 1] += (tmp[1] - bPos[i * 3 + 1]) * 0.25;
      bPos[i * 3 + 2] += (tmp[2] - bPos[i * 3 + 2]) * 0.25;
      // colour by half: 0..0.5 is going TO lungs (blue, deoxygenated), 0.5..1 returning (red, oxygenated)
      const oxy = bPath[i] > 0.5 ? 1 : 0;
      bCol[i * 3] += ((RED.r * oxy + BLUE.r * (1 - oxy)) - bCol[i * 3]) * 0.1;
      bCol[i * 3 + 1] += ((RED.g * oxy + BLUE.g * (1 - oxy)) - bCol[i * 3 + 1]) * 0.1;
      bCol[i * 3 + 2] += ((RED.b * oxy + BLUE.b * (1 - oxy)) - bCol[i * 3 + 2]) * 0.1;
    }
    bGeo.attributes.position.needsUpdate = true;
    bGeo.attributes.color.needsUpdate = true;
  });

  engine.start();

  return {
    dispose() {
      bGeo.dispose(); bMat.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
