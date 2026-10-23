import { THREE } from '../../core/engine.js';

const LMAP = { s: 0, p: 1, d: 2, f: 3 };
const MAXS = 8;

function slaterZeff(cfg, idx) {
  const me = cfg[idx];
  const Z = cfg.reduce((s, c) => s + c.count, 0);
  let S = 0;
  cfg.forEach((c, i) => {
    const same = c.n === me.n && ((me.l === 's' || me.l === 'p') ? (c.l === 's' || c.l === 'p') : c.l === me.l);
    const cnt = i === idx ? c.count - 1 : c.count;
    if (cnt <= 0) return;
    if (me.l === 's' || me.l === 'p') {
      if (c.n === me.n && (c.l === 's' || c.l === 'p')) S += cnt * (me.n === 1 ? 0.3 : 0.35);
      else if (c.n === me.n - 1) S += cnt * 0.85;
      else if (c.n < me.n - 1) S += cnt;
      else if (c.n === me.n && !same) S += 0;
    } else {
      if (same) S += cnt * 0.35;
      else if (c.n < me.n || (c.n === me.n && (c.l === 's' || c.l === 'p'))) S += cnt;
    }
  });
  return Math.max(1, Z - S);
}

function fact(n) { let f = 1; for (let i = 2; i <= n; i++) f *= i; return f; }

function laguerre(k, a, x) {
  let l0 = 1; if (k === 0) return l0;
  let l1 = 1 + a - x;
  for (let i = 1; i < k; i++) { const l2 = ((2 * i + 1 + a - x) * l1 - (i + a) * l0) / (i + 1); l0 = l1; l1 = l2; }
  return l1;
}

function radialPeak(n, l, z) {
  let best = 0;
  for (let i = 1; i <= 400; i++) {
    const r = i / 400 * n * n * 3 / z;
    const x = 2 * z * r / n;
    const R = Math.pow(x, l) * laguerre(n - l - 1, 2 * l + 1, x) * Math.exp(-x / 2);
    best = Math.max(best, R * R);
  }
  return best || 1;
}

// The density of every subshell is a fixed function of the electron configuration, so it is baked
// once per change into a 3D texture (premultiplied colour + density). The ray march then does one
// trilinear fetch per step instead of evaluating radial and angular parts of up to eight subshells,
// and it only marches through the sphere where the density is not negligible.
const BAKE = `
precision highp float;
uniform float uScale;
uniform int uCount;
uniform float uN[${MAXS}]; uniform float uL[${MAXS}]; uniform float uW[${MAXS}];
uniform sampler2D uRad; uniform float uRMax;
uniform vec4 uMOcc[${MAXS}];
uniform float uMOcc5[${MAXS}];
uniform float uPartial[${MAXS}];
uniform int uHi;
uniform float uZ; uniform float uRes;
varying vec2 vUv;
float Rn(int i, float r){ return texture2D(uRad, vec2(clamp(r / uRMax, 0.0, 1.0), (float(i) + 0.5) / ${MAXS}.0)).r * 2.0 - 1.0; }
void ylm(float l, vec3 u, out float y[5]){
  for (int i = 0; i < 5; i++) y[i] = 0.0;
  if (l < 0.5) { y[0] = 1.0; return; }
  if (l < 1.5) { y[0] = u.x; y[1] = u.y; y[2] = u.z; return; }
  y[0] = u.x * u.y * 1.732; y[1] = u.y * u.z * 1.732; y[2] = (3.0 * u.y * u.y - 1.0) * 0.5 * 1.15; y[3] = u.x * u.z * 1.732; y[4] = (u.x * u.x - u.z * u.z) * 0.866;
}
void main(){
  vec3 p = vec3(vUv, (uZ + 0.5) / uRes) * 2.0 - 1.0;
  float r = length(p) * uScale;
  vec3 u = normalize(p + 1e-5);
  vec3 col = vec3(0.0); float acc = 0.0;
  for (int i = 0; i < ${MAXS}; i++) {
    if (i >= uCount) break;
    float R = Rn(i, r);
    float R2 = R * R;
    if (R2 < 1e-4) continue;
    bool hi = (i == uHi);
    if (uPartial[i] > 0.5 || hi) {
      float y[5]; ylm(uL[i], u, y);
      float occ[5]; occ[0] = uMOcc[i].x; occ[1] = uMOcc[i].y; occ[2] = uMOcc[i].z; occ[3] = uMOcc[i].w; occ[4] = uMOcc5[i];
      for (int m = 0; m < 5; m++) {
        float o = hi ? 1.0 : occ[m];
        if (o <= 0.0) continue;
        float psi = R * y[m];
        float d = psi * psi * o * (hi ? 1.6 : 1.0);
        d = d * d * 2.2;
        vec3 c = psi > 0.0 ? vec3(1.0, 0.55, 0.18) : vec3(0.25, 0.55, 1.0);
        col += c * d * uW[i]; acc += d * uW[i];
      }
    } else {
      vec3 c = mix(vec3(0.55, 0.75, 1.0), vec3(0.9, 0.95, 1.0), clamp(uN[i] / 4.0, 0.0, 1.0));
      float d2 = R2 * R2 * 1.6;
      col += c * d2 * uW[i]; acc += d2 * uW[i];
    }
  }
  gl_FragColor = vec4(col, acc);
}`;

