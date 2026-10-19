/**
 * Weight on other worlds — five drop towers side by side, each on a different world. Drag any
 * ball to set the drop height (the same for all), then drop them together: each falls with its
 * world's g and lands at t = √(2h/g), timed in real seconds. Below, the same person stands on a
 * bathroom scale on each world: their mass never changes, their weight W = mg does, and the scale
 * (calibrated on Earth) reads W/9.81 "kg".
 */
import { createKit, T, Spring, fmt, clamp, text, withAlpha, sphere, softShadow, card } from '../core/kit2d.js';
import { starfield, npill } from '../core/space2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const ALL = {
  moon: { name: 'Moon', g: 1.62, ground: '#9aa1ad', sky: '#0b1020', atm: false },
  mercury: { name: 'Mercury', g: 3.7, ground: '#8d7f72', sky: '#0b0f18', atm: false },
  mars: { name: 'Mars', g: 3.71, ground: '#b5603a', sky: '#3a2116', atm: true },
  venus: { name: 'Venus', g: 8.87, ground: '#a68b4c', sky: '#5a4518', atm: true },
  earth: { name: 'Earth', g: 9.81, ground: '#5b8c4a', sky: '#2c6db5', atm: true },
  jupiter: { name: 'Jupiter', g: 24.79, ground: '#b08a5e', sky: '#5b4026', atm: true },
  saturn: { name: 'Saturn', g: 10.44, ground: '#c9ad7c', sky: '#5e4a2c', atm: true },
  uranus: { name: 'Uranus', g: 8.69, ground: '#8fc9cf', sky: '#24545a', atm: true },
  neptune: { name: 'Neptune', g: 11.15, ground: '#4f6fd0', sky: '#1d2d66', atm: true },
  pluto: { name: 'Pluto', g: 0.62, ground: '#c8b8a6', sky: '#06080f', atm: false },
  sun: { name: 'Sun', g: 274, ground: '#f59e0b', sky: '#7a2e06', atm: true },
};

