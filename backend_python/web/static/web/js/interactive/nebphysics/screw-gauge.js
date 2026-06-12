import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, panelBg, labelText } from './lab-utils.js';

const OBJECTS = {
  wire: { label: 'Copper wire', min: 40, max: 120 },
  sheet: { label: 'Metal sheet', min: 100, max: 250 },
  hair: { label: 'Human hair', min: 5, max: 12 },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Spindle open', '#9ec1ff');
  hud.badge('Pitch 1 mm · LC 0.01 mm', '#D97706');

  let objKey = 'wire';
  let trueSize = 0;
  let zeroErrOn = false;
  let zeroErr = 0;
  let gap = 5;
  let revealed = false;
  let ratchet = false;
  let dragging = false;
  let dragY = 0;
  let dragGap = 0;

  function newObject() {
    const o = OBJECTS[objKey];
    trueSize = (o.min + Math.floor(Math.random() * (o.max - o.min + 1))) / 100;
    zeroErr = zeroErrOn ? (Math.random() < 0.5 ? -1 : 1) * (2 + Math.floor(Math.random() * 6)) / 100 : 0;
    gap = Math.min(6, trueSize + 2.5);
    revealed = false;
    ratchet = false;
  }

  function turn(divs) {
    const next = Math.round((gap - divs * 0.01) * 100) / 100;
    if (next <= trueSize) {
      gap = trueSize;
      ratchet = true;
    } else {
      gap = Math.min(8, next);
      ratchet = false;
    }
  }

  const panel = createPanel(stage, { title: 'Screw Gauge Lab' });
  panel.select({
    label: 'Object',
    options: [
      { value: 'wire', label: 'Copper wire (diameter)' },
      { value: 'sheet', label: 'Metal sheet (thickness)' },
      { value: 'hair', label: 'Human hair (diameter)' },
    ],
    value: objKey,
    onChange: (v) => { objKey = v; newObject(); },
  });
  panel.button({ label: 'New object', icon: 'refresh', onClick: newObject });
  panel.toggle({ label: 'Zero error mode', value: false, onChange: (v) => { zeroErrOn = v; newObject(); } });
  panel.buttonRow([
    { label: '−1 turn', icon: 'rotate_left', onClick: () => turn(100) },
    { label: '−5 div', icon: 'remove', onClick: () => turn(5) },
  ]);
  panel.buttonRow([
    { label: '+1 turn', icon: 'rotate_right', onClick: () => turn(-100) },
    { label: '+5 div', icon: 'add', onClick: () => turn(-5) },
  ]);
  panel.divider();
  const obsOut = panel.readout({ label: 'Observed reading', value: '—' });
  const zeroOut = panel.readout({ label: 'Zero error', value: '—' });
  const corrOut = panel.readout({ label: 'Corrected value', value: '—' });
  panel.button({ label: 'Reveal answer', icon: 'visibility', variant: 'ghost', onClick: () => { revealed = true; } });
  panel.info('Drag up/down on the thimble (or use buttons) to close the spindle. Stop when the ratchet clicks, then read main + circular scale.');

  newObject();

  function geom(w, h) {
    return { cx: w * 0.5, cy: h * 0.34, scale: Math.min(w / 380, 1.3), zoomY: h * 0.6 };
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    if (p.y < g.zoomY && p.x > g.cx) {
      dragging = true;
      dragY = p.y;
      dragGap = gap;
      if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const divs = Math.round((p.y - dragY) / 3);
    const next = Math.round((dragGap - divs * 0.01) * 100) / 100;
    if (next <= trueSize) {
      gap = trueSize;
      ratchet = true;
    } else {
      gap = Math.min(8, next);
      ratchet = false;
    }
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function touching() { return Math.abs(gap - trueSize) < 0.0001; }

  function drawGauge(ctx, w, h) {
    const g = geom(w, h);
    const s = g.scale;
    const cy = g.cy;
    const frameX = g.cx - 150 * s;
    ctx.strokeStyle = '#39496b';
    ctx.lineWidth = 22 * s;
    ctx.beginPath();
    ctx.arc(g.cx - 70 * s, cy + 50 * s, 85 * s, Math.PI * 0.55, Math.PI * 1.5);
    ctx.stroke();
    ctx.fillStyle = '#39496b';
    ctx.fillRect(frameX - 18 * s, cy - 14 * s, 30 * s, 28 * s);
    const anvilX = frameX + 12 * s;
    const obs = gap + zeroErr;
    const spindleX = anvilX + gap * 14 * s;
    ctx.fillStyle = '#71819f';
    ctx.fillRect(spindleX, cy - 7 * s, g.cx + 20 * s - spindleX, 14 * s);
    ctx.fillStyle = '#4d5f85';
    ctx.fillRect(g.cx + 20 * s, cy - 13 * s, 90 * s, 26 * s);
    ctx.fillStyle = '#5b6f99';
    const thimbleX = g.cx + 50 * s + obs * 0;
    ctx.fillRect(thimbleX + 60 * s, cy - 20 * s, 50 * s, 40 * s);
    ctx.fillStyle = '#46587e';
    ctx.fillRect(thimbleX + 110 * s, cy - 12 * s, 26 * s, 24 * s);
    if (objKey === 'wire' || objKey === 'hair') {
      ctx.fillStyle = '#D97706';
      const r = Math.max(2, (trueSize * 14 * s) / 2);
      ctx.beginPath();
      ctx.arc((anvilX + spindleX) / 2, cy, r, 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.fillStyle = '#D97706';
      ctx.fillRect(anvilX, cy - 16 * s, Math.max(2, trueSize * 14 * s), 32 * s);
    }
    labelText(ctx, OBJECTS[objKey].label, g.cx, cy + 70 * s, { size: 10, weight: 600, align: 'center', color: 'rgba(199,212,234,0.8)' });
    if (ratchet) labelText(ctx, 'click · click · click', g.cx + 90 * s, cy - 30 * s, { size: 10, weight: 700, align: 'center', color: '#8be9a8' });
  }

  function drawZoom(ctx, w, h) {
    const g = geom(w, h);
    const obs = gap + zeroErr;
    const zh = h - g.zoomY - 12;
    panelBg(ctx, 10, g.zoomY, w - 20, zh);
    labelText(ctx, 'Magnified barrel: main scale (mm) + circular scale', 20, g.zoomY + 16, { size: 9.5, weight: 600, color: 'rgba(199,212,234,0.75)' });
    const midY = g.zoomY + zh * 0.52;
    const x0 = 30;
    const pxPerMm = (w * 0.52 - x0) / 7;
    ctx.strokeStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '600 9.5px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(232,238,251,0.9)';
    for (let mm = 0; mm <= 7; mm++) {
      const x = x0 + mm * pxPerMm;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(x, midY - 16);
      ctx.lineTo(x, midY);
      ctx.stroke();
      ctx.fillText(String(mm), x, midY - 22);
    }
    ctx.strokeStyle = 'rgba(158,193,255,0.5)';
    ctx.beginPath();
    ctx.moveTo(x0 - 8, midY);
    ctx.lineTo(x0 + 7.4 * pxPerMm, midY);
    ctx.stroke();
    const edgeX = x0 + Math.min(7.2, obs) * pxPerMm;
    ctx.fillStyle = 'rgba(91,111,153,0.5)';
    ctx.fillRect(edgeX, g.zoomY + 24, w * 0.52 - edgeX + 30, zh - 32);
    ctx.strokeStyle = '#ffd584';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(edgeX, g.zoomY + 26);
    ctx.lineTo(edgeX, g.zoomY + zh - 10);
    ctx.stroke();
    const circX = w * 0.78;
    const circR = Math.min(zh * 0.42, w * 0.16);
    const reading = ((obs % 1) + 1) % 1;
    const divNow = reading * 100;
    ctx.strokeStyle = 'rgba(232,238,251,0.85)';
    ctx.textAlign = 'left';
    for (let k = -8; k <= 8; k++) {
      const div = Math.round(divNow) + k;
      const yy = midY - k * (circR / 5.5);
      if (yy < g.zoomY + 26 || yy > g.zoomY + zh - 8) continue;
      const dd = ((div % 100) + 100) % 100;
      ctx.lineWidth = dd % 5 === 0 ? 1.8 : 1;
      ctx.beginPath();
      ctx.moveTo(circX, yy);
      ctx.lineTo(circX + (dd % 5 === 0 ? 22 : 14), yy);
      ctx.stroke();
      if (dd % 5 === 0) {
        ctx.fillStyle = 'rgba(232,238,251,0.9)';
        ctx.font = '600 9.5px Poppins, sans-serif';
        ctx.fillText(String(dd), circX + 27, yy + 3);
      }
    }
    ctx.strokeStyle = '#8be9a8';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(circX - 26, midY + (divNow - Math.round(divNow)) * (circR / 5.5));
    ctx.lineTo(circX - 2, midY + (divNow - Math.round(divNow)) * (circR / 5.5));
    ctx.stroke();
    labelText(ctx, 'reference line', circX - 26, midY - 8, { size: 8.5, weight: 600, color: '#8be9a8' });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    drawGauge(ctx, w, h);
    drawZoom(ctx, w, h);
    statusBadge.set(touching() ? 'Ratchet slipping — take reading' : `Gap ≈ ${fmt(gap, 2)} mm`);
    if (revealed && touching()) {
      const obs = gap + zeroErr;
      const msr = Math.floor(obs + 1e-9);
      const csr = Math.round((obs - msr) * 100);
      obsOut.set(`${fmt(obs, 2)} mm  (${msr} + ${csr}×0.01)`);
      zeroOut.set(`${zeroErr >= 0 ? '+' : ''}${fmt(zeroErr, 2)} mm`);
      corrOut.set(`${fmt(obs - zeroErr, 2)} mm`);
    } else {
      obsOut.set(revealed ? 'Close on the object first' : '—');
      zeroOut.set(zeroErrOn ? 'hidden — close with no object to find it' : '0 (no error)');
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
