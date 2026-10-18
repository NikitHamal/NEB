// Physics practicals, rebuilt at real proportions (1 unit = 10 cm) on the bench (y = BENCH_Y).
// Each builder returns nothing; it adds meshes to `g` and pushes animation callbacks to `anim`.
import { THREE } from './engine.js';
import { M, box, cyl, sphere, rot, tag, retortStand, clamp, meterRule, analogMeter, wire, cell, resistor, rheostat, stopwatch, slottedWeights, tuningFork, glassVessel, thermometer, bunsen, tripodWithGauze, scaleTexture } from './lab3d-kit.js';
import { BENCH_Y as Y } from './lab3d-room.js';

const D2R = Math.PI / 180;

/** A bare string or thread: a very thin cylinder from a to b. */
function thread(a, b, color = 0xf5f5f0, r = 0.008) {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b);
  const len = A.distanceTo(B);
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, 6), M.plastic(color));
  m.position.copy(A).lerp(B, 0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.clone().sub(A).normalize());
  return m;
}

// ---- simple pendulum: hung off the bench edge, timed with a stopwatch ---------------------
export function pendulum(g, anim, s) {
  const stand = retortStand({ rod: 6.2 }); stand.position.set(0.4, Y, 2.0); g.add(stand);
  const rodX = 0.4 + stand.userData.rodX;
  // clamp arm reaches out past the bench edge; a split cork grips the thread
  g.add(box(0.12, 0.12, 0.12, M.castIron(), [rodX, Y + 6.0, 2.0], 0.01));
  g.add(rot(cyl(0.022, 0.022, 2.0, M.steel(), [rodX, Y + 6.0, 3.0], 12), 'x', Math.PI / 2));
  g.add(box(0.22, 0.26, 0.16, M.paint(0xc8a46a), [rodX, Y + 5.92, 3.95], 0.03));
  const pivotY = Y + 5.8;
  const L = s.lengthCm / 10;
  const p = new THREE.Group(); p.position.set(rodX, pivotY, 3.95); g.add(p);
  p.add(thread([0, 0, 0], [0, -L + 0.18, 0]));
  p.add(sphere(0.18, M.brass(), [0, -L, 0], 40));
  p.add(cyl(0.02, 0.02, 0.08, M.brass(), [0, -L + 0.2, 0], 8));
  // a vertical metre rule clamped beside it, and a stopwatch on the bench
  const rule = meterRule(1); rule.rotation.set(Math.PI / 2, 0, Math.PI / 2); rule.position.set(rodX - 0.75, pivotY - 5, 3.8); g.add(rule);
  const sw = stopwatch(); sw.position.set(-2.6, Y + 0.3, 2.2); sw.rotation.x = -0.9; g.add(sw);
  tag(g, `L = ${s.lengthCm.toFixed(0)} cm`, [rodX, pivotY - L / 2, 3.95], { offset: [1.4, 0.2, 0] });
  const amp = s.amplitude * D2R; const w = Math.sqrt(9.81 / (s.lengthCm / 100));
  let clock = 0;
  anim.push((dt, t, st) => {
    p.rotation.z = amp * Math.sin(t * w);
    if (st.running) clock += dt;
    sw.userData.hand.rotation.z = -(clock % 60) / 60 * Math.PI * 2;
  });
}

