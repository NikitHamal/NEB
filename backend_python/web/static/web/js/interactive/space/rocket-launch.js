/**
 * Rocket launch in 3D — a single-stage rocket flown with Newton's laws: thrust from the exhaust
 * (mass flow = thrust ⁄ exhaust speed, 2.8 km/s), weight from gravity that weakens with height, and air
 * drag ½ρv²C_dA in an atmosphere that thins exponentially (scale height 8.5 km), integrated with RK4.
 * The camera rides alongside. The sky is computed for the rocket's altitude from the same scattering
 * model as the globe, so it darkens to black and the stars come out; the plume swells as the outside
 * pressure drops; the ground gives way to the real Earth, and a ring marks the Kármán line at 100 km.
 */
import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { NZ } from '../core/noise3d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { makeRK4 } from '../core/kit2d.js';
import { NOISE, SCATTER } from './cosmos/shaders.js';
import { createMilkySky } from './cosmos/milky.js';
import { createSkyBackground } from './cosmos/stars.js';
import { canvasCard } from './space3d/kit.js';

const VE = 2800; const DRY = 2000; const CD = 0.5; const AREA = 1.5; const RE = 6.371e6; const G0 = 9.81;
const TEX = '/static/web/js/interactive/space/cosmos/tex/';
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function rocketModel() {
  const g = new THREE.Group();
  const white = new THREE.MeshStandardMaterial({ color: 0xf1f3f5, roughness: 0.38, metalness: 0.05 });
  const black = new THREE.MeshStandardMaterial({ color: 0x15171c, roughness: 0.5 });
  const metal = new THREE.MeshStandardMaterial({ color: 0x8a8f99, roughness: 0.3, metalness: 0.9 });
  const pts = [[0, 0], [0.92, 0], [0.92, 13], [0.88, 14.4], [0.7, 16.2], [0.42, 17.6], [0.12, 18.6], [0, 18.85]].map(([r, y]) => new THREE.Vector2(r, y));
  const body = new THREE.Mesh(new THREE.LatheGeometry(pts, 48), white); g.add(body);
  for (const y of [3.0, 9.0]) { const band = new THREE.Mesh(new THREE.CylinderGeometry(0.925, 0.925, 0.7, 48, 1, true), black); band.position.y = y; g.add(band); }
  const flag = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.55), new THREE.MeshStandardMaterial({ color: 0xdc143c, roughness: 0.6 }));
  flag.position.set(0, 11.2, 0.93); g.add(flag);
  const finShape = new THREE.Shape(); finShape.moveTo(0, 0); finShape.lineTo(1.4, -0.4); finShape.lineTo(1.4, 0.5); finShape.lineTo(0, 2.6); finShape.closePath();
  const finGeo = new THREE.ExtrudeGeometry(finShape, { depth: 0.08, bevelEnabled: false }); finGeo.translate(0.88, 0.4, -0.04);
  for (let i = 0; i < 4; i++) { const f = new THREE.Mesh(finGeo, black); f.rotation.y = i * Math.PI / 2; g.add(f); }
  const bell = new THREE.Mesh(new THREE.LatheGeometry([[0.3, 0], [0.38, -0.3], [0.62, -1.2], [0.7, -1.4]].map(([r, y]) => new THREE.Vector2(r, y)), 32), metal);
  g.add(bell);
  g.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  return g;
}

