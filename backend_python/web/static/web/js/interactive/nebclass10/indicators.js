/**
 * Indicators (NEB class 10) — a rack of household solutions. Drag a strip of red or blue litmus
 * paper, or a dropper of phenolphthalein, methyl orange or universal indicator, onto a tube and
 * watch the colour change; every result fills the observation table. Dilute NaOH and HCl droppers
 * neutralise a tube drop by drop (each drop is 0.05 mL of 0.1 M into 5 mL), and universal
 * indicator follows the pH through green at 7.
 */
import { createKit, T, fmt, clamp, background, text, pill, withAlpha } from '../core/kit2d.js';
import { createShelf } from '../core/chem2d.js';
import { createRack } from '../core/tubes2d.js';
import { INDICATORS, litmusPaper, drawPHStrip } from '../core/indicators2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SOL = [
  { name: 'Lemon juice', short: 'Lemon', pH: 2.2, base: '#fbf3c4' },
  { name: 'Vinegar', short: 'Vinegar', pH: 2.9, base: '#f6efd9' },
  { name: 'Curd (dahi) water', short: 'Curd', pH: 4.5, base: '#f8f6ef' },
  { name: 'Common salt solution', short: 'Salt', pH: 7.0, base: '#eef4fb' },
  { name: 'Baking soda solution', short: 'Soda', pH: 8.3, base: '#eef4fb' },
  { name: 'Soap solution', short: 'Soap', pH: 10.0, base: '#f1f1f4' },
  { name: 'Milk of magnesia', short: 'Mg(OH)₂', pH: 10.5, base: '#f8fafc' },
  { name: 'Lime water', short: 'Lime w.', pH: 12.4, base: '#f1f7fd' },
];
const REAG = [
  { id: 'red', label: 'Red litmus', kind: 'object', color: '#e8596e' },
  { id: 'blue', label: 'Blue litmus', kind: 'object', color: '#4c6ef5' },
  { id: 'phenolphthalein', label: 'Phenolphth.', kind: 'object', color: '#f8fafc' },
  { id: 'methylorange', label: 'Methyl orange', kind: 'object', color: '#f76707' },
  { id: 'universal', label: 'Universal', kind: 'object', color: '#4caf50' },
  { id: 'naoh', label: 'NaOH (dil.)', kind: 'object', color: '#e2e8f0' },
  { id: 'hcl', label: 'HCl (dil.)', kind: 'object', color: '#e2e8f0' },
];
const KW = 1e-14;
const COLS = ['red', 'blue', 'phenolphthalein', 'methylorange', 'universal'];

