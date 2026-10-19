/**
 * Pushes and pulls — grab the box and pull it like a rope (the pull grows with the stretch), or
 * hold the push buttons. Newton's second law with static and sliding friction (μs > μk) on four
 * surfaces: a box at rest only moves once the push beats μs·m·g, and friction always opposes the
 * motion. Force, friction, net force and velocity are drawn as arrows to scale, with a free-body card.
 */
import { createKit, T, Spring, Ring, fmt, clamp, background, text, pill, arrow, softShadow, withAlpha, card } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SURFACES = [
  { value: 'ice', label: 'Ice', ms: 0.05, mk: 0.03, top: '#dff3ff', base: '#bfe3f7', line: '#9fd0ee' },
  { value: 'wood', label: 'Wood', ms: 0.4, mk: 0.3, top: '#e2bb88', base: '#c9995f', line: '#b07e45' },
  { value: 'carpet', label: 'Carpet', ms: 0.7, mk: 0.55, top: '#c8a2d6', base: '#a77fb8', line: '#8f68a0' },
  { value: 'grass', label: 'Grass', ms: 0.9, mk: 0.7, top: '#9ccc7d', base: '#7fb35f', line: '#6a9c4d' },
];
const LOADS = [
  { value: '10', label: 'Small box · 10 kg', m: 10, size: 0.5, color: '#f3b341' },
  { value: '40', label: 'Crate · 40 kg', m: 40, size: 0.8, color: '#d08a3c' },
  { value: '100', label: 'Fridge · 100 kg', m: 100, size: 1.1, color: '#e9eef5' },
];
const G = 9.81;

