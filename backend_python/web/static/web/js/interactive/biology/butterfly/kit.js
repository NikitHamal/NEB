import { THREE } from '../../core/engine.js';

export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a, b, t) => a + (b - a) * t;
export const smooth = (t) => { const x = clamp(t); return x * x * (3 - 2 * x); };
export const easeInOut = (t) => { const x = clamp(t); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
export const damp = (a, b, lambda, dt) => a + (b - a) * (1 - Math.exp(-lambda * dt));

export function rng(seed = 1) {
  let s = seed >>> 0;
  return () => {
    s += 0x6d2b79f5;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function makeCanvas(w, h = w) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return c;
}

export function canvasTexture(canvas, opts = {}) {
  const tex = new THREE.CanvasTexture(canvas);
  if (opts.color !== false) tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = opts.anisotropy ?? 4;
  if (opts.repeat) { tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(opts.repeat, opts.repeat); }
  tex.needsUpdate = true;
  return tex;
}

export function texSize(tier, high = 1024) {
  return tier === 'high' ? high : tier === 'medium' ? high / 2 : high / 4;
}

// Shared patch hook: a different map on the back face (leaf and wing undersides), light passing
// through thin tissue when the sun is behind it, and optional vertex/fragment injections.
export const sunUniforms = {
  uSunDir: { value: new THREE.Vector3(0, 1, 0) },
  uSunColor: { value: new THREE.Color(1, 0.95, 0.85) },
};
const tmpV = new THREE.Vector3();
export function updateSunUniforms(camera, sunWorldDir, color, intensity = 1) {
  tmpV.copy(sunWorldDir).normalize().transformDirection(camera.matrixWorldInverse);
  sunUniforms.uSunDir.value.copy(tmpV);
  if (color) sunUniforms.uSunColor.value.copy(color).multiplyScalar(intensity);
}

export function patchMaterial(material, opts = {}) {
  const extra = {};
  if (opts.backMap) extra.backMap = { value: opts.backMap };
  if (opts.translucency) {
    extra.uTrans = { value: opts.translucency };
    extra.uTransTint = { value: new THREE.Color(opts.transTint ?? 0xb8e070) };
  }
  Object.assign(extra, opts.uniforms || {});
  material.userData.extraUniforms = extra;
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, extra);
    if (opts.translucency) Object.assign(shader.uniforms, sunUniforms);
    let decl = '';
    if (opts.backMap) decl += 'uniform sampler2D backMap;\n';
    if (opts.translucency) decl += 'uniform float uTrans;\nuniform vec3 uTransTint;\nuniform vec3 uSunDir;\nuniform vec3 uSunColor;\n';
    if (opts.fragDecl) decl += opts.fragDecl;
    shader.fragmentShader = decl + shader.fragmentShader;
    if (opts.backMap && !opts.fragMap) {
      shader.fragmentShader = shader.fragmentShader.replace('#include <map_fragment>',
        '#ifdef USE_MAP\n vec4 sampledDiffuseColor = gl_FrontFacing ? texture2D( map, vMapUv ) : texture2D( backMap, vMapUv );\n diffuseColor *= sampledDiffuseColor;\n#endif');
    }
    if (opts.fragMap) shader.fragmentShader = shader.fragmentShader.replace('#include <map_fragment>', opts.fragMap);
    if (opts.translucency) {
      shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_end>',
        '#include <lights_fragment_end>\n float transK = max(0.0, -dot(normal, uSunDir));\n float viewK = 0.55 + 0.45 * max(0.0, dot(normalize(vViewPosition), uSunDir));\n reflectedLight.directDiffuse += diffuseColor.rgb * uTransTint * uSunColor * transK * viewK * uTrans;');
    }
    if (opts.fragEnd) shader.fragmentShader = shader.fragmentShader.replace('#include <dithering_fragment>', `#include <dithering_fragment>\n${opts.fragEnd}`);
    if (opts.vertDecl) shader.vertexShader = opts.vertDecl + shader.vertexShader;
    if (opts.vertBegin) shader.vertexShader = shader.vertexShader.replace('#include <begin_vertex>', opts.vertBegin);
    if (opts.vertNormal) shader.vertexShader = shader.vertexShader.replace('#include <beginnormal_vertex>', opts.vertNormal);
    material.userData.shader = shader;
  };
  const key = opts.key || `p${opts.backMap ? 1 : 0}${opts.translucency ? 1 : 0}${(opts.vertBegin || '').length}${(opts.fragMap || '').length}${(opts.fragEnd || '').length}`;
  material.customProgramCacheKey = () => key;
  return material;
}

