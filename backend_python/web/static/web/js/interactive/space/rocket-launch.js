import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const G0 = 9.81;
const VE = 2900;
const DRY_MASS = 1600;
const TARGET_ALT = 100000;

export default function init(stage) {
  const sim = createCanvas2D(stage);

  let thrustKN = 220;
  let fuelStart = 4500;
  let state = null;
  let clouds = [];
  let stars = [];
  let confetti = [];
  let viewMode = '2d';

  sim.onResize((w, h) => {
    clouds = [];
    for (let i = 0; i < 14; i++) {
      clouds.push({ alt: 800 + Math.random() * 11000, x: Math.random(), s: 30 + Math.random() * 50 });
    }
    stars = [];
    for (let i = 0; i < 90; i++) {
      stars.push({ x: Math.random(), y: Math.random(), r: Math.random() * 1.3 + 0.4 });
    }
  });

  function reset() {
    state = {
      phase: 'pad',
      alt: 0,
      vel: 0,
      fuel: fuelStart,
      fuelStart,
      stage1Fuel: fuelStart * 0.6,
      stage: 1,
      time: 0,
      success: false,
      booster: null,
      graph: [],
      graphT: 0,
      maxAlt: 0,
      flame: 0,
    };
    confetti = [];
    statusBadge.set('On the pad \u2014 set thrust & fuel, then IGNITE');
    statusBadge.el.style.setProperty('--ix-hud-color', '#9ec1ff');
  }

  const hud = createHud(stage);
  const statusBadge = hud.badge('On the pad', '#9ec1ff');

  const panel = createPanel(stage, { title: 'Mission Control' });
  panel.select({
    label: 'View',
    options: [
      { value: '2d', label: '2D' },
      { value: '3d', label: '3D' },
    ],
    value: viewMode,
    onChange: (v) => { viewMode = v; },
  });
  const thrustSlider = panel.slider({
    label: 'Thrust',
    min: 60, max: 420, step: 10, value: thrustKN,
    format: (v) => `${v} kN`,
    onChange: (v) => { thrustKN = v; if (state.phase === 'pad') reset(); },
  });
  const fuelSlider = panel.slider({
    label: 'Fuel load',
    min: 1000, max: 9000, step: 250, value: fuelStart,
    format: (v) => `${(v / 1000).toFixed(2)} t`,
    onChange: (v) => { fuelStart = v; if (state.phase === 'pad') reset(); },
  });
  const altReadout = panel.readout({ label: 'Altitude', value: '0.0 km' });
  const velReadout = panel.readout({ label: 'Velocity', value: '0 m/s' });
  const fuelReadout = panel.readout({ label: 'Fuel', value: '100%' });
  const twrReadout = panel.readout({ label: 'Thrust / weight', value: '\u2014' });
  panel.buttonRow([
    {
      label: 'IGNITE',
      icon: 'local_fire_department',
      onClick: () => {
        if (state.phase !== 'pad') return;
        state.phase = 'flight';
        statusBadge.set('Lift-off!');
        statusBadge.el.style.setProperty('--ix-hud-color', '#ffb340');
      },
    },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset },
  ]);
  panel.info('Newton\u2019s 3rd law: the engine throws gas down, the gas pushes the rocket up. Thrust must beat weight to lift off. Reach 100 km \u2014 the edge of space!');

  reset();

  function mass() {
    const stageDry = state.stage === 1 ? DRY_MASS : DRY_MASS * 0.45;
    return stageDry + state.fuel;
  }

  function physics(dt) {
    const s = state;
    s.time += dt;
    if (s.phase === 'flight' || s.phase === 'coast') {
      let thrust = 0;
      if (s.fuel > 0 && s.phase === 'flight') {
        thrust = thrustKN * 1000 * (s.stage === 2 ? 0.5 : 1);
        const mdot = thrust / VE;
        s.fuel = Math.max(0, s.fuel - mdot * dt);
        if (s.stage === 1 && s.fuel <= s.fuelStart - s.stage1Fuel) {
          s.stage = 2;
          s.booster = { alt: s.alt, vel: s.vel, x: 0, t: 0 };
          statusBadge.set('Stage separation!');
          statusBadge.el.style.setProperty('--ix-hud-color', '#c4b5fd');
        }
        if (s.fuel === 0) {
          s.phase = 'coast';
          if (!s.success) {
            statusBadge.set('Engine cut-off \u2014 coasting');
            statusBadge.el.style.setProperty('--ix-hud-color', '#9ec1ff');
          }
        }
      }
      const g = G0 * Math.pow(6371000 / (6371000 + s.alt), 2);
      const acc = thrust / mass() - g;
      if (s.alt <= 0 && acc < 0) {
        s.vel = 0;
        s.alt = 0;
      } else {
        s.vel += acc * dt;
        s.alt += s.vel * dt;
      }
      s.flame = thrust > 0 ? Math.min(1, s.flame + dt * 6) : Math.max(0, s.flame - dt * 8);
      s.maxAlt = Math.max(s.maxAlt, s.alt);
      s.graphT += dt;
      if (s.graphT > 0.25 && s.graph.length < 400) {
        s.graphT = 0;
        s.graph.push(s.alt);
      }
      if (s.alt >= TARGET_ALT && !s.success) {
        s.success = true;
        statusBadge.set('\ud83c\udf89 You reached space! 100 km \u2014 the K\u00e1rm\u00e1n line!');
        statusBadge.el.style.setProperty('--ix-hud-color', '#8be9a8');
        for (let i = 0; i < 70; i++) {
          confetti.push({
            x: Math.random(),
            y: Math.random() * 0.4,
            vx: (Math.random() - 0.5) * 60,
            vy: 30 + Math.random() * 80,
            color: ['#8be9a8', '#ffd27a', '#7dd3fc', '#f9a8d4', '#c4b5fd'][i % 5],
            t: 0,
            life: 2.5 + Math.random() * 2,
          });
        }
      }
      if (s.alt <= 0 && s.vel <= 0 && s.phase === 'coast') {
        s.phase = 'down';
        if (s.success) {
          statusBadge.set('Mission complete \u2014 you touched space and came home!');
          statusBadge.el.style.setProperty('--ix-hud-color', '#8be9a8');
        } else {
          statusBadge.set('Back on the ground \u2014 try more thrust or fuel');
          statusBadge.el.style.setProperty('--ix-hud-color', '#fda4af');
        }
      }
    }
    if (s.booster) {
      s.booster.t += dt;
      s.booster.vel -= G0 * dt;
      s.booster.alt = Math.max(0, s.booster.alt + s.booster.vel * dt);
      s.booster.x += dt * 18;
      if (s.booster.t > 9) s.booster = null;
    }
    for (let i = confetti.length - 1; i >= 0; i--) {
      const c = confetti[i];
      c.t += dt;
      if (c.t > c.life) confetti.splice(i, 1);
    }
  }

  function altToY(alt, h, viewTop) {
    return h * 0.86 - (alt / viewTop) * h * 0.78;
  }

  function drawRocket(ctx, x, y, scale, flame, hasBooster, is3d = false) {
    if (is3d) {
      ctx.fillStyle = 'rgba(0,0,0,0.22)';
      ctx.beginPath();
      ctx.ellipse(x + 10 * scale, y + 24 * scale, 20 * scale, 5 * scale, 0, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(scale, scale);
    if (flame > 0.05) {
      const fl = 18 + Math.random() * 10;
      const grad = ctx.createLinearGradient(0, 14, 0, 14 + fl);
      grad.addColorStop(0, 'rgba(255,220,120,0.95)');
      grad.addColorStop(0.5, 'rgba(255,140,50,0.8)');
      grad.addColorStop(1, 'rgba(255,80,30,0)');
      ctx.fillStyle = grad;
      ctx.globalAlpha = flame;
      ctx.beginPath();
      ctx.moveTo(-5, 14);
      ctx.lineTo(0, 14 + fl);
      ctx.lineTo(5, 14);
      ctx.closePath();
      ctx.fill();
      ctx.globalAlpha = 1;
    }
    if (hasBooster) {
      ctx.fillStyle = '#aab6c8';
      ctx.fillRect(-7, -2, 4, 16);
      ctx.fillRect(3, -2, 4, 16);
      if (is3d) {
        ctx.fillStyle = '#8793a4';
        ctx.fillRect(7, -1, 4, 15);
      }
    }
    if (is3d) {
      ctx.fillStyle = '#aab6c8';
      ctx.beginPath();
      ctx.moveTo(7, -16);
      ctx.quadraticCurveTo(14, -4, 13, 12);
      ctx.lineTo(7, 14);
      ctx.lineTo(7, 4);
      ctx.quadraticCurveTo(7, -8, 0, -22);
      ctx.closePath();
      ctx.fill();
    }
    ctx.fillStyle = '#e8eefb';
    ctx.beginPath();
    ctx.moveTo(0, -22);
    ctx.quadraticCurveTo(7, -8, 7, 4);
    ctx.lineTo(7, 14);
    ctx.lineTo(-7, 14);
    ctx.lineTo(-7, 4);
    ctx.quadraticCurveTo(-7, -8, 0, -22);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#e2484d';
    ctx.beginPath();
    ctx.moveTo(-7, 14);
    ctx.lineTo(-12, 20);
    ctx.lineTo(-7, 6);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(7, 14);
    ctx.lineTo(12, 20);
    ctx.lineTo(7, 6);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#4d7fff';
    ctx.beginPath();
    ctx.arc(0, -6, 3.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  sim.setUpdate((ctx, dt, w, h) => {
    physics(dt);
    const s = state;
    const is3d = viewMode === '3d';
    const viewTop = Math.max(2200, s.alt * 1.9);
    const skyT = Math.min(1, s.alt / 80000);
    const r = Math.round(120 - 108 * skyT);
    const g = Math.round(170 - 152 * skyT);
    const b = Math.round(230 - 196 * skyT);
    ctx.fillStyle = `rgb(${Math.round(r * 0.35)},${Math.round(g * 0.45)},${b})`;
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, `rgb(${Math.round(r * 0.3)},${Math.round(g * 0.4)},${Math.round(b * 0.75)})`);
    grad.addColorStop(1, `rgb(${r},${g},${b})`);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    if (skyT > 0.35) {
      ctx.globalAlpha = (skyT - 0.35) / 0.65;
      ctx.fillStyle = '#dde7f5';
      for (let i = 0; i < stars.length; i++) {
        ctx.fillRect(stars[i].x * w, stars[i].y * h, stars[i].r, stars[i].r);
      }
      ctx.globalAlpha = 1;
    }

    ctx.fillStyle = 'rgba(255,255,255,0.75)';
    for (let i = 0; i < clouds.length; i++) {
      const c = clouds[i];
      const y = altToY(c.alt, h, viewTop);
      if (y < -40 || y > h) continue;
      ctx.beginPath();
      ctx.ellipse(c.x * w + (is3d ? c.s * 0.18 : 0), y, c.s, c.s * (is3d ? 0.22 : 0.32), 0, 0, Math.PI * 2);
      ctx.fill();
    }

    const groundY = altToY(0, h, viewTop);
    if (groundY < h + 60) {
      if (is3d) {
        ctx.fillStyle = '#2e4d3a';
        ctx.beginPath();
        ctx.ellipse(w / 2, groundY + h * 0.14, w * 0.62, h * 0.18, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#3f6b4f';
        ctx.beginPath();
        ctx.ellipse(w / 2, groundY + 2, w * 0.34, 12, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#5b6573';
        ctx.beginPath();
        ctx.moveTo(w / 2 - 34, groundY - 5);
        ctx.lineTo(w / 2 + 34, groundY - 5);
        ctx.lineTo(w / 2 + 48, groundY + 6);
        ctx.lineTo(w / 2 - 18, groundY + 8);
        ctx.closePath();
        ctx.fill();
      } else {
        ctx.fillStyle = '#2e4d3a';
        ctx.fillRect(0, groundY, w, h - groundY + 2);
        ctx.fillStyle = '#3f6b4f';
        ctx.fillRect(0, groundY, w, 5);
        ctx.fillStyle = '#5b6573';
        ctx.fillRect(w / 2 - 30, groundY - 6, 60, 6);
      }
    }

    const kline = altToY(TARGET_ALT, h, viewTop);
    if (kline > -20 && kline < h) {
      ctx.strokeStyle = 'rgba(139,233,168,0.55)';
      ctx.setLineDash([8, 8]);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(0, kline);
      ctx.lineTo(w, kline);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = 'rgba(139,233,168,0.9)';
      ctx.font = '600 12px Poppins, sans-serif';
      ctx.fillText('SPACE \u2014 100 km (K\u00e1rm\u00e1n line)', 12, kline - 7);
    }

    if (s.booster) {
      const by = altToY(s.booster.alt, h, viewTop);
      ctx.save();
      ctx.translate(w / 2 + s.booster.x + (is3d ? 22 : 0), by + (is3d ? 10 : 0));
      ctx.rotate(s.booster.t * 0.8);
      ctx.fillStyle = '#8a96a8';
      ctx.fillRect(-4, -10, 8, 20);
      ctx.restore();
    }

    const ry = altToY(s.alt, h, viewTop);
    drawRocket(ctx, w / 2, ry, 1.15, s.flame, s.stage === 1, is3d);

    for (let i = 0; i < confetti.length; i++) {
      const c = confetti[i];
      ctx.globalAlpha = Math.max(0, 1 - c.t / c.life);
      ctx.fillStyle = c.color;
      ctx.fillRect(c.x * w + c.vx * c.t, c.y * h + c.vy * c.t, 5, 5);
    }
    ctx.globalAlpha = 1;

    const gw = Math.min(190, w * 0.34);
    const gh = 74;
    const gx = 12;
    const gy = h - gh - 12;
    ctx.fillStyle = 'rgba(13,24,41,0.78)';
    ctx.fillRect(gx, gy, gw, gh);
    ctx.strokeStyle = 'rgba(255,255,255,0.18)';
    ctx.lineWidth = 1;
    ctx.strokeRect(gx, gy, gw, gh);
    ctx.fillStyle = 'rgba(232,238,251,0.75)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText('Altitude vs time', gx + 8, gy + 14);
    if (s.graph.length > 1) {
      const maxA = Math.max(s.maxAlt, TARGET_ALT * 0.25);
      ctx.strokeStyle = '#7dd3fc';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      for (let i = 0; i < s.graph.length; i++) {
        const px = gx + 8 + (i / Math.max(s.graph.length - 1, 1)) * (gw - 16);
        const py = gy + gh - 8 - (s.graph[i] / maxA) * (gh - 28);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();
    }

    altReadout.set(`${(s.alt / 1000).toFixed(1)} km`);
    velReadout.set(`${Math.round(s.vel)} m/s`);
    fuelReadout.set(`${Math.round((s.fuel / s.fuelStart) * 100)}%`);
    const twr = (thrustKN * 1000 * (s.stage === 2 ? 0.5 : 1)) / (mass() * G0);
    twrReadout.set(s.phase === 'pad' ? `${twr.toFixed(2)} ${twr > 1 ? '\u2014 will fly!' : '\u2014 too heavy!'}` : twr.toFixed(2));
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
