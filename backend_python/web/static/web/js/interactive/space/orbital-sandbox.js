import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const COLORS = ['#7dd3fc', '#a5b4fc', '#f9a8d4', '#86efac', '#fcd34d', '#fda4af', '#c4b5fd', '#5eead4'];

function detectTier() {
  const smallViewport = Math.min(window.innerWidth, window.innerHeight) < 900;
  const mobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) || ((navigator.maxTouchPoints || 0) > 1 && smallViewport);
  const mem = navigator.deviceMemory || 4;
  const cores = navigator.hardwareConcurrency || 4;
  if (mobile && (mem <= 2 || cores <= 4)) return 'low';
  if (mobile || mem <= 4) return 'medium';
  return 'high';
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const tier = detectTier();
  const TRAIL_LEN = tier === 'low' ? 60 : tier === 'medium' ? 100 : 140;
  const MAX_BODIES = tier === 'low' ? 14 : tier === 'medium' ? 20 : 28;
  const bodies = [];
  const particles = [];
  let starMass = 5200;
  let showVectors = false;
  let drag = null;
  let colorIdx = 0;
  let bgStars = [];
  let viewMode = '2d';

  sim.onResize((w, h) => {
    bgStars = [];
    const n = Math.round((w * h) / 5200);
    for (let i = 0; i < n; i++) {
      bgStars.push({ x: Math.random() * w, y: Math.random() * h, r: Math.random() * 1.2 + 0.3, a: Math.random() * 0.5 + 0.2 });
    }
  });

  function starRadius() {
    return 10 + Math.sqrt(starMass) * 0.16;
  }

  function spawnBody(x, y, vx, vy) {
    if (bodies.length >= MAX_BODIES) bodies.shift();
    bodies.push({
      x, y, vx, vy,
      r: 4.5 + Math.random() * 2.5,
      color: COLORS[colorIdx++ % COLORS.length],
      trail: new Float32Array(TRAIL_LEN * 2),
      trailLen: 0,
      trailHead: 0,
      alive: true,
    });
  }

  function burn(b) {
    b.alive = false;
    for (let i = 0; i < 16; i++) {
      const a = Math.random() * Math.PI * 2;
      const s = 20 + Math.random() * 70;
      particles.push({ x: b.x, y: b.y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, life: 0.7 + Math.random() * 0.5, t: 0 });
    }
  }

  function addComet(w, h) {
    const cx = w / 2;
    const cy = h / 2;
    const edge = Math.min(w, h) * 0.46;
    const a = Math.random() * Math.PI * 2;
    const x = cx + Math.cos(a) * edge;
    const y = cy + Math.sin(a) * edge;
    const tangential = a + Math.PI / 2 + (Math.random() - 0.5) * 0.5;
    const v = Math.sqrt((starMass * 240) / edge) * (0.4 + Math.random() * 0.3);
    spawnBody(x, y, Math.cos(tangential) * v, Math.sin(tangential) * v);
  }

  const hud = createHud(stage);
  const countBadge = hud.badge('Bodies: 0', '#7dd3fc');
  const hintBadge = hud.badge('Drag anywhere to launch a planet', '#9ec1ff');

  const panel = createPanel(stage, { title: 'Gravity Sandbox' });
  panel.select({
    label: 'View',
    options: [
      { value: '2d', label: '2D' },
      { value: '3d', label: '3D' },
    ],
    value: viewMode,
    onChange: (v) => { viewMode = v; },
  });
  panel.slider({
    label: 'Star mass',
    min: 1500, max: 14000, step: 100, value: starMass,
    format: (v) => `${Math.round(v / 100)} suns`,
    onChange: (v) => { starMass = v; },
  });
  panel.toggle({ label: 'Show velocity vectors', value: false, onChange: (v) => { showVectors = v; } });
  panel.buttonRow([
    { label: 'Comet', icon: 'star_half', onClick: () => addComet(sim.width, sim.height) },
    { label: 'Clear', icon: 'delete', variant: 'danger', onClick: () => { bodies.length = 0; particles.length = 0; } },
  ]);
  panel.info('Drag from any point and release: the arrow sets the new planet\u2019s velocity. Short drags fall into the star, long drags escape. Find the orbit in between!');

  function onDown(e) {
    if (e.target !== sim.canvas) return;
    sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
    const raw = pointerPos(sim.canvas, e);
    const p = unproject(raw.x, raw.y, sim.width, sim.height);
    drag = { sx: p.x, sy: p.y, cx: p.x, cy: p.y, id: e.pointerId };
  }
  function onMove(e) {
    if (!drag || e.pointerId !== drag.id) return;
    const raw = pointerPos(sim.canvas, e);
    const p = unproject(raw.x, raw.y, sim.width, sim.height);
    drag.cx = p.x;
    drag.cy = p.y;
  }
  function onUp(e) {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = drag.cx - drag.sx;
    const dy = drag.cy - drag.sy;
    if (Math.hypot(dx, dy) > 6) {
      spawnBody(drag.sx, drag.sy, dx * 1.6, dy * 1.6);
      hintBadge.set('Nice launch! Watch gravity bend its path');
    }
    drag = null;
  }
  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function project(x, y, w, h, z = 0) {
    if (viewMode !== '3d') return { x, y };
    const cx = w / 2;
    const cy = h / 2;
    return { x: cx + (x - cx) * 0.98, y: cy + (y - cy) * 0.52 - z };
  }

  function unproject(x, y, w, h) {
    if (viewMode !== '3d') return { x, y };
    const cx = w / 2;
    const cy = h / 2;
    return { x: cx + (x - cx) / 0.98, y: cy + (y - cy) / 0.52 };
  }

  function physics(dt, w, h) {
    const cx = w / 2;
    const cy = h / 2;
    const sr = starRadius();
    const sub = 4;
    const step = Math.min(dt, 0.033) / sub;
    for (let s = 0; s < sub; s++) {
      for (let i = 0; i < bodies.length; i++) {
        const b = bodies[i];
        if (!b.alive) continue;
        const dx = cx - b.x;
        const dy = cy - b.y;
        const d2 = dx * dx + dy * dy;
        const d = Math.sqrt(d2);
        if (d < sr + b.r * 0.5) { burn(b); continue; }
        const acc = (starMass * 240) / Math.max(d2, 400);
        b.vx += (dx / d) * acc * step;
        b.vy += (dy / d) * acc * step;
        b.x += b.vx * step;
        b.y += b.vy * step;
      }
    }
    const limit = Math.max(w, h) * 2.5;
    for (let i = bodies.length - 1; i >= 0; i--) {
      const b = bodies[i];
      if (!b.alive) { bodies.splice(i, 1); continue; }
      if (Math.abs(b.x - cx) > limit || Math.abs(b.y - cy) > limit) { bodies.splice(i, 1); continue; }
      b.trail[b.trailHead * 2] = b.x;
      b.trail[b.trailHead * 2 + 1] = b.y;
      b.trailHead = (b.trailHead + 1) % TRAIL_LEN;
      if (b.trailLen < TRAIL_LEN) b.trailLen++;
    }
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.t += dt;
      if (p.t >= p.life) { particles.splice(i, 1); continue; }
      p.x += p.vx * dt;
      p.y += p.vy * dt;
    }
  }

  sim.setUpdate((ctx, dt, w, h) => {
    physics(dt, w, h);
    const cx = w / 2;
    const cy = h / 2;
    ctx.fillStyle = '#0a1322';
    ctx.fillRect(0, 0, w, h);
    for (let i = 0; i < bgStars.length; i++) {
      const s = bgStars[i];
      ctx.globalAlpha = s.a;
      ctx.fillStyle = '#cdd9ec';
      ctx.fillRect(s.x, s.y, s.r, s.r);
    }
    ctx.globalAlpha = 1;

    const sr = starRadius();
    if (viewMode === '3d') {
      ctx.strokeStyle = 'rgba(158,193,255,0.2)';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.ellipse(cx, cy, Math.min(w, h) * 0.43, Math.min(w, h) * 0.22, 0, 0, Math.PI * 2);
      ctx.stroke();
    }
    const grad = ctx.createRadialGradient(cx, cy, sr * 0.2, cx, cy, sr * 3.2);
    grad.addColorStop(0, 'rgba(255,200,90,0.95)');
    grad.addColorStop(0.3, 'rgba(255,160,60,0.35)');
    grad.addColorStop(1, 'rgba(255,140,40,0)');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(cx, cy, sr * 3.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#ffd27a';
    ctx.beginPath();
    ctx.arc(cx, cy, sr, 0, Math.PI * 2);
    ctx.fill();

    for (let i = 0; i < bodies.length; i++) {
      const b = bodies[i];
      if (b.trailLen > 1) {
        ctx.lineWidth = 1.6;
        ctx.strokeStyle = b.color;
        const bands = 4;
        const start = b.trailHead - b.trailLen + TRAIL_LEN * 2;
        const lastJ = b.trailLen - 1;
        for (let band = 0; band < bands; band++) {
          const j0 = Math.floor((band * lastJ) / bands);
          const j1 = Math.floor(((band + 1) * lastJ) / bands);
          if (j1 <= j0) continue;
          ctx.globalAlpha = (((j0 + j1) / 2) / b.trailLen) * 0.55;
          ctx.beginPath();
          let idx = (start + j0) % TRAIL_LEN;
          let tp = project(b.trail[idx * 2], b.trail[idx * 2 + 1], w, h);
          ctx.moveTo(tp.x, tp.y);
          for (let j = j0 + 1; j <= j1; j++) {
            idx = (start + j) % TRAIL_LEN;
            tp = project(b.trail[idx * 2], b.trail[idx * 2 + 1], w, h);
            ctx.lineTo(tp.x, tp.y);
          }
          ctx.stroke();
        }
        ctx.globalAlpha = 1;
      }
      const bp = project(b.x, b.y, w, h, viewMode === '3d' ? b.r * 0.8 : 0);
      if (viewMode === '3d') {
        const sp = project(b.x, b.y, w, h);
        ctx.fillStyle = 'rgba(0,0,0,0.22)';
        ctx.beginPath();
        ctx.ellipse(sp.x, sp.y + b.r * 0.5, b.r * 1.25, b.r * 0.45, 0, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.fillStyle = b.color;
      ctx.beginPath();
      ctx.arc(bp.x, bp.y, b.r, 0, Math.PI * 2);
      ctx.fill();
      if (showVectors) {
        drawArrow(ctx, b.x, b.y, b.x + b.vx * 0.25, b.y + b.vy * 0.25, '#ffffff', 0.7);
      }
    }

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      ctx.globalAlpha = 1 - p.t / p.life;
      ctx.fillStyle = '#ffb347';
      const pp = project(p.x, p.y, w, h, viewMode === '3d' ? 3 : 0);
      ctx.beginPath();
      ctx.arc(pp.x, pp.y, 2.2, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    if (drag) {
      drawArrow(ctx, drag.sx, drag.sy, drag.cx, drag.cy, '#8be9a8', 1);
      const dp = project(drag.sx, drag.sy, w, h, viewMode === '3d' ? 5 : 0);
      ctx.fillStyle = '#8be9a8';
      ctx.beginPath();
      ctx.arc(dp.x, dp.y, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    countBadge.set(`Bodies: ${bodies.length}`);
  });

  function drawArrow(ctx, x0, y0, x1, y1, color, alpha) {
    const p0 = project(x0, y0, sim.width, sim.height, viewMode === '3d' ? 5 : 0);
    const p1 = project(x1, y1, sim.width, sim.height, viewMode === '3d' ? 5 : 0);
    const dx = p1.x - p0.x;
    const dy = p1.y - p0.y;
    const len = Math.hypot(dx, dy);
    if (len < 2) return;
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(p0.x, p0.y);
    ctx.lineTo(p1.x, p1.y);
    ctx.stroke();
    const a = Math.atan2(dy, dx);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p1.x - Math.cos(a - 0.45) * 9, p1.y - Math.sin(a - 0.45) * 9);
    ctx.lineTo(p1.x - Math.cos(a + 0.45) * 9, p1.y - Math.sin(a + 0.45) * 9);
    ctx.closePath();
    ctx.fill();
    ctx.globalAlpha = 1;
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
