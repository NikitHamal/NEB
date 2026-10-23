/**
 * Reaction balancer in 3D. Set the coefficients of real equations with the steppers (subscripts are
 * locked, as in chemistry). Every species stands on a beam balance as that many molecules built from
 * atoms in their CPK colours and covalent sizes (simple ones in their real shapes: bent water,
 * tetrahedral methane, pyramidal ammonia, linear CO₂). Reactants on the left pan, products on the
 * right: the beam carries the total mass of each side (from atomic masses) and tips until the equation,
 * and the mass, balances. An atom tally compares both sides element by element.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, THREE } from './chem3d/stage.js';

const MASS = { H: 1.008, C: 12.011, N: 14.007, O: 15.999, Na: 22.99, Mg: 24.305, Al: 26.982, S: 32.06, Cl: 35.45, K: 39.098, Ca: 40.078, Fe: 55.845, Cu: 63.546 };
const COLOR = { H: 0xf1f5f9, C: 0x2f3742, N: 0x3b82f6, O: 0xef4444, Na: 0xa855f7, Mg: 0x22c55e, Al: 0xcbd5e1, S: 0xfacc15, Cl: 0x16a34a, K: 0x8b5cf6, Ca: 0xa3a3a3, Fe: 0xc2410c, Cu: 0xb45309 };
const RAD = { H: 0.31, C: 0.76, N: 0.71, O: 0.66, Na: 1.66, Mg: 1.41, Al: 1.21, S: 1.05, Cl: 1.02, K: 2.03, Ca: 1.76, Fe: 1.32, Cu: 1.32 };
const EQS = [
  { name: 'Water', l: ['H2', 'O2'], r: ['H2O'] },
  { name: 'Methane burns', l: ['CH4', 'O2'], r: ['CO2', 'H2O'] },
  { name: 'Rusting', l: ['Fe', 'O2'], r: ['Fe2O3'] },
  { name: 'Ammonia', l: ['N2', 'H2'], r: ['NH3'] },
  { name: 'Magnesium burns', l: ['Mg', 'O2'], r: ['MgO'] },
  { name: 'Propane burns', l: ['C3H8', 'O2'], r: ['CO2', 'H2O'] },
  { name: 'Photosynthesis', l: ['CO2', 'H2O'], r: ['C6H12O6', 'O2'] },
  { name: 'Aluminium + acid', l: ['Al', 'HCl'], r: ['AlCl3', 'H2'] },
  { name: 'Neutralisation', l: ['NaOH', 'H2SO4'], r: ['Na2SO4', 'H2O'] },
  { name: 'Limewater test', l: ['Ca(OH)2', 'CO2'], r: ['CaCO3', 'H2O'] },
];
const SUB = '₀₁₂₃₄₅₆₇₈₉';
const pretty = (f) => f.replace(/\d/g, (d) => SUB[+d]);
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });
function gcd(a, b) { return b ? gcd(b, a % b) : a; }

function parse(f) {
  const stack = [{}]; let i = 0;
  while (i < f.length) {
    const ch = f[i];
    if (ch === '(') { stack.push({}); i++; continue; }
    if (ch === ')') { i++; let n = ''; while (i < f.length && /\d/.test(f[i])) n += f[i++]; const g = stack.pop(); const m = n ? +n : 1; const top = stack[stack.length - 1]; for (const e in g) top[e] = (top[e] || 0) + g[e] * m; continue; }
    let el = ch; i++;
    while (i < f.length && /[a-z]/.test(f[i])) el += f[i++];
    let n = ''; while (i < f.length && /\d/.test(f[i])) n += f[i++];
    const top = stack[stack.length - 1]; top[el] = (top[el] || 0) + (n ? +n : 1);
  }
  return stack[0];
}

const DIRS = {
  1: [[1, 0, 0]], 2: [[1, 0, 0], [-1, 0, 0]], 3: [[1, 0, 0], [-0.5, 0, 0.866], [-0.5, 0, -0.866]],
  4: [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], 5: [[0, 1, 0], [0, -1, 0], [1, 0, 0], [-0.5, 0, 0.866], [-0.5, 0, -0.866]],
  6: [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
};
// A molecule's atoms as [element, x, y, z] in Å: VSEPR shapes for a centre with terminal atoms
// (bent water, pyramidal ammonia), chains and rings for the larger ones, a relaxed packing otherwise.
function geometry(f) {
  const atoms = parse(f);
  const list = []; Object.entries(atoms).forEach(([e, n]) => { for (let i = 0; i < n; i++) list.push(e); });
  if (list.length === 1) return [[list[0], 0, 0, 0]];
  const bond = (a, b) => (RAD[a] + RAD[b]) * 0.92;
  if (list.length === 2) { const d = bond(list[0], list[1]) / 2; return [[list[0], -d, 0, 0], [list[1], d, 0, 0]]; }
  const heavy = Object.keys(atoms).filter((e) => e !== 'H');
  const single = heavy.filter((e) => atoms[e] === 1 && e !== 'O');
  let centre = single.sort((a, b) => RAD[b] - RAD[a])[0] || (heavy.length === 1 ? heavy[0] : null);
  if (f === 'H2O') centre = 'O';
  const out = [];
  if (centre && (list.length - 1) <= 6 && Object.keys(atoms).every((e) => e === centre || atoms[e] <= 4) && !['C3H8', 'C6H12O6', 'Fe2O3', 'Na2SO4', 'H2SO4', 'Ca(OH)2', 'NaOH', 'CaCO3'].includes(f)) {
    out.push([centre, 0, 0, 0]);
    const others = list.filter((e, i) => !(e === centre && i === list.indexOf(centre)));
    let dirs = DIRS[others.length].map((d) => new THREE.Vector3(...d).normalize());
    if (f === 'H2O') { const a = 104.5 * Math.PI / 360; dirs = [new THREE.Vector3(Math.sin(a), -Math.cos(a), 0), new THREE.Vector3(-Math.sin(a), -Math.cos(a), 0)]; }
    if (f === 'NH3') { const a = 0.38; dirs = [0, 1, 2].map((k) => new THREE.Vector3(Math.cos(k * 2.094) * Math.cos(a), -Math.sin(a), Math.sin(k * 2.094) * Math.cos(a))); }
    others.forEach((e, i) => { const d = dirs[i].clone().multiplyScalar(bond(centre, e)); out.push([e, d.x, d.y, d.z]); });
    return out;
  }
  // relaxed packing: heavy atoms first near the middle, hydrogens outside, then springs push apart
  const pts = list.map((e, i) => { const a = i * 2.39996; const r = (e === 'H' ? 1.6 : 0.6) * Math.sqrt(i + 1); return { e, p: new THREE.Vector3(Math.cos(a) * r, ((i * 0.618) % 1 - 0.5) * 1.6, Math.sin(a) * r) }; });
  const tmp = new THREE.Vector3();
  for (let it = 0; it < 220; it++) {
    for (let i = 0; i < pts.length; i++) {
      pts[i].p.multiplyScalar(0.985);
      for (let j = 0; j < pts.length; j++) {
        if (i === j) continue;
        const d = tmp.subVectors(pts[i].p, pts[j].p); const L = d.length() || 1e-3; const want = bond(pts[i].e, pts[j].e) * (pts[i].e === 'H' && pts[j].e === 'H' ? 1.5 : 1.02);
        if (L < want) pts[i].p.addScaledVector(d.normalize(), (want - L) * 0.5);
      }
    }
  }
  const c = new THREE.Vector3(); pts.forEach((x) => c.add(x.p)); c.multiplyScalar(1 / pts.length);
  return pts.map((x) => [x.e, x.p.x - c.x, x.p.y - c.y, x.p.z - c.z]);
}

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Balancing equations', aim: 'Atoms and mass are conserved', target: [0, 1.6, 0], camera: [0, 2.6, 6.6], minDistance: 3, maxDistance: 12 });
  if (!L) return null;
  const { engine, world, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Change the big numbers until both sides match', '#2563eb');

  // the balance: a pillar, a pivoting beam, two pans hanging on chains
  const brass = new THREE.MeshStandardMaterial({ color: 0xc9a14a, metalness: 0.85, roughness: 0.3 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x2b2f36, roughness: 0.5, metalness: 0.3 });
  const baseB = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.12, 0.8), dark); baseB.position.y = 0.06; world.add(baseB);
  const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 2.0, 20), brass); pillar.position.y = 1.1; world.add(pillar);
  const beam = new THREE.Group(); beam.position.y = 2.12; world.add(beam);
  const bar = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.06, 0.08), brass); beam.add(bar);
  const pointer = new THREE.Mesh(new THREE.ConeGeometry(0.035, 0.5, 10), dark); pointer.rotation.z = Math.PI; pointer.position.y = -0.28; beam.add(pointer);
  const scaleArc = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.01, 6, 40, 0.8), dark); scaleArc.rotation.z = -Math.PI / 2 - 0.4; scaleArc.position.y = 2.12; world.add(scaleArc);
  const pans = [-1.6, 1.6].map((x) => {
    const g = new THREE.Group(); world.add(g);
    const pan = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.85, 0.06, 48), brass); g.add(pan);
    for (let k = 0; k < 3; k++) {
      const a = k * Math.PI * 2 / 3;
      const dir = new THREE.Vector3(-Math.cos(a) * 0.82, 1.3, -Math.sin(a) * 0.82);
      const ch = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, dir.length(), 6), dark);
      ch.position.set(Math.cos(a) * 0.41, 0.65, Math.sin(a) * 0.41);
      ch.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
      g.add(ch);
    }
    const mol = new THREE.Group(); mol.position.y = 0.04; g.add(mol);
    return { g, x, mol };
  });
  const glowRing = new THREE.Mesh(new THREE.TorusGeometry(2.6, 0.02, 8, 80), new THREE.MeshBasicMaterial({ color: 0x22c55e, transparent: true, opacity: 0 }));
  glowRing.rotation.x = Math.PI / 2; glowRing.position.y = 0.2; world.add(glowRing);

  const atomGeo = new THREE.SphereGeometry(1, 20, 14);
  const atomMats = {}; Object.keys(COLOR).forEach((e) => { atomMats[e] = new THREE.MeshPhysicalMaterial({ color: COLOR[e], roughness: 0.3, clearcoat: 0.5 }); });

  // the equation bar across the top of the stage, with steppers on every coefficient
  const bar2 = document.createElement('div');
  bar2.style.cssText = 'position:absolute;left:50%;top:56px;transform:translateX(-50%);display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;max-width:94%;padding:10px 14px;border-radius:16px;background:rgba(15,23,42,0.86);color:#f8fafc;font:700 18px Poppins,system-ui,sans-serif;z-index:3;box-shadow:0 8px 24px rgba(0,0,0,0.25)';
  stage.appendChild(bar2);

  let eq = null; let coef = []; let species = []; let elements = []; let solved = false; let celebrate = 0; let tilt = 0;
  const panel = createPanel(stage, { title: 'Balance the equation' });
  panel.chips({ label: 'Reaction', options: EQS.map((e, i) => ({ value: String(i), label: e.name })), value: '0', onChange: (v) => load(+v) });
  panel.buttonRow([{ label: 'Hint', icon: 'lightbulb', onClick: hint }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: () => load(EQS.indexOf(eq)) }]);
  const tally = document.createElement('div');
  tally.style.cssText = 'display:grid;grid-template-columns:auto 1fr 1fr auto;gap:3px 10px;font:600 12px Poppins,system-ui,sans-serif;color:#cbd5e1;padding:8px 10px;border-radius:12px;background:rgba(255,255,255,0.04);flex-shrink:0';
  panel.body.appendChild(tally);
  const st = panel.stats([{ key: 'l', label: 'Mass of reactants' }, { key: 'r', label: 'Mass of products' }, { key: 'ok', label: 'Elements balanced' }, { key: 'state', label: 'Equation' }]);
  panel.info('Only the big numbers in front (coefficients) may change: changing a subscript would make a different substance. Start with the element that appears in the fewest substances; leave H and O till last.');

  function counts(e) { let l = 0; let r = 0; species.forEach((s, i) => { const n = (s.atoms[e] || 0) * coef[i]; if (s.side) r += n; else l += n; }); return [l, r]; }
  function massSide(side) { let m = 0; species.forEach((s, i) => { if (s.side !== side) return; for (const e in s.atoms) m += s.atoms[e] * MASS[e] * coef[i]; }); return m; }
  const gcdAll = () => coef.reduce((a, b) => gcd(a, b));
  function buildBar() {
    bar2.innerHTML = '';
    species.forEach((s, i) => {
      if (i > 0) { const op = document.createElement('span'); op.textContent = species[i - 1].side !== s.side ? '→' : '+'; op.style.cssText = 'margin:0 4px;color:#94a3b8'; bar2.appendChild(op); }
      const w = document.createElement('span'); w.style.cssText = 'display:inline-flex;align-items:center;gap:4px';
      const mk = (txt, d) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = txt; b.setAttribute('aria-label', `${d > 0 ? 'more' : 'fewer'} ${s.f}`); b.style.cssText = 'width:26px;height:26px;border-radius:50%;border:none;background:rgba(255,255,255,0.12);color:#f8fafc;font:700 15px Poppins,system-ui,sans-serif;cursor:pointer;line-height:26px;padding:0'; b.onclick = () => setCoef(i, coef[i] + d); return b; };
      const n = document.createElement('b'); n.textContent = String(coef[i]); n.style.cssText = 'min-width:18px;text-align:center;color:#93c5fd;font-size:20px';
      const f = document.createElement('span'); f.textContent = pretty(s.f);
      w.append(mk('−', -1), n, mk('+', 1), f); bar2.appendChild(w);
      s.numEl = n;
    });
  }
  function buildTally() {
    tally.innerHTML = '<b style="color:#94a3b8;font-size:11px">Atom</b><b style="color:#94a3b8;font-size:11px">Left</b><b style="color:#94a3b8;font-size:11px">Right</b><span></span>' + elements.map((e) => {
      const [l, r] = counts(e); const ok = l === r;
      return `<span><i style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#${COLOR[e].toString(16).padStart(6, '0')};margin-right:5px"></i>${e}</span><span>${l}</span><span>${r}</span><span style="color:${ok ? '#4ade80' : '#f87171'}">${ok ? '✓' : '✗'}</span>`;
    }).join('');
  }
  function buildMolecules() {
    pans.forEach((p) => { while (p.mol.children.length) p.mol.remove(p.mol.children[0]); });
    const per = [[], []];
    species.forEach((s, i) => { for (let k = 0; k < coef[i]; k++) per[s.side].push(s); });
    per.forEach((list, side) => {
      const n = list.length; const cols = Math.ceil(Math.sqrt(n * 1.4));
      list.forEach((s, k) => {
        const g = new THREE.Group();
        const sc = n > 14 ? 0.13 : n > 8 ? 0.15 : 0.18;
        for (const [e, x, y, z] of s.geo) { const m = new THREE.Mesh(atomGeo, atomMats[e]); m.position.set(x * sc, y * sc, z * sc); m.scale.setScalar(RAD[e] * sc * 0.82); m.castShadow = true; g.add(m); }
        const row = Math.floor(k / cols); const col = k % cols; const rows = Math.ceil(n / cols);
        const sp = Math.min(0.55, 1.6 / Math.max(cols, rows));
        g.position.set((col - (cols - 1) / 2) * sp, 0.28 * sc / 0.18 + Math.floor(k / (cols * rows)) * 0.3, (row - (rows - 1) / 2) * sp);
        g.rotation.set(k * 0.7, k * 1.3, 0);
        pans[side].mol.add(g);
      });
    });
  }
  function load(i) {
    eq = EQS[i];
    species = eq.l.map((f) => ({ f, side: 0, atoms: parse(f), geo: geometry(f) })).concat(eq.r.map((f) => ({ f, side: 1, atoms: parse(f), geo: geometry(f) })));
    coef = species.map(() => 1);
    const set = new Set(); species.forEach((s) => Object.keys(s.atoms).forEach((e) => set.add(e)));
    elements = [...set]; solved = false; celebrate = 0;
    buildBar(); buildTally(); buildMolecules();
  }
  function setCoef(i, v) {
    v = Math.max(1, Math.min(12, v));
    if (v === coef[i]) return;
    coef[i] = v;
    const was = solved;
    solved = elements.every((e) => { const c = counts(e); return c[0] === c[1]; });
    if (solved && !was) celebrate = 1;
    species[i].numEl.textContent = String(v);
    buildTally(); buildMolecules();
  }
  function hint() {
    const bad = elements.filter((e) => { const c = counts(e); return c[0] !== c[1]; });
    if (!bad.length) { badge.set('Already balanced!'); return; }
    bad.sort((a, b) => (a === 'H' || a === 'O') - (b === 'H' || b === 'O') || species.filter((s) => s.atoms[a]).length - species.filter((s) => s.atoms[b]).length);
    const e = bad[0]; const c = counts(e);
    hintUntil = performance.now() + 5000;
    badge.set(`Hint: balance ${e} next: ${c[0]} on the left, ${c[1]} on the right`);
  }
  let hintUntil = 0;
  load(0);

  engine.setUpdate((dt, time) => {
    controls.update(dt);
    const ml = massSide(0); const mr = massSide(1);
    const goal = Math.max(-0.22, Math.min(0.22, (mr - ml) / Math.max(ml, mr, 1) * 0.6));
    tilt += (goal - tilt) * (1 - Math.exp(-dt * 2.5));
    beam.rotation.z = -tilt;
    pans.forEach((p) => { p.g.position.set(p.x * Math.cos(tilt), 2.12 - 1.3 - p.x * Math.sin(tilt), 0); p.g.position.y -= 0.02; });
    celebrate = Math.max(0, celebrate - dt * 0.6);
    glowRing.material.opacity = solved ? 0.25 + 0.55 * celebrate * (0.5 + 0.5 * Math.sin(time * 8)) : 0;
    pans.forEach((p, i) => { p.mol.rotation.y += dt * 0.15 * (i ? -1 : 1); });
    const ok = elements.filter((e) => { const c = counts(e); return c[0] === c[1]; }).length;
    st.l.set(`${fmt(ml, 2)} u`); st.r.set(`${fmt(mr, 2)} u`); st.ok.set(`${ok} of ${elements.length}`);
    st.state.set(solved ? (gcdAll() > 1 ? 'not simplest' : 'balanced ✓') : 'unbalanced');
    if (performance.now() > hintUntil) badge.set(solved ? (gcdAll() > 1 ? `Balanced, but divide every number by ${gcdAll()} for the simplest equation` : 'Same atoms on both sides, so the same mass: mass is conserved') : 'Change the big numbers until both sides match');
  });
  engine.start();

  stage.__balance = { set: (i, v) => setCoef(i, v), load, solved: () => solved };
  return { dispose() { panel.dispose(); hud.dispose(); bar2.remove(); atomGeo.dispose(); Object.values(atomMats).forEach((m) => m.dispose()); L.dispose(); } };
}
