import { THREE } from './engine.js';
import { indicatorColorName, lassaigneResult, separationObservation, separationPrinciple, titrationStatus } from './lab3d-science.js';

export const SUBJECT = {
  physics: { color: '#D97706', metal: 0x9ca3af, glass: 0xbdd7ff },
  chemistry: { color: '#10B981', metal: 0x94a3b8, glass: 0xc7ddff },
};

export const CATION_COLORS = {
  Na: { label: 'Sodium Na⁺', flame: 0xffd34d, result: 'intense golden-yellow flame, persistent' },
  K: { label: 'Potassium K⁺', flame: 0xb98cff, result: 'pale lilac flame; use cobalt glass if sodium masks it' },
  Ca: { label: 'Calcium Ca²⁺', flame: 0xff6b3d, result: 'brick-red flame' },
  Sr: { label: 'Strontium Sr²⁺', flame: 0xff244a, result: 'crimson red flame' },
  Ba: { label: 'Barium Ba²⁺', flame: 0x9dff73, result: 'apple-green flame' },
  Cu: { label: 'Copper Cu²⁺', flame: 0x39e6d6, result: 'blue-green flame' },
};

export const ANION_RESULTS = {
  carbonate: 'CO₃²⁻: brisk effervescence with dilute HCl; CO₂ turns lime water milky.',
  chloride: 'Cl⁻: white AgCl precipitate soluble in dilute NH₄OH.',
  sulfate: 'SO₄²⁻: dense white BaSO₄ precipitate with BaCl₂, insoluble in dilute HCl.',
  nitrate: 'NO₃⁻: brown ring at the junction after FeSO₄ + concentrated H₂SO₄.',
  sulfide: 'S²⁻: black PbS precipitate with lead acetate paper.',
};

export const GROUP_RESULTS = {
  alcohol: 'Alcohol: fruity ester smell after ethanoic acid + conc. H₂SO₄; no 2,4-DNP precipitate.',
  aldehyde: 'Aldehyde: brick-red Cu₂O with Fehling solution and silver mirror with Tollens reagent.',
  ketone: 'Ketone: orange/yellow 2,4-DNP precipitate, but no Tollens silver mirror.',
  carboxylic: 'Carboxylic acid: brisk CO₂ effervescence with NaHCO₃ and blue litmus turns red.',
  phenol: 'Phenol: violet complex with neutral FeCl₃; white precipitate with bromine water.',
};

export const GAS_RESULTS = {
  co2: 'CO₂ collected by downward delivery into lime water: Ca(OH)₂ + CO₂ → CaCO₃↓ + H₂O.',
  h2: 'H₂ collected over water; a burning splint gives the pop test.',
  o2: 'O₂ relights a glowing splint; MnO₂ catalyses decomposition of H₂O₂.',
  nh3: 'NH₃ is alkaline, pungent and turns moist red litmus blue; collect by upward displacement of air.',
};

