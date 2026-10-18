import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Concave mirror bench: move the object, read u, v, f and the magnification.
// The mirror obeys 1/f = 1/v + 1/u with the real-is-positive convention used in
// the Nepali grade-10 textbook.

const ACCENT = '#F59E0B';
const BLUE = '#38bdf8';
const GREEN = '#34d399';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Distant object → rays arrive parallel → image at the focus', ACCENT);

  let f = 10;          // cm
  let u = 30;          // cm, object distance (real, positive)
  let rayMode = 'principal'; // 'principal' | 'parallel'
  let showFormula = true;

  const panel = createPanel(stage, { title: 'Mirror bench' });
  const fSlider = panel.slider({
    label: 'Focal length f',
    min: 5, max: 20, step: 0.5, value: f, unit: ' cm',
    onChange: (v) => { f = v; },
  });
  panel.slider({
    label: 'Object distance u',
    min: 2, max: 60, step: 0.5, value: u, unit: ' cm',
    onChange: (v) => { u = v; },
  });
  panel.buttonRow([
    { label: 'Distant object', icon: 'landscape', onClick: () => { u = 200; setUSlider(200); rayMode = 'parallel'; badge.set('Parallel rays from a distant object focus at F — that is how f is measured in the lab.'); } },
    { label: 'Object at C', icon: 'circle', onClick: () => { u = 2 * f; setUSlider(2 * f); badge.set('Object at the centre of curvature: the image is real, inverted and the same size.'); } },
  ]);
  const raySel = panel.select({
    label: 'Ray diagram',
    options: [
      { value: 'principal', label: 'Principal rays' },
      { value: 'parallel', label: 'Parallel-ray bundle' },
    ],
    value: 'principal',
    onChange: (v) => { rayMode = v; },
  });
  const readU = panel.readout({ label: 'u', value: '—' });
  const readV = panel.readout({ label: 'v', value: '—' });
  const readM = panel.readout({ label: 'Magnification m = −v/u', value: '—' });
  const readNature = panel.readout({ label: 'Image', value: '—' });
  panel.info('Formula: 1/f = 1/v + 1/u, so v = uf ⁄ (u − f). Distances are measured from the pole of the mirror.');

  let uSlider = null;
  function setUSlider(v) {
    const inputs = panel.el.querySelectorAll('input[type=range]');
    if (inputs[1]) {
      inputs[1].value = v;
      const val = inputs[1].closest('.ix-ctrl-slider').querySelector('.ix-ctrl-value');
      if (val) val.textContent = `${v} cm`;
    }
  }
  uSlider = { set: setUSlider };

  function solve() {
    if (Math.abs(u - f) < 1e-6) return { v: Infinity, m: Infinity, real: null };
    const v = (u * f) / (u - f);
    const m = -v / u;
    return { v, m, real: v > 0 };
  }

  function draw(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);
    const cy = h * 0.56;
    const scale = Math.min((w * 0.9) / 90, (h * 0.5) / 46); // px per cm
    const poleX = w * 0.84;                                  // mirror pole
    const X = (cm) => poleX - cm * scale;                    // distances measured left of the pole

    // principal axis
    ctx.strokeStyle = 'rgba(199,212,234,0.35)';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(w * 0.03, cy); ctx.lineTo(w * 0.97, cy); ctx.stroke();

    // mirror: concave arc, centre of curvature 2f to the left of the pole
    const R = 2 * f * scale;
    ctx.strokeStyle = BLUE;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(poleX + R, cy, R, Math.PI * 0.86, Math.PI * 1.14);
    ctx.stroke();
    // hatching behind the mirror
    ctx.strokeStyle = 'rgba(56,189,248,0.45)';
    ctx.lineWidth = 1;
    for (let i = -6; i <= 6; i++) {
      const a = Math.PI + i * 0.045;
      const x1 = poleX + R + Math.cos(a) * R;
      const y1 = cy + Math.sin(a) * R;
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x1 + 5, y1 - 5); ctx.stroke();
    }

    const F = { x: X(f), y: cy };
    const C = { x: X(2 * f), y: cy };
    const P = { x: poleX, y: cy };
    const mark = (p, label, color) => {
      ctx.fillStyle = color;
      ctx.beginPath(); ctx.arc(p.x, p.y, 3.4, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(232,238,251,0.85)';
      ctx.font = '700 10px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(label, p.x, p.y + 16);
    };
    mark(F, 'F', GREEN);
    mark(C, 'C', GREEN);

    const { v, m, real } = solve();
    const objH = 26;
    const objX = X(u);

    // object arrow
    const arrow = (x, height, color, up = true) => {
      ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.4;
      const y0 = cy;
      const y1 = cy - (up ? height : -height);
      ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, y1); ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x, y1);
      ctx.lineTo(x - 4, y1 + (up ? 8 : -8));
      ctx.lineTo(x + 4, y1 + (up ? 8 : -8));
      ctx.closePath(); ctx.fill();
    };
    arrow(Math.max(objX, w * 0.02), objH, ACCENT, true);
    ctx.fillStyle = 'rgba(232,238,251,0.8)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('object', Math.max(objX, w * 0.05), cy + 30);

    // image
    if (Number.isFinite(v) && Math.abs(v) < 400) {
      const imgX = X(v);
      const imgH = objH * Math.abs(m);
      if (imgH < h * 1.6) {
        const inside = imgX > w * 0.02 && imgX < w * 0.99;
        arrow(inside ? imgX : Math.max(Math.min(imgX, w * 0.98), w * 0.02), Math.min(imgH, h * 0.75), real ? GREEN : '#fb7185', real);
        ctx.fillText(real ? 'real, inverted image' : 'virtual, erect image', Math.max(Math.min(imgX, w * 0.8), w * 0.12), real ? cy + 30 + Math.min(imgH, h * 0.75) : cy - 30);
      }
    }

    // rays
    const drawRay = (x1, y1, x2, y2, color) => {
      ctx.strokeStyle = color; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    };
    const topY = cy - objH;
    if (rayMode === 'principal') {
      // ray 1: parallel to the axis, reflects through F
      drawRay(objX, topY, poleX, topY, 'rgba(251,191,36,0.9)');
      if (Number.isFinite(v)) {
        const imgX = X(v);
        const imgH = objH * Math.abs(m);
        drawRay(poleX, topY, imgX, real ? cy - imgH : cy + imgH, 'rgba(251,191,36,0.9)');
      } else {
        drawRay(poleX, topY, F.x, F.y, 'rgba(251,191,36,0.9)');
      }
      // ray 2: through C, reflects back on itself
      drawRay(objX, topY, C.x, cy + (topY - cy) * 0.0, 'rgba(52,211,153,0.85)');
      // ray 3: to the pole, reflects at equal angle
      drawRay(objX, topY, poleX, cy, 'rgba(96,165,250,0.9)');
      drawRay(poleX, cy, poleX - 120, cy + (cy - topY) * 0.8, 'rgba(96,165,250,0.9)');
    } else {
      // parallel bundle
      for (let i = -2; i <= 2; i++) {
        const y = cy + i * 9;
        drawRay(w * 0.03, y, poleX, y, 'rgba(251,191,36,0.55)');
        if (Number.isFinite(v)) drawRay(poleX, y, X(v), cy, 'rgba(251,191,36,0.55)');
      }
    }

    // scale ruler
    ctx.strokeStyle = 'rgba(199,212,234,0.6)';
    ctx.lineWidth = 1;
    const rulerY = h - 26;
    ctx.beginPath(); ctx.moveTo(X(0), rulerY); ctx.lineTo(X(80), rulerY); ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.75)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let i = 0; i <= 80; i += 10) {
      ctx.beginPath(); ctx.moveTo(X(i), rulerY); ctx.lineTo(X(i), rulerY - 5); ctx.stroke();
      ctx.fillText(String(i), X(i), rulerY - 9);
    }
    ctx.fillText('cm from the pole', X(40), rulerY + 14);

    // formula panel
    if (showFormula) {
      ctx.fillStyle = 'rgba(8,16,30,0.78)';
      ctx.strokeStyle = 'rgba(158,193,255,0.25)';
      ctx.lineWidth = 1;
      const bw = 214; const bh = 62;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(14, 14, bw, bh, 8); else ctx.rect(14, 14, bw, bh);
      ctx.fill(); ctx.stroke();
      ctx.textAlign = 'left';
      ctx.fillStyle = ACCENT;
      ctx.font = '700 11px Poppins, sans-serif';
      ctx.fillText('1/f = 1/v + 1/u', 26, 34);
      ctx.fillStyle = 'rgba(232,238,251,0.9)';
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.fillText(`f = ${f.toFixed(1)} cm   u = ${u >= 200 ? 'very large' : u.toFixed(1) + ' cm'}`, 26, 52);
      const vTxt = Number.isFinite(v) ? `${v.toFixed(2)} cm` : 'at infinity';
      ctx.fillText(`v = ${vTxt}`, 26, 68);
    }

    // readouts
    readU.set(u >= 200 ? 'very large (distant object)' : `${u.toFixed(1)} cm`);
    readV.set(Number.isFinite(v) ? `${v.toFixed(2)} cm` : 'at infinity');
    readM.set(Number.isFinite(m) ? `${m.toFixed(2)}` : '—');
    readNature.set(Number.isFinite(v)
      ? (real ? 'Real, inverted, ' + (Math.abs(Math.abs(m) - 1) < 0.05 ? 'same size' : Math.abs(m) > 1 ? 'magnified' : 'diminished')
        : 'Virtual, erect, magnified')
      : 'At the focal plane');
  }

  // the canvas helper calls (ctx, dt, width, height); draw wants (ctx, width, height)
  sim.setUpdate((ctx, dt, w, h) => draw(ctx, w, h));
  sim.onResize(() => sim.renderOnce());
  sim.start();

  return {
    dispose() {
      sim.dispose();
      hud.dispose();
      panel.dispose();
      void pointerPos; void raySel; void uSlider; void fSlider;
    },
  };
}
