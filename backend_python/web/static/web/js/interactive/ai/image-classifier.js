import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { panelBg, labelText } from '../biology/bio-utils.js';

const G = 16; // 16x16 grid for the drawing

// A lightweight, deterministic "classifier" based on hand-crafted features.
// Not a real neural net, but it demonstrates pixels -> features -> class scores
// and behaves plausibly for digits drawn clearly.
function features(grid) {
  const f = new Array(G).fill(0);
  let ink = 0;
  // column ink distribution
  const colSum = new Array(G).fill(0);
  const rowSum = new Array(G).fill(0);
  for (let y = 0; y < G; y++) for (let x = 0; x < G; x++) {
    const v = grid[y * G + x];
    ink += v; colSum[x] += v; rowSum[y] += v;
  }
  if (ink < 4) return null;
  // top/bottom/middle ink, left/right, holes (rough)
  let top = 0, mid = 0, bot = 0, left = 0, right = 0;
  for (let y = 0; y < G; y++) for (let x = 0; x < G; x++) {
    const v = grid[y * G + x];
    if (y < G / 3) top += v;
    else if (y > (2 * G) / 3) bot += v;
    else mid += v;
    if (x < G / 3) left += v; else if (x > (2 * G) / 3) right += v;
  }
  // aspect / symmetry
  let minX = G, maxX = 0;
  for (let x = 0; x < G; x++) if (colSum[x] > 0) { minX = Math.min(minX, x); maxX = Math.max(maxX, x); }
  const width = Math.max(1, maxX - minX);
  // vertical profile peaks
  const peaks = [];
  for (let y = 1; y < G - 1; y++) {
    if (rowSum[y] > rowSum[y - 1] && rowSum[y] >= rowSum[y + 1] && rowSum[y] > ink / G * 0.15) peaks.push(y);
  }
  // holes: cells fully surrounded by ink (rough enclosed-area detector)
  let holes = 0;
  for (let y = 2; y < G - 2; y++) for (let x = 2; x < G - 2; x++) {
    if (grid[y * G + x] > 0) continue;
    if (grid[y * G + x - 1] > 0 && grid[y * G + x + 1] > 0 && grid[(y - 1) * G + x] > 0 && grid[(y + 1) * G + x] > 0) holes++;
  }
  return {
    ink, top: top / ink, mid: mid / ink, bot: bot / ink,
    left: left / ink, right: right / ink, width, peaks: peaks.length, holes,
  };
}