// ---- parallelogram of forces: a Gravesand board with two pulleys and three hangers ------
export function forceboard(g, anim, s) {
  const P = s.pN, Q = s.qN, th = s.angleDeg * D2R;
  const R = Math.sqrt(P * P + Q * Q + 2 * P * Q * Math.cos(th));
  const a1 = Math.atan2(Q * Math.sin(th), P + Q * Math.cos(th)); // P's angle from the resultant
  const a2 = th - a1;
  const board = new THREE.Group(); board.position.set(0, Y, -0.6); g.add(board);
  board.add(box(0.5, 0.12, 1.2, M.castIron(), [-2.4, 0.06, 0]), box(0.5, 0.12, 1.2, M.castIron(), [2.4, 0.06, 0]));
  board.add(box(6.4, 5.0, 0.12, M.wood('oak'), [0, 3.2, 0]));
  const paper = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 3.0), M.paint(0xfbfaf6)); paper.position.set(0, 3.0, 0.07); board.add(paper);
  const knot = new THREE.Vector3(0, 2.4, 0.12);
  const len = 2.3;
  const dirP = new THREE.Vector3(-Math.sin(a1), Math.cos(a1), 0), dirQ = new THREE.Vector3(Math.sin(a2), Math.cos(a2), 0);
  const pulleyP = knot.clone().addScaledVector(dirP, len), pulleyQ = knot.clone().addScaledVector(dirQ, len);
  for (const pp of [pulleyP, pulleyQ]) {
    board.add(rot(cyl(0.22, 0.22, 0.07, M.brass(), [pp.x, pp.y, 0.2], 28), 'x', Math.PI / 2));
    board.add(rot(cyl(0.03, 0.03, 0.3, M.steel(), [pp.x, pp.y, 0.08], 8), 'x', Math.PI / 2));
  }
  board.add(thread(knot.toArray(), pulleyP.toArray()), thread(knot.toArray(), pulleyQ.toArray()));
  // strings over the pulleys down to the hangers; weights scale with the force
  const hang = (pp, n, side) => {
    const x = pp.x + side * 0.22; const bottom = Math.min(pp.y - 1.0, 1.3);
    board.add(thread([x, pp.y, 0.2], [x, bottom, 0.2]));
    const w = slottedWeights(Math.max(1, Math.round(n))); w.position.set(x, bottom - 0.62 - n * 0.06, 0.2); board.add(w);
  };
  hang(pulleyP, P, -1); hang(pulleyQ, Q, 1);
  board.add(thread(knot.toArray(), [0, 1.3, 0.12]));
  const wR = slottedWeights(Math.max(1, Math.round(R))); wR.position.set(0, 1.3 - 0.62 - R * 0.06, 0.12); board.add(wR);
  board.add(sphere(0.05, M.paint(0x111827), knot.toArray(), 12));
  // the construction drawn in pencil on the paper: P, Q, and the parallelogram's diagonal
  const scale = 0.32;
  const pencil = (a, b, col) => { const t = thread([a.x, a.y, 0.08], [b.x, b.y, 0.08], col, 0.012); board.add(t); };
  const pEnd = knot.clone().addScaledVector(dirP, P * scale), qEnd = knot.clone().addScaledVector(dirQ, Q * scale);
  const rEnd = knot.clone().add(new THREE.Vector3(0, R * scale, 0));
  pencil(knot, pEnd, 0x2563eb); pencil(knot, qEnd, 0x16a34a); pencil(knot, rEnd, 0xd97706);
  pencil(pEnd, rEnd, 0x9ca3af); pencil(qEnd, rEnd, 0x9ca3af);
  tag(board, `P = ${P.toFixed(1)} N`, pEnd.toArray(), { offset: [-0.6, 0.3, 0.1] });
  tag(board, `Q = ${Q.toFixed(1)} N`, qEnd.toArray(), { offset: [0.6, 0.3, 0.1] });
  tag(board, `R = ${R.toFixed(2)} N`, rEnd.toArray(), { offset: [0, 0.45, 0.1] });
}

// ---- angle of repose on a hinged incline ---------------------------------------------------
export function incline(g, anim, s) {
  const th = s.angleDeg * D2R;
  const plane = new THREE.Group(); plane.position.set(-2.4, Y, 0); g.add(plane);
  plane.add(box(6.0, 0.12, 2.0, M.wood('pale'), [3.0, 0.06, 0]));
  const hinged = new THREE.Group(); plane.add(hinged);
  hinged.rotation.z = th;
  hinged.add(box(5.6, 0.1, 1.8, M.wood('oak'), [2.8, 0.17, 0]));
  hinged.add(box(5.6, 0.012, 1.6, M.paint(0xe5e7eb), [2.8, 0.226, 0]));
  hinged.add(rot(cyl(0.06, 0.06, 2.0, M.steel(), [0, 0.12, 0], 12), 'x', Math.PI / 2));
  // a quadrant protractor at the hinge reads the angle
  const quad = new THREE.Mesh(new THREE.RingGeometry(1.2, 1.5, 48, 1, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xfef3c7, transparent: true, opacity: 0.85, side: THREE.DoubleSide }));
  quad.position.set(0, 0.14, 1.02); plane.add(quad);
  for (let k = 0; k <= 9; k++) { const a = k * 10 * D2R; plane.add(thread([Math.cos(a) * 1.2, 0.14 + Math.sin(a) * 1.2, 1.03], [Math.cos(a) * 1.5, 0.14 + Math.sin(a) * 1.5, 1.03], 0x92400e, 0.006)); }
  // the block with a hook; it slides when tan(theta) beats the static coefficient
  const block = new THREE.Group(); hinged.add(block);
  block.add(box(0.9, 0.45, 0.7, M.wood('teak'), [0, 0.225, 0], 0.03));
  block.add(rot(new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.015, 8, 16), M.steel()), 'y', Math.PI / 2));
  block.children[1].position.set(-0.5, 0.25, 0);
  block.position.set(4.2, 0.23, 0);
  const slides = Math.tan(th) >= s.muStatic;
  tag(g, `θ = ${s.angleDeg.toFixed(1)}°  ·  ${slides ? 'block slides: μ ≤ tan θ' : 'block holds: μ > tan θ'}`, [-1.2, Y + 1.2, 1.0], { offset: [0.6, 1.6, 0] });
  let x = 4.2;
  anim.push((dt) => {
    if (!slides) return;
    x -= dt * (0.6 + (Math.tan(th) - s.muStatic) * 3);
    if (x < 0.8) x = 4.2;
    block.position.x = x;
  });
}

