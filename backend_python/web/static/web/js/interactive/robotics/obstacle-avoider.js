import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { workshop, miniBot } from '../core/robot-kit.js';

// corrugated cardboard with a strip of packing tape: the obstacles a classroom robot meets
let CARD = null;
function cardboard() {
  if (CARD) return CARD;
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  g.fillStyle = '#c69c6d'; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 256; i += 6) { g.fillStyle = i % 12 ? 'rgba(120,84,48,0.10)' : 'rgba(255,240,210,0.08)'; g.fillRect(i, 0, 3, 256); }
  g.fillStyle = 'rgba(210,190,150,0.85)'; g.fillRect(0, 112, 256, 32);
  const t = new THREE.CanvasTexture(c); if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace;
  CARD = new THREE.MeshStandardMaterial({ map: t, roughness: 0.85 });
  return CARD;
}

const ARENA = 10;

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 9, 9.5);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 26, target: new THREE.Vector3(0, 0, 0),
  });

  workshop(scene, engine, quality, { radius: ARENA * 2.2, tiles: 6, shadowSize: ARENA });

  const wallMat = new THREE.MeshPhysicalMaterial({ color: 0xf5f7fa, roughness: 0.35, clearcoat: 0.6 });
  const wallGeo = new THREE.BoxGeometry(ARENA * 2, 0.7, 0.25);
  [[0, -ARENA, 0], [0, ARENA, 0], [-ARENA, 0, Math.PI / 2], [ARENA, 0, Math.PI / 2]].forEach((w) => {
    const m = new THREE.Mesh(wallGeo, wallMat);
    m.position.set(w[0], 0.35, w[1]);
    m.rotation.y = w[2];
    scene.add(m);
  });

  const obstacles = [];
  const boxMat = cardboard();
  const count = quality.tier === 'low' ? 6 : 9;
  let s = 7;
  function rand() { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }
  for (let i = 0; i < count; i++) {
    const size = 0.8 + rand() * 1.3;
    const m = new THREE.Mesh(new THREE.BoxGeometry(size, 0.9 + rand() * 0.8, size), boxMat);
    let x, z;
    do {
      x = (rand() * 2 - 1) * (ARENA - 2);
      z = (rand() * 2 - 1) * (ARENA - 2);
    } while (Math.hypot(x, z) < 2.5);
    m.position.set(x, m.geometry.parameters.height / 2, z);
    m.rotation.y = rand() * 0.6 - 0.3; m.castShadow = true; m.receiveShadow = true;
    scene.add(m);
    obstacles.push({ x, z, r: size * 0.72 });
  }

  const bot = miniBot({ color: 0xf97316 });
  const robot = bot.group;
  scene.add(robot);

  const coneMat = new THREE.MeshBasicMaterial({ color: 0x0ea5e9, transparent: true, opacity: 0.14, side: THREE.DoubleSide, depthWrite: false });
  let cone = null;
  function rebuildCone(range) {
    if (cone) {
      robot.remove(cone);
      cone.geometry.dispose();
    }
    const geo = new THREE.ConeGeometry(range * 0.38, range, Math.max(16, seg / 2), 1, true);
    cone = new THREE.Mesh(geo, coneMat);
    cone.rotation.x = -Math.PI / 2;
    cone.position.set(0, 0.5, range / 2);
    robot.add(cone);
  }

  const hud = createHud(stage);
  const stateBadge = hud.badge('IDLE', '#94a3b8');

  const panel = createPanel(stage, { title: 'Autopilot Controls' });
  let autopilot = false;
  let sensorRange = 3.0;
  let speed = 2.2;
  let heading = 0;
  let turnDir = 1;
  let turnTime = 0;
  const pos = { x: 0, z: 0 };

  rebuildCone(sensorRange);

  panel.toggle({
    label: 'Autopilot', value: false,
    onChange: (v) => {
      autopilot = v;
      if (!v) setState('IDLE', '#94a3b8');
    },
  });
  panel.slider({
    label: 'Sensor range', min: 1, max: 6, step: 0.25, value: sensorRange,
    format: (v) => v.toFixed(2) + ' m',
    onChange: (v) => { sensorRange = v; rebuildCone(v); },
  });
  panel.slider({
    label: 'Robot speed', min: 0.5, max: 5, step: 0.25, value: speed,
    format: (v) => v.toFixed(2) + ' m/s',
    onChange: (v) => { speed = v; },
  });
  const distRead = panel.readout({ label: 'Sensor distance', value: '—' });
  panel.button({
    label: 'Reset position', icon: 'restart_alt', variant: 'ghost',
    onClick: () => { pos.x = 0; pos.z = 0; heading = 0; },
  });
  panel.info('Sense → think → act. The robot cruises until its distance sensor sees something closer than its range, then it turns away and tries again.');

  let curState = 'IDLE';
  function setState(name, color) {
    if (curState === name) return;
    curState = name;
    stateBadge.set(name);
    stateBadge.el.style.setProperty('--ix-hud-color', color);
  }

  function senseDistance() {
    const dirX = Math.sin(heading);
    const dirZ = Math.cos(heading);
    let best = Infinity;
    obstacles.forEach((o) => {
      const rx = o.x - pos.x;
      const rz = o.z - pos.z;
      const proj = rx * dirX + rz * dirZ;
      if (proj <= 0) return;
      const perp = Math.abs(rx * dirZ - rz * dirX);
      if (perp < o.r + 0.45) {
        const d = proj - o.r;
        if (d < best) best = d;
      }
    });
    const tx = dirX > 0 ? (ARENA - 0.7 - pos.x) / dirX : dirX < 0 ? (-ARENA + 0.7 - pos.x) / dirX : Infinity;
    const tz = dirZ > 0 ? (ARENA - 0.7 - pos.z) / dirZ : dirZ < 0 ? (-ARENA + 0.7 - pos.z) / dirZ : Infinity;
    best = Math.min(best, tx, tz);
    return Math.max(0, best);
  }

  engine.setUpdate((dt) => {
    const dist = senseDistance();
    distRead.set(dist > 8 ? '> 8 m' : dist.toFixed(2) + ' m');

    if (autopilot) {
      if (dist < sensorRange) {
        if (curState !== 'TURNING') {
          turnDir = Math.random() < 0.5 ? -1 : 1;
          turnTime = 0;
        }
        setState('TURNING', '#f5b942');
        turnTime += dt;
        heading += turnDir * dt * 2.4;
        if (turnTime > 2.5) {
          heading += turnDir * dt * 2.4;
        }
        pos.x += Math.sin(heading) * speed * 0.15 * dt;
        pos.z += Math.cos(heading) * speed * 0.15 * dt;
      } else {
        setState('CRUISING', '#35d07f');
        pos.x += Math.sin(heading) * speed * dt;
        pos.z += Math.cos(heading) * speed * dt;
      }
      for (const o of obstacles) {
        const dx = pos.x - o.x;
        const dz = pos.z - o.z;
        const d = Math.hypot(dx, dz);
        const minD = o.r + 0.65;
        if (d < minD && d > 0.0001) {
          pos.x = o.x + (dx / d) * minD;
          pos.z = o.z + (dz / d) * minD;
        }
      }
      const lim = ARENA - 0.7;
      pos.x = Math.max(-lim, Math.min(lim, pos.x));
      pos.z = Math.max(-lim, Math.min(lim, pos.z));
    }

    // the wheels turn with the distance travelled
    const moved = Math.hypot(pos.x - robot.position.x, pos.z - robot.position.z);
    bot.wheelL.rotation.x += moved / 0.33; bot.wheelR.rotation.x += moved / 0.33;
    robot.position.set(pos.x, 0, pos.z);
    robot.rotation.y = heading;
    coneMat.opacity = curState === 'TURNING' ? 0.3 : 0.16;
    coneMat.color.set(curState === 'TURNING' ? 0xffd76a : 0x7fe9ff);

    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose();
      panel.dispose();
      hud.dispose();
      coneMat.dispose();
      engine.dispose();
    },
  };
}
