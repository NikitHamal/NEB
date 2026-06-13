import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const ARENA = 11;
const WHEEL_BASE = 1.0;
const MAX_SPEED = 2.6;
const TRAIL_MAX = 400;

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 12, 9);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 26, target: new THREE.Vector3(0, 0, 0),
  });

  basicLights(scene);

  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(ARENA * 2, ARENA * 2),
    new THREE.MeshStandardMaterial({ color: 0x152741, roughness: 0.95 })
  );
  floor.rotation.x = -Math.PI / 2;
  scene.add(floor);
  scene.add(new THREE.GridHelper(ARENA * 2, 22, 0x35507c, 0x22344f));

  const wallMat = new THREE.MeshStandardMaterial({ color: 0x2c4368, roughness: 0.8 });
  const wallGeo = new THREE.BoxGeometry(ARENA * 2, 0.6, 0.25);
  [[0, -ARENA, 0], [0, ARENA, 0], [-ARENA, 0, Math.PI / 2], [ARENA, 0, Math.PI / 2]].forEach((w) => {
    const m = new THREE.Mesh(wallGeo, wallMat);
    m.position.set(w[0], 0.3, w[1]);
    m.rotation.y = w[2];
    scene.add(m);
  });

  const robot = new THREE.Group();
  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x2da4ec, roughness: 0.45, metalness: 0.3 });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x1c2c44, roughness: 0.6 });
  const body = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.34, 1.3), bodyMat);
  body.position.y = 0.46;
  robot.add(body);
  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.5, Math.max(12, seg / 2)), new THREE.MeshStandardMaterial({ color: 0xf5b942, roughness: 0.5 }));
  nose.rotation.x = -Math.PI / 2;
  nose.position.set(0, 0.46, 0.8);
  robot.add(nose);
  const wheelGeo = new THREE.CylinderGeometry(0.33, 0.33, 0.18, Math.max(16, seg / 2));
  const wheelL = new THREE.Mesh(wheelGeo, darkMat);
  wheelL.rotation.z = Math.PI / 2;
  wheelL.position.set(-0.62, 0.33, -0.1);
  robot.add(wheelL);
  const wheelR = wheelL.clone();
  wheelR.position.x = 0.62;
  robot.add(wheelR);
  const caster = new THREE.Mesh(new THREE.SphereGeometry(0.12, 12, 12), darkMat);
  caster.position.set(0, 0.12, 0.55);
  robot.add(caster);
  scene.add(robot);

  const trailGeo = new THREE.BufferGeometry();
  const trailPos = new Float32Array(TRAIL_MAX * 3);
  trailGeo.setAttribute('position', new THREE.BufferAttribute(trailPos, 3));
  trailGeo.setDrawRange(0, 0);
  const trail = new THREE.Line(trailGeo, new THREE.LineBasicMaterial({ color: 0x7fe9ff, transparent: true, opacity: 0.85 }));
  scene.add(trail);
  let trailLen = 0;
  let trailTimer = 0;

  const state = { x: 0, z: 0, heading: 0 };
  let powerL = 0;
  let powerR = 0;

  const hud = createHud(stage);
  const motionBadge = hud.badge('Stopped', '#94a3b8');

  const panel = createPanel(stage, { title: 'Motor Controls' });
  const sliderL = panel.slider({
    label: 'Left motor', min: -100, max: 100, step: 5, value: 0,
    format: (v) => (v > 0 ? '+' : '') + v + '%',
    onChange: (v) => { powerL = v / 100; },
  });
  const sliderR = panel.slider({
    label: 'Right motor', min: -100, max: 100, step: 5, value: 0,
    format: (v) => (v > 0 ? '+' : '') + v + '%',
    onChange: (v) => { powerR = v / 100; },
  });
  const speedRead = panel.readout({ label: 'Forward speed v', value: '0.00 m/s' });
  const turnRead = panel.readout({ label: 'Turn rate ω', value: '0.00 rad/s' });
  panel.buttonRow([
    { label: 'Straight', icon: 'straight', onClick: () => setPowers(80, 80) },
    { label: 'Spin', icon: 'rotate_right', onClick: () => setPowers(60, -60) },
  ]);
  panel.buttonRow([
    { label: 'Curve', icon: 'turn_right', onClick: () => setPowers(90, 45) },
    { label: 'Stop', icon: 'stop_circle', variant: 'ghost', onClick: () => setPowers(0, 0) },
  ]);
  panel.button({
    label: 'Reset position', icon: 'restart_alt', variant: 'ghost',
    onClick: () => {
      state.x = 0; state.z = 0; state.heading = 0;
      trailLen = 0;
      trailGeo.setDrawRange(0, 0);
    },
  });
  panel.info('v = (vL + vR) / 2 sets speed, ω = (vR − vL) / L sets turning. Equal powers drive straight; opposite powers spin in place.');

  function setPowers(l, r) {
    powerL = l / 100;
    powerR = r / 100;
    sliderL.set(l);
    sliderR.set(r);
  }

  engine.setUpdate((dt) => {
    const vl = powerL * MAX_SPEED;
    const vr = powerR * MAX_SPEED;
    const v = (vl + vr) / 2;
    const w = (vr - vl) / WHEEL_BASE;

    state.heading += w * dt;
    state.x += Math.sin(state.heading) * v * dt;
    state.z += Math.cos(state.heading) * v * dt;
    const lim = ARENA - 0.9;
    state.x = Math.max(-lim, Math.min(lim, state.x));
    state.z = Math.max(-lim, Math.min(lim, state.z));

    robot.position.set(state.x, 0, state.z);
    robot.rotation.y = state.heading;
    wheelL.rotation.x += (vl / 0.33) * dt;
    wheelR.rotation.x += (vr / 0.33) * dt;

    speedRead.set(v.toFixed(2) + ' m/s');
    turnRead.set(w.toFixed(2) + ' rad/s');
    if (Math.abs(v) < 0.02 && Math.abs(w) < 0.02) {
      motionBadge.set('Stopped');
      motionBadge.el.style.setProperty('--ix-hud-color', '#94a3b8');
    } else if (Math.abs(v) < 0.05) {
      motionBadge.set('Spinning in place!');
      motionBadge.el.style.setProperty('--ix-hud-color', '#f5b942');
    } else if (Math.abs(w) < 0.05) {
      motionBadge.set('Driving straight');
      motionBadge.el.style.setProperty('--ix-hud-color', '#35d07f');
    } else {
      motionBadge.set(w > 0 ? 'Curving left' : 'Curving right');
      motionBadge.el.style.setProperty('--ix-hud-color', '#0EA5E9');
    }

    trailTimer += dt;
    if (trailTimer > 0.08 && (Math.abs(v) > 0.02 || Math.abs(w) > 0.02)) {
      trailTimer = 0;
      if (trailLen >= TRAIL_MAX) {
        trailPos.copyWithin(0, 3);
        trailLen = TRAIL_MAX - 1;
      }
      trailPos[trailLen * 3] = state.x;
      trailPos[trailLen * 3 + 1] = 0.06;
      trailPos[trailLen * 3 + 2] = state.z;
      trailLen++;
      trailGeo.setDrawRange(0, trailLen);
      trailGeo.attributes.position.needsUpdate = true;
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
