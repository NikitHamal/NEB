import { THREE } from '../../core/engine.js';
import { NZ } from '../../core/noise3d.js';
import { NOISE, shader, pointsMaterial, makePoints, lineLoop, glowSprite } from './shaders.js';
import { AU, R_SUN, PLANETS, planetPosition, orbitPoint, radec, rng, gauss } from './astro.js';

export function markerMaterial() {
  return shader({
    vertexHead: 'attribute vec3 color; attribute float size; varying vec3 vC;',
    vertex: 'vC = color; gl_PointSize = size; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
    fragmentHead: 'varying vec3 vC;',
    fragment: `vec2 d = gl_PointCoord - 0.5; float r = length(d) * 2.0;
      float a = smoothstep(1.0, 0.55, r) * 0.9 + exp(-r * r * 8.0) * 0.6;
      if (a < 0.01) discard;
      gl_FragColor = vec4(vC * a * uOpacity, 1.0);`,
    blending: THREE.AdditiveBlending,
  });
}

// The photosphere at 5 772 K: granulation cells ~1 000 km across that boil, supergranulation and
// faculae, sunspots with umbra and penumbra in the activity belts, and limb darkening per colour
// (I/I0 = 1 - u(1 - mu), u larger in blue) so the edge goes orange; a thin chromosphere at the rim.
function sunMaterial() {
  return shader({
    transparent: false, depthWrite: true,
    uniforms: { uTime: { value: 0 } },
    vertexHead: 'varying vec3 vN; varying vec3 vV; varying vec3 vP;',
    vertex: `vP = position; vN = normalize(position); vV = normalize((inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz - position);
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);`,
    fragmentHead: `uniform float uTime; varying vec3 vN; varying vec3 vV; varying vec3 vP; ${NOISE}`,
    fragment: `
      vec3 n = normalize(vN);
      float mu = clamp(dot(n, normalize(vV)), 0.0, 1.0);
      float t = uTime;
      vec4 g1 = nz4(n * 96.0 + vec3(0.0, t * 0.05, 0.0));
      vec4 g2 = nz4(n * 190.0 - vec3(t * 0.07, 0.0, 0.0));
      float lanes = smoothstep(0.0, 0.16, g1.b) * 0.6 + smoothstep(0.0, 0.16, g2.b) * 0.4;
      float sup = fbm3(n * 20.0 + vec3(t * 0.01));
      float gran = mix(0.8, 1.04, lanes) * (0.93 + 0.1 * sup);
      float act = smoothstep(0.62, 0.2, abs(n.y)) * smoothstep(0.08, 0.2, abs(n.y));
      float sf = fbm3(n * 5.5 + 13.0);
      float spot = smoothstep(0.72, 0.8, sf) * act;
      float umbra = smoothstep(0.79, 0.84, sf) * act;
      float fil = 0.75 + 0.25 * sin(atan(n.z, n.x) * 260.0 + sf * 80.0);
      float fac = smoothstep(0.55, 0.7, sup) * pow(1.0 - mu, 1.5);
      vec3 u = vec3(0.47, 0.62, 0.82);
      vec3 limb = 1.0 - u * (1.0 - mu);
      vec3 col = vec3(1.0, 0.8, 0.56) * 1.55 * gran * limb;
      col *= mix(1.0, 0.45 * fil, spot);
      col *= 1.0 - umbra * 0.85;
      col += vec3(1.0, 0.85, 0.6) * fac * 1.4;
      col += vec3(1.0, 0.25, 0.3) * smoothstep(0.12, 0.0, mu) * 0.8;
      col = 1.0 - exp(-col * 1.15);
      gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);`,
  });
}

