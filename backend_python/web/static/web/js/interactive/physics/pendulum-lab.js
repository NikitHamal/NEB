/**
 * Pendulum lab — a simple pendulum solved exactly (θ'' = −(g/L) sin θ − bθ', RK4 at 480 Hz).
 * Drag the bob to set both the angle and the length; release and it swings. The period is timed
 * from the motion itself (interpolated zero crossings) and compared with the small-angle formula
 * 2π√(L/g) and the exact large-amplitude period (via the arithmetic–geometric mean).
 */
import { createKit, T, Spring, makeRK4, Ring, fmt, clamp, background, grid, text, pill, sphere, softShadow, knob, arrow, dashed, withAlpha, DOTS, NODASH } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const WORLDS = [
  { value: 'moon', label: 'Moon', g: 1.62, color: '#9ca3af' },
  { value: 'mars', label: 'Mars', g: 3.71, color: '#d9653b' },
  { value: 'earth', label: 'Earth', g: 9.81, color: '#2563eb' },
  { value: 'jupiter', label: 'Jupiter', g: 24.79, color: '#c58b4c' },
];
const DEG = Math.PI / 180;
const H = 1 / 480;

function agm(a, b) { for (let i = 0; i < 12; i++) { const an = (a + b) / 2; b = Math.sqrt(a * b); a = an; } return a; }

