/* global createNeedle */

importScripts("./needle.js");

var RUNTIME_VERSION = "needle2-runtime-v3";
var BINARY_CACHE = "needle2-assets-v2";
var WASM_URL = "./needle.wasm?v=2";
var CACT_URL = "./needle2.cact?v=2";
var SNAPSHOT_DB = "neby-needle2";
var SNAPSHOT_STORE = "runtime-snapshots";
var SNAPSHOT_CHUNK_BYTES = 2 * 1024 * 1024;

var moduleInstance = null;
var loadingPromise = null;
var loadedTools = null;
var outputPointer = 0;
var loadSeconds = 0;
var runtimeSource = "cold";
var cacheAssets = true;
var snapshotNamespace = "web";

function postError(error, id) {
  self.postMessage({
    type: "error",
    id: id,
    message: error instanceof Error ? error.message : String(error),
  });
}

function postStatus(status, extra) {
  self.postMessage(Object.assign({ type: "status", status: status }, extra || {}));
}

function hashText(value) {
  var hash = 2166136261;
  for (var i = 0; i < value.length; i += 1) {
    hash ^= value.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0).toString(16);
}

function snapshotKey(tools) {
  return RUNTIME_VERSION + ":" + snapshotNamespace + ":" + hashText(tools);
}

function openSnapshotDb() {
  return new Promise(function (resolve, reject) {
    if (!self.indexedDB) {
      reject(new Error("IndexedDB unavailable"));
      return;
    }
    var request = self.indexedDB.open(SNAPSHOT_DB, 1);
    request.onupgradeneeded = function () {
      if (!request.result.objectStoreNames.contains(SNAPSHOT_STORE)) {
        request.result.createObjectStore(SNAPSHOT_STORE);
      }
    };
    request.onsuccess = function () { resolve(request.result); };
    request.onerror = function () { reject(request.error || new Error("IndexedDB open failed")); };
  });
}

async function idbGet(key) {
  var db = await openSnapshotDb();
  return new Promise(function (resolve, reject) {
    var transaction = db.transaction(SNAPSHOT_STORE, "readonly");
    var request = transaction.objectStore(SNAPSHOT_STORE).get(key);
    request.onsuccess = function () { resolve(request.result); };
    request.onerror = function () { reject(request.error || new Error("IndexedDB read failed")); };
    transaction.oncomplete = function () { db.close(); };
    transaction.onerror = function () { db.close(); };
  });
}

async function idbPut(key, value) {
  var db = await openSnapshotDb();
  return new Promise(function (resolve, reject) {
    var transaction = db.transaction(SNAPSHOT_STORE, "readwrite");
    transaction.objectStore(SNAPSHOT_STORE).put(value, key);
    transaction.oncomplete = function () { db.close(); resolve(); };
    transaction.onerror = function () {
      db.close();
      reject(transaction.error || new Error("IndexedDB write failed"));
    };
    transaction.onabort = transaction.onerror;
  });
}

async function idbDelete(key) {
  var db = await openSnapshotDb();
  return new Promise(function (resolve, reject) {
    var transaction = db.transaction(SNAPSHOT_STORE, "readwrite");
    transaction.objectStore(SNAPSHOT_STORE).delete(key);
    transaction.oncomplete = function () { db.close(); resolve(); };
    transaction.onerror = function () {
      db.close();
      reject(transaction.error || new Error("IndexedDB delete failed"));
    };
  });
}

async function idbDeleteExcept(prefix) {
  var db = await openSnapshotDb();
  return new Promise(function (resolve, reject) {
    var transaction = db.transaction(SNAPSHOT_STORE, "readwrite");
    var request = transaction.objectStore(SNAPSHOT_STORE).openCursor();
    request.onsuccess = function () {
      var cursor = request.result;
      if (!cursor) return;
      if (typeof cursor.key === "string" && cursor.key.indexOf(prefix) !== 0) cursor.delete();
      cursor.continue();
    };
    transaction.oncomplete = function () { db.close(); resolve(); };
    transaction.onerror = function () {
      db.close();
      reject(transaction.error || new Error("IndexedDB cleanup failed"));
    };
  });
}

async function clearSnapshot(tools) {
  var key = snapshotKey(tools);
  var metadata = null;
  try { metadata = await idbGet(key); } catch (_) { return; }
  if (metadata && metadata.chunkCount) {
    for (var i = 0; i < metadata.chunkCount; i += 1) {
      try { await idbDelete(key + ":" + i); } catch (_) { }
    }
  }
  try { await idbDelete(key); } catch (_) { }
}

