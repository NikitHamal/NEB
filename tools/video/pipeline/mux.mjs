import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { ffmpeg } from '../lib/ffmpeg.mjs';
import { loadSpec } from '../lib/spec.mjs';
import { P } from '../lib/paths.mjs';
import { videoPath } from './render.mjs';

export const deliverable = (aspect, draft) => path.join(draft ? P.out : P.dist, `nebians-launch-${aspect.replace(':', 'x')}${draft ? '-draft' : ''}.mp4`);

export async function run({ flags }) {
  const spec = loadSpec();
  const aspect = flags.aspect ?? '16:9';
  const draft = Boolean(flags.draft);
  const video = path.resolve(flags.video ?? videoPath(aspect, draft));
  const audio = path.resolve(flags.audio ?? path.join(P.out, 'audio.wav'));
  const target = path.resolve(flags.out ?? deliverable(aspect, draft));
  mkdirSync(path.dirname(target), { recursive: true });

  await ffmpeg([
    '-i', video, '-i', audio, '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2',
    '-t', String(spec.meta.duration), '-movflags', '+faststart', target,
  ]);
  console.log(`muxed -> ${path.relative(process.cwd(), target)}`);

  if (!draft) {
    const poster = path.join(P.dist, `nebians-launch-${aspect.replace(':', 'x')}-poster.png`);
    await ffmpeg(['-ss', String(spec.meta.poster ?? spec.meta.duration - 0.6), '-i', target, '-frames:v', '1', poster]);
    console.log(`poster -> ${path.relative(process.cwd(), poster)}`);
  }
}
