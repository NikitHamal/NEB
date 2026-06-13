import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const WORLDS = {
  moon: { name: 'Moon', g: 1.62, ground: '#9aa1ad', sky: ['#05070d', '#10141f'], accent: '#c9d1dd' },
  mercury: { name: 'Mercury', g: 3.7, ground: '#8d7f72', sky: ['#05070d', '#181410'], accent: '#c9b8a6' },
  mars: { name: 'Mars', g: 3.71, ground: '#a3502f', sky: ['#2b1810', '#5a3322'], accent: '#e0824f' },
  venus: { name: 'Venus', g: 8.87, ground: '#9c8348', sky: ['#4a3a14', '#8a702e'], accent: '#e6c98e' },
  earth: { name: 'Earth', g: 9.81, ground: '#3f6b4f', sky: ['#1d4e89', '#4f8fd0'], accent: '#86efac' },
  jupiter: { name: 'Jupiter (cloud tops)', g: 24.79, ground: '#b08a5e', sky: ['#43301c', '#7a5c38'], accent: '#e8c9a0' },
  sun: { name: 'Sun (surface!)', g: 274, ground: '#d97b1f', sky: ['#7a3208', '#cf6a12'], accent: '#ffd27a' },
};

const DROP_HEIGHT = 10;

export default function init(stage) {
  const sim = createCanvas2D(stage);

  let worldKey = 'moon';
  let earthWeight = 45;
  let ball = { h: DROP_HEIGHT, v: 0, falling: false, landedT: 0, bounces: 0 };
  let timer = 0;
  let running = false;
  let viewMode = '2d';

  function world() { return WORLDS[worldKey]; }

  function weightThere() {
    return earthWeight * (world().g / 9.81);
  }

  function fallTime() {
    return Math.sqrt((2 * DROP_HEIGHT) / world().g);
  }

  function drop() {
    ball = { h: DROP_HEIGHT, v: 0, falling: true, landedT: 0, bounces: 0 };
    timer = 0;
    running = true;
    timeBadge.set('Falling\u2026');
  }

  const hud = createHud(stage);
  const worldBadge = hud.badge('Moon \u2014 g = 1.62 m/s\u00b2', '#c9d1dd');
  const timeBadge = hud.badge('Press DROP', '#9ec1ff');

  const panel = createPanel(stage, { title: 'Weight Lab' });
  panel.select({
    label: 'View',
    options: [
      { value: '2d', label: '2D' },
      { value: '3d', label: '3D' },
    ],
    value: viewMode,
    onChange: (v) => { viewMode = v; },
  });
  panel.select({
    label: 'Pick a world',
    options: Object.keys(WORLDS).map((k) => ({ value: k, label: WORLDS[k].name })),
    value: worldKey,
    onChange: (v) => {
      worldKey = v;
      const wd = world();
      worldBadge.set(`${wd.name} \u2014 g = ${wd.g} m/s\u00b2`);
      worldBadge.el.style.setProperty('--ix-hud-color', wd.accent);
      updateReadouts();
      drop();
    },
  });
  panel.slider({
    label: 'Your weight on Earth',
    min: 20, max: 120, step: 1, value: earthWeight,
    format: (v) => `${v} kg`,
    onChange: (v) => { earthWeight = v; updateReadouts(); },
  });
  const weightReadout = panel.readout({ label: 'Weight here', value: '' });
  const newtonReadout = panel.readout({ label: 'In newtons', value: '' });
  const fallReadout = panel.readout({ label: '10 m fall time', value: '' });
  panel.button({ label: 'DROP the ball', icon: 'arrow_downward', onClick: drop });
  panel.info('Your mass never changes \u2014 only the pull of gravity does. Weight = mass \u00d7 g. Compare how the same 10 m drop feels on each world.');

  function updateReadouts() {
    weightReadout.set(`${weightThere().toFixed(1)} kg-force`);
    newtonReadout.set(`${Math.round(weightThere() * 9.81)} N`);
    fallReadout.set(`${fallTime().toFixed(2)} s`);
  }
  updateReadouts();

  sim.setUpdate((ctx, dt, w, h) => {
    const wd = world();
    const is3d = viewMode === '3d';
    if (running && ball.falling) {
      timer += dt;
      ball.v += wd.g * dt;
      ball.h -= ball.v * dt;
      if (ball.h <= 0) {
        ball.h = 0;
        if (ball.bounces === 0) timeBadge.set(`Landed in ${timer.toFixed(2)} s!`);
        if (Math.abs(ball.v) > wd.g * 0.12 && ball.bounces < 5) {
          ball.v = -ball.v * 0.45;
          ball.bounces++;
        } else {
          ball.falling = false;
          running = false;
        }
      }
    }

    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, wd.sky[0]);
    grad.addColorStop(1, wd.sky[1]);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    if (worldKey === 'moon' || worldKey === 'mercury') {
      ctx.fillStyle = 'rgba(220,228,240,0.7)';
      for (let i = 0; i < 40; i++) {
        const sx = ((i * 97) % 100) / 100 * w;
        const sy = ((i * 61) % 67) / 100 * h;
        ctx.fillRect(sx, sy, 1.4, 1.4);
      }
    }

    const groundY = h * 0.82;
    ctx.fillStyle = wd.ground;
    if (is3d) {
      ctx.beginPath();
      ctx.moveTo(0, groundY);
      ctx.lineTo(w, groundY);
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,0.1)';
      ctx.beginPath();
      ctx.moveTo(w * 0.12, groundY + 10);
      ctx.lineTo(w * 0.88, groundY + 10);
      ctx.lineTo(w * 0.72, h);
      ctx.lineTo(w * 0.28, h);
      ctx.closePath();
      ctx.fill();
    } else {
      ctx.fillRect(0, groundY, w, h - groundY);
    }
    ctx.fillStyle = 'rgba(0,0,0,0.18)';
    for (let i = 0; i < 6; i++) {
      const bx = ((i * 173) % 100) / 100 * w;
      ctx.beginPath();
      ctx.ellipse(bx, groundY + 14 + ((i * 37) % 30), 16, 5, 0, 0, Math.PI * 2);
      ctx.fill();
    }

    const towerX = w * 0.26;
    const scaleTop = h * 0.12;
    const pxPerM = (groundY - scaleTop) / DROP_HEIGHT;
    ctx.strokeStyle = 'rgba(232,238,251,0.5)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(towerX, scaleTop);
    ctx.lineTo(towerX, groundY);
    if (is3d) {
      ctx.moveTo(towerX + 16, scaleTop + 10);
      ctx.lineTo(towerX + 16, groundY + 8);
      ctx.moveTo(towerX, scaleTop);
      ctx.lineTo(towerX + 16, scaleTop + 10);
      ctx.moveTo(towerX, groundY);
      ctx.lineTo(towerX + 16, groundY + 8);
    }
    ctx.stroke();
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillStyle = 'rgba(232,238,251,0.7)';
    ctx.textAlign = 'right';
    for (let m = 0; m <= DROP_HEIGHT; m += 2) {
      const y = groundY - m * pxPerM;
      ctx.beginPath();
      ctx.moveTo(towerX - 6, y);
      ctx.lineTo(towerX, y);
      ctx.stroke();
      ctx.fillText(`${m} m`, towerX - 10, y + 3);
    }
    ctx.textAlign = 'left';

    const ballX = towerX + 36;
    const ballY = groundY - ball.h * pxPerM - 10 + (is3d ? 4 : 0);
    ctx.fillStyle = 'rgba(0,0,0,0.3)';
    ctx.beginPath();
    ctx.ellipse(ballX + (is3d ? 12 : 0), groundY + (is3d ? 11 : 3), 12 * Math.max(0.4, 1 - ball.h / DROP_HEIGHT), is3d ? 3 : 4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#f9a8d4';
    ctx.beginPath();
    ctx.arc(ballX, ballY, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.55)';
    ctx.beginPath();
    ctx.arc(ballX - 3, ballY - 3, 3, 0, Math.PI * 2);
    ctx.fill();

    const px = w * 0.62;
    const py = groundY + (is3d ? 8 : 0);
    ctx.strokeStyle = '#e8eefb';
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    const squash = wd.g > 20 ? 6 : 0;
    ctx.beginPath();
    ctx.arc(px, py - 58 + squash, 9, 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(px, py - 49 + squash);
    ctx.lineTo(px, py - 22 + squash * 0.5);
    ctx.moveTo(px, py - 42 + squash);
    ctx.lineTo(px - 14, py - 30 + squash);
    ctx.moveTo(px, py - 42 + squash);
    ctx.lineTo(px + 14, py - 30 + squash);
    ctx.moveTo(px, py - 22 + squash * 0.5);
    ctx.lineTo(px - 10, py);
    ctx.moveTo(px, py - 22 + squash * 0.5);
    ctx.lineTo(px + 10, py);
    ctx.stroke();

    ctx.fillStyle = 'rgba(13,24,41,0.7)';
    const tag = `${weightThere().toFixed(0)} kg-force here`;
    ctx.font = '700 12px Poppins, sans-serif';
    const tw = ctx.measureText(tag).width;
    ctx.fillRect(px - tw / 2 - 8, py - 92, tw + 16, 22);
    ctx.fillStyle = wd.accent;
    ctx.textAlign = 'center';
    ctx.fillText(tag, px, py - 77);
    ctx.fillStyle = 'rgba(232,238,251,0.85)';
    ctx.font = '700 14px Poppins, sans-serif';
    ctx.fillText(wd.name, w / 2, h * 0.07);
    ctx.textAlign = 'left';
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
