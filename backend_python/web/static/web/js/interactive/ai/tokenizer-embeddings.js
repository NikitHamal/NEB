import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 6 – How AI Understands Words
// Shows tokenization + a small hardcoded 2D embedding space
// Includes the classic king - man + woman ≈ queen vector demo

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Word Embeddings', '#6366F1');

  // Hardcoded 2D embeddings (PCA-reduced for demo purposes, accurate clustering)
  const WORDS = {
    // royalty
    king:    [0.85, 0.70],
    queen:   [0.80, 0.55],
    prince:  [0.72, 0.68],
    princess:[0.68, 0.52],
    // gender
    man:     [0.40, 0.75],
    woman:   [0.35, 0.50],
    boy:     [0.30, 0.72],
    girl:    [0.25, 0.48],
    // animals
    cat:     [0.15, 0.20],
    dog:     [0.18, 0.25],
    kitten:  [0.10, 0.18],
    puppy:   [0.14, 0.22],
    // science
    physics: [0.60, 0.10],
    math:    [0.65, 0.08],
    biology: [0.62, 0.14],
    chemistry:[0.66, 0.12],
    // food
    apple:   [0.10, 0.85],
    banana:  [0.12, 0.88],
    orange:  [0.08, 0.82],
    mango:   [0.13, 0.86],
  };

  const WORD_LIST = Object.keys(WORDS);
  const CLUSTERS = {
    Royalty: ['king','queen','prince','princess'],
    'Gender': ['man','woman','boy','girl'],
    Animals: ['cat','dog','kitten','puppy'],
    Science: ['physics','math','biology','chemistry'],
    Food:    ['apple','banana','orange','mango'],
  };
  const CLUSTER_COLORS = {
    Royalty: '#a855f7',
    Gender: '#ec4899',
    Animals: '#10b981',
    Science: '#3b82f6',
    Food: '#f59e0b',
  };

  let selectedWord = 'king';
  let analogyA = 'king', analogyB = 'man', analogyC = 'woman'; // A - B + C ≈ ?
  let showAnalogy = false;
  let tokenText = 'Hello world, AI is amazing!';

  // Tokenization (simple word-piece-like split)
  function tokenize(text) {
    const tokens = [];
    const words = text.split(/\s+/);
    for (const word of words) {
      if (!word) continue;
      // Strip punctuation as separate token
      const match = word.match(/^([^.,!?;:]+)([.,!?;:]*)$/);
      if (match) {
        if (match[1]) tokens.push(match[1]);
        if (match[2]) tokens.push(match[2]);
      } else {
        tokens.push(word);
      }
    }
    return tokens;
  }

  function vecSub(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
  function vecAdd(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
  function cosSim(a, b) {
    const dot = a[0]*b[0] + a[1]*b[1];
    const na = Math.sqrt(a[0]*a[0] + a[1]*a[1]);
    const nb = Math.sqrt(b[0]*b[0] + b[1]*b[1]);
    return dot / (na * nb + 1e-8);
  }

  function findNearest(vec, exclude) {
    let best = -Infinity, bestWord = '';
    for (const [w, e] of Object.entries(WORDS)) {
      if (exclude.includes(w)) continue;
      const sim = cosSim(vec, e);
      if (sim > best) { best = sim; bestWord = w; }
    }
    return { word: bestWord, sim: best };
  }

  const panel = createPanel(stage, { title: 'Embeddings' });
  panel.select({
    label: 'Highlight word',
    options: WORD_LIST.map((w) => ({ value: w, label: w })),
    value: selectedWord,
    onChange: (v) => { selectedWord = v; },
  });
  panel.toggle({
    label: 'Show analogy',
    value: false,
    onChange: (v) => { showAnalogy = v; },
  });
  panel.section('Analogy: A − B + C ≈ ?');
  const [aSelect, bSelect, cSelect] = [
    panel.select({ label: 'A', options: WORD_LIST.map((w) => ({ value: w, label: w })), value: analogyA, onChange: (v) => { analogyA = v; } }),
    panel.select({ label: 'B', options: WORD_LIST.map((w) => ({ value: w, label: w })), value: analogyB, onChange: (v) => { analogyB = v; } }),
    panel.select({ label: 'C', options: WORD_LIST.map((w) => ({ value: w, label: w })), value: analogyC, onChange: (v) => { analogyC = v; } }),
  ];
  panel.divider();
  const analogyOut = panel.readout({ label: 'Result', value: '—' });
  const tokenOut = panel.readout({ label: 'Token count', value: '—' });
  panel.info('Classic analogy: king − man + woman ≈ queen. The math works because similar concepts cluster in embedding space.');

  // Tokens input
  panel.section('Tokenizer demo');
  const tokInfo = panel.info('Text: "' + tokenText + '"');

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);

    // Layout: embedding space takes most of screen; tokenizer strip at bottom
    const tokH = 60;
    const esX = 10, esY = 10;
    const esW = w - 20, esH = h - tokH - 20;

    // Background grid
    ctx.strokeStyle = 'rgba(255,255,255,0.04)'; ctx.lineWidth = 1;
    for (let i = 1; i < 8; i++) {
      ctx.beginPath(); ctx.moveTo(esX + i * esW / 8, esY); ctx.lineTo(esX + i * esW / 8, esY + esH); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(esX, esY + i * esH / 8); ctx.lineTo(esX + esW, esY + i * esH / 8); ctx.stroke();
    }

    // Cluster hulls (convex approximation = tinted bg boxes)
    for (const [clName, words] of Object.entries(CLUSTERS)) {
      const pts = words.map((ww) => WORDS[ww]);
      const xs = pts.map((p) => esX + p[0] * esW);
      const ys = pts.map((p) => esY + (1 - p[1]) * esH);
      const minX = Math.min(...xs) - 16, maxX = Math.max(...xs) + 16;
      const minY = Math.min(...ys) - 16, maxY = Math.max(...ys) + 16;
      ctx.fillStyle = CLUSTER_COLORS[clName] + '18';
      ctx.strokeStyle = CLUSTER_COLORS[clName] + '40';
      ctx.lineWidth = 1.5;
      if (ctx.roundRect) ctx.roundRect(minX, minY, maxX - minX, maxY - minY, 10);
      else ctx.rect(minX, minY, maxX - minX, maxY - minY);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = CLUSTER_COLORS[clName] + 'aa';
      ctx.font = 'bold 10px Poppins,sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(clName, (minX + maxX) / 2, minY + 11);
    }

    // Analogy vectors
    if (showAnalogy) {
      const eA = WORDS[analogyA], eB = WORDS[analogyB], eC = WORDS[analogyC];
      if (eA && eB && eC) {
        const result = vecAdd(vecSub(eA, eB), eC);
        const nearest = findNearest(result, [analogyA, analogyB, analogyC]);
        analogyOut.set(`${analogyA} − ${analogyB} + ${analogyC} ≈ ${nearest.word}`);

        // Draw vectors
        const toS = (e) => ({ x: esX + e[0] * esW, y: esY + (1 - e[1]) * esH });
        const pA = toS(eA), pB = toS(eB), pC = toS(eC);
        const pRes = { x: esX + result[0] * esW, y: esY + (1 - result[1]) * esH };

        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(pA.x, pA.y); ctx.lineTo(pB.x, pB.y); ctx.stroke();
        ctx.strokeStyle = '#22c55e'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(pC.x, pC.y); ctx.lineTo(pRes.x, pRes.y); ctx.stroke();
        ctx.setLineDash([]);

        ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(pA.x, pA.y); ctx.lineTo(pRes.x, pRes.y); ctx.stroke();

        // Result star
        ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 22px serif'; ctx.textAlign = 'center';
        ctx.fillText('★', pRes.x, pRes.y - 8);
        ctx.fillStyle = '#fef3c7'; ctx.font = 'bold 12px Poppins,sans-serif';
        ctx.fillText(nearest.word, pRes.x, pRes.y + 14);
      }
    }

    // Word points
    for (const [ww, emb] of Object.entries(WORDS)) {
      const px = esX + emb[0] * esW;
      const py = esY + (1 - emb[1]) * esH;
      const isSelected = ww === selectedWord;
      const isAnalogy = showAnalogy && [analogyA, analogyB, analogyC].includes(ww);

      ctx.beginPath(); ctx.arc(px, py, isSelected ? 9 : 6, 0, Math.PI * 2);
      // Color by cluster
      let col = '#94a3b8';
      for (const [clName, words] of Object.entries(CLUSTERS)) {
        if (words.includes(ww)) { col = CLUSTER_COLORS[clName]; break; }
      }
      ctx.fillStyle = isSelected ? '#fff' : col;
      ctx.fill();
      if (isSelected || isAnalogy) {
        ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2.5; ctx.stroke();
      }

      // Word label
      ctx.fillStyle = isSelected ? '#fff' : 'rgba(199,212,234,0.75)';
      ctx.font = `${isSelected ? 'bold' : ''} 11px Poppins,sans-serif`;
      ctx.textAlign = 'left';
      ctx.fillText(ww, px + 10, py + 4);
    }

    // Axis labels
    ctx.fillStyle = 'rgba(199,212,234,0.4)'; ctx.font = '10px Poppins,sans-serif';
    ctx.textAlign = 'center'; ctx.fillText('Embedding dimension 1 (e.g. gender)', esX + esW / 2, esY + esH - 4);
    ctx.save(); ctx.translate(esX + 10, esY + esH / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('Embedding dimension 2 (e.g. royalty)', 0, 0); ctx.restore();

    // Tokenizer strip
    const tokens = tokenize(tokenText);
    tokenOut.set(String(tokens.length));
    const tokenColors = ['#6366F1', '#F59E0B', '#10b981', '#ec4899', '#3b82f6', '#f97316', '#8b5cf6'];
    const tstartY = esY + esH + 8;
    ctx.fillStyle = 'rgba(199,212,234,0.7)'; ctx.font = 'bold 11px Poppins,sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('Tokens:', esX, tstartY + 14);
    let tx = esX + 60;
    tokens.forEach((tok, i) => {
      const col = tokenColors[i % tokenColors.length];
      ctx.fillStyle = col + '33';
      const tw = Math.max(ctx.measureText(tok).width + 10, 20);
      if (ctx.roundRect) ctx.roundRect(tx, tstartY + 2, tw, 22, 4);
      else ctx.rect(tx, tstartY + 2, tw, 22);
      ctx.fill();
      ctx.strokeStyle = col; ctx.lineWidth = 1; ctx.stroke();
      ctx.fillStyle = col; ctx.font = '11px monospace'; ctx.textAlign = 'center';
      ctx.fillText(tok, tx + tw / 2, tstartY + 17);
      tx += tw + 4;
      if (tx > w - 20) { tx = esX + 60; }
    });

    badge.set(`${WORD_LIST.length} words in embedding space`);
  });

  sim.start();

  return {
    dispose() { panel.dispose(); hud.dispose(); sim.dispose(); },
  };
}
