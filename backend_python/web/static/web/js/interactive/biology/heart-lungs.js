import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { buildScene, buildModels, backdrop } from './heartlungs/scene.js';
import { PARTS, ANCHORS } from './heartlungs/heart-model.js';
import { LOBES } from './heartlungs/lung-model.js';
import { createBloodFlow, createAirFlow } from './heartlungs/flow.js';
import { createMonitor, createHeartSound, cardiac } from './heartlungs/monitor.js';
import { createAtlasLabels } from './anatomy/labels.js';
import { setXray } from './anatomy/tissue.js';

const VIEWS = {
  overview: { label: 'Heart & lungs', target: [0, 0.25, 0], pos: [0.9, 0.6, 4.6] },
  heart: { label: 'The heart', target: [0.05, 0.05, 0.05], pos: [0.55, 0.25, 2.35] },
  inside: { label: 'Inside the heart', target: [0.0, 0.05, 0.0], pos: [0.15, 0.15, 2.2] },
  flow: { label: 'Blood flow', target: [0, 0.15, -0.1], pos: [0.6, 0.5, 3.9] },
  airways: { label: 'Airways', target: [0, 0.35, -0.1], pos: [0.4, 0.45, 4.2] },
};

const LUNG_INFO = {
  rul: 'The right lung has three lobes, separated by the oblique and horizontal fissures.',
  rml: 'The right middle lobe sits between the horizontal and oblique fissures. The left lung has no middle lobe; it is smaller to make room for the heart.',
  rll: 'The lower lobes are the largest and do most of the breathing work, sitting on the dome of the diaphragm.',
  lul: 'The left upper lobe has a notch, the cardiac notch, where the heart pushes into the lung, and a tongue-like part called the lingula.',
  lll: 'Each lung holds about 300 million alveoli, tiny air sacs wrapped in capillaries, where oxygen enters the blood and carbon dioxide leaves.',
};

const EXTRA = {
  diaphragm: ['Diaphragm', 'A dome of muscle under the lungs with a tough central tendon. When it contracts it flattens and moves down, the chest gets bigger, and air rushes in. That is about 75% of every quiet breath.'],
  trachea: ['Trachea (windpipe)', 'About 11 cm long and held open by 16–20 C-shaped rings of cartilage. The open part of each C faces back, so the oesophagus behind it can bulge when you swallow. It splits into the left and right main bronchi.'],
};

function activityName(a) { return a < 0.15 ? 'Resting' : a < 0.4 ? 'Walking' : a < 0.7 ? 'Jogging' : a < 0.9 ? 'Running' : 'Sprinting'; }

