import { ellipsoid, tube, capsule, smin, smax, norm, catmull } from '../anatomy/sdf.js';
import { surfaceNets, vertexAttribute } from '../anatomy/mesher.js';

const AX = norm([0.42, -0.83, 0.39]);
const AXR = norm([0.3, -0.85, 0.45]);

const LV = ellipsoid([1.7, -1.4, 0.2], [3.1, 4.6, 3.1], AX);
const RV = ellipsoid([-0.5, -1.0, 1.5], [3.3, 3.9, 2.3], AXR, 0.3);
const RA = ellipsoid([-3.1, 1.4, 0.0], [2.3, 2.7, 2.3], [0.1, 1, 0.1]);
const LA = ellipsoid([0.6, 2.3, -2.4], [2.8, 1.9, 2.0]);
const RAU = ellipsoid([-2.0, 2.9, 1.5], [1.5, 0.95, 1.1], [0.6, 0.3, 0.7]);
const LAU = ellipsoid([2.9, 2.1, 0.9], [1.4, 0.75, 1.0], [0.4, 0.5, 0.8]);

export const PATHS = {
  aorta: catmull([[0.6, 0.6, 0.1], [0.3, 3.0, 0.5], [0.0, 5.4, 0.4], [0.7, 6.9, -0.6], [2.1, 7.1, -2.0], [2.9, 5.7, -3.0], [3.0, 2.5, -3.6], [2.9, -1.0, -3.6], [2.7, -6.8, -3.2]], 6),
  brachio: [[0.4, 6.6, -0.2], [-0.6, 8.4, 0.1], [-1.3, 10.4, 0.3]],
  carotid: [[1.3, 7.3, -1.0], [1.5, 9.0, -0.8], [1.7, 10.8, -0.6]],
  subclavian: [[2.1, 7.1, -1.8], [3.0, 8.6, -1.9], [4.0, 10.0, -1.8]],
  trunk: catmull([[0.9, 0.6, 2.2], [1.2, 2.6, 2.0], [1.5, 4.2, 1.0], [1.4, 5.0, -0.2]], 6),
  lpa: catmull([[1.4, 5.0, -0.2], [3.4, 5.2, -1.4], [5.4, 4.8, -2.2]], 6),
  rpa: catmull([[1.4, 5.0, -0.2], [-0.5, 4.9, -1.7], [-2.8, 4.7, -2.1], [-4.8, 4.5, -2.3]], 6),
  svc: [[-2.8, 2.4, -0.2], [-2.7, 5.5, -0.3], [-2.6, 8.8, -0.4]],
  ivc: [[-2.6, 0.2, -1.0], [-2.6, -2.5, -1.4], [-2.6, -5.8, -1.8]],
  rspv: [[-0.9, 2.9, -2.9], [-2.5, 3.2, -3.2], [-4.4, 3.3, -3.4]],
  ripv: [[-0.8, 1.6, -3.0], [-2.4, 1.4, -3.3], [-4.2, 1.2, -3.6]],
  lspv: [[2.2, 3.0, -2.9], [3.6, 3.4, -3.1], [5.3, 3.6, -3.2]],
  lipv: [[2.3, 1.7, -3.0], [3.7, 1.5, -3.2], [5.3, 1.4, -3.4]],
};

const AORTA = tube(PATHS.aorta, 1.35, 1.05);
const ARCH = [tube(PATHS.brachio, 0.62, 0.52), tube(PATHS.carotid, 0.42, 0.38), tube(PATHS.subclavian, 0.48, 0.42)];
const TRUNK = tube(PATHS.trunk, 1.3, 1.2);
const PA = [tube(PATHS.lpa, 0.95, 0.8), tube(PATHS.rpa, 0.9, 0.75)];
const SVC = tube(PATHS.svc, 1.05, 1.0);
const IVC = tube(PATHS.ivc, 1.15, 1.1);
const PV = [tube(PATHS.rspv, 0.6, 0.55), tube(PATHS.ripv, 0.58, 0.52), tube(PATHS.lspv, 0.6, 0.55), tube(PATHS.lipv, 0.58, 0.52)];

