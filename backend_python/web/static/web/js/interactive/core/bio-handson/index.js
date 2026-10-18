// Which NEB biology practicals are hands-on, and the loader that starts one. A practical module
// exports create(ctx) returning { tools, steps, result, update, dispose }.
import { runPractical } from './runtime.js';

const PRACTICALS = {
  'alimentary-canal-dissection': () => import('./practicals/earthworm.js'),
};

export function hasHandsOn(slug) { return Object.prototype.hasOwnProperty.call(PRACTICALS, slug); }

export function startHandsOn(stage, config) {
  let handle = null; let disposed = false;
  PRACTICALS[config.slug]().then((mod) => {
    if (disposed) return;
    handle = runPractical(stage, config, mod);
  }).catch((err) => { console.error('Hands-on practical failed to load:', err); });
  return { dispose() { disposed = true; if (handle) handle.dispose(); } };
}
