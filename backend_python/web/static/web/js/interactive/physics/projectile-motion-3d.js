import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

export default function init(stage, opts) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(-8, 6, 18);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 60,
    target: new THREE.Vector3(20, 3, 0),
  });
  controls.setTarget(new THREE.Vector3(20, 3, 0));

  basicLights(scene, { ambient: 0.45, key: 1.5 });
  scene.background = new THREE.Color(0x0b1c30);
  scene.fog = new THREE.Fog(0x0b1c30, 80, 200);

  // Ground plane
  const groundGeo = new THREE.PlaneGeometry(120, 30);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.9 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.set(55, 0, 0);
  if (quality.shadows) ground.receiveShadow = true;
  scene.add(ground);

  // Grid lines on ground
  const gridHelper = new THREE.GridHelper(120, 24, 0x1a3a20, 0x1a3a20);
  gridHelper.position.set(55, 0.01, 0);
  scene.add(gridHelper);

  // Cannon
  const cannonBaseGeo = new THREE.CylinderGeometry(0.6, 0.7, 0.6, 16);
  const cannonMat = new THREE.MeshStandardMaterial({ color: 0x5d779e, metalness: 0.6, roughness: 0.4 });
  const cannonBase = new THREE.Mesh(cannonBaseGeo, cannonMat);
  cannonBase.position.set(0, 0.3, 0);
  scene.add(cannonBase);

  const barrelGroup = new THREE.Group();
  barrelGroup.position.set(0, 0.5, 0);
  scene.add(barrelGroup);
  const barrelGeo = new THREE.CylinderGeometry(0.18, 0.22, 1.2, 12);
  const barrel = new THREE.Mesh(barrelGeo, cannonMat);
  barrel.rotation.z = Math.PI / 2;
  barrel.position.x = 0.55;
  barrelGroup.add(barrel);

  // Projectile ball
  const ballGeo = new THREE.SphereGeometry(0.2, seg, seg);
  const ballMat = new THREE.MeshStandardMaterial({ color: 0xffd584, metalness: 0.4, roughness: 0.4, emissive: 0x7a5000, emissiveIntensity: 0.2 });
  const ball = new THREE.Mesh(ballGeo, ballMat);
  ball.visible = false;
  if (quality.shadows) ball.castShadow = true;
  scene.add(ball);

  // Trajectory ribbon
  const MAX_TRAIL = 400;
  const trailPositions = new Float32Array(MAX_TRAIL * 3);
  const trailGeo = new THREE.BufferGeometry();
  trailGeo.setAttribute('position', new THREE.BufferAttribute(trailPositions, 3));
  const trailMat = new THREE.LineBasicMaterial({ color: 0xF59E0B, transparent: true, opacity: 0.7 });
  const trailLine = new THREE.Line(trailGeo, trailMat);
  scene.add(trailLine);
  let trailCount = 0;

  // Landing marker
  const markerGeo = new THREE.ConeGeometry(0.25, 0.6, 8);
  const markerMat = new THREE.MeshStandardMaterial({ color: 0x8be9a8, emissive: 0x003010, emissiveIntensity: 0.3 });
  const marker = new THREE.Mesh(markerGeo, markerMat);
  marker.visible = false;
  scene.add(marker);
  const markerLabel = makeLabelSprite('', { scale: 1.0, fontSize: 34 });
  markerLabel.visible = false;
  scene.add(markerLabel);

  // Target ring on ground
  const targetGeo = new THREE.RingGeometry(0.4, 0.55, 24);
  const targetMat = new THREE.MeshBasicMaterial({ color: 0x8be9a8, side: THREE.DoubleSide, transparent: true, opacity: 0.6 });
  const targetRing = new THREE.Mesh(targetGeo, targetMat);
  targetRing.rotation.x = -Math.PI / 2;
  targetRing.position.y = 0.02;
  targetRing.visible = false;
  scene.add(targetRing);

  // Ghost trails storage
  const ghosts = [];
  const GHOST_COLORS = [0x7dd3fc, 0xf472b6, 0xa3e635, 0xc084fc];
  const ghostLines = [];
  for (let i = 0; i < 4; i++) {
    const gGeo = new THREE.BufferGeometry();
    const gPos = new Float32Array(MAX_TRAIL * 3);
    gGeo.setAttribute('position', new THREE.BufferAttribute(gPos, 3));
    const gLine = new THREE.Line(gGeo, new THREE.LineBasicMaterial({ color: GHOST_COLORS[i], transparent: true, opacity: 0.35 }));
    gLine.visible = false;
    scene.add(gLine);
    ghostLines.push(gLine);
  }

  // Labels
  const rangeLabel = makeLabelSprite('', { scale: 1.0, fontSize: 32 });
  rangeLabel.visible = false;
  scene.add(rangeLabel);

  // State
  let speed = 30;
  let angle = 45;
  let g = 9.81;
  let airOn = false;
  let flying = false;
  let px = 0, py = 0, vx = 0, vy = 0;
  let flightTime = 0;
  let maxH = 0;
  let trailPts = [];

  // Panel
  const panel = createPanel(stage, { title: 'Launch Controls 3D' });
  panel.slider({
    label: 'Launch speed', min: 5, max: 60, step: 1, value: speed,
    format: (v) => `${v} m/s`, onChange: (v) => { speed = v; updateBarrel(); },
  });
  panel.slider({
    label: 'Launch angle', min: 5, max: 85, step: 1, value: angle,
    format: (v) => `${v}°`, onChange: (v) => { angle = v; updateBarrel(); },
  });
  panel.slider({
    label: 'Gravity g', min: 1, max: 25, step: 0.1, value: g,
    format: (v) => `${v.toFixed(1)} m/s²`, onChange: (v) => { g = v; },
  });
  panel.toggle({ label: 'Air resistance', value: false, onChange: (v) => { airOn = v; } });
  panel.buttonRow([
    { label: 'Fire!', icon: 'rocket_launch', onClick: fire },
    { label: 'Clear', icon: 'mop', variant: 'ghost', onClick: clearAll },
  ]);
  panel.divider();
  const rangeOut = panel.readout({ label: 'Range', value: '—' });
  const heightOut = panel.readout({ label: 'Max height', value: '—' });
  const timeOut = panel.readout({ label: 'Flight time', value: '—' });
  panel.info('Fire shots at different angles — old trajectories stay as ghost ribbons. 45° gives the farthest shot without air drag.');

  const hud = createHud(stage);
  const statusBadge = hud.badge('Ready to fire', '#F59E0B');

  function updateBarrel() {
    const rad = (angle * Math.PI) / 180;
    barrelGroup.rotation.z = rad;
  }
  updateBarrel();

  function fire() {
    if (trailPts.length > 2) {
      const ghostIdx = ghosts.length % 4;
      const gl = ghostLines[ghostIdx];
      const pos = gl.geometry.attributes.position.array;
      const n = Math.min(trailPts.length, MAX_TRAIL);
      for (let i = 0; i < n; i++) {
        pos[i * 3] = trailPts[i].x;
        pos[i * 3 + 1] = trailPts[i].y;
        pos[i * 3 + 2] = trailPts[i].z;
      }
      gl.geometry.setDrawRange(0, n);
      gl.geometry.attributes.position.needsUpdate = true;
      gl.visible = true;
      ghosts.push(1);
    }
    const rad = (angle * Math.PI) / 180;
    px = 0; py = 0.5;
    vx = speed * Math.cos(rad);
    vy = speed * Math.sin(rad);
    flightTime = 0; maxH = 0;
    trailPts = [{ x: px, y: py, z: 0 }];
    trailCount = 1;
    flying = true;
    ball.visible = true;
    marker.visible = false;
    markerLabel.visible = false;
    targetRing.visible = false;
    rangeLabel.visible = false;
    statusBadge.set('In flight…');
  }

  function clearAll() {
    ghosts.length = 0;
    ghostLines.forEach((l) => { l.visible = false; });
    trailPts = [];
    trailCount = 0;
    trailGeo.setDrawRange(0, 0);
    flying = false;
    ball.visible = false;
    marker.visible = false;
    markerLabel.visible = false;
    targetRing.visible = false;
    rangeLabel.visible = false;
    statusBadge.set('Ready to fire');
  }

  engine.setUpdate((dt) => {
    controls.update(dt);

    if (flying) {
      const sub = 6;
      const h = dt / sub;
      for (let i = 0; i < sub && flying; i++) {
        if (airOn) {
          const k = 0.012;
          const v = Math.hypot(vx, vy);
          vx -= k * v * vx * h;
          vy -= k * v * vy * h;
        }
        vy -= g * h;
        px += vx * h;
        py += vy * h;
        flightTime += h;
        if (py > maxH) maxH = py;
        if (py <= 0 && vy < 0) {
          py = 0;
          flying = false;
          ball.visible = false;
          marker.position.set(px, 0.3, 0);
          marker.visible = true;
          targetRing.position.set(px, 0.02, 0);
          targetRing.visible = true;
          const txt = `R = ${px.toFixed(1)} m`;
          markerLabel.material.map.dispose();
          const newLabel = makeLabelSprite(txt, { scale: 1.2, fontSize: 34, bg: 'rgba(11,28,48,0.82)' });
          newLabel.position.set(px, 1.2, 0);
          scene.add(newLabel);
          markerLabel.position.copy(newLabel.position);
          markerLabel.scale.copy(newLabel.scale);
          markerLabel.material = newLabel.material;
          markerLabel.visible = true;
          scene.remove(newLabel);
          rangeOut.set(`${px.toFixed(1)} m`);
          heightOut.set(`${maxH.toFixed(1)} m`);
          timeOut.set(`${flightTime.toFixed(2)} s`);
          statusBadge.set(`Landed at ${px.toFixed(0)} m`);
        } else if (px > 110) {
          flying = false;
          ball.visible = false;
        }
        if (flying && trailCount < MAX_TRAIL) {
          trailPts.push({ x: px, y: py, z: 0 });
          trailCount++;
        }
      }

      if (flying) {
        ball.position.set(px, py, 0);
      }

      // Update trail
      const pos = trailGeo.attributes.position.array;
      const n = Math.min(trailPts.length, MAX_TRAIL);
      for (let i = 0; i < n; i++) {
        pos[i * 3] = trailPts[i].x;
        pos[i * 3 + 1] = trailPts[i].y;
        pos[i * 3 + 2] = trailPts[i].z || 0;
      }
      trailGeo.setDrawRange(0, n);
      trailGeo.attributes.position.needsUpdate = true;
    }

    // Show ideal range hint
    const rad = (angle * Math.PI) / 180;
    const ideal = (speed * speed * Math.sin(2 * rad)) / g;
    if (!flying) {
      rangeOut.set(`— (ideal: ${ideal.toFixed(1)} m)`);
    }
  });

  engine.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
