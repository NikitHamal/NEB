import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const GRAVITY_PRESETS = { moon: 1.62, earth: 9.81, jupiter: 24.8 };

export default function init(stage, opts) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 1, 5);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 1.5, maxDistance: 20,
    target: new THREE.Vector3(0, -1, 0),
  });
  controls.setTarget(new THREE.Vector3(0, -1, 0));

  basicLights(scene, { ambient: 0.5, key: 1.4 });
  scene.background = new THREE.Color(0x0b1c30);

  // Pivot mount
  const pivotGeo = new THREE.CylinderGeometry(0.07, 0.07, 0.4, 16);
  const pivotMat = new THREE.MeshStandardMaterial({ color: 0xc7d4ea, metalness: 0.6, roughness: 0.3 });
  const pivotMesh = new THREE.Mesh(pivotGeo, pivotMat);
  pivotMesh.rotation.z = Math.PI / 2;
  pivotMesh.position.set(0, 0, 0);
  scene.add(pivotMesh);

  const pivotLabel = makeLabelSprite('Pivot', { scale: 0.8, fontSize: 32 });
  pivotLabel.position.set(0.35, 0.15, 0);
  scene.add(pivotLabel);

  // String (line)
  const stringGeo = new THREE.BufferGeometry();
  const stringPositions = new Float32Array(6);
  stringGeo.setAttribute('position', new THREE.BufferAttribute(stringPositions, 3));
  const stringMat = new THREE.LineBasicMaterial({ color: 0xc7d4ea, linewidth: 2 });
  const stringLine = new THREE.Line(stringGeo, stringMat);
  scene.add(stringLine);

  // Bob
  const bobGeo = new THREE.SphereGeometry(0.12, seg, seg);
  const bobMat = new THREE.MeshStandardMaterial({ color: 0xF59E0B, metalness: 0.3, roughness: 0.5, emissive: 0x7a4f00, emissiveIntensity: 0.15 });
  const bob = new THREE.Mesh(bobGeo, bobMat);
  scene.add(bob);

  const bobLabel = makeLabelSprite('Bob', { scale: 0.8, fontSize: 32 });
  scene.add(bobLabel);

  // Protractor arc (shows angle range)
  const arcGroup = new THREE.Group();
  scene.add(arcGroup);
  const arcPoints = [];
  const ARC_SEGS = 60;
  for (let i = 0; i <= ARC_SEGS; i++) {
    const a = -Math.PI / 2 + (i / ARC_SEGS) * Math.PI;
    arcPoints.push(new THREE.Vector3(Math.sin(a), -Math.cos(a), 0));
  }
  const arcGeo = new THREE.BufferGeometry().setFromPoints(arcPoints);
  const arcLine = new THREE.Line(arcGeo, new THREE.LineBasicMaterial({ color: 0x3a4f70, transparent: true, opacity: 0.5 }));
  arcGroup.add(arcLine);

  // Floor / shadow catcher
  if (quality.shadows) {
    const floorGeo = new THREE.PlaneGeometry(8, 8);
    const floorMat = new THREE.ShadowMaterial({ opacity: 0.25 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.receiveShadow = true;
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -3.2;
    scene.add(floor);
  }

  // State
  let L = 1.0;
  let g = 9.81;
  let dampingOn = false;
  let theta = (30 * Math.PI) / 180;
  let omega = 0;
  let elapsed = 0;
  let swings = 0;
  let lastCross = -1;
  let measuredT = 0;
  let prevOmegaSign = 0;

  function resetMotion(angleDeg) {
    theta = (angleDeg * Math.PI) / 180;
    omega = 0;
    elapsed = 0;
    swings = 0;
    lastCross = -1;
    measuredT = 0;
    prevOmegaSign = 0;
  }

  // Panel
  const panel = createPanel(stage, { title: 'Pendulum 3D' });
  const lenSlider = panel.slider({
    label: 'Length L', min: 0.2, max: 3, step: 0.05, value: L,
    format: (v) => `${v.toFixed(2)} m`,
    onChange: (v) => { L = v; arcGroup.scale.setScalar(v); },
  });
  const gravSelect = panel.select({
    label: 'Gravity preset',
    options: [
      { value: 'earth', label: 'Earth (9.81 m/s²)' },
      { value: 'moon', label: 'Moon (1.62 m/s²)' },
      { value: 'jupiter', label: 'Jupiter (24.8 m/s²)' },
      { value: 'custom', label: 'Custom' },
    ],
    value: 'earth',
    onChange: (v) => { if (v !== 'custom') { g = GRAVITY_PRESETS[v]; gravSlider.set(g); } },
  });
  const gravSlider = panel.slider({
    label: 'Gravity g', min: 1, max: 30, step: 0.1, value: g,
    format: (v) => `${v.toFixed(2)} m/s²`,
    onChange: (v) => { g = v; gravSelect.set('custom'); },
  });
  const angleSlider = panel.slider({
    label: 'Initial angle', min: 5, max: 75, step: 1, value: 30,
    format: (v) => `${v}°`,
    onChange: (v) => resetMotion(v),
  });
  panel.toggle({
    label: 'Air damping', value: false,
    onChange: (v) => { dampingOn = v; },
  });
  panel.divider();
  const periodOut = panel.readout({ label: 'Measured period', value: '—' });
  const theoryOut = panel.readout({ label: 'Theory 2π√(L/g)', value: '—' });
  const angleOut = panel.readout({ label: 'Current angle θ', value: '—' });
  panel.button({ label: 'Reset swing', icon: 'replay', onClick: () => resetMotion(angleSlider.get()) });
  panel.info('Watch the 3D pendulum swing. The arc shows the angle range. Orbit the camera with drag.');

  const hud = createHud(stage);
  const phaseBadge = hud.badge('Swinging', '#F59E0B');

  // Initial arc scale
  arcGroup.scale.setScalar(L);

  engine.setUpdate((dt) => {
    controls.update(dt);

    // Physics step (same as 2D: exact ODE with sub-steps)
    const sub = 4;
    const h = dt / sub;
    for (let i = 0; i < sub; i++) {
      const b = dampingOn ? 0.18 : 0;
      const alpha = -(g / L) * Math.sin(theta) - b * omega;
      omega += alpha * h;
      theta += omega * h;
      elapsed += h;
      const sign = omega > 0 ? 1 : omega < 0 ? -1 : 0;
      if (prevOmegaSign <= 0 && sign > 0 && theta < 0.001) {
        if (lastCross >= 0) { measuredT = elapsed - lastCross; swings++; }
        lastCross = elapsed;
      }
      if (sign !== 0) prevOmegaSign = sign;
    }

    // Update 3D geometry
    const bobX = Math.sin(theta) * L;
    const bobY = -Math.cos(theta) * L;
    bob.position.set(bobX, bobY, 0);

    stringPositions[0] = 0; stringPositions[1] = 0; stringPositions[2] = 0;
    stringPositions[3] = bobX; stringPositions[4] = bobY; stringPositions[5] = 0;
    stringGeo.attributes.position.needsUpdate = true;

    bobLabel.position.set(bobX + 0.2, bobY + 0.15, 0);

    // Update readouts
    const theory = 2 * Math.PI * Math.sqrt(L / g);
    theoryOut.set(`${theory.toFixed(2)} s`);
    periodOut.set(measuredT > 0 ? `${measuredT.toFixed(2)} s` : '—');
    angleOut.set(`${((theta * 180) / Math.PI).toFixed(1)}°`);
    phaseBadge.set(dampingOn ? 'Damped swing' : 'Swinging');
  });

  engine.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
