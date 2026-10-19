/**
 * Hot and cold — melt and freeze ice, chocolate, butter and candle wax with a heat dial. The
 * energy goes into a real heating model (specific heats and latent heats per gram), so the
 * thermometer pauses at each substance's melting point while the solid melts, and pauses at the
 * same temperature on the way back while it freezes. A magnifier shows the particles: a jiggling
 * lattice that loosens from its surface into a flowing liquid.
 */
import { createKit, T, Spring, Ring, fmt, clamp, background, text, pill, withAlpha, card, softShadow } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createThermal, createParticles, thermometer, drawHeatDial, dialValue } from '../core/matter2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SUBS = {
  ice: { label: 'Ice', mp: 0, cS: 2.1, cL: 4.18, Lf: 334, start: -15, lo: -20, hi: 40, colors: ['#93c5fd', '#3b82f6', '#bfdbfe'], block: '#dbeafe', melt: '#7cc4f2' },
  chocolate: { label: 'Chocolate', mp: 34, cS: 1.6, cL: 1.7, Lf: 45, start: 20, lo: 0, hi: 60, colors: ['#7c4a1e', '#a0522d', '#d6b38a'], block: '#6b3a16', melt: '#8b4a1f' },
  butter: { label: 'Butter', mp: 35, cS: 2.1, cL: 2.2, Lf: 65, start: 5, lo: -5, hi: 60, colors: ['#facc15', '#eab308', '#fef9c3'], block: '#fde68a', melt: '#f5c542' },
  wax: { label: 'Candle wax', mp: 58, cS: 2.14, cL: 2.9, Lf: 200, start: 25, lo: 20, hi: 90, colors: ['#e2e8f0', '#f9a8d4', '#fdf2f8'], block: '#f1f5f9', melt: '#f9c4dc' },
};
const MASS = 20;
const PMAX = 60;
const LAPSE = 12;

