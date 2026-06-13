import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MASS = 2;
const G = 9.81;
const MU_K = 0.45;
const BOX_SIZE = 0.8;
const WORLD_W = 10;

export default function init(stage, opts) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 5, 10);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 25,
    target: new THREE.Vector3(0, 0.4, 0),
  });
  controls.setTarget(new THREE.Vector3(0, 0.4, 0));

  basicLights(scene, { ambient: 0.5, key: 1.4 });
  scene.background = new THREE.Color(0x0b1c30);

  // Ground / floor
  const floorGeo = new THREE.PlaneGeometry(WORLD_W * 2, 8);
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.9 });
  const floorMesh = new THREE.Mesh(floorGeo, floorMat);
  floorMesh.rotation.x = -Math.PI / 2;
  floorMesh.position.y = 0;
  if (quality.shadows) floorMesh.receiveShadow = true;
  scene.add(floorMesh);
  const gridHelper = new THREE.GridHelper(WORLD_W * 2, 20, 0x1a3a20, 0x1a3a20);
  gridHelper.position.y = 0.005;
  scene.add(gridHelper);

  // Crate mesh (box with friendly face)
  const crateGroup = new THREE.Group();
  scene.add(crateGroup);

  const crateGeo = new THREE.BoxGeometry(BOX_SIZE, BOX_SIZE, BOX_SIZE);
  const crateMat = new THREE.MeshStandardMaterial({ color: 0xF59E0B, roughness: 0.7, metalness: 0.1 });
  const crate = new THREE.Mesh(crateGeo, crateMat);
  crate.position.y = BOX_SIZE / 2;
  if (quality.shadows) { crate.castShadow = true; crate.receiveShadow = true; }
  crateGroup.add(crate);

  // Eyes on the crate
  const eyeMat = new THREE.MeshStandardMaterial({ color: 0x1c1206 });
  [-0.18, 0.18].forEach((ex) => {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 8), eyeMat);
    eye.position.set(ex, 0.12, BOX_SIZE / 2 + 0.01);
    crate.add(eye);
  });

  // Force arrow (ArrowHelper — pink, pointing in push direction)
  const forceArrow = new THREE.ArrowHelper(
    new THREE.Vector3(1, 0, 0),
    new THREE.Vector3(0, BOX_SIZE / 2, 0),
    0.01, 0xfb7185, 0.15, 0.1
  );
  scene.add(forceArrow);

  // Velocity arrow (blue)
  const velArrow = new THREE.ArrowHelper(
    new THREE.Vector3(1, 0, 0),
    new THREE.Vector3(0, BOX_SIZE * 0.9, 0),
    0.01, 0x38bdf8, 0.12, 0.08
  );
  scene.add(velArrow);

  // Friction label
  const fricLabel = makeLabelSprite('friction ON', { scale: 0.9, fontSize: 30 });
  fricLabel.position.set(0, 2, 0);
  scene.add(fricLabel);

  // Push-direction buttons (visual indicators in 3D — small panels on left/right)
  const btnMat = [
    new THREE.MeshStandardMaterial({ color: 0xF59E0B, emissive: 0x7a4f00, emissiveIntensity: 0.2 }),
    new THREE.MeshStandardMaterial({ color: 0xF59E0B, emissive: 0x7a4f00, emissiveIntensity: 0.2 }),
  ];
  const leftBtn = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.1), btnMat[0]);
  leftBtn.position.set(-4.5, 0.4, 0);
  scene.add(leftBtn);
  const rightBtn = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.1), btnMat[1]);
  rightBtn.position.set(4.5, 0.4, 0);
  scene.add(rightBtn);
  const leftLabel = makeLabelSprite('◀', { scale: 0.7, fontSize: 36 });
  leftLabel.position.set(-4.5, 0.4, 0.1);
  scene.add(leftLabel);
  const rightLabel = makeLabelSprite('▶', { scale: 0.7, fontSize: 36 });
  rightLabel.position.set(4.5, 0.4, 0.1);
  scene.add(rightLabel);

  // Keyboard push controls
  let holdDir = 0;
  const keys = new Set();
  function onKeyDown(e) {
    keys.add(e.code);
    if (e.code === 'ArrowLeft' || e.code === 'KeyA') holdDir = -1;
    if (e.code === 'ArrowRight' || e.code === 'KeyD') holdDir = 1;
  }
  function onKeyUp(e) {
    keys.delete(e.code);
    if (!keys.has('ArrowLeft') && !keys.has('KeyA') && !keys.has('ArrowRight') && !keys.has('KeyD')) holdDir = 0;
  }
  window.addEventListener('keydown', onKeyDown);
  window.addEventListener('keyup', onKeyUp);

  // State
  let pushStrength = 20;
  let frictionOn = true;
  let cx = 0;
  let cv = 0;

  function appliedForce() { return holdDir * pushStrength; }

  function step(dt) {
    const F = appliedForce();
    let fric = 0;
    if (frictionOn) {
      const maxFric = MU_K * MASS * G;
      if (Math.abs(cv) > 0.02) fric = -Math.sign(cv) * maxFric;
      else if (Math.abs(F) <= maxFric) { cv = 0; fric = -F; }
      else fric = -Math.sign(F) * maxFric;
    }
    const a = (F + fric) / MASS;
    cv += a * dt;
    cx += cv * dt;
    const maxX = WORLD_W / 2 - BOX_SIZE / 2;
    if (cx < -maxX) { cx = -maxX; cv = Math.abs(cv) * 0.3; }
    if (cx > maxX) { cx = maxX; cv = -Math.abs(cv) * 0.3; }
  }

  function updateFricLabel() {
    const txt = frictionOn ? 'friction ON' : 'friction OFF';
    const ns = makeLabelSprite(txt, { scale: 0.9, fontSize: 30, bg: frictionOn ? 'rgba(34,197,94,0.7)' : 'rgba(239,68,68,0.6)' });
    fricLabel.material.map.dispose();
    fricLabel.material = ns.material;
    fricLabel.scale.copy(ns.scale);
    scene.remove(ns);
  }

  const panel = createPanel(stage, { title: 'Forces 3D' });
  panel.slider({
    label: 'Push strength', min: 5, max: 60, step: 1, value: pushStrength,
    format: (v) => `${v} N`, onChange: (v) => { pushStrength = v; },
  });
  panel.toggle({
    label: 'Friction', value: true,
    onChange: (v) => { frictionOn = v; updateFricLabel(); },
  });
  panel.divider();
  const forceOut = panel.readout({ label: 'Applied force', value: '0 N' });
  const speedOut = panel.readout({ label: 'Speed', value: '0.0 m/s' });
  panel.button({ label: 'Reset crate', icon: 'replay', onClick: () => { cx = 0; cv = 0; holdDir = 0; } });
  panel.info('Use ◀ ▶ arrow keys (or A/D) to push the crate, or click the left/right panels. The pink arrow = force, blue = speed. Turn friction off and watch it glide!');

  const hud = createHud(stage);
  const badge = hud.badge('Push the crate!', '#F59E0B');

  // Mouse click on left/right buttons
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  let mouseHeldDir = 0;
  function onPointerDown(e) {
    const rect = engine.canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObjects([leftBtn, rightBtn]);
    if (hits.length > 0) {
      mouseHeldDir = hits[0].object === leftBtn ? -1 : 1;
      holdDir = mouseHeldDir;
    }
    e.preventDefault();
  }
  function onPointerUp() { mouseHeldDir = 0; if (holdDir === mouseHeldDir || mouseHeldDir === 0) holdDir = 0; }
  engine.canvas.addEventListener('pointerdown', onPointerDown);
  engine.canvas.addEventListener('pointerup', onPointerUp);

  engine.setUpdate((dt) => {
    controls.update(dt);
    step(Math.min(dt, 0.05));

    crateGroup.position.x = cx;

    const F = appliedForce();
    const fLen = Math.abs(F) * 0.04;
    forceArrow.position.set(cx, BOX_SIZE / 2, 0);
    if (fLen > 0.05) {
      forceArrow.setDirection(new THREE.Vector3(Math.sign(F), 0, 0));
      forceArrow.setLength(fLen, Math.min(0.2, fLen * 0.3), Math.min(0.12, fLen * 0.2));
      forceArrow.visible = true;
    } else {
      forceArrow.visible = false;
    }

    const vLen = Math.abs(cv) * 0.15;
    velArrow.position.set(cx, BOX_SIZE * 0.9, 0);
    if (vLen > 0.05) {
      velArrow.setDirection(new THREE.Vector3(Math.sign(cv), 0, 0));
      velArrow.setLength(vLen, Math.min(0.18, vLen * 0.35), Math.min(0.1, vLen * 0.25));
      velArrow.visible = true;
    } else {
      velArrow.visible = false;
    }

    fricLabel.position.set(cx, BOX_SIZE + 0.9, 0);

    forceOut.set(`${Math.abs(F).toFixed(0)} N`);
    speedOut.set(`${Math.abs(cv).toFixed(1)} m/s`);
    badge.set(
      holdDir !== 0 ? 'Pushing!' :
      Math.abs(cv) > 0.1 ? (frictionOn ? 'Friction is slowing it…' : 'Gliding — no friction!') :
      'Push the crate!'
    );
  });

  engine.start();

  return {
    dispose() {
      window.removeEventListener('keydown', onKeyDown);
      window.removeEventListener('keyup', onKeyUp);
      engine.canvas.removeEventListener('pointerdown', onPointerDown);
      engine.canvas.removeEventListener('pointerup', onPointerUp);
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