const FRAG = `
precision highp float;
precision highp sampler3D;
uniform vec3 uCam;
uniform highp sampler3D uVol;
uniform float uBound;
uniform float uSteps;
uniform float uGain;
uniform float uTime;
varying vec3 vPos;
float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
void main(){
  vec3 ro = uCam; vec3 rd = normalize(vPos - uCam);
  float b = dot(ro, rd); float c = dot(ro, ro) - uBound * uBound;
  float disc = b * b - c;
  if (disc <= 0.0) discard;
  float q = sqrt(disc);
  vec3 inv = 1.0 / rd; vec3 t0 = (vec3(-1.0) - ro) * inv; vec3 t1 = (vec3(1.0) - ro) * inv;
  vec3 tmin = min(t0, t1); vec3 tmax = max(t0, t1);
  float ta = max(max(max(tmin.x, tmin.y), max(tmin.z, 0.0)), -b - q);
  float tb = min(min(min(tmax.x, tmax.y), tmax.z), -b + q);
  if (tb <= ta) discard;
  float dt = (tb - ta) / uSteps;
  float t = ta + dt * h(gl_FragCoord.xy + uTime);
  vec4 sum = vec4(0.0);
  for (int s = 0; s < 72; s++) {
    if (float(s) >= uSteps) break;
    sum += texture(uVol, (ro + rd * t) * 0.5 + 0.5);
    t += dt;
  }
  vec3 col = sum.rgb * dt * uGain; float acc = sum.a * dt * uGain;
  float a = 1.0 - exp(-acc * 1.5);
  gl_FragColor = vec4(col / max(acc, 1e-4) * a * 1.4, a);
}`;

