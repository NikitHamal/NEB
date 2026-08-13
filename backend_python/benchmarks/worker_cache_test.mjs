// Needle worker asset-cache state machine test.
// Mocks IndexedDB + Cache Storage + fetch, loads the real needle.worker.js and
// verifies: run1 fetches once, run2 hits IDB, run3 works with network disabled.
// Usage: node benchmarks/worker_cache_test.mjs
// Validates needle.worker.js IndexedDB + CacheStorage + fetch caching logic
// under a mocked browser worker environment. No network actually happens if the
// IDB/cache layers work; a fake fetch is provided to simulate the first run.
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const BASE = '/home/user/NEB/backend_python/web/static/web/js/needle2';
const workerSrc = readFileSync(`${BASE}/needle.worker.js`, 'utf8');

// ── In-memory fake stores ────────────────────────────────────────────────
const idbStore = new Map();      // url -> Uint8Array
const cacheStore = new Map();    // url -> Uint8Array
let fetchCount = 0;

function makeFakeIdb() {
  const api = {
    open: (name) => {
      const req = { result: undefined };
      const db = {
        objectStoreNames: { contains: () => true },
        transaction: (store, mode) => {
          const tx = {
            objectStore: () => {
              const get = (key) => {
                const r = { result: idbStore.get(key) ?? null };
                queueMicrotask(() => { if (r.onsuccess) r.onsuccess(); });
                return r;
              };
              const put = (val, key) => {
                const r = {};
                idbStore.set(key, val);
                queueMicrotask(() => { if (tx.oncomplete) tx.oncomplete(); });
                return r;
              };
              return { get, put };
            },
          };
          return tx;
        },
      };
      req.result = db;
      queueMicrotask(() => { if (req.onsuccess) req.onsuccess({ target: { result: db } }); });
      return req;
    },
  };
  return api;
}

function makeFakeCaches() {
  return {
    open: async () => ({
      match: async (url) => cacheStore.has(url) ? new Response(cacheStore.get(url).slice().buffer) : null,
      put: async (url, response) => { cacheStore.set(url, new Uint8Array(await response.arrayBuffer())); },
    }),
  };
}

const context = {
  console,
  performance: { now: () => Date.now() },
  fetch: async (url) => {
    fetchCount += 1;
    const u = url.split('?')[0];
    const data = readFileSync(`${BASE}/${u.replace('./','')}`);
    return new Response(data.slice().buffer, { status: 200 });
  },
  Response,
  TextEncoder,
  Uint8Array,
  BigInt,
  JSON,
  Promise,
  setTimeout,
  Math,
  WebAssembly,
  globalThis: null,
};
context.globalThis = context;
context.self = context;
context.indexedDB = makeFakeIdb();
context.caches = makeFakeCaches();
context.importScripts = (path) => {
  // load needle.js into the same context via vm
  const glue = readFileSync(`${BASE}/needle.js`, 'utf8');
  vm.runInContext(glue, sandbox);
};

const sandbox = vm.createContext(context);
const messages = [];
context.postMessage = (m) => messages.push(m);
const listeners = {};
context.addEventListener = (type, fn) => { (listeners[type] ||= []).push(fn); };
// re-patch the init/run helpers to use the captured listener


vm.runInContext(workerSrc, sandbox);

function dispatch(obj) { (listeners['message'] || []).forEach(fn => fn({ data: obj })); }
function init() { messages.length = 0; dispatch({ type: 'initialize', tools: '[]', warmup: true }); }

function runQuery(q) {
  messages.length = 0;
  dispatch({ type: 'run', id: 1, query: q, tools: '[]', maxNewTokens: 64 });
}

await new Promise(r => setTimeout(r, 300));

// Run 1: first ever run → must fetch (network). Then populate IDB.
init();
await new Promise(r => setTimeout(r, 1500));
const run1Ready = messages.find(m => m.type === 'ready');
console.log('RUN1 (cold): fetchCount=', fetchCount, 'ready fromCache=', run1Ready && run1Ready.fromCache);
console.log('  IDB entries:', [...idbStore.keys()].join(', '));

// Run 2: identical "session" — should hit IDB (no new fetch).
const fetchBefore = fetchCount;
init();
await new Promise(r => setTimeout(r, 1500));
const run2Ready = messages.find(m => m.type === 'ready');
console.log('RUN2 (cached): new fetches=', fetchCount - fetchBefore, 'ready fromCache=', run2Ready && run2Ready.fromCache);
console.log('  model bytes in IDB:', (idbStore.get('./needle2.cact?v=3') || {length:0}).length);

// Run 3: clear fetch entirely; must still load from IDB only.
context.fetch = async () => { throw new Error('NETWORK DISABLED'); };
const fetchB3 = fetchCount;
init();
await new Promise(r => setTimeout(r, 1500));
const run3Ready = messages.find(m => m.type === 'ready');
console.log('RUN3 (offline, network disabled): ready fromCache=', run3Ready && run3Ready.fromCache, ' | OK:', !!run3Ready);

// Run a query offline.
runQuery('find physics notes');
await new Promise(r => setTimeout(r, 2000));
const res = messages.find(m => m.type === 'result');
console.log('OFFLINE QUERY result keys:', res ? Object.keys(res.result).join(',') : 'NONE', '| calls=', res ? res.result.function_calls.length : '-');
