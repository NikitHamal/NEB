import { clamp } from './math.js';

const c1 = 1.70158;
const c3 = c1 + 1;
const c4 = (2 * Math.PI) / 3;

export const linear = (t) => t;
export const inQuad = (t) => t * t;
export const outQuad = (t) => 1 - (1 - t) * (1 - t);
export const inOutQuad = (t) => (t < 0.5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2);
export const inCubic = (t) => t ** 3;
export const outCubic = (t) => 1 - (1 - t) ** 3;
export const inOutCubic = (t) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2);
export const inQuart = (t) => t ** 4;
export const outQuart = (t) => 1 - (1 - t) ** 4;
export const inOutQuart = (t) => (t < 0.5 ? 8 * t ** 4 : 1 - (-2 * t + 2) ** 4 / 2);
export const inQuint = (t) => t ** 5;
export const outQuint = (t) => 1 - (1 - t) ** 5;
export const inOutQuint = (t) => (t < 0.5 ? 16 * t ** 5 : 1 - (-2 * t + 2) ** 5 / 2);
export const inExpo = (t) => (t <= 0 ? 0 : 2 ** (10 * t - 10));
export const outExpo = (t) => (t >= 1 ? 1 : 1 - 2 ** (-10 * t));
export const inOutExpo = (t) => {
  if (t <= 0) return 0;
  if (t >= 1) return 1;
  return t < 0.5 ? 2 ** (20 * t - 10) / 2 : (2 - 2 ** (-20 * t + 10)) / 2;
};
export const inCirc = (t) => 1 - Math.sqrt(1 - t * t);
export const outCirc = (t) => Math.sqrt(1 - (t - 1) ** 2);
export const inOutCirc = (t) => (t < 0.5 ? (1 - Math.sqrt(1 - (2 * t) ** 2)) / 2 : (Math.sqrt(1 - (-2 * t + 2) ** 2) + 1) / 2);
export const inBack = (t) => c3 * t ** 3 - c1 * t ** 2;
export const outBack = (t) => 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2;
export const inOutBack = (t) => {
  const c2 = c1 * 1.525;
  return t < 0.5 ? ((2 * t) ** 2 * ((c2 + 1) * 2 * t - c2)) / 2 : ((2 * t - 2) ** 2 * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2;
};
export const outElastic = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : 2 ** (-10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1);
export const outBounce = (t) => {
  const n1 = 7.5625;
  const d1 = 2.75;
  if (t < 1 / d1) return n1 * t * t;
  if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
  if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
  return n1 * (t -= 2.625 / d1) * t + 0.984375;
};

export const backWith = (overshoot) => (t) => 1 + (overshoot + 1) * (t - 1) ** 3 + overshoot * (t - 1) ** 2;

export function bezier(x1, y1, x2, y2) {
  const cx = 3 * x1;
  const bx = 3 * (x2 - x1) - cx;
  const ax = 1 - cx - bx;
  const cy = 3 * y1;
  const by = 3 * (y2 - y1) - cy;
  const ay = 1 - cy - by;
  const sampleX = (s) => ((ax * s + bx) * s + cx) * s;
  const sampleY = (s) => ((ay * s + by) * s + cy) * s;
  const slopeX = (s) => (3 * ax * s + 2 * bx) * s + cx;
  return (x) => {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let s = x;
    for (let i = 0; i < 8; i += 1) {
      const err = sampleX(s) - x;
      if (Math.abs(err) < 1e-6) return sampleY(s);
      const slope = slopeX(s);
      if (Math.abs(slope) < 1e-6) break;
      s -= err / slope;
    }
    let lo = 0;
    let hi = 1;
    s = x;
    for (let i = 0; i < 24; i += 1) {
      const v = sampleX(s);
      if (Math.abs(v - x) < 1e-6) break;
      if (x > v) lo = s;
      else hi = s;
      s = (hi - lo) / 2 + lo;
    }
    return sampleY(s);
  };
}

export const spring = (zeta = 0.5, omega = 14) => {
  const wd = omega * Math.sqrt(1 - zeta * zeta);
  const decay = zeta * omega;
  return (u) => {
    if (u <= 0) return 0;
    if (u >= 1) return 1;
    return 1 - Math.exp(-decay * u) * (Math.cos(wd * u) + (decay / wd) * Math.sin(wd * u));
  };
};

export const smooth = bezier(0.65, 0, 0.35, 1);
export const swift = bezier(0.2, 0.9, 0.1, 1);
export const punch = bezier(0.16, 1, 0.3, 1);

export const clamped = (fn) => (t) => fn(clamp(t));
