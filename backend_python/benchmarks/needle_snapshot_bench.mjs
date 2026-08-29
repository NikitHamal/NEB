#!/usr/bin/env node
import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const root = dirname(fileURLToPath(import.meta.url));
const assets = join(root, '..', 'web', 'static', 'web', 'js', 'needle2');
const gluePath = join(assets, 'needle.js');
const wasmBytes = readFileSync(join(assets, 'needle.wasm'));
const modelBytes = readFileSync(join(assets, 'needle2.cact'));
const createNeedleModule = await import(gluePath);
const createNeedle = createNeedleModule.default || createNeedleModule;

const tools = JSON.stringify([
  { name: 'search_resources', description: 'Search for study resources on NEBians -- notes, past papers, textbooks, PDFs.', parameters: { type: 'object', properties: { query: { type: 'string', description: 'search keywords' }, subject: { type: 'string', description: 'subject name e.g. Mathematics, Physics, English' }, resource_type: { type: 'string', enum: ['PDF', 'Note', 'Past Paper', 'Textbook', 'Video', 'Link', ''], description: 'optional type filter' } }, required: ['query'] } },
  { name: 'find_notes', description: 'Find study notes or past exam papers for a specific subject and grade on NEBians.', parameters: { type: 'object', properties: { subject: { type: 'string', description: 'subject name e.g. Mathematics, Physics, Chemistry' }, grade_level: { type: 'string', description: 'e.g. Class 11, Class 12, SEE' }, exam_type: { type: 'string', enum: ['Notes', 'Board', 'Final', 'SEE', 'Mock', 'Reference', ''], description: 'type of material' } }, required: [] } },
  { name: 'get_forum_posts', description: 'Get forum posts from the NEBians discussion forum.', parameters: { type: 'object', properties: { category: { type: 'string', description: 'category to filter e.g. Science, Math, Help, General' }, sort: { type: 'string', enum: ['recent', 'popular'], description: 'sort order' } }, required: [] } },
  { name: 'navigate_to', description: 'Navigate the user to a specific page on NEBians.', parameters: { type: 'object', properties: { page: { type: 'string', enum: ['home', 'library', 'forum', 'search', 'news', 'settings', 'bookmarks', 'upload', 'results', 'leaderboard', 'tools'], description: 'destination page' } }, required: ['page'] } },
  { name: 'get_subjects', description: 'List all available subjects on NEBians.', parameters: { type: 'object', properties: {}, required: [] } },
  { name: 'generate_p5_art', description: 'Generate dynamic, interactive 2D/3D paintings, drawings, and generative art using p5.js canvas.', parameters: { type: 'object', properties: { prompt: { type: 'string', description: 'art description or topic e.g. cosmic nebula, flow field, mandala, sunset wave' }, style: { type: 'string', enum: ['generative', 'fractal', 'landscape', 'pattern', 'animated', 'abstract', ''], description: 'artistic technique' }, color_palette: { type: 'string', enum: ['vibrant', 'neon', 'pastel', 'monochrome', 'cyberpunk', 'warm', 'cool', ''], description: 'color scheme' }, complexity: { type: 'string', enum: ['low', 'medium', 'high', 'extreme', ''], description: 'level of visual detail' }, code: { type: 'string', description: 'optional custom p5.js sketch code' } }, required: ['prompt'] } },
]);

const cases = [
  ['find physics notes for class 12', ['search_resources', 'find_notes'], (a) => a.subject === 'Physics' && JSON.stringify(a).includes('12')],
  ['show me popular forum posts', ['get_forum_posts'], (a) => a.sort === 'popular'],
  ['search for mathematics study resources', ['search_resources'], (a) => /math/i.test((a.query || '') + (a.subject || ''))],
  ['take me to the library', ['navigate_to'], (a) => a.page === 'library'],
  ['find chemistry past papers', ['search_resources', 'find_notes'], (a) => /chemistry/i.test(JSON.stringify(a)) && /past paper|board/i.test(JSON.stringify(a))],
  ['what subjects are available', ['get_subjects'], () => true],
  ['search for english textbooks', ['search_resources'], (a) => /english/i.test(JSON.stringify(a)) && /textbook/i.test(JSON.stringify(a))],
  ['paint a glowing cosmic nebula with p5js', ['generate_p5_art'], (a) => Boolean(a.prompt)],
];

function now() {
  return process.hrtime.bigint();
}

function elapsed(start, end) {
  return Number(end - start) / 1e6;
}

function cstring(runtime, value) {
  const bytes = new TextEncoder().encode(value);
  const pointer = runtime._malloc(bytes.length + 1);
  runtime.HEAPU8.set(bytes, pointer);
  runtime.HEAPU8[pointer + bytes.length] = 0;
  return pointer;
}

