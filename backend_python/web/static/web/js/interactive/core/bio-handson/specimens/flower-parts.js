// Building blocks for flowers: a petal or sepal is a curved sheet (a width profile along its
// length, cupped across, curled along, with a narrow claw at the base) painted with a colour
// gradient, veins and optional spots; tubes and funnels (fused calyx or corolla) are lathe-like
// surfaces with lobes; stamens are filaments with two-lobed anthers; a pistil is an ovary,
// style and stigma. Everything is built along +Y from the receptacle.
import { THREE } from '../../engine.js';
import { canvasTexture, wet, mesh, rng } from '../kit.js';

export function petalTexture(key, { base, tip, vein = 'rgba(0,0,0,0.12)', spots = null, throat = null, veins = 9 }) {
  return canvasTexture(`petal:${key}`, 256, 512, (g, w, h) => {
    const gr = g.createLinearGradient(0, h, 0, 0);
    gr.addColorStop(0, throat || base); gr.addColorStop(0.25, base); gr.addColorStop(1, tip);
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.strokeStyle = vein; g.lineWidth = 2;
    for (let i = 0; i < veins; i++) {
      const x = (i + 0.5) / veins * w;
      g.beginPath(); g.moveTo(w / 2, h); g.bezierCurveTo(w / 2 + (x - w / 2) * 0.2, h * 0.7, x, h * 0.4, x + (x - w / 2) * 0.15, 0); g.stroke();
    }
    g.strokeStyle = vein.replace(/[\d.]+\)$/, '0.3)'); g.lineWidth = 3.5; g.beginPath(); g.moveTo(w / 2, h); g.lineTo(w / 2, 0); g.stroke();
    if (spots) { const R = rng(7); g.fillStyle = spots; for (let i = 0; i < 70; i++) { const y = h * (0.35 + R() * 0.55); const x = w / 2 + (R() - 0.5) * w * 0.55 * (y / h); g.beginPath(); g.ellipse(x, y, 3 + R() * 4, 4 + R() * 6, 0, 0, Math.PI * 2); g.fill(); } }
  });
}

/**
 * A petal-like sheet. len along +Y, width(v) half-widths, cup = sag across, curl = bend along
 * (positive curls outward, toward +Z), keel = fold along the midrib.
 */
