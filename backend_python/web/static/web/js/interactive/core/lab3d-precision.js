import { THREE, makeLabelSprite } from './engine.js';

function mat(color, opts = {}) {
  return new THREE.MeshStandardMaterial({
    color,
    roughness: opts.roughness ?? 0.42,
    metalness: opts.metalness ?? 0.08,
    transparent: opts.opacity !== undefined && opts.opacity < 1,
    opacity: opts.opacity ?? 1,
    emissive: opts.emissive || 0x000000,
    emissiveIntensity: opts.emissiveIntensity || 0,
    side: opts.side || THREE.FrontSide,
  });
}
function metal(color = 0xcbd5e1, roughness = 0.23) { return mat(color, { metalness: 0.78, roughness }); }
function darkMetal() { return mat(0x1f2937, { metalness: 0.62, roughness: 0.28 }); }
function glass(color = 0xbdd7ff, opacity = 0.26) { return mat(color, { opacity, roughness: 0.04, metalness: 0.02, side: THREE.DoubleSide }); }
function rubber(color = 0x0f172a) { return mat(color, { roughness: 0.82 }); }
function box(w, h, d, material, p = [0, 0, 0]) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
  mesh.position.set(...p); mesh.castShadow = true; mesh.receiveShadow = true; return mesh;
}
function cyl(r1, r2, h, material, p = [0, 0, 0], seg = 48) {
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), material);
  mesh.position.set(...p); mesh.castShadow = true; mesh.receiveShadow = true; return mesh;
}
function sph(r, material, p = [0, 0, 0], seg = 48) {
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(16, Math.floor(seg / 2))), material);
  mesh.position.set(...p); mesh.castShadow = true; mesh.receiveShadow = true; return mesh;
}
function line(points, color = 0xffffff, opacity = 1, width = 1) {
  const geo = new THREE.BufferGeometry().setFromPoints(points);
  const material = new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity, linewidth: width });
  return new THREE.Line(geo, material);
}
function label(group, text, p, opts = {}) {
  const sprite = makeLabelSprite(text, {
    fontSize: opts.fontSize || 26,
    scale: opts.scale || 0.18,
    bg: opts.bg ?? true,
    bgColor: opts.bgColor || 'rgba(2,6,23,.76)',
    color: opts.color || '#f8fafc',
    weight: opts.weight || 700,
  });
  sprite.position.set(...p); sprite.renderOrder = 30; group.add(sprite); return sprite;
}

function scaleTexture({ length = 10, minorPerUnit = 10, dark = false, labelText = 'cm', width = 1536, height = 220 } = {}) {
  const canvas = document.createElement('canvas');
  canvas.width = width; canvas.height = height;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = dark ? '#111827' : '#f8fafc';
  ctx.fillRect(0, 0, width, height);
  const pad = 36;
  const usable = width - pad * 2;
  ctx.strokeStyle = dark ? '#f8fafc' : '#020617';
  ctx.fillStyle = dark ? '#f8fafc' : '#020617';
  ctx.lineCap = 'square';
  const count = length * minorPerUnit;
  for (let i = 0; i <= count; i++) {
    const x = pad + usable * (i / count);
    const major = i % minorPerUnit === 0;
    const half = i % Math.max(1, minorPerUnit / 2) === 0;
    const h = major ? 0.72 : half ? 0.55 : 0.36;
    ctx.lineWidth = major ? 4 : 2;
    ctx.beginPath();
    ctx.moveTo(x, height - 8);
    ctx.lineTo(x, height - height * h);
    ctx.stroke();
    if (major) {
      ctx.font = '700 36px system-ui, sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'top';
      ctx.fillText(String(i / minorPerUnit), x, 12);
    }
  }
  ctx.font = '800 22px system-ui, sans-serif';
  ctx.textAlign = 'right';
  ctx.fillText(labelText, width - 22, 18);
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  return tex;
}
function planeWithTexture(w, h, texture) {
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide }));
}
function ribbedCylinder(radius, length, p, axis = 'x', color = 0x94a3b8) {
  const g = new THREE.Group();
  const main = cyl(radius, radius, length, metal(color, 0.26), [0, 0, 0], 72);
  if (axis === 'x') main.rotation.z = Math.PI / 2;
  if (axis === 'z') main.rotation.x = Math.PI / 2;
  g.add(main);
  const ribs = 18;
  for (let i = 0; i < ribs; i++) {
    const offset = -length / 2 + (i + 0.5) * (length / ribs);
    const ring = cyl(radius * 1.018, radius * 1.018, 0.012, metal(0xd7dee8, 0.2), axis === 'x' ? [offset, 0, 0] : [0, 0, offset], 72);
    if (axis === 'x') ring.rotation.z = Math.PI / 2;
    if (axis === 'z') ring.rotation.x = Math.PI / 2;
    g.add(ring);
  }
  g.position.set(...p);
  return g;
}
function ellipseTube(rx, ry, start, end, z, yOffset, material, radius = 0.06) {
  const points = [];
  const steps = 90;
  for (let i = 0; i <= steps; i++) {
    const a = start + (end - start) * (i / steps);
    points.push(new THREE.Vector3(Math.cos(a) * rx, yOffset + Math.sin(a) * ry, z));
  }
  const curve = new THREE.CatmullRomCurve3(points);
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, steps, radius, 18, false), material);
  mesh.castShadow = true; mesh.receiveShadow = true;
  return mesh;
}

