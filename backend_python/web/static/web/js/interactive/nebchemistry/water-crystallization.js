import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawBurner, text, roundRect } from './chem-utils.js';

const M_CUSO4 = 159.6;
const M_H2O = 18.0;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Weigh the empty crucible first', '#059669');

  const crucibleMass = 24.6 + Math.random() * 1.4;
  const sampleMass = 2.2 + Math.random() * 1.2;
  const trueX = 5;
  const waterMass = sampleMass * (trueX * M_H2O) / (M_CUSO4 + trueX * M_H2O);

  let onBalance = 'crucible';
  let sampleAdded = false;
  let heatProgress = 0;
  let heating = false;
  let coolTimer = 0;
  let readings = [];
  let t = 0;

  function currentSampleMass() {
    return sampleMass - waterMass * Math.min(1, heatProgress);
  }

  function balanceReading() {
    if (onBalance === 'nothing') return 0;
    if (!sampleAdded) return crucibleMass;
    return crucibleMass + currentSampleMass();
  }

  const panel = createPanel(stage, { title: 'Gravimetric Bench' });
  const massOut = panel.readout({ label: 'Balance', value: '0.00 g' });
  panel.divider();
  panel.button({ label: 'Add hydrated CuSO₄·xH₂O', icon: 'colorize', onClick: () => {
    if (sampleAdded) return;
    sampleAdded = true;
    badge.set('Blue crystals added. Record the mass, then heat!');
    badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
  } });
  panel.buttonRow([
    { label: 'Heat 1 min', icon: 'local_fire_department', onClick: () => heatFor(0.34) },
    { label: 'Heat 3 min', icon: 'whatshot', onClick: () => heatFor(1.0) },
  ]);
  panel.button({ label: 'Record balance reading', icon: 'edit_note', onClick: record });
  panel.divider();
  const lastOut = panel.readout({ label: 'Last reading', value: '—' });
  const lossOut = panel.readout({ label: 'Water lost so far', value: '—' });
  const xOut = panel.readout({ label: 'Computed x', value: '—' });
  panel.button({ label: 'Start over', icon: 'replay', variant: 'ghost', onClick: resetAll });
  panel.info('Heat, cool, weigh — and repeat until two consecutive readings agree within 0.02 g. That is "heating to constant mass": only then has ALL the water gone.');

  function heatFor(amount) {
    if (!sampleAdded) {
      badge.set('Nothing in the crucible yet!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    heating = true;
    coolTimer = 0;
    const target = Math.min(1.15, heatProgress + amount);
    const interval = setInterval(() => {
      heatProgress = Math.min(target, heatProgress + 0.04);
      if (heatProgress >= target) {
        clearInterval(interval);
        heating = false;
        badge.set('Heating done — let it cool in a desiccator, then weigh');
        badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
      }
    }, 120);
    timers.push(interval);
    badge.set('Heating… blue crystals turning white');
    badge.el.style.setProperty('--ix-hud-color', '#ef4444');
  }

  function record() {
    if (heating) {
      badge.set('Never weigh a hot crucible — air currents lift it and you burn the pan!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    const m = balanceReading();
    readings.push(m);
    lastOut.set(`${m.toFixed(2)} g`);
    if (!sampleAdded || readings.length < 2) {
      badge.set('Reading recorded');
      badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
      return;
    }
    const initial = crucibleMass + sampleMass;
    const lost = initial - m;
    lossOut.set(`${Math.max(0, lost).toFixed(2)} g`);
    const prev = readings[readings.length - 2];
    if (Math.abs(m - prev) <= 0.02 && heatProgress >= 0.99) {
      const anhydrous = m - crucibleMass;
      const molesSalt = anhydrous / M_CUSO4;
      const molesWater = lost / M_H2O;
      const x = molesWater / molesSalt;
      xOut.set(x.toFixed(2));
      badge.set(`Constant mass! x ≈ ${x.toFixed(2)}`);
      badge.el.style.setProperty('--ix-hud-color', '#10b981');
      showInfoCard(stage, {
        title: 'Constant mass reached',
        body: `Water lost = ${lost.toFixed(2)} g (${molesWater.toFixed(4)} mol). Anhydrous CuSO₄ = ${anhydrous.toFixed(2)} g (${molesSalt.toFixed(4)} mol).\nx = mol H₂O / mol CuSO₄ = ${x.toFixed(2)} → formula CuSO₄·5H₂O.\nCuSO₄·5H₂O --heat--> CuSO₄ + 5H₂O↑`,
        color: '#10b981',
      });
    } else if (heatProgress < 0.99) {
      badge.set('Mass still falling — water remains. Heat again!');
      badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
    } else {
      badge.set('Two readings agree? Compare with the previous one');
      badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
    }
  }

  function resetAll() {
    sampleAdded = false;
    heatProgress = 0;
    heating = false;
    readings = [];
    lastOut.set('—');
    lossOut.set('—');
    xOut.set('—');
    badge.set('Weigh the empty crucible first');
    badge.el.style.setProperty('--ix-hud-color', '#059669');
  }

  const timers = [];

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.84;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const bx = w * 0.7;
    ctx.fillStyle = '#334155';
    roundRect(ctx, bx - 56, benchY - 30, 112, 28, 5);
    ctx.fill();
    ctx.fillStyle = '#0f172a';
    roundRect(ctx, bx - 48, benchY - 24, 62, 16, 3);
    ctx.fill();
    text(ctx, `${balanceReading().toFixed(2)} g`, bx - 17, benchY - 12, { color: '#34d399', font: '700 11px monospace', align: 'center' });
    ctx.fillStyle = '#475569';
    ctx.fillRect(bx - 40, benchY - 36, 80, 5);
    text(ctx, 'electronic balance', bx, benchY + 14);

    const cx = w * 0.26;
    drawBurner(ctx, cx, benchY, t, heating, '#60a5fa', 36);
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(cx - 26, benchY - 2);
    ctx.lineTo(cx - 19, benchY - 52);
    ctx.lineTo(cx + 19, benchY - 52);
    ctx.lineTo(cx + 26, benchY - 2);
    ctx.stroke();
    const cruY = benchY - 64;
    ctx.strokeStyle = 'rgba(229,231,235,0.85)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx - 20, cruY);
    ctx.lineTo(cx - 14, cruY + 13);
    ctx.lineTo(cx + 14, cruY + 13);
    ctx.lineTo(cx + 20, cruY);
    ctx.stroke();
    if (sampleAdded) {
      const blue = Math.max(0, 1 - heatProgress);
      const r = Math.round(59 + (241 - 59) * (1 - blue));
      const gg = Math.round(130 + (245 - 130) * (1 - blue));
      const b = Math.round(246 + (249 - 246) * (1 - blue));
      ctx.fillStyle = `rgb(${r},${gg},${b})`;
      ctx.fillRect(cx - 12, cruY + 5, 24, 7);
      text(ctx, blue > 0.6 ? 'blue crystals (hydrated)' : blue > 0.05 ? 'turning pale…' : 'white powder (anhydrous)', cx, cruY - 10, { color: blue > 0.5 ? '#60a5fa' : '#e2e8f0' });
    } else {
      text(ctx, 'empty crucible', cx, cruY - 10);
    }
    if (heating) {
      text(ctx, 'steam ', cx + 30, cruY - 26, { color: '#94a3b8' });
      ctx.strokeStyle = `rgba(203,213,225,${0.4 + 0.2 * Math.sin(t * 5)})`;
      ctx.lineWidth = 1.5;
      for (let i = -1; i <= 1; i++) {
        ctx.beginPath();
        ctx.moveTo(cx + i * 9, cruY);
        ctx.quadraticCurveTo(cx + i * 9 + 5, cruY - 16, cx + i * 9, cruY - 30);
        ctx.stroke();
      }
    }

    text(ctx, 'Readings (g)', w * 0.06, h * 0.1, { align: 'left', font: '700 11px Poppins, sans-serif', color: '#e2e8f0' });
    readings.slice(-6).forEach((r, i) => {
      text(ctx, `#${readings.length - Math.min(6, readings.length) + i + 1}: ${r.toFixed(2)}`, w * 0.06, h * 0.1 + 16 + i * 14, { align: 'left', color: '#9ec1ff' });
    });

    massOut.set(`${balanceReading().toFixed(2)} g`);
  });

  sim.start();

  return {
    dispose() {
      timers.forEach(clearInterval);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