export default function init(stage) {
  stage.classList.add('bio-beginner-stage', 'bio-heart-lungs-stage');
  const engine = createEngine(stage, { noise: true, exposure: 0.92, fov: 38, near: 0.01, far: 200 });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  renderer.localClippingEnabled = true;
  scene.background = new THREE.Color(0x0b0e14);
  scene.add(backdrop());

  const hemi = new THREE.HemisphereLight(0xdfe8ff, 0x2a1a18, 0.3);
  const key = new THREE.DirectionalLight(0xfff0e2, 1.9); key.position.set(3, 5, 6);
  const fill = new THREE.DirectionalLight(0xc8d8ff, 0.45); fill.position.set(-5, 1, 3);
  const rim = new THREE.DirectionalLight(0xa8c4ff, 1.6); rim.position.set(-2, 4, -6);
  const under = new THREE.DirectionalLight(0xffb0a0, 0.35); under.position.set(0, -6, 2);
  scene.add(hemi, key, rim);
  hemi.intensity = 0.55;

  const loading = document.createElement('div');
  loading.style.cssText = 'position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:4;font:500 13px Poppins,system-ui;color:#dbe6ff;background:rgba(8,12,24,.6);padding:8px 14px;border-radius:999px;pointer-events:none';
  loading.textContent = 'Sculpting the heart and lungs…';
  stage.appendChild(loading);

  camera.position.set(...VIEWS.overview.pos);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 1.0, maxDistance: 9, enablePan: true, damping: 0.1 });
  controls.setTarget(new THREE.Vector3(...VIEWS.overview.target));

  const hud = createHud(stage);
  const hrBadge = hud.badge('♥ 70 bpm', '#f87171');
  const brBadge = hud.badge('12 breaths/min', '#60a5fa');

  let S = null; let blood = null; let air = null;
  let activity = 0;
  let view = 'overview';
  let breathing = true;
  let cph = 0; let bph = 0; let lastPh = 0;
  let xray = 0; let xrayGoal = 0; let lungFade = 1; let lungGoal = 1; let cut = 0; let cutGoal = 0;
  let camAnim = null;
  const sound = createHeartSound();
  const clipPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 10);

  const labels = createAtlasLabels(stage, { onPick: (id) => pick(id) });

  const panel = createPanel(stage, { title: 'Heart & Lungs' });
  panel.info('A beating heart and breathing lungs, sculpted from their real anatomy. Drag to turn, scroll to zoom, tap any part to learn what it does.');
  panel.slider({
    label: 'Activity', min: 0, max: 100, step: 1, value: 0, format: (v) => activityName(v / 100),
    onChange: (v) => { activity = v / 100; },
  });
  panel.chips({ label: 'View', options: Object.entries(VIEWS).map(([k, v]) => ({ value: k, label: v.label })), value: 'overview', onChange: (v) => setView(v) });
  const monitor = createMonitor(panel.body);
  const stats = panel.stats([
    { key: 'hr', label: 'Heart rate' }, { key: 'sv', label: 'Stroke volume' },
    { key: 'co', label: 'Cardiac output' }, { key: 'br', label: 'Breathing rate' },
    { key: 'tv', label: 'Tidal volume' }, { key: 'mv', label: 'Air per minute' },
  ]);
  panel.toggle({ label: 'Breathing', value: true, onChange: (v) => { breathing = v; } });
  panel.toggle({ label: 'Textbook blood colours', value: false, onChange: (v) => { if (S) S.uniforms.uTextbook.value = v ? 1 : 0; } });
  panel.toggle({ label: 'Labels', value: true, onChange: (v) => { labels.enabled = v; } });
  panel.toggle({ label: 'Heart sounds', value: false, onChange: (v) => { sound.on = v; } });
  panel.button({
    label: 'Why does exercise make you puff?', icon: 'menu_book',
    onClick: () => showInfoCard(stage, {
      title: 'Why exercise makes you puff',
      body: 'Working muscles burn glucose with oxygen and make carbon dioxide. Rising CO₂ in the blood is sensed in the brainstem, which tells the diaphragm and rib muscles to breathe faster and deeper. At the same time the heart beats faster and pumps more per beat, so cardiac output can rise from about 5 to over 20 litres a minute.',
      color: '#f87171',
    }),
  });

  function physiology() {
    const a = activity;
    const hr = 66 + 112 * a;
    const sv = 70 + 38 * Math.sqrt(a);
    const br = 12 + 30 * a * a + 6 * a;
    const tv = 0.5 + 2.1 * a;
    return { hr, sv, br, tv, co: hr * sv / 1000, mv: br * tv };
  }

  function setView(v) {
    view = v;
    const V = VIEWS[v];
    camAnim = { t: 0, fromP: camera.position.clone(), fromT: controls.target.clone(), toP: new THREE.Vector3(...V.pos), toT: new THREE.Vector3(...V.target) };
    xrayGoal = v === 'flow' ? 1 : 0;
    lungGoal = v === 'heart' || v === 'inside' ? 0 : 1;
    cutGoal = v === 'inside' ? 1 : 0;
  }

  function pick(id) {
    labels.active = id;
    const p = PARTS[id];
    if (p) {
      showInfoCard(stage, { title: p.name, body: p.text, color: '#f87171' });
      if (S) { S.uniforms.uHi.value = S.heart.userData.partNames.indexOf(id); S.uniforms.uHiAmt.value = 1; }
      return;
    }
    if (EXTRA[id]) { showInfoCard(stage, { title: EXTRA[id][0], body: EXTRA[id][1], color: '#93c5fd' }); return; }
    if (LOBES[id]) {
      showInfoCard(stage, { title: LOBES[id], body: LUNG_INFO[id], color: '#f9a8d4' });
      if (S) { S.uniforms.uHi.value = Object.keys(LOBES).indexOf(id); S.uniforms.uHiAmt.value = 1; }
    }
  }

  const ray = new THREE.Raycaster();
  let down = null;
  engine.canvas.addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY }; });
  engine.canvas.addEventListener('pointerup', (e) => {
    if (!down || !S || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6) return;
    const r = engine.canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1), camera);
    const targets = [S.heart];
    if (S.lungs.right.visible && lungFade > 0.5) targets.push(S.lungs.right, S.lungs.left);
    const hit = ray.intersectObjects(targets, false)[0];
    if (!hit) return;
    const attr = hit.object.geometry.attributes.part;
    const pidx = Math.round(attr.getX(hit.face.a));
    if (hit.object === S.heart) pick(S.heart.userData.partNames[pidx]);
    else pick(Object.keys(LOBES)[pidx]);
  });

  function lungAlpha(a) {
    ['right', 'left'].forEach((s) => { S.lungs[s].visible = a > 0.02; });
    S.materials.lung.userData.uniforms.uXray.value = 0;
    const m = S.materials.lung;
    const t = a < 0.999 || xray > 0.01 || view === 'airways';
    if (m.transparent !== t) { m.transparent = t; m.side = t ? THREE.FrontSide : THREE.DoubleSide; m.needsUpdate = true; }
    m.depthWrite = !t;
    m.opacity = a;
  }

  let disposed = false;
  buildModels(quality).then((models) => {
    if (disposed) return;
    S = buildScene(quality, models);
    scene.add(S.root);
    blood = createBloodFlow(quality);
    blood.mesh.visible = false;
    S.heartGroup.add(blood.mesh);
    air = createAirFlow(S.branches, quality);
    air.points.visible = false;
    S.root.add(air.points);
    [S.materials.heart, S.materials.airway, S.materials.diaphragm].forEach((m) => { m.clippingPlanes = []; });
    S.materials.heart.clippingPlanes = [clipPlane];
    Object.entries(ANCHORS).forEach(([id, a]) => labels.add({ id, text: PARTS[id].name, anchor: new THREE.Vector3(...a), object: S.heartGroup, group: 'heart', minor: ['svc', 'ra', 'trunk', 'arch', 'pa', 'pv', 'ivc'].includes(id) }));
    labels.add({ id: 'rul', text: 'Right lung', anchor: new THREE.Vector3(-8.2, 4.0, 2.0), object: S.root, group: 'lung' });
    labels.add({ id: 'lul', text: 'Left lung', anchor: new THREE.Vector3(8.0, 4.4, 1.6), object: S.root, group: 'lung' });
    labels.add({ id: 'diaphragm', text: 'Diaphragm', anchor: new THREE.Vector3(-3.0, -8.0, 4.0), object: S.root, group: 'lung', minor: true });
    labels.add({ id: 'trachea', text: 'Trachea', anchor: new THREE.Vector3(0, 13.5, 0.2), object: S.root, group: 'air' });
    loading.remove();
  });

  const LABEL_SET = {
    overview: (d) => ['aorta', 'svc', 'trunk', 'lv', 'rv', 'ra'].includes(d.id) || d.group === 'lung' || d.group === 'air',
    heart: (d) => d.group === 'heart',
    inside: (d) => ['lv', 'rv', 'ra', 'la', 'aorta', 'trunk'].includes(d.id),
    flow: (d) => ['aorta', 'svc', 'ivc', 'trunk', 'pv', 'pa'].includes(d.id),
    airways: (d) => d.group === 'air' || d.group === 'lung',
  };

  engine.setUpdate((dt, t) => {
    const P = physiology();
    controls.update(dt);
    if (camAnim) {
      camAnim.t = Math.min(1, camAnim.t + dt / 1.3);
      const e = camAnim.t * camAnim.t * (3 - 2 * camAnim.t);
      camera.position.lerpVectors(camAnim.fromP, camAnim.toP, e);
      controls.setView(camera.position.clone(), camAnim.fromT.clone().lerp(camAnim.toT, e));
      if (camAnim.t >= 1) camAnim = null;
    }
    cph += dt * P.hr / 60; const ph = cph % 1;
    if (lastPh < 0.2 && ph >= 0.2) sound.lub();
    if (lastPh < 0.5 && ph >= 0.5) sound.dub();
    lastPh = ph;
    const c = cardiac(ph);
    if (breathing) bph += dt * P.br / 60;
    const b = bph % 1;
    const ease = (x) => x * x * (3 - 2 * x);
    const vol = b < 0.4 ? ease(b / 0.4) : 1 - ease((b - 0.4) / 0.6);
    monitor.push(dt, ph, P.hr);
    hrBadge.set(`♥ ${Math.round(P.hr)} bpm`);
    brBadge.set(`${Math.round(P.br)} breaths/min`);
    stats.hr.set(`${Math.round(P.hr)} bpm`); stats.sv.set(`${Math.round(P.sv)} mL`); stats.co.set(`${P.co.toFixed(1)} L/min`);
    stats.br.set(`${Math.round(P.br)} /min`); stats.tv.set(`${P.tv.toFixed(1)} L`); stats.mv.set(`${P.mv.toFixed(0)} L/min`);
    if (!S) return;
    const amp = 0.35 + 0.65 * Math.min(1, P.tv / 2.6);
    const u = S.uniforms;
    u.uTime.value = t; u.uBeatV.value = c.vent * (0.85 + 0.25 * activity); u.uBeatA.value = c.atria; u.uBreath.value = vol * amp;
    u.uHiAmt.value = Math.max(0, u.uHiAmt.value - dt * 0.25);
    S.heartGroup.position.y = -0.55 * vol * amp;
    S.heartGroup.rotation.z = -0.02 * vol * amp;
    xray += (xrayGoal - xray) * Math.min(1, dt * 4);
    lungFade += (lungGoal - lungFade) * Math.min(1, dt * 4);
    cut += (cutGoal - cut) * Math.min(1, dt * 3);
    setXray(S.materials.heart, xray * 0.85);
    const hm = S.materials.heart; const wantSide = cut > 0.01 ? THREE.DoubleSide : THREE.FrontSide;
    if (!hm.transparent && hm.side !== wantSide) { hm.side = wantSide; hm.userData.side0 = wantSide; hm.needsUpdate = true; }
    lungAlpha(lungFade * (1 - xray * 0.78));
    S.materials.lung.opacity = lungFade * (1 - xray * 0.78);
    const airView = view === 'airways';
    S.tree.visible = airView || xray > 0.3;
    S.materials.lung.userData.uniforms.uXray.value = airView ? 0.88 : 0;
    if (airView) S.materials.lung.depthWrite = false;
    air.points.visible = airView;
    if (airView) air.update(vol);
    S.diaphragm.visible = lungFade > 0.3;
    S.airway.visible = lungFade > 0.3 || airView;
    blood.mesh.visible = xray > 0.3;
    if (blood.mesh.visible) blood.update(dt, { pulse: (0.35 + 1.7 * c.ejecting) * P.hr / 70, steady: P.hr / 70 }, u.uTextbook.value > 0.5);
    const zc = 6 - cut * 5.9;
    clipPlane.normal.set(0, 0, -1).transformDirection(S.heartGroup.matrixWorld);
    clipPlane.constant = new THREE.Vector3(0, 0, zc).applyMatrix4(S.heartGroup.matrixWorld).dot(clipPlane.normal) * -1;
    const w = stage.clientWidth; const h = stage.clientHeight;
    labels.update(camera, w, h, LABEL_SET[view]);
  });
  engine.start();

  stage.__hl = { setView, pick, get scene() { return S; } };
  return {
    dispose() {
      disposed = true;
      controls.dispose(); panel.dispose(); hud.dispose(); labels.dispose(); sound.dispose();
      if (blood) blood.dispose(); if (air) air.dispose(); if (S) S.dispose();
      engine.dispose();
    },
  };
}
