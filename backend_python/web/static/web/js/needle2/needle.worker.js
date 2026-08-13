/* global createNeedle */

importScripts("./needle.js");

/* Assets are served as binary files (needle.wasm + needle2.cact) and cached
   locally so the ~13 MB model is downloaded over the network exactly ONCE per
   browser, then reused on every later visit — no re-download on refresh, and
   reads on mobile come from fast local storage instead of a second network
   fetch (which is what made cold loads take 40-50s on phones).

   Caching layering (fastest first):
     1. IndexedDB      — primary store for the model bytes. Browsers keep IDB
                         blobs on disk with no quota pressure for ~13 MB, and
                         reads are synchronous-ish (no network, no HTTP).
     2. Cache Storage  — legacy layer from the previous pass, kept so users who
                         already have v2 bytes cached can migrate instantly
                         instead of re-fetching. Also a fallback if IDB is
                         unavailable (e.g. private mode / quota errors).
     3. Network fetch  — only when neither store has the bytes (true first run).

   Bump ASSET_VERSION + the ?v= query when the model or engine changes so every
   browser re-fetches exactly once. */

var ASSET_VERSION = "needle2-assets-v3";
var WASM_URL = "./needle.wasm?v=3";
var CACT_URL = "./needle2.cact?v=3";
var IDB_NAME = "neby-assets";
var IDB_STORE = "assets";

var moduleInstance = null;
var loadingPromise = null;
var loadedTools = null;
var outputPointer = 0;
var loadSeconds = 0;
/* true when every asset byte came from local storage (no network was hit) */
var fromCache = true;

function postError(error, id) {
  self.postMessage({
    type: "error",
    ...(id === undefined ? {} : { id }),
    message: error instanceof Error ? error.message : String(error),
  });
}

function fetchBytes(url) {
  return fetch(url).then(function (response) {
    if (!response.ok) {
      throw new Error("failed to fetch " + url + ": " + response.status);
    }
    return response.arrayBuffer().then(function (buffer) {
      return new Uint8Array(buffer);
    });
  });
}

/* ── IndexedDB layer ─────────────────────────────────────────────────────── */

var idbPromise = null;

function openIdb() {
  if (idbPromise) return idbPromise;
  idbPromise = new Promise(function (resolve, reject) {
    var req = indexedDB.open(IDB_NAME, 1);
    req.onupgradeneeded = function (e) {
      var db = e.target.result;
      if (!db.objectStoreNames.contains(IDB_STORE)) {
        db.createObjectStore(IDB_STORE); // key = asset url string
      }
    };
    req.onsuccess = function () { resolve(req.result); };
    req.onerror = function () { reject(req.error); };
  });
  return idbPromise;
}

function idbGet(key) {
  return openIdb().then(
    function (db) {
      return new Promise(function (resolve) {
        try {
          var tx = db.transaction(IDB_STORE, "readonly");
          var req = tx.objectStore(IDB_STORE).get(key);
          req.onsuccess = function () { resolve(req.result || null); };
          req.onerror = function () { resolve(null); };
        } catch (e) { resolve(null); }
      });
    },
    function () { return null; }
  );
}

function idbPut(key, bytes) {
  return openIdb().then(
    function (db) {
      return new Promise(function (resolve) {
        try {
          var tx = db.transaction(IDB_STORE, "readwrite");
          tx.objectStore(IDB_STORE).put(bytes, key);
          tx.oncomplete = function () { resolve(true); };
          tx.onerror = function () { resolve(false); };
        } catch (e) { resolve(false); }
      });
    },
    function () { return false; }
  );
}

/* ── Cache Storage layer (legacy + fallback) ─────────────────────────────── */

function cacheGet(url) {
  return caches.open(ASSET_VERSION).then(function (cache) {
    return cache.match(url).then(function (cached) {
      if (!cached) return null;
      return cached.arrayBuffer().then(function (buf) {
        return new Uint8Array(buf);
      });
    });
  }).catch(function () { return null; });
}

function cachePut(url, bytes) {
  return caches.open(ASSET_VERSION).then(function (cache) {
    return cache.put(url, new Response(bytes.slice().buffer, {
      headers: { "Content-Type": "application/octet-stream" },
    }));
  }).catch(function () { /* non-fatal */ });
}

