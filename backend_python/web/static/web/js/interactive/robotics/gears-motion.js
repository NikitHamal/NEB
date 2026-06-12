import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

function buildGear(radius, teeth, color, seg) {
  const group = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.45, metalness: 0.35 });
  const disk = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, 0.3, Math.max(seg, teeth * 2)), mat);
  group.add(disk);
  const toothW = (Math.PI * 2 * radius) / teeth * 0.45;
  const tooth = new THREE.BoxGeometry(toothW, 0.3, 0.36);
  for (let i = 0; i < teeth; i++) {
    const a = (i / teeth) * Math.PI * 2;
    const t = new THREE.Mesh(tooth, mat);
    t.position.set(Math.cos(a) * (radius + 0.16), 0, Math.sin(a) * (radius + 0.16));
    t.rotation.y = -a;
    group.add(t);
  }
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.5, 16), new THREE.MeshStandardMaterial({ color: 0x22344f, roughness: 0.6, metalness: 0.4 }));
  group.add(hub);
  const markMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x666666 });
  const mark = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.32, radius * 0.7), markMat);
  mark.position.z = radius * 0.5;
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

  basicLights(scene);
  const grid = new THREE.GridHelper(16, 16, 0x35507c, 0x22344f);
  grid.position.y = -1.2;
  scene.add(grid);

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
        if (o.geometry) o.geometry.dispose();
        if (o.material && o.material.map) o.material.map.dispose();
        if (o.material) o.material.dispose();
      });
    }
    gearGroup = new THREE.Group();
    const rDriver = 1.1;
    const rOut = rDriver * ratio;
    const teethOut = Math.round(baseTeeth * ratio);
    driverGear = buildGear(rDriver, baseTeeth, 0x3ba7e8, seg);
    outputGear = buildGear(rOut, teethOut, 0xf5b942, seg);
    outDist = rDriver + rOut + 0.36;
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
