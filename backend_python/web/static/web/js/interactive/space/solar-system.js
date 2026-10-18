import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import {
  applyRealisticRenderer, makeGlowTexture, makeRadialSprite, disposeObject,
} from '../core/realism.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { bodyMaterial, earthWithClouds, atmosphere, sun as makeSun, saturnRings, starfield, body } from '../core/space-kit.js';

const PLANETS = [
  { name: 'Mercury', radius: 0.38, dist: 10, period: 0.24, color: 0x9c8e84, atmo: 0x000000, info: 'The smallest planet and closest to the Sun. A year on Mercury lasts just 88 Earth days, and daytime is hot enough to melt lead!' },
  { name: 'Venus', radius: 0.95, dist: 14, period: 0.62, color: 0xe6c98e, atmo: 0xffd9a0, info: 'The hottest planet (about 465°C) because its thick clouds trap heat. Venus spins backwards compared to most planets.' },
  { name: 'Earth', radius: 1.0, dist: 18, period: 1.0, color: 0x2b6fd6, land: 0x3f8a3f, atmo: 0x8fc4ff, hasMoon: true, info: 'Our home! The only known world with liquid water oceans and life. It takes 365.25 days to orbit the Sun.' },
  { name: 'Mars', radius: 0.53, dist: 23, period: 1.88, color: 0xc1542e, atmo: 0xff9a6a, info: 'The red planet — its color comes from rusty iron dust. Mars has the tallest volcano in the solar system, Olympus Mons.' },
  { name: 'Jupiter', radius: 3.4, dist: 32, period: 11.86, color: 0xd8b48a, band: 0x9c6f44, atmo: 0xffd9b0, banded: true, info: 'The giant of the family — more than 1,300 Earths could fit inside! Its Great Red Spot is a storm bigger than Earth.' },
  { name: 'Saturn', radius: 2.9, dist: 42, period: 29.46, color: 0xe8d5a3, band: 0xc8a874, atmo: 0xffe9c0, rings: true, info: 'Famous for its dazzling rings made of billions of pieces of ice and rock. Saturn is so light it would float in water!' },
  { name: 'Uranus', radius: 1.9, dist: 51, period: 84.0, color: 0x9fd8e0, atmo: 0xbff0f5, info: 'An ice giant that rolls around the Sun on its side, like a ball. Its seasons last 21 Earth years each.' },
  { name: 'Neptune', radius: 1.85, dist: 59, period: 164.8, color: 0x2a4dd0, atmo: 0x6080ff, info: 'The windiest planet — storms blow at over 2,000 km/h. Neptune was found with math before anyone saw it in a telescope.' },
];

