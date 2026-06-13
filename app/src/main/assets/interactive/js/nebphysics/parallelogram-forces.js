import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Adjusting…', '#9ec1ff');

  let P = 150;
  let Q = 150;
  let R = 200;
  let ox = 0.5;
  let oy = 0.45;
  let vx = 0;
  let vy = 0;
  let showPara = true;
  let dragging = false;

  const panel = createPanel(stage, { title: 'Gravesand Apparatus' });
  const pS = panel.slider({ label: 'Weight P (left)', min: 50, max: 300, step: 10, value: P, format: (v) => `${v} g`, onChange: (v) => { P = v; } });
  const qS = panel.slider({ label: 'Weight Q (right)', min: 50, max: 300, step: 10, value: Q, format: (v) => `${v} g`, onChange: (v) => { Q = v; } });
  const rS = panel.slider({ label: 'Weight R (middle)', min: 50, max: 400, step: 10, value: R, format: (v) => `${v} g`, onChange: (v) => { R = v; } });
  panel.toggle({ label: 'Show parallelogram', value: true, onChange: (v) => { showPara = v; } });
  panel.divider();
  const angOut = panel.readout({ label: 'Angle P–Q (γ)', value: '—' });
  const resOut = panel.readout({ label: '√(P²+Q²+2PQcosγ)', value: '—' });
  const rOut = panel.readout({ label: 'Weight R', value: '—' });
  const errOut = panel.readout({ label: 'Difference', value: '—' });
  panel.button({
    label: 'Random weights',
    icon: 'casino',
    onClick: () => {
      P = 50 + 10 * Math.floor(Math.random() * 26);
      Q = 50 + 10 * Math.floor(Math.random() * 26);
      const lim = Math.min(P + Q - 20, 400);
      const low = Math.abs(P - Q) + 20;
      R = Math.max(50, Math.min(lim, low + 10 * Math.floor(Math.random() * Math.max(1, (lim - low) / 10))));
      pS.set(P); qS.set(Q); rS.set(R);
    },
  });
  panel.info('Strings over the two pulleys carry P and Q; R hangs from the junction O. The knot settles where the three tensions balance. You can also drag the knot and watch it return.');

  function pulleys(w, h) {
    return [
      { x: w * 0.13, y: h * 0.1 },
      { x: w * 0.87, y: h * 0.1 },
    ];
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const px = ox * sim.width;
    const py = oy * sim.height;
    if (Math.hypot(p.x - px, p.y - py) < 44) {
      dragging = true;
      if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    ox = Math.max(0.1, Math.min(0.9, p.x / sim.width));
    oy = Math.max(0.12, Math.min(0.75, p.y / sim.height));
    vx = 0;
    vy = 0;
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function drawWeightStack(ctx, x, y, grams, label) {
    const n = Math.max(1, Math.round(grams / 50));
    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(x, y - 14);
    ctx.lineTo(x, y);
    ctx.stroke();
    for (let i = 0; i < n; i++) {
      ctx.fillStyle = i % 2 ? '#4d5f85' : '#5b6f99';
      ctx.fillRect(x - 13, y + i * 7, 26, 6);
    }
    labelText(ctx, `${label} = ${grams} g`, x, y + n * 7 + 14, { size: 9.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.9)' });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    const [p1, p2] = pulleys(w, h);
    const px = ox * w;
    const py = oy * h;
    const u1 = norm(p1.x - px, p1.y - py);
    const u2 = norm(p2.x - px, p2.y - py);
    const fx = P * u1.x + Q * u2.x;
    const fy = P * u1.y + Q * u2.y + R;
    if (!dragging) {
      const k = 0.000045;
      vx += fx * k * (dt * 60);
      vy += fy * k * (dt * 60);
      vx *= 0.86;
      vy *= 0.86;
      ox = Math.max(0.1, Math.min(0.9, ox + vx * dt));
      oy = Math.max(0.12, Math.min(0.8, oy + vy * dt));
    }
    const balanced = Math.hypot(fx, fy) < 6 && !dragging;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = 'rgba(57,73,107,0.35)';
    ctx.fillRect(w * 0.06, h * 0.05, w * 0.88, h * 0.62);
    ctx.strokeStyle = 'rgba(158,193,255,0.2)';
    ctx.strokeRect(w * 0.06, h * 0.05, w * 0.88, h * 0.62);

    [p1, p2].forEach((pp) => {
      ctx.fillStyle = '#39496b';
      ctx.beginPath();
      ctx.arc(pp.x, pp.y, 11, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#9ec1ff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    ctx.strokeStyle = '#e8eefb';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(px, py);
    ctx.lineTo(p1.x, p1.y);
    ctx.moveTo(px, py);
    ctx.lineTo(p2.x, p2.y);
    ctx.moveTo(px, py);
    ctx.lineTo(px, py + 46);
    ctx.moveTo(p1.x - 11, p1.y);
    ctx.lineTo(p1.x - 11, p1.y + 50);
    ctx.moveTo(p2.x + 11, p2.y);
    ctx.lineTo(p2.x + 11, p2.y + 50);
    ctx.stroke();

    drawWeightStack(ctx, p1.x - 11, p1.y + 52, P, 'P');
    drawWeightStack(ctx, p2.x + 11, p2.y + 52, Q, 'Q');
    drawWeightStack(ctx, px, py + 48, R, 'R');

    const vScale = 0.42;
    const a1 = { x: u1.x * P * vScale, y: u1.y * P * vScale };
    const a2 = { x: u2.x * Q * vScale, y: u2.y * Q * vScale };
    arrow(ctx, px, py, px + a1.x, py + a1.y, '#F59E0B');
    arrow(ctx, px, py, px + a2.x, py + a2.y, '#8be9a8');
    arrow(ctx, px, py, px, py + R * vScale, '#ff8c8c');
    if (showPara) {
      ctx.strokeStyle = 'rgba(158,193,255,0.6)';
      ctx.setLineDash([5, 5]);
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(px + a1.x, py + a1.y);
      ctx.lineTo(px + a1.x + a2.x, py + a1.y + a2.y);
      ctx.lineTo(px + a2.x, py + a2.y);
      ctx.stroke();
      ctx.setLineDash([]);
      arrow(ctx, px, py, px + a1.x + a2.x, py + a1.y + a2.y, '#9ec1ff');
      labelText(ctx, 'resultant of P & Q', px + a1.x + a2.x + 6, py + a1.y + a2.y, { size: 9, weight: 600, color: '#9ec1ff' });
    }

    ctx.fillStyle = balanced ? '#8be9a8' : '#ffd584';
    ctx.beginPath();
    ctx.arc(px, py, 7, 0, Math.PI * 2);
    ctx.fill();

    const cosg = u1.x * u2.x + u1.y * u2.y;
    const gamma = Math.acos(Math.max(-1, Math.min(1, cosg)));
    const res = Math.sqrt(P * P + Q * Q + 2 * P * Q * Math.cos(gamma));
    angOut.set(`${fmt((gamma * 180) / Math.PI, 1)}°`);
    resOut.set(`${fmt(res, 0)} g-wt`);
    rOut.set(`${R} g-wt`);
    errOut.set(balanced ? `${fmt(Math.abs(res - R), 1)} g-wt (${fmt((100 * Math.abs(res - R)) / R, 1)}%)` : 'wait for balance');
    statusBadge.set(
      dragging ? 'Dragging the knot…'
        : balanced ? 'Balanced — resultant of P & Q equals R'
          : R >= P + Q || P >= Q + R || Q >= P + R ? 'No equilibrium possible (triangle rule!)' : 'Knot settling…',
    );
  });

  function norm(x, y) {
    const m = Math.hypot(x, y) || 1;
    return { x: x / m, y: y / m };
  }

  function arrow(ctx, x0, y0, x1, y1, color) {
    const ang = Math.atan2(y1 - y0, x1 - x0);
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 - 9 * Math.cos(ang - 0.42), y1 - 9 * Math.sin(ang - 0.42));
    ctx.lineTo(x1 - 9 * Math.cos(ang + 0.42), y1 - 9 * Math.sin(ang + 0.42));
    ctx.closePath();
    ctx.fill();
  }

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      sim.canvas.removeEventListener('pointermove', onMove);
      sim.canvas.removeEventListener('pointerup', onUp);
      sim.canvas.removeEventListener('pointercancel', onUp);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
