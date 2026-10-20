import { THREE } from '../../engine.js';
import { GLTFLoader } from 'three/addons/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/DRACOLoader.js';
import { detail } from '../../detail.js';

let LOAD = null;
function loadBones() {
  if (!LOAD) {
    LOAD = new Promise((resolve, reject) => {
      const loader = new GLTFLoader();
      const draco = new DRACOLoader();
      draco.setDecoderPath('/static/web/js/vendor/draco/');
      loader.setDRACOLoader(draco);
      loader.load('/static/web/js/interactive/biology/models/skeleton.glb', (g) => { g.scene.updateMatrixWorld(true); resolve(g.scene); }, undefined, reject);
    });
  }
  return LOAD;
}

const HAND = /carpal|scaphoid|lunate|triquetrum|pisiform|trapez|capitate|hamate|of hand/i;
const FOOT = /tarsal|calcaneus|talus|cuboid|navicular|cuneiform|of foot|sesamoid/i;

function classify(name, c) {
  const side = c.x < 0 ? 'R' : 'L';
  if (/mandible/i.test(name)) return 'mandible';
  if (/vertebra|atlas|axis/i.test(name)) return 'spine';
  if (/hip bone|sacrum|coccyx/i.test(name)) return 'pelvis';
  if (/rib|sternum|clavicle|scapula|costal/i.test(name)) return 'chest';
  if (/humerus/i.test(name)) return `hum${side}`;
  if (/radius|ulna/i.test(name)) return `fore${side}`;
  if (HAND.test(name)) return `hand${side}`;
  if (/femur/i.test(name)) return `fem${side}`;
  if (/patella/i.test(name)) return `pat${side}`;
  if (/tibia|fibula/i.test(name)) return `tib${side}`;
  if (FOOT.test(name)) return `foot${side}`;
  if (c.y > 1.45) return 'skull';
  return c.y > 1.0 ? 'chest' : 'pelvis';
}

function firstMesh(obj) {
  let m = null;
  obj.traverse((o) => { if (!m && o.isMesh) m = o; });
  return m;
}

function writeInto(target, geos, toLocal, others) {
  let vc = 0; let ic = 0;
  geos.forEach(({ g }) => { vc += g.attributes.position.count; ic += g.index ? g.index.count : g.attributes.position.count; });
  const pos = new Float32Array(vc * 3); const nor = new Float32Array(vc * 3); const idx = new Uint32Array(ic);
  const v = new THREE.Vector3(); const n = new THREE.Vector3(); const nm = new THREE.Matrix3(); const M = new THREE.Matrix4();
  let vo = 0; let io = 0;
  geos.forEach(({ g, world }) => {
    M.multiplyMatrices(toLocal, world);
    nm.getNormalMatrix(M);
    const P = g.attributes.position; const N = g.attributes.normal;
    for (let i = 0; i < P.count; i++) {
      v.fromBufferAttribute(P, i).applyMatrix4(M);
      pos[(vo + i) * 3] = v.x; pos[(vo + i) * 3 + 1] = v.y; pos[(vo + i) * 3 + 2] = v.z;
      if (N) { n.fromBufferAttribute(N, i).applyMatrix3(nm).normalize(); nor[(vo + i) * 3] = n.x; nor[(vo + i) * 3 + 1] = n.y; nor[(vo + i) * 3 + 2] = n.z; }
    }
    if (g.index) for (let i = 0; i < g.index.count; i++) idx[io + i] = g.index.getX(i) + vo;
    else for (let i = 0; i < P.count; i++) idx[io + i] = vo + i;
    vo += P.count; io += g.index ? g.index.count : P.count;
  });
  const shared = others.some((o) => o !== target && o.geometry === target.geometry);
  if (shared) { target.geometry.setDrawRange(0, 0); target.geometry = new THREE.BufferGeometry(); }
  const geo = target.geometry;
  Object.keys(geo.attributes).forEach((k) => geo.deleteAttribute(k));
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  geo.setIndex(new THREE.BufferAttribute(idx, 1));
  geo.clearGroups();
  geo.setDrawRange(0, Infinity);
  geo.computeBoundingSphere(); geo.computeBoundingBox();
  others.forEach((o) => { if (o !== target && o.geometry !== geo) { o.geometry.setDrawRange(0, 0); o.castShadow = false; } });
  geo.setDrawRange(0, Infinity);
}

