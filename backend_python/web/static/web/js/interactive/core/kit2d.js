/**
 * kit2d — the shared look and runtime of the 2D (canvas) simulations.
 *
 * createKit(stage, opts) gives a HiDPI canvas (device pixel ratio capped lower on low-end
 * devices), a render loop that only runs while the stage is on screen and the tab is visible
 * (continuous while animating, otherwise one frame per invalidate()), direct manipulation with
 * mouse, pen and touch (a touch that starts on a handle never scrolls the page; any other touch
 * scrolls as usual), and the light theme of the lesson shell. Drawing helpers, springs and an
 * allocation-free RK4 integrator live alongside so every lab speaks the same visual language.
 */
export const T = {
  bg0: '#f8fafd', bg1: '#e8eef8', paper: '#ffffff', ink: '#172033', ink2: '#4a5770', mute: '#8794a9',
  line: '#cfd8e6', line2: '#e3e9f2', grid: 'rgba(37,99,235,0.07)', gridStrong: 'rgba(37,99,235,0.14)',
  blue: '#2563eb', blueDeep: '#004ac6', blueSoft: '#dbe6ff', blueFaint: 'rgba(37,99,235,0.10)',
  orange: '#f08c00', amber: '#f59e0b', red: '#e5484d', green: '#16a34a', teal: '#0d9488',
  purple: '#7c3aed', pink: '#db2777', yellow: '#eab308', sky: '#0ea5e9', slate: '#64748b',
  steel: '#9aa8bd', wood: '#c08a55', woodDark: '#8d5a2b', glass: 'rgba(170,200,235,0.28)',
  shadow: 'rgba(23,40,80,0.16)', font: 'Poppins, system-ui, -apple-system, sans-serif',
  mono: 'ui-monospace, SFMono-Regular, Menlo, monospace',
};

export const NIGHT = {
  bg0: '#0b1324', bg1: '#050912', paper: '#111b30', ink: '#e8eefb', ink2: '#aab8d3', mute: '#6f7f9e',
  line: '#2a3958', line2: '#1b2740', grid: 'rgba(140,170,255,0.06)', gridStrong: 'rgba(140,170,255,0.12)',
};

export const reducedMotion = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;

const lowEnd = (navigator.hardwareConcurrency || 4) <= 4 || (navigator.deviceMemory || 4) <= 2;

const fontCache = new Map();
export function font(size, weight = 500, family) {
  const key = size * 10000 + weight + (family ? 0.5 : 0);
  let f = fontCache.get(key);
  if (!f) { f = `${weight} ${size}px ${family || T.font}`; fontCache.set(key, f); }
  return f;
}

export const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
export const lerp = (a, b, t) => a + (b - a) * t;
export const easeOutCubic = (t) => 1 - (1 - t) * (1 - t) * (1 - t);
export const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const easeOutBack = (t) => { const c = 1.70158; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };

/** A critically-damped-ish spring: s.to(target); s.step(dt); read s.x. */
export class Spring {
  constructor(x = 0, stiffness = 170, damping = 22) { this.x = x; this.v = 0; this.target = x; this.k = stiffness; this.c = damping; }
  to(t) { this.target = t; return this; }
  set(x) { this.x = x; this.target = x; this.v = 0; return this; }
  step(dt) {
    if (reducedMotion) { this.x = this.target; this.v = 0; return false; }
    const n = Math.max(1, Math.ceil(dt / 0.008));
    const h = dt / n;
    for (let i = 0; i < n; i++) {
      const a = this.k * (this.target - this.x) - this.c * this.v;
      this.v += a * h; this.x += this.v * h;
    }
    if (Math.abs(this.v) < 1e-4 && Math.abs(this.target - this.x) < 1e-4) { this.x = this.target; this.v = 0; return false; }
    return true;
  }
  get moving() { return this.v !== 0 || this.x !== this.target; }
}