export function buildPrecisionCaliper(group, s) {
  const g = new THREE.Group();
  g.position.set(-0.05, 0.32, 0.16);
  g.rotation.y = -0.04;
  const trueGap = THREE.MathUtils.clamp(s.sizeCm, 0.4, 8.0);
  const observed = THREE.MathUtils.clamp(s.sizeCm + s.zeroErrorCm, 0.4, 8.0);
  const fixedX = -4.0;
  const movingX = fixedX + trueGap;
  const objectX = fixedX + trueGap / 2;
  const y = 1.08;
  const jawTop = y + 1.02;
  const jawBottom = y - 0.82;

  const beam = box(8.7, 0.18, 0.52, metal(0xe6edf5, 0.2), [0, y, 0]);
  g.add(beam);
  const topScale = planeWithTexture(8.55, 0.42, scaleTexture({ length: 9, minorPerUnit: 10, labelText: 'main scale cm' }));
  topScale.rotation.x = -Math.PI / 2;
  topScale.position.set(0, y + 0.105, 0.012);
  g.add(topScale);
  g.add(box(8.75, 0.045, 0.06, darkMetal(), [0, y + 0.22, -0.31]));
  g.add(box(8.75, 0.045, 0.06, darkMetal(), [0, y - 0.22, 0.31]));

  function jaw(x, dir, name, moving = false) {
    const j = new THREE.Group();
    j.add(box(0.20, 2.45, 0.28, metal(moving ? 0xc9d3df : 0xe9eef5, 0.2), [x, y + 0.15, 0]));
    j.add(box(0.74, 0.20, 0.30, metal(0xe9eef5, 0.18), [x + dir * 0.27, jawTop, 0]));
    j.add(box(0.50, 0.15, 0.30, metal(0xe9eef5, 0.18), [x + dir * 0.22, jawTop - 0.24, 0]));
    j.add(box(0.82, 0.18, 0.34, metal(0xe9eef5, 0.18), [x + dir * 0.28, jawBottom, 0]));
    j.add(box(0.54, 0.14, 0.34, metal(0xe9eef5, 0.18), [x + dir * 0.20, jawBottom + 0.23, 0]));
    j.add(box(0.028, 2.08, 0.038, rubber(), [x + dir * 0.12, y + 0.05, 0.20]));
    label(j, name, [x + dir * 0.36, y + 1.55, -0.45], { scale: 0.08, fontSize: 18 });
    return j;
  }
  g.add(jaw(fixedX, 1, 'fixed jaw'));
  const slider = new THREE.Group();
  slider.position.x = movingX;
  slider.add(box(1.38, 0.56, 0.62, metal(0xb8c4d0, 0.22), [0.50, y, 0]));
  slider.add(box(0.42, 0.80, 0.64, metal(0xaab6c4, 0.24), [-0.05, y + 0.12, 0]));
  slider.add(jaw(0, -1, 'vernier slider', true));
  const vernier = planeWithTexture(1.22, 0.30, scaleTexture({ length: 10, minorPerUnit: 1, dark: true, labelText: '0.01 cm', width: 840, height: 180 }));
  vernier.rotation.x = -Math.PI / 2;
  vernier.position.set(0.45, y + 0.38, 0.33);
  slider.add(vernier);
  slider.add(cyl(0.12, 0.12, 0.16, darkMetal(), [0.05, y + 0.78, 0.34], 32));
  slider.children[slider.children.length - 1].rotation.x = Math.PI / 2;
  g.add(slider);

  const specimen = sph(0.48, mat(0x0f172a, { metalness: 0.4, roughness: 0.18 }), [objectX, y + 0.05, 0.54], 72);
  specimen.scale.set(Math.max(0.36, trueGap / 1.05), Math.max(0.55, trueGap * 0.26), 0.72);
  g.add(specimen);
  g.add(line([new THREE.Vector3(fixedX, y + 0.05, 0.98), new THREE.Vector3(movingX, y + 0.05, 0.98)], 0x22d3ee, 0.9));
  g.add(box(0.026, Math.max(1.2, trueGap * 0.52), 0.032, mat(0x22d3ee, { opacity: 0.7, emissive: 0x22d3ee, emissiveIntensity: 0.18 }), [fixedX, y + 0.05, 1.0]));
  g.add(box(0.026, Math.max(1.2, trueGap * 0.52), 0.032, mat(0x22d3ee, { opacity: 0.7, emissive: 0x22d3ee, emissiveIntensity: 0.18 }), [movingX, y + 0.05, 1.0]));
  const main = Math.floor(observed * 10) / 10;
  const vsd = Math.max(0, Math.min(9, Math.round((observed - main) / 0.01)));
  label(g, `${s.sizeCm.toFixed(2)} cm true diameter`, [objectX, y + 1.20, 0.72], { scale: 0.15, fontSize: 24 });
  label(g, `MSR ${main.toFixed(1)} cm + VSD ${vsd} × 0.01 cm`, [0.25, y + 0.78, 0.70], { scale: 0.12, fontSize: 21, color: '#dbeafe' });
  group.add(g);
}