export function upgradeSkeleton(sk, onDone) {
  loadBones().then((scene) => {
    const groups = {};
    const box = new THREE.Box3(); const c = new THREE.Vector3();
    const boxes = {};
    scene.traverse((o) => {
      if (!o.isMesh) return;
      box.setFromObject(o); box.getCenter(c);
      const k = classify(o.userData.name || o.name, c);
      (groups[k] = groups[k] || []).push({ g: o.geometry, world: o.matrixWorld });
      (boxes[k] = boxes[k] || new THREE.Box3()).union(box);
    });
    const S = 10;
    const P = (v) => v.multiplyScalar(S);
    const joint = {};
    for (const s of ['R', 'L']) {
      const h = boxes[`hum${s}`]; const f = boxes[`fore${s}`]; const fe = boxes[`fem${s}`]; const t = boxes[`tib${s}`];
      if (!h || !f || !fe || !t) continue;
      const med = s === 'R' ? 1 : -1;
      joint[`sh${s}`] = P(new THREE.Vector3(med > 0 ? h.max.x - 0.022 : h.min.x + 0.022, h.max.y - 0.024, (h.min.z + h.max.z) / 2));
      joint[`el${s}`] = P(new THREE.Vector3((h.min.x + h.max.x) / 2, h.min.y + 0.016, (h.min.z + h.max.z) / 2));
      joint[`wr${s}`] = P(new THREE.Vector3((f.min.x + f.max.x) / 2, f.min.y + 0.01, (f.min.z + f.max.z) / 2));
      joint[`hip${s}`] = P(new THREE.Vector3(med > 0 ? fe.max.x - 0.024 : fe.min.x + 0.024, fe.max.y - 0.026, (fe.min.z + fe.max.z) / 2));
      joint[`kn${s}`] = P(new THREE.Vector3((fe.min.x + fe.max.x) / 2, fe.min.y + 0.022, (fe.min.z + fe.max.z) / 2 + 0.005));
      joint[`an${s}`] = P(new THREE.Vector3((t.min.x + t.max.x) / 2, t.min.y + 0.02, (t.min.z + t.max.z) / 2));
    }
    const sp = boxes.spine;
    const neck = boxes.skull ? P(new THREE.Vector3(0, boxes.skull.min.y + 0.012, (sp.min.z + sp.max.z) / 2)) : null;
    const setPivot = (pivot, parentWorldPos, worldPos) => { pivot.rotation.set(0, 0, 0); pivot.position.copy(worldPos).sub(parentWorldPos); };
    const O = new THREE.Vector3();
    const arms = [['R', sk.RA], ['L', sk.LA]]; const legs = [['R', sk.RL], ['L', sk.LL]];
    arms.forEach(([s, A]) => {
      if (!joint[`sh${s}`]) return;
      setPivot(A.sh, O, joint[`sh${s}`]); setPivot(A.el, joint[`sh${s}`], joint[`el${s}`]);
      A.fore.position.set(0, 0, 0); A.fore.rotation.set(0, 0, 0);
      setPivot(A.wr, joint[`el${s}`], joint[`wr${s}`]);
    });
    legs.forEach(([s, L]) => {
      if (!joint[`hip${s}`]) return;
      setPivot(L.hip, O, joint[`hip${s}`]); setPivot(L.kn, joint[`hip${s}`], joint[`kn${s}`]);
      L.shin.position.set(0, 0, 0); L.shin.rotation.set(0, 0, 0);
      setPivot(L.ft, joint[`kn${s}`], joint[`an${s}`]);
    });
    if (neck && sk.J.neck) setPivot(sk.J.neck, O, neck);
    sk.root.updateMatrixWorld(true);
    const rootW = sk.root.matrixWorld;
    const scaleM = new THREE.Matrix4().makeScale(S, S, S);
    const meshesOf = (obj) => { const l = []; obj.traverse((o) => { if (o.isMesh) l.push(o); }); return l; };
    const put = (key, holder, exclude = []) => {
      if (!groups[key] || !holder) return;
      const ms = meshesOf(holder).filter((m) => !exclude.some((e) => e === m || isInside(m, e)));
      const target = ms[0];
      if (!target) return;
      const toLocal = new THREE.Matrix4().copy(target.matrixWorld).invert().multiply(rootW).multiply(scaleM);
      writeInto(target, groups[key], toLocal, ms);
      target.castShadow = true;
    };
    const isInside = (m, holder) => { let p = m.parent; while (p) { if (p === holder) return true; p = p.parent; } return false; };
    put('skull', sk.B.Skull);
    put('mandible', sk.B.Mandible);
    put('spine', sk.B.Spine);
    put('pelvis', sk.B.Pelvis);
    put('chest', sk.B.Ribs);
    arms.forEach(([s, A]) => {
      put(`hum${s}`, A.hum);
      put(`fore${s}`, A.fore, [A.wr]);
      put(`hand${s}`, A.wr);
    });
    legs.forEach(([s, L]) => {
      put(`fem${s}`, L.fem);
      put(`pat${s}`, L.pat);
      put(`tib${s}`, L.shin, [L.pat, L.ft]);
      put(`foot${s}`, L.ft);
    });
    L_extra(sk, joint, neck, boxes, S);
    if (sk.bone) {
      const b = sk.bone();
      b.color.set(0xe9dcc0);
      detail(b, { scale: 14, bump: 0.0012, mottle: 0.16, sss: 0xd9a070, roughVar: 0.4 });
    }
    sk.root.userData.skeleton = sk;
    if (onDone) onDone();
  }).catch(() => {});
}

