import { THREE } from '../../core/engine.js';
import { ellipsoid, sphere, capsule, smin, smax, vnoise } from '../anatomy/sdf.js';
import { surfaceNets, toGeometry } from '../anatomy/mesher.js';
import { sweepTube } from '../anatomy/sweep.js';

const cm = (x, y, z) => [x, y, z];

function sdfGeo(sdf, min, max, cell) {
  const mesh = surfaceNets(sdf, { min, max }, cell);
  const n = mesh.count;
  return toGeometry(THREE, mesh, { along: [new Float32Array(n), 1] });
}

function liver() {
  const right = ellipsoid(cm(-6, 113, 2.5), [9.5, 6.8, 7.2], [0.25, 1, 0.05]);
  const left = ellipsoid(cm(4.5, 115.5, 4.5), [6.5, 2.8, 4.6], [0.6, 1, 0.1]);
  return (p) => {
    let d = smin(right(p), left(p), 3.2);
    d = smax(d, -(p[1] - 107.2) - (p[0] + 2) * 0.12 + (p[2] - 2) * 0.1, 1.6);
    d = smax(d, (p[1] - 118.5) + Math.max(0, p[0]) * 0.18, 2.0);
    return d;
  };
}

function kidney(side) {
  const s = side;
  const c = cm(s * 5.6, s > 0 ? 105.6 : 104.4, -4.6);
  const body = ellipsoid(c, [2.9, 5.4, 2.0], [s * 0.28, 1, 0.12]);
  const hil = sphere([c[0] - s * 2.9, c[1], c[2] + 0.6], 1.55);
  return (p) => smax(body(p), -hil(p), 1.0);
}

function brain() {
  const lh = ellipsoid(cm(-3.05, 165.2, -1.2), [6.0, 5.5, 8.6]);
  const rh = ellipsoid(cm(3.05, 165.2, -1.2), [6.0, 5.5, 8.6]);
  const temporal = [ellipsoid(cm(-4.6, 161.6, 0.6), [3.0, 2.6, 4.6]), ellipsoid(cm(4.6, 161.6, 0.6), [3.0, 2.6, 4.6])];
  const cb = ellipsoid(cm(0, 159.4, -6.6), [5.0, 2.7, 3.3]);
  const stem = capsule(cm(0, 161.5, -2.6), cm(0, 154.0, -3.6), 1.25, 1.0);
  return (p) => {
    let cer = smin(lh(p), rh(p), 0.6);
    cer = smin(cer, smin(temporal[0](p), temporal[1](p), 0.5), 1.4);
    cer = smax(cer, -(Math.abs(p[0]) - 0.22), 0.35 * (p[1] > 162 ? 1 : 0.01));
    const w = vnoise(p[0] * 0.55, p[1] * 0.55, p[2] * 0.55) * 3.2;
    const g = Math.abs(Math.sin(p[0] * 1.15 + w) * Math.sin(p[2] * 1.05 + w * 0.8) + 0.25 * Math.sin(p[1] * 1.7 + w));
    cer += 0.32 * Math.pow(1 - Math.min(1, g * 2.2), 3);
    let c2 = cb(p) + 0.12 * Math.pow(Math.abs(Math.sin(p[1] * 5.4 + p[2] * 0.8)), 6);
    let d = smin(cer, c2, 0.4);
    d = smin(d, stem(p), 0.8);
    return d;
  };
}

const PATH = {
  esophagus: [[0, 150, -2.6], [0, 140, -3.6], [0.3, 128, -4.4], [1.2, 120, -3.4], [2.6, 116.5, -1.4]],
  stomach: [[2.6, 116.5, -1.4], [6.4, 116.8, 0.2], [8.8, 113.4, 2.0], [8.6, 108.5, 4.2], [5.8, 105.2, 5.8], [1.6, 104.4, 6.2], [-1.6, 105.6, 5.0]],
  pancreas: [[-2.4, 106.2, 1.2], [1.5, 107.4, 0.0], [5.5, 108.6, -1.4], [9.0, 109.8, -2.8]],
  colon: [[-7.2, 92.4, 3.6], [-8.4, 97, 3.4], [-8.6, 103.6, 2.8], [-7.2, 106.6, 4.4], [-3.5, 104.6, 7.2], [0, 103.4, 7.6], [4.2, 105.2, 7.0], [8.4, 108.4, 3.0], [9.4, 104.6, 1.4], [9.0, 97.5, 1.6], [8.0, 92.0, 2.2], [5.2, 89.4, 3.8], [2.0, 90.6, 2.8], [0.5, 88.2, -1.2], [0.2, 84.6, -4.0]],
  ureterL: [[3.4, 104.2, -3.6], [4.2, 98, -4.4], [4.6, 92, -3.6], [3.2, 88.4, 0.6], [1.6, 87.6, 2.6]],
  ureterR: [[-3.4, 103.0, -3.6], [-4.2, 98, -4.4], [-4.6, 92, -3.6], [-3.2, 88.4, 0.6], [-1.6, 87.6, 2.6]],
};

