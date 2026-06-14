// General molecule builder: parse a chemical formula, infer geometry via VSEPR,
// and place atoms in 3D. Pure logic — no Three.js dependency.
//
// Exports:
//   parseFormula(str) -> { atoms: [{el, count}], totalAtoms, counts: {sym:count} }
//   buildMolecule(str) -> { atoms:[{el,pos:[x,y,z]}], bonds:[{a,b,order}], note, shape, ionic, central }
//
// The buildMolecule result is in arbitrary "chemistry units"; the renderer scales it.

import { getBySymbol, isMetal, isNonmetal } from './elements-data.js';

const SCALE = 1.5; // bond length unit (matches old molecule-viewer)
const TAU = Math.PI * 2;

// ---------- Formula parser ----------
// Handles: H2O, NaCl, C6H12O6, (OH)2, Ca3(PO4)2, CuSO4.5H2O, [NH4]+, CH3COOH
export function parseFormula(input) {
  const str = (input || '').replace(/\s+/g, '');
  if (!str) return { ok: false, error: 'Empty formula', atoms: [], counts: {}, totalAtoms: 0 };
  const counts = {};
  const groups = [{ mult: 1, scope: counts }];
  let i = 0;
  let ok = true;
  let error = null;

  function currentScope() {
    const g = groups[groups.length - 1];
    return g ? g.scope : null;
  }
  function readNumber(at) {
    let s = '';
    while (at < str.length && /[0-9]/.test(str[at])) { s += str[at]; at++; }
    return { value: s === '' ? 1 : parseInt(s, 10), len: s.length };
  }
  function readElement(at) {
    if (at >= str.length || !/[A-Z]/.test(str[at])) return null;
    let sym = str[at++];
    while (at < str.length && /[a-z]/.test(str[at])) sym += str[at++];
    return sym;
  }
  function addAtoms(sym, n) {
    if (!getBySymbol(sym)) { ok = false; error = `Unknown element: ${sym}`; return; }
    const scope = currentScope();
    if (!scope) { ok = false; error = 'Malformed group'; return; }
    scope[sym] = (scope[sym] || 0) + n;
  }

  while (i < str.length && ok) {
    const ch = str[i];
    if (ch === '(' || ch === '[') {
      groups.push({ mult: 1, scope: {} });
      i++;
    } else if (ch === ')' || ch === ']') {
      const group = groups.pop();
      if (!group) { ok = false; error = 'Unmatched bracket'; break; }
      i++;
      const { value: mult, len } = readNumber(i);
      i += len;
      const target = currentScope();
      if (!target) { ok = false; error = 'Unmatched bracket'; break; }
      for (const k in group.scope) target[k] = (target[k] || 0) + group.scope[k] * mult;
    } else if (ch === '.' || ch === '·') {
      // fold any currently-open hydrate scope back into its parent
      while (groups.length > 1 && groups[groups.length - 1].hydrateMult) {
        const g = groups.pop();
        const target = currentScope();
        if (!target) { ok = false; error = 'Malformed hydrate'; break; }
        const m = g.hydrateMult || 1;
        for (const k in g.scope) target[k] = (target[k] || 0) + g.scope[k] * m;
      }
      if (!ok) break;
      i++;
      const { value: hmult, len } = readNumber(i);
      i += len;
      groups.push({ mult: 1, scope: {}, hydrateMult: hmult });
    } else if (/[A-Z]/.test(ch)) {
      const sym = readElement(i);
      if (!sym) { ok = false; error = `Bad element at position ${i}`; break; }
      i += sym.length;
      const { value: n, len } = readNumber(i);
      i += len;
      addAtoms(sym, n);
    } else if (ch === '+' || ch === '-') {
      i++;
      const { len } = readNumber(i);
      i += len;
    } else {
      ok = false;
      error = `Unexpected character '${ch}'`;
      break;
    }
  }

  if (groups.length !== 1) {
    // fold any open hydrate scopes back into the root
    while (groups.length > 1) {
      const g = groups.pop();
      const target = currentScope();
      if (!target) { ok = false; break; }
      const m = g.hydrateMult || 1;
      for (const k in g.scope) target[k] = (target[k] || 0) + g.scope[k] * m;
    }
  }

  if (!ok) return { ok: false, error, atoms: [], counts: {}, totalAtoms: 0 };
  const atoms = [];
  let totalAtoms = 0;
  for (const sym in counts) {
    const n = counts[sym];
    atoms.push({ el: sym, count: n });
    totalAtoms += n;
  }
  atoms.sort((a, b) => b.count - a.count);
  return { ok: true, atoms, counts, totalAtoms };
}

