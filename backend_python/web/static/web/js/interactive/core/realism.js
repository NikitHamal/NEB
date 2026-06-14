import { THREE } from './engine.js';

const ENV_CACHE = new WeakMap();

function buildEnvironmentTexture(renderer) {
  if (ENV_CACHE.has(renderer)) return ENV_CACHE.get(renderer);
  const pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 256;
  const ctx = c.getContext('2d');
  const sky = ctx.createLinearGradient(0, 0, 0, 256);
  sky.addColorStop(0.0, '#0a1430');
  sky.addColorStop(0.45, '#163a66');
  sky.addColorStop(0.7, '#2f6fa8');
  sky.addColorStop(0.85, '#7cb0d8');
  sky.addColorStop(1.0, '#cfe4f2');
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, 512, 256);
  for (let i = 0; i < 3; i++) {
    const x = 90 + i * 140;
    const g = ctx.createRadialGradient(x, 90, 4, x, 90, 120);
    g.addColorStop(0, 'rgba(255,245,225,0.95)');
    g.addColorStop(0.4, 'rgba(255,225,180,0.45)');
    g.addColorStop(1, 'rgba(255,225,180,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 512, 256);
  }
  const horizon = ctx.createLinearGradient(0, 230, 0, 256);
  horizon.addColorStop(0, 'rgba(240,210,170,0)');
  horizon.addColorStop(1, 'rgba(240,210,170,0.5)');
  ctx.fillStyle = horizon;
  ctx.fillRect(0, 230, 512, 26);
  const tex = new THREE.CanvasTexture(c);
  tex.mapping = THREE.EquirectangularReflectionMapping;
  tex.colorSpace = THREE.SRGBColorSpace;
  const target = pmrem.fromEquirectangular(tex);
  const envMap = target.texture;
  tex.dispose();
  pmrem.dispose();
  ENV_CACHE.set(renderer, envMap);
  return envMap;
}

export function applyRealisticRenderer(engine, opts = {}) {
  const { renderer, quality } = engine;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = opts.exposure ?? 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  if (quality.shadows && opts.shadows !== false) {
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.shadowMap.needsUpdate = true;
  }
  if (opts.env !== false) {
    const env = buildEnvironmentTexture(renderer);
    engine.scene.environment = env;
    if (opts.envBackground) {
      engine.scene.background = env;
    }
  }
  return { envMap: engine.scene.environment };
}

export function realisticLights(scene, opts = {}) {
  const ambient = new THREE.AmbientLight(0xcfe0ff, opts.ambient ?? 0.18);
  const hemi = new THREE.HemisphereLight(0xbfd8ff, 0x2a1d12, opts.hemi ?? 0.45);
  const key = new THREE.DirectionalLight(0xfff4e0, opts.key ?? 2.4);
  key.position.set(opts.keyPos?.[0] ?? 6, opts.keyPos?.[1] ?? 11, opts.keyPos?.[2] ?? 7);
  if (opts.shadows !== false) {
    key.castShadow = true;
    key.shadow.mapSize.set(opts.shadowMap ?? 1024, opts.shadowMap ?? 1024);
    key.shadow.camera.near = 0.5;
    key.shadow.camera.far = 60;
    const s = opts.shadowArea ?? 18;
    key.shadow.camera.left = -s;
    key.shadow.camera.right = s;
    key.shadow.camera.top = s;
    key.shadow.camera.bottom = -s;
    key.shadow.bias = -0.0004;
    key.shadow.normalBias = 0.02;
    key.shadow.radius = opts.shadowRadius ?? 6;
  }
  const rim = new THREE.DirectionalLight(0x6fa8ff, opts.rim ?? 0.7);
  rim.position.set(-7, 5, -8);
  const fill = new THREE.DirectionalLight(0xff9a6a, opts.fill ?? 0.25);
  fill.position.set(3, -4, 9);
  scene.add(ambient, hemi, key, rim, fill);
  return { ambient, hemi, key, rim, fill };
}

