/**
 * Mix it up, in 3D. A beaker on a hot plate and, on the bench, water, oil, a salt shaker, a jar of
 * sand and a dropper of food colouring: tap one to add it. Salt dissolves (up to its real solubility,
 * about 36 g per 100 mL of water) faster when you stir; sand settles to the bottom and never
 * dissolves; oil rises and floats as a layer; a drop of colouring sinks through the oil and spreads
 * through the water by diffusion. Heat the beaker to boil the water off and the salt comes back as
 * crystals.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { beaker } from '../core/handson/glass.js';
import { createChemLab, bottle, THREE } from './chem3d/stage.js';
import { createHotPlate } from './chem3d/particles.js';

const CAP = 300; const SOLUBILITY = 0.36;
const S = 1.25; const RIN = 0.244 * S; const AREA = Math.PI * (RIN * 10) ** 2;
const H_OF = (ml) => ml / AREA / 10;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Mixing lab', aim: 'Dissolving, settling, floating and diffusing', target: [0, 1.0, 0], camera: [0.8, 2.3, 4.6], minDistance: 1.6, maxDistance: 9 });
  if (!L) return null;
  const { engine, world, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Tap the water bottle to start', '#2563eb');

  let water = 0; let oil = 0; let saltAdded = 0; let saltDis = 0; let sandG = 0; let heating = false; let stirT = 0; let dyeAmt = 0; let dyeSpread = 1;
  let dyeColor = new THREE.Color(0xe5484d);
  const plate = createHotPlate(); world.add(plate.group);
  const bk = beaker(0); bk.group.scale.setScalar(S); bk.group.position.y = 0.36; world.add(bk.group);
  const y0 = 0.36 + 0.012 * S;
  const waterMat = new THREE.MeshPhysicalMaterial({ color: 0xcfe6f7, roughness: 0.05, transparent: true, opacity: 0.45, clearcoat: 0.5, depthWrite: false });
  const waterM = new THREE.Mesh(new THREE.CylinderGeometry(RIN - 0.004, RIN - 0.004, 1, 40), waterMat); waterM.renderOrder = 3; world.add(waterM);
  const oilM = new THREE.Mesh(new THREE.CylinderGeometry(RIN - 0.004, RIN - 0.004, 1, 40), new THREE.MeshPhysicalMaterial({ color: 0xf2c94c, roughness: 0.05, transparent: true, opacity: 0.72, clearcoat: 0.5, depthWrite: false }));
  oilM.renderOrder = 3; world.add(oilM);
  const plume = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 14), new THREE.MeshPhysicalMaterial({ color: 0xe5484d, transparent: true, opacity: 0.7, roughness: 0.2, depthWrite: false }));
  plume.renderOrder = 4; world.add(plume);

  const GRAINS = 500;
  const grainMesh = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.019, 0), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.8 }), GRAINS);
  grainMesh.count = 0; world.add(grainMesh);
  const grains = [];
  const crystals = new THREE.InstancedMesh(new THREE.BoxGeometry(0.03, 0.03, 0.03), new THREE.MeshPhysicalMaterial({ color: 0xf8fafc, roughness: 0.15, clearcoat: 0.5, transparent: true, opacity: 0.9 }), 120);
  crystals.count = 0; world.add(crystals);
  const steam = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.22, depthWrite: false }), 60);
  steam.count = 0; steam.renderOrder = 7; world.add(steam);
  const puffs = Array.from({ length: 60 }, () => ({ a: 99 }));
  const spoon = new THREE.Group();
  const rodMat = new THREE.MeshStandardMaterial({ color: 0xd1d5db, metalness: 0.9, roughness: 0.25 });
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.4, 10), rodMat); rod.position.y = 0.7; spoon.add(rod);
  spoon.position.set(0.95, 0, 0.5); spoon.rotation.z = 0.2; spoon.userData.home = spoon.position.clone(); world.add(spoon);

  const items = {
    water: bottle('Water', 0x7cc4f2, { h: 1.05, r: 0.24 }),
    oil: bottle('Oil', 0xf2c94c, { h: 1.05, r: 0.24 }),
    salt: bottle('Salt', 0xffffff, { h: 0.7, r: 0.17, glass: 0xffffff }),
    sand: bottle('Sand', 0xd6b37a, { h: 0.6, r: 0.24 }),
    dye: bottle('Colouring', 0xe5484d, { h: 0.55, r: 0.11 }),
  };
  const spots = { water: [-1.5, -0.4], oil: [-1.0, -0.75], salt: [1.05, -0.7], sand: [1.55, -0.3], dye: [-1.75, 0.35] };
  Object.entries(items).forEach(([k, b]) => { b.position.set(spots[k][0], 0, spots[k][1]); b.userData.home = b.position.clone(); world.add(b); L.tappable(b, () => act(k)); });
  L.tappable(spoon, () => act('stir'));

  const panel = createPanel(stage, { title: 'Mixing lab' });
  panel.buttonRow([{ label: 'Water 50 mL', icon: 'water', onClick: () => act('water') }, { label: 'Oil 25 mL', icon: 'opacity', onClick: () => act('oil') }]);
  panel.buttonRow([{ label: 'Salt 5 g', icon: 'grain', onClick: () => act('salt') }, { label: 'Sand 10 g', icon: 'landscape', onClick: () => act('sand') }]);
  panel.buttonRow([{ label: 'Colouring', icon: 'colorize', onClick: () => act('dye') }, { label: 'Stir', icon: 'cyclone', onClick: () => act('stir') }]);
  panel.chips({ label: 'Food colouring', options: [{ value: 'e5484d', label: 'Red' }, { value: '2563eb', label: 'Blue' }, { value: '16a34a', label: 'Green' }], value: 'e5484d', onChange: (v) => { dyeColor = new THREE.Color(`#${v}`); } });
  const heatT = panel.toggle({ label: 'Heat the beaker (evaporate)', value: false, onChange: (h) => { heating = h; } });
  panel.button({ label: 'Empty and wash the beaker', icon: 'delete', variant: 'ghost', onClick: () => { water = oil = saltAdded = saltDis = sandG = dyeAmt = 0; grains.length = 0; heating = false; heatT.set(false); } });
  const st = panel.stats([{ key: 'water', label: 'Water' }, { key: 'oil', label: 'Oil layer' }, { key: 'salt', label: 'Salt dissolved' }, { key: 'solid', label: 'Solid at the bottom' }]);
  panel.info('A solution forms when the particles of a solute spread out among the water particles. Salt dissolves (until the water is saturated); sand does not. Oil does not mix with water: it is less dense, so it floats. Colouring spreads on its own by diffusion; stirring speeds dissolving up.');

  const queue = [];
  function act(kind) { queue.push({ kind, t: 0 }); }
  const v3 = new THREE.Vector3(); const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const sc = new THREE.Vector3(); const e3 = new THREE.Euler();
  const stream = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.01, 1, 8), new THREE.MeshPhysicalMaterial({ transparent: true, opacity: 0.75 }));
  stream.visible = false; world.add(stream);
  let crystalN = 0;
  const SAND = new THREE.Color(0xd6b37a); const SALT = new THREE.Color(0xffffff);

  engine.setUpdate((dt, time) => {
    controls.update(dt);
    Object.values(items).forEach((b) => { b.position.lerp(b.userData.home, 0.18); b.rotation.z *= 0.82; });
    spoon.position.lerp(spoon.userData.home, 0.15); spoon.rotation.z += (0.2 - spoon.rotation.z) * 0.15;
    stream.visible = false;
    const a = queue[0];
    if (a) {
      a.t += dt;
      const k = Math.min(1, a.t / 0.5) * (a.t > 1.9 ? Math.max(0, 1 - (a.t - 1.9) / 0.4) : 1);
      const e = k * k * (3 - 2 * k);
      const top = y0 + H_OF(water) + H_OF(oil);
      if (a.kind === 'stir') {
        spoon.position.lerpVectors(spoon.userData.home, v3.set(Math.cos(time * 9) * 0.12, y0 + 0.02, Math.sin(time * 9) * 0.12), e);
        spoon.rotation.z = 0.08 * e;
        if (a.t > 0.5 && a.t < 1.9) stirT = 1;
      } else {
        const b = items[a.kind];
        const over = a.kind === 'salt' || a.kind === 'dye' ? v3.set(-0.05, 1.55, 0) : v3.set(-0.45, 1.75, 0);
        b.position.lerpVectors(b.userData.home, over, e); b.rotation.z = -e * (a.kind === 'salt' || a.kind === 'dye' ? 2.6 : 1.9);
        if (a.t > 0.5 && a.t < 1.9) {
          const f = dt / 1.4;
          if (a.kind === 'water') { water = Math.min(CAP - oil, water + 50 * f); stream.visible = true; stream.material.color.setHex(0x9fd3f7); }
          if (a.kind === 'oil') { oil = Math.min(CAP - water, oil + 25 * f); stream.visible = true; stream.material.color.setHex(0xf2c94c); }
          if (a.kind === 'salt' || a.kind === 'sand') {
            const g = (a.kind === 'salt' ? 5 : 10) * f;
            if (a.kind === 'salt') saltAdded += g; else sandG += g;
            const n = Math.ceil(g * (a.kind === 'salt' ? 30 : 14));
            for (let i = 0; i < n && grains.length < GRAINS; i++) grains.push({ s: a.kind, x: (Math.random() - 0.5) * 0.08, z: (Math.random() - 0.5) * 0.08, y: 1.4, v: 0, rest: false, life: 1 });
          }
          if (a.kind === 'dye' && !a.done) { a.done = true; dyeAmt = Math.min(1, dyeAmt + 0.25); dyeSpread = 0; plume.material.color.copy(dyeColor); }
          if (stream.visible) { stream.position.set(-0.02, (1.6 + top) / 2, 0); stream.scale.set(1, Math.max(0.01, 1.6 - top), 1); }
        }
      }
      if (a.t > 2.3) queue.shift();
    }
    stirT = Math.max(0, stirT - dt * 0.6);
    // heating boils the water off; salt left behind crystallises
    plate.set(heating ? 0.9 : 0);
    if (heating && water > 0) water = Math.max(0, water - 9 * dt);
    const cap = water * SOLUBILITY;
    if (saltDis > cap) { const out = saltDis - cap; saltDis = cap; crystalN = Math.min(120, crystalN + out * 3); }
    const undissolved = saltAdded - saltDis - crystalN / 3;
    if (water > 1 && undissolved > 0 && saltDis < cap) saltDis += Math.min(undissolved, cap - saltDis, (0.25 + 2.5 * stirT) * Math.min(undissolved, 4) * dt);
    if (water <= 1 && saltDis > 0) { crystalN = Math.min(120, crystalN + saltDis * 3); saltDis = 0; }
    // layers
    const hw = H_OF(water); const ho = H_OF(oil);
    waterM.visible = water > 0.5; waterM.scale.y = Math.max(1e-3, hw); waterM.position.y = y0 + hw / 2;
    oilM.visible = oil > 0.5; oilM.scale.y = Math.max(1e-3, ho); oilM.position.y = y0 + hw + ho / 2;
    // colouring: a plume that sinks, then spreads through all the water
    dyeSpread = Math.min(1, dyeSpread + dt * (0.08 + stirT * 1.2));
    const dyeConc = water > 1 ? dyeAmt * 60 / Math.max(30, water) : 0;
    waterMat.color.set(0xcfe6f7).lerp(dyeColor, Math.min(0.85, dyeConc * dyeSpread));
    waterMat.opacity = 0.45 + Math.min(0.35, dyeConc * dyeSpread * 0.4);
    plume.visible = water > 1 && dyeSpread < 0.97 && dyeAmt > 0;
    if (plume.visible) { const r = RIN * (0.15 + 0.85 * dyeSpread); plume.scale.set(r, Math.max(0.03, hw * (0.2 + 0.8 * dyeSpread) / 2), r); plume.position.y = y0 + hw - plume.scale.y - (1 - dyeSpread) * hw * 0.3; plume.material.opacity = 0.75 * (1 - dyeSpread); }
    // grains: salt grains fall, settle and vanish as they dissolve; sand stays as a pile
    const saltLeftFrac = saltAdded > 0 ? Math.max(0, undissolved) / saltAdded : 0;
    let n = 0; let saltSeen = 0;
    for (let i = 0; i < grains.length; i++) {
      const g = grains[i];
      const floor = y0 + 0.006 + (g.s === 'sand' ? Math.min(0.06, sandG * 0.0012) * (1 - Math.hypot(g.x, g.z) / RIN) : 0);
      const inLiq = g.y < y0 + hw + ho;
      g.v = inLiq ? g.v + (-0.25 - g.v) * (1 - Math.exp(-dt * 8)) : g.v - 9.8 * 0.4 * dt;
      g.y = Math.max(floor, g.y + g.v * dt);
      if (g.y <= floor && !g.rest) { g.rest = true; const r = Math.sqrt(Math.random()) * RIN * 0.85; const an = Math.random() * 6.283; g.x = Math.cos(an) * r * (g.s === 'sand' ? 0.8 : 1); g.z = Math.sin(an) * r * (g.s === 'sand' ? 0.8 : 1); }
      if (g.s === 'salt') { saltSeen++; if (saltSeen > Math.ceil(saltLeftFrac * 30 * saltAdded)) continue; }
      if (n >= GRAINS) break;
      e3.set(i, i * 1.3, 0); q.setFromEuler(e3);
      m4.compose(v3.set(g.x, g.y, g.z), q, sc.setScalar(g.s === 'sand' ? 0.9 : 0.7)); grainMesh.setMatrixAt(n, m4);
      grainMesh.setColorAt(n, g.s === 'sand' ? SAND : SALT); n++;
    }
    grainMesh.count = n; grainMesh.instanceMatrix.needsUpdate = true; if (grainMesh.instanceColor) grainMesh.instanceColor.needsUpdate = true;
    const cn = Math.floor(crystalN);
    for (let i = 0; i < cn; i++) { const an = i * 2.4; const r = Math.sqrt((i + 0.5) / 120) * RIN * 0.85; q.setFromEuler(e3.set(i * 0.7, i * 1.1, i * 0.3)); m4.compose(v3.set(Math.cos(an) * r, y0 + 0.015, Math.sin(an) * r), q, sc.setScalar(0.6 + (i % 5) * 0.12)); crystals.setMatrixAt(i, m4); }
    crystals.count = cn; crystals.instanceMatrix.needsUpdate = true;
    let sn = 0;
    for (const p of puffs) {
      if (p.a > 1 && heating && water > 0 && Math.random() < dt * 8) { p.a = 0; p.x = (Math.random() - 0.5) * 0.3; p.z = (Math.random() - 0.5) * 0.3; }
      if (p.a > 1) continue;
      p.a += dt * 0.5;
      m4.compose(v3.set(p.x + Math.sin(time + p.x * 9) * 0.05, y0 + hw + ho + p.a * 1.1, p.z), q.identity(), sc.setScalar(0.05 + p.a * 0.18)); steam.setMatrixAt(sn++, m4);
    }
    steam.count = sn; steam.instanceMatrix.needsUpdate = true;
    const solid = Math.max(0, undissolved) + sandG + crystalN / 3;
    st.water.set(`${fmt(water, 0)} mL`); st.oil.set(oil > 0 ? `${fmt(oil, 0)} mL on top` : '—');
    st.salt.set(`${fmt(saltDis, 1)} g${water > 1 && saltDis >= cap - 0.01 && saltAdded > 0 ? ' (saturated)' : ''}`);
    st.solid.set(solid > 0.05 ? `${fmt(solid, 1)} g` : '—');
    badge.set(heating && water > 0 ? 'Boiling the water off…' : crystalN > 1 && water < 1 ? 'The salt has come back as crystals' : water > 1 && saltAdded > 0 && saltDis >= cap - 0.01 ? 'Saturated: no more salt will dissolve' : stirT > 0.1 ? 'Stirring speeds up dissolving' : water < 1 ? 'Tap the water bottle to start' : 'Add salt, sand, oil or a drop of colouring');
  });
  engine.start();

  stage.__mix = { act, state: () => ({ water, oil, saltAdded, saltDis, sandG }), heat: (h) => { heating = h; heatT.set(h); } };
  return { dispose() { panel.dispose(); hud.dispose(); L.dispose(); } };
}
