import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 4 – Neural Network Playground
// Architecture: 2 inputs → [H neurons] hidden → 1 output (sigmoid)
// Dataset: spiral / XOR / circle  (2D classification)
// Training: full forward+backprop, SGD mini-batch

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Untrained', '#6366F1');

  // Hyper-params
  let hiddenN = 4;
  let lr = 0.05;
  let dataset = 'xor';
  let training = false;
  let epoch = 0;
  let loss = 1.0;

  // Network weights (2→H→1)
  let W1, b1, W2, b2; // H×2, H, 1×H, 1
  // Train button handle — assigned once the control panel is built below, but
  // initWeights() may run earlier, so it is declared here and null-guarded.
  let runBtn = null;

  function sigmoid(z) { return 1 / (1 + Math.exp(-Math.max(-20, Math.min(20, z)))); }
  function sigmoidD(a) { return a * (1 - a); }
  function relu(z) { return Math.max(0, z); }
  function reluD(a) { return a > 0 ? 1 : 0; }

  function initWeights() {
    W1 = []; b1 = [];
    for (let i = 0; i < hiddenN; i++) {
      W1.push([randn() * 0.8, randn() * 0.8]);
      b1.push(0);
    }
    W2 = []; b2 = [0];
    for (let i = 0; i < hiddenN; i++) W2.push(randn() * 0.8);
    epoch = 0; loss = 1.0; training = false;
    if (runBtn) runBtn.setLabel('Train');
    badge.set('Weights reset');
  }

  function randn() {
    const u = 1 - Math.random(), v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  // Forward pass: returns { h, a1, out }
  function forward(x1, x2) {
    const z1 = W1.map((w, i) => w[0] * x1 + w[1] * x2 + b1[i]);
    const a1 = z1.map(relu);
    const z2 = W2.reduce((s, w, i) => s + w * a1[i], b2[0]);
    const out = sigmoid(z2);
    return { a1, out };
  }

  // Backprop + update for one sample
  function trainSample(x1, x2, y) {
    const { a1, out } = forward(x1, x2);
    const dOut = out - y; // dL/dz2
    // W2 gradients
    for (let i = 0; i < hiddenN; i++) {
      W2[i] -= lr * dOut * a1[i];
    }
    b2[0] -= lr * dOut;
    // Hidden layer gradients
    for (let i = 0; i < hiddenN; i++) {
      const dA1 = dOut * W2[i] * reluD(a1[i]);
      W1[i][0] -= lr * dA1 * x1;
      W1[i][1] -= lr * dA1 * x2;
      b1[i] -= lr * dA1;
    }
    return -y * Math.log(out + 1e-8) - (1 - y) * Math.log(1 - out + 1e-8);
  }

  // Datasets
  function makeData(type, n) {
    const pts = [];
    if (type === 'xor') {
      for (let i = 0; i < n; i++) {
        const x1 = Math.random() * 2 - 1, x2 = Math.random() * 2 - 1;
        const y = (x1 * x2 > 0) ? 1 : 0;
        pts.push({ x1, x2, y });
      }
    } else if (type === 'circle') {
      for (let i = 0; i < n; i++) {
        const x1 = Math.random() * 2 - 1, x2 = Math.random() * 2 - 1;
        const r = Math.sqrt(x1 * x1 + x2 * x2);
        pts.push({ x1, x2, y: r < 0.6 ? 1 : 0 });
      }
    } else { // spiral
      const half = Math.floor(n / 2);
      for (let i = 0; i < half; i++) {
        const t = (i / half) * 3 * Math.PI;
        const r = 0.1 + 0.45 * i / half;
        pts.push({ x1: r * Math.cos(t), x2: r * Math.sin(t), y: 0 });
        pts.push({ x1: r * Math.cos(t + Math.PI), x2: r * Math.sin(t + Math.PI), y: 1 });
      }
    }
    return pts;
  }

  let data = makeData(dataset, 120);
  initWeights();

  const panel = createPanel(stage, { title: 'Network Controls' });
  panel.select({
    label: 'Dataset',
    options: [
      { value: 'xor', label: 'XOR' },
      { value: 'circle', label: 'Circle' },
      { value: 'spiral', label: 'Spiral' },
    ],
    value: dataset,
    onChange: (v) => { dataset = v; data = makeData(v, 120); initWeights(); },
  });
  panel.slider({
    label: 'Hidden neurons',
    min: 2, max: 8, step: 1, value: hiddenN,
    format: (v) => `${v}`,
    onChange: (v) => { hiddenN = v; initWeights(); },
  });
  panel.slider({
    label: 'Learning rate',
    min: 0.005, max: 0.3, step: 0.005, value: lr,
    format: (v) => v.toFixed(3),
    onChange: (v) => { lr = v; },
  });
  panel.divider();
  const epochOut = panel.readout({ label: 'Epoch', value: '0' });
  const lossOut = panel.readout({ label: 'Loss', value: '—' });
  panel.divider();
  let resetBtn;
  [runBtn, resetBtn] = panel.buttonRow([
    { label: 'Train', icon: 'play_arrow', onClick: toggleTrain },
    { label: 'Reset', icon: 'replay', onClick: initWeights },
  ]);
  panel.info('Press Train to watch the network learn. Try XOR first — simple networks struggle, but 4+ neurons crack it.');

  function toggleTrain() {
    training = !training;
    runBtn.setLabel(training ? 'Pause' : 'Train');
    badge.set(training ? 'Training…' : 'Paused');
  }

  const GRID = 28; // decision boundary grid resolution
  let bgGrid = new Float32Array(GRID * GRID);
  let bgDirty = true;

  function trainEpoch() {
    // shuffle
    for (let i = data.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [data[i], data[j]] = [data[j], data[i]];
    }
    let totalLoss = 0;
    for (const { x1, x2, y } of data) totalLoss += trainSample(x1, x2, y);
    loss = totalLoss / data.length;
    epoch++;
    bgDirty = true;
  }

  function buildBg() {
    for (let gy = 0; gy < GRID; gy++) {
      for (let gx = 0; gx < GRID; gx++) {
        const x1 = (gx / GRID) * 2 - 1;
        const x2 = ((GRID - 1 - gy) / GRID) * 2 - 1;
        bgGrid[gy * GRID + gx] = forward(x1, x2).out;
      }
    }
    bgDirty = false;
  }

  let trainAccum = 0;

  function drawNetworkDiagram(ctx, w, h, cw2, ch2, cx, cy) {
    // Draw network topology on right side
    const nx = cx, ny = cy;
    const layerX = [nx + 20, nx + 70, nx + 120, nx + 170];
    const layers = [2, hiddenN, 1];
    const maxN = Math.max(...layers);
    const nodeR = 10;
    const layerH = Math.min(ch2 * 0.6, 180);

    function nodePos(li, ni) {
      const count = layers[li];
      const spacing = count > 1 ? layerH / (count - 1) : 0;
      const startY = ny + ch2 / 2 - layerH / 2 + (count > 1 ? ni * spacing : layerH / 2);
      return { x: layerX[li], y: startY };
    }

    // Connections (weight strength as opacity)
    for (let i = 0; i < hiddenN; i++) {
      const src = nodePos(0, 0), src2 = nodePos(0, 1);
      const dst = nodePos(1, i);
      const mag = Math.min(1, Math.abs(W1[i][0]) / 2);
      ctx.strokeStyle = W1[i][0] > 0 ? `rgba(99,102,241,${0.2 + mag * 0.6})` : `rgba(245,158,11,${0.2 + mag * 0.6})`;
      ctx.lineWidth = 1 + mag * 1.5;
      ctx.beginPath(); ctx.moveTo(src.x, src.y); ctx.lineTo(dst.x, dst.y); ctx.stroke();
      const mag2 = Math.min(1, Math.abs(W1[i][1]) / 2);
      ctx.strokeStyle = W1[i][1] > 0 ? `rgba(99,102,241,${0.2 + mag2 * 0.6})` : `rgba(245,158,11,${0.2 + mag2 * 0.6})`;
      ctx.lineWidth = 1 + mag2 * 1.5;
      ctx.beginPath(); ctx.moveTo(src2.x, src2.y); ctx.lineTo(dst.x, dst.y); ctx.stroke();
      // to output
      const dst2 = nodePos(2, 0);
      const mag3 = Math.min(1, Math.abs(W2[i]) / 2);
      ctx.strokeStyle = W2[i] > 0 ? `rgba(99,102,241,${0.2 + mag3 * 0.6})` : `rgba(245,158,11,${0.2 + mag3 * 0.6})`;
      ctx.lineWidth = 1 + mag3 * 1.5;
      ctx.beginPath(); ctx.moveTo(dst.x, dst.y); ctx.lineTo(dst2.x, dst2.y); ctx.stroke();
    }

    // Nodes
    layers.forEach((count, li) => {
      for (let ni = 0; ni < count; ni++) {
        const { x, y } = nodePos(li, ni);
        const activation = li === 1 ? 0.5 : li === 0 ? 0.5 : forward(0, 0).out;
        ctx.beginPath(); ctx.arc(x, y, nodeR, 0, Math.PI * 2);
        ctx.fillStyle = li === 2 ? (forward(0, 0).out > 0.5 ? '#F59E0B' : '#6366F1') : `hsl(${220 + activation * 60},70%,55%)`;
        ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.5)'; ctx.lineWidth = 1.5; ctx.stroke();
        ctx.fillStyle = '#fff'; ctx.font = '9px Poppins,sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(li === 0 ? (ni === 0 ? 'x₁' : 'x₂') : li === 2 ? 'ŷ' : 'h', x, y + 3);
      }
    });

    // Layer labels
    ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '9px Poppins,sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('Input', layerX[0], ny + 14);
    ctx.fillText('Hidden', layerX[1], ny + 14);
    ctx.fillText('Output', layerX[2], ny + 14);
  }

  sim.setUpdate((ctx, dt, w, h) => {
    if (training) {
      trainAccum += dt;
      const rate = Math.max(1, Math.round(lr * 100 + 5));
      while (trainAccum > 0.016) {
        trainAccum -= 0.016;
        for (let r = 0; r < rate; r++) trainEpoch();
        if (epoch > 5000) { training = false; runBtn.setLabel('Train'); badge.set('Done!'); break; }
      }
    }
    if (bgDirty) buildBg();

    ctx.clearRect(0, 0, w, h);
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);

    // Feature space (left portion)
    const fsX = 10, fsY = 10;
    const fsSize = Math.min(h - 20, w * 0.55, 320);
    const cellSize = fsSize / GRID;

    // Decision boundary heatmap
    for (let gy = 0; gy < GRID; gy++) {
      for (let gx = 0; gx < GRID; gx++) {
        const val = bgGrid[gy * GRID + gx];
        const r = Math.round(val * 245 + (1 - val) * 99);
        const g2 = Math.round(val * 158 + (1 - val) * 102);
        const b2 = Math.round(val * 11 + (1 - val) * 241);
        ctx.fillStyle = `rgba(${r},${g2},${b2},0.35)`;
        ctx.fillRect(fsX + gx * cellSize, fsY + gy * cellSize, cellSize + 0.5, cellSize + 0.5);
      }
    }

    // Border
    ctx.strokeStyle = 'rgba(165,180,252,0.4)'; ctx.lineWidth = 1.5;
    ctx.strokeRect(fsX, fsY, fsSize, fsSize);

    // Data points
    for (const { x1, x2, y } of data) {
      const px = fsX + (x1 + 1) / 2 * fsSize;
      const py = fsY + (1 - (x2 + 1) / 2) * fsSize;
      ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2);
      ctx.fillStyle = y === 1 ? '#F59E0B' : '#6366F1';
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 1; ctx.stroke();
    }

    // Axis labels
    ctx.fillStyle = 'rgba(199,212,234,0.6)'; ctx.font = '10px Poppins,sans-serif';
    ctx.textAlign = 'center'; ctx.fillText('x₁', fsX + fsSize / 2, fsY + fsSize + 14);
    ctx.save(); ctx.translate(fsX - 14, fsY + fsSize / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('x₂', 0, 0); ctx.restore();

    // Network diagram
    const netX = fsX + fsSize + 20, netW = w - netX - 10;
    drawNetworkDiagram(ctx, w, h, netW, h, netX, 0);

    // Loss curve (bottom right)
    epochOut.set(String(epoch));
    lossOut.set(loss.toFixed(4));
    badge.set(training ? `Training… epoch ${epoch}` : epoch === 0 ? 'Untrained' : `Loss = ${loss.toFixed(4)}`);
  });

  sim.start();

  return {
    dispose() { panel.dispose(); hud.dispose(); sim.dispose(); },
  };
}
