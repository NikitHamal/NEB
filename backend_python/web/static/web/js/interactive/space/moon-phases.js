import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MOON_DIST = 7;
const PHASES = [
  ['New Moon (aunsi)', '#aab6c8'],
  ['Waxing Crescent', '#c8d2e0'],
  ['First Quarter', '#dce4f0'],
  ['Waxing Gibbous', '#eef2f8'],
  ['Full Moon (purnima)', '#fff7d6'],
  ['Waning Gibbous', '#eef2f8'],
  ['Last Quarter', '#dce4f0'],
  ['Waning Crescent', '#c8d2e0'],
];

export default function init(stage) {
  const engine = createEngine(stage, { far: 3000 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 16, 22);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 4, maxDistance: 80 });

  const starGeo = new THREE.BufferGeometry();
  const starCount = quality.tier === 'low' ? 500 : 1500;
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    const r = 300 + Math.random() * 500;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPos[i * 3 + 1] = r * Math.cos(phi);
    starPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xbfd0e8, size: 1.3, sizeAttenuation: false })));

  scene.add(new THREE.AmbientLight(0xffffff, 0.12));
  const sunDir = new THREE.DirectionalLight(0xfff4dd, 2.6);
  sunDir.position.set(60, 0, 0);
  scene.add(sunDir);

  const sunBall = new THREE.Mesh(new THREE.SphereGeometry(3, seg, seg), new THREE.MeshBasicMaterial({ color: 0xffc24d }));
  sunBall.position.set(60, 0, 0);
  scene.add(sunBall);
  const glowCanvas = document.createElement('canvas');
  glowCanvas.width = 128;
  glowCanvas.height = 128;
  const gctx = glowCanvas.getContext('2d');
  const grad = gctx.createRadialGradient(64, 64, 6, 64, 64, 64);
  grad.addColorStop(0, 'rgba(255,210,120,0.9)');
  grad.addColorStop(0.4, 'rgba(255,170,60,0.3)');
  grad.addColorStop(1, 'rgba(255,150,40,0)');
  gctx.fillStyle = grad;
  gctx.fillRect(0, 0, 128, 128);
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(glowCanvas), transparent: true, depthWrite: false }));
  glow.scale.set(16, 16, 1);
  sunBall.add(glow);
  const sunLabel = makeLabelSprite('Sunlight comes from here', { scale: 2, fontSize: 36 });
  sunLabel.position.set(0, 5.5, 0);
  sunBall.add(sunLabel);

  const earth = new THREE.Mesh(
    new THREE.SphereGeometry(1.6, seg, seg),
    new THREE.MeshStandardMaterial({ color: 0x4d7fff, roughness: 0.8 })
  );
  scene.add(earth);
  const earthLabel = makeLabelSprite('Earth (you are here)', { scale: 1.7, fontSize: 36 });
  earthLabel.position.y = 3;
  scene.add(earthLabel);

  const moon = new THREE.Mesh(
    new THREE.SphereGeometry(0.55, seg, seg),
    new THREE.MeshStandardMaterial({ color: 0xc9c9c9, roughness: 1 })
  );
  scene.add(moon);

  const orbitPts = [];
  const n = 128;
  for (let i = 0; i <= n; i++) {
    const a = (i / n) * Math.PI * 2;
    orbitPts.push(Math.cos(a) * MOON_DIST, 0, Math.sin(a) * MOON_DIST);
  }
  const orbitGeo = new THREE.BufferGeometry();
  orbitGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(orbitPts), 3));
  const orbitLine = new THREE.Line(orbitGeo, new THREE.LineBasicMaterial({ color: 0x4a5f80, transparent: true, opacity: 0.6 }));
  scene.add(orbitLine);

  const inset = document.createElement('div');
  inset.className = 'ix-moon-inset';
  const insetTitle = document.createElement('span');
  insetTitle.className = 'ix-moon-inset-title';
  insetTitle.textContent = 'Moon seen from Earth';
  const insetCanvas = document.createElement('canvas');
  const insetSize = 140;
  const insetDpr = Math.min(window.devicePixelRatio || 1, 2);
  insetCanvas.width = insetSize * insetDpr;
  insetCanvas.height = insetSize * insetDpr;
  insetCanvas.style.width = `${insetSize}px`;
  insetCanvas.style.height = `${insetSize}px`;
  inset.appendChild(insetTitle);
  inset.appendChild(insetCanvas);
  stage.appendChild(inset);
  const ictx = insetCanvas.getContext('2d');
  ictx.setTransform(insetDpr, 0, 0, insetDpr, 0, 0);

  function drawInset(angle) {
    const R = 52;
    const cx = 70;
    const cy = 70;
    ictx.clearRect(0, 0, 140, 140);
    ictx.fillStyle = '#0a1220';
    ictx.beginPath();
    ictx.arc(cx, cy, R + 8, 0, Math.PI * 2);
    ictx.fill();
    ictx.fillStyle = '#1c2738';
    ictx.beginPath();
    ictx.arc(cx, cy, R, 0, Math.PI * 2);
    ictx.fill();
    const a = ((angle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    const waxing = a < Math.PI;
    const cosA = Math.cos(a);
    ictx.save();
    ictx.beginPath();
    ictx.arc(cx, cy, R, 0, Math.PI * 2);
    ictx.clip();
    ictx.fillStyle = '#f2ead5';
    ictx.beginPath();
    ictx.arc(cx, cy, R, -Math.PI / 2, Math.PI / 2, !waxing);
    ictx.fill();
    ictx.beginPath();
    ictx.ellipse(cx, cy, Math.abs(cosA) * R, R, 0, 0, Math.PI * 2);
    if ((waxing && cosA > 0) || (!waxing && cosA < 0)) {
      ictx.fillStyle = '#1c2738';
    } else {
      ictx.fillStyle = '#f2ead5';
    }
    ictx.fill();
    ictx.restore();
    ictx.strokeStyle = 'rgba(255,255,255,0.18)';
    ictx.lineWidth = 1.5;
    ictx.beginPath();
    ictx.arc(cx, cy, R, 0, Math.PI * 2);
    ictx.stroke();
  }

  function phaseIndex(angle) {
    const a = ((angle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    return Math.round(a / (Math.PI / 4)) % 8;
  }

  const hud = createHud(stage);
  const phaseBadge = hud.badge('New Moon (aunsi)', '#fff7d6');
  const litBadge = hud.badge('0% lit', '#9ec1ff');

  let moonAngle = 0;
  let animate = false;
  let animSpeed = 0.35;

  const panel = createPanel(stage, { title: 'Moon Phase Controls' });
  const angleSlider = panel.slider({
    label: 'Moon position',
    min: 0, max: 360, step: 1, value: 0,
    format: (v) => `${Math.round(v)}\u00b0`,
    onChange: (v) => { moonAngle = THREE.MathUtils.degToRad(v); animate = false; animToggle.set(false); },
  });
  const animToggle = panel.toggle({ label: 'Animate orbit', value: false, onChange: (v) => { animate = v; } });
  panel.slider({
    label: 'Animation speed',
    min: 5, max: 100, step: 5, value: 35,
    format: (v) => `${v}%`,
    onChange: (v) => { animSpeed = v / 100; },
  });
  panel.info('Drag the Moon around its orbit with the slider. The small window shows exactly what the Moon looks like from Nepal that night. Phase 0\u00b0 = New Moon (Moon between Earth and Sun).');

  engine.setUpdate((dt) => {
    if (animate) {
      moonAngle = (moonAngle + dt * animSpeed) % (Math.PI * 2);
      angleSlider.set(Math.round(THREE.MathUtils.radToDeg(moonAngle)));
    }
    moon.position.set(Math.cos(moonAngle) * MOON_DIST, 0, -Math.sin(moonAngle) * MOON_DIST);
    earth.rotation.y += dt * 0.3;
    const idx = phaseIndex(moonAngle);
    const [name, color] = PHASES[idx];
    phaseBadge.set(name);
    phaseBadge.el.style.setProperty('--ix-hud-color', color);
    const lit = Math.round(((1 - Math.cos(moonAngle)) / 2) * 100);
    litBadge.set(`${lit}% lit`);
    drawInset(moonAngle);
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose();
      panel.dispose();
      hud.dispose();
      inset.remove();
      engine.dispose();
    },
  };
}
