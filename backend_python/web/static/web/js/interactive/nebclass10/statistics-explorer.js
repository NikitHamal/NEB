/**
 * Statistics explorer (NEB class 10) — every value is a dot on a number line that you can drag;
 * tap the line to add a value, drag a dot into the bin to remove it. The number line sits on a
 * see-saw whose pivot is the mean (the balance point of the data), with the median and the
 * mode marked, and a histogram with the class width you choose highlights the modal class.
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, withAlpha, card, sphere } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SETS = {
  marks: { name: 'Marks of 12 students (out of 100)', unit: 'marks', lo: 0, hi: 100, step: 1, cw: 10, data: [45, 62, 71, 58, 62, 80, 39, 62, 74, 55, 68, 50] },
  rain: { name: 'Monthly rainfall in Kathmandu (mm)', unit: 'mm', lo: 0, hi: 400, step: 1, cw: 50, data: [12, 18, 34, 61, 148, 284, 342, 296, 187, 62, 9, 6] },
  heights: { name: 'Heights of 15 students (cm)', unit: 'cm', lo: 140, hi: 170, step: 1, cw: 5, data: [148, 152, 155, 151, 160, 149, 154, 158, 152, 150, 156, 153, 157, 151, 154] },
  family: { name: 'Family size in 20 homes', unit: 'people', lo: 0, hi: 12, step: 1, cw: 2, data: [4, 5, 6, 4, 4, 7, 3, 5, 4, 6, 8, 4, 5, 4, 6, 4, 5, 3, 4, 5] },
};

export default function init(stage) {
  const k = createKit(stage, { label: 'A dot plot on a balancing number line with a histogram below' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag a dot, tap the line to add one', T.blue);

  let set = SETS.marks, vals = set.data.slice(), cw = set.cw, held = -1;
  const pivot = new Spring(0, 90, 16), tilt = new Spring(0, 60, 9);
  let bars = [];

  const panel = createPanel(stage, { title: 'Statistics' });
  panel.chips({ label: 'Data', options: Object.keys(SETS).map((key) => ({ value: key, label: SETS[key].name.split(' (')[0] })), value: 'marks', onChange: (v) => { set = SETS[v]; vals = set.data.slice(); cw = set.cw; cwS.set(cw); rebuild(); } });
  const cwS = panel.slider({ label: 'Class width', min: 1, max: 100, step: 1, value: cw, format: (v) => `${v}`, onChange: (v) => { cw = v; rebuild(); } });
  panel.buttonRow([{ label: 'Add an outlier', icon: 'add', variant: 'ghost', onClick: () => { vals.push(set.lo + (set.hi - set.lo) * (Math.random() < 0.5 ? 0.02 : 0.98)); rebuild(); } }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: () => { vals = set.data.slice(); rebuild(); } }]);
  const st = panel.stats([{ key: 'mean', label: 'Mean x̄ = Σx/n' }, { key: 'median', label: 'Median' }, { key: 'mode', label: 'Mode' }, { key: 'range', label: 'Range' }]);
  const work = panel.readout({ label: 'Working', value: '' });
  panel.info('The mean is the balance point: drag one dot far out and watch the see-saw pivot slide after it, while the median hardly moves. That is why the median suits skewed data such as rainfall or incomes.');

  function stats() {
    const n = vals.length, s = vals.slice().sort((x, y) => x - y);
    const sum = vals.reduce((p, v) => p + v, 0), mean = n ? sum / n : 0;
    const med = n ? (n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2) : 0;
    const cnt = new Map(); let best = 0; for (const v of vals) { const r = Math.round(v); const c = (cnt.get(r) || 0) + 1; cnt.set(r, c); best = Math.max(best, c); }
    const modes = best > 1 ? [...cnt.entries()].filter((e) => e[1] === best).map((e) => e[0]).sort((x, y) => x - y) : [];
    return { n, sum, mean, med, modes, best, min: s[0], max: s[n - 1] };
  }
  function rebuild() {
    const c0 = Math.floor(set.lo / cw) * cw, nb = Math.ceil((set.hi - c0) / cw) || 1;
    const old = bars; bars = [];
    for (let i = 0; i < nb; i++) { const lo = c0 + i * cw, hi = lo + cw; const count = vals.filter((v) => v >= lo && (v < hi || (i === nb - 1 && v <= hi))).length; const sp = old[i] && old.length === nb ? old[i].h : new Spring(0, 120, 16); sp.to(count); bars.push({ lo, hi, h: sp, n: count }); }
    k.animate(true);
  }

  let mh = 120, x0 = 0, x1 = 0, lineY = 0, histY = 0, histH = 0, binX = 0, binY = 0;
  k.onResize((w, h) => { x0 = k.small ? 20 : 60; x1 = w - (k.small ? 20 : 60); lineY = h * (k.small ? 0.4 : 0.42); mh = k.small ? 64 : 120; histY = h - 30; histH = h * (k.small ? 0.36 : 0.34); binX = w - 40; binY = lineY + 70; });
  const X = (v) => x0 + (v - set.lo) / (set.hi - set.lo) * (x1 - x0);
  const V = (px) => clamp(Math.round((set.lo + (px - x0) / (x1 - x0) * (set.hi - set.lo)) / set.step) * set.step, set.lo, set.hi);
  const dotY = new Float32Array(200);
  function layoutDots() {
    const order = vals.map((v, i) => i).sort((p, q) => vals[p] - vals[q]);
    const r = 7, buckets = new Map();
    for (const i of order) { const key = Math.round(X(vals[i]) / (r * 1.6)); const c = buckets.get(key) || 0; buckets.set(key, c + 1); dotY[i] = c; }
  }
  k.drag({
    hit: (x, y, s) => { layoutDots(); for (let i = 0; i < vals.length; i++) { const d = Math.hypot(x - X(vals[i]), y - (lineY - 12 - dotY[i] * 14 + tiltAt(vals[i]))); if (d < 9 + s) return d; } return false; },
    down: (x, y) => { let best = -1, bd = 1e9; for (let i = 0; i < vals.length; i++) { const d = Math.hypot(x - X(vals[i]), y - (lineY - 12 - dotY[i] * 14 + tiltAt(vals[i]))); if (d < bd) { bd = d; best = i; } } held = best; },
    move: (x, y) => { if (held < 0) return; vals[held] = V(x); heldOut = y > lineY + 50; rebuild(); },
    up: () => { if (held >= 0 && heldOut && vals.length > 2) vals.splice(held, 1); held = -1; heldOut = false; rebuild(); },
  });
  let heldOut = false;
  k.onTap((x, y) => { if (Math.abs(y - lineY) < 40 && x >= x0 && x <= x1 && vals.length < 60) { vals.push(V(x)); rebuild(); } });
  function tiltAt(v) { return (X(v) - X(pivot.x)) * Math.sin(tilt.x); }

  k.frame((ctx, dt, w, h) => {
    const s = stats();
    pivot.to(s.mean); tilt.to(0);
    let anim = pivot.step(dt) | tilt.step(dt);
    for (const b of bars) anim |= b.h.step(dt);
    background(k, ctx, w, h);
    if (!k.small) text(ctx, set.name, 60, 60, T.ink, k.small ? 12 : 14, 700);
    // see-saw: the line rests on a pivot at the mean
    const px = X(pivot.x);
    ctx.fillStyle = T.purple; ctx.beginPath(); ctx.moveTo(px, lineY + 4); ctx.lineTo(px - 14, lineY + 30); ctx.lineTo(px + 14, lineY + 30); ctx.fill();
    ctx.fillStyle = '#cbd5e1'; ctx.fillRect(x0 - 10, lineY + 30, x1 - x0 + 20, 3);
    ctx.strokeStyle = T.ink2; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x0 - 6, lineY); ctx.lineTo(x1 + 6, lineY); ctx.stroke();
    const step = niceTick(set.hi - set.lo);
    for (let v = set.lo; v <= set.hi; v += step) { ctx.strokeStyle = T.ink2; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(X(v), lineY); ctx.lineTo(X(v), lineY + 6); ctx.stroke(); text(ctx, String(v), X(v), lineY + 18, T.mute, 9.5, 500, 'center'); }
    pill(ctx, `mean ${fmt(s.mean, 1)}`, px, lineY + 46, { bg: T.purple, color: '#fff', border: false, size: 10.5 });
    // median and mode markers
    const mx = X(s.med);
    ctx.strokeStyle = T.green; ctx.lineWidth = 2; ctx.setLineDash([4, 3]); ctx.beginPath(); ctx.moveTo(mx, lineY - mh); ctx.lineTo(mx, lineY); ctx.stroke(); ctx.setLineDash([]);
    pill(ctx, `median ${fmt(s.med, 1)}`, mx, lineY - mh - 10, { color: T.green, size: 10 });
    // range bracket
    ctx.strokeStyle = withAlpha(T.slate, 0.6); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(X(s.min), lineY - mh - 30); ctx.lineTo(X(s.min), lineY - mh - 24); ctx.lineTo(X(s.max), lineY - mh - 24); ctx.lineTo(X(s.max), lineY - mh - 30); ctx.stroke();
    text(ctx, `range ${fmt(s.max - s.min, 0)}`, (X(s.min) + X(s.max)) / 2, lineY - mh - 32, T.slate, 10, 600, 'center');
    // dots
    layoutDots();
    for (let i = 0; i < vals.length; i++) {
      const isMode = s.modes.indexOf(Math.round(vals[i])) >= 0;
      const y = lineY - 12 - dotY[i] * 14;
      sphere(ctx, X(vals[i]), held === i ? k.pointer.y : y, 7, held === i && heldOut ? T.red : isMode ? T.orange : T.blue);
    }
    if (s.modes.length) text(ctx, `mode ${s.modes.join(', ')}`, X(s.modes[0]), lineY - 24 - s.best * 14, T.orange, 10, 700, 'center');
    if (held >= 0) { pill(ctx, heldOut ? 'release to remove' : `${vals[held]} ${set.unit}`, k.pointer.x, k.pointer.y - 22, { color: heldOut ? T.red : T.ink, size: 10.5 }); }
    // histogram
    const maxN = Math.max(1, ...bars.map((b) => b.n));
    const bw = (x1 - x0) / Math.max(1, bars.length);
    ctx.strokeStyle = T.line; ctx.beginPath(); ctx.moveTo(x0, histY); ctx.lineTo(x1, histY); ctx.stroke();
    for (const b of bars) {
      const bx = X(b.lo), bwp = X(Math.min(b.hi, set.hi)) - bx, bh = b.h.x / maxN * (histH - 30);
      const modal = b.n === maxN && maxN > 0;
      ctx.fillStyle = modal ? withAlpha(T.orange, 0.75) : withAlpha(T.blue, 0.55); ctx.fillRect(bx + 1, histY - bh, Math.max(1, bwp - 2), bh);
      if (bwp > 22 && b.n) text(ctx, String(b.n), bx + bwp / 2, histY - bh - 4, T.ink2, 10, 700, 'center');
      if (bwp > 34 || bars.length < 8) text(ctx, `${b.lo}–${b.hi}`, bx + bwp / 2, histY + 13, T.mute, k.small ? 7.5 : 9, 500, 'center');
    }
    text(ctx, 'frequency', x0, histY - histH + 8, T.ink2, 10, 600);
    // the bin
    ctx.fillStyle = held >= 0 && heldOut ? withAlpha(T.red, 0.15) : 'rgba(23,32,51,0.05)'; ctx.beginPath(); ctx.roundRect(binX - 24, binY - 20, 48, 40, 8); ctx.fill();
    ctx.strokeStyle = held >= 0 && heldOut ? T.red : T.mute; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(binX - 9, binY - 7); ctx.lineTo(binX + 9, binY - 7); ctx.moveTo(binX - 7, binY - 7); ctx.lineTo(binX - 5, binY + 10); ctx.lineTo(binX + 5, binY + 10); ctx.lineTo(binX + 7, binY - 7); ctx.moveTo(binX - 3, binY - 10); ctx.lineTo(binX + 3, binY - 10); ctx.stroke();
    st.mean.set(`${fmt(s.mean, 2)}`); st.median.set(fmt(s.med, 1)); st.mode.set(s.modes.length ? s.modes.join(', ') : 'none');
    st.range.set(`${fmt(s.max - s.min, 0)} (${fmt(s.min, 0)}–${fmt(s.max, 0)})`);
    work.set(`Σx = ${fmt(s.sum, 0)}, n = ${s.n}, x̄ = ${fmt(s.sum, 0)}/${s.n} = ${fmt(s.mean, 2)}`);
    badge.set(Math.abs(s.mean - s.med) > (set.hi - set.lo) * 0.06 ? 'Mean and median are far apart: the data are skewed' : `n = ${s.n}: mean ${fmt(s.mean, 1)}, median ${fmt(s.med, 1)}`);
    k.animate(!!anim || held >= 0);
  });
  function niceTick(span) { return span <= 15 ? 1 : span <= 40 ? 5 : span <= 120 ? 10 : 50; }

  rebuild();
  k.debug = { dot: (i) => { layoutDots(); return [X(vals[i]), lineY - 12 - dotY[i] * 14]; }, line: (v) => [X(v), lineY], stats: () => { const s = stats(); return [s.n, s.mean, s.med]; } };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
