/**
 * How language models work — a tiny language model you can watch. Text is split into tokens
 * (here, words and punctuation, each with its ID in the vocabulary), and the model predicts a
 * probability for every possible next token from counts of what followed the same one or two
 * tokens in its training text (a trigram model backed off to bigrams). Temperature reshapes those
 * probabilities before sampling. Tap a candidate to choose it yourself, or let it generate.
 * Real models do the same next-token step with a neural network that attends to the whole context.
 */
import { createKit, T, Spring, fmt, clamp, text, pill, withAlpha, card } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const CORPUS = `the cat sat on the mat . the dog sat on the rug . the cat chased the mouse . the dog chased the cat .
a cat is a small animal . a dog is a loyal friend . the sun rises in the east . the moon rises at night .
the sun sets in the west . i love to learn about ai . ai is the future of learning . nebians is a place to learn .
the future is bright for students . the cat and the dog are friends . knowledge is the key to success .
the sky is blue and clear . the sky is dark at night . students learn from books and from teachers .
a model learns from data . a model predicts the next word . the next word depends on the words before it .
the mountains of nepal are tall . mount everest is the tallest mountain . the river flows to the sea .
i love the mountains of nepal . the students love to learn . the dog is happy . the cat is sleepy .`;
const TOK = CORPUS.split(/\s+/).filter(Boolean);
const VOCAB = [...new Set(TOK)].sort();
const ID = new Map(VOCAB.map((w, i) => [w, i]));
const BI = new Map(), TRI = new Map();
for (let i = 0; i < TOK.length - 1; i++) {
  const a = TOK[i], b = TOK[i + 1];
  if (!BI.has(a)) BI.set(a, new Map()); BI.get(a).set(b, (BI.get(a).get(b) || 0) + 1);
  if (i < TOK.length - 2) { const key = a + ' ' + b, c = TOK[i + 2]; if (!TRI.has(key)) TRI.set(key, new Map()); TRI.get(key).set(c, (TRI.get(key).get(c) || 0) + 1); }
}
const COLORS = ['#dbeafe', '#fce7f3', '#dcfce7', '#fef3c7', '#ede9fe', '#cffafe', '#ffe4e6', '#e0e7ff'];

