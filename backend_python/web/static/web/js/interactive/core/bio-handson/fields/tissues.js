// Permanent-slide fields, in micrometres. A Leishman-stained human blood smear (pale biconcave
// red cells about 7.5 µm; neutrophils with 2-5 lobed nuclei, lymphocytes with a big round
// nucleus in a thin rim of blue cytoplasm, kidney-nucleus monocytes, eosinophils with red
// granules, basophils dark with blue-black granules, and platelets); squamous epithelium (flat
// polygonal cells, each with a small central nucleus); striated muscle in longitudinal section
// (long fibres with alternating dark A and light I bands and nuclei under the sarcolemma); frog
// embryos from the fertilised egg to the gastrula; and a newsprint letter "e" for the
// microscope's inverted image.
import { rng } from '../kit.js';

function gridOf(items, B) { const g = new Map(); items.forEach((it) => { const k = `${Math.floor(it.x / B)},${Math.floor(it.y / B)}`; if (!g.has(k)) g.set(k, []); g.get(k).push(it); }); return g; }
function near(grid, B, x, y, test) {
  let best = null; let bd = Infinity;
  for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) (grid.get(`${Math.floor(x / B) + dx},${Math.floor(y / B) + dy}`) || []).forEach((it) => { const d = Math.hypot(it.x - x, it.y - y); if (d < it.r * 1.15 && d < bd && (!test || test(it))) { bd = d; best = it; } });
  return best;
}
function visit(grid, B, v, fn) {
  const x0 = Math.floor((v.cx - v.halfW) / B) - 1; const x1 = Math.floor((v.cx + v.halfW) / B) + 1; const y0 = Math.floor((v.cy - v.halfH) / B) - 1; const y1 = Math.floor((v.cy + v.halfH) / B) + 1;
  for (let by = y0; by <= y1; by++) for (let bx = x0; bx <= x1; bx++) { const l = grid.get(`${bx},${by}`); if (l) for (let i = 0; i < l.length; i++) fn(l[i]); }
}

