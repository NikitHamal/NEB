/* global createNeedle */

importScripts("./needle.js");

/* Assets are served as binary files (needle.wasm + needle2.cact) and cached in
   the Cache Storage API. First visit downloads them once; every later visit
   loads straight from browser storage — no re-download on refresh. Bump
   ASSET_VERSION when the model or engine changes to force a refresh. */

var ASSET_VERSION = "needle2-assets-v1";
var WASM_URL = "./needle.wasm?v=1";
var CACT_URL = "./needle2.cact?v=1";

var moduleInstance = null;
var loadingPromise = null;
var loadedTools = null;
var outputPointer = 0;
var loadSeconds = 0;

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

async function loadAsset(url) {
  var cache = await caches.open(ASSET_VERSION);
  var cached = await cache.match(url);
  if (cached) {
    var cachedBytes = await cached.arrayBuffer();
    return new Uint8Array(cachedBytes);
  }
  var bytes = await fetchBytes(url);
  try {
    await cache.put(url, new Response(bytes.slice().buffer, {
      headers: { "Content-Type": "application/octet-stream" },
    }));
  } catch (e) {
    /* cache write failure is non-fatal — the model is still loaded */
  }
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

async function run({ id, query, tools }) {
  const runtime = await ensureModel();
  initializeTools(runtime, tools);
  runtime._needle_reset();

  const queryPointer = allocateCString(runtime, query);
  try {
    runtime._needle_complete(queryPointer, 256, outputPointer, 16384);
    const result = JSON.parse(runtime.UTF8ToString(outputPointer));
    self.postMessage({ type: "result", id, result });
  } finally {
    runtime._free(queryPointer);
  }
}

self.addEventListener("message", (event) => {
  const message = event.data;

  if (message?.type === "initialize") {
    ensureModel()
      .then((runtime) => {
        initializeTools(runtime, message.tools);
        self.postMessage({ type: "ready", loadSeconds });
      })
      .catch((error) => postError(error));
    return;
  }

  if (message?.type === "run") {
    run(message).catch((error) => postError(error, message.id));
  }
});
