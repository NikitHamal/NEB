import { THREE } from '../../core/engine.js';
import {
  AU, LY, R_EARTH, EVEREST, D2R, PLANETS, GALACTIC_R0, GAL_QUAT,
  daysSinceJ2000, planetPosition, moonOffset, eqToGlobal, galLB, basisQuaternion, smooth,
} from './astro.js';
import { setOpacity } from './shaders.js';
import { createTerrain, skyMaterial } from './terrain.js';
import { createClimber } from './climber.js';
import { createEarthSystem } from './earth.js';
import { createSolarSystem } from './solar.js';
import { createSkyBackground, createStarNeighbourhood } from './stars.js';
import { createMilkyWay, createLocalGroup } from './galaxy.js';
import { createCosmicWeb, createObservableUniverse } from './web.js';
import { viewQuaternion, keyframed } from './view.js';

const VIEW = 10;

function geometry() {
  const days = daysSinceJ2000(new Date());
  const earthPos = planetPosition(PLANETS[2], days);
  const sunDir = earthPos.clone().negate().normalize();
  const e1 = eqToGlobal(1, 0, 0); const e2 = eqToGlobal(0, 1, 0); const pole = eqToGlobal(0, 0, 1);
  const alpha = Math.atan2(sunDir.dot(e2), sunDir.dot(e1));
  const lat = EVEREST.lat * D2R; const lon = EVEREST.lon * D2R;
  const theta = alpha + 52 * D2R - lon;
  const g = e1.clone().multiplyScalar(Math.cos(theta)).addScaledVector(e2, Math.sin(theta));
  const e90 = e1.clone().multiplyScalar(-Math.sin(theta)).addScaledVector(e2, Math.cos(theta));
  const earthQuat = basisQuaternion(g, pole, e90.clone().negate());
  const m = theta + lon;
  const meridian = e1.clone().multiplyScalar(Math.cos(m)).addScaledVector(e2, Math.sin(m));
  const up = meridian.clone().multiplyScalar(Math.cos(lat)).addScaledVector(pole, Math.sin(lat)).normalize();
  const east = e1.clone().multiplyScalar(-Math.sin(m)).addScaledVector(e2, Math.cos(m)).normalize();
  const north = new THREE.Vector3().crossVectors(up, east).normalize();
  const summitQuat = basisQuaternion(east, up, north.clone().negate());
  const summitOrigin = earthPos.clone().addScaledVector(up, R_EARTH);
  const gc = galLB(0, 0, GALACTIC_R0);
  const m31 = galLB(121.17, -21.57, 2.54e6 * LY);
  const lg = m31.clone().multiplyScalar(0.42);
  const ga = galLB(325.3, -7.3, 2.2e8 * LY);
  return { days, earthPos, sunDir, earthQuat, up, east, north, summitQuat, summitOrigin, gc, m31, lg, ga, pole };
}

