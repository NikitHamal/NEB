import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const GHOST_COLORS = ['rgba(125,211,252,0.4)', 'rgba(244,114,182,0.4)', 'rgba(163,230,53,0.4)', 'rgba(196,181,253,0.4)'];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Ready to fire', '#F59E0B');

  let speed = 30;
  let angle = 45;
  let g = 9.81;
  let air = false;
  let flying = false;
  let px = 0, py = 0, vx = 0, vy = 0;
  let flightTime = 0;
  let maxH = 0;
  let trail = [];
  let ghosts = [];
  let lastResult = null;

  const WORLD_W = 400;
  const GROUND_PAD = 46;
  const MAX_TRAIL = 1200;

  const panel = createPanel(stage, { title: 'Launch Controls' });
  panel.slider({
    label: 'Launch speed',
    min: 5, max: 60, step: 1, value: speed,
    format: (v) => `${v} m/s`,
    onChange: (v) => { speed = v; },
  });
  panel.slider({
    label: 'Launch angle',
    min: 5, max: 85, step: 1, value: angle,
    format: (v) => `${v}°`,
    onChange: (v) => { angle = v; },
  });
  panel.slider({
    label: 'Gravity g',
    min: 1, max: 25, step: 0.1, value: g,
    format: (v) => `${v.toFixed(1)} m/s²`,
    onChange: (v) => { g = v; },
  });
  panel.toggle({
    label: 'Air resistance',
    value: false,
    onChange: (v) => { air = v; },
  });
  panel.buttonRow([
    { label: 'Fire!', icon: 'rocket_launch', onClick: fire },
    { label: 'Clear', icon: 'mop', variant: 'ghost', onClick: () => { ghosts = []; trail = []; lastResult = null; flying = false; statusBadge.set('Ready to fire'); } },
  ]);
  panel.divider();
  const rangeOut = panel.readout({ label: 'Range', value: '—' });
  const heightOut = panel.readout({ label: 'Max height', value: '—' });
  const timeOut = panel.readout({ label: 'Flight time', value: '—' });
  panel.info('Fire several shots at different angles — old trajectories stay as ghosts so you can compare. Try 30° vs 60°.');

  function fire() {
    if (trail.length > 1) {
      ghosts.push({ pts: trail, air });
      if (ghosts.length > 4) ghosts.shift();
    }
    const rad = (angle * Math.PI) / 180;
    px = 0;
    py = 0;
    vx = speed * Math.cos(rad);
    vy = speed * Math.sin(rad);
    flightTime = 0;
    maxH = 0;
    trail = [{ x: 0, y: 0 }];
    flying = true;
    lastResult = null;
    statusBadge.set('In flight…');
  }

  function step(dt) {
    const sub = 6;
    const h = dt / sub;
    for (let i = 0; i < sub && flying; i++) {
      if (air) {
        const k = 0.012;
        const v = Math.hypot(vx, vy);
        vx -= k * v * vx * h;
        vy -= k * v * vy * h;
      }
      vy -= g * h;
      px += vx * h;
      py += vy * h;
      flightTime += h;
      if (py > maxH) maxH = py;
      if (py <= 0 && vy < 0) {
        py = 0;
        flying = false;
        lastResult = { range: px, maxH, time: flightTime };
        rangeOut.set(`${px.toFixed(1)} m`);
        heightOut.set(`${maxH.toFixed(1)} m`);
        timeOut.set(`${flightTime.toFixed(2)} s`);
        statusBadge.set(`Landed at ${px.toFixed(0)} m`);
      } else if (px > WORLD_W) {
        flying = false;
        rangeOut.set(`> ${WORLD_W} m`);
        heightOut.set(`${maxH.toFixed(1)} m`);
        timeOut.set(`> ${flightTime.toFixed(2)} s`);
        statusBadge.set(`Out of range (> ${WORLD_W} m)`);
      }
    }
    if (flying) {
      trail.push({ x: px, y: py });
      if (trail.length > MAX_TRAIL) trail.shift();
    }
  }

  function toScreen(wx, wy, w, h) {
    const scale = (w - 70) / WORLD_W;
    return { x: 40 + wx * scale, y: h - GROUND_PAD - wy * scale, scale };
  }

  function drawTrail(ctx, pts, color, w, h, width) {
    if (pts.length < 2) return;
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    for (let i = 0; i < pts.length; i++) {
      const s = toScreen(pts[i].x, pts[i].y, w, h);
      if (i === 0) ctx.moveTo(s.x, s.y);
      else ctx.lineTo(s.x, s.y);
    }
    ctx.stroke();
  }

  sim.setUpdate((ctx, dt, w, h) => {
    if (flying) step(dt);
    ctx.clearRect(0, 0, w, h);
    const groundY = h - GROUND_PAD;
    const scale = (w - 70) / WORLD_W;

    ctx.fillStyle = 'rgba(34,52,80,0.85)';
    ctx.fillRect(0, groundY, w, GROUND_PAD);
    ctx.strokeStyle = 'rgba(199,212,234,0.6)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, groundY);
    ctx.lineTo(w, groundY);
    ctx.stroke();

    ctx.fillStyle = 'rgba(199,212,234,0.55)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.strokeStyle = 'rgba(199,212,234,0.3)';
    ctx.lineWidth = 1;
    for (let m = 0; m <= WORLD_W; m += 50) {
      const s = toScreen(m, 0, w, h);
      ctx.beginPath();
      ctx.moveTo(s.x, groundY);
      ctx.lineTo(s.x, groundY + 6);
      ctx.stroke();
      ctx.fillText(`${m} m`, s.x, groundY + 18);
    }

    ghosts.forEach((gh, i) => drawTrail(ctx, gh.pts, GHOST_COLORS[i % GHOST_COLORS.length], w, h, 1.5));
    drawTrail(ctx, trail, '#F59E0B', w, h, 2.5);

    const rad = (angle * Math.PI) / 180;
    const base = toScreen(0, 0, w, h);
    ctx.save();
    ctx.translate(base.x, base.y);
    ctx.rotate(-rad);
    ctx.fillStyle = '#8aa3c8';
    ctx.fillRect(0, -5, 34, 10);
    ctx.restore();
    ctx.fillStyle = '#5d779e';
    ctx.beginPath();
    ctx.arc(base.x, base.y, 11, Math.PI, 0);
    ctx.fill();

    if (!flying && !lastResult) {
      ctx.strokeStyle = 'rgba(245,158,11,0.45)';
      ctx.setLineDash([4, 6]);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(base.x, base.y);
      ctx.lineTo(base.x + Math.cos(rad) * 60, base.y - Math.sin(rad) * 60);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    if (flying) {
      const s = toScreen(px, py, w, h);
      ctx.fillStyle = '#ffd584';
      ctx.beginPath();
      ctx.arc(s.x, s.y, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(125,211,252,0.8)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(s.x + vx * scale * 0.4, s.y);
      ctx.stroke();
      ctx.strokeStyle = 'rgba(244,114,182,0.8)';
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(s.x, s.y - vy * scale * 0.4);
      ctx.stroke();
    }

    if (lastResult) {
      const top = toScreen(lastResult.range / 2, lastResult.maxH, w, h);
      const land = toScreen(lastResult.range, 0, w, h);
      ctx.strokeStyle = 'rgba(139,233,168,0.7)';
      ctx.setLineDash([3, 5]);
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(top.x, top.y);
      ctx.lineTo(top.x, groundY);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#8be9a8';
      ctx.font = '700 11px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`H = ${lastResult.maxH.toFixed(1)} m`, top.x, top.y - 8);
      ctx.fillStyle = '#F59E0B';
      ctx.beginPath();
      ctx.moveTo(land.x, groundY - 12);
      ctx.lineTo(land.x - 6, groundY);
      ctx.lineTo(land.x + 6, groundY);
      ctx.closePath();
      ctx.fill();
      ctx.fillText(`R = ${lastResult.range.toFixed(1)} m`, Math.min(land.x, w - 50), groundY - 20);
    }

    ctx.fillStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    const ideal = (speed * speed * Math.sin(2 * rad)) / g;
    ctx.fillText(`Ideal range (no air): ${ideal.toFixed(1)} m`, 16, 24);
  });

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
