import * as THREE from '../../vendor/three.module.min.js';
import { noise3D } from './noise3d.js';
import { liteScene } from './lite.js';

export { THREE };

export function detectQuality() {
  const smallViewport = Math.min(window.innerWidth, window.innerHeight) < 900;
  const mobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) || ((navigator.maxTouchPoints || 0) > 1 && smallViewport);
  const mem = navigator.deviceMemory || 4;
  const cores = navigator.hardwareConcurrency || 4;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const dpr = window.devicePixelRatio || 1;
  let tier = 'high';
  if (saveData || reducedMotion || (mobile && (mem <= 2 || cores <= 4))) tier = 'low';
  else if (mobile || mem <= 4 || cores <= 4) tier = 'medium';
  return {
    mobile,
    tier,
    pixelRatio: Math.min(dpr, tier === 'low' ? 1 : tier === 'medium' ? 1.5 : 2),
    // Drawing-buffer budget in pixels. A dense laptop panel at 2x asks for four times the pixels of
    // 1x for a difference the eye cannot see at arm's length; the budget keeps sharpness where it
    // shows and stops the GPU from shading pixels nobody resolves.
    maxPixels: tier === 'low' ? 0.9e6 : tier === 'medium' ? 1.6e6 : 2.6e6,
    // MSAA only where pixels are big enough for stair-steps to show.
    antialias: tier !== 'low' && dpr < 1.5,
    shadows: tier === 'high',
    segments: tier === 'low' ? 16 : tier === 'medium' ? 24 : 48,
    saveData,
    reducedMotion,
  };
}

// ---------------------------------------------------------------------------
// Cheaper soft shadows
// ---------------------------------------------------------------------------
// three's PCF and PCF-soft filters both read the shadow map 16-17 times per pixel per light. The
// depth texture is sampled with hardware comparison and bilinear filtering, so each read is already
// a 2x2 filtered test: four reads on a rotated grid give the same penumbra for a quarter of the cost.
let SHADOW_PATCHED = false;
function patchShadowFilter() {
  if (SHADOW_PATCHED) return;
  SHADOW_PATCHED = true;
  const chunk = THREE.ShaderChunk.shadowmap_pars_fragment;
  const a = chunk.indexOf('#if defined( SHADOWMAP_TYPE_PCF )');
  const b = a < 0 ? -1 : chunk.indexOf('#elif defined( SHADOWMAP_TYPE_VSM )', a);
  if (a < 0 || b < 0) return;
  THREE.ShaderChunk.shadowmap_pars_fragment = chunk.slice(0, a) + `#if defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_PCF_SOFT )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			#if defined( SHADOWMAP_TYPE_PCF_SOFT )
			vec2 k = texelSize;
			#else
			vec2 k = texelSize * max( shadowRadius * 0.6, 0.75 );
			#endif
			shadow = (
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( -0.5, -1.5 ) * k, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 1.5, -0.5 ) * k, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.5, 1.5 ) * k, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( -1.5, 0.5 ) * k, shadowCoord.z )
			) * 0.25;
		` + chunk.slice(b);
}

// ---------------------------------------------------------------------------
// Shared image-based lighting
// ---------------------------------------------------------------------------
// A single tiny equirect gradient is prefiltered once into a PMREM cubemap and reused by
// every simulation. Without it, MeshStandard/Physical materials have nothing to reflect,
// so metals read as flat grey and clearcoat/sheen contribute almost nothing. Cost is one
// prefilter pass at startup plus a single small cube map in GPU memory.
let ENV_TEXTURE = null;
let ENV_FAILED = false;