// ---- Hooke's law: a spring, a pointer and a vertical scale ---------------------------------
function helix(top, bottom, radius, coils, wireR = 0.018) {
  const pts = []; const H = top - bottom;
  const n = coils * 18;
  for (let i = 0; i <= n; i++) { const t = i / n; const a = t * coils * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(a) * radius, top - H * t, Math.sin(a) * radius)); }
  return new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), n, wireR, 6, false), M.steel());
}
export function spring(g, anim, s) {
  const stand = retortStand({ rod: 6.0 }); stand.position.set(0, Y, -0.6); g.add(stand);
  const rodX = stand.userData.rodX;
  const topY = Y + 5.7;
  g.add(box(0.12, 0.12, 0.12, M.castIron(), [rodX, topY, -0.6], 0.01));
  g.add(rot(cyl(0.022, 0.022, 1.4, M.steel(), [rodX + 0.7, topY, -0.6], 12), 'z', Math.PI / 2));
  const F = s.loadG / 1000 * 9.81; const ext = (F / s.kNm) * 10; // units
  const natural = 1.6;
  const sp = new THREE.Group(); sp.position.set(rodX + 1.3, 0, -0.6); g.add(sp);
  let current = ext; let v = 0;
  let coil = helix(topY, topY - natural - current, 0.16, 16);
  sp.add(coil);
  const hanger = new THREE.Group(); sp.add(hanger);
  const pointer = box(0.5, 0.025, 0.04, M.paint(0xdc2626), [0.25, 0, 0]); hanger.add(pointer);
  const weights = slottedWeights(Math.max(1, Math.round(s.loadG / 50))); weights.position.y = -0.75 - Math.round(s.loadG / 50) * 0.065; hanger.add(weights);
  // the scale: printed in cm, behind the pointer
  const scale = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 4.0), new THREE.MeshStandardMaterial({ map: scaleTexture({ length: 40, major: 10, minor: 1, unit: 'cm', w: 2048, h: 140 }), roughness: 0.6 }));
  scale.material.map = scale.material.map.clone(); scale.material.map.userData = { owned: true }; scale.material.map.needsUpdate = true; scale.material.map.center.set(0.5, 0.5); scale.material.map.rotation = -Math.PI / 2;
  scale.position.set(rodX + 1.95, topY - natural - 2.0, -0.62); g.add(scale);
  tag(g, `extension ${(ext * 10).toFixed(1)} cm`, [rodX + 1.55, topY - natural - ext, -0.6], { offset: [1.4, 0.2, 0] });
  // released from rest it bounces, then damps to the new equilibrium
  current = 0;
  anim.push((dt) => {
    if (Math.abs(current - ext) < 0.0005 && Math.abs(v) < 0.001) return; // at rest: nothing to redraw
    const a = -40 * (current - ext) - 2.4 * v; v += a * dt; current += v * dt;
    sp.remove(coil); coil.geometry.dispose();
    coil = helix(topY, topY - natural - current, 0.16, 16); sp.add(coil);
    hanger.position.y = topY - natural - current;
  });
}

