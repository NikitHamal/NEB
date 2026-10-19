import { ellipsoid, sphere, tube, smin, smax, norm, catmull } from '../anatomy/sdf.js';
import { surfaceNets } from '../anatomy/mesher.js';

const HEART_ROUGH = ellipsoid([0.4, -0.6, 0.8], [5.4, 6.2, 4.6], [0.42, -0.83, 0.39]);

function lungSDF(side) {
  const s = side === 'left' ? 1 : -1;
  const body0 = ellipsoid([s * 6.7, 0.6, -0.4], [side === 'left' ? 4.6 : 5.0, 10.6, 6.8], [s * -0.08, 1, 0.05]);
  const q = [0, 0, 0];
  const body = (p) => {
    const t = Math.min(1.15, Math.max(0.5, 1.0 - (p[1] - 0.6) * 0.035));
    q[0] = s * 1.7 + (p[0] - s * 1.7) / t; q[1] = p[1]; q[2] = -0.4 + (p[2] + 0.4) / (0.75 + 0.25 * t);
    return body0(q) * t;
  };
  const apex = ellipsoid([s * 5.4, 9.0, -0.6], [2.6, 3.4, 2.8]);
  const dome = sphere([s * 6.0, -15.6, 0.4], 9.4);
  const fiss = norm([0, 11, 10]);
  const hz = norm([0, 1, 0.08]);
  return {
    sdf(p) {
      let d = smin(body(p), apex(p), 2.2);
      d = smax(d, 1.7 - s * p[0], 1.6);
      d = smax(d, -dome(p), 1.1);
      d = smax(d, p[2] - 5.4, 1.2);
      d = smax(d, -(HEART_ROUGH(p) + (side === 'left' ? 0.9 : 0.2)), 1.4);
      const ob = p[1] * fiss[1] + p[2] * fiss[2] - (side === 'left' ? 0.9 : 0.4);
      d = smax(d, -(Math.abs(ob) - 0.13), 0.22);
      if (side === 'right') {
        const h = p[1] * hz[1] + p[2] * hz[2] - 1.4;
        if (ob > 0) d = smax(d, -(Math.abs(h) - 0.12), 0.2);
      }
      return d;
    },
    lobe(p) {
      const ob = p[1] * fiss[1] + p[2] * fiss[2] - (side === 'left' ? 0.9 : 0.4);
      if (side === 'left') return ob > 0 ? 'lul' : 'lll';
      const h = p[1] * hz[1] + p[2] * hz[2] - 1.4;
      return ob < 0 ? 'rll' : h > 0 ? 'rul' : 'rml';
    },
  };
}

export const LOBES = {
  rul: 'Right upper lobe', rml: 'Right middle lobe', rll: 'Right lower lobe', lul: 'Left upper lobe', lll: 'Left lower lobe',
};

export function buildLungs(quality) {
  const cell = quality.tier === 'low' ? 0.34 : quality.tier === 'medium' ? 0.27 : 0.22;
  const out = {};
  for (const side of ['right', 'left']) {
    const L = lungSDF(side);
    const s = side === 'left' ? 1 : -1;
    const min = side === 'left' ? [0.6, -10.5, -8] : [-12.4, -10.5, -8];
    const max = side === 'left' ? [12.4, 13.4, 6.8] : [-0.6, 13.4, 6.8];
    const mesh = surfaceNets((p) => L.sdf(p), { min, max }, cell);
    const lobe = new Float32Array(mesh.count);
    const names = Object.keys(LOBES);
    const p = [0, 0, 0];
    for (let i = 0; i < mesh.count; i++) {
      p[0] = mesh.position[i * 3]; p[1] = mesh.position[i * 3 + 1]; p[2] = mesh.position[i * 3 + 2];
      lobe[i] = names.indexOf(L.lobe(p));
    }
    out[side] = { mesh, lobe, sdf: L.sdf, sign: s };
  }
  return out;
}

export const AIRWAY = {
  trachea: catmull([[0, 15.5, -0.4], [0, 11.0, -0.8], [0, 7.6, -1.2], [0, 6.0, -1.5]], 6),
  right: catmull([[0, 6.0, -1.5], [-1.6, 5.0, -1.7], [-3.4, 3.6, -2.0]], 5),
  left: catmull([[0, 6.0, -1.5], [1.9, 5.3, -1.8], [3.9, 4.0, -2.2]], 5),
};

