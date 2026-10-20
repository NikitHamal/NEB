import { THREE } from '../../core/engine.js';
import { NZ, NOISE3D_GLSL } from '../../core/noise3d.js';

export const TISSUE_NOISE = `${NOISE3D_GLSL}
float tHash(vec3 p){p=fract(p*.1031);p+=dot(p,p.zyx+31.32);return fract((p.x+p.y)*p.z);}
float tNoise(vec3 p){ return nz4(p).g; }
float tFbm(vec3 p){ return nz4(p).r; }
vec2 tCell(vec3 p){ vec4 t = nz4(p); return vec2(t.a, t.a + t.b); }
`;

export function createTissue(opts = {}) {
  const uniforms = Object.assign({
    tNz: NZ,
    uTime: { value: 0 },
    uBeatV: { value: 0 },
    uBeatA: { value: 0 },
    uBreath: { value: 0 },
    uTextbook: { value: 0 },
    uXray: { value: 0 },
    uHi: { value: -1 },
    uHiAmt: { value: 0 },
  }, opts.uniforms || {});
  const mat = new THREE.MeshStandardMaterial({
    color: opts.color ?? 0xffffff,
    roughness: opts.roughness ?? 0.42,
    metalness: 0,
    side: opts.side ?? THREE.DoubleSide,
    transparent: false,
  });
  const coat = (opts.clearcoat ?? 0.7).toFixed(3);
  const coatPow = (2 / Math.pow(Math.max(0.04, opts.clearcoatRoughness ?? 0.22), 2)).toFixed(1);
  const sheen = (opts.sheen ?? 0.25).toFixed(3);
  const sheenC = new THREE.Color(opts.sheenColor ?? 0xffc4b8);
  const sheenV = `vec3(${sheenC.r.toFixed(3)}, ${sheenC.g.toFixed(3)}, ${sheenC.b.toFixed(3)})`;
  mat.userData.uniforms = uniforms;
  mat.customProgramCacheKey = () => `tissue-${opts.key || 'x'}`;
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, uniforms);
    const head = `uniform float uTime; uniform float uBeatV; uniform float uBeatA; uniform float uBreath; uniform float uTextbook; uniform float uXray; uniform float uHi; uniform float uHiAmt;
      varying vec3 vObj; varying float vKind; varying float vFat; varying float vPart;\n`;
    sh.vertexShader = head + `attribute float kind; attribute float fat; attribute float part; ${opts.vertexAttrs || ''}\n` + sh.vertexShader
      .replace('#include <begin_vertex>', `#include <begin_vertex>
        vObj = position; vKind = kind; vFat = fat; vPart = part;
        ${opts.vertex || ''}`)
      .replace('#include <beginnormal_vertex>', `#include <beginnormal_vertex>
        ${opts.normalVertex || ''}`);
    sh.fragmentShader = head + TISSUE_NOISE + (opts.fragmentHead || '') + '\n' + sh.fragmentShader
      .replace('#include <color_fragment>', `#include <color_fragment>
        ${opts.color_fragment}`)
      .replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>
        {
          float h = ${opts.bump || 'tFbm(vObj * 3.0) * 0.6 + tNoise(vObj * 14.0) * 0.4'};
          vec3 dpdx = dFdx(-vViewPosition); vec3 dpdy = dFdy(-vViewPosition);
          float dhdx = dFdx(h); float dhdy = dFdy(h);
          vec3 r1 = cross(dpdy, normal); vec3 r2 = cross(normal, dpdx);
          float det = dot(dpdx, r1);
          vec3 grad = sign(det) * (dhdx * r1 + dhdy * r2);
          normal = normalize(abs(det) * normal - grad * ${(opts.bumpAmt ?? 0.012).toFixed(4)});
        }`)
      .replace('#include <opaque_fragment>', `
        {
          vec3 V = normalize(vViewPosition);
          float rim = pow(1.0 - clamp(abs(dot(normal, V)), 0.0, 1.0), 2.5);
          outgoingLight += ${opts.sss || 'vec3(0.55, 0.06, 0.04)'} * rim * 0.35;
          #if NUM_DIR_LIGHTS > 0
          {
            vec3 Lc = directionalLights[0].direction;
            vec3 Hc = normalize(Lc + V);
            float nh = max(dot(normal, Hc), 0.0);
            float fc = 0.04 + 0.96 * pow(1.0 - max(dot(V, Hc), 0.0), 5.0);
            outgoingLight += directionalLights[0].color * (pow(nh, ${coatPow}) * ${coat} * fc * 6.0 * step(0.0, dot(normal, Lc)));
          }
          #endif
          outgoingLight += ${sheenV} * ${sheen} * rim * 0.12 * (diffuseColor.rgb + 0.2);
          outgoingLight += vec3(0.25, 0.55, 1.0) * uHiAmt * step(abs(vPart - uHi), 0.5) * (0.35 + rim);
          float fres = mix(1.0, 0.08 + 0.92 * pow(rim, 0.6), uXray);
          diffuseColor.a *= fres;
          ${opts.cap ? `if (!gl_FrontFacing) outgoingLight = ${opts.cap};` : ''}
        }
        #include <opaque_fragment>`);
  };
  return mat;
}

export function setXray(mat, x) {
  mat.userData.uniforms.uXray.value = x;
  const t = x > 0.01;
  if (mat.userData.side0 === undefined) mat.userData.side0 = mat.side;
  if (mat.transparent !== t) { mat.transparent = t; mat.side = t ? THREE.FrontSide : mat.userData.side0; mat.needsUpdate = true; }
  mat.depthWrite = !t;
}
