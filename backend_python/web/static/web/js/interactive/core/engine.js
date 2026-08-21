import * as THREE from '../../vendor/three.module.min.js';

export { THREE };

export function detectQuality() {
  const smallViewport = Math.min(window.innerWidth, window.innerHeight) < 900;
  const mobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) || ((navigator.maxTouchPoints || 0) > 1 && smallViewport);
  const mem = navigator.deviceMemory || 4;
  const cores = navigator.hardwareConcurrency || 4;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let tier = 'high';
  if (saveData || reducedMotion || (mobile && (mem <= 2 || cores <= 4))) tier = 'low';
  else if (mobile || mem <= 4 || cores <= 4) tier = 'medium';
  return {
    mobile,
    tier,
    pixelRatio: Math.min(window.devicePixelRatio || 1, tier === 'low' ? 1 : tier === 'medium' ? 1.5 : 2),
    antialias: tier !== 'low',
    shadows: tier === 'high',
    segments: tier === 'low' ? 16 : tier === 'medium' ? 24 : 48,
    saveData,
    reducedMotion,
  };
}

export function createEngine(stage, opts = {}) {
  const quality = opts.quality || detectQuality();
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      antialias: quality.antialias,
      alpha: opts.alpha !== false,
      powerPreference: quality.tier === 'low' ? 'default' : 'high-performance',
      stencil: false,
      depth: true,
      preserveDrawingBuffer: false,
    });
  } catch (e) {
    showWebGLFallback(stage);
    return null;
  }
  renderer.setPixelRatio(quality.pixelRatio);
  if (renderer.outputColorSpace !== undefined && THREE.SRGBColorSpace) renderer.outputColorSpace = THREE.SRGBColorSpace;
  if (renderer.toneMapping !== undefined && THREE.ACESFilmicToneMapping) renderer.toneMapping = THREE.ACESFilmicToneMapping;
  if (quality.shadows && opts.shadows) {
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  }
  renderer.domElement.classList.add('ix-sim-canvas');
  stage.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
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

  function resize() {
    const w = stage.clientWidth || 1;
    const h = stage.clientHeight || 1;
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

  function frame() {
    rafId = requestAnimationFrame(frame);
    const dt = Math.min(clock.getDelta(), 0.1);
    if (updateFn) updateFn(dt, clock.elapsedTime);
    renderer.render(scene, camera);
  }

  function syncLoop() {
    const shouldRun = running && visible && pageVisible && !disposed;
    if (shouldRun && !rafId) {
      clock.getDelta();
      rafId = requestAnimationFrame(frame);
    } else if (!shouldRun && rafId) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  return {
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
    renderOnce() { renderer.render(scene, camera); },
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
    },
  };
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
  scene.add(ambient, key, fill);
  return { ambient, key, fill };
}

export function showWebGLFallback(stage) {
  const div = document.createElement('div');
  div.className = 'ix-sim-fallback';
  div.innerHTML = '<span class="material-symbols-outlined">view_in_ar</span>' +
    '<h3>3D not supported here</h3>' +
    '<p>Your browser or device cannot show 3D graphics. Try updating your browser or opening this page on another device — the written lesson below still works!</p>';
  stage.appendChild(div);
}

export function makeLabelSprite(text, opts = {}) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const font = `${opts.weight || 600} ${opts.fontSize || 44}px Poppins, system-ui, sans-serif`;
  ctx.font = font;
  const padX = 28;
  const padY = 18;
  const w = Math.ceil(ctx.measureText(text).width) + padX * 2;
  const h = (opts.fontSize || 44) + padY * 2;
  canvas.width = w;
  canvas.height = h;
  const c2 = canvas.getContext('2d');
  if (opts.bg !== false) {
    c2.fillStyle = opts.bg || 'rgba(11,28,48,0.82)';
    c2.beginPath();
    if (c2.roundRect) c2.roundRect(0, 0, w, h, h / 2);
    else c2.rect(0, 0, w, h);
    c2.fill();
  }
  c2.font = font;
  c2.fillStyle = opts.color || '#ffffff';
  c2.textAlign = 'center';
  c2.textBaseline = 'middle';
  c2.fillText(text, w / 2, h / 2);
  const texture = new THREE.CanvasTexture(canvas);
  texture.anisotropy = 2;
  const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false });
  const sprite = new THREE.Sprite(material);
  const scale = opts.scale || 1;
  sprite.scale.set((w / h) * scale, scale, 1);
  return sprite;
}
