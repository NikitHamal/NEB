// The chemistry of systematic cation analysis, as rules on what is in a tube and in what order it
// went in. Group reagents only separate groups when used in sequence and in the right medium: H₂S
// without acid also brings down zinc, ammonia without ammonium chloride also brings down magnesium,
// and Fe³⁺ meeting H₂S in acid is reduced (milky sulphur) instead of giving a black sulphide.

export const SALTS = [
  { f: 'Pb(NO₃)₂', cat: 'Pb', an: 'nitrate', look: 'White crystalline solid', dry: 'It crackles (decrepitates), gives off brown fumes (NO₂) and leaves a yellow residue (PbO).' },
  { f: 'CuSO₄·5H₂O', cat: 'Cu', an: 'sulfate', look: 'Blue crystals', dry: 'Drops of water condense on the cool part of the tube and the blue crystals turn to a white powder.' },
  { f: 'FeCl₃', cat: 'Fe', an: 'chloride', look: 'Yellowish-brown solid', dry: 'It darkens to reddish-brown and gives off acidic fumes.' },
  { f: 'ZnSO₄·7H₂O', cat: 'Zn', an: 'sulfate', look: 'White crystals', dry: 'Water condenses; the residue is yellow while hot and white when cold (ZnO).' },
  { f: 'CaCl₂', cat: 'Ca', an: 'chloride', look: 'White solid', dry: 'No marked change (it may melt in its own water).' },
  { f: 'MgSO₄·7H₂O', cat: 'Mg', an: 'sulfate', look: 'White crystals', dry: 'Water condenses; a white residue is left.' },
  { f: 'NH₄Cl', cat: 'NH4', an: 'chloride', look: 'White solid', dry: 'It sublimes: a white sublimate forms on the cool part of the tube.' },
];

export const CATIONS = {
  Pb: { ion: 'Pb²⁺', name: 'Lead', group: 'I', flame: null, flameText: 'A dull bluish-white flame.', soln: 0xf2f6fa },
  Cu: { ion: 'Cu²⁺', name: 'Copper(II)', group: 'II', flame: { Cu: 1 }, flameText: 'A bluish-green flame.', soln: 0x6fa8dc },
  Fe: { ion: 'Fe³⁺', name: 'Iron(III)', group: 'III', flame: null, flameText: 'No characteristic colour (a few sparks).', soln: 0xd8b25a },
  Zn: { ion: 'Zn²⁺', name: 'Zinc', group: 'IV', flame: null, flameText: 'No characteristic colour.', soln: 0xf2f6fa },
  Ca: { ion: 'Ca²⁺', name: 'Calcium', group: 'V', flame: { Ca: 1 }, flameText: 'A brick-red flame.', soln: 0xf2f6fa },
  Mg: { ion: 'Mg²⁺', name: 'Magnesium', group: 'VI', flame: null, flameText: 'No characteristic colour.', soln: 0xf2f6fa },
  NH4: { ion: 'NH₄⁺', name: 'Ammonium', group: '0', flame: null, flameText: 'No characteristic colour.', soln: 0xf2f6fa },
};

export const CREAG = {
  soln: { short: 'O.S.', tag: 'salt solution', color: 0xeef6ff, sub: 'unknown' },
  hcl: { short: 'dil. HCl', color: 0xf1f7ff }, h2s: { short: 'H₂S water', tag: 'H₂S', color: 0xf3f7f0 }, nh4cl: { short: 'NH₄Cl', color: 0xf3f6fa }, nh4oh: { short: 'NH₄OH', color: 0xf2f8ff },
  nh42co3: { short: '(NH₄)₂CO₃', color: 0xf3f6fa }, naoh: { short: 'NaOH', color: 0xf2f6fb },
  ki: { short: 'KI', color: 0xf5f7f9 }, k4fe: { short: 'K₄[Fe(CN)₆]', color: 0xf3e7a4 }, kcns: { short: 'KCNS', color: 0xf5f7f9 }, c2o4: { short: '(NH₄)₂C₂O₄', tag: 'amm. oxalate', color: 0xf5f7f9 },
  hpo4: { short: 'Na₂HPO₄', color: 0xf5f7f9 }, nessler: { short: 'Nessler', color: 0xf0dc9a },
};
export const RNAME = { soln: 'salt solution', hcl: 'dil. HCl', h2s: 'H₂S', nh4cl: 'NH₄Cl', nh4oh: 'NH₄OH', nh42co3: '(NH₄)₂CO₃', naoh: 'NaOH', ki: 'KI', k4fe: 'K₄[Fe(CN)₆]', kcns: 'KCNS', c2o4: 'ammonium oxalate', hpo4: 'Na₂HPO₄', nessler: 'Nessler\'s reagent' };

