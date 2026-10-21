import { ellipsoid, smin, smax } from '../../biology/anatomy/sdf.js';
import { surfaceNets, vertexAttribute } from '../../biology/anatomy/mesher.js';

// A high-altitude mountaineer sculpted as signed distance fields: an 8000 m down suit with stitched
// baffles, a fur-ruffed hood, oxygen mask, double boots and a pack. Three parts so the head can turn
// and the raised arm can wave: body (pivot at the ground), head (pivot at the neck), arm (shoulder).
// Every vertex takes the colour of the primitive it belongs to.

const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);

function puff(a, b, ra, rb, pitch, amp) {
  const bx = b[0] - a[0]; const by = b[1] - a[1]; const bz = b[2] - a[2];
  const L = Math.hypot(bx, by, bz); const l2 = L * L;
  return (p) => {
    const px = p[0] - a[0]; const py = p[1] - a[1]; const pz = p[2] - a[2];
    const h = clamp((px * bx + py * by + pz * bz) / l2, 0, 1);
    const dx = px - bx * h; const dy = py - by * h; const dz = pz - bz * h;
    const s = Math.sin(h * L / pitch * Math.PI);
    return Math.sqrt(dx * dx + dy * dy + dz * dz) - (ra + (rb - ra) * h) - amp * s * s;
  };
}

function roundBox(c, half, r) {
  return (p) => {
    const qx = Math.abs(p[0] - c[0]) - half[0] + r; const qy = Math.abs(p[1] - c[1]) - half[1] + r; const qz = Math.abs(p[2] - c[2]) - half[2] + r;
    const ox = Math.max(qx, 0); const oy = Math.max(qy, 0); const oz = Math.max(qz, 0);
    return Math.hypot(ox, oy, oz) + Math.min(Math.max(qx, qy, qz), 0) - r;
  };
}

function torusZ(c, R, r) {
  return (p) => {
    const x = p[0] - c[0]; const y = p[1] - c[1]; const z = p[2] - c[2];
    const q = Math.hypot(x, y * 0.86) - R;
    return Math.hypot(q, z) - r;
  };
}

const C = {
  suit: [0.82, 0.22, 0.08], panel: [0.07, 0.075, 0.09], boot: [0.93, 0.66, 0.08], sole: [0.05, 0.05, 0.05],
  glove: [0.06, 0.06, 0.07], fur: [0.42, 0.36, 0.3], mask: [0.11, 0.11, 0.12], pack: [0.11, 0.2, 0.36], belt: [0.08, 0.08, 0.1],
};

function build(parts, bounds, cell, blend) {
  const sdf = (p) => {
    let d = 1e9;
    for (const pt of parts) d = smin(d, pt.f(p), pt.k ?? blend);
    return d;
  };
  const mesh = surfaceNets(sdf, bounds, cell, { project: 1 });
  const color = vertexAttribute(mesh, 3, (p) => {
    let best = null; let bd = 1e9;
    for (const pt of parts) { const d = Math.abs(pt.f(p)); if (d < bd) { bd = d; best = pt; } }
    return typeof best.c === 'function' ? best.c(p) : best.c;
  });
  return { mesh, color };
}

