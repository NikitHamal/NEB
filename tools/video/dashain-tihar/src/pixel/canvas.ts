// A tiny framebuffer for pixel art, drawn fresh every frame (a pure function of time, so renders
// are deterministic). Colours are packed for ImageData on little-endian: 0xAABBGGRR.

export type Col = number;

const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
export const bayer = (x: number, y: number) => (BAYER[(y & 3) * 4 + (x & 3)] + 0.5) / 16;

/** '#RRGGBB' (or with alpha 0..1) to a packed colour. */
export const rgb = (hex: string, a = 1): Col => {
  const n = parseInt(hex.slice(1), 16);
  const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  return ((Math.round(a * 255) << 24) | (b << 16) | (g << 8) | r) >>> 0;
};
export const mix = (a: Col, b: Col, t: number): Col => {
  const k = Math.max(0, Math.min(1, t));
  const ch = (s: number) => Math.round(((a >>> s) & 255) + ((((b >>> s) & 255) - ((a >>> s) & 255)) * k));
  return ((255 << 24) | (ch(16) << 16) | (ch(8) << 8) | ch(0)) >>> 0;
};

export class Px {
  data: Uint32Array;
  constructor(public w: number, public h: number) {
    this.data = new Uint32Array(w * h);
  }
  fill(c: Col) { this.data.fill(c); }
  set(x: number, y: number, c: Col) {
    x = Math.floor(x); y = Math.floor(y);
    if (x >= 0 && y >= 0 && x < this.w && y < this.h && c >>> 24) this.data[y * this.w + x] = c;
  }
  get(x: number, y: number): Col {
    return x >= 0 && y >= 0 && x < this.w && y < this.h ? this.data[y * this.w + x] : 0;
  }
  hline(x0: number, x1: number, y: number, c: Col) {
    y = Math.floor(y);
    if (y < 0 || y >= this.h) return;
    const a = Math.max(0, Math.floor(Math.min(x0, x1))), b = Math.min(this.w - 1, Math.floor(Math.max(x0, x1)));
    for (let x = a; x <= b; x++) this.data[y * this.w + x] = c;
  }
  rect(x: number, y: number, w: number, h: number, c: Col) {
    for (let yy = Math.floor(y); yy < Math.floor(y + h); yy++) this.hline(x, x + w - 1, yy, c);
  }
  line(x0: number, y0: number, x1: number, y1: number, c: Col) {
    x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1);
    const dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    let err = dx + dy;
    for (;;) {
      this.set(x0, y0, c);
      if (x0 === x1 && y0 === y1) return;
      const e2 = 2 * err;
      if (e2 >= dy) { err += dy; x0 += sx; }
      if (e2 <= dx) { err += dx; y0 += sy; }
    }
  }
  disc(cx: number, cy: number, r: number, c: Col) { this.ellipse(cx, cy, r, r, c); }
  ellipse(cx: number, cy: number, rx: number, ry: number, c: Col) {
    for (let y = Math.floor(cy - ry) - 1; y <= cy + ry + 1; y++)
      for (let x = Math.floor(cx - rx) - 1; x <= cx + rx + 1; x++) {
        const dx = (x + 0.5 - cx) / rx, dy = (y + 0.5 - cy) / ry;
        if (dx * dx + dy * dy <= 1) this.set(x, y, c);
      }
  }
  polygon(pts: number[], c: Col) {
    const n = pts.length / 2;
    let minY = Infinity, maxY = -Infinity;
    for (let i = 0; i < n; i++) { minY = Math.min(minY, pts[i * 2 + 1]); maxY = Math.max(maxY, pts[i * 2 + 1]); }
    for (let y = Math.max(0, Math.floor(minY)); y <= Math.min(this.h - 1, maxY); y++) {
      const sy = y + 0.5, xs: number[] = [];
      for (let i = 0; i < n; i++) {
        const ax = pts[i * 2], ay = pts[i * 2 + 1], bx = pts[((i + 1) % n) * 2], by = pts[((i + 1) % n) * 2 + 1];
        if ((ay <= sy && by > sy) || (by <= sy && ay > sy)) xs.push(ax + ((sy - ay) / (by - ay)) * (bx - ax));
      }
      xs.sort((a, b) => a - b);
      for (let k = 0; k + 1 < xs.length; k += 2) this.hline(Math.round(xs[k]), Math.round(xs[k + 1] - 0.5), y, c);
    }
  }
  dither(x: number, y: number, c: Col, amount: number) {
    if (amount > bayer(Math.floor(x), Math.floor(y))) this.set(x, y, c);
  }
  /** Vertical gradient between stops (posterised with ordered dithering). */
  vgrad(y0: number, y1: number, stops: Col[]) {
    for (let y = Math.max(0, Math.floor(y0)); y < Math.min(this.h, y1); y++) {
      const t = (y - y0) / Math.max(1, y1 - y0);
      const f = Math.min(0.9999, Math.max(0, t)) * (stops.length - 1);
      const i = Math.floor(f);
      for (let x = 0; x < this.w; x++) this.data[y * this.w + x] = f - i > bayer(x, y) ? stops[i + 1] : stops[i];
    }
  }
  /** A 1 px outline around everything drawn on a transparent buffer (use on sprite layers). */
  outline(c: Col) {
    const src = this.data.slice();
    for (let y = 0; y < this.h; y++)
      for (let x = 0; x < this.w; x++) {
        if (src[y * this.w + x] >>> 24) continue;
        const t = (xx: number, yy: number) => xx >= 0 && yy >= 0 && xx < this.w && yy < this.h && src[yy * this.w + xx] >>> 24;
        if (t(x - 1, y) || t(x + 1, y) || t(x, y - 1) || t(x, y + 1)) this.data[y * this.w + x] = c;
      }
  }
  /** Paint another buffer onto this one at (ox, oy), skipping transparent pixels. */
  stamp(src: Px, ox: number, oy: number) {
    ox = Math.round(ox); oy = Math.round(oy);
    for (let y = 0; y < src.h; y++) {
      const ty = y + oy;
      if (ty < 0 || ty >= this.h) continue;
      for (let x = 0; x < src.w; x++) {
        const c = src.data[y * src.w + x];
        const tx = x + ox;
        if (c >>> 24 && tx >= 0 && tx < this.w) this.data[ty * this.w + tx] = c;
      }
    }
  }
}

/** Paint [src] scaled by a whole number [k] (nearest neighbour), keeping pixels square. */
export const stampScaled = (dst: Px, src: Px, ox: number, oy: number, k: number) => {
  ox = Math.round(ox); oy = Math.round(oy);
  for (let y = 0; y < src.h; y++) for (let x = 0; x < src.w; x++) {
    const c = src.data[y * src.w + x];
    if (c >>> 24) dst.rect(ox + x * k, oy + y * k, k, k, c);
  }
};

/** Seeded random, so every frame of every render agrees. */
export const rnd = (seed: number) => {
  let s = seed >>> 0 || 1;
  return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; };
};
