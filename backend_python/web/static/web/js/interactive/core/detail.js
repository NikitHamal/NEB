import * as THREE from '../../vendor/three.module.min.js';
import { NZ, NOISE3D_GLSL } from './noise3d.js';

function v3(c) { const k = new THREE.Color(c); return `vec3(${k.r.toFixed(3)}, ${k.g.toFixed(3)}, ${k.b.toFixed(3)})`; }

export function detail(mat, o = {}) {
  if (!mat || mat.userData.detail) return mat;
  const scale = (o.scale ?? 30).toFixed(3);
  const bump = (o.bump ?? 0.003).toFixed(5);
  const mottle = (o.mottle ?? 0.18).toFixed(3);
  const speck = (o.speck ?? 0).toFixed(3);
  const sss = o.sss != null ? v3(o.sss) : null;
  const rough = (o.roughVar ?? 0).toFixed(3);
  const key = `detail-${scale}-${bump}-${mottle}-${speck}-${sss}-${rough}`;
  const prev = mat.onBeforeCompile && mat.onBeforeCompile !== THREE.Material.prototype.onBeforeCompile ? mat.onBeforeCompile : null;
  const prevKey = mat.customProgramCacheKey && mat.customProgramCacheKey !== THREE.Material.prototype.customProgramCacheKey ? mat.customProgramCacheKey() : '';
  mat.userData.detail = true;
  mat.onBeforeCompile = (sh, r) => {
    if (prev) prev.call(mat, sh, r);
    sh.uniforms.tNz = NZ;
    sh.vertexShader = 'varying vec3 vDtl;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\nvDtl = position;');
    sh.fragmentShader = `varying vec3 vDtl;\n${NOISE3D_GLSL}\n` + sh.fragmentShader
      .replace('#include <color_fragment>', `#include <color_fragment>
        vec4 dN = nz4(vDtl * ${scale});
        diffuseColor.rgb *= 1.0 - ${mottle} * 0.5 + ${mottle} * dN.r;
        diffuseColor.rgb *= 1.0 - ${speck} * step(0.86, nz4(vDtl * ${scale} * 7.3).g);`)
      .replace('#include <roughnessmap_fragment>', `#include <roughnessmap_fragment>
        roughnessFactor = clamp(roughnessFactor * (1.0 + ${rough} * (nz4(vDtl * ${scale} * 0.5).g - 0.5) * 2.0), 0.02, 1.0);`)
      .replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>
        {
          float h = nz4(vDtl * ${scale} * 3.1).g * 0.6 + nz4(vDtl * ${scale}).r * 0.4;
          vec3 dpdx = dFdx(-vViewPosition); vec3 dpdy = dFdy(-vViewPosition);
          float dhdx = dFdx(h); float dhdy = dFdy(h);
          vec3 r1 = cross(dpdy, normal); vec3 r2 = cross(normal, dpdx);
          float det = dot(dpdx, r1);
          normal = normalize(abs(det) * normal - sign(det) * (dhdx * r1 + dhdy * r2) * ${bump});
        }`)
      .replace('#include <opaque_fragment>', sss ? `{
          float rimD = pow(1.0 - clamp(abs(dot(normal, normalize(vViewPosition))), 0.0, 1.0), 2.5);
          outgoingLight += ${sss} * rimD * 0.3 * (diffuseColor.rgb + 0.1);
        }
        #include <opaque_fragment>` : '#include <opaque_fragment>');
  };
  mat.customProgramCacheKey = () => `${key}|${prevKey}`;
  mat.needsUpdate = true;
  return mat;
}

export function roomEnvironment(renderer, scene, opts = {}) {
  try {
    const pm = new THREE.PMREMGenerator(renderer);
    const prevFog = scene.fog; scene.fog = null;
    const rt = pm.fromScene(scene, opts.blur ?? 0.035, 0.1, 100);
    scene.fog = prevFog;
    pm.dispose();
    rt.texture.userData = { sharedFx: true };
    return rt.texture;
  } catch (e) { return null; }
}