export function taperedTube(curve, segments, radial, radiusAt, opts = {}) {
  const frames = curve.computeFrenetFrames(segments, false);
  const pos = []; const nor = []; const uv = []; const idx = [];
  const p = new THREE.Vector3(); const n = new THREE.Vector3();
  for (let i = 0; i <= segments; i++) {
    const t = i / segments;
    curve.getPointAt(t, p);
    const r = radiusAt(t);
    const N = frames.normals[i]; const B = frames.binormals[i];
    for (let j = 0; j <= radial; j++) {
      const a = (j / radial) * Math.PI * 2;
      const wob = opts.wobble ? 1 + opts.wobble(t, a) : 1;
      n.set(0, 0, 0).addScaledVector(N, Math.cos(a)).addScaledVector(B, Math.sin(a)).normalize();
      pos.push(p.x + n.x * r * wob, p.y + n.y * r * wob, p.z + n.z * r * wob);
      nor.push(n.x, n.y, n.z);
      uv.push(j / radial, t * (opts.vRepeat || 1));
    }
  }
  for (let i = 0; i < segments; i++) {
    for (let j = 0; j < radial; j++) {
      const a = i * (radial + 1) + j; const b = a + radial + 1;
      idx.push(a, b, a + 1, b, b + 1, a + 1);
    }
  }
  if (opts.capEnd) {
    const c = pos.length / 3;
    curve.getPointAt(1, p);
    const tan = curve.getTangentAt(1);
    const r1 = radiusAt(1);
    pos.push(p.x + tan.x * r1 * 0.6, p.y + tan.y * r1 * 0.6, p.z + tan.z * r1 * 0.6);
    nor.push(tan.x, tan.y, tan.z); uv.push(0.5, 1);
    const base = segments * (radial + 1);
    for (let j = 0; j < radial; j++) idx.push(base + j, base + j + 1, c);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx);
  if (opts.recomputeNormals) g.computeVertexNormals();
  return g;
}

export function mergeGeos(list) {
  let vCount = 0; let iCount = 0;
  const parts = list.map((g) => {
    if (!g.index) g.setIndex([...Array(g.attributes.position.count).keys()]);
    vCount += g.attributes.position.count; iCount += g.index.count;
    return g;
  });
  const pos = new Float32Array(vCount * 3); const nor = new Float32Array(vCount * 3);
  const uv = new Float32Array(vCount * 2); const col = new Float32Array(vCount * 3);
  const idx = new Uint32Array(iCount);
  let vo = 0; let io = 0;
  parts.forEach((g) => {
    const n = g.attributes.position.count;
    pos.set(g.attributes.position.array, vo * 3);
    if (g.attributes.normal) nor.set(g.attributes.normal.array, vo * 3);
    if (g.attributes.uv) uv.set(g.attributes.uv.array, vo * 2);
    if (g.attributes.color) col.set(g.attributes.color.array, vo * 3);
    else col.fill(1, vo * 3, (vo + n) * 3);
    const ia = g.index.array;
    for (let i = 0; i < ia.length; i++) idx[io + i] = ia[i] + vo;
    vo += n; io += ia.length;
    g.dispose();
  });
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  out.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  out.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  out.setAttribute('color', new THREE.BufferAttribute(col, 3));
  out.setIndex(new THREE.BufferAttribute(idx, 1));
  return out;
}

export function paintVertices(geo, fn) {
  const p = geo.attributes.position; const c = new Float32Array(p.count * 3); const col = new THREE.Color();
  for (let i = 0; i < p.count; i++) { fn(p.getX(i), p.getY(i), p.getZ(i), col, i); c[i * 3] = col.r; c[i * 3 + 1] = col.g; c[i * 3 + 2] = col.b; }
  geo.setAttribute('color', new THREE.BufferAttribute(c, 3));
  return geo;
}

export function basisQuaternion(dir, upHint, out = new THREE.Quaternion()) {
  const Y = dir.clone().normalize();
  const Z = upHint.clone().addScaledVector(Y, -upHint.dot(Y)).normalize();
  const X = new THREE.Vector3().crossVectors(Y, Z).normalize();
  return out.setFromRotationMatrix(new THREE.Matrix4().makeBasis(X, Y, Z));
}

