// The practical's interface: a step card with the teacher's instruction, a tool belt, the
// teacher's spoken feedback, the procedure checklist and score in the dock, and the result card.
import { createPanel } from '../sim-ui.js';
import { ICONS } from './icons.js';
import { sfx } from './sound.js';

function el(tag, cls, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; }
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export const TOOL_NAMES = {
  hand: 'Hand', scalpel: 'Scalpel', scissors: 'Fine scissors', forceps: 'Forceps', needle: 'Needle', pin: 'Pins', dropper: 'Dropper',
  coverslip: 'Coverslip', brush: 'Brush', lens: 'Hand lens', razor: 'Razor', paper: 'Paper', washbottle: 'Wash bottle', slide: 'Slide', lamp: 'Spirit lamp', tube: 'Test tube',
};

export function createUI(stage, opts) {
  stage.classList.add('bh-stage');
  const root = el('div', 'bh-overlay');
  stage.appendChild(root);

  const card = el('div', 'bh-card');
  card.innerHTML = '<div class="bh-card-top"><span class="bh-card-n"></span><span class="bh-card-title"></span></div><div class="bh-card-text"></div><div class="bh-card-bar"><i></i></div>';
  root.appendChild(card);
  const cardN = card.querySelector('.bh-card-n'); const cardTitle = card.querySelector('.bh-card-title');
  const cardText = card.querySelector('.bh-card-text'); const bar = card.querySelector('.bh-card-bar'); const barFill = bar.querySelector('i');

  card.addEventListener('click', () => card.classList.toggle('bh-collapsed'));
  const toast = el('div', 'bh-toast');
  toast.innerHTML = `<span class="bh-toast-ico">${ICONS.teacher}</span><span class="bh-toast-text"></span>`;
  root.appendChild(toast);
  const toastText = toast.querySelector('.bh-toast-text');
  let toastTimer = 0;

  const belt = el('div', 'bh-belt');
  root.appendChild(belt);
  const toolButtons = new Map();
  let activeTool = null;
  let onToolChange = null;

  // the dock: procedure, score, sound
  const panel = createPanel(stage, { title: opts.title, compact: true, collapseOnMobile: false });
  panel.info(opts.aim);
  const scoreRow = el('div', 'bh-score-row');
  scoreRow.innerHTML = '<div><b class="bh-score">100</b><span>score</span></div><div><b class="bh-mistakes">0</b><span>mistakes</span></div><div><b class="bh-time">0:00</b><span>time</span></div>';
  panel.body.appendChild(scoreRow);
  const ctrlRow = el('div', 'bh-ctrl-row');
  const btnHint = el('button', 'bh-mini', `${ICONS.hint}<span>Hint</span>`);
  const btnSound = el('button', 'bh-mini', `${ICONS.mute}<span>Sound off</span>`);
  const btnRestart = el('button', 'bh-mini', `${ICONS.restart}<span>Restart</span>`);
  [btnHint, btnSound, btnRestart].forEach((b) => { b.type = 'button'; ctrlRow.appendChild(b); });
  panel.body.appendChild(ctrlRow);
  panel.section('Procedure');
  const list = el('ol', 'bh-steps');
  panel.body.appendChild(list);
  const obsTitle = el('div', 'ix-ctrl-section bh-obs-title', 'Observations');
  const obs = el('div', 'bh-obs');
  panel.body.appendChild(obsTitle); panel.body.appendChild(obs);
  obsTitle.style.display = 'none';

  btnSound.addEventListener('click', () => {
    sfx.setMuted(!sfx.muted);
    btnSound.innerHTML = sfx.muted ? `${ICONS.mute}<span>Sound off</span>` : `${ICONS.sound}<span>Sound on</span>`;
    sfx.play('click');
  });

  const api = {
    root, panel,
    setSteps(steps) {
      list.innerHTML = '';
      steps.forEach((s, i) => { const li = el('li', 'bh-step-item', `<span class="bh-step-dot">${i + 1}</span><span>${esc(s.title)}</span>`); list.appendChild(li); });
    },
    setStep(i, total, step) {
      cardN.textContent = `Step ${i + 1} of ${total}`;
      cardTitle.textContent = step.title;
      cardText.innerHTML = step.text || '';
      card.classList.remove('bh-pop', 'bh-collapsed'); void card.offsetWidth; card.classList.add('bh-pop');
      [...list.children].forEach((li, k) => { li.classList.toggle('current', k === i); li.classList.toggle('done', k < i); });
      api.progress(null);
    },
    setText(html) { cardText.innerHTML = html; },
    progress(p) { if (p === null || p === undefined) { bar.style.display = 'none'; return; } bar.style.display = ''; barFill.style.transform = `scaleX(${Math.max(0, Math.min(1, p))})`; },
    markAllDone() { [...list.children].forEach((li) => { li.classList.remove('current'); li.classList.add('done'); }); },
    say(text, kind = 'info', ms = 4200) {
      toastText.innerHTML = text;
      toast.className = `bh-toast show ${kind}`;
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove('show'), ms);
    },
    hideToast() { toast.classList.remove('show'); },
    setTools(ids) {
      belt.innerHTML = ''; toolButtons.clear();
      ids.forEach((id) => {
        const b = el('button', 'bh-tool', `${ICONS[id] || ICONS.hand}<span>${TOOL_NAMES[id] || id}</span>`);
        b.type = 'button'; b.dataset.tool = id;
        b.addEventListener('click', () => api.selectTool(activeTool === id && id !== 'hand' ? 'hand' : id, true));
        belt.appendChild(b); toolButtons.set(id, b);
      });
      belt.style.display = ids.length ? '' : 'none';
    },
    selectTool(id, user = false) {
      if (activeTool === id) return;
      activeTool = id;
      toolButtons.forEach((b, k) => { b.classList.toggle('active', k === id); if (k === id) b.classList.remove('glow'); });
      if (user) sfx.play('pick');
      if (onToolChange) onToolChange(id, user);
    },
    get tool() { return activeTool; },
    collapseCard(v) { card.classList.toggle('bh-collapsed', v); },
    showBelt(v) { belt.classList.toggle('bh-hidden', !v); },
    onTool(fn) { onToolChange = fn; },
    glowTool(id, on = true) { const b = toolButtons.get(id); if (b) b.classList.toggle('glow', on && activeTool !== id); },
    setScore(score, mistakes) { scoreRow.querySelector('.bh-score').textContent = Math.round(score); scoreRow.querySelector('.bh-mistakes').textContent = mistakes; },
    setTime(sec) { const m = Math.floor(sec / 60); const s = Math.floor(sec % 60); scoreRow.querySelector('.bh-time').textContent = `${m}:${s < 10 ? '0' : ''}${s}`; },
    observe(label, value) {
      obsTitle.style.display = '';
      let row = [...obs.children].find((r) => r.dataset.k === label);
      if (!row) { row = el('div', 'bh-obs-row'); row.dataset.k = label; obs.appendChild(row); }
      row.innerHTML = `<span>${esc(label)}</span><b>${value}</b>`;
    },
    clearObservations() { obs.innerHTML = ''; obsTitle.style.display = 'none'; },
    onHint(fn) { btnHint.addEventListener('click', fn); },
    onRestart(fn) { btnRestart.addEventListener('click', fn); },
    showResult({ title, score, stars, rows, conclusion, onRedo, onExplore }) {
      const box = el('div', 'bh-result');
      const st = [1, 2, 3].map((k) => `<i class="${k <= stars ? 'on' : ''}">★</i>`).join('');
      box.innerHTML = `<div class="bh-result-card"><div class="bh-stars">${st}</div><h3>${esc(title)}</h3><div class="bh-result-score">${Math.round(score)}<small>/100</small></div>
        <table>${rows.map((r) => `<tr><td>${esc(r[0])}</td><td>${r[1]}</td></tr>`).join('')}</table>
        <p class="bh-conclusion">${conclusion}</p>
        <div class="bh-result-btns"><button type="button" class="bh-btn ghost" data-a="explore">Explore freely</button><button type="button" class="bh-btn" data-a="redo">Do it again</button></div></div>`;
      root.appendChild(box);
      requestAnimationFrame(() => box.classList.add('show'));
      box.querySelector('[data-a=redo]').addEventListener('click', () => { box.remove(); onRedo && onRedo(); });
      box.querySelector('[data-a=explore]').addEventListener('click', () => { box.remove(); onExplore && onExplore(); });
      return box;
    },
    /** A small chooser at (x, y) in stage pixels; calls back with the chosen value. */
    choose(x, y, title, options, cb) {
      root.querySelectorAll('.bh-pick').forEach((n) => n.remove());
      const box = el('div', 'bh-pick', `<b>${esc(title)}</b>`);
      options.forEach((o) => { const b = el('button', '', esc(o.label)); b.type = 'button'; b.addEventListener('click', (e) => { e.stopPropagation(); box.remove(); cb(o.value); }); box.appendChild(b); });
      const x2 = document.createElement('button'); x2.type = 'button'; x2.textContent = '✕'; x2.addEventListener('click', () => box.remove()); box.appendChild(x2);
      root.appendChild(box);
      const w = stage.clientWidth; const h = stage.clientHeight;
      const bw = Math.min(250, w - 16); box.style.left = `${Math.max(8, Math.min(w - bw - 8, x - bw / 2))}px`;
      box.style.top = `${Math.max(8, Math.min(h - box.offsetHeight - 8, y + 18))}px`;
      return box;
    },
    /** Pick any number of options, then Done. */
    chooseMany(x, y, title, options, cb) {
      root.querySelectorAll('.bh-pick').forEach((n) => n.remove());
      const box = el('div', 'bh-pick bh-pick-many', `<b>${esc(title)}</b>`); const picked = new Set();
      options.forEach((o) => { const b = el('button', '', esc(o.label)); b.type = 'button'; b.addEventListener('click', (e) => { e.stopPropagation(); if (picked.has(o.value)) { picked.delete(o.value); b.classList.remove('on'); } else { picked.add(o.value); b.classList.add('on'); } }); box.appendChild(b); });
      const done = el('button', 'bh-pick-done', 'Done'); done.type = 'button'; done.addEventListener('click', () => { box.remove(); cb([...picked]); }); box.appendChild(done);
      root.appendChild(box);
      const w = stage.clientWidth; const h = stage.clientHeight; const bw = Math.min(250, w - 16);
      box.style.left = `${Math.max(8, Math.min(w - bw - 8, x - bw / 2))}px`; box.style.top = `${Math.max(8, Math.min(h - box.offsetHeight - 8, y + 18))}px`;
      return box;
    },
    clearChooser() { root.querySelectorAll('.bh-pick').forEach((n) => n.remove()); },
    clearResult() { root.querySelectorAll('.bh-result').forEach((n) => n.remove()); },
    dispose() { clearTimeout(toastTimer); root.remove(); panel.dispose(); stage.classList.remove('bh-stage'); },
  };
  return api;
}