function buildEquirectGradient() {
  // A small photographic-studio environment: a cool sky dome, a warm floor bounce and three
  // softboxes (key, fill, rim). Prefiltered once, it gives every metal, glass and plastic in
  // every simulation believable reflections and soft image-based fill for a single cube map.
  const w = 128;
  const h = 64;
  const data = new Uint8Array(w * h * 4);
  const sky = [0.58, 0.66, 0.82];
  const horizon = [0.42, 0.45, 0.52];
  const ground = [0.16, 0.15, 0.15];
  const boxes = [
    { u: 0.30, v: 0.22, su: 0.07, sv: 0.06, k: 3.2, c: [1.0, 0.97, 0.92] },  // key, warm, upper front
    { u: 0.78, v: 0.30, su: 0.05, sv: 0.08, k: 1.3, c: [0.80, 0.88, 1.0] },  // fill, cool, side
    { u: 0.55, v: 0.12, su: 0.16, sv: 0.03, k: 1.6, c: [1.0, 1.0, 1.0] },    // overhead strip
  ];
  for (let y = 0; y < h; y++) {
    const v = y / (h - 1);
    for (let x = 0; x < w; x++) {
      const u = x / (w - 1);
      let r; let g; let b;
      if (v < 0.5) {
        const t = Math.pow(v / 0.5, 1.4);
        r = sky[0] + (horizon[0] - sky[0]) * t; g = sky[1] + (horizon[1] - sky[1]) * t; b = sky[2] + (horizon[2] - sky[2]) * t;
      } else {
        const t = Math.pow((v - 0.5) / 0.5, 0.6);
        r = horizon[0] + (ground[0] - horizon[0]) * t; g = horizon[1] + (ground[1] - horizon[1]) * t; b = horizon[2] + (ground[2] - horizon[2]) * t;
      }
      for (const box of boxes) {
        const du = Math.min(Math.abs(u - box.u), 1 - Math.abs(u - box.u)) / box.su;
        const dv = (v - box.v) / box.sv;
        // a rounded rectangle with a soft edge, like a diffuser panel
        const d = Math.pow(Math.pow(Math.abs(du), 4) + Math.pow(Math.abs(dv), 4), 0.25);
        const f = d < 1 ? 1 : Math.exp(-(d - 1) * (d - 1) * 6);
        r += box.k * box.c[0] * f; g += box.k * box.c[1] * f; b += box.k * box.c[2] * f;
      }
      const p = (y * w + x) * 4;
      data[p] = Math.min(255, Math.pow(r / (1 + r * 0.18), 1 / 1.0) * 255);
      data[p + 1] = Math.min(255, Math.pow(g / (1 + g * 0.18), 1 / 1.0) * 255);
      data[p + 2] = Math.min(255, Math.pow(b / (1 + b * 0.18), 1 / 1.0) * 255);
      data[p + 3] = 255;
    }
  }
  const tex = new THREE.DataTexture(data, w, h, THREE.RGBAFormat);
  tex.mapping = THREE.EquirectangularReflectionMapping;
  if (tex.colorSpace !== undefined) tex.colorSpace = THREE.SRGBColorSpace;
  tex.magFilter = THREE.LinearFilter;
  tex.needsUpdate = true;
  return tex;
}

export function getEnvironmentTexture(renderer) {
  if (ENV_TEXTURE || ENV_FAILED) return ENV_TEXTURE;
  try {
    const pmrem = new THREE.PMREMGenerator(renderer);
    const source = buildEquirectGradient();
    ENV_TEXTURE = pmrem.fromEquirectangular(source).texture;
    pmrem.dispose();
    source.dispose();
  } catch (e) {
    ENV_FAILED = true;
    ENV_TEXTURE = null;
  }
  return ENV_TEXTURE;
}

export function disposeEnvironment() {
  if (ENV_TEXTURE) ENV_TEXTURE.dispose();
  ENV_TEXTURE = null;
  ENV_FAILED = false;
}

// ---------------------------------------------------------------------------
// Cheap contact shadow
// ---------------------------------------------------------------------------
// A real shadow map costs a full extra render pass per light, which is not worth it on
// phones. A single soft blob under the bench reads as grounding contact occlusion for one
// draw call and no extra passes.
const CONTACT_CACHE = new Map();

