// Which NEB biology practicals are hands-on, and the loader that starts one. A practical module
// exports create(ctx) returning { tools, steps, result, update, dispose }.
import { runPractical } from './runtime.js';

const PRACTICALS = {
  'alimentary-canal-dissection': () => import('./practicals/earthworm.js'),
  'flower-family-dissection': () => import('./practicals/flower.js'),
  'plasmolysis-rhoeo-peel': () => import('./practicals/peel.js'),
  'stomata-upper-lower-distribution': () => import('./practicals/peel.js'),
  'ts-dicot-monocot-root-stem': () => import('./practicals/sections.js'),
  'animal-tissue-slides': () => import('./practicals/slides.js'),
  'plant-tissue-diversity': () => import('./practicals/slides.js'),
  'grasshopper-animal-mitosis': () => import('./practicals/slides.js'),
  'frog-development-stages': () => import('./practicals/slides.js'),
  'compound-microscope-parts': () => import('./practicals/scope-parts.js'),
  'starch-detection-sample': () => import('./practicals/biochem.js'),
  'protein-detection-sample': () => import('./practicals/biochem.js'),
  'urine-tests-urea-sugar-albumin-bile': () => import('./practicals/biochem.js'),
  'salivary-amylase-temp-ph': () => import('./practicals/biochem.js'),
  'blood-sugar-detection': () => import('./practicals/biochem.js'),
  'potato-osmometer-osmosis': () => import('./practicals/physiology.js'),
  'imbibition-seeds-raisins': () => import('./practicals/physiology.js'),
  'onion-root-tip-mitosis-11': () => import('./practicals/onion-mitosis.js'),
  'onion-root-tip-mitosis-12': () => import('./practicals/onion-mitosis.js'),
  'transpiration-upper-lower-rate': () => import('./practicals/transpiration.js'),
  'respiration-rate-germinating-seeds': () => import('./practicals/respirometer.js'),
  'anaerobic-respiration-setup': () => import('./practicals/anaerobic.js'),
  'phototropism-setup': () => import('./practicals/tropism.js'),
  'suction-due-transpiration-setup': () => import('./practicals/suction.js'),
  'mendelian-inheritance-seeds': () => import('./practicals/mendel.js'),
  'quadrat-density-plant': () => import('./practicals/quadrat.js'),
  'cockroach-external-morphology': () => import('./practicals/cockroach.js'),
  'human-skeleton-joints': () => import('./practicals/skeleton.js'),
  'soil-microorganism-culture': () => import('./practicals/culture.js'),
  'skeleton-joints-health-disorders': () => import('./practicals/skeleton.js'),
  'quadrat-frequency-field': () => import('./practicals/quadrat.js'),
  'apical-bud-removal-setup': () => import('./practicals/tropism.js'),
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
