import { THREE } from '../../core/engine.js';
import { canvasTexture, patchMaterial, paintVertices, texSize } from './kit.js';
import { chrysalisCanvases } from './textures.js';

export const STAGES = [
  {
    id: 'egg', name: 'Egg', color: '#fde68a', duration: '3–4 days', days: 'day 0–4', size: '≈1.2 mm tall',
    food: 'yolk stored inside the egg', process: 'embryo grows inside the ribbed shell (chorion)',
    info: 'The mother plain tiger glues each egg on its own to the underside of a young aak (Calotropis) leaf, hidden from sun and rain. The pearly shell is ribbed and has a tiny opening at the top, the micropyle, where sperm entered and air still gets in. Inside, an embryo turns yolk into a caterpillar in 3–4 days.',
  },
  {
    id: 'caterpillar', name: 'Caterpillar', color: '#86efac', duration: '10–14 days (5 instars)', days: 'day 4–18', size: '2 mm → 4.5 cm',
    food: 'aak leaves, poisonous milky latex and all', process: 'eats non-stop and moults its skin 4 times',
    info: 'The larva first eats its own eggshell, then the leaf. It grips with three pairs of true legs and ten stubby prolegs, and crawls by sending a wave of muscle contraction from tail to head. Its bold bands warn birds that it tastes bad: it stores poison from the aak plant’s milky sap. The three pairs of black filaments are sensory, not stings.',
  },
  {
    id: 'chrysalis', name: 'Chrysalis', color: '#a7f3d0', duration: '8–12 days', days: 'day 18–30', size: '≈1.8 cm long',
    food: 'none — runs on stored fat', process: 'body is broken down and rebuilt from imaginal discs',
    info: 'The full-grown caterpillar spins a silk pad under a twig, hooks its tail (the cremaster) into it, hangs in a J and sheds its skin one last time to reveal a jade-green pupa dotted with gold. Inside, enzymes dissolve most larval tissue and clusters of cells called imaginal discs build wings, legs, eyes and antennae. The day before emergence the case turns clear and the orange wings show through.',
  },
  {
    id: 'adult', name: 'Adult butterfly', color: '#fdba74', duration: '2–4 weeks', days: 'day 30 onward', size: 'wingspan 7–8 cm',
    food: 'nectar, sipped through a coiled proboscis', process: 'mates and lays eggs on aak plants',
    info: 'The adult splits the case, hangs from it and pumps blood (haemolymph) into its soft crumpled wings until they are full size, then waits about an hour for them to harden. It can no longer chew: it uncoils a long tube, the proboscis, to sip nectar. Like all brush-footed butterflies it stands on only four legs; the front pair is tiny and folded against the chest.',
  },
];

export function buildEgg(opts) {
  const seg = opts.tier === 'low' ? 40 : 80;
  const pts = [];
  for (let i = 0; i <= 24; i++) {
    const t = i / 24;
    const y = t * 1.2;
    const r = 0.42 * Math.pow(Math.sin(Math.PI * 0.5 * (1 - Math.pow(t, 1.7))), 0.55) + (t < 0.05 ? 0.02 : 0);
    pts.push(new THREE.Vector2(Math.max(0.0005, r), y));
  }
  const geo = new THREE.LatheGeometry(pts, seg);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i); const z = p.getZ(i); const y = p.getY(i);
    const a = Math.atan2(z, x);
    const rib = Math.pow(Math.abs(Math.cos(a * 10)), 3);
    const cross = Math.sin(y * 48) * 0.012;
    const top = Math.max(0, 1 - y / 1.05);
    const k = 1 + (rib * 0.11 + cross) * top;
    p.setX(i, x * k); p.setZ(i, z * k);
  }
  geo.computeVertexNormals();
  paintVertices(geo, (x, y, z, c) => c.set(0xe2dcc6).lerp(new THREE.Color(0xe9dcc0), Math.max(0, y - 0.9) * 2.5));
  geo.scale(0.1, 0.1, 0.1);
  const mat = new THREE.MeshPhysicalMaterial({
    vertexColors: true, roughness: 0.34, clearcoat: 0.8, clearcoatRoughness: 0.2,
    sheen: 0.35, sheenColor: new THREE.Color(0xfff6e6), iridescence: opts.tier === 'high' ? 0.35 : 0, iridescenceIOR: 1.4,
    transparent: true, opacity: 1,
  });
  const egg = new THREE.Mesh(geo, mat);
  const larva = new THREE.Mesh(new THREE.SphereGeometry(0.028, 12, 10), new THREE.MeshStandardMaterial({ color: 0x1a1a14, roughness: 0.6 }));
  larva.position.y = 0.09;
  larva.visible = false;
  const group = new THREE.Group();
  group.add(egg, larva);
  const glue = new THREE.Mesh(new THREE.CircleGeometry(0.055, 16), new THREE.MeshStandardMaterial({ color: 0xe8e2c8, roughness: 0.3, transparent: true, opacity: 0.6 }));
  glue.rotation.x = -Math.PI / 2; glue.position.y = 0.002;
  group.add(glue);
  return {
    group,
    setDevelop(k) {
      mat.color.setRGB(1 - k * 0.12, 1 - k * 0.14, 1 - k * 0.2);
      mat.opacity = 1 - k * 0.25;
      larva.visible = k > 0.3;
      larva.scale.setScalar(0.6 + k * 0.6);
    },
    setHatched(k) {
      egg.scale.set(1, 1 - k * 0.55, 1);
      larva.visible = k < 0.5 && larva.visible;
    },
  };
}

