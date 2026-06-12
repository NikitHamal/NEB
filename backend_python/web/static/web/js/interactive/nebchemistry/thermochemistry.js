import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { text, roundRect } from './chem-utils.js';

const ACIDS = {
  hcl: { label: 'HCl (strong acid)', dH: -57.3 },
  acetic: { label: 'CH₃COOH (weak acid)', dH: -55.2 },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Measure 50 mL of each, then mix', '#047857');

  let acidKey = 'hcl';
  let volume = 50;
  let conc = 1.0;
  let mixed = false;
  let temp = 24.0;
  let targetTemp = 24.0;
  let tInitial = null;
  let tFinal = null;
  let mixTime = 0;
  let t = 0;
  const history = [];

  function expectedRise() {
    const moles = conc * (volume / 1000);
    const totalMass = volume * 2;
    const joules = -ACIDS[acidKey].dH * 1000 * moles;
    return joules / (totalMass * 4.18);
  }

  const panel = createPanel(stage, { title: 'Calorimetry' });
  panel.select({
    label: 'Acid',
    options: Object.keys(ACIDS).map((k) => ({ value: k, label: ACIDS[k].label })),
    value: acidKey,
    onChange: (v) => { acidKey = v; reset(); },
  });
  panel.slider({ label: 'Volume of each', min: 25, max: 100, step: 5, value: volume, format: (v) => `${v} mL`, onChange: (v) => { volume = v; reset(); } });
  panel.divider();
  panel.buttonRow([
    { label: 'Record T₁', icon: 'thermostat', onClick: () => {
      tInitial = temp;
      t1Out.set(`${tInitial.toFixed(1)} °C`);
      badge.set(`Initial temperature ${tInitial.toFixed(1)} °C noted`);
      badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
    } },
    { label: 'MIX!', icon: 'science', onClick: mix },
  ]);
  panel.button({ label: 'Record T₂ (at the peak!)', icon: 'thermostat', onClick: () => {
    if (!mixed) {
      badge.set('Mix first!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    tFinal = temp;
    t2Out.set(`${tFinal.toFixed(1)} °C`);
    compute();
  } });
  panel.divider();
  const t1Out = panel.readout({ label: 'T₁ (initial)', value: '—' });
  const t2Out = panel.readout({ label: 'T₂ (final)', value: '—' });
  const dhOut = panel.readout({ label: 'Your ΔH', value: '—' });
  panel.button({ label: 'Reset experiment', icon: 'replay', variant: 'ghost', onClick: reset });
  panel.info('Mix equal volumes of 1.0 M acid and 1.0 M NaOH in the polystyrene cup. Catch T₂ at the peak — wait too long and heat leaks away. Strong acid gives ΔH ≈ −57.3 kJ/mol; weak acids give slightly less. Why?');

  function reset() {
    mixed = false;
    temp = 23.5 + Math.random();
    targetTemp = temp;
    tInitial = null;
    tFinal = null;
    mixTime = 0;
    history.length = 0;
    t1Out.set('—');
    t2Out.set('—');
    dhOut.set('—');
    badge.set('Measure solutions, record T₁, then mix');
    badge.el.style.setProperty('--ix-hud-color', '#047857');
  }

  function mix() {
    if (mixed) return;
    if (tInitial === null) {
      badge.set('Record T₁ before mixing — you can\'t go back!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    mixed = true;
    mixTime = 0;
    targetTemp = temp + expectedRise() + (Math.random() - 0.5) * 0.3;
    badge.set('Mixed! Watch the thermometer climb…');
    badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
  }

  function compute() {
    const rise = tFinal - tInitial;
    const moles = conc * (volume / 1000);
    const mass = volume * 2;
    const q = mass * 4.18 * rise;
    const dH = -q / moles / 1000;
    dhOut.set(`${dH.toFixed(1)} kJ/mol`);
    const ideal = ACIDS[acidKey].dH;
    showInfoCard(stage, {
      title: 'Heat of neutralisation',
      body: `q = m·c·ΔT = ${mass} g × 4.18 × ${rise.toFixed(1)} = ${q.toFixed(0)} J for ${moles.toFixed(3)} mol.\nΔH = −q/n = ${dH.toFixed(1)} kJ/mol (accepted: ${ideal} kJ/mol).\n${acidKey === 'acetic' ? 'Weak acids give a smaller rise: part of the energy is used up ionising the un-dissociated CH₃COOH molecules first.' : 'For any strong acid + strong base the reaction is simply H⁺ + OH⁻ → H₂O, so ΔH is always about −57.3 kJ/mol.'}`,
      color: '#10b981',
    });
    badge.set(`ΔH = ${dH.toFixed(1)} kJ/mol`);
    badge.el.style.setProperty('--ix-hud-color', '#10b981');
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    if (mixed) {
      mixTime += dt;
      if (mixTime < 6) {
        temp += (targetTemp - temp) * dt * 1.1;
      } else {
        temp += (24 - temp) * dt * 0.012;
      }
    }
    if (history.length === 0 || t - history[history.length - 1].t > 0.25) {
      history.push({ t, v: temp });
      if (history.length > 160) history.shift();
    }

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.86;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const cx = w * 0.26;
    ctx.fillStyle = '#f8fafc';
    roundRect(ctx, cx - 44, benchY - 104, 88, 100, 6);
    ctx.fill();
    ctx.fillStyle = '#e2e8f0';
    roundRect(ctx, cx - 38, benchY - 98, 76, 88, 4);
    ctx.fill();
    const mixCol = mixed ? 'rgba(96,165,250,0.5)' : 'rgba(203,213,225,0.4)';
    ctx.fillStyle = mixCol;
    ctx.fillRect(cx - 34, benchY - 64, 68, 50);
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(cx - 44, benchY - 112, 88, 10);
    text(ctx, 'polystyrene cup + lid', cx, benchY + 14);
    text(ctx, mixed ? `${volume} mL acid + ${volume} mL NaOH` : `${volume} mL NaOH waiting`, cx, benchY - 70);

    const tx = cx;
    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(tx - 2, benchY - 168, 4, 102);
    const frac = Math.max(0, Math.min(1, (temp - 20) / 20));
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(tx - 1, benchY - 66 - frac * 96, 2, frac * 96 + 4);
    ctx.beginPath();
    ctx.arc(tx, benchY - 60, 5, 0, Math.PI * 2);
    ctx.fill();
    text(ctx, `${temp.toFixed(1)} °C`, tx + 14, benchY - 150, { align: 'left', color: '#f87171', font: '700 12px Poppins, sans-serif' });

    const g = { x: w * 0.5, y: h * 0.12, w: w * 0.44, h: h * 0.55 };
    ctx.strokeStyle = 'rgba(158,193,255,0.3)';
    ctx.strokeRect(g.x, g.y, g.w, g.h);
    text(ctx, 'temperature vs time', g.x + g.w / 2, g.y - 8);
    for (let temp10 = 20; temp10 <= 40; temp10 += 5) {
      const yy = g.y + g.h - ((temp10 - 20) / 20) * g.h;
      text(ctx, `${temp10}`, g.x - 10, yy + 3, { font: '600 8px Poppins, sans-serif' });
    }
    if (history.length > 1) {
      const t0 = history[0].t;
      const span = Math.max(20, history[history.length - 1].t - t0);
      ctx.strokeStyle = '#f87171';
      ctx.lineWidth = 2;
      ctx.beginPath();
      history.forEach((pt, i) => {
        const xx = g.x + ((pt.t - t0) / span) * g.w;
        const yy = g.y + g.h - Math.max(0, Math.min(1, (pt.v - 20) / 20)) * g.h;
        if (i === 0) ctx.moveTo(xx, yy);
        else ctx.lineTo(xx, yy);
      });
      ctx.stroke();
    }
    if (tInitial !== null) {
      const yy = g.y + g.h - ((tInitial - 20) / 20) * g.h;
      ctx.strokeStyle = 'rgba(251,191,36,0.5)';
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(g.x, yy);
      ctx.lineTo(g.x + g.w, yy);
      ctx.stroke();
      ctx.setLineDash([]);
      text(ctx, 'T₁', g.x + g.w + 10, yy + 3, { color: '#fbbf24' });
    }
    if (mixed && mixTime > 6.5) {
      text(ctx, 'cooling — heat escaping to the room!', g.x + g.w / 2, g.y + g.h + 16, { color: '#f87171' });
    }
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
