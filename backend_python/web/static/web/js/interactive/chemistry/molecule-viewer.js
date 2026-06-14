import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard, hideInfoCard } from '../core/sim-ui.js';
import { getBySymbol } from './elements-data.js';
import { parseFormula, buildMolecule } from './molecule-builder.js';

// Richer info text for the most common elements; others fall back to a generic line.
const ELEMENT_INFO = {
  H: 'The lightest and most abundant element in the universe. One proton, one electron. In molecules it always forms exactly one bond.',
  C: 'The backbone of life. Carbon forms four strong bonds and chains with itself endlessly — over ten million carbon compounds are known.',
  N: 'Makes up 78% of the air as N₂. In ammonia and proteins it forms three bonds and keeps one lone pair of electrons.',
  O: 'The element you breathe. Forms two bonds; its strong pull on electrons makes water polar and fuels combustion.',
  Na: 'A soft reactive metal. It gives away one electron to become Na⁺ — in salt it is locked in a lattice with chloride ions.',
  Cl: 'A green-yellow gas as Cl₂. It grabs one electron to become Cl⁻, pairing with sodium to make table salt, NaCl.',
};

// Visual sizes tuned for clean ball-and-stick models (NOT raw covalent radii).
// These are the proven values from the original viewer — small, proportional, never bloated.
// The original six elements get exact sizes + info; everything else uses a moderate fixed
// radius in the same range with colour/name pulled from the periodic-table dataset.
const ELEMENT_STYLE = {
  H:  { color: 0xf1f5f9, r: 0.33 },
  C:  { color: 0x374151, r: 0.50 },
  N:  { color: 0x3b82f6, r: 0.48 },
  O:  { color: 0xef4444, r: 0.47 },
  Na: { color: 0x8b5cf6, r: 0.45 },
  Cl: { color: 0x22c55e, r: 0.56 },
};

function elementStyle(el) {
  const known = ELEMENT_STYLE[el];
  if (known) {
    const e = getBySymbol(el);
    return {
      color: known.color,
      r: known.r,
      name: e ? e.name : el,
      info: ELEMENT_INFO[el] || (e ? `${e.name} (Z=${e.z}). A ${e.category.replace('-', ' ')} element.` : `${el}.`),
    };
  }
  const e = getBySymbol(el);
  if (!e) return { color: 0xcccccc, r: 0.45, name: el, info: `${el}.` };
  return {
    color: e.color,
    r: 0.45,
    name: e.name,
    info: ELEMENT_INFO[el] || `${e.name} (Z=${e.z}). A ${e.category.replace('-', ' ')} element.`,
  };
}

const S = 1.5;
const TET = [
  [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1],
].map((v) => new THREE.Vector3(...v).normalize());