// ---------- Geometry helpers ----------
function tetraVerts(r) {
  return [
    [r, r, r], [r, -r, -r], [-r, r, -r], [-r, -r, r],
  ];
}
function normalize(v) {
  const m = Math.hypot(v[0], v[1], v[2]) || 1;
  return [v[0] / m, v[1] / m, v[2] / m];
}
function scale(v, s) { return [v[0] * s, v[1] * s, v[2] * s]; }

// Place `n` terminal atoms around the origin at the given steric geometry.
function placeTerminals(n, lonePairs, bondLen) {
  // Returns array of [x,y,z] positions (without the central atom at origin).
  const total = n + lonePairs;
  if (total === 2) {
    return [[bondLen, 0, 0], [-bondLen, 0, 0]].slice(0, n); // linear
  }
  if (total === 3) {
    // trigonal planar in xz plane
    const out = [];
    for (let k = 0; k < n; k++) {
      const a = (k / 3) * TAU;
      out.push([Math.cos(a) * bondLen, 0, Math.sin(a) * bondLen]);
    }
    return out;
  }
  if (total === 4) {
    // tetrahedral
    const tv = tetraVerts(bondLen);
    return tv.slice(0, n);
  }
  if (total === 5) {
    // trigonal bipyramidal: 3 equatorial + 2 axial
    const out = [];
    for (let k = 0; k < Math.min(n, 3); k++) {
      const a = (k / 3) * TAU;
      out.push([Math.cos(a) * bondLen, 0, Math.sin(a) * bondLen]);
    }
    if (n >= 4) out.push([0, bondLen, 0]);
    if (n >= 5) out.push([0, -bondLen, 0]);
    return out;
  }
  if (total === 6) {
    // octahedral: +x,-x,+y,-y,+z,-z
    const slots = [
      [bondLen,0,0],[-bondLen,0,0],
      [0,bondLen,0],[0,-bondLen,0],
      [0,0,bondLen],[0,0,-bondLen],
    ];
    return slots.slice(0, n);
  }
  // fallback: spread on a circle
  const out = [];
  for (let k = 0; k < n; k++) {
    const a = (k / n) * TAU;
    out.push([Math.cos(a) * bondLen, 0, Math.sin(a) * bondLen]);
  }
  return out;
}

function shapeLabel(bonded, lonePairs) {
  const total = bonded + lonePairs;
  if (total === 2) return 'Linear';
  if (total === 3) return lonePairs === 0 ? 'Trigonal planar' : 'Bent';
  if (total === 4) {
    if (lonePairs === 0) return 'Tetrahedral';
    if (lonePairs === 1) return 'Trigonal pyramidal';
    return 'Bent';
  }
  if (total === 5) {
    if (lonePairs === 0) return 'Trigonal bipyramidal';
    if (lonePairs === 1) return 'Seesaw';
    return 'T-shaped';
  }
  if (total === 6) {
    if (lonePairs === 0) return 'Octahedral';
    if (lonePairs === 1) return 'Square pyramidal';
    return 'Square planar';
  }
  return 'Molecular';
}

