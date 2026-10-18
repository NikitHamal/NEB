import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, showInfoCard } from '../core/sim-ui.js';
import { workshop, RM, wheel, servo, ultrasonic, pcbBoard, batteryPack, shadows } from '../core/robot-kit.js';

const PART_INFO = {
  head: { title: 'Sensors (the senses)', body: 'The head holds the robot\'s sensors — its eyes and ears. Cameras, distance sensors and microphones let the robot notice the world around it, just like your senses do.' },
  antenna: { title: 'Antenna (the voice)', body: 'The antenna sends and receives radio messages, so the robot can talk to computers, phones or other robots — like shouting and listening across the room without wires.' },
  body: { title: 'Controller (the brain)', body: 'Inside the chest sits the controller — a tiny computer. It reads the sensors, makes decisions hundreds of times a second, and tells the motors what to do. It is the robot\'s brain!' },
  battery: { title: 'Battery (the food)', body: 'The glowing pack on the back is the battery — the robot\'s lunchbox. It stores electrical energy and feeds every other part. No battery, no robot!' },
  armL: { title: 'Motors (the muscles)', body: 'Arms move thanks to motors — the robot\'s muscles. Motors turn electrical energy into spinning and lifting. Press "Wave arm" to watch this motor work!' },
  armR: { title: 'Motors (the muscles)', body: 'Arms move thanks to motors — the robot\'s muscles. Motors turn electrical energy into spinning and lifting. Press "Wave arm" to watch this motor work!' },
  wheelL: { title: 'Wheels (the legs)', body: 'Wheels driven by motors let the robot travel around. Two wheels with separate motors can drive straight, curve, or even spin in place!' },
  wheelR: { title: 'Wheels (the legs)', body: 'Wheels driven by motors let the robot travel around. Two wheels with separate motors can drive straight, curve, or even spin in place!' },
  chassis: { title: 'Chassis (the skeleton)', body: 'The lower frame is the chassis — the robot\'s skeleton. It is the strong base that holds the brain, battery, motors and wheels together in one sturdy body.' },
};

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(4.2, 3.4, 6.2);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 14, target: new THREE.Vector3(0, 1.5, 0),
  });

  // a bright workshop, and a robot built from real parts: an aluminium chassis on treaded
  // wheels, a clear-coated shell with its circuit board showing through a smoked window, a
  // battery pack on its back, a face screen for a head, servo shoulders and gripper hands
  workshop(scene, engine, quality, { radius: 18, tiles: 4, shadowSize: 5 });
  const robot = new THREE.Group();
  scene.add(robot);
  const name = (o, n) => { o.name = n; o.traverse((c) => { c.name = n; }); return o; };
  const blue = RM.shell(0x2f7de1);

  const chassis = name(new THREE.Group(), 'chassis');
  const plate = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.12, 1.3), RM.darkAlu()); plate.position.y = 0.5; chassis.add(plate);
  const skirt = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.3, 1.1), RM.matte(0x2b3138)); skirt.position.y = 0.32; chassis.add(skirt);
  const caster = new THREE.Mesh(new THREE.SphereGeometry(0.14, 20, 14), RM.steel()); caster.position.set(0, 0.14, -0.45); chassis.add(caster);
  name(chassis, 'chassis'); robot.add(chassis);

  const wheelL = name(wheel(0.42, 0.26), 'wheelL'); wheelL.position.set(-1.08, 0.42, 0.18); wheelL.rotation.y = Math.PI; robot.add(wheelL);
  const wheelR = name(wheel(0.42, 0.26), 'wheelR'); wheelR.position.set(1.08, 0.42, 0.18); robot.add(wheelR);

  const body = new THREE.Mesh(new THREE.BoxGeometry(1.36, 1.3, 0.96), blue); body.position.y = 1.23; body.name = 'body'; robot.add(body);
  const window_ = new THREE.Mesh(new THREE.BoxGeometry(0.92, 0.7, 0.02), RM.glassDark()); window_.position.set(0, 1.28, 0.49); window_.name = 'body'; robot.add(window_);
  const board = name(pcbBoard(0.8, 0.6), 'body'); board.rotation.x = Math.PI / 2; board.position.set(0, 1.28, 0.47); robot.add(board);
  const chest = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.04, 20), RM.glow(0x38bdf8, 1.4)); chest.rotation.x = Math.PI / 2; chest.position.set(0.36, 0.78, 0.49); chest.name = 'body'; robot.add(chest);

  const battery = name(batteryPack(), 'battery'); battery.position.set(0, 1.18, -0.62); robot.add(battery);

  const head = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.74, 0.82), blue); head.position.y = 2.32; head.name = 'head'; robot.add(head);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, 0.18, 20), RM.darkAlu()); neck.position.y = 1.92; neck.name = 'head'; robot.add(neck);
  const face = new THREE.Mesh(new THREE.BoxGeometry(0.84, 0.52, 0.02), RM.glassDark()); face.position.set(0, 2.33, 0.415); face.name = 'head'; robot.add(face);
  const eyeGeo = new THREE.CapsuleGeometry(0.07, 0.1, 6, 12);
  const matEye = RM.glow(0x7fe9ff, 2.2);
  const eyeL = new THREE.Mesh(eyeGeo, matEye); eyeL.position.set(-0.2, 2.37, 0.43); eyeL.name = 'head'; robot.add(eyeL);
  const eyeR = eyeL.clone(); eyeR.position.x = 0.2; robot.add(eyeR);
  const mouth = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.035, 0.01), RM.glow(0x7fe9ff, 1.2)); mouth.position.set(0, 2.18, 0.43); mouth.name = 'head'; robot.add(mouth);
  // the head's real senses: an ultrasonic ranger on the brow
  const sonar = name(ultrasonic(), 'head'); sonar.scale.setScalar(0.5); sonar.position.set(0, 2.78, 0.3); robot.add(sonar);

  const antennaPole = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.55, 10), RM.alu()); antennaPole.position.set(0.32, 2.96, -0.1); antennaPole.name = 'antenna'; robot.add(antennaPole);
  const antennaTip = new THREE.Mesh(new THREE.SphereGeometry(0.08, 16, 12), new THREE.MeshStandardMaterial({ color: 0xff5d73, emissive: 0xff2244, emissiveIntensity: 0.8 })); antennaTip.position.set(0.32, 3.26, -0.1); antennaTip.name = 'antenna'; robot.add(antennaTip);

  function makeArm(side) {
    const pivot = new THREE.Group();
    pivot.position.set(side * 0.86, 1.7, 0);
    const n = side < 0 ? 'armL' : 'armR';
    const sv = name(servo(0x1f2937), n); sv.rotation.z = Math.PI / 2; sv.scale.setScalar(0.8); pivot.add(sv);
    const upper = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.78, 0.16), RM.alu()); upper.position.set(side * 0.12, -0.45, 0); upper.name = n; pivot.add(upper);
    const wrist = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.12, 16), RM.darkAlu()); wrist.position.set(side * 0.12, -0.88, 0); wrist.name = n; pivot.add(wrist);
    for (const z of [-0.07, 0.07]) { const finger = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.22, 0.04), RM.matte(0xf59e0b)); finger.position.set(side * 0.12, -1.04, z); finger.name = n; pivot.add(finger); }
    shadows(pivot);
    robot.add(pivot);
    return pivot;
  }
  const armPivotL = makeArm(-1);
  const armPivotR = makeArm(1);
  shadows(robot);

  const labelDefs = [
    { text: 'Sensors', pos: [0, 3.15, 0.5], part: head },
    { text: 'Brain', pos: [-1.55, 1.3, 0.4], part: body },
    { text: 'Battery', pos: [0, 1.25, -1.35], part: battery },
    { text: 'Motors', pos: [1.75, 1.85, 0], part: armPivotR },
    { text: 'Wheels', pos: [-1.85, 0.5, 0.5], part: wheelL },
  ];
  const labels = [];
  labelDefs.forEach((d) => {
    const sprite = makeLabelSprite(d.text, { scale: 0.55, fontSize: 42 });
    sprite.position.set(d.pos[0], d.pos[1], d.pos[2]);
    robot.add(sprite);
    labels.push(sprite);
  });

  const panel = createPanel(stage, { title: 'Robot Controls' });
  let spinning = false;
  let waveT = -1;
  let blinkT = -1;

  panel.toggle({ label: 'Spin robot', value: false, onChange: (v) => { spinning = v; } });
  panel.buttonRow([
    { label: 'Wave arm', icon: 'waving_hand', onClick: () => { waveT = 0; } },
    { label: 'Blink eyes', icon: 'visibility', onClick: () => { blinkT = 0; } },
  ]);
  panel.toggle({ label: 'Show labels', value: true, onChange: (v) => labels.forEach((l) => { l.visible = v; }) });
  panel.info('Tap any robot part to learn what it does. Drag to look around!');

  const clickable = [robot];
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let downPos = null;
  function onDown(e) { downPos = { x: e.clientX, y: e.clientY }; }
  function onUp(e) {
    if (!downPos || Math.hypot(e.clientX - downPos.x, e.clientY - downPos.y) > 8) return;
    const rect = engine.canvas.getBoundingClientRect();
    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(clickable, true).filter((h) => h.object.name && !h.object.isSprite);
    if (hits.length) {
      let name = hits[0].object.name;
      if (hits[0].object === eyeL || hits[0].object === eyeR) name = 'head';
      const info = PART_INFO[name];
      if (info) showInfoCard(stage, { title: info.title, body: info.body, color: '#0EA5E9' });
    }
  }
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);

  engine.setUpdate((dt, t) => {
    if (spinning) robot.rotation.y += dt * 1.2;
    robot.position.y = Math.sin(t * 1.6) * 0.04;
    antennaTip.material.emissiveIntensity = 0.6 + Math.sin(t * 4) * 0.4;

    if (waveT >= 0) {
      waveT += dt;
      const p = waveT / 1.6;
      if (p >= 1) {
        waveT = -1;
        armPivotR.rotation.z = 0;
      } else {
        const lift = Math.min(p * 4, 1, (1 - p) * 4);
        armPivotR.rotation.z = 2.4 * lift + Math.sin(waveT * 10) * 0.25 * lift;
      }
    }

    if (blinkT >= 0) {
      blinkT += dt;
      const p = blinkT / 0.5;
      if (p >= 1) {
        blinkT = -1;
        eyeL.scale.y = 1;
        eyeR.scale.y = 1;
      } else {
        const s = Math.max(0.08, Math.abs(Math.cos(p * Math.PI)));
        eyeL.scale.y = s;
        eyeR.scale.y = s;
      }
    }

    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown);
      engine.canvas.removeEventListener('pointerup', onUp);
      const infoCard = stage.querySelector('.ix-info-card');
      if (infoCard) infoCard.remove();
      controls.dispose();
      panel.dispose();
      engine.dispose();
    },
  };
}
