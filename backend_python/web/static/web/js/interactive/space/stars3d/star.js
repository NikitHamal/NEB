import { THREE } from '../../core/engine.js';
import { NZ } from '../../core/noise3d.js';
import { NOISE } from '../cosmos/shaders.js';

// Blackbody colour of temperature T (K), linear RGB normalised to its brightest channel.
export const BLACKBODY = `
vec3 blackbody(float T) {
  float t = clamp(T, 1000.0, 40000.0) / 100.0;
  vec3 c;
  c.r = t <= 66.0 ? 1.0 : clamp(1.29293618606 * pow(t - 60.0, -0.1332047592), 0.0, 1.0);
  c.g = t <= 66.0 ? clamp(0.39008157876 * log(t) - 0.63184144378, 0.0, 1.0) : clamp(1.12989086089 * pow(t - 60.0, -0.0755148492), 0.0, 1.0);
  c.b = t >= 66.0 ? 1.0 : (t <= 19.0 ? 0.0 : clamp(0.54320678911 * log(t - 10.0) - 1.19625408914, 0.0, 1.0));
  return pow(c, vec3(2.2));
}`;

// A star's surface for any temperature and size. Convection cells are fine granules on a dwarf and a
// handful of giant cells on a red giant; each cell is a little hotter at its centre, so it is brighter
// as (T'/T)^4 and bluer. Limb darkening is stronger for cooler stars. Giants get an irregular limb.
export function createStar(quality) {
  const seg = quality.tier === 'low' ? 48 : 96;
  const U = {
    tNz: NZ, uT: { value: 5772 }, uCells: { value: 70 }, uGiant: { value: 0 }, uTime: { value: 0 }, uSpots: { value: 0.4 }, uBright: { value: 1 },
  };
  const mat = new THREE.ShaderMaterial({
    uniforms: U,
    vertexShader: `${NOISE}
      uniform float uGiant; uniform float uTime;
      varying vec3 vN; varying vec3 vV;
      void main() {
        vec3 n = normalize(position);
        float d = (fbm3(n * 1.4 + vec3(uTime * 0.02)) - 0.5) * 0.16 * uGiant + (fbm3(n * 3.5 - vec3(uTime * 0.03)) - 0.5) * 0.06 * uGiant;
        vec3 p = position * (1.0 + d);
        vN = n;
        vec4 wp = modelMatrix * vec4(p, 1.0);
        vV = normalize((inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz - p);
        gl_Position = projectionMatrix * viewMatrix * wp;
      }`,
    fragmentShader: `${NOISE}${BLACKBODY}
      uniform float uT; uniform float uCells; uniform float uGiant; uniform float uTime; uniform float uSpots; uniform float uBright;
      varying vec3 vN; varying vec3 vV;
      void main() {
        vec3 n = normalize(vN);
        float mu = clamp(dot(n, normalize(vV)), 0.0, 1.0);
        vec4 c1 = nz4(n * uCells + vec3(0.0, uTime * 0.03, 0.0));
        vec4 c2 = nz4(n * uCells * 2.1 - vec3(uTime * 0.04, 0.0, 0.0));
        float cellD = smoothstep(0.0, 0.2, c1.b) * 0.65 + smoothstep(0.0, 0.2, c2.b) * 0.35;
        float blob = (1.0 - smoothstep(0.05, 0.75, c1.a)) * 0.7 + (1.0 - smoothstep(0.05, 0.75, c2.a)) * 0.3;
        float cell = mix(cellD, blob, uGiant);
        float mott = fbm3(n * 2.2 + vec3(uTime * 0.01));
        float dT = (cell - 0.6) * mix(0.06, 0.16, uGiant) + (mott - 0.5) * mix(0.03, 0.22, uGiant);
        float Tl = uT * (1.0 + dT);
        float act = smoothstep(0.62, 0.2, abs(n.y)) * smoothstep(0.08, 0.2, abs(n.y));
        float sf = fbm3(n * 5.5 + 13.0);
        float spot = smoothstep(0.72, 0.8, sf) * act * uSpots;
        float coolness = clamp((6500.0 - uT) / 3500.0, 0.0, 1.0);
        float limb = 1.0 - mix(0.55, 0.85, coolness) * (1.0 - pow(mu, mix(0.9, 0.6, uGiant)));
        vec3 col = blackbody(Tl) * pow(Tl / uT, 4.0) * limb * (1.0 - spot * 0.7) * 1.7 * uBright;
        col += blackbody(uT) * pow(1.0 - mu, 3.0) * 0.25 * (1.0 - uGiant);
        col = 1.0 - exp(-col * mix(1.2, 0.75, uGiant));
        float lum = dot(col, vec3(0.3, 0.59, 0.11));
        col = max(mix(vec3(lum), col, mix(1.0, 1.45, uGiant)), 0.0);
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
      }`,
  });
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(1, seg, seg / 2), mat);

  // The light around the star: a glare that scales with luminosity, coronal streamers on hot dwarfs,
  // and a dusty, reddened envelope on giants. A camera-facing disc in stellar radii.
  const H = { tNz: NZ, uT: U.uT, uTime: U.uTime, uGiant: U.uGiant, uGlow: { value: 1 }, uCorona: { value: 1 } };
  const halo = new THREE.Mesh(new THREE.PlaneGeometry(16, 16), new THREE.ShaderMaterial({
    uniforms: H,
    vertexShader: `varying vec2 vQ;
      void main() { vQ = position.xy; vec4 c = modelViewMatrix * vec4(0.0, 0.0, 0.0, 1.0);
        float sc = length(modelMatrix[0].xyz); gl_Position = projectionMatrix * (c + vec4(position.xy * sc, 0.0, 0.0)); }`,
    fragmentShader: `${NOISE}${BLACKBODY}
      uniform float uT; uniform float uTime; uniform float uGiant; uniform float uGlow; uniform float uCorona; varying vec2 vQ;
      void main() {
        float r = length(vQ);
        if (r < 0.97) discard;
        float th = atan(vQ.y, vQ.x); vec3 dir = vec3(cos(th), sin(th), 0.0);
        vec3 bb = blackbody(uT);
        float glare = pow(max(r - 0.97, 0.0) + 0.04, -1.4) * 0.012 + exp(-(r - 1.0) * 2.2) * 0.25;
        float st = fbm3(dir * 2.2 + vec3(0.0, 0.0, uTime * 0.004)) * 0.7 + fbm3(dir * 7.0 + vec3(3.0, 1.0, uTime * 0.007)) * 0.5;
        float corona = pow(r, -2.6) * (0.2 + 1.4 * pow(clamp(st, 0.0, 1.2), 2.4)) * smoothstep(0.97, 1.03, r) * uCorona * (1.0 - uGiant);
        vec3 col = mix(bb, vec3(1.0), 0.35) * (glare * uGlow + corona * 0.7);
        float env = fbm3(vec3(vQ * 0.9, uTime * 0.01)) * fbm3(vec3(vQ * 2.4 + 5.0, uTime * 0.015));
        col += vec3(0.9, 0.38, 0.18) * env * exp(-(r - 1.0) * 0.9) * 0.9 * uGiant;
        col *= smoothstep(8.0, 4.5, r);
        gl_FragColor = vec4(col, 1.0);
      }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  halo.frustumCulled = false;
  halo.renderOrder = 4;
  const group = new THREE.Group();
  group.add(mesh, halo);
  return {
    group, mesh, halo, uniforms: U, haloUniforms: H,
    dispose() { mesh.geometry.dispose(); mat.dispose(); halo.geometry.dispose(); halo.material.dispose(); },
  };
}