// Outdoor image-based light: sky, a sun hot-spot and a ground bounce, prefiltered once.
export function outdoorEnvironment(renderer, opts = {}) {
  const w = 256; const h = 128;
  const c = makeCanvas(w, h);
  const g = c.getContext('2d');
  const grad = g.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, opts.zenith || '#5d8fd6');
  grad.addColorStop(0.47, opts.horizon || '#cfe0ee');
  grad.addColorStop(0.53, opts.horizonLow || '#8a9a6a');
  grad.addColorStop(1, opts.ground || '#3a3a22');
  g.fillStyle = grad; g.fillRect(0, 0, w, h);
  const su = opts.sunU ?? 0.3; const sv = opts.sunV ?? 0.25;
  const sg = g.createRadialGradient(su * w, sv * h, 0, su * w, sv * h, 26);
  sg.addColorStop(0, 'rgba(255,250,235,1)'); sg.addColorStop(0.25, 'rgba(255,240,200,0.7)'); sg.addColorStop(1, 'rgba(255,230,180,0)');
  g.fillStyle = sg; g.fillRect(0, 0, w, h);
  if (opts.paint) opts.paint(g, w, h);
  const tex = new THREE.CanvasTexture(c);
  tex.mapping = THREE.EquirectangularReflectionMapping;
  tex.colorSpace = THREE.SRGBColorSpace;
  let rt = null;
  try {
    const pmrem = new THREE.PMREMGenerator(renderer);
    rt = pmrem.fromEquirectangular(tex);
    pmrem.dispose();
  } catch (e) { rt = null; }
  tex.dispose();
  return { texture: rt ? rt.texture : null, dispose() { if (rt) rt.dispose(); } };
}

