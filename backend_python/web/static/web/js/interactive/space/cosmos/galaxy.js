import { THREE } from '../../core/engine.js';
import { pointsMaterial, dustMaterial, makePoints, glowSprite } from './shaders.js';
import { rng, gauss, galLB, galToGlobal, LOCAL_GROUP, GALACTIC_R0, LY } from './astro.js';

function hash2(x, y, s) {
  const h = Math.sin(x * 127.1 + y * 311.7 + s * 74.7) * 43758.5453;
  return h - Math.floor(h);
}

function noise2(x, y, s) {
  const ix = Math.floor(x); const iy = Math.floor(y); const fx = x - ix; const fy = y - iy;
  const ux = fx * fx * (3 - 2 * fx); const uy = fy * fy * (3 - 2 * fy);
  const a = hash2(ix, iy, s); const b = hash2(ix + 1, iy, s); const c = hash2(ix, iy + 1, s); const d = hash2(ix + 1, iy + 1, s);
  return (a * (1 - ux) + b * ux) * (1 - uy) + (c * (1 - ux) + d * ux) * uy;
}

function fbm2(x, y, s) {
  let a = 0.5; let t = 0;
  for (let i = 0; i < 5; i++) { t += a * noise2(x, y, s + i); x = x * 2.03 + 1.7; y = y * 2.03 + 9.2; a *= 0.5; }
  return t;
}

function armField(p, rho, th) {
  let arm = 0; let dust = 0;
  const w = 0.05 + 0.04 * rho;
  for (let k = 0; k < p.arms; k++) {
    const strength = p.armStrength ? p.armStrength[k] : 1;
    const target = p.phase + k * 2 * Math.PI / p.arms + p.wind * Math.log(Math.max(rho, 0.02) / 0.15);
    let d = th - target;
    d = Math.atan2(Math.sin(d), Math.cos(d));
    arm += strength * Math.exp(-Math.pow(d * rho / w, 2));
    const dl = d + p.dustLag;
    dust += strength * Math.exp(-Math.pow(dl * rho / (w * 0.45), 2));
  }
  return { arm, dust };
}

function paintTexture(p, size) {
  const c = document.createElement('canvas');
  c.width = size; c.height = size;
  const g = c.getContext('2d');
  const img = g.createImageData(size, size);
  const cb = Math.cos(p.bar.angle); const sb = Math.sin(p.bar.angle);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const u = (x + 0.5) / size * 2 - 1; const v = (y + 0.5) / size * 2 - 1;
      const rho = Math.hypot(u, v);
      const i = (y * size + x) * 4;
      if (rho > 1) { img.data[i + 3] = 0; continue; }
      const th = Math.atan2(v, u);
      const { arm, dust } = armField(p, rho, th);
      const clump = fbm2(u * 9, v * 9, p.seed);
      const fine = fbm2(u * 30, v * 30, p.seed + 9);
      const disk = Math.exp(-rho / p.scaleLen);
      const bu = u * cb + v * sb; const bv = -u * sb + v * cb;
      const bar = p.bar.len > 0 ? Math.exp(-(Math.pow(bu / p.bar.len, 2) + Math.pow(bv / (p.bar.len * 0.3), 2))) : 0;
      const bulge = Math.exp(-Math.pow(rho / p.bulge, 2));
      const armK = smoothstepJS(0.04, 0.2, rho) * (1 - smoothstepJS(0.75, 1.0, rho));
      let L = disk * (0.18 + p.armGain * arm * armK * (0.6 + clump * 0.8)) + bar * 0.9 + bulge * 2.4;
      const dustK = 1 - Math.min(0.85, dust * armK * (0.55 + fine * 0.6) * p.dustGain);
      L *= dustK;
      L *= 1 - smoothstepJS(0.85, 1.0, rho);
      const young = Math.min(1, arm * armK * 1.2);
      const core = Math.min(1, bulge * 1.4 + bar * 0.8);
      let r = 0.95 * (1 - young) + 0.72 * young; let gg = 0.88 * (1 - young) + 0.82 * young; let b = 0.74 * (1 - young) + 1.0 * young;
      r = r * (1 - core) + 1.0 * core; gg = gg * (1 - core) + 0.86 * core; b = b * (1 - core) + 0.62 * core;
      const hii = Math.pow(Math.max(0, fine - 0.62) * 3.2, 3) * young * 1.5;
      r += hii; gg += hii * 0.35; b += hii * 0.6;
      const tone = 1 - Math.exp(-L * 0.9);
      img.data[i] = Math.min(255, r * tone * 255);
      img.data[i + 1] = Math.min(255, gg * tone * 255);
      img.data[i + 2] = Math.min(255, b * tone * 255);
      img.data[i + 3] = 255;
    }
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function smoothstepJS(a, b, x) { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); }

