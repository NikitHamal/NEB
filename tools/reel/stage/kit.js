'use strict';
// Shared pieces for the reel: cue sheet, footage lookup, logo, phone, kinetic headline, callouts.
const ROOT = '../../../backend_python/web/static/web/';
const APPCAP = '../captures/app/';
const FOOT = window.FOOTAGE || { clips: {}, stills: [] };
const INK = '#0a1636', BLUE = '#004bd4', SKY = '#a8c5ff', PAPER = '#f4f6fb';
const CUES = [];
function CUE(t, type, o = {}) { CUES.push({ t: +t.toFixed(4), type, ...o }); }

function hasClip(name) { return !!FOOT.clips[name]; }
function hasStill(name) { return FOOT.stills.indexOf(name) >= 0; }
function stillSrc(name) { return `${APPCAP}stills/${name}.jpg`; }
function clipSrc(name, sec) {
  const c = FOOT.clips[name];
  if (!c) return null;
  const f = Math.max(0, Math.min(c.n - 1, Math.floor(sec * c.fps)));
  return `${APPCAP}${name}/${String(f + 1).padStart(5, '0')}.jpg`;
}
function setSrc(img, src) { if (src && img.getAttribute('src') !== src) img.setAttribute('src', src); }
// spec: {segs: [[at, clip, from, speed], ...]}: from scene-local time `at`, play `clip` starting at `from`.
function playInto(img, spec, tl, fallback) {
  const segs = spec ? spec.segs || [[0, spec.clip, spec.from || 0, spec.speed || 1]] : [];
  let seg = null;
  for (const s of segs) if (tl >= s[0] && hasClip(s[1])) seg = s;
  if (seg) return setSrc(img, clipSrc(seg[1], seg[2] + (tl - seg[0]) * (seg[3] || 1)));
  const st = (fallback || []).find(hasStill);
  if (st) setSrc(img, stillSrc(st));
}

const ICONS = {
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
  play: '<path d="M7 4.5v15l12-7.5z" fill="currentColor" stroke="none"/>',
  cube: '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/>',
};
const ic = (n, size = 24, sw = 2) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICONS[n]}</svg>`;
const ms = (n, size = 24) => `<span class="ms" style="font-size:${size}px">${n}</span>`;

const LOGO = [
  { d: 'M500 42 L501 135 L856 370 L858 1287 L943 1219 L943 331 Z', g: 'd' },
  { d: 'M441 191 L441 282 L691 447 L691 799 L774 886 L775 408 Z', g: 'i' },
  { d: 'M306 320 L307 377 L613 706 L613 485 Z', g: 'l' },
  { d: 'M51 228 L51 1132 L263 1346 L267 812 L775 1353 L775 887 L691 800 L685 902 Z', g: 'f' },
  { d: 'M691 800 L775 887 L775 1052 L691 958 Z', g: 's', ns: true },
];
let logoCount = 0;
function makeLogo(parent, height) {
  const p = 'lg' + (logoCount++);
  const svg = svgEl('svg', { viewBox: '226 96 578 830', width: (height * 578) / 830, height }, parent);
  svg.style.overflow = 'visible';
  svg.innerHTML = `<defs>
    <linearGradient id="${p}f" x1="40" y1="220" x2="800" y2="1350" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0058df"/><stop offset=".48" stop-color="#004bd4"/><stop offset="1" stop-color="#003cc3"/></linearGradient>
    <linearGradient id="${p}d" x1="505" y1="30" x2="960" y2="1290" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#07337f"/><stop offset=".55" stop-color="#052566"/><stop offset="1" stop-color="#021b54"/></linearGradient>
    <linearGradient id="${p}i" x1="435" y1="180" x2="780" y2="890" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#06327c"/><stop offset="1" stop-color="#04215e"/></linearGradient>
    <linearGradient id="${p}l" x1="305" y1="320" x2="615" y2="705" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#a8c5ff"/><stop offset=".52" stop-color="#90b4fb"/><stop offset="1" stop-color="#82a8f5"/></linearGradient>
    <linearGradient id="${p}s" x1="690" y1="780" x2="780" y2="1050" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0030a5" stop-opacity=".35"/><stop offset="1" stop-color="#001e77" stop-opacity="0"/></linearGradient>
  </defs>`;
  const g = svgEl('g', { transform: 'translate(210.601 86.137) scale(0.610119)', stroke: '#eef5ff', 'stroke-width': 8, 'stroke-linejoin': 'round' }, svg);
  const facets = LOGO.map((f) => {
    const a = { d: f.d, fill: `url(#${p}${f.g})` };
    if (f.ns) a.stroke = 'none';
    const e = svgEl('path', a, g);
    e.style.transformBox = 'fill-box';
    e.style.transformOrigin = 'center';
    return e;
  });
  return { svg, facets };
}

function makeRealPhone(parent, { left = 260, top = 640, w = 560 } = {}) {
  const sw = w - 32, sh = Math.round(sw * 2400 / 1080);
  const ph = el('div', 'phone', parent, { left: left + 'px', top: top + 'px', width: w + 'px', height: sh + 32 + 'px', borderRadius: '76px' });
  el('div', 'btn', ph, { top: '230px', height: '100px' });
  el('div', 'btn', ph, { top: '370px', height: '160px' });
  const scr = el('div', 'scr', ph, { borderRadius: '60px', background: '#fff' });
  const img = el('img', null, scr, { position: 'absolute', left: 0, top: 0, width: '100%', height: '100%', objectFit: 'cover' });
  el('div', 'glare', ph, { borderRadius: '76px' });
  return { ph, scr, img, w, h: sh + 32 };
}

