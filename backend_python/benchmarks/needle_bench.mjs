#!/usr/bin/env node
/* Needle 2 (WASM) benchmark harness for NEBians Neby AI.
 * Loads the SAME engine+model shipped to the browser and runs it in Node
 * for reproducible load/init/latency/memory numbers.
 */
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const __dirname = dirname(fileURLToPath(import.meta.url));

const ASSET_DIR = join(__dirname, '..', 'web', 'static', 'web', 'js', 'needle2');
const GLUE_JS = join(ASSET_DIR, 'needle.js');
const WASM = join(ASSET_DIR, 'needle.wasm');
const MODEL = join(ASSET_DIR, 'needle2.cact');

const NEBY_TOOLS = JSON.stringify([
  { name: 'search_resources', description: 'Search for study resources on NEBians -- notes, past papers, textbooks, PDFs.', parameters: { type: 'object', properties: { query: { type: 'string', description: 'search keywords' }, subject: { type: 'string', description: 'subject name e.g. Mathematics, Physics, English' }, resource_type: { type: 'string', enum: ['PDF', 'Note', 'Video', 'Link', ''], description: 'optional type filter' } }, required: ['query'] } },
  { name: 'find_notes', description: 'Find study notes or past exam papers for a specific subject and grade on NEBians.', parameters: { type: 'object', properties: { subject: { type: 'string', description: 'subject name e.g. Mathematics, Physics, Chemistry' }, grade_level: { type: 'string', description: 'e.g. Class 11, Class 12, SEE' }, exam_type: { type: 'string', enum: ['Notes', 'Board', 'Final', 'SEE', 'Mock', 'Reference', ''], description: 'type of material' } }, required: [] } },
  { name: 'get_forum_posts', description: 'Get forum posts from the NEBians discussion forum.', parameters: { type: 'object', properties: { category: { type: 'string', description: 'category to filter e.g. Science, Math, Help, General' }, sort: { type: 'string', enum: ['recent', 'popular'], description: 'sort order' } }, required: [] } },
  { name: 'navigate_to', description: 'Navigate the user to a specific page on NEBians.', parameters: { type: 'object', properties: { page: { type: 'string', enum: ['home', 'library', 'forum', 'search', 'news', 'settings', 'bookmarks', 'upload', 'results', 'leaderboard', 'tools'], description: 'destination page' } }, required: ['page'] } },
  { name: 'get_subjects', description: 'List all available subjects on NEBians.', parameters: { type: 'object', properties: {}, required: [] } },
]);

const MAX_NEW_TOKENS = Number(process.env.MAX_TOKENS) || 256;
const QUERIES = [
  'find physics notes for class 12',
  'show me popular forum posts',
  'search for mathematics study resources',
  'take me to the library',
  'find chemistry past papers',
  'what subjects are available',
  'search for english textbooks',
];
const WARMUP = 'hello, can you search for some science notes for class 11 please';

function allocateCString(runtime, value) {
  const bytes = new TextEncoder().encode(value);
  const ptr = runtime._malloc(bytes.length + 1);
  runtime.HEAPU8.set(bytes, ptr);
  runtime.HEAPU8[ptr + bytes.length] = 0;
  return ptr;
}

function runOne(runtime, outPtr, query, maxNewTokens) {
  runtime._needle_reset();
  const qPtr = allocateCString(runtime, query);
  const start = process.hrtime.bigint();
  const rc = runtime._needle_complete(qPtr, maxNewTokens, outPtr, 16384);
  const end = process.hrtime.bigint();
  runtime._free(qPtr);
  const elapsed = Number(end - start) / 1e6;
  // NOTE: the browser worker ignores the return code; rc ~= bytes written
  // to the output buffer (0 on genuine failure). We read the buffer always.
  const outStr = runtime.UTF8ToString(outPtr);
  if (rc === 0 || !outStr) {
    console.error('  completion FAILED rc=', rc, 'query=', query, 'out=', JSON.stringify(outStr).slice(0, 120));
    return { ms: elapsed, estTok: 0, genChars: 0 };
  }
  let parsed = null;
  try { parsed = JSON.parse(outStr); } catch { parsed = null; }
  const genChars = outStr.length;
  const calls = parsed?.function_calls || [];
  const preview = calls.length ? calls.map((c) => c.name + '(' + JSON.stringify(c.arguments || {}) + ')').join(' | ') : '(empty call)';
  const estTok = genChars / 4;
  console.log(' ' + query.padEnd(52) + ' ' + String(elapsed.toFixed(0)).padStart(7) + '  ' + String(genChars).padStart(7) + '  ' + String((estTok / (elapsed / 1000)).toFixed(0)).padStart(9));
  console.log('      -> ' + preview + '  (conf=' + (parsed?.confidence ?? '-') + ') gen_chars=' + genChars);
  return { ms: elapsed, estTok, genChars };
}

