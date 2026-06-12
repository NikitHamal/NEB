import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MASS = 2;
const G = 9.81;
const MU = 0.45;
const BOX_W = 64;
const BOX_H = 56;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Push the box!', '#F59E0B');

  let pushStrength = 20;
  let friction = true;
  let x = 4;
  let v = 0;
  let holdDir = 0;
  let dragging = false;
  let dragForce = 0;
  let squish = 0;
  const PX_PER_M = 46;
  const WORLD_W = 12;

  const panel = createPanel(stage, { title: 'Force Controls' });
  panel.slider({
    label: 'Push strength',
    min: 5, max: 60, step: 1, value: pushStrength,
    format: (val) => `${val} N`,
    onChange: (val) => { pushStrength = val; },
  });
  panel.toggle({
    label: 'Friction',
    value: true,
    onChange: (val) => { friction = val; },
  });
  panel.divider();
  const forceOut = panel.readout({ label: 'Your force', value: '0 N' });
  const speedOut = panel.readout({ label: 'Speed', value: '0.0 m/s' });
  panel.button({
    label: 'Reset box',
    icon: 'replay',
    onClick: () => { x = 4; v = 0; holdDir = 0; dragForce = 0; squish = 0; },
  });
  panel.info('Hold the big arrow buttons to push the box, or grab the box and drag it. Turn friction off and watch it glide!');

  function arrowRects(w, h) {
    const y = h - 64;
    const bw = Math.min(86, w * 0.2);
    return {
      left: { x: 14, y, w: bw, h: 50 },
      right: { x: w - bw - 14, y, w: bw, h: 50 },
    };
  }

  function inRect(p, r) {
    return p.x >= r.x && p.x <= r.x + r.w && p.y >= r.y && p.y <= r.y + r.h;
  }

  function boxScreen(w, h) {
    const groundY = h - 110;
    return { bx: 30 + x * PX_PER_M, by: groundY, groundY };
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const r = arrowRects(sim.width, sim.height);
    if (inRect(p, r.left)) { holdDir = -1; }
    else if (inRect(p, r.right)) { holdDir = 1; }
    else {
      const b = boxScreen(sim.width, sim.height);
      if (Math.abs(p.x - b.bx) < BOX_W && Math.abs(p.y - (b.by - BOX_H / 2)) < BOX_H) {
        dragging = true;
      }
    }
    if (holdDir || dragging) {
      sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const b = boxScreen(sim.width, sim.height);
    const off = (p.x - b.bx) / PX_PER_M;
    dragForce = Math.max(-pushStrength, Math.min(pushStrength, off * 30));
  }

  function onUp() {
    holdDir = 0;
    dragging = false;
    dragForce = 0;
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function appliedForce() {
    if (dragging) return dragForce;
    return holdDir * pushStrength;
  }

  function step(dt) {
    const F = appliedForce();
    let fric = 0;
    if (friction) {
      const maxFric = MU * MASS * G;
      if (Math.abs(v) > 0.02) fric = -Math.sign(v) * maxFric;
      else if (Math.abs(F) <= maxFric) { v = 0; fric = -F; }
      else fric = -Math.sign(F) * maxFric;
    }
    const a = (F + fric) / MASS;
    v += a * dt;
    x += v * dt;
    const maxX = WORLD_W - BOX_W / PX_PER_M;
    if (x < 0.2) { x = 0.2; v = Math.abs(v) * 0.3; squish = 1; }
    if (x > maxX) { x = maxX; v = -Math.abs(v) * 0.3; squish = 1; }
    squish = Math.max(0, squish - dt * 4);
  }

  function drawArrow(ctx, x0, y0, len, color, label) {
    if (Math.abs(len) < 4) return;
    const dir = Math.sign(len);
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x0 + len - dir * 10, y0);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x0 + len, y0);
    ctx.lineTo(x0 + len - dir * 14, y0 - 8);
    ctx.lineTo(x0 + len - dir * 14, y0 + 8);
    ctx.closePath();
    ctx.fill();
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = dir > 0 ? 'left' : 'right';
    ctx.fillText(label, x0 + len + dir * 6, y0 + 4);
  }

  function drawButton(ctx, r, dir, active) {
    ctx.fillStyle = active ? '#F59E0B' : 'rgba(245,158,11,0.25)';
    ctx.strokeStyle = '#F59E0B';
    ctx.lineWidth = 2;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(r.x, r.y, r.w, r.h, 16);
    else ctx.rect(r.x, r.y, r.w, r.h);
    ctx.fill();
    ctx.stroke();
    const cx = r.x + r.w / 2;
    const cy = r.y + r.h / 2;
    ctx.fillStyle = active ? '#1c1206' : '#ffd584';
    ctx.beginPath();
    ctx.moveTo(cx + dir * 14, cy);
    ctx.lineTo(cx - dir * 8, cy - 12);
    ctx.lineTo(cx - dir * 8, cy + 12);
    ctx.closePath();
    ctx.fill();
  }

  sim.setUpdate((ctx, dt, w, h) => {
    step(Math.min(dt, 0.05));
    ctx.clearRect(0, 0, w, h);
    const b = boxScreen(w, h);

    ctx.fillStyle = '#14532d';
    ctx.fillRect(0, b.groundY, w, h - b.groundY);
    ctx.fillStyle = '#22c55e';
    ctx.fillRect(0, b.groundY, w, 8);
    ctx.fillStyle = 'rgba(255,255,255,0.12)';
    for (let gx = 20; gx < w; gx += 60) {
      ctx.fillRect(gx, b.groundY + 18, 26, 4);
    }

    const sq = squish * 8;
    const bw = BOX_W + sq;
    const bh = BOX_H - sq;
    const grad = ctx.createLinearGradient(0, b.by - bh, 0, b.by);
    grad.addColorStop(0, '#fbbf24');
    grad.addColorStop(1, '#f59e0b');
    ctx.fillStyle = grad;
    ctx.strokeStyle = '#92400e';
    ctx.lineWidth = 3;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(b.bx - bw / 2, b.by - bh, bw, bh, 12);
    else ctx.rect(b.bx - bw / 2, b.by - bh, bw, bh);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#451a03';
    ctx.beginPath();
    ctx.arc(b.bx - 12, b.by - bh + 20, 4, 0, Math.PI * 2);
    ctx.arc(b.bx + 12, b.by - bh + 20, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#451a03';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(b.bx, b.by - bh + 30, 9, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();

    const F = appliedForce();
    drawArrow(ctx, b.bx, b.by - bh / 2, F * 2.2, '#fb7185', 'force');
    drawArrow(ctx, b.bx, b.by - bh - 22, v * 14, '#38bdf8', 'speed');

    const r = arrowRects(w, h);
    drawButton(ctx, r.left, -1, holdDir === -1);
    drawButton(ctx, r.right, 1, holdDir === 1);

    forceOut.set(`${Math.abs(F).toFixed(0)} N`);
    speedOut.set(`${Math.abs(v).toFixed(1)} m/s`);
    badge.set(
      dragging ? 'Dragging!' :
      holdDir !== 0 ? 'Pushing!' :
      Math.abs(v) > 0.1 ? (friction ? 'Friction is slowing it…' : 'Gliding — no friction!') :
      'Push the box!'
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
