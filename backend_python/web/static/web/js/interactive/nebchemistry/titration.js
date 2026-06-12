import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawFlask, drawBurette, drawStand, drawClamp, text } from './chem-utils.js';

const ACID_CONC = 0.1;
const FLASK_VOL = 25;
const BURETTE_VOL = 50;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Step 1: rinse the burette', '#059669');

  const trueConc = 0.08 + Math.random() * 0.05;
  const eqVol = () => (trueConc * FLASK_VOL) / ACID_CONC;

  let step = 0;
  let volume = 0;
  let initialReading = 0;
  let dispensing = false;
  let fast = false;
  let indicator = 'phenolphthalein';
  let swirl = 0;
  const trials = [];
  const drops = [];
  let t = 0;

  const steps = [
    'Rinse burette with HCl',
    'Fill burette with 0.10 M HCl',
    'Pipette 25.0 mL NaOH into flask',
    'Add 2 drops of indicator',
    'Note initial burette reading',
    'Titrate to the endpoint',
  ];

  function excessAcid() {
    return ACID_CONC * volume - trueConc * FLASK_VOL;
  }

  function flaskColor() {
    const ex = excessAcid();
    const eq = eqVol();
    if (indicator === 'phenolphthalein') {
      if (step < 4) return 'rgba(203,213,225,0.18)';
      if (ex >= 0.012) return 'rgba(203,213,225,0.18)';
      const fade = Math.max(0, Math.min(1, (0.012 - ex) / 0.024));
      return `rgba(236,72,153,${0.15 + 0.6 * fade})`;
    }
    if (step < 4) return 'rgba(203,213,225,0.18)';
    if (ex < -0.012) return 'rgba(250,204,21,0.6)';
    if (ex > 0.012) return 'rgba(248,113,113,0.7)';
    const k = (ex + 0.012) / 0.024;
    return `rgba(${Math.round(250 + 5 * k)},${Math.round(204 - 91 * k)},${Math.round(21 + 92 * k)},0.65)`;
  }

  function atEndpoint() {
    const ex = excessAcid();
    return ex >= -0.004 && ex <= 0.012;
  }

  function overshot() {
    return excessAcid() > 0.05;
  }

  const panel = createPanel(stage, { title: 'Titration Bench' });
  const stepOut = panel.readout({ label: 'Current step', value: steps[0] });
  const procBtn = panel.button({ label: 'Do this step', icon: 'play_arrow', onClick: doStep });
  panel.divider();
  panel.select({
    label: 'Indicator',
    options: [
      { value: 'phenolphthalein', label: 'Phenolphthalein' },
      { value: 'methyl', label: 'Methyl orange' },
    ],
    value: indicator,
    onChange: (v) => { indicator = v; },
  });
  const dripBtn = panel.button({ label: 'Hold: add acid (drop)', icon: 'water_drop', onClick: () => {} });
  panel.toggle({ label: 'Fast flow (tap open)', value: false, onChange: (v) => { fast = v; } });
  panel.divider();
  const readOut = panel.readout({ label: 'Burette reading', value: '0.00 mL' });
  const usedOut = panel.readout({ label: 'Acid run in', value: '—' });
  panel.buttonRow([
    { label: 'Record trial', icon: 'edit_note', onClick: recordTrial },
    { label: 'New flask', icon: 'replay', variant: 'ghost', onClick: newFlask },
  ]);
  const resultOut = panel.readout({ label: 'Your NaOH conc.', value: '—' });
  panel.info('Burette: 0.10 M HCl. Flask: 25.0 mL NaOH of unknown concentration. Slow down near the endpoint — one extra drop and the colour is gone for good!');

  function doStep() {
    if (step === 0) {
      step = 1;
      badge.set('Burette rinsed with the acid — no dilution errors now');
    } else if (step === 1) {
      step = 2;
      volume = 0;
      badge.set('Burette filled. Jet below the tap is full — no air bubble');
    } else if (step === 2) {
      step = 3;
      badge.set('25.0 mL of NaOH pipetted into the conical flask');
    } else if (step === 3) {
      step = 4;
      badge.set(indicator === 'phenolphthalein' ? 'Indicator added — solution turns pink (alkaline)' : 'Methyl orange added — solution is yellow (alkaline)');
    } else if (step === 4) {
      step = 5;
      initialReading = volume;
      badge.set(`Initial reading ${initialReading.toFixed(2)} mL. Titrate!`);
    }
    if (step < 5) {
      stepOut.set(steps[step]);
      badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
    } else {
      stepOut.set(steps[5]);
      procBtn.el.style.display = 'none';
    }
  }

  function recordTrial() {
    if (step < 5) {
      badge.set('Finish the setup steps first!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    const used = volume - initialReading;
    if (used < 1) {
      badge.set('You have hardly added any acid yet!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    let verdict;
    if (overshot()) verdict = 'overshot';
    else if (atEndpoint()) verdict = 'good';
    else verdict = 'undershot';
    trials.push({ used, verdict });
    const good = trials.filter((x) => x.verdict === 'good').map((x) => x.used);
    if (verdict === 'good' && good.length >= 2) {
      const avg = good.reduce((a, b) => a + b, 0) / good.length;
      const conc = (ACID_CONC * avg) / FLASK_VOL;
      resultOut.set(`${conc.toFixed(3)} M (true ${trueConc.toFixed(3)})`);
      const err = Math.abs(conc - trueConc) / trueConc * 100;
      showInfoCard(stage, {
        title: 'Concentration calculated!',
        body: `Mean titre = ${avg.toFixed(2)} mL.\nM(NaOH) = M(HCl) × V(HCl) / V(NaOH) = 0.100 × ${avg.toFixed(2)} / 25.0 = ${conc.toFixed(3)} M.\nTrue value: ${trueConc.toFixed(3)} M — your error is ${err.toFixed(1)}%. NaOH + HCl → NaCl + H₂O.`,
        color: '#10b981',
      });
      badge.set(`Result: ${conc.toFixed(3)} M`);
      badge.el.style.setProperty('--ix-hud-color', '#10b981');
    } else if (verdict === 'good') {
      badge.set('Concordant endpoint! Run one more trial');
      badge.el.style.setProperty('--ix-hud-color', '#10b981');
      showInfoCard(stage, { title: 'Trial recorded', body: `Titre = ${used.toFixed(2)} mL, right at the endpoint. Repeat until two concordant titres (within 0.2 mL) — then average them.`, color: '#10b981' });
    } else if (verdict === 'overshot') {
      badge.set('Overshot! This trial is rough only');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      showInfoCard(stage, { title: 'Overshot the endpoint', body: `You added ${used.toFixed(2)} mL but the colour vanished well before that. Use this as a rough trial: next time add fast until ~2 mL before, then drop by drop.`, color: '#ef4444' });
    } else {
      badge.set('Endpoint not reached yet');
      badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
    }
  }

  function newFlask() {
    if (step >= 5) {
      step = 2;
      stepOut.set(steps[2]);
      procBtn.el.style.display = '';
      badge.set('Fresh flask: pipette 25.0 mL NaOH again');
      badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
    }
  }

  function startDrip(e) { if (step >= 5) dispensing = true; e.preventDefault(); }
  function stopDrip() { dispensing = false; }
  dripBtn.el.addEventListener('pointerdown', startDrip);
  dripBtn.el.addEventListener('pointerup', stopDrip);
  dripBtn.el.addEventListener('pointercancel', stopDrip);
  dripBtn.el.addEventListener('pointerleave', stopDrip);

  let dropTimer = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    const benchY = h * 0.88;
    const standX = w * 0.18;
    const bx = w * 0.46;
    const bTop = h * 0.06;
    const bBot = h * 0.46;

    if (dispensing && volume < BURETTE_VOL && step >= 5) {
      const rate = fast ? 2.2 : 0.18;
      volume = Math.min(BURETTE_VOL, volume + rate * dt);
      swirl = 1;
      dropTimer += dt;
      if (dropTimer > (fast ? 0.06 : 0.3)) {
        dropTimer = 0;
        drops.push({ x: bx, y: bBot + 12, v: 30 });
      }
    }
    swirl = Math.max(0, swirl - dt * 0.6);

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    drawStand(ctx, standX, bTop - 4, benchY - 2);
    drawClamp(ctx, standX, h * 0.12, bx - 8);
    drawBurette(ctx, bx, bTop, bBot, step >= 2 ? (BURETTE_VOL - volume) / BURETTE_VOL : 0, 'rgba(186,230,253,0.5)', 50);
    text(ctx, '0.10 M HCl', bx + 38, bTop + 10, { align: 'left' });

    const fy = benchY - 4;
    const wob = swirl > 0 ? Math.sin(t * 10) * 3 * swirl : 0;
    ctx.save();
    ctx.translate(wob, 0);
    drawFlask(ctx, bx, fy, 86, 92, step >= 3 ? 0.55 : 0, flaskColor(), step >= 3 ? '25.0 mL NaOH + indicator' : 'empty conical flask');
    ctx.restore();

    ctx.fillStyle = 'rgba(186,230,253,0.9)';
    for (let i = drops.length - 1; i >= 0; i--) {
      const d = drops[i];
      d.v += 300 * dt;
      d.y += d.v * dt;
      if (d.y >= fy - 50) { drops.splice(i, 1); continue; }
      ctx.beginPath();
      ctx.arc(d.x, d.y, 2.6, 0, Math.PI * 2);
      ctx.fill();
    }

    const gx = w * 0.66;
    const gy = h * 0.08;
    const gw = w * 0.3;
    text(ctx, 'Trials', gx + gw / 2, gy, { font: '700 11px Poppins, sans-serif', color: '#e2e8f0' });
    trials.slice(-6).forEach((tr, i) => {
      const yy = gy + 18 + i * 17;
      const col = tr.verdict === 'good' ? '#34d399' : tr.verdict === 'overshot' ? '#f87171' : '#fbbf24';
      text(ctx, `#${trials.length - Math.min(6, trials.length) + i + 1}  ${tr.used.toFixed(2)} mL  ${tr.verdict}`, gx, yy, { align: 'left', color: col });
    });
    if (!trials.length) text(ctx, 'no trials yet', gx, gy + 18, { align: 'left' });

    if (step >= 5) {
      const ex = excessAcid();
      let msg, col;
      if (ex < -0.15) { msg = 'still alkaline — keep adding'; col = '#9ec1ff'; }
      else if (ex < -0.02) { msg = 'getting close — drop by drop now!'; col = '#fbbf24'; }
      else if (atEndpoint()) { msg = 'ENDPOINT — stop and record!'; col = '#34d399'; }
      else { msg = 'overshot the endpoint'; col = '#f87171'; }
      text(ctx, msg, bx, fy + 28, { color: col, font: '700 11px Poppins, sans-serif' });
      badge.set(`${(volume - initialReading).toFixed(2)} mL in · ${msg}`);
      badge.el.style.setProperty('--ix-hud-color', col);
    }

    readOut.set(`${volume.toFixed(2)} mL`);
    usedOut.set(step >= 5 ? `${(volume - initialReading).toFixed(2)} mL` : '—');
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
