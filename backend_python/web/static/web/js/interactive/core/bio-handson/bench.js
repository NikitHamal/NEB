// Shared bench kit for the field, physiology and genetics practicals: a time-lapse clock the
// student runs forward, a question asked until it is answered right, a notebook sheet on the stage
// for tables, keys, maps and Punnett squares, chips that are dragged (or tapped, then tapped on a
// slot) into place, floating name tags, and the common containers: beaker, jar, pot of soil,
// crucible, wooden tray and a bench rule.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture, ease, roundedSlab } from './kit.js';

function el(tag, cls, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; }
export const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

/**
 * A clock run forward in fixed jumps. unit: 'min' | 'h' | 'day'. onTick(t, settled) is called
 * through each jump (t eases from the old to the new time) and once more when it settles.
 */
export function timelapse(ctx, { step = 15, unit = 'min', label, onTick, dur = 1.2 }) {
  const b = el('div', 'bh-clock');
  const lbl = label || `+${step} ${unit === 'day' ? (step > 1 ? 'days' : 'day') : unit} ▶`;
  b.innerHTML = `<span class="bh-clock-face"><i></i></span><b>0 ${unit}</b><button type="button">${lbl}</button>`;
  ctx.ui.root.appendChild(b);
  const hand = b.querySelector('i'); const txt = b.querySelector('b'); const btn = b.querySelector('button');
  const per = unit === 'min' ? 6 : unit === 'h' ? 30 : 360 / 7;
  const name = (t) => (unit === 'day' ? `day ${Math.round(t)}` : unit === 'h' ? `${+t.toFixed(1)} h` : `${Math.round(t)} min`);
  let t = 0; let busy = false;
  const api = {
    el: b,
    get t() { return t; },
    get busy() { return busy; },
    advance(n = step, instant = false) {
      if (busy) return; const from = t; t += n; busy = true; btn.disabled = true; ctx.sfx.play('click');
      const set = (m) => { hand.style.transform = `rotate(${m * per}deg)`; txt.textContent = name(m); };
      if (instant) { set(t); onTick(t, false); busy = false; btn.disabled = false; onTick(t, true); return; }
      ctx.anim.add(dur, (k) => { const m = from + (t - from) * k; set(m); onTick(m, false); }, { ease: ease.inOut, done: () => { busy = false; btn.disabled = false; onTick(t, true); } });
    },
    enable(v) { btn.disabled = !v || busy; },
    show(v) { b.style.display = v ? '' : 'none'; },
    remove() { b.remove(); },
  };
  btn.addEventListener('click', () => api.advance());
  txt.textContent = name(0);
  return api;
}

/**
 * Ask a question until the right answer is chosen. right: a value or a predicate. ok: message (or
 * function returning one) said on the right answer; wrong: message or function(value).
 */
export function ask(ctx, title, options, right, { ok, wrong, penalty = 3, y = 0.12, delay = 0.6, then } = {}) {
  const isRight = typeof right === 'function' ? right : (v) => v === right;
  const opts = options.map((o) => (typeof o === 'string' ? { label: o, value: o } : o));
  const go = () => ctx.ui.choose(ctx.stage.clientWidth / 2, ctx.stage.clientHeight * y, title, opts, (v) => {
    if (isRight(v)) { const m = typeof ok === 'function' ? ok(v) : ok; if (then) { if (m) ctx.say(m, 'good', 4800); ctx.sfx.play('ok'); then(v); } else ctx.next(m); }
    else { ctx.mistake(typeof wrong === 'function' ? wrong(v) : (wrong || 'Not quite. Think again.'), penalty); ctx.anim.wait(0.4, go); }
  });
  ctx.anim.wait(delay, go);
}

/** A notebook sheet on the stage (right side on a desktop, bottom on a phone). */
export function sheet(ctx, { title = '', cls = '' } = {}) {
  const box = el('div', `bh-sheet ${cls}`, `<b class="bh-sheet-title">${title}</b><div class="bh-sheet-body"></div>`);
  ctx.ui.root.appendChild(box);
  const body = box.querySelector('.bh-sheet-body');
  requestAnimationFrame(() => box.classList.add('on'));
  return {
    el: box, body,
    title(t) { box.querySelector('.bh-sheet-title').innerHTML = t; },
    set(html) { body.innerHTML = html; return body; },
    show(v) { box.classList.toggle('on', v); },
    remove() { box.remove(); },
  };
}