export function bloodField() {
  const R = rng(4242); const W = 1600; const H = 1200; const items = [];
  const kinds = [['neutrophil', 0.6], ['lymphocyte', 0.27], ['monocyte', 0.07], ['eosinophil', 0.04], ['basophil', 0.02]];
  for (let i = 0; i < 5200; i++) items.push({ kind: 'red blood cell', x: R() * W, y: R() * H, r: 3.6 + R() * 0.5, a: R() * 6 });
  for (let i = 0; i < 70; i++) { let r = R(); let k = 'neutrophil'; for (const [n, p] of kinds) { if (r < p) { k = n; break; } r -= p; } items.push({ kind: k, x: 60 + R() * (W - 120), y: 60 + R() * (H - 120), r: k === 'monocyte' ? 8.5 : k === 'lymphocyte' ? 4.6 : 6.2, a: R() * 6, seed: R() * 999 }); }
  for (let i = 0; i < 260; i++) items.push({ kind: 'platelet', x: R() * W, y: R() * H, r: 1.3, a: R() * 6 });
  const B = 40; const grid = gridOf(items, B);
  function cell(g, it) {
    const { x, y, r } = it;
    if (it.kind === 'red blood cell') {
      const gr = g.createRadialGradient(x, y, r * 0.15, x, y, r);
      gr.addColorStop(0, 'rgba(246,206,200,0.55)'); gr.addColorStop(0.55, 'rgba(232,150,146,0.7)'); gr.addColorStop(1, 'rgba(214,118,118,0.85)');
      g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); return;
    }
    if (it.kind === 'platelet') { g.fillStyle = 'rgba(120,60,150,0.8)'; g.beginPath(); g.ellipse(x, y, r, r * 0.7, it.a, 0, Math.PI * 2); g.fill(); return; }
    const R2 = rng(it.seed | 0);
    g.fillStyle = it.kind === 'lymphocyte' ? 'rgba(170,190,230,0.8)' : it.kind === 'monocyte' ? 'rgba(190,190,215,0.75)' : 'rgba(230,205,215,0.8)';
    g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
    if (it.kind === 'eosinophil' || it.kind === 'basophil') { g.fillStyle = it.kind === 'eosinophil' ? 'rgba(220,70,60,0.85)' : 'rgba(40,30,90,0.85)'; for (let i = 0; i < 40; i++) { const a = R2() * 6.28; const d = R2() * r * 0.9; g.beginPath(); g.arc(x + Math.cos(a) * d, y + Math.sin(a) * d, 0.45, 0, Math.PI * 2); g.fill(); } }
    g.fillStyle = 'rgba(80,40,130,0.92)';
    if (it.kind === 'neutrophil') { const n = 3 + Math.floor(R2() * 3); for (let i = 0; i < n; i++) { const a = it.a + i * 1.2; g.beginPath(); g.ellipse(x + Math.cos(a) * r * 0.42, y + Math.sin(a) * r * 0.42, r * 0.3, r * 0.22, a, 0, Math.PI * 2); g.fill(); } }
    else if (it.kind === 'lymphocyte') { g.beginPath(); g.arc(x + 0.4, y, r * 0.82, 0, Math.PI * 2); g.fill(); }
    else if (it.kind === 'monocyte') { g.beginPath(); g.ellipse(x, y, r * 0.55, r * 0.38, it.a, 0.4, Math.PI * 2 - 0.4); g.quadraticCurveTo(x, y, x + Math.cos(it.a + 0.4) * r * 0.5, y + Math.sin(it.a + 0.4) * r * 0.3); g.fill(); }
    else if (it.kind === 'eosinophil') { for (const s of [-1, 1]) { g.beginPath(); g.ellipse(x + s * r * 0.35, y, r * 0.3, r * 0.24, 0, 0, Math.PI * 2); g.fill(); } }
    else if (it.kind === 'basophil') { g.fillStyle = 'rgba(90,60,150,0.6)'; g.beginPath(); g.ellipse(x, y, r * 0.5, r * 0.35, it.a, 0, Math.PI * 2); g.fill(); }
  }
  return {
    width: W, height: H, start: { x: W / 2, y: H / 2 }, background: '#f6efe6', mount: {},
    draw(g, v) { visit(grid, B, v, (it) => { if (it.kind === 'red blood cell') cell(g, it); }); visit(grid, B, v, (it) => { if (it.kind !== 'red blood cell') cell(g, it); }); },
    featureAt(x, y) { const w = near(grid, B, x, y, (it) => it.kind !== 'red blood cell'); if (w) return w.kind; const r = near(grid, B, x, y); return r ? r.kind : null; },
    find: ['red blood cell', 'neutrophil', 'lymphocyte', 'monocyte', 'eosinophil', 'platelet'],
    nearestOf(kind, x, y) { let best = null; let bd = Infinity; items.forEach((it) => { if (it.kind === kind) { const d = Math.hypot(it.x - x, it.y - y); if (d < bd) { bd = d; best = it; } } }); return best; },
  };
}