export function sheetGeometry({ len = 1, width = (v) => Math.sin(Math.PI * v) * 0.3, cup = 0.1, curl = 0, twist = 0, keel = 0, nu = 10, nv = 18, edgeWave = 0 }) {
  const pos = []; const uv = []; const idx = [];
  for (let j = 0; j <= nv; j++) {
    const v = j / nv; const w = width(v);
    const ang = curl * v * v;
    for (let i = 0; i <= nu; i++) {
      const u = i / nu * 2 - 1;
      let x = u * w;
      let z = cup * (u * u) * w * 2 - keel * Math.abs(u) * w;
      z += edgeWave * Math.sin(v * 18 + u * 3) * Math.abs(u) * w * 0.3;
      let y = v * len;
      // curl: rotate (y, z) about the base progressively
      const cy = Math.cos(ang); const sy = Math.sin(ang);
      const yy = y * cy - z * sy * 0.2; const zz = z * cy + y * sy;
      const tw = twist * v;
      x = x * Math.cos(tw) - zz * Math.sin(tw) * 0.3;
      pos.push(x, yy, zz); uv.push((u + 1) / 2, v);
    }
  }
  for (let j = 0; j < nv; j++) for (let i = 0; i < nu; i++) { const a = j * (nu + 1) + i; const b = a + nu + 1; idx.push(a, b, a + 1, b, b + 1, a + 1); }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

export function petalMaterial(tex, opts = {}) {
  const m = new THREE.MeshPhysicalMaterial({ map: tex, roughness: opts.roughness ?? 0.55, sheen: 0.6, sheenColor: new THREE.Color(0xffffff), sheenRoughness: 0.4, side: THREE.DoubleSide, clearcoat: opts.clearcoat ?? 0.1 });
  return m;
}

/** A fused tube: radius r(v) and height len, with n lobes at the rim (lobe(v, θ) adds radius/height). */
export function tubeGeometry({ len = 1, radius = (v) => 0.1, lobes = 5, lobeDepth = 0.2, lobeStart = 0.8, ridge = 0, nth = 60, nv = 24, flare = 0 }) {
  const pos = []; const uv = []; const idx = [];
  for (let j = 0; j <= nv; j++) {
    const v = j / nv;
    for (let i = 0; i <= nth; i++) {
      const th = (i / nth) * Math.PI * 2;
      const lobeK = Math.max(0, (v - lobeStart) / (1 - lobeStart));
      const pointy = Math.pow(Math.abs(Math.cos(th * lobes / 2)), 6);
      let r = radius(v) * (1 + ridge * Math.cos(th * lobes) * (1 - lobeK)) * (1 + lobeK * lobeDepth * (pointy - 0.4));
      const y = v * len - lobeK * lobeK * (1 - pointy) * len * 0.12 * (1 + flare);
      r *= 1;
      pos.push(Math.cos(th) * r, y, Math.sin(th) * r); uv.push(i / nth, v);
    }
  }
  for (let j = 0; j < nv; j++) for (let i = 0; i < nth; i++) { const a = j * (nth + 1) + i; const b = a + nth + 1; idx.push(a, a + 1, b, b, a + 1, b + 1); }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

export function stamen({ len = 0.5, filament = 0xf0f0e0, anther = 0xe5b72b, antherLen = 0.06, curve = 0.05, versatile = false }) {
  const g = new THREE.Group();
  const pts = []; for (let i = 0; i <= 8; i++) { const v = i / 8; pts.push(new THREE.Vector3(Math.sin(v * 1.5) * curve, v * len, 0)); }
  g.add(mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 16, Math.max(0.003, len * 0.012), 6), wet(filament, { roughness: 0.5 })));
  const a = new THREE.Group(); a.position.copy(pts[8]);
  const lobeMat = wet(anther, { roughness: 0.7, clearcoat: 0.2 });
  for (const s of [-1, 1]) { const lobe = mesh(new THREE.CapsuleGeometry(antherLen * 0.16, antherLen, 4, 8), lobeMat, [s * antherLen * 0.15, 0, 0]); a.add(lobe); }
  if (versatile) { a.rotation.z = Math.PI / 2; } else a.position.y += antherLen * 0.45;
  g.add(a);
  return g;
}

export function pistil({ ovaryR = 0.06, ovaryH = 0.12, styleLen = 0.4, stigma = 'capitate', color = 0x9ccc65, styleColor = 0xd9e7b0, lobes = 2, bend = 0, spiny = false }) {
  const g = new THREE.Group();
  const ov = mesh(new THREE.SphereGeometry(ovaryR, 18, 14), wet(color, { roughness: 0.45 }));
  ov.scale.y = ovaryH / ovaryR / 2; ov.position.y = ovaryH / 2; ov.name = 'ovary'; g.add(ov);
  if (spiny) { const R = rng(3); for (let i = 0; i < 24; i++) { const th = R() * 6.28; const ph = 0.3 + R() * 2.2; const sp = mesh(new THREE.ConeGeometry(ovaryR * 0.08, ovaryR * 0.35, 5), ov.material, [Math.sin(ph) * Math.cos(th) * ovaryR, ovaryH / 2 + Math.cos(ph) * ovaryH / 2, Math.sin(ph) * Math.sin(th) * ovaryR]); sp.lookAt(0, ovaryH / 2, 0); sp.rotateX(-Math.PI / 2); g.add(sp); } }
  const pts = []; for (let i = 0; i <= 10; i++) { const v = i / 10; pts.push(new THREE.Vector3(0, ovaryH + v * styleLen, Math.sin(v * Math.PI * 0.5) * bend)); }
  g.add(mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 20, Math.max(0.003, ovaryR * 0.12), 6), wet(styleColor)));
  const top = pts[10];
  const sm = wet(0xc5d86d, { roughness: 0.8 });
  if (stigma === 'capitate') g.add(mesh(new THREE.SphereGeometry(ovaryR * 0.3, 10, 8), sm, [top.x, top.y, top.z]));
  else for (let i = 0; i < lobes; i++) { const a = (i / lobes) * Math.PI * 2; const l = mesh(new THREE.SphereGeometry(ovaryR * 0.22, 8, 6), sm, [top.x + Math.cos(a) * ovaryR * 0.2, top.y + ovaryR * 0.05, top.z + Math.sin(a) * ovaryR * 0.2]); l.scale.set(1, 0.6, 1.4); l.rotation.y = -a; g.add(l); }
  g.userData.ovary = ov;
  return g;
}

