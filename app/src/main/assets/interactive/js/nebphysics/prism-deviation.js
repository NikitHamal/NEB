import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, drawGraph, panelBg, labelText } from './lab-utils.js';

const A = Math.PI / 3;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Trace rays through the prism', '#9ec1ff');

  let nTrue = 1.5;
  let iDeg = 50;
  let revealed = false;
  const records = [];

  function newPrism() {
    nTrue = Math.round((1.46 + Math.random() * 0.18) * 1000) / 1000;
    records.length = 0;
    revealed = false;
  }

  function trace(iRad) {
    const sinR1 = Math.sin(iRad) / nTrue;
    if (sinR1 > 1) return null;
    const r1 = Math.asin(sinR1);
    const r2 = A - r1;
    const sinE = nTrue * Math.sin(r2);
    if (sinE > 1) return { tir: true, r1, r2 };
    const e = Math.asin(sinE);
    return { tir: false, r1, r2, e, D: iRad + e - A };
  }

  const panel = createPanel(stage, { title: 'Prism Lab' });
  panel.slider({
    label: 'Angle of incidence i',
    min: 30, max: 80, step: 0.5, value: iDeg,
    format: (v) => `${v.toFixed(1)}°`,
    onChange: (v) => { iDeg = v; },
  });
  panel.button({
    label: 'Record (i, D)',
    icon: 'edit_note',
    onClick: () => {
      const t = trace((iDeg * Math.PI) / 180);
      if (!t || t.tir || records.length >= 12) return;
      if (records.some((r) => Math.abs(r.i - iDeg) < 0.6)) return;
      records.push({ i: iDeg, D: (t.D * 180) / Math.PI });
      records.sort((a, b) => a.i - b.i);
    },
  });
  panel.button({ label: 'Clear data', icon: 'delete', variant: 'ghost', onClick: () => { records.length = 0; } });
  panel.button({ label: 'New glass prism', icon: 'refresh', onClick: newPrism });
  panel.divider();
  const dOut = panel.readout({ label: 'Deviation D', value: '—' });
  const dmOut = panel.readout({ label: 'Minimum Dₘ found', value: '—' });
  const nOut = panel.readout({ label: 'n = sin((A+Dₘ)/2)/sin(A/2)', value: '—' });
  panel.button({ label: 'Reveal true n', icon: 'visibility', onClick: () => { revealed = true; } });
  panel.info('A = 60°. Sweep i from 30° to 80°, recording (i, D) pairs. D first falls then rises — the bottom of the curve is the angle of minimum deviation Dₘ.');

  newPrism();

  sim.setUpdate((ctx, dt, w, h) => {
    const iRad = (iDeg * Math.PI) / 180;
    const t = trace(iRad);
    ctx.clearRect(0, 0, w, h);

    const cx = w * 0.5;
    const cy = h * 0.32;
    const s = Math.min(w * 0.24, h * 0.2);
    const top = { x: cx, y: cy - s };
    const bl = { x: cx - s * Math.sin(A / 2) * 1.155, y: cy + s * 0.58 };
    const br = { x: cx + s * Math.sin(A / 2) * 1.155, y: cy + s * 0.58 };
    ctx.fillStyle = 'rgba(158,193,255,0.14)';
    ctx.strokeStyle = '#9ec1ff';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(top.x, top.y);
    ctx.lineTo(bl.x, bl.y);
    ctx.lineTo(br.x, br.y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    labelText(ctx, 'A = 60°', top.x, top.y - 8, { size: 10, weight: 700, align: 'center', color: '#9ec1ff' });

    const p1 = { x: (top.x + bl.x) / 2, y: (top.y + bl.y) / 2 };
    const faceL = norm(top.x - bl.x, top.y - bl.y);
    const n1 = { x: -faceL.y, y: faceL.x };
    if (n1.x > 0) { n1.x = -n1.x; n1.y = -n1.y; }
    drawNormal(ctx, p1, n1);
    const dIn = rot(neg(n1), -iRad);
    const start = { x: p1.x - dIn.x * s * 1.6, y: p1.y - dIn.y * s * 1.6 };
    ray(ctx, start, p1, '#F59E0B');

    if (t && !t.tir) {
      const dir = refractDir(dIn, n1, 1 / nTrue);
      const p2 = dir ? intersectFace(p1, dir, top, br) : null;
      if (p2) {
        ray(ctx, p1, p2, '#ffd584');
        const faceR = norm(top.x - br.x, top.y - br.y);
        let n2 = { x: -faceR.y, y: faceR.x };
        if (n2.x < 0) { n2.x = -n2.x; n2.y = -n2.y; }
        drawNormal(ctx, p2, n2);
        const dOut2 = refractDir(dir, neg(n2), nTrue);
        if (dOut2) {
          const end = { x: p2.x + dOut2.x * s * 1.7, y: p2.y + dOut2.y * s * 1.7 };
          ray(ctx, p2, end, '#8be9a8');
          ctx.setLineDash([4, 5]);
          ctx.strokeStyle = 'rgba(255,140,140,0.6)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p1.x + dIn.x * s * 1.8, p1.y + dIn.y * s * 1.8);
          ctx.stroke();
          ctx.setLineDash([]);
        }
      }
    } else if (t && t.tir) {
      labelText(ctx, 'Total internal reflection at second face!', cx, cy + s, { size: 11, weight: 700, align: 'center', color: '#ff8c8c' });
    }

    const pts = records.map((r) => ({ x: r.i, y: r.D }));
    drawGraph(ctx, {
      x: 12, y: h * 0.56, w: w - 24, h: h * 0.4,
      pts, xLabel: 'i (°)', yLabel: 'D (°)', xMax: 90, yMax: 70,
    });
    if (records.length >= 2) {
      const minRec = records.reduce((m, r) => (r.D < m.D ? r : m), records[0]);
      const gx = 12 + 14 + ((w - 24 - 24) * minRec.i) / 90;
      labelText(ctx, '▼ Dₘ', gx, h * 0.56 + 14, { size: 9, weight: 700, align: 'center', color: '#8be9a8' });
    }

    panelBg(ctx, 12, 12, Math.min(w * 0.5, 190), 58);
    labelText(ctx, `i = ${fmt(iDeg, 1)}°`, 22, 32, { size: 11, weight: 700, color: '#F59E0B' });
    if (t && !t.tir) {
      labelText(ctx, `r₁ = ${fmt((t.r1 * 180) / Math.PI, 1)}°  r₂ = ${fmt((t.r2 * 180) / Math.PI, 1)}°`, 22, 48, { size: 9.5, weight: 600 });
      labelText(ctx, `e = ${fmt((t.e * 180) / Math.PI, 1)}°  D = ${fmt((t.D * 180) / Math.PI, 1)}°`, 22, 64, { size: 9.5, weight: 600, color: '#8be9a8' });
    } else {
      labelText(ctx, 'no emergent ray (TIR)', 22, 48, { size: 9.5, weight: 600, color: '#ff8c8c' });
    }

    dOut.set(t && !t.tir ? `${fmt((t.D * 180) / Math.PI, 2)}°` : 'TIR');
    if (records.length >= 3) {
      const minRec = records.reduce((m, r) => (r.D < m.D ? r : m), records[0]);
      dmOut.set(`${fmt(minRec.D, 2)}° at i = ${fmt(minRec.i, 1)}°`);
      const dmRad = (minRec.D * Math.PI) / 180;
      const nExp = Math.sin((A + dmRad) / 2) / Math.sin(A / 2);
      nOut.set(revealed ? `${fmt(nExp, 3)} (true ${fmt(nTrue, 3)})` : fmt(nExp, 3));
    } else {
      dmOut.set('record ≥ 3 points');
      nOut.set('—');
    }
    const dmTrueRad = 2 * Math.asin(nTrue * Math.sin(A / 2)) - A;
    statusBadge.set(
      t && !t.tir && Math.abs((t.D - dmTrueRad) * 180 / Math.PI) < 0.5
        ? 'Near minimum deviation — i ≈ e here!'
        : 'Sweep i and record the deviation',
    );
  });

  function norm(x, y) {
    const m = Math.hypot(x, y) || 1;
    return { x: x / m, y: y / m };
  }

  function neg(v) { return { x: -v.x, y: -v.y }; }

  function rot(v, a) {
    return { x: v.x * Math.cos(a) - v.y * Math.sin(a), y: v.x * Math.sin(a) + v.y * Math.cos(a) };
  }

  function refractDir(d, n, eta) {
    const cosi = -(d.x * n.x + d.y * n.y);
    const k = 1 - eta * eta * (1 - cosi * cosi);
    if (k < 0) return null;
    const sq = Math.sqrt(k);
    return norm(eta * d.x + (eta * cosi - sq) * n.x, eta * d.y + (eta * cosi - sq) * n.y);
  }

  function intersectFace(p, d, a, b) {
    const ex = b.x - a.x;
    const ey = b.y - a.y;
    const den = d.x * ey - d.y * ex;
    if (Math.abs(den) < 1e-9) return null;
    const tt = ((a.x - p.x) * ey - (a.y - p.y) * ex) / den;
    if (tt < 1) return null;
    return { x: p.x + d.x * tt, y: p.y + d.y * tt };
  }

  function drawNormal(ctx, p, n) {
    ctx.setLineDash([3, 4]);
    ctx.strokeStyle = 'rgba(199,212,234,0.45)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(p.x - n.x * 34, p.y - n.y * 34);
    ctx.lineTo(p.x + n.x * 34, p.y + n.y * 34);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  function ray(ctx, a, b, color) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
    const ang = Math.atan2(b.y - a.y, b.x - a.x);
    const mx = (a.x + b.x) / 2;
    const my = (a.y + b.y) / 2;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(mx + 7 * Math.cos(ang), my + 7 * Math.sin(ang));
    ctx.lineTo(mx + 7 * Math.cos(ang + 2.5), my + 7 * Math.sin(ang + 2.5));
    ctx.lineTo(mx + 7 * Math.cos(ang - 2.5), my + 7 * Math.sin(ang - 2.5));
    ctx.closePath();
    ctx.fill();
  }

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
