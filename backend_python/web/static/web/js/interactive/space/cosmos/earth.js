import { THREE } from '../../core/engine.js';
import { shader, lineLoop, SCATTER, RA } from './shaders.js';
import { R_EARTH, R_MOON, KM, EVEREST } from './astro.js';

const TEX = '/static/web/js/interactive/space/cosmos/tex/';

function tex(loader, name, srgb = true) {
  const t = loader.load(TEX + name);
  t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  t.anisotropy = 8;
  return t;
}

export function createEarthSystem(quality, renderer) {
  const loader = new THREE.TextureLoader();
  const seg = quality.tier === 'low' ? 64 : 128;
  const day = tex(loader, quality.tier === 'high' ? 'earth_day_4k.jpg' : 'earth_day_2k.jpg');
  const night = tex(loader, 'earth_night_2k.jpg');
  const clouds = tex(loader, 'earth_clouds_2k.jpg', false);
  const moonTex = tex(loader, 'moon_2k.jpg');
  [day, night, clouds, moonTex].forEach((t) => { t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy()); });

  const sunLocal = { value: new THREE.Vector3(1, 0, 0) };
  const uTime = { value: 0 };
  const group = new THREE.Group();
  const globe = new THREE.Group();
  group.add(globe);

  const earthMat = shader({
    transparent: false, depthWrite: true,
    uniforms: { uDay: { value: day }, uNight: { value: night }, uClouds: { value: clouds }, uSun: sunLocal, uTime, uClear: { value: 0 } },
    vertexHead: 'varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying vec3 vC; varying vec3 vP;',
    vertex: `vUv = uv; vN = normalize(position); vP = position; vec4 wp = modelMatrix * vec4(position, 1.0);
      vC = (inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz;
      vV = normalize(vC - position);
      gl_Position = projectionMatrix * viewMatrix * wp;`,
    fragmentHead: `uniform sampler2D uDay; uniform sampler2D uNight; uniform sampler2D uClouds; uniform vec3 uSun; uniform float uTime; uniform float uClear;
      varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying vec3 vC; varying vec3 vP; ${SCATTER}`,
    fragment: `
      vec3 n = normalize(vN); vec3 v = normalize(vV); vec3 s = normalize(uSun);
      vec3 dayC = pow(texture2D(uDay, vUv).rgb, vec3(2.2));
      vec3 nightC = pow(texture2D(uNight, vUv).rgb, vec3(2.2));
      float ndl = dot(n, s);
      float ocean = smoothstep(0.02, 0.10, dayC.b - dayC.r) * (1.0 - smoothstep(0.10, 0.25, dayC.g));
      vec2 cuv = vUv + vec2(uTime * 0.0006, 0.0);
      vec2 shUv = cuv - vec2(s.x, s.y) * 0.0015;
      vec2 ev = (vUv - vec2(${((EVEREST.lon + 180) / 360).toFixed(5)}, ${((EVEREST.lat + 90) / 180).toFixed(5)})) * vec2(360.0 * ${Math.cos(EVEREST.lat * Math.PI / 180).toFixed(4)}, 180.0);
      float clear = 1.0 - uClear * 0.8 * (1.0 - smoothstep(2.0, 16.0, length(ev)));
      float cl = texture2D(uClouds, cuv).r * clear;
      float cs = texture2D(uClouds, shUv).r * clear;
      // sunlight that reaches the ground has crossed this much air (Kasten-Young), so it reddens at the terminator
      float zen = degrees(acos(clamp(ndl, -1.0, 1.0)));
      float air = 1.0 / (max(ndl, 0.0) + 0.50572 * pow(max(96.07995 - zen, 0.5), -1.6364));
      vec3 sunT = exp(-vec3(0.0059, 0.0137, 0.0331) * 8.0 * air - 0.004 * air);
      vec3 sun = sunT * smoothstep(-0.02, 0.04, ndl);
      vec3 lit = dayC * (1.0 - cs * 0.55) * max(0.0, ndl) * 2.4 * sun;
      vec3 h = normalize(s + v);
      float spec = pow(max(0.0, dot(n, h)), 90.0) * ocean * (1.0 - cl) * 2.6 + pow(max(0.0, dot(n, h)), 12.0) * ocean * 0.12;
      lit += vec3(1.0, 0.93, 0.82) * sun * spec;
      vec3 east = normalize(cross(vec3(0.0, 1.0, 0.0), n + vec3(1e-4, 0.0, 0.0))); vec3 north = cross(n, east);
      float cE = texture2D(uClouds, cuv + vec2(0.003, 0.0)).r; float cN = texture2D(uClouds, cuv + vec2(0.0, 0.003)).r;
      vec3 cn = normalize(n - (east * (cE - cl) + north * (cN - cl)) * 0.8);
      float cdl = max(0.0, dot(cn, s));
      vec3 cloudC = vec3(1.0) * (cdl * 2.1 * sun + vec3(0.06, 0.08, 0.12) * smoothstep(-0.2, 0.1, ndl));
      lit = mix(lit, cloudC, cl * 0.92);
      vec3 lights = nightC * vec3(1.0, 0.78, 0.45) * 2.2 * (1.0 - cl * 0.8) * (1.0 - smoothstep(-0.1, 0.02, ndl));
      vec3 col = lit + lights;
      vec3 ro = vC; vec3 rd = normalize(vP - vC); vec3 Ls; vec3 Ts;
      scatter(ro, rd, length(vP - vC), s, 6, Ls, Ts);
      col = col * Ts + Ls * 14.0;
      col = 1.0 - exp(-col * 1.1);
      gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);`,
  });
  const earth = new THREE.Mesh(new THREE.SphereGeometry(1, seg, seg / 2), earthMat);
  globe.add(earth);

  const atmMat = shader({
    uniforms: { uSun: sunLocal },
    vertexHead: 'varying vec3 vP; varying vec3 vC;',
    vertex: `vC = (inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz; vP = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);`,
    fragmentHead: `uniform vec3 uSun; varying vec3 vP; varying vec3 vC; ${SCATTER}`,
    fragment: `
      vec3 ro = vC; vec3 rd = normalize(vP - vC);
      if (hitSphere(ro, rd, 1.0).x > 0.0) discard;
      vec3 L; vec3 T;
      scatter(ro, rd, 1e9, normalize(uSun), 12, L, T);
      L = 1.0 - exp(-L * 14.0 * 1.1);
      float A = 1.0 - dot(T, vec3(0.3333));
      gl_FragColor = vec4(pow(L, vec3(1.0 / 2.2)) * uOpacity, A * uOpacity);`,
  });
  atmMat.blending = THREE.CustomBlending;
  atmMat.blendSrc = THREE.OneFactor; atmMat.blendDst = THREE.OneMinusSrcAlphaFactor;
  atmMat.blendSrcAlpha = THREE.ZeroFactor; atmMat.blendDstAlpha = THREE.OneFactor;
  const atmosphere = new THREE.Mesh(new THREE.SphereGeometry(RA, seg, seg / 2), atmMat);
  const camLocal = new THREE.Vector3();
  atmosphere.onBeforeRender = (r, sc, cam) => {
    const inside = atmosphere.worldToLocal(camLocal.copy(cam.position)).length() < RA;
    atmMat.side = inside ? THREE.BackSide : THREE.FrontSide;
  };
  globe.add(atmosphere);

  const moonGroup = new THREE.Group();
  group.add(moonGroup);
  const moonMat = shader({
    transparent: false, depthWrite: true,
    uniforms: { uMap: { value: moonTex }, uSun: { value: new THREE.Vector3(1, 0, 0) } },
    vertexHead: 'varying vec2 vUv; varying vec3 vN; varying vec3 vV;',
    vertex: `vUv = uv; vN = normalize(position); vV = normalize((inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz - position);
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);`,
    fragmentHead: 'uniform sampler2D uMap; uniform vec3 uSun; varying vec2 vUv; varying vec3 vN; varying vec3 vV;',
    fragment: `
      vec3 n = normalize(vN); vec3 s = normalize(uSun); vec3 v = normalize(vV);
      vec3 c = pow(texture2D(uMap, vUv).rgb, vec3(2.2));
      float mu0 = max(0.0, dot(n, s)); float mu = max(0.0, dot(n, v));
      float ls = mu0 / max(1e-3, mu0 + mu);
      vec3 col = c * (ls * 2.0 * 0.7 + mu0 * 0.6) * 2.4 + c * 0.004;
      col = 1.0 - exp(-col);
      gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);`,
  });
  const moon = new THREE.Mesh(new THREE.SphereGeometry(R_MOON / R_EARTH, seg / 2, seg / 4), moonMat);
  moonGroup.add(moon);

  const orbitPts = [];
  let orbit = null;

  return {
    group,
    globe,
    moon,
    moonGroup,
    setup({ earthQuat, moonOffset, sunGlobal }) {
      globe.quaternion.copy(earthQuat);
      const inv = earthQuat.clone().invert();
      sunLocal.value.copy(sunGlobal).applyQuaternion(inv).normalize();
      const m = moonOffset.clone().divideScalar(R_EARTH);
      moon.position.copy(m);
      moon.lookAt(0, 0, 0);
      moon.rotateY(-Math.PI / 2);
      const mi = moon.quaternion.clone().invert();
      moonMat.uniforms.uSun.value.copy(sunGlobal).applyQuaternion(mi).normalize();
      const r = m.length();
      const nrm = new THREE.Vector3(0, 1, 0).applyAxisAngle(new THREE.Vector3(1, 0, 0), 5.14 * Math.PI / 180);
      const a = m.clone().normalize();
      const b = new THREE.Vector3().crossVectors(nrm, a).normalize();
      for (let i = 0; i < 256; i++) {
        const t = i / 256 * Math.PI * 2;
        orbitPts.push(a.clone().multiplyScalar(Math.cos(t) * r).addScaledVector(b, Math.sin(t) * r));
      }
      orbit = lineLoop(orbitPts, 0x9fb4d8, 0.35);
      group.add(orbit);
    },
    update(t, logW) {
      uTime.value = t;
      earth.rotation.y = 0;
      earthMat.uniforms.uClear.value = 1 - Math.min(1, Math.max(0, (logW - 6.9) / 0.9));
      atmosphere.visible = logW > 5.2;
      if (orbit) orbit.visible = logW > 7.8 && logW < 11.5;
      moonGroup.visible = logW > 6.2 && logW < 11.6;
    },
    labels: [
      { text: 'Earth', sub: '12 742 km across', get: (v) => v.set(0, 0, 0), min: 6.6, max: 11.4 },
      { text: 'The Moon', sub: '384 400 km away · 3 474 km across', get: (v) => v.copy(moon.position), min: 8.1, max: 10.6 },
    ],
    dispose() { [day, night, clouds, moonTex].forEach((t) => t.dispose()); },
    R: R_EARTH,
    KM,
  };
}