function makeHead(parent, { kicker, lines, y = 250, onInk = false, size = 'h-l', fs }) {
  const wrap = el('div', 'abs center-x' + (onInk ? ' on-ink' : ''), parent, { top: y + 'px', color: onInk ? '#fff' : INK, zIndex: 10 });
  let k = null, kspans = [];
  if (kicker) {
    k = el('div', 'kicker', wrap, { color: onInk ? SKY : BLUE, marginBottom: '20px' });
    el('span', 'dot', k, onInk ? { background: SKY } : null);
    kspans = splitChars(el('span', null, k), kicker);
  }
  const rows = lines.map((ln) => {
    const d = el('div', size, wrap, fs ? { fontSize: fs + 'px' } : null);
    const words = [];
    ln.split(' ').forEach((w, i, arr) => {
      const m = el('span', 'mask', d);
      words.push(el('span', w.startsWith('*') ? 'hl' : '', m, null, w.replace(/\*/g, '')));
      if (i < arr.length - 1) d.appendChild(document.createTextNode(' '));
    });
    return words;
  });
  return {
    wrap, rows,
    update(t, tIn, tOut) {
      if (k) {
        const p = Ease.outExpo(prog(t, tIn, tIn + 0.5));
        const q = tOut != null ? Ease.inCubic(prog(t, tOut, tOut + 0.28)) : 0;
        tf(k, { y: (1 - p) * 26 - q * 40, o: p * (1 - q) });
        kspans.forEach((s, i) => tf(s, { py: (1 - Ease.outExpo(prog(t, tIn + i * 0.012, tIn + i * 0.012 + 0.45))) * 110 }));
      }
      let n = 0;
      rows.forEach((ws, li) => {
        const t0 = tIn + 0.06 + li * 0.11;
        ws.forEach((s, i) => {
          const pi = Ease.outExpo(prog(t, t0 + i * 0.055, t0 + i * 0.055 + 0.7));
          let py = (1 - pi) * 112;
          if (tOut != null) py -= Ease.inCubic(prog(t, tOut + n * 0.02, tOut + n * 0.02 + 0.28)) * 118;
          n++;
          tf(s, { py, r: (1 - pi) * 5 });
        });
      });
    },
  };
}

function bg(root, color) { root.style.background = color; }
function dotGrid(root, color, gap = 44, size = 2.2) {
  return el('div', 'abs', root, { inset: '-200px', backgroundImage: `radial-gradient(${color} ${size}px, transparent ${size + 0.6}px)`, backgroundSize: `${gap}px ${gap}px` });
}
function glowBlobs(root, dark) {
  const a = el('div', 'abs', root, { left: '-200px', top: '700px', width: '900px', height: '900px', borderRadius: '50%', background: dark ? 'rgba(0,75,212,0.45)' : 'rgba(0,75,212,0.16)', filter: 'blur(120px)' });
  const b = el('div', 'abs', root, { left: '520px', top: '1000px', width: '760px', height: '760px', borderRadius: '50%', background: dark ? 'rgba(124,92,255,0.28)' : 'rgba(168,197,255,0.55)', filter: 'blur(110px)' });
  return (t) => { tf(a, { x: Math.sin(t * 0.7) * 60, y: Math.cos(t * 0.5) * 50 }); tf(b, { x: Math.cos(t * 0.6) * 70, y: Math.sin(t * 0.8) * 40 }); };
}

function callout(parent, { text, icon, x, y, dark }) {
  const glyph = icon.startsWith('svg:') ? ic(icon.slice(4), 28, 2.2) : ms(icon, 30);
  return html(parent, `<div class="abs" style="left:${x}px;top:${y}px;z-index:30;display:flex;align-items:center;gap:14px;padding:16px 28px 16px 18px;border-radius:999px;
    background:${dark ? 'rgba(255,255,255,0.97)' : INK};color:${dark ? INK : '#fff'};font-size:31px;font-weight:700;letter-spacing:-0.01em;white-space:nowrap;
    box-shadow:0 24px 50px -22px rgba(10,22,54,.55)">
    <span style="width:50px;height:50px;border-radius:50%;background:${BLUE};color:#fff;display:flex;align-items:center;justify-content:center">${glyph}</span><span>${text}</span></div>`);
}
function popIn(e, t, t0, from = 0.6, out) {
  const p = sp(t - t0, 'bouncy');
  let o = clamp((t - t0) * 7);
  let s = from + (1 - from) * p;
  if (out != null) { const q = Ease.inCubic(prog(t, out, out + 0.25)); o *= 1 - q; s *= 1 - 0.2 * q; }
  tf(e, { s, o, y: (1 - p) * 30 });
}

function camKeys(keys) {
  return (tl) => {
    let k0 = keys[0], k1 = keys[keys.length - 1];
    for (let i = 0; i < keys.length - 1; i++) if (tl >= keys[i][0] && tl <= keys[i + 1][0]) { k0 = keys[i]; k1 = keys[i + 1]; break; }
    const p = k1 === k0 ? 1 : Ease.inOutCubic(prog(tl, k0[0], k1[0]));
    const o = {};
    for (const key of ['s', 'x', 'y', 'rx', 'ry']) o[key] = lerp(k0[1][key] ?? (key === 's' ? 1 : 0), k1[1][key] ?? (key === 's' ? 1 : 0), p);
    o.y += Math.sin(tl * 1.6) * 6;
    return o;
  };
}

const scenes = [];
function scene(a, b, build) {
  const root = el('div', 'scene', document.getElementById('world'));
  const s = { a, b, root };
  s.update = build(root, s) || (() => {});
  scenes.push(s);
  return s;
}
