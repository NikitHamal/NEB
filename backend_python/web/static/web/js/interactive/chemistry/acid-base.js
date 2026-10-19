/**
 * Acid–base titration — 25.0 mL of 0.100 M acid (hydrochloric or ethanoic) in a conical flask
 * with an indicator, and 0.100 M NaOH in a 50 mL burette. Turn the tap by dragging it (the flow
 * follows how far it is open) or tap it for single drops; swirl the flask by dragging it. Every
 * drop changes the pH, which is solved from the charge balance, so the curve, the equivalence
 * point (and for ethanoic acid the buffer region and pH 8.7 end point) are real.
 */
import { createKit, T, Spring, Ring, fmt, clamp, background, text, pill, withAlpha, softShadow, card } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { Pool } from '../core/chem2d.js';
import { solvePH, INDICATORS, drawPHStrip } from '../core/indicators2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const V0 = 25, CA = 0.1, CB = 0.1, DROP = 0.05, KA = 1.8e-5;

export default function init(stage) {
  const k = createKit(stage, { label: 'A burette over a conical flask, a pH meter and a live titration curve' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the burette tap to open it', T.blue);

  let acid = 'hcl', ind = 'phenolphthalein', added = 0, tap = 0, plume = 0, swirl = 0, pending = 0;
  const drops = new Pool(30);
  const curve = new Ring(1200);
  const fx = new Spring(0, 160, 12);
  const tapHot = new Spring(0, 260, 26);
  const plot = new Plot({ title: 'pH against volume of NaOH', xLabel: 'V(NaOH) / mL', yLabel: 'pH', xMin: 0, xMax: 50, yMin: 0, yMax: 14 });
  let dropTimer = 0, lastPH = 1;

  const panel = createPanel(stage, { title: 'Titration' });
  panel.chips({ label: 'Acid in the flask (0.100 M, 25.0 mL)', options: [{ value: 'hcl', label: 'Hydrochloric (strong)' }, { value: 'eth', label: 'Ethanoic (weak)' }], value: 'hcl', onChange: (v) => { acid = v; reset(); } });
  panel.chips({ label: 'Indicator', options: Object.keys(INDICATORS).map((key) => ({ value: key, label: INDICATORS[key].label })), value: ind, onChange: (v) => { ind = v; k.invalidate(); } });
  panel.buttonRow([{ label: 'One drop', icon: 'water_drop', onClick: () => { pending += DROP; spawnDrop(); k.animate(true); } }, { label: 'Restart', icon: 'replay', variant: 'ghost', onClick: reset }]);
  const st = panel.stats([{ key: 'v', label: 'NaOH added' }, { key: 'pH', label: 'pH (meter)' }, { key: 'eq', label: 'Equivalence' }, { key: 'conc', label: 'Acid conc. from your titre' }]);
  panel.info('NaOH + HCl → NaCl + H₂O. Near the end point one drop changes the pH by several units, so slow to single drops when the colour starts to linger. Phenolphthalein suits both acids; methyl orange changes too early for ethanoic acid.');

  function reset() { added = 0; tap = 0; plume = 0; pending = 0; drops.clear(); curve.clear(); curve.push(0, pH()); k.animate(true); }
  function pH(extra = 0) {
    const v = added + extra, Vt = (V0 + v) / 1000;
    const nb = CB * v / 1000, na = CA * V0 / 1000;
    return acid === 'hcl' ? solvePH(na / Vt, nb / Vt) : solvePH(0, nb / Vt, na / Vt, KA);
  }

  let bx = 0, btop = 0, bbot = 0, fy = 0, fw = 0, fh = 0, scale = 1;
  k.onResize((w, h) => {
    if (k.small) { bx = w * 0.3; btop = 30; bbot = h * 0.4; fy = h * 0.66; fw = 110; fh = 96; plot.box(w * 0.54, 30, w * 0.44, h * 0.36); }
    else { bx = w * 0.26; btop = 30; bbot = h * 0.5; fy = h * 0.8; fw = 150; fh = 130; plot.box(w * 0.48, 30, w * 0.5, h * 0.56); }
    scale = (bbot - btop - 40) / 50;
    fx.set(bx);
  });
  const tapY = () => bbot + 16;
  const tapH = k.drag({
    hit: (x, y, s) => { const d = Math.hypot(x - bx, y - tapY()); return d < 18 + s ? d : false; },
    down: (x) => { tapH._x0 = x; tapH._t0 = tap; tapH._moved = false; },
    move: (x) => { if (Math.abs(x - tapH._x0) > 4) tapH._moved = true; tap = clamp(tapH._t0 + (x - tapH._x0) / 60, 0, 1); k.animate(true); },
    up: () => { if (!tapH._moved) { if (tap > 0) tap = 0; else { pending += DROP; spawnDrop(); } } k.animate(true); },
    cursor: 'ew-resize',
  });
  k.drag({
    hit: (x, y, s) => (Math.abs(x - fx.x) < fw / 2 + s && y > fy - fh - 20 && y < fy + s ? 1 : false),
    down: (x) => { flaskGrab = x - fx.x; },
    move: (x) => { const nx = clamp(x - flaskGrab, bx - 40, bx + 40); swirl = Math.min(1, swirl + Math.abs(nx - fx.x) * 0.02); fx.set(nx); },
    up: () => { fx.to(bx); },
  });
  let flaskGrab = 0;
  function spawnDrop() { drops.add(bx, tapY() + 14, 0, 30, 3, 0, 0); }

  k.frame((ctx, dt, w, h) => {
    const flow = tap * tap * 1.2;
    if (tap > 0 && added + pending < 50) { dropTimer += dt; const per = DROP / Math.max(flow, 1e-3); while (dropTimer > per) { dropTimer -= per; pending += DROP; spawnDrop(); } }
    const surf = fy - fh * 0.32;
    for (let i = drops.n - 1; i >= 0; i--) {
      drops.vy[i] += 900 * dt; drops.y[i] += drops.vy[i] * dt;
      if (drops.y[i] > surf) { added = Math.min(50, added + DROP); pending = Math.max(0, pending - DROP); plume = Math.min(1.5, plume + 0.25); drops.kill(i); curve.push(added, pH()); }
    }
    swirl *= Math.exp(-dt * 1.5);
    plume *= Math.exp(-dt * (0.25 + 6 * swirl));
    fx.step(dt); tapHot.to(k.isHot(tapH) ? 1 : 0); tapHot.step(dt);
    const p = pH();
    lastPH = p;
    background(k, ctx, w, h);
    // stand
    ctx.fillStyle = '#64748b'; ctx.fillRect(bx - 80, 14, 6, fy - 2); ctx.fillRect(bx - 110, fy + 2, 120, 8);
    ctx.fillStyle = '#94a3b8'; ctx.fillRect(bx - 80, bbot - 60, 74, 6);
    // burette
    const bw = 18, top = btop + 10;
    ctx.fillStyle = 'rgba(214,230,248,0.5)'; ctx.fillRect(bx - bw / 2, top, bw, bbot - top);
    const lvl = top + 20 + (added + pending) * scale;
    ctx.fillStyle = 'rgba(200,220,245,0.85)'; ctx.fillRect(bx - bw / 2 + 2, lvl, bw - 4, bbot - lvl);
    ctx.strokeStyle = 'rgba(70,100,140,0.8)'; ctx.lineWidth = 1.5; ctx.strokeRect(bx - bw / 2, top, bw, bbot - top);
    ctx.strokeStyle = 'rgba(40,60,90,0.7)'; ctx.lineWidth = 1; ctx.beginPath();
    for (let ml = 0; ml <= 50; ml++) { const yy = top + 20 + ml * scale; const l = ml % 5 === 0 ? 8 : 4; ctx.moveTo(bx - bw / 2, yy); ctx.lineTo(bx - bw / 2 + l, yy); }
    ctx.stroke();
    for (let ml = 0; ml <= 50; ml += 10) text(ctx, String(ml), bx - bw / 2 - 4, top + 23 + ml * scale, T.ink2, 9, 600, 'right');
    ctx.strokeStyle = '#1e3a8a'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(bx - bw / 2 + 2, lvl - 1); ctx.quadraticCurveTo(bx, lvl + 3, bx + bw / 2 - 2, lvl - 1); ctx.stroke();
    pill(ctx, `${fmt(added + pending, 2)} mL`, bx + bw / 2 + 40, lvl, { size: 10, color: T.blue });
    text(ctx, '0.100 M NaOH', bx + bw / 2 + 6, top + 6, T.ink2, 10, 600);
    // tap and jet
    ctx.fillStyle = 'rgba(214,230,248,0.8)'; ctx.fillRect(bx - 3, bbot, 6, 34);
    ctx.save(); ctx.translate(bx, tapY()); ctx.rotate(tap * Math.PI / 2);
    if (tapHot.x > 0.02) { ctx.fillStyle = withAlpha(T.blue, 0.15 * tapHot.x); ctx.beginPath(); ctx.arc(0, 0, 20, 0, Math.PI * 2); ctx.fill(); }
    ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.roundRect(-16, -4, 32, 8, 3); ctx.fill(); ctx.restore();
    ctx.beginPath(); ctx.arc(bx, tapY(), 6, 0, Math.PI * 2); ctx.fillStyle = '#475569'; ctx.fill();
    text(ctx, tap > 0 ? `tap open ${Math.round(tap * 100)} %` : (k.small ? 'drag tap ↔' : 'drag the tap ↔ (tap for one drop)'), bx + 24, tapY() + 4, tap > 0 ? T.green : T.blue, 10, 600);
    if (flow > 0.6) { ctx.strokeStyle = 'rgba(200,220,245,0.9)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx, tapY() + 16); ctx.lineTo(fx.x, surf); ctx.stroke(); }
    ctx.fillStyle = 'rgba(190,215,245,0.95)';
    for (let i = 0; i < drops.n; i++) { ctx.beginPath(); ctx.ellipse(drops.x[i], drops.y[i], 2.6, 3.4, 0, 0, Math.PI * 2); ctx.fill(); }
    // flask
    const X = fx.x, neck = 26;
    softShadow(ctx, X, fy + 2, fw * 0.6, 6, 0.22);
    const I = INDICATORS[ind];
    const bulk = I.color(p), alpha = I.alpha(p);
    ctx.save(); flask(ctx, X, fy, fw, fh, neck); ctx.clip();
    ctx.fillStyle = 'rgba(235,242,250,0.9)'; ctx.fillRect(X - fw, surf, fw * 2, fh);
    ctx.fillStyle = withAlpha(bulk, alpha); ctx.fillRect(X - fw, surf, fw * 2, fh);
    if (plume > 0.03) {
      const pl = pH(Math.min(2, plume * 1.2)) ;
      const pc = I.color(pl), pa = I.alpha(pl) * Math.min(1, plume);
      if (pa > 0.02) { ctx.fillStyle = withAlpha(pc, pa); ctx.beginPath(); ctx.ellipse(X, surf + 16 + 10 * Math.sin(k.t * 3), 18 + 20 * (1 - plume / 1.5), 12, 0, 0, Math.PI * 2); ctx.fill(); }
    }
    ctx.restore();
    flask(ctx, X, fy, fw, fh, neck); ctx.strokeStyle = 'rgba(120,150,190,0.9)'; ctx.lineWidth = 2; ctx.stroke();
    text(ctx, acid === 'hcl' ? '25.0 mL 0.100 M HCl' : '25.0 mL 0.100 M CH₃COOH', X, fy + 24, T.ink2, 10, 600, 'center');
    if (!k.small) text(ctx, 'drag to swirl ↔', X + fw / 2 + 8, fy - 10, T.mute, 10, 600);
    // pH meter
    const mx = k.small ? w * 0.78 : X + fw / 2 + 120, my = k.small ? fy - 40 : fy - 100;
    card(ctx, mx - 50, my - 26, 100, 52, 10, '#1f2937', '#111827');
    ctx.fillStyle = '#a3e635'; ctx.font = `700 22px ${T.mono}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(fmt(p, 2), mx, my);
    text(ctx, 'pH meter', mx, my + 38, T.ink2, 10, 600, 'center');
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(mx - 50, my); ctx.quadraticCurveTo(X + 20, my - 30, X + 14, surf + 30); ctx.stroke();
    // graph
    plot.frame(ctx);
    plot.clip(ctx);
    const r = I.range; ctx.fillStyle = withAlpha(I.color((r[0] + r[1]) / 2), 0.14); ctx.fillRect(plot.ix, plot.Y(r[1]), plot.iw, plot.Y(r[0]) - plot.Y(r[1]));
    ctx.strokeStyle = withAlpha(T.slate, 0.5); ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(plot.X(25), plot.iy); ctx.lineTo(plot.X(25), plot.iy + plot.ih); ctx.stroke(); ctx.setLineDash([]);
    plot.ring(ctx, curve, T.blue, 2.2);
    plot.unclip(ctx);
    plot.dot(ctx, added, p, T.blue, 4);
    text(ctx, `${I.label} changes here`, plot.ix + 6, plot.Y(r[1]) - 4, T.ink2, 9.5, 600);
    // pH strip
    if (!k.small) drawPHStrip(ctx, plot.x + 10, plot.y + plot.h + 70, plot.w - 20, 14, p, true);
    const eqPH = pH(25 - added);
    st.v.set(`${fmt(added, 2)} mL`); st.pH.set(fmt(p, 2)); st.eq.set(`25.00 mL (pH ${fmt(eqPH, 1)})`);
    const endpoint = endPointHit(p);
    st.conc.set(endpoint ? `${fmt(CB * added / V0, 4)} M` : '—');
    badge.set(added >= 49.99 ? 'The burette is empty' : endpoint ? `End point! The colour stays: titre = ${fmt(added, 2)} mL` : tap > 0 ? `Adding NaOH… pH ${fmt(p, 2)}` : 'Drag the burette tap to open it, or tap it for one drop');
    k.animate(tap > 0 || drops.n > 0 || plume > 0.02 || fx.moving || tapHot.moving);
  });
  function endPointHit(p) {
    const r = INDICATORS[ind].range;
    if (ind === 'universal') return Math.abs(p - 7) < 0.5;
    return p >= r[0] + (r[1] - r[0]) * 0.3 && added > 0;
  }
  function flask(ctx, X, y, w, h, neck) {
    ctx.beginPath();
    ctx.moveTo(X - neck / 2, y - h - 30); ctx.lineTo(X - neck / 2, y - h); ctx.lineTo(X - w / 2, y - 12); ctx.quadraticCurveTo(X - w / 2, y, X - w / 2 + 12, y);
    ctx.lineTo(X + w / 2 - 12, y); ctx.quadraticCurveTo(X + w / 2, y, X + w / 2, y - 12); ctx.lineTo(X + neck / 2, y - h); ctx.lineTo(X + neck / 2, y - h - 30);
  }

  reset();
  k.debug = { tap: () => [bx, tapY()], add: (v) => { added = v; curve.push(added, pH()); k.invalidate(); }, state: () => ({ added, pH: lastPH }) };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
