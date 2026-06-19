import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { fmt, panelBg, labelText, drawTable, microscopeVignette } from './bio-utils.js';

// Phase definitions: how to draw each, and a relative time-weight so we spawn the right proportion.
// Weights approx: interphase ~80%, prophase ~8%, metaphase ~4%, anaphase ~2%, telophase ~6%.
const PHASES = [
  { id: 'interphase', name: 'Interphase', short: 'I', color: '#9ccc65', weight: 0.62,
    drawCell: drawInterphase },
  { id: 'prophase', name: 'Prophase', short: 'P', color: '#ffb74d', weight: 0.16,
    drawCell: drawProphase },
  { id: 'metaphase', name: 'Metaphase', short: 'M', color: '#4fc3f7', weight: 0.07,
    drawCell: drawMetaphase },
  { id: 'anaphase', name: 'Anaphase', short: 'A', color: '#f06292', weight: 0.05,
    drawCell: drawAnaphase },
  { id: 'telophase', name: 'Telophase', short: 'T', color: '#ba68c8', weight: 0.10,
    drawCell: drawTelophase },
];
const PHASE_MAP = Object.fromEntries(PHASES.map((p) => [p.id, p]));

function pickPhase() {
  const r = Math.random();
  let acc = 0;
  for (const p of PHASES) { acc += p.weight; if (r < acc) return p.id; }
  return 'interphase';
}

