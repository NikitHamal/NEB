/**
 * kit2d-plot — axes, nice ticks and live curves for the 2D labs. A Plot caches its tick labels
 * until its range or box changes, so drawing it every frame allocates nothing.
 */
import { T, font, card } from './kit2d.js';

export function niceStep(range, target) {
  const raw = range / Math.max(1, target);
  const p = Math.pow(10, Math.floor(Math.log10(raw)));
  const m = raw / p;
  return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p;
}

function tickText(v, step) {
  const d = step >= 1 ? 0 : Math.min(4, Math.ceil(-Math.log10(step) - 1e-9));
  const s = v.toFixed(d);
  return s === '-0' || /^-0\.0+$/.test(s) ? s.slice(1) : s;
}

export class Plot {
  constructor(o = {}) {
    this.xMin = o.xMin ?? 0; this.xMax = o.xMax ?? 1; this.yMin = o.yMin ?? 0; this.yMax = o.yMax ?? 1;
    this.xLabel = o.xLabel || ''; this.yLabel = o.yLabel || ''; this.title = o.title || '';
    this.x = 0; this.y = 0; this.w = 100; this.h = 100;
    this.pad = { l: 44, r: 12, t: o.title ? 28 : 12, b: 34 };
    this.cardBg = o.card !== false;
    this._key = ''; this._xt = []; this._yt = [];
    this.xTicks = o.xTicks || 6; this.yTicks = o.yTicks || 5;
  }
  box(x, y, w, h) { this.x = x; this.y = y; this.w = w; this.h = h; return this; }
  range(xMin, xMax, yMin, yMax) { this.xMin = xMin; this.xMax = xMax; this.yMin = yMin; this.yMax = yMax; return this; }
  get ix() { return this.x + this.pad.l; }
  get iy() { return this.y + this.pad.t; }
  get iw() { return Math.max(1, this.w - this.pad.l - this.pad.r); }
  get ih() { return Math.max(1, this.h - this.pad.t - this.pad.b); }
  X(v) { return this.ix + (v - this.xMin) / (this.xMax - this.xMin) * this.iw; }
  Y(v) { return this.iy + this.ih - (v - this.yMin) / (this.yMax - this.yMin) * this.ih; }
  invX(px) { return this.xMin + (px - this.ix) / this.iw * (this.xMax - this.xMin); }
  invY(py) { return this.yMin + (this.iy + this.ih - py) / this.ih * (this.yMax - this.yMin); }
  inside(px, py) { return px >= this.ix && px <= this.ix + this.iw && py >= this.iy && py <= this.iy + this.ih; }
  _ticks() {
    const key = this.xMin + ',' + this.xMax + ',' + this.yMin + ',' + this.yMax + ',' + this.w + ',' + this.h;
    if (key === this._key) return;
    this._key = key;
    const build = (a, b, n) => {
      const st = niceStep(b - a, n);
      const out = [];
      for (let v = Math.ceil(a / st - 1e-9) * st; v <= b + st * 1e-6; v += st) out.push({ v, s: tickText(v, st) });
      return out;
    };
    this._xt = build(this.xMin, this.xMax, Math.max(2, Math.min(this.xTicks, Math.floor(this.iw / 56))));
    this._yt = build(this.yMin, this.yMax, Math.max(2, Math.min(this.yTicks, Math.floor(this.ih / 30))));
  }
  frame(ctx, opt) {
    this._ticks();
    const th = (opt && opt.theme) || T;
    if (this.cardBg) card(ctx, this.x, this.y, this.w, this.h, 12, th.paper);
    const ix = this.ix, iy = this.iy, iw = this.iw, ih = this.ih;
    ctx.lineWidth = 1;
    ctx.strokeStyle = th.line2;
    ctx.beginPath();
    for (const t of this._xt) { const px = Math.round(this.X(t.v)) + 0.5; ctx.moveTo(px, iy); ctx.lineTo(px, iy + ih); }
    for (const t of this._yt) { const py = Math.round(this.Y(t.v)) + 0.5; ctx.moveTo(ix, py); ctx.lineTo(ix + iw, py); }
    ctx.stroke();
    ctx.strokeStyle = th.line; ctx.lineWidth = 1.2;
    ctx.beginPath();
    const y0 = this.yMin <= 0 && this.yMax >= 0 ? this.Y(0) : iy + ih;
    const x0 = this.xMin <= 0 && this.xMax >= 0 ? this.X(0) : ix;
    ctx.moveTo(ix, y0); ctx.lineTo(ix + iw, y0); ctx.moveTo(x0, iy); ctx.lineTo(x0, iy + ih);
    ctx.stroke();
    ctx.font = font(10, 500); ctx.fillStyle = th.mute;
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    for (const t of this._xt) ctx.fillText(t.s, this.X(t.v), iy + ih + 5);
    ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
    for (const t of this._yt) ctx.fillText(t.s, ix - 6, this.Y(t.v));
    ctx.font = font(10.5, 600); ctx.fillStyle = th.ink2;
    if (this.xLabel) { ctx.textAlign = 'right'; ctx.textBaseline = 'bottom'; ctx.fillText(this.xLabel, ix + iw, this.y + this.h - 3); }
    if (this.yLabel) { ctx.textAlign = 'left'; ctx.textBaseline = 'top'; ctx.fillText(this.yLabel, this.title ? ix + ctx.measureText(this.title).width + 30 : ix + 4, this.title ? this.y + 9 : iy + 2); }
    if (this.title) { ctx.font = font(11.5, 700); ctx.fillStyle = th.ink; ctx.textAlign = 'left'; ctx.textBaseline = 'top'; ctx.fillText(this.title, this.x + 12, this.y + 9); }
  }
  clip(ctx) { ctx.save(); ctx.beginPath(); ctx.rect(this.ix, this.iy, this.iw, this.ih); ctx.clip(); }
  unclip(ctx) { ctx.restore(); }
  /** Plot y = f(x) across the box. */
  fn(ctx, f, color, width = 2, steps = 160) {
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {
      const xv = this.xMin + (this.xMax - this.xMin) * i / steps;
      const yv = f(xv);
      const px = this.X(xv), py = this.Y(yv);
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.strokeStyle = color; ctx.lineWidth = width; ctx.stroke();
  }
  /** Plot a Ring buffer of samples. */
  ring(ctx, r, color, width = 2) {
    if (r.n < 2) return;
    ctx.beginPath();
    for (let i = 0; i < r.n; i++) {
      const j = r.idx(i);
      const px = this.X(r.x[j]), py = this.Y(r.y[j]);
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.strokeStyle = color; ctx.lineWidth = width; ctx.stroke();
  }
  dot(ctx, xv, yv, color, r = 4) {
    ctx.beginPath(); ctx.arc(this.X(xv), this.Y(yv), r, 0, Math.PI * 2);
    ctx.fillStyle = color; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
  }
}
