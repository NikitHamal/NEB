/**
 * Teaching machines to see — draw a digit on the pad. The drawing is turned into what the computer
 * actually gets: a 28 × 28 grid of brightness numbers (0–255), cropped and centred by its centre of
 * mass the way the MNIST dataset is prepared. A nearest-template classifier compares that grid
 * with digits rendered in several typefaces (cosine similarity on lightly blurred pixels) and turns
 * the similarities into probabilities with a softmax. A confusion matrix from a held-out test set
 * shows which digits it mixes up.
 */
import { createKit, T, fmt, clamp, text, pill, withAlpha, card } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const N = 28, D = N * N;
const FONTS = ['700 22px Poppins, sans-serif', '400 23px Georgia, serif', '600 22px ui-monospace, monospace', '500 22px system-ui, sans-serif', 'italic 600 22px Georgia, serif'];

function prep(src, out) {
  let minX = N, minY = N, maxX = -1, maxY = -1, sum = 0;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const v = src[y * N + x]; if (v > 0.1) { minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y); } sum += v; }
  out.fill(0);
  if (maxX < 0 || sum < 1) return false;
  const bw = maxX - minX + 1, bh = maxY - minY + 1, s = 20 / Math.max(bw, bh);
  const tmp = new Float32Array(D);
  let cx = 0, cy = 0, m = 0;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const sx = minX + (x - (N - bw * s) / 2) / s, sy = minY + (y - (N - bh * s) / 2) / s;
    const ix = Math.floor(sx), iy = Math.floor(sy);
    if (ix < minX || iy < minY || ix > maxX || iy > maxY) continue;
    const v = src[iy * N + ix]; tmp[y * N + x] = v; cx += x * v; cy += y * v; m += v;
  }
  const dx = Math.round(N / 2 - 0.5 - cx / m), dy = Math.round(N / 2 - 0.5 - cy / m);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const sx = x - dx, sy = y - dy; if (sx >= 0 && sy >= 0 && sx < N && sy < N) out[y * N + x] = tmp[sy * N + sx]; }
  // light blur, then normalise to unit length
  const b = new Float32Array(D);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { let s2 = 0, w = 0; for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) { const xx = x + i, yy = y + j; if (xx >= 0 && yy >= 0 && xx < N && yy < N) { const ww = i === 0 && j === 0 ? 4 : i === 0 || j === 0 ? 2 : 1; s2 += out[yy * N + xx] * ww; w += ww; } } b[y * N + x] = s2 / w; }
  let L = 0; for (let i = 0; i < D; i++) L += b[i] * b[i]; L = Math.sqrt(L) || 1;
  for (let i = 0; i < D; i++) out[i] = b[i] / L;
  return true;
}
function render(digit, font, rot, scale, thick) {
  const c = document.createElement('canvas'); c.width = c.height = N;
  const g = c.getContext('2d');
  g.fillStyle = '#000'; g.fillRect(0, 0, N, N);
  g.translate(N / 2, N / 2); g.rotate(rot); g.scale(scale, scale);
  g.font = font; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#fff'; g.strokeStyle = '#fff'; g.lineWidth = thick;
  g.fillText(String(digit), 0, 1); if (thick > 0) g.strokeText(String(digit), 0, 1);
  const d = g.getImageData(0, 0, N, N).data, out = new Float32Array(D);
  for (let i = 0; i < D; i++) out[i] = d[i * 4] / 255;
  return out;
}

