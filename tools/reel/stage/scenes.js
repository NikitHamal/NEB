'use strict';
// NEBians v1.7 launch reel: 1080x1920, 32 s, 120 BPM (a beat is 0.5 s, a bar is 2 s).
const ROOT = '../../../backend_python/web/static/web/';
const CAP = '../captures/';
const CUES = [];
function CUE(t, type, o = {}) { CUES.push({ t: +t.toFixed(4), type, ...o }); }
window.CUES = CUES;

const INK = '#0a1636', BLUE = '#004bd4', SKY = '#a8c5ff', PAPER = '#f4f6fb';

const ICONS = {
  home: '<path d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1z"/>',
  back: '<path d="M15 5l-7 7 7 7"/>',
  send: '<path d="M12 19V5M6 11l6-6 6 6"/>',
  more: '<circle cx="12" cy="5" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="12" cy="19" r="1.4"/>',
  bell: '<path d="M6 16v-5a6 6 0 1 1 12 0v5l2 2H4zM10 20.5a2 2 0 0 0 4 0"/>',
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
  draw: '<path d="M4 20l4-1 11-11-3-3L5 16zM14 6l3 3"/>',
  play: '<path d="M7 4.5v15l12-7.5z" fill="currentColor" stroke="none"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
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
function makeLogo(parent, height, css) {
  const p = 'lg' + (logoCount++);
  const svg = svgEl('svg', { viewBox: '226 96 578 830', width: (height * 578) / 830, height }, parent);
  svg.style.overflow = 'visible';
  if (css) Object.assign(svg.style, css);
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

function makePhone(parent, css) {
  const ph = el('div', 'phone', parent, css);
  el('div', 'btn', ph, { top: '250px', height: '110px' });
  el('div', 'btn', ph, { top: '400px', height: '180px' });
  const scr = el('div', 'scr', ph);
  el('div', 'island', ph);
  el('div', 'glare', ph);
  return { ph, scr };
}
const APP_SCALE = 568 / 412;
function makeApp(scr, bg) {
  return el('div', 'app', scr, { transform: `scale(${APP_SCALE})`, background: bg || '#fff' });
}
function statusBar(app, dark) {
  return html(app, `<div class="status" style="color:${dark ? '#e7e9ed' : '#1d1f25'}"><span>11:00</span>
    <span class="icons"><svg width="18" height="12" viewBox="0 0 18 12" fill="currentColor"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>
    <span class="bar"></span></span></div>`);
}
function navBar(app, active) {
  const items = [['home', 'Home'], ['library', 'Library'], ['canvas', 'Canvas']];
  const n = el('div', 'navbar', app);
  for (const [k, label] of items) {
    const glyph = k === 'home' ? ic('home', 22) : k === 'library' ? ms('menu_book', 23) : ic('draw', 22);
    html(n, `<div class="it ${k === active ? 'on' : ''}"><div class="ic">${glyph}</div><div>${label}</div></div>`);
  }
  return n;
}

// Headline block: kicker + lines; words wrapped in * are highlighted.
function makeHead(parent, { kicker, lines, y = 250, onInk = false, size = 'h-l', fs }) {
  const wrap = el('div', 'abs center-x' + (onInk ? ' on-ink' : ''), parent, { top: y + 'px', color: onInk ? '#fff' : INK, zIndex: 10 });
  let k = null, kspans = [];
  if (kicker) {
    k = el('div', 'kicker', wrap, { color: onInk ? SKY : BLUE, marginBottom: '22px' });
    el('span', 'dot', k, onInk ? { background: SKY } : null);
    const kt = el('span', null, k);
    kspans = splitChars(kt, kicker);
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
    update(t, tIn, tOut, lineTimes) {
      if (k) {
        const p = Ease.outExpo(prog(t, tIn, tIn + 0.5));
        const q = tOut != null ? Ease.inCubic(prog(t, tOut, tOut + 0.3)) : 0;
        tf(k, { y: (1 - p) * 26 - q * 40, o: p * (1 - q) });
        kspans.forEach((s, i) => {
          const pi = Ease.outExpo(prog(t, tIn + i * 0.012, tIn + i * 0.012 + 0.45));
          tf(s, { py: (1 - pi) * 110 });
        });
      }
      rows.forEach((ws, li) => {
        const t0 = lineTimes ? lineTimes[li] : tIn + 0.06 + li * 0.11;
        ws.forEach((s, i) => {
          const pi = Ease.outExpo(prog(t, t0 + i * 0.055, t0 + i * 0.055 + 0.7));
          let py = (1 - pi) * 112;
          if (tOut != null) {
            const q = Ease.inCubic(prog(t, tOut + (li * ws.length + i) * 0.02, tOut + (li * ws.length + i) * 0.02 + 0.3));
            py -= q * 118;
          }
          tf(s, { py, r: (1 - pi) * 5 });
        });
      });
    },
  };
}

function bg(root, color) { root.style.background = color; }
function dotGrid(root, color, gap = 44, size = 2.2, op = 1) {
  return el('div', 'abs', root, {
    inset: '-200px', opacity: op,
    backgroundImage: `radial-gradient(${color} ${size}px, transparent ${size + 0.6}px)`,
    backgroundSize: `${gap}px ${gap}px`,
  });
}

const scenes = [];
function scene(a, b, build) {
  const root = el('div', 'scene', document.getElementById('world'));
  const s = { a, b, root };
  s.update = build(root, s) || (() => {});
  scenes.push(s);
  return s;
}

const SHAKES = [[2.0, 16], [8.0, 22], [26.5, 12]];
const FLASHES = [[2.0, 0.16], [8.0, 0.3], [26.5, 0.18]];
const FAST = [[1.62, 2.1], [4.8, 5.18], [7.5, 7.95], [7.96, 8.12], [8.7, 9.1], [11.83, 12.2], [14.83, 15.2], [17.83, 18.18],
  [19.83, 20.2], [21.83, 22.2], [23.83, 24.2], [26.28, 26.66]];

// ------------------------------------------------------------------ S1 hook (0 to 2.0)
scene(0, 2.02, (root) => {
  bg(root, INK);
  const glow = el('div', 'abs', root, { inset: 0, background: 'radial-gradient(70% 45% at 50% 46%, rgba(0,75,212,0.38), rgba(10,22,54,0) 70%)' });
  const grid = dotGrid(root, 'rgba(168,197,255,0.16)', 48, 2);
  const l1 = el('div', 'abs center-x h-xl', root, { top: '470px', color: '#fff' });
  const c1 = splitChars(l1, 'Stuck at');
  // rolling clock 10:59 -> 11:00
  const clock = el('div', 'abs center-x', root, { top: '610px', display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: '0px', color: SKY });
  const digits = [['1', '1'], ['0', '1'], [':', ':'], ['5', '0'], ['9', '0']];
  const slots = digits.map(([a, b], i) => {
    const slot = el('div', null, clock, { position: 'relative', height: '290px', overflow: 'hidden', fontSize: '270px', fontWeight: 800, letterSpacing: '-0.04em', lineHeight: '290px', width: a === ':' ? '92px' : '172px', textAlign: 'center' });
    const o = el('div', null, slot, { position: 'absolute', left: 0, right: 0, top: 0 }, a);
    const n = el('div', null, slot, { position: 'absolute', left: 0, right: 0, top: 0 }, b);
    return { o, n, roll: a !== b, i };
  });
  const pm = el('div', null, clock, { fontSize: '110px', fontWeight: 800, color: '#fff', marginLeft: '26px', letterSpacing: '-0.03em' }, 'PM?');
  const l3 = el('div', 'abs center-x h-xl on-ink', root, { top: '930px', color: '#fff' });
  const w3 = splitWords(l3, 'Ask Neby.');
  w3[1].classList.add('hl');
  const neby = pixelCanvas(root, 288, { position: 'absolute', left: '396px', top: '1180px' });
  const shadow = el('div', 'abs', root, { left: '430px', top: '1452px', width: '220px', height: '26px', borderRadius: '50%', background: 'rgba(0,0,0,0.35)', filter: 'blur(6px)' });
  CUE(0.0, 'impact', { gain: 0.8 });
  CUE(0.3, 'tick'); CUE(0.55, 'tick');
  CUE(0.8, 'flip'); CUE(0.86, 'flip', { gain: 0.6 });
  CUE(1.12, 'whoosh', { gain: 0.5, dur: 0.3 });
  CUE(1.25, 'coin');
  CUE(1.55, 'riser', { dur: 0.45 });
  return (t) => {
    tf(grid, { y: -t * 30 });
    tf(glow, { s: 1 + t * 0.05, o: 0.7 + 0.3 * Ease.outCubic(prog(t, 0, 0.6)) });
    c1.forEach((s, i) => {
      const p = Ease.outExpo(prog(t, 0.0 + i * 0.022, 0.42 + i * 0.022));
      tf(s, { py: (1 - p) * 110, r: (1 - p) * 8 });
    });
    const cp = sp(t - 0.22, 'pop');
    tf(clock, { s: 0.55 + 0.45 * cp, o: clamp(cp * 3), y: (1 - cp) * 60 });
    slots.forEach((s) => {
      if (!s.roll) { tf(s.o, { py: 0 }); s.n.style.visibility = 'hidden'; return; }
      s.n.style.visibility = 'visible';
      const d = 0.78 + (4 - s.i) * 0.04;
      const p = Ease.snap(prog(t, d, d + 0.26));
      tf(s.o, { py: -p * 100, blur: Math.sin(p * Math.PI) * 6 });
      tf(s.n, { py: (1 - p) * 100, blur: Math.sin(p * Math.PI) * 6 });
    });
    tf(pm, { o: Ease.outCubic(prog(t, 0.4, 0.6)), x: (1 - Ease.outExpo(prog(t, 0.4, 0.9))) * 40 });
    rise(w3, t, 1.1, { stagger: 0.07, dur: 0.55 });
    const hp = sp(t - 1.22, 'bouncy');
    tf(neby, { y: (1 - hp) * 320, sy: 0.8 + 0.2 * hp, sx: 1.15 - 0.15 * hp, o: clamp((t - 1.2) * 8) });
    tf(shadow, { s: 0.4 + 0.6 * hp, o: clamp((t - 1.2) * 4) * 0.8 });
    drawNeby(neby, 'classic', t < 1.6 ? 'wave' : 'hop', t - 1.22);
    const push = Ease.inCubic(prog(t, 1.62, 2.0));
    root.style.transform = `scale(${1 + push * 0.12})`;
    root.style.transformOrigin = '540px 1324px';
  };
});

// ------------------------------------------------------------------ S2 brand (1.62 to 5.15)
scene(1.62, 5.15, (root) => {
  bg(root, PAPER);
  const grid = dotGrid(root, 'rgba(0,75,212,0.10)', 46, 2.2);
  const ring = el('div', 'abs', root, { left: '540px', top: '700px', width: '10px', height: '10px', borderRadius: '50%', border: `6px solid ${BLUE}` });
  const holder = el('div', 'abs', root, { left: '0', right: '0', top: '420px', display: 'flex', justifyContent: 'center' });
  const logo = makeLogo(holder, 520);
  const from = [[-520, -380, -48, 0.6], [560, -520, 40, 0.5], [620, 260, 75, 0.4], [-640, 420, -30, 0.7], [300, 640, 20, 0.5]];
  const order = [3, 0, 1, 2, 4];
  const word = el('div', 'abs center-x h-xxl', root, { top: '980px', color: INK });
  const wc = splitChars(word, 'NEBians');
  const tag1 = el('div', 'abs center-x h-m', root, { top: '1210px', color: INK });
  const t1 = splitWords(tag1, 'Study materials.');
  const tag2 = el('div', 'abs center-x h-m', root, { top: '1290px', color: INK });
  const t2 = splitWords(tag2, 'Study mates.');
  t2[1].classList.add('hl');
  const pill = el('div', 'abs', root, { left: 0, right: 0, top: '1450px', display: 'flex', justifyContent: 'center' });
  const pi = html(pill, `<div class="pill" style="background:${INK};color:#fff;font-size:36px;padding:20px 40px">
    <span style="color:${SKY}">Free</span><span style="opacity:.45">·</span><span>Made in Nepal</span></div>`);
  CUE(2.0, 'boom', { gain: 1.0 });
  order.forEach((k, j) => CUE(2.0 + j * 0.045, 'click', { gain: 0.35, pitch: 1 + j * 0.12 }));
  CUE(2.42, 'whoosh', { gain: 0.45, dur: 0.4 });
  CUE(2.95, 'pop', { gain: 0.5 }); CUE(3.25, 'pop', { gain: 0.55, pitch: 1.2 });
  CUE(3.8, 'chime');
  CUE(4.8, 'whoosh', { gain: 0.8, dur: 0.4 });
  return (t) => {
    const r = Ease.inCubic(prog(t, 1.62, 2.0));
    root.style.clipPath = t < 2.0 ? `circle(${(r * 2300).toFixed(1)}px at 540px 1324px)` : 'none';
    tf(grid, { y: -t * 24 });
    order.forEach((k, j) => {
      const f = logo.facets[k];
      const s = sp(t - 2.0 - j * 0.045, 'pop');
      const [x, y, rot, sc] = from[k];
      tf(f, { x: x * (1 - s), y: y * (1 - s), r: rot * (1 - s), s: sc + (1 - sc) * s, o: clamp((t - 2.0 - j * 0.045) * 12) });
    });
    const breathe = 1 + 0.012 * Math.sin((t - 2) * 2.2);
    tf(holder, { s: breathe, y: -Ease.inOutCubic(prog(t, 4.6, 5.15)) * 80 });
    const rp = Ease.outCubic(prog(t, 2.02, 2.7));
    tf(ring, { s: 1 + rp * 120, o: (1 - rp) * 0.5 });
    ring.style.borderWidth = (6 / (1 + rp * 120) * 3).toFixed(3) + 'px';
    wc.forEach((s, i) => {
      const p = Ease.outExpo(prog(t, 2.45 + i * 0.035, 3.05 + i * 0.035));
      tf(s, { py: (1 - p) * 110, r: (1 - p) * 6 });
    });
    rise(t1, t, 2.92, { stagger: 0.07 });
    rise(t2, t, 3.22, { stagger: 0.07 });
    const pp = sp(t - 3.78, 'bouncy');
    tf(pi, { s: 0.5 + 0.5 * pp, o: clamp((t - 3.78) * 8) });
    const out = Ease.inOutQuint(prog(t, 4.82, 5.15));
    root.style.transform = `translateY(${-out * 1920}px)`;
  };
});

// ------------------------------------------------------------------ S3 library (4.82 to 8.12)
const LIB = [
  ['physics-3-day', 'Notes', 'Waves and Optics', 'Class 12 · 48 pages'],
  ['chemistry-5-day', 'Past paper', 'Chemistry 2081', 'Class 12 · Solved'],
  ['math-2-day', 'Book', 'Basic Mathematics', 'Class 11 · 312 pages'],
  ['biology-4-day', 'Notes', 'Cell Biology', 'Class 11 · 36 pages'],
  ['computing-1-day', 'Notes', 'C Programming', 'Class 12 · 54 pages'],
  ['language-6-day', 'Past paper', 'English SEE 2080', 'Class 10 · Solved'],
  ['social-2-day', 'Notes', 'Social Studies', 'Class 10 · 40 pages'],
  ['exam-3-day', 'Past paper', 'Model Questions', 'Class 12 · 2082'],
  ['science-5-day', 'Book', 'Science and Tech', 'Class 8 · 220 pages'],
  ['commerce-1-day', 'Notes', 'Accountancy', 'Class 11 · 61 pages'],
];
scene(4.82, 7.95, (root) => {
  bg(root, PAPER);
  root.style.perspective = '2600px';
  const head = makeHead(root, { kicker: 'The library', lines: ['Notes, papers,', 'books. *Free.*'], y: 230, fs: 104 });
  const { ph, scr } = makePhone(root, { left: '240px', top: '640px' });
  const app = makeApp(scr);
  statusBar(app);
  html(app, `<div class="topbar"><div class="title">Library</div><div style="margin-left:auto;display:flex;gap:4px"><div class="iconbtn">${ms('search', 24)}</div><div class="iconbtn">${ic('bell', 22)}</div></div></div>`);
  html(app, `<div class="rail" style="position:absolute;left:16px;top:110px"><div class="tab on">Library</div><div class="tab">Syllabus</div><div class="tab">Interactive</div></div>`);
  html(app, `<div class="rail" style="position:absolute;left:16px;top:158px"><div class="tab" style="background:#dbe1ff;color:#003ea8">All</div><div class="tab">Notes</div><div class="tab">Past papers</div><div class="tab">Books</div></div>`);
  const list = el('div', 'abs', app, { left: 0, right: 0, top: '206px', bottom: '78px', overflow: 'hidden' });
  const inner = el('div', 'abs', list, { left: 0, top: 0, width: '412px' });
  const cards = LIB.map(([ban, kind, title, sub], i) => {
    const c = html(inner, `<div class="rcard" style="left:${16 + (i % 2) * 196}px;top:${Math.floor(i / 2) * 206}px">
      <div class="ban" style="background-image:url(${ROOT}img/pixel-art/banner/${ban}.png)"></div>
      <div class="meta"><div class="kind">${kind}</div><div class="t">${title}</div><div class="s">${sub}</div></div></div>`);
    return c;
  });
  navBar(app, 'library');
  const b1 = html(root, `<div class="abs" style="left:640px;top:1080px;padding:26px 34px;border-radius:34px;background:rgba(255,255,255,0.92);box-shadow:0 30px 60px -30px rgba(10,22,54,.45);border:1px solid #e3e8f2;z-index:20">
    <div style="font-size:84px;font-weight:800;letter-spacing:-0.04em;color:${INK};line-height:1"><span class="num">0</span><span style="color:${BLUE}">+</span></div>
    <div style="font-size:28px;font-weight:600;color:#5c6475;margin-top:4px">pages of notes</div></div>`);
  const num = b1.querySelector('.num');
  const b2 = html(root, `<div class="abs" style="left:56px;top:1370px;padding:22px 30px;border-radius:30px;background:${INK};color:#fff;box-shadow:0 30px 60px -30px rgba(10,22,54,.6);z-index:20;display:flex;align-items:center;gap:16px">
    <span style="width:52px;height:52px;border-radius:50%;background:${BLUE};display:flex;align-items:center;justify-content:center">${ms('check', 34)}</span>
    <div style="font-size:30px;font-weight:700;line-height:1.2">Every textbook<br>exercise, solved</div></div>`);
  CUE(5.25, 'pop', { gain: 0.35 }); CUE(5.4, 'pop', { gain: 0.35, pitch: 1.1 }); CUE(5.55, 'pop', { gain: 0.35, pitch: 1.2 });
  CUE(6.05, 'counter', { dur: 0.85 });
  CUE(6.9, 'ding', { gain: 0.5 });
  CUE(6.6, 'swish', { gain: 0.5 });
  CUE(7.5, 'zoom', { dur: 0.42 });
  return (t) => {
    head.update(t, 5.05, null);
    const ip = sp(t - 4.95, 'heavy');
    const out = Ease.inExpo(prog(t, 7.5, 7.92));
    tf(ph, { y: (1 - ip) * 900, rx: (1 - ip) * 30 + 6 * (1 - out), ry: -10 + 4 * Ease.inOutCubic(prog(t, 5.5, 7.7)), r: (1 - ip) * -4 });
    cards.forEach((c, i) => {
      const p = sp(t - 5.2 - i * 0.06, 'pop');
      tf(c, { y: (1 - p) * 160, s: 0.85 + 0.15 * p, o: clamp((t - 5.2 - i * 0.06) * 6) });
    });
    const sc = Ease.inOutCubic(prog(t, 6.2, 8.0));
    tf(inner, { y: -sc * 470 });
    const c1 = sp(t - 6.0, 'bouncy');
    tf(b1, { s: 0.6 + 0.4 * c1, o: clamp((t - 6.0) * 8), y: (1 - c1) * 40 });
    num.textContent = fmtInt(6000 * Ease.outExpo(prog(t, 6.05, 6.9)));
    const c2 = sp(t - 6.55, 'bouncy');
    tf(b2, { s: 0.6 + 0.4 * c2, o: clamp((t - 6.55) * 8), x: (1 - c2) * -80 });
    root.style.transformOrigin = '540px 1250px';
    root.style.filter = out > 0.01 ? `blur(${(out * 14).toFixed(2)}px)` : 'none';
    root.style.opacity = (1 - Ease.inCubic(prog(t, 7.75, 7.94))).toFixed(3);
    root.style.transform = `translateY(${(1 - Ease.inOutQuint(prog(t, 4.82, 5.15))) * 1920}px) scale(${1 + out * 2.2})`;
  };
});

// ------------------------------------------------------------------ S4 what's new (7.9 to 9.1)
scene(7.66, 9.1, (root) => {
  bg(root, INK);
  const glow = el('div', 'abs', root, { inset: 0, background: 'radial-gradient(60% 40% at 50% 50%, rgba(0,75,212,0.45), rgba(10,22,54,0) 70%)' });
  const l1 = el('div', 'abs center-x h-l', root, { top: '600px', color: '#fff' });
  const w1 = splitWords(l1, "What's new in");
  const v = el('div', 'abs center-x', root, { top: '700px', fontSize: '400px', fontWeight: 900, letterSpacing: '-0.06em', lineHeight: 1, color: SKY });
  v.innerHTML = 'v1.7';
  v.style.backgroundImage = 'linear-gradient(180deg,#ffffff 10%,#a8c5ff 90%)';
  v.style.webkitBackgroundClip = 'text';
  v.style.color = 'transparent';
  const sub = el('div', 'abs center-x', root, { top: '1150px', fontSize: '40px', fontWeight: 600, color: 'rgba(215,228,255,0.8)' }, 'The biggest NEBians update yet');
  const bands = [];
  for (let i = 0; i < 8; i++) bands.push(el('div', 'abs', root, { left: 0, top: i * 240 + 'px', width: '1080px', height: '241px', background: PAPER, transformOrigin: i % 2 ? '100% 50%' : '0% 50%' }));
  CUE(7.74, 'swish', { gain: 0.4 });
  CUE(8.0, 'boom', { gain: 1.0 }); CUE(8.0, 'glitch', { gain: 0.45 });
  CUE(8.7, 'whoosh', { gain: 0.8, dur: 0.38 });
  return (t) => {
    root.style.opacity = Ease.outCubic(prog(t, 7.66, 7.8)).toFixed(3);
    rise(w1, t, 7.72, { stagger: 0.06, dur: 0.45 });
    const vp = sp(t - 7.97, 'snappy');
    const z = Ease.inExpo(prog(t, 8.66, 8.98));
    tf(v, { s: (1.5 - 0.5 * vp) * (1 + z * 7), o: clamp((t - 7.97) * 14), y: z * 300 });
    tf(sub, { o: Ease.outCubic(prog(t, 8.2, 8.38)) * (1 - z), y: (1 - Ease.outExpo(prog(t, 8.2, 8.7))) * 30 });
    tf(w1[0].parentNode.parentNode, { o: 1 - z });
    tf(glow, { s: 1 + 0.3 * vp });
    bands.forEach((b, i) => {
      const p = Ease.inOutQuint(prog(t, 8.72 + i * 0.018, 8.94 + i * 0.018));
      tf(b, { sx: p });
    });
  };
});

// ------------------------------------------------------------------ S5 syllabus (9.0 to 12.15)
const SUBJ = [
  ['physics-8-day', 'Physics', '14 chapters', 0.64],
  ['chemistry-2-day', 'Chemistry', '12 chapters', 0.4],
  ['math-5-day', 'Mathematics', '16 chapters', 0.28],
  ['language-1-day', 'English', '35 units', 0.52],
  ['computing-6-day', 'Computer Science', '10 chapters', 0.2],
];
scene(9.08, 12.18, (root) => {
  bg(root, PAPER);
  root.style.perspective = '2600px';
  const head = makeHead(root, { kicker: 'New · Syllabus', lines: ['Class 8 to 12.', 'Every *chapter.*'], y: 230, fs: 108 });
  const { ph, scr } = makePhone(root, { left: '240px', top: '640px' });
  const app = makeApp(scr);
  statusBar(app);
  html(app, `<div class="topbar"><div class="title">Syllabus</div><div style="margin-left:auto" class="iconbtn">${ms('search', 24)}</div></div>`);
  const seg = el('div', 'seg', app, { top: '112px' });
  const knob = el('div', 'knob', seg);
  const opts = ['8', '10', '11', '12'].map((c) => el('div', 'opt', seg, null, 'Class ' + c));
  const cont = html(app, `<div class="abs" style="left:16px;right:16px;top:182px;height:92px;border-radius:22px;background:#1d1f25;color:#fff;padding:14px 18px">
    <div style="font-size:11px;font-weight:700;letter-spacing:.12em;color:#b4c5ff">CONTINUE READING</div>
    <div style="font-size:16px;font-weight:700;margin-top:4px">Unit 14 · Reflection at curved mirror</div>
    <div style="height:6px;border-radius:3px;background:rgba(255,255,255,.18);margin-top:10px"><div class="fill" style="height:100%;width:0;border-radius:3px;background:#b4c5ff"></div></div></div>`);
  const fill = cont.querySelector('.fill');
  const rows = SUBJ.map(([ban, nm, sub, v], i) => {
    const r = html(app, `<div class="subj" style="top:${290 + i * 106}px">
      <div class="thumb" style="background-image:url(${ROOT}img/pixel-art/banner/${ban}.png)"></div>
      <div><div class="nm">${nm}</div><div class="sub">${sub}</div></div>
      <svg class="ring" viewBox="0 0 54 54"><circle cx="27" cy="27" r="22" fill="none" stroke="#e7e9ee" stroke-width="6"/>
      <circle class="arc" cx="27" cy="27" r="22" fill="none" stroke="#004ac6" stroke-width="6" stroke-linecap="round" transform="rotate(-90 27 27)" stroke-dasharray="138.2" stroke-dashoffset="138.2"/>
      <text x="27" y="31.5" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d1f25" font-family="Poppins">0%</text></svg></div>`);
    return { r, arc: r.querySelector('.arc'), txt: r.querySelector('text'), v };
  });
  navBar(app, 'library');
  const ripple = el('div', 'abs', app, { left: '120px', top: '336px', width: '30px', height: '30px', borderRadius: '50%', background: 'rgba(0,74,198,0.18)' });
  // chapter reader (live capture of the website's chapter page)
  const rd = el('div', 'app', scr, { transform: `scale(${APP_SCALE})`, background: '#fff' });
  statusBar(rd);
  html(rd, `<div class="topbar" style="border-bottom:1px solid #eceef2"><div class="iconbtn">${ic('back', 22)}</div><div><div style="font-size:12px;font-weight:600;color:#5c6475">Physics · Class 11</div><div style="font-size:17px;font-weight:700;letter-spacing:-0.01em">Reflection at curved mirror</div></div></div>`);
  const rv = el('div', 'abs', rd, { left: 0, right: 0, top: '104px', bottom: 0, overflow: 'hidden' });
  const rimg = el('img', null, rv, { position: 'absolute', left: 0, top: 0, width: '412px' });
  rimg.src = CAP + 'reader-crop.jpg';
  const KN = [0, 1, 2, 3];
  CUE(9.02, 'whoosh', { gain: 0.6, dur: 0.35 });
  CUE(9.62, 'tick', { gain: 0.6 }); CUE(10.0, 'tick', { gain: 0.6, pitch: 1.1 }); CUE(10.38, 'tick', { gain: 0.6, pitch: 1.2 });
  CUE(10.45, 'shimmer', { dur: 0.5 });
  CUE(10.88, 'tap'); CUE(11.0, 'swish', { gain: 0.6 });
  return (t) => {
    head.update(t, 9.12, 11.88);
    const ip = sp(t - 9.05, 'heavy');
    tf(ph, { x: (1 - ip) * 700, ry: -10 - (1 - ip) * 40, rx: 6 });
    // knob: 8 -> 10 -> 11 -> 12 -> 11
    const steps = [[9.6, 1], [9.98, 2], [10.36, 3]];
    let target = 0, from = 0, t0 = -1;
    for (const [ts, k] of steps) { if (t >= ts) { from = target; target = k; t0 = ts; } }
    const kp = t0 < 0 ? 1 : sp(t - t0, 'snappy');
    const cur = from + (target - from) * kp;
    const w = (380 - 10) / 4;
    knob.style.left = (5 + cur * w).toFixed(2) + 'px';
    knob.style.width = (w + Math.sin(Math.min(1, kp) * Math.PI) * 18).toFixed(2) + 'px';
    opts.forEach((o, i) => o.classList.toggle('on', Math.round(cur) === i));
    const fp = Ease.outExpo(prog(t, 9.7, 10.6));
    fill.style.width = (fp * 62).toFixed(1) + '%';
    rows.forEach((r, i) => {
      const p = sp(t - 9.35 - i * 0.06, 'pop');
      tf(r.r, { y: (1 - p) * 140, o: clamp((t - 9.35 - i * 0.06) * 6) });
      const a = Ease.outExpo(prog(t, 10.4 + i * 0.07, 11.2 + i * 0.07)) * r.v;
      r.arc.setAttribute('stroke-dashoffset', (138.2 * (1 - a)).toFixed(2));
      r.txt.textContent = Math.round(a * 100) + '%';
    });
    tf(cont, { o: clamp((t - 9.3) * 6), y: (1 - sp(t - 9.3, 'pop')) * 100 });
    const rp = Ease.outCubic(prog(t, 10.86, 11.15));
    tf(ripple, { s: rp * 18, o: (t > 10.86 ? 1 : 0) * (1 - Ease.inCubic(prog(t, 11.0, 11.2))) });
    const nav = Ease.inOutQuint(prog(t, 10.98, 11.38));
    app.style.transform = `translateX(${-nav * 120}px) scale(${APP_SCALE})`;
    rd.style.transform = `translateX(${(1 - nav) * 412 * APP_SCALE}px) scale(${APP_SCALE})`;
    rd.style.visibility = t > 10.9 ? 'visible' : 'hidden';
    const sc = Ease.inOutCubic(prog(t, 11.3, 12.15));
    tf(rimg, { y: -sc * 520 });
  };
});

// ------------------------------------------------------------------ S6 3D labs (11.85 to 15.18)
scene(11.85, 15.18, (root) => {
  bg(root, INK);
  root.style.perspective = '2400px';
  el('div', 'abs', root, { inset: 0, background: 'radial-gradient(80% 50% at 50% 0%, rgba(0,75,212,0.45), rgba(10,22,54,0) 70%)' });
  const head = makeHead(root, { kicker: 'New · 3D labs', lines: ['Science you', 'can *touch.*'], y: 230, onInk: true, fs: 112 });
  const SIMS = [['pendulum', 'Pendulum lab'], ['molecule', 'Molecules'], ['orbit', 'Earth · Moon · Sun']];
  const tiles = SIMS.map(([k, label]) => {
    const tile = el('div', 'abs', root, { borderRadius: '48px', overflow: 'hidden', background: '#0f1a3a', boxShadow: '0 40px 80px -30px rgba(0,0,0,.7)', border: '2px solid rgba(168,197,255,0.18)' });
    const img = el('img', null, tile, { position: 'absolute', left: '50%', top: '50%', width: '100%', height: '100%', objectFit: 'cover', transform: 'translate(-50%,-50%)' });
    const lab = html(tile, `<div class="abs" style="left:26px;bottom:26px;padding:12px 22px;border-radius:999px;background:rgba(10,22,54,.72);color:#fff;font-size:28px;font-weight:600;display:flex;gap:10px;align-items:center">${ms('school', 28)}<span>${label}</span></div>`);
    return { tile, img, lab, k };
  });
  // layouts: [left, top, w, h] for big, small-a, small-b
  const BIG = [80, 600, 920, 820], SA = [80, 1450, 445, 330], SB = [555, 1450, 445, 330];
  const phases = [[11.85, [0, 1, 2]], [13.45, [1, 2, 0]], [14.3, [2, 0, 1]]];
  const slotRect = [BIG, SA, SB];
  CUE(12.0, 'whoosh', { gain: 0.6 }); CUE(12.08, 'flipcard'); CUE(12.22, 'flipcard', { pitch: 1.1 }); CUE(12.36, 'flipcard', { pitch: 1.2 });
  CUE(12.4, 'hum', { dur: 2.6 });
  CUE(13.45, 'swish', { gain: 0.7 }); CUE(14.3, 'swish', { gain: 0.7, pitch: 1.1 });
  CUE(14.85, 'whoosh', { gain: 0.8 });
  return (t) => {
    const wipe = Ease.inOutQuint(prog(t, 11.85, 12.18));
    root.style.clipPath = t < 12.18 ? `polygon(0 ${((1 - wipe) * 140).toFixed(2)}%, 100% ${((1 - wipe) * 140 - 40).toFixed(2)}%, 100% 100%, 0 100%)` : 'none';
    head.update(t, 12.02, 14.85);
    let ph = 0;
    for (let i = 0; i < phases.length; i++) if (t >= phases[i][0]) ph = i;
    const tPh = phases[ph][0];
    const prev = ph > 0 ? phases[ph - 1][1] : phases[0][1];
    const curr = phases[ph][1];
    const lp = ph === 0 ? 1 : sp(t - tPh, 'heavy');
    tiles.forEach((T, i) => {
      const r0 = slotRect[prev.indexOf(i)], r1 = slotRect[curr.indexOf(i)];
      const r = mix(r0, r1, lp);
      Object.assign(T.tile.style, { left: r[0] + 'px', top: r[1] + 'px', width: r[2] + 'px', height: r[3] + 'px' });
      const ep = sp(t - 12.05 - i * 0.14, 'pop');
      const out = Ease.inExpo(prog(t, 14.85 + i * 0.04, 15.15 + i * 0.04));
      tf(T.tile, { rx: (1 - ep) * 70, y: (1 - ep) * 260 - out * 1700, o: clamp((t - 12.05 - i * 0.14) * 6) });
      const f = Math.max(0, Math.floor((t - 11.85) * 30) + i * 17) % 150;
      const src = CAP + T.k + '/' + String(f).padStart(4, '0') + '.jpg';
      if (T.img.getAttribute('src') !== src) T.img.setAttribute('src', src);
      tf(T.lab, { o: clamp((t - 12.5 - i * 0.1) * 5) });
    });
    root.style.transform = `translateY(${-Ease.inOutQuint(prog(t, 14.85, 15.18)) * 1920}px)`;
  };
});

// ------------------------------------------------------------------ S7 Neby AI (14.85 to 18.12)
const Q = 'Why is the sky blue?';
const ANSWER = 'Sunlight holds every colour. Air molecules scatter **blue light** the most, because its waves are short. So blue reaches your eyes from all over the sky.';
scene(14.85, 18.12, (root) => {
  bg(root, PAPER);
  root.style.perspective = '2600px';
  const head = makeHead(root, { kicker: 'New · Neby AI chat', lines: ['Ask anything.', 'Neby *explains.*'], y: 230, fs: 108 });
  const { ph, scr } = makePhone(root, { left: '240px', top: '640px' });
  const app = makeApp(scr);
  statusBar(app);
  const tb = html(app, `<div class="topbar" style="border-bottom:1px solid #eceef2"><div class="iconbtn">${ic('back', 22)}</div>
    <div style="width:40px;height:40px;border-radius:50%;background:#dbe1ff;overflow:hidden;position:relative"></div>
    <div><div style="font-size:18px;font-weight:700">Neby</div><div style="font-size:12px;color:#5c6475">Your study buddy</div></div></div>`);
  const av = pixelCanvas(tb.children[1], 40, { position: 'absolute', left: 0, top: '2px', width: '40px', height: '40px' });
  av.width = 48; av.height = 48;
  const me = el('div', 'bubble-me', app, { top: '128px' }, Q);
  const nh = el('div', 'abs', app, { left: '18px', top: '206px', display: 'flex', alignItems: 'center', gap: '10px' });
  const nb = pixelCanvas(nh, 48, { width: '44px', height: '44px' });
  const nlabel = el('div', null, nh, { fontSize: '15px', fontWeight: 700 }, 'Neby');
  const dots = el('div', null, nh, { display: 'flex', gap: '5px', marginLeft: '4px' });
  const dd = [0, 1, 2].map(() => el('div', null, dots, { width: '7px', height: '7px', borderRadius: '50%', background: '#004ac6' }));
  const ans = el('div', 'answer', app, { top: '262px' });
  const words = [];
  ANSWER.split(' ').forEach((w, i, arr) => {
    const bold = /\*\*/.test(w);
    const s = el(bold ? 'b' : 'span', null, ans, { opacity: 0 }, w.replace(/\*\*/g, ''));
    words.push(s);
    if (i < arr.length - 1) ans.appendChild(document.createTextNode(' '));
  });
  const comp = html(app, `<div class="composer"><span class="txt"></span><span class="caret" style="width:2px;height:22px;background:#004ac6;margin-left:2px"></span><div class="send">${ic('send', 22, 2.4)}</div></div>`);
  const ctext = comp.querySelector('.txt'), caret = comp.querySelector('.caret'), send = comp.querySelector('.send');
  const BIGN = pixelCanvas(root, 240, { position: 'absolute', left: '800px', top: '1480px', zIndex: 15 });
  for (let i = 0; i < Q.length; i += 3) CUE(15.25 + (i / Q.length) * 0.5, 'type', { gain: 0.35 });
  CUE(15.8, 'send');
  CUE(15.95, 'bubble'); CUE(16.15, 'bubble', { pitch: 1.2 });
  for (let i = 0; i < 12; i++) CUE(16.45 + i * 0.105, 'stream', { gain: 0.22 });
  CUE(17.72, 'sparkle');
  CUE(15.98, 'coin', { gain: 0.45 });
  return (t) => {
    head.update(t, 15.0, 17.72);
    const ip = sp(t - 14.88, 'heavy');
    tf(ph, { y: (1 - ip) * 1000, rx: 6, ry: 8 - 4 * Ease.inOutCubic(prog(t, 15.2, 18)) });
    const n = Math.floor(Q.length * Ease.linear(prog(t, 15.25, 15.75)));
    const sent = t >= 15.8;
    ctext.textContent = sent ? 'Ask Neby anything' : Q.slice(0, n);
    ctext.style.color = sent || n === 0 ? '#8a90a0' : '#1d1f25';
    if (!sent && n === 0) ctext.textContent = 'Ask Neby anything';
    caret.style.opacity = !sent && Math.floor(t * 4) % 2 === 0 ? 1 : 0;
    tf(send, { s: 1 + 0.18 * Math.sin(Math.PI * prog(t, 15.75, 15.95)) });
    const mp = sp(t - 15.8, 'pop');
    tf(me, { y: (1 - mp) * 620, s: 0.7 + 0.3 * mp, o: sent ? 1 : 0 });
    const hp = sp(t - 15.95, 'pop');
    tf(nh, { o: clamp((t - 15.95) * 8), y: (1 - hp) * 30 });
    const thinking = t < 16.45;
    drawNeby(nb, 'classic', thinking ? 'think' : t < 17.72 ? 'talk' : 'success', thinking ? t - 15.95 : t < 17.72 ? t - 16.45 : t - 17.72, t < 17.72);
    drawNeby(av, 'classic', 'blink', t);
    dots.style.opacity = thinking ? 1 : 0;
    dd.forEach((d, i) => tf(d, { y: -5 * Math.max(0, Math.sin((t * 7) - i * 0.9)), o: 0.4 + 0.6 * Math.max(0, Math.sin((t * 7) - i * 0.9)) }));
    const rev = prog(t, 16.45, 17.7) * words.length;
    words.forEach((w, i) => {
      const p = clamp(rev - i);
      w.style.opacity = p.toFixed(3);
      w.style.filter = p < 1 ? `blur(${((1 - p) * 4).toFixed(2)}px)` : 'none';
    });
    const bp = sp(t - 16.0, 'bouncy');
    tf(BIGN, { y: (1 - bp) * 400, o: clamp((t - 16.0) * 6) });
    drawNeby(BIGN, 'classic', t < 16.45 ? 'think' : t < 17.72 ? 'talk' : 'celebrate', t < 16.45 ? t - 16 : t < 17.72 ? t - 16.45 : t - 17.72, true);
    root.style.transform = `translateY(${(1 - Ease.inOutQuint(prog(t, 14.85, 15.18))) * 1920}px)`;
    if (t > 17.85) tf(BIGN, { y: Ease.inCubic(prog(t, 17.85, 18.1)) * 500 });
  };
});

// ------------------------------------------------------------------ S8 PDF reader (17.85 to 20.18)
const PAGE_TXT = `A curved <i>mirror</i> is part of a polished sphere. A concave <i>mirror</i> bends light inward, to a point called the focus. Real images form in front of the <i>mirror</i>; virtual ones appear to lie behind it.`;
function readerUI(parent, night) {
  const a = el('div', 'app', parent, { transform: `scale(${APP_SCALE})`, background: night ? '#111317' : '#eceef2' });
  statusBar(a, night);
  const fg = night ? '#e7e9ed' : '#1d1f25';
  html(a, `<div class="topbar" style="color:${fg}"><div class="iconbtn">${ic('back', 22)}</div><div style="font-size:16px;font-weight:700">Physics · Class 12</div>
    <div style="margin-left:auto;display:flex"><div class="iconbtn">${ms('search', 23)}</div><div class="iconbtn">${ic('moon', 21)}</div><div class="iconbtn">${ic('more', 22)}</div></div></div>`);
  const page = html(a, `<div class="page" style="background:${night ? '#1b1d22' : '#fff'};color:${fg}">
    <div class="pk">Chapter 14 · Optics</div><div class="ph" style="margin-top:6px">Reflection at curved mirrors</div>
    <svg viewBox="0 0 340 150" style="width:100%;margin-top:14px" fill="none" stroke="${night ? '#b4c5ff' : '#004ac6'}" stroke-width="2.2">
      <path d="M300 10 Q 250 75 300 140" stroke-width="4" stroke="${fg}"/><line x1="10" y1="75" x2="320" y2="75" stroke-dasharray="5 6" stroke="${night ? '#6b7280' : '#9aa3b2'}"/>
      <path d="M20 40 L285 40 L190 75"/><path d="M20 110 L285 110 L190 75"/><circle cx="190" cy="75" r="5" fill="${night ? '#b4c5ff' : '#004ac6'}"/>
      <text x="183" y="98" font-size="13" fill="${fg}" stroke="none" font-family="Poppins">F</text><text x="95" y="98" font-size="13" fill="${fg}" stroke="none" font-family="Poppins">C</text><circle cx="100" cy="75" r="4" fill="${fg}" stroke="none"/></svg>
    <div class="tx" style="color:${night ? '#c9ccd3' : '#2b2f38'}">${PAGE_TXT}</div>
    <div class="ln" style="width:92%;background:${night ? '#2c2f36' : '#d9dde5'}"></div><div class="ln" style="width:84%;background:${night ? '#2c2f36' : '#d9dde5'}"></div><div class="ln" style="width:88%;background:${night ? '#2c2f36' : '#d9dde5'}"></div><div class="ln" style="width:60%;background:${night ? '#2c2f36' : '#d9dde5'}"></div>
    </div>`);
  html(a, `<div class="abs" style="left:16px;right:16px;bottom:30px;height:52px;border-radius:26px;background:${night ? '#1b1d22' : '#fff'};display:flex;align-items:center;padding:0 18px;gap:14px;color:${fg};box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <span style="font-size:14px;font-weight:700">42 / 186</span><div style="flex:1;height:4px;border-radius:2px;background:${night ? '#2c2f36' : '#e3e6ec'}"><div style="width:23%;height:100%;border-radius:2px;background:#004ac6"></div></div></div>`);
  return { a, page };
}
scene(17.85, 20.18, (root) => {
  root.style.perspective = '2600px';
  root.style.background = 'transparent';
  const head = makeHead(root, { kicker: 'Rebuilt · PDF reader', lines: ['Night mode.', 'Bookmarks.', '*Search.*'], y: 200, fs: 96 });
  const { ph, scr } = makePhone(root, { left: '240px', top: '640px' });
  const day = readerUI(scr, false);
  const nightBox = el('div', 'abs', scr, { inset: 0 });
  const night = readerUI(nightBox, true);
  const ribbon = html(night.page, `<div class="abs" style="right:22px;top:-6px;width:30px;height:62px;background:#e5484d;clip-path:polygon(0 0,100% 0,100% 100%,50% 78%,0 100%)"></div>`);
  const tx = night.page.querySelector('.tx');
  const marks = [...tx.querySelectorAll('i')];
  marks.forEach((m) => { m.style.fontStyle = 'normal'; m.style.borderRadius = '4px'; m.style.padding = '0 2px'; m.style.margin = '0 -2px'; });
  const sbar = html(night.a, `<div class="abs" style="left:12px;right:12px;top:46px;height:52px;border-radius:26px;background:#2a2d34;color:#e7e9ed;display:flex;align-items:center;padding:0 18px;gap:10px;font-size:16px">
    ${ms('search', 22)}<span class="q"></span><span style="margin-left:auto;font-size:13px;color:#9aa0ab" class="cnt"></span></div>`);
  const sq = sbar.querySelector('.q'), scnt = sbar.querySelector('.cnt');
  const flip = el('div', 'abs', scr, { left: '0', top: '0', width: '100%', height: '100%', transformOrigin: '0% 50%', background: '#1b1d22', visibility: 'hidden', boxShadow: '-30px 0 60px rgba(0,0,0,.4)' });
  CUE(18.2, 'toggle'); CUE(18.22, 'whoosh', { gain: 0.45, dur: 0.3 });
  CUE(18.72, 'ploink');
  CUE(19.2, 'type', { gain: 0.3 }); CUE(19.3, 'type', { gain: 0.3 });
  CUE(19.42, 'ping'); CUE(19.52, 'ping', { pitch: 1.12 }); CUE(19.62, 'ping', { pitch: 1.25 });
  CUE(19.85, 'pageflip');
  return (t) => {
    const inn = Ease.inOutQuint(prog(t, 17.85, 18.15));
    head.update(t, 17.95, 19.9, [18.1, 18.62, 19.12]);
    tf(ph, { x: (1 - inn) * 1200, rx: 6, ry: -8 });
    const nr = Ease.inOutCubic(prog(t, 18.2, 18.6));
    nightBox.style.clipPath = `circle(${(nr * 1500).toFixed(1)}px at 500px 140px)`;
    const rb = sp(t - 18.7, 'bouncy');
    tf(ribbon, { y: (rb - 1) * 70, o: t > 18.7 ? 1 : 0 });
    const sb = sp(t - 19.1, 'snappy');
    tf(sbar, { y: (1 - sb) * -80, o: t > 19.1 ? 1 : 0 });
    const q = 'mirror';
    sq.textContent = q.slice(0, Math.floor(q.length * prog(t, 19.15, 19.38)));
    scnt.textContent = t > 19.42 ? '1 of 12' : '';
    marks.forEach((m, i) => {
      const p = sp(t - 19.42 - i * 0.1, 'pop');
      m.style.background = t > 19.42 + i * 0.1 ? `rgba(255,176,32,${(0.55 * clamp(p)).toFixed(3)})` : 'transparent';
      m.style.outline = i === 0 && t > 19.42 ? '2px solid rgba(255,176,32,0.95)' : 'none';
    });
    const fp = Ease.inOutCubic(prog(t, 19.82, 20.1));
    flip.style.visibility = t > 19.82 && t < 20.12 ? 'visible' : 'hidden';
    flip.style.transform = `perspective(1600px) rotateY(${-fp * 100}deg)`;
    const out = Ease.inOutQuint(prog(t, 19.85, 20.18));
    root.style.transform = `translateX(${-out * 1080}px)`;
  };
});

// ------------------------------------------------------------------ S9 canvas board (19.85 to 22.18)
scene(19.85, 22.18, (root) => {
  bg(root, '#fbfcfe');
  const board = el('div', 'abs', root, { left: 0, top: 0, width: '1080px', height: '1920px', transformOrigin: '540px 1000px' });
  dotGrid(board, 'rgba(10,22,54,0.13)', 40, 2.4);
  const head = makeHead(root, { kicker: 'Canvas', lines: ['Map any topic.', 'Neby adds *cards.*'], y: 200, fs: 100 });
  const svg = svgEl('svg', { width: 1080, height: 1920, viewBox: '0 0 1080 1920' }, board);
  svg.style.position = 'absolute'; svg.style.left = 0; svg.style.top = 0;
  const C = [
    { x: 540, y: 960, k: 'Topic', tt: 'Photosynthesis', col: '#004bd4', t: 20.1, big: true },
    { x: 250, y: 720, k: 'Where', tt: 'Chloroplast', col: '#0f9d8a', t: 20.32 },
    { x: 820, y: 730, k: 'Stage 1', tt: 'Light reactions', col: '#f29d0c', t: 20.44 },
    { x: 250, y: 1200, k: 'Stage 2', tt: 'Calvin cycle', col: '#2e9e44', t: 20.56 },
    { x: 830, y: 1210, k: 'Makes', tt: 'Glucose', col: '#e5484d', t: 20.68 },
    { x: 540, y: 1430, k: 'Added by Neby', tt: '6CO<sub>2</sub> + 6H<sub>2</sub>O <span class="ms" style="font-size:34px;vertical-align:-6px">arrow_forward</span> C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> + 6O<sub>2</sub>', col: '#004bd4', t: 21.5, neby: true },
  ];
  const edges = C.slice(1).map((c) => {
    const mx = (540 + c.x) / 2, my = (960 + c.y) / 2;
    const d = `M540 960 Q ${mx + (c.y - 960) * 0.18} ${my - (c.x - 540) * 0.18} ${c.x} ${c.y}`;
    const p = svgEl('path', { d, fill: 'none', stroke: '#9aa6bd', 'stroke-width': 5, 'stroke-linecap': 'round' }, svg);
    const L = 700;
    p.setAttribute('stroke-dasharray', `${L} ${L}`);
    return { p, L, t: c.t - 0.06 };
  });
  const cards = C.map((c) => {
    const e = html(board, `<div class="ccard" style="left:${c.x}px;top:${c.y}px;${c.big ? 'padding:30px 40px 30px 46px' : ''}">
      <div class="spine" style="background:${c.col}"></div><div class="ck">${c.k}</div><div class="ct" style="${c.big ? 'font-size:56px' : ''}${c.neby ? ';font-size:34px' : ''}">${c.tt}</div></div>`);
    return { e, c };
  });
  const prompt = html(root, `<div class="abs" style="left:70px;right:70px;top:1585px;height:118px;border-radius:59px;background:${INK};color:#fff;display:flex;align-items:center;padding:0 16px 0 22px;gap:18px;box-shadow:0 30px 60px -30px rgba(10,22,54,.6)">
    <div class="nb" style="width:84px;height:84px;border-radius:50%;background:#1a3170;position:relative;overflow:hidden"></div>
    <span class="pt" style="font-size:34px;font-weight:500"></span>
    <div style="margin-left:auto;width:86px;height:86px;border-radius:50%;background:${BLUE};display:flex;align-items:center;justify-content:center">${ic('send', 40, 2.6)}</div></div>`);
  const pnb = pixelCanvas(prompt.querySelector('.nb'), 96, { position: 'absolute', left: '-6px', top: '-2px' });
  const pt = prompt.querySelector('.pt');
  CUE(20.1, 'pop', { gain: 0.6 });
  C.slice(1, 5).forEach((c, i) => { CUE(c.t - 0.06, 'draw', { gain: 0.3 }); CUE(c.t, 'pop', { gain: 0.4, pitch: 1 + i * 0.1 }); });
  for (let i = 0; i < 6; i++) CUE(20.95 + i * 0.07, 'type', { gain: 0.3 });
  CUE(21.42, 'send'); CUE(21.5, 'pop', { gain: 0.6, pitch: 1.3 }); CUE(21.52, 'sparkle', { gain: 0.6 });
  CUE(21.85, 'whoosh', { gain: 0.8 });
  return (t) => {
    const inn = Ease.inOutQuint(prog(t, 19.85, 20.18));
    root.style.transform = `translateX(${(1 - inn) * 1080 - Ease.inOutQuint(prog(t, 21.85, 22.18)) * 1080}px)`;
    head.update(t, 20.0, 21.85);
    const z = 1.12 - 0.14 * Ease.inOutCubic(prog(t, 20.0, 22.1));
    board.style.transform = `translate(${-20 * Ease.inOutCubic(prog(t, 20, 22))}px, ${30 - 60 * Ease.inOutCubic(prog(t, 20, 22))}px) scale(${z})`;
    cards.forEach(({ e, c }) => {
      const p = sp(t - c.t, 'bouncy');
      e.style.transform = `translate(-50%,-50%) scale(${(0.3 + 0.7 * p).toFixed(4)})`;
      e.style.opacity = clamp((t - c.t) * 8).toFixed(3);
    });
    edges.forEach((ed) => {
      const p = Ease.outCubic(prog(t, ed.t, ed.t + 0.32));
      ed.p.setAttribute('stroke-dashoffset', ((1 - p) * ed.L).toFixed(1));
      ed.p.style.opacity = t > ed.t ? 1 : 0;
    });
    const pp = sp(t - 20.7, 'pop');
    tf(prompt, { y: (1 - pp) * 260, o: clamp((t - 20.7) * 6) });
    const s = 'Add the equation';
    pt.textContent = t < 20.95 ? 'Ask Neby to add a card…' : s.slice(0, Math.ceil(s.length * prog(t, 20.95, 21.38)));
    pt.style.opacity = t < 20.95 ? 0.55 : 1;
    drawNeby(pnb, 'classic', t < 21.45 ? 'think' : 'success', t - 20.7);
  };
});

// ------------------------------------------------------------------ S10 community (21.85 to 24.18)
const POSTS = [
  { n: 'Aarav S.', m: 'Class 12 · 2m', av: '#ffd8a8', ini: 'A', body: 'Stuck on this circuit <span class="chip" style="background-image:url(' + ROOT + 'img/pixel-art/banner/physics-2-day.png)"></span> Any tips?', likes: [9, 24], c: 8, rot: -5 },
  { n: 'Sneha K.', m: 'Class 12 · 1m', av: '#c3fae8', ini: 'S', body: 'Current splits at each junction. Use V = IR on every branch.', likes: [12, 31], c: 3, rot: 4 },
  { n: 'Neby', m: 'AI study buddy · now', neby: true, body: 'Kirchhoff’s laws, solved: <span class="lk">nebians.consica.com.np</span>', likes: [5, 18], c: 2, rot: -2 },
];
scene(21.85, 24.18, (root) => {
  bg(root, INK);
  el('div', 'abs', root, { inset: 0, background: 'radial-gradient(70% 40% at 50% 100%, rgba(0,75,212,0.45), rgba(10,22,54,0) 70%)' });
  const head = makeHead(root, { kicker: 'Community', lines: ['Ask. Answer.', 'Grow *together.*'], y: 200, onInk: true, fs: 108 });
  const posts = POSTS.map((p, i) => {
    const e = html(root, `<div class="post" style="top:${570 + i * 350}px">
      <div class="who"><div class="av" style="background:${p.neby ? '#dbe1ff' : p.av}">${p.neby ? '' : `<span style="font-size:36px;font-weight:800;color:${INK};align-self:center">${p.ini}</span>`}</div>
      <div><div class="nm">${p.n}${p.neby ? ` <span style="color:${BLUE}">${ms('verified', 30)}</span>` : ''}</div><div class="mt">${p.m}</div></div></div>
      <div class="bd">${p.body}</div>
      <div class="ft"><span class="lk2">${ms('thumb_up', 34)}<span class="lc">${p.likes[0]}</span></span><span>${ms('chat_bubble', 32)}${p.c}</span></div></div>`);
    let cv = null;
    if (p.neby) cv = pixelCanvas(e.querySelector('.av'), 96, { width: '78px', height: '78px' });
    return { e, p, lc: e.querySelector('.lc'), lk: e.querySelector('.lk2'), cv };
  });
  CUE(22.0, 'whoosh', { gain: 0.5 });
  posts.forEach((P, i) => CUE(22.12 + i * 0.28, 'card', { gain: 0.55, pitch: 1 + i * 0.08 }));
  for (let i = 0; i < 8; i++) CUE(23.1 + i * 0.07, 'like', { gain: 0.3, pitch: 1 + i * 0.05 });
  CUE(23.85, 'whoosh', { gain: 0.8 });
  return (t) => {
    const inn = Ease.inOutQuint(prog(t, 21.85, 22.18));
    root.style.transform = `translateX(${(1 - inn) * 1080}px)`;
    head.update(t, 22.0, 23.85);
    posts.forEach((P, i) => {
      const s = sp(t - 22.12 - i * 0.28, 'heavy');
      const out = Ease.inExpo(prog(t, 23.85 + i * 0.03, 24.15 + i * 0.03));
      tf(P.e, { y: (1 - s) * 1200 + out * 1400, r: P.p.rot * (1 - s) + P.p.rot * 0.25, o: clamp((t - 22.12 - i * 0.28) * 5) });
      const lp = Ease.outExpo(prog(t, 23.1, 23.7));
      P.lc.textContent = Math.round(P.p.likes[0] + (P.p.likes[1] - P.p.likes[0]) * lp);
      P.lk.style.color = t > 23.1 ? BLUE : '';
      tf(P.lk, { s: 1 + 0.25 * Math.sin(Math.PI * prog(t, 23.1 + i * 0.05, 23.35 + i * 0.05)) });
      if (P.cv) drawNeby(P.cv, 'classic', 'talk', t);
    });
  };
});

// ------------------------------------------------------------------ S11 Neby's wardrobe (23.85 to 26.62)
const LOOKS = [
  ['dashain', 'tika', 'Dashain'], ['tihar', 'diyo', 'Tihar'], ['holi', 'splash', 'Holi'], ['teej', 'deusi', 'Teej'],
  ['losar', 'namaste', 'Losar'], ['new-year', 'fireworks', 'New Year'], ['graduate', 'success', 'Graduate'], ['astronaut', 'hop', 'Astronaut'],
  ['wizard', 'cool', 'Wizard'], ['headphones', 'talk', 'Headphones'], ['scientist', 'read', 'Scientist'], ['crown', 'celebrate', 'Champion'],
];
const MORE = ['Images in posts', 'Clickable links', 'Your own avatar', 'Account security', 'Faster on every phone'];
scene(23.85, 26.62, (root) => {
  bg(root, PAPER);
  const head = makeHead(root, { kicker: 'Meet Neby', lines: ['Dressed up for', 'every *festival.*'], y: 200, fs: 100 });
  const grid = el('div', 'abs', root, { left: '60px', top: '560px', width: '960px', height: '860px' });
  const cells = LOOKS.map(([look, state, label], i) => {
    const c = el('div', 'abs', grid, { left: (i % 4) * 240 + 'px', top: Math.floor(i / 4) * 280 + 'px', width: '240px', height: '270px', display: 'flex', flexDirection: 'column', alignItems: 'center' });
    const cv = pixelCanvas(c, 192, { width: '192px', height: '192px' });
    cv.width = 48; cv.height = 48;
    el('div', null, c, { fontSize: '27px', fontWeight: 700, color: INK, marginTop: '6px' }, label);
    return { c, cv, look, state, i, d: (i % 4) * 0.05 + Math.floor(i / 4) * 0.08 };
  });
  const more = el('div', 'abs', root, { left: 0, top: '1430px', width: '4000px', display: 'flex', gap: '18px' });
  const chips = [...MORE, ...MORE].map((m) => html(more, `<div class="pill" style="background:${INK};color:#fff;font-size:34px;white-space:nowrap">${ms('check_circle', 34)}<span>${m}</span></div>`));
  const kick = el('div', 'abs center-x kicker', root, { top: '1366px', color: BLUE, justifyContent: 'center', display: 'flex', fontSize: '26px' }, 'And more in v1.7');
  CUE(23.98, 'whoosh', { gain: 0.6 });
  cells.forEach((c) => CUE(24.15 + c.d, 'chip', { gain: 0.32, note: c.i }));
  CUE(25.2, 'swish', { gain: 0.6 });
  CUE(26.0, 'riser', { dur: 0.5, gain: 0.7 });
  return (t) => {
    const inn = Ease.inOutQuint(prog(t, 23.85, 24.18));
    root.style.clipPath = t < 24.18 ? `inset(${((1 - inn) * 100).toFixed(2)}% 0 0 0 round 80px 80px 0 0)` : 'none';
    head.update(t, 24.0, 26.3);
    cells.forEach((c) => {
      const p = sp(t - 24.15 - c.d, 'bouncy');
      const o2 = Ease.inExpo(prog(t, 26.3 + c.d * 0.5, 26.6 + c.d * 0.5));
      tf(c.c, { s: (0.2 + 0.8 * p) * (1 - o2), o: clamp((t - 24.15 - c.d) * 7), y: (1 - p) * 60 });
      drawNeby(c.cv, c.look, c.state, t - 24.15 - c.d);
    });
    const mp = Ease.outExpo(prog(t, 25.15, 25.6));
    tf(kick, { o: mp });
    tf(more, { x: 1080 - mp * 1020 - Math.max(0, t - 25.15) * 320, o: mp });
  };
});

// ------------------------------------------------------------------ S12 outro (26.3 to 32.0)
scene(26.3, 32.01, (root) => {
  bg(root, BLUE);
  const facets = el('div', 'abs', root, { inset: 0 });
  const FP = [['M-200 1500 L700 2100 L-200 2300 Z', 'rgba(0,40,140,0.55)'], ['M1300 -100 L500 -100 L1300 700 Z', 'rgba(70,130,255,0.35)'], ['M1300 1200 L780 1950 L1300 2000 Z', 'rgba(0,30,110,0.5)'], ['M-100 200 L360 -100 L-100 -100 Z', 'rgba(120,170,255,0.25)']];
  const fsvg = svgEl('svg', { width: 1080, height: 1920, viewBox: '0 0 1080 1920' }, facets);
  const fpaths = FP.map(([d, c]) => svgEl('path', { d, fill: c }, fsvg));
  const tile = el('div', 'abs', root, { left: '390px', top: '430px', width: '300px', height: '300px', borderRadius: '78px', background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 50px 90px -30px rgba(0,10,60,.55)', zIndex: 3 });
  const lg = makeLogo(tile, 210);
  const peek = pixelCanvas(root, 240, { position: 'absolute', left: '420px', top: '300px', zIndex: 2 });
  const word = el('div', 'abs center-x h-xxl', root, { top: '780px', color: '#fff' });
  const wc = splitChars(word, 'NEBians');
  const tag = el('div', 'abs center-x', root, { top: '990px', fontSize: '52px', fontWeight: 600, color: '#d7e4ff', letterSpacing: '-0.01em' });
  const tw = splitWords(tag, 'Study materials. Study mates.');
  const btnWrap = el('div', 'abs', root, { left: 0, right: 0, top: '1150px', display: 'flex', justifyContent: 'center' });
  const btn = html(btnWrap, `<div style="display:flex;align-items:center;gap:26px;padding:26px 54px 26px 40px;border-radius:999px;background:#05070c;color:#fff;box-shadow:0 40px 70px -30px rgba(0,0,0,.6)">
    <div style="width:84px;height:84px;border-radius:24px;background:#fff;color:${BLUE};display:flex;align-items:center;justify-content:center">${ic('play', 52)}</div>
    <div><div style="font-size:24px;font-weight:600;letter-spacing:.12em;opacity:.75">GET IT ON</div><div style="font-size:52px;font-weight:700;letter-spacing:-0.02em;line-height:1.05">Google Play</div></div></div>`);
  const ver = el('div', 'abs', root, { left: 0, right: 0, top: '1370px', display: 'flex', justifyContent: 'center' });
  const vp = html(ver, `<div class="pill" style="background:#d7e4ff;color:${INK};font-size:32px;padding:14px 30px">v1.7 · out now · free</div>`);
  const url = el('div', 'abs center-x', root, { top: '1470px', fontSize: '42px', fontWeight: 600, color: '#fff', opacity: 0.9 }, 'nebians.consica.com.np');
  CUE(26.5, 'boom', { gain: 0.9 });
  CUE(26.62, 'pop', { gain: 0.7, pitch: 0.8 });
  CUE(26.9, 'whoosh', { gain: 0.4, dur: 0.4 });
  CUE(27.2, 'coin', { gain: 0.5 });
  CUE(27.62, 'chime', { gain: 0.8 });
  CUE(28.05, 'pop', { gain: 0.4, pitch: 1.3 });
  CUE(28.3, 'tick', { gain: 0.4 });
  return (t) => {
    const inn = Ease.inOutQuint(prog(t, 26.3, 26.62));
    root.style.clipPath = t < 26.62 ? `polygon(0 ${(100 - inn * 140).toFixed(2)}%, 100% ${(100 - inn * 140 + 30).toFixed(2)}%, 100% 100%, 0 100%)` : 'none';
    fpaths.forEach((p, i) => { p.style.transform = `translate(${Math.sin(t * 0.6 + i) * 30}px, ${Math.cos(t * 0.5 + i * 2) * 30}px)`; });
    const ts = sp(t - 26.55, 'bouncy');
    tf(tile, { s: ts, r: (1 - ts) * -25, o: clamp((t - 26.55) * 10) });
    lg.facets.forEach((f, j) => {
      const s = sp(t - 26.62 - j * 0.04, 'pop');
      tf(f, { s: 0.3 + 0.7 * s, o: clamp((t - 26.62 - j * 0.04) * 10) });
    });
    const pk = sp(t - 27.15, 'bouncy');
    tf(peek, { y: (1 - pk) * 170 });
    drawNeby(peek, 'classic', t < 28.5 ? 'wave' : 'idle', t - 27.15);
    wc.forEach((s, i) => {
      const p = Ease.outExpo(prog(t, 26.85 + i * 0.035, 27.45 + i * 0.035));
      tf(s, { py: (1 - p) * 110, r: (1 - p) * 6 });
    });
    rise(tw, t, 27.2, { stagger: 0.06 });
    const bp = sp(t - 27.6, 'bouncy');
    tf(btn, { s: 0.4 + 0.6 * bp, o: clamp((t - 27.6) * 8) });
    const press = Math.sin(Math.PI * prog(t, 29.4, 29.65));
    if (t > 29.4) tf(btn, { s: 1 - 0.05 * press });
    tf(vp, { s: 0.5 + 0.5 * sp(t - 28.0, 'bouncy'), o: clamp((t - 28.0) * 8) });
    tf(url, { o: Ease.outCubic(prog(t, 28.25, 28.6)) * 0.92, y: (1 - Ease.outExpo(prog(t, 28.25, 28.9))) * 30 });
    const drift = Ease.inOutCubic(prog(t, 27, 32));
    root.style.transform = `scale(${1 + drift * 0.035})`;
  };
});
CUE(29.42, 'tap', { gain: 0.5 });

window.FAST = FAST;
window.SHAKES = SHAKES;
window.FLASHES = FLASHES;
