'use strict';
// Deterministic motion engine: every value is a pure function of time t (seconds).
const W = 1080, H = 1920, FPS = 60, DURATION = 32.0;

const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
const lerp = (a, b, t) => a + (b - a) * t;
const prog = (t, a, b) => clamp((t - a) / (b - a));
const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);

function bezier(p1x, p1y, p2x, p2y) {
  const cx = 3 * p1x, bx = 3 * (p2x - p1x) - cx, ax = 1 - cx - bx;
  const cy = 3 * p1y, by = 3 * (p2y - p1y) - cy, ay = 1 - cy - by;
  const sx = (u) => ((ax * u + bx) * u + cx) * u;
  const sy = (u) => ((ay * u + by) * u + cy) * u;
  const dx = (u) => (3 * ax * u + 2 * bx) * u + cx;
  return (x) => {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let u = x;
    for (let i = 0; i < 8; i++) {
      const e = sx(u) - x, d = dx(u);
      if (Math.abs(e) < 1e-6 || Math.abs(d) < 1e-6) break;
      u -= e / d;
    }
    let lo = 0, hi = 1;
    for (let i = 0; i < 20 && Math.abs(sx(u) - x) > 1e-6; i++) {
      if (sx(u) < x) lo = u; else hi = u;
      u = (lo + hi) / 2;
    }
    return sy(u);
  };
}

