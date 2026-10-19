// The chemistry behind the hands-on titrations. pH comes from the full charge balance, not a
// lookup: for a strong acid against a strong base, [H+] - [OH-] = (nH - nOH) / V with
// [H+][OH-] = Kw, so [H+] = (d + sqrt(d^2 + 4Kw)) / 2. Indicators are weak acids HIn with a
// pKa; the coloured fraction is 1 / (1 + 10^(pKa - pH)) and the colour is mixed from it through
// Beer-Lambert absorbance, so faint pinks look faint the way they do in a flask on a white tile.
import { THREE } from '../engine.js';

const KW = 1e-14;

export function phOf(nAcid, nBase, litres) {
  const d = (nAcid - nBase) / Math.max(1e-9, litres);
  const h = (d + Math.sqrt(d * d + 4 * KW)) / 2;
  return -Math.log10(h);
}

export const INDICATORS = {
  phenolphthalein: { name: 'Phenolphthalein', pKa: 9.3, acid: [0.0, 0.0, 0.0], base: [0.25, 2.6, 0.9], note: 'colourless in acid, pink in base (8.2–10)' },
  methylOrange: { name: 'Methyl orange', pKa: 3.47, acid: [0.1, 1.6, 1.2], base: [0.05, 0.55, 2.2], note: 'red in acid, yellow in base (3.1–4.4)' },
};

/** Fraction of the indicator in its basic (In-) form at a given pH. */
export function basicFraction(ind, pH) { return 1 / (1 + Math.pow(10, ind.pKa - pH)); }

const WATER = new THREE.Color(0xf4f9ff);
/** Colour of the flask through a path of liquid: absorbance per channel, A = eps * c * l. */
export function indicatorColor(ind, pH, strength, out) {
  const f = basicFraction(ind, pH);
  const r = ind.acid[0] * (1 - f) + ind.base[0] * f;
  const g = ind.acid[1] * (1 - f) + ind.base[1] * f;
  const b = ind.acid[2] * (1 - f) + ind.base[2] * f;
  return out.setRGB(WATER.r * Math.pow(10, -r * strength), WATER.g * Math.pow(10, -g * strength), WATER.b * Math.pow(10, -b * strength));
}

/**
 * A titration flask: base of unknown molarity, acid arriving from the burette into an unmixed
 * plume at the surface that swirling folds into the bulk. The plume is what makes the pink
 * vanish where each drop lands and return when swirled, lingering longer near the end point.
 */
export function createTitrationFlask({ baseM, acidM = 0.1, indicator = INDICATORS.phenolphthalein }) {
  const s = { baseMl: 0, waterMl: 0, acidMl: 0, plumeMl: 0, indicatorDrops: 0, swirl: 0, ind: indicator };
  const api = {
    state: s,
    reset() { s.baseMl = 0; s.waterMl = 0; s.acidMl = 0; s.plumeMl = 0; s.indicatorDrops = 0; },
    get volumeMl() { return s.baseMl + s.waterMl + s.acidMl + s.indicatorDrops * 0.05; },
    addBase(ml) { s.baseMl += ml; },
    addWater(ml) { s.waterMl += ml; },
    addIndicator(drops = 1) { s.indicatorDrops += drops; },
    addAcid(ml) { s.acidMl += ml; s.plumeMl += ml; },
    /** Moles of base the student's flask actually contains. */
    get nBase() { return baseM * s.baseMl / 1000; },
    get equivalenceMl() { return baseM * s.baseMl / acidM; },
    bulkPh() { const mixed = s.acidMl - s.plumeMl; return phOf(acidM * mixed / 1000, api.nBase, api.volumeMl / 1000); },
    finalPh() { return phOf(acidM * s.acidMl / 1000, api.nBase, api.volumeMl / 1000); },
    /** How strongly the patch where the acid lands has lost the bulk colour (0..1). */
    plumeStrength() {
      if (s.plumeMl <= 1e-6) return 0;
      const mixed = s.acidMl - s.plumeMl;
      const excessBase = Math.max(0, api.nBase - acidM * mixed / 1000);
      const local = (s.plumeMl + 3) / 1000;
      const cOH = excessBase / Math.max(1e-6, api.volumeMl / 1000);
      const z = (acidM * s.plumeMl / 1000) / Math.max(1e-12, cOH * local);
      return Math.min(1, z);
    },
    step(dt) {
      const k = 0.45 + 2.5 * (s.flow || 0) + 7 * s.swirl;
      s.plumeMl *= Math.exp(-k * dt);
      if (s.plumeMl < 1e-5) s.plumeMl = 0;
    },
    /** Indicator strength scales with drops and inversely with volume (more dilute, paler). */
    colour(out, pH = api.bulkPh()) {
      const strength = Math.min(1.4, s.indicatorDrops * 0.11 * (30 / Math.max(10, api.volumeMl)));
      return indicatorColor(s.ind, pH, strength, out);
    },
  };
  return api;
}