export function makeContactShadow(opts = {}) {
  const size = opts.size || 256;
  const radius = opts.radius ?? 0.5;
  const key = `${size}:${radius}`;
  let texture = CONTACT_CACHE.get(key);
  if (!texture) {
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');
    const c = size / 2;
    const grad = ctx.createRadialGradient(c, c, 0, c, c, c);
    grad.addColorStop(0, 'rgba(0,0,0,0.85)');
    grad.addColorStop(radius, 'rgba(0,0,0,0.42)');
    grad.addColorStop(0.82, 'rgba(0,0,0,0.10)');
    grad.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, size, size);
    texture = new THREE.CanvasTexture(canvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    CONTACT_CACHE.set(key, texture);
  }
  const mesh = new THREE.Mesh(
    new THREE.PlaneGeometry(opts.width || 5.6, opts.depth || 4.0),
    new THREE.MeshBasicMaterial({
      map: texture,
      transparent: true,
      opacity: opts.opacity ?? 0.62,
      depthWrite: false,
      color: 0x000000,
      toneMapped: false,
    })
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.set(opts.x || 0, opts.y ?? 0.705, opts.z || 0);
  mesh.renderOrder = -1;
  mesh.name = 'contact-shadow';
  mesh.userData.sharedFx = true;
  mesh.userData.noBatch = true;
  mesh.userData.noScan = true;
  return mesh;
}

export function createEngine(stage, opts = {}) {
  const quality = opts.quality || detectQuality();
  patchShadowFilter();
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      antialias: opts.antialias ?? quality.antialias,
      alpha: opts.alpha !== false,
      powerPreference: quality.tier === 'low' ? 'default' : 'high-performance',
      stencil: false,
      depth: true,
      preserveDrawingBuffer: false,
      logarithmicDepthBuffer: !!opts.logDepth,
    });
  } catch (e) {
    showWebGLFallback(stage);
    return null;
  }
  renderer.setPixelRatio(quality.pixelRatio);
  if (renderer.outputColorSpace !== undefined && THREE.SRGBColorSpace) renderer.outputColorSpace = THREE.SRGBColorSpace;
  if (renderer.toneMapping !== undefined && THREE.ACESFilmicToneMapping) renderer.toneMapping = THREE.ACESFilmicToneMapping;
  if (renderer.toneMappingExposure !== undefined) renderer.toneMappingExposure = opts.exposure ?? 1.0;
  if (quality.shadows && opts.shadows) {
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  }
  if (opts.noise) noise3D(renderer);
  renderer.domElement.classList.add('ix-sim-canvas');
  stage.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  // Image-based light is on by default now: one prefiltered cube map shared by every sim, and
  // the difference between plastic that looks like plastic and plastic that looks like paint.
  if (opts.environment !== false) {
    const env = getEnvironmentTexture(renderer);
    if (env) scene.environment = env;
  }
  const camera = new THREE.PerspectiveCamera(
    opts.fov || 50,
    1,
    opts.near || 0.1,
    opts.far || 5000
  );

  let updateFn = null;
  let running = false;
  let visible = true;
  let pageVisible = !document.hidden;
  let rafId = 0;
  let disposed = false;
  const clock = new THREE.Clock();
  const resizeFns = [];

  const maxPixels = quality.maxPixels || 2.6e6;
  let ratio = quality.pixelRatio;
  let appliedRatio = 0;
  function resize() {
    const w = stage.clientWidth || 1;
    const h = stage.clientHeight || 1;
    const r = Math.max(0.5, Math.min(ratio, Math.sqrt(maxPixels / (w * h))));
    if (r !== appliedRatio) { appliedRatio = r; renderer.setPixelRatio(r); }
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';
    resizeFns.forEach((fn) => fn(w, h));
  }

  const ro = new ResizeObserver(() => resize());
  ro.observe(stage);
  resize();

  const io = new IntersectionObserver((entries) => {
    visible = entries[0] ? entries[0].isIntersecting : true;
    syncLoop();
  }, { threshold: 0.01 });
  io.observe(stage);

  function onVisibility() {
    pageVisible = !document.hidden;
    syncLoop();
  }
  document.addEventListener('visibilitychange', onVisibility);

  // Adaptive resolution. The governor learns the display's refresh interval, and when frames start
  // missing it (the GPU cannot keep up), it renders on fewer pixels in proportion to the overrun.
  // Once frames have been on time for a while it probes one step sharper; a probe that brings the
  // misses back is undone and the next probe waits twice as long. Low tier is capped at 30 fps.
  const maxRatio = quality.pixelRatio;
  const minRatio = Math.max(0.5, maxRatio * (quality.tier === 'high' ? 0.6 : 0.5));
  let refresh = 1000 / 60;
  let lastFrameAt = 0;
  let liteTick = 0;
  let winSum = 0; let winN = 0; let winMiss = 0;
  let onTime = 0; let probeFrom = 0; let probeAt = 0; let backoff = 4000; let since = 0;
  const frameInterval = quality.tier === 'low' ? 1000 / 31 : 0;
  function setRatio(r) {
    r = Math.round(Math.max(minRatio, Math.min(maxRatio, r)) * 20) / 20;
    if (r === ratio) return false;
    ratio = r; resize(); return true;
  }
  function govern(ms, now) {
    if (window.__ixNoGovern || ms > 250) return;
    if (ms > 4 && ms < refresh * 0.97 && !frameInterval) refresh = refresh * 0.9 + ms * 0.1;
    const budget = frameInterval || refresh;
    winSum += ms; winN += 1; if (ms > budget * 1.45) winMiss += 1;
    if (winN < 24) return;
    const avg = winSum / winN; const missRate = winMiss / winN;
    winSum = 0; winN = 0; winMiss = 0;
    if (missRate > 0.25 && avg > budget * 1.2) {
      onTime = 0;
      if (probeFrom && now - probeAt < 3000) { setRatio(probeFrom); backoff = Math.min(60000, backoff * 2); probeFrom = 0; since = now; return; }
      probeFrom = 0;
      setRatio(ratio * Math.max(0.7, Math.sqrt(budget / avg)));
      since = now;
    } else if (missRate < 0.05) {
      onTime += 1;
      if (probeFrom && now - probeAt > 3000) { probeFrom = 0; backoff = 4000; }
      if (!probeFrom && ratio < maxRatio && now - since > backoff) {
        const from = ratio;
        if (setRatio(ratio + 0.1)) { probeFrom = from; probeAt = now; since = now; }
      }
    } else onTime = 0;
  }

  // Shadow maps are re-rendered only when a caster, or the light, has moved. A lab bench where only
  // a pipette changes position pays for one shadow pass when the pipette moves, not sixty a second.
  let shadowSig = NaN;
  const sigCasters = [];
  function shadowSignature() {
    let sig = 0;
    sigCasters.length = 0;
    scene.traverseVisible((o) => { if (o.castShadow || o.isLight) sigCasters.push(o); });
    for (let i = 0; i < sigCasters.length; i++) {
      const o = sigCasters[i]; const e = o.matrixWorld.elements;
      sig += (e[0] + e[5] * 3 + e[10] * 5 + e[12] * 7 + e[13] * 11 + e[14] * 13 + e[1] * 17 + e[8] * 19) * (i + 1);
      if (o.isInstancedMesh) sig += o.instanceMatrix.version * 23 + o.count * 29;
      if (o.geometry) { const pa = o.geometry.attributes.position; sig += (o.geometry.id * 43 + (pa ? pa.version * 47 : 0) + (o.geometry.drawRange.count % 1e6) * 53) * (i + 1); }
      if (o.isLight && o.target) { const t = o.target.matrixWorld.elements; sig += (t[12] * 31 + t[13] * 37 + t[14] * 41) * (i + 1); }
      if (o.userData.dynamicShadow) sig += performance.now();
    }
    return sig + sigCasters.length * 1e-3;
  }
  function updateShadows() {
    const sm = renderer.shadowMap;
    if (!sm.enabled || opts.shadowCache === false) return;
    if (sm.autoUpdate) { sm.autoUpdate = false; sm.needsUpdate = true; shadowSig = NaN; return; }
    scene.updateMatrixWorld();
    const sig = shadowSignature();
    if (sig !== shadowSig) { shadowSig = sig; sm.needsUpdate = true; }
  }

  function frame(now) {
    rafId = requestAnimationFrame(frame);
    if (frameInterval && now - lastFrameAt < frameInterval) return;
    if (lastFrameAt) govern(now - lastFrameAt, now);
    lastFrameAt = now;
    const dt = Math.min(clock.getDelta(), 0.1);
    if (updateFn) updateFn(dt, clock.elapsedTime);
    if (opts.lite && (liteTick++ % 90 === 0)) liteScene(scene, { env: opts.envIntensity });
    updateShadows();
    renderer.render(scene, camera);
  }

  function syncLoop() {
    const shouldRun = running && visible && pageVisible && !disposed;
    if (shouldRun && !rafId) {
      clock.getDelta();
      lastFrameAt = 0;
      rafId = requestAnimationFrame(frame);
    } else if (!shouldRun && rafId) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  const api = {
    THREE,
    scene,
    camera,
    renderer,
    quality,
    canvas: renderer.domElement,
    setUpdate(fn) { updateFn = fn; },
    onResize(fn) { resizeFns.push(fn); fn(stage.clientWidth || 1, stage.clientHeight || 1); },
    start() { running = true; syncLoop(); },
    stop() { running = false; syncLoop(); },
    renderOnce() { updateShadows(); renderer.render(scene, camera); },
    get pixelRatio() { return appliedRatio; },
    dispose() {
      disposed = true;
      running = false;
      syncLoop();
      ro.disconnect();
      io.disconnect();
      document.removeEventListener('visibilitychange', onVisibility);
      scene.traverse((obj) => {
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) {
          const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
          mats.forEach((m) => {
            if (!m.userData?.scanGrade && !m.userData?.sharedFx) Object.keys(m).forEach((k) => { if (m[k] && m[k].isTexture) m[k].dispose(); });
            m.dispose();
          });
        }
      });
      renderer.dispose();
      if (renderer.domElement.parentNode) renderer.domElement.parentNode.removeChild(renderer.domElement);
      if (stage.__engine === api) delete stage.__engine;
    },
  };
  stage.__engine = api;
  return api;
}

