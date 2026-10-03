#!/usr/bin/env node
import { parseArgs } from './lib/args.mjs';

const COMMANDS = {
  doctor: ['./pipeline/doctor.mjs', 'run', 'check the toolchain, spec and assets'],
  sync: ['./pipeline/sync.mjs', 'run', 'pull brand tokens and copy from the NEBians repo (add --write to update the spec)'],
  drift: ['./pipeline/drift.mjs', 'run', 'compare the spec against the repo and the live site'],
  icons: ['./pipeline/icons.mjs', 'run', 'rebuild the Material Symbols subset from spec.icons'],
  capture: ['./pipeline/capture.mjs', 'run', 'screenshot the live site into assets/captures'],
  still: ['./pipeline/stills.mjs', 'still', 'render single frames (--t 0,1.5 | --beats 0,4 | --scene id)'],
  contact: ['./pipeline/stills.mjs', 'contact', 'render a labelled contact sheet (--count 12 | --scene id | --beats ...)'],
  render: ['./pipeline/render.mjs', 'run', 'render the video track (--draft for a fast preview)'],
  audio: ['./pipeline/audio.mjs', 'run', 'synthesise the soundtrack'],
  mux: ['./pipeline/mux.mjs', 'run', 'combine video and audio into the deliverables'],
  qa: ['./pipeline/qa.mjs', 'run', 'verify the deliverables'],
  all: ['./pipeline/all.mjs', 'run', 'sync, render, audio, mux, qa in order'],
};

function help() {
  console.log('NEBians launch video pipeline\n\nusage: node tools/video/cli.mjs <command> [flags]\n');
  for (const [name, [, , text]] of Object.entries(COMMANDS)) console.log(`  ${name.padEnd(8)} ${text}`);
  console.log('\nsee tools/video/README.md and docs/LAUNCH_VIDEO.md');
}

const [command, ...rest] = process.argv.slice(2);
if (!command || command === 'help' || command === '--help') {
  help();
  process.exit(command ? 0 : 1);
}
const entry = COMMANDS[command];
if (!entry) {
  console.error(`unknown command "${command}"\n`);
  help();
  process.exit(1);
}

try {
  const module = await import(entry[0]);
  await module[entry[1]](parseArgs(rest));
} catch (error) {
  console.error(`\n${command} failed: ${error.message}`);
  process.exit(1);
}
