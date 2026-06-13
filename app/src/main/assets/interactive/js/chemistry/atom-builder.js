import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const ELEMENTS = [
  null,
  ['Hydrogen', 'H'], ['Helium', 'He'], ['Lithium', 'Li'], ['Beryllium', 'Be'], ['Boron', 'B'],
  ['Carbon', 'C'], ['Nitrogen', 'N'], ['Oxygen', 'O'], ['Fluorine', 'F'], ['Neon', 'Ne'],
  ['Sodium', 'Na'], ['Magnesium', 'Mg'], ['Aluminium', 'Al'], ['Silicon', 'Si'], ['Phosphorus', 'P'],
  ['Sulphur', 'S'], ['Chlorine', 'Cl'], ['Argon', 'Ar'], ['Potassium', 'K'], ['Calcium', 'Ca'],
];

const STABLE_N = [
  [], [0, 1], [1, 2], [3, 4], [5], [5, 6], [6, 7], [7, 8], [8, 9, 10], [10], [10, 11, 12],
  [12], [12, 13, 14], [14], [14, 15, 16], [16], [16, 17, 18, 20], [18, 20], [18, 20, 22], [20, 22], [20, 22, 23, 24, 26, 28],
];

const SHELL_CAP = [2, 8, 8, 4];
const MAX_P = 20;
const MAX_N = 30;
const MAX_E = 22;