export function createOrbitControls(camera, dom, opts = {}) {
  const target = opts.target ? opts.target.clone() : new THREE.Vector3(0, 0, 0);
  const spherical = new THREE.Spherical().setFromVector3(camera.position.clone().sub(target));
  const sphericalGoal = spherical.clone();
  const targetGoal = target.clone();
  const minDistance = opts.minDistance ?? 1;
  const maxDistance = opts.maxDistance ?? 100;
  const minPolar = opts.minPolar ?? 0.05;
  const maxPolar = opts.maxPolar ?? Math.PI - 0.05;
  const enablePan = opts.enablePan !== false;
  const damping = opts.damping ?? 0.12;
  let autoRotate = opts.autoRotate || 0;
  let enabled = true;

  const pointers = new Map();
  let pinchDist = 0;
  let panStart = null;

  function clampSpherical(s) {
    s.radius = Math.max(minDistance, Math.min(maxDistance, s.radius));
    s.phi = Math.max(minPolar, Math.min(maxPolar, s.phi));
  }

  function onPointerDown(e) {
    if (!enabled) return;
    dom.setPointerCapture && dom.setPointerCapture(e.pointerId);
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY, button: e.button });
    if (pointers.size === 2) {
      const pts = [...pointers.values()];
      pinchDist = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      panStart = { x: (pts[0].x + pts[1].x) / 2, y: (pts[0].y + pts[1].y) / 2 };
    }
    autoRotate = 0;
  }

  function onPointerMove(e) {
    if (!enabled || !pointers.has(e.pointerId)) return;
    const prev = pointers.get(e.pointerId);
    const dx = e.clientX - prev.x;
    const dy = e.clientY - prev.y;
    if (pointers.size === 1) {
      if (prev.button === 2 && enablePan) {
        pan(dx, dy);
      } else {
        sphericalGoal.theta -= dx * 0.0065;
        sphericalGoal.phi -= dy * 0.0065;
        clampSpherical(sphericalGoal);
      }
    } else if (pointers.size === 2) {
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY, button: prev.button });
      const pts = [...pointers.values()];
      const dist = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      if (pinchDist > 0) {
        sphericalGoal.radius *= pinchDist / Math.max(dist, 1);
        clampSpherical(sphericalGoal);
      }
      pinchDist = dist;
      const cx = (pts[0].x + pts[1].x) / 2;
      const cy = (pts[0].y + pts[1].y) / 2;
      if (panStart && enablePan) pan(cx - panStart.x, cy - panStart.y);
      panStart = { x: cx, y: cy };
      return;
    }
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY, button: prev.button });
  }

  function onPointerUp(e) {
    pointers.delete(e.pointerId);
    pinchDist = 0;
    panStart = null;
  }

  function pan(dx, dy) {
    const scale = sphericalGoal.radius * 0.0016;
    const offset = new THREE.Vector3();
    const te = camera.matrix.elements;
    offset.set(te[0], te[1], te[2]).multiplyScalar(-dx * scale);
    offset.add(new THREE.Vector3(te[4], te[5], te[6]).multiplyScalar(dy * scale));
    targetGoal.add(offset);
  }

  function onWheel(e) {
    if (!enabled) return;
    e.preventDefault();
    sphericalGoal.radius *= e.deltaY > 0 ? 1.1 : 0.9;
    clampSpherical(sphericalGoal);
  }

  function onContextMenu(e) { e.preventDefault(); }

  dom.style.touchAction = 'none';
  dom.addEventListener('pointerdown', onPointerDown);
  dom.addEventListener('pointermove', onPointerMove);
  dom.addEventListener('pointerup', onPointerUp);
  dom.addEventListener('pointercancel', onPointerUp);
  dom.addEventListener('wheel', onWheel, { passive: false });
  dom.addEventListener('contextmenu', onContextMenu);

  return {
    get target() { return target; },
    set enabled(v) { enabled = v; },
    get enabled() { return enabled; },
    setAutoRotate(speed) { autoRotate = speed; },
    setTarget(v) { targetGoal.copy(v); },
    setDistance(d) { sphericalGoal.radius = d; clampSpherical(sphericalGoal); },
    setView(position, newTarget = targetGoal) {
      target.copy(newTarget);
      targetGoal.copy(newTarget);
      spherical.setFromVector3(position.clone().sub(newTarget));
      sphericalGoal.copy(spherical);
      clampSpherical(spherical);
      clampSpherical(sphericalGoal);
      camera.position.copy(position);
      camera.lookAt(target);
    },
    update(dt) {
      if (autoRotate) sphericalGoal.theta += autoRotate * (dt || 0.016);
      const t = 1 - Math.pow(1 - damping, (dt || 0.016) * 60);
      spherical.radius += (sphericalGoal.radius - spherical.radius) * t;
      spherical.theta += (sphericalGoal.theta - spherical.theta) * t;
      spherical.phi += (sphericalGoal.phi - spherical.phi) * t;
      target.lerp(targetGoal, t);
      camera.position.setFromSpherical(spherical).add(target);
      camera.lookAt(target);
    },
    dispose() {
      dom.removeEventListener('pointerdown', onPointerDown);
      dom.removeEventListener('pointermove', onPointerMove);
      dom.removeEventListener('pointerup', onPointerUp);
      dom.removeEventListener('pointercancel', onPointerUp);
      dom.removeEventListener('wheel', onWheel);
      dom.removeEventListener('contextmenu', onContextMenu);
    },
  };
}