export default function init(stage) {
  const k = createKit(stage, { label: 'A box on the ground; grab it to pull, or hold the push buttons' });
  const hud = createHud(stage);
  const badge = hud.badge('Grab the box and pull', T.blue);

  let surf = SURFACES[1], load = LOADS[1], frictionOn = true, pushSet = 200;
  let x = 0, v = 0, Fapp = 0, Ff = 0, held = false, grabX = 0, btnDir = 0, simT = 0;
  const cam = new Spring(0, 60, 15);
  const face = new Spring(0, 120, 14);
  const wobble = new Spring(0, 220, 9);
  const trace = new Ring(400);
  const plot = new Plot({ title: 'Speed', xLabel: 't / s', yLabel: 'm/s', yMin: 0, yMax: 4 });

  const panel = createPanel(stage, { title: 'Pushes and pulls' });
  panel.chips({ label: 'Surface', options: SURFACES.map((s) => ({ value: s.value, label: s.label, color: s.base })), value: surf.value, onChange: (val) => { surf = SURFACES.find((s) => s.value === val); k.invalidate(); } });
  panel.chips({ label: 'What to push', options: LOADS.map((l) => ({ value: l.value, label: l.label, color: l.color })), value: load.value, onChange: (val) => { load = LOADS.find((l) => l.value === val); k.invalidate(); } });
  panel.slider({ label: 'Button push strength', min: 20, max: 600, step: 10, value: pushSet, format: (val) => `${val} N`, onChange: (val) => { pushSet = val; } });
  panel.toggle({ label: 'Friction', value: true, onChange: (val) => { frictionOn = val; k.animate(true); } });
  panel.button({ label: 'Back to start', icon: 'replay', variant: 'ghost', onClick: () => { x = 0; v = 0; simT = 0; trace.clear(); k.animate(true); } });
  const st = panel.stats([{ key: 'F', label: 'Your push' }, { key: 'f', label: 'Friction' }, { key: 'a', label: 'Acceleration' }, { key: 'v', label: 'Speed' }]);
  panel.info('A box at rest stays put until your push beats the grip of the surface (μs·m·g). Once it slides, friction is a little smaller. With friction off, one shove keeps it gliding forever.');

  let groundY = 0, scale = 120, W = 0, H = 0;
  k.onResize((w, h) => { W = w; H = h; groundY = h - (k.small ? 92 : 104); scale = Math.min(150, w / 7.5); plot.box(w - (k.small ? 0 : 238), 50, 224, 130); });
  const boxPx = () => load.size * scale;
  const SX = (m) => W * 0.42 + (m - cam.x) * scale;

  const boxH = k.drag({
    hit: (px, py, s) => { const bx = SX(x), b = boxPx(); return px > bx - b / 2 - s && px < bx + b / 2 + s && py > groundY - b - s && py < groundY + 4 ? Math.abs(px - bx) : false; },
    down: (px) => { held = true; grabX = (px - SX(x)) / scale; k.animate(true); },
    move: () => {},
    up: () => { held = false; },
  });
  const btnL = k.drag({ hit: (px, py, s) => (Math.hypot(px - 46, py - (H - 40)) < 30 + s ? 1 : false), down: () => { btnDir = -1; k.animate(true); }, up: () => { btnDir = 0; }, cursor: 'pointer', cursorActive: 'pointer' });
  const btnR = k.drag({ hit: (px, py, s) => (Math.hypot(px - (W - 46), py - (H - 40)) < 30 + s ? 1 : false), down: () => { btnDir = 1; k.animate(true); }, up: () => { btnDir = 0; }, cursor: 'pointer', cursorActive: 'pointer' });

  function physics(dt) {
    const m = load.m;
    if (held) {
      const stretch = k.pointer.x - (SX(x) + grabX * scale);
      Fapp = clamp(stretch * 3, -600, 600);
    } else Fapp = btnDir * pushSet;
    const n = Math.max(1, Math.ceil(dt / 0.004)), h = dt / n;
    for (let i = 0; i < n; i++) {
      const N = m * G;
      if (!frictionOn) Ff = 0;
      else if (Math.abs(v) < 1e-4) {
        Ff = Math.abs(Fapp) <= surf.ms * N ? -Fapp : -Math.sign(Fapp) * surf.mk * N;
        if (Math.abs(Fapp) <= surf.ms * N) v = 0;
      } else Ff = -Math.sign(v) * surf.mk * N;
      const a = (Fapp + Ff) / m;
      const nv = v + a * h;
      if (frictionOn && v !== 0 && Math.sign(nv) !== Math.sign(v) && Math.abs(Fapp) <= surf.ms * N) v = 0; else v = nv;
      x += v * h;
    }
    simT += dt;
    trace.push(simT, Math.abs(v));
  }

  k.frame((ctx, dt, w, h) => {
    physics(dt);
    cam.to(x); cam.step(dt);
    const a = (Fapp + Ff) / load.m;
    face.to(clamp(Math.abs(Fapp) / 300, 0, 1)); face.step(dt);
    wobble.step(dt);
    background(k, ctx, w, h, '#eef5ff', '#f8fbff');
    // background: fence and trees that scroll slower (parallax)
    const par = cam.x * scale * 0.4;
    ctx.fillStyle = '#e3edf8';
    for (let i = -2; i < w / 160 + 3; i++) { const bx = ((i * 160 - par) % (w + 320) + w + 320) % (w + 320) - 160; ctx.beginPath(); ctx.arc(bx - 22, groundY - 20, 24, 0, Math.PI * 2); ctx.arc(bx + 4, groundY - 34, 30, 0, Math.PI * 2); ctx.arc(bx + 32, groundY - 18, 22, 0, Math.PI * 2); ctx.fill(); }
    ctx.strokeStyle = '#d3dcea'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, groundY - 30); ctx.lineTo(w, groundY - 30); ctx.stroke();
    // ground
    ctx.fillStyle = surf.top; ctx.fillRect(0, groundY, w, 8);
    ctx.fillStyle = surf.base; ctx.fillRect(0, groundY + 8, w, h - groundY);
    ctx.strokeStyle = surf.line; ctx.lineWidth = 1; ctx.beginPath();
    for (let m = Math.floor(cam.x - 6); m < cam.x + 8; m++) { const px = SX(m); ctx.moveTo(px, groundY); ctx.lineTo(px, groundY + (m % 5 === 0 ? 16 : 9)); }
    ctx.stroke();
    for (let m = Math.ceil((cam.x - 6) / 5) * 5; m < cam.x + 8; m += 5) text(ctx, `${m} m`, SX(m), groundY + 30, withAlpha('#172033', 0.55), 10, 600, 'center');

    // box
    const b = boxPx(), bx = SX(x);
    wobble.to(clamp(-a * 0.006, -0.06, 0.06));
    softShadow(ctx, bx, groundY + 2, b * 0.62, 6, 0.28);
    ctx.save(); ctx.translate(bx, groundY); ctx.rotate(wobble.x);
    if (load.m === 100) {
      ctx.fillStyle = '#f4f7fb'; ctx.strokeStyle = '#b8c3d3'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.roundRect(-b * 0.36, -b * 1.25, b * 0.72, b * 1.25, 8); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(-b * 0.36, -b * 0.82); ctx.lineTo(b * 0.36, -b * 0.82); ctx.stroke();
      ctx.fillStyle = '#9aa8bd'; ctx.fillRect(b * 0.24, -b * 1.12, 4, b * 0.22); ctx.fillRect(b * 0.24, -b * 0.72, 4, b * 0.3);
      drawFace(ctx, 0, -b * 1.0, b * 0.5);
    } else {
      ctx.fillStyle = load.color; ctx.strokeStyle = '#8d5a2b'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.roundRect(-b / 2, -b, b, b, 6); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = 'rgba(141,90,43,0.45)'; ctx.lineWidth = 1.5; ctx.beginPath();
      ctx.moveTo(-b / 2 + 6, -b + 6); ctx.lineTo(b / 2 - 6, -6); ctx.moveTo(b / 2 - 6, -b + 6); ctx.lineTo(-b / 2 + 6, -6); ctx.stroke();
      drawFace(ctx, 0, -b * 0.52, b * 0.8);
    }
    ctx.restore();
    text(ctx, `${load.m} kg`, bx, groundY - (load.m === 100 ? b * 1.25 : b) - 8, T.ink2, 10.5, 700, 'center');

    // rope / hand
    if (held) {
      const side = Math.sign(Fapp) || 1, ax = bx + side * (load.m === 100 ? b * 0.36 : b / 2), ay = groundY - b * 0.5;
      const hx = ax + side * 14 + Fapp / 3;
      ctx.strokeStyle = '#7c5a32'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(hx, ay); ctx.stroke();
      ctx.beginPath(); ctx.arc(hx, ay, 9, 0, Math.PI * 2); ctx.fillStyle = '#f2c79a'; ctx.fill(); ctx.strokeStyle = '#c99868'; ctx.lineWidth = 1.5; ctx.stroke();
    }
    // arrows, to scale: 100 N = 40 px
    const fs = 0.4 * (k.small ? 0.7 : 1);
    const ay = groundY - b - 34;
    if (Math.abs(Fapp) > 1) { arrow(ctx, bx, ay, bx + Fapp * fs, ay, T.blue, 5); pill(ctx, `push ${fmt(Math.abs(Fapp), 0)} N`, bx + Fapp * fs, ay - 16, { color: T.blue, size: 10.5 }); }
    if (Math.abs(Ff) > 1) { arrow(ctx, bx, groundY - 6, bx + Ff * fs, groundY - 6, T.red, 4); pill(ctx, `friction ${fmt(Math.abs(Ff), 0)} N`, bx + Ff * fs, groundY + 46, { color: T.red, size: 10.5 }); }
    if (Math.abs(v) > 0.02) { arrow(ctx, bx, ay - 34, bx + v * 40, ay - 34, T.green, 3); pill(ctx, `${fmt(Math.abs(v), 2)} m/s`, bx + v * 40 + Math.sign(v) * 34, ay - 34, { color: T.green, size: 10 }); }

    // push buttons
    pushButton(ctx, 46, h - 40, -1, btnDir === -1 || k.isHot(btnL));
    pushButton(ctx, w - 46, h - 40, 1, btnDir === 1 || k.isHot(btnR));

    // free-body card
    if (!k.small) {
      const cx = 14, cy = 50, cw = 200, ch = 150;
      card(ctx, cx, cy, cw, ch, 12);
      text(ctx, 'Free-body diagram', cx + 12, cy + 20, T.ink, 11.5, 700);
      const ox = cx + cw / 2, oy = cy + 76;
      ctx.fillStyle = withAlpha(load.color === '#e9eef5' ? '#9aa8bd' : load.color, 0.9); ctx.fillRect(ox - 12, oy - 12, 24, 24);
      const sc = 30 / Math.max(load.m * G, 300);
      arrow(ctx, ox, oy, ox, oy + load.m * G * sc + 12, T.slate, 2); text(ctx, 'W', ox + 6, oy + load.m * G * sc + 12, T.slate, 10, 700);
      arrow(ctx, ox, oy, ox, oy - load.m * G * sc - 12, T.slate, 2); text(ctx, 'N', ox + 6, oy - load.m * G * sc - 6, T.slate, 10, 700);
      if (Math.abs(Fapp) > 1) arrow(ctx, ox, oy, ox + clamp(Fapp * sc, -80, 80) + Math.sign(Fapp) * 12, oy, T.blue, 2.5);
      if (Math.abs(Ff) > 1) arrow(ctx, ox, oy + 6, ox + clamp(Ff * sc, -80, 80) + Math.sign(Ff) * 12, oy + 6, T.red, 2.5);
      text(ctx, `net ${fmt(Fapp + Ff, 0)} N → a = ${fmt(a, 2)} m/s²`, cx + 12, cy + ch - 10, T.purple, 10, 600);
      const span = 10, t1 = Math.max(span, simT);
      plot.range(t1 - span, t1, 0, Math.max(2, Math.ceil(Math.max(Math.abs(v), 1) + 1))).frame(ctx);
      plot.clip(ctx); plot.ring(ctx, trace, T.green, 2); plot.unclip(ctx);
    }

    st.F.set(`${fmt(Math.abs(Fapp), 0)} N`); st.f.set(frictionOn ? `${fmt(Math.abs(Ff), 0)} N` : 'off');
    st.a.set(`${fmt(Math.abs(a), 2)} m/s²`); st.v.set(`${fmt(Math.abs(v), 2)} m/s`);
    const grip = surf.ms * load.m * G;
    badge.set(Math.abs(Fapp) > 0 && v === 0 && frictionOn ? `Stuck! Push more than ${fmt(grip, 0)} N to get it moving` : Math.abs(v) > 0.01 ? (Math.abs(Fapp) > 0 ? 'Speeding up' : frictionOn ? 'Friction is slowing it down' : 'Gliding — nothing to stop it') : 'Grab the box and pull');
    k.animate(held || btnDir !== 0 || Math.abs(v) > 1e-4 || cam.moving || face.moving || wobble.moving);
  });

  function drawFace(ctx, fx, fy, s) {
    const strain = face.x;
    ctx.fillStyle = '#1f2937';
    const ey = fy - s * 0.08, ex = s * 0.16;
    if (strain > 0.5) { ctx.lineWidth = 2.2; ctx.strokeStyle = '#1f2937'; ctx.beginPath(); ctx.moveTo(fx - ex - 4, ey - 3); ctx.lineTo(fx - ex + 4, ey); ctx.lineTo(fx - ex - 4, ey + 3); ctx.moveTo(fx + ex + 4, ey - 3); ctx.lineTo(fx + ex - 4, ey); ctx.lineTo(fx + ex + 4, ey + 3); ctx.stroke(); }
    else { ctx.beginPath(); ctx.arc(fx - ex, ey, 3.2, 0, Math.PI * 2); ctx.arc(fx + ex, ey, 3.2, 0, Math.PI * 2); ctx.fill(); }
    ctx.strokeStyle = '#1f2937'; ctx.lineWidth = 2; ctx.beginPath();
    if (Math.abs(v) > 0.6) { ctx.arc(fx, fy + s * 0.1, s * 0.1, 0, Math.PI * 2); }
    else ctx.arc(fx, fy + s * 0.04 - strain * s * 0.12, s * 0.12, 0.15 * Math.PI + strain * Math.PI, 0.85 * Math.PI + strain * Math.PI, strain > 0.5);
    ctx.stroke();
    ctx.fillStyle = 'rgba(240,120,120,0.35)'; ctx.beginPath(); ctx.arc(fx - ex * 1.9, fy + s * 0.06, 4, 0, Math.PI * 2); ctx.arc(fx + ex * 1.9, fy + s * 0.06, 4, 0, Math.PI * 2); ctx.fill();
  }
  function pushButton(ctx, cx, cy, dir, on) {
    ctx.beginPath(); ctx.arc(cx, cy + 2, 26, 0, Math.PI * 2); ctx.fillStyle = 'rgba(23,40,80,0.15)'; ctx.fill();
    ctx.beginPath(); ctx.arc(cx, cy + (on ? 2 : 0), 26, 0, Math.PI * 2); ctx.fillStyle = on ? T.blueDeep : T.blue; ctx.fill();
    ctx.fillStyle = '#fff'; ctx.beginPath();
    const yy = cy + (on ? 2 : 0);
    ctx.moveTo(cx + dir * 10, yy); ctx.lineTo(cx - dir * 6, yy - 10); ctx.lineTo(cx - dir * 6, yy + 10); ctx.fill();
    text(ctx, dir < 0 ? 'push left' : 'push right', cx, cy - 34, T.ink2, 10, 600, 'center');
  }

  k.debug = { box: () => [SX(x), groundY - boxPx() / 2], x: () => x, v: () => v };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
