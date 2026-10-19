/**
 * Projectile motion — aim the cannon by dragging its muzzle (direction = angle, pull = speed),
 * fire, and watch a stroboscopic trail (a dot every 0.2 s) split the motion into steady
 * horizontal spacing and vertical free fall. Flight is integrated with RK4, with optional
 * quadratic air drag for a football (½ρC_dAv²); the no-air theory R = v²sin2θ/g is shown alongside.
 */
import { createKit, T, Spring, makeRK4, fmt, clamp, background, text, pill, sphere, softShadow, arrow, knob, withAlpha, dashed, DOTS } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const DEG = Math.PI / 180;
const KDRAG = 0.5 * 1.2 * 0.25 * Math.PI * 0.11 * 0.11 / 0.43;
const GHOST_COLORS = ['#7c3aed', '#0d9488', '#db2777', '#0ea5e9', '#64748b', '#16a34a'];
const MAXPTS = 1200;

export default function init(stage) {
  const k = createKit(stage, { label: 'A cannon on a field; drag the muzzle to aim' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the muzzle to aim, then fire', T.blue);

  let v0 = 22, ang = 45 * DEG, g = 9.81, air = false;
  const s = new Float64Array(4);
  let launchA = ang, launchV = v0, launchAir = false;
  let flying = false, tFly = 0, apexH = 0, result = null, targetX = 40, hitFlash = 0;
  const px = new Float32Array(MAXPTS), py = new Float32Array(MAXPTS); let np = 0;
  const ghosts = [];
  const rk = makeRK4(4, (t, y, o) => {
    o[0] = y[2]; o[1] = y[3];
    if (air) { const sp = Math.hypot(y[2], y[3]); o[2] = -KDRAG * sp * y[2]; o[3] = -g - KDRAG * sp * y[3]; }
    else { o[2] = 0; o[3] = -g; }
  });
  const zoom = new Spring(60, 40, 12);
  const recoil = new Spring(0, 300, 18);
  const hotAim = new Spring(0, 260, 26), hotFlag = new Spring(0, 260, 26);

  const panel = createPanel(stage, { title: 'Launch' });
  const vS = panel.slider({ label: 'Launch speed v₀', min: 5, max: 40, step: 0.5, value: v0, format: (v) => `${v.toFixed(1)} m/s`, onChange: (v) => { v0 = v; k.invalidate(); } });
  const aS = panel.slider({ label: 'Launch angle θ', min: 0, max: 90, step: 1, value: 45, format: (v) => `${v}°`, onChange: (v) => { ang = v * DEG; k.invalidate(); } });
  panel.chips({ label: 'Gravity', options: [{ value: '1.62', label: 'Moon' }, { value: '3.71', label: 'Mars' }, { value: '9.81', label: 'Earth' }], value: '9.81', onChange: (v) => { g = parseFloat(v); k.invalidate(); } });
  panel.toggle({ label: 'Air resistance (football)', value: false, onChange: (v) => { air = v; k.invalidate(); } });
  panel.buttonRow([
    { label: 'Fire', icon: 'rocket_launch', onClick: fire },
    { label: 'Clear', icon: 'mop', variant: 'ghost', onClick: () => { ghosts.length = 0; np = 0; result = null; flying = false; k.invalidate(); } },
  ]);
  const st = panel.stats([{ key: 'R', label: 'Range' }, { key: 'H', label: 'Max height' }, { key: 'T', label: 'Flight time' }, { key: 'th', label: 'Theory (no air)' }]);
  panel.info('Each dot is 0.2 s apart: sideways the dots are evenly spaced (no horizontal force), upwards they bunch near the top. Try 30° and 60°: same range without air. Drag the flag to set a target.');

  let ox = 60, oy = 0, wpx = 1, groundY = 0;
  k.onResize((w, h) => { groundY = h - 46; ox = k.small ? 36 : 70; oy = groundY; });
  const SX = (m) => ox + m * zoom.x;
  const SY = (m) => oy - m * zoom.x;
  const barrel = () => 46 + 0 * v0;

  function idealRange(v, a) { return v * v * Math.sin(2 * a) / g; }
  function fitScale(w, h) {
    let maxX = Math.max(idealRange(v0, 45 * DEG) * 0.75, targetX + 4, 10), maxY = 4;
    const R = idealRange(v0, ang), H = v0 * v0 * Math.sin(ang) ** 2 / (2 * g);
    maxX = Math.max(maxX, R * 1.08); maxY = Math.max(maxY, H * 1.15);
    for (const gh of ghosts) { maxX = Math.max(maxX, gh.R * 1.05); maxY = Math.max(maxY, gh.H * 1.1); }
    return Math.min((w - ox - 30) / maxX, (groundY - 40) / maxY);
  }

  function fire() {
    if (!flying && result && np > 2) archive();
    launchA = ang; launchV = v0; launchAir = air;
    s[0] = 0; s[1] = 0; s[2] = v0 * Math.cos(ang); s[3] = v0 * Math.sin(ang);
    tFly = 0; apexH = 0; np = 0; flying = true; result = null; hitFlash = 0;
    px[np] = 0; py[np] = 0; np++;
    recoil.v = -260;
    k.animate(true);
  }
  function archive() {
    if (np < 2) return;
    const gx = new Float32Array(px.subarray(0, np)), gy = new Float32Array(py.subarray(0, np));
    ghosts.unshift({ x: gx, y: gy, n: np, a: Math.round(launchA / DEG), R: result.R, H: result.H, c: GHOST_COLORS[ghosts.length % GHOST_COLORS.length], air: launchAir });
    if (ghosts.length > 6) ghosts.pop();
  }

  const aim = k.drag({
    hit: (x, y, sl) => { const mx = SX(0) + Math.cos(ang) * (barrel() + 6), my = SY(0) - Math.sin(ang) * (barrel() + 6); const d = Math.hypot(x - mx, y - my); return d < 22 + sl ? d : false; },
    move: (x, y) => {
      const dx = x - SX(0), dy = SY(0) - y;
      ang = clamp(Math.atan2(dy, dx), 0, 90 * DEG);
      aS.set(Math.round(ang / DEG)); ang = Math.round(ang / DEG) * DEG;
      const pull = Math.hypot(dx, dy);
      v0 = clamp(Math.round((5 + (pull - 30) / 4) * 2) / 2, 5, 40); vS.set(v0);
    },
    up: () => fire(),
  });
  const flag = k.drag({
    hit: (x, y, sl) => { const fx = SX(targetX); return x > fx - 14 - sl && x < fx + 30 + sl && y > groundY - 50 - sl && y < groundY + 6 ? Math.abs(x - fx) : false; },
    move: (x) => { targetX = clamp(Math.round((x - ox) / zoom.x * 2) / 2, 3, 400); },
    cursor: 'ew-resize',
  });

  k.frame((ctx, dt, w, h) => {
    if (flying) {
      let rem = dt;
      const hstep = 1 / 240;
      while (rem > 1e-9 && flying) {
        const hh = Math.min(hstep, rem);
        const prevX = s[0], prevY = s[1];
        rk(s, tFly, hh); tFly += hh; rem -= hh;
        if (s[1] > apexH) apexH = s[1];
        if (s[1] < 0 && s[3] < 0) {
          const f = prevY / (prevY - s[1]);
          s[0] = prevX + (s[0] - prevX) * f; s[1] = 0;
          tFly -= hh * (1 - f);
          flying = false;
          result = { R: s[0], T: tFly, H: apexH };
          if (Math.abs(s[0] - targetX) < Math.max(1, targetX * 0.03)) hitFlash = 1;
        }
        if (np < MAXPTS && (Math.abs(s[0] - px[np - 1]) * zoom.x > 2 || Math.abs(s[1] - py[np - 1]) * zoom.x > 2 || !flying)) { px[np] = s[0]; py[np] = s[1]; np++; }
      }
    }
    zoom.to(fitScale(w, h)); zoom.step(dt); recoil.step(dt);
    hotAim.to(k.isHot(aim) ? 1 : 0); hotAim.step(dt); hotFlag.to(k.isHot(flag) ? 1 : 0); hotFlag.step(dt);
    hitFlash = Math.max(0, hitFlash - dt * 0.6);

    background(k, ctx, w, h, '#eef5ff', '#f7fbff');
    // distant hills
    ctx.fillStyle = '#dcebd9';
    ctx.beginPath(); ctx.moveTo(0, groundY);
    for (let x = 0; x <= w; x += 20) ctx.lineTo(x, groundY - 26 - 14 * Math.sin(x * 0.006) - 8 * Math.sin(x * 0.017 + 1));
    ctx.lineTo(w, groundY); ctx.fill();
    // ground
    ctx.fillStyle = '#9ccc7d'; ctx.fillRect(0, groundY, w, h - groundY);
    ctx.fillStyle = '#86b866'; ctx.fillRect(0, groundY, w, 3);
    // metre scale on the ground
    const step = niceStepM(40 / zoom.x);
    ctx.strokeStyle = 'rgba(30,60,20,0.35)'; ctx.lineWidth = 1; ctx.beginPath();
    for (let m = 0; SX(m) < w; m += step) { ctx.moveTo(SX(m), groundY + 2); ctx.lineTo(SX(m), groundY + (m % (step * 5) === 0 ? 12 : 7)); }
    ctx.stroke();
    for (let m = 0; SX(m) < w - 20; m += step * (zoom.x * step < 50 ? 2 : 1)) text(ctx, `${fmt(m, step < 1 ? 1 : 0)} m`, SX(m), groundY + 26, '#3f5b2c', 10, 600, 'center');
    // height grid lines
    ctx.strokeStyle = 'rgba(37,99,235,0.07)'; ctx.beginPath();
    for (let m = step; SY(m) > 10; m += step) { ctx.moveTo(ox, SY(m)); ctx.lineTo(w, SY(m)); }
    ctx.stroke();
    for (let m = step; SY(m) > 18; m += step * 2) text(ctx, `${fmt(m, step < 1 ? 1 : 0)} m`, 6, SY(m) + 4, T.mute, 9.5, 600);

    // ghosts
    for (const gh of ghosts) {
      ctx.strokeStyle = withAlpha(gh.c, 0.5); ctx.lineWidth = 1.8; ctx.beginPath();
      for (let i = 0; i < gh.n; i++) { const X = SX(gh.x[i]), Y = SY(gh.y[i]); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }
      ctx.stroke();
      const lx = SX(gh.R);
      ctx.beginPath(); ctx.arc(lx, groundY, 3.5, 0, Math.PI * 2); ctx.fillStyle = gh.c; ctx.fill();
      if (!k.small) pill(ctx, `${gh.a}° · ${fmt(gh.R, 1)} m${gh.air ? ' (air)' : ''}`, lx, groundY - 14, { size: 9.5, color: gh.c });
    }
    // aim preview (ideal parabola)
    if (!flying) {
      ctx.setLineDash(DOTS); ctx.strokeStyle = withAlpha(T.blue, 0.55); ctx.lineWidth = 2; ctx.beginPath();
      const Tt = 2 * v0 * Math.sin(ang) / g;
      for (let i = 0; i <= 60; i++) { const t = Tt * i / 60, X = v0 * Math.cos(ang) * t, Y = v0 * Math.sin(ang) * t - 0.5 * g * t * t; if (i) ctx.lineTo(SX(X), SY(Y)); else ctx.moveTo(SX(X), SY(Y)); }
      ctx.stroke(); ctx.setLineDash([]);
    }
    // target flag
    const fx = SX(targetX);
    ctx.fillStyle = withAlpha(hitFlash > 0 ? T.green : T.red, 0.18 + 0.2 * hitFlash);
    ctx.beginPath(); ctx.ellipse(fx, groundY + 2, Math.max(8, targetX * 0.03 * zoom.x) + 6 * hotFlag.x, 4, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(fx, groundY); ctx.lineTo(fx, groundY - 44); ctx.stroke();
    ctx.fillStyle = hitFlash > 0 ? T.green : T.red;
    const wave = Math.sin(k.t * 5) * 2;
    ctx.beginPath(); ctx.moveTo(fx, groundY - 44); ctx.quadraticCurveTo(fx + 12, groundY - 42 + wave, fx + 24, groundY - 38); ctx.lineTo(fx, groundY - 30); ctx.fill();
    text(ctx, `${fmt(targetX, 1)} m`, fx + 4, groundY - 50, T.ink2, 10, 600);
    if (hitFlash > 0) pill(ctx, 'Hit!', fx, groundY - 70 - (1 - hitFlash) * 20, { color: '#fff', bg: T.green, border: false, size: 13 });

    // current flight: strobe dots and path
    if (np > 1) {
      ctx.strokeStyle = withAlpha(T.orange, 0.85); ctx.lineWidth = 2.2; ctx.beginPath();
      for (let i = 0; i < np; i++) { const X = SX(px[i]), Y = SY(py[i]); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }
      ctx.stroke();
      const tEnd = flying ? tFly : result.T;
      for (let t = 0.2; t < tEnd; t += 0.2) {
        const X = SX(stroboX(t)), Y = SY(stroboY(t));
        ctx.beginPath(); ctx.arc(X, Y, 3.2, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = T.orange; ctx.lineWidth = 1.5; ctx.stroke();
        if (!k.small && Math.abs(t * 5 - Math.round(t * 5)) < 1e-6 && Math.round(t * 5) % 5 === 0) {
          dashedTick(ctx, X, Y);
        }
      }
      const bx = SX(flying ? s[0] : px[np - 1]), by = SY(flying ? s[1] : py[np - 1]);
      if (apexH > 0.5) {
        const ai = apexIndex();
        if (ai >= 0) pill(ctx, `H = ${fmt(apexH, 1)} m`, SX(px[ai]), SY(py[ai]) - 18, { size: 10, color: T.ink2 });
      }
      softShadow(ctx, bx, groundY + 1, 9, 3, 0.25);
      sphere(ctx, bx, by, 7, '#334155');
      if (flying) {
        const sc = 2.2;
        arrow(ctx, bx, by, bx + s[2] * sc, by, T.blue, 2);
        arrow(ctx, bx, by, bx, by - s[3] * sc, T.green, 2);
        if (!k.small) { text(ctx, 'vx', bx + s[2] * sc + 4, by + 4, T.blue, 10, 700); text(ctx, 'vy', bx + 4, by - s[3] * sc - 4, T.green, 10, 700); }
      }
    }

    // cannon
    const cx = SX(0), cy = SY(0) - 4;
    const rb = barrel() + recoil.x * 0.04;
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-ang);
    ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.roundRect(-14 + recoil.x * 0.04, -9, rb + 14, 18, [9, 5, 5, 9]); ctx.fill();
    ctx.fillStyle = '#475569'; ctx.fillRect(rb - 10 + recoil.x * 0.04, -10.5, 10, 21);
    ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(-6, -7, rb, 4);
    ctx.restore();
    ctx.fillStyle = T.woodDark; ctx.beginPath(); ctx.arc(cx, cy, 15, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#5c3a1a'; ctx.lineWidth = 2; ctx.beginPath();
    for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3 + 0.3; ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(a) * 14, cy + Math.sin(a) * 14); }
    ctx.stroke();
    ctx.beginPath(); ctx.arc(cx, cy, 4, 0, Math.PI * 2); ctx.fillStyle = '#1e293b'; ctx.fill();
    // aim handle + angle arc
    const mx = cx + Math.cos(ang) * (rb + 6), my = cy - Math.sin(ang) * (rb + 6);
    ctx.strokeStyle = withAlpha(T.blue, 0.35); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(cx, cy, 30, -ang, 0); ctx.stroke();
    text(ctx, `${Math.round(ang / DEG)}°`, cx + 34, cy - 6, T.blue, 11, 700);
    if (!flying) knob(ctx, mx, my, 8, T.blue, hotAim.x);
    if (k.active === aim) pill(ctx, `${fmt(v0, 1)} m/s at ${Math.round(ang / DEG)}°`, mx, my - 24, { color: T.blue });

    const R0 = idealRange(v0, ang), H0 = v0 * v0 * Math.sin(ang) ** 2 / (2 * g), T0 = 2 * v0 * Math.sin(ang) / g;
    st.R.set(result ? `${fmt(result.R, 1)} m` : '—');
    st.H.set(result ? `${fmt(result.H, 1)} m` : '—');
    st.T.set(result ? `${fmt(result.T, 2)} s` : flying ? `${fmt(tFly, 2)} s` : '—');
    st.th.set(`${fmt(R0, 1)} m · ${fmt(H0, 1)} m · ${fmt(T0, 2)} s`);
    badge.set(flying ? `t = ${fmt(tFly, 2)} s · x = ${fmt(s[0], 1)} m · y = ${fmt(s[1], 1)} m` : result ? `Landed at ${fmt(result.R, 1)} m after ${fmt(result.T, 2)} s` : 'Drag the muzzle to aim, then fire');
    k.animate(flying || zoom.moving || recoil.moving || hotAim.moving || hotFlag.moving || hitFlash > 0);
  });

  function apexIndex() { let bi = -1, by = -1; for (let i = 0; i < np; i++) if (py[i] > by) { by = py[i]; bi = i; } return bi; }
  function stroboX(t) { return sample(px, t); }
  function stroboY(t) { return sample(py, t); }
  function sample(arr, t) {
    if (!launchAir) return arr === px ? launchV * Math.cos(launchA) * t : launchV * Math.sin(launchA) * t - 0.5 * g * t * t;
    const tEnd = flying ? tFly : result.T, f = clamp(t / tEnd, 0, 1) * (np - 1), i = Math.floor(f);
    return i >= np - 1 ? arr[np - 1] : arr[i] + (arr[i + 1] - arr[i]) * (f - i);
  }
  function dashedTick(ctx, X, Y) { dashed(ctx, X, Y, X, groundY, withAlpha(T.orange, 0.3), 1, DOTS); }
  function niceStepM(raw) { const p = Math.pow(10, Math.floor(Math.log10(raw))); const m = raw / p; return (m < 2 ? 2 : m < 5 ? 5 : 10) * p / (m < 2 ? 1 : 1); }
  k.debug = { muzzle: () => [SX(0) + Math.cos(ang) * (barrel() + 6), SY(0) - Math.sin(ang) * (barrel() + 6)], cannon: () => [SX(0), SY(0)], result: () => result, fire };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
