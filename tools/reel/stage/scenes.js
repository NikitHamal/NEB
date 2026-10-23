'use strict';
// NEBians v1.7 for Android: 1080x1920, 32 s, 120 BPM (a beat is 0.5 s, a bar is 2 s).
// Every app screen is a real recording or screenshot of the Android app (tools/reel/capture/app).
const CLIPS = {
  home: { clip: 'home', from: 0.0 },
  syllabus: { clip: 'syllabus', from: 0.0, speed: 1.4 },
  reader: { clip: 'reader', from: 0.0 },
  pendulum: { clip: 'pendulum', from: 0.0 },
  molecule: { clip: 'molecule', from: 0.0 },
  pdf: { clip: 'pdf', from: 1.2 },
  night: { clip: 'pdf-night', from: 0.0 },
  ai: { clip: 'pdf-ai', from: 0.0 },
  canvas: { clip: 'canvas', from: 0.0 },
};
const WALL = ['home-top', 'syllabus-class11', 'reader-top', 'interactive-pendulum', 'pdf-first', 'pdf-night',
  'pdf-ai-answer', 'canvas-board', 'library-top', 'syllabus-subject', 'interactive-molecule', 'home-mid',
  'reader-mid', 'resource-detail', 'canvas-list', 'library-scrolled'];

const SHAKES = [[2.0, 16], [4.0, 22], [26.5, 12]];
const FLASHES = [[2.0, 0.16], [4.0, 0.32], [26.5, 0.18]];
const FAST = [[1.7, 2.1], [3.55, 4.1], [5.25, 5.6], [8.35, 8.62], [11.35, 11.62], [13.85, 14.12], [16.85, 17.12],
  [19.85, 20.12], [22.85, 23.12], [24.85, 25.12], [26.3, 26.62]];

// ------------------------------------------------------------------ 0.0 hook: a wall of real screens
scene(0, 2.08, (root) => {
  bg(root, '#050a1c');
  const wall = el('div', 'abs', root, { left: '-420px', top: '-760px', width: '1920px', height: '3440px', transformOrigin: '50% 50%' });
  const shots = WALL.filter(hasStill);
  const cw = 330, chh = Math.round(cw * 2400 / 1080), gap = 46;
  const cards = [];
  for (let c = 0; c < 5; c++) {
    for (let r = 0; r < 4; r++) {
      const name = shots.length ? shots[(c * 3 + r * 2) % shots.length] : null;
      const card = el('div', 'abs', wall, { left: c * (cw + gap) + 'px', top: r * (chh + gap) + (c % 2) * 220 + 'px', width: cw + 'px', height: chh + 'px', borderRadius: '42px', overflow: 'hidden', background: '#16213f', boxShadow: '0 30px 60px -20px rgba(0,0,0,.6)' });
      if (name) el('img', null, card, { width: '100%', height: '100%', objectFit: 'cover' }).src = stillSrc(name);
      cards.push({ card, c, r });
    }
  }
  const shade = el('div', 'abs', root, { inset: 0, background: 'radial-gradient(70% 45% at 50% 50%, rgba(5,10,28,0.55), rgba(5,10,28,0.92) 100%)' });
  const l1 = el('div', 'abs center-x h-xl', root, { top: '640px', color: '#fff' });
  const w1 = splitWords(l1, "Nepal's study app");
  const l2 = el('div', 'abs center-x h-xl on-ink', root, { top: '780px', color: '#fff' });
  const w2 = splitWords(l2, 'just leveled up.');
  w2[2].classList.add('hl');
  const chip = el('div', 'abs', root, { left: 0, right: 0, top: '980px', display: 'flex', justifyContent: 'center' });
  const ci = html(chip, `<div class="pill" style="background:rgba(168,197,255,0.16);color:#d7e4ff;font-size:34px;border:2px solid rgba(168,197,255,0.35)">${ms('smartphone', 34)}<span>New on Android</span></div>`);
  CUE(0.0, 'impact', { gain: 0.7 });
  CUE(0.12, 'whoosh', { gain: 0.35, dur: 0.5 });
  CUE(0.55, 'tick'); CUE(0.8, 'tick', { pitch: 1.1 });
  CUE(1.02, 'pop', { gain: 0.45 });
  CUE(1.5, 'riser', { dur: 0.5 });
  return (t) => {
    const drift = Ease.inOutCubic(prog(t, 0, 2.05));
    const zoom = Ease.inExpo(prog(t, 1.6, 2.05));
    wall.style.transform = `perspective(2200px) rotateX(${28 - 6 * drift}deg) rotateZ(${-14 + 4 * drift}deg) translateY(${-drift * 520}px) scale(${0.92 + 0.12 * drift + zoom * 1.4})`;
    cards.forEach(({ card, c, r }) => {
      const p = Ease.outExpo(prog(t, 0.02 * (c + r), 0.6 + 0.02 * (c + r)));
      tf(card, { o: p, s: 0.85 + 0.15 * p });
    });
    shade.style.opacity = (0.75 + 0.25 * Ease.outCubic(prog(t, 0.3, 0.8))).toFixed(3);
    rise(w1, t, 0.12, { stagger: 0.06 });
    rise(w2, t, 0.55, { stagger: 0.07 });
    const cp = sp(t - 1.0, 'bouncy');
    tf(ci, { s: 0.5 + 0.5 * cp, o: clamp((t - 1.0) * 8) });
    root.style.opacity = (1 - Ease.inCubic(prog(t, 1.95, 2.08))).toFixed(3);
  };
});

