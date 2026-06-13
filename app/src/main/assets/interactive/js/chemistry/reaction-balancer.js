import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const ATOM_COLORS = { H: '#f1f5f9', O: '#ef4444', C: '#475569', Fe: '#d97706', N: '#3b82f6' };

const LAYOUTS = {
  'H2': [['H', -4, 0], ['H', 4, 0]],
  'O2': [['O', -5, 0], ['O', 5, 0]],
  'N2': [['N', -5, 0], ['N', 5, 0]],
  'H2O': [['O', 0, -2], ['H', -6, 4], ['H', 6, 4]],
  'CH4': [['C', 0, 0], ['H', 0, -8], ['H', 8, 0], ['H', 0, 8], ['H', -8, 0]],
  'CO2': [['O', -9, 0], ['C', 0, 0], ['O', 9, 0]],
  'Fe': [['Fe', 0, 0]],
  'Fe2O3': [['Fe', -6, -4], ['Fe', 6, -4], ['O', -8, 5], ['O', 0, 7], ['O', 8, 5]],
  'NH3': [['N', 0, -2], ['H', -7, 4], ['H', 0, 6], ['H', 7, 4]],
  'C6H12O6': [['C', -7, -4], ['C', 0, -8], ['C', 7, -4], ['C', 7, 4], ['C', 0, 8], ['C', -7, 4], ['O', -13, 0], ['O', 13, 0], ['O', 0, -14]],
};