/** A canvas picture of the ovary in transverse section, for the cut face. */
export function ovaryTSTexture(kind) {
  return canvasTexture(`ovts:${kind}`, 512, 512, (g, w, h) => {
    const c = w / 2; const R = w * 0.46;
    g.fillStyle = '#a8c97a'; g.beginPath(); g.arc(c, c, R, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#d6e8b4'; g.beginPath(); g.arc(c, c, R * 0.92, 0, Math.PI * 2); g.fill();
    const ovule = (x, y, r = 13) => { g.fillStyle = '#f7f3e3'; g.strokeStyle = '#b9a77a'; g.lineWidth = 2; g.beginPath(); g.ellipse(x, y, r, r * 0.8, Math.atan2(y - c, x - c), 0, Math.PI * 2); g.fill(); g.stroke(); };
    const locule = (a0, a1, r0, r1) => { g.fillStyle = '#f4f9ec'; g.beginPath(); g.arc(c, c, r1, a0, a1); g.arc(c, c, r0, a1, a0, true); g.closePath(); g.fill(); };
    if (kind === 'marginal') {
      g.fillStyle = '#f4f9ec'; g.beginPath(); g.ellipse(c, c + 10, R * 0.55, R * 0.62, 0, 0, Math.PI * 2); g.fill();
      ovule(c, c - R * 0.42, 16); ovule(c - 22, c - R * 0.36, 13);
      g.fillStyle = '#9fbf6e'; g.fillRect(c - 8, c - R * 0.92, 16, R * 0.3);
    } else if (kind === 'axile2') {
      // Datura: two carpels, each locule divided by a false septum: four chambers round a swollen placenta
      for (let k = 0; k < 4; k++) locule(k * Math.PI / 2 + 0.12, (k + 1) * Math.PI / 2 - 0.12, R * 0.3, R * 0.78);
      g.fillStyle = '#c4dc98'; g.beginPath(); g.arc(c, c, R * 0.3, 0, Math.PI * 2); g.fill();
      for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2 + Math.PI / 4; for (let i = 0; i < 6; i++) { const rr = R * (0.38 + (i % 3) * 0.12); const da = (Math.floor(i / 3) - 0.5) * 0.34; ovule(c + Math.cos(a + da) * rr, c + Math.sin(a + da) * rr, 11); } }
    } else {
      // Liliaceae: three carpels, three locules, two rows of ovules on the central axis
      for (let k = 0; k < 3; k++) locule(k * 2 * Math.PI / 3 + 0.15, (k + 1) * 2 * Math.PI / 3 - 0.15, R * 0.18, R * 0.8);
      for (let k = 0; k < 3; k++) { const a = k * 2 * Math.PI / 3 + Math.PI / 3; for (const s of [-1, 1]) ovule(c + Math.cos(a + s * 0.22) * R * 0.36, c + Math.sin(a + s * 0.22) * R * 0.36, 14); }
    }
  });
}
