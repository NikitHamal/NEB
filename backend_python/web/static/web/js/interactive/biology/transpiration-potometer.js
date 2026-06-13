import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Bubble potometer sim — accurate effects of wind, humidity, light, temperature on transpiration rate

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const rateBadge = hud.badge('Rate: 0 mm/min', '#7dd3fc');

  let wind = 30;        // 0-100
  let humidity = 50;    // 0-100 (higher = less transpiration)
  let light = 60;       // 0-100 (more light = more stomata open)
  let temp = 25;        // °C, 5-45

  // Bubble position on capillary tube (0=right side = full, 1=left = empty)
  let bubblePos = 0.1;   // proportion along capillary from right
  let elapsed = 0;
  let running = true;

  // Chart
  const CHART_POINTS = 100;
  const chartData = new Float32Array(CHART_POINTS).fill(0);
  let chartHead = 0;
  let chartCount = 0;
  let chartTimer = 0;

  function computeRate() {
    // Wind: increases boundary layer disruption — strong effect
    const windFac = 0.3 + (wind / 100) * 0.7;
    // Humidity: VPD (vapour pressure deficit); higher humidity = lower VPD = less transpiration
    const humFac = 1.0 - humidity / 150;
    // Light: stomata open/close — major driver
    const lightFac = 0.1 + (light / 100) * 0.9;
    // Temperature: Q10 ~ 2 up to optimum, stomata close at extremes
    const optTemp = 28;
    const tempFac = Math.exp(-Math.pow((temp - optTemp) / 12, 2)) * 0.5 + 0.5;
    return windFac * humFac * lightFac * tempFac * 4.5; // mm/min
  }

  const panel = createPanel(stage, { title: 'Potometer Controls' });

  panel.slider({
    label: 'Wind speed',
    min: 0, max: 100, step: 1, value: wind,
    format: (v) => `${v} km/h`,
    onChange: (v) => { wind = v; },
  });
  panel.slider({
    label: 'Relative humidity',
    min: 10, max: 95, step: 1, value: humidity,
    format: (v) => `${v}%`,
    onChange: (v) => { humidity = v; },
  });
  panel.slider({
    label: 'Light intensity',
    min: 0, max: 100, step: 1, value: light,
    format: (v) => `${v}%`,
    onChange: (v) => { light = v; },
  });
  panel.slider({
    label: 'Temperature',
    min: 5, max: 45, step: 1, value: temp,
    format: (v) => `${v} °C`,
    onChange: (v) => { temp = v; },
  });
  panel.toggle({
    label: 'Run experiment',
    value: true,
    onChange: (v) => { running = v; },
  });
  panel.divider();
  const rateOut = panel.readout({ label: 'Water uptake rate', value: '0 mm/min' });
  const uptakeOut = panel.readout({ label: 'Total distance (mm)', value: '0.0' });
  panel.button({
    label: 'Reset potometer',
    icon: 'replay',
    onClick: () => { bubblePos = 0.1; elapsed = 0; chartHead = 0; chartCount = 0; uptakeOut.set('0.0'); },
  });
  panel.info('Wind increases transpiration by removing humid air from leaf surfaces. High humidity reduces VPD. Light opens stomata. Temperature affects enzyme activity and water viscosity.');

  sim.setUpdate((ctx, dt, w, h) => {
    const rate = computeRate();

    if (running && bubblePos < 0.98) {
      const advance = (rate / 200) * dt;  // scaled to canvas
      bubblePos = Math.min(0.98, bubblePos + advance);
      elapsed += dt;

      chartTimer += dt;
      if (chartTimer > 0.4) {
        chartTimer = 0;
        chartData[chartHead] = rate;
        chartHead = (chartHead + 1) % CHART_POINTS;
        if (chartCount < CHART_POINTS) chartCount++;
      }
    }

    const totalMm = bubblePos * 100;  // simulated mm
    rateOut.set(`${rate.toFixed(2)} mm/min`);
    uptakeOut.set(`${totalMm.toFixed(1)} mm`);
    rateBadge.set(`Rate: ${rate.toFixed(1)} mm/min`);

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#0a1628');
    bg.addColorStop(1, '#070f1a');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    // ---- Draw potometer apparatus ----
    const tubeY = h * 0.38;
    const tubeLeft = w * 0.06;
    const tubeRight = w * 0.62;
    const tubeH = 12;

    // Reservoir on the right
    const resX = tubeRight + 10;
    const resW = 28;
    const resH = 70;
    ctx.fillStyle = 'rgba(30,80,160,0.55)';
    ctx.fillRect(resX, tubeY - resH / 2, resW, resH);
    ctx.strokeStyle = 'rgba(150,200,255,0.7)';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(resX, tubeY - resH / 2, resW, resH);
    ctx.fillStyle = 'rgba(200,220,255,0.65)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Reservoir', resX + resW / 2, tubeY + resH / 2 + 12);

    // Capillary tube
    ctx.fillStyle = 'rgba(20,50,100,0.45)';
    ctx.fillRect(tubeLeft, tubeY - tubeH / 2, tubeRight - tubeLeft, tubeH);
    ctx.strokeStyle = 'rgba(150,200,255,0.6)';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(tubeLeft, tubeY - tubeH / 2, tubeRight - tubeLeft, tubeH);

    // Bubble (air bubble moves left as water is taken up)
    const bubX = tubeRight - bubblePos * (tubeRight - tubeLeft - 20);
    const bubR = tubeH * 0.38;
    ctx.fillStyle = 'rgba(220,240,255,0.85)';
    ctx.beginPath();
    ctx.ellipse(bubX, tubeY, bubR * 1.6, bubR, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(150,200,255,0.7)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Scale marks on tube
    ctx.strokeStyle = 'rgba(200,220,255,0.4)';
    ctx.lineWidth = 1;
    ctx.fillStyle = 'rgba(200,220,255,0.6)';
    ctx.font = '600 8px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let mm = 0; mm <= 100; mm += 10) {
      const mx = tubeRight - (mm / 100) * (tubeRight - tubeLeft - 20);
      ctx.beginPath();
      ctx.moveTo(mx, tubeY + tubeH / 2);
      ctx.lineTo(mx, tubeY + tubeH / 2 + (mm % 50 === 0 ? 10 : 5));
      ctx.stroke();
      if (mm % 20 === 0) ctx.fillText(`${mm}`, mx, tubeY + tubeH / 2 + 20);
    }
    ctx.fillStyle = 'rgba(180,210,255,0.6)';
    ctx.fillText('mm', tubeLeft - 14, tubeY + tubeH / 2 + 20);

    // Bubble position readout
    ctx.fillStyle = '#7dd3fc';
    ctx.font = '700 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`Bubble: ${totalMm.toFixed(0)} mm`, bubX, tubeY - tubeH - 8);

    // ---- Plant shoot connected to tube ----
    const stemX = tubeLeft - 5;
    const stemY = tubeY;
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(stemX, stemY);
    ctx.lineTo(stemX, stemY - h * 0.3);
    ctx.stroke();
    // Leaves
    for (let i = 0; i < 4; i++) {
      const ly = stemY - i * h * 0.075;
      const side = i % 2 === 0 ? -1 : 1;
      ctx.fillStyle = '#22c55e';
      ctx.beginPath();
      ctx.ellipse(stemX + side * 28, ly - 8, 28, 12, side * 0.4, 0, Math.PI * 2);
      ctx.fill();
      // Stomata open/close indicator
      const stoOpen = light / 100;
      ctx.strokeStyle = `rgba(50,100,50,${stoOpen})`;
      ctx.lineWidth = 0.8;
      for (let s = 0; s < 4; s++) {
        const sx = stemX + side * 16 + s * 5;
        ctx.beginPath();
        ctx.ellipse(sx, ly - 8 + (Math.random() * 4 - 2), 1.5, 1.5 * stoOpen + 0.2, 0, 0, Math.PI * 2);
        ctx.stroke();
      }
    }

    // Environmental indicators
    const envY = h * 0.12;
    const envItems = [
      { label: 'Wind', value: wind, unit: 'km/h', color: '#94a3b8', icon: '💨' },
      { label: 'Humidity', value: humidity, unit: '%', color: '#7dd3fc', icon: '💧' },
      { label: 'Light', value: light, unit: '%', color: '#fbbf24', icon: '☀️' },
      { label: 'Temp', value: temp, unit: '°C', color: '#f87171', icon: '🌡' },
    ];
    ctx.font = '600 9px Poppins, sans-serif';
    envItems.forEach((item, i) => {
      const ex = w * 0.67 + i * (w * 0.08 + 4);
      ctx.fillStyle = item.color;
      ctx.textAlign = 'center';
      ctx.fillText(item.label, ex, envY);
      ctx.fillText(`${item.value}${item.unit}`, ex, envY + 13);
    });

    // ---- Chart ----
    if (chartCount > 1) {
      const chartX2 = w * 0.64;
      const chartY2 = h * 0.55;
      const chartW = w * 0.34;
      const chartH2 = h * 0.38;

      ctx.fillStyle = 'rgba(8,16,30,0.6)';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(chartX2, chartY2, chartW, chartH2, 6);
      else ctx.rect(chartX2, chartY2, chartW, chartH2);
      ctx.fill();

      ctx.fillStyle = 'rgba(120,200,255,0.7)';
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('Transpiration rate (mm/min)', chartX2 + 4, chartY2 + 11);

      const maxRate = 5;
      ctx.strokeStyle = '#7dd3fc';
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      for (let i = 0; i < chartCount; i++) {
        const idx = (chartHead - chartCount + i + CHART_POINTS) % CHART_POINTS;
        const px = chartX2 + 4 + (i / Math.max(1, chartCount - 1)) * (chartW - 8);
        const py = chartY2 + chartH2 - 6 - (chartData[idx] / maxRate) * (chartH2 - 18);
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
      }
      ctx.stroke();
    }

    ctx.fillStyle = 'rgba(100,200,220,0.85)';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Bubble Potometer', 10, 18);
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
