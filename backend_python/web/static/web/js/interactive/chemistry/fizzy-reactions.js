/**
 * Fizzy reactions in 3D: tip vinegar into a conical flask and spoon in baking soda.
 * NaHCO₃ + CH₃COOH → CH₃COONa + H₂O + CO₂. Household vinegar is about 5 % acetic acid
 * (0.83 mmol/mL) and baking soda is 84 g/mol, so the amounts set how much carbon dioxide can be made
 * (24 L per mole at room temperature) and which ingredient runs out first. A balloon on the neck
 * catches the gas and swells to the real volume made.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { conicalFlask } from '../core/handson/glass.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createChemLab, bottle, THREE } from './chem3d/stage.js';

const ACID = 0.05 / 60; const SODA_M = 84; const VM = 24000;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Fizzy reactions', aim: 'Vinegar and baking soda make carbon dioxide', target: [0, 1.0, 0], camera: [0.9, 2.1, 4.4], minDistance: 1.6, maxDistance: 8 });
  if (!L) return null;
  const { engine, world, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Tap the vinegar bottle to pour some in', '#2563eb');

  let vinegar = 0; let water = 0; let acidMol = 0; let sodaSolid = 0; let sodaAdded = 0; let co2 = 0; let co2Balloon = 0; let balloonOn = true; let t = 0; let rate = 0;
  const trace = [];
  const flask = conicalFlask({ color: 0xf3e6bb, opacity: 0.55 });
  flask.group.scale.setScalar(1.35); world.add(flask.group);
  const S = 1.35;
  const CAP = 180;

  const vin = bottle('Vinegar 5%', 0xf3e3b0, { h: 1.1, r: 0.25 }); vin.position.set(-1.25, 0, -0.35); vin.userData.home = vin.position.clone(); world.add(vin);
  const wat = bottle('Water', 0x9fd3f7, { h: 1.1, r: 0.25 }); wat.position.set(-1.9, 0, 0.05); wat.userData.home = wat.position.clone(); world.add(wat);
  const jar = new THREE.Group(); jar.position.set(1.3, 0, -0.2); world.add(jar);
  const jarGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.5, 32, 1, true), new THREE.MeshPhysicalMaterial({ color: 0xeaf6ff, roughness: 0.05, transparent: true, opacity: 0.3, depthWrite: false, side: THREE.DoubleSide }));
  jarGlass.position.y = 0.25; jarGlass.renderOrder = 5;
  const powder = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.3, 32), new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 1 }));
  powder.position.y = 0.16;
  const jarLabel = bottle('Baking soda', 0xffffff, { h: 0.5, r: 0.3 }).children[3]; jarLabel.position.y = 0.2;
  jar.add(powder, jarGlass, jarLabel);
  const spoon = new THREE.Group();
  const bowl = new THREE.Mesh(new THREE.SphereGeometry(0.07, 20, 10, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xc7ccd4, metalness: 0.9, roughness: 0.25, side: THREE.DoubleSide }));
  const handle = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.012, 0.5), bowl.material); handle.position.z = 0.3;
  const heap = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 8), powder.material); heap.scale.y = 0.5; heap.position.y = -0.01;
  spoon.add(bowl, handle, heap); spoon.position.set(1.3, 0.6, -0.2); spoon.userData.home = spoon.position.clone(); world.add(spoon);

  const balloonMat = new THREE.MeshPhysicalMaterial({ color: 0xd61f26, roughness: 0.35, clearcoat: 0.5, transparent: true, opacity: 0.92 });
  const balloon = new THREE.Group();
  const bBody = new THREE.Mesh(new THREE.SphereGeometry(1, 40, 24), balloonMat);
  const bNeck = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.16, 24, 1, true), balloonMat);
  const bLimp = new THREE.Mesh(new THREE.CapsuleGeometry(0.12, 0.32, 6, 16), balloonMat);
  balloon.add(bBody, bNeck, bLimp);
  balloon.position.y = 1.42 * S; world.add(balloon);

  const BUB = 160;
  const bubbles = new THREE.InstancedMesh(new THREE.SphereGeometry(0.018, 8, 6), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.05, transparent: true, opacity: 0.7, clearcoat: 0.5 }), BUB);
  bubbles.renderOrder = 4; bubbles.count = 0; world.add(bubbles);
  const bub = [];
  const FOAM = 260;
  const foam = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 10, 8), new THREE.MeshStandardMaterial({ color: 0xfbfbf6, roughness: 0.35, transparent: true, opacity: 0.88 }), FOAM);
  foam.count = 0; foam.renderOrder = 4; world.add(foam);
  const foamSeed = Array.from({ length: FOAM }, () => [Math.random(), Math.random(), Math.random(), 0.6 + Math.random() * 0.8]);
  const pile = new THREE.Mesh(new THREE.SphereGeometry(0.2, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2), powder.material); pile.visible = false; world.add(pile);
  let foamH = 0;

  const panel = createPanel(stage, { title: 'Fizzy reactions' });
  panel.buttonRow([{ label: 'Pour 25 mL vinegar', icon: 'water_drop', onClick: () => act('vinegar') }, { label: 'Add 1 g soda', icon: 'grain', onClick: () => act('soda') }]);
  panel.buttonRow([{ label: 'Pour 25 mL water', icon: 'water', variant: 'ghost', onClick: () => act('water') }]);
  const balT = panel.toggle({ label: 'Balloon on the flask', value: true, onChange: (b) => { balloonOn = b; if (!b) co2Balloon = 0; } });
  panel.button({ label: 'Empty and wash the flask', icon: 'delete', variant: 'ghost', onClick: () => { vinegar = water = acidMol = sodaSolid = sodaAdded = co2 = co2Balloon = rate = t = 0; trace.length = 0; bub.length = 0; } });
  const graph = canvasCard(panel.body, 1.6);
  const st = panel.stats([{ key: 'vin', label: 'Vinegar (acid)' }, { key: 'soda', label: 'Baking soda added' }, { key: 'co2', label: 'CO₂ made' }, { key: 'left', label: 'Left over' }]);
  panel.info('Try 50 mL of vinegar: it can react with about 3.5 g of baking soda. Add less and the soda runs out first; add more and the extra powder just sits there because the acid has run out.');

  const actions = [];
  function act(kind) { actions.push({ kind, t: 0 }); }
  L.tappable(vin, () => act('vinegar'));
  L.tappable(wat, () => act('water'));
  L.tappable(jar, () => act('soda'));
  L.tappable(spoon, () => act('soda'));
  L.tappable(balloon, () => { balloonOn = !balloonOn; balT.set(balloonOn); if (!balloonOn) co2Balloon = 0; });

  const stream = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.01, 1, 8), new THREE.MeshPhysicalMaterial({ color: 0xf3e3b0, transparent: true, opacity: 0.8 }));
  stream.visible = false; world.add(stream);
  const v3 = new THREE.Vector3(); const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const sc = new THREE.Vector3();

  function drawGraph() {
    const { g, w, h } = graph.ctx();
    const ix = 40; const iy = 22; const iw = w - 50; const ih = h - 44;
    const span = Math.max(30, t); const vMax = Math.max(200, Math.ceil(co2 / 200 + 0.5) * 200);
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('CO₂ made', 10, 14);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih);
    g.strokeStyle = '#34d399'; g.lineWidth = 2; g.beginPath(); trace.forEach(([tt, v], i) => { const X = ix + tt / span * iw; const Y = iy + ih - v / vMax * ih; if (i) g.lineTo(X, Y); else g.moveTo(X, Y); }); g.stroke();
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#8ea0c2'; g.textAlign = 'center'; g.fillText(`t / s (0–${fmt(span, 0)})`, ix + iw / 2, h - 6);
    g.textAlign = 'right'; g.fillText(`${vMax} mL`, ix - 4, iy + 8); g.fillText('0', ix - 4, iy + ih);
  }

  let tick = 0;
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    // the current action: a bottle tips and pours, or the spoon scoops and tips
    stream.visible = false;
    const a = actions[0];
    [vin, wat].forEach((b) => { b.position.lerp(b.userData.home, 0.15); b.rotation.z *= 0.85; });
    spoon.position.lerp(spoon.userData.home, 0.15); spoon.rotation.x *= 0.85; heap.visible = true;
    if (a) {
      a.t += dt;
      const k = Math.min(1, a.t / 0.6) * (a.t > 2.4 ? Math.max(0, 1 - (a.t - 2.4) / 0.5) : 1);
      const e = k * k * (3 - 2 * k);
      if (a.kind === 'vinegar' || a.kind === 'water') {
        const b = a.kind === 'vinegar' ? vin : wat;
        b.position.lerpVectors(b.userData.home, v3.set(-0.5, 1.95, 0), e); b.rotation.z = -e * 1.9;
        if (a.t > 0.6 && a.t < 2.4) {
          const add = Math.min(25 / 1.8 * dt, CAP - vinegar - water);
          if (add > 0) { if (a.kind === 'vinegar') { vinegar += add; acidMol += add * ACID; } else water += add; }
          stream.visible = true; stream.material.color.setHex(a.kind === 'vinegar' ? 0xf3e3b0 : 0x9fd3f7);
          const top = flask.surfaceY() * S; stream.position.set(-0.02, (1.75 + top) / 2, 0); stream.scale.set(1, 1.75 - top, 1);
        }
      } else {
        spoon.position.lerpVectors(spoon.userData.home, v3.set(0.02, 2.05, 0.12), e); spoon.rotation.x = a.t > 1.2 ? -e * 2.2 : 0;
        if (a.t > 1.2 && !a.done) { a.done = true; sodaAdded += 1; sodaSolid += 1 / SODA_M; }
        heap.visible = a.t < 1.25;
      }
      if (a.t > 2.9) actions.shift();
    }
    // the reaction
    rate = 0;
    if (sodaSolid > 0 && acidMol > 0 && vinegar > 0) {
      const conc = acidMol / ((vinegar + water) / 1000);
      rate = Math.min(sodaSolid, acidMol, 1.6 * Math.pow(sodaSolid, 0.75) * Math.min(1, conc / 0.05) * dt);
      sodaSolid -= rate; acidMol -= rate; co2 += rate * VM;
      if (balloonOn) co2Balloon += rate * VM;
      rate /= Math.max(dt, 1e-6);
    }
    if (sodaSolid > 0 || rate > 0 || co2 > 0) t += dt;
    if (t > 0 && (tick++ & 1) === 0) { trace.push([t, co2]); if (trace.length > 800) trace.shift(); }
    flask.setVolume(vinegar + water);
    flask.setColor(new THREE.Color(vinegar > water ? 0xf3e6bb : 0xcfe8fb), 0.55);
    const surf = flask.surfaceY() * S;
    // bubbles rise from the powder at the bottom, foam climbs while it fizzes
    const nNew = Math.min(6, rate * 4000 * dt * 30);
    for (let i = 0; i < nNew && bub.length < BUB; i++) { const r = Math.random() * 0.28 * S; const an = Math.random() * Math.PI * 2; bub.push({ x: Math.cos(an) * r, z: Math.sin(an) * r, y: 0.05, v: 0.4 + Math.random() * 0.5, s: 0.6 + Math.random() * 1.2 }); }
    let n = 0;
    for (let i = bub.length - 1; i >= 0; i--) {
      const b = bub[i]; b.y += b.v * dt; b.x += Math.sin(time * 9 + i) * 0.002;
      if (b.y > surf + foamH * 0.6) { bub.splice(i, 1); continue; }
      const rr = flask.radiusAt(b.y / S) * S * 0.92; const d = Math.hypot(b.x, b.z); if (d > rr) { b.x *= rr / d; b.z *= rr / d; }
      m4.compose(v3.set(b.x, b.y, b.z), q, sc.setScalar(b.s)); bubbles.setMatrixAt(n++, m4);
    }
    bubbles.count = n; bubbles.instanceMatrix.needsUpdate = true;
    foamH += (Math.min(0.55, rate * 9000 * 0.004) - foamH) * (1 - Math.exp(-dt * 3));
    const nf = foamH > 0.005 && vinegar + water > 1 ? Math.min(FOAM, Math.round(foamH / 0.55 * FOAM) + 20) : 0;
    for (let i = 0; i < nf; i++) {
      const [u, w2, h2, sz] = foamSeed[i];
      const y = surf + h2 * foamH; const rr = flask.radiusAt(y / S) * S * 0.9 * Math.sqrt(u); const an = w2 * Math.PI * 2 + time * 0.2;
      const bs = 0.022 * sz * (0.7 + 0.3 * Math.sin(time * 5 + i));
      m4.compose(v3.set(Math.cos(an) * rr, y, Math.sin(an) * rr), q, sc.setScalar(bs)); foam.setMatrixAt(i, m4);
    }
    foam.count = nf; foam.instanceMatrix.needsUpdate = true;
    pile.visible = sodaSolid > 1e-4;
    if (pile.visible) { const pr = Math.min(0.24, Math.cbrt(sodaSolid * SODA_M) * 0.09); pile.scale.set(pr / 0.2, pr / 0.2 * 0.5, pr / 0.2); pile.position.y = 0.03; }
    // the balloon swells to the gas it has caught: V = 4/3 π r³
    const r = balloonOn ? Math.cbrt(3 * Math.max(0, co2Balloon) / (4 * Math.PI)) / 10 : 0;
    balloon.visible = balloonOn;
    const big = Math.min(1, r / 0.15);
    bBody.visible = r > 0.05; bLimp.visible = !bBody.visible;
    bBody.scale.set(Math.max(0.2, r), Math.max(0.24, r * 1.18), Math.max(0.2, r)); bBody.position.y = 0.08 + bBody.scale.y;
    bLimp.position.set(0.1 * (1 - big), 0.22, 0); bLimp.rotation.z = -0.9 * (1 - big);
    controls.setTarget(v3.set(0, 0.8 + 1.0 + (balloonOn ? Math.min(0.6, r * 0.9) : 0), 0));
    if ((tick & 3) === 0) drawGraph();
    const leftAcid = acidMol / ACID; const leftSoda = sodaSolid * SODA_M;
    st.vin.set(`${fmt(vinegar, 0)} mL`); st.soda.set(`${fmt(sodaAdded, 2)} g`); st.co2.set(`${fmt(co2, 0)} mL`);
    st.left.set(leftSoda > 0.01 ? `${fmt(leftSoda, 2)} g soda (acid used up)` : leftAcid > 0.5 ? `${fmt(leftAcid, 0)} mL vinegar's worth of acid` : '—');
    badge.set(rate > 1e-6 ? `Fizzing: ${fmt(rate * VM, 1)} mL of CO₂ a second` : vinegar < 1 ? 'Tap the vinegar bottle to pour some in' : sodaAdded === 0 ? 'Tap the baking soda to spoon some in' : leftSoda > 0.01 ? 'The acid is used up: extra soda just sits there' : `Done: ${fmt(co2, 0)} mL of CO₂`);
  });
  engine.start();

  stage.__fizzy = { act, state: () => ({ vinegar, sodaAdded, co2, co2Balloon }) };
  return { dispose() { panel.dispose(); hud.dispose(); flask.dispose(); L.dispose(); } };
}