function smallIntestine() {
  const pts = [[-1.6, 105.6, 5.0], [-3.4, 104.2, 3.8]];
  const rows = 9;
  for (let r = 0; r < rows; r++) {
    const y = 102.4 - r * 1.25;
    const dir = r % 2 ? -1 : 1;
    for (let k = 0; k <= 9; k++) {
      const x = dir * (-6.2 + k * 1.38);
      pts.push([x, y + Math.sin(k * 1.7 + r) * 0.45, 4.0 + 2.2 * Math.sin(k * 0.9 + r * 1.3)]);
    }
  }
  pts.push([-5.2, 92.0, 4.2], [-7.0, 92.6, 3.6]);
  return pts;
}

export const ORGAN_INFO = {
  brain: ['Brain', 'About 1.4 kg and 86 billion neurons. The wrinkled cerebrum thinks, remembers and feels; the cerebellum at the back keeps your balance; the brainstem runs breathing and heartbeat automatically.'],
  liver: ['Liver', 'The largest internal organ, about 1.5 kg. It cleans the blood, stores glucose as glycogen, makes bile to digest fat and does over 500 jobs. It can regrow from a quarter of its size.'],
  gallbladder: ['Gallbladder', 'A small green pouch under the liver that stores bile and squeezes it into the intestine after a fatty meal.'],
  stomach: ['Stomach', 'A J-shaped muscular bag that churns food with hydrochloric acid and the enzyme pepsin. Empty it holds about 50 mL; after a big meal it stretches to over a litre.'],
  esophagus: ['Oesophagus', 'A 25 cm muscular tube that pushes food from the throat to the stomach by waves of squeezing called peristalsis. It works even if you stand on your head.'],
  pancreas: ['Pancreas', 'Makes digestive enzymes for the small intestine, and the hormones insulin and glucagon that keep your blood sugar steady.'],
  spleen: ['Spleen', 'Filters old red blood cells out of the blood and stores white blood cells that fight infection.'],
  small: ['Small intestine', 'About 6 metres long, folded into your belly. Its lining is covered in millions of finger-like villi that absorb the nutrients from digested food.'],
  colon: ['Large intestine', 'About 1.5 m long. It frames the small intestine, absorbs water and salts, and its friendly bacteria make vitamins K and B.'],
  kidney: ['Kidneys', 'Two bean-shaped filters that clean about 180 litres of blood plasma a day and turn the waste into 1–2 litres of urine.'],
  ureter: ['Ureters', 'Thin muscular tubes, about 25 cm long, that carry urine from the kidneys down to the bladder.'],
  bladder: ['Urinary bladder', 'A stretchy muscular bag that stores urine; it signals the brain when it holds about 300 mL.'],
  adrenal: ['Adrenal glands', 'Small glands on top of each kidney that make adrenaline for “fight or flight”, and cortisol.'],
  cord: ['Spinal cord', 'A cable of nerves about 45 cm long inside the vertebral canal, carrying messages between the brain and the body. Reflexes are handled right here.'],
  nerves: ['Nerves', 'Bundles of nerve fibres. The sciatic nerve down the back of each leg is the longest and thickest in the body, about as wide as your thumb.'],
  arteries: ['Arteries', 'Thick, elastic vessels that carry blood away from the heart under pressure. You can feel their pulse at the wrist and neck.'],
  veins: ['Veins', 'Thinner vessels that return blood to the heart. Valves inside them stop the blood flowing backwards, helped by squeezing muscles.'],
};

