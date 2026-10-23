import { THREE } from '../../core/engine.js';
import { rng, makeCanvas, canvasTexture, patchMaterial, mergeGeos, taperedTube, basisQuaternion, paintVertices, clamp, lerp } from '../butterfly/kit.js';

const WATER_Y = 10;
const TUBE = { r: 0.95, bottom: 7.2, top: 19.5 };
const FUNNEL = { mouthY: 1.3, mouthR: 3.5, neckY: 6.2, neckR: 0.42, stemTop: 9.0 };

function woodCanvas(size, rand) {
  const c = makeCanvas(size, size / 2); const g = c.getContext('2d');
  const W = size; const H = size / 2;
  g.fillStyle = '#7a5434'; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 260; i++) {
    const y = rand() * H; const amp = 2 + rand() * 6; const ph = rand() * 6;
    g.strokeStyle = `rgba(${40 + rand() * 40 | 0},${24 + rand() * 20 | 0},${10 + rand() * 12 | 0},${0.12 + rand() * 0.25})`;
    g.lineWidth = 0.6 + rand() * 2.2;
    g.beginPath();
    for (let x = 0; x <= W; x += 16) g.lineTo(x, y + Math.sin(x / (60 + amp * 20) + ph) * amp);
    g.stroke();
  }
  for (let i = 0; i < 90; i++) {
    g.fillStyle = `rgba(${150 + rand() * 60 | 0},${100 + rand() * 40 | 0},${60 + rand() * 30 | 0},0.08)`;
    g.fillRect(rand() * W, rand() * H, 40 + rand() * 200, 1 + rand() * 4);
  }
  for (let p = 0; p < 6; p++) { g.fillStyle = 'rgba(30,18,8,0.25)'; g.fillRect(0, (p / 6) * H, W, 1.5); }
  return c;
}

function scaleCanvas(w, h, draw) { const c = makeCanvas(w, h); draw(c.getContext('2d'), w, h); return c; }

function glassMaterial(tier, opts = {}) {
  if (tier === 'low' || opts.simple) {
    const m = new THREE.MeshPhysicalMaterial({ color: opts.color ?? 0xffffff, transparent: true, opacity: opts.opacity ?? 0.16, roughness: 0.04, metalness: 0, clearcoat: 1, envMapIntensity: 1.6, depthWrite: false, side: THREE.DoubleSide });
    return patchMaterial(m, { fragEnd: 'float gRim = pow(1.0 - abs(dot(normalize(normal), normalize(vViewPosition))), 3.0); gl_FragColor.rgb += vec3(0.75, 0.85, 0.9) * gRim * 0.35; gl_FragColor.a = min(1.0, gl_FragColor.a + gRim * 0.35);', key: 'simple-glass' });
  }
  return new THREE.MeshPhysicalMaterial({
    color: opts.color ?? 0xffffff, transmission: 1, thickness: opts.thickness ?? 0.25, roughness: opts.roughness ?? 0.02, ior: opts.ior ?? 1.5,
    metalness: 0, envMapIntensity: 1.3, specularIntensity: 1, attenuationColor: new THREE.Color(opts.tint ?? 0xeaf6f0), attenuationDistance: opts.att ?? 30,
    side: opts.side ?? THREE.FrontSide, depthWrite: false,
  });
}

function latheShell(profile, seg) {
  return new THREE.LatheGeometry(profile.map(([r, y]) => new THREE.Vector2(r, y)), seg);
}

function hydrillaLeafGeometry() {
  const n = 9; const pos = []; const idx = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n; const y = t * 1.25;
    const w = 0.15 * Math.sin(Math.PI * Math.pow(t, 0.65)) * (1 - 0.2 * t) + 0.012;
    const tooth = i % 2 ? 0.018 : 0;
    const bend = 0.22 * t * t;
    pos.push(-(w + tooth), y, bend, 0, y, bend - 0.012, w + tooth, y, bend);
  }
  for (let i = 0; i < n; i++) {
    const a = i * 3;
    idx.push(a, a + 3, a + 1, a + 1, a + 3, a + 4, a + 1, a + 4, a + 2, a + 2, a + 4, a + 5);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(pos.length / 3 * 2), 2));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}

