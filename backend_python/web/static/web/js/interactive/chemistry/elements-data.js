// Compact periodic-table dataset for all 118 elements + electron-configuration engine.
// Each row: [Z, symbol, name, mass, category, cpkHex, covalentRadius, valenceE, electroneg, group, period]
//   category: alkali | alkaline | transition | post-transition | metalloid | nonmetal | halogen | noble | lanthanide | actinide
//   covalentRadius in Angstrom (used as visual scale); electronegativity = Pauling (0 if none)
// Hand-authored from standard reference values (IUPAC atomic weights, CPK colours, Pauling EN).

export const ELEMENTS = [
  [1,'H','Hydrogen',1.008,'nonmetal',0xffffff,0.31,1,2.20,1,1],
  [2,'He','Helium',4.0026,'noble',0xd9ffff,0.28,2,0,18,1],
  [3,'Li','Lithium',6.94,'alkali',0xcc80ff,1.28,1,0.98,1,2],
  [4,'Be','Beryllium',9.0122,'alkaline',0xc2ff00,0.96,2,1.57,2,2],
  [5,'B','Boron',10.81,'metalloid',0xffb5b5,0.84,3,2.04,13,2],
  [6,'C','Carbon',12.011,'nonmetal',0x909090,0.76,4,2.55,14,2],
  [7,'N','Nitrogen',14.007,'nonmetal',0x3050f8,0.71,5,3.04,15,2],
  [8,'O','Oxygen',15.999,'nonmetal',0xff0d0d,0.66,6,3.44,16,2],
  [9,'F','Fluorine',18.998,'halogen',0x90e050,0.57,7,3.98,17,2],
  [10,'Ne','Neon',20.180,'noble',0xb3e3f5,0.58,8,0,18,2],
  [11,'Na','Sodium',22.990,'alkali',0xab5cf2,1.66,1,0.93,1,3],
  [12,'Mg','Magnesium',24.305,'alkaline',0x8aff00,1.41,2,1.31,2,3],
  [13,'Al','Aluminium',26.982,'post-transition',0xbfa6a6,1.21,3,1.61,13,3],
  [14,'Si','Silicon',28.085,'metalloid',0xf0c8a0,1.11,4,1.90,14,3],
  [15,'P','Phosphorus',30.974,'nonmetal',0xff8000,1.07,5,2.19,15,3],
  [16,'S','Sulphur',32.06,'nonmetal',0xffff30,1.05,6,2.58,16,3],
  [17,'Cl','Chlorine',35.45,'halogen',0x1ff01f,1.02,7,3.16,17,3],
  [18,'Ar','Argon',39.948,'noble',0x80d1e3,1.06,8,0,18,3],
  [19,'K','Potassium',39.098,'alkali',0x8f40d4,2.03,1,0.82,1,4],
  [20,'Ca','Calcium',40.078,'alkaline',0x3dff00,1.76,2,1.00,2,4],
  [21,'Sc','Scandium',44.956,'transition',0xe6e6e6,1.70,3,1.36,3,4],
  [22,'Ti','Titanium',47.867,'transition',0xbfc2c7,1.60,4,1.54,4,4],
  [23,'V','Vanadium',50.942,'transition',0xa6a6ab,1.53,5,1.63,5,4],
  [24,'Cr','Chromium',51.996,'transition',0x8a99c7,1.39,6,1.66,6,4],
  [25,'Mn','Manganese',54.938,'transition',0x9c7ac7,1.39,7,1.55,7,4],
  [26,'Fe','Iron',55.845,'transition',0xe06633,1.32,8,1.83,8,4],
  [27,'Co','Cobalt',58.933,'transition',0xf090a0,1.26,9,1.88,9,4],
  [28,'Ni','Nickel',58.693,'transition',0x50d050,1.24,10,1.91,10,4],
  [29,'Cu','Copper',63.546,'transition',0xc88033,1.32,11,1.90,11,4],
  [30,'Zn','Zinc',65.38,'transition',0x7d80b0,1.22,12,1.65,12,4],
  [31,'Ga','Gallium',69.723,'post-transition',0xc28f8f,1.22,3,1.81,13,4],
  [32,'Ge','Germanium',72.630,'metalloid',0x668f8f,1.20,4,2.01,14,4],
  [33,'As','Arsenic',74.922,'metalloid',0xbd80e3,1.19,5,2.18,15,4],
  [34,'Se','Selenium',78.971,'nonmetal',0xffa100,1.20,6,2.55,16,4],
  [35,'Br','Bromine',79.904,'halogen',0xa62929,1.20,7,2.96,17,4],
  [36,'Kr','Krypton',83.798,'noble',0x5cb8d1,1.16,8,3.00,18,4],
  [37,'Rb','Rubidium',85.468,'alkali',0x702eb0,2.11,1,0.82,1,5],
  [38,'Sr','Strontium',87.62,'alkaline',0x00ff00,1.95,2,0.95,2,5],
  [39,'Y','Yttrium',88.906,'transition',0x94ffff,1.90,3,1.22,3,5],
  [40,'Zr','Zirconium',91.224,'transition',0x94e0e0,1.75,4,1.33,4,5],
  [41,'Nb','Niobium',92.906,'transition',0x73c2c9,1.64,5,1.6,5,5],
  [42,'Mo','Molybdenum',95.95,'transition',0x54b5b5,1.54,6,2.16,6,5],
  [43,'Tc','Technetium',98,'transition',0x3b9e9e,1.47,7,1.9,7,5],
  [44,'Ru','Ruthenium',101.07,'transition',0x248f8f,1.46,8,2.2,8,5],
  [45,'Rh','Rhodium',102.91,'transition',0x0a7d8c,1.42,9,2.28,9,5],
  [46,'Pd','Palladium',106.42,'transition',0x006985,1.39,10,2.20,10,5],
  [47,'Ag','Silver',107.87,'transition',0xc0c0c0,1.45,11,1.93,11,5],
  [48,'Cd','Cadmium',112.41,'transition',0xffd98f,1.44,12,1.69,12,5],
  [49,'In','Indium',114.82,'post-transition',0xa67573,1.42,3,1.78,13,5],
  [50,'Sn','Tin',118.71,'post-transition',0x668080,1.39,4,1.96,14,5],
  [51,'Sb','Antimony',121.76,'metalloid',0x9e63b5,1.39,5,2.05,15,5],
  [52,'Te','Tellurium',127.60,'metalloid',0xd47a00,1.38,6,2.1,16,5],
  [53,'I','Iodine',126.90,'halogen',0x940094,1.39,7,2.66,17,5],
  [54,'Xe','Xenon',131.29,'noble',0x429eb0,1.40,8,2.6,18,5],
  [55,'Cs','Caesium',132.91,'alkali',0x57178f,2.32,1,0.79,1,6],
  [56,'Ba','Barium',137.33,'alkaline',0x00c900,1.98,2,0.89,2,6],
  [57,'La','Lanthanum',138.91,'lanthanide',0x70d4ff,1.95,3,1.10,3,6],
  [58,'Ce','Cerium',140.12,'lanthanide',0xffffc7,1.85,4,1.12,3,6],
  [59,'Pr','Praseodymium',140.91,'lanthanide',0xd9ffc7,1.82,3,1.13,3,6],
  [60,'Nd','Neodymium',144.24,'lanthanide',0xc7ffc7,1.81,3,1.14,3,6],
  [61,'Pm','Promethium',145,'lanthanide',0xa3ffc7,1.83,3,1.13,3,6],
  [62,'Sm','Samarium',150.36,'lanthanide',0x8fffc7,1.80,3,1.17,3,6],
  [63,'Eu','Europium',151.96,'lanthanide',0x61ffc7,1.99,3,1.2,3,6],
  [64,'Gd','Gadolinium',157.25,'lanthanide',0x45ffc7,1.79,3,1.20,3,6],
  [65,'Tb','Terbium',158.93,'lanthanide',0x30ffc7,1.76,3,1.2,3,6],
  [66,'Dy','Dysprosium',162.50,'lanthanide',0x1fffc7,1.75,3,1.22,3,6],
  [67,'Ho','Holmium',164.93,'lanthanide',0x00ff9c,1.74,3,1.23,3,6],
  [68,'Er','Erbium',167.26,'lanthanide',0x00e675,1.73,3,1.24,3,6],
  [69,'Tm','Thulium',168.93,'lanthanide',0x00d452,1.71,3,1.25,3,6],
  [70,'Yb','Ytterbium',173.05,'lanthanide',0x00bf38,1.70,3,1.1,3,6],
  [71,'Lu','Lutetium',174.97,'lanthanide',0x00ab24,1.71,3,1.27,3,6],
  [72,'Hf','Hafnium',178.49,'transition',0x4dc2ff,1.52,4,1.3,4,6],
  [73,'Ta','Tantalum',180.95,'transition',0x4da6ff,1.46,5,1.5,5,6],
  [74,'W','Tungsten',183.84,'transition',0x2194d6,1.37,6,2.36,6,6],
  [75,'Re','Rhenium',186.21,'transition',0x267dab,1.37,7,1.9,7,6],
  [76,'Os','Osmium',190.23,'transition',0x266696,1.32,8,2.2,8,6],
  [77,'Ir','Iridium',192.22,'transition',0x175487,1.39,9,2.20,9,6],
  [78,'Pt','Platinum',195.08,'transition',0xd0d0e0,1.36,10,2.28,10,6],
  [79,'Au','Gold',196.97,'transition',0xffd123,1.24,11,2.54,11,6],
  [80,'Hg','Mercury',200.59,'transition',0xb8b8d0,1.49,12,2.00,12,6],
  [81,'Tl','Thallium',204.38,'post-transition',0xa6544d,1.48,3,1.62,13,6],
  [82,'Pb','Lead',207.2,'post-transition',0x575961,1.45,4,2.33,14,6],
  [83,'Bi','Bismuth',208.98,'post-transition',0x9e4fb5,1.46,5,2.02,15,6],
  [84,'Po','Polonium',209,'metalloid',0xab5c00,1.40,6,2.0,16,6],
  [85,'At','Astatine',210,'halogen',0x754f45,1.40,7,2.2,17,6],
  [86,'Rn','Radon',222,'noble',0x428296,1.40,8,2.2,18,6],
  [87,'Fr','Francium',223,'alkali',0x420066,2.30,1,0.7,1,7],
  [88,'Ra','Radium',226,'alkaline',0x007d00,2.10,2,0.9,2,7],
  [89,'Ac','Actinium',227,'actinide',0x70abfa,1.95,3,1.1,3,7],
  [90,'Th','Thorium',232.04,'actinide',0x00baff,1.80,4,1.3,3,7],
  [91,'Pa','Protactinium',231.04,'actinide',0x00a1ff,1.69,5,1.5,3,7],
  [92,'U','Uranium',238.03,'actinide',0x008cff,1.68,6,1.38,3,7],
  [93,'Np','Neptunium',237,'actinide',0x0080ff,1.65,7,1.36,3,7],
  [94,'Pu','Plutonium',244,'actinide',0x006bff,1.73,8,1.28,3,7],
  [95,'Am','Americium',243,'actinide',0x0055cf,1.66,9,1.13,3,7],
  [96,'Cm','Curium',247,'actinide',0x0045a8,1.66,10,1.28,3,7],
  [97,'Bk','Berkelium',247,'actinide',0x003590,1.68,11,1.3,3,7],
  [98,'Cf','Californium',251,'actinide',0x002a80,1.68,12,1.3,3,7],
  [99,'Es','Einsteinium',252,'actinide',0x002070,1.65,13,1.3,3,7],
  [100,'Fm','Fermium',257,'actinide',0x001560,1.67,14,1.3,3,7],
  [101,'Md','Mendelevium',258,'actinide',0x001050,1.67,15,1.3,3,7],
  [102,'No','Nobelium',259,'actinide',0x000a40,1.67,16,1.3,3,7],
  [103,'Lr','Lawrencium',266,'actinide',0x000530,1.67,17,1.3,3,7],
  [104,'Rf','Rutherfordium',267,'transition',0xcc0059,1.60,4,1.3,4,7],
  [105,'Db','Dubnium',268,'transition',0xcc0066,1.60,5,1.3,5,7],
  [106,'Sg','Seaborgium',269,'transition',0xcc0080,1.60,6,1.3,6,7],
  [107,'Bh','Bohrium',270,'transition',0xcc0095,1.60,7,1.3,7,7],
  [108,'Hs','Hassium',269,'transition',0xcc00aa,1.60,8,1.3,8,7],
  [109,'Mt','Meitnerium',278,'transition',0xcc00bf,1.60,9,1.3,9,7],
  [110,'Ds','Darmstadtium',281,'transition',0xcc00d5,1.60,10,1.3,10,7],
  [111,'Rg','Roentgenium',282,'transition',0xcc00e9,1.60,11,1.3,11,7],
  [112,'Cn','Copernicium',285,'transition',0xcc00ff,1.60,12,1.3,12,7],
  [113,'Nh','Nihonium',286,'post-transition',0xcc44ff,1.60,3,1.3,13,7],
  [114,'Fl','Flerovium',289,'post-transition',0xcc66ff,1.60,4,1.3,14,7],
  [115,'Mc','Moscovium',290,'post-transition',0xcc88ff,1.60,5,1.3,15,7],
  [116,'Lv','Livermorium',293,'post-transition',0xccccff,1.60,6,1.3,16,7],
  [117,'Ts','Tennessine',294,'halogen',0xccccff,1.60,7,1.3,17,7],
  [118,'Og','Oganesson',294,'noble',0xe0e0ff,1.60,8,1.3,18,7],
];

