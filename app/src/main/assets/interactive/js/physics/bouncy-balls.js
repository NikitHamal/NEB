import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const GRAVITY_PRESETS = { earth: 9.81, moon: 1.62, jupiter: 24.8 };
const COLORS = ['#fb7185', '#fbbf24', '#34d399', '#38bdf8', '#c084fc', '#f472b6'];
const PX_PER_M = 50;

function detectTier() {
  const mobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) || (navigator.maxTouchPoints || 0) > 1;
  const mem = navigator.deviceMemory || 4;
  const cores = navigator.hardwareConcurrency || 4;
  if (mobile && (mem <= 2 || cores <= 4)) return 'low';
  return 'high';
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Tap anywhere to drop a ball!', '#F59E0B');

  const MAX_N = detectTier() === 'low' ? 7 : 12;
  const px = new Float32Array(MAX_N);
  const py = new Float32Array(MAX_N);
  const vx = new Float32Array(MAX_N);
  const vy = new Float32Array(MAX_N);
  const rad = new Float32Array(MAX_N);
  const col = new Uint8Array(MAX_N);
  let count = 0;
  let head = 0;

  let g = 9.81;
  let bounciness = 0.75;
  let size = 18;

  const panel = createPanel(stage, { title: 'Bounce Controls' });
  const gravSelect = panel.select({
    label: 'Planet',
    options: [
      { value: 'earth', label: 'Earth (9.81 m/s²)' },
      { value: 'moon', label: 'Moon (1.62 m/s²)' },
      { value: 'jupiter', label: 'Jupiter (24.8 m/s²)' },
      { value: 'custom', label: 'Custom' },
    ],
    value: 'earth',
    onChange: (val) => {
      if (val !== 'custom') {
        g = GRAVITY_PRESETS[val];
        gravSlider.set(g);
      }
    },
  });
  const gravSlider = panel.slider({
    label: 'Gravity g',
    min: 1, max: 30, step: 0.1, value: g,
    format: (val) => `${val.toFixed(1)} m/s²`,
    onChange: (val) => { g = val; gravSelect.set('custom'); },
  });
  panel.slider({
    label: 'Bounciness',
    min: 0.3, max: 0.95, step: 0.05, value: bounciness,
    format: (val) => `${Math.round(val * 100)}%`,
    onChange: (val) => { bounciness = val; },
  });
  panel.slider({
    label: 'Ball size',
    min: 10, max: 28, step: 1, value: size,
    format: (val) => `${val} px`,
    onChange: (val) => { size = val; },
  });
  panel.divider();
  const countOut = panel.readout({ label: 'Balls', value: '0' });
  panel.button({
    label: 'Clear balls',
    icon: 'mop',
    onClick: () => { count = 0; head = 0; },
  });
  panel.info('Tap to drop a ball where you touch. Try Moon gravity for slow floaty bounces, then Jupiter for a heavy slam!');

  function addBall(x, y) {
    const i = head;
    px[i] = x;
    py[i] = y;
    vx[i] = (Math.random() - 0.5) * 60;
    vy[i] = 0;
    rad[i] = size;
    col[i] = (Math.random() * COLORS.length) | 0;
    head = (head + 1) % MAX_N;
    if (count < MAX_N) count++;
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    addBall(p.x, Math.min(p.y, sim.height - 60));
    e.preventDefault();
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);

  function step(dt, w, h) {
    const floor = h - 36;
    const gp = g * PX_PER_M;
    for (let i = 0; i < count; i++) {
      vy[i] += gp * dt;
      px[i] += vx[i] * dt;
      py[i] += vy[i] * dt;
      const r = rad[i];
      if (py[i] > floor - r) {
        py[i] = floor - r;
        if (Math.abs(vy[i]) > 20) vy[i] = -vy[i] * bounciness;
        else vy[i] = 0;
        vx[i] *= 0.985;
      }
      if (px[i] < r) { px[i] = r; vx[i] = Math.abs(vx[i]) * bounciness; }
      if (px[i] > w - r) { px[i] = w - r; vx[i] = -Math.abs(vx[i]) * bounciness; }
    }
    for (let i = 0; i < count; i++) {
      for (let j = i + 1; j < count; j++) {
        const dx = px[j] - px[i];
        const dy = py[j] - py[i];
        const minD = rad[i] + rad[j];
        const d2 = dx * dx + dy * dy;
        if (d2 > 0.0001 && d2 < minD * minD) {
          const d = Math.sqrt(d2);
          const nx = dx / d;
          const ny = dy / d;
          const overlap = (minD - d) / 2;
          px[i] -= nx * overlap;
          py[i] -= ny * overlap;
          px[j] += nx * overlap;
          py[j] += ny * overlap;
          const rel = (vx[j] - vx[i]) * nx + (vy[j] - vy[i]) * ny;
          if (rel < 0) {
            const imp = -rel * (0.5 + bounciness / 2);
            vx[i] -= nx * imp * 0.5;
            vy[i] -= ny * imp * 0.5;
            vx[j] += nx * imp * 0.5;
            vy[j] += ny * imp * 0.5;
          }
        }
      }
    }
  }

  sim.setUpdate((ctx, dt, w, h) => {
    step(Math.min(dt, 0.05), w, h);
    ctx.clearRect(0, 0, w, h);
    const floor = h - 36;

    ctx.fillStyle = '#14532d';
    ctx.fillRect(0, floor, w, h - floor);
    ctx.fillStyle = '#22c55e';
    ctx.fillRect(0, floor, w, 7);

    for (let i = 0; i < count; i++) {
      const c = COLORS[col[i]];
      const r = rad[i];
      const shadowW = r * Math.max(0.4, 1 - (floor - r - py[i]) / 300);
      ctx.fillStyle = 'rgba(0,0,0,0.25)';
      ctx.beginPath();
      ctx.ellipse(px[i], floor + 3, shadowW, 4, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = c;
      ctx.beginPath();
      ctx.arc(px[i], py[i], r, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,0.55)';
      ctx.beginPath();
      ctx.arc(px[i] - r * 0.32, py[i] - r * 0.32, r * 0.3, 0, Math.PI * 2);
      ctx.fill();
    }

    if (count === 0) {
      ctx.fillStyle = 'rgba(232,238,251,0.7)';
      ctx.font = '700 15px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Tap anywhere to drop a ball!', w / 2, h * 0.4);
    }

    countOut.set(`${count} / ${MAX_N}`);
    badge.set(count === 0 ? 'Tap anywhere to drop a ball!' : `Bouncing on g = ${g.toFixed(1)} m/s²`);
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
