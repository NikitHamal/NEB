import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawBeaker, drawBurner, text } from './chem-utils.js';

const SALTS = [
  { id: 'na', name: 'NaCl', ion: 'Na⁺ (sodium)', color: '#fbbf24', glow: 'rgba(251,191,36,0.5)', desc: 'Intense golden-yellow' },
  { id: 'k', name: 'KCl', ion: 'K⁺ (potassium)', color: '#c4b5fd', glow: 'rgba(196,181,253,0.45)', desc: 'Lilac / pale violet' },
  { id: 'ca', name: 'CaCl₂', ion: 'Ca²⁺ (calcium)', color: '#f97316', glow: 'rgba(249,115,22,0.45)', desc: 'Brick-red / orange-red' },
  { id: 'cu', name: 'CuSO₄', ion: 'Cu²⁺ (copper)', color: '#34d399', glow: 'rgba(52,211,153,0.45)', desc: 'Blue-green' },
  { id: 'sr', name: 'SrCl₂', ion: 'Sr²⁺ (strontium)', color: '#ef4444', glow: 'rgba(239,68,68,0.5)', desc: 'Crimson red' },
  { id: 'ba', name: 'BaCl₂', ion: 'Ba²⁺ (barium)', color: '#a3e635', glow: 'rgba(163,230,53,0.45)', desc: 'Apple-green (pale)' },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Clean the loop first!', '#059669');

  let loopState = 'dirty';
  let loopSalt = null;
  let inFlame = 0;
  let holding = false;
  let mode = 'practice';
  let unknown = null;
  let isUnknown = false;
  let solved = 0;
  let t = 0;

  const panel = createPanel(stage, { title: 'Flame Test Bench' });
  panel.buttonRow([
    { label: 'Practice', icon: 'school', onClick: () => setMode('practice') },
    { label: 'Identify!', icon: 'quiz', onClick: () => setMode('identify') },
  ]);
  panel.divider();
  const loopOut = panel.readout({ label: 'Wire loop', value: 'dirty (old residue)' });
  panel.button({ label: 'Clean loop in conc. HCl', icon: 'cleaning_services', onClick: () => {
    loopState = 'clean';
    loopSalt = null;
    badge.set('Loop cleaned in HCl — gives no colour now');
    badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
  } });
  const saltSel = panel.select({
    label: 'Dip into salt',
    options: [{ value: '', label: '— choose a salt —' }].concat(SALTS.map((s) => ({ value: s.id, label: s.name }))),
    value: '',
    onChange: (v) => {
      if (!v) return;
      loopSalt = SALTS.find((s) => s.id === v);
      isUnknown = false;
      badge.set(`Loop dipped in ${loopSalt.name}. Hold it in the flame!`);
      badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
    },
  });
  panel.button({ label: 'Dip in UNKNOWN sample', icon: 'help', onClick: () => {
    if (mode !== 'identify') return;
    loopSalt = unknown;
    isUnknown = true;
    badge.set('Loop dipped in the unknown. Into the flame!');
    badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
  } });
  const holdBtn = panel.button({ label: 'Hold loop in flame', icon: 'local_fire_department', onClick: () => {} });
  panel.divider();
  panel.section('Your conclusion (identify mode)');
  const guessSel = panel.select({
    label: 'The cation is…',
    options: [{ value: '', label: '— pick —' }].concat(SALTS.map((s) => ({ value: s.id, label: s.ion }))),
    value: '',
    onChange: (v) => {
      if (mode !== 'identify' || !v) return;
      if (v === unknown.id) {
        solved++;
        showInfoCard(stage, { title: 'Correct!', body: `The unknown was ${unknown.name} — ${unknown.ion}. Its flame colour is ${unknown.desc.toLowerCase()}. Solved: ${solved}.`, color: '#10b981' });
        newUnknown();
      } else {
        showInfoCard(stage, { title: 'Not this one', body: `That cation gives ${SALTS.find((s) => s.id === v).desc.toLowerCase()}. Clean the loop and test the unknown again — was your loop really clean?`, color: '#ef4444' });
      }
    },
  });
  const scoreOut = panel.readout({ label: 'Identified', value: '0' });
  panel.info('Heat energy excites the metal\'s electrons; falling back down they emit light of a fixed colour. A dirty loop shows the OLD salt\'s colour — sodium contamination is the classic trap!');

  function setMode(m) {
    mode = m;
    loopState = 'dirty';
    loopSalt = null;
    if (m === 'identify') {
      newUnknown();
    } else {
      badge.set('Practice: clean, dip a known salt, flame it');
      badge.el.style.setProperty('--ix-hud-color', '#059669');
    }
  }

  function newUnknown() {
    unknown = SALTS[Math.floor(Math.random() * SALTS.length)];
    loopState = 'dirty';
    loopSalt = null;
    guessSel.set('');
    saltSel.set('');
    scoreOut.set(String(solved));
    badge.set('New unknown sample on the bench. Clean the loop first!');
    badge.el.style.setProperty('--ix-hud-color', '#8b5cf6');
  }

  function startHold(e) { holding = true; e.preventDefault(); }
  function stopHold() { holding = false; }
  holdBtn.el.addEventListener('pointerdown', startHold);
  holdBtn.el.addEventListener('pointerup', stopHold);
  holdBtn.el.addEventListener('pointercancel', stopHold);
  holdBtn.el.addEventListener('pointerleave', stopHold);

  function flameColor() {
    if (inFlame < 0.25) return null;
    if (loopState === 'dirty') return { color: '#fbbf24', label: 'yellow (contamination!)' };
    if (!loopSalt) return null;
    return { color: loopSalt.color, label: isUnknown ? 'observe carefully…' : `${loopSalt.desc} — ${loopSalt.ion}` };
  }

  let loopX = 100;
  let loopY = 100;

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    inFlame += (holding ? 1 : -1.6) * dt;
    inFlame = Math.max(0, Math.min(1, inFlame));

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.85;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const bnx = w * 0.5;
    const fc = flameColor();
    drawBurner(ctx, bnx, benchY, t, true, fc ? fc.color : '#60a5fa', fc ? 56 : 44);
    if (fc) {
      const g = ctx.createRadialGradient(bnx, benchY - 60, 6, bnx, benchY - 60, 90);
      g.addColorStop(0, 'rgba(255,255,255,0.12)');
      g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g;
      ctx.fillRect(bnx - 90, benchY - 150, 180, 150);
      text(ctx, fc.label, bnx, benchY - 110, { color: fc.color, font: '700 12px Poppins, sans-serif' });
    }

    const loopTargetX = holding ? bnx : w * 0.22;
    const loopTargetY = holding ? benchY - 58 : benchY - 90;
    loopX += (loopTargetX - loopX) * Math.min(1, dt * 6);
    loopY += (loopTargetY - loopY) * Math.min(1, dt * 6);
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(loopX - 64, loopY - 30);
    ctx.lineTo(loopX - 8, loopY);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(loopX, loopY, 7, 0, Math.PI * 2);
    ctx.stroke();
    if (loopState === 'dirty') {
      ctx.fillStyle = 'rgba(120,113,108,0.8)';
      ctx.beginPath();
      ctx.arc(loopX, loopY, 4.5, 0, Math.PI * 2);
      ctx.fill();
    } else if (loopSalt) {
      ctx.fillStyle = 'rgba(241,245,249,0.9)';
      ctx.beginPath();
      ctx.arc(loopX, loopY, 4, 0, Math.PI * 2);
      ctx.fill();
    }
    text(ctx, loopState === 'dirty' ? 'platinum loop (dirty)' : loopSalt ? 'loop + sample' : 'platinum loop (clean)', w * 0.22, benchY - 116);

    drawBeaker(ctx, w * 0.07, benchY - 46, 42, 44, 0.5, 'rgba(186,230,253,0.35)', 'conc. HCl');
    const sx = w * 0.82;
    ctx.fillStyle = mode === 'identify' ? 'rgba(148,163,184,0.6)' : 'rgba(241,245,249,0.7)';
    ctx.fillRect(sx - 18, benchY - 16, 36, 14);
    text(ctx, mode === 'identify' ? 'unknown salt ?' : 'salt samples', sx, benchY - 24);

    loopOut.set(loopState === 'dirty' ? 'dirty (old residue)' : loopSalt ? 'carrying sample' : 'clean');
    if (holding && inFlame > 0.5 && loopState === 'dirty') {
      badge.set('Yellow flash — that is contamination, not your salt!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
    }
  });

  sim.start();

  return {
    dispose() {
      holdBtn.el.removeEventListener('pointerdown', startHold);
      holdBtn.el.removeEventListener('pointerup', stopHold);
      holdBtn.el.removeEventListener('pointercancel', stopHold);
      holdBtn.el.removeEventListener('pointerleave', stopHold);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
