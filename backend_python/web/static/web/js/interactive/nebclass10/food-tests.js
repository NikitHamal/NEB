import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Food tests bench (grade-10 biology practical): run iodine, Benedict's and
// Biuret tests on food samples and read the colour change.

const SAMPLES = [
  { id: 'rice', name: 'Boiled rice', starch: true, sugar: false, protein: false },
  { id: 'potato', name: 'Potato', starch: true, sugar: false, protein: false },
  { id: 'bread', name: 'Bread', starch: true, sugar: false, protein: false },
  { id: 'banana', name: 'Ripe banana', starch: false, sugar: true, protein: false },
  { id: 'milk', name: 'Milk', starch: false, sugar: true, protein: true },
  { id: 'egg', name: 'Egg white', starch: false, sugar: false, protein: true },
  { id: 'soybean', name: 'Soybean', starch: false, sugar: false, protein: true },
  { id: 'groundnut', name: 'Groundnut', starch: false, sugar: false, protein: true },
  { id: 'sugar', name: 'Sugar solution', starch: false, sugar: true, protein: false },
];

const TESTS = [
  { id: 'iodine', name: 'Iodine test (for starch)', reagent: '#8b5a2b', positive: '#141b2e', positiveName: 'blue-black', negativeName: 'yellow-brown', detects: 'starch', heat: false },
  { id: 'benedict', name: "Benedict's test (for reducing sugar)", reagent: '#4fa8e0', positive: '#c8541f', positiveName: 'brick red', negativeName: 'stays blue', detects: 'sugar', heat: true },
  { id: 'biuret', name: "Biuret test (for protein)", reagent: '#8f6ed5', positive: '#7d3fbf', positiveName: 'violet', negativeName: 'stays blue', detects: 'protein', heat: false },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Choose a food, then run a test', '#84CC16');

  let sample = SAMPLES[0];
  let test = TESTS[0];
  let boiled = 0;      // seconds of heating for Benedict's test
  let added = false;

  const panel = createPanel(stage, { title: 'Food tests' });
  panel.select({
    label: 'Food sample',
    options: SAMPLES.map((s) => ({ value: s.id, label: s.name })),
    value: sample.id,
    onChange: (id) => { sample = SAMPLES.find((s) => s.id === id); boiled = 0; added = false; update(); },
  });
  panel.select({
    label: 'Test',
    options: TESTS.map((t) => ({ value: t.id, label: t.name })),
    value: test.id,
    onChange: (id) => { test = TESTS.find((t) => t.id === id); boiled = 0; added = false; update(); },
  });
  const addBtn = panel.buttonRow([
    { label: 'Add reagent', icon: 'science', onClick: () => { added = true; update(); } },
    { label: 'Heat sample', icon: 'local_fire_department', variant: test.heat ? undefined : 'disabled', onClick: () => { boiled = Math.min(10, boiled + 2); added = true; update(); } },
  ]);
  panel.buttonRow([
    { label: 'Fresh sample', icon: 'refresh', variant: 'ghost', onClick: () => { boiled = 0; added = false; update(); } },
  ]);
  const readReagent = panel.readout({ label: 'Test for', value: '—' });
  const readResult = panel.readout({ label: 'Result', value: '—' });
  const readConcl = panel.readout({ label: 'Conclusion', value: '—' });
  const info = panel.info('');

  function present() {
    return test.detects === 'starch' ? sample.starch : test.detects === 'sugar' ? sample.sugar : sample.protein;
  }

  function draw(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = 'rgba(148,163,184,0.12)';
    ctx.fillRect(0, h * 0.8, w, h * 0.2);

    // tube
    const tubeW = Math.min(96, w * 0.17);
    const tubeH = h * 0.56;
    const tx = w * 0.1;
    const ty = h * 0.18;
    const pos = present() && added;
    const heatOK = !test.heat || boiled >= 4;
    const positive = pos && heatOK;
    const colour = !added ? '#c9a227' : positive ? test.positive : test.reagent;

    ctx.save();
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(tx, ty, tubeW, tubeH, [6, 6, tubeW / 2, tubeW / 2]);
    else ctx.rect(tx, ty, tubeW, tubeH);
    ctx.strokeStyle = 'rgba(232,238,251,0.8)';
    ctx.lineWidth = 2.4;
    ctx.stroke();
    ctx.clip();
    ctx.fillStyle = colour;
    ctx.globalAlpha = 0.9;
    ctx.fillRect(tx, ty + tubeH * 0.3, tubeW, tubeH * 0.7);
    ctx.globalAlpha = 1;
    ctx.restore();

    ctx.fillStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(sample.name.split(' ')[0], tx + tubeW / 2, ty - 12);

    // food on a tile
    const fx = w * 0.32;
    const fy = h * 0.62;
    ctx.fillStyle = 'rgba(248,250,252,0.92)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(fx - 46, fy - 34, 92, 68, 8); else ctx.rect(fx - 46, fy - 34, 92, 68);
    ctx.fill();
    ctx.fillStyle = '#d8c39a';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText('sample tile', fx, fy + 30);
    ctx.fillStyle = sample.id === 'milk' || sample.id === 'sugar' ? 'rgba(240,246,255,0.9)' : '#e3c07a';
    ctx.beginPath(); ctx.arc(fx, fy - 6, 20, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(2,6,23,0.35)'; ctx.lineWidth = 1; ctx.stroke();

    // heat source
    if (test.heat) {
      const bx = w * 0.62;
      const by = h * 0.72;
      ctx.fillStyle = boiled > 0 ? 'rgba(249,115,22,0.85)' : 'rgba(148,163,184,0.4)';
      ctx.beginPath();
      ctx.moveTo(bx - 14, by);
      ctx.quadraticCurveTo(bx, by - 26 - boiled * 1.6, bx + 14, by);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = 'rgba(232,238,251,0.85)';
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.fillText(boiled > 0 ? `heated ${boiled} s` : 'not heated yet', bx, by + 16);
    }

    // result card
    const cx = w * 0.42;
    const cy = h * 0.08;
    const cw = w * 0.54;
    const ch = h * 0.3;
    const cardColor = added ? (positive ? '#84cc16' : '#f59e0b') : 'rgba(158,193,255,0.6)';
    ctx.fillStyle = 'rgba(8,16,30,0.82)';
    ctx.strokeStyle = cardColor;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(cx, cy, cw, ch, 8); else ctx.rect(cx, cy, cw, ch);
    ctx.fill(); ctx.stroke();
    ctx.textAlign = 'left';
    ctx.fillStyle = cardColor;
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.fillText(test.name, cx + 14, cy + 24);
    ctx.fillStyle = 'rgba(232,238,251,0.92)';
    ctx.font = '600 10.5px Poppins, sans-serif';
    let line = 'Add the reagent to start the test.';
    if (added) {
      if (!present()) line = `No ${test.detects} present: the solution ${test.negativeName}.`;
      else if (!heatOK) line = `Heating needed: continue heating until the colour appears (Benedict's test needs gentle heating).`;
      else line = `${test.detects[0].toUpperCase()}${test.detects.slice(1)} present: the solution turns ${test.positiveName}.`;
    }
    wrap(ctx, line, cx + 14, cy + 46, cw - 28, 15);
    if (added) {
      ctx.fillStyle = 'rgba(199,212,234,0.8)';
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.fillText(`Observation: the solution ${positive ? test.positiveName : 'stays ' + test.negativeName.replace('stays ', '')}`, cx + 14, cy + ch - 16);
    }

    readReagent.set(test.detects);
    readResult.set(added ? (positive ? test.positiveName : test.negativeName) : 'not tested');
    readConcl.set(added ? (positive ? `${test.detects} present` : `${test.detects} absent`) : '—');
    info.set(`${test.name}: ${added ? (positive ? `positive for ${test.detects}` : `negative — no ${test.detects}`) : 'add the reagent and, where needed, heat the tube.'}`);
    void addBtn;
  }

  function wrap(ctx, text, x, y, maxW, lh) {
    const words = String(text).split(' ');
    let line = '';
    let ly = y;
    words.forEach((wd) => {
      const t = line ? `${line} ${wd}` : wd;
      if (ctx.measureText(t).width > maxW && line) { ctx.fillText(line, x, ly); line = wd; ly += lh; } else { line = t; }
    });
    if (line) ctx.fillText(line, x, ly);
  }

  function update() { sim.renderOnce(); }
  // the canvas helper calls (ctx, dt, width, height); draw wants (ctx, width, height)
  sim.setUpdate((ctx, dt, w, h) => draw(ctx, w, h));
  sim.onResize(() => sim.renderOnce());
  sim.start();
  update();

  return { dispose() { sim.dispose(); hud.dispose(); panel.dispose(); } };
}
