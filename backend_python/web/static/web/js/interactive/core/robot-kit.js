// The robotics kit: a clean engineering workshop to stage robots in, and the parts real
// classroom robots are made of: involute spur gears with a proper tooth profile, treaded
// tyres on alloy rims, hobby servos, an ultrasonic ranger, a printed circuit board with
// its chips and traces, an 18650 battery pack, aluminium extrusion. PBR materials lit by the
// engine's studio environment; geometry and textures are cached and shared.
import { THREE } from './engine.js';

const C = new Map();
function cache(k, f) { let v = C.get(k); if (!v) { v = f(); if (v && v.userData) v.userData.sharedFx = true; C.set(k, v); } return v; }
function tex(key, w, h, draw, repeat) {
  return cache(`t:${key}`, () => {
    const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
    const t = new THREE.CanvasTexture(c); if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
    return t;
  });
}

export const RM = {
  shell: (color) => cache(`shell${color}`, () => new THREE.MeshPhysicalMaterial({ color, roughness: 0.32, metalness: 0, clearcoat: 0.7, clearcoatRoughness: 0.18 })),
  matte: (color) => cache(`matte${color}`, () => new THREE.MeshStandardMaterial({ color, roughness: 0.62, metalness: 0.05 })),
  alu: () => cache('alu', () => new THREE.MeshStandardMaterial({ color: 0xc7ced6, roughness: 0.32, metalness: 0.9 })),
  darkAlu: () => cache('darkAlu', () => new THREE.MeshStandardMaterial({ color: 0x3a4048, roughness: 0.38, metalness: 0.85 })),
  steel: () => cache('steel', () => new THREE.MeshStandardMaterial({ color: 0xdfe4ea, roughness: 0.22, metalness: 1 })),
  brass: () => cache('brass', () => new THREE.MeshStandardMaterial({ color: 0xd6ad5a, roughness: 0.3, metalness: 0.95 })),
  rubber: () => cache('rubber', () => new THREE.MeshStandardMaterial({ color: 0x23262b, roughness: 0.92, metalness: 0, map: treadTexture() })),
  glow: (color, k = 1.6) => cache(`glow${color}:${k}`, () => new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: k, roughness: 0.3 })),
  glassDark: () => cache('glassDark', () => new THREE.MeshPhysicalMaterial({ color: 0x0b1220, roughness: 0.05, clearcoat: 1, metalness: 0.2 })),
  pcb: () => cache('pcb', () => new THREE.MeshStandardMaterial({ map: pcbTexture(), roughness: 0.5, metalness: 0.1 })),
};

function treadTexture() {
  return tex('tread', 256, 64, (g, w, h) => { g.fillStyle = '#2a2d31'; g.fillRect(0, 0, w, h); g.fillStyle = '#17191c'; for (let x = 0; x < w; x += 16) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x + 8, h / 2); g.lineTo(x, h); g.lineTo(x + 5, h); g.lineTo(x + 13, h / 2); g.lineTo(x + 5, 0); g.fill(); } }, [6, 1]);
}
function pcbTexture() {
  return tex('pcb', 512, 512, (g, w, h) => {
    g.fillStyle = '#0f5a3a'; g.fillRect(0, 0, w, h);
    g.strokeStyle = '#d4af37'; g.globalAlpha = 0.7; g.lineWidth = 3;
    for (let i = 0; i < 40; i++) { const x = (i * 97) % w, y = (i * 53) % h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + 60 * ((i % 3) - 1), y); g.lineTo(x + 60 * ((i % 3) - 1), y + 70); g.stroke(); }
    g.globalAlpha = 1; g.fillStyle = '#c0c0c0';
    for (let i = 0; i < 80; i++) { g.beginPath(); g.arc((i * 61) % w, (i * 113) % h, 4, 0, Math.PI * 2); g.fill(); }
    g.fillStyle = '#ffffff'; g.font = '600 22px monospace'; g.fillText('NEB-BOT v2', 24, h - 24);
  });
}

