/**
 * Bouncing balls — tap to drop a ball from that height, or grab one and throw it. Free flight is
 * integrated exactly (constant gravity), each floor impact is found at its true instant and the
 * rebound speed is e × the impact speed, so every bounce peaks at e² of the one before. Balls
 * collide with each other with the same coefficient of restitution.
 */
import { createKit, T, Ring, fmt, clamp, background, text, pill, sphere, softShadow, withAlpha, dashed, DASH } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const WORLDS = [
  { value: 'moon', label: 'Moon', g: 1.62, color: '#9ca3af' },
  { value: 'earth', label: 'Earth', g: 9.81, color: '#2563eb' },
  { value: 'jupiter', label: 'Jupiter', g: 24.79, color: '#c58b4c' },
];
const BALLS = [
  { value: 'super', label: 'Super ball', e: 0.9, r: 0.06, color: '#e5484d' },
  { value: 'tennis', label: 'Tennis', e: 0.75, r: 0.067, color: '#b5d334' },
  { value: 'basket', label: 'Basketball', e: 0.8, r: 0.12, color: '#e8742a' },
  { value: 'clay', label: 'Clay', e: 0.15, r: 0.08, color: '#a07a5a' },
];
const MAX = (navigator.hardwareConcurrency || 4) <= 4 ? 8 : 14;
const ROOM_H = 3.2;

