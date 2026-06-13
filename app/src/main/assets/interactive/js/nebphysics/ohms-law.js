import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, linFit, drawTable, drawGraph, drawNeedleMeter, labelText } from './lab-utils.js';

const WIRES = {
  constantan: { label: 'Constantan wire', rho: 49e-8 },
  nichrome: { label: 'Nichrome wire', rho: 110e-8 },
  manganin: { label: 'Manganin wire', rho: 44e-8 },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Build your data table', '#9ec1ff');

  const E = 2.0;
  const rInt = 0.8;
  let wireKey = 'constantan';
  let lenCm = 100;
  const diaMm = 0.4;
  let rheo = 10;
  let keyClosed = false;
  let revealed = false;
  const readings = [];

  function wireR() {
    const area = Math.PI * Math.pow((diaMm / 1000) / 2, 2);
    return (WIRES[wireKey].rho * (lenCm / 100)) / area;
  }

  function current() {
    if (!keyClosed) return 0;
    return E / (rInt + rheo + wireR());
  }

  const panel = createPanel(stage, { title: 'Ohm\u2019s Law Lab' });
  panel.select({
    label: 'Wire sample',
    options: Object.entries(WIRES).map(([value, s]) => ({ value, label: s.label })),
    value: wireKey,
    onChange: (v) => { wireKey = v; readings.length = 0; revealed = false; },
  });
  panel.slider({
    label: 'Wire length',
    min: 50, max: 200, step: 10, value: lenCm,
    format: (v) => `${v} cm`,
    onChange: (v) => { lenCm = v; readings.length = 0; },
  });
  panel.slider({
    label: 'Rheostat',
    min: 2, max: 25, step: 0.5, value: rheo,
    format: (v) => `${v.toFixed(1)} Ω`,
    onChange: (v) => { rheo = v; },
  });
  panel.toggle({ label: 'Plug key (circuit on)', value: false, onChange: (v) => { keyClosed = v; } });
  panel.button({
    label: 'Record V & I',
    icon: 'edit_note',
    onClick: () => {
      if (!keyClosed || readings.length >= 7) return;
      const I = current();
      const noise = 1 + (Math.random() - 0.5) * 0.015;
      readings.push({ I: I * noise, V: I * wireR() * noise });
      readings.sort((a, b) => a.I - b.I);
    },
  });
  panel.button({ label: 'Clear table', icon: 'delete', variant: 'ghost', onClick: () => { readings.length = 0; } });
  panel.divider();
  const rOut = panel.readout({ label: 'R from graph slope', value: '—' });
  const rhoOut = panel.readout({ label: 'ρ = πd²R / 4L', value: '—' });
  panel.button({ label: 'Reveal accepted ρ', icon: 'visibility', onClick: () => { revealed = true; } });
  panel.info(`Wire diameter d = ${diaMm} mm (measure with screw gauge in the real lab). Close the key, vary the rheostat, record several V-I pairs, then read R from the slope.`);

  sim.setUpdate((ctx, dt, w, h) => {
    const I = current();
    const V = I * wireR();
    ctx.clearRect(0, 0, w, h);

    const top = 18;
    const cw = w - 36;
    const cx0 = 18;
    ctx.strokeStyle = 'rgba(199,212,234,0.7)';
    ctx.lineWidth = 1.6;
    ctx.strokeRect(cx0, top, cw, h * 0.3);
    labelText(ctx, '— | |— battery 2V', cx0 + 10, top - 4, { size: 9, weight: 600, color: 'rgba(199,212,234,0.8)' });

    const midX = cx0 + cw / 2;
    ctx.fillStyle = '#39496b';
    ctx.fillRect(midX - 44, top - 9, 36, 18);
    labelText(ctx, keyClosed ? 'key ●' : 'key ○', midX - 26, top + 4, { size: 9, weight: 700, align: 'center', color: keyClosed ? '#8be9a8' : '#ff8c8c' });

    ctx.fillStyle = '#39496b';
    ctx.fillRect(midX + 8, top - 9, 76, 18);
    labelText(ctx, `rheostat ${rheo.toFixed(1)}Ω`, midX + 46, top + 4, { size: 8.5, weight: 600, align: 'center' });

    const wy = top + h * 0.3;
    ctx.strokeStyle = '#F59E0B';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(midX - 60, wy);
    ctx.lineTo(midX + 60, wy);
    ctx.stroke();
    labelText(ctx, `${WIRES[wireKey].label} · ${lenCm} cm`, midX, wy + 16, { size: 9, weight: 600, align: 'center', color: '#ffd584' });
    if (keyClosed && I > 0.02) {
      const tt = (performance.now() / 600) % 1;
      for (let i = 0; i < 3; i++) {
        const xx = midX - 60 + ((tt + i / 3) % 1) * 120;
        ctx.fillStyle = '#8be9a8';
        ctx.beginPath();
        ctx.arc(xx, wy, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    const meterR = Math.min(w * 0.16, 64);
    drawNeedleMeter(ctx, { cx: w * 0.25, cy: h * 0.52, r: meterR, value: I, min: 0, max: 1, label: `A: ${fmt(I, 2)} A`, divisions: 10 });
    drawNeedleMeter(ctx, { cx: w * 0.75, cy: h * 0.52, r: meterR, value: V, min: 0, max: 3, label: `V: ${fmt(V, 2)} V`, divisions: 6 });

    const rows = readings.map((r) => [fmt(r.I, 3), fmt(r.V, 3), fmt(r.V / r.I, 2)]);
    const tw = Math.min(w * 0.42, 180);
    drawTable(ctx, { x: 12, y: h * 0.66, w: tw, title: 'Observations', cols: ['I (A)', 'V (V)', 'V/I'], rows });
    const pts = readings.map((r) => ({ x: r.I, y: r.V }));
    const fit = linFit(pts);
    drawGraph(ctx, {
      x: tw + 22, y: h * 0.66, w: w - tw - 34, h: h * 0.3,
      pts, fit: pts.length >= 2 ? fit : null,
      xLabel: 'I (A)', yLabel: 'V (V)', xMax: 0.8, yMax: 3,
    });

    if (fit && pts.length >= 2) {
      const R = fit.m;
      rOut.set(`${fmt(R, 2)} Ω`);
      const area = Math.PI * Math.pow((diaMm / 1000) / 2, 2);
      const rho = (R * area) / (lenCm / 100);
      rhoOut.set(revealed
        ? `${(rho * 1e8).toFixed(1)}×10⁻⁸ (true ${(WIRES[wireKey].rho * 1e8).toFixed(0)}×10⁻⁸) Ωm`
        : `${(rho * 1e8).toFixed(1)}×10⁻⁸ Ωm`);
    } else {
      rOut.set('record ≥ 2 points');
      rhoOut.set('—');
    }
    statusBadge.set(!keyClosed ? 'Close the plug key' : `I = ${fmt(I, 2)} A, V = ${fmt(V, 2)} V — vary rheostat & record`);
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