// ---- Cell drawing helpers (work in local coords centred at 0,0, scale s) ----
function nucleus(ctx, cx, cy, r, color) {
  ctx.fillStyle = 'rgba(120,80,90,0.35)';
  ctx.beginPath(); ctx.arc(cx, cy, r + 1.5, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = color; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
}
function drawInterphase(ctx, s) {
  nucleus(ctx, 0, 0, s * 0.32, 'rgba(150,90,100,0.55)');
  ctx.fillStyle = 'rgba(255,255,255,0.25)';
  for (let i = 0; i < 3; i++) {
    ctx.beginPath(); ctx.arc((Math.random() - 0.5) * s, (Math.random() - 0.5) * s, s * 0.04, 0, Math.PI * 2); ctx.fill();
  }
}
function drawProphase(ctx, s) {
  // tangled chromosomes inside intact nucleus
  nucleus(ctx, 0, 0, s * 0.36, 'rgba(120,60,70,0.25)');
  ctx.strokeStyle = '#7b1fa2'; ctx.lineWidth = Math.max(1, s * 0.05);
  for (let i = 0; i < 5; i++) {
    const a = Math.random() * Math.PI * 2;
    ctx.beginPath();
    ctx.moveTo(Math.cos(a) * s * 0.1, Math.sin(a) * s * 0.1);
    ctx.bezierCurveTo(
      Math.cos(a + 1) * s * 0.3, Math.sin(a + 1) * s * 0.3,
      Math.cos(a + 2) * s * 0.3, Math.sin(a + 2) * s * 0.3,
      Math.cos(a + 3) * s * 0.28, Math.sin(a + 3) * s * 0.28
    );
    ctx.stroke();
  }
}
function drawMetaphase(ctx, s) {
  // chromosomes lined at equator
  ctx.fillStyle = '#1565c0';
  const n = 6;
  for (let i = 0; i < n; i++) {
    const x = (i - (n - 1) / 2) * s * 0.1;
    ctx.beginPath();
    ctx.ellipse(x, 0, s * 0.05, s * 0.1, 0, 0, Math.PI * 2); ctx.fill();
  }
  // faint spindle
  ctx.strokeStyle = 'rgba(255,255,255,0.3)'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(-s * 0.4, 0); ctx.lineTo(s * 0.4, 0); ctx.stroke();
}
function drawAnaphase(ctx, s) {
  // two V-shaped groups pulled to poles
  ctx.fillStyle = '#c2185b';
  [-1, 1].forEach((dir) => {
    for (let i = 0; i < 4; i++) {
      const x = dir * s * (0.25 + i * 0.04);
      ctx.beginPath();
      ctx.ellipse(x, 0, s * 0.045, s * 0.07, 0, 0, Math.PI * 2); ctx.fill();
    }
  });
  ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(-s * 0.45, 0); ctx.lineTo(s * 0.45, 0); ctx.stroke();
}
function drawTelophase(ctx, s) {
  // two new nuclei forming at ends, pinching middle
  [-1, 1].forEach((dir) => {
    nucleus(ctx, dir * s * 0.28, 0, s * 0.18, 'rgba(150,90,180,0.6)');
  });
  ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(0, -s * 0.45); ctx.lineTo(0, s * 0.45); ctx.stroke();
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const focusBadge = hud.badge('Focus: 0%', '#9ec1ff');
  hud.badge('Onion root tip · 400×', '#65A30D');

  // Microscope focus: 0..100, correct = 50. Defocus blurs cells.
  let focus = 50;
  // Pan position (root tip is wider than field of view)
  let panX = 0; let panY = 0;
  // Field cells: generated across a wider area; we render those in view.
  const FIELD_W = 1400; const FIELD_H = 900;
  const cells = [];
  function generateField() {
    cells.length = 0;
    const spacing = 70;
    for (let x = 0; x < FIELD_W; x += spacing + (Math.random() * 20 - 10)) {
      for (let y = 0; y < FIELD_H; y += spacing + (Math.random() * 20 - 10)) {
        cells.push({
          x: x + (Math.random() - 0.5) * 25,
          y: y + (Math.random() - 0.5) * 25,
          r: 26 + Math.random() * 8,
          phase: pickPhase(),
          rot: Math.random() * Math.PI,
        });
      }
    }
  }
  generateField();

  // Counting tally
  const counts = { interphase: 0, prophase: 0, metaphase: 0, anaphase: 0, telophase: 0 };
  const counted = new Set();

  const panel = createPanel(stage, { title: 'Onion Root Tip — Mitosis' });
  panel.info('Focus the microscope, then scan the root tip. Tap any cell to identify and tally its phase. Aim for ~100 cells counted.');
  panel.slider({
    label: 'Coarse focus', min: 0, max: 100, step: 1, value: 50,
    format: (v) => `${v}%`,
    onChange: (v) => { focus = v; },
  });
  panel.buttonRow([
    { label: '← Pan', icon: 'arrow_back', onClick: () => { panX -= 90; } },
    { label: 'Pan →', icon: 'arrow_forward', onClick: () => { panX += 90; } },
  ]);
  panel.buttonRow([
    { label: '↑ Pan', icon: 'arrow_upward', onClick: () => { panY -= 90; } },
    { label: '↓ Pan', icon: 'arrow_downward', onClick: () => { panY += 90; } },
  ]);
  panel.button({ label: 'New slide', icon: 'refresh', onClick: () => {
    generateField(); Object.keys(counts).forEach((k) => counts[k] = 0); counted.clear(); panX = 0; panY = 0; focus = 50;
    showInfoCard(stage, { title: 'Fresh slide prepared', body: 'A new onion root tip squash, stained with aceto-orcein. Refocus and count again.', color: '#65A30D' });
  } });
  panel.divider();
  const totalOut = panel.readout({ label: 'Cells counted', value: '0' });
  const indexOut = panel.readout({ label: 'Mitotic index', value: '—' });
  panel.button({ label: 'How is the index calculated?', icon: 'help', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Mitotic index',
      body: 'Mitotic index = (cells in prophase + metaphase + anaphase + telophase) ÷ total cells counted × 100%. It measures how actively a tissue is dividing. For an onion root tip expect roughly 5–10%.',
      color: '#65A30D',
    });
  } });

  function recompute() {
    const total = counts.interphase + counts.prophase + counts.metaphase + counts.anaphase + counts.telophase;
    const dividing = counts.prophase + counts.metaphase + counts.anaphase + counts.telophase;
    totalOut.set(String(total));
    indexOut.set(total > 0 ? `${fmt((dividing / total) * 100, 1)}%` : '—');
  }

  function viewGeo(w, h) {
    const r = Math.min(w, h) * 0.42;
    return { cx: w / 2, cy: h / 2, r, fovLeft: w / 2 - r, fovTop: h / 2 - r, fovW: r * 2, fovH: r * 2 };
  }

  // Tap a cell to tally
  function onTap(e) {
    const p = pointerPos(sim.canvas, e);
    const g = viewGeo(sim.width, sim.height);
    if (Math.hypot(p.x - g.cx, p.y - g.cy) > g.r) return;
    // find closest cell in view
    let best = null; let bestD = 40;
    cells.forEach((c, i) => {
      const sx = c.x + g.cx - panX - FIELD_W / 2;
      const sy = c.y + g.cy - panY - FIELD_H / 2;
      const d = Math.hypot(p.x - sx, p.y - sy);
      if (d < bestD && d < c.r + 6) { bestD = d; best = { c, i }; }
    });
    if (!best) return;
    const c = best.c;
    if (!counted.has(best.i)) {
      counts[c.phase]++; counted.add(best.i); recompute();
    }
    const ph = PHASE_MAP[c.phase];
    showInfoCard(stage, { title: `${ph.name} (counted)`, body: `${phHint(c.phase)} — added to your tally.`, color: ph.color });
  }
  sim.canvas.addEventListener('pointerdown', onTap);

  recompute();

  sim.setUpdate((ctx, dt) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    const g = viewGeo(w, h);

    // Slide background (outside the circular field)
    ctx.fillStyle = '#05080f'; ctx.fillRect(0, 0, w, h);

    // Field of view: clip to circle
    ctx.save();
    ctx.beginPath(); ctx.arc(g.cx, g.cy, g.r, 0, Math.PI * 2); ctx.clip();

    // stain background
    ctx.fillStyle = '#3a1a22';
    ctx.fillRect(g.fovLeft, g.fovTop, g.fovW, g.fovH);

    // Defocus blur: scale of chromatin wobble
    const defocus = Math.abs(focus - 50) / 50; // 0..1
    const blurPx = defocus * 4;

    cells.forEach((c) => {
      const sx = c.x + g.cx - panX - FIELD_W / 2;
      const sy = c.y + g.cy - panY - FIELD_H / 2;
      // cull cells outside fov
      if (Math.hypot(sx - g.cx, sy - g.cy) > g.r + c.r + 10) return;
      ctx.save();
      ctx.translate(sx, sy);
      ctx.rotate(c.rot);
      // cell wall
      ctx.fillStyle = 'rgba(60,30,30,0.45)';
      ctx.strokeStyle = 'rgba(255,200,200,0.25)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(0, 0, c.r, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      // chromosomes / nucleus
      ctx.translate(blurPx * (Math.random() - 0.5), blurPx * (Math.random() - 0.5));
      PHASE_MAP[c.phase].drawCell(ctx, c.r * 0.85);
      // counted marker
      ctx.restore();
    });

    ctx.restore();

    // Vignette + reticle
    microscopeVignette(ctx, g.cx, g.cy, g.r);
    ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(g.cx - 8, g.cy); ctx.lineTo(g.cx + 8, g.cy);
    ctx.moveTo(g.cx, g.cy - 8); ctx.lineTo(g.cx, g.cy + 8); ctx.stroke();

    // Badges update
    const fpct = Math.round(100 - defocus * 100);
    focusBadge.set(`Focus: ${fpct}%`);
    focusBadge.el.style.setProperty('--ix-hud-color', fpct > 80 ? '#a3e635' : '#fbbf24');

    // Counting table overlay
    const tableX = 12; const tableY = h - 168; const tableW = 210;
    const rows = PHASES.map((p) => [p.short, counts[p.id]]);
    drawTable(ctx, { x: tableX, y: tableY, w: tableW, title: 'Phase count', cols: ['Phase', 'n'], rows, accent: '#84CC16' });
    const total = counts.interphase + counts.prophase + counts.metaphase + counts.anaphase + counts.telophase;
    const dividing = counts.prophase + counts.metaphase + counts.anaphase + counts.telophase;
    const idx = total > 0 ? fmt((dividing / total) * 100, 1) + '%' : '—';
    labelText(ctx, `Mitotic index: ${idx}`, tableX, tableY + 168, { color: '#a3e635', size: 12 });
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onTap);
      panel.dispose(); hud.dispose(); sim.dispose();
    },
  };
}

function phHint(phase) {
  return {
    interphase: 'Nucleus intact and grainy — the cell is growing, not dividing',
    prophase: 'Chromosomes condensing into visible threads; nuclear membrane fading',
    metaphase: 'Chromosomes lined up at the cell equator',
    anaphase: 'Chromosomes pulled apart toward opposite poles',
    telophase: 'Two new nuclei forming; cell pinching in the middle',
  }[phase];
}