export default function init(stage) {
  const k = createKit(stage, { label: 'A room with a height ruler; tap to drop balls' });
  const hud = createHud(stage);
  const badge = hud.badge('Tap anywhere to drop a ball', T.blue);

  let g = 9.81, eSlider = 0.75, kind = BALLS[1], air = false, slow = false;
  const x = new Float64Array(MAX), y = new Float64Array(MAX), vx = new Float64Array(MAX), vy = new Float64Array(MAX);
  const r = new Float64Array(MAX), e = new Float64Array(MAX), sq = new Float64Array(MAX), sqv = new Float64Array(MAX);
  const col = new Array(MAX).fill('#e5484d');
  let n = 0, head = 0, tracked = -1, simT = 0;
  const peaks = new Float64Array(8); let nPeaks = 0, lastVy = 0;
  const trace = new Ring(600);
  let held = -1, holdX = 0, holdY = 0, holdT = 0, flingVx = 0, flingVy = 0;
  const puffs = new Float64Array(12 * 3); let puffHead = 0;

  const panel = createPanel(stage, { title: 'Bouncing balls' });
  panel.chips({ label: 'Ball', options: BALLS.map((b) => ({ value: b.value, label: b.label, color: b.color })), value: kind.value, onChange: (v) => { kind = BALLS.find((b) => b.value === v); eS.set(kind.e); eSlider = kind.e; } });
  const eS = panel.slider({ label: 'Bounciness e (restitution)', min: 0.05, max: 0.95, step: 0.05, value: kind.e, format: (v) => v.toFixed(2), onChange: (v) => { eSlider = v; for (let i = 0; i < n; i++) e[i] = v; } });
  panel.chips({ label: 'World', options: WORLDS.map((w) => ({ value: w.value, label: `${w.label} · ${w.g} m/s²`, color: w.color })), value: 'earth', onChange: (v) => { g = WORLDS.find((w) => w.value === v).g; } });
  panel.toggle({ label: 'Air resistance', value: false, onChange: (v) => { air = v; } });
  panel.toggle({ label: 'Slow motion (¼×)', value: false, onChange: (v) => { slow = v; } });
  panel.buttonRow([
    { label: 'Drop 2 m', icon: 'south', onClick: () => spawn(roomW * 0.5, 2, 0, 0) },
    { label: 'Clear', icon: 'delete_sweep', variant: 'ghost', onClick: () => { n = 0; head = 0; tracked = -1; nPeaks = 0; trace.clear(); k.invalidate(); } },
  ]);
  const st = panel.stats([{ key: 'h', label: 'Start height' }, { key: 'next', label: 'Next peak (e²h)' }, { key: 'last', label: 'Last peak' }, { key: 'ratio', label: 'Peak ratio' }]);
  panel.info('Each bounce keeps a fraction e of the speed, so it rises to e² of the height before. On the Moon the same ball falls slowly but bounces to the same fraction.');

  let scale = 100, floorY = 0, left = 0, roomW = 4, plotOn = true;
  const plot = new Plot({ title: 'Height of the last ball', xLabel: 't / s', yLabel: 'h / m', yMin: 0, yMax: 3 });
  k.onResize((w, h) => {
    plotOn = w > 640;
    const pw = plotOn ? Math.min(320, w * 0.32) : 0;
    left = 46;
    floorY = h - 44;
    scale = (floorY - 26) / ROOM_H;
    roomW = (w - left - pw - (plotOn ? 28 : 12)) / scale;
    if (plotOn) plot.box(w - pw - 14, 16, pw, Math.min(220, h * 0.4));
  });
  const SX = (m) => left + m * scale;
  const SY = (m) => floorY - m * scale;

  function spawn(mx, my, vx0, vy0) {
    const i = n < MAX ? n++ : (head = (head + 1) % MAX, head);
    x[i] = clamp(mx, kind.r, roomW - kind.r); y[i] = clamp(my, kind.r, ROOM_H - kind.r);
    vx[i] = vx0; vy[i] = vy0; r[i] = kind.r; e[i] = eSlider; col[i] = kind.color; sq[i] = 0; sqv[i] = 0;
    tracked = i; nPeaks = 0; peaks[nPeaks++] = y[i] - r[i]; lastVy = vy0; trace.clear(); simT = 0;
    k.animate(true);
    return i;
  }

  k.onTap((px, py) => { if (py < floorY) spawn((px - left) / scale, (floorY - py) / scale, 0, 0); });
  k.drag({
    hit: (px, py, s) => { let best = false; for (let i = 0; i < n; i++) { const d = Math.hypot(px - SX(x[i]), py - SY(y[i])); if (d < r[i] * scale + s && (best === false || d < best)) { best = d; } } return best; },
    down: (px, py) => {
      let bi = -1, bd = 1e9;
      for (let i = 0; i < n; i++) { const d = Math.hypot(px - SX(x[i]), py - SY(y[i])); if (d < bd) { bd = d; bi = i; } }
      held = bi; holdX = px; holdY = py; holdT = performance.now(); flingVx = 0; flingVy = 0;
      tracked = bi; nPeaks = 0; trace.clear(); simT = 0;
    },
    move: (px, py) => {
      if (held < 0) return;
      const now = performance.now(), dtm = Math.max(1, now - holdT) / 1000;
      const nvx = (px - holdX) / scale / dtm, nvy = -(py - holdY) / scale / dtm;
      flingVx = flingVx * 0.4 + nvx * 0.6; flingVy = flingVy * 0.4 + nvy * 0.6;
      holdX = px; holdY = py; holdT = now;
      x[held] = clamp((px - left) / scale, r[held], roomW - r[held]); y[held] = clamp((floorY - py) / scale, r[held], ROOM_H - r[held]);
      vx[held] = 0; vy[held] = 0;
    },
    up: () => {
      if (held < 0) return;
      const fresh = performance.now() - holdT < 80;
      vx[held] = fresh ? clamp(flingVx, -12, 12) : 0; vy[held] = fresh ? clamp(flingVy, -12, 12) : 0;
      nPeaks = 0; peaks[nPeaks++] = y[held] - r[held]; lastVy = vy[held];
      held = -1; k.animate(true);
    },
  });

  function puff(px, strength) {
    const j = puffHead * 3; puffs[j] = px; puffs[j + 1] = 0; puffs[j + 2] = strength; puffHead = (puffHead + 1) % 12;
  }

  function advance(i, h) {
    if (i === held) return;
    let rem = h;
    for (let guard = 0; guard < 4 && rem > 0; guard++) {
      let ax = 0, ay = -g;
      if (air) { const sp = Math.hypot(vx[i], vy[i]); const kd = 0.02 / r[i]; ax -= kd * sp * vx[i]; ay -= kd * sp * vy[i]; }
      const ny = y[i] + vy[i] * rem + 0.5 * ay * rem * rem;
      if (ny >= r[i] || vy[i] > 0 && ny >= r[i]) {
        x[i] += vx[i] * rem + 0.5 * ax * rem * rem; y[i] = ny; vx[i] += ax * rem; vy[i] += ay * rem; rem = 0;
      } else {
        const a = 0.5 * ay, b = vy[i], c = y[i] - r[i];
        const disc = Math.max(0, b * b - 4 * a * c);
        let tc = (-b - Math.sqrt(disc)) / (2 * a);
        if (!(tc >= 0 && tc <= rem)) tc = 0;
        x[i] += vx[i] * tc; vx[i] += ax * tc;
        const vImpact = vy[i] + ay * tc;
        y[i] = r[i];
        const speed = -vImpact;
        if (speed > 0.25) { sqv[i] -= Math.min(speed, 8) * 0.75; puff(x[i], Math.min(1, speed / 6)); }
        vy[i] = speed * e[i] > 0.12 ? speed * e[i] : 0;
        vx[i] *= vy[i] === 0 ? 0.985 : 0.97;
        rem -= tc;
        if (vy[i] === 0) { x[i] += vx[i] * rem; rem = 0; }
      }
    }
    if (x[i] < r[i]) { x[i] = r[i]; vx[i] = -vx[i] * e[i]; }
    if (x[i] > roomW - r[i]) { x[i] = roomW - r[i]; vx[i] = -vx[i] * e[i]; }
    if (y[i] > ROOM_H - r[i]) { y[i] = ROOM_H - r[i]; vy[i] = -Math.abs(vy[i]) * e[i]; }
  }

  function collide() {
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const dx = x[j] - x[i], dy = y[j] - y[i], d = Math.hypot(dx, dy), rr = r[i] + r[j];
      if (d >= rr || d < 1e-9) continue;
      const nx = dx / d, ny = dy / d;
      const mi = i === held ? 0 : r[i] * r[i] * r[i], mj = j === held ? 0 : r[j] * r[j] * r[j];
      const wi = mi ? 1 / mi : 0, wj = mj ? 1 / mj : 0;
      if (wi + wj === 0) continue;
      const corr = (rr - d) / (wi + wj);
      x[i] -= nx * corr * wi; y[i] -= ny * corr * wi; x[j] += nx * corr * wj; y[j] += ny * corr * wj;
      const rv = (vx[j] - vx[i]) * nx + (vy[j] - vy[i]) * ny;
      if (rv >= 0) continue;
      const jimp = -(1 + Math.min(e[i], e[j])) * rv / (wi + wj);
      vx[i] -= jimp * wi * nx; vy[i] -= jimp * wi * ny; vx[j] += jimp * wj * nx; vy[j] += jimp * wj * ny;
    }
  }

  k.frame((ctx, dt, w, h) => {
    const sdt = slow ? dt * 0.25 : dt;
    const sub = 8, hh = sdt / sub;
    let moving = held >= 0;
    for (let s = 0; s < sub; s++) { for (let i = 0; i < n; i++) advance(i, hh); collide(); }
    for (let i = 0; i < n; i++) {
      const a = -260 * sq[i] - 16 * sqv[i];
      sqv[i] += a * dt; sq[i] += sqv[i] * dt;
      if (Math.abs(sq[i]) < 1e-3 && Math.abs(sqv[i]) < 1e-2) { sq[i] = 0; sqv[i] = 0; }
      if (vy[i] !== 0 || Math.abs(vx[i]) > 0.01 || sq[i] !== 0 || y[i] > r[i] + 1e-6) moving = true;
    }
    if (tracked >= 0 && tracked < n) {
      simT += sdt;
      const hNow = y[tracked] - r[tracked];
      if (lastVy > 0 && vy[tracked] <= 0 && held !== tracked && nPeaks < 8) peaks[nPeaks++] = hNow;
      lastVy = vy[tracked];
      trace.push(simT, hNow);
    }

    background(k, ctx, w, h);
    // back wall tiles
    ctx.strokeStyle = 'rgba(37,99,235,0.06)'; ctx.lineWidth = 1; ctx.beginPath();
    for (let m = 0.5; m < ROOM_H; m += 0.5) { const py = Math.round(SY(m)) + 0.5; ctx.moveTo(left, py); ctx.lineTo(SX(roomW), py); }
    ctx.stroke();
    // floor
    const fg = k.cache('floor', () => { const gr = ctx.createLinearGradient(0, floorY, 0, h); gr.addColorStop(0, '#d9b98f'); gr.addColorStop(1, '#b98d5c'); return gr; });
    ctx.fillStyle = fg; ctx.fillRect(0, floorY, w, h - floorY);
    ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.fillRect(0, floorY, w, 2);
    ctx.strokeStyle = 'rgba(120,80,40,0.18)'; ctx.beginPath();
    for (let px = 60; px < w; px += 120) { ctx.moveTo(px, floorY + 3); ctx.lineTo(px - 18, h); }
    ctx.stroke();
    // ruler
    ctx.fillStyle = '#fff'; ctx.strokeStyle = T.line; ctx.beginPath(); ctx.roundRect(8, SY(ROOM_H) - 4, 32, ROOM_H * scale + 4, 6); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = T.ink2; ctx.beginPath();
    for (let cm = 0; cm <= ROOM_H * 100; cm += 10) { const py = Math.round(SY(cm / 100)) + 0.5; const l = cm % 50 === 0 ? 10 : 5; ctx.moveTo(40 - l, py); ctx.lineTo(40, py); }
    ctx.lineWidth = 1; ctx.stroke();
    for (let m = 0; m <= 3; m += 0.5) text(ctx, m % 1 === 0 ? m + ' m' : String(m), 12, SY(m) + 3.5, T.ink2, 9, 600);
    // peak markers of the tracked ball
    for (let p = 0; p < nPeaks; p++) {
      const py = SY(peaks[p]);
      const alpha = 1 - p / 9;
      ctx.strokeStyle = withAlpha(T.orange, 0.55 * alpha); ctx.setLineDash(DASH); ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(42, py); ctx.lineTo(tracked >= 0 ? SX(x[tracked]) - 14 : 120, py); ctx.stroke(); ctx.setLineDash([]);
      if (p < 4 && !k.small) pill(ctx, p === 0 ? `h = ${fmt(peaks[p], 2)} m` : `h${sub2(p)} = ${fmt(peaks[p], 2)}`, 50, py, { align: 'left', size: 10, color: T.orange });
    }
    // puffs
    for (let p = 0; p < 12; p++) {
      const j = p * 3; if (puffs[j + 2] <= 0.01) continue;
      puffs[j + 1] += dt * 1.8; puffs[j + 2] *= Math.exp(-dt * 3.5);
      const pr = 8 + puffs[j + 1] * 40, a = puffs[j + 2] * 0.35;
      ctx.fillStyle = withAlpha('#8d6a45', a);
      ctx.beginPath(); ctx.ellipse(SX(puffs[j]) - pr * 0.7, floorY - 3, pr * 0.5, pr * 0.18, 0, 0, Math.PI * 2); ctx.ellipse(SX(puffs[j]) + pr * 0.7, floorY - 3, pr * 0.5, pr * 0.18, 0, 0, Math.PI * 2); ctx.fill();
      moving = true;
    }
    // balls
    for (let i = 0; i < n; i++) {
      const R = r[i] * scale, cx = SX(x[i]), cy = SY(y[i]);
      const hgt = y[i] - r[i];
      softShadow(ctx, cx, floorY + 2, R * (1.2 - Math.min(0.6, hgt * 0.2)), R * 0.28, 0.3 * (1 - Math.min(0.8, hgt * 0.3)));
      const s = clamp(sq[i], -0.35, 0.3);
      ctx.save();
      ctx.translate(cx, cy - (s < 0 && hgt < 0.02 ? s * R : 0));
      ctx.scale(1 - s, 1 + s);
      sphere(ctx, 0, 0, R, col[i]);
      ctx.restore();
      if (i === tracked) { ctx.strokeStyle = withAlpha(T.blue, 0.6); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(cx, cy, R + 4, 0, Math.PI * 2); ctx.stroke(); }
    }
    if (tracked >= 0 && tracked < n) {
      const v = Math.hypot(vx[tracked], vy[tracked]);
      if (!k.small || v > 0.2) pill(ctx, `v = ${fmt(v, 1)} m/s`, SX(x[tracked]), SY(y[tracked]) - r[tracked] * scale - 16, { size: 10, color: T.ink2 });
    }
    if (!n) text(ctx, 'Tap anywhere to drop a ball', (left + SX(roomW)) / 2, floorY * 0.45, T.mute, k.small ? 14 : 17, 600, 'center');
    // graph
    if (plotOn) {
      const span = 6, t1 = Math.max(span, simT);
      plot.range(t1 - span, t1, 0, 3).frame(ctx);
      plot.clip(ctx); plot.ring(ctx, trace, T.orange, 2); plot.unclip(ctx);
    }
    st.h.set(nPeaks ? `${fmt(peaks[0], 2)} m` : '—');
    const lastP = nPeaks ? peaks[nPeaks - 1] : 0;
    const ee = tracked >= 0 ? e[tracked] : eSlider;
    st.next.set(nPeaks ? `${fmt(lastP * ee * ee, 2)} m` : '—');
    st.last.set(nPeaks > 1 ? `${fmt(lastP, 2)} m` : '—');
    st.ratio.set(nPeaks > 1 && peaks[nPeaks - 2] > 0.01 ? `${fmt(peaks[nPeaks - 1] / peaks[nPeaks - 2], 2)} (e² = ${fmt(ee * ee, 2)})` : `e² = ${fmt(ee * ee, 2)}`);
    badge.set(held >= 0 ? 'Let go to drop, or flick to throw' : n ? `g = ${g} m/s² · ${n} ball${n > 1 ? 's' : ''}` : 'Tap anywhere to drop a ball');
    k.animate(moving);
  });

  function sub2(p) { return '₀₁₂₃₄₅₆₇₈₉'[p] || String(p); }
  k.debug = { balls: () => n, ball: (i) => [SX(x[i]), SY(y[i])], peaks: () => Array.from(peaks.slice(0, nPeaks)) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
