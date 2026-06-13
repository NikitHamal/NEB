import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const STRING_LEN = 8;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const modeBadge = hud.badge('Travelling wave', '#F59E0B');

  let mode = 'travelling';
  let freq = 0.6;
  let amp = 0.8;
  let waveSpeed = 2.4;
  let freq2 = 0.8;
  let amp2 = 0.8;
  let showComponents = true;
  let t = 0;

  const panel = createPanel(stage, { title: 'Wave Controls' });
  panel.select({
    label: 'Mode',
    options: [
      { value: 'travelling', label: 'Travelling wave' },
      { value: 'standing', label: 'Standing wave' },
      { value: 'interference', label: 'Interference (two waves)' },
    ],
    value: mode,
    onChange: (v) => {
      mode = v;
      modeBadge.set(v === 'travelling' ? 'Travelling wave' : v === 'standing' ? 'Standing wave' : 'Superposition');
      wave2Rows.forEach((r) => { r.el.style.display = v === 'interference' ? '' : 'none'; });
      if (mode === 'standing') snapToHarmonic();
    },
  });
  const freqSlider = panel.slider({
    label: 'Frequency f',
    min: 0.2, max: 1.6, step: 0.05, value: freq,
    format: (v) => `${v.toFixed(2)} Hz`,
    onChange: (v) => {
      freq = v;
      if (mode === 'standing') snapToHarmonic();
    },
  });
  panel.slider({
    label: 'Amplitude A',
    min: 0.1, max: 1.2, step: 0.05, value: amp,
    format: (v) => `${v.toFixed(2)} m`,
    onChange: (v) => { amp = v; },
  });
  panel.slider({
    label: 'Wave speed v',
    min: 0.8, max: 5, step: 0.1, value: waveSpeed,
    format: (v) => `${v.toFixed(1)} m/s`,
    onChange: (v) => {
      waveSpeed = v;
      if (mode === 'standing') snapToHarmonic();
    },
  });
  const f2Row = panel.slider({
    label: 'Wave 2 frequency',
    min: 0.2, max: 1.6, step: 0.05, value: freq2,
    format: (v) => `${v.toFixed(2)} Hz`,
    onChange: (v) => { freq2 = v; },
  });
  const a2Row = panel.slider({
    label: 'Wave 2 amplitude',
    min: 0.1, max: 1.2, step: 0.05, value: amp2,
    format: (v) => `${v.toFixed(2)} m`,
    onChange: (v) => { amp2 = v; },
  });
  const compRow = panel.toggle({
    label: 'Show components',
    value: true,
    onChange: (v) => { showComponents = v; },
  });
  const wave2Rows = [f2Row, a2Row, compRow];
  wave2Rows.forEach((r) => { r.el.style.display = 'none'; });
  panel.divider();
  const lambdaOut = panel.readout({ label: 'Wavelength λ = v/f', value: '—' });
  const periodOut = panel.readout({ label: 'Period T = 1/f', value: '—' });
  panel.info('Raise the frequency and watch the wavelength shrink — the speed stays fixed by the string. In standing mode, find the still nodes.');

  function snapToHarmonic() {
    const fundamental = waveSpeed / (2 * STRING_LEN);
    const n = Math.max(1, Math.min(Math.round(freq / fundamental), Math.floor(1.6 / fundamental)));
    freq = n * fundamental;
    freqSlider.set(freq);
  }

  function y1(x, time) {
    const k = (2 * Math.PI * freq) / waveSpeed;
    const w = 2 * Math.PI * freq;
    return amp * Math.sin(k * x - w * time);
  }

  function y2(x, time) {
    const k = (2 * Math.PI * freq2) / waveSpeed;
    const w = 2 * Math.PI * freq2;
    return amp2 * Math.sin(k * x - w * time);
  }

  function yStanding(x, time) {
    const k = (2 * Math.PI * freq) / waveSpeed;
    const w = 2 * Math.PI * freq;
    return 2 * amp * Math.sin(k * x) * Math.cos(w * time);
  }

  function plot(ctx, fn, w, midY, scaleY, color, width, dash) {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    if (dash) ctx.setLineDash(dash);
    ctx.beginPath();
    const n = 160;
    for (let i = 0; i <= n; i++) {
      const x = (i / n) * STRING_LEN;
      const sx = 30 + (x / STRING_LEN) * (w - 60);
      const sy = midY - fn(x, t) * scaleY;
      if (i === 0) ctx.moveTo(sx, sy);
      else ctx.lineTo(sx, sy);
    }
    ctx.stroke();
    if (dash) ctx.setLineDash([]);
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    ctx.clearRect(0, 0, w, h);
    const midY = h * 0.46;
    const scaleY = Math.min(h * 0.16, 90);

    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(20, midY);
    ctx.lineTo(w - 20, midY);
    ctx.stroke();

    ctx.fillStyle = 'rgba(199,212,234,0.5)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let m = 0; m <= STRING_LEN; m += 1) {
      const sx = 30 + (m / STRING_LEN) * (w - 60);
      ctx.beginPath();
      ctx.moveTo(sx, midY - 4);
      ctx.lineTo(sx, midY + 4);
      ctx.stroke();
      ctx.fillText(`${m}`, sx, midY + 18);
    }
    ctx.fillText('metres along the string', w / 2, midY + 34);

    ctx.fillStyle = 'rgba(199,212,234,0.8)';
    ctx.fillRect(26, midY - scaleY * 2.6, 4, scaleY * 5.2);
    ctx.fillRect(w - 30, midY - scaleY * 2.6, 4, scaleY * 5.2);

    if (mode === 'travelling') {
      plot(ctx, y1, w, midY, scaleY, '#F59E0B', 2.5);
      const lambda = waveSpeed / freq;
      if (lambda <= STRING_LEN) {
        const x0 = ((waveSpeed * t) % lambda + lambda) % lambda;
        const crest = x0 + lambda * 0.25 > lambda ? x0 + lambda * 0.25 - lambda : x0 + lambda * 0.25;
        const sx1 = 30 + (crest / STRING_LEN) * (w - 60);
        const sx2 = 30 + (Math.min(crest + lambda, STRING_LEN) / STRING_LEN) * (w - 60);
        if (crest + lambda <= STRING_LEN) {
          const ay = midY - scaleY * amp - 16;
          ctx.strokeStyle = 'rgba(139,233,168,0.9)';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(sx1, ay);
          ctx.lineTo(sx2, ay);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(sx1 + 6, ay - 4); ctx.lineTo(sx1, ay); ctx.lineTo(sx1 + 6, ay + 4);
          ctx.moveTo(sx2 - 6, ay - 4); ctx.lineTo(sx2, ay); ctx.lineTo(sx2 - 6, ay + 4);
          ctx.stroke();
          ctx.fillStyle = '#8be9a8';
          ctx.font = '700 11px Poppins, sans-serif';
          ctx.fillText(`λ = ${lambda.toFixed(2)} m`, (sx1 + sx2) / 2, ay - 8);
        }
      }
    } else if (mode === 'standing') {
      const k = (2 * Math.PI * freq) / waveSpeed;
      ctx.strokeStyle = 'rgba(245,158,11,0.22)';
      plot(ctx, (x) => 2 * amp * Math.sin(k * x), w, midY, scaleY, 'rgba(245,158,11,0.22)', 1, [4, 5]);
      plot(ctx, (x) => -2 * amp * Math.sin(k * x), w, midY, scaleY, 'rgba(245,158,11,0.22)', 1, [4, 5]);
      plot(ctx, yStanding, w, midY, scaleY, '#F59E0B', 2.5);
      const lambda = waveSpeed / freq;
      const halfL = lambda / 2;
      ctx.fillStyle = '#7dd3fc';
      for (let x = 0; x <= STRING_LEN + 0.001; x += halfL) {
        const sx = 30 + (x / STRING_LEN) * (w - 60);
        ctx.beginPath();
        ctx.arc(sx, midY, 4, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.font = '700 11px Poppins, sans-serif';
      ctx.fillText('nodes (never move)', w / 2, midY - scaleY * 2.2 - 10);
    } else {
      if (showComponents) {
        plot(ctx, y1, w, midY, scaleY, 'rgba(125,211,252,0.5)', 1.2);
        plot(ctx, y2, w, midY, scaleY, 'rgba(244,114,182,0.5)', 1.2);
      }
      plot(ctx, (x, time) => y1(x, time) + y2(x, time), w, midY, scaleY, '#F59E0B', 2.5);
      ctx.font = '700 11px Poppins, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillStyle = 'rgba(125,211,252,0.9)';
      ctx.fillText('wave 1', 30, 26);
      ctx.fillStyle = 'rgba(244,114,182,0.9)';
      ctx.fillText('wave 2', 30, 42);
      ctx.fillStyle = '#F59E0B';
      ctx.fillText('sum (what the string does)', 30, 58);
    }

    lambdaOut.set(`${(waveSpeed / freq).toFixed(2)} m`);
    periodOut.set(`${(1 / freq).toFixed(2)} s`);
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
