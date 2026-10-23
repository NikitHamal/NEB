/**
 * Line of decision, in 3D — two kinds of points described by two features lie on a floor.
 * Set up your own fence with its two posts to separate them (its accuracy is counted live), then
 * let a perceptron learn. Its sum w₁x₁ + w₂x₂ + b is a tilted plane over the floor: orange where
 * it is above its zero level, blue below, and the line where it crosses that level is its decision
 * boundary (its shadow falls on the floor among the points).
 * Each step takes one misclassified point and nudges the weights, w ← w + η·y·x, tipping the plane;
 * the weight vector (the arrow) always points uphill, perpendicular to the line. On data that no
 * straight line can split (XOR) the perceptron never settles.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createStudio, framer, THREE } from './ai3d/stage.js';

const MAXN = 120;
const SQ = 2.4, ZS = 0.8, H0 = 1.0;   // the sum's zero level floats at H0 so both signs show
const ORANGE = new THREE.Color(0xf08c00), BLUE = new THREE.Color(0x2563eb);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

function clipLine(a, bb, c) {
  const pts = [];
  if (Math.abs(bb) > 1e-9) for (const x of [-1, 1]) { const y = -(a * x + c) / bb; if (y >= -1 && y <= 1) pts.push(x, y); }
  if (Math.abs(a) > 1e-9) for (const y of [-1, 1]) { const x = -(bb * y + c) / a; if (x >= -1 && x <= 1) pts.push(x, y); }
  return pts.length >= 4 ? pts : null;
}

function stripeTexture() {
  const c = document.createElement('canvas'); c.width = 64; c.height = 8; const g = c.getContext('2d');
  g.fillStyle = '#f8fafc'; g.fillRect(0, 0, 64, 8); g.fillStyle = '#0f172a'; g.fillRect(32, 0, 32, 8);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = THREE.RepeatWrapping;
  return t;
}

export default function init(stage) {
  const S = createStudio(stage, { camera: [0.6, 5.2, 7.0], target: [0, 0.6, 0], maxDistance: 20 });
  if (!S) return null;
  const { engine, scene, camera, controls } = S;
  const fit = framer(stage, camera, controls, { width: 7.4, height: 6.4, center: [0, 0.6, 0.2] });

  const px = new Float64Array(MAXN), py = new Float64Array(MAXN), lab = new Int8Array(MAXN);
  let n = 0, cls = 1, preset = 'sep';
  const mine = { ax: -0.8, ay: -0.6, bx: 0.8, by: 0.5 };
  let w1 = 0.1, w2 = -0.3, b = 0.05, eta = 0.2, steps = 0, running = false, cursor = 0, lastPick = -1, pickFlash = 0, sinceErr = 0, tick = 0;
  const show = { w1, w2, b };

  // input x₁ → world x, x₂ → world −z
  const WX = (v) => v * SQ, WZ = (v) => -v * SQ;

  const base = new THREE.Mesh(new THREE.BoxGeometry(SQ * 2 + 0.3, 0.1, SQ * 2 + 0.3), new THREE.MeshStandardMaterial({ color: 0x1e2440, roughness: 0.5, metalness: 0.2 }));
  base.position.y = -0.05; base.receiveShadow = true; scene.add(base);
  const grid = new THREE.GridHelper(SQ * 2, 8, 0x4f46e5, 0x312e81); grid.position.y = 0.004; grid.material.transparent = true; grid.material.opacity = 0.5; scene.add(grid);

  // the perceptron's sum as a plane: orange above zero, blue below
  const planeGeo = new THREE.PlaneGeometry(SQ * 2, SQ * 2, 1, 1); planeGeo.rotateX(-Math.PI / 2);
  const planeMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4, transparent: true, opacity: 0.42, side: THREE.DoubleSide, depthWrite: false });
  planeMat.onBeforeCompile = (sh) => {
    sh.vertexShader = 'varying float vH;\n' + sh.vertexShader.replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvH = (modelMatrix * vec4(transformed, 1.0)).y;');
    sh.fragmentShader = 'varying float vH;\n' + sh.fragmentShader.replace('#include <color_fragment>', `#include <color_fragment>
      float side = smoothstep(${(H0 - 0.01).toFixed(2)}, ${(H0 + 0.01).toFixed(2)}, vH);
      diffuseColor.rgb = mix(vec3(0.15, 0.39, 0.92), vec3(0.94, 0.55, 0.0), side);
      diffuseColor.a *= 0.55 + 0.35 * min(abs(vH - ${H0.toFixed(2)}) * 1.5, 1.0);`)
      .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\ntotalEmissiveRadiance += diffuseColor.rgb * 0.45;');
  };
  const sumPlane = new THREE.Mesh(planeGeo, planeMat); sumPlane.renderOrder = 3; scene.add(sumPlane);
  const planeEdge = new THREE.LineSegments(new THREE.EdgesGeometry(planeGeo), new THREE.LineBasicMaterial({ color: 0xc4b5fd, transparent: true, opacity: 0.6 })); scene.add(planeEdge);

  const zero = new THREE.Mesh(new THREE.PlaneGeometry(SQ * 2, SQ * 2), new THREE.MeshBasicMaterial({ color: 0xa5b4fc, transparent: true, opacity: 0.06, depthWrite: false, side: THREE.DoubleSide }));
  zero.rotation.x = -Math.PI / 2; zero.position.y = H0; scene.add(zero);
  // the decision line (where the plane crosses zero), its shadow on the floor, and the weight arrow
  const lineMat = new THREE.MeshBasicMaterial({ color: 0xa78bfa, toneMapped: false });
  const dLine = new THREE.Mesh(new THREE.BoxGeometry(1, 0.03, 0.05), lineMat); scene.add(dLine);
  const dShadow = new THREE.Mesh(new THREE.BoxGeometry(1, 0.01, 0.04), new THREE.MeshBasicMaterial({ color: 0x8b5cf6, transparent: true, opacity: 0.6 })); scene.add(dShadow);
  const arrow = new THREE.Group(); scene.add(arrow);
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.6, 12), lineMat); shaft.position.y = 0.3; arrow.add(shaft);
  const head = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.2, 16), lineMat); head.position.y = 0.7; arrow.add(head);
  const wTag = new THREE.Sprite(new THREE.SpriteMaterial({ map: (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); g.fillStyle = '#c4b5fd'; g.font = 'italic 800 48px Georgia, serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('w', 32, 30); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })(), depthWrite: false }));
  wTag.scale.set(0.3, 0.3, 1); wTag.position.y = 0.95; arrow.add(wTag);

  // your fence: two posts and a striped rail
  const postMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.35 });
  const posts = [0, 1].map(() => {
    const g = new THREE.Group(); scene.add(g);
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 0.5, 16), postMat); p.position.y = 0.25; p.castShadow = true; g.add(p);
    const k = new THREE.Mesh(new THREE.SphereGeometry(0.1, 20, 14), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.3 })); k.position.y = 0.55; g.add(k);
    return g;
  });
  const railTex = stripeTexture();
  const rail = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 1, 10, 1, true), new THREE.MeshStandardMaterial({ map: railTex, roughness: 0.4 }));
  rail.castShadow = true; scene.add(rail);

  // the points
  const beads = new THREE.InstancedMesh(new THREE.SphereGeometry(0.08, 18, 12), new THREE.MeshStandardMaterial({ roughness: 0.3, metalness: 0.1 }), MAXN); beads.castShadow = true; scene.add(beads);
  const wrongRings = new THREE.InstancedMesh(new THREE.TorusGeometry(0.13, 0.018, 8, 24), new THREE.MeshBasicMaterial({ color: 0xc084fc, toneMapped: false }), MAXN); scene.add(wrongRings);
  const pulse = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.02, 8, 32), new THREE.MeshBasicMaterial({ color: 0xc084fc, transparent: true, toneMapped: false })); pulse.rotation.x = Math.PI / 2; scene.add(pulse);
  beads.setColorAt(0, ORANGE);
  const M4 = new THREE.Matrix4(), QH = new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI / 2, 0, 0)), V = new THREE.Vector3(), ONE = new THREE.Vector3(1, 1, 1);

  const hud = createHud(stage);
  const badge = hud.badge('Drag the fence posts to split the colours', '#7c3aed');
  const panel = createPanel(stage, { title: 'Perceptron' });
  panel.chips({ label: 'Data', options: [{ value: 'sep', label: 'Separable' }, { value: 'overlap', label: 'Overlapping' }, { value: 'xor', label: 'XOR' }], value: 'sep', onChange: (v) => { preset = v; makeData(); } });
  panel.chips({ label: 'Tap the floor to add', options: [{ value: '1', label: 'orange', color: '#f08c00' }, { value: '-1', label: 'blue', color: '#2563eb' }], value: '1', onChange: (v) => { cls = +v; } });
  const [runB] = panel.buttonRow([
    { label: 'Learn', icon: 'play_arrow', onClick: () => setRun(!running) },
    { label: 'One step', icon: 'skip_next', variant: 'ghost', onClick: () => stepOnce() },
  ]);
  panel.button({ label: 'Forget (random weights)', icon: 'refresh', variant: 'ghost', onClick: () => { w1 = Math.random() - 0.5; w2 = Math.random() - 0.5; b = Math.random() * 0.4 - 0.2; steps = 0; sinceErr = 0; } });
  panel.slider({ label: 'Learning rate η', min: 0.02, max: 1, step: 0.02, value: eta, format: (v) => v.toFixed(2), onChange: (v) => { eta = v; } });
  const st = panel.stats([{ key: 'mine', label: 'Your fence' }, { key: 'perc', label: 'Perceptron' }, { key: 'w', label: 'Weights w₁, w₂, b' }, { key: 'steps', label: 'Updates' }]);
  panel.info('The two features are the inputs x₁ and x₂. The perceptron outputs orange when w₁x₁ + w₂x₂ + b > 0 and blue otherwise. That sum is the tilted plane; its boundary is the straight line where the plane crosses the faint zero level, with its shadow on the floor.');

  function setRun(v) { running = v; runB.setLabel(v ? 'Pause' : 'Learn'); }
  function makeData() {
    n = 0;
    const add = (x, y, c) => { if (n < MAXN) { px[n] = clamp(x, -0.95, 0.95); py[n] = clamp(y, -0.95, 0.95); lab[n] = c; n++; } };
    const g = () => (Math.random() + Math.random() + Math.random() - 1.5) * 0.5;
    for (let i = 0; i < 40; i++) {
      if (preset === 'sep') { add(-0.4 + g(), 0.35 + g(), 1); add(0.4 + g(), -0.35 + g(), -1); }
      else if (preset === 'overlap') { add(-0.2 + g() * 1.6, 0.2 + g() * 1.6, 1); add(0.2 + g() * 1.6, -0.2 + g() * 1.6, -1); }
      else { const x = Math.random() * 1.8 - 0.9, y = Math.random() * 1.8 - 0.9; if (Math.abs(x) > 0.08 && Math.abs(y) > 0.08) add(x, y, x * y > 0 ? 1 : -1); }
    }
    steps = 0; sinceErr = 0; cursor = 0;
  }
  const predict = (i) => (w1 * px[i] + w2 * py[i] + b > 0 ? 1 : -1);
  function stepOnce() {
    for (let t = 0; t < n; t++) {
      const i = (cursor + t) % n;
      if (predict(i) !== lab[i]) {
        w1 += eta * lab[i] * px[i]; w2 += eta * lab[i] * py[i]; b += eta * lab[i];
        steps++; cursor = (i + 1) % n; lastPick = i; pickFlash = 1; sinceErr = 0;
        return true;
      }
    }
    sinceErr++;
    return false;
  }
  function accLine(f) { if (!n) return 0; let ok = 0; for (let i = 0; i < n; i++) if (f(px[i], py[i]) === lab[i]) ok++; return ok / n; }
  const mineF = (x, y) => ((mine.bx - mine.ax) * (y - mine.ay) - (mine.by - mine.ay) * (x - mine.ax) > 0 ? 1 : -1);

  // ---- pointer: drag posts and points, tap the floor to add ----
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), hit = new THREE.Vector3(), floor = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  let held = null, downAt = null;
  function setRay(e) { const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); return r; }
  function nearest(e) {
    const r = setRay(e), v = new THREE.Vector3(); let best = null, bd = e.pointerType === 'touch' ? 30 : 18;
    const test = (wx, wy, wz, what) => { v.set(wx, wy, wz).project(camera); const d = Math.hypot((v.x + 1) / 2 * r.width - (e.clientX - r.left), (1 - v.y) / 2 * r.height - (e.clientY - r.top)); if (d < bd) { bd = d; best = what; } };
    test(WX(mine.ax), 0.55, WZ(mine.ay), 'a'); test(WX(mine.bx), 0.55, WZ(mine.by), 'b');
    test(WX(mine.ax), 0.25, WZ(mine.ay), 'a'); test(WX(mine.bx), 0.25, WZ(mine.by), 'b');
    for (let i = 0; i < n; i++) test(WX(px[i]), 0.08, WZ(py[i]), i);
    return best;
  }
  function onDown(e) {
    downAt = [e.clientX, e.clientY];
    const h = nearest(e);
    if (h === null) return;
    held = h; controls.enabled = false; e.stopImmediatePropagation(); engine.canvas.setPointerCapture && engine.canvas.setPointerCapture(e.pointerId);
  }
  function onMove(e) {
    if (held === null) { engine.canvas.style.cursor = nearest(e) !== null ? 'grab' : ''; return; }
    setRay(e);
    if (!ray.ray.intersectPlane(floor, hit)) return;
    const x = clamp(hit.x / SQ, -1, 1), y = clamp(-hit.z / SQ, -1, 1);
    if (held === 'a') { mine.ax = x; mine.ay = y; } else if (held === 'b') { mine.bx = x; mine.by = y; } else { px[held] = x; py[held] = y; sinceErr = 0; }
  }
  function onUp(e) {
    const tap = downAt && Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) < 6;
    if (held !== null) { held = null; controls.enabled = true; }
    else if (tap && n < MAXN) {
      setRay(e);
      if (ray.ray.intersectPlane(floor, hit) && Math.abs(hit.x) <= SQ && Math.abs(hit.z) <= SQ) { px[n] = hit.x / SQ; py[n] = -hit.z / SQ; lab[n] = cls; n++; sinceErr = 0; }
    }
    downAt = null;
  }
  engine.canvas.addEventListener('pointerdown', onDown, true);
  engine.canvas.addEventListener('pointermove', onMove);
  engine.canvas.addEventListener('pointerup', onUp);

  makeData();
  const A = new THREE.Vector3(), B = new THREE.Vector3(), Y = new THREE.Vector3(0, 1, 0), D = new THREE.Vector3();
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    fit();
    if (running) { tick += dt; while (tick > 0.12) { tick -= 0.12; stepOnce(); } if (sinceErr > 1 || steps > 2000) setRun(false); }
    const k = 1 - Math.exp(-dt * 9);
    show.w1 += (w1 - show.w1) * k; show.w2 += (w2 - show.w2) * k; show.b += (b - show.b) * k;
    pickFlash = Math.max(0, pickFlash - dt * 2);

    // the plane: height = sum, scaled so a long weight vector does not shoot off the screen
    const W1 = show.w1, W2 = show.w2, Bb = show.b, norm = Math.max(1, Math.hypot(W1, W2, Bb));
    const pos = planeGeo.attributes.position;
    for (let i = 0; i < pos.count; i++) { const x = pos.getX(i) / SQ, y = -pos.getZ(i) / SQ; pos.setY(i, H0 + ZS * (W1 * x + W2 * y + Bb) / norm); }
    pos.needsUpdate = true; planeGeo.computeVertexNormals(); planeGeo.computeBoundingSphere();
    const ep = planeEdge.geometry.attributes.position;
    for (let i = 0; i < ep.count; i++) { const x = ep.getX(i) / SQ, y = -ep.getZ(i) / SQ; ep.setY(i, H0 + ZS * (W1 * x + W2 * y + Bb) / norm); }
    ep.needsUpdate = true;

    const seg = clipLine(W1, W2, Bb);
    dLine.visible = arrow.visible = dShadow.visible = !!seg;
    if (seg) {
      A.set(WX(seg[0]), H0, WZ(seg[1])); B.set(WX(seg[2]), H0, WZ(seg[3]));
      dLine.position.copy(A).add(B).multiplyScalar(0.5); dLine.scale.x = A.distanceTo(B); dLine.rotation.y = -Math.atan2(B.z - A.z, B.x - A.x);
      dShadow.position.copy(dLine.position).setY(0.012); dShadow.scale.x = dLine.scale.x; dShadow.rotation.y = dLine.rotation.y;
      const L = Math.hypot(W1, W2) || 1;
      arrow.position.copy(dLine.position);
      D.set(W1 / L, 0, -W2 / L);
      arrow.quaternion.setFromUnitVectors(Y, D.normalize());
    }

    // fence
    posts[0].position.set(WX(mine.ax), 0, WZ(mine.ay)); posts[1].position.set(WX(mine.bx), 0, WZ(mine.by));
    A.copy(posts[0].position).setY(0.4); B.copy(posts[1].position).setY(0.4);
    const len = A.distanceTo(B); rail.position.copy(A).add(B).multiplyScalar(0.5); rail.scale.set(1, Math.max(0.01, len), 1);
    rail.quaternion.setFromUnitVectors(Y, D.subVectors(B, A).normalize()); railTex.repeat.set(Math.max(1, len / 0.3), 1);

    // points
    let nw = 0;
    for (let i = 0; i < n; i++) {
      V.set(WX(px[i]), 0.08, WZ(py[i]));
      beads.setMatrixAt(i, M4.makeTranslation(V.x, V.y, V.z)); beads.setColorAt(i, lab[i] > 0 ? ORANGE : BLUE);
      if (predict(i) !== lab[i]) wrongRings.setMatrixAt(nw++, M4.compose(V.setY(0.02), QH, ONE));
    }
    beads.count = n; wrongRings.count = nw;
    beads.instanceMatrix.needsUpdate = true; beads.instanceColor.needsUpdate = true; wrongRings.instanceMatrix.needsUpdate = true;
    pulse.visible = pickFlash > 0 && lastPick >= 0 && lastPick < n;
    if (pulse.visible) { pulse.position.set(WX(px[lastPick]), 0.03, WZ(py[lastPick])); pulse.scale.setScalar(1 + 1.6 * (1 - pickFlash)); pulse.material.opacity = pickFlash; }

    controls.update(dt);
    const am = accLine(mineF), ap = accLine((x, y) => (w1 * x + w2 * y + b > 0 ? 1 : -1)), amF = Math.max(am, 1 - am);
    st.mine.set(`${Math.round(amF * 100)} %`); st.perc.set(`${Math.round(ap * 100)} %`); st.w.set(`${w1.toFixed(2)}, ${w2.toFixed(2)}, ${b.toFixed(2)}`); st.steps.set(String(steps));
    badge.set(running ? `Learning… update ${steps}` : ap === 1 && steps ? `Converged after ${steps} updates: every point is on the right side` : preset === 'xor' && steps > 200 ? 'No straight line can split XOR: the perceptron keeps flipping' : 'Drag the fence posts to split the colours');
  });
  engine.start();

  stage.__perc = { learn: () => setRun(true), acc: () => [accLine(mineF), accLine((x, y) => (w1 * x + w2 * y + b > 0 ? 1 : -1)), steps], preset: (v) => { preset = v; makeData(); } };
  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown, true); engine.canvas.removeEventListener('pointermove', onMove); engine.canvas.removeEventListener('pointerup', onUp);
      beads.dispose(); wrongRings.dispose(); wTag.material.map.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__perc;
    },
  };
}
