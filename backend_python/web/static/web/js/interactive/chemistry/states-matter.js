/**
 * States of matter — heat or cool a sealed box of particles and watch them change state. The
 * temperature follows a real heating model (specific heats; latent heats of fusion and of
 * vaporisation), so the heating curve has a flat step at the melting point and a much longer one
 * at the boiling point, where far more energy is needed to pull particles fully apart. Particle
 * speed grows with temperature: lattice → flowing liquid → fast gas filling the box.
 */
import { createKit, T, Spring, Ring, fmt, clamp, background, text, pill, withAlpha, card } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createThermal, createParticles, thermometer, drawHeatDial, dialValue } from '../core/matter2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SUBS = {
  water: { label: 'Water', mp: 0, bp: 100, cS: 2.1, cL: 4.18, cG: 2.0, Lf: 334, Lv: 2257, start: -20, lo: -30, hi: 140, colors: ['#93c5fd', '#2563eb', '#7dd3fc'] },
  ethanol: { label: 'Ethanol', mp: -114, bp: 78, cS: 1.1, cL: 2.44, cG: 1.42, Lf: 108, Lv: 841, start: -130, lo: -140, hi: 110, colors: ['#e9d5ff', '#9333ea', '#d8b4fe'] },
  iron: { label: 'Iron', mp: 1538, bp: 2862, cS: 0.45, cL: 0.82, cG: 0.45, Lf: 247, Lv: 6090, start: 1300, lo: 1200, hi: 3200, colors: ['#94a3b8', '#f97316', '#fde047'] },
  oxygen: { label: 'Oxygen', mp: -218, bp: -183, cS: 1.67, cL: 1.7, cG: 0.92, Lf: 13.9, Lv: 213, start: -225, lo: -230, hi: -150, colors: ['#a5f3fc', '#06b6d4', '#cffafe'] },
};
const MASS = 10;

