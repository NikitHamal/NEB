import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { once } from 'node:events';
import path from 'node:path';
import { openStage, seekAndShot } from '../lib/session.mjs';
import { loadSpec } from '../lib/spec.mjs';
import { num } from '../lib/args.mjs';
import { P } from '../lib/paths.mjs';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export function frameTimes({ from, to, fps, samples, shutter, duration }) {
  const frames = Math.round((to - from) * fps);
  const at = (frame, k) => {
    const base = from + frame / fps;
    if (samples === 1) return Math.min(duration - 1e-4, base);
    const offset = ((k + 0.5) / samples - 0.5) * (shutter / fps);
    return Math.min(duration - 1e-4, Math.max(0, base + offset));
  };
  return { frames, at };
}

export function videoFilter({ samples, fps, grain }) {
  const chain = [];
  if (samples > 1) chain.push(`tmix=frames=${samples}`, `select='eq(mod(n\\,${samples})\\,${samples - 1})'`, `setpts=N/(${fps}*TB)`);
  if (grain > 0) chain.push(`noise=alls=${grain}:allf=t`);
  chain.push('scale=out_color_matrix=bt709:out_range=tv', 'format=yuv420p');
  return chain.join(',');
}

export function encodeArgs({ fps, samples, grain, crf, preset, out }) {
  return [
    '-y', '-hide_banner', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(fps * samples), '-c:v', 'png', '-i', '-',
    '-vf', videoFilter({ samples, fps, grain }), '-r', String(fps), '-an',
    '-c:v', 'libx264', '-preset', preset, '-crf', String(crf), '-profile:v', 'high', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-movflags', '+faststart', out,
  ];
}

export const videoPath = (aspect, draft) => path.join(P.out, `video-${aspect.replace(':', 'x')}${draft ? '-draft' : ''}.mp4`);

export async function run({ flags }) {
  const spec = loadSpec();
  const draft = Boolean(flags.draft);
  const aspect = flags.aspect ?? '16:9';
  const duration = spec.meta.duration;
  const fps = num(flags.fps, draft ? 30 : spec.meta.fps);
  const samples = num(flags.samples, draft ? 1 : 3);
  const shutter = num(flags.shutter, 0.5);
  const scale = num(flags.scale, draft ? 0.5 : 1);
  const workers = num(flags.workers, draft ? 1 : 2);
  const from = num(flags.from, 0);
  const to = num(flags.to, duration);
  const grain = num(flags.grain, draft ? 0 : 1.5);
  const out = path.resolve(flags.out ?? videoPath(aspect, draft));
  mkdirSync(path.dirname(out), { recursive: true });

  const { frames, at } = frameTimes({ from, to, fps, samples, shutter, duration });
  const total = frames * samples;
  const stage = await openStage({ aspect, scale, workers });
  const encoder = spawn('ffmpeg', encodeArgs({ fps, samples, grain, crf: num(flags.crf, draft ? 24 : 15), preset: flags.preset ?? (draft ? 'veryfast' : 'slow'), out }), { stdio: ['pipe', 'inherit', 'inherit'] });
  const encoderDone = new Promise((resolve, reject) => {
    encoder.once('error', reject);
    encoder.once('close', (code) => (code === 0 ? resolve() : reject(new Error(`ffmpeg exited with ${code}`))));
  });
  encoder.stdin.on('error', () => {});

  console.log(`rendering ${frames} frames @ ${fps}fps x${samples} samples, ${stage.width * scale}x${stage.height * scale}, ${workers} worker(s) -> ${path.relative(process.cwd(), out)}`);
  const results = new Map();
  let next = 0;
  let written = 0;
  let failure = null;
  const started = Date.now();

  const drain = async () => {
    while (results.has(written)) {
      const buffer = results.get(written);
      results.delete(written);
      written += 1;
      if (!encoder.stdin.write(buffer)) await once(encoder.stdin, 'drain');
      if (written % 30 === 0 || written === total) {
        const done = written / total;
        const elapsed = (Date.now() - started) / 1000;
        process.stdout.write(`\r  ${(done * 100).toFixed(1)}%  ${written}/${total}  ${elapsed.toFixed(0)}s elapsed  ~${(elapsed / done - elapsed).toFixed(0)}s left   `);
      }
    }
  };

  const loop = async (page) => {
    while (!failure) {
      const index = next;
      next += 1;
      if (index >= total) return;
      while (index - written > 24 && !failure) await sleep(4);
      try {
        const frame = Math.floor(index / samples);
        results.set(index, await seekAndShot(page, at(frame, index % samples), { format: 'png', fast: true }));
        await drain();
      } catch (error) {
        failure = error;
      }
    }
  };

  try {
    await Promise.all(stage.pages.map(loop));
    if (failure) throw failure;
    await drain();
    encoder.stdin.end();
    await encoderDone;
    console.log(`\ndone in ${((Date.now() - started) / 1000).toFixed(0)}s -> ${path.relative(process.cwd(), out)}`);
  } catch (error) {
    encoder.kill('SIGKILL');
    throw error;
  } finally {
    await stage.close();
  }
}
