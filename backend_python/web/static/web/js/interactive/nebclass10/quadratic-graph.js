/**
 * Quadratic graph (NEB class 10) — y = ax² + bx + c on graph paper. Drag the vertex to move the
 * parabola, the shape handle (one unit right of the vertex) to change a, the y-intercept to change
 * c, or a root to slide the zeros: every drag rewrites a, b and c exactly. The vertex
 * (−b/2a, c − b²/4a), the axis of symmetry, the discriminant and the roots are computed live, with
 * a table of values plotted as points the way it is done on paper.
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, knob, withAlpha, card, dashed, DOTS } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const R = 10;

function num(v) { const r = Math.round(v * 100) / 100; return Number.isInteger(r) ? String(r) : r.toFixed(2).replace(/0$/, ''); }
function poly(a, b, c) {
  let s = (a === 1 ? '' : a === -1 ? '−' : sgn(a, true)) + 'x²';
  if (Math.abs(b) > 1e-9) s += (b < 0 ? ' − ' : ' + ') + (Math.abs(b) === 1 ? '' : num(Math.abs(b))) + 'x';
  if (Math.abs(c) > 1e-9) s += (c < 0 ? ' − ' : ' + ') + num(Math.abs(c));
  return 'y = ' + s;
}
function factor(r) { return Math.abs(r) < 1e-9 ? 'x' : `(x ${r > 0 ? '−' : '+'} ${num(Math.abs(r))})`; }
function sgn(v, first) { const s = num(Math.abs(v)); return v < 0 ? (first ? '−' : ' − ') + s : (first ? '' : ' + ') + s; }

export default function init(stage) {
  const k = createKit(stage, { label: 'A parabola on graph paper with draggable vertex, roots and intercept' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the vertex, a root or the shape handle', T.blue);

  let a = 1, b = -2, c = -3;
  const A = new Spring(a, 140, 20), B = new Spring(b, 140, 20), C = new Spring(c, 140, 20);
  const panel = createPanel(stage, { title: 'y = ax² + bx + c' });
  const aS = panel.slider({ label: 'a', min: -3, max: 3, step: 0.1, value: a, format: (v) => v.toFixed(1), onChange: (v) => { a = Math.abs(v) < 0.05 ? (v < 0 ? -0.1 : 0.1) : v; go(); } });
  const bS = panel.slider({ label: 'b', min: -10, max: 10, step: 0.5, value: b, format: (v) => v.toFixed(1), onChange: (v) => { b = v; go(); } });
  const cS = panel.slider({ label: 'c', min: -10, max: 10, step: 0.5, value: c, format: (v) => v.toFixed(1), onChange: (v) => { c = v; go(); } });
  panel.buttonRow([
    { label: 'Two roots', variant: 'ghost', onClick: () => set(1, -2, -3) },
    { label: 'One root', variant: 'ghost', onClick: () => set(1, -6, 9) },
    { label: 'No roots', variant: 'ghost', onClick: () => set(1, 0, 4) },
  ]);
  const st = panel.stats([{ key: 'v', label: 'Vertex' }, { key: 'axis', label: 'Axis of symmetry' }, { key: 'D', label: 'D = b² − 4ac' }, { key: 'roots', label: 'Roots' }]);
  const fact = panel.readout({ label: 'Factorised', value: '—' });
  panel.info('a > 0 opens upwards (a minimum), a < 0 downwards (a maximum); a bigger |a| is narrower. D > 0: two roots, D = 0: one repeated root (the vertex touches the x-axis), D < 0: no real roots.');

  function set(na, nb, nc) { a = na; b = nb; c = nc; sync(); go(); }
  function sync() { aS.set(Math.round(a * 10) / 10); bS.set(Math.round(b * 2) / 2); cS.set(Math.round(c * 2) / 2); }
  function go() { A.to(a); B.to(b); C.to(c); k.animate(true); }

  let ox = 0, oy = 0, u = 20;
  k.onResize((w, h) => { u = Math.max(12, Math.min((w - 20) / (2 * R + 1), (h - 20) / (2 * R + 1))); ox = w / 2; oy = h / 2; if (!k.small) ox = Math.max(w / 2, u * R + 200); });
  const X = (x) => ox + x * u, Y = (y) => oy - y * u;
  const vx = () => -b / (2 * a), vy = () => c - b * b / (4 * a);
  const snap = (v, s) => Math.round(v / s) * s;

  const vH = k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - X(vx()), y - Y(vy())); return d < 12 + s ? d : false; },
    move: (x, y) => { const h0 = clamp(snap((x - ox) / u, 0.5), -R, R), k0 = clamp(snap((oy - y) / u, 0.5), -R, R); b = -2 * a * h0; c = a * h0 * h0 + k0; sync(); go(); },
  });
  const shH = k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - X(vx() + 1), y - Y(vy() + a)); return d < 11 + s ? d : false; },
    move: (x, y) => { const h0 = vx(), k0 = vy(); let na = clamp(snap((oy - y) / u - k0, 0.1), -3, 3); if (Math.abs(na) < 0.1) na = na < 0 ? -0.1 : 0.1; a = na; b = -2 * a * h0; c = a * h0 * h0 + k0; sync(); go(); },
    cursor: 'ns-resize',
  });
  const cH = k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - X(0), y - Y(c)); return d < 11 + s ? d : false; },
    move: (x, y) => { c = clamp(snap((oy - y) / u, 0.5), -R, R); sync(); go(); },
    cursor: 'ns-resize',
  });
  const roots = () => { const D = b * b - 4 * a * c; if (D < -1e-9) return null; const s = Math.sqrt(Math.max(0, D)); return [(-b - s) / (2 * a), (-b + s) / (2 * a)]; };
  const rootH = [0, 1].map((ri) => k.drag({
    enabled: () => roots() !== null,
    hit: (x, y, s) => { const r = roots(); if (!r) return false; const d = Math.hypot(x - X(r[ri]), y - Y(0)); return d < 11 + s ? d + 0.5 : false; },
    move: (x) => { const r = roots(); if (!r) return; const other = r[1 - ri]; const nr = clamp(snap((x - ox) / u, 0.5), -R, R); b = -a * (nr + other); c = a * nr * other; sync(); go(); },
    cursor: 'ew-resize',
  }));

  k.frame((ctx, dt, w, h) => {
    let anim = A.step(dt) | B.step(dt) | C.step(dt);
    const a1 = A.x, b1 = B.x, c1 = C.x;
    background(k, ctx, w, h, '#fbfdff', '#f3f7fd');
    // graph paper
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(37,99,235,0.08)'; ctx.beginPath();
    for (let i = -R; i <= R; i++) { ctx.moveTo(X(i) + 0.5, Y(R)); ctx.lineTo(X(i) + 0.5, Y(-R)); ctx.moveTo(X(-R), Y(i) + 0.5); ctx.lineTo(X(R), Y(i) + 0.5); }
    ctx.stroke();
    ctx.strokeStyle = 'rgba(37,99,235,0.18)'; ctx.beginPath();
    for (let i = -R; i <= R; i += 5) { ctx.moveTo(X(i) + 0.5, Y(R)); ctx.lineTo(X(i) + 0.5, Y(-R)); ctx.moveTo(X(-R), Y(i) + 0.5); ctx.lineTo(X(R), Y(i) + 0.5); }
    ctx.stroke();
    ctx.strokeStyle = T.ink2; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(X(-R), Y(0)); ctx.lineTo(X(R), Y(0)); ctx.moveTo(X(0), Y(R)); ctx.lineTo(X(0), Y(-R)); ctx.stroke();
    for (let i = -R; i <= R; i += 2) if (i) { text(ctx, String(i), X(i), Y(0) + 13, T.mute, 9, 500, 'center'); text(ctx, String(i), X(0) - 5, Y(i) + 3, T.mute, 9, 500, 'right'); }
    text(ctx, 'x', X(R) - 4, Y(0) - 6, T.ink2, 12, 700, 'right'); text(ctx, 'y', X(0) + 6, Y(R) + 12, T.ink2, 12, 700);
    // axis of symmetry
    const hv = -b1 / (2 * a1), kv = c1 - b1 * b1 / (4 * a1);
    dashed(ctx, X(hv), Y(R), X(hv), Y(-R), withAlpha(T.purple, 0.6), 1.3);
    // curve
    ctx.save(); ctx.beginPath(); ctx.rect(X(-R), Y(R), 2 * R * u, 2 * R * u); ctx.clip();
    ctx.strokeStyle = T.blue; ctx.lineWidth = 3; ctx.beginPath();
    for (let i = 0; i <= 240; i++) { const x = -R + 2 * R * i / 240, y = a1 * x * x + b1 * x + c1; if (i) ctx.lineTo(X(x), Y(y)); else ctx.moveTo(X(x), Y(y)); }
    ctx.stroke();
    // table-of-values dots
    for (let x = Math.ceil(hv - 3); x <= Math.floor(hv + 3); x++) { const y = a * x * x + b * x + c; if (Math.abs(y) <= R) { ctx.beginPath(); ctx.arc(X(x), Y(y), 3, 0, Math.PI * 2); ctx.fillStyle = T.orange; ctx.fill(); } }
    ctx.restore();
    // handles
    const D = b * b - 4 * a * c, r = roots();
    if (r) for (let i = 0; i < (D < 1e-9 ? 1 : 2); i++) { knob(ctx, X(r[i]), Y(0), 7, T.green, k.isHot(rootH[i]) ? 1 : 0); if (!k.small || i === 0) pill(ctx, `x = ${num(r[i])}`, X(r[i]), Y(0) + (a > 0 ? 22 : -22), { color: T.green, size: 10 }); }
    knob(ctx, X(0), Y(c1), 6, T.teal, k.isHot(cH) ? 1 : 0);
    if (!k.small) text(ctx, `(0, ${num(c)})`, X(0) + 10, Y(c1) - 8, T.teal, 10, 700);
    knob(ctx, X(hv + 1), Y(kv + a1), 6, T.orange, k.isHot(shH) ? 1 : 0);
    knob(ctx, X(hv), Y(kv), 8, T.purple, k.isHot(vH) ? 1 : 0);
    pill(ctx, `vertex (${num(vx())}, ${num(vy())})`, X(hv), Y(kv) + (a > 0 ? 26 : -26), { color: T.purple, size: 10.5 });
    // equation and table card
    if (!k.small) {
      const cx = 14, cy = 50, cw = Math.min(240, ox - u * R - 28);
      if (cw > 150) {
        card(ctx, cx, cy, cw, 196, 12);
        text(ctx, poly(a, b, c), cx + 12, cy + 26, T.ink, 13, 700);
        text(ctx, 'Table of values', cx + 12, cy + 52, T.ink2, 10.5, 700);
        let row = 0;
        for (let x = Math.ceil(vx() - 3); x <= Math.floor(vx() + 3) && row < 7; x++, row++) {
          const y = a * x * x + b * x + c;
          text(ctx, `x = ${x}`, cx + 14, cy + 72 + row * 17, T.ink2, 10.5, 500);
          text(ctx, `y = ${num(y)}`, cx + cw - 14, cy + 72 + row * 17, T.orange, 10.5, 700, 'right');
        }
      }
    }
    st.v.set(`(${num(vx())}, ${num(vy())}) ${a > 0 ? 'min' : 'max'}`);
    st.axis.set(`x = ${num(vx())}`);
    st.D.set(`${num(D)} ${D > 1e-9 ? '> 0' : D < -1e-9 ? '< 0' : '= 0'}`);
    st.roots.set(r ? (D < 1e-9 ? `x = ${num(r[0])} (twice)` : `${num(r[0])}, ${num(r[1])}`) : 'none (real)');
    fact.set(r ? `${a === 1 ? '' : a === -1 ? '−' : num(a)}${D < 1e-9 ? factor(r[0]) + '²' : factor(r[0]) + factor(r[1])}` : 'does not factorise over the reals');
    badge.set(k.active ? poly(a, b, c) : D > 1e-9 ? 'Two real roots: the curve crosses the x-axis twice' : D < -1e-9 ? 'No real roots: the curve never meets the x-axis' : 'One repeated root: the vertex touches the x-axis');
    k.animate(!!anim);
  });

  go();
  k.debug = { vertex: () => [X(vx()), Y(vy())], root: (i) => { const r = roots(); return r ? [X(r[i]), Y(0)] : null; }, coef: () => [a, b, c] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
