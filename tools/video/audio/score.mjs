import { cueTimes } from '../lib/spec.mjs';
import { SR, filter, makeBus, midi, noiseSource, pingPong, place, reverb, rms, sendTo } from './dsp.mjs';
import * as inst from './instruments.mjs';

const CHORDS = {
  Am: { root: 33, pad: [57, 60, 64], arp: [69, 72, 76, 81] },
  C: { root: 36, pad: [60, 64, 67], arp: [72, 76, 79, 84] },
  G: { root: 31, pad: [55, 59, 62], arp: [67, 71, 74, 79] },
  F: { root: 29, pad: [53, 57, 60], arp: [65, 69, 72, 77] },
};

const BARS = [
  { chord: 'Am', kick: 'hook', bass: 'drone', pad: 0.45, arp: 0, hat: 0, clap: 'hook', bell: null },
  { chord: 'C', kick: 'four', bass: 'off', pad: 0.8, arp: 0.5, hat: 8, clap: 0, bell: null },
  { chord: 'G', kick: 'four', bass: 'off', pad: 0.8, arp: 0.65, hat: 8, clap: 24, bell: null },
  { chord: 'Am', kick: 'four', bass: 'off', pad: 0.85, arp: 0.7, hat: 8, clap: 24, bell: null },
  { chord: 'F', kick: 'four', bass: 'off', pad: 0.9, arp: 0.75, hat: 16, clap: 24, bell: [[0, 84], [1.5, 81], [2, 84], [3, 89]] },
  { chord: 'C', kick: 'four', bass: 'off', pad: 0.9, arp: 0.75, hat: 16, clap: 24, bell: [[0, 88], [1.5, 91], [2, 88], [3, 84]] },
  { chord: 'G', kick: 'build', bass: 'off', pad: 1, arp: 0.8, hat: 16, clap: 'roll', bell: null },
  { chord: 'C', kick: 'four', bass: 'off', pad: 1, arp: 0.85, hat: 16, clap: 24, bell: [[0.5, 88], [1, 91], [1.5, 96], [2.5, 91], [3, 88]] },
];

const ARP_STEPS = [0, 1, 2, 3, 2, 1, 2, 3];