/** Classic RK4 over a Float64Array state; f(t, y, out) writes dy/dt. No allocation per step. */
export function makeRK4(n, f) {
  const k1 = new Float64Array(n), k2 = new Float64Array(n), k3 = new Float64Array(n), k4 = new Float64Array(n), tmp = new Float64Array(n);
  return function step(y, t, h) {
    f(t, y, k1);
    for (let i = 0; i < n; i++) tmp[i] = y[i] + 0.5 * h * k1[i];
    f(t + 0.5 * h, tmp, k2);
    for (let i = 0; i < n; i++) tmp[i] = y[i] + 0.5 * h * k2[i];
    f(t + 0.5 * h, tmp, k3);
    for (let i = 0; i < n; i++) tmp[i] = y[i] + h * k3[i];
    f(t + h, tmp, k4);
    for (let i = 0; i < n; i++) y[i] += (h / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
  };
}

/** Fixed-size ring buffer of (x, y) samples for trails and live graphs. */
export class Ring {
  constructor(cap) { this.cap = cap; this.x = new Float32Array(cap); this.y = new Float32Array(cap); this.n = 0; this.head = 0; }
  push(x, y) { this.x[this.head] = x; this.y[this.head] = y; this.head = (this.head + 1) % this.cap; if (this.n < this.cap) this.n++; }
  clear() { this.n = 0; this.head = 0; }
  idx(i) { return (this.head - this.n + i + this.cap) % this.cap; }
  get lastX() { return this.n ? this.x[(this.head - 1 + this.cap) % this.cap] : 0; }
  get lastY() { return this.n ? this.y[(this.head - 1 + this.cap) % this.cap] : 0; }
}

export function fmt(v, d = 2) {
  if (!isFinite(v)) return '—';
  const s = v.toFixed(d);
  return s === '-0' || /^-0\.0*$/.test(s) ? s.slice(1) : s;
}

export function createKit(stage, opts = {}) {
  const night = !!opts.night;
  const canvas = document.createElement('canvas');
  canvas.className = 'ix-sim-canvas ix-k2-canvas';
  canvas.setAttribute('role', 'img');
  if (opts.label) canvas.setAttribute('aria-label', opts.label);
  stage.appendChild(canvas);
  stage.classList.add('ix-k2-stage');
  if (night) stage.classList.add('ix-k2-night');
  const shell = stage.closest ? stage.closest('.ix-sim-shell') : null;
  if (shell) shell.classList.add(night ? 'ix-k2-dark' : 'ix-k2');
  const ctx = canvas.getContext('2d', { alpha: false });
  const dprCap = opts.dprCap || (lowEnd ? 1.5 : 2);

  const k = {
    canvas, ctx, stage, night, theme: night ? Object.assign({}, T, NIGHT) : T,
    w: 1, h: 1, dpr: 1, t: 0, small: false, reduced: reducedMotion,
    pointer: { x: -1e4, y: -1e4, inside: false, down: false, type: 'mouse' },
    hover: null, active: null,
  };
  let draw = null;
  let animating = false;
  let dirty = true;
  let onScreen = true;
  let pageVisible = !document.hidden;
  let raf = 0;
  let last = 0;
  let disposed = false;
  const resizeFns = [];
  const handles = [];
  const tapFns = [];
  const caches = new Map();

  function resize() {
    const w = stage.clientWidth || 1;
    const h = stage.clientHeight || 1;
    const dpr = Math.min(window.devicePixelRatio || 1, dprCap);
    if (w === k.w && h === k.h && dpr === k.dpr && canvas.width) { return; }
    k.w = w; k.h = h; k.dpr = dpr; k.small = w < 560;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    caches.clear();
    for (let i = 0; i < resizeFns.length; i++) resizeFns[i](w, h);
    dirty = true;
    renderNow(0);
    sync();
  }

  function renderNow(dt) {
    if (!draw) return;
    ctx.setTransform(k.dpr, 0, 0, k.dpr, 0, 0);
    ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
    draw(ctx, dt, k.w, k.h);
  }

  function frame(now) {
    raf = 0;
    const dt = Math.min((now - last) / 1000 || 0.016, 0.05);
    last = now;
    k.t += dt;
    dirty = false;
    renderNow(dt);
    sync();
  }

  function sync() {
    const run = !disposed && onScreen && pageVisible && (animating || dirty);
    if (run && !raf) { raf = requestAnimationFrame(frame); if (!animating) last = performance.now(); }
    else if (!run && raf) { cancelAnimationFrame(raf); raf = 0; }
  }

  const ro = new ResizeObserver(resize);
  ro.observe(stage);
  const io = new IntersectionObserver((e) => { onScreen = e[e.length - 1].isIntersecting; if (onScreen) last = performance.now(); sync(); }, { threshold: 0 });
  io.observe(stage);
  function onVis() { pageVisible = !document.hidden; if (pageVisible) last = performance.now(); sync(); }
  document.addEventListener('visibilitychange', onVis);

  function local(e) {
    const r = canvas.getBoundingClientRect();
    k.pointer.x = e.clientX - r.left; k.pointer.y = e.clientY - r.top;
  }
  function slack() { return k.pointer.type === 'touch' ? 26 : 12; }
  function pick(x, y) {
    const s = slack();
    let best = null, bestD = Infinity;
    for (let i = handles.length - 1; i >= 0; i--) {
      const hd = handles[i];
      if (hd.enabled && !hd.enabled()) continue;
      const d = hd.hit(x, y, s);
      if (d === false || d === null || d === undefined || d === -1) continue;
      const dist = d === true ? 0 : d;
      if (dist < bestD) { best = hd; bestD = dist; }
    }
    return best;
  }
  function onDown(e) {
    if (e.button > 0) return;
    k.pointer.type = e.pointerType || 'mouse';
    local(e);
    k.pointer.down = true;
    const hd = pick(k.pointer.x, k.pointer.y);
    if (hd) {
      k.active = hd; k.hover = hd;
      try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
      canvas.style.cursor = hd.cursorActive || 'grabbing';
      if (hd.down) hd.down(k.pointer.x, k.pointer.y, e);
      e.preventDefault();
    } else {
      k.tapStart = { x: k.pointer.x, y: k.pointer.y, t: performance.now() };
    }
    k.invalidate();
  }
  function onMove(e) {
    if (e.pointerType) k.pointer.type = e.pointerType;
    local(e);
    k.pointer.inside = true;
    if (k.active) {
      if (k.active.move) k.active.move(k.pointer.x, k.pointer.y, e);
      k.invalidate();
      return;
    }
    if (k.pointer.type !== 'touch') {
      const hd = pick(k.pointer.x, k.pointer.y);
      if (hd !== k.hover) { k.hover = hd; k.invalidate(); }
      canvas.style.cursor = hd ? (hd.cursor || 'grab') : (opts.cursor || '');
    }
    if (opts.trackPointer) k.invalidate();
  }
  function onUp(e) {
    local(e);
    k.pointer.down = false;
    if (k.active) {
      const hd = k.active; k.active = null;
      if (hd.up) hd.up(k.pointer.x, k.pointer.y, e);
      canvas.style.cursor = k.pointer.type === 'touch' ? '' : (hd.cursor || 'grab');
      if (k.pointer.type === 'touch') k.hover = null;
    } else if (k.tapStart && e.type === 'pointerup') {
      const ts = k.tapStart;
      if (Math.hypot(k.pointer.x - ts.x, k.pointer.y - ts.y) < 10 && performance.now() - ts.t < 600) {
        for (let i = 0; i < tapFns.length; i++) tapFns[i](k.pointer.x, k.pointer.y, e);
      }
    }
    k.tapStart = null;
    k.invalidate();
  }
  function onLeave() { k.pointer.inside = false; if (!k.active && k.hover) { k.hover = null; k.invalidate(); } }
  function onTouchStart(e) {
    if (e.touches.length !== 1) return;
    const r = canvas.getBoundingClientRect();
    const t = e.touches[0];
    k.pointer.type = 'touch';
    if (opts.captureTouch || pick(t.clientX - r.left, t.clientY - r.top)) e.preventDefault();
  }
  canvas.style.touchAction = opts.captureTouch ? 'none' : 'pan-y pinch-zoom';
  canvas.addEventListener('pointerdown', onDown);
  canvas.addEventListener('pointermove', onMove);
  canvas.addEventListener('pointerup', onUp);
  canvas.addEventListener('pointercancel', onUp);
  canvas.addEventListener('pointerleave', onLeave);
  canvas.addEventListener('touchstart', onTouchStart, { passive: false });

  Object.assign(k, {
    /** Set the draw function: fn(ctx, dt, w, h). dt is 0 for a redraw without time passing. */
    frame(fn) { draw = fn; dirty = true; sync(); return k; },
    animate(on) { on = !!on; if (on === animating) return; animating = on; if (on) last = performance.now(); sync(); },
    get animating() { return animating; },
    invalidate() { dirty = true; sync(); },
    onResize(fn) { resizeFns.push(fn); fn(k.w, k.h); },
    /** Register a draggable: { hit(x, y, slack) -> true | distance | false, down, move, up, cursor, enabled }. */
    drag(spec) { handles.push(spec); return spec; },
    onTap(fn) { tapFns.push(fn); },
    isHot(spec) { return k.active === spec || (k.hover === spec && k.pointer.type !== 'touch'); },
    /** Memoise an expensive object (gradient, sprite) until the next resize. */
    cache(key, make) { let v = caches.get(key); if (v === undefined) { v = make(); caches.set(key, v); } return v; },
    dispose() {
      disposed = true; animating = false; sync();
      ro.disconnect(); io.disconnect();
      document.removeEventListener('visibilitychange', onVis);
      canvas.removeEventListener('touchstart', onTouchStart);
      if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
      stage.classList.remove('ix-k2-stage', 'ix-k2-night');
      if (shell) shell.classList.remove('ix-k2', 'ix-k2-dark');
    },
  });
  stage.__k2 = k;
  resize();
  return k;
}

export function hitCircle(cx, cy, r) {
  return (x, y, s) => { const d = Math.hypot(x - cx(), y - cy()); return d <= r() + s ? d : false; };
}

/* ---------------------------------------------------------------- drawing */

export function background(k, ctx, w, h, top, bottom) {
  const th = k.theme;
  const g = k.cache('bg' + (top || '') + (bottom || ''), () => {
    const gr = ctx.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, top || th.bg0); gr.addColorStop(1, bottom || th.bg1);
    return gr;
  });
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, w, h);
}

