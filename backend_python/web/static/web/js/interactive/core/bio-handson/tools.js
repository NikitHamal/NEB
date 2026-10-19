// The instruments the student holds, modelled at true size (1 unit = 10 cm) with the tip at the
// local origin and the handle along +Y. The rig holds the active one in the student's hand: the
// tip follows the pointer on a spring, the handle leans toward the camera like a pencil held in
// the right hand, tilts into the motion, and dips when pressed. Scissors snip and forceps pinch.
import { THREE } from '../engine.js';
import { MAT, mesh, Spring, SpringV3, clamp } from './kit.js';
import { washBottle } from './props.js';

function lathe(points, seg = 20) { return new THREE.LatheGeometry(points.map(([r, y]) => new THREE.Vector2(r, y)), seg); }
function extrude(shape, depth) { const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false, curveSegments: 10 }); g.translate(0, 0, -depth / 2); return g; }

function scalpel() {
  const g = new THREE.Group();
  const blade = new THREE.Shape();
  blade.moveTo(0, 0); blade.quadraticCurveTo(0.055, 0.03, 0.06, 0.13); blade.lineTo(0.05, 0.36); blade.lineTo(0.0, 0.36); blade.lineTo(-0.005, 0.12); blade.quadraticCurveTo(-0.004, 0.04, 0, 0);
  g.add(mesh(extrude(blade, 0.004), MAT.blade()));
  const handle = new THREE.Shape();
  handle.moveTo(-0.01, 0.34); handle.lineTo(0.06, 0.34); handle.lineTo(0.075, 0.6); handle.lineTo(0.07, 1.3); handle.quadraticCurveTo(0.03, 1.36, -0.01, 1.3); handle.lineTo(-0.012, 0.6); handle.lineTo(-0.01, 0.34);
  g.add(mesh(extrude(handle, 0.026), MAT.brushed()));
  for (let i = 0; i < 9; i++) g.add(mesh(new THREE.BoxGeometry(0.07, 0.008, 0.03), MAT.steel(), [0.03, 0.66 + i * 0.045, 0]));
  return g;
}
function bladeHalf(side) {
  const s = new THREE.Shape();
  s.moveTo(0, 0); s.quadraticCurveTo(0.012 * side, 0.12, 0.022 * side, 0.3); s.lineTo(0.0, 0.3); s.lineTo(-0.004 * side, 0.1); s.lineTo(0, 0);
  const g = new THREE.Group();
  g.add(mesh(extrude(s, 0.006), MAT.blade(), [0, 0, 0.004 * side]));
  const shank = new THREE.Shape();
  shank.moveTo(0, 0.3); shank.lineTo(0.022 * side, 0.3); shank.lineTo(0.09 * side, 0.82); shank.lineTo(0.07 * side, 0.84); shank.lineTo(0, 0.3);
  g.add(mesh(extrude(shank, 0.012), MAT.steel(), [0, 0, 0.004 * side]));
  const ring = mesh(new THREE.TorusGeometry(0.07, 0.014, 8, 24), MAT.steel(), [0.11 * side, 0.9, 0.004 * side]);
  g.add(ring);
  return g;
}
function scissors() {
  const g = new THREE.Group();
  const a = new THREE.Group(); const b = new THREE.Group();
  const ha = bladeHalf(1); const hb = bladeHalf(-1);
  ha.position.y = -0.3; hb.position.y = -0.3; a.add(ha); b.add(hb);
  a.position.y = 0.3; b.position.y = 0.3;
  g.add(a, b);
  g.add(mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.03, 12), MAT.steel(), [0, 0.3, 0]).rotateX(Math.PI / 2));
  g.userData.set = (v) => { const ang = 0.03 + v * 0.32; a.rotation.z = -ang; b.rotation.z = ang; };
  g.userData.set(0);
  return g;
}
function forceps() {
  const g = new THREE.Group();
  const arms = [];
  for (const side of [1, -1]) {
    const s = new THREE.Shape();
    s.moveTo(0, 0); s.lineTo(0.008 * side, 0); s.lineTo(0.03 * side, 0.45); s.lineTo(0.04 * side, 1.05); s.lineTo(0.0, 1.08); s.lineTo(0, 0);
    const arm = new THREE.Group();
    const m = mesh(extrude(s, 0.014), MAT.steel()); m.position.y = -1.06; arm.add(m);
    for (let i = 0; i < 6; i++) arm.add(mesh(new THREE.BoxGeometry(0.03, 0.006, 0.016), MAT.brushed(), [0.022 * side, -0.5 + i * 0.04, 0]));
    arm.position.y = 1.06;
    g.add(arm); arms.push({ arm, side });
  }
  g.userData.set = (v) => { const ang = (1 - v) * 0.035; arms.forEach(({ arm, side }) => { arm.rotation.z = -ang * side; }); };
  g.userData.set(0);
  return g;
}
function needle() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.ConeGeometry(0.005, 0.32, 8), MAT.steel(), [0, 0.16, 0]).rotateX(Math.PI));
  g.add(mesh(lathe([[0.0, 0.3], [0.012, 0.3], [0.02, 0.34], [0.03, 0.4], [0.03, 0.9], [0.022, 0.95], [0, 0.96]], 16), MAT.gloss(0x8b5a2b)));
  return g;
}
export function pinModel(color = 0xef4444) {
  const g = new THREE.Group();
  g.add(mesh(new THREE.CylinderGeometry(0.0035, 0.002, 0.34, 6), MAT.steel(), [0, 0.17, 0]));
  g.add(mesh(new THREE.SphereGeometry(0.022, 14, 10), MAT.gloss(color), [0, 0.35, 0]));
  return g;
}
function dropper() {
  const g = new THREE.Group();
  g.add(mesh(lathe([[0.004, 0], [0.008, 0.02], [0.012, 0.18], [0.03, 0.26], [0.032, 0.62], [0.036, 0.64], [0.0, 0.64]], 16), MAT.glass(), null, { cast: false }));
  const liq = mesh(lathe([[0.002, 0.003], [0.006, 0.02], [0.009, 0.18], [0.026, 0.26], [0.027, 0.38], [0, 0.38]], 14), MAT.liquid(0xbe185d, 0.75).clone(), null, { cast: false });
  liq.material.userData.sharedFx = false;
  g.add(liq);
  const bulb = mesh(lathe([[0.034, 0.62], [0.05, 0.68], [0.055, 0.8], [0.04, 0.88], [0, 0.9]], 18), MAT.gloss(0x991b1b));
  g.add(bulb);
  g.userData.liquid = liq;
  g.userData.set = (v) => { bulb.scale.set(1 - v * 0.25, 1, 1 - v * 0.25); };
  return g;
}
function brush() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.ConeGeometry(0.018, 0.12, 10), MAT.matte(0x3f2a1d), [0, 0.06, 0]).rotateX(Math.PI));
  g.add(mesh(new THREE.CylinderGeometry(0.02, 0.018, 0.08, 12), MAT.brushed(), [0, 0.15, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.016, 0.022, 0.9, 12), MAT.gloss(0xc2410c), [0, 0.64, 0]));
  return g;
}
function razor() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.BoxGeometry(0.44, 0.19, 0.003), MAT.blade(), [0, 0.095, 0]));
  g.add(mesh(new THREE.BoxGeometry(0.46, 0.04, 0.014), MAT.brushed(), [0, 0.2, 0]));
  return g;
}
function lens() {
  const g = new THREE.Group();
  const ring = mesh(new THREE.TorusGeometry(0.3, 0.025, 10, 40), MAT.gloss(0x111827));
  ring.rotation.x = Math.PI / 2; g.add(ring);
  const glass = mesh(new THREE.CircleGeometry(0.29, 40), MAT.glass(), null, { cast: false }); glass.rotation.x = -Math.PI / 2; g.add(glass);
  g.userData.glass = glass;
  const h = mesh(new THREE.CylinderGeometry(0.03, 0.035, 0.7, 12), MAT.gloss(0x111827), [0.62, 0, 0]); h.rotation.z = Math.PI / 2; g.add(h);
  return g;
}
function loop() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.TorusGeometry(0.018, 0.0035, 6, 16), MAT.steel(), [0, 0.018, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.003, 0.003, 0.5, 6), MAT.steel(), [0, 0.28, 0]));
  g.add(mesh(lathe([[0.0, 0.5], [0.012, 0.5], [0.022, 0.56], [0.022, 1.05], [0, 1.08]], 12), MAT.gloss(0x1d4ed8)));
  return g;
}
function spreader() {
  const g = new THREE.Group(); const glass = MAT.glassEdge();
  const foot = mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.36, 10), glass, [0.18, 0.012, 0], { cast: false }); foot.rotation.z = Math.PI / 2; g.add(foot);
  g.add(mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.9, 10), glass, [0, 0.46, 0], { cast: false }));
  return g;
}
function marker() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.ConeGeometry(0.012, 0.05, 10), MAT.gloss(0x111827), [0, 0.025, 0]).rotateX(Math.PI));
  g.add(mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.6, 14), MAT.gloss(0xf8fafc), [0, 0.35, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.12, 14), MAT.gloss(0x111827), [0, 0.7, 0]));
  return g;
}
function plainGroup() { return new THREE.Group(); }
function bottle() {
  const g = new THREE.Group();
  const b = washBottle(); b.scale.setScalar(0.8);
  // the nozzle's end is the tool tip; the bottle hangs back and up from it, squeezed and tilted
  b.rotation.z = -2.45; b.position.set(-0.345, 0.856, 0);
  g.add(b);
  g.userData.set = (v) => { b.scale.set(0.8 * (1 - v * 0.08), 0.8, 0.8 * (1 + v * 0.05)); };
  return g;
}