export function makeGalaxy(p, quality) {
  const group = new THREE.Group();
  const tier = quality.tier;
  const r = rng(p.seed);
  const tex = paintTexture(p, tier === 'low' ? 384 : tier === 'medium' ? 640 : 900);
  const diskMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
  diskMat.toneMapped = false;
  const disk = new THREE.Mesh(new THREE.PlaneGeometry(2 * p.radius, 2 * p.radius), diskMat);
  disk.rotation.x = -Math.PI / 2;
  group.add(disk);
  const n = Math.round(p.stars * (tier === 'low' ? 0.35 : tier === 'medium' ? 0.65 : 1));
  const pos = new Float32Array(n * 3); const col = new Float32Array(n * 3); const size = new Float32Array(n);
  let i = 0;
  let guard = 0;
  while (i < n && guard++ < n * 20) {
    const rho = Math.min(0.98, -Math.log(1 - r() * 0.985) * p.scaleLen * 0.9);
    const th = r() * Math.PI * 2;
    const { arm } = armField(p, rho, th);
    const bulge = Math.exp(-Math.pow(rho / p.bulge, 2));
    const prob = 0.12 + 0.88 * Math.min(1, arm * smoothstepJS(0.04, 0.2, rho)) + bulge;
    if (r() > prob) continue;
    const inBulge = r() < bulge * 0.7;
    const rr = inBulge ? Math.abs(gauss(r)) * p.bulge * 0.7 : rho;
    const tt = inBulge ? r() * Math.PI * 2 : th;
    const thick = inBulge ? p.bulge * 0.55 : 0.012 + 0.01 * rho;
    pos[i * 3] = Math.cos(tt) * rr * p.radius;
    pos[i * 3 + 2] = Math.sin(tt) * rr * p.radius;
    pos[i * 3 + 1] = gauss(r) * thick * p.radius * (inBulge ? 0.75 : 1);
    const young = !inBulge && arm > 0.5 && r() < 0.6;
    const c = new THREE.Color(young ? (r() < 0.12 ? 0xff9fc0 : 0xb8ccff) : inBulge ? 0xffd9a0 : 0xfff0dc);
    const k = young ? 0.5 + r() * 0.8 : 0.3 + r() * 0.5;
    col[i * 3] = c.r * k; col[i * 3 + 1] = c.g * k; col[i * 3 + 2] = c.b * k;
    size[i] = p.radius * (young ? 0.006 : 0.004) * (0.6 + r());
    i++;
  }
  const stars = makePoints(pos.subarray(0, i * 3), col.subarray(0, i * 3), size.subarray(0, i), pointsMaterial({ min: 0.9, max: 7, gain: 0.8, core: 0.3 }));
  group.add(stars);
  const dn = Math.round(n * 0.18);
  const dpos = new Float32Array(dn * 3); const dsize = new Float32Array(dn);
  let j = 0; guard = 0;
  while (j < dn && guard++ < dn * 40) {
    const rho = 0.08 + r() * 0.75;
    const th = r() * Math.PI * 2;
    const { dust } = armField(p, rho, th);
    if (r() > dust * 0.9) continue;
    dpos[j * 3] = Math.cos(th) * rho * p.radius;
    dpos[j * 3 + 2] = Math.sin(th) * rho * p.radius;
    dpos[j * 3 + 1] = gauss(r) * 0.006 * p.radius;
    dsize[j] = p.radius * 0.03 * (0.5 + r());
    j++;
  }
  const dust = makePoints(dpos.subarray(0, j * 3), null, dsize.subarray(0, j), dustMaterial());
  group.add(dust);
  const bulgeGlow = glowSprite(0xffe2b0, p.radius * p.bulge * 5.5, 0.55);
  group.add(bulgeGlow);
  return {
    group,
    stars,
    dust,
    setPx(uPx, scale) {
      stars.material.uniforms.uPx.value = uPx; stars.material.uniforms.uScale.value = scale;
      dust.material.uniforms.uPx.value = uPx; dust.material.uniforms.uScale.value = scale;
    },
    dispose() { tex.dispose(); },
  };
}

