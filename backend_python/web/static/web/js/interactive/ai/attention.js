import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 7 – Attention & Transformers
// Demonstrates self-attention matrix: for each query token, attention weights
// are softmax(QK^T / sqrt(d)) applied to values.
// Uses simple fixed/procedural Q,K,V projections to show interpretable patterns.

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Self-Attention', '#6366F1');

  // Predefined sentences
  const SENTENCES = [
    'The cat sat on the mat',
    'She gave him the book that she liked',
    'The robot learned to walk by itself',
    'AI reads every word and weighs them',
    'John said that he was tired',
  ];

  let sentIdx = 0;
  let selectedToken = 0;

  function getSentence() { return SENTENCES[sentIdx]; }
  function getTokens() { return getSentence().split(' '); }

  // Simple deterministic pseudo-embeddings based on token string hash
  function hashEmbed(word, dim, seed) {
    let h = seed * 1000003;
    for (let i = 0; i < word.length; i++) h = (h * 31 + word.charCodeAt(i)) | 0;
    const results = [];
    for (let d = 0; d < dim; d++) {
      h = (h * 1664525 + 1013904223) | 0;
      results.push(((h & 0xffff) / 0xffff) * 2 - 1);
    }
    return results;
  }

  const DIM = 8;

  function dot(a, b) { return a.reduce((s, v, i) => s + v * b[i], 0); }
  function norm(a) { return Math.sqrt(a.reduce((s, v) => s + v * v, 0)); }
  function softmax(arr) {
    const mx = Math.max(...arr);
    const exps = arr.map((v) => Math.exp(v - mx));
    const sum = exps.reduce((s, v) => s + v, 0);
    return exps.map((v) => v / sum);
  }

  function computeAttention(tokens) {
    // Q, K, V projections: unique per layer seed
    const Q = tokens.map((t) => hashEmbed(t.toLowerCase(), DIM, 42));
    const K = tokens.map((t) => hashEmbed(t.toLowerCase(), DIM, 137));
    const V = tokens.map((t) => hashEmbed(t.toLowerCase(), DIM, 711));

    const N = tokens.length;
    const scale = Math.sqrt(DIM);

    // Attention matrix A[i][j] = softmax(Q[i] · K[j] / sqrt(d))[j]
    const A = [];
    for (let i = 0; i < N; i++) {
      const scores = K.map((k) => dot(Q[i], k) / scale);
      A.push(softmax(scores));
    }
    return { A, Q, K, V };
  }

  // Next-token prediction: crude language model based on context vector
  function predictNext(tokens, attn) {
    const VOCAB = ['the','a','is','was','and','to','it','that','with','on','by','in',
      'cat','dog','book','robot','man','woman','he','she','they','I',
      'happy','sad','big','small','fast','slow','runs','walks','learns','loves'];
    // Context vector = weighted average of value embeddings
    const N = tokens.length;
    const { A, V } = attn;
    const lastRow = A[N - 1];
    const ctx = new Array(DIM).fill(0);
    for (let j = 0; j < N; j++) {
      for (let d = 0; d < DIM; d++) ctx[d] += lastRow[j] * V[j][d];
    }
    // Score each vocab word by cosine similarity to context
    const scores = VOCAB.map((w) => {
      const we = hashEmbed(w, DIM, 99);
      return { w, s: dot(ctx, we) / (norm(ctx) * norm(we) + 1e-8) };
    });
    scores.sort((a, b) => b.s - a.s);
    return scores.slice(0, 5);
  }

  const panel = createPanel(stage, { title: 'Attention Controls' });
  const sentSelect = panel.select({
    label: 'Sentence',
    options: SENTENCES.map((s, i) => ({ value: String(i), label: s.slice(0, 28) + (s.length > 28 ? '…' : '') })),
    value: '0',
    onChange: (v) => { sentIdx = parseInt(v); selectedToken = 0; },
  });
  panel.divider();
  const tokenSelect = panel.select({
    label: 'Query token',
    options: getTokens().map((t, i) => ({ value: String(i), label: `${i}: "${t}"` })),
    value: '0',
    onChange: (v) => { selectedToken = parseInt(v); },
  });
  panel.divider();
  const headOut = panel.readout({ label: 'Selected token', value: '"The"' });
  const nextOut = panel.readout({ label: 'Top next token', value: '—' });
  panel.info('The colour of cell [i,j] = how much token i attends to token j. Darker = more attention.');

  // Update token select when sentence changes
  let lastSentIdx = -1;

  sim.setUpdate((ctx, dt, w, h) => {
    // Update select options if sentence changed
    if (sentIdx !== lastSentIdx) {
      lastSentIdx = sentIdx;
      const toks = getTokens();
      // Rebuild select options (best effort – replace select body)
      selectedToken = Math.min(selectedToken, toks.length - 1);
    }

    const tokens = getTokens();
    const N = tokens.length;
    const attn = computeAttention(tokens);
    const { A } = attn;

    ctx.clearRect(0, 0, w, h);
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);

    // Attention heatmap (left)
    const margin = 8;
    const labelH = 70;
    const mapSize = Math.min(w * 0.55 - margin, h - labelH * 2 - 40);
    const cellSize = mapSize / N;
    const mapX = margin + labelH, mapY = 50 + labelH;

    // Row/col labels
    ctx.fillStyle = 'rgba(199,212,234,0.75)'; ctx.font = '11px Poppins,sans-serif';
    tokens.forEach((tok, i) => {
      // Column header (rotated)
      ctx.save();
      ctx.translate(mapX + i * cellSize + cellSize / 2, mapY - 4);
      ctx.rotate(-Math.PI / 3);
      ctx.fillStyle = i === selectedToken ? '#fbbf24' : 'rgba(199,212,234,0.75)';
      ctx.textAlign = 'right'; ctx.font = '11px Poppins,sans-serif';
      ctx.fillText(tok, 0, 0);
      ctx.restore();
      // Row label
      ctx.fillStyle = i === selectedToken ? '#fbbf24' : 'rgba(199,212,234,0.75)';
      ctx.textAlign = 'right'; ctx.font = '11px Poppins,sans-serif';
      ctx.fillText(tok, mapX - 4, mapY + i * cellSize + cellSize / 2 + 4);
    });

    // Heatmap cells
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        const val = A[i][j];
        const isSelRow = i === selectedToken;
        const cx2 = mapX + j * cellSize, cy2 = mapY + i * cellSize;
        if (isSelRow) {
          const r = Math.round(val * 255);
          ctx.fillStyle = `rgba(245,158,11,${0.15 + val * 0.75})`;
        } else {
          ctx.fillStyle = `rgba(99,102,241,${0.1 + val * 0.7})`;
        }
        ctx.fillRect(cx2, cy2, cellSize - 1, cellSize - 1);
        // Show value if cell large enough
        if (cellSize > 28) {
          ctx.fillStyle = val > 0.4 ? '#fff' : 'rgba(199,212,234,0.5)';
          ctx.font = '9px monospace'; ctx.textAlign = 'center';
          ctx.fillText(val.toFixed(2), cx2 + cellSize / 2, cy2 + cellSize / 2 + 3);
        }
      }
      // Highlight selected row border
      if (i === selectedToken) {
        ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2;
        ctx.strokeRect(mapX, mapY + i * cellSize - 1, N * cellSize, cellSize + 1);
      }
    }
    // Grid
    ctx.strokeStyle = 'rgba(165,180,252,0.2)'; ctx.lineWidth = 0.5;
    for (let i = 0; i <= N; i++) {
      ctx.beginPath(); ctx.moveTo(mapX + i * cellSize, mapY); ctx.lineTo(mapX + i * cellSize, mapY + N * cellSize); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(mapX, mapY + i * cellSize); ctx.lineTo(mapX + N * cellSize, mapY + i * cellSize); ctx.stroke();
    }

    // Attention axis labels
    ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '10px Poppins,sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('Key tokens (what we attend TO)', mapX + mapSize / 2, mapY + mapSize + 18);
    ctx.save(); ctx.translate(margin, mapY + mapSize / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('Query tokens (who is attending)', 0, 0); ctx.restore();

    // Bar chart: selected row attention weights
    const barX = mapX + mapSize + 20;
    const barMaxW = w - barX - 16;
    if (barMaxW > 60) {
      const selRow = A[selectedToken];
      const barH = Math.min(24, (h - 80) / N - 4);
      ctx.fillStyle = 'rgba(199,212,234,0.8)'; ctx.font = 'bold 12px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(`"${tokens[selectedToken]}" attends to:`, barX, 48);

      selRow.forEach((val, j) => {
        const by = 64 + j * (barH + 6);
        ctx.fillStyle = 'rgba(99,102,241,0.1)';
        ctx.fillRect(barX, by, barMaxW, barH);
        ctx.fillStyle = `rgba(245,158,11,${0.4 + val * 0.6})`;
        ctx.fillRect(barX, by, val * barMaxW, barH);
        ctx.fillStyle = '#e8eefb'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'left';
        ctx.fillText(`"${tokens[j]}"  ${(val * 100).toFixed(0)}%`, barX + 4, by + barH - 3);
      });

      // Next-token prediction
      const preds = predictNext(tokens, attn);
      const predY = 64 + N * (barH + 6) + 20;
      ctx.fillStyle = 'rgba(199,212,234,0.8)'; ctx.font = 'bold 12px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('Next token probabilities:', barX, predY);
      preds.forEach(({ w: ww, s }, i) => {
        const normS = (s + 1) / 2;  // map [-1,1] → [0,1]
        const py2 = predY + 16 + i * 18;
        ctx.fillStyle = 'rgba(16,185,129,0.15)';
        ctx.fillRect(barX, py2, normS * barMaxW, 14);
        ctx.fillStyle = '#10b981'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'left';
        ctx.fillText(`"${ww}" (${(normS * 100).toFixed(0)}%)`, barX + 4, py2 + 11);
      });
      nextOut.set(`"${preds[0].w}"`);
    }

    headOut.set(`"${tokens[selectedToken]}"`);
    badge.set(`Attention: ${N} tokens × ${N} tokens`);
  });

  sim.start();

  return {
    dispose() { panel.dispose(); hud.dispose(); sim.dispose(); },
  };
}