const LVC = ellipsoid([1.6, -1.25, 0.25], [1.75, 3.4, 1.75], AX);
const RVC0 = ellipsoid([-0.6, -0.9, 1.65], [2.75, 3.25, 1.7], AXR, 0.3);
const RAC = ellipsoid([-3.1, 1.4, 0.0], [1.95, 2.35, 1.95], [0.1, 1, 0.1]);
const LAC = ellipsoid([0.6, 2.3, -2.4], [2.45, 1.55, 1.65]);
const lumen = (path, r0, r1) => tube(path, r0, r1);
const LUMENS = [
  lumen([[1.2, -0.6, 0.2], ...PATHS.aorta.slice(1)], 0.98, 0.72),
  lumen([[0.0, -0.4, 1.8], ...PATHS.trunk.slice(1)], 0.94, 0.86),
  lumen(PATHS.lpa, 0.62, 0.5), lumen(PATHS.rpa, 0.58, 0.46),
  lumen([[-3.0, 1.4, 0], ...PATHS.svc.slice(1)], 0.72, 0.68), lumen([[-3.0, 0.8, -0.4], ...PATHS.ivc.slice(1)], 0.8, 0.76),
  lumen(PATHS.brachio, 0.36, 0.3), lumen(PATHS.carotid, 0.2, 0.18), lumen(PATHS.subclavian, 0.24, 0.2),
  ...[PATHS.rspv, PATHS.ripv, PATHS.lspv, PATHS.lipv].map((pth) => lumen([[0.6, 2.3, -2.4], ...pth.slice(1)], 0.32, 0.28)),
];

const SULCI = [
  catmull([[1.5, 1.6, 2.6], [1.2, -1.0, 3.4], [2.2, -3.6, 3.4], [3.4, -5.0, 2.8]], 8),
  catmull([[-1.6, 1.3, 2.0], [-3.0, 0.4, 1.8], [-3.4, -0.4, 0.4], [-2.6, -0.2, -1.8], [-0.8, 0.6, -2.6]], 8),
  catmull([[2.0, 1.4, 1.6], [3.6, 0.4, 0.6], [3.8, 0.0, -1.2], [2.4, 0.4, -2.6], [0.6, 0.4, -2.8]], 8),
  catmull([[0.0, -0.4, -2.4], [1.0, -2.6, -2.0], [2.6, -4.6, -0.4], [3.4, -5.2, 1.6]], 8),
];
const GROOVES = SULCI.map((s) => tube(s, 0.32));

function chambers(p) {
  let d = smin(LV(p), RV(p), 0.9);
  d = smin(d, RA(p), 0.9);
  d = smin(d, LA(p), 1.0);
  d = smin(d, RAU(p), 0.5);
  d = smin(d, LAU(p), 0.45);
  return d;
}

function vessels(p) {
  let d = AORTA(p);
  for (const a of ARCH) d = smin(d, a(p), 0.35);
  d = Math.min(d, TRUNK(p));
  for (const a of PA) d = smin(d, a(p), 0.3);
  d = Math.min(d, SVC(p), IVC(p));
  for (const a of PV) d = smin(d, a(p), 0.25);
  return d;
}

function grooves(p) { let d = Infinity; for (const g of GROOVES) d = Math.min(d, g(p)); return d; }

function rvCavity(p) { return smax(RVC0(p), -(LV(p) - 0.25), 0.3); }

function cavities(p) {
  let d = Math.min(LVC(p), rvCavity(p), RAC(p), LAC(p));
  for (const l of LUMENS) d = Math.min(d, l(p));
  return d;
}

export function heartSDF(p) {
  let outer = smin(chambers(p), vessels(p), 0.55);
  if (outer > 0.8) return outer;
  outer = smax(outer, -grooves(p) - 0.1, 0.3);
  if (outer < -2.5) return smax(outer, -cavities(p), 0.12);
  return smax(outer, -cavities(p), 0.12);
}

