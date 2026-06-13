import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawFlask, drawBeaker, makeBubbles, text, GLASS } from './chem-utils.js';

const GASES = {
  h2: {
    name: 'Hydrogen (H₂)',
    reagents: 'granulated zinc + dilute HCl',
    eqn: 'Zn + 2HCl → ZnCl₂ + H₂↑',
    collect: 'downward displacement of water (H₂ is insoluble and lighter than air)',
    test: 'Burning splint near the mouth → goes off with a squeaky POP',
    testEqn: '2H₂ + O₂ → 2H₂O',
    color: 'rgba(186,230,253,0.0)',
    liquid: 'rgba(186,230,253,0.4)',
    solid: '#94a3b8',
    solidLabel: 'zinc granules',
    overWater: true,
  },
  o2: {
    name: 'Oxygen (O₂)',
    reagents: 'H₂O₂ solution + MnO₂ catalyst',
    eqn: '2H₂O₂ --MnO₂--> 2H₂O + O₂↑',
    collect: 'downward displacement of water (O₂ is only slightly soluble)',
    test: 'Glowing splint at the mouth → RELIGHTS brightly',
    testEqn: 'C + O₂ → CO₂ (the splint burns vigorously)',
    color: 'rgba(125,211,252,0.0)',
    liquid: 'rgba(226,232,240,0.35)',
    solid: '#1e293b',
    solidLabel: 'MnO₂ (black)',
    overWater: true,
  },
  co2: {
    name: 'Carbon dioxide (CO₂)',
    reagents: 'marble chips (CaCO₃) + dilute HCl',
    eqn: 'CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂↑',
    collect: 'upward displacement of air (CO₂ is denser than air)',
    test: 'Bubble through lime water → turns MILKY',
    testEqn: 'CO₂ + Ca(OH)₂ → CaCO₃↓ + H₂O',
    color: 'rgba(148,163,184,0.0)',
    liquid: 'rgba(186,230,253,0.4)',
    solid: '#e7e5e4',
    solidLabel: 'marble chips',
    overWater: false,
  },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Choose a gas to prepare', '#059669');
  const bubbles = makeBubbles(30);

  let gasKey = 'h2';
  let reacting = false;
  let collected = 0;
  let tested = false;
  let testAnim = 0;
  let t = 0;

  const panel = createPanel(stage, { title: 'Gas Preparation' });
  panel.select({
    label: 'Gas to prepare',
    options: Object.keys(GASES).map((k) => ({ value: k, label: GASES[k].name })),
    value: gasKey,
    onChange: (v) => { gasKey = v; reset(); },
  });
  const reagOut = panel.readout({ label: 'Reagents', value: GASES.h2.reagents });
  panel.divider();
  panel.buttonRow([
    { label: 'Add acid', icon: 'colorize', onClick: startReaction },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset },
  ]);
  const fillOut = panel.readout({ label: 'Jar filled', value: '0%' });
  const testBtn = panel.button({ label: 'Test the gas', icon: 'local_fire_department', onClick: testGas });
  panel.info('Set up the generator, run in the acid, collect a full jar, then do the identifying test. Note which gases are collected over water and which by air displacement.');

  function reset() {
    reacting = false;
    collected = 0;
    tested = false;
    testAnim = 0;
    bubbles.clear();
    const g = GASES[gasKey];
    reagOut.set(g.reagents);
    badge.set(`Ready: ${g.reagents}`);
    badge.el.style.setProperty('--ix-hud-color', '#059669');
    fillOut.set('0%');
  }

  function startReaction() {
    if (reacting) return;
    reacting = true;
    const g = GASES[gasKey];
    badge.set('Reaction started — gas evolving!');
    badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
    showInfoCard(stage, { title: g.name, body: `${g.eqn}\nCollection: ${g.collect}.`, color: '#059669' });
  }

  function testGas() {
    const g = GASES[gasKey];
    if (collected < 0.95) {
      badge.set('Jar not full yet — keep collecting!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    tested = true;
    testAnim = 1;
    badge.set('Positive test!');
    badge.el.style.setProperty('--ix-hud-color', '#10b981');
    showInfoCard(stage, { title: `Testing ${g.name}`, body: `${g.test}.\n${g.testEqn}`, color: '#10b981' });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    const g = GASES[gasKey];
    if (reacting && collected < 1) {
      collected = Math.min(1, collected + dt * 0.09);
      if (collected >= 1) {
        badge.set('Jar full — test the gas!');
        badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
      }
    }
    if (testAnim > 0) testAnim = Math.max(0, testAnim - dt * 0.25);

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.84;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const fx = w * 0.24;
    drawFlask(ctx, fx, benchY - 2, 84, 86, reacting ? 0.5 : 0.32, g.liquid, 'generator flask');
    ctx.fillStyle = g.solid;
    for (let i = 0; i < 8; i++) {
      ctx.beginPath();
      ctx.arc(fx - 18 + (i % 4) * 11, benchY - 14 - Math.floor(i / 4) * 8, 4, 0, Math.PI * 2);
      ctx.fill();
    }
    text(ctx, g.solidLabel, fx, benchY - 96);

    ctx.strokeStyle = GLASS;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(fx + 8, benchY - 86);
    ctx.lineTo(fx + 8, benchY - 120);
    ctx.lineTo(fx - 14, benchY - 140);
    ctx.stroke();
    text(ctx, 'thistle funnel (acid in)', fx - 16, benchY - 148);
    ctx.beginPath();
    ctx.moveTo(fx + 11, benchY - 80);
    ctx.lineTo(w * 0.56, benchY - 80);
    ctx.lineTo(w * 0.56, g.overWater ? benchY - 46 : benchY - 130);
    ctx.stroke();

    const jx = w * 0.7;
    if (g.overWater) {
      const trough = { x: w * 0.52, y: benchY - 40, w: w * 0.4, h: 38 };
      ctx.fillStyle = 'rgba(96,165,250,0.3)';
      ctx.fillRect(trough.x, trough.y + 8, trough.w, trough.h - 8);
      ctx.strokeStyle = GLASS;
      ctx.strokeRect(trough.x, trough.y, trough.w, trough.h);
      text(ctx, 'water trough', trough.x + trough.w / 2, benchY + 14);
      const jarH = 92;
      const jarY = trough.y + 12 - jarH;
      ctx.strokeStyle = GLASS;
      ctx.strokeRect(jx - 22, jarY, 44, jarH);
      ctx.fillStyle = 'rgba(96,165,250,0.3)';
      const waterH = jarH * (1 - collected);
      ctx.fillRect(jx - 20, jarY + jarH - waterH, 40, waterH);
      text(ctx, 'gas jar (inverted)', jx, jarY - 8);
      if (reacting && collected < 1) {
        bubbles.spawn(jx, trough.y + 16, { spread: 16, top: jarY + jarH - waterH });
      }
    } else {
      const jarH = 92;
      const jarY = benchY - jarH;
      ctx.strokeStyle = GLASS;
      ctx.strokeRect(jx - 22, jarY, 44, jarH);
      ctx.fillStyle = `rgba(148,163,184,${0.18 * collected})`;
      ctx.fillRect(jx - 20, jarY + jarH * (1 - collected), 40, jarH * collected);
      text(ctx, 'gas jar (mouth up)', jx, jarY - 8);
      text(ctx, 'CO₂ sinks — denser than air', jx, benchY + 14);
      if (reacting && collected < 1) {
        bubbles.spawn(w * 0.56, benchY - 110, { spread: 8, top: jarY, color: 'rgba(148,163,184,0.4)' });
      }
    }

    if (reacting) bubbles.spawn(fx, benchY - 16, { spread: 30, top: benchY - 62 });
    bubbles.step(dt);
    bubbles.draw(ctx);

    if (tested && testAnim > 0) {
      if (gasKey === 'h2') {
        text(ctx, 'POP!', jx, h * 0.2, { color: '#fbbf24', font: `800 ${18 + testAnim * 14}px Poppins, sans-serif` });
      } else if (gasKey === 'o2') {
        ctx.fillStyle = `rgba(251,191,36,${testAnim})`;
        ctx.beginPath();
        ctx.arc(jx, h * 0.24, 8 + (1 - testAnim) * 6, 0, Math.PI * 2);
        ctx.fill();
        text(ctx, 'splint relights!', jx, h * 0.16, { color: '#fbbf24' });
      } else {
        drawBeaker(ctx, jx + 36, h * 0.16, 40, 44, 0.5, `rgba(241,245,249,${0.3 + 0.5 * (1 - testAnim)})`, 'lime water');
        text(ctx, 'milky!', jx + 56, h * 0.12, { color: '#f8fafc' });
      }
    }

    text(ctx, g.eqn, w / 2, h * 0.05, { color: '#9ec1ff', font: '600 11px Poppins, sans-serif' });
    fillOut.set(`${Math.round(collected * 100)}%`);
    testBtn.el.style.opacity = collected >= 0.95 ? '1' : '0.5';
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
