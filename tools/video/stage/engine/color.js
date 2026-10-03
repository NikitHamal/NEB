import { clamp, lerp } from './math.js';

const cache = new Map();

export function parseHex(hex) {
  const hit = cache.get(hex);
  if (hit) return hit;
  let h = hex.replace('#', '');
  if (h.length === 3) h = [...h].map((c) => c + c).join('');
  const rgb = [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  cache.set(hex, rgb);
  return rgb;
}

export const toHex = ([r, g, b]) => `#${[r, g, b].map((v) => Math.round(clamp(v, 0, 255)).toString(16).padStart(2, '0')).join('')}`;
export const mixRgb = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
export const mixHex = (a, b, t) => toHex(mixRgb(parseHex(a), parseHex(b), t));
export const rgba = (hex, alpha = 1) => {
  const [r, g, b] = parseHex(hex);
  return `rgba(${r},${g},${b},${alpha})`;
};
export const hsl = (h, s, l, a = 1) => `hsla(${Math.round(h)},${Math.round(s)}%,${Math.round(l)}%,${a})`;
export const luminance = (hex) => {
  const [r, g, b] = parseHex(hex).map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
