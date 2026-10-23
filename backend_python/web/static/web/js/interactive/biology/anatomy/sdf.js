export const v = (x, y, z) => [x, y, z];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const len = (a) => Math.sqrt(dot(a, a));
export const norm = (a) => { const l = len(a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];

export function smin(a, b, k) {
  if (k <= 0) return Math.min(a, b);
  const h = Math.max(k - Math.abs(a - b), 0) / k;
  return Math.min(a, b) - h * h * k * 0.25;
}

export function smax(a, b, k) { return -smin(-a, -b, k); }

export function frame(axis) {
  const y = norm(axis);
  const t = Math.abs(y[1]) < 0.9 ? [0, 1, 0] : [1, 0, 0];
  const x = norm(cross(t, y));
  const z = cross(x, y);
  return { x, y, z };
}

export function ellipsoid(c, r, axis = null, roll = 0) {
  const f = axis ? frame(axis) : { x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1] };
  if (roll) {
    const cr = Math.cos(roll); const sr = Math.sin(roll);
    const x = f.x; const z = f.z;
    f.x = [x[0] * cr + z[0] * sr, x[1] * cr + z[1] * sr, x[2] * cr + z[2] * sr];
    f.z = cross(f.x, f.y);
  }
  const bound = Math.max(r[0], r[1], r[2]);
  const [ax, ay, az] = f.x; const [bx, by, bz] = f.y; const [cx, cy, cz] = f.z;
  const [r0, r1, r2] = r; const [ox, oy, oz] = c;
  const rmin = Math.min(r0, r1, r2);
  const fn = (p) => {
    const dx = p[0] - ox; const dy = p[1] - oy; const dz = p[2] - oz;
    const q0 = (dx * ax + dy * ay + dz * az) / r0; const q1 = (dx * bx + dy * by + dz * bz) / r1; const q2 = (dx * cx + dy * cy + dz * cz) / r2;
    const k0 = Math.sqrt(q0 * q0 + q1 * q1 + q2 * q2);
    const s0 = q0 / r0; const s1 = q1 / r1; const s2 = q2 / r2;
    const k1 = Math.sqrt(s0 * s0 + s1 * s1 + s2 * s2);
    return k1 > 1e-9 ? k0 * (k0 - 1) / k1 : -rmin;
  };
  fn.center = c; fn.bound = bound;
  return fn;
}

export function capsule(a, b, ra, rb = ra) {
  const bax = b[0] - a[0]; const bay = b[1] - a[1]; const baz = b[2] - a[2];
  const l2 = bax * bax + bay * bay + baz * baz;
  const dr = rb - ra;
  const fn = (p) => {
    const px = p[0] - a[0]; const py = p[1] - a[1]; const pz = p[2] - a[2];
    let h = (px * bax + py * bay + pz * baz) / l2;
    h = h < 0 ? 0 : h > 1 ? 1 : h;
    const dx = px - bax * h; const dy = py - bay * h; const dz = pz - baz * h;
    return Math.sqrt(dx * dx + dy * dy + dz * dz) - (ra + dr * h);
  };
  fn.center = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2];
  return fn;
}

export function tube(points, r0, r1 = r0) {
  const segs = [];
  let total = 0;
  for (let i = 0; i < points.length - 1; i++) { const l = len(sub(points[i + 1], points[i])); segs.push(l); total += l; }
  let acc = 0;
  const caps = [];
  let cx = 0; let cy = 0; let cz = 0;
  points.forEach((q) => { cx += q[0]; cy += q[1]; cz += q[2]; });
  const C = [cx / points.length, cy / points.length, cz / points.length];
  let R = 0;
  for (let i = 0; i < points.length - 1; i++) {
    const ta = acc / total; acc += segs[i]; const tb = acc / total;
    const ra = r0 + (r1 - r0) * ta; const rb = r0 + (r1 - r0) * tb;
    const a = points[i]; const b = points[i + 1];
    const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2];
    caps.push({ f: capsule(a, b, ra, rb), m, r: segs[i] / 2 + Math.max(ra, rb) });
    R = Math.max(R, len(sub(a, C)) + Math.max(ra, rb), len(sub(b, C)) + Math.max(ra, rb));
  }
  const fn = (p) => {
    const ex = p[0] - C[0]; const ey = p[1] - C[1]; const ez = p[2] - C[2];
    const dc = Math.sqrt(ex * ex + ey * ey + ez * ez) - R;
    if (dc > 1.5) return dc;
    let d = Infinity;
    const x = p[0]; const y = p[1]; const z = p[2];
    for (const c of caps) {
      const mx = x - c.m[0]; const my = y - c.m[1]; const mz = z - c.m[2];
      const lb = Math.sqrt(mx * mx + my * my + mz * mz) - c.r;
      if (lb > d) continue;
      d = Math.min(d, c.f(p));
    }
    return d;
  };
  fn.center = points[Math.floor(points.length / 2)];
  return fn;
}

export function plane(n, d) {
  const nn = norm(n);
  return (p) => dot(p, nn) - d;
}

export function sphere(c, r) { const fn = (p) => len(sub(p, c)) - r; fn.center = c; return fn; }

export function catmull(points, samples = 8) {
  const out = [];
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[Math.max(0, i - 1)]; const p1 = points[i]; const p2 = points[i + 1]; const p3 = points[Math.min(points.length - 1, i + 2)];
    for (let s = 0; s < samples; s++) {
      const t = s / samples; const t2 = t * t; const t3 = t2 * t;
      out.push([0, 1, 2].map((k) => 0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3)));
    }
  }
  out.push(points[points.length - 1]);
  return out;
}

export function hash3(x, y, z) {
  const h = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453;
  return h - Math.floor(h);
}

export function vnoise(x, y, z) {
  const ix = Math.floor(x); const iy = Math.floor(y); const iz = Math.floor(z);
  const fx = x - ix; const fy = y - iy; const fz = z - iz;
  const ux = fx * fx * (3 - 2 * fx); const uy = fy * fy * (3 - 2 * fy); const uz = fz * fz * (3 - 2 * fz);
  const l = (a, b, t) => a + (b - a) * t;
  return l(
    l(l(hash3(ix, iy, iz), hash3(ix + 1, iy, iz), ux), l(hash3(ix, iy + 1, iz), hash3(ix + 1, iy + 1, iz), ux), uy),
    l(l(hash3(ix, iy, iz + 1), hash3(ix + 1, iy, iz + 1), ux), l(hash3(ix, iy + 1, iz + 1), hash3(ix + 1, iy + 1, iz + 1), ux), uy),
    uz,
  );
}
