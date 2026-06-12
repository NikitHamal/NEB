import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, labelText, panelBg } from './lab-utils.js';

const SURFACES = {
  wood: { label: 'Wood on wood', mus: 0.42, muk: 0.32 },
  rubber: { label: 'Rubber on concrete', mus: 0.75, muk: 0.6 },
  steel: { label: 'Steel on steel', mus: 0.58, muk: 0.45 },
  ice: { label: 'Wood on ice', mus: 0.1, muk: 0.05 },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Block at rest', '#9ec1ff');

  let mode = 'incline';
  let surfKey = 'wood';
  let mus = 0;
  let muk = 0;
  let angle = 5;
  let mass = 1;
  let pull = 0;
  let blockS = 0;
  let blockV = 0;
  let slipping = false;
  let reposeAngle = null;
  let showForces = true;
  const g = 9.8;

  function rollSurface() {
    const s = SURFACES[surfKey];
    mus = s.mus + (Math.random() - 0.5) * 0.04;
    muk = s.muk + (Math.random() - 0.5) * 0.03;
    resetBlock();
    reposeAngle = null;
  }

  function resetBlock() {
    blockS = 0;
    blockV = 0;
    slipping = false;
  }

  const panel = createPanel(stage, { title: 'Friction Lab' });
  panel.select({
    label: 'Mode',
    options: [
      { value: 'incline', label: 'Inclined plane (angle of repose)' },
      { value: 'pull', label: 'Horizontal pull (spring balance)' },
    ],
    value: mode,
    onChange: (v) => { mode = v; resetBlock(); },
  });
  panel.select({
    label: 'Surfaces',
    options: Object.entries(SURFACES).map(([value, s]) => ({ value, label: s.label })),
    value: surfKey,
    onChange: (v) => { surfKey = v; rollSurface(); },
  });
  panel.slider({
    label: 'Incline angle θ',
    min: 0, max: 45, step: 0.5, value: angle,
    format: (v) => `${v.toFixed(1)}°`,
    onChange: (v) => { angle = v; if (!slipping) blockS = 0; },
  });
  panel.slider({
    label: 'Block mass',
    min: 0.5, max: 3, step: 0.25, value: mass,
    format: (v) => `${v.toFixed(2)} kg`,
    onChange: (v) => { mass = v; },
  });
  panel.slider({
    label: 'Applied pull F',
    min: 0, max: 25, step: 0.1, value: 0,
    format: (v) => `${v.toFixed(1)} N`,
    onChange: (v) => { pull = v; },
  });
  panel.toggle({ label: 'Show force arrows', value: true, onChange: (v) => { showForces = v; } });
  panel.buttonRow([
    { label: 'Reset block', icon: 'replay', onClick: resetBlock },
    { label: 'New surface', icon: 'refresh', onClick: rollSurface },
  ]);
  panel.divider();
  const tanOut = panel.readout({ label: 'tan θ', value: '—' });
  const repOut = panel.readout({ label: 'Angle of repose θᵣ', value: '—' });
  const muOut = panel.readout({ label: 'μₛ = tan θᵣ', value: '—' });
  const springOut = panel.readout({ label: 'Spring balance', value: '—' });
  panel.info('Incline mode: raise θ slowly until the block just slips — that is the angle of repose. Pull mode: increase F until the block just moves; then μₛ = F/mg.');

  rollSurface();

  sim.setUpdate((ctx, dt, w, h) => {
    const th = (angle * Math.PI) / 180;
    if (mode === 'incline') {
      if (!slipping && Math.tan(th) > mus) {
        slipping = true;
        if (reposeAngle === null) reposeAngle = angle;
      }
      if (slipping) {
        const a = g * (Math.sin(th) - muk * Math.cos(th));
        blockV += Math.max(0, a) * dt;
        blockS += blockV * dt;
        if (blockS > 2.2) resetBlock();
        if (Math.tan(th) < muk) { blockV = 0; slipping = false; }
      }
    } else {
      const N = mass * g;
      if (!slipping && pull > mus * N) slipping = true;
      if (slipping) {
        const a = (pull - muk * N) / mass;
        blockV += a * dt;
        if (blockV < 0) { blockV = 0; slipping = false; }
        blockS += blockV * dt;
        if (blockS > 2.2) { blockS = 0; }
      }
    }

    ctx.clearRect(0, 0, w, h);
    if (mode === 'incline') drawIncline(ctx, w, h, th);
    else drawPull(ctx, w, h);

    tanOut.set(mode === 'incline' ? fmt(Math.tan(th), 3) : '—');
    repOut.set(reposeAngle === null ? 'not found yet' : `${fmt(reposeAngle, 1)}°`);
    muOut.set(reposeAngle === null ? '—' : `${fmt(Math.tan((reposeAngle * Math.PI) / 180), 2)}`);
    const N = mass * g;
    const fNeeded = mus * N;
    springOut.set(mode === 'pull' ? `${fmt(pull, 1)} N (slips above ≈ ${fmt(fNeeded, 1)} N)` : '—');
    statusBadge.set(slipping ? (mode === 'incline' ? 'Slipping! θᵣ recorded' : 'Block sliding') : 'Block at rest (static friction)');
  });

  function drawIncline(ctx, w, h, th) {
    const baseY = h * 0.78;
    const baseX = w * 0.12;
    const len = w * 0.72;
    ctx.fillStyle = '#2b3a57';
    ctx.beginPath();
    ctx.moveTo(baseX, baseY);
    ctx.lineTo(baseX + len, baseY);
    ctx.lineTo(baseX + len, baseY - Math.tan(th) * len);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = 'rgba(158,193,255,0.5)';
    ctx.stroke();
    const s = Math.min(0.85, 0.25 + blockS / 2.2) * len;
    const bx = baseX + len - s * Math.cos(0);
    const hx = bx;
    const hy = baseY - Math.tan(th) * (hx - baseX);
    ctx.save();
    ctx.translate(hx, hy);
    ctx.rotate(-th);
    ctx.fillStyle = '#D97706';
    ctx.fillRect(-22, -30, 44, 30);
    ctx.fillStyle = 'rgba(255,255,255,0.15)';
    ctx.fillRect(-22, -30, 44, 7);
    if (showForces) {
      arrow(ctx, 0, -15, 0, -15 + 46, '#ff8c8c');
      labelText(ctx, 'mg', 6, 38, { size: 9, weight: 600, color: '#ff8c8c' });
      arrow(ctx, 0, -30, 0, -30 - 34 * Math.cos(th), '#9ec1ff');
      labelText(ctx, 'N', 6, -40, { size: 9, weight: 600, color: '#9ec1ff' });
      arrow(ctx, -22, -8, -22 - (slipping ? -28 : 28), -8, '#8be9a8');
      labelText(ctx, 'f', -38, -14, { size: 9, weight: 600, color: '#8be9a8' });
    }
    ctx.restore();
    ctx.strokeStyle = 'rgba(199,212,234,0.5)';
    ctx.beginPath();
    ctx.arc(baseX + len, baseY, 46, Math.PI, Math.PI + th, false);
    ctx.stroke();
    labelText(ctx, `θ = ${angle.toFixed(1)}°`, baseX + len - 92, baseY - 12, { size: 11 });
    panelBg(ctx, 12, 12, Math.min(200, w * 0.55), 44);
    labelText(ctx, 'Block slips when tan θ > μₛ', 22, 30, { size: 9.5, weight: 600, color: 'rgba(199,212,234,0.85)' });
    labelText(ctx, `surface: ${SURFACES[surfKey].label}`, 22, 46, { size: 9.5, weight: 600, color: '#ffd584' });
  }

  function drawPull(ctx, w, h) {
    const floorY = h * 0.6;
    ctx.fillStyle = '#2b3a57';
    ctx.fillRect(0, floorY, w, 14);
    const bx = w * 0.2 + (blockS / 2.2) * w * 0.4;
    ctx.fillStyle = '#D97706';
    ctx.fillRect(bx - 26, floorY - 38, 52, 38);
    ctx.fillStyle = 'rgba(255,255,255,0.15)';
    ctx.fillRect(bx - 26, floorY - 38, 52, 8);
    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(bx + 26, floorY - 19);
    ctx.lineTo(bx + 70, floorY - 19);
    ctx.stroke();
    panelBg(ctx, bx + 70, floorY - 34, 92, 30);
    labelText(ctx, `${fmt(pull, 1)} N`, bx + 116, floorY - 14, { size: 12, align: 'center', color: '#8be9a8' });
    ctx.strokeStyle = '#c7d4ea';
    ctx.beginPath();
    ctx.moveTo(bx + 162, floorY - 19);
    ctx.lineTo(bx + 186, floorY - 19);
    ctx.stroke();
    if (showForces) {
      const fric = slipping ? muk * mass * 9.8 : Math.min(pull, mus * mass * 9.8);
      arrow(ctx, bx, floorY - 19, bx + Math.min(70, pull * 4), floorY - 19, '#8be9a8');
      arrow(ctx, bx, floorY - 4, bx - Math.min(64, fric * 4), floorY - 4, '#ff8c8c');
      labelText(ctx, 'friction', bx - 60, floorY + 18, { size: 9, weight: 600, color: '#ff8c8c' });
    }
    labelText(ctx, `m = ${mass.toFixed(2)} kg · N = mg = ${fmt(mass * 9.8, 1)} N`, w * 0.5, floorY + 40, { size: 10.5, align: 'center' });
    labelText(ctx, `surface: ${SURFACES[surfKey].label}`, w * 0.5, floorY + 58, { size: 9.5, weight: 600, align: 'center', color: '#ffd584' });
  }

  function arrow(ctx, x0, y0, x1, y1, color) {
    if (Math.hypot(x1 - x0, y1 - y0) < 2) return;
    const ang = Math.atan2(y1 - y0, x1 - x0);
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 - 8 * Math.cos(ang - 0.42), y1 - 8 * Math.sin(ang - 0.42));
    ctx.lineTo(x1 - 8 * Math.cos(ang + 0.42), y1 - 8 * Math.sin(ang + 0.42));
    ctx.closePath();
    ctx.fill();
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
