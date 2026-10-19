/**
 * Orbital sandbox — press anywhere and drag to aim a launch (the arrow is the velocity), then let
 * go. While you aim, the path is predicted with the same integrator, coloured green for a closed
 * orbit, red for a crash and orange for an escape, and the arrow carries marks for circular speed
 * √(GM/r) and escape speed √(2GM/r). Units are real: GM☉ = 4π² AU³/yr², 1 AU/yr = 4.74 km/s.
 */
import { createKit, T, Spring, fmt, clamp, arrow, text, withAlpha, sphere } from '../core/kit2d.js';
import { starfield, glow, npill } from '../core/space2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const GM1 = 4 * Math.PI * Math.PI;
const KMS = 4.7406;
const MAXP = 8, TRAIL = 220, PRED = 900;
const COLORS = ['#60a5fa', '#34d399', '#f472b6', '#fbbf24', '#a78bfa', '#f87171', '#2dd4bf', '#e2e8f0'];

export default function init(stage) {
  const k = createKit(stage, { night: true, captureTouch: true, label: 'A star in space; drag and release to launch planets' });
  const hud = createHud(stage);
  const badge = hud.badge('Press and drag to aim, release to launch', '#60a5fa');

  let M = 1, speed = 1, paused = false;
  const px = new Float64Array(MAXP), py = new Float64Array(MAXP), vx = new Float64Array(MAXP), vy = new Float64Array(MAXP);
  const alive = new Uint8Array(MAXP), fate = new Uint8Array(MAXP);
  const tx = new Float32Array(MAXP * TRAIL), ty = new Float32Array(MAXP * TRAIL), tn = new Uint16Array(MAXP), th = new Uint16Array(MAXP);
  const predX = new Float32Array(PRED), predY = new Float32Array(PRED);
  let predN = 0, predFate = 0, n = 0, last = -1, aiming = false, ax = 0, ay = 0, avx = 0, avy = 0;
  const starPulse = new Spring(1, 120, 10);

  const panel = createPanel(stage, { title: 'Orbit sandbox' });
  panel.slider({ label: 'Star mass', min: 0.3, max: 3, step: 0.1, value: 1, format: (v) => `${v.toFixed(1)} M☉`, onChange: (v) => { M = v; starPulse.v = 6; } });
  panel.chips({ label: 'Time speed', options: [{ value: '0.25', label: '¼ yr/s' }, { value: '1', label: '1 yr/s' }, { value: '3', label: '3 yr/s' }], value: '1', onChange: (v) => { speed = +v; } });
  panel.buttonRow([
    { label: 'Earth orbit', icon: 'public', onClick: () => launch(1, 0, 0, Math.sqrt(GM1 * M)) },
    { label: 'Clear', icon: 'delete_sweep', variant: 'ghost', onClick: () => { n = 0; alive.fill(0); last = -1; } },
  ]);
  const st = panel.stats([{ key: 'v', label: 'Launch speed' }, { key: 'vc', label: 'Circular speed here' }, { key: 'fate', label: 'Result' }, { key: 'T', label: 'Period (Kepler III)' }]);
  panel.info('An orbit is falling sideways forever: too slow and the planet falls into the star, too fast (above escape speed) and it leaves for good. In between it loops round on an ellipse. A heavier star needs faster planets.');

  let cx = 0, cy = 0, sc = 100;
  k.onResize((w, h) => { cx = w / 2; cy = h / 2; sc = Math.min(w, h) / 2 / 3.2; });
  const W = (x) => cx + x * sc, H = (y) => cy - y * sc;
  const Rstar = () => 0.1 * Math.cbrt(M);

  function acc(x, y, out) { const r2 = x * x + y * y, r = Math.sqrt(r2), f = -GM1 * M / (r2 * r); out[0] = f * x; out[1] = f * y; }
  const A = new Float64Array(2);
  function step1(i, h) {
    acc(px[i], py[i], A);
    vx[i] += A[0] * h / 2; vy[i] += A[1] * h / 2;
    px[i] += vx[i] * h; py[i] += vy[i] * h;
    acc(px[i], py[i], A);
    vx[i] += A[0] * h / 2; vy[i] += A[1] * h / 2;
  }
  function launch(x, y, ux, uy) {
    const i = n < MAXP ? n++ : (last + 1) % MAXP;
    px[i] = x; py[i] = y; vx[i] = ux; vy[i] = uy; alive[i] = 1; fate[i] = 0; tn[i] = 0; th[i] = 0; last = i;
    k.animate(true);
  }
  function predict(x, y, ux, uy) {
    let X = x, Y = y, VX = ux, VY = uy, h = 0.004;
    predN = 0; predFate = 0;
    const E = 0.5 * (ux * ux + uy * uy) - GM1 * M / Math.hypot(x, y);
    for (let s = 0; s < PRED * 4 && predN < PRED; s++) {
      const r = Math.hypot(X, Y);
      if (r < Rstar()) { predFate = 1; break; }
      if (r > 8) { predFate = 2; break; }
      let r3 = r * r * r; VX -= GM1 * M * X / r3 * h / 2; VY -= GM1 * M * Y / r3 * h / 2;
      X += VX * h; Y += VY * h;
      const r2 = Math.hypot(X, Y); r3 = r2 * r2 * r2; VX -= GM1 * M * X / r3 * h / 2; VY -= GM1 * M * Y / r3 * h / 2;
      if (s % 4 === 0) { predX[predN] = X; predY[predN] = Y; predN++; }
    }
    if (!predFate && E >= 0) predFate = 2;
  }

  k.drag({
    hit: () => 1,
    down: (x, y) => { aiming = true; ax = (x - cx) / sc; ay = (cy - y) / sc; avx = 0; avy = 0; k.animate(true); },
    move: (x, y) => { avx = ((x - cx) / sc - ax) * 3; avy = ((cy - y) / sc - ay) * 3; predict(ax, ay, avx, avy); },
    up: () => { aiming = false; if (Math.hypot(ax, ay) > Rstar() * 1.2) launch(ax, ay, avx, avy); },
    cursor: 'crosshair', cursorActive: 'crosshair',
  });

  k.frame((ctx, dt, w, h) => {
    starPulse.to(1); starPulse.step(dt);
    if (!paused) {
      const simDt = dt * speed, sub = Math.max(1, Math.ceil(simDt / 0.0015)), hh = simDt / sub;
      for (let i = 0; i < n; i++) {
        if (!alive[i]) continue;
        for (let s = 0; s < sub; s++) step1(i, hh);
        const r = Math.hypot(px[i], py[i]);
        if (r < Rstar()) { alive[i] = 0; fate[i] = 1; starPulse.v = 4; }
        else if (r > 12) { alive[i] = 0; fate[i] = 2; }
        const j = i * TRAIL + th[i];
        tx[j] = px[i]; ty[j] = py[i]; th[i] = (th[i] + 1) % TRAIL; if (tn[i] < TRAIL) tn[i]++;
      }
    }
    starfield(k, ctx, w, h, { seed: 7 });
    // distance rings
    ctx.strokeStyle = 'rgba(140,170,255,0.08)'; ctx.lineWidth = 1;
    for (let r = 1; r <= 3; r++) { ctx.beginPath(); ctx.arc(cx, cy, r * sc, 0, Math.PI * 2); ctx.stroke(); text(ctx, `${r} AU`, cx + r * sc + 4, cy - 4, 'rgba(170,190,230,0.5)', 9.5, 600); }
    // star
    const rs = Rstar() * sc * starPulse.x;
    glow(ctx, cx, cy, rs * 7, '#ffd27a', 0.9);
    sphere(ctx, cx, cy, rs, '#ffcf5c');
    // trails and planets
    for (let i = 0; i < n; i++) {
      const c = COLORS[i % COLORS.length];
      const cnt = tn[i];
      for (let m = 1; m < cnt; m++) {
        const a = i * TRAIL + (th[i] - cnt + m - 1 + TRAIL) % TRAIL, b = i * TRAIL + (th[i] - cnt + m + TRAIL) % TRAIL;
        ctx.strokeStyle = withAlpha(c, (alive[i] ? 0.7 : 0.25) * m / cnt); ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(W(tx[a]), H(ty[a])); ctx.lineTo(W(tx[b]), H(ty[b])); ctx.stroke();
      }
      if (alive[i]) { glow(ctx, W(px[i]), H(py[i]), 14, c, 0.5); sphere(ctx, W(px[i]), H(py[i]), 6, c); }
    }
    // aiming
    if (aiming) {
      const r = Math.hypot(ax, ay), vc = Math.sqrt(GM1 * M / Math.max(r, 1e-3));
      const col = predFate === 1 ? '#f87171' : predFate === 2 ? '#fbbf24' : '#34d399';
      ctx.setLineDash([3, 5]); ctx.strokeStyle = withAlpha(col, 0.85); ctx.lineWidth = 1.6; ctx.beginPath();
      for (let p = 0; p < predN; p++) { const X = W(predX[p]), Y = H(predY[p]); if (p) ctx.lineTo(X, Y); else ctx.moveTo(W(ax), H(ay)); }
      ctx.stroke(); ctx.setLineDash([]);
      const sx = W(ax), sy = H(ay), v = Math.hypot(avx, avy);
      sphere(ctx, sx, sy, 6, '#e2e8f0');
      if (v > 0.01) {
        arrow(ctx, sx, sy, sx + avx / 3 * sc, sy - avy / 3 * sc, '#e8eefb', 2.2);
        const ux = avx / v, uy = avy / v;
        for (const [mult, lab, cc] of [[1, 'circular', '#34d399'], [Math.SQRT2, 'escape', '#fbbf24']]) {
          const L = vc * mult / 3 * sc, mx = sx + ux * L, my = sy - uy * L;
          ctx.strokeStyle = cc; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(mx - uy * 8, my - ux * 8); ctx.lineTo(mx + uy * 8, my + ux * 8); ctx.stroke();
          if (!k.small) text(ctx, lab, mx + uy * 12, my + ux * 12, cc, 9.5, 700);
        }
        npill(ctx, `${fmt(v * KMS, 1)} km/s`, sx, sy - 22, col, 11);
      }
    }
    // stats
    if (aiming || last >= 0) {
      const X = aiming ? ax : px[last], Y = aiming ? ay : py[last], VX = aiming ? avx : vx[last], VY = aiming ? avy : vy[last];
      const r = Math.hypot(X, Y), v = Math.hypot(VX, VY), E = 0.5 * v * v - GM1 * M / r, a = -GM1 * M / (2 * E);
      st.v.set(`${fmt(v * KMS, 1)} km/s`); st.vc.set(`${fmt(Math.sqrt(GM1 * M / r) * KMS, 1)} km/s`);
      const f = aiming ? predFate : fate[last] || (E >= 0 ? 2 : 0);
      st.fate.set(f === 1 ? 'crash into the star' : f === 2 ? 'escapes' : 'stable orbit');
      st.T.set(E < 0 ? `${fmt(2 * Math.PI * Math.sqrt(a * a * a / (GM1 * M)), 2)} yr` : '—');
      badge.set(aiming ? (predFate === 1 ? 'Too slow: it will fall into the star' : predFate === 2 ? 'Too fast: it will escape' : 'Just right: a closed orbit') : 'Press and drag to aim, release to launch');
    }
    let any = false; for (let i = 0; i < n; i++) if (alive[i]) any = true;
    k.animate(any || aiming || starPulse.moving);
  });

  launch(1, 0, 0, Math.sqrt(GM1));
  k.debug = { at: (x, y) => [cx + x * sc, cy - y * sc], alive: () => Array.from(alive.slice(0, n)), fate: () => Array.from(fate.slice(0, n)) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
