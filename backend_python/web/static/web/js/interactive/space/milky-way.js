import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const GALAXY_RADIUS = 50;
const SUN_RADIUS = 26;

function makeStarTexture() {
  const c = document.createElement('canvas');
  c.width = 64;
  c.height = 64;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(32, 32, 1, 32, 32, 32);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.25, 'rgba(255,255,255,0.5)');
  g.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}

export default function init(stage) {
  const engine = createEngine(stage, { far: 2000 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;

  camera.position.set(0, 52, 78);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 10, maxDistance: 300, autoRotate: 0.02 });

  const count = quality.tier === 'low' ? 3000 : quality.tier === 'medium' ? 9000 : 16000;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const arms = 4;
  const armSpread = 0.34;
  const coreColor = new THREE.Color(0xffe2b0);
  const midColor = new THREE.Color(0xfff4e0);
  const armColor = new THREE.Color(0x9fb8ff);
  const tmpColor = new THREE.Color();

  for (let i = 0; i < count; i++) {
    const isBulge = i < count * 0.22;
    let x;
    let y;
    let z;
    let rNorm;
    if (isBulge) {
      const r = Math.pow(Math.random(), 2) * GALAXY_RADIUS * 0.2;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      x = r * Math.sin(phi) * Math.cos(theta);
      y = r * Math.cos(phi) * 0.62;
      z = r * Math.sin(phi) * Math.sin(theta);
      rNorm = r / GALAXY_RADIUS;
    } else {
      const t = Math.pow(Math.random(), 0.62);
      const r = 4 + t * (GALAXY_RADIUS - 4);
      const arm = i % arms;
      const baseAngle = Math.log(r / 3.2) / 0.28 + (arm * Math.PI * 2) / arms;
      const scatter = (Math.random() - 0.5) * armSpread * (1 + r / GALAXY_RADIUS);
      const angle = baseAngle + scatter;
      const wobble = (Math.random() - 0.5) * 2.2;
      x = Math.cos(angle) * r + wobble;
      z = Math.sin(angle) * r + wobble * 0.7;
      y = (Math.random() - 0.5) * (2.6 - 1.9 * (r / GALAXY_RADIUS));
      rNorm = r / GALAXY_RADIUS;
    }
    positions[i * 3] = x;
    positions[i * 3 + 1] = y;
    positions[i * 3 + 2] = z;
    if (rNorm < 0.3) tmpColor.copy(coreColor).lerp(midColor, rNorm / 0.3);
    else tmpColor.copy(midColor).lerp(armColor, (rNorm - 0.3) / 0.7);
    const jitter = 0.82 + Math.random() * 0.18;
    colors[i * 3] = tmpColor.r * jitter;
    colors[i * 3 + 1] = tmpColor.g * jitter;
    colors[i * 3 + 2] = tmpColor.b * jitter;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.PointsMaterial({
    size: quality.tier === 'low' ? 1.1 : 0.85,
    map: makeStarTexture(),
    vertexColors: true,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
  });
  const galaxy = new THREE.Points(geo, mat);
  scene.add(galaxy);

  const coreGlow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeStarTexture(),
    color: 0xffe0a8,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    opacity: 0.85,
  }));
  coreGlow.scale.set(26, 18, 1);
  galaxy.add(coreGlow);

  const bgGeo = new THREE.BufferGeometry();
  const bgCount = quality.tier === 'low' ? 400 : 1200;
  const bgPos = new Float32Array(bgCount * 3);
  for (let i = 0; i < bgCount; i++) {
    const r = 500 + Math.random() * 800;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    bgPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    bgPos[i * 3 + 1] = r * Math.cos(phi);
    bgPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  bgGeo.setAttribute('position', new THREE.BufferAttribute(bgPos, 3));
  scene.add(new THREE.Points(bgGeo, new THREE.PointsMaterial({ color: 0x8fa3c4, size: 1.1, sizeAttenuation: false })));

  const sunMarker = new THREE.Group();
  const sunAngle = Math.log(SUN_RADIUS / 3.2) / 0.28 + Math.PI / 2;
  sunMarker.position.set(Math.cos(sunAngle) * SUN_RADIUS, 0.6, Math.sin(sunAngle) * SUN_RADIUS);
  const sunDot = new THREE.Mesh(new THREE.SphereGeometry(0.55, 16, 16), new THREE.MeshBasicMaterial({ color: 0xffd24d }));
  sunMarker.add(sunDot);
  const ringGeo = new THREE.RingGeometry(1.1, 1.35, 32);
  const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: 0xffd24d, side: THREE.DoubleSide, transparent: true, opacity: 0.85 }));
  ring.rotation.x = Math.PI / 2;
  sunMarker.add(ring);
  const hereLabel = makeLabelSprite('\u2605 You are here \u2014 the Sun', { scale: 5, fontSize: 42, color: '#ffe3a3' });
  hereLabel.position.y = 4.2;
  sunMarker.add(hereLabel);
  galaxy.add(sunMarker);

  const coreLabel = makeLabelSprite('Galactic core \u00b7 Sagittarius A*', { scale: 4.4, fontSize: 40 });
  coreLabel.position.set(0, 7.5, 0);
  galaxy.add(coreLabel);
  const distLabel = makeLabelSprite('26,000 light-years from the core', { scale: 3.6, fontSize: 36, bg: 'rgba(11,28,48,0.55)' });
  distLabel.position.set(Math.cos(sunAngle) * SUN_RADIUS * 0.55, 2.6, Math.sin(sunAngle) * SUN_RADIUS * 0.55);
  galaxy.add(distLabel);

  const hud = createHud(stage);
  hud.badge('The Milky Way \u2014 100,000 light-years across', '#c4b5fd');
  hud.badge(`${count.toLocaleString()} of ~200,000,000,000 stars shown`, '#9ec1ff');

  let rotSpeed = 0.02;
  const panel = createPanel(stage, { title: 'Galaxy Controls' });
  panel.slider({
    label: 'Rotation speed',
    min: 0, max: 100, step: 5, value: 20,
    format: (v) => (v === 0 ? 'Paused' : `${v}%`),
    onChange: (v) => { rotSpeed = v / 1000; },
  });
  panel.toggle({
    label: 'Show labels',
    value: true,
    onChange: (v) => { hereLabel.visible = v; coreLabel.visible = v; distLabel.visible = v; },
  });
  panel.info('Each dot here stands in for millions of real stars \u2014 the actual galaxy holds about 200 billion. Our whole night sky \u2014 every star you have ever seen \u2014 sits inside a tiny bubble around the yellow marker.');

  let pulse = 0;
  engine.setUpdate((dt) => {
    galaxy.rotation.y += rotSpeed * dt * 10;
    pulse += dt * 2.4;
    const s = 1 + Math.sin(pulse) * 0.18;
    ring.scale.set(s, s, 1);
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
