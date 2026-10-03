import { SR, adsr, blepSaw, filter, midi, noiseSource, render, sweep } from './dsp.mjs';

const TAU = Math.PI * 2;
const fadeTail = (buf, seconds = 0.03) => {
  const n = Math.min(buf.length, Math.round(seconds * SR));
  for (let i = 0; i < n; i += 1) buf[buf.length - 1 - i] *= i / n;
  return buf;
};

export function kick(seed = 1) {
  const noise = noiseSource(seed);
  let phase = 0;
  return fadeTail(render(0.5, (t) => {
    phase += (TAU * (46 + 124 * Math.exp(-t / 0.045))) / SR;
    let v = Math.sin(phase) * Math.exp(-t / 0.2);
    if (t < 0.004) v += noise() * 0.3 * (1 - t / 0.004);
    return v * 0.95;
  }));
}

export function subNote(freq, seconds) {
  return render(seconds + 0.12, (t) => (Math.sin(TAU * freq * t) + 0.22 * Math.sin(TAU * freq * 2 * t)) * adsr(t, seconds, 0.008, 0.05, 0.85, 0.1) * 0.8);
}

export function bassNote(freq, seconds) {
  const dt = freq / SR;
  let phase = 0;
  const raw = render(seconds + 0.08, (t) => {
    phase = (phase + dt) % 1;
    return (blepSaw(phase, dt) * 0.55 + Math.sin(TAU * freq * t) * 0.6) * adsr(t, seconds, 0.006, 0.07, 0.7, 0.07);
  });
  return filter(raw, 'lp', 520, 0.9);
}

export function clap(seed = 2, level = 1) {
  const noise = noiseSource(seed);
  const raw = render(0.34, (t) => {
    const burst = (b) => (t >= b ? Math.exp(-(t - b) / 0.0045) : 0);
    const env = burst(0) + burst(0.011) + burst(0.022) + 0.75 * Math.exp(-t / 0.085);
    return noise() * env;
  });
  return fadeTail(filter(raw, 'bp', 1500, 0.9).map((v) => v * 1.6 * level));
}

export function snare(seed = 3, level = 1) {
  const noise = noiseSource(seed);
  const raw = render(0.24, (t) => noise() * Math.exp(-t / 0.07) * 0.9 + Math.sin(TAU * 185 * t) * Math.exp(-t / 0.05) * 0.5);
  return fadeTail(filter(raw, 'bp', 2200, 0.6).map((v) => v * 1.8 * level));
}

export function hat(open = false, seed = 4) {
  const noise = noiseSource(seed);
  const tau = open ? 0.16 : 0.022;
  return fadeTail(filter(render(open ? 0.5 : 0.12, (t) => noise() * Math.exp(-t / tau)), 'hp', 7200, 0.7).map((v) => v * 0.9), 0.02);
}

export function pad(freq, seconds, seed = 5) {
  const detune = [-8, 0, 8].map((c) => 2 ** (c / 1200));
  const offsets = detune.map((_, i) => (i * 0.31 + seed * 0.17) % 1);
  const phases = [...offsets];
  const raw = render(seconds + 0.45, (t) => {
    let sum = 0;
    for (let v = 0; v < 3; v += 1) {
      const f = freq * detune[v];
      phases[v] = (phases[v] + f / SR) % 1;
      sum += blepSaw(phases[v], f / SR);
    }
    return (sum / 3) * adsr(t, seconds, 0.16, 0.05, 0.95, 0.45);
  });
  return filter(raw, 'lp', 1500, 0.6);
}

export function pluck(freq, seconds = 0.32) {
  return filter(render(seconds, (t) => {
    const attack = Math.min(1, t / 0.003);
    return (Math.sin(TAU * freq * t) + 0.32 * Math.sin(TAU * freq * 2 * t) + 0.1 * Math.sin(TAU * freq * 3 * t)) * Math.exp(-t / 0.13) * attack;
  }), 'lp', 6500, 0.7);
}

export function bell(freq, seconds = 1.6) {
  const partials = [[1, 1, 1.1], [2.0, 0.5, 0.7], [3.01, 0.28, 0.45], [4.2, 0.14, 0.3]];
  return fadeTail(render(seconds, (t) => partials.reduce((sum, [ratio, amp, tau]) => sum + amp * Math.sin(TAU * freq * ratio * t) * Math.exp(-t / tau), 0) * Math.min(1, t / 0.002) * 0.5), 0.05);
}

