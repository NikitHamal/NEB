/**
 * How machines learn — a real neural network (2 inputs → two hidden layers of tanh neurons →
 * a sigmoid output) trained in the browser by backpropagation and the Adam optimiser on the
 * points you place. The background shows the network's current answer everywhere, the loss
 * (binary cross-entropy) falls on the graph, and a held-out test set reveals overfitting.
 * Tap to add a point, drag a point to move it.
 */
import { createKit, T, Ring, fmt, clamp, text, pill, withAlpha, card } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const KEYS = ['W1', 'b1', 'W2', 'b2', 'W3', 'b3'];
const MAXN = 260, HMAX = 12, GW = 56, GH = 42;

function makeNet() {
  const n = { H: 6 };
  const sz = { W1: 2 * HMAX, b1: HMAX, W2: HMAX * HMAX, b2: HMAX, W3: HMAX, b3: 1 };
  for (const key in sz) { n[key] = new Float64Array(sz[key]); n['g' + key] = new Float64Array(sz[key]); n['m' + key] = new Float64Array(sz[key]); n['v' + key] = new Float64Array(sz[key]); }
  n.h1 = new Float64Array(HMAX); n.h2 = new Float64Array(HMAX); n.d1 = new Float64Array(HMAX); n.d2 = new Float64Array(HMAX);
  n.t = 0;
  return n;
}
function initNet(n, H) {
  n.H = H; n.t = 0;
  const r = (s) => (Math.random() * 2 - 1) * s;
  for (const key of KEYS) { n[key].fill(0); n['m' + key].fill(0); n['v' + key].fill(0); }
  for (let i = 0; i < 2 * H; i++) n.W1[i] = r(Math.sqrt(6 / (2 + H)));
  for (let i = 0; i < H * H; i++) n.W2[i] = r(Math.sqrt(6 / (2 * H)));
  for (let i = 0; i < H; i++) n.W3[i] = r(Math.sqrt(6 / (H + 1)));
}
function forward(n, x, y) {
  const H = n.H;
  for (let j = 0; j < H; j++) n.h1[j] = Math.tanh(n.W1[j] * x + n.W1[H + j] * y + n.b1[j]);
  for (let j = 0; j < H; j++) { let s = n.b2[j]; for (let i = 0; i < H; i++) s += n.W2[i * H + j] * n.h1[i]; n.h2[j] = Math.tanh(s); }
  let o = n.b3[0]; for (let j = 0; j < H; j++) o += n.W3[j] * n.h2[j];
  return 1 / (1 + Math.exp(-o));
}

