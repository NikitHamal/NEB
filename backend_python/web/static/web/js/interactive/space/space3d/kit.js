import { THREE, createEngine, createOrbitControls } from '../../core/engine.js';
import { createMilkySky } from '../cosmos/milky.js';
import { createSkyBackground } from '../cosmos/stars.js';
import { PLANETS } from '../cosmos/astro.js';
import { litPlanet, ringMesh } from '../cosmos/solar.js';
import { createStar } from '../stars3d/star.js';

// Shared pieces for the space labs in 3D: a stage with the real Milky Way behind it, a Sun from the
// stellar-surface shader, planets with the same procedural surfaces as Scale of the Universe, fading
// trails, arrows and dragging on the orbital plane.
export function createSpace(stage, opts = {}) {
  stage.classList.add('ix-cosmos-stage');
  const engine = createEngine(stage, { noise: true, alpha: false, environment: false, fov: opts.fov || 40, near: 0.01, far: 2e5 });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  scene.background = new THREE.Color(0x000000);
  renderer.setClearColor(0x000000, 1);
  const sky = new THREE.Group();
  sky.add(createMilkySky(quality), createSkyBackground(quality));
  scene.add(sky);
  const p = opts.camera || [0, 6, 10];
  camera.position.set(p[0], p[1], p[2]);
  const controls = createOrbitControls(camera, engine.canvas, { target: new THREE.Vector3(...(opts.target || [0, 0, 0])), minDistance: opts.minDistance ?? 1, maxDistance: opts.maxDistance ?? 200, damping: 0.1, maxPolar: opts.maxPolar });
  scene.add(new THREE.AmbientLight(0x30384a, 0.6));
  const sunLight = new THREE.PointLight(0xfff2e0, 3.2, 0, 0);
  scene.add(sunLight);
  return { engine, scene, camera, renderer, quality, controls, sky, sunLight };
}

export function makeSun(quality, radius = 0.3) {
  const s = createStar(quality);
  s.group.scale.setScalar(radius);
  s.haloUniforms.uGlow.value = 1.4;
  return s;
}

export function makePlanet(id, radius = 0.12) {
  const p = PLANETS.find((x) => x.id === id) || PLANETS[2];
  const m = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 24), litPlanet(p));
  m.scale.setScalar(radius);
  if (id === 'saturn') m.add(ringMesh(1.24, 2.27));
  return m;
}

