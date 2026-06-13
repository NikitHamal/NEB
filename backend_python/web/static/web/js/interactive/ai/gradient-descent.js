import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 3 – Gradient Descent
// Loss landscape: L(w) = (w-2)^2 + 0.3*sin(4*w) + 1  (a bumpy bowl)
// Ball rolls down via: w ← w - lr * dL/dw
// Shows overshoot (high LR), slow convergence (low LR), local minima

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Ready', '#6366F1');

  let lr = 0.1;
  let w = -2.5;   // current parameter value
  let running = false;
  let stepCount = 0;
  let history = []; // { w, loss }
  let animAccum = 0;

  // Loss and gradient
  const W_MIN = -3.5, W_MAX = 5;
  function loss(x) {
    return (x - 2) * (x - 2) + 0.4 * Math.sin(4 * x) + 0.5;
  }
  function dLoss(x) {
    return 2 * (x - 2) + 1.6 * Math.cos(4 * x);
  }

  function startPos(v) {
    w = v;
    history = [{ w, loss: loss(w) }];
    stepCount = 0;
    running = false;
    badge.set('Paused — press Step or Run');
  }

  const panel = createPanel(stage, { title: 'Gradient Descent' });
  panel.slider({
    label: 'Learning rate α',
    min: 0.01, max: 0.8, step: 0.01, value: lr,
    format: (v) => v.toFixed(2),
    onChange: (v) => { lr = v; },
  });
  panel.slider({
    label: 'Start position w',
    min: W_MIN, max: W_MAX - 0.5, step: 0.1, value: w,
    format: (v) => v.toFixed(1),
    onChange: (v) => startPos(v),
  });
  panel.divider();
  const lossOut = panel.readout({ label: 'Current loss L(w)', value: '—' });
  const gradOut = panel.readout({ label: 'Gradient dL/dw', value: '—' });
  const wOut = panel.readout({ label: 'Parameter w', value: w.toFixed(3) });
  const stepOut = panel.readout({ label: 'Steps taken', value: '0' });
  panel.divider();
  const [stepBtn, runBtn, resetBtn] = panel.buttonRow([
    { label: 'Step', icon: 'step_over', onClick: doStep },
    { label: 'Run', icon: 'play_arrow', onClick: toggleRun },
    { label: 'Reset', icon: 'replay', onClick: doReset },
  ]);
  panel.info('High learning rate → overshoot. Low rate → very slow. Try α = 0.5 and start from the left edge.');

  function doStep() {
    const grad = dLoss(w);
    w = w - lr * grad;
    stepCount++;
    history.push({ w, loss: loss(w) });
    if (history.length > 200) history.shift();
  }

  function toggleRun() {
    running = !running;
    runBtn.setLabel(running ? 'Pause' : 'Run');
    badge.set(running ? 'Running…' : 'Paused');
  }

  function doReset() {
    running = false;
    runBtn.setLabel('Run');
    w = -2.5;
    history = [{ w, loss: loss(w) }];
    stepCount = 0;
    badge.set('Reset — choose start position');
  }

  sim.setUpdate((ctx, dt, w_arg, h) => {
    // animation steps
    if (running) {
      animAccum += dt;
      const stepsPerSec = Math.max(1, Math.round(lr * 40 + 2));
      while (animAccum > 1 / stepsPerSec) {
        animAccum -= 1 / stepsPerSec;
        doStep();
        // auto-stop near minimum
        if (Math.abs(dLoss(w)) < 0.005) { running = false; runBtn.setLabel('Run'); badge.set('Converged!'); }
      }
    }

    ctx.clearRect(0, 0, w_arg, h);
    const bg = ctx.createLinearGradient(0, 0, w_arg, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w_arg, h);

    // Layout
    const mL = 55, mR = 20, mT = 30, mB = 55;
    const cw = w_arg - mL - mR;
    const ch = h - mT - mB - 70; // leave room for loss history at bottom
    const lhH = 65;
    const lhY = h - mB - lhH;

    function toScreen(wVal, lVal, lMin, lMax) {
      const sx = mL + (wVal - W_MIN) / (W_MAX - W_MIN) * cw;
      const sy = mT + (1 - (lVal - lMin) / (lMax - lMin)) * ch;
      return { sx, sy };
    }

    // Compute loss curve
    const N = 200;
    const lVals = [];
    for (let i = 0; i <= N; i++) lVals.push(loss(W_MIN + (i / N) * (W_MAX - W_MIN)));
    const lMin = Math.min(...lVals) - 0.1;
    const lMax = Math.max(...lVals) + 0.3;

    // Background region colours by gradient direction
    for (let i = 0; i < N; i++) {
      const wv = W_MIN + (i / N) * (W_MAX - W_MIN);
      const g = dLoss(wv);
      ctx.fillStyle = g < 0 ? 'rgba(99,102,241,0.07)' : 'rgba(245,158,11,0.07)';
      const sx = mL + (i / N) * cw;
      ctx.fillRect(sx, mT, cw / N + 1, ch);
    }

    // Loss curve
    ctx.strokeStyle = '#a5b4fc'; ctx.lineWidth = 2.5; ctx.beginPath();
    for (let i = 0; i <= N; i++) {
      const wv = W_MIN + (i / N) * (W_MAX - W_MIN);
      const lv = loss(wv);
      const { sx, sy } = toScreen(wv, lv, lMin, lMax);
      if (i === 0) ctx.moveTo(sx, sy); else ctx.lineTo(sx, sy);
    }
    ctx.stroke();

    // History path
    if (history.length > 1) {
      ctx.strokeStyle = 'rgba(245,158,11,0.45)'; ctx.lineWidth = 1.5; ctx.setLineDash([3, 3]);
      ctx.beginPath();
      history.forEach(({ w: wh, loss: lh }, i) => {
        const { sx, sy } = toScreen(wh, lh, lMin, lMax);
        if (i === 0) ctx.moveTo(sx, sy); else ctx.lineTo(sx, sy);
      });
      ctx.stroke(); ctx.setLineDash([]);
    }

    // Gradient arrow at current position
    const curLoss = loss(w);
    const curGrad = dLoss(w);
    const { sx: bx, sy: by } = toScreen(w, curLoss, lMin, lMax);
    const arrowLen = Math.min(Math.abs(curGrad) * 30, 60);
    if (Math.abs(curGrad) > 0.01) {
      ctx.strokeStyle = '#f97316'; ctx.lineWidth = 2; ctx.fillStyle = '#f97316';
      ctx.beginPath(); ctx.moveTo(bx, by);
      const ex = bx + Math.sign(curGrad) * arrowLen;
      ctx.lineTo(ex, by);
      ctx.stroke();
      // arrowhead
      ctx.beginPath(); ctx.moveTo(ex, by);
      ctx.lineTo(ex - Math.sign(curGrad) * 8, by - 5);
      ctx.lineTo(ex - Math.sign(curGrad) * 8, by + 5);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#fed7aa'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('gradient', Math.min(bx, ex) + 4, by - 7);
    }

    // Ball (current position)
    const grad2 = ctx.createRadialGradient(bx - 3, by - 4, 2, bx, by, 12);
    grad2.addColorStop(0, '#fbbf24'); grad2.addColorStop(1, '#d97706');
    ctx.beginPath(); ctx.arc(bx, by, 12, 0, Math.PI * 2);
    ctx.fillStyle = grad2; ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)'; ctx.lineWidth = 1.5; ctx.stroke();

    // Axes
    ctx.strokeStyle = 'rgba(165,180,252,0.5)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(mL, mT); ctx.lineTo(mL, mT + ch); ctx.lineTo(mL + cw, mT + ch); ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.7)'; ctx.font = '11px Poppins,sans-serif';
    ctx.textAlign = 'center'; ctx.fillText('Parameter w', mL + cw / 2, mT + ch + 18);
    ctx.save(); ctx.translate(14, mT + ch / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('Loss L(w)', 0, 0); ctx.restore();
    // x-axis ticks
    [-3, -2, -1, 0, 1, 2, 3, 4].forEach((v) => {
      if (v < W_MIN || v > W_MAX) return;
      const sx = mL + (v - W_MIN) / (W_MAX - W_MIN) * cw;
      ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '10px monospace'; ctx.textAlign = 'center';
      ctx.fillText(v, sx, mT + ch + 30);
    });
    // y ticks
    [1, 2, 3, 4, 5].forEach((v) => {
      if (v < lMin || v > lMax) return;
      const sy = mT + (1 - (v - lMin) / (lMax - lMin)) * ch;
      ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '10px monospace'; ctx.textAlign = 'right';
      ctx.fillText(v, mL - 4, sy + 3);
    });

    // Loss history plot
    ctx.fillStyle = 'rgba(8,16,30,0.6)';
    if (ctx.roundRect) ctx.roundRect(mL, lhY, cw, lhH - 5, 6);
    else ctx.rect(mL, lhY, cw, lhH - 5);
    ctx.fill();
    ctx.strokeStyle = 'rgba(165,180,252,0.25)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '10px Poppins,sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('Loss over steps', mL + 6, lhY + 13);
    if (history.length > 1) {
      const lMin2 = Math.min(...history.map((x) => x.loss));
      const lMax2 = Math.max(...history.map((x) => x.loss)) + 0.1;
      ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2; ctx.beginPath();
      history.forEach(({ loss: lv }, i) => {
        const hx = mL + (i / (history.length - 1)) * cw;
        const hy = lhY + (1 - (lv - lMin2) / (lMax2 - lMin2)) * (lhH - 22) + 4;
        if (i === 0) ctx.moveTo(hx, hy); else ctx.lineTo(hx, hy);
      });
      ctx.stroke();
    }

    lossOut.set(curLoss.toFixed(4));
    gradOut.set(curGrad.toFixed(4));
    wOut.set(w.toFixed(4));
    stepOut.set(String(stepCount));
  });

  startPos(w);
  sim.start();

  return {
    dispose() { panel.dispose(); hud.dispose(); sim.dispose(); },
  };
}