export function skyDome(opts = {}) {
  const mat = new THREE.ShaderMaterial({
    uniforms: {
      zenith: { value: new THREE.Color(opts.zenith ?? 0x3f78c8) },
      horizon: { value: new THREE.Color(opts.horizon ?? 0xd9e6ee) },
      ground: { value: new THREE.Color(opts.ground ?? 0x8c9472) },
      sunDir: { value: (opts.sunDir || new THREE.Vector3(0.4, 0.6, -0.6)).clone().normalize() },
      sunColor: { value: new THREE.Color(opts.sunColor ?? 0xfff2d8) },
      sunSize: { value: opts.sunSize ?? 1600 },
      haze: { value: opts.haze ?? 1 },
    },
    vertexShader: 'varying vec3 vDir; void main(){ vDir = normalize(position); vec4 p = modelViewMatrix * vec4(position,1.0); gl_Position = projectionMatrix * p; gl_Position.z = gl_Position.w * 0.99999; }',
    fragmentShader: `uniform vec3 zenith; uniform vec3 horizon; uniform vec3 ground; uniform vec3 sunDir; uniform vec3 sunColor; uniform float sunSize; uniform float haze; varying vec3 vDir;
      void main(){ vec3 d = normalize(vDir); float y = d.y;
        vec3 col = y > 0.0 ? mix(horizon, zenith, pow(clamp(y,0.0,1.0), 0.55)) : mix(horizon, ground, pow(clamp(-y*3.0,0.0,1.0), 0.6));
        float s = max(dot(d, sunDir), 0.0);
        col += sunColor * (pow(s, sunSize) * 6.0 + pow(s, 24.0) * 0.35 * haze + pow(s, 4.0) * 0.12 * haze);
        gl_FragColor = vec4(col, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
    side: THREE.BackSide, depthWrite: false, fog: false,
  });
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(opts.radius || 900, 32, 16), mat);
  mesh.renderOrder = -20;
  mesh.frustumCulled = false;
  return mesh;
}

// Camera rig: damped orbit, pinch/wheel zoom, cinematic fly-to between shots, ground clamp, tap picking.
export function createRig(camera, dom, opts = {}) {
  const target = new THREE.Vector3(); const targetGoal = new THREE.Vector3();
  const sph = { r: 10, theta: 0, phi: 1.1 }; const goal = { ...sph };
  let lim = { minR: 1, maxR: 200, minPhi: 0.1, maxPhi: Math.PI - 0.1 };
  let tween = null; let autoSpin = 0; let idle = 0; let enabled = true;
  const minY = opts.minY ?? -Infinity;
  const pointers = new Map(); let pinch = 0; let down = null;

  function clampGoal() {
    goal.r = clamp(goal.r, lim.minR, lim.maxR);
    let maxPhi = lim.maxPhi;
    if (Number.isFinite(minY)) {
      const k = (minY - targetGoal.y) / goal.r;
      if (k > -1 && k < 1) maxPhi = Math.min(maxPhi, Math.acos(k));
    }
    goal.phi = clamp(goal.phi, lim.minPhi, maxPhi);
  }
  function cancelTween() { if (tween) { tween = null; Object.assign(goal, sph); targetGoal.copy(target); } }

  function onDown(e) {
    if (!enabled) return;
    if (dom.setPointerCapture) dom.setPointerCapture(e.pointerId);
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 1) down = { x: e.clientX, y: e.clientY, t: performance.now() };
    if (pointers.size === 2) { const p = [...pointers.values()]; pinch = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y); down = null; }
    idle = 0;
  }
  function onMove(e) {
    if (!enabled || !pointers.has(e.pointerId)) return;
    const prev = pointers.get(e.pointerId);
    const dx = e.clientX - prev.x; const dy = e.clientY - prev.y;
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (down && Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6) down = null;
    if (pointers.size === 1 && !down) {
      cancelTween();
      goal.theta -= dx * 0.006; goal.phi -= dy * 0.006; clampGoal();
    } else if (pointers.size === 2) {
      cancelTween();
      const p = [...pointers.values()]; const d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
      if (pinch > 0) { goal.r *= pinch / Math.max(d, 1); clampGoal(); }
      pinch = d;
    }
    idle = 0;
  }
  function onUp(e) {
    if (down && pointers.size === 1 && performance.now() - down.t < 450 && opts.onTap) {
      const rect = dom.getBoundingClientRect();
      opts.onTap(new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1));
    }
    pointers.delete(e.pointerId); pinch = 0; down = null;
  }
  function onWheel(e) {
    if (!enabled) return;
    e.preventDefault(); cancelTween();
    goal.r *= e.deltaY > 0 ? 1.1 : 0.9; clampGoal(); idle = 0;
  }
  function onCtx(e) { e.preventDefault(); }
  dom.style.touchAction = 'none';
  dom.addEventListener('pointerdown', onDown);
  dom.addEventListener('pointermove', onMove);
  dom.addEventListener('pointerup', onUp);
  dom.addEventListener('pointercancel', onUp);
  dom.addEventListener('wheel', onWheel, { passive: false });
  dom.addEventListener('contextmenu', onCtx);

  const out = new THREE.Vector3();
  function place() {
    out.set(Math.sin(sph.phi) * Math.sin(sph.theta), Math.cos(sph.phi), Math.sin(sph.phi) * Math.cos(sph.theta)).multiplyScalar(sph.r).add(target);
    if (out.y < minY) out.y = minY;
    camera.position.copy(out);
    camera.lookAt(target);
  }

  return {
    target,
    set enabled(v) { enabled = v; },
    get busy() { return !!tween; },
    get radius() { return sph.r; },
    setLimits(l) { lim = { ...lim, ...l }; clampGoal(); },
    setAutoSpin(v) { autoSpin = v; },
    jump(shot) {
      tween = null;
      if (shot.limits) lim = { ...lim, ...shot.limits };
      target.copy(shot.target); targetGoal.copy(shot.target);
      sph.r = goal.r = shot.r; sph.theta = goal.theta = shot.theta; sph.phi = goal.phi = shot.phi;
      place();
    },
    flyTo(shot, duration = 1.8) {
      if (shot.limits) lim = { ...lim, ...shot.limits };
      let dTheta = shot.theta - sph.theta;
      dTheta = Math.atan2(Math.sin(dTheta), Math.cos(dTheta));
      tween = {
        t: 0, d: Math.max(0.01, duration),
        from: { target: target.clone(), r: sph.r, theta: sph.theta, phi: sph.phi },
        to: { target: shot.target.clone(), r: shot.r, theta: sph.theta + dTheta, phi: shot.phi },
        arc: shot.arc ?? 0.25,
      };
    },
    follow(point, lambda = 3, dt = 0.016) {
      const k = 1 - Math.exp(-lambda * dt);
      if (tween) tween.to.target.lerp(point, k);
      else targetGoal.lerp(point, k);
    },
    update(dt) {
      idle += dt;
      if (tween) {
        tween.t += dt;
        const k = easeInOut(tween.t / tween.d);
        const f = tween.from; const t = tween.to;
        target.lerpVectors(f.target, t.target, k);
        const lift = Math.sin(Math.PI * k) * tween.arc;
        sph.r = Math.exp(lerp(Math.log(f.r), Math.log(t.r), k)) * (1 + lift);
        sph.theta = lerp(f.theta, t.theta, k);
        sph.phi = lerp(f.phi, t.phi, k) - lift * 0.2;
        if (tween.t >= tween.d) { tween = null; Object.assign(goal, { r: t.r, theta: t.theta, phi: t.phi }); targetGoal.copy(t.target); clampGoal(); }
      } else {
        if (autoSpin && idle > 5) goal.theta += autoSpin * dt;
        const a = 1 - Math.exp(-9 * dt);
        sph.r += (goal.r - sph.r) * a; sph.theta += (goal.theta - sph.theta) * a; sph.phi += (goal.phi - sph.phi) * a;
        target.lerp(targetGoal, a);
      }
      place();
    },
    dispose() {
      dom.removeEventListener('pointerdown', onDown);
      dom.removeEventListener('pointermove', onMove);
      dom.removeEventListener('pointerup', onUp);
      dom.removeEventListener('pointercancel', onUp);
      dom.removeEventListener('wheel', onWheel);
      dom.removeEventListener('contextmenu', onCtx);
    },
  };
}
