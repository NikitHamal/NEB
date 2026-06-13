import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const G = 9.81;
const RAMP_LEN = 6;

export default function init(stage, opts) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(-2, 4, 8);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 2, maxDistance: 25,
    target: new THREE.Vector3(3, 1, 0),
  });
  controls.setTarget(new THREE.Vector3(3, 1, 0));

  basicLights(scene, { ambient: 0.5, key: 1.5 });
  scene.background = new THREE.Color(0x0b1c30);

  // Ground
  const groundGeo = new THREE.PlaneGeometry(20, 10);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.9 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.set(5, 0, 0);
  if (quality.shadows) ground.receiveShadow = true;
  scene.add(ground);
  scene.add(new THREE.GridHelper(20, 20, 0x1a3a20, 0x1a3a20));

  // Ramp group — rebuilt when angle changes
  const rampGroup = new THREE.Group();
  scene.add(rampGroup);

  let rampMesh = null;
  let rampSurface = null;

  function buildRamp(angleDeg) {
    rampGroup.clear();
    const rad = (angleDeg * Math.PI) / 180;
    const rampW = 1.2;
    const rampH = Math.sin(rad) * RAMP_LEN;
    const rampBase = Math.cos(rad) * RAMP_LEN;

    // Ramp inclined surface
    const shape = new THREE.Shape();
    shape.moveTo(0, 0);
    shape.lineTo(rampBase, rampH);
    shape.lineTo(rampBase, 0);
    shape.closePath();
    const extrudeSettings = { depth: rampW, bevelEnabled: false };
    const rampGeo = new THREE.ExtrudeGeometry(shape, extrudeSettings);
    const rampMat = new THREE.MeshStandardMaterial({ color: 0x7c3aed, roughness: 0.7, metalness: 0.1 });
    rampMesh = new THREE.Mesh(rampGeo, rampMat);
    rampMesh.position.set(0, 0, -rampW / 2);
    if (quality.shadows) { rampMesh.castShadow = true; rampMesh.receiveShadow = true; }
    rampGroup.add(rampMesh);

    // Ramp surface line (for ball to slide on)
    const topLinePts = [
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(rampBase, rampH, 0),
    ];
    const topLineGeo = new THREE.BufferGeometry().setFromPoints(topLinePts);
    const topLine = new THREE.Line(topLineGeo, new THREE.LineBasicMaterial({ color: 0xc4b5fd, linewidth: 3 }));
    rampGroup.add(topLine);

    // Finish line posts
    const postMat = new THREE.MeshStandardMaterial({ color: 0x22c55e });
    for (let z = -rampW / 2; z <= rampW / 2; z += rampW) {
      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.0, 8), postMat);
      post.position.set(rampBase + 0.1, 0.5, z);
      rampGroup.add(post);
    }
    const flagGeo = new THREE.PlaneGeometry(0.35, 0.22);
    const flagMat = new THREE.MeshBasicMaterial({ color: 0xffd584, side: THREE.DoubleSide });
    const flag = new THREE.Mesh(flagGeo, flagMat);
    flag.position.set(rampBase + 0.27, 1.1, 0);
    rampGroup.add(flag);

    const finishLabel = makeLabelSprite('FINISH', { scale: 0.9, fontSize: 32 });
    finishLabel.position.set(rampBase + 0.1, 1.5, 0);
    rampGroup.add(finishLabel);

    // Angle arc indicator
    const arcPts = [];
    const arcR = 0.8;
    const arcSegs = 30;
    for (let i = 0; i <= arcSegs; i++) {
      const a = (i / arcSegs) * rad;
      arcPts.push(new THREE.Vector3(Math.cos(a) * arcR, Math.sin(a) * arcR, 0));
    }
    const arcGeo = new THREE.BufferGeometry().setFromPoints(arcPts);
    rampGroup.add(new THREE.Line(arcGeo, new THREE.LineBasicMaterial({ color: 0xF59E0B, transparent: true, opacity: 0.7 })));

    const angleLabel = makeLabelSprite(`${angleDeg}°`, { scale: 0.7, fontSize: 30 });
    angleLabel.position.set(Math.cos(rad / 2) * arcR * 1.3, Math.sin(rad / 2) * arcR * 1.3, 0);
    rampGroup.add(angleLabel);

    // Force arrows (ArrowHelper)
    const gravDir = new THREE.Vector3(0, -1, 0);
    gravArrow = new THREE.ArrowHelper(gravDir, new THREE.Vector3(rampBase * 0.5, rampH * 0.5 + 0.5, 0), 0.8, 0x38bdf8, 0.2, 0.15);
    rampGroup.add(gravArrow);
    const gravLabel = makeLabelSprite('g', { scale: 0.6, fontSize: 28 });
    gravLabel.position.set(rampBase * 0.5 - 0.3, rampH * 0.5, 0);
    rampGroup.add(gravLabel);
  }

  let gravArrow = null;

  // Ball
  const ballGeo = new THREE.SphereGeometry(0.18, seg, seg);
  const ballMat = new THREE.MeshStandardMaterial({ color: 0xe11d48, metalness: 0.2, roughness: 0.6, emissive: 0x5a0010, emissiveIntensity: 0.15 });
  const ballMesh = new THREE.Mesh(ballGeo, ballMat);
  if (quality.shadows) { ballMesh.castShadow = true; }
  scene.add(ballMesh);

  // Ball spin marker (line across ball)
  const spinGeo = new THREE.BufferGeometry();
  spinGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
  const spinLine = new THREE.Line(spinGeo, new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.7 }));
  ballMesh.add(spinLine);

  // Velocity arrow on ball
  let velArrow = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 0), 0.01, 0x38bdf8, 0.15, 0.1);
  scene.add(velArrow);

  // State
  let angle = 25;
  let mu = 0.1;
  let s = 0;
  let vel = 0;
  let t = 0;
  let running = false;
  let finished = false;
  let bestTime = 0;
  let spin = 0;

  function accel() {
    const rad = (angle * Math.PI) / 180;
    return Math.max(0, G * (Math.sin(rad) - mu * Math.cos(rad)));
  }

  function reset() {
    s = 0; vel = 0; t = 0; spin = 0;
    running = false; finished = false;
    badge.set('Press Go to race!');
    positionBall();
  }

  function positionBall() {
    const rad = (angle * Math.PI) / 180;
    const along = s;
    const bx = Math.cos(rad) * along;
    const by = Math.sin(rad) * along;
    const nx = -Math.sin(rad);
    const ny = Math.cos(rad);
    ballMesh.position.set(bx + nx * 0.18, by + ny * 0.18, 0);
  }

  buildRamp(angle);
  positionBall();

  // Panel
  const panel = createPanel(stage, { title: 'Ramp 3D' });
  panel.slider({
    label: 'Ramp angle', min: 5, max: 45, step: 1, value: angle,
    format: (v) => `${v}°`,
    onChange: (v) => { angle = v; buildRamp(v); reset(); },
  });
  panel.slider({
    label: 'Friction', min: 0, max: 0.8, step: 0.02, value: mu,
    format: (v) => v.toFixed(2),
    onChange: (v) => { mu = v; reset(); },
  });
  panel.buttonRow([
    { label: 'Go!', icon: 'play_arrow', onClick: () => { if (!running && !finished) { running = true; badge.set('Rolling…'); } } },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset },
  ]);
  panel.divider();
  const timeOut = panel.readout({ label: 'Race time', value: '0.00 s' });
  const bestOut = panel.readout({ label: 'Best time', value: '—' });
  const speedOut = panel.readout({ label: 'Speed', value: '0.0 m/s' });
  const accelOut = panel.readout({ label: 'Acceleration', value: '0.0 m/s²' });
  panel.info('3D inclined ramp. Orbit the camera to see depth. The blue arrow shows velocity, the formula is a = g(sinθ − μcosθ).');

  const hud = createHud(stage);
  const badge = hud.badge('Press Go to race!', '#F59E0B');

  engine.setUpdate((dt) => {
    controls.update(dt);

    const ddt = Math.min(dt, 0.05);
    if (running) {
      const a = accel();
      if (a <= 0 && vel <= 0) {
        running = false;
        badge.set('Too much friction — will not roll!');
      } else {
        vel += a * ddt;
        s += vel * ddt;
        spin += (vel / 0.18) * ddt;
        t += ddt;
        if (s >= RAMP_LEN) {
          s = RAMP_LEN;
          running = false;
          finished = true;
          if (!bestTime || t < bestTime) {
            bestTime = t;
            bestOut.set(`${bestTime.toFixed(2)} s`);
          }
          badge.set(`Finished in ${t.toFixed(2)} s!`);
        }
      }
    }

    positionBall();
    ballMesh.rotation.z = -spin;

    // Velocity arrow
    const rad = (angle * Math.PI) / 180;
    const velDir = new THREE.Vector3(Math.cos(rad), Math.sin(rad), 0).normalize();
    velArrow.position.copy(ballMesh.position);
    const velLen = Math.max(0.01, vel * 0.12);
    velArrow.setDirection(velDir);
    velArrow.setLength(velLen, Math.min(0.18, velLen * 0.4), Math.min(0.12, velLen * 0.25));
    velArrow.visible = vel > 0.05;

    timeOut.set(`${t.toFixed(2)} s`);
    speedOut.set(`${vel.toFixed(1)} m/s`);
    const a = accel();
    accelOut.set(`${a.toFixed(2)} m/s²${a === 0 ? ' (stuck!)' : ''}`);
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
