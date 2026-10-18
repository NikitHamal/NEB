// The practical room: a bright school lab built once per lesson and never rebuilt. A long
// bench (black epoxy for chemistry, oiled teak for physics), a pale wall with a daylight
// window, a whiteboard with the practical's title written on it, shelves stocked for the
// subject, and lighting that reads like a real room: sky light through the window, a warm
// ceiling key that casts soft shadows, and the studio environment for reflections.
import { THREE } from './engine.js';
import { M, box, cyl, glassVessel, woodTexture } from './lab3d-kit.js';

export const BENCH_Y = 0.8;

// the bench top's grain at the scale of a real 1.6 m bench, a little muted
function benchWood() { const t = woodTexture('oak').clone(); t.needsUpdate = true; t.repeat.set(5, 2); return t; }

function boardTexture(title, subtitle, subject) {
  const c = document.createElement('canvas'); c.width = 1536; c.height = 768;
  const g = c.getContext('2d');
  g.fillStyle = '#fbfcfd'; g.fillRect(0, 0, c.width, c.height);
  // faint ghosting of old marker, the way a real board looks
  g.globalAlpha = 0.05; g.fillStyle = '#1f2937';
  for (let i = 0; i < 14; i++) g.fillRect(80 + i * 97 % 1300, 120 + (i * 211) % 560, 180 + (i * 37) % 160, 6);
  g.globalAlpha = 1;
  g.fillStyle = '#6b7280'; g.font = '600 38px "Segoe Print", "Comic Sans MS", system-ui, sans-serif';
  g.fillText(`NEB ${subject === 'chemistry' ? 'Chemistry' : 'Physics'} Practical`, 80, 110);
  g.fillStyle = subject === 'chemistry' ? '#0f766e' : '#1d4ed8';
  g.font = '700 84px "Segoe Print", "Comic Sans MS", system-ui, sans-serif';
  const words = title.split(' '); let line = ''; let y = 240;
  for (const w of words) { const t = line ? `${line} ${w}` : w; if (g.measureText(t).width > 1360) { g.fillText(line, 80, y); y += 100; line = w; } else line = t; }
  g.fillText(line, 80, y);
  g.strokeStyle = g.fillStyle; g.lineWidth = 6; g.beginPath(); g.moveTo(80, y + 26); g.quadraticCurveTo(500, y + 40, 900, y + 22); g.stroke();
  g.fillStyle = '#374151'; g.font = '500 44px "Segoe Print", "Comic Sans MS", system-ui, sans-serif';
  const sub = subtitle || '';
  let l2 = ''; let y2 = y + 120;
  for (const w of sub.split(' ')) { const t = l2 ? `${l2} ${w}` : w; if (g.measureText(t).width > 1360) { g.fillText(l2, 80, y2); y2 += 60; l2 = w; } else l2 = t; }
  if (l2) g.fillText(l2, 80, y2);
  const t = new THREE.CanvasTexture(c);
  if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

function windowTexture() {
  const c = document.createElement('canvas'); c.width = 512; c.height = 384;
  const g = c.getContext('2d');
  const sky = g.createLinearGradient(0, 0, 0, c.height);
  sky.addColorStop(0, '#9cc8f2'); sky.addColorStop(0.62, '#e4f1fb'); sky.addColorStop(0.63, '#bfd3c6'); sky.addColorStop(1, '#8fb39a');
  g.fillStyle = sky; g.fillRect(0, 0, c.width, c.height);
  // distant hills and a white peak, the view from a Nepali school window
  g.fillStyle = '#c8d6e8';
  g.beginPath(); g.moveTo(0, 240); g.lineTo(90, 170); g.lineTo(150, 205); g.lineTo(260, 120); g.lineTo(330, 190); g.lineTo(420, 150); g.lineTo(512, 210); g.lineTo(512, 260); g.lineTo(0, 260); g.fill();
  g.fillStyle = '#ffffff';
  g.beginPath(); g.moveTo(232, 145); g.lineTo(260, 120); g.lineTo(290, 152); g.lineTo(270, 146); g.lineTo(255, 158); g.fill();
  g.fillStyle = '#7fa489'; g.fillRect(0, 250, c.width, 134);
  const t = new THREE.CanvasTexture(c);
  if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export function buildRoom(scene, config, quality) {
  const room = new THREE.Group();
  const chem = config.subject === 'chemistry';
  scene.background = new THREE.Color(0xd9dee5);
  scene.fog = new THREE.Fog(0xd9dee5, 34, 70);

  // floor and walls
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 60), new THREE.MeshStandardMaterial({ color: 0xb7b2a8, roughness: 0.85 }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -8.2; floor.receiveShadow = true; room.add(floor);
  const wallMat = new THREE.MeshStandardMaterial({ color: 0xeceae4, roughness: 0.92 });
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(80, 26), wallMat); wall.position.set(0, 4.8, -4.2); wall.receiveShadow = true; room.add(wall);
  const skirting = box(80, 0.5, 0.06, M.paint(0x9aa3ad), [0, -7.95, -4.17]); room.add(skirting);

  // the bench: a carcass with drawers and a worktop slightly overhanging
  const top = chem
    ? new THREE.Mesh(new THREE.BoxGeometry(16, 0.16, 6.6), new THREE.MeshPhysicalMaterial({ color: 0x1c2125, roughness: 0.38, clearcoat: 0.55, clearcoatRoughness: 0.3 }))
    : new THREE.Mesh(new THREE.BoxGeometry(16, 0.16, 6.6), new THREE.MeshPhysicalMaterial({ map: benchWood(), color: 0xd9cbb8, roughness: 0.5, clearcoat: 0.4, clearcoatRoughness: 0.35 }));
  top.position.set(0, BENCH_Y - 0.08, 0); top.receiveShadow = true; top.castShadow = true; room.add(top);
  const carcass = box(15.6, 8.8, 6.2, M.paint(chem ? 0xe8e4dc : 0xd9d2c3), [0, BENCH_Y - 0.16 - 4.4, -0.1]); room.add(carcass);
  for (let i = -3; i <= 3; i++) {
    room.add(box(2.0, 1.6, 0.04, M.paint(chem ? 0xdedad1 : 0xcfc6b4), [i * 2.2, BENCH_Y - 1.4, 3.02], 0.03));
    room.add(box(0.5, 0.06, 0.06, M.steel(), [i * 2.2, BENCH_Y - 0.9, 3.08], 0.02));
  }

  // window with daylight
  const win = new THREE.Group(); win.position.set(-6.4, 6.0, -4.15);
  const glassPane = new THREE.Mesh(new THREE.PlaneGeometry(5.2, 3.9), new THREE.MeshBasicMaterial({ map: windowTexture(), toneMapped: false }));
  win.add(glassPane);
  const frameM = M.paint(0xf5f5f2);
  win.add(box(5.5, 0.16, 0.14, frameM, [0, 2.02, 0.05]), box(5.5, 0.16, 0.14, frameM, [0, -2.02, 0.05]), box(0.16, 4.2, 0.14, frameM, [-2.68, 0, 0.05]), box(0.16, 4.2, 0.14, frameM, [2.68, 0, 0.05]), box(0.1, 3.9, 0.1, frameM, [0, 0, 0.05]));
  win.add(box(5.9, 0.12, 0.5, frameM, [0, -2.1, 0.25]));
  room.add(win);

  // whiteboard with the practical's title
  const board = new THREE.Group(); board.position.set(2.6, 6.2, -4.12);
  board.add(box(7.6, 3.9, 0.08, M.paint(0xb9c0c8), [0, 0, 0]));
  const face = new THREE.Mesh(new THREE.PlaneGeometry(7.3, 3.65), new THREE.MeshStandardMaterial({ map: boardTexture(config.title.replace(/^3D |^Real 3D /, ''), config.subtitle, config.subject), roughness: 0.3 }));
  face.position.z = 0.045; board.add(face);
  board.add(box(7.6, 0.08, 0.3, M.paint(0x9aa3ad), [0, -1.98, 0.12]));
  board.add(box(0.5, 0.08, 0.08, M.plastic(chem ? 0x0f766e : 0x1d4ed8), [2.6, -1.9, 0.2], 0.03));
  room.add(board);

  // a shelf stocked for the subject
  const shelf = new THREE.Group(); shelf.position.set(9.2, 5.4, -3.8);
  shelf.add(box(4.2, 0.1, 0.8, M.wood('oak'), [0, 0, 0]), box(4.2, 0.1, 0.8, M.wood('oak'), [0, 1.5, 0]));
  if (chem) {
    const reagents = [0x8a5a2b, 0x1f6fb5, 0xf2f2ee, 0x6b2f86, 0xc0392b, 0x2e7d32, 0xf2f2ee];
    reagents.forEach((col, i) => {
      const b = glassVessel('beaker100', { fill: 0.7, color: col, opacity: 0.9, scale: 0.9 });
      b.position.set(-1.7 + i * 0.56, 0.05, 0); shelf.add(b);
      shelf.add(cyl(0.12, 0.12, 0.12, M.plastic(0x222222), [-1.7 + i * 0.56, 0.72, 0], 16));
    });
    reagents.slice(0, 5).forEach((col, i) => { const b = glassVessel('conical', { fill: 0.3, color: col, opacity: 0.85, scale: 0.75 }); b.position.set(-1.6 + i * 0.8, 1.55, 0); shelf.add(b); });
  } else {
    const cols = [0x1d4ed8, 0xd97706, 0x374151, 0x15803d, 0xb91c1c];
    cols.forEach((col, i) => shelf.add(box(0.7, 0.55 + (i % 2) * 0.2, 0.6, M.paint(col), [-1.6 + i * 0.8, 0.33 + (i % 2) * 0.1, 0], 0.03)));
    for (let i = 0; i < 9; i++) shelf.add(box(0.14, 1.0 + (i % 3) * 0.12, 0.7, M.paint([0x7c2d12, 0x1e3a8a, 0x14532d, 0x713f12][i % 4]), [-1.7 + i * 0.2, 2.06 + (i % 3) * 0.06, 0]));
  }
  room.add(shelf);

  // a wall clock: every school lab has one
  const clock = new THREE.Group(); clock.position.set(-1.9, 8.3, -4.1);
  clock.add(cyl(0.55, 0.55, 0.08, M.plastic(0xffffff), [0, 0, 0], 40)); clock.children[0].rotation.x = Math.PI / 2;
  const rim = new THREE.Mesh(new THREE.TorusGeometry(0.56, 0.05, 10, 48), M.plastic(0x1f2937)); clock.add(rim);
  const now = new Date();
  const hh = new THREE.Group(); hh.add(box(0.04, 0.3, 0.01, M.ink(0x111827), [0, 0.15, 0.05])); hh.rotation.z = -((now.getHours() % 12) + now.getMinutes() / 60) / 12 * Math.PI * 2; clock.add(hh);
  const mm = new THREE.Group(); mm.add(box(0.03, 0.44, 0.01, M.ink(0x111827), [0, 0.22, 0.06])); mm.rotation.z = -now.getMinutes() / 60 * Math.PI * 2; clock.add(mm);
  room.add(clock);

  // light: sky through the window, a warm ceiling key with soft shadows, a cool fill
  const hemi = new THREE.HemisphereLight(0xe8f1ff, 0x8a8174, 0.85);
  room.add(hemi);
  const key = new THREE.DirectionalLight(0xfff4e5, 1.9);
  key.position.set(4, 16, 9);
  key.castShadow = !!quality.shadows || quality.tier !== 'low';
  if (key.castShadow) {
    key.shadow.mapSize.set(quality.tier === 'high' ? 2048 : 1024, quality.tier === 'high' ? 2048 : 1024);
    const cam = key.shadow.camera; cam.left = -9; cam.right = 9; cam.top = 9; cam.bottom = -9; cam.near = 4; cam.far = 40;
    key.shadow.bias = -0.0006; key.shadow.normalBias = 0.02; key.shadow.radius = 4;
  }
  room.add(key);
  const windowLight = new THREE.DirectionalLight(0xcfe3ff, 0.6);
  windowLight.position.set(-10, 8, 6);
  room.add(windowLight);
  scene.add(room);
  return { room, key };
}