async function coldRuntime() {
  const started = now();
  const runtime = await createNeedle({ wasmBinary: wasmBytes });
  const modelPointer = runtime._malloc(modelBytes.length);
  runtime.HEAPU8.set(modelBytes, modelPointer);
  if (runtime._needle_load(modelPointer, BigInt(modelBytes.length)) !== 0) throw new Error('model load failed');
  const systemPointer = cstring(runtime, '');
  const toolsPointer = cstring(runtime, tools);
  if (runtime._needle_init(systemPointer, toolsPointer, 0) < 0) throw new Error('tool init failed');
  runtime._free(systemPointer);
  runtime._free(toolsPointer);
  const outputPointer = runtime._malloc(16384);
  return { runtime, outputPointer, milliseconds: elapsed(started, now()) };
}

function complete(runtime, outputPointer, query) {
  runtime._needle_reset();
  const queryPointer = cstring(runtime, query);
  const started = now();
  const written = runtime._needle_complete(queryPointer, 128, outputPointer, 16384);
  const milliseconds = elapsed(started, now());
  runtime._free(queryPointer);
  if (written <= 0) throw new Error('completion failed for ' + query);
  const raw = runtime.UTF8ToString(outputPointer);
  return { raw, parsed: JSON.parse(raw), milliseconds };
}

const cold = await coldRuntime();
const snapshotPath = join(tmpdir(), 'nebians-needle2-' + process.pid + '.snapshot');
const saveStarted = now();
const snapshot = cold.runtime.HEAPU8.slice();
writeFileSync(snapshotPath, snapshot);
const saveMs = elapsed(saveStarted, now());

const restoreStarted = now();
const diskSnapshot = readFileSync(snapshotPath);
const restoredRuntime = await createNeedle({ wasmBinary: wasmBytes });
restoredRuntime._malloc(diskSnapshot.length);
restoredRuntime.HEAPU8.set(diskSnapshot);
const restoreMs = elapsed(restoreStarted, now());
unlinkSync(snapshotPath);

function semanticResult(value) {
  const copy = { ...value };
  delete copy.prefill_tps;
  delete copy.decode_tps;
  delete copy.peak_ram_mb;
  return JSON.stringify(copy);
}

let identical = 0;
let correctRoutes = 0;
let groundedArguments = 0;
let reasoningFields = 0;
let generatedReasoning = 0;
const latencies = [];
for (const [query, acceptedTools, validateArguments] of cases) {
  const baseline = complete(cold.runtime, cold.outputPointer, query);
  const restored = complete(restoredRuntime, cold.outputPointer, query);
  const firstCall = restored.parsed.function_calls?.[0];
  const tool = firstCall?.name || '(empty)';
  const same = semanticResult(baseline.parsed) === semanticResult(restored.parsed);
  const correct = acceptedTools.includes(tool);
  const grounded = correct && validateArguments(firstCall?.arguments || {});
  if (same) identical += 1;
  if (correct) correctRoutes += 1;
  if (grounded) groundedArguments += 1;
  if (Object.hasOwn(restored.parsed, 'reasoning')) reasoningFields += 1;
  if (restored.parsed.reasoning) generatedReasoning += 1;
  latencies.push(restored.milliseconds);
  console.log(`${same ? 'PASS' : 'FAIL'}  ${query.padEnd(46)} ${restored.milliseconds.toFixed(0).padStart(5)} ms  ${tool}`);
}

const average = latencies.reduce((total, value) => total + value, 0) / latencies.length;
const sorted = [...latencies].sort((a, b) => a - b);
const p50 = sorted[Math.floor(sorted.length / 2)];
const p95 = sorted[Math.ceil(sorted.length * 0.95) - 1];
const mib = (bytes) => (bytes / (1024 * 1024)).toFixed(2);

console.log('\n========================================================');
console.log(' Needle 2 persisted-runtime benchmark');
console.log('========================================================');
console.log(` cold load + tool init       : ${cold.milliseconds.toFixed(1)} ms`);
console.log(` snapshot save (memory+disk) : ${saveMs.toFixed(1)} ms`);
console.log(` snapshot restore (disk)     : ${restoreMs.toFixed(1)} ms`);
console.log(` relaunch reduction          : ${((1 - restoreMs / cold.milliseconds) * 100).toFixed(1)}%`);
console.log(` runtime snapshot            : ${mib(snapshot.length)} MB`);
console.log(` model file                  : ${mib(modelBytes.length)} MB`);
console.log(` Android APK engine assets   : ${mib(wasmBytes.length + readFileSync(gluePath).length)} MB (model excluded)`);
console.log(` restored output equivalence : ${identical}/${cases.length}`);
console.log(` expected tool routing       : ${correctRoutes}/${cases.length}`);
console.log(` grounded key arguments      : ${groundedArguments}/${cases.length}`);
console.log(` reasoning field exposed     : ${reasoningFields}/${cases.length}`);
console.log(` generated reasoning trace   : ${generatedReasoning}/${cases.length}`);
console.log(` restored decode avg/p50/p95 : ${average.toFixed(1)} / ${p50.toFixed(1)} / ${p95.toFixed(1)} ms`);
console.log('========================================================');

if (identical !== cases.length || correctRoutes !== cases.length || groundedArguments !== cases.length || reasoningFields !== cases.length) process.exitCode = 1;