const BUILDERS = { loop, spreader, marker, scalpel, scissors, forceps, needle, pin: () => pinModel(0xef4444), dropper, brush, razor, lens, hand: plainGroup, coverslip: plainGroup, paper: plainGroup, washbottle: bottle, slide: plainGroup, lamp: plainGroup, tube: plainGroup };

/** Handle lean per tool: [toward camera, up, right] weights. A razor is held flat. */
const LEAN = { loop: [0.5, 1, 0.3], spreader: [0.4, 1, 0.2], marker: [0.4, 1, 0.3], washbottle: [0, 1, 0], scalpel: [0.75, 0.9, 0.35], scissors: [0.55, 1, 0.45], forceps: [0.6, 1, 0.4], needle: [0.7, 0.95, 0.35], pin: [0.2, 1, 0.15], dropper: [0.1, 1, 0.05], brush: [0.6, 1, 0.35], razor: [0.0, 1, 0.0], lens: [0, 1, 0] };
const SCALE = { lens: 0.8, pin: 0.75, dropper: 0.75, washbottle: 1 };
const LIFT = { loop: 0.03, spreader: 0.03, marker: 0.03, washbottle: 0.5, scalpel: 0.05, scissors: 0.05, forceps: 0.06, needle: 0.05, pin: 0.1, dropper: 0.18, brush: 0.04, razor: 0.06, lens: 0.16 };

