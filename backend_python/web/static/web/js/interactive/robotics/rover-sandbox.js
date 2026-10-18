import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { RM, wheel, shadows } from '../core/robot-kit.js';
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

  // Mars by day: a butterscotch sky that pales to the horizon, a small white sun, dust haze
  const skyCol = new THREE.Color(0xc99a72);
  scene.background = skyCol;
  scene.fog = new THREE.Fog(0xd2a47c, 26, 92);
  const sky = new THREE.Mesh(new THREE.SphereGeometry(180, 32, 16), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
    fragmentShader: 'varying vec3 vP; void main(){ float h = clamp(vP.y,0.0,1.0); vec3 zen = vec3(0.47,0.33,0.27); vec3 hor = vec3(0.86,0.66,0.48); vec3 c = mix(hor, zen, pow(h,0.55)); vec3 s = normalize(vec3(0.5,0.62,0.2)); float sun = pow(max(dot(normalize(vP), s),0.0), 900.0); float halo = pow(max(dot(normalize(vP), s),0.0), 18.0)*0.25; gl_FragColor = vec4(c + vec3(0.95,0.97,1.0)*(sun*1.5) + vec3(0.9,0.85,0.8)*halo, 1.0); }',
  }));
  scene.add(sky);
  scene.add(new THREE.HemisphereLight(0xf0d2b4, 0x6b3a28, 0.75));
  const sunL = new THREE.DirectionalLight(0xfff1de, 2.2);
  sunL.position.set(18, 22, 7);
  if (quality.tier !== 'low') {
    engine.renderer.shadowMap.enabled = true; engine.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    sunL.castShadow = true; sunL.shadow.mapSize.set(quality.tier === 'high' ? 2048 : 1024, quality.tier === 'high' ? 2048 : 1024);
    const sc = sunL.shadow.camera; sc.left = -14; sc.right = 14; sc.top = 14; sc.bottom = -14; sc.near = 1; sc.far = 80; sunL.shadow.bias = -0.0006;
  }
  scene.add(sunL); scene.add(sunL.target);

  // regolith: a tiling grain texture, and colour from height and slope (bright dust on flats,
  // darker basalt on slopes)
  const regolith = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
    g.fillStyle = '#c8c4c0'; g.fillRect(0, 0, 512, 512); // neutral grain: the hue comes from the vertex colours
    for (let i = 0; i < 9000; i++) { const v = Math.random(); g.fillStyle = v < 0.5 ? `rgba(60,56,52,${Math.random() * 0.3})` : `rgba(255,250,245,${Math.random() * 0.25})`; const r = Math.random() * 2.4; g.fillRect(Math.random() * 512, Math.random() * 512, r, r); }
    for (let i = 0; i < 60; i++) { g.fillStyle = 'rgba(50,46,42,0.35)'; g.beginPath(); g.arc(Math.random() * 512, Math.random() * 512, 1 + Math.random() * 4, 0, Math.PI * 2); g.fill(); }
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(14, 14); if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  })();
  const res = quality.tier === 'low' ? 64 : quality.tier === 'medium' ? 110 : 170;
  const terrainGeo = new THREE.PlaneGeometry(WORLD * 2, WORLD * 2, res, res);
  terrainGeo.rotateX(-Math.PI / 2);
  const tPos = terrainGeo.attributes.position;
  for (let i = 0; i < tPos.count; i++) tPos.setY(i, terrainHeight(tPos.getX(i), tPos.getZ(i)));
  terrainGeo.computeVertexNormals();
  const nrm = terrainGeo.attributes.normal;
  const cols = new Float32Array(tPos.count * 3);
  const dust = new THREE.Color(0xd8a07a), basalt = new THREE.Color(0x6e4232), tc = new THREE.Color();
  for (let i = 0; i < tPos.count; i++) {
    const slope = 1 - nrm.getY(i);
    const h = tPos.getY(i);
    tc.copy(dust).lerp(basalt, Math.min(1, slope * 4.5 + Math.max(0, -h) * 0.1));
    cols[i * 3] = tc.r; cols[i * 3 + 1] = tc.g; cols[i * 3 + 2] = tc.b;
  }
  terrainGeo.setAttribute('color', new THREE.BufferAttribute(cols, 3));
  const terrain = new THREE.Mesh(terrainGeo, new THREE.MeshStandardMaterial({ map: regolith, vertexColors: true, roughness: 0.97, metalness: 0, bumpMap: regolith, bumpScale: 0.6 }));
  terrain.receiveShadow = true;
  scene.add(terrain);

  // basalt rocks, each a different lumpy shape
  const rocks = [];
  const rockMat = new THREE.MeshStandardMaterial({ color: 0x5c3a2c, roughness: 0.93, map: regolith, bumpMap: regolith, bumpScale: 1.2 });
  const rockCount = quality.tier === 'low' ? 14 : 26;
  let rs = 4242;
  function rand() { rs = (rs * 16807) % 2147483647; return (rs - 1) / 2147483646; }
  const shapes = [];
  for (let k = 0; k < 5; k++) {
    const gg = new THREE.IcosahedronGeometry(1, quality.tier === 'low' ? 1 : 2);
    const p = gg.attributes.position; const v = new THREE.Vector3();
    for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const n = 1 + 0.22 * Math.sin(v.x * 3.1 + k) * Math.cos(v.y * 2.7 + k * 2) + 0.12 * Math.sin(v.z * 5.3 + k); v.multiplyScalar(n); if (v.y < -0.2) v.y = -0.2 + (v.y + 0.2) * 0.3; p.setXYZ(i, v.x, v.y, v.z); }
    gg.computeVertexNormals(); shapes.push(gg);
  }
  for (let i = 0; i < rockCount; i++) {
    const size = 0.5 + rand() * 1.2;
    let x, z;
    do { x = (rand() * 2 - 1) * (WORLD - 4); z = (rand() * 2 - 1) * (WORLD - 4); } while (Math.hypot(x, z) < 5);
    const rock = new THREE.Mesh(shapes[i % shapes.length], rockMat);
    rock.scale.set(size, size * (0.55 + rand() * 0.4), size * (0.8 + rand() * 0.4));
    rock.position.set(x, terrainHeight(x, z) + size * 0.25, z);
    rock.rotation.set(0, rand() * 6, 0);
    rock.castShadow = true; rock.receiveShadow = true;
    scene.add(rock);
    rocks.push({ x, z, r: size * 1.05 });
  }

  // a Curiosity-class rover: rocker-bogie suspension on six aluminium wheels, a white body with
  // gold foil, a mast camera, a high-gain antenna dish, the finned power unit at the back and
  // the robotic arm folded across the front
  const rover = new THREE.Group();
  const white = RM.shell(0xeef0f2);
  const foil = new THREE.MeshStandardMaterial({ color: 0xd4a94a, roughness: 0.35, metalness: 0.9 });
  const darkMat = RM.darkAlu();
  const chassis = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.48, 2.2), white); chassis.position.y = 1.0; rover.add(chassis);
  const deck = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.06, 1.9), foil); deck.position.y = 1.27; rover.add(deck);
  const mastPole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.07, 1.1, 14), white); mastPole.position.set(0.42, 1.85, 0.75); rover.add(mastPole);
  const mastHead = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.22, 0.24), white); mastHead.position.set(0.42, 2.45, 0.75); rover.add(mastHead);
  for (const x of [0.3, 0.54]) { const lens = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.04, 16), RM.glassDark()); lens.rotation.x = Math.PI / 2; lens.position.set(x, 2.45, 0.88); rover.add(lens); }
  const dish = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.3, 0.06, 32), white); dish.position.set(-0.45, 1.5, 0.15); dish.rotation.set(0.5, 0, 0.3); rover.add(dish);
  const rtg = new THREE.Group(); rtg.position.set(0, 1.15, -1.3); rtg.rotation.x = -0.5; rover.add(rtg);
  rtg.add(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.8, 18), darkMat));
  for (let k = 0; k < 8; k++) { const fin = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.7, 0.26), darkMat); const p = new THREE.Group(); p.rotation.y = k * Math.PI / 4; fin.position.z = 0.3; p.add(fin); rtg.add(p); }
  const armA = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 0.9), white); armA.position.set(-0.3, 0.95, 1.35); armA.rotation.y = 0.9; rover.add(armA);
  const turret = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.22, 16), darkMat); turret.position.set(0.1, 0.9, 1.5); rover.add(turret);

  const wheels = [];
  const sideZ = [0.95, 0, -0.95];
  [-1, 1].forEach((side) => {
    // the rocker and bogie beams
    const rocker = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 1.4), white); rocker.position.set(side * 0.95, 0.88, 0.45); rocker.rotation.x = -0.25; rover.add(rocker);
    const bogie = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 1.2), white); bogie.position.set(side * 0.95, 0.7, -0.45); bogie.rotation.x = 0.2; rover.add(bogie);
    sideZ.forEach((z) => {
      const leg = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.45, 0.07), white); leg.position.set(side * 0.95, 0.62, z); rover.add(leg);
      const w = wheel(0.42, 0.34);
      if (side < 0) w.rotation.y = Math.PI;
      const spin = new THREE.Group(); spin.position.set(side * 1.08, 0.42, z); spin.add(w); rover.add(spin);
      wheels.push(spin);
    });
  });
  shadows(rover);
  scene.add(rover);
  sunL.target = rover;

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
    // the sun's shadow frustum follows the rover, so its shadow is always crisp
    sunL.position.set(state.x + 18, hC + 22, state.z + 7);

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
