// Chemistry practicals, rebuilt with lathe-turned glassware, real reagent colours and live
// chemistry (drops falling, effervescence, flames, silver mirrors, copper plating). Same
// contract as lab3d-physics.js: add meshes to `g`, push per-frame callbacks to `anim`.
import { THREE } from './engine.js';
import { M, box, cyl, sphere, rot, tag, glassVessel, testTube, burette, thermometer, retortStand, clamp, bunsen, tripodWithGauze, wire, analogMeter } from './lab3d-kit.js';
import { BENCH_Y as Y } from './lab3d-room.js';
import { ANION_RESULTS, CATION_COLORS, GAS_RESULTS, GROUP_RESULTS } from './lab3d-data.js';
import { indicatorColor, indicatorColorName, lassaigneResult, titrationStatus } from './lab3d-science.js';

const toHex = (c) => (typeof c === 'number' ? c : parseInt(String(c).replace('#', ''), 16));

/** Rising bubbles inside a vessel: a small pool of spheres recycled from the bottom. */
function bubbles(parent, { x = 0, z = 0, r = 0.25, y0 = 0.08, y1 = 0.8, n = 18, size = 0.022, rate = 1, color = 0xffffff }) {
  const mat = new THREE.MeshPhysicalMaterial({ color, transparent: true, opacity: 0.6, roughness: 0.05, clearcoat: 1, depthWrite: false });
  const geom = new THREE.SphereGeometry(size, 10, 8);
  const list = [];
  for (let i = 0; i < n; i++) {
    const b = new THREE.Mesh(geom, mat);
    b.userData = { a: Math.random() * Math.PI * 2, rr: Math.random() * r, sp: 0.3 + Math.random() * 0.5, y: y0 + Math.random() * (y1 - y0) };
    parent.add(b); list.push(b);
  }
  return (dt) => {
    for (const b of list) {
      const u = b.userData; u.y += dt * u.sp * rate;
      if (u.y > y1) { u.y = y0; u.a = Math.random() * Math.PI * 2; u.rr = Math.random() * r; }
      b.position.set(x + Math.cos(u.a) * u.rr, u.y, z + Math.sin(u.a) * u.rr);
      b.scale.setScalar(0.6 + (u.y - y0) / (y1 - y0) * 0.8);
    }
  };
}

/** A single drop that falls from (x, y0) to y1 and repeats while dripping. */
function dripper(g, x, y0, y1, color) {
  const d = sphere(0.035, M.liquid(color, 0.85), [x, y0, 0], 14); d.scale.y = 1.3; g.add(d);
  let y = y0;
  return (dt, on = true) => { if (!on) { d.visible = false; return; } d.visible = true; y -= dt * 3.2; if (y < y1) y = y0; d.position.y = y; };
}

function rack(g, n = 5, x = 0, z = 0) {
  const r = new THREE.Group(); r.position.set(x, Y, z); g.add(r);
  r.add(box(n * 0.62 + 0.4, 0.08, 0.7, M.wood('oak'), [0, 0.04, 0], 0.02));
  r.add(box(n * 0.62 + 0.4, 0.08, 0.7, M.wood('oak'), [0, 0.9, 0], 0.02));
  for (const sx of [-1, 1]) r.add(box(0.1, 0.9, 0.7, M.wood('oak'), [sx * (n * 0.31 + 0.15), 0.45, 0], 0.02));
  return r;
}

