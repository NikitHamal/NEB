/**
 * Kepler's laws — a planet on an ellipse with the Sun at one focus, moved by Kepler's equation
 * (M = E − e sin E, solved by Newton's method), so its speed is exactly what the second law
 * demands. Drag the aphelion end of the orbit to stretch it, or drag the planet to scrub time.
 * Twelve sectors swept in equal times are shaded: thin and long far away, short and wide close in,
 * all with equal area. The third-law panel plots T² against a³ for the real planets.
 */
import { createKit, T, Spring, fmt, clamp, text, withAlpha, sphere, knob, card, arrow } from '../core/kit2d.js';
import { starfield, glow, npill } from '../core/space2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const PLANETS = [['Mercury', 0.387, 0.206], ['Venus', 0.723, 0.007], ['Earth', 1, 0.017], ['Mars', 1.524, 0.093], ['Jupiter', 5.203, 0.048], ['Saturn', 9.537, 0.054]];
const SECT = 12;

export default function init(stage) {
  const k = createKit(stage, { night: true, label: 'An elliptical orbit with the Sun at one focus and equal-area sectors' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the far end of the orbit to stretch it', '#60a5fa');

  let a = 1, e = 0.5, t = 0, rate = 0.25, showSectors = true, scrub = false;
  const zoom = new Spring(100, 60, 14);
  let first = true;

  const panel = createPanel(stage, { title: "Kepler's laws" });
  const eS = panel.slider({ label: 'Eccentricity e', min: 0, max: 0.9, step: 0.01, value: e, format: (v) => v.toFixed(2), onChange: (v) => { e = v; } });
  const aS = panel.slider({ label: 'Semi-major axis a', min: 0.4, max: 5.2, step: 0.01, value: a, format: (v) => `${v.toFixed(2)} AU`, onChange: (v) => { a = v; } });
  panel.chips({ label: 'Real orbits', options: PLANETS.map((p) => ({ value: p[0], label: p[0] })).concat([{ value: 'Halley', label: "Halley's comet" }]), value: '', onChange: (v) => { const p = PLANETS.find((q) => q[0] === v); if (p) { a = p[1]; e = p[2]; } else { a = 17.8; e = 0.967; } aS.set(Math.min(a, 5.2)); eS.set(Math.min(e, 0.9)); } });
  panel.toggle({ label: 'Equal-time sectors', value: true, onChange: (v) => { showSectors = v; } });
  panel.slider({ label: 'Animation speed', min: 0.05, max: 1, step: 0.05, value: rate, format: (v) => `${v.toFixed(2)} orbits/s`, onChange: (v) => { rate = v; } });
  const st = panel.stats([{ key: 'T', label: 'Period T = a^1.5' }, { key: 'r', label: 'Distance now' }, { key: 'v', label: 'Speed now' }, { key: 'pa', label: 'Perihelion / aphelion' }]);
  panel.info('1: orbits are ellipses with the Sun at one focus. 2: the line to the Sun sweeps equal areas in equal times, so the planet speeds up near the Sun. 3: T² ∝ a³ (T in years, a in AU, T² = a³ for anything orbiting the Sun).');

  function solveE(M) { let E = e < 0.8 ? M : Math.PI; for (let i = 0; i < 30; i++) { const f = E - e * Math.sin(E) - M; E -= f / (1 - e * Math.cos(E)); if (Math.abs(f) < 1e-12) break; } return E; }
  function pos(M, out) { const E = solveE(M); out[0] = a * (Math.cos(E) - e); out[1] = a * Math.sqrt(1 - e * e) * Math.sin(E); return out; }
  const P = new Float64Array(2);

  let cx = 0, cy = 0, sc = 100, gx = 0, gy = 0, gw = 0, gh = 0;
  k.onResize((w, h) => {
    const graphW = k.small ? 0 : Math.min(260, w * 0.3);
    cx = (w - graphW) * 0.5 + 40; cy = h * (k.small ? 0.5 : 0.5); sc = 1;
    gx = w - graphW - 16; gy = 50; gw = graphW; gh = Math.min(240, h * 0.45);
  });
  function fit(w, h) { const avail = Math.min((w - (k.small ? 0 : gw + 40)) * 0.45, h * 0.42); return avail / (a * (1 + e) + 0.05); }
  const X = (x) => cx + x * sc, Y = (y) => cy - y * sc;

  const apo = k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - X(-a * (1 + e)), y - Y(0)); return d < 14 + s ? d : false; },
    move: (x) => { const ra = clamp((cx - x) / sc, 0.3, 12), rp = a * (1 - e); const na = (ra + rp) / 2, ne = clamp((ra - rp) / (ra + rp), 0, 0.9); a = clamp(na, 0.4, 5.2); e = ne; aS.set(a); eS.set(e); },
    cursor: 'ew-resize',
  });
  const planetH = k.drag({
    hit: (x, y, s) => { pos(2 * Math.PI * (t % 1), P); const d = Math.hypot(x - X(P[0]), y - Y(P[1])); return d < 14 + s ? d : false; },
    down: () => { scrub = true; },
    move: (x, y) => { const px = (x - cx) / sc + a * e, py = (cy - y) / sc / Math.sqrt(1 - e * e); const E = Math.atan2(py, px); let M = E - e * Math.sin(E); if (M < 0) M += 2 * Math.PI; t = Math.floor(t) + M / (2 * Math.PI); },
    up: () => { scrub = false; },
  });

  k.frame((ctx, dt, w, h) => {
    if (first) { zoom.set(fit(w, h)); first = false; }
    if (k.active !== apo) { zoom.to(fit(w, h)); zoom.step(dt); } sc = zoom.x;
    const Tyr = Math.pow(a, 1.5);
    if (!scrub) t += dt * rate;
    starfield(k, ctx, w, h, { seed: 11 });
    // sectors swept in equal times
    if (showSectors) {
      for (let s = 0; s < SECT; s++) {
        ctx.beginPath(); ctx.moveTo(X(0), Y(0));
        for (let j = 0; j <= 16; j++) { pos(2 * Math.PI * (s + j / 16) / SECT, P); ctx.lineTo(X(P[0]), Y(P[1])); }
        ctx.closePath(); ctx.fillStyle = s % 2 ? 'rgba(96,165,250,0.16)' : 'rgba(167,139,250,0.16)'; ctx.fill();
      }
      npill(ctx, `each sector: ${fmt(Tyr / SECT * 365.25, 0)} days, area ${fmt(Math.PI * a * a * Math.sqrt(1 - e * e) / SECT, 3)} AU²`, w * 0.5 - (k.small ? 0 : gw / 2), h - 22, '#c7d2fe', 10);
    }
    // ellipse
    ctx.strokeStyle = 'rgba(200,215,255,0.65)'; ctx.lineWidth = 1.6; ctx.beginPath();
    ctx.ellipse(X(-a * e), Y(0), a * sc, a * Math.sqrt(1 - e * e) * sc, 0, 0, Math.PI * 2); ctx.stroke();
    // foci and axis
    ctx.setLineDash([3, 5]); ctx.strokeStyle = 'rgba(200,215,255,0.25)'; ctx.beginPath(); ctx.moveTo(X(-a * (1 + e)), Y(0)); ctx.lineTo(X(a * (1 - e)), Y(0)); ctx.stroke(); ctx.setLineDash([]);
    ctx.beginPath(); ctx.arc(X(-2 * a * e), Y(0), 3, 0, Math.PI * 2); ctx.fillStyle = 'rgba(200,215,255,0.6)'; ctx.fill();
    if (e > 0.05) text(ctx, 'empty focus', X(-2 * a * e), Y(0) + 16, 'rgba(200,215,255,0.6)', 9.5, 600, 'center');
    glow(ctx, X(0), Y(0), 46, '#ffd27a', 0.9); sphere(ctx, X(0), Y(0), 9, '#ffcf5c');
    text(ctx, 'perihelion', X(a * (1 - e)) + 8, Y(0) - 8, '#fbbf24', 10, 700);
    knob(ctx, X(-a * (1 + e)), Y(0), 7, '#60a5fa', k.isHot(apo) ? 1 : 0);
    text(ctx, 'aphelion', X(-a * (1 + e)), Y(0) - 16, '#93c5fd', 10, 700, 'center');
    // planet, radius line and velocity
    const M = 2 * Math.PI * (t % 1);
    pos(M, P);
    const r = Math.hypot(P[0], P[1]), GM = 4 * Math.PI * Math.PI, v = Math.sqrt(GM * (2 / r - 1 / a));
    ctx.strokeStyle = 'rgba(255,210,122,0.6)'; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(P[0]), Y(P[1])); ctx.stroke();
    const E = solveE(M), vxd = -a * Math.sin(E), vyd = a * Math.sqrt(1 - e * e) * Math.cos(E), vl = Math.hypot(vxd, vyd);
    arrow(ctx, X(P[0]), Y(P[1]), X(P[0]) + vxd / vl * v * 9, Y(P[1]) - vyd / vl * v * 9, '#34d399', 2.2);
    glow(ctx, X(P[0]), Y(P[1]), 18, '#60a5fa', 0.6); sphere(ctx, X(P[0]), Y(P[1]), 7, '#60a5fa');
    npill(ctx, `${fmt(v * 4.7406, 1)} km/s`, X(P[0]), Y(P[1]) - 22, '#a7f3d0', 10);
    // third law graph
    if (gw > 0) {
      card(ctx, gx, gy, gw, gh, 12, 'rgba(15,25,48,0.92)', 'rgba(160,190,255,0.18)');
      text(ctx, "Kepler's third law: T² = a³", gx + 12, gy + 20, '#e8eefb', 11.5, 700);
      const ix = gx + 40, iy = gy + 34, iw = gw - 56, ih = gh - 64;
      const L = (v2) => Math.log10(v2);
      const lx = (v2) => ix + (L(v2) + 0.5) / 2.0 * iw, ly = (v2) => iy + ih - (L(v2) + 1) / 4 * ih;
      ctx.strokeStyle = 'rgba(160,190,255,0.2)'; ctx.strokeRect(ix, iy, iw, ih);
      ctx.strokeStyle = 'rgba(96,165,250,0.6)'; ctx.beginPath(); ctx.moveTo(lx(0.3), ly(Math.pow(0.3, 1.5))); ctx.lineTo(lx(31), ly(Math.pow(31, 1.5))); ctx.stroke();
      for (const p of PLANETS) { ctx.beginPath(); ctx.arc(lx(p[1]), ly(Math.pow(p[1], 1.5)), 3.5, 0, Math.PI * 2); ctx.fillStyle = '#e2e8f0'; ctx.fill(); text(ctx, p[0], lx(p[1]) + 6, ly(Math.pow(p[1], 1.5)) + 3, '#aab8d3', 9, 600); }
      ctx.beginPath(); ctx.arc(lx(a), ly(Tyr), 5, 0, Math.PI * 2); ctx.fillStyle = '#34d399'; ctx.fill();
      text(ctx, 'log a (AU) →', ix + iw, iy + ih + 16, '#8ea0c2', 9, 600, 'right'); text(ctx, 'log T (yr)', ix - 4, iy - 4, '#8ea0c2', 9, 600);
    }
    st.T.set(`${fmt(Tyr, 2)} yr`); st.r.set(`${fmt(r, 2)} AU`); st.v.set(`${fmt(v * 4.7406, 1)} km/s`); st.pa.set(`${fmt(a * (1 - e), 2)} / ${fmt(a * (1 + e), 2)} AU`);
    badge.set(e < 0.02 ? 'A circle is an ellipse with e = 0: constant speed' : `Fastest at perihelion: ${fmt(Math.sqrt(GM * (2 / (a * (1 - e)) - 1 / a)) * 4.74, 1)} km/s, slowest at aphelion: ${fmt(Math.sqrt(GM * (2 / (a * (1 + e)) - 1 / a)) * 4.74, 1)} km/s`);
    k.animate(true);
  });

  k.debug = { apo: () => [X(-a * (1 + e)), Y(0)], state: () => [a, e] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
