/**
 * Logic and state machines — a robot vacuum run by a finite state machine. Each state has one
 * job (SEARCH drives and cleans, BACKUP reverses after a bump, TURN picks a new heading, DOCK
 * steers home on a low battery, CHARGE waits on the dock) and events move it between them. The
 * live diagram lights the current state and flashes each transition as it fires. Drag the
 * furniture or the robot, or fire the events yourself.
 */
import { createKit, T, Spring, fmt, clamp, text, pill, withAlpha, softShadow, card, arrow } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const STATES = ['SEARCH', 'BACKUP', 'TURN', 'DOCK', 'CHARGE'];
const SCOL = { SEARCH: '#2563eb', BACKUP: '#f08c00', TURN: '#7c3aed', DOCK: '#0d9488', CHARGE: '#16a34a' };
const EDGES = [
  ['SEARCH', 'BACKUP', 'bump'], ['BACKUP', 'TURN', 'timer done'], ['TURN', 'SEARCH', 'turn done'],
  ['SEARCH', 'DOCK', 'battery low'], ['BACKUP', 'DOCK', 'battery low'], ['TURN', 'DOCK', 'battery low'],
  ['DOCK', 'BACKUP', 'bump'], ['DOCK', 'CHARGE', 'docked'], ['CHARGE', 'SEARCH', 'battery full'],
];
const GX = 40, GY = 26;