// ------------------------------------------------------------------ 1.7 brand
scene(1.7, 4.12, (root) => {
  bg(root, PAPER);
  const grid = dotGrid(root, 'rgba(0,75,212,0.10)', 46, 2.2);
  const ring = el('div', 'abs', root, { left: '535px', top: '695px', width: '10px', height: '10px', borderRadius: '50%', border: `6px solid ${BLUE}` });
  const holder = el('div', 'abs', root, { left: 0, right: 0, top: '420px', display: 'flex', justifyContent: 'center' });
  const logo = makeLogo(holder, 520);
  const from = [[-520, -380, -48, 0.6], [560, -520, 40, 0.5], [620, 260, 75, 0.4], [-640, 420, -30, 0.7], [300, 640, 20, 0.5]];
  const order = [3, 0, 1, 2, 4];
  const wc = splitChars(el('div', 'abs center-x h-xxl', root, { top: '980px', color: INK }), 'NEBians');
  const t1 = splitWords(el('div', 'abs center-x h-m', root, { top: '1205px', color: INK }), 'Study materials.');
  const t2 = splitWords(el('div', 'abs center-x h-m', root, { top: '1285px', color: INK }), 'Study mates.');
  t2[1].classList.add('hl');
  const pill = el('div', 'abs', root, { left: 0, right: 0, top: '1440px', display: 'flex', justifyContent: 'center' });
  const pi = html(pill, `<div class="pill" style="background:${INK};color:#fff;font-size:36px;padding:20px 40px"><span style="color:${SKY}">Free</span><span style="opacity:.45">·</span><span>Made in Nepal</span></div>`);
  CUE(2.0, 'boom', { gain: 1.0 });
  order.forEach((k, j) => CUE(2.0 + j * 0.045, 'click', { gain: 0.35, pitch: 1 + j * 0.12 }));
  CUE(2.3, 'whoosh', { gain: 0.4, dur: 0.35 });
  CUE(2.72, 'pop', { gain: 0.5 }); CUE(2.95, 'pop', { gain: 0.55, pitch: 1.2 });
  CUE(3.2, 'chime', { gain: 0.8 });
  return (t) => {
    const r = Ease.inCubic(prog(t, 1.7, 2.02));
    root.style.clipPath = t < 2.02 ? `circle(${(r * 2300).toFixed(1)}px at 540px 960px)` : 'none';
    tf(grid, { y: -t * 24 });
    order.forEach((k, j) => {
      const s = sp(t - 2.0 - j * 0.045, 'pop');
      const [x, y, rot, sc] = from[k];
      tf(logo.facets[k], { x: x * (1 - s), y: y * (1 - s), r: rot * (1 - s), s: sc + (1 - sc) * s, o: clamp((t - 2.0 - j * 0.045) * 12) });
    });
    tf(holder, { s: 1 + 0.012 * Math.sin((t - 2) * 2.2) });
    const rp = Ease.outCubic(prog(t, 2.02, 2.7));
    tf(ring, { s: 1 + rp * 120, o: (1 - rp) * 0.5 });
    wc.forEach((s, i) => tf(s, { py: (1 - Ease.outExpo(prog(t, 2.3 + i * 0.035, 2.9 + i * 0.035))) * 110 }));
    rise(t1, t, 2.68, { stagger: 0.07 });
    rise(t2, t, 2.9, { stagger: 0.07 });
    const pp = sp(t - 3.18, 'bouncy');
    tf(pi, { s: 0.5 + 0.5 * pp, o: clamp((t - 3.18) * 8) });
    const out = Ease.inExpo(prog(t, 3.6, 4.0));
    root.style.transformOrigin = '540px 700px';
    root.style.transform = `scale(${1 + out * 5})`;
    root.style.opacity = (1 - Ease.inCubic(prog(t, 3.85, 4.05))).toFixed(3);
  };
});

