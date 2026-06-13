import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const L1 = 2.2;
const L2 = 1.8;

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(5.5, 4.5, 6.5);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 16, target: new THREE.Vector3(0, 1.8, 0),
  });

  basicLights(scene);
  scene.add(new THREE.GridHelper(12, 12, 0x35507c, 0x22344f));
  const floor = new THREE.Mesh(
    new THREE.CircleGeometry(6, seg),
    new THREE.MeshStandardMaterial({ color: 0x152741, roughness: 0.95 })
  );
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.01;
  scene.add(floor);

  const metalMat = new THREE.MeshStandardMaterial({ color: 0x2da4ec, roughness: 0.4, metalness: 0.4 });
  const jointMat = new THREE.MeshStandardMaterial({ color: 0xf5b942, roughness: 0.45, metalness: 0.3 });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x22344f, roughness: 0.6, metalness: 0.3 });

  const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.1, 0.4, seg), darkMat);
  stand.position.y = 0.2;
  scene.add(stand);

  const basePivot = new THREE.Group();
  basePivot.position.y = 0.4;
  scene.add(basePivot);
  const baseDisk = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.7, 0.35, seg), metalMat);
  baseDisk.position.y = 0.17;
  basePivot.add(baseDisk);

  const shoulderPivot = new THREE.Group();
  shoulderPivot.position.y = 0.45;
  basePivot.add(shoulderPivot);
  const shoulderJoint = new THREE.Mesh(new THREE.SphereGeometry(0.34, Math.max(16, seg / 2), Math.max(16, seg / 2)), jointMat);
  shoulderPivot.add(shoulderJoint);
  const upperArm = new THREE.Mesh(new THREE.BoxGeometry(0.3, L1, 0.3), metalMat);
  upperArm.position.y = L1 / 2;
  shoulderPivot.add(upperArm);

  const elbowPivot = new THREE.Group();
  elbowPivot.position.y = L1;
  shoulderPivot.add(elbowPivot);
  const elbowJoint = new THREE.Mesh(new THREE.SphereGeometry(0.27, Math.max(16, seg / 2), Math.max(16, seg / 2)), jointMat);
  elbowPivot.add(elbowJoint);
  const foreArm = new THREE.Mesh(new THREE.BoxGeometry(0.24, L2, 0.24), metalMat);
  foreArm.position.y = L2 / 2;
  elbowPivot.add(foreArm);

  const wrist = new THREE.Group();
  wrist.position.y = L2;
  elbowPivot.add(wrist);
  const palm = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.16, 0.3), darkMat);
  palm.position.y = 0.08;
  wrist.add(palm);
  const fingerGeo = new THREE.BoxGeometry(0.07, 0.42, 0.22);
  const fingerL = new THREE.Mesh(fingerGeo, jointMat);
  fingerL.position.set(-0.16, 0.34, 0);
  wrist.add(fingerL);
  const fingerR = fingerL.clone();
  fingerR.position.x = 0.16;
  wrist.add(fingerR);

  const tipMarker = new THREE.Object3D();
  tipMarker.position.y = 0.45;
  wrist.add(tipMarker);

  const lbls = [
    { text: 'Base', target: baseDisk, y: -0.5 },
    { text: 'Shoulder', target: shoulderJoint, y: 0.0, x: 0.9 },
    { text: 'Elbow', target: elbowJoint, y: 0.0, x: 0.8 },
  ];
  lbls.forEach((d) => {
    const s = makeLabelSprite(d.text, { scale: 0.5, fontSize: 40 });
    s.position.set(d.x || 0, d.y, 0);
    d.target.add(s);
  });

  const ballMat = new THREE.MeshStandardMaterial({ color: 0xff5d73, roughness: 0.4 });
  const ball = new THREE.Mesh(new THREE.SphereGeometry(0.28, Math.max(16, seg / 2), Math.max(16, seg / 2)), ballMat);
  const ballHome = new THREE.Vector3(2.6, 0.28, 1.2);
  ball.position.copy(ballHome);
  scene.add(ball);

  const hud = createHud(stage);
  const grabBadge = hud.badge('Gripper open · ball free', '#94a3b8');

  const panel = createPanel(stage, { title: 'Arm Controls' });
  let baseAngle = 25;
  let shoulderAngle = 40;
  let elbowAngle = 70;
  let gripClosed = false;
  let holding = false;

  panel.slider({
    label: 'Base rotation', min: -180, max: 180, step: 1, value: baseAngle,
    format: (v) => v + '°',
    onChange: (v) => { baseAngle = v; },
  });
  panel.slider({
    label: 'Shoulder', min: 5, max: 100, step: 1, value: shoulderAngle,
    format: (v) => v + '°',
    onChange: (v) => { shoulderAngle = v; },
  });
  panel.slider({
    label: 'Elbow', min: 0, max: 135, step: 1, value: elbowAngle,
    format: (v) => v + '°',
    onChange: (v) => { elbowAngle = v; },
  });
  const gripBtn = panel.button({
    label: 'Close gripper', icon: 'pan_tool',
    onClick: () => {
      gripClosed = !gripClosed;
      gripBtn.setLabel(gripClosed ? 'Open gripper' : 'Close gripper');
      if (!gripClosed && holding) {
        holding = false;
        const p = tip.clone();
        ball.position.set(p.x, Math.max(0.28, p.y - 0.2), p.z);
        dropVel = 0;
        dropping = true;
      }
    },
  });
  panel.button({
    label: 'Reset ball', icon: 'restart_alt', variant: 'ghost',
    onClick: () => {
      holding = false;
      dropping = false;
      ball.position.copy(ballHome);
    },
  });
  const distRead = panel.readout({ label: 'Tip → ball', value: '—' });
  panel.info('Move the three joints so the open gripper reaches the ball, then close it to grab. Three joints = three degrees of freedom.');

  const tip = new THREE.Vector3();
  let dropping = false;
  let dropVel = 0;

  engine.setUpdate((dt, t) => {
    basePivot.rotation.y += ((baseAngle * Math.PI) / 180 - basePivot.rotation.y) * Math.min(dt * 8, 1);
    shoulderPivot.rotation.x += ((shoulderAngle * Math.PI) / 180 - shoulderPivot.rotation.x) * Math.min(dt * 8, 1);
    elbowPivot.rotation.x += ((elbowAngle * Math.PI) / 180 - elbowPivot.rotation.x) * Math.min(dt * 8, 1);

    const fingerGap = gripClosed ? 0.085 : 0.16;
    fingerL.position.x += (-fingerGap - fingerL.position.x) * Math.min(dt * 10, 1);
    fingerR.position.x += (fingerGap - fingerR.position.x) * Math.min(dt * 10, 1);

    tipMarker.getWorldPosition(tip);
    const dist = tip.distanceTo(ball.position);
    distRead.set(holding ? 'holding!' : dist.toFixed(2) + ' m');

    if (!holding && gripClosed && dist < 0.42 && !dropping) {
      holding = true;
    }
    if (holding) {
      ball.position.lerp(tip, Math.min(dt * 14, 1));
      grabBadge.set('Ball grabbed! Move it and open the gripper to drop.');
      grabBadge.el.style.setProperty('--ix-hud-color', '#35d07f');
    } else {
      grabBadge.set(gripClosed ? 'Gripper closed · nothing inside' : dist < 0.42 ? 'In range — close the gripper!' : 'Gripper open · ball free');
      grabBadge.el.style.setProperty('--ix-hud-color', dist < 0.42 && !gripClosed ? '#f5b942' : '#94a3b8');
    }
    if (dropping) {
      dropVel += 9.8 * dt;
      ball.position.y -= dropVel * dt;
      if (ball.position.y <= 0.28) {
        ball.position.y = 0.28;
        dropping = false;
      }
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
