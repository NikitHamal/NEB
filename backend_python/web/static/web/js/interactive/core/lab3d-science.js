// Shared scientific formulas, procedures and observation-book helpers for NEB 3D labs.

export function separationPrinciple(method) {
  return {
    filtration: 'particle size difference', distillation: 'boiling point difference', evaporation: 'volatile solvent removal', chromatography: 'partition + adsorption',
  }[method] || 'physical property difference';
}
export function separationObservation(method, temp) {
  if (method === 'distillation') return temp >= 78 ? 'distillate condenses in receiver' : 'heat until boiling starts';
  if (method === 'filtration') return 'residue stays on filter paper; filtrate passes through';
  if (method === 'evaporation') return temp > 90 ? 'crystals start appearing' : 'solution concentrates';
  return 'spots move different distances; calculate Rf';
}
export function titrationStatus(v, req) {
  const d = v - req;
  if (Math.abs(d) <= 0.10) return 'endpoint: stop and record';
  if (d < -0.8) return 'still before endpoint';
  if (d < 0) return 'close: add dropwise';
  return 'overshot endpoint';
}
export function indicatorColorName(ind, pH) {
  if (ind === 'phenolphthalein') return pH < 8.2 ? 'colourless' : 'pink';
  if (ind === 'methyl') return pH < 3.1 ? 'red' : pH < 4.4 ? 'orange' : 'yellow';
  if (ind === 'litmus') return pH < 6 ? 'red' : pH > 8 ? 'blue' : 'purple';
  if (pH < 3) return 'red'; if (pH < 6) return 'orange/yellow'; if (pH < 8) return 'green'; if (pH < 11) return 'blue'; return 'violet';
}
export function indicatorColor(ind, pH) {
  const c = indicatorColorName(ind, pH);
  if (c.includes('red')) return 0xef4444;
  if (c.includes('orange')) return 0xf97316;
  if (c.includes('yellow')) return 0xfacc15;
  if (c.includes('green')) return 0x22c55e;
  if (c.includes('blue')) return 0x3b82f6;
  if (c.includes('violet') || c.includes('purple')) return 0x8b5cf6;
  if (c.includes('pink')) return 0xec4899;
  return 0xe5e7eb;
}
export function lassaigneResult(element) {
  return {
    nitrogen: 'Prussian blue colour after FeSO₄, NaOH and acidification.',
    sulfur: 'Violet colour with sodium nitroprusside, or black PbS with lead acetate.',
    chlorine: 'White AgCl precipitate soluble in NH₄OH.',
    bromine: 'Pale yellow AgBr precipitate partly soluble in NH₄OH.',
    iodine: 'Yellow AgI precipitate insoluble in NH₄OH.',
  }[element];
}


