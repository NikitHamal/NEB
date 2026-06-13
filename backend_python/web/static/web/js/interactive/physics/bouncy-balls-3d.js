import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const GRAVITY_PRESETS = { earth: 9.81, moon: 1.62, jupiter: 24.8 };
const COLORS = [0xfb7185, 0xfbbf24, 0x34d399, 0x38bdf8, 0xc084fc, 0xf472b6];

export default function init(stage, opts) {
  const engine = createEngine(stage, {});
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 4, 12);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 30,
    target: new THREE.Vector3(0, 2, 0),
  });
  controls.setTarget(new THREE.Vector3(0, 2, 0));

  basicLights(scene, { ambient: 0.5, key: 1.4 });
  scene.background = new THREE.Color(0x0b1c30);

  // Box walls (transparent)
  const BOX_W = 7, BOX_H = 8, BOX_D = 4;
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x1a3a60, transparent: true, opacity: 0.18, side: THREE.BackSide, roughness: 0.9 });
  const boxGeo = new THREE.BoxGeometry(BOX_W, BOX_H, BOX_D);
  const boxMesh = new THREE.Mesh(boxGeo, wallMat);
  boxMesh.position.set(0, BOX_H / 2, 0);
  scene.add(boxMesh);

  // Floor
  const floorGeo = new THREE.PlaneGeometry(BOX_W, BOX_D);
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.9 });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = 0.01;
  if (quality.shadows) floor.receiveShadow = true;
  scene.add(floor);

  // Edge frame lines
  const edgeMat = new THREE.LineBasicMaterial({ color: 0x2a5080, transparent: true, opacity: 0.5 });
  const edges = new THREE.EdgesGeometry(new THREE.BoxGeometry(BOX_W, BOX_H, BOX_D));
  const edgeLines = new THREE.LineSegments(edges, edgeMat);
  edgeLines.position.set(0, BOX_H / 2, 0);
  scene.add(edgeLines);

  // Planet label
  const planetLabel = makeLabelSprite('Earth  g = 9.81 m/s²', { scale: 1.4, fontSize: 34 });
  planetLabel.position.set(0, BOX_H + 0.4, 0);
  scene.add(planetLabel);

  // Ball pool
  const MAX_N = quality.tier === 'low' ? 6 : 10;
  const balls = [];
  const ballMeshes = [];

  function updatePlanetLabel(label) {
    const newSprite = makeLabelSprite(label, { scale: 1.4, fontSize: 34 });
    planetLabel.material.map.dispose();
    planetLabel.material = newSprite.material;
    planetLabel.scale.copy(newSprite.scale);
    scene.remove(newSprite);
  }

  function addBall(wx, wy, wz) {
    if (balls.length >= MAX_N) {
      const old = balls.shift();
      const oldMesh = ballMeshes.shift();
      scene.remove(oldMesh);
      oldMesh.geometry.dispose();
      oldMesh.material.dispose();
    }
    const r = 0.18 + Math.random() * 0.12;
    const colorIdx = (balls.length) % COLORS.length;
    const geo = new THREE.SphereGeometry(r, seg, seg);
    const mat = new THREE.MeshStandardMaterial({ color: COLORS[colorIdx], roughness: 0.5, metalness: 0.1, emissiveIntensity: 0.1, emissive: new THREE.Color(COLORS[colorIdx]).multiplyScalar(0.15) });
    const mesh = new THREE.Mesh(geo, mat);
    if (quality.shadows) { mesh.castShadow = true; }
    scene.add(mesh);
    ballMeshes.push(mesh);
    balls.push({ x: wx, y: wy, z: wz, vx: (Math.random() - 0.5) * 3, vy: 0, vz: (Math.random() - 0.5) * 1.5, r });
  }

  // Click to drop
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  function onPointerDown(e) {
    const rect = engine.canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    const pt = new THREE.Vector3();
    raycaster.ray.intersectPlane(plane, pt);
    if (pt) {
      const bx = Math.max(-BOX_W / 2 + 0.3, Math.min(BOX_W / 2 - 0.3, pt.x));
      addBall(bx, Math.min(BOX_H - 0.3, pt.y || BOX_H * 0.8), 0);
    }
    e.preventDefault();
  }
  engine.canvas.addEventListener('pointerdown', onPointerDown);

  let g = 9.81;
  let bounciness = 0.75;

  const panel = createPanel(stage, { title: 'Bounce 3D' });
  const gravSelect = panel.select({
    label: 'Planet',
    options: [
      { value: 'earth', label: 'Earth (9.81 m/s²)' },
      { value: 'moon', label: 'Moon (1.62 m/s²)' },
      { value: 'jupiter', label: 'Jupiter (24.8 m/s²)' },
      { value: 'custom', label: 'Custom' },
    ],
    value: 'earth',
    onChange: (v) => {
      if (v !== 'custom') {
        g = GRAVITY_PRESETS[v];
        gravSlider.set(g);
        updatePlanetLabel(`${v.charAt(0).toUpperCase() + v.slice(1)}  g = ${g.toFixed(2)} m/s²`);
      }
    },
  });
  const gravSlider = panel.slider({
    label: 'Gravity g', min: 1, max: 30, step: 0.1, value: g,
    format: (v) => `${v.toFixed(1)} m/s²`,
    onChange: (v) => { g = v; gravSelect.set('custom'); updatePlanetLabel(`Custom  g = ${v.toFixed(1)} m/s²`); },
  });
  panel.slider({
    label: 'Bounciness', min: 0.3, max: 0.95, step: 0.05, value: bounciness,
    format: (v) => `${Math.round(v * 100)}%`,
    onChange: (v) => { bounciness = v; },
  });
  panel.divider();
  const countOut = panel.readout({ label: 'Balls', value: '0' });
  panel.button({ label: 'Clear balls', icon: 'mop', onClick: () => { balls.length = 0; ballMeshes.forEach((m) => { scene.remove(m); m.geometry.dispose(); m.material.dispose(); }); ballMeshes.length = 0; } });
  panel.info('Click in the 3D box to drop a ball. Try Moon gravity for graceful slow bounces, Jupiter for heavy fast ones!');

  const hud = createHud(stage);
  const badge = hud.badge('Click the box to drop balls!', '#F59E0B');

  engine.setUpdate((dt) => {
    controls.update(dt);
    const ddt = Math.min(dt, 0.05);
    const HW = BOX_W / 2, HH = BOX_H, HD = BOX_D / 2;

    for (let i = 0; i < balls.length; i++) {
      const b = balls[i];
      b.vy -= g * ddt;
      b.x += b.vx * ddt;
      b.y += b.vy * ddt;
      b.z += b.vz * ddt;

      // Floor bounce
      if (b.y < b.r) {
        b.y = b.r;
        if (Math.abs(b.vy) > 0.3) { b.vy = -b.vy * bounciness; } else { b.vy = 0; }
        b.vx *= 0.985;
        b.vz *= 0.985;
      }
      // Ceiling
      if (b.y > HH - b.r) { b.y = HH - b.r; b.vy = -Math.abs(b.vy) * bounciness; }
      // Side walls X
      if (b.x < -HW + b.r) { b.x = -HW + b.r; b.vx = Math.abs(b.vx) * bounciness; }
      if (b.x > HW - b.r) { b.x = HW - b.r; b.vx = -Math.abs(b.vx) * bounciness; }
      // Side walls Z
      if (b.z < -HD + b.r) { b.z = -HD + b.r; b.vz = Math.abs(b.vz) * bounciness; }
      if (b.z > HD - b.r) { b.z = HD - b.r; b.vz = -Math.abs(b.vz) * bounciness; }

      ballMeshes[i].position.set(b.x, b.y, b.z);
    }

    // Ball-ball collisions
    for (let i = 0; i < balls.length; i++) {
      for (let j = i + 1; j < balls.length; j++) {
        const bi = balls[i], bj = balls[j];
        const dx = bj.x - bi.x, dy = bj.y - bi.y, dz = bj.z - bi.z;
        const minD = bi.r + bj.r;
        const d2 = dx * dx + dy * dy + dz * dz;
        if (d2 < minD * minD && d2 > 0.0001) {
          const d = Math.sqrt(d2);
          const nx = dx / d, ny = dy / d, nz = dz / d;
          const overlap = (minD - d) / 2;
          bi.x -= nx * overlap; bi.y -= ny * overlap; bi.z -= nz * overlap;
          bj.x += nx * overlap; bj.y += ny * overlap; bj.z += nz * overlap;
          const rel = (bj.vx - bi.vx) * nx + (bj.vy - bi.vy) * ny + (bj.vz - bi.vz) * nz;
          if (rel < 0) {
            const imp = -rel * (0.5 + bounciness / 2);
            bi.vx -= nx * imp * 0.5; bi.vy -= ny * imp * 0.5; bi.vz -= nz * imp * 0.5;
            bj.vx += nx * imp * 0.5; bj.vy += ny * imp * 0.5; bj.vz += nz * imp * 0.5;
          }
        }
      }
    }

    countOut.set(`${balls.length} / ${MAX_N}`);
    badge.set(balls.length === 0 ? 'Click the box to drop balls!' : `Bouncing on g = ${g.toFixed(1)} m/s²`);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onPointerDown);
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
