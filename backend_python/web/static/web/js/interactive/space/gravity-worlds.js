/**
 * Weight on other worlds, in 3D: five drop towers on five worlds, side by side. Drag any ball up or
 * down its tower to set the drop height (the same for all), then drop them together: each falls with
 * its world's g and lands at t = √(2h/g), timed in real seconds. In front of each tower the same person
 * stands on a bathroom scale: their mass never changes, their weight W = mg does, and the scale
 * (calibrated on Earth) reads W / 9.81 "kg".
 */
import { THREE } from '../core/engine.js';
import { NZ } from '../core/noise3d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { NOISE } from './cosmos/shaders.js';
import { createSpace, planeDrag } from './space3d/kit.js';

const ALL = {
  moon: { name: 'Moon', g: 1.62, ground: [0.42, 0.42, 0.43], sky: null, kind: 0 },
  mercury: { name: 'Mercury', g: 3.7, ground: [0.36, 0.33, 0.3], sky: null, kind: 0 },
  mars: { name: 'Mars', g: 3.71, ground: [0.55, 0.26, 0.13], sky: [0.75, 0.52, 0.36], kind: 1 },
  venus: { name: 'Venus', g: 8.87, ground: [0.5, 0.4, 0.22], sky: [0.85, 0.66, 0.32], kind: 1 },
  earth: { name: 'Earth', g: 9.81, ground: [0.22, 0.36, 0.14], sky: [0.42, 0.62, 0.95], kind: 2 },
  jupiter: { name: 'Jupiter', g: 24.79, ground: [0.72, 0.58, 0.42], sky: [0.7, 0.55, 0.38], kind: 3 },
  saturn: { name: 'Saturn', g: 10.44, ground: [0.8, 0.7, 0.5], sky: [0.78, 0.66, 0.45], kind: 3 },
  uranus: { name: 'Uranus', g: 8.69, ground: [0.55, 0.78, 0.82], sky: [0.5, 0.78, 0.84], kind: 3 },
  neptune: { name: 'Neptune', g: 11.15, ground: [0.24, 0.38, 0.8], sky: [0.25, 0.42, 0.9], kind: 3 },
  pluto: { name: 'Pluto', g: 0.62, ground: [0.78, 0.72, 0.64], sky: null, kind: 0 },
  sun: { name: 'Sun', g: 274, ground: [1.0, 0.62, 0.2], sky: [1.0, 0.45, 0.12], kind: 4 },
};
const SPACING = 3.1; const MPU = 0.2;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function groundMaterial() {
  return new THREE.ShaderMaterial({
    uniforms: { tNz: NZ, uC: { value: new THREE.Vector3(0.5, 0.5, 0.5) }, uKind: { value: 0 }, uTime: { value: 0 } },
    vertexShader: 'varying vec3 vP; varying vec3 vN; void main() { vP = position; vN = normal; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `${NOISE}
      uniform vec3 uC; uniform float uKind; uniform float uTime; varying vec3 vP; varying vec3 vN;
      void main() {
        vec3 p = vP * 2.0;
        float n = fbm3(p * 1.5); float f = fbm3(p * 7.0);
        vec3 c = uC * (0.75 + 0.5 * n) * (0.9 + 0.2 * f);
        if (uKind < 0.5) { vec4 cr = nz4(p * 1.2); float rim = smoothstep(0.08, 0.0, abs(cr.a - 0.32)); float bowl = smoothstep(0.32, 0.1, cr.a); c *= 1.0 - bowl * 0.35 + rim * 0.4; }
        else if (uKind < 1.5) { float rocks = smoothstep(0.72, 0.8, fbm3(p * 5.0)); c *= 1.0 - rocks * 0.45; }
        else if (uKind < 2.5) { c = mix(c, vec3(0.32, 0.27, 0.18), smoothstep(0.6, 0.75, fbm3(p * 3.0))); c *= 0.85 + 0.3 * fbm3(p * 22.0); }
        else if (uKind < 3.5) { float band = sin(vP.z * 6.0 + fbm3(p * 2.0 + vec3(uTime * 0.05)) * 6.0); c *= 0.85 + 0.2 * band; }
        else { vec4 g = nz4(p * 3.0 + vec3(0.0, uTime * 0.2, 0.0)); c = vec3(1.0, 0.55, 0.15) * (0.7 + 0.8 * smoothstep(0.0, 0.2, g.b)) * 1.6; }
        float side = 1.0 - abs(normalize(vN).y);
        c *= mix(1.0, 0.45, side);
        float lit = 0.55 + 0.45 * max(normalize(vN).y, 0.0);
        vec3 col = c * lit;
        col = 1.0 - exp(-col * 1.6);
        gl_FragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
      }`,
  });
}

function skyColumn() {
  return new THREE.Mesh(new THREE.CylinderGeometry(1.45, 1.45, 5.4, 48, 1, true), new THREE.ShaderMaterial({
    uniforms: { uC: { value: new THREE.Vector3(0.4, 0.6, 1) }, uK: { value: 1 } },
    vertexShader: 'varying vec3 vP; void main() { vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform vec3 uC; uniform float uK; varying vec3 vP; void main() { float h = (vP.y + 2.7) / 5.4; float a = (1.0 - h) * 0.55 * uK; gl_FragColor = vec4(uC * a, a); }',
    transparent: true, depthWrite: false, side: THREE.BackSide, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  }));
}

function tower(metal) {
  const g = new THREE.Group();
  const h = 20 * MPU + 0.2;
  for (const [x, z] of [[-0.16, -0.16], [0.16, -0.16], [-0.16, 0.16], [0.16, 0.16]]) {
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.014, h, 6), metal); leg.position.set(x, h / 2, z); g.add(leg);
  }
  const rung = new THREE.CylinderGeometry(0.007, 0.007, 0.32, 5);
  const n = 20;
  const inst = new THREE.InstancedMesh(rung, metal, n * 4);
  const m = new THREE.Matrix4(); const q = new THREE.Quaternion(); const e = new THREE.Euler(); let k = 0;
  for (let i = 1; i <= n; i++) {
    const y = i * MPU;
    for (const [x, z, ry] of [[0, -0.16, 0], [0, 0.16, 0], [-0.16, 0, Math.PI / 2], [0.16, 0, Math.PI / 2]]) {
      m.compose(new THREE.Vector3(x, y, z), q.setFromEuler(e.set(0, ry, Math.PI / 2)), new THREE.Vector3(1, 1, 1)); inst.setMatrixAt(k++, m);
    }
  }
  g.add(inst);
  const arm = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.025, 0.025), metal); arm.position.set(0.25, h, 0); g.add(arm);
  return g;
}

function person(skin, cloth, pants) {
  const g = new THREE.Group();
  const add = (geo, mat, x, y, z, rz = 0) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.rotation.z = rz; g.add(m); return m; };
  const leg = new THREE.CapsuleGeometry(0.036, 0.36, 4, 10);
  add(leg, pants, -0.05, 0.22, 0); add(leg, pants, 0.05, 0.22, 0);
  const torso = add(new THREE.CapsuleGeometry(0.08, 0.2, 6, 14), cloth, 0, 0.6, 0); torso.scale.z = 0.7;
  const arm = new THREE.CapsuleGeometry(0.026, 0.3, 4, 8);
  const armL = add(arm, cloth, -0.11, 0.58, 0, 0.12); const armR = add(arm, cloth, 0.11, 0.58, 0, -0.12);
  add(new THREE.CylinderGeometry(0.028, 0.03, 0.05, 10), skin, 0, 0.77, 0);
  const head = add(new THREE.SphereGeometry(0.068, 20, 14), skin, 0, 0.86, 0); head.scale.set(0.92, 1.05, 0.95);
  const shoe = new THREE.BoxGeometry(0.06, 0.03, 0.12);
  add(shoe, pants, -0.05, 0.015, 0.02); add(shoe, pants, 0.05, 0.015, 0.02);
  return { group: g, armL, armR };
}

export default function init(stage) {
  const S = createSpace(stage, { camera: [0, 2.6, 11.5], target: [0, 1.6, 0], minDistance: 3, maxDistance: 30, maxPolar: 1.62 });
  if (!S) return null;
  const { engine, scene, camera, controls, sunLight } = S;
  sunLight.position.set(4, 12, 10);
  scene.add(new THREE.HemisphereLight(0xdbe8ff, 0x2a2a30, 1.1));
  const hud = createHud(stage);
  const badge = hud.badge('Drag a ball to set the height, then drop', '#60a5fa');

  const lanes = ['moon', 'mars', 'earth', 'jupiter', 'sun'];
  let H = 10; let mass = 50; let dropping = false;
  const y = new Float64Array(5); const t = new Float64Array(5); const landed = new Uint8Array(5); const shown = new Float64Array(5);

  const metal = new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.8, roughness: 0.35 });
  const ballMat = new THREE.MeshStandardMaterial({ color: 0xe5484d, roughness: 0.3, metalness: 0.1 });
  const skin = new THREE.MeshStandardMaterial({ color: 0xc58c6a, roughness: 0.7 });
  const cloth = new THREE.MeshStandardMaterial({ color: 0x3b5bdb, roughness: 0.8 });
  const pants = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.85 });
  const scaleMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.4 });
  const L = lanes.map((key, i) => {
    const g = new THREE.Group(); g.position.x = (i - 2) * SPACING; scene.add(g);
    const gm = groundMaterial();
    const plat = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.25, 0.3, 64), gm); plat.position.y = -0.15; g.add(plat);
    const sky = skyColumn(); sky.position.y = 2.7; g.add(sky);
    const tw = tower(metal); tw.position.set(-0.55, 0, -0.3); g.add(tw);
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.1, 24, 16), ballMat); g.add(ball);
    const shadow = new THREE.Mesh(new THREE.CircleGeometry(0.16, 32), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.4, depthWrite: false }));
    shadow.rotation.x = -Math.PI / 2; shadow.position.set(-0.05, 0.004, -0.3); g.add(shadow);
    const mark = new THREE.Mesh(new THREE.RingGeometry(0.2, 0.23, 40), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.5, side: THREE.DoubleSide, depthWrite: false }));
    mark.rotation.x = -Math.PI / 2; g.add(mark);
    const p = person(skin, cloth, pants); p.group.position.set(0.55, 0.06, 0.55); g.add(p.group);
    const sc = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.05, 0.3), scaleMat); sc.position.set(0.55, 0.025, 0.55); g.add(sc);
    const nameEl = document.createElement('div'); const timeEl = document.createElement('div'); const scaleEl = document.createElement('div');
    nameEl.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;text-align:center;font:700 12px Poppins,system-ui,sans-serif;color:#e8eefb;white-space:nowrap;text-shadow:0 1px 3px #000;z-index:2';
    timeEl.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;font:700 11px Poppins,system-ui,sans-serif;padding:2px 8px;border-radius:999px;background:rgba(8,14,30,0.8);color:#e8eefb;white-space:nowrap;z-index:2';
    scaleEl.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;font:700 10px ui-monospace,Menlo,monospace;padding:2px 6px;border-radius:5px;background:#0f172a;color:#86efac;white-space:nowrap;z-index:2';
    stage.append(nameEl, timeEl, scaleEl);
    return { g, gm, sky, ball, shadow, mark, p, nameEl, timeEl, scaleEl };
  });
  function setLane(i, key) {
    const W = ALL[key]; const l = L[i];
    l.gm.uniforms.uC.value.set(...W.ground); l.gm.uniforms.uKind.value = W.kind;
    l.sky.visible = !!W.sky; if (W.sky) l.sky.material.uniforms.uC.value.set(...W.sky);
    l.nameEl.innerHTML = `${W.name}<br><span style="font-weight:600;font-size:10px;color:#aab8d3">g = ${W.g} m/s²</span>`;
  }
  lanes.forEach((key, i) => setLane(i, key));

  const panel = createPanel(stage, { title: 'Weight on other worlds' });
  panel.chips({ label: 'Fifth tower', options: ['sun', 'mercury', 'venus', 'saturn', 'uranus', 'neptune', 'pluto'].map((key) => ({ value: key, label: ALL[key].name })), value: 'sun', onChange: (key) => { lanes[4] = key; setLane(4, key); reset(); } });
  panel.slider({ label: 'Your mass', min: 10, max: 120, step: 1, value: mass, format: (m) => `${m} kg`, onChange: (m) => { mass = m; } });
  panel.buttonRow([{ label: 'Drop all', icon: 'south', onClick: drop }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset }]);
  const st = panel.stats(lanes.map((key, i) => ({ key: 'l' + i, label: i === 4 ? 'Fifth tower' : ALL[key].name })));
  panel.info('Mass is how much stuff you are made of: the same everywhere. Weight is the pull of gravity on that mass, W = mg, in newtons. A smaller g means a slower fall: t = √(2h/g).');

  function reset() { dropping = false; for (let i = 0; i < 5; i++) { y[i] = H; t[i] = 0; landed[i] = 0; } }
  function drop() { reset(); dropping = true; }

  const drag = planeDrag(engine.canvas, camera, controls, {
    plane: new THREE.Plane(new THREE.Vector3(0, 0, 1), 0.3),
    handles: () => L.map((l, i) => ({ i, pos: l.ball.getWorldPosition(new THREE.Vector3()) })),
    onMove: (h, p) => { H = Math.min(20, Math.max(1, Math.round(p.y / MPU))); reset(); },
    onUp: () => drop(),
  });

  const v3 = new THREE.Vector3();
  function place(el, obj, x, yy, z, dy) {
    v3.set(x, yy, z); obj.localToWorld(v3); v3.project(camera);
    const w = stage.clientWidth; const h = stage.clientHeight;
    const vis = v3.z < 1 && Math.abs(v3.x) < 1.15 && Math.abs(v3.y) < 1.15;
    el.style.opacity = vis ? '1' : '0';
    if (vis) el.style.transform = `translate(${((v3.x + 1) / 2 * w).toFixed(1)}px, ${((1 - v3.y) / 2 * h + dy).toFixed(1)}px) translate(-50%, -50%)`;
  }

  engine.onResize((w, h) => {
    const vf = camera.fov * Math.PI / 180; const hf = 2 * Math.atan(Math.tan(vf / 2) * (w / h));
    controls.setDistance(Math.max(9, (2 * SPACING + 1.6) / Math.tan(hf / 2) * 1.04));
  });
  reset();
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    if (dropping) {
      for (let i = 0; i < 5; i++) {
        if (landed[i]) continue;
        const g = ALL[lanes[i]].g;
        t[i] += dt; y[i] = H - 0.5 * g * t[i] * t[i];
        if (y[i] <= 0) { t[i] = Math.sqrt(2 * H / g); y[i] = 0; landed[i] = 1; }
      }
      if (landed.every((l) => l)) dropping = false;
    }
    for (let i = 0; i < 5; i++) {
      const W = ALL[lanes[i]]; const l = L[i];
      l.gm.uniforms.uTime.value = time;
      l.ball.position.set(-0.05, 0.1 + y[i] * MPU, -0.3);
      l.shadow.scale.setScalar(0.6 + 0.4 * (1 - y[i] / 20)); l.shadow.material.opacity = 0.45 * (1 - y[i] / 26);
      l.mark.position.set(-0.05, 0.1 + H * MPU, -0.3);
      const sq = Math.min(2, Math.max(0.4, W.g / 9.81));
      const crouch = Math.min(1, Math.max(0, (sq - 1.2) / 0.8));
      l.p.group.scale.set(1 + crouch * 0.12, 1 - crouch * 0.22, 1 + crouch * 0.12);
      l.p.armL.rotation.z = 0.12 - crouch * 0.1; l.p.armR.rotation.z = -0.12 + crouch * 0.1;
      const Wn = mass * W.g; const read = Wn / 9.81;
      shown[i] += (read - shown[i]) * (1 - Math.exp(-dt * 6));
      l.scaleEl.textContent = `${shown[i] > 999 ? 'ERR' : fmt(shown[i], 0) + ' kg'} · ${fmt(Wn, 0)} N`;
      l.timeEl.textContent = `${fmt(t[i], 2)} s`;
      l.timeEl.style.color = landed[i] ? '#86efac' : '#e8eefb';
      place(l.nameEl, l.g, 0, -0.3, 1.3, 20);
      place(l.scaleEl, l.g, 0.55, 0.05, 0.75, 14);
      place(l.timeEl, l.g, -0.05, 0.1 + y[i] * MPU, -0.3, -24);
      l.timeEl.style.display = dropping || landed[i] ? '' : 'none';
      st['l' + i].set(`${fmt(Math.sqrt(2 * H / W.g), 2)} s · ${fmt(Wn, 0)} N`);
    }
    badge.set(dropping ? 'Falling…' : landed[0] ? `Same ${H} m drop: ${fmt(t[4], 2)} s on ${ALL[lanes[4]].name}, ${fmt(t[0], 2)} s on the Moon` : `Drop height ${H} m: drag a ball to change it`);
  });
  engine.start();

  stage.__worlds = { drop, setH: (h) => { H = h; reset(); }, times: () => Array.from(t) };
  return {
    dispose() {
      drag.dispose(); controls.dispose(); panel.dispose(); hud.dispose();
      L.forEach((l) => { l.nameEl.remove(); l.timeEl.remove(); l.scaleEl.remove(); });
      engine.dispose();
    },
  };
}
