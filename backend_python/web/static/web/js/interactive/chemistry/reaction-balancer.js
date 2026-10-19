/**
 * Reaction balancer — set the coefficients of real equations (tap the arrows or drag a number up
 * and down; subscripts are locked, as in chemistry). Each species is drawn as that many molecules
 * built from coloured atoms, an atom tally compares both sides element by element, and a beam
 * balance carries the total mass of each side (from atomic masses), tipping until the equation —
 * and the mass — balances.
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, withAlpha, card, sphere } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const MASS = { H: 1.008, C: 12.011, N: 14.007, O: 15.999, Na: 22.99, Mg: 24.305, Al: 26.982, S: 32.06, Cl: 35.45, K: 39.098, Ca: 40.078, Fe: 55.845, Cu: 63.546 };
const COLOR = { H: '#f1f5f9', C: '#334155', N: '#3b82f6', O: '#ef4444', Na: '#a855f7', Mg: '#22c55e', Al: '#cbd5e1', S: '#facc15', Cl: '#16a34a', K: '#8b5cf6', Ca: '#a3a3a3', Fe: '#c2410c', Cu: '#b45309' };
const EQS = [
  { name: 'Water', l: ['H2', 'O2'], r: ['H2O'] },
  { name: 'Methane burns', l: ['CH4', 'O2'], r: ['CO2', 'H2O'] },
  { name: 'Rusting', l: ['Fe', 'O2'], r: ['Fe2O3'] },
  { name: 'Ammonia', l: ['N2', 'H2'], r: ['NH3'] },
  { name: 'Magnesium burns', l: ['Mg', 'O2'], r: ['MgO'] },
  { name: 'Propane burns', l: ['C3H8', 'O2'], r: ['CO2', 'H2O'] },
  { name: 'Photosynthesis', l: ['CO2', 'H2O'], r: ['C6H12O6', 'O2'] },
  { name: 'Aluminium + acid', l: ['Al', 'HCl'], r: ['AlCl3', 'H2'] },
  { name: 'Neutralisation', l: ['NaOH', 'H2SO4'], r: ['Na2SO4', 'H2O'] },
  { name: 'Limewater test', l: ['Ca(OH)2', 'CO2'], r: ['CaCO3', 'H2O'] },
];

function parse(f) {
  const stack = [{}];
  let i = 0;
  while (i < f.length) {
    const ch = f[i];
    if (ch === '(') { stack.push({}); i++; continue; }
    if (ch === ')') { i++; let n = ''; while (i < f.length && /\d/.test(f[i])) n += f[i++]; const g = stack.pop(), m = n ? +n : 1; const top = stack[stack.length - 1]; for (const e in g) top[e] = (top[e] || 0) + g[e] * m; continue; }
    let el = ch; i++;
    while (i < f.length && /[a-z]/.test(f[i])) el += f[i++];
    let n = ''; while (i < f.length && /\d/.test(f[i])) n += f[i++];
    const top = stack[stack.length - 1]; top[el] = (top[el] || 0) + (n ? +n : 1);
  }
  return stack[0];
}
const SUB = '₀₁₂₃₄₅₆₇₈₉';
const pretty = (f) => f.replace(/\d/g, (d) => SUB[+d]);
function gcd(a, b) { return b ? gcd(b, a % b) : a; }

export default function init(stage) {
  const k = createKit(stage, { label: 'A chemical equation with adjustable coefficients, molecules and a mass balance' });
  const hud = createHud(stage);
  const badge = hud.badge('Change the big numbers until both sides match', T.blue);

  let eq = null, coef = [], species = [], elements = [], solved = false, celebrate = 0;
  const beam = new Spring(0, 40, 6);
  const pops = [];

  const panel = createPanel(stage, { title: 'Balance the equation' });
  panel.chips({ label: 'Reaction', options: EQS.map((e, i) => ({ value: String(i), label: e.name })), value: '0', onChange: (v) => load(+v) });
  panel.buttonRow([{ label: 'Hint', icon: 'lightbulb', onClick: hint }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: () => load(EQS.indexOf(eq)) }]);
  const st = panel.stats([{ key: 'l', label: 'Mass of reactants' }, { key: 'r', label: 'Mass of products' }, { key: 'ok', label: 'Elements balanced' }, { key: 'state', label: 'Equation' }]);
  panel.info('Only the big numbers in front (coefficients) may change: changing a subscript would make a different substance. Start with the element that appears in the fewest substances; leave H and O till last.');

  function load(i) {
    eq = EQS[i];
    species = eq.l.map((f) => ({ f, side: 0, atoms: parse(f) })).concat(eq.r.map((f) => ({ f, side: 1, atoms: parse(f) })));
    coef = species.map(() => 1);
    pops.length = 0;
    for (const s of species) { s.bump = new Spring(0, 300, 14); }
    const set = new Set(); species.forEach((s) => Object.keys(s.atoms).forEach((e) => set.add(e)));
    elements = [...set];
    solved = false; celebrate = 0;
    k.animate(true);
  }
  function counts(e) { let l = 0, r = 0; species.forEach((s, i) => { const n = (s.atoms[e] || 0) * coef[i]; if (s.side) r += n; else l += n; }); return [l, r]; }
  function massSide(side) { let m = 0; species.forEach((s, i) => { if (s.side !== side) return; for (const e in s.atoms) m += s.atoms[e] * MASS[e] * coef[i]; }); return m; }
  function setCoef(i, v) {
    v = clamp(v, 1, 12);
    if (v === coef[i]) return;
    coef[i] = v; species[i].bump.v = 6;
    const was = solved;
    solved = elements.every((e) => { const c = counts(e); return c[0] === c[1]; });
    if (solved && !was) { celebrate = 1; for (let n = 0; n < 40; n++) pops.push({ x: k.w / 2, y: k.h * 0.3, vx: (Math.random() - 0.5) * 420, vy: -Math.random() * 380 - 80, c: ['#2563eb', '#16a34a', '#f59e0b', '#db2777'][n % 4], life: 1.4 }); }
    k.animate(true);
  }
  function hint() {
    const bad = elements.filter((e) => { const c = counts(e); return c[0] !== c[1]; });
    if (!bad.length) { badge.set('Already balanced!'); return; }
    bad.sort((a, b) => (a === 'H' || a === 'O') - (b === 'H' || b === 'O') || species.filter((s) => s.atoms[a]).length - species.filter((s) => s.atoms[b]).length);
    const e = bad[0], c = counts(e);
    badge.set(`Hint: balance ${e} next — ${c[0]} on the left, ${c[1]} on the right`);
  }

  // layout of the equation row
  const slot = [];
  let rowY = 0, molY = 0, scaleY = 0, fsz = 28;
  k.onResize(() => k.invalidate());
  function layoutRow(ctx, w) {
    fsz = k.small ? 18 : 28;
    ctx.font = `700 ${fsz}px ${T.font}`;
    const parts = [];
    let total = 0;
    species.forEach((s, i) => {
      const fw = ctx.measureText(pretty(s.f)).width, cw = fsz * 0.9;
      parts.push({ i, cw, fw });
      total += cw + fw;
      const last = i === species.length - 1, next = species[i + 1];
      if (!last) total += next && next.side !== s.side ? fsz * 2.2 : fsz * 1.4;
    });
    let x = (w - total) / 2;
    slot.length = 0;
    species.forEach((s, i) => {
      const p = parts[i];
      slot.push({ cx: x + p.cw / 2, fx: x + p.cw + 2, fw: p.fw, w: p.cw + p.fw });
      x += p.cw + p.fw;
      const next = species[i + 1];
      if (next) { slot[i].sep = next.side !== s.side ? '→' : '+'; slot[i].sx = x + (next.side !== s.side ? fsz * 1.1 : fsz * 0.7); x += next.side !== s.side ? fsz * 2.2 : fsz * 1.4; }
    });
  }
  let dragI = -1, dragY0 = 0, dragC0 = 0;
  k.drag({
    hit: (x, y, s) => { for (let i = 0; i < slot.length; i++) if (Math.abs(x - slot[i].cx) < fsz * 0.6 + s && Math.abs(y - rowY) < fsz * 1.6 + s) return Math.abs(x - slot[i].cx); return false; },
    down: (x, y) => { dragI = -1; let bd = 1e9; slot.forEach((sl, i) => { const d = Math.abs(x - sl.cx); if (d < bd) { bd = d; dragI = i; } }); dragY0 = y; dragC0 = coef[dragI]; moved = false; },
    move: (x, y) => { if (dragI < 0) return; if (Math.abs(y - dragY0) > 6) moved = true; setCoef(dragI, dragC0 + Math.round((dragY0 - y) / 22)); },
    up: (x, y) => { if (dragI >= 0 && !moved) { if (y < rowY - fsz * 0.55) setCoef(dragI, coef[dragI] + 1); else if (y > rowY + fsz * 0.25) setCoef(dragI, coef[dragI] - 1); else setCoef(dragI, coef[dragI] + 1); } dragI = -1; },
    cursor: 'ns-resize',
  });
  let moved = false;

  k.frame((ctx, dt, w, h) => {
    background(k, ctx, w, h);
    layoutRow(ctx, w);
    rowY = k.small ? 70 : 96; molY = k.small ? 150 : 200; scaleY = k.small ? h - 70 : h - 90;
    let anim = false;
    // equation
    species.forEach((s, i) => {
      const sl = slot[i];
      if (s.bump.step(dt)) anim = true;
      const b = 1 + s.bump.x * 0.04;
      const hot = k.active && dragI === i;
      ctx.fillStyle = hot ? T.blueSoft : '#ffffff'; ctx.strokeStyle = T.blue; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.roundRect(sl.cx - fsz * 0.45, rowY - fsz * 0.85, fsz * 0.9, fsz * 1.2, 8); ctx.fill(); ctx.stroke();
      ctx.save(); ctx.translate(sl.cx, rowY - fsz * 0.25); ctx.scale(b, b);
      text(ctx, String(coef[i]), 0, 0, T.blue, fsz, 800, 'center', 'middle'); ctx.restore();
      ctx.fillStyle = T.blue; ctx.beginPath(); ctx.moveTo(sl.cx, rowY - fsz * 1.35); ctx.lineTo(sl.cx - 6, rowY - fsz * 1.05); ctx.lineTo(sl.cx + 6, rowY - fsz * 1.05); ctx.fill();
      ctx.beginPath(); ctx.moveTo(sl.cx, rowY + fsz * 0.85); ctx.lineTo(sl.cx - 6, rowY + fsz * 0.55); ctx.lineTo(sl.cx + 6, rowY + fsz * 0.55); ctx.fill();
      text(ctx, pretty(s.f), sl.fx, rowY, T.ink, fsz, 700, 'left', 'alphabetic');
      if (sl.sep) text(ctx, sl.sep, sl.sx, rowY, T.ink2, fsz, 600, 'center', 'alphabetic');
      // molecules
      const n = coef[i], mx = sl.cx + sl.w / 2 - fsz * 0.2;
      const per = k.small ? 3 : 4;
      for (let m = 0; m < Math.min(n, 12); m++) drawMolecule(ctx, s.atoms, mx + ((m % per) - (Math.min(n, per) - 1) / 2) * (k.small ? 28 : 50), molY + Math.floor(m / per) * (k.small ? 28 : 46), k.small ? 4.6 : 8.5);
    });
    // atom tally
    const tx = k.small ? 10 : 24, ty = k.small ? molY + 110 : molY + 160, rowH = k.small ? 18 : 22;
    const tw = Math.min(k.small ? w - 20 : 360, w - 40);
    card(ctx, tx, ty, tw, 30 + elements.length * rowH, 12);
    text(ctx, 'Atom count', tx + 12, ty + 19, T.ink, 11.5, 700); text(ctx, 'left', tx + tw * 0.55, ty + 19, T.ink2, 10, 700, 'center'); text(ctx, 'right', tx + tw * 0.78, ty + 19, T.ink2, 10, 700, 'center');
    let ok = 0;
    elements.forEach((e, j) => {
      const c = counts(e), yy = ty + 40 + j * rowH, good = c[0] === c[1];
      if (good) ok++;
      sphere(ctx, tx + 20, yy - 4, 6, COLOR[e] || '#999');
      text(ctx, e, tx + 34, yy, T.ink, 11, 700);
      text(ctx, String(c[0]), tx + tw * 0.55, yy, good ? T.green : T.red, 12, 700, 'center');
      text(ctx, String(c[1]), tx + tw * 0.78, yy, good ? T.green : T.red, 12, 700, 'center');
      text(ctx, good ? '✓' : '✗', tx + tw - 18, yy, good ? T.green : T.red, 13, 800, 'center');
    });
    // beam balance with the mass of each side
    const ml = massSide(0), mr = massSide(1);
    beam.to(clamp((mr - ml) / Math.max(ml, mr) * 0.5, -0.32, 0.32)); if (beam.step(dt)) anim = true;
    const bxc = k.small ? w / 2 : w * 0.7, L = k.small ? w * 0.36 : Math.min(240, w * 0.22), a = beam.x;
    if (!k.small || ty + 30 + elements.length * rowH < scaleY - 90) {
      ctx.fillStyle = '#64748b'; ctx.beginPath(); ctx.moveTo(bxc, scaleY - 70); ctx.lineTo(bxc - 18, scaleY + 6); ctx.lineTo(bxc + 18, scaleY + 6); ctx.fill();
      ctx.fillStyle = '#94a3b8'; ctx.fillRect(bxc - 60, scaleY + 6, 120, 8);
      const lx = bxc - Math.cos(a) * L, ly = scaleY - 70 - Math.sin(a) * L, rx = bxc + Math.cos(a) * L, ry = scaleY - 70 + Math.sin(a) * L;
      ctx.strokeStyle = '#475569'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(rx, ry); ctx.stroke();
      for (const [px, py, m, lab] of [[lx, ly, ml, 'reactants'], [rx, ry, mr, 'products']]) {
        ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px - 26, py + 34); ctx.moveTo(px, py); ctx.lineTo(px + 26, py + 34); ctx.stroke();
        ctx.fillStyle = '#cbd5e1'; ctx.beginPath(); ctx.ellipse(px, py + 36, 34, 6, 0, 0, Math.PI * 2); ctx.fill();
        pill(ctx, `${fmt(m, 1)} u`, px, py + 22, { size: 10.5, color: T.ink });
        text(ctx, lab, px, py + 58, T.ink2, 10, 600, 'center');
      }
    }
    // celebration
    for (let i = pops.length - 1; i >= 0; i--) { const p = pops[i]; p.vy += 600 * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt; if (p.life <= 0) { pops.splice(i, 1); continue; } ctx.fillStyle = withAlpha(p.c, Math.min(1, p.life)); ctx.fillRect(p.x, p.y, 5, 5); anim = true; }
    if (solved) pill(ctx, gcdAll() > 1 ? 'Balanced — but divide by ' + gcdAll() + ' for the simplest numbers' : 'Balanced!', w / 2, rowY + fsz * 1.5 + 6, { bg: T.green, color: '#fff', border: false, size: 12 });
    st.l.set(`${fmt(ml, 2)} u`); st.r.set(`${fmt(mr, 2)} u`); st.ok.set(`${ok} of ${elements.length}`); st.state.set(solved ? (gcdAll() > 1 ? 'not simplest' : 'balanced ✓') : 'unbalanced');
    if (!solved && badge.el.textContent.indexOf('Hint') !== 0) badge.set('Tap the arrows or drag a big number up and down');
    if (solved) badge.set('Same atoms on both sides, so the same mass: mass is conserved');
    k.animate(anim);
  });
  function gcdAll() { return coef.reduce((g, c) => gcd(g, c), 0); }
  function drawMolecule(ctx, atoms, x, y, r) {
    let n = 0; for (const e in atoms) n += atoms[e];
    let idx = 0;
    for (const e in atoms) for (let j = 0; j < atoms[e]; j++) {
      let ax = x, ay = y;
      if (idx > 0) { const ring = idx <= 6 ? 1 : 2, a = (idx - 1) * (Math.PI * 2 / Math.min(6, n - 1)) + (ring - 1) * 0.5; ax = x + Math.cos(a) * r * 1.5 * ring; ay = y + Math.sin(a) * r * 1.5 * ring; }
      sphere(ctx, ax, ay, r * (e === 'H' ? 0.75 : 1), COLOR[e] || '#999');
      idx++;
    }
  }

  load(0);
  k.debug = { set: (i, v) => setCoef(i, v), solved: () => solved, slot: (i) => [slot[i].cx, rowY - fsz * 1.2] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