export function squamousField() {
  const R = rng(99); const W = 1800; const H = 1400; const items = [];
  const clusters = Array.from({ length: 14 }, () => [150 + R() * (W - 300), 150 + R() * (H - 300)]);
  clusters[0] = [W / 2, H / 2];
  for (let i = 0; i < 300; i++) {
    const cl = clusters[i % clusters.length]; const sp = 160;
    const x = cl[0] + (R() - 0.5) * sp * 2; const y = cl[1] + (R() - 0.5) * sp * 2; const r = 26 + R() * 12;
    const pts = []; const n = 6 + Math.floor(R() * 3); for (let k = 0; k < n; k++) { const a = (k / n) * Math.PI * 2 + R() * 0.4; const rr = r * (0.8 + R() * 0.35); pts.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); }
    items.push({ kind: 'cell', x, y, r, pts, nx: x + (R() - 0.5) * r * 0.3, ny: y + (R() - 0.5) * r * 0.3, fold: R() });
  }
  const B = 120; const grid = gridOf(items, B);
  return {
    width: W, height: H, start: { x: W / 2, y: H / 2 }, background: '#eef2f6', mount: {},
    draw(g, v) {
      visit(grid, B, v, (it) => {
        g.beginPath(); it.pts.forEach(([px, py], i) => (i ? g.lineTo(px, py) : g.moveTo(px, py))); g.closePath();
        g.fillStyle = 'rgba(150,180,215,0.32)'; g.fill(); g.strokeStyle = 'rgba(60,90,150,0.6)'; g.lineWidth = 1.2; g.stroke();
        if (it.fold > 0.6) { g.strokeStyle = 'rgba(80,110,160,0.25)'; g.beginPath(); g.moveTo(it.pts[0][0], it.pts[0][1]); g.quadraticCurveTo(it.x, it.y + 8, it.pts[3][0], it.pts[3][1]); g.stroke(); }
        g.fillStyle = 'rgba(40,60,140,0.85)'; g.beginPath(); g.ellipse(it.nx, it.ny, 5, 4, 0, 0, Math.PI * 2); g.fill();
      });
    },
    featureAt(x, y) { const c = near(grid, B, x, y); if (!c) return null; const dn = Math.hypot(x - c.nx, y - c.ny); if (dn < 7) return 'nucleus'; let minEdge = Infinity; c.pts.forEach(([px, py]) => { minEdge = Math.min(minEdge, Math.hypot(px - x, py - y)); }); return minEdge < 8 ? 'cell membrane' : 'cytoplasm'; },
    find: ['nucleus', 'cytoplasm', 'cell membrane'],
  };
}

export function muscleField() {
  const R = rng(7); const W = 1600; const H = 1200; const fibres = [];
  let y = 40; while (y < H - 40) { const h = 50 + R() * 20; fibres.push({ y0: y, y1: y + h, ph: R() * 3, nuclei: Array.from({ length: 9 }, () => ({ x: R() * W, top: R() < 0.5 })) }); y += h + 6 + R() * 6; }
  const sarc = 2.3; // sarcomere length, µm
  return {
    width: W, height: H, start: { x: W / 2, y: H / 2 }, background: '#f4ece8', mount: {},
    draw(g, v) {
      const x0 = v.cx - v.halfW; const x1 = v.cx + v.halfW;
      fibres.forEach((f) => {
        if (f.y1 < v.cy - v.halfH || f.y0 > v.cy + v.halfH) return;
        g.fillStyle = 'rgba(214,150,170,0.55)'; g.fillRect(x0, f.y0, x1 - x0, f.y1 - f.y0);
        if (v.scale > 0.6) { g.fillStyle = 'rgba(150,60,100,0.5)'; const s0 = Math.floor(x0 / sarc); for (let k = s0; k * sarc < x1; k++) { const x = k * sarc + Math.sin(f.y0 * 0.02 + k * 0.01) * 0.3; g.fillRect(x, f.y0, sarc * 0.55, f.y1 - f.y0); } }
        g.strokeStyle = 'rgba(120,50,80,0.7)'; g.lineWidth = 1.2; g.strokeRect(x0, f.y0, x1 - x0, f.y1 - f.y0);
        g.fillStyle = 'rgba(70,30,110,0.9)'; f.nuclei.forEach((n) => { g.beginPath(); g.ellipse(n.x, n.top ? f.y0 + 4 : f.y1 - 4, 7, 2.6, 0, 0, Math.PI * 2); g.fill(); });
      });
    },
    featureAt(x, y) {
      const f = fibres.find((q) => y >= q.y0 - 2 && y <= q.y1 + 2); if (!f) return null;
      if (f.nuclei.some((n) => Math.abs(n.x - x) < 9 && Math.abs((n.top ? f.y0 + 4 : f.y1 - 4) - y) < 5)) return 'nucleus';
      if (y - f.y0 < 2.5 || f.y1 - y < 2.5) return 'sarcolemma';
      const ph = ((x / sarc) % 1 + 1) % 1; return ph < 0.55 ? 'dark band (A band)' : 'light band (I band)';
    },
    find: ['dark band (A band)', 'light band (I band)', 'nucleus', 'sarcolemma'],
  };
}

