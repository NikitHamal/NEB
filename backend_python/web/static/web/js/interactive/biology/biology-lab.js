import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const LESSONS = {
  'compound-microscope': ['Microscope', '#65A30D', 'Focus'],
  'onion-cell-mount': ['Onion mount', '#84CC16', 'Stain'],
  'leaf-stomata': ['Stomata', '#22C55E', 'Turgor'],
  'plasmolysis-osmosis': ['Osmosis', '#0EA5E9', 'Solute'],
  'food-tests': ['Food tests', '#F59E0B', 'Sample strength'],
  'photosynthesis-rate': ['Photosynthesis', '#EAB308', 'Light'],
  'flower-dissection': ['Flower', '#EC4899', 'Dissection'],
  'animal-specimen-identification': ['Specimen', '#A16207', 'Rotation'],
  'plant-anatomy-sections': ['Plant anatomy', '#15803D', 'Section depth'],
  'transpiration-potometer': ['Potometer', '#0891B2', 'Environment'],
  'pollen-germination': ['Pollen', '#F97316', 'Sucrose'],
  'mitosis-root-tip': ['Mitosis', '#7C3AED', 'Stage scan'],
  'mendelian-cross': ['Genetics', '#2563EB', 'Sample size'],
  'dna-isolation': ['DNA extraction', '#14B8A6', 'Reagent quality'],
  'animal-tissue-histology': ['Histology', '#DC2626', 'Magnification'],
  'blood-grouping': ['Blood grouping', '#BE123C', 'Sample'],
};

const SPECIMENS = [
  ['Earthworm', 'segments + setae', '#A16207'],
  ['Cockroach', 'jointed legs + exoskeleton', '#92400E'],
  ['Fish', 'fins + gills', '#0284C7'],
  ['Frog', 'moist skin + limbs', '#16A34A'],
];

const TISSUES = [
  ['Epithelium', '#38BDF8'],
  ['Cartilage', '#A78BFA'],
  ['Muscle', '#F97316'],
  ['Neuron', '#F43F5E'],
];

