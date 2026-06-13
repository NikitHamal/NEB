import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawBeaker, text, roundRect } from './chem-utils.js';

const SOLUTIONS = [
  { id: 'hcl', label: 'Dilute HCl (0.1 M)', ph: 1.0 },
  { id: 'lemon', label: 'Lemon juice', ph: 2.4 },
  { id: 'vinegar', label: 'Vinegar', ph: 2.9 },
  { id: 'soda', label: 'Soda water', ph: 4.5 },
  { id: 'milk', label: 'Milk', ph: 6.6 },
  { id: 'water', label: 'Distilled water', ph: 7.0 },
  { id: 'blood', label: 'Blood (buffered!)', ph: 7.4, buffer: true },
  { id: 'baking', label: 'Baking soda solution', ph: 8.4 },
  { id: 'soap', label: 'Soap solution', ph: 9.6 },
  { id: 'lime', label: 'Lime water', ph: 11.0 },
  { id: 'naoh', label: 'Dilute NaOH (0.1 M)', ph: 13.0 },
];

function uiColor(ph) {
  if (ph < 2) return '#dc2626';
  if (ph < 4) return '#f97316';
  if (ph < 6) return '#facc15';
  if (ph < 6.8) return '#a3e635';
  if (ph < 7.5) return '#22c55e';
  if (ph < 9) return '#14b8a6';
  if (ph < 11) return '#3b82f6';
  return '#7c3aed';
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Pick a solution and an indicator', '#047857');

  let sol = SOLUTIONS[0];
  let indicator = 'universal';
  let addedAcid = 0;
  let addedBase = 0;
  let t = 0;

  function effectivePH() {
    let ph = sol.ph;
    const shift = (addedBase - addedAcid) * (sol.buffer ? 0.18 : 1.4);
    ph = Math.max(0.3, Math.min(13.7, ph + shift));
    return ph;
  }

  const panel = createPanel(stage, { title: 'pH Bench' });
  panel.select({
    label: 'Solution',
    options: SOLUTIONS.map((s) => ({ value: s.id, label: s.label })),
    value: sol.id,
    onChange: (v) => {
      sol = SOLUTIONS.find((s) => s.id === v);
      addedAcid = 0;
      addedBase = 0;
      badge.set(`Testing: ${sol.label}`);
      badge.el.style.setProperty('--ix-hud-color', uiColor(sol.ph));
      if (sol.buffer) showInfoCard(stage, { title: 'A natural buffer', body: 'Blood is buffered by the H₂CO₃/HCO₃⁻ pair. Try adding acid or base — the pH barely moves. Your body keeps blood between 7.35 and 7.45 or cells stop working.', color: '#10b981' });
    },
  });
  panel.select({
    label: 'Indicator / meter',
    options: [
      { value: 'universal', label: 'Universal indicator' },
      { value: 'litmus', label: 'Litmus paper' },
      { value: 'paper', label: 'pH paper strip' },
      { value: 'meter', label: 'Digital pH meter' },
    ],
    value: indicator,
    onChange: (v) => { indicator = v; },
  });
  panel.divider();
  panel.section('Disturb the solution');
  panel.buttonRow([
    { label: '+ acid drop', icon: 'remove', onClick: () => { addedAcid += 1; nudge(); } },
    { label: '+ base drop', icon: 'add', onClick: () => { addedBase += 1; nudge(); } },
  ]);
  const phOut = panel.readout({ label: 'True pH', value: '1.0' });
  panel.button({ label: 'Reset drops', icon: 'replay', variant: 'ghost', onClick: () => { addedAcid = 0; addedBase = 0; } });
  panel.info('Litmus only says acid-or-base. pH paper gives a rough number. Universal indicator shows a colour spectrum. The meter reads to 0.01 — but must be calibrated with buffer solutions first!');

  function nudge() {
    const ph = effectivePH();
    badge.set(sol.buffer ? `Buffer resists! pH ${ph.toFixed(2)}` : `pH now ${ph.toFixed(2)}`);
    badge.el.style.setProperty('--ix-hud-color', uiColor(ph));
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    const ph = effectivePH();
    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.85;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const cx = w * 0.3;
    const liqRGBA = indicator === 'universal' ? hexA(uiColor(ph), 0.55) : 'rgba(203,213,225,0.3)';
    drawBeaker(ctx, cx - 50, benchY - 110, 100, 106, 0.6, liqRGBA, sol.label);

    if (indicator === 'litmus') {
      ctx.fillStyle = ph < 7 ? '#ef4444' : ph > 7 ? '#3b82f6' : '#a78bfa';
      ctx.fillRect(cx - 8, benchY - 150, 16, 52);
      text(ctx, ph < 6.5 ? 'red → ACID' : ph > 7.5 ? 'blue → BASE' : 'purple-ish → near neutral', cx, benchY - 160, { color: '#e2e8f0' });
    } else if (indicator === 'paper') {
      ctx.fillStyle = uiColor(ph);
      ctx.fillRect(cx - 8, benchY - 150, 16, 52);
      text(ctx, `matches chart ≈ pH ${Math.round(ph)}`, cx, benchY - 160, { color: '#e2e8f0' });
    } else if (indicator === 'meter') {
      ctx.fillStyle = '#1e293b';
      roundRect(ctx, cx + 64, benchY - 170, 84, 46, 6);
      ctx.fill();
      ctx.strokeStyle = '#64748b';
      ctx.stroke();
      text(ctx, ph.toFixed(2), cx + 106, benchY - 142, { color: '#34d399', font: '700 18px monospace' });
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(cx + 80, benchY - 124);
      ctx.lineTo(cx + 20, benchY - 60);
      ctx.stroke();
      text(ctx, 'glass electrode', cx + 70, benchY - 100, { align: 'left' });
    } else {
      text(ctx, 'colour shows the pH directly', cx, benchY - 130, { color: uiColor(ph) });
    }

    const sx = w * 0.08;
    const sw = w * 0.84;
    const sy = h * 0.08;
    for (let i = 0; i <= 13; i++) {
      ctx.fillStyle = uiColor(i + 0.5);
      ctx.fillRect(sx + (i / 14) * sw, sy, sw / 14 - 1, 14);
    }
    text(ctx, '0', sx, sy + 28, { align: 'left' });
    text(ctx, '7', sx + sw / 2, sy + 28);
    text(ctx, '14', sx + sw, sy + 28, { align: 'right' });
    const mark = sx + (ph / 14) * sw;
    ctx.fillStyle = '#f8fafc';
    ctx.beginPath();
    ctx.moveTo(mark, sy + 18);
    ctx.lineTo(mark - 5, sy + 26);
    ctx.lineTo(mark + 5, sy + 26);
    ctx.fill();
    text(ctx, `pH ${ph.toFixed(2)} — ${ph < 6.8 ? 'acidic' : ph > 7.2 ? 'basic' : 'neutral'}`, mark, sy + 44, { color: uiColor(ph), font: '700 11px Poppins, sans-serif' });

    if (sol.buffer && (addedAcid || addedBase)) {
      text(ctx, 'buffer action: H₂CO₃ / HCO₃⁻ absorbs the added H⁺ or OH⁻', w / 2, h - 10, { color: '#34d399' });
    }
    phOut.set(ph.toFixed(2));
  });

  function hexA(hex, a) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${a})`;
  }

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