export function airwaySDF() {
  const t = tube(AIRWAY.trachea, 1.0, 0.95);
  const r = tube(AIRWAY.right, 0.8, 0.7);
  const l = tube(AIRWAY.left, 0.7, 0.62);
  const tl = tube(AIRWAY.trachea, 0.82, 0.78);
  const rl = tube(AIRWAY.right, 0.62, 0.54);
  const ll = tube(AIRWAY.left, 0.53, 0.47);
  return (p) => {
    const outer = smin(t(p), smin(r(p), l(p), 0.6), 0.6);
    if (outer > 0.5) return outer;
    const inner = smin(tl(p), smin(rl(p), ll(p), 0.4), 0.4);
    return smax(outer, -inner, 0.08);
  };
}

export function buildAirway(quality) {
  return surfaceNets(airwaySDF(), { min: [-4.6, 2.4, -3.6], max: [5.0, 16.0, 1.0] }, quality.tier === 'low' ? 0.16 : 0.11);
}

export function bronchialTree(lungs, seed = 3, depth = 7) {
  let s = seed;
  const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  const branches = [];
  function grow(start, dir, r, gen, side) {
    const L = lungs[side];
    const length = Math.max(0.6, 3.4 * Math.pow(0.78, gen));
    let end = [start[0] + dir[0] * length, start[1] + dir[1] * length, start[2] + dir[2] * length];
    let tries = 0;
    while (L.sdf(end) > -0.6 && tries++ < 6) {
      const toCore = norm([L.sign * 6.5 - end[0], 0.5 - end[1], -0.4 - end[2]]);
      dir = norm([dir[0] + toCore[0] * 0.6, dir[1] + toCore[1] * 0.6, dir[2] + toCore[2] * 0.6]);
      end = [start[0] + dir[0] * length * 0.8, start[1] + dir[1] * length * 0.8, start[2] + dir[2] * length * 0.8];
    }
    branches.push({ a: start, b: end, r, gen });
    if (gen >= depth) return;
    const t1 = norm([dir[1] + 0.3, -dir[0] + (rnd() - 0.5), dir[2] + (rnd() - 0.5)]);
    for (const sgn of [-1, 1]) {
      const ang = 0.45 + rnd() * 0.25;
      const nd = norm([
        dir[0] * Math.cos(ang) + t1[0] * Math.sin(ang) * sgn,
        dir[1] * Math.cos(ang) + t1[1] * Math.sin(ang) * sgn,
        dir[2] * Math.cos(ang) + t1[2] * Math.sin(ang) * sgn,
      ]);
      grow(end, nd, r * 0.76, gen + 1, side);
    }
  }
  grow(AIRWAY.right[AIRWAY.right.length - 1], norm([-0.5, -0.7, 0.1]), 0.5, 1, 'right');
  grow(AIRWAY.right[AIRWAY.right.length - 1], norm([-0.4, 0.8, 0.2]), 0.42, 2, 'right');
  grow(AIRWAY.left[AIRWAY.left.length - 1], norm([0.5, -0.75, 0.1]), 0.46, 1, 'left');
  grow(AIRWAY.left[AIRWAY.left.length - 1], norm([0.35, 0.85, 0.25]), 0.4, 2, 'left');
  return branches;
}

export function diaphragmSDF() {
  const leftDome = sphere([5.4, -13.9, 0.2], 8.4);
  const rightDome = sphere([-5.4, -13.5, 0.2], 8.4);
  return (p) => {
    const shellR = smin(rightDome(p), leftDome(p), 3.0);
    let d = Math.abs(shellR) - 0.18;
    d = smax(d, -p[1] - 7.6, 0.5);
    d = smax(d, Math.hypot(p[0] / 1.15, p[2] / 0.8) - 9.6, 0.8);
    return d;
  };
}

export function buildDiaphragm(quality) {
  return surfaceNets(diaphragmSDF(), { min: [-14.5, -10.2, -10.5], max: [14.5, -3.0, 10.5] }, quality.tier === 'low' ? 0.32 : 0.24);
}
