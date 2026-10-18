// Transverse sections of stems and roots in micrometres, stained with safranin: lignified walls
// (xylem, sclerenchyma) take a deep red, cellulose walls stay pale. Built ring by ring from the
// outside in, as the textbook diagrams are read.
// Dicot stem (sunflower): cuticle, epidermis with hairs, collenchymatous hypodermis, parenchyma
// cortex, a wavy endodermis (starch sheath), sclerenchyma caps of the pericycle, a ring of
// conjoint, collateral, open bundles (phloem outside, cambium, endarch xylem), medullary rays, pith.
// Monocot stem (maize): epidermis, sclerenchymatous hypodermis, undifferentiated ground tissue
// with scattered, closed, skull-shaped bundles in sclerenchyma sheaths, small and crowded toward
// the edge. Dicot root (gram): epiblema with root hairs, wide cortex, endodermis with Casparian
// strips and passage cells, pericycle, a radial tetrarch exarch xylem star with phloem between.
// Monocot root (maize): the same plan but polyarch (many xylem groups) round a large pith.
import { rng } from '../kit.js';

const RED = (a) => `rgba(170,20,45,${a})`;
function sector(g, cx, cy, r0, r1, a0, a1) { g.moveTo(cx + Math.cos(a0) * r0, cy + Math.sin(a0) * r0); g.lineTo(cx + Math.cos(a0) * r1, cy + Math.sin(a0) * r1); g.lineTo(cx + Math.cos(a1) * r1, cy + Math.sin(a1) * r1); g.lineTo(cx + Math.cos(a1) * r0, cy + Math.sin(a1) * r0); g.closePath(); }

