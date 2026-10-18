// Which NEB physics and chemistry practicals are hands-on. They run on the same practical runtime
// as the biology labs (procedure, teacher, score, result card) in the physics or chemistry room.
import { runPractical } from '../bio-handson/runtime.js';

const PRACTICALS = {
  'acid-base-titration': () => import('./practicals/titration.js'),
  'flame-tests': () => import('./practicals/flame-tests.js'),
};

export function hasHandsOn(slug) { return Object.prototype.hasOwnProperty.call(PRACTICALS, slug); }

export function startHandsOn(stage, slug, preset) {
  let handle = null; let disposed = false;
  const config = { slug, subject: preset.subject, title: preset.title.replace(/^(Real )?3D /, ''), aim: preset.subtitle || '' };
  PRACTICALS[slug]().then((mod) => {
    if (disposed) return;
    handle = runPractical(stage, config, mod);
  }).catch((err) => { console.error('Hands-on practical failed to load:', err); });
  return { dispose() { disposed = true; if (handle) handle.dispose(); } };
}