// ---- method of mixtures calorimetry -------------------------------------------------------
export function calorimeter(g, anim, s) {
  // the copper calorimeter in its wooden lagging box, stirrer and thermometer through the lid
  const lag = new THREE.Group(); lag.position.set(1.4, Y, 0); g.add(lag);
  lag.add(box(1.5, 1.2, 1.5, M.wood('oak'), [0, 0.6, 0], 0.04));
  const cu = glassVessel('calorimeter'); cu.children[0].material = M.copper(); cu.position.y = 0.22; lag.add(cu);
  const mix = (s.metalMass * 0.385 * s.metalTemp + s.waterMass * 4.18 * s.waterTemp) / (s.metalMass * 0.385 + s.waterMass * 4.18);
  const water = glassVessel('calorimeter', { fill: 0.7, color: 0xbfe3ff, opacity: 0.6 }); water.children[0].visible = false; water.position.y = 0.22; lag.add(water);
  lag.add(cyl(0.48, 0.48, 0.05, M.wood('teak'), [0, 1.24, 0], 32));
  const th = thermometer(mix, { height: 3.0 }); th.position.set(0.18, 0.5, 0.1); lag.add(th);
  lag.add(cyl(0.012, 0.012, 2.0, M.copper(), [-0.18, 1.3, 0], 8));
  lag.add(rot(new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.012, 6, 24), M.copper()), 'x', Math.PI / 2)); lag.children[lag.children.length - 1].position.set(-0.18, 0.5, 0);
  // the steam heater: a boiling tube with the metal shot, on a tripod over a burner
  const heater = new THREE.Group(); heater.position.set(-2.2, Y, 0); g.add(heater);
  const b = bunsen(); heater.add(b); heater.add(tripodWithGauze());
  const beaker = glassVessel('beaker250', { fill: 0.75, color: 0xd6ecff, opacity: 0.5 }); beaker.position.y = 1.47; heater.add(beaker);
  const tube = glassVessel('boilingTube', { fill: 0.35, color: 0xb87333, opacity: 0.95 }); tube.position.set(0, 1.6, 0); heater.add(tube);
  tag(g, `metal ${s.metalTemp.toFixed(0)} °C`, [-2.2, Y + 2.9, 0], { offset: [0, 0.6, 0] });
  tag(g, `mixture ≈ ${mix.toFixed(1)} °C`, [1.6, Y + 3.3, 0.1], { offset: [0.9, 0.3, 0] });
  const stirrer = lag.children[lag.children.length - 1];
  anim.push((dt, t) => { stirrer.position.y = 0.5 + Math.abs(Math.sin(t * 2.4)) * 0.4; b.userData.flame.scale.setScalar(1 + Math.sin(t * 17) * 0.05); });
}

// ---- resonance air column ------------------------------------------------------------------
export function resonance(g, anim, s) {
  const stand = retortStand({ rod: 7.0 }); stand.position.set(-0.6, Y, -0.4); g.add(stand);
  const x = 0.4; const tubeH = 6.0;
  g.add(cyl(0.2, 0.2, tubeH, M.glass(), [x, Y + 0.6 + tubeH / 2, -0.4], 32));
  clamp(g, -0.6 + stand.userData.rodX, Y + 2.0, x - 0.2, 0.2); clamp(g, -0.6 + stand.userData.rodX, Y + 5.6, x - 0.2, 0.2);
  const air = s.lengthCm / 10;
  const waterTop = Y + 0.6 + tubeH - air;
  const waterH = waterTop - (Y + 0.6);
  g.add(cyl(0.185, 0.185, waterH, M.liquid(0x7cc4ff, 0.6), [x, Y + 0.6 + waterH / 2, -0.4], 28));
  // reservoir on a slider, connected by rubber tubing
  g.add(glassVessel('beaker100', { fill: 0.6, color: 0x7cc4ff, opacity: 0.6 })); g.children[g.children.length - 1].position.set(2.0, Y + waterH * 0.6, -0.4);
  g.add(wire([x, Y + 0.65, -0.4], [2.0, Y + waterH * 0.6 + 0.05, -0.4], 0x8a2d2d, 0.5, 0.04));
  // a meter rule along the tube, and the fork struck above the mouth
  const rule = meterRule(0.6); rule.rotation.set(Math.PI / 2, 0, Math.PI / 2); rule.position.set(x + 0.45, Y + 0.6 + tubeH / 2, -0.25); g.add(rule);
  const fork = tuningFork(); fork.position.set(x, Y + 0.6 + tubeH + 0.45, -0.4); fork.rotation.z = Math.PI / 2; fork.scale.setScalar(0.8); g.add(fork);
  // the standing wave in the column: a faint glowing envelope, antinode at the mouth, node at the water
  const env = new THREE.Group(); g.add(env);
  const n = 12;
  for (let k = 0; k < n; k++) {
    const y = waterTop + (air * k) / (n - 1);
    const a = Math.sin((Math.PI / 2) * (k / (n - 1)));
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.06 + a * 0.1, 0.008, 6, 24), M.flame(0x7dd3fc));
    ring.rotation.x = Math.PI / 2; ring.position.set(x, y, -0.4); env.add(ring);
  }
  tag(g, `air column l = ${s.lengthCm.toFixed(1)} cm`, [x, waterTop + air / 2, -0.4], { offset: [-1.6, 0.2, 0] });
  anim.push((dt, t) => {
    fork.rotation.x = Math.sin(t * 90) * 0.01;
    env.children.forEach((r, k) => { r.scale.setScalar(0.7 + 0.3 * Math.abs(Math.sin(t * 6))); r.material.opacity = 0.25 + 0.3 * (k / n); });
  });
}

