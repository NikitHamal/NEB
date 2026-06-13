import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const LY = 9.461e15;
const OBJECTS = [
  { name: 'Mt. Everest', size: 8.8e3, color: '#cdd9ec', type: 'mountain', label: '8,849 m tall' },
  { name: 'Earth', size: 1.27e7, color: '#4d9fff', type: 'planet', label: '12,742 km wide' },
  { name: 'Moon\u2019s orbit', size: 7.7e8, color: '#9aa7bd', type: 'orbit', label: '770,000 km wide' },
  { name: 'The Sun', size: 1.39e9, color: '#ffd27a', type: 'star', label: '1.39 million km wide' },
  { name: 'Earth\u2019s orbit', size: 3.0e11, color: '#7dd3fc', type: 'orbit', label: '2 AU wide' },
  { name: 'Solar System', size: 9.0e12, color: '#a5b4fc', type: 'orbit', label: 'Neptune\u2019s orbit \u2014 60 AU' },
  { name: 'One light-year', size: LY, color: '#8be9a8', type: 'orbit', label: '9.46 trillion km' },
  { name: 'To Proxima Centauri', size: 8.0e16, color: '#f9a8d4', type: 'orbit', label: 'nearest star \u2014 4.2 ly' },
  { name: 'Milky Way', size: 9.5e20, color: '#c4b5fd', type: 'galaxy', label: '100,000 ly across' },
  { name: 'Local Group', size: 9.5e22, color: '#94a8d0', type: 'group', label: '~10 million ly' },
  { name: 'Observable Universe', size: 8.8e26, color: '#7c8db0', type: 'universe', label: '93 billion ly' },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);

  let exp = 4.4;
  let targetExp = 4.4;
  const minExp = 3.9;
  const maxExp = 27.2;
  let pinch = null;
  let viewMode = '2d';

  const hud = createHud(stage);
  const scaleBadge = hud.badge('View width: 10\u2074 m', '#8be9a8');
  const nameBadge = hud.badge('Mt. Everest \u2014 Sagarmatha', '#cdd9ec');

  const panel = createPanel(stage, { title: 'Cosmic Zoom' });
  panel.select({
    label: 'View',
    options: [
      { value: '2d', label: '2D' },
      { value: '3d', label: '3D' },
    ],
    value: viewMode,
    onChange: (v) => { viewMode = v; },
  });
  const zoomSlider = panel.slider({
    label: 'Zoom (powers of ten)',
    min: minExp, max: maxExp, step: 0.05, value: exp,
    format: (v) => `10^${v.toFixed(1)} m`,
    onChange: (v) => { targetExp = v; },
  });
  panel.buttonRow([
    { label: 'Everest', onClick: () => { targetExp = 4.4; zoomSlider.set(4.4); } },
    { label: 'Earth', onClick: () => { targetExp = 7.5; zoomSlider.set(7.5); } },
  ]);
  panel.buttonRow([
    { label: 'Solar Sys', onClick: () => { targetExp = 13.4; zoomSlider.set(13.4); } },
    { label: 'Galaxy', onClick: () => { targetExp = 21.4; zoomSlider.set(21.4); } },
    { label: 'Universe', onClick: () => { targetExp = 27.2; zoomSlider.set(27.2); } },
  ]);
  panel.info('Slide to zoom out from the summit of Everest to the edge of everything. Each whole step is 10\u00d7 bigger. You can also scroll or pinch on the view.');

  function onWheel(e) {
    e.preventDefault();
    targetExp = Math.max(minExp, Math.min(maxExp, targetExp + (e.deltaY > 0 ? 0.35 : -0.35)));
    zoomSlider.set(Math.round(targetExp * 20) / 20);
  }
  const pointers = new Map();
  function onDown(e) {
    sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
    pointers.set(e.pointerId, pointerPos(sim.canvas, e));
    if (pointers.size === 2) {
      const pts = [...pointers.values()];
      pinch = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
    }
  }
  function onMove(e) {
    if (!pointers.has(e.pointerId)) return;
    pointers.set(e.pointerId, pointerPos(sim.canvas, e));
    if (pointers.size === 2 && pinch) {
      const pts = [...pointers.values()];
      const d = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      targetExp = Math.max(minExp, Math.min(maxExp, targetExp + (pinch - d) * 0.012));
      pinch = d;
      zoomSlider.set(Math.round(targetExp * 20) / 20);
    }
  }
  function onUp(e) {
    pointers.delete(e.pointerId);
    if (pointers.size < 2) pinch = null;
  }
  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('wheel', onWheel, { passive: false });
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function fmtScale(width) {
    if (width >= LY * 0.1) {
      const ly = width / LY;
      if (ly >= 1e9) return `${(ly / 1e9).toFixed(1)} billion light-years`;
      if (ly >= 1e6) return `${(ly / 1e6).toFixed(1)} million light-years`;
      if (ly >= 1000) return `${Math.round(ly).toLocaleString()} light-years`;
      return `${ly.toFixed(1)} light-years`;
    }
    if (width >= 1e9) return `${(width / 1e9).toFixed(1)} million km`;
    if (width >= 1e6) return `${(width / 1e6).toFixed(1)} thousand km`;
    if (width >= 1000) return `${(width / 1000).toFixed(1)} km`;
    return `${Math.round(width)} m`;
  }

  function superscript(n) {
    const map = { '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3', '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079', '.': '\u00b7' };
    return String(n).split('').map((c) => map[c] || c).join('');
  }

  function drawObject(ctx, o, cx, cy, dpx, t) {
    const r = dpx / 2;
    const is3d = viewMode === '3d';
    if (o.type === 'mountain') {
      ctx.fillStyle = '#5d6b80';
      ctx.beginPath();
      ctx.moveTo(cx - r, cy + r * 0.7);
      ctx.lineTo(cx, cy - r * 0.7);
      ctx.lineTo(cx + r, cy + r * 0.7);
      ctx.closePath();
      ctx.fill();
      if (is3d) {
        ctx.fillStyle = '#46546a';
        ctx.beginPath();
        ctx.moveTo(cx + r, cy + r * 0.7);
        ctx.lineTo(cx + r * 1.18, cy + r * 0.52);
        ctx.lineTo(cx + r * 0.18, cy - r * 0.86);
        ctx.lineTo(cx, cy - r * 0.7);
        ctx.closePath();
        ctx.fill();
      }
      ctx.fillStyle = '#e8eefb';
      ctx.beginPath();
      ctx.moveTo(cx - r * 0.28, cy - r * 0.31);
      ctx.lineTo(cx, cy - r * 0.7);
      ctx.lineTo(cx + r * 0.28, cy - r * 0.31);
      ctx.closePath();
      ctx.fill();
    } else if (o.type === 'planet') {
      if (is3d) {
        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.beginPath();
        ctx.ellipse(cx + r * 0.12, cy + r * 0.72, r * 0.72, r * 0.14, 0, 0, Math.PI * 2);
        ctx.fill();
        const pg = ctx.createRadialGradient(cx - r * 0.35, cy - r * 0.4, r * 0.12, cx, cy, r);
        pg.addColorStop(0, '#ffffff');
        pg.addColorStop(0.2, o.color);
        pg.addColorStop(1, '#18344f');
        ctx.fillStyle = pg;
      } else {
        ctx.fillStyle = o.color;
      }
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.fill();
      if (r > 8) {
        ctx.fillStyle = 'rgba(63,174,106,0.7)';
        ctx.beginPath();
        ctx.ellipse(cx - r * 0.25, cy - r * 0.15, r * 0.4, r * 0.28, 0.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(cx + r * 0.3, cy + r * 0.3, r * 0.3, r * 0.2, -0.4, 0, Math.PI * 2);
        ctx.fill();
      }
    } else if (o.type === 'star') {
      const g = ctx.createRadialGradient(cx, cy, r * 0.3, cx, cy, r * 2.2);
      g.addColorStop(0, 'rgba(255,210,122,0.9)');
      g.addColorStop(0.5, 'rgba(255,170,60,0.25)');
      g.addColorStop(1, 'rgba(255,150,40,0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(cx, cy, r * 2.2, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = o.color;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.fill();
    } else if (o.type === 'orbit') {
      ctx.strokeStyle = o.color;
      ctx.globalAlpha = 0.75;
      ctx.setLineDash([6, 6]);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      if (is3d) ctx.ellipse(cx, cy, r, r * 0.42, 0, 0, Math.PI * 2);
      else ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.globalAlpha = 1;
    } else if (o.type === 'galaxy') {
      const g = ctx.createRadialGradient(cx, cy, r * 0.05, cx, cy, r);
      g.addColorStop(0, 'rgba(255,226,176,0.95)');
      g.addColorStop(0.3, 'rgba(196,181,253,0.5)');
      g.addColorStop(1, 'rgba(159,184,255,0)');
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(t * 0.04);
      ctx.scale(1, 0.42);
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(159,184,255,0.5)';
      ctx.lineWidth = Math.max(1, r * 0.03);
      for (let a = 0; a < 2; a++) {
        ctx.beginPath();
        for (let i = 0; i <= 40; i++) {
          const th = (i / 40) * Math.PI * 1.7 + a * Math.PI;
          const rr = r * 0.12 * Math.exp(th * 0.36);
          if (rr > r) break;
          const px = Math.cos(th) * rr;
          const py = Math.sin(th) * rr;
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
      }
      ctx.restore();
    } else if (o.type === 'group') {
      for (let i = 0; i < 12; i++) {
        const ang = i * 2.62;
        const rr = r * (0.12 + ((i * 53) % 80) / 100);
        const gx = cx + Math.cos(ang) * rr;
        const gy = cy + Math.sin(ang) * rr * (is3d ? 0.42 : 0.8);
        const gr = r * (i < 2 ? 0.09 : 0.035);
        ctx.fillStyle = i % 2 ? 'rgba(196,181,253,0.65)' : 'rgba(255,226,176,0.6)';
        ctx.save();
        ctx.translate(gx, gy);
        ctx.rotate(ang);
        ctx.scale(1, 0.5);
        ctx.beginPath();
        ctx.arc(0, 0, gr, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    } else if (o.type === 'universe') {
      const g = ctx.createRadialGradient(cx, cy, r * 0.1, cx, cy, r);
      g.addColorStop(0, 'rgba(124,141,176,0.3)');
      g.addColorStop(0.7, 'rgba(124,141,176,0.14)');
      g.addColorStop(1, 'rgba(124,141,176,0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(220,228,245,0.55)';
      for (let i = 0; i < 70; i++) {
        const ang = i * 2.39996;
        const rr = r * Math.sqrt(((i * 41) % 100) / 100);
        ctx.fillRect(cx + Math.cos(ang) * rr, cy + Math.sin(ang) * rr * (is3d ? 0.5 : 0.96), 1.6, 1.6);
      }
    }
  }

  let elapsed = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    elapsed += dt;
    exp += (targetExp - exp) * Math.min(1, dt * 5);
    const viewW = Math.pow(10, exp);
    const cx = w / 2;
    const cy = h / 2;

    ctx.fillStyle = '#080f1c';
    ctx.fillRect(0, 0, w, h);
    const starAlpha = Math.min(0.7, Math.max(0.12, (exp - 5) / 10));
    ctx.fillStyle = '#cdd9ec';
    for (let i = 0; i < 80; i++) {
      ctx.globalAlpha = (((i * 37) % 60) / 100 + 0.1) * starAlpha;
      ctx.fillRect(((i * 89) % 100) / 100 * w, ((i * 53) % 100) / 100 * h, 1.3, 1.3);
    }
    ctx.globalAlpha = 1;

    let focus = OBJECTS[0];
    let bestScore = Infinity;
    for (let i = 0; i < OBJECTS.length; i++) {
      const o = OBJECTS[i];
      const dpx = (o.size / viewW) * w;
      if (dpx > w * 5 || dpx < 0.6) continue;
      const score = Math.abs(Math.log(dpx / (w * 0.45)));
      if (score < bestScore) { bestScore = score; focus = o; }
    }
    for (let i = OBJECTS.length - 1; i >= 0; i--) {
      const o = OBJECTS[i];
      const dpx = (o.size / viewW) * w;
      if (dpx > w * 5 || dpx < 0.6) continue;
      drawObject(ctx, o, cx, cy, dpx, elapsed);
      if (dpx > 26 && dpx < w * 1.6) {
        ctx.font = '600 11px Poppins, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillStyle = o.color;
        const ly2 = cy - dpx / 2 - 8;
        if (ly2 > 14) ctx.fillText(o.name, cx, ly2);
        ctx.textAlign = 'left';
      }
    }

    const barW = w * 0.24;
    ctx.strokeStyle = 'rgba(232,238,251,0.8)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(w - barW - 16, h - 20);
    ctx.lineTo(w - 16, h - 20);
    ctx.moveTo(w - barW - 16, h - 25);
    ctx.lineTo(w - barW - 16, h - 15);
    ctx.moveTo(w - 16, h - 25);
    ctx.lineTo(w - 16, h - 15);
    ctx.stroke();
    ctx.fillStyle = 'rgba(232,238,251,0.85)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(fmtScale(viewW * 0.24), w - barW / 2 - 16, h - 28);
    ctx.textAlign = 'left';

    scaleBadge.set(`View width: 10${superscript(exp.toFixed(1))} m \u2248 ${fmtScale(viewW)}`);
    nameBadge.set(`${focus.name} \u2014 ${focus.label}`);
    nameBadge.el.style.setProperty('--ix-hud-color', focus.color);
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('wheel', onWheel);
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
