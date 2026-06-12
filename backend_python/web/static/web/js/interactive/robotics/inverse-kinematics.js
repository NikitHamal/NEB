import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const L1 = 2.4;
const L2 = 1.8;

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0.6, 2.6, 9);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4, maxDistance: 18, target: new THREE.Vector3(0, 2, 0),
  });

  basicLights(scene);
  scene.add(new THREE.GridHelper(12, 12, 0x35507c, 0x22344f));

  const planeMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(12, 9),
    new THREE.MeshBasicMaterial({ color: 0x1a2c4a, transparent: true, opacity: 0.18, side: THREE.DoubleSide })
  );
  planeMesh.position.y = 2;
  scene.add(planeMesh);

  const reachRing = new THREE.Mesh(
    new THREE.RingGeometry(L1 + L2 - 0.04, L1 + L2 + 0.04, Math.max(48, seg * 2)),
    new THREE.MeshBasicMaterial({ color: 0x35d07f, transparent: true, opacity: 0.35, side: THREE.DoubleSide })
  );
  reachRing.position.y = 0;
  scene.add(reachRing);
  const innerRing = new THREE.Mesh(
    new THREE.RingGeometry(Math.abs(L1 - L2) - 0.04, Math.abs(L1 - L2) + 0.04, Math.max(32, seg)),
    new THREE.MeshBasicMaterial({ color: 0xe2484d, transparent: true, opacity: 0.3, side: THREE.DoubleSide })
  );
  scene.add(innerRing);

  const metalMat = new THREE.MeshStandardMaterial({ color: 0x4d9fe0, roughness: 0.4, metalness: 0.4 });
  const jointMat = new THREE.MeshStandardMaterial({ color: 0xf5b942, roughness: 0.45, metalness: 0.3 });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x22344f, roughness: 0.6 });

  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.65, 0.4, seg), darkMat);
  base.position.y = -0.2;
  scene.add(base);

  const shoulder = new THREE.Group();
  scene.add(shoulder);
  shoulder.add(new THREE.Mesh(new THREE.SphereGeometry(0.3, Math.max(16, seg / 2), Math.max(16, seg / 2)), jointMat));
  const link1 = new THREE.Mesh(new THREE.BoxGeometry(L1, 0.26, 0.26), metalMat);
  link1.position.x = L1 / 2;
  shoulder.add(link1);

  const elbow = new THREE.Group();
  elbow.position.x = L1;
  shoulder.add(elbow);
  elbow.add(new THREE.Mesh(new THREE.SphereGeometry(0.24, Math.max(16, seg / 2), Math.max(16, seg / 2)), jointMat));
  const link2 = new THREE.Mesh(new THREE.BoxGeometry(L2, 0.2, 0.2), metalMat);
  link2.position.x = L2 / 2;
  elbow.add(link2);

  const hand = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), new THREE.MeshStandardMaterial({ color: 0x7fe9ff, emissive: 0x1c5a6a, emissiveIntensity: 0.8 }));
  hand.position.x = L2;
  elbow.add(hand);

  const targetMat = new THREE.MeshStandardMaterial({ color: 0x35d07f, emissive: 0x0d5c34, emissiveIntensity: 0.7 });
  const target = new THREE.Mesh(new THREE.SphereGeometry(0.24, Math.max(16, seg / 2), Math.max(16, seg / 2)), targetMat);
  target.position.set(2.6, 2.4, 0);
  scene.add(target);
  const targetRing = new THREE.Mesh(
    new THREE.TorusGeometry(0.4, 0.03, 8, 32),
    new THREE.MeshBasicMaterial({ color: 0x35d07f, transparent: true, opacity: 0.7 })
  );
  target.add(targetRing);
  const tLabel = makeLabelSprite('Drag me!', { scale: 0.6, fontSize: 40 });
  tLabel.position.y = 0.65;
  target.add(tLabel);

  const hud = createHud(stage);
  const reachBadge = hud.badge('Target reachable', '#35d07f');

  const panel = createPanel(stage, { title: 'IK Solver' });
  let elbowUp = true;
  const t1Read = panel.readout({ label: 'Shoulder θ1', value: '0°' });
  const t2Read = panel.readout({ label: 'Elbow θ2', value: '0°' });
  const dRead = panel.readout({ label: 'Target distance', value: '0.0' });
  panel.toggle({
    label: 'Elbow-up solution', value: true,
    onChange: (v) => { elbowUp = v; },
  });
  panel.info('Drag the green target anywhere on the plane. The arm computes its own joint angles with the law of cosines — instantly. Outside the green circle? No solution exists.');

  const raycaster = new THREE.Raycaster();
  const pointerNdc = new THREE.Vector2();
  const dragPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
  const hitPoint = new THREE.Vector3();
  let dragging = false;

  function updateNdc(e) {
    const rect = engine.canvas.getBoundingClientRect();
    pointerNdc.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointerNdc.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
  }

  function onDown(e) {
    updateNdc(e);
    raycaster.setFromCamera(pointerNdc, camera);
    const hit = raycaster.intersectObject(target, false);
    let near = hit.length > 0;
    if (!near && raycaster.ray.intersectPlane(dragPlane, hitPoint)) {
      near = hitPoint.distanceTo(target.position) < 0.9;
    }
    if (near) {
      dragging = true;
      controls.enabled = false;
      engine.canvas.setPointerCapture && engine.canvas.setPointerCapture(e.pointerId);
      moveTarget();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    updateNdc(e);
    raycaster.setFromCamera(pointerNdc, camera);
    moveTarget();
  }

  function moveTarget() {
    if (raycaster.ray.intersectPlane(dragPlane, hitPoint)) {
      target.position.x = Math.max(-5.5, Math.min(5.5, hitPoint.x));
      target.position.y = Math.max(-1.5, Math.min(5.2, hitPoint.y));
      target.position.z = 0;
    }
  }

  function onUp() {
    if (dragging) {
      dragging = false;
      controls.enabled = true;
    }
  }

  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointermove', onMove);
  engine.canvas.addEventListener('pointerup', onUp);
  engine.canvas.addEventListener('pointercancel', onUp);

  let curT1 = 0.6;
  let curT2 = 0.8;

  engine.setUpdate((dt) => {
    const tx = target.position.x;
    const ty = target.position.y;
    const d = Math.hypot(tx, ty);
    dRead.set(d.toFixed(2) + ' m');

    const reachable = d <= L1 + L2 - 0.001 && d >= Math.abs(L1 - L2) + 0.001;
    let goalT1, goalT2;
    if (reachable) {
      let c2 = (d * d - L1 * L1 - L2 * L2) / (2 * L1 * L2);
      c2 = Math.max(-1, Math.min(1, c2));
      const t2 = Math.acos(c2) * (elbowUp ? -1 : 1);
      const t1 = Math.atan2(ty, tx) - Math.atan2(L2 * Math.sin(t2), L1 + L2 * Math.cos(t2));
      goalT1 = t1;
      goalT2 = t2;
      targetMat.color.set(0x35d07f);
      targetMat.emissive.set(0x0d5c34);
      targetRing.material.color.set(0x35d07f);
      reachBadge.set('Target reachable · two solutions');
      reachBadge.el.style.setProperty('--ix-hud-color', '#35d07f');
    } else {
      goalT1 = Math.atan2(ty, tx);
      goalT2 = d < Math.abs(L1 - L2) ? (elbowUp ? -2.6 : 2.6) : 0;
      targetMat.color.set(0xe2484d);
      targetMat.emissive.set(0x5c0d16);
      targetRing.material.color.set(0xe2484d);
      reachBadge.set(d > L1 + L2 ? 'Unreachable — outside workspace!' : 'Unreachable — inside dead zone!');
      reachBadge.el.style.setProperty('--ix-hud-color', '#e2484d');
    }

    const k = Math.min(dt * 9, 1);
    curT1 += (goalT1 - curT1) * k;
    curT2 += (goalT2 - curT2) * k;
    shoulder.rotation.z = curT1;
    elbow.rotation.z = curT2;

    t1Read.set(((curT1 * 180) / Math.PI).toFixed(1) + '°');
    t2Read.set(((curT2 * 180) / Math.PI).toFixed(1) + '°');

    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown);
      engine.canvas.removeEventListener('pointermove', onMove);
      engine.canvas.removeEventListener('pointerup', onUp);
      engine.canvas.removeEventListener('pointercancel', onUp);
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
