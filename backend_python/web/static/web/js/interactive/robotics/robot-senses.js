import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(2.5, 4.5, 9);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 4, maxDistance: 20, target: new THREE.Vector3(2.2, 1, 0),
  });

  basicLights(scene);
  const grid = new THREE.GridHelper(20, 20, 0x35507c, 0x22344f);
  scene.add(grid);
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshStandardMaterial({ color: 0x152338, roughness: 0.95 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.01;
  scene.add(ground);

  const robot = new THREE.Group();
  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x3ba7e8, roughness: 0.5, metalness: 0.25 });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x24344e, roughness: 0.6 });
  const body = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.8, 1.1), bodyMat);
  body.position.y = 0.75;
  robot.add(body);
  const wheelGeo = new THREE.CylinderGeometry(0.34, 0.34, 0.2, Math.max(16, seg / 2));
  [-0.62, 0.62].forEach((z) => {
    [-0.42, 0.42].forEach((x) => {
      const w = new THREE.Mesh(wheelGeo, darkMat);
      w.rotation.x = Math.PI / 2;
      w.position.set(x, 0.34, z);
      robot.add(w);
    });
  });
  const sensorBlock = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.42, 0.7), darkMat);
  sensorBlock.position.set(0.85, 0.95, 0);
  robot.add(sensorBlock);
  const eyeMat = new THREE.MeshStandardMaterial({ color: 0x101a2c, emissive: 0x7fe9ff, emissiveIntensity: 1.0 });
  const eyeGeo = new THREE.CylinderGeometry(0.14, 0.14, 0.1, 18);
  [-0.2, 0.2].forEach((z) => {
    const eye = new THREE.Mesh(eyeGeo, eyeMat);
    eye.rotation.z = Math.PI / 2;
    eye.position.set(1.02, 0.95, z);
    robot.add(eye);
  });
  const lbl = makeLabelSprite('Ultrasonic sensor', { scale: 0.7, fontSize: 38 });
  lbl.position.set(0.85, 1.8, 0);
  robot.add(lbl);
  robot.position.x = -3;
  scene.add(robot);

  const wall = new THREE.Mesh(
    new THREE.BoxGeometry(0.3, 2.6, 4),
    new THREE.MeshStandardMaterial({ color: 0xf5b942, roughness: 0.8 })
  );
  wall.position.set(1.5, 1.3, 0);
  scene.add(wall);
  const wallLbl = makeLabelSprite('Wall', { scale: 0.7, fontSize: 38 });
  wallLbl.position.y = 1.7;
  wall.add(wallLbl);

  const ringCount = 5;
  const ringMat = new THREE.MeshBasicMaterial({ color: 0x7fe9ff, transparent: true, opacity: 0.8, side: THREE.DoubleSide });
  const ringGeo = new THREE.TorusGeometry(0.5, 0.03, 8, Math.max(24, seg));
  const rings = [];
  for (let i = 0; i < ringCount; i++) {
    const m = new THREE.Mesh(ringGeo, ringMat.clone());
    m.rotation.y = Math.PI / 2;
    m.visible = false;
    scene.add(m);
    rings.push({ mesh: m, t: -1, echo: false });
  }

  const hud = createHud(stage);
  const distBadge = hud.badge('Distance: 120 cm', '#0EA5E9');

  const panel = createPanel(stage, { title: 'Sensor Lab' });
  let wallDist = 1.2;
  let showWaves = true;
  let pingTimer = 0;
  const SPEED = 3.43;

  const distRead = panel.readout({ label: 'Measured distance', value: '120 cm' });
  const timeRead = panel.readout({ label: 'Echo time', value: '7.0 ms' });
  panel.slider({
    label: 'Wall distance', min: 0.2, max: 3.5, step: 0.05, value: wallDist,
    format: (v) => Math.round(v * 100) + ' cm',
    onChange: (v) => { wallDist = v; },
  });
  panel.toggle({ label: 'Show sound wave', value: true, onChange: (v) => { showWaves = v; } });
  panel.button({
    label: 'Send ping now', icon: 'wifi_tethering',
    onClick: () => { firePing(); },
  });
  panel.info('Blue rings are the outgoing ping; gold rings are the echo bouncing back. Echo time × speed of sound ÷ 2 = distance.');

  const sensorX = () => robot.position.x + 1.02;

  function firePing() {
    const free = rings.find((r) => r.t < 0);
    if (!free) return;
    free.t = 0;
    free.echo = false;
    free.mesh.material.color.set(0x7fe9ff);
    free.mesh.visible = showWaves;
  }

  engine.setUpdate((dt, t) => {
    wall.position.x = sensorX() + wallDist + 0.15;
    const distCm = wallDist * 100;
    const echoMs = (2 * wallDist) / 343 * 1000;
    distRead.set(distCm.toFixed(0) + ' cm');
    timeRead.set(echoMs.toFixed(2) + ' ms');
    distBadge.set('Distance: ' + distCm.toFixed(0) + ' cm · Echo: ' + echoMs.toFixed(2) + ' ms');

    pingTimer -= dt;
    if (pingTimer <= 0) {
      firePing();
      pingTimer = 1.4;
    }

    rings.forEach((r) => {
      if (r.t < 0) return;
      r.t += dt;
      const travelled = r.t * SPEED;
      let x;
      if (travelled <= wallDist) {
        x = sensorX() + travelled;
        if (r.echo) {
          r.echo = false;
        }
      } else if (travelled <= wallDist * 2) {
        x = sensorX() + (wallDist * 2 - travelled);
        if (!r.echo) {
          r.echo = true;
          r.mesh.material.color.set(0xffd76a);
        }
      } else {
        r.t = -1;
        r.mesh.visible = false;
        return;
      }
      r.mesh.visible = showWaves;
      r.mesh.position.set(x, 0.95, 0);
      const grow = 0.4 + r.t * 1.1;
      r.mesh.scale.set(grow, grow, grow);
      r.mesh.material.opacity = Math.max(0.12, 0.85 - r.t * 0.5);
    });

    robot.position.y = Math.sin(t * 1.4) * 0.02;
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose();
      panel.dispose();
      hud.dispose();
      ringMat.dispose();
      engine.dispose();
    },
  };
}
