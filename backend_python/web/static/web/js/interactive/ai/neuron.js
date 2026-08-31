import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite, makeSignalPoints } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

// A single neuron, built from real geometry rather than hairlines: dendrites and the axon are
// tubes whose radius tracks the synaptic weight (WebGL ignores LineBasicMaterial.linewidth,
// so the previous version could not show weight at all), the axon carries myelin sheath
// segments with nodes of Ranvier, and it terminates in synaptic buttons.
export default function init(stage) {
  const engine = createEngine(stage, { shadows: true, environment: true, exposure: 1.05 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(12, Math.round(quality.segments / 2));
  const tubeRadial = quality.tier === 'low' ? 6 : 10;

  camera.position.set(0, 1.5, 11);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 20, enablePan: false, maxPolar: Math.PI * 0.7, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 0.5, 0));

  scene.background = new THREE.Color(0x0a0e1a);
  scene.fog = new THREE.Fog(0x0a0e1a, 16, 34);
  basicLights(scene, { ambient: 0.34, key: 1.45, fill: 0.4, rim: 0.45, rimPos: [-5, 4, -8] });

  const inputs = [
    { val: 0.6, weight: 0.8, color: 0x60a5fa },
    { val: 0.4, weight: -0.5, color: 0xf472b6 },
    { val: 0.8, weight: 0.6, color: 0x34d399 },
  ];
  let bias = 0.0;
  let outValue = 0;
  let weightedSum = 0;

  const SOMA_R = 1.0;
  const somaMat = new THREE.MeshStandardMaterial({
    color: 0x6366f1, emissive: 0x4338ca, emissiveIntensity: 0.3, roughness: 0.38, metalness: 0.1,
  });
  const soma = new THREE.Mesh(new THREE.SphereGeometry(SOMA_R, seg, Math.max(10, seg >> 1)), somaMat);
  soma.castShadow = quality.shadows;
  scene.add(soma);

  // Nucleus: visible inside the soma through the translucent membrane.
  const nucleus = new THREE.Mesh(
    new THREE.SphereGeometry(SOMA_R * 0.34, seg, Math.max(8, seg >> 1)),
    new THREE.MeshStandardMaterial({ color: 0x1e1b4b, emissive: 0x312e81, emissiveIntensity: 0.35, roughness: 0.5 })
  );
  scene.add(nucleus);
  somaMat.transparent = true;
  somaMat.opacity = 0.86;

  const outMat = new THREE.MeshStandardMaterial({
    color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.2, roughness: 0.36, metalness: 0.12,
  });
  const outNode = new THREE.Mesh(new THREE.SphereGeometry(0.45, seg, Math.max(10, seg >> 1)), outMat);
  outNode.position.set(4, 0, 0);
  outNode.castShadow = quality.shadows;
  scene.add(outNode);

  const inputNodes = [];
  const dendriteMeshes = [];
  const dendriteMat = [];
  const dendriteSamples = [];
  const weightLabels = [];

  const SAMPLE_COUNT = 48;

  function sampleCurve(curve) {
    const arr = new Float32Array((SAMPLE_COUNT + 1) * 3);
    const p = new THREE.Vector3();
    for (let i = 0; i <= SAMPLE_COUNT; i++) {
      curve.getPointAt(i / SAMPLE_COUNT, p);
      arr[i * 3] = p.x; arr[i * 3 + 1] = p.y; arr[i * 3 + 2] = p.z;
    }
    return arr;
  }

  inputs.forEach((inp, i) => {
    const y = 2.2 - i * 2.2;
    const mat = new THREE.MeshStandardMaterial({
      color: inp.color, emissive: inp.color, emissiveIntensity: inp.val * 0.8, roughness: 0.38, metalness: 0.1,
    });
    const node = new THREE.Mesh(new THREE.SphereGeometry(0.35, seg, Math.max(10, seg >> 1)), mat);
    node.position.set(-4.5, y, 0);
    node.castShadow = quality.shadows;
    scene.add(node);

    const dMat = new THREE.MeshStandardMaterial({
      color: inp.weight >= 0 ? 0x60a5fa : 0xf87171,
      emissive: inp.weight >= 0 ? 0x1d4ed8 : 0x991b1b,
      emissiveIntensity: 0.35, roughness: 0.42, metalness: 0.1,
    });
    const mesh = new THREE.Mesh(new THREE.BufferGeometry(), dMat);
    scene.add(mesh);

    inputNodes.push({ node, mat, inp, y });
    dendriteMeshes.push(mesh);
    dendriteMat.push(dMat);

    weightLabels.push({ sprite: null, y });
  });

  // Axon: soma -> terminal, with myelin sheath segments and a branching terminal.
  const axonMat = new THREE.MeshStandardMaterial({
    color: 0xfde68a, emissive: 0xb45309, emissiveIntensity: 0.25, roughness: 0.4, metalness: 0.1,
  });
  const sheathMat = new THREE.MeshStandardMaterial({
    color: 0xe7e5e4, roughness: 0.55, metalness: 0.05, transparent: true, opacity: 0.72,
  });
  const axonCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(0.9, 0, 0), new THREE.Vector3(2.0, 0.04, 0), new THREE.Vector3(3.0, -0.02, 0), new THREE.Vector3(3.55, 0, 0),
  ]);
  const axon = new THREE.Mesh(new THREE.TubeGeometry(axonCurve, 48, 0.075, tubeRadial, false), axonMat);
  axon.castShadow = quality.shadows;
  scene.add(axon);
  const axonSamples = sampleCurve(axonCurve);

  // Myelin sheath with nodes of Ranvier - the gaps are what makes saltatory conduction fast.
  const sheathGroup = new THREE.Group();
  for (let i = 0; i < 4; i++) {
    const t0 = 0.06 + i * 0.23;
    const p0 = new THREE.Vector3(axonSamples[Math.round(t0 * SAMPLE_COUNT) * 3], axonSamples[Math.round(t0 * SAMPLE_COUNT) * 3 + 1], axonSamples[Math.round(t0 * SAMPLE_COUNT) * 3 + 2]);
    const i1 = Math.round((t0 + 0.15) * SAMPLE_COUNT);
    const p1 = new THREE.Vector3(axonSamples[i1 * 3], axonSamples[i1 * 3 + 1], axonSamples[i1 * 3 + 2]);
    const len = p0.distanceTo(p1);
    const s = new THREE.Mesh(new THREE.CapsuleGeometry(0.115, len, 4, tubeRadial), sheathMat);
    s.position.copy(p0).add(p1).multiplyScalar(0.5);
    s.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p1.clone().sub(p0).normalize());
    sheathGroup.add(s);
  }
  scene.add(sheathGroup);

  // Synaptic terminal: the axon splits into buttons that face the output neuron.
  const terminalGroup = new THREE.Group();
  const buttonMat = new THREE.MeshStandardMaterial({
    color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.3, roughness: 0.4, metalness: 0.1,
  });
  for (let i = 0; i < 3; i++) {
    const a = (i - 1) * 0.55;
    const from = new THREE.Vector3(3.55, 0, 0);
    const to = new THREE.Vector3(4.28, Math.sin(a) * 0.42, Math.cos(a) * 0.16);
    const mid = from.clone().lerp(to, 0.5);
    mid.z += 0.05;
    const curve = new THREE.CatmullRomCurve3([from, mid, to]);
    const branch = new THREE.Mesh(new THREE.TubeGeometry(curve, 16, 0.028, 6, false), axonMat);
    terminalGroup.add(branch);
    const button = new THREE.Mesh(new THREE.SphereGeometry(0.10, 12, 10), buttonMat);
    button.position.copy(to);
    terminalGroup.add(button);
  }
  scene.add(terminalGroup);

  const dendriteTargets = [
    new THREE.Vector3(-0.92, 0.34, 0),
    new THREE.Vector3(-0.98, 0.0, 0),
    new THREE.Vector3(-0.92, -0.34, 0),
  ];

  function rebuildDendrite(i) {
    const inp = inputs[i];
    const y = inputNodes[i].y;
    const radius = 0.028 + Math.abs(inp.weight) * 0.062;
    const curve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-4.15, y, 0),
      new THREE.Vector3(-3.0, y * 0.72, 0.02),
      new THREE.Vector3(-1.9, y * 0.34, 0.0),
      dendriteTargets[i],
    ]);
    const geo = new THREE.TubeGeometry(curve, 40, radius, tubeRadial, false);
    dendriteMeshes[i].geometry.dispose();
    dendriteMeshes[i].geometry = geo;
    dendriteSamples[i] = sampleCurve(curve);
    dendriteMat[i].color.setHex(inp.weight >= 0 ? 0x60a5fa : 0xf87171);
    dendriteMat[i].emissive.setHex(inp.weight >= 0 ? 0x1d4ed8 : 0x991b1b);
    // The weight readout is baked into a texture, so it has to be regenerated when the
    // slider moves - the old build left a stale number on screen forever.
    const slot = weightLabels[i];
    if (slot.sprite) scene.remove(slot.sprite);
    const lbl = makeLabelSprite(`w=${inp.weight.toFixed(1)}`, { scale: 0.45, fontSize: 30 });
    lbl.position.set(-2.5, slot.y + 0.4, 0);
    scene.add(lbl);
    slot.sprite = lbl;
  }
  for (let i = 0; i < inputs.length; i++) rebuildDendrite(i);

  // ---- signal particles ----------------------------------------------------
  const MAX_SIG = 220;
  const signal = makeSignalPoints(MAX_SIG, { size: 0.19 });
  scene.add(signal.points);
  const sigPath = new Int32Array(MAX_SIG); // 0..2 dendrite index, 3 = axon
  const sigT = new Float32Array(MAX_SIG);
  const sigCol = new Float32Array(MAX_SIG * 3);
  let sigCount = 0;

  function spawnSignal(path, col) {
    if (sigCount >= MAX_SIG) return;
    const i = sigCount++;
    sigPath[i] = path;
    sigT[i] = 0;
    sigCol[i * 3] = col[0]; sigCol[i * 3 + 1] = col[1]; sigCol[i * 3 + 2] = col[2];
  }

  const hud = createHud(stage);
  const sumBadge = hud.badge('Sum = 0.0', '#a3e635');
  const outBadge = hud.badge('output is 0.0', '#fbbf24');

  const panel = createPanel(stage, { title: 'Meet the Neuron' });
  panel.info('A neuron multiplies each input by its weight, adds them with a bias, and squashes the result through an activation. Slide the inputs and weights and watch the output light up.');
  inputs.forEach((inp, i) => {
    panel.slider({
      label: `Input ${i + 1}`, min: 0, max: 100, step: 1, value: inp.val * 100,
      format: (v) => v.toFixed(0),
      onChange: (v) => { inp.val = v / 100; recompute(); },
    });
    panel.slider({
      label: `  weight w${i + 1}`, min: -150, max: 150, step: 5, value: inp.weight * 100,
      format: (v) => (v / 100).toFixed(2),
      onChange: (v) => { inp.weight = v / 100; rebuildDendrite(i); recompute(); },
    });
  });
  panel.slider({
    label: 'Bias', min: -200, max: 200, step: 5, value: 0,
    format: (v) => (v / 100).toFixed(2),
    onChange: (v) => { bias = v / 100; recompute(); },
  });
  panel.divider();
  const sumOut = panel.readout({ label: 'Weighted sum', value: '0.00' });
  const actOut = panel.readout({ label: 'Activation (sigmoid)', value: '0.50' });
  panel.button({ label: 'What is ReLU / sigmoid?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Activation functions',
      body: 'The activation decides whether the neuron fires. Sigmoid squashes any sum into 0-1 (a smooth yes/no). ReLU outputs 0 for negatives and the raw value for positives - simpler, and stacked in millions it powers modern deep learning.',
      color: '#6366F1',
    });
  } });

  // Recompute is event driven: it runs when a control changes, not once per frame. The old
  // version called it inside the render loop, producing four DOM writes every frame.
  function recompute() {
    let sum = bias;
    for (let i = 0; i < inputs.length; i++) sum += inputs[i].val * inputs[i].weight;
    weightedSum = sum;
    outValue = 1 / (1 + Math.exp(-sum));
    sumBadge.set(`Sum = ${sum.toFixed(2)}`);
    outBadge.set(`output is ${outValue.toFixed(2)}`);
    sumOut.set(sum.toFixed(2));
    actOut.set(outValue.toFixed(2));
    somaMat.emissiveIntensity = 0.2 + outValue * 0.9;
    outMat.emissiveIntensity = 0.2 + outValue * 1.2;
    buttonMat.emissiveIntensity = 0.15 + outValue * 1.0;
    for (let i = 0; i < inputNodes.length; i++) {
      inputNodes[i].mat.emissiveIntensity = inputs[i].val * 0.9;
    }
  }
  recompute();

  let sigAcc = 0;
  let pulseAcc = 0;
  engine.setUpdate((dt) => {
    controls.update(dt);

    // Spawn signals in proportion to how strongly each input is driving the cell.
    sigAcc += dt;
    if (sigAcc > 0.05) {
      sigAcc = 0;
      for (let i = 0; i < inputs.length; i++) {
        const inp = inputs[i];
        if (Math.abs(inp.weight) > 0.05 && Math.random() < inp.val * 0.55) {
          spawnSignal(i, inp.weight >= 0 ? [0.45, 0.7, 1] : [1, 0.5, 0.5]);
        }
      }
    }

    // Advance along the sampled path buffers: no Vector3 allocation per particle per frame.
    let w = 0;
    for (let i = 0; i < sigCount; i++) {
      let t = sigT[i] + dt * 1.15;
      let path = sigPath[i];
      if (t >= 1) {
        if (path < 3) { path = 3; t -= 1; sigPath[i] = 3; } else continue;
      }
      sigPath[w] = path;
      sigT[w] = t;
      sigCol[w * 3] = sigCol[i * 3];
      sigCol[w * 3 + 1] = sigCol[i * 3 + 1];
      sigCol[w * 3 + 2] = sigCol[i * 3 + 2];

      const samples = path < 3 ? dendriteSamples[path] : axonSamples;
      const f = t * SAMPLE_COUNT;
      const i0 = Math.min(SAMPLE_COUNT, f | 0);
      const i1 = Math.min(SAMPLE_COUNT, i0 + 1);
      const frac = f - i0;
      const o = w * 3;
      signal.position[o] = samples[i0 * 3] + (samples[i1 * 3] - samples[i0 * 3]) * frac;
      signal.position[o + 1] = samples[i0 * 3 + 1] + (samples[i1 * 3 + 1] - samples[i0 * 3 + 1]) * frac;
      signal.position[o + 2] = samples[i0 * 3 + 2] + (samples[i1 * 3 + 2] - samples[i0 * 3 + 2]) * frac;
      const gain = path < 3 ? 0.55 + Math.abs(weightedSum) * 0.1 : 0.7 + outValue * 0.8;
      signal.color[o] = sigCol[i * 3] * gain;
      signal.color[o + 1] = sigCol[i * 3 + 1] * gain;
      signal.color[o + 2] = sigCol[i * 3 + 2] * gain;
      w++;
    }
    sigCount = w;

    signal.geo.setDrawRange(0, sigCount);
    if (sigCount > 0) {
      signal.geo.attributes.position.needsUpdate = true;
      signal.geo.attributes.color.needsUpdate = true;
    }

    // Gentle systolic pulse scaled by how strongly the cell is firing.
    pulseAcc += dt;
    const beat = 1 + Math.sin(pulseAcc * 3.2) * 0.03 * outValue;
    soma.scale.setScalar(beat);
    nucleus.scale.setScalar(beat);
    outNode.scale.setScalar(1 + (outValue - 0.5) * 0.12);
  });

  engine.start();

  return {
    dispose() {
      dendriteMeshes.forEach((m) => m.geometry.dispose());
      dendriteMat.forEach((m) => m.dispose());
      [soma, nucleus, outNode, axon].forEach((m) => m.geometry.dispose());
      sheathGroup.traverse((o) => { if (o.geometry) o.geometry.dispose(); });
      terminalGroup.traverse((o) => { if (o.geometry) o.geometry.dispose(); });
      signal.geo.dispose();
      signal.mat.dispose();
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
