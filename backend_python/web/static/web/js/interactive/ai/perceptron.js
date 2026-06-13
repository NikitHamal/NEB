import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 2 – The Neuron: interactive perceptron
// y = step(w1*x1 + w2*x2 + b)
// Decision boundary: w1*x1 + w2*x2 + b = 0  →  x2 = -(w1*x1 + b) / w2

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Perceptron', '#6366F1');

  let w1 = 1.2, w2 = -0.8, bias = -0.3;
  let activation = 'step'; // 'step' | 'sigmoid'

  const panel = createPanel(stage, { title: 'Neuron Controls' });
  panel.slider({ label: 'Weight w₁', min: -3, max: 3, step: 0.05, value: w1,
    format: (v) => v.toFixed(2), onChange: (v) => { w1 = v; } });
  panel.slider({ label: 'Weight w₂', min: -3, max: 3, step: 0.05, value: w2,
    format: (v) => v.toFixed(2), onChange: (v) => { w2 = v; } });
  panel.slider({ label: 'Bias b', min: -3, max: 3, step: 0.05, value: bias,
    format: (v) => v.toFixed(2), onChange: (v) => { bias = v; } });
  panel.select({
    label: 'Activation',
    options: [{ value: 'step', label: 'Step (hard)' }, { value: 'sigmoid', label: 'Sigmoid (soft)' }],
    value: 'step',
    onChange: (v) => { activation = v; },
  });
  panel.divider();
  const sumOut = panel.readout({ label: 'Weighted sum z', value: '—' });
  const outOut = panel.readout({ label: 'Output f(z)', value: '—' });
  panel.info('Drag sliders to move the decision boundary. The line is where w₁x₁ + w₂x₂ + b = 0.');

  function sigmoid(z) { return 1 / (1 + Math.exp(-z)); }
  function activate(z) { return activation === 'step' ? (z >= 0 ? 1 : 0) : sigmoid(z); }

  // Fixed test points for demonstration
  const POINTS = [
    { x1: 0.6, x2: 0.7 }, { x1: 0.8, x2: 0.4 }, { x1: 0.7, x2: 0.8 },
    { x1: 0.2, x2: 0.3 }, { x1: 0.1, x2: 0.6 }, { x1: 0.3, x2: 0.2 },
    { x1: 0.5, x2: 0.5 }, { x1: 0.9, x2: 0.1 }, { x1: 0.15, x2: 0.8 },
    { x1: 0.6, x2: 0.2 }, { x1: 0.4, x2: 0.7 }, { x1: 0.8, x2: 0.6 },
  ];

  // hover tracking
  let hoverPt = null;

  sim.canvas.addEventListener('pointermove', (e) => {
    const rect = sim.canvas.getBoundingClientRect();
    hoverPt = { cx: e.clientX - rect.left, cy: e.clientY - rect.top };
  });
  sim.canvas.addEventListener('pointerleave', () => { hoverPt = null; });

  function drawNeuronDiagram(ctx, w, h) {
    // Small neuron diagram top-right
    const cx = w - 90, cy = 80, r = 28;
    // Input lines
    ctx.strokeStyle = '#6366F1'; ctx.lineWidth = 2;
    const inputs = [
      { lx: cx - 70, ly: cy - 20, label: 'x₁' },
      { lx: cx - 70, ly: cy + 20, label: 'x₂' },
    ];
    inputs.forEach(({ lx, ly }) => {
      ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(cx - r, cy + (ly - cy) * 0.3); ctx.stroke();
    });
    // Weights labels
    ctx.fillStyle = '#a5b4fc'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'right';
    ctx.fillText(`w₁=${w1.toFixed(1)}`, cx - 36, cy - 14);
    ctx.fillText(`w₂=${w2.toFixed(1)}`, cx - 36, cy + 26);

    // Neuron body
    const grad = ctx.createRadialGradient(cx - 6, cy - 6, 3, cx, cy, r);
    grad.addColorStop(0, '#818cf8'); grad.addColorStop(1, '#4338ca');
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.fillStyle = grad; ctx.fill();
    ctx.strokeStyle = 'rgba(165,180,252,0.8)'; ctx.lineWidth = 2; ctx.stroke();

    // bias text inside
    ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Poppins,sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('Σ', cx, cy - 4);
    ctx.fillText(`b=${bias.toFixed(1)}`, cx, cy + 10);

    // output arrow
    ctx.strokeStyle = '#F59E0B'; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(cx + r, cy); ctx.lineTo(cx + r + 40, cy); ctx.stroke();
    // arrowhead
    ctx.fillStyle = '#F59E0B'; ctx.beginPath();
    ctx.moveTo(cx + r + 40, cy); ctx.lineTo(cx + r + 30, cy - 5); ctx.lineTo(cx + r + 30, cy + 5);
    ctx.closePath(); ctx.fill();

    // input labels
    ctx.fillStyle = '#e8eefb'; ctx.font = '12px Poppins,sans-serif'; ctx.textAlign = 'right';
    inputs.forEach(({ lx, ly, label }) => ctx.fillText(label, lx - 4, ly + 4));
  }

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);

    // Feature space occupies left part
    const margin = 40;
    const fsX = margin, fsY = margin;
    const fsW = Math.min(w - 220, w * 0.65), fsH = h - margin * 2 - 60;

    // Colored background regions
    const res = 24;
    const cw = fsW / res, ch = fsH / res;
    for (let gy = 0; gy < res; gy++) {
      for (let gx = 0; gx < res; gx++) {
        const x1n = gx / res, x2n = 1 - gy / res;
        const z = w1 * x1n + w2 * x2n + bias;
        const out = activation === 'sigmoid' ? sigmoid(z) : (z >= 0 ? 1 : 0);
        ctx.fillStyle = `rgba(${activation === 'sigmoid'
          ? `${Math.round(out * 245 + (1 - out) * 99)},${Math.round(out * 158 + (1 - out) * 102)},${Math.round(out * 11 + (1 - out) * 241)},0.22`
          : (out > 0.5 ? '245,158,11,0.18' : '99,102,241,0.18')})`;
        ctx.fillRect(fsX + gx * cw, fsY + gy * ch, cw + 1, ch + 1);
      }
    }

    // Feature space border
    ctx.strokeStyle = 'rgba(165,180,252,0.4)'; ctx.lineWidth = 1.5;
    ctx.strokeRect(fsX, fsY, fsW, fsH);

    // Axis labels
    ctx.fillStyle = 'rgba(199,212,234,0.7)'; ctx.font = '11px Poppins,sans-serif';
    ctx.textAlign = 'center'; ctx.fillText('Feature x₁', fsX + fsW / 2, fsY + fsH + 18);
    ctx.save(); ctx.translate(fsX - 18, fsY + fsH / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('Feature x₂', 0, 0); ctx.restore();

    // Decision boundary line: w1*x1 + w2*x2 + b = 0
    // x2 = -(w1*x1 + b) / w2
    if (Math.abs(w2) > 0.05) {
      ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = 2.5; ctx.setLineDash([6, 4]);
      ctx.beginPath();
      const x1a = 0, x2a = -(w1 * x1a + bias) / w2;
      const x1b = 1, x2b = -(w1 * x1b + bias) / w2;
      const toCanvas = (x1, x2) => ({ px: fsX + x1 * fsW, py: fsY + (1 - x2) * fsH });
      const ca = toCanvas(x1a, x2a), cb = toCanvas(x1b, x2b);
      ctx.moveTo(ca.px, ca.py); ctx.lineTo(cb.px, cb.py); ctx.stroke();
      ctx.setLineDash([]);
      // Label
      const mx = (ca.px + cb.px) / 2, my = (ca.py + cb.py) / 2;
      ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Poppins,sans-serif'; ctx.textAlign = 'center';
      ctx.fillText('Decision boundary', mx, Math.min(Math.max(my - 8, fsY + 16), fsY + fsH - 8));
    } else {
      // Vertical line
      const x1v = -bias / w1;
      const px = fsX + x1v * fsW;
      if (px >= fsX && px <= fsX + fsW) {
        ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = 2.5; ctx.setLineDash([6, 4]);
        ctx.beginPath(); ctx.moveTo(px, fsY); ctx.lineTo(px, fsY + fsH); ctx.stroke();
        ctx.setLineDash([]);
      }
    }

    // Data points
    for (const pt of POINTS) {
      const z = w1 * pt.x1 + w2 * pt.x2 + bias;
      const out = activate(z);
      const px = fsX + pt.x1 * fsW, py = fsY + (1 - pt.x2) * fsH;
      ctx.beginPath(); ctx.arc(px, py, 9, 0, Math.PI * 2);
      ctx.fillStyle = out >= 0.5 ? '#F59E0B' : '#6366F1';
      ctx.fill(); ctx.strokeStyle = 'rgba(255,255,255,0.6)'; ctx.lineWidth = 1.5; ctx.stroke();
    }

    // Hover: show z and output for nearest point
    if (hoverPt) {
      const x1h = (hoverPt.cx - fsX) / fsW;
      const x2h = 1 - (hoverPt.cy - fsY) / fsH;
      if (x1h >= 0 && x1h <= 1 && x2h >= 0 && x2h <= 1) {
        const z = w1 * x1h + w2 * x2h + bias;
        const out = activate(z);
        sumOut.set(z.toFixed(3));
        outOut.set(out.toFixed(3));
        badge.set(out >= 0.5 ? 'Output → 1 (fires!)' : 'Output → 0 (silent)');
      }
    }

    // Activation function plot
    const afX = fsX + fsW + 30, afY = fsY, afW = w - afX - 20, afH = Math.min(fsH * 0.55, 140);
    if (afW > 60) {
      ctx.strokeStyle = 'rgba(165,180,252,0.4)'; ctx.lineWidth = 1;
      ctx.strokeRect(afX, afY, afW, afH);
      ctx.fillStyle = 'rgba(199,212,234,0.7)'; ctx.font = '10px Poppins,sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(activation === 'step' ? 'Step function' : 'Sigmoid σ(z)', afX + afW / 2, afY - 6);
      const midY = afY + afH / 2;
      ctx.strokeStyle = 'rgba(165,180,252,0.25)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(afX, midY); ctx.lineTo(afX + afW, midY); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(afX + afW / 2, afY); ctx.lineTo(afX + afW / 2, afY + afH); ctx.stroke();
      ctx.strokeStyle = '#F59E0B'; ctx.lineWidth = 2.5; ctx.beginPath();
      for (let i = 0; i <= afW; i++) {
        const z = (i / afW - 0.5) * 8;
        const out = activate(z);
        const px2 = afX + i;
        const py2 = midY - (out - 0.5) * (afH - 16);
        if (i === 0) ctx.moveTo(px2, py2); else ctx.lineTo(px2, py2);
      }
      ctx.stroke();
      // current z marker
      const zCur = (hoverPt && (hoverPt.cx - fsX) / fsW >= 0 && (hoverPt.cx - fsX) / fsW <= 1)
        ? (() => { const x1h = (hoverPt.cx - fsX) / fsW; const x2h = 1 - (hoverPt.cy - fsY) / fsH; return w1 * x1h + w2 * x2h + bias; })()
        : w1 * 0.5 + w2 * 0.5 + bias;
      const zPx = afX + (zCur / 8 + 0.5) * afW;
      const outCur = activate(zCur);
      const outPy = midY - (outCur - 0.5) * (afH - 16);
      if (zPx >= afX && zPx <= afX + afW) {
        ctx.strokeStyle = 'rgba(255,255,255,0.5)'; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
        ctx.beginPath(); ctx.moveTo(zPx, afY); ctx.lineTo(zPx, afY + afH); ctx.stroke();
        ctx.setLineDash([]);
        ctx.beginPath(); ctx.arc(zPx, outPy, 5, 0, Math.PI * 2);
        ctx.fillStyle = '#fff'; ctx.fill();
      }
      // Axis ticks
      ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '9px monospace'; ctx.textAlign = 'center';
      [-4, -2, 0, 2, 4].forEach((v) => {
        const x = afX + (v / 8 + 0.5) * afW;
        ctx.fillText(v, x, afY + afH + 10);
      });
      ctx.textAlign = 'right';
      ctx.fillText('1', afX - 2, afY + 10); ctx.fillText('0', afX - 2, afY + afH - 2);
    }

    drawNeuronDiagram(ctx, w, h);
  });

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
