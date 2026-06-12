import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, panelBg, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('On plane glass', '#9ec1ff');
  hud.badge('Pitch 1 mm · LC 0.01 mm', '#D97706');

  const legDist = 40;
  let trueR = 0;
  let sagitta = 0;
  let onGlass = true;
  let screwH = 3;
  let zeroRead = null;
  let glassRead = null;
  let dragging = false;
  let dragY = 0;
  let dragH = 0;

  function newGlass() {
    trueR = 200 + Math.random() * 400;
    const a = (legDist / 10) / Math.sqrt(3);
    sagitta = (trueR / 10) - Math.sqrt((trueR / 10) * (trueR / 10) - a * a);
    sagitta = Math.round(sagitta * 1000) / 100;
    zeroRead = null;
    glassRead = null;
    screwH = 3;
    onGlass = true;
  }

  function surfaceH() { return onGlass ? 0 : sagitta; }

  function touching() { return Math.abs(screwH - surfaceH()) < 0.005; }

  function moveScrew(divs) {
    let next = Math.round((screwH - divs * 0.01) * 100) / 100;
    next = Math.max(surfaceH(), Math.min(8, next));
    screwH = next;
  }

  const panel = createPanel(stage, { title: 'Spherometer Lab' });
  panel.select({
    label: 'Surface',
    options: [
      { value: 'plane', label: 'Plane glass slab (zero)' },
      { value: 'watch', label: 'Watch glass (convex)' },
    ],
    value: 'plane',
    onChange: (v) => { onGlass = v === 'plane'; screwH = Math.max(screwH, surfaceH() + 1.5); },
  });
  panel.button({ label: 'New watch glass', icon: 'refresh', onClick: newGlass });
  panel.buttonRow([
    { label: 'Lower −1 turn', icon: 'arrow_downward', onClick: () => moveScrew(100) },
    { label: '−5 div', icon: 'remove', onClick: () => moveScrew(5) },
  ]);
  panel.buttonRow([
    { label: 'Raise +1 turn', icon: 'arrow_upward', onClick: () => moveScrew(-100) },
    { label: '+5 div', icon: 'add', onClick: () => moveScrew(-5) },
  ]);
  panel.divider();
  const readOut = panel.readout({ label: 'Screw reading', value: '—' });
  const aOut = panel.readout({ label: 'Reading a (plane)', value: '—' });
  const bOut = panel.readout({ label: 'Reading b (glass)', value: '—' });
  const hOut = panel.readout({ label: 'h = b − a', value: '—' });
  const rOut = panel.readout({ label: 'R = l²/6h + h/2', value: '—' });
  panel.buttonRow([
    {
      label: 'Record a',
      icon: 'push_pin',
      onClick: () => { if (onGlass && touching()) zeroRead = screwH; },
    },
    {
      label: 'Record b',
      icon: 'push_pin',
      onClick: () => { if (!onGlass && touching()) glassRead = screwH; },
    },
  ]);
  panel.info(`Leg circle: l = ${legDist / 10} cm between legs. Touch the plane glass, record a. Move to the watch glass, touch again, record b. Then R = l²/6h + h/2.`);

  newGlass();

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    if (p.y < sim.height * 0.62) {
      dragging = true;
      dragY = p.y;
      dragH = screwH;
      if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const divs = Math.round((p.y - dragY) / 3);
    let next = Math.round((dragH - divs * 0.01) * 100) / 100;
    screwH = Math.max(surfaceH(), Math.min(8, next));
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function drawApparatus(ctx, w, h) {
    const cx = w * 0.5;
    const baseY = h * 0.5;
    const s = Math.min(w / 360, 1.2);
    ctx.fillStyle = '#2b3a57';
    ctx.fillRect(cx - 130 * s, baseY + 18 * s, 260 * s, 12 * s);
    if (!onGlass) {
      ctx.strokeStyle = 'rgba(158,193,255,0.8)';
      ctx.lineWidth = 5 * s;
      ctx.beginPath();
      ctx.arc(cx, baseY + 18 * s + trueR * s * 0.55, trueR * s * 0.55, Math.PI * 1.35, Math.PI * 1.65);
      ctx.stroke();
    } else {
      ctx.fillStyle = 'rgba(158,193,255,0.35)';
      ctx.fillRect(cx - 110 * s, baseY + 10 * s, 220 * s, 8 * s);
    }
    const tipY = baseY + 10 * s - (screwH - surfaceH()) * 6 * s;
    ctx.strokeStyle = '#71819f';
    ctx.lineWidth = 5 * s;
    ctx.beginPath();
    ctx.moveTo(cx - 70 * s, baseY + 10 * s - (onGlass ? 0 : (sagitta * 0)) * s);
    ctx.lineTo(cx - 50 * s, baseY - 40 * s);
    ctx.lineTo(cx + 50 * s, baseY - 40 * s);
    ctx.lineTo(cx + 70 * s, baseY + 10 * s);
    ctx.stroke();
    ctx.fillStyle = '#4d5f85';
    ctx.beginPath();
    ctx.ellipse(cx, baseY - 48 * s, 60 * s, 10 * s, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#39496b';
    ctx.fillRect(cx - 4 * s, baseY - 90 * s, 8 * s, 50 * s);
    ctx.fillStyle = '#5b6f99';
    ctx.fillRect(cx - 14 * s, baseY - 102 * s, 28 * s, 14 * s);
    ctx.strokeStyle = touching() ? '#8be9a8' : '#ffd584';
    ctx.lineWidth = 3 * s;
    ctx.beginPath();
    ctx.moveTo(cx, baseY - 40 * s);
    ctx.lineTo(cx, tipY);
    ctx.stroke();
    if (touching()) {
      ctx.fillStyle = 'rgba(139,233,168,0.25)';
      ctx.beginPath();
      ctx.arc(cx, tipY, 9 * s, 0, Math.PI * 2);
      ctx.fill();
    }
    labelText(ctx, onGlass ? 'plane glass slab' : `watch glass (R hidden)`, cx, baseY + 48 * s, { size: 10, weight: 600, align: 'center', color: 'rgba(199,212,234,0.8)' });
  }

  function drawScales(ctx, w, h) {
    const y0 = h * 0.62;
    const zh = h - y0 - 12;
    panelBg(ctx, 10, y0, w - 20, zh);
    labelText(ctx, 'Pitch scale (mm) + circular disc scale (100 div)', 20, y0 + 16, { size: 9.5, weight: 600, color: 'rgba(199,212,234,0.75)' });
    const px0 = w * 0.18;
    const midY = y0 + zh * 0.55;
    const pxPerMm = zh * 0.36 / 2;
    ctx.font = '600 9.5px Poppins, sans-serif';
    for (let mm = 0; mm <= 8; mm++) {
      const yy = midY + (screwH - mm) * pxPerMm;
      if (yy < y0 + 24 || yy > y0 + zh - 8) continue;
      ctx.strokeStyle = 'rgba(232,238,251,0.85)';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(px0, yy);
      ctx.lineTo(px0 + 18, yy);
      ctx.stroke();
      ctx.fillStyle = 'rgba(232,238,251,0.9)';
      ctx.textAlign = 'right';
      ctx.fillText(String(mm), px0 - 6, yy + 3);
    }
    ctx.strokeStyle = '#8be9a8';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(px0 - 2, midY);
    ctx.lineTo(px0 + 34, midY);
    ctx.stroke();
    labelText(ctx, 'disc edge', px0 + 38, midY + 3, { size: 8.5, weight: 600, color: '#8be9a8' });
    const circX = w * 0.66;
    const divNow = (((screwH % 1) + 1) % 1) * 100;
    ctx.textAlign = 'left';
    for (let k = -7; k <= 7; k++) {
      const div = Math.round(divNow) + k;
      const yy = midY + k * (zh / 16);
      if (yy < y0 + 24 || yy > y0 + zh - 8) continue;
      const dd = ((div % 100) + 100) % 100;
      ctx.strokeStyle = 'rgba(255,213,132,0.95)';
      ctx.lineWidth = dd % 10 === 0 ? 1.8 : 1;
      ctx.beginPath();
      ctx.moveTo(circX, yy);
      ctx.lineTo(circX + (dd % 10 === 0 ? 22 : 14), yy);
      ctx.stroke();
      if (dd % 10 === 0) {
        ctx.fillStyle = 'rgba(255,213,132,0.95)';
        ctx.font = '600 9.5px Poppins, sans-serif';
        ctx.fillText(String(dd), circX + 27, yy + 3);
      }
    }
    ctx.strokeStyle = '#8be9a8';
    ctx.beginPath();
    ctx.moveTo(circX - 24, midY - (divNow - Math.round(divNow)) * (zh / 16));
    ctx.lineTo(circX - 2, midY - (divNow - Math.round(divNow)) * (zh / 16));
    ctx.stroke();
  }

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    drawApparatus(ctx, w, h);
    drawScales(ctx, w, h);
    statusBadge.set(
      touching()
        ? (onGlass ? 'Tip touches plane glass — record a' : 'Tip touches watch glass — record b')
        : (onGlass ? 'On plane glass' : 'On watch glass'),
    );
    readOut.set(`${fmt(screwH, 2)} mm`);
    aOut.set(zeroRead === null ? '—' : `${fmt(zeroRead, 2)} mm`);
    bOut.set(glassRead === null ? '—' : `${fmt(glassRead, 2)} mm`);
    if (zeroRead !== null && glassRead !== null) {
      const hh = glassRead - zeroRead;
      hOut.set(`${fmt(hh, 2)} mm`);
      if (hh > 0.01) {
        const l = legDist;
        const R = (l * l) / (6 * hh) + hh / 2;
        rOut.set(`${fmt(R / 10, 1)} cm  (true ${fmt(trueR / 10, 1)})`);
      } else {
        rOut.set('h too small');
      }
    } else {
      hOut.set('—');
      rOut.set('—');
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
