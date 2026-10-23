/**
 * Hot and cold, in 3D: melt and freeze ice, chocolate, butter and candle wax in a glass dish on a hot
 * plate. The energy goes into a real heating model (specific heats and latent heats per gram), so the
 * thermometer pauses at each substance's melting point while the solid melts, and pauses at the same
 * temperature on the way back while it freezes. The block softens and shrinks into a growing puddle;
 * beside it, a magnified box shows the particles: a lattice that loosens from its surface into a liquid.
 */
import { createThermal } from '../core/matter2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createChemLab, THREE } from './chem3d/stage.js';
import { createParticleBox, createHotPlate } from './chem3d/particles.js';

const SUBS = {
  ice: { label: 'Ice', mp: 0, cS: 2.1, cL: 4.18, Lf: 334, start: -15, lo: -20, hi: 40, colors: [0xa9d4f8, 0x3b82f6, 0xbfdbfe], block: 0xdbeafe, melt: 0x8cc8f0, glassy: true },
  chocolate: { label: 'Chocolate', mp: 34, cS: 1.6, cL: 1.7, Lf: 45, start: 20, lo: 0, hi: 60, colors: [0x7c4a1e, 0xa0522d, 0xd6b38a], block: 0x4a2611, melt: 0x5e2f12 },
  butter: { label: 'Butter', mp: 35, cS: 2.1, cL: 2.2, Lf: 65, start: 5, lo: -5, hi: 60, colors: [0xfacc15, 0xeab308, 0xfef9c3], block: 0xf7dc7c, melt: 0xf2c544 },
  wax: { label: 'Candle wax', mp: 58, cS: 2.14, cL: 2.9, Lf: 200, start: 25, lo: 20, hi: 90, colors: [0xe2e8f0, 0xf9a8d4, 0xfdf2f8], block: 0xf3eef0, melt: 0xf4c6da },
};
const MASS = 20; const PMAX = 60; const LAPSE = 12;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Hot and cold', aim: 'Melting and freezing points', target: [0.5, 0.8, 0], camera: [1.6, 2.4, 4.8], minDistance: 2, maxDistance: 9 });
  if (!L) return null;
  const { engine, world, controls, quality } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Turn the heater up', '#2563eb');

  let sub = SUBS.ice; let th = createThermal(sub, MASS); let dial = 0; let room = false; let simT = 0;
  const trace = [];
  const plate = createHotPlate(); plate.group.position.x = -0.35; world.add(plate.group);
  const glassMat = new THREE.MeshPhysicalMaterial({ color: 0xeaf6ff, roughness: 0.05, transparent: true, opacity: 0.25, clearcoat: 1, depthWrite: false });
  const dish = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [0.5, 0], [0.52, 0.02], [0.52, 0.16], [0.5, 0.16], [0.49, 0.02]].map(([x, y]) => new THREE.Vector2(x, y)), 48), glassMat);
  dish.position.set(-0.35, 0.37, 0); dish.renderOrder = 6; world.add(dish);
  const blockMat = new THREE.MeshPhysicalMaterial({ color: sub.block, roughness: 0.3, clearcoat: 0.5, transparent: true, opacity: 0.9 });
  const block = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.34, 0.42, 6, 6, 6), blockMat); block.castShadow = true;
  const bp = block.geometry.attributes.position;
  for (let i = 0; i < bp.count; i++) { const x = bp.getX(i); const y = bp.getY(i); const z = bp.getZ(i); const k = 1 - 0.18 * Math.pow(Math.max(Math.abs(x) / 0.21, Math.abs(z) / 0.21, Math.abs(y) / 0.17), 6); bp.setXYZ(i, x * k, y * k, z * k); }
  block.geometry.computeVertexNormals();
  world.add(block);
  const puddleMat = new THREE.MeshPhysicalMaterial({ color: sub.melt, roughness: 0.05, clearcoat: 0.5, transparent: true, opacity: 0.85 });
  const puddle = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.48, 1, 48), puddleMat);
  puddle.position.set(-0.35, 0.39, 0); world.add(puddle);
  const parts = createParticleBox(quality.tier === 'low' ? 64 : 125, { size: 0.8, radius: 0.045 });
  parts.group.position.set(1.15, 0.4, 0); world.add(parts.group);
  const probe = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.8, 10), new THREE.MeshStandardMaterial({ color: 0xc0c6cf, metalness: 0.9, roughness: 0.3 }));
  probe.position.set(-0.15, 0.75, 0.15); probe.rotation.z = 0.35; world.add(probe);
  const readout = L.label(); readout.el.style.font = '700 13px ui-monospace,Menlo,monospace'; readout.el.style.color = '#fca5a5';
  const zoomLbl = L.label(); zoomLbl.el.textContent = 'particles, magnified';

  const panel = createPanel(stage, { title: 'Hot and cold' });
  panel.chips({ label: 'Substance', options: Object.keys(SUBS).map((s) => ({ value: s, label: `${SUBS[s].label} · ${SUBS[s].mp} °C` })), value: 'ice', onChange: (v) => { sub = SUBS[v]; reset(); } });
  const pS = panel.slider({ label: 'Heater', min: -100, max: 100, step: 5, value: 0, format: (v) => (v > 0 ? `heating ${v} %` : v < 0 ? `cooling ${-v} %` : 'off'), onChange: (v) => { dial = v / 100; } });
  panel.toggle({ label: 'Leave it out in the room (25 °C)', value: false, onChange: (v) => { room = v; } });
  panel.button({ label: 'Start again', icon: 'replay', variant: 'ghost', onClick: reset });
  const graph = canvasCard(panel.body, 1.5);
  const st = panel.stats([{ key: 'T', label: 'Thermometer' }, { key: 'state', label: 'State' }, { key: 'melted', label: 'Melted' }, { key: 'mp', label: 'Melting point' }]);
  panel.info('While it melts, all the heat goes into pulling particles out of the lattice, not into speeding them up, so the temperature stays put. Freezing gives that heat back at the very same temperature.');

  function reset() {
    th = createThermal(sub, MASS); trace.length = 0; simT = 0; dial = 0; pS.set(0);
    blockMat.color.setHex(sub.block); blockMat.opacity = sub.glassy ? 0.8 : 1; blockMat.transparent = !!sub.glassy; blockMat.roughness = sub.glassy ? 0.08 : 0.45;
    puddleMat.color.setHex(sub.melt); puddleMat.opacity = sub.glassy ? 0.78 : 0.95;
    parts.setColors(...sub.colors); parts.reset(th.fm, 0);
  }
  reset();

  function drawGraph() {
    const { g, w, h } = graph.ctx();
    const ix = 38; const iy = 22; const iw = w - 48; const ih = h - 44;
    const tMax = Math.max(5, simT / 60 * 1.15);
    const X = (t) => ix + t / tMax * iw; const Y = (T) => iy + ih - (T - sub.lo) / (sub.hi - sub.lo) * ih;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('Temperature against time', 10, 14);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih);
    g.setLineDash([4, 4]); g.strokeStyle = '#c084fc'; g.beginPath(); g.moveTo(ix, Y(sub.mp)); g.lineTo(ix + iw, Y(sub.mp)); g.stroke(); g.setLineDash([]);
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#c084fc'; g.textAlign = 'right'; g.fillText(`melting point ${sub.mp} °C`, ix + iw - 3, Y(sub.mp) - 4);
    g.strokeStyle = '#f87171'; g.lineWidth = 2; g.beginPath(); trace.forEach(([t, T], i) => { if (i) g.lineTo(X(t), Y(T)); else g.moveTo(X(t), Y(T)); }); g.stroke();
    g.fillStyle = '#8ea0c2'; g.textAlign = 'center'; g.fillText('t / min', ix + iw / 2, h - 6);
    g.textAlign = 'right'; g.fillText(`${sub.hi}`, ix - 4, iy + 8); g.fillText(`${sub.lo} °C`, ix - 4, iy + ih);
  }

  const v3 = new THREE.Vector3(); let tick = 0;
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    const P = dial * PMAX + (room ? 0.25 * (25 - th.T) : 0);
    th.add(P * dt * LAPSE); simT += dt * LAPSE;
    if ((dial !== 0 || room) && (tick++ & 1) === 0) { trace.push([simT / 60, th.T]); if (trace.length > 1500) trace.shift(); }
    const heat = Math.min(1.2, Math.max(0, (th.T - sub.lo) / (sub.hi - sub.lo)));
    parts.step(dt, th.fm, 0, 0.15 + heat * 0.6);
    plate.set(dial);
    const left = Math.max(1e-3, 1 - th.fm);
    const s = Math.cbrt(left);
    block.scale.set(s * (1 + th.fm * 0.15), s * (1 - th.fm * 0.25), s * (1 + th.fm * 0.15));
    block.position.set(-0.35, 0.39 + 0.17 * block.scale.y + puddle.scale.y * 0.5, 0);
    block.visible = left > 0.01;
    const pv = th.fm;
    puddle.visible = pv > 0.01;
    puddle.scale.set(0.35 + 0.65 * Math.sqrt(pv), Math.max(0.002, 0.04 * pv), 0.35 + 0.65 * Math.sqrt(pv));
    puddle.position.y = 0.39 + puddle.scale.y / 2;
    if ((tick & 3) === 0) drawGraph();
    readout.el.textContent = `${fmt(th.T, 1)} °C`; readout.at(v3.set(-0.32, 0.8 + 1.18, 0.15));
    zoomLbl.at(v3.set(1.15, 0.8 + 0.95, 0));
    st.T.set(`${fmt(th.T, 1)} °C`); st.state.set(th.phase().split(' (')[0]); st.melted.set(`${fmt(th.fm * 100, 0)} %`); st.mp.set(`${sub.mp} °C`);
    const melting = th.fm > 0 && th.fm < 1;
    badge.set(melting ? `${dial < 0 || (room && th.T > 25) ? 'Freezing' : 'Melting'}: the thermometer stays at ${fmt(th.T, 0)} °C until it is done` : dial === 0 && !room ? 'Turn the heater up (or down to cool)' : `${th.phase()} at ${fmt(th.T, 0)} °C`);
    void time;
  });
  engine.start();

  stage.__melt = { heat: (v) => { dial = v; pS.set(Math.round(v * 100)); }, add: (q) => { th.add(q); }, state: () => ({ T: th.T, fm: th.fm }) };
  return { dispose() { panel.dispose(); hud.dispose(); readout.remove(); zoomLbl.remove(); parts.dispose(); L.dispose(); } };
}
