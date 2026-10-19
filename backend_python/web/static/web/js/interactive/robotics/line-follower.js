/**
 * Line follower — a two-wheeled robot with infrared sensors on a taped track. Each sensor reads
 * how dark the floor is under its footprint (sampled from the track image itself), and the robot
 * steers by a rule: bang-bang with two sensors (left sees the line → turn left) or proportional
 * steering with three. Wheel speeds lag behind their commands like real motors, so too much speed
 * makes it overshoot and lose the line. Draw your own track with the pen, or drag the robot.
 */
import { createKit, T, Spring, Ring, fmt, clamp, text, pill, withAlpha, softShadow, card } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const TAPE = 18;

export default function init(stage) {
  const k = createKit(stage, { label: 'A robot following a black line on a white floor' });
  const hud = createHud(stage);
  const badge = hud.badge('Press Run, or draw a track with the pen', T.blue);

  let running = false, speed = 90, turn = 70, mode = 'bang', shape = 'oval', drawing = false, pen = false;
  let track = new Float32Array(0), trackN = 0, mask = null, mw = 0, mh = 0;
  const bot = { x: 0, y: 0, a: 0, vl: 0, vr: 0 };
  const sens = new Float32Array(3);
  let lostT = 0, lapT = 0, lastLap = 0, dist = 0;
  const trail = new Ring(400);
  const drawPts = [];

  const panel = createPanel(stage, { title: 'Line follower' });
  const [runB] = panel.buttonRow([
    { label: 'Run', icon: 'play_arrow', onClick: () => { running = !running; runB.setLabel(running ? 'Stop' : 'Run'); k.animate(true); } },
    { label: 'Reset', icon: 'restart_alt', variant: 'ghost', onClick: () => placeBot() },
  ]);
  panel.chips({ label: 'Brain', options: [{ value: 'bang', label: '2 sensors · bang-bang' }, { value: 'prop', label: '3 sensors · proportional' }], value: 'bang', onChange: (v) => { mode = v; } });
  panel.slider({ label: 'Speed', min: 20, max: 220, step: 5, value: speed, format: (v) => `${v} px/s`, onChange: (v) => { speed = v; } });
  panel.slider({ label: 'Turn strength', min: 10, max: 140, step: 5, value: turn, format: (v) => `${v} %`, onChange: (v) => { turn = v; } });
  panel.chips({ label: 'Track', options: [{ value: 'oval', label: 'Oval' }, { value: 'wavy', label: 'Wavy' }, { value: 'eight', label: 'Figure 8' }, { value: 'pen', label: 'Draw my own' }], value: 'oval', onChange: (v) => { if (v === 'pen') { pen = true; badge.set('Draw a closed loop on the floor with your finger or mouse'); } else { pen = false; shape = v; buildTrack(); placeBot(); } } });
  const st = panel.stats([{ key: 'L', label: 'Left sensor' }, { key: 'R', label: 'Right sensor' }, { key: 'lap', label: 'Last lap' }, { key: 'state', label: 'Doing' }]);
  panel.info('Dark tape reflects little infrared light, the white floor reflects a lot. That one reading per sensor is enough: if the left sensor sees the tape, the line is drifting left, so slow the left wheel. Correcting from its own sensors is feedback.');

  function buildTrack() {
    const w = k.w, h = k.h, cx = w / 2, cy = h / 2, rx = w * 0.38, ry = h * 0.36, n = 400;
    track = new Float32Array(n * 2); trackN = n;
    for (let i = 0; i < n; i++) {
      const t = i / n * Math.PI * 2;
      let x, y;
      if (shape === 'eight') { x = cx + rx * Math.sin(t); y = cy + ry * Math.sin(t) * Math.cos(t) * 1.6; }
      else if (shape === 'wavy') { const r = 1 + 0.16 * Math.sin(5 * t); x = cx + rx * r * Math.cos(t); y = cy + ry * r * Math.sin(t); }
      else { x = cx + rx * Math.cos(t); y = cy + ry * Math.sin(t); }
      track[i * 2] = x; track[i * 2 + 1] = y;
    }
    bake();
  }
  function bake() {
    mw = Math.max(1, Math.round(k.w)); mh = Math.max(1, Math.round(k.h));
    const c = document.createElement('canvas'); c.width = mw; c.height = mh;
    const g = c.getContext('2d');
    g.lineWidth = TAPE; g.lineJoin = 'round'; g.lineCap = 'round'; g.strokeStyle = '#000';
    g.beginPath(); for (let i = 0; i < trackN; i++) { const x = track[i * 2], y = track[i * 2 + 1]; if (i) g.lineTo(x, y); else g.moveTo(x, y); } g.closePath(); g.stroke();
    mask = g.getImageData(0, 0, mw, mh).data;
    trail.clear(); k.invalidate();
  }
  function placeBot() {
    if (!trackN) return;
    bot.x = track[0]; bot.y = track[1];
    bot.a = Math.atan2(track[3] - track[1], track[2] - track[0]);
    bot.vl = bot.vr = 0; lostT = 0; lapT = 0; dist = 0; trail.clear(); k.animate(true);
  }
  function dark(x, y) {
    let s = 0;
    for (let dy = -3; dy <= 3; dy += 3) for (let dx = -3; dx <= 3; dx += 3) {
      const px = (x + dx) | 0, py = (y + dy) | 0;
      if (px >= 0 && py >= 0 && px < mw && py < mh) s += mask[(py * mw + px) * 4 + 3] / 255;
    }
    return s / 9;
  }
  const SX = [-11, 0, 11];
  function sensorPos(i, out) { const fx = 26, ca = Math.cos(bot.a), sa = Math.sin(bot.a); out[0] = bot.x + ca * fx - sa * SX[i]; out[1] = bot.y + sa * fx + ca * SX[i]; return out; }
  const SP = new Float32Array(2);

  k.onResize(() => { buildTrack(); placeBot(); });

  const botH = k.drag({
    enabled: () => !pen,
    hit: (x, y, s) => { const d = Math.hypot(x - bot.x, y - bot.y); return d < 26 + s ? d : false; },
    down: () => { running = false; runB.setLabel('Run'); },
    move: (x, y) => { const dx = x - bot.x, dy = y - bot.y; if (Math.hypot(dx, dy) > 2) bot.a = bot.a + clamp(Math.atan2(Math.sin(Math.atan2(dy, dx) - bot.a), Math.cos(Math.atan2(dy, dx) - bot.a)), -0.15, 0.15); bot.x = x; bot.y = y; trail.clear(); },
  });
  k.drag({
    enabled: () => pen,
    hit: () => 1,
    down: (x, y) => { drawPts.length = 0; drawPts.push(x, y); drawing = true; running = false; runB.setLabel('Run'); },
    move: (x, y) => { const n = drawPts.length; if (Math.hypot(x - drawPts[n - 2], y - drawPts[n - 1]) > 6) drawPts.push(x, y); },
    up: () => {
      drawing = false;
      if (drawPts.length > 40) {
        trackN = drawPts.length / 2; track = new Float32Array(drawPts);
        for (let it = 0; it < 3; it++) { const c = new Float32Array(track); for (let i = 0; i < trackN; i++) { const a = (i - 1 + trackN) % trackN, b = (i + 1) % trackN; track[i * 2] = (c[a * 2] + 2 * c[i * 2] + c[b * 2]) / 4; track[i * 2 + 1] = (c[a * 2 + 1] + 2 * c[i * 2 + 1] + c[b * 2 + 1]) / 4; } }
        bake(); placeBot(); pen = false; badge.set('Your track! Press Run');
      }
    },
    cursor: 'crosshair', cursorActive: 'crosshair',
  });

  k.frame((ctx, dt, w, h) => {
    for (let i = 0; i < 3; i++) { sensorPos(i, SP); sens[i] = dark(SP[0], SP[1]); }
    let doing = 'stopped';
    if (running) {
      let cl = speed, cr = speed;
      const L = mode === 'bang' ? sens[0] > 0.4 : 0, R = mode === 'bang' ? sens[2] > 0.4 : 0;
      if (mode === 'bang') {
        if (L && !R) { cl = speed * (1 - turn / 100); doing = 'line on the left: turn left'; }
        else if (R && !L) { cr = speed * (1 - turn / 100); doing = 'line on the right: turn right'; }
        else if (!L && !R) doing = 'line between sensors: straight';
        else doing = 'both on the line: straight';
      } else {
        const tot = sens[0] + sens[1] + sens[2];
        const err = tot > 0.05 ? (sens[2] - sens[0]) / tot : 0;
        cl = speed * (1 + err * turn / 100); cr = speed * (1 - err * turn / 100);
        doing = tot < 0.05 ? 'lost: going straight' : `error ${fmt(err, 2)}: steer ${err < -0.05 ? 'left' : err > 0.05 ? 'right' : 'straight'}`;
      }
      const tau = 0.12, f = 1 - Math.exp(-dt / tau);
      bot.vl += (cl - bot.vl) * f; bot.vr += (cr - bot.vr) * f;
      const v = (bot.vl + bot.vr) / 2, om = (bot.vl - bot.vr) / 30;
      bot.a += om * dt; bot.x += Math.cos(bot.a) * v * dt; bot.y += Math.sin(bot.a) * v * dt;
      bot.x = clamp(bot.x, 10, w - 10); bot.y = clamp(bot.y, 10, h - 10);
      dist += v * dt; lapT += dt;
      if (Math.hypot(bot.x - track[0], bot.y - track[1]) < 14 && lapT > 3) { lastLap = lapT; lapT = 0; }
      const onAny = sens[0] + sens[1] + sens[2] > 0.1;
      lostT = onAny ? 0 : lostT + dt;
      if (lostT > 1.2) { running = false; runB.setLabel('Run'); badge.set('Lost the line! Slow down or turn harder'); }
      trail.push(bot.x, bot.y);
    }
    // floor
    ctx.fillStyle = '#f4f1ea'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(0,0,0,0.04)'; ctx.lineWidth = 1; ctx.beginPath();
    for (let x = 0; x < w; x += 60) { ctx.moveTo(x, 0); ctx.lineTo(x, h); } for (let y = 0; y < h; y += 60) { ctx.moveTo(0, y); ctx.lineTo(w, y); } ctx.stroke();
    // tape
    ctx.strokeStyle = '#1b1d22'; ctx.lineWidth = TAPE; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.beginPath(); for (let i = 0; i < trackN; i++) { const x = track[i * 2], y = track[i * 2 + 1]; if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y); } ctx.closePath(); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,0.08)'; ctx.lineWidth = 2; ctx.stroke();
    if (drawing || (pen && drawPts.length)) { ctx.strokeStyle = withAlpha(T.blue, 0.7); ctx.lineWidth = TAPE * 0.6; ctx.beginPath(); for (let i = 0; i < drawPts.length; i += 2) { if (i) ctx.lineTo(drawPts[i], drawPts[i + 1]); else ctx.moveTo(drawPts[i], drawPts[i + 1]); } ctx.stroke(); }
    // trail
    ctx.strokeStyle = withAlpha(T.orange, 0.5); ctx.lineWidth = 2; ctx.beginPath();
    for (let i = 0; i < trail.n; i++) { const j = trail.idx(i); if (i) ctx.lineTo(trail.x[j], trail.y[j]); else ctx.moveTo(trail.x[j], trail.y[j]); }
    ctx.stroke();
    // robot
    softShadow(ctx, bot.x + 2, bot.y + 4, 30, 24, 0.25);
    ctx.save(); ctx.translate(bot.x, bot.y); ctx.rotate(bot.a);
    ctx.fillStyle = '#334155'; ctx.fillRect(-12, -24, 20, 7); ctx.fillRect(-12, 17, 20, 7);
    ctx.fillStyle = k.isHot(botH) ? '#3b82f6' : '#2563eb'; ctx.beginPath(); ctx.roundRect(-20, -17, 50, 34, 9); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fillRect(-14, -13, 34, 5);
    ctx.fillStyle = '#0f172a'; ctx.fillRect(22, -16, 8, 32);
    ctx.restore();
    for (let i = 0; i < 3; i++) {
      if (mode === 'bang' && i === 1) continue;
      sensorPos(i, SP);
      const on = sens[i] > 0.4;
      ctx.beginPath(); ctx.arc(SP[0], SP[1], 5, 0, Math.PI * 2); ctx.fillStyle = on ? '#ef4444' : '#fde68a'; ctx.fill(); ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 1.2; ctx.stroke();
      if (running && on) { ctx.beginPath(); ctx.arc(SP[0], SP[1], 9, 0, Math.PI * 2); ctx.strokeStyle = 'rgba(239,68,68,0.4)'; ctx.stroke(); }
    }
    // sensor/motor panel
    if (!k.small) {
      const cx = w - 190, cy = 14;
      card(ctx, cx, cy, 176, 112, 12);
      text(ctx, 'Sensors (darkness)', cx + 12, cy + 20, T.ink, 11, 700);
      const names = ['L', 'M', 'R'];
      for (let i = 0; i < 3; i++) { if (mode === 'bang' && i === 1) continue; const bx = cx + 14 + i * 52; ctx.fillStyle = T.line2; ctx.fillRect(bx, cy + 30, 36, 8); ctx.fillStyle = sens[i] > 0.4 ? T.red : T.amber; ctx.fillRect(bx, cy + 30, 36 * sens[i], 8); text(ctx, names[i], bx + 18, cy + 52, T.ink2, 10, 700, 'center'); }
      text(ctx, 'Wheel speeds', cx + 12, cy + 74, T.ink, 11, 700);
      ctx.fillStyle = T.green; ctx.fillRect(cx + 14, cy + 82, 70 * clamp(bot.vl / 220, 0, 1), 8); ctx.fillRect(cx + 92, cy + 82, 70 * clamp(bot.vr / 220, 0, 1), 8);
      text(ctx, 'left', cx + 14, cy + 104, T.ink2, 9.5, 600); text(ctx, 'right', cx + 92, cy + 104, T.ink2, 9.5, 600);
    }
    if (pen && !drawing && drawPts.length === 0) pill(ctx, 'Draw a closed loop', w / 2, h / 2, { color: T.blue, size: 13 });
    st.L.set(sens[0] > 0.4 ? 'ON the line' : 'off'); st.R.set(sens[2] > 0.4 ? 'ON the line' : 'off');
    st.lap.set(lastLap ? `${fmt(lastLap, 2)} s` : '—'); st.state.set(doing);
    if (running) badge.set(doing);
    k.animate(running || drawing);
  });

  k.debug = { bot: () => [bot.x, bot.y], run: () => { running = true; runB.setLabel('Stop'); k.animate(true); }, state: () => ({ x: bot.x, y: bot.y, lost: lostT, lap: lastLap, running }), pen: () => { pen = true; } };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