async function restoreSnapshot(runtime, tools) {
  var key = snapshotKey(tools);
  var metadata;
  try {
    metadata = await idbGet(key);
  } catch (_) {
    return false;
  }
  if (!metadata || metadata.version !== RUNTIME_VERSION ||
      metadata.byteLength < 16 * 1024 * 1024 || metadata.byteLength > 128 * 1024 * 1024 ||
      metadata.outputPointer <= 0 || metadata.outputPointer + 16384 > metadata.byteLength) {
    return false;
  }

  postStatus("restoring");
  try {
    if (runtime.HEAPU8.byteLength < metadata.byteLength) {
      runtime._malloc(metadata.byteLength);
    }
    if (runtime.HEAPU8.byteLength < metadata.byteLength) {
      throw new Error("WASM heap could not grow for snapshot");
    }
    for (var i = 0; i < metadata.chunkCount; i += 1) {
      var chunk = await idbGet(key + ":" + i);
      if (!chunk) throw new Error("Snapshot chunk missing");
      var bytes = chunk instanceof Uint8Array ? chunk : new Uint8Array(chunk);
      var offset = i * metadata.chunkBytes;
      runtime.HEAPU8.set(bytes, offset);
      postStatus("restoring", { progress: Math.min(1, (offset + bytes.byteLength) / metadata.byteLength) });
    }
    outputPointer = metadata.outputPointer;
    loadedTools = tools;
    return true;
  } catch (_) {
    await clearSnapshot(tools);
    return false;
  }
}

async function saveSnapshot(runtime, tools) {
  var key = snapshotKey(tools);
  var byteLength = runtime.HEAPU8.byteLength;
  var chunkCount = Math.ceil(byteLength / SNAPSHOT_CHUNK_BYTES);
  postStatus("saving");
  try {
    await clearSnapshot(tools);
    await idbDeleteExcept(key + ":");
    for (var i = 0; i < chunkCount; i += 1) {
      var offset = i * SNAPSHOT_CHUNK_BYTES;
      var chunk = runtime.HEAPU8.slice(offset, Math.min(byteLength, offset + SNAPSHOT_CHUNK_BYTES));
      await idbPut(key + ":" + i, chunk.buffer);
      postStatus("saving", { progress: Math.min(1, (offset + chunk.byteLength) / byteLength) });
    }
    await idbPut(key, {
      version: RUNTIME_VERSION,
      byteLength: byteLength,
      chunkBytes: SNAPSHOT_CHUNK_BYTES,
      chunkCount: chunkCount,
      outputPointer: outputPointer,
      createdAt: Date.now(),
    });
    return true;
  } catch (_) {
    await clearSnapshot(tools);
    return false;
  }
}

async function readResponse(response, label) {
  var total = Number(response.headers.get("Content-Length")) || 0;
  if (!response.body || !response.body.getReader || !total) {
    var plain = new Uint8Array(await response.arrayBuffer());
    postStatus("downloading", { asset: label, loaded: plain.byteLength, total: plain.byteLength, progress: 1 });
    return plain;
  }

  var output = new Uint8Array(total);
  var loaded = 0;
  var reader = response.body.getReader();
  while (true) {
    var part = await reader.read();
    if (part.done) break;
    if (loaded + part.value.byteLength > output.byteLength) {
      var expanded = new Uint8Array(Math.max(loaded + part.value.byteLength, output.byteLength * 2));
      expanded.set(output);
      output = expanded;
    }
    output.set(part.value, loaded);
    loaded += part.value.byteLength;
    postStatus("downloading", { asset: label, loaded: loaded, total: total, progress: Math.min(1, loaded / total) });
  }
  return loaded === output.byteLength ? output : output.slice(0, loaded);
}

async function loadAsset(url, label) {
  var cache = null;
  if (cacheAssets && self.caches) {
    try {
      cache = await self.caches.open(BINARY_CACHE);
      var cached = await cache.match(url);
      if (cached) {
        postStatus("cache-hit", { asset: label });
        return new Uint8Array(await cached.arrayBuffer());
      }
    } catch (_) {
      cache = null;
    }
  }

  postStatus("downloading", { asset: label, loaded: 0, total: 0, progress: 0 });
  var response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error("failed to fetch " + url + ": " + response.status);
  var cacheWrite = Promise.resolve();
  if (cache) {
    try { cacheWrite = cache.put(url, response.clone()).catch(function () {}); } catch (_) { }
  }
  var bytes = await readResponse(response, label);
  await cacheWrite;
  return bytes;
}

