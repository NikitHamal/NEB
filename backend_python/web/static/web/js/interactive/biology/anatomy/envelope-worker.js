import { buildEnvelope } from './skin.js';

self.onmessage = (e) => {
  const { positions, bounds, cell, opts } = e.data;
  const env = buildEnvelope(positions, bounds, cell, opts);
  const out = new Set();
  Object.values(env).forEach((v) => { if (ArrayBuffer.isView(v)) out.add(v.buffer); });
  self.postMessage(env, [...out]);
};