/** A bright engineering workshop: a large pale floor with a subtle grid, sky light and a soft-shadow key. */
export function workshop(scene, engine, quality, opts = {}) {
  scene.background = new THREE.Color(opts.background ?? 0xe7ebf0);
  scene.fog = new THREE.Fog(scene.background, opts.fogNear ?? 28, opts.fogFar ?? 70);
  const floorTex = tex('floor', 1024, 1024, (g, w, h) => {
    g.fillStyle = '#d7dce2'; g.fillRect(0, 0, w, h);
    g.strokeStyle = 'rgba(70,84,104,0.22)'; g.lineWidth = 2;
    for (let i = 0; i <= w; i += 64) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); }
    g.strokeStyle = 'rgba(70,84,104,0.08)'; g.lineWidth = 1;
    for (let i = 0; i <= w; i += 16) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); }
  }, [opts.tiles ?? 6, opts.tiles ?? 6]);
  const floor = new THREE.Mesh(new THREE.CircleGeometry(opts.radius ?? 30, 96), new THREE.MeshStandardMaterial({ map: floorTex, roughness: 0.78, metalness: 0 }));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; floor.name = 'floor';
  scene.add(floor);
  scene.add(new THREE.HemisphereLight(0xf2f6ff, 0x8d8f94, 0.9));
  const key = new THREE.DirectionalLight(0xfff6ea, 2.2);
  key.position.set(6, 14, 8);
  if (quality.tier !== 'low') {
    engine.renderer.shadowMap.enabled = true; engine.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    key.castShadow = true; key.shadow.mapSize.set(quality.tier === 'high' ? 2048 : 1024, quality.tier === 'high' ? 2048 : 1024);
    const s = opts.shadowSize ?? 10; const cam = key.shadow.camera; cam.left = -s; cam.right = s; cam.top = s; cam.bottom = -s; cam.near = 1; cam.far = 50;
    key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  }
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xcfe0ff, 0.7); rim.position.set(-8, 6, -10); scene.add(rim);
  return { floor, key };
}

/** Marks every mesh in a group to cast and receive shadows (transparent ones excepted). */
export function shadows(group) { group.traverse((o) => { if (o.isMesh && !(o.material && o.material.transparent)) { o.castShadow = true; o.receiveShadow = true; } }); return group; }

// ---- gears ------------------------------------------------------------------------------------
/** An involute-profile spur gear in the XY plane, extruded along Z, centred, with a bored hub. */
export function gearGeometry(teeth, module = 0.1, thickness = 0.2, bore = 0.08) {
  return cache(`gear:${teeth}:${module}:${thickness}:${bore}`, () => {
    const rp = (module * teeth) / 2, ra = rp + module, rf = rp - 1.25 * module, rb = rp * Math.cos(20 * Math.PI / 180);
    const shape = new THREE.Shape();
    const inv = (a) => Math.tan(a) - a;
    const step = (Math.PI * 2) / teeth;
    const halfTooth = Math.PI / (2 * teeth) + inv(Math.acos(rb / rp));
    const pts = [];
    for (let i = 0; i < teeth; i++) {
      const c = i * step;
      // root, rising flank (involute from base to tip), tip, falling flank, root
      const flank = [];
      for (let k = 0; k <= 6; k++) {
        const r = Math.max(rb, rf) + (ra - Math.max(rb, rf)) * (k / 6);
        const a = Math.acos(Math.min(1, rb / r));
        flank.push([r, inv(a)]);
      }
      pts.push([rf, c - halfTooth - 0.03]);
      flank.forEach(([r, t]) => pts.push([r, c - halfTooth + t]));
      flank.slice().reverse().forEach(([r, t]) => pts.push([r, c + halfTooth - t]));
      pts.push([rf, c + halfTooth + 0.03]);
    }
    pts.forEach(([r, a], i) => { const x = Math.cos(a) * r, y = Math.sin(a) * r; if (i === 0) shape.moveTo(x, y); else shape.lineTo(x, y); });
    const hole = new THREE.Path(); hole.absarc(0, 0, bore, 0, Math.PI * 2, true); shape.holes.push(hole);
    // lightening holes in larger gears, as a machined gear would have
    if (teeth >= 24) for (let k = 0; k < 6; k++) { const a = k * Math.PI / 3; const h = new THREE.Path(); h.absarc(Math.cos(a) * rp * 0.55, Math.sin(a) * rp * 0.55, rp * 0.16, 0, Math.PI * 2, true); shape.holes.push(h); }
    const g = new THREE.ExtrudeGeometry(shape, { depth: thickness, bevelEnabled: true, bevelThickness: thickness * 0.08, bevelSize: module * 0.12, bevelSegments: 2, curveSegments: 16 });
    g.translate(0, 0, -thickness / 2);
    g.computeVertexNormals();
    return g;
  });
}
export function gear(teeth, material, module = 0.1, thickness = 0.2) {
  const m = new THREE.Mesh(gearGeometry(teeth, module, thickness, Math.max(0.05, module * 0.9)), material);
  m.castShadow = true; m.receiveShadow = true;
  m.userData.pitchRadius = (module * teeth) / 2;
  return m;
}

