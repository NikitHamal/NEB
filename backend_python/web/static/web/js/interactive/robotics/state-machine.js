/**
 * Logic and state machines in 3D — a robot vacuum in a living room, run by a finite state machine.
 * Each state has one job (SEARCH drives and cleans, BACKUP reverses after a bump, TURN picks a new
 * heading, DOCK steers home on a low battery, CHARGE waits on the dock) and events move it between
 * them. The status ring on the robot shows the current state's colour, and the live diagram in the
 * panel lights the state and flashes each transition as it fires. Drag the furniture or the robot,
 * or fire the events yourself. 1 unit = 1 m.
 */
import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { workshop, RM, shadows } from '../core/robot-kit.js';
import { planeDrag, canvasCard } from '../space/space3d/kit.js';
import { label } from '../physics/physics3d/field.js';

const STATES = ['SEARCH', 'BACKUP', 'TURN', 'DOCK', 'CHARGE'];
const SCOL = { SEARCH: '#2563eb', BACKUP: '#f08c00', TURN: '#7c3aed', DOCK: '#0d9488', CHARGE: '#16a34a' };
const EDGES = [
  ['SEARCH', 'BACKUP', 'bump'], ['BACKUP', 'TURN', 'timer done'], ['TURN', 'SEARCH', 'turn done'],
  ['SEARCH', 'DOCK', 'battery low'], ['BACKUP', 'DOCK', 'battery low'], ['TURN', 'DOCK', 'battery low'],
  ['DOCK', 'BACKUP', 'bump'], ['DOCK', 'CHARGE', 'docked'], ['CHARGE', 'SEARCH', 'battery full'],
];
const RW = 5.6, RD = 3.8, X0 = -RW / 2, Z0 = -RD / 2;   // the room
const R = 0.17;                                         // robot radius
// where each transition's label sits: fraction along the arrow and side offset
const LBL = [[0.5, 1.9], [0.3, -1.6], [0.2, -1.9], [0.45, -1.9], [0.45, 1.9], [0.55, 1.9], [0.55, 1.9], [0.5, 1.9], [0.36, -1.2]];
const GX = 40, GZ = 26;                                 // dirt grid
const V = 0.45;                                         // cruising speed, m/s
const DOCK = { x: X0 + RW - 0.36, z: Z0 + RD - 0.4 };
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

function woodTexture() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 1024; const g = c.getContext('2d');
  const tones = ['#b98b5b', '#c49766', '#ad7f52', '#bf9061', '#b48656'];
  const pw = 128;
  for (let x = 0; x < 1024; x += pw) {
    let y = -((x / pw) * 331 % 700);
    while (y < 1024) {
      const L = 520 + ((x * 7 + y * 13) % 300);
      g.fillStyle = tones[Math.abs((x / pw * 3 + Math.round(y / 97)) % tones.length)]; g.fillRect(x, y, pw, L);
      for (let k = 0; k < 22; k++) { g.fillStyle = `rgba(80,50,25,${0.03 + (k % 4) * 0.015})`; g.fillRect(x + ((k * 37) % pw), y, 1 + (k % 3), L); }
      g.fillStyle = 'rgba(60,35,15,0.55)'; g.fillRect(x, y, pw, 2);
      y += L;
    }
    g.fillStyle = 'rgba(60,35,15,0.5)'; g.fillRect(x, 0, 2, 1024);
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(RW / 2.4, RD / 2.4); t.anisotropy = 8;
  return t;
}

function fabric(color) {
  return new THREE.MeshStandardMaterial({ color, roughness: 0.95 });
}