export const PARTS = {
  lv: { name: 'Left ventricle', text: 'The strongest chamber. Its wall is up to 1.5 cm thick because it pumps oxygen-rich blood out through the aorta to the whole body, against high pressure.' },
  rv: { name: 'Right ventricle', text: 'Pumps oxygen-poor blood up the pulmonary trunk to the lungs. The lungs are close and low-pressure, so its wall is only about 4 mm thick.' },
  ra: { name: 'Right atrium', text: 'Collects oxygen-poor blood returning from the body through the superior and inferior venae cavae. The heartbeat starts here, in the sinoatrial node.' },
  la: { name: 'Left atrium', text: 'Receives oxygen-rich blood from the lungs through four pulmonary veins and passes it through the mitral valve to the left ventricle.' },
  aorta: { name: 'Aorta', text: 'The body’s largest artery, about 2.5 cm wide. It arches over the heart and sends branches to the head and arms before running down through the chest and abdomen.' },
  arch: { name: 'Branches of the aortic arch', text: 'The brachiocephalic trunk, left common carotid and left subclavian arteries carry blood to the head, brain and arms.' },
  trunk: { name: 'Pulmonary trunk', text: 'Carries oxygen-poor blood from the right ventricle and divides into the left and right pulmonary arteries, the only arteries that carry oxygen-poor blood.' },
  pa: { name: 'Pulmonary arteries', text: 'Take oxygen-poor blood to each lung, where it picks up oxygen in the capillaries around the alveoli.' },
  svc: { name: 'Superior vena cava', text: 'Returns oxygen-poor blood from the head, neck and arms to the right atrium.' },
  ivc: { name: 'Inferior vena cava', text: 'The largest vein, returning oxygen-poor blood from the legs and abdomen to the right atrium.' },
  pv: { name: 'Pulmonary veins', text: 'Four veins that bring freshly oxygenated blood from the lungs to the left atrium, the only veins that carry oxygen-rich blood.' },
  inner: { name: 'Inside the heart', text: 'The chambers are lined with endocardium. Ridges of muscle (trabeculae) and the valves keep blood flowing one way only.' },
};

const KIND = { muscle: 0, artery: 1, vein: 2, inner: 3, pulmArtery: 4, pulmVein: 5 };

export function classify(p) {
  const c = cavities(p);
  if (Math.abs(c) < 0.18 || c < 0) {
    const dl = LUMENS.map((l) => l(p));
    const min = Math.min(...dl);
    if (min < Math.min(LVC(p), rvCavity(p), RAC(p), LAC(p)) - 0.05) {
      const i = dl.indexOf(min);
      return { part: [0, 6, 7, 8].includes(i) ? (i === 0 ? 'aorta' : 'arch') : i === 1 ? 'trunk' : i < 4 ? 'pa' : i === 4 ? 'svc' : i === 5 ? 'ivc' : 'pv', inner: true };
    }
    const d = { lv: LVC(p), rv: rvCavity(p), ra: RAC(p), la: LAC(p) };
    return { part: Object.keys(d).reduce((a, b) => (d[a] < d[b] ? a : b)), inner: true };
  }
  const v = {
    aorta: AORTA(p), arch: Math.min(...ARCH.map((a) => a(p))), trunk: TRUNK(p), pa: Math.min(...PA.map((a) => a(p))),
    svc: SVC(p), ivc: IVC(p), pv: Math.min(...PV.map((a) => a(p))),
  };
  const ch = { lv: LV(p), rv: RV(p), ra: Math.min(RA(p), RAU(p)), la: Math.min(LA(p), LAU(p)) };
  const vb = Object.keys(v).reduce((a, b) => (v[a] < v[b] ? a : b));
  const cb = Object.keys(ch).reduce((a, b) => (ch[a] < ch[b] ? a : b));
  return { part: v[vb] < ch[cb] - 0.15 ? vb : cb, inner: false };
}

const KIND_OF = { aorta: KIND.artery, arch: KIND.artery, trunk: KIND.pulmArtery, pa: KIND.pulmArtery, svc: KIND.vein, ivc: KIND.vein, pv: KIND.pulmVein };

function ventCenterDisp(p, sel, cav, axis) {
  const c = sel.center;
  const d = [p[0] - c[0], p[1] - c[1], p[2] - c[2]];
  const along = d[0] * axis[0] + d[1] * axis[1] + d[2] * axis[2];
  const radial = [d[0] - axis[0] * along, d[1] - axis[1] * along, d[2] - axis[2] * along];
  const k = cav;
  return [-radial[0] * 0.16 * k - axis[0] * along * 0.07 * k, -radial[1] * 0.16 * k - axis[1] * along * 0.07 * k, -radial[2] * 0.16 * k - axis[2] * along * 0.07 * k];
}