// ---- wheels, servos, sensors ------------------------------------------------------------------
/** A wheel lying on its axle along X: a treaded tyre on a five-spoke alloy rim. */
export function wheel(radius = 0.4, width = 0.24) {
  const g = new THREE.Group();
  const tyre = new THREE.Mesh(cache(`tyre:${radius}:${width}`, () => {
    const pts = []; const w = width / 2; const r0 = radius * 0.72;
    for (let i = 0; i <= 12; i++) { const a = -Math.PI / 2 + (i / 12) * Math.PI; pts.push(new THREE.Vector2(radius - width * 0.18 + Math.cos(a) * width * 0.18, Math.sin(a) * w)); }
    pts.unshift(new THREE.Vector2(r0, -w * 0.9)); pts.push(new THREE.Vector2(r0, w * 0.9));
    const geo = new THREE.LatheGeometry(pts, 48); geo.rotateZ(Math.PI / 2); return geo;
  }), RM.rubber());
  g.add(tyre);
  const rim = new THREE.Mesh(cache(`rim:${radius}:${width}`, () => new THREE.CylinderGeometry(radius * 0.72, radius * 0.72, width * 0.82, 40).rotateZ(Math.PI / 2)), RM.alu());
  g.add(rim);
  for (let k = 0; k < 5; k++) {
    // five spokes on the outer face, each on its own pivot around the axle
    const piv = new THREE.Group(); piv.rotation.x = k * Math.PI * 2 / 5;
    const sp = new THREE.Mesh(cache(`spoke:${radius}:${width}`, () => new THREE.BoxGeometry(width * 0.14, radius * 0.56, radius * 0.11)), RM.darkAlu());
    sp.position.set(width * 0.36, radius * 0.4, 0);
    piv.add(sp); g.add(piv);
  }
  const hub = new THREE.Mesh(cache(`hub:${radius}`, () => new THREE.CylinderGeometry(radius * 0.16, radius * 0.16, width * 0.95, 20).rotateZ(Math.PI / 2)), RM.steel());
  g.add(hub);
  shadows(g);
  return g;
}

export function servo(color = 0x1f2937) {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.38, 0.2), RM.matte(color)));
  const ear = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.03, 0.2), RM.matte(color)); ear.position.y = 0.12; g.add(ear);
  const horn = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.06, 16), RM.matte(0xf8fafc)); horn.rotation.x = Math.PI / 2; horn.position.set(0.1, 0.12, 0.13); g.add(horn);
  shadows(g);
  return g;
}

/** An HC-SR04 style ultrasonic ranger: a blue board with two silver transducers. */
export function ultrasonic() {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.42, 0.04), RM.matte(0x1d4ed8)));
  for (const x of [-0.25, 0.25]) {
    const can = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.2, 28), RM.steel()); can.rotation.x = Math.PI / 2; can.position.set(x, 0, 0.1); g.add(can);
    const mesh = new THREE.Mesh(new THREE.CircleGeometry(0.13, 24), RM.matte(0x2b2f36)); mesh.position.set(x, 0, 0.201); g.add(mesh);
  }
  shadows(g);
  return g;
}

