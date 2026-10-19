/**
 * Food tests (NEB class 10) — ten food extracts in a rack. Drag iodine, Benedict's or Biuret
 * reagent onto a tube: iodine turns blue-black with starch, Biuret turns violet with protein, and
 * Benedict's only changes when the tube is heated in the water bath — blue, green, yellow, orange
 * or brick red depending on how much reducing sugar there is. Table sugar (sucrose) is a sugar but
 * not a reducing one, so it stays blue: an honest negative.
 */
import { createKit, T, fmt, clamp, background, text, pill, withAlpha } from '../core/kit2d.js';
import { createShelf } from '../core/chem2d.js';
import { createRack, mixHex } from '../core/tubes2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const FOODS = [
  { name: 'Boiled rice', short: 'Rice', s: 0.9, r: 0.02, p: 0.15, base: '#f8f5ec' },
  { name: 'Potato', short: 'Potato', s: 0.85, r: 0.08, p: 0.1, base: '#f6f0dc' },
  { name: 'Bread', short: 'Bread', s: 0.75, r: 0.18, p: 0.3, base: '#f3ead6' },
  { name: 'Ripe banana', short: 'Banana', s: 0.12, r: 0.8, p: 0.05, base: '#f8f1cf' },
  { name: 'Milk', short: 'Milk', s: 0, r: 0.5, p: 0.6, base: '#fbfbf7' },
  { name: 'Egg white', short: 'Egg w.', s: 0, r: 0.02, p: 0.95, base: '#f4f6ee' },
  { name: 'Soybean', short: 'Soybean', s: 0.1, r: 0.05, p: 0.85, base: '#f3eedb' },
  { name: 'Groundnut', short: 'G.nut', s: 0.1, r: 0.05, p: 0.7, base: '#f1e9d6' },
  { name: 'Table sugar (sucrose)', short: 'Sucrose', s: 0, r: 0, p: 0, base: '#f5f8fc' },
  { name: 'Glucose', short: 'Glucose', s: 0, r: 1, p: 0, base: '#f5f8fc' },
];
const REAG = [
  { id: 'iodine', label: 'Iodine', kind: 'object', color: '#c8892b' },
  { id: 'benedict', label: "Benedict's", kind: 'object', color: '#3b82f6' },
  { id: 'biuret', label: 'Biuret', kind: 'object', color: '#7da2e8' },
];
const BEN = ['#3b82f6', '#4caf50', '#d9c13a', '#e8742a', '#b5401f'];
const benColor = (x) => { const f = clamp(x, 0, 1) * 4, i = Math.min(3, Math.floor(f)); return mixHex(BEN[i], BEN[i + 1], f - i); };
const benName = (x) => (x < 0.12 ? 'stays blue' : x < 0.35 ? 'green (a trace)' : x < 0.6 ? 'yellow (some)' : x < 0.85 ? 'orange (a lot)' : 'brick red (very much)');

