/**
 * Fizzy reactions — tip vinegar into a conical flask and spoon in baking soda:
 * NaHCO₃ + CH₃COOH → CH₃COONa + H₂O + CO₂. Household vinegar is about 5 % acetic acid
 * (0.83 mmol/mL) and baking soda is 84 g/mol, so the amounts set how much carbon dioxide can be
 * made (24 L per mole at room temperature) and which ingredient runs out first. Fit the balloon to
 * catch the gas: it swells to the real volume made.
 */
import { createKit, T, Spring, Ring, fmt, clamp, background, text, pill, withAlpha, softShadow, card } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { Pool, createShelf, stream } from '../core/chem2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const ACID = 0.05 / 60;
const SODA_M = 84;
const VM = 24000;
const ITEMS = [
  { id: 'vinegar', label: 'Vinegar', color: '#f3e3b0', kind: 'bottle', sub: 'VIN', glass: '#fffbeb' },
  { id: 'soda', label: 'Baking soda', color: '#f8fafc', kind: 'spoon' },
  { id: 'water', label: 'Water', color: '#bfe3fb', kind: 'bottle', sub: 'H₂O' },
];

export default function init(stage) {
  const k = createKit(stage, { label: 'A conical flask with vinegar and baking soda and a balloon' });
  const hud = createHud(stage);
  const badge = hud.badge('Pour some vinegar into the flask', T.blue);

  let vinegar = 0, water = 0, acidMol = 0, sodaSolid = 0, sodaAdded = 0, co2 = 0, co2Balloon = 0, balloonOn = true, t = 0, rate = 0, spoonT = 0;
  const bubbles = new Pool(220);
  const grains = new Pool(120);
  const trace = new Ring(400);
  const balloonR = new Spring(0, 80, 9);
  const foam = new Spring(0, 40, 10);
  const plot = new Plot({ title: 'CO₂ made', xLabel: 't / s', yLabel: 'V / mL', yMin: 0, yMax: 500 });
  const f = { x: 0, y: 0, w: 170, h: 200, neck: 34, neckH: 50 };

  const panel = createPanel(stage, { title: 'Fizzy reactions' });
  const balT = panel.toggle({ label: 'Balloon on the flask', value: true, onChange: (b) => { balloonOn = b; if (!b) { co2Balloon = 0; } k.animate(true); } });
  panel.button({ label: 'Empty and wash the flask', icon: 'delete', variant: 'ghost', onClick: () => { vinegar = water = acidMol = sodaSolid = sodaAdded = co2 = co2Balloon = rate = t = 0; bubbles.clear(); grains.clear(); trace.clear(); k.invalidate(); } });
  const st = panel.stats([{ key: 'vin', label: 'Vinegar (acid)' }, { key: 'soda', label: 'Baking soda added' }, { key: 'co2', label: 'CO₂ made' }, { key: 'left', label: 'Left over' }]);
  panel.info('Try 50 mL of vinegar: it can react with about 3.5 g of baking soda. Add less and the soda runs out first; add more and the extra powder just sits there because the acid has run out.');

  const shelf = createShelf(k, ITEMS, {
    target: () => ({ x: f.x, y: f.y - f.h - f.neckH, w: f.neck + 30 }),
    onPour: (it, dt, lx, ly) => {
      if (it.id === 'vinegar' && vinegar + water < 240) { const a = 25 * dt; vinegar += a; acidMol += a * ACID; }
      else if (it.id === 'water' && vinegar + water < 240) water += 25 * dt;
      else if (it.id === 'soda') { spoonT += dt; while (spoonT > 0.08) { spoonT -= 0.08; sodaAdded += 0.25; sodaSolid += 0.25 / SODA_M; grains.add(lx + (Math.random() - 0.5) * 8, ly, (Math.random() - 0.5) * 10, 20, 2.2, 0.25 / SODA_M, 0); } }
      k.animate(true);
    },
  });

  k.onResize((w, h) => {
    f.w = k.small ? 140 : 190; f.h = k.small ? h * 0.32 : Math.min(230, h * 0.38); f.neck = k.small ? 30 : 36; f.neckH = k.small ? 36 : 50;
    f.x = k.small ? w * 0.36 : w * 0.3; f.y = h - (k.small ? 28 : 46);
    shelf.layout(k.small ? 4 : w * 0.04, 22, k.small ? w * 0.7 : w * 0.5, 80);
    if (k.small) plot.box(w * 0.64, h * 0.42, w * 0.34, h * 0.4); else plot.box(w * 0.58, h * 0.3, w * 0.4, Math.min(260, h * 0.48));
  });
  const liquidH = () => { const V = vinegar + water; return V <= 0 ? 0 : Math.min(f.h - 8, Math.sqrt(V / 240) * (f.h * 0.75)); };
  const widthAt = (hy) => f.neck + (f.w - f.neck) * clamp(1 - hy / f.h, 0, 1);

  k.drag({ hit: (x, y, s) => (Math.abs(x - f.x) < f.neck + s && y > f.y - f.h - f.neckH - 20 - s && y < f.y - f.h ? 1 : false), up: () => { balloonOn = !balloonOn; balT.set(balloonOn); if (!balloonOn) co2Balloon = 0; k.animate(true); }, cursor: 'pointer', cursorActive: 'pointer' });

  k.frame((ctx, dt, w, h) => {
    const moving = shelf.step(dt);
    const lh = liquidH(), surf = f.y - lh;
    // reaction kinetics: rate grows with exposed powder and with the acid left
    rate = 0;
    if (sodaSolid > 0 && acidMol > 0 && vinegar > 0) {
      const conc = acidMol / ((vinegar + water) / 1000);
      rate = Math.min(sodaSolid, acidMol, 1.6 * Math.pow(sodaSolid, 0.75) * Math.min(1, conc / 0.05) * dt);
      sodaSolid -= rate; acidMol -= rate; co2 += rate * VM;
      if (balloonOn) co2Balloon += rate * VM;
      rate /= Math.max(dt, 1e-6);
      for (let i = 0; i < Math.min(8, rate * 4000 * dt * 30); i++) bubbles.add(f.x + (Math.random() - 0.5) * widthAt(0) * 0.7, f.y - 6 - Math.random() * 10, (Math.random() - 0.5) * 10, -40 - Math.random() * 60, 1.5 + Math.random() * 3, 1, 0);
    }
    if (sodaSolid > 0 || rate > 0 || co2 > 0) t += dt;
    if (t > 0) trace.push(t, co2);
    for (let i = grains.n - 1; i >= 0; i--) { grains.vy[i] += (grains.y[i] > surf ? 60 : 500) * dt; if (grains.y[i] > surf) grains.vy[i] = Math.min(grains.vy[i], 50); grains.y[i] += grains.vy[i] * dt; grains.x[i] += grains.vx[i] * dt; if (grains.y[i] > f.y - 5) { grains.y[i] = f.y - 5 - Math.random() * 3; grains.vy[i] = 0; if (vinegar > 1) grains.kill(i); } }
    for (let i = bubbles.n - 1; i >= 0; i--) { bubbles.y[i] += bubbles.vy[i] * dt; bubbles.x[i] += bubbles.vx[i] * dt + Math.sin(k.t * 9 + i) * 0.3; if (bubbles.y[i] < surf - foam.x * 0.8) bubbles.kill(i); }
    foam.to(clamp(rate * 9000, 0, f.h * 0.7)); foam.step(dt);
    const bv = co2Balloon;
    balloonR.to(balloonOn ? Math.cbrt(3 * Math.max(0, bv) / (4 * Math.PI)) * (k.small ? 6 : 8.9) : 0); balloonR.step(dt);

    background(k, ctx, w, h);
    ctx.fillStyle = '#e6dccb'; ctx.fillRect(0, f.y, w, h - f.y); ctx.fillStyle = '#d4c4a8'; ctx.fillRect(0, f.y, w, 3);
    ctx.fillStyle = '#c9a77a'; ctx.fillRect(k.small ? 0 : w * 0.02, shelf.slots[0].y, k.small ? w * 0.72 : w * 0.52, 6);
    softShadow(ctx, f.x, f.y + 2, f.w * 0.6, 6, 0.2);
    // flask path
    const top = f.y - f.h, nl = f.x - f.neck / 2, nr = f.x + f.neck / 2;
    flaskPath(ctx, nl, nr, top);
    ctx.fillStyle = 'rgba(214,230,248,0.35)'; ctx.fill();
    ctx.save(); flaskPath(ctx, nl, nr, top); ctx.clip();
    if (lh > 0) { ctx.fillStyle = withAlpha(vinegar > water ? '#f6e7b6' : '#cfe8fb', 0.8); ctx.fillRect(f.x - f.w, surf, f.w * 2, lh + 2); }
    if (foam.x > 1) { ctx.fillStyle = 'rgba(255,255,255,0.88)'; ctx.beginPath(); ctx.moveTo(f.x - f.w, surf + 3); for (let x = -f.w / 2; x <= f.w / 2; x += 8) ctx.lineTo(f.x + x, surf - foam.x - 4 * Math.sin(x * 0.3 + k.t * 6)); ctx.lineTo(f.x + f.w, surf + 3); ctx.fill(); }
    ctx.fillStyle = 'rgba(255,255,255,0.75)';
    for (let i = 0; i < bubbles.n; i++) { ctx.beginPath(); ctx.arc(bubbles.x[i], bubbles.y[i], bubbles.r[i], 0, Math.PI * 2); ctx.fill(); }
    ctx.fillStyle = '#ffffff'; ctx.strokeStyle = 'rgba(100,120,150,0.5)'; ctx.lineWidth = 0.6;
    for (let i = 0; i < grains.n; i++) { ctx.fillRect(grains.x[i] - 1.5, grains.y[i] - 1.5, 3, 3); }
    if (sodaSolid > 1e-4 && vinegar > 1) { const pile = Math.min(18, Math.cbrt(sodaSolid * SODA_M) * 6); ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.ellipse(f.x, f.y - 3, pile * 2.4, pile, 0, Math.PI, 0); ctx.fill(); ctx.stroke(); }
    ctx.restore();
    flaskPath(ctx, nl, nr, top);
    ctx.strokeStyle = 'rgba(120,150,190,0.9)'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,0.45)'; ctx.fillRect(f.x - f.w / 2 + 16, f.y - f.h * 0.5, 4, f.h * 0.4);
    // balloon
    const br = balloonR.x;
    if (balloonOn) {
      const by = top - f.neckH;
      ctx.fillStyle = '#e5484d';
      ctx.beginPath(); ctx.roundRect(nl - 3, by - 4, f.neck + 6, 14, 4); ctx.fill();
      const r = Math.max(10, br), cy = by - r * 0.9 - 4;
      ctx.beginPath(); ctx.moveTo(nl - 2, by); ctx.quadraticCurveTo(f.x - r * 1.0, by - r * 0.3, f.x - r, cy); ctx.arc(f.x, cy, r, Math.PI, 0); ctx.quadraticCurveTo(f.x + r * 1.0, by - r * 0.3, nr + 2, by); ctx.closePath();
      const g = ctx.createRadialGradient(f.x - r * 0.35, cy - r * 0.4, r * 0.1, f.x, cy, r * 1.2); g.addColorStop(0, '#ff8a8e'); g.addColorStop(1, '#c81e25');
      ctx.fillStyle = g; ctx.fill();
      if (br > 14) pill(ctx, `${fmt(co2Balloon, 0)} mL of CO₂`, f.x + r + 46, cy, { color: T.red, size: 10.5 });
      else text(ctx, 'tap to remove', f.x + 30, by - 4, T.mute, 9.5, 600);
    } else text(ctx, 'tap the neck to fit the balloon', f.x + 26, top - f.neckH, T.mute, 9.5, 600);
    // equation
    if (!k.small) { card(ctx, w * 0.58, 20, w * 0.4, 70, 12); text(ctx, 'NaHCO₃ + CH₃COOH → CH₃COONa + H₂O + CO₂↑', w * 0.58 + 14, 48, T.ink, 12, 700); text(ctx, 'baking soda + vinegar → sodium acetate + water + carbon dioxide', w * 0.58 + 14, 70, T.ink2, 10, 500); }
    const span = Math.max(30, t);
    plot.range(0, span, 0, Math.max(200, Math.ceil(co2 / 200 + 0.5) * 200)).frame(ctx);
    plot.clip(ctx); plot.ring(ctx, trace, T.green, 2.2); plot.unclip(ctx);
    shelf.draw(ctx);
    const held = shelf.held;
    if (held && shelf.pouring && held.id !== 'soda') { const l = shelf.tipOf(ITEMS.indexOf(held), { x: 0, y: 0 }); stream(ctx, l.x, l.y, f.x, surf, held.color === '#f3e3b0' ? '#e9d48a' : '#9fd0f3', 4); }

    const sodaLeft = sodaSolid * SODA_M, acidLeftmL = acidMol / ACID;
    st.vin.set(`${fmt(vinegar, 0)} mL`); st.soda.set(`${fmt(sodaAdded, 2)} g`);
    st.co2.set(`${fmt(co2, 0)} mL`);
    st.left.set(sodaAdded === 0 ? '—' : sodaLeft > 0.02 && acidMol < 2e-4 ? `${fmt(sodaLeft, 2)} g soda` : acidLeftmL > 0.5 && sodaSolid < 2e-4 ? `${fmt(acidLeftmL, 0)} mL vinegar` : 'reacting…');
    badge.set(vinegar < 1 ? 'Pour some vinegar into the flask' : sodaAdded === 0 ? 'Now spoon in some baking soda' : rate > 2e-5 ? `Fizzing! CO₂ being made: ${fmt(rate * VM, 0)} mL/s` : sodaLeft > 0.02 ? 'The acid has run out: the leftover powder cannot react' : 'The baking soda has run out: add more to fizz again');
    k.animate(moving || rate > 1e-6 || bubbles.n > 0 || grains.n > 0 || balloonR.moving || foam.moving);
  });

  function flaskPath(ctx, nl, nr, top) {
    ctx.beginPath();
    ctx.moveTo(nl - 4, top - f.neckH); ctx.lineTo(nl, top - f.neckH + 4); ctx.lineTo(nl, top);
    ctx.lineTo(f.x - f.w / 2, f.y - 14); ctx.quadraticCurveTo(f.x - f.w / 2, f.y, f.x - f.w / 2 + 14, f.y);
    ctx.lineTo(f.x + f.w / 2 - 14, f.y); ctx.quadraticCurveTo(f.x + f.w / 2, f.y, f.x + f.w / 2, f.y - 14);
    ctx.lineTo(nr, top); ctx.lineTo(nr, top - f.neckH + 4); ctx.lineTo(nr + 4, top - f.neckH);
  }

  k.debug = { slot: (i) => [shelf.slots[i].x, shelf.slots[i].y - 30], mouth: () => [f.x - 10, f.y - f.h - f.neckH - 40], state: () => ({ vinegar, sodaAdded, co2, co2Balloon }) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
