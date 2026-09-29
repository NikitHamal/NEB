import { readFileSync } from 'node:fs';
import { P } from './paths.mjs';

export const CUE_KINDS = [
  'hit', 'boom', 'riser', 'whoosh', 'pop', 'tick', 'type', 'swell', 'sparkle', 'chord', 'sting', 'thud',
];

const HEX = /^#[0-9a-fA-F]{6}$/;

export function loadSpec(file = P.specFile) {
  return JSON.parse(readFileSync(file, 'utf8'));
}

export function derive(spec) {
  const { duration, fps, bpm, beatsPerBar } = spec.meta;
  const beatSeconds = 60 / bpm;
  return {
    beatSeconds,
    totalBeats: duration / beatSeconds,
    totalFrames: Math.round(duration * fps),
    barSeconds: beatSeconds * beatsPerBar,
  };
}

export function validateSpec(spec) {
  const problems = [];
  const add = (message) => problems.push(message);
  const { meta } = spec;
  if (!meta) return ['meta is missing'];
  for (const key of ['duration', 'fps', 'bpm', 'beatsPerBar']) {
    if (!(meta[key] > 0)) add(`meta.${key} must be a positive number`);
  }
  if (problems.length) return problems;
  const { totalBeats } = derive(spec);

  for (const [name, entry] of Object.entries(spec.palette ?? {})) {
    if (!HEX.test(entry.hex ?? '')) add(`palette.${name}.hex must be #RRGGBB, got "${entry.hex}"`);
  }

  const seen = new Set();
  let cursor = 0;
  for (const [i, scene] of (spec.timeline ?? []).entries()) {
    if (seen.has(scene.id)) add(`timeline[${i}] repeats scene id "${scene.id}"`);
    seen.add(scene.id);
    if (Math.abs(scene.from - cursor) > 1e-6) add(`timeline[${i}] "${scene.id}" starts at beat ${scene.from} but the previous scene ended at ${cursor}`);
    if (!(scene.to > scene.from)) add(`timeline[${i}] "${scene.id}" must end after it starts`);
    cursor = scene.to;
  }
  if (Math.abs(cursor - totalBeats) > 1e-6) {
    add(`timeline ends at beat ${cursor} but duration ${meta.duration}s at ${meta.bpm} BPM is ${totalBeats.toFixed(3)} beats`);
  }

  for (const [i, cue] of (spec.cues ?? []).entries()) {
    if (!CUE_KINDS.includes(cue.kind)) add(`cues[${i}] has unknown kind "${cue.kind}" (known: ${CUE_KINDS.join(', ')})`);
    if (!(cue.beat >= 0 && cue.beat <= totalBeats)) add(`cues[${i}] beat ${cue.beat} is outside 0-${totalBeats}`);
  }

  const stops = spec.background ?? [];
  for (const [i, stop] of stops.entries()) {
    if (!HEX.test(stop.base ?? '')) add(`background[${i}].base must be #RRGGBB`);
    for (const blob of stop.blobs ?? []) if (!HEX.test(blob)) add(`background[${i}] blob "${blob}" must be #RRGGBB`);
  }
  return problems;
}

export function assertSpec(spec) {
  const problems = validateSpec(spec);
  if (problems.length) throw new Error(`spec/launch.spec.json is invalid:\n  - ${problems.join('\n  - ')}`);
  return spec;
}

export function aspectSize(spec, aspect) {
  const size = spec.meta.aspects[aspect];
  if (!size) throw new Error(`unknown aspect "${aspect}" (known: ${Object.keys(spec.meta.aspects).join(', ')})`);
  return { width: size[0], height: size[1] };
}

export function cueTimes(spec) {
  const { beatSeconds } = derive(spec);
  return (spec.cues ?? []).map((cue) => ({ ...cue, t: cue.beat * beatSeconds, dur: (cue.beats ?? 0) * beatSeconds }));
}
