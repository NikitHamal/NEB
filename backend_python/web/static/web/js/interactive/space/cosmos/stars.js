import { THREE } from '../../core/engine.js';
import { shader, pointsMaterial, makePoints, lineLoop } from './shaders.js';
import { NEAR_STARS, radec, spectralColor, rng, gauss, galToGlobal } from './astro.js';
import { markerMaterial } from './solar.js';

function skyStarsMaterial() {
  return shader({
    vertexHead: 'attribute vec3 color; attribute float size; varying vec3 vC;',
    vertex: `vC = color; gl_PointSize = size;
      vec4 p = projectionMatrix * viewMatrix * vec4(cameraPosition + mat3(modelMatrix) * position, 1.0);
      gl_Position = p;`,
    fragmentHead: 'varying vec3 vC;',
    fragment: `vec2 d = gl_PointCoord - 0.5; float r2 = dot(d, d) * 4.0;
      float a = exp(-r2 * 4.0);
      if (a < 0.01) discard;
      gl_FragColor = vec4(vC * a * uOpacity, 1.0);`,
    blending: THREE.AdditiveBlending,
  });
}

export function createSkyBackground(quality) {
  const n = quality.tier === 'low' ? 5000 : 14000;
  const r = rng(2024);
  const pos = new Float32Array(n * 3); const col = new Float32Array(n * 3); const size = new Float32Array(n);
  const v = new THREE.Vector3();
  const R = 5e4;
  for (let i = 0; i < n; i++) {
    const band = i < n * 0.55;
    const l = r() * Math.PI * 2;
    let b;
    if (band) b = gauss(r) * 0.12 * (1 + 0.8 * Math.cos(l));
    else b = Math.asin(r() * 2 - 1);
    galToGlobal(Math.cos(b) * Math.cos(l), Math.cos(b) * Math.sin(l), Math.sin(b), v).multiplyScalar(R);
    pos[i * 3] = v.x; pos[i * 3 + 1] = v.y; pos[i * 3 + 2] = v.z;
    const m = Math.pow(r(), 6);
    const t = r();
    const c = new THREE.Color(t < 0.15 ? 0xaabfff : t < 0.55 ? 0xfff4e8 : t < 0.85 ? 0xffe0b8 : 0xffc58a);
    const k = band ? 0.18 + m * 1.2 : 0.3 + m * 1.6;
    col[i * 3] = c.r * k; col[i * 3 + 1] = c.g * k; col[i * 3 + 2] = c.b * k;
    size[i] = (band ? 1.3 : 1.6) + m * 3.2;
  }
  const pts = makePoints(pos, col, size, skyStarsMaterial());
  pts.renderOrder = -5;
  return pts;
}

export function createStarNeighbourhood(quality) {
  const group = new THREE.Group();
  const n = NEAR_STARS.length;
  const pos = new Float32Array(n * 3); const col = new Float32Array(n * 3); const size = new Float32Array(n);
  const labels = [];
  const drops = [];
  const v = new THREE.Vector3();
  NEAR_STARS.forEach(([name, ra, dec, dist, cls, rad], i) => {
    radec(ra, dec, dist, v);
    pos[i * 3] = v.x; pos[i * 3 + 1] = v.y; pos[i * 3 + 2] = v.z;
    const c = new THREE.Color(spectralColor(cls));
    const lum = Math.min(1.6, 0.55 + Math.log10(1 + rad) * 0.6);
    col[i * 3] = c.r * lum; col[i * 3 + 1] = c.g * lum; col[i * 3 + 2] = c.b * lum;
    size[i] = Math.min(16, 5 + Math.log10(1 + rad * 3) * 5);
    const p = v.clone();
    const near = dist < 14;
    labels.push({
      text: name,
      sub: `${dist < 100 ? dist.toFixed(dist < 20 ? 2 : 0) : Math.round(dist).toLocaleString()} light-years`,
      get: (o) => o.copy(p),
      min: near ? 16.3 : dist < 50 ? 17.0 : 18.0,
      max: near ? 17.8 : dist < 50 ? 18.6 : 19.8,
      minor: !['Proxima Centauri', 'Alpha Centauri A & B', 'Sirius A & B', "Barnard's Star", 'Vega', 'Betelgeuse', 'Polaris', 'Rigel', 'Pleiades', 'Arcturus', 'Deneb', 'Orion Nebula', 'Tau Ceti', 'Epsilon Eridani', 'Altair', 'Aldebaran'].includes(name),
    });
    if (dist < 20) drops.push(new THREE.Vector3(p.x, p.y, p.z), new THREE.Vector3(p.x, 0, p.z));
  });
  pos.set([0, 0, 0], 0);
  const stars = makePoints(pos, col, size, markerMaterial());
  group.add(stars);
  const sun = makePoints(new Float32Array(3), new Float32Array([1, 0.92, 0.75]), new Float32Array([8]), markerMaterial());
  group.add(sun);
  const grid = new THREE.Group();
  [5, 10, 15, 20].forEach((r) => {
    const pts = [];
    for (let i = 0; i < 128; i++) pts.push(new THREE.Vector3(Math.cos(i / 128 * Math.PI * 2) * r, 0, Math.sin(i / 128 * Math.PI * 2) * r));
    grid.add(lineLoop(pts, 0x6f86b8, 0.22));
  });
  const dropGeo = new THREE.BufferGeometry().setFromPoints(drops);
  const dropMat = shader({
    vertex: 'gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
    fragment: 'gl_FragColor = vec4(0.5, 0.62, 0.9, 0.25 * uOpacity);',
  });
  grid.add(new THREE.LineSegments(dropGeo, dropMat));
  group.add(grid);

  const fieldN = quality.tier === 'low' ? 6000 : 18000;
  const r = rng(77);
  const fp = new Float32Array(fieldN * 3); const fc = new Float32Array(fieldN * 3); const fs = new Float32Array(fieldN);
  for (let i = 0; i < fieldN; i++) {
    const d = 15 + Math.pow(r(), 0.5) * 3000;
    const l = r() * Math.PI * 2;
    const b = gauss(r) * Math.min(1.2, 600 / d);
    galToGlobal(Math.cos(b) * Math.cos(l) * d, Math.cos(b) * Math.sin(l) * d, Math.sin(b) * d, v);
    fp[i * 3] = v.x; fp[i * 3 + 1] = v.y; fp[i * 3 + 2] = v.z;
    const t = r();
    const c = new THREE.Color(t < 0.08 ? 0xaabfff : t < 0.3 ? 0xf8f7ff : t < 0.6 ? 0xfff1df : t < 0.8 ? 0xffd2a1 : 0xffb56c);
    const k = 0.4 + Math.pow(r(), 4) * 1.4;
    fc[i * 3] = c.r * k; fc[i * 3 + 1] = c.g * k; fc[i * 3 + 2] = c.b * k;
    fs[i] = 2.2 * (0.5 + r());
  }
  const field = makePoints(fp, fc, fs, pointsMaterial({ min: 1.2, max: 6, gain: 0.9, core: 0.25 }));
  group.add(field);
  return {
    group,
    labels,
    update(t, logW) {
      grid.visible = logW > 16.5 && logW < 18.6;
      stars.visible = logW > 15.2;
      field.visible = logW > 16.4;
      const fa = Math.min(1, (logW - 16.4) / 1.2) * Math.min(1, Math.max(0, (20.6 - logW) / 0.8));
      field.material.uniforms.uOpacity.value *= Math.max(0, fa);
    },
    setPx(uPx, scale) { field.material.uniforms.uPx.value = uPx; field.material.uniforms.uScale.value = scale; },
  };
}
