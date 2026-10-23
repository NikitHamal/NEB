import { THREE } from '../../core/engine.js';
import { NOISE, shader } from './shaders.js';
import { R_EARTH } from './astro.js';

// The sea of cloud the summit so often stands above: a deck near 6 300 m that fills the valleys and
// parts around every ridge. Where the real terrain (the regional DEM, baked to a texture) rises to
// meet it the deck thins out, so peaks break through without a hard line, and low valleys stay full.
export function createCloudSea(height, sunLocal) {
  const { n, h, px, ax, ay, scale } = height;
  const data = new Uint8Array(n * n);
  for (let i = 0; i < n * n; i++) data[i] = Math.max(0, Math.min(255, Math.round(h[i] * scale / 9000 * 255)));
  const tex = new THREE.DataTexture(data, n, n, THREE.RedFormat, THREE.UnsignedByteType);
  tex.magFilter = THREE.LinearFilter; tex.minFilter = THREE.LinearFilter; tex.needsUpdate = true;
  const span = 140000;
  const geo = new THREE.PlaneGeometry(span, span, 96, 96);
  geo.rotateX(-Math.PI / 2);
  const mat = shader({
    uniforms: {
      uH: { value: tex }, uSun: { value: sunLocal.clone() }, uTime: { value: 0 }, uMpu: { value: 1 }, uVis: { value: 1 },
      uDem: { value: new THREE.Vector4(1 / px, ax + 0.5, ay + 0.5, 1 / n) },
    },
    vertexHead: 'varying vec3 vP; varying float vDist;',
    vertex: `vec3 p = position; p.y = 6300.0;
      vP = p;
      p.y -= dot(p.xz, p.xz) / (2.0 * ${R_EARTH.toFixed(1)});
      vec4 mv = modelViewMatrix * vec4(p, 1.0); vDist = -mv.z;
      gl_Position = projectionMatrix * mv;`,
    fragmentHead: `uniform sampler2D uH; uniform vec3 uSun; uniform float uTime; uniform float uMpu; uniform float uVis; uniform vec4 uDem;
      varying vec3 vP; varying float vDist; ${NOISE}
      float ground(vec2 xz) { return texture2D(uH, (xz * uDem.x + uDem.yz) * uDem.w).r * 9000.0; }`,
    fragment: `
      vec2 xz = vP.xz;
      float hg = ground(xz);
      vec3 q = vec3(xz.x / 7000.0 + uTime * 0.004, 0.0, xz.y / 7000.0);
      float big = fbm3(q);
      float mid = fbm3(q * 3.1 + vec3(2.3, 0.0, 1.1) + vec3(uTime * 0.006, 0.0, 0.0));
      float fine = fbm3(q * 11.0 + vec3(0.0, 0.0, uTime * 0.01));
      float valley = smoothstep(6200.0, 4200.0, hg);
      float cover = big * 0.55 + mid * 0.3 + fine * 0.15 + valley * 0.22 - 0.1;
      float clear = smoothstep(6600.0, 5700.0, hg);
      float a = smoothstep(0.38, 0.6, cover) * clear;
      float r = length(xz);
      a *= smoothstep(68000.0, 40000.0, r) * uVis;
      if (a < 0.01) discard;
      float e = 260.0;
      float gx = fbm3(q + vec3(0.02, 0.0, 0.0)) - big; float gz = fbm3(q + vec3(0.0, 0.0, 0.02)) - big;
      vec3 nrm = normalize(vec3(-gx * 30.0, 1.0, -gz * 30.0) + vec3(mid - 0.5, 0.0, fine - 0.5) * 0.6);
      float ndl = max(0.0, dot(nrm, normalize(uSun)));
      float thick = smoothstep(0.38, 0.85, cover);
      vec3 sunC = vec3(1.0, 0.96, 0.9);
      vec3 col = vec3(0.92, 0.94, 0.98) * (0.55 + 0.75 * ndl) * mix(0.82, 1.0, thick);
      col += vec3(0.25, 0.32, 0.45) * (1.0 - ndl) * 0.35;
      col *= mix(vec3(0.82, 0.86, 0.95), sunC, 0.6 + 0.4 * ndl);
      float meters = min(vDist * uMpu, 60000.0);
      col = mix(col, vec3(0.62, 0.72, 0.86), (1.0 - exp(-meters / 90000.0)) * 0.6);
      col = col / (col + vec3(0.85)) * 1.25;
      gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), a * uOpacity);`,
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.renderOrder = 2;
  mesh.frustumCulled = false;
  return {
    mesh,
    update(logW, mpu, t) {
      mat.uniforms.uMpu.value = mpu; mat.uniforms.uTime.value = t;
      mat.uniforms.uVis.value = 1 - Math.min(1, Math.max(0, (logW - 4.3) / 0.8));
      mesh.visible = logW < 5.1;
    },
    dispose() { geo.dispose(); mat.dispose(); tex.dispose(); },
  };
}
