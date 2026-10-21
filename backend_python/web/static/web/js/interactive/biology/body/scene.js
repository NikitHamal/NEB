import { THREE } from '../../core/engine.js';
import { GLTFLoader } from 'three/addons/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/DRACOLoader.js';
import { mergeMeshes, principalAxis } from '../anatomy/merge.js';
import { buildEnvelopeAsync } from '../anatomy/skin.js';
import { toGeometry } from '../anatomy/mesher.js';
import { createTissue } from '../anatomy/tissue.js';
import { buildOrgans, buildVessels } from './organs.js';

const MUSCLE_COLOR = `
  vec3 fd = normalize(vFib + vec3(1e-4));
  vec3 side = normalize(cross(fd, abs(fd.y) < 0.9 ? vec3(0.0, 1.0, 0.0) : vec3(1.0, 0.0, 0.0)));
  float w = tNoise(vObj * 60.0) * 3.0;
  float stri = sin(dot(vObj, side) * 1100.0 + w) * 0.5 + 0.5;
  float stri2 = sin(dot(vObj, cross(fd, side)) * 1100.0 + w) * 0.5 + 0.5;
  vec3 m = vec3(0.46, 0.075, 0.06) * (0.78 + 0.32 * tFbm(vObj * 18.0)) * (0.86 + 0.1 * stri + 0.06 * stri2);
  vec3 tendon = vec3(0.86, 0.84, 0.80) * (0.92 + 0.08 * stri);
  float te = smoothstep(0.55, 0.95, vTend);
  diffuseColor.rgb = mix(m, tendon, te);`;

const BONE_COLOR = `
  float n1 = tFbm(vObj * 22.0);
  vec3 bone = vec3(0.86, 0.80, 0.67) * (0.84 + 0.22 * n1);
  bone = mix(bone, vec3(0.80, 0.70, 0.55), smoothstep(0.55, 0.8, tFbm(vObj * 6.0)) * 0.4);
  vec3 cart = vec3(0.78, 0.84, 0.88) * (0.9 + 0.1 * n1);
  vec3 tooth = vec3(0.95, 0.93, 0.86);
  vec3 c = bone;
  if (vBK > 0.5 && vBK < 1.5) c = cart;
  if (vBK > 1.5) c = tooth;
  diffuseColor.rgb = c;`;

const SKIN_COLOR = `
  float n1 = tFbm(vObj * 9.0);
  vec3 s = vec3(0.47, 0.30, 0.21) * (0.9 + 0.16 * n1);
  s = mix(s, vec3(0.55, 0.30, 0.24), smoothstep(0.5, 0.8, tFbm(vObj * 3.0 + 4.0)) * 0.35);
  diffuseColor.rgb = s;`;

const ORGAN_COLORS = {
  liver: ['vec3(0.34, 0.09, 0.06)', 0.4], gallbladder: ['vec3(0.22, 0.38, 0.18)', 0.3], spleen: ['vec3(0.36, 0.09, 0.15)', 0.4],
  kidney: ['vec3(0.44, 0.12, 0.09)', 0.4], adrenal: ['vec3(0.78, 0.55, 0.22)', 0.5], bladder: ['vec3(0.82, 0.62, 0.52)', 0.45],
  brain: ['vec3(0.84, 0.64, 0.62)', 0.55], esophagus: ['vec3(0.72, 0.42, 0.40)', 0.4], stomach: ['vec3(0.80, 0.50, 0.44)', 0.4],
  pancreas: ['vec3(0.86, 0.66, 0.48)', 0.5], colon: ['vec3(0.78, 0.58, 0.47)', 0.45], small: ['vec3(0.86, 0.60, 0.52)', 0.45],
  ureter: ['vec3(0.84, 0.70, 0.62)', 0.4], ureter2: ['vec3(0.84, 0.70, 0.62)', 0.4], cord: ['vec3(0.92, 0.86, 0.66)', 0.45],
};

const CARTILAGE = /cartilage|meniscus|disc|symphysis/i;
const TOOTH = /incisor|canine|premolar|molar/i;

