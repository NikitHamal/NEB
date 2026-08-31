import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite, makeSignalPoints } from '../core/engine.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

export default function init(stage) {
  const engine = createEngine(stage, { shadows: true, environment: true, exposure: 1.05 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = Math.max(10, Math.round(quality.segments / 3));

  camera.position.set(0, 2, 13);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 6, maxDistance: 22, enablePan: false, maxPolar: Math.PI * 0.7, minPolar: Math.PI * 0.2,
  });
  controls.setTarget(new THREE.Vector3(0, 0, 0));

  scene.background = new THREE.Color(0x070a18);
  scene.fog = new THREE.Fog(0x070a18, 16, 38);
  basicLights(scene, { ambient: 0.38, key: 1.35, fill: 0.45, rim: 0.5, rimPos: [-6, 4, -8] });

  const LAYOUT = [4, 6, 5, 3];
  const LAYER_LABELS = ['Input', 'Hidden 1', 'Hidden 2', 'Output'];
  const LAYER_SPACING = 3.4;
  const NEURON_SPACING = 1.5;
  const NEURON_RADIUS = 0.32;
  const LAYER_COUNT = LAYOUT.length;
  const NEURON_COUNT = LAYOUT.reduce((a, b) => a + b, 0);

  // ---- neurons -------------------------------------------------------------
  // Index neurons globally so connections can be resolved by integer id instead of the
  // O(n) `find` lookups the previous build used inside an O(n^2) loop.
  const layerStart = [];
  let cursor = 0;
  for (let li = 0; li < LAYER_COUNT; li++) { layerStart.push(cursor); cursor += LAYOUT[li]; }

  const neuronLayer = new Int32Array(NEURON_COUNT);
  const neuronPos = new Float32Array(NEURON_COUNT * 3);
  const neuronMesh = new Array(NEURON_COUNT);
  const neuronMat = new Array(NEURON_COUNT);
  const neuronGlow = new Float32Array(NEURON_COUNT);

  // One geometry shared by every neuron: 18 spheres no longer mean 18 vertex buffers.
  const neuronGeometry = new THREE.SphereGeometry(NEURON_RADIUS, seg, Math.max(8, seg >> 1));

  for (let li = 0; li < LAYER_COUNT; li++) {
    const x = (li - (LAYER_COUNT - 1) / 2) * LAYER_SPACING;
    for (let i = 0; i < LAYOUT[li]; i++) {
      const id = layerStart[li] + i;
      const y = (i - (LAYOUT[li] - 1) / 2) * NEURON_SPACING;
      neuronLayer[id] = li;
      neuronPos[id * 3] = x;
      neuronPos[id * 3 + 1] = y;
      neuronPos[id * 3 + 2] = 0;
      const mat = new THREE.MeshStandardMaterial({
        color: 0x6366f1,
        emissive: 0x312e81,
        emissiveIntensity: 0.3,
        roughness: 0.34,
        metalness: 0.12,
      });
      const mesh = new THREE.Mesh(neuronGeometry, mat);
      mesh.position.set(x, y, 0);
      mesh.castShadow = quality.shadows;
      scene.add(mesh);
      neuronMesh[id] = mesh;
      neuronMat[id] = mat;
      neuronGlow[id] = 0.3;
    }
  }

  // ---- layer plates --------------------------------------------------------
  // Thin panels behind each column give the layout physical depth and make the
  // layer-to-layer ordering readable without extra labels.
  const plateMat = new THREE.MeshStandardMaterial({
    color: 0x111a33, roughness: 0.62, metalness: 0.2,
    transparent: true, opacity: 0.55, side: THREE.DoubleSide,
  });
  for (let li = 0; li < LAYER_COUNT; li++) {
    const x = (li - (LAYER_COUNT - 1) / 2) * LAYER_SPACING;
    const h = LAYOUT[li] * NEURON_SPACING * 0.62 + 0.55;
    const plate = new THREE.Mesh(new THREE.PlaneGeometry(1.5, h), plateMat);
    plate.position.set(x, 0, -0.72);
    scene.add(plate);
    const lbl = makeLabelSprite(LAYER_LABELS[li], { scale: 0.2, fontSize: 30, bg: 'rgba(11,28,48,0.7)' });
    lbl.position.set(x, h / 2 + 0.42, -0.7);
    scene.add(lbl);
  }

  // ---- connections ---------------------------------------------------------
  // All 69 synapses are packed into a single LineSegments buffer with per-vertex colour,
  // replacing 69 individual THREE.Line objects (69 draw calls) with one.
  const CONN_COUNT = (() => {
    let n = 0;
    for (let li = 0; li < LAYER_COUNT - 1; li++) n += LAYOUT[li] * LAYOUT[li + 1];
    return n;
  })();

  const connFrom = new Int32Array(CONN_COUNT);
  const connTo = new Int32Array(CONN_COUNT);
  const connWeight = new Float32Array(CONN_COUNT);
  const connPos = new Float32Array(CONN_COUNT * 6);
  const connColor = new Float32Array(CONN_COUNT * 8);
  // outgoing[neuronId] -> array of connection indices; precomputed so signal propagation
  // never allocates a filtered array inside the animation loop.
  const outgoing = [];
  for (let i = 0; i < NEURON_COUNT; i++) outgoing.push([]);

  let ci = 0;
  for (let li = 0; li < LAYER_COUNT - 1; li++) {
    for (let a = 0; a < LAYOUT[li]; a++) {
      const from = layerStart[li] + a;
      for (let b = 0; b < LAYOUT[li + 1]; b++) {
        const to = layerStart[li + 1] + b;
        const weight = Math.random() * 2 - 1;
        connFrom[ci] = from;
        connTo[ci] = to;
        connWeight[ci] = weight;
        outgoing[from].push(ci);
        ci++;
      }
    }
  }
  const outgoingFlat = outgoing.map((arr) => Int32Array.from(arr));

  for (let c = 0; c < CONN_COUNT; c++) {
    const f = connFrom[c] * 3;
    const t = connTo[c] * 3;
    connPos[c * 6] = neuronPos[f];
    connPos[c * 6 + 1] = neuronPos[f + 1];
    connPos[c * 6 + 2] = neuronPos[f + 2];
    connPos[c * 6 + 3] = neuronPos[t];
    connPos[c * 6 + 4] = neuronPos[t + 1];
    connPos[c * 6 + 5] = neuronPos[t + 2];
    // Positive weights read cool, inhibitory weights read warm; alpha carries |weight|.
    setConnColor(c, connWeight[c]);
  }

  function setConnColor(c, weight) {
    const positive = weight >= 0;
    const strength = 0.10 + Math.abs(weight) * 0.20;
    const r = positive ? 0.31 : 1.0;
    const g = positive ? 0.48 : 0.33;
    const b = positive ? 1.0 : 0.40;
    const base = c * 8;
    connColor[base] = r; connColor[base + 1] = g; connColor[base + 2] = b; connColor[base + 3] = strength;
    connColor[base + 4] = r; connColor[base + 5] = g; connColor[base + 6] = b; connColor[base + 7] = strength;
  }

  const connGeo = new THREE.BufferGeometry();
  connGeo.setAttribute('position', new THREE.BufferAttribute(connPos, 3));
  connGeo.setAttribute('color', new THREE.BufferAttribute(connColor, 4));
  const connMat = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false });
  const connLines = new THREE.LineSegments(connGeo, connMat);
  connLines.userData.noScan = true;
  scene.add(connLines);

  // ---- signal pulses -------------------------------------------------------
  const MAX_PULSE = 512;
  const signal = makeSignalPoints(MAX_PULSE, { size: 0.22 });
  scene.add(signal.points);
  const pulseConn = new Int32Array(MAX_PULSE);
  const pulseT = new Float32Array(MAX_PULSE);
  const pulseStrength = new Float32Array(MAX_PULSE);
  let pulseCount = 0;

  const inputVals = [1, 0.5, 0.8, 0.3];
  let speed = 1.0;
  let autoFeed = true;
  let activeLayer = -1;

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
    format: (x) => `${(x / 100).toFixed(1)}x`,
    onChange: (x) => { speed = x / 100; },
  });
  panel.toggle({ label: 'Auto-feed inputs', value: true, onChange: (v) => { autoFeed = v; } });
  panel.button({ label: 'Fire one signal', icon: 'bolt', onClick: () => { fireFromInputs(); } });
  panel.divider();
  panel.readout({ label: 'Layers', value: LAYOUT.join(' -> ') });
  panel.readout({ label: 'Total neurons', value: String(NEURON_COUNT) });
  panel.readout({ label: 'Connections', value: String(CONN_COUNT) });
  const depthOut = panel.readout({ label: 'Signals in flight', value: '0' });
  panel.button({ label: 'Why does depth matter?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'Depth creates power',
      body: 'Each layer builds on the last: early layers detect simple features, deeper layers combine them into complex ones. Stacking many layers (depth) lets a network represent abstractions efficiently - far fewer neurons than one giant layer would need.',
      color: '#6366F1',
    });
  } });

  function spawnPulse(connIndex, strength) {
    if (pulseCount >= MAX_PULSE || strength <= 0.004) return;
    pulseConn[pulseCount] = connIndex;
    pulseT[pulseCount] = 0;
    pulseStrength[pulseCount] = strength;
    pulseCount++;
  }

  function fireFromInputs() {
    for (let i = 0; i < LAYOUT[0]; i++) {
      const value = inputVals[i];
      if (value <= 0.05) continue;
      const id = layerStart[0] + i;
      const edges = outgoingFlat[id];
      for (let k = 0; k < edges.length; k++) {
        const c = edges[k];
        spawnPulse(c, value * Math.abs(connWeight[c]));
      }
    }
    activeLayer = 0;
    passBadge.set('Forward pass ->');
  }

  let feedAcc = 0;
  let hudAcc = 0;
  engine.setUpdate((dt) => {
    controls.update(dt);

    // Input neurons glow with their slider value; deeper neurons decay toward rest.
    for (let i = 0; i < LAYOUT[0]; i++) {
      const id = layerStart[0] + i;
      neuronGlow[id] = 0.2 + inputVals[i] * 1.0;
    }
    for (let li = 1; li < LAYER_COUNT; li++) {
      for (let i = 0; i < LAYOUT[li]; i++) {
        const id = layerStart[li] + i;
        neuronGlow[id] += (0.25 - neuronGlow[id]) * 0.05;
      }
    }

    if (autoFeed) {
      feedAcc += dt * speed;
      if (feedAcc > 0.8) { feedAcc = 0; fireFromInputs(); }
    }

    // Advance pulses in place and compact the array without allocating.
    // The bound is captured because arriving pulses spawn children during the loop.
    const startCount = pulseCount;
    let w = 0;
    const step = dt * speed * 1.2;
    for (let i = 0; i < startCount; i++) {
      const c = pulseConn[i];
      const t = pulseT[i] + step;
      if (t >= 1) {
        const target = connTo[c];
        const strength = pulseStrength[i];
        neuronGlow[target] = Math.min(1.4, neuronGlow[target] + strength * 0.8);
        const li = neuronLayer[target];
        if (li > activeLayer) activeLayer = li;
        if (li < LAYER_COUNT - 1) {
          const edges = outgoingFlat[target];
          for (let k = 0; k < edges.length; k++) {
            spawnPulse(edges[k], strength * Math.abs(connWeight[edges[k]]) * 0.9);
          }
        }
        continue;
      }
      pulseConn[w] = c;
      pulseT[w] = t;
      pulseStrength[w] = pulseStrength[i];
      w++;
      const a = connFrom[c] * 3;
      const b = connTo[c] * 3;
      const o = (w - 1) * 3;
      signal.position[o] = neuronPos[a] + (neuronPos[b] - neuronPos[a]) * t;
      signal.position[o + 1] = neuronPos[a + 1] + (neuronPos[b + 1] - neuronPos[a + 1]) * t;
      signal.position[o + 2] = neuronPos[a + 2] + (neuronPos[b + 2] - neuronPos[a + 2]) * t;
      const s = pulseStrength[i];
      const positive = connWeight[c] >= 0;
      signal.color[o] = (positive ? 0.45 : 1.0) * s;
      signal.color[o + 1] = (positive ? 0.65 : 0.42) * s;
      signal.color[o + 2] = (positive ? 1.0 : 0.48) * s;
    }
    // Survivors occupy [0, w); children spawned during the loop sit in [startCount, pulseCount).
    // Slide that tail down so nothing is dropped. dst < src, so a forward copy is safe.
    const spawned = pulseCount - startCount;
    if (spawned > 0 && w !== startCount) {
      for (let k = 0; k < spawned; k++) {
        pulseConn[w + k] = pulseConn[startCount + k];
        pulseT[w + k] = pulseT[startCount + k];
        pulseStrength[w + k] = pulseStrength[startCount + k];
      }
    }
    pulseCount = w + spawned;

    signal.geo.setDrawRange(0, pulseCount);
    if (pulseCount > 0) {
      signal.geo.attributes.position.needsUpdate = true;
      signal.geo.attributes.color.needsUpdate = true;
    }

    // Push the animated glow values onto the shared per-neuron materials.
    for (let i = 0; i < NEURON_COUNT; i++) {
      const m = neuronMat[i];
      m.emissiveIntensity = neuronGlow[i];
      const s = 1 + (neuronGlow[i] - 0.3) * 0.14;
      neuronMesh[i].scale.setScalar(s);
    }

    hudAcc += dt;
    if (hudAcc > 0.15) {
      hudAcc = 0;
      depthOut.set(String(pulseCount));
      if (activeLayer >= 0 && activeLayer < LAYER_COUNT) {
        passBadge.set(pulseCount > 0 ? `Forward pass -> ${LAYER_LABELS[activeLayer]}` : 'Forward pass: idle');
      }
      if (pulseCount === 0) activeLayer = -1;
    }
  });

  engine.start();

  return {
    dispose() {
      neuronGeometry.dispose();
      connGeo.dispose();
      connMat.dispose();
      signal.geo.dispose();
      signal.mat.dispose();
      plateMat.dispose();
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
