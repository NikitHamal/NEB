// A drop of pond water under the microscope, in micrometres, alive. Phytoplankton: Spirogyra
// filaments with spiral chloroplasts, boat-shaped diatoms, Volvox colonies rolling slowly,
// Chlamydomonas darting on two flagella, gliding blue-green Oscillatoria and green Euglena.
// Zooplankton: Paramecium, a rotifer with its beating corona, a Cyclops with its single eye and
// egg sacs, and a water flea (Daphnia) with its heart and brood pouch — large enough to need the 4×.
import { rng } from '../kit.js';

export const POND_KINDS = {
  Spirogyra: 'producer', Diatom: 'producer', Volvox: 'producer', Chlamydomonas: 'producer', Oscillatoria: 'producer', Euglena: 'producer',
  Paramecium: 'consumer', Rotifer: 'consumer', Cyclops: 'consumer', Daphnia: 'consumer',
};

export function createPondField(seed = 7) {
  const R = rng(seed); const W = 6000; const H = 4500; const items = [];
  const add = (kind, n, r, speed, extra = {}) => { for (let i = 0; i < n; i++) items.push({ kind, x0: 250 + R() * (W - 500), y0: 250 + R() * (H - 500), r, a: R() * 6.28, sp: speed * (0.6 + R() * 0.8), ph: R() * 6.28, turn: (R() - 0.5) * 0.6, ...extra }); };
  add('Spirogyra', 5, 600, 0, {}); add('Diatom', 14, 32, 3); add('Volvox', 4, 210, 12); add('Chlamydomonas', 12, 9, 55);
  add('Oscillatoria', 4, 450, 2); add('Euglena', 6, 30, 30); add('Paramecium', 6, 100, 70); add('Rotifer', 4, 120, 10);
  add('Cyclops', 3, 450, 45); add('Daphnia', 2, 700, 25);
  items.forEach((it) => { if (it.kind === 'Spirogyra') { it.len = 900 + R() * 900; it.w = 38; } if (it.kind === 'Oscillatoria') { it.len = 500 + R() * 500; it.w = 8; } });
  // the first few of each kind start near the centre so a student finds them without a long hunt
  const seen = new Set(); items.forEach((it) => { if (!seen.has(it.kind)) { seen.add(it.kind); const a = R() * 6.28; const d = 300 + R() * 600; it.x0 = W / 2 + Math.cos(a) * d; it.y0 = H / 2 + Math.sin(a) * d; } });
  let lastT = 0;
  function pos(it, t) {
    if (!it.sp) return [it.x0, it.y0, it.a];
    const a = it.a + Math.sin(t * 0.3 + it.ph) * it.turn * 2 + t * it.turn * 0.15;
    const d = it.sp * t;
    let x = it.x0 + Math.cos(it.a) * d + Math.sin(t * 0.7 + it.ph) * it.sp * 0.6; let y = it.y0 + Math.sin(it.a) * d + Math.cos(t * 0.5 + it.ph) * it.sp * 0.6;
    x = ((x % W) + W) % W; y = ((y % H) + H) % H; return [x, y, a];
  }
  function draw1(g, it, t) {
    const [x, y, a] = pos(it, t);
    g.save(); g.translate(x, y); g.rotate(a);
    switch (it.kind) {
      case 'Spirogyra': {
        const L = it.len; const w = it.w; const cell = 70;
        g.fillStyle = 'rgba(200,235,190,0.55)'; g.strokeStyle = 'rgba(60,110,50,0.8)'; g.lineWidth = 2; g.fillRect(-L / 2, -w / 2, L, w); g.strokeRect(-L / 2, -w / 2, L, w);
        for (let c = -L / 2; c < L / 2; c += cell) { g.beginPath(); g.moveTo(c, -w / 2); g.lineTo(c, w / 2); g.stroke(); }
        g.strokeStyle = 'rgba(40,140,40,0.9)'; g.lineWidth = 6; g.beginPath(); for (let s = -L / 2; s <= L / 2; s += 4) { const yy = Math.sin(s / 22) * (w / 2 - 6); s === -L / 2 ? g.moveTo(s, yy) : g.lineTo(s, yy); } g.stroke();
        g.fillStyle = 'rgba(120,90,60,0.6)'; for (let c = -L / 2 + cell / 2; c < L / 2; c += cell) { g.beginPath(); g.arc(c, 0, 5, 0, 6.28); g.fill(); }
        break;
      }
      case 'Diatom': {
        g.fillStyle = 'rgba(200,170,90,0.7)'; g.strokeStyle = 'rgba(120,90,30,0.9)'; g.lineWidth = 1.5;
        g.beginPath(); g.ellipse(0, 0, it.r * 1.6, it.r * 0.45, 0, 0, 6.28); g.fill(); g.stroke();
        g.strokeStyle = 'rgba(120,90,30,0.4)'; for (let k = -6; k <= 6; k++) { g.beginPath(); g.moveTo(k * it.r * 0.22, -it.r * 0.4); g.lineTo(k * it.r * 0.22, it.r * 0.4); g.stroke(); }
        g.beginPath(); g.moveTo(-it.r * 1.4, 0); g.lineTo(it.r * 1.4, 0); g.stroke();
        break;
      }
      case 'Volvox': {
        const r = it.r; g.fillStyle = 'rgba(150,210,120,0.25)'; g.strokeStyle = 'rgba(60,130,50,0.7)'; g.lineWidth = 3; g.beginPath(); g.arc(0, 0, r, 0, 6.28); g.fill(); g.stroke();
        g.fillStyle = 'rgba(40,140,40,0.85)'; const Rr = rng(7); for (let k = 0; k < 180; k++) { const aa = Rr() * 6.28; const rr = Math.sqrt(Rr()) * r * 0.97; g.beginPath(); g.arc(Math.cos(aa + t * 0.2) * rr, Math.sin(aa + t * 0.2) * rr, 4, 0, 6.28); g.fill(); }
        g.fillStyle = 'rgba(30,110,30,0.75)'; for (let k = 0; k < 4; k++) { g.beginPath(); g.arc(Math.cos(k * 1.7 + t * 0.2) * r * 0.45, Math.sin(k * 1.7 + t * 0.2) * r * 0.45, r * 0.18, 0, 6.28); g.fill(); }
        break;
      }
      case 'Chlamydomonas': {
        g.fillStyle = 'rgba(60,160,60,0.95)'; g.beginPath(); g.ellipse(0, 0, it.r * 1.3, it.r, 0, 0, 6.28); g.fill();
        g.fillStyle = '#dc2626'; g.beginPath(); g.arc(it.r * 0.6, -it.r * 0.4, 1.8, 0, 6.28); g.fill();
        g.strokeStyle = 'rgba(60,90,60,0.6)'; g.lineWidth = 1; const f = Math.sin(t * 20 + it.ph) * 0.5; [-1, 1].forEach((s) => { g.beginPath(); g.moveTo(it.r * 1.2, 0); g.quadraticCurveTo(it.r * 2.2, s * it.r * (1.2 + f), it.r * 3, s * it.r * 2); g.stroke(); });
        break;
      }
      case 'Oscillatoria': {
        const L = it.len; g.fillStyle = 'rgba(40,110,110,0.85)'; g.fillRect(-L / 2, -it.w / 2, L, it.w);
        g.strokeStyle = 'rgba(20,70,70,0.6)'; g.lineWidth = 0.8; for (let c = -L / 2; c < L / 2; c += 5) { g.beginPath(); g.moveTo(c, -it.w / 2); g.lineTo(c, it.w / 2); g.stroke(); }
        break;
      }
      case 'Euglena': {
        const k = 1 + Math.sin(t * 3 + it.ph) * 0.15; g.fillStyle = 'rgba(70,170,70,0.85)'; g.beginPath(); g.ellipse(0, 0, it.r * 1.6 * k, it.r * 0.5 / k, 0, 0, 6.28); g.fill();
        g.fillStyle = '#dc2626'; g.beginPath(); g.arc(it.r * 1.1, 0, 3, 0, 6.28); g.fill();
        g.strokeStyle = 'rgba(60,90,60,0.6)'; g.lineWidth = 1.2; g.beginPath(); g.moveTo(it.r * 1.6, 0); g.quadraticCurveTo(it.r * 2.6, Math.sin(t * 12) * 18, it.r * 3.4, 0); g.stroke();
        break;
      }
      case 'Paramecium': {
        g.fillStyle = 'rgba(210,215,225,0.75)'; g.strokeStyle = 'rgba(90,100,120,0.85)'; g.lineWidth = 2;
        g.beginPath(); g.ellipse(0, 0, it.r * 1.2, it.r * 0.42, 0, 0, 6.28); g.fill(); g.stroke();
        g.strokeStyle = 'rgba(90,100,120,0.35)'; g.lineWidth = 1; for (let k = 0; k < 60; k++) { const aa = k / 60 * 6.28; const w = Math.sin(t * 25 + k) * 3; g.beginPath(); g.moveTo(Math.cos(aa) * it.r * 1.2, Math.sin(aa) * it.r * 0.42); g.lineTo(Math.cos(aa) * (it.r * 1.2 + 8 + w), Math.sin(aa) * (it.r * 0.42 + 8 + w)); g.stroke(); }
        g.fillStyle = 'rgba(120,110,160,0.6)'; g.beginPath(); g.ellipse(0, 0, 22, 14, 0, 0, 6.28); g.fill();
        g.strokeStyle = 'rgba(80,90,110,0.7)'; g.beginPath(); g.arc(-it.r * 0.6, 0, 12, 0, 6.28); g.stroke(); g.beginPath(); g.arc(it.r * 0.6, 0, 12, 0, 6.28); g.stroke();
        break;
      }
      case 'Rotifer': {
        g.fillStyle = 'rgba(225,215,195,0.75)'; g.strokeStyle = 'rgba(120,100,70,0.85)'; g.lineWidth = 2;
        g.beginPath(); g.moveTo(-it.r, 0); g.quadraticCurveTo(-it.r * 0.2, -it.r * 0.6, it.r * 0.6, -it.r * 0.35); g.lineTo(it.r * 0.6, it.r * 0.35); g.quadraticCurveTo(-it.r * 0.2, it.r * 0.6, -it.r, 0); g.fill(); g.stroke();
        g.strokeStyle = 'rgba(120,100,70,0.6)'; [-1, 1].forEach((s) => { g.beginPath(); g.arc(it.r * 0.75, s * it.r * 0.22, it.r * 0.22, 0, 6.28); g.stroke(); for (let k = 0; k < 10; k++) { const aa = k / 10 * 6.28 + t * 9; g.beginPath(); g.moveTo(it.r * 0.75 + Math.cos(aa) * it.r * 0.22, s * it.r * 0.22 + Math.sin(aa) * it.r * 0.22); g.lineTo(it.r * 0.75 + Math.cos(aa) * it.r * 0.32, s * it.r * 0.22 + Math.sin(aa) * it.r * 0.32); g.stroke(); } });
        g.fillStyle = 'rgba(150,110,60,0.6)'; g.beginPath(); g.arc(0, 0, it.r * 0.18, 0, 6.28); g.fill();
        break;
      }
      case 'Cyclops': {
        const r = it.r; g.fillStyle = 'rgba(200,180,150,0.7)'; g.strokeStyle = 'rgba(110,80,50,0.9)'; g.lineWidth = 3;
        g.beginPath(); g.ellipse(r * 0.2, 0, r * 0.55, r * 0.32, 0, 0, 6.28); g.fill(); g.stroke();
        g.beginPath(); g.moveTo(-r * 0.3, 0); g.lineTo(-r * 0.95, 0); g.stroke();
        [-1, 1].forEach((s) => { g.beginPath(); g.moveTo(r * 0.7, s * r * 0.1); g.quadraticCurveTo(r * 0.9, s * r * 0.6, r * 0.5, s * r * 0.95); g.stroke(); g.fillStyle = 'rgba(120,150,60,0.75)'; g.beginPath(); g.ellipse(-r * 0.45, s * r * 0.22, r * 0.22, r * 0.11, s * 0.3, 0, 6.28); g.fill(); g.fillStyle = 'rgba(200,180,150,0.7)'; });
        g.fillStyle = '#b91c1c'; g.beginPath(); g.arc(r * 0.6, 0, r * 0.06, 0, 6.28); g.fill();
        break;
      }
      case 'Daphnia': {
        const r = it.r; g.fillStyle = 'rgba(220,190,150,0.55)'; g.strokeStyle = 'rgba(120,80,40,0.9)'; g.lineWidth = 4;
        g.beginPath(); g.ellipse(0, 0, r * 0.6, r * 0.42, 0, 0, 6.28); g.fill(); g.stroke();
        g.beginPath(); g.moveTo(-r * 0.55, 0.1 * r); g.lineTo(-r * 0.95, r * 0.25); g.stroke();
        g.beginPath(); g.arc(r * 0.55, -r * 0.05, r * 0.2, 0, 6.28); g.stroke();
        g.fillStyle = '#111'; g.beginPath(); g.arc(r * 0.62, -r * 0.05, r * 0.06, 0, 6.28); g.fill();
        const sw = Math.sin(t * 6 + it.ph) * 0.3; [-1, 1].forEach((s) => { g.beginPath(); g.moveTo(r * 0.5, s * r * 0.15); g.lineTo(r * 0.8, s * r * (0.55 + sw)); g.lineTo(r * 1.05, s * r * (0.7 + sw)); g.stroke(); });
        g.fillStyle = 'rgba(200,60,60,0.6)'; g.beginPath(); g.arc(r * 0.15, -r * 0.25, r * 0.06 * (1 + 0.3 * Math.sin(t * 15)), 0, 6.28); g.fill();
        g.fillStyle = 'rgba(90,120,60,0.6)'; for (let k = 0; k < 5; k++) { g.beginPath(); g.arc(-r * 0.15 + k * r * 0.07, -r * 0.18, r * 0.05, 0, 6.28); g.fill(); }
        g.strokeStyle = 'rgba(80,110,40,0.6)'; g.lineWidth = 6; g.beginPath(); g.moveTo(r * 0.4, 0.05 * r); g.quadraticCurveTo(0, r * 0.25, -r * 0.4, 0.05 * r); g.stroke();
        break;
      }
      default: break;
    }
    g.restore();
  }
  return {
    width: W, height: H, start: { x: W / 2, y: H / 2 }, background: '#eef3ea', animated: true, mount: {},
    draw(g, v) { lastT = v.t || 0; items.forEach((it) => { const [x, y] = pos(it, lastT); const ext = (it.len || it.r * 2) + 60; if (Math.abs(x - v.cx) > v.halfW + ext || Math.abs(y - v.cy) > v.halfH + ext) return; draw1(g, it, lastT); }); },
    hit(x, y) {
      let best = null; let bd = Infinity;
      items.forEach((it) => {
        const [px, py, a] = pos(it, lastT); const dx = x - px; const dy = y - py; const ca = Math.cos(-a); const sa = Math.sin(-a); const lx = dx * ca - dy * sa; const ly = dx * sa + dy * ca;
        let inside; if (it.len) inside = Math.abs(lx) < it.len / 2 && Math.abs(ly) < it.w / 2 + 25; else inside = Math.hypot(lx / (it.r * 1.6 + 25), ly / (it.r + 25)) < 1;
        const d = Math.hypot(dx, dy); if (inside && d < bd) { bd = d; best = it; }
      });
      return best;
    },
    featureAt(x, y) { const h = this.hit(x, y); return h ? h.kind : null; },
    nearestOf(kind) { const it = items.find((q) => q.kind === kind); const [x, y] = pos(it, lastT); return { x, y }; },
  };
}