function loadGLB(url, onProgress) {
  const loader = new GLTFLoader();
  const draco = new DRACOLoader();
  draco.setDecoderPath('/static/web/js/vendor/draco/');
  loader.setDRACOLoader(draco);
  return new Promise((resolve, reject) => loader.load(url, (g) => { draco.dispose(); resolve(g); }, onProgress, reject));
}

function cleanName(n, x) {
  let s = n.replace(/\.\d+$/, '').replace(/\s+\(.*?\)\s*$/, '').trim();
  s = s.charAt(0).toUpperCase() + s.slice(1);
  if (Math.abs(x) > 0.012) s += x > 0 ? ' (left)' : ' (right)';
  return s;
}

export async function buildBody(quality, { onProgress, onStage } = {}) {
  const gltf = await loadGLB('/static/web/js/interactive/biology/models/body.glb', onProgress);
  onStage && onStage('Preparing bones and muscles…');
  await new Promise((r) => setTimeout(r, 0));
  gltf.scene.updateMatrixWorld(true);
  const bones = []; const muscles = [];
  gltf.scene.traverse((o) => {
    if (!o.isMesh) return;
    const name = o.material && o.material.name || '';
    (name.includes('Bone') ? bones : muscles).push(o);
  });
  const boneNames = []; const muscleNames = [];
  const tmp = new THREE.Vector3();
  const centroid = (m) => { m.geometry.computeBoundingBox(); return m.geometry.boundingBox.getCenter(tmp).applyMatrix4(m.matrixWorld).x; };
  const nm = (m) => m.userData.name || m.name;
  bones.forEach((m) => boneNames.push(cleanName(nm(m), centroid(m))));
  muscles.forEach((m) => muscleNames.push(cleanName(nm(m), centroid(m))));

  const boneGeo = mergeMeshes(bones, {
    attrs: { bk: 1 },
    fill(ex, m, pos, start, count) { const n = m.userData.name || m.name; const k = TOOTH.test(n) ? 2 : CARTILAGE.test(n) ? 1 : 0; ex.bk.fill(k, start, start + count); },
  });
  const muscleGeo = mergeMeshes(muscles, {
    attrs: { fib: 3, tend: 1 },
    fill(ex, m, pos, start, count) {
      const { c, axis } = principalAxis(pos, start, count);
      let lo = Infinity; let hi = -Infinity;
      for (let i = start; i < start + count; i++) {
        const t = (pos[i * 3] - c[0]) * axis[0] + (pos[i * 3 + 1] - c[1]) * axis[1] + (pos[i * 3 + 2] - c[2]) * axis[2];
        lo = Math.min(lo, t); hi = Math.max(hi, t);
      }
      const flat = /diaphragm|oblique|transvers|intercostal/i.test(m.userData.name || m.name);
      for (let i = start; i < start + count; i++) {
        ex.fib[i * 3] = axis[0]; ex.fib[i * 3 + 1] = axis[1]; ex.fib[i * 3 + 2] = axis[2];
        const t = (pos[i * 3] - c[0]) * axis[0] + (pos[i * 3 + 1] - c[1]) * axis[1] + (pos[i * 3 + 2] - c[2]) * axis[2];
        const u = (t - lo) / Math.max(1e-6, hi - lo);
        ex.tend[i] = flat ? 0 : Math.pow(Math.abs(u * 2 - 1), 3) * (hi - lo > 0.06 ? 1 : 0.4);
      }
    },
  });
  bones.forEach((m) => m.geometry.dispose());
  muscles.forEach((m) => m.geometry.dispose());

  const shared = { uTime: { value: 0 }, uBeatV: { value: 0 }, uBeatA: { value: 0 }, uBreath: { value: 0 }, uTextbook: { value: 0 } };
  const own = () => ({ ...shared, uXray: { value: 0 }, uHi: { value: -1 }, uHiAmt: { value: 0 } });
  const boneMat = createTissue({
    key: 'bone', uniforms: own(), color_fragment: BONE_COLOR, roughness: 0.55, clearcoat: 0.25, clearcoatRoughness: 0.5, sheen: 0.2, sheenColor: 0xfff2dc,
    vertexAttrs: 'attribute float bk; varying float vBK;', fragmentHead: 'varying float vBK;', vertex: 'vBK = bk;',
    bump: 'tFbm(vObj * 140.0)', bumpAmt: 0.0006, sss: 'vec3(0.45, 0.32, 0.2)',
  });
  const muscleMat = createTissue({
    key: 'muscle', uniforms: own(), color_fragment: MUSCLE_COLOR, roughness: 0.4, clearcoat: 0.55, clearcoatRoughness: 0.28, sheen: 0.4, sheenColor: 0xff9f90,
    vertexAttrs: 'attribute vec3 fib; attribute float tend; varying vec3 vFib; varying float vTend;', fragmentHead: 'varying vec3 vFib; varying float vTend;',
    vertex: 'vFib = fib; vTend = tend;', bump: 'sin(dot(vObj, normalize(cross(normalize(vFib + vec3(1e-4)), vec3(0.0, 1.0, 0.0)))) * 1100.0) * 0.5', bumpAmt: 0.00025,
  });
  const boneMesh = new THREE.Mesh(boneGeo, boneMat);
  const muscleMesh = new THREE.Mesh(muscleGeo, muscleMat);
  boneMesh.userData.names = boneNames;
  muscleMesh.userData.names = muscleNames;

  const landmarks = { canal: [] };
  onStage && onStage('Growing the skin…');
  await new Promise((r) => setTimeout(r, 0));
  const all = new Float32Array(boneGeo.attributes.position.count * 3 + muscleGeo.attributes.position.count * 3);
  all.set(boneGeo.attributes.position.array, 0);
  all.set(muscleGeo.attributes.position.array, boneGeo.attributes.position.array.length);
  const cell = quality.tier === 'low' ? 0.011 : quality.tier === 'medium' ? 0.0085 : 0.0068;
  const env = await buildEnvelopeAsync(all, { min: [-0.37, -0.02, -0.17], max: [0.37, 1.74, 0.18] }, cell, { dilate: 1, blur: 2, blurPasses: 2, threshold: 0.42 });
  const skinGeo = toGeometry(THREE, env, { kind: [new Float32Array(env.count), 1], fat: [new Float32Array(env.count), 1], part: [new Float32Array(env.count), 1] });
  const skinMat = createTissue({
    key: 'skin', side: THREE.FrontSide, uniforms: own(), color_fragment: SKIN_COLOR, roughness: 0.52, clearcoat: 0.12, clearcoatRoughness: 0.5, sheen: 0.45, sheenColor: 0xffd2b8,
    bump: 'tNoise(vObj * 900.0) * 0.5 + tFbm(vObj * 60.0) * 0.5', bumpAmt: 0.00018, sss: 'vec3(0.75, 0.24, 0.12)',
  });
  const skin = new THREE.Mesh(skinGeo, skinMat);

  onStage && onStage('Placing the organs…');
  await new Promise((r) => setTimeout(r, 0));
  const canal = [];
  ['Atlas (C1)', 'Vertebra C3', 'Vertebra C5', 'Vertebra C7', 'Vertebra T2', 'Vertebra T4', 'Vertebra T6', 'Vertebra T8', 'Vertebra T10', 'Vertebra T12', 'Vertebra L1'].forEach((n) => {
    let m = null; gltf.scene.traverse((o) => { if (!m && o.isMesh && (o.userData.name || o.name) === n) m = o; });
    if (!m || !m.isMesh) return;
    const box = new THREE.Box3().setFromObject(m);
    canal.push([0, (box.min.y + box.max.y) * 50, (box.min.z + (box.max.z - box.min.z) * 0.32) * 100]);
  });
  canal.unshift([0, canal.length ? canal[0][1] + 6 : 155, canal.length ? canal[0][2] + 1 : -3]);
  landmarks.canal = canal;
  const organGeo = buildOrgans(quality, landmarks);
  const organs = new THREE.Group();
  organs.scale.setScalar(0.01);
  const organMeshes = {};
  for (const [k, g] of Object.entries(organGeo)) {
    if (!g.attributes.kind) {
      const n = g.attributes.position.count;
      g.setAttribute('kind', new THREE.BufferAttribute(new Float32Array(n), 1));
      g.setAttribute('fat', new THREE.BufferAttribute(new Float32Array(n), 1));
      g.setAttribute('part', new THREE.BufferAttribute(new Float32Array(n), 1));
    }
    const [col, rough] = ORGAN_COLORS[k] || ['vec3(0.8,0.5,0.45)', 0.45];
    const extra = k === 'brain' ? 'c *= 0.82 + 0.25 * smoothstep(0.2, 0.8, tFbm(vObj * 1.6)); c *= 0.8 + 0.25 * smoothstep(0.3, 0.7, tNoise(vObj * 2.2));'
      : k === 'stomach' ? 'c *= 0.86 + 0.18 * sin(vObj.y * 9.0 + tNoise(vObj * 2.0) * 4.0);'
        : k === 'small' || k === 'colon' ? 'c *= 0.88 + 0.16 * tFbm(vObj * 3.0);'
          : k === 'liver' || k === 'spleen' || k === 'kidney' ? 'c *= 0.85 + 0.25 * tFbm(vObj * 2.5);' : 'c *= 0.9 + 0.15 * tFbm(vObj * 3.0);';
    const mat = createTissue({ key: `organ-${k}`, side: THREE.FrontSide, uniforms: own(), roughness: rough, clearcoat: 0.75, clearcoatRoughness: 0.2, color_fragment: `vec3 c = ${col}; ${extra} diffuseColor.rgb = c;`, bump: 'tFbm(vObj * 4.0)', bumpAmt: 0.02, sss: 'vec3(0.5, 0.12, 0.08)' });
    const mesh = new THREE.Mesh(g, mat);
    mesh.userData.organ = k.replace(/2$/, '');
    organs.add(mesh);
    organMeshes[k] = mesh;
  }
  const vessels = new THREE.Group();
  vessels.scale.setScalar(0.01);
  const V = buildVessels();
  const vesselMats = {};
  for (const [k, list] of Object.entries(V)) {
    const col = k === 'arteries' ? 'vec3(0.72, 0.06, 0.05)' : k === 'veins' ? 'vec3(0.12, 0.2, 0.62)' : 'vec3(0.92, 0.78, 0.3)';
    const mat = createTissue({
      key: `vessel-${k}`, side: THREE.FrontSide, uniforms: own(), roughness: 0.35, clearcoat: 0.8,
      vertexAttrs: 'attribute float along; varying float vAlong;', fragmentHead: 'varying float vAlong;', vertex: 'vAlong = along;',
      color_fragment: `vec3 c = ${col}; ${k === 'arteries' ? 'float pl = pow(max(0.0, sin((vAlong * 6.0 - uTime * 1.2) * 6.283)), 18.0); c += vec3(0.9, 0.2, 0.1) * pl * 0.8;' : k === 'nerves' ? 'float pl = pow(max(0.0, sin((vAlong * 10.0 - uTime * 3.0) * 6.283)), 30.0); c += vec3(1.0, 0.9, 0.5) * pl;' : ''} diffuseColor.rgb = c;`,
      sss: k === 'nerves' ? 'vec3(0.5, 0.4, 0.1)' : 'vec3(0.3, 0.05, 0.1)',
    });
    vesselMats[k] = mat;
    const grp = new THREE.Group();
    list.forEach((g) => {
      const n = g.attributes.position.count;
      g.setAttribute('kind', new THREE.BufferAttribute(new Float32Array(n), 1));
      g.setAttribute('fat', new THREE.BufferAttribute(new Float32Array(n), 1));
      g.setAttribute('part', new THREE.BufferAttribute(new Float32Array(n), 1));
      const m = new THREE.Mesh(g, mat);
      m.userData.organ = k;
      grp.add(m);
    });
    grp.userData.kind = k;
    vessels.add(grp);
  }
  return { boneMesh, muscleMesh, skin, organs, organMeshes, vessels, materials: { bone: boneMat, muscle: muscleMat, skin: skinMat, vessels: vesselMats }, uniforms: shared };
}