function idealAngle(bonded, lonePairs) {
  const total = bonded + lonePairs;
  if (total === 2) return 180;
  if (total === 3) return 120;
  if (total === 4) return lonePairs === 0 ? 109.5 : 107 - lonePairs * 1.5;
  if (total === 5) return 120;
  if (total === 6) return 90;
  return 109.5;
}

// ---------- Central-atom selection ----------
// Heuristic: prefer the element that appears exactly once and is the least electronegative
// (typically the "skeleton" atom). For organics, prefer Carbon. Hydrogen is never central.
function pickCentral(counts) {
  const entries = Object.entries(counts).filter(([sym]) => sym !== 'H');
  if (entries.length === 0) {
    // diatomic of H or single element
    const syms = Object.keys(counts);
    return syms[0];
  }
  // single-occurrence non-H atoms are strong central candidates
  const singletons = entries.filter(([, c]) => c === 1).map(([s]) => s);
  if (singletons.length) {
    if (singletons.includes('C')) return 'C';
    singletons.sort((a, b) => (getBySymbol(a).en || 0) - (getBySymbol(b).en || 0));
    return singletons[0];
  }
  // otherwise least electronegative non-H element
  entries.sort((a, b) => (getBySymbol(a[0]).en || 0) - (getBySymbol(b[0]).en || 0));
  return entries[0][0];
}

// ---------- Bond-order inference ----------
// For a central atom with `bonded` terminals and known valence, decide if bonds should
// be upgraded to double/triple so the central atom reaches an octet (or duet for H).
function inferBondOrder(centralEl, terminalEl, bondedCount, lonePairs) {
  const cen = getBySymbol(centralEl);
  const term = getBySymbol(terminalEl);
  if (!cen || !term) return 1;
  // Octet electrons the central atom wants to share via bonds = 8 - 2*lonePairs
  const wanted = Math.max(2, 8 - 2 * lonePairs);
  const electronsViaSingleBonds = bondedCount; // each single bond contributes 1 shared electron to central's count
  const deficit = wanted - 2 * lonePairs - electronsViaSingleBonds;
  if (bondedCount === 1) {
    // diatomic-ish: order from octet deficit of the two
    const cenWant = Math.min(3, Math.max(1, Math.ceil((8 - cen.valence) / 2)));
    const termWant = Math.min(3, Math.max(1, Math.ceil((term.valence === 1 ? 2 : 8 - term.valence) / 2)));
    return Math.max(1, Math.min(3, Math.min(cenWant, termWant)));
  }
  if (bondedCount === 2 && deficit > 0) return 2;
  return 1;
}

// ---------- Ionic detection ----------
function isIonicCompound(counts) {
  const syms = Object.keys(counts);
  if (syms.length !== 2) return false;
  const cats = syms.map((s) => getBySymbol(s));
  if (cats.some((c) => !c)) return false;
  const hasMetal = cats.some((c) => isMetal(c.category));
  const hasNonmetal = cats.some((c) => isNonmetal(c.category));
  return hasMetal && hasNonmetal;
}

function buildIonicLattice(counts) {
  const syms = Object.keys(counts);
  const metals = syms.filter((s) => isMetal(getBySymbol(s).category));
  const nonmetals = syms.filter((s) => isNonmetal(getBySymbol(s).category));
  const m = metals[0] || syms[0];
  const x = nonmetals[0] || syms[1];
  const atoms = [];
  const bonds = [];
  const sp = 1.55;
  const idx = (i, j, k) => i * 9 + j * 3 + k;
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) for (let k = 0; k < 3; k++) {
    const cation = (i + j + k) % 2 === 0;
    atoms.push({
      el: cation ? m : x,
      pos: [(i - 1) * sp, (j - 1) * sp, (k - 1) * sp],
    });
    if (i > 0) bonds.push({ a: idx(i - 1, j, k), b: idx(i, j, k), order: 1 });
    if (j > 0) bonds.push({ a: idx(i, j - 1, k), b: idx(i, j, k), order: 1 });
    if (k > 0) bonds.push({ a: idx(i, j, k - 1), b: idx(i, j, k), order: 1 });
  }
  return { atoms, bonds, ionic: true, shape: 'Ionic lattice', note: `Ionic lattice of ${m}⁺ and ${x}⁻ in a repeating cube`, central: null };
}