// ---- the apparatus bench: everything named, the focused piece lit -------------------------
export function apparatus(g, anim, s) {
  const items = {
    burette: () => { const st = retortStand({ rod: 6.6 }); st.position.set(-3.6, Y, -0.6); g.add(st); const b = burette({ fillMl: 42, color: 0xe0f2fe }); b.position.set(-3.6 + st.userData.rodX + 0.75, Y + 0.6, -0.6); g.add(b); clamp(g, -3.6 + st.userData.rodX, Y + 4.4, -3.6 + st.userData.rodX + 0.72, 0.07); return [-3.6 + st.userData.rodX + 0.75, Y + 3.5, -0.6]; },
    pipette: () => { const p = new THREE.Group(); p.position.set(-1.5, Y + 0.1, 0.6); p.rotation.z = Math.PI / 2 - 0.08; p.add(cyl(0.025, 0.025, 1.4, M.glass(), [0, 0.7, 0], 12)); p.add(sphere(0.16, M.glass(), [0, 1.55, 0], 24)); p.add(cyl(0.025, 0.012, 1.2, M.glass(), [0, 2.3, 0], 12)); g.add(p); return [-1.5, Y + 0.3, 0.6]; },
    flask: () => { const f = glassVessel('conical', { fill: 0.3, color: 0xfbcfe8, opacity: 0.8 }); f.position.set(0.4, Y, 0.2); g.add(f); return [0.4, Y + 0.9, 0.2]; },
    burner: () => { const b = bunsen(); b.position.set(2.6, Y, 0.1); g.add(b); anim.push((dt, t) => b.userData.flame.scale.set(1 + Math.sin(t * 15) * 0.05, 1 + Math.sin(t * 11) * 0.06, 1)); return [2.6, Y + 1.4, 0.1]; },
    beaker: () => { const b = glassVessel('beaker250', { fill: 0.55, color: 0xbfe3ff, opacity: 0.55 }); b.position.set(4.3, Y, 0.3); g.add(b); return [4.3, Y + 1.0, 0.3]; },
  };
  const names = { burette: '50 mL burette', pipette: '25 mL pipette', flask: 'conical flask', burner: 'Bunsen burner', beaker: '250 mL beaker' };
  let focusAt = null;
  for (const [k, make] of Object.entries(items)) {
    const at = make();
    if (k === s.focus) focusAt = at;
    tag(g, names[k], at, { offset: [0, k === s.focus ? 0.9 : 0.6, 0], scale: k === s.focus ? 0.24 : 0.16 });
  }
  if (focusAt) {
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.75, 0.86, 48), new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.85, side: THREE.DoubleSide }));
    ring.rotation.x = -Math.PI / 2; ring.position.set(focusAt[0], Y + 0.01, focusAt[2]); g.add(ring);
    anim.push((dt, t) => { const k = 1 + Math.sin(t * 3) * 0.06; ring.scale.set(k, k, 1); });
  }
}

