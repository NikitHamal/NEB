import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const WORLD = 34;

function makeNoise(seed) {
  const perm = new Uint8Array(512);
  let s = seed;
  for (let i = 0; i < 256; i++) perm[i] = i;
  for (let i = 255; i > 0; i--) {
    s = (s * 16807) % 2147483647;
    const j = s % (i + 1);
    const t = perm[i];
    perm[i] = perm[j];
    perm[j] = t;
  }
  for (let i = 0; i < 256; i++) perm[256 + i] = perm[i];
  function grad(ix, iz) {
    return perm[(perm[ix & 255] + iz) & 255] / 255;
  }
  function smooth(t) { return t * t * (3 - 2 * t); }
  return function (x, z) {
    const ix = Math.floor(x);
    const iz = Math.floor(z);
    const fx = smooth(x - ix);
    const fz = smooth(z - iz);
    const a = grad(ix, iz);
    const b = grad(ix + 1, iz);
    const c = grad(ix, iz + 1);
    const d = grad(ix + 1, iz + 1);
    return a + (b - a) * fx + (c - a) * fz + (a - b - c + d) * fx * fz;
  };
}

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  const noise = makeNoise(1337);
  function terrainHeight(x, z) {
    const u = (x + WORLD) * 0.09;
    const v = (z + WORLD) * 0.09;
    let h = noise(u, v) * 2.4;
    h += noise(u * 2.3 + 7, v * 2.3 + 11) * 0.9;
    h += noise(u * 5.1 + 23, v * 5.1 + 31) * 0.3;
    const edge = Math.max(Math.abs(x), Math.abs(z)) / WORLD;
    return h - 1.8 + Math.max(0, edge - 0.75) * 6;
  }

  camera.position.set(0, 7, -9);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3, maxDistance: 40, maxPolar: Math.PI / 2.05,
  });

  basicLights(scene, { ambient: 0.4, key: 1.4, keyPos: [10, 16, 4] });
  scene.fog = new THREE.Fog(0x1a1018, 30, 95);
  scene.background = new THREE.Color(0x271820);

  const starGeo = new THREE.BufferGeometry();
  const starCount = quality.tier === 'low' ? 200 : 500;
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    const r = 150 + Math.random() * 80;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI * 0.45;
    starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPos[i * 3 + 1] = r * Math.cos(phi);
    starPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xd8c8cc, size: 1.1, sizeAttenuation: false })));

  const res = quality.tier === 'low' ? 48 : quality.tier === 'medium' ? 72 : 110;
  const terrainGeo = new THREE.PlaneGeometry(WORLD * 2, WORLD * 2, res, res);
  terrainGeo.rotateX(-Math.PI / 2);
  const tPos = terrainGeo.attributes.position;
  for (let i = 0; i < tPos.count; i++) {
    tPos.setY(i, terrainHeight(tPos.getX(i), tPos.getZ(i)));
  }
  terrainGeo.computeVertexNormals();
  const terrain = new THREE.Mesh(
    terrainGeo,
    new THREE.MeshStandardMaterial({ color: 0xb05a38, roughness: 0.96, metalness: 0.02, flatShading: quality.tier === 'low' })
  );
  scene.add(terrain);

  const rocks = [];
  const rockMat = new THREE.MeshStandardMaterial({ color: 0x6e3a26, roughness: 0.9, flatShading: true });
  const rockGeo = new THREE.DodecahedronGeometry(1, 0);
  const rockCount = quality.tier === 'low' ? 12 : 22;
  let rs = 4242;
  function rand() { rs = (rs * 16807) % 2147483647; return (rs - 1) / 2147483646; }
  for (let i = 0; i < rockCount; i++) {
    const size = 0.5 + rand() * 1.2;
    let x, z;
    do {
      x = (rand() * 2 - 1) * (WORLD - 4);
      z = (rand() * 2 - 1) * (WORLD - 4);
    } while (Math.hypot(x, z) < 5);
    const rock = new THREE.Mesh(rockGeo, rockMat);
    rock.scale.set(size, size * (0.7 + rand() * 0.5), size);
    rock.position.set(x, terrainHeight(x, z) + size * 0.4, z);
    rock.rotation.set(rand() * 3, rand() * 3, rand() * 3);
    scene.add(rock);
    rocks.push({ x, z, r: size * 1.05 });
  }

  const rover = new THREE.Group();
  const bodyMat = new THREE.MeshStandardMaterial({ color: 0xd8dde6, roughness: 0.5, metalness: 0.45 });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x2a3240, roughness: 0.65, metalness: 0.3 });
  const goldMat = new THREE.MeshStandardMaterial({ color: 0xc9a23f, roughness: 0.4, metalness: 0.6 });

  const chassis = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.5, 2.2), bodyMat);
  chassis.position.y = 0.95;
  rover.add(chassis);
  const deck = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.2, 1.4), goldMat);
  deck.position.y = 1.3;
  rover.add(deck);
  const mastPole = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.9, 10), darkMat);
  mastPole.position.set(0.35, 1.85, 0.8);
  rover.add(mastPole);
  const mastHead = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.18, 0.16), darkMat);
  mastHead.position.set(0.35, 2.32, 0.8);
  rover.add(mastHead);
  const panelMesh = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.05, 1.1), new THREE.MeshStandardMaterial({ color: 0x1d3f73, roughness: 0.35, metalness: 0.5 }));
  panelMesh.position.set(0, 1.45, -0.35);
  rover.add(panelMesh);

  const wheels = [];
  const wheelGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.32, Math.max(14, seg / 3));
  const sideZ = [0.95, 0, -0.95];
  [-0.95, 0.95].forEach((x) => {
    sideZ.forEach((z) => {
      const arm = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.55, 0.12), darkMat);
      arm.position.set(x * 0.82, 0.75, z);
      rover.add(arm);
      const w = new THREE.Mesh(wheelGeo, darkMat);
      w.rotation.z = Math.PI / 2;
      w.position.set(x, 0.42, z);
      rover.add(w);
      wheels.push(w);
    });
  });
  scene.add(rover);

  const hud = createHud(stage);
  const tiltBadge = hud.badge('Tilt 0°', '#35d07f');
  const speedBadge = hud.badge('0.0 m/s', '#0EA5E9');

  const panel = createPanel(stage, { title: 'Rover Mission', startCollapsed: true });
  let followCam = true;
  panel.toggle({ label: 'Camera follows rover', value: true, onChange: (v) => { followCam = v; } });
  panel.button({
    label: 'Reset rover', icon: 'restart_alt', variant: 'ghost',
    onClick: () => { state.x = 0; state.z = 0; state.heading = 0; state.speed = 0; },
  });
  panel.info('Drive with the D-pad or arrow keys. Watch the tilt readout — real Mars rovers refuse commands that would tip them past safe limits.');
  panel.info('Real rovers drive themselves: radio signals take 4-24 minutes to reach Mars, so engineers send goals, not joystick commands.');

  const keys = { up: false, down: false, left: false, right: false };

  const dpad = document.createElement('div');
  dpad.className = 'ix-dpad';
  const dirs = [
    { key: 'up', icon: 'keyboard_arrow_up', cls: 'ix-dpad-up' },
    { key: 'left', icon: 'keyboard_arrow_left', cls: 'ix-dpad-left' },
    { key: 'right', icon: 'keyboard_arrow_right', cls: 'ix-dpad-right' },
    { key: 'down', icon: 'keyboard_arrow_down', cls: 'ix-dpad-down' },
  ];
  dirs.forEach((d) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ix-dpad-btn ' + d.cls;
    btn.setAttribute('aria-label', d.key);
    btn.innerHTML = '<span class="material-symbols-outlined">' + d.icon + '</span>';
    btn.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      btn.setPointerCapture && btn.setPointerCapture(e.pointerId);
      keys[d.key] = true;
      btn.classList.add('active');
    });
    const release = () => { keys[d.key] = false; btn.classList.remove('active'); };
    btn.addEventListener('pointerup', release);
    btn.addEventListener('pointercancel', release);
    btn.addEventListener('contextmenu', (e) => e.preventDefault());
    dpad.appendChild(btn);
  });
  stage.appendChild(dpad);

  let stageInView = false;
  const viewObserver = new IntersectionObserver((entries) => {
    stageInView = entries[0] ? entries[0].isIntersecting : false;
  }, { threshold: 0.01 });
  viewObserver.observe(stage);

  function onKey(e, down) {
    if (!stageInView) return;
    if (e.target && e.target.closest && e.target.closest('input,textarea,select,[contenteditable]')) return;
    const map = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', w: 'up', s: 'down', a: 'left', d: 'right' };
    const k = map[e.key];
    if (k) {
      keys[k] = down;
      e.preventDefault();
    }
  }
  const keyDown = (e) => onKey(e, true);
  const keyUp = (e) => onKey(e, false);
  window.addEventListener('keydown', keyDown);
  window.addEventListener('keyup', keyUp);

  const state = { x: 0, z: 0, heading: 0, speed: 0 };
  const camTarget = new THREE.Vector3();
  const fwd = new THREE.Vector3();
  const right = new THREE.Vector3();
  const up = new THREE.Vector3();
  const quat = new THREE.Quaternion();
  const mat3 = new THREE.Matrix4();

  engine.setUpdate((dt) => {
    const accel = 6;
    const maxSpeed = 4.2;
    if (keys.up) state.speed = Math.min(maxSpeed, state.speed + accel * dt);
    else if (keys.down) state.speed = Math.max(-maxSpeed * 0.6, state.speed - accel * dt);
    else state.speed *= Math.max(0, 1 - dt * 3.2);
    if (keys.left) state.heading += dt * 1.7;
    if (keys.right) state.heading -= dt * 1.7;

    const dirX = Math.sin(state.heading);
    const dirZ = Math.cos(state.heading);
    let nx = state.x + dirX * state.speed * dt;
    let nz = state.z + dirZ * state.speed * dt;
    const lim = WORLD - 2.5;
    nx = Math.max(-lim, Math.min(lim, nx));
    nz = Math.max(-lim, Math.min(lim, nz));
    for (const rock of rocks) {
      const dx = nx - rock.x;
      const dz = nz - rock.z;
      const d = Math.hypot(dx, dz);
      const minD = rock.r + 1.1;
      if (d < minD && d > 0.0001) {
        nx = rock.x + (dx / d) * minD;
        nz = rock.z + (dz / d) * minD;
        state.speed *= 0.4;
      }
    }
    state.x = nx;
    state.z = nz;

    const hC = terrainHeight(state.x, state.z);
    const probe = 1.0;
    const hF = terrainHeight(state.x + dirX * probe, state.z + dirZ * probe);
    const hB = terrainHeight(state.x - dirX * probe, state.z - dirZ * probe);
    const hR = terrainHeight(state.x + dirZ * probe, state.z - dirX * probe);
    const hL = terrainHeight(state.x - dirZ * probe, state.z + dirX * probe);
    const pitch = Math.atan2(hB - hF, probe * 2);
    const roll = Math.atan2(hR - hL, probe * 2);

    fwd.set(dirX, (hF - hB) / (probe * 2), dirZ).normalize();
    right.set(dirZ, (hR - hL) / (probe * 2), -dirX).normalize();
    up.crossVectors(fwd, right).normalize();
    if (up.y < 0) up.negate();
    right.crossVectors(up, fwd).normalize();
    mat3.makeBasis(right, up, fwd);
    quat.setFromRotationMatrix(mat3);
    rover.quaternion.slerp(quat, Math.min(dt * 8, 1));
    rover.position.set(state.x, hC, state.z);

    const wheelSpin = (state.speed / 0.42) * dt;
    wheels.forEach((w) => { w.rotation.x += wheelSpin; });

    const tiltDeg = Math.max(Math.abs(pitch), Math.abs(roll)) * 180 / Math.PI;
    tiltBadge.set(tiltDeg > 24 ? '⚠ Tilt ' + tiltDeg.toFixed(0) + '° — DANGER' : 'Tilt ' + tiltDeg.toFixed(0) + '°');
    tiltBadge.el.style.setProperty('--ix-hud-color', tiltDeg > 24 ? '#e2484d' : tiltDeg > 15 ? '#f5b942' : '#35d07f');
    speedBadge.set(Math.abs(state.speed).toFixed(1) + ' m/s');

    if (followCam) {
      camTarget.set(state.x, hC + 1.2, state.z);
      controls.setTarget(camTarget);
    }
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      viewObserver.disconnect();
      window.removeEventListener('keydown', keyDown);
      window.removeEventListener('keyup', keyUp);
      dpad.remove();
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