export function pcbBoard(w = 1.0, d = 0.7) {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.BoxGeometry(w, 0.03, d), RM.pcb()));
  const chip = new THREE.Mesh(new THREE.BoxGeometry(w * 0.3, 0.05, d * 0.3), RM.matte(0x111111)); chip.position.y = 0.04; g.add(chip);
  for (let i = 0; i < 4; i++) { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.1, 12), RM.matte(0x1e3a8a)); c.position.set(-w * 0.35 + i * 0.12, 0.06, d * 0.3); g.add(c); }
  const led = new THREE.Mesh(new THREE.SphereGeometry(0.025, 10, 8), RM.glow(0x22c55e, 2)); led.position.set(w * 0.4, 0.04, -d * 0.35); g.add(led);
  g.userData.led = led;
  shadows(g);
  return g;
}

export function batteryPack() {
  const g = new THREE.Group();
  for (let i = 0; i < 2; i++) {
    const cell = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.65, 20), RM.shell(0x16a34a)); cell.rotation.z = Math.PI / 2; cell.position.y = i * 0.21; g.add(cell);
    const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.02, 12), RM.steel()); cap.rotation.z = Math.PI / 2; cap.position.set(0.33, i * 0.21, 0); g.add(cap);
  }
  shadows(g);
  return g;
}

/** A length of aluminium extrusion (a robot arm link) from a to b, square section. */
export function extrusion(len, size = 0.2) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(size, len, size), RM.alu());
  m.position.y = len / 2; m.castShadow = true; m.receiveShadow = true;
  return m;
}

/**
 * A two-wheeled differential-drive classroom robot, nose toward +z: two aluminium decks on
 * brass standoffs, the battery between them, the controller board on top, an ultrasonic
 * ranger on the nose, treaded wheels on the sides and a ball caster at the back.
 */
export function miniBot({ color = 0x2f7de1, wheelR = 0.33, width = 1.1, length = 1.3 } = {}) {
  const group = new THREE.Group();
  const lower = new THREE.Mesh(new THREE.BoxGeometry(width, 0.05, length), RM.darkAlu()); lower.position.y = 0.3; group.add(lower);
  const upper = new THREE.Mesh(new THREE.BoxGeometry(width * 0.92, 0.05, length * 0.88), RM.alu()); upper.position.y = 0.64; group.add(upper);
  for (const x of [-1, 1]) for (const z of [-1, 1]) { const st = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.34, 10), RM.brass()); st.position.set(x * width * 0.38, 0.47, z * length * 0.36); group.add(st); }
  const bat = batteryPack(); bat.scale.setScalar(0.7); bat.position.set(0, 0.36, -0.1); group.add(bat);
  const board = pcbBoard(width * 0.7, length * 0.55); board.position.set(0, 0.68, -0.05); group.add(board);
  const bumper = new THREE.Mesh(new THREE.BoxGeometry(width * 0.98, 0.22, 0.12), RM.shell(color)); bumper.position.set(0, 0.36, length / 2 + 0.02); group.add(bumper);
  const sonar = ultrasonic(); sonar.scale.setScalar(0.55); sonar.position.set(0, 0.5, length / 2 + 0.1); group.add(sonar);
  const shell = new THREE.Mesh(new THREE.BoxGeometry(width * 0.5, 0.18, length * 0.3), RM.shell(color)); shell.position.set(0, 0.77, length * 0.22); group.add(shell);
  const wl = wheel(wheelR, 0.18); wl.rotation.y = Math.PI; wl.position.set(-width / 2 - 0.12, wheelR, -0.1); group.add(wl);
  const wr = wheel(wheelR, 0.18); wr.position.set(width / 2 + 0.12, wheelR, -0.1); group.add(wr);
  const caster = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), RM.steel()); caster.position.set(0, 0.1, -length * 0.42); group.add(caster);
  shadows(group);
  // the spin is about the axle: rotation.x of each wheel's inner pivot
  const spinL = new THREE.Group(); const spinR = new THREE.Group();
  wl.parent.remove(wl); wr.parent.remove(wr);
  spinL.position.copy(wl.position); spinR.position.copy(wr.position); wl.position.set(0, 0, 0); wr.position.set(0, 0, 0);
  spinL.add(wl); spinR.add(wr); group.add(spinL, spinR);
  return { group, wheelL: spinL, wheelR: spinR, sonar, led: board.userData.led };
}