// ------------------------------------------------------------------ 3.6 the v1.7 slam
scene(3.6, 5.62, (root) => {
  bg(root, INK);
  const glow = el('div', 'abs', root, { inset: 0, background: 'radial-gradient(60% 40% at 50% 50%, rgba(0,75,212,0.5), rgba(10,22,54,0) 70%)' });
  const l1 = el('div', 'abs center-x h-l', root, { top: '560px', color: '#fff' });
  const w1 = splitWords(l1, "What's new in");
  const v = el('div', 'abs center-x', root, { top: '660px', fontSize: '400px', fontWeight: 900, letterSpacing: '-0.06em', lineHeight: 1 }, 'v1.7');
  v.style.backgroundImage = 'linear-gradient(180deg,#ffffff 10%,#a8c5ff 90%)';
  v.style.webkitBackgroundClip = 'text';
  v.style.color = 'transparent';
  const sub = el('div', 'abs', root, { left: 0, right: 0, top: '1120px', display: 'flex', justifyContent: 'center' });
  const sp1 = html(sub, `<div class="pill" style="background:#fff;color:${INK};font-size:38px;padding:18px 36px">${ms('smartphone', 38)}<span>NEBians for Android</span></div>`);
  const bands = [];
  for (let i = 0; i < 8; i++) bands.push(el('div', 'abs', root, { left: 0, top: i * 240 + 'px', width: '1080px', height: '241px', background: PAPER, transformOrigin: i % 2 ? '100% 50%' : '0% 50%' }));
  CUE(3.62, 'swish', { gain: 0.4 });
  CUE(4.0, 'boom', { gain: 1.0 }); CUE(4.0, 'glitch', { gain: 0.45 });
  CUE(4.42, 'pop', { gain: 0.5 });
  CUE(5.22, 'whoosh', { gain: 0.8, dur: 0.38 });
  return (t) => {
    root.style.opacity = Ease.outCubic(prog(t, 3.6, 3.75)).toFixed(3);
    rise(w1, t, 3.66, { stagger: 0.06, dur: 0.45 });
    const vp = sp(t - 3.97, 'snappy');
    const z = Ease.inExpo(prog(t, 5.1, 5.4));
    tf(v, { s: (1.5 - 0.5 * vp) * (1 + z * 7), o: clamp((t - 3.97) * 14), y: z * 300 });
    tf(l1, { o: 1 - z });
    tf(sp1, { s: 0.5 + 0.5 * sp(t - 4.4, 'bouncy'), o: clamp((t - 4.4) * 8) * (1 - z) });
    tf(glow, { s: 1 + 0.3 * vp });
    bands.forEach((b, i) => tf(b, { sx: Ease.inOutQuint(prog(t, 5.22 + i * 0.018, 5.44 + i * 0.018)) }));
  };
});

