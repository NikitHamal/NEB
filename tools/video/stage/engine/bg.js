import { clamp } from './math.js';
import { inOutCubic } from './ease.js';
import { mixHex, rgba } from './color.js';
import { makeNoise } from './noise.js';

const LAYOUT = [
  { ax: 0.18, ay: 0.22, r: 0.62, sx: 0.11, sy: 0.09 },
  { ax: 0.82, ay: 0.16, r: 0.55, sx: 0.08, sy: 0.12 },
  { ax: 0.1, ay: 0.86, r: 0.58, sx: 0.1, sy: 0.08 },
  { ax: 0.9, ay: 0.82, r: 0.6, sx: 0.09, sy: 0.1 },
  { ax: 0.5, ay: 0.52, r: 0.48, sx: 0.12, sy: 0.07 },
  { ax: 0.55, ay: 0.1, r: 0.4, sx: 0.06, sy: 0.06 },
];

export function makeBackground(S) {
  const w = 480;
  const h = Math.max(2, Math.round((w * S.H) / S.W));
  const canvas = S.mk('canvas', { class: 'fill', width: w, height: h });
  const ctx = canvas.getContext('2d');
  const noise = makeNoise(11);
  const stops = S.spec.background;
  const blendBeats = 1;

  function paletteAt(t) {
    const b = t / S.bd;
    let i = stops.length - 1;
    while (i > 0 && stops[i].beat > b) i -= 1;
    const cur = stops[i];
    const next = stops[i + 1];
    if (!next) return cur;
    const start = next.beat - blendBeats;
    if (b <= start) return cur;
    const k = inOutCubic(clamp((b - start) / blendBeats));
    return {
      base: mixHex(cur.base, next.base, k),
      blobs: cur.blobs.map((c, j) => mixHex(c, next.blobs[j % next.blobs.length], k)),
    };
  }

  return {
    canvas,
    draw(t) {
      const pal = paletteAt(t);
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = pal.base;
      ctx.fillRect(0, 0, w, h);
      pal.blobs.forEach((color, i) => {
        const L = LAYOUT[i % LAYOUT.length];
        const x = (L.ax + noise.noise2(i * 3.1, t * L.sx) * 0.24) * w;
        const y = (L.ay + noise.noise2(i * 5.7 + 9, t * L.sy) * 0.24) * h;
        const r = L.r * Math.max(w, h) * (0.92 + 0.12 * noise.noise2(i * 2.3 + 4, t * 0.07));
        const g = ctx.createRadialGradient(x, y, 0, x, y, r);
        g.addColorStop(0, rgba(color, 0.95));
        g.addColorStop(1, rgba(color, 0));
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, w, h);
      });
    },
  };
}