export function whoosh(seconds = 0.5, seed = 6, up = true) {
  const noise = noiseSource(seed);
  const raw = render(seconds, (t, i, n) => noise() * Math.sin((Math.PI * i) / n) ** 2);
  return sweep(raw, 'bp', up ? 300 : 6500, up ? 6500 : 300, 1.3).map((v) => v * 2.2);
}

export function riser(seconds, seed = 7) {
  const noise = noiseSource(seed);
  let phase = 0;
  const raw = render(seconds, (t, i, n) => {
    const u = i / n;
    phase += (TAU * (220 * 8 ** u)) / SR;
    return (noise() * 0.9 + Math.sin(phase) * 0.35) * u ** 2.2;
  });
  return fadeTail(sweep(raw, 'bp', 250, 9000, 0.9).map((v) => v * 2), 0.015);
}

export function boom(seed = 8) {
  const noise = noiseSource(seed);
  let phase = 0;
  const raw = render(1.9, (t) => {
    phase += (TAU * (36 + 30 * Math.exp(-t / 0.18))) / SR;
    return Math.sin(phase) * Math.exp(-t / 0.75) * 0.95 + noise() * Math.exp(-t / 0.45) * 0.25;
  });
  return fadeTail(filter(raw, 'lp', 9000, 0.7), 0.1);
}

export function reverseCymbal(seconds, seed = 9) {
  const noise = noiseSource(seed);
  const raw = render(seconds, (t, i, n) => noise() * (i / n) ** 3);
  return fadeTail(sweep(raw, 'hp', 2500, 9000, 0.8).map((v) => v * 1.4), 0.012);
}

export function pop(freq) {
  let phase = 0;
  return fadeTail(render(0.22, (t) => {
    phase += (TAU * freq * (0.8 + 0.5 * (1 - Math.exp(-t / 0.02)))) / SR;
    return Math.sin(phase) * Math.exp(-t / 0.06) * Math.min(1, t / 0.001);
  }));
}

export function tick(seed = 10, freq = 3200) {
  const noise = noiseSource(seed);
  return filter(render(0.03, (t) => noise() * Math.exp(-t / 0.003)), 'bp', freq, 3).map((v) => v * 2.4);
}

export function swell(seconds, seed = 11) {
  const noise = noiseSource(seed);
  let phase = 0;
  const raw = render(seconds, (t, i, n) => {
    const u = i / n;
    phase += (TAU * (180 * 5 ** u)) / SR;
    return (noise() * 0.7 + Math.sin(phase) * 0.25) * u ** 2.4;
  });
  return fadeTail(sweep(raw, 'lp', 500, 9000, 0.8).map((v) => v * 1.6), 0.02);
}

export function thud() {
  let phase = 0;
  return fadeTail(render(0.32, (t) => {
    phase += (TAU * (48 + 44 * Math.exp(-t / 0.05))) / SR;
    return Math.sin(phase) * Math.exp(-t / 0.09);
  }));
}

export function sting() {
  const notes = [48, 60, 64, 67, 72, 76, 79, 84];
  const seconds = 2.8;
  const mix = new Float32Array(Math.round(seconds * SR));
  notes.forEach((n, k) => {
    const f = midi(n);
    const phases = [0.1 * k, 0.5 + 0.13 * k];
    const voice = render(seconds, (t) => {
      let sum = 0;
      [1, 1.004].forEach((r, v) => {
        phases[v] = (phases[v] + (f * r) / SR) % 1;
        sum += blepSaw(phases[v], (f * r) / SR);
      });
      return (sum / 2) * adsr(t, 0.4, 0.004, 0.35, 0.3, 2.2);
    });
    for (let i = 0; i < mix.length; i += 1) mix[i] += voice[i] * (k < 2 ? 0.36 : 0.2);
  });
  return filter(mix, 'lp', 6500, 0.7);
}

export function sparkle(seed = 12) {
  const noiseVal = noiseSource(seed);
  const notes = [96, 100, 103, 108, 112];
  const out = new Float32Array(Math.round(0.9 * SR));
  notes.forEach((n, k) => {
    const b = bell(midi(n), 0.5);
    const at = Math.round((k * 0.055 + (noiseVal() + 1) * 0.004) * SR);
    for (let i = 0; i < b.length && at + i < out.length; i += 1) out[at + i] += b[i] * 0.5;
  });
  return out;
}
