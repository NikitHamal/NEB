/**
 * Magnet magic — two bar magnets modelled as pairs of magnetic poles (inverse-square, like
 * Gilbert's model), so the field, the forces and the turning effects all come from one formula.
 * Drag a magnet to carry it (drag its end to turn it), let go and it is pulled or pushed by the
 * other one. Iron paperclips are induced magnets: they are pulled up the gradient of B², so the pull
 * grows sharply near the poles. Copper, wood and plastic ignore the magnets entirely.
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, softShadow, withAlpha, knob } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const NCLIP = 10;
const LINE_STEPS = 220;
const MAXLINES = 40;

export default function init(stage) {
  const k = createKit(stage, { label: 'Two bar magnets on a table with paperclips and other objects' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag a magnet towards the other one', T.blue);

  let showLines = true, showFilings = true;
  const mags = [
    { x: 0, y: 0, a: 0, vx: 0, vy: 0, w: 0, len: 120, th: 34, held: false },
    { x: 0, y: 0, a: 0, vx: 0, vy: 0, w: 0, len: 120, th: 34, held: false },
  ];
  const Q = 9000;
  const cx = new Float64Array(NCLIP), cy = new Float64Array(NCLIP), cvx = new Float64Array(NCLIP), cvy = new Float64Array(NCLIP), crot = new Float64Array(NCLIP);
  const stuck = new Uint8Array(NCLIP);
  const others = [];
  const lineBuf = new Float32Array(MAXLINES * LINE_STEPS * 2);
  const lineLen = new Uint16Array(MAXLINES);
  let nLines = 0, fieldDirty = true;
  let filA = new Float32Array(0), filS = new Float32Array(0), filCols = 0, filRows = 0;
  const FS = 26;
  let W = 1, Hh = 1;
  const flipAnim = [new Spring(0, 200, 18), new Spring(0, 200, 18)];
  const hot = [new Spring(0, 260, 26), new Spring(0, 260, 26)];
  const B = { x: 0, y: 0 };

  const panel = createPanel(stage, { title: 'Magnets' });
  panel.buttonRow([
    { label: 'Flip left', icon: 'swap_horiz', variant: 'ghost', onClick: () => flip(0) },
    { label: 'Flip right', icon: 'swap_horiz', variant: 'ghost', onClick: () => flip(1) },
  ]);
  panel.toggle({ label: 'Field lines', value: true, onChange: (v) => { showLines = v; k.invalidate(); } });
  panel.toggle({ label: 'Iron filings', value: true, onChange: (v) => { showFilings = v; k.invalidate(); } });
  panel.button({ label: 'Scatter the objects', icon: 'shuffle', variant: 'ghost', onClick: () => { scatter(); k.animate(true); } });
  const st = panel.stats([{ key: 'gap', label: 'Gap' }, { key: 'force', label: 'Force' }, { key: 'rule', label: 'Facing poles' }, { key: 'clips', label: 'Clips held' }]);
  panel.info('Opposite poles (N and S) attract, like poles repel. The pull fades fast with distance, so bring the magnet close. Only iron feels it: the coin, pencil and eraser stay put.');

  function poles(m, out) {
    const c = Math.cos(m.a), s = Math.sin(m.a), h = m.len / 2 - 10;
    out[0] = m.x + c * h; out[1] = m.y + s * h; out[2] = m.x - c * h; out[3] = m.y - s * h;
  }
  const P0 = new Float64Array(4), P1 = new Float64Array(4);
  function field(x, y, skip, out) {
    let bx = 0, by = 0;
    for (let i = 0; i < 2; i++) {
      if (i === skip) continue;
      const P = i === 0 ? P0 : P1;
      for (let j = 0; j < 2; j++) {
        const q = j === 0 ? Q : -Q;
        const dx = x - P[j * 2], dy = y - P[j * 2 + 1];
        const r2 = dx * dx + dy * dy + 120;
        const inv = q / (r2 * Math.sqrt(r2));
        bx += dx * inv; by += dy * inv;
      }
    }
    out.x = bx; out.y = by;
    return out;
  }

  function layout(w, h) {
    W = w; Hh = h;
    const s = k.small ? 0.72 : 1;
    for (const m of mags) { m.len = 130 * s; m.th = 36 * s; }
    mags[0].x = w * 0.3; mags[0].y = h * 0.45; mags[0].a = 0;
    mags[1].x = w * 0.68; mags[1].y = h * 0.55; mags[1].a = 0;
    others.length = 0;
    others.push({ kind: 'coin', x: w * 0.15, y: h * 0.8 }, { kind: 'pencil', x: w * 0.5, y: h * 0.86 }, { kind: 'eraser', x: w * 0.86, y: h * 0.22 });
    scatter();
    filCols = Math.ceil(w / FS); filRows = Math.ceil(h / FS);
    filA = new Float32Array(filCols * filRows); filS = new Float32Array(filCols * filRows);
    fieldDirty = true;
  }
  function scatter() {
    for (let i = 0; i < NCLIP; i++) {
      let tries = 0;
      do { cx[i] = 30 + Math.random() * (W - 60); cy[i] = 50 + Math.random() * (Hh - 80); tries++; } while (tries < 30 && nearMagnet(cx[i], cy[i], 150));
      cvx[i] = 0; cvy[i] = 0; crot[i] = Math.random() * Math.PI; stuck[i] = 0;
    }
  }
  function nearMagnet(x, y, pad) {
    for (const m of mags) if (Math.hypot(x - m.x, y - m.y) < m.len / 2 + pad) return true;
    return false;
  }
  k.onResize(layout);

  function flip(i) { mags[i].a += Math.PI; flipAnim[i].x = -Math.PI; flipAnim[i].v = 0; flipAnim[i].to(0); fieldDirty = true; k.animate(true); }

  function segClosest(m, px, py, out) {
    const c = Math.cos(m.a), s = Math.sin(m.a), h = m.len / 2 - m.th / 2;
    const t = clamp((px - m.x) * c + (py - m.y) * s, -h, h);
    out.x = m.x + c * t; out.y = m.y + s * t;
    return out;
  }
  const tmp = { x: 0, y: 0 }, tmp2 = { x: 0, y: 0 };

  let dragMode = 0, grabDX = 0, grabDY = 0;
  for (let i = 0; i < 2; i++) {
    const m = mags[i];
    const spec = k.drag({
      hit: (x, y, sl) => {
        const c = Math.cos(m.a), s = Math.sin(m.a);
        const u = (x - m.x) * c + (y - m.y) * s, v = -(x - m.x) * s + (y - m.y) * c;
        return Math.abs(u) < m.len / 2 + sl && Math.abs(v) < m.th / 2 + sl ? Math.hypot(u, v) * 0.5 : false;
      },
      down: (x, y) => {
        const c = Math.cos(m.a), s = Math.sin(m.a);
        const u = (x - m.x) * c + (y - m.y) * s;
        dragMode = Math.abs(u) > m.len * 0.36 ? 2 : 1;
        grabDX = x - m.x; grabDY = y - m.y; m.held = true; m.vx = m.vy = m.w = 0;
        k.animate(true);
      },
      move: (x, y) => {
        if (dragMode === 2) { m.a = Math.atan2(y - m.y, x - m.x) + (Math.cos(Math.atan2(grabDY, grabDX) - m.a) < 0 ? Math.PI : 0); }
        else { m.x = clamp(x - grabDX, 30, W - 30); m.y = clamp(y - grabDY, 30, Hh - 30); }
        fieldDirty = true;
      },
      up: () => { m.held = false; },
      cursor: 'grab',
    });
    m.spec = spec;
  }

  function stepMagnets(dt) {
    poles(mags[0], P0); poles(mags[1], P1);
    for (let i = 0; i < 2; i++) {
      const m = mags[i];
      if (m.held) continue;
      const P = i === 0 ? P0 : P1;
      let fx = 0, fy = 0, tq = 0;
      for (let j = 0; j < 2; j++) {
        field(P[j * 2], P[j * 2 + 1], i, B);
        const q = j === 0 ? Q : -Q;
        const Fx = q * B.x * 0.02, Fy = q * B.y * 0.02;
        fx += Fx; fy += Fy;
        tq += (P[j * 2] - m.x) * Fy - (P[j * 2 + 1] - m.y) * Fx;
      }
      const mass = 1, I = m.len * m.len / 12;
      const fmag = Math.hypot(fx, fy);
      const fric = 40;
      if (fmag > fric || Math.hypot(m.vx, m.vy) > 1) {
        m.vx += (fx / mass) * dt; m.vy += (fy / mass) * dt;
        const sp = Math.hypot(m.vx, m.vy);
        const dec = Math.min(sp, fric * dt * 2.5);
        if (sp > 0) { m.vx -= m.vx / sp * dec; m.vy -= m.vy / sp * dec; }
      }
      if (Math.abs(tq) > fric * 20 || Math.abs(m.w) > 0.02) { m.w += tq / (mass * I) * dt; m.w *= Math.exp(-dt * 6); }
      m.x += m.vx * dt; m.y += m.vy * dt; m.a += m.w * dt;
      m.x = clamp(m.x, 40, W - 40); m.y = clamp(m.y, 40, Hh - 40);
      if (Math.abs(m.vx) + Math.abs(m.vy) + Math.abs(m.w) > 0.01) fieldDirty = true;
    }
    // keep the magnets from passing through each other (capsule contact)
    const a = mags[0], b = mags[1];
    for (let it = 0; it < 3; it++) {
      segClosest(a, b.x, b.y, tmp); segClosest(b, tmp.x, tmp.y, tmp2); segClosest(a, tmp2.x, tmp2.y, tmp);
      const dx = tmp2.x - tmp.x, dy = tmp2.y - tmp.y, d = Math.hypot(dx, dy) || 1e-6, minD = (a.th + b.th) / 2;
      if (d < minD) {
        const push = (minD - d), nx = dx / d, ny = dy / d;
        const wa = a.held ? 0 : b.held ? 1 : 0.5, wb = 1 - wa;
        a.x -= nx * push * wa; a.y -= ny * push * wa; b.x += nx * push * wb; b.y += ny * push * wb;
        const rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny;
        if (rv < 0) { a.vx += nx * rv * wa; a.vy += ny * rv * wa; b.vx -= nx * rv * wb; b.vy -= ny * rv * wb; a.w *= 0.5; b.w *= 0.5; }
        fieldDirty = true;
      }
    }
  }

  function stepClips(dt) {
    let moving = false;
    for (let i = 0; i < NCLIP; i++) {
      const e = 2;
      field(cx[i] + e, cy[i], -1, B); const b1 = B.x * B.x + B.y * B.y;
      field(cx[i] - e, cy[i], -1, B); const b2 = B.x * B.x + B.y * B.y;
      field(cx[i], cy[i] + e, -1, B); const b3 = B.x * B.x + B.y * B.y;
      field(cx[i], cy[i] - e, -1, B); const b4 = B.x * B.x + B.y * B.y;
      field(cx[i], cy[i], -1, B);
      const chi = 6e4;
      let fx = chi * (b1 - b2) / (2 * e), fy = chi * (b3 - b4) / (2 * e);
      const fm = Math.hypot(fx, fy);
      const grip = 25;
      if (fm < grip && Math.hypot(cvx[i], cvy[i]) < 2) { cvx[i] = 0; cvy[i] = 0; stuck[i] = 0; continue; }
      if (fm > 4000) { fx *= 4000 / fm; fy *= 4000 / fm; }
      cvx[i] += fx * dt; cvy[i] += fy * dt;
      const damp = Math.exp(-dt * 7);
      cvx[i] *= damp; cvy[i] *= damp;
      cx[i] += cvx[i] * dt; cy[i] += cvy[i] * dt;
      const ta = Math.atan2(B.y, B.x);
      let da = ta - crot[i]; da = Math.atan2(Math.sin(2 * da), Math.cos(2 * da)) / 2;
      crot[i] += da * Math.min(1, dt * 8);
      stuck[i] = 0;
      for (const m of mags) {
        segClosest(m, cx[i], cy[i], tmp);
        const dx = cx[i] - tmp.x, dy = cy[i] - tmp.y, d = Math.hypot(dx, dy) || 1e-6, minD = m.th / 2 + 5;
        if (d < minD) { cx[i] = tmp.x + dx / d * minD; cy[i] = tmp.y + dy / d * minD; const vn = cvx[i] * dx / d + cvy[i] * dy / d; if (vn < 0) { cvx[i] -= vn * dx / d; cvy[i] -= vn * dy / d; } cvx[i] *= 0.6; cvy[i] *= 0.6; stuck[i] = 1; if (m.held || Math.abs(m.vx) + Math.abs(m.vy) > 1) { cx[i] += m.vx * dt; cy[i] += m.vy * dt; } }
      }
      for (let j = 0; j < i; j++) {
        const dx = cx[i] - cx[j], dy = cy[i] - cy[j], d = Math.hypot(dx, dy) || 1e-6;
        if (d < 12) { const p = (12 - d) / 2; cx[i] += dx / d * p; cy[i] += dy / d * p; cx[j] -= dx / d * p; cy[j] -= dy / d * p; }
      }
      cx[i] = clamp(cx[i], 8, W - 8); cy[i] = clamp(cy[i], 8, Hh - 8);
      if (Math.hypot(cvx[i], cvy[i]) > 0.5) moving = true;
    }
    return moving;
  }

  function rebuildField() {
    fieldDirty = false;
    poles(mags[0], P0); poles(mags[1], P1);
    for (let r = 0; r < filRows; r++) for (let c = 0; c < filCols; c++) {
      const x = (c + 0.5) * FS + ((r & 1) ? FS * 0.25 : -FS * 0.25), y = (r + 0.5) * FS;
      field(x, y, -1, B);
      const idx = r * filCols + c;
      filA[idx] = Math.atan2(B.y, B.x);
      filS[idx] = Math.hypot(B.x, B.y);
    }
    nLines = 0;
    const per = k.small ? 10 : 14;
    for (let mi = 0; mi < 2; mi++) {
      const P = mi === 0 ? P0 : P1;
      for (let l = 0; l < per && nLines < MAXLINES; l++) {
        const ang = (l + 0.5) / per * Math.PI * 2;
        let x = P[0] + Math.cos(ang) * 8, y = P[1] + Math.sin(ang) * 8;
        const base = nLines * LINE_STEPS * 2;
        let n = 0;
        for (let s = 0; s < LINE_STEPS; s++) {
          lineBuf[base + n * 2] = x; lineBuf[base + n * 2 + 1] = y; n++;
          field(x, y, -1, B);
          const bm = Math.hypot(B.x, B.y) || 1e-9;
          x += B.x / bm * 7; y += B.y / bm * 7;
          if (x < -40 || x > W + 40 || y < -40 || y > Hh + 40) break;
          if (Math.hypot(x - P0[2], y - P0[3]) < 8 || Math.hypot(x - P1[2], y - P1[3]) < 8) { lineBuf[base + n * 2] = x; lineBuf[base + n * 2 + 1] = y; n++; break; }
        }
        lineLen[nLines++] = n;
      }
    }
  }

  k.frame((ctx, dt, w, h) => {
    stepMagnets(dt);
    const clipsMoving = stepClips(dt);
    for (let i = 0; i < 2; i++) { flipAnim[i].step(dt); hot[i].to(k.isHot(mags[i].spec) ? 1 : 0); hot[i].step(dt); }
    if (fieldDirty) rebuildField();
    background(k, ctx, w, h, '#f6f1e8', '#ece3d3');
    // wood grain
    ctx.strokeStyle = 'rgba(150,110,60,0.07)'; ctx.lineWidth = 1; ctx.beginPath();
    for (let y = 12; y < h; y += 22) { ctx.moveTo(0, y); for (let x = 0; x <= w; x += 60) ctx.lineTo(x, y + Math.sin(x * 0.01 + y) * 3); }
    ctx.stroke();
    if (showFilings) {
      ctx.strokeStyle = 'rgba(60,64,72,0.55)'; ctx.lineWidth = 1.3; ctx.beginPath();
      for (let r = 0; r < filRows; r++) for (let c = 0; c < filCols; c++) {
        const idx = r * filCols + c, s = filS[idx];
        if (s < 0.02) continue;
        const x = (c + 0.5) * FS + ((r & 1) ? FS * 0.25 : -FS * 0.25), y = (r + 0.5) * FS;
        if (nearMagnet(x, y, -4) && insideAny(x, y)) continue;
        const L = Math.min(9, 3 + s * 20), a = filA[idx];
        const dx = Math.cos(a) * L, dy = Math.sin(a) * L;
        ctx.moveTo(x - dx, y - dy); ctx.lineTo(x + dx, y + dy);
      }
      ctx.stroke();
    }
    if (showLines) {
      ctx.lineWidth = 1.4; ctx.strokeStyle = withAlpha(T.blue, 0.45);
      ctx.beginPath();
      for (let l = 0; l < nLines; l++) {
        const base = l * LINE_STEPS * 2, n = lineLen[l];
        for (let s = 0; s < n; s++) { const x = lineBuf[base + s * 2], y = lineBuf[base + s * 2 + 1]; if (s) ctx.lineTo(x, y); else ctx.moveTo(x, y); }
      }
      ctx.stroke();
      ctx.fillStyle = withAlpha(T.blue, 0.7);
      for (let l = 0; l < nLines; l++) {
        const base = l * LINE_STEPS * 2, n = lineLen[l];
        if (n < 12) continue;
        const s = Math.floor(n * 0.45);
        const x = lineBuf[base + s * 2], y = lineBuf[base + s * 2 + 1], x2 = lineBuf[base + s * 2 + 2], y2 = lineBuf[base + s * 2 + 3];
        const a = Math.atan2(y2 - y, x2 - x);
        ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * 5, y + Math.sin(a) * 5); ctx.lineTo(x + Math.cos(a + 2.5) * 5, y + Math.sin(a + 2.5) * 5); ctx.lineTo(x + Math.cos(a - 2.5) * 5, y + Math.sin(a - 2.5) * 5); ctx.fill();
      }
    }
    for (const o of others) drawOther(ctx, o);
    for (let i = 0; i < NCLIP; i++) drawClip(ctx, cx[i], cy[i], crot[i]);
    for (let i = 0; i < 2; i++) drawMagnet(ctx, mags[i], flipAnim[i].x, hot[i].x);

    const a = mags[0], b = mags[1];
    segClosest(a, b.x, b.y, tmp); segClosest(b, tmp.x, tmp.y, tmp2); segClosest(a, tmp2.x, tmp2.y, tmp);
    const gap = Math.max(0, Math.hypot(tmp2.x - tmp.x, tmp2.y - tmp.y) - (a.th + b.th) / 2);
    poles(a, P0); poles(b, P1);
    let fx = 0, fy = 0;
    for (let j = 0; j < 2; j++) { field(P1[j * 2], P1[j * 2 + 1], 1, B); const q = j === 0 ? Q : -Q; fx += q * B.x * 0.02; fy += q * B.y * 0.02; }
    const toward = (fx * (a.x - b.x) + fy * (a.y - b.y)) > 0;
    const nearA = nearestPole(P0, b.x, b.y), nearB = nearestPole(P1, a.x, a.y);
    const rule = nearA === nearB ? 'repel' : 'attract';
    st.gap.set(`${fmt(gap / 40 * 2, 1)} cm`);
    st.force.set(`${fmt(Math.hypot(fx, fy) / 40, 1)} units ${toward ? '(pull)' : '(push)'}`);
    st.rule.set(`${nearA ? 'N' : 'S'}–${nearB ? 'N' : 'S'}: ${rule}`);
    let held = 0; for (let i = 0; i < NCLIP; i++) held += stuck[i]; st.clips.set(String(held));
    if (gap < 140) pill(ctx, nearA === nearB ? 'Like poles repel' : 'Opposites attract', (tmp.x + tmp2.x) / 2, (tmp.y + tmp2.y) / 2 - 34, { color: nearA === nearB ? T.red : T.green, size: 11 });
    badge.set(a.held || b.held ? 'Feel the push or pull as you get close' : 'Drag a magnet; drag its end to turn it');
    const moving = a.held || b.held || clipsMoving || Math.abs(a.vx) + Math.abs(a.vy) + Math.abs(b.vx) + Math.abs(b.vy) + Math.abs(a.w) + Math.abs(b.w) > 0.05 || flipAnim[0].moving || flipAnim[1].moving || hot[0].moving || hot[1].moving;
    k.animate(moving);
  });

  function nearestPole(P, x, y) { return Math.hypot(P[0] - x, P[1] - y) < Math.hypot(P[2] - x, P[3] - y); }
  function insideAny(x, y) {
    for (const m of mags) { const c = Math.cos(m.a), s = Math.sin(m.a); const u = (x - m.x) * c + (y - m.y) * s, v = -(x - m.x) * s + (y - m.y) * c; if (Math.abs(u) < m.len / 2 && Math.abs(v) < m.th / 2) return true; }
    return false;
  }
  function drawMagnet(ctx, m, spinX, hotX) {
    softShadow(ctx, m.x + 3, m.y + m.th * 0.5, m.len * 0.6, m.th * 0.4, 0.25);
    ctx.save(); ctx.translate(m.x, m.y); ctx.rotate(m.a + spinX);
    const L = m.len, H = m.th, sc = 1 + hotX * 0.04;
    ctx.scale(sc, sc);
    if (hotX > 0.02) { ctx.beginPath(); ctx.roundRect(-L / 2 - 6, -H / 2 - 6, L + 12, H + 12, 10); ctx.fillStyle = withAlpha(T.blue, 0.12 * hotX); ctx.fill(); }
    ctx.beginPath(); ctx.roundRect(-L / 2, -H / 2, L / 2, H, [6, 0, 0, 6]); ctx.fillStyle = '#3b6fd8'; ctx.fill();
    ctx.beginPath(); ctx.roundRect(0, -H / 2, L / 2, H, [0, 6, 6, 0]); ctx.fillStyle = '#e5484d'; ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.25)'; ctx.fillRect(-L / 2 + 4, -H / 2 + 3, L - 8, H * 0.22);
    ctx.fillStyle = 'rgba(0,0,0,0.12)'; ctx.fillRect(-L / 2 + 2, H / 2 - 5, L - 4, 4);
    ctx.fillStyle = '#fff'; ctx.font = `800 ${Math.round(H * 0.5)}px Poppins, system-ui, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.save(); ctx.translate(L / 4, 1); ctx.rotate(-(m.a + spinX)); ctx.fillText('N', 0, 0); ctx.restore();
    ctx.save(); ctx.translate(-L / 4, 1); ctx.rotate(-(m.a + spinX)); ctx.fillText('S', 0, 0); ctx.restore();
    ctx.restore();
  }
  function drawClip(ctx, x, y, a) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(1.4, 1.4);
    ctx.strokeStyle = '#7d8796'; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(-7, 2.5); ctx.lineTo(6, 2.5); ctx.arc(6, 0, 2.5, Math.PI / 2, -Math.PI / 2, true); ctx.lineTo(-6, -2.5); ctx.arc(-6, 0, 2.5, -Math.PI / 2, Math.PI / 2, true); ctx.lineTo(4, 0.5);
    ctx.stroke();
    ctx.restore();
  }
  function drawOther(ctx, o) {
    softShadow(ctx, o.x + 2, o.y + 6, 18, 5, 0.2);
    if (o.kind === 'coin') {
      ctx.beginPath(); ctx.arc(o.x, o.y, 13, 0, Math.PI * 2); ctx.fillStyle = '#c47a3a'; ctx.fill(); ctx.strokeStyle = '#9a5a26'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.beginPath(); ctx.arc(o.x, o.y, 8.5, 0, Math.PI * 2); ctx.stroke();
      text(ctx, 'copper coin', o.x, o.y + 28, T.ink2, 9.5, 600, 'center');
    } else if (o.kind === 'pencil') {
      ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(-0.12);
      ctx.fillStyle = '#f5c242'; ctx.fillRect(-40, -4, 66, 8); ctx.fillStyle = '#e9cfa6'; ctx.beginPath(); ctx.moveTo(26, -4); ctx.lineTo(38, 0); ctx.lineTo(26, 4); ctx.fill();
      ctx.fillStyle = '#333'; ctx.beginPath(); ctx.moveTo(34, -1.3); ctx.lineTo(38, 0); ctx.lineTo(34, 1.3); ctx.fill(); ctx.fillStyle = '#e88aa0'; ctx.fillRect(-46, -4, 6, 8); ctx.restore();
      text(ctx, 'wooden pencil', o.x, o.y + 22, T.ink2, 9.5, 600, 'center');
    } else {
      ctx.fillStyle = '#f08fa6'; ctx.beginPath(); ctx.roundRect(o.x - 16, o.y - 9, 32, 18, 4); ctx.fill(); ctx.fillStyle = '#3b82f6'; ctx.fillRect(o.x - 16, o.y - 9, 12, 18);
      text(ctx, 'plastic eraser', o.x, o.y + 24, T.ink2, 9.5, 600, 'center');
    }
  }

  k.debug = { mag: (i) => [mags[i].x, mags[i].y], held: () => { let n = 0; for (let i = 0; i < NCLIP; i++) n += stuck[i]; return n; } };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