export function createToolRig(scene, camera) {
  const holder = new THREE.Group();
  holder.visible = false;
  scene.add(holder);
  const models = new Map();
  let current = null; let currentId = null;
  const pos = new SpringV3(1600, 1.0);
  const press = new Spring(0, 260, 0.9);
  const action = new Spring(0, 500, 0.7);
  const visibleK = new Spring(0, 200, 1);
  const goal = new THREE.Vector3();
  const toCam = new THREE.Vector3();
  const prev = new THREE.Vector3();
  const vel = new THREE.Vector3();
  const vx = new THREE.Vector3(); const vy = new THREE.Vector3(); const vz = new THREE.Vector3();
  const camRight = new THREE.Vector3(); const camBack = new THREE.Vector3();
  const m4 = new THREE.Matrix4();
  const tiltQ = new THREE.Quaternion();
  let shown = false; let hasGoal = false;
  let liftScale = 1;

  function get(id) {
    if (!models.has(id)) { const m = (BUILDERS[id] || plainGroup)(); m.traverse((o) => { if (o.isMesh) o.userData.noPick = true; }); models.set(id, m); }
    return models.get(id);
  }
  return {
    holder,
    get id() { return currentId; },
    get model() { return current; },
    use(id) {
      if (currentId === id) return;
      if (current) holder.remove(current);
      currentId = id; current = id && id !== 'hand' ? get(id) : null;
      if (current) { holder.add(current); visibleK.snap(0.2); }
    },
    /** Where the tip should be (world). Call each frame the pointer is meaningful. */
    aim(p) { goal.copy(p); if (!hasGoal) { pos.snap(p); prev.copy(p); } hasGoal = true; },
    show(v) { shown = v; },
    press(v) { press.target = v; },
    action(v) { action.target = v; },
    setLift(k) { liftScale = k; },
    get tip() { return pos.v; },
    update(dt) {
      visibleK.target = shown && current && hasGoal ? 1 : 0;
      visibleK.step(dt);
      holder.visible = visibleK.v > 0.02 && !!current;
      if (!current) return;
      // hover the tool toward the eye along the line of sight, so its tip stays exactly under the pointer
      const lift = (LIFT[currentId] ?? 0.06) * liftScale;
      toCam.subVectors(camera.position, goal).normalize();
      pos.target.copy(goal).addScaledVector(toCam, lift * (1 - press.v));
      press.step(dt); action.step(dt);
      prev.copy(pos.v); pos.step(dt);
      vel.subVectors(pos.v, prev).divideScalar(Math.max(dt, 1e-3));
      holder.position.copy(pos.v);
      const w = LEAN[currentId] || LEAN.needle;
      camera.matrixWorld.extractBasis(camRight, vx, camBack);
      camBack.y = 0; camBack.normalize(); camRight.y = 0; camRight.normalize();
      vy.set(0, 0, 0).addScaledVector(camBack, w[0]).addScaledVector(camRight, w[2]); vy.y += w[1];
      vy.addScaledVector(vel, -0.025); vy.normalize();
      if (currentId === 'razor' || currentId === 'lens' || currentId === 'washbottle') { vz.copy(camBack); vz.y = 0; vz.normalize(); vy.set(0, 1, 0); }
      else { vz.copy(camBack).addScaledVector(vy, -camBack.dot(vy)).normalize(); }
      vx.crossVectors(vy, vz).normalize();
      m4.makeBasis(vx, vy, vz);
      holder.quaternion.setFromRotationMatrix(m4);
      if (currentId === 'razor') { tiltQ.setFromAxisAngle(vx.set(1, 0, 0), -1.35); holder.quaternion.multiply(tiltQ); }
      const camDist = camera.position.distanceTo(pos.v);
      const s = (0.85 + 0.15 * visibleK.v) * (SCALE[currentId] || 0.62) * clamp(camDist / 2.2, currentId === 'lens' ? 0.7 : 0.38, 1);
      holder.scale.setScalar(s);
      if (current.userData.set) current.userData.set(clamp(action.v, 0, 1));
    },
    dispose() { scene.remove(holder); },
  };
}