export function buildOrgans(quality, landmarks) {
  const low = quality.tier === 'low';
  const c = low ? 0.42 : 0.3;
  const out = {};
  out.liver = sdfGeo(liver(), [-17, 104, -6], [12, 122, 12], c);
  out.gallbladder = sdfGeo(ellipsoid(cm(-5.6, 106.8, 7.6), [1.3, 3.0, 1.4], [0.15, -1, 0.5]), [-8, 102, 5], [-3, 111, 10.5], c * 0.7);
  out.spleen = sdfGeo(ellipsoid(cm(10.4, 112.5, -4.2), [2.2, 5.6, 3.4], [0.5, 1, -0.35]), [6, 105, -9], [15, 120, 1], c);
  const kl = kidney(1); const kr = kidney(-1);
  out.kidney = sdfGeo((p) => Math.min(kl(p), kr(p)), [-10, 97, -8.5], [10, 112, -0.5], c * 0.8);
  out.adrenal = sdfGeo((p) => Math.min(ellipsoid(cm(4.4, 111.4, -3.8), [1.8, 1.0, 0.7])(p), ellipsoid(cm(-4.4, 110.2, -3.8), [1.8, 1.0, 0.7])(p)), [-7, 108, -6], [7, 113.5, -1.5], c * 0.6);
  out.bladder = sdfGeo(ellipsoid(cm(0, 87.4, 3.6), [3.9, 3.3, 3.4]), [-5, 83, -0.5], [5, 92, 8], c * 0.8);
  out.brain = sdfGeo(brain(), [-7.6, 151, -11.5], [7.6, 172, 9], low ? 0.32 : 0.2);
  out.esophagus = sweepTube(PATH.esophagus, (t) => 0.9 + 0.2 * Math.sin(t * 40), { segments: 80, radial: 12 });
  out.stomach = sweepTube(PATH.stomach, (t) => (t < 0.2 ? 0.9 + t * 17 : t < 0.55 ? 4.3 - (t - 0.2) * 2 : 3.6 - (t - 0.55) * 5.2) * (1 + 0.015 * Math.sin(t * 90)), { segments: 140, radial: 28, recompute: true });
  out.pancreas = sweepTube(PATH.pancreas, (t) => 1.9 - t * 1.0 + 0.12 * Math.sin(t * 60), { segments: 60, radial: 16 });
  out.colon = sweepTube(PATH.colon, (t) => (t < 0.08 ? 2.6 : t > 0.9 ? 1.7 : 2.2) * (1 + 0.1 * Math.pow(Math.abs(Math.sin(t * 150)), 0.6) - 0.06), { segments: 420, radial: 18, recompute: true });
  out.small = sweepTube(smallIntestine(), 1.15, { segments: 900, radial: 12 });
  out.ureter = sweepTube(PATH.ureterL, 0.32, { segments: 60, radial: 8 });
  out.ureter2 = sweepTube(PATH.ureterR, 0.32, { segments: 60, radial: 8 });
  if (landmarks.canal && landmarks.canal.length > 2) out.cord = sweepTube(landmarks.canal, (t) => 0.55 - t * 0.12, { segments: 120, radial: 12 });
  return out;
}

