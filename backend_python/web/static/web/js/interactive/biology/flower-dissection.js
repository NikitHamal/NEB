import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard, hideInfoCard } from '../core/sim-ui.js';

const PARTS = [
  { id: 'sepal', name: 'Calyx (sepals)', layer: 0, color: 0x4caf50,
    info: 'The outermost whorl — green, leaf-like sepals that protect the flower bud before it opens. Together they form the calyx.' },
  { id: 'petal', name: 'Corolla (petals)', layer: 1, color: 0xe53935,
    info: 'The colourful, often scented petals. Their job is to attract pollinators — bees, butterflies and birds drawn by colour and nectar. Together they form the corolla.' },
  { id: 'stamen', name: 'Androecium (stamens)', layer: 2, color: 0xfbc02d,
    info: 'The male parts. Each stamen has a thin filament topped by an anther, which produces the dust-like pollen grains carrying the male sex cells.' },
  { id: 'carpel', name: 'Gynoecium (carpel)', layer: 3, color: 0xab47bc,
    info: 'The female part at the very centre — the carpel. A sticky stigma catches pollen, a slender style carries it down, and a swollen ovary holds the ovules that become seeds.' },
];

export default function init(stage) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(14, quality.segments / 2);

  camera.position.set(0, 2.5, 9);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4, maxDistance: 16, enablePan: false, maxPolar: Math.PI * 0.65, minPolar: Math.PI * 0.15,
  });
  controls.setTarget(new THREE.Vector3(0, 0.5, 0));

  scene.background = new THREE.Color(0x0e0f1a);
  scene.fog = new THREE.Fog(0x0e0f1a, 14, 28);
  basicLights(scene, { ambient: 0.5, key: 1.6 });

  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(6, 48),
    new THREE.MeshStandardMaterial({ color: 0x15201a, roughness: 1 })
  );
  ground.rotation.x = -Math.PI / 2; ground.position.y = -2; ground.receiveShadow = true; scene.add(ground);

  const root = new THREE.Group(); scene.add(root);

  // Pedicel + thalamus base
  const pedicel = new THREE.Mesh(
    new THREE.CylinderGeometry(0.09, 0.12, 1.6, 10),
    new THREE.MeshStandardMaterial({ color: 0x2e7d32, roughness: 0.7 })
  );
  pedicel.position.set(0, -1.2, 0); pedicel.castShadow = true; root.add(pedicel);
  const thalamus = new THREE.Mesh(
    new THREE.SphereGeometry(0.32, 16, 12),
    new THREE.MeshStandardMaterial({ color: 0x4caf50, roughness: 0.7 })
  );
  thalamus.scale.set(1.4, 0.6, 1.4); thalamus.position.set(0, -0.45, 0); root.add(thalamus);

  // ---- Build each whorl as its own group, so we can peel them ----
  const groups = {};

  // SEPALS (5 green sepals around the base)
  groups.sepal = new THREE.Group();
  const sepalMat = new THREE.MeshStandardMaterial({ color: 0x4caf50, roughness: 0.6, side: THREE.DoubleSide });
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2;
    const sh = new THREE.Shape();
    sh.moveTo(0, 0); sh.bezierCurveTo(0.3, 0.4, 0.2, 1.0, 0, 1.1); sh.bezierCurveTo(-0.2, 1.0, -0.3, 0.4, 0, 0);
    const geo = new THREE.ShapeGeometry(sh, 16);
    const m = new THREE.Mesh(geo, sepalMat); m.castShadow = true;
    m.position.set(Math.cos(a) * 0.3, -0.4, Math.sin(a) * 0.3);
    m.rotation.y = -a; m.rotation.z = -0.3;
    groups.sepal.add(m);
  }

  // PETALS (5 big red petals)
  groups.petal = new THREE.Group();
  const petalMat = new THREE.MeshStandardMaterial({ color: 0xe53935, roughness: 0.45, side: THREE.DoubleSide, emissive: 0x5a1410, emissiveIntensity: 0.15 });
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2;
    const sh = new THREE.Shape();
    sh.moveTo(0, 0); sh.bezierCurveTo(1.0, 0.5, 1.2, 2.4, 0, 3.0); sh.bezierCurveTo(-1.2, 2.4, -1.0, 0.5, 0, 0);
    const geo = new THREE.ShapeGeometry(sh, 24);
    // curve it
    const pos2 = geo.attributes.position;
    for (let v = 0; v < pos2.count; v++) {
      const y = pos2.getY(v);
      pos2.setZ(v, Math.sin(y * 0.6) * 0.15);
    }
    geo.computeVertexNormals();
    const m = new THREE.Mesh(geo, petalMat); m.castShadow = true;
    m.position.set(Math.cos(a) * 0.12, -0.3, Math.sin(a) * 0.12);
    m.rotation.y = -a; m.rotation.z = -0.5;
    groups.petal.add(m);
  }

  // STAMENS (filament + anther) — many
  groups.stamen = new THREE.Group();
  const filamentMat = new THREE.MeshStandardMaterial({ color: 0xfff59d, roughness: 0.5 });
  const antherMat = new THREE.MeshStandardMaterial({ color: 0xfbc02d, roughness: 0.4 });
  const stamens = [];
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2;
    const sg = new THREE.Group();
    const tube = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.04, 1.7, 8), filamentMat);
    tube.castShadow = true; sg.add(tube);
    const anther = new THREE.Mesh(new THREE.SphereGeometry(0.1, 12, 8), antherMat);
    anther.scale.set(0.7, 1.6, 0.7); anther.position.y = 0.95; anther.castShadow = true; sg.add(anther);
    const tilt = 0.15;
    sg.position.set(Math.cos(a) * 0.12, -0.2, Math.sin(a) * 0.12);
    sg.rotation.set(Math.sin(a) * tilt, -a, -Math.cos(a) * tilt);
    sg.userData.anther = anther;
    groups.stamen.add(sg); stamens.push(sg);
  }

  // CARPEL (stigma + style + ovary)
  groups.carpel = new THREE.Group();
  const styleMat = new THREE.MeshStandardMaterial({ color: 0xce93d8, roughness: 0.5 });
  const ovaryMat = new THREE.MeshStandardMaterial({ color: 0x7b1fa2, roughness: 0.5 });
  const stigmaMat = new THREE.MeshStandardMaterial({ color: 0xba68c8, roughness: 0.4, emissive: 0x4a148c, emissiveIntensity: 0.2 });
  const style = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 1.6, 12), styleMat);
  style.position.y = 0.0; style.castShadow = true; groups.carpel.add(style);
  const stigma = new THREE.Mesh(new THREE.SphereGeometry(0.16, 16, 12), stigmaMat);
  stigma.scale.set(1, 0.5, 1); stigma.position.y = 0.9; groups.carpel.add(stigma); groups.carpel.userData.stigma = stigma;
  const ovary = new THREE.Mesh(new THREE.SphereGeometry(0.3, 20, 16), ovaryMat);
  ovary.scale.set(1, 0.8, 1); ovary.position.y = -0.7; ovary.castShadow = true; groups.carpel.add(ovary);
  // ovules inside (visible when peeled deep)
  for (let i = 0; i < 4; i++) {
    const a = (i / 4) * Math.PI * 2;
    const ovule = new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8),
      new THREE.MeshStandardMaterial({ color: 0xffe082, roughness: 0.4 }));
    ovule.position.set(Math.cos(a) * 0.16, -0.7, Math.sin(a) * 0.16);
    groups.carpel.add(ovule);
  }

  Object.values(groups).forEach((g) => { root.add(g); });

  // Labels
  const labels = PARTS.map((p) => {
    const s = makeLabelSprite(p.name, { scale: 0.55, fontSize: 32 });
    s.visible = false; root.add(s); return s;
  });
  // Position labels at each whorl's ring
  function placeLabels() {
    labels[0].position.set(1.0, 0.0, 0);   // sepal
    labels[1].position.set(1.6, 1.6, 0);   // petal
    labels[2].position.set(1.0, 0.9, 0);   // stamen
    labels[3].position.set(0.4, 1.4, 0);   // carpel
  }
  placeLabels();

  // ---- Layer peeling: show only layers <= current ----
  let currentLayer = 3; // 0=sepal ... 3=carpel (deepest)
  function setLayer(n) {
    currentLayer = n;
    groups.sepal.visible = n >= 0;
    groups.petal.visible = n >= 1;
    groups.stamen.visible = n >= 2;
    groups.carpel.visible = n >= 3;
    // label only the topmost visible layer
    labels.forEach((l, i) => { l.visible = (i === n); });
    layerBadge.set(PARTS[n].name);
    layerBadge.el.style.setProperty('--ix-hud-color', '#a3e635');
  }

  const hud = createHud(stage);
  const layerBadge = hud.badge('Gynoecium (carpel)', '#a3e635');
  const hoverBadge = hud.badge('Drag the slider to dissect', '#84CC16');

  // Hover highlight: tap a part to read about it
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let downPos = null;
  function collectTargets() {
    const out = [];
    if (groups.sepal.visible) groups.sepal.children.forEach((m) => out.push({ m, p: PARTS[0] }));
    if (groups.petal.visible) groups.petal.children.forEach((m) => out.push({ m, p: PARTS[1] }));
    if (groups.stamen.visible) stamens.forEach((sg) => out.push({ m: sg.userData.anther, p: PARTS[2] }));
    if (groups.carpel.visible) out.push({ m: groups.carpel.userData.stigma, p: PARTS[3] });
    return out;
  }
  function onDown(e) { downPos = { x: e.clientX, y: e.clientY }; }
  function onUp(e) {
    if (!downPos || Math.hypot(e.clientX - downPos.x, e.clientY - downPos.y) > 8) return;
    const rect = engine.canvas.getBoundingClientRect();
    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const targets = collectTargets().map((t) => t.m);
    const hits = raycaster.intersectObjects(targets, false);
    if (hits.length) {
      const found = collectTargets().find((t) => t.m === hits[0].object);
      if (found) {
        showInfoCard(stage, { title: found.p.name, body: found.p.info, color: '#84CC16' });
      }
    }
  }
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);

  // ---- Pollination: a pollen grain you can drop onto the stigma ----
  const pollen = new THREE.Mesh(
    new THREE.SphereGeometry(0.12, 12, 10),
    new THREE.MeshStandardMaterial({ color: 0xffca28, roughness: 0.5, emissive: 0xffca28, emissiveIntensity: 0.2 })
  );
  pollen.position.set(2.5, 1.8, 0); pollen.castShadow = true; scene.add(pollen);
  let dragging = false; let pollenY = 1.8; let pollenTarget = new THREE.Vector3(2.5, 1.8, 0);
  let pollinated = false;
  function pollenDown(e) {
    const rect = engine.canvas.getBoundingClientRect();
    const sx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    const sy = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera({ x: sx, y: sy }, camera);
    if (raycaster.intersectObject(pollen, false).length) {
      dragging = true; if (engine.canvas.setPointerCapture) engine.canvas.setPointerCapture(e.pointerId);
    }
  }
  function pollenMove(e) {
    if (!dragging) return;
    const rect = engine.canvas.getBoundingClientRect();
    const sx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    const sy = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    // project onto a plane through the stigma at y
    const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    raycaster.setFromCamera({ x: sx, y: sy }, camera);
    const hit = new THREE.Vector3();
    raycaster.ray.intersectPlane(plane, hit);
    pollenTarget.copy(hit);
  }
  function pollenUp(e) {
    if (!dragging) return;
    dragging = false;
    // check proximity to stigma
    const stigmaWorld = new THREE.Vector3(); groups.carpel.userData.stigma.getWorldPosition(stigmaWorld);
    if (pollen.position.distanceTo(stigmaWorld) < 0.4 && !pollinated) {
      pollinated = true;
      showInfoCard(stage, {
        title: 'Pollination!',
        body: 'The pollen grain has landed on the sticky stigma. It will now grow a tube down the style into the ovary, where fertilisation occurs — and the ovary will swell into a fruit.',
        color: '#84CC16',
      });
    }
  }
  engine.canvas.addEventListener('pointerdown', pollenDown);
  engine.canvas.addEventListener('pointermove', pollenMove);
  engine.canvas.addEventListener('pointerup', pollenUp);

  const panel = createPanel(stage, { title: 'Flower Dissection' });
  panel.info('A flower is built in four rings. Drag the slider to peel back each whorl, tap any part to learn its job, then drag the pollen grain onto the stigma to pollinate.');
  panel.slider({
    label: 'Dissect to layer', min: 0, max: 3, step: 1, value: 3,
    format: (v) => PARTS[v].name,
    onChange: (v) => { setLayer(v); hideInfoCard(stage); },
  });
  panel.divider();
  PARTS.forEach((p) => {
    panel.button({
      label: p.name, icon: p.id === 'sepal' ? 'eco' : p.id === 'petal' ? 'local_florist' : p.id === 'stamen' ? 'grain' : 'spa',
      variant: 'ghost',
      onClick: () => { showInfoCard(stage, { title: p.name, body: p.info, color: '#84CC16' }); },
    });
  });
  panel.divider();
  panel.readout({ label: 'Floral whorls', value: '4' });
  panel.readout({ label: 'After fertilisation', value: 'ovary → fruit, ovules → seeds' });
  panel.toggle({ label: 'Slow spin', value: true, onChange: (v) => { spin = v; } });

  let spin = true;
  setLayer(3);

  engine.setUpdate((dt) => {
    if (spin) root.rotation.y += dt * 0.15;
    // pollen follow
    pollen.position.lerp(pollenTarget, 0.2);
    if (pollinated) {
      // stick to stigma
      const sw = new THREE.Vector3(); groups.carpel.userData.stigma.getWorldPosition(sw);
      pollen.position.lerp(sw, 0.3);
      pollen.material.emissiveIntensity = 0.3 + Math.sin(performance.now() * 0.005) * 0.2;
    }
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown);
      engine.canvas.removeEventListener('pointerup', onUp);
      engine.canvas.removeEventListener('pointerdown', pollenDown);
      engine.canvas.removeEventListener('pointermove', pollenMove);
      engine.canvas.removeEventListener('pointerup', pollenUp);
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
