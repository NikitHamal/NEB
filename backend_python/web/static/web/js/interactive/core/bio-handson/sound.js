// Synthesised lab sounds (no audio files): the snick of a blade, the snip of scissors, a pin
// pushed into wax, a drop landing, the click of the objective turret, a soft chime for a step
// done and a low buzz for a mistake. Muted by default; the student turns sound on.
let ctx = null;
let master = null;
let noiseBuf = null;
let muted = true;

function ac() {
  if (ctx) return ctx;
  const AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return null;
  ctx = new AC();
  master = ctx.createGain(); master.gain.value = 0.5; master.connect(ctx.destination);
  noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 0.5, ctx.sampleRate);
  const d = noiseBuf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  return ctx;
}

function tone(freq, dur, { type = 'sine', gain = 0.2, attack = 0.005, slide = 0, delay = 0 } = {}) {
  const c = ac(); if (!c) return;
  const t = c.currentTime + delay;
  const o = c.createOscillator(); const g = c.createGain();
  o.type = type; o.frequency.setValueAtTime(freq, t);
  if (slide) o.frequency.exponentialRampToValueAtTime(Math.max(30, freq * slide), t + dur);
  g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(gain, t + attack); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.connect(g); g.connect(master); o.start(t); o.stop(t + dur + 0.02);
}
function noise(dur, { freq = 3000, q = 1, gain = 0.2, type = 'bandpass', delay = 0, sweep = 0 } = {}) {
  const c = ac(); if (!c) return;
  const t = c.currentTime + delay;
  const s = c.createBufferSource(); s.buffer = noiseBuf;
  const f = c.createBiquadFilter(); f.type = type; f.frequency.setValueAtTime(freq, t); f.Q.value = q;
  if (sweep) f.frequency.exponentialRampToValueAtTime(freq * sweep, t + dur);
  const g = c.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(gain, t + 0.004); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  s.connect(f); f.connect(g); g.connect(master); s.start(t, Math.random() * 0.3); s.stop(t + dur + 0.02);
}

const LIB = {
  cut: () => noise(0.09, { freq: 5200, q: 2.5, gain: 0.12, sweep: 0.6 }),
  snip: () => { noise(0.05, { freq: 6500, q: 4, gain: 0.25 }); tone(2400, 0.04, { type: 'triangle', gain: 0.05 }); },
  pin: () => { noise(0.06, { freq: 900, q: 1.2, gain: 0.25 }); tone(320, 0.08, { type: 'sine', gain: 0.08, slide: 0.7 }); },
  pick: () => tone(660, 0.07, { type: 'sine', gain: 0.08, slide: 1.4 }),
  drop: () => { tone(900, 0.12, { type: 'sine', gain: 0.12, slide: 0.45 }); noise(0.04, { freq: 2500, q: 3, gain: 0.05, delay: 0.02 }); },
  place: () => { noise(0.05, { freq: 1600, q: 2, gain: 0.18 }); tone(220, 0.06, { gain: 0.05 }); },
  click: () => { noise(0.025, { freq: 4000, q: 6, gain: 0.3 }); tone(1800, 0.02, { type: 'square', gain: 0.03 }); },
  tear: () => noise(0.18, { freq: 1200, q: 0.8, gain: 0.12, sweep: 2.5 }),
  squish: () => { noise(0.12, { freq: 500, q: 1.5, gain: 0.2, sweep: 0.5, type: 'lowpass' }); tone(140, 0.1, { gain: 0.05, slide: 0.6 }); },
  ok: () => { tone(880, 0.16, { type: 'sine', gain: 0.1 }); tone(1320, 0.22, { type: 'sine', gain: 0.08, delay: 0.08 }); },
  done: () => { [523, 659, 784, 1047].forEach((f, i) => tone(f, 0.3, { type: 'triangle', gain: 0.08, delay: i * 0.09 })); },
  bad: () => { tone(180, 0.22, { type: 'sawtooth', gain: 0.05, slide: 0.8 }); tone(150, 0.25, { type: 'square', gain: 0.025, delay: 0.05 }); },
  pour: () => noise(0.6, { freq: 700, q: 0.7, gain: 0.08, type: 'lowpass', sweep: 1.8 }),
  knob: () => noise(0.015, { freq: 3000, q: 8, gain: 0.08 }),
};

// Recorded sounds (CC0, Kenney.nl) for the moments a synth cannot fake: a petal plucked, a blade
// through tissue, a pin into wax, glass on the bench. Fetched only once sound is turned on; until a
// sample has loaded the synthesised version plays. Each play nudges pitch and level a little so a
// repeated action never sounds mechanical.
const SAMPLES = {
  pick: ['pluck1', 'pluck2'], tear: ['tear1', 'tear2', 'pluck2'], cut: ['cut1', 'cut2'], snip: ['snip1'], pin: ['pin1', 'pin2'],
  drop: ['drop1', 'drop2'], drip: ['drop1', 'drop2'], place: ['place1', 'place2'], glass: ['glass1', 'glass2'], click: ['click1', 'click2'],
  knob: ['knob1', 'knob2'], ok: ['ok1'], done: ['done1'], bad: ['bad1'], squish: ['squish1'], grab: ['pick1', 'pick2'], switch: ['switch1'],
};
const GAIN = { pick: 0.8, tear: 0.6, cut: 0.55, drop: 0.5, drip: 0.35, knob: 0.35, click: 0.5, place: 0.7, glass: 0.6, ok: 0.45, done: 0.5, bad: 0.45 };
const BASE = (() => {
  const s = (typeof document !== 'undefined' && [...document.querySelectorAll('script[src*="interactive/core/lesson.js"]')][0]) || null;
  return s ? s.src.replace(/js\/interactive\/core\/lesson\.js.*$/, 'audio/sfx/') : '/static/web/audio/sfx/';
})();
const buffers = new Map(); let loading = false;
function loadSamples() {
  if (loading) return; loading = true;
  const c = ac(); if (!c) return;
  const names = new Set(Object.values(SAMPLES).flat());
  names.forEach((n) => fetch(`${BASE}${n}.ogg`).then((r) => (r.ok ? r.arrayBuffer() : Promise.reject())).then((b) => c.decodeAudioData(b)).then((buf) => buffers.set(n, buf)).catch(() => {}));
}
function playSample(name) {
  const list = SAMPLES[name]; if (!list) return false;
  const ready = list.filter((n) => buffers.has(n)); if (!ready.length) return false;
  const c = ctx; const src = c.createBufferSource(); src.buffer = buffers.get(ready[Math.floor(Math.random() * ready.length)]);
  src.playbackRate.value = 0.94 + Math.random() * 0.12;
  const g = c.createGain(); g.gain.value = (GAIN[name] ?? 0.6) * (0.85 + Math.random() * 0.3);
  src.connect(g); g.connect(master); src.start();
  return true;
}

export { tone, noise };
export const sfx = {
  register(name, f) { LIB[name] = f; },
  play(name) {
    if (muted) return; const c = ac(); if (!c) return; if (c.state === 'suspended') c.resume();
    loadSamples();
    if (playSample(name)) return;
    const f = LIB[name]; if (f) f();
  },
  get muted() { return muted; },
  setMuted(v) { muted = !!v; if (!muted) { const c = ac(); if (c && c.state === 'suspended') c.resume(); loadSamples(); } },
};
