import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Osmosis / potato osmometer simulation
// Accurate: net water movement follows osmotic potential difference
// Δψ = ψ_solution - ψ_cell; hypertonic → shrinks, hypotonic → swells, isotonic → no change

const CHART_POINTS = 80;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Isotonic — no net movement', '#84CC16');

  // State
  let externalConc = 0.9;  // % NaCl / sucrose equivalent (0.9 = isotonic for potato ~0.9%)
  let running = false;
  let elapsed = 0;
  let massChange = 0;      // percent change from initial
  const INITIAL_MASS = 5.0; // grams
  const CELL_CONC = 0.9;    // isotonic point for potato

  // Chart history
  const chartX = new Float32Array(CHART_POINTS).fill(0);
  const chartY = new Float32Array(CHART_POINTS).fill(0);
  let chartHead = 0;
  let chartCount = 0;
  let chartTimer = 0;

  function reset() {
    elapsed = 0;
    massChange = 0;
    chartHead = 0;
    chartCount = 0;
    chartTimer = 0;
  }

  const panel = createPanel(stage, { title: 'Osmosis Controls' });

  const concCtrl = panel.slider({
    label: 'External solution conc.',
    min: 0, max: 3, step: 0.05, value: 0.9,
    unit: '%',
    format: (v) => `${v.toFixed(2)}% (w/v)`,
    onChange: (v) => { externalConc = v; if (!running) { reset(); } },
  });

  panel.divider();
  const [startBtn, resetBtn] = panel.buttonRow([
    {
      label: 'Start',
      icon: 'play_arrow',
      variant: 'primary',
      onClick: () => { running = !running; startBtn.setLabel(running ? 'Pause' : 'Start'); },
    },
    {
      label: 'Reset',
      icon: 'replay',
      onClick: () => { running = false; startBtn.setLabel('Start'); reset(); },
    },
  ]);

  panel.divider();
  const massOut = panel.readout({ label: 'Current mass', value: `${INITIAL_MASS.toFixed(1)} g` });
  const changePctOut = panel.readout({ label: 'Mass change %', value: '0.0%' });
  const tonicOut = panel.readout({ label: 'Tonicity', value: 'Isotonic' });
  panel.info('Set concentration > 0.9% for hypertonic (potato shrinks), < 0.9% for hypotonic (potato swells), 0.9% ≈ isotonic (no change). Based on potato cell sap osmolarity.');

  function tonicityLabel(ext, cell) {
    const diff = ext - cell;
    if (Math.abs(diff) < 0.05) return 'Isotonic';
    if (diff > 0) return 'Hypertonic (water leaves cell)';
    return 'Hypotonic (water enters cell)';
  }

  // Rate of mass change: logistic curve — slows as equilibrium approaches
  function massChangeRate(ext, mc) {
    const diff = ext - CELL_CONC;
    const maxChange = diff > 0 ? -30 : 20;  // max % change
    const currentFrac = mc / maxChange;
    return diff * 2.5 * (1 - currentFrac) * 0.5;
  }

  function pushChart() {
    chartX[chartHead] = elapsed / 60; // minutes
    chartY[chartHead] = massChange;
    chartHead = (chartHead + 1) % CHART_POINTS;
    if (chartCount < CHART_POINTS) chartCount++;
  }

  sim.setUpdate((ctx, dt, w, h) => {
    if (running) {
      const rate = massChangeRate(externalConc, massChange);
      massChange += rate * dt;
      // clamp
      if (externalConc > CELL_CONC) massChange = Math.max(massChange, -35);
      else massChange = Math.min(massChange, 25);
      elapsed += dt;

      chartTimer += dt;
      if (chartTimer > 0.5) { chartTimer = 0; pushChart(); }
    }

    const currentMass = INITIAL_MASS * (1 + massChange / 100);
    massOut.set(`${currentMass.toFixed(2)} g`);
    changePctOut.set(`${massChange >= 0 ? '+' : ''}${massChange.toFixed(1)}%`);
    const tonLabel = tonicityLabel(externalConc, CELL_CONC);
    tonicOut.set(tonLabel);
    statusBadge.set(tonLabel);

    ctx.clearRect(0, 0, w, h);

    // ---- Draw beaker ----
    const beakerX = w * 0.28;
    const beakerBottom = h * 0.78;
    const beakerW = w * 0.28;
    const beakerH = h * 0.45;
    const beakerTop = beakerBottom - beakerH;

    // Solution colour: blue=dilute, orange=concentrated
    const frac = Math.min(1, externalConc / 3);
    const r = Math.round(100 + frac * 100);
    const b = Math.round(220 - frac * 160);
    ctx.fillStyle = `rgba(${r},180,${b},0.35)`;
    ctx.fillRect(beakerX - beakerW / 2, beakerTop + beakerH * 0.1, beakerW, beakerH * 0.9);

    // Beaker walls
    ctx.strokeStyle = 'rgba(180,210,255,0.8)';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(beakerX - beakerW / 2, beakerTop);
    ctx.lineTo(beakerX - beakerW / 2, beakerBottom);
    ctx.lineTo(beakerX + beakerW / 2, beakerBottom);
    ctx.lineTo(beakerX + beakerW / 2, beakerTop);
    ctx.stroke();

    // Concentration label
    ctx.fillStyle = 'rgba(220,235,255,0.85)';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${externalConc.toFixed(2)}% solution`, beakerX, beakerBottom + 18);

    // ---- Potato cylinder ----
    const baseW = 38;
    const baseH = 70;
    // Volume change from osmosis changes size
    const scaleFactor = 1 + massChange / 100;
    const pW = baseW * Math.pow(scaleFactor, 0.5);
    const pH = baseH * Math.pow(scaleFactor, 0.5);

    const potatoX = beakerX;
    const potatoY = beakerBottom - pH / 2 - 30;

    // Potato fill
    ctx.fillStyle = `rgba(200,160,80,${0.85 + massChange * 0.002})`;
    ctx.beginPath();
    ctx.roundRect
      ? ctx.roundRect(potatoX - pW / 2, potatoY - pH / 2, pW, pH, 6)
      : ctx.rect(potatoX - pW / 2, potatoY - pH / 2, pW, pH);
    ctx.fill();
    ctx.strokeStyle = '#8b6020';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Cell pattern inside
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 2; col++) {
        const cx = potatoX - pW / 4 + col * pW / 2;
        const cy = potatoY - pH / 3 + row * pH / 3;
        ctx.strokeStyle = 'rgba(140,90,10,0.5)';
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.ellipse(cx, cy, pW * 0.2, pH * 0.12, 0, 0, Math.PI * 2);
        ctx.stroke();
      }
    }

    // Arrow showing water movement
    const diff = CELL_CONC - externalConc;
    if (Math.abs(diff) > 0.05) {
      const arrowDir = diff > 0 ? 1 : -1; // 1=inward, -1=outward
      const arrowColor = diff > 0 ? '#7dd3fc' : '#f87171';
      ctx.fillStyle = arrowColor;
      ctx.strokeStyle = arrowColor;
      ctx.lineWidth = 2;
      for (let i = 0; i < 3; i++) {
        const oy = potatoY + (i - 1) * pH * 0.28;
        const startX = arrowDir > 0 ? beakerX - beakerW / 2 + 8 : potatoX + pW / 2;
        const endX = arrowDir > 0 ? potatoX - pW / 2 : beakerX + beakerW / 2 - 8;
        ctx.beginPath();
        ctx.moveTo(startX, oy);
        ctx.lineTo(endX, oy);
        ctx.stroke();
        // arrowhead
        const tipX = endX;
        ctx.beginPath();
        ctx.moveTo(tipX, oy);
        ctx.lineTo(tipX - arrowDir * 8, oy - 5);
        ctx.lineTo(tipX - arrowDir * 8, oy + 5);
        ctx.closePath();
        ctx.fill();
      }
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillStyle = arrowColor;
      ctx.fillText(diff > 0 ? 'H₂O in' : 'H₂O out', (beakerX - beakerW / 2 + potatoX) / 2, potatoY + pH / 2 + 14);
    }

    // ---- Mass change bar ----
    const barX = w * 0.6;
    const barY = h * 0.15;
    const barH = h * 0.6;
    const barW = 28;
    const neutral = barY + barH * 0.5;

    ctx.fillStyle = 'rgba(8,16,30,0.6)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(barX - barW / 2, barY, barW, barH, 6);
    else ctx.rect(barX - barW / 2, barY, barW, barH);
    ctx.fill();

    // Zero line
    ctx.strokeStyle = 'rgba(255,255,255,0.3)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(barX - barW / 2 - 10, neutral);
    ctx.lineTo(barX + barW / 2 + 10, neutral);
    ctx.stroke();
    ctx.setLineDash([]);

    const fillH = (massChange / 35) * barH * 0.45;
    const fillColor = massChange >= 0 ? '#7dd3fc' : '#f87171';
    ctx.fillStyle = fillColor;
    if (fillH >= 0) {
      ctx.fillRect(barX - barW / 2 + 2, neutral - fillH, barW - 4, fillH);
    } else {
      ctx.fillRect(barX - barW / 2 + 2, neutral, barW - 4, -fillH);
    }

    ctx.fillStyle = 'rgba(220,235,255,0.85)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Mass', barX, barY - 6);
    ctx.fillText('change', barX, barY + 6);
    ctx.fillText('+30%', barX - barW / 2 - 20, barY + 10);
    ctx.fillText('0', barX - barW / 2 - 12, neutral + 4);
    ctx.fillText('-30%', barX - barW / 2 - 20, barY + barH - 4);

    // ---- Chart ----
    if (chartCount > 1) {
      const chartAreaX = w * 0.63;
      const chartAreaY = h * 0.15;
      const chartAreaW = w * 0.34;
      const chartAreaH = h * 0.55;

      ctx.fillStyle = 'rgba(8,16,30,0.55)';
      ctx.strokeStyle = 'rgba(100,140,200,0.3)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(chartAreaX, chartAreaY, chartAreaW, chartAreaH, 6);
      else ctx.rect(chartAreaX, chartAreaY, chartAreaW, chartAreaH);
      ctx.fill(); ctx.stroke();

      const midChart = chartAreaY + chartAreaH / 2;
      ctx.strokeStyle = 'rgba(255,255,255,0.15)';
      ctx.setLineDash([3, 4]);
      ctx.beginPath();
      ctx.moveTo(chartAreaX + 4, midChart);
      ctx.lineTo(chartAreaX + chartAreaW - 4, midChart);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.font = '600 9px Poppins, sans-serif';
      ctx.fillStyle = 'rgba(200,220,255,0.7)';
      ctx.textAlign = 'left';
      ctx.fillText('Mass change % vs time (min)', chartAreaX + 4, chartAreaY + 11);

      const maxTime = Math.max(...Array.from({ length: chartCount }, (_, i) => {
        const idx = (chartHead - chartCount + i + CHART_POINTS) % CHART_POINTS;
        return chartX[idx];
      }), 1);

      ctx.strokeStyle = '#84CC16';
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      for (let i = 0; i < chartCount; i++) {
        const idx = (chartHead - chartCount + i + CHART_POINTS) % CHART_POINTS;
        const px = chartAreaX + 8 + (chartX[idx] / maxTime) * (chartAreaW - 16);
        const py = midChart - (chartY[idx] / 35) * (chartAreaH / 2 - 12);
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
      }
      ctx.stroke();
    }

    // Title
    ctx.fillStyle = 'rgba(220,235,255,0.85)';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Potato Osmometer', 12, 22);
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