// ---- sonometer -----------------------------------------------------------------------------
export function sonometer(g, anim, s) {
  const boxG = new THREE.Group(); boxG.position.set(0, Y, 0); g.add(boxG);
  boxG.add(box(11.0, 0.8, 1.4, M.wood('oak'), [0, 0.4, 0], 0.03));
  for (const x of [-2.4, 2.4]) { const hole = new THREE.Mesh(new THREE.CircleGeometry(0.22, 24), M.ink(0x1b120a)); hole.rotation.x = -Math.PI / 2; hole.position.set(x, 0.805, 0); boxG.add(hole); }
  const wy = 1.25;
  // pegs at the left, a pulley at the right, weights hanging off the end
  boxG.add(box(0.2, 0.5, 0.2, M.steel(), [-5.3, 1.05, 0]));
  boxG.add(rot(cyl(0.25, 0.25, 0.1, M.brass(), [5.65, wy - 0.25, 0], 28), 'x', Math.PI / 2));
  boxG.add(box(0.3, 0.4, 0.3, M.steel(), [5.5, 0.95, 0]));
  boxG.add(thread([-5.3, wy, 0], [5.65, wy, 0], 0xd7dde4, 0.012));
  boxG.add(thread([5.9, wy - 0.25, 0], [5.9, -0.9, 0], 0xd7dde4, 0.012));
  const w = slottedWeights(Math.max(1, Math.round(s.tensionN / 10))); w.position.set(5.9, -1.5 - Math.round(s.tensionN / 10) * 0.065, 0); boxG.add(w);
  // two knife-edge bridges set to the vibrating length
  const L = s.lengthCm / 10;
  for (const x of [-L / 2, L / 2]) {
    const br = new THREE.Mesh(new THREE.CylinderGeometry(0.0, 0.14, 0.44, 3), M.brass()); br.rotation.set(0, 0, 0); br.position.set(x, 1.02, 0); boxG.add(br);
  }
  // the vibrating segment, drawn live as a standing wave, and a paper rider on it
  const segN = 48; const pts = new Float32Array((segN + 1) * 3);
  const geoW = new THREE.BufferGeometry(); geoW.setAttribute('position', new THREE.BufferAttribute(pts, 3));
  const lineW = new THREE.Line(geoW, new THREE.LineBasicMaterial({ color: 0xffffff })); boxG.add(lineW);
  const rider = box(0.12, 0.1, 0.02, M.paint(0xfde68a), [0, wy + 0.06, 0]); rider.rotation.z = Math.PI / 4; boxG.add(rider);
  const fork = tuningFork(); fork.position.set(-3.6, 0.9, 0.5); fork.scale.setScalar(0.7); boxG.add(fork);
  tag(g, `l = ${s.lengthCm.toFixed(0)} cm · T = ${s.tensionN.toFixed(0)} N`, [0, Y + 1.3, 0], { offset: [0, 1.2, 0] });
  anim.push((dt, t) => {
    const amp = 0.07 * Math.sin(t * 60);
    for (let i = 0; i <= segN; i++) { const u = i / segN; pts[i * 3] = -L / 2 + u * L; pts[i * 3 + 1] = wy + Math.sin(Math.PI * u) * amp; pts[i * 3 + 2] = 0; }
    geoW.attributes.position.needsUpdate = true;
    rider.position.y = wy + 0.07 + Math.abs(amp) * 1.4;
  });
}

// ---- circuits on a board: Ohm's law, meter bridge, potentiometer, galvanometer -------------
function board(g, w = 8.0, d = 3.6) {
  const b = box(w, 0.12, d, M.wood('pale'), [0, Y + 0.06, 0], 0.03); g.add(b); return Y + 0.12;
}
export function circuit(g, anim, s) {
  const top = board(g);
  const I = s.voltage / s.resistance;
  const A = analogMeter('A', 1, 'ampere'); A.position.set(-2.6, top, -0.9); g.add(A); A.userData.setValue(I);
  const V = analogMeter('V', 5, 'volt'); V.position.set(1.0, top, -0.9); g.add(V); V.userData.setValue(s.voltage);
  // the resistance wire stretched along a metre-rule section, the cells, a key and a rheostat
  const rule = meterRule(0.6); rule.position.set(1.0, top, 0.9); g.add(rule);
  g.add(thread([1.0 - 2.9, top + 0.08, 0.9], [1.0 - 2.9 + s.lengthCm / 10, top + 0.08, 0.9], 0xc0a050, 0.01));
  const c1 = cell(); c1.position.set(-3.4, top, 1.0); g.add(c1); const c2 = cell(); c2.position.set(-3.0, top, 1.0); g.add(c2);
  const rh = rheostat(); rh.position.set(-1.0, top, 0.6); rh.scale.setScalar(0.7); g.add(rh);
  const wires = [
    [[-3.25, top + 0.62, 1.0], [-2.9, top + 0.05, -0.65], 0xd32f2f], [[-2.3, top + 0.05, -0.65], [-1.6, top + 0.35, 0.6], 0x111827],
    [[-0.4, top + 0.35, 0.6], [-1.9, top + 0.1, 0.9], 0x111827], [[1.0 - 2.9 + s.lengthCm / 10, top + 0.1, 0.9], [-2.95, top + 0.62, 1.0], 0x111827],
    [[0.7, top + 0.05, -0.65], [-1.6, top + 0.1, 0.95], 0xd32f2f], [[1.3, top + 0.05, -0.65], [1.0 - 2.9 + s.lengthCm / 10, top + 0.1, 0.95], 0x111827],
  ];
  wires.forEach(([a, b, c]) => g.add(wire(a, b, c, 0.18)));
  tag(g, `I = ${I.toFixed(3)} A`, [-2.6, top + 0.9, -0.9], { offset: [0, 0.5, 0] });
  tag(g, `V = ${s.voltage.toFixed(2)} V`, [1.0, top + 0.9, -0.9], { offset: [0, 0.5, 0] });
  let k = 0; anim.push((dt) => { k = Math.min(1, k + dt * 1.5); A.userData.setValue(I * k); V.userData.setValue(s.voltage * k); });
}