// ------------------------------------------------------------------ features on real footage
function feature(o) {
  return scene(o.a, o.b, (root) => {
    const dark = !!o.dark;
    bg(root, dark ? INK : PAPER);
    root.style.perspective = '2600px';
    const blobs = glowBlobs(root, dark);
    if (!dark) dotGrid(root, 'rgba(0,75,212,0.07)', 46, 2);
    const head = makeHead(root, { kicker: o.kicker, lines: o.lines, y: o.headY || 250, onInk: dark, fs: o.fs || 104 });
    const P = makeRealPhone(root, { left: o.px ?? 260, top: o.py ?? 640, w: o.pw || 560 });
    const extra = o.build ? o.build(root, P) : null;
    const calls = (o.callouts || []).map((c) => ({ ...c, e: callout(root, { ...c, dark }) }));
    (o.cues || []).forEach(([t, type, opt]) => CUE(t, type, opt || {}));
    calls.forEach((c) => CUE(c.t, 'pop', { gain: 0.45, pitch: 1.1 }));
    const cam = o.camera || camKeys([[0, { rx: 4, ry: -6 }]]);
    return (t) => {
      const tl = t - o.a;
      blobs(t);
      head.update(t, o.a + 0.12, o.b - 0.5);
      let tx = 0, ty = 0;
      if (o.enter === 'right') tx += (1 - Ease.inOutQuint(prog(t, o.a, o.a + 0.32))) * 1080;
      if (o.enter === 'up') ty += (1 - Ease.inOutQuint(prog(t, o.a, o.a + 0.32))) * 1920;
      if (o.exit === 'left') tx -= Ease.inOutQuint(prog(t, o.b - 0.3, o.b)) * 1080;
      if (o.exit === 'up') ty -= Ease.inOutQuint(prog(t, o.b - 0.3, o.b)) * 1920;
      root.style.transform = `translate(${tx.toFixed(1)}px, ${ty.toFixed(1)}px)`;
      if (o.enter === 'wipe') root.style.clipPath = t < o.a + 0.34 ? `inset(${((1 - Ease.inOutQuint(prog(t, o.a, o.a + 0.34))) * 100).toFixed(2)}% 0 0 0 round 90px 90px 0 0)` : 'none';
      const ip = sp(tl - 0.05, 'heavy');
      const c = cam(tl);
      tf(P.ph, { x: c.x, y: c.y + (1 - ip) * 900, s: c.s, rx: c.rx + (1 - ip) * 24, ry: c.ry, r: (1 - ip) * -3 });
      o.play(P, t, tl);
      calls.forEach((k) => popIn(k.e, t, k.t, 0.6, o.b - 0.45));
      if (extra) extra(t, tl);
    };
  });
}

feature({
  a: 5.3, b: 8.62, enter: 'wipe', exit: 'left', kicker: 'All-new design', lines: ['A fresh new', '*look.*'],
  play: (P, t, tl) => playInto(P.img, CLIPS.home, tl, ['home-top']),
  camera: camKeys([[0, { rx: 4, ry: -6 }], [1.6, { rx: 2, ry: 4 }], [3.3, { s: 1.04, y: -20, ry: 6 }]]),
  callouts: [
    { t: 6.35, text: 'Pixel-art Neby', icon: 'auto_awesome', x: 60, y: 1010 },
    { t: 6.85, text: 'Festival themes', icon: 'star', x: 560, y: 1260 },
  ],
});

feature({
  a: 8.35, b: 11.62, enter: 'right', exit: 'left', kicker: 'New · Syllabus tab', lines: ['Class 8 to 12.', 'Every *chapter.*'],
  play: (P, t, tl) => playInto(P.img, CLIPS.syllabus, tl, ['syllabus-class11', 'syllabus-hub']),
  camera: camKeys([[0, { rx: 4, ry: 8 }], [1.8, { s: 1.06, y: -40, rx: 2, ry: -2 }], [3.2, { s: 1.06, y: -40, rx: 2, ry: -6 }]]),
  callouts: [
    { t: 9.4, text: 'Question banks', icon: 'quiz', x: 40, y: 1120 },
    { t: 9.9, text: 'Track your progress', icon: 'check_circle', x: 470, y: 1380 },
  ],
});

