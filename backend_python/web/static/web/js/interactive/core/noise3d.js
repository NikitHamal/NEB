import * as THREE from '../../vendor/three.module.min.js';

const N = 64;
const P = 8;
const CACHE = new WeakMap();
export const NZ = { value: null };

const GEN = `
precision highp float; precision highp int;
uniform float uZ;
in vec2 vUv;
out vec4 outColor;
float h(ivec3 c, int s, int per) {
  c = ((c % per) + per) % per;
  uint x = uint(c.x) * 374761393u + uint(c.y) * 668265263u + uint(c.z) * 2147483647u + uint(s) * 1274126177u;
  x = (x ^ (x >> 13u)) * 1274126177u;
  x = x ^ (x >> 16u);
  return float(x) / 4294967295.0;
}
float vn(vec3 p, int per, int s) {
  ivec3 i = ivec3(floor(p)); vec3 f = fract(p); vec3 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(h(i, s, per), h(i + ivec3(1,0,0), s, per), u.x), mix(h(i + ivec3(0,1,0), s, per), h(i + ivec3(1,1,0), s, per), u.x), u.y),
             mix(mix(h(i + ivec3(0,0,1), s, per), h(i + ivec3(1,0,1), s, per), u.x), mix(h(i + ivec3(0,1,1), s, per), h(i + ivec3(1,1,1), s, per), u.x), u.y), u.z);
}
void main() {
  vec3 p = vec3(vUv, (uZ + 0.5) / ${N}.0) * ${P}.0;
  float f = 0.0; float a = 0.5; float fr = 1.0; int per = ${P};
  for (int o = 0; o < 4; o++) { f += a * vn(p * fr, per, 10 + o); a *= 0.5; fr *= 2.0; per *= 2; }
  float g = vn(p, ${P}, 20);
  ivec3 c = ivec3(floor(p));
  float d1 = 9.0; float d2 = 9.0;
  for (int z = -1; z <= 1; z++) for (int y = -1; y <= 1; y++) for (int x = -1; x <= 1; x++) {
    ivec3 q = c + ivec3(x, y, z);
    vec3 fp = vec3(q) + vec3(h(q, 2, ${P}), h(q, 3, ${P}), h(q, 4, ${P}));
    float d = length(fp - p);
    if (d < d1) { d2 = d1; d1 = d; } else if (d < d2) d2 = d;
  }
  outColor = vec4(min(1.0, f * 1.06), g, min(1.0, d2 - d1), min(1.0, d1));
}`;

export function noise3D(renderer) {
  if (!renderer) return null;
  if (CACHE.has(renderer)) { NZ.value = CACHE.get(renderer); return NZ.value; }
  let tex = null;
  try {
    const rt = new THREE.WebGL3DRenderTarget(N, N, N, { depthBuffer: false });
    const t = rt.texture;
    t.format = THREE.RGBAFormat; t.type = THREE.UnsignedByteType;
    t.wrapS = t.wrapT = t.wrapR = THREE.RepeatWrapping;
    t.magFilter = THREE.LinearFilter; t.minFilter = THREE.LinearMipmapLinearFilter;
    t.generateMipmaps = false;
    const mat = new THREE.RawShaderMaterial({
      glslVersion: THREE.GLSL3,
      uniforms: { uZ: { value: 0 } },
      vertexShader: 'in vec3 position; in vec2 uv; out vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy * 2.0, 0.0, 1.0); }',
      fragmentShader: GEN,
      depthTest: false, depthWrite: false,
    });
    const quad = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat);
    quad.frustumCulled = false;
    const sc = new THREE.Scene(); sc.add(quad);
    const cam = new THREE.Camera();
    const prev = renderer.getRenderTarget();
    const prevAuto = renderer.autoClear;
    renderer.autoClear = false;
    for (let z = 0; z < N; z++) {
      mat.uniforms.uZ.value = z;
      renderer.setRenderTarget(rt, z);
      renderer.render(sc, cam);
    }
    renderer.setRenderTarget(prev);
    const gl = renderer.getContext();
    const wt = renderer.properties.get(t).__webglTexture;
    if (wt) {
      renderer.state.bindTexture(gl.TEXTURE_3D, wt);
      gl.generateMipmap(gl.TEXTURE_3D);
      renderer.state.bindTexture(gl.TEXTURE_3D, null);
    }
    renderer.autoClear = prevAuto;
    mat.dispose(); quad.geometry.dispose();
    t.userData = { sharedFx: true };
    tex = t;
  } catch (e) {
    tex = null;
  }
  CACHE.set(renderer, tex);
  NZ.value = tex;
  return tex;
}

export const NOISE3D_GLSL = `
uniform highp sampler3D tNz;
vec4 nz4(vec3 p){ return texture(tNz, p * ${(1 / P).toFixed(4)}); }
`;