// The corona, prominences and glare: a camera-facing disc in solar radii. Streamers follow a noise
// in position angle and fall off as r^-2.5; red prominence loops rise just above the limb.
function coronaMaterial() {
  return shader({
    uniforms: { uTime: { value: 0 } },
    vertexHead: 'varying vec2 vQ;',
    vertex: `vQ = position.xy;
      vec4 c = modelViewMatrix * vec4(0.0, 0.0, 0.0, 1.0);
      float sc = length(modelMatrix[0].xyz);
      gl_Position = projectionMatrix * (c + vec4(position.xy * sc, 0.0, 0.0));`,
    fragmentHead: `uniform float uTime; varying vec2 vQ; ${NOISE}`,
    fragment: `
      float r = length(vQ);
      if (r < 0.985) discard;
      float th = atan(vQ.y, vQ.x);
      vec3 dir = vec3(cos(th), sin(th), 0.0);
      float st = fbm3(dir * 2.2 + vec3(0.0, 0.0, uTime * 0.003)) ;
      float st2 = fbm3(dir * 7.0 + vec3(3.0, 1.0, uTime * 0.006));
      float ray = pow(clamp(st * 0.7 + st2 * 0.5, 0.0, 1.2), 2.4);
      float k = pow(r, -2.6);
      vec3 col = vec3(1.0, 0.94, 0.86) * k * (0.25 + 1.6 * ray) * smoothstep(0.985, 1.02, r) * 0.9;
      col += vec3(1.0, 0.78, 0.5) * exp(-(r - 1.0) * 5.0) * 0.55 * smoothstep(0.985, 1.0, r);
      float pr = fbm3(vec3(dir.xy * 9.0, (r - 1.0) * 16.0) + vec3(0.0, 0.0, uTime * 0.02));
      float band = smoothstep(1.14, 1.0, r) * smoothstep(0.985, 1.005, r);
      col += vec3(1.0, 0.22, 0.28) * smoothstep(0.62, 0.78, pr) * band * 1.6;
      col *= smoothstep(6.0, 3.5, r);
      gl_FragColor = vec4(col * uOpacity, 1.0);`,
    blending: THREE.AdditiveBlending,
  });
}

const GIANTS = {
  jupiter: { a: [0.93, 0.87, 0.76], b: [0.62, 0.42, 0.28], c: [0.82, 0.68, 0.52], n: 10, warp: 1.3, spot: 1 },
  saturn: { a: [0.93, 0.86, 0.68], b: [0.78, 0.66, 0.46], c: [0.86, 0.77, 0.58], n: 11, warp: 0.35, spot: 0 },
  uranus: { a: [0.68, 0.87, 0.90], b: [0.60, 0.80, 0.86], c: [0.64, 0.84, 0.88], n: 5, warp: 0.1, spot: 0 },
  neptune: { a: [0.30, 0.48, 0.92], b: [0.22, 0.36, 0.80], c: [0.36, 0.55, 0.95], n: 6, warp: 0.25, spot: 0 },
};
const v3 = (c) => `vec3(${c.map((x) => x.toFixed(3)).join(',')})`;