export function basicLights(scene, opts = {}) {
  const ambient = new THREE.AmbientLight(0xffffff, opts.ambient ?? 0.55);
  const key = new THREE.DirectionalLight(0xffffff, opts.key ?? 1.6);
  key.position.set(opts.keyPos?.[0] ?? 5, opts.keyPos?.[1] ?? 10, opts.keyPos?.[2] ?? 7);
  const fill = new THREE.DirectionalLight(0xbfd4ff, opts.fill ?? 0.5);
  fill.position.set(-6, 4, -6);
  const added = [ambient, key, fill];
  let rim = null;
  // Opt-in only: existing simulations keep their current lighting unless they ask for a rim.
  if (opts.rim) {
    rim = new THREE.DirectionalLight(opts.rimColor ?? 0xbcd7ff, opts.rim);
    rim.position.set(opts.rimPos?.[0] ?? -4, opts.rimPos?.[1] ?? 5.5, opts.rimPos?.[2] ?? -8);
    added.push(rim);
  }
  scene.add(...added);
  return { ambient, key, fill, rim };
}

export function showWebGLFallback(stage) {
  const div = document.createElement('div');
  div.className = 'ix-sim-fallback';
  div.innerHTML = '<span class="material-symbols-outlined">view_in_ar</span>' +
    '<h3>3D not supported here</h3>' +
    '<p>Your browser or device cannot show 3D graphics. Try updating your browser or opening this page on another device — the written lesson below still works!</p>';
  stage.appendChild(div);
}