export const VESSELS = {
  arteries: [
    [[1.2, 133, -1.8], [1.8, 125, -4.6], [1.4, 112, -5.0], [0.8, 101, -4.4], [0.4, 97.5, -3.6]],
    [[0.4, 97.5, -3.6], [4.4, 93.5, -2.8], [7.4, 88.5, 0.8], [8.6, 80, 1.6], [8.8, 66, -0.6], [8.2, 50, -3.4], [8.2, 40, -3.6], [8.4, 24, -2.6], [8.4, 9, -2.0], [8.6, 4, 2.4], [8.6, 3.6, 9.0]],
    [[0.4, 97.5, -3.6], [-4.4, 93.5, -2.8], [-7.4, 88.5, 0.8], [-8.6, 80, 1.6], [-8.8, 66, -0.6], [-8.2, 50, -3.4], [-8.2, 40, -3.6], [-8.4, 24, -2.6], [-8.4, 9, -2.0], [-8.6, 4, 2.4], [-8.6, 3.6, 9.0]],
    [[1.6, 134, -0.6], [2.4, 141, 0.4], [2.6, 150, 0.8], [3.0, 157, 1.6]],
    [[-1.0, 135, 0.2], [-2.4, 141, 0.4], [-2.6, 150, 0.8], [-3.0, 157, 1.6]],
    [[2.4, 134, -1.4], [7, 140, -1.0], [13, 138, -1.4], [16.8, 132, -1.8], [19.6, 118, -1.8], [21.6, 109, -0.4], [24.4, 98, 0.6], [26.8, 88, 1.0], [27.8, 82, 1.6]],
    [[-1.2, 136, -0.4], [-7, 140, -1.0], [-13, 138, -1.4], [-16.8, 132, -1.8], [-19.6, 118, -1.8], [-21.6, 109, -0.4], [-24.4, 98, 0.6], [-26.8, 88, 1.0], [-27.8, 82, 1.6]],
  ],
  veins: [
    [[-2.6, 132, -0.8], [-2.0, 125, -3.4], [-1.6, 112, -3.6], [-1.6, 101, -3.0], [-0.6, 96.5, -2.6]],
    [[-0.6, 96.5, -2.6], [3.6, 92.5, -1.6], [6.4, 88.2, 1.6], [7.6, 80, 2.4], [7.8, 66, 0.2], [7.4, 50, -2.6], [7.4, 40, -2.8], [7.6, 24, -1.8], [7.6, 9, -1.2], [7.8, 4, 3.2], [7.8, 3.6, 9.6]],
    [[-0.6, 96.5, -2.6], [-5.2, 92.5, -1.6], [-8.0, 88.2, 1.6], [-9.2, 80, 2.4], [-9.6, 66, 0.2], [-9.0, 50, -2.6], [-9.0, 40, -2.8], [-9.2, 24, -1.8], [-9.2, 9, -1.2], [-9.4, 4, 3.2], [-9.4, 3.6, 9.6]],
    [[-2.8, 134, 0.6], [-3.6, 141, 1.4], [-4.0, 150, 1.8], [-4.2, 157, 2.2]],
    [[-1.2, 135, 0.8], [3.4, 141, 1.4], [4.0, 150, 1.8], [4.2, 157, 2.2]],
    [[-2.8, 135, 0.2], [-7.6, 139.6, 0.2], [-13.4, 137.6, -0.4], [-17.6, 131, -0.8], [-20.4, 118, -0.8], [-22.4, 109, 0.6], [-25, 98, 1.6], [-27.4, 88, 2.0], [-28.6, 82, 2.6]],
    [[-1.0, 135, 0.4], [7.6, 139.6, 0.2], [13.4, 137.6, -0.4], [17.6, 131, -0.8], [20.4, 118, -0.8], [22.4, 109, 0.6], [25, 98, 1.6], [27.4, 88, 2.0], [28.6, 82, 2.6]],
  ],
  nerves: [
    [[3.0, 94, -6.5], [5.4, 88, -6.4], [8.6, 80, -5.2], [9.2, 66, -4.8], [9.0, 50, -4.6], [9.0, 44, -4.6], [8.6, 30, -4.0], [8.4, 12, -3.6], [8.4, 4, -1.0], [8.4, 2.6, 6.0]],
    [[-3.0, 94, -6.5], [-5.4, 88, -6.4], [-8.6, 80, -5.2], [-9.2, 66, -4.8], [-9.0, 50, -4.6], [-9.0, 44, -4.6], [-8.6, 30, -4.0], [-8.4, 12, -3.6], [-8.4, 4, -1.0], [-8.4, 2.6, 6.0]],
    [[3.2, 143, -4.4], [8.6, 139, -2.6], [15.2, 134, -2.0], [18.8, 120, -1.2], [21.4, 108, 0.6], [24.6, 97, 1.4], [27.2, 87, 1.8], [28.6, 80, 2.2]],
    [[-3.2, 143, -4.4], [-8.6, 139, -2.6], [-15.2, 134, -2.0], [-18.8, 120, -1.2], [-21.4, 108, 0.6], [-24.6, 97, 1.4], [-27.2, 87, 1.8], [-28.6, 80, 2.2]],
  ],
};

export function buildVessels() {
  const g = {};
  for (const [k, list] of Object.entries(VESSELS)) {
    g[k] = list.map((pts, i) => sweepTube(pts, (t) => (k === 'nerves' ? 0.42 - t * 0.18 : (i === 0 ? 0.95 : 0.55) * (1 - t * 0.45)), { segments: Math.max(60, pts.length * 14), radial: 10 }));
  }
  return g;
}
