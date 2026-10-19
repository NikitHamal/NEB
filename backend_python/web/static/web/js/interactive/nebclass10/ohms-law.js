/**
 * Ohm's law (NEB class 10) — the school practical: a 6 V battery, a plug key, a slide-wire
 * rheostat, an ammeter in series and a voltmeter across the resistor (or two resistors in series
 * or parallel, or a torch bulb). Slide the rheostat, read the analogue meters (their needles
 * settle like real ones), record readings and build the I–V graph: its slope is 1/R. The bulb's
 * filament heats up, so its graph bends — Ohm's law needs a steady temperature.
 */
import { createKit, T, Spring, fmt, clamp, background, grid, text, pill, knob, withAlpha, card } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const E = 6, RINT = 0.4, RH = 20;
const NETS = [
  { value: 'single', label: 'R₁ only' }, { value: 'series', label: 'R₁ + R₂ series' },
  { value: 'parallel', label: 'R₁ ∥ R₂ parallel' }, { value: 'bulb', label: 'Torch bulb' },
];

export default function init(stage) {
  const k = createKit(stage, { label: 'An Ohm\'s law circuit with a rheostat, ammeter and voltmeter, and an I–V graph' });
  const hud = createHud(stage);
  const badge = hud.badge('Insert the key, then slide the rheostat', T.blue);

  let net = 'single', R1 = 10, R2 = 15, keyIn = false, slide = 0.9;
  let I = 0, V = 0, Rnet = 10, aFull = 1, aLc = 0.02;
  const pts = [];
  const nA = new Spring(0, 70, 7), nV = new Spring(0, 70, 7);
  const plot = new Plot({ title: 'I–V graph (your readings)', xLabel: 'V / volt', yLabel: 'I / A', xMin: 0, xMax: 6, yMin: 0, yMax: 1 });

  const panel = createPanel(stage, { title: 'Ohm\'s law practical' });
  panel.chips({ label: 'What is being tested', options: NETS, value: 'single', onChange: (v) => { net = v; pts.length = 0; renderTable(); solve(); } });
  panel.chips({ label: 'R₁', options: [5, 10, 15, 20].map((r) => ({ value: String(r), label: `${r} Ω` })), value: '10', onChange: (v) => { R1 = +v; pts.length = 0; renderTable(); solve(); } });
  panel.chips({ label: 'R₂', options: [5, 10, 15, 20].map((r) => ({ value: String(r), label: `${r} Ω` })), value: '15', onChange: (v) => { R2 = +v; pts.length = 0; renderTable(); solve(); } });
  panel.buttonRow([{ label: 'Record', icon: 'add_chart', onClick: record }, { label: 'Clear', icon: 'restart_alt', variant: 'ghost', onClick: () => { pts.length = 0; renderTable(); k.invalidate(); } }]);
  const st = panel.stats([{ key: 'R', label: 'Expected R' }, { key: 'slope', label: 'Slope of I–V' }, { key: 'fit', label: 'R = 1/slope' }, { key: 'n', label: 'Readings' }]);
  const table = document.createElement('div'); table.className = 'k2-table'; panel.body.appendChild(table);
  panel.info('Read each meter to its least count (ammeter 0.02 A on the 1 A scale, voltmeter 0.1 V). Take five or six readings spread across the range; the best straight line through the origin has slope 1/R.');

  function netR(i) {
    if (net === 'single') return R1;
    if (net === 'series') return R1 + R2;
    if (net === 'parallel') return R1 * R2 / (R1 + R2);
    const P = i * i * 6;
    return 4 * (1 + 2.2 * Math.sqrt(P));
  }
  function solve() {
    const Rr = RH * slide;
    aFull = E / (RINT + netR(net === 'bulb' ? 0.4 : 0)) > 1 ? 3 : 1; aLc = aFull === 1 ? 0.02 : 0.05;
    plot.range(0, 6, 0, aFull);
    if (!keyIn) { I = 0; V = 0; Rnet = netR(0); }
    else {
      I = E / (Rr + netR(0) + RINT);
      for (let it = 0; it < 30; it++) I = 0.5 * I + 0.5 * E / (Rr + netR(I) + RINT);
      Rnet = netR(I); V = I * Rnet;
    }
    k.animate(true);
  }
  function settled() { return Math.abs(nA.x - nA.target) < aLc * 0.3 && Math.abs(nV.x - nV.target) < 0.03 && Math.abs(nA.v) < 0.05 && Math.abs(nV.v) < 0.2; }
  function readA() { return Math.round(nA.x / aLc) * aLc; }
  function readV() { return Math.round(nV.x / 0.1) * 0.1; }
  function record() {
    if (!keyIn) { badge.set('Insert the key first: no current flows'); return; }
    if (!settled()) { badge.set('Wait for the needles to settle'); return; }
    const a = readA(), vv = readV();
    if (pts.some((p) => Math.abs(p.v - vv) < 0.05)) { badge.set('You already have that reading: move the rheostat'); return; }
    pts.push({ v: vv, i: a }); pts.sort((p, q) => p.v - q.v); renderTable(); k.invalidate();
  }
  function renderTable() {
    table.innerHTML = pts.length ? '<div class="k2-tr k2-th"><span>V / volt</span><span>I / A</span><span>V/I / Ω</span></div>' + pts.map((p) => `<div class="k2-tr"><span>${fmt(p.v, 1)}</span><span>${fmt(p.i, 2)}</span><span>${p.i > 0 ? fmt(p.v / p.i, 1) : '—'}</span></div>`).join('') : '';
  }
  function fitSlope() { let sxy = 0, sxx = 0; for (const p of pts) { sxy += p.v * p.i; sxx += p.v * p.v; } return sxx > 0 ? sxy / sxx : 0; }

  let cx0 = 0, cy0 = 0, cw = 0, ch = 0;
  k.onResize((w, h) => {
    if (k.small) { cx0 = 16; cy0 = 44; cw = w - 32; ch = h * 0.52; plot.box(10, cy0 + ch + 8, w - 20, h - cy0 - ch - 14); }
    else { cx0 = 24; cy0 = 50; cw = w * 0.56; ch = h - 90; plot.box(cx0 + cw + 24, 50, w - cx0 - cw - 40, Math.min(h - 70, 420)); }
  });
  const rhX = (s) => cx0 + cw * 0.3 + s * cw * 0.42;
  const keyPos = () => [cx0 + cw * 0.12, cy0 + ch * 0.15];
  const keyH = k.drag({ hit: (x, y, s) => { const p = keyPos(); return Math.abs(x - p[0]) < 26 + s && Math.abs(y - p[1]) < 20 + s ? 1 : false; }, up: () => { keyIn = !keyIn; solve(); }, cursor: 'pointer', cursorActive: 'pointer' });
  const rhH = k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - rhX(slide), y - (cy0 + ch * 0.15 - 20)); return d < 16 + s ? d : false; },
    move: (x) => { slide = clamp((x - cx0 - cw * 0.3) / (cw * 0.42), 0, 1); solve(); },
    cursor: 'ew-resize',
  });

  k.frame((ctx, dt, w, h) => {
    nA.to(I); nV.to(V); nA.step(dt); nV.step(dt);
    background(k, ctx, w, h);
    grid(ctx, 0, 0, w, h, 24, T.grid);
    const top = cy0 + ch * 0.15, bot = cy0 + ch * 0.86, L = cx0 + cw * 0.04, R = cx0 + cw * 0.96;
    // wires
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(L, top); ctx.lineTo(R, top); ctx.lineTo(R, bot); ctx.lineTo(L, bot); ctx.closePath(); ctx.stroke();
    // battery on the left
    const by = (top + bot) / 2;
    ctx.fillStyle = '#f8fafc'; ctx.fillRect(L - 18, by - 34, 36, 68);
    for (let i = 0; i < 4; i++) { const yy = by - 30 + i * 16; ctx.fillStyle = '#334155'; ctx.fillRect(L - 16, yy, 32, 3); ctx.fillRect(L - 9, yy + 7, 18, 5); }
    text(ctx, '6 V', L + 24, by + 4, T.red, 11, 700);
    // key
    const kp = keyPos();
    ctx.fillStyle = '#1f2937'; ctx.beginPath(); ctx.roundRect(kp[0] - 24, kp[1] - 9, 48, 18, 4); ctx.fill();
    ctx.fillStyle = '#d4a017'; ctx.fillRect(kp[0] - 20, kp[1] - 5, 14, 10); ctx.fillRect(kp[0] + 6, kp[1] - 5, 14, 10);
    if (keyIn) { ctx.fillStyle = '#b08d57'; ctx.beginPath(); ctx.arc(kp[0], kp[1] - 4, 7, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#7c5a32'; ctx.fillRect(kp[0] - 3, kp[1] - 16, 6, 12); }
    else if (k.isHot(keyH)) { ctx.strokeStyle = T.blue; ctx.lineWidth = 2; ctx.strokeRect(kp[0] - 27, kp[1] - 12, 54, 24); }
    pill(ctx, keyIn ? 'key in' : 'tap to insert key', kp[0], kp[1] + 24, { size: 10, color: keyIn ? T.green : T.blue });
    // rheostat
    const rx0 = rhX(0), rx1 = rhX(1);
    ctx.fillStyle = '#e2e8f0'; ctx.beginPath(); ctx.roundRect(rx0 - 10, top - 10, rx1 - rx0 + 20, 20, 8); ctx.fill();
    ctx.strokeStyle = '#a16207'; ctx.lineWidth = 1;
    ctx.beginPath(); for (let x = rx0; x <= rx1; x += 4) { ctx.moveTo(x, top - 8); ctx.lineTo(x + 2, top + 8); } ctx.stroke();
    ctx.strokeStyle = '#64748b'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(rx0, top - 24); ctx.lineTo(rx1, top - 24); ctx.stroke();
    const jx = rhX(slide);
    ctx.fillStyle = '#334155'; ctx.fillRect(jx - 7, top - 30, 14, 22);
    knob(ctx, jx, top - 20, 8, T.blue, k.isHot(rhH) || k.active === rhH ? 1 : 0);
    text(ctx, `rheostat ${fmt(RH * slide, 1)} Ω`, (rx0 + rx1) / 2, top - 40, T.ink2, 10.5, 600, 'center');
    // network on the right side
    const nx = R, ny = (top + bot) / 2;
    drawNet(ctx, nx, ny);
    // ammeter in the bottom wire, voltmeter across the network
    dial(ctx, cx0 + cw * 0.45, bot, k.small ? 38 : 58, 'A', nA.x, aFull, aLc, T.blue);
    const vx = R - cw * 0.2;
    ctx.setLineDash([5, 4]); ctx.strokeStyle = withAlpha(T.purple, 0.7); ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(R, ny - 62); ctx.lineTo(vx, ny - 62); ctx.lineTo(vx, ny - 40); ctx.moveTo(vx, ny + 40); ctx.lineTo(vx, ny + 62); ctx.lineTo(R, ny + 62); ctx.stroke(); ctx.setLineDash([]);
    dial(ctx, vx, ny, k.small ? 34 : 52, 'V', nV.x, 6, 0.1, T.purple);
    // graph
    plot.frame(ctx);
    plot.clip(ctx);
    const slope = fitSlope();
    if (pts.length >= 2) { ctx.strokeStyle = withAlpha(T.blue, 0.6); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(plot.X(0), plot.Y(0)); ctx.lineTo(plot.X(6), plot.Y(6 * slope)); ctx.stroke(); }
    plot.unclip(ctx);
    for (const p of pts) plot.dot(ctx, p.v, p.i, T.orange, 4.5);
    if (keyIn) { ctx.globalAlpha = 0.5; plot.dot(ctx, readV(), readA(), T.slate, 3.5); ctx.globalAlpha = 1; }
    const Rexp = net === 'bulb' ? Rnet : netR(0);
    st.R.set(net === 'bulb' ? `${fmt(Rnet, 1)} Ω (now)` : `${fmt(Rexp, 2)} Ω`);
    st.slope.set(pts.length >= 2 ? `${fmt(slope, 3)} A/V` : '—');
    st.fit.set(pts.length >= 2 && slope > 0 ? `${fmt(1 / slope, 2)} Ω` : '—');
    st.n.set(String(pts.length));
    if (!(badge.el.textContent.startsWith('Wait') && !settled())) badge.set(!keyIn ? 'Insert the key, then slide the rheostat' : `Read: I = ${fmt(readA(), 2)} A, V = ${fmt(readV(), 1)} V — then record`);
    k.animate(nA.moving || nV.moving);
  });

  function drawNet(ctx, x, y) {
    const res = (cx, cy, label) => { ctx.fillStyle = '#e7d3ad'; ctx.strokeStyle = '#a8855a'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.roundRect(cx - 9, cy - 24, 18, 48, 7); ctx.fill(); ctx.stroke(); ctx.fillStyle = '#7c4a1e'; ctx.fillRect(cx - 9, cy - 12, 18, 3); ctx.fillRect(cx - 9, cy - 4, 18, 3); text(ctx, label, cx + 14, cy + 4, T.ink, 10.5, 700); };
    ctx.fillStyle = '#f8fafc'; ctx.fillRect(x - 6, y - 50, 12, 100);
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 3;
    if (net === 'single') { ctx.beginPath(); ctx.moveTo(x, y - 50); ctx.lineTo(x, y + 50); ctx.stroke(); res(x, y, `${R1} Ω`); }
    else if (net === 'series') { ctx.beginPath(); ctx.moveTo(x, y - 60); ctx.lineTo(x, y + 60); ctx.stroke(); res(x, y - 28, `R₁ ${R1} Ω`); res(x, y + 28, `R₂ ${R2} Ω`); }
    else if (net === 'parallel') {
      ctx.beginPath(); ctx.moveTo(x, y - 50); ctx.lineTo(x - 16, y - 50); ctx.lineTo(x - 16, y + 50); ctx.lineTo(x, y + 50); ctx.moveTo(x, y - 50); ctx.lineTo(x + 16, y - 50); ctx.lineTo(x + 16, y + 50); ctx.lineTo(x, y + 50); ctx.stroke();
      ctx.fillStyle = '#f8fafc'; ctx.fillRect(x - 3, y - 48, 6, 96);
      res(x - 16, y, ''); res(x + 16, y, ''); text(ctx, `${R1} Ω ∥ ${R2} Ω`, x - 30, y - 60, T.ink, 10.5, 700, 'right');
    } else {
      ctx.beginPath(); ctx.moveTo(x, y - 50); ctx.lineTo(x, y + 50); ctx.stroke();
      const P = I * V, glow = clamp(P / 2.2, 0, 1);
      if (glow > 0.02) { ctx.fillStyle = withAlpha('#fde047', 0.35 * glow); ctx.beginPath(); ctx.arc(x, y - 6, 22 + 16 * glow, 0, Math.PI * 2); ctx.fill(); }
      ctx.beginPath(); ctx.arc(x, y - 6, 16, 0, Math.PI * 2); ctx.fillStyle = withAlpha('#fef9c3', 0.6 + 0.4 * glow); ctx.fill(); ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.strokeStyle = glow > 0.1 ? '#f59e0b' : '#78716c'; ctx.beginPath(); ctx.moveTo(x - 6, y); ctx.lineTo(x - 4, y - 10); ctx.lineTo(x, y - 6); ctx.lineTo(x + 4, y - 10); ctx.lineTo(x + 6, y); ctx.stroke();
      ctx.fillStyle = '#9ca3af'; ctx.fillRect(x - 8, y + 9, 16, 10);
      text(ctx, 'bulb', x + 22, y + 4, T.ink, 10.5, 700);
    }
  }
  function dial(ctx, x, y, r, sym, val, full, lc, color) {
    ctx.beginPath(); ctx.arc(x, y + 3, r, 0, Math.PI * 2); ctx.fillStyle = 'rgba(23,40,80,0.12)'; ctx.fill();
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fillStyle = '#fffdf6'; ctx.fill(); ctx.strokeStyle = '#334155'; ctx.lineWidth = 2.5; ctx.stroke();
    const a0 = Math.PI * 1.15, a1 = Math.PI * 1.85, rr = r * 0.8;
    ctx.strokeStyle = '#334155'; ctx.lineWidth = 1; ctx.beginPath();
    const n = Math.round(full / lc) > 80 ? Math.round(full / lc / 2) : Math.round(full / lc);
    for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * i / n, l = i % 5 === 0 ? 7 : 3.5; ctx.moveTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); ctx.lineTo(x + Math.cos(a) * (rr - l), y + Math.sin(a) * (rr - l)); }
    ctx.stroke();
    const labels = r < 45 ? (full === 6 ? 3 : full === 3 ? 3 : 2) : full === 1 ? 5 : full === 3 ? 3 : 6;
    for (let i = 0; i <= labels; i++) { const a = a0 + (a1 - a0) * i / labels; text(ctx, full === 1 ? fmt(i / labels, 1) : String(i * full / labels), x + Math.cos(a) * (rr - 15), y + Math.sin(a) * (rr - 15) + 3, T.ink2, r > 45 ? 9.5 : 8, 600, 'center'); }
    text(ctx, sym, x, y + r * 0.42, color, r > 40 ? 15 : 12, 800, 'center');
    const a = a0 + (a1 - a0) * clamp(val / full, -0.02, 1.04);
    ctx.strokeStyle = T.red; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(x, y + r * 0.1); ctx.lineTo(x + Math.cos(a) * rr * 0.95, y + Math.sin(a) * rr * 0.95); ctx.stroke();
    ctx.beginPath(); ctx.arc(x, y + r * 0.1, 3, 0, Math.PI * 2); ctx.fillStyle = '#334155'; ctx.fill();
  }

  solve();
  k.debug = { key: () => keyPos(), jockey: () => [rhX(slide), cy0 + ch * 0.15 - 20], record, pts: () => pts, IV: () => [I, V] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