export default function init(stage) {
  const k = createKit(stage, { trackPointer: true, label: 'Tokens of a sentence and a tiny language model\'s next-token probabilities' });
  const hud = createHud(stage);
  const badge = hud.badge('Tap a candidate word to add it', '#7c3aed');

  let tokens = ['the', 'cat'], temp = 1, gen = false, genT = 0, genCount = 0, src = 'trigram';
  let cands = [], seen = [];
  const grow = new Spring(0, 200, 16);

  const panel = createPanel(stage, { title: 'Next-token prediction' });
  const row = document.createElement('div'); row.className = 'ix-ctrl-row';
  const input = document.createElement('input'); input.type = 'text'; input.value = tokens.join(' '); input.setAttribute('aria-label', 'Prompt');
  input.style.cssText = 'font:500 .85rem var(--md-font,Poppins,sans-serif);padding:9px 11px;border-radius:10px;border:1px solid #d9e1ee;background:#f6f8fc;color:#172033;width:100%;box-sizing:border-box';
  const lab = document.createElement('span'); lab.className = 'ix-ctrl-label'; lab.textContent = 'Your prompt (type, then press Enter)';
  row.appendChild(lab); row.appendChild(input); panel.body.appendChild(row);
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') { tokens = tokenize(input.value); predict(); k.invalidate(); } });
  input.addEventListener('change', () => { tokens = tokenize(input.value); predict(); k.invalidate(); });
  panel.chips({ label: 'Start with', options: ['the cat', 'ai is', 'the sun', 'i love', 'a model'].map((s) => ({ value: s, label: s })), value: 'the cat', onChange: (s) => { tokens = s.split(' '); sync(); } });
  panel.slider({ label: 'Temperature', min: 0.1, max: 2, step: 0.05, value: temp, format: (v) => v.toFixed(2), onChange: (v) => { temp = v; predict(); k.invalidate(); } });
  const [genB] = panel.buttonRow([{ label: 'Generate', icon: 'auto_awesome', onClick: () => { gen = !gen; genCount = 0; genB.setLabel(gen ? 'Stop' : 'Generate'); k.animate(true); } }, { label: 'Undo', icon: 'undo', variant: 'ghost', onClick: () => { if (tokens.length > 1) tokens.pop(); sync(); } }]);
  const st = panel.stats([{ key: 'n', label: 'Tokens' }, { key: 'vocab', label: 'Vocabulary' }, { key: 'src', label: 'Prediction uses' }, { key: 'top', label: 'Most likely next' }]);
  panel.info('Low temperature always picks the most likely word (safe but repetitive); high temperature flattens the odds (creative, then nonsense). Training is counting (here) or adjusting billions of weights (real models); prompting is just running the prediction again and again.');
  st.vocab.set(`${VOCAB.length} tokens`);

  function tokenize(s) { return s.toLowerCase().replace(/([.,!?])/g, ' $1 ').split(/\s+/).filter(Boolean); }
  function sync() { input.value = tokens.join(' ').replace(/ \./g, '.'); predict(); k.invalidate(); }
  function predict() {
    const counts = new Map();
    src = 'nothing it knows';
    const n = tokens.length;
    if (n >= 2 && TRI.has(tokens[n - 2] + ' ' + tokens[n - 1])) { for (const [w, c] of TRI.get(tokens[n - 2] + ' ' + tokens[n - 1])) counts.set(w, (counts.get(w) || 0) + c * 4); src = 'last 2 tokens'; }
    if (n >= 1 && BI.has(tokens[n - 1])) { for (const [w, c] of BI.get(tokens[n - 1])) counts.set(w, (counts.get(w) || 0) + c); if (src === 'nothing it knows') src = 'last token only'; }
    seen = [];
    if (n >= 2 && TRI.has(tokens[n - 2] + ' ' + tokens[n - 1])) for (const [w, c] of TRI.get(tokens[n - 2] + ' ' + tokens[n - 1])) seen.push(`"${tokens[n - 2]} ${tokens[n - 1]}" was followed by "${w}" ${c}×`);
    if (n >= 1 && BI.has(tokens[n - 1])) for (const [w, c] of BI.get(tokens[n - 1])) seen.push(`"${tokens[n - 1]}" was followed by "${w}" ${c}×`);
    if (!counts.size) for (const w of ['the', 'a', 'i']) counts.set(w, 1);
    let list = [...counts.entries()].map(([w, c]) => ({ w, p: Math.pow(c, 1 / temp) }));
    const z = list.reduce((s, x) => s + x.p, 0); list.forEach((x) => { x.p /= z; });
    list.sort((a, b) => b.p - a.p);
    cands = list.slice(0, 8);
    grow.set(0); grow.to(1); k.animate(true);
  }
  function sample() { let r = Math.random(), acc = 0; for (const c of cands) { acc += c.p; if (r <= acc) return c.w; } return cands[0].w; }

  let tx = 0, ty = 0, bx = 0, by = 0, bw = 0, rowH = 30;
  const hits = [];
  k.onResize((w, h) => { tx = 16; ty = 58; bx = 16; bw = w - 32; by = k.small ? 170 : 200; rowH = Math.min(36, (h - by - 20) / 8); });
  k.drag({ hit: (x, y) => { for (const hh of hits) if (x > hh.x && x < hh.x + hh.w && y > hh.y && y < hh.y + hh.h) return 1; return false; }, up: (x, y) => { for (const hh of hits) if (x > hh.x && x < hh.x + hh.w && y > hh.y && y < hh.y + hh.h) { tokens.push(hh.wd); sync(); return; } }, cursor: 'pointer', cursorActive: 'pointer' });

  k.frame((ctx, dt, w, h) => {
    if (gen) { genT += dt; if (genT > 0.7) { genT = 0; tokens.push(sample()); genCount++; sync(); if (genCount >= 14 || tokens.length > 40) { gen = false; genB.setLabel('Generate'); } } }
    const g = grow.step(dt);
    ctx.fillStyle = '#f7f8fd'; ctx.fillRect(0, 0, w, h);
    // token chips (wrap)
    text(ctx, 'Tokens and their IDs', tx, ty - 12, T.ink2, 10.5, 700);
    ctx.font = `600 ${k.small ? 12 : 14}px ${T.font}`;
    let x = tx, y = ty;
    const pos = [];
    const start = Math.max(0, tokens.length - 30);
    for (let i = start; i < tokens.length; i++) {
      const t2 = tokens[i], tw = ctx.measureText(t2).width + 22;
      if (x + tw > w - 16) { x = tx; y += k.small ? 40 : 46; }
      const used = (src === 'last 2 tokens' && i >= tokens.length - 2) || (src === 'last token only' && i === tokens.length - 1);
      ctx.fillStyle = COLORS[(ID.get(t2) ?? 7) % COLORS.length]; ctx.strokeStyle = used ? '#7c3aed' : 'rgba(23,32,51,0.12)'; ctx.lineWidth = used ? 2 : 1;
      ctx.beginPath(); ctx.roundRect(x, y, tw, k.small ? 24 : 28, 7); ctx.fill(); ctx.stroke();
      text(ctx, t2, x + tw / 2, y + (k.small ? 17 : 19), T.ink, k.small ? 12 : 14, 600, 'center');
      text(ctx, ID.has(t2) ? `#${ID.get(t2)}` : 'unknown', x + tw / 2, y + (k.small ? 35 : 40), ID.has(t2) ? T.mute : T.red, 8.5, 600, 'center');
      pos.push(x + tw / 2, y);
      x += tw + 6;
    }
    // the slot for the next token
    ctx.setLineDash([4, 4]); ctx.strokeStyle = '#7c3aed'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.roundRect(x, y, 46, k.small ? 24 : 28, 7); ctx.stroke(); ctx.setLineDash([]);
    text(ctx, '?', x + 23, y + (k.small ? 17 : 19), '#7c3aed', 14, 800, 'center');
    // attention arcs from the slot to the tokens it uses
    const nUsed = src === 'last 2 tokens' ? 2 : src === 'last token only' ? 1 : 0;
    for (let u = 0; u < nUsed; u++) {
      const pi = pos.length - 2 - u * 2; if (pi < 0) break;
      const sx = x + 23, sy = y, ex = pos[pi], ey = pos[pi + 1];
      ctx.strokeStyle = withAlpha('#7c3aed', u === 0 ? 0.8 : 0.45); ctx.lineWidth = u === 0 ? 3 : 2;
      ctx.beginPath(); ctx.moveTo(sx, sy); ctx.quadraticCurveTo((sx + ex) / 2, Math.min(sy, ey) - 26 - u * 10, ex, ey); ctx.stroke();
    }
    // candidates
    text(ctx, `Next-token probabilities (temperature ${fmt(temp, 2)}) — tap one to choose it`, bx, by - 12, T.ink2, 10.5, 700);
    hits.length = 0;
    for (let i = 0; i < cands.length; i++) {
      const c = cands[i], yy = by + i * rowH, bwid = (bw - 120) * c.p * grow.x;
      const hot = k.pointer.inside && k.pointer.y > yy && k.pointer.y < yy + rowH - 4 && k.pointer.x > bx && k.pointer.x < bx + bw;
      ctx.fillStyle = hot ? '#f1edff' : '#ffffff'; ctx.strokeStyle = 'rgba(23,32,51,0.08)'; ctx.beginPath(); ctx.roundRect(bx, yy, bw, rowH - 4, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = withAlpha('#7c3aed', i === 0 ? 0.75 : 0.4); ctx.beginPath(); ctx.roundRect(bx + 100, yy + 5, Math.max(2, bwid), rowH - 14, 5); ctx.fill();
      text(ctx, c.w, bx + 12, yy + rowH * 0.62, T.ink, 13, 700);
      text(ctx, `${fmt(c.p * 100, 1)} %`, bx + bw - 10, yy + rowH * 0.62, T.ink2, 11, 600, 'right');
      hits.push({ x: bx, y: yy, w: bw, h: rowH - 4, wd: c.w });
    }
    const sy = by + cands.length * rowH + 16;
    if (h - sy > 80 && seen.length) {
      card(ctx, bx, sy, bw, Math.min(h - sy - 12, 26 + Math.min(seen.length, 8) * 18), 12);
      text(ctx, 'What it saw in its training text', bx + 12, sy + 19, T.ink, 11, 700);
      for (let i = 0; i < Math.min(seen.length, Math.floor((h - sy - 40) / 18), 8); i++) text(ctx, seen[i], bx + 12, sy + 40 + i * 18, T.ink2, 10.5, 500);
    }
    st.n.set(String(tokens.length)); st.src.set(src); st.top.set(cands.length ? `"${cands[0].w}" ${fmt(cands[0].p * 100, 0)} %` : '—');
    badge.set(gen ? `Generating… ${genCount} new tokens` : src === 'nothing it knows' ? 'It has never seen these words: it can only guess common ones' : 'Tap a candidate word to add it');
    k.animate(gen || g);
  });

  predict();
  k.debug = { tokens: () => tokens.join(' '), cand: (i) => [bx + 40, by + i * rowH + rowH / 2], cands: () => cands.map((c) => c.w) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
