import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, linFit, drawTable, drawGraph, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Move the pins', '#9ec1ff');

  let mode = 'lens';
  let fTrue = 15;
  let objPos = 20;
  let imgPin = 80;
  let dragTarget = null;
  let revealed = false;
  const records = [];

  function newElement() {
    fTrue = Math.round((10 + Math.random() * 8) * 2) / 2;
    records.length = 0;
    revealed = false;
  }

  function elementPos() { return mode === 'lens' ? 50 : 90; }

  function u() { return Math.abs(elementPos() - objPos); }

  function v() {
    const uu = u();
    if (uu <= fTrue + 0.01) return null;
    return (uu * fTrue) / (uu - fTrue);
  }

  function imagePos() {
    const vv = v();
    if (vv === null) return null;
    return mode === 'lens' ? elementPos() + vv : elementPos() - vv;
  }

  function aligned() {
    const ip = imagePos();
    return ip !== null && Math.abs(ip - imgPin) < 0.7 && ip > 0 && ip < 100;
  }

  const panel = createPanel(stage, { title: 'Optical Bench' });
  panel.select({
    label: 'Element',
    options: [
      { value: 'lens', label: 'Convex lens (at 50 cm)' },
      { value: 'mirror', label: 'Concave mirror (at 90 cm)' },
    ],
    value: 'lens',
    onChange: (v2) => { mode = v2; records.length = 0; objPos = mode === 'lens' ? 20 : 50; imgPin = mode === 'lens' ? 80 : 40; },
  });
  panel.button({ label: 'New lens/mirror', icon: 'refresh', onClick: newElement });
  panel.button({
    label: 'Record u, v',
    icon: 'edit_note',
    onClick: () => {
      if (!aligned() || records.length >= 6) return;
      const uu = u();
      const vv = Math.abs(imgPin - elementPos());
      records.push({ u: uu, v: vv, f: (uu * vv) / (uu + vv) });
    },
  });
  panel.button({ label: 'Clear table', icon: 'delete', variant: 'ghost', onClick: () => { records.length = 0; } });
  panel.divider();
  const uOut = panel.readout({ label: 'Object distance u', value: '—' });
  const vOut = panel.readout({ label: 'Image distance v', value: '—' });
  const fOut = panel.readout({ label: 'Mean f = uv/(u+v)', value: '—' });
  panel.button({ label: 'Reveal true f', icon: 'visibility', onClick: () => { revealed = true; } });
  panel.info('Drag the object pin (left) and the image pin until the image pin sits exactly on the real image — no parallax. Record several u-v pairs; f = uv/(u+v) and the 1/v vs 1/u graph confirm it.');

  newElement();

  function benchGeom(w, h) {
    return { x0: w * 0.06, x1: w * 0.94, by: h * 0.4 };
  }

  function cmToX(cm, g) { return g.x0 + ((g.x1 - g.x0) * cm) / 100; }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const g = benchGeom(sim.width, sim.height);
    const ox = cmToX(objPos, g);
    const ix = cmToX(imgPin, g);
    if (Math.abs(p.x - ox) < 30 && Math.abs(p.y - g.by) < 90) dragTarget = 'obj';
    else if (Math.abs(p.x - ix) < 30 && Math.abs(p.y - g.by) < 90) dragTarget = 'img';
    if (dragTarget) {
      if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragTarget) return;
    const p = pointerPos(sim.canvas, e);
    const g = benchGeom(sim.width, sim.height);
    let cm = ((p.x - g.x0) / (g.x1 - g.x0)) * 100;
    cm = Math.round(cm * 5) / 5;
    if (dragTarget === 'obj') {
      objPos = mode === 'lens' ? Math.max(2, Math.min(46, cm)) : Math.max(30, Math.min(86, cm));
    } else {
      imgPin = mode === 'lens' ? Math.max(54, Math.min(99, cm)) : Math.max(2, Math.min(86, cm));
    }
  }

  function onUp() { dragTarget = null; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    const g = benchGeom(w, h);

    ctx.fillStyle = '#2b3a57';
    ctx.fillRect(g.x0 - 10, g.by + 30, g.x1 - g.x0 + 20, 10);
    ctx.font = '600 8.5px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let cm = 0; cm <= 100; cm += 10) {
      const xx = cmToX(cm, g);
      ctx.strokeStyle = 'rgba(232,238,251,0.55)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(xx, g.by + 30);
      ctx.lineTo(xx, g.by + 24);
      ctx.stroke();
      ctx.fillStyle = 'rgba(232,238,251,0.8)';
      ctx.fillText(String(cm), xx, g.by + 52);
    }

    const ex = cmToX(elementPos(), g);
    if (mode === 'lens') {
      ctx.strokeStyle = '#9ec1ff';
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.ellipse(ex, g.by - 20, 7, 52, 0, 0, Math.PI * 2);
      ctx.stroke();
      labelText(ctx, 'convex lens', ex, g.by - 84, { size: 9, weight: 600, align: 'center', color: '#9ec1ff' });
    } else {
      ctx.strokeStyle = '#9ec1ff';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(ex + 48, g.by - 20, 70, Math.PI - 0.75, Math.PI + 0.75);
      ctx.stroke();
      labelText(ctx, 'concave mirror', ex, g.by - 100, { size: 9, weight: 600, align: 'center', color: '#9ec1ff' });
    }

    const ox = cmToX(objPos, g);
    drawPin(ctx, ox, g.by + 30, 56, '#F59E0B', 'object pin');

    const vv = v();
    const ip = imagePos();
    if (vv !== null && ip !== null && ip > 0 && ip < 100) {
      const ix2 = cmToX(ip, g);
      const mfac = vv / u();
      const ih = Math.min(70, 32 * mfac);
      ctx.save();
      ctx.globalAlpha = 0.55;
      drawArrowPin(ctx, ix2, g.by - 20, ih, '#8be9a8', true);
      ctx.restore();
      ctx.strokeStyle = 'rgba(255,213,132,0.5)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(ox, g.by - 52);
      ctx.lineTo(ex, g.by - 52);
      ctx.lineTo(ix2, g.by - 20 + ih);
      ctx.moveTo(ox, g.by - 52);
      ctx.lineTo(ex, g.by - 20);
      ctx.lineTo(ix2, g.by - 20 + ih);
      ctx.stroke();
    }

    const px = cmToX(imgPin, g);
    drawPin(ctx, px, g.by + 30, 44, aligned() ? '#8be9a8' : '#c7d4ea', 'image pin');

    const rows = records.map((r) => [fmt(r.u, 1), fmt(r.v, 1), fmt(r.f, 2)]);
    const tw = Math.min(w * 0.4, 180);
    drawTable(ctx, { x: 12, y: h * 0.62, w: tw, title: 'u-v method', cols: ['u (cm)', 'v (cm)', 'f (cm)'], rows });
    const pts = records.map((r) => ({ x: 1 / r.u, y: 1 / r.v }));
    drawGraph(ctx, {
      x: tw + 22, y: h * 0.62, w: w - tw - 34, h: h * 0.34,
      pts, fit: pts.length >= 2 ? linFit(pts) : null,
      xLabel: '1/u (cm⁻¹)', yLabel: '1/v (cm⁻¹)', xMax: 0.08, yMax: 0.08,
    });

    uOut.set(`${fmt(u(), 1)} cm`);
    vOut.set(vv === null ? 'virtual / no real image' : `${fmt(Math.abs(imgPin - elementPos()), 1)} cm pin (image at ${fmt(vv, 1)})`);
    if (records.length) {
      const mean = records.reduce((s, r) => s + r.f, 0) / records.length;
      fOut.set(revealed ? `${fmt(mean, 2)} cm (true ${fmt(fTrue, 1)})` : `${fmt(mean, 2)} cm`);
    } else {
      fOut.set('—');
    }
    statusBadge.set(
      vv === null ? 'Object inside focus — image is virtual!'
        : ip !== null && (ip <= 0 || ip >= 100) ? 'Image beyond the bench — move object'
          : aligned() ? 'No parallax — record u and v!'
            : 'Slide the image pin onto the green image',
    );
  });

  function drawPin(ctx, x, baseY, len, color, label) {
    ctx.fillStyle = '#39496b';
    ctx.fillRect(x - 9, baseY - 12, 18, 12);
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    ctx.moveTo(x, baseY - 12);
    ctx.lineTo(x, baseY - 12 - len);
    ctx.stroke();
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, baseY - 12 - len, 4, 0, Math.PI * 2);
    ctx.fill();
    labelText(ctx, label, x, baseY + 14, { size: 8.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.75)' });
  }

  function drawArrowPin(ctx, x, tipY, len, color, inverted) {
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    ctx.moveTo(x, tipY);
    ctx.lineTo(x, tipY + (inverted ? len : -len));
    ctx.stroke();
    const ay = tipY + (inverted ? len : -len);
    ctx.beginPath();
    ctx.moveTo(x - 5, ay - (inverted ? 7 : -7));
    ctx.lineTo(x, ay);
    ctx.lineTo(x + 5, ay - (inverted ? 7 : -7));
    ctx.closePath();
    ctx.fill();
  }

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