feature({
  a: 11.35, b: 14.12, enter: 'right', exit: 'left', kicker: 'Read in the app', lines: ['Chapters, notes', 'and *maths.*'],
  play: (P, t, tl) => playInto(P.img, CLIPS.reader, tl, ['reader-top', 'reader-mid']),
  camera: camKeys([[0, { rx: 8, ry: -4 }], [2.7, { s: 1.1, y: -60, rx: 14, ry: 2 }]]),
  callouts: [{ t: 12.3, text: 'Mark chapters done', icon: 'fact_check', x: 80, y: 1300 }],
});

feature({
  a: 13.85, b: 17.12, dark: true, enter: 'right', exit: 'up', kicker: 'New · 3D labs', lines: ['Science you', 'can *touch.*'],
  px: 70, pw: 470, py: 700,
  build: (root) => {
    const Q = makeRealPhone(root, { left: 540, top: 820, w: 470 });
    return (t, tl) => {
      const ip = sp(tl - 0.25, 'heavy');
      tf(Q.ph, { y: (1 - ip) * 1000 + Math.sin(tl * 1.4 + 1) * 8, rx: 4 + (1 - ip) * 24, ry: 8, r: (1 - ip) * 3 });
      playInto(Q.img, CLIPS.molecule, tl, ['interactive-molecule']);
    };
  },
  play: (P, t, tl) => playInto(P.img, CLIPS.pendulum, tl, ['interactive-pendulum']),
  camera: camKeys([[0, { rx: 4, ry: -8 }], [3.2, { s: 1.02, y: -20, rx: 2, ry: -4 }]]),
  callouts: [{ t: 15.0, text: 'Pendulum, molecules, orbits', icon: 'school', x: 150, y: 1720 }],
  cues: [[14.6, 'hum', { dur: 2.4 }]],
});

feature({
  a: 16.85, b: 20.12, enter: 'up', exit: 'left', kicker: 'Rebuilt · PDF reader', lines: ['Night mode.', 'Search. *Resume.*'],
  play: (P, t, tl) => (tl < 1.7 ? playInto(P.img, CLIPS.pdf, tl, ['pdf-first']) : playInto(P.img, CLIPS.night, tl - 1.7, ['pdf-night'])),
  camera: camKeys([[0, { rx: 4, ry: -6 }], [3.2, { s: 1.05, y: -30, rx: 2, ry: 6 }]]),
  callouts: [
    { t: 17.75, text: 'Night, sepia, paper', icon: 'svg:moon', x: 50, y: 1150 },
    { t: 18.3, text: 'Bookmarks', icon: 'bookmark', x: 640, y: 1420 },
  ],
});

feature({
  a: 19.85, b: 23.12, dark: true, enter: 'right', exit: 'left', kicker: 'New · AI in your PDFs', lines: ['Ask Neby about', 'any *page.*'],
  play: (P, t, tl) => playInto(P.img, CLIPS.ai, tl, ['pdf-ai-answer', 'pdf-ai-open']),
  camera: camKeys([[0, { rx: 4, ry: 6 }], [3.2, { s: 1.08, y: -60, rx: 2, ry: -4 }]]),
  callouts: [{ t: 21.0, text: 'Answers from your document', icon: 'psychology', x: 60, y: 1660 }],
  cues: [[20.6, 'sparkle', { gain: 0.6 }]],
});

feature({
  a: 22.85, b: 25.12, enter: 'right', exit: 'up', kicker: 'Canvas', lines: ['Map any topic', 'on a *board.*'],
  play: (P, t, tl) => playInto(P.img, CLIPS.canvas, tl, ['canvas-board', 'canvas-list']),
  camera: camKeys([[0, { rx: 4, ry: -6 }], [2.3, { s: 1.04, y: -20, rx: 2, ry: 4 }]]),
  callouts: [{ t: 23.6, text: 'Neby adds the cards', icon: 'auto_awesome', x: 300, y: 1500 }],
});

