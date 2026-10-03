export function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a += 0x6d2b79f5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function hashString(text) {
  let h = 2166136261;
  for (let i = 0; i < text.length; i += 1) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

export function rng(seed) {
  const next = mulberry32(typeof seed === 'string' ? hashString(seed) : seed);
  const api = () => next();
  api.range = (a, b) => a + (b - a) * next();
  api.int = (a, b) => Math.floor(a + (b - a + 1) * next());
  api.pick = (list) => list[Math.floor(next() * list.length)];
  api.sign = () => (next() < 0.5 ? -1 : 1);
  return api;
}
