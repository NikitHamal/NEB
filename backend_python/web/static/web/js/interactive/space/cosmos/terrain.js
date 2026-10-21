import { THREE } from '../../core/engine.js';
import { NOISE, shader, SCATTER } from './shaders.js';
import { R_EARTH, EVEREST } from './astro.js';

const TEX = '/static/web/js/interactive/space/cosmos/tex/';

function loadImage(url) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = url;
  });
}

async function loadDEM(name, sizeMeters) {
  const img = await loadImage(TEX + name);
  const n = img.width;
  const c = document.createElement('canvas');
  c.width = n; c.height = n;
  const g = c.getContext('2d', { willReadFrequently: true });
  g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, n, n).data;
  const h = new Float32Array(n * n);
  let max = -1; let at = 0;
  for (let i = 0; i < n * n; i++) {
    h[i] = ((d[i * 4] << 8) | d[i * 4 + 1]) / 65535 * 8900;
    if (h[i] > max) { max = h[i]; at = i; }
  }
  return { n, h, max, ax: at % n, ay: Math.floor(at / n), px: sizeMeters / n };
}

function sampler(dem) {
  const { n, h } = dem;
  return (x, y) => {
    x = Math.min(n - 1.001, Math.max(0, x)); y = Math.min(n - 1.001, Math.max(0, y));
    const ix = Math.floor(x); const iy = Math.floor(y); const fx = x - ix; const fy = y - iy;
    const a = h[iy * n + ix]; const b = h[iy * n + ix + 1]; const c = h[(iy + 1) * n + ix]; const d = h[(iy + 1) * n + ix + 1];
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy;
  };
}