/**
 * Drag-and-drop (or tap, then tap) chips into slots. chips: [{ id, html }]; slots: elements with
 * data-slot. accept(chipId, slotId, chipEl, slotEl) returns true to keep the chip there.
 */
export function chipDrop(ctx, tray, chips, slotRoot, accept) {
  let selected = null;
  const made = chips.map((c) => {
    const b = el('button', 'bh-dchip', c.html); b.type = 'button'; b.dataset.id = c.id; tray.appendChild(b);
    let drag = null;
    b.addEventListener('pointerdown', (e) => {
      if (b.classList.contains('placed')) return; e.preventDefault(); e.stopPropagation();
      b.setPointerCapture(e.pointerId); drag = { x: e.clientX, y: e.clientY, moved: 0 };
    });
    b.addEventListener('pointermove', (e) => {
      if (!drag) return; const dx = e.clientX - drag.x; const dy = e.clientY - drag.y; drag.moved = Math.max(drag.moved, Math.hypot(dx, dy));
      if (drag.moved > 6) { b.classList.add('dragging'); b.style.transform = `translate(${dx}px, ${dy}px)`; hover(e.clientX, e.clientY); }
    });
    const end = (e) => {
      if (!drag) return; const moved = drag.moved; drag = null; b.classList.remove('dragging'); b.style.transform = '';
      slotRoot.querySelectorAll('[data-slot].near').forEach((s) => s.classList.remove('near'));
      if (moved <= 6) { select(b); return; }
      const s = slotAt(e.clientX, e.clientY); if (s) drop(b, s);
    };
    b.addEventListener('pointerup', end); b.addEventListener('pointercancel', end);
    return b;
  });
  function select(b) { if (selected) selected.classList.remove('sel'); selected = selected === b ? null : b; if (selected) { selected.classList.add('sel'); ctx.sfx.play('pick'); } }
  function slotAt(x, y) { return [...slotRoot.querySelectorAll('[data-slot]')].find((s) => { const r = s.getBoundingClientRect(); return x >= r.left - 6 && x <= r.right + 6 && y >= r.top - 6 && y <= r.bottom + 6; }); }
  function hover(x, y) { const s = slotAt(x, y); slotRoot.querySelectorAll('[data-slot]').forEach((q) => q.classList.toggle('near', q === s)); }
  function drop(b, s) {
    if (accept(b.dataset.id, s.dataset.slot, b, s)) { ctx.sfx.play('place'); b.classList.add('placed'); b.classList.remove('sel'); if (selected === b) selected = null; }
  }
  const onSlot = (e) => { const s = e.target.closest('[data-slot]'); if (s && selected) { e.stopPropagation(); drop(selected, s); } };
  slotRoot.addEventListener('click', onSlot);
  return { chips: made, dispose() { slotRoot.removeEventListener('click', onSlot); } };
}

/** A floating name tag (sprite) for dishes, pots and sites. */
export function tag(text, { color = '#0f172a', bg = 'rgba(255,255,255,0.92)', h = 0.09 } = {}) {
  const tex = canvasTexture(`tag2:${text}:${color}`, 512, 96, (g, w, hh) => {
    g.font = '700 54px system-ui, sans-serif'; const tw = Math.min(w - 8, g.measureText(text).width + 44);
    g.fillStyle = bg; const x = (w - tw) / 2; g.beginPath(); g.roundRect ? g.roundRect(x, 8, tw, hh - 16, 30) : g.rect(x, 8, tw, hh - 16); g.fill();
    g.fillStyle = color; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, w / 2, hh / 2 + 2);
  });
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthWrite: false, transparent: true }));
  s.scale.set(h * 512 / 96, h, 1); s.renderOrder = 8; s.userData.noPick = true;
  return s;
}

