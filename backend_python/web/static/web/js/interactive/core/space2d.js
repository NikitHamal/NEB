/**
 * space2d — the night-sky look shared by the 2D space labs: a pre-rendered starfield (drawn once
 * per size, then blitted), soft glows for stars and engines, and star colours from temperature
 * (a blackbody fit to sRGB).
 */
import { clamp, withAlpha, pill as pillLight } from './kit2d.js';

export function starfield(k, ctx, w, h, opt) {
  const key = 'stars' + ((opt && opt.seed) || 1);
  const c = k.cache(key, () => {
    const cv = document.createElement('canvas');
    cv.width = Math.max(1, Math.round(w * k.dpr)); cv.height = Math.max(1, Math.round(h * k.dpr));
    const g = cv.getContext('2d');
    const bg = g.createRadialGradient(cv.width * 0.5, cv.height * 0.4, 0, cv.width * 0.5, cv.height * 0.5, Math.max(cv.width, cv.height) * 0.8);
    bg.addColorStop(0, '#0f1a33'); bg.addColorStop(1, '#04070f');
    g.fillStyle = bg; g.fillRect(0, 0, cv.width, cv.height);
    let s = (opt && opt.seed) || 1;
    const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    // a faint band of the Milky Way
    g.save(); g.translate(cv.width * 0.5, cv.height * 0.5); g.rotate(-0.5);
    const band = g.createLinearGradient(0, -cv.height * 0.18, 0, cv.height * 0.18);
    band.addColorStop(0, 'rgba(120,140,200,0)'); band.addColorStop(0.5, 'rgba(120,140,200,0.07)'); band.addColorStop(1, 'rgba(120,140,200,0)');
    g.fillStyle = band; g.fillRect(-cv.width, -cv.height * 0.18, cv.width * 2, cv.height * 0.36); g.restore();
    const n = Math.round(w * h / 900);
    for (let i = 0; i < n; i++) {
      const x = rnd() * cv.width, y = rnd() * cv.height, m = rnd();
      const r = (m > 0.985 ? 1.6 : m > 0.9 ? 1.0 : 0.6) * k.dpr;
      const t = rnd();
      g.fillStyle = t < 0.15 ? `rgba(255,210,170,${0.4 + m * 0.6})` : t < 0.3 ? `rgba(170,200,255,${0.4 + m * 0.6})` : `rgba(255,255,255,${0.3 + m * 0.7})`;
      g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
    }
    return cv;
  });
  ctx.drawImage(c, 0, 0, w, h);
}

const glowCache = new Map();
/** A soft radial glow (cached sprite per colour). */
export function glow(ctx, x, y, r, color, alpha = 1) {
  if (r <= 0.5) return;
  let s = glowCache.get(color);
  if (!s) {
    s = document.createElement('canvas'); s.width = s.height = 128;
    const g = s.getContext('2d');
    const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    gr.addColorStop(0, withAlpha(color, 1)); gr.addColorStop(0.22, withAlpha(color, 0.5)); gr.addColorStop(0.55, withAlpha(color, 0.12)); gr.addColorStop(1, withAlpha(color, 0));
    g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
    glowCache.set(color, s);
  }
  ctx.globalAlpha = alpha; ctx.globalCompositeOperation = 'lighter';
  ctx.drawImage(s, x - r, y - r, r * 2, r * 2);
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
}

/** sRGB colour of a blackbody at T kelvin (Tanner Helland's fit), as #rrggbb. */
export function starColor(T) {
  const t = clamp(T, 1000, 40000) / 100;
  let r, g, b;
  if (t <= 66) { r = 255; g = 99.47 * Math.log(t) - 161.12; b = t <= 19 ? 0 : 138.52 * Math.log(t - 10) - 305.04; }
  else { r = 329.7 * Math.pow(t - 60, -0.1332); g = 288.12 * Math.pow(t - 60, -0.0755); b = 255; }
  const R = Math.round(clamp(r, 0, 255)), G = Math.round(clamp(g, 0, 255)), B = Math.round(clamp(b, 0, 255));
  return '#' + ((1 << 24) | (R << 16) | (G << 8) | B).toString(16).slice(1);
}

/** A label pill for dark skies. */
export function npill(ctx, s, x, y, color, size) {
  return pillDark(ctx, s, x, y, color, size);
}
function pillDark(ctx, s, x, y, color, size) {
  return pillLight(ctx, s, x, y, { bg: 'rgba(10,18,36,0.86)', border: 'rgba(160,190,255,0.22)', color: color || '#e8eefb', size: size || 11 });
}