// ---- Hand-built geometries for common molecules (most accurate) ----
function buildWater() {
  const a = (104.5 / 2) * (Math.PI / 180);
  return {
    atoms: [
      { el: 'O', p: [0, 0.25, 0] },
      { el: 'H', p: [Math.sin(a) * 0.96, 0.25 - Math.cos(a) * 0.96, 0] },
      { el: 'H', p: [-Math.sin(a) * 0.96, 0.25 - Math.cos(a) * 0.96, 0] },
    ],
    bonds: [[0, 1, 1], [0, 2, 1]],
    note: 'Bent — 104.5° between the O–H bonds',
  };
}
function buildCO2() {
  return {
    atoms: [
      { el: 'C', p: [0, 0, 0] }, { el: 'O', p: [1.16, 0, 0] }, { el: 'O', p: [-1.16, 0, 0] },
    ],
    bonds: [[0, 1, 2], [0, 2, 2]],
    note: 'Linear — 180°, two double bonds',
  };
}
function buildMethane() {
  const atoms = [{ el: 'C', p: [0, 0, 0] }];
  const bonds = [];
  TET.forEach((d, i) => {
    atoms.push({ el: 'H', p: [d.x * 1.09, d.y * 1.09, d.z * 1.09] });
    bonds.push([0, i + 1, 1]);
  });
  return { atoms, bonds, note: 'Tetrahedral — 109.5° bond angles' };
}
function buildAmmonia() {
  const atoms = [{ el: 'N', p: [0, 0.22, 0] }];
  const bonds = [];
  for (let i = 0; i < 3; i++) {
    const a = (i / 3) * Math.PI * 2;
    atoms.push({ el: 'H', p: [Math.cos(a) * 0.94, 0.22 - 0.38, Math.sin(a) * 0.94] });
    bonds.push([0, i + 1, 1]);
  }
  return { atoms, bonds, note: 'Pyramidal — a lone pair sits on top of the nitrogen' };
}
function buildO2() {
  return {
    atoms: [{ el: 'O', p: [0.6, 0, 0] }, { el: 'O', p: [-0.6, 0, 0] }],
    bonds: [[0, 1, 2]],
    note: 'A double bond joins the two oxygen atoms',
  };
}
function buildEthanol() {
  return {
    atoms: [
      { el: 'C', p: [-1.23, -0.25, 0.05] }, { el: 'C', p: [0.07, 0.51, 0] },
      { el: 'O', p: [1.16, -0.36, -0.05] }, { el: 'H', p: [1.97, 0.12, 0.1] },
      { el: 'H', p: [-2.1, 0.4, 0.1] }, { el: 'H', p: [-1.3, -0.9, 0.9] },
      { el: 'H', p: [-1.33, -0.87, -0.86] }, { el: 'H', p: [0.13, 1.15, 0.89] },
      { el: 'H', p: [0.1, 1.18, -0.85] },
    ],
    bonds: [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 4, 1], [0, 5, 1], [0, 6, 1], [1, 7, 1], [1, 8, 1]],
    note: 'Ethanol C₂H₅OH — the –OH group makes it an alcohol',
  };
}
function buildGlucose() {
  const atoms = [];
  const bonds = [];
  for (let i = 0; i < 6; i++) {
    const a = (i / 6) * Math.PI * 2;
    const y = i % 2 === 0 ? -0.26 : 0.26;
    atoms.push({ el: i === 0 ? 'O' : 'C', p: [Math.cos(a) * 1.45, y, Math.sin(a) * 1.45] });
    bonds.push([i, (i + 1) % 6, 1]);
  }
  for (let i = 1; i <= 4; i++) {
    const a = (i / 6) * Math.PI * 2;
    const dir = [Math.cos(a), 0, Math.sin(a)];
    const c = atoms[i].p;
    const oIdx = atoms.length;
    atoms.push({ el: 'O', p: [c[0] + dir[0] * 1.25, c[1] - 0.55, c[2] + dir[2] * 1.25] });
    bonds.push([i, oIdx, 1]);
    atoms.push({ el: 'H', p: [c[0] + dir[0] * 2.0, c[1] - 0.85, c[2] + dir[2] * 2.0] });
    bonds.push([oIdx, oIdx + 1, 1]);
    atoms.push({ el: 'H', p: [c[0] + dir[0] * 0.3, c[1] + 0.95, c[2] + dir[2] * 0.3] });
    bonds.push([i, oIdx + 2, 1]);
  }
  const c5 = atoms[5].p;
  const a5 = (5 / 6) * Math.PI * 2;
  const d5 = [Math.cos(a5), 0, Math.sin(a5)];
  const c6 = atoms.length;
  atoms.push({ el: 'C', p: [c5[0] + d5[0] * 1.3, c5[1] + 0.75, c5[2] + d5[2] * 1.3] });
  bonds.push([5, c6, 1]);
  atoms.push({ el: 'O', p: [c5[0] + d5[0] * 2.3, c5[1] + 1.45, c5[2] + d5[2] * 2.3] });
  bonds.push([c6, c6 + 1, 1]);
  atoms.push({ el: 'H', p: [c5[0] + d5[0] * 3.05, c5[1] + 1.1, c5[2] + d5[2] * 3.05] });
  bonds.push([c6 + 1, c6 + 2, 1]);
  atoms.push({ el: 'H', p: [c5[0] + d5[0] * 0.3, c5[1] - 0.85, c5[2] + d5[2] * 0.3] });
  bonds.push([5, c6 + 3, 1]);
  return { atoms, bonds, note: 'Glucose C₆H₁₂O₆ (simplified ring) — the sugar your cells burn' };
}
function buildNaCl() {
  const atoms = [];
  const bonds = [];
  const sp = 1.55;
  const idx = (i, j, k) => i * 9 + j * 3 + k;
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) for (let k = 0; k < 3; k++) {
    atoms.push({ el: (i + j + k) % 2 === 0 ? 'Na' : 'Cl', p: [(i - 1) * sp, (j - 1) * sp, (k - 1) * sp] });
    if (i > 0) bonds.push([idx(i - 1, j, k), idx(i, j, k), 1]);
    if (j > 0) bonds.push([idx(i, j - 1, k), idx(i, j, k), 1]);
    if (k > 0) bonds.push([idx(i, j, k - 1), idx(i, j, k), 1]);
  }
  return { atoms, bonds, ionic: true, note: 'Ionic lattice — Na⁺ and Cl⁻ alternate in a repeating cube' };
}

