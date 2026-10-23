// A full-size articulated human skeleton on a stand (1 unit = 10 cm, 1.7 m tall), built from
// turned and swept bone shapes: skull with orbits, nasal aperture, teeth and a separate mandible;
// a curved column of 7 cervical, 12 thoracic and 5 lumbar vertebrae on a sacrum; twelve pairs of
// ribs (true, false and floating) to a sternum; clavicles and scapulae; pelvis; arms and legs with
// carpals, tarsals, metacarpals, metatarsals and phalanges. The right shoulder, elbow, hip, knee and
// the atlanto-axial joint are real pivots the practicals can move. Feet stand at y = 0.
import { THREE } from '../../engine.js';
import { mesh, MAT } from '../kit.js';
import { upgradeSkeleton } from './skeleton-real.js';

const V = (x, y, z) => new THREE.Vector3(x, y, z);
let BONE = null;
const bone = () => { if (!BONE) { BONE = new THREE.MeshPhysicalMaterial({ color: 0xeee2c4, roughness: 0.55, clearcoat: 0.25, sheen: 0.2, sheenColor: new THREE.Color(0xfff3dc) }); BONE.userData.sharedFx = true; } return BONE; };

/** A long bone from a to b: a shaft with swollen ends (epiphyses). */
export function longBone(a, b, r, mat = bone(), knob = 1.8) {
  const d = new THREE.Vector3().subVectors(b, a); const L = d.length();
  const prof = [[0.001, 0], [r * knob * 0.8, 0.02 * L], [r * knob, 0.06 * L], [r * knob * 0.75, 0.13 * L], [r, 0.22 * L], [r * 0.92, 0.5 * L], [r, 0.78 * L], [r * knob * 0.75, 0.87 * L], [r * knob, 0.94 * L], [r * knob * 0.8, 0.98 * L], [0.001, L]];
  const m = mesh(new THREE.LatheGeometry(prof.map(([x, y]) => new THREE.Vector2(x, y)), 14), mat);
  m.position.copy(a); m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize());
  return m;
}
function blob(rx, ry, rz, pos, mat = bone(), seg = 16) { const m = mesh(new THREE.SphereGeometry(1, seg, Math.max(8, seg >> 1)), mat); m.scale.set(rx, ry, rz); m.position.copy(pos); return m; }
function tube(pts, r, mat = bone(), seg = 24) { return mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), seg, r, 7, false), mat); }

function skull() {
  const g = new THREE.Group(); const dark = MAT.matte(0x2a1d14);
  g.add(blob(0.78, 0.82, 0.98, V(0, 0.25, -0.12), bone(), 24));
  g.add(blob(0.62, 0.55, 0.6, V(0, -0.18, 0.28), bone(), 18));
  [-1, 1].forEach((s) => { g.add(blob(0.2, 0.19, 0.12, V(s * 0.3, 0.02, 0.72), dark, 12)); g.add(blob(0.16, 0.12, 0.3, V(s * 0.62, -0.12, 0.2), bone(), 10)); });
  g.add(blob(0.09, 0.15, 0.08, V(0, -0.22, 0.82), dark, 10));
  for (let i = 0; i < 10; i++) { const a = (i / 9 - 0.5) * 1.6; g.add(mesh(new THREE.BoxGeometry(0.07, 0.11, 0.06), MAT.gloss(0xf8f1df), [Math.sin(a) * 0.36, -0.52, 0.52 + Math.cos(a) * 0.2 - 0.2])); }
  return g;
}
function mandible() {
  const g = new THREE.Group();
  const pts = [V(-0.55, 0.15, -0.05), V(-0.5, -0.25, 0.15), V(-0.3, -0.45, 0.55), V(0, -0.5, 0.72), V(0.3, -0.45, 0.55), V(0.5, -0.25, 0.15), V(0.55, 0.15, -0.05)];
  g.add(tube(pts, 0.1, bone(), 30));
  for (let i = 0; i < 10; i++) { const a = (i / 9 - 0.5) * 1.6; g.add(mesh(new THREE.BoxGeometry(0.07, 0.1, 0.06), MAT.gloss(0xf8f1df), [Math.sin(a) * 0.36, -0.36, 0.5 + Math.cos(a) * 0.2 - 0.2])); }
  return g;
}
function vertebra(r) {
  const g = new THREE.Group();
  g.add(mesh(new THREE.CylinderGeometry(r, r, r * 0.75, 12), bone()));
  g.add(mesh(new THREE.BoxGeometry(r * 0.35, r * 0.4, r * 1.6), bone(), [0, 0, -r * 1.2]));
  g.add(mesh(new THREE.BoxGeometry(r * 2.4, r * 0.3, r * 0.35), bone(), [0, 0, -r * 0.7]));
  return g;
}
function hand(s) {
  const g = new THREE.Group();
  for (let i = 0; i < 8; i++) g.add(blob(0.09, 0.08, 0.08, V(s * ((i % 4) - 1.5) * 0.12, -0.08 - Math.floor(i / 4) * 0.13, 0), bone(), 8));
  for (let f = 0; f < 5; f++) {
    const x = s * (f - 2) * 0.13; const thumb = f === (s > 0 ? 0 : 4);
    const segs = thumb ? [0.42, 0.3, 0.22] : [0.52, 0.36, 0.25, 0.18]; let y = -0.3; let xx = thumb ? x - s * 0.15 : x;
    segs.forEach((L, k) => { const a = V(xx, y, thumb ? 0.1 : 0); const b = V(xx + (thumb ? -s * 0.08 : 0), y - L * (thumb ? 0.8 : 1), thumb ? 0.18 : 0); g.add(longBone(a, b, k ? 0.03 : 0.035, bone(), 1.5)); y -= L * (thumb ? 0.8 : 1) + 0.02; xx = b.x; });
  }
  return g;
}
function foot(s) {
  const g = new THREE.Group();
  g.add(blob(0.2, 0.22, 0.32, V(0, -0.25, -0.15), bone(), 10));
  for (let i = 0; i < 5; i++) g.add(blob(0.11, 0.1, 0.12, V(s * (i - 2) * 0.1, -0.3, 0.25 + (i % 2) * 0.08), bone(), 8));
  for (let t = 0; t < 5; t++) { const x = s * (t - 2) * 0.13; const a = V(x, -0.38, 0.4); const b = V(x * 1.15, -0.62, 1.15 - Math.abs(t - 2) * 0.08); g.add(longBone(a, b, t === 2 ? 0.05 : 0.04, bone(), 1.5)); g.add(longBone(b, b.clone().add(V(0, -0.04, t === 2 ? 0.3 : 0.22)), 0.035, bone(), 1.5)); }
  return g;
}

