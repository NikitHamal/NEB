import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SUBSTANCES = {
  water: { label: 'Water', melt: 0, boil: 100, tMin: -50, tMax: 150, solidColor: '#93c5fd', liquidColor: '#3b82f6', gasColor: '#bfdbfe' },
  iron: { label: 'Iron', melt: 1538, boil: 2862, tMin: 1300, tMax: 3000, solidColor: '#cbd5e1', liquidColor: '#f97316', gasColor: '#fde68a' },
  oxygen: { label: 'Oxygen', melt: -218, boil: -183, tMin: -245, tMax: -150, solidColor: '#a5f3fc', liquidColor: '#22d3ee', gasColor: '#cffafe' },
};

function detectTier() {
  const mobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) || (navigator.maxTouchPoints || 0) > 1;
  const mem = navigator.deviceMemory || 4;
  const cores = navigator.hardwareConcurrency || 4;
  if (mobile && (mem <= 2 || cores <= 4)) return 'low';
  if (mobile || mem <= 4) return 'medium';
  return 'high';
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const phaseBadge = hud.badge('LIQUID', '#10B981');

  const tier = detectTier();
  const N = tier === 'low' ? 80 : tier === 'medium' ? 110 : 150;

  let substance = SUBSTANCES.water;
  let T = 20;

  const px = new Float32Array(N);
  const py = new Float32Array(N);
  const vx = new Float32Array(N);
  const vy = new Float32Array(N);
  const sx = new Float32Array(N);
  const sy = new Float32Array(N);
  const phase0 = new Float32Array(N);
  for (let i = 0; i < N; i++) phase0[i] = Math.random() * Math.PI * 2;
  let initialized = false;
  let prevPhase = '';

  function getPhase() {
    if (T < substance.melt) return 'solid';
    if (T < substance.boil) return 'liquid';
    return 'gas';
  }

  function containerRect(w, h) {
    const cw = Math.min(w * 0.62, w - 40);
    const ch = h * 0.72;
    return { x: 24, y: h - 36 - ch, w: cw, h: ch };
  }

  function latticeSites(box) {
    const cols = Math.ceil(Math.sqrt(N * (box.w / box.h) * 1.6));
    const gap = Math.min(box.w / (cols + 1), 18);
    let i = 0;
    let row = 0;
    while (i < N) {
      const inRow = cols - (row % 2);
      for (let c = 0; c < inRow && i < N; c++) {
        sx[i] = box.x + gap * 0.9 + c * gap + (row % 2) * gap * 0.5;
        sy[i] = box.y + box.h - 10 - row * gap * 0.85;
        i++;
      }
      row++;
    }
  }

  function seed(box, phase) {
    latticeSites(box);
    for (let i = 0; i < N; i++) {
      if (phase === 'gas') {
        px[i] = box.x + 8 + Math.random() * (box.w - 16);
        py[i] = box.y + 8 + Math.random() * (box.h - 16);
        const a = Math.random() * Math.PI * 2;
        vx[i] = Math.cos(a);
        vy[i] = Math.sin(a);
      } else {
        px[i] = sx[i] + (phase === 'liquid' ? (Math.random() - 0.5) * 14 : 0);
        py[i] = sy[i] + (phase === 'liquid' ? (Math.random() - 0.5) * 8 : 0);
        vx[i] = 0;
        vy[i] = 0;
      }
    }
  }

  sim.onResize((w, h) => {
    if (initialized) latticeSites(containerRect(w, h));
  });

  function kelvin() { return T + 273.15; }

  function step(dt, box, phase, t) {
    const kT = Math.max(10, kelvin());
    if (phase === 'solid') {
      const norm = Math.max(0, Math.min(1, (T - substance.tMin) / (substance.melt - substance.tMin + 0.001)));
      const amp = 0.8 + norm * 3.2;
      for (let i = 0; i < N; i++) {
        px[i] += (sx[i] + Math.sin(t * (6 + (i % 5)) + phase0[i]) * amp - px[i]) * Math.min(1, dt * 10);
        py[i] += (sy[i] + Math.cos(t * (7 + (i % 4)) + phase0[i] * 1.7) * amp - py[i]) * Math.min(1, dt * 10);
      }
    } else if (phase === 'liquid') {
      const jiggle = 30 + 60 * Math.max(0, Math.min(1, (T - substance.melt) / (substance.boil - substance.melt)));
      const rad = 13;
      for (let i = 0; i < N; i++) {
        vy[i] += 220 * dt;
        vx[i] += (Math.random() - 0.5) * jiggle * dt * 8;
        vy[i] += (Math.random() - 0.5) * jiggle * dt * 8;
        for (let j = i + 1; j < N; j++) {
          const dx = px[j] - px[i];
          if (dx > rad || dx < -rad) continue;
          const dy = py[j] - py[i];
          if (dy > rad || dy < -rad) continue;
          const d2 = dx * dx + dy * dy;
          if (d2 < rad * rad && d2 > 0.01) {
            const d = Math.sqrt(d2);
            const f = ((rad - d) / rad) * 260 * dt;
            const ux = dx / d;
            const uy = dy / d;
            vx[i] -= ux * f; vy[i] -= uy * f;
            vx[j] += ux * f; vy[j] += uy * f;
          }
        }
        vx[i] *= 1 - Math.min(1, dt * 2.2);
        vy[i] *= 1 - Math.min(1, dt * 2.2);
        px[i] += vx[i] * dt;
        py[i] += vy[i] * dt;
        if (px[i] < box.x + 6) { px[i] = box.x + 6; vx[i] *= -0.3; }
        if (px[i] > box.x + box.w - 6) { px[i] = box.x + box.w - 6; vx[i] *= -0.3; }
        if (py[i] > box.y + box.h - 6) { py[i] = box.y + box.h - 6; vy[i] *= -0.3; }
        if (py[i] < box.y + 6) { py[i] = box.y + 6; vy[i] = 0; }
      }
    } else {
      const speed = 26 * Math.sqrt(kT / 80);
      for (let i = 0; i < N; i++) {
        const cur = Math.hypot(vx[i], vy[i]) || 1;
        const k = 1 + (speed / cur - 1) * Math.min(1, dt * 2);
        vx[i] *= k;
        vy[i] *= k;
        px[i] += vx[i] * dt;
        py[i] += vy[i] * dt;
        if (px[i] < box.x + 5) { px[i] = box.x + 5; vx[i] = Math.abs(vx[i]); }
        if (px[i] > box.x + box.w - 5) { px[i] = box.x + box.w - 5; vx[i] = -Math.abs(vx[i]); }
        if (py[i] < box.y + 5) { py[i] = box.y + 5; vy[i] = Math.abs(vy[i]); }
        if (py[i] > box.y + box.h - 5) { py[i] = box.y + box.h - 5; vy[i] = -Math.abs(vy[i]); }
      }
    }
  }

  function curvePoints() {
    const s = substance;
    const riseSpan = (s.melt - s.tMin) + (s.boil - s.melt) + (s.tMax - s.boil);
    const plateau = 0.16;
    const riseScale = (1 - 2 * plateau) / riseSpan;
    const pts = [];
    let x = 0;
    pts.push({ x, t: s.tMin });
    x += (s.melt - s.tMin) * riseScale;
    pts.push({ x, t: s.melt });
    x += plateau;
    pts.push({ x, t: s.melt });
    x += (s.boil - s.melt) * riseScale;
    pts.push({ x, t: s.boil });
    x += plateau;
    pts.push({ x, t: s.boil });
    x += (s.tMax - s.boil) * riseScale;
    pts.push({ x, t: s.tMax });
    return pts;
  }

  function markerX(pts) {
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i];
      const b = pts[i + 1];
      if (b.t > a.t && T >= a.t && T <= b.t) {
        return a.x + ((T - a.t) / (b.t - a.t)) * (b.x - a.x);
      }
      if (b.t === a.t && Math.abs(T - a.t) < 0.5) return (a.x + b.x) / 2;
    }
    return T <= pts[0].t ? 0 : 1;
  }

  function drawGraph(ctx, w, h) {
    const gx = Math.min(w * 0.62, w - 40) + 40;
    const gw = w - gx - 20;
    if (gw < 90) return;
    const gy = h * 0.2;
    const gh = h * 0.5;
    ctx.strokeStyle = 'rgba(158,193,255,0.35)';
    ctx.lineWidth = 1;
    ctx.strokeRect(gx, gy, gw, gh);
    ctx.fillStyle = 'rgba(199,212,234,0.6)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('heating curve', gx + gw / 2, gy - 8);
    ctx.fillText('energy added →', gx + gw / 2, gy + gh + 14);
    ctx.save();
    ctx.translate(gx - 8, gy + gh / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('temperature →', 0, 0);
    ctx.restore();
    const pts = curvePoints();
    const ty = (t) => gy + gh - ((t - substance.tMin) / (substance.tMax - substance.tMin)) * gh;
    ctx.strokeStyle = '#10B981';
    ctx.lineWidth = 2;
    ctx.beginPath();
    pts.forEach((p, i) => {
      const x = gx + p.x * gw;
      const y = ty(p.t);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.7)';
    ctx.textAlign = 'left';
    ctx.fillText(`melt ${substance.melt}°`, gx + 4, ty(substance.melt) - 4);
    ctx.fillText(`boil ${substance.boil}°`, gx + 4, ty(substance.boil) - 4);
    const mx = gx + markerX(pts) * gw;
    ctx.fillStyle = '#fbbf24';
    ctx.beginPath();
    ctx.arc(mx, ty(T), 5, 0, Math.PI * 2);
    ctx.fill();
  }

  const panel = createPanel(stage, { title: 'Matter Controls' });
  panel.select({
    label: 'Substance',
    options: Object.entries(SUBSTANCES).map(([value, s]) => ({ value, label: `${s.label} (melts ${s.melt}°C, boils ${s.boil}°C)` })),
    value: 'water',
    onChange: (v) => {
      substance = SUBSTANCES[v];
      T = (substance.tMin + substance.tMax) / 2;
      const input = tempSlider.el.querySelector('input');
      input.min = substance.tMin;
      input.max = substance.tMax;
      tempSlider.set(T);
      initialized = false;
    },
  });
  const tempSlider = panel.slider({
    label: 'Temperature',
    min: substance.tMin, max: substance.tMax, step: 1, value: T,
    format: (v) => `${v} °C`,
    onChange: (v) => { T = v; },
  });
  panel.divider();
  const tempOut = panel.readout({ label: 'Temperature', value: '20 °C' });
  const phaseOut = panel.readout({ label: 'Phase', value: 'Liquid' });
  panel.info('Slide the temperature slowly through the melting and boiling points and watch the particles change behaviour. The plateaus on the curve are where latent heat is absorbed.');

  let elapsed = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    elapsed += dt;
    const box = containerRect(w, h);
    const phase = getPhase();
    if (!initialized || phase !== prevPhase) {
      if (!initialized) seed(box, phase);
      else if (phase === 'gas') {
        for (let i = 0; i < N; i++) {
          const a = Math.random() * Math.PI * 2;
          vx[i] = Math.cos(a) * 20;
          vy[i] = Math.sin(a) * 20;
        }
      } else if (phase === 'solid') {
        latticeSites(box);
      }
      initialized = true;
      prevPhase = phase;
    }
    step(dt, box, phase, elapsed);

    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(199,212,234,0.7)';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(box.x, box.y);
    ctx.lineTo(box.x, box.y + box.h);
    ctx.lineTo(box.x + box.w, box.y + box.h);
    ctx.lineTo(box.x + box.w, box.y);
    ctx.stroke();

    const color = phase === 'solid' ? substance.solidColor : phase === 'liquid' ? substance.liquidColor : substance.gasColor;
    ctx.fillStyle = color;
    for (let i = 0; i < N; i++) {
      ctx.beginPath();
      ctx.arc(px[i], py[i], 4.5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawGraph(ctx, w, h);

    const phaseLabel = phase.toUpperCase();
    phaseBadge.set(`${substance.label}: ${phaseLabel}`);
    phaseBadge.el.style.setProperty('--ix-hud-color', phase === 'solid' ? '#93c5fd' : phase === 'liquid' ? '#10B981' : '#fbbf24');
    tempOut.set(`${T} °C`);
    phaseOut.set(phaseLabel[0] + phaseLabel.slice(1).toLowerCase());
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
