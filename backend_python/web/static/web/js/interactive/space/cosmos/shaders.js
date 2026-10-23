import { THREE } from '../../core/engine.js';
import { NZ, NOISE3D_GLSL } from '../../core/noise3d.js';

export const NOISE = `${NOISE3D_GLSL}
vec3 hash33(vec3 p){p=fract(p*vec3(.1031,.1030,.0973));p+=dot(p,p.yxz+33.33);return fract((p.xxy+p.yxx)*p.zyx);}
float hash13(vec3 p){p=fract(p*.1031);p+=dot(p,p.zyx+31.32);return fract((p.x+p.y)*p.z);}
float vnoise(vec3 p){ return nz4(p).g; }
float fbm3(vec3 p){ return nz4(p).r; }
`;

// Single scattering in a 100 km shell: Rayleigh and Mie with their real coefficients and scale
// heights, in Earth radii. The surface shader composes it in linear light (aerial perspective over
// the disc); the shell pass draws only the sky beyond the limb, over black space.
export const RA = 1 + 100 / 6371;
export const SCATTER = `
      const float RA = ${RA.toFixed(6)};
      const vec3 BR = vec3(36.95, 86.01, 210.9);
      const float BM = 133.8;
      const float HR = ${(8 / 6371).toFixed(7)};
      const float HM = ${(1.2 / 6371).toFixed(7)};
      vec2 hitSphere(vec3 o, vec3 d, float r) { float b = dot(o, d); float c = dot(o, o) - r * r; float h = b * b - c; if (h < 0.0) return vec2(1e9, -1e9); h = sqrt(h); return vec2(-b - h, -b + h); }
      vec2 depthTo(vec3 p, vec3 s) {
        vec2 e = hitSphere(p, s, RA); float L = max(e.y, 0.0); float dl = L / 4.0; vec2 od = vec2(0.0);
        for (int j = 0; j < 4; j++) { float hh = length(p + s * dl * (float(j) + 0.5)) - 1.0; od += exp(-vec2(hh / HR, hh / HM)) * dl; }
        return od;
      }
      void scatter(vec3 ro, vec3 rd, float tEnd, vec3 s, int n, out vec3 L, out vec3 T) {
        vec2 a = hitSphere(ro, rd, RA);
        float t0 = max(a.x, 0.0); float t1 = min(a.y, tEnd);
        L = vec3(0.0); T = vec3(1.0);
        if (t1 <= t0) return;
        float dt = (t1 - t0) / float(n);
        vec3 sumR = vec3(0.0); vec3 sumM = vec3(0.0); vec2 odV = vec2(0.0);
        for (int i = 0; i < 12; i++) {
          if (i >= n) break;
          vec3 p = ro + rd * (t0 + dt * (float(i) + 0.5));
          float hh = max(length(p) - 1.0, 0.0);
          vec2 dens = exp(-vec2(hh / HR, hh / HM)) * dt;
          odV += dens;
          if (hitSphere(p, s, 0.9995).x > 0.0) continue;
          vec2 odL = depthTo(p, s);
          vec3 att = exp(-(BR * (odV.x + odL.x) + BM * 1.1 * (odV.y + odL.y)));
          sumR += dens.x * att; sumM += dens.y * att;
        }
        float mu = dot(rd, s);
        float gg = 0.76;
        float pm = 0.1193662 * ((1.0 - gg * gg) * (1.0 + mu * mu)) / ((2.0 + gg * gg) * pow(1.0 + gg * gg - 2.0 * gg * mu, 1.5));
        L = sumR * BR * 0.0596831 * (1.0 + mu * mu) + sumM * BM * pm;
        T = exp(-(BR * odV.x + BM * 1.1 * odV.y));
      }`;

export const LOGDEPTH_V = ['#include <common>', '#include <logdepthbuf_pars_vertex>'].join('\n');
export const LOGDEPTH_VM = '#include <logdepthbuf_vertex>';
export const LOGDEPTH_F = ['#include <common>', '#include <logdepthbuf_pars_fragment>'].join('\n');
export const LOGDEPTH_FM = '#include <logdepthbuf_fragment>';

export function shader(opts) {
  const mat = new THREE.ShaderMaterial({
    uniforms: Object.assign({ uOpacity: { value: 1 }, tNz: NZ }, opts.uniforms || {}),
    vertexShader: `${LOGDEPTH_V}\n${opts.vertexHead || ''}\nvoid main(){\n${opts.vertex}\n${LOGDEPTH_VM}\n}`,
    fragmentShader: `${LOGDEPTH_F}\nuniform float uOpacity;\n${opts.fragmentHead || ''}\nvoid main(){\n${LOGDEPTH_FM}\n${opts.fragment}\n}`,
    transparent: opts.transparent !== false,
    depthWrite: opts.depthWrite ?? false,
    depthTest: opts.depthTest ?? true,
    blending: opts.blending ?? THREE.NormalBlending,
    side: opts.side ?? THREE.FrontSide,
  });
  mat.toneMapped = false;
  return mat;
}

