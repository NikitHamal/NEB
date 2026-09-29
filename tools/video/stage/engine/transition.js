import { seg } from './tl.js';
import { outExpo, inOutCubic } from './ease.js';
import { place } from './dom.js';

export function pushProgress(lt, total, { lead = 0.32, inDur = 0.42, outDur = 0.36 } = {}) {
  return {
    enter: outExpo(seg(lt, -lead, inDur)),
    leave: inOutCubic(seg(lt, total - lead, outDur)),
  };
}

export function applyPush(S, node, lt, total, cfg) {
  const progress = pushProgress(lt, total, cfg);
  const enter = progress.enter;
  const leave = cfg?.exit === false ? 0 : progress.leave;
  place(node, { x: (1 - enter) * S.W - leave * S.W * 0.92, y: 0, s: 1 - leave * 0.04 });
  return { enter, leave };
}
