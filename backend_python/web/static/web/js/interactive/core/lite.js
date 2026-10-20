import * as THREE from '../../vendor/three.module.min.js';

function v3(c) { return `vec3(${c.r.toFixed(3)}, ${c.g.toFixed(3)}, ${c.b.toFixed(3)})`; }

function convert(src) {
  if (src.userData.lite) return src;
  const glass = (src.transmission || 0) > 0.01 || (src.transparent && (src.clearcoat || 0) > 0.5 && (src.opacity ?? 1) < 0.75);
  const dst = src;
  const coat = src.clearcoat || 0;
  const coatR = Math.max(0.04, src.clearcoatRoughness ?? 0.1);
  const sheen = src.sheen || 0;
  const sheenC = src.sheenColor ? src.sheenColor.clone() : new THREE.Color(1, 1, 1);
  const prev = src.onBeforeCompile && src.onBeforeCompile !== THREE.Material.prototype.onBeforeCompile ? src.onBeforeCompile : null;
  const prevKey = src.customProgramCacheKey && src.customProgramCacheKey !== THREE.Material.prototype.customProgramCacheKey ? src.customProgramCacheKey() : '';
  src.userData.lite = true;
  src.clearcoat = 0; src.sheen = 0; src.iridescence = 0;
  if (glass) {
    dst.transparent = true;
    dst.depthWrite = false;
    dst.roughness = Math.min(dst.roughness, 0.08);
    if (!src.transmission) dst.opacity = Math.min(1, (src.opacity ?? 1) * 1.8);
    dst.metalness = 0;
    dst.envMapIntensity = (src.envMapIntensity ?? 1) * 1.6;
    if (src.attenuationColor && src.attenuationDistance < 1e6) dst.color.copy(src.attenuationColor).lerp(new THREE.Color(1, 1, 1), 0.35);
    dst.transmission = 0;
    dst.thickness = 0;
  }
  const key = `lite-${glass ? 'g' : ''}${coat ? 'c' : ''}${sheen ? 's' : ''}-${coat.toFixed(2)}-${coatR.toFixed(2)}-${sheen.toFixed(2)}-${sheenC.getHexString()}-${prevKey}`;
  dst.customProgramCacheKey = () => key;
  if (coat || sheen || glass || prev) {
    dst.onBeforeCompile = (sh, r) => {
      if (prev) prev.call(dst, sh, r);
      if (!(coat || sheen || glass)) return;
      sh.fragmentShader = sh.fragmentShader.replace('#include <opaque_fragment>', `
        {
          vec3 Vv = normalize(vViewPosition);
          float ndv = clamp(abs(dot(normal, Vv)), 0.0, 1.0);
          float rimv = pow(1.0 - ndv, 2.5);
          ${coat ? `#if NUM_DIR_LIGHTS > 0
          for (int li = 0; li < NUM_DIR_LIGHTS; li++) {
            vec3 Lc = directionalLights[li].direction;
            vec3 Hc = normalize(Lc + Vv);
            float fc = 0.04 + 0.96 * pow(1.0 - max(dot(Vv, Hc), 0.0), 5.0);
            outgoingLight += directionalLights[li].color * pow(max(dot(normal, Hc), 0.0), ${(2 / (coatR * coatR)).toFixed(1)}) * ${coat.toFixed(3)} * fc * 5.0 * step(0.0, dot(normal, Lc));
          }
          #endif
          outgoingLight += vec3(0.04) * ${coat.toFixed(3)} * rimv;` : ''}
          ${sheen ? `outgoingLight += ${v3(sheenC)} * ${sheen.toFixed(3)} * rimv * 0.35 * (diffuseColor.rgb + 0.15);` : ''}
          ${glass ? 'diffuseColor.a = clamp(diffuseColor.a * (0.10 + 0.85 * pow(1.0 - ndv, 3.0)), 0.0, 1.0); outgoingLight += vec3(0.9) * pow(1.0 - ndv, 4.0) * 0.25;' : ''}
        }
        #include <opaque_fragment>`);
    };
  }
  return dst;
}

export function liteScene(root, opts = {}) {
  root.traverse((o) => {
    if (!o.material) return;
    const swap = (m) => {
      if (!m || !m.isMeshPhysicalMaterial || m.userData.keepPhysical || m.userData.lite) return m;
      convert(m); m.needsUpdate = true;
      return m;
    };
    if (Array.isArray(o.material)) o.material.forEach(swap);
    else swap(o.material);
  });
}

export function liteMaterial(m) { if (m && m.isMeshPhysicalMaterial && !m.userData.lite) { convert(m); m.needsUpdate = true; } return m; }
