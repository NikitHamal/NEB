import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Enzyme activity simulation — catalase / amylase
// Accurate: bell-curve temperature (optimum ~37°C for catalase, denaturation >50°C)
// Bell-curve pH (optimum pH 7 for catalase, pH 5 for amylase)
// Michaelis-Menten substrate concentration → Vmax saturation

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const activityBadge = hud.badge('Activity: 100%', '#22c55e');

  let temperature = 37;     // °C
  let pH = 7.0;             // 1-14
  let substrate = 50;       // 0-100% of Km
  let enzymeType = 'catalase'; // catalase | amylase
  let elapsed = 0;

  // Product accumulated
  let product = 0;
  let running = true;

  function getEnzymeParams() {
    if (enzymeType === 'catalase') {
      return { optTemp: 37, optPH: 7.0, tempWidth: 12, pHWidth: 1.8, maxVmax: 100 };
    } else {
      // Amylase: optimum ~37°C, pH 6.8-7.0 (salivary), but optimal around pH 6.7-7.0
      return { optTemp: 37, optPH: 6.8, tempWidth: 11, pHWidth: 1.5, maxVmax: 80 };
    }
  }

  function computeActivity() {
    const p = getEnzymeParams();
    // Temperature bell curve (asymmetric — steep drop after denaturation)
    let tempFac;
    if (temperature <= p.optTemp) {
      tempFac = Math.exp(-Math.pow((temperature - p.optTemp) / p.tempWidth, 2));
    } else {
      // Steeper drop above optimum (denaturation)
      const excess = temperature - p.optTemp;
      tempFac = Math.exp(-Math.pow(excess / (p.tempWidth * 0.7), 2));
    }
    // pH bell curve
    const pHFac = Math.exp(-Math.pow((pH - p.optPH) / p.pHWidth, 2));
    // Michaelis-Menten: v = Vmax × [S] / (Km + [S]), normalised
    const s = substrate / 100;
    const Km_norm = 0.3;
    const substFac = s / (Km_norm + s);
    const activity = tempFac * pHFac * substFac * 100;
    return { activity, tempFac, pHFac, substFac };
  }

  const panel = createPanel(stage, { title: 'Enzyme Lab' });

  panel.select({
    label: 'Enzyme',
    options: [
      { value: 'catalase', label: 'Catalase (H₂O₂ → H₂O + O₂)' },
      { value: 'amylase', label: 'Amylase (starch → maltose)' },
    ],
    value: 'catalase',
    onChange: (v) => { enzymeType = v; product = 0; },
  });
  panel.slider({
    label: 'Temperature',
    min: 10, max: 70, step: 1, value: temperature,
    format: (v) => `${v} °C`,
    onChange: (v) => { temperature = v; },
  });
  panel.slider({
    label: 'pH',
    min: 1.0, max: 13.0, step: 0.1, value: pH,
    format: (v) => `pH ${v.toFixed(1)}`,
    onChange: (v) => { pH = v; },
  });
  panel.slider({
    label: 'Substrate concentration',
    min: 1, max: 100, step: 1, value: substrate,
    format: (v) => `${v}%`,
    onChange: (v) => { substrate = v; },
  });
  panel.toggle({
    label: 'Run reaction',
    value: true,
    onChange: (v) => { running = v; },
  });
  panel.divider();
  const actOut = panel.readout({ label: 'Relative activity', value: '100%' });
  const prodOut = panel.readout({ label: 'Product formed', value: '0 units' });
  panel.button({
    label: 'Reset',
    icon: 'replay',
    onClick: () => { product = 0; elapsed = 0; },
  });
  panel.info('Temperature bell curve: activity rises with temperature (faster molecular motion) until the enzyme denatures above ~50°C. pH affects the charge of active site amino acids. Substrate concentration follows Michaelis-Menten — saturates at Vmax.');

  // Curve data for display
  const N_CURVE = 60;
  const tempCurveX = new Float32Array(N_CURVE);
  const tempCurveY = new Float32Array(N_CURVE);
  const pHCurveX = new Float32Array(N_CURVE);
  const pHCurveY = new Float32Array(N_CURVE);
  const mmCurveX = new Float32Array(N_CURVE);
  const mmCurveY = new Float32Array(N_CURVE);

  function precomputeCurves() {
    const p = getEnzymeParams();
    for (let i = 0; i < N_CURVE; i++) {
      const t = 10 + (i / (N_CURVE - 1)) * 60;
      tempCurveX[i] = t;
      let tf;
      if (t <= p.optTemp) tf = Math.exp(-Math.pow((t - p.optTemp) / p.tempWidth, 2));
      else tf = Math.exp(-Math.pow((t - p.optTemp) / (p.tempWidth * 0.7), 2));
      tempCurveY[i] = tf;

      const ph2 = 1 + (i / (N_CURVE - 1)) * 12;
      pHCurveX[i] = ph2;
      pHCurveY[i] = Math.exp(-Math.pow((ph2 - p.optPH) / p.pHWidth, 2));

      const s = (i / (N_CURVE - 1));
      mmCurveX[i] = s * 100;
      mmCurveY[i] = s / (0.3 + s);
    }
  }

  sim.setUpdate((ctx, dt, w, h) => {
    precomputeCurves();
    const { activity, tempFac, pHFac, substFac } = computeActivity();

    if (running) {
      elapsed += dt;
      product += activity * dt * 0.08;
    }

    actOut.set(`${activity.toFixed(1)}%`);
    prodOut.set(`${product.toFixed(0)} units`);
    activityBadge.set(`Activity: ${activity.toFixed(0)}%`);

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#071510');
    bg.addColorStop(1, '#0a1205');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    ctx.fillStyle = 'rgba(150,230,160,0.85)';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Enzyme Activity Lab', 10, 18);

    // Current conditions panel
    ctx.fillStyle = 'rgba(8,20,10,0.7)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(10, 28, w * 0.55, h * 0.12, 6);
    else ctx.rect(10, 28, w * 0.55, h * 0.12);
    ctx.fill();

    const condY = 28 + h * 0.04;
    const conditions = [
      { label: `Temp: ${temperature}°C`, fac: tempFac, color: '#f87171' },
      { label: `pH ${pH.toFixed(1)}`, fac: pHFac, color: '#7dd3fc' },
      { label: `[S]: ${substrate}%`, fac: substFac, color: '#fbbf24' },
      { label: `Activity: ${activity.toFixed(0)}%`, fac: activity / 100, color: '#22c55e' },
    ];
    conditions.forEach((c, i) => {
      const cx2 = 20 + i * (w * 0.14);
      ctx.fillStyle = c.color;
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(c.label, cx2, condY - 4);
      // Mini bar
      ctx.fillStyle = 'rgba(30,60,30,0.8)';
      ctx.fillRect(cx2, condY + 2, 50, 6);
      ctx.fillStyle = c.color;
      ctx.fillRect(cx2, condY + 2, c.fac * 50, 6);
    });

    // Helper to draw a curve
    function drawCurve(data_x, data_y, curX, curY, areaX, areaY, areaW, areaH, xLabel, yLabel, cursorVal, color) {
      ctx.fillStyle = 'rgba(8,20,10,0.65)';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(areaX, areaY, areaW, areaH, 6);
      else ctx.rect(areaX, areaY, areaW, areaH);
      ctx.fill();

      ctx.fillStyle = 'rgba(150,220,160,0.6)';
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(yLabel, areaX + areaW / 2, areaY + 10);

      const padL = 10, padR = 10, padT = 16, padB = 18;
      const pw = areaW - padL - padR;
      const ph2 = areaH - padT - padB;
      const gx = areaX + padL;
      const gy = areaY + padT;

      // Axes
      ctx.strokeStyle = 'rgba(100,180,100,0.3)';
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(gx, gy + ph2);
      ctx.lineTo(gx + pw, gy + ph2);
      ctx.moveTo(gx, gy);
      ctx.lineTo(gx, gy + ph2);
      ctx.stroke();

      // Curve
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      for (let i = 0; i < N_CURVE; i++) {
        const px2 = gx + ((data_x[i] - data_x[0]) / (data_x[N_CURVE - 1] - data_x[0])) * pw;
        const py2 = gy + (1 - data_y[i]) * ph2;
        i === 0 ? ctx.moveTo(px2, py2) : ctx.lineTo(px2, py2);
      }
      ctx.stroke();

      // Current value marker
      const normX = (cursorVal - data_x[0]) / (data_x[N_CURVE - 1] - data_x[0]);
      const markerX = gx + normX * pw;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.setLineDash([2, 3]);
      ctx.beginPath();
      ctx.moveTo(markerX, gy);
      ctx.lineTo(markerX, gy + ph2);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = 'rgba(200,240,200,0.6)';
      ctx.font = '600 8px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(xLabel, areaX + areaW / 2, areaY + areaH - 4);
    }

    const curveAreaH = h * 0.22;
    const curveAreaW = w * 0.32;
    const curveY2 = h * 0.24;

    drawCurve(tempCurveX, tempCurveY, temperature, tempFac,
      w * 0.03, curveY2, curveAreaW, curveAreaH,
      `Temperature (10-70°C) — current: ${temperature}°C`, 'Activity vs Temperature', temperature, '#f87171');

    drawCurve(pHCurveX, pHCurveY, pH, pHFac,
      w * 0.37, curveY2, curveAreaW, curveAreaH,
      `pH (1-13) — current: ${pH.toFixed(1)}`, 'Activity vs pH', pH, '#7dd3fc');

    drawCurve(mmCurveX, mmCurveY, substrate, substFac,
      w * 0.67, curveY2, curveAreaW, curveAreaH,
      `[S] — current: ${substrate}%`, 'Michaelis-Menten ([S] vs rate)', substrate, '#fbbf24');

    // Product accumulation bar
    const barAreaY2 = curveY2 + curveAreaH + 8;
    const barAreaH2 = h - barAreaY2 - 10;
    ctx.fillStyle = 'rgba(8,20,10,0.6)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(10, barAreaY2, w - 20, barAreaH2, 6);
    else ctx.rect(10, barAreaY2, w - 20, barAreaH2);
    ctx.fill();

    ctx.fillStyle = 'rgba(150,230,160,0.65)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`Product accumulation (${enzymeType === 'catalase' ? 'O₂ produced' : 'maltose produced'})`, 18, barAreaY2 + 12);

    const maxProd = 500;
    const fillFrac = Math.min(1, product / maxProd);
    ctx.fillStyle = 'rgba(30,60,30,0.8)';
    ctx.fillRect(18, barAreaY2 + 18, w - 36, barAreaH2 - 24);
    const prodGrad = ctx.createLinearGradient(18, 0, 18 + fillFrac * (w - 36), 0);
    prodGrad.addColorStop(0, '#22c55e');
    prodGrad.addColorStop(1, '#86efac');
    ctx.fillStyle = prodGrad;
    ctx.fillRect(18, barAreaY2 + 18, fillFrac * (w - 36), barAreaH2 - 24);
    ctx.fillStyle = 'rgba(220,255,220,0.85)';
    ctx.font = '700 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${product.toFixed(0)} / ${maxProd} units`, w / 2, barAreaY2 + 18 + (barAreaH2 - 24) / 2 + 4);
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
