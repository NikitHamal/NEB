/**
 * matter2d — heating curves and the particle model, shared by the melting and states-of-matter
 * labs. Heat is bookkept as energy: below the melting point it raises T by Q/(m·c); at the
 * melting or boiling point it goes into the latent heat (L) and the thermometer pauses until the
 * change is complete. The particle box follows the same state: particles bound to a lattice
 * jiggle with an amplitude that grows with temperature, liquid particles cling together and
 * flow, gas particles fly freely, and the solid melts from its surface first.
 */
import { T as TH, clamp, withAlpha, sphere, text } from './kit2d.js';

export function createThermal(sub, mass) {
  const s = { sub, m: mass, T: sub.start ?? (sub.mp - 15), fm: 0, fb: 0 };
  s.fm = s.T > sub.mp ? 1 : 0; s.fb = sub.bp !== undefined && s.T > sub.bp ? 1 : 0;
  s.add = (Q) => {
    const S = s.sub;
    let q = Q;
    for (let guard = 0; guard < 6 && Math.abs(q) > 1e-9; guard++) {
      if (q > 0) {
        if (s.fm < 1 && s.T >= S.mp - 1e-9) { const need = (1 - s.fm) * s.m * S.Lf; const use = Math.min(q, need); s.fm += use / (s.m * S.Lf); q -= use; s.T = S.mp; if (s.fm > 1 - 1e-9) s.fm = 1; continue; }
        if (S.bp !== undefined && s.fm >= 1 && s.fb < 1 && s.T >= S.bp - 1e-9) { const need = (1 - s.fb) * s.m * S.Lv; const use = Math.min(q, need); s.fb += use / (s.m * S.Lv); q -= use; s.T = S.bp; if (s.fb > 1 - 1e-9) s.fb = 1; continue; }
        const c = s.fm < 1 ? S.cS : s.fb >= 1 ? S.cG : S.cL;
        const next = s.fm < 1 ? S.mp : S.bp !== undefined && s.fb < 1 ? S.bp : Infinity;
        const dT = q / (s.m * c);
        if (s.T + dT > next) { q -= (next - s.T) * s.m * c; s.T = next; } else { s.T += dT; q = 0; }
      } else {
        if (S.bp !== undefined && s.fb > 0 && s.T <= S.bp + 1e-9) { const have = s.fb * s.m * S.Lv; const use = Math.min(-q, have); s.fb -= use / (s.m * S.Lv); q += use; s.T = S.bp; if (s.fb < 1e-9) s.fb = 0; continue; }
        if (s.fm > 0 && s.fb <= 0 && s.T <= S.mp + 1e-9) { const have = s.fm * s.m * S.Lf; const use = Math.min(-q, have); s.fm -= use / (s.m * S.Lf); q += use; s.T = S.mp; if (s.fm < 1e-9) s.fm = 0; continue; }
        const c = s.fm < 1 ? S.cS : s.fb >= 1 ? S.cG : S.cL;
        const next = s.fb >= 1 && S.bp !== undefined ? S.bp : s.fm > 0 ? S.mp : -Infinity;
        const dT = q / (s.m * c);
        if (s.T + dT < next) { q += (s.T - next) * s.m * c; s.T = next; } else { s.T += dT; q = 0; }
      }
    }
    s.T = Math.max(-273.15, s.T);
  };
  s.phase = () => (s.fb >= 1 ? 'Gas' : s.fb > 0 ? 'Boiling (liquid + gas)' : s.fm >= 1 ? 'Liquid' : s.fm > 0 ? 'Melting (solid + liquid)' : 'Solid');
  return s;
}