// ---------- Main builder ----------
export function buildMolecule(input) {
  const parsed = parseFormula(input);
  if (!parsed.ok) return { ok: false, error: parsed.error };

  // Diatomic / single-element (H2, O2, N2, Cl2, P4, S8...)
  const distinct = parsed.atoms.length;
  if (distinct === 1) {
    return buildSingleElement(parsed);
  }

  // Ionic: render as lattice fragment
  if (isIonicCompound(parsed.counts)) {
    const result = buildIonicLattice(parsed.counts);
    return { ok: true, ...result };
  }

  // Check exceptions registry first
  const canon = canonicalFormula(parsed.counts);
  if (EXCEPTIONS[canon]) {
    return { ok: true, ...EXCEPTIONS[canon](parsed) };
  }

  // Generic VSEPR build
  return buildGeneric(parsed);
}

// Canonical key from counts (e.g. H2O -> "H2O1") so exception lookup is order-independent.
function canonicalFormula(counts) {
  return Object.keys(counts).sort().map((s) => s + counts[s]).join('');
}

function buildSingleElement(parsed) {
  const el = parsed.atoms[0].el;
  const n = parsed.atoms[0].count;
  const e = getBySymbol(el);
  if (!e) return { ok: false, error: `Unknown element ${el}` };
  const bondLen = (e.radius + e.radius) * SCALE * 0.55;
  if (n === 1) {
    return { ok: true, atoms: [{ el, pos: [0, 0, 0] }], bonds: [], shape: 'Single atom', note: `A single ${e.name} atom`, central: el };
  }
  if (n === 2) {
    const order = ['N','C'].includes(el) ? 3 : ['O','S'].includes(el) ? 2 : 1;
    const atoms = [{ el, pos: [-bondLen / 2, 0, 0] }, { el, pos: [bondLen / 2, 0, 0] }];
    return { ok: true, atoms, bonds: [{ a: 0, b: 1, order }], shape: 'Diatomic', note: `${el}₂ — ${order === 3 ? 'triple' : order === 2 ? 'double' : 'single'} bond`, central: null };
  }
  // For n>=3 (P4, S8...) build a ring/tetrahedron approximation
  if (n === 4) {
    // tetrahedron (white phosphorus P4)
    const tv = tetraVerts(bondLen / 1.6);
    const atoms = tv.map((p) => ({ el, pos: p }));
    const bonds = [];
    for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) bonds.push({ a: i, b: j, order: 1 });
    return { ok: true, atoms, bonds, shape: 'Tetrahedral cluster', note: `${el}₄ tetrahedral cluster (e.g. white phosphorus)`, central: null };
  }
  // ring
  const atoms = [];
  const bonds = [];
  const ringR = bondLen / (2 * Math.sin(Math.PI / n));
  for (let i = 0; i < n; i++) {
    const a = (i / n) * TAU;
    atoms.push({ el, pos: [Math.cos(a) * ringR, 0, Math.sin(a) * ringR] });
    bonds.push({ a: i, b: (i + 1) % n, order: 1 });
  }
  return { ok: true, atoms, bonds, shape: `${n}-membered ring`, note: `${el}_${n} ring allotrope`, central: null };
}