export function grid(ctx, x0, y0, w, h, step, color, ox = 0, oy = 0) {
  ctx.beginPath();
  const sx = x0 + ((ox - x0) % step + step) % step;
  const sy = y0 + ((oy - y0) % step + step) % step;
  for (let x = sx; x <= x0 + w; x += step) { const px = Math.round(x) + 0.5; ctx.moveTo(px, y0); ctx.lineTo(px, y0 + h); }
  for (let y = sy; y <= y0 + h; y += step) { const py = Math.round(y) + 0.5; ctx.moveTo(x0, py); ctx.lineTo(x0 + w, py); }
  ctx.strokeStyle = color || T.grid; ctx.lineWidth = 1; ctx.stroke();
}

export function arrow(ctx, x0, y0, x1, y1, color, width = 2.5, head = 0) {
  const dx = x1 - x0, dy = y1 - y0;
  const len = Math.hypot(dx, dy);
  if (len < 0.5) return;
  const hs = head || Math.min(12, 4 + width * 2.6, len * 0.6);
  const ux = dx / len, uy = dy / len;
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = width;
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1 - ux * hs * 0.8, y1 - uy * hs * 0.8); ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x1 - ux * hs - uy * hs * 0.5, y1 - uy * hs + ux * hs * 0.5);
  ctx.lineTo(x1 - ux * hs + uy * hs * 0.5, y1 - uy * hs - ux * hs * 0.5);
  ctx.closePath(); ctx.fill();
}

