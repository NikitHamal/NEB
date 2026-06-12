import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawBeaker, drawFlask, drawBurner, drawStand, makeBubbles, text, GLASS } from './chem-utils.js';

const MIXTURES = {
  sandsalt: {
    label: 'Sand + salt + water',
    steps: ['filtration', 'evaporation'],
    parts: ['sand (insoluble)', 'salt (dissolved)', 'water'],
    done: 'Sand collected on the filter paper, salt recovered as crystals from the evaporating dish. Mixture fully separated!',
  },
  ink: {
    label: 'Black ink (mixed dyes)',
    steps: ['chromatography'],
    parts: ['several coloured dyes'],
    done: 'The dyes travelled different distances up the paper and separated into coloured spots — that is paper chromatography.',
  },
  naphthalene: {
    label: 'Naphthalene + salt',
    steps: ['sublimation'],
    parts: ['naphthalene (sublimes)', 'salt (stable)'],
    done: 'Naphthalene turned straight to vapour and re-formed as crystals on the cold watch glass. Salt stayed behind.',
  },
  muddy: {
    label: 'Muddy water',
    steps: ['filtration'],
    parts: ['mud (insoluble)', 'water'],
    done: 'Mud stayed on the filter paper as residue; clear water passed through as the filtrate.',
  },
  saltwater: {
    label: 'Salt solution (pure water wanted)',
    steps: ['distillation'],
    parts: ['salt (dissolved)', 'water'],
    done: 'Water boiled, the vapour condensed in the condenser and pure distilled water collected. Salt remained in the flask.',
  },
};

