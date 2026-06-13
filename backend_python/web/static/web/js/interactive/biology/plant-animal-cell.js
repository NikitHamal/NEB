import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

// 3D cell explorer — plant vs animal cell, click organelles for info

const ORGANELLES = {
  nucleus: {
    color: 0x3b5bdb,
    label: 'Nucleus',
    info: 'The control centre of the cell. Contains DNA (genetic information) packaged in chromosomes. The nuclear membrane has pores for RNA export. All eukaryotic cells have a nucleus.',
    presentIn: ['plant', 'animal'],
  },
  mitochondria: {
    color: 0xf59e0b,
    label: 'Mitochondria',
    info: 'The powerhouse — carries out aerobic respiration (C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP) to produce ATP energy. Has inner folded membranes (cristae) to increase surface area. Present in almost all eukaryotes.',
    presentIn: ['plant', 'animal'],
  },
  er_rough: {
    color: 0x94a3b8,
    label: 'Rough ER',
    info: 'Endoplasmic reticulum studded with ribosomes. Synthesises and folds proteins destined for secretion or membrane insertion. Connected to the nuclear envelope.',
    presentIn: ['plant', 'animal'],
  },
  golgi: {
    color: 0x10b981,
    label: 'Golgi Apparatus',
    info: 'The cell\'s post office — receives proteins from rough ER, modifies them (glycosylation), packages them in vesicles and dispatches them to destinations inside or outside the cell.',
    presentIn: ['plant', 'animal'],
  },
  ribosome: {
    color: 0xfbbf24,
    label: 'Ribosomes',
    info: 'Tiny molecular machines that translate mRNA into proteins (polypeptide chains). Present in ALL living cells. In eukaryotes they are 80S ribosomes; prokaryotes have 70S. Extremely numerous — a single cell can have millions.',
    presentIn: ['plant', 'animal'],
  },
  chloroplast: {
    color: 0x22c55e,
    label: 'Chloroplast',
    info: 'Site of photosynthesis: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂. Has a double membrane plus internal thylakoid membranes stacked into grana. Contains green pigment chlorophyll. Unique to plants and algae.',
    presentIn: ['plant'],
  },
  cell_wall: {
    color: 0xa16207,
    label: 'Cell Wall',
    info: 'Rigid outer layer made of cellulose (β-1,4 glucose polymer) providing structural support, preventing over-expansion and maintaining shape. Freely permeable to water and ions. Absent in animal cells — they have only a plasma membrane.',
    presentIn: ['plant'],
  },
  vacuole: {
    color: 0x7dd3fc,
    label: 'Central Vacuole',
    info: 'Large membrane-bound sac (tonoplast) in plant cells, often occupying >80% of cell volume. Stores water, ions, pigments and waste products. Turgor pressure from the vacuole keeps plant cells firm (turgid).',
    presentIn: ['plant'],
  },
  lysosome: {
    color: 0xef4444,
    label: 'Lysosome',
    info: 'Membrane-bound organelle containing hydrolytic enzymes (acid hydrolases). Digests worn-out organelles (autophagy), foreign particles and cellular debris. Found mainly in animal cells — plant cells use the vacuole for similar functions.',
    presentIn: ['animal'],
  },
  centriole: {
    color: 0xc084fc,
    label: 'Centrioles',
    info: 'Paired cylindrical structures made of microtubule triplets. Form the mitotic spindle during cell division. Found in animal cells and lower plant forms; absent in higher plants (which still divide successfully without them).',
    presentIn: ['animal'],
  },
};

