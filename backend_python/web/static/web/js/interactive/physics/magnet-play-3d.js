import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const K_CLIP = 90000;
const K_MAG = 260000;
const SOFT = 900;
const N_CLIPS = 10;
const MAG_LEN = 2.2;
const HALF = MAG_LEN / 2 - 0.3;

export default function init(stage, opts) {
  const engine = createEngine(stage, {});
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 6, 12);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 25,
    target: new THREE.Vector3(0, 0, 0),
  });
  controls.setTarget(new THREE.Vector3(0, 0, 0));

  basicLights(scene, { ambient: 0.5, key: 1.4 });
  scene.background = new THREE.Color(0x0b1c30);

  // Floor
  const floorMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 16),
    new THREE.MeshStandardMaterial({ color: 0x0f1f30, roughness: 0.9 })
  );
  floorMesh.rotation.x = -Math.PI / 2;
  floorMesh.position.y = -0.5;
  scene.add(floorMesh);

  // Magnet factory: returns group with north (red) and south (blue) halves
  function makeMagnet(flip) {
    const grp = new THREE.Group();
    const halfGeo = new THREE.BoxGeometry(MAG_LEN / 2, 0.45, 0.45);
    const nMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.5, metalness: 0.2 });
    const sMat = new THREE.MeshStandardMaterial({ color: 0x3b82f6, roughness: 0.5, metalness: 0.2 });
    const leftHalf = new THREE.Mesh(halfGeo, flip < 0 ? nMat : sMat);
    leftHalf.position.x = -MAG_LEN / 4;
    grp.add(leftHalf);
    const rightHalf = new THREE.Mesh(halfGeo, flip < 0 ? sMat : nMat);
    rightHalf.position.x = MAG_LEN / 4;
    grp.add(rightHalf);
    // Pole labels
    const nlbl = makeLabelSprite(flip < 0 ? 'N' : 'S', { scale: 0.6, fontSize: 28 });
    nlbl.position.set(-MAG_LEN / 4, 0.42, 0);
    grp.add(nlbl);
    const slbl = makeLabelSprite(flip < 0 ? 'S' : 'N', { scale: 0.6, fontSize: 28 });
    slbl.position.set(MAG_LEN / 4, 0.42, 0);
    grp.add(slbl);
    grp._flip = flip;
    grp._nHalf = leftHalf;
    grp._sHalf = rightHalf;
    grp._nlbl = nlbl;
    grp._slbl = slbl;
    return grp;
  }

  function updateMagnetColors(grp) {
    const nColor = 0xef4444, sColor = 0x3b82f6;
    grp._nHalf.material.color.setHex(grp._flip < 0 ? nColor : sColor);
    grp._sHalf.material.color.setHex(grp._flip < 0 ? sColor : nColor);
    const ns = makeLabelSprite(grp._flip < 0 ? 'N' : 'S', { scale: 0.6, fontSize: 28 });
    grp._nlbl.material.map.dispose(); grp._nlbl.material = ns.material; grp._nlbl.scale.copy(ns.scale); scene.remove(ns);
    const ss = makeLabelSprite(grp._flip < 0 ? 'S' : 'N', { scale: 0.6, fontSize: 28 });
    grp._slbl.material.map.dispose(); grp._slbl.material = ss.material; grp._slbl.scale.copy(ss.scale); scene.remove(ss);
  }

  const mag1 = makeMagnet(1);
  mag1.position.set(-3, 0, 0);
  scene.add(mag1);

  const mag2 = makeMagnet(1);
  mag2.position.set(3, 0, 0);
  scene.add(mag2);

  // Fixed label
  const fixedLabel = makeLabelSprite('fixed', { scale: 0.7, fontSize: 26, bg: 'rgba(90,110,140,0.8)' });
  fixedLabel.position.set(3, 0.7, 0);
  scene.add(fixedLabel);

  // Paperclips
  const clips = [];
  const clipMeshes = [];
  const clipMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.7, roughness: 0.4 });
  for (let i = 0; i < N_CLIPS; i++) {
    const cx = (Math.random() - 0.5) * 14;
    const cz = (Math.random() - 0.5) * 8;
    clips.push({ x: cx, y: 0, z: cz, vx: 0, vy: 0, vz: 0, rot: Math.random() * Math.PI });
    const cm = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.5, 8), clipMat);
    cm.position.set(cx, 0, cz);
    scene.add(cm);
    clipMeshes.push(cm);
  }

  // Field lines (visible arc curves, rebuilt on demand)
  const fieldLines = [];
  let showField = true;

  function buildFieldLines() {
    fieldLines.forEach((l) => scene.remove(l));
    fieldLines.length = 0;
    if (!showField) return;
    [[mag1, 0xc084fc], [mag2, 0x6366f1]].forEach(([mag, col]) => {
      for (let i = 1; i <= 3; i++) {
        const bulge = i * 0.8 + 0.6;
        const nPoleX = mag.position.x + mag._flip * HALF;
        const sPoleX = mag.position.x - mag._flip * HALF;
        const arcPts = [];
        const SEGS = 30;
        for (let j = 0; j <= SEGS; j++) {
          const t2 = j / SEGS;
          const x = nPoleX + (sPoleX - nPoleX) * t2;
          const y = Math.sin(t2 * Math.PI) * bulge;
          arcPts.push(new THREE.Vector3(x, y, mag.position.z));
        }
        const geo = new THREE.BufferGeometry().setFromPoints(arcPts);
        const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: 0.35 }));
        scene.add(line);
        fieldLines.push(line);
        // Bottom arc
        const arcPts2 = arcPts.map((p) => new THREE.Vector3(p.x, -p.y, p.z));
        const geo2 = new THREE.BufferGeometry().setFromPoints(arcPts2);
        const line2 = new THREE.Line(geo2, new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: 0.35 }));
        scene.add(line2);
        fieldLines.push(line2);
      }
    });
  }
  buildFieldLines();

  // Physics state
  const mag1State = { x: -3, y: 0, z: 0, vx: 0, vy: 0, vz: 0, flip: 1 };
  const mag2State = { x: 3, y: 0, z: 0, flip: 1 };

  function poleX(state, sign) { return state.x + sign * state.flip * HALF; }

  function poleForce(px, pz, polX, polZ, k) {
    const dx = polX - px;
    const dz = polZ - pz;
    const d2 = dx * dx + dz * dz + SOFT;
    const f = k / d2;
    const d = Math.sqrt(d2);
    return { fx: (dx / d) * f, fz: (dz / d) * f };
  }

  // Drag via raycasting
  let dragging = false;
  const dragPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  const dragOffset = new THREE.Vector3();

  function onPointerDown(e) {
    const rect = engine.canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const hit = raycaster.intersectObject(mag1, true);
    if (hit.length > 0) {
      dragging = true;
      const pt = new THREE.Vector3();
      raycaster.ray.intersectPlane(dragPlane, pt);
      dragOffset.set(mag1State.x - pt.x, 0, mag1State.z - pt.z);
      mag1State.vx = 0; mag1State.vz = 0;
      e.preventDefault();
    }
  }
  function onPointerMove(e) {
    if (!dragging) return;
    const rect = engine.canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const pt = new THREE.Vector3();
    raycaster.ray.intersectPlane(dragPlane, pt);
    if (pt) {
      mag1State.x = pt.x + dragOffset.x;
      mag1State.z = pt.z + dragOffset.z;
    }
  }
  function onPointerUp() { dragging = false; }
  engine.canvas.addEventListener('pointerdown', onPointerDown);
  engine.canvas.addEventListener('pointermove', onPointerMove);
  engine.canvas.addEventListener('pointerup', onPointerUp);
  engine.canvas.addEventListener('pointercancel', onPointerUp);

  // Panel
  const panel = createPanel(stage, { title: 'Magnets 3D' });
  panel.button({
    label: 'Flip polarity', icon: 'swap_horiz',
    onClick: () => { mag1State.flip *= -1; mag1._flip = mag1State.flip; updateMagnetColors(mag1); buildFieldLines(); },
  });
  panel.toggle({
    label: 'Field hints', value: true,
    onChange: (v) => { showField = v; buildFieldLines(); },
  });
  panel.divider();
  const stateOut = panel.readout({ label: 'Magnets', value: '—' });
  panel.button({
    label: 'Scatter clips', icon: 'replay',
    onClick: () => {
      clips.forEach((c, i) => {
        c.x = (Math.random() - 0.5) * 14;
        c.z = (Math.random() - 0.5) * 8;
        c.vx = 0; c.vz = 0;
      });
    },
  });
  panel.info('Drag the loose magnet (left one) near the paperclips or the fixed magnet. Flip its poles and see attraction turn to repulsion!');

  const hud = createHud(stage);
  const badge = hud.badge('Drag the loose magnet!', '#F59E0B');

  engine.setUpdate((dt) => {
    controls.update(dt);
    const ddt = Math.min(dt, 0.05);

    // Paperclip physics
    for (let i = 0; i < N_CLIPS; i++) {
      const c = clips[i];
      let fx = 0, fz = 0;
      for (const s of [-1, 1]) {
        const { fx: f1x, fz: f1z } = poleForce(c.x, c.z, poleX(mag1State, s), mag1State.z, K_CLIP);
        fx += f1x; fz += f1z;
        const { fx: f2x, fz: f2z } = poleForce(c.x, c.z, poleX(mag2State, s), mag2State.z, K_CLIP);
        fx += f2x; fz += f2z;
      }
      c.vx = (c.vx + fx * ddt) * 0.9;
      c.vz = (c.vz + fz * ddt) * 0.9;
      c.x += c.vx * ddt;
      c.z += c.vz * ddt;
      c.x = Math.max(-9, Math.min(9, c.x));
      c.z = Math.max(-6, Math.min(6, c.z));
      const sp2 = c.vx * c.vx + c.vz * c.vz;
      if (sp2 > 0.01) c.rot = Math.atan2(c.vz, c.vx);
      clipMeshes[i].position.set(c.x, 0, c.z);
      clipMeshes[i].rotation.y = c.rot;
    }

    // Mag1 physics when not dragging
    if (!dragging) {
      let fx = 0, fz = 0;
      for (const s1 of [-1, 1]) {
        for (const s2 of [-1, 1]) {
          const sign = -(s1 * mag1State.flip) * (s2 * mag2State.flip);
          const { fx: pfx, fz: pfz } = poleForce(poleX(mag1State, s1), mag1State.z, poleX(mag2State, s2), mag2State.z, K_MAG);
          fx += sign * pfx;
          fz += sign * pfz;
        }
      }
      mag1State.vx = (mag1State.vx + fx * ddt) * 0.88;
      mag1State.vz = (mag1State.vz + fz * ddt) * 0.88;
      mag1State.x += mag1State.vx * ddt;
      mag1State.z += mag1State.vz * ddt;
      mag1State.x = Math.max(-8, Math.min(8, mag1State.x));
      mag1State.z = Math.max(-5, Math.min(5, mag1State.z));
      // Collision repulsion between magnets
      const dx = mag1State.x - mag2State.x;
      const dz = mag1State.z - mag2State.z;
      if (Math.hypot(dx, dz) < MAG_LEN + 0.1) {
        mag1State.vx = 0; mag1State.vz = 0;
        const d = Math.hypot(dx, dz) || 1;
        mag1State.x = mag2State.x + (dx / d) * (MAG_LEN + 0.15);
        mag1State.z = mag2State.z + (dz / d) * (MAG_LEN + 0.15);
      }
    }

    // Sync mesh positions
    mag1.position.set(mag1State.x, 0, mag1State.z);
    mag2.position.set(mag2State.x, 0, mag2State.z);

    // Determine attract/repel
    const facingS1 = mag1State.x < mag2State.x ? mag1State.flip : -mag1State.flip;
    const facingS2 = mag1State.x < mag2State.x ? -mag2State.flip : mag2State.flip;
    const attract = facingS1 !== facingS2;
    stateOut.set(attract ? 'Pulling together' : 'Pushing apart');
    badge.set(dragging ? 'Carrying the magnet…' : attract ? 'Opposite poles attract!' : 'Same poles repel!');
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onPointerDown);
      engine.canvas.removeEventListener('pointermove', onPointerMove);
      engine.canvas.removeEventListener('pointerup', onPointerUp);
      engine.canvas.removeEventListener('pointercancel', onPointerUp);
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