// Label textures are pure functions of (text, style) and a model rebuild recreates every
// label, so they are cached and shared. Without this, each slider step re-uploaded a dozen
// or more canvas textures to the GPU.
const LABEL_CACHE = new Map();
const LABEL_CACHE_MAX = 96;

export function makeLabelSprite(text, opts = {}) {
  const fontSize = opts.fontSize || 44;
  const weight = opts.weight || 600;
  const bg = opts.bg === false ? '' : (opts.bg || 'rgba(11,28,48,0.82)');
  const color = opts.color || '#ffffff';
  const key = `${text}|${fontSize}|${weight}|${bg}|${color}`;

  let entry = LABEL_CACHE.get(key);
  if (!entry) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const font = `${weight} ${fontSize}px Poppins, system-ui, sans-serif`;
    ctx.font = font;
    const padX = 28;
    const padY = 18;
    const w = Math.ceil(ctx.measureText(text).width) + padX * 2;
    const h = fontSize + padY * 2;
    canvas.width = w;
    canvas.height = h;
    // Resizing the canvas resets its context state, so restyle after both dimensions are set.
    const c2 = canvas.getContext('2d');
    if (opts.bg !== false) {
      c2.fillStyle = bg;
      c2.beginPath();
      if (c2.roundRect) c2.roundRect(0, 0, w, h, h / 2);
      else c2.rect(0, 0, w, h);
      c2.fill();
    }
    c2.font = font;
    c2.fillStyle = color;
    c2.textAlign = 'center';
    c2.textBaseline = 'middle';
    c2.fillText(text, w / 2, h / 2);
    const texture = new THREE.CanvasTexture(canvas);
    texture.anisotropy = 4;
    if (texture.colorSpace !== undefined) texture.colorSpace = THREE.SRGBColorSpace;
    texture.needsUpdate = true;
    const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false });
    material.userData.sharedFx = true;
    entry = { material, aspect: w / h };
    if (LABEL_CACHE.size >= LABEL_CACHE_MAX) {
      LABEL_CACHE.forEach((e) => { e.material.map.dispose(); e.material.dispose(); });
      LABEL_CACHE.clear();
    }
    LABEL_CACHE.set(key, entry);
  }

  const sprite = new THREE.Sprite(entry.material);
  sprite.userData.sharedFx = true;
  const scale = opts.scale || 1;
  sprite.scale.set(entry.aspect * scale, scale, 1);
  return sprite;
}

