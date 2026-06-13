import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const STRING_LEN = 8;
const STRING_SEGS = 120;

export default function init(stage, opts) {
  const engine = createEngine(stage, {});
  if (!engine) return null;
  const { scene, camera, quality } = engine;

  camera.position.set(0, 2, 10);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 2, maxDistance: 24,
    target: new THREE.Vector3(0, 0, 0),
  });
  controls.setTarget(new THREE.Vector3(0, 0, 0));

  basicLights(scene, { ambient: 0.6, key: 1.2 });
  scene.background = new THREE.Color(0x0b1c30);

  // Axis line
  const axisGeo = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(-STRING_LEN / 2, 0, 0),
    new THREE.Vector3(STRING_LEN / 2, 0, 0),
  ]);
  scene.add(new THREE.Line(axisGeo, new THREE.LineBasicMaterial({ color: 0x2a4060, transparent: true, opacity: 0.6 })));

  // End posts
  [-1, 1].forEach((side) => {
    const post = new THREE.Mesh(
      new THREE.CylinderGeometry(0.04, 0.04, 3, 8),
      new THREE.MeshStandardMaterial({ color: 0x5d779e, metalness: 0.5, roughness: 0.5 })
    );
    post.position.set(side * STRING_LEN / 2, 0, 0);
    scene.add(post);
  });

  // Main wave string
  const stringPositions = new Float32Array((STRING_SEGS + 1) * 3);
  const stringGeo = new THREE.BufferGeometry();
  stringGeo.setAttribute('position', new THREE.BufferAttribute(stringPositions, 3));
  stringGeo.setDrawRange(0, STRING_SEGS + 1);
  const stringMat = new THREE.LineBasicMaterial({ color: 0xF59E0B, linewidth: 2 });
  const stringLine = new THREE.Line(stringGeo, stringMat);
  scene.add(stringLine);

  // Wave 2 line (interference mode)
  const str2Positions = new Float32Array((STRING_SEGS + 1) * 3);
  const str2Geo = new THREE.BufferGeometry();
  str2Geo.setAttribute('position', new THREE.BufferAttribute(str2Positions, 3));
  str2Geo.setDrawRange(0, STRING_SEGS + 1);
  const str2Line = new THREE.Line(str2Geo, new THREE.LineBasicMaterial({ color: 0xf472b6, transparent: true, opacity: 0.55 }));
  str2Line.visible = false;
  scene.add(str2Line);

  // Resultant sum line
  const sumPositions = new Float32Array((STRING_SEGS + 1) * 3);
  const sumGeo = new THREE.BufferGeometry();
  sumGeo.setAttribute('position', new THREE.BufferAttribute(sumPositions, 3));
  sumGeo.setDrawRange(0, STRING_SEGS + 1);
  const sumLine = new THREE.Line(sumGeo, new THREE.LineBasicMaterial({ color: 0xF59E0B, linewidth: 2.5 }));
  sumLine.visible = false;
  scene.add(sumLine);

  // Node dots for standing wave
  const nodeDots = [];
  for (let i = 0; i <= 20; i++) {
    const dot = new THREE.Mesh(
      new THREE.SphereGeometry(0.06, 8, 8),
      new THREE.MeshStandardMaterial({ color: 0x7dd3fc, emissive: 0x2060a0, emissiveIntensity: 0.4 })
    );
    dot.visible = false;
    scene.add(dot);
    nodeDots.push(dot);
  }

  // Labels
  const lambdaSprite = makeLabelSprite('λ = —', { scale: 1.1, fontSize: 34 });
  lambdaSprite.position.set(0, 2.2, 0);
  scene.add(lambdaSprite);

  // Wavelength bracket (two small lines)
  const bracketGeo = new THREE.BufferGeometry();
  bracketGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(12), 3));
  const bracketLine = new THREE.LineSegments(bracketGeo, new THREE.LineBasicMaterial({ color: 0x8be9a8, transparent: true, opacity: 0.8 }));
  scene.add(bracketLine);

  // State
  let mode = 'travelling';
  let freq = 0.6;
  let amp = 0.8;
  let waveSpeed = 2.4;
  let freq2 = 0.8;
  let amp2 = 0.8;
  let showComponents = true;
  let t = 0;

  function y1(x, time) {
    const k = (2 * Math.PI * freq) / waveSpeed;
    const w = 2 * Math.PI * freq;
    return amp * Math.sin(k * x - w * time);
  }
  function y2(x, time) {
    const k = (2 * Math.PI * freq2) / waveSpeed;
    const w = 2 * Math.PI * freq2;
    return amp2 * Math.sin(k * x - w * time);
  }
  function yStanding(x, time) {
    const k = (2 * Math.PI * freq) / waveSpeed;
    const w = 2 * Math.PI * freq;
    return 2 * amp * Math.sin(k * x) * Math.cos(w * time);
  }

  function updateLambdaLabel(lambda) {
    const txt = `λ = ${lambda.toFixed(2)} m`;
    const ns = makeLabelSprite(txt, { scale: 1.1, fontSize: 34 });
    lambdaSprite.material.map.dispose();
    lambdaSprite.material = ns.material;
    lambdaSprite.scale.copy(ns.scale);
    scene.remove(ns);
  }

  let freqSlider;

  const panel = createPanel(stage, { title: 'Waves 3D' });
  panel.select({
    label: 'Mode',
    options: [
      { value: 'travelling', label: 'Travelling wave' },
      { value: 'standing', label: 'Standing wave' },
      { value: 'interference', label: 'Interference (two waves)' },
    ],
    value: mode,
    onChange: (v) => {
      mode = v;
      modeBadge.set(v === 'travelling' ? 'Travelling wave' : v === 'standing' ? 'Standing wave' : 'Superposition');
      wave2Rows.forEach((r) => { r.el.style.display = v === 'interference' ? '' : 'none'; });
      if (mode === 'standing') snapToHarmonic();
    },
  });
  freqSlider = panel.slider({
    label: 'Frequency f', min: 0.2, max: 1.6, step: 0.05, value: freq,
    format: (v) => `${v.toFixed(2)} Hz`,
    onChange: (v) => { freq = v; if (mode === 'standing') snapToHarmonic(); },
  });
  panel.slider({
    label: 'Amplitude A', min: 0.1, max: 1.2, step: 0.05, value: amp,
    format: (v) => `${v.toFixed(2)} m`, onChange: (v) => { amp = v; },
  });
  panel.slider({
    label: 'Wave speed v', min: 0.8, max: 5, step: 0.1, value: waveSpeed,
    format: (v) => `${v.toFixed(1)} m/s`,
    onChange: (v) => { waveSpeed = v; if (mode === 'standing') snapToHarmonic(); },
  });
  const f2Row = panel.slider({
    label: 'Wave 2 frequency', min: 0.2, max: 1.6, step: 0.05, value: freq2,
    format: (v) => `${v.toFixed(2)} Hz`, onChange: (v) => { freq2 = v; },
  });
  const a2Row = panel.slider({
    label: 'Wave 2 amplitude', min: 0.1, max: 1.2, step: 0.05, value: amp2,
    format: (v) => `${v.toFixed(2)} m`, onChange: (v) => { amp2 = v; },
  });
  const compRow = panel.toggle({
    label: 'Show components', value: true, onChange: (v) => { showComponents = v; },
  });
  const wave2Rows = [f2Row, a2Row, compRow];
  wave2Rows.forEach((r) => { r.el.style.display = 'none'; });
  panel.divider();
  const lambdaOut = panel.readout({ label: 'Wavelength λ = v/f', value: '—' });
  const periodOut = panel.readout({ label: 'Period T = 1/f', value: '—' });
  panel.info('Orbit to see the 3D wave. In standing mode, blue dots mark the nodes (never move). In interference mode watch constructive/destructive superposition.');

  const hud = createHud(stage);
  const modeBadge = hud.badge('Travelling wave', '#F59E0B');

  function snapToHarmonic() {
    const fundamental = waveSpeed / (2 * STRING_LEN);
    const n = Math.max(1, Math.min(Math.round(freq / fundamental), Math.floor(1.6 / fundamental)));
    freq = n * fundamental;
    freqSlider.set(freq);
  }

  engine.setUpdate((dt) => {
    controls.update(dt);
    t += dt;

    const lambda = waveSpeed / freq;

    // Update string points
    for (let i = 0; i <= STRING_SEGS; i++) {
      const xWorld = (i / STRING_SEGS) * STRING_LEN - STRING_LEN / 2;
      const xParam = i / STRING_SEGS * STRING_LEN;
      let yVal = 0;

      if (mode === 'travelling') {
        yVal = y1(xParam, t);
        stringMat.color.set(0xF59E0B);
      } else if (mode === 'standing') {
        yVal = yStanding(xParam, t);
      } else {
        // interference: wave 1 on string, sum on sumLine
        yVal = y1(xParam, t);
        const y2Val = y2(xParam, t);
        str2Positions[i * 3] = xWorld;
        str2Positions[i * 3 + 1] = y2Val;
        str2Positions[i * 3 + 2] = 0;
        sumPositions[i * 3] = xWorld;
        sumPositions[i * 3 + 1] = yVal + y2Val;
        sumPositions[i * 3 + 2] = 0;
      }
      stringPositions[i * 3] = xWorld;
      stringPositions[i * 3 + 1] = yVal;
      stringPositions[i * 3 + 2] = 0;
    }

    stringGeo.attributes.position.needsUpdate = true;

    // Manage line visibility
    str2Line.visible = mode === 'interference' && showComponents;
    sumLine.visible = mode === 'interference';
    if (mode === 'interference') {
      str2Geo.attributes.position.needsUpdate = true;
      sumGeo.attributes.position.needsUpdate = true;
    }

    // Node dots for standing wave
    if (mode === 'standing') {
      const halfL = lambda / 2;
      let dotIdx = 0;
      for (let x = 0; x <= STRING_LEN + 0.001; x += halfL) {
        if (dotIdx < nodeDots.length) {
          nodeDots[dotIdx].position.set(x - STRING_LEN / 2, 0, 0);
          nodeDots[dotIdx].visible = true;
          dotIdx++;
        }
      }
      for (let i = dotIdx; i < nodeDots.length; i++) nodeDots[i].visible = false;
    } else {
      nodeDots.forEach((d) => { d.visible = false; });
    }

    updateLambdaLabel(lambda);
    lambdaOut.set(`${lambda.toFixed(2)} m`);
    periodOut.set(`${(1 / freq).toFixed(2)} s`);
  });

  engine.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