// Score each digit class from features using simple rule weights.
function classify(grid) {
  const f = features(grid);
  if (!f) return null;
  const s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  // Heuristic scoring (intentionally transparent, not a black box):
  s[1] += f.top * 1.2 + f.bot * 0.3 + (f.width < 6 ? 1.2 : 0);
  s[7] += f.top * 1.6 + f.bot * 0.1 + (f.peaks === 1 ? 0.8 : 0);
  s[4] += f.mid * 1.4 + (f.peaks >= 2 ? 0.6 : 0);
  s[0] += (f.holes > 2 ? 1.6 : 0) + (Math.abs(f.top - f.bot) < 0.12 ? 0.6 : 0);
  s[6] += (f.holes > 1 ? 0.9 : 0) + f.bot * 1.1;
  s[9] += (f.holes > 1 ? 0.9 : 0) + f.top * 1.1;
  s[8] += (f.holes > 4 ? 1.8 : 0) + f.mid * 0.6;
  s[2] += f.top * 0.8 + f.bot * 0.8 + (f.peaks >= 2 ? 0.5 : 0) + (f.right > f.left ? 0.4 : 0);
  s[3] += f.top * 0.9 + f.bot * 0.9 + (f.peaks >= 2 ? 0.5 : 0) + (f.holes > 1 ? 0.6 : 0);
  s[5] += f.top * 1.0 + f.bot * 0.9 + (f.left > f.right ? 0.4 : 0);
  // normalise to probabilities via softmax
  const mx = Math.max(...s);
  const exps = s.map((v) => Math.exp((v - mx) * 1.6));
  const sum = exps.reduce((a, b) => a + b, 0);
  return exps.map((v) => v / sum);
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const guessBadge = hud.badge('Draw a digit!', '#a3e635');

  let grid = new Float32Array(G * G);
  let drawing = false;
  let probs = null;

  const panel = createPanel(stage, { title: 'Teaching Machines to See' });
  panel.info('Draw a digit (0–9) on the grid. The classifier turns your strokes into pixel numbers, computes features, and outputs a probability for each digit — exactly how a real image classifier works, just smaller.');
  panel.button({ label: 'Clear', icon: 'delete', onClick: () => { grid.fill(0); probs = null; guessBadge.set('Draw a digit!'); } });
  panel.divider();
  const topOut = panel.readout({ label: 'Top guess', value: '—' });
  const confOut = panel.readout({ label: 'Confidence', value: '—' });
  panel.button({ label: 'How does it see?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'From pixels to prediction',
      body: 'Your drawing becomes a grid of numbers (0 = blank, 1 = ink). The classifier measures features — ink at the top, bottom, left, right, the number of enclosed holes — and combines them into a score for each digit. The highest score wins. Real CNNs learn these features automatically from millions of examples.',
      color: '#6366F1',
    });
  } });

  function geom(w, h) {
    const size = Math.min(w * 0.5, h - 80);
    return { x: w * 0.06, y: (h - size) / 2, size: Math.max(120, size) };
  }

  function paintAt(px, py) {
    const g = geom(sim.width, sim.height);
    const cell = g.size / G;
    const gx = Math.floor((px - g.x) / cell);
    const gy = Math.floor((py - g.y) / cell);
    if (gx < 0 || gx >= G || gy < 0 || gy >= G) return;
    // brush with neighbours for smoother strokes
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
      const x = gx + dx, y = gy + dy;
      if (x < 0 || x >= G || y < 0 || y >= G) continue;
      const falloff = (Math.abs(dx) + Math.abs(dy)) === 0 ? 1 : 0.5;
      grid[y * G + x] = Math.min(1, grid[y * G + x] + 0.6 * falloff);
    }
  }
  function onDown(e) {
    drawing = true; const p = pointerPos(sim.canvas, e); paintAt(p.x, p.y);
    if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
  }
  function onMove(e) { if (!drawing) return; const p = pointerPos(sim.canvas, e); paintAt(p.x, p.y); }
  function onUp() { drawing = false; probs = classify(grid); if (probs) {
    let bi = 0; probs.forEach((v, i) => { if (v > probs[bi]) bi = i; });
    guessBadge.set(`Guess: ${bi}`);
    topOut.set(String(bi)); confOut.set(`${Math.round(probs[bi] * 100)}%`);
  } }
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);

  sim.setUpdate((ctx) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#070a14'; ctx.fillRect(0, 0, w, h);
    const g = geom(w, h);
    // draw grid
    const cell = g.size / G;
    ctx.fillStyle = '#0c1226'; ctx.fillRect(g.x, g.y, g.size, g.size);
    ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 1;
    for (let i = 0; i <= G; i++) {
      ctx.beginPath(); ctx.moveTo(g.x + i * cell, g.y); ctx.lineTo(g.x + i * cell, g.y + g.size); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(g.x, g.y + i * cell); ctx.lineTo(g.x + g.size, g.y + i * cell); ctx.stroke();
    }
    // ink
    for (let y = 0; y < G; y++) for (let x = 0; x < G; x++) {
      const v = grid[y * G + x];
      if (v > 0) {
        ctx.fillStyle = `rgba(96,165,250,${v})`;
        ctx.fillRect(g.x + x * cell, g.y + y * cell, cell, cell);
      }
    }
    ctx.strokeStyle = 'rgba(99,102,241,0.5)'; ctx.lineWidth = 2;
    ctx.strokeRect(g.x, g.y, g.size, g.size);

    // probabilities bar chart on the right
    const cx = g.x + g.size + 30; const cy = g.y; const cw = Math.min(w - cx - 16, 260); const ch = g.size;
    panelBg(ctx, cx, cy, cw, ch);
    labelText(ctx, 'Class probabilities', cx + 10, cy + 18, { color: '#9ec1ff', size: 12 });
    const barH = (ch - 36) / 10;
    let topIdx = 0;
    if (probs) probs.forEach((v, i) => { if (v > probs[topIdx]) topIdx = i; });
    for (let d = 0; d < 10; d++) {
      const by = cy + 24 + d * barH;
      labelText(ctx, String(d), cx + 12, by + barH / 2 + 4, { color: '#cbd5e1', size: 12 });
      const p = probs ? probs[d] : 0;
      const bw = (cw - 60) * p;
      ctx.fillStyle = d === topIdx ? '#34d399' : 'rgba(99,102,241,0.4)';
      ctx.fillRect(cx + 30, by + 4, Math.max(2, bw), barH - 8);
      labelText(ctx, `${Math.round(p * 100)}%`, cx + 30 + Math.max(2, bw) + 6, by + barH / 2 + 4,
        { color: '#e2e8f0', size: 11 });
    }
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
