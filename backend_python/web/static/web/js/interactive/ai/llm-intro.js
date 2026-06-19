import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { panelBg, labelText, roundRect } from '../biology/bio-utils.js';

// A tiny n-gram "language model" trained on a small in-memory corpus.
// Demonstrates next-token prediction, attention highlight, and tokenisation.

const CORPUS = [
  'the cat sat on the mat',
  'the dog sat on the rug',
  'the cat chased the mouse',
  'the dog chased the cat',
  'a cat is a small animal',
  'a dog is a loyal friend',
  'the sun rises in the east',
  'the moon rises in the night',
  'i love to learn about ai',
  'ai is the future of learning',
  'nebians is a place to learn',
  'the future is bright for ai',
  'the cat and the dog are friends',
  'knowledge is the key to success',
  'the sky is blue and clear',
];

function tokenize(s) { return s.toLowerCase().split(/\s+/).filter(Boolean); }

// Build a bigram + trigram count model from the corpus.
const bigram = {}; const trigram = {};
CORPUS.forEach((s) => {
  const t = tokenize(s);
  for (let i = 0; i < t.length - 1; i++) {
    const a = t[i], b = t[i + 1];
    bigram[a] = bigram[a] || {}; bigram[a][b] = (bigram[a][b] || 0) + 1;
  }
  for (let i = 0; i < t.length - 2; i++) {
    const key = t[i] + ' ' + t[i + 1];
    trigram[key] = trigram[key] || {}; trigram[key][t[i + 2]] = (trigram[key][t[i + 2]] || 0) + 1;
  }
});
const VOCAB = [...new Set(CORPUS.flatMap(tokenize))].sort();