function bridgeBoard(g, wires = 1) {
  const top = board(g, 12.0, 3.6);
  const rule = meterRule(1); rule.position.set(0, top, 1.0); g.add(rule);
  for (let i = 0; i < wires; i++) g.add(thread([-5, top + 0.06, 0.55 - i * 0.35], [5, top + 0.06, 0.55 - i * 0.35], 0xc0a050, 0.01));
  // thick copper strips at the ends, with brass terminals
  g.add(box(0.3, 0.04, 1.8, M.copper(), [-5.2, top + 0.02, 0]), box(0.3, 0.04, 1.8, M.copper(), [5.2, top + 0.02, 0]));
  for (const x of [-5.2, 5.2]) for (const z of [-0.6, 0.3]) g.add(cyl(0.07, 0.07, 0.16, M.brass(), [x, top + 0.1, z], 12));
  return top;
}
function jockey(x, y, z) {
  const j = new THREE.Group(); j.position.set(x, y, z);
  j.add(cyl(0.06, 0.04, 0.5, M.plastic(0x111827), [0, 0.4, 0], 12));
  j.add(new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.16, 12).rotateX(Math.PI), M.brass())); j.children[1].position.y = 0.08;
  return j;
}
export function meterbridge(g, anim, s) {
  const top = bridgeBoard(g, 1);
  const x = -5 + s.balanceCm / 10;
  const rb = box(1.4, 0.5, 0.9, M.wood('teak'), [-3.2, top + 0.25, -0.9], 0.03); g.add(rb);
  for (let i = 0; i < 6; i++) g.add(cyl(0.05, 0.05, 0.08, M.brass(), [-3.7 + i * 0.2, top + 0.54, -0.9], 10));
  const R = resistor(); R.position.set(3.2, top, -0.9); g.add(R);
  const G = analogMeter('G', 30, 'centre zero'); G.position.set(0, top, -1.0); G.scale.setScalar(0.8); g.add(G);
  const jk = jockey(x, top + 0.07, 0.55); g.add(jk);
  g.add(wire([0, top + 0.1, -0.85], [x, top + 0.6, 0.55], 0x111827, 0.1));
  g.add(wire([-3.2, top + 0.5, -0.45], [-5.2, top + 0.15, -0.6], 0xd32f2f, 0.12), wire([3.6, top + 0.12, -0.9], [5.2, top + 0.15, -0.6], 0xd32f2f, 0.12));
  tag(g, `null point l = ${s.balanceCm.toFixed(1)} cm`, [x, top + 0.6, 0.55], { offset: [0, 0.7, 0] });
  anim.push((dt, t) => { jk.position.y = top + 0.07 + Math.max(0, Math.sin(t * 3)) * 0.06; G.userData.setValue(15 + Math.sin(t * 3) * 0.6); });
}
export function potentiometer(g, anim, s) {
  const top = bridgeBoard(g, 4);
  const x1 = -5 + s.l1 / 10, x2 = -5 + s.l2 / 10;
  const j1 = jockey(x1, top + 0.07, 0.55); g.add(j1);
  const j2 = jockey(x2, top + 0.07, 0.2); j2.children[0].material = M.plastic(0xb45309); g.add(j2);
  const c1 = cell(); c1.position.set(-3.2, top, -1.1); g.add(c1);
  const c2 = cell(); c2.position.set(-2.6, top, -1.1); c2.children[1].material = M.paint(0x2563eb); g.add(c2);
  const G = analogMeter('G', 30, 'centre zero'); G.position.set(0.8, top, -1.1); G.scale.setScalar(0.8); g.add(G);
  const drv = cell(); drv.position.set(3.4, top, -1.1); g.add(drv); const drv2 = cell(); drv2.position.set(3.8, top, -1.1); g.add(drv2);
  g.add(wire([3.6, top + 0.62, -1.1], [5.2, top + 0.15, -0.6], 0xd32f2f, 0.15), wire([-3.2, top + 0.62, -1.1], [-5.2, top + 0.15, -0.6], 0x111827, 0.15));
  g.add(wire([0.8, top + 0.1, -0.95], [x1, top + 0.6, 0.55], 0x111827, 0.1));
  tag(g, `E₁ balances at l₁ = ${s.l1.toFixed(1)} cm`, [x1, top + 0.6, 0.55], { offset: [-0.6, 0.8, 0] });
  tag(g, `E₂ at l₂ = ${s.l2.toFixed(1)} cm`, [x2, top + 0.6, 0.2], { offset: [0.8, 0.6, 0] });
  anim.push((dt, t) => { G.userData.setValue(15 + Math.sin(t * 2) * 0.4); });
}
export function galvanometer(g, anim, s) {
  const top = board(g, 8, 3.6);
  const G = analogMeter('G', 30, 'divisions'); G.position.set(0, top, -0.6); G.scale.setScalar(1.6); g.add(G);
  const rb = box(1.8, 0.55, 1.0, M.wood('teak'), [-2.6, top + 0.28, 0.6], 0.03); g.add(rb);
  for (let i = 0; i < 8; i++) g.add(cyl(0.05, 0.05, 0.08, M.brass(), [-3.3 + i * 0.2, top + 0.6, 0.6], 10));
  const c = cell(); c.position.set(2.6, top, 0.7); g.add(c);
  const rh = rheostat(); rh.position.set(1.2, top, 1.1); rh.scale.setScalar(0.6); g.add(rh);
  g.add(wire([-1.0, top + 0.2, -0.4], [-2.6, top + 0.56, 0.3], 0xd32f2f, 0.15), wire([1.0, top + 0.2, -0.4], [2.6, top + 0.62, 0.7], 0x111827, 0.15));
  tag(g, `${s.currentUa.toFixed(0)} µA → ${s.deflection.toFixed(0)} div`, [0, top + 1.6, -0.6], { offset: [0, 0.5, 0] });
  let k = 0; anim.push((dt) => { k = Math.min(1, k + dt); G.userData.setValue(s.deflection * k); });
}

