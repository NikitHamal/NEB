/**
 * optics2d — a thin lens or spherical mirror on a principal axis, shared by the optics bench and
 * the class 10 concave mirror lab. Distances use the real-is-positive convention:
 * 1/f = 1/u + 1/v, m = −v/u (f > 0 converging, v < 0 virtual). Every ray is traced with the
 * paraxial transfer s' = s − y/f at the element plane, so the drawn rays meet exactly where the
 * formula puts the image. Drag the object's tip (distance and height), the focus F (focal length)
 * and, on a lens bench, the screen that catches a real image.
 */
import { T, Spring, fmt, clamp, text, pill, knob, withAlpha, DASH, NODASH } from './kit2d.js';

export const KINDS = {
  'convex-lens': { lens: true, sign: 1, label: 'Convex lens' },
  'concave-lens': { lens: true, sign: -1, label: 'Concave lens' },
  'concave-mirror': { lens: false, sign: 1, label: 'Concave mirror' },
  'convex-mirror': { lens: false, sign: -1, label: 'Convex mirror' },
};
const RAY_COLORS = ['#e5484d', '#2563eb', '#16a34a', '#a855f7'];

export function solve(kind, u, f, h, out) {
  const F = KINDS[kind].sign * f;
  out.F = F;
  if (Math.abs(u - F) < 0.05) { out.v = Infinity; out.m = Infinity; out.hi = Infinity; out.real = true; out.inf = true; return out; }
  out.inf = false;
  out.v = u * F / (u - F);
  out.m = -out.v / u;
  out.hi = out.m * h;
  out.real = out.v > 0;
  return out;
}

export function describe(r) {
  if (r.inf) return 'At infinity (no image)';
  const size = Math.abs(r.m) > 1.02 ? 'magnified' : Math.abs(r.m) < 0.98 ? 'diminished' : 'same size';
  return `${r.real ? 'Real' : 'Virtual'}, ${r.m < 0 ? 'inverted' : 'erect'}, ${size}`;
}

