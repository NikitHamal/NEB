import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

const PLANETS = [
  { name: 'Mercury', radius: 0.38, dist: 10, period: 0.24, color: 0x9c8e84, info: 'The smallest planet and closest to the Sun. A year on Mercury lasts just 88 Earth days, and daytime is hot enough to melt lead!' },
  { name: 'Venus', radius: 0.95, dist: 14, period: 0.62, color: 0xe6c98e, info: 'The hottest planet (about 465°C) because its thick clouds trap heat. Venus spins backwards compared to most planets.' },
  { name: 'Earth', radius: 1.0, dist: 18, period: 1.0, color: 0x4d7fff, hasMoon: true, info: 'Our home! The only known world with liquid water oceans and life. It takes 365.25 days to orbit the Sun.' },
  { name: 'Mars', radius: 0.53, dist: 23, period: 1.88, color: 0xd96a45, info: 'The red planet — its color comes from rusty iron dust. Mars has the tallest volcano in the solar system, Olympus Mons.' },
  { name: 'Jupiter', radius: 3.4, dist: 32, period: 11.86, color: 0xd8b48a, banded: true, info: 'The giant of the family — more than 1,300 Earths could fit inside! Its Great Red Spot is a storm bigger than Earth.' },
  { name: 'Saturn', radius: 2.9, dist: 42, period: 29.46, color: 0xe8d5a3, rings: true, info: 'Famous for its dazzling rings made of billions of pieces of ice and rock. Saturn is so light it would float in water!' },
  { name: 'Uranus', radius: 1.9, dist: 51, period: 84.0, color: 0x9fd8e0, info: 'An ice giant that rolls around the Sun on its side, like a ball. Its seasons last 21 Earth years each.' },
  { name: 'Neptune', radius: 1.85, dist: 59, period: 164.8, color: 0x4862d8, info: 'The windiest planet — storms blow at over 2,000 km/h. Neptune was found with math before anyone saw it in a telescope.' },
];

