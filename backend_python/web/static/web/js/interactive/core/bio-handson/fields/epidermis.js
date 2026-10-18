// A peel of leaf epidermis in micrometres: one cell thick, cells elongated along the leaf in
// staggered rows, stomata scattered among them. For Rhoeo (Tradescantia spathacea) the lower
// epidermis has purple anthocyanin in the cell sap of most cells, and each stoma has two green,
// chloroplast-bearing guard cells with four colourless subsidiary cells (tetracytic). Each
// cell's protoplast can be drawn turgid (pressed to the wall), incipiently plasmolysed (pulling
// from the corners) or fully plasmolysed (a rounded, deeper purple mass), so plasmolysis and
// deplasmolysis can be watched as they happen.
import { rng } from '../kit.js';

export function createEpidermisField(opts = {}) {
  const W = 2600; const H = 2000;
  const R = rng(opts.seed || 77);
  const rowH = opts.rowH || 46;
  const purple = opts.purple ?? 0.85;
  const stomaRate = opts.stomaRate ?? 0.07;
  const cells = []; const stomata = []; const grid = new Map(); const B = 120;
  const rows = Math.ceil(H / rowH);
  const yb = (row, x) => row * rowH + Math.sin(x * 0.021 + row * 1.7) * 4 + Math.sin(x * 0.007 + row) * 3;
  for (let row = 0; row < rows; row++) {
    let x = -R() * 80;
    while (x < W) {
      const len = (opts.cellLen || 85) * (0.7 + R() * 0.6);
      const x0 = x; const x1 = x + len;
      const j0 = (R() - 0.5) * 14; const j1 = (R() - 0.5) * 14;
      const p = [x0 + j0, yb(row, x0 + j0), x1 + j1, yb(row, x1 + j1), x1 - j1 * 0.6, yb(row + 1, x1 - j1 * 0.6), x0 - j0 * 0.6, yb(row + 1, x0 - j0 * 0.6)];
      const c = { p, cx: (x0 + x1) / 2, cy: (yb(row, (x0 + x1) / 2) + yb(row + 1, (x0 + x1) / 2)) / 2, len, h: rowH, purple: R() < purple, k: 0.55 + R() * 0.45, seed: R() * 1000, stoma: false, mark: null };
      if (R() < stomaRate && row > 0 && x0 > 40 && len > (opts.cellLen || 85) * 0.75) { c.stoma = true; c.purple = false; stomata.push(c); }
      cells.push(c);
      const key = `${Math.floor(c.cx / B)},${Math.floor(c.cy / B)}`; if (!grid.has(key)) grid.set(key, []); grid.get(key).push(c);
      x = x1;
    }
  }
  const state = { p: 0, target: 0, speed: 0.12, bubbles: [] };
  for (let i = 0; i < (opts.bubbles || 0); i++) state.bubbles.push({ x: W * 0.3 + R() * W * 0.4, y: H * 0.3 + R() * H * 0.4, r: 50 + R() * 100 });

  function protoplast(g, c, p) {
    const pts = c.p; const cx = c.cx; const cy = c.cy;
    const e = Math.min(1, p / c.k); // each cell has its own threshold
    if (e <= 0.001) { g.beginPath(); g.moveTo(pts[0], pts[1]); g.lineTo(pts[2], pts[3]); g.lineTo(pts[4], pts[5]); g.lineTo(pts[6], pts[7]); g.closePath(); return 0; }
    const corner = 1 - e * 0.62; const mid = 1 - e * (0.18 + 0.3 * e);
    g.beginPath();
    for (let i = 0; i < 4; i++) {
      const ax = pts[i * 2]; const ay = pts[i * 2 + 1]; const bx = pts[((i + 1) % 4) * 2]; const by = pts[((i + 1) % 4) * 2 + 1];
      const mx = cx + ((ax + bx) / 2 - cx) * mid; const my = cy + ((ay + by) / 2 - cy) * mid;
      const kx = cx + (ax - cx) * corner; const ky = cy + (ay - cy) * corner;
      if (i === 0) { const px = pts[6]; const py = pts[7]; g.moveTo(cx + ((px + ax) / 2 - cx) * mid, cy + ((py + ay) / 2 - cy) * mid); }
      g.quadraticCurveTo(kx, ky, mx, my);
    }
    g.closePath();
    return e;
  }
  function drawCell(g, c, s) {
    const pts = c.p;
    if (c.stoma) {
      g.fillStyle = 'rgba(236,240,226,0.5)';
      g.beginPath(); g.moveTo(pts[0], pts[1]); g.lineTo(pts[2], pts[3]); g.lineTo(pts[4], pts[5]); g.lineTo(pts[6], pts[7]); g.closePath(); g.fill();
      g.strokeStyle = 'rgba(70,80,60,0.6)'; g.lineWidth = 1.6 / Math.max(0.5, s); g.stroke();
      // subsidiary walls and the guard cell pair
      const L = Math.min(c.len * 0.42, 34); const Hh = c.h * 0.36; const open = 1 - state.p * 0.8;
      g.strokeStyle = 'rgba(80,90,70,0.45)'; g.beginPath(); g.ellipse(c.cx, c.cy, L * 1.25, Hh * 1.35, 0, 0, Math.PI * 2); g.stroke();
      for (const side of [-1, 1]) {
        g.fillStyle = 'rgba(120,170,80,0.92)';
        g.beginPath(); g.ellipse(c.cx, c.cy + side * Hh * 0.45, L, Hh * 0.55, 0, 0, Math.PI * 2); g.fill();
        g.strokeStyle = 'rgba(50,90,40,0.8)'; g.lineWidth = 1 / Math.max(0.5, s); g.stroke();
        if (s > 0.9) { g.fillStyle = 'rgba(40,110,40,0.9)'; const r2 = rng(c.seed | 0); for (let i = 0; i < 7; i++) { g.beginPath(); g.arc(c.cx + (r2() - 0.5) * L * 1.5, c.cy + side * Hh * (0.3 + r2() * 0.4), 1.6, 0, Math.PI * 2); g.fill(); } }
      }
      g.fillStyle = 'rgba(40,40,30,0.85)'; g.beginPath(); g.ellipse(c.cx, c.cy, L * 0.62, Math.max(0.6, Hh * 0.12 * open), 0, 0, Math.PI * 2); g.fill();
      return;
    }
    // cell wall (with a faint space when plasmolysed) and the coloured sap
    if (c.purple) {
      const e = protoplast(g, c, state.p);
      const a = 0.42 + e * 0.32;
      g.fillStyle = `rgba(${150 - e * 40 | 0},${48 - e * 18 | 0},${150 - e * 10 | 0},${a})`; g.fill();
      if (e > 0.05) { g.strokeStyle = `rgba(90,20,100,${0.3 + e * 0.3})`; g.lineWidth = 1 / Math.max(0.5, s); g.stroke(); }
      if (s > 0.9) { g.fillStyle = 'rgba(200,170,210,0.55)'; g.beginPath(); g.ellipse(c.cx + c.len * 0.18, c.cy, 5, 4, 0, 0, Math.PI * 2); g.fill(); }
    } else {
      g.fillStyle = 'rgba(232,238,226,0.35)';
      g.beginPath(); g.moveTo(pts[0], pts[1]); g.lineTo(pts[2], pts[3]); g.lineTo(pts[4], pts[5]); g.lineTo(pts[6], pts[7]); g.closePath(); g.fill();
    }
    g.strokeStyle = 'rgba(70,70,60,0.75)'; g.lineWidth = 1.8 / Math.max(0.5, s);
    g.beginPath(); g.moveTo(pts[0], pts[1]); g.lineTo(pts[2], pts[3]); g.lineTo(pts[4], pts[5]); g.lineTo(pts[6], pts[7]); g.closePath(); g.stroke();
  }
  return {
    width: W, height: H, start: { x: W / 2, y: H / 2 }, background: '#eef0e6', mount: { thick: 0 },
    get animated() { return state.p !== state.target; },
    cells, stomata, state,
    draw(g, v) {
      const x0 = v.cx - v.halfW - 120; const x1 = v.cx + v.halfW + 120; const y0 = v.cy - v.halfH - 120; const y1 = v.cy + v.halfH + 120;
      for (let by = Math.floor(y0 / B); by <= Math.floor(y1 / B); by++) for (let bx = Math.floor(x0 / B); bx <= Math.floor(x1 / B); bx++) { const l = grid.get(`${bx},${by}`); if (l) for (let i = 0; i < l.length; i++) drawCell(g, l[i], v.scale); }
      for (const b of state.bubbles) { g.lineWidth = 7; g.strokeStyle = 'rgba(20,20,20,0.85)'; g.fillStyle = 'rgba(255,255,255,0.35)'; g.beginPath(); g.arc(b.x, b.y, b.r, 0, Math.PI * 2); g.fill(); g.stroke(); }
    },
    step(dt) {
      if (state.p === state.target) return false;
      const d = state.target - state.p; const st = state.speed * dt;
      state.p = Math.abs(d) <= st ? state.target : state.p + Math.sign(d) * st;
      return true;
    },
    hit(x, y) {
      let best = null; let bd = Infinity;
      for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) { const l = grid.get(`${Math.floor(x / B) + dx},${Math.floor(y / B) + dy}`) || []; l.forEach((c) => { const d = Math.hypot((c.cx - x) / c.len, (c.cy - y) / c.h); if (d < bd && d < 0.7) { bd = d; best = c; } }); }
      return best;
    },
    countIn(cx, cy, r, pred) { let n = 0; cells.forEach((c) => { if (pred(c) && Math.hypot(c.cx - cx, c.cy - cy) < r) n += 1; }); return n; },
  };
}