const V2 = (x, y) => new THREE.Vector2(x, y);
/** A glass beaker (r, h in units) with a liquid whose level (0..1) and colour can change. */
export function glassBeaker(r = 0.3, h = 0.6, color = 0xdbeafe, level = 0) {
  const g = new THREE.Group();
  const shell = mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(r, 0), V2(r + 0.01, 0.015), V2(r + 0.01, h), V2(r + 0.03, h + 0.025)], 36), MAT.glass(), null, { cast: false });
  shell.renderOrder = 5; g.add(shell);
  const mat = new THREE.MeshPhysicalMaterial({ color, roughness: 0.08, transparent: true, opacity: 0.55, clearcoat: 1, depthWrite: false });
  const liq = mesh(new THREE.CylinderGeometry(r - 0.006, r - 0.006, 1, 32), mat, null, { cast: false }); liq.renderOrder = 4; g.add(liq);
  const api = { group: g, liquid: liq, material: mat, r, h, level: 0, setLevel(f) { api.level = f; liq.visible = f > 0.002; liq.scale.y = Math.max(0.001, f * (h - 0.02)); liq.position.y = 0.01 + liq.scale.y / 2; } };
  api.setLevel(level);
  return api;
}

/** A clay pot of soil, rim radius r. */
export function clayPot(r = 0.45, h = 0.6) {
  const g = new THREE.Group();
  const clay = new THREE.MeshStandardMaterial({ color: 0xb4532a, roughness: 0.85 });
  g.add(mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(r * 0.7, 0), V2(r, h * 0.92), V2(r * 1.08, h * 0.93), V2(r * 1.08, h), V2(r * 0.95, h), V2(r * 0.93, h * 0.94)], 32), clay));
  const soil = mesh(new THREE.CircleGeometry(r * 0.93, 32), new THREE.MeshStandardMaterial({ map: soilTexture(), roughness: 1 }), [0, h * 0.9, 0]);
  soil.rotation.x = -Math.PI / 2; g.add(soil);
  g.userData.top = h * 0.9;
  return g;
}
export function soilTexture(tint = '#4a3424') {
  return canvasTexture(`soil:${tint}`, 256, 256, (g, w, h) => {
    g.fillStyle = tint; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 2200; i++) { const v = Math.random(); g.fillStyle = v < 0.5 ? 'rgba(0,0,0,0.25)' : v < 0.85 ? 'rgba(120,90,60,0.35)' : 'rgba(200,180,150,0.3)'; g.fillRect(Math.random() * w, Math.random() * h, 1 + Math.random() * 3, 1 + Math.random() * 3); }
  });
}

/** A porcelain crucible (or evaporating dish) of radius r. */
export function crucible(r = 0.18) {
  const g = new THREE.Group();
  g.add(mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(r * 0.6, 0), V2(r, r * 0.9), V2(r * 1.05, r * 0.95)], 28), MAT.gloss(0xf8fafc)));
  const fill = mesh(new THREE.CircleGeometry(r * 0.88, 24), new THREE.MeshStandardMaterial({ map: soilTexture('#6b4a32'), roughness: 1 }), [0, r * 0.7, 0]);
  fill.rotation.x = -Math.PI / 2; fill.visible = false; g.add(fill); g.userData.fill = fill;
  return g;
}

/** A shallow wooden-rimmed white enamel tray. */
export function enamelTray(w = 1.4, d = 0.9) {
  const g = new THREE.Group();
  const m = MAT.gloss(0xf8fafc);
  g.add(mesh(roundedSlab(w, d, 0.02, 0.06), m));
  const rim = MAT.gloss(0x1e3a8a);
  [[w, 0.05, 0.02, 0, d / 2], [w, 0.05, 0.02, 0, -d / 2], [0.02, 0.05, d, w / 2, 0], [0.02, 0.05, d, -w / 2, 0]].forEach(([a, b, c, x, z]) => g.add(mesh(new THREE.BoxGeometry(a, b, c), rim, [x, 0.035, z])));
  return g;
}

/** A 30 cm bench rule lying flat, millimetre ticks on its top face. */
export function benchRule(len = 3.0) {
  const tex = canvasTexture(`rule:${len}`, 2048, 128, (g, w, h) => {
    g.fillStyle = '#f8f3dc'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827';
    const mm = len * 100; for (let i = 0; i <= mm; i++) { const x = 20 + (w - 40) * i / mm; const t = i % 10 === 0 ? 48 : i % 5 === 0 ? 34 : 20; g.fillRect(x - 1, 0, 2, t); if (i % 10 === 0) { g.font = '600 30px system-ui'; g.textAlign = 'center'; g.fillText(String(i / 10), x, 86); } }
  });
  const m = mesh(new THREE.BoxGeometry(len + 0.04, 0.012, 0.32), [MAT.gloss(0xf1e7c4), MAT.gloss(0xf1e7c4), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6 }), MAT.gloss(0xf1e7c4), MAT.gloss(0xf1e7c4), MAT.gloss(0xf1e7c4)]);
  return m;
}

