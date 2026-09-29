import { existsSync, mkdirSync, copyFileSync } from 'node:fs';
import path from 'node:path';
import { loadSpec, assertSpec } from '../lib/spec.mjs';
import { run as exec, ffmpeg } from '../lib/ffmpeg.mjs';
import { writeWav } from '../audio/dsp.mjs';
import { compose } from '../audio/score.mjs';
import { P } from '../lib/paths.mjs';

const TARGET = { I: -14, TP: -1.5, LRA: 7 };

export async function normalise(input, output) {
  const filter = `loudnorm=I=${TARGET.I}:TP=${TARGET.TP}:LRA=${TARGET.LRA}`;
  const { stderr } = await exec('ffmpeg', ['-hide_banner', '-nostats', '-i', input, '-af', `${filter}:print_format=json`, '-f', 'null', '-']);
  const stats = JSON.parse(stderr.slice(stderr.lastIndexOf('{'), stderr.lastIndexOf('}') + 1));
  const measured = `measured_I=${stats.input_i}:measured_TP=${stats.input_tp}:measured_LRA=${stats.input_lra}:measured_thresh=${stats.input_thresh}:offset=${stats.target_offset}`;
  await ffmpeg(['-i', input, '-af', `${filter}:${measured}:linear=true`, '-ar', '48000', '-c:a', 'pcm_s16le', output]);
  return stats;
}

export async function run({ flags }) {
  const spec = assertSpec(loadSpec());
  mkdirSync(P.out, { recursive: true });
  const custom = flags.track ? path.resolve(flags.track) : null;
  const raw = path.join(P.out, 'audio-raw.wav');
  const final = path.join(P.out, 'audio.wav');

  if (custom) {
    if (!existsSync(custom)) throw new Error(`--track file not found: ${custom}`);
    copyFileSync(custom, raw);
    console.log(`using supplied track ${custom}`);
  } else {
    const { L, R } = compose(spec);
    writeWav(raw, L, R);
    console.log(`synthesised ${(L.length / 48000).toFixed(2)}s at ${spec.meta.bpm} BPM`);
  }

  const stats = await normalise(raw, final);
  console.log(`loudnorm input ${stats.input_i} LUFS / ${stats.input_tp} dBTP -> target ${TARGET.I} LUFS / ${TARGET.TP} dBTP`);
  const image = path.join(P.out, 'audio-analysis.png');
  await ffmpeg(['-i', final, '-filter_complex', '[0:a]showspectrumpic=s=1600x420:legend=0:scale=log[s];[0:a]showwavespic=s=1600x180:colors=0x004AC6[w];[s][w]vstack', '-frames:v', '1', image]);
  console.log(`audio -> ${path.relative(process.cwd(), final)}  (inspect ${path.relative(process.cwd(), image)})`);
}
