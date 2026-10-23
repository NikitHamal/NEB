/**
 * Acid–base titration in 3D — 25.0 mL of 0.100 M acid (hydrochloric or ethanoic) in a conical flask
 * with an indicator, and 0.100 M NaOH in a 50 mL burette clamped above it. Open the tap (the flow
 * follows how far it is open) or add single drops; each drop lands as a coloured plume that swirling
 * mixes in. Every drop changes the pH, which is solved from the charge balance, so the curve, the
 * equivalence point (and for ethanoic acid the buffer region and the pH 8.7 end point) are real.
 */
import { solvePH, INDICATORS } from '../core/indicators2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { conicalFlask, burette, whiteTile } from '../core/handson/glass.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createChemLab, THREE } from './chem3d/stage.js';

const V0 = 25; const CA = 0.1; const CB = 0.1; const DROP = 0.05; const KA = 1.8e-5;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Acid-base titration', aim: 'Find the concentration of an acid', target: [0, 1.15, 0], camera: [1.3, 2.4, 4.9], minDistance: 1.8, maxDistance: 11 });
  if (!L) return null;
  const { engine, world, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Open the burette tap a little', '#2563eb');

  let acid = 'hcl'; let ind = 'phenolphthalein'; let added = 0; let tap = 0; let plume = 0; let swirl = 1; let pending = 0;
  const curve = [[0, 1]];

  const tile = whiteTile(); world.add(tile);
  const flask = conicalFlask({ color: 0xf3f8ff, opacity: 0.4 }); flask.group.position.y = 0.04; world.add(flask.group);
  const B = burette(); B.group.position.set(0, 1.75, 0); world.add(B.group);
  const steel = new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.85, roughness: 0.3 });
  const base = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.08, 1.0), new THREE.MeshStandardMaterial({ color: 0x2b2f36, roughness: 0.6 })); base.position.set(-0.55, 0.04, -0.1); world.add(base);
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 8.6, 16), steel); rod.position.set(-0.85, 4.3, -0.35); world.add(rod);
  for (const y of [3.2, 6.5]) {
    const boss = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.12, 0.16), steel); boss.position.set(-0.85, y, -0.35); world.add(boss);
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.95, 10), steel); arm.rotation.set(0, 0, Math.PI / 2); arm.position.set(-0.42, y, -0.18); arm.rotation.y = -0.38; world.add(arm);
    const jaw = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.016, 8, 20), new THREE.MeshStandardMaterial({ color: 0xc2410c, roughness: 0.7 })); jaw.rotation.x = Math.PI / 2; jaw.position.set(0, y, 0); world.add(jaw);
  }
  const meter = new THREE.Group(); meter.position.set(1.05, 0, 0.35); world.add(meter);
  const meterBody = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.32, 0.4), new THREE.MeshStandardMaterial({ color: 0xe5e7eb, roughness: 0.5 })); meterBody.position.y = 0.16; meter.add(meterBody);
  const lcd = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.14), new THREE.MeshBasicMaterial({ color: 0x0f2a1e })); lcd.position.set(0, 0.22, 0.201); meter.add(lcd);
  const probe = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 1.25, 12), new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.4 }));
  probe.position.set(0.1, 0.85, -0.12); probe.rotation.set(-0.12, 0, 0.24); world.add(probe);
  const cable = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(0.25, 1.45, -0.2), new THREE.Vector3(0.8, 1.55, -0.1), new THREE.Vector3(1.05, 0.5, 0.25)]), 30, 0.01, 6), probe.material); world.add(cable);
  const phText = L.label(); phText.el.style.font = '700 14px ui-monospace,Menlo,monospace'; phText.el.style.color = '#6ee7b7'; phText.el.style.background = 'rgba(6,26,18,0.92)';
  const readLbl = L.label();
  const plumeBlob = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 16), new THREE.MeshPhysicalMaterial({ color: 0xe64980, roughness: 0.1, transparent: true, opacity: 0, depthWrite: false }));
  plumeBlob.renderOrder = 4; world.add(plumeBlob);
  const drop = new THREE.Mesh(new THREE.SphereGeometry(0.022, 12, 8), new THREE.MeshPhysicalMaterial({ color: 0xeaf4ff, roughness: 0.05, transparent: true, opacity: 0.8 }));
  world.add(drop);
  const dropsInAir = [];

  const panel = createPanel(stage, { title: 'Titration' });
  panel.chips({ label: 'Acid in the flask (0.100 M, 25.0 mL)', options: [{ value: 'hcl', label: 'Hydrochloric (strong)' }, { value: 'eth', label: 'Ethanoic (weak)' }], value: 'hcl', onChange: (v) => { acid = v; reset(); } });
  panel.chips({ label: 'Indicator', options: Object.keys(INDICATORS).map((key) => ({ value: key, label: INDICATORS[key].label })), value: ind, onChange: (v) => { ind = v; } });
  const tapS = panel.slider({ label: 'Burette tap', min: 0, max: 100, step: 1, value: 0, format: (v) => (v === 0 ? 'closed' : v < 15 ? `dripping ${v} %` : `open ${v} %`), onChange: (v) => { tap = v / 100; } });
  panel.buttonRow([{ label: 'One drop', icon: 'water_drop', onClick: () => { pending += DROP; dropsInAir.push({ y: 0, v: 0 }); } }, { label: 'Restart', icon: 'replay', variant: 'ghost', onClick: reset }]);
  panel.toggle({ label: 'Swirl the flask', value: true, onChange: (v) => { swirl = v ? 1 : 0; } });
  const graph = canvasCard(panel.body, 1.45);
  const st = panel.stats([{ key: 'v', label: 'NaOH added' }, { key: 'pH', label: 'pH (meter)' }, { key: 'eq', label: 'Equivalence' }, { key: 'conc', label: 'Acid conc. from your titre' }]);
  panel.info('NaOH + HCl → NaCl + H₂O. Near the end point one drop changes the pH by several units, so slow to single drops when the colour starts to linger. Phenolphthalein suits both acids; methyl orange changes too early for ethanoic acid.');

  function pH(extra = 0) {
    const v = added + extra; const Vt = (V0 + v) / 1000;
    const nb = CB * v / 1000; const na = CA * V0 / 1000;
    return acid === 'hcl' ? solvePH(na / Vt, nb / Vt) : solvePH(0, nb / Vt, na / Vt, KA);
  }
  function reset() { added = 0; tap = 0; tapS.set(0); plume = 0; pending = 0; dropsInAir.length = 0; curve.length = 0; curve.push([0, pH()]); }
  reset();

  function drawGraph() {
    const { g, w, h } = graph.ctx();
    const ix = 30; const iy = 22; const iw = w - 40; const ih = h - 44;
    const X = (v) => ix + v / 50 * iw; const Y = (p) => iy + ih - p / 14 * ih;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('pH against volume of NaOH', 10, 14);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih);
    const [a, b] = INDICATORS[ind].range;
    g.fillStyle = 'rgba(230,73,128,0.12)'; g.fillRect(ix, Y(Math.min(14, b)), iw, Y(Math.max(0, a)) - Y(Math.min(14, b)));
    g.setLineDash([3, 4]); g.strokeStyle = 'rgba(160,190,255,0.35)'; g.beginPath(); g.moveTo(X(25), iy); g.lineTo(X(25), iy + ih); g.stroke(); g.setLineDash([]);
    g.strokeStyle = '#60a5fa'; g.lineWidth = 2; g.beginPath(); curve.forEach(([v, p], i) => { if (i) g.lineTo(X(v), Y(p)); else g.moveTo(X(v), Y(p)); }); g.stroke();
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#8ea0c2'; g.textAlign = 'center'; g.fillText('V(NaOH) / mL', ix + iw / 2, h - 6);
    g.textAlign = 'right'; g.fillText('14', ix - 4, iy + 8); g.fillText('7', ix - 4, Y(7) + 3); g.fillText('0', ix - 4, iy + ih);
  }

  const col = new THREE.Color(); const clear = new THREE.Color(0xf3f8ff); const tip = new THREE.Vector3(); const v3 = new THREE.Vector3();
  let tick = 0; let dropTimer = 0;
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    // flow: a stream when well open, drops when barely open
    const flow = tap < 0.15 ? tap * 1.2 : 0.2 + (tap - 0.15) * 1.6;
    if (tap > 0) {
      if (tap < 0.15) { dropTimer += dt * flow * 20; while (dropTimer > 1) { dropTimer -= 1; pending += DROP; dropsInAir.push({ y: 0, v: 0 }); } }
      else pending += flow * dt;
    }
    B.handle.rotation.x = -tap * Math.PI / 2;
    const add = Math.min(pending, 50 - added);
    if (add > 0) { const before = pH(); added += add; pending -= add; const after = pH(); plume = Math.min(1, plume + Math.abs(after - before) * 0.4 + add * 2); curve.push([added, after]); if (curve.length > 1500) curve.shift(); }
    plume *= Math.exp(-dt * (0.5 + 4 * swirl + flow * 2));
    B.set(added);
    flask.setVolume(V0 + added);
    const p = pH();
    const I = INDICATORS[ind];
    col.copy(clear).lerp(new THREE.Color(I.color(p)), I.alpha(p));
    flask.setColor(col, 0.42 + I.alpha(p) * 0.3);
    flask.group.rotation.y += swirl * dt * 1.2;
    flask.group.position.x = Math.sin(time * 6) * 0.01 * swirl;
    // the plume where the base lands shows the colour of a local excess
    const pl = INDICATORS[ind];
    const localPH = acid === 'hcl' ? 12.5 : 12.5;
    plumeBlob.material.color.set(pl.color(localPH));
    plumeBlob.material.opacity = Math.min(0.7, plume * pl.alpha(localPH) * 1.2);
    const sy = 0.04 + flask.surfaceY();
    const pr = Math.min(0.08 + plume * 0.12, flask.radiusAt(sy - 0.04 - 0.06) * 0.75);
    plumeBlob.scale.set(pr, Math.min(0.05 + plume * 0.06, (sy - 0.04) * 0.45), pr); plumeBlob.position.set(0, sy - Math.min(0.06, (sy - 0.04) * 0.5), 0);
    plumeBlob.visible = plumeBlob.material.opacity > 0.02;
    // falling drops from the tip
    B.tipWorld(tip); world.worldToLocal(tip);
    drop.visible = false;
    for (let i = dropsInAir.length - 1; i >= 0; i--) {
      const d = dropsInAir[i]; d.v += 9.8 * 2 * dt; d.y += d.v * dt;
      const y = tip.y - d.y;
      if (y <= sy) { dropsInAir.splice(i, 1); continue; }
      drop.visible = true; drop.position.set(tip.x, y, tip.z);
    }
    if ((tick++ & 3) === 0) drawGraph();
    phText.el.textContent = `pH ${fmt(p, 2)}`; phText.at(v3.set(1.05, 0.8 + 0.22, 0.56));
    readLbl.el.textContent = `${fmt(added, 2)} mL`; readLbl.at(v3.set(0.25, 0.8 + 1.75 + B.yOf(added), 0.1));
    const eq = acid === 'hcl' ? 25 : 25;
    st.v.set(`${fmt(added, 2)} mL`); st.pH.set(fmt(p, 2)); st.eq.set(`${eq.toFixed(2)} mL (pH ${acid === 'hcl' ? '7.00' : '8.72'})`);
    const endHit = I.alpha(p) > 0.25 && ind === 'phenolphthalein';
    st.conc.set(endHit || Math.abs(added - 25) < 0.06 ? `${fmt(CB * added / V0, 4)} M` : '—');
    badge.set(tap > 0.15 ? 'Running fast: slow down near 24 mL' : p > 6 && p < 10 ? 'The end point is here: one drop changes everything' : added > 26 ? 'Past the end point: the flask stays coloured' : 'Open the tap, then add drops near the end point');
  });
  engine.start();

  stage.__titration = { add: (ml) => { pending += ml; }, state: () => ({ added, pH: pH() }) };
  return { dispose() { panel.dispose(); hud.dispose(); phText.remove(); readLbl.remove(); flask.dispose(); L.dispose(); } };
}