export function createParticles(n) {
  const p = {
    n, x: new Float32Array(n), y: new Float32Array(n), vx: new Float32Array(n), vy: new Float32Array(n),
    sx: new Float32Array(n), sy: new Float32Array(n), st: new Uint8Array(n), site: new Int16Array(n),
    box: { x: 0, y: 0, w: 100, h: 100 }, d: 12, cols: 1,
  };
  function sites() {
    const b = p.box, d = p.d;
    p.cols = Math.max(4, Math.floor((b.w * 0.9) / d));
    const x0 = b.x + (b.w - (p.cols - 1) * d) / 2;
    for (let i = 0; i < n; i++) {
      const r = Math.floor(i / p.cols), c = i % p.cols;
      p.sx[i] = x0 + c * d + (r & 1 ? d / 2 : 0);
      p.sy[i] = b.y + b.h - d * 0.6 - r * d * 0.87;
    }
  }
  p.layout = (x, y, w, h, d) => { p.box.x = x; p.box.y = y; p.box.w = w; p.box.h = h; p.d = d; sites(); for (let i = 0; i < n; i++) if (p.st[i] === 0) { p.x[i] = p.sx[i]; p.y[i] = p.sy[i]; } };
  p.reset = (fm, fb) => {
    for (let i = 0; i < n; i++) { p.st[i] = 0; p.x[i] = p.sx[i]; p.y[i] = p.sy[i]; p.vx[i] = p.vy[i] = 0; }
    p.sync(fm, fb, 1);
  };
  /** Bring the particle states in line with the melted and boiled fractions. */
  p.sync = (fm, fb, kT) => {
    const wantSolid = Math.round((1 - fm) * n), wantGas = Math.round(fb * n);
    let solid = 0, gas = 0;
    for (let i = 0; i < n; i++) { if (p.st[i] === 0) solid++; else if (p.st[i] === 2) gas++; }
    while (solid > wantSolid) { let best = -1; for (let i = 0; i < n; i++) if (p.st[i] === 0 && (best < 0 || p.sy[i] < p.sy[best] || (p.sy[i] === p.sy[best] && Math.abs(p.sx[i] - p.box.x - p.box.w / 2) > Math.abs(p.sx[best] - p.box.x - p.box.w / 2)))) best = i; if (best < 0) break; p.st[best] = 1; solid--; }
    while (solid < wantSolid) { let best = -1; for (let i = 0; i < n; i++) if (p.st[i] === 1 && (best < 0 || p.sy[i] > p.sy[best])) best = i; if (best < 0) { for (let i = 0; i < n; i++) if (p.st[i] === 2) { best = i; break; } } if (best < 0) break; if (p.st[best] === 2) gas--; p.st[best] = 0; solid++; }
    while (gas < wantGas) { let best = -1; for (let i = 0; i < n; i++) if (p.st[i] === 1 && (best < 0 || p.y[i] < p.y[best])) best = i; if (best < 0) break; p.st[best] = 2; p.vy[best] = -Math.sqrt(kT) * 160; gas++; }
    while (gas > wantGas) { let best = -1; for (let i = 0; i < n; i++) if (p.st[i] === 2) { best = i; break; } if (best < 0) break; p.st[best] = 1; gas--; }
  };
  /** kT: a 0..1+ motion scale for the temperature. */
  p.step = (dt, kT) => {
    const b = p.box, d = p.d, h = Math.min(dt, 1 / 60) / 2;
    const vth = 30 + 260 * Math.sqrt(Math.max(0, kT));
    for (let sub = 0; sub < 2; sub++) {
      for (let i = 0; i < n; i++) {
        if (p.st[i] === 0) {
          const amp = d * (0.04 + 0.16 * Math.min(1.2, kT));
          p.vx[i] += (-(p.x[i] - p.sx[i]) * 900 + (Math.random() - 0.5) * vth * 40) * h;
          p.vy[i] += (-(p.y[i] - p.sy[i]) * 900 + (Math.random() - 0.5) * vth * 40) * h;
          p.vx[i] *= 0.9; p.vy[i] *= 0.9;
          p.x[i] += p.vx[i] * h; p.y[i] += p.vy[i] * h;
          const dx = p.x[i] - p.sx[i], dy = p.y[i] - p.sy[i], r = Math.hypot(dx, dy);
          if (r > amp) { p.x[i] = p.sx[i] + dx / r * amp; p.y[i] = p.sy[i] + dy / r * amp; }
        } else if (p.st[i] === 1) {
          p.vy[i] += 500 * h;
          p.vx[i] += (Math.random() - 0.5) * vth * 30 * h; p.vy[i] += (Math.random() - 0.5) * vth * 30 * h;
          const sp = Math.hypot(p.vx[i], p.vy[i]), cap = vth * 0.9;
          if (sp > cap) { p.vx[i] *= cap / sp; p.vy[i] *= cap / sp; }
        } else {
          const sp = Math.hypot(p.vx[i], p.vy[i]) || 1;
          const tgt = vth * 1.6;
          p.vx[i] += (p.vx[i] / sp) * (tgt - sp) * 2 * h; p.vy[i] += (p.vy[i] / sp) * (tgt - sp) * 2 * h + 40 * h;
        }
      }
      for (let i = 0; i < n; i++) {
        if (p.st[i] === 0) continue;
        for (let j = 0; j < n; j++) {
          if (j === i) continue;
          const dx = p.x[i] - p.x[j], dy = p.y[i] - p.y[j];
          const r2 = dx * dx + dy * dy;
          if (r2 > d * d * 2.6 || r2 < 1e-6) continue;
          const r = Math.sqrt(r2);
          if (r < d) { const f = (d - r) / r * 0.5; p.x[i] += dx * f; p.y[i] += dy * f; if (p.st[j] !== 0) { p.x[j] -= dx * f; p.y[j] -= dy * f; } const vn = ((p.vx[i] - p.vx[j]) * dx + (p.vy[i] - p.vy[j]) * dy) / r2; if (vn < 0) { p.vx[i] -= vn * dx; p.vy[i] -= vn * dy; } }
          else if (p.st[i] === 1 && p.st[j] !== 2) { const f = -260 * h / r; p.vx[i] += dx * f; p.vy[i] += dy * f; }
        }
        p.vx[i] *= p.st[i] === 1 ? 0.985 : 1; p.vy[i] *= p.st[i] === 1 ? 0.985 : 1;
        p.x[i] += p.vx[i] * h; p.y[i] += p.vy[i] * h;
        const r0 = d / 2;
        if (p.x[i] < b.x + r0) { p.x[i] = b.x + r0; p.vx[i] = Math.abs(p.vx[i]); }
        if (p.x[i] > b.x + b.w - r0) { p.x[i] = b.x + b.w - r0; p.vx[i] = -Math.abs(p.vx[i]); }
        if (p.y[i] < b.y + r0) { p.y[i] = b.y + r0; p.vy[i] = Math.abs(p.vy[i]); }
        if (p.y[i] > b.y + b.h - r0) { p.y[i] = b.y + b.h - r0; p.vy[i] = -Math.abs(p.vy[i]) * (p.st[i] === 2 ? 1 : 0.3); }
      }
    }
  };
  p.draw = (ctx, colors) => {
    const d = p.d;
    ctx.strokeStyle = withAlpha(colors[0], 0.5); ctx.lineWidth = 1.2; ctx.beginPath();
    for (let i = 0; i < n; i++) {
      if (p.st[i] !== 0) continue;
      for (let j = i + 1; j < n; j++) { if (p.st[j] !== 0) continue; const dx = p.sx[i] - p.sx[j], dy = p.sy[i] - p.sy[j]; if (dx * dx + dy * dy < d * d * 1.1) { ctx.moveTo(p.x[i], p.y[i]); ctx.lineTo(p.x[j], p.y[j]); } }
    }
    ctx.stroke();
    for (let i = 0; i < n; i++) sphere(ctx, p.x[i], p.y[i], d * 0.42, colors[p.st[i]]);
  };
  return p;
}

