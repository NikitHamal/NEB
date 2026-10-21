/**
 * Line follower — a two-wheeled robot with infrared reflectance sensors on a taped track in a
 * workshop. Each sensor reads how much of its footprint covers the black tape (the overlap of
 * a disc with the tape strip, from the exact distance to the track), and the robot steers by a
 * rule: bang-bang with two sensors (left sees the line → slow the left wheel) or proportional
 * steering with three. Wheel speeds lag behind their commands like real motors, so too much
 * speed makes it overshoot and lose the line. Draw your own track on the floor, or drag the robot.
 * One world unit is 10 cm.
 */
import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { workshop, miniBot, RM } from '../core/robot-kit.js';
import { planeDrag } from '../space/space3d/kit.js';

const TAPE = 0.5;            // 5 cm tape
const FOOT = 0.11;           // sensor footprint radius
const FX = 0.74;             // sensor bar ahead of the axle
const SX = [0.3, 0, -0.3];   // left, middle, right (robot's left is local +x)
const WIDTH = 0.72, AXLE = WIDTH + 0.24;
const TRAIL = 360;

function trackPoints(shape, n = 400) {
  const p = new Float32Array(n * 2), rx = 6.6, rz = 4.4;
  for (let i = 0; i < n; i++) {
    const t = i / n * Math.PI * 2;
    let x, z;
    if (shape === 'eight') { x = rx * Math.sin(t); z = rz * Math.sin(t) * Math.cos(t) * 1.7; }
    else if (shape === 'wavy') { const r = 1 + 0.16 * Math.sin(5 * t); x = rx * r * Math.cos(t); z = rz * r * Math.sin(t); }
    else { x = rx * Math.cos(t); z = rz * Math.sin(t); }
    p[i * 2] = x; p[i * 2 + 1] = z;
  }
  return p;
}

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;

  camera.position.set(1.4, 8.2, 9.8);
  const HOME = new THREE.Vector3(1.4, 0, 0.6);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 3, maxDistance: 26, target: HOME.clone() });
  workshop(scene, engine, quality, { radius: 30, tiles: 7, shadowSize: 9 });

  // the tape: a flat vinyl ribbon with mitred joints, a hair above the floor
  const tapeMat = new THREE.MeshStandardMaterial({ color: 0x15171b, roughness: 0.42, metalness: 0, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
  const tape = new THREE.Mesh(new THREE.BufferGeometry(), tapeMat);
  tape.receiveShadow = true; scene.add(tape);

  // start line: a strip of white tape across the track
  const startMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.5, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 });
  const start = new THREE.Mesh(new THREE.PlaneGeometry(0.12, TAPE * 1.5), startMat);
  start.rotation.x = -Math.PI / 2; start.receiveShadow = true; scene.add(start);

  // the robot, slimmed to a classroom line-follower, with a sensor bar on its nose
  const B = miniBot({ color: 0x2563eb, width: WIDTH, length: 1.0, wheelR: 0.26 });
  const robot = B.group; scene.add(robot);
  const barMat = RM.pcb();
  const bar = new THREE.Mesh(new THREE.BoxGeometry(0.86, 0.025, 0.16), barMat);
  bar.position.set(0, 0.14, FX); bar.castShadow = true; robot.add(bar);
  const arm = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.03, 0.3), RM.alu()); arm.position.set(0, 0.24, FX - 0.15); arm.rotation.x = 0.55; robot.add(arm);
  const offMat = new THREE.MeshStandardMaterial({ color: 0x3f1515, roughness: 0.4 });
  const onMat = RM.glow(0xff3b30, 2.4);
  const eyes = SX.map((x) => {
    const g = new THREE.Group(); g.position.set(x, 0.1, FX); robot.add(g);
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.05, 0.07), RM.matte(0x0f172a)); g.add(body);
    for (const dz of [-0.02, 0.02]) {
      const d = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.03, 12), RM.glassDark()); d.position.set(0, -0.035, dz); g.add(d);
    }
    const led = new THREE.Mesh(new THREE.SphereGeometry(0.018, 10, 8), offMat); led.position.set(0.04, 0.045, 0); g.add(led);
    return { g, led };
  });
  // where each sensor looks: a faint disc on the floor the size of its footprint
  const spotGeo = new THREE.CircleGeometry(FOOT, 24);
  const spots = SX.map(() => {
    const m = new THREE.Mesh(spotGeo, new THREE.MeshBasicMaterial({ color: 0xff5a4f, transparent: true, opacity: 0.25, depthWrite: false }));
    m.rotation.x = -Math.PI / 2; m.renderOrder = 2; scene.add(m); return m;
  });

  // the path driven so far: a thin fading ribbon on the floor
  const tPos = new Float32Array(TRAIL * 2 * 3), tA = new Float32Array(TRAIL * 2);
  const tGeo = new THREE.BufferGeometry();
  tGeo.setAttribute('position', new THREE.BufferAttribute(tPos, 3));
  tGeo.setAttribute('alpha', new THREE.BufferAttribute(tA, 1));
  const tIdx = []; for (let i = 0; i < TRAIL - 1; i++) { const a = i * 2; tIdx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
  tGeo.setIndex(tIdx); tGeo.setDrawRange(0, 0);
  const trailMat = new THREE.ShaderMaterial({
    uniforms: { uC: { value: new THREE.Color(0xf97316) } },
    vertexShader: 'attribute float alpha; varying float vA; void main() { vA = alpha; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform vec3 uC; varying float vA; void main() { gl_FragColor = vec4(uC, vA * 0.85); }',
    transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -6, polygonOffsetUnits: -6,
  });
  const trailMesh = new THREE.Mesh(tGeo, trailMat); trailMesh.frustumCulled = false; trailMesh.renderOrder = 1; scene.add(trailMesh);
  const tx = [];
  function trailClear() { tx.length = 0; tGeo.setDrawRange(0, 0); }
  function trailPush(x, z, a) {
    tx.push(x, z, a); if (tx.length > TRAIL * 3) tx.splice(0, 3);
    const n = tx.length / 3, w = 0.03;
    for (let i = 0; i < n; i++) {
      const px = tx[i * 3], pz = tx[i * 3 + 1], h = tx[i * 3 + 2], cx = Math.cos(h) * w, sz = -Math.sin(h) * w;
      const k = i * 6; tPos[k] = px + cx; tPos[k + 1] = 0.006; tPos[k + 2] = pz + sz; tPos[k + 3] = px - cx; tPos[k + 4] = 0.006; tPos[k + 5] = pz - sz;
      tA[i * 2] = tA[i * 2 + 1] = Math.pow(i / Math.max(1, n - 1), 1.4);
    }
    tGeo.attributes.position.needsUpdate = true; tGeo.attributes.alpha.needsUpdate = true;
    tGeo.setDrawRange(0, Math.max(0, n - 1) * 6);
  }

  // the pen line while drawing a track
  const penGeo = new THREE.BufferGeometry(); const penPos = new Float32Array(3000 * 3);
  penGeo.setAttribute('position', new THREE.BufferAttribute(penPos, 3)); penGeo.setDrawRange(0, 0);
  const penLine = new THREE.Line(penGeo, new THREE.LineBasicMaterial({ color: 0x2563eb })); penLine.frustumCulled = false; scene.add(penLine);

  const hud = createHud(stage);
  const badge = hud.badge('Press Run, or draw a track on the floor', '#3b82f6');

  let follow = false;
  let running = false, speed = 2.5, turn = 70, mode = 'bang', shape = 'oval', pen = false;
  let track = new Float32Array(0), trackN = 0;
  const bot = { x: 0, z: 0, a: 0, vl: 0, vr: 0 };
  const sens = new Float32Array(3);
  let lostT = 0, lapT = 0, lastLap = 0, trailD = 0;
  const drawPts = [];

  const panel = createPanel(stage, { title: 'Line follower' });
  const [runB] = panel.buttonRow([
    { label: 'Run', icon: 'play_arrow', onClick: () => setRun(!running) },
    { label: 'Reset', icon: 'restart_alt', variant: 'ghost', onClick: () => placeBot() },
  ]);
  panel.chips({ label: 'Brain', options: [{ value: 'bang', label: '2 sensors · bang-bang' }, { value: 'prop', label: '3 sensors · proportional' }], value: 'bang', onChange: (v) => { mode = v; } });
  panel.slider({ label: 'Speed', min: 0.5, max: 6, step: 0.1, value: speed, format: (v) => `${Math.round(v * 10)} cm/s`, onChange: (v) => { speed = v; } });
  panel.slider({ label: 'Turn strength', min: 10, max: 140, step: 5, value: turn, format: (v) => `${v} %`, onChange: (v) => { turn = v; } });
  panel.chips({ label: 'Track', options: [{ value: 'oval', label: 'Oval' }, { value: 'wavy', label: 'Wavy' }, { value: 'eight', label: 'Figure 8' }, { value: 'pen', label: 'Draw my own' }], value: 'oval', onChange: (v) => {
    if (v === 'pen') { pen = true; setRun(false); badge.set('Draw a closed loop on the floor with your finger or mouse'); }
    else { pen = false; shape = v; setTrack(trackPoints(v)); placeBot(); }
  } });
  panel.toggle({ label: 'Ride along (camera follows the robot)', value: false, onChange: (v) => {
    follow = v; controls.setDistance(v ? 4.5 : 12.3); if (!v) controls.setTarget(HOME);
  } });
  const st = panel.stats([{ key: 'L', label: 'Left sensor' }, { key: 'R', label: 'Right sensor' }, { key: 'wheels', label: 'Wheels L · R' }, { key: 'lap', label: 'Last lap' }, { key: 'state', label: 'Doing' }]);
  panel.info('Dark tape reflects little infrared light, the white floor reflects a lot. That one reading per sensor is enough: if the left sensor sees the tape, the line is drifting left, so slow the left wheel. Correcting from its own sensors is feedback.');

  function setRun(v) { running = v; runB.setLabel(v ? 'Stop' : 'Run'); }

  function setTrack(p) {
    track = p; trackN = p.length / 2;
    const pos = new Float32Array(trackN * 2 * 3), nrm = new Float32Array(trackN * 2 * 3), uv = new Float32Array(trackN * 2 * 2), idx = [];
    for (let i = 0; i < trackN; i++) {
      const a = (i - 1 + trackN) % trackN, b = (i + 1) % trackN;
      // mitred offset from the averaged tangent so the tape keeps its width through curves
      let ux = p[i * 2] - p[a * 2], uz = p[i * 2 + 1] - p[a * 2 + 1], vx = p[b * 2] - p[i * 2], vz = p[b * 2 + 1] - p[i * 2 + 1];
      const lu = Math.hypot(ux, uz) || 1, lv = Math.hypot(vx, vz) || 1; ux /= lu; uz /= lu; vx /= lv; vz /= lv;
      let tx2 = ux + vx, tz2 = uz + vz; const lt = Math.hypot(tx2, tz2) || 1; tx2 /= lt; tz2 /= lt;
      const m = Math.min(1.6, 1 / Math.max(0.3, tx2 * vx + tz2 * vz)), hw = TAPE / 2 * m;
      const y = 0.004 + 0.0015 * (i / trackN);
      const k = i * 6;
      pos[k] = p[i * 2] - tz2 * hw; pos[k + 1] = y; pos[k + 2] = p[i * 2 + 1] + tx2 * hw;
      pos[k + 3] = p[i * 2] + tz2 * hw; pos[k + 4] = y; pos[k + 5] = p[i * 2 + 1] - tx2 * hw;
      nrm[k + 1] = nrm[k + 4] = 1;
      uv[i * 4] = 0; uv[i * 4 + 1] = i; uv[i * 4 + 2] = 1; uv[i * 4 + 3] = i;
      const c = i * 2, d = b * 2; idx.push(c, d, c + 1, c + 1, d, d + 1);
    }
    tape.geometry.dispose();
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.setAttribute('normal', new THREE.BufferAttribute(nrm, 3));
    g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
    g.setIndex(idx); tape.geometry = g;
    start.position.set(p[0], 0.007, p[1]);
    start.rotation.z = Math.atan2(p[3] - p[1], p[2] - p[0]);
    trailClear();
  }

  function placeBot() {
    if (!trackN) return;
    bot.x = track[0]; bot.z = track[1];
    bot.a = Math.atan2(track[2] - track[0], track[3] - track[1]);
    bot.vl = bot.vr = 0; lostT = 0; lapT = 0; trailClear();
  }

  // fraction of a sensor's footprint disc lying on the tape, from the distance to the centre line
  function dark(x, z) {
    let best = Infinity;
    for (let i = 0; i < trackN; i++) {
      const j = (i + 1) % trackN, ax = track[i * 2], az = track[i * 2 + 1];
      const ex = track[j * 2] - ax, ez = track[j * 2 + 1] - az, px = x - ax, pz = z - az;
      const l2 = ex * ex + ez * ez; const t = l2 > 0 ? Math.max(0, Math.min(1, (px * ex + pz * ez) / l2)) : 0;
      const dx = px - ex * t, dz = pz - ez * t, d2 = dx * dx + dz * dz;
      if (d2 < best) best = d2;
    }
    const d = Math.sqrt(best), u = Math.max(-1, Math.min(1, (TAPE / 2 - d) / FOOT));
    // area of a unit disc's segment beyond a chord at -u, normalised: the straight-edge overlap
    return (Math.asin(u) + u * Math.sqrt(1 - u * u)) / Math.PI + 0.5;
  }
  const SP = [0, 0];
  function sensorPos(i) {
    const s = Math.sin(bot.a), c = Math.cos(bot.a);
    SP[0] = bot.x + s * FX + c * SX[i]; SP[1] = bot.z + c * FX - s * SX[i];
    return SP;
  }

  const drag = planeDrag(engine.canvas, camera, controls, {
    handles: () => (pen ? [] : [{ pos: robot.position }]),
    onDown: () => setRun(false),
    onMove: (h, p) => {
      if (h.empty) { penAdd(p); return; }
      const dx = p.x - bot.x, dz = p.z - bot.z;
      if (Math.hypot(dx, dz) > 0.05) { const want = Math.atan2(dx, dz); bot.a += Math.max(-0.15, Math.min(0.15, Math.atan2(Math.sin(want - bot.a), Math.cos(want - bot.a)))); }
      bot.x = Math.max(-13, Math.min(13, p.x)); bot.z = Math.max(-13, Math.min(13, p.z)); trailClear();
    },
    onUp: (h) => { if (h.empty) finishPen(); },
    onEmpty: (p) => {
      if (!pen) return false;
      drawPts.length = 0; penGeo.setDrawRange(0, 0); penAdd(p); return true;
    },
  });
  function penAdd(p) {
    const n = drawPts.length;
    if (n && (Math.hypot(p.x - drawPts[n - 2], p.z - drawPts[n - 1]) < 0.12 || n >= 6000)) return;
    drawPts.push(p.x, p.z);
    const m = drawPts.length / 2 - 1; penPos[m * 3] = p.x; penPos[m * 3 + 1] = 0.02; penPos[m * 3 + 2] = p.z;
    penGeo.attributes.position.needsUpdate = true; penGeo.setDrawRange(0, m + 1);
  }
  function finishPen() {
    if (drawPts.length > 40) {
      const n = drawPts.length / 2; const p = new Float32Array(drawPts);
      for (let it = 0; it < 3; it++) { const c = new Float32Array(p); for (let i = 0; i < n; i++) { const a = (i - 1 + n) % n, b = (i + 1) % n; p[i * 2] = (c[a * 2] + 2 * c[i * 2] + c[b * 2]) / 4; p[i * 2 + 1] = (c[a * 2 + 1] + 2 * c[i * 2 + 1] + c[b * 2 + 1]) / 4; } }
      setTrack(p); placeBot(); pen = false; badge.set('Your track! Press Run');
    } else badge.set('Too short: draw a bigger loop');
    drawPts.length = 0; penGeo.setDrawRange(0, 0);
  }

  setTrack(trackPoints(shape)); placeBot();

  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    for (let i = 0; i < 3; i++) { sensorPos(i); sens[i] = dark(SP[0], SP[1]); }
    let doing = 'stopped';
    if (running) {
      let cl = speed, cr = speed;
      if (mode === 'bang') {
        const L = sens[0] > 0.4, R = sens[2] > 0.4;
        if (L && !R) { cl = speed * (1 - turn / 100); doing = 'line on the left: turn left'; }
        else if (R && !L) { cr = speed * (1 - turn / 100); doing = 'line on the right: turn right'; }
        else if (!L && !R) doing = 'line between sensors: straight';
        else doing = 'both on the line: straight';
      } else {
        const tot = sens[0] + sens[1] + sens[2];
        const err = tot > 0.05 ? (sens[2] - sens[0]) / tot : 0;
        cl = speed * (1 + err * turn / 100); cr = speed * (1 - err * turn / 100);
        doing = tot < 0.05 ? 'lost: going straight' : `error ${err.toFixed(2)}: steer ${err < -0.05 ? 'left' : err > 0.05 ? 'right' : 'straight'}`;
      }
      // sub-step so a fast robot cannot skip over the tape between sensor readings
      const steps = Math.max(1, Math.ceil(speed * dt / 0.04)), h = dt / steps, f = 1 - Math.exp(-h / 0.12);
      for (let s = 0; s < steps; s++) {
        bot.vl += (cl - bot.vl) * f; bot.vr += (cr - bot.vr) * f;
        const v = (bot.vl + bot.vr) / 2;
        bot.a += (bot.vr - bot.vl) / AXLE * h;
        bot.x += Math.sin(bot.a) * v * h; bot.z += Math.cos(bot.a) * v * h;
        trailD += v * h;
      }
      bot.x = Math.max(-13, Math.min(13, bot.x)); bot.z = Math.max(-13, Math.min(13, bot.z));
      B.wheelR.rotation.x += bot.vl * dt / 0.26; B.wheelL.rotation.x += bot.vr * dt / 0.26;
      lapT += dt;
      if (Math.hypot(bot.x - track[0], bot.z - track[1]) < 0.4 && lapT > 3) { lastLap = lapT; lapT = 0; }
      lostT = sens[0] + sens[1] + sens[2] > 0.1 ? 0 : lostT + dt;
      if (lostT > 1.2) { setRun(false); badge.set('Lost the line! Slow down or turn harder'); }
      if (trailD > 0.06) { trailD = 0; trailPush(bot.x, bot.z, bot.a); }
      badge.set(doing);
    } else {
      bot.vl *= 0.8; bot.vr *= 0.8;
    }
    robot.position.set(bot.x, 0, bot.z); robot.rotation.y = bot.a;
    for (let i = 0; i < 3; i++) {
      const used = mode === 'prop' || i !== 1, on = used && sens[i] > 0.4;
      eyes[i].g.visible = used; spots[i].visible = used;
      eyes[i].led.material = on ? onMat : offMat;
      sensorPos(i); spots[i].position.set(SP[0], 0.009, SP[1]);
      spots[i].material.opacity = on ? 0.5 : 0.22;
    }
    B.led.material = running ? RM.glow(0x22c55e, 2) : RM.glow(0xf59e0b, 1.6);
    st.L.set(sens[0] > 0.4 ? 'ON the line' : 'off'); st.R.set(sens[2] > 0.4 ? 'ON the line' : 'off');
    st.wheels.set(`${Math.round(bot.vl * 10)} · ${Math.round(bot.vr * 10)} cm/s`);
    st.lap.set(lastLap ? `${lastLap.toFixed(2)} s` : '—'); st.state.set(doing);
    if (follow) controls.setTarget(robot.position);
    controls.update(dt);
  });
  engine.start();

  stage.__line = {
    run: () => setRun(true), state: () => ({ x: bot.x, z: bot.z, lost: lostT, lap: lastLap, running, sens: Array.from(sens) }),
    track: (v) => { shape = v; setTrack(trackPoints(v)); placeBot(); },
    set: (o) => { if (o.speed != null) speed = o.speed; if (o.turn != null) turn = o.turn; if (o.mode) mode = o.mode; },
  };

  return {
    dispose() {
      drag.dispose();
      tape.geometry.dispose(); tapeMat.dispose(); start.geometry.dispose(); startMat.dispose();
      bar.geometry.dispose(); arm.geometry.dispose(); offMat.dispose(); spotGeo.dispose(); spots.forEach((s) => s.material.dispose());
      tGeo.dispose(); trailMat.dispose(); penGeo.dispose(); penLine.material.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__line;
    },
  };
}
