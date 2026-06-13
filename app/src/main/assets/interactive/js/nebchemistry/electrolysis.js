import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawBeaker, text, roundRect } from './chem-utils.js';

const Z_CU = 0.000329;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Weigh the cathode, then switch on', '#047857');

  let current = 1.0;
  let runMinutes = 10;
  let running = false;
  let elapsed = 0;
  let deposited = 0;
  const startMass = 12.4 + Math.random() * 0.8;
  let weighed = false;
  const ions = [];
  let t = 0;

  for (let i = 0; i < 16; i++) {
    ions.push({
      x: Math.random(), y: Math.random(),
      kind: i % 2 === 0 ? 'cu' : 'so4',
      sp: 0.4 + Math.random() * 0.5,
    });
  }

  const panel = createPanel(stage, { title: 'Electrolysis of CuSO₄' });
  panel.button({ label: 'Weigh cathode (before)', icon: 'scale', onClick: () => {
    weighed = true;
    beforeOut.set(`${startMass.toFixed(3)} g`);
    badge.set(`Cathode mass: ${startMass.toFixed(3)} g — noted!`);
    badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
  } });
  panel.slider({ label: 'Current', min: 0.2, max: 3, step: 0.1, value: current, format: (v) => `${v.toFixed(1)} A`, onChange: (v) => { current = v; } });
  panel.slider({ label: 'Run time', min: 5, max: 30, step: 1, value: runMinutes, format: (v) => `${v} min`, onChange: (v) => { runMinutes = v; } });
  panel.buttonRow([
    { label: 'Start', icon: 'power', onClick: start },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset },
  ]);
  panel.divider();
  const beforeOut = panel.readout({ label: 'Cathode before', value: '—' });
  const clockOut = panel.readout({ label: 'Time elapsed', value: '0.0 min' });
  const afterOut = panel.readout({ label: 'Cathode after', value: '—' });
  panel.button({ label: 'Weigh cathode (after)', icon: 'scale', onClick: weighAfter });
  panel.info('Faraday\'s first law: m = Z·I·t. For copper Z = 0.000329 g/C (M/2F). Doubling current OR time doubles the copper deposited — verify it yourself!');

  function start() {
    if (!weighed) {
      badge.set('Weigh the cathode first — you need the initial mass!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    if (running) return;
    running = true;
    elapsed = 0;
    deposited = 0;
    afterOut.set('—');
    badge.set('Current flowing — Cu²⁺ migrating to the cathode');
    badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
  }

  function reset() {
    running = false;
    elapsed = 0;
    deposited = 0;
    weighed = false;
    beforeOut.set('—');
    afterOut.set('—');
    badge.set('Weigh the cathode, then switch on');
    badge.el.style.setProperty('--ix-hud-color', '#047857');
  }

  function weighAfter() {
    if (running) {
      badge.set('Switch off first — never weigh a live electrode!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    if (deposited <= 0) {
      badge.set('Nothing deposited yet');
      badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
      return;
    }
    const after = startMass + deposited;
    afterOut.set(`${after.toFixed(3)} g`);
    const seconds = elapsed * 60;
    const theory = Z_CU * current * seconds;
    showInfoCard(stage, {
      title: 'Verify Faraday\'s first law',
      body: `Gain = ${after.toFixed(3)} − ${startMass.toFixed(3)} = ${deposited.toFixed(3)} g.\nTheory: m = Z·I·t = 0.000329 × ${current.toFixed(1)} × ${Math.round(seconds)} = ${theory.toFixed(3)} g.\nCathode: Cu²⁺ + 2e⁻ → Cu. Anode: Cu → Cu²⁺ + 2e⁻ (anode loses the same mass, so the blue colour stays constant).`,
      color: '#10b981',
    });
    badge.set(`Deposit ${deposited.toFixed(3)} g — matches Z·I·t!`);
    badge.el.style.setProperty('--ix-hud-color', '#10b981');
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    if (running) {
      elapsed += dt * 1.6;
      deposited = Z_CU * current * elapsed * 60;
      if (elapsed >= runMinutes) {
        running = false;
        badge.set('Timer done — switch off, rinse, dry and reweigh');
        badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
      }
    }

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.86;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const cx = w * 0.42;
    const bw = Math.min(w * 0.5, 230);
    const bkX = cx - bw / 2;
    const bkY = h * 0.3;
    const bkH = benchY - bkY - 8;
    drawBeaker(ctx, bkX, bkY, bw, bkH, 0.8, 'rgba(59,130,246,0.4)', 'CuSO₄ solution (blue)');

    const elTop = bkY - 26;
    const elBot = bkY + bkH - 26;
    const anodeX = bkX + bw * 0.25;
    const cathX = bkX + bw * 0.75;
    ctx.fillStyle = '#b45309';
    ctx.fillRect(anodeX - 5, elTop, 10, elBot - elTop);
    const growth = Math.min(6, deposited * 40);
    ctx.fillRect(cathX - 5 - growth / 2, elTop, 10 + growth, elBot - elTop);
    ctx.fillStyle = '#d97706';
    ctx.fillRect(cathX - 5 - growth / 2, elBot - 30, 10 + growth, 30);
    text(ctx, 'anode (+)', anodeX, elTop - 24, { color: '#f87171' });
    text(ctx, 'Cu → Cu²⁺ + 2e⁻', anodeX, elTop - 12, { font: '600 8.5px Poppins, sans-serif' });
    text(ctx, 'cathode (−)', cathX, elTop - 24, { color: '#60a5fa' });
    text(ctx, 'Cu²⁺ + 2e⁻ → Cu', cathX, elTop - 12, { font: '600 8.5px Poppins, sans-serif' });

    ctx.strokeStyle = running ? '#fbbf24' : '#64748b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(anodeX, elTop);
    ctx.lineTo(anodeX, h * 0.08);
    ctx.lineTo(cx - 22, h * 0.08);
    ctx.moveTo(cathX, elTop);
    ctx.lineTo(cathX, h * 0.08);
    ctx.lineTo(cx + 22, h * 0.08);
    ctx.stroke();
    ctx.fillStyle = '#1e293b';
    roundRect(ctx, cx - 24, h * 0.05, 48, 24, 4);
    ctx.fill();
    ctx.strokeStyle = '#64748b';
    ctx.stroke();
    text(ctx, running ? `${current.toFixed(1)} A` : 'OFF', cx, h * 0.05 + 16, { color: running ? '#fbbf24' : '#64748b', font: '700 10px monospace' });

    const liqTop = bkY + bkH * 0.2;
    ions.forEach((ion) => {
      if (running) {
        const dir = ion.kind === 'cu' ? 1 : -1;
        ion.x += dir * ion.sp * dt * 0.12 * current;
        ion.y += Math.sin(t * ion.sp * 3 + ion.x * 9) * dt * 0.12;
        if (ion.kind === 'cu' && ion.x > 0.92) { ion.x = 0.1; ion.y = Math.random(); }
        if (ion.kind === 'so4' && ion.x < 0.08) { ion.x = 0.9; ion.y = Math.random(); }
      }
      ion.y = Math.max(0.05, Math.min(0.95, ion.y));
      const ix = bkX + 10 + ion.x * (bw - 20);
      const iy = liqTop + ion.y * (bkH - liqTop + bkY - 14);
      ctx.fillStyle = ion.kind === 'cu' ? '#60a5fa' : '#fcd34d';
      ctx.beginPath();
      ctx.arc(ix, iy, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#0f172a';
      ctx.font = '700 5.5px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(ion.kind === 'cu' ? 'Cu²⁺' : 'SO₄²⁻', ix, iy + 2);
    });

    text(ctx, `m = Z·I·t = 0.000329 × ${current.toFixed(1)} × ${Math.round(elapsed * 60)} s = ${deposited.toFixed(3)} g`, w / 2, h - 10, { color: '#9ec1ff' });
    clockOut.set(`${elapsed.toFixed(1)} min`);
  });

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