const TECHNIQUES = {
  filtration: { label: 'Filtration', why: 'Separates an insoluble solid from a liquid using filter paper in a funnel.' },
  evaporation: { label: 'Evaporation', why: 'Heats a solution so the solvent escapes, leaving dissolved solid as crystals.' },
  sublimation: { label: 'Sublimation', why: 'Heats a solid that turns straight to vapour (no liquid stage) and re-condenses on a cold surface.' },
  distillation: { label: 'Distillation', why: 'Boils a liquid, then condenses the vapour back — collects the pure solvent.' },
  chromatography: { label: 'Chromatography', why: 'Solvent climbs paper, carrying dyes different distances by their solubility.' },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Pick a mixture, then a technique', '#059669');
  const bubbles = makeBubbles(28);

  let mixKey = 'sandsalt';
  let stepIdx = 0;
  let anim = null;
  let animT = 0;
  let doneSteps = [];
  let t = 0;

  const panel = createPanel(stage, { title: 'Separation Lab' });
  panel.select({
    label: 'Mixture',
    options: Object.keys(MIXTURES).map((k) => ({ value: k, label: MIXTURES[k].label })),
    value: mixKey,
    onChange: (v) => { mixKey = v; reset(); },
  });
  panel.divider();
  panel.section('Apply a technique');
  panel.buttonRow([
    { label: 'Filter', icon: 'filter_alt', onClick: () => attempt('filtration') },
    { label: 'Evaporate', icon: 'heat', onClick: () => attempt('evaporation') },
  ]);
  panel.buttonRow([
    { label: 'Sublime', icon: 'air', onClick: () => attempt('sublimation') },
    { label: 'Distil', icon: 'water_full', onClick: () => attempt('distillation') },
  ]);
  panel.button({ label: 'Chromatography', icon: 'gradient', onClick: () => attempt('chromatography') });
  panel.divider();
  const stepOut = panel.readout({ label: 'Progress', value: 'step 1' });
  panel.button({ label: 'Reset mixture', icon: 'replay', variant: 'ghost', onClick: reset });
  panel.info('Choose the right technique for each stage. Wrong choices waste the sample — think about what each component can and cannot do!');

  function reset() {
    stepIdx = 0;
    anim = null;
    animT = 0;
    doneSteps = [];
    bubbles.clear();
    badge.set(`Mixture: ${MIXTURES[mixKey].label}`);
    badge.el.style.setProperty('--ix-hud-color', '#059669');
    stepOut.set('step 1');
  }

  function attempt(tech) {
    const mix = MIXTURES[mixKey];
    if (stepIdx >= mix.steps.length || anim) return;
    if (tech === mix.steps[stepIdx]) {
      anim = tech;
      animT = 0;
      badge.set(`${TECHNIQUES[tech].label} running…`);
      badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
      showInfoCard(stage, { title: `Correct: ${TECHNIQUES[tech].label}`, body: TECHNIQUES[tech].why, color: '#059669' });
    } else {
      badge.set(`${TECHNIQUES[tech].label} won't work here!`);
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      showInfoCard(stage, {
        title: `Not ${TECHNIQUES[tech].label.toLowerCase()}`,
        body: `${TECHNIQUES[tech].why}\nThat does not match this mixture at this stage. Components left: ${mix.parts.join(', ')}.`,
        color: '#ef4444',
      });
    }
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    const mix = MIXTURES[mixKey];
    if (anim) {
      animT += dt / 5;
      if (animT >= 1) {
        doneSteps.push(anim);
        stepIdx++;
        anim = null;
        bubbles.clear();
        if (stepIdx >= mix.steps.length) {
          badge.set('Separation complete!');
          badge.el.style.setProperty('--ix-hud-color', '#10b981');
          stepOut.set('complete');
          showInfoCard(stage, { title: 'Separation complete', body: mix.done, color: '#10b981' });
        } else {
          badge.set(`Step ${stepIdx + 1}: what next?`);
          badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
          stepOut.set(`step ${stepIdx + 1}`);
        }
      }
    }

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.82;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    text(ctx, mix.label, w / 2, 22, { font: '700 12px Poppins, sans-serif', color: '#e2e8f0' });
    const remaining = mix.steps.slice(stepIdx).length;
    text(ctx, stepIdx >= mix.steps.length ? 'fully separated ✓' : `${remaining} separation step${remaining > 1 ? 's' : ''} needed`, w / 2, 38);

    const cur = anim || (stepIdx < mix.steps.length ? null : 'done');
    const cx = w / 2;
    const p = anim ? Math.min(1, animT) : 0;

    if (cur === 'filtration') {
      drawStand(ctx, cx - 70, h * 0.18, benchY - 4);
      ctx.strokeStyle = GLASS;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(cx - 34, h * 0.26);
      ctx.lineTo(cx + 34, h * 0.26);
      ctx.lineTo(cx + 3, h * 0.4);
      ctx.lineTo(cx + 3, h * 0.5);
      ctx.moveTo(cx - 3, h * 0.4);
      ctx.lineTo(cx - 3, h * 0.5);
      ctx.moveTo(cx - 34, h * 0.26);
      ctx.lineTo(cx - 3, h * 0.4);
      ctx.stroke();
      ctx.fillStyle = `rgba(120,113,108,${0.25 + 0.6 * p})`;
      ctx.beginPath();
      ctx.moveTo(cx - 24, h * 0.27);
      ctx.lineTo(cx + 24, h * 0.27);
      ctx.lineTo(cx, h * 0.38);
      ctx.fill();
      text(ctx, 'residue builds up', cx + 60, h * 0.3, { align: 'left' });
      drawBeaker(ctx, cx - 26, benchY - 60, 52, 58, 0.15 + 0.5 * p, mixKey === 'muddy' || mixKey === 'sandsalt' ? 'rgba(186,230,253,0.45)' : 'rgba(125,211,252,0.4)', 'filtrate');
      if (anim) {
        ctx.strokeStyle = 'rgba(186,230,253,0.7)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(cx, h * 0.5);
        ctx.lineTo(cx, benchY - 60 + 58 * (0.85 - 0.5 * p));
        ctx.stroke();
      }
    } else if (cur === 'evaporation') {
      drawBurner(ctx, cx, benchY, t, !!anim, '#60a5fa', 30);
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(cx - 30, benchY - 2);
      ctx.lineTo(cx - 22, benchY - 56);
      ctx.lineTo(cx + 22, benchY - 56);
      ctx.lineTo(cx + 30, benchY - 2);
      ctx.stroke();
      ctx.strokeStyle = GLASS;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(cx, benchY - 62, 38, 9, 0, 0, Math.PI, false);
      ctx.stroke();
      ctx.fillStyle = `rgba(125,211,252,${0.5 * (1 - p)})`;
      ctx.beginPath();
      ctx.ellipse(cx, benchY - 63, 32 * (1 - p * 0.4), 5, 0, 0, Math.PI, false);
      ctx.fill();
      if (p > 0.3) {
        ctx.fillStyle = `rgba(248,250,252,${Math.min(1, (p - 0.3) * 1.6)})`;
        for (let i = 0; i < 7; i++) {
          ctx.fillRect(cx - 24 + i * 8, benchY - 66, 4, 3);
        }
        text(ctx, 'salt crystals appear', cx + 60, benchY - 70, { align: 'left' });
      }
      if (anim) {
        bubbles.spawn(cx, benchY - 64, { spread: 44, top: h * 0.2, v: 40 });
        text(ctx, 'water vapour escapes', cx, h * 0.22);
      }
    } else if (cur === 'sublimation') {
      drawBurner(ctx, cx, benchY, t, !!anim, '#60a5fa', 28);
      drawBeaker(ctx, cx - 26, benchY - 92, 52, 56, 0, '', '');
      ctx.fillStyle = `rgba(241,245,249,${0.8 * (1 - p)})`;
      ctx.fillRect(cx - 20, benchY - 44, 40, 5);
      ctx.strokeStyle = GLASS;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(cx, benchY - 94, 30, 7, 0, 0, Math.PI * 2);
      ctx.stroke();
      text(ctx, 'cold watch glass', cx, benchY - 108);
      if (p > 0.25) {
        ctx.fillStyle = `rgba(226,232,240,${Math.min(1, (p - 0.25) * 1.5)})`;
        for (let i = 0; i < 6; i++) ctx.fillRect(cx - 18 + i * 7, benchY - 90, 3.5, 4);
        text(ctx, 'naphthalene crystals re-form', cx + 40, benchY - 86, { align: 'left' });
      }
      if (anim) bubbles.spawn(cx, benchY - 48, { spread: 30, top: benchY - 90, color: 'rgba(226,232,240,0.5)' });
      text(ctx, 'salt stays behind', cx, benchY - 30);
    } else if (cur === 'distillation') {
      drawBurner(ctx, cx - 80, benchY, t, !!anim, '#60a5fa', 26);
      drawFlask(ctx, cx - 80, benchY - 32, 56, 62, 0.55 - 0.25 * p, 'rgba(125,211,252,0.45)', 'salt solution');
      ctx.strokeStyle = GLASS;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(cx - 80, benchY - 94);
      ctx.lineTo(cx - 80, benchY - 110);
      ctx.lineTo(cx + 40, benchY - 80);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(cx - 30, benchY - 108);
      ctx.lineTo(cx + 52, benchY - 86);
      ctx.stroke();
      text(ctx, 'condenser (cold water jacket)', cx + 6, benchY - 116);
      drawBeaker(ctx, cx + 36, benchY - 46, 46, 44, 0.1 + 0.6 * p, 'rgba(186,230,253,0.5)', 'pure water');
      if (anim) {
        bubbles.spawn(cx - 80, benchY - 60, { spread: 26, top: benchY - 100 });
        text(ctx, '100 °C', cx - 80, benchY - 120, { color: '#fbbf24' });
      }
    } else if (cur === 'chromatography') {
      const py = h * 0.2;
      const ph = h * 0.46;
      ctx.fillStyle = 'rgba(248,250,252,0.92)';
      ctx.fillRect(cx - 26, py, 52, ph);
      drawBeaker(ctx, cx - 44, py + ph - 26, 88, 50, 0.4, 'rgba(186,230,253,0.35)', 'solvent');
      ctx.strokeStyle = '#94a3b8';
      ctx.beginPath();
      ctx.moveTo(cx - 26, py + ph - 34);
      ctx.lineTo(cx + 26, py + ph - 34);
      ctx.stroke();
      const front = py + ph - 34 - (ph - 50) * p;
      ctx.strokeStyle = 'rgba(125,211,252,0.8)';
      ctx.beginPath();
      ctx.moveTo(cx - 26, front);
      ctx.lineTo(cx + 26, front);
      ctx.stroke();
      const dyes = [
        { c: '#facc15', f: 0.95 },
        { c: '#ef4444', f: 0.62 },
        { c: '#3b82f6', f: 0.34 },
      ];
      ctx.fillStyle = `rgba(15,23,42,${1 - p})`;
      ctx.beginPath();
      ctx.arc(cx, py + ph - 34, 5, 0, Math.PI * 2);
      ctx.fill();
      dyes.forEach((d) => {
        const dy = py + ph - 34 - (ph - 50) * p * d.f;
        ctx.fillStyle = d.c;
        ctx.globalAlpha = Math.min(1, p * 2);
        ctx.beginPath();
        ctx.arc(cx, dy, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      });
      text(ctx, 'dyes climb at different speeds', cx, py - 10);
    } else {
      drawBeaker(ctx, cx - 32, benchY - 76, 64, 70, 0.55, mixColor(), MIXTURES[mixKey].label);
      if (stepIdx >= mix.steps.length) {
        text(ctx, '✓ all components separated', cx, benchY - 96, { color: '#34d399', font: '700 12px Poppins, sans-serif' });
      } else {
        text(ctx, 'choose the right technique →', cx, benchY - 96, { color: '#fbbf24' });
      }
    }

    bubbles.step(dt);
    bubbles.draw(ctx);

    const doneY = h - 14;
    text(ctx, doneSteps.length ? `done: ${doneSteps.map((s) => TECHNIQUES[s].label).join(' → ')}` : 'no steps done yet', w / 2, doneY);
  });

  function mixColor() {
    if (mixKey === 'muddy') return 'rgba(120,86,52,0.7)';
    if (mixKey === 'ink') return 'rgba(30,41,59,0.85)';
    if (mixKey === 'naphthalene') return 'rgba(226,232,240,0.55)';
    return 'rgba(173,196,230,0.5)';
  }

  reset();
  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
