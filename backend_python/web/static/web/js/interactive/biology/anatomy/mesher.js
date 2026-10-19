export function surfaceNets(sdf, bounds, cell, opts = {}) {
  const [x0, y0, z0] = bounds.min;
  const nx = Math.ceil((bounds.max[0] - x0) / cell) + 1;
  const ny = Math.ceil((bounds.max[1] - y0) / cell) + 1;
  const nz = Math.ceil((bounds.max[2] - z0) / cell) + 1;
  const field = new Float32Array(nx * ny * nz);
  const p = [0, 0, 0];
  const B = 4;
  const cx = Math.ceil((nx - 1) / B) + 1; const cy = Math.ceil((ny - 1) / B) + 1; const cz = Math.ceil((nz - 1) / B) + 1;
  const coarse = new Float32Array(cx * cy * cz);
  for (let k = 0; k < cz; k++) for (let j = 0; j < cy; j++) for (let i = 0; i < cx; i++) {
    p[0] = x0 + i * B * cell; p[1] = y0 + j * B * cell; p[2] = z0 + k * B * cell;
    coarse[(k * cy + j) * cx + i] = sdf(p);
  }
  const band = B * cell * 1.9;
  for (let k = 0; k < nz; k++) {
    const kc = Math.min(cz - 2, Math.floor(k / B)); const fz = k / B - kc;
    p[2] = z0 + k * cell;
    for (let j = 0; j < ny; j++) {
      const jc = Math.min(cy - 2, Math.floor(j / B)); const fy = j / B - jc;
      p[1] = y0 + j * cell;
      const row = (k * ny + j) * nx;
      for (let i = 0; i < nx; i++) {
        const ic = Math.min(cx - 2, Math.floor(i / B)); const fx = i / B - ic;
        const c0 = (kc * cy + jc) * cx + ic;
        const a000 = coarse[c0]; const a100 = coarse[c0 + 1]; const a010 = coarse[c0 + cx]; const a110 = coarse[c0 + cx + 1];
        const a001 = coarse[c0 + cx * cy]; const a101 = coarse[c0 + cx * cy + 1]; const a011 = coarse[c0 + cx * cy + cx]; const a111 = coarse[c0 + cx * cy + cx + 1];
        const lo = Math.min(Math.abs(a000), Math.abs(a100), Math.abs(a010), Math.abs(a110), Math.abs(a001), Math.abs(a101), Math.abs(a011), Math.abs(a111));
        if (lo > band && (a000 > 0) === (a111 > 0) && (a000 > 0) === (a100 > 0) && (a000 > 0) === (a011 > 0)) {
          const x00 = a000 + (a100 - a000) * fx; const x10 = a010 + (a110 - a010) * fx;
          const x01 = a001 + (a101 - a001) * fx; const x11 = a011 + (a111 - a011) * fx;
          const y0v = x00 + (x10 - x00) * fy; const y1v = x01 + (x11 - x01) * fy;
          field[row + i] = y0v + (y1v - y0v) * fz;
        } else {
          p[0] = x0 + i * cell;
          field[row + i] = sdf(p);
        }
      }
    }
  }
  return meshFromField(field, nx, ny, nz, [x0, y0, z0], cell, sdf, opts);
}