export function text(ctx, s, x, y, color, size = 12, weight = 500, align = 'left', baseline = 'alphabetic') {
  ctx.font = font(size, weight); ctx.fillStyle = color; ctx.textAlign = align; ctx.textBaseline = baseline;
  ctx.fillText(s, x, y);
}

/** A rounded label pill. Returns its width. */
export function pill(ctx, s, x, y, opt) {
  const size = (opt && opt.size) || 11.5;
  const pad = (opt && opt.pad) || 7;
  ctx.font = font(size, (opt && opt.weight) || 600);
  const tw = ctx.measureText(s).width;
  const w = tw + pad * 2, h = size + pad + 2;
  const align = (opt && opt.align) || 'center';
  const left = align === 'center' ? x - w / 2 : align === 'right' ? x - w : x;
  const top = y - h / 2;
  ctx.beginPath(); ctx.roundRect(left, top, w, h, h / 2);
  ctx.fillStyle = (opt && opt.bg) || 'rgba(255,255,255,0.94)'; ctx.fill();
  if (!opt || opt.border !== false) { ctx.strokeStyle = (opt && opt.border) || 'rgba(23,32,51,0.12)'; ctx.lineWidth = 1; ctx.stroke(); }
  ctx.fillStyle = (opt && opt.color) || T.ink; ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
  ctx.fillText(s, left + pad, top + h / 2 + 0.5);
  return w;
}

