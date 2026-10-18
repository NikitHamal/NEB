// Bakes Neby's performance for the reader act: one SVG per act-local frame, from the product's own
// avatar engine (neby-avatar.js) through the film rig (neb/tools/video/neby/neby_rig.mjs). The act
// plays the frames back exactly, so Neby is deterministic like everything else in the film.
//   node tools/bake-neby.mjs <neby_rig.mjs> <neby-avatar.js> public/neby/reader.json
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import readline from 'node:readline';

const [rigPath, avatarJs, out] = process.argv.slice(2);
const FPS = 60;
const FRAMES = 288; // two bars at 100 BPM

// Who Neby is in each beat (act-local frames): it rises listening, explains (talking), then smiles
// as the line on the page lights, and settles on a small success.
const SEGMENTS = [
  [0, 'listening-focus'],
  [140, 'talk'],
  [214, 'soft-smile'],
  [246, 'success'],
];
const TALK = ['talk-a', 'talk-b', 'talk-c'];
const BLINKS = [118, 196, 268];
const smooth = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

function keysAt(f) {
  // crossfade 16 f into each segment
  const weights = new Map();
  let prev = null;
  for (let i = 0; i < SEGMENTS.length; i++) {
    const [s, id] = SEGMENTS[i];
    if (f < s) break;
    const k = i === 0 ? 1 : smooth((f - s) / 16);
    if (prev) for (const [pid, w] of prev) weights.set(pid, (weights.get(pid) || 0) * 0 + w * (1 - k));
    const cur = id === 'talk' ? talkKeys(f) : [[id, 1]];
    const next = new Map(prev ? [...weights] : []);
    for (const [cid, w] of cur) next.set(cid, (next.get(cid) || 0) + w * k);
    prev = next;
    weights.clear();
    for (const [a, b] of next) weights.set(a, b);
  }
  return [...weights].filter(([, w]) => w > 0.001);
}
function talkKeys(f) {
  const step = 10;
  const i = Math.floor(f / step);
  const k = smooth((f % step) / 6);
  return [[TALK[i % 3], k], [TALK[(i + 2) % 3], 1 - k]];
}
function blinkAt(f) {
  for (const b of BLINKS) if (f >= b && f < b + 9) return 0.5 + 0.5 * Math.cos(((f - b) / 9) * Math.PI * 2);
  return 1;
}
function lookAt(f) {
  // looks down-left at the page while explaining, then back up at the reader
  const k = smooth((f - 150) / 30) * (1 - smooth((f - 236) / 24));
  return [-0.45 * k, 0.3 * k];
}

const rig = spawn('node', [rigPath, avatarJs], { stdio: ['pipe', 'pipe', 'inherit'] });
if (process.env.PRINT_KEYS) { for (const f of [0, 100, 145, 150, 160, 220, 250, 280]) console.log(f, JSON.stringify(keysAt(f))); process.exit(0); }
const rl = readline.createInterface({ input: rig.stdout });
const frames = [];
rl.on('line', (l) => {
  if (l.startsWith('ERR')) { console.error(l); process.exit(1); }
  // one decimal is far below a pixel at film size and quarters the file
  frames.push(l.replace(/(-?\d+\.\d)\d+/g, '$1'));
  if (frames.length === FRAMES) {
    fs.writeFileSync(out, JSON.stringify(frames));
    console.log(`bake-neby: ${FRAMES} frames -> ${out} (${(fs.statSync(out).size / 1e6).toFixed(1)} MB)`);
    rig.kill();
  }
});
for (let f = 0; f < FRAMES; f++) {
  rig.stdin.write(JSON.stringify({ keys: keysAt(f), t: (f / FPS) * 1000, blink: blinkAt(f), look: lookAt(f) }) + '\n');
}
