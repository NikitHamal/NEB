import { THREE } from '../../core/engine.js';
import { NZ } from '../../core/noise3d.js';
import { NOISE } from '../cosmos/shaders.js';

// Gas lit from inside, ray-marched through a sphere. Mode 0: the dusty birth cloud, H-alpha pink where
// the young source lights it, dark lanes where dust absorbs. Mode 1: a planetary nebula shell, teal
// [O III] inside and red H-alpha/[N II] at the edge, with knots. Mode 2: a supernova remnant, red
// filaments on an expanding shock around blue synchrotron glow. Emission and absorption are
// integrated front to back and written premultiplied, so dust really hides the stars behind it.
// Drawn at a fraction of the screen resolution into its own target (the gas is soft, so nothing is
// lost) and composited over the frame by a fullscreen quad with the same premultiplied blend.
export function createNebula(quality, renderer) {
  const steps = quality.tier === 'low' ? 20 : quality.tier === 'medium' ? 28 : 36;
  const U = {
    tNz: NZ, uMode: { value: 0 }, uExpand: { value: 0 }, uTime: { value: 0 }, uSource: { value: new THREE.Color(1, 0.8, 0.6) },
    uSourceK: { value: 1 }, uFade: { value: 1 }, uSteps: { value: steps },
  };
  const mat = new THREE.ShaderMaterial({
    uniforms: U,
    vertexShader: `varying vec3 vP; varying vec3 vC;
      void main() { vP = position; vC = (inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `${NOISE}
      uniform float uMode; uniform float uExpand; uniform float uTime; uniform vec3 uSource; uniform float uSourceK; uniform float uFade; uniform float uSteps;
      varying vec3 vP; varying vec3 vC;
      float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
      void nebSample(vec3 p, out vec3 em, out float ab) {
        float r = length(p);
        em = vec3(0.0); ab = 0.0;
        if (uMode < 0.5) {
          vec3 w = p * 1.7 + (nz4(p * 1.3 + 4.0).rga - 0.5) * 2.8;
          float d = fbm3(w + vec3(0.0, uTime * 0.004, 0.0));
          vec4 n2 = nz4(w * 3.1 + 2.0);
          float gas = smoothstep(0.3, 0.7, d * 0.8 + n2.r * 0.3) * (1.0 - smoothstep(0.5, 1.0, r));
          float dust = smoothstep(0.55, 0.8, d * 0.6 + n2.g * 0.55) * (1.0 - smoothstep(0.6, 1.0, r));
          gas *= 1.0 + uExpand * 4.0 * exp(-r * r * 22.0);
          float light = uSourceK / (0.02 + r * r * 3.0) + 0.06;
          float rim = smoothstep(0.0, 0.25, gas) * (1.0 - smoothstep(0.25, 0.7, gas));
          em = (vec3(1.0, 0.3, 0.42) * (gas * 0.55 + rim * 0.9) + vec3(0.45, 0.62, 1.0) * 0.35 * exp(-r * 3.0) * gas) * light * 0.6;
          ab = gas * 0.7 + dust * 7.0;
        } else if (uMode < 1.5) {
          vec3 q = p * vec3(1.0, 0.78, 1.0);
          float sr = 0.22 + 0.55 * uExpand;
          float rq = length(q);
          float k1 = fbm3(p * 5.0 + 1.0); float k2 = fbm3(p * 13.0 + 7.0);
          float shell = exp(-pow((rq - sr) / (0.05 + 0.05 * k1), 2.0));
          float inner = smoothstep(sr * 0.9, sr * 0.4, rq) * 0.18;
          float spokes = pow(0.5 + 0.5 * sin(atan(q.z, q.x) * 18.0 + k1 * 6.0), 6.0) * shell * 0.5;
          float lobes = exp(-pow(length(vec2(q.x, q.z)) / (0.12 + 0.3 * uExpand), 2.0)) * smoothstep(sr * 0.8, sr * 1.6, rq) * smoothstep(sr * 2.0, sr * 1.4, rq) * 0.6;
          float dens = (shell + inner + lobes + spokes) * (0.45 + 1.1 * k1) * (0.6 + 0.7 * k2);
          float edge = smoothstep(sr * 0.75, sr * 1.05, rq);
          vec3 c = mix(vec3(0.25, 0.95, 0.82), vec3(1.0, 0.25, 0.32), edge);
          c += vec3(0.6, 0.65, 1.0) * smoothstep(sr * 0.5, 0.0, rq) * 0.4;
          float knots = smoothstep(0.7, 0.85, k2) * shell;
          em = c * dens * 1.1 + vec3(1.0, 0.45, 0.3) * knots * 0.6;
          ab = knots * 2.0;
        } else {
          float sr = 0.12 + 0.8 * pow(uExpand, 0.6);
          float k1 = fbm3(p * 4.0 + 3.0); float k2 = fbm3(p * 11.0 + 1.0);
          float ridge = 1.0 - abs(2.0 * fbm3(p * 6.0 + vec3(uExpand)) - 1.0);
          float shell = exp(-pow((r - sr) / (0.03 + 0.05 * k1), 2.0));
          float fil = pow(ridge, 9.0) * smoothstep(sr * 1.05, sr * 0.55, r) * smoothstep(sr * 0.1, sr * 0.45, r);
          float sync = exp(-r * r / (sr * sr * 0.16)) * 0.22;
          float flash = exp(-uExpand * 28.0) * exp(-r * r * 30.0) * 12.0;
          em = vec3(1.0, 0.3, 0.16) * fil * (0.5 + k2) * 3.2 + vec3(0.45, 0.6, 1.0) * sync * (0.5 + k1) + vec3(0.75, 0.82, 1.0) * shell * 0.3 * (0.4 + k2) + vec3(1.0) * flash;
          ab = fil * 1.2;
        }
      }
      void main() {
        vec3 ro = vC; vec3 rd = normalize(vP - vC);
        float b = dot(ro, rd); float c = dot(ro, ro) - 1.0; float h = b * b - c;
        if (h <= 0.0) discard;
        h = sqrt(h);
        float t0 = max(-b - h, 0.0); float t1 = -b + h;
        if (t1 <= t0) discard;
        float dt = (t1 - t0) / uSteps;
        float t = t0 + dt * hash(gl_FragCoord.xy + fract(uTime));
        vec3 col = vec3(0.0); float T = 1.0;
        for (int i = 0; i < 64; i++) {
          if (float(i) >= uSteps || T < 0.02) break;
          vec3 em; float ab;
          nebSample(ro + rd * t, em, ab);
          col += T * em * dt;
          T *= exp(-ab * dt);
          t += dt;
        }
        col = 1.0 - exp(-col * 1.4);
        float a = (1.0 - T) * uFade;
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)) * uFade, a);
      }`,
    transparent: true, depthWrite: false, side: THREE.BackSide,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  });
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 24), mat);
  mesh.layers.set(1);
  const frac = quality.tier === 'low' ? 0.34 : 0.5;
  const rt = new THREE.WebGLRenderTarget(2, 2, { depthBuffer: false });
  const comp = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({
    uniforms: { tMap: { value: rt.texture } },
    vertexShader: 'varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: 'uniform sampler2D tMap; varying vec2 vUv; void main() { gl_FragColor = texture2D(tMap, vUv); }',
    transparent: true, depthTest: false, depthWrite: false,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  }));
  comp.frustumCulled = false;
  comp.renderOrder = 6;
  const size = new THREE.Vector2();
  const clear = new THREE.Color();
  return {
    mesh, comp, uniforms: U,
    render(scene, camera) {
      comp.visible = mesh.visible;
      if (!mesh.visible) return;
      renderer.getDrawingBufferSize(size);
      const w = Math.max(2, Math.round(size.x * frac)); const h = Math.max(2, Math.round(size.y * frac));
      if (rt.width !== w || rt.height !== h) rt.setSize(w, h);
      const bg = scene.background; const prevRT = renderer.getRenderTarget();
      renderer.getClearColor(clear); const ca = renderer.getClearAlpha();
      scene.background = null; renderer.setClearColor(0x000000, 0);
      camera.layers.set(1);
      renderer.setRenderTarget(rt); renderer.clear(); renderer.render(scene, camera);
      camera.layers.set(0);
      renderer.setRenderTarget(prevRT); renderer.setClearColor(clear, ca); scene.background = bg;
    },
    dispose() { mesh.geometry.dispose(); mat.dispose(); rt.dispose(); comp.geometry.dispose(); comp.material.dispose(); },
  };
}