/** A thermometer: bulb at (x, y), tube up to y - h, range lo..hi °C. */
export function thermometer(ctx, x, y, h, T, lo, hi, opt) {
  const f = clamp((T - lo) / (hi - lo), 0, 1);
  ctx.fillStyle = '#fff'; ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.roundRect(x - 7, y - h - 8, 14, h + 8, 7); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.arc(x, y + 6, 11, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#e5484d'; ctx.beginPath(); ctx.arc(x, y + 6, 8, 0, Math.PI * 2); ctx.fill();
  ctx.fillRect(x - 3, y - f * h, 6, f * h + 6);
  const span = hi - lo, step = span > 400 ? 500 : span > 150 ? 50 : span > 60 ? 20 : 10;
  ctx.strokeStyle = '#64748b'; ctx.lineWidth = 1; ctx.beginPath();
  for (let v = Math.ceil(lo / step) * step; v <= hi; v += step) { const yy = y - (v - lo) / span * h; ctx.moveTo(x + 7, yy); ctx.lineTo(x + 12, yy); }
  ctx.stroke();
  for (let v = Math.ceil(lo / step) * step; v <= hi; v += step) text(ctx, `${v}`, x + 15, y - (v - lo) / span * h + 3.5, TH.ink2, 9, 600);
  if (opt && opt.marks) for (const m of opt.marks) { const yy = y - (m.T - lo) / span * h; if (yy < y - h || yy > y) continue; ctx.strokeStyle = m.color; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x - 12, yy); ctx.lineTo(x - 7, yy); ctx.stroke(); text(ctx, m.label, x - 15, yy + 3.5, m.color, 9, 700, 'right'); }
}

