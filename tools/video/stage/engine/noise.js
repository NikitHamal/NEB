import { mulberry32 } from './rng.js';

const F2 = 0.5 * (Math.sqrt(3) - 1);
const G2 = (3 - Math.sqrt(3)) / 6;
const GRAD = [[1, 1], [-1, 1], [1, -1], [-1, -1], [1, 0], [-1, 0], [0, 1], [0, -1]];

export function makeNoise(seed = 1) {
  const rand = mulberry32(seed);
  const perm = new Uint8Array(512);
  const base = Array.from({ length: 256 }, (_, i) => i);
  for (let i = 255; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [base[i], base[j]] = [base[j], base[i]];
  }
  for (let i = 0; i < 512; i += 1) perm[i] = base[i & 255];

  const noise2 = (xin, yin) => {
    const s = (xin + yin) * F2;
    const i = Math.floor(xin + s);
    const j = Math.floor(yin + s);
    const t = (i + j) * G2;
    const x0 = xin - (i - t);
    const y0 = yin - (j - t);
    const i1 = x0 > y0 ? 1 : 0;
    const j1 = x0 > y0 ? 0 : 1;
    const x1 = x0 - i1 + G2;
    const y1 = y0 - j1 + G2;
    const x2 = x0 - 1 + 2 * G2;
    const y2 = y0 - 1 + 2 * G2;
    const ii = i & 255;
    const jj = j & 255;
    const corner = (x, y, gi) => {
      const t0 = 0.5 - x * x - y * y;
      if (t0 < 0) return 0;
      const g = GRAD[gi % 8];
      return t0 * t0 * t0 * t0 * (g[0] * x + g[1] * y);
    };
    return 70 * (corner(x0, y0, perm[ii + perm[jj]]) + corner(x1, y1, perm[ii + i1 + perm[jj + j1]]) + corner(x2, y2, perm[ii + 1 + perm[jj + 1]]));
  };

  const fbm2 = (x, y, octaves = 4, gain = 0.5, lacunarity = 2) => {
    let amp = 1;
    let freq = 1;
    let sum = 0;
    let norm = 0;
    for (let o = 0; o < octaves; o += 1) {
      sum += amp * noise2(x * freq, y * freq);
      norm += amp;
      amp *= gain;
      freq *= lacunarity;
    }
    return sum / norm;
  };

  return { noise2, fbm2 };
}