/** A tube of the salt solution and what each addition does to it. */
export function createCationTube(cat) {
  const s = { added: [], gone: false, ppt: null, color: CATIONS[cat].soln, warmed: false, gas: null };
  const has = (k) => s.added.includes(k);
  const L = (text, look = {}) => ({ text, look });
  return {
    state: s,
    warm() { s.warmed = true; if (has('naoh') && cat === 'NH4') { s.gas = 'NH₃'; return L('On warming, a pungent smell of ammonia; moist red litmus held at the mouth turns blue.'); } return L(has('naoh') ? 'Warming gives no smell of ammonia.' : 'Warmed.'); },
    apply(k) {
      const first = !has(k); s.added.push(k);
      if (k === 'soln') return L(cat === 'Cu' ? 'A clear blue solution.' : cat === 'Fe' ? 'A clear yellow-brown solution.' : 'A clear, colourless solution.', { fill: 0.2, color: s.color, opacity: 0.55 });
      if (!has('soln')) return L('There is no salt solution in this tube yet.');
      if (s.gone) return L('The cation has already been precipitated: the solution above the precipitate gives nothing more.');
      const fin = (text, color, groupDone = true) => { s.gone = groupDone; s.ppt = color; return L(text, { ppt: { color, amount: 0.9 }, opacity: 0.7 }); };
      switch (k) {
        case 'hcl': return cat === 'Pb' ? fin('A white precipitate (PbCl₂). It dissolves when the tube is heated: Group I.', 0xf6f6f2) : L(first ? 'No precipitate.' : 'No further change.');
        case 'h2s':
          if (has('nh4oh')) {
            if (cat === 'Zn') return fin('A dirty-white precipitate of ZnS in the ammoniacal solution: Group IV.', 0xe9e6dc);
            return L('No precipitate.');
          }
          if (!has('hcl')) {
            if (cat === 'Cu' || cat === 'Pb') return fin('A black precipitate.', 0x161616);
            if (cat === 'Zn') return fin('A white precipitate (ZnS) — but the solution was not acidified, so zinc came down with Group II.', 0xeeeeea);
            if (cat === 'Fe') return fin('A black precipitate of iron sulphide (the solution was not acidified).', 0x1b1b1b);
            return L('No precipitate.');
          }
          if (cat === 'Cu') return fin('A black precipitate of CuS in the acid solution: Group II.', 0x161616);
          if (cat === 'Fe') { s.color = 0xdfe8cf; return L('No black precipitate, but the solution turns milky white (sulphur) and pale green: Fe³⁺ is reduced to Fe²⁺. Boil off the H₂S and oxidise it back before Group III.', { color: 0xeef1e4, opacity: 0.8 }); }
          return L('No precipitate.');
        case 'nh4cl': return L('No visible change.');
        case 'nh4oh':
          if (cat === 'Fe') return fin('A reddish-brown gelatinous precipitate of Fe(OH)₃: Group III.', 0x8b3a12);
          if (cat === 'Cu') { s.color = 0x1d3fa8; return L('A pale blue precipitate that dissolves in excess to a deep blue solution, [Cu(NH₃)₄]²⁺.', { color: 0x1d3fa8, opacity: 0.8 }); }
          if (cat === 'Zn') return L('A white gelatinous precipitate that dissolves in excess ammonia.', { color: 0xf3f6f8 });
          if (cat === 'Mg' && !has('nh4cl')) return fin('A white precipitate of Mg(OH)₂ — but without NH₄Cl to suppress it, magnesium has come down with Group III.', 0xf4f4f0);
          if (cat === 'Pb') return fin('A white precipitate.', 0xf6f6f2);
          return L('No precipitate.');
        case 'nh42co3':
          if (cat === 'Ca') return fin('A white precipitate of CaCO₃: Group V.', 0xf8f8f4);
          if (cat === 'Mg' && !has('nh4cl')) return fin('A white precipitate (basic MgCO₃) — without NH₄Cl, magnesium is precipitated here too.', 0xf4f4f0);
          if (cat === 'Pb' || cat === 'Zn') return fin('A white precipitate.', 0xf6f6f2);
          if (cat === 'Cu') return fin('A pale blue precipitate.', 0x9cc3e4);
          return L('No precipitate.');
        case 'naoh':
          if (cat === 'Cu') return fin('A pale blue precipitate of Cu(OH)₂, insoluble in excess.', 0x7fb0e0, false);
          if (cat === 'Fe') return fin('A reddish-brown precipitate of Fe(OH)₃.', 0x8b3a12, false);
          if (cat === 'Zn' || cat === 'Pb') return L('A white precipitate that dissolves in excess NaOH.', { color: 0xf3f6f8 });
          if (cat === 'Mg') return fin('A white precipitate of Mg(OH)₂, insoluble in excess.', 0xf4f4f0, false);
          if (cat === 'Ca') return L('A slight white turbidity.', { opacity: 0.7 });
          return L('No precipitate. Warm it and test the vapour.');
        case 'ki':
          if (cat === 'Pb') return fin('A bright yellow precipitate of PbI₂ (it dissolves in hot water and comes back as golden spangles on cooling).', 0xf2cc1d, false);
          if (cat === 'Cu') return fin('A white precipitate (CuI) in a brown solution of iodine.', 0xeeeae0, false);
          if (cat === 'Fe') { s.color = 0x8a4a12; return L('The solution turns brown: iodine is liberated.', { color: 0x8a4a12, opacity: 0.7 }); }
          return L('No precipitate.');
        case 'k4fe':
          if (cat === 'Cu') return fin('A chocolate-brown precipitate of Cu₂[Fe(CN)₆].', 0x5a2e14, false);
          if (cat === 'Fe') return fin('A deep Prussian-blue precipitate.', 0x12338a, false);
          if (cat === 'Zn') return fin('A bluish-white precipitate.', 0xe4ecf2, false);
          return L('No characteristic change.');
        case 'kcns': if (cat === 'Fe') { s.color = 0x8a0f0f; return L('A blood-red colour, Fe(SCN)²⁺.', { color: 0x8a0f0f, opacity: 0.85 }); } return L('No characteristic change.');
        case 'c2o4': return cat === 'Ca' ? fin('A white precipitate of calcium oxalate, insoluble in acetic acid.', 0xf8f8f4, false) : cat === 'Pb' ? fin('A white precipitate.', 0xf6f6f2, false) : L('No precipitate.');
        case 'hpo4': return cat === 'Mg' ? fin('A white crystalline precipitate of Mg(NH₄)PO₄ (scratch the inside of the tube).', 0xf8f8f4, false) : cat === 'Ca' ? fin('A white precipitate.', 0xf8f8f4, false) : L('No precipitate.');
        case 'nessler': return cat === 'NH4' ? fin('A brown precipitate (iodide of Millon\'s base): ammonium.', 0x8a4b12, false) : L('A faint yellow colour only; no brown precipitate.', { color: 0xf3e4a6 });
        default: return L('No visible change.');
      }
    },
  };
}
