import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import {
  applyRealisticRenderer, realisticLights, polishedMaterial,
  makeGlowTexture, makeRadialSprite,
} from '../core/realism.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import {
  ELEMENTS, ELEMENT_MAP, CATEGORY_COLORS, CATEGORY_LABELS,
  electronConfiguration, configToString, shellPacking, commonNeutrons,
} from './elements-data.js';

// Stable-neutron counts for the first 20 elements (Z 1..20).
// Beyond Z=20 we show the typical neutron count without a stable/unstable verdict.
const STABLE_N = [
  [], [0, 1], [1, 2], [3, 4], [5], [5, 6], [6, 7], [7, 8], [8, 9, 10], [10], [10, 11, 12],
  [12], [12, 13, 14], [14], [14, 15, 16], [16], [16, 17, 18, 20], [18, 20], [18, 20, 22], [20, 22], [20, 22, 23, 24, 26, 28],
];

const MAX_P = 118;
const MAX_E = 120;

function buildPeriodicTable(stage, onPick) {
  const simShell = stage.closest('.ix-sim-shell');
  const host = simShell ? simShell.parentNode : stage;

  const wrap = document.createElement('div');
  wrap.className = 'ix-pt-wrap';

  const title = document.createElement('div');
  title.className = 'ix-pt-title';
  title.innerHTML = '<span class="material-symbols-outlined">grid_view</span>Periodic table — tap any element to build its atom';
  wrap.appendChild(title);

  const grid = document.createElement('div');
  grid.className = 'ix-pt-grid';

  const cellMap = new Map();

  ELEMENTS.forEach((row) => {
    const el = {
      z: row[0], symbol: row[1], name: row[2], category: row[4], group: row[9], period: row[10],
    };
    const cell = document.createElement('button');
    cell.type = 'button';
    cell.className = 'ix-pt-cell';
    cell.style.setProperty('--cat', CATEGORY_COLORS[el.category]);
    cell.title = `${el.name} (Z=${el.z})`;
    cell.dataset.z = String(el.z);
    cell.innerHTML =
      `<span class="ix-pt-cell-z">${el.z}</span>` +
      `<span class="ix-pt-cell-sym">${el.symbol}</span>` +
      `<span class="ix-pt-cell-name">${el.name}</span>`;

    let col = el.group, r = el.period;
    if (el.category === 'lanthanide') { r = 9; col = 3 + (el.z - 57); }
    if (el.category === 'actinide') { r = 10; col = 3 + (el.z - 89); }
    cell.style.gridColumn = String(col);
    cell.style.gridRow = String(r);

    cell.addEventListener('click', () => onPick(el.z));
    grid.appendChild(cell);
    cellMap.set(el.z, cell);
  });

  const scroll = document.createElement('div');
  scroll.className = 'ix-pt-scroll';
  scroll.appendChild(grid);
  wrap.appendChild(scroll);

  const legend = document.createElement('div');
  legend.className = 'ix-pt-legend';
  Object.entries(CATEGORY_LABELS).forEach(([key, label]) => {
    const item = document.createElement('span');
    item.className = 'ix-pt-legend-item';
    item.innerHTML = `<span class="ix-pt-dot" style="--cat:${CATEGORY_COLORS[key]}"></span>${label}`;
    legend.appendChild(item);
  });
  wrap.appendChild(legend);

  if (simShell) simShell.insertAdjacentElement('afterend', wrap);
  else host.appendChild(wrap);

  function setActive(z) {
    cellMap.forEach((cell, zz) => cell.classList.toggle('active', zz === z));
  }
  function dispose() { if (wrap.parentNode) wrap.parentNode.removeChild(wrap); }
  return { el: wrap, setActive, dispose };
}

