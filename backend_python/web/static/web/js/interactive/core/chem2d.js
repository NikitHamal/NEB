/**
 * chem2d — glassware and pouring for the 2D chemistry labs. Vessels are drawn back-glass,
 * contents, front-glass (with a meniscus and printed graduations), so liquids look like they sit
 * inside the glass. A Shelf of bottles, shakers and spoons can be dragged over a vessel: the
 * container tilts and pours (or sprinkles) only while it is held over the mouth.
 */
import { T, Spring, clamp, text, withAlpha, softShadow, mix } from './kit2d.js';

/** Particle pool for bubbles, grains and drops. */
export class Pool {
  constructor(cap) {
    this.cap = cap; this.x = new Float32Array(cap); this.y = new Float32Array(cap); this.vx = new Float32Array(cap); this.vy = new Float32Array(cap);
    this.r = new Float32Array(cap); this.life = new Float32Array(cap); this.kind = new Uint8Array(cap); this.n = 0;
  }
  add(x, y, vx, vy, r, life, kind = 0) {
    if (this.n >= this.cap) return -1;
    const i = this.n++;
    this.x[i] = x; this.y[i] = y; this.vx[i] = vx; this.vy[i] = vy; this.r[i] = r; this.life[i] = life; this.kind[i] = kind;
    return i;
  }
  kill(i) {
    const j = --this.n;
    if (i === j) return;
    this.x[i] = this.x[j]; this.y[i] = this.y[j]; this.vx[i] = this.vx[j]; this.vy[i] = this.vy[j]; this.r[i] = this.r[j]; this.life[i] = this.life[j]; this.kind[i] = this.kind[j];
  }
  clear() { this.n = 0; }
}

/** A beaker or cylinder. v = { x (centre), y (bottom), w, h, r (corner), capacity (mL), lip }. */
export function vesselBack(ctx, v) {
  ctx.fillStyle = 'rgba(214,230,248,0.35)';
  ctx.beginPath(); ctx.roundRect(v.x - v.w / 2, v.y - v.h, v.w, v.h, [2, 2, v.r || 10, v.r || 10]); ctx.fill();
}

/** Fill from the bottom: liquid top at height hTop (px above the vessel bottom). */
export function liquid(ctx, v, y0, y1, color, alpha = 0.85) {
  if (y1 <= y0 + 0.2) return;
  const inset = 3, left = v.x - v.w / 2 + inset, w = v.w - inset * 2;
  const top = v.y - y1, bot = v.y - y0;
  ctx.fillStyle = withAlpha(color, alpha);
  ctx.beginPath();
  if (y0 < (v.r || 10)) ctx.roundRect(left, top, w, bot - top - inset * 0.5, [0, 0, Math.max(0, (v.r || 10) - inset), Math.max(0, (v.r || 10) - inset)]);
  else ctx.rect(left, top, w, bot - top);
  ctx.fill();
}

export function meniscus(ctx, v, hTop, color) {
  const left = v.x - v.w / 2 + 3, right = v.x + v.w / 2 - 3, y = v.y - hTop;
  ctx.strokeStyle = withAlpha(mix(color, '#ffffff', 0.5), 0.9); ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(left, y - 3); ctx.quadraticCurveTo(left + 4, y, left + 10, y); ctx.lineTo(right - 10, y); ctx.quadraticCurveTo(right - 4, y, right, y - 3); ctx.stroke();
}