// furniture models built to fill their collision rectangle (w along x, d along z), origin at the centre
function sofa(w, d) {
  const g = new THREE.Group(); const m = fabric(0x8a6a4f); const c = fabric(0x9c7a5c);
  const add = (geo, mat, x, y, z) => { const o = new THREE.Mesh(geo, mat); o.position.set(x, y, z); g.add(o); };
  add(new THREE.BoxGeometry(w, 0.22, d), m, 0, 0.17, 0);
  add(new THREE.BoxGeometry(w, 0.42, 0.16), m, 0, 0.43, -d / 2 + 0.08);
  for (const s of [-1, 1]) add(new THREE.BoxGeometry(0.14, 0.34, d), m, s * (w / 2 - 0.07), 0.36, 0);
  const n = 2, cw = (w - 0.3) / n;
  for (let i = 0; i < n; i++) add(new THREE.BoxGeometry(cw - 0.02, 0.1, d - 0.2), c, -w / 2 + 0.15 + cw * (i + 0.5), 0.33, 0.06);
  for (let i = 0; i < n; i++) { const o = new THREE.Mesh(new THREE.BoxGeometry(cw - 0.06, 0.3, 0.1), c); o.position.set(-w / 2 + 0.15 + cw * (i + 0.5), 0.52, -d / 2 + 0.2); o.rotation.x = -0.18; g.add(o); }
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) add(new THREE.CylinderGeometry(0.025, 0.02, 0.06, 8), RM.darkAlu(), sx * (w / 2 - 0.08), 0.03, sz * (d / 2 - 0.08));
  return shadows(g);
}
function table(w, d) {
  const g = new THREE.Group(); const wood = new THREE.MeshStandardMaterial({ color: 0x5b3a24, roughness: 0.45 });
  const top = new THREE.Mesh(new THREE.BoxGeometry(w, 0.05, d), wood); top.position.y = 0.42; g.add(top);
  const skirt = new THREE.Mesh(new THREE.BoxGeometry(w - 0.04, 0.34, d - 0.04), new THREE.MeshStandardMaterial({ color: 0x6d4930, roughness: 0.55 })); skirt.position.y = 0.21; g.add(skirt);
  const books = [0x2563eb, 0xdc2626, 0xf5f5f4];
  books.forEach((c, i) => { const b = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.035, 0.2), RM.matte(c)); b.position.set(-w * 0.18, 0.462 + i * 0.036, d * 0.12); b.rotation.y = i * 0.25; g.add(b); });
  const mug = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.035, 0.09, 16), RM.shell(0xf8fafc)); mug.position.set(w * 0.22, 0.49, -d * 0.18); g.add(mug);
  return shadows(g);
}
function toyBox(w, d) {
  const g = new THREE.Group();
  const box = new THREE.Mesh(new THREE.BoxGeometry(w, 0.3, d), RM.shell(0x8b5cf6)); box.position.y = 0.15; g.add(box);
  const lid = new THREE.Mesh(new THREE.BoxGeometry(w + 0.02, 0.03, d + 0.02), RM.shell(0x7c3aed)); lid.position.y = 0.315; g.add(lid);
  const ball = new THREE.Mesh(new THREE.SphereGeometry(0.06, 20, 14), RM.shell(0xf59e0b)); ball.position.set(w * 0.2, 0.39, 0); g.add(ball);
  return shadows(g);
}