function L_extra(sk, joint, neck, boxes, S) {
  const s = sk.sites; const set = (k, v) => { if (s[k] && v) s[k].copy(v); };
  set('Shoulder', joint.shR); set('Elbow', joint.elR); set('Wrist (carpals)', joint.wrR); set('Hip', joint.hipR); set('Knee', joint.knR); set('Ankle', joint.anR);
  if (neck) set('Atlas–axis (neck)', neck);
  if (boxes.skull) set('Skull sutures', new THREE.Vector3(0, boxes.skull.max.y * S - 0.15, (boxes.skull.min.z + boxes.skull.max.z) / 2 * S));
  if (boxes.pelvis) set('Pubic symphysis', new THREE.Vector3(0, boxes.pelvis.min.y * S + 0.6, boxes.pelvis.max.z * S - 0.1));
  if (joint.knR && joint.hipR) set('Thigh', joint.knR.clone().lerp(joint.hipR, 0.5));
  if (joint.knR && joint.anR) set('Leg', joint.knR.clone().lerp(joint.anR, 0.5));
  if (boxes.footR) set('Big toe joint', new THREE.Vector3(boxes.footR.max.x * S - 0.25, 0.25, boxes.footR.max.z * S - 0.35));
  if (boxes.handR) set('Finger joints', new THREE.Vector3((boxes.handR.min.x + boxes.handR.max.x) / 2 * S, boxes.handR.min.y * S + 0.6, (boxes.handR.min.z + boxes.handR.max.z) / 2 * S));
  if (boxes.spine) { set('Intervertebral discs', new THREE.Vector3(0, 11.0, boxes.spine.max.z * S - 0.3)); set('Lumbar spine', new THREE.Vector3(0, 10.4, boxes.spine.max.z * S - 0.3)); }
}