export default function init(stage) {
  const k = createKit(stage, { label: 'Points of two colours and a neural network learning to separate them' });
  const hud = createHud(stage);
  const badge = hud.badge('Press Train and watch the loss fall', '#7c3aed');

  const px = new Float64Array(MAXN), py = new Float64Array(MAXN), lab = new Uint8Array(MAXN), test = new Uint8Array(MAXN);
  let n = 0, cls = 1, training = false, lr = 0.03, H = 6, epoch = 0, noise = 0.15, holdout = true, preset = 'circle';
  const net = makeNet();
  const trL = new Ring(600), teL = new Ring(600);
  const grid = document.createElement('canvas'); grid.width = GW; grid.height = GH;
  const gctx = grid.getContext('2d'); const img = gctx.createImageData(GW, GH);
  const plot = new Plot({ title: 'Loss (lower is better)', xLabel: 'epoch', yLabel: '', yMin: 0, yMax: 0.8 });

  const panel = createPanel(stage, { title: 'Train a network' });
  const [trainB] = panel.buttonRow([{ label: 'Train', icon: 'play_arrow', onClick: () => { training = !training; trainB.setLabel(training ? 'Pause' : 'Train'); k.animate(true); } }, { label: 'New weights', icon: 'refresh', variant: 'ghost', onClick: () => { initNet(net, H); epoch = 0; trL.clear(); teL.clear(); k.invalidate(); } }]);
  panel.chips({ label: 'Data', options: [{ value: 'blobs', label: 'Two groups' }, { value: 'circle', label: 'Circle' }, { value: 'xor', label: 'XOR' }, { value: 'spiral', label: 'Spiral' }, { value: 'none', label: 'Empty' }], value: preset, onChange: (v) => { preset = v; makeData(); } });
  panel.chips({ label: 'Tap to add', options: [{ value: '1', label: 'orange points', color: '#f08c00' }, { value: '0', label: 'blue points', color: '#2563eb' }], value: '1', onChange: (v) => { cls = +v; } });
  panel.slider({ label: 'Hidden neurons per layer', min: 2, max: HMAX, step: 1, value: H, format: (v) => `${v}`, onChange: (v) => { H = v; initNet(net, H); epoch = 0; trL.clear(); teL.clear(); } });
  panel.slider({ label: 'Learning rate', min: -3, max: -0.7, step: 0.1, value: Math.log10(lr), format: (v) => fmt(Math.pow(10, v), 3), onChange: (v) => { lr = Math.pow(10, v); } });
  panel.slider({ label: 'Noise in the data', min: 0, max: 0.5, step: 0.05, value: noise, format: (v) => v.toFixed(2), onChange: (v) => { noise = v; makeData(); } });
  panel.toggle({ label: 'Hold back 25 % as a test set', value: true, onChange: (v) => { holdout = v; split(); } });
  const st = panel.stats([{ key: 'ep', label: 'Epochs' }, { key: 'tr', label: 'Training loss' }, { key: 'te', label: 'Test loss' }, { key: 'acc', label: 'Test accuracy' }]);
  panel.info('Each epoch the network guesses every training point, measures how wrong it was (the loss), and nudges every weight a little downhill (gradient descent). If test loss starts rising while training loss keeps falling, it is memorising: overfitting.');

  function split() { for (let i = 0; i < n; i++) test[i] = holdout && ((i * 7919) % 4 === 0) ? 1 : 0; k.invalidate(); }
  function makeData() {
    n = 0;
    const g = () => { let u = 0, v = 0; while (u === 0) u = Math.random(); v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
    const add = (x, y, c) => { if (n < MAXN) { px[n] = clamp(x + g() * noise * 0.4, -1, 1); py[n] = clamp(y + g() * noise * 0.4, -1, 1); lab[n] = c; n++; } };
    const N = 140;
    for (let i = 0; i < N && preset !== 'none'; i++) {
      if (preset === 'blobs') { const c = i % 2; add(c ? 0.45 : -0.45, c ? 0.35 : -0.35, c); }
      else if (preset === 'circle') { const c = i % 2, r = c ? Math.random() * 0.35 : 0.6 + Math.random() * 0.3, a = Math.random() * Math.PI * 2; add(r * Math.cos(a), r * Math.sin(a), c); }
      else if (preset === 'xor') { const x = Math.random() * 2 - 1, y = Math.random() * 2 - 1; add(x, y, x * y > 0 ? 1 : 0); }
      else if (preset === 'spiral') { const c = i % 2, t = (i >> 1) / (N / 2) * 2.4 * Math.PI, r = 0.12 + t / (2.4 * Math.PI) * 0.8, a = t + c * Math.PI; add(r * Math.cos(a), r * Math.sin(a), c); }
    }
    split(); initNet(net, H); epoch = 0; trL.clear(); teL.clear(); k.invalidate();
  }

  function trainEpoch() {
    const Hh = net.H;
    for (const key of KEYS) net['g' + key].fill(0);
    let cnt = 0;
    for (let s = 0; s < n; s++) {
      if (test[s]) continue; cnt++;
      const out = forward(net, px[s], py[s]);
      const dO = out - lab[s];
      net.gb3[0] += dO;
      for (let j = 0; j < Hh; j++) { net.gW3[j] += dO * net.h2[j]; net.d2[j] = dO * net.W3[j] * (1 - net.h2[j] * net.h2[j]); net.gb2[j] += net.d2[j]; }
      for (let i = 0; i < Hh; i++) { let s2 = 0; for (let j = 0; j < Hh; j++) { net.gW2[i * Hh + j] += net.d2[j] * net.h1[i]; s2 += net.W2[i * Hh + j] * net.d2[j]; } net.d1[i] = s2 * (1 - net.h1[i] * net.h1[i]); net.gb1[i] += net.d1[i]; net.gW1[i] += net.d1[i] * px[s]; net.gW1[Hh + i] += net.d1[i] * py[s]; }
    }
    if (!cnt) return;
    net.t++;
    const b1 = 0.9, b2 = 0.999, c1 = 1 - Math.pow(b1, net.t), c2 = 1 - Math.pow(b2, net.t);
    for (const key of KEYS) {
      const W = net[key], G = net['g' + key], M = net['m' + key], V = net['v' + key];
      for (let i = 0; i < W.length; i++) { const g = G[i] / cnt; M[i] = b1 * M[i] + (1 - b1) * g; V[i] = b2 * V[i] + (1 - b2) * g * g; W[i] -= lr * (M[i] / c1) / (Math.sqrt(V[i] / c2) + 1e-8); }
    }
    epoch++;
  }
  const L = { tr: 0, te: 0, acc: 0 };
  function losses() {
    let a = 0, an = 0, b = 0, bn = 0, ok = 0;
    for (let s = 0; s < n; s++) { const o = clamp(forward(net, px[s], py[s]), 1e-7, 1 - 1e-7), l = -(lab[s] ? Math.log(o) : Math.log(1 - o)); if (test[s]) { b += l; bn++; if ((o > 0.5) === !!lab[s]) ok++; } else { a += l; an++; } }
    L.tr = an ? a / an : 0; L.te = bn ? b / bn : NaN; L.acc = bn ? ok / bn : NaN;
  }

  let bx = 0, by = 0, bs = 100;
  k.onResize((w, h) => {
    if (k.small) { bs = Math.min(w - 24, h * 0.62); bx = (w - bs) / 2; by = 44; plot.box(10, by + bs + 8, w - 20, h - by - bs - 14); }
    else { bs = Math.min(h - 70, w * 0.55); bx = 20; by = 50; plot.box(bx + bs + 24, 50, w - bx - bs - 40, Math.min(260, h * 0.45)); }
  });
  const X = (v) => bx + (v + 1) / 2 * bs, Y = (v) => by + (1 - (v + 1) / 2) * bs;
  let held = -1;
  k.drag({
    hit: (x, y, s) => { let best = false; for (let i = 0; i < n; i++) { const d = Math.hypot(x - X(px[i]), y - Y(py[i])); if (d < 7 + s && (best === false || d < best)) best = d; } return best; },
    down: (x, y) => { let bd = 1e9; for (let i = 0; i < n; i++) { const d = Math.hypot(x - X(px[i]), y - Y(py[i])); if (d < bd) { bd = d; held = i; } } },
    move: (x, y) => { if (held >= 0) { px[held] = clamp((x - bx) / bs * 2 - 1, -1, 1); py[held] = clamp(1 - (y - by) / bs * 2, -1, 1); } },
    up: () => { held = -1; },
  });
  k.onTap((x, y) => { if (x > bx && x < bx + bs && y > by && y < by + bs && n < MAXN) { px[n] = (x - bx) / bs * 2 - 1; py[n] = 1 - (y - by) / bs * 2; lab[n] = cls; test[n] = holdout && ((n * 7919) % 4 === 0) ? 1 : 0; n++; k.invalidate(); } });

  k.frame((ctx, dt, w, h) => {
    if (training) { for (let i = 0; i < 6; i++) trainEpoch(); }
    losses();
    if (training) { trL.push(epoch, L.tr); if (!isNaN(L.te)) teL.push(epoch, L.te); }
    // decision map
    const d = img.data;
    for (let j = 0; j < GH; j++) for (let i = 0; i < GW; i++) {
      const o = forward(net, i / (GW - 1) * 2 - 1, 1 - j / (GH - 1) * 2), q = (j * GW + i) * 4;
      const t2 = o; d[q] = Math.round(37 + (240 - 37) * t2); d[q + 1] = Math.round(99 + (140 - 99) * t2); d[q + 2] = Math.round(235 + (0 - 235) * t2); d[q + 3] = Math.round(40 + 80 * Math.abs(o - 0.5) * 2);
    }
    gctx.putImageData(img, 0, 0);
    ctx.fillStyle = '#f7f8fd'; ctx.fillRect(0, 0, w, h);
    card(ctx, bx - 4, by - 4, bs + 8, bs + 8, 10);
    ctx.imageSmoothingEnabled = true; ctx.drawImage(grid, bx, by, bs, bs);
    // 0.5 contour hint: a thin grid
    ctx.strokeStyle = 'rgba(23,32,51,0.06)'; ctx.lineWidth = 1; ctx.beginPath(); for (let v = -1; v <= 1; v += 0.5) { ctx.moveTo(X(v), by); ctx.lineTo(X(v), by + bs); ctx.moveTo(bx, Y(v)); ctx.lineTo(bx + bs, Y(v)); } ctx.stroke();
    for (let i = 0; i < n; i++) {
      const c = lab[i] ? '#f08c00' : '#2563eb';
      ctx.beginPath(); ctx.arc(X(px[i]), Y(py[i]), test[i] ? 4.5 : 4, 0, Math.PI * 2);
      if (test[i]) { ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = c; ctx.lineWidth = 2; ctx.stroke(); }
      else { ctx.fillStyle = c; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.2; ctx.stroke(); }
    }
    if (!k.small) text(ctx, 'filled = training data · hollow = test data', bx, by + bs + 20, T.mute, 10, 600);
    // loss plot
    const ymax = Math.max(0.8, trL.n ? Math.min(2, trL.y[trL.idx(0)] * 1.1) : 0.8);
    plot.range(0, Math.max(50, epoch), 0, ymax).frame(ctx);
    plot.clip(ctx); plot.ring(ctx, trL, '#7c3aed', 2.2); plot.ring(ctx, teL, T.orange, 2); plot.unclip(ctx);
    text(ctx, 'training', plot.ix + plot.iw - 90, plot.y + 18, '#7c3aed', 10.5, 700); text(ctx, 'test', plot.ix + plot.iw - 30, plot.y + 18, T.orange, 10.5, 700);
    if (!k.small) drawNet(ctx, plot.x, plot.y + plot.h + 16, plot.w, h - plot.y - plot.h - 30);
    st.ep.set(String(epoch)); st.tr.set(fmt(L.tr, 3)); st.te.set(isNaN(L.te) ? '—' : fmt(L.te, 3)); st.acc.set(isNaN(L.acc) ? '—' : `${fmt(L.acc * 100, 0)} %`);
    badge.set(!training ? (epoch ? 'Paused. Add points or change the network, then train again' : 'Press Train and watch the loss fall') : teL.n > 50 && L.te > L.tr * 1.8 ? 'Test loss is much higher than training loss: overfitting' : `Epoch ${epoch}: loss ${fmt(L.tr, 3)}`);
    k.animate(training || held >= 0);
  });

  function drawNet(ctx, x, y, w, h) {
    if (h < 90) return;
    card(ctx, x, y, w, h, 12);
    text(ctx, 'The network (line thickness = weight size)', x + 12, y + 20, T.ink, 11, 700);
    const Hh = net.H, cols = [2, Hh, Hh, 1], lx = (c) => x + 30 + c * (w - 60) / 3, ly = (c, i) => y + 36 + (i + 0.5) * (h - 46) / cols[c];
    for (let c = 0; c < 3; c++) for (let i = 0; i < cols[c]; i++) for (let j = 0; j < cols[c + 1]; j++) {
      const wv = c === 0 ? net.W1[i * Hh + j] : c === 1 ? net.W2[i * Hh + j] : net.W3[i];
      ctx.strokeStyle = wv > 0 ? withAlpha('#f08c00', Math.min(0.8, Math.abs(wv) * 0.4)) : withAlpha('#2563eb', Math.min(0.8, Math.abs(wv) * 0.4)); ctx.lineWidth = Math.min(3, 0.4 + Math.abs(wv));
      ctx.beginPath(); ctx.moveTo(lx(c), ly(c, i)); ctx.lineTo(lx(c + 1), ly(c + 1, j)); ctx.stroke();
    }
    for (let c = 0; c < 4; c++) for (let i = 0; i < cols[c]; i++) { ctx.beginPath(); ctx.arc(lx(c), ly(c, i), 5, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = T.ink2; ctx.lineWidth = 1.2; ctx.stroke(); }
  }

  makeData();
  k.debug = { train: () => { training = true; k.animate(true); }, stats: () => [epoch, L.tr, L.te, L.acc], pt: (i) => [X(px[i]), Y(py[i])] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