// ---- separation: filtration, distillation, evaporation, chromatography --------------------
export function separation(g, anim, s) {
  if (s.method === 'filtration') {
    const st = retortStand({ rod: 5 }); st.position.set(-0.8, Y, -0.4); g.add(st);
    const funnel = glassVessel('funnel'); funnel.position.set(0, Y + 1.7, -0.4); g.add(funnel);
    const paper = new THREE.Mesh(new THREE.ConeGeometry(0.36, 0.5, 32, 1, true).rotateX(Math.PI), M.paint(0xf5f1e6)); paper.position.set(0, Y + 2.48, -0.4); g.add(paper);
    g.add(cyl(0.3, 0.3, 0.05, M.paint(0x8d6e63), [0, Y + 2.62, -0.4], 24));
    clamp(g, -0.8 + st.userData.rodX, Y + 2.4, -0.06, 0.08);
    const b = glassVessel('beaker250', { fill: 0.25, color: 0xd6ecff, opacity: 0.5 }); b.position.set(0, Y, -0.4); g.add(b);
    const drop = dripper(g, 0, Y + 1.65, Y + 0.3, 0xd6ecff); anim.push((dt) => drop(dt));
    tag(g, 'residue stays on the filter paper', [0, Y + 2.6, -0.4], { offset: [1.6, 0.4, 0] });
    tag(g, 'clear filtrate', [0, Y + 0.3, -0.4], { offset: [1.4, 0.2, 0] });
  } else if (s.method === 'distillation') {
    const st = retortStand({ rod: 5 }); st.position.set(-3.2, Y, -0.4); g.add(st);
    const tri = tripodWithGauze(); tri.position.set(-2.4, Y, -0.4); g.add(tri);
    const b = bunsen(); b.position.set(-2.4, Y, -0.4); g.add(b);
    const flask = glassVessel('roundBottom', { fill: 0.32, color: 0x9cc9ff, opacity: 0.55 }); flask.position.set(-2.4, Y + 1.47, -0.4); g.add(flask);
    const th = thermometer(s.temperature, { height: 1.6 }); th.position.set(-2.4, Y + 2.5, -0.4); g.add(th);
    // a Liebig condenser sloping down to the receiver, cooling water in and out
    const cond = new THREE.Group(); cond.position.set(-0.6, Y + 2.35, -0.4); cond.rotation.z = -0.28; g.add(cond);
    cond.add(rot(cyl(0.16, 0.16, 3.0, M.glass(), [0, 0, 0], 24), 'z', Math.PI / 2));
    cond.add(rot(cyl(0.05, 0.05, 3.6, M.glass(), [0, 0, 0], 16), 'z', Math.PI / 2));
    cond.add(rot(cyl(0.15, 0.15, 2.9, M.liquid(0xa5d8ff, 0.25), [0, 0, 0], 24), 'z', Math.PI / 2));
    g.add(wire([-1.2, Y + 2.2, -0.2], [-1.9, Y + 0.05, 1.0], 0x2563eb, 0.9, 0.03), wire([0.0, Y + 2.65, -0.2], [0.8, Y + 0.05, 1.1], 0x2563eb, 0.9, 0.03));
    const recv = glassVessel('conical', { fill: s.temperature >= 78 ? 0.32 : 0.06, color: 0xe8f4ff, opacity: 0.6 }); recv.position.set(1.5, Y, -0.4); g.add(recv);
    const boiling = s.temperature >= 78;
    const fizz = bubbles(flask, { r: 0.22, y0: 0.08, y1: 0.36, rate: boiling ? 1.6 : 0.2, n: boiling ? 22 : 6 });
    const drop = dripper(g, 1.5, Y + 1.5, Y + 0.45, 0xe8f4ff);
    anim.push((dt) => { fizz(dt); drop(dt, boiling); b.userData.flame.rotation.y += dt; });
    tag(g, `thermometer ${s.temperature.toFixed(0)} °C`, [-2.4, Y + 3.8, -0.4], { offset: [0, 0.5, 0] });
    tag(g, boiling ? 'distillate collects' : 'below the boiling point: nothing distils', [1.5, Y + 1.0, -0.4], { offset: [0.6, 0.9, 0] });
  } else if (s.method === 'chromatography') {
    const jar = glassVessel('gasJar', { fill: 0.06, color: 0xdbeafe, opacity: 0.5 }); jar.position.set(0, Y, 0); g.add(jar);
    g.add(cyl(0.42, 0.42, 0.06, M.glassEdge(), [0, Y + 1.56, 0], 32));
    const strip = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 1.4), new THREE.MeshStandardMaterial({ map: chromaTexture(), roughness: 0.9 })); strip.position.set(0, Y + 0.8, 0); g.add(strip);
    tag(g, 'the solvent front carries each dye a different distance', [0, Y + 1.4, 0], { offset: [1.8, 0.5, 0] });
  } else {
    const tri = tripodWithGauze(); tri.position.set(0, Y, 0); g.add(tri);
    const b = bunsen(); b.position.set(0, Y, 0); g.add(b);
    const dish = glassVessel('dish', { fill: 0.4, color: 0xd6ecff, opacity: 0.5 }); dish.children[0].material = M.porcelain(); dish.position.set(0, Y + 1.47, 0); g.add(dish);
    for (let i = 0; i < 26; i++) { const c = box(0.05, 0.05, 0.05, M.glassEdge(), [(Math.random() - 0.5) * 0.7, Y + 1.53, (Math.random() - 0.5) * 0.7]); c.rotation.set(Math.random(), Math.random(), Math.random()); g.add(c); }
    tag(g, 'crystals appear as the water evaporates', [0, Y + 1.6, 0], { offset: [1.6, 0.6, 0] });
    anim.push((dt, t) => b.userData.flame.scale.setScalar(1 + Math.sin(t * 14) * 0.05));
  }
}
function chromaTexture() {
  const c = document.createElement('canvas'); c.width = 128; c.height = 512; const x = c.getContext('2d');
  x.fillStyle = '#f6f3ea'; x.fillRect(0, 0, 128, 512);
  x.fillStyle = 'rgba(147,197,253,0.25)'; x.fillRect(0, 60, 128, 452);
  x.strokeStyle = '#94a3b8'; x.setLineDash([6, 6]); x.beginPath(); x.moveTo(0, 60); x.lineTo(128, 60); x.stroke();
  [['#ef4444', 140], ['#22c55e', 250], ['#3b82f6', 330], ['#a855f7', 420]].forEach(([col, y]) => { x.fillStyle = col; x.beginPath(); x.ellipse(64, y, 18, 12, 0, 0, Math.PI * 2); x.fill(); });
  const t = new THREE.CanvasTexture(c); if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace; t.userData.owned = true; return t;
}

