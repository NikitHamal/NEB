// Which NEB physics and chemistry practicals are hands-on. They run on the same practical runtime
// as the biology labs (procedure, teacher, score, result card) in the physics or chemistry room.
import { runPractical } from '../bio-handson/runtime.js';

const PRACTICALS = {
  'acid-base-titration': () => import('./practicals/titration.js'),
  'simple-pendulum-g': () => import('./practicals/pendulum.js'),
  'vernier-calipers': () => import('./practicals/vernier.js'),
  'meter-bridge': () => import('./practicals/meter-bridge.js'),
  'screw-gauge': () => import('./practicals/screw-gauge.js'),
  'anion-tests': () => import('./practicals/anion-tests.js'),
  'redox-titration-kmno4': () => import('./practicals/titration.js'),
  'resonance-air-column': () => import('./practicals/resonance.js'),
  'ohms-law-resistivity': () => import('./practicals/ohms-law.js'),
  'hookes-law-spring': () => import('./practicals/hookes-law.js'),
  'focal-length-mirror-lens': () => import('./practicals/focal-length.js'),
  'sonometer-laws': () => import('./practicals/sonometer.js'),
  'potentiometer-emf': () => import('./practicals/potentiometer.js'),
  'electrolysis-cuso4': () => import('./practicals/electrolysis.js'),
  'flame-tests': () => import('./practicals/flame-tests.js'),
  'spherometer': () => import('./practicals/spherometer.js'),
  'coefficient-of-friction': () => import('./practicals/friction.js'),
  'specific-heat-mixtures': () => import('./practicals/specific-heat.js'),
  'heat-of-neutralization': () => import('./practicals/neutralization.js'),
  'parallelogram-of-forces': () => import('./practicals/parallelogram.js'),
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