export const ELEMENT_MAP = {};
export const SYMBOL_MAP = {};
for (const row of ELEMENTS) {
  const e = {
    z: row[0], symbol: row[1], name: row[2], mass: row[3], category: row[4],
    color: row[5], radius: row[6], valence: row[7], en: row[8], group: row[9], period: row[10],
  };
  ELEMENT_MAP[e.z] = e;
  SYMBOL_MAP[e.symbol] = e;
}

export function getElement(z) { return ELEMENT_MAP[z]; }
export function getBySymbol(sym) { return SYMBOL_MAP[sym]; }

export const CATEGORY_COLORS = {
  'alkali': '#ff6b6b',
  'alkaline': '#ffa94d',
  'transition': '#ffd43b',
  'post-transition': '#69db7c',
  'metalloid': '#38d9a9',
  'nonmetal': '#4dabf7',
  'halogen': '#9775fa',
  'noble': '#f783ac',
  'lanthanide': '#da77f2',
  'actinide': '#e599f7',
};

export const CATEGORY_LABELS = {
  'alkali': 'Alkali metal',
  'alkaline': 'Alkaline earth',
  'transition': 'Transition metal',
  'post-transition': 'Post-transition metal',
  'metalloid': 'Metalloid',
  'nonmetal': 'Nonmetal',
  'halogen': 'Halogen',
  'noble': 'Noble gas',
  'lanthanide': 'Lanthanide',
  'actinide': 'Actinide',
};

