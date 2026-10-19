/**
 * Circuit builder — a battery, a switch and two resistors that can be wired in series or in
 * parallel. Ohm's law sets every current (I = V/R, series R₁ + R₂, parallel R₁R₂/(R₁ + R₂)),
 * and the charge carriers flow round each branch at a speed proportional to its current, so the
 * split in a parallel circuit is visible. Tap the switch, drag a resistor up or down to change it
 * (its colour bands follow), and drag the battery to add or remove cells.
 */
import { createKit, T, Spring, fmt, clamp, background, grid, text, pill, withAlpha, mix } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const VALUES = [1, 2.2, 3.3, 4.7, 6.8, 10, 15, 22, 33, 47, 68, 100];
const BAND = ['#111827', '#7c4a1e', '#dc2626', '#f97316', '#facc15', '#16a34a', '#2563eb', '#7c3aed', '#6b7280', '#f8fafc'];
const CELL = 1.5;
const MAXDOTS = 200;

function bands(R) {
  let exp = 0, v = R;
  while (v >= 100) { v /= 10; exp++; }
  while (v < 10) { v *= 10; exp--; }
  const d = Math.round(v);
  return [Math.floor(d / 10), d % 10, exp];
}

export default function init(stage) {
  const k = createKit(stage, { label: 'A circuit with a battery, switch, ammeter, voltmeter and two resistors' });
  const hud = createHud(stage);
  const badge = hud.badge('Tap the switch to close the circuit', T.blue);

  let cells = 4, R1i = 5, R2i = 7, parallel = false, closed = false, electrons = false;
  let I = 0, I1 = 0, I2 = 0, V1 = 0, V2 = 0, Rt = 0;
  const flow = new Spring(0, 30, 10);
  const sw = new Spring(0, 220, 18);
  const off = new Float64Array(3);
  const needle = [new Spring(0, 90, 12), new Spring(0, 90, 12)];
  const paths = [new Float32Array(32), new Float32Array(32), new Float32Array(32)];
  const plen = new Float32Array(3), pn = new Uint8Array(3);
  let L = 0, R = 0, Tp = 0, B = 0, xa = 0, battX = 0, battY = 0;

  const panel = createPanel(stage, { title: 'Circuit' });
  const vS = panel.slider({ label: 'Battery', min: 1, max: 8, step: 1, value: cells, format: (v) => `${v} cell${v > 1 ? 's' : ''} · ${fmt(v * CELL, 1)} V`, onChange: (v) => { cells = v; solve(); } });
  const r1S = panel.slider({ label: 'R₁', min: 0, max: VALUES.length - 1, step: 1, value: R1i, format: (v) => `${VALUES[v]} Ω`, onChange: (v) => { R1i = v; solve(); } });
  const r2S = panel.slider({ label: 'R₂', min: 0, max: VALUES.length - 1, step: 1, value: R2i, format: (v) => `${VALUES[v]} Ω`, onChange: (v) => { R2i = v; solve(); } });
  const topo = panel.chips({ label: 'Wiring', options: [{ value: 's', label: 'Series' }, { value: 'p', label: 'Parallel' }], value: 's', onChange: (v) => { parallel = v === 'p'; buildPaths(); solve(); } });
  panel.toggle({ label: 'Show electrons (they flow from −)', value: false, onChange: (v) => { electrons = v; k.invalidate(); } });
  const st = panel.stats([{ key: 'R', label: 'Total resistance' }, { key: 'I', label: 'Current from battery' }, { key: 'b1', label: 'R₁: V, I' }, { key: 'b2', label: 'R₂: V, I' }]);
  panel.info('Series: the same current passes through both and the voltage is shared. Parallel: each resistor gets the full battery voltage and the current splits, more through the smaller resistor.');

  function solve() {
    const V = cells * CELL, r1 = VALUES[R1i], r2 = VALUES[R2i];
    Rt = parallel ? r1 * r2 / (r1 + r2) : r1 + r2;
    if (!closed) { I = I1 = I2 = V1 = V2 = 0; }
    else if (parallel) { I1 = V / r1; I2 = V / r2; I = I1 + I2; V1 = V2 = V; }
    else { I = V / Rt; I1 = I2 = I; V1 = I * r1; V2 = I * r2; }
    k.animate(true);
  }

  function setPath(i, pts) {
    const a = paths[i]; pn[i] = pts.length / 2; let len = 0;
    for (let j = 0; j < pts.length; j++) a[j] = pts[j];
    for (let j = 1; j < pn[i]; j++) len += Math.hypot(a[j * 2] - a[j * 2 - 2], a[j * 2 + 1] - a[j * 2 - 1]);
    plen[i] = len;
  }
  function buildPaths() {
    if (!parallel) {
      setPath(0, [L, B, L, Tp, R, Tp, R, B, L, B]); pn[1] = pn[2] = 0;
    } else {
      setPath(0, [xa, B, L, B, L, Tp, xa, Tp]);
      setPath(1, [xa, Tp, xa, B]);
      setPath(2, [xa, Tp, R, Tp, R, B, xa, B]);
    }
    k.invalidate();
  }
  k.onResize((w, h) => {
    L = k.small ? 44 : w * 0.16; R = k.small ? w - 40 : w * 0.8; Tp = k.small ? 70 : h * 0.2; B = k.small ? h - 60 : h * 0.78;
    xa = L + (R - L) * 0.6; battX = L; battY = (Tp + B) / 2;
    buildPaths();
  });
  const r1Pos = (o) => { if (parallel) { o.x = xa; o.y = (Tp + B) / 2; o.v = true; } else { o.x = L + (R - L) * 0.68; o.y = Tp; o.v = false; } return o; };
  const r2Pos = (o) => { o.x = R; o.y = (Tp + B) / 2; o.v = true; return o; };
  const swPos = () => [L + (R - L) * (parallel ? 0.3 : 0.5), B];
  const amPos = () => [L + (R - L) * 0.3, Tp];
  const P1 = { x: 0, y: 0, v: false }, P2 = { x: 0, y: 0, v: true };

  const swH = k.drag({ hit: (x, y, s) => { const p = swPos(); return Math.abs(x - p[0]) < 30 + s && Math.abs(y - p[1]) < 22 + s ? 1 : false; }, up: () => { closed = !closed; solve(); }, cursor: 'pointer', cursorActive: 'pointer' });
  function resHandle(pos, getI, setI, slider) {
    let y0 = 0, i0 = 0;
    return k.drag({
      hit: (x, y, s) => { pos(P1); const hw = P1.v ? 16 : 40, hh = P1.v ? 40 : 16; return Math.abs(x - P1.x) < hw + s && Math.abs(y - P1.y) < hh + s ? 1 : false; },
      down: (x, y) => { y0 = y; i0 = getI(); },
      move: (x, y) => { const ni = clamp(i0 + Math.round((y0 - y) / 18), 0, VALUES.length - 1); if (ni !== getI()) { setI(ni); slider.set(ni); solve(); } },
      cursor: 'ns-resize',
    });
  }
  const r1H = resHandle(r1Pos, () => R1i, (v) => { R1i = v; }, r1S);
  const r2H = resHandle(r2Pos, () => R2i, (v) => { R2i = v; }, r2S);
  let by0 = 0, c0 = 0;
  const batH = k.drag({
    hit: (x, y, s) => (Math.abs(x - battX) < 26 + s && Math.abs(y - battY) < 50 + s ? 1 : false),
    down: (x, y) => { by0 = y; c0 = cells; },
    move: (x, y) => { const c = clamp(c0 + Math.round((by0 - y) / 16), 1, 8); if (c !== cells) { cells = c; vS.set(c); solve(); } },
    cursor: 'ns-resize',
  });

  function pointOn(i, d, out) {
    const a = paths[i];
    for (let j = 1; j < pn[i]; j++) {
      const x0 = a[j * 2 - 2], y0 = a[j * 2 - 1], x1 = a[j * 2], y1 = a[j * 2 + 1];
      const sl = Math.hypot(x1 - x0, y1 - y0);
      if (d <= sl) { out.x = x0 + (x1 - x0) * d / sl; out.y = y0 + (y1 - y0) * d / sl; return out; }
      d -= sl;
    }
    out.x = a[(pn[i] - 1) * 2]; out.y = a[(pn[i] - 1) * 2 + 1];
    return out;
  }
  const Q = { x: 0, y: 0 };

  k.frame((ctx, dt, w, h) => {
    flow.to(closed ? 1 : 0); flow.step(dt); sw.to(closed ? 1 : 0); sw.step(dt);
    for (let i = 0; i < 3; i++) off[i] = (off[i] + (i === 0 ? I : !parallel ? 0 : i === 1 ? I1 : I2) * flow.x * 46 * dt * (electrons ? -1 : 1) + 1e6) % 24;
    needle[0].to(I); needle[1].to(V1); needle[0].step(dt); needle[1].step(dt);
    background(k, ctx, w, h);
    grid(ctx, 0, 0, w, h, 24, T.grid);
    // wires
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 5; ctx.lineJoin = 'round';
    for (let i = 0; i < 3; i++) { if (!pn[i]) continue; ctx.beginPath(); for (let j = 0; j < pn[i]; j++) { const x = paths[i][j * 2], y = paths[i][j * 2 + 1]; if (j) ctx.lineTo(x, y); else ctx.moveTo(x, y); } ctx.stroke(); }
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.2;
    for (let i = 0; i < 3; i++) { if (!pn[i]) continue; ctx.beginPath(); for (let j = 0; j < pn[i]; j++) { const x = paths[i][j * 2], y = paths[i][j * 2 + 1] - 1; if (j) ctx.lineTo(x, y); else ctx.moveTo(x, y); } ctx.stroke(); }
    if (parallel) { for (const yy of [Tp, B]) { ctx.beginPath(); ctx.arc(xa, yy, 5, 0, Math.PI * 2); ctx.fillStyle = '#334155'; ctx.fill(); } }
    // charges
    if (flow.x > 0.02) {
      ctx.fillStyle = electrons ? withAlpha('#38bdf8', flow.x) : withAlpha('#fde047', flow.x);
      for (let i = 0; i < 3; i++) {
        if (!pn[i]) continue;
        const n = Math.min(MAXDOTS, Math.floor(plen[i] / 24));
        for (let d = 0; d < n; d++) { pointOn(i, (d * 24 + off[i]) % plen[i], Q); ctx.beginPath(); ctx.arc(Q.x, Q.y, 3.4, 0, Math.PI * 2); ctx.fill(); }
      }
    }
    // battery
    drawBattery(ctx, battX, battY);
    // switch
    const sp = swPos();
    ctx.fillStyle = '#f8fafc'; ctx.fillRect(sp[0] - 26, sp[1] - 8, 52, 16);
    ctx.beginPath(); ctx.arc(sp[0] - 20, sp[1], 4.5, 0, Math.PI * 2); ctx.arc(sp[0] + 20, sp[1], 4.5, 0, Math.PI * 2); ctx.fillStyle = '#334155'; ctx.fill();
    const ang = -0.6 * (1 - sw.x);
    ctx.strokeStyle = k.isHot(swH) ? T.blue : '#334155'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(sp[0] - 20, sp[1]); ctx.lineTo(sp[0] - 20 + Math.cos(ang) * 42, sp[1] + Math.sin(ang) * 42); ctx.stroke();
    pill(ctx, closed ? 'switch closed' : 'tap to close', sp[0], sp[1] + 26, { size: 10, color: closed ? T.green : T.blue });
    // resistors
    drawResistor(ctx, r1Pos(P1), VALUES[R1i], 'R₁', I1, k.isHot(r1H));
    drawResistor(ctx, r2Pos(P2), VALUES[R2i], 'R₂', I2, k.isHot(r2H));
    // ammeter
    const am = amPos();
    meter(ctx, am[0], am[1], 'A', `${fmt(I, 2)} A`, T.blue);
    if (parallel) { meterSmall(ctx, xa + 30, B - 34, `${fmt(I1, 2)} A`); meterSmall(ctx, R - 30, B - 34, `${fmt(I2, 2)} A`); }
    // voltmeter across R1
    r1Pos(P1);
    const vx = P1.v ? P1.x - 70 : P1.x, vy = P1.v ? P1.y : P1.y + 70;
    ctx.setLineDash([5, 4]); ctx.strokeStyle = withAlpha(T.purple, 0.7); ctx.lineWidth = 1.5; ctx.beginPath();
    if (P1.v) { ctx.moveTo(P1.x, P1.y - 50); ctx.lineTo(vx, P1.y - 50); ctx.lineTo(vx, vy - 20); ctx.moveTo(vx, vy + 20); ctx.lineTo(vx, P1.y + 50); ctx.lineTo(P1.x, P1.y + 50); }
    else { ctx.moveTo(P1.x - 50, P1.y); ctx.lineTo(P1.x - 50, vy); ctx.lineTo(vx - 20, vy); ctx.moveTo(vx + 20, vy); ctx.lineTo(P1.x + 50, vy); ctx.lineTo(P1.x + 50, P1.y); }
    ctx.stroke(); ctx.setLineDash([]);
    meter(ctx, vx, vy, 'V', `${fmt(V1, 2)} V`, T.purple);
    if (!k.small) text(ctx, `V = IR → ${fmt(V1, 2)} V = ${fmt(I1, 3)} A × ${VALUES[R1i]} Ω`, 16, h - 16, T.ink2, 11.5, 600);
    st.R.set(`${fmt(Rt, 2)} Ω`); st.I.set(`${fmt(I, 3)} A`);
    st.b1.set(`${fmt(V1, 2)} V, ${fmt(I1, 3)} A`); st.b2.set(`${fmt(V2, 2)} V, ${fmt(I2, 3)} A`);
    badge.set(!closed ? 'Tap the switch to close the circuit' : parallel ? `Current splits: ${fmt(I1, 2)} A + ${fmt(I2, 2)} A = ${fmt(I, 2)} A` : `Same current everywhere: ${fmt(I, 2)} A`);
    k.animate(closed || flow.moving || sw.moving || needle[0].moving);
  });

  function drawBattery(ctx, x, y) {
    const n = cells, gap = 9, hgt = n * gap * 2;
    ctx.fillStyle = withAlpha('#f8fafc', 1); ctx.fillRect(x - 24, y - hgt / 2 - 6, 48, hgt + 12);
    for (let i = 0; i < n; i++) {
      const cy = y - hgt / 2 + i * gap * 2 + 4;
      ctx.fillStyle = '#334155'; ctx.fillRect(x - 18, cy, 36, 3); ctx.fillRect(x - 10, cy + gap, 20, 5);
    }
    text(ctx, '+', x + 26, y - hgt / 2 + 6, T.red, 14, 800);
    text(ctx, '−', x + 26, y + hgt / 2 + 2, T.ink, 14, 800);
    pill(ctx, `${fmt(cells * CELL, 1)} V`, x - (k.small ? 0 : 52), y + (k.small ? hgt / 2 + 24 : 0), { color: T.red, size: 11 });
    if (k.isHot(batH)) text(ctx, 'drag ↕ for cells', x, y - hgt / 2 - 14, T.blue, 10, 600, 'center');
  }
  function drawResistor(ctx, p, Rv, label, Ib, hot) {
    const pw = Ib * Ib * Rv;
    const glow = clamp(pw / 6, 0, 1) * flow.x;
    ctx.save(); ctx.translate(p.x, p.y); if (p.v) ctx.rotate(Math.PI / 2);
    if (glow > 0.03) { ctx.fillStyle = withAlpha('#f97316', 0.22 * glow); ctx.beginPath(); ctx.roundRect(-46, -20, 92, 40, 20); ctx.fill(); }
    if (hot) { ctx.fillStyle = withAlpha(T.blue, 0.12); ctx.beginPath(); ctx.roundRect(-44, -18, 88, 36, 12); ctx.fill(); }
    ctx.fillStyle = mix('#e7d3ad', '#f97316', glow * 0.5); ctx.strokeStyle = '#a8855a'; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.roundRect(-34, -11, 68, 22, 9); ctx.fill(); ctx.stroke();
    const b = bands(Rv);
    const cols = [BAND[b[0]], BAND[b[1]], b[2] < 0 ? '#d4a017' : BAND[b[2]], '#d4a017'];
    const xs = [-20, -10, 0, 18];
    for (let i = 0; i < 4; i++) { ctx.fillStyle = cols[i]; ctx.fillRect(xs[i] - 2.5, -11, 5, 22); }
    ctx.restore();
    const flipL = p.v && p.x > k.w - 90;
    const lx = p.v ? (flipL ? p.x - 62 : p.x + 62) : p.x, ly = p.v ? p.y : p.y - 30;
    pill(ctx, `${label} = ${Rv} Ω`, lx, ly, { size: 10.5, color: T.ink });
    if (hot) text(ctx, 'drag ↕', lx, ly + 20, T.blue, 10, 600, 'center');
  }
  function meter(ctx, x, y, sym, val, color) {
    ctx.beginPath(); ctx.arc(x, y + 2, 20, 0, Math.PI * 2); ctx.fillStyle = 'rgba(23,40,80,0.12)'; ctx.fill();
    ctx.beginPath(); ctx.arc(x, y, 20, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = color; ctx.lineWidth = 2.5; ctx.stroke();
    text(ctx, sym, x, y + 1, color, 15, 800, 'center', 'middle');
    pill(ctx, val, x, y - 34, { color, size: 11, bg: '#fff' });
  }
  function meterSmall(ctx, x, y, val) { pill(ctx, val, x, y, { size: 10, color: T.blue }); }

  k.debug = { sw: () => swPos(), r1: () => { r1Pos(P1); return [P1.x, P1.y]; }, state: () => ({ I, I1, I2, V1, Rt, closed, R1: VALUES[R1i] }), parallel: () => { topo.set('p'); parallel = true; buildPaths(); solve(); } };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