/**
 * A redox titration flask: Fe2+ (Mohr's salt, acidified) titrated with KMnO4, which is its own
 * indicator. MnO4- + 5Fe2+ + 8H+ -> Mn2+ + 5Fe3+ + 4H2O. Each drop is purple where it lands and
 * is decolourised as swirling mixes it into the Fe2+; once every Fe2+ is used, the first excess
 * of permanganate (about 1e-5 M) turns the whole flask a faint permanent pink.
 */
export function createRedoxFlask({ fasM, kmM = 0.02 }) {
  const s = { baseMl: 0, waterMl: 0, acidMl: 0, plumeMl: 0, indicatorDrops: 1, swirl: 0, flow: 0, acidified: false };
  const EPS = 2.4e3; const PATH = 4;
  const api = {
    state: s,
    redox: true,
    reset() { s.baseMl = 0; s.waterMl = 0; s.acidMl = 0; s.plumeMl = 0; s.acidified = false; },
    get volumeMl() { return s.baseMl + s.waterMl + s.acidMl; },
    addBase(ml) { s.baseMl += ml; },
    addWater(ml) { s.waterMl += ml; },
    addIndicator() {},
    addAcid(ml) { s.acidMl += ml; s.plumeMl += ml; },
    get equivalenceMl() { return fasM * s.baseMl / (5 * kmM); },
    /** Molar excess of MnO4- once mixed (0 before the end point). */
    excess(mixedOnly = true) {
      const km = kmM * (s.acidMl - (mixedOnly ? s.plumeMl : 0)) / 1000;
      const fe = fasM * s.baseMl / 1000;
      return Math.max(0, km - fe / 5) / Math.max(1e-6, api.volumeMl / 1000);
    },
    /** True when the fully mixed flask stays pink. */
    atEndpoint() { return api.excess(false) > 4e-6; },
    plumeStrength() {
      if (s.plumeMl <= 1e-6) return 0;
      const mixed = s.acidMl - s.plumeMl;
      const feLeft = Math.max(0, fasM * s.baseMl / 1000 - 5 * kmM * mixed / 1000);
      const cFe = feLeft / Math.max(1e-6, api.volumeMl / 1000);
      const z = (5 * kmM * s.plumeMl / 1000) / Math.max(1e-12, cFe * (s.plumeMl + 3) / 1000);
      return Math.min(1, z);
    },
    step(dt) { const k = 0.45 + 2.5 * (s.flow || 0) + 7 * s.swirl; s.plumeMl *= Math.exp(-k * dt); if (s.plumeMl < 1e-5) s.plumeMl = 0; },
    colour(out) {
      const a = EPS * api.excess(true) * PATH;
      const fe = s.baseMl > 0 ? 0.03 : 0;
      return out.setRGB(0.97 * Math.pow(10, -0.12 * a) - fe * 0.2, 0.98 * Math.pow(10, -1.0 * a), 0.99 * Math.pow(10, -0.35 * a) - fe * 0.25);
    },
    /** Fraction of the end-point colour showing (0..1), used for opacity. */
    showing() { return Math.min(1, api.excess(true) / 2e-5); },
  };
  return api;
}