export const PRESETS = {
  'vernier-calipers': {
    subject: 'physics', kind: 'caliper', title: 'Real 3D Vernier Calipers', accent: '#D97706',
    subtitle: 'Least count 0.01 cm · main scale + vernier coincidence',
    controls: [
      { id: 'sizeCm', label: 'Object diameter', min: 1.2, max: 7.8, step: 0.01, value: 3.42, unit: ' cm', randomize: true },
      { id: 'zeroErrorCm', label: 'Zero error', min: -0.05, max: 0.05, step: 0.01, value: 0, unit: ' cm' },
    ],
    metrics(s) {
      const obs = s.sizeCm + s.zeroErrorCm;
      const corrected = obs - s.zeroErrorCm;
      const main = Math.floor(obs * 10) / 10;
      const vernier = Math.round((obs - main) / 0.01);
      return [
        ['Observed reading', `${obs.toFixed(2)} cm`],
        ['Main scale', `${main.toFixed(1)} cm`],
        ['Coinciding vernier', `${Math.max(0, Math.min(9, vernier))}th division`],
        ['Corrected value', `${corrected.toFixed(2)} cm`],
      ];
    },
    explain: 'Corrected reading = main scale reading + vernier coincidence × least count − zero error. The 3D jaws close on the specimen and the scale updates to the same numerical reading.',
  },
  'screw-gauge': {
    subject: 'physics', kind: 'micrometer', title: '3D Micrometer Screw Gauge', accent: '#D97706',
    subtitle: 'Pitch 0.5 mm · circular scale 50 divisions · LC 0.01 mm',
    controls: [
      { id: 'diameterMm', label: 'Wire diameter', min: 0.18, max: 2.8, step: 0.01, value: 0.76, unit: ' mm', randomize: true },
      { id: 'zeroErrorMm', label: 'Zero error', min: -0.05, max: 0.05, step: 0.01, value: 0, unit: ' mm' },
    ],
    metrics(s) {
      const obs = s.diameterMm + s.zeroErrorMm;
      const sleeve = Math.floor(obs / 0.5) * 0.5;
      const circular = Math.round((obs - sleeve) / 0.01);
      return [
        ['Sleeve reading', `${sleeve.toFixed(2)} mm`],
        ['Circular scale', `${circular} divisions`],
        ['Observed reading', `${obs.toFixed(2)} mm`],
        ['Corrected diameter', `${(obs - s.zeroErrorMm).toFixed(2)} mm`],
      ];
    },
    explain: 'Observed reading = pitch-scale reading + circular-scale division × least count. Subtract the zero error to obtain the true diameter.',
  },
  'spherometer': {
    subject: 'physics', kind: 'spherometer', title: '3D Spherometer', accent: '#D97706',
    subtitle: 'Radius of curvature from leg separation and sagitta',
    controls: [
      { id: 'legCm', label: 'Leg separation l', min: 3.0, max: 6.5, step: 0.1, value: 4.5, unit: ' cm' },
      { id: 'sagittaMm', label: 'Sagitta h', min: 0.35, max: 3.0, step: 0.01, value: 1.2, unit: ' mm', randomize: true },
    ],
    metrics(s) {
      const hcm = s.sagittaMm / 10;
      const radius = (s.legCm * s.legCm) / (6 * hcm) + hcm / 2;
      return [
        ['Mean leg distance l', `${s.legCm.toFixed(2)} cm`],
        ['Sagitta h', `${s.sagittaMm.toFixed(2)} mm`],
        ['Radius R', `${radius.toFixed(2)} cm`],
        ['Formula', 'R = l²/6h + h/2'],
      ];
    },
    explain: 'The central screw touches the curved glass surface. The sagitta h is the difference between plane and curved-surface readings.',
  },
  'simple-pendulum-g': {
    subject: 'physics', kind: 'pendulum', title: '3D Simple Pendulum', accent: '#D97706',
    subtitle: 'Measure time for repeated oscillations and calculate g',
    controls: [
      { id: 'lengthCm', label: 'Length L', min: 40, max: 120, step: 1, value: 80, unit: ' cm' },
      { id: 'timingBias', label: 'Stopwatch bias', min: -0.35, max: 0.35, step: 0.01, value: 0.04, unit: ' s' },
      { id: 'amplitude', label: 'Amplitude', min: 2, max: 12, step: 1, value: 6, unit: '°' },
    ],
    metrics(s) {
      const L = s.lengthCm / 100;
      const T = 2 * Math.PI * Math.sqrt(L / 9.81);
      const t20 = T * 20 + s.timingBias;
      const g = 4 * Math.PI * Math.PI * L / Math.pow(t20 / 20, 2);
      return [
        ['Time for 20 oscillations', `${t20.toFixed(2)} s`],
        ['Period T', `${(t20 / 20).toFixed(3)} s`],
        ['Measured g', `${g.toFixed(2)} m s⁻²`],
        ['Small-angle condition', s.amplitude <= 8 ? 'good' : 'too large: systematic error'],
      ];
    },
    explain: 'Use a small amplitude and time 20 oscillations to reduce reaction-time error. g = 4π²L/T².',
  },
  'parallelogram-of-forces': {
    subject: 'physics', kind: 'forceboard', title: '3D Parallelogram of Forces', accent: '#D97706',
    subtitle: 'Vector resultant and equilibrant on a Gravesand board',
    controls: [
      { id: 'pN', label: 'Force P', min: 1, max: 8, step: 0.1, value: 4.0, unit: ' N' },
      { id: 'qN', label: 'Force Q', min: 1, max: 8, step: 0.1, value: 3.0, unit: ' N' },
      { id: 'angleDeg', label: 'Angle θ', min: 25, max: 145, step: 1, value: 70, unit: '°' },
    ],
    metrics(s) {
      const a = THREE.MathUtils.degToRad(s.angleDeg);
      const R = Math.sqrt(s.pN * s.pN + s.qN * s.qN + 2 * s.pN * s.qN * Math.cos(a));
      const phi = Math.atan2(s.qN * Math.sin(a), s.pN + s.qN * Math.cos(a));
      return [
        ['Resultant R', `${R.toFixed(2)} N`],
        ['Direction from P', `${THREE.MathUtils.radToDeg(phi).toFixed(1)}°`],
        ['Equilibrant', `${R.toFixed(2)} N opposite R`],
        ['Check', 'ring centred when ΣF = 0'],
      ];
    },
    explain: 'The diagonal of the parallelogram gives the resultant. A third force equal and opposite to R is the equilibrant.',
  },
  'coefficient-of-friction': {
    subject: 'physics', kind: 'incline', title: '3D Friction Inclined Plane', accent: '#D97706',
    subtitle: 'Critical angle method: μ = tan θ',
    controls: [
      { id: 'angleDeg', label: 'Inclination θ', min: 5, max: 42, step: 0.5, value: 22, unit: '°' },
      { id: 'muStatic', label: 'Surface μₛ', min: 0.15, max: 0.85, step: 0.01, value: 0.40, unit: '' },
      { id: 'massG', label: 'Block mass', min: 50, max: 500, step: 10, value: 200, unit: ' g' },
    ],
    metrics(s) {
      const tan = Math.tan(THREE.MathUtils.degToRad(s.angleDeg));
      return [
        ['tan θ', tan.toFixed(3)],
        ['Actual μₛ', s.muStatic.toFixed(2)],
        ['State', tan >= s.muStatic ? 'sliding: limiting friction exceeded' : 'at rest'],
        ['Measured μ', `${tan.toFixed(3)} at critical angle`],
      ];
    },
    explain: 'At the angle of repose, the block is just about to slide, so μ = tan θ. Mass cancels out because both normal reaction and friction scale with weight.',
  },
  'hookes-law-spring': {
    subject: 'physics', kind: 'spring', title: '3D Hooke’s Law Apparatus', accent: '#D97706',
    subtitle: 'Load-extension graph and spring constant',
    controls: [
      { id: 'loadG', label: 'Load', min: 50, max: 650, step: 10, value: 250, unit: ' g' },
      { id: 'kNm', label: 'Spring constant k', min: 8, max: 45, step: 1, value: 22, unit: ' N m⁻¹' },
    ],
    metrics(s) {
      const F = s.loadG / 1000 * 9.81;
      const x = F / s.kNm;
      return [
        ['Load force F', `${F.toFixed(2)} N`],
        ['Extension x', `${(x * 100).toFixed(1)} cm`],
        ['Spring constant k', `${(F / x).toFixed(1)} N m⁻¹`],
        ['Limit', x < 0.22 ? 'elastic range' : 'near elastic limit'],
      ];
    },
    explain: 'Hooke’s law says F = kx within the elastic limit. The slope of the F–x graph gives k.',
  },
  'specific-heat-mixtures': {
    subject: 'physics', kind: 'calorimeter', title: '3D Calorimetry by Mixtures', accent: '#D97706',
    subtitle: 'Heat lost by hot metal = heat gained by water + calorimeter',
    controls: [
      { id: 'metalMass', label: 'Metal mass', min: 40, max: 180, step: 5, value: 80, unit: ' g' },
      { id: 'metalTemp', label: 'Metal temp', min: 70, max: 100, step: 1, value: 95, unit: ' °C' },
      { id: 'waterMass', label: 'Water mass', min: 50, max: 220, step: 5, value: 120, unit: ' g' },
      { id: 'waterTemp', label: 'Water temp', min: 15, max: 35, step: 1, value: 25, unit: ' °C' },
    ],
    metrics(s) {
      const cMetal = 0.39; // J g-1 C-1, copper-like
      const cal = 12;
      const finalT = (s.metalMass * cMetal * s.metalTemp + (s.waterMass * 4.18 + cal) * s.waterTemp) / (s.metalMass * cMetal + s.waterMass * 4.18 + cal);
      const measuredC = ((s.waterMass * 4.18 + cal) * (finalT - s.waterTemp)) / (s.metalMass * (s.metalTemp - finalT));
      return [
        ['Equilibrium temp', `${finalT.toFixed(1)} °C`],
        ['Measured c', `${measuredC.toFixed(2)} J g⁻¹ °C⁻¹`],
        ['Correction', 'calorimeter water equivalent included'],
        ['Reference', 'copper ≈ 0.39 J g⁻¹ °C⁻¹'],
      ];
    },
    explain: 'Energy conservation gives mₘcₘ(Tₘ−T) = (m_w c_w + water equivalent)(T−T_w). Stir gently and read the thermometer at eye level.',
  },
  'resonance-air-column': {
    subject: 'physics', kind: 'resonance', title: '3D Resonance Tube', accent: '#D97706',
    subtitle: 'Speed of sound from resonant air-column length',
    controls: [
      { id: 'lengthCm', label: 'First resonance length', min: 12, max: 32, step: 0.5, value: 19.5, unit: ' cm' },
      { id: 'tempC', label: 'Room temperature', min: 10, max: 35, step: 1, value: 24, unit: ' °C' },
      { id: 'diameterCm', label: 'Tube diameter', min: 2.0, max: 5.0, step: 0.1, value: 3.0, unit: ' cm' },
    ],
    metrics(s) {
      const v = 331 + 0.6 * s.tempC;
      const e = 0.3 * s.diameterCm;
      const f = v / (4 * ((s.lengthCm + e) / 100));
      return [
        ['End correction', `${e.toFixed(2)} cm`],
        ['Frequency', `${f.toFixed(0)} Hz`],
        ['Speed of sound', `${v.toFixed(1)} m s⁻¹`],
        ['Formula', 'v = 4f(l + e)'],
      ];
    },
    explain: 'A closed pipe resonates when L + e ≈ λ/4. End correction e is about 0.3d for the first resonance.',
  },
  'sonometer-laws': {
    subject: 'physics', kind: 'sonometer', title: '3D Sonometer', accent: '#D97706',
    subtitle: 'Frequency, tension, length and linear density',
    controls: [
      { id: 'lengthCm', label: 'Vibrating length', min: 30, max: 90, step: 1, value: 60, unit: ' cm' },
      { id: 'tensionN', label: 'Tension', min: 10, max: 90, step: 1, value: 40, unit: ' N' },
      { id: 'muGm', label: 'Linear density', min: 0.20, max: 1.8, step: 0.05, value: 0.75, unit: ' g m⁻¹' },
    ],
    metrics(s) {
      const mu = s.muGm / 1000;
      const f = (1 / (2 * s.lengthCm / 100)) * Math.sqrt(s.tensionN / mu);
      return [
        ['Fundamental f', `${f.toFixed(1)} Hz`],
        ['Law verified', 'f ∝ 1/L, √T, 1/√μ'],
        ['Tension', `${s.tensionN.toFixed(1)} N`],
        ['Linear density', `${s.muGm.toFixed(2)} g m⁻¹`],
      ];
    },
    explain: 'For a stretched string, f = (1/2L)√(T/μ). Move the bridges and change tension to see the relation in 3D.',
  },
  'ohms-law-resistivity': {
    subject: 'physics', kind: 'circuit', title: '3D Ohm’s Law Circuit', accent: '#D97706',
    subtitle: 'Ammeter in series, voltmeter in parallel',
    controls: [
      { id: 'voltage', label: 'Applied voltage', min: 0.5, max: 8, step: 0.1, value: 3.0, unit: ' V' },
      { id: 'resistance', label: 'Resistance wire R', min: 2, max: 25, step: 0.5, value: 8.0, unit: ' Ω' },
      { id: 'lengthCm', label: 'Wire length', min: 20, max: 100, step: 1, value: 60, unit: ' cm' },
    ],
    metrics(s) {
      const I = s.voltage / s.resistance;
      const area = Math.PI * Math.pow(0.00025, 2);
      const rho = s.resistance * area / (s.lengthCm / 100);
      return [
        ['Current I', `${I.toFixed(3)} A`],
        ['V/I', `${(s.voltage / I).toFixed(2)} Ω`],
        ['Resistivity ρ', `${rho.toExponential(2)} Ω m`],
        ['Graph', 'straight line through origin'],
      ];
    },
    explain: 'Ohm’s law gives V = IR. For a wire, ρ = RA/L. Keep temperature constant for accurate readings.',
  },
  'meter-bridge': {
    subject: 'physics', kind: 'meterbridge', title: '3D Meter Bridge', accent: '#D97706',
    subtitle: 'Null point method for unknown resistance',
    controls: [
      { id: 'knownR', label: 'Known resistance R', min: 1, max: 20, step: 0.5, value: 5.0, unit: ' Ω' },
      { id: 'balanceCm', label: 'Balance length l', min: 20, max: 80, step: 0.5, value: 55, unit: ' cm' },
    ],
    metrics(s) {
      const X = s.knownR * s.balanceCm / (100 - s.balanceCm);
      return [
        ['Unknown X', `${X.toFixed(2)} Ω`],
        ['Ratio arms', `${s.balanceCm.toFixed(1)} : ${(100 - s.balanceCm).toFixed(1)}`],
        ['Galvanometer', 'zero at balance point'],
        ['Formula', 'X/R = l/(100−l)'],
      ];
    },
    explain: 'At the null point no current flows through the galvanometer, so the wire lengths are proportional to resistances.',
  },
  'potentiometer-emf': {
    subject: 'physics', kind: 'potentiometer', title: '3D Potentiometer', accent: '#D97706',
    subtitle: 'Compare cell EMFs by balancing lengths',
    controls: [
      { id: 'e1', label: 'Standard EMF E₁', min: 1.0, max: 1.8, step: 0.01, value: 1.50, unit: ' V' },
      { id: 'l1', label: 'Balance length l₁', min: 40, max: 95, step: 0.5, value: 75, unit: ' cm' },
      { id: 'l2', label: 'Balance length l₂', min: 30, max: 95, step: 0.5, value: 62, unit: ' cm' },
    ],
    metrics(s) {
      const e2 = s.e1 * s.l2 / s.l1;
      return [
        ['Unknown EMF E₂', `${e2.toFixed(3)} V`],
        ['Ratio', `E₁/E₂ = l₁/l₂`],
        ['Null point', `${s.l2.toFixed(1)} cm for unknown cell`],
        ['Current draw', 'nearly zero at balance'],
      ];
    },
    explain: 'A potentiometer compares EMFs without drawing current from the test cell, making it more accurate than a voltmeter.',
  },
  'galvanometer-figure-of-merit': {
    subject: 'physics', kind: 'galvanometer', title: '3D Galvanometer', accent: '#D97706',
    subtitle: 'Figure of merit: current per division',
    controls: [
      { id: 'currentUa', label: 'Current', min: 5, max: 90, step: 1, value: 32, unit: ' µA' },
      { id: 'deflection', label: 'Deflection', min: 4, max: 35, step: 1, value: 16, unit: ' div' },
    ],
    metrics(s) {
      const k = s.currentUa / s.deflection;
      return [
        ['Figure of merit k', `${k.toFixed(2)} µA div⁻¹`],
        ['Current', `${s.currentUa.toFixed(0)} µA`],
        ['Deflection', `${s.deflection.toFixed(0)} divisions`],
        ['Linearity', s.deflection < 28 ? 'good scale region' : 'near end-scale'],
      ];
    },
    explain: 'The figure of merit is the current needed for one scale division. Take readings on both sides to remove zero error.',
  },
  'focal-length-mirror-lens': {
    subject: 'physics', kind: 'optics', title: '3D Optical Bench', accent: '#D97706',
    subtitle: 'Lens formula and sharp image position',
    controls: [
      { id: 'focalCm', label: 'Focal length f', min: 8, max: 25, step: 0.5, value: 15, unit: ' cm' },
      { id: 'objectCm', label: 'Object distance u', min: 25, max: 90, step: 1, value: 45, unit: ' cm' },
    ],
    metrics(s) {
      const v = 1 / (1 / s.focalCm - 1 / s.objectCm);
      const mag = v / s.objectCm;
      return [
        ['Image distance v', `${v.toFixed(1)} cm`],
        ['Magnification', `${mag.toFixed(2)}×`],
        ['Lens formula', '1/f = 1/v + 1/u'],
        ['Screen', v > 0 && v < 140 ? 'real focused image' : 'move object farther'],
      ];
    },
    explain: 'The screen is placed where refracted rays actually meet. For a convex lens, 1/f = 1/v + 1/u.',
  },
  'prism-minimum-deviation': {
    subject: 'physics', kind: 'prism', title: '3D Prism Spectrometer', accent: '#D97706',
    subtitle: 'Refractive index from angle of minimum deviation',
    controls: [
      { id: 'angleA', label: 'Prism angle A', min: 45, max: 70, step: 0.5, value: 60, unit: '°' },
      { id: 'devD', label: 'Minimum deviation D', min: 30, max: 55, step: 0.5, value: 42, unit: '°' },
    ],
    metrics(s) {
      const A = THREE.MathUtils.degToRad(s.angleA);
      const D = THREE.MathUtils.degToRad(s.devD);
      const n = Math.sin((A + D) / 2) / Math.sin(A / 2);
      return [
        ['Refractive index μ', n.toFixed(3)],
        ['A + D', `${(s.angleA + s.devD).toFixed(1)}°`],
        ['Formula', 'μ = sin((A+D)/2)/sin(A/2)'],
        ['Ray path', 'symmetric at minimum deviation'],
      ];
    },
    explain: 'At minimum deviation the ray path through the prism is symmetric. The telescope angle gives D.',
  },
  'lab-apparatus-safety': {
    subject: 'chemistry', kind: 'apparatus', title: '3D Chemistry Apparatus Bench', accent: '#10B981',
    subtitle: 'Realistic glassware, burner, clamp stand and safety zone',
    controls: [
      { type: 'select', id: 'focus', label: 'Focus apparatus', value: 'burette', options: [
        ['burette', 'Burette + stand'], ['pipette', 'Pipette'], ['flask', 'Conical flask'], ['burner', 'Bunsen burner'], ['beaker', 'Beaker'],
      ] },
    ],
    metrics(s) { return [['Selected item', s.focus], ['Safety rule', 'goggles, apron, clear bench'], ['Glassware', 'vertical, clamped, eye-level readings'], ['Free upgrade', 'No external 3D assets used']]; },
    explain: 'A real practical begins with correct apparatus handling. The 3D bench shows the same objects used in later simulations.',
  },
  'separation-techniques': {
    subject: 'chemistry', kind: 'separation', title: '3D Separation Lab', accent: '#10B981',
    subtitle: 'Filtration, distillation, evaporation and paper chromatography',
    controls: [
      { type: 'select', id: 'method', label: 'Technique', value: 'distillation', options: [
        ['filtration', 'Filtration'], ['distillation', 'Simple distillation'], ['evaporation', 'Evaporation'], ['chromatography', 'Paper chromatography'],
      ] },
      { id: 'temperature', label: 'Temperature', min: 25, max: 110, step: 1, value: 78, unit: ' °C' },
    ],
    metrics(s) { return [['Technique', s.method], ['Temperature', `${s.temperature.toFixed(0)} °C`], ['Principle', separationPrinciple(s.method)], ['Observation', separationObservation(s.method, s.temperature)]]; },
    explain: 'Separation methods depend on physical properties: particle size, boiling point, volatility, solubility and adsorption.',
  },
  'acid-base-titration': {
    subject: 'chemistry', kind: 'titration', title: '3D Acid–Base Titration', accent: '#10B981',
    subtitle: '0.10 M HCl against 25.0 mL NaOH · endpoint is over-shootable',
    controls: [
      { id: 'titreMl', label: 'Titre delivered', min: 0, max: 50, step: 0.05, value: 22.5, unit: ' mL' },
      { id: 'unknownM', label: 'NaOH concentration', min: 0.06, max: 0.14, step: 0.001, value: 0.09, unit: ' M', randomize: true },
      { type: 'select', id: 'indicator', label: 'Indicator', value: 'phenolphthalein', options: [['phenolphthalein', 'Phenolphthalein'], ['methyl', 'Methyl orange']] },
    ],
    metrics(s) {
      const required = s.unknownM * 25.0 / 0.10;
      const calc = 0.10 * s.titreMl / 25.0;
      return [['Endpoint titre', `${required.toFixed(2)} mL`], ['Your titre', `${s.titreMl.toFixed(2)} mL`], ['Calculated NaOH', `${calc.toFixed(3)} M`], ['Status', titrationStatus(s.titreMl, required)]];
    },
    explain: 'For NaOH + HCl, the mole ratio is 1:1. M(NaOH) × 25.0 = 0.100 × V(HCl).',
  },
  'flame-tests': {
    subject: 'chemistry', kind: 'flame', title: '3D Flame Test Bench', accent: '#10B981',
    subtitle: 'Clean loop, dip salt, observe characteristic emission colour',
    controls: [
      { type: 'select', id: 'cation', label: 'Salt cation', value: 'Na', options: Object.entries(CATION_COLORS).map(([k, v]) => [k, v.label]) },
      { id: 'contamination', label: 'Sodium contamination', min: 0, max: 100, step: 5, value: 15, unit: '%' },
    ],
    metrics(s) { const c = CATION_COLORS[s.cation]; return [['Flame colour', c.result], ['Loop cleaning', s.contamination < 25 ? 'clean enough' : 'yellow contamination likely'], ['Observation', c.label], ['Quantum reason', 'excited electrons emit fixed wavelengths']]; },
    explain: 'Each metal ion emits a unique flame colour because its electrons have fixed energy gaps. Sodium contamination is the classic practical trap.',
  },
  'anion-tests': {
    subject: 'chemistry', kind: 'testtubes', title: '3D Anion Test Rack', accent: '#10B981',
    subtitle: 'Reagent, gas/precipitate and confirmatory observation',
    controls: [
      { type: 'select', id: 'anion', label: 'Unknown anion', value: 'chloride', options: Object.keys(ANION_RESULTS).map((k) => [k, k]) },
      { id: 'drops', label: 'Reagent drops', min: 0, max: 10, step: 1, value: 5, unit: '' },
    ],
    metrics(s) { return [['Anion', s.anion], ['Confirmatory result', ANION_RESULTS[s.anion]], ['Drops added', `${s.drops}`], ['Technique', 'add reagent slowly and record precipitate/gas']]; },
    explain: 'Anion analysis is evidence-based: a preliminary reaction plus confirmatory test prevents false positives.',
  },
  'gas-preparation': {
    subject: 'chemistry', kind: 'gasprep', title: '3D Gas Preparation Setup', accent: '#10B981',
    subtitle: 'Delivery tube, collection jar and confirmatory test',
    controls: [
      { type: 'select', id: 'gas', label: 'Gas', value: 'co2', options: [['co2', 'CO₂'], ['h2', 'H₂'], ['o2', 'O₂'], ['nh3', 'NH₃']] },
      { id: 'rate', label: 'Generation rate', min: 10, max: 100, step: 5, value: 55, unit: '%' },
    ],
    metrics(s) { return [['Gas prepared', s.gas.toUpperCase()], ['Confirmatory test', GAS_RESULTS[s.gas]], ['Rate', `${s.rate}%`], ['Collection', s.gas === 'nh3' ? 'upward displacement of air' : 'over water / displacement']]; },
    explain: 'The 3D model shows the reaction flask, delivery tube and collection method. Collection depends on solubility and density of the gas.',
  },
  'water-of-crystallization': {
    subject: 'chemistry', kind: 'crystallization', title: '3D Water of Crystallization', accent: '#10B981',
    subtitle: 'Heat hydrate to constant mass and compute water percentage',
    controls: [
      { id: 'hydrateMass', label: 'Hydrated salt mass', min: 1.0, max: 6.0, step: 0.01, value: 2.50, unit: ' g' },
      { id: 'residueMass', label: 'Anhydrous residue', min: 0.4, max: 4.0, step: 0.01, value: 1.60, unit: ' g' },
      { id: 'heating', label: 'Heating progress', min: 0, max: 100, step: 5, value: 75, unit: '%' },
    ],
    metrics(s) { const water = Math.max(0, s.hydrateMass - s.residueMass); return [['Water lost', `${water.toFixed(2)} g`], ['Water %', `${(100 * water / s.hydrateMass).toFixed(1)}%`], ['Constant mass', s.heating > 90 ? 'achieved' : 'keep heating/cooling/weighing'], ['Observation', 'blue crystals turn pale/white if CuSO₄·5H₂O']]; },
    explain: 'Heat gently, cool in a desiccator and weigh. Repeat until mass is constant; mass lost is water of crystallization.',
  },
  'redox-titration-kmno4': {
    subject: 'chemistry', kind: 'titration', title: '3D KMnO₄ Redox Titration', accent: '#10B981',
    subtitle: 'Self-indicator endpoint: faint permanent pink',
    controls: [
      { id: 'titreMl', label: 'KMnO₄ titre', min: 0, max: 40, step: 0.05, value: 18.4, unit: ' mL' },
      { id: 'fasM', label: 'FAS concentration', min: 0.04, max: 0.12, step: 0.001, value: 0.08, unit: ' M' },
      { id: 'kmno4M', label: 'KMnO₄ concentration', min: 0.01, max: 0.04, step: 0.001, value: 0.02, unit: ' M' },
    ],
    metrics(s) { const req = (s.fasM * 25.0) / (5 * s.kmno4M); return [['Theoretical titre', `${req.toFixed(2)} mL`], ['Your titre', `${s.titreMl.toFixed(2)} mL`], ['Endpoint', Math.abs(s.titreMl - req) <= 0.15 ? 'faint permanent pink' : s.titreMl < req ? 'still colourless' : 'overshot pink'], ['Stoichiometry', 'MnO₄⁻ : Fe²⁺ = 1 : 5']]; },
    explain: 'Acidified KMnO₄ oxidizes Fe²⁺ to Fe³⁺. KMnO₄ is its own indicator; the endpoint is a faint pink that persists.',
  },
  'salt-analysis-scheme': {
    subject: 'chemistry', kind: 'saltanalysis', title: '3D Full Salt Analysis', accent: '#10B981',
    subtitle: 'Systematic cation + anion identification workflow',
    controls: [
      { type: 'select', id: 'cation', label: 'Cation path', value: 'Cu', options: Object.entries(CATION_COLORS).map(([k, v]) => [k, v.label]) },
      { type: 'select', id: 'anion', label: 'Anion path', value: 'sulfate', options: Object.keys(ANION_RESULTS).map((k) => [k, k]) },
    ],
    metrics(s) { return [['Cation evidence', CATION_COLORS[s.cation].result], ['Anion evidence', ANION_RESULTS[s.anion]], ['Report format', 'preliminary + confirmatory tests'], ['Error control', 'use clean test tubes and small reagent volumes']]; },
    explain: 'The full scheme narrows evidence step by step instead of guessing from one observation.',
  },
  'electrolysis-cuso4': {
    subject: 'chemistry', kind: 'electrolysis', title: '3D CuSO₄ Electrolysis', accent: '#10B981',
    subtitle: 'Copper deposition calculated by Faraday’s law',
    controls: [
      { id: 'currentA', label: 'Current', min: 0.1, max: 2.0, step: 0.05, value: 0.55, unit: ' A' },
      { id: 'timeMin', label: 'Time', min: 1, max: 45, step: 1, value: 20, unit: ' min' },
    ],
    metrics(s) { const m = 63.546 * s.currentA * s.timeMin * 60 / (2 * 96485); return [['Cu deposited', `${m.toFixed(3)} g`], ['Cathode', 'mass increases, reddish Cu deposit'], ['Anode', 'dissolves if copper electrode'], ['Law', 'm = ZIt = MIt/nF']]; },
    explain: 'Cu²⁺ gains two electrons at the cathode: Cu²⁺ + 2e⁻ → Cu(s). Faraday’s law predicts the deposited mass.',
  },
  'ph-and-indicators': {
    subject: 'chemistry', kind: 'ph', title: '3D pH & Indicator Lab', accent: '#10B981',
    subtitle: 'Indicator colour against actual pH',
    controls: [
      { id: 'pH', label: 'Solution pH', min: 1, max: 14, step: 0.1, value: 7.0, unit: '' },
      { type: 'select', id: 'indicator', label: 'Indicator', value: 'universal', options: [['universal', 'Universal indicator'], ['litmus', 'Litmus'], ['phenolphthalein', 'Phenolphthalein'], ['methyl', 'Methyl orange']] },
    ],
    metrics(s) { return [['pH', s.pH.toFixed(1)], ['Colour', indicatorColorName(s.indicator, s.pH)], ['Nature', s.pH < 7 ? 'acidic' : s.pH > 7 ? 'basic' : 'neutral'], ['Best indicator', 'choose transition range near endpoint']]; },
    explain: 'Indicators are weak dyes whose structures and colours change over specific pH ranges.',
  },
  'organic-functional-groups': {
    subject: 'chemistry', kind: 'functional', title: '3D Organic Functional Group Tests', accent: '#10B981',
    subtitle: 'Observation-driven identification of organic groups',
    controls: [
      { type: 'select', id: 'group', label: 'Functional group', value: 'aldehyde', options: Object.keys(GROUP_RESULTS).map((k) => [k, k]) },
      { id: 'reagentDrops', label: 'Reagent drops', min: 1, max: 10, step: 1, value: 4, unit: '' },
    ],
    metrics(s) { return [['Functional group', s.group], ['Expected test', GROUP_RESULTS[s.group]], ['Reagent drops', `${s.reagentDrops}`], ['Observation quality', 'record colour, precipitate and smell carefully']]; },
    explain: 'Functional group tests are selective chemical reactions. One positive test is confirmed with a second observation when possible.',
  },
  'heat-of-neutralization': {
    subject: 'chemistry', kind: 'thermochemistry', title: '3D Heat of Neutralization', accent: '#10B981',
    subtitle: 'Temperature rise in insulated calorimeter',
    controls: [
      { id: 'acidMl', label: 'Acid volume', min: 20, max: 75, step: 1, value: 50, unit: ' mL' },
      { id: 'baseMl', label: 'Base volume', min: 20, max: 75, step: 1, value: 50, unit: ' mL' },
      { id: 'deltaT', label: 'Temperature rise', min: 1, max: 9, step: 0.1, value: 6.7, unit: ' °C' },
    ],
    metrics(s) { const mass = s.acidMl + s.baseMl; const q = mass * 4.18 * s.deltaT; const mol = Math.min(s.acidMl, s.baseMl) / 1000; return [['Heat evolved q', `${(q / 1000).toFixed(2)} kJ`], ['ΔH neutralization', `${(-q / 1000 / mol).toFixed(1)} kJ mol⁻¹`], ['Total solution mass', `${mass.toFixed(0)} g approx.`], ['Assumption', 'density 1 g mL⁻¹, c = 4.18 J g⁻¹ °C⁻¹']]; },
    explain: 'For strong acid + strong base, heat of neutralization is close to −57 kJ mol⁻¹ when heat losses are minimized.',
  },
  'lassaigne-test': {
    subject: 'chemistry', kind: 'lassaigne', title: '3D Lassaigne’s Test', accent: '#10B981',
    subtitle: 'Sodium fusion extract tests for N, S and halogens',
    controls: [
      { type: 'select', id: 'element', label: 'Element to test', value: 'nitrogen', options: [['nitrogen', 'Nitrogen'], ['sulfur', 'Sulfur'], ['chlorine', 'Chlorine'], ['bromine', 'Bromine'], ['iodine', 'Iodine']] },
      { id: 'extractStrength', label: 'Extract strength', min: 20, max: 100, step: 5, value: 70, unit: '%' },
    ],
    metrics(s) { return [['Element', s.element], ['Positive observation', lassaigneResult(s.element)], ['Extract strength', `${s.extractStrength}%`], ['Safety', 'sodium fusion is demonstration-only in real labs']]; },
    explain: 'Sodium fusion converts covalently bound elements into ionic salts that can be detected in aqueous extract.',
  },
};