// ---- titration (acid–base and KMnO4) ----------------------------------------------------
export function titration(g, anim, s, config) {
  const redox = config.title.includes('KMnO');
  const req = redox ? (s.fasM * 25.0) / (5 * s.kmno4M) : s.unknownM * 25.0 / 0.10;
  let flaskColor;
  if (redox) flaskColor = s.titreMl >= req ? 0xf0abfc : 0xfafaf7;
  else if (s.indicator === 'methyl') flaskColor = s.titreMl < req ? 0xfacc15 : s.titreMl - req > 0.3 ? 0xef4444 : 0xfb923c;
  else flaskColor = s.titreMl < req ? 0xfafaf7 : 0xf472b6;
  const st = retortStand({ rod: 7.2 }); st.position.set(-0.9, Y, -0.2); g.add(st);
  const bx = -0.9 + st.userData.rodX + 1.0;
  const filled = Math.max(2, 50 - s.titreMl);
  const bur = burette({ fillMl: filled, color: redox ? 0x7e22ce : 0xe0f2fe, opacity: redox ? 0.92 : 0.55 }); bur.position.set(bx, Y + 2.0, -0.2); g.add(bur);
  clamp(g, -0.9 + st.userData.rodX, Y + 5.6, bx - 0.07, 0.07);
  g.add(box(1.6, 0.03, 1.6, M.porcelain(), [bx, Y + 0.015, -0.2]));
  const flask = glassVessel('conical', { fill: 0.24, color: flaskColor, opacity: 0.8 }); flask.position.set(bx, Y + 0.03, -0.2); g.add(flask);
  const done = s.titreMl >= req - 0.05;
  const drop = dripper(g, bx, Y + 1.9, Y + 0.4, redox ? 0x7e22ce : 0xe0f2fe);
  anim.push((dt, t) => { drop(dt, !done); flask.rotation.y = Math.sin(t * 2.2) * 0.12; });
  tag(g, `burette reads ${s.titreMl.toFixed(2)} mL`, [bx, Y + 2.0 + 0.5 + (filled / 50) * 5, -0.2], { offset: [1.5, 0.2, 0] });
  tag(g, titrationStatus(s.titreMl, req), [bx, Y + 0.5, -0.2], { offset: [-1.9, 0.5, 0] });
}

// ---- flame tests --------------------------------------------------------------------------
export function flame(g, anim, s) {
  const c = CATION_COLORS[s.cation] || CATION_COLORS.Na;
  const b = bunsen({ color: toHex(c.flame) }); b.position.set(0, Y, 0); g.add(b);
  // the salt colours the flame; sodium contamination tints it yellow
  const f = b.userData.flame;
  const tint = new THREE.Color(toHex(c.flame)).lerp(new THREE.Color(0xffc93c), Math.min(0.85, s.contamination / 100));
  f.children.forEach((m) => { m.material = m.material.clone(); m.material.color.copy(tint); m.material.opacity = Math.min(0.85, m.material.opacity * 1.5); });
  f.scale.set(1.4, 1.5, 1.4);
  // nichrome loop in its holder, dipped into the flame edge; a watch glass of the salt
  const holder = new THREE.Group(); holder.position.set(-1.2, Y + 1.45, 0); holder.rotation.z = -0.3; g.add(holder);
  holder.add(rot(cyl(0.06, 0.06, 0.9, M.plastic(0x7c2d12), [-0.4, 0, 0], 12), 'z', Math.PI / 2));
  holder.add(rot(cyl(0.008, 0.008, 1.0, M.steel(), [0.5, 0, 0], 6), 'z', Math.PI / 2));
  holder.add(rot(new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.008, 6, 16), M.glow(0xffb347, 1.2)), 'y', Math.PI / 2)); holder.children[2].position.set(1.03, 0, 0);
  const wg = glassVessel('dish', { fill: 0.3, color: 0xf5f5f0, opacity: 0.95, scale: 0.6 }); wg.position.set(-2.6, Y, 0.6); g.add(wg);
  const tt = testTube(0xf8fafc, 0.4); tt.position.set(-2.6, Y, -0.6); g.add(tt);
  tag(g, c.result, [0, Y + 2.1, 0], { offset: [1.7, 0.6, 0] });
  anim.push((dt, t) => { f.scale.set(1.4 + Math.sin(t * 17) * 0.06, 1.5 + Math.sin(t * 11) * 0.09, 1.4); f.rotation.y += dt * 1.2; });
}