export function buildHeart(quality) {
  const cell = quality.tier === 'low' ? 0.24 : quality.tier === 'medium' ? 0.19 : 0.155;
  const mesh = surfaceNets(heartSDF, { min: [-6.2, -8.0, -5.2], max: [6.6, 11.6, 5.2] }, cell);
  const kind = new Float32Array(mesh.count);
  const cR = new Float32Array(mesh.count * 3);
  const cB = new Float32Array(mesh.count * 3);
  const inr = new Float32Array(mesh.count);
  const fat = new Float32Array(mesh.count);
  const dispV = new Float32Array(mesh.count * 3);
  const dispA = new Float32Array(mesh.count * 3);
  const partIdx = new Uint8Array(mesh.count);
  const partNames = Object.keys(PARTS);
  const p = [0, 0, 0];
  for (let i = 0; i < mesh.count; i++) {
    p[0] = mesh.position[i * 3]; p[1] = mesh.position[i * 3 + 1]; p[2] = mesh.position[i * 3 + 2];
    const c = classify(p);
    partIdx[i] = partNames.indexOf(c.inner && !KIND_OF[c.part] ? 'inner' : c.part);
    kind[i] = c.inner ? (KIND_OF[c.part] ?? KIND.inner) : (KIND_OF[c.part] ?? KIND.muscle);
    if (c.inner && KIND_OF[c.part] === undefined) kind[i] = KIND.inner;
    const k = kind[i];
    const real = k === KIND.artery || k === KIND.pulmArtery ? [0.70, 0.50, 0.44] : k === KIND.vein ? [0.30, 0.16, 0.26] : k === KIND.pulmVein ? [0.46, 0.20, 0.24] : [0.48, 0.07, 0.065];
    const book = k === KIND.artery || k === KIND.pulmVein ? [0.75, 0.07, 0.05] : k === KIND.vein || k === KIND.pulmArtery ? [0.14, 0.24, 0.72] : [0.48, 0.07, 0.065];
    cR.set(real, i * 3); cB.set(book, i * 3);
    inr[i] = k === KIND.inner ? 1 : 0;
    const g = grooves(p);
    fat[i] = c.inner ? 0 : Math.max(0, Math.min(1, 1 - (g + 0.05) / 0.55));
    const dv = Math.min(LV(p), RV(p));
    const da = Math.min(RA(p), LA(p), RAU(p), LAU(p));
    const dves = vessels(p);
    const nearVessel = Math.max(0, Math.min(1, (dves - Math.min(dv, da) + 0.6) / 1.2));
    const wV = Math.max(0, Math.min(1, 0.5 + (da - dv) / 1.6)) * nearVessel;
    const wA = Math.max(0, Math.min(1, 0.5 + (dv - da) / 1.6)) * nearVessel;
    const sel = LV(p) < RV(p) ? LV : RV;
    const v = ventCenterDisp(p, sel, wV, sel === LV ? AX : AXR);
    dispV[i * 3] = v[0]; dispV[i * 3 + 1] = v[1]; dispV[i * 3 + 2] = v[2];
    const at = da === RA(p) || da === RAU(p) ? RA.center : LA.center;
    dispA[i * 3] = (at[0] - p[0]) * 0.1 * wA; dispA[i * 3 + 1] = (at[1] - p[1]) * 0.1 * wA; dispA[i * 3 + 2] = (at[2] - p[2]) * 0.1 * wA;
  }
  return { mesh, kind, fat, dispV, dispA, partIdx, partNames, cR, cB, inr };
}

export function coronaryPaths() {
  return {
    lad: SULCI[0].map((q) => [q[0], q[1], q[2] + 0.12]),
    rca: SULCI[1],
    lcx: SULCI[2],
    pda: SULCI[3],
  };
}

export const ANCHORS = {
  lv: [3.2, -3.4, 2.4], rv: [-0.6, -2.0, 3.6], ra: [-5.2, 1.2, 0.6], la: [2.0, 3.4, -4.2],
  aorta: [0.9, 7.6, -0.6], trunk: [1.6, 3.4, 2.6], svc: [-3.6, 7.2, -0.2], ivc: [-2.7, -5.4, -0.6], pv: [5.6, 2.4, -3.2], pa: [-4.6, 5.2, -2.0], arch: [-1.4, 10.2, 0.6],
};

export { KIND, AX, vertexAttribute, capsule };
