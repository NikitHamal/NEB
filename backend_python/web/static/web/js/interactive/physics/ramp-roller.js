/**
 * Ramps and rolling — drag the top of the ramp to tilt it, pick what rolls and the surface, then
 * race to the finish. A solid ball rolling without slipping accelerates at
 * a = (5/7)·g·(sin θ − c·cos θ) (a hoop at ½, a sliding block at g(sin θ − μ cos θ)); if the slope
 * is too gentle for the surface it never starts. The stopwatch and the formula t = √(2L/a) agree.
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, sphere, softShadow, knob, arrow, withAlpha, card } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const DEG = Math.PI / 180;
const G = 9.81;
const L = 3;
const ROLLERS = [
  { value: 'ball', label: 'Solid ball', f: 5 / 7, color: '#e5484d' },
  { value: 'hoop', label: 'Hoop', f: 1 / 2, color: '#7c3aed' },
  { value: 'block', label: 'Sliding block', f: 1, color: '#f08c00' },
];
const SURF = [
  { value: 'glass', label: 'Smooth', c: 0.005, mu: 0.05, color: '#bfe3f7' },
  { value: 'wood', label: 'Wood', c: 0.02, mu: 0.3, color: '#d9b07a' },
  { value: 'carpet', label: 'Carpet', c: 0.12, mu: 0.55, color: '#b28fc4' },
  { value: 'sand', label: 'Sand', c: 0.3, mu: 0.7, color: '#e6cf98' },
];

export default function init(stage) {
  const k = createKit(stage, { label: 'A ramp with a ball at the top and a finish line at the bottom' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the ramp top to tilt it, then press Go', T.blue);

  let theta = 20 * DEG, roller = ROLLERS[0], surf = SURF[1];
  let s = 0, v = 0, t = 0, racing = false, done = false, stuck = false, spin = 0;
  const runs = [];
  const pop = new Spring(0, 200, 14);
  const hotTop = new Spring(0, 260, 26);

  const panel = createPanel(stage, { title: 'Ramp race' });
  const angS = panel.slider({ label: 'Ramp angle θ', min: 3, max: 60, step: 1, value: 20, format: (x) => `${x}°`, onChange: (x) => { theta = x * DEG; reset(); } });
  panel.chips({ label: 'What rolls?', options: ROLLERS.map((r) => ({ value: r.value, label: r.label, color: r.color })), value: 'ball', onChange: (x) => { roller = ROLLERS.find((r) => r.value === x); reset(); } });
  panel.chips({ label: 'Ramp surface', options: SURF.map((r) => ({ value: r.value, label: r.label, color: r.color })), value: 'wood', onChange: (x) => { surf = SURF.find((r) => r.value === x); reset(); } });
  panel.buttonRow([{ label: 'Go!', icon: 'flag', onClick: go }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset }]);
  const st = panel.stats([{ key: 't', label: 'Stopwatch' }, { key: 'pred', label: 'Formula √(2L/a)' }, { key: 'a', label: 'Acceleration' }, { key: 'v', label: 'Speed at finish' }]);
  panel.info('The ramp is 3 m long. Gravity pulls along the slope with g·sin θ, so steeper is faster. A rolling ball also has to spin up, so it is slower than a frictionless slide; a hoop is slower still.');

  function accel() {
    if (roller.value === 'block') return G * (Math.sin(theta) - surf.mu * Math.cos(theta));
    return roller.f * G * (Math.sin(theta) - surf.c * Math.cos(theta));
  }
  function reset() { s = 0; v = 0; t = 0; racing = false; done = false; stuck = false; spin = 0; k.invalidate(); }
  function go() {
    reset();
    if (accel() <= 0) { stuck = true; pop.v = 30; k.animate(true); return; }
    racing = true; k.animate(true);
  }

  let bx0 = 0, by0 = 0, scale = 100;
  k.onResize((w, h) => { bx0 = k.small ? 20 : 60; by0 = h - 70; scale = Math.min((w - bx0 - (k.small ? 30 : 230)) / L, (by0 - 70) / (L * Math.sin(60 * DEG))); });
  const topX = () => bx0, topY = () => by0 - L * Math.sin(theta) * scale;
  const botX = () => bx0 + L * Math.cos(theta) * scale;

  const topH = k.drag({
    hit: (x, y, sl) => { const d = Math.hypot(x - topX(), y - topY()); return d < 18 + sl ? d : false; },
    move: (x, y) => { const hgt = clamp(by0 - y, 10, L * scale); theta = clamp(Math.round(Math.asin(hgt / (L * scale)) / DEG), 3, 60) * DEG; angS.set(Math.round(theta / DEG)); reset(); },
    cursor: 'ns-resize',
  });

  k.frame((ctx, dt, w, h) => {
    if (racing) {
      const a = accel();
      const n = 8, hh = dt / n;
      for (let i = 0; i < n && racing; i++) {
        const ns = s + v * hh + 0.5 * a * hh * hh;
        if (ns >= L) { const tc = (-v + Math.sqrt(v * v + 2 * a * (L - s))) / a; t += tc; v += a * tc; s = L; racing = false; done = true; pop.v = 40; runs.unshift({ a: Math.round(theta / DEG), r: roller.label, s: surf.label, t, v }); if (runs.length > 5) runs.pop(); }
        else { s = ns; v += a * hh; t += hh; }
      }
    }
    pop.step(dt); hotTop.to(k.isHot(topH) ? 1 : 0); hotTop.step(dt);
    background(k, ctx, w, h);
    // floor
    ctx.fillStyle = '#dfe6f0'; ctx.fillRect(0, by0, w, h - by0);
    ctx.fillStyle = '#c9d3e1'; ctx.fillRect(0, by0, w, 3);
    // ramp body
    const tx = topX(), ty = topY(), bx = botX();
    ctx.beginPath(); ctx.moveTo(tx, ty); ctx.lineTo(bx, by0); ctx.lineTo(tx, by0); ctx.closePath();
    const rg = k.cache('ramp' + Math.round(ty), () => { const g = ctx.createLinearGradient(0, ty, 0, by0); g.addColorStop(0, '#e9d3b2'); g.addColorStop(1, '#cfae80'); return g; });
    ctx.fillStyle = rg; ctx.fill();
    ctx.strokeStyle = '#a77d4b'; ctx.lineWidth = 1.5; ctx.stroke();
    // surface strip
    ctx.strokeStyle = surf.color; ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(tx, ty - 3); ctx.lineTo(bx, by0 - 3); ctx.stroke();
    // metre marks along the ramp
    const ux = Math.cos(theta), uy = Math.sin(theta);
    for (let m = 0.5; m < L; m += 0.5) { const mx = tx + ux * m * scale, my = ty + uy * m * scale; ctx.strokeStyle = 'rgba(80,50,20,0.4)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(mx + uy * 2, my - ux * 2); ctx.lineTo(mx + uy * 9, my - ux * 9); ctx.stroke(); }
    // angle arc
    ctx.strokeStyle = T.blue; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(bx, by0, 46, Math.PI, Math.PI + theta); ctx.stroke();
    text(ctx, `${Math.round(theta / DEG)}°`, bx - 62, by0 - 10, T.blue, 12, 700, 'right');
    // height dimension
    ctx.strokeStyle = T.ink2; ctx.lineWidth = 1; ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(tx - 10, ty); ctx.lineTo(tx - 10, by0); ctx.stroke(); ctx.setLineDash([]);
    if (!k.small) pill(ctx, `h = ${fmt(L * Math.sin(theta), 2)} m`, tx + 46, (ty + by0) / 2, { size: 10, color: T.ink2 });
    // finish flag
    ctx.fillStyle = '#334155'; ctx.fillRect(bx + 2, by0 - 70, 3, 70);
    for (let i = 0; i < 4; i++) for (let j = 0; j < 3; j++) { ctx.fillStyle = (i + j) % 2 ? '#172033' : '#fff'; ctx.fillRect(bx + 5 + i * 7, by0 - 70 + j * 7, 7, 7); }
    text(ctx, 'FINISH', bx + 4, by0 - 76, T.ink, 10, 800);
    // the roller
    const R = 0.12 * scale;
    const cxp = tx + ux * s * scale + uy * R, cyp = ty + uy * s * scale - ux * R;
    spin = s / 0.12;
    softShadow(ctx, cxp - uy * R, cyp + ux * R + 2, R * 1.1, 3, 0.25);
    if (roller.value === 'block') {
      ctx.save(); ctx.translate(cxp, cyp); ctx.rotate(theta);
      ctx.fillStyle = roller.color; ctx.strokeStyle = '#a35f00'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.roundRect(-R * 1.1, -R, R * 2.2, R * 2, 3); ctx.fill(); ctx.stroke(); ctx.restore();
    } else if (roller.value === 'hoop') {
      ctx.save(); ctx.translate(cxp, cyp); ctx.rotate(spin);
      ctx.strokeStyle = roller.color; ctx.lineWidth = R * 0.28; ctx.beginPath(); ctx.arc(0, 0, R * 0.86, 0, Math.PI * 2); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(0, 0, R * 0.86, -0.3, 0.3); ctx.stroke(); ctx.restore();
    } else {
      sphere(ctx, cxp, cyp, R, roller.color);
      ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(cxp, cyp, R * 0.62, spin, spin + 1.2); ctx.stroke();
    }
    // gravity component arrow
    if (!k.small || racing) {
      const comp = G * Math.sin(theta) * 7;
      arrow(ctx, cxp, cyp, cxp + ux * comp, cyp + uy * comp, T.green, 2.5);
      if (s < 0.3) text(ctx, 'g sin θ', cxp + ux * comp + 6, cyp + uy * comp - 4, T.green, 10, 700);
    }
    knob(ctx, tx, ty, 9, T.blue, hotTop.x);
    // stopwatch
    const swx = k.small ? w - 70 : w - 120, swy = 70, sr = k.small ? 34 : 44;
    ctx.beginPath(); ctx.arc(swx, swy, sr + 4, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = T.line; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#94a3b8'; ctx.fillRect(swx - 5, swy - sr - 12, 10, 8);
    ctx.strokeStyle = T.line2; ctx.lineWidth = 1; ctx.beginPath();
    for (let i = 0; i < 60; i += 5) { const a = i / 60 * Math.PI * 2; ctx.moveTo(swx + Math.sin(a) * sr, swy - Math.cos(a) * sr); ctx.lineTo(swx + Math.sin(a) * (sr - 5), swy - Math.cos(a) * (sr - 5)); }
    ctx.stroke();
    const ha = (t % 5) / 5 * Math.PI * 2;
    ctx.strokeStyle = T.red; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(swx, swy); ctx.lineTo(swx + Math.sin(ha) * (sr - 6), swy - Math.cos(ha) * (sr - 6)); ctx.stroke();
    text(ctx, `${fmt(t, 2)} s`, swx, swy + sr * 0.45, T.ink, k.small ? 12 : 14, 700, 'center');
    if (done) pill(ctx, `${fmt(t, 2)} s!`, bx, by0 - 96 - pop.x * 0.2, { bg: T.green, color: '#fff', border: false, size: 13 });
    if (stuck) pill(ctx, 'Too gentle — friction wins, it will not start', (tx + bx) / 2, ty - 30, { color: T.red, size: 11.5 });
    // results
    if (!k.small && runs.length) {
      const cx = w - 220, cy = 140, ch = 30 + runs.length * 20;
      card(ctx, cx, cy, 206, ch, 10);
      text(ctx, 'Races', cx + 12, cy + 19, T.ink, 11.5, 700);
      for (let i = 0; i < runs.length; i++) { const r = runs[i]; text(ctx, `${r.a}° · ${r.r} · ${r.s}`, cx + 12, cy + 38 + i * 20, T.ink2, 10, 500); text(ctx, `${fmt(r.t, 2)} s`, cx + 194, cy + 38 + i * 20, i === 0 ? T.green : T.ink, 10.5, 700, 'right'); }
    }
    const a = accel();
    st.t.set(`${fmt(t, 2)} s`); st.pred.set(a > 0 ? `${fmt(Math.sqrt(2 * L / a), 2)} s` : 'never');
    st.a.set(`${fmt(Math.max(0, a), 2)} m/s²`); st.v.set(done ? `${fmt(v, 2)} m/s` : '—');
    badge.set(racing ? `${fmt(v, 2)} m/s` : done ? `Finished in ${fmt(t, 2)} s` : stuck ? 'Stuck: try a steeper ramp' : 'Drag the ramp top to tilt it, then press Go');
    k.animate(racing || pop.moving || hotTop.moving);
  });

  k.debug = { top: () => [topX(), topY()], go, time: () => t, done: () => done };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
