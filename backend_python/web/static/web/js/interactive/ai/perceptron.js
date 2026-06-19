import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { panelBg, labelText } from '../biology/bio-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const accBadge = hud.badge('Accuracy: —', '#a3e635');

  // Two classes of points
  let points = [];
  function makeData(kind) {
    points = [];
    if (kind === 'linear') {
      // two separable blobs
      for (let i = 0; i < 12; i++) {
        points.push({ x: 0.25 + (Math.random() - 0.5) * 0.25, y: 0.7 + (Math.random() - 0.5) * 0.25, c: 1 });
        points.push({ x: 0.75 + (Math.random() - 0.5) * 0.25, y: 0.3 + (Math.random() - 0.5) * 0.25, c: 0 });
      }
    } else {
      // XOR-like (not linearly separable)
      for (let i = 0; i < 8; i++) {
        points.push({ x: 0.25 + (Math.random() - 0.5) * 0.18, y: 0.25 + (Math.random() - 0.5) * 0.18, c: 1 });
        points.push({ x: 0.75 + (Math.random() - 0.5) * 0.18, y: 0.75 + (Math.random() - 0.5) * 0.18, c: 1 });
        points.push({ x: 0.25 + (Math.random() - 0.5) * 0.18, y: 0.75 + (Math.random() - 0.5) * 0.18, c: 0 });
        points.push({ x: 0.75 + (Math.random() - 0.5) * 0.18, y: 0.25 + (Math.random() - 0.5) * 0.18, c: 0 });
      }
    }
  }
  makeData('linear');

  // Manual line: y = m*x + b, in 0..1 space; and an auto perceptron
  let lineM = -1; let lineB = 1.0;
  let autoLine = null; // {w1,w2,b} — decision: w1*x + w2*y + b >= 0 -> class 1
  let useAuto = false;
  let autoAcc = 0;

  function autoClassify(p, l) {
    if (!l) return 0;
    return (l.w1 * p.x + l.w2 * p.y + l.b) >= 0 ? 1 : 0;
  }
  function trainAuto() {
    if (!autoLine) autoLine = { w1: Math.random() - 0.5, w2: Math.random() - 0.5, b: 0 };
    for (let iter = 0; iter < 200; iter++) {
      const p = points[Math.floor(Math.random() * points.length)];
      const pred = autoClassify(p, autoLine) ? 1 : 0;
      const err = p.c - pred;
      const lr = 0.05;
      autoLine.w1 += lr * err * p.x;
      autoLine.w2 += lr * err * p.y;
      autoLine.b += lr * err;
    }
    // accuracy
    let correct = 0;
    points.forEach((p) => { if (autoClassify(p, autoLine) === p.c) correct++; });
    autoAcc = correct / points.length;
  }

  const panel = createPanel(stage, { title: 'Drawing the Line' });
  panel.info('A classifier separates groups by drawing a boundary. Drag the white line to separate red and blue. Or press Auto-train and let a perceptron learn the line itself.');
  panel.select({
    label: 'Dataset', value: 'linear',
    options: [{ value: 'linear', label: 'Linearly separable' }, { value: 'xor', label: 'XOR (not separable)' }],
    onChange: (v) => { makeData(v); autoLine = null; autoAcc = 0; },
  });
  panel.button({ label: 'Auto-train perceptron', icon: 'model_training', onClick: () => { useAuto = true; trainAuto(); } });
  panel.toggle({ label: 'Keep training', value: false, onChange: (v) => { useAuto = v; if (v && !autoLine) trainAuto(); } });
  panel.divider();
  const accOut = panel.readout({ label: 'Accuracy', value: '—' });
  panel.button({ label: 'Why can\'t one line solve XOR?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'The XOR problem',
      body: 'XOR arranges four points so no single straight line can separate them. A single perceptron provably cannot solve it. The fix is a hidden layer — several perceptrons whose lines combine into a curved boundary.',
      color: '#6366F1',
    });
  } });

  // Drag the manual line by dragging its endpoints
  let dragging = null;
  function lineEnds() {
    // two control points: left (x=0) and right (x=1) at y = b and y = m+b
    return [
      { x: 0, y: lineB },
      { x: 1, y: lineM + lineB },
    ];
  }
  function plotGeom(w, h) {
    const padL = 40; const padT = 20; const padB = 30; const padR = 20;
    return { x: padL, y: padT, w: w - padL - padR, h: h - padT - padB };
  }
  function dataToPx(p, g, W, H) {
    return { x: g.x + p.x * g.w, y: g.y + (1 - p.y) * g.h };
  }
  function pxToData(px, py, g) {
    return { x: (px - g.x) / g.w, y: 1 - (py - g.y) / g.h };
  }
  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const g = plotGeom(sim.width, sim.height);
    const ends = lineEnds();
    ends.forEach((en, i) => {
      const ep = dataToPx(en, g);
      if (Math.hypot(p.x - ep.x, p.y - ep.y) < 18) dragging = i;
    });
    if (dragging !== null && sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
  }
  function onMove(e) {
    if (dragging === null) return;
    const p = pointerPos(sim.canvas, e);
    const g = plotGeom(sim.width, sim.height);
    const d = pxToData(p.x, p.y, g);
    // dragging left end sets b; right end sets m+b
    if (dragging === 0) lineB = Math.max(-0.5, Math.min(1.5, d.y));
    else { lineM = Math.max(-0.5, Math.min(1.5, d.y)) - lineB; }
    useAuto = false;
  }
  function onUp() { dragging = null; }
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);

  function manualClassify(p) {
    // above the line (y > m*x + b) -> class 1
    return p.y > (lineM * p.x + lineB) ? 1 : 0;
  }

  let trainAcc = 0;
  sim.setUpdate((ctx, dt) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#070a14'; ctx.fillRect(0, 0, w, h);
    const g = plotGeom(w, h);
    panelBg(ctx, g.x, g.y, g.w, g.h);

    if (useAuto && autoLine) {
      // train a bit each frame
      trainAuto();
    }

    // decision boundary
    const classify = useAuto ? ((p) => autoClassify(p, autoLine)) : manualClassify;
    // fill regions lightly
    if (useAuto && autoLine) {
      // draw contour: sample grid
      const step = 12;
      for (let py = 0; py < g.h; py += step) {
        for (let px = 0; px < g.w; px += step) {
          const d = pxToData(g.x + px, g.y + py, g);
          const cls = autoClassify(d, autoLine);
          ctx.fillStyle = cls === 1 ? 'rgba(96,165,250,0.10)' : 'rgba(248,113,113,0.10)';
          ctx.fillRect(g.x + px, g.y + py, step, step);
        }
      }
      // draw boundary line where w1*x + w2*y + b = 0
      const l = autoLine;
      ctx.strokeStyle = '#34d399'; ctx.lineWidth = 2.5;
      ctx.beginPath();
      let first = true;
      for (let i = 0; i <= 60; i++) {
        const x = i / 60;
        if (Math.abs(l.w2) < 1e-6) continue;
        const y = -(l.w1 * x + l.b) / l.w2;
        if (y < -0.2 || y > 1.2) continue;
        const pp = dataToPx({ x, y }, g);
        if (first) { ctx.moveTo(pp.x, pp.y); first = false; } else ctx.lineTo(pp.x, pp.y);
      }
      ctx.stroke();
    } else {
      // manual line
      const ends = lineEnds().map((e) => dataToPx(e, g));
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(ends[0].x, ends[0].y); ctx.lineTo(ends[1].x, ends[1].y); ctx.stroke();
      // endpoints
      ends.forEach((en) => {
        ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(en.x, en.y, 7, 0, Math.PI * 2); ctx.fill();
      });
    }

    // points
    let correct = 0;
    points.forEach((p) => {
      const pred = classify(p);
      const ok = pred === p.c;
      if (ok) correct++;
      const pp = dataToPx(p, g);
      ctx.fillStyle = p.c === 1 ? '#60a5fa' : '#f87171';
      ctx.beginPath(); ctx.arc(pp.x, pp.y, 6, 0, Math.PI * 2); ctx.fill();
      if (!ok) {
        ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(pp.x, pp.y, 9, 0, Math.PI * 2); ctx.stroke();
      }
    });
    trainAcc = correct / points.length;

    // axes labels
    labelText(ctx, 'feature x →', g.x + g.w / 2 - 30, g.y + g.h + 22, { color: '#94a3b8', size: 10 });
    labelText(ctx, '↑ feature y', g.x - 30, g.y + 10, { color: '#94a3b8', size: 10 });

    accBadge.set(`Accuracy: ${Math.round(trainAcc * 100)}%`);
    accOut.set(`${Math.round(trainAcc * 100)}%`);
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      sim.canvas.removeEventListener('pointermove', onMove);
      sim.canvas.removeEventListener('pointerup', onUp);
      panel.dispose(); hud.dispose(); sim.dispose();
    },
  };
}
