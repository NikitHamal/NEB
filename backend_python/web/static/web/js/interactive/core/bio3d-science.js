// Scientific calculation layer shared by the NEB Biology 3D models and runtime.
// The goal is to keep every visual label, live reading and recorded observation
// consistent with the same deterministic formulas instead of hard-coded display text.

function n(value, fallback = 0) {
  const parsed = parseFloat(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function pct(value, digits = 0) { return `${Number(value).toFixed(digits)}%`; }
function fixed(value, digits = 2, unit = '') { return `${Number(value).toFixed(digits)}${unit}`; }
function clamp(value, min, max) { return Math.max(min, Math.min(max, value)); }
function pow10(exp) { return 10 ** Math.max(0, Math.round(n(exp, 0))); }
function safeDiv(a, b, fallback = 0) { return Math.abs(b) > 1e-9 ? a / b : fallback; }

const FLOWER_FORMULAE = {
  Solanaceae: 'K(5) C(5) A5 G(2), actinomorphic',
  Fabaceae: 'K(5) C1+2+(2) A(9)+1 G1, papilionaceous',
  Liliaceae: 'P3+3 A3+3 G(3), monocot perigone',
};

const INFLORESCENCE_FEATURES = {
  raceme: 'elongated axis; pedicellate flowers',
  spike: 'elongated axis; sessile flowers',
  umbel: 'pedicels arise from one point',
  capitulum: 'many florets on a flat receptacle',
  cyme: 'main axis ends in a flower first',
};

const SPECIMEN_FEATURES = {
  Bacteria: 'unicellular prokaryote; no true nucleus',
  Oscillatoria: 'filamentous cyanobacterium; gliding trichomes',
  Spirogyra: 'spiral chloroplasts in green filaments',
  Rhizopus: 'sporangia on sporangiophores; rhizoids',
  Mushroom: 'basidiocarp with cap, gills and stipe',
  Yeast: 'unicellular fungus; budding reproduction',
  Moss: 'bryophyte with capsule-bearing sporophyte',
  Fern: 'vascular cryptogam with sori on fronds',
  Pine: 'gymnosperm; cones and naked seeds',
  Monocot: 'parallel venation; fibrous roots',
  Dicot: 'reticulate venation; tap root',
  Lichen: 'symbiosis of alga/cyanobacterium and fungus',
};

const ANIMAL_FEATURES = {
  Amoeba: 'irregular cell; pseudopodia',
  Hydra: 'cnidarian; tentacles and gastrovascular cavity',
  Liverfluke: 'flatworm parasite; leaf-like body',
  Ascaris: 'roundworm; cylindrical unsegmented body',
  Leech: 'annelid; suckers at both ends',
  Earthworm: 'segmented annelid with clitellum',
  Prawn: 'arthropod; jointed appendages and carapace',
  Silkworm: 'insect larva; prolegs and silk gland',
  Honeybee: 'insect; three body regions and wings',
  Snail: 'mollusc; muscular foot and shell',
  Starfish: 'echinoderm; pentaradial adult symmetry',
  Shark: 'cartilaginous fish; placoid scales',
  Rohu: 'bony fish; operculum and fins',
  Frog: 'amphibian; moist skin and hind limbs',
  Lizard: 'reptile; dry scales and claws',
  Pigeon: 'bird; feathers and beak',
  Rabbit: 'mammal; hair and mammary glands',
};

const TS_FEATURES = {
  'dicot root': 'radial xylem, star-shaped centre, no pith',
  'monocot root': 'polyarch xylem with large central pith',
  'dicot stem': 'vascular bundles in a ring; cambium present',
  'monocot stem': 'scattered closed vascular bundles',
};

const TISSUE_FEATURES = {
  'squamous epithelium': 'flat tile-like cells with central nuclei',
  'muscle fibres': 'elongated contractile fibres; striations visible',
  'blood smear': 'many RBCs, fewer WBCs and platelets',
};

const FROG_STAGE = {
  'fertilized egg': 'single zygote within jelly coat',
  cleavage: 'blastomeres form by rapid mitosis',
  blastula: 'blastocoel cavity visible',
  gastrula: 'germ layers begin to form',
};

function mitosisRows(state, animal = false) {
  const total = Math.max(1, Math.round(n(state.cells, animal ? 60 : 100)));
  const field = Math.round(n(state.field, 2));
  const dividingFrac = animal ? 0.16 : 0.115;
  const wave = Math.sin(field * 1.7) * (animal ? 0.018 : 0.014);
  const dividing = clamp(Math.round(total * (dividingFrac + wave)), 1, total - 1);
  const prophase = Math.round(dividing * 0.55);
  const metaphase = Math.round(dividing * 0.20);
  const anaphase = Math.max(1, Math.round(dividing * 0.10));
  const telophase = Math.max(1, dividing - prophase - metaphase - anaphase);
  const interphase = Math.max(0, total - dividing);
  return [
    ['Cells counted', total],
    ['Interphase', interphase],
    ['Dividing cells', `${dividing} (${pct((dividing / total) * 100, 1)})`],
    ['Phase spread', `P${prophase} M${metaphase} A${anaphase} T${telophase}`],
    ['Mitotic index', pct((dividing / total) * 100, 1)],
  ];
}

function mushroomRisk(state) {
  if (state.volva === 'yes' && String(state.sporePrint).toLowerCase() === 'white') return 'high-risk Amanita-like warning';
  if (state.volva === 'yes') return 'volva present: do not eat';
  return 'edibility not concluded from one trait';
}

function urineObservation(test, intensity) {
  const level = n(intensity, 0) > 60 ? 'strong positive' : n(intensity, 0) > 20 ? 'weak positive' : 'negative';
  const reaction = {
    urea: 'alkaline ammonia release',
    sugar: 'brick-red/green reducing sugar scale',
    albumin: 'coagulum/ring at interface',
    'bile salts': 'sulphur ring / surface-tension effect',
  }[test] || 'standard qualitative reaction';
  return `${level}; ${reaction}`;
}

function bloodGlucoseBand(glucose) {
  if (glucose < 70) return 'low';
  if (glucose < 140) return 'normal/random acceptable';
  if (glucose < 200) return 'elevated';
  return 'high';
}

function jointType(joint) {
  const j = String(joint || '').toLowerCase();
  if (j.includes('suture')) return 'fixed/immovable fibrous joint';
  if (j.includes('hinge') || j.includes('knee') || j.includes('elbow')) return 'hinge synovial joint';
  if (j.includes('shoulder') || j.includes('hip') || j.includes('ball')) return 'ball-and-socket synovial joint';
  if (j.includes('neck') || j.includes('pivot')) return 'pivot synovial joint';
  if (j.includes('spine')) return 'slightly movable/cartilaginous series';
  return 'movable joint';
}

function physiologyRows(kind, state) {
  if (kind === 'transpiration') {
    const time = Math.max(1, n(state.time, 75));
    const base = 60 / time;
    const surfaceFactor = state.surface === 'upper' ? 0.45 : 1.0;
    return [
      ['Leaf surface', state.surface || 'lower'],
      ['Colour-change time', fixed(time, 0, ' s')],
      ['Relative rate', fixed(base * surfaceFactor, 2, ' units/min')],
      ['Inference', state.surface === 'upper' ? 'lower stomatal frequency expected' : 'higher stomatal frequency expected'],
    ];
  }
  if (kind === 'respiration') {
    const mass = Math.max(1, n(state.mass, 20));
    const movement = n(state.movement, 18);
    const rate = movement / mass;
    return [
      ['Seed mass', fixed(mass, 0, ' g')],
      ['Manometer movement', fixed(movement, 0, ' mm')],
      ['Respiration index', fixed(rate, 2, ' mm/g')],
      ['Result', rate > 0.8 ? 'actively respiring sample' : 'slow respiration'],
    ];
  }
  if (kind === 'anaerobic') {
    const co2 = n(state.yeast, 70) * n(state.time, 25) / 100;
    return [
      ['Yeast activity', pct(n(state.yeast, 70), 0)],
      ['Time', fixed(n(state.time, 25), 0, ' min')],
      ['CO2 output', fixed(co2, 1, ' units')],
      ['Result', co2 > 20 ? 'rapid fermentation' : 'slow fermentation'],
    ];
  }
  if (kind === 'phototropism') {
    const curvature = clamp(n(state.light, 70) * n(state.hours, 36) / 90, 0, 70);
    return [
      ['Light intensity', pct(n(state.light, 70), 0)],
      ['Exposure', fixed(n(state.hours, 36), 0, ' h')],
      ['Curvature', fixed(curvature, 0, ' deg')],
      ['Result', 'shoot bends toward unilateral light'],
    ];
  }
  if (kind === 'apicalBud') {
    const growth = (100 - n(state.auxin, 35)) * n(state.days, 10) / 100;
    return [
      ['Days', n(state.days, 10)],
      ['Auxin level', pct(n(state.auxin, 35), 0)],
      ['Lateral growth', fixed(growth, 1, ' cm')],
      ['Result', growth > 5 ? 'apical dominance released' : 'apical dominance still strong'],
    ];
  }
  if (kind === 'suction') {
    const movement = n(state.leafArea, 60) * n(state.minutes, 30) / 1000;
    return [
      ['Leaf area', fixed(n(state.leafArea, 60), 0, ' cm2')],
      ['Time', fixed(n(state.minutes, 30), 0, ' min')],
      ['Water-column movement', fixed(movement, 2, ' cm')],
      ['Result', movement > 1.5 ? 'strong transpiration pull' : 'moderate transpiration pull'],
    ];
  }
  return [['Observation', 'physiology setup'], ['Result', 'record with reason']];
}

export function getBiologyMetricRows(config = {}, state = {}, recordCount = 0) {
  const kind = config.kind || 'unknown';
  if (kind === 'microscope') {
    const mag = n(state.magnification, 400);
    const focus = n(state.focus, 66);
    const clarity = clamp(100 - Math.abs(focus - 66) * 2.2, 0, 100);
    return [['Magnification', `${mag}x`], ['Fine focus', pct(focus, 0)], ['Image clarity', pct(clarity, 0)], ['Observation', clarity > 70 ? 'cell walls/nuclei clear' : 'refocus before drawing']];
  }
  if (kind === 'mitosis') return mitosisRows(state, false);
  if (kind === 'animalMitosis') return mitosisRows(state, true);
  if (kind === 'herbarium') {
    const score = n(state.dryness, 82) * 0.55 + n(state.labelScore, 75) * 0.45;
    return [['Dryness', pct(n(state.dryness, 82), 0)], ['Label completeness', pct(n(state.labelScore, 75), 0)], ['Preservation score', pct(score, 0)], ['Result', score >= 80 ? 'exam-ready herbarium sheet' : 'improve drying/label data']];
  }
  if (kind === 'mushroom') return [['Spore print', state.sporePrint || 'brown'], ['Volva', state.volva || 'no'], ['Diagnostic warning', mushroomRisk(state)], ['Result', 'never classify edible by colour alone']];
  if (kind === 'flower') return [['Family', state.family || 'Solanaceae'], ['Whorl opened', `${state.whorl || 3}/4`], ['Floral formula', FLOWER_FORMULAE[state.family] || FLOWER_FORMULAE.Solanaceae], ['Result', 'identify family using multiple floral traits']];
  if (kind === 'inflorescence') return [['Type', state.type || 'raceme'], ['Pedicel length', fixed(n(state.pedicel, 2), 1, ' mm')], ['Diagnostic character', INFLORESCENCE_FEATURES[state.type] || INFLORESCENCE_FEATURES.raceme]];
  if (kind === 'culture') {
    const colonies = Math.round(n(state.colonies, 54));
    const dilution = Math.round(n(state.dilution, 3));
    const cfu = colonies * pow10(dilution);
    return [['Colonies', colonies], ['Dilution', `10^-${dilution}`], ['Estimated CFU', `${cfu.toExponential(2)} / mL`], ['Result', colonies >= 30 && colonies <= 300 ? 'countable culture plate' : 'outside ideal count range']];
  }
  if (kind === 'pond' || kind === 'pondZoo') {
    const pH = n(state.pH, kind === 'pondZoo' ? 7.4 : 7.2);
    const oxygen = n(state.oxygen, 6.8);
    const turbidity = n(state.turbidity, 32);
    const water = pH < 6.5 || pH > 8.5 ? 'pH stress likely' : kind === 'pondZoo' && oxygen < 5 ? 'low dissolved oxygen' : 'freshwater range';
    const rows = [['Water pH', fixed(pH, 1)], ['Water quality', water]];
    if (kind === 'pondZoo') rows.splice(1, 0, ['Dissolved oxygen', fixed(oxygen, 1, ' mg/L')]);
    else rows.splice(1, 0, ['Turbidity', fixed(turbidity, 0, ' NTU')]);
    rows.push(['Survey focus', kind === 'pondZoo' ? 'plankton + consumers' : 'producer/consumer/decomposer web']);
    return rows;
  }
  if (kind === 'quadrat') {
    const density = safeDiv(n(state.plants, 22), n(state.area, 1));
    return [['Individuals counted', Math.round(n(state.plants, 22))], ['Quadrat area', fixed(n(state.area, 1), 2, ' m2')], ['Population density', fixed(density, 2, ' plants/m2')], ['Result', 'repeat quadrats for a reliable mean']];
  }
  if (kind === 'quadrat2') {
    const total = Math.max(1, n(state.total, 10));
    const hits = clamp(n(state.hits, 7), 0, total);
    return [['Quadrats present', `${hits}/${total}`], ['Frequency', pct((hits / total) * 100, 1)], ['Result', hits / total > 0.6 ? 'common species' : 'patchy distribution']];
  }
  if (kind === 'soil') {
    const wet = n(state.wetMass, 80), dry = Math.min(n(state.dryMass, 62), wet);
    const moisture = safeDiv(wet - dry, dry) * 100;
    const whc = safeDiv(wet - dry, wet) * 100;
    return [['Wet mass', fixed(wet, 0, ' g')], ['Dry mass', fixed(dry, 0, ' g')], ['Moisture content', pct(moisture, 1)], ['Water held', pct(whc, 1)]];
  }
  if (kind === 'specimens') return [['Specimen', state.specimen || 'Spirogyra'], ['Matched characters', pct(n(state.confidence, 80), 0)], ['Diagnostic feature', SPECIMEN_FEATURES[state.specimen] || 'observe diagnostic structures'], ['Result', 'identify from structure, not colour alone']];
  if (kind === 'microscopeParts') {
    const obj = n(String(state.objective || '40x').replace('x', ''), 40);
    return [['Objective lens', `${obj}x`], ['Total magnification', `${obj * 10}x with 10x eyepiece`], ['Light aperture', pct(n(state.diaphragm, 65), 0)], ['Handling', 'start low power; use fine focus on high power']];
  }
  if (kind === 'fossil') return [['Visible chambers', Math.round(n(state.chambers, 9))], ['Preservation', pct(n(state.ageScore, 75), 0)], ['Evolution evidence', 'hard parts preserve morphology over geologic time']];
  if (kind === 'animals') return [['Specimen', state.animal || 'Earthworm'], ['Characters matched', `${n(state.featureScore, 4)}/5`], ['Diagnostic feature', ANIMAL_FEATURES[state.animal] || 'observe external morphology'], ['Result', 'classify by body plan and characters']];
  if (kind === 'dissection') return [['Animal model', state.model || 'Earthworm'], ['Dissection opened', pct(n(state.opened, 70), 0)], ['Visible canal', state.model === 'Earthworm' ? 'pharynx, crop, gizzard, intestine' : state.model === 'Frog' ? 'stomach, intestine, liver region' : 'stomach, small and large intestine'], ['Result', 'trace alimentary canal from mouth to anus']];
  if (kind === 'conservation') {
    const score = n(state.habitat, 62) * 0.65 + n(state.corridor, 45) * 0.35;
    return [['Habitat intactness', pct(n(state.habitat, 62), 0)], ['Corridor strength', pct(n(state.corridor, 45), 0)], ['Connectivity score', pct(score, 0)], ['Strategy', score > 70 ? 'maintain corridor + anti-poaching' : 'restore habitat and corridor first']];
  }
  if (kind === 'anatomyTS') return [['Section', state.section || 'dicot stem'], ['Magnification', `${state.magnification || 100}x`], ['Diagnostic feature', TS_FEATURES[state.section] || TS_FEATURES['dicot stem']], ['Result', 'label epidermis/cortex/vascular tissue/pith']];
  if (kind === 'osmosis') {
    const rise = n(state.sucrose, 20) * n(state.time, 45) / 1200;
    return [['Sucrose concentration', pct(n(state.sucrose, 20), 0)], ['Time', fixed(n(state.time, 45), 0, ' min')], ['Liquid rise', fixed(rise, 2, ' cm')], ['Result', rise > 1 ? 'endosmosis into hypertonic cup' : 'small osmotic rise']];
  }
  if (kind === 'plasmolysis') {
    const cells = Math.max(1, n(state.cells, 60));
    const frac = clamp(n(state.salt, 3) / 7.5, 0, 0.96);
    return [['Salt concentration', pct(n(state.salt, 3), 1)], ['Cells observed', cells], ['Plasmolysed cells', `${Math.round(cells * frac)} (${pct(frac * 100, 1)})`], ['Result', frac > 0.5 ? 'hypertonic solution' : 'partial/no plasmolysis']];
  }
  if (kind === 'stomata') {
    const surface = state.surface || 'lower';
    const fieldArea = 0.18;
    const density = n(state.stomata, 42) / fieldArea;
    return [['Leaf surface', surface], ['Stomata counted', Math.round(n(state.stomata, 42))], ['Density', fixed(density, 0, ' /mm2')], ['Result', surface === 'lower' ? 'usually higher density' : 'usually lower density']];
  }
  if (['transpiration', 'respiration', 'anaerobic', 'phototropism', 'apicalBud', 'suction'].includes(kind)) return physiologyRows(kind, state);
  if (kind === 'genetics') {
    const dom = n(state.dominant, 90), rec = n(state.recessive, 32), total = Math.max(1, dom + rec);
    const expD = total * 0.75, expR = total * 0.25;
    const chi = ((dom - expD) ** 2 / expD) + ((rec - expR) ** 2 / expR);
    return [['Dominant seeds', Math.round(dom)], ['Recessive seeds', Math.round(rec)], ['Observed ratio', `${fixed(safeDiv(dom, rec, 0), 2)}:1`], ['Chi-square vs 3:1', fixed(chi, 2)]];
  }
  if (kind === 'imbibition') {
    const initial = Math.max(0.1, n(state.initial, 20)), final = Math.max(initial, n(state.final, 32));
    return [['Initial mass', fixed(initial, 1, ' g')], ['Final mass', fixed(final, 1, ' g')], ['Water uptake', pct(((final - initial) / initial) * 100, 1)], ['Result', 'colloids imbibe water and swell']];
  }
  if (kind === 'biofertilizer') {
    const moisture = n(state.moisture, 45), days = n(state.days, 7);
    const moistureScore = clamp(100 - Math.abs(moisture - 45) * 2.4, 0, 100);
    const maturity = clamp(days * 10, 0, 100);
    return [['Moisture', pct(moisture, 0)], ['Incubation', fixed(days, 0, ' days')], ['Viability index', pct((moistureScore * 0.6 + maturity * 0.4), 0)], ['Culture', 'Rhizobium/Azotobacter carrier batch']];
  }
  if (kind === 'animalTissue') return [['Tissue', state.tissue || 'blood smear'], ['Magnification', `${state.magnification || 400}x`], ['Diagnostic feature', TISSUE_FEATURES[state.tissue] || TISSUE_FEATURES['blood smear']]];
  if (kind === 'frogDev') return [['Stage', state.stage || 'blastula'], ['Magnification', `${state.magnification || 100}x`], ['Embryology note', FROG_STAGE[state.stage] || FROG_STAGE.blastula]];
  if (kind === 'starchTest') {
    const positive = ['potato', 'rice water'].includes(state.sample);
    return [['Sample', state.sample || 'potato'], ['Iodine drops', n(state.iodine, 2)], ['Colour', positive ? 'blue-black' : 'yellow-brown'], ['Result', positive ? 'starch present' : 'starch absent/control negative']];
  }
  if (kind === 'proteinTest') {
    const positive = ['egg albumin', 'milk'].includes(state.sample);
    return [['Sample', state.sample || 'egg albumin'], ['Biuret drops', n(state.biuret, 4)], ['Colour', positive ? 'violet' : 'blue'], ['Result', positive ? 'protein present' : 'protein absent/control negative']];
  }
  if (kind === 'amylase') {
    const temp = n(state.temperature, 37), pH = n(state.pH, 7);
    const tempEffect = Math.exp(-((temp - 37) ** 2) / (2 * 14 ** 2));
    const phEffect = Math.exp(-((pH - 7) ** 2) / (2 * 1.45 ** 2));
    const activity = clamp(tempEffect * phEffect * 100, 0, 100);
    return [['Temperature', fixed(temp, 0, ' C')], ['pH', fixed(pH, 1)], ['Relative activity', pct(activity, 0)], ['Result', activity > 65 ? 'near optimum amylase activity' : 'enzyme activity reduced']];
  }
  if (kind === 'urine') return [['Test', state.test || 'sugar'], ['Intensity', pct(n(state.intensity, 55), 0)], ['Observation', urineObservation(state.test || 'sugar', state.intensity)], ['Result', n(state.intensity, 55) > 20 ? 'positive qualitative test' : 'negative/trace']];
  if (kind === 'bloodSugar') {
    const glucose = n(state.glucose, 96);
    return [['Read time', fixed(n(state.time, 30), 0, ' s')], ['Glucose', fixed(glucose, 0, ' mg/dL')], ['Range', bloodGlucoseBand(glucose)], ['Result', glucose < 70 || glucose >= 200 ? 'clinical follow-up needed' : 'simulated reading in expected range']];
  }
  if (kind === 'skeleton') return [['Joint', state.joint || 'knee hinge'], ['Movement angle', fixed(n(state.angle, 110), 0, ' deg')], ['Joint type', jointType(state.joint || 'knee hinge')], ['Result', 'movement matches joint structure']];
  if (kind === 'skeletonHealth') return [['Joint', state.joint || 'knee'], ['Mobility', pct(n(state.mobility, 72), 0)], ['Joint context', jointType(state.joint || 'knee')], ['Result', n(state.mobility, 72) < 50 ? 'restricted movement' : 'functional range']];
  if (kind === 'cockroach') return [['View', state.view || 'dorsal'], ['Focus part', state.zoomPart || 'thorax'], ['Diagnostic feature', 'head, thorax, abdomen; three pairs of legs'], ['Result', 'insect external morphology verified']];
  return [['Trial', recordCount + 1], ['Observation', config.record || 'biology observation'], ['Result', 'record with reason']];
}

export function getBiologyFormula(config = {}, state = {}) {
  const kind = config.kind || 'unknown';
  const formulas = {
    microscope: 'clarity = 100 - |focus - optimum| x 2.2',
    mitosis: 'mitotic index = dividing cells / total cells x 100',
    animalMitosis: 'mitotic index = dividing cells / total cells x 100',
    herbarium: 'preservation score = 0.55 x dryness + 0.45 x label completeness',
    mushroom: 'diagnosis compares spore print + volva; edibility is not inferred',
    inflorescence: 'identify by main axis, pedicel length and flower arrangement',
    culture: 'CFU estimate = colonies x dilution factor',
    quadrat: 'density = individuals / quadrat area',
    quadrat2: 'frequency = occupied quadrats / total quadrats x 100',
    soil: 'moisture = (wet mass - dry mass) / dry mass x 100',
    pond: 'water quality checked against pH 6.5-8.5',
    pondZoo: 'DO + pH used for pond-fauna suitability',
    specimens: 'classification = diagnostic characters matched to specimen group',
    microscopeParts: 'total magnification = ocular lens x objective lens',
    fossil: 'relative evidence = preserved chambers + morphology score',
    animals: 'classification = body plan + diagnostic external characters',
    dissection: 'trace alimentary canal from mouth to anus',
    conservation: 'connectivity score = 0.65 x habitat + 0.35 x corridor',
    anatomyTS: 'section identity comes from vascular-bundle/root-stem characters',
    osmosis: 'rise ~ sucrose concentration x time / 1200',
    plasmolysis: 'plasmolysis % rises with external solute concentration',
    stomata: 'density = stomata counted / microscope field area',
    transpiration: 'relative rate = 60 / colour-change time',
    respiration: 'respiration index = manometer movement / sample mass',
    anaerobic: 'CO2 output ~ yeast activity x time',
    phototropism: 'curvature ~ light intensity x exposure time',
    apicalBud: 'lateral growth ~ days x reduced auxin dominance',
    suction: 'water movement ~ leaf area x transpiration time',
    genetics: 'compare observed dominant:recessive ratio with 3:1',
    imbibition: 'uptake = (final mass - initial mass) / initial mass x 100',
    biofertilizer: 'viability balances moisture near 45% and incubation time',
    animalTissue: 'tissue identity from cell shape and matrix under magnification',
    frogDev: 'embryo stage identified by cleavage/blastula/gastrula structures',
    amylase: 'activity peaks near 37 C and pH 7',
    bloodSugar: 'strip value classified by mg/dL ranges',
    skeleton: 'joint movement is constrained by joint type',
    skeletonHealth: 'mobility % indicates functional restriction',
    cockroach: 'insect plan = head + thorax + abdomen + three leg pairs',
  };
  if (kind === 'flower') return FLOWER_FORMULAE[state.family] || FLOWER_FORMULAE.Solanaceae;
  if (kind === 'starchTest') return 'iodine + starch -> blue-black complex';
  if (kind === 'proteinTest') return 'Biuret reagent + peptide bonds -> violet complex';
  if (kind === 'urine') return 'qualitative colour/ring reaction interpreted by intensity';
  return formulas[kind] || 'observation + labelled structure + reasoned conclusion';
}

export function getBiologyBadge(config = {}, state = {}) {
  const rows = getBiologyMetricRows(config, state, 0);
  const terminal = rows.find(([label]) => /result|range|index|density|score|activity|rate|formula/i.test(label)) || rows[rows.length - 1];
  return terminal ? `${terminal[0]}: ${terminal[1]}` : (config.record || 'Biology lab');
}

export function getBiologyConclusion(config = {}, state = {}) {
  const rows = getBiologyMetricRows(config, state, 0);
  const result = rows.find(([label]) => String(label).toLowerCase() === 'result');
  const formula = getBiologyFormula(config, state);
  return result ? `${result[1]}. ${formula}.` : formula;
}