export default function init(stage) {
  const k = createKit(stage, { label: 'A sealed box of particles with a heat dial, thermometer and heating curve' });
  const hud = createHud(stage);
  const badge = hud.badge('Turn the dial towards heat', T.blue);

  let sub = SUBS.water, th = createThermal(sub, MASS), dial = 0, simT = 0;
  const parts = createParticles(k.small ? 56 : 80);
  const trace = new Ring(1200);
  const plot = new Plot({ title: 'Heating curve', xLabel: 'heat added / kJ', yLabel: 'T / °C' });
  let Q = 0;
  const hotDial = new Spring(0, 260, 26);

  const panel = createPanel(stage, { title: 'States of matter' });
  panel.chips({ label: 'Substance', options: Object.keys(SUBS).map((s) => ({ value: s, label: SUBS[s].label, color: SUBS[s].colors[1] })), value: 'water', onChange: (v) => { sub = SUBS[v]; reset(); } });
  const pS = panel.slider({ label: 'Heater', min: -100, max: 100, step: 5, value: 0, format: (v) => (v > 0 ? `heating ${v} %` : v < 0 ? `cooling ${-v} %` : 'off'), onChange: (v) => { dial = v / 100; } });
  panel.button({ label: 'Start again', icon: 'replay', variant: 'ghost', onClick: reset });
  const st = panel.stats([{ key: 'T', label: 'Temperature' }, { key: 'phase', label: 'State' }, { key: 'mp', label: 'Melting point' }, { key: 'bp', label: 'Boiling point' }]);
  const lat = panel.readout({ label: 'Latent heats (per gram)', value: '' });
  panel.info('Temperature measures how fast the particles move. On the flat parts of the curve the heat breaks the bonds between particles instead, so the temperature stays the same until the change of state is complete.');

  function reset() { th = createThermal(sub, MASS); parts.reset(th.fm, th.fb); trace.clear(); simT = 0; Q = 0; dial = 0; pS.set(0); lat.set(`melting ${sub.Lf} J, boiling ${sub.Lv} J`); k.animate(true); }

  let bx = 0, by = 0, bw = 0, bh = 0, dx = 0, dy = 0, dr = 40, tx = 0, ty = 0, tH = 0;
  k.onResize((w, h) => {
    if (k.small) { bx = 12; by = 46; bw = w * 0.62; bh = h * 0.42; tx = w * 0.78; ty = by + bh - 8; tH = bh - 90; dx = w * 0.84; dy = by + 26; dr = 26; plot.box(10, by + bh + 14, w - 20, h - by - bh - 20); }
    else { bx = 30; by = 50; bw = Math.min(w * 0.38, h * 0.82); bh = h - 100; tx = bx + bw + 40; ty = by + bh - 14; tH = bh * 0.62; dx = bx + bw + 58; dy = by + 50; dr = 40; plot.box(tx + 90, 50, w - tx - 106, h - 100); }
    parts.layout(bx + 6, by + 6, bw - 12, bh - 12, Math.min(bw, bh) / 14);
    parts.reset(th.fm, th.fb);
  });
  const dialH = k.drag({ hit: (x, y, s) => { const d = Math.hypot(x - dx, y - dy); return d < dr + s ? d : false; }, move: (x, y) => { dial = Math.round(dialValue(x, y, dx, dy) * 20) / 20; pS.set(Math.round(dial * 100)); }, cursor: 'grab' });

  k.frame((ctx, dt, w, h) => {
    const P = dial * MASS * sub.Lf / 7;
    th.add(P * dt); Q += P * dt / 1000;
    simT += dt;
    if (dial !== 0) trace.push(Q, th.T);
    parts.sync(th.fm, th.fb, clamp((th.T - sub.lo) / (sub.hi - sub.lo), 0, 1));
    parts.step(dt, 0.08 + 0.9 * clamp((th.T - sub.lo) / (sub.hi - sub.lo), 0, 1.3));
    hotDial.to(k.isHot(dialH) ? 1 : 0); hotDial.step(dt);

    background(k, ctx, w, h);
    card(ctx, bx, by, bw, bh, 14, '#fbfdff');
    parts.draw(ctx, sub.colors);
    ctx.strokeStyle = '#334155'; ctx.lineWidth = 3; ctx.beginPath(); ctx.roundRect(bx, by, bw, bh, 14); ctx.stroke();
    pill(ctx, th.phase(), bx + bw / 2, by + 16, { color: T.ink, size: 11 });
    thermometer(ctx, tx, ty, tH, th.T, sub.lo, sub.hi, { marks: [{ T: sub.mp, label: 'mp', color: T.purple }, { T: sub.bp, label: 'bp', color: T.red }] });
    if (!k.small) pill(ctx, `${fmt(th.T, 1)} °C`, tx, ty - tH - 26, { color: T.red, size: 12 });
    drawHeatDial(ctx, dx, dy, dr, dial, hotDial.x > 0.5);
    const qMax = Math.max(1, Math.ceil(Q * 1.15 + 0.2));
    plot.range(0, Math.max(qMax, (MASS * (sub.Lf + sub.Lv) / 1000) * 0.5), sub.lo, sub.hi).frame(ctx);
    plot.clip(ctx);
    for (const m of [sub.mp, sub.bp]) { ctx.strokeStyle = withAlpha(m === sub.mp ? T.purple : T.red, 0.5); ctx.setLineDash([5, 4]); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(plot.ix, plot.Y(m)); ctx.lineTo(plot.ix + plot.iw, plot.Y(m)); ctx.stroke(); }
    ctx.setLineDash([]);
    plot.ring(ctx, trace, T.red, 2.2);
    plot.unclip(ctx);
    text(ctx, `melts ${sub.mp} °C`, plot.ix + plot.iw - 4, plot.Y(sub.mp) - 6, T.purple, 10, 700, 'right');
    text(ctx, `boils ${sub.bp} °C`, plot.ix + plot.iw - 4, plot.Y(sub.bp) - 6, T.red, 10, 700, 'right');
    st.T.set(`${fmt(th.T, 1)} °C`); st.phase.set(th.phase().split(' (')[0]); st.mp.set(`${sub.mp} °C`); st.bp.set(`${sub.bp} °C`);
    const plateau = (th.fm > 0 && th.fm < 1) || (th.fb > 0 && th.fb < 1);
    badge.set(plateau ? `${th.phase()}: the temperature is stuck at ${fmt(th.T, 0)} °C until it is done` : dial === 0 ? 'Turn the dial towards heat (or cool)' : `${th.phase()} at ${fmt(th.T, 0)} °C`);
    k.animate(true);
  });
  lat.set(`melting ${sub.Lf} J, boiling ${sub.Lv} J`);

  k.debug = { dial: () => [dx, dy], heat: (v) => { dial = v; }, state: () => ({ T: th.T, fm: th.fm, fb: th.fb }) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