export default function init(stage) {
  const engine = createEngine(stage, { fov: 45 });
  if (!engine) return { dispose() {} };
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 2, 9);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 3, maxDistance: 22, target: new THREE.Vector3(0, 0, 0) });
  basicLights(scene, { ambient: 0.6, key: 1.4 });
  scene.background = new THREE.Color(0x0b1c2e);

  let currentCell = 'plant';
  const orgMeshes = new Map();   // key → THREE.Mesh
  const sprites = new Map();     // key → sprite

  function buildCell(type) {
    // Remove old meshes
    orgMeshes.forEach((m) => { scene.remove(m); m.geometry.dispose(); m.material.dispose(); });
    sprites.forEach((s) => { scene.remove(s); });
    orgMeshes.clear();
    sprites.clear();

    // Cell membrane / wall
    const wallR = 3.3;
    const cellMat = new THREE.MeshStandardMaterial({
      color: type === 'plant' ? 0xd4a017 : 0xaabbcc,
      transparent: true, opacity: type === 'plant' ? 0.12 : 0.1,
      side: THREE.FrontSide, depthWrite: false, roughness: 1,
    });
    const cellSphere = new THREE.Mesh(
      new THREE.SphereGeometry(wallR, seg, seg),
      cellMat
    );
    scene.add(cellSphere);
    orgMeshes.set('__cell__', cellSphere);

    if (type === 'plant') {
      // Cell wall — wire frame
      const wallMat = new THREE.MeshStandardMaterial({ color: 0xa16207, transparent: true, opacity: 0.35, wireframe: true });
      const wall = new THREE.Mesh(new THREE.SphereGeometry(wallR + 0.18, Math.max(8, seg / 2), Math.max(8, seg / 2)), wallMat);
      scene.add(wall);
      orgMeshes.set('cell_wall', wall);
      addLabel('cell_wall', wall, 'Cell Wall');

      // Large vacuole
      const vac = new THREE.Mesh(
        new THREE.SphereGeometry(1.4, seg, seg),
        new THREE.MeshStandardMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.45, roughness: 0.3 })
      );
      vac.position.set(0.6, 0.4, 0.3);
      scene.add(vac);
      orgMeshes.set('vacuole', vac);
      addLabel('vacuole', vac, 'Vacuole');

      // Chloroplasts
      for (let i = 0; i < 5; i++) {
        const angle = (i / 5) * Math.PI * 2;
        const cp = new THREE.Mesh(
          new THREE.SphereGeometry(0.32, Math.max(8, seg / 3), Math.max(8, seg / 3)),
          new THREE.MeshStandardMaterial({ color: 0x22c55e, roughness: 0.7 })
        );
        cp.scale.z = 0.55;
        cp.position.set(Math.cos(angle) * 2.1, 0.2 + Math.sin(angle) * 0.3, Math.sin(angle) * 2.0);
        scene.add(cp);
        orgMeshes.set(`chloroplast_${i}`, cp);
        if (i === 0) addLabel('chloroplast', cp, 'Chloroplast');
      }
    }

    // Nucleus
    const nuc = new THREE.Mesh(
      new THREE.SphereGeometry(0.75, seg, seg),
      new THREE.MeshStandardMaterial({ color: 0x3b5bdb, roughness: 0.5, metalness: 0.1 })
    );
    nuc.position.set(-0.5, 0, 0);
    scene.add(nuc);
    orgMeshes.set('nucleus', nuc);
    addLabel('nucleus', nuc, 'Nucleus');

    // Mitochondria
    for (let i = 0; i < 4; i++) {
      const angle = (i / 4) * Math.PI * 2 + 0.5;
      const mt = new THREE.Mesh(
        new THREE.SphereGeometry(0.26, Math.max(6, seg / 3), Math.max(6, seg / 3)),
        new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.6 })
      );
      mt.scale.z = 1.8;
      mt.position.set(Math.cos(angle) * 1.5, Math.sin(angle) * 0.8, Math.sin(angle) * 1.2);
      scene.add(mt);
      orgMeshes.set(`mitochondria_${i}`, mt);
      if (i === 0) addLabel('mitochondria', mt, 'Mitochondria');
    }

    // Rough ER (flat torus)
    const er = new THREE.Mesh(
      new THREE.TorusGeometry(0.9, 0.12, Math.max(6, seg / 4), Math.max(12, seg / 2)),
      new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.8 })
    );
    er.rotation.x = Math.PI / 3;
    er.position.set(1.0, -0.6, 0.4);
    scene.add(er);
    orgMeshes.set('er_rough', er);
    addLabel('er_rough', er, 'Rough ER');

    // Golgi (stacked discs)
    const golgiGroup = new THREE.Group();
    golgiGroup.position.set(-1.5, 0.8, 0.8);
    for (let i = 0; i < 4; i++) {
      const disc = new THREE.Mesh(
        new THREE.TorusGeometry(0.4 - i * 0.03, 0.07, Math.max(4, seg / 6), Math.max(8, seg / 3)),
        new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.7 })
      );
      disc.rotation.x = Math.PI / 2;
      disc.position.y = i * 0.18;
      golgiGroup.add(disc);
    }
    scene.add(golgiGroup);
    orgMeshes.set('golgi', golgiGroup);
    addLabel('golgi', golgiGroup, 'Golgi');

    // Ribosomes (tiny spheres)
    for (let i = 0; i < 12; i++) {
      const rb = new THREE.Mesh(
        new THREE.SphereGeometry(0.07, Math.max(4, seg / 8), Math.max(4, seg / 8)),
        new THREE.MeshStandardMaterial({ color: 0xfbbf24 })
      );
      const a = (i / 12) * Math.PI * 2;
      rb.position.set(Math.cos(a) * (0.5 + Math.random() * 1.5), (Math.random() - 0.5) * 2, Math.sin(a) * (0.5 + Math.random() * 1.5));
      scene.add(rb);
      orgMeshes.set(`ribosome_${i}`, rb);
      if (i === 0) addLabel('ribosome', rb, 'Ribosomes');
    }

    if (type === 'animal') {
      // Lysosomes
      for (let i = 0; i < 3; i++) {
        const ly = new THREE.Mesh(
          new THREE.SphereGeometry(0.2, Math.max(5, seg / 4), Math.max(5, seg / 4)),
          new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.6 })
        );
        ly.position.set(-1.2 + i * 0.5, -1.2, 0.4 + i * 0.3);
        scene.add(ly);
        orgMeshes.set(`lysosome_${i}`, ly);
        if (i === 0) addLabel('lysosome', ly, 'Lysosome');
      }
      // Centrioles
      for (let k = 0; k < 2; k++) {
        const cen = new THREE.Mesh(
          new THREE.CylinderGeometry(0.1, 0.1, 0.5, Math.max(6, seg / 4)),
          new THREE.MeshStandardMaterial({ color: 0xc084fc, roughness: 0.5 })
        );
        cen.rotation.z = k === 0 ? 0 : Math.PI / 2;
        cen.position.set(0.5 + k * 0.3, 1.5, -0.5);
        scene.add(cen);
        orgMeshes.set(`centriole_${k}`, cen);
        if (k === 0) addLabel('centriole', cen, 'Centrioles');
      }
    }
  }

  function addLabel(key, obj, text) {
    const sp = makeLabelSprite(text, { scale: 1.2, fontSize: 30 });
    const box = new THREE.Box3().setFromObject(obj);
    const size = box.getSize(new THREE.Vector3());
    sp.position.copy(obj.position.clone());
    sp.position.y += size.y / 2 + 0.5;
    scene.add(sp);
    sprites.set(key, sp);
  }

  // Raycasting for click
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  function onClick(e) {
    const rect = engine.canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const meshArr = [];
    orgMeshes.forEach((m) => { meshArr.push(m); });
    const hits = raycaster.intersectObjects(meshArr, true);
    if (!hits.length) return;
    // find which key was hit
    let hitObj = hits[0].object;
    while (hitObj.parent && hitObj.parent !== scene) hitObj = hitObj.parent;
    orgMeshes.forEach((m, key) => {
      if (m === hitObj || m.children.includes(hitObj)) {
        // Find canonical key
        const canonKey = key.replace(/_\d+$/, '');
        const org = ORGANELLES[canonKey];
        if (org) {
          showInfoCard(stage, { title: org.label, body: org.info, color: '#' + org.color.toString(16).padStart(6, '0') });
        }
      }
    });
  }

  engine.canvas.addEventListener('click', onClick);

  const hud = createHud(stage);
  const typeBadge = hud.badge('Plant Cell', '#22c55e');
  const panel = createPanel(stage, { title: 'Cell Explorer' });

  panel.buttonRow([
    {
      label: 'Plant Cell',
      onClick: () => { currentCell = 'plant'; buildCell('plant'); typeBadge.set('Plant Cell'); },
    },
    {
      label: 'Animal Cell',
      onClick: () => { currentCell = 'animal'; buildCell('animal'); typeBadge.set('Animal Cell'); },
    },
  ]);
  panel.info('Drag to rotate. Click any organelle to learn its function. Toggle between plant and animal cells to compare structures.');

  buildCell('plant');

  engine.setUpdate((dt) => {
    controls.update(dt);
    // gentle auto-rotate organelles for visual interest
    orgMeshes.forEach((m, key) => {
      if (key.startsWith('mitochondria') || key.startsWith('ribosome')) {
        m.rotation.y += dt * 0.3;
      }
    });
  });

  engine.start();

  return {
    dispose() {
      engine.canvas.removeEventListener('click', onClick);
      orgMeshes.forEach((m) => { m.geometry && m.geometry.dispose(); m.material && m.material.dispose(); });
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
