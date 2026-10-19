/**
 * What is AI? — drag each card into the right place: inside Deep Learning, Machine Learning or
 * AI (the rings are nested, because deep learning is a kind of machine learning, which is one way
 * of doing AI), or into "Not AI" for things that only follow fixed instructions. A right answer
 * settles into its ring; a wrong one springs back and says why.
 */
import { createKit, T, Spring, fmt, clamp, text, pill, withAlpha, card, softShadow } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const ITEMS = [
  { t: 'Chess engine searching millions of moves', r: 'ai', why: 'It plans with search and hand-written rules about good positions: AI, but it does not learn from data.' },
  { t: 'Spam filter that learns from emails you mark', r: 'ml', why: 'It learns which words predict spam from labelled examples: machine learning.' },
  { t: 'Chatbot writing an essay', r: 'dl', why: 'Large language models are huge neural networks trained on text: deep learning.' },
  { t: 'Face unlock on a phone', r: 'dl', why: 'Faces are recognised by a deep convolutional network trained on many images.' },
  { t: 'Calculator doing 2 + 2', r: 'none', why: 'It follows exact arithmetic rules. No reasoning, no learning: not AI.' },
  { t: 'Route planner finding the shortest path', r: 'ai', why: 'Classic search (Dijkstra, A*) is a core AI technique, with no learning needed.' },
  { t: 'Video recommender', r: 'ml', why: 'It learns your tastes from what you and similar people watched.' },
  { t: 'Self-driving car seeing pedestrians', r: 'dl', why: 'Camera images are understood by deep neural networks.' },
  { t: 'Thermostat switching on at 7 am', r: 'none', why: 'A fixed timer rule set by a person: automation, not AI.' },
  { t: 'Image generator from a text prompt', r: 'dl', why: 'Diffusion models are deep networks trained on millions of captioned pictures.' },
  { t: 'Weather forecast fitted to past data', r: 'ml', why: 'A model learns patterns from years of measurements.' },
  { t: 'Digital clock', r: 'none', why: 'It just counts seconds. Nothing is decided or learned.' },
];
const RING = { ai: { label: 'Artificial Intelligence', color: '#4f46e5' }, ml: { label: 'Machine Learning', color: '#7c3aed' }, dl: { label: 'Deep Learning', color: '#db2777' }, none: { label: 'Not AI', color: '#64748b' } };

