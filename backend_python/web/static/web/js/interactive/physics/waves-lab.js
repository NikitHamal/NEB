/**
 * Waves and sound — a real string. In "Shake it" the string is solved with the wave equation
 * (finite differences, y_tt = v²y_xx): grab the hand and shake, or switch on the oscillator, and
 * choose what the far end does (tied: pulses come back upside down; loose ring: upright;
 * endless: no echo). "Standing waves" shows harmonic n with its nodes and antinodes,
 * f = nv/2L; "Interference" adds two waves with a phase difference. One bead is marked so you can
 * see the string only moves up and down while the wave travels along.
 */
import { createKit, T, Spring, Ring, fmt, clamp, background, grid, text, pill, knob, withAlpha, dimension, sphere } from '../core/kit2d.js';
import { Plot } from '../core/kit2d-plot.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const LEN = 8;
const N = 200;
const DX = LEN / N;

export default function init(stage) {
  const k = createKit(stage, { label: 'A string stretched from a hand to a wall, carrying waves' });
  const hud = createHud(stage);
  const badge = hud.badge('Grab the hand and shake the string', T.blue);

  let mode = 'shake', end = 'fixed', osc = false, f = 1, A = 0.3, v = 4, harmonic = 3, phase = 0, f2 = 1, paused = false, sound = false;
  let y = new Float64Array(N + 1), yp = new Float64Array(N + 1), yn = new Float64Array(N + 1);
  let t = 0, handY = 0, handHeld = false, simT = 0;
  const handSpring = new Spring(0, 60, 9);
  const hotHand = new Spring(0, 260, 26);
  const trace = new Ring(500);
  const plot = new Plot({ title: 'Red bead: displacement against time', xLabel: 't / s', yLabel: 'y / m', yMin: -0.8, yMax: 0.8 });
  let audio = null;

  const panel = createPanel(stage, { title: 'Waves' });
  const modeC = panel.chips({ label: 'Experiment', options: [{ value: 'shake', label: 'Shake it' }, { value: 'standing', label: 'Standing waves' }, { value: 'interference', label: 'Interference' }], value: 'shake', onChange: (m) => { mode = m; resetString(); show(); } });
  const endC = panel.chips({ label: 'Far end', options: [{ value: 'fixed', label: 'Tied to wall' }, { value: 'free', label: 'Loose ring' }, { value: 'open', label: 'Endless' }], value: 'fixed', onChange: (e) => { end = e; resetString(); } });
  const oscT = panel.toggle({ label: 'Oscillator drives the hand', value: false, onChange: (o) => { osc = o; k.animate(true); } });
  const fS = panel.slider({ label: 'Frequency f', min: 0.25, max: 3, step: 0.05, value: f, format: (x) => `${x.toFixed(2)} Hz`, onChange: (x) => { f = x; } });
  const aS = panel.slider({ label: 'Amplitude A', min: 0.05, max: 0.6, step: 0.05, value: A, format: (x) => `${x.toFixed(2)} m`, onChange: (x) => { A = x; } });
  panel.slider({ label: 'Wave speed v', min: 1, max: 8, step: 0.5, value: v, format: (x) => `${x.toFixed(1)} m/s`, onChange: (x) => { v = x; } });
  const hS = panel.slider({ label: 'Harmonic n', min: 1, max: 6, step: 1, value: harmonic, format: (x) => `n = ${x}`, onChange: (x) => { harmonic = x; } });
  const pS = panel.slider({ label: 'Phase difference', min: 0, max: 360, step: 15, value: 0, format: (x) => `${x}°`, onChange: (x) => { phase = x * Math.PI / 180; } });
  const f2S = panel.slider({ label: 'Wave 2 frequency', min: 0.25, max: 3, step: 0.05, value: 1, format: (x) => `${x.toFixed(2)} Hz`, onChange: (x) => { f2 = x; } });
  panel.toggle({ label: 'Hear the pitch (f × 200)', value: false, onChange: (s) => { sound = s; syncSound(); } });
  panel.buttonRow([
    { label: 'Pause', icon: 'pause', variant: 'ghost', onClick: () => { paused = !paused; k.animate(!paused); } },
    { label: 'Calm string', icon: 'waves', variant: 'ghost', onClick: resetString },
  ]);
  const st = panel.stats([{ key: 'f', label: 'Frequency f' }, { key: 'lam', label: 'Wavelength λ = v/f' }, { key: 'T', label: 'Period T = 1/f' }, { key: 'v', label: 'Speed v = fλ' }]);
  panel.info('Every bit of the string only moves up and down; the shape is what travels. Double f and λ halves, because v = fλ stays fixed by the string.');

  function show() {
    endC.el.style.display = mode === 'shake' ? '' : 'none';
    oscT.el.style.display = mode === 'shake' ? '' : 'none';
    hS.el.style.display = mode === 'standing' ? '' : 'none';
    pS.el.style.display = f2S.el.style.display = mode === 'interference' ? '' : 'none';
    fS.el.style.display = mode === 'standing' ? 'none' : '';
    k.animate(true);
  }
  function resetString() { y.fill(0); yp.fill(0); yn.fill(0); handY = 0; handSpring.set(0); trace.clear(); simT = 0; k.animate(true); }

  let x0 = 0, x1 = 0, midY = 0, sy = 100;
  k.onResize((w, h) => {
    x0 = k.small ? 40 : 80; x1 = w - (k.small ? 26 : 50);
    const graphH = k.small ? 0 : Math.max(120, h * 0.24);
    midY = (h - graphH) * 0.5 + 6; sy = Math.min(((h - graphH) * 0.5 - 50) / 0.8, 260);
    if (graphH) plot.box(14, h - graphH - 10, w - 28, graphH);
  });
  const SX = (m) => x0 + m / LEN * (x1 - x0);
  const SY = (m) => midY - m * sy;

  const hand = k.drag({
    enabled: () => mode === 'shake',
    hit: (px, py, s) => { const d = Math.hypot(px - x0 + 22, py - SY(handY)); return d < 26 + s ? d : false; },
    down: () => { handHeld = true; osc = false; oscT.set(false); k.animate(true); },
    move: (px, py) => { handY = clamp((midY - py) / sy, -0.7, 0.7); handSpring.set(handY); },
    up: () => { handHeld = false; handSpring.set(handY); handSpring.to(0); },
  });

  function stepString(dt) {
    const hmax = 0.7 * DX / v;
    const n = Math.max(1, Math.ceil(dt / hmax)), h = dt / n;
    const r2 = (v * h / DX) ** 2, damp = 0.15 * h;
    for (let s = 0; s < n; s++) {
      t += h;
      const drive = handHeld ? handY : osc ? A * Math.sin(2 * Math.PI * f * t) : handSpring.x;
      for (let i = 1; i < N; i++) yn[i] = 2 * y[i] - yp[i] + r2 * (y[i + 1] - 2 * y[i] + y[i - 1]) - damp * (y[i] - yp[i]);
      yn[0] = drive;
      if (end === 'fixed') yn[N] = 0;
      else if (end === 'free') yn[N] = yn[N - 1];
      else { const c = v * h; yn[N] = y[N - 1] + (c - DX) / (c + DX) * (yn[N - 1] - y[N]); }
      const tmp = yp; yp = y; y = yn; yn = tmp;
    }
  }

  function analytic(xm, tt) {
    const om = 2 * Math.PI * f, kk = om / v;
    if (mode === 'standing') return comp(xm, tt, 0) + comp(xm, tt, 1);
    const om2 = 2 * Math.PI * f2, k2 = om2 / v;
    return A * 0.6 * Math.sin(om * tt - kk * xm) + A * 0.6 * Math.sin(om2 * tt - k2 * xm + phase);
  }
  function comp(xm, tt, which) {
    if (mode === 'standing') { const kn = harmonic * Math.PI / LEN, om = 2 * Math.PI * harmonic * v / (2 * LEN); return which ? -A * 0.6 * Math.sin(om * tt + kn * xm) : A * 0.6 * Math.sin(om * tt - kn * xm); }
    if (which === 0) return A * 0.6 * Math.sin(2 * Math.PI * f * tt - 2 * Math.PI * f / v * xm);
    return A * 0.6 * Math.sin(2 * Math.PI * f2 * tt - 2 * Math.PI * f2 / v * xm + phase);
  }
  function yAt(i) { return mode === 'shake' ? y[i] : analytic(i * DX, t); }

  function syncSound() {
    const want = sound && !paused && !document.hidden;
    if (want && !audio) {
      try {
        const ac = new (window.AudioContext || window.webkitAudioContext)();
        const o = ac.createOscillator(), g = ac.createGain();
        o.type = 'sine'; g.gain.value = 0.0001; o.connect(g); g.connect(ac.destination); o.start();
        g.gain.setTargetAtTime(0.05, ac.currentTime, 0.05);
        audio = { ac, o, g };
      } catch (e) { audio = null; }
    } else if (!want && audio) { const a = audio; audio = null; a.g.gain.setTargetAtTime(0, a.ac.currentTime, 0.04); setTimeout(() => a.ac.close(), 200); }
  }
  document.addEventListener('visibilitychange', syncSound);

  k.frame((ctx, dt, w, h) => {
    if (!paused) {
      if (mode === 'shake') { handSpring.step(dt); stepString(dt); } else t += dt;
      simT += dt;
      trace.push(simT, yAt(Math.round(2 / DX)));
    }
    hotHand.to(k.isHot(hand) ? 1 : 0); hotHand.step(dt);
    const fNow = mode === 'standing' ? harmonic * v / (2 * LEN) : f;
    if (audio) audio.o.frequency.setTargetAtTime(fNow * 200, audio.ac.currentTime, 0.03);
    background(k, ctx, w, h);
    grid(ctx, 0, 0, w, h, 24, T.grid);
    // axis and metre marks
    ctx.strokeStyle = T.line; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x0, midY); ctx.lineTo(x1, midY); ctx.stroke();
    for (let m = 0; m <= LEN; m++) text(ctx, `${m}`, SX(m), midY + 0.8 * sy + 20, T.mute, 9.5, 500, 'center');
    text(ctx, 'metres along the string', (x0 + x1) / 2, midY + 0.8 * sy + 36, T.mute, 10, 600, 'center');
    // wall / ring
    if (mode !== 'shake' || end !== 'open') {
      ctx.fillStyle = '#cbd5e1'; ctx.fillRect(x1, midY - 0.8 * sy, 12, 1.6 * sy);
      ctx.strokeStyle = '#94a3b8'; ctx.beginPath(); for (let yy = midY - 0.8 * sy; yy < midY + 0.8 * sy; yy += 10) { ctx.moveTo(x1 + 12, yy); ctx.lineTo(x1 + 4, yy + 8); } ctx.stroke();
      if (mode === 'shake' && end === 'free') { ctx.strokeStyle = '#64748b'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x1 - 2, midY - 0.8 * sy); ctx.lineTo(x1 - 2, midY + 0.8 * sy); ctx.stroke(); }
    } else text(ctx, 'continues forever →', x1, midY - 0.8 * sy, T.mute, 10, 600, 'right');
    // components
    if (mode !== 'shake') {
      for (let c = 0; c < 2; c++) {
        ctx.strokeStyle = withAlpha(c ? T.teal : T.purple, 0.55); ctx.lineWidth = 1.5; ctx.setLineDash([5, 4]); ctx.beginPath();
        for (let i = 0; i <= N; i += 2) { const X = SX(i * DX), Y = SY(comp(i * DX, t, c)); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }
        ctx.stroke(); ctx.setLineDash([]);
      }
    }
    // string
    ctx.strokeStyle = '#1e3a8a'; ctx.lineWidth = 3.2; ctx.beginPath();
    for (let i = 0; i <= N; i++) { const X = SX(i * DX), Y = SY(yAt(i)); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }
    ctx.stroke();
    ctx.fillStyle = '#60a5fa';
    for (let i = 0; i <= N; i += 10) { ctx.beginPath(); ctx.arc(SX(i * DX), SY(yAt(i)), 2.6, 0, Math.PI * 2); ctx.fill(); }
    const bi = Math.round(2 / DX);
    sphere(ctx, SX(2), SY(yAt(bi)), 6, '#e5484d');
    // standing wave labels
    if (mode === 'standing') {
      for (let n = 0; n <= harmonic; n++) { const X = SX(n * LEN / harmonic); ctx.beginPath(); ctx.arc(X, midY, 4, 0, Math.PI * 2); ctx.fillStyle = T.red; ctx.fill(); if (!k.small || harmonic < 4) text(ctx, 'N', X, midY - 10, T.red, 10, 800, 'center'); }
      for (let n = 0; n < harmonic; n++) { const X = SX((n + 0.5) * LEN / harmonic); text(ctx, 'A', X, SY(2 * A * 0.6) - 10, T.green, 10, 800, 'center'); }
      const lam = 2 * LEN / harmonic;
      if (lam <= LEN) dimension(ctx, SX(0), midY + 0.8 * sy - 8, SX(lam), midY + 0.8 * sy - 8, `λ = ${fmt(lam, 2)} m`, T.blue);
      else pill(ctx, `λ = ${fmt(lam, 2)} m (longer than the string)`, (x0 + x1) / 2, midY + 0.8 * sy - 8, { color: T.blue, size: 10.5 });
    } else if (mode === 'interference' || osc) {
      const lam = v / f;
      if (lam < LEN * 0.9) {
        let ic = -1;
        for (let i = 10; i < N - 2; i++) { if (yAt(i) > yAt(i - 1) && yAt(i) >= yAt(i + 1) && yAt(i) > A * 0.2) { ic = i; break; } }
        if (ic > 0 && ic * DX + lam < LEN) dimension(ctx, SX(ic * DX), SY(yAt(ic)) - 18, SX(ic * DX + lam), SY(yAt(ic)) - 18, `λ = ${fmt(lam, 2)} m`, T.blue);
      }
    }
    // the hand
    if (mode === 'shake') {
      const hy = SY(y[0]);
      ctx.strokeStyle = '#d6a77a'; ctx.lineWidth = 10; ctx.beginPath(); ctx.moveTo(x0 - 60, hy + 8); ctx.lineTo(x0 - 18, hy); ctx.stroke();
      ctx.beginPath(); ctx.ellipse(x0 - 12, hy, 12, 10, 0, 0, Math.PI * 2); ctx.fillStyle = '#f2c79a'; ctx.fill(); ctx.strokeStyle = '#c99868'; ctx.lineWidth = 1.5; ctx.stroke();
      knob(ctx, x0 - 22, hy, 7, T.blue, hotHand.x);
      if (!handHeld && !osc && trace.n < 30) pill(ctx, 'grab and shake ↕', x0 + 60, hy - 30, { color: T.blue, size: 10.5 });
    } else {
      ctx.fillStyle = '#cbd5e1'; ctx.fillRect(x0 - 12, midY - 0.8 * sy, 12, 1.6 * sy);
    }
    if (plot.w > 100) {
      const span = 8, t1 = Math.max(span, simT);
      plot.range(t1 - span, t1, -0.8, 0.8).frame(ctx);
      plot.clip(ctx); plot.ring(ctx, trace, T.red, 2); plot.unclip(ctx);
    }
    const lam = mode === 'standing' ? 2 * LEN / harmonic : v / f;
    st.f.set(mode === 'shake' && !osc ? 'your hand' : `${fmt(fNow, 2)} Hz`);
    st.lam.set(mode === 'shake' && !osc ? '—' : `${fmt(lam, 2)} m`);
    st.T.set(mode === 'shake' && !osc ? '—' : `${fmt(1 / fNow, 2)} s`);
    st.v.set(`${fmt(v, 1)} m/s`);
    const constructive = Math.cos(phase) > 0.7, destructive = Math.cos(phase) < -0.7;
    badge.set(mode === 'standing' ? `Harmonic ${harmonic}: f = nv/2L = ${fmt(fNow, 2)} Hz, ${harmonic + 1} nodes` : mode === 'interference' ? (Math.abs(f - f2) > 0.01 ? 'Different frequencies: the sum swells and fades (beats)' : constructive ? 'In step: constructive interference' : destructive ? 'Opposite: destructive interference' : 'Partly in step') : end === 'fixed' ? 'Tied end: pulses come back upside down' : end === 'free' ? 'Loose end: pulses come back upright' : 'Endless string: no echo');
    k.animate(!paused);
  });

  show();
  k.debug = { hand: () => [x0 - 22, SY(y[0])], peak: () => { let m = 0; for (let i = 0; i <= N; i++) m = Math.max(m, Math.abs(y[i])); return m; }, mode: (m) => { modeC.set(m); mode = m; show(); } };
  return { dispose() { sound = false; syncSound(); document.removeEventListener('visibilitychange', syncSound); k.dispose(); panel.dispose(); hud.dispose(); } };
}