// Soft round sprite used for signal particles. Square GL points read as cheap artefacts;
// a single cached radial gradient makes them look like glowing emitters for no extra cost.
let DOT_TEXTURE = null;

export function getSoftDotTexture() {
  if (DOT_TEXTURE) return DOT_TEXTURE;
  const size = 64;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const c = size / 2;
  const grad = ctx.createRadialGradient(c, c, 0, c, c, c);
  grad.addColorStop(0, 'rgba(255,255,255,1)');
  grad.addColorStop(0.28, 'rgba(255,255,255,0.92)');
  grad.addColorStop(0.62, 'rgba(255,255,255,0.30)');
  grad.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  DOT_TEXTURE = new THREE.CanvasTexture(canvas);
  if (DOT_TEXTURE.colorSpace !== undefined) DOT_TEXTURE.colorSpace = THREE.SRGBColorSpace;
  DOT_TEXTURE.needsUpdate = true;
  DOT_TEXTURE.userData = { sharedFx: true };
  return DOT_TEXTURE;
}

export function makeSignalPoints(max, opts = {}) {
  const position = new Float32Array(max * 3);
  const color = new Float32Array(max * 3);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(position, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(color, 3));
  geo.setDrawRange(0, 0);
  geo.boundingSphere = new THREE.Sphere(new THREE.Vector3(), opts.radius || 1e4);
  const mat = new THREE.PointsMaterial({
    size: opts.size || 0.2,
    vertexColors: true,
    map: getSoftDotTexture(),
    transparent: true,
    opacity: opts.opacity ?? 0.95,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
    toneMapped: false,
  });
  mat.userData.sharedFx = true;
  const points = new THREE.Points(geo, mat);
  points.frustumCulled = false;
  points.userData.sharedFx = true;
  return { points, geo, mat, position, color };
}

export function disposeLabelCache() {
  LABEL_CACHE.forEach((e) => { e.material.map.dispose(); e.material.dispose(); });
  LABEL_CACHE.clear();
}
