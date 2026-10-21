/**
 * Density tower in 3D, on the lab bench. Tap a bottle (or use the panel) to tip it into a tall
 * measuring cylinder, in any order: the liquids sort themselves by density (g/mL), a denser one
 * falling through the lighter layers as drops before joining its own layer. Then drop objects in:
 * each is pushed up by the weight of liquid it displaces (Archimedes), so it sinks until the liquid
 * around it is as dense as it is and floats there, often right on an interface between two layers.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, bottle, THREE } from './chem3d/stage.js';

const CAP = 480;
const R = 0.28; const AREA = Math.PI * (R * 10) * (R * 10);
const H_OF = (ml) => ml / AREA / 10;
const LIQ = [
  { id: 'honey', label: 'Honey', rho: 1.42, color: 0xd99a1e },
  { id: 'syrup', label: 'Corn syrup', rho: 1.33, color: 0x9b51e0 },
  { id: 'soap', label: 'Dish soap', rho: 1.06, color: 0x22c55e },
  { id: 'water', label: 'Water', rho: 1.0, color: 0x3b82f6 },
  { id: 'oil', label: 'Vegetable oil', rho: 0.92, color: 0xf5c518 },
  { id: 'alcohol', label: 'Rubbing alcohol', rho: 0.79, color: 0xef4444 },
];
const OBJ = [
  { id: 'cork', label: 'Cork', rho: 0.24, s: 0.11 },
  { id: 'ice', label: 'Ice cube', rho: 0.917, s: 0.1 },
  { id: 'tomato', label: 'Cherry tomato', rho: 1.03, s: 0.1 },
  { id: 'bead', label: 'Plastic bead', rho: 1.38, s: 0.06 },
  { id: 'nut', label: 'Steel nut', rho: 7.8, s: 0.07 },
];
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function objectMesh(id) {
  const g = new THREE.Group();
  if (id === 'cork') { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.085, 0.2, 24), new THREE.MeshStandardMaterial({ color: 0xb98552, roughness: 0.95 })); m.rotation.z = Math.PI / 2; g.add(m); }
  else if (id === 'ice') { const m = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.18, 2, 2, 2), new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, roughness: 0.12, transparent: true, opacity: 0.6, clearcoat: 1 })); m.rotation.set(0.3, 0.5, 0.1); g.add(m); }
  else if (id === 'tomato') { g.add(new THREE.Mesh(new THREE.SphereGeometry(0.1, 24, 16), new THREE.MeshPhysicalMaterial({ color: 0xd62d20, roughness: 0.25, clearcoat: 0.8 }))); const st = new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.03, 5), new THREE.MeshStandardMaterial({ color: 0x2f7d32 })); st.position.y = 0.1; g.add(st); }
  else if (id === 'bead') g.add(new THREE.Mesh(new THREE.SphereGeometry(0.06, 20, 14), new THREE.MeshPhysicalMaterial({ color: 0x2563eb, roughness: 0.2, clearcoat: 1 })));
  else {
    const shape = new THREE.Shape(); for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2; shape[i ? 'lineTo' : 'moveTo'](Math.cos(a) * 0.075, Math.sin(a) * 0.075); }
    const hole = new THREE.Path(); hole.absarc(0, 0, 0.035, 0, Math.PI * 2, true); shape.holes.push(hole);
    const geo = new THREE.ExtrudeGeometry(shape, { depth: 0.05, bevelEnabled: true, bevelSize: 0.006, bevelThickness: 0.006, bevelSegments: 2 }); geo.center();
    const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0xa8b0bb, metalness: 0.9, roughness: 0.32 })); m.rotation.x = 1.2; g.add(m);
  }
  g.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  return g;
}

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Density tower', aim: 'Liquids and objects settle by density', target: [0, 1.15, 0], camera: [1.2, 2.2, 5.6], minDistance: 2.2, maxDistance: 10 });
  if (!L) return null;
  const { engine, world, camera, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Tap a bottle to pour it into the cylinder', '#2563eb');

  const vol = new Float64Array(LIQ.length);
  const things = [];
  let pouring = null;

  // the measuring cylinder: hexagonal foot, tall wall, spout, printed scale
  const glass = new THREE.MeshPhysicalMaterial({ color: 0xeaf6ff, roughness: 0.04, transparent: true, opacity: 0.22, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
  const cylH = H_OF(CAP) + 0.25;
  const wall = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.018, R + 0.018, cylH, 48, 1, true), glass); wall.position.y = 0.06 + cylH / 2; wall.renderOrder = 6;
  const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.6, 0.06, 6), glass.clone()); foot.position.y = 0.03; foot.material.opacity = 0.45;
  const lip = new THREE.Mesh(new THREE.TorusGeometry(R + 0.02, 0.012, 8, 48), glass); lip.rotation.x = Math.PI / 2; lip.position.y = 0.06 + cylH;
  world.add(wall, foot, lip);
  const ink = new THREE.MeshBasicMaterial({ color: 0xf8fafc });
  for (let ml = 20; ml <= CAP; ml += 20) {
    const big = ml % 100 === 0;
    const t = new THREE.Mesh(new THREE.BoxGeometry(big ? 0.1 : 0.05, 0.006, 0.004), ink);
    t.position.set(-(big ? 0.05 : 0.025) + 0.02, 0.06 + H_OF(ml), R + 0.02); world.add(t);
  }
  const layerGroup = new THREE.Group(); layerGroup.position.y = 0.06; world.add(layerGroup);
  const layers = LIQ.map((l) => {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(R, R, 1, 48), new THREE.MeshPhysicalMaterial({ color: l.color, roughness: 0.08, transparent: true, opacity: l.id === 'water' || l.id === 'alcohol' ? 0.55 : 0.78, clearcoat: 0.6, depthWrite: false }));
    m.renderOrder = 4; m.visible = false; layerGroup.add(m); return m;
  });

  // the bottles, standing in an arc behind the cylinder
  const bottles = LIQ.map((l, i) => {
    const b = bottle(l.label, l.color, { h: 1.15, r: 0.26 });
    const a = -1.05 + i * 0.42;
    b.userData.home = new THREE.Vector3(Math.sin(a) * 2.3, 0, -Math.cos(a) * 1.0 - 0.3);
    b.position.copy(b.userData.home);
    world.add(b);
    L.tappable(b, () => pour(i));
    return b;
  });

  // drops of a denser liquid falling through the layers
  const DROPS = 140;
  const dropMesh = new THREE.InstancedMesh(new THREE.SphereGeometry(0.03, 10, 8), new THREE.MeshPhysicalMaterial({ roughness: 0.1, clearcoat: 1 }), DROPS);
  dropMesh.count = 0; dropMesh.renderOrder = 5; world.add(dropMesh);
  const drops = [];
  const stream = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.012, 1, 10), new THREE.MeshPhysicalMaterial({ transparent: true, opacity: 0.8, roughness: 0.1 }));
  stream.visible = false; world.add(stream);

  const panel = createPanel(stage, { title: 'Density tower' });
  panel.chips({ label: 'Pour a liquid', options: LIQ.map((l, i) => ({ value: String(i), label: l.label })), value: '', onChange: (v) => pour(+v) });
  panel.chips({ label: 'Drop an object in', options: OBJ.map((o) => ({ value: o.id, label: o.label })), value: '', onChange: (id) => dropObject(id) });
  panel.buttonRow([
    { label: 'Pour all', icon: 'shuffle', onClick: () => { queue.push(...[4, 0, 3, 5, 1, 2]); } },
    { label: 'Empty', icon: 'delete', variant: 'ghost', onClick: () => { vol.fill(0); drops.length = 0; things.forEach((t) => world.remove(t.mesh)); things.length = 0; queue.length = 0; } },
  ]);
  const st = panel.stats([{ key: 'total', label: 'Liquid in the cylinder' }, { key: 'layers', label: 'Layers' }, { key: 'top', label: 'Top layer' }, { key: 'bottom', label: 'Bottom layer' }]);
  const table = document.createElement('div');
  table.style.cssText = 'display:grid;grid-template-columns:1fr auto;gap:2px 12px;font:500 12px Poppins,system-ui,sans-serif;color:#cbd5e1;padding:8px 10px;border-radius:12px;background:rgba(255,255,255,0.04);flex-shrink:0';
  const hex = (c) => `#${c.toString(16).padStart(6, '0')}`;
  table.innerHTML = '<b style="color:#94a3b8;font-size:11px">Substance</b><b style="color:#94a3b8;font-size:11px">g/mL</b>' + LIQ.map((l) => `<span><i style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${hex(l.color)};margin-right:6px"></i>${l.label}</span><span>${l.rho.toFixed(2)}</span>`).join('') + OBJ.map((o) => `<span style="color:#94a3b8">${o.label}</span><span style="color:#94a3b8">${o.rho.toFixed(2)}</span>`).join('');
  panel.body.appendChild(table);
  panel.info('Density = mass ÷ volume. A denser liquid sinks below a lighter one, whatever order you pour them in. An object floats where the liquid around it is just as dense as it is.');

  const queue = [];
  const total = () => vol.reduce((s, v) => s + v, 0);
  const inFlight = () => drops.reduce((s, d) => s + d.ml, 0);
  function pour(i) { if (pouring) { queue.push(i); return; } if (total() + inFlight() >= CAP - 5) { badge.set('The cylinder is full: empty it first'); return; } pouring = { i, t: 0, poured: 0 }; }
  function stack() {
    const order = LIQ.map((l, i) => i).filter((i) => vol[i] > 0.05).sort((a, b) => LIQ[b].rho - LIQ[a].rho);
    let y = 0; const out = [];
    for (const i of order) { const h = H_OF(vol[i]); out.push({ i, y0: y, y1: y + h, rho: LIQ[i].rho }); y += h; }
    return out;
  }
  function dropObject(id) {
    const o = OBJ.find((x) => x.id === id);
    const mesh = objectMesh(id);
    const x = (Math.random() - 0.5) * 0.18; const z = (Math.random() - 0.5) * 0.18;
    mesh.position.set(x, 0.06 + cylH + 0.3, z);
    world.add(mesh);
    things.push({ o, mesh, v: 0, phase: Math.random() * 6 });
  }

  const m4 = new THREE.Matrix4(); const col = new THREE.Color(); const lbl = L.label(); const v3 = new THREE.Vector3();
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    if (!pouring && queue.length) pour(queue.shift());
    // pouring: lift and tip the bottle over the cylinder, stream into the top
    for (let i = 0; i < bottles.length; i++) {
      const b = bottles[i]; const home = b.userData.home;
      const active = pouring && pouring.i === i;
      const k = active ? Math.min(1, pouring.t / 0.8) : 0;
      const target = v3.set(-0.62, cylH + 0.55, 0);
      b.position.lerpVectors(home, target, k * k * (3 - 2 * k));
      b.rotation.z = -k * 1.95;
      b.rotation.y = 0;
    }
    stream.visible = false;
    if (pouring) {
      pouring.t += dt;
      const l = LIQ[pouring.i];
      if (pouring.t > 0.8 && pouring.t < 2.6) {
        const add = Math.min(CAP - total() - inFlight(), 70 * dt);
        if (add > 0) {
          pouring.poured += add;
          const n = Math.max(1, Math.round(add / 1.2));
          for (let d = 0; d < n && drops.length < DROPS; d++) drops.push({ i: pouring.i, ml: add / n, x: (Math.random() - 0.5) * 0.06, z: (Math.random() - 0.5) * 0.06, y: H_OF(total() + inFlight()) + 0.2, v: -0.4 - Math.random() * 0.3 });
          stream.visible = true;
          const top = 0.06 + H_OF(total());
          stream.position.set(-0.03, (cylH + 0.42 + top) / 2, 0); stream.scale.set(1, cylH + 0.42 - top, 1);
          stream.material.color.setHex(l.color);
        }
      }
      if (pouring.t > 3.4) pouring = null;
    }
    // drops fall through lighter layers to the top of their own (denser layers stay below)
    const S = stack();
    let n = 0;
    for (let k = drops.length - 1; k >= 0; k--) {
      const d = drops[k];
      let floor = 0;
      for (const s of S) if (s.rho >= LIQ[d.i].rho) floor = Math.max(floor, s.y1);
      const inLiquid = d.y < H_OF(total());
      d.v = inLiquid ? d.v + (-0.9 - d.v) * (1 - Math.exp(-dt * 6)) : d.v - 9.8 * 0.3 * dt;
      d.y += d.v * dt;
      if (d.y <= floor + 0.01) { vol[d.i] += d.ml; drops.splice(k, 1); continue; }
      if (n < DROPS) { m4.makeTranslation(d.x, 0.06 + d.y, d.z); dropMesh.setMatrixAt(n, m4); dropMesh.setColorAt(n, col.setHex(LIQ[d.i].color)); n++; }
    }
    dropMesh.count = n; dropMesh.instanceMatrix.needsUpdate = true; if (dropMesh.instanceColor) dropMesh.instanceColor.needsUpdate = true;
    // layers with gently curved interfaces
    layers.forEach((m) => { m.visible = false; });
    for (const s of S) { const m = layers[s.i]; m.visible = true; m.scale.y = Math.max(1e-3, s.y1 - s.y0); m.position.y = (s.y0 + s.y1) / 2; }
    // objects settle where the liquid around them is as dense as they are
    const surf = S.length ? S[S.length - 1].y1 : 0;
    for (const t of things) {
      const o = t.o; let eq = o.s;
      if (S.length) {
        const top = S[S.length - 1];
        if (o.rho < top.rho) eq = surf + o.s * (1 - 2 * o.rho / top.rho);
        else { eq = o.s; for (let q = S.length - 1; q >= 0; q--) if (S[q].rho > o.rho) { eq = S[q].y1 + o.s * (1 - 2 * Math.min(1, o.rho / S[q].rho)) * 0.5; break; } }
      }
      const y = t.mesh.position.y - 0.06;
      const inL = y < surf;
      const a = (eq - y) * (inL ? 18 : 0) - (inL ? 0 : 9.8 * 0.4);
      t.v += a * dt; t.v *= Math.exp(-dt * (inL ? 5 : 0.2));
      t.mesh.position.y = 0.06 + Math.max(o.s, y + t.v * dt);
      t.mesh.rotation.y += dt * 0.3;
      if (inL && Math.abs(eq - y) < 0.01) t.mesh.position.y += Math.sin(time * 2 + t.phase) * 0.0008;
    }
    const tot = total();
    st.total.set(`${fmt(tot, 0)} mL`); st.layers.set(String(S.length));
    st.top.set(S.length ? LIQ[S[S.length - 1].i].label : '—'); st.bottom.set(S.length ? LIQ[S[0].i].label : '—');
    if (pouring) badge.set(`Pouring ${LIQ[pouring.i].label} (${LIQ[pouring.i].rho.toFixed(2)} g/mL)`);
    else if (things.length) { const t = things[things.length - 1]; badge.set(`${t.o.label} (${t.o.rho} g/mL) settles where the liquid is as dense as it is`); }
    else if (S.length) badge.set(`${S.length} layer${S.length > 1 ? 's' : ''}: densest at the bottom, lightest on top`);
    if (S.length) { lbl.el.textContent = `${LIQ[S[S.length - 1].i].label} on top`; lbl.at(v3.set(R + 0.6, 0.8 + 0.06 + surf, 0)); } else lbl.el.style.opacity = '0';
  });
  engine.start();

  stage.__density = { pour, dropObject, vol: () => Array.from(vol), fill: (arr) => { arr.forEach((v, i) => { vol[i] = v; }); } };
  return { dispose() { panel.dispose(); hud.dispose(); lbl.remove(); L.dispose(); } };
}