const SUBSHELL_CAP = { s: 2, p: 6, d: 10, f: 14 };
const FILLING_ORDER = ['1s','2s','2p','3s','3p','4s','3d','4p','5s','4d','5p','6s','4f','5d','6p','7s','5f','6d','7p'];

// Known Aufbau exceptions (observed ground-state configurations).
// Value is the full explicit subshell occupancy string, e.g. '1s2 2s2 2p6 3s2 3p6 3d5 4s1' for Cr.
const CONFIG_EXCEPTIONS = {
  24: '1s2 2s2 2p6 3s2 3p6 3d5 4s1',   // Cr  (half-filled d)
  29: '1s2 2s2 2p6 3s2 3p6 3d10 4s1',  // Cu  (filled d)
  41: '[Kr] 4d4 5s1',                  // Nb
  42: '[Kr] 4d5 5s1',                  // Mo
  44: '[Kr] 4d7 5s1',                  // Ru
  45: '[Kr] 4d8 5s1',                  // Rh
  46: '[Kr] 4d10',                     // Pd
  47: '[Kr] 4d10 5s1',                 // Ag
  57: '[Xe] 5d1 6s2',                  // La
  58: '[Xe] 4f1 5d1 6s2',             // Ce
  64: '[Xe] 4f7 5d1 6s2',             // Gd
  78: '[Xe] 4f14 5d9 6s1',            // Pt
  79: '[Xe] 4f14 5d10 6s1',           // Au
  89: '[Rn] 6d1 7s2',                  // Ac
  90: '[Rn] 6d2 7s2',                  // Th
  91: '[Rn] 5f2 6d1 7s2',             // Pa
  92: '[Rn] 5f3 6d1 7s2',             // U
  93: '[Rn] 5f4 6d1 7s2',             // Np
  96: '[Rn] 5f7 6d1 7s2',             // Cm
};