export default function init(stage, context = {}) {
  const sim = createCanvas2D(stage, { dprCap: 1.5 });
  const cfg = LESSONS[context.lessonSlug] || LESSONS['compound-microscope'];
  const hud = createHud(stage);
  const badge = hud.badge(cfg[0], cfg[1]);
  const panel = createPanel(stage, { title: 'Biology Lab' });

  let mode = '3d';
  let value = 0.55;
  let animate = true;
  let tick = 0;
  let selected = 0;

  panel.select({
    label: 'View',
    options: [{ value: '2d', label: '2D diagram' }, { value: '3d', label: '3D bench' }],
    value: mode,
    onChange: (val) => { mode = val; },
  });
  panel.slider({
    label: cfg[2],
    min: 0,
    max: 100,
    step: 1,
    value: Math.round(value * 100),
    format: (v) => `${v}%`,
    onChange: (val) => { value = val / 100; },
  });
  panel.toggle({
    label: 'Animate process',
    value: animate,
    onChange: (val) => { animate = val; },
  });
  panel.divider();
  const readout = panel.readout({ label: 'Observation', value: 'Ready' });
  panel.button({
    label: 'Next field',
    icon: 'skip_next',
    onClick: () => { selected = (selected + 1) % 8; },
  });
  panel.info('Compare the labelled 2D practical diagram with the 3D bench view. Tap the stage to move through specimens or microscope fields.');

  function onDown(e) {
    selected = (selected + 1) % 8;
    const p = pointerPos(sim.canvas, e);
    value = p.x < sim.width / 2 ? Math.max(0, value - 0.08) : Math.min(1, value + 0.08);
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);

  function bg(ctx, w, h) {
    const g = ctx.createLinearGradient(0, 0, w, h);
    g.addColorStop(0, '#07150f');
    g.addColorStop(0.55, '#10251a');
    g.addColorStop(1, '#172718');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
    if (mode === '3d') {
      ctx.fillStyle = 'rgba(255,255,255,0.06)';
      ctx.beginPath();
      ctx.moveTo(0, h * 0.72);
      ctx.lineTo(w, h * 0.55);
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fill();
    }
  }

  function rr(ctx, x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, r);
    else ctx.rect(x, y, w, h);
  }

  function text(ctx, s, x, y, opts = {}) {
    ctx.fillStyle = opts.color || '#ECFDF5';
    ctx.font = `${opts.weight || 700} ${opts.size || 12}px Poppins, system-ui, sans-serif`;
    ctx.textAlign = opts.align || 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(s, x, y);
  }

  function line(ctx, x1, y1, x2, y2, color = 'rgba(220,252,231,0.65)', width = 2) {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function pill(ctx, s, x, y, color = cfg[1]) {
    ctx.font = '700 11px Poppins, system-ui, sans-serif';
    const wid = Math.max(82, ctx.measureText(s).width + 24);
    ctx.fillStyle = color;
    rr(ctx, x - wid / 2, y - 15, wid, 30, 15);
    ctx.fill();
    text(ctx, s, x, y + 1, { size: 11, color: '#F8FAFC' });
  }

  function project(x, y, z) {
    if (mode === '2d') return { x, y };
    return { x: x + z * 0.42, y: y - z * 0.28 };
  }

  function circle(ctx, x, y, r, color, z = 0) {
    const p = project(x, y, z);
    if (mode === '3d' && z) {
      ctx.fillStyle = 'rgba(0,0,0,0.2)';
      ctx.beginPath();
      ctx.ellipse(p.x + 8, p.y + 12, r * 1.1, r * 0.32, 0, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
    ctx.fill();
    return p;
  }

  function microscopeFrame(ctx, w, h) {
    const cx = w * 0.56;
    const cy = h * 0.43;
    ctx.strokeStyle = '#D9F99D';
    ctx.lineWidth = 9;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(cx - 58, cy + 92);
    ctx.quadraticCurveTo(cx - 130, cy + 12, cx - 58, cy - 76);
    ctx.stroke();
    ctx.fillStyle = '#334155';
    rr(ctx, cx - 80, cy - 120, 54, 100, 12);
    ctx.fill();
    rr(ctx, cx - 105, cy + 24, 170, 16, 8);
    ctx.fill();
    rr(ctx, cx - 120, cy + 112, 230, 22, 11);
    ctx.fill();
    ctx.fillStyle = '#94A3B8';
    rr(ctx, cx - 72, cy - 146, 38, 32, 8);
    ctx.fill();
    ['10x', '40x'].forEach((s, i) => {
      const x = cx - 14 + i * 42;
      rr(ctx, x, cy - 28, 26, 72, 8);
      ctx.fillStyle = i === selected % 2 ? '#84CC16' : '#64748B';
      ctx.fill();
      text(ctx, s, x + 13, cy + 58, { size: 10, color: '#D9F99D' });
    });
    const focus = 16 + value * 34;
    ctx.strokeStyle = '#FDE68A';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(cx + 84, cy - 5, focus, 0, Math.PI * 2);
    ctx.stroke();
    pill(ctx, `${Math.round((10 * (selected % 2 ? 40 : 10)))}x total`, cx, h * 0.84, '#65A30D');
    readout.set(value > 0.35 && value < 0.75 ? 'Specimen in focus' : 'Adjust fine focus');
  }

  function cellGrid(ctx, w, h, type) {
    const sx = w * 0.15;
    const sy = h * 0.18;
    const cw = w * 0.11;
    const ch = h * 0.115;
    for (let r = 0; r < 5; r++) {
      for (let c = 0; c < 6; c++) {
        const x = sx + c * cw + (r % 2) * 8;
        const y = sy + r * ch;
        ctx.fillStyle = type === 'plasmolysis' ? 'rgba(132,204,22,0.16)' : 'rgba(236,252,203,0.22)';
        ctx.strokeStyle = '#A3E635';
        ctx.lineWidth = 2;
        rr(ctx, x, y, cw * 0.88, ch * 0.82, 8);
        ctx.fill();
        ctx.stroke();
        const shrink = type === 'plasmolysis' ? value * 0.34 : 0.06;
        ctx.fillStyle = type === 'onion' ? `rgba(190,242,100,${0.22 + value * 0.45})` : 'rgba(34,197,94,0.35)';
        rr(ctx, x + cw * shrink, y + ch * shrink, cw * (0.88 - shrink * 2), ch * (0.82 - shrink * 2), 8);
        ctx.fill();
        circle(ctx, x + cw * 0.63, y + ch * 0.34, 5, '#A855F7');
      }
    }
  }

  function drawOnion(ctx, w, h) {
    cellGrid(ctx, w, h, 'onion');
    pill(ctx, 'cell wall', w * 0.3, h * 0.82, '#65A30D');
    pill(ctx, 'nucleus', w * 0.58, h * 0.82, '#A855F7');
    readout.set(value > 0.45 ? 'Stain reveals nucleus clearly' : 'Low contrast: add a little stain');
  }

  function drawStomata(ctx, w, h) {
    cellGrid(ctx, w, h, 'onion');
    const open = 10 + value * 34;
    for (let i = 0; i < 5; i++) {
      const x = w * (0.2 + i * 0.14);
      const y = h * (0.34 + (i % 2) * 0.18);
      ctx.fillStyle = '#22C55E';
      ctx.beginPath();
      ctx.ellipse(x - open * 0.45, y, 18, 38, -0.25, 0, Math.PI * 2);
      ctx.ellipse(x + open * 0.45, y, 18, 38, 0.25, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#052E16';
      ctx.beginPath();
      ctx.ellipse(x, y, open * 0.35, 26, 0, 0, Math.PI * 2);
      ctx.fill();
    }
    pill(ctx, value > 0.5 ? 'open stomata' : 'closing stomata', w * 0.5, h * 0.82, '#16A34A');
    readout.set(value > 0.5 ? 'Guard cells are turgid' : 'Guard cells are losing turgor');
  }

  function drawOsmosis(ctx, w, h) {
    cellGrid(ctx, w, h, 'plasmolysis');
    const arrows = 3 + Math.round(value * 5);
    for (let i = 0; i < arrows; i++) {
      const y = h * (0.25 + i * 0.07);
      line(ctx, w * 0.82, y, w * 0.68, y + 18, '#38BDF8', 3);
      circle(ctx, w * 0.84, y - 3, 4, '#7DD3FC');
    }
    pill(ctx, value > 0.55 ? 'hypertonic: plasmolysis' : 'hypotonic: turgid', w * 0.52, h * 0.84, value > 0.55 ? '#DC2626' : '#0EA5E9');
    readout.set(value > 0.55 ? 'Water leaves the vacuole' : 'Water enters; cells stay turgid');
  }

  function drawFood(ctx, w, h) {
    const tests = [
      ['Iodine', 'starch', '#1E3A8A'],
      ['Benedict', 'sugar', '#EA580C'],
      ['Biuret', 'protein', '#7E22CE'],
      ['Emulsion', 'lipid', '#E5E7EB'],
    ];
    tests.forEach((t, i) => {
      const x = w * (0.18 + i * 0.2);
      const y = h * 0.42;
      ctx.fillStyle = '#CBD5E1';
      rr(ctx, x - 18, y - 95, 36, 130, 14);
      ctx.fill();
      const positive = (i + selected) % 4 < Math.ceil(value * 4);
      ctx.fillStyle = positive ? t[2] : '#94A3B8';
      rr(ctx, x - 14, y - 46, 28, 76, 10);
      ctx.fill();
      text(ctx, t[0], x, y + 60, { size: 11, color: '#E2E8F0' });
      text(ctx, positive ? t[1] : 'negative', x, y + 78, { size: 10, color: positive ? '#FDE68A' : '#CBD5E1' });
    });
    readout.set('Compare final colour with controls');
  }

  function drawPhotosynthesis(ctx, w, h) {
    const beakerX = w * 0.5;
    const beakerY = h * 0.58;
    ctx.strokeStyle = '#BAE6FD';
    ctx.lineWidth = 4;
    rr(ctx, beakerX - 130, beakerY - 130, 260, 170, 16);
    ctx.stroke();
    ctx.fillStyle = 'rgba(14,165,233,0.2)';
    ctx.fillRect(beakerX - 126, beakerY - 60, 252, 98);
    for (let i = 0; i < 6; i++) {
      line(ctx, beakerX - 80 + i * 25, beakerY + 20, beakerX - 40 + i * 18, beakerY - 58, '#22C55E', 5);
    }
    const bubbles = Math.max(2, Math.round(value * 16));
    for (let i = 0; i < bubbles; i++) {
      const x = beakerX - 60 + Math.sin(i * 2.2) * 80;
      const y = beakerY - 58 - ((tick * 40 + i * 29) % 95);
      circle(ctx, x, y, 4 + (i % 3), 'rgba(186,230,253,0.78)');
    }
    const lamp = project(w * 0.18, h * 0.18, mode === '3d' ? 70 : 0);
    circle(ctx, lamp.x, lamp.y, 32, '#FDE047');
    pill(ctx, `${Math.round(value * 30)} bubbles/min`, w * 0.5, h * 0.84, '#EAB308');
    readout.set(value > 0.72 ? 'CO2 may become limiting' : 'Light controls oxygen output');
  }

  function drawFlower(ctx, w, h) {
    const cx = w * 0.5;
    const cy = h * 0.44;
    for (let i = 0; i < 5; i++) {
      const a = i / 5 * Math.PI * 2 + tick * 0.05;
      const p = project(cx + Math.cos(a) * 52, cy + Math.sin(a) * 34, mode === '3d' ? 38 : 0);
      ctx.fillStyle = i < Math.ceil(value * 5) ? '#F472B6' : 'rgba(244,114,182,0.38)';
      ctx.beginPath();
      ctx.ellipse(p.x, p.y, 42, 24, a, 0, Math.PI * 2);
      ctx.fill();
    }
    circle(ctx, cx, cy, 25, '#FDE047', mode === '3d' ? 52 : 0);
    for (let i = 0; i < 6; i++) {
      const a = i / 6 * Math.PI * 2;
      line(ctx, cx, cy, cx + Math.cos(a) * 78, cy + Math.sin(a) * 60, '#FBBF24', 3);
      circle(ctx, cx + Math.cos(a) * 82, cy + Math.sin(a) * 64, 7, '#A16207');
    }
    pill(ctx, 'calyx - corolla - androecium - gynoecium', w * 0.5, h * 0.84, '#DB2777');
    readout.set('Dissect outer whorls before inner whorls');
  }

  function drawSpecimen(ctx, w, h) {
    const s = SPECIMENS[selected % SPECIMENS.length];
    const cx = w * 0.5;
    const cy = h * 0.46;
    ctx.fillStyle = s[2];
    if (s[0] === 'Earthworm') {
      for (let i = 0; i < 18; i++) circle(ctx, cx - 150 + i * 17, cy + Math.sin(i * 0.7) * 18, 13, s[2], mode === '3d' ? i * 2 : 0);
    } else if (s[0] === 'Cockroach') {
      rr(ctx, cx - 62, cy - 28, 124, 56, 26);
      ctx.fill();
      for (let i = -1; i <= 1; i++) {
        line(ctx, cx - 20, cy + i * 18, cx - 110, cy + i * 42, '#FBBF24', 4);
        line(ctx, cx + 20, cy + i * 18, cx + 110, cy + i * 42, '#FBBF24', 4);
      }
    } else if (s[0] === 'Fish') {
      ctx.beginPath();
      ctx.ellipse(cx, cy, 118, 52, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(cx + 105, cy);
      ctx.lineTo(cx + 172, cy - 48);
      ctx.lineTo(cx + 172, cy + 48);
      ctx.closePath();
      ctx.fill();
      circle(ctx, cx - 74, cy - 12, 7, '#E0F2FE');
    } else {
      circle(ctx, cx - 38, cy, 58, s[2]);
      circle(ctx, cx + 60, cy - 20, 36, s[2]);
      for (let i = -1; i <= 1; i += 2) {
        line(ctx, cx - 64, cy + i * 22, cx - 134, cy + i * 58, '#BBF7D0', 6);
        line(ctx, cx + 30, cy + i * 20, cx + 116, cy + i * 54, '#BBF7D0', 6);
      }
    }
    pill(ctx, s[0], w * 0.5, h * 0.8, s[2]);
    readout.set(s[1]);
  }

  function drawAnatomy(ctx, w, h) {
    const cx = w * 0.48;
    const cy = h * 0.44;
    const rings = [
      [150, '#DCFCE7', 'epidermis'],
      [122, '#BBF7D0', 'cortex'],
      [88, '#86EFAC', 'endodermis'],
      [56, '#22C55E', 'vascular'],
    ];
    rings.forEach((r, i) => {
      circle(ctx, cx, cy, r[0], r[1], mode === '3d' ? i * 12 : 0);
      ctx.strokeStyle = '#14532D';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
    for (let i = 0; i < 10; i++) {
      const a = i / 10 * Math.PI * 2;
      const rad = value > 0.5 ? 76 : 42 + (i % 3) * 24;
      circle(ctx, cx + Math.cos(a) * rad, cy + Math.sin(a) * rad, 13, i % 2 ? '#0EA5E9' : '#F97316', mode === '3d' ? 64 : 0);
    }
    pill(ctx, value > 0.5 ? 'dicot: ring bundles' : 'monocot: scattered bundles', w * 0.5, h * 0.84, '#15803D');
    readout.set('Xylem and phloem arrangement identifies section type');
  }

  function drawPotometer(ctx, w, h) {
    const y = h * 0.52;
    line(ctx, w * 0.18, y, w * 0.8, y, '#BAE6FD', 10);
    rr(ctx, w * 0.16, y - 26, w * 0.66, 52, 20);
    ctx.strokeStyle = '#E0F2FE';
    ctx.lineWidth = 3;
    ctx.stroke();
    const bubbleX = w * (0.22 + value * 0.48 + Math.sin(tick) * 0.015);
    circle(ctx, bubbleX, y, 13, '#F8FAFC');
    for (let i = 0; i < 7; i++) {
      line(ctx, w * 0.76, y - 20, w * 0.86 + Math.sin(i) * 18, y - 150 + i * 22, '#22C55E', 5);
    }
    pill(ctx, `${(value * 2.8 + 0.2).toFixed(2)} mm/min`, w * 0.5, h * 0.8, '#0891B2');
    readout.set('Bubble displacement estimates water uptake');
  }

  function drawPollen(ctx, w, h) {
    for (let i = 0; i < 22; i++) {
      const x = w * (0.16 + ((i * 37) % 70) / 100);
      const y = h * (0.2 + ((i * 53) % 52) / 100);
      circle(ctx, x, y, 13, '#F97316', mode === '3d' ? (i % 4) * 10 : 0);
      if ((i + selected) % 4 < value * 4) {
        line(ctx, x + 9, y + 5, x + 36 + value * 60, y + 20 + Math.sin(i) * 18, '#FDBA74', 4);
      }
    }
    pill(ctx, `${Math.round(value * 86)}% germination`, w * 0.5, h * 0.84, '#F97316');
    readout.set('Count germinated grains in multiple fields');
  }

  function drawMitosis(ctx, w, h) {
    const stages = ['prophase', 'metaphase', 'anaphase', 'telophase'];
    for (let i = 0; i < 16; i++) {
      const x = w * (0.17 + (i % 4) * 0.18);
      const y = h * (0.22 + Math.floor(i / 4) * 0.14);
      const st = (i + selected) % 4;
      circle(ctx, x, y, 34, 'rgba(221,214,254,0.35)', mode === '3d' ? st * 8 : 0);
      ctx.strokeStyle = '#C4B5FD';
      ctx.stroke();
      if (st === 0) for (let k = 0; k < 5; k++) line(ctx, x - 12 + k * 6, y - 10, x + 8 - k * 4, y + 12, '#7C3AED', 3);
      else if (st === 1) for (let k = 0; k < 5; k++) line(ctx, x - 18 + k * 9, y - 20, x - 18 + k * 9, y + 20, '#7C3AED', 3);
      else if (st === 2) for (let k = 0; k < 4; k++) {
        line(ctx, x - 6, y, x - 24, y - 18 + k * 12, '#7C3AED', 3);
        line(ctx, x + 6, y, x + 24, y - 18 + k * 12, '#7C3AED', 3);
      } else {
        circle(ctx, x - 12, y, 10, '#7C3AED');
        circle(ctx, x + 12, y, 10, '#7C3AED');
      }
    }
    pill(ctx, stages[selected % 4], w * 0.5, h * 0.84, '#7C3AED');
    readout.set('Classify cells before calculating mitotic index');
  }

  function drawGenetics(ctx, w, h) {
    const x0 = w * 0.28;
    const y0 = h * 0.25;
    const cell = Math.min(72, w * 0.12);
    const labels = ['AA', 'Aa', 'Aa', 'aa'];
    for (let r = 0; r < 2; r++) for (let c = 0; c < 2; c++) {
      const idx = r * 2 + c;
      ctx.fillStyle = labels[idx] === 'aa' ? '#DBEAFE' : '#BFDBFE';
      rr(ctx, x0 + c * cell, y0 + r * cell, cell - 3, cell - 3, 8);
      ctx.fill();
      text(ctx, labels[idx], x0 + c * cell + cell / 2, y0 + r * cell + cell / 2, { color: '#1E3A8A', size: 18 });
    }
    const n = 20 + Math.round(value * 180);
    const rec = Math.round(n * 0.25 + Math.sin(selected) * Math.sqrt(n));
    pill(ctx, `${n - rec}:${rec} observed`, w * 0.66, h * 0.42, '#2563EB');
    pill(ctx, 'expected phenotype 3:1', w * 0.5, h * 0.82, '#1D4ED8');
    readout.set('Small samples drift away from expected ratio');
  }

  function drawDna(ctx, w, h) {
    const steps = [
      ['crush', '#84CC16'],
      ['detergent', '#38BDF8'],
      ['salt', '#CBD5E1'],
      ['filter', '#FDE68A'],
      ['cold alcohol', '#A78BFA'],
      ['DNA threads', '#F8FAFC'],
    ];
    steps.forEach((s, i) => {
      const x = w * (0.14 + i * 0.145);
      const y = h * 0.34 + Math.sin(tick + i) * 4;
      circle(ctx, x, y, 30, s[1], mode === '3d' ? i * 14 : 0);
      text(ctx, String(i + 1), x, y, { color: '#0F172A', size: 18 });
      text(ctx, s[0], x, y + 48, { size: 10, color: '#E0F2FE' });
      if (i < steps.length - 1) line(ctx, x + 34, y, w * (0.14 + (i + 1) * 0.145) - 34, y, '#A7F3D0', 3);
    });
    for (let i = 0; i < Math.round(value * 10); i++) {
      line(ctx, w * 0.72 + i * 6, h * 0.61, w * 0.76 + i * 4, h * 0.72, '#F8FAFC', 2);
    }
    readout.set(value > 0.55 ? 'White DNA precipitate visible' : 'Poor yield: improve reagent conditions');
  }

  function drawHistology(ctx, w, h) {
    const t = TISSUES[selected % TISSUES.length];
    const sx = w * 0.16;
    const sy = h * 0.2;
    for (let i = 0; i < 28; i++) {
      const x = sx + (i % 7) * w * 0.09;
      const y = sy + Math.floor(i / 7) * h * 0.105;
      if (t[0] === 'Neuron') {
        circle(ctx, x, y, 10, t[1]);
        line(ctx, x, y, x + 30, y - 18, t[1], 3);
        line(ctx, x, y, x - 20, y + 20, t[1], 3);
      } else if (t[0] === 'Muscle') {
        line(ctx, x - 24, y, x + 34, y, t[1], 7);
        line(ctx, x - 18, y - 7, x + 26, y - 7, '#FED7AA', 1);
      } else {
        circle(ctx, x, y, t[0] === 'Cartilage' ? 15 : 13, t[1], mode === '3d' ? (i % 3) * 8 : 0);
      }
    }
    pill(ctx, t[0], w * 0.5, h * 0.83, t[1]);
    readout.set(t[0] === 'Muscle' ? 'Striations indicate skeletal muscle' : 'Use visible structure to justify identity');
  }

  function drawBlood(ctx, w, h) {
    const sample = selected % 4;
    const groups = [
      ['A+', true, false, true],
      ['B-', false, true, false],
      ['AB+', true, true, true],
      ['O-', false, false, false],
    ];
    const g = groups[sample];
    ['anti-A', 'anti-B', 'anti-D'].forEach((s, i) => {
      const x = w * (0.25 + i * 0.25);
      const y = h * 0.42;
      circle(ctx, x, y, 58, 'rgba(254,226,226,0.24)', mode === '3d' ? i * 18 : 0);
      const agg = g[i + 1];
      for (let k = 0; k < 20; k++) {
        const a = k * 2.4;
        const r = agg ? 12 + (k % 4) * 6 : 12 + (k % 6) * 7;
        circle(ctx, x + Math.cos(a) * r, y + Math.sin(a * 1.3) * r * 0.8, agg ? 5 : 3, '#DC2626');
      }
      text(ctx, s, x, y + 82, { size: 12, color: '#FECACA' });
      text(ctx, agg ? 'clumps' : 'smooth', x, y + 102, { size: 10, color: agg ? '#FDE68A' : '#E2E8F0' });
    });
    pill(ctx, `sample ${g[0]}`, w * 0.5, h * 0.82, '#BE123C');
    readout.set('Agglutination pattern identifies ABO and Rh group');
  }

  function draw(ctx, dt, w, h) {
    if (animate) tick += dt * 1.35;
    bg(ctx, w, h);
    badge.set(`${cfg[0]} - ${mode.toUpperCase()}`);
    const slug = context.lessonSlug || 'compound-microscope';
    if (slug === 'compound-microscope') microscopeFrame(ctx, w, h);
    else if (slug === 'onion-cell-mount') drawOnion(ctx, w, h);
    else if (slug === 'leaf-stomata') drawStomata(ctx, w, h);
    else if (slug === 'plasmolysis-osmosis') drawOsmosis(ctx, w, h);
    else if (slug === 'food-tests') drawFood(ctx, w, h);
    else if (slug === 'photosynthesis-rate') drawPhotosynthesis(ctx, w, h);
    else if (slug === 'flower-dissection') drawFlower(ctx, w, h);
    else if (slug === 'animal-specimen-identification') drawSpecimen(ctx, w, h);
    else if (slug === 'plant-anatomy-sections') drawAnatomy(ctx, w, h);
    else if (slug === 'transpiration-potometer') drawPotometer(ctx, w, h);
    else if (slug === 'pollen-germination') drawPollen(ctx, w, h);
    else if (slug === 'mitosis-root-tip') drawMitosis(ctx, w, h);
    else if (slug === 'mendelian-cross') drawGenetics(ctx, w, h);
    else if (slug === 'dna-isolation') drawDna(ctx, w, h);
    else if (slug === 'animal-tissue-histology') drawHistology(ctx, w, h);
    else drawBlood(ctx, w, h);
  }

  sim.setUpdate(draw);
  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