const FROG = ['fertilised egg', '2-cell stage', '4-cell stage', '8-cell stage', 'morula', 'blastula', 'gastrula'];
export function frogField() {
  const W = 1500 * 2 + 6 * 2600; const H = 3200; const items = FROG.map((s, i) => ({ kind: s, x: 1500 + i * 2600, y: H / 2 + (i % 2 ? 160 : -160), r: 780 }));
  function embryo(g, it) {
    const { x, y, r } = it;
    const gr = g.createLinearGradient(x, y - r, x, y + r);
    gr.addColorStop(0, '#3b2a24'); gr.addColorStop(0.48, '#5a4136'); gr.addColorStop(0.62, '#d9c9a6'); gr.addColorStop(1, '#efe3c4');
    g.fillStyle = 'rgba(220,235,240,0.35)'; g.beginPath(); g.arc(x, y, r * 1.35, 0, Math.PI * 2); g.fill();
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
    g.strokeStyle = 'rgba(30,20,15,0.55)'; g.lineWidth = 10;
    const k = FROG.indexOf(it.kind);
    if (k >= 1 && k <= 3) { g.beginPath(); g.moveTo(x, y - r); g.lineTo(x, y + r); g.stroke(); }
    if (k >= 2 && k <= 3) { g.beginPath(); g.ellipse(x, y, r * 0.3, r, 0, -Math.PI / 2, Math.PI / 2); g.stroke(); g.beginPath(); g.ellipse(x, y, r * 0.3, r, 0, Math.PI / 2, Math.PI * 1.5); g.stroke(); }
    if (k === 3) { g.beginPath(); g.moveTo(x - r * 0.98, y - r * 0.25); g.quadraticCurveTo(x, y - r * 0.12, x + r * 0.98, y - r * 0.25); g.stroke(); }
    if (k === 4) { g.lineWidth = 5; const R = rng(3); for (let i = 0; i < 46; i++) { const a = R() * 6.28; const d = Math.sqrt(R()) * r * 0.85; const cr = d < r * 0.5 && Math.sin(a) < 0 ? 60 : 110; g.beginPath(); g.arc(x + Math.cos(a) * d, y + Math.sin(a) * d, cr, 0, Math.PI * 2); g.stroke(); } }
    if (k === 5) { g.fillStyle = 'rgba(240,235,220,0.9)'; g.beginPath(); g.ellipse(x, y - r * 0.28, r * 0.5, r * 0.32, 0, 0, Math.PI * 2); g.fill(); g.strokeStyle = 'rgba(30,20,15,0.35)'; g.lineWidth = 6; g.stroke(); }
    if (k === 6) { g.fillStyle = '#efe3c4'; g.beginPath(); g.arc(x, y + r * 0.62, r * 0.22, 0, Math.PI * 2); g.fill(); g.strokeStyle = 'rgba(30,20,15,0.8)'; g.lineWidth = 14; g.beginPath(); g.arc(x, y + r * 0.62, r * 0.24, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); }
  }
  return {
    width: W, height: H, start: { x: items[0].x, y: H / 2 }, background: '#f1f3ee', mount: {}, items,
    draw(g) { items.forEach((it) => embryo(g, it)); },
    featureAt(x, y) { const it = items.find((q) => Math.hypot(q.x - x, q.y - y) < q.r * 1.2); return it ? it.kind : null; },
    find: FROG,
  };
}

export function letterField() {
  const W = 3000; const H = 3000;
  return {
    width: W, height: H, start: { x: W / 2, y: H / 2 }, background: '#f7f5ef', mount: {},
    draw(g) {
      // newsprint: fibres, and the letter printed as dots of ink, drawn upside down and mirrored (as the microscope shows it)
      g.save(); g.translate(W / 2, H / 2); g.rotate(Math.PI);
      g.fillStyle = 'rgba(25,25,30,0.9)'; g.font = '700 1600px Georgia, serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('e', 0, 0);
      g.restore();
      const R = rng(8); g.strokeStyle = 'rgba(150,140,120,0.25)'; g.lineWidth = 6; for (let i = 0; i < 120; i++) { const x = R() * W; const y = R() * H; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 150, y + (R() - 0.5) * 120, x + 300, y + (R() - 0.5) * 60); g.stroke(); }
    },
    featureAt() { return null; },
    find: [],
  };
}
