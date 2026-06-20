import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard, hideInfoCard } from '../core/sim-ui.js';

// Body layers, outside -> inside. Each part has a 3D representation + a real description.
const LAYERS = ['skin', 'muscle', 'skeleton', 'organs'];
const LAYER_LABEL = { skin: 'Skin', muscle: 'Muscles', skeleton: 'Skeleton', organs: 'Organs' };

const ORGANS = [
  {
    id: 'brain', name: 'Brain', color: 0xf2b3c5,
    pos: [0, 4.2, 0],
    info: 'Your control centre. The brain processes your senses, stores memories, and sends the signals that move every muscle. Wrapped safely in the skull, it uses about 20% of your energy even though it is only 2% of your weight.',
  },
  {
    id: 'heart', name: 'Heart', color: 0xc0392b,
    pos: [0.16, 1.56, 0.34],
    info: 'A muscular pump the size of your fist. It beats around 100,000 times a day, pushing blood through a network of vessels that would wrap around the Earth more than twice.',
  },
  {
    id: 'lungs', name: 'Lungs', color: 0xe08aa8,
    pos: [-0.48, 1.92, 0.12], second: [0.48, 1.92, 0.12],
    info: 'Your breathing organs. They take in the oxygen every cell needs and breathe out waste carbon dioxide. Unfolded, their air sacs would cover about half a tennis court.',
  },
  {
    id: 'liver', name: 'Liver', color: 0x7c3a23,
    pos: [0.34, 0.58, 0.26],
    info: 'The body\'s chemical factory. The liver cleans the blood, stores energy, and helps turn food into fuel. It does over 500 different jobs — the busiest organ you have.',
  },
  {
    id: 'stomach', name: 'Stomach', color: 0xd98b5f,
    pos: [-0.43, 0.38, 0.34],
    info: 'A stretchy muscular bag that churns food into a soup with strong acid and squeezing waves. The soup then flows into the intestines, where the goodness is absorbed.',
  },
  {
    id: 'intestines', name: 'Intestines', color: 0xc9a86b,
    pos: [0, -0.78, 0.30],
    info: 'A long coiled tube — about 7 metres if stretched out. The small intestine soaks up nutrients from food; the large intestine reclaims water and packs up what is left.',
  },
];

const MUSCLE_INFO = 'Red ropes that can only pull, never push. Over 600 of them work in opposing pairs across your joints to move you. To bend the elbow, the biceps pulls; to straighten it, the triceps takes its turn.';
const SKELETON_INFO = 'Your frame of 206 bones. It holds you upright, protects soft organs like the brain and heart, and works with muscles as levers to let you move. Bone is living tissue — it rebuilds itself constantly.';
const SKIN_INFO = 'Your body\'s largest organ and its waterproof suit. Skin keeps water in, germs out, and lets you feel the world through millions of nerve endings. It also cools you by sweating.';