export function vesselFront(ctx, v, opt) {
  const left = v.x - v.w / 2, top = v.y - v.h;
  ctx.strokeStyle = 'rgba(120,150,190,0.85)'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(left - (v.lip || 4), top); ctx.lineTo(left, top + 2); ctx.lineTo(left, v.y - (v.r || 10)); ctx.quadraticCurveTo(left, v.y, left + (v.r || 10), v.y);
  ctx.lineTo(v.x + v.w / 2 - (v.r || 10), v.y); ctx.quadraticCurveTo(v.x + v.w / 2, v.y, v.x + v.w / 2, v.y - (v.r || 10)); ctx.lineTo(v.x + v.w / 2, top + 2); ctx.lineTo(v.x + v.w / 2 + (v.lip || 4), top);
  ctx.stroke();
  ctx.fillStyle = 'rgba(255,255,255,0.5)'; ctx.fillRect(left + 5, top + 8, 4, v.h - 20);
  ctx.fillStyle = 'rgba(255,255,255,0.22)'; ctx.fillRect(left + 12, top + 8, 2, v.h - 30);
  if (opt && opt.capacity) {
    const step = opt.step || opt.capacity / 5, pxPer = (v.h - 10) / opt.capacity;
    ctx.strokeStyle = 'rgba(70,90,120,0.55)'; ctx.lineWidth = 1; ctx.beginPath();
    const minor = step / 5;
    for (let ml = minor; ml < opt.capacity + 0.01; ml += minor) { const yy = Math.round(v.y - ml * pxPer) + 0.5, big = Math.abs(ml / step - Math.round(ml / step)) < 1e-6; ctx.moveTo(v.x + v.w / 2 - (big ? 16 : 8), yy); ctx.lineTo(v.x + v.w / 2 - 2, yy); }
    ctx.stroke();
    for (let ml = step; ml < opt.capacity + 0.01; ml += step) text(ctx, ml + step > opt.capacity + 0.01 && opt.unit !== false ? Math.round(ml) + ' mL' : String(Math.round(ml)), v.x + v.w / 2 - 19, v.y - ml * pxPer + 3.5, 'rgba(70,90,120,0.8)', 9, 600, 'right');
  }
}

/**
 * A shelf of draggable containers. items: [{ id, label, color, kind: 'bottle'|'shaker'|'dropper'|'spoon'|'jar'|'object', sub }].
 * target(): { x, y (mouth), w } where pouring counts. onPour(item, dt, lipX, lipY) is called each
 * frame an item is tilted over the target; onDrop(item, x, y) when an 'object' is released.
 */