function buildGeneric(parsed) {
  const centralSym = pickCentral(parsed.counts);
  const cenEl = getBySymbol(centralSym);
  if (!cenEl) return { ok: false, error: `Cannot resolve central element ${centralSym}` };

  // Build the terminal atom list (everything except one central atom)
  const terminals = [];
  for (const { el, count } of parsed.atoms) {
    const use = el === centralSym ? count - 1 : count;
    for (let i = 0; i < use; i++) terminals.push(el);
  }
  if (terminals.length === 0) {
    return buildSingleElement({ atoms: [{ el: centralSym, count: 1 }] });
  }

  const bondedCount = terminals.length;
  const cenValence = cenEl.valence;
  // Octet-based lone-pair estimate for the central atom:
  // electrons left for lone pairs = valence - bondedCount (each single bond uses 1 of its electrons)
  const lpElectrons = Math.max(0, cenValence - bondedCount);
  let lonePairs = Math.floor(lpElectrons / 2);
  // Cap total steric number at 6
  if (bondedCount + lonePairs > 6) lonePairs = Math.max(0, 6 - bondedCount);

  const avgTermRadius = terminals.reduce((s, sym) => s + getBySymbol(sym).radius, 0) / terminals.length;
  const bondLen = (cenEl.radius + avgTermRadius) * SCALE;

  const positions = placeTerminals(bondedCount, lonePairs, bondLen);
  const atoms = [{ el: centralSym, pos: [0, 0, 0] }];
  positions.forEach((p) => atoms.push({ el: terminals.shift(), pos: p }));

  // Bond order inference (uniform — first guess)
  const order = inferBondOrder(centralSym, terminals[0] || centralSym, bondedCount, lonePairs);
  const bonds = [];
  for (let i = 1; i <= bondedCount; i++) bonds.push({ a: 0, b: i, order });

  const shape = shapeLabel(bondedCount, lonePairs);
  const angle = idealAngle(bondedCount, lonePairs);
  const note = `${shape} geometry · ~${angle}° bond angle`;

  return { ok: true, atoms, bonds, shape, ionic: false, note, central: centralSym, angle };
}

// ---------- Exceptions registry ----------
// Hand-built geometry for cases VSEPR/infra can't infer well.
// Each entry is keyed by the canonical formula and returns the same shape as buildMolecule.
const EXCEPTIONS = {};

// Water — bent, 104.5°
EXCEPTIONS['H2O1'] = () => {
  const a = (104.5 / 2) * (Math.PI / 180);
  const r = 0.96 * SCALE;
  return {
    ok: true,
    atoms: [
      { el: 'O', pos: [0, 0.25 * SCALE, 0] },
      { el: 'H', pos: [Math.sin(a) * r, (0.25 - Math.cos(a)) * SCALE, 0] },
      { el: 'H', pos: [-Math.sin(a) * r, (0.25 - Math.cos(a)) * SCALE, 0] },
    ],
    bonds: [{ a: 0, b: 1, order: 1 }, { a: 0, b: 2, order: 1 }],
    shape: 'Bent',
    note: 'Bent — 104.5° between the O–H bonds',
    central: 'O',
    angle: 104.5,
  };
};

// Ammonia — trigonal pyramidal
EXCEPTIONS['H3N1'] = () => {
  const r = 1.01 * SCALE;
  const atoms = [{ el: 'N', pos: [0, 0.34 * SCALE, 0] }];
  for (let i = 0; i < 3; i++) {
    const a = (i / 3) * TAU;
    atoms.push({ el: 'H', pos: [Math.cos(a) * r, -0.34 * SCALE, Math.sin(a) * r] });
  }
  return {
    ok: true, atoms,
    bonds: [{ a: 0, b: 1, order: 1 }, { a: 0, b: 2, order: 1 }, { a: 0, b: 3, order: 1 }],
    shape: 'Trigonal pyramidal', note: 'Pyramidal — a lone pair sits on top of the nitrogen',
    central: 'N', angle: 107,
  };
};

