import { THREE, getSoftDotTexture, makeContactShadow } from '../../core/engine.js';
import { rng, canvasTexture, skyDome, outdoorEnvironment, patchMaterial } from './kit.js';
import { groundCanvas, bokehCanvas } from './textures.js';

export const SUN_DIR = new THREE.Vector3(-0.55, 0.62, -0.42).normalize();

// Sunny Terai roadside: blue sky with a warm sun, out-of-focus shrubs and trees, dry grassy ground.
export function buildEnvironment(engine, opts = {}) {
  const { scene, renderer, quality } = engine;
  const tier = quality.tier;
  const rand = rng(31);
  const group = new THREE.Group();
  scene.add(group);

  const env = outdoorEnvironment(renderer, {
    zenith: '#4f86d0', horizon: '#d6e4ec', horizonLow: '#7f9468', ground: '#5d5a3c', sunU: 0.15, sunV: 0.22,
    paint: (g, w, h) => {
      for (let i = 0; i < 26; i++) {
        g.fillStyle = `rgba(${50 + rand() * 40 | 0},${80 + rand() * 40 | 0},${40 + rand() * 20 | 0},0.6)`;
        g.beginPath(); g.arc(rand() * w, h * (0.5 + rand() * 0.06), 4 + rand() * 9, 0, Math.PI * 2); g.fill();
      }
    },
  });
  if (env.texture) scene.environment = env.texture;
  const sky = skyDome({ zenith: 0x3d74c4, horizon: 0xdfe9ee, ground: 0x9aa078, sunDir: SUN_DIR, radius: 1200, sunSize: 2200 });
  group.add(sky);
  scene.fog = new THREE.Fog(0xcfdbe0, 260, 1100);

  const sun = new THREE.DirectionalLight(0xfff0d6, 3.1);
  sun.position.copy(SUN_DIR).multiplyScalar(120).add(new THREE.Vector3(2, 28, 0));
  sun.target.position.set(2, 28, 0);
  group.add(sun, sun.target);
  if (quality.shadows) {
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    const c = sun.shadow.camera;
    c.left = -34; c.right = 34; c.top = 34; c.bottom = -34; c.near = 40; c.far = 220;
    sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.05; sun.shadow.radius = 3;
  }
  const hemi = new THREE.HemisphereLight(0xcfe3ff, 0x6f6a48, 0.9);
  group.add(hemi);
  const fill = new THREE.DirectionalLight(0xdfe9ff, 0.55);
  fill.position.set(30, 20, 60);
  group.add(fill);

  const groundTex = canvasTexture(groundCanvas(tier === 'high' ? 1024 : 512), { repeat: 36, anisotropy: 8 });
  const ground = new THREE.Mesh(new THREE.CircleGeometry(900, 64), new THREE.MeshStandardMaterial({ map: groundTex, roughness: 1, color: 0xd8d2c0 }));
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  group.add(ground);
  const contact = makeContactShadow({ width: 34, depth: 34, y: 0.05, opacity: 0.5, radius: 0.3 });
  group.add(contact);

  const far = canvasTexture(bokehCanvas(2048, 512, 21, { top: 0.25, highlights: 60 }), { anisotropy: 2 });
  far.wrapS = THREE.RepeatWrapping; far.repeat.x = 3;
  const farRing = new THREE.Mesh(new THREE.CylinderGeometry(620, 620, 300, 48, 1, true), new THREE.MeshBasicMaterial({ map: far, transparent: true, side: THREE.BackSide, depthWrite: false, fog: false, color: 0xc4d2c0 }));
  farRing.position.y = 110;
  farRing.renderOrder = -10;
  group.add(farRing);

  const midTex = canvasTexture(bokehCanvas(1024, 512, 44, { top: 0.15, highlights: 50, fadeBottom: true, fadeSides: true, greens: ['rgba(70,104,52,A)', 'rgba(96,126,64,A)', 'rgba(56,86,44,A)', 'rgba(124,140,82,A)'] }), { anisotropy: 2 });
  const midMat = new THREE.MeshBasicMaterial({ map: midTex, transparent: true, depthWrite: false, fog: true, side: THREE.DoubleSide });
  const cards = tier === 'low' ? 7 : 12;
  for (let i = 0; i < cards; i++) {
    const a = (i / cards) * Math.PI * 2 + rand() * 0.3;
    const r = 170 + rand() * 120;
    const w = 150 + rand() * 120; const h = w * 0.5;
    const card = new THREE.Mesh(new THREE.PlaneGeometry(w, h), midMat);
    card.position.set(Math.cos(a) * r, h * 0.42, Math.sin(a) * r);
    card.lookAt(0, h * 0.42, 0);
    card.renderOrder = -5;
    group.add(card);
  }

  const bladeCount = tier === 'low' ? 260 : tier === 'medium' ? 900 : 1800;
  const blade = new THREE.PlaneGeometry(0.5, 1, 1, 4);
  blade.translate(0, 0.5, 0);
  const bp = blade.attributes.position;
  for (let i = 0; i < bp.count; i++) {
    const y = bp.getY(i);
    bp.setX(i, bp.getX(i) * (1 - y * 0.92));
    bp.setZ(i, y * y * 0.35);
  }
  blade.computeVertexNormals();
  const time = { value: 0 };
  const grassMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.85, side: THREE.DoubleSide });
  patchMaterial(grassMat, {
    uniforms: { uTime: time }, translucency: 0.4, transTint: 0xd0e080,
    vertDecl: 'uniform float uTime;\n',
    vertBegin: '#include <begin_vertex>\n#ifdef USE_INSTANCING\n vec3 ip = vec3(instanceMatrix[3][0], instanceMatrix[3][1], instanceMatrix[3][2]);\n float sw = sin(uTime * 1.6 + ip.x * 0.08 + ip.z * 0.05) * 0.12 + sin(uTime * 3.7 + ip.z * 0.3) * 0.03;\n transformed.z += sw * position.y * position.y;\n#endif',
    key: 'grass',
  });
  const grass = new THREE.InstancedMesh(blade, grassMat, bladeCount);
  const m = new THREE.Matrix4(); const q = new THREE.Quaternion(); const s = new THREE.Vector3(); const p = new THREE.Vector3(); const e = new THREE.Euler(); const c = new THREE.Color();
  for (let i = 0; i < bladeCount; i++) {
    let r = 4 + Math.pow(rand(), 1.3) * 140;
    let a = rand() * Math.PI * 2;
    if (rand() < 0.5) {
      const ci = (rand() * 14) | 0; const ca = ci * 2.4; const cr = 8 + (ci * 37 % 60);
      a = ca + (rand() - 0.5) * 0.25; r = cr + (rand() - 0.5) * 6;
    }
    p.set(Math.cos(a) * r, 0, Math.sin(a) * r);
    e.set((rand() - 0.5) * 0.5, rand() * Math.PI * 2, (rand() - 0.5) * 0.5);
    q.setFromEuler(e);
    const h = 4 + rand() * 9;
    s.set(0.6 + rand() * 0.6, h, 1);
    m.compose(p, q, s);
    grass.setMatrixAt(i, m);
    const dry = rand();
    c.setRGB(0.42 + dry * 0.35, 0.55 + dry * 0.12, 0.2 + dry * 0.1);
    grass.setColorAt(i, c);
  }
  grass.receiveShadow = true;
  group.add(grass);

  const pebbleGeo = new THREE.IcosahedronGeometry(1, 1);
  const pebbles = new THREE.InstancedMesh(pebbleGeo, new THREE.MeshStandardMaterial({ color: 0x9a8f7c, roughness: 0.9, flatShading: true }), 26);
  for (let i = 0; i < 26; i++) {
    const a = rand() * Math.PI * 2; const r = 3 + rand() * 22;
    p.set(Math.cos(a) * r, 0, Math.sin(a) * r);
    q.setFromEuler(e.set(rand() * 3, rand() * 3, rand() * 3));
    const k = 0.4 + rand() * 1.4;
    s.set(k, k * 0.5, k * (0.7 + rand() * 0.5));
    m.compose(p, q, s);
    pebbles.setMatrixAt(i, m);
  }
  pebbles.receiveShadow = true; pebbles.castShadow = quality.shadows;
  group.add(pebbles);

  const moteN = tier === 'low' ? 24 : 60;
  const motePos = new Float32Array(moteN * 3); const moteSeed = new Float32Array(moteN * 3);
  for (let i = 0; i < moteN; i++) {
    moteSeed[i * 3] = (rand() - 0.5) * 60; moteSeed[i * 3 + 1] = 10 + rand() * 45; moteSeed[i * 3 + 2] = (rand() - 0.5) * 50;
  }
  const moteGeo = new THREE.BufferGeometry();
  moteGeo.setAttribute('position', new THREE.BufferAttribute(motePos, 3));
  const motes = new THREE.Points(moteGeo, new THREE.PointsMaterial({ size: 0.22, map: getSoftDotTexture(), transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending, color: 0xfff1c8 }));
  motes.frustumCulled = false;
  motes.material.userData.sharedFx = true;
  group.add(motes);

  return {
    group, sun, hemi,
    update(t) {
      time.value = t;
      for (let i = 0; i < moteN; i++) {
        motePos[i * 3] = moteSeed[i * 3] + Math.sin(t * 0.13 + i) * 4;
        motePos[i * 3 + 1] = moteSeed[i * 3 + 1] + Math.sin(t * 0.21 + i * 2.1) * 2.5;
        motePos[i * 3 + 2] = moteSeed[i * 3 + 2] + Math.cos(t * 0.11 + i * 1.3) * 4;
      }
      moteGeo.attributes.position.needsUpdate = true;
    },
    dispose() {
      env.dispose();
      motes.material.dispose();
    },
  };
}