const CORE_CONFIGS = {
  '[He]': 2,
  '[Ne]': 10,
  '[Ar]': 18,
  '[Kr]': 36,
  '[Xe]': 54,
  '[Rn]': 86,
};

// Returns an ordered array of subshell objects: [{ sub:'1s', n:1, l:'s', cap:2, count:2 }, ...]
// Only subshells with count > 0 are returned.
export function electronConfiguration(z) {
  const cfg = [];
  if (CONFIG_EXCEPTIONS[z]) {
    return parseConfigString(CONFIG_EXCEPTIONS[z]);
  }
  let remaining = z;
  for (const key of FILLING_ORDER) {
    if (remaining <= 0) break;
    const n = parseInt(key[0], 10);
    const l = key[1];
    const cap = SUBSHELL_CAP[l];
    const take = Math.min(cap, remaining);
    if (take > 0) {
      cfg.push({ sub: key, n, l, cap, count: take });
      remaining -= take;
    }
  }
  return cfg;
}

function parseConfigString(str) {
  const tokens = str.split(/\s+/).filter(Boolean);
  const cfg = [];
  for (const tok of tokens) {
    if (CORE_CONFIGS.hasOwnProperty(tok)) {
      const coreZ = CORE_CONFIGS[tok];
      const coreCfg = electronConfigurationBase(coreZ);
      for (const c of coreCfg) cfg.push(c);
    } else {
      const m = tok.match(/^(\d)([spdf])(\d+)$/);
      if (!m) continue;
      const n = parseInt(m[1], 10);
      const l = m[2];
      cfg.push({ sub: `${n}${l}`, n, l, cap: SUBSHELL_CAP[l], count: parseInt(m[3], 10) });
    }
  }
  return cfg;
}