function blob(p, quality, seed) {
  const r = rng(seed);
  const n = Math.round((p.kind === 'irregular' ? 3000 : 1600) * (quality.tier === 'low' ? 0.4 : 1));
  const pos = new Float32Array(n * 3); const col = new Float32Array(n * 3); const size = new Float32Array(n);
  const R = p.size / 2000;
  for (let i = 0; i < n; i++) {
    let x; let y; let z;
    if (p.kind === 'irregular') {
      const cl = Math.floor(r() * 6);
      const cx = Math.cos(cl * 2.1) * 0.35 * (cl % 3 === 0 ? 0 : 1); const cz = Math.sin(cl * 1.3) * 0.25;
      x = (cx + gauss(r) * 0.32) * R; z = (cz + gauss(r) * 0.22) * R; y = gauss(r) * 0.08 * R;
    } else {
      x = gauss(r) * 0.3 * R; z = gauss(r) * 0.22 * R; y = gauss(r) * 0.2 * R;
    }
    pos[i * 3] = x; pos[i * 3 + 1] = y; pos[i * 3 + 2] = z;
    const c = new THREE.Color(p.kind === 'irregular' ? (r() < 0.5 ? 0xbcd0ff : 0xfff0dc) : 0xffe2b8);
    const k = 0.3 + r() * 0.5;
    col[i * 3] = c.r * k; col[i * 3 + 1] = c.g * k; col[i * 3 + 2] = c.b * k;
    size[i] = R * 0.03 * (0.5 + r());
  }
  return makePoints(pos, col, size, pointsMaterial({ min: 0.9, max: 5, gain: 0.8 }));
}

export const MILKY_WAY = {
  seed: 11, radius: 52, arms: 4, armStrength: [1, 0.55, 1, 0.55], phase: 0.6, wind: -3.4, dustLag: 0.16,
  scaleLen: 0.34, bulge: 0.075, bar: { len: 0.2, angle: 0.47 }, armGain: 1.7, dustGain: 1.25, stars: 90000,
};

export function createMilkyWay(quality) {
  const g = makeGalaxy(MILKY_WAY, quality);
  const sunLocal = new THREE.Vector3(-GALACTIC_R0 / LY / 1000, 0.02, 0);
  return {
    ...g,
    sunLocal,
    labels: [
      { text: 'Milky Way', sub: '~100 000 light-years across · 100–400 billion stars', get: (v) => v.set(30, 0, 44), min: 20.8, max: 22.7 },
      { text: 'You are here', sub: 'the Sun, 26 700 light-years from the centre', get: (v) => v.copy(sunLocal), min: 19.6, max: 22.0, cls: 'here' },
      { text: 'Sagittarius A*', sub: 'a black hole of 4 million Suns', get: (v) => v.set(0, 0, 0), min: 20.0, max: 21.9 },
      { text: 'Perseus Arm', sub: '', get: (v) => v.set(-28, 0, -18), min: 20.3, max: 21.6, minor: true },
      { text: 'Scutum–Centaurus Arm', sub: '', get: (v) => v.set(14, 0, 22), min: 20.3, max: 21.6, minor: true },
    ],
  };
}

function diskQuaternion(los, incl, pa) {
  const north = galToGlobal(0, 0, 1);
  const axis = new THREE.Vector3().crossVectors(los, north).normalize();
  axis.applyAxisAngle(los, pa * Math.PI / 180);
  const normal = los.clone().negate().applyAxisAngle(axis, incl * Math.PI / 180);
  return new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), normal);
}

