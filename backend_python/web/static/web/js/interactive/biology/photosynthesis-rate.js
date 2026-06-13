import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Hydrilla bubble-counting photosynthesis rate experiment
// Accurate limiting-factor model: rate = min(light_factor, co2_factor, temp_factor) × max_rate
// Limiting factor plateaus reproduced accurately

const CHART_POINTS = 120;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const rateBadge = hud.badge('Rate: 0 bubbles/min', '#22c55e');
  const limitBadge = hud.badge('Limiting factor: —', '#f59e0b');

  // Variables
  let lightIntensity = 50;   // 0-100 (lux equiv)
  let co2Conc = 0.04;        // % (0.01..0.2)
  let temperature = 25;      // °C (5..45)
  let running = true;

  // Bubble simulation
  let bubbleCount = 0;
  let bubbleTimer = 0;
  const bubbles = [];        // {x, y, r, age, maxAge}

  // Chart
  const chartY = new Float32Array(CHART_POINTS).fill(0);
  let chartHead = 0;
  let chartCount = 0;
  let chartTimer = 0;
  let elapsed = 0;

  function computeRate() {
    // Light factor: logarithmic saturation (light compensation ~5%, saturation ~80%)
    const lightFac = Math.min(1, Math.log(1 + lightIntensity * 0.12) / Math.log(1 + 0.12 * 100));
    // CO₂ factor: Michaelis-Menten style (Km ~ 0.04%)
    const co2Fac = co2Conc / (co2Conc + 0.03);
    // Temperature factor: bell-curve, optimum ~30°C, denatures >40°C
    const optTemp = 30;
    const tempFac = Math.exp(-Math.pow((temperature - optTemp) / 9, 2));
    const rawRate = lightFac * co2Fac * tempFac;
    return { rate: rawRate * 45, lightFac, co2Fac, tempFac, lightIntensity, co2Conc, temperature };
  }

  function limitingFactor(lf, cf, tf) {
    const m = Math.min(lf, cf, tf);
    if (m === lf && lf < 0.98) return 'Light intensity';
    if (m === cf && cf < 0.98) return 'CO₂ concentration';
    if (m === tf && tf < 0.98) return 'Temperature';
    return 'None (all adequate)';
  }

  const panel = createPanel(stage, { title: 'Photosynthesis Controls' });

  const lightCtrl = panel.slider({
    label: 'Light intensity',
    min: 0, max: 100, step: 1, value: lightIntensity,
    format: (v) => `${v} klux`,
    onChange: (v) => { lightIntensity = v; },
  });
  const co2Ctrl = panel.slider({
    label: 'CO₂ concentration',
    min: 0.01, max: 0.20, step: 0.005, value: co2Conc,
    format: (v) => `${(v * 100).toFixed(2)}%`,
    onChange: (v) => { co2Conc = v; },
  });
  const tempCtrl = panel.slider({
    label: 'Temperature',
    min: 5, max: 45, step: 1, value: temperature,
    format: (v) => `${v} °C`,
    onChange: (v) => { temperature = v; },
  });
  panel.toggle({
    label: 'Run experiment',
    value: true,
    onChange: (v) => { running = v; },
  });
  panel.divider();
  const rateOut = panel.readout({ label: 'O₂ bubble rate', value: '0 bubbles/min' });
  const limitOut = panel.readout({ label: 'Limiting factor', value: '—' });
  panel.info('Based on Hydrilla (water weed) bubble counting. Rate is controlled by the most limiting factor — just like in real experiments. Raise each variable to see where the plateau is.');

  sim.setUpdate((ctx, dt, w, h) => {
    const { rate, lightFac, co2Fac, tempFac } = computeRate();
    const bubblesPerMin = rate;
    const bubblesPerSec = bubblesPerMin / 60;

    if (running) {
      elapsed += dt;
      bubbleTimer += dt;
      const interval = bubblesPerSec > 0 ? 1 / bubblesPerSec : 9999;
      while (bubbleTimer > interval && interval < 9999) {
        bubbleTimer -= interval;
        bubbles.push({
          x: w * 0.38 + (Math.random() - 0.5) * 30,
          y: h * 0.58,
          r: 3 + Math.random() * 3,
          age: 0,
          maxAge: 2 + Math.random(),
          vx: (Math.random() - 0.5) * 6,
        });
        bubbleCount++;
      }
      // Move bubbles
      for (const b of bubbles) {
        b.age += dt;
        b.y -= 28 * dt;
        b.x += b.vx * dt;
      }
      // Remove old
      for (let i = bubbles.length - 1; i >= 0; i--) {
        if (bubbles[i].age > bubbles[i].maxAge) bubbles.splice(i, 1);
      }

      chartTimer += dt;
      if (chartTimer > 0.5) {
        chartTimer = 0;
        chartY[chartHead] = bubblesPerMin;
        chartHead = (chartHead + 1) % CHART_POINTS;
        if (chartCount < CHART_POINTS) chartCount++;
      }
    }

    const lf = limitingFactor(lightFac, co2Fac, tempFac);
    rateOut.set(`${bubblesPerMin.toFixed(1)} bubbles/min`);
    limitOut.set(lf);
    rateBadge.set(`Rate: ${bubblesPerMin.toFixed(0)} b/min`);
    limitBadge.set(`Limit: ${lf.split(' ')[0]}`);

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#0a1a10');
    bg.addColorStop(1, '#071510');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    // ---- Water container ----
    const contX = w * 0.22;
    const contY = h * 0.12;
    const contW = w * 0.32;
    const contH = h * 0.68;

    // Water
    ctx.fillStyle = 'rgba(30,80,120,0.5)';
    ctx.fillRect(contX, contY + contH * 0.08, contW, contH * 0.92);

    // Beaker outline
    ctx.strokeStyle = 'rgba(150,200,255,0.7)';
    ctx.lineWidth = 2;
    ctx.strokeRect(contX, contY, contW, contH);

    // Hydrilla plant
    const plantX = contX + contW / 2;
    const plantY = contY + contH * 0.85;
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 2.5;
    // Stem
    ctx.beginPath();
    ctx.moveTo(plantX, plantY);
    ctx.lineTo(plantX, plantY - contH * 0.48);
    ctx.stroke();
    // Leaves
    for (let i = 0; i < 6; i++) {
      const leafY = plantY - i * contH * 0.08;
      const side = i % 2 === 0 ? 1 : -1;
      ctx.beginPath();
      ctx.moveTo(plantX, leafY);
      ctx.quadraticCurveTo(plantX + side * 28, leafY - 12, plantX + side * 22, leafY - 22);
      ctx.stroke();
    }

    // Light rays if light > 0
    if (lightIntensity > 5) {
      const rayAlpha = lightIntensity / 150;
      ctx.strokeStyle = `rgba(255,240,100,${rayAlpha})`;
      ctx.lineWidth = 1.5;
      for (let i = 0; i < 5; i++) {
        const rx = contX + (i / 4) * contW;
        ctx.beginPath();
        ctx.moveTo(rx, contY - 20);
        ctx.lineTo(rx + (Math.random() - 0.5) * 6, contY);
        ctx.stroke();
      }
    }

    // Bubbles
    for (const b of bubbles) {
      const alpha = Math.max(0, 1 - b.age / b.maxAge);
      ctx.strokeStyle = `rgba(180,230,255,${alpha * 0.85})`;
      ctx.fillStyle = `rgba(200,240,255,${alpha * 0.25})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    // O₂ label at top
    ctx.fillStyle = 'rgba(100,220,150,0.8)';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('O₂ bubbles', contX + contW / 2, contY - 6);

    // ---- Factor bar chart ----
    const barStartX = w * 0.62;
    const barAreaW = w * 0.35;
    const barAreaH = h * 0.55;
    const barAreaY = h * 0.08;

    ctx.fillStyle = 'rgba(8,16,10,0.6)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(barStartX, barAreaY, barAreaW, barAreaH, 6);
    else ctx.rect(barStartX, barAreaY, barAreaW, barAreaH);
    ctx.fill();

    ctx.fillStyle = 'rgba(180,230,200,0.7)';
    ctx.font = '700 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Limiting factors', barStartX + barAreaW / 2, barAreaY + 13);

    const factors = [
      { label: 'Light', value: lightFac, color: '#fbbf24' },
      { label: 'CO₂', value: co2Fac, color: '#22c55e' },
      { label: 'Temp', value: tempFac, color: '#f87171' },
    ];
    const barW = barAreaW * 0.18;
    const maxBarH = barAreaH * 0.72;
    factors.forEach((f, i) => {
      const bx = barStartX + barAreaW * (0.18 + i * 0.27);
      const by = barAreaY + barAreaH * 0.88 - f.value * maxBarH;
      ctx.fillStyle = f.color;
      ctx.fillRect(bx - barW / 2, by, barW, f.value * maxBarH);
      ctx.fillStyle = 'rgba(220,240,220,0.8)';
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(f.label, bx, barAreaY + barAreaH * 0.95);
      ctx.fillText(`${(f.value * 100).toFixed(0)}%`, bx, by - 3);
    });

    // Rate chart
    const chartAreaY2 = barAreaY + barAreaH + 8;
    const chartAreaH2 = h - chartAreaY2 - 8;
    if (chartCount > 1) {
      ctx.fillStyle = 'rgba(8,16,10,0.55)';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(barStartX, chartAreaY2, barAreaW, chartAreaH2, 6);
      else ctx.rect(barStartX, chartAreaY2, barAreaW, chartAreaH2);
      ctx.fill();

      ctx.fillStyle = 'rgba(150,220,160,0.7)';
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('Rate (b/min) over time', barStartX + 4, chartAreaY2 + 11);

      const maxRate = 50;
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      for (let i = 0; i < chartCount; i++) {
        const idx = (chartHead - chartCount + i + CHART_POINTS) % CHART_POINTS;
        const px = barStartX + 4 + (i / Math.max(1, chartCount - 1)) * (barAreaW - 8);
        const py = chartAreaY2 + chartAreaH2 - 8 - (chartY[idx] / maxRate) * (chartAreaH2 - 16);
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
      }
      ctx.stroke();
    }

    // Title
    ctx.fillStyle = 'rgba(150,240,160,0.85)';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Hydrilla Photosynthesis Rate', 10, 18);
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