export function meshFromField(field, nx, ny, nz, origin, cell, sdf = null, opts = {}) {
  const [x0, y0, z0] = origin;
  const idx = (i, j, k) => (k * ny + j) * nx + i;
  const cellIndex = new Int32Array((nx - 1) * (ny - 1) * (nz - 1)).fill(-1);
  const cid = (i, j, k) => (k * (ny - 1) + j) * (nx - 1) + i;
  const pos = [];
  const corners = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]];
  const edges = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
  const val = new Float32Array(8);
  for (let k = 0; k < nz - 1; k++) {
    for (let j = 0; j < ny - 1; j++) {
      for (let i = 0; i < nx - 1; i++) {
        let mask = 0;
        for (let c = 0; c < 8; c++) {
          const o = corners[c];
          val[c] = field[idx(i + o[0], j + o[1], k + o[2])];
          if (val[c] < 0) mask |= 1 << c;
        }
        if (mask === 0 || mask === 255) continue;
        let sx = 0; let sy = 0; let sz = 0; let n = 0;
        for (const [a, b] of edges) {
          const va = val[a]; const vb = val[b];
          if ((va < 0) === (vb < 0)) continue;
          const t = va / (va - vb);
          const ca = corners[a]; const cb = corners[b];
          sx += ca[0] + (cb[0] - ca[0]) * t; sy += ca[1] + (cb[1] - ca[1]) * t; sz += ca[2] + (cb[2] - ca[2]) * t;
          n++;
        }
        cellIndex[cid(i, j, k)] = pos.length / 3;
        pos.push(x0 + (i + sx / n) * cell, y0 + (j + sy / n) * cell, z0 + (k + sz / n) * cell);
      }
    }
  }
  const index = [];
  const quad = (a, b, c, d, flip) => {
    if (a < 0 || b < 0 || c < 0 || d < 0) return;
    if (flip) index.push(a, b, c, a, c, d);
    else index.push(a, c, b, a, d, c);
  };
  for (let k = 1; k < nz - 1; k++) {
    for (let j = 1; j < ny - 1; j++) {
      for (let i = 1; i < nx - 1; i++) {
        const v0 = field[idx(i, j, k)];
        const s0 = v0 < 0;
        if (i < nx - 1 && (field[idx(i + 1, j, k)] < 0) !== s0) {
          quad(cellIndex[cid(i, j - 1, k - 1)], cellIndex[cid(i, j, k - 1)], cellIndex[cid(i, j, k)], cellIndex[cid(i, j - 1, k)], s0);
        }
        if (j < ny - 1 && (field[idx(i, j + 1, k)] < 0) !== s0) {
          quad(cellIndex[cid(i - 1, j, k - 1)], cellIndex[cid(i - 1, j, k)], cellIndex[cid(i, j, k)], cellIndex[cid(i, j, k - 1)], s0);
        }
        if (k < nz - 1 && (field[idx(i, j, k + 1)] < 0) !== s0) {
          quad(cellIndex[cid(i - 1, j - 1, k)], cellIndex[cid(i, j - 1, k)], cellIndex[cid(i, j, k)], cellIndex[cid(i - 1, j, k)], s0);
        }
      }
    }
  }
  const count = pos.length / 3;
  const P = new Float32Array(pos);
  const N = new Float32Array(count * 3);
  const e = cell * 0.5;
  const q = [0, 0, 0];
  const steps = opts.project ?? 0;
  const F = (i, j, k) => field[idx(Math.min(nx - 1, Math.max(0, i)), Math.min(ny - 1, Math.max(0, j)), Math.min(nz - 1, Math.max(0, k)))];
  for (let vi = 0; vi < count; vi++) {
    let x = P[vi * 3]; let y = P[vi * 3 + 1]; let z = P[vi * 3 + 2];
    let gx = 0; let gy = 0; let gz = 0;
    if (!sdf || opts.gridNormals !== false) {
      const fx = (x - x0) / cell; const fy = (y - y0) / cell; const fz = (z - z0) / cell;
      const i0 = Math.floor(fx); const j0 = Math.floor(fy); const k0 = Math.floor(fz);
      const tx = fx - i0; const ty = fy - j0; const tz = fz - k0;
      for (let c = 0; c < 8; c++) {
        const di = c & 1; const dj = (c >> 1) & 1; const dk = (c >> 2) & 1;
        const w = (di ? tx : 1 - tx) * (dj ? ty : 1 - ty) * (dk ? tz : 1 - tz);
        const i = i0 + di; const j = j0 + dj; const k = k0 + dk;
        gx += w * (F(i + 1, j, k) - F(i - 1, j, k));
        gy += w * (F(i, j + 1, k) - F(i, j - 1, k));
        gz += w * (F(i, j, k + 1) - F(i, j, k - 1));
      }
      const gl = Math.hypot(gx, gy, gz) || 1;
      gx /= gl; gy /= gl; gz /= gl;
    } else {
      for (let s = 0; s <= steps; s++) {
        q[0] = x + e; q[1] = y; q[2] = z; const a = sdf(q); q[0] = x - e; const b = sdf(q);
        q[0] = x; q[1] = y + e; const c = sdf(q); q[1] = y - e; const d = sdf(q);
        q[1] = y; q[2] = z + e; const f = sdf(q); q[2] = z - e; const g = sdf(q);
        gx = a - b; gy = c - d; gz = f - g;
        const gl = Math.hypot(gx, gy, gz) || 1;
        gx /= gl; gy /= gl; gz /= gl;
        if (s < steps) {
          q[0] = x; q[1] = y; q[2] = z;
          const dist = sdf(q);
          if (Math.abs(dist) < cell) { x -= gx * dist; y -= gy * dist; z -= gz * dist; }
        }
      }
    }
    P[vi * 3] = x; P[vi * 3 + 1] = y; P[vi * 3 + 2] = z;
    N[vi * 3] = gx; N[vi * 3 + 1] = gy; N[vi * 3 + 2] = gz;
  }
  return { position: P, normal: N, index: count > 65535 ? new Uint32Array(index) : new Uint16Array(index), count };
}

export function toGeometry(THREE, mesh, attrs = {}) {
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(mesh.position, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(mesh.normal, 3));
  Object.entries(attrs).forEach(([k, [arr, size]]) => geo.setAttribute(k, new THREE.BufferAttribute(arr, size)));
  geo.setIndex(new THREE.BufferAttribute(mesh.index, 1));
  geo.computeBoundingSphere();
  return geo;
}

export function vertexAttribute(mesh, size, fn) {
  const out = new Float32Array(mesh.count * size);
  const p = [0, 0, 0]; const n = [0, 0, 0];
  for (let i = 0; i < mesh.count; i++) {
    p[0] = mesh.position[i * 3]; p[1] = mesh.position[i * 3 + 1]; p[2] = mesh.position[i * 3 + 2];
    n[0] = mesh.normal[i * 3]; n[1] = mesh.normal[i * 3 + 1]; n[2] = mesh.normal[i * 3 + 2];
    const r = fn(p, n, i);
    if (size === 1) out[i] = r;
    else for (let c = 0; c < size; c++) out[i * size + c] = r[c];
  }
  return out;
}