export function litPlanet(p) {
  const gi = GIANTS[p.id];
  const mat = new THREE.MeshStandardMaterial({ color: gi ? 0xffffff : p.color, roughness: 0.9, metalness: 0 });
  mat.onBeforeCompile = (sh) => {
    sh.uniforms.tNz = NZ;
    sh.vertexShader = 'varying vec3 vObj;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\nvObj = position;');
    sh.fragmentShader = `varying vec3 vObj;\n${NOISE}\n` + sh.fragmentShader.replace('#include <color_fragment>', gi ? `#include <color_fragment>
      vec3 on = normalize(vObj);
      float lat = on.y;
      vec3 q = on * 4.0;
      float w = fbm3(q + vec3(0.0, 0.0, 0.0)) * ${gi.warp.toFixed(2)};
      float turb = fbm3(vec3(on.x * 9.0, lat * 30.0, on.z * 9.0) + w * 3.0);
      float y = lat * ${gi.n.toFixed(1)} + w * 0.9 + turb * 0.35;
      float band = mix(sin(y * 3.14159) * 0.5 + 0.5, vnoise(vec3(y * 1.7, 3.0, 1.0)), 0.55);
      float fine2 = sin(lat * 140.0 + turb * 6.0) * 0.5 + 0.5;
      vec3 col = mix(${v3(gi.b)}, ${v3(gi.a)}, smoothstep(0.25, 0.75, band));
      col = mix(col, ${v3(gi.c)}, fine2 * 0.25);
      col *= 0.82 + turb * 0.36;
      float oval = step(0.86, vnoise(vec3(atan(on.z, on.x) * 6.0, lat * 26.0, 1.0))) * smoothstep(0.2, 0.5, abs(lat));
      col = mix(col, vec3(0.97, 0.95, 0.9), oval * 0.5);
      ${gi.spot ? `vec2 sp = vec2(atan(on.z, on.x) - 1.2, (lat + 0.37) * 3.2);
      float spot = exp(-dot(sp * vec2(3.2, 2.6), sp * vec2(3.2, 2.6)));
      col = mix(col, vec3(0.75, 0.36, 0.22), smoothstep(0.25, 0.7, spot + turb * 0.15) * 0.85);` : ''}
      col = mix(col, col * 0.75, smoothstep(0.82, 0.98, abs(lat)));
      diffuseColor.rgb = col;` : `#include <color_fragment>
      vec3 on = normalize(vObj);
      float tt = fbm3(on * 5.0 + ${(p.r * 1e-7).toFixed(3)});
      float cr = fbm3(on * 22.0);
      diffuseColor.rgb *= 0.72 + 0.45 * tt + 0.15 * cr;`);
  };
  mat.customProgramCacheKey = () => `planet-${p.id}`;
  return mat;
}

export function ringMesh(inner, outer) {
  const geo = new THREE.RingGeometry(inner, outer, 128, 1);
  const pos = geo.attributes.position; const uv = geo.attributes.uv;
  for (let i = 0; i < pos.count; i++) uv.setXY(i, (Math.hypot(pos.getX(i), pos.getY(i)) - inner) / (outer - inner), 0.5);
  const c = document.createElement('canvas'); c.width = 512; c.height = 4;
  const g = c.getContext('2d');
  const r = rng(7);
  for (let x = 0; x < 512; x++) {
    const t = x / 512;
    let a = 0.55 + 0.35 * Math.sin(t * 90 + r() * 2) * r();
    if (t > 0.62 && t < 0.68) a *= 0.08;
    if (t < 0.12) a *= 0.25;
    if (t > 0.9 && t < 0.92) a *= 0.3;
    const L = 215 + 40 * r();
    g.fillStyle = `rgba(${Math.min(255, L)},${L * 0.92},${L * 0.8},${Math.min(1, a * 1.25)})`;
    g.fillRect(x, 0, 1, 4);
  }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const mat = new THREE.MeshStandardMaterial({ map: tex, transparent: true, side: THREE.DoubleSide, roughness: 1, depthWrite: false, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 0.18 });
  const m = new THREE.Mesh(geo, mat);
  m.rotation.x = -Math.PI / 2 + 0.47;
  return m;
}

function belt(count, seed, aMin, aMax, inc, color) {
  const r = rng(seed);
  const pos = new Float32Array(count * 3); const col = new Float32Array(count * 3); const size = new Float32Array(count);
  const c = new THREE.Color(color);
  for (let i = 0; i < count; i++) {
    const a = aMin + (aMax - aMin) * Math.pow(r(), 0.8);
    const th = r() * Math.PI * 2;
    const y = gauss(r) * inc * a;
    pos[i * 3] = Math.cos(th) * a; pos[i * 3 + 1] = y; pos[i * 3 + 2] = Math.sin(th) * a;
    const k = 0.5 + r() * 0.5;
    col[i * 3] = c.r * k; col[i * 3 + 1] = c.g * k; col[i * 3 + 2] = c.b * k;
    size[i] = 0.004 * a * (0.5 + r());
  }
  return makePoints(pos, col, size, pointsMaterial({ min: 1.2, max: 3, gain: 0.55, core: 0 }));
}

