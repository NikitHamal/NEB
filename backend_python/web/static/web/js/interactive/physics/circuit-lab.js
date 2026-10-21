/**
 * Circuit builder in 3D: a battery pack of cells, a knife switch, an ammeter, a voltmeter and two
 * colour-banded resistors on a wooden board, wired in series or in parallel. Ohm's law sets every
 * current (I = V/R; series R₁ + R₂; parallel R₁R₂/(R₁ + R₂)), and the charge carriers flow round each
 * branch at a speed proportional to its current, so the split in a parallel circuit is visible. Tap
 * the switch or a resistor (or use the panel) to change things; the meters' needles read the real values.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { dialMeter } from '../core/handson/circuit.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const VALUES = [1, 2.2, 3.3, 4.7, 6.8, 10, 15, 22, 33, 47, 68, 100];
const BAND = [0x111827, 0x7c4a1e, 0xdc2626, 0xf97316, 0xfacc15, 0x16a34a, 0x2563eb, 0x7c3aed, 0x6b7280, 0xf8fafc];
const CELL = 1.5; const Y = 0.12;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });
function bands(R) { let exp = 0; let v = R; while (v >= 100) { v /= 10; exp++; } while (v < 10) { v *= 10; exp--; } const d = Math.round(v); return [Math.floor(d / 10), d % 10, exp]; }

function resistor() {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.11, 0.42, 8, 20), new THREE.MeshStandardMaterial({ color: 0xd9c4a0, roughness: 0.6 })); body.rotation.x = Math.PI / 2; g.add(body);
  const bandMats = [0, 1, 2, 3].map((i) => new THREE.MeshStandardMaterial({ color: i === 3 ? 0xc9a14a : 0x111827, roughness: 0.5, metalness: i === 3 ? 0.8 : 0 }));
  [-0.16, -0.06, 0.04, 0.17].forEach((z, i) => { const b = new THREE.Mesh(new THREE.CylinderGeometry(0.118, 0.118, 0.05, 20), bandMats[i]); b.rotation.x = Math.PI / 2; b.position.z = z; g.add(b); });
  const legs = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.2, 8), new THREE.MeshStandardMaterial({ color: 0xc0c6cf, metalness: 0.9, roughness: 0.3 })); legs.rotation.x = Math.PI / 2; g.add(legs);
  g.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  return { group: g, set(R) { const [a, b, e] = bands(R); bandMats[0].color.setHex(BAND[a]); bandMats[1].color.setHex(BAND[b]); bandMats[2].color.setHex(e < 0 ? 0xc9a14a : BAND[e]); } };
}

export default function init(stage) {
  const S = createChemLab(stage, { title: 'Circuit builder', aim: "Series and parallel circuits and Ohm's law", subject: 'physics', target: [0.3, 0.2, 0], camera: [0.6, 5.2, 5.8], minDistance: 3, maxDistance: 14 });
  if (!S) return null;
  const { engine, world, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Tap the switch to close the circuit', '#2563eb');

  let cells = 4; let R1i = 5; let R2i = 7; let parallel = false; let closed = false; let electrons = false;
  let I = 0; let I1 = 0; let I2 = 0; let V1 = 0; let V2 = 0; let Rt = 0; let flowK = 0;

  const board = new THREE.Mesh(new THREE.BoxGeometry(8.4, 0.12, 5.2), new THREE.MeshStandardMaterial({ color: 0xc8a06a, roughness: 0.65 })); board.position.y = 0.06; board.receiveShadow = true; world.add(board);
  const pack = new THREE.Group(); pack.position.set(-3.4, Y, 0); world.add(pack);
  const holder = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.18, 3.2), new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.6 })); holder.position.y = 0.06; pack.add(holder);
  const cellMeshes = Array.from({ length: 8 }, (_, i) => {
    const c = new THREE.Group();
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.36, 20), new THREE.MeshStandardMaterial({ color: i % 2 ? 0x1d4ed8 : 0x111827, metalness: 0.3, roughness: 0.4 })); body.rotation.x = Math.PI / 2;
    const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.04, 12), new THREE.MeshStandardMaterial({ color: 0xc0c6cf, metalness: 0.9 })); cap.rotation.x = Math.PI / 2; cap.position.z = -0.2;
    c.add(body, cap); c.position.set(0, 0.2, -1.4 + i * 0.4); pack.add(c); return c;
  });
  const swG = new THREE.Group(); swG.position.set(-1.7, Y, -2.0); world.add(swG);
  const swBase = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.08, 0.4), new THREE.MeshStandardMaterial({ color: 0x334155 })); swBase.position.y = 0.04; swG.add(swBase);
  const blade = new THREE.Group(); blade.position.set(-0.35, 0.18, 0); swG.add(blade);
  const bladeM = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.03, 0.08), new THREE.MeshStandardMaterial({ color: 0xc9a14a, metalness: 0.9, roughness: 0.25 })); bladeM.position.x = 0.36; blade.add(bladeM);
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.07, 14, 10), new THREE.MeshStandardMaterial({ color: 0xdc2626 })); knob.position.set(0.75, 0, 0); blade.add(knob);
  const ammeter = dialMeter('A', 2, 'A', 0.5); ammeter.group.position.set(0.2, Y, -2.0); ammeter.group.scale.setScalar(0.9); world.add(ammeter.group);
  const voltmeter = dialMeter('V', 12, 'V', 2); voltmeter.group.position.set(0.6, Y, 1.7); voltmeter.group.scale.setScalar(0.9); world.add(voltmeter.group);
  const r1 = resistor(); const r2 = resistor(); world.add(r1.group, r2.group);
  const copper = new THREE.MeshStandardMaterial({ color: 0xb87333, metalness: 0.85, roughness: 0.3 });
  const wireGroup = new THREE.Group(); world.add(wireGroup);
  const carriers = new THREE.InstancedMesh(new THREE.SphereGeometry(0.045, 10, 8), new THREE.MeshBasicMaterial({ color: 0x60d4ff, toneMapped: false }), 240);
  carriers.count = 0; world.add(carriers);
  const lbl = { r1: S.label(), r2: S.label(), sw: S.label() };

  const panel = createPanel(stage, { title: 'Circuit' });
  panel.slider({ label: 'Battery', min: 1, max: 8, step: 1, value: cells, format: (v) => `${v} cell${v > 1 ? 's' : ''} · ${fmt(v * CELL, 1)} V`, onChange: (v) => { cells = v; } });
  const a1 = panel.slider({ label: 'R₁', min: 0, max: VALUES.length - 1, step: 1, value: R1i, format: (v) => `${VALUES[v]} Ω`, onChange: (v) => { R1i = v; } });
  const a2 = panel.slider({ label: 'R₂', min: 0, max: VALUES.length - 1, step: 1, value: R2i, format: (v) => `${VALUES[v]} Ω`, onChange: (v) => { R2i = v; } });
  panel.chips({ label: 'Wiring', options: [{ value: 'series', label: 'Series' }, { value: 'parallel', label: 'Parallel' }], value: 'series', onChange: (v) => { parallel = v === 'parallel'; build(); } });
  const swT = panel.toggle({ label: 'Switch closed', value: false, onChange: (v) => { closed = v; } });
  panel.toggle({ label: 'Show electrons (opposite way)', value: false, onChange: (v) => { electrons = v; } });
  const st = panel.stats([{ key: 'R', label: 'Total resistance' }, { key: 'I', label: 'Current (ammeter)' }, { key: 'V1', label: 'Voltage across R₁' }, { key: 'P', label: 'Power' }]);
  panel.info('In series the same current passes through both and the voltages add up; in parallel each branch gets the full voltage and the currents add up. Conventional current flows from + to −; the electrons actually drift the other way.');
  S.tappable(swG, () => { closed = !closed; swT.set(closed); });
  S.tappable(r1.group, () => { R1i = (R1i + 1) % VALUES.length; a1.set(R1i); });
  S.tappable(r2.group, () => { R2i = (R2i + 1) % VALUES.length; a2.set(R2i); });

  // wire routes: the main loop and, in parallel, two branches between the nodes
  let paths = [];
  const P = (x, z) => new THREE.Vector3(x, Y + 0.05, z);
  function polyLen(pts) { let L = 0; for (let i = 1; i < pts.length; i++) L += pts[i].distanceTo(pts[i - 1]); return L; }
  const segs = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.03, 0.03, 1, 8), copper, 64); segs.castShadow = true; world.add(segs);
  const joints = new THREE.InstancedMesh(new THREE.SphereGeometry(0.04, 10, 8), copper, 64); world.add(joints);
  let ns = 0;
  const q = new THREE.Quaternion(); const up = new THREE.Vector3(0, 1, 0); const sc = new THREE.Vector3(); const mm = new THREE.Matrix4();
  function tube(pts) {
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1]; const b = pts[i]; const d = new THREE.Vector3().subVectors(b, a); const L = d.length();
      q.setFromUnitVectors(up, d.clone().normalize());
      segs.setMatrixAt(ns, mm.compose(a.clone().addScaledVector(d, 0.5), q, sc.set(1, L, 1)));
      joints.setMatrixAt(ns, mm.makeTranslation(b.x, b.y, b.z)); ns++;
    }
    segs.count = joints.count = ns; segs.instanceMatrix.needsUpdate = joints.instanceMatrix.needsUpdate = true;
  }
  function build() {
    while (wireGroup.children.length) { const c = wireGroup.children.pop(); c.geometry.dispose(); }
    ns = 0;
    if (!parallel) {
      r1.group.position.set(2.6, Y + 0.12, -0.9); r2.group.position.set(2.6, Y + 0.12, 0.9);
      const loop = [P(-3.4, -1.65), P(-3.4, -2.0), P(-2.05, -2.0), P(-1.35, -2.0), P(-0.25, -2.0), P(0.65, -2.0), P(2.6, -2.0), P(2.6, -1.5), P(2.6, -0.3), P(2.6, 0.3), P(2.6, 1.5), P(2.6, 2.2), P(-3.4, 2.2), P(-3.4, 1.65)];
      tube(loop);
      paths = [{ pts: loop, which: 0 }];
    } else {
      r1.group.position.set(1.9, Y + 0.12, 0); r2.group.position.set(3.3, Y + 0.12, 0);
      const main1 = [P(-3.4, -1.65), P(-3.4, -2.0), P(-2.05, -2.0), P(-1.35, -2.0), P(-0.25, -2.0), P(0.65, -2.0), P(1.9, -2.0)];
      const b1 = [P(1.9, -2.0), P(1.9, -0.6), P(1.9, 0.6), P(1.9, 2.2)];
      const b2 = [P(1.9, -2.0), P(3.3, -2.0), P(3.3, -0.6), P(3.3, 0.6), P(3.3, 2.2), P(1.9, 2.2)];
      const main2 = [P(1.9, 2.2), P(-3.4, 2.2), P(-3.4, 1.65)];
      [main1, b1, b2, main2].forEach(tube);
      paths = [{ pts: main1, which: 0 }, { pts: b1, which: 1 }, { pts: b2, which: 2 }, { pts: main2, which: 0 }];
    }
    paths.forEach((p) => { p.len = polyLen(p.pts); p.phase = 0; });
    const vleads = [[P(r1.group.position.x, r1.group.position.z - 0.6), P(0.4, 1.45)], [P(r1.group.position.x, r1.group.position.z + 0.6), P(0.85, 1.45)]];
    vleads.forEach(([a, b], i) => { const c = new THREE.CatmullRomCurve3([a.clone().setY(Y + 0.1), a.clone().lerp(b, 0.5).setY(Y + 0.55), b.clone().setY(Y + 0.25)]); const m = new THREE.Mesh(new THREE.TubeGeometry(c, 24, 0.018, 6), new THREE.MeshStandardMaterial({ color: i ? 0x111827 : 0xdc2626, roughness: 0.5 })); wireGroup.add(m); });
  }
  build();
  function solve() {
    const R1 = VALUES[R1i]; const R2 = VALUES[R2i]; const V = cells * CELL;
    Rt = parallel ? R1 * R2 / (R1 + R2) : R1 + R2;
    I = closed ? V / Rt : 0;
    if (parallel) { I1 = closed ? V / R1 : 0; I2 = closed ? V / R2 : 0; V1 = V2 = closed ? V : 0; } else { I1 = I2 = I; V1 = I * R1; V2 = I * R2; }
  }
  const at = (pts, s) => { for (let i = 1; i < pts.length; i++) { const L = pts[i].distanceTo(pts[i - 1]); if (s <= L) return pts[i - 1].clone().lerp(pts[i], s / L); s -= L; } return pts[pts.length - 1].clone(); };
  const m4 = new THREE.Matrix4(); const v3 = new THREE.Vector3();
  engine.setUpdate((dt) => {
    controls.update(dt);
    solve();
    cellMeshes.forEach((c, i) => { c.visible = i < cells; });
    blade.rotation.z += ((closed ? 0 : 0.9) - blade.rotation.z) * (1 - Math.exp(-dt * 10));
    r1.set(VALUES[R1i]); r2.set(VALUES[R2i]);
    ammeter.set(I); voltmeter.set(V1);
    flowK += ((closed ? 1 : 0) - flowK) * (1 - Math.exp(-dt * 4));
    let n = 0; const dir = electrons ? -1 : 1;
    for (const p of paths) {
      const cur = p.which === 0 ? I : p.which === 1 ? I1 : I2;
      p.phase = (p.phase + dir * cur * 0.9 * dt * flowK) % 0.32;
      const count = Math.floor(p.len / 0.32);
      for (let k = 0; k < count && n < 240; k++) { let s = k * 0.32 + p.phase; if (s < 0) s += 0.32; if (s > p.len) continue; m4.makeTranslation(...at(p.pts, s).toArray()); carriers.setMatrixAt(n++, m4); }
    }
    carriers.count = flowK > 0.05 ? n : 0; carriers.instanceMatrix.needsUpdate = true;
    carriers.material.color.setHex(electrons ? 0x93c5fd : 0xfbbf24);
    lbl.r1.el.textContent = `R₁ ${VALUES[R1i]} Ω${closed ? ` · ${fmt(I1, 2)} A` : ''}`; lbl.r1.at(v3.set(r1.group.position.x + 0.9, 0.8 + 0.55, r1.group.position.z));
    lbl.r2.el.textContent = `R₂ ${VALUES[R2i]} Ω${closed ? ` · ${fmt(I2, 2)} A` : ''}`; lbl.r2.at(v3.set(r2.group.position.x + 0.9, 0.8 + 0.55, r2.group.position.z));
    lbl.sw.el.textContent = closed ? 'switch closed' : 'switch open · tap'; lbl.sw.at(v3.set(-1.7, 0.8 + 0.7, -2.0));
    st.R.set(`${fmt(Rt, 2)} Ω`); st.I.set(`${fmt(I, 3)} A`); st.V1.set(`${fmt(V1, 2)} V`); st.P.set(`${fmt(I * cells * CELL, 2)} W`);
    badge.set(!closed ? 'Tap the switch to close the circuit' : parallel ? `Parallel: ${fmt(I1, 2)} A + ${fmt(I2, 2)} A = ${fmt(I, 2)} A from the battery` : `Series: the same ${fmt(I, 3)} A everywhere; ${fmt(V1, 2)} V + ${fmt(V2, 2)} V = ${fmt(cells * CELL, 1)} V`);
  });
  engine.start();

  stage.__circuit = { close: (v) => { closed = v; swT.set(v); }, parallel: (v) => { parallel = v; build(); }, state: () => ({ I, I1, I2, V1, V2, Rt }) };
  return { dispose() { panel.dispose(); hud.dispose(); Object.values(lbl).forEach((l) => l.remove()); S.dispose(); } };
}
