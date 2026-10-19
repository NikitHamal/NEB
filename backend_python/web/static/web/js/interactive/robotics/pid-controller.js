/**
 * PID controller — a 1 kg cart on a rail must hold the setpoint. The controller samples at 50 Hz
 * like a real microcontroller: u = Kp·e + Ki·∫e dt + Kd·de/dt (derivative taken on the measurement,
 * integral clamped against wind-up), and the motor force saturates at ±20 N. Drag the setpoint flag
 * for a step, grab the cart and let go for a disturbance, or switch on the wind for a steady push
 * that only the I term can cancel. Overshoot, settling time and steady-state error are measured.
 */
import { createKit, T, Spring, Ring, fmt, clamp, text, pill, withAlpha, softShadow, knob, arrow } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MASS = 1, FRICTION = 0.4, FMAX = 20, DT_CTRL = 0.02;

export default function init(stage) {
  const k = createKit(stage, { label: 'A cart on a rail controlled by a PID loop, with live graphs' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the flag to set a new target', T.blue);

  let kp = 14, ki = 0, kd = 4, wind = false;
  let x = 0, v = 0, sp = 1.0, integ = 0, prevX = 0, u = 0, uP = 0, uI = 0, uD = 0, ctrlT = 0, simT = 0, held = false;
  let stepT = 0, stepFrom = 0, peak = 0, settle = -1;
  const trX = new Ring(800), trS = new Ring(800), trP = new Ring(800), trI = new Ring(800), trD = new Ring(800);
  const pPos = new Plot({ title: 'Position (blue) and setpoint (dashed)', xLabel: 't / s', yLabel: 'm', yMin: -2.5, yMax: 2.5 });
  const pU = new Plot({ title: 'Controller output: P, I, D', xLabel: 't / s', yLabel: 'N', yMin: -20, yMax: 20 });

  const panel = createPanel(stage, { title: 'PID tuning' });
  const kpS = panel.slider({ label: 'Kp (proportional)', min: 0, max: 60, step: 0.5, value: kp, format: (v2) => v2.toFixed(1), onChange: (v2) => { kp = v2; } });
  const kiS = panel.slider({ label: 'Ki (integral)', min: 0, max: 20, step: 0.1, value: ki, format: (v2) => v2.toFixed(1), onChange: (v2) => { ki = v2; integ = 0; } });
  const kdS = panel.slider({ label: 'Kd (derivative)', min: 0, max: 15, step: 0.1, value: kd, format: (v2) => v2.toFixed(1), onChange: (v2) => { kd = v2; } });
  panel.chips({ label: 'Try', options: [{ value: 'p', label: 'P only' }, { value: 'hot', label: 'Too much Kp' }, { value: 'pd', label: 'PD' }, { value: 'pid', label: 'PID' }], value: 'pd', onChange: (c) => { const g = { p: [14, 0, 0], hot: [55, 0, 0.5], pd: [14, 0, 4], pid: [14, 6, 4.5] }[c]; kp = g[0]; ki = g[1]; kd = g[2]; kpS.set(kp); kiS.set(ki); kdS.set(kd); integ = 0; newStep(sp); } });
  panel.toggle({ label: 'Wind pushes the cart (6 N)', value: false, onChange: (w) => { wind = w; } });
  const st = panel.stats([{ key: 'os', label: 'Overshoot' }, { key: 'ts', label: 'Settling time (2 %)' }, { key: 'ess', label: 'Error now' }, { key: 'u', label: 'Motor force' }]);
  panel.info('P pushes harder the further away it is (too much: it overshoots and oscillates). D brakes as it approaches (damping). I adds up the error over time and removes the steady offset a constant push leaves behind.');

  function newStep(target) { stepFrom = x; sp = target; stepT = simT; peak = 0; settle = -1; }

  let railY = 0, x0 = 0, x1 = 0, scale = 100;
  k.onResize((w, h) => {
    railY = k.small ? 96 : 120; x0 = 30; x1 = w - 30; scale = (x1 - x0) / 5.4;
    const gy = railY + 60, gh = (h - gy - 16) / 2 - 6;
    pPos.box(14, gy, w - 28, gh); pU.box(14, gy + gh + 12, w - 28, gh);
  });
  const X = (m) => (x0 + x1) / 2 + m * scale;
  const flag = k.drag({
    hit: (px, py, s) => (Math.abs(px - X(sp)) < 16 + s && py > railY - 74 && py < railY - 10 ? Math.abs(px - X(sp)) : false),
    move: (px) => newStep(clamp(Math.round((px - (x0 + x1) / 2) / scale * 10) / 10, -2.4, 2.4)),
    cursor: 'ew-resize',
  });
  let grabOff = 0;
  const cartH = k.drag({
    hit: (px, py, s) => (Math.abs(px - X(x)) < 34 + s && Math.abs(py - (railY - 6)) < 22 + s ? 1 : false),
    down: (px) => { held = true; grabOff = px - X(x); },
    move: (px) => { const nx = clamp((px - grabOff - (x0 + x1) / 2) / scale, -2.6, 2.6); v = (nx - x) / Math.max(1e-3, 1 / 60); x = nx; },
    up: () => { held = false; newStep(sp); },
  });

  k.frame((ctx, dt, w, h) => {
    const n = Math.max(1, Math.ceil(dt / 0.002)), hh = dt / n;
    for (let i = 0; i < n; i++) {
      simT += hh; ctrlT += hh;
      if (ctrlT >= DT_CTRL) {
        ctrlT -= DT_CTRL;
        const e = sp - x;
        integ = clamp(integ + e * DT_CTRL, -FMAX / Math.max(ki, 1e-3), FMAX / Math.max(ki, 1e-3));
        uP = kp * e; uI = ki * integ; uD = -kd * (x - prevX) / DT_CTRL; prevX = x;
        u = clamp(uP + uI + uD, -FMAX, FMAX);
      }
      if (!held) {
        const F = u - FRICTION * v + (wind ? 6 : 0);
        v += F / MASS * hh; x += v * hh;
        if (x < -2.6 || x > 2.6) { x = clamp(x, -2.6, 2.6); v = 0; }
      }
    }
    trX.push(simT, x); trS.push(simT, sp); trP.push(simT, uP); trI.push(simT, uI); trD.push(simT, uD);
    // step metrics
    const dist = sp - stepFrom;
    if (Math.abs(dist) > 0.05) {
      const over = (x - stepFrom) / dist;
      if (over > peak) peak = over;
      const inBand = Math.abs(x - sp) <= 0.02 * Math.abs(dist);
      if (inBand && settle < 0) settle = simT - stepT; else if (!inBand) settle = -1;
    }
    // scene
    ctx.fillStyle = '#f7f9fd'; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#cbd5e1'; ctx.fillRect(x0 - 10, railY + 14, x1 - x0 + 20, 6);
    ctx.fillStyle = '#94a3b8'; ctx.fillRect(x0 - 14, railY - 20, 6, 40); ctx.fillRect(x1 + 8, railY - 20, 6, 40);
    for (let m = -2; m <= 2; m++) { ctx.fillStyle = T.mute; ctx.fillRect(X(m), railY + 22, 1, 6); text(ctx, `${m} m`, X(m), railY + 40, T.mute, 9.5, 600, 'center'); }
    // setpoint flag
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(X(sp), railY + 12); ctx.lineTo(X(sp), railY - 66); ctx.stroke();
    ctx.fillStyle = k.isHot(flag) ? T.blueDeep : T.blue; ctx.beginPath(); ctx.moveTo(X(sp), railY - 66); ctx.lineTo(X(sp) + 24, railY - 58); ctx.lineTo(X(sp), railY - 50); ctx.fill();
    text(ctx, 'target', X(sp) + 4, railY - 72, T.blue, 10, 700);
    // cart
    const cx = X(x);
    softShadow(ctx, cx, railY + 12, 36, 4, 0.25);
    ctx.fillStyle = held ? '#f97316' : '#334155'; ctx.beginPath(); ctx.roundRect(cx - 30, railY - 26, 60, 32, 7); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(cx - 24, railY - 22, 48, 5);
    for (const d of [-18, 18]) { ctx.beginPath(); ctx.arc(cx + d, railY + 8, 7, 0, Math.PI * 2); ctx.fillStyle = '#0f172a'; ctx.fill(); ctx.beginPath(); ctx.arc(cx + d, railY + 8, 2.5, 0, Math.PI * 2); ctx.fillStyle = '#94a3b8'; ctx.fill(); }
    if (Math.abs(u) > 0.2) arrow(ctx, cx, railY - 40, cx + u * 3, railY - 40, T.green, 3);
    if (wind) { for (let i = 0; i < 3; i++) { const yy = railY - 30 + i * 10, xx = cx - 70 - ((k.t * 120 + i * 30) % 60); ctx.strokeStyle = withAlpha(T.sky, 0.6); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(xx, yy); ctx.lineTo(xx + 24, yy); ctx.stroke(); } }
    if (!held && !k.small) text(ctx, 'grab and fling the cart', cx, railY - 34 - (Math.abs(u) > 0.2 ? 12 : 0) - 6, T.mute, 9.5, 600, 'center');
    // graphs
    const span = 10, t1 = Math.max(span, simT);
    pPos.range(t1 - span, t1, -2.6, 2.6).frame(ctx);
    pPos.clip(ctx);
    ctx.setLineDash([5, 4]); pPos.ring(ctx, trS, T.slate, 1.5); ctx.setLineDash([]);
    pPos.ring(ctx, trX, T.blue, 2.2);
    pPos.unclip(ctx);
    pU.range(t1 - span, t1, -FMAX * 1.2, FMAX * 1.2).frame(ctx);
    pU.clip(ctx); pU.ring(ctx, trP, T.red, 1.6); pU.ring(ctx, trI, T.purple, 1.6); pU.ring(ctx, trD, T.green, 1.6); pU.unclip(ctx);
    text(ctx, 'P', pU.ix + pU.iw - 60, pU.y + 18, T.red, 11, 800); text(ctx, 'I', pU.ix + pU.iw - 40, pU.y + 18, T.purple, 11, 800); text(ctx, 'D', pU.ix + pU.iw - 20, pU.y + 18, T.green, 11, 800);
    st.os.set(Math.abs(dist) > 0.05 ? `${fmt(Math.max(0, peak - 1) * 100, 0)} %` : '—');
    st.ts.set(settle >= 0 ? `${fmt(settle, 2)} s` : 'not yet');
    st.ess.set(`${fmt(sp - x, 3)} m`); st.u.set(`${fmt(u, 1)} N${Math.abs(u) >= FMAX - 0.01 ? ' (max)' : ''}`);
    const osc = peak > 1.3;
    badge.set(held ? 'Let go and watch it recover' : wind && ki === 0 && Math.abs(sp - x) > 0.05 && settle < 0 && Math.abs(v) < 0.02 ? 'The wind leaves a steady error: add some Ki' : osc ? 'Big overshoot: lower Kp or raise Kd' : settle >= 0 ? `Settled in ${fmt(settle, 2)} s` : 'Drag the flag to set a new target');
    k.animate(true);
  });

  newStep(1);
  k.debug = { flag: () => [X(sp), railY - 58], cart: () => [X(x), railY - 6], state: () => ({ x, sp, peak, settle }) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