export default function init(stage) {
  const k = createKit(stage, { label: 'A rack of food extracts with iodine, Benedict\'s and Biuret reagents and a water bath' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag a reagent onto a food tube', T.blue);

  const rack = createRack(k, FOODS.length);
  const st = FOODS.map(() => ({ reag: null, heat: 0, res: {} }));
  let bathOn = false, bathT = 25;
  for (const r of REAG) r.draw = drawDropper;

  const panel = createPanel(stage, { title: 'Food tests' });
  const bathTg = panel.toggle({ label: 'Water bath (boiling)', value: false, onChange: (v) => { bathOn = v; k.animate(true); } });
  panel.button({ label: 'Wash all the tubes', icon: 'water', variant: 'ghost', onClick: wash });
  const table = document.createElement('div'); table.className = 'k2-table'; table.style.setProperty('--k2-cols', 4); panel.body.appendChild(table);
  const last = panel.readout({ label: 'Last result', value: '—' });
  panel.info("Iodine: yellow-brown → blue-black means starch. Benedict's: heat for 2–3 minutes; green → yellow → orange → brick red means more and more reducing sugar. Biuret: blue → violet means protein. Always compare with a control.");

  function wash() { FOODS.forEach((f, i) => { st[i].reag = null; st[i].heat = 0; rack.setColor(i, f.base, 0.5, true); rack.tubes[i].ppt = 0; }); k.animate(true); }
  function renderTable() {
    const cell = (r) => (r ? `<span><i style="display:inline-block;width:11px;height:11px;border-radius:3px;vertical-align:-2px;background:${r.c};box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)"></i> ${r.v}</span>` : '<span>·</span>');
    table.innerHTML = '<div class="k2-tr k2-th"><span>Food</span><span>Starch</span><span>Sugar</span><span>Protein</span></div>' + FOODS.map((f, i) => `<div class="k2-tr"><span>${f.short}</span>${cell(st[i].res.iodine)}${cell(st[i].res.benedict)}${cell(st[i].res.biuret)}</div>`).join('');
  }
  function colorOf(i) {
    const f = FOODS[i], s = st[i];
    if (s.reag === 'iodine') return [mixHex('#c8892b', '#1b2240', clamp((f.s - 0.05) * 1.4, 0, 1)), 0.85];
    if (s.reag === 'biuret') return [mixHex('#7da2e8', '#7d3fbf', clamp((f.p - 0.08) * 1.3, 0, 1)), 0.75];
    if (s.reag === 'benedict') return [benColor(f.r * s.heat), 0.8];
    return [f.base, 0.5];
  }
  function apply(item, i) {
    const f = FOODS[i];
    if (st[i].reag && st[i].reag !== item.id) { badge.set('Use a clean tube for each test: wash the tubes first'); return; }
    st[i].reag = item.id; st[i].heat = 0;
    const [c, a] = colorOf(i); rack.setColor(i, c, a);
    if (item.id === 'iodine') { const pos = f.s > 0.15; st[i].res.iodine = { c, v: pos ? '+' : '−' }; last.set(`${f.name} + iodine: ${pos ? 'blue-black → starch present' : 'stays yellow-brown → no starch'}`); }
    else if (item.id === 'biuret') { const pos = f.p > 0.2; st[i].res.biuret = { c, v: pos ? '+' : '−' }; last.set(`${f.name} + Biuret: ${pos ? 'violet → protein present' : 'stays blue → no protein'}`); }
    else last.set(`Benedict's added to ${f.name}. It stays blue until you heat it in the water bath.`);
    badge.set(last.el.querySelector('.ix-readout-value').textContent);
    renderTable(); k.animate(true);
  }
  const shelf = createShelf(k, REAG, { target: () => ({ x: -999, y: -999, w: 0 }), onPour: () => {}, onDrop: (it, x, y) => { const i = rack.tubeAt(x, y + 30); if (i >= 0) apply(it, i); } });

  let bathY = 0, bathX = 0, bathW = 0;
  k.onResize((w, h) => {
    shelf.layout(k.small ? 10 : w * 0.2, 14, k.small ? w - 20 : w * 0.6, k.small ? 70 : 86);
    rack.layout(k.small ? 2 : w * 0.03, k.small ? 110 : 130, k.small ? w - 4 : w * 0.94, k.small ? h - 170 : h - 210);
    bathX = k.small ? 2 : w * 0.03; bathW = k.small ? w - 4 : w * 0.94; bathY = rack.tubes[0].y - rack.h * 0.45;
  });

  k.frame((ctx, dt, w, h) => {
    bathT += ((bathOn ? 100 : 25) - bathT) * (1 - Math.exp(-dt * 0.8));
    let heating = false;
    for (let i = 0; i < FOODS.length; i++) {
      const t = rack.tubes[i];
      t.heat = bathT > 60 ? 1 : 0; t.bubbles = bathT > 90;
      if (st[i].reag === 'benedict' && bathT > 70 && st[i].heat < 1) {
        st[i].heat = Math.min(1, st[i].heat + dt / 5); heating = true;
        const [c, a] = colorOf(i); rack.setColor(i, c, a);
        t.ppt = FOODS[i].r * st[i].heat > 0.3 ? st[i].heat * 0.8 : 0; t.pptC = benColor(FOODS[i].r);
        if (st[i].heat >= 1) { const x = FOODS[i].r; st[i].res.benedict = { c, v: x > 0.12 ? '+' : '−' }; last.set(`${FOODS[i].name} + Benedict's, heated: ${benName(x)}${FOODS[i].short === 'Sucrose' ? ' — sucrose is not a reducing sugar' : ''}`); badge.set(last.el.querySelector('.ix-readout-value').textContent); renderTable(); }
      }
    }
    const m1 = shelf.step(dt), m2 = rack.step(dt);
    background(k, ctx, w, h);
    ctx.fillStyle = '#c9a77a'; ctx.fillRect(k.small ? 0 : w * 0.18, shelf.slots[0].y, k.small ? w : w * 0.64, 6);
    // water bath behind the lower half of the tubes
    ctx.fillStyle = withAlpha('#bfdbfe', 0.25 + 0.25 * (bathT - 25) / 75); ctx.fillRect(bathX, bathY, bathW, rack.tubes[0].y - bathY + 10);
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 2; ctx.strokeRect(bathX, bathY - 8, bathW, rack.tubes[0].y - bathY + 18);
    if (bathT > 90) { ctx.fillStyle = 'rgba(255,255,255,0.7)'; for (let b = 0; b < 30; b++) { const bx = bathX + ((b * 97) % bathW), by = rack.tubes[0].y - ((k.t * 50 + b * 31) % (rack.tubes[0].y - bathY)); ctx.beginPath(); ctx.arc(bx, by, 2, 0, Math.PI * 2); ctx.fill(); } }
    pill(ctx, `water bath ${fmt(bathT, 0)} °C`, bathX + 70, bathY - 8, { color: bathT > 90 ? T.red : T.ink2, size: 10 });
    for (let i = 0; i < FOODS.length; i++) { rack.tubes[i].label = FOODS[i].short; rack.tubes[i].sub = st[i].reag ? REAG.find((r) => r.id === st[i].reag).label : ''; }
    rack.draw(ctx);
    shelf.draw(ctx);
    const held = shelf.held;
    if (held) { const i = rack.tubeAt(k.pointer.x, k.pointer.y + 30); if (i >= 0) { const t = rack.tubes[i]; ctx.strokeStyle = withAlpha(T.blue, 0.6); ctx.lineWidth = 2; ctx.setLineDash([4, 4]); ctx.strokeRect(t.x - rack.gap / 2 + 3, t.y - rack.h - 20, rack.gap - 6, rack.h + 50); ctx.setLineDash([]); } }
    k.animate(m1 || m2 || heating || Math.abs(bathT - (bathOn ? 100 : 25)) > 0.5 || bathT > 90);
  });

  wash(); renderTable();
  k.debug = { reagent: (j) => [shelf.slots[j].x, shelf.slots[j].y - 20], tube: (i) => [rack.tubes[i].x, rack.tubes[i].y - rack.h * 0.6], apply: (j, i) => apply(REAG[j], i), bath: (v) => { bathOn = v; bathTg.set(v); k.animate(true); }, res: () => st.map((s) => s.res) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}

function drawDropper(ctx, it) {
  ctx.fillStyle = 'rgba(219,234,254,0.85)'; ctx.strokeStyle = 'rgba(100,130,170,0.8)'; ctx.lineWidth = 1.2;
  ctx.beginPath(); ctx.roundRect(-13, -38, 26, 36, 4); ctx.fill(); ctx.stroke();
  ctx.fillStyle = withAlpha(it.color, 0.85); ctx.fillRect(-11, -22, 22, 18);
  ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.roundRect(-6, -56, 12, 18, 5); ctx.fill();
  ctx.fillStyle = 'rgba(220,235,250,0.95)'; ctx.fillRect(-2, -68, 4, 13);
}