export function createOrbitalCloud(quality, renderer) {
  const steps = quality.tier === 'low' ? 26 : quality.tier === 'medium' ? 40 : 56;
  const VR = quality.tier === 'low' ? 64 : quality.tier === 'medium' ? 96 : 128;
  const B = {
    uScale: { value: 4 }, uCount: { value: 0 },
    uN: { value: new Array(MAXS).fill(1) }, uL: { value: new Array(MAXS).fill(0) },
    uW: { value: new Array(MAXS).fill(0) }, uRad: { value: null }, uRMax: { value: 10 },
    uMOcc: { value: Array.from({ length: MAXS }, () => new THREE.Vector4()) }, uMOcc5: { value: new Array(MAXS).fill(0) },
    uPartial: { value: new Array(MAXS).fill(0) }, uHi: { value: -1 }, uZ: { value: 0 }, uRes: { value: VR },
  };
  const vol = new THREE.WebGL3DRenderTarget(VR, VR, VR, { depthBuffer: false, type: THREE.HalfFloatType });
  vol.texture.format = THREE.RGBAFormat;
  vol.texture.minFilter = vol.texture.magFilter = THREE.LinearFilter;
  vol.texture.wrapS = vol.texture.wrapT = vol.texture.wrapR = THREE.ClampToEdgeWrapping;
  vol.texture.generateMipmaps = false;
  const bakeMat = new THREE.ShaderMaterial({
    uniforms: B,
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy * 2.0, 0.0, 1.0); }',
    fragmentShader: BAKE, depthTest: false, depthWrite: false,
  });
  const quad = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), bakeMat);
  quad.frustumCulled = false;
  const bakeScene = new THREE.Scene(); bakeScene.add(quad);
  const bakeCam = new THREE.Camera();
  let dirty = true;
  function bake() {
    dirty = false;
    const prev = renderer.getRenderTarget(); const prevAuto = renderer.autoClear;
    renderer.autoClear = false;
    for (let z = 0; z < VR; z++) { B.uZ.value = z; renderer.setRenderTarget(vol, z); renderer.render(bakeScene, bakeCam); }
    renderer.setRenderTarget(prev); renderer.autoClear = prevAuto;
  }
  const U = {
    uCam: { value: new THREE.Vector3() }, uVol: { value: vol.texture }, uBound: { value: Math.sqrt(3) },
    uSteps: { value: steps }, uGain: { value: 1 }, uTime: { value: 0 },
  };
  const mat = new THREE.ShaderMaterial({
    uniforms: U,
    vertexShader: 'varying vec3 vPos; void main(){ vPos = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: FRAG,
    transparent: true, depthWrite: false, side: THREE.BackSide, blending: THREE.CustomBlending,
    blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  });
  mat.toneMapped = false;
  const RES = 512;
  const radData = new Uint8Array(RES * MAXS * 4);
  const radTex = new THREE.DataTexture(radData, RES, MAXS, THREE.RGBAFormat);
  radTex.magFilter = THREE.LinearFilter; radTex.minFilter = THREE.LinearFilter; radTex.needsUpdate = true;
  B.uRad.value = radTex;
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), mat);
  mesh.renderOrder = 5;
  let subs = [];
  const inv = new THREE.Matrix4();
  return {
    mesh,
    get subshells() { return subs; },
    setConfig(cfg, highlight = null) {
      const list = cfg.slice(-MAXS);
      subs = list.map((c) => c.sub);
      B.uCount.value = list.length;
      let outer = 1;
      const zs = [];
      list.forEach((c, i) => {
        const l = LMAP[c.l];
        const z = slaterZeff(cfg, cfg.indexOf(c));
        const nEff = c.n;
        B.uN.value[i] = nEff; B.uL.value[i] = Math.min(l, 2);
        zs[i] = z;
        B.uW.value[i] = (0.35 + 0.65 * c.count / c.cap) * 9.0 * (i === list.length - 1 ? 1.5 : 0.8);
        outer = Math.max(outer, (nEff * nEff / z) * (l === 0 ? 1.6 : 1.3) + 1);
        const partial = c.count < c.cap && l > 0 && l < 3;
        B.uPartial.value[i] = partial ? 1 : 0;
        const orbs = 2 * Math.min(l, 2) + 1; const occ = new Array(5).fill(0);
        for (let e = 0; e < c.count && l < 3; e++) occ[e % orbs] += 1;
        B.uMOcc.value[i].set(occ[0] / 2, occ[1] / 2, occ[2] / 2, occ[3] / 2); B.uMOcc5.value[i] = occ[4] / 2;
      });
      B.uScale.value = outer * 0.78;
      const rmax = Math.sqrt(3) * B.uScale.value;
      B.uRMax.value = rmax;
      list.forEach((c, i) => {
        const l = Math.min(LMAP[c.l], 2); const n = c.n; const z = zs[i];
        const pk = Math.sqrt(radialPeak(n, l, z));
        for (let k = 0; k < RES; k++) {
          const r = k / (RES - 1) * rmax; const x = 2 * z * r / n;
          const v = Math.pow(Math.max(x, 1e-4), l) * laguerre(n - l - 1, 2 * l + 1, x) * Math.exp(-x / 2) / pk;
          const o = (i * RES + k) * 4;
          radData[o] = Math.max(0, Math.min(255, Math.round((Math.max(-1, Math.min(1, v)) * 0.5 + 0.5) * 255)));
        }
      });
      radTex.needsUpdate = true;
      let cut = 0;
      for (let k = RES - 1; k > 0 && !cut; k--) for (let i = 0; i < list.length; i++) { if (Math.abs(radData[(i * RES + k) * 4] / 127.5 - 1) > 0.012) { cut = k; break; } }
      U.uBound.value = Math.min(Math.sqrt(3), (cut + 2) / (RES - 1) * rmax / B.uScale.value);
      dirty = true;
      B.uHi.value = highlight != null ? subs.indexOf(highlight) : -1;
      dirty = true;
    },
    update(camera, t, size = 6.5) {
      mesh.scale.setScalar(size);
      mesh.updateMatrixWorld();
      inv.copy(mesh.matrixWorld).invert();
      U.uCam.value.copy(camera.position).applyMatrix4(inv);
      U.uTime.value = t % 10;
      if (dirty) bake();
    },
    dispose() { mesh.geometry.dispose(); mat.dispose(); radTex.dispose(); vol.dispose(); bakeMat.dispose(); quad.geometry.dispose(); },
  };
}
