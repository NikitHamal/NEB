import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SUBSTANCES = {
  ice: { label: 'Ice / Water', melt: 0, tMin: -20, tMax: 40, solid: '#bfdbfe', liquid: '#3b82f6' },
  chocolate: { label: 'Chocolate', melt: 34, tMin: 0, tMax: 70, solid: '#92400e', liquid: '#b45309' },
  butter: { label: 'Butter', melt: 35, tMin: 0, tMax: 70, solid: '#fde68a', liquid: '#fbbf24' },
  wax: { label: 'Candle wax', melt: 60, tMin: 20, tMax: 100, solid: '#e2e8f0', liquid: '#fda4af' },
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
  const badge = hud.badge('SOLID', '#93c5fd');

  const tier = detectTier();
  const N = tier === 'low' ? 60 : tier === 'medium' ? 90 : 120;
  const px = new Float32Array(N);
  const py = new Float32Array(N);
  const vx = new Float32Array(N);
  const vy = new Float32Array(N);
  const sx = new Float32Array(N);
  const sy = new Float32Array(N);
  const phase0 = new Float32Array(N);
  const order = new Uint16Array(N);
  const rank = new Float32Array(N);
  for (let i = 0; i < N; i++) { phase0[i] = Math.random() * Math.PI * 2; order[i] = i; }
  for (let i = N - 1; i > 0; i--) {
    const j = (Math.random() * (i + 1)) | 0;
    const t = order[i]; order[i] = order[j]; order[j] = t;
  }
  for (let i = 0; i < N; i++) rank[order[i]] = i / N;

  let substance = SUBSTANCES.ice;
  let T = -10;
  let frac = 0;
  let power = 0;
  let seeded = false;

  function boxRect(w, h) {
    const bw = Math.min(w * 0.46, 250);
    const bh = h * 0.56;
    return { x: w * 0.16, y: h * 0.5 - bh / 2 + 10, w: bw, h: bh };
  }

  function latticeSites(box) {
    const cols = Math.ceil(Math.sqrt(N * (box.w / box.h) * 1.4));
    const gap = Math.min(box.w / (cols + 1), 20);
    let i = 0;
    let row = 0;
    while (i < N) {
      const inRow = cols - (row % 2);
      for (let c = 0; c < inRow && i < N; c++) {
        sx[i] = box.x + gap + c * gap + (row % 2) * gap * 0.5;
        sy[i] = box.y + box.h - 12 - row * gap * 0.85;
        i++;
      }
      row++;
    }
  }

  function seed(box) {
    latticeSites(box);
    for (let i = 0; i < N; i++) {
      px[i] = sx[i]; py[i] = sy[i]; vx[i] = 0; vy[i] = 0;
    }
    seeded = true;
  }

  const panel = createPanel(stage, { title: 'Heat Lab' });
  panel.select({
    label: 'Substance',
    options: Object.entries(SUBSTANCES).map(([value, s]) => ({ value, label: `${s.label} (melts at ${s.melt}°C)` })),
    value: 'ice',
    onChange: (v) => {
      substance = SUBSTANCES[v];
      T = substance.tMin + (substance.melt - substance.tMin) * 0.5;
      frac = 0;
      seeded = false;
      heatSlider.set(0);
      power = 0;
    },
  });
  const heatSlider = panel.slider({
    label: 'Cool ❄  /  Heat 🔥',
    min: -100, max: 100, step: 5, value: 0,
    format: (v) => (v > 0 ? `heating +${v}` : v < 0 ? `cooling ${v}` : 'off'),
    onChange: (v) => { power = v / 100; },
  });
  panel.divider();
  const tempOut = panel.readout({ label: 'Thermometer', value: '-10 °C' });
  const stateOut = panel.readout({ label: 'State', value: 'Solid' });
  const meltOut = panel.readout({ label: 'Melting point', value: '0 °C' });
  panel.info('Push the dial to heat or cool. Watch the thermometer PAUSE right at the melting point — all the energy is busy breaking (or building) the particle pattern!');

  let elapsed = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    dt = Math.min(dt, 0.05);
    elapsed += dt;
    const box = boxRect(w, h);
    if (!seeded) seed(box);

    const rate = 9;
    if (power > 0) {
      if (T < substance.melt || frac >= 1) {
        T = Math.min(substance.tMax, T + power * rate * dt);
        if (T > substance.melt && frac < 1) T = substance.melt;
      } else {
        frac = Math.min(1, frac + power * 0.28 * dt * rate / 4);
      }
    } else if (power < 0) {
      if (T > substance.melt || frac <= 0) {
        T = Math.max(substance.tMin, T + power * rate * dt);
        if (T < substance.melt && frac > 0) T = substance.melt;
      } else {
        frac = Math.max(0, frac + power * 0.28 * dt * rate / 4);
      }
    }

    const wob = 1 + Math.max(0, Math.min(1, (T - substance.tMin) / (substance.melt - substance.tMin + 0.001))) * 2.4;
    for (let i = 0; i < N; i++) {
      if (rank[i] < frac) {
        vx[i] += (Math.random() - 0.5) * 700 * dt;
        vy[i] += (Math.random() - 0.5) * 700 * dt + 60 * dt;
        vx[i] *= 1 - Math.min(1, dt * 1.8);
        vy[i] *= 1 - Math.min(1, dt * 1.8);
        px[i] += vx[i] * dt;
        py[i] += vy[i] * dt;
        if (px[i] < box.x + 6) { px[i] = box.x + 6; vx[i] *= -0.5; }
        if (px[i] > box.x + box.w - 6) { px[i] = box.x + box.w - 6; vx[i] *= -0.5; }
        if (py[i] > box.y + box.h - 6) { py[i] = box.y + box.h - 6; vy[i] *= -0.5; }
        if (py[i] < box.y + box.h * 0.35) { py[i] = box.y + box.h * 0.35; vy[i] = Math.abs(vy[i]) * 0.5; }
      } else {
        px[i] += (sx[i] + Math.sin(elapsed * (6 + (i % 5)) + phase0[i]) * wob - px[i]) * Math.min(1, dt * 10);
        py[i] += (sy[i] + Math.cos(elapsed * (7 + (i % 4)) + phase0[i] * 1.7) * wob - py[i]) * Math.min(1, dt * 10);
        vx[i] = 0; vy[i] = 0;
      }
    }

    ctx.clearRect(0, 0, w, h);

    ctx.strokeStyle = 'rgba(199,212,234,0.85)';
    ctx.lineWidth = 2.5;
    ctx.strokeRect(box.x, box.y, box.w, box.h);

    for (let i = 0; i < N; i++) {
      ctx.fillStyle = rank[i] < frac ? substance.liquid : substance.solid;
      ctx.beginPath();
      ctx.arc(px[i], py[i], 5, 0, Math.PI * 2);
      ctx.fill();
    }

    if (power !== 0) {
      const flameY = box.y + box.h + 16;
      ctx.fillStyle = power > 0 ? `rgba(249,115,22,${0.4 + 0.6 * power})` : `rgba(125,211,252,${0.4 - 0.6 * power})`;
      ctx.font = '600 13px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(power > 0 ? '🔥 heating 🔥' : '❄ cooling ❄', box.x + box.w / 2, flameY);
    }

    const tx = box.x + box.w + Math.min(w * 0.12, 56);
    const tTop = box.y;
    const tH = box.h;
    const tw = 14;
    const fracT = Math.max(0, Math.min(1, (T - substance.tMin) / (substance.tMax - substance.tMin)));
    ctx.strokeStyle = 'rgba(199,212,234,0.85)';
    ctx.lineWidth = 2;
    ctx.strokeRect(tx - tw / 2, tTop, tw, tH);
    ctx.beginPath();
    ctx.arc(tx, tTop + tH + 10, 11, 0, Math.PI * 2);
    ctx.stroke();
    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.arc(tx, tTop + tH + 10, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillRect(tx - 4, tTop + tH * (1 - fracT), 8, tH * fracT + 2);
    const meltY = tTop + tH * (1 - (substance.melt - substance.tMin) / (substance.tMax - substance.tMin));
    ctx.strokeStyle = 'rgba(251,191,36,0.8)';
    ctx.setLineDash([3, 4]);
    ctx.beginPath();
    ctx.moveTo(tx - tw, meltY);
    ctx.lineTo(tx + tw, meltY);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = 'rgba(251,191,36,0.9)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`melts ${substance.melt}°C`, tx + tw, meltY - 4);
    ctx.fillStyle = 'rgba(199,212,234,0.8)';
    ctx.textAlign = 'center';
    ctx.fillText(`${Math.round(T)}°C`, tx, tTop - 8);

    const state = frac >= 1 ? 'LIQUID' : frac <= 0 ? 'SOLID' : power >= 0 ? 'MELTING…' : 'FREEZING…';
    badge.set(`${substance.label}: ${state}`);
    badge.el.style.setProperty('--ix-hud-color', frac >= 1 ? '#10B981' : frac <= 0 ? '#93c5fd' : '#fbbf24');
    tempOut.set(`${Math.round(T)} °C`);
    stateOut.set(state === 'SOLID' ? 'Solid' : state === 'LIQUID' ? 'Liquid' : state === 'MELTING…' ? 'Melting…' : 'Freezing…');
    meltOut.set(`${substance.melt} °C`);
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
