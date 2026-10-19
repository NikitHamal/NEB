// On-stage controls for the physics and chemistry practicals: a bar of action buttons above the
// scene's bottom edge, floating chips pinned to points in 3D (a reading beside a meniscus, a
// stopwatch face), and a screen-space picker with generous touch targets.
import { THREE } from '../engine.js';

function el(tag, cls, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; }

export function createHud(ctx) {
  const root = el('div', 'ho-hud');
  ctx.ui.root.appendChild(root);
  const bar = el('div', 'ho-actions');
  root.appendChild(bar);
  const chips = [];
  const v = new THREE.Vector3();
  const api = {
    root,
    /** buttons: [{ id, label, primary, onClick, disabled }] */
    actions(buttons) {
      bar.innerHTML = '';
      (buttons || []).forEach((b) => {
        const n = el('button', `ho-act${b.primary ? ' primary' : ''}`, b.label); n.type = 'button'; n.dataset.id = b.id || b.label;
        if (b.disabled) n.disabled = true;
        n.addEventListener('click', (e) => { e.stopPropagation(); if (!n.disabled) b.onClick && b.onClick(); });
        bar.appendChild(n);
      });
      bar.classList.toggle('show', !!(buttons && buttons.length));
    },
    enable(id, on) { const n = bar.querySelector(`[data-id="${id}"]`); if (n) n.disabled = !on; },
    relabel(id, label) { const n = bar.querySelector(`[data-id="${id}"]`); if (n) n.innerHTML = label; },
    /** A chip that follows a world point each frame. */
    chip(cls = '') {
      const n = el('div', `ho-chip ${cls}`); root.appendChild(n);
      const c = { el: n, at: new THREE.Vector3(), visible: false, dx: 0, dy: 0 };
      c.set = (html) => { if (n.__h !== html) { n.innerHTML = html; n.__h = html; } return c; };
      c.show = (on) => { c.visible = on; n.classList.toggle('show', on); return c; };
      c.remove = () => { n.remove(); const i = chips.indexOf(c); if (i >= 0) chips.splice(i, 1); };
      chips.push(c);
      return c;
    },
    update() {
      if (!chips.length) return;
      const w = ctx.stage.clientWidth; const h = ctx.stage.clientHeight;
      for (const c of chips) {
        if (!c.visible) continue;
        ctx.input.project(c.at, v, w, h);
        const off = v.z > 1 || v.x < -30 || v.x > w + 30 || v.y < -30 || v.y > h + 30;
        if (off !== !!c.off) { c.off = off; c.el.style.visibility = off ? 'hidden' : ''; }
        if (off) continue;
        const x = Math.max(4, Math.min(w - c.el.offsetWidth - 4, v.x + c.dx)); const y = Math.max(4, Math.min(h - c.el.offsetHeight - 4, v.y + c.dy));
        c.el.style.transform = `translate(${Math.round(x)}px, ${Math.round(y)}px)`;
      }
    },
    clear() { bar.innerHTML = ''; bar.classList.remove('show'); chips.splice(0).forEach((c) => c.el.remove()); },
    dispose() { root.remove(); },
  };
  return api;
}

const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3();
/** Screen distance in px from the pointer to an object's (or point's) projection. */
export function screenDist(ctx, target, p, offsetY = 0) {
  if (target.isObject3D) target.getWorldPosition(tmp); else tmp.copy(target);
  tmp.y += offsetY;
  ctx.input.project(tmp, tmp2, ctx.stage.clientWidth, ctx.stage.clientHeight);
  return Math.hypot(tmp2.x - p.x, tmp2.y - p.y);
}
/** Screen position of a world point. */
export function toScreen(ctx, target, out) {
  if (target.isObject3D) target.getWorldPosition(tmp); else tmp.copy(target);
  return ctx.input.project(tmp, out, ctx.stage.clientWidth, ctx.stage.clientHeight);
}
/** True if the pointer is over the object or within radius px of its anchor. */
export function hits(ctx, obj, p, radius = 46, offsetY = 0) {
  if (ctx.input.pick([obj])) return true;
  return screenDist(ctx, obj, p, offsetY) < radius * (p.touch ? 1.35 : 1);
}