function allocateCString(runtime, value) {
  var bytes = new TextEncoder().encode(value);
  var pointer = runtime._malloc(bytes.length + 1);
  runtime.HEAPU8.set(bytes, pointer);
  runtime.HEAPU8[pointer + bytes.length] = 0;
  return pointer;
}

function initializeTools(runtime, tools) {
  if (loadedTools === tools) return;
  JSON.parse(tools);
  var promptPointer = allocateCString(runtime, "");
  var toolsPointer = allocateCString(runtime, tools);
  try {
    var result = runtime._needle_init(promptPointer, toolsPointer, 0);
    if (result < 0) throw new Error("tool initialization failed");
    loadedTools = tools;
  } finally {
    runtime._free(promptPointer);
    runtime._free(toolsPointer);
  }
}

async function ensureRuntime(tools, options) {
  if (moduleInstance) {
    initializeTools(moduleInstance, tools);
    return moduleInstance;
  }
  if (options) {
    if (options.wasmUrl) WASM_URL = options.wasmUrl;
    if (options.cactUrl) CACT_URL = options.cactUrl;
    if (options.snapshotNamespace) snapshotNamespace = options.snapshotNamespace;
    if (options.cacheAssets === false) cacheAssets = false;
  }
  if (loadingPromise) return loadingPromise;

  loadingPromise = (async function () {
    var startedAt = performance.now();
    postStatus("loading-engine");
    var wasmBytes = await loadAsset(WASM_URL, "engine");
    var runtime = await createNeedle({ wasmBinary: wasmBytes });

    if (await restoreSnapshot(runtime, tools)) {
      moduleInstance = runtime;
      runtimeSource = "snapshot";
      loadSeconds = (performance.now() - startedAt) / 1000;
      return runtime;
    }

    postStatus("loading-model");
    var modelBytes = await loadAsset(CACT_URL, "model");
    var modelPointer = runtime._malloc(modelBytes.length);
    runtime.HEAPU8.set(modelBytes, modelPointer);
    if (runtime._needle_load(modelPointer, BigInt(modelBytes.length)) !== 0) {
      throw new Error("model load failed");
    }

    outputPointer = runtime._malloc(16384);
    postStatus("preparing-tools");
    initializeTools(runtime, tools);
    moduleInstance = runtime;
    runtimeSource = "cold";
    await saveSnapshot(runtime, tools);
    loadSeconds = (performance.now() - startedAt) / 1000;
    return runtime;
  })().catch(function (error) {
    loadingPromise = null;
    moduleInstance = null;
    loadedTools = null;
    throw error;
  });

  return loadingPromise;
}

async function run(message) {
  var runtime = await ensureRuntime(message.tools, message);
  runtime._needle_reset();
  var queryPointer = allocateCString(runtime, message.query);
  var startedAt = performance.now();
  try {
    var limit = Number.isInteger(message.maxNewTokens) ? Math.max(16, Math.min(256, message.maxNewTokens)) : 128;
    var written = runtime._needle_complete(queryPointer, limit, outputPointer, 16384);
    if (written <= 0) throw new Error("completion failed");
    var result = JSON.parse(runtime.UTF8ToString(outputPointer));
    self.postMessage({
      type: "result",
      id: message.id,
      durationMs: performance.now() - startedAt,
      result: result,
    });
  } finally {
    runtime._free(queryPointer);
  }
}

self.addEventListener("message", function (event) {
  var message = event.data || {};
  if (message.type === "initialize") {
    ensureRuntime(message.tools, message)
      .then(function () {
        self.postMessage({
          type: "ready",
          loadSeconds: loadSeconds,
          source: runtimeSource,
          heapBytes: moduleInstance && moduleInstance.HEAPU8 ? moduleInstance.HEAPU8.byteLength : 0,
        });
      })
      .catch(function (error) { postError(error); });
    return;
  }
  if (message.type === "run") {
    run(message).catch(function (error) { postError(error, message.id); });
    return;
  }
  if (message.type === "clear-cache") {
    clearSnapshot(message.tools || loadedTools || "[]")
      .then(function () { self.postMessage({ type: "cache-cleared" }); })
      .catch(function (error) { postError(error); });
  }
});
