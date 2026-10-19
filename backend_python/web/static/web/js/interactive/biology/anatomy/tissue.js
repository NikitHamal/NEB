import { THREE } from '../../core/engine.js';

export const TISSUE_NOISE = `
float tHash(vec3 p){p=fract(p*.1031);p+=dot(p,p.zyx+31.32);return fract((p.x+p.y)*p.z);}
float tNoise(vec3 p){vec3 i=floor(p);vec3 f=fract(p);f=f*f*(3.-2.*f);
  return mix(mix(mix(tHash(i),tHash(i+vec3(1,0,0)),f.x),mix(tHash(i+vec3(0,1,0)),tHash(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(tHash(i+vec3(0,0,1)),tHash(i+vec3(1,0,1)),f.x),mix(tHash(i+vec3(0,1,1)),tHash(i+vec3(1,1,1)),f.x),f.y),f.z);}
float tFbm(vec3 p){float a=.5,s=0.;for(int i=0;i<4;i++){s+=a*tNoise(p);p=p*2.07+vec3(3.1,1.7,5.3);a*=.5;}return s;}
vec2 tCell(vec3 p){vec3 i=floor(p);vec3 f=fract(p);float d1=9.,d2=9.;
  for(int z=-1;z<=1;z++)for(int y=-1;y<=1;y++)for(int x=-1;x<=1;x++){vec3 g=vec3(x,y,z);vec3 o=vec3(tHash(i+g),tHash(i+g+11.3),tHash(i+g+27.1));float d=length(g+o-f);if(d<d1){d2=d1;d1=d;}else if(d<d2)d2=d;}
  return vec2(d1,d2);}
`;

export function createTissue(opts = {}) {
  const uniforms = Object.assign({
    uTime: { value: 0 },
    uBeatV: { value: 0 },
    uBeatA: { value: 0 },
    uBreath: { value: 0 },
    uTextbook: { value: 0 },
    uXray: { value: 0 },
    uHi: { value: -1 },
    uHiAmt: { value: 0 },
  }, opts.uniforms || {});
  const mat = new THREE.MeshPhysicalMaterial({
    color: opts.color ?? 0xffffff,
    roughness: opts.roughness ?? 0.42,
    metalness: 0,
    clearcoat: opts.clearcoat ?? 0.7,
    clearcoatRoughness: opts.clearcoatRoughness ?? 0.22,
    sheen: opts.sheen ?? 0.25,
    sheenColor: new THREE.Color(opts.sheenColor ?? 0xffc4b8),
    sheenRoughness: 0.6,
    side: opts.side ?? THREE.DoubleSide,
    transparent: false,
  });
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
