// The labelling task: name chips wait in a tray at the bottom of the stage; numbered markers sit
// on the structures. Drag a chip onto its structure and it snaps in place as a label with a
// leader; drop it on the wrong one and it springs back while the teacher explains the mix-up.
import { THREE } from '../engine.js';

export function createLabelQuiz(ctx, items, opts = {}) {
  const { stage, camera, ui } = ctx;
  const layer = document.createElement('div'); layer.className = 'bh-quiz';
  const tray = document.createElement('div'); tray.className = 'bh-quiz-tray';
  layer.appendChild(tray);
  ui.root.appendChild(layer);
  const v = new THREE.Vector3();
  const markers = items.map((it, i) => {
    const m = document.createElement('div'); m.className = 'bh-quiz-dot'; m.textContent = String(i + 1);
    layer.appendChild(m);
    return { ...it, el: m, sx: 0, sy: 0, done: false, visible: true };
  });
  const order = items.map((_, i) => i).sort(() => Math.random() - 0.5);
  let placed = 0; let finished = false;
  const chips = order.map((i) => {
    const it = items[i];
    const c = document.createElement('button'); c.type = 'button'; c.className = 'bh-chip'; c.textContent = it.name;
    tray.appendChild(c);
    let drag = null;
    c.addEventListener('pointerdown', (e) => {
      if (c.classList.contains('placed')) return;
      e.preventDefault(); e.stopPropagation();
      c.setPointerCapture(e.pointerId);
      const r = c.getBoundingClientRect(); const sr = stage.getBoundingClientRect();
      drag = { ox: e.clientX - r.left, oy: e.clientY - r.top, sr };
      c.classList.add('dragging');
      c.style.left = `${r.left - sr.left}px`; c.style.top = `${r.top - sr.top}px`; c.style.width = `${r.width}px`;
      layer.appendChild(c);
      ctx.sfx.play('pick');
    });
    c.addEventListener('pointermove', (e) => {
      if (!drag) return;
      c.style.left = `${e.clientX - drag.sr.left - drag.ox}px`; c.style.top = `${e.clientY - drag.sr.top - drag.oy}px`;
      const near = nearest(e.clientX - drag.sr.left, e.clientY - drag.sr.top);
      markers.forEach((m) => m.el.classList.toggle('near', m === near));
    });
    const end = (e) => {
      if (!drag) return;
      const x = e.clientX - drag.sr.left; const y = e.clientY - drag.sr.top;
      drag = null; c.classList.remove('dragging');
      markers.forEach((m) => m.el.classList.remove('near'));
      const m = nearest(x, y);
      if (m && m.name === it.name) {
        m.done = true; m.chip = c; c.classList.add('placed'); m.el.classList.add('done');
        placed += 1; ctx.sfx.play('place');
        ctx.say(it.fact || `<b>${it.name}</b> — correct.`, 'good', 4200);
        if (opts.onPlace) opts.onPlace(it, placed, items.length);
        if (placed === items.length && !finished) { finished = true; if (opts.onDone) opts.onDone(); }
      } else {
        c.removeAttribute('style'); tray.appendChild(c);
        if (m) {
          const wrong = m.name;
          ctx.mistake(it.confuse && it.confuse[wrong] ? it.confuse[wrong] : `That marker is not the <b>${it.name}</b>. ${it.where || ''}`, 3);
        }
      }
    };
    c.addEventListener('pointerup', end); c.addEventListener('pointercancel', end);
    return c;
  });
  function nearest(x, y) {
    let best = null; let bd = opts.radius || 46;
    markers.forEach((m) => { if (m.done || !m.visible) return; const d = Math.hypot(m.sx - x, m.sy - y); if (d < bd) { bd = d; best = m; } });
    return best;
  }
  return {
    update() {
      const w = stage.clientWidth; const h = stage.clientHeight;
      for (let i = 0; i < markers.length; i++) {
        const m = markers[i];
        v.copy(m.at); if (m.object) m.object.localToWorld(v);
        v.project(camera);
        m.visible = v.z < 1;
        m.sx = (v.x + 1) / 2 * w; m.sy = (1 - v.y) / 2 * h;
        m.el.style.transform = `translate(${m.sx}px, ${m.sy}px)`;
        if (m.done && m.chip) m.chip.style.transform = `translate(${m.sx}px, ${m.sy}px)`;
      }
    },
    get done() { return finished; },
    dispose() { layer.remove(); void chips; },
  };
}
