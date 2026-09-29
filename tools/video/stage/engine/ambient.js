import { TAU } from './math.js';
import { rng } from './rng.js';

export function makeAmbient(S) {
  const canvas = S.mk('canvas', { class: 'fill', width: S.W, height: S.H });
  const ctx = canvas.getContext('2d');
  const r = rng(21);
  const count = S.portrait ? 24 : 36;
  const base = Math.min(S.W, S.H) * 0.03;
  const items = Array.from({ length: count }, (_, i) => ({
    x: r(),
    y: r(),
    z: r(),
    rot: r() * TAU,
    spin: r.range(0.4, 1.3) * r.sign(),
    flip: r.range(0.6, 1.6),
    phase: r() * TAU,
    paper: i % 4 === 0,
    size: r.range(0.75, 1.3),
    speed: r.range(0.016, 0.034),
    sway: r.range(0.008, 0.024),
    tint: r.pick(['#F7A8B8', '#FFC2D0', '#FF9FB5', '#FFD3DD']),
  }));

  const petal = (size, tint) => {
    const g = ctx.createLinearGradient(0, -size, 0, size);
    g.addColorStop(0, '#FFFFFF');
    g.addColorStop(0.35, tint);
    g.addColorStop(1, '#F27A96');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.moveTo(0, -size);
    ctx.bezierCurveTo(size * 0.95, -size * 0.35, size * 0.7, size * 0.65, 0, size);
    ctx.bezierCurveTo(-size * 0.7, size * 0.65, -size * 0.95, -size * 0.35, 0, -size);
    ctx.fill();
  };

  const paper = (size) => {
    const w = size * 1.5;
    const h = size * 2;
    ctx.fillStyle = 'rgba(0,40,120,0.10)';
    ctx.beginPath();
    ctx.roundRect(-w / 2 + size * 0.1, -h / 2 + size * 0.16, w, h, size * 0.14);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.roundRect(-w / 2, -h / 2, w, h, size * 0.14);
    ctx.fill();
    ctx.fillStyle = 'rgba(0,74,198,0.28)';
    for (let k = 0; k < 4; k += 1) {
      ctx.beginPath();
      ctx.roundRect(-w / 2 + size * 0.28, -h / 2 + size * (0.42 + k * 0.36), w - size * (0.56 + (k % 2) * 0.4), size * 0.11, size * 0.05);
      ctx.fill();
    }
  };

  return {
    canvas,
    draw(t, alpha) {
      ctx.clearRect(0, 0, S.W, S.H);
      if (alpha < 0.01) return;
      for (const it of items) {
        const depth = 0.45 + 0.55 * it.z;
        const fall = (it.y + t * it.speed * depth) % 1.2;
        const y = (fall - 0.1) * S.H;
        const drift = it.x + Math.sin(t * 0.55 + it.phase) * it.sway * 3 - t * it.speed * 0.35 * depth;
        const x = ((((drift % 1.1) + 1.1) % 1.1) - 0.05) * S.W;
        const size = base * it.size * (0.55 + 0.9 * depth);
        const flip = Math.abs(Math.cos(t * it.flip + it.phase));
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(it.rot + t * it.spin * 0.5);
        ctx.globalAlpha = alpha * (0.4 + 0.55 * depth);
        if (it.paper) {
          ctx.scale(1, 0.35 + 0.65 * flip);
          paper(size);
        } else {
          ctx.scale(0.4 + 0.6 * flip, 1);
          petal(size, it.tint);
        }
        ctx.restore();
      }
    },
  };
}
