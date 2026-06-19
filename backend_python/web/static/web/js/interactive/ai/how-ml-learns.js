import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { panelBg, labelText } from '../biology/bio-utils.js';

// A tiny 2-layer network learns to fit y = sin(x) on [-π, π].
// 1 hidden layer of N tanh units, linear output. Trained by plain gradient descent on MSE.

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const lossBadge = hud.badge('Loss: —', '#f87171');
  const epochBadge = hud.badge('Epoch 0', '#a3e635');

  const XMIN = -Math.PI; const XMAX = Math.PI;
  // training samples
  const N = 24;
  const xs = []; const ys = [];
  for (let i = 0; i < N; i++) {
    const x = XMIN + (i / (N - 1)) * (XMAX - XMIN);
    xs.push(x); ys.push(Math.sin(x));
  }

  let hidden = 8;
  let learningRate = 0.05;
  let epoch = 0;
  let loss = 0;
  let training = false;

  // network params: W1[h][1], b1[h], W2[1][h], b2
  let W1, b1, W2, b2;
  function initNet() {
    W1 = []; b1 = []; W2 = [];
    for (let h = 0; h < hidden; h++) {
      W1.push((Math.random() * 2 - 1)); b1.push((Math.random() * 2 - 1) * 0.3);
      W2.push((Math.random() * 2 - 1));
    }
    b2 = (Math.random() * 2 - 1) * 0.3;
    epoch = 0; loss = 0;
  }
  initNet();

  function forward(x) {
    const a = [];
    for (let h = 0; h < hidden; h++) {
      a.push(Math.tanh(W1[h] * x + b1[h]));
    }
    let y = b2;
    for (let h = 0; h < hidden; h++) y += W2[h] * a[h];
    return { y, a };
  }

  function trainBatch() {
    // one full gradient descent step over all samples
    const gW1 = new Array(hidden).fill(0);
    const gb1 = new Array(hidden).fill(0);
    const gW2 = new Array(hidden).fill(0);
    let gb2 = 0;
    let totalLoss = 0;
    for (let i = 0; i < N; i++) {
      const x = xs[i]; const t = ys[i];
      const { y, a } = forward(x);
      const err = y - t;
      totalLoss += err * err;
      // dL/dy = 2*err
      const dy = 2 * err;
      gb2 += dy;
      for (let h = 0; h < hidden; h++) {
        gW2[h] += dy * a[h];
        // backprop through tanh: da = (1 - a²)
        const da = dy * W2[h] * (1 - a[h] * a[h]);
        gW1[h] += da * x;
        gb1[h] += da;
      }
    }
    const lr = learningRate / N;
    for (let h = 0; h < hidden; h++) {
      W1[h] -= lr * gW1[h]; b1[h] -= lr * gb1[h]; W2[h] -= lr * gW2[h];
    }
    b2 -= lr * gb2;
    loss = totalLoss / N;
    epoch++;
  }

  const panel = createPanel(stage, { title: 'How Machines Learn' });
  panel.info('A tiny network is trying to learn the curve y = sin(x). Press Train to run gradient descent — watch the loss fall and the prediction (green) creep towards the truth (white).');
  const trainBtn = panel.button({ label: 'Train 1 step', icon: 'play_arrow', onClick: () => { trainBatch(); } });
  panel.button({ label: 'Train 100 steps', icon: 'fast_forward', onClick: () => { for (let i = 0; i < 100; i++) trainBatch(); } });
  panel.toggle({ label: 'Auto-train', value: false, onChange: (v) => { training = v; } });
  panel.divider();
  panel.slider({
    label: 'Learning rate', min: 1, max: 50, step: 1, value: 5,
    format: (v) => (v / 100).toFixed(2),
    onChange: (v) => { learningRate = v / 100; },
  });
  panel.select({
    label: 'Hidden units (complexity)', value: '8',
    options: [{ value: '2', label: '2 (too simple)' }, { value: '8', label: '8 (balanced)' }, { value: '32', label: '32 (may overfit)' }],
    onChange: (v) => { hidden = parseInt(v, 10); initNet(); },
  });
  panel.button({ label: 'Reset network', icon: 'refresh', variant: 'ghost', onClick: () => { initNet(); } });
  panel.divider();
  const lossOut = panel.readout({ label: 'Loss (MSE)', value: '—' });
  const epochOut = panel.readout({ label: 'Epoch', value: '0' });
  panel.button({ label: 'What is gradient descent?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Gradient descent',
      body: 'Imagine you are blindfolded on a hilly landscape trying to reach the lowest valley. You feel the slope under your feet and take a step downhill. The model does the same: it computes the slope of the loss with respect to each weight, then nudges the weight a small step (the learning rate) downhill.',
      color: '#6366F1',
    });
  } });

  // loss history for the sparkline
  const lossHist = [];

  let acc = 0;
  sim.setUpdate((ctx, dt) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#070a14'; ctx.fillRect(0, 0, w, h);

    if (training) {
      acc += dt;
      while (acc > 0.03) { trainBatch(); acc -= 0.03; }
    }

    // Plot area
    const padL = 50; const padR = 20; const padT = 20; const padB = 40;
    const px = padL; const py = padT; const pw = w - padL - padR; const ph = h - padT - padB - 120;
    panelBg(ctx, px, py, pw, ph);
    // axes
    ctx.strokeStyle = 'rgba(199,212,234,0.3)'; ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(px + pw / 2, py + 4); ctx.lineTo(px + pw / 2, py + ph - 4);
    ctx.moveTo(px + 8, py + ph / 2); ctx.lineTo(px + pw - 8, py + ph / 2);
    ctx.stroke();
    labelText(ctx, 'y', px + pw / 2 + 6, py + 14, { color: '#9ec1ff', size: 11 });
    labelText(ctx, 'x', px + pw - 14, py + ph / 2 - 6, { color: '#9ec1ff', size: 11 });
    labelText(ctx, '−π', px + 4, py + ph / 2 - 4, { color: '#94a3b8', size: 10 });
    labelText(ctx, '+π', px + pw - 22, py + ph / 2 - 4, { color: '#94a3b8', size: 10 });

    const xToPx = (x) => px + ((x - XMIN) / (XMAX - XMIN)) * pw;
    const yToPx = (y) => py + ph / 2 - y * (ph / 2 - 8);

    // truth curve
    ctx.strokeStyle = 'rgba(255,255,255,0.8)'; ctx.lineWidth = 2;
    ctx.beginPath();
    for (let i = 0; i <= 80; i++) {
      const x = XMIN + (i / 80) * (XMAX - XMIN);
      const X = xToPx(x); const Y = yToPx(Math.sin(x));
      if (i === 0) ctx.moveTo(X, Y); else ctx.lineTo(X, Y);
    }
    ctx.stroke();

    // prediction curve
    ctx.strokeStyle = '#34d399'; ctx.lineWidth = 2;
    ctx.beginPath();
    for (let i = 0; i <= 80; i++) {
      const x = XMIN + (i / 80) * (XMAX - XMIN);
      const X = xToPx(x); const Y = yToPx(forward(x).y);
      if (i === 0) ctx.moveTo(X, Y); else ctx.lineTo(X, Y);
    }
    ctx.stroke();

    // data points
    ctx.fillStyle = '#60a5fa';
    xs.forEach((x, i) => {
      ctx.beginPath(); ctx.arc(xToPx(x), yToPx(ys[i]), 3, 0, Math.PI * 2); ctx.fill();
    });

    // legend
    labelText(ctx, '● truth (sin)', px + 10, py + ph + 16, { color: '#fff', size: 11 });
    labelText(ctx, '— model prediction', px + 110, py + ph + 16, { color: '#34d399', size: 11 });
    labelText(ctx, '● training data', px + 260, py + ph + 16, { color: '#60a5fa', size: 11 });

    // loss sparkline at bottom
    if (epoch % 5 === 0 || lossHist.length === 0) { lossHist.push(loss); if (lossHist.length > 200) lossHist.shift(); }
    const sx = px; const sy = py + ph + 40; const sw = pw; const sh = 60;
    panelBg(ctx, sx, sy, sw, sh);
    labelText(ctx, 'Loss over time', sx + 8, sy + 14, { color: '#9ec1ff', size: 11 });
    const maxL = Math.max(0.01, ...lossHist);
    ctx.strokeStyle = '#f87171'; ctx.lineWidth = 2;
    ctx.beginPath();
    lossHist.forEach((l, i) => {
      const X = sx + (i / Math.max(1, lossHist.length - 1)) * (sw - 16) + 8;
      const Y = sy + sh - 10 - (l / maxL) * (sh - 24);
      if (i === 0) ctx.moveTo(X, Y); else ctx.lineTo(X, Y);
    });
    ctx.stroke();

    lossBadge.set(`Loss: ${loss.toFixed(4)}`);
    epochBadge.set(`Epoch ${epoch}`);
    lossOut.set(loss.toFixed(4));
    epochOut.set(String(epoch));
  });

  sim.start();

  return {
    dispose() { panel.dispose(); hud.dispose(); sim.dispose(); },
  };
}
