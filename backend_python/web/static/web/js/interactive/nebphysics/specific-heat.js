import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, panelBg, labelText } from './lab-utils.js';

const SOLIDS = {
  copper: { label: 'Copper piece', c: 385 },
  aluminium: { label: 'Aluminium piece', c: 900 },
  iron: { label: 'Iron piece', c: 450 },
  brass: { label: 'Brass piece', c: 380 },
};
const C_WATER = 4186;
const C_CAL = 385;
const M_CAL = 0.06;
const ROOM = 20;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Set up the experiment', '#9ec1ff');

  let solidKey = 'copper';
  let mSolid = 0.1;
  let mWater = 0.15;
  let phase = 'setup';
  let solidT = ROOM;
  let waterT = ROOM;
  let heatLoss = true;
  let speed = 5;
  let theta1 = null;
  let theta2 = null;
  let thetaMix = null;
  let revealed = false;
  let peakT = ROOM;

  function reset() {
    phase = 'setup';
    solidT = ROOM;
    waterT = ROOM;
    theta1 = null;
    theta2 = null;
    thetaMix = null;
    revealed = false;
    peakT = ROOM;
  }

  const panel = createPanel(stage, { title: 'Method of Mixtures' });
  panel.select({
    label: 'Solid sample',
    options: Object.entries(SOLIDS).map(([value, s]) => ({ value, label: s.label })),
    value: solidKey,
    onChange: (v) => { solidKey = v; reset(); },
  });
  panel.slider({
    label: 'Solid mass',
    min: 50, max: 200, step: 10, value: 100,
    format: (v) => `${v} g`,
    onChange: (v) => { mSolid = v / 1000; },
  });
  panel.slider({
    label: 'Water mass',
    min: 100, max: 250, step: 10, value: 150,
    format: (v) => `${v} g`,
    onChange: (v) => { mWater = v / 1000; },
  });
  panel.toggle({ label: 'Heat loss to room', value: true, onChange: (v) => { heatLoss = v; } });
  panel.slider({
    label: 'Time speed-up',
    min: 1, max: 10, step: 1, value: 5,
    format: (v) => `×${v}`,
    onChange: (v) => { speed = v; },
  });
  panel.buttonRow([
    { label: 'Heat solid', icon: 'local_fire_department', onClick: () => { if (phase === 'setup') phase = 'heating'; } },
    { label: 'Drop in!', icon: 'colorize', onClick: () => { if (phase === 'heating' && solidT > 95) { theta2 = solidT; phase = 'mixed'; } } },
  ]);
  panel.buttonRow([
    { label: 'Record θ₁', icon: 'push_pin', onClick: () => { if (phase !== 'mixed') theta1 = waterT; } },
    { label: 'Record θ', icon: 'push_pin', onClick: () => { if (phase === 'mixed') thetaMix = waterT; } },
  ]);
  panel.button({ label: 'Reset experiment', icon: 'replay', variant: 'ghost', onClick: reset });
  panel.divider();
  const t1Out = panel.readout({ label: 'θ₁ water initial', value: '—' });
  const t2Out = panel.readout({ label: 'θ₂ solid (hot)', value: '—' });
  const tmOut = panel.readout({ label: 'θ mixture', value: '—' });
  const sOut = panel.readout({ label: 'Computed c (solid)', value: '—' });
  panel.button({ label: 'Reveal true value', icon: 'visibility', onClick: () => { revealed = true; } });
  panel.info('Record θ₁ first. Heat the solid to ~100°C, note θ₂ by pressing Drop in!, stir, and record the HIGHEST mixture temperature before it starts cooling.');

  sim.setUpdate((ctx, dt, w, h) => {
    const sdt = dt * speed;
    if (phase === 'heating') {
      solidT += (100 - solidT) * 0.12 * sdt;
      if (solidT > 99.4) solidT = 99.5 + Math.random() * 0.3;
    }
    if (phase === 'mixed') {
      const cs = SOLIDS[solidKey].c;
      const heatCap = mWater * C_WATER + M_CAL * C_CAL;
      const eq = (mSolid * cs * solidT + heatCap * waterT) / (mSolid * cs + heatCap);
      const rate = 0.25;
      waterT += (eq - waterT) * rate * sdt;
      solidT += (eq - solidT) * rate * 2.2 * sdt;
      if (heatLoss) {
        waterT -= (waterT - ROOM) * 0.006 * sdt;
        solidT -= (solidT - ROOM) * 0.006 * sdt;
      }
      if (waterT > peakT) peakT = waterT;
    }

    ctx.clearRect(0, 0, w, h);
    const calX = w * 0.3;
    const calY = h * 0.46;
    ctx.strokeStyle = '#9ec1ff';
    ctx.lineWidth = 3;
    ctx.strokeRect(calX - 52, calY, 104, 88);
    ctx.strokeStyle = 'rgba(158,193,255,0.4)';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(calX - 62, calY - 8, 124, 104);
    const waterFrac = 0.3 + mWater * 1.6;
    ctx.fillStyle = 'rgba(77,127,255,0.35)';
    ctx.fillRect(calX - 50, calY + 88 - 84 * Math.min(0.95, waterFrac), 100, 84 * Math.min(0.95, waterFrac));
    if (phase === 'mixed') {
      ctx.fillStyle = '#D97706';
      ctx.fillRect(calX - 16, calY + 62, 32, 22);
    }
    labelText(ctx, 'calorimeter + stirrer', calX, calY + 112, { size: 9.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.8)' });

    const heaterX = w * 0.72;
    const heaterY = h * 0.46;
    if (phase !== 'mixed') {
      ctx.strokeStyle = 'rgba(255,140,140,0.8)';
      ctx.lineWidth = 2;
      ctx.strokeRect(heaterX - 40, heaterY, 80, 70);
      ctx.fillStyle = '#D97706';
      ctx.fillRect(heaterX - 16, heaterY + 40, 32, 22);
      if (phase === 'heating') {
        for (let i = 0; i < 5; i++) {
          const fx = heaterX - 28 + i * 14;
          ctx.fillStyle = 'rgba(255,140,60,0.7)';
          ctx.beginPath();
          ctx.arc(fx, heaterY + 78 + Math.sin(performance.now() / 150 + i) * 2, 5, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      labelText(ctx, phase === 'heating' ? `steam heater: ${fmt(solidT, 1)}°C` : 'solid in heater', heaterX, heaterY + 104, { size: 9.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.8)' });
    }

    drawThermo(ctx, w * 0.07, h * 0.12, h * 0.5, waterT, 'water');
    if (phase !== 'mixed') drawThermo(ctx, w * 0.9, h * 0.12, h * 0.28, solidT, 'solid');

    panelBg(ctx, w * 0.18, 12, w * 0.64, 46);
    labelText(ctx, `heat given by solid = heat gained by water + calorimeter`, w * 0.5, 30, { size: 9.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.85)' });
    labelText(ctx, `c = (m_w·c_w + m_c·c_c)(θ−θ₁) / m_s(θ₂−θ)`, w * 0.5, 48, { size: 10, weight: 700, align: 'center', color: '#ffd584' });

    t1Out.set(theta1 === null ? '—' : `${fmt(theta1, 1)} °C`);
    t2Out.set(theta2 === null ? '—' : `${fmt(theta2, 1)} °C`);
    tmOut.set(thetaMix === null ? '—' : `${fmt(thetaMix, 1)} °C`);
    if (theta1 !== null && theta2 !== null && thetaMix !== null && thetaMix > theta1) {
      const heatCap = mWater * C_WATER + M_CAL * C_CAL;
      const c = (heatCap * (thetaMix - theta1)) / (mSolid * (theta2 - thetaMix));
      sOut.set(revealed ? `${fmt(c, 0)} (true ${SOLIDS[solidKey].c}) J/kg·K` : `${fmt(c, 0)} J/kg·K`);
    } else {
      sOut.set('—');
    }
    statusBadge.set(
      phase === 'setup' ? 'Record θ₁, then heat the solid'
        : phase === 'heating' ? (solidT > 95 ? 'Solid at ~100°C — drop it in!' : 'Heating solid…')
          : waterT >= peakT - 0.05 ? 'Mixing — watch for the peak!' : 'Cooling — peak has passed',
    );
  });

  function drawThermo(ctx, x, y, len, temp, label) {
    panelBg(ctx, x - 16, y - 8, 50, len + 42);
    ctx.strokeStyle = 'rgba(232,238,251,0.7)';
    ctx.lineWidth = 1;
    ctx.strokeRect(x, y, 10, len);
    const frac = Math.max(0, Math.min(1, (temp - 0) / 110));
    ctx.fillStyle = temp > 60 ? '#ff8c8c' : '#ffd584';
    ctx.fillRect(x + 1.5, y + len - len * frac, 7, len * frac);
    ctx.beginPath();
    ctx.arc(x + 5, y + len + 7, 8, 0, Math.PI * 2);
    ctx.fill();
    labelText(ctx, `${fmt(temp, 1)}°`, x + 5, y + len + 28, { size: 9.5, align: 'center' });
    labelText(ctx, label, x + 5, y - 12, { size: 8.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.75)' });
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