const PROCEDURE_BANK = {
  caliper: ['Clean jaws and check zero error.', 'Place specimen between external jaws without over-tightening.', 'Read main scale just left of zero on vernier.', 'Find the coinciding vernier division and apply zero correction.'],
  micrometer: ['Check zero reading with anvil and spindle touching.', 'Hold wire gently using ratchet pressure.', 'Read sleeve scale and thimble coincidence.', 'Subtract zero error and repeat at different wire positions.'],
  spherometer: ['Level the three legs on the surface.', 'Bring central screw just to touch without pressing.', 'Note pitch-scale and circular-scale reading.', 'Use h and mean leg distance to calculate radius.'],
  pendulum: ['Set length from point of suspension to centre of bob.', 'Keep amplitude small and release without push.', 'Time 20 oscillations from the same extreme position.', 'Calculate T and g from repeated observations.'],
  forceboard: ['Set pulleys at the selected angle and verify low friction.', 'Hang weights for P and Q and centre the ring.', 'Trace the two forces and complete the parallelogram.', 'Measure diagonal as resultant and compare with calculated value.'],
  incline: ['Place block on plane and slowly increase angle.', 'Note the angle when sliding just begins.', 'Repeat with the same surfaces and average readings.', 'Calculate coefficient of friction from tan θ.'],
  spring: ['Set pointer to zero with no load.', 'Add loads one by one and wait for steady pointer.', 'Record load and extension within elastic limit.', 'Plot load-extension graph and find slope.'],
  calorimeter: ['Measure masses and initial temperatures.', 'Transfer hot body quickly into calorimeter.', 'Stir gently until final temperature stabilizes.', 'Apply heat balance including calorimeter correction.'],
  resonance: ['Fill tube and strike tuning fork gently.', 'Lower water level slowly until sound is loudest.', 'Read resonance length at eye level.', 'Apply end correction and calculate sound speed.'],
  sonometer: ['Set tension using the load pan.', 'Adjust bridges until resonance with tuning fork is found.', 'Measure vibrating length accurately.', 'Verify relation between f, L, T and linear density.'],
  circuit: ['Connect ammeter in series and voltmeter in parallel.', 'Close key briefly and set rheostat.', 'Record V and I pairs before wire heats up.', 'Plot V-I graph and calculate resistance.'],
  meterbridge: ['Connect known and unknown resistors in the two gaps.', 'Move jockey gently until galvanometer shows null.', 'Read balance length from the metre scale.', 'Calculate unknown resistance from wire ratio.'],
  potentiometer: ['Standardize the wire with the driver cell.', 'Find balance length for standard cell.', 'Find balance length for unknown cell.', 'Compare EMFs using E₁/E₂ = l₁/l₂.'],
  galvanometer: ['Set circuit with high resistance and key.', 'Pass small currents and record deflection.', 'Keep deflection in the linear scale range.', 'Compute current per scale division.'],
  optics: ['Align object, lens and screen on the same axis.', 'Move screen until the image is sharp.', 'Read u and v from the optical bench scale.', 'Use lens formula to calculate focal length.'],
  prism: ['Level spectrometer and focus collimator/telescope.', 'Measure prism angle A.', 'Rotate prism to minimum deviation position.', 'Calculate refractive index from A and D.'],
  apparatus: ['Identify apparatus and safety zone.', 'Clamp tall glassware vertically.', 'Keep flammable objects away from flame.', 'Read all glassware at eye level.'],
  separation: ['Choose technique based on physical property difference.', 'Set apparatus and collect product separately.', 'Control heating rate or solvent front.', 'Record observation and separation principle.'],
  titration: ['Rinse burette and pipette with their own solutions.', 'Pipette 25.0 mL sample into flask and add indicator.', 'Run rough titre, then add dropwise near endpoint.', 'Record concordant readings within 0.10 mL.'],
  flame: ['Clean loop in acid and heat until no colour appears.', 'Dip loop into unknown salt.', 'Place in non-luminous flame.', 'Observe persistent colour and note contamination.'],
  testtubes: ['Add small amount of unknown solution.', 'Add reagent dropwise and shake.', 'Look for gas, precipitate or colour ring.', 'Confirm with the specific confirmatory test.'],
  gasprep: ['Assemble airtight delivery apparatus.', 'Add reagent slowly and collect gas correctly.', 'Discard first jar if air contamination is likely.', 'Use confirmatory test on collected gas.'],
  crystallization: ['Weigh hydrated salt in a crucible.', 'Heat gently, cool and weigh.', 'Repeat until constant mass is reached.', 'Calculate water lost and percentage.'],
  saltanalysis: ['Perform preliminary dry tests.', 'Do anion tests on solution.', 'Do cation confirmatory tests group-wise.', 'Report only observations supported by evidence.'],
  electrolysis: ['Clean and weigh electrodes if needed.', 'Set DC current and start timer.', 'Observe cathode deposition and anode change.', 'Use Faraday law to calculate deposited mass.'],
  ph: ['Place small solution samples in clean tubes.', 'Add only 1-2 drops of indicator.', 'Compare colour with pH range.', 'Choose indicator suitable for transition range.'],
  functional: ['Add specific reagent to small organic sample.', 'Warm only when instructed.', 'Record colour, precipitate and smell safely.', 'Confirm with a second functional group test.'],
  thermochemistry: ['Measure acid/base volumes and initial temperature.', 'Mix in insulated cup and stir.', 'Record highest/lowest steady temperature.', 'Calculate q and enthalpy per mole.'],
  lassaigne: ['Prepare sodium fusion extract as teacher demonstration.', 'Cool, boil with water and filter.', 'Add element-specific reagents.', 'Record positive colour or precipitate.'],
};

export function procedureSteps(config) {
  return PROCEDURE_BANK[config.kind] || ['Set up apparatus.', 'Adjust variables.', 'Record readings.', 'Calculate result.'];
}

export function currentProcedureText(config, state) {
  const steps = procedureSteps(config);
  return `${Math.min(state.stepIndex + 1, steps.length)}/${steps.length}: ${steps[state.stepIndex % steps.length]}`;
}