export default function init(stage) {
  const k = createKit(stage, { label: 'A rack of test tubes with solutions, and indicators to test them' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag an indicator onto a test tube', T.blue);

  const rack = createRack(k, SOL.length);
  const state = SOL.map((s) => ({ c: excess(s.pH), ind: null, res: {} }));
  for (const r of REAG) r.draw = drawReagent;

  const panel = createPanel(stage, { title: 'Indicator tests' });
  panel.button({ label: 'Wash all the tubes', icon: 'water', variant: 'ghost', onClick: wash });
  const table = document.createElement('div'); table.className = 'k2-table k2-first6'; table.style.setProperty('--k2-cols', 6); table.style.fontSize = '.68rem'; panel.body.appendChild(table);
  const verdict = panel.readout({ label: 'Last test', value: '—' });
  panel.info('Acids turn blue litmus red; bases turn red litmus blue. Phenolphthalein is colourless in acid and pink in base; methyl orange is red in acid and yellow in base. Universal indicator shows the whole pH scale. Acid + base → salt + water.');

  function excess(pH) { return Math.pow(10, -pH) - Math.pow(10, pH - 14); }
  function pHof(c) { const h = (c + Math.sqrt(c * c + 4 * KW)) / 2; return -Math.log10(h); }
  function wash() { SOL.forEach((s, i) => { state[i].c = excess(s.pH); state[i].ind = null; rack.tubes[i].paper = null; rack.setColor(i, s.base, 0.55, true); }); k.animate(true); }
  function tubeColor(i) {
    const st = state[i], p = pHof(st.c);
    if (!st.ind) return [SOL[i].base, 0.55];
    const I = INDICATORS[st.ind], a = I.alpha(p);
    return a < 0.05 ? [SOL[i].base, 0.55] : [I.color(p), Math.max(0.5, a)];
  }
  function renderTable() {
    const head = '<div class="k2-tr k2-th"><span>Solution</span><span>Red lit.</span><span>Blue lit.</span><span>Phen.</span><span>M.O.</span><span>pH</span></div>';
    table.innerHTML = head + SOL.map((s, i) => `<div class="k2-tr"><span>${s.short}</span>${COLS.map((c) => { const r = state[i].res[c]; return `<span>${r ? `<i style="display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;background:${r.color};box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)"></i>${c === 'universal' ? ' ' + fmt(r.pH, 0) : ''}` : '·'}</span>`; }).join('')}</div>`).join('');
  }

  function apply(item, i) {
    const st = state[i], t = rack.tubes[i], p = pHof(st.c);
    const name = SOL[i].name;
    if (item.id === 'red' || item.id === 'blue') {
      t.paper = item.id === 'red' ? '#e8596e' : '#4c6ef5';
      t.paperC = litmusPaper(item.id, p);
      t.glow.v = 8;
      const changed = t.paperC !== t.paper;
      st.res[item.id] = { color: t.paperC };
      verdict.set(`${item.label} in ${name}: ${changed ? (item.id === 'red' ? 'turns blue → base' : 'turns red → acid') : 'no change'}`);
    } else if (item.id === 'naoh' || item.id === 'hcl') {
      st.c += (item.id === 'naoh' ? -1 : 1) * 0.1 * 0.05 / 5 * 4;
      const np = pHof(st.c);
      verdict.set(`${item.id === 'naoh' ? 'Base' : 'Acid'} added to ${name}: pH is now ${fmt(np, 1)}${Math.abs(np - 7) < 0.6 ? ' — neutral! acid + base → salt + water' : ''}`);
      if (t.paper) t.paperC = litmusPaper(t.paper === '#e8596e' ? 'red' : 'blue', np);
    } else {
      st.ind = item.id;
      st.res[item.id] = { color: INDICATORS[item.id].alpha(p) < 0.05 ? '#ffffff' : INDICATORS[item.id].color(p), pH: p };
      verdict.set(`${INDICATORS[item.id].label} in ${name}: ${describe(item.id, p)}`);
    }
    const [c, a] = tubeColor(i); rack.setColor(i, c, a);
    renderTable();
    badge.set(verdict.el.querySelector('.ix-readout-value').textContent);
    k.animate(true);
  }
  function describe(id, p) {
    if (id === 'phenolphthalein') return p > 8.2 ? 'pink → base' : 'colourless → acid or neutral';
    if (id === 'methylorange') return p < 3.1 ? 'red → acid' : p > 4.4 ? 'yellow → neutral or base' : 'orange';
    return `pH ${fmt(p, 0)} → ${p < 6.5 ? 'acid' : p > 7.5 ? 'base' : 'neutral'}`;
  }

  const shelf = createShelf(k, REAG, {
    target: () => ({ x: -999, y: -999, w: 0 }), onPour: () => {},
    onDrop: (it, x, y) => { const i = rack.tubeAt(x, y + 30); if (i >= 0) apply(it, i); },
  });

  let stripY = 0, stripX = 0, stripW = 0;
  k.onResize((w, h) => {
    shelf.layout(6, 14, w - 12, k.small ? 70 : 86);
    rack.layout(k.small ? 4 : w * 0.04, k.small ? 110 : 130, k.small ? w - 8 : w * 0.92, k.small ? h - 200 : h - 250);
    stripX = k.small ? 20 : w * 0.15; stripW = k.small ? w - 40 : w * 0.7; stripY = h - (k.small ? 46 : 56);
  });

  k.frame((ctx, dt, w, h) => {
    const m1 = shelf.step(dt), m2 = rack.step(dt);
    background(k, ctx, w, h);
    ctx.fillStyle = '#c9a77a'; ctx.fillRect(0, shelf.slots[0].y, w, 6);
    rack.draw(ctx);
    for (let i = 0; i < SOL.length; i++) { rack.tubes[i].label = SOL[i].short; rack.tubes[i].sub = state[i].ind === 'universal' ? `pH ${fmt(pHof(state[i].c), 0)}` : ''; }
    shelf.draw(ctx);
    const held = shelf.held;
    if (held) { const i = rack.tubeAt(k.pointer.x, k.pointer.y + 30); if (i >= 0) { const t = rack.tubes[i]; ctx.strokeStyle = withAlpha(T.blue, 0.6); ctx.lineWidth = 2; ctx.setLineDash([4, 4]); ctx.strokeRect(t.x - rack.gap / 2 + 4, t.y - rack.h - 20, rack.gap - 8, rack.h + 50); ctx.setLineDash([]); } }
    drawPHStrip(ctx, stripX, stripY, stripW, 12, null, !k.small);
    text(ctx, 'acid', stripX, stripY + 34, T.red, 10, 700); text(ctx, 'neutral', stripX + stripW / 2, stripY + 34, T.green, 10, 700, 'center'); text(ctx, 'base', stripX + stripW, stripY + 34, T.purple, 10, 700, 'right');
    k.animate(m1 || m2);
  });

  wash(); renderTable();
  k.debug = { reagent: (j) => [shelf.slots[j].x, shelf.slots[j].y - 20], tube: (i) => [rack.tubes[i].x, rack.tubes[i].y - rack.h * 0.6], apply: (j, i) => apply(REAG[j], i), pH: (i) => pHof(state[i].c) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}

function drawReagent(ctx, it) {
  if (it.id === 'red' || it.id === 'blue') {
    ctx.fillStyle = it.color; ctx.fillRect(-5, -56, 10, 52); ctx.strokeStyle = 'rgba(0,0,0,0.15)'; ctx.strokeRect(-5, -56, 10, 52);
    return;
  }
  ctx.fillStyle = 'rgba(219,234,254,0.85)'; ctx.strokeStyle = 'rgba(100,130,170,0.8)'; ctx.lineWidth = 1.2;
  ctx.beginPath(); ctx.roundRect(-12, -36, 24, 34, 4); ctx.fill(); ctx.stroke();
  ctx.fillStyle = withAlpha(it.color, it.id === 'phenolphthalein' || it.id === 'naoh' || it.id === 'hcl' ? 0.5 : 0.85); ctx.fillRect(-10, -20, 20, 16);
  ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.roundRect(-6, -54, 12, 18, 5); ctx.fill();
  ctx.fillStyle = 'rgba(220,235,250,0.95)'; ctx.fillRect(-2, -66, 4, 13);
  if (it.id === 'universal') { const g = ['#e8432e', '#f2c12e', '#4caf50', '#2f6fbf', '#5b3aa8']; for (let i = 0; i < 5; i++) { ctx.fillStyle = g[i]; ctx.fillRect(-10 + i * 4, -20, 4, 16); } }
}