async function main() {
  const mod = await import(GLUE_JS);
  const createNeedle = mod.default || mod;
  const wasmBytes = readFileSync(WASM);
  const modelBytes = readFileSync(MODEL);
  const glueBytes = readFileSync(GLUE_JS);
  const sizeMB = (b) => (b / (1024 * 1024)).toFixed(2) + ' MB';

  const t0 = process.hrtime.bigint();
  const runtime = await createNeedle({ wasmBinary: wasmBytes });
  const t1 = process.hrtime.bigint();

  const modelPtr = runtime._malloc(modelBytes.length);
  runtime.HEAPU8.set(modelBytes, modelPtr);
  const t2 = process.hrtime.bigint();
  const loadRc = runtime._needle_load(modelPtr, BigInt(modelBytes.length));
  const t3 = process.hrtime.bigint();
  if (loadRc !== 0) { console.error('model load FAILED rc=', loadRc); process.exit(2); }

  const sysPtr = allocateCString(runtime, '');
  const toolsPtr = allocateCString(runtime, NEBY_TOOLS);
  const initRc = runtime._needle_init(sysPtr, toolsPtr, 0);
  runtime._free(sysPtr); runtime._free(toolsPtr);
  const t4 = process.hrtime.bigint();
  if (initRc < 0) { console.error('tool init FAILED rc=', initRc); process.exit(2); }
  const outPtr = runtime._malloc(16384);
  const ms = (a, b) => Number(b - a) / 1e6;

  console.log('========================================================');
  console.log(' Needle 2 WASM benchmark - NEBians Neby AI');
  console.log('========================================================');
  console.log(' assets:');
  console.log('   needle.js      ' + sizeMB(glueBytes.length));
  console.log('   needle.wasm    ' + sizeMB(wasmBytes.length));
  console.log('   needle2.cact   ' + sizeMB(modelBytes.length) + '  (model)');
  console.log('   TOTAL transfer ' + sizeMB(glueBytes.length + wasmBytes.length + modelBytes.length));
  console.log(' engine+glue init : ' + ms(t0, t1).toFixed(1) + ' ms');
  console.log(' model load       : ' + ms(t2, t3).toFixed(1) + ' ms');
  console.log(' tool init        : ' + ms(t3, t4).toFixed(1) + ' ms');
  console.log(' cold start TOTAL : ' + ms(t0, t4).toFixed(1) + ' ms');
  const heapMB = (runtime.HEAPU8 && runtime.HEAPU8.buffer) ? (runtime.HEAPU8.buffer.byteLength / (1024 * 1024)) : 0;
  console.log(' wasm HEAP        : ' + heapMB.toFixed(1) + ' MB');
  console.log(' process RSS      : ' + (process.memoryUsage().rss / (1024 * 1024)).toFixed(1) + ' MB');
  console.log('');
  console.log(' warmup (first completion call)...');
  runOne(runtime, outPtr, WARMUP, MAX_NEW_TOKENS);
  console.log('');
  console.log(' per-query decode (single turn, independent like the site):');
  console.log('   query                                                    ms    out_len  est tok/s');
  const rows = [];
  for (const q of QUERIES) { rows.push(runOne(runtime, outPtr, q, MAX_NEW_TOKENS)); }
  console.log('');
  console.log(' ---------------------------------------------------');
  const lat = rows.map((r) => r.ms);
  const avg = lat.reduce((a, b) => a + b, 0) / lat.length;
  const sorted = [...lat].sort((a, b) => a - b);
  const p50 = sorted[Math.floor(sorted.length / 2)];
  const p95 = sorted[Math.ceil(sorted.length * 0.95) - 1];
  const max = Math.max(...lat); const min = Math.min(...lat);
  const toks = rows.map((r) => r.estTok);
  const tokAvg = toks.reduce((a, b) => a + b, 0) / toks.length;
  console.log(' queries            : ' + rows.length);
  console.log(' latency avg/min/max: ' + avg.toFixed(1) + ' / ' + min.toFixed(1) + ' / ' + max.toFixed(1) + ' ms');
  console.log(' latency p50/p95    : ' + p50.toFixed(1) + ' / ' + p95.toFixed(1) + ' ms');
  console.log(' est. decode        : ~' + tokAvg.toFixed(0) + ' tok/query @ ' + (tokAvg / (avg / 1000)).toFixed(0) + ' tok/s');
  console.log('========================================================');
}

main().catch((e) => { console.error('T_BENCH fatal:', e); process.exit(1); });