export function makeContactShadow(scene, opts = {}) {
  const size = opts.size ?? 512;
  const c = document.createElement('canvas');
  c.width = size;
  c.height = size;
  const ctx = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  const mat = new THREE.MeshBasicMaterial({
    map: tex,
    transparent: true,
    opacity: 0.55,
    depthWrite: false,
    polygonOffset: true,
    polygonOffsetFactor: -2,
  });
  const radius = opts.radius ?? 8;
  const geo = new THREE.CircleGeometry(radius, 64);
  const mesh = new THREE.Mesh(geo, mat);
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = opts.y ?? 0.001;
  scene.add(mesh);
  let ctx_dirty = true;
  const blobs = [];
  function addBlob(x, z, r, alpha = 1) {
    blobs.push({ x, z, r, alpha });
    ctx_dirty = true;
  }
  function clearBlobs() {
    blobs.length = 0;
    ctx_dirty = true;
  }
  function setBlob(i, x, z, r, alpha) {
    if (i >= blobs.length) return;
    blobs[i].x = x; blobs[i].z = z; blobs[i].r = r; blobs[i].alpha = alpha;
    ctx_dirty = true;
  }
  function render() {
    if (!ctx_dirty) return;
    ctx_dirty = false;
    ctx.clearRect(0, 0, size, size);
    blobs.forEach((b) => {
      const cx = size / 2 + (b.x / radius) * (size / 2 - 4);
      const cy = size / 2 - (b.z / radius) * (size / 2 - 4);
      const cr = Math.max(2, (b.r / radius) * (size / 2));
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, cr);
      g.addColorStop(0, `rgba(8,14,28,${0.55 * b.alpha})`);
      g.addColorStop(0.5, `rgba(8,14,28,${0.3 * b.alpha})`);
      g.addColorStop(1, 'rgba(8,14,28,0)');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, size, size);
    });
    tex.needsUpdate = true;
  }
  return {
    mesh,
    tex,
    addBlob,
    clearBlobs,
    setBlob,
    setOpacity(v) { mat.opacity = v; },
    render,
    dispose() { geo.dispose(); mat.dispose(); tex.dispose(); },
  };
}

export function glassMaterial(opts = {}) {
  return new THREE.MeshPhysicalMaterial({
    color: opts.color ?? 0xffffff,
    roughness: opts.roughness ?? 0.06,
    metalness: 0,
    transmission: opts.transmission ?? 0.95,
    thickness: opts.thickness ?? 0.7,
    ior: opts.ior ?? 1.45,
    clearcoat: opts.clearcoat ?? 1,
    clearcoatRoughness: opts.clearcoatRoughness ?? 0.06,
    iridescence: opts.iridescence ?? 0,
    iridescenceIOR: 1.3,
    attenuationColor: opts.attenuationColor ?? 0xffffff,
    attenuationDistance: opts.attenuationDistance ?? 1.6,
    envMapIntensity: opts.envMapIntensity ?? 1.2,
    transparent: true,
    opacity: opts.opacity ?? 1,
  });
}

export function metalMaterial(opts = {}) {
  return new THREE.MeshPhysicalMaterial({
    color: opts.color ?? 0xbfc6d0,
    roughness: opts.roughness ?? 0.22,
    metalness: opts.metalness ?? 1,
    clearcoat: opts.clearcoat ?? 0.4,
    clearcoatRoughness: 0.18,
    envMapIntensity: opts.envMapIntensity ?? 1.4,
  });
}

export function polishedMaterial(opts = {}) {
  return new THREE.MeshPhysicalMaterial({
    color: opts.color ?? 0xffffff,
    roughness: opts.roughness ?? 0.35,
    metalness: opts.metalness ?? 0.15,
    clearcoat: opts.clearcoat ?? 1,
    clearcoatRoughness: opts.clearcoatRoughness ?? 0.08,
    envMapIntensity: opts.envMapIntensity ?? 1.2,
    emissive: opts.emissive ?? 0x000000,
    emissiveIntensity: opts.emissiveIntensity ?? 0,
  });
}

export function makeGlowTexture(inner, mid, outer) {
  const c = document.createElement('canvas');
  c.width = 256;
  c.height = 256;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
  g.addColorStop(0, inner);
  g.addColorStop(0.4, mid);
  g.addColorStop(1, outer);
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 256, 256);
  return new THREE.CanvasTexture(c);
}

export function makeRadialSprite(tex, opts = {}) {
  const mat = new THREE.SpriteMaterial({
    map: tex,
    color: opts.color ?? 0xffffff,
    transparent: true,
    depthWrite: false,
    blending: opts.additive !== false ? THREE.AdditiveBlending : THREE.NormalBlending,
    opacity: opts.opacity ?? 1,
  });
  const sprite = new THREE.Sprite(mat);
  const s = opts.scale ?? 1;
  sprite.scale.set(s, s, 1);
  return sprite;
}