export default function init(stage) {
  const k = createKit(stage, { label: 'A robot vacuum in a room and its live state diagram' });
  const hud = createHud(stage);
  const badge = hud.badge('State: SEARCH', SCOL.SEARCH);

  let state = 'SEARCH', timer = 0, turnLeft = 0, battery = 100, running = true, speedMul = 1, dockEnabled = true, prevState = 'SEARCH';
  const bot = { x: 0, y: 0, a: 0.4 };
  const furn = [];
  const dirt = new Uint8Array(GX * GY);
  let dirtLeft = 0, dirtTotal = 0;
  const log = [];
  const glowS = {}; STATES.forEach((s) => { glowS[s] = new Spring(s === 'SEARCH' ? 1 : 0, 120, 14); });
  const flash = EDGES.map(() => 0);

  const panel = createPanel(stage, { title: 'State machine' });
  const [runB] = panel.buttonRow([{ label: 'Pause', icon: 'pause', variant: 'ghost', onClick: () => { running = !running; runB.setLabel(running ? 'Pause' : 'Run'); k.animate(true); } }, { label: 'New room', icon: 'restart_alt', variant: 'ghost', onClick: () => { layoutRoom(); } }]);
  panel.slider({ label: 'Speed', min: 0.5, max: 3, step: 0.25, value: 1, format: (v) => `${v}×`, onChange: (v) => { speedMul = v; } });
  panel.toggle({ label: 'DOCK state enabled', value: true, onChange: (v) => { dockEnabled = v; } });
  panel.buttonRow([{ label: 'Battery low', icon: 'battery_alert', onClick: () => { battery = Math.min(battery, 19); } }, { label: 'Bump!', icon: 'touch_app', onClick: () => fire('bump') }]);
  const st = panel.stats([{ key: 'state', label: 'State' }, { key: 'bat', label: 'Battery' }, { key: 'clean', label: 'Floor cleaned' }, { key: 'last', label: 'Last event' }]);
  panel.info('In a state machine the robot is always in exactly one state, and only the listed events can move it. To know what "battery low" does you read one arrow, not a tangle of if-else. Without the DOCK state, the battery simply runs flat.');

  function fire(ev) {
    for (let i = 0; i < EDGES.length; i++) {
      const [a, b, e] = EDGES[i];
      if (a === state && e === ev) {
        if (b === 'DOCK' && !dockEnabled) return;
        prevState = state; state = b; flash[i] = 1; timer = 0;
        if (b === 'TURN') turnLeft = (Math.random() < 0.5 ? -1 : 1) * (0.6 + Math.random() * 1.8);
        log.unshift(`${a} —${ev}→ ${b}`); if (log.length > 5) log.pop();
        k.animate(true);
        return true;
      }
    }
    return false;
  }

  let room = { x: 0, y: 0, w: 0, h: 0 }, dock = { x: 0, y: 0 }, R = 14, dg = { x: 0, y: 0, w: 0, h: 0 };
  function layoutRoom() {
    furn.length = 0;
    const r = room;
    furn.push({ x: r.x + r.w * 0.18, y: r.y + r.h * 0.2, w: r.w * 0.2, h: r.h * 0.14, c: '#c08a55', name: 'sofa' });
    furn.push({ x: r.x + r.w * 0.55, y: r.y + r.h * 0.5, w: r.w * 0.14, h: r.h * 0.22, c: '#94a3b8', name: 'table' });
    furn.push({ x: r.x + r.w * 0.2, y: r.y + r.h * 0.66, w: r.w * 0.1, h: r.h * 0.1, c: '#a78bfa', name: 'box' });
    dock.x = r.x + r.w - 26; dock.y = r.y + r.h - 26;
    bot.x = r.x + r.w * 0.5; bot.y = r.y + r.h * 0.3; bot.a = 0.5; battery = 100; state = 'SEARCH';
    dirtTotal = 0;
    for (let j = 0; j < GY; j++) for (let i = 0; i < GX; i++) { const px = r.x + (i + 0.5) * r.w / GX, py = r.y + (j + 0.5) * r.h / GY; const d = inFurn(px, py, 0) ? 0 : Math.random() < 0.55 ? 1 : 0; dirt[j * GX + i] = d; dirtTotal += d; }
    dirtLeft = dirtTotal; log.length = 0; k.animate(true);
  }
  function inFurn(px, py, pad) { for (const f of furn) if (px > f.x - pad && px < f.x + f.w + pad && py > f.y - pad && py < f.y + f.h + pad) return f; return null; }

  k.onResize((w, h) => {
    if (k.small) { room = { x: 10, y: 44, w: w - 20, h: h * 0.48 }; dg = { x: 10, y: 44 + h * 0.48 + 10, w: w - 20, h: h - h * 0.48 - 64 }; }
    else { room = { x: 16, y: 50, w: w * 0.56, h: h - 70 }; dg = { x: w * 0.56 + 32, y: 50, w: w * 0.44 - 48, h: h - 70 }; }
    R = k.small ? 10 : 14;
    layoutRoom();
  });

  let dragF = null, dfx = 0, dfy = 0;
  k.drag({
    hit: (x, y, s) => (inFurn(x, y, s) ? 1 : false),
    down: (x, y) => { dragF = inFurn(x, y, 30); dfx = x - dragF.x; dfy = y - dragF.y; },
    move: (x, y) => { if (!dragF) return; dragF.x = clamp(x - dfx, room.x, room.x + room.w - dragF.w); dragF.y = clamp(y - dfy, room.y, room.y + room.h - dragF.h); },
    up: () => { dragF = null; },
  });
  k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - bot.x, y - bot.y); return d < R + 6 + s ? d * 0.5 : false; },
    move: (x, y) => { bot.x = clamp(x, room.x + R, room.x + room.w - R); bot.y = clamp(y, room.y + R, room.y + room.h - R); },
  });

  function blocked(nx, ny) {
    if (nx < room.x + R || nx > room.x + room.w - R || ny < room.y + R || ny > room.y + room.h - R) return true;
    for (const f of furn) { const cx = clamp(nx, f.x, f.x + f.w), cy = clamp(ny, f.y, f.y + f.h); if (Math.hypot(nx - cx, ny - cy) < R) return true; }
    return false;
  }

  function stepFSM(dt) {
    const v = 70 * (k.small ? 0.7 : 1);
    if (state !== 'CHARGE') battery = Math.max(0, battery - dt * 2.2);
    if (battery <= 0) { badge.set('Battery flat! The robot stopped (no DOCK state).'); return; }
    if (battery < 20 && (state === 'SEARCH' || state === 'BACKUP' || state === 'TURN') && dockEnabled) fire('battery low');
    timer += dt;
    if (state === 'SEARCH' || state === 'DOCK') {
      if (state === 'DOCK') { const ta = Math.atan2(dock.y - bot.y, dock.x - bot.x); let da = Math.atan2(Math.sin(ta - bot.a), Math.cos(ta - bot.a)); bot.a += clamp(da, -2.5 * dt, 2.5 * dt); if (Math.hypot(dock.x - bot.x, dock.y - bot.y) < 8) { fire('docked'); return; } }
      else bot.a += (Math.random() - 0.5) * 0.6 * dt;
      const nx = bot.x + Math.cos(bot.a) * v * dt, ny = bot.y + Math.sin(bot.a) * v * dt;
      if (blocked(nx, ny)) fire('bump'); else { bot.x = nx; bot.y = ny; }
    } else if (state === 'BACKUP') {
      const nx = bot.x - Math.cos(bot.a) * v * 0.6 * dt, ny = bot.y - Math.sin(bot.a) * v * 0.6 * dt;
      if (!blocked(nx, ny)) { bot.x = nx; bot.y = ny; }
      if (timer > 0.45) fire('timer done');
    } else if (state === 'TURN') {
      const s = Math.sign(turnLeft) * 2.6 * dt; bot.a += s; turnLeft -= s;
      if (Math.abs(turnLeft) < 0.05) fire('turn done');
    } else if (state === 'CHARGE') {
      battery = Math.min(100, battery + dt * 12);
      if (battery >= 100) { fire('battery full'); bot.a += Math.PI; }
    }
    if (state === 'SEARCH' || state === 'DOCK') {
      const i = Math.floor((bot.x - room.x) / room.w * GX), j = Math.floor((bot.y - room.y) / room.h * GY);
      for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) { const ii = i + di, jj = j + dj; if (ii >= 0 && jj >= 0 && ii < GX && jj < GY && dirt[jj * GX + ii]) { dirt[jj * GX + ii] = 0; dirtLeft--; } }
    }
  }

  const NODE = {};
  function nodePos() {
    const cx = dg.x + dg.w / 2, cy = dg.y + dg.h * 0.5, rx = dg.w * 0.34, ry = dg.h * 0.28;
    NODE.SEARCH = [cx, cy - ry]; NODE.BACKUP = [cx + rx, cy]; NODE.TURN = [cx, cy + ry * 0.6]; NODE.DOCK = [cx - rx, cy]; NODE.CHARGE = [cx - rx, cy - ry];
  }

  k.frame((ctx, dt, w, h) => {
    if (running) { const n = Math.ceil(speedMul); for (let i = 0; i < n; i++) stepFSM(dt * speedMul / n); }
    for (const s of STATES) { glowS[s].to(s === state ? 1 : 0); glowS[s].step(dt); }
    for (let i = 0; i < flash.length; i++) flash[i] = Math.max(0, flash[i] - dt * 1.2);
    ctx.fillStyle = '#f7f9fd'; ctx.fillRect(0, 0, w, h);
    // room floor
    ctx.fillStyle = '#efe6d6'; ctx.beginPath(); ctx.roundRect(room.x, room.y, room.w, room.h, 10); ctx.fill();
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 4; ctx.stroke();
    ctx.fillStyle = 'rgba(120,90,50,0.45)';
    const cw = room.w / GX, ch = room.h / GY;
    for (let j = 0; j < GY; j++) for (let i = 0; i < GX; i++) if (dirt[j * GX + i]) ctx.fillRect(room.x + i * cw + cw * 0.35, room.y + j * ch + ch * 0.35, 3, 3);
    // dock
    ctx.fillStyle = state === 'CHARGE' ? '#16a34a' : '#334155'; ctx.beginPath(); ctx.roundRect(dock.x - 14, dock.y - 14, 28, 28, 6); ctx.fill();
    text(ctx, '⚡', dock.x, dock.y + 5, '#fde047', 14, 700, 'center');
    for (const f of furn) { softShadow(ctx, f.x + f.w / 2, f.y + f.h + 2, f.w * 0.55, 5, 0.2); ctx.fillStyle = f.c; ctx.beginPath(); ctx.roundRect(f.x, f.y, f.w, f.h, 6); ctx.fill(); text(ctx, f.name, f.x + f.w / 2, f.y + f.h / 2 + 4, 'rgba(255,255,255,0.9)', 10, 700, 'center'); }
    // robot
    softShadow(ctx, bot.x, bot.y + 3, R * 1.1, R * 0.8, 0.25);
    ctx.beginPath(); ctx.arc(bot.x, bot.y, R, 0, Math.PI * 2); ctx.fillStyle = '#e2e8f0'; ctx.fill(); ctx.strokeStyle = SCOL[state]; ctx.lineWidth = 3; ctx.stroke();
    ctx.beginPath(); ctx.arc(bot.x, bot.y, R, bot.a - 1, bot.a + 1); ctx.strokeStyle = '#334155'; ctx.lineWidth = 4; ctx.stroke();
    ctx.beginPath(); ctx.arc(bot.x + Math.cos(bot.a) * R * 0.45, bot.y + Math.sin(bot.a) * R * 0.45, 2.5, 0, Math.PI * 2); ctx.fillStyle = SCOL[state]; ctx.fill();
    // battery bar
    ctx.fillStyle = T.line2; ctx.fillRect(room.x + 8, room.y + 8, 80, 8); ctx.fillStyle = battery < 20 ? T.red : T.green; ctx.fillRect(room.x + 8, room.y + 8, 0.8 * battery, 8);
    // diagram
    nodePos();
    card(ctx, dg.x, dg.y, dg.w, dg.h, 14);
    text(ctx, 'State diagram', dg.x + 12, dg.y + 20, T.ink, 11.5, 700);
    const nw = k.small ? 64 : 84, nh = k.small ? 24 : 30;
    for (let i = 0; i < EDGES.length; i++) {
      const [a, b, e] = EDGES[i];
      if (b === 'DOCK' && !dockEnabled) continue;
      const A = NODE[a], B = NODE[b];
      const mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2, dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy);
      const off = 14, ox = -dy / L * off, oy = dx / L * off;
      const sx = A[0] + ox + dx / L * nw * 0.45, sy = A[1] + oy + dy / L * nh * 0.9, ex = B[0] + ox - dx / L * nw * 0.45, ey = B[1] + oy - dy / L * nh * 0.9;
      const f = flash[i];
      arrow(ctx, sx, sy, ex, ey, f > 0 ? withAlpha(T.orange, 0.5 + f * 0.5) : 'rgba(100,116,139,0.55)', f > 0 ? 2.5 + f * 2 : 1.6, 8);
      if (!k.small || e === 'bump') text(ctx, e, mx + ox * 1.8, my + oy * 1.8 + 3, f > 0 ? T.orange : T.mute, k.small ? 8 : 9.5, 600, 'center');
    }
    for (const s of STATES) {
      if (s === 'DOCK' && !dockEnabled) continue;
      const [x, y] = NODE[s], g = glowS[s].x;
      if (g > 0.02) { ctx.fillStyle = withAlpha(SCOL[s], 0.18 * g); ctx.beginPath(); ctx.roundRect(x - nw / 2 - 6 * g, y - nh / 2 - 6 * g, nw + 12 * g, nh + 12 * g, 12); ctx.fill(); }
      ctx.fillStyle = g > 0.5 ? SCOL[s] : '#fff'; ctx.strokeStyle = SCOL[s]; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.roundRect(x - nw / 2, y - nh / 2, nw, nh, 9); ctx.fill(); ctx.stroke();
      text(ctx, s, x, y + 4, g > 0.5 ? '#fff' : SCOL[s], k.small ? 10 : 11.5, 800, 'center');
    }
    if (!k.small) { for (let i = 0; i < log.length; i++) text(ctx, log[i], dg.x + 14, dg.y + dg.h - 14 - i * 16, i ? T.mute : T.ink2, 10.5, i ? 500 : 700); }
    st.state.set(state); st.bat.set(`${fmt(battery, 0)} %`); st.clean.set(`${fmt(100 * (1 - dirtLeft / Math.max(1, dirtTotal)), 0)} %`); st.last.set(log[0] || '—');
    if (battery > 0 || dockEnabled) { badge.set(`State: ${state}`); badge.el.style.setProperty('--ix-hud-color', SCOL[state]); }
    k.animate(running || dragF !== null);
  });

  k.debug = { state: () => state, fire, battery: (b) => { battery = b; }, furn: () => [furn[0].x + 10, furn[0].y + 10] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