export function pointsMaterial(opts = {}) {
  return shader({
    uniforms: {
      uScale: { value: 1 },
      uPx: { value: 1 },
      uMin: { value: opts.min ?? 0.6 },
      uMax: { value: opts.max ?? 24 },
      uGain: { value: opts.gain ?? 1 },
      uCore: { value: opts.core ?? 0.18 },
    },
    vertexHead: `attribute vec3 color; attribute float size; uniform float uScale; uniform float uPx; uniform float uMin; uniform float uMax; uniform float uGain; varying vec3 vColor; varying float vFade;`,
    vertex: `
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      float px = size * uScale * uPx / max(1e-6, -mv.z);
      float clamped = clamp(px, uMin, uMax);
      vFade = uGain * min(1.0, px / uMin) * min(1.0, 2.5 * uMax / max(px, 1.0));
      vColor = color;
      gl_PointSize = clamped;
      gl_Position = projectionMatrix * mv;`,
    fragmentHead: 'uniform float uCore; varying vec3 vColor; varying float vFade;',
    fragment: `
      vec2 d = gl_PointCoord - 0.5;
      float r2 = dot(d, d) * 4.0;
      float a = exp(-r2 * 5.5) + uCore * exp(-r2 * 40.0);
      if (a < 0.003) discard;
      gl_FragColor = vec4(vColor * a * vFade * uOpacity, 1.0);`,
    blending: THREE.AdditiveBlending,
  });
}

export function dustMaterial() {
  return shader({
    uniforms: { uScale: { value: 1 }, uPx: { value: 1 } },
    vertexHead: 'attribute float size; uniform float uScale; uniform float uPx; varying float vA;',
    vertex: `
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      float px = size * uScale * uPx / max(1e-6, -mv.z);
      vA = min(1.0, px / 3.0) * min(1.0, 160.0 / max(px, 1.0));
      gl_PointSize = clamp(px, 1.0, 160.0);
      gl_Position = projectionMatrix * mv;`,
    fragmentHead: 'varying float vA;',
    fragment: `
      vec2 d = gl_PointCoord - 0.5;
      float a = exp(-dot(d, d) * 14.0) * 0.16 * vA * uOpacity;
      if (a < 0.004) discard;
      gl_FragColor = vec4(0.05, 0.03, 0.02, a);`,
  });
}

export function makePoints(positions, colors, sizes, material) {
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  if (colors) geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  geo.computeBoundingSphere();
  const pts = new THREE.Points(geo, material);
  pts.frustumCulled = false;
  return pts;
}

let GLOW = null;
export function glowTexture() {
  if (GLOW) return GLOW;
  const s = 128;
  const c = document.createElement('canvas');
  c.width = s; c.height = s;
  const g = c.getContext('2d');
  const img = g.createImageData(s, s);
  for (let y = 0; y < s; y++) {
    for (let x = 0; x < s; x++) {
      const dx = (x + 0.5) / s * 2 - 1;
      const dy = (y + 0.5) / s * 2 - 1;
      const r = Math.sqrt(dx * dx + dy * dy);
      const v = Math.max(0, Math.exp(-r * r * 9) * 0.85 + Math.exp(-r * 3.2) * 0.3 * (1 - r)) ;
      const i = (y * s + x) * 4;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = 255;
      img.data[i + 3] = Math.min(255, v * 255);
    }
  }
  g.putImageData(img, 0, 0);
  GLOW = new THREE.CanvasTexture(c);
  GLOW.colorSpace = THREE.SRGBColorSpace;
  return GLOW;
}

export function glowSprite(color, size, opacity = 1) {
  const mat = new THREE.SpriteMaterial({
    map: glowTexture(), color, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity,
  });
  mat.toneMapped = false;
  const s = new THREE.Sprite(mat);
  s.scale.setScalar(size);
  s.userData.baseOpacity = opacity;
  return s;
}

export function lineLoop(points, color, opacity = 0.5) {
  const geo = new THREE.BufferGeometry().setFromPoints(points);
  const mat = shader({
    uniforms: { uColor: { value: new THREE.Color(color) }, uAlpha: { value: opacity } },
    vertex: 'gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
    fragmentHead: 'uniform vec3 uColor; uniform float uAlpha;',
    fragment: 'gl_FragColor = vec4(uColor, uAlpha * uOpacity);',
  });
  const line = new THREE.LineLoop(geo, mat);
  line.frustumCulled = false;
  return line;
}

export function setOpacity(obj, a) {
  obj.visible = a > 0.002;
  if (!obj.visible) return;
  obj.traverse((o) => {
    const m = o.material;
    if (!m) return;
    if (m.uniforms && m.uniforms.uOpacity) m.uniforms.uOpacity.value = a;
    else if ('opacity' in m && m.userData.fade !== false) {
      const base = o.userData.baseOpacity ?? 1;
      if (m.userData.baseT === undefined) { m.userData.baseT = m.transparent; m.userData.baseDW = m.depthWrite; }
      m.opacity = base * a;
      m.transparent = m.userData.baseT || a < 0.999;
      m.depthWrite = a < 0.999 ? false : m.userData.baseDW;
    }
  });
}
