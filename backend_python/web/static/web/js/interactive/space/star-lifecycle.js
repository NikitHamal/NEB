// Life cycle of stars in 3D. Choose a starting mass and scrub through the star's life: the birth cloud
// collapsing around a protostar with its disc and jets, the main-sequence star with its granulation and
// corona, the red giant boiling in a few huge cells, the planetary nebula and white dwarf, or the
// supernova, its remnant and the pulsar or black hole it leaves. Temperatures, luminosities and
// lifetimes come from the mass (stars3d/model.js); the HR diagram traces the path.
import { THREE, createEngine, createOrbitControls } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createMilkySky } from './cosmos/milky.js';
import { createSkyBackground } from './cosmos/stars.js';
import { stages, at, fmt } from './stars3d/model.js';
import { createStar } from './stars3d/star.js';
import { createNebula } from './stars3d/nebula.js';
import { createPulsar, createBlackHole, glow } from './stars3d/compact.js';
import { createHR } from './stars3d/hr.js';

const L10 = Math.log10;

function jets() {
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 }, uK: { value: 1 } },
    vertexShader: 'varying vec3 vP; void main() { vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform float uTime; uniform float uK; varying vec3 vP;
      void main() { float y = abs(vP.y) / 9.0; float rad = length(vP.xz) / (0.08 + abs(vP.y) * 0.07);
        float knots = 0.65 + 0.35 * sin(abs(vP.y) * 3.0 - uTime * 6.0);
        float a = pow(1.0 - clamp(y, 0.0, 1.0), 1.4) * exp(-rad * rad * 2.5) * knots * uK;
        gl_FragColor = vec4(vec3(1.0, 0.55, 0.35) * a, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  });
  const g = new THREE.CylinderGeometry(0.8, 0.05, 9, 24, 6, true); g.translate(0, 4.5, 0);
  const a = new THREE.Mesh(g, mat); const b = new THREE.Mesh(g, mat); b.rotation.z = Math.PI;
  const disk = new THREE.Mesh(new THREE.RingGeometry(1.2, 4.2, 96, 1), new THREE.ShaderMaterial({
    uniforms: { uTime: mat.uniforms.uTime, uK: mat.uniforms.uK },
    vertexShader: 'varying vec2 vQ; void main() { vQ = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform float uTime; uniform float uK; varying vec2 vQ;
      void main() { float r = length(vQ); float an = atan(vQ.y, vQ.x);
        float sw = an - uTime * 0.9 / (r * sqrt(r));
        float s = 0.55 + 0.22 * sin(sw * 7.0 + sin(r * 3.1) * 2.0) + 0.18 * sin(sw * 17.0 - r * 5.3) + 0.1 * sin(sw * 31.0 + r * 11.0);
        float a = smoothstep(4.2, 2.0, r) * smoothstep(1.2, 1.6, r) * s * uK;
        vec3 c = mix(vec3(1.0, 0.7, 0.4), vec3(0.45, 0.2, 0.15), smoothstep(1.4, 3.6, r));
        gl_FragColor = vec4(c * a * 0.7, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  }));
  disk.rotation.x = -Math.PI / 2;
  const group = new THREE.Group();
  group.add(a, b, disk);
  group.rotation.z = 0.25; group.rotation.x = 0.2;
  [a, b, disk].forEach((m) => { m.renderOrder = 7; });
  return { group, mat };
}

export default function init(stage) {
  stage.classList.add('ix-cosmos-stage');
  const engine = createEngine(stage, { noise: true, alpha: false, environment: false, fov: 40, near: 0.01, far: 2e5, exposure: 1 });
  if (!engine) return null;
  const { scene, camera, renderer, quality } = engine;
  scene.background = new THREE.Color(0x000000);
  renderer.setClearColor(0x000000, 1);
  camera.position.set(0, 2.5, 12);
  const controls = createOrbitControls(camera, engine.canvas, { target: new THREE.Vector3(), minDistance: 0.4, maxDistance: 160, damping: 0.08 });
  controls.setAutoRotate(0.04);

  const sky = new THREE.Group();
  sky.add(createMilkySky(quality), createSkyBackground(quality));
  scene.add(sky);

  const star = createStar(quality);
  const nebula = createNebula(quality, renderer);
  const pulsar = createPulsar();
  const hole = createBlackHole(renderer, sky, quality);
  const proto = jets();
  const flash = glow(0xe8f0ff, 40, 0);
  scene.add(star.group, nebula.mesh, nebula.comp, pulsar.group, hole.group, proto.group, flash);

  const hud = createHud(stage);
  const badge = hud.badge('Drag the timeline, or press Play', '#60a5fa');
  let M = 1; let S = stages(M); let s = 0.3; let playing = false;
  const O = {};

  const panel = createPanel(stage, { title: 'Life of a star' });
  const mS = panel.slider({ label: 'Starting mass', min: -1, max: 1.6, step: 0.01, value: 0, format: (v) => `${fmt(Math.pow(10, v), Math.pow(10, v) < 2 ? 2 : 1)} M☉`, onChange: (v) => { M = Math.pow(10, v); S = stages(M); stageKey = ''; } });
  panel.chips({ label: 'Examples', options: [{ value: '0.2', label: 'Red dwarf' }, { value: '1', label: 'The Sun' }, { value: '5', label: '5 Suns' }, { value: '15', label: '15 Suns' }, { value: '40', label: '40 Suns' }], value: '1', onChange: (v) => { M = +v; mS.set(L10(M)); S = stages(M); stageKey = ''; } });
  const [playB] = panel.buttonRow([{ label: 'Play the life', icon: 'play_arrow', onClick: () => { playing = !playing; if (playing && s > 0.995) s = 0; playB.setLabel(playing ? 'Pause' : 'Play the life'); } }]);
  const hr = createHR(panel.body);
  const st = panel.stats([{ key: 'stage', label: 'Stage' }, { key: 'dur', label: 'Lasts' }, { key: 'T', label: 'Surface temperature' }, { key: 'L', label: 'Luminosity' }, { key: 'R', label: 'Radius' }, { key: 'M', label: 'Mass' }]);
  const info = panel.info('');

  // the timeline across the bottom of the stage
  const tl = document.createElement('div');
  tl.style.cssText = 'position:absolute;left:16px;right:16px;bottom:14px;height:44px;z-index:3;touch-action:none;user-select:none;cursor:ew-resize';
  const track = document.createElement('div');
  track.style.cssText = 'position:absolute;left:0;right:0;top:4px;height:14px;display:flex;gap:3px';
  const labelsRow = document.createElement('div');
  labelsRow.style.cssText = 'position:absolute;left:0;right:0;top:22px;height:16px;display:flex;gap:3px;font:600 10px Poppins,system-ui,sans-serif;color:#8ea0c2';
  const knob = document.createElement('div');
  knob.style.cssText = 'position:absolute;top:0;width:22px;height:22px;margin-left:-11px;border-radius:50%;background:#60a5fa;box-shadow:0 0 0 4px rgba(96,165,250,0.25),0 2px 8px rgba(0,0,0,0.5)';
  tl.append(track, labelsRow, knob);
  stage.appendChild(tl);
  let tlKey = '';
  function buildTimeline() {
    const k = S.map((x) => x.key).join();
    if (k === tlKey) return;
    tlKey = k;
    track.innerHTML = ''; labelsRow.innerHTML = '';
    S.forEach((x) => {
      const seg = document.createElement('div');
      seg.style.cssText = `flex:${x.w};border-radius:7px;background:rgba(160,190,255,0.16);transition:background .2s`;
      seg.dataset.key = x.key; track.appendChild(seg);
      const lab = document.createElement('div');
      lab.style.cssText = `flex:${x.w};text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis`;
      lab.textContent = x.name.replace(' (far future)', ''); labelsRow.appendChild(lab);
    });
  }
  function setFromX(clientX) {
    const r = tl.getBoundingClientRect();
    s = Math.min(1, Math.max(0, (clientX - r.left) / r.width));
    playing = false; playB.setLabel('Play the life');
  }
  let dragging = false;
  tl.addEventListener('pointerdown', (e) => { dragging = true; tl.setPointerCapture(e.pointerId); setFromX(e.clientX); e.stopPropagation(); });
  tl.addEventListener('pointermove', (e) => { if (dragging) setFromX(e.clientX); });
  tl.addEventListener('pointerup', () => { dragging = false; });
  tl.addEventListener('pointercancel', () => { dragging = false; });

  let stageKey = '';
  let goalDist = 12;
  let elapsed = 0;
  function frameStage(c) {
    const disp = Math.min(6, Math.max(0.05, 0.6 * Math.pow(c.R, 0.3)));
    const d = { nebula: 30, proto: 16, ms: 7, giant: Math.max(12, disp * 5.2), pneb: 18, wd: 9, sn: 26, ns: 12, bh: 22 }[c.key] || 12;
    goalDist = d;
    controls.setDistance(d);
  }

  engine.setUpdate((dt, t) => {
    elapsed = t;
    if (playing) { s += dt / 40; if (s >= 1) { s = 1; playing = false; playB.setLabel('Play the life'); } }
    buildTimeline();
    at(S, s, O);
    const c = O.c; const f = O.f;
    if (c.key + M !== stageKey) { stageKey = c.key + M; frameStage(c); }
    controls.update(dt);

    const k = c.key;
    const disp = Math.min(6, Math.max(0.05, 0.6 * Math.pow(O.R, 0.3)));
    const showStar = k === 'proto' || k === 'ms' || k === 'giant' || k === 'pneb' || k === 'wd' || (k === 'sn' && f < 0.03);
    star.group.visible = showStar;
    star.uniforms.uTime.value = t;
    if (showStar) {
      const T = k === 'pneb' ? 30000 : k === 'proto' ? 3200 + 1200 * f : O.T;
      star.uniforms.uT.value = T;
      star.uniforms.uGiant.value = k === 'giant' ? 1 : 0;
      star.uniforms.uCells.value = k === 'giant' ? 3.2 : k === 'proto' ? 14 : 70;
      star.uniforms.uSpots.value = k === 'ms' && T > 4200 && T < 6800 ? 0.6 : 0;
      star.uniforms.uBright.value = k === 'proto' ? 0.7 + 0.5 * f : 1;
      star.haloUniforms.uCorona.value = k === 'ms' ? 1 : 0.2;
      star.haloUniforms.uGlow.value = k === 'pneb' || k === 'wd' ? 2.2 : k === 'giant' ? 0.6 : 1;
      const r = k === 'pneb' ? 0.1 : k === 'wd' ? 0.14 : k === 'sn' ? disp * (1 + f * 40) : disp;
      star.group.scale.setScalar(r);
    }

    nebula.mesh.visible = k === 'nebula' || k === 'proto' || k === 'pneb' || k === 'wd' || k === 'sn' || k === 'ns';
    const NU = nebula.uniforms; NU.uTime.value = t;
    if (k === 'nebula') { NU.uMode.value = 0; NU.uExpand.value = f; NU.uSourceK.value = 0.04 + f * 0.25; NU.uFade.value = 1; nebula.mesh.scale.setScalar(11); }
    else if (k === 'proto') { NU.uMode.value = 0; NU.uExpand.value = 1; NU.uSourceK.value = 0.3 + f * 0.5; NU.uFade.value = 1 - f * 0.75; nebula.mesh.scale.setScalar(8 - 3 * f); }
    else if (k === 'pneb') { NU.uMode.value = 1; NU.uExpand.value = 0.15 + 0.85 * f; NU.uFade.value = 1; nebula.mesh.scale.setScalar(7); }
    else if (k === 'wd') { NU.uMode.value = 1; NU.uExpand.value = 1; NU.uFade.value = M >= 0.5 ? Math.max(0, 0.6 - f) : 0; nebula.mesh.scale.setScalar(7 + f * 3); nebula.mesh.visible = M >= 0.5 && f < 0.6; }
    else if (k === 'sn') { NU.uMode.value = 2; NU.uExpand.value = 0.25 + 0.75 * f; NU.uFade.value = 1; nebula.mesh.scale.setScalar(1.5 + 8.5 * Math.pow(f, 0.6)); }
    else if (k === 'ns') { NU.uMode.value = 2; NU.uExpand.value = 1; NU.uFade.value = 0.28 * (1 - f * 0.5); nebula.mesh.scale.setScalar(6.5); }

    proto.group.visible = k === 'proto';
    proto.mat.uniforms.uTime.value = t; proto.mat.uniforms.uK.value = Math.min(1, f * 3);
    proto.group.scale.setScalar(Math.max(0.6, disp * 1.4));

    flash.visible = k === 'sn' && f < 0.35;
    flash.material.uniforms.uK.value = k === 'sn' ? Math.max(0, 1.6 * Math.exp(-f * 9) - 0.02) : 0;
    flash.scale.setScalar(1 + f * 6);

    pulsar.group.visible = k === 'ns';
    if (k === 'ns') { pulsar.update(dt, t); pulsar.group.scale.setScalar(0.18); }
    hole.group.visible = k === 'bh';
    if (k === 'bh') { hole.capture(scene); hole.update(dt, t); hole.group.scale.setScalar(0.55); }

    nebula.render(scene, camera);
    hr.draw(S, s, O);
    [...track.children].forEach((el) => { el.style.background = el.dataset.key === k ? 'rgba(96,165,250,0.6)' : 'rgba(160,190,255,0.16)'; });
    knob.style.left = `${(s * 100).toFixed(2)}%`;
    st.stage.set(c.name);
    st.dur.set(c.dur);
    st.T.set(k === 'bh' ? '—' : k === 'nebula' ? '≈ 10–30 K' : `${fmt(O.T, 0)} K`);
    st.L.set(O.L > 0 && k !== 'bh' ? (O.L >= 100 ? `${fmt(O.L, 0)} L☉` : `${fmt(O.L, 3)} L☉`) : '0 (no light escapes)');
    st.R.set(k === 'nebula' ? 'light-years' : O.R >= 1 ? `${fmt(O.R, O.R < 10 ? 1 : 0)} R☉` : O.R > 1e-3 ? `${fmt(O.R * 109, 1)} Earths` : `${fmt(O.R * 696000, 0)} km`);
    st.M.set(`${fmt(k === 'wd' ? Math.min(1.35, 0.5 + M * 0.08) : k === 'ns' ? 1.4 : k === 'bh' ? M * 0.3 : M, 2)} M☉`);
    info.set(c.info);
    badge.set(`${fmt(M, M < 2 ? 2 : 1)} M☉ star · ${c.name}`);
  });
  engine.start();

  stage.__stars = { set: (v) => { s = v; }, mass: (m) => { M = m; S = stages(M); stageKey = ''; }, get key() { return O.c && O.c.key; }, get t() { return elapsed; } };
  return {
    dispose() {
      controls.dispose(); panel.dispose(); hud.dispose(); tl.remove();
      star.dispose(); nebula.dispose(); pulsar.dispose(); hole.dispose();
      engine.dispose();
    },
  };
}