function oort(count) {
  const r = rng(99);
  const pos = new Float32Array(count * 3); const col = new Float32Array(count * 3); const size = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    const inner = i < count * 0.35;
    const d = inner ? 2000 + 18000 * Math.pow(r(), 0.7) : Math.exp(Math.log(20000) + r() * Math.log(100000 / 20000));
    const u = r() * 2 - 1; const th = r() * Math.PI * 2; const s = Math.sqrt(1 - u * u);
    const flat = inner ? 0.35 : 1;
    pos[i * 3] = s * Math.cos(th) * d; pos[i * 3 + 1] = u * d * flat; pos[i * 3 + 2] = s * Math.sin(th) * d;
    const k = 0.35 + r() * 0.4;
    col[i * 3] = 0.7 * k; col[i * 3 + 1] = 0.8 * k; col[i * 3 + 2] = 1.0 * k;
    size[i] = d * 0.012;
  }
  return makePoints(pos, col, size, pointsMaterial({ min: 1.1, max: 3, gain: 0.7, core: 0 }));
}

function heliosphere() {
  const geo = new THREE.SphereGeometry(1, 64, 32);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i);
    const tail = x < 0 ? 1 + 1.6 * Math.pow(-x, 2) : 1;
    p.setXYZ(i, x * 120 * tail, p.getY(i) * 120, p.getZ(i) * 120);
  }
  const mat = shader({
    uniforms: { uColor: { value: new THREE.Color(0x6fa8ff) } },
    vertexHead: 'varying vec3 vN; varying vec3 vV;',
    vertex: `vec4 wp = modelMatrix * vec4(position, 1.0); vN = normalize(mat3(modelMatrix) * normal); vV = normalize(cameraPosition - wp.xyz);
      gl_Position = projectionMatrix * viewMatrix * wp;`,
    fragmentHead: 'uniform vec3 uColor; varying vec3 vN; varying vec3 vV;',
    fragment: 'float f = pow(1.0 - abs(dot(normalize(vN), normalize(vV))), 3.0); gl_FragColor = vec4(uColor * f * 0.35 * uOpacity, 1.0);',
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
  });
  geo.computeVertexNormals();
  return new THREE.Mesh(geo, mat);
}