export function createOptics(k, opts = {}) {
  const s = {
    kind: opts.kind || 'convex-lens', f: opts.f || 20, u: opts.u || 50, h: opts.h || 8,
    mode: 'principal', screen: opts.screen ? 40 : null, span: opts.span || 100, regions: !!opts.regions,
    onChange: opts.onChange || null,
  };
  const r = { F: 0, v: 0, m: 0, hi: 0, real: true, inf: false };
  let ex = 0, ay = 0, sc = 4, left = 0, right = 0, top = 0, bottom = 0;
  const hot = { obj: new Spring(0, 260, 26), f: new Spring(0, 260, 26), scr: new Spring(0, 260, 26) };
  const fShow = new Spring(s.f, 140, 20), uShow = new Spring(s.u, 160, 22);

  function layout(x0, y0, w, h) {
    left = x0 + 10; right = x0 + w - 10; top = y0 + 10; bottom = y0 + h - 30;
    const lens = KINDS[s.kind].lens;
    ex = lens ? x0 + w * (k.small ? 0.56 : 0.52) : x0 + w * (k.small ? 0.74 : 0.7);
    ay = y0 + h * 0.52;
    sc = (ex - left - 16) / s.span;
  }
  const X = (cm) => ex + cm * sc;
  const changed = () => { if (s.onChange) s.onChange(); k.invalidate(); };

  const objH = k.drag({
    enabled: () => s.mode !== 'parallel',
    hit: (x, y, sl) => { const d = Math.hypot(x - X(-uShow.x), y - (ay - s.h * sc)); return d < 14 + sl ? d : false; },
    move: (x, y) => {
      s.u = clamp(Math.round((ex - x) / sc), 2, Math.round(s.span * 0.98));
      s.h = clamp(Math.round((ay - y) / sc), 2, Math.round((ay - top - 10) / sc));
      uShow.set(s.u); changed();
    },
  });
  const fKnob = () => X(KINDS[s.kind].lens || KINDS[s.kind].sign > 0 ? -fShow.x : fShow.x);
  const fH = k.drag({
    hit: (x, y, sl) => { const fx = fKnob(); const d = Math.hypot(x - fx, y - ay); return d < 12 + sl ? d : false; },
    move: (x) => { s.f = clamp(Math.round(Math.abs(ex - x) / sc), 5, Math.round(s.span * 0.45)); fShow.set(s.f); changed(); },
    cursor: 'ew-resize',
  });
  const scrH = k.drag({
    enabled: () => s.screen !== null && KINDS[s.kind].lens,
    hit: (x, y, sl) => (Math.abs(x - X(s.screen)) < 10 + sl && y > ay - 120 && y < ay + 120 ? Math.abs(x - X(s.screen)) : false),
    move: (x) => { s.screen = clamp(Math.round((x - ex) / sc), 2, Math.round((right - ex) / sc)); changed(); },
    cursor: 'ew-resize',
  });

  function physX(cmUnfolded) { return KINDS[s.kind].lens ? X(cmUnfolded) : X(-cmUnfolded); }

  function rayOut(ctx, yHit, sIn, color, virtualImage) {
    const kd = KINDS[s.kind];
    const sOut = sIn - yHit / r.F;
    const xEnd = kd.lens ? (right - ex) / sc : (ex - left) / sc;
    const yEnd = yHit + sOut * xEnd;
    ctx.strokeStyle = color; ctx.lineWidth = 1.8;
    ctx.beginPath(); ctx.moveTo(ex, ay - yHit * sc); ctx.lineTo(physX(xEnd), ay - yEnd * sc); ctx.stroke();
    arrowMid(ctx, ex, ay - yHit * sc, physX(xEnd), ay - yEnd * sc, color);
    if (virtualImage) {
      const xb = kd.lens ? -(ex - left) / sc : -(right - ex) / sc;
      ctx.setLineDash(DASH); ctx.strokeStyle = withAlpha(color, 0.6); ctx.lineWidth = 1.3;
      ctx.beginPath(); ctx.moveTo(ex, ay - yHit * sc); ctx.lineTo(physX(xb), ay - (yHit + sOut * xb) * sc); ctx.stroke(); ctx.setLineDash(NODASH);
    }
  }
  function arrowMid(ctx, x0, y0, x1, y1, color) {
    const mx = x0 + (x1 - x0) * 0.35, my = y0 + (y1 - y0) * 0.35, a = Math.atan2(y1 - y0, x1 - x0);
    ctx.fillStyle = color; ctx.beginPath();
    ctx.moveTo(mx + Math.cos(a) * 6, my + Math.sin(a) * 6); ctx.lineTo(mx + Math.cos(a + 2.6) * 6, my + Math.sin(a + 2.6) * 6); ctx.lineTo(mx + Math.cos(a - 2.6) * 6, my + Math.sin(a - 2.6) * 6); ctx.fill();
  }
  function rayIn(ctx, yHit, color, viaX) {
    const ox = X(-uShow.x), oy = ay - s.h * sc;
    if (viaX !== undefined) { ctx.setLineDash(DASH); ctx.strokeStyle = withAlpha(color, 0.5); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(viaX, ay); ctx.lineTo(ox, oy); ctx.stroke(); ctx.setLineDash(NODASH); }
    ctx.strokeStyle = color; ctx.lineWidth = 1.8; ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(ex, ay - yHit * sc); ctx.stroke();
    arrowMid(ctx, ox, oy, ex, ay - yHit * sc, color);
  }

  function drawArrow(ctx, x, y0, y1, color, width, dashedLine) {
    if (dashedLine) ctx.setLineDash([4, 4]);
    ctx.strokeStyle = color; ctx.lineWidth = width;
    ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, y1); ctx.stroke(); ctx.setLineDash(NODASH);
    const dir = y1 < y0 ? -1 : 1, hs = Math.min(9, Math.abs(y1 - y0) * 0.5);
    ctx.fillStyle = color; ctx.beginPath(); ctx.moveTo(x, y1); ctx.lineTo(x - hs * 0.7, y1 - dir * hs); ctx.lineTo(x + hs * 0.7, y1 - dir * hs); ctx.fill();
  }

  function drawElement(ctx, halfH) {
    const kd = KINDS[s.kind];
    if (kd.lens) {
      const bulge = Math.min(16, 6 + 160 / s.f) * (kd.sign > 0 ? 1 : -1);
      ctx.beginPath();
      if (kd.sign > 0) {
        ctx.moveTo(ex, ay - halfH); ctx.quadraticCurveTo(ex + bulge * 2, ay, ex, ay + halfH); ctx.quadraticCurveTo(ex - bulge * 2, ay, ex, ay - halfH);
      } else {
        const t = 7;
        ctx.moveTo(ex - t, ay - halfH); ctx.lineTo(ex + t, ay - halfH); ctx.quadraticCurveTo(ex + t + bulge * 2, ay, ex + t, ay + halfH); ctx.lineTo(ex - t, ay + halfH); ctx.quadraticCurveTo(ex - t - bulge * 2, ay, ex - t, ay - halfH);
      }
      ctx.fillStyle = 'rgba(150,195,240,0.35)'; ctx.fill(); ctx.strokeStyle = 'rgba(37,99,235,0.65)'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.strokeStyle = 'rgba(37,99,235,0.25)'; ctx.setLineDash([2, 4]); ctx.beginPath(); ctx.moveTo(ex, ay - halfH); ctx.lineTo(ex, ay + halfH); ctx.stroke(); ctx.setLineDash(NODASH);
    } else {
      const R = Math.max(2 * s.f * sc, halfH * 2.6);
      const a = Math.asin(Math.min(0.95, halfH / R));
      const cxm = kd.sign > 0 ? ex - R : ex + R;
      ctx.beginPath();
      if (kd.sign > 0) ctx.arc(cxm, ay, R, -a, a); else ctx.arc(cxm, ay, R, Math.PI - a, Math.PI + a);
      ctx.strokeStyle = '#64748b'; ctx.lineWidth = 4; ctx.stroke();
      ctx.strokeStyle = '#c7d2e0'; ctx.lineWidth = 1.5; ctx.stroke();
      // silvered back: hatching
      ctx.strokeStyle = 'rgba(100,116,139,0.6)'; ctx.lineWidth = 1; ctx.beginPath();
      for (let t = -a; t <= a; t += 0.06 * (60 / Math.max(60, R)) + 0.02) {
        const px = kd.sign > 0 ? cxm + Math.cos(t) * R : cxm - Math.cos(t) * R, py = ay + Math.sin(t) * R;
        ctx.moveTo(px + 2, py); ctx.lineTo(px + 9, py - 6);
      }
      ctx.stroke();
      ctx.strokeStyle = 'rgba(100,116,139,0.25)'; ctx.setLineDash([2, 4]); ctx.beginPath(); ctx.moveTo(ex, ay - halfH); ctx.lineTo(ex, ay + halfH); ctx.stroke(); ctx.setLineDash(NODASH);
    }
  }

  function axisPoint(ctx, cm, label, color, big) {
    const x = X(cm);
    if (x < left || x > right) return;
    ctx.beginPath(); ctx.arc(x, ay, big ? 4.5 : 3.5, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
    text(ctx, label, x, ay + 18, color, 11, 700, 'center');
  }

  function draw(ctx, dt) {
    fShow.to(s.f); fShow.step(dt); uShow.to(s.u); uShow.step(dt);
    hot.obj.to(k.isHot(objH) ? 1 : 0); hot.f.to(k.isHot(fH) ? 1 : 0); hot.scr.to(k.isHot(scrH) ? 1 : 0);
    hot.obj.step(dt); hot.f.step(dt); hot.scr.step(dt);
    const kd = KINDS[s.kind];
    solve(s.kind, uShow.x, fShow.x, s.h, r);
    const fsg = kd.sign * fShow.x;
    // axis and scale
    ctx.strokeStyle = T.ink2; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(left, ay); ctx.lineTo(right, ay); ctx.stroke();
    const step = sc * 10 < 26 ? 20 : 10;
    ctx.strokeStyle = T.line; ctx.lineWidth = 1; ctx.beginPath();
    for (let cm = -Math.floor((ex - left) / sc / step) * step; X(cm) <= right; cm += step) { ctx.moveTo(X(cm), ay + 3); ctx.lineTo(X(cm), ay + 8); }
    ctx.stroke();
    for (let cm = -Math.floor((ex - left) / sc / (step * 2)) * step * 2; X(cm) <= right - 10; cm += step * 2) if (cm !== 0) text(ctx, `${Math.abs(cm)}`, X(cm), bottom + 16, T.mute, 9.5, 500, 'center');
    text(ctx, 'distances in cm from the ' + (kd.lens ? 'lens' : 'pole'), left, top + 4, T.mute, 9.5, 600, 'left', 'top');
    // regions for the concave mirror
    if (s.regions && !kd.lens && kd.sign > 0) {
      const xC = X(-2 * fShow.x), xF = X(-fShow.x);
      ctx.fillStyle = 'rgba(37,99,235,0.04)'; ctx.fillRect(Math.max(left, X(-s.span)), top, xC - Math.max(left, X(-s.span)), bottom - top);
      ctx.fillStyle = 'rgba(234,179,8,0.06)'; ctx.fillRect(xC, top, xF - xC, bottom - top);
      ctx.fillStyle = 'rgba(22,163,74,0.05)'; ctx.fillRect(xF, top, ex - xF, bottom - top);
      if (!k.small) {
        text(ctx, 'beyond C', (Math.max(left, X(-s.span)) + xC) / 2, top + 14, T.mute, 10, 600, 'center');
        if (xF - xC > 50) text(ctx, 'between C and F', (xC + xF) / 2, top + 14, T.mute, 10, 600, 'center');
        if (ex - xF > 50) text(ctx, 'F to P', (xF + ex) / 2, top + 14, T.mute, 10, 600, 'center');
      }
    }
    // rays
    let maxY = Math.abs(s.h);
    const rays = [];
    if (s.mode === 'parallel') {
      const H = Math.min((ay - top) / sc * 0.7, 18);
      for (let i = -3; i <= 3; i++) if (i) rays.push(H * i / 3);
      maxY = Math.max(maxY, H);
    } else {
      rays.push(s.h);
      rays.push(kd.lens || Math.abs(uShow.x - 2 * fsg) < 0.3 ? 0 : s.h - (s.h / (uShow.x - 2 * fsg)) * uShow.x);
      if (Math.abs(uShow.x - fsg) > 0.5) rays.push(s.h - (s.h / (uShow.x - fsg)) * uShow.x);
      for (const y of rays) maxY = Math.max(maxY, Math.abs(y));
    }
    const halfH = clamp(maxY * sc * 1.12 + 6, 40, Math.min(ay - top, bottom - ay));
    ctx.save(); ctx.beginPath(); ctx.rect(left, top, right - left, bottom - top); ctx.clip();
    if (s.mode === 'parallel') {
      for (const y of rays) {
        ctx.strokeStyle = T.orange; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(left, ay - y * sc); ctx.lineTo(ex, ay - y * sc); ctx.stroke();
        arrowMid(ctx, left, ay - y * sc, ex, ay - y * sc, T.orange);
        rayOut(ctx, y, 0, T.orange, fsg < 0);
      }
    } else {
      const virt = !r.real && !r.inf;
      rayIn(ctx, rays[0], RAY_COLORS[0]); rayOut(ctx, rays[0], 0, RAY_COLORS[0], virt);
      const s1 = (rays[1] - s.h) / uShow.x;
      rayIn(ctx, rays[1], RAY_COLORS[1], !kd.lens && kd.sign > 0 && uShow.x < 2 * fsg ? X(-2 * fsg) : undefined); rayOut(ctx, rays[1], s1, RAY_COLORS[1], virt);
      if (rays.length > 2) {
        const s2 = (rays[2] - s.h) / uShow.x;
        rayIn(ctx, rays[2], RAY_COLORS[2], fsg > 0 && uShow.x < fsg ? X(-fsg) : undefined); rayOut(ctx, rays[2], s2, RAY_COLORS[2], virt);
      }
    }
    ctx.restore();
    drawElement(ctx, halfH);
    // focal points
    axisPoint(ctx, -fsg, 'F', T.orange, true);
    if (kd.lens) axisPoint(ctx, fsg, "F'", T.orange);
    axisPoint(ctx, -2 * fsg, kd.lens ? '2F' : 'C', T.purple);
    if (kd.lens) axisPoint(ctx, 2 * fsg, "2F'", T.purple);
    text(ctx, kd.lens ? 'O' : 'P', ex + 6, ay + 16, T.ink2, 11, 700);
    knob(ctx, fKnob(), ay, 6, T.orange, hot.f.x);
    // object
    const ox = X(-uShow.x);
    if (s.mode !== 'parallel') {
    drawArrow(ctx, ox, ay, ay - s.h * sc, T.orange, 3.5);
    text(ctx, 'object', ox, ay + 32, T.orange, 10, 700, 'center');
    knob(ctx, ox, ay - s.h * sc, 7, T.orange, hot.obj.x);
    } else text(ctx, 'rays from a distant object (the Sun, a far tree)', left + 6, top + 22, T.orange, 10.5, 600, 'left', 'top');
    // image
    if (s.mode === 'principal' && !r.inf) {
      const ix = physX(r.v);
      if (ix > left && ix < right && Math.abs(r.hi) * sc < (bottom - top)) {
        drawArrow(ctx, ix, ay, ay - r.hi * sc, r.real ? T.purple : withAlpha(T.purple, 0.6), 3.5, !r.real);
        pill(ctx, r.real ? 'real image' : 'virtual image', ix, ay - r.hi * sc + (r.hi > 0 ? -16 : 16), { color: T.purple, size: 10 });
      } else pill(ctx, 'image off the bench →', kd.lens === r.real ? right - 70 : left + 70, ay - 30, { color: T.purple, size: 10 });
    } else if (r.inf && s.mode === 'principal') pill(ctx, 'rays leave parallel: image at infinity', (left + right) / 2, top + 30, { color: T.purple, size: 10.5 });
    // screen
    if (s.screen !== null && kd.lens) {
      const sx = X(s.screen);
      ctx.fillStyle = '#fff'; ctx.strokeStyle = T.line; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.roundRect(sx - 4, ay - 110, 8, 220, 3); ctx.fill(); ctx.stroke();
      if (hot.scr.x > 0.02) { ctx.fillStyle = withAlpha(T.blue, 0.12 * hot.scr.x); ctx.fillRect(sx - 10, ay - 116, 20, 232); }
      ctx.fillStyle = '#64748b'; ctx.fillRect(sx - 12, ay + 106, 24, 8);
      if (r.real && !r.inf && r.v > 0) {
        const blur = 2 * halfH / sc * Math.abs(s.screen - r.v) / r.v;
        const mag = s.screen / uShow.x;
        const hh = -s.h * mag * sc;
        const a = 1 / (1 + blur * 0.9);
        ctx.strokeStyle = withAlpha(T.purple, 0.25 + 0.75 * a); ctx.lineWidth = 2 + blur * sc * 0.9;
        ctx.beginPath(); ctx.moveTo(sx, ay); ctx.lineTo(sx, ay - hh); ctx.stroke();
        s.blur = blur;
        text(ctx, blur < 0.4 ? 'sharp image!' : 'blurred', sx, ay - 120, blur < 0.4 ? T.green : T.mute, 10.5, 700, 'center');
      } else { s.blur = Infinity; text(ctx, 'no image', sx, ay - 120, T.mute, 10.5, 700, 'center'); }
      text(ctx, 'screen', sx, ay + 128, T.ink2, 10, 600, 'center');
    }
    return r;
  }

  return {
    state: s, result: r, layout, draw,
    debug: () => ({ objTip: [X(-s.u), ay - s.h * sc], f: [fKnob(), ay], screen: s.screen !== null ? [X(s.screen), ay] : null, ex, ay, sc }),
    get moving() { return fShow.moving || uShow.moving || hot.obj.moving || hot.f.moving || hot.scr.moving; },
    setKind(kind) { s.kind = kind; changed(); },
  };
}
