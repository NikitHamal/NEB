import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const LESSONS = {
  'what-is-ai': { title: 'Rules vs learning', color: '#4F46E5', slider: 'Training examples' },
  'data-is-the-teacher': { title: 'Dataset quality', color: '#0891B2', slider: 'Bias/noise' },
  'classification-boundaries': { title: 'Classifier metrics', color: '#DC2626', slider: 'Decision threshold' },
  'neural-network-neurons': { title: 'Neural network', color: '#7C3AED', slider: 'Weight strength' },
  'gradient-descent-training': { title: 'Gradient descent', color: '#EA580C', slider: 'Learning rate' },
  'computer-vision-features': { title: 'Vision pipeline', color: '#16A34A', slider: 'Filter sensitivity' },
  'language-tokenization': { title: 'Tokens and embeddings', color: '#2563EB', slider: 'Context window' },
  'attention-transformers': { title: 'Transformer attention', color: '#9333EA', slider: 'Attention focus' },
  'generative-ai-limits': { title: 'Next-token sampling', color: '#DB2777', slider: 'Temperature' },
  'ai-safety-deployment': { title: 'Deployment safety', color: '#0F766E', slider: 'Risk pressure' },
};

const TOKENS = ['Nepal', 'student', 'learns', 'AI', 'with', 'evidence'];
const EMBEDS = [
  ['teacher', 0.18, 0.45, '#60A5FA'],
  ['school', 0.27, 0.58, '#60A5FA'],
  ['student', 0.34, 0.38, '#60A5FA'],
  ['plant', 0.72, 0.34, '#22C55E'],
  ['photosynthesis', 0.82, 0.48, '#22C55E'],
  ['algorithm', 0.56, 0.72, '#A78BFA'],
  ['model', 0.66, 0.66, '#A78BFA'],
  ['Kathmandu', 0.2, 0.76, '#F59E0B'],
];

