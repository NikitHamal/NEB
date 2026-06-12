import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const ACID_MMOL = 2.5;
const ACID_VOL = 25;
const BASE_CONC = 0.1;
const MAX_VOL = 50;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const phBadge = hud.badge('pH 1.0', '#ef4444');

  let volume = 0;
  let dispensing = false;
  let dropRate = 1;
  let indicator = 'universal';
  const curve = [];
  let lastRecorded = -1;
  const drops = [];

  function computePH(vb) {
    const nb = BASE_CONC * vb;
    const vt = ACID_VOL + vb;
    const diff = ACID_MMOL - nb;
    if (Math.abs(diff) < 1e-6) return 7;
    if (diff > 0) return Math.max(0, -Math.log10(diff / vt));
    return Math.min(14, 14 + Math.log10(-diff / vt));
  }

  function solutionColor(ph) {
    if (indicator === 'litmus') {
      if (ph < 6.5) return 'rgba(239,68,68,0.78)';
      if (ph > 7.5) return 'rgba(59,130,246,0.78)';
      return 'rgba(139,92,246,0.78)';
    }
    if (indicator === 'phenolphthalein') {
      if (ph < 8.3) return 'rgba(203,213,225,0.22)';
      return 'rgba(236,72,153,0.8)';
    }
    if (ph < 3) return 'rgba(239,68,68,0.8)';
    if (ph < 5) return 'rgba(249,115,22,0.8)';
    if (ph < 6.5) return 'rgba(234,179,8,0.8)';
    if (ph < 7.5) return 'rgba(34,197,94,0.8)';
    if (ph < 9) return 'rgba(20,184,166,0.8)';
    if (ph < 11) return 'rgba(59,130,246,0.8)';
    return 'rgba(139,92,246,0.8)';
  }

  function badgeColor(ph) {
    if (ph < 5) return '#ef4444';
    if (ph < 6.5) return '#eab308';
    if (ph < 7.5) return '#22c55e';
    if (ph < 10) return '#3b82f6';
    return '#8b5cf6';
  }

  const panel = createPanel(stage, { title: 'Titration Controls' });
  const holdBtn = panel.button({
    label: 'Hold to add NaOH',
    icon: 'colorize',
    onClick: () => {},
  });
  panel.slider({
    label: 'Drop rate',
    min: 0.2, max: 3, step: 0.1, value: dropRate,
    format: (v) => `${v.toFixed(1)} mL/s`,
    onChange: (v) => { dropRate = v; },
  });
  panel.select({
    label: 'Indicator',
    options: [
      { value: 'universal', label: 'Universal indicator' },
      { value: 'litmus', label: 'Litmus' },
      { value: 'phenolphthalein', label: 'Phenolphthalein' },
    ],
    value: indicator,
    onChange: (v) => { indicator = v; },
  });
  panel.divider();
  const phOut = panel.readout({ label: 'pH', value: '1.00' });
  const volOut = panel.readout({ label: 'NaOH added', value: '0.0 mL' });
  const eqOut = panel.readout({ label: 'Equivalence at', value: '25.0 mL' });
  panel.button({
    label: 'Reset titration',
    icon: 'replay',
    variant: 'ghost',
    onClick: () => {
      volume = 0;
      curve.length = 0;
      drops.length = 0;
      lastRecorded = -1;
    },
  });
  panel.info('The flask holds 25 mL of 0.10 M HCl. The burette holds 0.10 M NaOH. Hold the button and watch the pH crawl — then leap — past 25 mL.');

  function startDispense(e) { dispensing = true; e.preventDefault(); }
  function stopDispense() { dispensing = false; }
  holdBtn.el.addEventListener('pointerdown', startDispense);
  holdBtn.el.addEventListener('pointerup', stopDispense);
  holdBtn.el.addEventListener('pointercancel', stopDispense);
  holdBtn.el.addEventListener('pointerleave', stopDispense);

  function layout(w, h) {
    const bw = Math.min(w * 0.34, 220);
    const bh = h * 0.34;
    const bx = w * 0.06;
    const by = h - 40 - bh;
    return {
      beaker: { x: bx, y: by, w: bw, h: bh },
      buretteX: bx + bw / 2,
      buretteTop: 14,
      buretteBot: by - h * 0.06,
      graph: { x: w * 0.5, y: 34, w: w * 0.46 - 20, h: h - 90 },
    };
  }

  let dropTimer = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    const ly = layout(w, h);
    if (dispensing && volume < MAX_VOL) {
      volume = Math.min(MAX_VOL, volume + dropRate * dt);
      dropTimer += dt;
      if (dropTimer > 0.12) {
        dropTimer = 0;
        drops.push({ x: ly.buretteX, y: ly.buretteBot + 8, v: 40 });
      }
    }
    if (volume - lastRecorded >= 0.15) {
      const phNow = computePH(volume);
      const prev = curve.length ? curve[curve.length - 1] : null;
      if (prev && Math.abs(phNow - prev.ph) > 0.6) {
        const eqVol = ACID_MMOL / BASE_CONC;
        const steps = Math.min(32, Math.ceil(Math.abs(phNow - prev.ph) / 0.3));
        const vs = [];
        for (let i = 1; i < steps; i++) vs.push(prev.v + ((volume - prev.v) * i) / steps);
        if (prev.v < eqVol && volume > eqVol) {
          vs.push(eqVol);
          vs.sort((a, b) => a - b);
        }
        vs.forEach((v) => curve.push({ v, ph: computePH(v) }));
      }
      lastRecorded = volume;
      curve.push({ v: volume, ph: phNow });
    }
    const ph = computePH(volume);

    ctx.clearRect(0, 0, w, h);
    const bk = ly.beaker;

    const liqFrac = (ACID_VOL + volume) / (ACID_VOL + MAX_VOL);
    const liqH = bk.h * (0.35 + 0.55 * liqFrac);
    const liqY = bk.y + bk.h - liqH;
    ctx.fillStyle = solutionColor(ph);
    ctx.fillRect(bk.x + 3, liqY, bk.w - 6, liqH - 3);
    ctx.strokeStyle = 'rgba(255,255,255,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(bk.x + 3, liqY);
    ctx.lineTo(bk.x + bk.w - 3, liqY);
    ctx.stroke();

    ctx.strokeStyle = 'rgba(199,212,234,0.85)';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(bk.x, bk.y - 6);
    ctx.lineTo(bk.x, bk.y + bk.h);
    ctx.lineTo(bk.x + bk.w, bk.y + bk.h);
    ctx.lineTo(bk.x + bk.w, bk.y - 6);
    ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.7)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('25 mL HCl + indicator', bk.x + bk.w / 2, bk.y + bk.h + 16);

    const tubeW = 14;
    const bx = ly.buretteX;
    ctx.fillStyle = 'rgba(125,211,252,0.25)';
    const baseFill = (MAX_VOL - volume) / MAX_VOL;
    const tubeH = ly.buretteBot - ly.buretteTop;
    ctx.fillRect(bx - tubeW / 2 + 2, ly.buretteTop + tubeH * (1 - baseFill), tubeW - 4, tubeH * baseFill);
    ctx.strokeStyle = 'rgba(199,212,234,0.85)';
    ctx.lineWidth = 2;
    ctx.strokeRect(bx - tubeW / 2, ly.buretteTop, tubeW, tubeH);
    ctx.beginPath();
    ctx.moveTo(bx - tubeW / 2, ly.buretteBot);
    ctx.lineTo(bx, ly.buretteBot + 12);
    ctx.lineTo(bx + tubeW / 2, ly.buretteBot);
    ctx.stroke();
    ctx.strokeStyle = 'rgba(199,212,234,0.4)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
      const gy = ly.buretteTop + (i / 10) * tubeH;
      ctx.beginPath();
      ctx.moveTo(bx + tubeW / 2, gy);
      ctx.lineTo(bx + tubeW / 2 + 5, gy);
      ctx.stroke();
    }
    ctx.fillStyle = 'rgba(199,212,234,0.7)';
    ctx.textAlign = 'left';
    ctx.fillText('NaOH 0.10 M', bx + tubeW / 2 + 9, ly.buretteTop + 12);

    ctx.fillStyle = 'rgba(125,211,252,0.9)';
    for (let i = drops.length - 1; i >= 0; i--) {
      const d = drops[i];
      d.v += 320 * dt;
      d.y += d.v * dt;
      if (d.y >= liqY) {
        drops.splice(i, 1);
        continue;
      }
      ctx.beginPath();
      ctx.arc(d.x, d.y, 3, 0, Math.PI * 2);
      ctx.fill();
    }

    const g = ly.graph;
    ctx.strokeStyle = 'rgba(158,193,255,0.35)';
    ctx.lineWidth = 1;
    ctx.strokeRect(g.x, g.y, g.w, g.h);
    ctx.fillStyle = 'rgba(199,212,234,0.6)';
    ctx.textAlign = 'center';
    ctx.fillText('pH curve', g.x + g.w / 2, g.y - 8);
    ctx.fillText('volume NaOH added (mL)', g.x + g.w / 2, g.y + g.h + 16);
    for (let p = 0; p <= 14; p += 2) {
      const yy = g.y + g.h - (p / 14) * g.h;
      ctx.fillText(String(p), g.x - 12, yy + 3);
      ctx.strokeStyle = 'rgba(158,193,255,0.12)';
      ctx.beginPath();
      ctx.moveTo(g.x, yy);
      ctx.lineTo(g.x + g.w, yy);
      ctx.stroke();
    }
    for (let v = 0; v <= MAX_VOL; v += 10) {
      const xx = g.x + (v / MAX_VOL) * g.w;
      ctx.fillText(String(v), xx, g.y + g.h + 4 + 8);
    }
    const eqX = g.x + (25 / MAX_VOL) * g.w;
    ctx.strokeStyle = 'rgba(251,191,36,0.5)';
    ctx.setLineDash([4, 5]);
    ctx.beginPath();
    ctx.moveTo(eqX, g.y);
    ctx.lineTo(eqX, g.y + g.h);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = 'rgba(251,191,36,0.9)';
    ctx.fillText('equivalence', eqX, g.y + 12);

    if (curve.length > 1) {
      ctx.strokeStyle = '#10B981';
      ctx.lineWidth = 2;
      ctx.beginPath();
      curve.forEach((pt, i) => {
        const xx = g.x + (pt.v / MAX_VOL) * g.w;
        const yy = g.y + g.h - (pt.ph / 14) * g.h;
        if (i === 0) ctx.moveTo(xx, yy);
        else ctx.lineTo(xx, yy);
      });
      ctx.stroke();
    }
    const cx = g.x + (volume / MAX_VOL) * g.w;
    const cy = g.y + g.h - (ph / 14) * g.h;
    ctx.fillStyle = '#fbbf24';
    ctx.beginPath();
    ctx.arc(cx, cy, 4.5, 0, Math.PI * 2);
    ctx.fill();

    phOut.set(ph.toFixed(2));
    volOut.set(`${volume.toFixed(1)} mL`);
    eqOut.set('25.0 mL');
    phBadge.set(`pH ${ph.toFixed(2)}${volume >= MAX_VOL ? ' · burette empty' : dispensing ? ' · adding…' : ''}`);
    phBadge.el.style.setProperty('--ix-hud-color', badgeColor(ph));
  });

  sim.start();

  return {
    dispose() {
      holdBtn.el.removeEventListener('pointerdown', startDispense);
      holdBtn.el.removeEventListener('pointerup', stopDispense);
      holdBtn.el.removeEventListener('pointercancel', stopDispense);
      holdBtn.el.removeEventListener('pointerleave', stopDispense);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
