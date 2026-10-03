import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { run as exec, probe, ffmpeg } from '../lib/ffmpeg.mjs';
import { loadSpec, aspectSize } from '../lib/spec.mjs';
import { P } from '../lib/paths.mjs';
import { deliverable } from './mux.mjs';

const filterLog = async (file, args) => {
  const { stderr } = await exec('ffmpeg', ['-hide_banner', '-nostats', '-loglevel', 'info', '-i', file, ...args, '-f', 'null', '-']);
  return stderr;
};

export async function run({ flags }) {
  const spec = loadSpec();
  const aspect = flags.aspect ?? '16:9';
  const draft = Boolean(flags.draft);
  const file = path.resolve(flags.file ?? deliverable(aspect, draft));
  const { width, height } = aspectSize(spec, aspect);
  const info = await probe(file);
  const video = info.streams.find((s) => s.codec_type === 'video');
  const audio = info.streams.find((s) => s.codec_type === 'audio');
  const checks = [];
  const check = (name, ok, detail, level = 'fail') => checks.push({ name, ok, level: ok ? 'pass' : level, detail });
  const duration = Number(info.format.duration);

  check('container has video and audio', Boolean(video && audio), `${info.streams.map((s) => s.codec_name).join(', ')}`);
  check('duration matches spec', Math.abs(duration - spec.meta.duration) <= 0.05, `${duration.toFixed(3)}s vs ${spec.meta.duration}s`);
  if (video) {
    const expectFps = draft ? 30 : spec.meta.fps;
    const [n, d] = video.r_frame_rate.split('/').map(Number);
    check('frame size', draft || (video.width === width && video.height === height), `${video.width}x${video.height} (want ${width}x${height})`);
    check('frame rate', Math.abs(n / d - expectFps) < 0.01, `${(n / d).toFixed(2)} fps (want ${expectFps})`);
    check('codec is H.264 yuv420p', video.codec_name === 'h264' && video.pix_fmt === 'yuv420p', `${video.codec_name} ${video.pix_fmt}`);
    check('colour tagged bt709', video.color_space === 'bt709' && video.color_transfer === 'bt709' && video.color_primaries === 'bt709', `${video.color_space}/${video.color_transfer}/${video.color_primaries}`, 'warn');
  }
  if (audio) {
    check('audio is stereo 48 kHz', audio.channels === 2 && Number(audio.sample_rate) === 48000, `${audio.channels}ch ${audio.sample_rate}Hz`);
    check('audio length matches video', Math.abs(Number(audio.duration) - duration) < 0.1, `${Number(audio.duration).toFixed(3)}s`, 'warn');
  }
  const megabytes = Number(info.format.size) / 1e6;
  check('file size is share-friendly (< 25 MB)', megabytes < 25, `${megabytes.toFixed(1)} MB`, 'warn');

  const black = await filterLog(file, ['-vf', 'blackdetect=d=0.08:pix_th=0.05', '-an']);
  const blackSpans = [...black.matchAll(/black_start:([\d.]+) black_end:([\d.]+)/g)].map((m) => [Number(m[1]), Number(m[2])]);
  check('no black frames', blackSpans.length === 0, blackSpans.length ? blackSpans.map(([a, b]) => `${a}-${b}s`).join(', ') : 'none');

  const freeze = await filterLog(file, ['-vf', 'freezedetect=n=0.001:d=0.4', '-an']);
  const freezes = [...freeze.matchAll(/freeze_start: ([\d.]+)/g)].map((m) => Number(m[1]));
  check('no frozen picture', freezes.length === 0, freezes.length ? `frozen from ${freezes.map((f) => `${f.toFixed(2)}s`).join(', ')}` : 'none', 'warn');

  if (audio) {
    const loud = await filterLog(file, ['-af', 'ebur128=peak=true', '-vn']);
    const summary = loud.slice(loud.lastIndexOf('Summary:'));
    const lufs = Number(summary.match(/I:\s+(-?[\d.]+) LUFS/)?.[1]);
    const peak = Number(summary.match(/Peak:\s+(-?[\d.]+) dBFS/)?.[1]);
    check('loudness near -14 LUFS', Number.isFinite(lufs) && lufs > -16 && lufs < -12, `${lufs} LUFS`, 'warn');
    check('true peak under -1 dBFS', Number.isFinite(peak) && peak <= -0.9, `${peak} dBFS`);
    const silence = await filterLog(file, ['-af', 'silencedetect=n=-50dB:d=0.35', '-vn']);
    const gaps = [...silence.matchAll(/silence_start: ([\d.]+)/g)].map((m) => Number(m[1]));
    check('no dead air', gaps.length === 0, gaps.length ? `silence from ${gaps.map((g) => `${g.toFixed(2)}s`).join(', ')}` : 'none', 'warn');
  }

  const failed = checks.filter((c) => c.level === 'fail');
  const warned = checks.filter((c) => c.level === 'warn');
  for (const c of checks) console.log(`${{ pass: 'PASS', warn: 'WARN', fail: 'FAIL' }[c.level]}  ${c.name}  (${c.detail})`);
  if (!draft) {
    const report = path.join(P.dist, `qa-report-${aspect.replace(':', 'x')}.json`);
    writeFileSync(report, `${JSON.stringify({ file: path.basename(file), checks }, null, 2)}\n`);
    const sheet = path.join(P.dist, `nebians-launch-${aspect.replace(':', 'x')}-contact.png`);
    const step = spec.meta.duration / 12;
    await ffmpeg(['-i', file, '-vf', `fps=1/${step.toFixed(4)},scale=480:-1,tile=4x3:padding=6:margin=6:color=0x111111`, '-frames:v', '1', sheet]);
    console.log(`report -> ${path.relative(process.cwd(), report)}\ncontact sheet -> ${path.relative(process.cwd(), sheet)}`);
  }
  console.log(`\n${checks.length - failed.length - warned.length} passed, ${warned.length} warnings, ${failed.length} failed`);
  if (failed.length) throw new Error('QA failed');
}