export function createSectionField(kind, mount = {}) {
  const R = rng(kind.length * 977 + 13);
  const stem = kind.endsWith('Stem'); const dicot = kind.startsWith('dicot');
  const RAD = stem ? (dicot ? 1450 : 1500) : (dicot ? 1050 : 1250);
  const W = RAD * 2 + 600; const H = W; const C = W / 2;
  const stain = mount.stain ?? 1; const thick = mount.thick || 0;
  const rings = []; // {r0, r1, size, fill, wall, kind}
  const bundles = []; // {r, a, s}
  const hairs = [];
  const T = {};
  function band(name, r0, r1, size, fill, wall, lig = false, extra = {}) { T[name] = [r0, r1]; rings.push(Object.assign({ name, r0, r1, size, fill, wall, lig }, extra)); }
  if (kind === 'dicotStem') {
    band('epidermis', RAD - 22, RAD, 22, 'rgba(240,236,220,0.55)', 'rgba(90,80,60,0.7)');
    band('hypodermis', RAD - 110, RAD - 22, 24, 'rgba(240,238,225,0.5)', 'rgba(150,120,90,0.75)', false, { collen: true });
    band('cortex', RAD - 300, RAD - 110, 42, 'rgba(244,242,232,0.45)', 'rgba(110,100,80,0.5)', false, { round: true });
    band('endodermis', RAD - 325, RAD - 300, 25, 'rgba(236,228,200,0.6)', 'rgba(110,90,60,0.7)', false, { starch: true });
    band('pith', 0, RAD - 760, 70, 'rgba(246,244,236,0.4)', 'rgba(120,110,90,0.45)', false, { round: true });
    band('medullary ray', RAD - 760, RAD - 325, 34, 'rgba(244,242,232,0.42)', 'rgba(120,110,90,0.45)');
    for (let i = 0; i < 12; i++) bundles.push({ a: (i / 12) * Math.PI * 2 + (R() - 0.5) * 0.08, r: RAD - 545, s: 1.05 + (i % 2 ? -0.25 : 0.1) });
    for (let i = 0; i < 30; i++) hairs.push({ a: R() * Math.PI * 2, len: 120 + R() * 140, n: 3 + Math.floor(R() * 3) });
    T.pericycle = [RAD - 380, RAD - 325]; T['vascular bundle'] = [RAD - 760, RAD - 380];
  } else if (kind === 'monocotStem') {
    band('epidermis', RAD - 20, RAD, 20, 'rgba(240,236,220,0.55)', 'rgba(90,80,60,0.7)');
    band('hypodermis', RAD - 75, RAD - 20, 18, 'rgba(230,200,200,0.5)', RED(0.85), true);
    band('ground tissue', 0, RAD - 75, 60, 'rgba(246,244,236,0.42)', 'rgba(120,110,90,0.45)', false, { round: true });
    // scattered bundles: many small ones near the edge, fewer larger ones inside
    let tries = 0;
    while (bundles.length < 40 && tries < 4000) {
      tries++;
      const r = Math.sqrt(R()) * (RAD - 170); const a = R() * Math.PI * 2;
      const s = 0.8 + 0.6 * (1 - r / RAD) + R() * 0.2;
      if (bundles.every((b) => Math.hypot(Math.cos(a) * r - Math.cos(b.a) * b.r, Math.sin(a) * r - Math.sin(b.a) * b.r) > 150 * (s + b.s) / 2 + 40)) bundles.push({ a, r, s });
    }
  } else {
    const poly = kind === 'monocotRoot';
    band('epiblema', RAD - 24, RAD, 24, 'rgba(240,236,220,0.55)', 'rgba(90,80,60,0.7)');
    band('cortex', poly ? 520 : 330, RAD - 24, 48, 'rgba(244,242,232,0.45)', 'rgba(110,100,80,0.5)', false, { round: true });
    band('endodermis', (poly ? 520 : 330) - 24, poly ? 520 : 330, 24, 'rgba(236,228,200,0.6)', 'rgba(110,90,60,0.75)', false, { casparian: true, arms: poly ? 14 : 4 });
    band('pericycle', (poly ? 496 : 306) - 20, poly ? 496 : 306, 20, 'rgba(244,240,226,0.5)', 'rgba(110,100,80,0.6)');
    if (poly) band('pith', 0, 300, 50, 'rgba(246,244,236,0.4)', 'rgba(120,110,90,0.45)', false, { round: true });
    else band('conjunctive tissue', 0, 286, 26, 'rgba(246,244,236,0.4)', 'rgba(120,110,90,0.45)');
    for (let i = 0; i < 70; i++) hairs.push({ a: R() * Math.PI * 2, len: 150 + R() * 260, n: 1 });
    T.xylem = [poly ? 300 : 0, poly ? 476 : 286]; T.phloem = T.xylem;
  }
  const arms = kind === 'monocotRoot' ? 14 : 4;

  function drawRings(g, s, detail) {
    for (const b of rings) {
      const n = Math.max(1, Math.round((b.r1 - b.r0) / b.size));
      for (let k = 0; k < n; k++) {
        const r0 = b.r0 + (k / n) * (b.r1 - b.r0); const r1 = b.r0 + ((k + 1) / n) * (b.r1 - b.r0);
        const rm = (r0 + r1) / 2; const cells = Math.max(6, Math.round((Math.PI * 2 * rm) / b.size));
        if (rm < b.size * 0.8) continue;
        const off = (k % 2) * 0.5;
        g.beginPath();
        for (let i = 0; i < cells; i++) {
          const a0 = ((i + off) / cells) * Math.PI * 2; const a1 = ((i + 1 + off) / cells) * Math.PI * 2;
          if (b.round && detail) { const j = 0.4 + 0.1 * Math.sin(i * 12.9898 + k * 78.233); const am = (a0 + a1) / 2 + Math.sin(i * 3.1 + k) * 0.15 / cells; const rr = Math.min(r1 - r0, rm * (a1 - a0)) * j * 1.05; const x = C + Math.cos(am) * rm; const y = C + Math.sin(am) * rm; g.moveTo(x + rr, y); g.ellipse(x, y, rr, rr * (0.85 + 0.15 * Math.cos(i)), am, 0, Math.PI * 2); }
          else sector(g, C, C, r0, r1, a0, a1);
        }
        g.fillStyle = b.fill; g.fill();
        g.strokeStyle = b.lig ? RED(0.45 + 0.45 * stain) : b.wall; g.lineWidth = (b.lig ? 3 : 1.4) / Math.max(0.4, s); g.stroke();
        if (b.collen && detail) { g.fillStyle = 'rgba(205,190,170,0.55)'; for (let i = 0; i < cells; i++) { const a = ((i + off) / cells) * Math.PI * 2; g.beginPath(); g.arc(C + Math.cos(a) * r0, C + Math.sin(a) * r0, b.size * 0.16, 0, Math.PI * 2); g.fill(); } }
        if (b.starch && detail) { g.fillStyle = 'rgba(120,110,150,0.45)'; for (let i = 0; i < cells; i += 2) { const a = ((i + 0.5) / cells) * Math.PI * 2; g.beginPath(); g.arc(C + Math.cos(a) * rm, C + Math.sin(a) * rm, 3, 0, Math.PI * 2); g.fill(); } }
        if (b.casparian) { g.fillStyle = RED(0.5 + 0.4 * stain); for (let i = 0; i < cells; i++) { const a = ((i + off) / cells) * Math.PI * 2; g.beginPath(); g.arc(C + Math.cos(a) * rm, C + Math.sin(a) * rm, 3.2, 0, Math.PI * 2); g.fill(); } }
      }
    }
    if (kind === 'dicotStem' || kind === 'monocotStem') { g.strokeStyle = RED(0.5 * stain + 0.2); g.lineWidth = 5 / Math.max(0.4, s); g.beginPath(); g.arc(C, C, RAD + 2, 0, Math.PI * 2); g.stroke(); }
  }
  function vessel(g, x, y, r, s) { g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fillStyle = 'rgba(250,240,235,0.85)'; g.fill(); g.strokeStyle = RED(0.55 + 0.4 * stain); g.lineWidth = Math.max(2.2, r * 0.22) / Math.max(0.4, s) * Math.min(1, s * 2); g.stroke(); }
  function dicotBundle(g, b, s) {
    const cx = C + Math.cos(b.a) * b.r; const cy = C + Math.sin(b.a) * b.r; const ux = Math.cos(b.a); const uy = Math.sin(b.a); const vx = -uy; const vy = ux;
    const L = 300 * b.s; const Wd = 150 * b.s;
    const at = (u, v) => [cx + ux * u + vx * v, cy + uy * u + vy * v];
    // sclerenchyma cap (pericycle) outermost, then phloem, cambium, xylem toward the pith
    g.fillStyle = 'rgba(225,170,170,0.6)'; g.beginPath(); let p = at(L * 0.62, 0); g.ellipse(p[0], p[1], 38 * b.s, Wd * 0.62, b.a, 0, Math.PI * 2); g.fill();
    g.strokeStyle = RED(0.6 + 0.35 * stain); g.lineWidth = 2.5 / Math.max(0.4, s); g.stroke();
    for (let i = 0; i < 14; i++) { const q = at(L * 0.62 + (R2() - 0.5) * 50 * b.s, (R2() - 0.5) * Wd * 1.0); g.beginPath(); g.arc(q[0], q[1], 7 * b.s, 0, Math.PI * 2); g.stroke(); }
    g.fillStyle = 'rgba(230,236,210,0.75)'; g.beginPath(); p = at(L * 0.3, 0); g.ellipse(p[0], p[1], 48 * b.s, Wd * 0.55, b.a, 0, Math.PI * 2); g.fill();
    g.strokeStyle = 'rgba(100,110,80,0.55)'; g.lineWidth = 1 / Math.max(0.4, s); for (let i = 0; i < 16; i++) { const q = at(L * 0.3 + (R2() - 0.5) * 60 * b.s, (R2() - 0.5) * Wd * 0.9); g.beginPath(); g.arc(q[0], q[1], 6 * b.s, 0, Math.PI * 2); g.stroke(); }
    g.strokeStyle = 'rgba(120,120,90,0.7)'; g.lineWidth = 1 / Math.max(0.4, s); for (let k = 0; k < 3; k++) { const q0 = at(L * 0.05 + k * 8, -Wd * 0.5); const q1 = at(L * 0.05 + k * 8, Wd * 0.5); g.beginPath(); g.moveTo(q0[0], q0[1]); g.lineTo(q1[0], q1[1]); g.stroke(); }
    // endarch xylem: large metaxylem near the cambium, small protoxylem toward the pith
    for (let k = 0; k < 4; k++) for (let j = -1; j <= 1; j++) { const u = -L * (0.08 + k * 0.17); const r = (19 - k * 3.6) * b.s; const q = at(u, j * Wd * 0.28 * (1 - k * 0.18)); vessel(g, q[0], q[1], r, s); }
  }
  function monocotBundle(g, b, s) {
    const cx = C + Math.cos(b.a) * b.r; const cy = C + Math.sin(b.a) * b.r; const ux = Math.cos(b.a); const uy = Math.sin(b.a); const vx = -uy; const vy = ux;
    const at = (u, v) => [cx + ux * u + vx * v, cy + uy * u + vy * v];
    const k = b.s; const sh = 82 * k;
    g.fillStyle = 'rgba(232,200,200,0.55)'; g.beginPath(); g.ellipse(cx, cy, sh, sh * 0.82, b.a, 0, Math.PI * 2); g.fill();
    g.strokeStyle = RED(0.55 + 0.4 * stain); g.lineWidth = 9 * k / Math.max(0.6, s * 0.8); g.stroke();
    let p = at(sh * 0.42, 0); g.fillStyle = 'rgba(226,234,206,0.85)'; g.beginPath(); g.ellipse(p[0], p[1], sh * 0.32, sh * 0.42, b.a, 0, Math.PI * 2); g.fill();
    // two metaxylem "eyes", protoxylem below with the lysigenous water cavity: the skull
    for (const sd of [-1, 1]) { p = at(-sh * 0.05, sd * sh * 0.45); vessel(g, p[0], p[1], 17 * k, s); }
    p = at(-sh * 0.35, 0); vessel(g, p[0], p[1], 8 * k, s);
    p = at(-sh * 0.6, 0); g.fillStyle = 'rgba(255,255,250,0.9)'; g.beginPath(); g.ellipse(p[0], p[1], sh * 0.2, sh * 0.16, b.a, 0, Math.PI * 2); g.fill(); g.strokeStyle = 'rgba(150,140,110,0.6)'; g.lineWidth = 1 / Math.max(0.4, s); g.stroke();
  }
  function rootStele(g, s) {
    const r0 = kind === 'monocotRoot' ? 300 : 0; const r1 = (kind === 'monocotRoot' ? 476 : 286);
    for (let i = 0; i < arms; i++) {
      const a = (i / arms) * Math.PI * 2;
      // exarch: small protoxylem at the outer tip, larger metaxylem toward the centre
      const steps = kind === 'monocotRoot' ? 3 : 5;
      for (let k = 0; k < steps; k++) { const r = r1 - 16 - k * ((r1 - r0 - 30) / steps); const rad = 9 + k * (kind === 'monocotRoot' ? 9 : 5); vessel(g, C + Math.cos(a) * r, C + Math.sin(a) * r, rad, s); }
      const ap = a + Math.PI / arms; const rp = r1 - 60;
      g.fillStyle = 'rgba(226,234,206,0.85)'; g.beginPath(); g.ellipse(C + Math.cos(ap) * rp, C + Math.sin(ap) * rp, 40, 30, ap, 0, Math.PI * 2); g.fill();
      g.strokeStyle = 'rgba(100,110,80,0.55)'; g.lineWidth = 1 / Math.max(0.4, s); g.stroke();
    }
  }
  let R2 = rng(5);
  function drawHairs(g, s) {
    g.strokeStyle = 'rgba(120,110,90,0.55)'; g.fillStyle = 'rgba(245,242,232,0.5)'; g.lineWidth = 1.2 / Math.max(0.4, s);
    for (const h of hairs) {
      const x0 = C + Math.cos(h.a) * RAD; const y0 = C + Math.sin(h.a) * RAD;
      const x1 = C + Math.cos(h.a + 0.03) * (RAD + h.len); const y1 = C + Math.sin(h.a + 0.03) * (RAD + h.len);
      g.beginPath(); g.moveTo(x0, y0); g.quadraticCurveTo((x0 + x1) / 2 + 10, (y0 + y1) / 2, x1, y1); g.lineWidth = 7 / Math.max(0.4, s) * 0.6; g.stroke();
      if (h.n > 1) for (let k = 1; k < h.n; k++) { const t = k / h.n; g.beginPath(); g.arc(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 3, 0, Math.PI * 2); g.fill(); }
    }
  }
  function drawAll(g, s, detail) {
    R2 = rng(5);
    g.save(); g.beginPath(); g.arc(C, C, RAD, 0, Math.PI * 2); g.fillStyle = 'rgba(245,242,232,0.5)'; g.fill(); g.restore();
    drawRings(g, s, detail);
    if (kind === 'dicotStem') bundles.forEach((b) => dicotBundle(g, b, s));
    if (kind === 'monocotStem') bundles.forEach((b) => monocotBundle(g, b, s));
    if (!stem) rootStele(g, s);
    drawHairs(g, s);
    if (thick > 0) { g.fillStyle = `rgba(120,60,60,${0.25 * thick})`; g.beginPath(); g.arc(C, C, RAD, 0, Math.PI * 2); g.fill(); }
  }
  let low = null; const LOW = 0.32;
  return {
    width: W, height: H, start: { x: C, y: C }, background: '#f1eee4', mount, center: { x: C, y: C }, radius: RAD,
    draw(g, v) {
      if (v.scale < 0.55) { if (!low) { low = document.createElement('canvas'); low.width = Math.round(W * LOW); low.height = Math.round(H * LOW); const lg = low.getContext('2d'); lg.setTransform(LOW, 0, 0, LOW, 0, 0); drawAll(lg, LOW, false); } g.drawImage(low, 0, 0, W, H); }
      else drawAll(g, v.scale, v.scale > 0.35);
      if (thick > 0.5) { g.fillStyle = 'rgba(60,20,20,0.18)'; g.fillRect(0, 0, W, H); }
    },
    /** The tissue under a field point. */
    tissueAt(x, y) {
      const dx = x - C; const dy = y - C; const r = Math.hypot(dx, dy); const a = Math.atan2(dy, dx);
      if (r > RAD + 4) return r < RAD + 400 && hairs.length ? (stem ? 'hairs' : 'root hairs') : null;
      if (stem) {
        for (const b of bundles) {
          const bx = C + Math.cos(b.a) * b.r; const by = C + Math.sin(b.a) * b.r; const d = Math.hypot(x - bx, y - by);
          if (kind === 'dicotStem') {
            const u = (x - bx) * Math.cos(b.a) + (y - by) * Math.sin(b.a); const vv = Math.abs(-(x - bx) * Math.sin(b.a) + (y - by) * Math.cos(b.a));
            if (vv < 70 * b.s && u > -200 * b.s && u < 170 * b.s) return u > 85 * b.s ? 'sclerenchyma (pericycle)' : u > 15 * b.s ? 'phloem' : u > -5 * b.s ? 'cambium' : 'xylem';
          } else if (d < 82 * b.s) {
            const u = (x - bx) * Math.cos(b.a) + (y - by) * Math.sin(b.a);
            if (d > 66 * b.s) return 'bundle sheath'; return u > 10 * b.s ? 'phloem' : 'xylem';
          }
        }
      } else {
        const r1 = kind === 'monocotRoot' ? 476 : 286; const r0 = kind === 'monocotRoot' ? 300 : 0;
        if (r < r1 && r > r0) { const seg = (Math.PI * 2) / arms; const m = ((a % seg) + seg) % seg; return (m < seg * 0.25 || m > seg * 0.75) ? 'xylem' : 'phloem'; }
      }
      for (const b of rings) if (r >= b.r0 && r <= b.r1) return b.name;
      return null;
    },
    dispose() { low = null; },
  };
}
