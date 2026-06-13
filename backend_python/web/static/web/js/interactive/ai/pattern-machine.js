import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 1 – "What is AI?" pattern machine
// User labels points as circle or triangle; a 1-NN classifier predicts new points.
// Demonstrates: AI = pattern-matching from examples, not magic.

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Label some points!', '#6366F1');

  // labelled examples: { x, y, label: 0|1 }
  const examples = [];
  // query point for prediction
  let query = null;
  let mode = 'circle'; // 'circle' | 'triangle'
  let showTraditional = false;

  const panel = createPanel(stage, { title: 'Controls' });
  const modeSelect = panel.select({
    label: 'Label tool',
    options: [
      { value: 'circle', label: '⬤ Circle (class A)' },
      { value: 'triangle', label: '▲ Triangle (class B)' },
      { value: 'predict', label: '? Predict' },
    ],
    value: 'circle',
    onChange: (v) => { mode = v; },
  });
  panel.toggle({
    label: 'Show rule-based code',
    value: false,
    onChange: (v) => { showTraditional = v; },
  });
  panel.divider();
  const countOut = panel.readout({ label: 'Examples given', value: '0' });
  const predOut = panel.readout({ label: 'Prediction', value: '—' });
  const nnOut = panel.readout({ label: 'Nearest neighbour', value: '—' });
  panel.button({ label: 'Clear all', icon: 'delete', onClick: () => { examples.length = 0; query = null; } });
  panel.info('Add circle (A) and triangle (B) examples, then switch to Predict and click anywhere to see how the machine guesses.');

  // 1-Nearest-Neighbour classifier
  function classify(px, py) {
    if (examples.length === 0) return null;
    let best = Infinity, bestLabel = 0;
    for (const ex of examples) {
      const d = Math.hypot(px - ex.x, py - ex.y);
      if (d < best) { best = d; bestLabel = ex.label; }
    }
    return { label: bestLabel, dist: best };
  }

  function onPointer(e) {
    if (e.type === 'pointerdown') {
      const p = pointerPos(sim.canvas, e);
      // normalise to [0,1]
      const nx = p.x / sim.width;
      const ny = p.y / sim.height;
      if (mode === 'circle') {
        examples.push({ x: nx, y: ny, label: 0 });
      } else if (mode === 'triangle') {
        examples.push({ x: nx, y: ny, label: 1 });
      } else if (mode === 'predict') {
        query = { x: nx, y: ny };
      }
    }
    if (e.type === 'pointermove' && mode === 'predict') {
      const p = pointerPos(sim.canvas, e);
      query = { x: p.x / sim.width, y: p.y / sim.height };
    }
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onPointer);
  sim.canvas.addEventListener('pointermove', onPointer);

  function drawTriangle(ctx, cx, cy, r, fill) {
    ctx.beginPath();
    ctx.moveTo(cx, cy - r);
    ctx.lineTo(cx + r * 0.866, cy + r * 0.5);
    ctx.lineTo(cx - r * 0.866, cy + r * 0.5);
    ctx.closePath();
    ctx.fillStyle = fill;
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  function drawCircle(ctx, cx, cy, r, fill) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.fillStyle = fill;
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  // Draw Voronoi-like background using grid sampling
  const GRID = 30;
  let bgCache = null;
  let lastExCount = -1;

  function buildBgCache(w, h) {
    if (examples.length === lastExCount && bgCache && bgCache.w === w && bgCache.h === h) return;
    lastExCount = examples.length;
    bgCache = { w, h, cells: [] };
    for (let gy = 0; gy < GRID; gy++) {
      for (let gx = 0; gx < GRID; gx++) {
        const nx = (gx + 0.5) / GRID;
        const ny = (gy + 0.5) / GRID;
        const res = classify(nx, ny);
        bgCache.cells.push({ gx, gy, label: res ? res.label : -1 });
      }
    }
  }

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);

    // Background gradient
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729');
    bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    // Decision region background
    if (examples.length >= 2) {
      buildBgCache(w, h);
      const cw = w / GRID;
      const ch = h / GRID;
      for (const cell of bgCache.cells) {
        if (cell.label < 0) continue;
        ctx.fillStyle = cell.label === 0
          ? 'rgba(99,102,241,0.18)'
          : 'rgba(245,158,11,0.18)';
        ctx.fillRect(cell.gx * cw, cell.gy * ch, cw + 1, ch + 1);
      }
    }

    // Grid lines
    ctx.strokeStyle = 'rgba(255,255,255,0.04)';
    ctx.lineWidth = 1;
    for (let i = 1; i < 8; i++) {
      ctx.beginPath(); ctx.moveTo(w * i / 8, 0); ctx.lineTo(w * i / 8, h); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, h * i / 8); ctx.lineTo(w, h * i / 8); ctx.stroke();
    }

    // Draw examples
    for (const ex of examples) {
      const px = ex.x * w, py = ex.y * h;
      if (ex.label === 0) drawCircle(ctx, px, py, 12, '#6366F1');
      else drawTriangle(ctx, px, py, 13, '#F59E0B');
    }

    // Query + prediction
    if (query && mode === 'predict') {
      const px = query.x * w, py = query.y * h;
      const res = classify(query.x, query.y);
      if (res) {
        // Draw line to nearest neighbour
        const nearest = examples.reduce((b, ex) => {
          const d = Math.hypot(ex.x - query.x, ex.y - query.y);
          return d < b.d ? { ex, d } : b;
        }, { ex: null, d: Infinity });
        if (nearest.ex) {
          ctx.setLineDash([4, 4]);
          ctx.strokeStyle = 'rgba(200,200,200,0.5)';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(px, py);
          ctx.lineTo(nearest.ex.x * w, nearest.ex.y * h);
          ctx.stroke();
          ctx.setLineDash([]);
        }
        // Glow ring
        ctx.beginPath();
        ctx.arc(px, py, 22, 0, Math.PI * 2);
        ctx.strokeStyle = res.label === 0 ? 'rgba(99,102,241,0.7)' : 'rgba(245,158,11,0.7)';
        ctx.lineWidth = 2.5;
        ctx.stroke();
        // Predicted shape
        if (res.label === 0) drawCircle(ctx, px, py, 13, 'rgba(99,102,241,0.85)');
        else drawTriangle(ctx, px, py, 14, 'rgba(245,158,11,0.85)');
        // ? label
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 11px Poppins,sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('?', px, py + 4);
        predOut.set(res.label === 0 ? 'Circle (A)' : 'Triangle (B)');
        nnOut.set(`${(res.dist * Math.max(w, h)).toFixed(1)} px`);
      } else {
        ctx.beginPath();
        ctx.arc(px, py, 16, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(200,200,200,0.5)';
        ctx.lineWidth = 2;
        ctx.stroke();
        predOut.set('Need examples first');
      }
    }

    // Traditional code overlay
    if (showTraditional) {
      const lines = [
        'Traditional programming:',
        'if (x > 0.5 && y < 0.3) → Circle',
        'else if (x < 0.3) → Triangle',
        '// Brittle: breaks on new data',
        '',
        'AI approach:',
        'classify(x, y) { find nearest',
        '  labelled example, return its',
        '  class } // learns from data!',
      ];
      ctx.fillStyle = 'rgba(10,15,30,0.88)';
      const bw = 240, bh = lines.length * 17 + 20;
      if (ctx.roundRect) ctx.roundRect(w - bw - 12, 12, bw, bh, 8);
      else ctx.rect(w - bw - 12, 12, bw, bh);
      ctx.fill();
      ctx.font = '12px monospace';
      ctx.textAlign = 'left';
      lines.forEach((line, i) => {
        ctx.fillStyle = i === 0 || i === 4 ? '#F59E0B' : '#a0d8ef';
        ctx.fillText(line, w - bw - 4, 28 + i * 17);
      });
    }

    // Labels
    ctx.fillStyle = '#e8eefb';
    ctx.font = '700 13px Poppins,sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('⬤ Circle = Class A', 14, 24);
    ctx.fillText('▲ Triangle = Class B', 14, 42);

    countOut.set(String(examples.length));
    badge.set(examples.length === 0 ? 'Add labelled examples' : mode === 'predict' ? 'Predicting…' : `Labelling: ${mode}`);
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onPointer);
      sim.canvas.removeEventListener('pointermove', onPointer);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