export function buildChrysalis(opts) {
  const seg = opts.tier === 'low' ? 24 : 48;
  const prof = [[0.0, -1.8], [0.16, -1.76], [0.34, -1.62], [0.46, -1.42], [0.52, -1.12], [0.5, -0.8], [0.47, -0.55], [0.5, -0.45], [0.47, -0.38], [0.38, -0.22], [0.2, -0.1], [0.05, -0.02]];
  const pts = prof.map(([r, y]) => new THREE.Vector2(r, y));
  const geo = new THREE.LatheGeometry(pts, seg);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const z = p.getZ(i); const y = p.getY(i);
    if (z > 0) p.setZ(i, z * (1 + 0.12 * Math.sin(Math.PI * Math.min(1, Math.max(0, (-y - 0.5) / 1.1)))));
  }
  geo.computeVertexNormals();
  const W = texSize(opts.tier, 512);
  const cv = chrysalisCanvases(W);
  const young = canvasTexture(cv.young);
  const mature = canvasTexture(cv.mature);
  const metal = canvasTexture(cv.metal, { color: false });
  const uMature = { value: 0 };
  const uEmpty = { value: 0 };
  const mat = new THREE.MeshPhysicalMaterial({
    map: young, metalnessMap: metal, metalness: 1, roughness: 0.22,
    clearcoat: 1, clearcoatRoughness: 0.08, sheen: 0.3, sheenColor: new THREE.Color(0xd8ffe0),
    transparent: true,
  });
  patchMaterial(mat, {
    uniforms: { matureMap: { value: mature }, uMature, uEmpty },
    translucency: 0.5, transTint: 0xbaf5c0,
    fragDecl: 'uniform sampler2D matureMap;\nuniform float uMature;\nuniform float uEmpty;\n',
    fragMap: '#ifdef USE_MAP\n vec4 cy = texture2D( map, vMapUv ); vec4 cm = texture2D( matureMap, vMapUv );\n vec4 cc = mix(cy, cm, uMature);\n cc.rgb = mix(cc.rgb, vec3(0.86, 0.84, 0.74), uEmpty);\n diffuseColor *= cc;\n diffuseColor.a *= mix(1.0, 0.55, uEmpty);\n#endif',
    key: 'chrysalis',
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.castShadow = true;
  const cremaster = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.05, 0.24, 8), new THREE.MeshStandardMaterial({ color: 0x1a1612, roughness: 0.5 }));
  cremaster.position.y = 0.1;
  const pad = new THREE.Mesh(new THREE.SphereGeometry(0.13, 14, 8), new THREE.MeshPhysicalMaterial({ color: 0xf4f2ec, roughness: 0.9, sheen: 1, sheenColor: new THREE.Color(0xffffff) }));
  pad.scale.set(1.2, 0.4, 1.0);
  pad.position.y = 0.2;
  const swing = new THREE.Group();
  swing.add(mesh, cremaster);
  const group = new THREE.Group();
  group.add(pad, swing);
  return {
    group, swing, mesh, material: mat,
    setMature(k) { uMature.value = k; mat.roughness = 0.22 + k * 0.1; },
    setEmpty(k) { uEmpty.value = k; mat.metalness = 1 - k; mat.clearcoat = 1 - k * 0.6; },
    textures: [mature],
    dispose() { mature.dispose(); },
  };
}
