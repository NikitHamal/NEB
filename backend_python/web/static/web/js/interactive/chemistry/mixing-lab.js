/**
 * Mix it up — drag water, oil, salt, sand and food colouring from the shelf and tip them into
 * the beaker. Salt dissolves (up to its real solubility, about 36 g per 100 mL of water) faster
 * when you stir with the spoon; sand settles to the bottom and never dissolves; oil rises and
 * floats as a layer; a drop of colouring sinks through the oil and spreads through the water by
 * diffusion. Heat the beaker to boil the water off and the salt comes back as crystals.
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, withAlpha, card, softShadow } from '../core/kit2d.js';
import { Pool, vesselBack, vesselFront, liquid, meniscus, createShelf, stream } from '../core/chem2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const CAP = 250;
const GX = 18, GY = 22;
const SOLUBILITY = 0.36;
const ITEMS = [
  { id: 'water', label: 'Water', color: '#7cc4f2', kind: 'bottle', sub: 'H₂O' },
  { id: 'oil', label: 'Oil', color: '#f2c94c', kind: 'bottle', sub: 'OIL', glass: '#fef3c7' },
  { id: 'salt', label: 'Salt', color: '#f8fafc', kind: 'shaker' },
  { id: 'sand', label: 'Sand', color: '#d6b37a', kind: 'jar' },
  { id: 'dye', label: 'Colouring', color: '#e5484d', kind: 'dropper' },
];

export default function init(stage) {
  const k = createKit(stage, { label: 'A beaker and a shelf of water, oil, salt, sand and food colouring' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag something from the shelf over the beaker', T.blue);

  let water = 0, oil = 0, saltAdded = 0, saltDis = 0, sandG = 0, heating = false, stir = 0, dyeColor = '#e5484d', dropTimer = 0, grainTimer = 0;
  const grains = new Pool(400);
  const drops = new Pool(24);
  const dye = new Float32Array(GX * GY), dye2 = new Float32Array(GX * GY);
  const v = { x: 0, y: 0, w: 160, h: 220, r: 14, lip: 5 };
  let pxPer = 1, lastMsg = '';
  const spoon = { x: 0, y: 0, held: false, px: 0, py: 0, ang: 0 };
  const flame = new Spring(0, 80, 12);

  const panel = createPanel(stage, { title: 'Mixing lab' });
  panel.chips({ label: 'Food colouring', options: [{ value: '#e5484d', label: 'Red', color: '#e5484d' }, { value: '#2563eb', label: 'Blue', color: '#2563eb' }, { value: '#16a34a', label: 'Green', color: '#16a34a' }], value: dyeColor, onChange: (c) => { dyeColor = c; ITEMS[4].color = c; } });
  const heatT = panel.toggle({ label: 'Heat the beaker (evaporate)', value: false, onChange: (h) => { heating = h; k.animate(true); } });
  panel.buttonRow([
    { label: 'Stir', icon: 'cyclone', onClick: () => { stir = 1; k.animate(true); } },
    { label: 'Empty', icon: 'delete', variant: 'ghost', onClick: empty },
  ]);
  const st = panel.stats([{ key: 'water', label: 'Water' }, { key: 'oil', label: 'Oil' }, { key: 'salt', label: 'Salt dissolved' }, { key: 'conc', label: 'Salt per 100 mL' }]);
  panel.info('Dissolved salt is still there: it has split into particles too small to see. Sand grains are too strongly held together to dissolve. Oil is less dense than water and does not mix with it.');

  function empty() { water = oil = saltAdded = saltDis = sandG = 0; grains.clear(); drops.clear(); dye.fill(0); heating = false; heatT.set(false); k.invalidate(); }

  const shelf = createShelf(k, ITEMS, {
    target: () => ({ x: v.x, y: v.y - v.h, w: v.w }),
    onPour: (it, dt, lx, ly) => {
      const room = CAP - water - oil - sandG / 2.65;
      if (it.id === 'water' && room > 0) water += Math.min(room, 30 * dt);
      else if (it.id === 'oil' && room > 0) { oil += Math.min(room, 20 * dt); if (water > 5 && Math.random() < dt * 12) drops.add(v.x + (Math.random() - 0.5) * v.w * 0.6, v.y - (water * 0.6) * pxPer, 0, -40, 3 + Math.random() * 4, 3, 1); }
      else if (it.id === 'salt' || it.id === 'sand') {
        grainTimer += dt;
        const per = it.id === 'salt' ? 0.05 : 0.04;
        while (grainTimer > per) {
          grainTimer -= per;
          if (it.id === 'salt') { saltAdded += 0.5; grains.add(lx + (Math.random() - 0.5) * 6, ly, (Math.random() - 0.5) * 20, 30, 3.6, 0.5, 0); }
          else { sandG += 1.5; grains.add(lx + (Math.random() - 0.5) * 10, ly, (Math.random() - 0.5) * 30, 40, 1.8, 1.5, 1); }
        }
      } else if (it.id === 'dye') {
        dropTimer += dt;
        if (dropTimer > 0.45) { dropTimer = 0; drops.add(lx, ly, 0, 20, 3.5, 1, 0); }
      }
    },
  });

  k.drag({
    hit: (x, y, s) => (Math.hypot(x - spoon.x, y - spoon.y) < 20 + s || (Math.abs(x - spoon.x - Math.sin(spoon.ang) * 40) < 10 + s && Math.abs(y - spoon.y + 40) < 40) ? 1 : false),
    down: (x, y) => { spoon.held = true; spoon.px = x; spoon.py = y; k.animate(true); },
    move: (x, y) => {
      const nx = clamp(x, v.x - v.w / 2 + 14, v.x + v.w / 2 - 14), ny = clamp(y, v.y - v.h + 10, v.y - 12);
      const sp = Math.hypot(nx - spoon.px, ny - spoon.py);
      if (water + oil > 5 && ny > v.y - (water + oil) * pxPer) stir = Math.min(1, stir + sp * 0.01);
      spoon.x = nx; spoon.y = ny; spoon.px = nx; spoon.py = ny;
    },
    up: () => { spoon.held = false; },
  });

  k.onResize((w, h) => {
    const small = k.small;
    v.w = small ? 140 : 200; v.h = small ? h * 0.5 : Math.min(340, h * 0.58);
    v.x = small ? w * 0.42 : w * 0.42; v.y = h - (small ? 40 : 56);
    pxPer = (v.h - 10) / CAP;
    shelf.layout(small ? 6 : w * 0.06, 20, small ? w - 12 : w * 0.72, small ? 74 : 92);
    spoon.x = v.x + v.w / 2 - 22; spoon.y = v.y - v.h * 0.5;
  });

  function waterTop() { return (sandG / 2.65 + water) * pxPer; }
  function bedTop() { return sandG / 1.6 * pxPer; }
  function cell(px, py) {
    const wt = waterTop(), bt = bedTop();
    if (wt - bt < 2) return -1;
    const gx = Math.floor((px - (v.x - v.w / 2 + 3)) / ((v.w - 6) / GX)), gy = Math.floor(((v.y - bt) - py) / ((wt - bt) / GY));
    if (gx < 0 || gx >= GX || gy < 0 || gy >= GY) return -1;
    return gy * GX + gx;
  }

  function physics(dt) {
    // evaporation
    if (heating && water > 0) {
      water = Math.max(0, water - 6 * dt);
      if (Math.random() < dt * 20) drops.add(v.x + (Math.random() - 0.5) * v.w * 0.6, v.y - waterTop() - 6, (Math.random() - 0.5) * 6, -30, 5, 1.2, 2);
    }
    // dissolving and crystallising
    const cap = water * SOLUBILITY;
    if (saltDis > cap) {
      const back = saltDis - cap; saltDis = cap;
      for (let n = 0; n < Math.min(60, back / 0.5); n++) grains.add(v.x + (Math.random() - 0.5) * (v.w - 30), v.y - bedTop() - 3, 0, 0, 2.6, 0.5, 0);
    }
    stir *= Math.exp(-dt * 0.8);
    const rate = (0.12 + 1.6 * stir) * dt;
    for (let i = grains.n - 1; i >= 0; i--) {
      const kind = grains.kind[i];
      const wt = waterTop(), surfY = v.y - wt, inWater = grains.y[i] > surfY && water > 1;
      const g = inWater ? (kind ? 160 : 90) : 500;
      grains.vy[i] += g * dt; grains.vx[i] *= inWater ? Math.exp(-dt * 6) : 1; grains.vy[i] *= inWater ? Math.exp(-dt * 5) : 1;
      if (inWater && stir > 0.05) grains.vx[i] += Math.sin(k.t * 3 + grains.y[i] * 0.05) * stir * 120 * dt;
      grains.x[i] += grains.vx[i] * dt; grains.y[i] += grains.vy[i] * dt;
      grains.x[i] = clamp(grains.x[i], v.x - v.w / 2 + 6, v.x + v.w / 2 - 6);
      const floor = v.y - bedTop() - 3 - (kind ? 0 : 0);
      if (grains.y[i] > floor && grains.y[i] > v.y - v.h) { grains.y[i] = floor - Math.random() * 2; grains.vy[i] = 0; grains.vx[i] = 0; if (kind === 1) { grains.kill(i); continue; } }
      if (kind === 0 && inWater) {
        const room = water * SOLUBILITY - saltDis;
        if (room > 0) { const d = Math.min(grains.life[i], rate * 0.5 * Math.min(1, room / 2) * (grains.y[i] >= floor - 3 ? 0.6 : 1)); grains.life[i] -= d; saltDis += d; grains.r[i] = 3.6 * Math.sqrt(grains.life[i] / 0.5) + 0.6; if (grains.life[i] <= 0.002) { grains.kill(i); } }
      }
    }
    for (let i = drops.n - 1; i >= 0; i--) {
      const kind = drops.kind[i];
      drops.life[i] -= dt * (kind === 2 ? 1 : 0);
      if (kind === 1) {
        drops.y[i] += drops.vy[i] * dt;
        if (drops.y[i] < v.y - waterTop() - 2) drops.kill(i);
        continue;
      }
      if (kind === 2) { drops.y[i] += drops.vy[i] * dt; drops.x[i] += drops.vx[i] * dt; drops.r[i] += dt * 6; if (drops.life[i] <= 0) drops.kill(i); continue; }
      drops.vy[i] += (drops.y[i] > v.y - waterTop() - oil * pxPer ? 40 : 600) * dt;
      if (drops.y[i] > v.y - waterTop()) drops.vy[i] = Math.min(drops.vy[i], 60);
      drops.y[i] += drops.vy[i] * dt;
      const c = cell(drops.x[i], drops.y[i] + 4);
      if (water > 2 && c >= 0) { dye[c] += 7; drops.kill(i); }
      else if (drops.y[i] > v.y - bedTop() - 4) { const c2 = cell(drops.x[i], v.y - bedTop() - 6); if (c2 >= 0) dye[c2] += 7; drops.kill(i); }
    }
    // diffusion (with a gentle sink of the denser dye) plus stirring
    if (water > 2) {
      const D = 1.4 + 30 * stir, n = Math.ceil(D * dt / 0.2), h = dt / n;
      for (let s = 0; s < n; s++) {
        for (let y = 0; y < GY; y++) for (let x = 0; x < GX; x++) {
          const i = y * GX + x, c = dye[i];
          const l = x > 0 ? dye[i - 1] : c, r = x < GX - 1 ? dye[i + 1] : c, d = y > 0 ? dye[i - GX] : c, u = y < GY - 1 ? dye[i + GX] : c;
          dye2[i] = c + D * h * (l + r + u + d - 4 * c);
        }
        for (let y = 0; y < GY; y++) for (let x = 0; x < GX; x++) { const i = y * GX + x; if (y > 0) { const m = dye2[i] * 1.0 * h; dye2[i] -= m; dye2[i - GX] += m; } }
        dye.set(dye2);
      }
    }
  }

  k.frame((ctx, dt, w, h) => {
    physics(dt);
    const shelfMoving = shelf.step(dt);
    flame.to(heating ? 1 : 0); flame.step(dt);
    background(k, ctx, w, h);
    // bench and shelf
    ctx.fillStyle = '#e6dccb'; ctx.fillRect(0, v.y, w, h - v.y); ctx.fillStyle = '#d4c4a8'; ctx.fillRect(0, v.y, w, 3);
    const sy = shelf.slots[0].y;
    ctx.fillStyle = '#c9a77a'; ctx.fillRect(0, sy, k.small ? w : w * 0.78, 6); ctx.fillStyle = 'rgba(0,0,0,0.08)'; ctx.fillRect(0, sy + 6, k.small ? w : w * 0.78, 4);
    // heater
    if (flame.x > 0.02) {
      ctx.fillStyle = '#475569'; ctx.fillRect(v.x - 30, v.y - 2, 60, 6);
      for (let i = -2; i <= 2; i++) { const fh = (12 + 6 * Math.sin(k.t * 14 + i)) * flame.x; ctx.fillStyle = withAlpha('#3b82f6', 0.7); ctx.beginPath(); ctx.ellipse(v.x + i * 10, v.y - 2 - fh / 2, 3.5, fh / 2, 0, 0, Math.PI * 2); ctx.fill(); }
    }
    softShadow(ctx, v.x, v.y + 2, v.w * 0.6, 6, 0.2);
    vesselBack(ctx, v);
    const bt = bedTop(), wt = waterTop();
    // sand bed
    if (sandG > 0) { liquid(ctx, v, 0, bt, '#c9a46a', 1); ctx.fillStyle = 'rgba(120,90,40,0.35)'; for (let i = 0; i < Math.min(160, sandG * 2); i++) { const gx = v.x - v.w / 2 + 6 + ((i * 37) % (v.w - 12)), gy = v.y - 4 - ((i * 13) % Math.max(1, bt - 4)); ctx.fillRect(gx, gy, 1.6, 1.6); } }
    // water with dye
    if (water > 0.5) {
      liquid(ctx, v, bt, wt, '#bfe3fb', 0.75);
      const cw = (v.w - 6) / GX, chh = (wt - bt) / GY, x0 = v.x - v.w / 2 + 3;
      ctx.fillStyle = dyeColor;
      for (let y = 0; y < GY; y++) for (let x = 0; x < GX; x++) { const c = dye[y * GX + x]; if (c < 0.01) continue; ctx.globalAlpha = Math.min(0.85, c * 0.5); ctx.fillRect(x0 + x * cw - 0.5, v.y - bt - (y + 1) * chh - 0.5, cw + 1, chh + 1); }
      ctx.globalAlpha = 1;
    }
    if (oil > 0.5) liquid(ctx, v, water > 0.5 ? wt : bt, (water > 0.5 ? wt : bt) + oil * pxPer, '#f2c94c', 0.75);
    const top = (water > 0.5 ? wt : bt) + oil * pxPer;
    if (water + oil > 1) meniscus(ctx, v, top, oil > 0.5 ? '#f2c94c' : '#7cc4f2');
    if (oil > 0.5 && water > 0.5) { ctx.strokeStyle = 'rgba(180,140,40,0.6)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(v.x - v.w / 2 + 3, v.y - wt); ctx.lineTo(v.x + v.w / 2 - 3, v.y - wt); ctx.stroke(); }
    // grains and drops
    for (let i = 0; i < grains.n; i++) { ctx.fillStyle = grains.kind[i] ? '#b88a4a' : '#ffffff'; const r = grains.r[i]; ctx.fillRect(grains.x[i] - r / 2, grains.y[i] - r / 2, r, r); if (!grains.kind[i]) { ctx.strokeStyle = 'rgba(70,90,120,0.75)'; ctx.lineWidth = 0.8; ctx.strokeRect(grains.x[i] - r / 2, grains.y[i] - r / 2, r, r); } }
    for (let i = 0; i < drops.n; i++) {
      const kind = drops.kind[i];
      ctx.fillStyle = kind === 1 ? withAlpha('#f2c94c', 0.85) : kind === 2 ? withAlpha('#ffffff', Math.max(0, drops.life[i] * 0.5)) : dyeColor;
      ctx.beginPath(); ctx.arc(drops.x[i], drops.y[i], drops.r[i], 0, Math.PI * 2); ctx.fill();
    }
    vesselFront(ctx, v, { capacity: CAP, step: 50 });
    // stream from the held bottle
    const held = shelf.held;
    if (held && shelf.pouring && (held.id === 'water' || held.id === 'oil')) { const l = shelf.tipOf(ITEMS.indexOf(held), { x: 0, y: 0 }); stream(ctx, l.x, l.y, l.x + 6, v.y - top, held.color, 5); }
    // spoon
    ctx.save(); ctx.translate(spoon.x, spoon.y); ctx.rotate(spoon.held ? Math.sin(k.t * 10) * 0.2 * stir : 0.15);
    ctx.fillStyle = '#94a3b8'; ctx.fillRect(-2, -110, 4, 100); ctx.beginPath(); ctx.ellipse(0, -6, 7, 11, 0, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
    if (!spoon.held && stir < 0.05 && water > 20) text(ctx, 'stir ↻', spoon.x + 14, spoon.y - 60, T.blue, 10, 700);
    shelf.draw(ctx);
    // observation card
    const msg = observe();
    if (!k.small) {
      const cx = v.x + v.w / 2 + 30, cw = Math.min(260, w - cx - 16);
      if (cw > 140) { card(ctx, cx, v.y - 150, cw, 120, 12); text(ctx, 'What do you see?', cx + 12, v.y - 128, T.ink, 11.5, 700); wrap(ctx, msg, cx + 12, v.y - 108, cw - 24, 15); }
    }
    if (msg !== lastMsg) { lastMsg = msg; badge.set(msg.length > 70 ? msg.slice(0, msg.indexOf('.') + 1) || msg : msg); }
    st.water.set(`${fmt(water, 0)} mL`); st.oil.set(`${fmt(oil, 0)} mL`);
    st.salt.set(`${fmt(saltDis, 1)} of ${fmt(saltAdded, 1)} g`);
    st.conc.set(water > 1 ? `${fmt(saltDis / water * 100, 1)} g${saltDis >= water * SOLUBILITY - 0.05 && saltAdded > saltDis + 0.3 ? ' (saturated)' : ''}` : '—');
    k.animate(shelfMoving || grains.n > 0 && hasMoving() || drops.n > 0 || stir > 0.01 || heating || flame.moving || spoon.held || dyeActive());
  });

  function hasMoving() { for (let i = 0; i < grains.n; i++) if (grains.vy[i] !== 0 || (grains.kind[i] === 0 && water > 1 && saltDis < water * SOLUBILITY - 0.01)) return true; return false; }
  function dyeActive() { if (water < 2) return false; let mx = 0, mn = 1e9; for (let i = 0; i < dye.length; i++) { if (dye[i] > mx) mx = dye[i]; if (dye[i] < mn) mn = dye[i]; } return mx - mn > 0.02; }
  function observe() {
    if (water + oil + saltAdded + sandG < 0.1) return 'Drag a bottle, the salt shaker, the sand jar or the colouring over the beaker and tip it in.';
    if (heating && water > 0) return 'The water is evaporating. Watch: when too little water is left, the salt comes back as crystals.';
    if (heating && saltAdded > 0) return 'All the water has boiled away and the salt is back as white crystals. It was there all along!';
    if (saltAdded > saltDis + 0.6 && water > 5 && saltDis >= water * SOLUBILITY - 0.1) return 'Saturated! The water cannot dissolve any more salt, so the extra stays at the bottom. Add water to dissolve it.';
    if (saltAdded > 0 && saltDis > saltAdded - 0.6 && water > 5) return 'The salt has dissolved: it has broken into particles too small to see, spread through the water.';
    if (saltAdded > 0 && water > 5) return 'The salt is dissolving. Stir with the spoon to make it dissolve faster.';
    if (oil > 1 && water > 1) return 'Oil floats on water: it is less dense and does not mix, even when you stir.';
    if (sandG > 0 && water > 1) return 'Sand sinks and settles. Stir all you like, it will not dissolve.';
    if (dyeActive()) return 'The colouring spreads out on its own (diffusion). Stirring makes it spread much faster.';
    if (water > 1) return 'Plain water. Try adding salt, sand, oil or a drop of colouring.';
    return 'Things behave differently without water. Add some water!';
  }
  function wrap(ctx, s, x, y, maxW, lh) {
    ctx.font = '500 11px Poppins, system-ui, sans-serif'; ctx.fillStyle = T.ink2; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    let line = '', yy = y;
    const words = s.split(' ');
    for (let i = 0; i < words.length; i++) { const test = line ? line + ' ' + words[i] : words[i]; if (ctx.measureText(test).width > maxW && line) { ctx.fillText(line, x, yy); line = words[i]; yy += lh; } else line = test; }
    if (line) ctx.fillText(line, x, yy);
  }

  k.debug = { slot: (i) => [shelf.slots[i].x, shelf.slots[i].y - 30], beaker: () => [v.x, v.y - v.h - 30], state: () => ({ water, oil, saltAdded, saltDis, sandG }) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
