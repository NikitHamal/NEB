import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

// 3D plant explorer for kids — roots, stem, leaf, flower
// Click each part to learn its job

const PARTS = {
  root: {
    label: 'Roots',
    color: '#a16207',
    info: 'Roots anchor the plant in the soil and soak up water and minerals. They also store food. Tiny root hairs make the roots much better at absorbing water — like a giant sponge underground!',
  },
  stem: {
    label: 'Stem',
    color: '#65a30d',
    info: 'The stem holds the plant upright like a skeleton. It carries water and minerals UP from the roots to the leaves, and carries sugary food DOWN from the leaves to the rest of the plant through special tubes.',
  },
  leaf: {
    label: 'Leaves',
    color: '#22c55e',
    info: 'Leaves are the plant\'s food factories! They use sunlight, water, and carbon dioxide from the air to make sugar (food) in a process called photosynthesis. The green colour comes from a pigment called chlorophyll.',
  },
  flower: {
    label: 'Flower',
    color: '#f9a8d4',
    info: 'Flowers attract insects and birds with their bright colours and sweet nectar. When pollen moves from one flower to another (pollination), seeds can form — and seeds grow into new plants!',
  },
};

export default function init(stage) {
  const engine = createEngine(stage, { fov: 45 });
  if (!engine) return { dispose() {} };
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 3, 10);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 4, maxDistance: 20 });
  basicLights(scene, { ambient: 0.7, key: 1.3 });
  scene.background = new THREE.Color(0x071c10);

  const meshMap = new Map();

  // Soil
  const soil = new THREE.Mesh(
    new THREE.CylinderGeometry(2.5, 2.5, 0.4, Math.max(8, seg / 4)),
    new THREE.MeshStandardMaterial({ color: 0x6b3f1a, roughness: 1 })
  );
  soil.position.y = -2.2;
  scene.add(soil);

  // Roots
  const rootGroup = new THREE.Group();
  rootGroup.position.y = -2.0;
  for (let i = 0; i < 5; i++) {
    const angle = (i / 5) * Math.PI * 2;
    const rootMesh = new THREE.Mesh(
      new THREE.CylinderGeometry(0.06, 0.02, 1.4, Math.max(4, seg / 8)),
      new THREE.MeshStandardMaterial({ color: 0xa16207, roughness: 1 })
    );
    rootMesh.rotation.z = Math.cos(angle) * 0.7;
    rootMesh.rotation.x = Math.sin(angle) * 0.7;
    rootMesh.position.set(Math.cos(angle) * 0.5, -0.4, Math.sin(angle) * 0.5);
    rootGroup.add(rootMesh);
  }
  scene.add(rootGroup);
  meshMap.set('root', rootGroup);
  const rootLabel = makeLabelSprite('Roots', { scale: 1.4 });
  rootLabel.position.set(1.5, -2.5, 0);
  scene.add(rootLabel);

  // Stem
  const stemMesh = new THREE.Mesh(
    new THREE.CylinderGeometry(0.15, 0.2, 5, Math.max(6, seg / 4)),
    new THREE.MeshStandardMaterial({ color: 0x65a30d, roughness: 0.9 })
  );
  stemMesh.position.y = 0.5;
  scene.add(stemMesh);
  meshMap.set('stem', stemMesh);
  const stemLabel = makeLabelSprite('Stem', { scale: 1.4 });
  stemLabel.position.set(1.2, 0.5, 0);
  scene.add(stemLabel);

  // Leaves
  const leafGroup = new THREE.Group();
  for (let i = 0; i < 4; i++) {
    const angle = (i / 4) * Math.PI * 2;
    const leafGeo = new THREE.SphereGeometry(0.6, Math.max(4, seg / 6), Math.max(4, seg / 6));
    const leafMesh = new THREE.Mesh(
      leafGeo,
      new THREE.MeshStandardMaterial({ color: 0x22c55e, roughness: 0.8, side: THREE.DoubleSide })
    );
    leafMesh.scale.z = 0.2;
    leafMesh.position.set(Math.cos(angle) * 1.2, 1.0 + i * 0.5, Math.sin(angle) * 1.2);
    leafGroup.add(leafMesh);
  }
  scene.add(leafGroup);
  meshMap.set('leaf', leafGroup);
  const leafLabel = makeLabelSprite('Leaves', { scale: 1.4 });
  leafLabel.position.set(-1.8, 2.0, 0);
  scene.add(leafLabel);

  // Flower
  const flowerGroup = new THREE.Group();
  flowerGroup.position.y = 3.5;
  // Centre
  const centre = new THREE.Mesh(
    new THREE.SphereGeometry(0.3, Math.max(6, seg / 4), Math.max(6, seg / 4)),
    new THREE.MeshStandardMaterial({ color: 0xfbbf24, roughness: 0.5 })
  );
  flowerGroup.add(centre);
  // Petals
  for (let i = 0; i < 6; i++) {
    const angle = (i / 6) * Math.PI * 2;
    const petal = new THREE.Mesh(
      new THREE.SphereGeometry(0.32, Math.max(4, seg / 6), Math.max(4, seg / 6)),
      new THREE.MeshStandardMaterial({ color: 0xf9a8d4, roughness: 0.6 })
    );
    petal.scale.z = 0.35;
    petal.position.set(Math.cos(angle) * 0.55, 0, Math.sin(angle) * 0.55);
    flowerGroup.add(petal);
  }
  scene.add(flowerGroup);
  meshMap.set('flower', flowerGroup);
  const flowerLabel = makeLabelSprite('Flower', { scale: 1.4 });
  flowerLabel.position.set(1.5, 4.5, 0);
  scene.add(flowerLabel);

  // Raycasting
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  function onClick(e) {
    const rect = engine.canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const meshArr = [];
    meshMap.forEach((m) => { meshArr.push(m); });
    const hits = raycaster.intersectObjects(meshArr, true);
    if (!hits.length) return;
    let obj = hits[0].object;
    while (obj.parent && !meshMap.has(obj.parent) && obj.parent !== scene) obj = obj.parent;
    meshMap.forEach((m, key) => {
      if (m === obj || m.children && m.children.includes(obj) || (m.parent && m.parent === obj)) {
        const part = PARTS[key];
        if (part) showInfoCard(stage, { title: part.label, body: part.info, color: part.color });
      }
    });
    // Also check if object is inside a group
    meshMap.forEach((m, key) => {
      if (m.isGroup) {
        let cur = hits[0].object;
        while (cur) {
          if (cur === m) {
            const part = PARTS[key];
            if (part) showInfoCard(stage, { title: part.label, body: part.info, color: part.color });
            return;
          }
          cur = cur.parent;
        }
      }
    });
  }

  engine.canvas.addEventListener('click', onClick);

  const hud = createHud(stage);
  hud.badge('Click a plant part!', '#22c55e');

  const panel = createPanel(stage, { title: 'Plant Explorer' });
  panel.info('Drag to rotate the plant. Click any part — roots, stem, leaves or flower — to discover its job!');

  let t = 0;
  engine.setUpdate((dt) => {
    t += dt;
    // Gentle flower wobble
    flowerGroup.rotation.y = Math.sin(t * 0.5) * 0.1;
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('click', onClick);
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
