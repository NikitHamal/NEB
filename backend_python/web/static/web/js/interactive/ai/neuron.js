import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

export default function init(stage) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(12, quality.segments / 2);

  camera.position.set(0, 1.5, 11);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 5, maxDistance: 20, enablePan: false, maxPolar: Math.PI * 0.7, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 0.5, 0));

  scene.background = new THREE.Color(0x0a0e1a);
  scene.fog = new THREE.Fog(0x0a0e1a, 16, 34);
  basicLights(scene, { ambient: 0.45, key: 1.5 });

  // The neuron body (soma): a glowing sphere
  const somaMat = new THREE.MeshStandardMaterial({
    color: 0x6366f1, emissive: 0x4338ca, emissiveIntensity: 0.3, roughness: 0.4,
  });
  const soma = new THREE.Mesh(new THREE.SphereGeometry(1.0, seg, seg), somaMat);
  soma.castShadow = true; scene.add(soma);

  // Three inputs on the left
  const inputs = [
    { val: 0.6, weight: 0.8, color: 0x60a5fa },
    { val: 0.4, weight: -0.5, color: 0xf472b6 },
    { val: 0.8, weight: 0.6, color: 0x34d399 },
  ];
  let bias = 0.0;

  const inputGroup = new THREE.Group(); scene.add(inputGroup);
  const inputNodes = [];
  const wires = [];
  inputs.forEach((inp, i) => {
    const y = 2.2 - i * 2.2;
    const mat = new THREE.MeshStandardMaterial({
      color: inp.color, emissive: inp.color, emissiveIntensity: inp.val * 0.8, roughness: 0.4,
    });
    const node = new THREE.Mesh(new THREE.SphereGeometry(0.35, seg, seg), mat);
    node.position.set(-4.5, y, 0); node.castShadow = true;
    inputGroup.add(node); inputNodes.push({ node, mat, inp, y });

    // wire from input to soma — thickness encodes |weight|
    const wireMat = new THREE.LineBasicMaterial({ color: inp.weight >= 0 ? 0x60a5fa : 0xf87171, linewidth: 2 });
    const geo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-4.15, y, 0), new THREE.Vector3(-0.9, 0, 0),
    ]);
    const line = new THREE.Line(geo, wireMat);
    inputGroup.add(line); wires.push({ line, mat: wireMat, inp });

    // weight label
    const lbl = makeLabelSprite(`w=${inp.weight.toFixed(1)}`, { scale: 0.45, fontSize: 30 });
    lbl.position.set(-2.5, y + 0.4, 0); inputGroup.add(lbl);
  });

  // Output on the right
  const outMat = new THREE.MeshStandardMaterial({
    color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.2, roughness: 0.4,
  });
  const outNode = new THREE.Mesh(new THREE.SphereGeometry(0.45, seg, seg), outMat);
  outNode.position.set(4, 0, 0); outNode.castShadow = true; scene.add(outNode);
  const outWire = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(1.0, 0, 0), new THREE.Vector3(3.55, 0, 0)]),
    new THREE.LineBasicMaterial({ color: 0xfbbf24 })
  );
  scene.add(outWire);

  // Signal particles travelling along wires
  const MAX_SIG = 60;
  const sigPos = new Float32Array(MAX_SIG * 3);
  const sigCol = new Float32Array(MAX_SIG * 3);
  const sigGeo = new THREE.BufferGeometry();
  sigGeo.setAttribute('position', new THREE.BufferAttribute(sigPos, 3));
  sigGeo.setAttribute('color', new THREE.BufferAttribute(sigCol, 3));
  const sigMat = new THREE.PointsMaterial({ size: 0.16, vertexColors: true, transparent: true, opacity: 0.9, depthWrite: false });
  const sig = new THREE.Points(sigGeo, sigMat); scene.add(sig);
  const sigs = []; // {t, inputIdx, color}

  function activation(x) {
    // ReLU for >=0 area, but show sigmoid-like glow for nicer visual: use sigmoid
    return 1 / (1 + Math.exp(-x));
  }

  let outValue = 0;

  const hud = createHud(stage);
  const sumBadge = hud.badge('Σ = 0.0', '#a3e635');
  const outBadge = hud.badge('output ≈ 0.0', '#fbbf24');

  const panel = createPanel(stage, { title: 'Meet the Neuron' });
  panel.info('A neuron multiplies each input by its weight, adds them with a bias, and squashes the result through an activation. Slide the inputs and weights and watch the output light up.');
  inputs.forEach((inp, i) => {
    panel.slider({
      label: `Input ${i + 1}`, min: 0, max: 100, step: 1, value: inp.val * 100,
      format: (v) => v.toFixed(0),
      onChange: (v) => { inp.val = v / 100; },
    });
    panel.slider({
      label: `  weight w${i + 1}`, min: -150, max: 150, step: 5, value: inp.weight * 100,
      format: (v) => (v / 100).toFixed(2),
      onChange: (v) => { inp.weight = v / 100; },
    });
  });
  panel.slider({
    label: 'Bias', min: -200, max: 200, step: 5, value: 0,
    format: (v) => (v / 100).toFixed(2),
    onChange: (v) => { bias = v / 100; },
  });
  panel.divider();
  const sumOut = panel.readout({ label: 'Weighted sum', value: '0.00' });
  const actOut = panel.readout({ label: 'Activation (sigmoid)', value: '0.50' });
  panel.button({ label: 'What is ReLU / sigmoid?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Activation functions',
      body: 'The activation decides whether the neuron fires. Sigmoid squashes any sum into 0–1 (a smooth yes/no). ReLU outputs 0 for negatives and the raw value for positives — simpler, and stacked in millions it powers modern deep learning.',
      color: '#6366F1',
    });
  } });

  function recompute() {
    let sum = bias;
    inputs.forEach((inp) => { sum += inp.val * inp.weight; });
    outValue = activation(sum);
    sumBadge.set(`Σ = ${sum.toFixed(2)}`);
    outBadge.set(`output ≈ ${outValue.toFixed(2)}`);
    sumOut.set(sum.toFixed(2));
    actOut.set(outValue.toFixed(2));
    // soma glow scales with output
    somaMat.emissiveIntensity = 0.2 + outValue * 0.9;
    outMat.emissiveIntensity = 0.2 + outValue * 1.2;
    // input glows scale with input value
    inputNodes.forEach(({ mat, inp }) => { mat.emissiveIntensity = inp.val * 0.9; });
    // wire colour: blue positive, red negative; opacity by |weight|
    wires.forEach(({ mat, inp }) => {
      mat.color.setHex(inp.weight >= 0 ? 0x60a5fa : 0xf87171);
    });
  }
  recompute();

  let sigAcc = 0;
  engine.setUpdate((dt) => {
    controls.update(dt);
    recompute();
    // spawn signals proportional to input * |weight|
    sigAcc += dt;
    if (sigAcc > 0.08) {
      sigAcc = 0;
      inputNodes.forEach(({ inp, y }, i) => {
        if (Math.abs(inp.weight) > 0.05 && Math.random() < inp.val * 0.6) {
          if (sigs.length < MAX_SIG) {
            sigs.push({ t: 0, y, color: inp.weight >= 0 ? [0.4, 0.65, 1] : [1, 0.45, 0.45] });
          }
        }
      });
    }
    // advance signals along wire from input to soma, then soma to output
    let w = 0;
    const colOut = [1, 0.75, 0.2];
    for (let i = 0; i < sigs.length; i++) {
      const s = sigs[i];
      s.t += dt * 1.2;
      if (s.t > 2) continue;
      let x, y, r, g, b;
      if (s.t < 1) {
        const tt = s.t;
        x = -4.15 + tt * 3.25; y = s.y * (1 - tt); r = s.color[0]; g = s.color[1]; b = s.color[2];
      } else {
        const tt = s.t - 1;
        x = 1.0 + tt * 2.55; y = 0; r = colOut[0]; g = colOut[1]; b = colOut[2];
      }
      sigPos[w * 3] = x; sigPos[w * 3 + 1] = y; sigPos[w * 3 + 2] = 0;
      sigCol[w * 3] = r; sigCol[w * 3 + 1] = g; sigCol[w * 3 + 2] = b;
      w++;
    }
    sigs.length = w;
    sigGeo.setDrawRange(0, w);
    sigGeo.attributes.position.needsUpdate = true;
    sigGeo.attributes.color.needsUpdate = true;

    // gentle soma pulse
    soma.scale.setScalar(1 + Math.sin(performance.now() * 0.003) * 0.03 * outValue);
  });

  engine.start();

  return {
    dispose() {
      sigGeo.dispose(); sigMat.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