function buildGrid(dem, grid, sunLocal, scaleTo) {
  const { n, px } = dem;
  const sample = sampler(dem);
  const hScale = scaleTo / dem.max;
  const step = (n - 1) / (grid - 1);
  const pos = new Float32Array(grid * grid * 3);
  const nor = new Float32Array(grid * grid * 3);
  const light = new Float32Array(grid * grid * 2);
  const H = new Float32Array(grid * grid);
  for (let j = 0; j < grid; j++) {
    for (let i = 0; i < grid; i++) H[j * grid + i] = sample(i * step, j * step) * hScale;
  }
  const cell = px * step;
  const sx = sunLocal.x; const sz = sunLocal.z; const sy = sunLocal.y;
  const horiz = Math.hypot(sx, sz) || 1e-6;
  const tanElev = sy / horiz;
  const dx = sx / horiz; const dz = sz / horiz;
  const blurR = Math.max(2, Math.round(grid / 64));
  for (let j = 0; j < grid; j++) {
    for (let i = 0; i < grid; i++) {
      const k = j * grid + i;
      const x = (i * step - dem.ax) * px;
      const z = (j * step - dem.ay) * px;
      const y = H[k];
      pos[k * 3] = x; pos[k * 3 + 1] = y; pos[k * 3 + 2] = z;
      const hl = H[j * grid + Math.max(0, i - 1)]; const hr = H[j * grid + Math.min(grid - 1, i + 1)];
      const hu = H[Math.max(0, j - 1) * grid + i]; const hd = H[Math.min(grid - 1, j + 1) * grid + i];
      const nx = (hl - hr) / (2 * cell); const nz = (hu - hd) / (2 * cell);
      const inv = 1 / Math.hypot(nx, 1, nz);
      nor[k * 3] = nx * inv; nor[k * 3 + 1] = inv; nor[k * 3 + 2] = nz * inv;
      let lit = 1;
      for (let s = 1; s < 260; s++) {
        const ti = i + dx * s * 0.75; const tj = j + dz * s * 0.75;
        if (ti < 0 || tj < 0 || ti > grid - 1 || tj > grid - 1) break;
        const ray = y + tanElev * s * 0.75 * cell;
        if (ray > scaleTo + 50) break;
        const th = H[Math.round(tj) * grid + Math.round(ti)];
        const over = (th - ray) / (cell * 0.6);
        if (over > -1) lit = Math.min(lit, Math.max(0, -over));
        if (lit <= 0) break;
      }
      let sum = 0; let cnt = 0;
      for (let b = -blurR; b <= blurR; b += blurR) {
        for (let a = -blurR; a <= blurR; a += blurR) {
          const ii = Math.min(grid - 1, Math.max(0, i + a)); const jj = Math.min(grid - 1, Math.max(0, j + b));
          sum += H[jj * grid + ii]; cnt++;
        }
      }
      const ao = Math.min(1, Math.max(0.35, 1 + (y - sum / cnt) / (cell * blurR * 1.6)));
      light[k * 2] = lit; light[k * 2 + 1] = ao;
    }
  }
  const idx = new Uint32Array((grid - 1) * (grid - 1) * 6);
  let p = 0;
  for (let j = 0; j < grid - 1; j++) {
    for (let i = 0; i < grid - 1; i++) {
      const a = j * grid + i; const b = a + 1; const c = a + grid; const d = c + 1;
      idx[p++] = a; idx[p++] = c; idx[p++] = b; idx[p++] = b; idx[p++] = c; idx[p++] = d;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  geo.setAttribute('light', new THREE.BufferAttribute(light, 2));
  geo.setIndex(new THREE.BufferAttribute(idx, 1));
  geo.computeBoundingSphere();
  return { geo, sample: (x, z) => sample(x / px + dem.ax, z / px + dem.ay) * hScale };
}

function terrainMaterial(regional) {
  return shader({
    transparent: regional,
    depthWrite: true,
    uniforms: {
      uSun: { value: new THREE.Vector3(0, 1, 0) },
      uHole: { value: 0 },
      uMpu: { value: 1 },
      uFade: { value: 1 },
      uSat: { value: null },
      uHaze: { value: new THREE.Color(0x8fa9cf) },
      uVis: { value: 1 },
    },
    vertexHead: `attribute vec2 light; varying vec3 vP; varying vec3 vN; varying vec2 vL; varying float vDist;`,
    vertex: `
      vec3 p = position;
      vP = p;
      float r2 = dot(p.xz, p.xz);
      p.y -= r2 / (2.0 * ${R_EARTH.toFixed(1)});
      vN = normal; vL = light;
      vec4 mv = modelViewMatrix * vec4(p, 1.0);
      vDist = -mv.z;
      gl_Position = projectionMatrix * mv;`,
    fragmentHead: `uniform vec3 uSun; uniform float uHole; uniform float uMpu; uniform float uFade; uniform vec3 uHaze; uniform sampler2D uSat; uniform float uVis;
      varying vec3 vP; varying vec3 vN; varying vec2 vL; varying float vDist; ${NOISE}`,
    fragment: `
      if (uHole > 0.0 && max(abs(vP.x), abs(vP.z)) < uHole) discard;
      if (${regional ? '1' : '0'} == 0 && uHole < 0.0 && length(vP.xz) < -uHole) discard;
      float dith = hash13(vec3(gl_FragCoord.xy, 0.0));
      ${regional ? 'float edgeA = smoothstep(172000.0, 100000.0, length(vP.xz)) * uVis; if (edgeA < 0.004) discard;' : 'float edgeA = 1.0; if (dith > smoothstep(12900.0, 10600.0, max(abs(vP.x), abs(vP.z)))) discard;'}
      vec3 n = normalize(vN);
      float detail = fbm3(vP * ${regional ? '0.0012' : '0.012'}) - 0.5;
      float fine = fbm3(vP * ${regional ? '0.01' : '0.11'}) - 0.5;
      vec3 bump = vec3(fbm3(vP * 0.02 + 3.1) - 0.5, 0.0, fbm3(vP * 0.02 + 7.7) - 0.5);
      n = normalize(n + bump * 0.35);
      float alt = vP.y;
      float slope = n.y;
      float snowLine = 5700.0 + detail * 900.0;
      float snow = smoothstep(snowLine - 250.0, snowLine + 250.0, alt) * smoothstep(0.64 + fine * 0.15, 0.82 + fine * 0.1, slope);
      snow = max(snow, smoothstep(8300.0, 8700.0, alt) * smoothstep(0.42, 0.62, slope));
      float glacier = smoothstep(4700.0, 5300.0, alt) * smoothstep(0.86, 0.95, slope) * (1.0 - smoothstep(6400.0, 6600.0, alt));
      vec3 rockDark = vec3(0.17, 0.155, 0.15);
      vec3 rockWarm = vec3(0.36, 0.31, 0.26);
      float strata = sin(alt * 0.013 + detail * 9.0 + fine * 4.0) * 0.5 + 0.5;
      vec3 rock = mix(rockDark, rockWarm, clamp(strata * 0.6 + fine + 0.25, 0.0, 1.0));
      float yellowBand = smoothstep(8150.0, 8250.0, alt) * (1.0 - smoothstep(8500.0, 8600.0, alt));
      rock = mix(rock, vec3(0.55, 0.45, 0.30), yellowBand * 0.8);
      vec3 base = rock;
      ${regional ? `
      float veg = 1.0 - smoothstep(2600.0, 4000.0, alt + detail * 500.0);
      float forest = 1.0 - smoothstep(1400.0, 3200.0, alt + detail * 400.0);
      vec3 tundra = mix(vec3(0.42, 0.36, 0.27), vec3(0.50, 0.44, 0.33), fine + 0.5);
      base = mix(base, tundra, smoothstep(0.6, 0.85, slope) * (1.0 - smoothstep(5000.0, 5600.0, alt)));
      base = mix(base, mix(vec3(0.20, 0.26, 0.12), vec3(0.08, 0.16, 0.07), forest), veg);
      float lat = ${EVEREST.lat.toFixed(5)} - vP.z / 110574.0;
      float lon = ${EVEREST.lon.toFixed(5)} + vP.x / (111320.0 * cos(radians(lat)));
      vec3 sat = pow(texture2D(uSat, vec2((lon + 180.0) / 360.0, (lat + 90.0) / 180.0)).rgb, vec3(2.2)) * 1.25;
      base = mix(base, sat * (0.85 + fine * 0.4), 0.6 * (1.0 - smoothstep(4200.0, 5400.0, alt)));
      base = mix(base, sat, 1.0 - uFade);
      ` : `
      vec3 moraine = mix(vec3(0.33, 0.30, 0.27), vec3(0.24, 0.22, 0.20), fine + 0.5);
      base = mix(base, moraine, smoothstep(0.7, 0.9, slope) * (1.0 - smoothstep(5200.0, 5600.0, alt)));
      `}
      vec3 ice = mix(vec3(0.62, 0.70, 0.76), vec3(0.42, 0.40, 0.38), smoothstep(0.1, 0.4, fine + 0.3));
      base = mix(base, ice, glacier);
      vec3 snowC = vec3(0.93, 0.95, 0.98) * (0.92 + fine * 0.12);
      base = mix(base, snowC, snow);
      float ndl = max(0.0, dot(n, uSun));
      float lit = vL.x;
      vec3 sky = vec3(0.38, 0.52, 0.80);
      vec3 col = base * (vec3(1.0, 0.97, 0.92) * 2.4 * ndl * lit + sky * (0.55 + 0.25 * n.y) * vL.y);
      float meters = min(vDist * uMpu, ${regional ? '45000.0' : '60000.0'});
      float haze = 1.0 - exp(-meters / ${regional ? '120000.0' : '70000.0'});
      col = mix(col, uHaze, haze * 0.75 * uFade);
      col = col / (col + vec3(0.85)) * 1.25;
      gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), edgeA * uOpacity);`,
  });
}

function summitCap(sample, sunLocal) {
  const R = 110; const seg = 120;
  const ring = new THREE.RingGeometry(0.01, R, 96, 60);
  const pos = ring.attributes.position;
  const light = new Float32Array(pos.count * 2);
  const H = (x, z) => {
    const r = Math.min(R, Math.hypot(x, z));
    const ridge = Math.exp(-Math.pow((x * 0.8 + z * 0.6) / 6, 2)) * 1.2;
    const platform = Math.exp(-(r * r) / 18) * 0.9;
    let y = sample(x, z) + ridge * (1 - r / R) + platform;
    y += (Math.sin(x * 1.3 + z * 0.4) * 0.12 + Math.sin(z * 2.1 - x * 0.7) * 0.08) * (1 - r / R);
    return y - Math.pow(r / R, 6) * 3;
  };
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i); const z = -pos.getY(i);
    pos.setXYZ(i, x, H(x, z), z);
    light[i * 2] = 1; light[i * 2 + 1] = 1;
  }
  ring.setAttribute('light', new THREE.BufferAttribute(light, 2));
  ring.computeVertexNormals();
  const mat = shader({
    transparent: false, depthWrite: true,
    uniforms: { uSun: { value: sunLocal.clone() }, uMpu: { value: 1 } },
    vertexHead: 'varying vec3 vP; varying vec3 vN; varying float vDist;',
    vertex: 'vP = position; vN = normal; vec4 mv = modelViewMatrix * vec4(position, 1.0); vDist = -mv.z; gl_Position = projectionMatrix * mv;',
    fragmentHead: `uniform vec3 uSun; uniform float uMpu; varying vec3 vP; varying vec3 vN; varying float vDist; ${NOISE}`,
    fragment: `
      vec3 n = normalize(vN);
      vec3 b = vec3(fbm3(vP * 1.7) - 0.5, 0.0, fbm3(vP * 1.7 + 5.3) - 0.5);
      vec3 b2 = vec3(vnoise(vP * 9.0) - 0.5, 0.0, vnoise(vP * 9.0 + 2.0) - 0.5);
      n = normalize(n + b * 0.45 + b2 * 0.12);
      float ndl = max(0.0, dot(n, uSun));
      float sss = pow(max(0.0, 1.0 - n.y), 2.0) * 0.15;
      vec3 snowC = vec3(0.94, 0.96, 1.0);
      vec3 col = snowC * (vec3(1.0, 0.97, 0.92) * 2.3 * ndl + vec3(0.36, 0.52, 0.86) * (0.6 + 0.3 * n.y)) + vec3(0.2, 0.35, 0.6) * sss;
      vec3 h = normalize(uSun + vec3(0.0, 0.2, 0.9));
      float glint = step(0.994, hash13(floor(vP * 40.0))) * pow(max(0.0, dot(n, h)), 30.0) * 3.0;
      col += glint * smoothstep(12.0, 2.0, vDist * uMpu);
      col = col / (col + vec3(0.85)) * 1.25;
      gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);`,
  });
  const mesh = new THREE.Mesh(ring, mat);
  mesh.userData.height = H;
  return mesh;
}

