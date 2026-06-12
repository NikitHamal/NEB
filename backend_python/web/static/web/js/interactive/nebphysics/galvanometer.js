import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, drawTable, drawNeedleMeter, panelBg, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Close the key and vary R', '#9ec1ff');

  const E = 2.0;
  const G = 100;
  let kTrue = 0;
  let boxR = 6000;
  let keyClosed = false;
  let revealed = false;
  const records = [];

  function newGalvo() {
    kTrue = (1.8 + Math.random() * 0.8) * 1e-5;
    records.length = 0;
    revealed = false;
  }

  function theta() {
    if (!keyClosed) return 0;
    const I = E / (boxR + G);
    return Math.min(30, I / kTrue);
  }

  const panel = createPanel(stage, { title: 'Figure of Merit Lab' });
  panel.toggle({ label: 'Plug key (circuit on)', value: false, onChange: (v) => { keyClosed = v; } });
  panel.slider({
    label: 'Resistance box R',
    min: 3000, max: 12000, step: 500, value: boxR,
    format: (v) => `${v} Ω`,
    onChange: (v) => { boxR = v; },
  });
  panel.button({
    label: 'Record R and θ',
    icon: 'edit_note',
    onClick: () => {
      if (!keyClosed || records.length >= 6) return;
      const th = theta();
      if (th < 3 || th > 29.5) return;
      if (records.some((r) => r.R === boxR)) return;
      const k = E / ((boxR + G) * th);
      records.push({ R: boxR, th, k });
      records.sort((a, b) => a.R - b.R);
    },
  });
  panel.button({ label: 'Clear table', icon: 'delete', variant: 'ghost', onClick: () => { records.length = 0; } });
  panel.button({ label: 'New galvanometer', icon: 'refresh', onClick: newGalvo });
  panel.divider();
  const thOut = panel.readout({ label: 'Deflection θ', value: '—' });
  const kOut = panel.readout({ label: 'Mean k = E/(R+G)θ', value: '—' });
  const igOut = panel.readout({ label: 'Ig = k × 30 div', value: '—' });
  panel.button({ label: 'Reveal true k', icon: 'visibility', onClick: () => { revealed = true; } });
  panel.info(`Galvanometer resistance G = ${G} Ω, cell E = ${E.toFixed(1)} V. Choose R so the deflection lies between 5 and 29 divisions, record several pairs and average k.`);

  newGalvo();

  sim.setUpdate((ctx, dt, w, h) => {
    const th = theta();
    ctx.clearRect(0, 0, w, h);

    drawNeedleMeter(ctx, {
      cx: w * 0.5, cy: h * 0.24, r: Math.min(w * 0.22, 86),
      value: th, min: -30, max: 30, label: `θ = ${fmt(th, 1)} div`, divisions: 12,
    });

    panelBg(ctx, 12, h * 0.42, w - 24, 52);
    labelText(ctx, `cell ${E.toFixed(1)} V  →  key ${keyClosed ? '●' : '○'}  →  R box: ${boxR} Ω  →  G (${G} Ω)`, w * 0.5, h * 0.42 + 22, { size: 10, weight: 600, align: 'center' });
    labelText(ctx, `I = E/(R+G) = ${keyClosed ? fmt((E / (boxR + G)) * 1e3, 3) : '0.000'} mA`, w * 0.5, h * 0.42 + 40, { size: 10, weight: 700, align: 'center', color: '#ffd584' });

    const rows = records.map((r) => [r.R, fmt(r.th, 1), `${(r.k * 1e5).toFixed(2)}×10⁻⁵`]);
    drawTable(ctx, {
      x: 12, y: h * 0.56, w: Math.min(w - 24, 300),
      title: 'Observations', cols: ['R (Ω)', 'θ (div)', 'k (A/div)'], rows,
    });

    thOut.set(keyClosed ? `${fmt(th, 1)} div` : 'key open');
    if (records.length) {
      const mean = records.reduce((s, r) => s + r.k, 0) / records.length;
      kOut.set(revealed
        ? `${(mean * 1e5).toFixed(2)}×10⁻⁵ (true ${(kTrue * 1e5).toFixed(2)}×10⁻⁵)`
        : `${(mean * 1e5).toFixed(2)}×10⁻⁵ A/div`);
      igOut.set(`${(mean * 30 * 1e3).toFixed(2)} mA`);
    } else {
      kOut.set('—');
      igOut.set('—');
    }
    statusBadge.set(
      !keyClosed ? 'Close the key and vary R'
        : th > 29.5 ? 'Needle at full scale — increase R!'
          : th < 3 ? 'Deflection too small — decrease R'
            : 'Good deflection — record it',
    );
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
