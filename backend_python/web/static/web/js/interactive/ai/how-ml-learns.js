/**
 * How machines learn, in 3D — a real neural network (2 inputs → two hidden layers of tanh
 * neurons → a sigmoid output) trained in the browser by backpropagation and the Adam optimiser.
 * Its answer for every input is drawn as a landscape: height and colour are the predicted chance
 * of "orange". Orange points stand at height 1 and blue points lie at 0, so learning is the
 * landscape bending until it passes through them; the glowing line where it crosses one half is
 * the decision boundary. The loss (binary cross-entropy) falls on the graph, a held-out test set
 * (the rings) reveals overfitting, and the network itself is shown with its live weights.
 * Tap the floor to add a point, drag a point to move it.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createStudio, framer, THREE } from './ai3d/stage.js';

const KEYS = ['W1', 'b1', 'W2', 'b2', 'W3', 'b3'];
const MAXN = 260, HMAX = 12, G = 48;
const SQ = 2.4;      // half-size of the input square in world units
const HS = 1.8;      // height of probability 1
const ORANGE = new THREE.Color(0xf08c00), BLUE = new THREE.Color(0x2563eb);

function makeNet() {
  const n = { H: 6 };
  const sz = { W1: 2 * HMAX, b1: HMAX, W2: HMAX * HMAX, b2: HMAX, W3: HMAX, b3: 1 };
  for (const key in sz) { n[key] = new Float64Array(sz[key]); n['g' + key] = new Float64Array(sz[key]); n['m' + key] = new Float64Array(sz[key]); n['v' + key] = new Float64Array(sz[key]); }
  n.h1 = new Float64Array(HMAX); n.h2 = new Float64Array(HMAX); n.d1 = new Float64Array(HMAX); n.d2 = new Float64Array(HMAX);
  n.t = 0;
  return n;
}
function initNet(n, H) {
  n.H = H; n.t = 0;
  const r = (s) => (Math.random() * 2 - 1) * s;
  for (const key of KEYS) { n[key].fill(0); n['m' + key].fill(0); n['v' + key].fill(0); }
  for (let i = 0; i < 2 * H; i++) n.W1[i] = r(Math.sqrt(6 / (2 + H)));
  for (let i = 0; i < H * H; i++) n.W2[i] = r(Math.sqrt(6 / (2 * H)));
  for (let i = 0; i < H; i++) n.W3[i] = r(Math.sqrt(6 / (H + 1)));
}
function forward(n, x, y) {
  const H = n.H;
  for (let j = 0; j < H; j++) n.h1[j] = Math.tanh(n.W1[j] * x + n.W1[H + j] * y + n.b1[j]);
  for (let j = 0; j < H; j++) { let s = n.b2[j]; for (let i = 0; i < H; i++) s += n.W2[i * H + j] * n.h1[i]; n.h2[j] = Math.tanh(s); }
  let o = n.b3[0]; for (let j = 0; j < H; j++) o += n.W3[j] * n.h2[j];
  return 1 / (1 + Math.exp(-o));
}
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

export default function init(stage) {
  const S = createStudio(stage, { camera: [1.5, 6.2, 8.2], target: [1.4, 0.8, 0], maxDistance: 24 });
  if (!S) return null;
  const { engine, scene, camera, controls } = S;

  // ---- the network and its data (same maths as the classic 2D version) ----
  const px = new Float64Array(MAXN), py = new Float64Array(MAXN), lab = new Uint8Array(MAXN), test = new Uint8Array(MAXN);
  let n = 0, cls = 1, training = false, lr = 0.03, H = 6, epoch = 0, noise = 0.15, holdout = true, preset = 'circle';
  const net = makeNet();
  const trL = [], teL = [];

  function split() { for (let i = 0; i < n; i++) test[i] = holdout && ((i * 7919) % 4 === 0) ? 1 : 0; dirty = true; }
  function resetNet() { initNet(net, H); epoch = 0; trL.length = 0; teL.length = 0; dirty = true; buildNetGraph(); }
  function makeData() {
    n = 0;
    const g = () => { let u = 0; while (u === 0) u = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * Math.random()); };
    const add = (x, y, c) => { if (n < MAXN) { px[n] = clamp(x + g() * noise * 0.4, -1, 1); py[n] = clamp(y + g() * noise * 0.4, -1, 1); lab[n] = c; n++; } };
    const N = 140;
    for (let i = 0; i < N && preset !== 'none'; i++) {
      if (preset === 'blobs') { const c = i % 2; add(c ? 0.45 : -0.45, c ? 0.35 : -0.35, c); }
      else if (preset === 'circle') { const c = i % 2, r = c ? Math.random() * 0.35 : 0.6 + Math.random() * 0.3, a = Math.random() * Math.PI * 2; add(r * Math.cos(a), r * Math.sin(a), c); }
      else if (preset === 'xor') { const x = Math.random() * 2 - 1, y = Math.random() * 2 - 1; add(x, y, x * y > 0 ? 1 : 0); }
      else if (preset === 'spiral') { const c = i % 2, t = (i >> 1) / (N / 2) * 2.4 * Math.PI, r = 0.12 + t / (2.4 * Math.PI) * 0.8, a = t + c * Math.PI; add(r * Math.cos(a), r * Math.sin(a), c); }
    }
    split(); resetNet();
  }
  function trainEpoch() {
    const Hh = net.H;
    for (const key of KEYS) net['g' + key].fill(0);
    let cnt = 0;
    for (let s = 0; s < n; s++) {
      if (test[s]) continue; cnt++;
      const out = forward(net, px[s], py[s]);
      const dO = out - lab[s];
      net.gb3[0] += dO;
      for (let j = 0; j < Hh; j++) { net.gW3[j] += dO * net.h2[j]; net.d2[j] = dO * net.W3[j] * (1 - net.h2[j] * net.h2[j]); net.gb2[j] += net.d2[j]; }
      for (let i = 0; i < Hh; i++) { let s2 = 0; for (let j = 0; j < Hh; j++) { net.gW2[i * Hh + j] += net.d2[j] * net.h1[i]; s2 += net.W2[i * Hh + j] * net.d2[j]; } net.d1[i] = s2 * (1 - net.h1[i] * net.h1[i]); net.gb1[i] += net.d1[i]; net.gW1[i] += net.d1[i] * px[s]; net.gW1[Hh + i] += net.d1[i] * py[s]; }
    }
    if (!cnt) return;
    net.t++;
    const b1 = 0.9, b2 = 0.999, c1 = 1 - Math.pow(b1, net.t), c2 = 1 - Math.pow(b2, net.t);
    for (const key of KEYS) {
      const W = net[key], Gr = net['g' + key], M = net['m' + key], V = net['v' + key];
      for (let i = 0; i < W.length; i++) { const g = Gr[i] / cnt; M[i] = b1 * M[i] + (1 - b1) * g; V[i] = b2 * V[i] + (1 - b2) * g * g; W[i] -= lr * (M[i] / c1) / (Math.sqrt(V[i] / c2) + 1e-8); }
    }
    epoch++;
  }
  const L = { tr: 0, te: 0, acc: 0 };
  function losses() {
    let a = 0, an = 0, b = 0, bn = 0, ok = 0;
    for (let s = 0; s < n; s++) { const o = clamp(forward(net, px[s], py[s]), 1e-7, 1 - 1e-7), l = -(lab[s] ? Math.log(o) : Math.log(1 - o)); if (test[s]) { b += l; bn++; if ((o > 0.5) === !!lab[s]) ok++; } else { a += l; an++; } }
    L.tr = an ? a / an : 0; L.te = bn ? b / bn : NaN; L.acc = bn ? ok / bn : NaN;
  }

  // ---- the scene ----
  // input x → world x, input y → world −z (so "up" in the data is away from the viewer)
  const WX = (v) => v * SQ, WZ = (v) => -v * SQ;
  const base = new THREE.Mesh(new THREE.BoxGeometry(SQ * 2 + 0.3, 0.1, SQ * 2 + 0.3), new THREE.MeshStandardMaterial({ color: 0x1e2440, roughness: 0.5, metalness: 0.2 }));
  base.position.y = -0.05; base.receiveShadow = true; scene.add(base);
  const frame = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(SQ * 2, HS, SQ * 2)), new THREE.LineBasicMaterial({ color: 0x6366f1, transparent: true, opacity: 0.35 }));
  frame.position.y = HS / 2; scene.add(frame);

  const surfGeo = new THREE.PlaneGeometry(SQ * 2, SQ * 2, G, G); surfGeo.rotateX(-Math.PI / 2);
  const surfCol = new Float32Array(surfGeo.attributes.position.count * 3);
  surfGeo.setAttribute('color', new THREE.BufferAttribute(surfCol, 3));
  const surfMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.45, metalness: 0.05, side: THREE.DoubleSide, transparent: true, opacity: 0.82, depthWrite: false });
  // a little self-light so the steep back faces of a cliff never turn black
  surfMat.onBeforeCompile = (sh) => { sh.fragmentShader = sh.fragmentShader.replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n totalEmissiveRadiance += vColor * 0.28;'); };
  const surf = new THREE.Mesh(surfGeo, surfMat); surf.renderOrder = 2; scene.add(surf);
  const vals = new Float32Array((G + 1) * (G + 1));

  // decision boundary: on the landscape at one half, and its shadow on the floor
  const bPos = new Float32Array(G * G * 4 * 3), fPos = new Float32Array(G * G * 4 * 3);
  const bGeo = new THREE.BufferGeometry(); bGeo.setAttribute('position', new THREE.BufferAttribute(bPos, 3));
  const fGeo = new THREE.BufferGeometry(); fGeo.setAttribute('position', new THREE.BufferAttribute(fPos, 3));
  const bLine = new THREE.LineSegments(bGeo, new THREE.LineBasicMaterial({ color: 0xffffff, toneMapped: false })); bLine.frustumCulled = false; bLine.renderOrder = 3; scene.add(bLine);
  const fLine = new THREE.LineSegments(fGeo, new THREE.LineBasicMaterial({ color: 0xc7d2fe, transparent: true, opacity: 0.7 })); fLine.frustumCulled = false; scene.add(fLine);
  const half = new THREE.Mesh(new THREE.PlaneGeometry(SQ * 2, SQ * 2), new THREE.MeshBasicMaterial({ color: 0xa5b4fc, transparent: true, opacity: 0.07, depthWrite: false, side: THREE.DoubleSide }));
  half.rotation.x = -Math.PI / 2; half.position.y = HS / 2; scene.add(half);

  // the points: training ones are glossy beads, test ones are rings
  const beadMat = new THREE.MeshStandardMaterial({ roughness: 0.3, metalness: 0.1 });
  const beads = new THREE.InstancedMesh(new THREE.SphereGeometry(0.075, 16, 12), beadMat, MAXN); beads.castShadow = true; scene.add(beads);
  const rings = new THREE.InstancedMesh(new THREE.TorusGeometry(0.08, 0.024, 8, 20), new THREE.MeshStandardMaterial({ roughness: 0.3 }), MAXN); scene.add(rings);
  beads.setColorAt(0, ORANGE); rings.setColorAt(0, ORANGE);
  const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI / 2, 0, 0)), V3 = new THREE.Vector3(), ONE = new THREE.Vector3(1, 1, 1);
  function placePoints() {
    let nb = 0, nr = 0;
    for (let i = 0; i < n; i++) {
      V3.set(WX(px[i]), lab[i] ? HS : 0.075, WZ(py[i]));
      if (test[i]) { rings.setMatrixAt(nr, M4.compose(V3, Q, ONE)); rings.setColorAt(nr, lab[i] ? ORANGE : BLUE); nr++; }
      else { beads.setMatrixAt(nb, M4.makeTranslation(V3.x, V3.y, V3.z)); beads.setColorAt(nb, lab[i] ? ORANGE : BLUE); nb++; }
    }
    beads.count = nb; rings.count = nr;
    beads.instanceMatrix.needsUpdate = true; rings.instanceMatrix.needsUpdate = true;
    beads.instanceColor.needsUpdate = true; rings.instanceColor.needsUpdate = true;
  }

  function updateSurface() {
    const pos = surfGeo.attributes.position, c = new THREE.Color();
    for (let j = 0; j <= G; j++) for (let i = 0; i <= G; i++) {
      const k = j * (G + 1) + i, x = i / G * 2 - 1, y = 1 - j / G * 2;
      const o = forward(net, x, y); vals[k] = o;
      pos.setY(k, o * HS);
      c.copy(BLUE).lerp(ORANGE, o); surfCol[k * 3] = c.r; surfCol[k * 3 + 1] = c.g; surfCol[k * 3 + 2] = c.b;
    }
    pos.needsUpdate = true; surfGeo.attributes.color.needsUpdate = true; surfGeo.computeVertexNormals();
    // marching squares at 0.5
    let m = 0;
    const at = (i, j) => vals[j * (G + 1) + i] - 0.5;
    const edge = (i0, j0, i1, j1) => { const a = at(i0, j0), b = at(i1, j1), t = a / (a - b); return [(i0 + (i1 - i0) * t) / G * 2 - 1, 1 - (j0 + (j1 - j0) * t) / G * 2]; };
    const seg = (p, q) => {
      bPos[m] = WX(p[0]); bPos[m + 1] = HS / 2 + 0.01; bPos[m + 2] = WZ(p[1]); bPos[m + 3] = WX(q[0]); bPos[m + 4] = HS / 2 + 0.01; bPos[m + 5] = WZ(q[1]);
      fPos[m] = WX(p[0]); fPos[m + 1] = 0.006; fPos[m + 2] = WZ(p[1]); fPos[m + 3] = WX(q[0]); fPos[m + 4] = 0.006; fPos[m + 5] = WZ(q[1]);
      m += 6;
    };
    for (let j = 0; j < G; j++) for (let i = 0; i < G; i++) {
      const s0 = at(i, j) > 0, s1 = at(i + 1, j) > 0, s2 = at(i + 1, j + 1) > 0, s3 = at(i, j + 1) > 0;
      const crosses = [];
      if (s0 !== s1) crosses.push(edge(i, j, i + 1, j));
      if (s1 !== s2) crosses.push(edge(i + 1, j, i + 1, j + 1));
      if (s2 !== s3) crosses.push(edge(i + 1, j + 1, i, j + 1));
      if (s3 !== s0) crosses.push(edge(i, j + 1, i, j));
      if (crosses.length >= 2) seg(crosses[0], crosses[1]);
      if (crosses.length === 4) seg(crosses[2], crosses[3]);
    }
    bGeo.setDrawRange(0, m / 3); fGeo.setDrawRange(0, m / 3);
    bGeo.attributes.position.needsUpdate = true; fGeo.attributes.position.needsUpdate = true;
  }

  // the network itself, standing beside the landscape: neurons and weighted connections
  const netG = new THREE.Group(); scene.add(netG);
  const nodeGeo = new THREE.SphereGeometry(0.11, 20, 14), nodeMat = new THREE.MeshStandardMaterial({ color: 0xe0e7ff, roughness: 0.35, emissive: 0x4338ca, emissiveIntensity: 0.25 });
  const edgeGeo = new THREE.CylinderGeometry(1, 1, 1, 6, 1, true); edgeGeo.translate(0, 0.5, 0); edgeGeo.rotateX(Math.PI / 2);
  const edgeMat = new THREE.MeshBasicMaterial({ toneMapped: false, transparent: true, opacity: 0.75, depthWrite: false });
  const edges = new THREE.InstancedMesh(edgeGeo, edgeMat, 2 * HMAX + HMAX * HMAX + HMAX); edges.frustumCulled = false; netG.add(edges);
  const nodes = new THREE.InstancedMesh(nodeGeo, nodeMat, 2 + 2 * HMAX + 1); nodes.castShadow = true; netG.add(nodes);
  const nodePos = [];
  function buildNetGraph() {
    const cols = [2, net.H, net.H, 1], W = 3.0, Hgt = 3.0;
    nodePos.length = 0; let k = 0;
    for (let c = 0; c < 4; c++) { const col = []; for (let i = 0; i < cols[c]; i++) { const p = new THREE.Vector3(c * W / 3, Hgt / 2 - (i + 0.5) * Hgt / cols[c] + 0.0, 0); col.push(p); nodes.setMatrixAt(k++, M4.makeTranslation(p.x, p.y, p.z)); } nodePos.push(col); }
    nodes.count = k; nodes.instanceMatrix.needsUpdate = true;
  }
  const eCol = new THREE.Color(), up = new THREE.Vector3(), dir = new THREE.Vector3(), qq = new THREE.Quaternion(), sc = new THREE.Vector3(), Z = new THREE.Vector3(0, 0, 1);
  function updateEdges() {
    const Hh = net.H; let k = 0;
    for (let c = 0; c < 3; c++) for (let i = 0; i < nodePos[c].length; i++) for (let j = 0; j < nodePos[c + 1].length; j++) {
      const wv = c === 0 ? net.W1[i * Hh + j] : c === 1 ? net.W2[i * Hh + j] : net.W3[i];
      const a = nodePos[c][i], b = nodePos[c + 1][j];
      dir.subVectors(b, a); const len = dir.length(); dir.divideScalar(len);
      qq.setFromUnitVectors(Z, dir); const r = Math.min(0.022, 0.003 + Math.abs(wv) * 0.008);
      edges.setMatrixAt(k, M4.compose(up.copy(a), qq, sc.set(r, r, len)));
      eCol.copy(wv > 0 ? ORANGE : BLUE).multiplyScalar(0.4 + Math.min(1.2, Math.abs(wv) * 0.6)); edges.setColorAt(k, eCol);
      k++;
    }
    edges.count = k; edges.instanceMatrix.needsUpdate = true; if (edges.instanceColor) edges.instanceColor.needsUpdate = true;
  }

  // ---- panel ----
  const hud = createHud(stage);
  const badge = hud.badge('Press Train and watch the loss fall', '#7c3aed');
  const panel = createPanel(stage, { title: 'Train a network' });
  const [trainB] = panel.buttonRow([
    { label: 'Train', icon: 'play_arrow', onClick: () => { training = !training; trainB.setLabel(training ? 'Pause' : 'Train'); } },
    { label: 'New weights', icon: 'refresh', variant: 'ghost', onClick: resetNet },
  ]);
  panel.chips({ label: 'Data', options: [{ value: 'blobs', label: 'Two groups' }, { value: 'circle', label: 'Circle' }, { value: 'xor', label: 'XOR' }, { value: 'spiral', label: 'Spiral' }, { value: 'none', label: 'Empty' }], value: preset, onChange: (v) => { preset = v; makeData(); } });
  panel.chips({ label: 'Tap the floor to add', options: [{ value: '1', label: 'orange points', color: '#f08c00' }, { value: '0', label: 'blue points', color: '#2563eb' }], value: '1', onChange: (v) => { cls = +v; } });
  panel.slider({ label: 'Hidden neurons per layer', min: 2, max: HMAX, step: 1, value: H, format: (v) => `${v}`, onChange: (v) => { H = v; resetNet(); } });
  panel.slider({ label: 'Learning rate', min: -3, max: -0.7, step: 0.1, value: Math.log10(lr), format: (v) => Math.pow(10, v).toFixed(3), onChange: (v) => { lr = Math.pow(10, v); } });
  panel.slider({ label: 'Noise in the data', min: 0, max: 0.5, step: 0.05, value: noise, format: (v) => v.toFixed(2), onChange: (v) => { noise = v; makeData(); } });
  panel.toggle({ label: 'Hold back 25 % as a test set', value: true, onChange: (v) => { holdout = v; split(); } });
  const lossCard = canvasCard(panel.body, 1.9);
  const st = panel.stats([{ key: 'ep', label: 'Epochs' }, { key: 'tr', label: 'Training loss' }, { key: 'te', label: 'Test loss' }, { key: 'acc', label: 'Test accuracy' }]);
  panel.info('Each epoch the network guesses every training point, measures how wrong it was (the loss), and nudges every weight a little downhill (gradient descent). If test loss starts rising while training loss keeps falling, it is memorising: overfitting.');

  function drawLoss() {
    const { g, w, h } = lossCard.ctx();
    const ix = 34, iy = 22, iw = w - 44, ih = h - 40;
    const e1 = Math.max(50, epoch), ymax = Math.max(0.8, trL.length ? Math.min(2, Math.max(trL[0][1], teL.length ? teL[0][1] : 0) * 1.1) : 0.8);
    const X = (e) => ix + e / e1 * iw, Y = (v) => iy + ih - Math.min(1, v / ymax) * ih;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('Loss (lower is better)', 10, 14);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.lineWidth = 1; g.strokeRect(ix, iy, iw, ih);
    for (const [arr, col] of [[trL, '#a78bfa'], [teL, '#fb923c']]) { g.strokeStyle = col; g.lineWidth = 2; g.beginPath(); arr.forEach(([e, v], i) => (i ? g.lineTo(X(e), Y(v)) : g.moveTo(X(e), Y(v)))); g.stroke(); }
    g.font = '700 10px Poppins, system-ui, sans-serif'; g.fillStyle = '#a78bfa'; g.fillText('training', ix + iw - 92, iy + 12); g.fillStyle = '#fb923c'; g.fillText('test', ix + iw - 30, iy + 12);
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#8ea0c2'; g.textAlign = 'right'; g.fillText(ymax.toFixed(1), ix - 4, iy + 8); g.fillText('0', ix - 4, iy + ih);
    g.textAlign = 'center'; g.fillText(`epoch (0 to ${e1})`, ix + iw / 2, h - 4);
  }

  // ---- input: tap the floor to add, drag points ----
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), hit = new THREE.Vector3(), plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  let held = -1, downAt = null;
  function setRay(e) { const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); }
  function pickPoint() {
    let best = -1, bd = 1e9; const v = new THREE.Vector3(), r = engine.canvas.getBoundingClientRect();
    for (let i = 0; i < n; i++) {
      v.set(WX(px[i]), lab[i] ? HS : 0.075, WZ(py[i])).project(camera);
      const sx = (v.x + 1) / 2 * r.width, sy = (1 - v.y) / 2 * r.height, d = Math.hypot(sx - (ndc.x + 1) / 2 * r.width, sy - (1 - ndc.y) / 2 * r.height);
      if (d < bd) { bd = d; best = i; }
    }
    return bd < 14 ? best : -1;
  }
  function onDown(e) {
    setRay(e); downAt = [e.clientX, e.clientY];
    const i = pickPoint();
    if (i < 0) return;
    held = i; controls.enabled = false; e.stopImmediatePropagation(); engine.canvas.setPointerCapture && engine.canvas.setPointerCapture(e.pointerId);
  }
  function onMove(e) {
    if (held < 0) return;
    setRay(e); plane.constant = -(lab[held] ? HS : 0.075);
    if (ray.ray.intersectPlane(plane, hit)) { px[held] = clamp(hit.x / SQ, -1, 1); py[held] = clamp(-hit.z / SQ, -1, 1); dirty = true; }
  }
  function onUp(e) {
    const tap = downAt && Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) < 6;
    if (held >= 0) { held = -1; controls.enabled = true; }
    else if (tap && n < MAXN) {
      setRay(e); plane.constant = 0;
      if (ray.ray.intersectPlane(plane, hit) && Math.abs(hit.x) <= SQ && Math.abs(hit.z) <= SQ) {
        px[n] = hit.x / SQ; py[n] = -hit.z / SQ; lab[n] = cls; test[n] = holdout && ((n * 7919) % 4 === 0) ? 1 : 0; n++; dirty = true;
      }
    }
    downAt = null;
  }
  engine.canvas.addEventListener('pointerdown', onDown, true);
  engine.canvas.addEventListener('pointermove', onMove);
  engine.canvas.addEventListener('pointerup', onUp);

  // ---- layout: the network stands to the right, or behind on narrow screens ----
  let narrow = null, fit = null;
  function layout() {
    const nw = stage.clientWidth < 640;
    if (nw === narrow) return;
    narrow = nw;
    if (nw) { netG.position.set(-1.5, HS + 1.9, -SQ - 0.6); netG.rotation.y = 0; fit = framer(stage, camera, controls, { width: 6.6, height: 8, center: [0, 1.2, 0] }); }
    else { netG.position.set(SQ + 1.2, 1.9, -0.4); netG.rotation.y = -0.3; fit = framer(stage, camera, controls, { width: 13.6, height: 6.5, center: [1.1, 0.9, 0] }); }
  }

  let dirty = true, tick = 0;
  makeData();
  engine.setUpdate((dt) => {
    layout(); fit();
    if (training) for (let i = 0; i < 6; i++) trainEpoch();
    if (training || dirty) {
      losses();
      if (training) { trL.push([epoch, L.tr]); if (!isNaN(L.te)) teL.push([epoch, L.te]); if (trL.length > 900) { trL.splice(0, 300); teL.splice(0, 300); } }
      updateSurface(); placePoints(); updateEdges(); dirty = false;
    }
    controls.update(dt);
    if ((tick++ & 1) === 0) drawLoss();
    st.ep.set(String(epoch)); st.tr.set(L.tr.toFixed(3)); st.te.set(isNaN(L.te) ? '—' : L.te.toFixed(3)); st.acc.set(isNaN(L.acc) ? '—' : `${Math.round(L.acc * 100)} %`);
    badge.set(!training ? (epoch ? 'Paused. Add points or change the network, then train again' : 'Press Train and watch the landscape bend to the points')
      : teL.length > 50 && L.te > L.tr * 1.8 ? 'Test loss is much higher than training loss: overfitting' : `Epoch ${epoch}: loss ${L.tr.toFixed(3)}`);
  });
  engine.start();

  stage.__ml = { train: () => { training = true; trainB.setLabel('Pause'); }, stats: () => [epoch, L.tr, L.te, L.acc], preset: (v) => { preset = v; makeData(); } };
  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown, true); engine.canvas.removeEventListener('pointermove', onMove); engine.canvas.removeEventListener('pointerup', onUp);
      beads.dispose(); rings.dispose(); edges.dispose(); nodes.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__ml;
    },
  };
}
