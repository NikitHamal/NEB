import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 9 – AI Ethics & Bias
// Demonstrates how biased training data skews a classifier's predictions.
// Shows hiring-rate disparity across groups when training data is skewed.
// Accurate, responsible framing.

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Bias Explorer', '#6366F1');

  // Simulation: a hiring classifier trained on historical data
  // Group A (majority) and Group B (minority) with controllable historical bias
  // Feature: "score" (0-100), true positive rate threshold

  let biasSlider = 20;   // % extra acceptance for group A in training data
  let threshold = 60;    // classifier score threshold
  let sampleN = 60;      // points per group
  let showFairMetrics = true;

  // Generate biased training data
  function generateData(bias) {
    const data = [];
    const rng = mulberry32(42);
    for (let i = 0; i < sampleN; i++) {
      // Group A: centered at score 65 (majority, historically over-represented)
      const scoreA = Math.max(0, Math.min(100, 65 + (rng() - 0.5) * 40));
      // Outcome biased: higher if group A and score in middle range
      const qualifiedA = scoreA > (55 - bias * 0.4);
      data.push({ group: 'A', score: scoreA, qualified: qualifiedA, label: qualifiedA ? 'hired' : 'rejected' });

      // Group B: same underlying ability distribution, but historically under-represented
      const scoreB = Math.max(0, Math.min(100, 62 + (rng() - 0.5) * 40));
      // Outcome biased: requires higher score due to historical discrimination
      const qualifiedB = scoreB > (55 + bias * 0.4);
      data.push({ group: 'B', score: scoreB, qualified: qualifiedB, label: qualifiedB ? 'hired' : 'rejected' });
    }
    return data;
  }

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  // Train a simple logistic regression on biased data, then predict
  function trainClassifier(data) {
    // Simple threshold-based "model" trained on biased data
    // In a fair world, threshold should be the same for both groups.
    // With bias, the training data leads to different effective thresholds.
    const biasEffect = biasSlider / 100;
    return {
      predict: (group, score) => {
        // Model learned implicit bias: slightly lower bar for A
        const adjThreshold = group === 'A'
          ? threshold - biasEffect * 15
          : threshold + biasEffect * 15;
        return score >= adjThreshold;
      },
    };
  }

  function computeMetrics(data, model) {
    const groups = ['A', 'B'];
    return groups.map((g) => {
      const grp = data.filter((d) => d.group === g);
      const predicted = grp.map((d) => ({ ...d, pred: model.predict(g, d.score) }));
      const accepted = predicted.filter((d) => d.pred).length;
      const rejected = predicted.filter((d) => !d.pred).length;
      const truePositive = predicted.filter((d) => d.pred && d.qualified).length;
      const falsePositive = predicted.filter((d) => d.pred && !d.qualified).length;
      const trueNegative = predicted.filter((d) => !d.pred && !d.qualified).length;
      const falseNegative = predicted.filter((d) => !d.pred && d.qualified).length;
      const precision = accepted > 0 ? truePositive / accepted : 0;
      const recall = (truePositive + falseNegative) > 0 ? truePositive / (truePositive + falseNegative) : 0;
      const acceptanceRate = accepted / grp.length;
      return { group: g, accepted, rejected, acceptanceRate, precision, recall, truePositive, falsePositive };
    });
  }

  const panel = createPanel(stage, { title: 'Bias Controls' });
  panel.slider({
    label: 'Historical bias strength',
    min: 0, max: 50, step: 1, value: biasSlider,
    format: (v) => `${v}%`,
    onChange: (v) => { biasSlider = v; },
  });
  panel.slider({
    label: 'Classifier threshold',
    min: 30, max: 90, step: 1, value: threshold,
    format: (v) => v.toFixed(0),
    onChange: (v) => { threshold = v; },
  });
  panel.toggle({
    label: 'Show fairness metrics',
    value: true,
    onChange: (v) => { showFairMetrics = v; },
  });
  panel.divider();
  const rateAOut = panel.readout({ label: 'Group A accept rate', value: '—' });
  const rateBOut = panel.readout({ label: 'Group B accept rate', value: '—' });
  const dispOut = panel.readout({ label: 'Disparity ratio', value: '—' });
  panel.info('Disparity ratio < 0.8 is considered discriminatory under the "80% rule" (US EEOC). Increase historical bias to watch it drop.');

  const COLORS = { A: '#6366F1', B: '#F59E0B' };

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);

    const data = generateData(biasSlider);
    const model = trainClassifier(data);
    const metrics = computeMetrics(data, model);
    const [mA, mB] = metrics;

    // Score distributions (histogram)
    const histX = 16, histY = 50, histW = w * 0.58, histH = Math.min(h * 0.4, 160);
    const bins = 20;
    const binW = 100 / bins;

    function buildHist(group) {
      const hist = new Array(bins).fill(0);
      data.filter((d) => d.group === group).forEach(({ score }) => {
        const b = Math.min(bins - 1, Math.floor(score / binW));
        hist[b]++;
      });
      return hist;
    }

    const histA = buildHist('A');
    const histB = buildHist('B');
    const maxH = Math.max(...histA, ...histB, 1);

    // Title
    ctx.fillStyle = 'rgba(199,212,234,0.8)'; ctx.font = 'bold 12px Poppins,sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('Score distributions (same underlying ability):', histX, histY - 8);

    // Draw histograms
    for (let i = 0; i < bins; i++) {
      const bx = histX + i * (histW / bins);
      const bwPx = histW / bins - 2;
      const score = i * binW;
      const isPastThreshold = score >= threshold;

      // Group A
      const hA = (histA[i] / maxH) * (histH - 20);
      ctx.fillStyle = isPastThreshold ? COLORS.A : COLORS.A + '55';
      ctx.fillRect(bx, histY + histH - hA, bwPx / 2 - 1, hA);

      // Group B
      const hB = (histB[i] / maxH) * (histH - 20);
      ctx.fillStyle = isPastThreshold ? COLORS.B : COLORS.B + '55';
      ctx.fillRect(bx + bwPx / 2 + 1, histY + histH - hB, bwPx / 2 - 1, hB);
    }

    // Threshold line
    const threshX = histX + (threshold / 100) * histW;
    ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 2; ctx.setLineDash([6, 4]);
    ctx.beginPath(); ctx.moveTo(threshX, histY - 4); ctx.lineTo(threshX, histY + histH); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#f43f5e'; ctx.font = 'bold 11px Poppins,sans-serif'; ctx.textAlign = 'center';
    ctx.fillText(`Threshold: ${threshold}`, threshX, histY - 10);

    // Axis
    ctx.strokeStyle = 'rgba(165,180,252,0.4)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(histX, histY + histH); ctx.lineTo(histX + histW, histY + histH); ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '10px Poppins,sans-serif'; ctx.textAlign = 'center';
    [0,25,50,75,100].forEach((v) => {
      const sx = histX + (v / 100) * histW;
      ctx.fillText(v, sx, histY + histH + 14);
    });
    ctx.fillText('Score', histX + histW / 2, histY + histH + 28);

    // Legend
    ctx.fillStyle = COLORS.A; ctx.fillRect(histX, histY + histH + 34, 12, 10);
    ctx.fillStyle = '#e8eefb'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('Group A (majority)', histX + 16, histY + histH + 44);
    ctx.fillStyle = COLORS.B; ctx.fillRect(histX + 140, histY + histH + 34, 12, 10);
    ctx.fillText('Group B (minority)', histX + 156, histY + histH + 44);

    // Acceptance rate bars
    const barSectionY = histY + histH + 58;
    ctx.fillStyle = 'rgba(199,212,234,0.8)'; ctx.font = 'bold 12px Poppins,sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('Acceptance rates:', histX, barSectionY);
    [mA, mB].forEach((m, i) => {
      const by = barSectionY + 14 + i * 26;
      ctx.fillStyle = 'rgba(255,255,255,0.07)';
      ctx.fillRect(histX, by, histW * 0.75, 18);
      ctx.fillStyle = COLORS[m.group];
      ctx.fillRect(histX, by, m.acceptanceRate * histW * 0.75, 18);
      ctx.fillStyle = '#e8eefb'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(`Group ${m.group}: ${(m.acceptanceRate * 100).toFixed(0)}% hired`, histX + 4, by + 13);
    });

    // Fairness metrics panel
    if (showFairMetrics) {
      const fmX = w * 0.6, fmY = 50, fmW = w - fmX - 10;
      ctx.fillStyle = 'rgba(8,16,30,0.7)';
      if (ctx.roundRect) ctx.roundRect(fmX, fmY, fmW, h - 60, 8);
      else ctx.rect(fmX, fmY, fmW, h - 60);
      ctx.fill();
      ctx.strokeStyle = 'rgba(165,180,252,0.2)'; ctx.lineWidth = 1; ctx.stroke();

      ctx.fillStyle = 'rgba(199,212,234,0.9)'; ctx.font = 'bold 12px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('Fairness Metrics', fmX + 8, fmY + 18);

      const disparity = mB.acceptanceRate / (mA.acceptanceRate + 0.001);
      const items = [
        { label: 'A accept rate', val: `${(mA.acceptanceRate * 100).toFixed(0)}%`, good: null },
        { label: 'B accept rate', val: `${(mB.acceptanceRate * 100).toFixed(0)}%`, good: null },
        { label: 'Disparity ratio', val: disparity.toFixed(2), good: disparity >= 0.8 },
        { label: 'A precision', val: `${(mA.precision * 100).toFixed(0)}%`, good: null },
        { label: 'B precision', val: `${(mB.precision * 100).toFixed(0)}%`, good: null },
        { label: 'A recall (TPR)', val: `${(mA.recall * 100).toFixed(0)}%`, good: null },
        { label: 'B recall (TPR)', val: `${(mB.recall * 100).toFixed(0)}%`, good: null },
      ];
      items.forEach(({ label, val, good }, i) => {
        const iy = fmY + 32 + i * 22;
        ctx.fillStyle = 'rgba(199,212,234,0.6)'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'left';
        ctx.fillText(label + ':', fmX + 8, iy);
        ctx.fillStyle = good === null ? '#e8eefb' : good ? '#6ee7b7' : '#fca5a5';
        ctx.font = 'bold 11px Poppins,sans-serif'; ctx.textAlign = 'right';
        ctx.fillText(val, fmX + fmW - 8, iy);
      });

      // EEOC 80% rule explanation
      const explY = fmY + 32 + items.length * 22 + 10;
      ctx.fillStyle = disparity < 0.8 ? '#fca5a5' : '#6ee7b7';
      ctx.font = 'bold 11px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(disparity < 0.8 ? '⚠ Disparate impact!' : '✓ Within 80% rule', fmX + 8, explY);

      ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '10px Poppins,sans-serif';
      const wrapText = (text, x, y, maxW, lineH) => {
        const words2 = text.split(' ');
        let line = '';
        let yy = y;
        for (const word of words2) {
          const test = line + word + ' ';
          if (ctx.measureText(test).width > maxW && line) {
            ctx.fillText(line, x, yy); line = word + ' '; yy += lineH;
          } else line = test;
        }
        ctx.fillText(line, x, yy);
      };
      wrapText('Disparity < 0.8 means Group B is less than 80% as likely to be hired as Group A. This is a legal threshold in employment law.', fmX + 8, explY + 14, fmW - 16, 14);

      // What to do section
      const fixY = explY + 70;
      ctx.fillStyle = 'rgba(165,180,252,0.8)'; ctx.font = 'bold 11px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('Mitigation strategies:', fmX + 8, fixY);
      const fixes = ['Re-sample training data', 'Use fairness constraints', 'Audit model output', 'Diverse data collection'];
      fixes.forEach((f, i) => {
        ctx.fillStyle = 'rgba(199,212,234,0.55)'; ctx.font = '10px Poppins,sans-serif';
        ctx.fillText('• ' + f, fmX + 8, fixY + 14 + i * 14);
      });
    }

    rateAOut.set(`${(mA.acceptanceRate * 100).toFixed(0)}%`);
    rateBOut.set(`${(mB.acceptanceRate * 100).toFixed(0)}%`);
    const disp2 = mB.acceptanceRate / (mA.acceptanceRate + 0.001);
    dispOut.set(disp2.toFixed(2) + (disp2 < 0.8 ? ' ⚠' : ' ✓'));
    badge.set(biasSlider === 0 ? 'No bias — fair classifier' : `Bias: ${biasSlider}% | Disparity: ${disp2.toFixed(2)}`);
  });

  sim.start();

  return {
    dispose() { panel.dispose(); hud.dispose(); sim.dispose(); },
  };
}