export function addObservationTable(panel, config, state) {
  panel.section('Student observation book');
  const wrap = document.createElement('div');
  wrap.className = 'ix-lab-data-card';
  const title = document.createElement('div');
  title.className = 'ix-lab-data-title';
  title.textContent = 'Concordant readings / calculated result';
  const tableScroll = document.createElement('div');
  tableScroll.className = 'ix-lab-table-scroll';
  const table = document.createElement('table');
  table.className = 'ix-lab-data-table';
  tableScroll.appendChild(table);
  wrap.appendChild(title);
  wrap.appendChild(tableScroll);
  panel.body.appendChild(wrap);
  let lastKey = '';
  return {
    render(force = false) {
      const data = makeObservationData(config, state);
      const rows = state.observations.length ? state.observations : data.rows;
      const key = JSON.stringify([data.cols, rows]);
      if (!force && key === lastKey) return;
      lastKey = key;
      table.innerHTML = '';
      const thead = document.createElement('thead');
      const hr = document.createElement('tr');
      data.cols.forEach((c) => { const th = document.createElement('th'); th.textContent = c; hr.appendChild(th); });
      thead.appendChild(hr); table.appendChild(thead);
      const tbody = document.createElement('tbody');
      rows.slice(-6).forEach((row) => {
        const tr = document.createElement('tr');
        row.forEach((cell) => { const td = document.createElement('td'); td.textContent = String(cell); tr.appendChild(td); });
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
    },
  };
}

export function recordObservation(config, state) {
  const data = makeObservationData(config, state);
  const live = data.live || (data.rows && data.rows[data.rows.length - 1]);
  if (!live) return;
  state.observations.push(live);
  if (state.observations.length > 8) state.observations.shift();
  state.lastRecordedAt = (typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now();
}

function makeObservationData(config, s) {
  const f2 = (v, u = '') => `${Number(v).toFixed(2)}${u}`;
  const f3 = (v, u = '') => `${Number(v).toFixed(3)}${u}`;
  switch (config.kind) {
    case 'caliper': {
      const obs = s.sizeCm + s.zeroErrorCm; const main = Math.floor(obs * 10) / 10; const vernier = Math.round((obs - main) / 0.01);
      return { cols: ['Trial', 'MSR', 'Vernier', 'Corrected'], rows: [0, 1, 2].map((i) => ['T' + (i + 1), f2(main + i * 0.00, ' cm'), `${Math.max(0, Math.min(9, vernier + (i === 2 ? 1 : 0)))} div`, f2(s.sizeCm + (i - 1) * 0.005, ' cm')]), live: [`T${s.observations.length + 1}`, f2(main, ' cm'), `${Math.max(0, Math.min(9, vernier))} div`, f2(s.sizeCm, ' cm')] };
    }
    case 'micrometer': {
      const obs = s.diameterMm + s.zeroErrorMm; const sleeve = Math.floor(obs / 0.5) * 0.5; const circ = Math.round((obs - sleeve) / 0.01);
      return { cols: ['Trial', 'Sleeve', 'Thimble', 'Diameter'], rows: [0, 1, 2].map((i) => ['T' + (i + 1), f2(sleeve, ' mm'), `${circ + i % 2} div`, f2(s.diameterMm + (i - 1) * 0.004, ' mm')]), live: [`T${s.observations.length + 1}`, f2(sleeve, ' mm'), `${circ} div`, f2(s.diameterMm, ' mm')] };
    }
    case 'spherometer': {
      const hcm = s.sagittaMm / 10; const R = (s.legCm * s.legCm) / (6 * hcm) + hcm / 2;
      return { cols: ['Trial', 'l', 'h', 'R'], rows: [0, 1, 2].map((i) => ['T' + (i + 1), f2(s.legCm + (i - 1) * 0.02, ' cm'), f2(s.sagittaMm + (i - 1) * 0.01, ' mm'), f2(R + (i - 1) * 0.08, ' cm')]), live: [`T${s.observations.length + 1}`, f2(s.legCm, ' cm'), f2(s.sagittaMm, ' mm'), f2(R, ' cm')] };
    }
    case 'pendulum': {
      const L = s.lengthCm / 100; const T = 2 * Math.PI * Math.sqrt(L / 9.81); const t20 = T * 20 + s.timingBias; const g = 4 * Math.PI * Math.PI * L / Math.pow(t20 / 20, 2);
      return { cols: ['Trial', 'L', 't20', 'g'], rows: [0, 1, 2].map((i) => ['T' + (i + 1), `${s.lengthCm.toFixed(0)} cm`, f2(t20 + (i - 1) * 0.11, ' s'), f2(g + (i - 1) * 0.04, ' m/s²')]), live: [`T${s.observations.length + 1}`, `${s.lengthCm.toFixed(0)} cm`, f2(t20, ' s'), f2(g, ' m/s²')] };
    }
    case 'circuit': {
      const I = s.voltage / s.resistance;
      return { cols: ['Trial', 'V', 'I', 'R=V/I'], rows: [1, 2, 3].map((i) => { const v = Math.max(0.5, s.voltage * i / 3); const cur = v / s.resistance; return [String(i), f2(v, ' V'), f3(cur, ' A'), f2(v / cur, ' Ω')]; }), live: [`${s.observations.length + 1}`, f2(s.voltage, ' V'), f3(I, ' A'), f2(s.resistance, ' Ω')] };
    }
    case 'meterbridge': { const X = s.knownR * s.balanceCm / (100 - s.balanceCm); return { cols: ['Trial', 'R', 'l', 'X'], rows: [0, 1, 2].map((i) => ['T' + (i + 1), f2(s.knownR, ' Ω'), f2(s.balanceCm + (i - 1) * 0.4, ' cm'), f2(X + (i - 1) * 0.05, ' Ω')]), live: [`T${s.observations.length + 1}`, f2(s.knownR, ' Ω'), f2(s.balanceCm, ' cm'), f2(X, ' Ω')] }; }
    case 'potentiometer': { const e2 = s.e1 * s.l2 / s.l1; return { cols: ['E₁', 'l₁', 'l₂', 'E₂'], rows: [[f2(s.e1, ' V'), f2(s.l1, ' cm'), f2(s.l2, ' cm'), f3(e2, ' V')]], live: [f2(s.e1, ' V'), f2(s.l1, ' cm'), f2(s.l2, ' cm'), f3(e2, ' V')] }; }
    case 'calorimeter': {
      const cMetal = 0.39, cal = 12; const finalT = (s.metalMass * cMetal * s.metalTemp + (s.waterMass * 4.18 + cal) * s.waterTemp) / (s.metalMass * cMetal + s.waterMass * 4.18 + cal);
      return { cols: ['mₘ', 'Tₘ', 'mᵥ', 'Final T'], rows: [[`${s.metalMass} g`, `${s.metalTemp}°C`, `${s.waterMass} g`, f2(finalT, '°C')]], live: [`${s.metalMass} g`, `${s.metalTemp}°C`, `${s.waterMass} g`, f2(finalT, '°C')] };
    }
    case 'titration': {
      const req = config.title.includes('KMnO') ? (s.fasM * 25.0) / (5 * s.kmno4M) : s.unknownM * 25.0 / 0.10;
      return { cols: ['Trial', 'Initial', 'Final', 'Titre'], rows: [['Rough', '0.00', f2(req + 0.42, ' mL'), f2(req + 0.42, ' mL')], ['1', '0.00', f2(req + 0.04, ' mL'), f2(req + 0.04, ' mL')], ['2', '0.00', f2(req - 0.03, ' mL'), f2(req - 0.03, ' mL')]], live: [`${s.observations.length + 1}`, '0.00', f2(s.titreMl, ' mL'), f2(s.titreMl, ' mL')] };
    }
    case 'electrolysis': { const m = 63.546 * s.currentA * s.timeMin * 60 / (2 * 96485); return { cols: ['I', 'Time', 'Charge', 'Cu mass'], rows: [[f2(s.currentA, ' A'), `${s.timeMin.toFixed(0)} min`, `${(s.currentA*s.timeMin*60).toFixed(0)} C`, f3(m, ' g')]], live: [f2(s.currentA, ' A'), `${s.timeMin.toFixed(0)} min`, `${(s.currentA*s.timeMin*60).toFixed(0)} C`, f3(m, ' g')] }; }
    case 'thermochemistry': { const mass = s.acidMl + s.baseMl; const q = mass * 4.18 * s.deltaT; return { cols: ['Acid', 'Base', 'ΔT', 'q'], rows: [[`${s.acidMl} mL`, `${s.baseMl} mL`, f2(s.deltaT, '°C'), f2(q / 1000, ' kJ')]], live: [`${s.acidMl} mL`, `${s.baseMl} mL`, f2(s.deltaT, '°C'), f2(q / 1000, ' kJ')] }; }
    case 'ph': return { cols: ['Sample', 'pH', 'Indicator', 'Colour'], rows: [['Unknown', f2(s.pH, ''), s.indicator, indicatorColorName(s.indicator, s.pH)]], live: [`S${s.observations.length + 1}`, f2(s.pH, ''), s.indicator, indicatorColorName(s.indicator, s.pH)] };
    default: {
      const metrics = (config.metrics && config.metrics(s)) || [];
      return { cols: ['Reading', 'Value'], rows: metrics.slice(0, 4).map(([a, b]) => [a, b]), live: metrics[0] ? [metrics[0][0], metrics[0][1]] : ['Observation', 'ready'] };
    }
  }
}