/** A white card with a soft, cheap shadow (no blur filter). */
export function card(ctx, x, y, w, h, r = 12, fill, border) {
  ctx.fillStyle = 'rgba(23,40,80,0.06)';
  ctx.beginPath(); ctx.roundRect(x, y + 3, w, h, r); ctx.fill();
  ctx.fillStyle = 'rgba(23,40,80,0.05)';
  ctx.beginPath(); ctx.roundRect(x - 1, y + 1, w + 2, h + 1.5, r + 1); ctx.fill();
  ctx.beginPath(); ctx.roundRect(x, y, w, h, r);
  ctx.fillStyle = fill || '#fff'; ctx.fill();
  ctx.strokeStyle = border || 'rgba(23,32,51,0.10)'; ctx.lineWidth = 1; ctx.stroke();
}

/** A soft elliptical contact shadow. */
export function softShadow(ctx, x, y, rx, ry, alpha = 0.22) {
  if (rx <= 0 || ry <= 0) return;
  const spr = shadowSprite();
  ctx.globalAlpha = alpha;
  ctx.drawImage(spr, x - rx, y - ry, rx * 2, ry * 2);
  ctx.globalAlpha = 1;
}
let _shadow = null;
function shadowSprite() {
  if (_shadow) return _shadow;
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d');
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(15,25,50,1)'); gr.addColorStop(0.5, 'rgba(15,25,50,0.45)'); gr.addColorStop(1, 'rgba(15,25,50,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  _shadow = c; return c;
}

const spriteCache = new Map();
/** A lit sphere (ball, bob, planet) pre-rendered once per colour and size bucket. */
export function sphere(ctx, x, y, r, color, opt) {
  if (r <= 0.3) return;
  const bucket = r < 8 ? 8 : r < 16 ? 16 : r < 32 ? 32 : r < 64 ? 64 : 128;
  const key = color + bucket + (opt && opt.glow ? 'g' : '');
  let spr = spriteCache.get(key);
  if (!spr) {
    const S = bucket * 2 * 2 + 4;
    spr = document.createElement('canvas'); spr.width = spr.height = S;
    const g = spr.getContext('2d');
    const R = bucket * 2, c = S / 2;
    const gr = g.createRadialGradient(c - R * 0.38, c - R * 0.42, R * 0.05, c, c, R);
    gr.addColorStop(0, mix(color, '#ffffff', 0.62)); gr.addColorStop(0.35, color); gr.addColorStop(1, mix(color, '#000000', 0.42));
    g.fillStyle = gr; g.beginPath(); g.arc(c, c, R, 0, Math.PI * 2); g.fill();
    const hl = g.createRadialGradient(c - R * 0.35, c - R * 0.4, 0, c - R * 0.35, c - R * 0.4, R * 0.45);
    hl.addColorStop(0, 'rgba(255,255,255,0.75)'); hl.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = hl; g.beginPath(); g.arc(c, c, R, 0, Math.PI * 2); g.fill();
    spriteCache.set(key, spr);
  }
  const s = r * (spr.width / 2) / (bucket * 2);
  ctx.drawImage(spr, x - s, y - s, s * 2, s * 2);
}

/** A draggable knob: white disc, coloured ring, halo when hot. `hot` 0..1 (use a Spring). */
export function knob(ctx, x, y, r, color, hot = 0) {
  if (hot > 0.01) {
    ctx.beginPath(); ctx.arc(x, y, r + 6 + hot * 5, 0, Math.PI * 2);
    ctx.fillStyle = withAlpha(color, 0.16 * hot); ctx.fill();
  }
  ctx.beginPath(); ctx.arc(x, y + 1.5, r, 0, Math.PI * 2); ctx.fillStyle = 'rgba(15,25,50,0.18)'; ctx.fill();
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill();
  ctx.lineWidth = 2.5; ctx.strokeStyle = color; ctx.stroke();
  ctx.beginPath(); ctx.arc(x, y, r * 0.38, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
}

/** A dimension line with end ticks and a centred label pill. */
export function dimension(ctx, x0, y0, x1, y1, label, color = T.ink2) {
  const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy);
  if (len < 2) return;
  const nx = -dy / len * 5, ny = dx / len * 5;
  ctx.strokeStyle = color; ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(x0, y0); ctx.lineTo(x1, y1);
  ctx.moveTo(x0 - nx, y0 - ny); ctx.lineTo(x0 + nx, y0 + ny);
  ctx.moveTo(x1 - nx, y1 - ny); ctx.lineTo(x1 + nx, y1 + ny);
  ctx.stroke();
  if (label) pill(ctx, label, (x0 + x1) / 2, (y0 + y1) / 2, { color, size: 10.5 });
}

/** Dashed line helper that leaves the dash state clean. */
export function dashed(ctx, x0, y0, x1, y1, color, width = 1.2, dash = DASH) {
  ctx.setLineDash(dash); ctx.strokeStyle = color; ctx.lineWidth = width;
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
  ctx.setLineDash(NODASH);
}
export const DASH = [5, 5];
export const DOTS = [1.5, 4.5];
export const NODASH = [];

/* ---------------------------------------------------------------- colour */

const rgbCache = new Map();
export function rgb(hex) {
  let v = rgbCache.get(hex);
  if (v) return v;
  let h = hex.replace('#', '');
  if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
  const n = parseInt(h, 16);
  v = [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  rgbCache.set(hex, v);
  return v;
}
export function mix(a, b, t) {
  const A = rgb(a), B = rgb(b);
  const r = Math.round(A[0] + (B[0] - A[0]) * t), g = Math.round(A[1] + (B[1] - A[1]) * t), bl = Math.round(A[2] + (B[2] - A[2]) * t);
  return '#' + ((1 << 24) | (r << 16) | (g << 8) | bl).toString(16).slice(1);
}
const alphaCache = new Map();
export function withAlpha(hex, a) {
  const q = Math.round(a * 100);
  const key = hex + q;
  let s = alphaCache.get(key);
  if (!s) { const c = rgb(hex); s = `rgba(${c[0]},${c[1]},${c[2]},${q / 100})`; alphaCache.set(key, s); }
  return s;
}
