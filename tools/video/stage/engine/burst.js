import { TAU } from './math.js';
import { rng } from './rng.js';

export function drawBurst(ctx, t, cfg) {
  const { t0, x, y, n = 40, speed = 700, life = 1, size = 18, colors, gravity = 0, drag = 3, angle = -Math.PI / 2, spread = TAU, seed = 1, shape = 'mix' } = cfg;
  const age = t - t0;
  if (age < 0 || age > life) return;
  const r = rng(seed);
  const fade = Math.min(1, (life - age) / (life * 0.4));
  for (let i = 0; i < n; i += 1) {
    const a = angle + (r() - 0.5) * spread;
    const v = speed * (0.3 + r() * 0.7);
    const travel = (v * (1 - Math.exp(-drag * age))) / drag;
    const px = x + Math.cos(a) * travel;
    const py = y + Math.sin(a) * travel + 0.5 * gravity * age * age;
    const s = size * (0.5 + r() * 0.9);
    const rot = r() * TAU + (r() - 0.5) * 9 * age;
    const color = colors[Math.floor(r() * colors.length)];
    const kind = shape === 'mix' ? (r() < 0.5 ? 'rect' : 'dot') : shape;
    const tumble = 0.35 + 0.65 * Math.abs(Math.cos(age * (3 + r() * 6) + r() * TAU));
    ctx.save();
    ctx.translate(px, py);
    ctx.rotate(rot);
    ctx.globalAlpha = fade;
    ctx.fillStyle = color;
    if (kind === 'rect') {
      ctx.scale(1, tumble);
      ctx.beginPath();
      ctx.roundRect(-s * 0.8, -s * 0.5, s * 1.6, s, s * 0.18);
      ctx.fill();
    } else {
      ctx.beginPath();
      ctx.arc(0, 0, s * 0.42, 0, TAU);
      ctx.fill();
    }
    ctx.restore();
  }
}