export default function init(stage) {
  const k = createKit(stage, { trackPointer: true, label: 'A drawing pad for digits, the 28 by 28 pixel grid and the classifier\'s probabilities' });
  const hud = createHud(stage);
  const badge = hud.badge('Draw a digit from 0 to 9', '#db2777');

  const pad = document.createElement('canvas'); pad.width = pad.height = 280;
  const pg = pad.getContext('2d'); pg.fillStyle = '#000'; pg.fillRect(0, 0, 280, 280);
  const small = document.createElement('canvas'); small.width = small.height = N;
  const sg = small.getContext('2d', { willReadFrequently: true });
  const raw = new Float32Array(D), vec = new Float32Array(D), view = document.createElement('canvas'); view.width = view.height = N;
  const vg = view.getContext('2d'); const vimg = vg.createImageData(N, N);
  const probs = new Float32Array(10), sims = new Float32Array(10), best = new Int16Array(10);
  const templates = [];
  const conf = new Int16Array(100);
  let has = false, brush = 1.6, showNums = true, lastX = -1, lastY = -1, testAcc = 0;

  for (let dgt = 0; dgt < 10; dgt++) for (let f = 0; f < FONTS.length; f++) for (const r of [-0.12, 0.08]) { const v = new Float32Array(D); if (prep(render(dgt, FONTS[f], r, 1, f % 2 ? 1.6 : 0.6), v)) templates.push({ d: dgt, v }); }
  function classify(v, out) {
    sims.fill(-1);
    for (let t = 0; t < templates.length; t++) { const T2 = templates[t].v; let s = 0; for (let i = 0; i < D; i++) s += T2[i] * v[i]; const d = templates[t].d; if (s > sims[d]) { sims[d] = s; best[d] = t; } }
    let mx = -1e9; for (let d = 0; d < 10; d++) mx = Math.max(mx, sims[d]);
    let z = 0; for (let d = 0; d < 10; d++) { out[d] = Math.exp((sims[d] - mx) * 30); z += out[d]; }
    for (let d = 0; d < 10; d++) out[d] /= z;
  }
  // held-out test: other sizes, angles and stroke widths
  (function test() {
    const v = new Float32Array(D), p = new Float32Array(10); let ok = 0, tot = 0;
    for (let dgt = 0; dgt < 10; dgt++) for (let rep = 0; rep < 8; rep++) {
      const f = FONTS[(rep * 3 + dgt) % FONTS.length], rot = (Math.random() - 0.5) * 0.5, sc = 0.8 + Math.random() * 0.35, th = Math.random() * 2.2;
      if (!prep(render(dgt, f, rot, sc, th), v)) continue;
      classify(v, p); let am = 0; for (let d = 1; d < 10; d++) if (p[d] > p[am]) am = d;
      conf[dgt * 10 + am]++; tot++; if (am === dgt) ok++;
    }
    testAcc = ok / Math.max(1, tot);
  })();

  const panel = createPanel(stage, { title: 'Digit classifier' });
  panel.buttonRow([{ label: 'Clear', icon: 'delete', variant: 'ghost', onClick: clear }]);
  panel.slider({ label: 'Pen thickness', min: 0.8, max: 2.6, step: 0.1, value: brush, format: (v) => v.toFixed(1), onChange: (v) => { brush = v; } });
  panel.toggle({ label: 'Show pixel numbers', value: true, onChange: (v) => { showNums = v; k.invalidate(); } });
  const st = panel.stats([{ key: 'guess', label: 'Best guess' }, { key: 'conf', label: 'Confidence' }, { key: 'test', label: 'Accuracy on the test set' }, { key: 'templ', label: 'Templates stored' }]);
  panel.info('To the computer an image is just numbers. This simple classifier compares those numbers with stored examples; modern convolutional networks instead learn small pattern detectors (edges, loops, corners) that work wherever the pattern appears, which is why they are so good at images.');
  st.test.set(`${fmt(testAcc * 100, 0)} %`); st.templ.set(String(templates.length));

  function clear() { pg.fillStyle = '#000'; pg.fillRect(0, 0, 280, 280); has = false; probs.fill(0); update(); k.invalidate(); }
  function update() {
    sg.clearRect(0, 0, N, N); sg.imageSmoothingEnabled = true; sg.drawImage(pad, 0, 0, N, N);
    const d = sg.getImageData(0, 0, N, N).data;
    for (let i = 0; i < D; i++) raw[i] = d[i * 4] / 255;
    for (let i = 0; i < D; i++) { const v = Math.round(raw[i] * 255); vimg.data[i * 4] = vimg.data[i * 4 + 1] = vimg.data[i * 4 + 2] = v; vimg.data[i * 4 + 3] = 255; }
    vg.putImageData(vimg, 0, 0);
    has = prep(raw, vec);
    if (has) classify(vec, probs);
  }

  let ox = 0, oy = 0, ps = 280, gx = 0, gy = 0, gs = 140, bx = 0, by = 0, bw = 0, cmx = 0, cmy = 0, cms = 0;
  k.onResize((w, h) => {
    if (k.small) { ps = Math.min(w * 0.56, h * 0.52); ox = 10; oy = 44; gs = w - ps - 30; gx = ox + ps + 10; gy = oy; bx = 10; by = oy + ps + 18; bw = w - 20; cms = 0; }
    else { ps = Math.min(h - 120, w * 0.36); ox = 20; oy = 50; gs = Math.min(ps * 0.5, w * 0.2); gx = ox + ps + 24; gy = oy; bx = gx; by = gy + gs + 34; bw = w - gx - 20; cms = Math.min(w - gx - gs - 50, gs * 1.1, 190); cmx = gx + gs + 26; cmy = oy; }
  });
  k.drag({
    hit: (x, y) => (x > ox && x < ox + ps && y > oy && y < oy + ps ? 1 : false),
    down: (x, y) => { lastX = x; lastY = y; stroke(x, y); },
    move: (x, y) => stroke(x, y),
    up: () => { lastX = -1; },
    cursor: 'crosshair', cursorActive: 'crosshair',
  });
  function stroke(x, y) {
    const s = 280 / ps, x0 = (lastX - ox) * s, y0 = (lastY - oy) * s, x1 = (x - ox) * s, y1 = (y - oy) * s;
    pg.strokeStyle = '#fff'; pg.lineCap = 'round'; pg.lineJoin = 'round'; pg.lineWidth = brush * 10 * 2;
    pg.beginPath(); pg.moveTo(x0, y0); pg.lineTo(x1, y1); pg.stroke();
    lastX = x; lastY = y; update(); k.invalidate();
  }

  k.frame((ctx, dt, w, h) => {
    ctx.fillStyle = '#f7f8fd'; ctx.fillRect(0, 0, w, h);
    // pad
    card(ctx, ox - 4, oy - 4, ps + 8, ps + 8, 12, '#111827', '#111827');
    ctx.imageSmoothingEnabled = true; ctx.drawImage(pad, ox, oy, ps, ps);
    ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 1; ctx.beginPath(); for (let i = 1; i < N; i++) { const p = ox + i * ps / N; ctx.moveTo(p, oy); ctx.lineTo(p, oy + ps); ctx.moveTo(ox, oy + i * ps / N); ctx.lineTo(ox + ps, oy + i * ps / N); } ctx.stroke();
    if (!has) text(ctx, 'draw here', ox + ps / 2, oy + ps / 2, 'rgba(255,255,255,0.35)', 16, 600, 'center');
    // what the computer sees
    text(ctx, '28 × 28 pixels', gx, gy - 8, T.ink2, 10.5, 700);
    ctx.imageSmoothingEnabled = false; ctx.drawImage(view, gx, gy, gs, gs); ctx.imageSmoothingEnabled = true;
    ctx.strokeStyle = T.line; ctx.strokeRect(gx + 0.5, gy + 0.5, gs, gs);
    if (showNums && k.pointer.inside && k.pointer.x > ox && k.pointer.x < ox + ps && k.pointer.y > oy && k.pointer.y < oy + ps && !k.small) {
      const cx = Math.floor((k.pointer.x - ox) / ps * N), cy = Math.floor((k.pointer.y - oy) / ps * N);
      const mx = clamp(k.pointer.x + 18, 0, w - 170), my = clamp(k.pointer.y + 18, 0, h - 150);
      card(ctx, mx, my, 160, 140, 10);
      for (let j = -2; j <= 2; j++) for (let i = -2; i <= 2; i++) { const xx = cx + i, yy = cy + j; if (xx < 0 || yy < 0 || xx >= N || yy >= N) continue; const v = Math.round(raw[yy * N + xx] * 255); ctx.fillStyle = `rgb(${v},${v},${v})`; ctx.fillRect(mx + 8 + (i + 2) * 29, my + 8 + (j + 2) * 25, 28, 24); text(ctx, String(v), mx + 22 + (i + 2) * 29, my + 24 + (j + 2) * 25, v > 128 ? '#000' : '#fff', 9, 600, 'center'); }
    } else if (showNums && !k.small) text(ctx, 'hover the pad to read the pixel numbers', gx, gy + gs + 16, T.mute, 9.5, 600);
    // probabilities
    let am = 0; for (let d = 1; d < 10; d++) if (probs[d] > probs[am]) am = d;
    const rowH = k.small ? Math.min(18, (h - by - 10) / 10) : Math.min(24, (h - by - 20) / 10);
    for (let d = 0; d < 10; d++) {
      const yy = by + d * rowH;
      text(ctx, String(d), bx, yy + rowH * 0.7, d === am && has ? '#db2777' : T.ink2, 12, 800);
      ctx.fillStyle = T.line2; ctx.beginPath(); ctx.roundRect(bx + 18, yy + 3, bw - 70, rowH - 6, 4); ctx.fill();
      ctx.fillStyle = d === am && has ? '#db2777' : withAlpha('#7c3aed', 0.6); ctx.beginPath(); ctx.roundRect(bx + 18, yy + 3, (bw - 70) * probs[d], rowH - 6, 4); ctx.fill();
      text(ctx, has ? `${fmt(probs[d] * 100, 0)} %` : '', bx + bw - 6, yy + rowH * 0.7, T.ink2, 10, 600, 'right');
    }
    // confusion matrix
    if (cms > 90) {
      text(ctx, 'Confusion matrix (test set)', cmx, cmy - 8, T.ink2, 10.5, 700);
      const c = cms / 10;
      let mx2 = 1; for (let i = 0; i < 100; i++) mx2 = Math.max(mx2, conf[i]);
      for (let r = 0; r < 10; r++) for (let q = 0; q < 10; q++) { const v = conf[r * 10 + q] / mx2; ctx.fillStyle = r === q ? withAlpha('#16a34a', 0.1 + 0.85 * v) : withAlpha('#e5484d', v > 0 ? 0.25 + 0.6 * v : 0.03); ctx.fillRect(cmx + q * c, cmy + r * c, c - 1, c - 1); }
      for (let i = 0; i < 10; i++) { text(ctx, String(i), cmx + i * c + c / 2, cmy + cms + 11, T.mute, 8.5, 600, 'center'); text(ctx, String(i), cmx - 6, cmy + i * c + c * 0.7, T.mute, 8.5, 600, 'right'); }
      text(ctx, 'predicted →', cmx + cms, cmy + cms + 24, T.mute, 9, 600, 'right');
    }
    st.guess.set(has ? String(am) : '—'); st.conf.set(has ? `${fmt(probs[am] * 100, 0)} %` : '—');
    badge.set(has ? `I think it is a ${am} (${fmt(probs[am] * 100, 0)} % sure)` : 'Draw a digit from 0 to 9');
    k.animate(false);
  });

  update();
  k.debug = { pad: () => [ox, oy, ps], probs: () => Array.from(probs).map((p) => Math.round(p * 100)), acc: () => testAcc };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