// ---- anion tests in a rack ----------------------------------------------------------------
const PPT = { carbonate: [0xf8fafc, 'fizz'], chloride: [0xffffff, 'cloud'], sulfate: [0xffffff, 'cloud'], nitrate: [0x7c2d12, 'ring'], sulfide: [0x1f2937, 'cloud'] };
export function testtubes(g, anim, s) {
  const r = rack(g, 5, 0, 0);
  const active = 2;
  const [col, kind] = PPT[s.anion] || [0xbfdbfe, 'clear'];
  for (let i = 0; i < 5; i++) {
    const on = i === active;
    const t = testTube(on && kind === 'cloud' ? col : 0xdbeafe, 0.32 + (on ? s.drops * 0.02 : 0), { opacity: on && kind === 'cloud' ? 0.9 : 0.4 });
    t.position.set(-1.24 + i * 0.62, 0.0, 0); r.add(t);
    if (on && kind === 'fizz') anim.push(bubbles(t, { r: 0.05, y0: 0.08, y1: 0.5, n: 16, size: 0.014, rate: 1.4 }));
    if (on && kind === 'ring') t.add(cyl(0.075, 0.075, 0.05, M.liquid(0x7c2d12, 0.95), [0, 0.32, 0], 20));
  }
  // a dropper above the active tube
  const dr = new THREE.Group(); dr.position.set(-1.24 + active * 0.62, Y + 2.1, 0); g.add(dr);
  dr.add(cyl(0.025, 0.012, 0.6, M.glass(), [0, 0, 0], 12)); dr.add(sphere(0.08, M.rubber(0x8a2d2d), [0, 0.38, 0], 16)); dr.children[1].scale.y = 1.4;
  const drop = dripper(g, -1.24 + active * 0.62, Y + 1.78, Y + 0.6, 0xf8fafc);
  anim.push((dt) => drop(dt));
  tag(g, ANION_RESULTS[s.anion], [-1.24 + active * 0.62, Y + 1.5, 0], { offset: [2.2, 0.9, 0], scale: 0.17 });
}

// ---- gas preparation ----------------------------------------------------------------------
export function gasprep(g, anim, s) {
  const flask = glassVessel('conical', { fill: 0.3, color: s.gas === 'co2' ? 0xf3f4f6 : s.gas === 'o2' ? 0x3f3f46 : 0xdbeafe, opacity: 0.75 }); flask.position.set(-2.0, Y, 0); g.add(flask);
  // stopper with a thistle funnel and a delivery tube
  g.add(cyl(0.13, 0.11, 0.18, M.rubber(0x8a2d2d), [-2.0, Y + 1.15, 0], 16));
  g.add(cyl(0.025, 0.025, 1.5, M.glass(), [-2.12, Y + 1.5, 0], 10));
  const th = glassVessel('funnel', { scale: 0.55 }); th.position.set(-2.12, Y + 2.1, 0); g.add(th);
  const up = s.gas === 'co2'; const down = s.gas === 'nh3';
  const jarY = up ? Y : Y + 0.1;
  const jar = glassVessel('gasJar', { fill: s.gas === 'h2' || s.gas === 'o2' ? 0.5 : 0, color: 0xbfe3ff, opacity: 0.4 }); jar.position.set(1.6, jarY, 0);
  if (down) { jar.rotation.z = Math.PI; jar.position.y = Y + 1.6; }
  g.add(jar);
  if (s.gas === 'h2' || s.gas === 'o2') {
    // collected over water: a trough under an inverted, water-filled jar
    const trough = glassVessel('dish', { fill: 0.6, color: 0x93c5fd, opacity: 0.5, scale: 2.6 }); trough.position.set(1.6, Y, 0); g.add(trough);
    jar.rotation.z = Math.PI; jar.position.y = Y + 1.62;
  }
  g.add(wire([-1.95, Y + 1.25, 0], [1.6, Y + (up ? 0.25 : 0.45), 0], 0xdbeafe, 0.4, 0.025));
  anim.push(bubbles(flask, { r: 0.25, y0: 0.05, y1: 0.3, n: 20, rate: s.rate / 50 }));
  anim.push(bubbles(jar, { r: 0.2, y0: 0.1, y1: 1.4, n: 10, rate: s.rate / 60, size: 0.03 }));
  tag(g, GAS_RESULTS[s.gas], [1.6, Y + 1.6, 0], { offset: [0.6, 1.0, 0], scale: 0.17 });
}