// A trail that fades from head to tail: a ring buffer of points drawn as one line with per-vertex alpha.
export function makeTrail(max, color) {
  const pos = new Float32Array(max * 3); const a = new Float32Array(max);
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('alpha', new THREE.BufferAttribute(a, 1));
  g.setDrawRange(0, 0);
  const mat = new THREE.ShaderMaterial({
    uniforms: { uC: { value: new THREE.Color(color) }, uK: { value: 1 } },
    vertexShader: 'attribute float alpha; varying float vA; void main() { vA = alpha; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform vec3 uC; uniform float uK; varying float vA; void main() { gl_FragColor = vec4(uC * vA * uK, 1.0); }',
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  const line = new THREE.Line(g, mat);
  line.frustumCulled = false;
  const xs = []; let n = 0;
  return {
    line, mat,
    clear() { n = 0; xs.length = 0; g.setDrawRange(0, 0); },
    push(x, y, z) {
      xs.push(x, y, z); if (xs.length > max * 3) xs.splice(0, 3);
      n = xs.length / 3;
      for (let i = 0; i < n; i++) { pos[i * 3] = xs[i * 3]; pos[i * 3 + 1] = xs[i * 3 + 1]; pos[i * 3 + 2] = xs[i * 3 + 2]; a[i] = Math.pow(i / Math.max(1, n - 1), 1.6); }
      g.attributes.position.needsUpdate = true; g.attributes.alpha.needsUpdate = true;
      g.setDrawRange(0, n);
    },
    set(points) {
      n = Math.min(max, points.length / 3);
      for (let i = 0; i < n; i++) { pos[i * 3] = points[i * 3]; pos[i * 3 + 1] = points[i * 3 + 1]; pos[i * 3 + 2] = points[i * 3 + 2]; a[i] = 1; }
      g.attributes.position.needsUpdate = true; g.attributes.alpha.needsUpdate = true;
      g.setDrawRange(0, n);
    },
    dispose() { g.dispose(); mat.dispose(); },
  };
}

export function makeArrow(color, shaft = 0.012) {
  const mat = new THREE.MeshBasicMaterial({ color, toneMapped: false });
  const group = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CylinderGeometry(shaft, shaft, 1, 10), mat);
  const head = new THREE.Mesh(new THREE.ConeGeometry(shaft * 3.2, shaft * 9, 14), mat);
  group.add(body, head);
  const up = new THREE.Vector3(0, 1, 0); const d = new THREE.Vector3();
  return {
    group,
    set(from, vec) {
      const L = vec.length();
      group.visible = L > 1e-4;
      if (!group.visible) return;
      group.position.copy(from);
      group.quaternion.setFromUnitVectors(up, d.copy(vec).divideScalar(L));
      const hl = Math.min(shaft * 9, L * 0.5);
      body.scale.y = Math.max(1e-4, L - hl); body.position.y = (L - hl) / 2;
      head.scale.setScalar(hl / (shaft * 9)); head.position.y = L - hl / 2;
    },
    dispose() { body.geometry.dispose(); head.geometry.dispose(); mat.dispose(); },
  };
}

// Pointer helpers on a plane (default the orbital plane y = 0): hit-test handles, drag along the plane.
export function planeDrag(dom, camera, controls, { plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), handles, onDown, onMove, onUp, onEmpty }) {
  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const hit = new THREE.Vector3();
  let active = null;
  function toPlane(e) {
    const r = dom.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    return ray.ray.intersectPlane(plane, hit) ? hit : null;
  }
  function pick(e) {
    const r = dom.getBoundingClientRect(); const v = new THREE.Vector3();
    let best = null; let bd = (e.pointerType === 'touch' ? 34 : 20);
    for (const h of handles()) {
      v.copy(h.pos).project(camera);
      const x = (v.x + 1) / 2 * r.width + r.left; const y = (1 - v.y) / 2 * r.height + r.top;
      const d = Math.hypot(x - e.clientX, y - e.clientY);
      if (d < bd && v.z < 1) { bd = d; best = h; }
    }
    return best;
  }
  function down(e) {
    const h = pick(e);
    if (h) {
      active = h; controls.enabled = false; dom.setPointerCapture && dom.setPointerCapture(e.pointerId);
      e.stopImmediatePropagation();
      const p = toPlane(e); if (onDown) onDown(h, p);
    } else if (onEmpty) {
      const p = toPlane(e); if (p && onEmpty(p, e)) { active = { empty: true }; controls.enabled = false; e.stopImmediatePropagation(); }
    }
  }
  function move(e) {
    if (!active) { const h = pick(e); dom.style.cursor = h ? 'grab' : ''; return; }
    const p = toPlane(e); if (p && onMove) onMove(active, p);
  }
  function up() { if (active) { if (onUp) onUp(active); active = null; controls.enabled = true; } }
  dom.addEventListener('pointerdown', down, true);
  dom.addEventListener('pointermove', move);
  dom.addEventListener('pointerup', up);
  dom.addEventListener('pointercancel', up);
  return { dispose() { dom.removeEventListener('pointerdown', down, true); dom.removeEventListener('pointermove', move); dom.removeEventListener('pointerup', up); dom.removeEventListener('pointercancel', up); } };
}

export function canvasCard(parent, aspect = 1.4) {
  const wrap = document.createElement('div');
  wrap.style.cssText = `position:relative;width:100%;aspect-ratio:${aspect};border-radius:14px;overflow:hidden;background:rgba(8,14,30,0.85);border:1px solid rgba(160,190,255,0.16);margin:4px 0 10px;flex-shrink:0`;
  const cv = document.createElement('canvas');
  cv.style.cssText = 'width:100%;height:100%;display:block';
  wrap.appendChild(cv); parent.appendChild(wrap);
  return {
    el: wrap,
    ctx() {
      const w = wrap.clientWidth || 260; const h = wrap.clientHeight || 180; const dpr = Math.min(2, window.devicePixelRatio || 1);
      if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
      const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
      return { g, w, h };
    },
  };
}
