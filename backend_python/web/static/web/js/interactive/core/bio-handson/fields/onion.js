// An acetocarmine-stained squash of an onion (Allium cepa, 2n = 16) root tip, in micrometres.
// The tip is laid out as it grows: a loose root cap, the meristem a few hundred micrometres
// behind it (small, near-square cells, 16-18 µm, with big nuclei, where cells divide), then the
// zone of elongation (cells stretching to 70 µm, vacuolate, not dividing). Chromosomes stain
// deep magenta-red; cytoplasm faint pink. Mitotic figures follow the cell file axis: prophase
// threads in an intact nucleus, a metaphase plate of 16 chromosomes across the equator,
// anaphase V-shapes moving to the poles, telophase masses with the cell plate between.
// How well the slide was made shows: an unsquashed tip stays in overlapping layers, an
// over-squashed one breaks into fragments, trapped air shows as black-rimmed bubbles.
import { rng } from '../kit.js';

const W = 2400; const H = 1800;
const TIP_X = 520; const AXIS_Y = 900;
const PHASES = ['interphase', 'prophase', 'metaphase', 'anaphase', 'telophase'];
export const PHASE_INFO = {
  interphase: 'Interphase: an intact, evenly stained nucleus with one or two pale nucleoli; chromosomes not visible as threads.',
  prophase: 'Prophase: chromatin condenses into visible coiled threads inside a still intact nucleus; the nucleolus fades.',
  metaphase: 'Metaphase: the nuclear envelope has gone and the 16 chromosomes line up across the middle of the cell on the equatorial plate.',
  anaphase: 'Anaphase: sister chromatids separate and move to opposite poles, arms trailing behind like a V.',
  telophase: 'Telophase: two dense groups of chromosomes at the poles, nuclei re-forming and a cell plate appearing between them.',
};