function vacuum(seg) {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CylinderGeometry(R, R * 0.97, 0.07, seg), RM.shell(0xe5e7eb)); body.position.y = 0.05; g.add(body);
  const top = new THREE.Mesh(new THREE.CylinderGeometry(R * 0.9, R * 0.9, 0.006, seg), RM.glassDark()); top.position.y = 0.087; g.add(top);
  const bumper = new THREE.Mesh(new THREE.CylinderGeometry(R * 1.03, R * 1.03, 0.05, seg, 1, true, -Math.PI / 2 - 1.2, 2.4), new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.6, side: THREE.DoubleSide }));
  bumper.position.y = 0.045; g.add(bumper);
  const lidar = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.035, 24), RM.matte(0x111827)); lidar.position.set(0, 0.105, -0.04); g.add(lidar);
  const ringMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, emissive: 0x2563eb, emissiveIntensity: 1.8, roughness: 0.3 });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(R * 0.7, 0.007, 8, seg), ringMat); ring.rotation.x = Math.PI / 2; ring.position.y = 0.092; g.add(ring);
  const brushes = [];
  for (const s of [-1, 1]) {
    const b = new THREE.Group(); b.position.set(s * R * 0.62, 0.012, R * 0.62); g.add(b);
    for (let i = 0; i < 3; i++) { const bristle = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.004, 0.09), RM.matte(0x334155)); bristle.position.z = 0.045; const p = new THREE.Group(); p.rotation.y = i * 2.094; p.add(bristle); b.add(p); }
    brushes.push(b);
  }
  shadows(g);
  return { group: g, ringMat, brushes };
}

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(24, quality.segments || 48);

  camera.position.set(0.6, 5.2, 5.4);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 1.5, maxDistance: 16, target: new THREE.Vector3(0.6, 0, 0.2) });
  workshop(scene, engine, quality, { radius: 26, tiles: 6, shadowSize: 4.5 });

  // the room: plank floor, two painted back walls with skirting, a low front kerb so the view stays open
  const floorTex = woodTexture();
  const floorMat = new THREE.MeshStandardMaterial({ map: floorTex, roughness: 0.55 });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(RW, RD), floorMat); floor.rotation.x = -Math.PI / 2; floor.position.y = 0.002; floor.receiveShadow = true; scene.add(floor);
  const wallMat = new THREE.MeshStandardMaterial({ color: 0xf3efe7, roughness: 0.9 });
  const skirtMat = RM.matte(0xf8fafc);
  const walls = new THREE.Group(); scene.add(walls);
  const wall = (w, h, t, x, z, ry, mat) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, t), mat); m.position.set(x, h / 2, z); m.rotation.y = ry; walls.add(m); return m; };
  wall(RW + 0.16, 1.1, 0.08, 0, Z0 - 0.04, 0, wallMat);
  wall(RD, 1.1, 0.08, X0 - 0.04, 0, Math.PI / 2, wallMat);
  wall(RW, 0.08, 0.02, 0, Z0 + 0.01, 0, skirtMat);
  wall(RD, 0.08, 0.02, X0 + 0.01, 0, Math.PI / 2, skirtMat);
  wall(RW + 0.16, 0.1, 0.08, 0, Z0 + RD + 0.04, 0, wallMat);
  wall(RD + 0.08, 0.1, 0.08, X0 + RW + 0.04, 0, Math.PI / 2, wallMat);
  shadows(walls);
  const rug = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.2), new THREE.MeshStandardMaterial({ color: 0x9fb6c9, roughness: 1 }));
  rug.rotation.x = -Math.PI / 2; rug.position.set(-1.0, 0.004, -0.4); rug.receiveShadow = true; scene.add(rug);

  // the charging dock against the right wall
  const dock = new THREE.Group(); dock.position.set(DOCK.x, 0, DOCK.z); scene.add(dock);
  const tower = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.14, 0.3), RM.shell(0x111827)); tower.position.set(R + 0.07, 0.07, 0); dock.add(tower);
  const plate = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.008, 0.3), RM.matte(0x1f2937)); plate.position.set(0.05, 0.006, 0); dock.add(plate);
  for (const s of [-1, 1]) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.004, 0.03), RM.brass()); c.position.set(0.1, 0.012, s * 0.06); dock.add(c); }
  const dockLedMat = new THREE.MeshStandardMaterial({ color: 0x64748b, emissive: 0x000000, roughness: 0.3 });
  const dockLed = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.02, 0.12), dockLedMat); dockLed.position.set(R + 0.015, 0.11, 0); dock.add(dockLed);
  shadows(dock);

  // dirt: one speck per grid cell at most, instanced; cleaning shrinks it to nothing
  const dirt = new Uint8Array(GX * GZ);
  const specks = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.014, 0), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1 }), GX * GZ);
  specks.receiveShadow = true; scene.add(specks);
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), P = new THREE.Vector3(), S3 = new THREE.Vector3(), ZERO = new THREE.Matrix4().makeScale(0, 0, 0), col = new THREE.Color();
  let dirtLeft = 0, dirtTotal = 0;

  const vac = vacuum(seg); scene.add(vac.group);
  const tag = label(stage, camera);

  const furn = [
    { name: 'sofa', w: 1.12, d: 0.53, make: sofa },
    { name: 'table', w: 0.78, d: 0.84, make: table },
    { name: 'toy box', w: 0.56, d: 0.38, make: toyBox },
  ];
  const HOME = [[X0 + RW * 0.18, Z0 + RD * 0.2], [X0 + RW * 0.55, Z0 + RD * 0.5], [X0 + RW * 0.2, Z0 + RD * 0.66]];
  furn.forEach((f) => { f.group = f.make(f.w, f.d); scene.add(f.group); f.centre = new THREE.Vector3(); });
  function placeFurn(f, x, z) {
    f.x = clamp(x, X0, X0 + RW - f.w); f.z = clamp(z, Z0, Z0 + RD - f.d);
    f.group.position.set(f.x + f.w / 2, 0, f.z + f.d / 2); f.centre.set(f.x + f.w / 2, 0.35, f.z + f.d / 2);
  }
  function inFurn(px, pz, pad) { for (const f of furn) if (px > f.x - pad && px < f.x + f.w + pad && pz > f.z - pad && pz < f.z + f.d + pad) return f; return null; }

  const hud = createHud(stage);
  const badge = hud.badge('State: SEARCH', SCOL.SEARCH);

  let state = 'SEARCH', timer = 0, turnLeft = 0, battery = 100, running = true, speedMul = 1, dockEnabled = true, brushSpin = 0;
  const bot = { x: 0, z: 0, a: 0.4 };
  const log = [];
  const glow = {}; STATES.forEach((s) => { glow[s] = s === 'SEARCH' ? 1 : 0; });
  const flash = EDGES.map(() => 0);

  const panel = createPanel(stage, { title: 'State machine' });
  const [runB] = panel.buttonRow([
    { label: 'Pause', icon: 'pause', variant: 'ghost', onClick: () => { running = !running; runB.setLabel(running ? 'Pause' : 'Run'); } },
    { label: 'New room', icon: 'restart_alt', variant: 'ghost', onClick: () => layoutRoom(true) },
  ]);
  panel.slider({ label: 'Speed', min: 0.5, max: 3, step: 0.25, value: 1, format: (v) => `${v}×`, onChange: (v) => { speedMul = v; } });
  panel.toggle({ label: 'DOCK state enabled', value: true, onChange: (v) => { dockEnabled = v; } });
  panel.buttonRow([{ label: 'Battery low', icon: 'battery_alert', onClick: () => { battery = Math.min(battery, 19); } }, { label: 'Bump!', icon: 'touch_app', onClick: () => fire('bump') }]);
  const diagram = canvasCard(panel.body, 0.95);
  const st = panel.stats([{ key: 'state', label: 'State' }, { key: 'bat', label: 'Battery' }, { key: 'clean', label: 'Floor cleaned' }, { key: 'last', label: 'Last event' }]);
  panel.info('In a state machine the robot is always in exactly one state, and only the listed events can move it. To know what "battery low" does you read one arrow, not a tangle of if-else. Without the DOCK state, the battery simply runs flat.');

  function fire(ev) {
    for (let i = 0; i < EDGES.length; i++) {
      const [a, b, e] = EDGES[i];
      if (a === state && e === ev) {
        if (b === 'DOCK' && !dockEnabled) return false;
        state = b; flash[i] = 1; timer = 0;
        if (b === 'TURN') turnLeft = (Math.random() < 0.5 ? -1 : 1) * (0.6 + Math.random() * 1.8);
        log.unshift(`${a} —${ev}→ ${b}`); if (log.length > 4) log.pop();
        return true;
      }
    }
    return false;
  }

  function layoutRoom(shuffle) {
    furn.forEach((f, i) => placeFurn(f, HOME[i][0] + (shuffle ? (Math.random() - 0.5) * 1.2 : 0), HOME[i][1] + (shuffle ? (Math.random() - 0.5) * 0.8 : 0)));
    bot.x = X0 + RW * 0.5; bot.z = Z0 + RD * 0.3; bot.a = 0.5; battery = 100; state = 'SEARCH'; timer = 0;
    dirtTotal = 0;
    for (let j = 0; j < GZ; j++) for (let i = 0; i < GX; i++) {
      const k = j * GX + i, px = X0 + (i + 0.2 + Math.random() * 0.6) * RW / GX, pz = Z0 + (j + 0.2 + Math.random() * 0.6) * RD / GZ;
      const d = inFurn(px, pz, 0) || Math.random() >= 0.55 ? 0 : 1;
      dirt[k] = d; dirtTotal += d;
      if (d) {
        const s = 0.6 + Math.random() * 0.9;
        specks.setMatrixAt(k, M.compose(P.set(px, 0.006, pz), Q.setFromAxisAngle(S3.set(0, 1, 0), Math.random() * 6), S3.set(s, s * 0.45, s)));
        specks.setColorAt(k, col.setHSL(0.07 + Math.random() * 0.04, 0.35 + Math.random() * 0.2, 0.18 + Math.random() * 0.2));
      } else specks.setMatrixAt(k, ZERO);
    }
    specks.instanceMatrix.needsUpdate = true; if (specks.instanceColor) specks.instanceColor.needsUpdate = true;
    dirtLeft = dirtTotal; log.length = 0;
  }

  function blocked(nx, nz) {
    if (nx < X0 + R || nx > X0 + RW - R || nz < Z0 + R || nz > Z0 + RD - R) return true;
    for (const f of furn) { const cx = clamp(nx, f.x, f.x + f.w), cz = clamp(nz, f.z, f.z + f.d); if (Math.hypot(nx - cx, nz - cz) < R) return true; }
    return false;
  }

  let dockSide = 1;
  function clearAhead(a) {
    const d = Math.min(0.4, Math.hypot(DOCK.x - bot.x, DOCK.z - bot.z));
    for (let t = 0.1; t <= d + 1e-6; t += 0.1) if (blocked(bot.x + Math.sin(a) * t, bot.z + Math.cos(a) * t)) return false;
    return true;
  }

  function stepFSM(dt) {
    if (state !== 'CHARGE') battery = Math.max(0, battery - dt * 1.6);
    if (battery <= 0) return;
    if (battery < 20 && (state === 'SEARCH' || state === 'BACKUP' || state === 'TURN') && dockEnabled) fire('battery low');
    timer += dt;
    if (state === 'SEARCH' || state === 'DOCK') {
      if (state === 'DOCK') {
        // home on the dock's beacon; if furniture is in the way, swing to the clear side and skirt it
        const ta = Math.atan2(DOCK.x - bot.x, DOCK.z - bot.z);
        let want = ta;
        if (!clearAhead(ta)) {
          for (let k = 1; k <= 8; k++) {
            const a1 = ta + dockSide * k * 0.35, a2 = ta - dockSide * k * 0.35;
            if (clearAhead(a1)) { want = a1; break; }
            if (clearAhead(a2)) { want = a2; dockSide = -dockSide; break; }
          }
        }
        const da = Math.atan2(Math.sin(want - bot.a), Math.cos(want - bot.a));
        bot.a += clamp(da, -2.5 * dt, 2.5 * dt);
        if (Math.hypot(DOCK.x - bot.x, DOCK.z - bot.z) < 0.06) { fire('docked'); return; }
      } else bot.a += (Math.random() - 0.5) * 0.6 * dt;
      const nx = bot.x + Math.sin(bot.a) * V * dt, nz = bot.z + Math.cos(bot.a) * V * dt;
      if (blocked(nx, nz)) fire('bump'); else { bot.x = nx; bot.z = nz; }
    } else if (state === 'BACKUP') {
      const nx = bot.x - Math.sin(bot.a) * V * 0.6 * dt, nz = bot.z - Math.cos(bot.a) * V * 0.6 * dt;
      if (!blocked(nx, nz)) { bot.x = nx; bot.z = nz; }
      if (timer > 0.45) fire('timer done');
    } else if (state === 'TURN') {
      const s = Math.sign(turnLeft) * 2.6 * dt; bot.a += s; turnLeft -= s;
      if (Math.abs(turnLeft) < 0.05) fire('turn done');
    } else if (state === 'CHARGE') {
      battery = Math.min(100, battery + dt * 12);
      if (battery >= 100) { fire('battery full'); bot.a += Math.PI; }
    }
    if (state === 'SEARCH' || state === 'DOCK') {
      const i = Math.floor((bot.x - X0) / RW * GX), j = Math.floor((bot.z - Z0) / RD * GZ);
      let changed = false;
      for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
        const ii = i + di, jj = j + dj, k = jj * GX + ii;
        if (ii >= 0 && jj >= 0 && ii < GX && jj < GZ && dirt[k]) { dirt[k] = 0; dirtLeft--; specks.setMatrixAt(k, ZERO); changed = true; }
      }
      if (changed) specks.instanceMatrix.needsUpdate = true;
    }
  }

  const drag = planeDrag(engine.canvas, camera, controls, {
    handles: () => [{ id: 'bot', pos: vac.group.position }, ...furn.map((f) => ({ id: 'f', f, pos: f.centre }))],
    onDown: (h, p) => { if (h.f && p) { h.ox = p.x - h.f.x; h.oz = p.z - h.f.z; } },
    onMove: (h, p) => {
      if (h.f) placeFurn(h.f, p.x - h.ox, p.z - h.oz);
      else { bot.x = clamp(p.x, X0 + R, X0 + RW - R); bot.z = clamp(p.z, Z0 + R, Z0 + RD - R); }
    },
  });

  // the live state diagram, drawn into the panel card
  function arrowLine(g, sx, sy, ex, ey, color, w) {
    const a = Math.atan2(ey - sy, ex - sx), hl = 6 + w;
    g.strokeStyle = color; g.fillStyle = color; g.lineWidth = w;
    g.beginPath(); g.moveTo(sx, sy); g.lineTo(ex - Math.cos(a) * hl * 0.8, ey - Math.sin(a) * hl * 0.8); g.stroke();
    g.beginPath(); g.moveTo(ex, ey); g.lineTo(ex - Math.cos(a - 0.4) * hl, ey - Math.sin(a - 0.4) * hl); g.lineTo(ex - Math.cos(a + 0.4) * hl, ey - Math.sin(a + 0.4) * hl); g.fill();
  }
  function drawDiagram() {
    const { g, w, h } = diagram.ctx();
    const cx = w / 2, cy = h * 0.46, rx = w * 0.33, ry = h * 0.3;
    const N = { SEARCH: [cx + w * 0.1, cy - ry], BACKUP: [cx + rx, cy], TURN: [cx + w * 0.1, cy + ry], DOCK: [cx - rx, cy + ry * 0.15], CHARGE: [cx - rx, cy - ry] };
    const nw = Math.min(84, w * 0.25), nh = 26;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('State diagram', 10, 16);
    g.textAlign = 'center';
    for (let i = 0; i < EDGES.length; i++) {
      const [a, b, e] = EDGES[i];
      if (b === 'DOCK' && !dockEnabled) continue;
      const A = N[a], B = N[b], dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy);
      const ox = -dy / L * 9, oy = dx / L * 9;
      const sx = A[0] + ox + dx / L * nw * 0.42, sy = A[1] + oy + dy / L * nh * 0.85, ex = B[0] + ox - dx / L * nw * 0.42, ey = B[1] + oy - dy / L * nh * 0.85;
      const f = flash[i];
      arrowLine(g, sx, sy, ex, ey, f > 0 ? `rgba(251,146,60,${0.5 + f * 0.5})` : 'rgba(148,163,184,0.55)', f > 0 ? 2 + f * 2 : 1.4);
      g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = f > 0 ? '#fb923c' : '#8ea0c2';
      const [lt, lk] = LBL[i]; g.fillText(e, A[0] + dx * lt + ox * lk, A[1] + dy * lt + oy * lk + 3);
    }
    for (const s of STATES) {
      if (s === 'DOCK' && !dockEnabled) continue;
      const [x, y] = N[s], k = glow[s];
      if (k > 0.02) { g.fillStyle = SCOL[s] + Math.round(0x30 * k).toString(16).padStart(2, '0'); g.beginPath(); g.roundRect(x - nw / 2 - 6 * k, y - nh / 2 - 6 * k, nw + 12 * k, nh + 12 * k, 12); g.fill(); }
      g.fillStyle = k > 0.5 ? SCOL[s] : 'rgba(15,23,42,0.9)'; g.strokeStyle = SCOL[s]; g.lineWidth = 2;
      g.beginPath(); g.roundRect(x - nw / 2, y - nh / 2, nw, nh, 8); g.fill(); g.stroke();
      g.font = '800 10.5px Poppins, system-ui, sans-serif'; g.fillStyle = k > 0.5 ? '#fff' : '#cbd5e1'; g.fillText(s, x, y + 4);
    }
    g.textAlign = 'left';
    for (let i = 0; i < Math.min(2, log.length); i++) { g.font = `${i ? 500 : 700} 9.5px Poppins, system-ui, sans-serif`; g.fillStyle = i ? '#8ea0c2' : '#e8eefb'; g.fillText(log[i], 10, h - 8 - i * 14); }
  }

  // frame the room beside the docked panel whenever the screen shape changes
  let fitW = 0;
  const fitT = new THREE.Vector3();
  function fit() {
    const W = stage.clientWidth;
    if (W === fitW || !W) return;
    fitW = W;
    const avail = W > 760 ? W - 310 : W, totalW = 6.4 * W / avail;
    const half = Math.tan(camera.fov * Math.PI / 360);
    controls.setDistance(Math.min(16, Math.max(totalW / 2 / half / camera.aspect, 2.6 / half)));
    controls.setTarget(fitT.set((W - avail) / 2 / W * totalW, 0, 0.3));
  }

  layoutRoom(false);
  let tick = 0;
  const tagAt = new THREE.Vector3();
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    if (running) { const n = Math.ceil(speedMul * 2); for (let i = 0; i < n; i++) stepFSM(dt * speedMul / n); }
    for (const s of STATES) glow[s] += ((s === state ? 1 : 0) - glow[s]) * (1 - Math.exp(-dt * 10));
    for (let i = 0; i < flash.length; i++) flash[i] = Math.max(0, flash[i] - dt * 1.2);

    const dead = battery <= 0;
    vac.group.position.set(bot.x, 0, bot.z); vac.group.rotation.y = bot.a;
    const c = dead ? 0x475569 : parseInt(SCOL[state].slice(1), 16);
    vac.ringMat.color.setHex(c); vac.ringMat.emissive.setHex(c); vac.ringMat.emissiveIntensity = dead ? 0 : state === 'CHARGE' ? 1 + 0.8 * Math.sin(performance.now() / 300) : 1.8;
    if (running && !dead && (state === 'SEARCH' || state === 'DOCK')) brushSpin += dt * 14 * speedMul;
    vac.brushes[0].rotation.y = brushSpin; vac.brushes[1].rotation.y = -brushSpin;
    dockLedMat.emissive.setHex(state === 'CHARGE' ? 0x22c55e : dockEnabled ? 0x0d9488 : 0x000000); dockLedMat.emissiveIntensity = 1.6;
    tag.el.textContent = dead ? 'battery flat' : `${state} · ${Math.round(battery)} %`;
    tag.el.style.background = dead ? 'rgba(220,38,38,0.9)' : SCOL[state];
    tag.at(tagAt.set(bot.x, 0.32, bot.z));

    fit();
    controls.update(dt);
    if ((tick++ & 1) === 0) drawDiagram();
    st.state.set(state); st.bat.set(`${Math.round(battery)} %`); st.clean.set(`${Math.round(100 * (1 - dirtLeft / Math.max(1, dirtTotal)))} %`); st.last.set(log[0] || '—');
    if (dead) badge.set('Battery flat! The robot stopped (no DOCK state).');
    else { badge.set(`State: ${state}`); badge.el.style.setProperty('--ix-hud-color', SCOL[state]); }
  });
  engine.start();

  stage.__fsm = { state: () => ({ state, battery, clean: 1 - dirtLeft / Math.max(1, dirtTotal), x: bot.x, z: bot.z }), fire, battery: (b) => { battery = b; }, speed: (s) => { speedMul = s; } };
  return {
    dispose() {
      drag.dispose(); tag.remove();
      specks.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__fsm;
    },
  };
}