// Quick-pick registry: formula -> { label, build, zoom }
const KNOWN = {
  'H2O': { label: 'Water H₂O', build: buildWater, zoom: 8 },
  'CO2': { label: 'Carbon dioxide CO₂', build: buildCO2, zoom: 9 },
  'CH4': { label: 'Methane CH₄', build: buildMethane, zoom: 9 },
  'NH3': { label: 'Ammonia NH₃', build: buildAmmonia, zoom: 8 },
  'O2': { label: 'Oxygen O₂', build: buildO2, zoom: 8 },
  'C2H5OH': { label: 'Ethanol C₂H₅OH', build: buildEthanol, zoom: 11 },
  'C6H12O6': { label: 'Glucose C₆H₁₂O₆', build: buildGlucose, zoom: 14 },
  'NaCl': { label: 'Salt NaCl lattice', build: buildNaCl, zoom: 14 },
};

// Normalise a typed formula so it matches a KNOWN key (e.g. "c2h5oh" -> "C2H5OH").
function normaliseForLookup(formula) {
  let out = '';
  let expectUpper = true;
  for (const ch of formula) {
    if (/[a-zA-Z]/.test(ch)) {
      out += expectUpper ? ch.toUpperCase() : ch.toLowerCase();
      expectUpper = false;
    } else {
      out += ch;
      expectUpper = true;
    }
  }
  return out;
}