// ------------------------------------------------------------------ 24.85 and more
const MORE = [['Images and links in posts', 'forum'], ['Your own avatar', 'verified'], ['Account security', 'check_circle'], ['Faster on every phone', 'bolt']];
scene(24.85, 26.62, (root) => {
  bg(root, PAPER);
  const head = makeHead(root, { kicker: 'And more in v1.7', lines: ['Smoother.', '*Faster.*'], y: 300, fs: 120 });
  const rows = MORE.map(([text, icon], i) => html(root, `<div class="abs" style="left:150px;top:${760 + i * 150}px;display:flex;align-items:center;gap:24px;font-size:44px;font-weight:700;color:${INK}">
    <span style="width:84px;height:84px;border-radius:26px;background:${i % 2 ? INK : BLUE};color:#fff;display:flex;align-items:center;justify-content:center">${ms(icon, 46)}</span><span>${text}</span></div>`));
  const neby = pixelCanvas(root, 240, { position: 'absolute', left: '760px', top: '1380px' });
  CUE(24.9, 'whoosh', { gain: 0.5 });
  rows.forEach((r, i) => CUE(25.15 + i * 0.12, 'chip', { gain: 0.4, note: i * 2 }));
  CUE(26.0, 'riser', { dur: 0.5, gain: 0.7 });
  return (t) => {
    root.style.transform = `translateY(${(1 - Ease.inOutQuint(prog(t, 24.85, 25.15))) * 1920}px)`;
    head.update(t, 24.95, 26.25);
    rows.forEach((r, i) => {
      const p = sp(t - 25.15 - i * 0.12, 'pop');
      const q = Ease.inCubic(prog(t, 26.2 + i * 0.03, 26.45 + i * 0.03));
      tf(r, { x: (1 - p) * -200 + q * 1200, o: clamp((t - 25.15 - i * 0.12) * 7) });
    });
    tf(neby, { y: (1 - sp(t - 25.4, 'bouncy')) * 500 });
    drawNeby(neby, 'classic', 'celebrate', t - 25.4);
  };
});

