import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, panelBg, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Strike the fork to begin', '#9ec1ff');

  let freq = 512;
  let temp = 25;
  let waterLevel = 30;
  let ringing = 0;
  let l1 = null;
  let l2 = null;
  let dragging = false;
  const endCorr = 1.05;

  function vSound() { return 331.4 + 0.6 * temp; }

  function resonanceLengths() {
    const v = vSound() * 100;
    const out = [];
    for (let n = 1; n <= 3; n++) {
      const l = ((2 * n - 1) * v) / (4 * freq) - endCorr;
      if (l > 2 && l < 95) out.push(l);
    }
    return out;
  }

  function airLen() { return 100 - waterLevel; }

  function loudness() {
    let best = 0;
    for (const lr of resonanceLengths()) {
      const d = (airLen() - lr) / 1.6;
      best = Math.max(best, 1 / (1 + d * d));
    }
    return best * ringing;
  }

  const panel = createPanel(stage, { title: 'Resonance Tube' });
  panel.select({
    label: 'Tuning fork',
    options: [320, 384, 426, 480, 512].map((f) => ({ value: String(f), label: `${f} Hz` })),
    value: '512',
    onChange: (v) => { freq = parseInt(v, 10); l1 = null; l2 = null; },
  });
  panel.slider({
    label: 'Room temperature',
    min: 10, max: 35, step: 1, value: temp,
    format: (v) => `${v} °C`,
    onChange: (v) => { temp = v; },
  });
  panel.button({ label: 'Strike fork', icon: 'graphic_eq', onClick: () => { ringing = 1; } });
  panel.buttonRow([
    { label: 'Mark l₁', icon: 'push_pin', onClick: () => { if (loudness() > 0.5) l1 = airLen(); } },
    { label: 'Mark l₂', icon: 'push_pin', onClick: () => { if (loudness() > 0.5) l2 = airLen(); } },
  ]);
  panel.button({ label: 'Clear marks', icon: 'delete', variant: 'ghost', onClick: () => { l1 = null; l2 = null; } });
  panel.divider();
  const airOut = panel.readout({ label: 'Air column l', value: '—' });
  const l1Out = panel.readout({ label: 'First resonance l₁', value: '—' });
  const l2Out = panel.readout({ label: 'Second resonance l₂', value: '—' });
  const vOut = panel.readout({ label: 'v = 2f(l₂−l₁)', value: '—' });
  const vTrueOut = panel.readout({ label: 'Accepted v (at T)', value: '—' });
  panel.info('Drag the water level (or reservoir). Strike the fork, lower the water slowly and listen for the loudest point — mark l₁ there, keep lowering for l₂.');

  function geom(w, h) {
    return { tx: w * 0.3, top: 26, bottom: h - 36, tw: Math.max(34, w * 0.09) };
  }

  function onDown(e) {
    dragging = true;
    if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
    onMove(e);
    e.preventDefault();
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    const frac = (p.y - g.top) / (g.bottom - g.top);
    waterLevel = Math.max(2, Math.min(95, 100 - frac * 100));
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  sim.setUpdate((ctx, dt, w, h) => {
    ringing = Math.max(0, ringing - dt * 0.12);
    const g = geom(w, h);
    const loud = loudness();
    ctx.clearRect(0, 0, w, h);

    const yOf = (cmFromTop) => g.top + ((g.bottom - g.top) * cmFromTop) / 100;
    ctx.strokeStyle = 'rgba(158,193,255,0.7)';
    ctx.lineWidth = 2;
    ctx.strokeRect(g.tx - g.tw / 2, g.top, g.tw, g.bottom - g.top);
    const wy = yOf(airLen());
    ctx.fillStyle = 'rgba(77,127,255,0.4)';
    ctx.fillRect(g.tx - g.tw / 2 + 2, wy, g.tw - 4, g.bottom - wy - 2);

    ctx.font = '600 8.5px Poppins, sans-serif';
    ctx.textAlign = 'right';
    for (let cm = 0; cm <= 100; cm += 10) {
      const yy = yOf(cm);
      ctx.strokeStyle = 'rgba(232,238,251,0.6)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(g.tx - g.tw / 2 - 8, yy);
      ctx.lineTo(g.tx - g.tw / 2, yy);
      ctx.stroke();
      ctx.fillStyle = 'rgba(232,238,251,0.8)';
      ctx.fillText(String(cm), g.tx - g.tw / 2 - 12, yy + 3);
    }

    if (loud > 0.08) {
      ctx.strokeStyle = `rgba(255,213,132,${0.3 + 0.6 * loud})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      const lenPx = wy - g.top;
      for (let i = 0; i <= 40; i++) {
        const yy = g.top + (lenPx * i) / 40;
        const phase = ((yy - g.top) / lenPx) * Math.PI * (airLen() > (resonanceLengths()[1] || 999) - 8 ? 1.5 : 0.5);
        const amp = Math.cos(phase) * (g.tw / 2 - 6) * loud;
        if (i === 0) ctx.moveTo(g.tx + amp, yy);
        else ctx.lineTo(g.tx + amp, yy);
      }
      ctx.stroke();
    }

    const forkX = g.tx;
    const forkY = g.top - 14;
    const vib = ringing > 0 ? Math.sin(performance.now() / 30) * 2.5 * ringing : 0;
    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(forkX - 8 + vib, forkY - 14);
    ctx.lineTo(forkX - 8, forkY);
    ctx.moveTo(forkX + 8 - vib, forkY - 14);
    ctx.lineTo(forkX + 8, forkY);
    ctx.stroke();
    labelText(ctx, `${freq} Hz`, forkX + 18, forkY - 4, { size: 10 });

    const handleY = wy;
    ctx.fillStyle = dragging ? '#ffd584' : '#9ec1ff';
    ctx.beginPath();
    ctx.arc(g.tx + g.tw / 2 + 26, handleY, 13, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(232,238,251,0.6)';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(g.tx + g.tw / 2, handleY);
    ctx.lineTo(g.tx + g.tw / 2 + 14, handleY);
    ctx.stroke();
    labelText(ctx, 'reservoir', g.tx + g.tw / 2 + 26, handleY + 28, { size: 8.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.7)' });

    const mx = w * 0.74;
    const mTop = h * 0.12;
    const mH = h * 0.5;
    panelBg(ctx, mx - 26, mTop - 24, 64, mH + 56);
    labelText(ctx, 'loudness', mx + 6, mTop - 8, { size: 9, weight: 600, align: 'center', color: 'rgba(199,212,234,0.8)' });
    ctx.fillStyle = 'rgba(255,255,255,0.1)';
    ctx.fillRect(mx - 8, mTop, 28, mH);
    const lh = mH * Math.min(1, loud);
    const grad = ctx.createLinearGradient(0, mTop + mH - lh, 0, mTop + mH);
    grad.addColorStop(0, '#ff8c8c');
    grad.addColorStop(1, '#8be9a8');
    ctx.fillStyle = grad;
    ctx.fillRect(mx - 8, mTop + mH - lh, 28, lh);
    if (ringing <= 0.02) labelText(ctx, 'fork silent', mx + 6, mTop + mH + 24, { size: 8.5, weight: 600, align: 'center', color: '#ff8c8c' });

    airOut.set(`${fmt(airLen(), 1)} cm`);
    l1Out.set(l1 === null ? '—' : `${fmt(l1, 1)} cm`);
    l2Out.set(l2 === null ? '—' : `${fmt(l2, 1)} cm`);
    if (l1 !== null && l2 !== null && l2 > l1) {
      vOut.set(`${fmt((2 * freq * (l2 - l1)) / 100, 1)} m/s`);
    } else {
      vOut.set('—');
    }
    vTrueOut.set(`${fmt(vSound(), 1)} m/s`);
    statusBadge.set(
      ringing <= 0.02 ? 'Strike the fork to begin'
        : loud > 0.75 ? 'LOUD — resonance! Mark this length'
          : loud > 0.3 ? 'Getting louder…' : 'Faint hum — keep adjusting',
    );
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      sim.canvas.removeEventListener('pointermove', onMove);
      sim.canvas.removeEventListener('pointerup', onUp);
      sim.canvas.removeEventListener('pointercancel', onUp);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