function electronConfigurationBase(z) {
  const cfg = [];
  let remaining = z;
  for (const key of FILLING_ORDER) {
    if (remaining <= 0) break;
    const n = parseInt(key[0], 10);
    const l = key[1];
    const cap = SUBSHELL_CAP[l];
    const take = Math.min(cap, remaining);
    if (take > 0) {
      cfg.push({ sub: key, n, l, cap, count: take });
      remaining -= take;
    }
  }
  return cfg;
}

export function configToString(cfg) {
  return cfg.map((c) => `${c.sub}${superscript(c.count)}`).join(' ');
}

const SUP_MAP = { 0:'⁰',1:'¹',2:'²',3:'³',4:'⁴',5:'⁵',6:'⁶',7:'⁷',8:'⁸',9:'⁹' };
function superscript(n) {
  return String(n).split('').map((d) => SUP_MAP[d]).join('');
}

// Pack a configuration into principal shells: [{ n, capacity, count }, ...]
// Capacity of shell n = 2n². Electrons from all subshells of that n are summed.
export function shellPacking(cfg) {
  const shells = {};
  for (const c of cfg) {
    if (!shells[c.n]) shells[c.n] = 0;
    shells[c.n] += c.count;
  }
  const ns = Object.keys(shells).map(Number).sort((a, b) => a - b);
  return ns.map((n) => ({ n, capacity: 2 * n * n, count: shells[n] }));
}

// Neutrons for the most common (stable) isotope approximation.
// Uses the rounded atomic mass minus Z, clamped to >= 0.
export function commonNeutrons(z) {
  const e = ELEMENT_MAP[z];
  if (!e) return Math.round(z * 1.1);
  return Math.max(0, Math.round(e.mass) - z);
}

export function isMetal(category) {
  return ['alkali','alkaline','transition','post-transition','lanthanide','actinide'].includes(category);
}
export function isNonmetal(category) {
  return ['nonmetal','halogen','noble'].includes(category);
}