export function createSolarSystem(quality, days) {
  const group = new THREE.Group();
  const low = quality.tier === 'low';
  const sun = new THREE.Mesh(new THREE.SphereGeometry(R_SUN / AU, 64, 32), sunMaterial());
  group.add(sun);
  const corona = new THREE.Mesh(new THREE.PlaneGeometry(12, 12), coronaMaterial());
  corona.scale.setScalar(R_SUN / AU);
  corona.frustumCulled = false;
  corona.renderOrder = 3;
  const corona2 = glowSprite(0xffc27a, R_SUN / AU * 16, 0.22);
  group.add(corona, corona2);
  const sunLight = new THREE.PointLight(0xfff4e6, 1.15, 0, 0);
  group.add(sunLight);

  const bodies = [];
  const markerPos = new Float32Array((PLANETS.length + 2) * 3);
  const markerCol = new Float32Array((PLANETS.length + 2) * 3);
  const markerSize = new Float32Array(PLANETS.length + 2);
  markerCol.set([1.0, 0.85, 0.55], 0); markerSize[0] = 9;
  const orbits = new THREE.Group();
  group.add(orbits);
  PLANETS.forEach((p, i) => {
    const pos = planetPosition(p, days).divideScalar(AU);
    const pts = [];
    for (let k = 0; k < 360; k++) pts.push(orbitPoint(p, k).divideScalar(AU));
    orbits.add(lineLoop(pts, p.id === 'earth' ? 0x7fb6ff : 0x8c9ab8, p.id === 'earth' ? 0.55 : 0.32));
    if (p.id !== 'earth') {
      const m = new THREE.Mesh(new THREE.SphereGeometry(p.r / AU, 48, 24), litPlanet(p));
      m.position.copy(pos);
      if (p.id === 'saturn') m.add(ringMesh(1.24 * p.r / AU, 2.27 * p.r / AU));
      group.add(m);
    }
    bodies.push({ ...p, pos });
    markerPos.set([pos.x, pos.y, pos.z], (i + 1) * 3);
    const c = new THREE.Color(p.color);
    markerCol.set([c.r, c.g, c.b], (i + 1) * 3);
    markerSize[i + 1] = p.id === 'earth' ? 6 : 5;
  });
  const voyager = radec(17.2, 12.0, 170);
  markerPos.set([voyager.x, voyager.y, voyager.z], (PLANETS.length + 1) * 3);
  markerCol.set([0.6, 1.0, 0.7], (PLANETS.length + 1) * 3); markerSize[PLANETS.length + 1] = 4;
  const markers = makePoints(markerPos, markerCol, markerSize, markerMaterial());
  group.add(markers);

  const asteroids = belt(low ? 1500 : 4000, 3, 2.15, 3.3, 0.08, 0xb8a58a);
  const kuiper = belt(low ? 1500 : 4000, 5, 30, 50, 0.12, 0x9fb2d0);
  group.add(asteroids, kuiper);
  const helio = heliosphere();
  const flow = radec(17.4, -17, 1).normalize();
  helio.quaternion.setFromUnitVectors(new THREE.Vector3(1, 0, 0), flow);
  group.add(helio);
  const cloud = oort(low ? 5000 : 14000);
  group.add(cloud);

  return {
    group,
    bodies,
    update(t, logW) {
      sun.material.uniforms.uTime.value = t;
      corona.material.uniforms.uTime.value = t;
      sun.visible = logW < 13.5;
      corona.visible = corona2.visible = logW < 12.8;
      markers.visible = logW > 9.3 && logW < 15.6;
      orbits.visible = logW > 10.2 && logW < 15.2;
      asteroids.visible = logW > 10.6 && logW < 13.6;
      kuiper.visible = logW > 12 && logW < 15;
      helio.visible = logW > 12.8 && logW < 15.6;
      cloud.visible = logW > 14.2 && logW < 17.6;
      const oortA = Math.min(1, Math.max(0, (logW - 14.2) / 0.8)) * Math.min(1, Math.max(0, (17.6 - logW) / 0.8));
      cloud.material.uniforms.uOpacity.value *= oortA;
    },
    setPx(uPx, scale) {
      [asteroids, kuiper, cloud].forEach((o) => { o.material.uniforms.uPx.value = uPx; o.material.uniforms.uScale.value = scale; });
    },
    labels: [
      { text: 'The Sun', sub: '1.39 million km across', get: (v) => v.set(0, 0, 0), min: 9.2, max: 15.6 },
      ...PLANETS.map((p, i) => ({ text: p.name, sub: p.id === 'earth' ? 'you are here' : '', get: (v) => v.copy(bodies[i].pos), min: p.el[0] < 2 ? 10.6 : p.el[0] < 10 ? 11.6 : 12.4, max: p.el[0] < 2 ? 13.0 : 14.6, cls: p.id === 'earth' ? 'here' : '' })),
      { text: 'Asteroid belt', sub: '', get: (v) => v.set(2.7, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), 2.2), min: 11.4, max: 12.9 },
      { text: 'Kuiper belt', sub: '30–50 AU', get: (v) => v.set(42, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), -0.6), min: 13.1, max: 14.6 },
      { text: 'Voyager 1', sub: 'farthest spacecraft, ~170 AU', get: (v) => v.copy(voyager), min: 13.4, max: 15.2 },
      { text: 'Heliopause', sub: 'edge of the Sun’s wind', get: (v) => v.set(0, 120, 0), min: 13.6, max: 15.2 },
      { text: 'Oort cloud', sub: 'a trillion icy comets', get: (v) => v.set(0, 52000, 0), min: 15.2, max: 17.3 },
    ],
  };
}
