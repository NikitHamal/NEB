import { THREE } from '../../core/engine.js';

export const AU = 1.495978707e11;
export const LY = 9.4607304725808e15;
export const KM = 1e3;
export const R_EARTH = 6.371e6;
export const R_SUN = 6.957e8;
export const R_MOON = 1.7374e6;
export const D2R = Math.PI / 180;
const OBLIQUITY = 23.4393 * D2R;

export const EVEREST = { lat: 27.98806, lon: 86.92528, height: 8849 };

export function rng(seed) {
  let s = seed >>> 0 || 1;
  return () => {
    s = (s + 0x6D2B79F5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function gauss(r) {
  const u = Math.max(1e-9, r());
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * r());
}

export function smooth(a, b, x) {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
}

export function eclToGlobal(x, y, z, out = new THREE.Vector3()) {
  return out.set(x, z, -y);
}

export function eqToGlobal(x, y, z, out = new THREE.Vector3()) {
  const c = Math.cos(OBLIQUITY);
  const s = Math.sin(OBLIQUITY);
  return eclToGlobal(x, y * c + z * s, -y * s + z * c, out);
}

const GAL = [
  [-0.0548755604, 0.4941094279, -0.8676661490],
  [-0.8734370902, -0.4448296300, -0.1980763734],
  [-0.4838350155, 0.7469822445, 0.4559837762],
];

export function galToGlobal(x, y, z, out = new THREE.Vector3()) {
  return eqToGlobal(
    GAL[0][0] * x + GAL[1][0] * y + GAL[2][0] * z,
    GAL[0][1] * x + GAL[1][1] * y + GAL[2][1] * z,
    GAL[0][2] * x + GAL[1][2] * y + GAL[2][2] * z,
    out,
  );
}

export function radec(raH, decD, dist, out = new THREE.Vector3()) {
  const a = raH * 15 * D2R;
  const d = decD * D2R;
  return eqToGlobal(Math.cos(d) * Math.cos(a) * dist, Math.cos(d) * Math.sin(a) * dist, Math.sin(d) * dist, out);
}

export function galLB(lDeg, bDeg, dist, out = new THREE.Vector3()) {
  const l = lDeg * D2R;
  const b = bDeg * D2R;
  return galToGlobal(Math.cos(b) * Math.cos(l) * dist, Math.cos(b) * Math.sin(l) * dist, Math.sin(b) * dist, out);
}

export function basisQuaternion(xAxis, yAxis, zAxis) {
  const m = new THREE.Matrix4().makeBasis(xAxis, yAxis, zAxis);
  return new THREE.Quaternion().setFromRotationMatrix(m);
}

export const GAL_QUAT = basisQuaternion(galToGlobal(1, 0, 0), galToGlobal(0, 0, 1), galToGlobal(0, -1, 0));

export function daysSinceJ2000(date = new Date()) {
  return (date.getTime() - Date.UTC(2000, 0, 1, 12)) / 86400000;
}

export const PLANETS = [
  { id: 'mercury', name: 'Mercury', el: [0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593], rate: 149472.67411175, r: 2.4397e6, color: 0x9b958f },
  { id: 'venus', name: 'Venus', el: [0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255], rate: 58517.81538729, r: 6.0518e6, color: 0xe8cf9a },
  { id: 'earth', name: 'Earth', el: [1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0], rate: 35999.37244981, r: R_EARTH, color: 0x5d8fd6 },
  { id: 'mars', name: 'Mars', el: [1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891], rate: 19140.30268499, r: 3.3895e6, color: 0xc1643a },
  { id: 'jupiter', name: 'Jupiter', el: [5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909], rate: 3034.74612775, r: 6.9911e7, color: 0xd8b48a },
  { id: 'saturn', name: 'Saturn', el: [9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448], rate: 1222.49362201, r: 5.8232e7, color: 0xe3cf9c },
  { id: 'uranus', name: 'Uranus', el: [19.18916464, 0.04725744, 0.77263783, 313.23810451, 170.95427630, 74.01692503], rate: 428.48202785, r: 2.5362e7, color: 0x9fd8e0 },
  { id: 'neptune', name: 'Neptune', el: [30.06992276, 0.00859048, 1.77004347, -55.12002969, 44.96476227, 131.78422574], rate: 218.45945325, r: 2.4622e7, color: 0x4f74d9 },
  { id: 'pluto', name: 'Pluto', el: [39.48211675, 0.24882730, 17.14001206, 238.92903833, 224.06891629, 110.30393684], rate: 145.20780515, r: 1.1883e6, color: 0xcdb8a0 },
];

function solveKepler(M, e) {
  let E = M + e * Math.sin(M);
  for (let i = 0; i < 8; i++) E -= (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
  return E;
}

export function orbitPoint(p, meanAnomalyDeg, out = new THREE.Vector3()) {
  const [a, e, I, , w, O] = p.el;
  const om = (w - O) * D2R;
  const E = solveKepler(meanAnomalyDeg * D2R, e);
  const xp = a * (Math.cos(E) - e);
  const yp = a * Math.sqrt(1 - e * e) * Math.sin(E);
  const co = Math.cos(om), so = Math.sin(om), cO = Math.cos(O * D2R), sO = Math.sin(O * D2R), cI = Math.cos(I * D2R), sI = Math.sin(I * D2R);
  const x = (co * cO - so * sO * cI) * xp + (-so * cO - co * sO * cI) * yp;
  const y = (co * sO + so * cO * cI) * xp + (-so * sO + co * cO * cI) * yp;
  const z = (so * sI) * xp + (co * sI) * yp;
  return eclToGlobal(x * AU, y * AU, z * AU, out);
}

export function planetPosition(p, days, out) {
  const L = p.el[3] + p.rate * (days / 36525);
  const M = ((L - p.el[4]) % 360 + 360) % 360;
  return orbitPoint(p, M, out);
}

export function moonOffset(days, out = new THREE.Vector3()) {
  const L = (218.316 + 13.176396 * days) * D2R;
  const M = (134.963 + 13.064993 * days) * D2R;
  const F = (93.272 + 13.229350 * days) * D2R;
  const lon = L + 6.289 * D2R * Math.sin(M);
  const lat = 5.128 * D2R * Math.sin(F);
  const dist = (385001 - 20905 * Math.cos(M)) * KM;
  return eclToGlobal(Math.cos(lat) * Math.cos(lon) * dist, Math.cos(lat) * Math.sin(lon) * dist, Math.sin(lat) * dist, out);
}

const SPEC = { O: 0x9bb0ff, B: 0xaabfff, A: 0xcad7ff, F: 0xf8f7ff, G: 0xfff1df, K: 0xffd2a1, M: 0xffb56c, W: 0xe8eeff };

export function spectralColor(cls) { return SPEC[cls[0]] || 0xffffff; }

export const NEAR_STARS = [
  ['Proxima Centauri', 14.4953, -62.679, 4.24, 'M', 0.15],
  ['Alpha Centauri A & B', 14.66, -60.835, 4.37, 'G', 1.2],
  ["Barnard's Star", 17.9633, 4.6933, 5.96, 'M', 0.2],
  ['Wolf 359', 10.9414, 7.0147, 7.86, 'M', 0.16],
  ['Lalande 21185', 11.0556, 35.97, 8.31, 'M', 0.39],
  ['Sirius A & B', 6.7525, -16.7161, 8.6, 'A', 1.71],
  ['Luyten 726-8', 1.6503, -17.9503, 8.79, 'M', 0.14],
  ['Ross 154', 18.8303, -23.8361, 9.7, 'M', 0.24],
  ['Ross 248', 23.6986, 44.175, 10.3, 'M', 0.16],
  ['Epsilon Eridani', 3.5489, -9.4583, 10.5, 'K', 0.74],
  ['Lacaille 9352', 23.0978, -35.8531, 10.7, 'M', 0.47],
  ['Ross 128', 11.7956, 0.8044, 11.0, 'M', 0.2],
  ['EZ Aquarii', 22.6425, -15.3019, 11.1, 'M', 0.14],
  ['Procyon A & B', 7.655, 5.225, 11.46, 'F', 2.05],
  ['61 Cygni A & B', 21.115, 38.7494, 11.4, 'K', 0.67],
  ['Struve 2398', 18.7131, 59.6303, 11.5, 'M', 0.33],
  ['Groombridge 34', 0.3064, 44.0231, 11.6, 'M', 0.38],
  ['Epsilon Indi', 22.0561, -56.7861, 11.9, 'K', 0.73],
  ['DX Cancri', 8.4969, 26.7769, 11.8, 'M', 0.11],
  ['Tau Ceti', 1.7344, -15.9375, 11.9, 'G', 0.79],
  ['GJ 1061', 3.6, -44.5125, 12.0, 'M', 0.16],
  ['YZ Ceti', 1.2086, -16.9989, 12.1, 'M', 0.17],
  ["Luyten's Star", 7.4567, 5.2258, 12.2, 'M', 0.29],
  ["Teegarden's Star", 2.8836, 16.8814, 12.5, 'M', 0.11],
  ["Kapteyn's Star", 5.1947, -45.0183, 12.8, 'M', 0.29],
  ['Lacaille 8760', 21.2875, -38.8675, 12.9, 'M', 0.51],
  ['Kruger 60', 22.4664, 57.6958, 13.1, 'M', 0.35],
  ['Altair', 19.8464, 8.8683, 16.7, 'A', 1.8],
  ['Vega', 18.6156, 38.7836, 25.0, 'A', 2.4],
  ['Fomalhaut', 22.9608, -29.6222, 25.1, 'A', 1.84],
  ['Pollux', 7.7553, 28.0261, 33.8, 'K', 8.8],
  ['Arcturus', 14.2611, 19.1825, 36.7, 'K', 25.4],
  ['Capella', 5.2781, 45.9981, 42.9, 'G', 12],
  ['Aldebaran', 4.5986, 16.5092, 65, 'K', 44],
  ['Regulus', 10.1395, 11.9672, 79, 'B', 4.2],
  ['Spica', 13.4199, -11.1614, 250, 'B', 7.5],
  ['Canopus', 6.3992, -52.6956, 310, 'F', 71],
  ['Polaris', 2.5303, 89.2641, 433, 'F', 37.5],
  ['Pleiades', 3.7914, 24.105, 444, 'B', 8],
  ['Betelgeuse', 5.9195, 7.4071, 548, 'M', 764],
  ['Antares', 16.49, -26.4319, 550, 'M', 680],
  ['Rigel', 5.2423, -8.2017, 860, 'B', 79],
  ['Orion Nebula', 5.5881, -5.3911, 1344, 'O', 10],
  ['Deneb', 20.6905, 45.2803, 2600, 'A', 203],
];

export const GALACTIC_R0 = 26670 * LY;

export const LOCAL_GROUP = [
  { id: 'm31', name: 'Andromeda Galaxy', l: 121.17, b: -21.57, d: 2.54e6, size: 152000, kind: 'spiral', tilt: [77.5, 38] },
  { id: 'm33', name: 'Triangulum Galaxy', l: 133.61, b: -31.33, d: 2.73e6, size: 61000, kind: 'spiral', tilt: [55, 23] },
  { id: 'lmc', name: 'Large Magellanic Cloud', l: 280.47, b: -32.89, d: 1.63e5, size: 32000, kind: 'irregular' },
  { id: 'smc', name: 'Small Magellanic Cloud', l: 302.8, b: -44.3, d: 2.0e5, size: 18900, kind: 'irregular' },
  { id: 'm32', name: 'M32', l: 121.15, b: -21.98, d: 2.49e6, size: 6500, kind: 'elliptical' },
  { id: 'm110', name: 'M110', l: 120.72, b: -21.14, d: 2.69e6, size: 17000, kind: 'elliptical' },
  { id: 'ic10', name: 'IC 10', l: 118.97, b: -3.34, d: 2.2e6, size: 5000, kind: 'irregular' },
  { id: 'ngc6822', name: "Barnard's Galaxy", l: 25.34, b: -18.4, d: 1.63e6, size: 7000, kind: 'irregular' },
  { id: 'sag', name: 'Sagittarius Dwarf', l: 5.6, b: -14.2, d: 7.0e4, size: 10000, kind: 'irregular' },
];

export const CLUSTERS = [
  { name: 'Virgo Cluster', l: 283.8, b: 74.5, d: 5.4e7, n: 1500, r: 7.5e6 },
  { name: 'Fornax Cluster', l: 236.7, b: -53.6, d: 6.2e7, n: 200, r: 3e6 },
  { name: 'Centaurus Cluster', l: 302.4, b: 21.6, d: 1.7e8, n: 600, r: 6e6 },
  { name: 'Norma Cluster (Great Attractor)', l: 325.3, b: -7.3, d: 2.2e8, n: 900, r: 8e6 },
  { name: 'Hydra Cluster', l: 269.6, b: 26.5, d: 1.6e8, n: 400, r: 5e6 },
  { name: 'Coma Cluster', l: 58.1, b: 88.0, d: 3.2e8, n: 1000, r: 1e7 },
  { name: 'Perseus Cluster', l: 150.6, b: -13.3, d: 2.4e8, n: 700, r: 8e6 },
];