export function buildBench({ tier }) {
  const rand = rng(77);
  const group = new THREE.Group();
  const seg = tier === 'low' ? 32 : 64;
  const rich = tier !== 'low';

  const woodTex = canvasTexture(woodCanvas(tier === 'high' ? 1024 : 512, rand), { anisotropy: 8 });
  const bench = new THREE.Mesh(new THREE.BoxGeometry(130, 4, 64), new THREE.MeshPhysicalMaterial({ map: woodTex, roughness: 0.48, clearcoat: rich ? 0.6 : 0, clearcoatRoughness: 0.35 }));
  bench.position.set(-18, -2, -6);
  bench.receiveShadow = true;
  group.add(bench);

  const wallTex = canvasTexture(scaleCanvas(512, 256, (g, w, h) => {
    const grd = g.createLinearGradient(0, 0, 0, h); grd.addColorStop(0, '#2c3a4a'); grd.addColorStop(1, '#1b242f');
    g.fillStyle = grd; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 14; i++) { g.fillStyle = `rgba(${120 + rand() * 80 | 0},${150 + rand() * 60 | 0},${170 + rand() * 50 | 0},0.18)`; g.fillRect(30 + i * 34 + rand() * 8, h * (0.25 + rand() * 0.12), 8 + rand() * 12, h * (0.18 + rand() * 0.15)); }
    g.fillStyle = 'rgba(200,220,240,0.14)'; g.fillRect(0, h * 0.44, w, 4);
    const win = g.createLinearGradient(w * 0.62, 0, w * 0.95, 0); win.addColorStop(0, 'rgba(120,150,190,0)'); win.addColorStop(0.5, 'rgba(150,180,215,0.25)'); win.addColorStop(1, 'rgba(120,150,190,0)');
    g.fillStyle = win; g.fillRect(w * 0.62, h * 0.05, w * 0.33, h * 0.32);
  }));
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(260, 130), new THREE.MeshStandardMaterial({ map: wallTex, roughness: 0.95, emissive: 0xffffff, emissiveMap: wallTex, emissiveIntensity: 0.35 }));
  wall.position.set(-10, 50, -45);
  group.add(wall);

  const glass = glassMaterial(tier, { thickness: 0.3 });
  const beakerProfile = [[0.001, 0], [4.55, 0], [4.7, 0.25], [4.7, 12.6], [4.95, 12.85], [4.98, 13.05], [4.75, 13.05], [4.45, 12.8], [4.45, 0.42], [0.001, 0.42]];
  const beaker = new THREE.Mesh(latheShell(beakerProfile, seg), glass);
  beaker.renderOrder = 3;
  group.add(beaker);
  const gradTex = canvasTexture(scaleCanvas(512, 512, (g, w, h) => {
    g.clearRect(0, 0, w, h);
    g.strokeStyle = 'rgba(255,255,255,0.85)'; g.fillStyle = 'rgba(255,255,255,0.85)'; g.lineWidth = 3;
    g.font = 'bold 30px system-ui, sans-serif';
    for (let i = 1; i <= 6; i++) {
      const y = h - (i / 6.6) * h * 0.9 - h * 0.03;
      g.beginPath(); g.moveTo(w * 0.04, y); g.lineTo(w * 0.16, y); g.stroke();
      g.fillText(`${i * 100}`, w * 0.18, y + 10);
      for (let k = 1; k < 5; k++) { const yy = y + (k / 5) * (h * 0.9 / 6.6); g.beginPath(); g.moveTo(w * 0.04, yy); g.lineTo(w * 0.09, yy); g.stroke(); }
    }
    g.font = 'bold 26px system-ui, sans-serif'; g.fillText('mL', w * 0.04, h * 0.08);
  }), { anisotropy: 8 });
  const marks = new THREE.Mesh(new THREE.CylinderGeometry(4.73, 4.73, 12, seg, 1, true, -0.5, 1.0), new THREE.MeshBasicMaterial({ map: gradTex, transparent: true, depthWrite: false, toneMapped: false, opacity: 0.8 }));
  marks.position.y = 6.4; marks.renderOrder = 4;
  group.add(marks);

  const waterMat = tier === 'low'
    ? new THREE.MeshPhysicalMaterial({ color: 0x9fd4d8, transparent: true, opacity: 0.32, roughness: 0.05, depthWrite: false })
    : new THREE.MeshPhysicalMaterial({ color: 0xffffff, transmission: 1, thickness: 7, roughness: 0.03, ior: 1.33, attenuationColor: new THREE.Color(0xa8dccb), attenuationDistance: 14, envMapIntensity: 1, depthWrite: false });
  const water = new THREE.Mesh(new THREE.CylinderGeometry(4.43, 4.43, WATER_Y - 0.44, seg, 1), waterMat);
  water.position.y = 0.44 + (WATER_Y - 0.44) / 2;
  water.renderOrder = 2;
  group.add(water);
  const meniscus = new THREE.Mesh(new THREE.TorusGeometry(4.4, 0.06, 6, seg), new THREE.MeshBasicMaterial({ color: 0xdff4ff, transparent: true, opacity: 0.55, depthWrite: false }));
  meniscus.rotation.x = Math.PI / 2; meniscus.position.y = WATER_Y - 0.02;
  const surface = new THREE.Mesh(new THREE.CircleGeometry(4.42, seg), new THREE.MeshPhysicalMaterial({ color: 0xcfeeee, transparent: true, opacity: 0.12, roughness: 0.05, clearcoat: 1, depthWrite: false }));
  surface.rotation.x = -Math.PI / 2; surface.position.y = WATER_Y - 0.03;
  group.add(meniscus, surface);

  const funnelProfile = [[FUNNEL.mouthR, FUNNEL.mouthY], [FUNNEL.neckR + 0.05, FUNNEL.neckY], [FUNNEL.neckR, FUNNEL.stemTop], [FUNNEL.neckR - 0.12, FUNNEL.stemTop], [FUNNEL.neckR - 0.17, FUNNEL.neckY], [FUNNEL.mouthR - 0.14, FUNNEL.mouthY + 0.05]];
  const funnel = new THREE.Mesh(latheShell(funnelProfile, seg), glassMaterial(tier, { simple: true, opacity: 0.1, color: 0xe6f4ff }));
  funnel.renderOrder = 3;
  group.add(funnel);
  const feetMat = new THREE.MeshStandardMaterial({ color: 0x3f6fb5, roughness: 0.7 });
  for (let i = 0; i < 3; i++) {
    const a = (i / 3) * Math.PI * 2 + 0.4;
    const foot = new THREE.Mesh(new THREE.SphereGeometry(0.55, 12, 8), feetMat);
    foot.scale.set(1, 0.85, 1);
    foot.position.set(Math.cos(a) * 3.3, 0.85, Math.sin(a) * 3.3);
    group.add(foot);
  }

  const tp = [[TUBE.r + 0.06, TUBE.bottom]];
  for (let i = 0; i <= 8; i++) { const a = (i / 8) * Math.PI / 2; tp.push([(TUBE.r + 0.06) * Math.cos(a) + 0.001, TUBE.top - TUBE.r + (TUBE.r + 0.06) * Math.sin(a)]); }
  for (let i = 8; i >= 0; i--) { const a = (i / 8) * Math.PI / 2; tp.push([(TUBE.r - 0.04) * Math.cos(a) + 0.001, TUBE.top - TUBE.r + (TUBE.r - 0.04) * Math.sin(a)]); }
  tp.push([TUBE.r - 0.04, TUBE.bottom]);
  const tube = new THREE.Mesh(latheShell(tp, seg), glassMaterial(tier, { simple: true, opacity: 0.2 }));
  tube.renderOrder = 3;
  group.add(tube);
  const tubeWaterMat = new THREE.MeshPhysicalMaterial({ color: 0x9fd6d6, transparent: true, opacity: 0.14, roughness: 0.05, depthWrite: false });
  const tubeWater = new THREE.Mesh(new THREE.CylinderGeometry(TUBE.r - 0.09, TUBE.r - 0.09, 1, seg / 2, 1), tubeWaterMat);
  tubeWater.renderOrder = 2;
  group.add(tubeWater);
  const gasCap = new THREE.Mesh(new THREE.CircleGeometry(TUBE.r - 0.09, seg / 2), new THREE.MeshPhysicalMaterial({ color: 0xdff6ff, roughness: 0.1, transparent: true, opacity: 0.55, depthWrite: false, side: THREE.DoubleSide }));
  gasCap.rotation.x = -Math.PI / 2;
  group.add(gasCap);
  const clamp1 = new THREE.Group();
  const rodMat = new THREE.MeshStandardMaterial({ color: 0xb8bec6, metalness: 0.9, roughness: 0.3 });
  const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 34, 12), rodMat);
  stand.position.set(9.5, 17, -4.5);
  const standBase = new THREE.Mesh(new THREE.BoxGeometry(9, 0.9, 6), new THREE.MeshStandardMaterial({ color: 0x2a2f36, metalness: 0.4, roughness: 0.5 }));
  standBase.position.set(9.5, 0.45, -4.5);
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 10.6, 10), rodMat);
  arm.rotation.z = Math.PI / 2; arm.rotation.y = -0.44;
  arm.position.set(4.8, 16.5, -2.3);
  const jaw = new THREE.Mesh(new THREE.TorusGeometry(TUBE.r + 0.25, 0.22, 8, 24), new THREE.MeshStandardMaterial({ color: 0x7a4b2a, roughness: 0.8 }));
  jaw.rotation.x = Math.PI / 2; jaw.position.set(0, 16.5, 0);
  clamp1.add(stand, standBase, arm, jaw);
  clamp1.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  group.add(clamp1);

  const stemCurve = new THREE.CatmullRomCurve3([new THREE.Vector3(1.8, 0.9, 1.6), new THREE.Vector3(1.1, 2.4, 0.8), new THREE.Vector3(0.35, 4.0, 0.25), new THREE.Vector3(0.05, 5.4, 0.0)]);
  const plantMat = new THREE.MeshPhysicalMaterial({ color: 0x5fae3c, roughness: 0.45, side: THREE.DoubleSide, sheen: rich ? 0.4 : 0, sheenColor: new THREE.Color(0xc8ff9a) });
  patchMaterial(plantMat, { translucency: 0.9, transTint: 0xb0ff60, key: 'hydrilla' });
  const stem = new THREE.Mesh(taperedTube(stemCurve, 30, 8, () => 0.09, { capEnd: true }), new THREE.MeshPhysicalMaterial({ color: 0x8fbf5a, roughness: 0.5 }));
  group.add(stem);
  const branch = new THREE.CatmullRomCurve3([stemCurve.getPointAt(0.35), new THREE.Vector3(-0.6, 3.3, 1.3), new THREE.Vector3(-1.4, 4.2, 1.2)]);
  group.add(new THREE.Mesh(taperedTube(branch, 16, 6, () => 0.07, { capEnd: true }), stem.material));
  const leafGeo = hydrillaLeafGeometry();
  const whorls = [];
  [[stemCurve, 14], [branch, 6]].forEach(([curve, n]) => {
    for (let i = 0; i < n; i++) {
      const t = 0.06 + (i / n) * 0.9;
      whorls.push({ p: curve.getPointAt(t), T: curve.getTangentAt(t), scale: 0.65 + 0.35 * Math.sin(Math.PI * Math.min(1, t * 1.1)), rot: i * 0.6 });
    }
  });
  const perWhorl = 4;
  const leaves = new THREE.InstancedMesh(leafGeo, plantMat, whorls.length * perWhorl);
  const m4 = new THREE.Matrix4(); const sc = new THREE.Vector3(); const q = new THREE.Quaternion();
  let li = 0;
  whorls.forEach((w) => {
    const side = Math.abs(w.T.y) < 0.9 ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(1, 0, 0);
    const u = new THREE.Vector3().crossVectors(w.T, side).normalize(); const v = new THREE.Vector3().crossVectors(w.T, u);
    for (let k = 0; k < perWhorl; k++) {
      const a = w.rot + (k / perWhorl) * Math.PI * 2;
      const out = u.clone().multiplyScalar(Math.cos(a)).addScaledVector(v, Math.sin(a));
      const dir = out.clone().multiplyScalar(0.75).addScaledVector(w.T, 0.66).normalize();
      basisQuaternion(dir, out.clone().negate().add(w.T), q);
      sc.setScalar(w.scale * (0.85 + rand() * 0.3));
      m4.compose(w.p, q, sc);
      leaves.setMatrixAt(li++, m4);
    }
  });
  group.add(leaves);

  const thermo = new THREE.Group();
  const tGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 24, 16, 1), glassMaterial(tier, { simple: true, opacity: 0.22 }));
  tGlass.position.y = 12; tGlass.renderOrder = 3;
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.36, 16, 12), new THREE.MeshPhysicalMaterial({ color: 0xd63a2e, roughness: 0.2, clearcoat: 1 }));
  bulb.scale.y = 1.8; bulb.position.y = 0.2;
  const column = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1, 8), new THREE.MeshStandardMaterial({ color: 0xe0352b, roughness: 0.3, emissive: 0x400800 }));
  const tScale = canvasTexture(scaleCanvas(64, 1024, (g, w, h) => {
    g.fillStyle = '#f4f1e6'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#1d2733'; g.font = 'bold 15px system-ui, sans-serif';
    for (let c = 0; c <= 50; c += 1) {
      const y = h - (0.12 + (c / 50) * 0.8) * h;
      g.fillRect(w * 0.55, y, c % 10 === 0 ? w * 0.45 : c % 5 === 0 ? w * 0.3 : w * 0.18, c % 5 === 0 ? 2 : 1);
      if (c % 10 === 0) g.fillText(String(c), 4, y + 5);
    }
    g.fillText('°C', 6, h * 0.05);
  }), { anisotropy: 8 });
  const card = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 20), new THREE.MeshStandardMaterial({ map: tScale, roughness: 0.6 }));
  card.position.set(0, 12.2, -0.2);
  thermo.add(tGlass, bulb, column, card);
  thermo.position.set(3.0, 3.2, -2.4);
  thermo.rotation.set(-0.12, 0.6, -0.2);
  group.add(thermo);
  const colBase = 0.6; const colSpan = 16;

  const lamp = new THREE.Group();
  const lampMat = new THREE.MeshPhysicalMaterial({ color: 0x2e6b5a, metalness: 0.3, roughness: 0.35, clearcoat: 0.8 });
  const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(5.5, 6, 1.2, 32), lampMat);
  lampBase.position.y = 0.6;
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 14, 12), rodMat);
  pole.position.set(-1.5, 7.5, 0); pole.rotation.z = -0.12;
  const shade = new THREE.Mesh(latheShell([[0.8, 0], [1.6, 0.4], [3.6, 3.0], [4.2, 4.6], [4.05, 4.65], [3.45, 3.05], [1.45, 0.5], [0.001, 0.4]], 32), new THREE.MeshPhysicalMaterial({ color: 0x2e6b5a, metalness: 0.3, roughness: 0.35, clearcoat: 0.8, side: THREE.DoubleSide }));
  shade.rotation.z = -Math.PI / 2 - 0.08;
  shade.position.set(-0.6, 14.4, 0);
  const bulbMesh = new THREE.Mesh(new THREE.SphereGeometry(1.5, 24, 16), new THREE.MeshStandardMaterial({ color: 0xfff6dc, emissive: 0xffe2a8, emissiveIntensity: 3 }));
  bulbMesh.position.set(1.6, 14.3, 0);
  lamp.add(lampBase, pole, shade, bulbMesh);
  lamp.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  const spot = new THREE.SpotLight(0xffe9c4, 900, 0, 0.62, 0.55, 2);
  spot.position.set(2.2, 14.2, 0);
  spot.target.position.set(40, 6, 0);
  if (tier === 'high') { spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -0.0005; spot.shadow.camera.near = 1; spot.shadow.camera.far = 120; }
  lamp.add(spot, spot.target);
  const coneTex = canvasTexture(scaleCanvas(64, 256, (g, w, h) => {
    const grd = g.createLinearGradient(0, 0, 0, h); grd.addColorStop(0, 'rgba(255,236,190,0.55)'); grd.addColorStop(1, 'rgba(255,236,190,0)');
    g.fillStyle = grd; g.fillRect(0, 0, w, h);
    const s = g.createLinearGradient(0, 0, w, 0); s.addColorStop(0, 'rgba(0,0,0,1)'); s.addColorStop(0.5, 'rgba(0,0,0,0)'); s.addColorStop(1, 'rgba(0,0,0,1)');
    g.globalCompositeOperation = 'destination-out'; g.fillStyle = s; g.fillRect(0, 0, w, h);
  }));
  const beam = new THREE.Mesh(new THREE.CylinderGeometry(4, 14, 40, 24, 1, true), new THREE.MeshBasicMaterial({ map: coneTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, opacity: 0.16 }));
  beam.rotation.z = Math.PI / 2; beam.position.set(22.5, 13, 0); beam.rotation.y = 0;
  beam.renderOrder = 6;
  lamp.add(beam);
  lamp.rotation.y = 0;
  group.add(lamp);

  const rulerTex = canvasTexture(scaleCanvas(2048, 64, (g, w, h) => {
    g.fillStyle = '#e9dcb8'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#2b2416'; g.font = 'bold 22px system-ui, sans-serif';
    for (let cm = 0; cm <= 80; cm++) {
      const x = w - (cm / 80) * w;
      g.fillRect(x - 1, 0, 2, cm % 10 === 0 ? h * 0.55 : cm % 5 === 0 ? h * 0.38 : h * 0.24);
      if (cm % 10 === 0 && cm > 0 && cm < 80) g.fillText(String(cm), x - 12, h * 0.92);
    }
  }), { anisotropy: 8 });
  const ruler = new THREE.Mesh(new THREE.BoxGeometry(80, 0.25, 3), [0, 1, 2, 3, 4, 5].map((i) => (i === 2 ? new THREE.MeshStandardMaterial({ map: rulerTex, roughness: 0.6 }) : new THREE.MeshStandardMaterial({ color: 0xcdbf98, roughness: 0.6 }))));
  ruler.position.set(-40, 0.13, 7.5);
  ruler.receiveShadow = true;
  group.add(ruler);

  const dish = new THREE.Group();
  const dishGlass = new THREE.Mesh(latheShell([[0.001, 0], [4, 0], [4.1, 1.1], [3.92, 1.1], [3.85, 0.18], [0.001, 0.18]], 40), glassMaterial(tier, { simple: true, opacity: 0.25 }));
  const powder = new THREE.Mesh(new THREE.SphereGeometry(2.2, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xf6f6f2, roughness: 1 }));
  powder.scale.y = 0.42; powder.position.y = 0.18;
  const labelTex = canvasTexture(scaleCanvas(256, 128, (g, w, h) => {
    g.fillStyle = '#fbfaf4'; g.fillRect(0, 0, w, h); g.strokeStyle = '#9aa3ad'; g.lineWidth = 3; g.strokeRect(5, 5, w - 10, h - 10);
    g.fillStyle = '#1e293b'; g.font = 'bold 44px system-ui, sans-serif'; g.fillText('NaHCO₃', 22, 62);
    g.font = '22px system-ui, sans-serif'; g.fillText('sodium bicarbonate', 22, 100);
  }), { anisotropy: 8 });
  const label = new THREE.Mesh(new THREE.PlaneGeometry(6, 3), new THREE.MeshStandardMaterial({ map: labelTex, roughness: 0.8 }));
  label.rotation.x = -Math.PI / 2; label.rotation.z = 0.15; label.position.set(0.5, 0.03, 6.2);
  const spatula = new THREE.Mesh(new THREE.BoxGeometry(11, 0.12, 0.8), rodMat);
  spatula.position.set(5, 0.5, 1.2); spatula.rotation.set(0, -0.5, 0.08);
  dish.add(dishGlass, powder, label, spatula);
  dish.position.set(14, 0, 9);
  group.add(dish);

  const iceMat = rich ? new THREE.MeshPhysicalMaterial({ color: 0xffffff, transmission: 1, thickness: 1.2, roughness: 0.18, ior: 1.31 }) : new THREE.MeshPhysicalMaterial({ color: 0xe8f6ff, transparent: true, opacity: 0.6, roughness: 0.2 });
  const ice = [];
  for (let i = 0; i < 3; i++) {
    const c = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.4, 1.6, 2, 2, 2), iceMat);
    const a = i * 2.1 + 0.6;
    c.position.set(Math.cos(a) * 3.2, WATER_Y - 0.3, Math.sin(a) * 3.2 + 0.4);
    c.rotation.set(rand(), rand() * 3, rand());
    c.visible = false;
    group.add(c); ice.push(c);
  }

  const bubbleMax = tier === 'low' ? 24 : 48;
  const bubbleMat = new THREE.ShaderMaterial({
    uniforms: {},
    vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * instanceMatrix * vec4(position,1.0); vN = normalize(normalMatrix * mat3(instanceMatrix) * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }',
    fragmentShader: 'varying vec3 vN; varying vec3 vV; void main(){ float f = 1.0 - abs(dot(normalize(vN), vV)); float rim = pow(f, 2.2); float spec = pow(max(dot(reflect(-vV, normalize(vN)), normalize(vec3(-0.6,0.6,0.5))), 0.0), 40.0); gl_FragColor = vec4(vec3(0.92,0.98,1.0) * (rim * 1.4 + spec * 2.0) + 0.04, rim * 0.85 + spec + 0.06); }',
    transparent: true, depthWrite: false,
  });
  const bubbles = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 14, 10), bubbleMat, bubbleMax);
  bubbles.count = 0; bubbles.renderOrder = 8; bubbles.frustumCulled = false;
  group.add(bubbles);
  const live = [];
  const cut = stemCurve.getPointAt(1);

  const state = { gas: 0.04, acc: 0, onBubble: null };
  function spawn() {
    if (live.length >= bubbleMax) return;
    live.push({ p: cut.clone().add(new THREE.Vector3((rand() - 0.5) * 0.08, 0.12, (rand() - 0.5) * 0.08)), v: 0.6, r: 0.1 + rand() * 0.1, ph: rand() * 6.28, age: 0 });
  }
  const tubeTopFor = () => TUBE.top - TUBE.r * 0.6 - state.gas * (TUBE.top - TUBE.bottom - 3);

  function setLevels(levels) {
    lamp.position.set(-(levels.distance + 1.6), 0, 0);
    spot.visible = !!levels.lamp;
    spot.target.position.set(levels.distance + 1.6, 6, 0);
    beam.visible = !!levels.lamp;
    bulbMesh.material.emissiveIntensity = levels.lamp ? 3 : 0.05;
    const tc = clamp(levels.temperature / 50);
    column.scale.y = colBase + tc * colSpan;
    column.position.y = 0.6 + column.scale.y / 2 + 1.2;
    ice.forEach((c, i) => { c.visible = levels.temperature < 12 - i * 2; });
    powder.scale.setScalar(0.35 + levels.bicarb * 1.2); powder.scale.y *= 0.42;
  }

  const tmp = new THREE.Matrix4(); const sv = new THREE.Vector3(); const qi = new THREE.Quaternion();
  function update(dt, time, metrics) {
    state.acc += dt * (metrics.bubbles / 60);
    while (state.acc >= 1) { state.acc -= 1; spawn(); }
    const top = tubeTopFor();
    for (let i = live.length - 1; i >= 0; i--) {
      const b = live[i];
      b.age += dt;
      b.v = Math.min(5.5, b.v + dt * 7);
      b.p.y += b.v * dt;
      const y = b.p.y;
      let rmax;
      if (y < FUNNEL.neckY) rmax = lerp(FUNNEL.mouthR - 0.3, FUNNEL.neckR - 0.2, clamp((y - FUNNEL.mouthY) / (FUNNEL.neckY - FUNNEL.mouthY)));
      else if (y < FUNNEL.stemTop) rmax = FUNNEL.neckR - 0.22;
      else rmax = TUBE.r - 0.3;
      const wob = Math.sin(time * 9 + b.ph) * 0.05;
      b.p.x += wob * dt * 4;
      const rr = Math.hypot(b.p.x, b.p.z);
      if (rr > rmax) { b.p.x *= rmax / rr; b.p.z *= rmax / rr; }
      if (y > top - b.r) {
        state.gas = Math.min(0.78, state.gas + b.r * b.r * 0.06);
        live.splice(i, 1);
        if (state.onBubble) state.onBubble();
      }
    }
    live.forEach((b, i) => {
      const s = b.r * (1 + 0.12 * Math.sin(time * 18 + b.ph));
      tmp.compose(b.p, qi, sv.set(s * 1.1, s * 0.9, s));
      bubbles.setMatrixAt(i, tmp);
    });
    bubbles.count = live.length;
    bubbles.instanceMatrix.needsUpdate = true;
    const t2 = tubeTopFor();
    tubeWater.scale.y = Math.max(0.01, t2 - TUBE.bottom);
    tubeWater.position.y = TUBE.bottom + tubeWater.scale.y / 2;
    gasCap.position.y = t2 + 0.01;
    leaves.rotation.y = Math.sin(time * 0.6) * 0.004;
  }

  return {
    group, lamp, state, setLevels, update,
    resetGas() { state.gas = 0.04; },
    focus: new THREE.Vector3(0, 7, 0),
    leafPoint: () => cut.clone(),
    hotspots: () => [
      { id: 'lamp', pos: () => lamp.localToWorld(new THREE.Vector3(0, 13, 0)), r: 5 },
      { id: 'tube', pos: () => new THREE.Vector3(0, 16, 0), r: 2.2 },
      { id: 'hydrilla', pos: () => new THREE.Vector3(0.6, 3.4, 0.6), r: 2.4 },
      { id: 'funnel', pos: () => new THREE.Vector3(0, 5, 0), r: 2.6 },
      { id: 'thermometer', pos: () => thermo.localToWorld(new THREE.Vector3(0, 14, 0)), r: 2 },
      { id: 'bicarb', pos: () => dish.localToWorld(new THREE.Vector3(0, 0.6, 0)), r: 4 },
      { id: 'beaker', pos: () => new THREE.Vector3(3.6, 8, 2.5), r: 3 },
    ],
    textures: [],
    dispose() { bubbleMat.dispose(); },
  };
}