const REACTIONS = [
  {
    name: 'Making water: H₂ + O₂ → H₂O',
    left: [{ f: 'H₂', key: 'H2', atoms: { H: 2 } }, { f: 'O₂', key: 'O2', atoms: { O: 2 } }],
    right: [{ f: 'H₂O', key: 'H2O', atoms: { H: 2, O: 1 } }],
  },
  {
    name: 'Methane combustion: CH₄ + O₂ → CO₂ + H₂O',
    left: [{ f: 'CH₄', key: 'CH4', atoms: { C: 1, H: 4 } }, { f: 'O₂', key: 'O2', atoms: { O: 2 } }],
    right: [{ f: 'CO₂', key: 'CO2', atoms: { C: 1, O: 2 } }, { f: 'H₂O', key: 'H2O', atoms: { H: 2, O: 1 } }],
  },
  {
    name: 'Rusting: Fe + O₂ → Fe₂O₃',
    left: [{ f: 'Fe', key: 'Fe', atoms: { Fe: 1 } }, { f: 'O₂', key: 'O2', atoms: { O: 2 } }],
    right: [{ f: 'Fe₂O₃', key: 'Fe2O3', atoms: { Fe: 2, O: 3 } }],
  },
  {
    name: 'Photosynthesis: CO₂ + H₂O → C₆H₁₂O₆ + O₂',
    left: [{ f: 'CO₂', key: 'CO2', atoms: { C: 1, O: 2 } }, { f: 'H₂O', key: 'H2O', atoms: { H: 2, O: 1 } }],
    right: [{ f: 'C₆H₁₂O₆', key: 'C6H12O6', atoms: { C: 6, H: 12, O: 6 } }, { f: 'O₂', key: 'O2', atoms: { O: 2 } }],
  },
  {
    name: 'Ammonia synthesis: N₂ + H₂ → NH₃',
    left: [{ f: 'N₂', key: 'N2', atoms: { N: 2 } }, { f: 'H₂', key: 'H2', atoms: { H: 2 } }],
    right: [{ f: 'NH₃', key: 'NH3', atoms: { N: 1, H: 3 } }],
  },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Not balanced yet', '#f87171');

  let reaction = REACTIONS[0];
  let coeffs = [];
  let hitRects = [];
  let confetti = [];
  let wasBalanced = false;
  let tilt = 0;

  function resetCoeffs() {
    coeffs = new Array(reaction.left.length + reaction.right.length).fill(1);
    confetti = [];
    wasBalanced = false;
  }
  resetCoeffs();

  const panel = createPanel(stage, { title: 'Reaction Controls', collapseOnMobile: true });
  panel.select({
    label: 'Reaction',
    options: REACTIONS.map((r, i) => ({ value: String(i), label: r.name })),
    value: '0',
    onChange: (v) => { reaction = REACTIONS[parseInt(v, 10)]; resetCoeffs(); },
  });
  panel.button({
    label: 'Reset coefficients',
    icon: 'replay',
    variant: 'ghost',
    onClick: resetCoeffs,
  });
  panel.info('Tap the + and − steppers under each substance to set its coefficient. The scale tips until every element has equal atoms on both sides.');

  function species() {
    return [...reaction.left.map((s) => ({ ...s, side: 'L' })), ...reaction.right.map((s) => ({ ...s, side: 'R' }))];
  }

  function tallies() {
    const totals = {};
    species().forEach((s, i) => {
      Object.entries(s.atoms).forEach(([el, n]) => {
        if (!totals[el]) totals[el] = { L: 0, R: 0 };
        totals[el][s.side] += n * coeffs[i];
      });
    });
    return totals;
  }

  function isBalanced(t) {
    return Object.values(t).every((v) => v.L === v.R);
  }

  function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }

  function drawMolecule(ctx, key, x, y, scale) {
    const layout = LAYOUTS[key] || [['C', 0, 0]];
    for (let i = 0; i < layout.length; i++) {
      const [el, dx, dy] = layout[i];
      const r = (el === 'H' ? 3 : el === 'Fe' ? 5 : 4.4) * scale;
      ctx.fillStyle = ATOM_COLORS[el] || '#94a3b8';
      ctx.beginPath();
      ctx.arc(x + dx * scale, y + dy * scale, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.25)';
      ctx.lineWidth = 0.8;
      ctx.stroke();
    }
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    for (const r of hitRects) {
      if (p.x >= r.x && p.x <= r.x + r.w && p.y >= r.y && p.y <= r.y + r.h) {
        coeffs[r.idx] = Math.max(1, Math.min(9, coeffs[r.idx] + r.delta));
        e.preventDefault();
        return;
      }
    }
  }
  sim.canvas.style.touchAction = 'manipulation';
  sim.canvas.addEventListener('pointerdown', onDown);

  function spawnConfetti(w, h) {
    for (let i = 0; i < 60; i++) {
      confetti.push({
        x: w / 2 + (Math.random() - 0.5) * 60,
        y: h * 0.4,
        vx: (Math.random() - 0.5) * 260,
        vy: -120 - Math.random() * 200,
        color: ['#10B981', '#fbbf24', '#7dd3fc', '#f472b6'][i % 4],
        life: 1.6,
      });
    }
  }

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    hitRects = [];
    const sp = species();
    const t = tallies();
    const balanced = isBalanced(t);
    if (balanced && !wasBalanced) spawnConfetti(w, h);
    wasBalanced = balanced;

    let eq = '';
    sp.forEach((s, i) => {
      const sep = i === 0 ? '' : s.side === 'R' && sp[i - 1].side === 'L' ? '  →  ' : ' + ';
      eq += `${sep}${coeffs[i] > 1 ? coeffs[i] : ''}${s.f}`;
    });
    ctx.fillStyle = balanced ? '#8be9a8' : '#e8eefb';
    ctx.font = `700 ${w < 560 ? 15 : 19}px Poppins, sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillText(eq, w / 2, 32);

    const nL = reaction.left.length;
    const nR = reaction.right.length;
    const halfW = w / 2 - 30;
    const colW = (side, n) => halfW / n;
    const colX = (side, j, n) => (side === 'L' ? 16 : w / 2 + 14) + j * colW(side, n) + colW(side, n) / 2;

    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 6]);
    ctx.beginPath();
    ctx.moveTo(w / 2, 48);
    ctx.lineTo(w / 2, h * 0.62);
    ctx.stroke();
    ctx.setLineDash([]);

    const stepY = 64;
    const btn = 34;
    sp.forEach((s, i) => {
      const sideN = s.side === 'L' ? nL : nR;
      const j = s.side === 'L' ? i : i - nL;
      const cx = colX(s.side, j, sideN);

      ctx.fillStyle = 'rgba(13,24,41,0.85)';
      ctx.strokeStyle = 'rgba(255,255,255,0.18)';
      const minusX = cx - btn - 26;
      const plusX = cx + 26;
      [[minusX, '−', -1], [plusX, '+', 1]].forEach(([bx, label, delta]) => {
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(bx, stepY, btn, btn, 9);
        else ctx.rect(bx, stepY, btn, btn);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#9ec1ff';
        ctx.font = '800 20px Poppins, sans-serif';
        ctx.fillText(label, bx + btn / 2, stepY + btn / 2 + 7);
        ctx.fillStyle = 'rgba(13,24,41,0.85)';
        hitRects.push({ x: bx - 5, y: stepY - 5, w: btn + 10, h: btn + 10, idx: i, delta });
      });
      ctx.fillStyle = '#e8eefb';
      ctx.font = '800 22px Poppins, sans-serif';
      ctx.fillText(String(coeffs[i]), cx, stepY + btn / 2 + 8);
      ctx.font = '600 11px Poppins, sans-serif';
      ctx.fillStyle = 'rgba(199,212,234,0.8)';
      ctx.fillText(s.f, cx, stepY + btn + 16);

      const groupTop = stepY + btn + 28;
      const areaH = h * 0.62 - groupTop;
      const perRow = Math.max(1, Math.floor(colW(s.side, sideN) / 42));
      const scale = s.key === 'C6H12O6' ? 1.0 : 1.15;
      for (let m = 0; m < coeffs[i]; m++) {
        const row = Math.floor(m / perRow);
        const col = m % perRow;
        const mx = cx + (col - (Math.min(coeffs[i], perRow) - 1) / 2) * 42;
        const my = groupTop + 18 + row * 38;
        if (my < groupTop + areaH) drawMolecule(ctx, s.key, mx, my, scale);
      }
    });

    const els = Object.keys(t);
    const scaleY = h * 0.78;
    const beamHalf = Math.min(w * 0.26, 190);
    let imbalance = 0;
    els.forEach((el) => { imbalance += t[el].R - t[el].L; });
    const targetTilt = balanced ? 0 : Math.max(-0.14, Math.min(0.14, imbalance * 0.02));
    tilt += (targetTilt - tilt) * Math.min(1, dt * 6);

    ctx.save();
    ctx.translate(w / 2, scaleY);
    ctx.fillStyle = '#5d779e';
    ctx.beginPath();
    ctx.moveTo(-10, 26);
    ctx.lineTo(10, 26);
    ctx.lineTo(3, 0);
    ctx.lineTo(-3, 0);
    ctx.closePath();
    ctx.fill();
    ctx.rotate(tilt);
    ctx.strokeStyle = balanced ? '#10B981' : '#c7d4ea';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(-beamHalf, 0);
    ctx.lineTo(beamHalf, 0);
    ctx.stroke();
    [[-beamHalf, 'L'], [beamHalf, 'R']].forEach(([bx, side]) => {
      ctx.strokeStyle = 'rgba(199,212,234,0.6)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(bx, 0);
      ctx.lineTo(bx - 14, 18);
      ctx.moveTo(bx, 0);
      ctx.lineTo(bx + 14, 18);
      ctx.stroke();
      ctx.strokeStyle = balanced ? '#10B981' : '#c7d4ea';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(bx, 12, 17, 0.15 * Math.PI, 0.85 * Math.PI);
      ctx.stroke();
      let total = 0;
      els.forEach((el) => { total += t[el][side]; });
      ctx.fillStyle = '#e8eefb';
      ctx.font = '700 12px Poppins, sans-serif';
      ctx.fillText(`${total}`, bx, 40);
    });
    ctx.restore();
    ctx.fillStyle = 'rgba(199,212,234,0.65)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText('total atoms each side', w / 2, scaleY + 52);

    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    let ty = h * 0.66;
    els.forEach((el) => {
      const ok = t[el].L === t[el].R;
      ctx.fillStyle = ok ? '#8be9a8' : '#f87171';
      ctx.fillText(`${el}: ${t[el].L} | ${t[el].R} ${ok ? '✓' : '✗'}`, 16, ty);
      ty += 17;
    });

    for (let i = confetti.length - 1; i >= 0; i--) {
      const c = confetti[i];
      c.life -= dt;
      if (c.life <= 0) { confetti.splice(i, 1); continue; }
      c.vy += 380 * dt;
      c.x += c.vx * dt;
      c.y += c.vy * dt;
      ctx.fillStyle = c.color;
      ctx.globalAlpha = Math.min(1, c.life);
      ctx.fillRect(c.x, c.y, 5, 5);
      ctx.globalAlpha = 1;
    }

    if (balanced) {
      const g = coeffs.reduce((a, b) => gcd(a, b));
      statusBadge.set(g > 1 ? 'Balanced — but can you simplify it?' : 'Balanced! Mass is conserved ✓');
      statusBadge.el.style.setProperty('--ix-hud-color', '#10B981');
    } else {
      statusBadge.set('Not balanced yet — check the red elements');
      statusBadge.el.style.setProperty('--ix-hud-color', '#f87171');
    }
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
