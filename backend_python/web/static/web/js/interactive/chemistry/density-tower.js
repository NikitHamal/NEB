/**
 * Density tower — tip six real liquids into a tall cylinder in any order and they sort
 * themselves by density (g/mL): a denser liquid falls through the lighter layers as drops before
 * joining its own layer. Then drop objects in: each one is pushed up by the weight of the liquid
 * it displaces (Archimedes), so it sinks until the liquid around it is as dense as it is and
 * floats at that floor — often right on an interface between two layers.
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, withAlpha, sphere, softShadow } from '../core/kit2d.js';
import { Pool, vesselBack, vesselFront, createShelf, stream } from '../core/chem2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const CAP = 480;
const LIQ = [
  { id: 'honey', label: 'Honey', rho: 1.42, color: '#e0a526', kind: 'bottle', sub: 'HON' },
  { id: 'syrup', label: 'Corn syrup', rho: 1.33, color: '#a855f7', kind: 'bottle', sub: 'SYR' },
  { id: 'soap', label: 'Dish soap', rho: 1.06, color: '#22c55e', kind: 'bottle', sub: 'SOAP' },
  { id: 'water', label: 'Water', rho: 1.0, color: '#3b82f6', kind: 'bottle', sub: 'H₂O' },
  { id: 'oil', label: 'Vegetable oil', rho: 0.92, color: '#facc15', kind: 'bottle', sub: 'OIL', glass: '#fef9c3' },
  { id: 'alcohol', label: 'Rubbing alcohol', rho: 0.79, color: '#ef4444', kind: 'bottle', sub: 'ALC' },
];
const OBJ = [
  { id: 'cork', label: 'Cork', rho: 0.24, size: 13, kind: 'object', color: '#c08a55' },
  { id: 'ice', label: 'Ice cube', rho: 0.917, size: 13, kind: 'object', color: '#dbeafe' },
  { id: 'tomato', label: 'Cherry tomato', rho: 1.03, size: 11, kind: 'object', color: '#e5484d' },
  { id: 'bead', label: 'Plastic bead', rho: 1.38, size: 8, kind: 'object', color: '#2563eb' },
  { id: 'nut', label: 'Steel nut', rho: 7.8, size: 9, kind: 'object', color: '#94a3b8' },
];

export default function init(stage) {
  const k = createKit(stage, { label: 'A tall cylinder for layering liquids, with bottles and objects to add' });
  const hud = createHud(stage);
  const badge = hud.badge('Tip the bottles into the cylinder in any order', T.blue);

  const vol = new Float64Array(LIQ.length);
  const shown = LIQ.map(() => new Spring(0, 60, 14));
  const drops = new Pool(160);
  const things = [];
  const v = { x: 0, y: 0, w: 110, h: 360, r: 10, lip: 5 };
  let pxPer = 1, pending = new Float64Array(LIQ.length), dropT = 0;
  for (const o of OBJ) o.draw = drawObjIcon;

  const panel = createPanel(stage, { title: 'Density tower' });
  panel.buttonRow([
    { label: 'Pour all', icon: 'shuffle', onClick: pourAll },
    { label: 'Empty', icon: 'delete', variant: 'ghost', onClick: () => { vol.fill(0); pending.fill(0); drops.clear(); things.length = 0; shown.forEach((s) => s.set(0)); k.invalidate(); } },
  ]);
  const st = panel.stats([{ key: 'total', label: 'Liquid in the cylinder' }, { key: 'layers', label: 'Layers' }, { key: 'top', label: 'Top layer' }, { key: 'bottom', label: 'Bottom layer' }]);
  const table = document.createElement('div'); table.className = 'k2-table'; table.style.setProperty('--k2-cols', 2); panel.body.appendChild(table);
  table.innerHTML = '<div class="k2-tr k2-th"><span>Liquid</span><span>Density g/mL</span></div>' + LIQ.map((l) => `<div class="k2-tr"><span>${l.label}</span><span>${l.rho.toFixed(2)}</span></div>`).join('') + OBJ.map((o) => `<div class="k2-tr"><span>${o.label}</span><span>${o.rho.toFixed(2)}</span></div>`).join('');
  panel.info('Density = mass ÷ volume. A denser liquid sinks below a lighter one, whatever order you pour them in. An object floats where the liquid around it is just as dense as it is.');

  const shelf = createShelf(k, LIQ, {
    target: () => ({ x: v.x, y: v.y - v.h, w: v.w }),
    onPour: (it, dt, lx, ly) => {
      const i = LIQ.indexOf(it);
      const room = CAP - total() - totalPending();
      if (room <= 0) return;
      const add = Math.min(room, 45 * dt);
      pending[i] += add;
      dropT += dt;
      if (dropT > 0.04) { dropT = 0; drops.add(v.x + (Math.random() - 0.5) * (v.w - 30), v.y - surface() - 2, 0, 20, 4 + Math.random() * 3, i, 0); }
    },
  });
  const tray = createShelf(k, OBJ, {
    target: () => ({ x: -999, y: -999, w: 0 }),
    onPour: () => {},
    onDrop: (it, x, y) => {
      if (Math.abs(x - v.x) < v.w / 2 + 30 && y < v.y && y > v.y - v.h - 120) {
        things.push({ o: it, x: clamp(x, v.x - v.w / 2 + it.size + 4, v.x + v.w / 2 - it.size - 4), y: v.y - v.h - 10, vy: 0, rot: Math.random() * 6 });
        if (things.length > 10) things.shift();
        k.animate(true);
      }
    },
  });

  function total() { let s = 0; for (let i = 0; i < vol.length; i++) s += vol[i]; return s; }
  function totalPending() { let s = 0; for (let i = 0; i < pending.length; i++) s += pending[i]; return s; }
  function surface() { return (total() + totalPending()) * pxPer; }
  function order(i) { let below = 0; for (let j = 0; j < LIQ.length; j++) if (LIQ[j].rho > LIQ[i].rho) below += vol[j]; return below; }
  function densityAt(hpx) {
    if (hpx < 0) return 7.8;
    for (let j = 0; j < LIQ.length; j++) {
      if (vol[j] < 0.01) continue;
      const b0 = order(j) * pxPer, t0 = b0 + vol[j] * pxPer;
      if (hpx >= b0 && hpx < t0) return LIQ[j].rho;
    }
    return 0.0012;
  }

  function pourAll() {
    vol.fill(0); pending.fill(0); drops.clear(); things.length = 0; shown.forEach((s) => s.set(0));
    const seq = LIQ.map((_, i) => i).sort(() => Math.random() - 0.5);
    seq.forEach((i, n) => setTimeout(() => { for (let d = 0; d < 26; d++) drops.add(v.x + (Math.random() - 0.5) * (v.w - 30), v.y - surface() - 2 - d * 2, 0, 20, 4 + Math.random() * 3, i, 0); pending[i] += 60; k.animate(true); }, n * 700));
    badge.set(`Pouring in this order: ${seq.map((i) => LIQ[i].label).join(', ')}`);
  }

  k.onResize((w, h) => {
    if (k.small) {
      v.w = 90; v.h = h * 0.6; v.x = w * 0.36; v.y = h - 26;
      shelf.layout(4, 8, w - 8, 66); tray.layout(w * 0.62, h * 0.32, w * 0.38, h * 0.56);
    } else {
      v.w = 120; v.h = Math.min(h - 170, 420); v.x = w * 0.36; v.y = h - 36;
      shelf.layout(w * 0.04, 26, w * 0.66, 90); tray.layout(w * 0.62, h - 120, w * 0.36, 70);
    }
    if (k.small) { for (let i = 0; i < OBJ.length; i++) { const sl = tray.slots[i]; sl.x = w * 0.84; sl.y = h * 0.3 + i * (h * 0.6 / OBJ.length) + 30; sl.hx.set(sl.x); sl.hy.set(sl.y); } }
    pxPer = (v.h - 14) / CAP;
  });

  k.frame((ctx, dt, w, h) => {
    const moving1 = shelf.step(dt), moving2 = tray.step(dt);
    // drops: denser ones sink through lighter layers, lighter ones rise; then join their layer
    for (let n = drops.n - 1; n >= 0; n--) {
      const i = drops.life[n] | 0;
      const hNow = v.y - drops.y[n];
      const target = (order(i) + vol[i]) * pxPer;
      const dir = hNow > target ? 1 : -1;
      const env = densityAt(hNow);
      const speed = clamp(Math.abs(LIQ[i].rho - env) * 260 + 30, 30, 220);
      drops.y[n] += dir * speed * dt;
      drops.x[n] += Math.sin(k.t * 4 + n) * 6 * dt;
      if ((dir > 0 && v.y - drops.y[n] <= target + 1) || (dir < 0 && v.y - drops.y[n] >= target - 1)) {
        const share = Math.min(pending[i], 60 / 26);
        pending[i] -= share; vol[i] += share; drops.kill(n);
      }
    }
    for (let i = 0; i < LIQ.length; i++) if (drops.n === 0 && pending[i] > 0) { vol[i] += pending[i]; pending[i] = 0; }
    let anim = false;
    for (let i = 0; i < LIQ.length; i++) { shown[i].to(order(i) * pxPer); if (shown[i].step(dt)) anim = true; }
    // objects: buoyancy from the liquid they displace
    for (const t of things) {
      const sz = t.o.size, hb = v.y - t.y;
      let disp = 0;
      for (let s = -2; s <= 2; s++) disp += densityAt(hb + s * sz / 2.5) / 5;
      const a = 9.81 * 160 * (disp - t.o.rho) / Math.max(t.o.rho, 0.5);
      t.vy -= a * dt; t.vy *= Math.exp(-dt * (disp > 0.01 ? 4 : 0.2));
      t.y += t.vy * dt;
      const floor = v.y - 4 - sz;
      if (t.y > floor) { t.y = floor; t.vy = 0; }
      if (Math.abs(t.vy) > 0.5) anim = true;
    }
    background(k, ctx, w, h);
    ctx.fillStyle = '#e6dccb'; ctx.fillRect(0, v.y, w, h - v.y); ctx.fillStyle = '#d4c4a8'; ctx.fillRect(0, v.y, w, 3);
    const sy = shelf.slots[0].y;
    ctx.fillStyle = '#c9a77a'; ctx.fillRect(k.small ? 0 : w * 0.02, sy, k.small ? w : w * 0.7, 6);
    softShadow(ctx, v.x, v.y + 2, v.w * 0.7, 6, 0.2);
    vesselBack(ctx, v);
    for (let i = 0; i < LIQ.length; i++) {
      if (vol[i] < 0.05) continue;
      const y0 = shown[i].x, y1 = y0 + vol[i] * pxPer;
      const left = v.x - v.w / 2 + 3, ww = v.w - 6;
      ctx.fillStyle = withAlpha(LIQ[i].color, LIQ[i].id === 'water' ? 0.45 : 0.78);
      ctx.fillRect(left, v.y - y1, ww, y1 - y0 - (y0 < 1 ? 3 : 0));
      ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(left, v.y - y1, ww, 2);
      if (vol[i] * pxPer > 12) {
        const lx = v.x + v.w / 2 + 12, ly = v.y - (y0 + y1) / 2;
        ctx.strokeStyle = withAlpha(LIQ[i].color, 0.8); ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(v.x + v.w / 2 - 2, ly); ctx.lineTo(lx, ly); ctx.stroke();
        text(ctx, `${LIQ[i].label} ${LIQ[i].rho.toFixed(2)}`, lx + 4, ly + 4, T.ink, k.small ? 9.5 : 11, 600);
      }
    }
    for (let n = 0; n < drops.n; n++) { const i = drops.life[n] | 0; ctx.fillStyle = withAlpha(LIQ[i].color, 0.85); ctx.beginPath(); ctx.ellipse(drops.x[n], drops.y[n], drops.r[n] * 0.8, drops.r[n], 0, 0, Math.PI * 2); ctx.fill(); }
    for (const t of things) drawThing(ctx, t);
    vesselFront(ctx, v, { capacity: CAP, step: 100 });
    const held = shelf.held;
    if (held && shelf.pouring) { const l = shelf.tipOf(LIQ.indexOf(held), { x: 0, y: 0 }); stream(ctx, l.x, l.y, l.x + 6, v.y - surface(), held.color, held.id === 'honey' || held.id === 'syrup' ? 7 : 4); }
    shelf.draw(ctx); tray.draw(ctx);
    if (!k.small) text(ctx, 'Drop objects in →', tray.slots[0].x - 50, tray.slots[0].y - 74, T.ink2, 10.5, 600);
    let layers = 0, top = -1, bot = -1;
    for (let i = 0; i < LIQ.length; i++) if (vol[i] > 0.5) { layers++; if (top < 0 || LIQ[i].rho < LIQ[top].rho) top = i; if (bot < 0 || LIQ[i].rho > LIQ[bot].rho) bot = i; }
    st.total.set(`${fmt(total(), 0)} mL`); st.layers.set(String(layers));
    st.top.set(top >= 0 ? LIQ[top].label : '—'); st.bottom.set(bot >= 0 ? LIQ[bot].label : '—');
    if (drops.n > 0) badge.set('Watch the drops find their own layer');
    k.animate(moving1 || moving2 || anim || drops.n > 0);
  });

  function drawThing(ctx, t) {
    const o = t.o, s = o.size;
    if (o.id === 'tomato' || o.id === 'bead') { sphere(ctx, t.x, t.y, s, o.color); if (o.id === 'tomato') { ctx.fillStyle = '#15803d'; ctx.fillRect(t.x - 2, t.y - s - 2, 4, 4); } return; }
    ctx.save(); ctx.translate(t.x, t.y); ctx.rotate(Math.sin(t.rot) * 0.2);
    drawObjShape(ctx, o, s);
    ctx.restore();
  }
  function drawObjShape(ctx, o, s) {
    if (o.id === 'cork') { ctx.fillStyle = '#c08a55'; ctx.beginPath(); ctx.roundRect(-s, -s * 0.75, s * 2, s * 1.5, 3); ctx.fill(); ctx.fillStyle = 'rgba(90,50,20,0.35)'; for (let i = 0; i < 6; i++) ctx.fillRect(-s + 3 + (i * 7) % (2 * s - 5), -s * 0.5 + (i * 5) % s, 2, 2); }
    else if (o.id === 'ice') { ctx.fillStyle = 'rgba(219,234,254,0.85)'; ctx.strokeStyle = 'rgba(120,160,210,0.9)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.roundRect(-s, -s, s * 2, s * 2, 4); ctx.fill(); ctx.stroke(); ctx.fillStyle = 'rgba(255,255,255,0.8)'; ctx.fillRect(-s + 3, -s + 3, 5, 3); }
    else if (o.id === 'nut') { ctx.fillStyle = '#94a3b8'; ctx.beginPath(); for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3; ctx.lineTo(Math.cos(a) * s, Math.sin(a) * s); } ctx.closePath(); ctx.fill(); ctx.strokeStyle = '#64748b'; ctx.stroke(); ctx.beginPath(); ctx.arc(0, 0, s * 0.45, 0, Math.PI * 2); ctx.fillStyle = '#e2e8f0'; ctx.fill(); }
  }
  function drawObjIcon(ctx, o) {
    if (o.id === 'tomato' || o.id === 'bead') { sphere(ctx, 0, -o.size - 2, o.size, o.color); return; }
    ctx.translate(0, -o.size - 2); drawObjShape(ctx, o, o.size);
  }

  k.debug = { slot: (i) => [shelf.slots[i].x, shelf.slots[i].y - 30], obj: (i) => [tray.slots[i].x, tray.slots[i].y - 12], top: () => [v.x, v.y - v.h - 30], vol: () => Array.from(vol), things: () => things.map((t) => [t.o.id, Math.round(v.y - t.y)]), pourAll };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