export default function init(stage, context = {}) {
  const sim = createCanvas2D(stage, { dprCap: 1.5 });
  const lesson = LESSONS[context.lessonSlug] || LESSONS['what-is-ai'];
  const hud = createHud(stage);
  const badge = hud.badge(lesson.title, lesson.color);
  const panel = createPanel(stage, { title: 'AI Lab' });

  let mode = '3d';
  let control = 0.55;
  let animate = true;
  let tick = 0;
  let selected = 0;
  let trainStep = 0;

  panel.select({
    label: 'View',
    options: [{ value: '2d', label: '2D diagram' }, { value: '3d', label: '3D model' }],
    value: mode,
    onChange: (val) => { mode = val; },
  });
  panel.slider({
    label: lesson.slider,
    min: 0,
    max: 100,
    step: 1,
    value: Math.round(control * 100),
    format: (v) => `${v}%`,
    onChange: (val) => { control = val / 100; },
  });
  panel.toggle({
    label: 'Animate',
    value: animate,
    onChange: (val) => { animate = val; },
  });
  panel.divider();
  const readout = panel.readout({ label: 'State', value: 'Ready' });
  panel.button({
    label: 'Step model',
    icon: 'skip_next',
    onClick: () => { trainStep = (trainStep + 1) % 6; selected = (selected + 1) % 6; },
  });
  panel.info('Use the view switch to compare a flat diagram with a spatial model. Tap the stage to inspect the next part.');

  function onDown(e) {
    selected = (selected + 1) % 8;
    trainStep = (trainStep + 1) % 6;
    const p = pointerPos(sim.canvas, e);
    if (p.x < sim.width * 0.5) control = Math.max(0, control - 0.08);
    else control = Math.min(1, control + 0.08);
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);

  function background(ctx, w, h) {
    const g = ctx.createLinearGradient(0, 0, w, h);
    g.addColorStop(0, '#07111f');
    g.addColorStop(0.55, '#0e1f36');
    g.addColorStop(1, '#14213f');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
    ctx.globalAlpha = 0.2;
    ctx.strokeStyle = '#8fb3ff';
    ctx.lineWidth = 1;
    for (let x = -80; x < w + 80; x += 42) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x + h * 0.35, h);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function rr(ctx, x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, r);
    else ctx.rect(x, y, w, h);
  }

  function label(ctx, text, x, y, opts = {}) {
    ctx.fillStyle = opts.color || '#E5EEF9';
    ctx.font = `${opts.weight || 700} ${opts.size || 12}px Poppins, system-ui, sans-serif`;
    ctx.textAlign = opts.align || 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, x, y);
  }

  function pill(ctx, text, x, y, color) {
    ctx.font = '700 11px Poppins, system-ui, sans-serif';
    const width = Math.max(76, ctx.measureText(text).width + 24);
    ctx.fillStyle = color || lesson.color;
    rr(ctx, x - width / 2, y - 15, width, 30, 15);
    ctx.fill();
    label(ctx, text, x, y + 1, { size: 11, color: '#F8FAFC' });
  }

  function project(x, y, z) {
    if (mode === '2d') return { x, y };
    return { x: x + z * 0.45, y: y - z * 0.32 };
  }

  function drawPoint(ctx, x, y, z, color, text) {
    const p = project(x, y, z);
    if (mode === '3d') {
      ctx.fillStyle = 'rgba(0,0,0,0.22)';
      ctx.beginPath();
      ctx.ellipse(p.x + 8, p.y + 12, 15, 5, 0, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 8 + z * 0.01, 0, Math.PI * 2);
    ctx.fill();
    if (text) label(ctx, text, p.x, p.y - 18, { size: 10, color: '#CFE1FF' });
  }

  function drawAxes(ctx, x, y, w, h, z = 0) {
    const a = project(x, y + h, z);
    const b = project(x + w, y + h, z);
    const c = project(x, y, z);
    ctx.strokeStyle = 'rgba(203,213,225,0.52)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(c.x, c.y);
    if (mode === '3d') {
      const d = project(x, y + h, 110);
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(d.x, d.y);
    }
    ctx.stroke();
  }

  function dataPoints() {
    const pts = [];
    const n = 18 + Math.round(control * 22);
    for (let i = 0; i < n; i++) {
      const a = i * 1.618 + 0.5;
      const rx = (Math.sin(a * 2.1) + 1) / 2;
      const ry = (Math.cos(a * 1.7) + 1) / 2;
      const cls = rx + ry + Math.sin(i) * 0.18 > 0.95 + (control - 0.5) * 0.35;
      pts.push({ x: rx, y: ry, cls });
    }
    return pts;
  }

  function drawDataset(ctx, w, h, variant) {
    const bx = w * 0.11;
    const by = h * 0.16;
    const bw = w * 0.72;
    const bh = h * 0.6;
    drawAxes(ctx, bx, by, bw, bh, 0);
    const boundary = bx + bw * (0.36 + control * 0.32);
    ctx.strokeStyle = variant === 'rule' ? '#F97316' : '#A78BFA';
    ctx.lineWidth = 4;
    ctx.beginPath();
    if (variant === 'curve') {
      for (let i = 0; i <= 70; i++) {
        const t = i / 70;
        const x = bx + t * bw;
        const y = by + bh * (0.72 - 0.36 * Math.sin(t * Math.PI + control));
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
    } else {
      ctx.moveTo(boundary, by + 8);
      ctx.lineTo(boundary + bw * 0.2, by + bh - 8);
    }
    ctx.stroke();
    dataPoints().forEach((pt, i) => {
      const z = mode === '3d' ? (pt.cls ? 62 : 16) + Math.sin(tick + i) * 6 : 0;
      drawPoint(ctx, bx + pt.x * bw, by + (1 - pt.y) * bh, z, pt.cls ? '#22C55E' : '#F43F5E');
    });
  }

  function drawRulesVsLearning(ctx, w, h) {
    drawDataset(ctx, w, h, control > 0.52 ? 'curve' : 'rule');
    pill(ctx, 'Rule: exact thresholds', w * 0.28, h * 0.83, '#F97316');
    pill(ctx, 'Learned: fitted boundary', w * 0.66, h * 0.83, '#7C3AED');
    readout.set(control > 0.52 ? 'Model is fitting examples' : 'Rule system is using fixed cutoffs');
  }

  function drawData(ctx, w, h) {
    drawDataset(ctx, w, h, 'curve');
    const bias = Math.round(control * 100);
    pill(ctx, `${bias}% bias/noise`, w * 0.5, h * 0.84, bias > 65 ? '#DC2626' : '#0891B2');
    readout.set(bias > 65 ? 'High bias: test behavior is unreliable' : 'Balanced examples improve generalization');
  }

  function drawClassification(ctx, w, h) {
    drawDataset(ctx, w, h, 'line');
    const m = [
      ['TP', 24 + selected, '#22C55E'],
      ['FP', Math.round(control * 9), '#F97316'],
      ['FN', Math.round((1 - control) * 8), '#EF4444'],
      ['TN', 22, '#38BDF8'],
    ];
    m.forEach((cell, i) => {
      const x = w * 0.67 + (i % 2) * 84;
      const y = h * 0.22 + Math.floor(i / 2) * 72;
      ctx.fillStyle = 'rgba(15,23,42,0.82)';
      rr(ctx, x, y, 72, 54, 10);
      ctx.fill();
      label(ctx, cell[0], x + 36, y + 18, { color: cell[2], size: 13 });
      label(ctx, String(cell[1]), x + 36, y + 39, { color: '#F8FAFC', size: 16 });
    });
    readout.set(`Precision ${Math.round((24 / (24 + m[1][1])) * 100)}%`);
  }

  function drawNetwork(ctx, w, h) {
    const layers = [3, 5, 4, 2];
    const xs = layers.map((_, i) => w * (0.18 + i * 0.21));
    const nodes = [];
    layers.forEach((count, li) => {
      for (let ni = 0; ni < count; ni++) {
        const y = h * 0.2 + (ni + 0.5) * (h * 0.56 / count);
        const z = mode === '3d' ? li * 34 : 0;
        nodes.push({ li, ni, x: xs[li], y, z });
      }
    });
    for (let li = 0; li < layers.length - 1; li++) {
      const a = nodes.filter((n) => n.li === li);
      const b = nodes.filter((n) => n.li === li + 1);
      a.forEach((n1, i) => b.forEach((n2, j) => {
        const p1 = project(n1.x, n1.y, n1.z);
        const p2 = project(n2.x, n2.y, n2.z);
        const active = (i + j + trainStep + li) % 3 === 0;
        ctx.strokeStyle = active ? `rgba(96,165,250,${0.35 + control * 0.5})` : 'rgba(148,163,184,0.16)';
        ctx.lineWidth = active ? 2.5 : 1;
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
      }));
    }
    nodes.forEach((n) => drawPoint(ctx, n.x, n.y, n.z, n.li === 0 ? '#38BDF8' : n.li === 3 ? '#22C55E' : '#A78BFA'));
    pill(ctx, 'inputs', xs[0], h * 0.84, '#38BDF8');
    pill(ctx, 'hidden layers', (xs[1] + xs[2]) / 2, h * 0.84, '#7C3AED');
    pill(ctx, 'output', xs[3], h * 0.84, '#22C55E');
    readout.set(`Weight strength ${(control * 2 - 1).toFixed(2)}`);
  }

  function loss(x, y) {
    return 0.35 + Math.sin(x * 0.024) * 0.15 + Math.cos(y * 0.031) * 0.12 + ((x - 260) ** 2 + (y - 160) ** 2) / 180000;
  }

  function drawGradient(ctx, w, h) {
    const ox = w * 0.14;
    const oy = h * 0.16;
    const sw = w * 0.7;
    const sh = h * 0.58;
    for (let y = 0; y < 16; y++) {
      for (let x = 0; x < 26; x++) {
        const lx = x / 25 * sw;
        const ly = y / 15 * sh;
        const v = loss(lx, ly);
        ctx.fillStyle = `rgba(${Math.round(80 + v * 120)},${Math.round(120 + v * 80)},255,0.34)`;
        const p = project(ox + lx, oy + ly, mode === '3d' ? (1 - v) * 90 : 0);
        ctx.fillRect(p.x, p.y, Math.ceil(sw / 25) + 1, Math.ceil(sh / 15) + 1);
      }
    }
    let px = sw * 0.82;
    let py = sh * 0.18;
    for (let i = 0; i <= trainStep + 2; i++) {
      const lr = 0.04 + control * 0.22;
      px += (sw * 0.42 - px) * lr * 2.4;
      py += (sh * 0.55 - py) * lr * 2;
      drawPoint(ctx, ox + px, oy + py, mode === '3d' ? 80 - i * 7 : 0, i === trainStep + 2 ? '#FDE047' : '#FB923C');
    }
    readout.set(control > 0.78 ? 'Overshoot risk' : control < 0.22 ? 'Slow but stable' : 'Converging');
  }

  function drawVision(ctx, w, h) {
    const sx = w * 0.13;
    const sy = h * 0.18;
    const cell = Math.min(28, w * 0.05);
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
        const bright = Math.sin(i * 0.9 + tick) + Math.cos(j * 0.8) + (i > j ? 0.6 : -0.3);
        ctx.fillStyle = bright > 0.45 ? '#E0F2FE' : bright > -0.25 ? '#38BDF8' : '#0F172A';
        const p = project(sx + i * cell, sy + j * cell, mode === '3d' ? bright * 16 + 30 : 0);
        ctx.fillRect(p.x, p.y, cell - 2, cell - 2);
      }
    }
    label(ctx, 'pixels', sx + cell * 4, sy + cell * 10.2, { color: '#BAE6FD' });
    for (let i = 0; i < 9; i++) {
      const x = w * 0.52 + i * 16;
      const hgt = 40 + Math.abs(Math.sin(i + control * 4)) * 120;
      ctx.fillStyle = i % 2 ? '#22C55E' : '#A78BFA';
      rr(ctx, x, h * 0.62 - hgt, 10, hgt, 5);
      ctx.fill();
    }
    pill(ctx, 'edge map -> feature stack', w * 0.63, h * 0.78, '#16A34A');
    readout.set(`Filter sensitivity ${Math.round(control * 100)}%`);
  }

  function drawLanguage(ctx, w, h) {
    TOKENS.forEach((t, i) => pill(ctx, t, w * 0.16 + i * w * 0.12, h * 0.2 + (i % 2) * 44, i === selected % TOKENS.length ? '#2563EB' : '#334155'));
    const bx = w * 0.12;
    const by = h * 0.42;
    const bw = w * 0.74;
    const bh = h * 0.34;
    drawAxes(ctx, bx, by, bw, bh, 0);
    EMBEDS.forEach((e, i) => {
      const z = mode === '3d' ? Math.sin(i + tick) * 35 + 38 : 0;
      drawPoint(ctx, bx + e[1] * bw, by + (1 - e[2]) * bh, z, e[3], e[0]);
    });
    readout.set(`${TOKENS.length} tokens -> embedding vectors`);
  }

  function drawAttention(ctx, w, h) {
    const cx = w * 0.5;
    const cy = h * 0.44;
    const radius = Math.min(w, h) * 0.27;
    const pts = TOKENS.map((t, i) => {
      const a = -Math.PI / 2 + i / TOKENS.length * Math.PI * 2;
      return { t, x: cx + Math.cos(a) * radius, y: cy + Math.sin(a) * radius, z: mode === '3d' ? i * 16 : 0 };
    });
    pts.forEach((a, i) => pts.forEach((b, j) => {
      if (i === j) return;
      const weight = Math.max(0.05, Math.cos((i - selected) * 0.9) * Math.cos((j - control * 5) * 0.7));
      if (weight < 0.22) return;
      const p1 = project(a.x, a.y, a.z);
      const p2 = project(b.x, b.y, b.z);
      ctx.strokeStyle = `rgba(129,140,248,${Math.min(0.9, weight)})`;
      ctx.lineWidth = 1 + weight * 4;
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();
    }));
    pts.forEach((p, i) => drawPoint(ctx, p.x, p.y, p.z, i === selected % pts.length ? '#FDE047' : '#A78BFA', p.t));
    readout.set(`Token "${pts[selected % pts.length].t}" is querying context`);
  }

  function drawGeneration(ctx, w, h) {
    const words = ['answer', 'maybe', 'source', 'invent', 'verify', 'because'];
    let total = 0;
    const probs = words.map((word, i) => {
      const p = Math.exp((Math.sin(i * 1.7 + control * 4) + (i === 2 ? 0.8 : 0)) / (0.35 + control));
      total += p;
      return { word, p };
    });
    probs.forEach((p, i) => {
      const val = p.p / total;
      const x = w * 0.16 + i * w * 0.115;
      const bar = val * h * 1.7;
      ctx.fillStyle = i === selected % probs.length ? '#FDE047' : '#DB2777';
      rr(ctx, x, h * 0.68 - bar, w * 0.075, bar, 8);
      ctx.fill();
      label(ctx, p.word, x + w * 0.037, h * 0.73, { size: 10, color: '#FCE7F3' });
      label(ctx, `${Math.round(val * 100)}%`, x + w * 0.037, h * 0.68 - bar - 12, { size: 10, color: '#F8FAFC' });
    });
    pill(ctx, control > 0.72 ? 'creative, higher risk' : 'conservative sampling', w * 0.5, h * 0.25, control > 0.72 ? '#DC2626' : '#DB2777');
    readout.set(`Temperature ${control.toFixed(2)}`);
  }

  function drawSafety(ctx, w, h) {
    const checks = [
      ['Privacy', 0.85 - control * 0.25],
      ['Bias tests', 0.78 - Math.abs(control - 0.45) * 0.35],
      ['Citations', 0.62 + (1 - control) * 0.2],
      ['Human review', 0.74 - control * 0.18],
      ['Monitoring', 0.7 + Math.sin(tick) * 0.04],
      ['Rollback', 0.66],
    ];
    let score = 0;
    checks.forEach((c, i) => {
      const x = w * (0.23 + (i % 3) * 0.23);
      const y = h * (0.28 + Math.floor(i / 3) * 0.25);
      const ok = c[1] > 0.62;
      score += c[1];
      ctx.fillStyle = ok ? 'rgba(20,83,45,0.88)' : 'rgba(127,29,29,0.88)';
      rr(ctx, x - 72, y - 40, 144, 80, 14);
      ctx.fill();
      label(ctx, ok ? 'ready' : 'needs work', x, y + 18, { size: 11, color: ok ? '#BBF7D0' : '#FECACA' });
      label(ctx, c[0], x, y - 10, { size: 14, color: '#F8FAFC' });
    });
    score = Math.round(score / checks.length * 100);
    pill(ctx, `readiness ${score}%`, w * 0.5, h * 0.82, score > 70 ? '#0F766E' : '#DC2626');
    readout.set(score > 70 ? 'Deploy with monitoring' : 'Do not launch yet');
  }

  function draw(ctx, dt, w, h) {
    if (animate) tick += dt * 1.4;
    background(ctx, w, h);
    badge.set(`${lesson.title} - ${mode.toUpperCase()}`);
    const slug = context.lessonSlug || 'what-is-ai';
    if (slug === 'what-is-ai') drawRulesVsLearning(ctx, w, h);
    else if (slug === 'data-is-the-teacher') drawData(ctx, w, h);
    else if (slug === 'classification-boundaries') drawClassification(ctx, w, h);
    else if (slug === 'neural-network-neurons') drawNetwork(ctx, w, h);
    else if (slug === 'gradient-descent-training') drawGradient(ctx, w, h);
    else if (slug === 'computer-vision-features') drawVision(ctx, w, h);
    else if (slug === 'language-tokenization') drawLanguage(ctx, w, h);
    else if (slug === 'attention-transformers') drawAttention(ctx, w, h);
    else if (slug === 'generative-ai-limits') drawGeneration(ctx, w, h);
    else drawSafety(ctx, w, h);
  }

  sim.setUpdate(draw);
  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
