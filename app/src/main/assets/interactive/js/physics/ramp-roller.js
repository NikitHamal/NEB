import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const G = 9.81;
const RAMP_LEN = 6;
const BALL_R = 16;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Press Go to race!', '#F59E0B');

  let angle = 25;
  let mu = 0.1;
  let s = 0;
  let v = 0;
  let t = 0;
  let running = false;
  let finished = false;
  let bestTime = 0;
  let spin = 0;

  function accel() {
    const rad = (angle * Math.PI) / 180;
    return Math.max(0, G * (Math.sin(rad) - mu * Math.cos(rad)));
  }

  function reset() {
    s = 0;
    v = 0;
    t = 0;
    spin = 0;
    running = false;
    finished = false;
    badge.set('Press Go to race!');
  }

  const panel = createPanel(stage, { title: 'Ramp Controls' });
  panel.slider({
    label: 'Ramp angle',
    min: 5, max: 45, step: 1, value: angle,
    format: (val) => `${val}°`,
    onChange: (val) => { angle = val; reset(); },
  });
  panel.slider({
    label: 'Friction',
    min: 0, max: 0.8, step: 0.02, value: mu,
    format: (val) => val.toFixed(2),
    onChange: (val) => { mu = val; reset(); },
  });
  panel.buttonRow([
    { label: 'Go!', icon: 'play_arrow', onClick: () => { if (!running && !finished) { running = true; badge.set('Rolling…'); } } },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset },
  ]);
  panel.divider();
  const timeOut = panel.readout({ label: 'Race time', value: '0.00 s' });
  const bestOut = panel.readout({ label: 'Best time', value: '—' });
  const speedOut = panel.readout({ label: 'Speed', value: '0.0 m/s' });
  panel.info('Steeper ramps make the ball speed up faster. Slide the friction up and see what slows it down — or stops it completely!');

  function step(dt) {
    if (!running) return;
    const a = accel();
    if (a <= 0 && v <= 0) {
      running = false;
      badge.set('Too much friction — it will not roll!');
      return;
    }
    v += a * dt;
    s += v * dt;
    spin += (v / (BALL_R / 40)) * dt;
    t += dt;
    if (s >= RAMP_LEN) {
      s = RAMP_LEN;
      running = false;
      finished = true;
      if (!bestTime || t < bestTime) {
        bestTime = t;
        bestOut.set(`${bestTime.toFixed(2)} s`);
      }
      badge.set(`Finished in ${t.toFixed(2)} s!`);
    }
  }

  function geometry(w, h) {
    const rad = (angle * Math.PI) / 180;
    const margin = 36;
    const baseY = h - 70;
    const availW = w - margin * 2;
    const availH = baseY - 60;
    const scale = Math.min(availW / (RAMP_LEN * Math.cos(rad)), availH / (RAMP_LEN * Math.sin(rad)));
    const topX = margin;
    const topY = baseY - RAMP_LEN * Math.sin(rad) * scale;
    return { rad, topX, topY, baseY, scale, botX: topX + RAMP_LEN * Math.cos(rad) * scale };
  }

  sim.setUpdate((ctx, dt, w, h) => {
    step(Math.min(dt, 0.05));
    ctx.clearRect(0, 0, w, h);
    const gm = geometry(w, h);

    ctx.fillStyle = '#14532d';
    ctx.fillRect(0, gm.baseY, w, h - gm.baseY);
    ctx.fillStyle = '#22c55e';
    ctx.fillRect(0, gm.baseY, w, 7);

    ctx.fillStyle = '#7c3aed';
    ctx.beginPath();
    ctx.moveTo(gm.topX, gm.topY);
    ctx.lineTo(gm.botX, gm.baseY);
    ctx.lineTo(gm.topX, gm.baseY);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#c4b5fd';
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(gm.topX, gm.topY);
    ctx.lineTo(gm.botX, gm.baseY);
    ctx.stroke();

    const fx = gm.botX + 4;
    for (let i = 0; i < 5; i++) {
      ctx.fillStyle = i % 2 ? '#e8eefb' : '#1c2f4d';
      ctx.fillRect(fx, gm.baseY - 8 - i * 9, 10, 9);
      ctx.fillStyle = i % 2 ? '#1c2f4d' : '#e8eefb';
      ctx.fillRect(fx + 10, gm.baseY - 8 - i * 9, 10, 9);
    }
    ctx.fillStyle = '#ffd584';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('FINISH', fx + 10, gm.baseY - 56);

    const along = s * gm.scale;
    const nx = -Math.sin(gm.rad);
    const ny = -Math.cos(gm.rad);
    const cx = gm.topX + Math.cos(gm.rad) * along - nx * BALL_R;
    const cy = gm.topY + Math.sin(gm.rad) * along + ny * BALL_R;
    const grad = ctx.createRadialGradient(cx - 5, cy - 5, 3, cx, cy, BALL_R + 2);
    grad.addColorStop(0, '#fda4af');
    grad.addColorStop(1, '#e11d48');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(cx, cy, BALL_R, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,0.85)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(spin) * (BALL_R - 5), cy + Math.sin(spin) * (BALL_R - 5));
    ctx.stroke();

    ctx.fillStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '700 13px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`angle = ${angle}°`, 16, 26);
    const a = accel();
    ctx.fillText(`a = ${a.toFixed(1)} m/s²${a === 0 ? '  (stuck!)' : ''}`, 16, 44);

    timeOut.set(`${t.toFixed(2)} s`);
    speedOut.set(`${v.toFixed(1)} m/s`);
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