export function compose(spec) {
  const { bpm, duration, beatsPerBar } = spec.meta;
  const bd = 60 / bpm;
  const tail = 1.2;
  const total = duration + tail;
  const drums = makeBus(total);
  const bed = makeBus(total);
  const fx = makeBus(total);
  const verbSend = new Float32Array(drums.n);
  const echoSend = new Float32Array(drums.n);
  const kickTimes = [];
  const noise = noiseSource(99);
  const bars = Math.ceil(duration / (bd * beatsPerBar));

  const drum = (buf, beat, gain, pan = 0, verb = 0) => {
    place(drums, buf, beat * bd, gain, pan);
    if (verb) sendTo(verbSend, buf, beat * bd, verb);
  };
  const bedNote = (buf, beat, gain, pan = 0, verb = 0, echo = 0) => {
    place(bed, buf, beat * bd, gain, pan);
    if (verb) sendTo(verbSend, buf, beat * bd, verb);
    if (echo) sendTo(echoSend, buf, beat * bd, echo);
  };
  const kickAt = (beat, gain = 1) => {
    drum(inst.kick(1), beat, gain * 0.78);
    kickTimes.push(beat * bd);
  };

  for (let bar = 0; bar < bars; bar += 1) {
    const cfg = BARS[Math.min(bar, BARS.length - 1)];
    const chord = CHORDS[cfg.chord];
    const b0 = bar * beatsPerBar;
    const barSeconds = bd * beatsPerBar;

    if (cfg.kick === 'hook') {
      kickAt(b0);
      kickAt(b0 + 2);
      drum(inst.clap(2, 0.9), b0 + 1, 0.55, 0, 0.12);
      drum(inst.clap(3, 1), b0 + 3, 0.6, 0, 0.12);
      for (let k = 0; k < 4; k += 1) drum(inst.snare(20 + k, 0.35 + k * 0.18), b0 + 3 + k * 0.25 + 0.001, 0.4);
    } else if (cfg.kick === 'build') {
      [0, 1, 2, 3].forEach((k) => kickAt(b0 + k, 0.9));
    } else {
      for (let k = 0; k < beatsPerBar; k += 1) kickAt(b0 + k);
    }

    if (cfg.bass === 'drone') {
      bedNote(inst.subNote(midi(chord.root), barSeconds), b0, 0.5);
    } else {
      for (let k = 0; k < beatsPerBar; k += 1) bedNote(inst.bassNote(midi(chord.root), bd * 0.42), b0 + k + 0.5, 0.62);
    }

    chord.pad.forEach((n, i) => bedNote(inst.pad(midi(n), barSeconds - 0.05, bar * 7 + i), b0, cfg.pad * 0.24, (i - 1) * 0.35, 0.3));

    if (cfg.arp) {
      ARP_STEPS.forEach((step, i) => {
        const beat = b0 + i * 0.5;
        const accent = i % 4 === 0 ? 1.15 : 0.85;
        bedNote(inst.pluck(midi(chord.arp[step] + (i % 8 === 7 ? 12 : 0))), beat, cfg.arp * 0.42 * accent, i % 2 ? 0.3 : -0.3, 0.14, 0.32);
      });
    }

    if (cfg.hat === 8) {
      for (let k = 0; k < beatsPerBar; k += 1) drum(inst.hat(false, 30 + k + bar), b0 + k + 0.5, 0.22, 0.2);
    } else if (cfg.hat === 16) {
      for (let k = 0; k < beatsPerBar * 4; k += 1) {
        const level = [0.11, 0.22, 0.14, 0.22][k % 4];
        drum(inst.hat(false, 40 + k + bar * 16), b0 + k * 0.25, level, k % 2 ? -0.2 : 0.2);
      }
      drum(inst.hat(true, 77 + bar), b0 + 3.5, 0.26, 0.25);
    }

    if (cfg.clap === 24) {
      drum(inst.clap(50 + bar, 1), b0 + 1, 0.55, 0, 0.16);
      drum(inst.clap(60 + bar, 1), b0 + 3, 0.55, 0, 0.16);
    } else if (cfg.clap === 'roll') {
      drum(inst.clap(70, 1), b0 + 1, 0.5, 0, 0.16);
      for (let k = 0; k < 4; k += 1) drum(inst.snare(80 + k, 0.4 + k * 0.1), b0 + 2 + k * 0.5, 0.4);
      for (let k = 0; k < 7; k += 1) drum(inst.snare(90 + k, 0.55 + k * 0.08), b0 + 3 + k * 0.125, 0.42);
    }

    (cfg.bell ?? []).forEach(([offset, note]) => bedNote(inst.bell(midi(note)), b0 + offset, 0.2, offset % 2 ? 0.35 : -0.35, 0.35, 0.3));
  }

  const fxAt = (buf, beat, gain, pan = 0, verb = 0) => {
    place(fx, buf, beat * bd, gain, pan);
    if (verb) sendTo(verbSend, buf, beat * bd, verb);
  };
  const popNotes = [880, 1046.5, 1318.5, 1568, 1174.7];
  let popIndex = 0;
  for (const cue of cueTimes(spec)) {
    const beat = cue.beat;
    if (cue.kind === 'hit') fxAt(inst.tick(100 + Math.round(beat), 2600), beat, 0.5);
    else if (cue.kind === 'boom') {
      fxAt(inst.boom(), beat, 0.75, 0, 0.1);
      fxAt(inst.reverseCymbal(bd * 2.4), beat - 2.4, 0.55);
      kickTimes.push(cue.t);
    } else if (cue.kind === 'riser') fxAt(inst.riser(cue.dur), beat, 0.5);
    else if (cue.kind === 'whoosh') fxAt(inst.whoosh(0.5, 200 + Math.round(beat * 10)), beat - 0.1 / bd, 0.5, (Math.round(beat) % 2 ? 1 : -1) * 0.4);
    else if (cue.kind === 'pop') {
      fxAt(inst.pop(popNotes[popIndex % popNotes.length]), beat, 0.32, ((popIndex % 3) - 1) * 0.45, 0.12);
      popIndex += 1;
    } else if (cue.kind === 'tick') fxAt(inst.tick(300 + Math.round(beat)), beat, 0.5);
    else if (cue.kind === 'type') {
      for (let t = 0; t < cue.dur; t += 0.052 + (noise() + 1) * 0.015) fxAt(inst.tick(400 + Math.round(t * 1000), 2000 + (noise() + 1) * 1500), beat + t / bd, 0.16);
    } else if (cue.kind === 'swell') fxAt(inst.swell(cue.dur), beat, 0.5);
    else if (cue.kind === 'sparkle') fxAt(inst.sparkle(Math.round(beat)), beat, 0.4, 0.2, 0.4);
    else if (cue.kind === 'thud') fxAt(inst.thud(), beat, 0.85);
    else if (cue.kind === 'sting') fxAt(inst.sting(), beat, 0.7, 0, 0.35);
  }

  const duck = new Float32Array(bed.n).fill(1);
  for (const kt of kickTimes) {
    const start = Math.round(kt * SR);
    for (let i = 0; i < 0.4 * SR && start + i < duck.length; i += 1) duck[start + i] = Math.min(duck[start + i], 1 - 0.6 * Math.exp(-i / SR / 0.11));
  }
  const gapFrom = Math.round((27.55 * bd) * SR);
  const gapTo = Math.round((27.95 * bd) * SR);
  for (let i = gapFrom; i < Math.min(gapTo, duck.length); i += 1) duck[i] *= Math.max(0.12, 1 - (i - gapFrom) / (gapTo - gapFrom));

  const n = drums.n;
  const L = new Float32Array(n);
  const R = new Float32Array(n);
  const [rl, rr] = reverb(verbSend);
  const [el, er] = pingPong(echoSend, bd * 0.75);
  const dryRms = rms(bed.L.map((v, i) => v * duck[i] + drums.L[i] + fx.L[i]));
  const wetGain = (0.32 * dryRms) / Math.max(1e-6, rms(rl));
  const echoGain = (0.22 * dryRms) / Math.max(1e-6, rms(el));
  for (let i = 0; i < n; i += 1) {
    L[i] = bed.L[i] * duck[i] + drums.L[i] + fx.L[i] + rl[i] * wetGain + el[i] * echoGain;
    R[i] = bed.R[i] * duck[i] + drums.R[i] + fx.R[i] + rr[i] * wetGain + er[i] * echoGain;
  }
  const hpL = filter(L, 'hp', 28, 0.7);
  const hpR = filter(R, 'hp', 28, 0.7);

  const keep = Math.round(duration * SR);
  const outL = new Float32Array(keep);
  const outR = new Float32Array(keep);
  const fadeSamples = Math.round(0.35 * SR);
  let peak = 1e-9;
  for (let i = 0; i < keep; i += 1) {
    const fade = i > keep - fadeSamples ? 0.5 * (1 + Math.cos((Math.PI * (i - (keep - fadeSamples))) / fadeSamples)) : 1;
    outL[i] = Math.tanh(hpL[i] * 1.15) * fade;
    outR[i] = Math.tanh(hpR[i] * 1.15) * fade;
    peak = Math.max(peak, Math.abs(outL[i]), Math.abs(outR[i]));
  }
  const norm = 0.7 / peak;
  for (let i = 0; i < keep; i += 1) {
    outL[i] *= norm;
    outR[i] *= norm;
  }
  return { L: outL, R: outR, kickTimes };
}
