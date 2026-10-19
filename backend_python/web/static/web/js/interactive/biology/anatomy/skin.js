import { meshFromField } from './mesher.js';

function maxFilter(src, nx, ny, nz, r, axis) {
  const out = new Uint8Array(src.length);
  const stride = axis === 0 ? 1 : axis === 1 ? nx : nx * ny;
  const n = axis === 0 ? nx : axis === 1 ? ny : nz;
  const total = nx * ny * nz;
  for (let base = 0; base < total; base++) {
    const c = axis === 0 ? base % nx : axis === 1 ? Math.floor(base / nx) % ny : Math.floor(base / (nx * ny));
    if (c !== 0) continue;
    let count = 0;
    for (let k = 0; k < Math.min(n, r + 1); k++) count += src[base + k * stride];
    for (let k = 0; k < n; k++) {
      out[base + k * stride] = count > 0 ? 1 : 0;
      const add = k + r + 1; const rem = k - r;
      if (add < n) count += src[base + add * stride];
      if (rem >= 0) count -= src[base + rem * stride];
    }
  }
  return out;
}

function boxBlur(src, nx, ny, nz, r, axis) {
  const out = new Float32Array(src.length);
  const stride = axis === 0 ? 1 : axis === 1 ? nx : nx * ny;
  const n = axis === 0 ? nx : axis === 1 ? ny : nz;
  const total = nx * ny * nz;
  const w = 1 / (2 * r + 1);
  for (let base = 0; base < total; base++) {
    const c = axis === 0 ? base % nx : axis === 1 ? Math.floor(base / nx) % ny : Math.floor(base / (nx * ny));
    if (c !== 0) continue;
    let sum = 0;
    for (let k = -r; k <= r; k++) sum += src[base + Math.min(n - 1, Math.max(0, k)) * stride];
    for (let k = 0; k < n; k++) {
      out[base + k * stride] = sum * w;
      sum += src[base + Math.min(n - 1, k + r + 1) * stride] - src[base + Math.max(0, k - r) * stride];
    }
  }
  return out;
}

export function buildEnvelope(positions, bounds, cell, opts = {}) {
  const [x0, y0, z0] = bounds.min;
  const nx = Math.ceil((bounds.max[0] - x0) / cell) + 1;
  const ny = Math.ceil((bounds.max[1] - y0) / cell) + 1;
  const nz = Math.ceil((bounds.max[2] - z0) / cell) + 1;
  let occ = new Uint8Array(nx * ny * nz);
  for (let i = 0; i < positions.length; i += 3) {
    const a = Math.round((positions[i] - x0) / cell); const b = Math.round((positions[i + 1] - y0) / cell); const c = Math.round((positions[i + 2] - z0) / cell);
    if (a > 0 && b > 0 && c > 0 && a < nx - 1 && b < ny - 1 && c < nz - 1) occ[(c * ny + b) * nx + a] = 1;
  }
  const dil = opts.dilate ?? 2;
  for (let ax = 0; ax < 3; ax++) occ = maxFilter(occ, nx, ny, nz, dil, ax);
  const outside = new Uint8Array(nx * ny * nz);
  const queue = new Int32Array(nx * ny * nz);
  let head = 0; let tail = 0;
  const push = (i) => { if (!occ[i] && !outside[i]) { outside[i] = 1; queue[tail++] = i; } };
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    if (i === 0 || j === 0 || k === 0 || i === nx - 1 || j === ny - 1 || k === nz - 1) push((k * ny + j) * nx + i);
  }
  while (head < tail) {
    const id = queue[head++];
    const i = id % nx; const j = Math.floor(id / nx) % ny; const k = Math.floor(id / (nx * ny));
    if (i > 0) push(id - 1); if (i < nx - 1) push(id + 1);
    if (j > 0) push(id - nx); if (j < ny - 1) push(id + nx);
    if (k > 0) push(id - nx * ny); if (k < nz - 1) push(id + nx * ny);
  }
  let f = new Float32Array(nx * ny * nz);
  for (let i = 0; i < f.length; i++) f[i] = outside[i] ? 0 : 1;
  const br = opts.blur ?? 1;
  for (let it = 0; it < (opts.blurPasses ?? 2); it++) for (let ax = 0; ax < 3; ax++) f = boxBlur(f, nx, ny, nz, br, ax);
  const t = opts.threshold ?? 0.5;
  for (let i = 0; i < f.length; i++) f[i] = (t - f[i]) * cell * 4;
  return meshFromField(f, nx, ny, nz, [x0, y0, z0], cell);
}