export function disposeObject(obj) {
  obj.traverse((node) => {
    if (node.geometry) node.geometry.dispose();
    if (node.material) {
      const mats = Array.isArray(node.material) ? node.material : [node.material];
      mats.forEach((m) => {
        Object.keys(m).forEach((k) => { if (m[k] && m[k].isTexture) m[k].dispose(); });
        m.dispose();
      });
    }
  });
}

const ACTIVE_PARTICLES = [];

export function updateParticles(dt) {
  for (let i = ACTIVE_PARTICLES.length - 1; i >= 0; i--) {
    const p = ACTIVE_PARTICLES[i];
    p.life += dt;
    const f = Math.min(1, p.life / p.duration);
    const e = p.ease(f);
    p.objects.forEach((obj) => {
      const d = obj.userData._dis;
      obj.position.x = d.ox + d.dx * e;
      obj.position.y = d.oy + d.dy * e - p.gravity * p.life * p.life;
      obj.position.z = d.oz + d.dz * e;
      obj.rotation.x += d.spinX * dt;
      obj.rotation.y += d.spinY * dt;
      obj.rotation.z += d.spinZ * dt;
      if (p.fade && obj.material) {
        const o = Math.max(0, 1 - f) * d.startOpacity;
        obj.material.opacity = o;
        obj.material.transparent = true;
      }
      if (p.scaleBy && obj.scale) {
        const sc = p.scaleBy(f, d);
        obj.scale.setScalar(Math.max(0.001, sc));
      }
    });
    if (f >= 1) {
      if (p.onComplete) p.onComplete();
      ACTIVE_PARTICLES.splice(i, 1);
    }
  }
}

export function disintegrate(objects, opts = {}) {
  const speed = opts.speed ?? 1;
  const gravity = opts.gravity ?? 1.2;
  const spread = opts.spread ?? 6;
  const fade = opts.fade !== false;
  const scaleBy = opts.scaleBy || ((f) => Math.max(0, 1 - f));
  const pack = {
    objects,
    life: 0,
    duration: (opts.duration ?? 1.4) / speed,
    gravity,
    fade,
    scaleBy,
    ease: opts.ease || ((f) => f * (2 - f)),
    onComplete: opts.onComplete,
  };
  objects.forEach((obj) => {
    const ox = obj.position.x, oy = obj.position.y, oz = obj.position.z;
    const len = Math.hypot(ox, oy, oz) || 1;
    let dx, dy, dz;
    if (opts.radial && len > 0.05) {
      const rx = (ox / len) + (Math.random() - 0.5) * 0.7;
      const ry = (oy / len) + (Math.random() - 0.5) * 0.7 + 0.3;
      const rz = (oz / len) + (Math.random() - 0.5) * 0.7;
      const rl = Math.hypot(rx, ry, rz) || 1;
      dx = (rx / rl) * spread * (0.6 + Math.random() * 0.7);
      dy = (ry / rl) * spread * (0.6 + Math.random() * 0.7);
      dz = (rz / rl) * spread * (0.6 + Math.random() * 0.7);
    } else {
      dx = (Math.random() - 0.5) * spread * 2;
      dy = Math.random() * spread + 0.5;
      dz = (Math.random() - 0.5) * spread * 2;
    }
    const startOpacity = obj.material ? (obj.material.opacity ?? 1) : 1;
    obj.userData._dis = {
      ox, oy, oz, dx, dy, dz,
      spinX: (Math.random() - 0.5) * 8,
      spinY: (Math.random() - 0.5) * 8,
      spinZ: (Math.random() - 0.5) * 8,
      startOpacity,
    };
    if (obj.material && fade) obj.material.transparent = true;
  });
  ACTIVE_PARTICLES.push(pack);
  return pack;
}

export function stopParticlePack(pack) {
  const i = ACTIVE_PARTICLES.indexOf(pack);
  if (i >= 0) ACTIVE_PARTICLES.splice(i, 1);
}

export function isDisintegrating() {
  return ACTIVE_PARTICLES.length > 0;
}

export { buildEnvironmentTexture };