// ---- water of crystallisation -------------------------------------------------------------
export function crystallization(g, anim, s) {
  const tri = tripodWithGauze(); tri.position.set(-1.2, Y, 0); g.add(tri);
  const b = bunsen(); b.position.set(-1.2, Y, 0); g.add(b);
  const cr = glassVessel('crucible', { scale: 1.2 }); cr.children[0].material = M.porcelain(); cr.position.set(-1.2, Y + 1.47, 0); g.add(cr);
  // crystals turn from blue CuSO4·5H2O to white anhydrous salt as they are heated
  const k = Math.min(1, s.heating / 100);
  const col = new THREE.Color(0x2563eb).lerp(new THREE.Color(0xf1f5f9), k);
  const cm = new THREE.MeshPhysicalMaterial({ color: col, roughness: 0.3, clearcoat: 0.6 });
  for (let i = 0; i < 24; i++) { const c = new THREE.Mesh(new THREE.OctahedronGeometry(0.045), cm); c.position.set(-1.2 + (Math.random() - 0.5) * 0.3, Y + 1.55 + Math.random() * 0.12, (Math.random() - 0.5) * 0.3); c.rotation.set(Math.random() * 3, Math.random() * 3, 0); g.add(c); }
  // an electronic balance for the weighings
  const bal = new THREE.Group(); bal.position.set(2.2, Y, 0.2); g.add(bal);
  bal.add(box(1.6, 0.35, 1.3, M.plastic(0xe5e7eb), [0, 0.18, 0], 0.06));
  bal.add(cyl(0.55, 0.55, 0.04, M.steel(), [0, 0.38, -0.1], 40));
  const disp = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.2), new THREE.MeshBasicMaterial({ map: lcdTexture(`${(s.residueMass + (s.hydrateMass - s.residueMass) * (1 - k)).toFixed(2)} g`), toneMapped: false }));
  disp.position.set(0, 0.25, 0.651); bal.add(disp);
  tag(g, `water lost ${(s.hydrateMass - s.residueMass).toFixed(2)} g`, [-1.2, Y + 1.8, 0], { offset: [0, 0.8, 0] });
  anim.push((dt, t) => b.userData.flame.scale.setScalar(1 + Math.sin(t * 15) * 0.05));
}
function lcdTexture(text) {
  const c = document.createElement('canvas'); c.width = 256; c.height = 64; const x = c.getContext('2d');
  x.fillStyle = '#9fb08a'; x.fillRect(0, 0, 256, 64); x.fillStyle = '#1f2a14'; x.font = '700 40px monospace'; x.textAlign = 'right'; x.textBaseline = 'middle'; x.fillText(text, 244, 34);
  const t = new THREE.CanvasTexture(c); if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace; t.userData.owned = true; return t;
}

// ---- full salt analysis: the anion rack and the cation flame side by side ----------------
export function saltanalysis(g, anim, s) {
  const left = new THREE.Group(); left.position.x = -1.6; g.add(left);
  testtubes(left, anim, { anion: s.anion, drops: 5 });
  const right = new THREE.Group(); right.position.x = 2.4; g.add(right);
  flame(right, anim, { cation: s.cation, contamination: 5 });
}