/** Pick the object (among list) under the pointer, by ray or within radius px of its anchor. */
export function pickNear(ctx, list, p, radius = 40) {
  const h = ctx.input.pick(list.filter((o) => o.visible !== false), true);
  if (h) { let o = h.object; while (o && !list.includes(o)) o = o.parent; if (o) return o; }
  let best = null; let bd = radius * (p.touch ? 1.4 : 1); const v = new THREE.Vector3();
  const w = ctx.stage.clientWidth; const hh = ctx.stage.clientHeight;
  list.forEach((o) => { if (o.visible === false) return; o.getWorldPosition(v); ctx.input.project(v, v, w, hh); const d = Math.hypot(v.x - p.x, v.y - p.y); if (d < bd) { bd = d; best = o; } });
  return best;
}

/** Fly an object (in the world group) along an arc to a local position, then call done. */
export function flyTo(ctx, obj, to, { dur = 0.7, lift = 0.3, rot, done } = {}) {
  const from = obj.position.clone(); const r0 = obj.rotation.clone();
  ctx.anim.add(dur, (k) => {
    obj.position.lerpVectors(from, to, k); obj.position.y += Math.sin(Math.PI * k) * lift;
    if (rot) { obj.rotation.set(r0.x + (rot[0] - r0.x) * k, r0.y + (rot[1] - r0.y) * k, r0.z + (rot[2] - r0.z) * k); }
  }, { ease: ease.inOut, done });
}

/** A standard result-table HTML for the sheet. rows: arrays of cells; head: header cells. */
export function table(head, rows, cls = '') {
  return `<table class="bh-tab ${cls}"><tr>${head.map((h) => `<th>${h}</th>`).join('')}</tr>${rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('')}</table>`;
}

/**
 * Take the practical outdoors: hide the lab room's furniture (its lights stay on), open the sky and
 * push the haze back. Returns a function that brings the room back.
 */
export function outdoors(ctx, { sky = 0xbfdcf0, fogNear = 60, fogFar = 160 } = {}) {
  const { scene } = ctx;
  const room = scene.children.find((o) => o.isGroup && o !== ctx.world && o.children.length > 8);
  const hidden = [];
  if (room) room.traverse((o) => { if (o.isMesh && o.visible) { o.visible = false; hidden.push(o); } });
  const bg = scene.background; const fog = scene.fog;
  scene.background = new THREE.Color(sky); scene.fog = new THREE.Fog(sky, fogNear, fogFar);
  return () => { hidden.forEach((o) => { o.visible = true; }); scene.background = bg; scene.fog = fog; };
}

/** Merge simple geometries (each with an optional vertex colour) into one indexed geometry. */
export function mergeGeos(parts) {
  let nv = 0; let ni = 0;
  const gs = parts.map(([g, color]) => { const ng = g.index ? g : g.toNonIndexed(); nv += ng.attributes.position.count; ni += ng.index ? ng.index.count : ng.attributes.position.count; return [ng, new THREE.Color(color ?? 0xffffff)]; });
  const pos = new Float32Array(nv * 3); const nor = new Float32Array(nv * 3); const col = new Float32Array(nv * 3); const idx = new Uint32Array(ni);
  let vo = 0; let io = 0;
  gs.forEach(([g, c]) => {
    const p = g.attributes.position; const n = g.attributes.normal;
    for (let i = 0; i < p.count; i++) { pos.set([p.getX(i), p.getY(i), p.getZ(i)], (vo + i) * 3); if (n) nor.set([n.getX(i), n.getY(i), n.getZ(i)], (vo + i) * 3); col.set([c.r, c.g, c.b], (vo + i) * 3); }
    if (g.index) for (let k = 0; k < g.index.count; k++) idx[io + k] = g.index.getX(k) + vo; else for (let k = 0; k < p.count; k++) idx[io + k] = vo + k;
    io += g.index ? g.index.count : p.count; vo += p.count; g.dispose();
  });
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(pos, 3)); out.setAttribute('normal', new THREE.BufferAttribute(nor, 3)); out.setAttribute('color', new THREE.BufferAttribute(col, 3));
  out.setIndex(new THREE.BufferAttribute(idx, 1));
  return out;
}
