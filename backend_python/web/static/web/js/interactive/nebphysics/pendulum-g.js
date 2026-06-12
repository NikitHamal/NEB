import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, linFit, drawTable, drawGraph, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Pendulum swinging', '#D97706');
  const countBadge = hud.badge('Oscillations: 0', '#9ec1ff');

  const gTrue = 9.806;
  let L = 0.8;
  let simTime = 0;
  let watchRunning = false;
  let watchStart = 0;
  let watchValue = 0;
  let oscCount = 0;
  let lastPhase = 0;
  const trials = [];

  function period() { return 2 * Math.PI * Math.sqrt(L / gTrue); }

  const panel = createPanel(stage, { title: 'Pendulum g Lab' });
  panel.slider({
    label: 'Thread length L',
    min: 40, max: 120, step: 5, value: 80,
    format: (v) => `${v} cm`,
    onChange: (v) => { L = v / 100; },
  });
  panel.section('Stopwatch');
  panel.buttonRow([
    {
      label: 'Start',
      icon: 'play_arrow',
      onClick: () => {
        if (watchRunning) return;
        watchRunning = true;
        watchStart = simTime;
        watchValue = 0;
        oscCount = 0;
        lastPhase = phaseNow();
      },
    },
    { label: 'Stop', icon: 'stop', onClick: () => { watchRunning = false; } },
    { label: 'Reset', icon: 'replay', onClick: () => { watchRunning = false; watchValue = 0; oscCount = 0; } },
  ]);
  panel.button({
    label: 'Record trial',
    icon: 'edit_note',
    onClick: () => {
      if (watchRunning || watchValue < 1 || oscCount < 5 || trials.length >= 6) return;
      const T = watchValue / oscCount;
      trials.push({ L, t: watchValue, n: oscCount, T });
      watchValue = 0;
      oscCount = 0;
    },
  });
  panel.button({ label: 'Clear trials', icon: 'delete', variant: 'ghost', onClick: () => { trials.length = 0; } });
  panel.divider();
  const watchOut = panel.readout({ label: 'Stopwatch', value: '0.00 s' });
  const tOut = panel.readout({ label: 'T = t/n', value: '—' });
  const gOut = panel.readout({ label: 'g from graph slope', value: '—' });
  panel.info('Set L, start the stopwatch as the bob crosses the mean position, count 20 oscillations, stop, then Record trial. Repeat for 4-5 lengths and read g from the L vs T² slope.');

  function phaseNow() {
    return (simTime / period()) % 1;
  }

  sim.setUpdate((ctx, dt, w, h) => {
    simTime += dt;
    if (watchRunning) {
      watchValue = simTime - watchStart;
      const ph = phaseNow();
      if (ph < lastPhase) oscCount++;
      lastPhase = ph;
    }
    ctx.clearRect(0, 0, w, h);

    const px = w * 0.3;
    const py = 34;
    const maxLen = h * 0.42;
    const r = (L / 1.2) * maxLen;
    const theta = 0.14 * Math.cos((2 * Math.PI * simTime) / period());
    const bx = px + Math.sin(theta) * r;
    const by = py + Math.cos(theta) * r;

    ctx.fillStyle = 'rgba(199,212,234,0.85)';
    ctx.fillRect(px - 40, py - 10, 80, 7);
    ctx.strokeStyle = 'rgba(158,193,255,0.18)';
    ctx.setLineDash([4, 5]);
    ctx.beginPath();
    ctx.moveTo(px, py);
    ctx.lineTo(px, py + r + 24);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(px, py);
    ctx.lineTo(bx, by);
    ctx.stroke();
    const grad = ctx.createRadialGradient(bx - 4, by - 5, 2, bx, by, 13);
    grad.addColorStop(0, '#ffd584');
    grad.addColorStop(1, '#D97706');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(bx, by, 12, 0, Math.PI * 2);
    ctx.fill();
    labelText(ctx, `L = ${(L * 100).toFixed(0)} cm`, px, py + r + 40, { size: 11, align: 'center' });

    const swX = w * 0.72;
    const swY = 60;
    ctx.fillStyle = 'rgba(8,16,30,0.78)';
    ctx.strokeStyle = watchRunning ? '#8be9a8' : 'rgba(158,193,255,0.3)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(swX, swY, 36, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    labelText(ctx, watchValue.toFixed(1), swX, swY + 1, { size: 15, align: 'center', color: watchRunning ? '#8be9a8' : '#e8eefb' });
    labelText(ctx, 'seconds', swX, swY + 16, { size: 8.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.7)' });

    const rows = trials.map((tr) => [
      (tr.L * 100).toFixed(0), fmt(tr.t, 2), tr.n, fmt(tr.T, 3), fmt(tr.T * tr.T, 3),
    ]);
    const tableW = Math.min(w * 0.55, 250);
    const tableH = drawTable(ctx, {
      x: 12, y: h * 0.6, w: tableW,
      title: 'Observations', cols: ['L cm', 't s', 'n', 'T s', 'T² s²'], rows,
    });
    const pts = trials.map((tr) => ({ x: tr.L, y: tr.T * tr.T }));
    const fit = linFit(pts);
    drawGraph(ctx, {
      x: tableW + 22, y: h * 0.6, w: w - tableW - 34, h: Math.max(tableH, h * 0.3),
      pts, fit: pts.length >= 2 ? fit : null,
      xLabel: 'L (m)', yLabel: 'T² (s²)', xMax: 1.3, yMax: 5.5,
    });

    countBadge.set(`Oscillations: ${oscCount}`);
    statusBadge.set(watchRunning ? 'Timing… count the swings' : trials.length >= 2 ? 'Plotting L vs T²' : 'Pendulum swinging');
    watchOut.set(`${fmt(watchValue, 2)} s`);
    tOut.set(!watchRunning && watchValue > 0 && oscCount > 0 ? `${fmt(watchValue / oscCount, 3)} s (n=${oscCount})` : '—');
    if (fit && pts.length >= 2 && fit.m > 0) {
      const g = (4 * Math.PI * Math.PI) / fit.m;
      gOut.set(`${fmt(g, 2)} m/s²`);
    } else {
      gOut.set('record ≥ 2 trials');
    }
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
