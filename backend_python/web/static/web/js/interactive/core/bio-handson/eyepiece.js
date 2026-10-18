// Looking down the eyepiece. A round field of view drawn from the specimen (cells in micrometres)
// at the true scale of the objective in use, with a working focus: the coarse and fine knobs
// move the stage, the image sharpens only within the objective's depth of field (about 30 µm
// at 4x, 8 µm at 10x, under 2 µm at 40x), and racking the stage up too far at high power drives
// the objective into the coverslip. The iris diaphragm sets brightness and contrast. Drag the
// field to move the slide; tap a cell to examine it.
import { sfx } from './sound.js';

const FIELD_NUMBER = 13000; // µm: a school 10x eyepiece
const OBJ = {
  4: { dof: 30, offset: -6, wd: 17000, color: '#dc2626' },
  10: { dof: 8, offset: 0, wd: 6000, color: '#eab308' },
  40: { dof: 1.8, offset: 2.5, wd: 550, color: '#2563eb' },
};

function el(tag, cls, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; }

function makeKnob(label, cls, onTurn) {
  const wrap = el('div', `bh-knob ${cls}`);
  wrap.innerHTML = `<div class="bh-knob-dial"><i></i></div><span>${label}</span>`;
  const dial = wrap.querySelector('.bh-knob-dial');
  let drag = null; let angle = 0;
  dial.addEventListener('pointerdown', (e) => { e.preventDefault(); e.stopPropagation(); dial.setPointerCapture(e.pointerId); drag = { y: e.clientY, x: e.clientX }; wrap.classList.add('turning'); });
  dial.addEventListener('pointermove', (e) => {
    if (!drag) return;
    const dy = (drag.y - e.clientY) + (e.clientX - drag.x) * 0.5; drag.y = e.clientY; drag.x = e.clientX;
    if (!dy) return;
    angle += dy * 2.2; dial.style.transform = `rotate(${angle}deg)`;
    onTurn(dy);
  });
  const end = () => { drag = null; wrap.classList.remove('turning'); };
  dial.addEventListener('pointerup', end); dial.addEventListener('pointercancel', end);
  dial.addEventListener('wheel', (e) => { e.preventDefault(); const dy = e.deltaY > 0 ? -6 : 6; angle += dy * 2.2; dial.style.transform = `rotate(${angle}deg)`; onTurn(dy); }, { passive: false });
  return wrap;
}

/**
 * field: { width, height, draw(g, view), hit(x, y), animated, start: {x, y}, mount: {bubbles, thick} }
 * opts: { objective, focus, light, onTap(item, ev), onChange(state), onMistake(text, penalty), onClose }
 */
