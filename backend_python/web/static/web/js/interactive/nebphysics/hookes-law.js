import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, linFit, drawTable, drawGraph, labelText } from './lab-utils.js';

const K1 = 25;
const K2 = 40;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('No load', '#9ec1ff');

  const g = 9.8;
  let combo = 'single';
  let massG = 0;
  let dispNow = 0;
  let vel = 0;
  const readings = [];

  function keff() {
    if (combo === 'series') return (K1 * K2) / (K1 + K2);
    if (combo === 'parallel') return K1 + K2;
    return K1;
  }

  function targetX() {
    return ((massG / 1000) * g) / keff();
  }

  const panel = createPanel(stage, { title: 'Hooke\u2019s Law Lab' });
  panel.select({
    label: 'Spring arrangement',
    options: [
      { value: 'single', label: 'Single spring (k₁)' },
      { value: 'series', label: 'Two springs in series' },
      { value: 'parallel', label: 'Two springs in parallel' },
    ],
    value: combo,
    onChange: (v) => { combo = v; readings.length = 0; },
  });
  panel.buttonRow([
    { label: 'Add 50 g', icon: 'add', onClick: () => { massG = Math.min(500, massG + 50); } },
    { label: 'Remove 50 g', icon: 'remove', onClick: () => { massG = Math.max(0, massG - 50); } },
  ]);
  panel.button({
    label: 'Record reading',
    icon: 'edit_note',
    onClick: () => {
      if (massG === 0 || readings.length >= 8) return;
      if (Math.abs(dispNow - targetX()) > 0.0015) return;
      if (readings.some((r) => r.m === massG)) return;
      readings.push({ m: massG, F: (massG / 1000) * g, x: dispNow });
      readings.sort((a, b) => a.m - b.m);
    },
  });
  panel.button({ label: 'Clear table', icon: 'delete', variant: 'ghost', onClick: () => { readings.length = 0; } });
  panel.divider();
  const loadOut = panel.readout({ label: 'Load F = mg', value: '0.00 N' });
  const extOut = panel.readout({ label: 'Pointer extension', value: '0.0 cm' });
  const kOut = panel.readout({ label: 'k from graph slope', value: '—' });
  const kTheory = panel.readout({ label: 'Expected k', value: '—' });
  panel.info('Add slotted 50 g masses, wait for the pointer to settle, then Record. Plot F vs x — the slope is the spring constant k. Try series and parallel combos!');

  sim.setUpdate((ctx, dt, w, h) => {
    const xT = targetX();
    const k = 60;
    const acc = (xT - dispNow) * k - vel * 7;
    vel += acc * dt;
    dispNow += vel * dt;
    const settled = Math.abs(dispNow - xT) < 0.0015 && Math.abs(vel) < 0.004;

    ctx.clearRect(0, 0, w, h);
    const topY = 30;
    const sx = w * 0.26;
    const pxPerM = h * 0.32 / 0.25;
    const natural = h * 0.13;

    ctx.fillStyle = 'rgba(199,212,234,0.85)';
    ctx.fillRect(sx - 60, topY - 8, 120, 7);

    const yEnd = topY + natural + dispNow * pxPerM;
    drawSpring(ctx, sx, topY, yEnd, combo);
    const hangY = yEnd;
    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(sx, hangY);
    ctx.lineTo(sx, hangY + 14);
    ctx.stroke();
    const n = massG / 50;
    for (let i = 0; i < n; i++) {
      ctx.fillStyle = i % 2 ? '#4d5f85' : '#5b6f99';
      ctx.fillRect(sx - 16, hangY + 14 + i * 8, 32, 7);
    }
    labelText(ctx, `${massG} g`, sx, hangY + 30 + n * 8, { size: 10, align: 'center' });

    ctx.strokeStyle = '#ffd584';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(sx + 22, hangY);
    ctx.lineTo(sx + 52, hangY);
    ctx.stroke();
    const scaleX = sx + 56;
    ctx.strokeStyle = 'rgba(232,238,251,0.8)';
    ctx.lineWidth = 1;
    ctx.font = '600 8.5px Poppins, sans-serif';
    ctx.textAlign = 'left';
    const zeroY = topY + natural;
    for (let cm = 0; cm <= 24; cm += 1) {
      const yy = zeroY + (cm / 100) * pxPerM;
      if (yy > h * 0.62) break;
      ctx.beginPath();
      ctx.moveTo(scaleX, yy);
      ctx.lineTo(scaleX + (cm % 5 === 0 ? 14 : 8), yy);
      ctx.stroke();
      if (cm % 5 === 0) {
        ctx.fillStyle = 'rgba(232,238,251,0.85)';
        ctx.fillText(`${cm}`, scaleX + 18, yy + 3);
      }
    }
    labelText(ctx, 'cm scale', scaleX, zeroY - 10, { size: 8.5, weight: 600, color: 'rgba(199,212,234,0.7)' });

    const rows = readings.map((r) => [r.m, fmt(r.F, 2), fmt(r.x * 100, 1)]);
    const tw = Math.min(w * 0.42, 190);
    drawTable(ctx, { x: 12, y: h * 0.66, w: tw, title: 'F vs x', cols: ['m (g)', 'F (N)', 'x (cm)'], rows });
    const pts = readings.map((r) => ({ x: r.x, y: r.F }));
    const fit = linFit(pts);
    drawGraph(ctx, {
      x: tw + 22, y: h * 0.66, w: w - tw - 34, h: h * 0.3,
      pts, fit: pts.length >= 2 ? fit : null,
      xLabel: 'x (m)', yLabel: 'F (N)', xMax: 0.22, yMax: 5.5,
    });

    loadOut.set(`${fmt((massG / 1000) * g, 2)} N`);
    extOut.set(`${fmt(dispNow * 100, 1)} cm`);
    kTheory.set(`${fmt(keff(), 1)} N/m (${combo})`);
    if (fit && pts.length >= 2) kOut.set(`${fmt(fit.m, 1)} N/m`);
    else kOut.set('record ≥ 2 points');
    statusBadge.set(massG === 0 ? 'No load' : settled ? 'Pointer steady — record it' : 'Oscillating… wait to settle');
  });

  function drawSpring(ctx, x, y0, y1, arrangement) {
    ctx.strokeStyle = '#9ec1ff';
    ctx.lineWidth = 2;
    if (arrangement === 'parallel') {
      coil(ctx, x - 12, y0, y1);
      coil(ctx, x + 12, y0, y1);
      ctx.beginPath();
      ctx.moveTo(x - 14, y1);
      ctx.lineTo(x + 14, y1);
      ctx.stroke();
    } else if (arrangement === 'series') {
      const mid = (y0 + y1) / 2;
      coil(ctx, x, y0, mid - 4);
      ctx.fillStyle = '#5b6f99';
      ctx.fillRect(x - 7, mid - 4, 14, 8);
      coil(ctx, x, mid + 4, y1);
    } else {
      coil(ctx, x, y0, y1);
    }
  }

  function coil(ctx, x, y0, y1) {
    const turns = 9;
    const seg = (y1 - y0) / turns;
    ctx.beginPath();
    ctx.moveTo(x, y0);
    for (let i = 0; i < turns; i++) {
      const ya = y0 + seg * (i + 0.25);
      const yb = y0 + seg * (i + 0.75);
      ctx.lineTo(x + 11, ya);
      ctx.lineTo(x - 11, yb);
    }
    ctx.lineTo(x, y1);
    ctx.stroke();
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
