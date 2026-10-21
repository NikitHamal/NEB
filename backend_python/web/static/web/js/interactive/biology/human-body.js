import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { buildBody } from './body/scene.js';
import { ORGAN_INFO } from './body/organs.js';
import { buildScene as buildHeartLungs, buildModels as buildHeartLungModels, backdrop } from './heartlungs/scene.js';
import { cardiac } from './heartlungs/monitor.js';
import { createAtlasLabels } from './anatomy/labels.js';
import { setXray } from './anatomy/tissue.js';

const LAYERS = ['Skin', 'Muscles', 'Skeleton', 'Organs'];
const SYSTEMS = {
  all: { label: 'Whole body' },
  skeletal: { label: 'Skeleton', depth: 2 },
  muscular: { label: 'Muscles', depth: 1 },
  digestive: { label: 'Digestion', organs: ['esophagus', 'stomach', 'liver', 'gallbladder', 'pancreas', 'small', 'colon'], depth: 3 },
  cardio: { label: 'Heart, lungs & blood', organs: ['heartlungs', 'arteries', 'veins'], depth: 3 },
  nervous: { label: 'Nerves & brain', organs: ['brain', 'cord', 'nerves'], depth: 3 },
  urinary: { label: 'Kidneys & bladder', organs: ['kidney', 'ureter', 'ureter2', 'bladder', 'adrenal'], depth: 3 },
};
const LAYER_INFO = {
  Skin: 'Your largest organ, about 2 m² and 4 kg. It keeps water in and germs out, senses touch, heat and pain, and cools you by sweating.',
  Muscles: 'More than 600 skeletal muscles make up about 40% of your weight. They can only pull, so they work in pairs across joints. White tendons tie them to bone.',
  Skeleton: '206 bones in an adult. They hold you up, protect the brain, heart and lungs, store calcium, and make blood cells inside their marrow.',
  Organs: 'Organs work in systems: digestion, breathing, circulation, the nervous system and the urinary system all share the space inside your trunk.',
};
const BONE_INFO = {
  Femur: 'The thigh bone, the longest and strongest bone in the body, about a quarter of your height.',
  Cranium: 'The skull’s brain case: eight bones fused at wavy joints called sutures.',
  Mandible: 'The lower jaw, the only skull bone that moves.',
  Sternum: 'The breastbone. Ribs attach to it with flexible cartilage so the chest can expand when you breathe.',
  Humerus: 'The upper-arm bone, from the shoulder to the elbow.',
  Tibia: 'The shin bone, which carries almost all of your weight down to the ankle.',
  Pelvis: 'The pelvic girdle, a ring of bones that carries the weight of the trunk to the legs and protects the bladder.',
};

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-human-body-stage');
  const engine = createEngine(stage, { noise: true, exposure: 0.95, fov: 30, near: 0.01, far: 100 });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  scene.background = new THREE.Color(0x0b0e14);
  const bd = backdrop(); bd.scale.setScalar(0.4); scene.add(bd);
  const hemi = new THREE.HemisphereLight(0xe6eeff, 0x2a2420, 0.35);
  const key = new THREE.DirectionalLight(0xfff1e4, 2.0); key.position.set(2.5, 4, 4);
  const fill = new THREE.DirectionalLight(0xc6d6ff, 0.55); fill.position.set(-4, 1.5, 2.5);
  const rim = new THREE.DirectionalLight(0xb0c8ff, 1.5); rim.position.set(-1.5, 3, -4);
  scene.add(hemi, key, rim);
  hemi.intensity = 0.5;
  const floorMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, vertexShader: 'varying vec2 vU; void main(){ vU = uv * 2.0 - 1.0; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }', fragmentShader: 'varying vec2 vU; void main(){ float r = length(vU); float a = smoothstep(1.0, 0.2, r) * 0.55; float ring = smoothstep(0.012, 0.0, abs(r - 0.62)) * 0.25; gl_FragColor = vec4(vec3(0.16, 0.2, 0.28) + ring, a); }' });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.6), floorMat);
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.002;
  scene.add(floor);
  const shadow = new THREE.Mesh(new THREE.CircleGeometry(0.42, 48), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.45, depthWrite: false }));
  shadow.rotation.x = -Math.PI / 2; shadow.position.y = 0.001; shadow.scale.set(1, 0.55, 1);
  scene.add(shadow);

  camera.position.set(0.32, 0.98, 3.35);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 0.35, maxDistance: 6, enablePan: true, damping: 0.1, minPolar: 0.15, maxPolar: Math.PI - 0.3 });
  controls.setTarget(new THREE.Vector3(0, 0.88, 0));

  const loading = document.createElement('div');
  loading.style.cssText = 'position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:4;font:500 13px Poppins,system-ui;color:#dbe6ff;background:rgba(8,12,24,.6);padding:8px 14px;border-radius:999px;pointer-events:none;white-space:nowrap';
  loading.textContent = 'Loading the anatomy model…';
  stage.appendChild(loading);
  const sysLoading = document.getElementById('ix-sim-loading');
  if (sysLoading) sysLoading.remove();

  const hud = createHud(stage);
  const layerBadge = hud.badge('Skin', '#84CC16');
  const partBadge = hud.badge('Tap a body part', '#60a5fa');

  let B = null; let HL = null;
  let depth = 0; let depthGoal = 0;
  let system = 'all';
  let ghost = true;
  let activity = 0;
  let cph = 0; let bph = 0;
  let camAnim = null;

  const labels = createAtlasLabels(stage, { onPick: (id) => pickOrgan(id) });
  const panel = createPanel(stage, { title: 'Human Body Explorer' });
  panel.info('A real, full-size human anatomy: 206 bones and hundreds of muscles from an anatomical atlas, with organs that beat and breathe. Peel the layers, or pick a body system.');
  const layerSlider = panel.slider({
    label: 'Peel the layers', min: 0, max: 3, step: 0.01, value: 0, format: (v) => LAYERS[Math.round(v)],
    onChange: (v) => { depthGoal = v; system = 'all'; },
  });
  panel.chips({ label: 'Body system', options: Object.entries(SYSTEMS).map(([k, v]) => ({ value: k, label: v.label })), value: 'all', onChange: (v) => setSystem(v) });
  panel.slider({ label: 'Activity', min: 0, max: 100, step: 1, value: 0, format: (v) => (v < 15 ? 'Resting' : v < 45 ? 'Walking' : v < 80 ? 'Running' : 'Sprinting'), onChange: (v) => { activity = v / 100; } });
  panel.toggle({ label: 'Glass skin', value: true, onChange: (v) => { ghost = v; } });
  panel.toggle({ label: 'Labels', value: true, onChange: (v) => { labels.enabled = v; } });
  const stats = panel.stats([{ key: 'sel', label: 'Selected' }, { key: 'hr', label: 'Heart rate' }, { key: 'br', label: 'Breathing' }, { key: 'co', label: 'Blood pumped' }]);
  const about = panel.info(LAYER_INFO.Skin);

  function setSystem(k) {
    system = k;
    const S = SYSTEMS[k];
    if (S.depth !== undefined) { depthGoal = S.depth; layerSlider.set(S.depth); }
    const focus = { digestive: [0, 1.04, 0.02, 1.05], cardio: [0, 1.22, 0.02, 1.1], nervous: [0, 1.15, 0, 2.6], urinary: [0, 0.98, -0.02, 0.95], skeletal: [0, 0.88, 0, 3.35], muscular: [0, 0.88, 0, 3.35], all: [0, 0.88, 0, 3.35] }[k];
    flyTo(new THREE.Vector3(focus[0], focus[1], focus[2]), focus[3]);
  }
  function flyTo(target, dist) {
    const dir = camera.position.clone().sub(controls.target).normalize();
    camAnim = { t: 0, fromP: camera.position.clone(), fromT: controls.target.clone(), toT: target, toP: target.clone().addScaledVector(dir, dist) };
  }
  function pickOrgan(id) {
    const info = id === 'heartlungs' ? ['Heart and lungs', 'The heart pumps about 5 litres of blood a minute at rest; the lungs fill with about half a litre of air in every quiet breath. Open the Heart & Lungs lesson to explore them in depth.'] : ORGAN_INFO[id];
    if (!info) return;
    labels.active = id;
    partBadge.set(info[0]); stats.sel.set(info[0]);
    showInfoCard(stage, { title: info[0], body: info[1], color: '#84CC16' });
  }

  const ray = new THREE.Raycaster();
  let down = null;
  engine.canvas.addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY }; });
  engine.canvas.addEventListener('pointerup', (e) => {
    if (!down || !B || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6) return;
    const r = engine.canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1), camera);
    const cands = [];
    if (depth < 0.6) cands.push(B.skin);
    if (depth < 1.6) cands.push(B.muscleMesh);
    if (depth < 2.6) cands.push(B.boneMesh);
    if (depth > 1.4) { B.organs.children.forEach((m) => m.visible && cands.push(m)); if (HL) cands.push(HL.heart, HL.lungs.left, HL.lungs.right); B.vessels.children.forEach((g) => g.visible && cands.push(...g.children)); }
    const hit = ray.intersectObjects(cands, false)[0];
    if (!hit) return;
    const o = hit.object;
    if (o === B.skin) { partBadge.set('Skin'); stats.sel.set('Skin'); showInfoCard(stage, { title: 'Skin', body: LAYER_INFO.Skin, color: '#84CC16' }); return; }
    if (o === B.boneMesh || o === B.muscleMesh) {
      const idx = Math.round(o.geometry.attributes.part.getX(hit.face.a));
      const name = o.userData.names[idx] || 'Body part';
      const u = o.material.userData.uniforms; u.uHi.value = idx; u.uHiAmt.value = 1;
      const base = name.replace(/ \((left|right)\)$/, '');
      const known = Object.keys(BONE_INFO).find((k) => base.startsWith(k));
      partBadge.set(name); stats.sel.set(name.length > 24 ? `${name.slice(0, 23)}…` : name);
      showInfoCard(stage, { title: name, body: known ? BONE_INFO[known] : (o === B.boneMesh ? `A bone of the ${/rib|vertebra|sternum|cranium|skull|sacrum|coccyx/i.test(name) ? 'axial skeleton (skull, spine and ribcage)' : 'limbs and girdles (the appendicular skeleton)'}. Bone is living tissue that remodels itself throughout life.` : `A skeletal muscle. It shortens when it contracts and pulls on the bones it is attached to through its tendons. Muscle fibres run along its length.`), color: '#84CC16' });
      return;
    }
    if (HL && (o === HL.heart || o === HL.lungs.left || o === HL.lungs.right)) { pickOrgan('heartlungs'); return; }
    if (o.userData.organ) pickOrgan(o.userData.organ);
  });

  const hlQuality = { tier: quality.tier === 'high' ? 'medium' : 'low' };
  const hlModels = buildHeartLungModels(hlQuality);
  buildBody(quality, {
    onProgress: (x) => { if (x.total) loading.textContent = `Loading the anatomy model… ${Math.round(x.loaded / x.total * 100)}%`; },
    onStage: (t) => { loading.textContent = t; },
  }).then((body) => hlModels.then((models) => [body, models])).then(([body, models]) => {
    B = body;
    scene.add(B.skin, B.muscleMesh, B.boneMesh, B.organs, B.vessels);
    HL = buildHeartLungs(hlQuality, models);
    HL.root.scale.setScalar(0.01);
    HL.root.position.set(0.004, 1.262, 0.012);
    HL.diaphragm.visible = false;
    HL.root.userData.organ = 'heartlungs';
    scene.add(HL.root);
    const L = (id, text, a, minor) => labels.add({ id, text, anchor: new THREE.Vector3(...a), group: 'organ', minor });
    L('brain', 'Brain', [0.03, 1.69, 0.02]); L('heartlungs', 'Heart', [0.03, 1.24, 0.07]); L('heartlungs', 'Lungs', [-0.09, 1.3, 0.05]);
    L('liver', 'Liver', [-0.1, 1.13, 0.06]); L('stomach', 'Stomach', [0.09, 1.1, 0.04]); L('small', 'Small intestine', [-0.03, 0.98, 0.07]);
    L('colon', 'Large intestine', [0.09, 1.0, 0.03], true); L('kidney', 'Kidneys', [0.06, 1.05, -0.04], true); L('bladder', 'Bladder', [0, 0.88, 0.07], true);
    L('cord', 'Spinal cord', [0, 1.3, -0.07], true); L('pancreas', 'Pancreas', [0.03, 1.075, 0.015], true); L('spleen', 'Spleen', [0.11, 1.12, -0.03], true);
    loading.remove();
  }).catch((err) => {
    console.error('Body failed to load', err);
    loading.textContent = 'The anatomy model could not load. Check your connection and refresh.';
  });

  const ORGAN_SET = (d) => {
    if (system === 'all') return depth > 2.2 && !d.minor;
    const S = SYSTEMS[system];
    return S.organs && S.organs.includes(d.id === 'heartlungs' ? 'heartlungs' : d.id);
  };

  engine.setUpdate((dt, t) => {
    controls.update(dt);
    if (camAnim) {
      camAnim.t = Math.min(1, camAnim.t + dt / 1.2);
      const e = camAnim.t * camAnim.t * (3 - 2 * camAnim.t);
      controls.setView(camAnim.fromP.clone().lerp(camAnim.toP, e), camAnim.fromT.clone().lerp(camAnim.toT, e));
      if (camAnim.t >= 1) camAnim = null;
    }
    const hr = 66 + 112 * activity; const br = 12 + 30 * activity * activity + 6 * activity;
    stats.hr.set(`${Math.round(hr)} bpm`); stats.br.set(`${Math.round(br)} /min`); stats.co.set(`${(hr * (70 + 38 * Math.sqrt(activity)) / 1000).toFixed(1)} L/min`);
    depth += (depthGoal - depth) * Math.min(1, dt * 5);
    const layer = LAYERS[Math.min(3, Math.round(depth))];
    layerBadge.set(layer);
    about.set(SYSTEMS[system].organs ? `${SYSTEMS[system].label}: tap an organ to learn what it does.` : LAYER_INFO[layer]);
    if (!B) return;
    cph += dt * hr / 60; bph += dt * br / 60;
    const c = cardiac(cph % 1);
    const b = bph % 1;
    const ez = (x) => x * x * (3 - 2 * x);
    const vol = b < 0.4 ? ez(b / 0.4) : 1 - ez((b - 0.4) / 0.6);
    [B.uniforms, HL && HL.uniforms].forEach((u) => {
      if (!u) return;
      u.uTime.value = t; u.uBeatV.value = c.vent; u.uBeatA.value = c.atria; u.uBreath.value = vol * (0.35 + 0.4 * activity);
    });
    [B.materials.bone, B.materials.muscle].forEach((m) => { const u = m.userData.uniforms; u.uHiAmt.value = Math.max(0, u.uHiAmt.value - dt * 0.35); });
    const skinA = 1 - Math.min(1, Math.max(0, depth));
    const muscleA = 1 - Math.min(1, Math.max(0, depth - 1));
    const sysOn = system !== 'all' && SYSTEMS[system].organs;
    B.skin.visible = skinA > 0.02 || ghost;
    const glass = ghost ? 0.62 + (1 - skinA) * 0.36 : (skinA > 0.98 ? 0 : 1 - skinA * 0.9);
    setXray(B.materials.skin, glass);
    B.materials.skin.opacity = ghost ? 0.3 + skinA * 0.6 : skinA;
    B.muscleMesh.visible = muscleA > 0.02 && system !== 'skeletal';
    setXray(B.materials.muscle, muscleA > 0.98 ? 0 : 1 - muscleA * 0.9);
    B.materials.muscle.opacity = muscleA;
    const boneGhost = depth > 2.2 || sysOn ? Math.min(1, (depth - 2.2) / 0.6 + (sysOn ? 1 : 0)) : 0;
    B.boneMesh.visible = system !== 'muscular' || depth > 1.5;
    setXray(B.materials.bone, boneGhost * 0.8);
    B.materials.bone.opacity = 1 - boneGhost * 0.35;
    const organsOn = depth > 1.2;
    B.organs.visible = organsOn; B.vessels.visible = organsOn;
    if (HL) HL.root.visible = organsOn && (!sysOn || SYSTEMS[system].organs.includes('heartlungs'));
    B.organs.children.forEach((m) => { m.visible = !sysOn || SYSTEMS[system].organs.includes(m.userData.organ) || SYSTEMS[system].organs.includes(m.userData.organ + '2'); });
    B.vessels.children.forEach((g) => { g.visible = sysOn ? SYSTEMS[system].organs.includes(g.userData.kind) : depth > 2.6; });
    labels.update(camera, stage.clientWidth, stage.clientHeight, ORGAN_SET);
  });
  engine.start();

  stage.__hb = { setSystem, setDepth: (d) => { depthGoal = d; layerSlider.set(d); }, flyTo: (x, y, z, d) => flyTo(new THREE.Vector3(x, y, z), d), get body() { return B; } };
  return {
    dispose() {
      controls.dispose(); panel.dispose(); hud.dispose(); labels.dispose();
      if (HL) HL.dispose();
      engine.dispose();
    },
  };
}