export function createUniverse(engine, { onProgress } = {}) {
  const { scene, camera, quality, renderer } = engine;
  const G = geometry();
  const root = new THREE.Group();
  scene.add(root);
  const layers = [];
  const labelDefs = [];

  function layer(id, opts) {
    const L = {
      id, group: new THREE.Group(), unit: opts.unit, origin: opts.origin, quat: opts.quat || new THREE.Quaternion(),
      win: opts.win, alpha: 0, impl: null, build: opts.build, built: false, building: null, eager: opts.eager,
    };
    L.group.visible = false;
    root.add(L.group);
    layers.push(L);
    return L;
  }

  function ensure(L) {
    if (L.built || L.building) return L.building;
    L.building = Promise.resolve().then(() => L.build()).then((impl) => {
      L.impl = impl;
      L.group.add(impl.group);
      (impl.labels || []).forEach((d) => labelDefs.push({ layer: L, def: d }));
      L.built = true;
      if (onProgress) onProgress(L.id, impl.labels || []);
    });
    return L.building;
  }

  const sunSummit = G.sunDir.clone().applyQuaternion(G.summitQuat.clone().invert());
  let terrain = null;
  let climber = null;
  const summit = layer('summit', {
    unit: 1, origin: G.summitOrigin, quat: G.summitQuat, win: [-5, 7.0], eager: true,
    build: async () => {
      const g = new THREE.Group();
      const sat = new THREE.TextureLoader().load(`/static/web/js/interactive/space/cosmos/tex/${quality.tier === 'high' ? 'earth_day_4k' : 'earth_day_2k'}.jpg`);
      sat.colorSpace = THREE.NoColorSpace;
      terrain = await createTerrain(quality, sunSummit, sat);
      g.add(terrain.group);
      const rot = 0.2; const base = terrain.summitY - 0.08;
      climber = createClimber((x, z) => terrain.capHeight(x * Math.cos(rot) + z * Math.sin(rot), -x * Math.sin(rot) + z * Math.cos(rot)) - base);
      climber.group.position.y = base;
      climber.group.rotation.y = rot;
      g.add(climber.group);
      const sun = new THREE.DirectionalLight(0xfff1df, 3.2);
      sun.position.copy(sunSummit).multiplyScalar(10);
      g.add(sun, sun.target);
      const hemi = new THREE.HemisphereLight(0x8fb4ff, 0xe8eef8, 1.1);
      g.add(hemi);
      const S = (x, z) => terrain.sample(x, z);
      return {
        group: g,
        labels: [
          { text: 'You', sub: '1.7 m tall, on the summit', get: (v) => v.set(0.25, terrain.summitY + 1.85, 0), min: -2, max: 1.7, cls: 'here' },
          { text: 'Mount Everest · Sagarmatha', sub: '8 849 m, the highest point on Earth', get: (v) => v.set(0, terrain.summitY + 40, 0), min: 2.4, max: 4.7, cls: 'here' },
          { text: 'Lhotse', sub: '8 516 m', get: (v) => v.set(790, S(790, 2930) + 60, 2930), min: 3.4, max: 4.7, minor: true },
          { text: 'Nuptse', sub: '7 861 m', get: (v) => v.set(-3830, S(-3830, 2310) + 60, 2310), min: 3.5, max: 4.7, minor: true },
          { text: 'Everest Base Camp', sub: '5 364 m', get: (v) => v.set(-7120, S(-7120, -1600) + 40, -1600), min: 3.8, max: 4.9 },
          { text: 'Makalu', sub: '8 485 m', get: (v) => v.set(16100, S(16100, 10900) + 60, 10900), min: 4.2, max: 5.2, minor: true },
          { text: 'Kathmandu', sub: 'capital of Nepal, 1 400 m', get: (v) => v.set(-157400, 1500, 30000), min: 5.0, max: 6.2 },
          { text: 'Nepal', sub: '', get: (v) => v.set(-60000, 3000, 70000), min: 5.0, max: 6.4 },
          { text: 'Tibet', sub: 'the Tibetan Plateau, ~4 500 m', get: (v) => v.set(20000, 5500, -110000), min: 5.0, max: 6.4, minor: true },
        ],
      };
    },
  });
  const skyMat = skyMaterial();
  const sky = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 16), skyMat);
  sky.renderOrder = -10;
  sky.frustumCulled = false;
  scene.add(sky);

  const earthsys = layer('earth', {
    unit: R_EARTH, origin: G.earthPos, win: [5.0, 11.8], eager: true,
    build: () => {
      const es = createEarthSystem(quality, renderer);
      es.setup({ earthQuat: G.earthQuat, moonOffset: moonOffset(G.days), sunGlobal: G.sunDir });
      return { ...es, update: (t, lw) => es.update(t, lw) };
    },
  });
  const solar = layer('solar', { unit: AU, origin: new THREE.Vector3(), win: [7.5, 17.8], build: () => createSolarSystem(quality, G.days) });
  const stars = layer('stars', { unit: LY, origin: new THREE.Vector3(), win: [15.2, 20.6], build: () => createStarNeighbourhood(quality) });
  const galaxy = layer('galaxy', { unit: LY * 1000, origin: G.gc, quat: GAL_QUAT, win: [18.6, 24.8], build: () => createMilkyWay(quality) });
  const group = layer('localgroup', { unit: LY * 1000, origin: new THREE.Vector3(), win: [21.4, 25.0], build: () => createLocalGroup(quality) });
  const web = layer('web', { unit: LY * 1e6, origin: new THREE.Vector3(), win: [23.0, 26.7], build: () => createCosmicWeb(quality) });
  const universe = layer('universe', { unit: LY * 1e9, origin: new THREE.Vector3(), win: [25.4, 30], build: () => createObservableUniverse(quality) });
  const skyStars = createSkyBackground(quality);
  root.add(skyStars);

  const summitFocus = G.summitOrigin.clone();
  let summitReady = false;
  const chain = () => [
    { p: summitFocus }, { p: G.earthPos, s: 0.3, e: 3.0 }, { p: new THREE.Vector3(), s: 0.15, e: 2.5 },
    { p: G.gc, s: 0.15, e: 2.5 }, { p: G.lg, s: 0.15, e: 2.5 }, { p: G.ga.clone().multiplyScalar(0.6), s: 0.12, e: 2.0 },
    { p: new THREE.Vector3(), s: 30, e: 260 },
  ];
  let FK = chain();
  function focusAt(W, out) {
    out.copy(FK[0].p);
    for (let i = 1; i < FK.length; i++) {
      const d = FK[i].p.distanceTo(FK[i - 1].p) || 1;
      const t = smooth(Math.log(FK[i].s), Math.log(FK[i].e), Math.log(W / d));
      if (t <= 0) break;
      out.lerp(FK[i].p, t);
      if (t < 1) break;
      out.copy(FK[i].p);
    }
    return out;
  }

  const eclUp = new THREE.Vector3(0, 1, 0);
  const galUp = new THREE.Vector3(0, 1, 0).applyQuaternion(GAL_QUAT);
  const sunFromGC = G.gc.clone().negate().normalize();
  const sideOfGal = sunFromGC.clone().applyAxisAngle(galUp, 0.9);
  const lgFront = new THREE.Vector3().crossVectors(galUp, G.m31.clone().normalize()).normalize();
  const camFront = G.north.clone().negate().multiplyScalar(0.85).addScaledVector(G.east, 0.55);
  const OK = [
    { log: 1.0, value: { q: viewQuaternion(G.up, camFront), e: 0.2 } },
    { log: 2.8, value: { q: viewQuaternion(G.up, camFront), e: 0.32 } },
    { log: 4.6, value: { q: viewQuaternion(G.up, camFront), e: 0.5 } },
    { log: 7.0, value: { q: viewQuaternion(G.pole, G.up), e: 0.42 } },
    { log: 9.6, value: { q: viewQuaternion(G.pole, G.up.clone().applyAxisAngle(G.pole, -0.5)), e: 0.35 } },
    { log: 12.0, value: { q: viewQuaternion(eclUp, G.earthPos.clone().normalize().applyAxisAngle(eclUp, -0.7)), e: 0.5 } },
    { log: 16.0, value: { q: viewQuaternion(eclUp, G.earthPos.clone().normalize().applyAxisAngle(eclUp, 0.3)), e: 0.42 } },
    { log: 18.0, value: { q: viewQuaternion(galUp, sideOfGal), e: 0.3 } },
    { log: 21.2, value: { q: viewQuaternion(galUp, sideOfGal), e: 0.85 } },
    { log: 23.4, value: { q: viewQuaternion(galUp, lgFront), e: 0.4 } },
    { log: 25.4, value: { q: viewQuaternion(galUp, lgFront.clone().applyAxisAngle(galUp, 0.8)), e: 0.3 } },
    { log: 27.0, value: { q: viewQuaternion(galUp, lgFront.clone().applyAxisAngle(galUp, 1.4)), e: 0.35 } },
  ];
  const mixO = (a, b, t) => ({ q: a.q.clone().slerp(b.q, t), e: a.e + (b.e - a.e) * t });

  let override = null;
  const tmp = new THREE.Vector3();
  const focus = new THREE.Vector3();

  let blendFrom = null;
  let blendT = 1;
  function setOverride(o) {
    blendFrom = focus.clone();
    blendT = 0;
    override = o ? { ...o } : null;
  }

  function fade(win, lw) {
    return Math.min(1, Math.max(0, (lw - win[0]) / 0.6), Math.max(0, (win[1] - lw) / 0.6));
  }

  function frame(lw, t, dt, orbit, D) {
    if (!summitReady && terrain) {
      summitFocus.copy(G.summitOrigin).addScaledVector(G.up, terrain.summitY + 0.95);
      summitReady = true;
      FK = chain();
    }
    focusAt(Math.pow(10, lw), focus);
    if (override) {
      const w = 1 - smooth(override.log + 0.8, override.log + 2.4, lw);
      if (w <= 0 && lw > override.log + 2.4) override = null;
      else focus.lerp(override.get(tmp), w);
    }
    if (blendFrom && blendT < 1) {
      blendT = Math.min(1, blendT + dt / 1.6);
      focus.lerpVectors(blendFrom, focus, smooth(0, 1, blendT));
    }
    const o = keyframed(OK, lw, mixO);
    root.quaternion.copy(o.q);
    const W = Math.pow(10, lw);
    const k = VIEW / W;
    const pitch = Math.min(1.45, Math.max(-1.45, o.e + orbit.pitch));
    camera.position.set(Math.sin(orbit.yaw) * Math.cos(pitch) * D, Math.sin(pitch) * D, Math.cos(orbit.yaw) * Math.cos(pitch) * D);
    camera.lookAt(0, 0, 0);
    camera.updateMatrixWorld();
    const uPx = renderer.getDrawingBufferSize(tmp).y / (2 * Math.tan(camera.fov * D2R / 2));
    for (const L of layers) {
      const near = lw > L.win[0] - 2.2 && lw < L.win[1] + 1.5;
      if ((near || L.eager) && !L.built && !L.building) ensure(L);
      L.alpha = fade(L.win, lw);
      if (!L.built) { L.group.visible = false; continue; }
      L.group.position.copy(L.origin).sub(focus).multiplyScalar(k);
      L.group.quaternion.copy(L.quat);
      L.group.scale.setScalar(L.unit * k);
      setOpacity(L.group, L.alpha);
      if (!L.group.visible) continue;
      L.group.updateMatrixWorld();
      if (L.impl.update) L.impl.update(t, lw, dt);
      if (L.impl.setPx) L.impl.setPx(uPx, L.unit * k);
    }
    if (terrain) terrain.update(lw, 1 / k);
    if (climber) {
      climber.group.visible = lw < 3.6;
      if (climber.group.visible) climber.update(t);
    }
    const skyA = 1 - smooth(4.9, 5.9, lw);
    sky.visible = skyA > 0.01 && summit.built;
    if (sky.visible) {
      sky.position.copy(camera.position);
      sky.scale.setScalar(D * 50);
      skyMat.uniforms.uOpacity.value = skyA;
      skyMat.uniforms.uUp.value.copy(G.up).applyQuaternion(root.quaternion);
      skyMat.uniforms.uSun.value.copy(G.sunDir).applyQuaternion(root.quaternion);
    }
    const starA = smooth(4.8, 5.8, lw) * (1 - smooth(16.6, 18.2, lw));
    setOpacity(skyStars, starA);
    return { W, k, focus };
  }

  return {
    G,
    layers,
    labelDefs,
    frame,
    ensure,
    setOverride,
    focusNow: () => focus.clone(),
    pathFocus: (lw, out) => focusAt(Math.pow(10, lw), out),
    ready: () => Promise.all([ensure(summit), ensure(earthsys)]),
    targets: {
      moon: () => G.earthPos.clone().add(moonOffset(G.days)),
      sun: () => new THREE.Vector3(),
      jupiter: () => planetPosition(PLANETS[4], G.days),
      saturn: () => planetPosition(PLANETS[5], G.days),
      m31: () => G.m31.clone(),
    },
    dispose() {
      layers.forEach((L) => L.impl && L.impl.dispose && L.impl.dispose());
      if (terrain) terrain.dispose();
      if (climber) climber.dispose();
    },
  };
}
