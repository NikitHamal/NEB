import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { loadSpec } from '../lib/spec.mjs';
import { P } from '../lib/paths.mjs';

const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36';

export async function run() {
  const names = [...new Set(loadSpec().icons)].sort();
  const css = await (await fetch(`https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0..1,0&icon_names=${names.join(',')}&display=block`, { headers: { 'user-agent': UA } })).text();
  const url = css.match(/url\((https:[^)]+)\)/)?.[1];
  if (!url) throw new Error(`Google Fonts returned no font URL. Check the icon names.\n${css.slice(0, 300)}`);
  const font = Buffer.from(await (await fetch(url, { headers: { 'user-agent': UA } })).arrayBuffer());
  writeFileSync(path.join(P.fonts, 'material-symbols-subset.woff2'), font);
  writeFileSync(path.join(P.fonts, 'icons.json'), `${JSON.stringify(names)}\n`);
  console.log(`icon subset rebuilt: ${names.length} icons, ${(font.length / 1024).toFixed(1)} KB`);
}