export function buildClimber(tier) {
  const cell = tier === 'high' ? 0.0085 : tier === 'medium' ? 0.011 : 0.015;
  const _e3 = ellipsoid([0, 1.0, -0.005], [0.22, 0.17, 0.16]);
  const _e4 = ellipsoid([0, 1.21, 0], [0.24, 0.24, 0.17]);
  const _e5 = ellipsoid([0, 1.38, 0.005], [0.255, 0.16, 0.17]);
  const _e6 = ellipsoid([-0.302, 0.835, 0.185], [0.052, 0.068, 0.048], [0.05, 1, 0.3]);
  const _e7 = ellipsoid([0, 0.07, -0.005], [0.13, 0.15, 0.14]);
  const _e8 = ellipsoid([0, 0.065, 0.125], [0.066, 0.082, 0.05]);
  const _e9 = torusZ([0, 0.065, 0.112], 0.082, 0.028);
  const _e10 = ellipsoid([0, 0.005, 0.13], [0.052, 0.048, 0.044]);
  const _e11 = ellipsoid([0.158, 0.56, 0.09], [0.05, 0.072, 0.046], [0.2, 1, 0.15]);
  const _e12 = ellipsoid([0.125, 0.585, 0.11], [0.022, 0.04, 0.02], [0.3, 1, 0.4]);
  const legColor = (p) => (p[1] < 0.6 && p[1] > 0.33 && p[2] > -0.02 ? C.panel : C.suit);
  const body = [];
  [-1, 1].forEach((s) => {
    const x = 0.115 * s;
    const _e1 = puff([x, 0.075, -0.05], [x, 0.075, 0.12], 0.068, 0.06, 1, 0);
    const _e2 = puff([x, 0.07, -0.01], [x, 0.31, 0], 0.08, 0.078, 0.06, 0.004);
    const boot = (p) => smax(smin(_e1(p), _e2(p), 0.05), 0.004 - p[1], 0.01);
    body.push({ f: boot, c: (p) => (p[1] < 0.032 ? C.sole : p[1] > 0.27 ? C.panel : C.boot), k: 0.02 });
    body.push({ f: puff([x, 0.3, 0], [x * 1.04, 0.54, 0.035], 0.087, 0.094, 0.085, 0.006), c: legColor, k: 0.04 });
    body.push({ f: puff([x * 1.04, 0.54, 0.035], [x * 0.96, 0.95, 0], 0.094, 0.112, 0.085, 0.007), c: legColor, k: 0.05 });
  });
  body.push({ f: (p) => _e3(p), c: (p) => (p[1] > 0.955 && p[1] < 1.0 ? C.belt : C.suit), k: 0.08 });
  const torsoBaffle = (p) => { const s = Math.sin((p[1] - 1.0) / 0.085 * Math.PI); return -0.007 * s * s; };
  body.push({ f: (p) => _e4(p) + torsoBaffle(p), c: C.suit, k: 0.09 });
  body.push({ f: (p) => _e5(p) + torsoBaffle(p), c: (p) => (p[1] > 1.4 && Math.abs(p[0]) > 0.17 ? C.panel : C.suit), k: 0.08 });
  body.push({ f: puff([0, 1.45, 0], [0, 1.6, 0.01], 0.075, 0.07, 1, 0), c: C.suit, k: 0.06 });
  body.push({ f: puff([-0.235, 1.43, 0], [-0.33, 1.13, 0.06], 0.088, 0.08, 0.075, 0.006), c: C.suit, k: 0.05 });
  body.push({ f: puff([-0.33, 1.13, 0.06], [-0.305, 0.89, 0.165], 0.08, 0.07, 0.075, 0.005), c: C.suit, k: 0.04 });
  body.push({ f: (p) => _e6(p), c: C.glove, k: 0.03 });
  body.push({ f: roundBox([0, 1.17, -0.25], [0.16, 0.25, 0.1], 0.05), c: C.pack, k: 0.03 });
  body.push({ f: puff([-0.12, 1.4, -0.16], [-0.1, 1.0, -0.19], 0.022, 0.022, 1, 0), c: C.pack, k: 0.02 });
  body.push({ f: puff([0.12, 1.4, -0.16], [0.1, 1.0, -0.19], 0.022, 0.022, 1, 0), c: C.pack, k: 0.02 });
  const B = build(body, { min: [-0.46, -0.01, -0.4], max: [0.42, 1.68, 0.3] }, cell, 0.04);

  const head = [];
  head.push({ f: (p) => smax(_e7(p), -_e8(p), 0.02), c: C.suit, k: 0.03 });
  head.push({ f: (p) => _e9(p) + 0.006 * Math.sin(Math.atan2(p[1] - 0.065, p[0]) * 23) * Math.sin(p[2] * 300), c: C.fur, k: 0.015 });
  head.push({ f: (p) => _e10(p), c: C.mask, k: 0.012 });
  head.push({ f: puff([0.02, -0.01, 0.15], [0.04, -0.035, 0.172], 0.017, 0.015, 1, 0), c: C.mask, k: 0.01 });
  const H = build(head, { min: [-0.17, -0.1, -0.17], max: [0.17, 0.25, 0.22] }, cell * 0.7, 0.02);

  const arm = [];
  arm.push({ f: puff([0, 0, 0], [0.1, 0.25, 0.04], 0.088, 0.08, 0.075, 0.006), c: C.suit, k: 0.04 });
  arm.push({ f: puff([0.1, 0.25, 0.04], [0.15, 0.5, 0.08], 0.08, 0.07, 0.075, 0.005), c: C.suit, k: 0.04 });
  arm.push({ f: (p) => _e11(p), c: C.glove, k: 0.025 });
  arm.push({ f: (p) => _e12(p), c: C.glove, k: 0.015 });
  const A = build(arm, { min: [-0.12, -0.12, -0.12], max: [0.25, 0.66, 0.2] }, cell, 0.04);

  return { body: B, head: H, arm: A };
}
