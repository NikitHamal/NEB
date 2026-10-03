import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { resolveChrome } from '../lib/chrome.mjs';
import { hasEncoder, version } from '../lib/ffmpeg.mjs';
import { loadSpec, validateSpec } from '../lib/spec.mjs';
import { P } from '../lib/paths.mjs';

export async function run() {
  const rows = [];
  const row = (name, ok, detail = '') => rows.push({ name, ok, detail });
  const attempt = async (name, fn) => {
    try {
      row(name, true, await fn());
    } catch (error) {
      row(name, false, error.message.split('\n')[0]);
    }
  };

  const major = Number(process.versions.node.split('.')[0]);
  row('node >= 22 (global WebSocket)', major >= 22, process.version);
  await attempt('ffmpeg', () => version('ffmpeg'));
  await attempt('ffprobe', () => version('ffprobe'));
  await attempt('ffmpeg has libx264 and aac', async () => {
    if (!(await hasEncoder('libx264')) || !(await hasEncoder('aac'))) throw new Error('libx264 and aac encoders are required');
    return 'ok';
  });
  await attempt('Chrome or Chromium', () => resolveChrome());

  const spec = loadSpec();
  const problems = validateSpec(spec);
  row('spec/launch.spec.json is valid', problems.length === 0, problems[0] ?? `${spec.timeline.length} scenes, ${spec.cues.length} cues`);

  const fonts = ['Poppins-Regular', 'Poppins-Medium', 'Poppins-SemiBold', 'Poppins-Bold', 'Poppins-ExtraBold', 'Poppins-Black'].map((n) => `${n}.ttf`);
  const missing = fonts.filter((f) => !existsSync(path.join(P.fonts, f)));
  row('Poppins weights vendored', missing.length === 0, missing.join(', ') || `${fonts.length} files`);
  row('Material Symbols subset present', existsSync(path.join(P.fonts, 'material-symbols-subset.woff2')), 'run "icons" to rebuild');

  await attempt('every timeline scene has an implementation', async () => {
    const { SCENES } = await import('../stage/scenes/index.js');
    const absent = spec.timeline.map((s) => s.id).filter((id) => !SCENES[id]);
    if (absent.length) throw new Error(`missing scenes: ${absent.join(', ')}`);
    return `${Object.keys(SCENES).length} scenes`;
  });

  await attempt('icons used by the spec exist in the font subset', async () => {
    const known = JSON.parse(readFileSync(path.join(P.fonts, 'icons.json'), 'utf8'));
    const used = [...JSON.stringify(spec).matchAll(/"(?:icon|ic)"\s*:\s*"([a-z0-9_]+)"/g)].map((m) => m[1]);
    const lacking = [...new Set(used)].filter((n) => !known.includes(n));
    if (lacking.length) throw new Error(`add to spec.icons and run "icons": ${lacking.join(', ')}`);
    return `${new Set(used).size} icons in use`;
  });

  await attempt('logo and JS engines come from the repo', async () => {
    for (const rel of ['img/n-logo-master.svg', 'js/blobatar.js', 'js/neb-art.js']) {
      if (!existsSync(path.join(P.site, rel))) throw new Error(`missing ${rel} in backend_python/web/static/web`);
    }
    return 'n-logo-master.svg, blobatar.js, neb-art.js';
  });

  const manifest = path.join(P.captures, 'manifest.json');
  if (existsSync(manifest)) {
    const items = JSON.parse(readFileSync(manifest, 'utf8')).items ?? [];
    const gaps = (spec.captures ?? []).filter((c) => !items.some((i) => i.id === c.id));
    row('screen captures present', gaps.length === 0, gaps.map((c) => c.id).join(', ') || `${items.length} captures`);
  } else {
    row('screen captures present', false, 'run "capture"');
  }

  for (const r of rows) console.log(`${r.ok ? 'ok  ' : 'FAIL'}  ${r.name}${r.detail ? `  (${r.detail})` : ''}`);
  if (rows.some((r) => !r.ok)) throw new Error('doctor found problems');
  console.log('\nall checks passed');
}