export function buildPrecisionMicrometer(group, s) {
  const g = new THREE.Group();
  g.position.set(-0.05, 0.58, 0.25);
  g.rotation.y = -0.08;
  const observed = THREE.MathUtils.clamp(s.diameterMm + s.zeroErrorMm, 0.05, 3.0);
  const sleeve = Math.floor(observed / 0.5) * 0.5;
  const circular = Math.round((observed - sleeve) / 0.01);
  const wireRadius = Math.max(0.045, s.diameterMm / 16);
  const frameMat = metal(0xb9c3cf, 0.18);

  const frame = new THREE.Group();
  frame.add(ellipseTube(1.92, 1.45, Math.PI * 0.64, Math.PI * 1.62, 0, 1.62, frameMat, 0.075));
  frame.add(ellipseTube(1.72, 1.23, Math.PI * 0.66, Math.PI * 1.60, 0, 1.62, metal(0xe2e8f0, 0.22), 0.026));
  frame.add(box(0.36, 0.30, 0.32, frameMat, [-1.62, 1.62, 0]));
  frame.add(box(0.34, 0.26, 0.30, frameMat, [-1.18, 1.62, 0]));
  g.add(frame);

  const anvil = cyl(0.16, 0.16, 0.52, metal(0xf1f5f9, 0.16), [-1.07, 1.62, 0], 56);
  anvil.rotation.z = Math.PI / 2; g.add(anvil);
  const spindleTip = cyl(0.15, 0.15, 0.46, metal(0xf8fafc, 0.14), [-0.40, 1.62, 0], 56);
  spindleTip.rotation.z = Math.PI / 2; g.add(spindleTip);
  const spindle = cyl(0.13, 0.13, 1.32, metal(0xdbe5ef, 0.17), [0.40, 1.62, 0], 72);
  spindle.rotation.z = Math.PI / 2; g.add(spindle);
  const wire = cyl(wireRadius, wireRadius, 0.95, mat(0x111827, { metalness: 0.35, roughness: 0.24 }), [-0.74, 1.62, 0], 48);
  wire.rotation.x = Math.PI / 2; g.add(wire);

  const sleeveBody = cyl(0.26, 0.26, 1.05, metal(0xe5edf6, 0.2), [0.60, 1.62, 0], 72);
  sleeveBody.rotation.z = Math.PI / 2; g.add(sleeveBody);
  const sleeveScale = planeWithTexture(1.0, 0.20, scaleTexture({ length: 5, minorPerUnit: 2, labelText: 'mm', width: 900, height: 150 }));
  sleeveScale.position.set(0.61, 1.90, 0.02);
  g.add(sleeveScale);
  const thimble = ribbedCylinder(0.48, 0.94, [1.42, 1.62, 0], 'x', 0x94a3b8);
  g.add(thimble);
  for (let i = 0; i < 10; i++) {
    const tick = box(0.018, 0.20, 0.012, mat(0x020617), [1.02, 1.62 + 0.38 * Math.sin(i * Math.PI / 10), 0.38 * Math.cos(i * Math.PI / 10)]);
    tick.rotation.x = i * Math.PI / 10;
    g.add(tick);
  }
  const ratchet = ribbedCylinder(0.34, 0.48, [2.17, 1.62, 0], 'x', 0x64748b);
  g.add(ratchet);
  const lock = box(0.12, 0.42, 0.18, darkMetal(), [0.02, 2.05, 0]);
  g.add(lock);

  const contactLine = line([new THREE.Vector3(-1.07, 1.62, 0.52), new THREE.Vector3(-0.40, 1.62, 0.52)], 0x22d3ee, 0.9);
  g.add(contactLine);
  label(g, `${observed.toFixed(2)} mm observed`, [-0.45, 2.38, 0.24], { scale: 0.15, fontSize: 24 });
  label(g, `pitch ${sleeve.toFixed(2)} mm + ${circular} × 0.01 mm`, [0.92, 2.26, 0.28], { scale: 0.12, fontSize: 20, color: '#dbeafe' });
  label(g, 'ratchet', [2.18, 2.16, 0.20], { scale: 0.10, fontSize: 18 });
  label(g, 'anvil', [-1.24, 2.08, 0.18], { scale: 0.09, fontSize: 18 });
  group.add(g);
}