// ------------------------------------------------------------------ 26.3 outro
scene(26.3, 32.01, (root) => {
  bg(root, BLUE);
  const fsvg = svgEl('svg', { width: 1080, height: 1920, viewBox: '0 0 1080 1920' }, el('div', 'abs', root, { inset: 0 }));
  const FP = [['M-200 1500 L700 2100 L-200 2300 Z', 'rgba(0,40,140,0.55)'], ['M1300 -100 L500 -100 L1300 700 Z', 'rgba(70,130,255,0.35)'], ['M1300 1200 L780 1950 L1300 2000 Z', 'rgba(0,30,110,0.5)'], ['M-100 200 L360 -100 L-100 -100 Z', 'rgba(120,170,255,0.25)']];
  const fpaths = FP.map(([d, c]) => svgEl('path', { d, fill: c }, fsvg));
  const tile = el('div', 'abs', root, { left: '390px', top: '430px', width: '300px', height: '300px', borderRadius: '78px', background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 50px 90px -30px rgba(0,10,60,.55)', zIndex: 3 });
  const lg = makeLogo(tile, 210);
  const peek = pixelCanvas(root, 240, { position: 'absolute', left: '420px', top: '268px', zIndex: 2 });
  const wc = splitChars(el('div', 'abs center-x h-xxl', root, { top: '780px', color: '#fff' }), 'NEBians');
  const tw = splitWords(el('div', 'abs center-x', root, { top: '990px', fontSize: '52px', fontWeight: 600, color: '#d7e4ff', letterSpacing: '-0.01em' }), 'Study materials. Study mates.');
  const btnWrap = el('div', 'abs', root, { left: 0, right: 0, top: '1150px', display: 'flex', justifyContent: 'center' });
  const btn = html(btnWrap, `<div style="display:flex;align-items:center;gap:26px;padding:26px 54px 26px 40px;border-radius:999px;background:#05070c;color:#fff;box-shadow:0 40px 70px -30px rgba(0,0,0,.6)">
    <div style="width:84px;height:84px;border-radius:24px;background:#fff;color:${BLUE};display:flex;align-items:center;justify-content:center">${ic('play', 52)}</div>
    <div><div style="font-size:24px;font-weight:600;letter-spacing:.12em;opacity:.75">GET IT ON</div><div style="font-size:52px;font-weight:700;letter-spacing:-0.02em;line-height:1.05">Google Play</div></div></div>`);
  const ver = el('div', 'abs', root, { left: 0, right: 0, top: '1370px', display: 'flex', justifyContent: 'center' });
  const vp = html(ver, `<div class="pill" style="background:#d7e4ff;color:${INK};font-size:32px;padding:14px 30px">v1.7 · out now · free</div>`);
  const url = el('div', 'abs center-x', root, { top: '1470px', fontSize: '42px', fontWeight: 600, color: '#fff' }, 'nebians.consica.com.np');
  CUE(26.5, 'boom', { gain: 0.9 });
  CUE(26.62, 'pop', { gain: 0.7, pitch: 0.8 });
  CUE(26.9, 'whoosh', { gain: 0.4, dur: 0.4 });
  CUE(27.2, 'coin', { gain: 0.5 });
  CUE(27.62, 'chime', { gain: 0.8 });
  CUE(28.05, 'pop', { gain: 0.4, pitch: 1.3 });
  CUE(28.3, 'tick', { gain: 0.4 });
  CUE(29.42, 'tap', { gain: 0.5 });
  return (t) => {
    const inn = Ease.inOutQuint(prog(t, 26.3, 26.62));
    root.style.clipPath = t < 26.62 ? `polygon(0 ${(100 - inn * 140).toFixed(2)}%, 100% ${(100 - inn * 140 + 30).toFixed(2)}%, 100% 100%, 0 100%)` : 'none';
    fpaths.forEach((p, i) => { p.style.transform = `translate(${Math.sin(t * 0.6 + i) * 30}px, ${Math.cos(t * 0.5 + i * 2) * 30}px)`; });
    const ts = sp(t - 26.55, 'bouncy');
    tf(tile, { s: ts, r: (1 - ts) * -25, o: clamp((t - 26.55) * 10) });
    lg.facets.forEach((f, j) => tf(f, { s: 0.3 + 0.7 * sp(t - 26.62 - j * 0.04, 'pop'), o: clamp((t - 26.62 - j * 0.04) * 10) }));
    tf(peek, { y: (1 - sp(t - 27.15, 'bouncy')) * 170 });
    drawNeby(peek, 'classic', t < 28.5 ? 'wave' : 'idle', t - 27.15);
    wc.forEach((s, i) => tf(s, { py: (1 - Ease.outExpo(prog(t, 26.85 + i * 0.035, 27.45 + i * 0.035))) * 110 }));
    rise(tw, t, 27.2, { stagger: 0.06 });
    tf(btn, { s: (0.4 + 0.6 * sp(t - 27.6, 'bouncy')) * (1 - 0.05 * Math.sin(Math.PI * prog(t, 29.4, 29.65))), o: clamp((t - 27.6) * 8) });
    tf(vp, { s: 0.5 + 0.5 * sp(t - 28.0, 'bouncy'), o: clamp((t - 28.0) * 8) });
    tf(url, { o: Ease.outCubic(prog(t, 28.25, 28.6)) * 0.92, y: (1 - Ease.outExpo(prog(t, 28.25, 28.9))) * 30 });
    root.style.transform = `scale(${1 + Ease.inOutCubic(prog(t, 27, 32)) * 0.035})`;
  };
});

window.CUES = CUES;
window.FAST = FAST;
window.SHAKES = SHAKES;
window.FLASHES = FLASHES;