// Carbon dioxide — linear, two double bonds
EXCEPTIONS['C1O2'] = () => ({
  ok: true,
  atoms: [
    { el: 'C', pos: [0, 0, 0] },
    { el: 'O', pos: [1.16 * SCALE, 0, 0] },
    { el: 'O', pos: [-1.16 * SCALE, 0, 0] },
  ],
  bonds: [{ a: 0, b: 1, order: 2 }, { a: 0, b: 2, order: 2 }],
  shape: 'Linear', note: 'Linear — 180°, two double bonds', central: 'C', angle: 180,
});

// Sulfur hexafluoride — octahedral, hypervalent
EXCEPTIONS['F6S1'] = () => {
  const r = 1.56 * SCALE;
  const slots = [[r,0,0],[-r,0,0],[0,r,0],[0,-r,0],[0,0,r],[0,0,-r]];
  const atoms = [{ el: 'S', pos: [0, 0, 0] }, ...slots.map((p) => ({ el: 'F', pos: p }))];
  return {
    ok: true, atoms,
    bonds: [1,2,3,4,5,6].map((i) => ({ a: 0, b: i, order: 1 })),
    shape: 'Octahedral', note: 'Hypervalent — six single bonds in an octahedron',
    central: 'S', angle: 90,
  };
};

// Phosphorus pentachloride — trigonal bipyramidal, hypervalent
EXCEPTIONS['Cl5P1'] = () => {
  const r = 2.04 * SCALE;
  const atoms = [{ el: 'P', pos: [0, 0, 0] }];
  for (let k = 0; k < 3; k++) {
    const a = (k / 3) * TAU;
    atoms.push({ el: 'Cl', pos: [Math.cos(a) * r, 0, Math.sin(a) * r] });
  }
  atoms.push({ el: 'Cl', pos: [0, r, 0] });
  atoms.push({ el: 'Cl', pos: [0, -r, 0] });
  return {
    ok: true, atoms,
    bonds: [1,2,3,4,5].map((i) => ({ a: 0, b: i, order: 1 })),
    shape: 'Trigonal bipyramidal', note: 'Hypervalent — five single bonds, 3 equatorial + 2 axial',
    central: 'P', angle: 120,
  };
};

// Methane — perfect tetrahedron (also covered by generic, but pin the angle/note)
EXCEPTIONS['C1H4'] = () => {
  const r = 1.09 * SCALE;
  const tv = tetraVerts(r);
  return {
    ok: true,
    atoms: [{ el: 'C', pos: [0, 0, 0] }, ...tv.map((p) => ({ el: 'H', pos: p }))],
    bonds: [1,2,3,4].map((i) => ({ a: 0, b: i, order: 1 })),
    shape: 'Tetrahedral', note: 'Tetrahedral — 109.5° bond angles',
    central: 'C', angle: 109.5,
  };
};

// Benzene — flat hexagonal ring with alternating (drawn as 1.5) bonds
EXCEPTIONS['C6H6'] = () => {
  const r = 1.40 * SCALE;
  const atoms = [];
  const bonds = [];
  for (let i = 0; i < 6; i++) {
    const a = (i / 6) * TAU;
    atoms.push({ el: 'C', pos: [Math.cos(a) * r, 0, Math.sin(a) * r] });
    const a2 = ((i + 0.5) / 6) * TAU;
    atoms.push({ el: 'H', pos: [Math.cos(a2) * r * 1.75, 0, Math.sin(a2) * r * 1.75] });
  }
  for (let i = 0; i < 6; i++) {
    bonds.push({ a: i * 2, b: ((i + 1) % 6) * 2, order: i % 2 === 0 ? 2 : 1 });
    bonds.push({ a: i * 2, b: i * 2 + 1, order: 1 });
  }
  return {
    ok: true, atoms, bonds,
    shape: 'Planar hexagonal ring', note: 'Benzene — a flat ring with delocalised π electrons',
    central: null, angle: 120,
  };
};

export { EXCEPTIONS, idealAngle, shapeLabel, pickCentral, inferBondOrder, canonicalFormula };