export function buildPrecisionSpherometer(group, s) {
  const g = new THREE.Group();
  g.position.set(0, 0.42, 0.1);
  const baseY = 0.48;
  const glassPlate = cyl(2.25, 2.25, 0.08, glass(0x93c5fd, 0.20), [0, baseY, 0], 96);
  glassPlate.scale.y = 0.12;
  g.add(glassPlate);
  const legR = s.legCm / 4.3;
  const pts = [[0, legR], [-legR * 0.866, -legR / 2], [legR * 0.866, -legR / 2]];
  pts.forEach(([x, z], i) => {
    const leg = cyl(0.042, 0.042, 1.10, metal(0xdbe4ee, 0.18), [x, baseY + 0.60, z], 32);
    g.add(leg);
    g.add(sph(0.105, metal(0xf8fafc, 0.14), [x, baseY + 0.05, z], 32));
    label(g, `leg ${i + 1}`, [x, baseY + 1.25, z], { bg: false, scale: 0.08, fontSize: 18, color: '#e2e8f0' });
  });
  g.add(cyl(0.055, 0.055, 1.45, metal(0xe5e7eb, 0.16), [0, baseY + 0.86, 0], 48));
  const dial = cyl(0.62, 0.62, 0.06, metal(0xa8b3c2, 0.22), [0, baseY + 1.58, 0], 80);
  dial.rotation.x = Math.PI / 2;
  g.add(dial);
  for (let i = 0; i < 40; i++) {
    const a = i * Math.PI * 2 / 40;
    const r1 = i % 5 === 0 ? 0.46 : 0.52;
    const r2 = 0.59;
    g.add(line([new THREE.Vector3(Math.cos(a) * r1, baseY + 1.61 + Math.sin(a) * r1, 0.05), new THREE.Vector3(Math.cos(a) * r2, baseY + 1.61 + Math.sin(a) * r2, 0.05)], 0x111827, 0.9));
  }
  const needleAngle = THREE.MathUtils.degToRad((s.sagittaMm * 120) % 360);
  g.add(line([new THREE.Vector3(0, baseY + 1.61, 0.08), new THREE.Vector3(Math.cos(needleAngle) * 0.48, baseY + 1.61 + Math.sin(needleAngle) * 0.48, 0.08)], 0xef4444, 1));
  label(g, `sagitta h = ${s.sagittaMm.toFixed(2)} mm`, [0, baseY + 2.38, 0.08], { scale: 0.15, fontSize: 24 });
  group.add(g);
}