export default function init(stage) {
  const engine = createEngine(stage, { far: 4000 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 38, 78);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 6,
    maxDistance: 220,
    autoRotate: 0.03,
  });

  const starGeo = new THREE.BufferGeometry();
  const starCount = quality.tier === 'low' ? 800 : 2200;
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    const r = 500 + Math.random() * 900;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPos[i * 3 + 1] = r * Math.cos(phi);
    starPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xbfd0e8, size: 1.4, sizeAttenuation: false })));

  scene.add(new THREE.AmbientLight(0xffffff, 0.22));
  const sunLight = new THREE.PointLight(0xfff2d8, 2600, 0, 2);
  scene.add(sunLight);

  const sun = new THREE.Mesh(
    new THREE.SphereGeometry(4.6, seg, seg),
    new THREE.MeshBasicMaterial({ color: 0xffc24d })
  );
  sun.name = 'Sun';
  scene.add(sun);

  const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: makeGlowTexture(), color: 0xffb340, transparent: true, depthWrite: false }));
  glow.scale.set(20, 20, 1);
  sun.add(glow);

  const planetGroup = new THREE.Group();
  scene.add(planetGroup);
  const clickables = [{ mesh: sun, name: 'Sun', info: 'Our star — a giant ball of glowing gas. The Sun holds 99.8% of all the mass in the solar system and gives us light and warmth.' }];
  const labels = [];

  PLANETS.forEach((p) => {
    const pivot = new THREE.Object3D();
    pivot.rotation.y = Math.random() * Math.PI * 2;
    planetGroup.add(pivot);

    const mat = new THREE.MeshStandardMaterial({ color: p.color, roughness: 0.85, metalness: 0.05 });
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(p.radius, seg, seg), mat);
    mesh.position.x = p.dist;
    mesh.name = p.name;
    pivot.add(mesh);

    if (p.banded) {
      const band = new THREE.Mesh(
        new THREE.SphereGeometry(p.radius * 1.004, seg, seg),
        new THREE.MeshStandardMaterial({ color: 0xb08a5e, transparent: true, opacity: 0.35, roughness: 1 })
      );
      band.scale.y = 0.55;
      mesh.add(band);
    }

    if (p.rings) {
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(p.radius * 1.5, p.radius * 2.45, seg * 2),
        new THREE.MeshBasicMaterial({ color: 0xcdba8c, side: THREE.DoubleSide, transparent: true, opacity: 0.7 })
      );
      ring.rotation.x = Math.PI / 2.25;
      mesh.add(ring);
    }

    let moonPivot = null;
    if (p.hasMoon) {
      moonPivot = new THREE.Object3D();
      mesh.add(moonPivot);
      const moon = new THREE.Mesh(
        new THREE.SphereGeometry(0.27, Math.max(10, seg / 2), Math.max(10, seg / 2)),
        new THREE.MeshStandardMaterial({ color: 0xb8b8b8, roughness: 1 })
      );
      moon.position.x = 2.0;
      moonPivot.add(moon);
    }

    const orbitGeo = new THREE.BufferGeometry();
    const pts = [];
    const n = 96;
    for (let i = 0; i <= n; i++) {
      const a = (i / n) * Math.PI * 2;
      pts.push(Math.cos(a) * p.dist, 0, Math.sin(a) * p.dist);
    }
    orbitGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts), 3));
    const orbit = new THREE.Line(orbitGeo, new THREE.LineBasicMaterial({ color: 0x3a4f70, transparent: true, opacity: 0.55 }));
    scene.add(orbit);

    const label = makeLabelSprite(p.name, { scale: 2.2, fontSize: 40 });
    label.position.y = p.radius + 1.6;
    mesh.add(label);
    labels.push(label);

    clickables.push({ mesh, name: p.name, info: p.info });
    p._pivot = pivot;
    p._mesh = mesh;
    p._moonPivot = moonPivot;
    p._orbit = orbit;
  });

  const hud = createHud(stage);
  const dayBadge = hud.badge('Day 0');

  const panel = createPanel(stage, { title: 'Solar System Controls' });
  let speed = 8;
  let elapsedDays = 0;
  let followTarget = null;

  panel.slider({
    label: 'Time speed',
    min: 0, max: 60, step: 1, value: speed,
    format: (v) => (v === 0 ? 'Paused' : `${v} days/s`),
    onChange: (v) => { speed = v; },
  });
  panel.toggle({
    label: 'Show orbit paths',
    value: true,
    onChange: (v) => PLANETS.forEach((p) => { p._orbit.visible = v; }),
  });
  panel.toggle({
    label: 'Show names',
    value: true,
    onChange: (v) => labels.forEach((l) => { l.visible = v; }),
  });
  panel.select({
    label: 'Fly to',
    options: ['Free view', 'Sun', ...PLANETS.map((p) => p.name)],
    value: 'Free view',
    onChange: (name) => {
      if (name === 'Free view') { followTarget = null; controls.setTarget(new THREE.Vector3(0, 0, 0)); controls.setDistance(85); return; }
      if (name === 'Sun') { followTarget = sun; controls.setDistance(16); return; }
      const p = PLANETS.find((x) => x.name === name);
      if (p) { followTarget = p._mesh; controls.setDistance(Math.max(4, p.radius * 5)); }
    },
  });
  panel.info('Tap a planet to learn about it. Drag to look around, pinch or scroll to zoom. Sizes and distances are not to scale.');

  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let downPos = null;
  function onCanvasDown(e) { downPos = { x: e.clientX, y: e.clientY }; }
  function onCanvasUp(e) {
    if (!downPos || Math.hypot(e.clientX - downPos.x, e.clientY - downPos.y) > 8) return;
    const rect = engine.canvas.getBoundingClientRect();
    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(clickables.map((c) => c.mesh), true);
    if (hits.length) {
      let obj = hits[0].object;
      while (obj && !clickables.find((c) => c.mesh === obj)) obj = obj.parent;
      const item = clickables.find((c) => c.mesh === obj);
      if (item) showInfoCard(stage, { title: item.name, body: item.info, color: '#8B5CF6' });
    }
  }
  engine.canvas.addEventListener('pointerdown', onCanvasDown);
  engine.canvas.addEventListener('pointerup', onCanvasUp);

  const worldPos = new THREE.Vector3();
  engine.setUpdate((dt) => {
    elapsedDays += dt * speed;
    dayBadge.set(`Day ${Math.floor(elapsedDays)}`);
    sun.rotation.y += dt * 0.05;
    PLANETS.forEach((p) => {
      p._pivot.rotation.y += (dt * speed * 2 * Math.PI) / (p.period * 365.25);
      p._mesh.rotation.y += dt * 0.4;
      if (p._moonPivot) p._moonPivot.rotation.y += (dt * speed * 2 * Math.PI) / 27.3;
    });
    if (followTarget) {
      followTarget.getWorldPosition(worldPos);
      controls.setTarget(worldPos);
    }
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onCanvasDown);
      engine.canvas.removeEventListener('pointerup', onCanvasUp);
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}

function makeGlowTexture() {
  const c = document.createElement('canvas');
  c.width = 128;
  c.height = 128;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(64, 64, 6, 64, 64, 64);
  g.addColorStop(0, 'rgba(255,210,120,0.85)');
  g.addColorStop(0.35, 'rgba(255,170,60,0.32)');
  g.addColorStop(1, 'rgba(255,150,40,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 128, 128);
  return new THREE.CanvasTexture(c);
}
