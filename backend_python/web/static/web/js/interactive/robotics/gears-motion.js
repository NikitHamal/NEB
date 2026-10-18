import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { workshop, gear, RM } from '../core/robot-kit.js';

function buildGear(radius, teeth, color) {
  // a true involute spur gear (module = pitch diameter / teeth, so any pair with the same module
  // meshes), on a steel shaft, with a white index stripe to compare speeds by eye
  const group = new THREE.Group();
  const module = (radius * 2) / teeth;
  const mat = color === 'brass' ? RM.brass() : new THREE.MeshPhysicalMaterial({ color, roughness: 0.3, metalness: 0.75, clearcoat: 0.4 });
  const g = gear(teeth, mat, module, 0.32);
  g.rotation.x = -Math.PI / 2;
  group.add(g);
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(module * 0.85, module * 0.85, 1.6, 20), RM.steel());
  shaft.position.y = -0.55; shaft.castShadow = true;
  group.add(shaft);
  const collar = new THREE.Mesh(new THREE.CylinderGeometry(module * 1.6, module * 1.6, 0.14, 24), RM.steel());
  collar.position.y = 0.24; group.add(collar);
  const mark = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.02, radius * 0.62), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x555555 }));
  mark.position.set(0, 0.18, radius * 0.5);
  group.add(mark);
  return group;
}

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 6.5, 7.5);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 18, target: new THREE.Vector3(0, 0, 0),
  });

  // a workshop, and a machined aluminium base plate the gear train is mounted on
  const ws = workshop(scene, engine, quality, { radius: 18, tiles: 4, shadowSize: 6 });
  ws.floor.position.y = -1.6;
  const base = new THREE.Mesh(new THREE.BoxGeometry(9, 0.25, 4.6), RM.alu()); base.position.y = -1.32; base.receiveShadow = true; base.castShadow = true; scene.add(base);
  for (const x of [-4.2, 4.2]) for (const z of [-2.0, 2.0]) { const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.2, 16), RM.matte(0x1f2937)); foot.position.set(x, -1.5, z); scene.add(foot); }

  const hud = createHud(stage);
  const dirBadge = hud.badge('Driver ↻  Output ↺', '#0EA5E9');

  let driverRpm = 30;
  let ratio = 2;
  let driverAngle = 0;
  let gearGroup = null;
  let driverGear = null;
  let outputGear = null;
  let outDist = 0;

  const baseTeeth = 12;

  function rebuild() {
    if (gearGroup) {
      scene.remove(gearGroup);
      gearGroup.traverse((o) => {
        if (o.geometry && !o.geometry.userData?.sharedFx) o.geometry.dispose();
        if (o.material && o.material.map) o.material.map.dispose();
        if (o.material && !o.material.userData?.sharedFx) o.material.dispose();
      });
    }
    gearGroup = new THREE.Group();
    const rDriver = 1.1;
    const rOut = rDriver * ratio;
    const teethOut = Math.round(baseTeeth * ratio);
    driverGear = buildGear(rDriver, baseTeeth, 0x3b82c4);
    outputGear = buildGear(rOut, teethOut, 'brass');
    outDist = rDriver + rOut; // pitch circles touch: the gears mesh
    // a small DC gear motor drives the first shaft from below
    const motor = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.0, 28), RM.darkAlu()); motor.position.set(-outDist / 2, -2.0, 0); gearGroup.add(motor);
    const offset = -outDist / 2;
    driverGear.position.x = offset;
    outputGear.position.x = offset + outDist;
    outputGear.rotation.y = Math.PI / teethOut;
    gearGroup.add(driverGear, outputGear);

    const lblD = makeLabelSprite(`Driver · ${baseTeeth} teeth`, { scale: 0.8, fontSize: 40 });
    lblD.position.set(offset, 1.8, 0);
    gearGroup.add(lblD);
    const lblO = makeLabelSprite(`Output · ${teethOut} teeth`, { scale: 0.8, fontSize: 40 });
    lblO.position.set(offset + outDist, ratio > 1 ? rOut + 0.9 : 1.8, 0);
    gearGroup.add(lblO);

    scene.add(gearGroup);
  }
  rebuild();

  const panel = createPanel(stage, { title: 'Gear Controls' });
  const inRead = panel.readout({ label: 'Input RPM', value: '30' });
  const outRead = panel.readout({ label: 'Output RPM', value: '15' });
  panel.slider({
    label: 'Driver speed', min: 0, max: 60, step: 1, value: driverRpm,
    format: (v) => v + ' RPM',
    onChange: (v) => { driverRpm = v; },
  });
  panel.select({
    label: 'Gear ratio',
    options: [
      { value: '1', label: '1:1 — same speed' },
      { value: '2', label: '2:1 — half speed, double strength' },
      { value: '3', label: '3:1 — third speed, triple strength' },
    ],
    value: '2',
    onChange: (v) => { ratio = parseInt(v, 10); rebuild(); },
  });
  panel.info('The white stripe on each gear helps you compare speeds. Meshing gears always spin opposite ways!');

  engine.setUpdate((dt) => {
    const wIn = (driverRpm / 60) * Math.PI * 2;
    driverAngle += wIn * dt;
    if (driverGear) driverGear.rotation.y = driverAngle;
    if (outputGear) outputGear.rotation.y = -driverAngle / ratio + Math.PI / Math.round(baseTeeth * ratio);
    inRead.set(driverRpm.toString());
    outRead.set((driverRpm / ratio).toFixed(ratio === 3 ? 1 : 0));
    dirBadge.set(driverRpm > 0 ? 'Driver ↻   Output ↺  (opposite!)' : 'Paused');
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