// ---- optics: convex lens on an optical bench, candle and screen -------------------------
function upright(x, y, z, h = 1.6) {
  const u = new THREE.Group(); u.position.set(x, y, z);
  u.add(box(0.5, 0.1, 0.6, M.castIron(), [0, 0.05, 0], 0.02));
  u.add(cyl(0.035, 0.035, h, M.chrome(), [0, h / 2, 0], 12));
  return u;
}
export function optics(g, anim, s) {
  const f = s.focalCm, u = s.objectCm;
  const v = 1 / (1 / f - 1 / u);
  const k = 0.1; // world units per cm
  const benchTop = Y + 0.2;
  g.add(box(16, 0.2, 0.7, M.castIron(), [0, Y + 0.1, 0], 0.03));
  const rule = meterRule(1.5); rule.position.set(0, benchTop, 0.5); g.add(rule);
  const lensX = -1.5;
  // the lens: biconvex, lathe-turned glass in a ring holder
  const lu = upright(lensX, benchTop, 0); g.add(lu);
  const lensG = new THREE.LatheGeometry([0, 0.15, 0.35, 0.5, 0.62].map((r, i, a) => new THREE.Vector2(r, 0.09 * (1 - (r / 0.62) ** 2))).concat([0.62, 0.5, 0.35, 0.15, 0].map((r) => new THREE.Vector2(r, -0.09 * (1 - (r / 0.62) ** 2)))), 40);
  const lens = new THREE.Mesh(lensG, M.glassEdge()); lens.rotation.z = Math.PI / 2; lens.position.set(0, 1.9, 0); lu.add(lens);
  lu.add(rot(new THREE.Mesh(new THREE.TorusGeometry(0.64, 0.035, 8, 40), M.paint(0x111827)), 'y', Math.PI / 2)); lu.children[lu.children.length - 1].position.y = 1.9;
  // the object: a candle; the image: on a white screen at v, inverted
  const ox = lensX - u * k;
  const cu = upright(ox, benchTop, 0, 1.1); g.add(cu);
  cu.add(cyl(0.09, 0.09, 0.7, M.paint(0xfaf6ea), [0, 1.45, 0], 16));
  const fl = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.24, 12), M.flame(0xffb347)); fl.position.set(0, 1.94, 0); cu.add(fl);
  const real = v > 0;
  const sx = lensX + (real ? v : 30) * k;
  const su = upright(Math.min(7.6, sx), benchTop, 0, 1.2); g.add(su);
  su.add(box(0.04, 1.4, 1.4, M.paint(0xf8fafc), [0, 1.9, 0]));
  if (real && sx < 7.8) {
    const mag = v / u;
    const img = new THREE.Mesh(new THREE.ConeGeometry(0.06 * Math.min(3, mag), 0.24 * Math.min(3, mag), 12), M.flame(0xffb347));
    img.rotation.z = Math.PI; img.position.set(-0.03, 1.9 - 0.25 * Math.min(2, mag), 0); su.add(img);
  }
  // two principal rays from the flame tip, drawn as light
  const tip = new THREE.Vector3(ox, benchTop + 1.94 + 0.12, 0);
  const ray = (pts) => g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xffd166, transparent: true, opacity: 0.85 })));
  const lensC = new THREE.Vector3(lensX, benchTop + 1.9, 0);
  if (real) {
    const imgY = benchTop + 1.9 - (tip.y - lensC.y) * (v / u);
    const imgP = new THREE.Vector3(lensX + v * k, imgY, 0);
    ray([tip, new THREE.Vector3(lensX, tip.y, 0), imgP]);
    ray([tip, lensC, imgP]);
  }
  tag(g, `f = ${f} cm`, [lensX, benchTop + 2.6, 0], { offset: [0, 0.4, 0] });
  tag(g, real ? `u = ${u} cm · v = ${v.toFixed(1)} cm` : 'object inside f: virtual image', [0, benchTop + 3.2, 0], { offset: [0, 0.5, 0], leader: false });
  anim.push((dt, t) => { fl.scale.set(1 + Math.sin(t * 13) * 0.08, 1 + Math.sin(t * 9) * 0.1, 1); });
}

