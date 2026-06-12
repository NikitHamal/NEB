import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const TRACK = [];
const N = 220;
for (let i = 0; i <= N; i++) {
  const t = (i / N) * Math.PI * 2;
  const r = 0.33 + 0.10 * Math.sin(t * 3) + 0.045 * Math.sin(t * 5 + 1.3);
  TRACK.push({ a: t, r });
}

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const panel = createPanel(stage, { title: 'Line Follower' });
  const hud = createHud(stage);
  const stateBadge = hud.badge('Paused', '#94a3b8');

  let running = false;
  let speed = 60;
  let turnStrength = 60;
  let lost = false;
  let lostTimer = 0;

  const robot = { x: 0, y: 0, heading: 0 };
  let placed = false;

  panel.toggle({
    label: 'Run', value: false,
    onChange: (v) => {
      running = v;
      stateBadge.set(running ? 'Following the line' : 'Paused');
      stateBadge.el.style.setProperty('--ix-hud-color', running ? '#35d07f' : '#94a3b8');
    },
  });
  panel.slider({
    label: 'Speed', min: 20, max: 160, step: 5, value: speed,
    format: (v) => v + ' px/s',
    onChange: (v) => { speed = v; },
  });
  panel.slider({
    label: 'Turn strength', min: 20, max: 140, step: 5, value: turnStrength,
    format: (v) => v + '°/s',
    onChange: (v) => { turnStrength = v; },
  });
  panel.button({
    label: 'Reset robot', icon: 'restart_alt', variant: 'ghost',
    onClick: () => { placed = false; lost = false; },
  });
  panel.info('Two IR sensors watch the floor. If the left sensor sees the dark line, steer left; right sensor, steer right. Crank the speed and watch it lose the track on sharp bends!');

  let trackPts = [];
  sim.onResize((w, h) => {
    const cx = w / 2;
    const cy = h / 2;
    const scale = Math.min(w, h);
    trackPts = TRACK.map((p) => ({ x: cx + Math.cos(p.a) * p.r * scale, y: cy + Math.sin(p.a) * p.r * scale * 0.92 }));
    placed = false;
  });

  function trackPoint(idx) {
    return trackPts[((idx % trackPts.length) + trackPts.length) % trackPts.length];
  }

  function isOnLine(x, y, lineW) {
    let best = Infinity;
    const step = 2;
    for (let i = 0; i < trackPts.length; i += step) {
      const p = trackPts[i];
      const d = (p.x - x) * (p.x - x) + (p.y - y) * (p.y - y);
      if (d < best) best = d;
    }
    return Math.sqrt(best) < lineW / 2;
  }

  sim.setUpdate((ctx, dt, w, h) => {
    const lineW = Math.max(10, Math.min(w, h) * 0.028);

    if (!placed && w > 10) {
      const p0 = trackPoint(0);
      const p1 = trackPoint(2);
      robot.x = p0.x;
      robot.y = p0.y;
      robot.heading = Math.atan2(p1.y - p0.y, p1.x - p0.x);
      placed = true;
      lost = false;
    }

    const sensorDist = lineW * 1.5;
    const sensorSpread = lineW * 0.78;
    const fx = Math.cos(robot.heading);
    const fy = Math.sin(robot.heading);
    const sx = -fy;
    const sy = fx;
    const sensorL = { x: robot.x + fx * sensorDist - sx * sensorSpread, y: robot.y + fy * sensorDist - sy * sensorSpread };
    const sensorR = { x: robot.x + fx * sensorDist + sx * sensorSpread, y: robot.y + fy * sensorDist + sy * sensorSpread };
    const onL = isOnLine(sensorL.x, sensorL.y, lineW * 1.25);
    const onR = isOnLine(sensorR.x, sensorR.y, lineW * 1.25);

    if (running) {
      const turn = (turnStrength * Math.PI) / 180;
      if (onL && !onR) robot.heading -= turn * dt;
      else if (onR && !onL) robot.heading += turn * dt;
      const mx = Math.cos(robot.heading);
      const my = Math.sin(robot.heading);
      robot.x += mx * speed * dt;
      robot.y += my * speed * dt;
      robot.x = Math.max(20, Math.min(w - 20, robot.x));
      robot.y = Math.max(20, Math.min(h - 20, robot.y));

      const bodyOn = isOnLine(robot.x + mx * sensorDist, robot.y + my * sensorDist, lineW * 3.2);
      if (!onL && !onR && !bodyOn) {
        lostTimer += dt;
        if (lostTimer > 0.7 && !lost) {
          lost = true;
          stateBadge.set('Lost the line! Lower the speed and reset.');
          stateBadge.el.style.setProperty('--ix-hud-color', '#e2484d');
        }
      } else {
        lostTimer = 0;
        if (lost) {
          lost = false;
          stateBadge.set('Following the line');
          stateBadge.el.style.setProperty('--ix-hud-color', '#35d07f');
        }
      }
    }

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#dbe4f0';
    ctx.fillRect(w * 0.04, h * 0.04, w * 0.92, h * 0.92);

    ctx.strokeStyle = '#141a24';
    ctx.lineWidth = lineW;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    const start = trackPoint(0);
    ctx.moveTo(start.x, start.y);
    for (let i = 1; i <= trackPts.length; i++) {
      const p = trackPoint(i);
      ctx.lineTo(p.x, p.y);
    }
    ctx.closePath();
    ctx.stroke();

    const rw = lineW * 2.4;
    ctx.save();
    ctx.translate(robot.x, robot.y);
    ctx.rotate(robot.heading);
    ctx.fillStyle = lost ? '#e2484d' : '#0284C7';
    roundRect(ctx, -rw * 0.55, -rw * 0.42, rw * 1.1, rw * 0.84, 6);
    ctx.fill();
    ctx.fillStyle = '#1c2c44';
    ctx.fillRect(-rw * 0.45, -rw * 0.58, rw * 0.42, rw * 0.16);
    ctx.fillRect(-rw * 0.45, rw * 0.42, rw * 0.42, rw * 0.16);
    ctx.fillStyle = '#f5b942';
    ctx.beginPath();
    ctx.moveTo(rw * 0.55, 0);
    ctx.lineTo(rw * 0.3, -rw * 0.2);
    ctx.lineTo(rw * 0.3, rw * 0.2);
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    drawSensor(ctx, sensorL, onL);
    drawSensor(ctx, sensorR, onR);

    ctx.fillStyle = 'rgba(20,26,36,0.78)';
    ctx.font = '600 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    const msg = !running ? 'Toggle "Run" to start' :
      onL && !onR ? 'Left sensor on line → steering LEFT' :
      onR && !onL ? 'Right sensor on line → steering RIGHT' :
      onL && onR ? 'Both sensors on line → straight' :
      'Searching for the line…';
    ctx.fillText(msg, w * 0.06, h * 0.09);
  });

  function drawSensor(ctx, s, active) {
    ctx.beginPath();
    ctx.arc(s.x, s.y, 6, 0, Math.PI * 2);
    ctx.fillStyle = active ? '#ff4d5e' : '#7c8aa3';
    ctx.fill();
    ctx.strokeStyle = '#10151f';
    ctx.lineWidth = 2;
    ctx.stroke();
    if (active) {
      ctx.beginPath();
      ctx.arc(s.x, s.y, 11, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255,77,94,0.5)';
      ctx.stroke();
    }
  }

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