export default function init(stage) {
  const k = createKit(stage, { night: true, label: 'Five drop towers on different worlds and a bathroom scale on each' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag a ball to set the height, then drop', '#60a5fa');

  const lanes = ['moon', 'mars', 'earth', 'jupiter', 'sun'];
  let H = 10, mass = 50;
  const y = new Float64Array(5), v = new Float64Array(5), t = new Float64Array(5), landed = new Uint8Array(5);
  let dropping = false;
  const scaleR = lanes.map(() => new Spring(0, 90, 10));

  const panel = createPanel(stage, { title: 'Weight on other worlds' });
  panel.chips({ label: 'Fifth tower', options: ['sun', 'mercury', 'venus', 'saturn', 'uranus', 'neptune', 'pluto'].map((key) => ({ value: key, label: ALL[key].name })), value: 'sun', onChange: (key) => { lanes[4] = key; reset(); } });
  panel.slider({ label: 'Your mass', min: 10, max: 120, step: 1, value: mass, format: (m) => `${m} kg`, onChange: (m) => { mass = m; k.animate(true); } });
  panel.buttonRow([{ label: 'Drop all', icon: 'south', onClick: drop }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset }]);
  const st = panel.stats(lanes.map((key, i) => ({ key: 'l' + i, label: i === 4 ? 'Fifth tower' : ALL[key].name })));
  panel.info('Mass is how much stuff you are made of: the same everywhere. Weight is the pull of gravity on that mass, W = mg, in newtons. A smaller g means a slower fall: t = √(2h/g).');

  function reset() { dropping = false; for (let i = 0; i < 5; i++) { y[i] = H; v[i] = 0; t[i] = 0; landed[i] = 0; } k.animate(true); }
  function drop() { reset(); dropping = true; }

  let lw = 0, top = 0, ground = 0, scaleY = 0, sc = 10;
  k.onResize((w, h) => { lw = w / 5; top = 56; scaleY = h - (k.small ? 46 : 62); ground = scaleY - (k.small ? 70 : 96); sc = (ground - top - 20) / 20; });
  const Y = (m) => ground - m * sc;

  k.drag({
    hit: (x, yy, s) => { const i = Math.floor(x / lw); if (i < 0 || i > 4) return false; const d = Math.hypot(x - (i + 0.5) * lw, yy - Y(y[i])); return d < 16 + s ? d : false; },
    move: (x, yy) => { H = clamp(Math.round((ground - yy) / sc), 1, 20); reset(); },
    up: () => drop(),
    cursor: 'ns-resize',
  });

  k.frame((ctx, dt, w, h) => {
    if (dropping) {
      for (let i = 0; i < 5; i++) {
        if (landed[i]) continue;
        const g = ALL[lanes[i]].g;
        t[i] += dt; v[i] = g * t[i]; y[i] = H - 0.5 * g * t[i] * t[i];
        if (y[i] <= 0) { t[i] = Math.sqrt(2 * H / g); y[i] = 0; landed[i] = 1; }
      }
      if (landed.every((l) => l)) dropping = false;
    }
    starfield(k, ctx, w, h, { seed: 3 });
    for (let i = 0; i < 5; i++) {
      const W0 = ALL[lanes[i]], x0 = i * lw, cx = x0 + lw / 2;
      ctx.fillStyle = withAlpha(W0.sky, W0.atm ? 0.6 : 0.3); ctx.fillRect(x0 + 1, top - 10, lw - 2, ground - top + 10);
      ctx.fillStyle = W0.ground; ctx.fillRect(x0 + 1, ground, lw - 2, scaleY - ground + 30);
      ctx.fillStyle = 'rgba(0,0,0,0.15)'; ctx.fillRect(x0 + 1, ground, lw - 2, 3);
      text(ctx, W0.name, cx, top + 6, '#e8eefb', k.small ? 10 : 12.5, 700, 'center');
      text(ctx, `g = ${W0.g} m/s²`, cx, top + (k.small ? 20 : 24), '#aab8d3', k.small ? 8.5 : 10, 600, 'center');
      // tower scale
      ctx.strokeStyle = 'rgba(255,255,255,0.25)'; ctx.lineWidth = 1; ctx.beginPath();
      for (let m = 0; m <= 20; m += 2) { ctx.moveTo(x0 + 6, Y(m)); ctx.lineTo(x0 + (m % 10 === 0 ? 16 : 11), Y(m)); }
      ctx.stroke();
      if (i === 0) for (let m = 0; m <= 20; m += 10) text(ctx, `${m} m`, x0 + 18, Y(m) + 3, '#aab8d3', 9, 600);
      ctx.setLineDash([3, 4]); ctx.strokeStyle = 'rgba(255,255,255,0.3)'; ctx.beginPath(); ctx.moveTo(x0 + 4, Y(H)); ctx.lineTo(x0 + lw - 4, Y(H)); ctx.stroke(); ctx.setLineDash([]);
      softShadow(ctx, cx, ground + 2, 10 * (1 - y[i] / 25), 3, 0.35);
      sphere(ctx, cx, Y(y[i]) - 8, 8, '#e5484d');
      if (dropping || landed[i]) npill(ctx, `${fmt(t[i], 2)} s`, cx, Math.min(Y(y[i]) - 30, ground - 34), landed[i] ? '#86efac' : '#e8eefb', k.small ? 9.5 : 11);
      // the bathroom scale
      const Wn = mass * W0.g, read = Wn / 9.81;
      scaleR[i].to(read); scaleR[i].step(dt);
      const sw = Math.min(lw - 14, 74), sy = scaleY;
      ctx.fillStyle = '#e2e8f0'; ctx.beginPath(); ctx.roundRect(cx - sw / 2, sy - 10, sw, 18, 5); ctx.fill();
      ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.roundRect(cx - sw * 0.32, sy - 6, sw * 0.64, 11, 3); ctx.fill();
      ctx.fillStyle = '#86efac'; ctx.font = `700 ${k.small ? 8 : 9.5}px ${T.mono}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(scaleR[i].x > 999 ? 'ERR' : `${fmt(scaleR[i].x, 0)} kg`, cx, sy);
      const fh = k.small ? 40 : 60, sq = clamp(W0.g / 9.81, 0.4, 2);
      ctx.fillStyle = '#e8eefb'; ctx.beginPath(); ctx.arc(cx, sy - 14 - fh, fh * 0.12, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = '#e8eefb'; ctx.lineWidth = k.small ? 2.5 : 3.5; ctx.beginPath();
      const knee = sq > 1.5 ? 0.12 : 0;
      ctx.moveTo(cx, sy - 12 - fh * 0.86); ctx.lineTo(cx, sy - 12 - fh * 0.4);
      ctx.moveTo(cx, sy - 12 - fh * 0.4); ctx.lineTo(cx - fh * (0.12 + knee), sy - 12 - fh * 0.2); ctx.lineTo(cx - fh * 0.1, sy - 12);
      ctx.moveTo(cx, sy - 12 - fh * 0.4); ctx.lineTo(cx + fh * (0.12 + knee), sy - 12 - fh * 0.2); ctx.lineTo(cx + fh * 0.1, sy - 12);
      ctx.moveTo(cx - fh * 0.2, sy - 12 - fh * (0.75 - 0.15 * (sq - 1) * 0.3)); ctx.lineTo(cx, sy - 12 - fh * 0.7); ctx.lineTo(cx + fh * 0.2, sy - 12 - fh * (0.75 - 0.15 * (sq - 1) * 0.3));
      ctx.stroke();
      text(ctx, `${fmt(Wn, 0)} N`, cx, sy + 22, '#e8eefb', k.small ? 9.5 : 11, 700, 'center');
      st['l' + i].set(`${fmt(Math.sqrt(2 * H / W0.g), 2)} s · ${fmt(Wn, 0)} N`);
      if (i) { ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fillRect(x0, top - 10, 1, h); }
    }
    badge.set(dropping ? 'Falling…' : landed[0] ? `Same ${H} m drop: ${fmt(t[4], 2)} s on ${ALL[lanes[4]].name}, ${fmt(t[0], 2)} s on the Moon` : `Drop height ${H} m — drag a ball to change it`);
    k.animate(dropping || scaleR.some((s) => s.moving));
  });

  reset();
  k.debug = { ball: (i) => [(i + 0.5) * lw, Y(y[i]) - 8], times: () => Array.from(t) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
