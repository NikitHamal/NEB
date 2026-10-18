// The chemistry of the anion tests, as rules on what is in a test tube. Each addition is applied
// in order, so the order matters the way it does at the bench: silver nitrate on an unacidified
// carbonate throws down Ag2CO3 (a false 'chloride'), barium chloride does the same with BaCO3,
// and the brown ring only forms when the concentrated acid runs down the side under the FeSO4.
// apply() returns what the student sees: colour, cloudiness, a precipitate, gas, a ring, a smell.

export const ANIONS = {
  carbonate: { name: 'Carbonate', ion: 'CO₃²⁻', salt: 'Na₂CO₃' },
  chloride: { name: 'Chloride', ion: 'Cl⁻', salt: 'NaCl' },
  sulfate: { name: 'Sulphate', ion: 'SO₄²⁻', salt: 'Na₂SO₄' },
  nitrate: { name: 'Nitrate', ion: 'NO₃⁻', salt: 'KNO₃' },
  sulfide: { name: 'Sulphide', ion: 'S²⁻', salt: 'Na₂S' },
};

export const REAGENTS = {
  solid: { name: 'Salt (solid)', short: 'salt', color: 0xf5f5f0 },
  soln: { name: 'Salt solution', short: 'extract', color: 0xeef6ff },
  hcl: { name: 'dil. HCl', short: 'HCl', color: 0xf1f7ff },
  hno3: { name: 'dil. HNO₃', short: 'HNO₃', color: 0xf3f7ff },
  agno3: { name: 'AgNO₃', short: 'AgNO₃', color: 0xf7f7ff, amber: true },
  nh4oh: { name: 'NH₄OH', short: 'NH₄OH', color: 0xf2f8ff },
  bacl2: { name: 'BaCl₂', short: 'BaCl₂', color: 0xf3f7fb },
  feso4: { name: 'FeSO₄ (fresh)', short: 'FeSO₄', color: 0xc9e8c4 },
  h2so4: { name: 'conc. H₂SO₄', short: 'H₂SO₄', color: 0xf7f3e8 },
};

/** A test tube's chemistry: what went in, in what order, and what that looks like. */
export function createTubeChem(anion) {
  const s = { added: [], acid: 0, ppt: null, pptAmount: 0, cloudy: 0, color: 0xeef6ff, gas: null, ring: false, layered: false, smell: null, salt: false, log: [] };
  function note(t) { s.log.push(t); return t; }
  const has = (k) => s.added.includes(k);
  return {
    state: s,
    /** Adds a reagent (how = 'side' for conc. acid run down the side). Returns the observation. */
    apply(k, how) {
      const first = !has(k); s.added.push(k);
      if (k === 'solid' || k === 'soln') { s.salt = true; s.color = 0xeef6ff; return note(k === 'solid' ? 'A little of the solid salt.' : 'Clear, colourless salt solution.'); }
      if (!s.salt) return note('Nothing happens: there is no salt in this tube yet.');
      if (k === 'hcl' || k === 'hno3') {
        s.acid += 1;
        if (anion === 'carbonate') {
          if (s.ppt === 'Ag₂CO₃' || s.ppt === 'BaCO₃') { s.ppt = null; s.pptAmount = 0; s.cloudy = 0; s.gas = 'CO₂'; return note('The white precipitate dissolves with brisk effervescence: it was a carbonate, not a chloride or sulphate.'); }
          s.gas = 'CO₂'; return note('Brisk effervescence: a colourless, odourless gas.');
        }
        if (anion === 'sulfide') { s.gas = 'H₂S'; s.smell = 'rotten eggs'; if (s.ppt === 'Ag₂S') return note('The black precipitate stays.'); return note('Effervescence; a gas that smells of rotten eggs.'); }
        if (k === 'hcl' && s.ppt === 'BaSO₄') return note('The white precipitate does not dissolve in dilute HCl.');
        return note(first ? 'No visible change.' : 'No further change.');
      }
      if (k === 'agno3') {
        if (anion === 'chloride') { s.ppt = 'AgCl'; s.pptAmount = 1; s.cloudy = 0.9; s.color = 0xffffff; return note('A white, curdy precipitate.'); }
        if (anion === 'carbonate' && s.acid === 0) { s.ppt = 'Ag₂CO₃'; s.pptAmount = 0.7; s.cloudy = 0.7; s.color = 0xfff9e6; return note('A white precipitate that turns yellowish (Ag₂CO₃). Was the solution acidified with HNO₃ first?'); }
        if (anion === 'sulfide') { s.ppt = 'Ag₂S'; s.pptAmount = 1; s.cloudy = 0.95; s.color = 0x111111; return note('A black precipitate.'); }
        return note('No precipitate.');
      }
      if (k === 'nh4oh') {
        if (s.ppt === 'AgCl') { s.ppt = null; s.pptAmount = 0; s.cloudy = 0; s.color = 0xeef6ff; return note('The white precipitate dissolves in ammonia solution: silver chloride.'); }
        return note('No visible change.');
      }
      if (k === 'bacl2') {
        if (anion === 'sulfate') { s.ppt = 'BaSO₄'; s.pptAmount = 1; s.cloudy = 0.9; s.color = 0xffffff; return note('A dense white precipitate.'); }
        if (anion === 'carbonate' && s.acid === 0) { s.ppt = 'BaCO₃'; s.pptAmount = 0.8; s.cloudy = 0.8; s.color = 0xffffff; return note('A white precipitate. Does it dissolve in dilute HCl?'); }
        return note('No precipitate.');
      }
      if (k === 'feso4') { s.color = 0xd9eed6; return note('Pale green iron(II) sulphate mixes in.'); }
      if (k === 'h2so4') {
        if (how !== 'side') {
          s.color = anion === 'nitrate' && has('feso4') ? 0x8a5a2b : s.color;
          return note(anion === 'nitrate' && has('feso4') ? 'The whole tube darkens and warms: the acid was poured in, so it mixed. No ring to judge.' : 'The tube becomes hot. Concentrated acid should run slowly down the side.');
        }
        s.layered = true;
        if (anion === 'nitrate' && has('feso4')) { s.ring = true; return note('A brown ring forms where the heavy acid meets the solution: [Fe(H₂O)₅NO]²⁺.'); }
        if (!has('feso4')) return note('The acid sinks to the bottom as a separate layer.');
        return note('The acid sinks and forms a layer; no brown ring at the junction.');
      }
      return note('No visible change.');
    },
  };
}

/** What a gas does to a test held at the mouth of the tube. */
export function gasTest(gas, test) {
  if (test === 'limewater') return gas === 'CO₂' ? 'Lime water turns milky (CaCO₃).' : 'Lime water stays clear.';
  if (test === 'leadpaper') return gas === 'H₂S' ? 'Lead acetate paper turns black (PbS).' : 'The lead acetate paper does not change.';
  if (test === 'splint') return gas === 'CO₂' ? 'The burning splint goes out.' : gas === 'H₂S' ? 'The gas burns with a blue flame.' : 'The splint keeps burning.';
  return '';
}