/** A drag-to-turn heat/cool dial. Returns { draw(ctx, x, y, r, v, hot) }; v in −1..1. */
export function drawHeatDial(ctx, x, y, r, v, hot) {
  ctx.beginPath(); ctx.arc(x, y + 2, r, 0, Math.PI * 2); ctx.fillStyle = 'rgba(23,40,80,0.15)'; ctx.fill();
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = hot ? TH.blue : '#cbd5e1'; ctx.lineWidth = 2; ctx.stroke();
  ctx.lineWidth = 6; ctx.lineCap = 'round';
  ctx.strokeStyle = 'rgba(59,130,246,0.35)'; ctx.beginPath(); ctx.arc(x, y, r - 8, Math.PI * 0.75, Math.PI * 1.5); ctx.stroke();
  ctx.strokeStyle = 'rgba(239,68,68,0.35)'; ctx.beginPath(); ctx.arc(x, y, r - 8, Math.PI * 1.5, Math.PI * 2.25); ctx.stroke();
  const a = Math.PI * 1.5 + v * Math.PI * 0.75;
  ctx.strokeStyle = v > 0.02 ? '#ef4444' : v < -0.02 ? '#3b82f6' : '#94a3b8';
  ctx.beginPath(); ctx.arc(x, y, r - 8, Math.PI * 1.5, a, v < 0); ctx.stroke();
  ctx.lineWidth = 3; ctx.strokeStyle = '#334155'; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a) * (r - 14), y + Math.sin(a) * (r - 14)); ctx.stroke();
  ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI * 2); ctx.fillStyle = '#334155'; ctx.fill();
  text(ctx, 'cool', x - r + 2, y + r + 14, '#3b82f6', 10, 700, 'center');
  text(ctx, 'heat', x + r - 2, y + r + 14, '#ef4444', 10, 700, 'center');
}
export function dialValue(x, y, cx, cy) {
  let a = Math.atan2(y - cy, x - cx) - Math.PI * 1.5;
  while (a < -Math.PI) a += Math.PI * 2;
  while (a > Math.PI) a -= Math.PI * 2;
  return clamp(a / (Math.PI * 0.75), -1, 1);
}
