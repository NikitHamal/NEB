import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { fmt, panelBg, labelText, drawTable, microscopeVignette } from './bio-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const focusBadge = hud.badge('Focus: 0%', '#9ec1ff');
  hud.badge('Lower epidermis · 100×', '#65A30D');

  let focus = 50;
  let surface = 'lower'; // 'lower' or 'upper'
  let panX = 0; let panY = 0;

  const FIELD_W = 1200; const FIELD_H = 800;
  let epidermal = [];
  let stomata = [];

  function generateField() {
    epidermal = [];
    stomata = [];
    // jigsaw epidermal cells
    const cellR = 38;
    for (let x = 0; x < FIELD_W; x += cellR * 1.6) {
      for (let y = 0; y < FIELD_H; y += cellR * 1.4) {
        epidermal.push({
          x: x + (y % (cellR * 2.8) < cellR * 1.4 ? cellR * 0.8 : 0) + (Math.random() * 8 - 4),
          y: y + (Math.random() * 8 - 4),
          r: cellR + (Math.random() * 6 - 3),
          wob: Array.from({ length: 10 }, () => 0.85 + Math.random() * 0.3),
        });
      }
    }
    // stomata scattered — more on lower surface
    const density = surface === 'lower' ? 0.0016 : 0.00035; // per px²
    const n = Math.floor(FIELD_W * FIELD_H * density);
    for (let i = 0; i < n; i++) {
      stomata.push({
        x: 60 + Math.random() * (FIELD_W - 120),
        y: 60 + Math.random() * (FIELD_H - 120),
        open: 0.4 + Math.random() * 0.5,
        rot: Math.random() * Math.PI,
        len: 16 + Math.random() * 6,
        counted: false,
      });
    }
  }
  generateField();

  let countedCount = 0;
  let fieldArea = 0; // mm²

  const panel = createPanel(stage, { title: 'Leaf Peel — Stomata' });
  panel.info('Focus the microscope on the leaf peel, then tap each stoma (the tiny pairs of guard cells) to count it. Compare upper vs lower surfaces.');
  panel.slider({
    label: 'Focus', min: 0, max: 100, step: 1, value: 50,
    format: (v) => `${v}%`,
    onChange: (v) => { focus = v; },
  });
  panel.select({
    label: 'Surface', value: 'lower',
    options: [{ value: 'lower', label: 'Lower epidermis' }, { value: 'upper', label: 'Upper epidermis' }],
    onChange: (v) => { surface = v; countedCount = 0; stomata.forEach((s) => s.counted = false); generateField(); recompute(); },
  });
  panel.buttonRow([
    { label: '←', icon: 'arrow_back', onClick: () => { panX -= 90; } },
    { label: '→', icon: 'arrow_forward', onClick: () => { panX += 90; } },
  ]);
  panel.buttonRow([
    { label: '↑', icon: 'arrow_upward', onClick: () => { panY -= 90; } },
    { label: '↓', icon: 'arrow_downward', onClick: () => { panY += 90; } },
  ]);
  panel.button({ label: 'New peel', icon: 'refresh', onClick: () => {
    countedCount = 0; generateField(); recompute(); focus = 50; panX = 0; panY = 0;
  } });
  panel.divider();
  const countedOut = panel.readout({ label: 'Stomata in view', value: '0' });
  const densityOut = panel.readout({ label: 'Density (per mm²)', value: '—' });
  panel.button({ label: 'Why count both surfaces?', icon: 'help', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Upper vs lower',
      body: 'Most land plants keep far more stomata on the lower surface, out of direct sun, to cut water loss. Water lilies flip this — stomata only on top, so they can breathe while floating.',
      color: '#65A30D',
    });
  } });

  function recompute() {
    countedOut.set(String(countedCount));
    // Assume field of view at 100× is ~1.8 mm diameter → area ~2.5 mm². We approximate by stomata in view.
    const area = 2.5;
    fieldArea = area;
    densityOut.set(fmt(countedCount / area, 0));
  }
  recompute();

  function viewGeo(w, h) {
    const r = Math.min(w, h) * 0.42;
    return { cx: w / 2, cy: h / 2, r };
  }

  function onTap(e) {
    const p = pointerPos(sim.canvas, e);
    const g = viewGeo(sim.width, sim.height);
    if (Math.hypot(p.x - g.cx, p.y - g.cy) > g.r) return;
    let best = null; let bestD = 30;
    stomata.forEach((s) => {
      const sx = s.x + g.cx - panX - FIELD_W / 2;
      const sy = s.y + g.cy - panY - FIELD_H / 2;
      const d = Math.hypot(p.x - sx, p.y - sy);
      if (d < bestD) { bestD = d; best = s; }
    });
    if (best) {
      if (!best.counted) { best.counted = true; countedCount++; recompute(); }
      showInfoCard(stage, {
        title: 'Stoma (counted)',
        body: `A pore between two guard cells. This one is ${best.open > 0.7 ? 'open' : best.open > 0.4 ? 'partly open' : 'mostly closed'} — ${fmt(best.len * 2, 1)} μm long. ${best.counted ? '' : ''}`,
        color: '#84CC16',
      });
    } else {
      showInfoCard(stage, {
        title: 'Epidermal cell',
        body: 'A jigsaw-shaped pavement cell of the leaf epidermis. Look for pairs of bean-shaped guard cells with a slit between them — those are the stomata.',
        color: '#84CC16',
      });
    }
  }
  sim.canvas.addEventListener('pointerdown', onTap);

  sim.setUpdate((ctx) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    const g = viewGeo(w, h);
    ctx.fillStyle = '#05080f'; ctx.fillRect(0, 0, w, h);

    ctx.save();
    ctx.beginPath(); ctx.arc(g.cx, g.cy, g.r, 0, Math.PI * 2); ctx.clip();
    ctx.fillStyle = '#13351c'; ctx.fillRect(g.cx - g.r, g.cy - g.r, g.r * 2, g.r * 2);

    const defocus = Math.abs(focus - 50) / 50;
    const blur = defocus * 3;

    // epidermal cells (jigsaw)
    epidermal.forEach((c) => {
      const sx = c.x + g.cx - panX - FIELD_W / 2;
      const sy = c.y + g.cy - panY - FIELD_H / 2;
      if (Math.hypot(sx - g.cx, sy - g.cy) > g.r + c.r) return;
      ctx.save();
      ctx.translate(sx + blur * (Math.random() - 0.5), sy + blur * (Math.random() - 0.5));
      ctx.fillStyle = 'rgba(120,180,90,0.18)';
      ctx.strokeStyle = 'rgba(180,220,140,0.4)'; ctx.lineWidth = 1.2;
      ctx.beginPath();
      for (let i = 0; i <= 10; i++) {
        const a = (i / 10) * Math.PI * 2;
        const rr = c.r * c.wob[i % 10];
        const px = Math.cos(a) * rr; const py = Math.sin(a) * rr;
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.restore();
    });

    // stomata
    stomata.forEach((s) => {
      const sx = s.x + g.cx - panX - FIELD_W / 2;
      const sy = s.y + g.cy - panY - FIELD_H / 2;
      if (Math.hypot(sx - g.cx, sy - g.cy) > g.r + 30) return;
      ctx.save();
      ctx.translate(sx, sy);
      ctx.rotate(s.rot);
      // two guard cells (bean shapes) around a pore
      const len = s.len; const openW = len * 0.35 * s.open;
      ctx.fillStyle = '#6fae4a';
      // left guard cell
      drawBean(ctx, -len * 0.55, 0, len * 0.9, len * 0.45, 0);
      // right guard cell
      drawBean(ctx, len * 0.55, 0, len * 0.9, len * 0.45, Math.PI);
      // pore (the stoma itself)
      ctx.fillStyle = '#0a1a0a';
      ctx.beginPath();
      ctx.ellipse(0, 0, len * 0.25, openW, 0, 0, Math.PI * 2); ctx.fill();
      // counted ring
      if (s.counted) {
        ctx.strokeStyle = '#a3e635'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(0, 0, len * 1.3, 0, Math.PI * 2); ctx.stroke();
      }
      ctx.restore();
    });

    ctx.restore();

    microscopeVignette(ctx, g.cx, g.cy, g.r);
    ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(g.cx - 8, g.cy); ctx.lineTo(g.cx + 8, g.cy);
    ctx.moveTo(g.cx, g.cy - 8); ctx.lineTo(g.cx, g.cy + 8); ctx.stroke();

    const fpct = Math.round(100 - defocus * 100);
    focusBadge.set(`Focus: ${fpct}%`);
    focusBadge.el.style.setProperty('--ix-hud-color', fpct > 80 ? '#a3e635' : '#fbbf24');

    // table
    drawTable(ctx, {
      x: 12, y: h - 110, w: 210, title: 'Observations',
      cols: ['Quantity', 'Value'],
      rows: [
        ['Surface', surface === 'lower' ? 'Lower' : 'Upper'],
        ['Stomata counted', countedCount],
        ['FOV area', `${fmt(fieldArea, 2)} mm²`],
        ['Density', `${fmt(countedCount / fieldArea, 0)} /mm²`],
      ],
      accent: '#84CC16',
    });
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onTap);
      panel.dispose(); hud.dispose(); sim.dispose();
    },
  };
}

function drawBean(ctx, cx, cy, w, h, rot) {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(rot);
  ctx.beginPath();
  ctx.ellipse(0, 0, w * 0.5, h, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}