// ---- prism: angle of minimum deviation, white light and its spectrum --------------------
export function prism(g, anim, s) {
  const table = new THREE.Group(); table.position.set(0, Y, 0); g.add(table);
  table.add(cyl(1.6, 1.7, 0.18, M.castIron(), [0, 0.09, 0], 48));
  table.add(cyl(1.5, 1.5, 0.04, M.paint(0xf5f5f0), [0, 0.2, 0], 48));
  const A = s.angleA * D2R;
  const shape = new THREE.Shape(); const side = 1.4;
  const h = side * Math.cos(A / 2) ; const half = side * Math.sin(A / 2);
  shape.moveTo(0, h * 0.66); shape.lineTo(-half, -h * 0.34); shape.lineTo(half, -h * 0.34); shape.lineTo(0, h * 0.66);
  const pg = new THREE.ExtrudeGeometry(shape, { depth: 0.9, bevelEnabled: true, bevelSize: 0.015, bevelThickness: 0.015, bevelSegments: 2 });
  pg.rotateX(-Math.PI / 2); pg.translate(0, 0.22, 0.45);
  const pr = new THREE.Mesh(pg, M.glassEdge()); table.add(pr);
  // light source with a slit, the incoming beam, and the dispersed fan bent by D
  const lamp = new THREE.Group(); lamp.position.set(-4.4, 0.6, 1.4); table.add(lamp);
  lamp.add(box(0.8, 0.8, 0.8, M.paint(0x1f2937), [0, 0, 0], 0.05));
  lamp.add(box(0.04, 0.3, 0.06, M.glow(0xfff6d5, 2), [0.41, 0, 0]));
  const yb = 0.6;
  const entry = new THREE.Vector3(-half * 0.55, yb, 0.35);
  const beam = (pts, col, op = 0.9) => table.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: op, toneMapped: false })));
  beam([new THREE.Vector3(-4.0, yb, 1.4), entry], 0xfffbea);
  const exit = new THREE.Vector3(half * 0.55, yb, 0.35);
  beam([entry, exit], 0xfff7d6, 0.5);
  const D = s.devD * D2R;
  const cols = [0xe53935, 0xfb8c00, 0xfdd835, 0x43a047, 0x1e88e5, 0x8e24aa];
  cols.forEach((c, i) => {
    const d = D + (i - 2.5) * 0.012;
    const dir = new THREE.Vector3(Math.cos(-d + 0.25), 0, Math.sin(-d + 0.25) * -1);
    beam([exit, exit.clone().addScaledVector(dir, 4.5)], c);
  });
  tag(g, `A = ${s.angleA.toFixed(0)}° · D = ${s.devD.toFixed(1)}°`, [0, Y + 1.4, 0], { offset: [0, 0.9, 0] });
}