export default function init(stage) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(16, quality.segments / 2);

  camera.position.set(0, 1.5, 12);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 22, enablePan: false, maxPolar: Math.PI * 0.62, minPolar: Math.PI * 0.18,
  });
  controls.setTarget(new THREE.Vector3(0, 1, 0));

  // Soft studio background + warm key light
  scene.background = new THREE.Color(0x0e1424);
  scene.fog = new THREE.Fog(0x0e1424, 18, 36);
  basicLights(scene, { key: 1.7, ambient: 0.5 });
  const rim = new THREE.DirectionalLight(0x88aaff, 0.6); rim.position.set(-6, 3, -8); scene.add(rim);

  // Ground shadow disk
  const groundGeo = new THREE.CircleGeometry(7, 48);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a2336, roughness: 0.95 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2; ground.position.y = -3.4; ground.receiveShadow = true;
  scene.add(ground);

  const root = new THREE.Group();
  scene.add(root);

  // ---- Build a stylised human figure ----
  const skinMat = new THREE.MeshStandardMaterial({ color: 0xe7a982, roughness: 0.7, transparent: true, opacity: 0.42 });
  const muscleMat = new THREE.MeshStandardMaterial({ color: 0xb13a3a, roughness: 0.55, transparent: true, opacity: 0.88 });
  const boneMat = new THREE.MeshStandardMaterial({ color: 0xf2ede0, roughness: 0.5 });

  // Skin shell: head + torso + limbs (capsules approximated with stretched spheres)
  const skin = new THREE.Group();
  function part(mat, geo, x, y, z) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; return m; }
  const sR = 0.95; // sphere radius unit
  skin.add(part(skinMat, new THREE.SphereGeometry(sR, seg, seg), 0, 4.2, 0));                 // head
  const torsoGeo = new THREE.SphereGeometry(1.35, seg, seg); torsoGeo.scale(1, 1.45, 0.72);
  skin.add(part(skinMat, torsoGeo, 0, 1.6, 0));                                                // torso
  const upperArmGeo = new THREE.SphereGeometry(0.45, seg, seg); upperArmGeo.scale(1, 2.3, 1);
  const foreArmGeo = new THREE.SphereGeometry(0.38, seg, seg); foreArmGeo.scale(1, 2.0, 1);
  skin.add(part(skinMat, upperArmGeo, 1.55, 1.9, 0)); skin.add(part(skinMat, upperArmGeo, -1.55, 1.9, 0));
  skin.add(part(skinMat, foreArmGeo, 1.7, -0.5, 0)); skin.add(part(skinMat, foreArmGeo, -1.7, -0.5, 0));
  const thighGeo = new THREE.SphereGeometry(0.55, seg, seg); thighGeo.scale(1, 2.4, 1);
  const shinGeo = new THREE.SphereGeometry(0.45, seg, seg); shinGeo.scale(1, 2.2, 1);
  skin.add(part(skinMat, thighGeo, 0.55, -0.8, 0)); skin.add(part(skinMat, thighGeo, -0.55, -0.8, 0));
  skin.add(part(skinMat, shinGeo, 0.55, -3.0, 0)); skin.add(part(skinMat, shinGeo, -0.55, -3.0, 0));

  // Muscles: simplified red ropes (arms, legs, torso core)
  const muscle = new THREE.Group();
  const muRope = (geo, x, y, z) => { const m = new THREE.Mesh(geo, muscleMat); m.position.set(x, y, z); m.castShadow = true; muscle.add(m); };
  const armGeo = new THREE.CapsuleGeometry(0.32, 1.5, 8, 16);
  muRope(armGeo, 1.55, 1.9, 0); muRope(armGeo.clone(), -1.55, 1.9, 0);
  muRope(new THREE.CapsuleGeometry(0.26, 1.2, 8, 16), 1.7, -0.5, 0); muRope(new THREE.CapsuleGeometry(0.26, 1.2, 8, 16), -1.7, -0.5, 0);
  const legGeo = new THREE.CapsuleGeometry(0.4, 1.7, 8, 16);
  muRope(legGeo, 0.55, -0.8, 0); muRope(legGeo.clone(), -0.55, -0.8, 0);
  muRope(new THREE.CapsuleGeometry(0.32, 1.4, 8, 16), 0.55, -3.0, 0); muRope(new THREE.CapsuleGeometry(0.32, 1.4, 8, 16), -0.55, -3.0, 0);
  const torsoMuGeo = new THREE.SphereGeometry(1.1, seg, seg); torsoMuGeo.scale(1, 1.4, 0.6);
  muRope(torsoMuGeo, 0, 1.6, 0);

  // Skeleton: skull + spine + ribcage + pelvis + long bones
  const skeleton = new THREE.Group();
  const bone = (geo, x, y, z, mat = boneMat) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; skeleton.add(m); return m; };
  bone(new THREE.SphereGeometry(0.85, seg, seg), 0, 4.2, 0);                                       // skull
  bone(new THREE.CylinderGeometry(0.16, 0.18, 4.4, 12), 0, 1.6, -0.1);                            // spine
  // ribcage: a set of torus arcs
  for (let i = 0; i < 7; i++) {
    const rib = new THREE.Mesh(new THREE.TorusGeometry(0.95 - i * 0.02, 0.05, 8, 24, Math.PI * 1.1), boneMat);
    rib.position.set(0, 2.7 - i * 0.32, 0); rib.rotation.x = Math.PI / 2; rib.rotation.z = -Math.PI * 0.55;
    rib.castShadow = true; skeleton.add(rib);
  }
  const pelvisGeo = new THREE.SphereGeometry(0.8, seg, seg); pelvisGeo.scale(1.3, 0.55, 0.8);
  bone(pelvisGeo, 0, -0.5, 0);
  // limb bones
  const longBone = (l) => new THREE.CylinderGeometry(0.13, 0.13, l, 10);
  bone(longBone(1.8), 1.55, 1.9, 0); bone(longBone(1.8), -1.55, 1.9, 0);     // humerus
  bone(longBone(1.7), 1.7, -0.5, 0); bone(longBone(1.7), -1.7, -0.5, 0);     // radius/ulna
  bone(longBone(2.1), 0.55, -0.8, 0); bone(longBone(2.1), -0.55, -0.8, 0);   // femur
  bone(longBone(2.0), 0.55, -3.0, 0); bone(longBone(2.0), -0.55, -3.0, 0);   // tibia/fibula

  // Organs: built as anatomical groups rather than colored blobs. Each visible mesh is raycastable.
  const organs = new THREE.Group();
  const organMeshes = [];
  function organMat(o, rough = 0.55) {
    const m = new THREE.MeshStandardMaterial({ color: o.color, roughness: rough, metalness: 0.03 });
    m.emissive = new THREE.Color(o.color);
    m.emissiveIntensity = 0;
    return m;
  }
  function addOrganMesh(mesh, o) { mesh.castShadow = true; mesh.receiveShadow = true; mesh.userData.organ = o; organs.add(mesh); organMeshes.push(mesh); return mesh; }
  function ellipsoid(o, rx, ry, rz, x, y, z, material = organMat(o), detail = seg) {
    const geo = new THREE.SphereGeometry(1, detail, Math.max(12, Math.floor(detail / 2)));
    geo.scale(rx, ry, rz);
    const mesh = new THREE.Mesh(geo, material);
    mesh.position.set(x, y, z);
    return addOrganMesh(mesh, o);
  }
  function cylBetween(o, a, b, r, material = organMat(o), radial = 12) {
    const va = new THREE.Vector3(...a); const vb = new THREE.Vector3(...b);
    const mid = va.clone().add(vb).multiplyScalar(0.5);
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(r, r, va.distanceTo(vb), radial), material);
    mesh.position.copy(mid);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), vb.clone().sub(va).normalize());
    return addOrganMesh(mesh, o);
  }
  function tubeOrgan(o, pts, r, material = organMat(o), tubularSeg = 48) {
    const curve = new THREE.CatmullRomCurve3(pts.map((v) => new THREE.Vector3(...v)));
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, tubularSeg, r, 8, false), material);
    return addOrganMesh(mesh, o);
  }
  ORGANS.forEach((o) => {
    const m = organMat(o);
    if (o.id === 'brain') {
      ellipsoid(o, 0.42, 0.30, 0.34, -0.22, 4.22, 0.02, m);
      ellipsoid(o, 0.42, 0.30, 0.34, 0.22, 4.22, 0.02, m);
      ellipsoid(o, 0.22, 0.15, 0.18, 0.00, 4.00, -0.10, organMat(o, 0.7), 24);
      for (let i = -3; i <= 3; i++) {
        const ridge = tubeOrgan(o, [[i * 0.08, 4.34, 0.28], [i * 0.10, 4.24, 0.35], [i * 0.08, 4.12, 0.25]], 0.009, new THREE.MeshStandardMaterial({ color: 0xd987a6, roughness: 0.8 }), 12);
        ridge.userData.organ = o;
      }
    } else if (o.id === 'lungs') {
      const lm = organMat(o, 0.66);
      ellipsoid(o, 0.34, 0.78, 0.26, o.pos[0], o.pos[1], o.pos[2], lm);
      ellipsoid(o, 0.34, 0.78, 0.26, o.second[0], o.second[1], o.second[2], lm);
      const trachea = new THREE.MeshStandardMaterial({ color: 0xf3e7d7, roughness: 0.58 });
      cylBetween(o, [0, 2.98, 0.06], [0, 2.12, 0.08], 0.055, trachea, 16);
      cylBetween(o, [0, 2.14, 0.08], [-0.36, 1.88, 0.10], 0.035, trachea, 12);
      cylBetween(o, [0, 2.14, 0.08], [0.36, 1.88, 0.10], 0.035, trachea, 12);
    } else if (o.id === 'heart') {
      const hm = organMat(o, 0.42);
      ellipsoid(o, 0.28, 0.34, 0.24, o.pos[0] - 0.09, o.pos[1] + 0.05, o.pos[2], hm);
      ellipsoid(o, 0.26, 0.32, 0.24, o.pos[0] + 0.12, o.pos[1] + 0.02, o.pos[2], hm);
      const apex = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.42, 24), hm);
      apex.position.set(o.pos[0] + 0.04, o.pos[1] - 0.35, o.pos[2]); apex.rotation.x = Math.PI; addOrganMesh(apex, o);
      cylBetween(o, [o.pos[0], o.pos[1] + 0.34, o.pos[2]], [o.pos[0] - 0.04, o.pos[1] + 0.72, o.pos[2]], 0.055, new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.48 }), 16);
      cylBetween(o, [o.pos[0] + 0.15, o.pos[1] + 0.28, o.pos[2]], [o.pos[0] + 0.40, o.pos[1] + 0.55, o.pos[2] + 0.02], 0.045, new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.48 }), 16);
    } else if (o.id === 'liver') {
      const mesh = ellipsoid(o, 0.72, 0.28, 0.34, o.pos[0], o.pos[1], o.pos[2], organMat(o, 0.62));
      mesh.rotation.z = -0.10;
      ellipsoid(o, 0.14, 0.09, 0.09, o.pos[0] - 0.36, o.pos[1] - 0.03, o.pos[2] + 0.20, new THREE.MeshStandardMaterial({ color: 0x236b38, roughness: 0.62 }), 16);
    } else if (o.id === 'stomach') {
      const st = ellipsoid(o, 0.30, 0.46, 0.22, o.pos[0], o.pos[1], o.pos[2], organMat(o, 0.55));
      st.rotation.z = -0.45;
      tubeOrgan(o, [[o.pos[0] + .12, o.pos[1] + .30, o.pos[2]], [o.pos[0] + .32, o.pos[1] + .12, o.pos[2]], [o.pos[0] + .18, o.pos[1] - .25, o.pos[2]]], .055, organMat(o, 0.58), 28);
    } else if (o.id === 'intestines') {
      const im = organMat(o, 0.78);
      for (let row = 0; row < 4; row++) {
        tubeOrgan(o, [[-0.50, -0.47 - row * 0.18, o.pos[2]], [-0.20, -0.58 - row * 0.18, o.pos[2]], [0.20, -0.44 - row * 0.18, o.pos[2]], [0.50, -0.56 - row * 0.18, o.pos[2]]], 0.055, im, 28);
      }
      const colon = tubeOrgan(o, [[-0.66, -0.36, o.pos[2] - .02], [-0.70, -1.20, o.pos[2] - .02], [0.70, -1.20, o.pos[2] - .02], [0.66, -0.36, o.pos[2] - .02]], 0.080, new THREE.MeshStandardMaterial({ color: 0xb99054, roughness: 0.76 }), 52);
      colon.userData.organ = o;
    }
  });

  root.add(skin); root.add(muscle); root.add(skeleton); root.add(organs);

  // Labels (sprites) for organs, shown only on organs layer
  const labels = ORGANS.map((o) => {
    const s = makeLabelSprite(o.name, { scale: 0.6, fontSize: 34 });
    s.position.set(o.pos[0], o.pos[1] + (o.id === 'brain' ? 0.95 : 0.75), o.pos[2]);
    s.visible = false; organs.add(s); return s;
  });

  // ---- Layer visibility ----
  let currentLayer = 'organs';
  function setLayer(layer) {
    currentLayer = layer;
    const idx = LAYERS.indexOf(layer);
    // skin: visible only if it's the outermost shown
    skin.visible = idx >= LAYERS.indexOf('skin') && false; // skin shown faintly always until we go deeper
    // Actually show layers cumulatively-fading: show skin only when skin selected
    skin.visible = (layer === 'skin');
    muscle.visible = (layer === 'muscle');
    skeleton.visible = (layer === 'skeleton' || layer === 'organs');
    organs.visible = (layer === 'organs');
    labels.forEach((l) => { l.visible = (layer === 'organs'); });
    // Make skin translucent overlay when deeper layers shown, to keep context
    if (layer !== 'skin') {
      skin.visible = true;
      skinMat.opacity = layer === 'muscle' ? 0.10 : 0.05;
    } else {
      skinMat.opacity = 0.55;
    }
    layerBadge.set(LAYER_LABEL[layer]);
    layerBadge.el.style.setProperty('--ix-hud-color', '#84CC16');
  }

  const hud = createHud(stage);
  const layerBadge = hud.badge('Organs', '#84CC16');
  const partBadge = hud.badge('Tap an organ!', '#a3e635');

  // Pulse highlight on hovered/selected organ
  let selected = null;
  function highlight(o) {
    organMeshes.forEach((m) => { m.material.emissiveIntensity = 0.0; });
    if (o) { o.material.emissiveIntensity = 0.35; }
  }

  // Raycast for organ taps
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let downPos = null;
  function onDown(e) { downPos = { x: e.clientX, y: e.clientY }; }
  function onUp(e) {
    if (!downPos || Math.hypot(e.clientX - downPos.x, e.clientY - downPos.y) > 8) return;
    if (currentLayer !== 'organs') {
      const info = currentLayer === 'skin' ? SKIN_INFO : currentLayer === 'muscle' ? MUSCLE_INFO : SKELETON_INFO;
      showInfoCard(stage, { title: LAYER_LABEL[currentLayer], body: info, color: '#84CC16' });
      return;
    }
    const rect = engine.canvas.getBoundingClientRect();
    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(organMeshes, false);
    if (hits.length) {
      const o = hits[0].object; const data = o.userData.organ;
      selected = o; highlight(o);
      partBadge.set(data.name);
      showInfoCard(stage, { title: data.name, body: data.info, color: '#84CC16' });
    }
  }
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);

  // ---- Panel ----
  const panel = createPanel(stage, { title: 'Human Body Explorer' });
  panel.info('Drag the body to rotate. Use the slider to peel back the layers, then tap any organ to learn its job.');
  const slider = panel.slider({
    label: 'Body layer', min: 0, max: LAYERS.length - 1, step: 1, value: LAYERS.indexOf(currentLayer),
    format: (v) => LAYER_LABEL[LAYERS[v]],
    onChange: (v) => { setLayer(LAYERS[v]); selected = null; highlight(null); partBadge.set('Tap an organ!'); hideInfoCard(stage); },
  });
  panel.divider();
  panel.readout({ label: 'Bones', value: '206' });
  panel.readout({ label: 'Muscles', value: '600+' });
  panel.readout({ label: 'Heart beats/day', value: '~100,000' });
  panel.toggle({ label: 'Slow spin', value: true, onChange: (v) => { spin = v; } });

  let spin = true;
  setLayer('organs');

  engine.setUpdate((dt) => {
    if (spin) root.rotation.y += dt * 0.18;
    // gentle breathing on organs
    const t = performance.now() * 0.001;
    organs.scale.setScalar(1 + Math.sin(t * 1.2) * 0.012);
    if (selected) selected.material.emissiveIntensity = 0.25 + Math.sin(t * 4) * 0.12;
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown);
      engine.canvas.removeEventListener('pointerup', onUp);
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
