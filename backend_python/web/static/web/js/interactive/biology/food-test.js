import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { fmt, panelBg, labelText, drawTable } from './bio-utils.js';

// Each food sample has the nutrients it tests positive for.
const FOODS = [
  { id: 'potato', name: 'Potato', starch: true, sugar: false, protein: false, fat: false },
  { id: 'bread', name: 'Bread', starch: true, sugar: false, protein: true, fat: false },
  { id: 'glucose', name: 'Glucose solution', starch: false, sugar: true, protein: false, fat: false },
  { id: 'sucrose', name: 'Sucrose solution', starch: false, sugar: false, protein: false, fat: false },
  { id: 'eggwhite', name: 'Egg white', starch: false, sugar: false, protein: true, fat: false },
  { id: 'milk', name: 'Milk', starch: false, sugar: true, protein: true, fat: true },
  { id: 'oil', name: 'Cooking oil', starch: false, sugar: false, protein: false, fat: true },
  { id: 'water', name: 'Distilled water (control)', starch: false, sugar: false, protein: false, fat: false },
];

const TESTS = [
  { id: 'iodine', name: 'Iodine test', nutrient: 'starch', positiveLabel: 'Blue-black', negativeLabel: 'Yellow-brown',
    posColor: '#1a1a4d', negColor: '#d4a017',
    info: 'Iodine solution turns blue-black in the presence of starch. Add just 2 drops to the food sample.' },
  { id: 'benedicts', name: 'Benedict\'s test', nutrient: 'sugar', positiveLabel: 'Brick-red', negativeLabel: 'Blue',
    posColor: '#c0392b', negColor: '#1f6feb',
    info: 'Add Benedict\'s reagent and HEAT in a water bath. Reducing sugar turns blue → green/yellow/orange/brick-red (more sugar = redder).' },
  { id: 'biuret', name: 'Biuret test', nutrient: 'protein', positiveLabel: 'Violet', negativeLabel: 'Blue',
    posColor: '#8e44ad', negColor: '#1f6feb',
    info: 'Add NaOH then a few drops of CuSO₄. Protein turns blue → violet/purple.' },
  { id: 'ethanol', name: 'Ethanol emulsion', nutrient: 'fat', positiveLabel: 'Cloudy white', negativeLabel: 'Clear',
    posColor: '#f5f5f5', negColor: '#cfe8ff',
    info: 'Shake the food with ethanol to dissolve any fat, decant into water. Fat gives a cloudy white emulsion.' },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const resultBadge = hud.badge('Choose a food and a test', '#9ec1ff');

  let foodId = 'potato';
  let testId = 'iodine';
  let heated = false;        // for benedict's
  let result = null;         // 'positive' | 'negative' | null

  const panel = createPanel(stage, { title: 'Food Tests' });
  panel.info('Pick a food sample and a reagent, then press Run test. Benedict\'s needs heat first. Record the colour and conclude which nutrient is present.');
  panel.select({
    label: 'Food sample',
    options: FOODS.map((f) => ({ value: f.id, label: f.name })),
    value: foodId,
    onChange: (v) => { foodId = v; reset(); },
  });
  panel.select({
    label: 'Test',
    options: TESTS.map((t) => ({ value: t.id, label: t.name })),
    value: testId,
    onChange: (v) => { testId = v; reset(); },
  });
  const heatToggle = panel.toggle({ label: 'Heat (for Benedict\'s)', value: false, onChange: (v) => { heated = v; if (testId === 'benedicts') runIfReady(); } });
  panel.button({ label: 'Run test', icon: 'science', onClick: () => { runIfReady(); } });
  panel.button({ label: 'Reset', icon: 'refresh', variant: 'ghost', onClick: () => { reset(); } });
  panel.divider();
  const resultOut = panel.readout({ label: 'Result', value: '—' });
  const conclOut = panel.readout({ label: 'Conclusion', value: '—' });
  panel.button({ label: 'What do the colours mean?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'The four tests',
      body: 'Iodine → blue-black = starch. Benedict\'s (heated) → green to brick-red = reducing sugar. Biuret → violet = protein. Ethanol emulsion → cloudy white = fat. Always run distilled water as a control.',
      color: '#84CC16',
    });
  } });

  function reset() {
    result = null; heated = false; heatToggle.set(false);
    resultOut.set('—'); conclOut.set('—');
    resultBadge.set('Press Run test'); resultBadge.el.style.setProperty('--ix-hud-color', '#9ec1ff');
  }
  function runIfReady() {
    const food = FOODS.find((f) => f.id === foodId);
    const test = TESTS.find((t) => t.id === testId);
    if (test.id === 'benedicts' && !heated) {
      result = null;
      resultBadge.set('Heat the mixture first!'); resultBadge.el.style.setProperty('--ix-hud-color', '#fbbf24');
      resultOut.set('—'); conclOut.set('—');
      return;
    }
    const positive = food[test.nutrient];
    result = positive ? 'positive' : 'negative';
    resultOut.set(positive ? test.positiveLabel : test.negativeLabel);
    conclOut.set(positive ? `${test.nutrient.charAt(0).toUpperCase() + test.nutrient.slice(1)} PRESENT` : `${test.nutrient.charAt(0).toUpperCase() + test.nutrient.slice(1)} absent`);
    resultBadge.set(positive ? 'Positive ✓' : 'Negative');
    resultBadge.el.style.setProperty('--ix-hud-color', positive ? '#a3e635' : '#94a3b8');
  }

  // Current liquid colour (animated to target)
  let curColor = [212, 160, 23]; // iodine default yellow-brown
  let tgtColor = [212, 160, 23];

  function colorForState() {
    if (!result) {
      // pre-test: show reagent colour
      const t = TESTS.find((x) => x.id === testId);
      return hexToRgb(t.negColor);
    }
    const test = TESTS.find((t) => t.id === testId);
    const positive = result === 'positive';
    return hexToRgb(positive ? test.posColor : test.negColor);
  }
  function hexToRgb(h) {
    const n = parseInt(h.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  sim.setUpdate((ctx) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#05080f'; ctx.fillRect(0, 0, w, h);

    // animate liquid colour
    const tgt = colorForState();
    for (let i = 0; i < 3; i++) curColor[i] += (tgt[i] - curColor[i]) * 0.08;
    const [r, g, b] = curColor.map((v) => Math.round(v));

    // Test tube
    const tubeX = w * 0.5;
    const tubeTop = h * 0.18; const tubeBottom = h * 0.78;
    const tubeW = Math.min(w * 0.12, 90);
    // glass
    ctx.fillStyle = 'rgba(255,255,255,0.06)';
    ctx.strokeStyle = 'rgba(200,220,255,0.5)'; ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(tubeX - tubeW / 2, tubeTop);
    ctx.lineTo(tubeX - tubeW / 2, tubeBottom - tubeW / 2);
    ctx.arc(tubeX, tubeBottom - tubeW / 2, tubeW / 2, Math.PI, 0, true);
    ctx.lineTo(tubeX + tubeW / 2, tubeTop);
    ctx.stroke();
    // liquid fill (only if a test was run, or show reagent ready)
    const fillLevel = result ? 0.7 : 0.3;
    const liquidTop = tubeBottom - tubeW / 2 - (tubeBottom - tubeW / 2 - tubeTop) * fillLevel;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(tubeX - tubeW / 2 + 2, liquidTop);
    ctx.lineTo(tubeX - tubeW / 2 + 2, tubeBottom - tubeW / 2);
    ctx.arc(tubeX, tubeBottom - tubeW / 2, tubeW / 2 - 2, Math.PI, 0, true);
    ctx.lineTo(tubeX + tubeW / 2 - 2, liquidTop);
    ctx.closePath();
    ctx.fillStyle = `rgb(${r},${g},${b})`;
    ctx.globalAlpha = 0.92; ctx.fill();
    // surface highlight
    ctx.globalAlpha = 0.25; ctx.fillStyle = '#ffffff';
    ctx.fillRect(tubeX - tubeW / 2 + 4, liquidTop - 2, tubeW - 8, 3);
    ctx.restore();

    // bubbles for benedict's heating
    if (testId === 'benedicts' && heated) {
      ctx.fillStyle = 'rgba(255,255,255,0.5)';
      for (let i = 0; i < 6; i++) {
        const bx = tubeX + (Math.sin(performance.now() * 0.003 + i) * tubeW * 0.3);
        const by = tubeBottom - tubeW / 2 - ((performance.now() * 0.05 + i * 60) % (tubeBottom - tubeW / 2 - liquidTop));
        ctx.beginPath(); ctx.arc(bx, by, 2 + Math.sin(performance.now() * 0.01 + i), 0, Math.PI * 2); ctx.fill();
      }
    }

    // flame under tube if heating
    if (testId === 'benedicts' && heated) {
      ctx.fillStyle = '#fb923c';
      ctx.beginPath();
      const fy = tubeBottom + 8;
      ctx.moveTo(tubeX - 14, fy);
      ctx.quadraticCurveTo(tubeX, fy - 30 + Math.sin(performance.now() * 0.02) * 4, tubeX + 14, fy);
      ctx.quadraticCurveTo(tubeX, fy + 6, tubeX - 14, fy);
      ctx.fill();
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.moveTo(tubeX - 7, fy);
      ctx.quadraticCurveTo(tubeX, fy - 16, tubeX + 7, fy);
      ctx.fill();
    }

    // Sample label
    labelText(ctx, FOODS.find((f) => f.id === foodId).name, tubeX - tubeW / 2, tubeTop - 16,
      { color: '#e2e8f0', size: 13, align: 'left' });
    labelText(ctx, TESTS.find((t) => t.id === testId).name + (testId === 'benedicts' && heated ? ' (heated)' : ''),
      tubeX - tubeW / 2, tubeTop - 2, { color: '#9ec1ff', size: 11, align: 'left' });

    // Result / observation panel on right
    drawTable(ctx, {
      x: w - 232, y: 24, w: 220, title: 'Observation',
      cols: ['Field', 'Value'],
      rows: [
        ['Sample', FOODS.find((f) => f.id === foodId).name],
        ['Test', TESTS.find((t) => t.id === testId).name],
        ['Colour', result ? (result === 'positive' ? TESTS.find((t) => t.id === testId).positiveLabel : TESTS.find((t) => t.id === testId).negativeLabel) : '—'],
        ['Result', result ? (result === 'positive' ? 'Positive' : 'Negative') : '—'],
      ],
      accent: '#84CC16',
    });

    // Legend of all tests at bottom-left
    drawTable(ctx, {
      x: 12, y: h - 110, w: 260, title: 'Colour key',
      cols: ['Test', '+', '−'],
      rows: TESTS.map((t) => [t.name.split(' ')[0], t.positiveLabel, t.negativeLabel]),
      accent: '#84CC16',
    });
  });

  sim.start();

  return {
    dispose() {
      panel.dispose(); hud.dispose(); sim.dispose();
    },
  };
}