export function createOnionField(mount = {}) {
  const R = rng(20240611);
  const cells = []; const grid = new Map(); const B = 60;
  const squash = mount.squash || 'good'; // good | under | over
  const animal = !!mount.animal; const NCH = animal ? 23 : 16;
  const spread = squash === 'under' ? 0.55 : squash === 'over' ? 1.45 : 1;
  function halfWidth(u) { return 430 * spread * Math.sqrt(Math.min(1, Math.max(0, u + 40) / 360)); }
  function pickPhase(u) {
    if (u < 140 || u > 760) return 'interphase';
    const k = u < 520 ? 1 : 1 - (u - 520) / 240;
    const r = R();
    if (r < 0.085 * k) return 'prophase';
    if (r < 0.125 * k) return 'metaphase';
    if (r < 0.155 * k) return 'anaphase';
    if (r < 0.2 * k) return 'telophase';
    return 'interphase';
  }
  // cells in files parallel to the axis; u is distance from the tip
  let u = 0;
  while (u < 1700) {
    const len = u < 140 ? 26 : u < 650 ? 15 + R() * 4 : 18 + Math.min(55, (u - 650) * 0.075) + R() * 6;
    const hw = halfWidth(u + len / 2);
    const wid = u < 140 ? 24 : 17;
    let v = -hw + R() * wid * 0.5;
    while (v < hw - 6) {
      const ww = wid * (0.85 + R() * 0.3);
      const edge = hw - Math.abs(v + ww / 2);
      if ((edge < 40 && R() < 0.35 * (1 - edge / 40)) || u > 1380 + 180 * Math.sin(v * 0.013) + R() * 140) { v += ww; continue; }
      const jx = () => (R() - 0.5) * 3; const jy = () => (R() - 0.5) * 3;
      const x0 = TIP_X + u * spread; const x1 = TIP_X + (u + len) * spread;
      const y0 = AXIS_Y + v; const y1 = AXIS_Y + v + ww;
      // squash spreads cells into islands with cracks between them
      const crack = Math.sin(u * 0.012 + v * 0.02) + Math.sin(v * 0.031 - u * 0.007);
      const off = squash === 'over' ? 30 : 8;
      const dx = Math.sin(v * 0.015) * off * 0.6 + (crack > 1.2 ? off : 0); const dy = Math.cos(u * 0.011) * off * 0.5;
      const c = {
        p: [x0 + jx() + dx, y0 + jy() + dy, x1 + jx() + dx, y0 + jy() + dy, x1 + jx() + dx, y1 + jy() + dy, x0 + jx() + dx, y1 + jy() + dy],
        cx: (x0 + x1) / 2 + dx, cy: (y0 + y1) / 2 + dy, len: (x1 - x0), wid: ww,
        zone: u < 140 ? 'cap' : u < 650 ? 'meristem' : 'elongation',
        phase: pickPhase(u), seed: R() * 1000, k: R(), broken: squash === 'over' && R() < 0.3,
      };
      cells.push(c);
      const key = `${Math.floor(c.cx / B)},${Math.floor(c.cy / B)}`;
      if (!grid.has(key)) grid.set(key, []);
      grid.get(key).push(c);
      v += ww;
    }
    u += len;
  }
  const bubbles = [];
  for (let i = 0; i < (mount.bubbles || 0); i++) bubbles.push({ x: TIP_X + 150 + R() * 900, y: AXIS_Y + (R() - 0.5) * 700, r: 40 + R() * 90 });
  const dust = []; for (let i = 0; i < 40; i++) dust.push({ x: R() * W, y: R() * H, r: 2 + R() * 6, a: 0.1 + R() * 0.25 });
  const stain = mount.stain ?? 1;

  let low = null; const LOW = 0.45;
  function drawCell(g, c, s, detail) {
    const p = c.p;
    if (animal) { g.beginPath(); if (c.phase === 'telophase') { g.ellipse(c.cx - c.len * 0.24, c.cy, c.len * 0.3, c.wid * 0.46, 0, 0, Math.PI * 2); g.moveTo(c.cx + c.len * 0.54, c.cy); g.ellipse(c.cx + c.len * 0.24, c.cy, c.len * 0.3, c.wid * 0.46, 0, 0, Math.PI * 2); } else g.ellipse(c.cx, c.cy, c.len * 0.47, c.wid * 0.46, 0, 0, Math.PI * 2); }
    else { g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(p[2], p[3]); g.lineTo(p[4], p[5]); g.lineTo(p[6], p[7]); g.closePath(); }
    const pale = c.zone === 'elongation' ? 0.55 : c.zone === 'cap' ? 0.5 : 1;
    g.fillStyle = `rgba(236,182,196,${0.22 * pale * stain + 0.06})`; g.fill();
    if (!c.broken) { g.strokeStyle = animal ? 'rgba(122,62,86,0.3)' : 'rgba(122,62,86,0.55)'; g.lineWidth = Math.max(0.7, 1.1 / s); g.stroke(); }
    const r = Math.min(c.len, c.wid) * (c.zone === 'meristem' ? 0.33 : c.zone === 'cap' ? 0.18 : 0.24);
    const ax = c.cx; const ay = c.cy;
    const R2 = rng(c.seed | 0);
    const ink = (a) => `rgba(${120 - 30 * stain | 0},${12},${62},${Math.min(1, a * (0.35 + 0.65 * stain))})`;
    if (c.phase === 'interphase' || !detail) {
      if (c.phase !== 'interphase' && !detail) { g.fillStyle = ink(0.85); g.beginPath(); g.ellipse(ax, ay, r * 0.9, r * 1.05, 0, 0, Math.PI * 2); g.fill(); return; }
      g.fillStyle = ink(0.62 * pale + 0.15); g.beginPath(); g.ellipse(ax + (c.k - 0.5) * 2, ay, r * 1.05, r, 0, 0, Math.PI * 2); g.fill();
      if (detail) {
        g.fillStyle = ink(0.5); for (let i = 0; i < 9; i++) { const a = R2() * 6.28; const d = R2() * r * 0.8; g.fillRect(ax + Math.cos(a) * d, ay + Math.sin(a) * d, 0.9, 0.9); }
        g.fillStyle = 'rgba(250,215,225,0.75)'; g.beginPath(); g.arc(ax + r * 0.25, ay - r * 0.2, r * 0.22, 0, Math.PI * 2); g.fill();
        if (c.k > 0.6) { g.beginPath(); g.arc(ax - r * 0.3, ay + r * 0.25, r * 0.14, 0, Math.PI * 2); g.fill(); }
      }
      return;
    }
    g.lineCap = 'round';
    if (c.phase === 'prophase') {
      g.fillStyle = ink(0.22); g.beginPath(); g.ellipse(ax, ay, r * 1.12, r * 1.08, 0, 0, Math.PI * 2); g.fill();
      g.strokeStyle = ink(0.95); g.lineWidth = 0.95 + c.k * 0.5;
      for (let i = 0; i < 9; i++) {
        let x = ax + (R2() - 0.5) * r * 1.3; let y = ay + (R2() - 0.5) * r * 1.3;
        g.beginPath(); g.moveTo(x, y);
        for (let k = 0; k < 4; k++) { const nx = x + (R2() - 0.5) * r * 0.9; const ny = y + (R2() - 0.5) * r * 0.9; g.quadraticCurveTo((x + nx) / 2 + (R2() - 0.5) * 2, (y + ny) / 2 + (R2() - 0.5) * 2, nx, ny); x = nx; y = ny; }
        g.stroke();
      }
    } else if (c.phase === 'metaphase') {
      g.strokeStyle = ink(1); g.lineWidth = 1.35;
      const half = c.wid * 0.36;
      for (let i = 0; i < NCH; i++) {
        const y = ay - half + (i / (NCH - 1)) * half * 2 + (R2() - 0.5) * 1.2; const x = ax + (R2() - 0.5) * 2.2; const L = 2.2 + R2() * 2.5;
        g.beginPath(); g.moveTo(x - L / 2, y + (R2() - 0.5)); g.lineTo(x + L / 2, y + (R2() - 0.5)); g.stroke();
      }
    } else if (c.phase === 'anaphase') {
      g.strokeStyle = ink(1); g.lineWidth = 1.1;
      const d = c.len * (0.14 + c.k * 0.14); const half = c.wid * 0.33;
      for (const side of [-1, 1]) {
        for (let i = 0; i < NCH; i++) {
          const y = ay - half + (i / (NCH - 1)) * half * 2 + (R2() - 0.5); const x = ax + side * d; const arm = 2 + R2() * 2.5;
          g.beginPath(); g.moveTo(x - side * arm, y - 1.1); g.lineTo(x, y); g.lineTo(x - side * arm, y + 1.1); g.stroke();
        }
      }
    } else if (c.phase === 'telophase') {
      const d = c.len * 0.3;
      for (const side of [-1, 1]) {
        g.fillStyle = ink(0.95); g.beginPath(); g.ellipse(ax + side * d, ay, r * 0.55, c.wid * 0.3, 0, 0, Math.PI * 2); g.fill();
        g.fillStyle = ink(0.6); for (let i = 0; i < 8; i++) g.fillRect(ax + side * d + (R2() - 0.5) * r, ay + (R2() - 0.5) * c.wid * 0.5, 1.1, 1.1);
      }
      if (!animal) { g.strokeStyle = `rgba(150,80,110,${0.25 + c.k * 0.4})`; g.lineWidth = 0.8; g.beginPath(); g.moveTo(ax, ay - c.wid * 0.45); g.lineTo(ax, ay + c.wid * 0.45); g.stroke(); }
    }
  }
  function drawAll(g, s, x0, y0, x1, y1, detail) {
    const bx0 = Math.floor(x0 / B) - 1; const bx1 = Math.floor(x1 / B) + 1; const by0 = Math.floor(y0 / B) - 1; const by1 = Math.floor(y1 / B) + 1;
    for (let by = by0; by <= by1; by++) for (let bx = bx0; bx <= bx1; bx++) { const list = grid.get(`${bx},${by}`); if (list) for (let i = 0; i < list.length; i++) drawCell(g, list[i], s, detail); }
    if (squash === 'under') {
      g.save(); g.globalAlpha = 0.45; g.translate(9, 6);
      for (let by = by0; by <= by1; by++) for (let bx = bx0; bx <= bx1; bx++) { const list = grid.get(`${bx},${by}`); if (list) for (let i = 0; i < list.length; i += 2) drawCell(g, list[i], s, false); }
      g.restore();
    }
  }
  function lowRes() {
    if (low) return low;
    low = document.createElement('canvas'); low.width = Math.round(W * LOW); low.height = Math.round(H * LOW);
    const g = low.getContext('2d'); g.setTransform(LOW, 0, 0, LOW, 0, 0);
    drawAll(g, LOW, 0, 0, W, H, false);
    return low;
  }
  return {
    width: W, height: H, start: { x: TIP_X + 1150, y: AXIS_Y - 260 }, background: '#f4efe4', mount,
    cells,
    draw(g, v) {
      const x0 = v.cx - v.halfW; const x1 = v.cx + v.halfW; const y0 = v.cy - v.halfH; const y1 = v.cy + v.halfH;
      if (v.scale < 0.9) g.drawImage(lowRes(), 0, 0, W, H);
      else drawAll(g, v.scale, x0, y0, x1, y1, v.scale > 1.6);
      for (const b of bubbles) {
        g.lineWidth = 6; g.strokeStyle = 'rgba(20,20,20,0.85)'; g.fillStyle = 'rgba(255,255,255,0.35)';
        g.beginPath(); g.arc(b.x, b.y, b.r, 0, Math.PI * 2); g.fill(); g.stroke();
        g.lineWidth = 2; g.strokeStyle = 'rgba(255,255,255,0.8)'; g.beginPath(); g.arc(b.x - b.r * 0.2, b.y - b.r * 0.2, b.r * 0.6, 3.6, 4.6); g.stroke();
      }
      for (const d of dust) { if (d.x < x0 - 10 || d.x > x1 + 10 || d.y < y0 - 10 || d.y > y1 + 10) continue; g.fillStyle = `rgba(60,50,40,${d.a})`; g.beginPath(); g.arc(d.x, d.y, d.r, 0, Math.PI * 2); g.fill(); }
    },
    hit(x, y) {
      const list = grid.get(`${Math.floor(x / B)},${Math.floor(y / B)}`) || [];
      let best = null; let bd = Infinity;
      const near = [list];
      for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) if (dx || dy) near.push(grid.get(`${Math.floor(x / B) + dx},${Math.floor(y / B) + dy}`) || []);
      near.forEach((l) => l.forEach((c) => { const d = Math.hypot(c.cx - x, c.cy - y); if (d < bd && d < Math.max(c.len, c.wid) * 0.6) { bd = d; best = c; } }));
      return best;
    },
    /** Tally of phases among meristem cells inside a circular field. */
    tally(cx, cy, radius) {
      const t = { total: 0 }; PHASES.forEach((p) => { t[p] = 0; });
      cells.forEach((c) => { if (c.zone !== 'cap' && Math.hypot(c.cx - cx, c.cy - cy) < radius) { t.total += 1; t[c.phase] += 1; } });
      return t;
    },
    meristem: { x: TIP_X + 330 * spread, y: AXIS_Y },
    dispose() { low = null; },
  };
}
