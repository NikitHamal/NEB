// The AI studio: a deep blue sweep, a dark satin floor with a faint glowing grid that fades into
// the distance, soft key light with shadows. Plus the pieces the AI labs share: slab cards with
// crisp canvas text on the face, a pointer drag that grabs real meshes, and camera framing that
// keeps the subject clear of the docked panel. 1 unit ≈ 10 cm of desk.
import { THREE, createEngine, createOrbitControls } from '../../core/engine.js';

export { THREE };

export function createStudio(stage, { camera = [0, 6, 9], target = [0, 0.5, 0], minDistance = 3, maxDistance = 30, floor = 14 } = {}) {
  const engine = createEngine(stage, { shadows: true, environment: true, exposure: 1.05 });
  if (!engine) return null;
  const { scene, quality, renderer } = engine;
  const cam = engine.camera;
  cam.position.set(...camera);
  const controls = createOrbitControls(cam, engine.canvas, { minDistance, maxDistance, target: new THREE.Vector3(...target), maxPolar: 1.45 });

  scene.background = new THREE.Color(0x0a0f24);
  scene.fog = new THREE.Fog(0x0a0f24, floor * 1.2, floor * 3.2);
  scene.add(new THREE.Mesh(new THREE.SphereGeometry(90, 32, 16), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'varying vec3 vP; void main(){ float t = clamp(vP.y * 0.5 + 0.5, 0.0, 1.0); vec3 c = mix(vec3(0.03, 0.04, 0.11), vec3(0.13, 0.14, 0.32), pow(t, 1.4)); gl_FragColor = vec4(c, 1.0); }',
  })));

  const floorMat = new THREE.MeshStandardMaterial({ color: 0x11162c, roughness: 0.62, metalness: 0 });
  floorMat.onBeforeCompile = (sh) => {
    sh.vertexShader = 'varying vec3 vW;\n' + sh.vertexShader.replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvW = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = 'varying vec3 vW;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
      vec2 g = abs(fract(vW.xz - 0.5) - 0.5) / fwidth(vW.xz);
      float line = 1.0 - min(min(g.x, g.y), 1.0);
      float fade = exp(-dot(vW.xz, vW.xz) / ${(floor * floor * 0.2).toFixed(1)});
      totalEmissiveRadiance += vec3(0.20, 0.28, 0.75) * line * fade * 0.2;`);
  };
  const ground = new THREE.Mesh(new THREE.CircleGeometry(floor * 3, 96), floorMat);
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

  scene.add(new THREE.HemisphereLight(0xc7d2fe, 0x1e1b4b, 0.7));
  const key = new THREE.DirectionalLight(0xffffff, 2.0); key.position.set(5, 12, 7);
  if (quality.shadows) {
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    key.castShadow = true; key.shadow.mapSize.set(quality.tier === 'high' ? 2048 : 1024, quality.tier === 'high' ? 2048 : 1024);
    const c = key.shadow.camera; c.left = -floor * 0.6; c.right = floor * 0.6; c.top = floor * 0.6; c.bottom = -floor * 0.6; c.near = 1; c.far = 40;
    key.shadow.bias = -0.0005; key.shadow.normalBias = 0.02;
  }
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x8b9cff, 0.9); rim.position.set(-7, 5, -9); scene.add(rim);

  return { engine, scene, camera: cam, controls, quality, key };
}

/**
 * Keep a subject `width` units wide (and `height` tall) in view beside the panel that docks on
 * the right of wide screens. Call every frame; it only acts when the stage width changes.
 */
export function framer(stage, camera, controls, { width, height = width * 0.5, center = [0, 0, 0], panel = 310, maxDistance = 40 }) {
  let lastW = 0; const t = new THREE.Vector3();
  return function fit(force) {
    const W = stage.clientWidth;
    if ((W === lastW && !force) || !W) return;
    lastW = W;
    const avail = W > 760 ? W - panel : W, total = width * W / avail;
    const half = Math.tan(camera.fov * Math.PI / 360);
    controls.setDistance(Math.min(maxDistance, Math.max(total / 2 / half / camera.aspect, height / 2 / half)));
    controls.setTarget(t.set(center[0] + (W - avail) / 2 / W * total, center[1], center[2]));
  };
}

function roundRect(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r);
  s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}

/**
 * A card: a thin bevelled slab with a canvas-drawn face. `draw(g, W, H)` paints the face in
 * canvas pixels (`res` per unit); call `card.redraw()` after changing what it shows.
 */
export function slabCard({ w = 2, h = 0.8, depth = 0.06, radius = 0.12, color = 0xf8fafc, res = 256, draw }) {
  const geo = new THREE.ExtrudeGeometry(roundRect(w, h, radius), { depth, bevelEnabled: true, bevelSize: 0.015, bevelThickness: 0.015, bevelSegments: 2, curveSegments: 8 });
  geo.translate(0, 0, -depth / 2);
  const body = new THREE.MeshPhysicalMaterial({ color, roughness: 0.35, clearcoat: 0.4, clearcoatRoughness: 0.3 });
  const mesh = new THREE.Mesh(geo, body); mesh.castShadow = true;
  const cv = document.createElement('canvas'); cv.width = Math.round(w * res); cv.height = Math.round(h * res);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const faceMat = new THREE.MeshStandardMaterial({ map: tex, transparent: true, roughness: 0.5, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
  const faceGeo = new THREE.ShapeGeometry(roundRect(w, h, radius), 8);
  const uv = faceGeo.attributes.uv, pos = faceGeo.attributes.position;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, pos.getX(i) / w + 0.5, pos.getY(i) / h + 0.5);
  const face = new THREE.Mesh(faceGeo, faceMat); face.position.z = depth / 2 + 0.016; mesh.add(face);
  const card = {
    mesh, body, face, w, h,
    redraw() { const g = cv.getContext('2d'); g.clearRect(0, 0, cv.width, cv.height); if (draw) draw(g, cv.width, cv.height); tex.needsUpdate = true; },
    dispose() { geo.dispose(); body.dispose(); faceGeo.dispose(); faceMat.dispose(); tex.dispose(); },
  };
  card.redraw();
  return card;
}

/** Wraps `text` into lines no wider than `maxW` in the current font; returns the lines. */
export function wrapLines(g, text, maxW) {
  const out = []; let line = '';
  for (const word of text.split(' ')) { const t = line ? `${line} ${word}` : word; if (g.measureText(t).width > maxW && line) { out.push(line); line = word; } else line = t; }
  if (line) out.push(line);
  return out;
}

/**
 * Pointer drag of real meshes: `objects()` lists what can be grabbed (raycast against them), the
 * pointer is projected onto `plane` while dragging. `onDown(obj, point)` may return false to
 * refuse. Taps that do not move call `onTap(obj | null, point)`.
 */
export function meshDrag(dom, camera, controls, { objects, plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), onDown, onMove, onUp, onTap }) {
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), hit = new THREE.Vector3();
  let active = null, start = null, moved = false;
  function setRay(e) { const r = dom.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); }
  function toPlane() { return ray.ray.intersectPlane(plane, hit) ? hit : null; }
  function pick() {
    const list = objects(); const hits = ray.intersectObjects(list, true);
    if (!hits.length) return null;
    let o = hits[0].object; while (o && !list.includes(o)) o = o.parent;
    return o;
  }
  function down(e) {
    setRay(e); start = [e.clientX, e.clientY]; moved = false;
    const o = pick();
    if (!o) return;
    if (onDown && onDown(o, toPlane()) === false) return;
    active = o; controls.enabled = false; e.stopImmediatePropagation();
    dom.setPointerCapture && dom.setPointerCapture(e.pointerId);
  }
  function move(e) {
    setRay(e);
    if (start && Math.hypot(e.clientX - start[0], e.clientY - start[1]) > 5) moved = true;
    if (!active) { dom.style.cursor = pick() ? 'grab' : ''; return; }
    dom.style.cursor = 'grabbing';
    const p = toPlane(); if (p && onMove) onMove(active, p);
  }
  function up(e) {
    setRay(e);
    if (!moved && onTap && start) onTap(active || pick(), toPlane());
    if (active) { if (onUp) onUp(active, toPlane()); active = null; controls.enabled = true; dom.style.cursor = ''; }
    start = null;
  }
  dom.addEventListener('pointerdown', down, true);
  dom.addEventListener('pointermove', move);
  dom.addEventListener('pointerup', up);
  dom.addEventListener('pointercancel', up);
  return { get active() { return active; }, dispose() { dom.removeEventListener('pointerdown', down, true); dom.removeEventListener('pointermove', move); dom.removeEventListener('pointerup', up); dom.removeEventListener('pointercancel', up); } };
}