// The sky seen from the summit, 8 849 m up: the same single-scattering atmosphere as the globe,
// so the zenith is the deep blue of a third of the air, the horizon pales, and the sun is a white disc.
export function skyMaterial() {
  return shader({
    depthWrite: false,
    uniforms: { uUp: { value: new THREE.Vector3(0, 1, 0) }, uSun: { value: new THREE.Vector3(0, 1, 0) } },
    vertexHead: 'varying vec3 vDir;',
    vertex: 'vDir = normalize((modelMatrix * vec4(position, 1.0)).xyz - cameraPosition); gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);',
    fragmentHead: `uniform vec3 uUp; uniform vec3 uSun; varying vec3 vDir; ${SCATTER}`,
    fragment: `
      vec3 up = normalize(uUp); vec3 d = normalize(vDir); vec3 sd = normalize(uSun);
      vec3 x = normalize(cross(up, abs(up.y) < 0.9 ? vec3(0.0, 1.0, 0.0) : vec3(1.0, 0.0, 0.0))); vec3 z = cross(x, up);
      vec3 rd = vec3(dot(d, x), dot(d, up), dot(d, z)); vec3 s = vec3(dot(sd, x), dot(sd, up), dot(sd, z));
      vec3 ro = vec3(0.0, 1.0 + ${(EVEREST.height / 6.371e6).toFixed(7)}, 0.0);
      float g = hitSphere(ro, rd, 1.0).x;
      vec3 L; vec3 T;
      scatter(ro, rd, g > 0.0 ? g : 1e9, s, 10, L, T);
      vec3 col = L * 16.0;
      float mu = dot(rd, s);
      col += T * smoothstep(0.99996, 0.99999, mu) * 60.0 + T * pow(max(mu, 0.0), 900.0) * 3.0;
      if (g > 0.0) col += vec3(0.55, 0.6, 0.68) * T * 0.35 * max(s.y, 0.0);
      col = 1.0 - exp(-col * 1.1);
      gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), uOpacity);`,
    side: THREE.BackSide,
  });
}

