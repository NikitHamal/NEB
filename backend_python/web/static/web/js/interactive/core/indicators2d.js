/**
 * indicators2d — pH from a charge balance and the colours of common indicators, shared by the
 * titration lab and the class 10 indicator tests. pH is solved, not looked up: for a mixture of
 * strong acid, strong base, a weak acid (Ka) and a weak base (Kb) the hydrogen-ion concentration
 * is found by bisection on [H⁺] + [B⁺] + [Na⁺] = [OH⁻] + [Cl⁻] + [A⁻] (Kw = 1.0 × 10⁻¹⁴).
 */
import { mix, clamp } from './kit2d.js';

const KW = 1e-14;

/** All concentrations in mol/L of the final mixture. */
export function solvePH(strongAcid, strongBase, weakAcid = 0, Ka = 1.8e-5, weakBase = 0, Kb = 1.8e-5) {
  let lo = -1, hi = 15;
  for (let i = 0; i < 80; i++) {
    const mid = (lo + hi) / 2, h = Math.pow(10, -mid), oh = KW / h;
    const pos = h + strongBase + weakBase * h / (h + KW / Kb);
    const neg = oh + strongAcid + weakAcid * Ka / (Ka + h);
    if (pos > neg) lo = mid; else hi = mid;
  }
  return (lo + hi) / 2;
}

const UNI = [[0, '#c0262d'], [2, '#e8432e'], [4, '#f08a24'], [5, '#f2c12e'], [6, '#d8d83a'], [7, '#4caf50'], [8, '#2e9e8f'], [9, '#2f6fbf'], [10, '#3b4fb8'], [11, '#5b3aa8'], [14, '#4a1f7a']];
function ramp(stops, x) {
  if (x <= stops[0][0]) return stops[0][1];
  for (let i = 1; i < stops.length; i++) if (x <= stops[i][0]) return mix(stops[i - 1][1], stops[i][1], (x - stops[i - 1][0]) / (stops[i][0] - stops[i - 1][0]));
  return stops[stops.length - 1][1];
}

export const INDICATORS = {
  universal: { label: 'Universal indicator', range: [0, 14], color: (pH) => ramp(UNI, pH), alpha: () => 0.75 },
  litmus: { label: 'Litmus', range: [5, 8], color: (pH) => ramp([[4.5, '#d6336c'], [6.5, '#8e4fa8'], [8.3, '#3b5bdb']], pH), alpha: () => 0.7 },
  phenolphthalein: { label: 'Phenolphthalein', range: [8.2, 10], color: () => '#e64980', alpha: (pH) => clamp((pH - 8.2) / 1.8, 0, 1) * 0.75 },
  methylorange: { label: 'Methyl orange', range: [3.1, 4.4], color: (pH) => ramp([[3.1, '#e03131'], [3.8, '#f76707'], [4.4, '#f2b705']], pH), alpha: () => 0.7 },
};

/** Litmus paper: red paper turns blue in base, blue paper turns red in acid. */
export function litmusPaper(start, pH) {
  if (start === 'red') return pH > 8 ? '#3b5bdb' : pH > 7.2 ? mix('#e8596e', '#3b5bdb', (pH - 7.2) / 0.8) : '#e8596e';
  return pH < 5 ? '#e8596e' : pH < 6.8 ? mix('#e8596e', '#4c6ef5', (pH - 5) / 1.8) : '#4c6ef5';
}

export const PH_SCALE = [
  { pH: 1.5, label: 'stomach acid' }, { pH: 2.2, label: 'lemon juice' }, { pH: 2.9, label: 'vinegar' },
  { pH: 5, label: 'black coffee' }, { pH: 6.5, label: 'milk' }, { pH: 7, label: 'pure water' }, { pH: 7.4, label: 'blood' },
  { pH: 8.3, label: 'baking soda' }, { pH: 10, label: 'soap' }, { pH: 11.6, label: 'ammonia' }, { pH: 12.4, label: 'lime water' },
];

let stripCanvas = null;
/** Draw a universal-indicator pH strip from x to x+w at y with height h; optional pointer. */
export function drawPHStrip(ctx, x, y, w, h, pointer, labels) {
  if (!stripCanvas) {
    stripCanvas = document.createElement('canvas'); stripCanvas.width = 280; stripCanvas.height = 1;
    const g = stripCanvas.getContext('2d');
    for (let i = 0; i < 280; i++) { g.fillStyle = ramp(UNI, i / 20); g.fillRect(i, 0, 1, 1); }
  }
  ctx.drawImage(stripCanvas, x, y, w, h);
  ctx.strokeStyle = 'rgba(23,32,51,0.15)'; ctx.lineWidth = 1; ctx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
  ctx.font = '600 9px Poppins, system-ui, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'top'; ctx.fillStyle = '#4a5770';
  for (let p = 0; p <= 14; p += 1) ctx.fillText(String(p), x + w * p / 14, y + h + 3);
  if (labels) {
    ctx.font = '500 9px Poppins, system-ui, sans-serif'; ctx.fillStyle = '#64748b';
    for (let i = 0; i < PH_SCALE.length; i++) { const s = PH_SCALE[i]; const px = x + w * s.pH / 14; ctx.save(); ctx.translate(px, y - 4); ctx.rotate(-0.6); ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(s.label, 0, 0); ctx.restore(); }
  }
  if (pointer !== undefined && pointer !== null) {
    const px = x + w * clamp(pointer, 0, 14) / 14;
    ctx.fillStyle = '#172033'; ctx.beginPath(); ctx.moveTo(px, y + h + 14); ctx.lineTo(px - 6, y + h + 24); ctx.lineTo(px + 6, y + h + 24); ctx.fill();
  }
}