const Ease = {
  linear: (x) => x,
  outCubic: (x) => 1 - Math.pow(1 - x, 3),
  inCubic: (x) => x * x * x,
  inOutCubic: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  outQuint: (x) => 1 - Math.pow(1 - x, 5),
  inQuint: (x) => x ** 5,
  inOutQuint: (x) => (x < 0.5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2),
  outExpo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  inExpo: (x) => (x <= 0 ? 0 : Math.pow(2, 10 * x - 10)),
  inOutExpo: (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x < 0.5 ? Math.pow(2, 20 * x - 10) / 2 : (2 - Math.pow(2, -20 * x + 10)) / 2),
  outBack: (x, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
  smooth: bezier(0.22, 1, 0.36, 1),
  snap: bezier(0.75, 0, 0.15, 1),
  swift: bezier(0.4, 0, 0, 1),
  anticipate: bezier(0.6, -0.28, 0.3, 1),
};

// Damped harmonic oscillator from 0 to 1, released at t = 0 (t in seconds).
function spring(t, k = 220, c = 20, m = 1) {
  if (t <= 0) return 0;
  const w0 = Math.sqrt(k / m), z = c / (2 * Math.sqrt(k * m));
  if (z < 1) {
    const wd = w0 * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + ((z * w0) / wd) * Math.sin(wd * t));
  }
  if (z === 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
  const s = Math.sqrt(z * z - 1), r1 = -w0 * (z - s), r2 = -w0 * (z + s);
  return 1 - ((r2 * Math.exp(r1 * t)) - (r1 * Math.exp(r2 * t))) / (r2 - r1);
}
const SP = {
  pop: [260, 17], soft: [120, 20], snappy: [420, 36], bouncy: [300, 11], heavy: [180, 24], gentle: [90, 17],
};
const sp = (t, name = 'pop') => spring(t, SP[name][0], SP[name][1]);

// Seeded random (mulberry32)
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let r = Math.imul(a ^ (a >>> 15), 1 | a);
    r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------- DOM helpers ----------
function el(tag, cls, parent, css, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (css) Object.assign(e.style, css);
  if (text != null) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
}
function svgEl(tag, attrs, parent) {
  const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function html(parent, markup) {
  const t = document.createElement('template');
  t.innerHTML = markup.trim();
  const node = t.content.firstElementChild;
  parent.appendChild(node);
  return node;
}
// transform + opacity in one write
function tf(e, o) {
  let s = '';
  if (o.x != null || o.y != null) s += `translate3d(${o.x || 0}px,${o.y || 0}px,0) `;
  if (o.px != null || o.py != null) s += `translate(${o.px || 0}%,${o.py || 0}%) `;
  if (o.z != null) s += `translateZ(${o.z}px) `;
  if (o.rx != null) s += `rotateX(${o.rx}deg) `;
  if (o.ry != null) s += `rotateY(${o.ry}deg) `;
  if (o.r != null) s += `rotate(${o.r}deg) `;
  if (o.s != null) s += `scale(${o.s}) `;
  if (o.sx != null || o.sy != null) s += `scale(${o.sx ?? 1},${o.sy ?? 1}) `;
  e.style.transform = s || 'none';
  if (o.o != null) e.style.opacity = clamp(o.o).toFixed(4);
  if (o.blur != null) e.style.filter = o.blur > 0.05 ? `blur(${o.blur.toFixed(2)}px)` : 'none';
}
function show(e, on) { e.style.visibility = on ? 'visible' : 'hidden'; }

// Split text into masked words or characters; returns the inner (animated) spans.
function splitWords(parent, text, cls) {
  const out = [];
  const parts = text.split(' ');
  parts.forEach((w, i) => {
    const m = el('span', 'mask', parent);
    const s = el('span', cls || '', m, null, w);
    out.push(s);
    if (i < parts.length - 1) parent.appendChild(document.createTextNode(' '));
  });
  return out;
}
function splitChars(parent, text, cls) {
  const out = [];
  for (const ch of text) {
    const m = el('span', 'mask', parent);
    const s = el('span', cls || '', m, null, ch === ' ' ? ' ' : ch);
    out.push(s);
  }
  return out;
}
// Masked rise: spans slide up from below their mask.
function rise(spans, t, t0, o = {}) {
  const st = o.stagger ?? 0.045, dur = o.dur ?? 0.6, ease = o.ease || Ease.outExpo, from = o.from ?? 110;
  spans.forEach((s, i) => {
    const p = ease(prog(t, t0 + i * st, t0 + i * st + dur));
    tf(s, { py: (1 - p) * from, r: o.rot ? (1 - p) * o.rot : null });
  });
}
function sink(spans, t, t0, o = {}) {
  const st = o.stagger ?? 0.03, dur = o.dur ?? 0.35, ease = o.ease || Ease.inCubic, to = o.to ?? -115;
  spans.forEach((s, i) => {
    const p = ease(prog(t, t0 + i * st, t0 + i * st + dur));
    if (p > 0) tf(s, { py: p * to });
  });
}

// ---------- assets ----------
const IMG = {};
function loadImage(key, src) {
  return new Promise((res) => {
    const im = new Image();
    im.onload = () => { IMG[key] = im; (im.decode ? im.decode() : Promise.resolve()).then(() => res(im), () => res(im)); };
    im.onerror = () => { console.warn('missing', src); res(null); };
    im.src = src;
  });
}

const NEBY_META = {
  idle: [16, 115], still: [1, 1000], blink: [6, 110], think: [8, 160], talk: [8, 95], read: [14, 140],
  wave: [10, 110], hop: [12, 72], wink: [10, 110], love: [12, 110], laugh: [10, 80], cool: [10, 120],
  surprised: [10, 80], success: [12, 80], celebrate: [14, 85], tika: [24, 110], kite: [16, 130],
  diyo: [12, 110], deusi: [12, 95], splash: [16, 90], fireworks: [16, 100], namaste: [12, 120],
};
// Draw one Neby frame. tl is local time in seconds; loop=false holds the last frame.
function drawNeby(cv, look, state, tl, loop = true) {
  const g = cv.getContext('2d');
  g.imageSmoothingEnabled = false;
  g.clearRect(0, 0, cv.width, cv.height);
  const im = IMG[`neby/${look}/${state}`];
  if (!im) return;
  const [n, ms] = NEBY_META[state] || [1, 1000];
  let f = Math.floor(Math.max(0, tl) * 1000 / ms);
  f = loop ? f % n : Math.min(n - 1, f);
  g.drawImage(im, f * 48, 0, 48, 48, 0, 0, cv.width, cv.height);
}
function pixelCanvas(parent, size, css) {
  const cv = el('canvas', 'pix', parent, css);
  cv.width = size; cv.height = size;
  cv.style.width = size + 'px'; cv.style.height = size + 'px';
  return cv;
}
function drawStrip(cv, key, fw, fh, n, ms, tl, loop = true) {
  const g = cv.getContext('2d');
  g.imageSmoothingEnabled = false;
  g.clearRect(0, 0, cv.width, cv.height);
  const im = IMG[key];
  if (!im) return;
  let f = Math.floor(Math.max(0, tl) * 1000 / ms);
  f = loop ? f % n : Math.min(n - 1, f);
  g.drawImage(im, f * fw, 0, fw, fh, 0, 0, cv.width, cv.height);
}

// Camera shake: sum of decaying oscillations from impact times.
function shake(t, hits) {
  let x = 0, y = 0, r = 0;
  for (const [t0, a] of hits) {
    const d = t - t0;
    if (d < 0 || d > 0.6) continue;
    const env = a * Math.exp(-d * 9);
    x += env * Math.sin(d * 71) * 1.0;
    y += env * Math.sin(d * 53 + 1.3) * 0.8;
    r += env * Math.sin(d * 47 + 0.4) * 0.02;
  }
  return { x, y, r };
}

const fmtInt = (n) => Math.round(n).toLocaleString('en-US');