export default function init(stage) {
  const k = createKit(stage, { label: 'Nested rings for AI, machine learning and deep learning, with cards to sort' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the card into the right ring', '#4f46e5');

  let order = ITEMS.map((_, i) => i).sort(() => Math.random() - 0.5), cur = 0, correct = 0, tries = 0;
  const placed = [];
  const cx = new Spring(0, 200, 18), cy = new Spring(0, 200, 18), shake = new Spring(0, 500, 12), pop = new Spring(0, 200, 14);
  let held = false, gx = 0, gy = 0, msg = '', msgOk = true, msgT = 0;

  const panel = createPanel(stage, { title: 'Sort it out' });
  panel.button({ label: 'Shuffle and start again', icon: 'shuffle', variant: 'ghost', onClick: restart });
  const st = panel.stats([{ key: 'done', label: 'Sorted' }, { key: 'acc', label: 'First-try accuracy' }]);
  const why = panel.info('Traditional programs follow rules a person wrote. Machine learning finds the rules from examples. Deep learning does that with many-layered neural networks.');

  function restart() { order = ITEMS.map((_, i) => i).sort(() => Math.random() - 0.5); cur = 0; correct = 0; tries = 0; placed.length = 0; resetCard(); k.animate(true); }
  let deckX = 0, deckY = 0, cw = 220, ch = 70, vx = 0, vy = 0, vrx = 0, vry = 0, noneBox = { x: 0, y: 0, w: 0, h: 0 };
  function resetCard() { cx.to(deckX); cy.to(deckY); }
  k.onResize((w, h) => {
    cw = k.small ? 180 : 230; ch = k.small ? 62 : 72;
    if (k.small) { deckX = w / 2; deckY = 76; vx = w / 2; vy = h * 0.6; vrx = w * 0.46; vry = h * 0.3; noneBox = { x: w - 96, y: 120, w: 86, h: 60 }; }
    else { deckX = w * 0.82; deckY = h * 0.3; vx = w * 0.38; vy = h * 0.54; vrx = w * 0.34; vry = h * 0.42; noneBox = { x: w * 0.72, y: h * 0.62, w: w * 0.24, h: h * 0.3 }; }
    cx.set(deckX); cy.set(deckY);
  });
  const inEll = (x, y, s) => ((x - vx) / (vrx * s)) ** 2 + ((y - (vy + vry * (1 - s) * 0.7)) / (vry * s)) ** 2 <= 1;
  function regionAt(x, y) {
    if (x > noneBox.x && x < noneBox.x + noneBox.w && y > noneBox.y && y < noneBox.y + noneBox.h) return 'none';
    if (inEll(x, y, 0.38)) return 'dl';
    if (inEll(x, y, 0.68)) return 'ml';
    if (inEll(x, y, 1)) return 'ai';
    return null;
  }

  const cardH = k.drag({
    enabled: () => cur < order.length,
    hit: (x, y, s) => (Math.abs(x - cx.x) < cw / 2 + s && Math.abs(y - cy.x) < ch / 2 + s ? 1 : false),
    down: (x, y) => { held = true; gx = x - cx.x; gy = y - cy.x; },
    move: (x, y) => { cx.set(x - gx); cy.set(y - gy); },
    up: (x, y) => {
      held = false;
      const reg = regionAt(x, y), it = ITEMS[order[cur]];
      if (!reg) { resetCard(); return; }
      tries++;
      if (reg === it.r) {
        if (tries === 1) correct++;
        placed.push({ i: order[cur], r: reg, x: x, y: y });
        msg = `✓ ${it.why}`; msgOk = true; pop.v = 8;
        cur++; tries = 0; cx.set(deckX); cy.set(deckY - 40); resetCard();
      } else {
        msg = `Not quite — ${it.why}`; msgOk = false; shake.v = 60; resetCard();
      }
      msgT = 6; why.set(msg);
      k.animate(true);
    },
  });

  k.frame((ctx, dt, w, h) => {
    const moving = cx.step(dt) | cy.step(dt) | shake.step(dt) | pop.step(dt);
    msgT = Math.max(0, msgT - dt);
    ctx.fillStyle = '#f7f8fd'; ctx.fillRect(0, 0, w, h);
    // nested rings
    const hover = held ? regionAt(k.pointer.x, k.pointer.y) : null;
    for (const [key, s] of [['ai', 1], ['ml', 0.68], ['dl', 0.38]]) {
      const R = RING[key], yy = vy + vry * (1 - s) * 0.7;
      ctx.beginPath(); ctx.ellipse(vx, yy, vrx * s, vry * s, 0, 0, Math.PI * 2);
      ctx.fillStyle = withAlpha(R.color, hover === key ? 0.2 : 0.08); ctx.fill();
      ctx.strokeStyle = withAlpha(R.color, hover === key ? 1 : 0.6); ctx.lineWidth = hover === key ? 3 : 2; ctx.stroke();
      text(ctx, R.label, vx, yy - vry * s + (k.small ? 16 : 22), R.color, k.small ? 11 : 13, 800, 'center');
    }
    ctx.fillStyle = withAlpha(RING.none.color, hover === 'none' ? 0.18 : 0.07); ctx.strokeStyle = withAlpha(RING.none.color, hover === 'none' ? 1 : 0.5); ctx.setLineDash([6, 5]); ctx.lineWidth = 2;
    ctx.beginPath(); ctx.roundRect(noneBox.x, noneBox.y, noneBox.w, noneBox.h, 12); ctx.fill(); ctx.stroke(); ctx.setLineDash([]);
    text(ctx, 'Not AI', noneBox.x + noneBox.w / 2, noneBox.y + 20, RING.none.color, k.small ? 11 : 13, 800, 'center');
    // placed chips
    ctx.font = `600 9.5px ${T.font}`;
    for (const p of placed) {
      const it = ITEMS[p.i], maxW = k.small ? 100 : 170;
      let label = it.t; while (ctx.measureText(label).width > maxW - 14 && label.length > 4) label = label.slice(0, -2);
      if (label !== it.t) label = label.trimEnd() + '…';
      const tw = ctx.measureText(label).width + 14;
      ctx.fillStyle = '#fff'; ctx.strokeStyle = withAlpha(RING[p.r].color, 0.7); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.roundRect(p.x - tw / 2, p.y - 10, tw, 20, 10); ctx.fill(); ctx.stroke();
      text(ctx, label, p.x, p.y + 4, T.ink2, 9.5, 600, 'center');
    }
    // the card
    if (cur < order.length) {
      const it = ITEMS[order[cur]], x = cx.x + Math.sin(shake.x * 0.3) * shake.x * 0.08, y = cy.x;
      softShadow(ctx, x, y + ch / 2 + 4, cw * 0.5, 6, held ? 0.35 : 0.2);
      ctx.save(); ctx.translate(x, y); ctx.rotate(held ? 0.03 : 0); const sc = 1 + (held ? 0.04 : 0) + pop.x * 0.004; ctx.scale(sc, sc);
      card(ctx, -cw / 2, -ch / 2, cw, ch, 14, '#ffffff', held ? '#4f46e5' : 'rgba(23,32,51,0.12)');
      wrap(ctx, it.t, 0, -ch / 2 + 26, cw - 28, 17);
      ctx.restore();
      if (!held && placed.length === 0) text(ctx, 'drag me ↓', deckX, deckY + ch / 2 + 18, '#4f46e5', 11, 700, 'center');
      text(ctx, `${cur + 1} / ${order.length}`, deckX + cw / 2, deckY - ch / 2 - 8, T.mute, 10, 600, 'right');
    } else {
      pill(ctx, `All sorted! ${correct} of ${ITEMS.length} right first time`, deckX, deckY, { bg: T.green, color: '#fff', border: false, size: 13 });
    }
    if (msgT > 0 && !k.small) { const a = Math.min(1, msgT); ctx.globalAlpha = a; card(ctx, 16, h - 76, Math.min(560, w - 32), 60, 12, msgOk ? '#f0fdf4' : '#fff7ed', msgOk ? '#86efac' : '#fdba74'); wrap(ctx, msg, 30, h - 54, Math.min(530, w - 60), 16, 'left'); ctx.globalAlpha = 1; }
    st.done.set(`${cur} of ${ITEMS.length}`); st.acc.set(cur ? `${fmt(correct / cur * 100, 0)} %` : '—');
    badge.set(msgT > 0 ? (msgOk ? 'Right!' : 'Try another ring') : 'Drag the card into the right ring');
    k.animate(moving || held || msgT > 0);
  });

  function wrap(ctx, s, x, y, maxW, lh, align = 'center') {
    ctx.font = `600 ${k.small ? 11.5 : 13}px ${T.font}`; ctx.fillStyle = T.ink; ctx.textAlign = align; ctx.textBaseline = 'alphabetic';
    let line = '', yy = y;
    for (const word of s.split(' ')) { const test = line ? line + ' ' + word : word; if (ctx.measureText(test).width > maxW && line) { ctx.fillText(line, x, yy); line = word; yy += lh; } else line = test; }
    if (line) ctx.fillText(line, x, yy);
  }

  resetCard();
  k.debug = { card: () => [cx.x, cy.x], answer: () => ITEMS[order[cur]].r, target: (r) => r === 'none' ? [noneBox.x + noneBox.w / 2, noneBox.y + noneBox.h / 2] : r === 'dl' ? [vx, vy + vry * 0.62 * 0.7] : r === 'ml' ? [vx - vrx * 0.5, vy + vry * 0.2] : [vx - vrx * 0.85, vy], done: () => cur };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
