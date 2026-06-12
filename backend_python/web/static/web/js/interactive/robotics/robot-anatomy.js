import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, showInfoCard } from '../core/sim-ui.js';

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

  basicLights(scene);

  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(6, seg),
    new THREE.MeshStandardMaterial({ color: 0x1b2c47, roughness: 0.95 })
  );
  ground.rotation.x = -Math.PI / 2;
  scene.add(ground);
  const grid = new THREE.GridHelper(12, 24, 0x35507c, 0x22344f);
  grid.position.y = 0.001;
  scene.add(grid);

  const robot = new THREE.Group();
  scene.add(robot);

  const matBody = new THREE.MeshStandardMaterial({ color: 0x3ba7e8, roughness: 0.45, metalness: 0.25 });
  const matDark = new THREE.MeshStandardMaterial({ color: 0x24344e, roughness: 0.6, metalness: 0.3 });
  const matAccent = new THREE.MeshStandardMaterial({ color: 0xf5b942, roughness: 0.5, metalness: 0.2 });
  const matEye = new THREE.MeshStandardMaterial({ color: 0x0c1626, emissive: 0x7fe9ff, emissiveIntensity: 1.4 });
  const matBattery = new THREE.MeshStandardMaterial({ color: 0x35d07f, roughness: 0.4, emissive: 0x0d5c34, emissiveIntensity: 0.6 });

  const chassis = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.45, 1.2), matDark);
  chassis.position.y = 0.55;
  chassis.name = 'chassis';
  robot.add(chassis);

  const wheelGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.26, seg);
  const wheelL = new THREE.Mesh(wheelGeo, matAccent);
  wheelL.rotation.z = Math.PI / 2;
  wheelL.position.set(-0.98, 0.42, 0);
  wheelL.name = 'wheelL';
  robot.add(wheelL);
  const wheelR = wheelL.clone();
  wheelR.position.x = 0.98;
  wheelR.name = 'wheelR';
  robot.add(wheelR);

  const body = new THREE.Mesh(new THREE.BoxGeometry(1.35, 1.35, 0.95), matBody);
  body.position.y = 1.48;
  body.name = 'body';
  robot.add(body);

  const panelChip = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.6, 0.06), matDark);
  panelChip.position.set(0, 1.52, 0.49);
  robot.add(panelChip);
  const chipDot = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.05), matAccent);
  chipDot.position.set(0, 1.52, 0.53);
  robot.add(chipDot);

  const battery = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.55, 0.22), matBattery);
  battery.position.set(0, 1.42, -0.58);
  battery.name = 'battery';
  robot.add(battery);

  const head = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.75, 0.8), matBody);
  head.position.y = 2.62;
  head.name = 'head';
  robot.add(head);

  const eyeGeo = new THREE.SphereGeometry(0.13, Math.max(12, seg / 2), Math.max(12, seg / 2));
  const eyeL = new THREE.Mesh(eyeGeo, matEye);
  eyeL.position.set(-0.22, 2.7, 0.41);
  robot.add(eyeL);
  const eyeR = eyeL.clone();
  eyeR.position.x = 0.22;
  robot.add(eyeR);

  const mouth = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.07, 0.05), matDark);
  mouth.position.set(0, 2.42, 0.41);
  robot.add(mouth);

  const antennaPole = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.55, 10), matDark);
  antennaPole.position.set(0.25, 3.25, 0);
  antennaPole.name = 'antenna';
  robot.add(antennaPole);
  const antennaTip = new THREE.Mesh(new THREE.SphereGeometry(0.1, 12, 12), new THREE.MeshStandardMaterial({ color: 0xff5d73, emissive: 0xff2244, emissiveIntensity: 0.8 }));
  antennaTip.position.set(0.25, 3.55, 0);
  antennaTip.name = 'antenna';
  robot.add(antennaTip);

  function makeArm(side) {
    const pivot = new THREE.Group();
    pivot.position.set(side * 0.82, 2.0, 0);
    const upper = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.85, 0.22), matAccent);
    upper.position.y = -0.42;
    upper.name = side < 0 ? 'armL' : 'armR';
    pivot.add(upper);
    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.17, 12, 12), matDark);
    hand.position.y = -0.92;
    hand.name = upper.name;
    pivot.add(hand);
    robot.add(pivot);
    return pivot;
  }
  const armPivotL = makeArm(-1);
  const armPivotR = makeArm(1);

  const labelDefs = [
    { text: 'Sensors', pos: [0, 3.35, 0.2], part: head },
    { text: 'Brain', pos: [-1.45, 1.5, 0.3], part: body },
    { text: 'Battery', pos: [0, 1.42, -1.35], part: battery },
    { text: 'Motors', pos: [1.75, 2.15, 0], part: armPivotR },
    { text: 'Wheels', pos: [-1.75, 0.42, 0.4], part: wheelL },
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

  const clickable = [head, eyeL, eyeR, body, battery, antennaPole, antennaTip, wheelL, wheelR, chassis, ...armPivotL.children, ...armPivotR.children];
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
    const hits = raycaster.intersectObjects(clickable, false);
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
