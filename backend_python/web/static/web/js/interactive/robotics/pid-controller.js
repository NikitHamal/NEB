/**
 * PID controller in 3D — a 1 kg carriage on a linear guide, pulled by a toothed belt from a
 * stepper-style motor, must hold the setpoint. The controller samples at 50 Hz like a real
 * microcontroller: u = Kp·e + Ki·∫e dt + Kd·de/dt (derivative taken on the measurement, integral
 * clamped against wind-up), and the motor force saturates at ±20 N. Drag the target flag for a
 * step, grab the carriage and let go for a disturbance, or switch on the fan for a steady push that
 * only the I term can cancel. Overshoot, settling time and steady-state error are measured.
 */
import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { workshop, RM, shadows } from '../core/robot-kit.js';
import { planeDrag, canvasCard, makeArrow } from '../space/space3d/kit.js';

const MASS = 1, FRICTION = 0.4, FMAX = 20, DT_CTRL = 0.02, WIND = 6;
const U = 2;                 // world units per metre
const LIM = 2.6;             // travel, metres either side of centre
const RAIL_Y = 1.0;
const SPAN = 10;             // seconds shown on the graphs

function rulerTexture() {
  const c = document.createElement('canvas'); c.width = 2048; c.height = 64; const g = c.getContext('2d');
  g.fillStyle = '#f1f5f9'; g.fillRect(0, 0, 2048, 64);
  g.fillStyle = '#0f172a'; g.font = '700 26px Poppins, system-ui, sans-serif'; g.textAlign = 'center';
  for (let cm = -280; cm <= 280; cm += 5) {
    const x = 1024 + cm / 280 * 1000, major = cm % 50 === 0;
    g.fillRect(x - (major ? 2 : 1), 0, major ? 4 : 2, major ? 30 : cm % 10 === 0 ? 18 : 10);
    if (cm % 100 === 0) g.fillText(`${cm / 100} m`, x, 58);
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}

function beltTexture() {
  const c = document.createElement('canvas'); c.width = 64; c.height = 16; const g = c.getContext('2d');
  g.fillStyle = '#1b1d21'; g.fillRect(0, 0, 64, 16);
  g.fillStyle = '#2c2f35'; for (let i = 0; i < 64; i += 8) g.fillRect(i, 0, 4, 16);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = THREE.RepeatWrapping; t.repeat.set(120, 1);
  return t;
}

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(16, quality.segments || 32);

  camera.position.set(0, 3.4, 9);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 3, maxDistance: 28, target: new THREE.Vector3(-0.4, 1.2, 0) });
  workshop(scene, engine, quality, { radius: 30, tiles: 7, shadowSize: 8 });

  const own = [];   // geometries and materials made here, disposed with the sim
  const mk = (geo, mat, x, y, z, parent = scene) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); parent.add(m); own.push(geo); return m; };

  // the frame: aluminium extrusion on two legs, a steel guide rail on top, a ruler on the front
  const rig = new THREE.Group(); scene.add(rig);
  const len = (LIM * 2 + 0.6) * U;
  mk(new THREE.BoxGeometry(len + 0.6, 0.3, 0.3), RM.alu(), 0, RAIL_Y - 0.15, 0, rig);
  mk(new THREE.BoxGeometry(len, 0.07, 0.14), RM.steel(), 0, RAIL_Y + 0.035, 0, rig);
  for (const s of [-1, 1]) {
    mk(new THREE.BoxGeometry(0.24, RAIL_Y - 0.3, 0.24), RM.alu(), s * (len / 2 - 0.4), (RAIL_Y - 0.3) / 2, 0, rig);
    mk(new THREE.BoxGeometry(0.9, 0.06, 0.9), RM.darkAlu(), s * (len / 2 - 0.4), 0.03, 0, rig);
    mk(new THREE.BoxGeometry(0.16, 0.2, 0.34), RM.matte(0xef4444), s * (LIM * U + 0.75), RAIL_Y + 0.1, 0, rig);  // end stops
  }
  const rulerTex = rulerTexture(); const rulerMat = new THREE.MeshStandardMaterial({ map: rulerTex, roughness: 0.6 });
  own.push(rulerMat, rulerTex);
  const ruler = mk(new THREE.PlaneGeometry(LIM * 2 * U * (1024 / 1000) * (280 / 260), 0.22), rulerMat, 0, RAIL_Y - 0.15, 0.152, rig);
  ruler.receiveShadow = true;

  // belt drive: motor and drive pulley on the right, idler on the left, belt runs behind the rail
  const BZ = -0.3, PR = 0.13, PX = len / 2 + 0.05;
  const motor = new THREE.Group(); motor.position.set(PX, RAIL_Y - 0.13, BZ - 0.35); rig.add(motor);
  mk(new THREE.BoxGeometry(0.5, 0.5, 0.5), RM.matte(0x111318), 0, 0, 0, motor);
  mk(new THREE.BoxGeometry(0.52, 0.5, 0.08), RM.darkAlu(), 0, 0, 0.21, motor);
  mk(new THREE.BoxGeometry(0.52, 0.5, 0.08), RM.darkAlu(), 0, 0, -0.21, motor);
  const pulleys = [];
  for (const s of [-1, 1]) {
    const p = new THREE.Group(); p.position.set(s * PX, RAIL_Y - 0.13, BZ); rig.add(p);
    const body = mk(new THREE.CylinderGeometry(PR, PR, 0.12, 24), RM.steel(), 0, 0, 0, p); body.rotation.x = Math.PI / 2;
    const flange = mk(new THREE.CylinderGeometry(PR * 1.25, PR * 1.25, 0.02, 24), RM.brass(), 0, 0, 0.07, p); flange.rotation.x = Math.PI / 2;
    mk(new THREE.BoxGeometry(0.03, PR * 1.1, 0.02), RM.matte(0x111318), 0, PR * 0.4, 0.085, p);
    pulleys.push(p);
  }
  const beltTex = beltTexture(); const beltMat = new THREE.MeshStandardMaterial({ map: beltTex, roughness: 0.8 });
  const beltBot = beltTex.clone(); beltBot.needsUpdate = true; const beltMatB = new THREE.MeshStandardMaterial({ map: beltBot, roughness: 0.8 });
  own.push(beltTex, beltMat, beltBot, beltMatB);
  mk(new THREE.BoxGeometry(PX * 2, 0.025, 0.1), beltMat, 0, RAIL_Y - 0.13 + PR, BZ, rig);
  mk(new THREE.BoxGeometry(PX * 2, 0.025, 0.1), beltMatB, 0, RAIL_Y - 0.13 - PR, BZ, rig);
  shadows(rig);

  // the carriage: bearing block on the rail, a deck, a shell, and a clamp onto the belt
  const cart = new THREE.Group(); scene.add(cart);
  mk(new THREE.BoxGeometry(0.8, 0.2, 0.36), RM.darkAlu(), 0, RAIL_Y + 0.15, 0, cart);
  mk(new THREE.BoxGeometry(1.1, 0.06, 0.8), RM.alu(), 0, RAIL_Y + 0.28, -0.05, cart);
  const shellMat = new THREE.MeshPhysicalMaterial({ color: 0x334155, roughness: 0.32, clearcoat: 0.6, clearcoatRoughness: 0.2 }); own.push(shellMat);
  mk(new THREE.BoxGeometry(0.8, 0.36, 0.56), shellMat, 0, RAIL_Y + 0.49, 0, cart);
  mk(new THREE.BoxGeometry(0.14, 0.5, 0.1), RM.darkAlu(), 0, RAIL_Y + 0.02, BZ, cart);
  const pointer = mk(new THREE.ConeGeometry(0.06, 0.16, 12), RM.matte(0xef4444), 0, RAIL_Y - 0.0, 0.2, cart);
  pointer.rotation.x = Math.PI;
  shadows(cart);

  // target flag on a post behind the rail
  const flag = new THREE.Group(); scene.add(flag);
  mk(new THREE.CylinderGeometry(0.025, 0.025, 1.9, 10), RM.steel(), 0, RAIL_Y + 0.95, -0.55, flag);
  mk(new THREE.CylinderGeometry(0.16, 0.18, 0.05, 20), RM.darkAlu(), 0, RAIL_Y + 0.02, -0.55, flag);
  const flagShape = new THREE.Shape(); flagShape.moveTo(0, 0); flagShape.lineTo(0.6, -0.17); flagShape.lineTo(0, -0.34);
  const flagMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.55, side: THREE.DoubleSide }); own.push(flagMat);
  mk(new THREE.ShapeGeometry(flagShape), flagMat, 0, RAIL_Y + 1.88, -0.55, flag);
  const laser = mk(new THREE.PlaneGeometry(0.03, 0.55), new THREE.MeshBasicMaterial({ color: 0x3b82f6, transparent: true, opacity: 0.55, depthWrite: false }), 0, RAIL_Y + 0.0, -0.26, flag);
  laser.rotation.x = -Math.PI / 2; own.push(laser.material);
  shadows(flag);
  const flagTop = new THREE.Vector3();

  // a desk fan at the left end for the steady disturbance
  const fan = new THREE.Group(); fan.position.set(-len / 2 - 1.5, 0, 0); scene.add(fan);
  mk(new THREE.CylinderGeometry(0.35, 0.4, 0.08, 24), RM.matte(0xe2e8f0), 0, 0.04, 0, fan);
  mk(new THREE.CylinderGeometry(0.05, 0.05, RAIL_Y + 0.3, 10), RM.steel(), 0, (RAIL_Y + 0.3) / 2, 0, fan);
  const hub = new THREE.Group(); hub.position.set(0.12, RAIL_Y + 0.4, 0); fan.add(hub);
  const cage = mk(new THREE.TorusGeometry(0.55, 0.02, 8, seg), RM.steel(), 0.06, 0, 0, hub); cage.rotation.y = Math.PI / 2;
  const blades = new THREE.Group(); hub.add(blades);
  const bladeMat = new THREE.MeshStandardMaterial({ color: 0x7dd3fc, roughness: 0.3, transparent: true, opacity: 0.85 }); own.push(bladeMat);
  const bladeGeo = new THREE.BoxGeometry(0.02, 0.45, 0.16); own.push(bladeGeo);
  for (let i = 0; i < 4; i++) { const piv = new THREE.Group(); piv.rotation.x = i * Math.PI / 2; blades.add(piv); const b = new THREE.Mesh(bladeGeo, bladeMat); b.position.y = 0.24; b.rotation.y = 0.5; piv.add(b); }
  mk(new THREE.SphereGeometry(0.09, 16, 10), RM.matte(0xe2e8f0), 0.02, 0, 0, hub);
  mk(new THREE.BoxGeometry(0.35, 0.4, 0.35), RM.matte(0xe2e8f0), -0.2, 0, 0, hub);
  shadows(fan);
  // wind streaks
  const NW = 24, wPos = new Float32Array(NW * 6), wSeed = new Float32Array(NW * 3);
  for (let i = 0; i < NW; i++) { wSeed[i * 3] = Math.random(); wSeed[i * 3 + 1] = (Math.random() - 0.5) * 0.9; wSeed[i * 3 + 2] = (Math.random() - 0.5) * 0.9; }
  const wGeo = new THREE.BufferGeometry(); wGeo.setAttribute('position', new THREE.BufferAttribute(wPos, 3));
  const wMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.6 }); own.push(wGeo, wMat);
  const streaks = new THREE.LineSegments(wGeo, wMat); streaks.frustumCulled = false; scene.add(streaks);

  const force = makeArrow(0x16a34a, 0.035); scene.add(force.group);
  const forceFrom = new THREE.Vector3(), forceVec = new THREE.Vector3();

  const hud = createHud(stage);
  const badge = hud.badge('Drag the flag to set a new target', '#2563eb');

  let kp = 14, ki = 0, kd = 4, wind = false;
  let x = 0, v = 0, sp = 1.0, integ = 0, prevX = 0, u = 0, uP = 0, uI = 0, uD = 0, ctrlT = 0, simT = 0, held = false;
  let stepT = 0, stepFrom = 0, peak = 0, settle = -1, heldX = 0, heldPrev = 0, fanSpin = 0, fanW = 0;
  const N = 600, tr = new Float32Array(N * 6); let trN = 0, trHead = 0, trTick = 0;

  const panel = createPanel(stage, { title: 'PID tuning' });
  const kpS = panel.slider({ label: 'Kp (proportional)', min: 0, max: 60, step: 0.5, value: kp, format: (q) => q.toFixed(1), onChange: (q) => { kp = q; } });
  const kiS = panel.slider({ label: 'Ki (integral)', min: 0, max: 20, step: 0.1, value: ki, format: (q) => q.toFixed(1), onChange: (q) => { ki = q; integ = 0; } });
  const kdS = panel.slider({ label: 'Kd (derivative)', min: 0, max: 15, step: 0.1, value: kd, format: (q) => q.toFixed(1), onChange: (q) => { kd = q; } });
  panel.chips({ label: 'Try', options: [{ value: 'p', label: 'P only' }, { value: 'hot', label: 'Too much Kp' }, { value: 'pd', label: 'PD' }, { value: 'pid', label: 'PID' }], value: 'pd', onChange: (c) => preset(c) });
  panel.toggle({ label: `Fan pushes the carriage (${WIND} N)`, value: false, onChange: (w) => { wind = w; } });
  const gPos = canvasCard(panel.body, 2.1);
  const gU = canvasCard(panel.body, 2.1);
  const st = panel.stats([{ key: 'os', label: 'Overshoot' }, { key: 'ts', label: 'Settling time (2 %)' }, { key: 'ess', label: 'Error now' }, { key: 'u', label: 'Motor force' }]);
  panel.info('P pushes harder the further away it is (too much: it overshoots and oscillates). D brakes as it approaches (damping). I adds up the error over time and removes the steady offset a constant push leaves behind.');

  function preset(c) {
    const g = { p: [14, 0, 0], hot: [55, 0, 0.5], pd: [14, 0, 4], pid: [14, 6, 4.5] }[c];
    kp = g[0]; ki = g[1]; kd = g[2]; kpS.set(kp); kiS.set(ki); kdS.set(kd); integ = 0; newStep(sp);
  }
  function newStep(target) { stepFrom = x; sp = target; stepT = simT; peak = 0; settle = -1; }

  const drag = planeDrag(engine.canvas, camera, controls, {
    plane: new THREE.Plane(new THREE.Vector3(0, 0, 1), 0),
    handles: () => [{ id: 'flag', pos: flagTop }, { id: 'cart', pos: cart.getWorldPosition(new THREE.Vector3()).setY(RAIL_Y + 0.5) }],
    onDown: (h, p) => { if (h.id === 'cart' && p) { held = true; heldX = x; h.off = p.x / U - x; } },
    onMove: (h, p) => {
      if (h.id === 'flag') newStep(Math.max(-2.4, Math.min(2.4, Math.round(p.x / U * 10) / 10)));
      else heldX = Math.max(-LIM, Math.min(LIM, p.x / U - h.off));
    },
    onUp: (h) => { if (h.id === 'cart') { held = false; newStep(sp); } },
  });

  function plot(card, title, series, yMax, unit) {
    const { g, w, h } = card.ctx();
    const ix = 34, iy = 22, iw = w - 44, ih = h - 40;
    const t1 = Math.max(SPAN, simT), t0 = t1 - SPAN;
    const X = (t) => ix + (t - t0) / SPAN * iw, Y = (q) => iy + ih / 2 - q / yMax * ih / 2;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText(title, 10, 14);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.lineWidth = 1; g.strokeRect(ix, iy, iw, ih);
    g.beginPath(); g.moveTo(ix, Y(0)); g.lineTo(ix + iw, Y(0)); g.stroke();
    g.save(); g.beginPath(); g.rect(ix, iy, iw, ih); g.clip();
    for (const [k, color, dash] of series) {
      g.strokeStyle = color; g.lineWidth = dash ? 1.4 : 2; g.setLineDash(dash ? [5, 4] : []); g.beginPath();
      for (let i = 0; i < trN; i++) { const j = ((trHead - trN + i + N) % N) * 6; const px = X(tr[j]), py = Y(tr[j + k]); if (i) g.lineTo(px, py); else g.moveTo(px, py); }
      g.stroke();
    }
    g.restore(); g.setLineDash([]);
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#8ea0c2'; g.textAlign = 'right';
    g.fillText(`${yMax} ${unit}`, ix - 4, iy + 8); g.fillText(`−${yMax}`, ix - 4, iy + ih); g.textAlign = 'center'; g.fillText('t / s, last 10 s', ix + iw / 2, h - 4);
  }

  // frame the whole rig and fan whenever the screen shape changes
  let fitW = 0;
  const fitT = new THREE.Vector3();
  function fit() {
    const W = stage.clientWidth;
    if (W === fitW || !W) return;
    fitW = W;
    // the docked panel covers ~310 px on the right of wide screens: fit the rig into the rest
    const avail = W > 760 ? W - 310 : W, totalW = 15.2 * W / avail;
    const half = Math.tan(camera.fov * Math.PI / 360);
    controls.setDistance(Math.min(26, Math.max(totalW / 2 / half / camera.aspect, 2.4 / half)));
    controls.setTarget(fitT.set(-0.6 + (W - avail) / 2 / W * totalW, 1.2, 0));
  }

  newStep(1);
  let tick = 0;
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    const n = Math.max(1, Math.ceil(dt / 0.002)), hh = dt / n;
    for (let i = 0; i < n; i++) {
      simT += hh; ctrlT += hh;
      if (ctrlT >= DT_CTRL) {
        ctrlT -= DT_CTRL;
        const e = sp - x;
        integ = Math.max(-FMAX / Math.max(ki, 1e-3), Math.min(FMAX / Math.max(ki, 1e-3), integ + e * DT_CTRL));
        uP = kp * e; uI = ki * integ; uD = -kd * (x - prevX) / DT_CTRL; prevX = x;
        u = Math.max(-FMAX, Math.min(FMAX, uP + uI + uD));
      }
      if (!held) {
        const F = u - FRICTION * v + (wind ? WIND : 0);
        v += F / MASS * hh; x += v * hh;
        if (x < -LIM || x > LIM) { x = Math.max(-LIM, Math.min(LIM, x)); v = 0; }
      }
    }
    if (held) { v = (heldX - heldPrev) / Math.max(dt, 1e-3); x = heldX; }
    heldPrev = x;
    if ((trTick++ & 1) === 0) {
      const j = trHead * 6; tr[j] = simT; tr[j + 1] = x; tr[j + 2] = sp; tr[j + 3] = uP; tr[j + 4] = uI; tr[j + 5] = uD;
      trHead = (trHead + 1) % N; trN = Math.min(N, trN + 1);
    }
    const dist = sp - stepFrom;
    if (Math.abs(dist) > 0.05) {
      const over = (x - stepFrom) / dist;
      if (over > peak) peak = over;
      const inBand = Math.abs(x - sp) <= 0.02 * Math.abs(dist);
      if (inBand && settle < 0) settle = simT - stepT; else if (!inBand) settle = -1;
    }

    // scene
    cart.position.x = x * U;
    shellMat.color.setHex(held ? 0xf97316 : 0x334155);
    flag.position.x = sp * U; flagTop.set(sp * U + 0.25, RAIL_Y + 1.7, -0.55);
    beltTex.offset.x = -x * U / (PX * 2) * 120; beltBot.offset.x = x * U / (PX * 2) * 120;
    pulleys.forEach((p) => { p.rotation.z = -x * U / PR; });
    forceFrom.set(x * U, RAIL_Y + 1.0, 0); forceVec.set(u * 0.06, 0, 0); force.set(forceFrom, forceVec);
    fanW += ((wind ? 28 : 0) - fanW) * (1 - Math.exp(-dt * 1.5)); fanSpin += fanW * dt; blades.rotation.x = fanSpin;
    streaks.visible = fanW > 2;
    if (streaks.visible) {
      const x0 = -len / 2 - 1.2, reach = x * U - 0.4 - x0;
      for (let i = 0; i < NW; i++) {
        wSeed[i * 3] = (wSeed[i * 3] + dt * 0.9) % 1;
        const f = wSeed[i * 3], px = x0 + f * reach, y = RAIL_Y + 0.4 + wSeed[i * 3 + 1] * (1 - f * 0.5), z = wSeed[i * 3 + 2];
        wPos[i * 6] = px; wPos[i * 6 + 1] = y; wPos[i * 6 + 2] = z; wPos[i * 6 + 3] = px + 0.35; wPos[i * 6 + 4] = y; wPos[i * 6 + 5] = z;
      }
      wGeo.attributes.position.needsUpdate = true; wMat.opacity = 0.6 * Math.min(1, fanW / 28);
    }
    fit();
    controls.update(dt);
    if ((tick++ & 1) === 0) {
      plot(gPos, 'Position (blue) and target (dashed)', [[2, '#94a3b8', true], [1, '#60a5fa']], 2.5, 'm');
      plot(gU, 'Motor force: P (red), I (purple), D (green)', [[3, '#f87171'], [4, '#c084fc'], [5, '#4ade80']], FMAX, 'N');
    }
    st.os.set(Math.abs(dist) > 0.05 ? `${(Math.max(0, peak - 1) * 100).toFixed(0)} %` : '—');
    st.ts.set(settle >= 0 ? `${settle.toFixed(2)} s` : 'not yet');
    st.ess.set(`${(sp - x).toFixed(3)} m`); st.u.set(`${u.toFixed(1)} N${Math.abs(u) >= FMAX - 0.01 ? ' (max)' : ''}`);
    badge.set(held ? 'Let go and watch it recover'
      : wind && ki === 0 && Math.abs(sp - x) > 0.05 && settle < 0 && Math.abs(v) < 0.02 ? 'The fan leaves a steady error: add some Ki'
        : peak > 1.3 ? 'Big overshoot: lower Kp or raise Kd'
          : settle >= 0 ? `Settled in ${settle.toFixed(2)} s` : 'Drag the flag to set a new target');
  });
  engine.start();

  stage.__pid = { step: (t) => newStep(t), preset, wind: (w) => { wind = w; }, state: () => ({ x, sp, peak, settle, u, simT }) };
  return {
    dispose() {
      drag.dispose(); force.dispose();
      own.forEach((o) => o.dispose());
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__pid;
    },
  };
}
