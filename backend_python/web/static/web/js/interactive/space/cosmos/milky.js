import { THREE } from '../../core/engine.js';
import { shader, NOISE } from './shaders.js';
import { galToGlobal } from './astro.js';

// The Milky Way as it hangs over a dark site, painted in true galactic coordinates: an exponential
// disc that thickens towards Sagittarius, the bulge, the Scutum, Cygnus and Carina star clouds, the
// Great Rift and the Coalsack in dust, and the two Magellanic Clouds and Andromeda where they are.
// One sphere drawn behind everything, centred on the camera, so it never parallaxes.
export function createMilkySky(quality) {
  const gx = galToGlobal(1, 0, 0); const gy = galToGlobal(0, 1, 0); const gz = galToGlobal(0, 0, 1);
  const toGal = new THREE.Matrix3().set(gx.x, gx.y, gx.z, gy.x, gy.y, gy.z, gz.x, gz.y, gz.z);
  const mat = shader({
    uniforms: { uGal: { value: toGal }, uGain: { value: 1 } },
    vertexHead: 'varying vec3 vDir;',
    vertex: `vDir = position;
      gl_Position = projectionMatrix * viewMatrix * vec4(cameraPosition + mat3(modelMatrix) * position * 4.0e4, 1.0);`,
    fragmentHead: `uniform mat3 uGal; uniform float uGain; varying vec3 vDir; ${NOISE}
      float blob(float l, float b, float l0, float b0, float sl, float sb) {
        float dl = l - l0; dl = dl - 6.28318 * floor(dl / 6.28318 + 0.5);
        return exp(-(dl * dl) / (2.0 * sl * sl) - (b - b0) * (b - b0) / (2.0 * sb * sb));
      }`,
    fragment: `
      vec3 g = uGal * normalize(vDir);
      float l = atan(g.y, g.x);
      float b = asin(clamp(g.z, -1.0, 1.0));
      float al = abs(l);
      float n1 = fbm3(g * 5.0 + 1.7);
      float n2 = fbm3(g * 17.0 + 4.1);
      float n3 = fbm3(g * 46.0);
      float width = mix(0.055, 0.15, exp(-al * al / 1.1)) * (0.85 + 0.3 * n1);
      float disk = exp(-abs(b - 0.01 * sin(l * 2.0)) / width);
      float along = 0.22 + 0.78 * exp(-al * al / (2.0 * 0.9 * 0.9));
      float bulge = exp(-(l * l) / (2.0 * 0.17 * 0.17) - (b * b) / (2.0 * 0.11 * 0.11));
      float clouds = 0.9 * blob(l, b, 0.47, -0.03, 0.06, 0.04) + 0.7 * blob(l, b, 0.1, -0.05, 0.12, 0.06)
                   + 0.6 * blob(l, b, 1.36, 0.02, 0.18, 0.06) + 0.55 * blob(l, b, -1.27, -0.01, 0.16, 0.05);
      float light = (disk * along * (0.55 + 0.9 * n1) + bulge * 1.5 + clouds * (0.6 + 0.8 * n2)) * (0.7 + 0.6 * n3);
      float riftOn = smoothstep(-0.45, -0.15, l) * (1.0 - smoothstep(1.25, 1.55, l));
      float riftB = 0.03 + 0.015 * sin(l * 3.0 + 1.0);
      float rift = riftOn * exp(-pow((b - riftB) / (0.022 + 0.03 * exp(-al * al / 0.4)), 2.0));
      float lanes = smoothstep(0.45, 0.8, fbm3(g * 11.0 + 7.3)) * disk;
      float coal = blob(l, b, -1.04, -0.02, 0.05, 0.04);
      float dust = clamp(rift * (0.55 + 0.7 * n2) + lanes * 0.5 + coal * 0.85, 0.0, 0.93);
      light *= 1.0 - dust;
      float glow = blob(l, b, -1.39, -0.574, 0.07, 0.05) * 0.9 + blob(l, b, -1.0, -0.773, 0.045, 0.03) * 0.55 + blob(l, b, 2.115, -0.376, 0.012, 0.006) * 0.6;
      vec3 warm = vec3(1.0, 0.84, 0.66); vec3 cool = vec3(0.66, 0.74, 1.0);
      vec3 col = mix(cool, warm, clamp(bulge * 1.4 + 0.55 * exp(-al * al / 0.5) + 0.25 * n2, 0.0, 1.0)) * light;
      col += vec3(0.85, 0.82, 0.9) * glow * (0.6 + 0.6 * n2);
      col += vec3(0.9, 0.35, 0.45) * pow(max(0.0, n3 - 0.6), 2.0) * disk * along * 1.2;
      col *= 0.11 * uGain * uOpacity;
      gl_FragColor = vec4(col, 1.0);`,
    blending: THREE.AdditiveBlending,
    side: THREE.BackSide,
  });
  const seg = quality.tier === 'low' ? 32 : 64;
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(1, seg, seg / 2), mat);
  mesh.frustumCulled = false;
  mesh.renderOrder = -6;
  return mesh;
}
