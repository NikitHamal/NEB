import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Realistic compound microscope sim: focus, objective, diaphragm, slide selection
// Total magnification = eyepiece (10x) × objective (10x / 40x / 100x)

const SLIDES = {
  onion: {
    label: 'Onion peel (100x)',
    // cells drawn as a grid of rectangular cells with nuclei
    draw(ctx, cx, cy, r, focus) {
      const alpha = Math.max(0, Math.min(1, 1 - Math.abs(focus) * 0.045));
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.clip();
      // background — cytoplasm colour
      ctx.fillStyle = `rgba(220,200,160,${alpha * 0.9})`;
      ctx.fillRect(cx - r, cy - r, r * 2, r * 2);
      // cell walls & nuclei
      const cellW = r * 0.22;
      const cellH = r * 0.28;
      for (let row = -3; row <= 3; row++) {
        for (let col = -3; col <= 3; col++) {
          const x = cx + col * cellW;
          const y = cy + row * cellH;
          ctx.strokeStyle = `rgba(100,70,20,${alpha * 0.95})`;
          ctx.lineWidth = 1.6;
          ctx.strokeRect(x - cellW / 2, y - cellH / 2, cellW, cellH);
          // nucleus
          ctx.fillStyle = `rgba(120,60,40,${alpha * 0.8})`;
          ctx.beginPath();
          ctx.ellipse(x, y, cellW * 0.22, cellH * 0.2, 0, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      ctx.restore();
    },
  },
  blood: {
    label: 'Blood smear (400x)',
    draw(ctx, cx, cy, r, focus) {
      const alpha = Math.max(0, Math.min(1, 1 - Math.abs(focus) * 0.045));
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.clip();
      ctx.fillStyle = `rgba(255,220,210,${alpha * 0.85})`;
      ctx.fillRect(cx - r, cy - r, r * 2, r * 2);
      // Red blood cells (biconcave discs — shown as donut-like circles)
      const rbc = [
        [0, 0], [-0.3, 0.2], [0.25, -0.25], [-0.15, -0.35],
        [0.35, 0.3], [-0.4, -0.1], [0.05, 0.4], [0.45, -0.1],
      ];
      rbc.forEach(([dx, dy]) => {
        const x = cx + dx * r;
        const y = cy + dy * r;
        const rr = r * 0.13;
        ctx.fillStyle = `rgba(210,80,80,${alpha * 0.75})`;
        ctx.beginPath();
        ctx.arc(x, y, rr, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = `rgba(255,200,190,${alpha * 0.9})`;
        ctx.beginPath();
        ctx.arc(x, y, rr * 0.45, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = `rgba(180,50,50,${alpha * 0.6})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      });
      // White blood cell (larger, with lobed nucleus)
      ctx.fillStyle = `rgba(230,230,255,${alpha * 0.75})`;
      ctx.beginPath();
      ctx.arc(cx + r * 0.1, cy - r * 0.05, r * 0.19, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = `rgba(80,80,180,${alpha * 0.7})`;
      ctx.beginPath();
      ctx.arc(cx + r * 0.08, cy - r * 0.07, r * 0.08, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    },
  },
};

const OBJECTIVES = [
  { label: '10×', mag: 10, fov: 1.0 },
  { label: '40×', mag: 40, fov: 0.32 },
  { label: '100× (oil)', mag: 100, fov: 0.13 },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const magBadge = hud.badge('100×', '#84CC16');
  const focusBadge = hud.badge('Focus: coarse', '#9ec1ff');

  let objIdx = 0;          // 0=10x, 1=40x, 2=100x
  let coarseFocus = 0;     // -100..100 offset from optical centre
  let fineFocus = 0;       // -10..10
  let diaphragm = 0.7;     // 0..1
  let slideKey = 'onion';

  const panel = createPanel(stage, { title: 'Microscope Controls' });
  const slideCtrl = panel.select({
    label: 'Slide',
    options: [
      { value: 'onion', label: 'Onion peel' },
      { value: 'blood', label: 'Blood smear' },
    ],
    value: 'onion',
    onChange: (v) => { slideKey = v; coarseFocus = 0; fineFocus = 0; },
  });

  panel.section('Objective');
  panel.buttonRow(
    OBJECTIVES.map((o, i) => ({
      label: o.label,
      onClick: () => {
        objIdx = i;
        coarseFocus = 0; fineFocus = 0;
        coarseCtrl.set(0); fineCtrl.set(0);
      },
    }))
  );

  panel.section('Focus');
  const coarseCtrl = panel.slider({
    label: 'Coarse focus',
    min: -100, max: 100, step: 1, value: 0,
    format: (v) => `${v > 0 ? '+' : ''}${v}`,
    onChange: (v) => { coarseFocus = v; },
  });
  const fineCtrl = panel.slider({
    label: 'Fine focus',
    min: -10, max: 10, step: 0.5, value: 0,
    format: (v) => `${v > 0 ? '+' : ''}${v.toFixed(1)}`,
    onChange: (v) => { fineFocus = v; },
  });
  const diaphCtrl = panel.slider({
    label: 'Diaphragm (light)',
    min: 0.1, max: 1.0, step: 0.05, value: 0.7,
    format: (v) => `${Math.round(v * 100)}%`,
    onChange: (v) => { diaphragm = v; },
  });

  panel.divider();
  const magOut = panel.readout({ label: 'Total magnification', value: '100×' });
  panel.info('Adjust Coarse focus first — then fine-tune. Higher objectives need more precise focus. Open the diaphragm for more light (can reduce contrast).');

  function computeFocusOffset() {
    return coarseFocus + fineFocus;
  }

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);

    const obj = OBJECTIVES[objIdx];
    const totalMag = 10 * obj.mag;
    const focusOffset = computeFocusOffset();
    const sharpness = Math.max(0, 1 - Math.abs(focusOffset) * 0.028);

    // Draw microscope body (stylised)
    const bodyX = w * 0.5;
    const bodyTop = 20;
    const tubeH = h * 0.28;

    // Eyepiece
    ctx.fillStyle = '#2d3a4a';
    ctx.beginPath();
    ctx.roundRect(bodyX - 16, bodyTop, 32, 28, 6);
    ctx.fill();
    ctx.fillStyle = '#1a2530';
    ctx.beginPath();
    ctx.ellipse(bodyX, bodyTop + 14, 10, 8, 0, 0, Math.PI * 2);
    ctx.fill();

    // Tube
    ctx.fillStyle = '#3a4a5a';
    ctx.fillRect(bodyX - 9, bodyTop + 28, 18, tubeH);

    // Objective revolver
    const revolverY = bodyTop + 28 + tubeH;
    ctx.fillStyle = '#2a3848';
    ctx.beginPath();
    ctx.arc(bodyX, revolverY, 22, 0, Math.PI * 2);
    ctx.fill();
    // Current objective label
    ctx.fillStyle = '#84CC16';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(obj.label, bodyX, revolverY + 4);

    // Stage
    const stageY = revolverY + 40;
    ctx.fillStyle = '#2a3848';
    ctx.fillRect(bodyX - 70, stageY, 140, 10);

    // Arm
    ctx.fillStyle = '#4a5a6a';
    ctx.fillRect(bodyX + 26, bodyTop + 20, 14, stageY - bodyTop - 20);

    // Base
    ctx.fillStyle = '#2a3848';
    ctx.beginPath();
    ctx.ellipse(bodyX, h - 30, 70, 18, 0, 0, Math.PI * 2);
    ctx.fill();

    // ---- Field of view circle (eyepiece view on right side) ----
    const viewCX = w * 0.72;
    const viewCY = h * 0.5;
    const viewR = Math.min(w * 0.22, h * 0.36);

    // Outer ring
    ctx.fillStyle = '#111820';
    ctx.beginPath();
    ctx.arc(viewCX, viewCY, viewR + 10, 0, Math.PI * 2);
    ctx.fill();

    // Light intensity from diaphragm
    const brightness = 0.12 + diaphragm * 0.68;
    ctx.fillStyle = `rgba(${Math.round(brightness * 240)},${Math.round(brightness * 230)},${Math.round(brightness * 200)},1)`;
    ctx.beginPath();
    ctx.arc(viewCX, viewCY, viewR, 0, Math.PI * 2);
    ctx.fill();

    // Clip and draw slide content
    SLIDES[slideKey].draw(ctx, viewCX, viewCY, viewR * 0.95, focusOffset);

    // Vignette
    const vig = ctx.createRadialGradient(viewCX, viewCY, viewR * 0.55, viewCX, viewCY, viewR);
    vig.addColorStop(0, 'rgba(0,0,0,0)');
    vig.addColorStop(1, 'rgba(0,0,0,0.55)');
    ctx.fillStyle = vig;
    ctx.beginPath();
    ctx.arc(viewCX, viewCY, viewR, 0, Math.PI * 2);
    ctx.fill();

    // Crosshairs
    ctx.strokeStyle = 'rgba(200,220,200,0.18)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 5]);
    ctx.beginPath();
    ctx.moveTo(viewCX - viewR, viewCY);
    ctx.lineTo(viewCX + viewR, viewCY);
    ctx.moveTo(viewCX, viewCY - viewR);
    ctx.lineTo(viewCX, viewCY + viewR);
    ctx.stroke();
    ctx.setLineDash([]);

    // Eyepiece ring outline
    ctx.strokeStyle = '#4a6080';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(viewCX, viewCY, viewR + 4, 0, Math.PI * 2);
    ctx.stroke();

    // Focus indicator bar
    const barX = viewCX - viewR + 8;
    const barY = viewCY + viewR - 22;
    const barW = viewR * 2 - 16;
    ctx.fillStyle = 'rgba(0,0,0,0.45)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(barX, barY, barW, 14, 4);
    else ctx.rect(barX, barY, barW, 14);
    ctx.fill();
    const sharpColor = sharpness > 0.7 ? '#84CC16' : sharpness > 0.35 ? '#F59E0B' : '#ef4444';
    ctx.fillStyle = sharpColor;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(barX, barY, barW * sharpness, 14, 4);
    else ctx.rect(barX, barY, barW * sharpness, 14);
    ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`Focus: ${Math.round(sharpness * 100)}%`, barX + 4, barY + 10);

    // Labels
    ctx.fillStyle = 'rgba(220,235,255,0.85)';
    ctx.font = '600 11px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Eyepiece view', viewCX - viewR + 4, viewCY - viewR - 6);

    // Labels on microscope body parts
    const labelPairs = [
      [bodyX + 28, bodyTop + 10, 'Eyepiece (10×)'],
      [bodyX + 28, revolverY, `Objective (${obj.label})`],
      [bodyX + 28, stageY + 5, 'Stage'],
      [bodyX + 28, stageY + 32, 'Condenser'],
    ];
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillStyle = 'rgba(180,210,255,0.75)';
    labelPairs.forEach(([lx, ly, txt]) => {
      ctx.beginPath();
      ctx.moveTo(bodyX + 15, ly);
      ctx.lineTo(lx - 2, ly);
      ctx.strokeStyle = 'rgba(100,150,200,0.4)';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillText(txt, lx, ly + 4);
    });

    // Update HUD and readouts
    const totalMagStr = `${totalMag}×`;
    magBadge.set(`Mag: ${totalMagStr}`);
    focusBadge.set(Math.abs(focusOffset) > 15 ? 'Use fine focus' : sharpness > 0.7 ? 'In focus!' : 'Adjust focus');
    magOut.set(totalMagStr);
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
