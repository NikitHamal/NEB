/**
 * Line of decision — two kinds of points described by two features. Drag the ends of your own
 * line to separate them (its accuracy is counted live), then let a perceptron learn its own line:
 * each step takes one misclassified point and nudges the weights, w ← w + η·y·x, and the weight
 * vector (drawn as an arrow) always stands perpendicular to the line. On data that no straight
 * line can split (XOR) the perceptron never settles.
 */
import { createKit, T, Spring, fmt, clamp, text, pill, withAlpha, card, knob, arrow } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MAXN = 120;

export default function init(stage) {
  const k = createKit(stage, { label: 'Points of two classes, a draggable dividing line and a perceptron' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the ends of the line to split the colours', '#7c3aed');

  const px = new Float64Array(MAXN), py = new Float64Array(MAXN), lab = new Int8Array(MAXN);
  let n = 0, cls = 1, preset = 'sep';
  const mine = { ax: -0.8, ay: -0.6, bx: 0.8, by: 0.5 };
  let w1 = 0.1, w2 = -0.3, b = 0.05, eta = 0.2, steps = 0, epochErr = 0, running = false, cursor = 0, lastPick = -1, pickFlash = 0, sinceErr = 0, acc = 0;
  const show = { w1: new Spring(w1, 120, 16), w2: new Spring(w2, 120, 16), b: new Spring(b, 120, 16) };
  let tick = 0;

  const panel = createPanel(stage, { title: 'Perceptron' });
  panel.chips({ label: 'Data', options: [{ value: 'sep', label: 'Separable' }, { value: 'overlap', label: 'Overlapping' }, { value: 'xor', label: 'XOR' }], value: 'sep', onChange: (v) => { preset = v; makeData(); } });
  panel.chips({ label: 'Tap to add', options: [{ value: '1', label: 'orange', color: '#f08c00' }, { value: '-1', label: 'blue', color: '#2563eb' }], value: '1', onChange: (v) => { cls = +v; } });
  const [runB] = panel.buttonRow([{ label: 'Learn', icon: 'play_arrow', onClick: () => { running = !running; runB.setLabel(running ? 'Pause' : 'Learn'); k.animate(true); } }, { label: 'One step', icon: 'skip_next', variant: 'ghost', onClick: () => { stepOnce(); k.animate(true); } }]);
  panel.button({ label: 'Forget (random weights)', icon: 'refresh', variant: 'ghost', onClick: () => { w1 = Math.random() - 0.5; w2 = Math.random() - 0.5; b = Math.random() * 0.4 - 0.2; steps = 0; sinceErr = 0; k.animate(true); } });
  panel.slider({ label: 'Learning rate η', min: 0.02, max: 1, step: 0.02, value: eta, format: (v) => v.toFixed(2), onChange: (v) => { eta = v; } });
  const st = panel.stats([{ key: 'mine', label: 'Your line' }, { key: 'perc', label: 'Perceptron' }, { key: 'w', label: 'Weights w₁, w₂, b' }, { key: 'steps', label: 'Updates' }]);
  panel.info('The two features are the inputs x₁ and x₂. The perceptron outputs orange when w₁x₁ + w₂x₂ + b > 0 and blue otherwise, so its boundary is the straight line w₁x₁ + w₂x₂ + b = 0.');

  function makeData() {
    n = 0;
    const add = (x, y, c) => { if (n < MAXN) { px[n] = clamp(x, -0.95, 0.95); py[n] = clamp(y, -0.95, 0.95); lab[n] = c; n++; } };
    const g = () => (Math.random() + Math.random() + Math.random() - 1.5) * 0.5;
    for (let i = 0; i < 40; i++) {
      if (preset === 'sep') { add(-0.4 + g(), 0.35 + g(), 1); add(0.4 + g(), -0.35 + g(), -1); }
      else if (preset === 'overlap') { add(-0.2 + g() * 1.6, 0.2 + g() * 1.6, 1); add(0.2 + g() * 1.6, -0.2 + g() * 1.6, -1); }
      else { const x = Math.random() * 1.8 - 0.9, y = Math.random() * 1.8 - 0.9; if (Math.abs(x) > 0.08 && Math.abs(y) > 0.08) add(x, y, x * y > 0 ? 1 : -1); }
    }
    steps = 0; sinceErr = 0; cursor = 0; k.animate(true);
  }
  function predict(i) { return w1 * px[i] + w2 * py[i] + b > 0 ? 1 : -1; }
  function stepOnce() {
    for (let t = 0; t < n; t++) {
      const i = (cursor + t) % n;
      if (predict(i) !== lab[i]) {
        w1 += eta * lab[i] * px[i]; w2 += eta * lab[i] * py[i]; b += eta * lab[i];
        steps++; cursor = (i + 1) % n; lastPick = i; pickFlash = 1; sinceErr = 0;
        return true;
      }
    }
    sinceErr++;
    return false;
  }
  function accLine(f) { if (!n) return 0; let ok = 0; for (let i = 0; i < n; i++) if (f(px[i], py[i]) === lab[i]) ok++; return ok / n; }
  const mineF = (x, y) => ((mine.bx - mine.ax) * (y - mine.ay) - (mine.by - mine.ay) * (x - mine.ax) > 0 ? 1 : -1);

  let bx = 0, by = 0, bs = 100;
  k.onResize((w, h) => { if (k.small) { bs = Math.min(w - 24, h - 70); bx = (w - bs) / 2; by = 46; } else { bs = Math.min(h - 70, w * 0.66); bx = (w - bs) / 2 - 60; by = 46; } });
  const X = (v) => bx + (v + 1) / 2 * bs, Y = (v) => by + (1 - (v + 1) / 2) * bs, IX = (p) => (p - bx) / bs * 2 - 1, IY = (p) => 1 - (p - by) / bs * 2;

  const hA = k.drag({ hit: (x, y, s) => { const d = Math.hypot(x - X(mine.ax), y - Y(mine.ay)); return d < 12 + s ? d : false; }, move: (x, y) => { mine.ax = clamp(IX(x), -1, 1); mine.ay = clamp(IY(y), -1, 1); } });
  const hB = k.drag({ hit: (x, y, s) => { const d = Math.hypot(x - X(mine.bx), y - Y(mine.by)); return d < 12 + s ? d : false; }, move: (x, y) => { mine.bx = clamp(IX(x), -1, 1); mine.by = clamp(IY(y), -1, 1); } });
  let held = -1;
  k.drag({
    hit: (x, y, s) => { let best = false; for (let i = 0; i < n; i++) { const d = Math.hypot(x - X(px[i]), y - Y(py[i])); if (d < 8 + s && (best === false || d < best)) best = d + 1; } return best; },
    down: (x, y) => { let bd = 1e9; for (let i = 0; i < n; i++) { const d = Math.hypot(x - X(px[i]), y - Y(py[i])); if (d < bd) { bd = d; held = i; } } },
    move: (x, y) => { if (held >= 0) { px[held] = clamp(IX(x), -1, 1); py[held] = clamp(IY(y), -1, 1); sinceErr = 0; } },
    up: () => { held = -1; },
  });
  k.onTap((x, y) => { if (x > bx && x < bx + bs && y > by && y < by + bs && n < MAXN) { px[n] = IX(x); py[n] = IY(y); lab[n] = cls; n++; sinceErr = 0; k.invalidate(); } });

  function clipLine(a, bb, c, out) {
    const pts = [];
    if (Math.abs(bb) > 1e-9) { for (const x of [-1, 1]) { const y = -(a * x + c) / bb; if (y >= -1 && y <= 1) pts.push(x, y); } }
    if (Math.abs(a) > 1e-9) { for (const y of [-1, 1]) { const x = -(bb * y + c) / a; if (x >= -1 && x <= 1) pts.push(x, y); } }
    return pts.length >= 4 ? pts : null;
  }

  k.frame((ctx, dt, w, h) => {
    if (running) { tick += dt; while (tick > 0.12) { tick -= 0.12; stepOnce(); } if (sinceErr > 1) { running = false; runB.setLabel('Learn'); } if (steps > 2000) { running = false; runB.setLabel('Learn'); } }
    show.w1.to(w1); show.w2.to(w2); show.b.to(b);
    const anim = show.w1.step(dt) | show.w2.step(dt) | show.b.step(dt);
    pickFlash = Math.max(0, pickFlash - dt * 2);
    ctx.fillStyle = '#f7f8fd'; ctx.fillRect(0, 0, w, h);
    card(ctx, bx - 4, by - 4, bs + 8, bs + 8, 10);
    // perceptron regions
    const W1 = show.w1.x, W2 = show.w2.x, B = show.b.x;
    ctx.save(); ctx.beginPath(); ctx.rect(bx, by, bs, bs); ctx.clip();
    const seg = clipLine(W1, W2, B);
    if (seg) {
      // shade the orange side with a big polygon
      const nx = W1, ny = W2, L = Math.hypot(nx, ny) || 1;
      const mx = (seg[0] + seg[2]) / 2, my = (seg[1] + seg[3]) / 2;
      const dx = seg[2] - seg[0], dy = seg[3] - seg[1];
      ctx.fillStyle = 'rgba(240,140,0,0.10)'; ctx.beginPath();
      ctx.moveTo(X(seg[0] - dx * 3), Y(seg[1] - dy * 3)); ctx.lineTo(X(seg[2] + dx * 3), Y(seg[3] + dy * 3)); ctx.lineTo(X(seg[2] + dx * 3 + nx / L * 6), Y(seg[3] + dy * 3 + ny / L * 6)); ctx.lineTo(X(seg[0] - dx * 3 + nx / L * 6), Y(seg[1] - dy * 3 + ny / L * 6)); ctx.closePath(); ctx.fill();
      ctx.fillStyle = 'rgba(37,99,235,0.08)'; ctx.beginPath();
      ctx.moveTo(X(seg[0] - dx * 3), Y(seg[1] - dy * 3)); ctx.lineTo(X(seg[2] + dx * 3), Y(seg[3] + dy * 3)); ctx.lineTo(X(seg[2] + dx * 3 - nx / L * 6), Y(seg[3] + dy * 3 - ny / L * 6)); ctx.lineTo(X(seg[0] - dx * 3 - nx / L * 6), Y(seg[1] - dy * 3 - ny / L * 6)); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = '#7c3aed'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(X(seg[0]), Y(seg[1])); ctx.lineTo(X(seg[2]), Y(seg[3])); ctx.stroke();
      arrow(ctx, X(mx), Y(my), X(mx + nx / L * 0.22), Y(my + ny / L * 0.22), '#7c3aed', 2.2);
      text(ctx, 'w', X(mx + nx / L * 0.26), Y(my + ny / L * 0.26), '#7c3aed', 12, 800, 'center', 'middle');
    }
    ctx.restore();
    // axes labels
    text(ctx, 'feature x₁ →', bx + bs, by + bs + 18, T.ink2, 10.5, 600, 'right'); text(ctx, 'feature x₂ ↑', bx + 8, by + 16, T.ink2, 10.5, 600);
    // your line
    ctx.setLineDash([7, 5]); ctx.strokeStyle = T.ink; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(X(mine.ax), Y(mine.ay)); ctx.lineTo(X(mine.bx), Y(mine.by)); ctx.stroke(); ctx.setLineDash([]);
    knob(ctx, X(mine.ax), Y(mine.ay), 7, T.ink, k.isHot(hA) ? 1 : 0); knob(ctx, X(mine.bx), Y(mine.by), 7, T.ink, k.isHot(hB) ? 1 : 0);
    // points
    for (let i = 0; i < n; i++) {
      const c = lab[i] > 0 ? '#f08c00' : '#2563eb', wrong = predict(i) !== lab[i];
      if (i === lastPick && pickFlash > 0) { ctx.beginPath(); ctx.arc(X(px[i]), Y(py[i]), 10 + 8 * (1 - pickFlash), 0, Math.PI * 2); ctx.strokeStyle = withAlpha('#7c3aed', pickFlash); ctx.lineWidth = 2; ctx.stroke(); }
      ctx.beginPath(); ctx.arc(X(px[i]), Y(py[i]), 5, 0, Math.PI * 2); ctx.fillStyle = c; ctx.fill(); ctx.strokeStyle = wrong ? '#7c3aed' : '#fff'; ctx.lineWidth = wrong ? 2 : 1.2; ctx.stroke();
    }
    const am = accLine(mineF), ap = accLine((x, y) => (w1 * x + w2 * y + b > 0 ? 1 : -1));
    const amF = Math.max(am, 1 - am);
    if (!k.small) {
      const cx = bx + bs + 20, cw = w - cx - 14;
      if (cw > 120) {
        card(ctx, cx, by, cw, 120, 12);
        text(ctx, 'Accuracy', cx + 12, by + 22, T.ink, 11.5, 700);
        bar(ctx, cx + 12, by + 36, cw - 24, 'your line', amF, T.ink);
        bar(ctx, cx + 12, by + 74, cw - 24, 'perceptron', ap, '#7c3aed');
      }
    }
    st.mine.set(`${fmt(amF * 100, 0)} %`); st.perc.set(`${fmt(ap * 100, 0)} %`); st.w.set(`${fmt(w1, 2)}, ${fmt(w2, 2)}, ${fmt(b, 2)}`); st.steps.set(String(steps));
    badge.set(running ? `Learning… update ${steps}` : ap === 1 && steps ? `Converged after ${steps} updates: every point is on the right side` : preset === 'xor' && steps > 200 ? 'No straight line can split XOR: the perceptron keeps flipping' : 'Drag the ends of the line to split the colours');
    k.animate(running || !!anim || pickFlash > 0 || held >= 0);
  });
  function bar(ctx, x, y, w, label, f, color) { text(ctx, `${label} ${fmt(f * 100, 0)} %`, x, y + 10, T.ink2, 10.5, 600); ctx.fillStyle = T.line2; ctx.beginPath(); ctx.roundRect(x, y + 16, w, 8, 4); ctx.fill(); ctx.fillStyle = color; ctx.beginPath(); ctx.roundRect(x, y + 16, w * f, 8, 4); ctx.fill(); }

  makeData();
  k.debug = { learn: () => { running = true; k.animate(true); }, end: () => [X(mine.bx), Y(mine.by)], acc: () => [accLine(mineF), accLine((x, y) => (w1 * x + w2 * y + b > 0 ? 1 : -1)), steps] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