export default function init(stage) {
  const k = createKit(stage, { label: 'A pendulum hanging from a support; drag the bob to pull it aside' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the bob, then let go', T.blue);

  let L = 1.0, g = 9.81, mass = 0.2, damping = false, paused = false;
  const y = new Float64Array(2);
  y[0] = 20 * DEG;
  let amp0 = y[0];
  let simT = 0, acc = 0;
  let lastCross = -1, measuredT = 0, crossings = 0;
  const trace = new Ring(900);
  const trail = new Ring(48);
  const hot = new Spring(0, 260, 26);
  const lenShow = new Spring(L, 120, 20);
  let dragging = false;
  const rk = makeRK4(2, (t, s, out) => {
    out[0] = s[1];
    out[1] = -(g / L) * Math.sin(s[0]) - (damping ? 0.18 : 0.0) * s[1];
  });

  const E = { ke: 0, pe: 0, tot: 1 };
  const plot = new Plot({ title: 'Angle θ against time', xLabel: 't / s', yLabel: 'θ / °', yMin: -90, yMax: 90 });

  function restart(fromAngle) {
    y[0] = fromAngle; y[1] = 0; amp0 = Math.abs(fromAngle);
    simT = 0; acc = 0; lastCross = -1; measuredT = 0; crossings = 0;
    trace.clear(); trail.clear();
  }

  const panel = createPanel(stage, { title: 'Pendulum' });
  const lenS = panel.slider({ label: 'Length L', min: 0.2, max: 2, step: 0.05, value: L, format: (v) => `${v.toFixed(2)} m`, onChange: (v) => { L = v; restart(y[0]); k.invalidate(); } });
  const worldC = panel.chips({ label: 'Where is the lab?', options: WORLDS.map((w) => ({ value: w.value, label: w.label, color: w.color })), value: 'earth', onChange: (v) => { g = WORLDS.find((w) => w.value === v).g; restart(y[0]); k.invalidate(); } });
  panel.slider({ label: 'Bob mass', min: 0.05, max: 1, step: 0.05, value: mass, format: (v) => `${(v * 1000).toFixed(0)} g`, onChange: (v) => { mass = v; k.invalidate(); } });
  panel.toggle({ label: 'Air damping', value: false, onChange: (v) => { damping = v; } });
  const [playB] = panel.buttonRow([
    { label: 'Pause', icon: 'pause', onClick: () => { paused = !paused; playB.setLabel(paused ? 'Play' : 'Pause'); playB.el.querySelector('.material-symbols-outlined').textContent = paused ? 'play_arrow' : 'pause'; } },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: () => { restart(20 * DEG); } },
  ]);
  const st = panel.stats([
    { key: 'meas', label: 'Measured T' }, { key: 'small', label: '2π√(L/g)' },
    { key: 'exact', label: 'Exact T' }, { key: 'swings', label: 'Swings', value: '0' },
  ]);
  panel.info('Drag the bob sideways to set the angle and up or down to change the length. Try 10° and 60°: only the big swing is slower than 2π√(L/g).');

  let pivotX = 0, pivotY = 0, scale = 100, sceneH = 0, bobX = 0, bobY = 0;
  k.onResize((w, h) => {
    const graphH = k.small ? Math.max(130, h * 0.3) : Math.max(150, h * 0.3);
    sceneH = h - graphH - 18;
    pivotX = k.small ? w * 0.5 : w * 0.42;
    pivotY = 40;
    scale = Math.min((sceneH - pivotY - 34) / 2.08, (Math.min(pivotX, w - pivotX) - 24) / (2 * Math.sin(1.05)));
    plot.box(14, h - graphH - 8, w - 28, graphH);
  });
  function bobR() { return 9 + Math.cbrt(mass) * 14; }

  const bobHandle = k.drag({
    hit: (x, yy, s) => { const d = Math.hypot(x - bobX, yy - bobY); return d < bobR() + s ? d : false; },
    down: () => { dragging = true; },
    move: (x, yy) => {
      const dx = x - pivotX, dy = Math.max(1, yy - pivotY);
      const th = clamp(Math.atan2(dx, dy), -80 * DEG, 80 * DEG);
      L = clamp(Math.round(Math.hypot(dx, dy) / scale / 0.05) * 0.05, 0.2, 2);
      lenS.set(L);
      restart(th);
    },
    up: () => { dragging = false; restart(y[0]); },
  });

  k.debug = { bob: () => [bobX, bobY], pivot: () => [pivotX, pivotY], theta: () => y[0] / DEG, L: () => L };

  function step(dt) {
    if (paused || dragging) return;
    acc += dt;
    while (acc >= H) {
      const prev = y[0];
      rk(y, simT, H);
      simT += H; acc -= H;
      if (prev < 0 && y[0] >= 0) {
        const tc = simT - H * (y[0] / (y[0] - prev));
        if (lastCross >= 0) { measuredT = tc - lastCross; crossings++; }
        lastCross = tc;
      }
    }
    trace.push(simT, y[0] / DEG);
  }

  k.frame((ctx, dt, w, h) => {
    step(dt);
    hot.to(k.isHot(bobHandle) || dragging ? 1 : 0); hot.step(dt);
    lenShow.to(L); lenShow.step(dt);
    background(k, ctx, w, h);
    grid(ctx, 0, 0, w, sceneH, 28, T.grid, pivotX, pivotY);

    const r = L * scale;
    bobX = pivotX + Math.sin(y[0]) * r;
    bobY = pivotY + Math.cos(y[0]) * r;
    trail.push(bobX, bobY);

    // support: a clamp on a beam
    ctx.fillStyle = '#e4e9f1'; ctx.fillRect(0, 0, w, pivotY - 18);
    ctx.strokeStyle = '#b8c3d3'; ctx.lineWidth = 1; ctx.beginPath();
    for (let x = -10; x < w; x += 12) { ctx.moveTo(x, pivotY - 18); ctx.lineTo(x + 12, 0); }
    ctx.stroke();
    ctx.fillStyle = T.steel; ctx.fillRect(0, pivotY - 20, w, 4);
    ctx.fillStyle = '#7b889c'; ctx.beginPath(); ctx.roundRect(pivotX - 12, pivotY - 14, 24, 14, 3); ctx.fill();

    // protractor at the pivot
    const pr = Math.min(r * 0.55, 120, sceneH * 0.3);
    if (pr > 40) {
      ctx.beginPath(); ctx.arc(pivotX, pivotY, pr, 10 * DEG, 170 * DEG);
      ctx.fillStyle = 'rgba(37,99,235,0.05)'; ctx.fill();
      ctx.strokeStyle = 'rgba(37,99,235,0.25)'; ctx.lineWidth = 1; ctx.stroke();
      ctx.beginPath();
      for (let a = -80; a <= 80; a += 5) {
        const t = (90 - a) * DEG, l = a % 30 === 0 ? 10 : a % 10 === 0 ? 6 : 3;
        ctx.moveTo(pivotX + Math.cos(t) * pr, pivotY + Math.sin(t) * pr);
        ctx.lineTo(pivotX + Math.cos(t) * (pr - l), pivotY + Math.sin(t) * (pr - l));
      }
      ctx.stroke();
      if (pr > 70) for (let a = -60; a <= 60; a += 30) {
        const t = (90 - a) * DEG;
        text(ctx, Math.abs(a) + '°', pivotX + Math.cos(t) * (pr - 20), pivotY + Math.sin(t) * (pr - 20), T.mute, 9.5, 600, 'center', 'middle');
      }
      // angle wedge
      ctx.beginPath(); ctx.moveTo(pivotX, pivotY);
      ctx.arc(pivotX, pivotY, pr * 0.5, Math.PI / 2, Math.PI / 2 - y[0], y[0] > 0);
      ctx.closePath(); ctx.fillStyle = withAlpha(T.orange, 0.18); ctx.fill();
    }
    dashed(ctx, pivotX, pivotY, pivotX, pivotY + r + 30, 'rgba(23,32,51,0.25)', 1, DOTS);
    // amplitude ghosts
    if (amp0 > 2 * DEG && !dragging) {
      ctx.globalAlpha = 0.18;
      for (let s = -1; s <= 1; s += 2) {
        const gx = pivotX + Math.sin(s * amp0) * r, gy = pivotY + Math.cos(s * amp0) * r;
        ctx.setLineDash(DOTS); ctx.strokeStyle = T.ink2; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(pivotX, pivotY); ctx.lineTo(gx, gy); ctx.stroke(); ctx.setLineDash(NODASH);
        ctx.beginPath(); ctx.arc(gx, gy, bobR(), 0, Math.PI * 2); ctx.stroke();
      }
      ctx.globalAlpha = 1;
    }
    // motion trail
    for (let i = 1; i < trail.n; i++) {
      const a = trail.idx(i - 1), b = trail.idx(i);
      ctx.strokeStyle = withAlpha(T.orange, 0.35 * i / trail.n); ctx.lineWidth = 3 * i / trail.n;
      ctx.beginPath(); ctx.moveTo(trail.x[a], trail.y[a]); ctx.lineTo(trail.x[b], trail.y[b]); ctx.stroke();
    }
    softShadow(ctx, bobX, sceneH - 6, bobR() * 1.6, 5, 0.12 + 0.1 * (1 - Math.abs(bobX - pivotX) / (r + 1)));
    // string and bob
    ctx.strokeStyle = '#4b5563'; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(pivotX, pivotY); ctx.lineTo(bobX, bobY); ctx.stroke();
    ctx.beginPath(); ctx.arc(pivotX, pivotY, 3.5, 0, Math.PI * 2); ctx.fillStyle = T.ink; ctx.fill();
    const br = bobR() * (1 + hot.x * 0.08);
    if (hot.x > 0.02) { ctx.beginPath(); ctx.arc(bobX, bobY, br + 8 * hot.x, 0, Math.PI * 2); ctx.fillStyle = withAlpha(T.blue, 0.14 * hot.x); ctx.fill(); }
    sphere(ctx, bobX, bobY, br, '#f0a020');
    // velocity arrow
    if (!dragging && Math.abs(y[1]) > 0.05) {
      const v = y[1] * L;
      const len = clamp(v * 26, -90, 90);
      const tx = Math.cos(y[0]), ty = -Math.sin(y[0]);
      arrow(ctx, bobX, bobY, bobX + tx * len, bobY + ty * len, T.green, 2.2);
    }
    // labels
    const ang = y[0] / DEG;
    pill(ctx, `θ = ${fmt(ang, 1)}°`, pivotX + (y[0] >= 0 ? -1 : 1) * 58, pivotY + 14, { color: T.orange });
    pill(ctx, `L = ${fmt(lenShow.x, 2)} m`, (pivotX + bobX) / 2 + (y[0] >= 0 ? 44 : -44), (pivotY + bobY) / 2, { color: T.ink2, size: 10.5 });
    const world = WORLDS.find((wd) => wd.g === g);
    text(ctx, `g = ${fmt(g, 2)} m/s²${world ? ' · ' + world.label : ''}`, 14, sceneH - 10, T.ink2, 11, 600);

    // energy bars
    if (!k.small) {
      const e = energy(E);
      const bx = w - 150, by = 20, bw = 130;
      text(ctx, 'Energy', bx, by + 10, T.ink, 11.5, 700);
      bar(ctx, bx, by + 22, bw, 'Kinetic', e.ke / e.tot, T.green);
      bar(ctx, bx, by + 54, bw, 'Potential', e.pe / e.tot, T.blue);
      text(ctx, `${fmt(e.tot * 1000, 0)} mJ total`, bx, by + 96, T.mute, 10, 500);
    }

    // graph
    const span = 10;
    const t1 = Math.max(span, simT);
    const yr = Math.min(90, Math.max(20, Math.ceil(amp0 / DEG * 1.15 / 10) * 10));
    plot.range(t1 - span, t1, -yr, yr).frame(ctx);
    plot.clip(ctx);
    ctx.fillStyle = withAlpha(T.blue, 0.05);
    ctx.fillRect(plot.ix, plot.Y(15), plot.iw, plot.Y(-15) - plot.Y(15));
    plot.ring(ctx, trace, T.orange, 2.2);
    plot.unclip(ctx);
    if (trace.n) plot.dot(ctx, trace.lastX, trace.lastY, T.orange, 4);

    const T0 = 2 * Math.PI * Math.sqrt(L / g);
    const Tex = T0 / agm(1, Math.cos(amp0 / 2));
    st.meas.set(measuredT > 0 ? `${fmt(measuredT, 3)} s` : '—');
    st.small.set(`${fmt(T0, 3)} s`);
    st.exact.set(`${fmt(Tex, 3)} s`);
    st.swings.set(String(crossings));
    badge.set(dragging ? `Release to swing · ${fmt(Math.abs(ang), 0)}°` : paused ? 'Paused' : measuredT > 0 ? `T = ${fmt(measuredT, 2)} s (formula ${fmt(T0, 2)} s)` : 'Timing the first swing…');
    k.animate(!paused || hot.moving || lenShow.moving);
  });

  function energy(e) {
    const v = y[1] * L;
    e.ke = 0.5 * mass * v * v;
    e.pe = mass * g * L * (1 - Math.cos(y[0]));
    e.tot = Math.max(1e-9, mass * g * L * (1 - Math.cos(Math.max(amp0, Math.abs(y[0])))), e.ke + e.pe);
    return e;
  }
  function bar(ctx, x, yy, w, label, f, color) {
    text(ctx, label, x, yy + 9, T.ink2, 10, 600);
    ctx.fillStyle = T.line2; ctx.beginPath(); ctx.roundRect(x, yy + 14, w, 8, 4); ctx.fill();
    ctx.fillStyle = color; ctx.beginPath(); ctx.roundRect(x, yy + 14, Math.max(0, Math.min(1, f)) * w, 8, 4); ctx.fill();
  }

  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