function formatFormulaBadge(formula) {
  const parsed = parseFormula(formula);
  if (!parsed.ok) return formula;
  const sup = '⁰¹²³⁴⁵⁶⁷⁸⁹';
  return parsed.atoms.map((a) => a.el + String(a.count).split('').map((d) => sup[parseInt(d, 10)] || d).join('')).join('');
}

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(14, quality.segments / 2);

  camera.position.set(0, 3, 9);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 3,
    maxDistance: 40,
    enablePan: false,
  });
  basicLights(scene);

  let group = null;
  let atomMeshes = [];
  let labelSprites = [];
  let spinning = true;
  let showLabels = false;
  let currentFormula = 'H2O';

  const hud = createHud(stage);
  const shapeBadge = hud.badge('Bent — 104.5°', '#10B981');
  const formulaBadge = hud.badge('H₂O', '#7dd3fc');

  function clearGroup() {
    if (!group) return;
    group.traverse((obj) => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material && obj.material.map) obj.material.map.dispose();
      if (obj.material) obj.material.dispose();
    });
    scene.remove(group);
    group = null;
    atomMeshes = [];
    labelSprites = [];
  }

  function makeBondMesh(a, b, order) {
    const meshes = [];
    const va = new THREE.Vector3(...a).multiplyScalar(S);
    const vb = new THREE.Vector3(...b).multiplyScalar(S);
    const dir = vb.clone().sub(va);
    const len = dir.length();
    const mid = va.clone().add(vb).multiplyScalar(0.5);
    const up = Math.abs(dir.y) > 0.93 * len ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0);
    const perp = dir.clone().cross(up).normalize();
    const offsets = order === 2 ? [-0.11, 0.11] : order === 3 ? [-0.16, 0, 0.16] : [0];
    offsets.forEach((off) => {
      const r = order >= 2 ? 0.07 : 0.1;
      const geo = new THREE.CylinderGeometry(r, r, len, 10);
      const mat = new THREE.MeshStandardMaterial({ color: 0xb8c4d8, roughness: 0.6 });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.copy(mid).addScaledVector(perp, off * S);
      mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
      meshes.push(mesh);
    });
    return meshes;
  }

  function loadFormula(formula) {
    clearGroup();
    hideInfoCard(stage);
    const trimmed = (formula || '').trim();
    if (!trimmed) return;

    const knownKey = normaliseForLookup(trimmed);
    let data, zoom;
    if (KNOWN[knownKey]) {
      data = KNOWN[knownKey].build();
      zoom = KNOWN[knownKey].zoom;
    } else {
      const result = buildMolecule(trimmed);
      if (!result.ok || !result.atoms || !result.atoms.length) {
        shapeBadge.set('Cannot build');
        shapeBadge.el.style.setProperty('--ix-hud-color', '#f87171');
        formulaBadge.set(trimmed);
        showInfoCard(stage, {
          title: 'Cannot build that molecule',
          body: (result.error || 'Unrecognised formula') + '. Try a formula like H₂O, CH₄, NaCl, C₆H₆ or SF₆.',
          color: '#f87171',
        });
        return;
      }
      data = result;
      const center = new THREE.Vector3();
      data.atoms.forEach((a) => center.add(new THREE.Vector3(a.pos[0], a.pos[1], a.pos[2])));
      center.multiplyScalar(1 / data.atoms.length);
      data.atoms = data.atoms.map((a) => ({ el: a.el, p: [a.pos[0] - center.x, a.pos[1] - center.y, a.pos[2] - center.z] }));
      data.bonds = (data.bonds || []).map((b) => ({ a: b.a, b: b.b, order: b.order }));
      const maxCoord = data.atoms.reduce((m, a) => Math.max(m, Math.abs(a.p[0]), Math.abs(a.p[1]), Math.abs(a.p[2])), 0);
      zoom = Math.max(7, maxCoord * 2.2);
    }

    group = new THREE.Group();
    data.atoms.forEach((atom) => {
      const style = elementStyle(atom.el);
      const scale = data.ionic ? 0.85 : 1;
      const geo = new THREE.SphereGeometry(style.r * S * scale, seg, seg);
      const mat = new THREE.MeshStandardMaterial({ color: style.color, roughness: 0.4, metalness: 0.05 });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(atom.p[0] * S, atom.p[1] * S, atom.p[2] * S);
      mesh.userData.el = atom.el;
      group.add(mesh);
      atomMeshes.push(mesh);
      const label = makeLabelSprite(atom.el, { scale: 0.7, fontSize: 38 });
      label.position.copy(mesh.position);
      label.position.y += style.r * S + 0.45;
      label.visible = showLabels;
      group.add(label);
      labelSprites.push(label);
    });
    (data.bonds || []).forEach((bond) => {
      const a = bond.a !== undefined ? bond.a : bond[0];
      const b = bond.b !== undefined ? bond.b : bond[1];
      const order = bond.order !== undefined ? bond.order : bond[2];
      makeBondMesh(data.atoms[a].p, data.atoms[b].p, order).forEach((m) => group.add(m));
    });
    scene.add(group);
    controls.setDistance(zoom);
    shapeBadge.set(data.note || data.shape || 'Molecule');
    shapeBadge.el.style.setProperty('--ix-hud-color', data.ionic ? '#a78bfa' : '#10B981');
    currentFormula = knownKey || trimmed;
    formulaBadge.set(formatFormulaBadge(currentFormula));
    atomCountOut.set(String(data.atoms.length));
    bondCountOut.set(String((data.bonds || []).length));
    shapeOut.set(data.shape || (data.ionic ? 'Ionic lattice' : 'Molecule'));
  }

  const panel = createPanel(stage, { title: 'Molecule Builder' });

  const inputWrap = document.createElement('div');
  inputWrap.className = 'ix-ctrl-row ix-formula-input';
  const input = document.createElement('input');
  input.type = 'text';
  input.value = 'H2O';
  input.placeholder = 'e.g. H2O, C6H6, NaCl';
  input.spellcheck = false;
  input.className = 'ix-formula-field';
  const buildBtn = document.createElement('button');
  buildBtn.type = 'button';
  buildBtn.className = 'ix-ctrl-btn';
  buildBtn.innerHTML = '<span class="material-symbols-outlined">play_arrow</span>Build';
  buildBtn.addEventListener('click', () => { const v = input.value.trim(); if (v) loadFormula(v); });
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') { const v = input.value.trim(); if (v) loadFormula(v); } });
  inputWrap.appendChild(input);
  inputWrap.appendChild(buildBtn);
  panel.body.appendChild(inputWrap);

  const chipsWrap = document.createElement('div');
  chipsWrap.className = 'ix-formula-chips';
  Object.keys(KNOWN).forEach((f) => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'ix-formula-chip';
    chip.textContent = KNOWN[f].label;
    chip.addEventListener('click', () => { input.value = f; loadFormula(f); });
    chipsWrap.appendChild(chip);
  });
  panel.body.appendChild(chipsWrap);

  panel.divider();
  const atomCountOut = panel.readout({ label: 'Atoms', value: '3' });
  const bondCountOut = panel.readout({ label: 'Bonds', value: '2' });
  const shapeOut = panel.readout({ label: 'Shape', value: 'Bent' });
  panel.toggle({
    label: 'Show atom labels',
    value: false,
    onChange: (v) => { showLabels = v; labelSprites.forEach((l) => { l.visible = v; }); },
  });
  panel.toggle({
    label: 'Spin',
    value: true,
    onChange: (v) => { spinning = v; },
  });
  panel.info('Type any chemical formula and press Build. The 8 quick-pick molecules use exact geometries; everything else is computed from VSEPR rules. Tap an atom to learn about its element.');

  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let downPos = null;
  function onDown(e) { downPos = { x: e.clientX, y: e.clientY }; }
  function onUp(e) {
    if (!downPos || Math.hypot(e.clientX - downPos.x, e.clientY - downPos.y) > 8) return;
    const rect = engine.canvas.getBoundingClientRect();
    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(atomMeshes, false);
    if (hits.length) {
      const el = hits[0].object.userData.el;
      const style = elementStyle(el);
      showInfoCard(stage, { title: `${style.name} (${el})`, body: style.info, color: '#10B981' });
    }
  }
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);

  loadFormula('H2O');

  engine.setUpdate((dt) => {
    if (group && spinning) group.rotation.y += dt * 0.35;
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown);
      engine.canvas.removeEventListener('pointerup', onUp);
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
