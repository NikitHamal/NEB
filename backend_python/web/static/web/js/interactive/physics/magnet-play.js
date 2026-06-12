import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MAG_W = 110;
const MAG_H = 34;
const HALF = MAG_W / 2 - 14;
const N_CLIPS = 8;
const K_CLIP = 90000;
const K_MAG = 260000;
const SOFT = 900;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Drag the loose magnet!', '#F59E0B');

  const mag1 = { x: 120, y: 150, vx: 0, vy: 0, flip: 1 };
  const mag2 = { x: 320, y: 220, flip: 1 };
  let showField = true;
  let dragging = false;
  let dragDX = 0;
  let dragDY = 0;

  const cx = new Float32Array(N_CLIPS);
  const cy = new Float32Array(N_CLIPS);
  const cvx = new Float32Array(N_CLIPS);
  const cvy = new Float32Array(N_CLIPS);
  const crot = new Float32Array(N_CLIPS);

  function scatterClips(w, h) {
    for (let i = 0; i < N_CLIPS; i++) {
      cx[i] = 40 + Math.random() * Math.max(80, w - 80);
      cy[i] = 50 + Math.random() * Math.max(80, h - 110);
      cvx[i] = 0;
      cvy[i] = 0;
      crot[i] = Math.random() * Math.PI;
    }
  }
  scatterClips(stage.clientWidth || 360, stage.clientHeight || 420);

  const panel = createPanel(stage, { title: 'Magnet Controls' });
  panel.button({
    label: 'Flip polarity',
    icon: 'swap_horiz',
    onClick: () => { mag1.flip *= -1; },
  });
  panel.toggle({
    label: 'Field hints',
    value: true,
    onChange: (val) => { showField = val; },
  });
  panel.divider();
  const stateOut = panel.readout({ label: 'Magnets', value: '—' });
  panel.button({
    label: 'Scatter clips',
    icon: 'replay',
    onClick: () => scatterClips(sim.width, sim.height),
  });
  panel.info('Drag the loose magnet near the paperclips, then near the fixed magnet. Flip its poles and feel push turn into pull!');

  function poleX(m, sign) { return m.x + sign * m.flip * HALF; }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    if (Math.abs(p.x - mag1.x) < MAG_W / 2 + 14 && Math.abs(p.y - mag1.y) < MAG_H / 2 + 14) {
      dragging = true;
      dragDX = mag1.x - p.x;
      dragDY = mag1.y - p.y;
      mag1.vx = 0;
      mag1.vy = 0;
      sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    mag1.x = p.x + dragDX;
    mag1.y = p.y + dragDY;
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  let pfx = 0;
  let pfy = 0;
  function poleForce(x, y, polX, polY, k) {
    const dx = polX - x;
    const dy = polY - y;
    const d2 = dx * dx + dy * dy + SOFT;
    const f = k / d2;
    const d = Math.sqrt(d2);
    pfx = (dx / d) * f;
    pfy = (dy / d) * f;
  }

  function step(dt, w, h) {
    for (let i = 0; i < N_CLIPS; i++) {
      let fx = 0;
      let fy = 0;
      for (let s = -1; s <= 1; s += 2) {
        poleForce(cx[i], cy[i], poleX(mag1, s), mag1.y, K_CLIP);
        fx += pfx;
        fy += pfy;
        poleForce(cx[i], cy[i], poleX(mag2, s), mag2.y, K_CLIP);
        fx += pfx;
        fy += pfy;
      }
      cvx[i] = (cvx[i] + fx * dt) * 0.92;
      cvy[i] = (cvy[i] + fy * dt) * 0.92;
      cx[i] += cvx[i] * dt;
      cy[i] += cvy[i] * dt;
      if (cx[i] < 10) { cx[i] = 10; cvx[i] = 0; }
      if (cx[i] > w - 10) { cx[i] = w - 10; cvx[i] = 0; }
      if (cy[i] < 10) { cy[i] = 10; cvy[i] = 0; }
      if (cy[i] > h - 10) { cy[i] = h - 10; cvy[i] = 0; }
      const speed2 = cvx[i] * cvx[i] + cvy[i] * cvy[i];
      if (speed2 > 1) crot[i] = Math.atan2(cvy[i], cvx[i]);
    }
    if (!dragging) {
      let fx = 0;
      let fy = 0;
      for (let s1 = -1; s1 <= 1; s1 += 2) {
        for (let s2 = -1; s2 <= 1; s2 += 2) {
          const sign = -(s1 * mag1.flip) * (s2 * mag2.flip);
          poleForce(poleX(mag1, s1), mag1.y, poleX(mag2, s2), mag2.y, K_MAG);
          fx += sign * pfx;
          fy += sign * pfy;
        }
      }
      mag1.vx = (mag1.vx + fx * dt) * 0.9;
      mag1.vy = (mag1.vy + fy * dt) * 0.9;
      mag1.x += mag1.vx * dt;
      mag1.y += mag1.vy * dt;
      mag1.x = Math.max(MAG_W / 2, Math.min(w - MAG_W / 2, mag1.x));
      mag1.y = Math.max(MAG_H / 2, Math.min(h - MAG_H / 2, mag1.y));
      const gapX = Math.abs(mag1.x - mag2.x);
      const gapY = Math.abs(mag1.y - mag2.y);
      if (gapX < MAG_W + 4 && gapY < MAG_H + 4) {
        mag1.vx = 0;
        mag1.vy = 0;
        mag1.x = mag2.x + Math.sign(mag1.x - mag2.x || 1) * (MAG_W + 4);
      }
    }
  }

  function drawFieldLines(ctx, m) {
    const nx = poleX(m, 1);
    const sx = poleX(m, -1);
    ctx.strokeStyle = 'rgba(196,181,253,0.4)';
    ctx.lineWidth = 1.5;
    for (let i = 1; i <= 3; i++) {
      const bulge = i * 26;
      ctx.beginPath();
      ctx.moveTo(nx, m.y);
      ctx.quadraticCurveTo(m.x, m.y - bulge - MAG_H, sx, m.y);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(nx, m.y);
      ctx.quadraticCurveTo(m.x, m.y + bulge + MAG_H, sx, m.y);
      ctx.stroke();
    }
  }

  function drawMagnet(ctx, m, fixed) {
    const x0 = m.x - MAG_W / 2;
    const y0 = m.y - MAG_H / 2;
    const nLeft = m.flip < 0;
    ctx.fillStyle = nLeft ? '#ef4444' : '#3b82f6';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x0, y0, MAG_W / 2, MAG_H, [8, 0, 0, 8]);
    else ctx.rect(x0, y0, MAG_W / 2, MAG_H);
    ctx.fill();
    ctx.fillStyle = nLeft ? '#3b82f6' : '#ef4444';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(m.x, y0, MAG_W / 2, MAG_H, [0, 8, 8, 0]);
    else ctx.rect(m.x, y0, MAG_W / 2, MAG_H);
    ctx.fill();
    ctx.strokeStyle = fixed ? 'rgba(232,238,251,0.5)' : '#ffd584';
    ctx.lineWidth = fixed ? 2 : 3;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x0, y0, MAG_W, MAG_H, 8);
    else ctx.rect(x0, y0, MAG_W, MAG_H);
    ctx.stroke();
    ctx.fillStyle = '#fff';
    ctx.font = '800 15px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(nLeft ? 'N' : 'S', x0 + MAG_W / 4, m.y + 5);
    ctx.fillText(nLeft ? 'S' : 'N', m.x + MAG_W / 4, m.y + 5);
    if (fixed) {
      ctx.fillStyle = 'rgba(232,238,251,0.6)';
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.fillText('fixed', m.x, y0 - 6);
    }
  }

  sim.onResize((w, h) => {
    mag2.x = Math.max(200, w * 0.68);
    mag2.y = h * 0.55;
  });

  sim.setUpdate((ctx, dt, w, h) => {
    step(Math.min(dt, 0.05), w, h);
    ctx.clearRect(0, 0, w, h);

    if (showField) {
      drawFieldLines(ctx, mag1);
      drawFieldLines(ctx, mag2);
    }

    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    for (let i = 0; i < N_CLIPS; i++) {
      const dx = Math.cos(crot[i]) * 9;
      const dy = Math.sin(crot[i]) * 9;
      ctx.beginPath();
      ctx.moveTo(cx[i] - dx, cy[i] - dy);
      ctx.lineTo(cx[i] + dx, cy[i] + dy);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(cx[i] - dx * 0.4, cy[i] - dy * 0.4, 4, 0, Math.PI * 2);
      ctx.stroke();
    }

    drawMagnet(ctx, mag2, true);
    drawMagnet(ctx, mag1, false);

    const facing1 = mag1.x < mag2.x ? mag1.flip : -mag1.flip;
    const facing2 = mag1.x < mag2.x ? -mag2.flip : mag2.flip;
    const attract = facing1 !== facing2;
    stateOut.set(attract ? 'Pulling together' : 'Pushing apart');
    badge.set(dragging ? 'Carrying the magnet…' : attract ? 'Opposite poles attract!' : 'Same poles repel!');
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