export default function init(stage) {
  const engine = createEngine(stage, { far: 6000, shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const tier = quality.tier;
  const seg = tier === 'low' ? 16 : tier === 'medium' ? 24 : 48;
  const texSize = tier === 'low' ? 128 : 256;
  const useShadows = quality.shadows && tier !== 'low';
  const useAtmoGlow = tier !== 'low';
  const useNebulae = tier === 'high';

  applyRealisticRenderer(engine, { exposure: 0.95, env: false, shadows: useShadows });
  scene.background = new THREE.Color(0x05070f);

  camera.position.set(0, 38, 78);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 6, maxDistance: 230, autoRotate: 0.03,
  });

  // the sky: real star colours, and the Milky Way across it
  scene.add(starfield(quality, 1500));

  const glowTex = makeGlowTexture('rgba(255,255,240,1)', 'rgba(255,200,90,0.85)', 'rgba(255,160,50,0)');

  if (useNebulae) {
    const nebula = makeRadialSprite(glowTex, { scale: 1400, color: 0x6a4ab0, opacity: 0.4 });
    nebula.position.set(-400, 200, -900);
    scene.add(nebula);
    const nebula2 = makeRadialSprite(glowTex, { scale: 1100, color: 0x4080b0, opacity: 0.35 });
    nebula2.position.set(500, -120, -700);
    scene.add(nebula2);
  }

  scene.add(new THREE.AmbientLight(0x202840, 0.2));
  const sunLight = new THREE.PointLight(0xfff0d0, 3200, 0, 1.9);
  if (useShadows) {
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.set(tier === 'medium' ? 512 : 1024, tier === 'medium' ? 512 : 1024);
    sunLight.shadow.camera.near = 1;
    sunLight.shadow.camera.far = 200;
    sunLight.shadow.bias = -0.0005;
  }
  scene.add(sunLight);

  // a granulated photosphere with a layered corona
  const sun = makeSun(4.6, quality);
  sun.name = 'Sun';
  scene.add(sun);

  const planetGroup = new THREE.Group();
  scene.add(planetGroup);
  const clickables = [{ mesh: sun, name: 'Sun', info: 'Our star — a giant ball of glowing gas. The Sun holds 99.8% of all the mass in the solar system and gives us light and warmth.' }];
  const labels = [];
  const sharedOrbitMat = new THREE.LineBasicMaterial({ color: 0x4a6090, transparent: true, opacity: 0.4 });

  PLANETS.forEach((p) => {
    const pivot = new THREE.Object3D();
    pivot.rotation.y = Math.random() * Math.PI * 2;
    planetGroup.add(pivot);

    // each world's own procedural surface; Earth carries its drifting cloud deck
    const key = p.name.toLowerCase();
    const mesh = key === 'earth' ? earthWithClouds(p.radius, quality) : body(key, p.radius, quality);
    mesh.position.x = p.dist;
    mesh.castShadow = useShadows;
    mesh.receiveShadow = useShadows;
    mesh.name = p.name;
    pivot.add(mesh);

    if (p.atmo && p.atmo !== 0x000000 && key !== 'earth') mesh.add(atmosphere(p.radius, p.atmo, 1.08, 3.4, 0.7));

    if (p.rings) {
      const ring = saturnRings(p.radius * 1.24, p.radius * 2.3);
      ring.rotation.x = -Math.PI / 2 + 0.47;
      mesh.add(ring);
    }

    let moonPivot = null;
    if (p.hasMoon) {
      moonPivot = new THREE.Object3D();
      mesh.add(moonPivot);
      const moon = body('moon', 0.27, quality);
      moon.position.x = 2.0;
      moon.castShadow = useShadows;
      moonPivot.add(moon);
    }

    const orbitGeo = new THREE.BufferGeometry();
    const pts = [];
    const n = tier === 'low' ? 64 : 128;
    for (let i = 0; i <= n; i++) {
      const a = (i / n) * Math.PI * 2;
      pts.push(Math.cos(a) * p.dist, 0, Math.sin(a) * p.dist);
    }
    orbitGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts), 3));
    const orbit = new THREE.Line(orbitGeo, sharedOrbitMat);
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
    label: 'Time speed', min: 0, max: 60, step: 1, value: speed,
    format: (v) => (v === 0 ? 'Paused' : `${v} days/s`),
    onChange: (v) => { speed = v; },
  });
  panel.toggle({
    label: 'Show orbit paths', value: true,
    onChange: (v) => PLANETS.forEach((p) => { p._orbit.visible = v; }),
  });
  panel.toggle({
    label: 'Show names', value: true,
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
  panel.info('Drag to look around, pinch or scroll to zoom. Tap a planet to learn about it. Sizes and distances are not to scale.');

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
    const pulse = 1 + Math.sin(elapsedDays * 0.3) * 0.04;
    sun.children.forEach((c, i) => { if (c.isSprite) c.scale.setScalar(4.6 * [2.6, 5.0, 9.0][i] * pulse); });
    PLANETS.forEach((p) => {
      p._pivot.rotation.y += (dt * speed * 2 * Math.PI) / (p.period * 365.25);
      p._mesh.rotation.y += dt * 0.4;
      if (p._mesh.userData.clouds) p._mesh.userData.clouds.rotation.y += dt * 0.05;
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