// ---- electrolysis of copper sulphate with copper electrodes ------------------------------
export function electrolysis(g, anim, s) {
  const beaker = glassVessel('beaker250', { fill: 0.75, color: 0x2563eb, opacity: 0.6, scale: 1.4 }); beaker.position.set(0, Y, 0); g.add(beaker);
  const plated = Math.min(1, s.currentA * s.timeMin / 40);
  const cathodeM = new THREE.MeshStandardMaterial({ color: new THREE.Color(0xc77b4a).lerp(new THREE.Color(0xe39a72), plated), metalness: 0.9, roughness: 0.4 - plated * 0.2 });
  const cathode = box(0.06 + plated * 0.02, 1.5, 0.4, cathodeM, [-0.3, Y + 1.1, 0]); g.add(cathode);
  const anode = box(0.06, 1.5, 0.4, M.copper(), [0.3, Y + 1.1, 0]); g.add(anode);
  // a DC supply with an ammeter in series
  const psu = new THREE.Group(); psu.position.set(-2.8, Y, 0.2); g.add(psu);
  psu.add(box(1.4, 0.9, 1.0, M.plastic(0x334155), [0, 0.45, 0], 0.05));
  const lcd = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.22), new THREE.MeshBasicMaterial({ map: lcdTexture(`${s.currentA.toFixed(2)} A`), toneMapped: false })); lcd.position.set(0, 0.62, 0.501); psu.add(lcd);
  psu.add(cyl(0.06, 0.06, 0.08, M.plastic(0xdc2626), [-0.3, 0.25, 0.52], 12)); psu.add(cyl(0.06, 0.06, 0.08, M.plastic(0x111827), [0.3, 0.25, 0.52], 12));
  g.add(wire([-3.1, Y + 0.25, 0.72], [-0.3, Y + 1.85, 0], 0x111827, 0.4), wire([-2.5, Y + 0.25, 0.72], [0.3, Y + 1.85, 0], 0xdc2626, 0.5));
  // Cu2+ ions drift to the cathode
  const ions = []; const im = M.glow(0x60a5fa, 0.8);
  for (let i = 0; i < 18; i++) { const io = sphere(0.025, im, [0, 0, 0], 8); io.userData = { x: Math.random() * 0.5 - 0.25, y: Y + 0.3 + Math.random() * 0.8, z: Math.random() * 0.6 - 0.3 }; g.add(io); ions.push(io); }
  anim.push((dt) => { for (const io of ions) { const u = io.userData; u.x -= dt * 0.12 * s.currentA; if (u.x < -0.27) u.x = 0.27; io.position.set(u.x, u.y, u.z); } });
  tag(g, `cathode gains copper: Cu²⁺ + 2e⁻ → Cu`, [-0.3, Y + 1.85, 0], { offset: [-1.2, 0.9, 0], scale: 0.17 });
  tag(g, `${s.currentA.toFixed(2)} A for ${s.timeMin.toFixed(0)} min`, [0.3, Y + 1.85, 0], { offset: [1.4, 0.6, 0] });
}

// ---- pH and indicators ---------------------------------------------------------------------
export function ph(g, anim, s) {
  const r = rack(g, 5, -0.8, 0);
  for (let i = 0; i < 5; i++) {
    const p = Math.max(1, Math.min(14, s.pH + (i - 2) * 1.2));
    const t = testTube(toHex(indicatorColor(s.indicator, p)), 0.42, { opacity: 0.9 }); t.position.set(-1.24 + i * 0.62, 0, 0); r.add(t);
  }
  // a pH meter with its probe in a beaker
  const meter = new THREE.Group(); meter.position.set(2.5, Y, 0.3); g.add(meter);
  meter.add(box(1.0, 0.4, 0.8, M.plastic(0xf1f5f9), [0, 0.2, 0], 0.06));
  const lcd = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 0.2), new THREE.MeshBasicMaterial({ map: lcdTexture(`pH ${s.pH.toFixed(1)}`), toneMapped: false })); lcd.position.set(0, 0.28, 0.401); lcd.rotation.x = -0.2; meter.add(lcd);
  const bk = glassVessel('beaker100', { fill: 0.6, color: toHex(indicatorColor(s.indicator, s.pH)), opacity: 0.75 }); bk.position.set(3.6, Y, 0.1); g.add(bk);
  g.add(cyl(0.035, 0.035, 1.6, M.plastic(0x111827), [3.6, Y + 0.9, 0.1], 12));
  g.add(wire([2.5, Y + 0.35, -0.1], [3.6, Y + 1.7, 0.1], 0x111827, 0.3, 0.015));
  tag(g, `${s.indicator}: ${indicatorColorName(s.indicator, s.pH)}`, [-0.8, Y + 1.5, 0], { offset: [0, 0.8, 0] });
}

// ---- organic functional group tests ------------------------------------------------------
export function functional(g, anim, s) {
  const r = rack(g, 5, 0, 0);
  const order = ['alcohol', 'aldehyde', 'ketone', 'carboxylic', 'phenol'];
  const looks = { alcohol: [0xf1f5f9, 'fizz'], aldehyde: [0xd1d5db, 'mirror'], ketone: [0xf97316, 'cloud'], carboxylic: [0xf8fafc, 'fizz'], phenol: [0x7c3aed, 'clear'] };
  order.forEach((k, i) => {
    const on = k === s.group;
    const [col, kind] = looks[k];
    const t = testTube(on ? col : 0xe5e7eb, 0.36, { opacity: on ? 0.92 : 0.35 }); t.position.set(-1.24 + i * 0.62, 0, 0); r.add(t);
    if (on && kind === 'mirror') {
      // Tollens' test: a silver mirror coats the inside of the tube
      t.add(cyl(0.085, 0.085, 0.8, new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 1, roughness: 0.08 }), [0, 0.55, 0], 20));
    }
    if (on && kind === 'fizz') anim.push(bubbles(t, { r: 0.05, y0: 0.08, y1: 0.5, n: 14, size: 0.013, rate: s.reagentDrops / 3 }));
  });
  tag(g, GROUP_RESULTS[s.group], [-1.24 + order.indexOf(s.group) * 0.62, Y + 1.5, 0], { offset: [0, 1.0, 0], scale: 0.17 });
}