export function buildSkeleton() {
  const root = new THREE.Group(); const B = {}; const J = {};
  // stand
  root.add(mesh(new THREE.CylinderGeometry(1.4, 1.5, 0.12, 28), MAT.gloss(0x1f2937), [0, 0.06, -0.9]));
  root.add(mesh(new THREE.CylinderGeometry(0.07, 0.07, 9.6, 10), MAT.steel(), [0, 4.8, -0.9]));
  root.add(mesh(new THREE.BoxGeometry(0.14, 0.14, 0.8), MAT.steel(), [0, 9.5, -0.5]));
  // pelvis and sacrum
  const pelvis = new THREE.Group(); pelvis.position.set(0, 9.4, 0); root.add(pelvis); B.Pelvis = pelvis;
  [-1, 1].forEach((s) => { const il = blob(0.85, 0.78, 0.2, V(s * 0.85, 0.55, -0.1), bone(), 18); il.rotation.set(0.25, s * 0.55, s * 0.35); pelvis.add(il); pelvis.add(mesh(new THREE.TorusGeometry(0.42, 0.11, 8, 18, Math.PI * 1.3), bone(), [s * 0.55, -0.35, 0.35]).rotateY(s * 0.6)); });
  pelvis.add(blob(0.42, 0.55, 0.22, V(0, 0.2, -0.45), bone(), 12));
  pelvis.add(blob(0.12, 0.14, 0.1, V(0, -0.55, 0.62), bone(), 8));
  // column: lumbar, thoracic, cervical along an S curve
  const spine = new THREE.Group(); root.add(spine); B.Spine = spine;
  const vy = []; for (let i = 0; i < 24; i++) vy.push(10.05 + i * (5.75 / 24));
  vy.forEach((y, i) => { const lumbar = i < 5; const cerv = i >= 17; const r = lumbar ? 0.26 : cerv ? 0.15 : 0.2 + (11 - Math.min(11, i - 5)) * 0.004; const v = vertebra(r); const z = -0.35 + Math.sin((y - 10) / 5.75 * Math.PI * 1.15) * -0.18; v.position.set(0, y, z); spine.add(v); });
  // ribs and sternum
  const chest = new THREE.Group(); root.add(chest); B.Ribs = chest;
  for (let i = 0; i < 12; i++) {
    const y = 14.4 - i * 0.27; const w = 0.9 + Math.sin(Math.min(1, (i + 1) / 7) * Math.PI / 2) * 0.75 - Math.max(0, i - 8) * 0.12; const d = 0.75 + Math.min(i, 6) * 0.08;
    [-1, 1].forEach((s) => {
      const len = i < 7 ? 1 : i < 10 ? 0.92 : 0.55;
      const pts = []; for (let k = 0; k <= 10; k++) { const a = -Math.PI / 2 + k / 10 * Math.PI * len; pts.push(V(s * Math.cos(a) * w, y - k * 0.04 - (1 - Math.cos(a)) * 0.15, Math.sin(a) * d * 0.9 + 0.15)); }
      chest.add(tube(pts, 0.05, bone(), 20));
    });
  }
  chest.add(mesh(new THREE.BoxGeometry(0.32, 1.7, 0.08), bone(), [0, 13.65, 0.98]));
  chest.add(mesh(new THREE.BoxGeometry(0.36, 0.42, 0.08), bone(), [0, 14.6, 0.9]));
  // shoulder girdle
  [-1, 1].forEach((s) => {
    chest.add(tube([V(s * 0.2, 14.75, 0.85), V(s * 0.9, 14.85, 0.75), V(s * 1.5, 14.9, 0.25), V(s * 1.9, 14.85, -0.05)], 0.06, bone(), 16));
    const sc = new THREE.Shape(); sc.moveTo(0, 0); sc.lineTo(s * 1.0, 0.1); sc.lineTo(s * 0.25, -1.4); sc.lineTo(0, 0);
    const scap = mesh(new THREE.ExtrudeGeometry(sc, { depth: 0.06, bevelEnabled: false }), bone(), [s * 0.75, 14.75, -0.75]); scap.rotation.y = s * 0.35; chest.add(scap);
  });
  B.Clavicle = chest; B.Scapula = chest;
  // head on the atlas: a pivot about the vertical axis
  J.neck = new THREE.Group(); J.neck.position.set(0, 15.85, -0.25); root.add(J.neck);
  const sk = skull(); sk.position.set(0, 0.85, 0.05); J.neck.add(sk); B.Skull = sk;
  const md = mandible(); md.position.set(0, 0.4, 0.15); J.neck.add(md); B.Mandible = md;
  // arms: the right one is articulated (shoulder ball-and-socket, elbow hinge, radio-ulnar, wrist)
  const arm = (s) => {
    const sh = new THREE.Group(); sh.position.set(s * 1.95, 14.55, 0); root.add(sh);
    const hum = longBone(V(0, 0, 0), V(s * 0.15, -3.0, -0.05), 0.11); sh.add(hum);
    const el = new THREE.Group(); el.position.set(s * 0.15, -3.05, -0.05); sh.add(el);
    const fore = new THREE.Group(); el.add(fore);
    fore.add(longBone(V(s * 0.08, 0, 0), V(s * 0.16, -2.5, 0.08), 0.06));
    fore.add(longBone(V(-s * 0.06, 0.05, -0.02), V(-s * 0.02, -2.5, 0.0), 0.06));
    const wr = new THREE.Group(); wr.position.set(s * 0.06, -2.6, 0.04); fore.add(wr); wr.add(hand(s));
    return { sh, hum, el, fore, wr };
  };
  const RA = arm(-1); const LA = arm(1);
  J.shoulder = RA.sh; J.elbow = RA.el; J.wrist = RA.wr; B.Humerus = RA.hum; B['Radius and ulna'] = RA.fore;
  // legs: the right hip (ball and socket) and knee (hinge) are articulated
  const leg = (s) => {
    const hip = new THREE.Group(); hip.position.set(s * 0.95, 9.05, 0.1); root.add(hip);
    const fem = longBone(V(0, 0, 0), V(s * -0.1, -4.25, 0.05), 0.15); hip.add(fem);
    hip.add(blob(0.2, 0.2, 0.2, V(-s * 0.15, 0.1, 0), bone(), 10));
    const kn = new THREE.Group(); kn.position.set(s * -0.1, -4.35, 0.05); hip.add(kn);
    const pat = blob(0.16, 0.2, 0.08, V(0, 0.05, 0.25), bone(), 10); kn.add(pat);
    const shin = new THREE.Group(); kn.add(shin);
    const tib = longBone(V(0, 0, 0), V(0, -3.85, -0.05), 0.13); shin.add(tib);
    shin.add(longBone(V(s * 0.28, -0.15, -0.08), V(s * 0.26, -3.8, -0.1), 0.05));
    const ft = foot(s); ft.position.set(0, -3.75, -0.05); shin.add(ft);
    return { hip, fem, kn, shin, pat, tib, ft };
  };
  const RL = leg(-1); const LL = leg(1);
  J.hip = RL.hip; J.knee = RL.kn; J.shin = RL.shin; B.Femur = LL.fem; B.Patella = LL.pat; B.Tibia = LL.tib;
  const sites = {
    'Skull sutures': V(0, 17.55, -0.1), 'Atlas–axis (neck)': V(0, 15.75, -0.35), Shoulder: V(-1.95, 14.55, 0.1), Elbow: V(-1.82, 11.5, 0), 'Wrist (carpals)': V(-1.8, 8.85, 0.1),
    'Intervertebral discs': V(0, 11.0, -0.25), 'Pubic symphysis': V(0, 8.85, 0.65), Hip: V(-0.95, 9.05, 0.25), Knee: V(-0.85, 4.7, 0.3), Ankle: V(-0.85, 0.85, 0.1),
    'Big toe joint': V(-0.95, 0.2, 1.45), 'Finger joints': V(-1.88, 7.55, 0.05), 'Lumbar spine': V(0, 10.6, -0.3), Thigh: V(-0.95, 7, 0.2), Leg: V(-0.9, 2.8, 0.15),
  };
  const out = { root, B, J, RA, LA, RL, LL, sites, bone };
  upgradeSkeleton(out);
  return out;
}
