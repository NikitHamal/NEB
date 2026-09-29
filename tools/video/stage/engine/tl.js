import { clamp, lerp } from './math.js';
import { linear } from './ease.js';

export const seg = (t, start, dur, ease = linear) => ease(clamp(dur <= 0 ? (t >= start ? 1 : 0) : (t - start) / dur));

export function keys(t, frames, ease = linear) {
  if (t <= frames[0][0]) return frames[0][1];
  const last = frames[frames.length - 1];
  if (t >= last[0]) return last[1];
  for (let i = 0; i < frames.length - 1; i += 1) {
    const [t0, v0] = frames[i];
    const [t1, v1] = frames[i + 1];
    if (t >= t0 && t <= t1) return lerp(v0, v1, ease((t - t0) / (t1 - t0)));
  }
  return last[1];
}

export const stagger = (t, index, { start = 0, step = 0.04, dur = 0.4, ease = linear } = {}) => seg(t, start + index * step, dur, ease);

export const decay = (t, at, tau) => (t < at ? 0 : Math.exp(-(t - at) / tau));

export const window = (t, from, to, edge = 0.001) => {
  if (t < from || t > to) return 0;
  return Math.min(1, (t - from) / edge, (to - t) / edge);
};
