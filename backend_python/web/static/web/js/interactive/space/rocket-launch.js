/**
 * Rocket launch — a single-stage rocket flown with Newton's laws: thrust from the exhaust
 * (mass flow = thrust ⁄ exhaust speed, 2.8 km/s), weight from gravity that weakens with height,
 * and air drag ½ρv²C_dA in an atmosphere that thins exponentially (scale height 8.5 km). The
 * state (height, speed, mass) is integrated with RK4. Drag the throttle lever during the flight;
 * as fuel burns the rocket gets lighter and accelerates harder. Reach the Kármán line at 100 km.
 */
import { createKit, T, Spring, Ring, fmt, clamp, text, withAlpha, mix, card, makeRK4, knob } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { starfield, glow, npill } from '../core/space2d.js';
import { Pool } from '../core/chem2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const VE = 2800, DRY = 2000, CD = 0.5, AREA = 1.5, RE = 6.371e6, G0 = 9.81;

export default function init(stage) {
  const k = createKit(stage, { night: true, label: 'A rocket on a launch pad with a throttle lever, altitude ruler and graphs' });
  const hud = createHud(stage);
  const badge = hud.badge('Set the throttle and press Ignite', '#60a5fa');

  let warp = 5;
  let thrustMax = 300e3, fuel0 = 12000, throttle = 1, launched = false, simT = 0, maxH = 0, reached = false, landed = false;
  const y = new Float64Array(3);
  const trH = new Ring(600), trV = new Ring(600);
  const smoke = new Pool(160);
  const cam = new Spring(0, 30, 10), shake = new Spring(0, 400, 10);
  const pH = new Plot({ title: 'Altitude', xLabel: 't / s', yLabel: 'km', yMin: 0, yMax: 10 });
  const pV = new Plot({ title: 'Speed', xLabel: 't / s', yLabel: 'm/s', yMin: 0, yMax: 500 });
  const rk = makeRK4(3, (t, s, o) => {
    const h = Math.max(0, s[0]), v = s[1], m = s[2];
    const burning = m > DRY + 1e-6 && launched;
    const F = burning ? thrustMax * throttle : 0;
    const g = G0 * (RE / (RE + h)) ** 2;
    const rho = 1.225 * Math.exp(-h / 8500);
    const drag = 0.5 * rho * v * Math.abs(v) * CD * AREA;
    o[0] = v; o[1] = (F - drag) / m - g; o[2] = burning ? -F / VE : 0;
    if (s[0] <= 0 && o[1] < 0 && v <= 0) { o[0] = 0; o[1] = 0; }
  });

  const panel = createPanel(stage, { title: 'Launch control' });
  panel.slider({ label: 'Maximum thrust', min: 50, max: 600, step: 10, value: thrustMax / 1000, format: (v) => `${v} kN`, onChange: (v) => { thrustMax = v * 1000; } });
  panel.slider({ label: 'Fuel load', min: 1000, max: 25000, step: 500, value: fuel0, format: (v) => `${(v / 1000).toFixed(1)} t`, onChange: (v) => { fuel0 = v; if (!launched) reset(); } });
  panel.chips({ label: 'Time warp', options: [{ value: '1', label: '1×' }, { value: '5', label: '5×' }, { value: '20', label: '20×' }], value: '5', onChange: (v) => { warp = +v; } });
  panel.buttonRow([{ label: 'Ignite', icon: 'local_fire_department', onClick: () => { if (!launched) { launched = true; k.animate(true); } } }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset }]);
  const st = panel.stats([{ key: 'h', label: 'Altitude' }, { key: 'v', label: 'Speed' }, { key: 'a', label: 'Acceleration' }, { key: 'twr', label: 'Thrust ÷ weight' }, { key: 'fuel', label: 'Fuel left' }, { key: 'dv', label: 'Δv = vₑ ln(m₀/m)' }]);
  panel.info('The rocket pushes exhaust down; the exhaust pushes the rocket up (Newton\'s third law). It only lifts off if thrust is bigger than its weight. Reaching 100 km takes about 1.4 km/s; escaping Earth altogether would need 11.2 km/s.');

  function reset() { y[0] = 0; y[1] = 0; y[2] = DRY + fuel0; launched = false; simT = 0; maxH = 0; reached = false; landed = false; trH.clear(); trV.clear(); smoke.clear(); cam.set(0); throttle = 1; k.animate(true); }

  let rx = 0, ry = 0, leverX = 0, leverY = 0, leverH = 0, pxPerM = 4;
  k.onResize((w, h) => {
    rx = k.small ? w * 0.42 : w * 0.34; ry = h * 0.6; pxPerM = 3.2;
    leverX = k.small ? w - 34 : w * 0.56; leverY = h * 0.25; leverH = h * 0.45;
    if (!k.small) { pH.box(w * 0.64, 16, w * 0.34, h * 0.44); pV.box(w * 0.64, h * 0.5, w * 0.34, h * 0.44); }
  });
  const lever = k.drag({
    hit: (x, yy, s) => (Math.abs(x - leverX) < 20 + s && yy > leverY - 16 && yy < leverY + leverH + 16 ? 1 : false),
    move: (x, yy) => { throttle = clamp(1 - (yy - leverY) / leverH, 0, 1); },
    cursor: 'ns-resize',
  });

  k.frame((ctx, dt, w, h) => {
    if (launched && !landed) {
      const n = Math.max(1, Math.ceil(dt * warp / 0.01)), hh = dt * warp / n;
      for (let i = 0; i < n; i++) { rk(y, simT, hh); simT += hh; if (y[0] < 0) { y[0] = 0; if (y[1] < 0) { if (simT > 2) landed = true; y[1] = 0; } } }
      if (y[2] < DRY) y[2] = DRY;
      maxH = Math.max(maxH, y[0]); if (y[0] >= 100000) reached = true;
      trH.push(simT, y[0] / 1000); trV.push(simT, y[1]);
    }
    const burning = launched && y[2] > DRY + 1 && throttle > 0.01 && !landed;
    const hgt = y[0];
    // sky darkens with altitude
    const dark = clamp(hgt / 60000, 0, 1);
    if (dark > 0.02) starfield(k, ctx, w, h, { seed: 5 });
    if (dark < 1) { ctx.fillStyle = withAlpha(mix('#7fb4ef', '#0b1730', dark), 1 - dark * dark); ctx.fillRect(0, 0, w, h); }
    // world offset: the rocket is pinned near ry, the ground scrolls away
    const scale = hgt < 300 ? pxPerM : pxPerM * Math.pow(300 / hgt, 0.85);
    const groundY = ry + 40 + hgt * scale;
    // altitude ruler
    const step = niceStep(h / scale / 5);
    ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 1;
    for (let m = Math.max(0, Math.floor((hgt - (h - ry) / scale) / step) * step); m < hgt + ry / scale; m += step) {
      const yy = groundY - m * scale; if (yy < 0 || yy > h) continue;
      ctx.beginPath(); ctx.moveTo(0, yy); ctx.lineTo(12, yy); ctx.stroke();
      text(ctx, m >= 1000 ? `${fmt(m / 1000, step < 1000 ? 1 : 0)} km` : `${m} m`, 16, yy + 3.5, 'rgba(232,238,251,0.75)', 9.5, 600);
    }
    // Kármán line
    const ky = groundY - 100000 * scale;
    if (ky > -10 && ky < h) { ctx.setLineDash([6, 6]); ctx.strokeStyle = '#a78bfa'; ctx.beginPath(); ctx.moveTo(0, ky); ctx.lineTo(w, ky); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'Kármán line · 100 km · space begins', w * 0.04 + 50, ky - 6, '#c4b5fd', 10.5, 700); }
    // clouds
    for (let c = 0; c < 6; c++) { const ch = 1500 + c * 1400, cy = groundY - ch * scale, cx = ((c * 173) % 100) / 100 * w; if (cy < -40 || cy > h + 40) continue; ctx.fillStyle = 'rgba(255,255,255,0.75)'; ctx.beginPath(); ctx.ellipse(cx, cy, 60, 14, 0, 0, Math.PI * 2); ctx.ellipse(cx + 30, cy - 8, 40, 14, 0, 0, Math.PI * 2); ctx.fill(); }
    // ground and pad
    if (groundY < h + 10) {
      ctx.fillStyle = '#4b6b3f'; ctx.fillRect(0, groundY, w, h - groundY + 2);
      ctx.fillStyle = '#6b7280'; ctx.fillRect(rx - 50, groundY - 6, 100, 8);
      ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(rx - 34, groundY - 6); ctx.lineTo(rx - 34, groundY - 120 * scale / pxPerM); ctx.stroke();
    }
    // smoke and flame
    const rocketY = groundY - hgt * scale - 6;
    const ry0 = Math.min(rocketY, ry);
    if (burning) {
      for (let i = 0; i < 3; i++) smoke.add(rx + (Math.random() - 0.5) * 8, ry0 + 6, (Math.random() - 0.5) * 40, 60 + Math.random() * 40, 6, 1.6, 0);
      shake.v += (Math.random() - 0.5) * 30 * throttle;
    }
    for (let i = smoke.n - 1; i >= 0; i--) { smoke.life[i] -= dt; if (smoke.life[i] <= 0) { smoke.kill(i); continue; } smoke.x[i] += smoke.vx[i] * dt; smoke.y[i] += (smoke.vy[i] + y[1] * scale * 0.6) * dt; smoke.r[i] += dt * 18; ctx.fillStyle = '#dcdce6'; ctx.globalAlpha = smoke.life[i] / 1.6 * 0.35 * (1 - dark); ctx.beginPath(); ctx.arc(smoke.x[i], smoke.y[i], smoke.r[i], 0, Math.PI * 2); ctx.fill(); }
    ctx.globalAlpha = 1;
    shake.step(dt);
    const sx = rx + shake.x * 0.3;
    if (burning) {
      const spread = 1 + dark * 2.5, L = 30 + 50 * throttle;
      glow(ctx, sx, ry0 + 40, 40 * spread, '#ffb347', 0.8);
      ctx.fillStyle = 'rgba(255,190,90,0.9)'; ctx.beginPath(); ctx.moveTo(sx - 7, ry0 + 30); ctx.quadraticCurveTo(sx - 7 * spread, ry0 + 30 + L * 0.6, sx, ry0 + 30 + L + Math.random() * 8); ctx.quadraticCurveTo(sx + 7 * spread, ry0 + 30 + L * 0.6, sx + 7, ry0 + 30); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,230,0.95)'; ctx.beginPath(); ctx.moveTo(sx - 4, ry0 + 30); ctx.quadraticCurveTo(sx, ry0 + 30 + L * 0.5, sx + 4, ry0 + 30); ctx.fill();
    }
    drawRocket(ctx, sx, ry0);
    // throttle lever
    ctx.fillStyle = 'rgba(15,25,48,0.85)'; ctx.beginPath(); ctx.roundRect(leverX - 14, leverY - 10, 28, leverH + 20, 10); ctx.fill();
    ctx.fillStyle = withAlpha('#f97316', 0.7); ctx.fillRect(leverX - 4, leverY + leverH * (1 - throttle), 8, leverH * throttle);
    knob(ctx, leverX, leverY + leverH * (1 - throttle), 11, '#f97316', k.isHot(lever) ? 1 : 0);
    text(ctx, 'throttle', leverX, leverY + leverH + 30, '#e8eefb', 10, 700, 'center');
    text(ctx, `${Math.round(throttle * 100)} %`, leverX, leverY - 18, '#fdba74', 11, 700, 'center');
    // graphs
    if (!k.small) {
      const t1 = Math.max(20, simT);
      pH.range(0, t1, 0, Math.max(10, Math.ceil(maxH / 1000 / 10) * 10 + 10)).frame(ctx, { theme: k.theme }); pH.clip(ctx); pH.ring(ctx, trH, '#60a5fa', 2); pH.unclip(ctx);
      let vmax = 200; for (let i = 0; i < trV.n; i++) vmax = Math.max(vmax, Math.abs(trV.y[trV.idx(i)]));
      pV.range(0, t1, Math.min(0, -vmax * 0.3), Math.ceil(vmax / 200) * 200).frame(ctx, { theme: k.theme }); pV.clip(ctx); pV.ring(ctx, trV, '#34d399', 2); pV.unclip(ctx);
    }
    const m = y[2], g = G0 * (RE / (RE + hgt)) ** 2, twr = thrustMax * throttle / (m * g);
    const rho = 1.225 * Math.exp(-hgt / 8500), acc = burning ? (thrustMax * throttle - 0.5 * rho * y[1] * Math.abs(y[1]) * CD * AREA) / m - g : -g;
    st.h.set(hgt >= 1000 ? `${fmt(hgt / 1000, 2)} km` : `${fmt(hgt, 0)} m`); st.v.set(`${fmt(y[1], 0)} m/s`);
    st.a.set(`${fmt(launched && !landed ? acc / G0 : 0, 2)} g`); st.twr.set(fmt(twr, 2));
    st.fuel.set(`${fmt((m - DRY) / 1000, 2)} t`); st.dv.set(`${fmt(VE * Math.log((DRY + fuel0) / DRY), 0)} m/s total`);
    badge.set(!launched ? (thrustMax / ((DRY + fuel0) * G0) <= 1 ? 'Thrust is less than weight: it will not lift off!' : 'Set the throttle and press Ignite') : landed ? `Back on the ground. Highest point: ${fmt(maxH / 1000, 1)} km${reached ? ' — you reached space!' : ''}` : reached ? `In space! ${fmt(hgt / 1000, 1)} km up` : burning ? (y[0] < 1 && twr <= 1 ? 'Thrust ≤ weight: still on the pad' : 'Climbing — lighter every second') : y[1] > 0 ? 'Engine off: coasting up, gravity slowing it' : 'Falling back');
    npill(ctx, `${fmt(hgt / 1000, 2)} km · ${fmt(y[1], 0)} m/s`, sx + 60, ry0 - 10, '#e8eefb', 10.5);
    k.animate((launched && !landed) || smoke.n > 0 || shake.moving || cam.moving);
  });

  function drawRocket(ctx, x, top) {
    ctx.fillStyle = '#e2e8f0'; ctx.beginPath(); ctx.moveTo(x, top - 46); ctx.quadraticCurveTo(x + 10, top - 34, x + 10, top - 20); ctx.lineTo(x + 10, top + 28); ctx.lineTo(x - 10, top + 28); ctx.lineTo(x - 10, top - 20); ctx.quadraticCurveTo(x - 10, top - 34, x, top - 46); ctx.fill();
    ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.moveTo(x, top - 46); ctx.quadraticCurveTo(x + 8, top - 37, x + 9, top - 28); ctx.lineTo(x - 9, top - 28); ctx.quadraticCurveTo(x - 8, top - 37, x, top - 46); ctx.fill();
    ctx.fillStyle = '#1e3a8a'; ctx.beginPath(); ctx.arc(x, top - 12, 4.5, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#94a3b8'; ctx.beginPath(); ctx.moveTo(x - 10, top + 12); ctx.lineTo(x - 20, top + 30); ctx.lineTo(x - 10, top + 28); ctx.fill(); ctx.beginPath(); ctx.moveTo(x + 10, top + 12); ctx.lineTo(x + 20, top + 30); ctx.lineTo(x + 10, top + 28); ctx.fill();
    ctx.fillStyle = '#475569'; ctx.fillRect(x - 6, top + 28, 12, 4);
    const f = clamp((y[2] - DRY) / Math.max(1, fuel0), 0, 1);
    ctx.fillStyle = 'rgba(37,99,235,0.35)'; ctx.fillRect(x - 8, top + 26 - 44 * f, 3, 44 * f);
  }
  function niceStep(raw) { const p = Math.pow(10, Math.floor(Math.log10(Math.max(raw, 1)))); const m = raw / p; return (m < 2 ? 2 : m < 5 ? 5 : 10) * p; }

  reset();
  k.debug = { lever: () => [leverX, leverY + leverH * (1 - throttle)], ignite: () => { launched = true; k.animate(true); }, state: () => [y[0], y[1], y[2], simT] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
