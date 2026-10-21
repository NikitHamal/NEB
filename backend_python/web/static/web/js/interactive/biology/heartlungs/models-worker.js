import { buildHeart } from './heart-model.js';
import { buildLungs, buildAirway, buildDiaphragm } from './lung-model.js';

function buffers(o, out = new Set()) {
  if (!o || typeof o !== 'object') return out;
  if (ArrayBuffer.isView(o)) { out.add(o.buffer); return out; }
  Object.values(o).forEach((v) => buffers(v, out));
  return out;
}

self.onmessage = (e) => {
  const q = e.data.quality;
  const models = { H: buildHeart(q), L: buildLungs(q), A: buildAirway(q), D: buildDiaphragm(q) };
  self.postMessage(models, [...buffers(models)]);
};
