import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const HISTORY = 360;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const panel = createPanel(stage, { title: 'PID Tuning' });
  const hud = createHud(stage);
  const badge = hud.badge('Tune the gains, then disturb the cart', '#075985');

  let kp = 8;
  let ki = 0;
  let kd = 0;
  const cart = { pos: -1.2, vel: 0 };
  const targetPos = 0;
  let integral = 0;
  let prevError = targetPos - cart.pos;
  let disturbance = 0;
  const history = new Float32Array(HISTORY);
  let histIdx = 0;
  let histFilled = 0;
  let sampleAcc = 0;

  const kpSlider = panel.slider({
    label: 'Kp (proportional)', min: 0, max: 30, step: 0.5, value: kp,
    format: (v) => v.toFixed(1),
    onChange: (v) => { kp = v; },
  });
  const kiSlider = panel.slider({
    label: 'Ki (integral)', min: 0, max: 10, step: 0.1, value: ki,
    format: (v) => v.toFixed(1),
    onChange: (v) => { ki = v; },
  });
  const kdSlider = panel.slider({
    label: 'Kd (derivative)', min: 0, max: 12, step: 0.1, value: kd,
    format: (v) => v.toFixed(1),
    onChange: (v) => { kd = v; },
  });
  const errRead = panel.readout({ label: 'Error', value: '0.00' });
  panel.section('Disturb');
  panel.buttonRow([
    { label: 'Nudge ←', icon: 'arrow_back', onClick: () => { cart.vel -= 2.2; } },
    { label: 'Nudge →', icon: 'arrow_forward', onClick: () => { cart.vel += 2.2; } },
  ]);
  const windBtn = panel.button({
    label: 'Constant push: OFF', icon: 'air',
    onClick: () => {
      disturbance = disturbance ? 0 : 3.5;
      windBtn.setLabel(disturbance ? 'Constant push: ON' : 'Constant push: OFF');
    },
  });
  panel.section('Presets');
  panel.buttonRow([
    { label: 'P only', variant: 'ghost', onClick: () => setGains(14, 0, 0) },
    { label: 'PD', variant: 'ghost', onClick: () => setGains(14, 0, 5) },
    { label: 'PID', variant: 'ghost', onClick: () => setGains(14, 2.5, 5) },
  ]);
  panel.button({
    label: 'Reset cart', icon: 'restart_alt', variant: 'ghost',
    onClick: () => { cart.pos = -1.2; cart.vel = 0; integral = 0; prevError = targetPos - cart.pos; },
  });
  panel.info('Output = Kp·e + Ki·∫e + Kd·de/dt. Raise Kp until it oscillates, damp with Kd, then add a little Ki to kill the leftover offset.');

  function setGains(p, i, d) {
    kp = p; ki = i; kd = d;
    kpSlider.set(p);
    kiSlider.set(i);
    kdSlider.set(d);
  }

  sim.setUpdate((ctx, dt, w, h) => {
    const steps = 4;
    const sdt = Math.min(dt, 0.05) / steps;
    for (let i = 0; i < steps; i++) {
      const error = targetPos - cart.pos;
      integral += error * sdt;
      integral = Math.max(-3, Math.min(3, integral));
      const derivative = sdt > 0 ? (error - prevError) / sdt : 0;
      prevError = error;
      const force = kp * error + ki * integral + kd * derivative;
      const accel = force + disturbance - cart.vel * 0.6;
      cart.vel += accel * sdt;
      cart.pos += cart.vel * sdt;
      cart.pos = Math.max(-2.4, Math.min(2.4, cart.pos));
    }
    const err = targetPos - cart.pos;
    errRead.set(err.toFixed(2));
    if (Math.abs(err) < 0.03 && Math.abs(cart.vel) < 0.08) {
      badge.set('Settled on target ✓');
      badge.el.style.setProperty('--ix-hud-color', '#35d07f');
    } else if (Math.abs(err) > 0.8) {
      badge.set('Large error — controller working…');
      badge.el.style.setProperty('--ix-hud-color', '#e2484d');
    } else {
      badge.set('Correcting…');
      badge.el.style.setProperty('--ix-hud-color', '#f5b942');
    }

    sampleAcc += dt;
    if (sampleAcc >= 1 / 60) {
      sampleAcc = 0;
      history[histIdx] = cart.pos;
      histIdx = (histIdx + 1) % HISTORY;
      if (histFilled < HISTORY) histFilled++;
    }

    ctx.clearRect(0, 0, w, h);

    const trackY = h * 0.30;
    const scaleX = w * 0.18;
    const cx = w / 2;

    ctx.strokeStyle = '#33486b';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(cx - 2.4 * scaleX - 30, trackY + 26);
    ctx.lineTo(cx + 2.4 * scaleX + 30, trackY + 26);
    ctx.stroke();

    ctx.strokeStyle = '#35d07f';
    ctx.setLineDash([6, 6]);
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx, trackY - 44);
    ctx.lineTo(cx, trackY + 26);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#35d07f';
    ctx.font = '600 12px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('target', cx, trackY - 52);

    const cartX = cx + cart.pos * scaleX;
    ctx.fillStyle = '#0EA5E9';
    roundRect(ctx, cartX - 34, trackY - 24, 68, 38, 8);
    ctx.fill();
    ctx.fillStyle = '#1c2c44';
    ctx.beginPath();
    ctx.arc(cartX - 18, trackY + 18, 9, 0, Math.PI * 2);
    ctx.arc(cartX + 18, trackY + 18, 9, 0, Math.PI * 2);
    ctx.fill();
    if (disturbance) {
      ctx.fillStyle = '#ff8a5c';
      ctx.font = '700 14px Poppins, sans-serif';
      ctx.fillText('→ push', cartX, trackY - 34);
    }

    const gx = w * 0.08;
    const gy = h * 0.52;
    const gw = w * 0.84;
    const gh = h * 0.38;
    ctx.fillStyle = 'rgba(10,18,32,0.55)';
    roundRect(ctx, gx, gy, gw, gh, 10);
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.12)';
    ctx.lineWidth = 1;
    ctx.stroke();

    const midY = gy + gh / 2;
    ctx.strokeStyle = 'rgba(53,208,127,0.55)';
    ctx.setLineDash([4, 5]);
    ctx.beginPath();
    ctx.moveTo(gx + 8, midY);
    ctx.lineTo(gx + gw - 8, midY);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.strokeStyle = '#7fc7ff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    const span = gh / 5.2;
    for (let i = 0; i < histFilled; i++) {
      const idx = (histIdx - histFilled + i + HISTORY) % HISTORY;
      const px = gx + 8 + ((gw - 16) * i) / (HISTORY - 1);
      const py = midY - history[idx] * span;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    ctx.fillStyle = 'rgba(199,212,234,0.7)';
    ctx.font = '600 11px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('cart position vs time →', gx + 10, gy + 16);
  });

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, r);
    else ctx.rect(x, y, w, h);
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
