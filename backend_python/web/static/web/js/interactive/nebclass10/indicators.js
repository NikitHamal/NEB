import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Acid–base indicator bench: choose a solution and an indicator, then watch the
// colour change. The pH values are the standard ones used in the grade-10 book.

const NEUTRAL = '#a7c7e7';

const SOLUTIONS = [
  { id: 'lemon', name: 'Lemon juice', ph: 2.2, kind: 'acid' },
  { id: 'vinegar', name: 'Vinegar', ph: 3.0, kind: 'acid' },
  { id: 'curd', name: 'Curd (dahi)', ph: 4.5, kind: 'acid' },
  { id: 'water', name: 'Distilled water', ph: 7.0, kind: 'neutral' },
  { id: 'salt', name: 'Common salt solution', ph: 7.0, kind: 'neutral' },
  { id: 'milk', name: 'Milk of magnesia', ph: 10.0, kind: 'base' },
  { id: 'soap', name: 'Soap solution', ph: 9.5, kind: 'base' },
  { id: 'lime', name: 'Lime water', ph: 12.0, kind: 'base' },
  { id: 'soda', name: 'Baking soda solution', ph: 8.5, kind: 'base' },
];

const INDICATORS = [
  { id: 'litmus', name: 'Litmus paper (blue)', color: (s) => (s.kind === 'acid' ? '#e0454a' : s.kind === 'base' ? '#2f66c9' : '#4b6d9a'),
    note: (s) => (s.kind === 'acid' ? 'Blue litmus turns red in an acid.' : s.kind === 'base' ? 'Blue litmus stays blue in a base.' : 'Blue litmus shows no change in a neutral solution.') },
  { id: 'litmusr', name: 'Litmus paper (red)', color: (s) => (s.kind === 'base' ? '#2f66c9' : '#e0454a'),
    note: (s) => (s.kind === 'base' ? 'Red litmus turns blue in a base.' : 'Red litmus stays red in an acid or a neutral solution.') },
  { id: 'phenol', name: 'Phenolphthalein', color: (s) => (s.kind === 'base' ? '#f0569f' : 'rgba(255,255,255,0.14)'),
    note: (s) => (s.kind === 'base' ? 'Phenolphthalein turns pink in a base.' : 'Phenolphthalein stays colourless in an acid and in a neutral solution.') },
  { id: 'methyl', name: 'Methyl orange', color: (s) => (s.kind === 'acid' ? '#e8623c' : s.kind === 'base' ? '#f2c53d' : '#e8a33c'),
    note: (s) => (s.kind === 'acid' ? 'Methyl orange turns red-orange in an acid.' : s.kind === 'base' ? 'Methyl orange turns yellow in a base.' : 'Methyl orange stays orange in a neutral solution.') },
  { id: 'universal', name: 'Universal indicator', color: (s) => {
    if (s.ph < 3) return '#d7263d';
    if (s.ph < 5) return '#e8623c';
    if (s.ph < 6.5) return '#f2c53d';
    if (s.ph <= 7.5) return '#4caf50';
    if (s.ph < 9) return '#2196a6';
    if (s.ph < 11) return '#2f66c9';
    return '#5b2fa8';
  },
  note: (s) => (s.kind === 'acid' ? 'Universal indicator shows red to orange in an acid.' : s.kind === 'base' ? 'Universal indicator shows blue to violet in a base.' : 'Universal indicator shows green in a neutral solution.') },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Pick a solution, then an indicator', '#10B981');

  let solution = SOLUTIONS[0];
  let indicator = INDICATORS[0];
  let drops = 0;

  const panel = createPanel(stage, { title: 'Indicator tests' });
  const solSel = panel.select({
    label: 'Solution in the test tube',
    options: SOLUTIONS.map((s) => ({ value: s.id, label: `${s.name} (pH ${s.ph.toFixed(1)})` })),
    value: solution.id,
    onChange: (id) => { solution = SOLUTIONS.find((s) => s.id === id); drops = 0; update(); },
  });
  const indSel = panel.select({
    label: 'Indicator added',
    options: INDICATORS.map((i) => ({ value: i.id, label: i.name })),
    value: indicator.id,
    onChange: (id) => { indicator = INDICATORS.find((i) => i.id === id); drops = 0; update(); },
  });
  panel.buttonRow([
    { label: 'Add drops', icon: 'water_drop', onClick: () => { drops = Math.min(6, drops + 1); update(); } },
    { label: 'Rinse tube', icon: 'cleaning_services', variant: 'ghost', onClick: () => { drops = 0; update(); } },
  ]);
  const readPH = panel.readout({ label: 'pH', value: '—' });
  const readKind = panel.readout({ label: 'Nature', value: '—' });
  const readResult = panel.readout({ label: 'Observation', value: '—' });
  const info = panel.info('');

  function isLitmus() { return indicator.id === 'litmus' || indicator.id === 'litmusr'; }

  function acidBaseBar(ctx, x, y, w, h, ph) {
    const grad = ctx.createLinearGradient(x, 0, x + w, 0);
    grad.addColorStop(0, '#d7263d');
    grad.addColorStop(0.35, '#f2c53d');
    grad.addColorStop(0.5, '#4caf50');
    grad.addColorStop(0.68, '#2196a6');
    grad.addColorStop(1, '#5b2fa8');
    ctx.fillStyle = grad;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, 4); else ctx.rect(x, y, w, h);
    ctx.fill();
    const px = x + (Math.max(0, Math.min(14, ph)) / 14) * w;
    ctx.strokeStyle = '#f8fafc';
    ctx.lineWidth = 2.4;
    ctx.beginPath(); ctx.moveTo(px, y - 5); ctx.lineTo(px, y + h + 5); ctx.stroke();
    ctx.fillStyle = 'rgba(232,238,251,0.85)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('acidic', x + w * 0.16, y + h + 20);
    ctx.fillText('neutral', x + w * 0.5, y + h + 20);
    ctx.fillText('basic', x + w * 0.84, y + h + 20);
    for (let i = 0; i <= 14; i += 2) {
      const tx = x + (i / 14) * w;
      ctx.strokeStyle = 'rgba(2,6,23,0.35)';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(tx, y + h); ctx.lineTo(tx, y + h + 4); ctx.stroke();
      ctx.fillStyle = 'rgba(199,212,234,0.75)';
      ctx.fillText(String(i), tx, y + h + 14);
    }
  }

  function draw(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);

    // bench
    ctx.fillStyle = 'rgba(148,163,184,0.12)';
    ctx.fillRect(0, h * 0.78, w, h * 0.22);

    // test tube
    const tubeW = Math.min(110, w * 0.2);
    const tubeH = h * 0.6;
    const tx = w * 0.2;
    const ty = h * 0.14;
    ctx.strokeStyle = 'rgba(232,238,251,0.8)';
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(tx, ty, tubeW, tubeH, [6, 6, tubeW / 2, tubeW / 2]);
    else ctx.rect(tx, ty, tubeW, tubeH);
    ctx.stroke();
    ctx.save();
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(tx, ty, tubeW, tubeH, [6, 6, tubeW / 2, tubeW / 2]);
    else ctx.rect(tx, ty, tubeW, tubeH);
    ctx.clip();
    const liquidH = tubeH * 0.72;
    const ly = ty + tubeH - liquidH;
    const base = indicator.color(solution);
    const mixed = drops === 0 && !isLitmus() ? NEUTRAL : base;
    const alpha = drops === 0 ? 0.35 : Math.min(1, 0.35 + drops * 0.11);
    ctx.globalAlpha = alpha;
    ctx.fillStyle = solution.kind === 'neutral' && drops === 0 ? 'rgba(167,199,231,0.75)' : mixed;
    ctx.fillRect(tx, ly, tubeW, liquidH);
    ctx.globalAlpha = 1;
    ctx.restore();
    ctx.fillStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(solution.name, tx + tubeW / 2, ty - 14);

    // drops
    if (drops === 0) {
      ctx.fillStyle = 'rgba(199,212,234,0.7)';
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.fillText('no indicator yet', tx + tubeW / 2, ty + tubeH + 20);
    } else {
      for (let i = 0; i < drops; i++) {
        ctx.fillStyle = '#f8fafc';
        ctx.beginPath();
        ctx.arc(tx + tubeW / 2 + (i - (drops - 1) / 2) * 12, ty - 34, 3.6, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // pH scale
    acidBaseBar(ctx, w * 0.44, h * 0.26, w * 0.5, 16, solution.ph);

    // result card
    const kindColor = solution.kind === 'acid' ? '#fb7185' : solution.kind === 'base' ? '#60a5fa' : '#4ade80';
    ctx.fillStyle = 'rgba(8,16,30,0.8)';
    ctx.strokeStyle = kindColor;
    ctx.lineWidth = 1.4;
    const cx = w * 0.44; const cy = h * 0.5; const cw = w * 0.5; const ch = h * 0.28;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(cx, cy, cw, ch, 8); else ctx.rect(cx, cy, cw, ch);
    ctx.fill(); ctx.stroke();
    ctx.textAlign = 'left';
    ctx.fillStyle = kindColor;
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.fillText(solution.kind === 'acid' ? 'ACIDIC solution' : solution.kind === 'base' ? 'BASIC solution' : 'NEUTRAL solution', cx + 14, cy + 24);
    ctx.fillStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '600 10.5px Poppins, sans-serif';
    const note = drops === 0 ? 'Add a few drops of the indicator to see the change.' : indicator.note(solution);
    wrapText(ctx, note, cx + 14, cy + 46, cw - 28, 15);
    ctx.fillStyle = 'rgba(199,212,234,0.75)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText(`Colour now: ${drops === 0 ? 'unchanged' : describe(base)}`, cx + 14, cy + ch - 16);

    readPH.set(solution.ph.toFixed(1));
    readKind.set(solution.kind === 'acid' ? 'acidic' : solution.kind === 'base' ? 'basic' : 'neutral');
    readResult.set(drops === 0 ? 'add the indicator' : describe(base));
    info.set(`${solution.name} has pH ${solution.ph.toFixed(1)}, so it is ${solution.kind === 'acid' ? 'acidic' : solution.kind === 'base' ? 'basic' : 'neutral'}. ${drops === 0 ? '' : indicator.note(solution)}`);
    void solSel; void indSel;
  }

  function describe(color) {
    if (typeof color !== 'string' || color.startsWith('rgba')) return 'colourless';
    const map = {
      '#e0454a': 'red', '#2f66c9': 'blue', '#f0569f': 'pink', '#e8623c': 'red-orange',
      '#f2c53d': 'yellow', '#e8a33c': 'orange', '#d7263d': 'red', '#4caf50': 'green',
      '#2196a6': 'blue-green', '#5b2fa8': 'violet',
    };
    return map[color] || 'changed';
  }

  function wrapText(ctx, text, x, y, maxW, lh) {
    const words = String(text).split(' ');
    let line = '';
    let ly = y;
    words.forEach((word) => {
      const test = line ? `${line} ${word}` : word;
      if (ctx.measureText(test).width > maxW && line) {
        ctx.fillText(line, x, ly);
        line = word;
        ly += lh;
      } else {
        line = test;
      }
    });
    if (line) ctx.fillText(line, x, ly);
  }

  function update() { sim.renderOnce(); }
  sim.setUpdate(draw);
  sim.onResize(() => sim.renderOnce());
  sim.start();
  update();

  return {
    dispose() { sim.dispose(); hud.dispose(); panel.dispose(); },
  };
}