export function createShelf(k, items, opts) {
  const slots = items.map(() => ({ x: 0, y: 0, hx: new Spring(0, 180, 20), hy: new Spring(0, 180, 20), tilt: new Spring(0, 120, 14), hot: new Spring(0, 260, 26) }));
  let held = -1, pouring = false;
  const lip = { x: 0, y: 0 };
  function layout(x0, y0, w, h) {
    const n = items.length, gap = w / n;
    for (let i = 0; i < n; i++) { slots[i].x = x0 + gap * (i + 0.5); slots[i].y = y0 + h; if (held !== i) { slots[i].hx.set(slots[i].x); slots[i].hy.set(slots[i].y); } }
  }
  const handles = items.map((it, i) => k.drag({
    enabled: () => !opts.enabled || opts.enabled(it),
    hit: (x, y, s) => { const sl = slots[i]; return Math.abs(x - sl.hx.x) < 22 + s && y < sl.hy.x + 6 + s && y > sl.hy.x - 66 - s ? Math.abs(x - sl.hx.x) : false; },
    down: () => { held = i; k.animate(true); },
    move: (x, y) => { slots[i].hx.set(x); slots[i].hy.set(y + 30); },
    up: (x, y) => { if (it.kind === 'object' && opts.onDrop) opts.onDrop(it, x, y); held = -1; pouring = false; slots[i].hx.to(slots[i].x); slots[i].hy.to(slots[i].y); slots[i].tilt.to(0); k.animate(true); },
  }));
  function step(dt) {
    let moving = false;
    pouring = false;
    for (let i = 0; i < items.length; i++) {
      const sl = slots[i];
      sl.hot.to(k.isHot(handles[i]) || held === i ? 1 : 0);
      if (held === i && items[i].kind !== 'object') {
        const t = opts.target();
        const over = Math.abs(sl.hx.x - (t.x - 24)) < t.w * 0.75 + 30 && sl.hy.x < t.y + 10 && sl.hy.x > t.y - 220;
        sl.tilt.to(over ? (items[i].kind === 'bottle' || items[i].kind === 'jar' ? 1.9 : items[i].kind === 'spoon' ? 2.3 : 1.2) : 0);
        if (over && sl.tilt.x > 1) { pouring = true; tipOf(i, lip); opts.onPour(items[i], dt, lip.x, lip.y); }
      }
      if (sl.hx.step(dt)) moving = true;
      if (sl.hy.step(dt)) moving = true;
      if (sl.tilt.step(dt)) moving = true;
      if (sl.hot.step(dt)) moving = true;
    }
    return moving || held >= 0;
  }
  function tipOf(i, out) {
    const sl = slots[i], a = sl.tilt.x;
    const lx = 0, ly = items[i].kind === 'spoon' ? -6 : -58;
    out.x = sl.hx.x + lx * Math.cos(a) - ly * Math.sin(a);
    out.y = sl.hy.x + lx * Math.sin(a) + ly * Math.cos(a);
    return out;
  }
  function draw(ctx) {
    for (let i = 0; i < items.length; i++) if (i !== held) drawItem(ctx, i);
    if (held >= 0) drawItem(ctx, held);
  }
  function drawItem(ctx, i) {
    const it = items[i], sl = slots[i];
    const x = sl.hx.x, y = sl.hy.x, a = sl.tilt.x;
    if (held !== i) softShadow(ctx, x, y + 2, 20, 4, 0.22);
    ctx.save(); ctx.translate(x, y); ctx.rotate(a);
    const s = 1 + sl.hot.x * 0.06; ctx.scale(s, s);
    if (it.kind === 'bottle') {
      ctx.fillStyle = withAlpha(it.glass || '#dbeafe', 0.75); ctx.strokeStyle = 'rgba(100,130,170,0.8)'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(-16, 0); ctx.lineTo(-16, -34); ctx.quadraticCurveTo(-16, -44, -6, -46); ctx.lineTo(-6, -58); ctx.lineTo(6, -58); ctx.lineTo(6, -46); ctx.quadraticCurveTo(16, -44, 16, -34); ctx.lineTo(16, 0); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillStyle = withAlpha(it.color, 0.9); ctx.beginPath(); ctx.roundRect(-14, -30, 28, 28, [0, 0, 3, 3]); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.fillRect(-12, -24, 24, 10);
      text(ctx, it.sub || it.label.slice(0, 3), 0, -16, T.ink, 7.5, 700, 'center');
    } else if (it.kind === 'shaker') {
      ctx.fillStyle = '#f1f5f9'; ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.roundRect(-13, -44, 26, 44, 5); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#cbd5e1'; ctx.beginPath(); ctx.roundRect(-14, -58, 28, 15, [8, 8, 2, 2]); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#64748b'; for (let d = -1; d <= 1; d++) { ctx.beginPath(); ctx.arc(d * 6, -52, 1.6, 0, Math.PI * 2); ctx.fill(); }
      ctx.fillStyle = withAlpha(it.color, 0.9); ctx.fillRect(-11, -26, 22, 24);
    } else if (it.kind === 'dropper') {
      ctx.fillStyle = withAlpha(it.color, 0.85); ctx.strokeStyle = 'rgba(100,130,170,0.8)'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.roundRect(-10, -30, 20, 30, 4); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.roundRect(-6, -48, 12, 18, 5); ctx.fill();
      ctx.fillStyle = 'rgba(220,235,250,0.9)'; ctx.fillRect(-2, -60, 4, 13);
    } else if (it.kind === 'spoon' || it.kind === 'jar') {
      if (it.kind === 'jar') {
        ctx.fillStyle = 'rgba(219,234,254,0.7)'; ctx.strokeStyle = 'rgba(100,130,170,0.8)'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.roundRect(-17, -50, 34, 50, 6); ctx.fill(); ctx.stroke();
        ctx.fillStyle = withAlpha(it.color, 0.95); ctx.beginPath(); ctx.roundRect(-15, -30, 30, 28, [0, 0, 5, 5]); ctx.fill();
        ctx.fillStyle = '#94a3b8'; ctx.fillRect(-18, -58, 36, 8);
      } else {
        ctx.fillStyle = '#cbd5e1'; ctx.fillRect(-2, -60, 4, 46);
        ctx.beginPath(); ctx.ellipse(0, -8, 12, 9, 0, 0, Math.PI * 2); ctx.fillStyle = '#e2e8f0'; ctx.fill(); ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.2; ctx.stroke();
        ctx.beginPath(); ctx.ellipse(0, -10, 9, 5, 0, 0, Math.PI * 2); ctx.fillStyle = it.color; ctx.fill();
      }
    } else if (it.draw) it.draw(ctx, it);
    ctx.restore();
    if (held !== i) text(ctx, it.label, x, y + 16, T.ink2, k.small ? 8.5 : 10, 600, 'center');
  }
  return { layout, step, draw, get held() { return held >= 0 ? items[held] : null; }, get pouring() { return pouring; }, slots, handles, tipOf };
}

/** A falling stream from a lip to a surface. */
export function stream(ctx, x0, y0, x1, y1, color, width) {
  const g = Math.max(0, y1 - y0);
  ctx.strokeStyle = withAlpha(color, 0.85); ctx.lineWidth = width; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.quadraticCurveTo(x0 + (x1 - x0) * 0.2, y0 + g * 0.5, x1, y1); ctx.stroke();
}

export { clamp };
