import { writeFileSync } from 'node:fs';
import { mulberry32 } from '../stage/engine/rng.js';

export const SR = 48000;
const TAU = Math.PI * 2;

export const midi = (n) => 440 * 2 ** ((n - 69) / 12);
export const noiseSource = (seed = 1) => {
  const r = mulberry32(seed);
  return () => r() * 2 - 1;
};
export const render = (seconds, fn) => {
  const n = Math.max(1, Math.round(seconds * SR));
  const out = new Float32Array(n);
  for (let i = 0; i < n; i += 1) out[i] = fn(i / SR, i, n);
  return out;
};

export function biquad(type, freq, q = 0.707) {
  const w = (TAU * Math.min(freq, SR * 0.45)) / SR;
  const cos = Math.cos(w);
  const alpha = Math.sin(w) / (2 * q);
  let b0;
  let b1;
  let b2;
  if (type === 'lp') {
    b0 = (1 - cos) / 2;
    b1 = 1 - cos;
    b2 = b0;
  } else if (type === 'hp') {
    b0 = (1 + cos) / 2;
    b1 = -(1 + cos);
    b2 = b0;
  } else {
    b0 = alpha;
    b1 = 0;
    b2 = -alpha;
  }
  const a0 = 1 + alpha;
  return { b0: b0 / a0, b1: b1 / a0, b2: b2 / a0, a1: (-2 * cos) / a0, a2: (1 - alpha) / a0, z1: 0, z2: 0 };
}

function step(f, x) {
  const y = f.b0 * x + f.z1;
  f.z1 = f.b1 * x - f.a1 * y + f.z2;
  f.z2 = f.b2 * x - f.a2 * y;
  return y;
}

export function filter(buf, type, freq, q) {
  const f = biquad(type, freq, q);
  const out = new Float32Array(buf.length);
  for (let i = 0; i < buf.length; i += 1) out[i] = step(f, buf[i]);
  return out;
}

export function sweep(buf, type, f0, f1, q = 0.8) {
  const out = new Float32Array(buf.length);
  let f = biquad(type, f0, q);
  for (let i = 0; i < buf.length; i += 1) {
    if (i % 32 === 0) {
      const next = biquad(type, f0 * (f1 / f0) ** (i / buf.length), q);
      next.z1 = f.z1;
      next.z2 = f.z2;
      f = next;
    }
    out[i] = step(f, buf[i]);
  }
  return out;
}

export function blepSaw(phase, dt) {
  let v = 2 * phase - 1;
  if (phase < dt) {
    const t = phase / dt;
    v -= t + t - t * t - 1;
  } else if (phase > 1 - dt) {
    const t = (phase - 1) / dt;
    v -= t * t + t + t + 1;
  }
  return v;
}

export const adsr = (t, hold, a, d, s, r) => {
  if (t < a) return t / a;
  if (t < a + d) return 1 - (1 - s) * ((t - a) / d);
  if (t < hold) return s;
  const tail = t - hold;
  return tail < r ? s * (1 - tail / r) : 0;
};

export function makeBus(seconds) {
  const n = Math.ceil(seconds * SR);
  return { n, L: new Float32Array(n), R: new Float32Array(n) };
}

export function place(bus, mono, at, gain = 1, pan = 0) {
  const start = Math.round(at * SR);
  const angle = ((pan + 1) * Math.PI) / 4;
  const gl = gain * Math.cos(angle);
  const gr = gain * Math.sin(angle);
  const from = Math.max(0, -start);
  const to = Math.min(mono.length, bus.n - start);
  for (let i = from; i < to; i += 1) {
    bus.L[start + i] += mono[i] * gl;
    bus.R[start + i] += mono[i] * gr;
  }
}

export function sendTo(send, mono, at, gain) {
  const start = Math.round(at * SR);
  const from = Math.max(0, -start);
  const to = Math.min(mono.length, send.length - start);
  for (let i = from; i < to; i += 1) send[start + i] += mono[i] * gain;
}

const COMB = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617];
const ALLPASS = [556, 441, 341, 225];

export function reverb(input, { room = 0.86, damp = 0.3, spread = 23 } = {}) {
  const scale = SR / 44100;
  const channel = (offset) => {
    const combs = COMB.map((d) => ({ buf: new Float32Array(Math.round((d + offset) * scale)), i: 0, store: 0 }));
    const aps = ALLPASS.map((d) => ({ buf: new Float32Array(Math.round((d + offset) * scale)), i: 0 }));
    const out = new Float32Array(input.length);
    for (let n = 0; n < input.length; n += 1) {
      const x = input[n] * 0.03;
      let sum = 0;
      for (const c of combs) {
        const y = c.buf[c.i];
        c.store = y * (1 - damp) + c.store * damp;
        c.buf[c.i] = x + c.store * room;
        c.i = (c.i + 1) % c.buf.length;
        sum += y;
      }
      for (const a of aps) {
        const b = a.buf[a.i];
        const y = -sum + b;
        a.buf[a.i] = sum + b * 0.5;
        a.i = (a.i + 1) % a.buf.length;
        sum = y;
      }
      out[n] = sum;
    }
    return out;
  };
  return [channel(0), channel(spread)];
}

export function pingPong(send, seconds, feedback = 0.38) {
  const d = Math.round(seconds * SR);
  const L = new Float32Array(send.length);
  const R = new Float32Array(send.length);
  for (let i = 0; i < send.length; i += 1) {
    L[i] = send[i] + (i >= d ? R[i - d] * feedback : 0);
    R[i] = i >= d ? L[i - d] : 0;
  }
  return [L, R];
}

export const rms = (buf) => {
  let sum = 0;
  for (let i = 0; i < buf.length; i += 1) sum += buf[i] * buf[i];
  return Math.sqrt(sum / Math.max(1, buf.length));
};

export function writeWav(file, L, R) {
  const n = L.length;
  const buf = Buffer.alloc(44 + n * 4);
  buf.write('RIFF', 0);
  buf.writeUInt32LE(36 + n * 4, 4);
  buf.write('WAVEfmt ', 8);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(2, 22);
  buf.writeUInt32LE(SR, 24);
  buf.writeUInt32LE(SR * 4, 28);
  buf.writeUInt16LE(4, 32);
  buf.writeUInt16LE(16, 34);
  buf.write('data', 36);
  buf.writeUInt32LE(n * 4, 40);
  const clip = (v) => Math.max(-1, Math.min(1, v));
  for (let i = 0; i < n; i += 1) {
    buf.writeInt16LE(Math.round(clip(L[i]) * 32767), 44 + i * 4);
    buf.writeInt16LE(Math.round(clip(R[i]) * 32767), 46 + i * 4);
  }
  writeFileSync(file, buf);
}
