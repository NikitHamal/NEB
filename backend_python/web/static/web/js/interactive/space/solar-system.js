import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import {
  applyRealisticRenderer, makeGlowTexture, makeRadialSprite, disposeObject,
} from '../core/realism.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

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

function planetTexture(p, size) {
  const c = document.createElement('canvas');
  c.width = size; c.height = size / 2;
  const ctx = c.getContext('2d');
  const base = new THREE.Color(p.color);
  ctx.fillStyle = `rgb(${base.r * 255 | 0},${base.g * 255 | 0},${base.b * 255 | 0})`;
  ctx.fillRect(0, 0, size, size / 2);
  if (p.banded) {
    const band = new THREE.Color(p.band);
    for (let i = 0; i < 14; i++) {
      const y = (i / 14) * size / 2;
      const h = (size / 2) / 14;
      ctx.fillStyle = `rgba(${band.r * 255 | 0},${band.g * 255 | 0},${band.b * 255 | 0},${0.15 + Math.random() * 0.35})`;
      ctx.fillRect(0, y, size, h * (0.5 + Math.random() * 0.6));
    }
    ctx.fillStyle = '#a8482a';
    ctx.beginPath();
    ctx.ellipse(size * 0.32, size * 0.16, size * 0.06, size * 0.035, 0, 0, Math.PI * 2);
    ctx.fill();
  } else if (p.land) {
    const land = new THREE.Color(p.land);
    for (let i = 0; i < 50; i++) {
      const x = Math.random() * size, y = Math.random() * size / 2;
      const r = 6 + Math.random() * 24;
      ctx.fillStyle = `rgba(${land.r * 255 | 0},${land.g * 255 | 0},${land.b * 255 | 0},0.55)`;
      ctx.beginPath();
      ctx.ellipse(x, y, r, r * (0.5 + Math.random() * 0.5), Math.random() * Math.PI, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = 'rgba(255,255,255,0.55)';
    for (let i = 0; i < 14; i++) {
      ctx.beginPath();
      ctx.ellipse(Math.random() * size, Math.random() * size / 2, 6 + Math.random() * 10, 3 + Math.random() * 5, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  } else {
    for (let i = 0; i < 32; i++) {
      const x = Math.random() * size, y = Math.random() * size / 2;
      const r = 8 + Math.random() * 28;
      ctx.fillStyle = `rgba(255,255,255,${0.04 + Math.random() * 0.08})`;
      ctx.beginPath(); ctx.ellipse(x, y, r, r * 0.6, 0, 0, Math.PI * 2); ctx.fill();
    }
    for (let i = 0; i < 16; i++) {
      const x = Math.random() * size, y = Math.random() * size / 2;
      const r = 4 + Math.random() * 12;
      ctx.fillStyle = `rgba(0,0,0,${0.06 + Math.random() * 0.1})`;
      ctx.beginPath(); ctx.ellipse(x, y, r, r * 0.6, 0, 0, Math.PI * 2); ctx.fill();
    }
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 2;
  return tex;
}

function ringTexture() {
  const c = document.createElement('canvas');
  c.width = 256; c.height = 32;
  const ctx = c.getContext('2d');
  const g = ctx.createLinearGradient(0, 0, 256, 0);
  g.addColorStop(0.0, 'rgba(0,0,0,0)');
  g.addColorStop(0.05, 'rgba(232,213,163,0.85)');
  g.addColorStop(0.4, 'rgba(200,168,116,0.65)');
  g.addColorStop(0.55, 'rgba(0,0,0,0)');
  g.addColorStop(0.6, 'rgba(200,168,116,0.65)');
  g.addColorStop(0.95, 'rgba(232,213,163,0.85)');
  g.addColorStop(1.0, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 256, 32);
  for (let i = 0; i < 24; i++) {
    ctx.fillStyle = `rgba(0,0,0,${0.05 + Math.random() * 0.18})`;
    ctx.fillRect(Math.random() * 256, 0, 1 + Math.random() * 2, 32);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

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

  const starCount = tier === 'low' ? 600 : tier === 'medium' ? 1800 : 3200;
  const starGeo = new THREE.BufferGeometry();
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    const r = 600 + Math.random() * 1100;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPos[i * 3 + 1] = r * Math.cos(phi);
    starPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({
    color: 0xc8d6ee, size: 1.5, sizeAttenuation: false, transparent: true, opacity: 0.9,
  })));

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

  const sun = new THREE.Mesh(
    new THREE.SphereGeometry(4.6, seg, seg),
    new THREE.MeshBasicMaterial({ color: 0xffd060 })
  );
  sun.name = 'Sun';
  scene.add(sun);
  const sunInnerGlow = makeRadialSprite(glowTex, { scale: 14, color: 0xffc060, opacity: 0.95 });
  sun.add(sunInnerGlow);
  const sunOuterGlow = makeRadialSprite(glowTex, { scale: 30, color: 0xffa040, opacity: 0.55 });
  sun.add(sunOuterGlow);
  if (tier !== 'low') {
    const sunFarGlow = makeRadialSprite(glowTex, { scale: 60, color: 0xff7a30, opacity: 0.22 });
    sun.add(sunFarGlow);
  }

  const planetGroup = new THREE.Group();
  scene.add(planetGroup);
  const clickables = [{ mesh: sun, name: 'Sun', info: 'Our star — a giant ball of glowing gas. The Sun holds 99.8% of all the mass in the solar system and gives us light and warmth.' }];
  const labels = [];
  const sharedOrbitMat = new THREE.LineBasicMaterial({ color: 0x4a6090, transparent: true, opacity: 0.4 });
  const sharedRingTex = ringTexture();

  PLANETS.forEach((p) => {
    const pivot = new THREE.Object3D();
    pivot.rotation.y = Math.random() * Math.PI * 2;
    planetGroup.add(pivot);

    const tex = planetTexture(p, texSize);
    const mat = new THREE.MeshStandardMaterial({ map: tex, color: 0xffffff, roughness: 0.85, metalness: 0.0 });
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(p.radius, seg, seg), mat);
    mesh.position.x = p.dist;
    mesh.castShadow = useShadows;
    mesh.receiveShadow = useShadows;
    mesh.name = p.name;
    pivot.add(mesh);
    p._tex = tex;

    if (p.atmo && p.atmo !== 0x000000) {
      const atmoMat = new THREE.MeshBasicMaterial({
        color: p.atmo, transparent: true, opacity: 0.18, side: THREE.BackSide, depthWrite: false,
      });
      const atmo = new THREE.Mesh(new THREE.SphereGeometry(p.radius * 1.08, seg, seg), atmoMat);
      mesh.add(atmo);
      if (useAtmoGlow) {
        const atmoGlow = makeRadialSprite(glowTex, {
          scale: p.radius * 3.4, color: p.atmo, opacity: 0.4,
        });
        mesh.add(atmoGlow);
      }
    }

    if (p.rings) {
      const ringGeo = new THREE.RingGeometry(p.radius * 1.5, p.radius * 2.45, seg * 2, 1);
      const pos = ringGeo.attributes.position;
      const v3 = new THREE.Vector3();
      const inner = p.radius * 1.5, outer = p.radius * 2.45;
      for (let i = 0; i < pos.count; i++) {
        v3.fromBufferAttribute(pos, i);
        const r = v3.length();
        ringGeo.attributes.uv.setXY(i, (r - inner) / (outer - inner), 1);
      }
      const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({
        map: sharedRingTex, side: THREE.DoubleSide, transparent: true, opacity: 0.9, depthWrite: false,
      }));
      ring.rotation.x = Math.PI / 2.25;
      mesh.add(ring);
    }

    let moonPivot = null;
    if (p.hasMoon) {
      moonPivot = new THREE.Object3D();
      mesh.add(moonPivot);
      const moon = new THREE.Mesh(
        new THREE.SphereGeometry(0.27, Math.max(10, seg / 2), Math.max(10, seg / 2)),
        new THREE.MeshStandardMaterial({ color: 0xc8c4be, roughness: 1 })
      );
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
    sunInnerGlow.scale.setScalar(14 * pulse);
    sunOuterGlow.scale.setScalar(30 * pulse);
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
      PLANETS.forEach((p) => { if (p._tex) p._tex.dispose(); });
      sharedRingTex.dispose();
      engine.dispose();
    },
  };
}