function predictNext(contextTokens) {
  // prefer trigram if available, fall back to bigram, then uniform
  const counts = {};
  if (contextTokens.length >= 2) {
    const key = contextTokens.slice(-2).join(' ');
    if (trigram[key]) Object.entries(trigram[key]).forEach(([w, c]) => counts[w] = (counts[w] || 0) + c * 3);
  }
  if (contextTokens.length >= 1) {
    const last = contextTokens[contextTokens.length - 1];
    if (bigram[last]) Object.entries(bigram[last]).forEach(([w, c]) => counts[w] = (counts[w] || 0) + c);
  }
  const entries = Object.entries(counts);
  if (!entries.length) {
    // fallback: most common starting tokens
    return VOCAB.map((w) => ({ w, p: 1 / VOCAB.length }));
  }
  const total = entries.reduce((s, [, c]) => s + c, 0);
  return entries.map(([w, c]) => ({ w, p: c / total })).sort((a, b) => b.p - a.p).slice(0, 8);
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const stateBadge = hud.badge('Type some words…', '#a3e635');

  let text = 'the cat';
  let caret = text.length;
  let predictions = predictNext(tokenize(text));
  let generated = '';

  const panel = createPanel(stage, { title: 'How ChatGPT Works' });
  panel.info('A language model predicts the next token from the text so far. Type words (or pick a suggestion) and watch the model\'s ranked guesses. Press Auto-complete to let it write on its own.');
  panel.button({ label: 'Auto-complete next word', icon: 'auto_awesome', onClick: () => { acceptTop(); } });
  panel.button({ label: 'Generate 8 words', icon: 'fast_forward', onClick: () => { for (let i = 0; i < 8; i++) acceptTop(true); } });
  panel.button({ label: 'Clear', icon: 'delete', variant: 'ghost', onClick: () => { text = ''; caret = 0; generated = ''; refresh(); } });
  panel.divider();
  const tokenOut = panel.readout({ label: 'Tokens so far', value: '0' });
  panel.button({ label: 'What is a token?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Tokens, not words',
      body: 'Language models work with tokens — small chunks of text, often a word or part of a word. "unbelievable" might split into "un" + "believ" + "able". This lets one model handle any language and spell even rare words. A model\'s context window is measured in tokens.',
      color: '#6366F1',
    });
  } });
  panel.button({ label: 'What is attention?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Attention',
      body: 'Attention lets each token look back at every earlier token and decide which matter most. To predict "it" in "the dog chased the cat because it…", attention focuses on "dog" or "cat" to resolve what "it" refers to. Transformers are built entirely from attention.',
      color: '#6366F1',
    });
  } });

  function refresh() {
    predictions = predictNext(tokenize(text));
    tokenOut.set(String(tokenize(text).length));
    if (!text.trim()) stateBadge.set('Type some words…');
    else stateBadge.set(`${predictions.length} guesses for next token`);
  }

  function acceptTop(silent) {
    if (!predictions.length) return;
    text = (text + (text && !text.endsWith(' ') ? ' ' : '') + predictions[0].w);
    caret = text.length;
    generated += (generated ? ' ' : '') + predictions[0].w;
    refresh();
    if (!silent) {
      showInfoCard(stage, {
        title: `Added "${predictions[0].w}"`,
        body: `The model\'s top guess (probability ${(predictions[0].p * 100).toFixed(0)}%). It now re-predicts the next token from the new context.`,
        color: '#a3e635',
      });
    }
  }

  // Keyboard input via a hidden text field trick: we listen on window keydown
  function onKey(e) {
    if (e.key === ' ') { text = text.slice(0, caret) + ' ' + text.slice(caret); caret++; e.preventDefault(); refresh(); }
    else if (e.key === 'Backspace') { if (caret > 0) { text = text.slice(0, caret - 1) + text.slice(caret); caret--; } refresh(); }
    else if (e.key === 'Enter') { acceptTop(); }
    else if (e.key.length === 1 && /[a-z]/i.test(e.key)) { text = text.slice(0, caret) + e.key + text.slice(caret); caret++; refresh(); }
  }
  window.addEventListener('keydown', onKey);

  refresh();

  sim.setUpdate((ctx) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#070a14'; ctx.fillRect(0, 0, w, h);

    // Text prompt box
    const boxX = 20; const boxY = 20; const boxW = w - 40; const boxH = 70;
    panelBg(ctx, boxX, boxY, boxW, boxH);
    labelText(ctx, 'Your text (type, or click a suggestion below):', boxX + 12, boxY + 18, { color: '#9ec1ff', size: 11 });
    // render tokens as chips with attention tint
    const tokens = tokenize(text);
    let tx = boxX + 12; const ty = boxY + 44;
    ctx.font = '600 18px Poppins, sans-serif'; ctx.textBaseline = 'alphabetic';
    if (!text) {
      labelText(ctx, '▍ start typing…', tx, ty, { color: '#475569', size: 18 });
    } else {
      // split with spaces preserved
      let cursor = 0;
      const parts = text.split(/(\s+)/);
      parts.forEach((part) => {
        if (!part) return;
        if (/^\s+$/.test(part)) { tx += ctx.measureText(part).width; return; }
        // attention weight: more recent tokens brighter
        const recency = 0.4 + 0.6 * (cursor / Math.max(1, tokens.length - 1));
        const pw = ctx.measureText(part).width;
        ctx.fillStyle = `rgba(99,102,241,${0.15 + recency * 0.35})`;
        roundRect(ctx, tx - 4, ty - 18, pw + 8, 26, 6); ctx.fill();
        ctx.fillStyle = `rgba(226,232,240,${0.7 + recency * 0.3})`;
        ctx.fillText(part, tx, ty);
        tx += pw;
        cursor++;
      });
      // caret
      if (Math.floor(performance.now() / 500) % 2 === 0) {
        ctx.fillStyle = '#a3e635';
        ctx.fillRect(tx + 2, ty - 18, 2, 24);
      }
    }

    // Predictions
    const py = boxY + boxH + 24;
    labelText(ctx, 'Most likely next token:', boxX + 12, py, { color: '#9ec1ff', size: 12 });
    predictions.slice(0, 6).forEach((p, i) => {
      const chipX = boxX + 12 + i * 150; const chipY = py + 10; const chipW = 140; const chipH = 56;
      ctx.fillStyle = i === 0 ? 'rgba(52,211,153,0.18)' : 'rgba(99,102,241,0.12)';
      ctx.strokeStyle = i === 0 ? '#34d399' : '#6366f1'; ctx.lineWidth = i === 0 ? 2 : 1;
      roundRect(ctx, chipX, chipY, chipW, chipH, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#e2e8f0'; ctx.font = '600 16px Poppins, sans-serif';
      ctx.fillText(p.w, chipX + 12, chipY + 24);
      ctx.fillStyle = i === 0 ? '#34d399' : '#94a3b8'; ctx.font = '500 12px Poppins, sans-serif';
      ctx.fillText(`${(p.p * 100).toFixed(0)}%`, chipX + 12, chipY + 44);
      // store chip rect for click hit-testing
      p._rect = { x: chipX, y: chipY, w: chipW, h: chipH };
    });

    // Help footer
    labelText(ctx, 'Tip: this is a tiny model trained on ~15 sentences. Real models like GPT-4 train on billions of pages — but the core idea is identical: predict the next token.', boxX + 12, h - 16, { color: '#64748b', size: 11 });
  });

  // click prediction chips
  function onClick(e) {
    const rect = sim.canvas.getBoundingClientRect();
    const x = e.clientX - rect.left, y = e.clientY - rect.top;
    for (const p of predictions) {
      if (!p._rect) continue;
      if (x >= p._rect.x && x <= p._rect.x + p._rect.w && y >= p._rect.y && y <= p._rect.y + p._rect.h) {
        text = (text + (text && !text.endsWith(' ') ? ' ' : '') + p.w);
        caret = text.length; refresh();
        break;
      }
    }
  }
  sim.canvas.addEventListener('click', onClick);

  sim.start();

  return {
    dispose() {
      window.removeEventListener('keydown', onKey);
      sim.canvas.removeEventListener('click', onClick);
      panel.dispose(); hud.dispose(); sim.dispose();
    },
  };
}