/* Resolve one asset: IndexedDB → Cache Storage → network. Returns bytes and
   flips `fromCache` to false the moment any byte came over the wire. */
async function loadAsset(url) {
  var idb = await idbGet(url);
  if (idb) return idb;

  var cache = await cacheGet(url);
  if (cache) {
    // Migrate the old Cache Storage copy into IDB so future loads skip HTTP.
    await idbPut(url, cache);
    return cache;
  }

  fromCache = false;
  var bytes = await fetchBytes(url);
  // Await the IDB write so the model is guaranteed persisted before we report
  // "ready" — otherwise a fast page close could drop it and force a re-download.
  // (13 MB IDB write is tens of ms; far cheaper than re-fetching on a phone.)
  await idbPut(url, bytes);
  // Secondary best-effort copy in Cache Storage for older-browser fallback.
  cachePut(url, bytes);
  return bytes;
}

async function ensureModel() {
  if (moduleInstance) return moduleInstance;

  loadingPromise ||= (async () => {
    self.postMessage({ type: "status", status: "loading" });
    const startedAt = performance.now();

    const [wasmBytes, modelBytes] = await Promise.all([
      loadAsset(WASM_URL),
      loadAsset(CACT_URL),
    ]);

    const runtime = await createNeedle({ wasmBinary: wasmBytes });
    const modelPointer = runtime._malloc(modelBytes.length);
    runtime.HEAPU8.set(modelBytes, modelPointer);

    if (runtime._needle_load(modelPointer, BigInt(modelBytes.length)) !== 0) {
      throw new Error("model load failed");
    }

    outputPointer = runtime._malloc(16384);
    moduleInstance = runtime;

    loadSeconds = (performance.now() - startedAt) / 1000;

    return runtime;
  })();

  return loadingPromise;
}

function initializeTools(runtime, tools) {
  if (loadedTools === tools) return;

  JSON.parse(tools);
  const promptPointer = allocateCString(runtime, "");
  const toolsPointer = allocateCString(runtime, tools);

  try {
    const result = runtime._needle_init(promptPointer, toolsPointer);
    if (result < 0) throw new Error("tool initialization failed");
    loadedTools = tools;
  } finally {
    runtime._free(promptPointer);
    runtime._free(toolsPointer);
  }
}

function allocateCString(runtime, value) {
  const bytes = new TextEncoder().encode(value);
  const pointer = runtime._malloc(bytes.length + 1);
  runtime.HEAPU8.set(bytes, pointer);
  runtime.HEAPU8[pointer + bytes.length] = 0;
  return pointer;
}

async function run({ id, query, tools, maxNewTokens }) {
  const runtime = await ensureModel();
  initializeTools(runtime, tools);
  runtime._needle_reset();

  const queryPointer = allocateCString(runtime, query);
  try {
    const limit = Number.isInteger(maxNewTokens) ? maxNewTokens : 128;
    runtime._needle_complete(queryPointer, limit, outputPointer, 16384);
    const result = JSON.parse(runtime.UTF8ToString(outputPointer));
    self.postMessage({ type: "result", id, result });
  } finally {
    runtime._free(queryPointer);
  }
}

function warmup(runtime, tools) {
  /* Best-effort: run one tiny completion so the engine's internal buffers,
     allocators and JIT paths are warm before the user's first real query. */
  try {
    initializeTools(runtime, tools);
    runtime._needle_reset();
    const p = allocateCString(runtime, "hi");
    runtime._needle_complete(p, 64, outputPointer, 16384);
    runtime._free(p);
  } catch (e) {
    /* ignore warm-up failures */
  }
}

self.addEventListener("message", (event) => {
  const message = event.data;

  if (message?.type === "initialize") {
    ensureModel()
      .then((runtime) => {
        initializeTools(runtime, message.tools);
        const data = { type: "ready", loadSeconds, fromCache: fromCache };
        self.postMessage(data);
        if (message.warmup) warmup(runtime, message.tools);
      })
      .catch((error) => postError(error));
    return;
  }

  if (message?.type === "run") {
    run(message).catch((error) => postError(error, message.id));
  }
});
