import { THREE } from '../../core/engine.js';
import { NZ } from '../../core/noise3d.js';
import { NOISE } from '../cosmos/shaders.js';
import { BLACKBODY } from './star.js';

const billboardVS = `varying vec2 vQ;
  void main() { vQ = position.xy; vec4 c = modelViewMatrix * vec4(0.0, 0.0, 0.0, 1.0);
    float sc = length(modelMatrix[0].xyz); gl_Position = projectionMatrix * (c + vec4(position.xy * sc, 0.0, 0.0)); }`;

export function glow(color, size, k = 1) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.ShaderMaterial({
    uniforms: { uC: { value: new THREE.Color(color) }, uK: { value: k } },
    vertexShader: billboardVS,
    fragmentShader: `uniform vec3 uC; uniform float uK; varying vec2 vQ;
      void main() { float r = length(vQ) * 2.0 / ${size.toFixed(2)}; float a = exp(-r * 7.0) * 1.4 + exp(-r * r * 90.0) * 2.0 + pow(max(1.0 - r, 0.0), 3.0) * 0.12; gl_FragColor = vec4(uC * a * uK, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  m.frustumCulled = false;
  m.renderOrder = 7;
  return m;
}

// A pulsar: the neutron star, its dipole field and two radio beams along the magnetic axis, which is
// tilted from the spin axis, so the beams sweep round like a lighthouse.
export function createPulsar() {
  const group = new THREE.Group();
  const mag = new THREE.Group();
  mag.rotation.z = 0.5;
  group.add(mag);
  const core = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 16), new THREE.MeshBasicMaterial({ color: 0xdfeaff }));
  group.add(core, glow(0xa9c4ff, 14, 0.9));
  const beamMat = new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 } },
    vertexShader: 'varying vec3 vP; void main() { vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform float uTime; varying vec3 vP;
      void main() { float along = clamp(abs(vP.y) / 22.0, 0.0, 1.0); float rad = length(vP.xz) / (0.2 + abs(vP.y) * 0.16);
        float a = pow(1.0 - along, 1.6) * exp(-rad * rad * 2.2) * (0.85 + 0.15 * sin(abs(vP.y) * 2.0 - uTime * 30.0));
        gl_FragColor = vec4(vec3(0.55, 0.72, 1.0) * a * 0.9, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  });
  const beamGeo = new THREE.CylinderGeometry(3.7, 0.2, 22, 32, 8, true);
  beamGeo.translate(0, 11, 0);
  const b1 = new THREE.Mesh(beamGeo, beamMat); const b2 = new THREE.Mesh(beamGeo, beamMat);
  b2.rotation.z = Math.PI;
  b1.renderOrder = b2.renderOrder = 8;
  mag.add(b1, b2);
  const pts = [];
  for (const L of [2.2, 3.4, 5, 7]) {
    for (let a = 0; a < 8; a++) {
      const phi = a / 8 * Math.PI * 2;
      let prev = null;
      for (let i = 1; i < 40; i++) {
        const th = 0.05 + (Math.PI - 0.1) * i / 40;
        const r = L * Math.sin(th) * Math.sin(th);
        if (r < 1) { prev = null; continue; }
        const p = new THREE.Vector3(r * Math.sin(th) * Math.cos(phi), r * Math.cos(th), r * Math.sin(th) * Math.sin(phi));
        if (prev) pts.push(prev, p);
        prev = p;
      }
    }
  }
  const field = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0x6f8fd8, transparent: true, opacity: 0.32, depthWrite: false, blending: THREE.AdditiveBlending }));
  mag.add(field);
  return {
    group,
    update(dt, t) { group.rotation.y += dt * 5.5; beamMat.uniforms.uTime.value = t; },
    dispose() { group.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); },
  };
}

// A black hole of Schwarzschild radius 1. Each pixel's ray is bent towards the hole by 2 r_s / b,
// strengthened near the photon sphere (b = 2.6) and faded to zero at the lens edge so the lensed sky
// meets the real one without a seam. The thin disc (from the innermost stable orbit, 3 r_s) is looked
// up on both the incoming and the bent part of the ray, which is why its far side shows above and below
// the shadow; Doppler beaming brightens and blues the approaching side.
export function createBlackHole(renderer, skyGroup, quality) {
  const group = new THREE.Group();
  const cubeRT = new THREE.WebGLCubeRenderTarget(quality.tier === 'low' ? 128 : 256);
  const cubeCam = new THREE.CubeCamera(0.1, 1e6, cubeRT);
  let captured = false;
  const RL = 16;
  const U = {
    tNz: NZ, uEnv: { value: cubeRT.texture }, uTime: { value: 0 }, uN: { value: new THREE.Vector3(0.08, 1, 0.22).normalize() }, uRL: { value: RL },
  };
  const mat = new THREE.ShaderMaterial({
    uniforms: U,
    vertexShader: `varying vec3 vP; varying vec3 vC;
      void main() { vP = position; vC = (inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `${NOISE}${BLACKBODY}
      uniform samplerCube uEnv; uniform float uTime; uniform vec3 uN; uniform float uRL;
      varying vec3 vP; varying vec3 vC;
      vec4 disk(vec3 o, vec3 d, float tmax, vec3 view) {
        float dn = dot(d, uN);
        if (abs(dn) < 1e-4) return vec4(0.0);
        float t = -dot(o, uN) / dn;
        if (t < 0.0 || t > tmax) return vec4(0.0);
        vec3 p = o + d * t;
        float r = length(p);
        if (r < 3.0 || r > 10.0) return vec4(0.0);
        vec3 tang = normalize(cross(uN, p));
        float beta = clamp(sqrt(0.5 / r), 0.0, 0.7);
        float g = 1.0 / (inversesqrt(1.0 - beta * beta) * (1.0 - beta * dot(tang, -view)));
        float temp = pow(r / 3.0, -0.75) * pow(max(1.0 - sqrt(3.0 / r), 0.0), 0.25);
        float ang = atan(dot(p, cross(uN, vec3(1.0, 0.0, 0.0))), dot(p, vec3(1.0, 0.0, 0.0)));
        float turb = fbm3(vec3(r * 1.3, ang * 3.0 - uTime * 2.2 / pow(r, 1.5), 0.0)) * 0.7 + fbm3(vec3(r * 5.0, ang * 9.0 - uTime * 3.0 / pow(r, 1.5), 3.0)) * 0.5;
        float I = temp * 2.4 * pow(g, 3.0) * (0.35 + turb) * smoothstep(10.0, 6.5, r) * smoothstep(3.0, 3.3, r);
        vec3 c = blackbody(2200.0 + 9500.0 * temp * g) * I;
        return vec4(c, clamp(I * 1.2, 0.0, 0.95));
      }
      void main() {
        vec3 ro = vC; vec3 rd = normalize(vP - vC);
        float tc = -dot(ro, rd);
        vec3 pc = ro + rd * tc;
        float b = length(pc);
        if (tc < 0.0) { b = length(ro); pc = ro; tc = 0.0; }
        float fade = smoothstep(uRL, uRL * 0.55, b);
        float alpha = 2.0 / max(b, 1e-3) * (1.0 + 1.6 * exp(-(b - 2.6) * 1.4)) * fade;
        vec3 inward = -normalize(pc + 1e-5);
        vec3 rd2 = normalize(rd * cos(min(alpha, 3.0)) + inward * sin(min(alpha, 3.0)));
        vec3 view = -rd;
        vec4 d1 = disk(ro, rd, tc, view);
        bool captured = b < 2.6;
        vec4 d2 = captured ? vec4(0.0) : disk(pc, rd2, 1e4, view);
        vec3 sky = captured ? vec3(0.0) : textureCube(uEnv, rd2).rgb;
        sky = pow(sky, vec3(2.2));
        vec3 col = mix(sky + d2.rgb, d1.rgb, d1.a);
        col += vec3(1.0, 0.75, 0.45) * exp(-pow((b - 2.62) / 0.05, 2.0)) * 0.9;
        col = 1.0 - exp(-col * 1.2);
        float a = max(smoothstep(uRL, uRL * 0.8, b), d1.a);
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)) * a, a);
      }`,
    transparent: true, depthWrite: false, side: THREE.BackSide,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  });
  const lens = new THREE.Mesh(new THREE.SphereGeometry(RL, 64, 32), mat);
  lens.renderOrder = 9;
  group.add(lens);
  return {
    group,
    capture(scene) {
      if (captured) return;
      captured = true;
      const vis = [];
      scene.children.forEach((o) => { vis.push(o.visible); o.visible = o === skyGroup; });
      cubeCam.position.set(0, 0, 0);
      cubeCam.update(renderer, scene);
      scene.children.forEach((o, i) => { o.visible = vis[i]; });
    },
    update(dt, t) { U.uTime.value = t; },
    dispose() { cubeRT.dispose(); lens.geometry.dispose(); mat.dispose(); },
  };
}
