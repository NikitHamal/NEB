import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
const TILT = THREE.MathUtils.degToRad(23.5);
const EARTH_DIST = 26;
const MOON_DIST = 3.2;

function makeGlowTexture(inner, mid) {
  const c = document.createElement('canvas');
  c.width = 128;
  c.height = 128;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(64, 64, 6, 64, 64, 64);
  g.addColorStop(0, inner);
  g.addColorStop(0.35, mid);
  g.addColorStop(1, 'rgba(255,150,40,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 128, 128);
  return new THREE.CanvasTexture(c);
}

export default function init(stage) {
  const engine = createEngine(stage, { far: 3000 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 30, 58);
  let controls = createOrbitControls(camera, engine.canvas, { minDistance: 4, maxDistance: 160 });

  const starGeo = new THREE.BufferGeometry();
  const starCount = quality.tier === 'low' ? 600 : 1800;
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    const r = 400 + Math.random() * 700;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPos[i * 3 + 1] = r * Math.cos(phi);
    starPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xbfd0e8, size: 1.3, sizeAttenuation: false })));

  scene.add(new THREE.AmbientLight(0xffffff, 0.14));
  const sunLight = new THREE.PointLight(0xfff2d8, 2400, 0, 2);
  scene.add(sunLight);

  const sun = new THREE.Mesh(new THREE.SphereGeometry(4.2, seg, seg), new THREE.MeshBasicMaterial({ color: 0xffc24d }));
  scene.add(sun);
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(255,210,120,0.85)', 'rgba(255,170,60,0.32)'),
    transparent: true,
    depthWrite: false,
    color: 0xffb340,
  }));
  glow.scale.set(19, 19, 1);
  sun.add(glow);

  const earthGroup = new THREE.Group();
  scene.add(earthGroup);

  const tiltGroup = new THREE.Group();
  tiltGroup.rotation.z = -TILT;
  earthGroup.add(tiltGroup);

  const earth = new THREE.Mesh(
    new THREE.SphereGeometry(1.5, seg, seg),
    new THREE.MeshStandardMaterial({ color: 0x4d7fff, roughness: 0.75, metalness: 0.05 })
  );
  tiltGroup.add(earth);

  const landMat = new THREE.MeshStandardMaterial({ color: 0x3fae6a, roughness: 0.95, transparent: true, opacity: 0.85 });
  for (let i = 0; i < 7; i++) {
    const blob = new THREE.Mesh(new THREE.SphereGeometry(0.45 + Math.random() * 0.35, Math.max(8, seg / 3), Math.max(8, seg / 3)), landMat);
    const th = Math.random() * Math.PI * 2;
    const ph = Math.acos(2 * Math.random() - 1);
    blob.position.setFromSphericalCoords(1.32, ph, th);
    blob.scale.z = 0.35;
    blob.lookAt(0, 0, 0);
    earth.add(blob);
  }

  const axisGeo = new THREE.CylinderGeometry(0.04, 0.04, 5.4, 8);
  const axis = new THREE.Mesh(axisGeo, new THREE.MeshBasicMaterial({ color: 0xff6b81 }));
  tiltGroup.add(axis);
  const axisTip = new THREE.Mesh(new THREE.ConeGeometry(0.14, 0.4, 8), new THREE.MeshBasicMaterial({ color: 0xff6b81 }));
  axisTip.position.y = 2.7;
  tiltGroup.add(axisTip);

  const earthLabel = makeLabelSprite('Earth', { scale: 1.6, fontSize: 38 });
  earthLabel.position.y = 3.4;
  earthGroup.add(earthLabel);

  const moonPivot = new THREE.Group();
  earthGroup.add(moonPivot);
  const moon = new THREE.Mesh(
    new THREE.SphereGeometry(0.42, Math.max(10, seg / 2), Math.max(10, seg / 2)),
    new THREE.MeshStandardMaterial({ color: 0xb8b8b8, roughness: 1 })
  );
  moon.position.x = MOON_DIST;
  moonPivot.add(moon);

  function circleLine(radius, color, opacity) {
    const pts = [];
    const n = 128;
    for (let i = 0; i <= n; i++) {
      const a = (i / n) * Math.PI * 2;
      pts.push(Math.cos(a) * radius, 0, Math.sin(a) * radius);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts), 3));
    return new THREE.Line(g, new THREE.LineBasicMaterial({ color, transparent: true, opacity }));
  }

  const earthOrbit = circleLine(EARTH_DIST, 0x3a4f70, 0.6);
  scene.add(earthOrbit);
  const moonOrbit = circleLine(MOON_DIST, 0x5a6f90, 0.5);
  earthGroup.add(moonOrbit);

  const seasonMarkers = [];
  [['Jun solstice', Math.PI], ['Dec solstice', 0], ['Mar equinox', Math.PI / 2], ['Sep equinox', -Math.PI / 2]].forEach(([txt, ang]) => {
    const m = makeLabelSprite(txt, { scale: 1.5, fontSize: 34, bg: 'rgba(11,28,48,0.6)' });
    m.position.set(Math.cos(ang) * (EARTH_DIST + 4.5), 0.4, -Math.sin(ang) * (EARTH_DIST + 4.5));
    scene.add(m);
    seasonMarkers.push(m);
  });

  const hud = createHud(stage);
  const monthBadge = hud.badge('January', '#9ec1ff');
  const seasonBadge = hud.badge('Winter in Nepal', '#8be9a8');

  let speed = 10;
  let orbitAngle = Math.PI * 0.3;
  let moonAngle = 0;
  let view = 'wide';

  const panel = createPanel(stage, { title: 'Earth · Moon · Sun' });
  panel.slider({
    label: 'Time speed',
    min: 0, max: 40, step: 1, value: speed,
    format: (v) => (v === 0 ? 'Paused' : `${v} days/s`),
    onChange: (v) => { speed = v; },
  });
  panel.toggle({ label: 'Show Earth axis', value: true, onChange: (v) => { axis.visible = v; axisTip.visible = v; } });
  panel.toggle({
    label: 'Show orbit lines',
    value: true,
    onChange: (v) => { earthOrbit.visible = v; moonOrbit.visible = v; seasonMarkers.forEach((m) => { m.visible = v; }); },
  });
  panel.select({
    label: 'Camera view',
    options: [
      { value: 'wide', label: 'View from space' },
      { value: 'follow', label: 'Follow Earth' },
      { value: 'seasons', label: 'Season view (side-on)' },
    ],
    value: 'wide',
    onChange: (v) => { view = v; applyView(); },
  });
  panel.info('Watch the day/night line on Earth, and how the tilted axis keeps pointing the same way all year — that is what makes the seasons. Earth\u2019s spin is slowed down so you can watch it. Sizes and distances are not to scale.');

  function applyView() {
    controls.dispose();
    if (view === 'wide') {
      camera.position.set(0, 30, 58);
      controls = createOrbitControls(camera, engine.canvas, { minDistance: 4, maxDistance: 160 });
    } else if (view === 'seasons') {
      const p = earthGroup.position;
      camera.position.set(p.x * 1.32, 2.5, p.z * 1.32 + 0.01);
      controls = createOrbitControls(camera, engine.canvas, { minDistance: 3, maxDistance: 160, target: p });
    } else {
      const p = earthGroup.position;
      camera.position.set(p.x + 5, 4, p.z + 7);
      controls = createOrbitControls(camera, engine.canvas, { minDistance: 3, maxDistance: 160, target: p });
    }
  }

  function dayOfYear() {
    const f = ((orbitAngle / (Math.PI * 2)) % 1 + 1) % 1;
    return (f * 365.25 + 355) % 365.25;
  }

  function monthName(doy) {
    let d = doy;
    for (let i = 0; i < 12; i++) {
      if (d < MONTH_DAYS[i]) return MONTHS[i];
      d -= MONTH_DAYS[i];
    }
    return 'Dec';
  }

  function seasonName(doy) {
    if (doy < 79 || doy >= 355) return 'Winter in Nepal';
    if (doy < 172) return 'Spring in Nepal';
    if (doy < 266) return 'Summer in Nepal';
    return 'Autumn in Nepal';
  }

  const worldPos = new THREE.Vector3();
  engine.setUpdate((dt) => {
    const days = dt * speed;
    orbitAngle += (days * Math.PI * 2) / 365.25;
    moonAngle += (days * Math.PI * 2) / 27.3;
    earthGroup.position.set(Math.cos(orbitAngle) * EARTH_DIST, 0, -Math.sin(orbitAngle) * EARTH_DIST);
    earth.rotation.y += days * Math.PI * 2 * 0.35;
    moonPivot.rotation.y = moonAngle;
    const doy = dayOfYear();
    monthBadge.set(monthName(doy));
    seasonBadge.set(seasonName(doy));
    if (view !== 'wide') {
      earthGroup.getWorldPosition(worldPos);
      controls.setTarget(worldPos);
    }
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
