import { THREE, createEngine, createOrbitControls, basicLights } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

export default function init(stage) {
  const engine = createEngine(stage, { shadows: true });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(10, quality.segments / 3);

  camera.position.set(0, 2, 13);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 6, maxDistance: 22, enablePan: false, maxPolar: Math.PI * 0.7, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 0, 0));

  scene.background = new THREE.Color(0x070a18);
  scene.fog = new THREE.Fog(0x070a18, 16, 38);
  basicLights(scene, { ambient: 0.5, key: 1.4 });

  // Layer config
  const LAYOUT = [4, 6, 5, 3]; // input, hidden1, hidden2, output
  const LAYER_LABELS = ['Input', 'Hidden 1', 'Hidden 2', 'Output'];
  const LAYER_SPACING = 3.4;
  const NEURON_SPACING = 1.5;

  const layerGroups = [];
  const allNeurons = [];
  const allConnections = [];

  LAYOUT.forEach((count, li) => {
    const group = new THREE.Group();
    const x = (li - (LAYOUT.length - 1) / 2) * LAYER_SPACING;
    group.position.x = x;
    for (let i = 0; i < count; i++) {
      const y = (i - (count - 1) / 2) * NEURON_SPACING;
      const mat = new THREE.MeshStandardMaterial({
        color: 0x6366f1, emissive: 0x312e81, emissiveIntensity: 0.3, roughness: 0.4,
      });
      const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.32, seg, seg), mat);
      mesh.position.set(0, y, 0); mesh.castShadow = true;
      group.add(mesh);
      allNeurons.push({ mesh, mat, layer: li, idx: i, basePos: new THREE.Vector3(x, y, 0) });
    }
    scene.add(group);
    layerGroups.push(group);
  });

  // Connections: each neuron to every neuron in the next layer
  for (let li = 0; li < LAYOUT.length - 1; li++) {
    const fromCount = LAYOUT[li];
    const toCount = LAYOUT[li + 1];
    for (let a = 0; a < fromCount; a++) {
      for (let b = 0; b < toCount; b++) {
        const from = allNeurons.find((n) => n.layer === li && n.idx === a);
        const to = allNeurons.find((n) => n.layer === li + 1 && n.idx === b);
        // weight as random for visual variety
        const weight = (Math.random() * 2 - 1);
        const geo = new THREE.BufferGeometry().setFromPoints([from.basePos.clone(), to.basePos.clone()]);
        const mat = new THREE.LineBasicMaterial({
          color: weight >= 0 ? 0x4f7bff : 0xff5566,
          transparent: true, opacity: 0.12 + Math.abs(weight) * 0.18,
        });
        const line = new THREE.Line(geo, mat);
        scene.add(line);
        allConnections.push({ line, mat, from, to, weight });
      }
    }
  }

  // Signal pulses travelling along connections
  const MAX_PULSE = 200;
  const pulsePos = new Float32Array(MAX_PULSE * 3);
  const pulseCol = new Float32Array(MAX_PULSE * 3);
  const pulseGeo = new THREE.BufferGeometry();
  pulseGeo.setAttribute('position', new THREE.BufferAttribute(pulsePos, 3));
  pulseGeo.setAttribute('color', new THREE.BufferAttribute(pulseCol, 3));
  const pulseMat = new THREE.PointsMaterial({ size: 0.18, vertexColors: true, transparent: true, opacity: 0.95, depthWrite: false });
  const pulses = new THREE.Points(pulseGeo, pulseMat); scene.add(pulses);
  const pulseList = []; // {conn, t, color}

  // Input values (sliders) drive the signal
  let inputVals = [1, 0.5, 0.8, 0.3];
  let speed = 1.0;
  let autoFeed = true;

  const hud = createHud(stage);
  const passBadge = hud.badge('Forward pass: idle', '#a3e635');

  const panel = createPanel(stage, { title: 'Inside a Neural Network' });
  panel.info('A neural network passes signals forward, layer by layer. Each connection has a weight; brighter pulses mean stronger signals. Slide the inputs and watch the wave travel to the output.');
  inputVals.forEach((v, i) => {
    panel.slider({
      label: `Input ${i + 1}`, min: 0, max: 100, step: 1, value: v * 100,
      format: (x) => x.toFixed(0),
      onChange: (x) => { inputVals[i] = x / 100; },
    });
  });
  panel.slider({
    label: 'Signal speed', min: 20, max: 300, step: 10, value: 100,
    format: (x) => `${(x / 100).toFixed(1)}×`,
    onChange: (x) => { speed = x / 100; },
  });
  panel.toggle({ label: 'Auto-feed inputs', value: true, onChange: (v) => { autoFeed = v; } });
  panel.button({ label: 'Fire one signal', icon: 'bolt', onClick: () => { fireFromInputs(); } });
  panel.divider();
  const layerOut = panel.readout({ label: 'Layers', value: LAYOUT.join(' → ') });
  panel.readout({ label: 'Total neurons', value: String(allNeurons.length) });
  panel.readout({ label: 'Connections', value: String(allConnections.length) });
  panel.button({ label: 'Why does depth matter?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Depth creates power',
      body: 'Each layer builds on the last: early layers detect simple features, deeper layers combine them into complex ones. Stacking many layers (depth) lets a network represent abstractions efficiently — far fewer neurons than one giant layer would need.',
      color: '#6366F1',
    });
  } });

  // input neuron glow follows inputVals
  function refreshInputGlow() {
    allNeurons.filter((n) => n.layer === 0).forEach((n, i) => {
      n.mat.emissiveIntensity = 0.2 + inputVals[i] * 1.0;
    });
  }

  function fireFromInputs() {
    allNeurons.filter((n) => n.layer === 0).forEach((n, i) => {
      if (inputVals[i] > 0.05) {
        allConnections.filter((c) => c.from === n).forEach((c) => {
          if (pulseList.length < MAX_PULSE) {
            pulseList.push({ conn: c, t: 0, strength: inputVals[i] * Math.abs(c.weight) });
          }
        });
      }
    });
    passBadge.set('Forward pass →');
  }

  let feedAcc = 0;
  engine.setUpdate((dt) => {
    controls.update(dt);
    refreshInputGlow();
    if (autoFeed) {
      feedAcc += dt * speed;
      if (feedAcc > 0.8) { feedAcc = 0; fireFromInputs(); }
    }
    // advance pulses
    let w = 0;
    for (let i = 0; i < pulseList.length; i++) {
      const p = pulseList[i];
      p.t += dt * speed * 1.2;
      if (p.t >= 1) {
        // arrived: light up target neuron and continue
        p.conn.to.mat.emissiveIntensity = Math.min(1.4, p.conn.to.mat.emissiveIntensity + p.strength * 0.8);
        // spawn onward pulses
        if (p.conn.to.layer < LAYOUT.length - 1) {
          allConnections.filter((c) => c.from === p.conn.to).forEach((c) => {
            if (pulseList.length < MAX_PULSE) {
              pulseList.push({ conn: c, t: 0, strength: p.strength * Math.abs(c.weight) * 0.9 });
            }
          });
        }
        continue;
      }
      const pos = p.conn.from.basePos.clone().lerp(p.conn.to.basePos, p.t);
      pulsePos[w * 3] = pos.x; pulsePos[w * 3 + 1] = pos.y; pulsePos[w * 3 + 2] = pos.z;
      const col = p.conn.weight >= 0 ? [0.35, 0.55, 1] : [1, 0.4, 0.45];
      pulseCol[w * 3] = col[0] * p.strength; pulseCol[w * 3 + 1] = col[1] * p.strength; pulseCol[w * 3 + 2] = col[2] * p.strength;
      w++;
    }
    pulseList.length = w;
    pulseGeo.setDrawRange(0, w);
    pulseGeo.attributes.position.needsUpdate = true;
    pulseGeo.attributes.color.needsUpdate = true;

    // decay neuron glows (except inputs)
    allNeurons.forEach((n) => {
      if (n.layer > 0) n.mat.emissiveIntensity += (0.25 - n.mat.emissiveIntensity) * 0.05;
    });
  });

  engine.start();

  return {
    dispose() {
      pulseGeo.dispose(); pulseMat.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose();
    },
  };
}