export default function init(stage) {
  const engine = createEngine(stage);
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(12, quality.segments / 2);

  camera.position.set(0, 5, 16);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5,
    maxDistance: 40,
    enablePan: false,
    autoRotate: 0.06,
  });
  basicLights(scene);

  let protons = 1;
  let neutrons = 0;
  let electrons = 1;

  const nucleonGeo = new THREE.SphereGeometry(0.42, seg, seg);
  const protonMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.45 });
  const neutronMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.55 });
  const electronGeo = new THREE.SphereGeometry(0.2, seg, seg);
  const electronMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0x8a6d00, roughness: 0.3 });
  const ringMat = new THREE.LineBasicMaterial({ color: 0x3a4f70, transparent: true, opacity: 0.55 });

  const nucleusGroup = new THREE.Group();
  scene.add(nucleusGroup);
  const shellGroups = [];

  const nucleonPositions = [];
  (function generatePositions() {
    nucleonPositions.push(new THREE.Vector3(0, 0, 0));
    const golden = Math.PI * (3 - Math.sqrt(5));
    let placed = 1;
    let shell = 1;
    while (placed < MAX_P + MAX_N) {
      const count = Math.min(shell * 8 + 4, MAX_P + MAX_N - placed);
      const r = shell * 0.62;
      for (let i = 0; i < count; i++) {
        const y = 1 - (2 * (i + 0.5)) / count;
        const rad = Math.sqrt(1 - y * y);
        const th = golden * (placed + i);
        nucleonPositions.push(new THREE.Vector3(Math.cos(th) * rad * r, y * r, Math.sin(th) * rad * r));
      }
      placed += count;
      shell++;
    }
  })();

  function rebuildNucleus() {
    while (nucleusGroup.children.length) nucleusGroup.remove(nucleusGroup.children[0]);
    const order = [];
    let p = protons;
    let n = neutrons;
    while (p > 0 || n > 0) {
      if (p > 0) { order.push('p'); p--; }
      if (n > 0) { order.push('n'); n--; }
    }
    order.forEach((kind, i) => {
      const mesh = new THREE.Mesh(nucleonGeo, kind === 'p' ? protonMat : neutronMat);
      mesh.position.copy(nucleonPositions[i % nucleonPositions.length]);
      nucleusGroup.add(mesh);
    });
  }

  function rebuildShells() {
    shellGroups.forEach((g) => {
      scene.remove(g.group);
      g.ring.geometry.dispose();
    });
    shellGroups.length = 0;
    let remaining = electrons;
    for (let s = 0; s < SHELL_CAP.length && remaining > 0; s++) {
      const inShell = Math.min(SHELL_CAP[s], remaining);
      remaining -= inShell;
      const radius = 3.2 + s * 1.9;
      const group = new THREE.Group();
      group.rotation.x = 0.35 * (s % 2 === 0 ? 1 : -1);
      group.rotation.z = 0.18 * s;
      const pts = [];
      const nSeg = 72;
      for (let i = 0; i <= nSeg; i++) {
        const a = (i / nSeg) * Math.PI * 2;
        pts.push(new THREE.Vector3(Math.cos(a) * radius, 0, Math.sin(a) * radius));
      }
      const ringGeo = new THREE.BufferGeometry().setFromPoints(pts);
      const ring = new THREE.Line(ringGeo, ringMat);
      group.add(ring);
      const electronMeshes = [];
      for (let i = 0; i < inShell; i++) {
        const e = new THREE.Mesh(electronGeo, electronMat);
        const a = (i / inShell) * Math.PI * 2;
        e.position.set(Math.cos(a) * radius, 0, Math.sin(a) * radius);
        group.add(e);
        electronMeshes.push(e);
      }
      scene.add(group);
      shellGroups.push({ group, ring, radius, speed: 0.9 - s * 0.18 });
    }
  }

  const hud = createHud(stage);
  const symbolBadge = hud.badge('H', '#10B981');
  const ionBadge = hud.badge('Neutral atom', '#7dd3fc');
  const stableBadge = hud.badge('Stable', '#8be9a8');

  const panel = createPanel(stage, { title: 'Atom Builder' });
  panel.section('Protons (red)');
  panel.buttonRow([
    { label: '− proton', icon: 'remove', variant: 'ghost', onClick: () => { if (protons > 1) { protons--; refresh(); } } },
    { label: '+ proton', icon: 'add', onClick: () => { if (protons < MAX_P) { protons++; refresh(); } } },
  ]);
  panel.section('Neutrons (grey)');
  panel.buttonRow([
    { label: '− neutron', icon: 'remove', variant: 'ghost', onClick: () => { if (neutrons > 0) { neutrons--; refresh(); } } },
    { label: '+ neutron', icon: 'add', onClick: () => { if (neutrons < MAX_N) { neutrons++; refresh(); } } },
  ]);
  panel.section('Electrons (yellow)');
  panel.buttonRow([
    { label: '− electron', icon: 'remove', variant: 'ghost', onClick: () => { if (electrons > 0) { electrons--; refresh(); } } },
    { label: '+ electron', icon: 'add', onClick: () => { if (electrons < MAX_E) { electrons++; refresh(); } } },
  ]);
  panel.divider();
  const elemOut = panel.readout({ label: 'Element', value: 'Hydrogen' });
  const massOut = panel.readout({ label: 'Mass number A', value: '1' });
  const chargeOut = panel.readout({ label: 'Charge', value: '0' });
  const shellOut = panel.readout({ label: 'Shells', value: '1' });
  const hintInfo = panel.info('Add a proton and the element itself changes — protons define identity.');
  panel.button({
    label: 'Reset to hydrogen',
    icon: 'replay',
    variant: 'ghost',
    onClick: () => { protons = 1; neutrons = 0; electrons = 1; refresh(); },
  });

  function shellConfig() {
    const parts = [];
    let remaining = electrons;
    for (let s = 0; s < SHELL_CAP.length && remaining > 0; s++) {
      const inShell = Math.min(SHELL_CAP[s], remaining);
      parts.push(inShell);
      remaining -= inShell;
    }
    return parts.length ? parts.join(', ') : '0';
  }

  function refresh() {
    rebuildNucleus();
    rebuildShells();
    const el = ELEMENTS[protons];
    const charge = protons - electrons;
    const chargeStr = charge === 0 ? '0 (neutral)' : charge > 0 ? `+${charge} (cation)` : `${charge} (anion)`;
    const supe = charge === 0 ? '' : charge > 0 ? (charge === 1 ? '⁺' : `${charge}⁺`) : (charge === -1 ? '⁻' : `${-charge}⁻`);
    elemOut.set(`${el[0]} (${el[1]})`);
    massOut.set(`${protons + neutrons} (${protons}p + ${neutrons}n)`);
    chargeOut.set(chargeStr);
    shellOut.set(shellConfig());
    symbolBadge.set(`${el[1]}${supe} · A=${protons + neutrons}`);
    ionBadge.set(charge === 0 ? 'Neutral atom' : charge > 0 ? `Positive ion ${el[1]}${supe}` : `Negative ion ${el[1]}${supe}`);
    const stable = STABLE_N[protons].includes(neutrons);
    stableBadge.set(stable ? 'Stable nucleus' : 'Unstable (radioactive)');
    stableBadge.el.style.setProperty('--ix-hud-color', stable ? '#8be9a8' : '#f87171');
    if (charge !== 0) hintInfo.set(`This is an ion: ${protons} protons vs ${electrons} electrons gives a net charge of ${charge > 0 ? '+' : ''}${charge}.`);
    else if (!stable) hintInfo.set(`This isotope ${el[1]}-${protons + neutrons} is unstable — try a neutron count of ${STABLE_N[protons].join(' or ')}.`);
    else hintInfo.set(`${el[0]} with ${neutrons} neutrons is a stable isotope. Shell filling: ${shellConfig()}.`);
  }

  refresh();

  engine.setUpdate((dt, t) => {
    nucleusGroup.rotation.y += dt * 0.25;
    shellGroups.forEach((g) => {
      g.group.rotation.y += dt * g.speed;
    });
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
