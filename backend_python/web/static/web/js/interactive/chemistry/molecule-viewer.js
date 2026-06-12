import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard, hideInfoCard } from '../core/sim-ui.js';

const ELEMENT_STYLE = {
  H: { color: 0xf1f5f9, r: 0.33, name: 'Hydrogen', info: 'The lightest and most abundant element in the universe. One proton, one electron. In molecules it always forms exactly one bond.' },
  C: { color: 0x374151, r: 0.5, name: 'Carbon', info: 'The backbone of life. Carbon forms four strong bonds and chains with itself endlessly — over ten million carbon compounds are known.' },
  N: { color: 0x3b82f6, r: 0.48, name: 'Nitrogen', info: 'Makes up 78% of the air as N₂. In ammonia and proteins it forms three bonds and keeps one lone pair of electrons.' },
  O: { color: 0xef4444, r: 0.47, name: 'Oxygen', info: 'The element you breathe. Forms two bonds; its strong pull on electrons makes water polar and fuels combustion.' },
  Na: { color: 0x8b5cf6, r: 0.45, name: 'Sodium', info: 'A soft reactive metal. It gives away one electron to become Na⁺ — in salt it is locked in a lattice with chloride ions.' },
  Cl: { color: 0x22c55e, r: 0.56, name: 'Chlorine', info: 'A green-yellow gas as Cl₂. It grabs one electron to become Cl⁻, pairing with sodium to make table salt, NaCl.' },
};

const S = 1.5;
const TET = [
  [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1],
].map((v) => new THREE.Vector3(...v).normalize());

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
      { el: 'C', p: [0, 0, 0] },
      { el: 'O', p: [1.16, 0, 0] },
      { el: 'O', p: [-1.16, 0, 0] },
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
      { el: 'C', p: [-1.23, -0.25, 0.05] },
      { el: 'C', p: [0.07, 0.51, 0] },
      { el: 'O', p: [1.16, -0.36, -0.05] },
      { el: 'H', p: [1.97, 0.12, 0.1] },
      { el: 'H', p: [-2.1, 0.4, 0.1] },
      { el: 'H', p: [-1.3, -0.9, 0.9] },
      { el: 'H', p: [-1.33, -0.87, -0.86] },
      { el: 'H', p: [0.13, 1.15, 0.89] },
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
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      for (let k = 0; k < 3; k++) {
        atoms.push({
          el: (i + j + k) % 2 === 0 ? 'Na' : 'Cl',
          p: [(i - 1) * sp, (j - 1) * sp, (k - 1) * sp],
        });
        if (i > 0) bonds.push([idx(i - 1, j, k), idx(i, j, k), 1]);
        if (j > 0) bonds.push([idx(i, j - 1, k), idx(i, j, k), 1]);
        if (k > 0) bonds.push([idx(i, j, k - 1), idx(i, j, k), 1]);
      }
    }
  }
  return { atoms, bonds, ionic: true, note: 'Ionic lattice — Na⁺ and Cl⁻ alternate in a repeating cube' };
}

const MOLECULES = {
  h2o: { label: 'Water H₂O', build: buildWater, zoom: 8 },
  co2: { label: 'Carbon dioxide CO₂', build: buildCO2, zoom: 9 },
  ch4: { label: 'Methane CH₄', build: buildMethane, zoom: 9 },
  nh3: { label: 'Ammonia NH₃', build: buildAmmonia, zoom: 8 },
  o2: { label: 'Oxygen O₂', build: buildO2, zoom: 8 },
  ethanol: { label: 'Ethanol C₂H₅OH', build: buildEthanol, zoom: 11 },
  glucose: { label: 'Glucose C₆H₁₂O₆', build: buildGlucose, zoom: 14 },
  nacl: { label: 'Salt NaCl lattice', build: buildNaCl, zoom: 14 },
};

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

  const hud = createHud(stage);
  const shapeBadge = hud.badge('Bent — 104.5°', '#10B981');

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
    const offsets = order === 2 ? [-0.11, 0.11] : [0];
    offsets.forEach((off) => {
      const geo = new THREE.CylinderGeometry(order === 2 ? 0.07 : 0.1, order === 2 ? 0.07 : 0.1, len, 10);
      const mat = new THREE.MeshStandardMaterial({ color: 0xb8c4d8, roughness: 0.6 });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.copy(mid).addScaledVector(perp, off * S);
      mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
      meshes.push(mesh);
    });
    return meshes;
  }

  function loadMolecule(key) {
    clearGroup();
    hideInfoCard(stage);
    const def = MOLECULES[key];
    const data = def.build();
    group = new THREE.Group();
    data.atoms.forEach((atom) => {
      const style = ELEMENT_STYLE[atom.el];
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
    data.bonds.forEach(([i, j, order]) => {
      makeBondMesh(data.atoms[i].p, data.atoms[j].p, order).forEach((m) => group.add(m));
    });
    scene.add(group);
    controls.setDistance(def.zoom);
    shapeBadge.set(data.note);
  }

  const panel = createPanel(stage, { title: 'Molecule Gallery' });
  panel.select({
    label: 'Molecule',
    options: Object.entries(MOLECULES).map(([value, def]) => ({ value, label: def.label })),
    value: 'h2o',
    onChange: (v) => loadMolecule(v),
  });
  panel.toggle({
    label: 'Show atom labels',
    value: false,
    onChange: (v) => {
      showLabels = v;
      labelSprites.forEach((l) => { l.visible = v; });
    },
  });
  panel.toggle({
    label: 'Spin',
    value: true,
    onChange: (v) => { spinning = v; },
  });
  panel.info('Drag to rotate and pinch to zoom. Tap any atom to learn about its element. Red = oxygen, white = hydrogen, dark grey = carbon.');

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
      const style = ELEMENT_STYLE[el];
      showInfoCard(stage, { title: `${style.name} (${el})`, body: style.info, color: '#10B981' });
    }
  }
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);

  loadMolecule('h2o');

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
