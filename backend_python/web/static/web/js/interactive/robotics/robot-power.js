/**
 * Robot Power in 3D — a real little circuit on a plywood board: AA cells in a holder, a knife
 * switch, a toy DC motor with a propeller, and red and black wires joining them in a loop. Close
 * the switch (tap it, or use the panel) and glowing dots show the current flowing round the loop;
 * more cells mean more voltage, more current and a faster fan. Pull a wire loose and everything
 * stops. The motor is a proper DC motor: its spin makes a back-voltage, so the current is
 * I = (V − kω) / R, and the propeller's air drag grows with ω². 1 unit = 10 cm.
 */
import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { workshop, RM, shadows } from '../core/robot-kit.js';
import { label } from '../physics/physics3d/field.js';

const CELL_V = 1.5, MAX_CELLS = 6;
const RM_OHM = 2.5, KE = 0.01146, J = 5e-6, DRAG = 2.1e-8, VISC = 2e-6, COULOMB = 4e-4;   // motor and propeller, SI
const NDOTS = 36;

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(24, quality.segments || 48);

  camera.position.set(0.9, 4.2, 6.2);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 2, maxDistance: 16, target: new THREE.Vector3(0.1, 0.5, 0) });
  workshop(scene, engine, quality, { radius: 24, tiles: 6, shadowSize: 4 });

  const add = (geo, mat, x, y, z, parent = scene) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); parent.add(m); return m; };
  const TOP = 0.12;

  // plywood board
  const ply = new THREE.MeshStandardMaterial({ color: 0xd9b88a, roughness: 0.7 });
  const board = add(new THREE.BoxGeometry(6.6, 0.12, 3.2), ply, 0, 0.06, 0); board.receiveShadow = true; board.castShadow = true;

  // battery holder: six slots, filled by as many AA cells as the voltage needs
  const holder = new THREE.Group(); holder.position.set(-2.3, TOP, 0.25); scene.add(holder);
  const slotD = 0.17, HD = MAX_CELLS * slotD + 0.1;
  add(new THREE.BoxGeometry(0.66, 0.06, HD), RM.matte(0x111318), 0, 0.03, 0, holder);
  for (const s of [-1, 1]) add(new THREE.BoxGeometry(0.06, 0.18, HD), RM.matte(0x111318), s * 0.3, 0.09, 0, holder);
  for (let i = 0; i <= MAX_CELLS; i++) add(new THREE.BoxGeometry(0.54, 0.1, 0.012), RM.matte(0x111318), 0, 0.08, -HD / 2 + 0.05 + i * slotD, holder);
  const cells = [];
  for (let i = 0; i < MAX_CELLS; i++) {
    const c = new THREE.Group(); c.position.set(0, 0.12, -HD / 2 + 0.05 + (i + 0.5) * slotD); c.rotation.y = i % 2 ? Math.PI : 0; holder.add(c);
    const body = add(new THREE.CylinderGeometry(0.072, 0.072, 0.46, 24), RM.shell(0x16a34a), 0, 0, 0, c); body.rotation.z = Math.PI / 2;
    const band = add(new THREE.CylinderGeometry(0.073, 0.073, 0.12, 24), RM.shell(0x111827), -0.17, 0, 0, c); band.rotation.z = Math.PI / 2;
    const nub = add(new THREE.CylinderGeometry(0.025, 0.025, 0.03, 12), RM.steel(), 0.245, 0, 0, c); nub.rotation.z = Math.PI / 2;
    const cap = add(new THREE.CylinderGeometry(0.06, 0.06, 0.012, 20), RM.steel(), -0.235, 0, 0, c); cap.rotation.z = Math.PI / 2;
    cells.push(c);
  }
  shadows(holder);
  const plusT = new THREE.Vector3(-2.3 + 0.2, TOP + 0.14, 0.25 + HD / 2 + 0.02);
  const minusT = new THREE.Vector3(-2.3 - 0.2, TOP + 0.14, 0.25 + HD / 2 + 0.02);
  add(new THREE.BoxGeometry(0.08, 0.12, 0.03), RM.matte(0xdc2626), plusT.x, TOP + 0.08, plusT.z - 0.01);
  add(new THREE.BoxGeometry(0.08, 0.12, 0.03), RM.matte(0x111318), minusT.x, TOP + 0.08, minusT.z - 0.01);

  // knife switch on a wooden block: a copper blade hinged at one end, closing into a sprung clip
  const sw = new THREE.Group(); sw.position.set(-0.3, TOP, -0.9); scene.add(sw);
  add(new THREE.BoxGeometry(1.1, 0.08, 0.4), new THREE.MeshStandardMaterial({ color: 0x7c4a2a, roughness: 0.55 }), 0, 0.04, 0, sw);
  const copper = new THREE.MeshStandardMaterial({ color: 0xc8794a, roughness: 0.28, metalness: 1 });
  add(new THREE.BoxGeometry(0.06, 0.18, 0.14), copper, -0.42, 0.17, 0, sw);
  for (const s of [-1, 1]) add(new THREE.BoxGeometry(0.06, 0.16, 0.02), copper, 0.42, 0.16, s * 0.035, sw);
  const hinge = new THREE.Group(); hinge.position.set(-0.42, 0.22, 0); sw.add(hinge);
  add(new THREE.BoxGeometry(0.86, 0.025, 0.05), copper, 0.43, 0, 0, hinge);
  add(new THREE.CylinderGeometry(0.045, 0.04, 0.22, 16), RM.matte(0x111318), 0.82, 0.11, 0, hinge);
  const spark = add(new THREE.SphereGeometry(0.03, 10, 8), new THREE.MeshBasicMaterial({ color: 0xfff3b0, transparent: true, opacity: 0, depthWrite: false }), 0.42, 0.22, 0, sw);
  shadows(sw);
  const swIn = new THREE.Vector3(-0.3 - 0.42, TOP + 0.1, -0.9), swOut = new THREE.Vector3(-0.3 + 0.42, TOP + 0.1, -0.9);

  // DC motor on a bracket, shaft along +x, a three-blade propeller and the blur disc it makes at speed
  const mot = new THREE.Group(); mot.position.set(1.7, TOP, 0.2); scene.add(mot);
  add(new THREE.BoxGeometry(0.5, 0.06, 0.6), RM.alu(), 0, 0.03, 0, mot);
  add(new THREE.BoxGeometry(0.06, 0.8, 0.4), RM.alu(), -0.1, 0.4, 0, mot);
  const can = add(new THREE.CylinderGeometry(0.15, 0.15, 0.36, seg), RM.steel(), 0.1, 0.78, 0, mot); can.rotation.z = Math.PI / 2;
  const endCap = add(new THREE.CylinderGeometry(0.14, 0.14, 0.06, seg), RM.matte(0xf8fafc), -0.1, 0.78, 0, mot); endCap.rotation.z = Math.PI / 2;
  [-1, 1].forEach((s) => add(new THREE.BoxGeometry(0.02, 0.08, 0.03), RM.brass(), -0.14, 0.78 - 0.1, s * 0.07, mot));
  const shaft = add(new THREE.CylinderGeometry(0.015, 0.015, 0.22, 10), RM.steel(), 0.38, 0.78, 0, mot); shaft.rotation.z = Math.PI / 2;
  const prop = new THREE.Group(); prop.position.set(0.48, 0.78, 0); mot.add(prop);
  const propMat = new THREE.MeshStandardMaterial({ color: 0xf97316, roughness: 0.4 });
  const hub = add(new THREE.CylinderGeometry(0.06, 0.07, 0.08, 20), propMat, 0, 0, 0, prop); hub.rotation.z = Math.PI / 2;
  const bladeGeo = new THREE.BoxGeometry(0.02, 0.5, 0.13);
  for (let i = 0; i < 3; i++) { const p = new THREE.Group(); p.rotation.x = i * Math.PI * 2 / 3; prop.add(p); const b = add(bladeGeo, propMat, 0, 0.27, 0, p); b.rotation.y = 0.45; }
  const blurMat = new THREE.MeshBasicMaterial({ color: 0xf97316, transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide });
  const blur = add(new THREE.RingGeometry(0.08, 0.52, seg), blurMat, 0.5, 0.78, 0, mot); blur.rotation.y = Math.PI / 2;
  shadows(mot);
  const motA = new THREE.Vector3(1.7 - 0.14, TOP + 0.68, 0.2 - 0.07), motB = new THREE.Vector3(1.7 - 0.14, TOP + 0.68, 0.2 + 0.07);

  // paper streamers in the breeze
  const flags = new THREE.Group(); flags.position.set(2.85, TOP, 0.2); scene.add(flags);
  add(new THREE.CylinderGeometry(0.02, 0.02, 1.3, 10), RM.steel(), 0, 0.65, 0, flags);
  add(new THREE.CylinderGeometry(0.12, 0.12, 0.03, 20), RM.darkAlu(), 0, 0.015, 0, flags);
  const streamers = [0x38bdf8, 0xfacc15, 0xf472b6].map((c, i) => {
    const p = new THREE.Group(); p.position.set(0, 1.22, (i - 1) * 0.1); flags.add(p);
    const strip = add(new THREE.PlaneGeometry(0.06, 0.55), new THREE.MeshStandardMaterial({ color: c, roughness: 0.8, side: THREE.DoubleSide }), 0, -0.275, 0, p);
    strip.castShadow = true;
    return p;
  });

  // wires: soft tubes resting on the board between the terminals
  const wireOf = (pts, color) => {
    const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
    const m = new THREE.Mesh(new THREE.TubeGeometry(curve, 96, 0.028, 10, false), new THREE.MeshStandardMaterial({ color, roughness: 0.45 }));
    m.castShadow = true; scene.add(m);
    return { curve, mesh: m, len: curve.getLength() };
  };
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  const w1 = wireOf([plusT, V3(plusT.x + 0.15, TOP + 0.06, plusT.z + 0.25), V3(-1.4, TOP + 0.04, 0.9), V3(-1.3, TOP + 0.04, -0.6), V3(swIn.x - 0.12, TOP + 0.06, -0.9), swIn], 0xdc2626);
  const w2 = wireOf([swOut, V3(swOut.x + 0.18, TOP + 0.05, -0.9), V3(1.0, TOP + 0.04, -0.6), V3(motA.x - 0.25, TOP + 0.1, motA.z - 0.1), motA], 0xdc2626);
  // the black return wire can be pulled loose from the battery's − terminal
  const loosePts = [motB, V3(motB.x - 0.2, TOP + 0.1, motB.z + 0.2), V3(0.6, TOP + 0.04, 1.2), V3(-1.2, TOP + 0.04, 1.35), V3(-1.75, TOP + 0.1, 1.15)];
  const w3 = wireOf([...loosePts, V3(minusT.x + 0.2, TOP + 0.08, minusT.z + 0.35), V3(minusT.x - 0.05, TOP + 0.06, minusT.z + 0.15), minusT], 0x1f2937);
  const w3loose = wireOf([...loosePts, V3(-2.0, TOP + 0.3, 1.35), V3(-2.1, TOP + 0.55, 1.4)], 0x1f2937);
  w3loose.mesh.visible = false;
  const clip = add(new THREE.CylinderGeometry(0.035, 0.035, 0.08, 12), RM.brass(), -2.1, TOP + 0.6, 1.4); clip.visible = false;
  const loop = [w1, w2, w3], loopLen = w1.len + w2.len + w3.len;

  // the current: glowing dots travelling the loop from + round to −
  const dots = new THREE.InstancedMesh(new THREE.SphereGeometry(0.03, 10, 8), new THREE.MeshBasicMaterial({ color: 0xfde047, toneMapped: false }), NDOTS);
  dots.frustumCulled = false; scene.add(dots);
  const M = new THREE.Matrix4(), P = new THREE.Vector3(), ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
  const dotS = new Float32Array(NDOTS); for (let i = 0; i < NDOTS; i++) dotS[i] = i / NDOTS * loopLen;
  function pointAt(s, out) {
    for (const w of loop) { if (s <= w.len) return w.curve.getPointAt(Math.min(1, s / w.len), out); s -= w.len; }
    return out.copy(minusT);
  }

  const vLbl = label(stage, camera), rpmLbl = label(stage, camera);

  const hud = createHud(stage);
  const badge = hud.badge('Circuit OPEN', '#94a3b8');

  let nCells = 3, closed = false, loose = false, omega = 0, I = 0, blade = 1.05, sparkT = 0, flutter = 0;
  const panel = createPanel(stage, { title: 'Robot power' });
  panel.slider({ label: 'Batteries (AA cells)', min: 1, max: MAX_CELLS, step: 1, value: nCells, format: (n) => `${n} × 1.5 V = ${(n * CELL_V).toFixed(1)} V`, onChange: (n) => { nCells = n; } });
  const swT = panel.toggle({ label: 'Switch closed', value: false, onChange: (v) => setClosed(v) });
  panel.toggle({ label: 'Pull the black wire loose', value: false, onChange: (v) => { loose = v; } });
  const st = panel.stats([{ key: 'v', label: 'Voltage' }, { key: 'i', label: 'Current' }, { key: 'rpm', label: 'Motor speed' }, { key: 'p', label: 'Power' }]);
  panel.info('Electricity needs a complete loop. Close the switch to let current flow from the battery, through the motor, and back again. Tap the switch on the board too. More cells push harder: more current, a faster fan.');

  function setClosed(v) { if (v && !closed) sparkT = 1; closed = v; swT.set(v); }

  // tap the switch itself to flip it
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  let downAt = null;
  function onDown(e) { downAt = [e.clientX, e.clientY]; }
  function onUp(e) {
    if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 6) { downAt = null; return; }
    downAt = null;
    const r = engine.canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    if (ray.intersectObject(sw, true).length) setClosed(!closed);
  }
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);

  // frame the board beside the docked panel whenever the screen shape changes
  let fitW = 0;
  const fitT = new THREE.Vector3();
  function fit() {
    const W = stage.clientWidth;
    if (W === fitW || !W) return;
    fitW = W;
    const avail = W > 760 ? W - 310 : W, totalW = 6.6 * W / avail;
    const half = Math.tan(camera.fov * Math.PI / 360);
    controls.setDistance(Math.min(16, Math.max(totalW / 2 / half / camera.aspect, 2.4 / half)));
    controls.setTarget(fitT.set(0.1 + (W - avail) / 2 / W * totalW, 0.4, 0));
  }

  let tick = 0;
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    const V = nCells * CELL_V, complete = closed && !loose;
    // the motor, sub-stepped: electrical side is instantaneous, the rotor has inertia
    const n = 20, h = dt / n;
    for (let i = 0; i < n; i++) {
      I = complete ? (V - KE * omega) / RM_OHM : 0;
      const torque = KE * I - DRAG * omega * omega - VISC * omega - (omega > 0.5 ? COULOMB : 0);
      omega = Math.max(0, omega + torque / J * h);
    }
    const rpm = omega * 60 / (2 * Math.PI);

    cells.forEach((c, i) => { c.visible = i < nCells; });
    blade += ((closed ? 0 : 1.05) - blade) * (1 - Math.exp(-dt * 14));
    hinge.rotation.z = blade;
    sparkT = Math.max(0, sparkT - dt * 4); spark.material.opacity = sparkT * (loose ? 0 : 1); spark.scale.setScalar(1 + sparkT * 2);
    w3.mesh.visible = !loose; w3loose.mesh.visible = loose; clip.visible = loose;

    // the eye cannot follow thousands of rpm: show a slowed, stroboscopic blade and a blur disc
    const visW = omega < 40 ? omega : 40 + (omega - 40) * 0.03;
    prop.rotation.x += visW * dt;
    blurMat.opacity = Math.min(0.45, Math.max(0, (omega - 30) / 400));
    flutter += dt * (3 + omega * 0.03);
    const breeze = Math.min(1, (omega / 600) ** 2);
    streamers.forEach((p, i) => { p.rotation.z = breeze * 1.25 + Math.sin(flutter + i * 1.7) * 0.12 * breeze; p.rotation.x = Math.sin(flutter * 1.3 + i) * 0.08 * breeze; });

    const flowing = complete && I > 0.005;
    const speed = I * 1.6;
    for (let i = 0; i < NDOTS; i++) {
      if (!flowing) { dots.setMatrixAt(i, ZERO); continue; }
      dotS[i] = (dotS[i] + speed * dt) % loopLen;
      pointAt(dotS[i], P); dots.setMatrixAt(i, M.makeTranslation(P.x, P.y + 0.01, P.z));
    }
    dots.instanceMatrix.needsUpdate = true;

    vLbl.el.textContent = `${V.toFixed(1)} V`; vLbl.at(P.set(-2.3, TOP + 0.55, 0.25));
    rpmLbl.el.textContent = `${Math.round(rpm).toLocaleString('en-US')} rpm`; rpmLbl.at(P.set(1.7, TOP + 1.45, 0.2));
    fit();
    controls.update(dt);
    if ((tick++ & 3) === 0) {
      st.v.set(`${V.toFixed(1)} V`); st.i.set(`${I.toFixed(2)} A`); st.rpm.set(`${Math.round(rpm).toLocaleString('en-US')} rpm`); st.p.set(`${(V * I).toFixed(1)} W`);
      const msg = !closed ? ['Circuit OPEN: the switch breaks the loop', '#94a3b8'] : loose ? ['Loop broken: a wire is loose', '#f59e0b'] : ['Circuit CLOSED: current flows!', '#35d07f'];
      badge.set(msg[0]); badge.el.style.setProperty('--ix-hud-color', msg[1]);
    }
  });
  engine.start();

  stage.__power = { set: (o) => { if (o.cells) nCells = o.cells; if (o.closed != null) setClosed(o.closed); if (o.loose != null) loose = o.loose; }, state: () => ({ I, rpm: omega * 60 / (2 * Math.PI), closed, loose }) };
  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown); engine.canvas.removeEventListener('pointerup', onUp);
      vLbl.remove(); rpmLbl.remove(); dots.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__power;
    },
  };
}
