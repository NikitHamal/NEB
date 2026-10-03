import { makeNoise } from './noise.js';
import { rng } from './rng.js';
import { svg } from './dom.js';

const LAYERS = [
  { fill: 'rgba(150,196,255,0.55)', base: 0.34, peaks: 6, hMin: 0.4, hMax: 0.95, wMin: 0.1, wMax: 0.2, rim: 'rgba(255,255,255,0.75)', seed: 3 },
  { fill: '#0A48BD', base: 0.2, peaks: 7, hMin: 0.3, hMax: 0.7, wMin: 0.09, wMax: 0.18, rim: 'rgba(160,200,255,0.45)', seed: 8 },
  { fill: '#04277A', base: 0.09, peaks: 8, hMin: 0.2, hMax: 0.5, wMin: 0.07, wMax: 0.15, rim: null, seed: 13 },
];

export function makeHills(S, { seed = 5 } = {}) {
  const noise = makeNoise(seed);
  const width = S.W * 1.16;
  const height = S.H * 0.6;
  const node = svg('svg', {
    width, height, viewBox: `0 0 ${width} ${height}`,
    style: { position: 'absolute', left: `${-(width - S.W) / 2}px`, top: `${S.H - height}px`, overflow: 'visible' },
  });
  const layers = LAYERS.map((L) => {
    const r = rng(L.seed);
    const peaks = Array.from({ length: L.peaks }, (_, i) => ({
      c: width * ((i + 0.5 + r.range(-0.3, 0.3)) / L.peaks),
      w: width * r.range(L.wMin, L.wMax),
      h: r.range(L.hMin, L.hMax),
    }));
    const pts = [];
    for (let x = 0; x <= width; x += 6) {
      let top = 0;
      for (const p of peaks) {
        const d = Math.abs(x - p.c) / p.w;
        if (d < 1) top = Math.max(top, p.h * (1 - d) ** 1.35);
      }
      const rough = noise.fbm2(x / 90 + L.seed, L.seed, 3, 0.5) * 0.018;
      pts.push([x, height * (1 - (L.base + (1 - L.base) * 0.62 * top + rough))]);
    }
    const line = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ');
    const g = svg('g', {}, [
      svg('path', { d: `${line} L${width},${height} L0,${height} Z`, fill: L.fill }),
      L.rim ? svg('path', { d: line, fill: 'none', stroke: L.rim, 'stroke-width': 3, 'stroke-linejoin': 'round' }) : null,
    ]);
    node.append(g);
    return { g, depth: L };
  });
  return { node, layers, height };
}