export async function createTerrain(quality, sunLocal, satTexture) {
  const tier = quality.tier;
  const [fineDem, regDem] = await Promise.all([
    loadDEM('dem_everest_26km.png', 25917),
    loadDEM('dem_himalaya_345km.png', 345590),
  ]);
  const fine = buildGrid(fineDem, tier === 'high' ? 448 : tier === 'medium' ? 320 : 224, sunLocal, EVEREST.height);
  const regScale = EVEREST.height;
  const reg = buildGrid(regDem, tier === 'high' ? 320 : tier === 'medium' ? 256 : 160, sunLocal, regScale);
  const fineMat = terrainMaterial(false);
  const regMat = terrainMaterial(true);
  regMat.uniforms.uSat.value = satTexture;
  fineMat.uniforms.uSun.value.copy(sunLocal);
  regMat.uniforms.uSun.value.copy(sunLocal);
  const fineMesh = new THREE.Mesh(fine.geo, fineMat);
  const regMesh = new THREE.Mesh(reg.geo, regMat);
  regMesh.position.y = -0.5;
  const cap = summitCap(fine.sample, sunLocal);
  const group = new THREE.Group();
  group.add(regMesh, fineMesh, cap);
  const summitY = cap.geometry.attributes.position.getY(0);
  return {
    group,
    summitY,
    height: { n: regDem.n, h: regDem.h, px: regDem.px, ax: regDem.ax, ay: regDem.ay, scale: regScale / regDem.max },
    sample: fine.sample,
    capHeight: cap.userData.height,
    update(logW, mpu) {
      fineMat.uniforms.uMpu.value = mpu; regMat.uniforms.uMpu.value = mpu; cap.material.uniforms.uMpu.value = mpu;
      cap.visible = logW < 2.3;
      fineMesh.visible = logW < 5.6;
      regMesh.visible = logW > 3.0 && logW < 6.6;
      regMat.uniforms.uVis.value = 1 - Math.min(1, Math.max(0, (logW - 5.9) / 0.65));
      regMat.uniforms.uFade.value = 1 - Math.min(1, Math.max(0, (logW - 4.9) / 1.4));
      fineMat.uniforms.uFade.value = 1 - Math.min(1, Math.max(0, (logW - 4.2) / 1.0));
      fineMat.uniforms.uHole.value = cap.visible ? -100 : 0;
      regMat.uniforms.uHole.value = fineMesh.visible ? 10600 : 0;
    },
    dispose() { fine.geo.dispose(); reg.geo.dispose(); cap.geometry.dispose(); fineMat.dispose(); regMat.dispose(); cap.material.dispose(); },
  };
}
