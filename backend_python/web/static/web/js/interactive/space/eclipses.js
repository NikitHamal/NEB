import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const EARTH_DIST = 34;
const MOON_DIST = 5.5;

export default function init(stage) {
  const engine = createEngine(stage, { far: 3000 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(10, 18, 40);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4,
    maxDistance: 140,
    target: new THREE.Vector3(EARTH_DIST * 0.6, 0, 0),
  });

  const starGeo = new THREE.BufferGeometry();
  const starCount = quality.tier === 'low' ? 500 : 1500;
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    const r = 350 + Math.random() * 600;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPos[i * 3 + 1] = r * Math.cos(phi);
    starPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xbfd0e8, size: 1.3, sizeAttenuation: false })));

  scene.add(new THREE.AmbientLight(0xffffff, 0.16));
  const sunLight = new THREE.PointLight(0xfff2d8, 2200, 0, 2);
  scene.add(sunLight);

  const sun = new THREE.Mesh(new THREE.SphereGeometry(3.6, seg, seg), new THREE.MeshBasicMaterial({ color: 0xffc24d }));
  scene.add(sun);
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
  glow.scale.set(18, 18, 1);
  sun.add(glow);
  const sunLabel = makeLabelSprite('Sun', { scale: 1.8, fontSize: 38 });
  sunLabel.position.y = 6;
  sun.add(sunLabel);

  const earth = new THREE.Mesh(
    new THREE.SphereGeometry(1.5, seg, seg),
    new THREE.MeshStandardMaterial({ color: 0x4d7fff, roughness: 0.8 })
  );
  earth.position.set(EARTH_DIST, 0, 0);
  scene.add(earth);
  const earthLabel = makeLabelSprite('Earth', { scale: 1.6, fontSize: 36 });
  earthLabel.position.y = 3;
  earth.add(earthLabel);

  const moon = new THREE.Mesh(
    new THREE.SphereGeometry(0.55, seg, seg),
    new THREE.MeshStandardMaterial({ color: 0xc9c9c9, roughness: 1 })
  );
  scene.add(moon);
  const moonLabel = makeLabelSprite('Moon', { scale: 1.2, fontSize: 34 });
  moonLabel.position.y = 1.6;
  moon.add(moonLabel);

  const coneMat = new THREE.MeshBasicMaterial({ color: 0x10131c, transparent: true, opacity: 0.42, side: THREE.DoubleSide, depthWrite: false });
  const earthConeLen = 26;
  const earthCone = new THREE.Mesh(new THREE.ConeGeometry(1.45, earthConeLen, 24, 1, true), coneMat);
  scene.add(earthCone);
  const moonConeLen = 11;
  const moonCone = new THREE.Mesh(new THREE.ConeGeometry(0.52, moonConeLen, 20, 1, true), coneMat);
  scene.add(moonCone);

  const sunPos = new THREE.Vector3(0, 0, 0);
  const tmp = new THREE.Vector3();
  const axisY = new THREE.Vector3(0, 1, 0);
  const quat = new THREE.Quaternion();

  function placeShadowCone(cone, body, len) {
    tmp.copy(body.position).sub(sunPos).normalize();
    cone.position.copy(body.position).addScaledVector(tmp, len / 2);
    quat.setFromUnitVectors(axisY, tmp);
    cone.quaternion.copy(quat);
  }

  let tiltDeg = 5;
  let moonAngle = Math.PI;
  let animate = true;
  let animSpeed = 0.3;

  function moonPosition() {
    const tilt = THREE.MathUtils.degToRad(tiltDeg);
    const x = -Math.cos(moonAngle) * MOON_DIST;
    const z = -Math.sin(moonAngle) * MOON_DIST;
    const y = Math.cos(moonAngle) * Math.sin(tilt) * MOON_DIST;
    moon.position.set(earth.position.x + x, y, earth.position.z + z);
  }

  const orbitGeo = new THREE.BufferGeometry();
  const orbitArr = new Float32Array(129 * 3);
  orbitGeo.setAttribute('position', new THREE.BufferAttribute(orbitArr, 3));
  const orbitLine = new THREE.Line(orbitGeo, new THREE.LineBasicMaterial({ color: 0x4a5f80, transparent: true, opacity: 0.6 }));
  scene.add(orbitLine);

  function rebuildOrbit() {
    const tilt = THREE.MathUtils.degToRad(tiltDeg);
    for (let i = 0; i <= 128; i++) {
      const a = (i / 128) * Math.PI * 2;
      orbitArr[i * 3] = earth.position.x - Math.cos(a) * MOON_DIST;
      orbitArr[i * 3 + 1] = Math.cos(a) * Math.sin(tilt) * MOON_DIST;
      orbitArr[i * 3 + 2] = earth.position.z - Math.sin(a) * MOON_DIST;
    }
    orbitGeo.attributes.position.needsUpdate = true;
  }
  rebuildOrbit();

  const hud = createHud(stage);
  const stateBadge = hud.badge('No eclipse', '#9ec1ff');
  const tiltBadge = hud.badge('Orbit tilt: 5\u00b0', '#8be9a8');

  const panel = createPanel(stage, { title: 'Eclipse Controls' });
  panel.buttonRow([
    {
      label: 'Solar eclipse',
      icon: 'wb_twilight',
      onClick: () => { tiltDeg = 0; tiltSlider.set(0); moonAngle = 0; angleSlider.set(0); animate = false; animToggle.set(false); rebuildOrbit(); },
    },
    {
      label: 'Lunar eclipse',
      icon: 'nightlight',
      onClick: () => { tiltDeg = 0; tiltSlider.set(0); moonAngle = Math.PI; angleSlider.set(180); animate = false; animToggle.set(false); rebuildOrbit(); },
    },
  ]);
  const angleSlider = panel.slider({
    label: 'Moon position',
    min: 0, max: 360, step: 1, value: 180,
    format: (v) => `${Math.round(v)}\u00b0`,
    onChange: (v) => { moonAngle = THREE.MathUtils.degToRad(v); animate = false; animToggle.set(false); },
  });
  const tiltSlider = panel.slider({
    label: 'Moon orbit tilt',
    min: 0, max: 10, step: 0.5, value: 5,
    format: (v) => `${v}\u00b0`,
    onChange: (v) => { tiltDeg = v; tiltBadge.set(`Orbit tilt: ${v}\u00b0`); rebuildOrbit(); },
  });
  const animToggle = panel.toggle({ label: 'Animate Moon', value: true, onChange: (v) => { animate = v; } });
  panel.info('The real Moon orbit is tilted about 5\u00b0, so the shadows usually miss. Set the tilt to 0\u00b0 and line up the Moon to make your own eclipse. Never look at the real Sun directly! Sizes and distances are not to scale.');

  function eclipseState() {
    const a = ((moonAngle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    const nearNew = a < 0.16 || a > Math.PI * 2 - 0.16;
    const nearFull = Math.abs(a - Math.PI) < 0.16;
    const yOff = Math.abs(moon.position.y);
    if (nearNew && yOff < 0.45) return ['SOLAR ECLIPSE \u2014 Moon\u2019s shadow touches Earth!', '#ffb340'];
    if (nearFull && yOff < 0.45) return ['LUNAR ECLIPSE \u2014 Moon inside Earth\u2019s shadow!', '#ff6b81'];
    if ((nearNew || nearFull) && yOff >= 0.45) return ['So close\u2026 the tilt makes the shadow miss', '#c8d2e0'];
    return ['No eclipse \u2014 shadows miss', '#9ec1ff'];
  }

  engine.setUpdate((dt) => {
    if (animate) {
      moonAngle = (moonAngle + dt * animSpeed) % (Math.PI * 2);
      angleSlider.set(Math.round(THREE.MathUtils.radToDeg(moonAngle)));
    }
    moonPosition();
    placeShadowCone(earthCone, earth, earthConeLen);
    placeShadowCone(moonCone, moon, moonConeLen);
    earth.rotation.y += dt * 0.25;
    const [txt, color] = eclipseState();
    stateBadge.set(txt);
    stateBadge.el.style.setProperty('--ix-hud-color', color);
    const a = ((moonAngle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    const isLunar = Math.abs(a - Math.PI) < 0.16 && Math.abs(moon.position.y) < 0.45;
    moon.material.color.setHex(isLunar ? 0xb5523c : 0xc9c9c9);
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
