import { buildClimber } from './climber-model.js';

self.onmessage = (e) => {
  const r = buildClimber(e.data.tier);
  const t = [];
  Object.values(r).forEach((p) => { t.push(p.mesh.position.buffer, p.mesh.normal.buffer, p.mesh.index.buffer, p.color.buffer); });
  self.postMessage(r, t);
};
