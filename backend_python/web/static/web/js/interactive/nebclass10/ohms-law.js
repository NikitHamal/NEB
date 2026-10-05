import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Ohm's law bench: vary the applied voltage, read the ammeter, build the V–I
// graph and get R from its slope. A second resistor can be switched in series
// or in parallel, and the equivalent resistance is computed live.

const ACCENT = '#F59E0B';
const BLUE = '#38bdf8';
const GREEN = '#34d399';
const ROSE = '#fb7185';

const RESISTORS = [2, 5, 10, 20, 30];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Raise V and watch the ammeter — the graph is a straight line', ACCENT);

  let V = 6;
  let R1 = 10;
  let R2 = 20;
  let mode = 'single';       // single | series | parallel
  const points = [];
  let fit = null;

  const panel = createPanel(stage, { title: 'Circuit controls' });
  panel.slider({
    label: 'Supply voltage V',
    min: 0, max: 24, step: 0.5, value: V, unit: ' V',
    onChange: (v) => { V = v; },
  });
  panel.select({
    label: 'Resistor R₁',
    options: RESISTORS.map((r) => ({ value: String(r), label: `${r} Ω` })),
    value: String(R1),
    onChange: (v) => { R1 = Number(v); reset(); },
  });
  panel.select({
    label: 'Connection',
    options: [
      { value: 'single', label: 'R₁ only' },
      { value: 'series', label: 'R₁ and R₂ in series' },
      { value: 'parallel', label: 'R₁ and R₂ in parallel' },
    ],
    value: 'single',
    onChange: (v) => { mode = v; reset(); },
  });
  const r2Slider = panel.slider({
    label: 'Resistor R₂',
    min: 2, max: 40, step: 1, value: R2, unit: ' Ω',
    onChange: (v) => { R2 = v; reset(); },
  });
  panel.buttonRow([
    { label: 'Record point', icon: 'add_chart', onClick: () => record() },
    { label: 'Clear graph', icon: 'restart_alt', variant: 'ghost', onClick: () => reset() },
  ]);
  const readR = panel.readout({ label: 'Equivalent resistance', value: '—' });
  const readI = panel.readout({ label: 'Current I', value: '—' });
  const readSlope = panel.readout({ label: 'Slope of V–I graph', value: '—' });
  panel.info('Ohm\'s law: V = IR. The V–I graph is a straight line through the origin and its slope is the resistance.');

  function equivalent() {
    if (mode === 'series') return R1 + R2;
    if (mode === 'parallel') return (R1 * R2) / (R1 + R2);
    return R1;
  }
  function current() { return V / equivalent(); }
  function reset() { points.length = 0; fit = null; }
  function record() {
    const I = current();
    if (!Number.isFinite(I)) return;
    if (!points.some((p) => Math.abs(p.x - V) < 0.26)) points.push({ x: V, y: I });
    points.sort((a, b) => a.x - b.x);
    const n = points.length;
    let sx = 0; let sy = 0; let sxx = 0; let sxy = 0;
    points.forEach((p) => { sx += p.x; sy += p.y; sxx += p.x * p.x; sxy += p.x * p.y; });
    const den = n * sxx - sx * sx;
    fit = Math.abs(den) < 1e-12 ? null : { m: (n * sxy - sx * sy) / den, b: (sy - (n * sxy - sx * sy) / den * sx) / n };
    badge.set(`Recorded V = ${V} V, I = ${I.toFixed(3)} A`);
  }

  function drawAmmeter(ctx, cx, cy, r, value, max) {
    ctx.fillStyle = 'rgba(8,16,30,0.85)';
    ctx.strokeStyle = 'rgba(158,193,255,0.35)';
    ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    const a0 = Math.PI * 0.78;
    const a1 = Math.PI * 2.22;
    ctx.strokeStyle = 'rgba(232,238,251,0.5)';
    ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.arc(cx, cy, r * 0.78, a0, a1); ctx.stroke();
    for (let i = 0; i <= 10; i++) {
      const a = a0 + ((a1 - a0) * i) / 10;
      const inner = i % 5 === 0 ? 0.6 : 0.68;
      ctx.strokeStyle = 'rgba(199,212,234,0.75)';
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a) * r * 0.78, cy + Math.sin(a) * r * 0.78);
      ctx.lineTo(cx + Math.cos(a) * r * inner, cy + Math.sin(a) * r * inner);
      ctx.stroke();
    }
    const t = Math.max(0, Math.min(1, value / max));
    const na = a0 + (a1 - a0) * t;
    ctx.strokeStyle = ACCENT; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(na) * r * 0.72, cy + Math.sin(na) * r * 0.72); ctx.stroke();
    ctx.fillStyle = ACCENT;
    ctx.beginPath(); ctx.arc(cx, cy, 3.4, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(232,238,251,0.92)';
    ctx.font = '700 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`A  ${value.toFixed(2)} A`, cx, cy + r + 15);
  }

  function drawGraph(ctx, x, y, w, h) {
    ctx.fillStyle = 'rgba(8,16,30,0.78)';
    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, 8); else ctx.rect(x, y, w, h);
    ctx.fill(); ctx.stroke();

    const padL = 34; const padR = 12; const padT = 20; const padB = 26;
    const gx = x + padL; const gy = y + padT;
    const gw = w - padL - padR; const gh = h - padT - padB;
    const xMax = 26;
    const yMax = 5;
    ctx.strokeStyle = 'rgba(199,212,234,0.45)';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(gx, gy); ctx.lineTo(gx, gy + gh); ctx.lineTo(gx + gw, gy + gh); ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.8)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('I (A)', gx - 30, gy - 6);
    ctx.textAlign = 'right';
    ctx.fillText('V (volt)', x + w - 12, gy + gh + 18);
    ctx.textAlign = 'center';
    for (let v = 0; v <= 24; v += 6) {
      const px = gx + (v / xMax) * gw;
      ctx.strokeStyle = 'rgba(199,212,234,0.18)';
      ctx.beginPath(); ctx.moveTo(px, gy); ctx.lineTo(px, gy + gh); ctx.stroke();
      ctx.fillStyle = 'rgba(199,212,234,0.7)';
      ctx.fillText(String(v), px, gy + gh + 12);
    }
    for (let i = 0; i <= 4; i++) {
      const py = gy + gh - (i / yMax / 4 * 4) * gh / 1;
      ctx.strokeStyle = 'rgba(199,212,234,0.18)';
      ctx.beginPath(); ctx.moveTo(gx, gy + gh - (i / 4) * gh); ctx.lineTo(gx + gw, gy + gh - (i / 4) * gh); ctx.stroke();
      ctx.fillStyle = 'rgba(199,212,234,0.7)';
      ctx.textAlign = 'right';
      ctx.fillText((yMax * i / 4).toFixed(2), gx - 4, gy + gh - (i / 4) * gh + 3);
      ctx.textAlign = 'center';
      void py;
    }
    if (fit) {
      const y1 = fit.m * 0 + fit.b;
      const y2 = fit.m * xMax + fit.b;
      ctx.strokeStyle = 'rgba(52,211,153,0.85)';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      ctx.moveTo(gx, gy + gh - Math.max(0, Math.min(1, y1 / yMax)) * gh);
      ctx.lineTo(gx + gw, gy + gh - Math.max(0, Math.min(1, y2 / yMax)) * gh);
      ctx.stroke();
    }
    points.forEach((p) => {
      const px = gx + (p.x / xMax) * gw;
      const py = gy + gh - Math.max(0, Math.min(1, p.y / yMax)) * gh;
      ctx.fillStyle = ACCENT;
      ctx.beginPath(); ctx.arc(px, py, 3.4, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 1; ctx.stroke();
    });
    ctx.fillStyle = BLUE;
    ctx.font = '700 10px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('V–I graph', x + 10, y + 14);
  }

  function drawCircuit(ctx, x, y, w, h) {
    const left = x + 16; const right = x + w - 16;
    const top = y + 26; const bottom = y + h - 26;
    ctx.strokeStyle = 'rgba(232,238,251,0.85)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(left, top); ctx.lineTo(right, top);
    ctx.lineTo(right, bottom); ctx.lineTo(left, bottom); ctx.closePath();
    ctx.stroke();
    // battery on the left
    ctx.strokeStyle = ACCENT; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(left, (top + bottom) / 2 - 8); ctx.lineTo(left, (top + bottom) / 2 + 8); ctx.stroke();
    ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(left - 7, (top + bottom) / 2 - 4); ctx.lineTo(left + 7, (top + bottom) / 2 - 4); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(left - 11, (top + bottom) / 2 + 4); ctx.lineTo(left + 11, (top + bottom) / 2 + 4); ctx.stroke();
    ctx.fillStyle = 'rgba(232,238,251,0.85)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`${V.toFixed(1)} V`, left + 8, (top + bottom) / 2 + 4);

    // ammeter on the top wire
    drawAmmeter(ctx, (left + right) / 2, top, 26, current(), Math.max(2, 24 / equivalent() * 1.2));

    // resistors on the bottom wire
    const box = (bx, label, value, color) => {
      ctx.fillStyle = 'rgba(8,16,30,0.9)';
      ctx.strokeStyle = color; ctx.lineWidth = 2;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(bx - 26, bottom - 11, 52, 22, 4); else ctx.rect(bx - 26, bottom - 11, 52, 22);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = 'rgba(232,238,251,0.95)';
      ctx.font = '700 10px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(label, bx, bottom + 3);
      ctx.fillStyle = color;
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.fillText(`${value.toFixed(1)} Ω`, bx, bottom + 26);
    };
    if (mode === 'single') {
      box((left + right) / 2, 'R₁', R1, BLUE);
    } else if (mode === 'series') {
      box(left + (right - left) * 0.3, 'R₁', R1, BLUE);
      box(left + (right - left) * 0.7, 'R₂', R2, GREEN);
    } else {
      box(left + (right - left) * 0.34, 'R₁', R1, BLUE);
      box(left + (right - left) * 0.66, 'R₂', R2, GREEN);
      ctx.strokeStyle = 'rgba(232,238,251,0.5)';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(left + (right - left) * 0.34 - 26, bottom);
      ctx.lineTo(left + (right - left) * 0.34 - 26, bottom + 30);
      ctx.lineTo(left + (right - left) * 0.66 + 26, bottom + 30);
      ctx.lineTo(left + (right - left) * 0.66 + 26, bottom);
      ctx.stroke();
    }
    void ROSE;
  }

  function draw(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);
    const Req = equivalent();
    const I = current();
    const graphW = Math.max(210, w * 0.34);
    drawCircuit(ctx, w * 0.03, h * 0.06, w - graphW - w * 0.09, h * 0.86);
    drawGraph(ctx, w - graphW - w * 0.03, h * 0.08, graphW, h * 0.5);
    readR.set(`${Req.toFixed(2)} Ω`);
    readI.set(`${I.toFixed(3)} A`);
    readSlope.set(fit ? `${fit.m.toFixed(3)} A/V → R ≈ ${(1 / fit.m).toFixed(2)} Ω` : 'record at least two points');
    void r2Slider;
  }

  sim.setUpdate(draw);
  sim.onResize(() => sim.renderOnce());
  sim.start();

  return {
    dispose() { sim.dispose(); hud.dispose(); panel.dispose(); },
  };
}