export function createLocalGroup(quality) {
  const group = new THREE.Group();
  const parts = [];
  const labels = [];
  LOCAL_GROUP.forEach((p, idx) => {
    const pos = galLB(p.l, p.b, p.d / 1000);
    const los = pos.clone().normalize();
    let obj;
    if (p.kind === 'spiral') {
      const big = p.id === 'm31';
      const gal = makeGalaxy({
        seed: 40 + idx, radius: p.size / 2000, arms: 2, phase: big ? 1.2 : 0.4, wind: big ? -4.6 : -2.6, dustLag: 0.14,
        scaleLen: big ? 0.36 : 0.4, bulge: big ? 0.11 : 0.05, bar: { len: 0, angle: 0 }, armGain: big ? 1.3 : 1.9, dustGain: big ? 1.4 : 0.8,
        stars: big ? 50000 : 16000,
      }, quality);
      gal.group.quaternion.copy(diskQuaternion(los, p.tilt[0], p.tilt[1]));
      obj = gal;
      parts.push(gal);
    } else {
      const b = blob(p, quality, 70 + idx);
      obj = { group: b, setPx(uPx, scale) { b.material.uniforms.uPx.value = uPx; b.material.uniforms.uScale.value = scale; } };
      parts.push(obj);
    }
    obj.group.position.copy(pos);
    group.add(obj.group);
    const halo = glowSprite(p.kind === 'irregular' ? 0xcfdcff : 0xffe6c4, p.size / 1000 * (p.kind === 'spiral' ? 1.6 : 2.2), p.kind === 'spiral' ? 0.55 : 0.4);
    halo.position.copy(pos);
    group.add(halo);
    const major = ['m31', 'm33', 'lmc', 'smc'].includes(p.id);
    labels.push({
      text: p.name,
      sub: `${p.d >= 1e6 ? (p.d / 1e6).toFixed(2) + ' million' : Math.round(p.d / 1000) + ' thousand'} light-years away`,
      get: (v) => v.copy(pos), min: p.d > 1e6 ? 21.3 : 21.0, max: major ? 24.3 : 23.6, minor: !major,
    });
  });
  const r = rng(5150);
  const dn = 40;
  const dp = new Float32Array(dn * 3); const dc = new Float32Array(dn * 3); const ds = new Float32Array(dn);
  const m31 = galLB(121.17, -21.57, 2540);
  for (let i = 0; i < dn; i++) {
    const host = i % 2 === 0 ? m31 : new THREE.Vector3();
    const d = 60 + Math.pow(r(), 0.7) * 900;
    const u = r() * 2 - 1; const th = r() * Math.PI * 2; const s = Math.sqrt(1 - u * u);
    dp[i * 3] = host.x + s * Math.cos(th) * d; dp[i * 3 + 1] = host.y + u * d; dp[i * 3 + 2] = host.z + s * Math.sin(th) * d;
    dc[i * 3] = 0.7; dc[i * 3 + 1] = 0.66; dc[i * 3 + 2] = 0.6;
    ds[i] = 4 + r() * 6;
  }
  const dwarfs = makePoints(dp, dc, ds, pointsMaterial({ min: 1.5, max: 5, gain: 0.6 }));
  group.add(dwarfs);
  parts.push({ setPx(uPx, scale) { dwarfs.material.uniforms.uPx.value = uPx; dwarfs.material.uniforms.uScale.value = scale; } });
  labels.push({ text: 'Milky Way', sub: 'our galaxy', get: (v) => v.set(0, 0, 0), min: 22.6, max: 24.0, cls: 'here' });
  labels.push({ text: 'Local Group', sub: '~80 galaxies, 10 million light-years across', get: (v) => v.copy(m31).multiplyScalar(0.45).add(new THREE.Vector3(0, 1600, 0)), min: 23.2, max: 24.6 });
  return {
    group,
    labels,
    setPx(uPx, scale) { parts.forEach((p) => p.setPx(uPx, scale)); },
    dispose() { parts.forEach((p) => p.dispose && p.dispose()); },
  };
}
