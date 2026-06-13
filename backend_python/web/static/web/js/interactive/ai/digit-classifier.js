import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 5 – Teaching Machines to See
// 8×8 pixel grid drawing → nearest-centroid classifier for digits 0-9
// Also shows edge-detection (Sobel-like) convolution on the drawn grid.

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Draw a digit!', '#6366F1');

  const GRID = 8;  // 8×8 pixels
  const pixels = new Float32Array(GRID * GRID);

  let showEdges = false;
  let predLabel = -1;
  let predScores = new Array(10).fill(0);
  let drawing = false;
  let erasing = false;

  // Hardcoded centroids for digits 0-9 (8×8 bitmap templates, simplified)
  // Each is a 64-element Float32Array of 0/1 values (approximate ideal digit shape)
  function makeTemplate(rows) {
    const t = new Float32Array(64);
    rows.forEach((row, r) => {
      for (let c = 0; c < 8; c++) {
        t[r * 8 + c] = row[c] || 0;
      }
    });
    return t;
  }

  const TEMPLATES = [
    // 0
    makeTemplate([
      [0,1,1,1,1,1,0,0],
      [1,1,0,0,1,1,0,0],
      [1,0,0,0,0,1,0,0],
      [1,0,0,0,0,1,0,0],
      [1,0,0,0,0,1,0,0],
      [1,1,0,0,1,1,0,0],
      [0,1,1,1,1,1,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 1
    makeTemplate([
      [0,0,1,1,0,0,0,0],
      [0,1,1,1,0,0,0,0],
      [0,0,1,1,0,0,0,0],
      [0,0,1,1,0,0,0,0],
      [0,0,1,1,0,0,0,0],
      [0,0,1,1,0,0,0,0],
      [0,1,1,1,1,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 2
    makeTemplate([
      [0,1,1,1,0,0,0,0],
      [1,0,0,0,1,0,0,0],
      [0,0,0,0,1,0,0,0],
      [0,0,0,1,0,0,0,0],
      [0,0,1,0,0,0,0,0],
      [0,1,0,0,0,0,0,0],
      [1,1,1,1,1,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 3
    makeTemplate([
      [0,1,1,1,0,0,0,0],
      [0,0,0,1,1,0,0,0],
      [0,0,0,0,1,0,0,0],
      [0,1,1,1,0,0,0,0],
      [0,0,0,0,1,0,0,0],
      [0,0,0,1,1,0,0,0],
      [0,1,1,1,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 4
    makeTemplate([
      [0,0,0,1,1,0,0,0],
      [0,0,1,0,1,0,0,0],
      [0,1,0,0,1,0,0,0],
      [1,0,0,0,1,0,0,0],
      [1,1,1,1,1,1,0,0],
      [0,0,0,0,1,0,0,0],
      [0,0,0,0,1,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 5
    makeTemplate([
      [1,1,1,1,1,0,0,0],
      [1,0,0,0,0,0,0,0],
      [1,1,1,1,0,0,0,0],
      [0,0,0,0,1,0,0,0],
      [0,0,0,0,1,0,0,0],
      [1,0,0,0,1,0,0,0],
      [0,1,1,1,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 6
    makeTemplate([
      [0,0,1,1,1,0,0,0],
      [0,1,0,0,0,0,0,0],
      [1,0,0,0,0,0,0,0],
      [1,1,1,1,0,0,0,0],
      [1,0,0,0,1,0,0,0],
      [1,0,0,0,1,0,0,0],
      [0,1,1,1,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 7
    makeTemplate([
      [1,1,1,1,1,0,0,0],
      [0,0,0,0,1,0,0,0],
      [0,0,0,1,0,0,0,0],
      [0,0,1,0,0,0,0,0],
      [0,0,1,0,0,0,0,0],
      [0,1,0,0,0,0,0,0],
      [0,1,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 8
    makeTemplate([
      [0,1,1,1,0,0,0,0],
      [1,0,0,0,1,0,0,0],
      [1,0,0,0,1,0,0,0],
      [0,1,1,1,0,0,0,0],
      [1,0,0,0,1,0,0,0],
      [1,0,0,0,1,0,0,0],
      [0,1,1,1,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
    // 9
    makeTemplate([
      [0,1,1,1,0,0,0,0],
      [1,0,0,0,1,0,0,0],
      [1,0,0,0,1,0,0,0],
      [0,1,1,1,1,0,0,0],
      [0,0,0,0,1,0,0,0],
      [0,0,0,1,0,0,0,0],
      [0,1,1,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]),
  ];

  // Cosine similarity classifier
  function classify() {
    const norm = Math.sqrt(pixels.reduce((s, v) => s + v * v, 0));
    if (norm < 0.5) { predLabel = -1; predScores.fill(0); return; }
    predScores = TEMPLATES.map((tmpl) => {
      const dot = pixels.reduce((s, v, i) => s + v * tmpl[i], 0);
      const tn = Math.sqrt(tmpl.reduce((s, v) => s + v * v, 0));
      return dot / (norm * tn + 1e-8);
    });
    predLabel = predScores.indexOf(Math.max(...predScores));
  }

  // Sobel edge detection on pixel grid
  function edgeMap() {
    const edges = new Float32Array(GRID * GRID);
    const Kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];
    const Ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]];
    for (let r = 1; r < GRID - 1; r++) {
      for (let c = 1; c < GRID - 1; c++) {
        let gx = 0, gy = 0;
        for (let kr = -1; kr <= 1; kr++) {
          for (let kc = -1; kc <= 1; kc++) {
            const v = pixels[(r + kr) * GRID + (c + kc)];
            gx += v * Kx[kr + 1][kc + 1];
            gy += v * Ky[kr + 1][kc + 1];
          }
        }
        edges[r * GRID + c] = Math.min(1, Math.sqrt(gx * gx + gy * gy) / 2);
      }
    }
    return edges;
  }

  const panel = createPanel(stage, { title: 'Classifier' });
  panel.toggle({ label: 'Show edge detection', value: false, onChange: (v) => { showEdges = v; } });
  panel.divider();
  const predOut = panel.readout({ label: 'Prediction', value: '—' });
  const confOut = panel.readout({ label: 'Confidence', value: '—' });
  panel.button({ label: 'Clear', icon: 'delete', onClick: () => { pixels.fill(0); predLabel = -1; predScores.fill(0); } });
  panel.info('Draw a digit (0-9) on the 8×8 grid. Left-click draws, right-click erases. Toggle "edge detection" to see how a CNN kernel finds outlines.');

  function getCell(e) {
    const rect = sim.canvas.getBoundingClientRect();
    const p = { x: e.clientX - rect.left, y: e.clientY - rect.top };
    const w = sim.width, h = sim.height;
    const gridSize = Math.min(w * 0.55, h - 60);
    const gx0 = 20, gy0 = (h - gridSize) / 2;
    const col = Math.floor((p.x - gx0) / (gridSize / GRID));
    const row = Math.floor((p.y - gy0) / (gridSize / GRID));
    return { col, row, valid: col >= 0 && col < GRID && row >= 0 && row < GRID };
  }

  function paint(e) {
    const { col, row, valid } = getCell(e);
    if (!valid) return;
    pixels[row * GRID + col] = erasing ? 0 : 1;
    classify();
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('contextmenu', (e) => e.preventDefault());
  sim.canvas.addEventListener('pointerdown', (e) => {
    drawing = true;
    erasing = e.button === 2 || e.buttons === 2;
    paint(e);
    sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
  });
  sim.canvas.addEventListener('pointermove', (e) => { if (drawing) paint(e); });
  sim.canvas.addEventListener('pointerup', () => { drawing = false; });
  sim.canvas.addEventListener('pointercancel', () => { drawing = false; });

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);

    const gridSize = Math.min(w * 0.55, h - 60);
    const cellPx = gridSize / GRID;
    const gx0 = 20, gy0 = (h - gridSize) / 2;

    // Pixel grid or edge map
    const display = showEdges ? edgeMap() : pixels;
    for (let r = 0; r < GRID; r++) {
      for (let c = 0; c < GRID; c++) {
        const v = display[r * GRID + c];
        if (showEdges) {
          ctx.fillStyle = `rgba(245,158,11,${v * 0.9 + 0.05})`;
        } else {
          ctx.fillStyle = v > 0.5 ? '#e0e7ff' : 'rgba(30,40,80,0.6)';
        }
        ctx.fillRect(gx0 + c * cellPx + 1, gy0 + r * cellPx + 1, cellPx - 2, cellPx - 2);
      }
    }

    // Grid lines
    ctx.strokeStyle = 'rgba(165,180,252,0.25)'; ctx.lineWidth = 1;
    for (let i = 0; i <= GRID; i++) {
      ctx.beginPath(); ctx.moveTo(gx0 + i * cellPx, gy0); ctx.lineTo(gx0 + i * cellPx, gy0 + gridSize); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(gx0, gy0 + i * cellPx); ctx.lineTo(gx0 + gridSize, gy0 + i * cellPx); ctx.stroke();
    }

    // Label
    ctx.fillStyle = 'rgba(199,212,234,0.7)'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'center';
    ctx.fillText(showEdges ? 'Edge detection (Sobel filter)' : 'Draw here (8×8 pixels)', gx0 + gridSize / 2, gy0 - 8);

    // Prediction display
    const barX = gx0 + gridSize + 20;
    const barW = w - barX - 16;
    if (barW > 50) {
      ctx.fillStyle = 'rgba(199,212,234,0.8)'; ctx.font = 'bold 13px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('Class scores:', barX, gy0 + 10);
      const barH = (gridSize - 20) / 10 - 4;
      for (let d = 0; d < 10; d++) {
        const by = gy0 + 20 + d * (barH + 6);
        const score = predScores[d] || 0;
        const isTop = d === predLabel;
        ctx.fillStyle = isTop ? 'rgba(245,158,11,0.2)' : 'rgba(99,102,241,0.1)';
        ctx.fillRect(barX, by, barW, barH);
        ctx.fillStyle = isTop ? '#F59E0B' : '#6366F1';
        ctx.fillRect(barX, by, Math.max(0, score) * barW, barH);
        ctx.fillStyle = '#e8eefb'; ctx.font = `${isTop ? 'bold' : 'normal'} 11px Poppins,sans-serif`;
        ctx.textAlign = 'left';
        ctx.fillText(`${d}  ${(score * 100).toFixed(0)}%`, barX + 4, by + barH - 3);
      }

      if (predLabel >= 0) {
        ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 32px Poppins,sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(String(predLabel), barX + barW / 2, gy0 + gridSize + 28);
        predOut.set(String(predLabel));
        confOut.set(`${(predScores[predLabel] * 100).toFixed(0)}%`);
        badge.set(`Looks like a "${predLabel}"!`);
      } else {
        predOut.set('—'); confOut.set('—');
        badge.set('Draw a digit…');
      }
    }

    // Convolution kernel visualization
    if (showEdges) {
      const kx0 = gx0, ky0 = gy0 + gridSize + 14;
      const ks = 18;
      const Kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];
      ctx.fillStyle = 'rgba(199,212,234,0.6)'; ctx.font = '10px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('Sobel kernel Kx:', kx0, ky0 + 10);
      for (let kr = 0; kr < 3; kr++) {
        for (let kc = 0; kc < 3; kc++) {
          const v = Kx[kr][kc];
          ctx.fillStyle = v > 0 ? 'rgba(99,102,241,0.7)' : v < 0 ? 'rgba(245,158,11,0.7)' : 'rgba(50,60,100,0.7)';
          ctx.fillRect(kx0 + kc * ks + 90, ky0, ks - 1, ks - 1);
          ctx.fillStyle = '#fff'; ctx.font = '10px monospace'; ctx.textAlign = 'center';
          ctx.fillText(String(v), kx0 + kc * ks + 90 + ks / 2, ky0 + 12 + kr * ks);
        }
      }
    }
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', () => {});
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
