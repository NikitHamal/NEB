import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawFlask, drawBurette, drawStand, drawClamp, drawBurner, text } from './chem-utils.js';

const OXALIC_CONC = 0.05;
const FLASK_VOL = 25;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Pipette 25.0 mL oxalic acid', '#047857');

  const trueKMnO4 = 0.018 + Math.random() * 0.006;
  const eqVol = () => (2 / 5) * (OXALIC_CONC * FLASK_VOL) / trueKMnO4;

  let flaskReady = false;
  let temp = 25;
  let heaterOn = false;
  let volume = 0;
  let dispensing = false;
  let fast = false;
  const trials = [];
  const drops = [];
  let t = 0;

  function excessMnO4() {
    return trueKMnO4 * volume - (2 / 5) * OXALIC_CONC * FLASK_VOL;
  }

  function flaskColor() {
    if (!flaskReady) return 'rgba(203,213,225,0.0)';
    if (temp < 55) {
      const pink = Math.min(0.65, volume * 0.06);
      return `rgba(192,38,211,${pink})`;
    }
    const ex = excessMnO4();
    if (ex <= 0) return 'rgba(203,213,225,0.15)';
    return `rgba(192,38,211,${Math.min(0.7, 0.18 + ex * 18)})`;
  }

  function atEndpoint() {
    const ex = excessMnO4();
    return temp >= 55 && ex > 0 && ex <= 0.012;
  }

  const panel = createPanel(stage, { title: 'KMnO₄ Standardisation' });
  panel.button({ label: 'Pipette 25.0 mL oxalic acid', icon: 'colorize', onClick: () => {
    flaskReady = true;
    volume = 0;
    badge.set('Flask charged: 0.05 M oxalic acid + dil. H₂SO₄');
    badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
  } });
  panel.toggle({ label: 'Heat flask (60–70 °C)', value: false, onChange: (v) => { heaterOn = v; } });
  const tempOut = panel.readout({ label: 'Flask temperature', value: '25 °C' });
  panel.divider();
  const dripBtn = panel.button({ label: 'Hold: run in KMnO₄', icon: 'water_drop', onClick: () => {} });
  panel.toggle({ label: 'Fast flow', value: false, onChange: (v) => { fast = v; } });
  const volOut = panel.readout({ label: 'KMnO₄ added', value: '0.00 mL' });
  panel.buttonRow([
    { label: 'Record trial', icon: 'edit_note', onClick: record },
    { label: 'New flask', icon: 'replay', variant: 'ghost', onClick: () => {
      flaskReady = false;
      volume = 0;
      badge.set('Pipette a fresh 25.0 mL portion');
      badge.el.style.setProperty('--ix-hud-color', '#047857');
    } },
  ]);
  const resOut = panel.readout({ label: 'Your KMnO₄ molarity', value: '—' });
  panel.info('KMnO₄ is self-indicating: purple while unreacted, colourless once reduced to Mn²⁺. The endpoint is the FIRST permanent pale pink. Heat to 60–70 °C or the reaction is too slow and colour lingers falsely.');

  function record() {
    if (!flaskReady || volume < 1) {
      badge.set('Run the titration first!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    if (temp < 55) {
      badge.set('Cold flask: pink stayed from the start — invalid trial!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      showInfoCard(stage, { title: 'Invalid trial — flask too cold', body: 'Below ~60 °C the MnO₄⁻/oxalate reaction is very slow, so purple colour persists even before the true endpoint. Heat the flask to 60–70 °C and repeat.', color: '#ef4444' });
      return;
    }
    const ex = excessMnO4();
    let verdict = atEndpoint() ? 'good' : ex <= 0 ? 'undershot' : 'overshot';
    trials.push({ used: volume, verdict });
    const good = trials.filter((x) => x.verdict === 'good').map((x) => x.used);
    if (verdict === 'good' && good.length >= 2) {
      const avg = good.reduce((a, b) => a + b, 0) / good.length;
      const conc = (2 / 5) * (OXALIC_CONC * FLASK_VOL) / avg;
      resOut.set(`${conc.toFixed(4)} M (true ${trueKMnO4.toFixed(4)})`);
      showInfoCard(stage, {
        title: 'KMnO₄ standardised!',
        body: `2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O.\nMole ratio MnO₄⁻ : C₂O₄²⁻ = 2 : 5.\nM(KMnO₄) = (2/5) × 0.050 × 25.0 / ${avg.toFixed(2)} = ${conc.toFixed(4)} M.\nTrue value ${trueKMnO4.toFixed(4)} M.`,
        color: '#10b981',
      });
      badge.set(`Standardised: ${conc.toFixed(4)} M`);
      badge.el.style.setProperty('--ix-hud-color', '#10b981');
    } else if (verdict === 'good') {
      badge.set('Good endpoint — one more concordant trial!');
      badge.el.style.setProperty('--ix-hud-color', '#10b981');
    } else if (verdict === 'overshot') {
      badge.set('Deep pink — overshot. Rough trial only');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
    } else {
      badge.set('Still colourless — endpoint not reached');
      badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
    }
  }

  function startDrip(e) { if (flaskReady) dispensing = true; e.preventDefault(); }
  function stopDrip() { dispensing = false; }
  dripBtn.el.addEventListener('pointerdown', startDrip);
  dripBtn.el.addEventListener('pointerup', stopDrip);
  dripBtn.el.addEventListener('pointercancel', stopDrip);
  dripBtn.el.addEventListener('pointerleave', stopDrip);

  let dropTimer = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    temp += ((heaterOn ? 68 : 25) - temp) * dt * 0.18;
    if (dispensing && volume < 50) {
      volume = Math.min(50, volume + (fast ? 1.8 : 0.15) * dt);
      dropTimer += dt;
      if (dropTimer > (fast ? 0.07 : 0.32)) {
        dropTimer = 0;
        drops.push({ x: w * 0.46, y: h * 0.48, v: 30 });
      }
    }

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.88;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const standX = w * 0.16;
    const bx = w * 0.46;
    drawStand(ctx, standX, h * 0.04, benchY - 2);
    drawClamp(ctx, standX, h * 0.1, bx - 7);
    drawBurette(ctx, bx, h * 0.05, h * 0.44, (50 - volume) / 50, 'rgba(147,51,234,0.65)', 50);
    text(ctx, 'KMnO₄ (unknown M)', bx + 36, h * 0.08, { align: 'left', color: '#c084fc' });

    drawBurner(ctx, bx, benchY, t, heaterOn, '#60a5fa', 26);
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(bx - 28, benchY - 2);
    ctx.lineTo(bx - 21, benchY - 42);
    ctx.lineTo(bx + 21, benchY - 42);
    ctx.lineTo(bx + 28, benchY - 2);
    ctx.stroke();
    drawFlask(ctx, bx, benchY - 46, 82, 84, flaskReady ? 0.55 : 0, flaskColor(), flaskReady ? 'oxalic acid + H₂SO₄' : 'empty flask');

    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(bx + 52, benchY - 120, 4, 76);
    const mercH = Math.min(70, ((temp - 20) / 60) * 70);
    ctx.fillStyle = temp >= 55 && temp <= 75 ? '#34d399' : '#f87171';
    ctx.fillRect(bx + 53, benchY - 46 - mercH, 2, mercH);
    text(ctx, `${Math.round(temp)} °C`, bx + 70, benchY - 80, { align: 'left', color: temp >= 55 ? '#34d399' : '#f87171' });

    ctx.fillStyle = 'rgba(192,38,211,0.9)';
    for (let i = drops.length - 1; i >= 0; i--) {
      const d = drops[i];
      d.v += 300 * dt;
      d.y += d.v * dt;
      if (d.y >= benchY - 90) { drops.splice(i, 1); continue; }
      ctx.beginPath();
      ctx.arc(d.x, d.y, 2.6, 0, Math.PI * 2);
      ctx.fill();
    }

    const gx = w * 0.68;
    text(ctx, 'Trials', gx, h * 0.08, { align: 'left', font: '700 11px Poppins, sans-serif', color: '#e2e8f0' });
    trials.slice(-6).forEach((tr, i) => {
      const col = tr.verdict === 'good' ? '#34d399' : tr.verdict === 'overshot' ? '#f87171' : '#fbbf24';
      text(ctx, `${tr.used.toFixed(2)} mL — ${tr.verdict}`, gx, h * 0.08 + 16 + i * 15, { align: 'left', color: col });
    });

    if (flaskReady && volume > 0) {
      let msg, col;
      if (temp < 55) { msg = 'too cold — colour misleading!'; col = '#f87171'; }
      else if (excessMnO4() <= -0.05) { msg = 'decolourising instantly — keep going'; col = '#9ec1ff'; }
      else if (excessMnO4() <= 0) { msg = 'colour fading slowly — dropwise!'; col = '#fbbf24'; }
      else if (atEndpoint()) { msg = 'permanent pale pink — ENDPOINT'; col = '#34d399'; }
      else { msg = 'deep pink — overshot'; col = '#f87171'; }
      text(ctx, msg, bx, benchY + 16, { color: col, font: '700 10.5px Poppins, sans-serif' });
      badge.set(`${volume.toFixed(2)} mL · ${msg}`);
      badge.el.style.setProperty('--ix-hud-color', col);
    }

    tempOut.set(`${Math.round(temp)} °C`);
    volOut.set(`${volume.toFixed(2)} mL`);
  });

  sim.start();

  return {
    dispose() {
      dripBtn.el.removeEventListener('pointerdown', startDrip);
      dripBtn.el.removeEventListener('pointerup', stopDrip);
      dripBtn.el.removeEventListener('pointercancel', stopDrip);
      dripBtn.el.removeEventListener('pointerleave', stopDrip);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
