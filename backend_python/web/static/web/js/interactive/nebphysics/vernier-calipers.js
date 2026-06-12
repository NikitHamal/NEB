import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, panelBg, labelText } from './lab-utils.js';

const OBJECTS = {
  sphere: { label: 'Steel sphere', min: 160, max: 250 },
  cylinder: { label: 'Metal cylinder', min: 80, max: 150 },
  beaker: { label: 'Beaker depth', min: 300, max: 520 },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Jaws open', '#9ec1ff');
  const lcBadge = hud.badge('LC = 0.01 cm', '#D97706');

  let objKey = 'sphere';
  let trueSize = 0;
  let zeroErrOn = false;
  let zeroErr = 0;
  let jawGap = 400;
  let showHint = false;
  let revealed = false;
  let dragging = false;
  let dragStartX = 0;
  let dragStartGap = 0;

  function newObject() {
    const o = OBJECTS[objKey];
    trueSize = (o.min + Math.floor(Math.random() * (o.max - o.min + 1))) / 10;
    zeroErr = zeroErrOn ? (Math.random() < 0.5 ? -1 : 1) * (1 + Math.floor(Math.random() * 4)) / 10 : 0;
    jawGap = Math.min(110, trueSize + 25);
    revealed = false;
  }

  const panel = createPanel(stage, { title: 'Vernier Lab' });
  panel.select({
    label: 'Object to measure',
    options: [
      { value: 'sphere', label: 'Steel sphere (diameter)' },
      { value: 'cylinder', label: 'Cylinder (diameter)' },
      { value: 'beaker', label: 'Beaker (internal depth)' },
    ],
    value: objKey,
    onChange: (v) => { objKey = v; newObject(); },
  });
  panel.button({ label: 'New object', icon: 'refresh', onClick: newObject });
  panel.toggle({ label: 'Zero error mode', value: false, onChange: (v) => { zeroErrOn = v; newObject(); } });
  panel.toggle({ label: 'Highlight coincidence', value: false, onChange: (v) => { showHint = v; } });
  panel.buttonRow([
    { label: 'Close −0.01', icon: 'remove', onClick: () => { jawGap = Math.max(trueSize, +(jawGap - 0.1).toFixed(1)); } },
    { label: 'Open +0.01', icon: 'add', onClick: () => { jawGap = Math.min(118, +(jawGap + 0.1).toFixed(1)); } },
  ]);
  panel.divider();
  const obsOut = panel.readout({ label: 'Observed reading', value: '—' });
  const zeroOut = panel.readout({ label: 'Zero error', value: '—' });
  const corrOut = panel.readout({ label: 'Corrected value', value: '—' });
  panel.button({
    label: 'Reveal answer',
    icon: 'visibility',
    variant: 'ghost',
    onClick: () => { revealed = true; },
  });
  panel.info('Drag the sliding jaw until it just grips the object, then read main scale + coincident vernier division from the magnified strip.');

  newObject();

  function geom(w, h) {
    const pxPerMm = (w - 70) / 125;
    return { x0: 30, beamY: h * 0.2, pxPerMm, zoomY: h * 0.62, jawTop: h * 0.2 + 34 };
  }

  function gripping() {
    return Math.abs(jawGap - trueSize) < 0.005;
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    const slideX = g.x0 + jawGap * g.pxPerMm;
    if (p.y < g.zoomY - 10 && Math.abs(p.x - slideX) < 70) {
      dragging = true;
      dragStartX = p.x;
      dragStartGap = jawGap;
      if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    let next = dragStartGap + (p.x - dragStartX) / g.pxPerMm;
    next = Math.round(next * 10) / 10;
    jawGap = Math.max(trueSize, Math.min(118, next));
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function drawCaliper(ctx, w, h) {
    const g = geom(w, h);
    const obs = jawGap + zeroErr;
    ctx.fillStyle = '#39496b';
    ctx.fillRect(g.x0 - 14, g.beamY, w - g.x0 - 14, 30);
    ctx.fillStyle = 'rgba(255,255,255,0.08)';
    ctx.fillRect(g.x0 - 14, g.beamY, w - g.x0 - 14, 6);
    ctx.strokeStyle = 'rgba(232,238,251,0.85)';
    ctx.lineWidth = 1;
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let mm = 0; mm <= 120; mm += 1) {
      const x = g.x0 + mm * g.pxPerMm;
      const len = mm % 10 === 0 ? 12 : mm % 5 === 0 ? 8 : 5;
      ctx.beginPath();
      ctx.moveTo(x, g.beamY);
      ctx.lineTo(x, g.beamY + len);
      ctx.stroke();
      if (mm % 10 === 0) {
        ctx.fillStyle = 'rgba(232,238,251,0.9)';
        ctx.fillText(String(mm / 10), x, g.beamY + 24);
      }
    }
    ctx.fillStyle = '#4d5f85';
    ctx.fillRect(g.x0 - 16, g.beamY - 4, 14, 86);
    const slideX = g.x0 + jawGap * g.pxPerMm;
    const vzX = g.x0 + obs * g.pxPerMm;
    ctx.fillStyle = '#5b6f99';
    ctx.fillRect(vzX, g.beamY - 4, 9 * g.pxPerMm + 18, 38);
    ctx.fillRect(slideX, g.beamY + 30, 12, 52);
    ctx.strokeStyle = '#ffd584';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(vzX, g.beamY + 30);
    ctx.lineTo(vzX, g.beamY + 34);
    ctx.stroke();
    const oy = g.jawTop + 24;
    const ow = jawGap * g.pxPerMm;
    ctx.fillStyle = '#D97706';
    if (objKey === 'sphere') {
      const r = (trueSize * g.pxPerMm) / 2;
      ctx.beginPath();
      ctx.arc(g.x0 + r, oy + 12, r, 0, Math.PI * 2);
      ctx.fill();
    } else if (objKey === 'cylinder') {
      ctx.fillRect(g.x0, oy, trueSize * g.pxPerMm, 30);
      ctx.fillStyle = 'rgba(255,255,255,0.15)';
      ctx.fillRect(g.x0, oy, trueSize * g.pxPerMm, 7);
    } else {
      ctx.strokeStyle = '#D97706';
      ctx.lineWidth = 4;
      ctx.strokeRect(g.x0 + 2, oy - 4, trueSize * g.pxPerMm - 4, 34);
    }
    if (!gripping()) {
      ctx.strokeStyle = 'rgba(158,193,255,0.4)';
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(g.x0 + ow, oy - 8);
      ctx.lineTo(g.x0 + ow, oy + 36);
      ctx.stroke();
      ctx.setLineDash([]);
    }
    labelText(ctx, OBJECTS[objKey].label, g.x0, oy + 56, { size: 10, weight: 600, color: 'rgba(199,212,234,0.8)' });
  }

  function drawZoom(ctx, w, h) {
    const g = geom(w, h);
    const obs = jawGap + zeroErr;
    const zh = h - g.zoomY - 12;
    panelBg(ctx, 10, g.zoomY, w - 20, zh);
    labelText(ctx, 'Magnified view (main scale in mm, vernier 0–10)', 20, g.zoomY + 16, { size: 9.5, weight: 600, color: 'rgba(199,212,234,0.75)' });
    const midY = g.zoomY + zh * 0.5;
    const zf = (w - 60) / 16;
    const cx = w / 2;
    const startMm = obs - 4;
    ctx.save();
    ctx.beginPath();
    ctx.rect(12, g.zoomY + 20, w - 24, zh - 26);
    ctx.clip();
    ctx.strokeStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let mm = Math.floor(startMm) - 2; mm <= startMm + 14; mm++) {
      if (mm < 0) continue;
      const x = cx + (mm - obs - 4) * zf + 8 * zf;
      ctx.lineWidth = mm % 10 === 0 ? 2 : 1;
      ctx.beginPath();
      ctx.moveTo(x, midY - (mm % 10 === 0 ? 26 : mm % 5 === 0 ? 22 : 17));
      ctx.lineTo(x, midY);
      ctx.stroke();
      if (mm % 10 === 0) {
        ctx.fillStyle = '#ffd584';
        ctx.fillText(`${mm / 10} cm`, x, midY - 32);
      }
    }
    const frac = Math.round((obs - Math.floor(obs + 1e-6)) * 10);
    for (let d = 0; d <= 10; d++) {
      const mmPos = obs + d * 0.9;
      const x = cx + (mmPos - obs - 4) * zf + 8 * zf;
      const coincident = d === frac;
      ctx.strokeStyle = coincident && showHint ? '#8be9a8' : 'rgba(255,213,132,0.95)';
      ctx.lineWidth = coincident && showHint ? 2.4 : 1.2;
      ctx.beginPath();
      ctx.moveTo(x, midY + 2);
      ctx.lineTo(x, midY + (d % 5 === 0 ? 22 : 16));
      ctx.stroke();
      if (d % 5 === 0 || (coincident && showHint)) {
        ctx.fillStyle = coincident && showHint ? '#8be9a8' : 'rgba(255,213,132,0.9)';
        ctx.fillText(String(d), x, midY + 34);
      }
    }
    ctx.restore();
    ctx.strokeStyle = 'rgba(158,193,255,0.35)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(12, midY);
    ctx.lineTo(w - 12, midY);
    ctx.stroke();
  }

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    drawCaliper(ctx, w, h);
    drawZoom(ctx, w, h);
    const obs = jawGap + zeroErr;
    statusBadge.set(gripping() ? 'Jaws gripping — take reading' : 'Jaws open');
    if (revealed && gripping()) {
      const msr = Math.floor(obs + 1e-6);
      const vd = Math.round((obs - msr) * 10);
      obsOut.set(`${fmt(obs / 10, 3)} cm  (${(msr / 10).toFixed(1)} + ${vd}×0.01)`);
      zeroOut.set(`${zeroErr >= 0 ? '+' : ''}${fmt(zeroErr / 10, 2)} cm`);
      corrOut.set(`${fmt((obs - zeroErr) / 10, 3)} cm`);
    } else {
      obsOut.set(revealed ? 'Grip the object first' : '—');
      zeroOut.set(zeroErrOn ? (revealed ? '—' : 'hidden — close jaws fully to find it') : '0 (no error)');
      corrOut.set('—');
    }
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
