import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import path from 'node:path';
import { openStage, seekAndShot } from '../lib/session.mjs';
import { derive } from '../lib/spec.mjs';
import { ffmpeg } from '../lib/ffmpeg.mjs';
import { list, num } from '../lib/args.mjs';
import { P } from '../lib/paths.mjs';

function resolveTimes(spec, flags) {
  const { beatSeconds, totalBeats } = derive(spec);
  if (flags.t) return list(flags.t).map(Number);
  if (flags.beats) return list(flags.beats).map((b) => Number(b) * beatSeconds);
  if (flags.count) {
    const n = num(flags.count, 12);
    return Array.from({ length: n }, (_, i) => ((i + 0.5) / n) * totalBeats * beatSeconds);
  }
  if (flags.scene) {
    const entry = spec.timeline.find((s) => s.id === flags.scene);
    if (!entry) throw new Error(`unknown scene "${flags.scene}"`);
    const n = num(flags.count, 8);
    return Array.from({ length: n }, (_, i) => (entry.from + ((i + 0.5) / n) * (entry.to - entry.from)) * beatSeconds);
  }
  return [0, 1, 2, 3, 5, 8, 11, 14].map((s) => Math.min(s, spec.meta.duration - 0.01));
}

async function shoot(flags, label) {
  const aspect = flags.aspect ?? '16:9';
  const scale = num(flags.scale, label ? 0.5 : 1);
  const stage = await openStage({ aspect, scale });
  try {
    const times = resolveTimes(stage.spec, flags);
    const dir = path.resolve(flags.out ?? path.join(P.out, label ? 'contact' : 'stills'));
    rmSync(dir, { recursive: true, force: true });
    mkdirSync(dir, { recursive: true });
    const files = [];
    for (const [i, t] of times.entries()) {
      if (label) await stage.page.evaluate(`window.__label(${JSON.stringify(`${t.toFixed(2)}s  b${(t / stage.spec.meta.duration * 32).toFixed(2)}`)})`);
      const buf = await seekAndShot(stage.page, t, { format: 'png' });
      const file = path.join(dir, `s_${String(i).padStart(3, '0')}.png`);
      writeFileSync(file, buf);
      files.push({ file, t });
    }
    return { dir, files, stage, times };
  } catch (error) {
    await stage.close();
    throw error;
  }
}

export async function still({ flags }) {
  const { files, stage } = await shoot(flags, false);
  await stage.close();
  for (const f of files) console.log(`${f.t.toFixed(3)}s -> ${path.relative(process.cwd(), f.file)}`);
}

export async function contact({ flags }) {
  const { dir, files, stage } = await shoot(flags, true);
  await stage.close();
  const cols = num(flags.cols, 4);
  const rows = Math.ceil(files.length / cols);
  const out = path.resolve(flags.sheet ?? path.join(P.out, 'contact-sheet.png'));
  const width = num(flags.width, 640);
  await ffmpeg(['-framerate', '1', '-i', path.join(dir, 's_%03d.png'), '-vf', `scale=${width}:-1,tile=${cols}x${rows}:padding=8:margin=8:color=0x111111`, '-frames:v', '1', out]);
  console.log(`contact sheet (${files.length} frames) -> ${path.relative(process.cwd(), out)}`);
}

export { shoot };
export const run = still;
