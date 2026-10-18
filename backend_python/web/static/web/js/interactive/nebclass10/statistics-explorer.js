import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Statistics explorer: a small data set you can edit, with live mean, median,
// mode, range and a histogram. Built for the grade-10 statistics chapter.

const ACCENT = '#F59E0B';
const BLUE = '#38bdf8';
const GREEN = '#34d399';

const PRESETS = {
  'marks': { name: 'Marks of 12 students', data: [45, 62, 71, 58, 62, 80, 39, 62, 74, 55, 68, 50] },
  'rain': { name: 'Rainfall (mm), 12 months', data: [12, 18, 34, 61, 148, 284, 342, 296, 187, 62, 9, 6] },
  'heights': { name: 'Heights (cm) of 15 students', data: [148, 152, 155, 151, 160, 149, 154, 158, 152, 150, 156, 153, 157, 151, 154] },
  'family': { name: 'Family size in 20 homes', data: [4, 5, 6, 4, 4, 7, 3, 5, 4, 6, 8, 4, 5, 4, 6, 4, 5, 3, 4, 5] },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Mean, median and mode answer three different questions about the same data', ACCENT);

  let key = 'marks';
  let data = [...PRESETS[key].data];
  let bins = 6;

  const panel = createPanel(stage, { title: 'Data set' });
  panel.select({
    label: 'Preset',
    options: Object.entries(PRESETS).map(([k, v]) => ({ value: k, label: v.name })),
    value: key,
    onChange: (k) => { key = k; data = [...PRESETS[k].data]; },
  });
  panel.slider({
    label: 'Class width (bins)',
    min: 3, max: 10, step: 1, value: bins,
    onChange: (v) => { bins = v; },
  });
  panel.buttonRow([
    { label: 'Add a value', icon: 'add', onClick: () => { const m = Math.round(mean()); data.push(m + Math.round((Math.random() - 0.5) * 10)); } },
    { label: 'Undo last', icon: 'undo', variant: 'ghost', onClick: () => { if (data.length > 2) data.pop(); } },
  ]);
  const readMean = panel.readout({ label: 'Mean', value: '—' });
  const readMedian = panel.readout({ label: 'Median', value: '—' });
  const readMode = panel.readout({ label: 'Mode', value: '—' });
  const readRange = panel.readout({ label: 'Range', value: '—' });
  const readN = panel.readout({ label: 'Number of values (n)', value: '—' });
  panel.info('Mean = Σx/n. The median is the middle value after sorting. The mode is the value that appears most often — a set can have none or several.');

  function mean() { return data.reduce((s, v) => s + v, 0) / data.length; }
  function sorted() { return [...data].sort((p, q) => p - q); }
  function median() {
    const s = sorted();
    const n = s.length;
    return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  }
  function modes() {
    const count = new Map();
    data.forEach((v) => count.set(v, (count.get(v) || 0) + 1));
    let best = 0;
    count.forEach((v) => { if (v > best) best = v; });
    if (best <= 1) return [];
    return [...count.entries()].filter(([, v]) => v === best).map(([k]) => k).sort((p, q) => p - q);
  }

  function draw(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);

    const chartX = w * 0.04;
    const chartY = h * 0.1;
    const chartW = w * 0.56;
    const chartH = h * 0.56;

    const s = sorted();
    const lo = s[0];
    const hi = s[s.length - 1];
    const span = Math.max(1e-6, hi - lo);
    const bw = span / bins;
    const counts = new Array(bins).fill(0);
    data.forEach((v) => {
      let idx = Math.floor((v - lo) / bw);
      if (idx >= bins) idx = bins - 1;
      if (idx < 0) idx = 0;
      counts[idx] += 1;
    });
    const maxC = Math.max(...counts, 1);

    ctx.fillStyle = 'rgba(8,16,30,0.7)';
    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(chartX, chartY, chartW, chartH, 8); else ctx.rect(chartX, chartY, chartW, chartH);
    ctx.fill(); ctx.stroke();

    const gx = chartX + 34;
    const gy = chartY + 22;
    const gw = chartW - 48;
    const gh = chartH - 56;
    ctx.strokeStyle = 'rgba(199,212,234,0.45)';
    ctx.beginPath(); ctx.moveTo(gx, gy); ctx.lineTo(gx, gy + gh); ctx.lineTo(gx + gw, gy + gh); ctx.stroke();

    const colW = gw / bins;
    counts.forEach((c, i) => {
      const bh = (c / maxC) * gh;
      const bx = gx + i * colW + 3;
      const by = gy + gh - bh;
      const grad = ctx.createLinearGradient(0, by, 0, gy + gh);
      grad.addColorStop(0, ACCENT);
      grad.addColorStop(1, 'rgba(245,158,11,0.35)');
      ctx.fillStyle = grad;
      ctx.fillRect(bx, by, colW - 6, bh);
      ctx.fillStyle = 'rgba(232,238,251,0.9)';
      ctx.font = '700 10px Poppins, sans-serif';
      ctx.textAlign = 'center';
      if (c > 0) ctx.fillText(String(c), bx + (colW - 6) / 2, by - 4);
      ctx.fillStyle = 'rgba(199,212,234,0.7)';
      ctx.font = '600 8.5px Poppins, sans-serif';
      ctx.fillText((lo + i * bw).toFixed(bw < 1 ? 1 : 0), bx + (colW - 6) / 2, gy + gh + 12);
    });
    ctx.fillStyle = 'rgba(199,212,234,0.8)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('frequency', chartX + 8, chartY + 14);
    ctx.textAlign = 'right';
    ctx.fillText('value', chartX + chartW - 10, gy + gh + 26);

    // mean and median markers
    const mx = gx + ((mean() - lo) / span) * gw;
    ctx.strokeStyle = GREEN;
    ctx.lineWidth = 1.8;
    ctx.setLineDash([5, 4]);
    ctx.beginPath(); ctx.moveTo(mx, gy); ctx.lineTo(mx, gy + gh); ctx.stroke();
    const medx = gx + ((median() - lo) / span) * gw;
    ctx.strokeStyle = BLUE;
    ctx.beginPath(); ctx.moveTo(medx, gy); ctx.lineTo(medx, gy + gh); ctx.stroke();
    ctx.setLineDash([]);
    ctx.font = '700 9.5px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillStyle = GREEN;
    ctx.fillText('mean', mx + 4, gy + 12);
    ctx.fillStyle = BLUE;
    ctx.fillText('median', medx + 4, gy + 24);

    // ordered list
    const listX = w * 0.64;
    const listY = h * 0.1;
    const listW = w * 0.32;
    const listH = h * 0.56;
    ctx.fillStyle = 'rgba(8,16,30,0.7)';
    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(listX, listY, listW, listH, 8); else ctx.rect(listX, listY, listW, listH);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = ACCENT;
    ctx.font = '700 10.5px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('values in order', listX + 12, listY + 18);
    ctx.font = '600 10px Poppins, sans-serif';
    const perRow = Math.max(4, Math.floor(listW / 34));
    s.forEach((v, i) => {
      const cx = listX + 12 + (i % perRow) * 32;
      const cy = listY + 40 + Math.floor(i / perRow) * 18;
      const isMedian = (data.length % 2 === 1 && v === median()) || (data.length % 2 === 0 && false);
      ctx.fillStyle = isMedian ? BLUE : 'rgba(232,238,251,0.88)';
      ctx.fillText(String(v), cx, cy);
    });
    const md = modes();
    ctx.fillStyle = 'rgba(199,212,234,0.8)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText(md.length ? `mode: ${md.join(', ')}` : 'mode: none (no value repeats)', listX + 12, listY + listH - 14);

    readMean.set(mean().toFixed(2));
    readMedian.set(String(Number.isInteger(median()) ? median() : median().toFixed(2)));
    readMode.set(md.length ? md.join(', ') : 'none');
    readRange.set(`${lo} to ${hi} (${hi - lo})`);
    readN.set(String(data.length));
    void badge;
  }

  // the canvas helper calls (ctx, dt, width, height); draw wants (ctx, width, height)
  sim.setUpdate((ctx, dt, w, h) => draw(ctx, w, h));
  sim.onResize(() => sim.renderOnce());
  sim.start();

  return { dispose() { sim.dispose(); hud.dispose(); panel.dispose(); } };
}
