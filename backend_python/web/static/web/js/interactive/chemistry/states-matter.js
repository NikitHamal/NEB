/**
 * States of matter in 3D. A sealed glass box of particles sits on a hot plate on the lab bench: heat
 * it or cool it and watch the particles change state. The temperature follows a real heating model
 * (specific heats; latent heats of fusion and of vaporisation), so the heating curve has a flat step
 * at the melting point and a much longer one at the boiling point, where far more energy is needed to
 * pull particles fully apart. The lattice loosens from its surface, the liquid pools, the gas fills
 * the box at speeds that grow as √T.
 */
import { createThermal } from '../core/matter2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createChemLab, THREE } from './chem3d/stage.js';
import { createParticleBox, createHotPlate } from './chem3d/particles.js';

const SUBS = {
  water: { label: 'Water', mp: 0, bp: 100, cS: 2.1, cL: 4.18, cG: 2.0, Lf: 334, Lv: 2257, start: -20, lo: -30, hi: 140, colors: [0x9ccff6, 0x2f7de1, 0xbfe3ff] },
  ethanol: { label: 'Ethanol', mp: -114, bp: 78, cS: 1.1, cL: 2.44, cG: 1.42, Lf: 108, Lv: 841, start: -130, lo: -140, hi: 110, colors: [0xe4d2fb, 0x8b3fd9, 0xdcc0fb] },
  iron: { label: 'Iron', mp: 1538, bp: 2862, cS: 0.45, cL: 0.82, cG: 0.45, Lf: 247, Lv: 6090, start: 1300, lo: 1200, hi: 3200, colors: [0x9aa5b5, 0xff7a1a, 0xffe25a] },
  oxygen: { label: 'Oxygen', mp: -218, bp: -183, cS: 1.67, cL: 1.7, cG: 0.92, Lf: 13.9, Lv: 213, start: -225, lo: -230, hi: -150, colors: [0xa5f3fc, 0x0ea5c6, 0xd6fbff] },
};
const MASS = 10;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const L = createChemLab(stage, { title: 'States of matter', aim: 'Heat and cool a substance through its changes of state', target: [0, 1.0, 0], camera: [1.4, 2.0, 4.6], minDistance: 2, maxDistance: 9 });
  if (!L) return null;
  const { engine, world, controls, quality } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Turn the heater up', '#2563eb');

  let sub = SUBS.water; let th = createThermal(sub, MASS); let dial = 0; let Q = 0;
  const trace = [];
  const plate = createHotPlate(); world.add(plate.group);
  const parts = createParticleBox(quality.tier === 'low' ? 125 : 216, { size: 1.15, radius: 0.05 });
  parts.group.position.y = 0.37 + 0.575; world.add(parts.group);
  const probe = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.0, 10), new THREE.MeshStandardMaterial({ color: 0xc0c6cf, metalness: 0.9, roughness: 0.3 }));
  probe.position.set(0.42, 1.25, 0.42); probe.rotation.z = 0.15; world.add(probe);
  const readout = L.label(); readout.el.style.font = '700 13px ui-monospace,Menlo,monospace'; readout.el.style.color = '#fca5a5';
  const phaseLbl = L.label();

  const panel = createPanel(stage, { title: 'States of matter' });
  panel.chips({ label: 'Substance', options: Object.keys(SUBS).map((s) => ({ value: s, label: SUBS[s].label })), value: 'water', onChange: (v) => { sub = SUBS[v]; reset(); } });
  const pS = panel.slider({ label: 'Heater', min: -100, max: 100, step: 5, value: 0, format: (v) => (v > 0 ? `heating ${v} %` : v < 0 ? `cooling ${-v} %` : 'off'), onChange: (v) => { dial = v / 100; } });
  panel.button({ label: 'Start again', icon: 'replay', variant: 'ghost', onClick: reset });
  const graph = canvasCard(panel.body, 1.5);
  const st = panel.stats([{ key: 'T', label: 'Temperature' }, { key: 'phase', label: 'State' }, { key: 'mp', label: 'Melting point' }, { key: 'bp', label: 'Boiling point' }]);
  const lat = panel.readout({ label: 'Latent heats (per gram)', value: '' });
  panel.info('Temperature measures how fast the particles move. On the flat parts of the curve the heat breaks the bonds between particles instead, so the temperature stays the same until the change of state is complete.');

  function reset() {
    th = createThermal(sub, MASS); trace.length = 0; Q = 0; dial = 0; pS.set(0);
    parts.setColors(...sub.colors); parts.reset(th.fm, th.fb);
    lat.set(`melting ${sub.Lf} J, boiling ${sub.Lv} J`);
  }
  reset();

  function drawGraph() {
    const { g, w, h } = graph.ctx();
    const ix = 38; const iy = 22; const iw = w - 48; const ih = h - 44;
    const qMax = Math.max(Q * 1.15 + 0.2, MASS * (sub.Lf + sub.Lv) / 1000 * 0.5);
    const X = (q) => ix + q / qMax * iw; const Y = (T) => iy + ih - (T - sub.lo) / (sub.hi - sub.lo) * ih;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('Heating curve', 10, 14);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih);
    g.font = '600 9px Poppins, system-ui, sans-serif';
    for (const [m, c, t] of [[sub.mp, '#c084fc', 'melts'], [sub.bp, '#f87171', 'boils']]) {
      g.setLineDash([4, 4]); g.strokeStyle = c; g.globalAlpha = 0.6; g.beginPath(); g.moveTo(ix, Y(m)); g.lineTo(ix + iw, Y(m)); g.stroke(); g.setLineDash([]); g.globalAlpha = 1;
      g.fillStyle = c; g.textAlign = 'right'; g.fillText(`${t} ${m} °C`, ix + iw - 3, Y(m) - 4);
    }
    g.strokeStyle = '#f87171'; g.lineWidth = 2; g.beginPath();
    trace.forEach(([q, T], i) => { if (i) g.lineTo(X(q), Y(T)); else g.moveTo(X(q), Y(T)); });
    g.stroke();
    g.fillStyle = '#8ea0c2'; g.textAlign = 'center'; g.fillText('heat added / kJ', ix + iw / 2, h - 6);
    g.textAlign = 'right'; g.fillText(`${sub.hi}`, ix - 4, iy + 8); g.fillText(`${sub.lo} °C`, ix - 4, iy + ih);
  }

  const v3 = new THREE.Vector3(); let tick = 0;
  engine.setUpdate((dt) => {
    controls.update(dt);
    const P = dial * MASS * sub.Lf / 7;
    th.add(P * dt); Q += P * dt / 1000;
    if (dial !== 0 && (tick++ & 1) === 0) { trace.push([Q, th.T]); if (trace.length > 1500) trace.shift(); }
    const heat = Math.min(1.3, Math.max(0, (th.T - sub.lo) / (sub.hi - sub.lo)));
    parts.step(dt, th.fm, th.fb, heat);
    plate.set(dial);
    if ((tick & 3) === 0) drawGraph();
    readout.el.textContent = `${fmt(th.T, 1)} °C`; readout.at(v3.set(0.5, 0.8 + 1.78, 0.42));
    phaseLbl.el.textContent = th.phase(); phaseLbl.at(v3.set(-0.2, 0.8 + 0.37 + 1.15, 0.6), 0);
    st.T.set(`${fmt(th.T, 1)} °C`); st.phase.set(th.phase().split(' (')[0]); st.mp.set(`${sub.mp} °C`); st.bp.set(`${sub.bp} °C`);
    const plateau = (th.fm > 0 && th.fm < 1) || (th.fb > 0 && th.fb < 1);
    badge.set(plateau ? `${th.phase()}: the temperature is stuck at ${fmt(th.T, 0)} °C until it is done` : dial === 0 ? 'Turn the heater up (or down to cool)' : `${th.phase()} at ${fmt(th.T, 0)} °C`);
  });
  engine.start();

  stage.__states = { heat: (v) => { dial = v; pS.set(Math.round(v * 100)); }, add: (q) => { th.add(q); }, state: () => ({ T: th.T, fm: th.fm, fb: th.fb }) };
  return { dispose() { panel.dispose(); hud.dispose(); readout.remove(); phaseLbl.remove(); parts.dispose(); L.dispose(); } };
}