export default function init(stage) {
  const k = createKit(stage, { label: 'A substance in a dish with a heat dial, a thermometer and its particles' });
  const hud = createHud(stage);
  const badge = hud.badge('Turn the dial to heat', T.blue);

  let key = 'ice', sub = SUBS.ice, th = createThermal(sub, MASS), dial = 0, room = false, simT = 0;
  const parts = createParticles(k.small ? 48 : 66);
  const trace = new Ring(900);
  const plot = new Plot({ title: 'Temperature against time', xLabel: 't / min', yLabel: 'T / °C' });
  const flame = new Spring(0, 80, 12), hotDial = new Spring(0, 260, 26);

  const panel = createPanel(stage, { title: 'Hot and cold' });
  panel.chips({ label: 'Substance', options: Object.keys(SUBS).map((s) => ({ value: s, label: `${SUBS[s].label} · ${SUBS[s].mp} °C`, color: SUBS[s].block })), value: 'ice', onChange: (v) => { key = v; sub = SUBS[v]; reset(); } });
  const pS = panel.slider({ label: 'Heater', min: -100, max: 100, step: 5, value: 0, format: (v) => (v > 0 ? `heating ${v} %` : v < 0 ? `cooling ${-v} %` : 'off'), onChange: (v) => { dial = v / 100; k.animate(true); } });
  panel.toggle({ label: 'Leave it out in the room (25 °C)', value: false, onChange: (v) => { room = v; k.animate(true); } });
  panel.button({ label: 'Start again', icon: 'replay', variant: 'ghost', onClick: reset });
  const st = panel.stats([{ key: 'T', label: 'Thermometer' }, { key: 'state', label: 'State' }, { key: 'melted', label: 'Melted' }, { key: 'mp', label: 'Melting point' }]);
  panel.info('While it melts, all the heat goes into pulling particles out of the lattice, not into speeding them up, so the temperature stays put. Freezing gives that heat back at the very same temperature.');

  function reset() { th = createThermal(sub, MASS); parts.reset(th.fm, 0); trace.clear(); simT = 0; dial = 0; pS.set(0); k.animate(true); }

  let dx = 0, dy = 0, dr = 40, zx = 0, zy = 0, zr = 80, dishX = 0, dishY = 0;
  k.onResize((w, h) => {
    if (k.small) {
      dishX = w * 0.26; dishY = h * 0.22; zx = w * 0.72; zy = h * 0.24; zr = Math.min(78, w * 0.22);
      dx = w * 0.2; dy = h * 0.46; dr = 30; plot.box(10, h * 0.6, w - 20, h * 0.38);
    } else {
      dishX = w * 0.17; dishY = h * 0.42; zx = w * 0.465; zy = h * 0.4; zr = Math.min(130, h * 0.24, w * 0.12);
      dx = w * 0.16; dy = h * 0.78; dr = 46; plot.box(w * 0.62, 50, w * 0.36, h - 80);
    }
    parts.layout(zx - zr * 0.78, zy - zr * 0.78, zr * 1.56, zr * 1.56, zr / 6.5);
    parts.reset(th.fm, 0);
  });
  const dialH = k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - dx, y - dy); return d < dr + s ? d : false; },
    move: (x, y) => { dial = Math.round(dialValue(x, y, dx, dy) * 20) / 20; pS.set(Math.round(dial * 100)); k.animate(true); },
    cursor: 'grab',
  });

  k.frame((ctx, dt, w, h) => {
    const P = dial * PMAX + (room ? 0.25 * (25 - th.T) : 0);
    th.add(P * dt * LAPSE);
    simT += dt * LAPSE;
    if (dial !== 0 || room) trace.push(simT / 60, th.T);
    parts.sync(th.fm, 0, 0);
    const kT = clamp((th.T - sub.lo) / (sub.hi - sub.lo), 0, 1.2);
    parts.step(dt, 0.15 + kT * 0.6);
    flame.to(Math.max(0, dial)); flame.step(dt); hotDial.to(k.isHot(dialH) ? 1 : 0); hotDial.step(dt);

    background(k, ctx, w, h);
    ctx.fillStyle = '#e6dccb'; ctx.fillRect(0, dishY + 40, k.small ? w * 0.5 : w * 0.34, 8);
    // heater below the dish
    const hx = dishX, hy = dishY + 40;
    ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.roundRect(hx - 50, hy - 4, 100, 10, 4); ctx.fill();
    if (flame.x > 0.02) for (let i = -3; i <= 3; i++) { const fh = (10 + 6 * Math.sin(k.t * 13 + i * 1.7)) * flame.x; ctx.fillStyle = withAlpha('#f97316', 0.75); ctx.beginPath(); ctx.ellipse(hx + i * 12, hy - 4 - fh / 2, 4, fh / 2, 0, 0, Math.PI * 2); ctx.fill(); }
    if (dial < -0.02) { ctx.fillStyle = withAlpha('#93c5fd', -dial * 0.5); ctx.beginPath(); ctx.roundRect(hx - 54, hy - 8, 108, 14, 6); ctx.fill(); }
    // dish with the block melting into a puddle
    softShadow(ctx, hx, hy - 8, 70, 6, 0.2);
    const bw = 64 * Math.cbrt(1 - th.fm + 1e-3), bh = 52 * Math.cbrt(1 - th.fm + 1e-3);
    const pw = 40 + 50 * Math.sqrt(th.fm), ph = 4 + 6 * Math.sqrt(th.fm);
    if (th.fm > 0.01) { ctx.fillStyle = withAlpha(sub.melt, 0.9); ctx.beginPath(); ctx.ellipse(hx, hy - 14, pw, ph, 0, 0, Math.PI * 2); ctx.fill(); }
    if (th.fm < 0.995) {
      ctx.fillStyle = sub.block; ctx.strokeStyle = withAlpha('#334155', 0.25); ctx.lineWidth = 1;
      ctx.beginPath(); ctx.roundRect(hx - bw / 2, hy - 14 - bh, bw, bh, 4 + 10 * th.fm); ctx.fill(); ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,0.4)'; ctx.fillRect(hx - bw / 2 + 4, hy - 10 - bh, bw * 0.25, 3);
      if (th.fm > 0.05) { ctx.fillStyle = withAlpha(sub.melt, 0.8); for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.ellipse(hx - bw / 3 + i * bw / 3, hy - 14 - bh * 0.3 * (i % 2 ? 1 : 0.6), 3, 6, 0, 0, Math.PI * 2); ctx.fill(); } }
    }
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(hx - 76, hy - 26); ctx.quadraticCurveTo(hx - 70, hy - 8, hx - 50, hy - 8); ctx.lineTo(hx + 50, hy - 8); ctx.quadraticCurveTo(hx + 70, hy - 8, hx + 76, hy - 26); ctx.stroke();
    // magnifier
    ctx.strokeStyle = withAlpha(T.blue, 0.35); ctx.setLineDash([4, 4]); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(hx + 20, hy - 40); ctx.lineTo(zx - zr * 0.7, zy + zr * 0.7); ctx.stroke(); ctx.setLineDash([]);
    ctx.save(); ctx.beginPath(); ctx.arc(zx, zy, zr, 0, Math.PI * 2); ctx.fillStyle = '#fbfdff'; ctx.fill(); ctx.clip();
    parts.draw(ctx, sub.colors);
    ctx.restore();
    ctx.beginPath(); ctx.arc(zx, zy, zr, 0, Math.PI * 2); ctx.strokeStyle = '#334155'; ctx.lineWidth = 5; ctx.stroke();
    text(ctx, 'particles, magnified', zx, zy + zr + 18, T.ink2, 10, 600, 'center');
    // thermometer
    const tx = k.small ? w * 0.47 : w * 0.5 + 10, ty = k.small ? h * 0.52 : h * 0.86;
    if (!k.small) thermometer(ctx, w * 0.29, h * 0.9, h * 0.34, th.T, sub.lo, sub.hi, { marks: [{ T: sub.mp, label: 'mp', color: T.purple }] });
    pill(ctx, `${fmt(th.T, 1)} °C`, k.small ? w * 0.5 : w * 0.29, k.small ? h * 0.47 : h * 0.9 - h * 0.34 - 26, { color: T.red, size: 12 });
    drawHeatDial(ctx, dx, dy, dr, dial, hotDial.x > 0.5);
    // graph
    const t1 = Math.max(4, simT / 60);
    plot.range(0, t1, sub.lo, sub.hi).frame(ctx);
    plot.clip(ctx);
    ctx.strokeStyle = withAlpha(T.purple, 0.5); ctx.setLineDash([5, 4]); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(plot.ix, plot.Y(sub.mp)); ctx.lineTo(plot.ix + plot.iw, plot.Y(sub.mp)); ctx.stroke(); ctx.setLineDash([]);
    plot.ring(ctx, trace, T.red, 2.2);
    plot.unclip(ctx);
    text(ctx, `melting point ${sub.mp} °C`, plot.ix + plot.iw - 4, plot.Y(sub.mp) - 6, T.purple, 10, 700, 'right');
    st.T.set(`${fmt(th.T, 1)} °C`); st.state.set(th.phase()); st.melted.set(`${fmt(th.fm * 100, 0)} %`); st.mp.set(`${sub.mp} °C`);
    const plateau = th.fm > 0 && th.fm < 1;
    badge.set(plateau ? (P > 0 ? `Melting at ${sub.mp} °C — the thermometer pauses` : P < 0 ? `Freezing at ${sub.mp} °C — the same temperature` : `Half melted, holding at ${sub.mp} °C`) : dial === 0 && !room ? 'Turn the dial to heat (or cool)' : `${sub.label}: ${th.phase().toLowerCase()} at ${fmt(th.T, 1)} °C`);
    k.animate(true);
  });

  k.debug = { dial: () => [dx, dy], heat: (v) => { dial = v; }, state: () => ({ T: th.T, fm: th.fm }) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