export default function init(stage) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(16, quality.segments / 2);

  applyRealisticRenderer(engine, { exposure: 1.1, envBackground: false });
  realisticLights(scene, { shadows: quality.shadows, shadowMap: quality.tier === 'low' ? 512 : 1024 });
  scene.fog = new THREE.FogExp2(0x0a1424, 0.012);

  const backdrop = new THREE.Mesh(
    new THREE.SphereGeometry(120, 24, 16),
    new THREE.MeshBasicMaterial({ color: 0x0a1424, side: THREE.BackSide })
  );
  scene.add(backdrop);

  camera.position.set(0, 5, 16);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5,
    maxDistance: 40,
    enablePan: false,
    autoRotate: 0.06,
  });

  let protons = 1;
  let neutrons = 0;
  let electrons = 1;

  const nucleonGeo = new THREE.SphereGeometry(0.42, seg, seg);
  const protonMat = polishedMaterial({
    color: 0xff5a4a, roughness: 0.28, metalness: 0.1, clearcoat: 1,
    emissive: 0x5a0f08, emissiveIntensity: 0.35,
  });
  const neutronMat = polishedMaterial({
    color: 0xaeb6c4, roughness: 0.4, metalness: 0.2, clearcoat: 0.6,
  });
  const electronGeo = new THREE.SphereGeometry(0.2, seg, seg);
  const electronMat = polishedMaterial({
    color: 0xffd24a, roughness: 0.18, metalness: 0.1, clearcoat: 1,
    emissive: 0x9a6a00, emissiveIntensity: 0.7,
  });
  const electronMatCore = new THREE.MeshBasicMaterial({ color: 0xfff2b0 });
  const orbitMat = new THREE.MeshStandardMaterial({
    color: 0x6fa0ff, emissive: 0x2a4a80, emissiveIntensity: 0.6,
    transparent: true, opacity: 0.5, roughness: 0.3, metalness: 0.4,
  });

  const nucleusGlowTex = makeGlowTexture(
    'rgba(255,120,90,0.9)', 'rgba(255,70,40,0.35)', 'rgba(255,60,30,0)'
  );
  const nucleusGlow = makeRadialSprite(nucleusGlowTex, { scale: 6.5, color: 0xff7a5a, opacity: 0.85 });
  scene.add(nucleusGlow);
  const electronGlowTex = makeGlowTexture(
    'rgba(255,225,120,0.85)', 'rgba(255,180,50,0.3)', 'rgba(255,160,30,0)'
  );

  const nucleusGroup = new THREE.Group();
  scene.add(nucleusGroup);
  const shellGroups = [];

  const MAX_NUCLEONS = 200;
  const nucleonPositions = [];
  (function generatePositions() {
    nucleonPositions.push(new THREE.Vector3(0, 0, 0));
    const golden = Math.PI * (3 - Math.sqrt(5));
    let placed = 1;
    let shell = 1;
    while (placed < MAX_NUCLEONS) {
      const count = Math.min(shell * 8 + 4, MAX_NUCLEONS - placed);
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
      mesh.castShadow = quality.shadows;
      nucleusGroup.add(mesh);
    });
  }

  function rebuildShells() {
    shellGroups.forEach((g) => {
      scene.remove(g.group);
      g.ring.geometry.dispose();
      g.cloud.geometry.dispose();
    });
    shellGroups.length = 0;
    const shells = shellPacking(electronConfiguration(Math.max(1, electrons)));
    shells.forEach((shell, s) => {
      if (shell.count === 0) return;
      const inShell = shell.count;
      const radius = 3.2 + s * 1.7;
      const group = new THREE.Group();
      group.rotation.x = 0.35 * (s % 2 === 0 ? 1 : -1);
      group.rotation.z = 0.18 * s;

      const orbit = new THREE.Mesh(new THREE.TorusGeometry(radius, 0.012, 8, 96), orbitMat);
      group.add(orbit);

      const cloudN = quality.tier === 'low' ? 40 : 90;
      const cloudPts = [];
      for (let i = 0; i < cloudN; i++) {
        const a = Math.random() * Math.PI * 2;
        const rr = radius + (Math.random() - 0.5) * 0.55;
        cloudPts.push(Math.cos(a) * rr, (Math.random() - 0.5) * 0.25, Math.sin(a) * rr);
      }
      const cloudGeo = new THREE.BufferGeometry();
      cloudGeo.setAttribute('position', new THREE.Float32BufferAttribute(cloudPts, 3));
      const cloud = new THREE.Points(cloudGeo, new THREE.PointsMaterial({
        color: 0x9fc4ff, size: 0.05, transparent: true, opacity: 0.35,
        blending: THREE.AdditiveBlending, depthWrite: false,
      }));
      group.add(cloud);

      const electronMeshes = [];
      for (let i = 0; i < inShell; i++) {
        const e = new THREE.Mesh(electronGeo, electronMat);
        const core = new THREE.Mesh(new THREE.SphereGeometry(0.1, 12, 12), electronMatCore);
        e.add(core);
        const g = makeRadialSprite(electronGlowTex, { scale: 1.3, color: 0xffd24a, opacity: 0.95 });
        e.add(g);
        const a = (i / inShell) * Math.PI * 2;
        e.position.set(Math.cos(a) * radius, 0, Math.sin(a) * radius);
        e.userData.angle = a;
        e.userData.phase = Math.random() * Math.PI * 2;
        group.add(e);
        electronMeshes.push(e);
      }
      scene.add(group);
      shellGroups.push({ group, ring: orbit, cloud, electronMeshes, radius, speed: 0.9 - s * 0.18 });
    });
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
    { label: '+ neutron', icon: 'add', onClick: () => { if (neutrons < maxNeutrons()) { neutrons++; refresh(); } } },
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
  const cfgOut = panel.readout({ label: 'Electron config', value: '1s¹' });
  const catOut = panel.readout({ label: 'Category', value: 'Nonmetal' });
  const gpOut = panel.readout({ label: 'Group / Period', value: '1 / 1' });
  const hintInfo = panel.info('Add a proton and the element itself changes — protons define identity. Or tap the periodic table below to jump to any element.');
  panel.button({
    label: 'Reset to hydrogen',
    icon: 'replay',
    variant: 'ghost',
    onClick: () => { protons = 1; neutrons = 0; electrons = 1; refresh(); },
  });

  function maxNeutrons() {
    const typical = commonNeutrons(protons);
    return typical * 2 + 10;
  }

  function shellConfig() {
    const shells = shellPacking(electronConfiguration(Math.max(1, electrons)));
    return shells.length ? shells.map((s) => s.count).join(', ') : '0';
  }

  function refresh() {
    rebuildNucleus();
    rebuildShells();
    const el = ELEMENT_MAP[protons] || { symbol: '?', name: 'Unknown', mass: protons, valence: '?', category: '?', group: '?', period: '?' };
    const charge = protons - electrons;
    const chargeStr = charge === 0 ? '0 (neutral)' : charge > 0 ? `+${charge} (cation)` : `${charge} (anion)`;
    const supe = charge === 0 ? '' : charge > 0 ? (charge === 1 ? '⁺' : `${charge}⁺`) : (charge === -1 ? '⁻' : `${-charge}⁻`);
    elemOut.set(`${el.name} (${el.symbol})`);
    massOut.set(`${protons + neutrons} (${protons}p + ${neutrons}n)`);
    chargeOut.set(chargeStr);
    shellOut.set(shellConfig());
    const cfg = electronConfiguration(Math.max(1, electrons));
    cfgOut.set(configToString(cfg));
    catOut.set(CATEGORY_LABELS[el.category] || el.category || '—');
    gpOut.set(`${el.group === '?' ? '—' : el.group} / ${el.period === '?' ? '—' : el.period}`);
    symbolBadge.set(`${el.symbol}${supe} · A=${protons + neutrons}`);
    symbolBadge.el.style.setProperty('--ix-hud-color', CATEGORY_COLORS[el.category] || '#10B981');
    ionBadge.set(charge === 0 ? 'Neutral atom' : charge > 0 ? `Positive ion ${el.symbol}${supe}` : `Negative ion ${el.symbol}${supe}`);
    if (STABLE_N[protons]) {
      const stable = STABLE_N[protons].includes(neutrons);
      stableBadge.set(stable ? 'Stable nucleus' : 'Unstable (radioactive)');
      stableBadge.el.style.setProperty('--ix-hud-color', stable ? '#8be9a8' : '#f87171');
    } else {
      stableBadge.set('Heavy element');
      stableBadge.el.style.setProperty('--ix-hud-color', '#7dd3fc');
    }
    if (charge !== 0) hintInfo.set(`This is an ion: ${protons} protons vs ${electrons} electrons gives a net charge of ${charge > 0 ? '+' : ''}${charge}.`);
    else if (STABLE_N[protons] && !STABLE_N[protons].includes(neutrons)) hintInfo.set(`This isotope ${el.symbol}-${protons + neutrons} is unstable — try a neutron count of ${STABLE_N[protons].join(' or ')}.`);
    else hintInfo.set(`${el.name} with ${neutrons} neutrons. Shell filling: ${shellConfig()}.`);

    const shellCount = shellPacking(cfg).length;
    const atomScale = shellCount >= 6 ? 0.55 : shellCount >= 5 ? 0.72 : shellCount >= 4 ? 0.85 : 1;
    nucleusGroup.scale.setScalar(atomScale);
    shellGroups.forEach((g) => g.group.scale.setScalar(atomScale));

    pt.setActive(protons);
  }

  const pt = buildPeriodicTable(stage, (z) => {
    protons = z;
    electrons = z;
    neutrons = commonNeutrons(z);
    refresh();
  });

  refresh();

  engine.setUpdate((dt, t) => {
    nucleusGroup.rotation.y += dt * 0.25;
    nucleusGlow.scale.setScalar(6.5 + Math.sin(t * 2.5) * 0.4);
    shellGroups.forEach((g) => {
      g.group.rotation.y += dt * g.speed;
      g.cloud.rotation.z -= dt * 0.15;
      g.electronMeshes.forEach((e) => {
        e.userData.angle += dt * g.speed * 1.4;
        const a = e.userData.angle;
        e.position.x = Math.cos(a) * g.radius;
        e.position.z = Math.sin(a) * g.radius;
        e.position.y = Math.sin(t * 3 + e.userData.phase) * 0.18;
      });
    });
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose();
      panel.dispose();
      hud.dispose();
      pt.dispose();
      protonMat.dispose(); neutronMat.dispose();
      electronMat.dispose(); electronMatCore.dispose();
      nucleonGeo.dispose(); electronGeo.dispose();
      orbitMat.dispose();
      nucleusGlowTex.dispose(); electronGlowTex.dispose();
      engine.dispose();
    },
  };
}