export function createEyepiece(ctx, field, opts = {}) {
  const { stage } = ctx;
  const overlay = el('div', 'bh-eye');
  overlay.innerHTML = '<div class="bh-eye-view"><canvas></canvas><div class="bh-eye-glare"></div><div class="bh-eye-crack"></div><div class="bh-eye-marks"></div></div><div class="bh-eye-ctrl"></div><div class="bh-eye-mag"></div>';
  ctx.ui.root.appendChild(overlay);
  const view = overlay.querySelector('.bh-eye-view');
  const canvas = view.querySelector('canvas');
  const g = canvas.getContext('2d');
  const marks = view.querySelector('.bh-eye-marks');
  const ctrl = overlay.querySelector('.bh-eye-ctrl');
  const magTag = overlay.querySelector('.bh-eye-mag');
  const crack = view.querySelector('.bh-eye-crack');

  const st = {
    objective: opts.objective || 10,
    focus: opts.focus ?? -900, // µm of stage travel from the in-focus position (negative = too low)
    light: opts.light ?? 0.55,
    cx: field.start ? field.start.x : field.width / 2,
    cy: field.start ? field.start.y : field.height / 2,
    cracked: false,
    coarseAtHigh: 0,
  };
  let D = 300; let dpr = 1; let dirty = true; let lastDraw = 0; let disposed = false;

  // controls: nosepiece, coarse and fine knobs, diaphragm, back
  const turret = el('div', 'bh-turret');
  Object.keys(OBJ).forEach((m) => {
    const b = el('button', 'bh-obj', `<i style="background:${OBJ[m].color}"></i>${m}×`); b.type = 'button'; b.dataset.mag = m;
    b.addEventListener('click', () => api.setObjective(Number(m), true));
    turret.appendChild(b);
  });
  const knobs = el('div', 'bh-knobs');
  knobs.appendChild(makeKnob('Coarse', 'coarse', (d) => turn(d, 22)));
  knobs.appendChild(makeKnob('Fine', 'fine', (d) => turn(d, 0.45)));
  const lightRow = el('label', 'bh-light', '<span>Diaphragm</span><input type="range" min="0" max="100" value="55">');
  const lightInput = lightRow.querySelector('input');
  lightInput.value = String(Math.round(st.light * 100));
  lightInput.addEventListener('input', () => { st.light = Number(lightInput.value) / 100; applyFilter(); changed(); });
  const back = el('button', 'bh-eye-back', '<span>Look up</span>'); back.type = 'button';
  back.addEventListener('click', () => { if (opts.onClose) opts.onClose(); });
  ctrl.append(turret, knobs, lightRow, back);
  if (opts.closable === false) back.style.display = 'none';

  function blurPx() {
    const o = OBJ[st.objective];
    const err = Math.abs(st.focus - o.offset);
    const b = Math.pow(err / o.dof, 0.85) * 0.9;
    return Math.min(16, Math.max(0, b - 0.25)) * (D / 420);
  }
  function applyFilter() {
    const b = blurPx();
    const L = st.light;
    const thick = field.mount && field.mount.thick ? field.mount.thick : 0;
    const bright = 0.35 + L * 1.05 - thick * 0.25;
    const contrast = 1.35 - L * 0.55 + thick * 0.1;
    canvas.style.filter = `blur(${b.toFixed(2)}px) brightness(${bright.toFixed(3)}) contrast(${contrast.toFixed(3)}) saturate(${(1.1 - L * 0.25).toFixed(3)})`;
  }
  function turn(d, perPx) {
    if (st.cracked) return;
    const before = st.focus;
    st.focus += d * perPx;
    if (perPx > 1 && st.objective === 40) {
      st.coarseAtHigh += Math.abs(d);
      if (st.coarseAtHigh > 14 && opts.onMistake) { st.coarseAtHigh = -1e9; opts.onMistake('At 40× use only the <b>fine</b> adjustment. The coarse knob moves the stage too far for the tiny working distance of the high-power objective.', 3); }
    }
    const wd = OBJ[st.objective].wd;
    if (st.focus > wd * 0.5) {
      st.focus = wd * 0.5;
      if (st.objective === 40 && !st.cracked) {
        st.cracked = true; crack.classList.add('show'); sfx.play('bad');
        if (opts.onMistake) opts.onMistake('Crunch — the 40× objective was driven into the coverslip and cracked it. Always focus at high power by lowering the stage, with the fine knob.', 8);
        setTimeout(() => { st.cracked = false; crack.classList.remove('show'); st.focus = -60; applyFilter(); changed(); }, 2600);
      }
    }
    if (Math.floor(before / 4) !== Math.floor(st.focus / 4)) sfx.play('knob');
    if (opts.onFocus) opts.onFocus(st.focus - before);
    applyFilter(); changed();
  }
  function changed() { if (opts.onChange) opts.onChange(api.state); }

  function layout() {
    const w = stage.clientWidth; const h = stage.clientHeight;
    const narrow = w < 640 || w < h;
    overlay.classList.toggle('narrow', narrow);
    const ctrlSpace = narrow ? 150 : 0; const side = narrow ? 0 : 230;
    D = Math.max(160, Math.min(w - side - 24, h - ctrlSpace - (narrow ? 72 : 84)));
    dpr = Math.min(window.devicePixelRatio || 1, ctx.low ? 1 : 2);
    view.style.width = `${D}px`; view.style.height = `${D}px`;
    canvas.width = Math.round(D * dpr); canvas.height = Math.round(D * dpr);
    canvas.style.width = `${D}px`; canvas.style.height = `${D}px`;
    dirty = true; applyFilter();
  }
  const scale = () => (D / (FIELD_NUMBER / st.objective)); // px per µm

  // drag to move the slide; tap to examine
  let pan = null;
  view.addEventListener('pointerdown', (e) => {
    e.preventDefault(); view.setPointerCapture(e.pointerId);
    pan = { x: e.clientX, y: e.clientY, moved: 0 };
  });
  view.addEventListener('pointermove', (e) => {
    if (!pan) return;
    const dx = e.clientX - pan.x; const dy = e.clientY - pan.y; pan.x = e.clientX; pan.y = e.clientY; pan.moved += Math.abs(dx) + Math.abs(dy);
    const s = scale();
    st.cx = Math.max(0, Math.min(field.width, st.cx - dx / s)); st.cy = Math.max(0, Math.min(field.height, st.cy - dy / s));
    dirty = true; changed();
  });
  const endPan = (e) => {
    if (!pan) return;
    const tap = pan.moved < 8; pan = null;
    if (tap && opts.onTap) {
      const r = view.getBoundingClientRect();
      const px = e.clientX - r.left; const py = e.clientY - r.top;
      if (Math.hypot(px - D / 2, py - D / 2) > D / 2) return;
      const s = scale();
      const x = st.cx + (px - D / 2) / s; const y = st.cy + (py - D / 2) / s;
      opts.onTap(field.hit ? field.hit(x, y, st) : null, { px, py, x, y, blur: blurPx() });
    }
  };
  view.addEventListener('pointerup', endPan); view.addEventListener('pointercancel', endPan);
  view.addEventListener('wheel', (e) => { e.preventDefault(); turn(e.deltaY > 0 ? -3 : 3, 0.45); }, { passive: false });

  function draw(t) {
    const w = canvas.width; const h = canvas.height; const s = scale() * dpr;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.fillStyle = field.background || '#f3eee2'; g.fillRect(0, 0, w, h);
    g.setTransform(s, 0, 0, s, w / 2 - st.cx * s, h / 2 - st.cy * s);
    field.draw(g, { cx: st.cx, cy: st.cy, scale: s, halfW: w / 2 / s, halfH: h / 2 / s, t, mag: st.objective * 10, objective: st.objective, dpr });
    g.setTransform(1, 0, 0, 1, 0, 0);
    // the edge of the field stop, uneven illumination and dust on the eyepiece lens
    const gr = g.createRadialGradient(w / 2, h / 2, w * 0.3, w / 2, h / 2, w * 0.5);
    gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(0.86, 'rgba(40,30,20,0.18)'); gr.addColorStop(1, 'rgba(0,0,0,0.85)');
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
  }
  const api = {
    el: overlay, view,
    get state() { return { objective: st.objective, focus: st.focus, light: st.light, cx: st.cx, cy: st.cy, blur: blurPx(), sharp: blurPx() < 0.9 * (D / 420), D, scale: scale() }; },
    setObjective(m, user) {
      if (st.objective === m) return;
      const prev = st.objective; st.objective = m;
      overlay.querySelectorAll('.bh-obj').forEach((b) => b.classList.toggle('active', Number(b.dataset.mag) === m));
      magTag.innerHTML = `<b>${m * 10}×</b> total · ${m}× objective · 10× eyepiece`;
      sfx.play('click'); st.coarseAtHigh = 0;
      dirty = true; applyFilter();
      if (opts.onObjective) opts.onObjective(m, prev, user);
      changed();
    },
    setFocus(f) { st.focus = f; applyFilter(); },
    redraw() { dirty = true; },
    /** Screen position (px inside the view) of a field point, for markers. */
    toView(x, y) { const s = scale(); return { x: D / 2 + (x - st.cx) * s, y: D / 2 + (y - st.cy) * s }; },
    mark(x, y, text, cls = '') {
      const m = el('div', `bh-eye-mark ${cls}`, text ? `<span>${text}</span>` : ''); m.dataset.x = x; m.dataset.y = y; marks.appendChild(m); placeMarks(); return m;
    },
    clearMarks() { marks.innerHTML = ''; },
    centerOn(x, y) { st.cx = x; st.cy = y; dirty = true; },
    update(t) {
      if (disposed) return;
      if (dirty || (field.animated && t - lastDraw > (ctx.low ? 0.066 : 0.033))) { dirty = false; lastDraw = t; draw(t); placeMarks(); }
    },
    show(v) { overlay.classList.toggle('show', v); if (v) { layout(); } },
    dispose() { disposed = true; window.removeEventListener('resize', layout); overlay.remove(); },
  };
  function placeMarks() {
    marks.querySelectorAll('.bh-eye-mark').forEach((m) => { const p = api.toView(Number(m.dataset.x), Number(m.dataset.y)); m.style.transform = `translate(${p.x}px, ${p.y}px)`; });
  }
  window.addEventListener('resize', layout);
  const startObj = st.objective; st.objective = 0; api.setObjective(startObj, false);
  layout();
  return api;
}