// ---- heat of neutralisation -----------------------------------------------------------------
export function thermochemistry(g, anim, s) {
  // a polystyrene cup calorimeter in a beaker, with a lid, thermometer and stirrer
  const outer = glassVessel('beaker250', { scale: 1.4 }); outer.position.set(0, Y, 0); g.add(outer);
  const cup = new THREE.Mesh(new THREE.LatheGeometry([[0.3, 0], [0.33, 0.02], [0.42, 1.1], [0.45, 1.13], [0.43, 1.13], [0.4, 1.08], [0.31, 0.04], [0, 0.04]].map(([r, y]) => new THREE.Vector2(r, y)), 40), new THREE.MeshStandardMaterial({ color: 0xfafaf9, roughness: 0.95 }));
  cup.position.set(0, Y + 0.05, 0); cup.castShadow = true; g.add(cup);
  const liq = glassVessel('calorimeter', { fill: 0.75, color: 0xe0f2fe, opacity: 0.5, scale: 0.9 }); liq.children[0].visible = false; liq.position.set(0, Y + 0.08, 0); g.add(liq);
  g.add(cyl(0.47, 0.47, 0.04, new THREE.MeshStandardMaterial({ color: 0xfafaf9, roughness: 0.95 }), [0, Y + 1.2, 0], 40));
  const th = thermometer(25 + s.deltaT, { height: 3 }); th.position.set(0.12, Y + 0.3, 0); g.add(th);
  for (const [x, label] of [[-2.0, `${s.acidMl} mL HCl`], [2.0, `${s.baseMl} mL NaOH`]]) {
    const mc = glassVessel('measuring', { fill: 0.5, color: 0xe0f2fe, opacity: 0.5 }); mc.position.set(x, Y, 0); g.add(mc);
    mc.add(box(0.5, 0.06, 0.5, M.plastic(0x60a5fa), [0, 0.06, 0], 0.02));
    tag(g, label, [x, Y + 2.4, 0], { offset: [0, 0.4, 0] });
  }
  tag(g, `ΔT = ${s.deltaT.toFixed(1)} °C`, [0.12, Y + 3.3, 0], { offset: [0.8, 0.3, 0] });
}

// ---- Lassaigne's test ---------------------------------------------------------------------
const LAS = { nitrogen: 0x1e3a8a, sulfur: 0x6b21a8, chlorine: 0xf8fafc, bromine: 0xfef3c7, iodine: 0xfde68a };
export function lassaigne(g, anim, s) {
  const b = bunsen(); b.position.set(-1.6, Y, 0); g.add(b);
  // the fusion tube in tongs, red hot over the flame
  const tongs = new THREE.Group(); tongs.position.set(-1.6, Y + 2.0, 0); tongs.rotation.z = -0.6; g.add(tongs);
  tongs.add(rot(cyl(0.02, 0.02, 1.6, M.steel(), [-0.9, 0, 0], 8), 'z', Math.PI / 2));
  const ft = testTube(0x7c2d12, 0.2); ft.rotation.z = Math.PI / 2; ft.position.set(0, 0, 0); ft.scale.setScalar(0.7); tongs.add(ft);
  tongs.add(sphere(0.06, M.glow(0xff7a1a, 2), [0.02, -0.06, 0], 12));
  // the china dish of water, then the result tube
  const dish = glassVessel('dish', { fill: 0.4, color: 0xe0f2fe, opacity: 0.5 }); dish.children[0].material = M.porcelain(); dish.position.set(0.6, Y, 0.4); g.add(dish);
  const strength = s.extractStrength / 100;
  const res = testTube(LAS[s.element] || 0xdbeafe, 0.45, { opacity: 0.4 + strength * 0.55 }); res.position.set(2.0, Y, 0); g.add(res);
  tag(g, lassaigneResult(s.element), [2.0, Y + 1.3, 0], { offset: [0.4, 0.9, 0], scale: 0.16 });
  anim.push((dt, t) => { b.userData.flame.scale.setScalar(1 + Math.sin(t * 15) * 0.05); });
}
