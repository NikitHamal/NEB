import { THREE, createEngine, createOrbitControls } from '../../core/engine.js';
import { NZ } from '../../core/noise3d.js';
import { NOISE, SCATTER } from '../../space/cosmos/shaders.js';

export { THREE };

// An outdoor school sports field for the mechanics labs: grass with chalked metre lines, foothills
// round the horizon, and the sky computed by the same single-scattering atmosphere as Scale of the
// Universe (from 1 400 m, the height of Kathmandu), with a sun that casts real shadows. 1 unit = 1 m.
export function createField(stage, { camera = [0, 6, 28], target = [12, 4, 0], maxDistance = 400 } = {}) {
  const engine = createEngine(stage, { noise: true, alpha: false, environment: true, fov: 40, near: 0.1, far: 6000, shadows: true, exposure: 1.0 });
  if (!engine) return null;
  const { scene, renderer, quality } = engine;
  const cam = engine.camera;
  if (quality.tier !== 'low') { renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; }
  const sun = new THREE.Vector3(-0.35, 0.62, 0.7).normalize();
  const key = new THREE.DirectionalLight(0xfff2df, 3.0); key.position.copy(sun).multiplyScalar(120);
  key.castShadow = quality.tier !== 'low';
  key.shadow.mapSize.set(2048, 2048); const sc = key.shadow.camera; sc.left = -60; sc.right = 60; sc.top = 60; sc.bottom = -60; sc.near = 1; sc.far = 400; key.shadow.bias = -0.0004; key.shadow.normalBias = 0.03;
  scene.add(key, key.target, new THREE.HemisphereLight(0xbcd4ff, 0x4a5a2a, 0.9));
  const skyMat = new THREE.ShaderMaterial({
    uniforms: { uSun: { value: sun } },
    vertexShader: 'varying vec3 vDir; void main() { vDir = normalize((modelMatrix * vec4(position, 1.0)).xyz - cameraPosition); gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform vec3 uSun; varying vec3 vDir; ${SCATTER}
      void main() {
        vec3 rd = normalize(vDir); vec3 ro = vec3(0.0, 1.0 + 1.4 / 6371.0, 0.0);
        rd.y = max(rd.y, -0.02);
        vec3 L; vec3 T; scatter(ro, normalize(rd), 1e9, uSun, 10, L, T);
        vec3 col = L * 18.0;
        float mu = dot(normalize(rd), uSun);
        col += T * smoothstep(0.99995, 0.99999, mu) * 50.0 + T * pow(max(mu, 0.0), 600.0) * 2.0;
        col = 1.0 - exp(-col * 1.05);
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
      }`,
    side: THREE.BackSide, depthWrite: false,
  });
  const sky = new THREE.Mesh(new THREE.SphereGeometry(4000, 48, 24), skyMat); sky.renderOrder = -10; scene.add(sky);
  const grassMat = new THREE.MeshStandardMaterial({ color: 0x5a8a34, roughness: 0.95 });
  grassMat.onBeforeCompile = (sh) => {
    sh.uniforms.tNz = NZ;
    sh.vertexShader = 'varying vec3 vW;\n' + sh.vertexShader.replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvW = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = `varying vec3 vW;\n${NOISE}\n` + sh.fragmentShader.replace('#include <color_fragment>', `#include <color_fragment>
      float n = fbm3(vec3(vW.xz * 0.05, 1.0)); float f = fbm3(vec3(vW.xz * 0.8, 2.0));
      float stripe = step(0.5, fract(vW.x / 10.0)) * 0.06;
      diffuseColor.rgb *= 0.75 + 0.4 * n + 0.15 * f + stripe;
      float lw = 0.06; float line = (1.0 - smoothstep(lw, lw + 0.02, abs(fract(vW.x / 10.0 + 0.5) - 0.5) * 10.0)) * step(vW.x, 100.5) * step(-0.5, vW.x) * step(abs(vW.z), 6.0);
      line += (1.0 - smoothstep(lw, lw + 0.02, abs(abs(vW.z) - 6.0))) * step(-0.5, vW.x) * step(vW.x, 100.5);
      diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.95), clamp(line, 0.0, 1.0) * 0.85);`);
  };
  const ground = new THREE.Mesh(new THREE.CircleGeometry(1500, 96), grassMat); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const hillGeo = new THREE.CylinderGeometry(1400, 1400, 1, 512, 8, true);
  const hp = hillGeo.attributes.position;
  for (let i = 0; i < hp.count; i++) { const x = hp.getX(i); const z = hp.getZ(i); const y = hp.getY(i); const a = Math.atan2(z, x); const h = 55 + 95 * (0.5 + 0.5 * Math.sin(a * 3.1)) * (0.6 + 0.4 * Math.sin(a * 11.7 + 1.3)) + 12 * Math.sin(a * 23.0 + 0.7) + 5 * Math.sin(a * 61.0); hp.setY(i, (y + 0.5) * h); }
  hillGeo.computeVertexNormals();
  const hills = new THREE.Mesh(hillGeo, new THREE.MeshStandardMaterial({ color: 0x6b8fae, roughness: 1, side: THREE.BackSide, fog: false }));
  hills.material.onBeforeCompile = (sh) => { sh.fragmentShader = sh.fragmentShader.replace('#include <opaque_fragment>', 'outgoingLight = mix(outgoingLight, vec3(0.62, 0.72, 0.84), 0.55);\n#include <opaque_fragment>'); };
  scene.add(hills);
  cam.position.set(...camera);
  const controls = createOrbitControls(cam, engine.canvas, { target: new THREE.Vector3(...target), minDistance: 3, maxDistance, minPolar: 0.2, maxPolar: 1.52, damping: 0.1 });
  return { engine, scene, camera: cam, controls, renderer, quality, sun, key };
}

export function label(stage, camera) {
  const el = document.createElement('div');
  el.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;font:700 11px Poppins,system-ui,sans-serif;padding:3px 9px;border-radius:999px;background:rgba(15,23,42,0.82);color:#f8fafc;white-space:nowrap;z-index:2;will-change:transform';
  stage.appendChild(el);
  const v = new THREE.Vector3();
  return {
    el,
    at(p, dy = 0) {
      v.copy(p).project(camera);
      const vis = v.z < 1 && Math.abs(v.x) < 1.1 && Math.abs(v.y) < 1.1;
      el.style.opacity = vis ? '1' : '0';
      if (vis) el.style.transform = `translate(${((v.x + 1) / 2 * stage.clientWidth).toFixed(1)}px, ${((1 - v.y) / 2 * stage.clientHeight + dy).toFixed(1)}px) translate(-50%, -50%)`;
    },
    remove() { el.remove(); },
  };
}