function plumeMaterial() {
  return new THREE.ShaderMaterial({
    uniforms: { tNz: NZ, uTime: { value: 0 }, uK: { value: 0 }, uP: { value: 1 } },
    vertexShader: '#include <common>\n#include <logdepthbuf_pars_vertex>\nvarying vec3 vP; void main() { vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);\n#include <logdepthbuf_vertex>\n}',
    fragmentShader: `#include <common>\n#include <logdepthbuf_pars_fragment>\n${NOISE}
      uniform float uTime; uniform float uK; uniform float uP; varying vec3 vP;
      void main() {
        #include <logdepthbuf_fragment>
        float y = -vP.y / 30.0;
        float rad = length(vP.xz);
        float w = mix(0.75, 0.75 + y * mix(14.0, 2.2, uP), 1.0);
        float core = exp(-pow(rad / (w * 0.55), 2.0));
        float n = fbm3(vec3(vP.xz * 0.6, vP.y * 0.25 + uTime * 9.0));
        float diamonds = uP * pow(0.5 + 0.5 * cos(y * 30.0 * 6.2832 / 6.0), 6.0) * exp(-y * 4.0) * exp(-pow(rad / 0.35, 2.0)) * 1.6;
        float a = core * pow(max(1.0 - y, 0.0), 1.3) * (0.65 + 0.7 * n) * uK;
        vec3 c = mix(vec3(1.0, 0.95, 0.85), vec3(1.0, 0.45, 0.12), smoothstep(0.02, 0.35, y));
        c = mix(c, vec3(0.55, 0.65, 1.0), (1.0 - uP) * 0.35);
        gl_FragColor = vec4((c * a + vec3(0.75, 0.85, 1.0) * diamonds * uK) * 1.6, 1.0);
      }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  });
}

export default function init(stage) {
  stage.classList.add('ix-cosmos-stage');
  const engine = createEngine(stage, { noise: true, alpha: false, environment: false, fov: 42, near: 0.5, far: 5e7, logDepth: true, shadows: true });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  scene.background = new THREE.Color(0x000000);
  renderer.setClearColor(0x000000, 1);
  camera.position.set(38, 14, 52);
  const controls = createOrbitControls(camera, engine.canvas, { target: new THREE.Vector3(0, 10, 0), minDistance: 18, maxDistance: 400, enablePan: false, damping: 0.1 });

  const hud = createHud(stage);
  const badge = hud.badge('Set the throttle and press Ignite', '#60a5fa');
  let warp = 5; let thrustMax = 300e3; let fuel0 = 12000; let throttle = 1; let launched = false; let simT = 0; let maxH = 0; let reached = false; let landed = false;
  const y = new Float64Array(3);
  const rk = makeRK4(3, (t, s, o) => {
    const h = Math.max(0, s[0]); const v = s[1]; const m = s[2];
    const burning = m > DRY + 1e-6 && launched;
    const F = burning ? thrustMax * throttle : 0;
    const g = G0 * (RE / (RE + h)) ** 2;
    const rho = 1.225 * Math.exp(-h / 8500);
    const drag = 0.5 * rho * v * Math.abs(v) * CD * AREA;
    o[0] = v; o[1] = (F - drag) / m - g; o[2] = burning ? -F / VE : 0;
    if (s[0] <= 0 && o[1] < 0 && v <= 0) { o[0] = 0; o[1] = 0; }
  });

  const panel = createPanel(stage, { title: 'Launch control' });
  panel.slider({ label: 'Throttle', min: 0, max: 100, step: 1, value: 100, format: (v) => `${v} %`, onChange: (v) => { throttle = v / 100; } });
  panel.slider({ label: 'Maximum thrust', min: 50, max: 600, step: 10, value: thrustMax / 1000, format: (v) => `${v} kN`, onChange: (v) => { thrustMax = v * 1000; } });
  panel.slider({ label: 'Fuel load', min: 1000, max: 25000, step: 500, value: fuel0, format: (v) => `${(v / 1000).toFixed(1)} t`, onChange: (v) => { fuel0 = v; if (!launched) reset(); } });
  panel.chips({ label: 'Time warp', options: [{ value: '1', label: '1×' }, { value: '5', label: '5×' }, { value: '20', label: '20×' }], value: '5', onChange: (v) => { warp = +v; } });
  panel.buttonRow([{ label: 'Ignite', icon: 'local_fire_department', onClick: () => { launched = true; } }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset }]);
  const graph = canvasCard(panel.body, 1.6);
  const st = panel.stats([{ key: 'h', label: 'Altitude' }, { key: 'v', label: 'Speed' }, { key: 'a', label: 'Acceleration' }, { key: 'twr', label: 'Thrust ÷ weight' }, { key: 'fuel', label: 'Fuel left' }, { key: 'dv', label: 'Δv = vₑ ln(m₀/m₁)' }]);
  panel.info('The rocket pushes exhaust down; the exhaust pushes the rocket up (Newton\'s third law). It only lifts off if thrust is bigger than its weight. Reaching 100 km takes about 1.4 km/s; escaping Earth altogether would need 11.2 km/s.');

  // world: a pad and fields near the ground, the real Earth below once you climb
  const world = new THREE.Group(); scene.add(world);
  const sun = new THREE.Vector3(0.45, 0.62, 0.35).normalize();
  const key = new THREE.DirectionalLight(0xfff1df, 3.0); key.position.copy(sun).multiplyScalar(200); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024); const sc = key.shadow.camera; sc.left = -40; sc.right = 40; sc.top = 40; sc.bottom = -40; sc.near = 10; sc.far = 400; key.shadow.bias = -0.0004;
  world.add(key, key.target, new THREE.HemisphereLight(0xbcd2ff, 0x5a4a3a, 1.0));
  const groundMat = new THREE.ShaderMaterial({
    uniforms: { tNz: NZ, uSun: { value: sun }, uFade: { value: 1 } },
    vertexShader: '#include <common>\n#include <logdepthbuf_pars_vertex>\nvarying vec3 vP; varying float vD; void main() { vP = position; vec4 mv = modelViewMatrix * vec4(position, 1.0); vD = -mv.z; gl_Position = projectionMatrix * mv;\n#include <logdepthbuf_vertex>\n}',
    fragmentShader: `#include <common>\n#include <logdepthbuf_pars_fragment>\n${NOISE}
      uniform vec3 uSun; uniform float uFade; varying vec3 vP; varying float vD;
      void main() {
        #include <logdepthbuf_fragment>
        vec2 q = vP.xz;
        float fieldId = fract(sin(dot(floor(q / 160.0), vec2(12.9898, 78.233))) * 43758.5453);
        float near = 1.0 - smoothstep(0.08, 0.5, length(fwidth(q)) / 160.0);
        vec3 c = mix(vec3(0.33, 0.39, 0.16), mix(vec3(0.24, 0.36, 0.13), vec3(0.45, 0.42, 0.2), step(0.55, fieldId)), near);
        c = mix(c, vec3(0.13, 0.22, 0.09), smoothstep(0.55, 0.7, fbm3(vec3(q / 900.0, 1.0))));
        c *= 0.8 + 0.4 * mix(0.5, fbm3(vec3(q / 40.0, 3.0)), 1.0 - smoothstep(0.1, 1.0, length(fwidth(q)) / 40.0));
        float r = length(q);
        c = mix(vec3(0.55, 0.55, 0.53), c, smoothstep(34.0, 38.0, r));
        float road = smoothstep(4.0, 2.5, abs(q.x - 0.5 * q.y * 0.0 - 0.0)) * step(38.0, r) * step(q.y, 0.0);
        c = mix(c, vec3(0.32, 0.31, 0.3), road);
        vec3 col = c * (2.2 * max(uSun.y, 0.0) + vec3(0.45, 0.55, 0.75) * 0.5);
        col = mix(col, vec3(0.66, 0.74, 0.86), 1.0 - exp(-vD / 22000.0));
        col = 1.0 - exp(-col * 1.1);
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), uFade);
      }`,
    transparent: true,
  });
  const ground = new THREE.Mesh(new THREE.CircleGeometry(200000, 128), groundMat);
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; world.add(ground);
  const padMat = new THREE.MeshStandardMaterial({ color: 0x9a9a98, roughness: 0.9 });
  const pad = new THREE.Mesh(new THREE.CylinderGeometry(9, 10, 1.2, 48), padMat); pad.position.y = -0.6; pad.receiveShadow = true; world.add(pad);
  const steel = new THREE.MeshStandardMaterial({ color: 0xb4532a, roughness: 0.6, metalness: 0.4 });
  const towerG = new THREE.Group(); towerG.position.set(-4.2, 0, 0);
  for (const [x, z] of [[-0.8, -0.8], [0.8, -0.8], [-0.8, 0.8], [0.8, 0.8]]) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.16, 22, 0.16), steel); l.position.set(x, 11, z); l.castShadow = true; towerG.add(l); }
  for (let i = 1; i < 11; i++) for (const r of [0, Math.PI / 2]) { const b = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.1, 0.1), steel); b.position.y = i * 2; b.rotation.y = r; towerG.add(b); }
  world.add(towerG);

  const earthGroup = new THREE.Group(); earthGroup.position.set(0, -RE, 0); earthGroup.scale.setScalar(RE); scene.add(earthGroup);
  const loader = new THREE.TextureLoader();
  const dayTex = loader.load(TEX + (quality.tier === 'high' ? 'earth_day_4k.jpg' : 'earth_day_2k.jpg')); dayTex.colorSpace = THREE.NoColorSpace;
  const cloudTex = loader.load(TEX + 'earth_clouds_2k.jpg'); cloudTex.colorSpace = THREE.NoColorSpace;
  const earthMat = new THREE.ShaderMaterial({
    uniforms: { uDay: { value: dayTex }, uClouds: { value: cloudTex }, uSun: { value: sun }, uFade: { value: 0 } },
    vertexShader: `#include <common>\n#include <logdepthbuf_pars_vertex>\nvarying vec2 vUv; varying vec3 vP; varying vec3 vC;
      void main() { vUv = uv; vP = position; vC = (inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);\n#include <logdepthbuf_vertex>\n}`,
    fragmentShader: `#include <common>\n#include <logdepthbuf_pars_fragment>\nuniform sampler2D uDay; uniform sampler2D uClouds; uniform vec3 uSun; uniform float uFade; varying vec2 vUv; varying vec3 vP; varying vec3 vC; ${SCATTER}
      void main() {
        #include <logdepthbuf_fragment>
        vec3 n = normalize(vP);
        vec3 day = pow(texture2D(uDay, vUv).rgb, vec3(2.2));
        float cl = texture2D(uClouds, vUv).r;
        float ndl = max(dot(n, uSun), 0.0);
        vec3 col = mix(day, vec3(1.0), cl * 0.9) * ndl * 2.4;
        vec3 Ls; vec3 Ts; vec3 rd = normalize(vP - vC);
        scatter(vC, rd, length(vP - vC), uSun, 6, Ls, Ts);
        col = col * Ts + Ls * 14.0;
        col = 1.0 - exp(-col * 1.1);
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), uFade);
      }`,
    transparent: true, depthWrite: false,
  });
  // the launch site faces the camera: rotate the globe so 27.7 N, 85.3 E (Kathmandu valley) is on top
  const earth = new THREE.Mesh(new THREE.SphereGeometry(1, 128, 64), earthMat);
  earth.rotation.order = 'YXZ'; earth.rotation.y = -(85.3 + 90) * Math.PI / 180; earth.rotation.x = (90 - 27.7) * Math.PI / 180;
  earthGroup.add(earth);

  const skyMat = new THREE.ShaderMaterial({
    uniforms: { uSun: { value: sun }, uAlt: { value: 0 } },
    vertexShader: '#include <common>\n#include <logdepthbuf_pars_vertex>\nvarying vec3 vDir; void main() { vDir = normalize((modelMatrix * vec4(position, 1.0)).xyz - cameraPosition); gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);\n#include <logdepthbuf_vertex>\n}',
    fragmentShader: `#include <common>\n#include <logdepthbuf_pars_fragment>\nuniform vec3 uSun; uniform float uAlt; varying vec3 vDir; ${SCATTER}
      void main() {
        #include <logdepthbuf_fragment>
        vec3 rd = normalize(vDir); vec3 ro = vec3(0.0, 1.0 + uAlt, 0.0);
        float g = hitSphere(ro, rd, 1.0).x;
        vec3 L; vec3 T;
        scatter(ro, rd, g > 0.0 ? g : 1e9, uSun, 10, L, T);
        vec3 col = L * 16.0;
        float mu = dot(rd, uSun);
        col += T * smoothstep(0.99996, 0.99999, mu) * 60.0 + T * pow(max(mu, 0.0), 800.0) * 3.0;
        col = 1.0 - exp(-col * 1.1);
        float a = clamp(max(max(col.r, col.g), col.b) * 1.4, 0.0, 1.0);
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), a);
      }`,
    transparent: true, depthWrite: false, side: THREE.BackSide,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  });
  const sky = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 24), skyMat);
  sky.renderOrder = -2; sky.frustumCulled = false;
  const stars = new THREE.Group(); stars.add(createMilkySky(quality), createSkyBackground(quality)); stars.renderOrder = -3;
  scene.add(stars, sky);

  const karman = new THREE.Mesh(new THREE.RingGeometry(900, 1000, 128), new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.0, side: THREE.DoubleSide, depthWrite: false }));
  karman.rotation.x = -Math.PI / 2; karman.position.y = 100000; scene.add(karman);

  const rocket = rocketModel(); scene.add(rocket);
  const plume = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 9, 30, 32, 16, true), plumeMaterial());
  plume.geometry.translate(0, -15, 0); plume.position.y = -1.3; plume.renderOrder = 5; rocket.add(plume);
  const flameLight = new THREE.PointLight(0xffa04a, 0, 60, 2); flameLight.position.y = -4; rocket.add(flameLight);

  const SMOKE = quality.tier === 'low' ? 160 : 400;
  const smPos = new Float32Array(SMOKE * 3); const smAge = new Float32Array(SMOKE).fill(1e9); const smVel = new Float32Array(SMOKE * 3);
  const smGeo = new THREE.BufferGeometry(); smGeo.setAttribute('position', new THREE.BufferAttribute(smPos, 3)); smGeo.setAttribute('age', new THREE.BufferAttribute(smAge, 1));
  const smoke = new THREE.Points(smGeo, new THREE.ShaderMaterial({
    uniforms: { uSun: { value: sun }, uPx: { value: 600 } },
    vertexShader: '#include <common>\n#include <logdepthbuf_pars_vertex>\nattribute float age; uniform float uPx; varying float vA; void main() { vA = age; vec4 mv = modelViewMatrix * vec4(position, 1.0); gl_PointSize = clamp((3.0 + age * 2.2) * uPx / -mv.z, 1.0, 420.0); gl_Position = projectionMatrix * mv;\n#include <logdepthbuf_vertex>\n}',
    fragmentShader: '#include <common>\n#include <logdepthbuf_pars_fragment>\nvarying float vA; void main() {\n#include <logdepthbuf_fragment>\n vec2 d = gl_PointCoord - 0.5; float r = length(d) * 2.0; if (r > 1.0 || vA > 30.0) discard; float a = (1.0 - r * r) * 0.22 * exp(-vA / 14.0); vec3 c = mix(vec3(1.0, 0.75, 0.5), vec3(0.86, 0.85, 0.84), smoothstep(0.0, 2.5, vA)) * (0.65 + 0.4 * (0.5 - d.y)); gl_FragColor = vec4(c * a, a); }',
    transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  }));
  smoke.frustumCulled = false; smoke.renderOrder = 6; scene.add(smoke);
  let smNext = 0;
  engine.onResize((w, h) => { smoke.material.uniforms.uPx.value = h / (2 * Math.tan(camera.fov * Math.PI / 360)); });

  const trH = []; const trV = [];
  function reset() { y[0] = 0; y[1] = 0; y[2] = DRY + fuel0; launched = false; simT = 0; maxH = 0; reached = false; landed = false; trH.length = 0; trV.length = 0; smAge.fill(1e9); }
  reset();

  function drawGraph() {
    const { g, w, h } = graph.ctx();
    const t1 = Math.max(20, simT * 1.1);
    const hMax = Math.max(10, Math.ceil(maxH / 1000 / 10) * 10 + 10); const vMax = Math.max(500, Math.ceil(Math.max(...trV.map((p) => Math.abs(p[1])), 1) / 250) * 250);
    const ix = 34; const iy = 18; const iw = w - 70; const ih = h - 40;
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih);
    g.font = '600 9px Poppins, system-ui, sans-serif';
    g.fillStyle = '#60a5fa'; g.textAlign = 'left'; g.fillText(`altitude (0–${hMax} km)`, ix, 12);
    g.fillStyle = '#fbbf24'; g.textAlign = 'right'; g.fillText(`speed (0–${vMax} m/s)`, ix + iw, 12);
    g.fillStyle = '#8ea0c2'; g.textAlign = 'center'; g.fillText(`time / s (0–${fmt(t1, 0)})`, ix + iw / 2, h - 6);
    const kx = ix + iw * (100 / hMax); if (hMax > 100) { g.setLineDash([3, 4]); g.strokeStyle = 'rgba(96,165,250,0.5)'; const ky = iy + ih - 100 / hMax * ih; g.beginPath(); g.moveTo(ix, ky); g.lineTo(ix + iw, ky); g.stroke(); g.setLineDash([]); }
    const plot = (arr, max, col) => { g.strokeStyle = col; g.lineWidth = 2; g.beginPath(); arr.forEach(([t, v], i) => { const X = ix + t / t1 * iw; const Y = iy + ih - Math.max(0, v) / max * ih; if (i) g.lineTo(X, Y); else g.moveTo(X, Y); }); g.stroke(); };
    plot(trH.map(([t, v]) => [t, v / 1000]), hMax, '#60a5fa'); plot(trV, vMax, '#fbbf24');
    return kx;
  }

  const camOff = new THREE.Vector3();
  let gTick = 0;
  engine.setUpdate((dt, time) => {
    if (launched && !landed) {
      const n = 8; const hh = dt * warp / n;
      for (let i = 0; i < n; i++) { rk(y, simT, hh); simT += hh; if (y[0] < 0) { y[0] = 0; if (y[1] < 0) { if (simT > 2) landed = true; y[1] = 0; } } }
      maxH = Math.max(maxH, y[0]); if (y[0] >= 100000) reached = true;
      if ((gTick++ & 3) === 0) { trH.push([simT, y[0]]); trV.push([simT, y[1]]); if (trH.length > 600) { trH.shift(); trV.shift(); } }
    }
    const hgt = Math.max(0, y[0]); const m = y[2];
    const burning = launched && m > DRY + 1 && throttle > 0.01 && !landed;
    const g = G0 * (RE / (RE + hgt)) ** 2; const twr = (thrustMax * throttle) / (m * g);
    const P = Math.exp(-hgt / 8500);

    rocket.position.y = hgt;
    rocket.rotation.z = burning ? Math.sin(time * 37) * 0.002 : 0;
    camOff.set(0, hgt + 10, 0);
    controls.setTarget(camOff); controls.target.copy(camOff);
    controls.update(dt);
    camOff.copy(camera.position).sub(controls.target);

    plume.visible = burning;
    plume.material.uniforms.uK.value = burning ? 0.4 + 0.6 * throttle : 0;
    plume.material.uniforms.uP.value = P;
    plume.material.uniforms.uTime.value = time;
    plume.scale.set(1, 0.6 + 0.6 * throttle, 1);
    flameLight.intensity = burning ? 900 * throttle * (0.85 + 0.15 * Math.sin(time * 60)) : 0;

    if (burning && hgt < 400) {
      const k = Math.ceil(dt * 90 * throttle);
      for (let s = 0; s < k; s++) {
        const i = smNext++ % SMOKE; const a = Math.random() * Math.PI * 2; const sp = 6 + Math.random() * 10;
        smPos[i * 3] = Math.cos(a) * 1.5; smPos[i * 3 + 1] = Math.max(0.5, hgt - 3); smPos[i * 3 + 2] = Math.sin(a) * 1.5;
        smVel[i * 3] = Math.cos(a) * sp * (hgt < 15 ? 1 : 0.25); smVel[i * 3 + 1] = hgt < 15 ? 0.6 : -2; smVel[i * 3 + 2] = Math.sin(a) * sp * (hgt < 15 ? 1 : 0.25);
        smAge[i] = 0;
      }
    }
    for (let i = 0; i < SMOKE; i++) {
      if (smAge[i] > 40) continue;
      smAge[i] += dt;
      const damp = Math.exp(-dt * 0.9);
      smVel[i * 3] *= damp; smVel[i * 3 + 2] *= damp; smVel[i * 3 + 1] = smVel[i * 3 + 1] * damp + dt * 0.35;
      smPos[i * 3] += smVel[i * 3] * dt; smPos[i * 3 + 1] = Math.max(0.5, smPos[i * 3 + 1] + smVel[i * 3 + 1] * dt); smPos[i * 3 + 2] += smVel[i * 3 + 2] * dt;
    }
    smGeo.attributes.position.needsUpdate = true; smGeo.attributes.age.needsUpdate = true;

    const altR = (hgt + camOff.y) / RE;
    skyMat.uniforms.uAlt.value = Math.max(altR, 1e-6);
    sky.position.copy(camera.position); sky.scale.setScalar(4e5);
    const space = Math.min(1, Math.max(0, (hgt - 12000) / 40000));
    stars.visible = space > 0.01;
    stars.traverse((o) => { if (o.material && o.material.uniforms && o.material.uniforms.uOpacity) o.material.uniforms.uOpacity.value = space; });
    const gf = 1 - Math.min(1, Math.max(0, (hgt - 4000) / 9000));
    groundMat.uniforms.uFade.value = gf; ground.visible = gf > 0.01; pad.visible = towerG.visible = hgt < 15000;
    earthMat.uniforms.uFade.value = 1 - gf * 0.999; earth.visible = hgt > 2500;
    karman.material.opacity = 0.55 * Math.min(1, Math.max(0, 1 - Math.abs(hgt - 100000) / 40000));
    karman.visible = karman.material.opacity > 0.01;

    if ((gTick & 7) === 0) drawGraph();
    const rho = 1.225 * P; const acc = burning ? (thrustMax * throttle - 0.5 * rho * y[1] * Math.abs(y[1]) * CD * AREA) / m - g : -g;
    st.h.set(hgt >= 1000 ? `${fmt(hgt / 1000, 2)} km` : `${fmt(hgt, 0)} m`); st.v.set(`${fmt(y[1], 0)} m/s`);
    st.a.set(`${fmt(launched && !landed ? acc / G0 : 0, 2)} g`); st.twr.set(fmt(twr, 2));
    st.fuel.set(`${fmt((m - DRY) / 1000, 2)} t`); st.dv.set(`${fmt(VE * Math.log((DRY + fuel0) / DRY), 0)} m/s total`);
    badge.set(!launched ? (thrustMax / ((DRY + fuel0) * G0) <= 1 ? 'Thrust is less than weight: it will not lift off!' : 'Set the throttle and press Ignite') : landed ? `Back on the ground. Highest point: ${fmt(maxH / 1000, 1)} km${reached ? ': you reached space!' : ''}` : reached ? `In space! ${fmt(hgt / 1000, 1)} km up` : burning ? (y[0] < 1 && twr <= 1 ? 'Thrust ≤ weight: still on the pad' : `Climbing: ${fmt(hgt / 1000, 1)} km, lighter every second`) : y[1] > 0 ? 'Engine off: coasting up, gravity slowing it' : 'Falling back');
  });
  engine.start();

  stage.__rocket = { ignite: () => { launched = true; }, jump: (h, v) => { launched = true; y[0] = h; y[1] = v; }, state: () => Array.from(y) };
  return { dispose() { controls.dispose(); panel.dispose(); hud.dispose(); [dayTex, cloudTex].forEach((t) => t.dispose()); engine.dispose(); } };
}
