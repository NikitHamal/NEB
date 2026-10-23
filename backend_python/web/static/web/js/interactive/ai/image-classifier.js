/**
 * Teaching machines to see, in 3D — draw a digit on the tablet. Beside it the drawing becomes what
 * the computer actually gets: a 28 × 28 grid of brightness numbers (0–255), shown as a city of
 * pillars whose heights are those numbers. The grid is cropped and centred by its centre of mass
 * the way the MNIST dataset is prepared; a nearest-template classifier compares it with digits
 * rendered in several typefaces (cosine similarity on lightly blurred pixels) and a softmax turns
 * the similarities into the ten probability columns. A confusion matrix from a held-out test set
 * shows which digits it mixes up.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { makeLabelSprite } from '../core/engine.js';
import { canvasCard } from '../space/space3d/kit.js';
import { label } from '../physics/physics3d/field.js';
import { createStudio, framer, THREE } from './ai3d/stage.js';

const N = 28, D = N * N;
const FONTS = ['700 22px Poppins, sans-serif', '400 23px Georgia, serif', '600 22px ui-monospace, monospace', '500 22px system-ui, sans-serif', 'italic 600 22px Georgia, serif'];

function prep(src, out) {
  let minX = N, minY = N, maxX = -1, maxY = -1, sum = 0;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const v = src[y * N + x]; if (v > 0.1) { minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y); } sum += v; }
  out.fill(0);
  if (maxX < 0 || sum < 1) return false;
  const bw = maxX - minX + 1, bh = maxY - minY + 1, s = 20 / Math.max(bw, bh);
  const tmp = new Float32Array(D);
  let cx = 0, cy = 0, m = 0;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const sx = minX + (x - (N - bw * s) / 2) / s, sy = minY + (y - (N - bh * s) / 2) / s;
    const ix = Math.floor(sx), iy = Math.floor(sy);
    if (ix < minX || iy < minY || ix > maxX || iy > maxY) continue;
    const v = src[iy * N + ix]; tmp[y * N + x] = v; cx += x * v; cy += y * v; m += v;
  }
  const dx = Math.round(N / 2 - 0.5 - cx / m), dy = Math.round(N / 2 - 0.5 - cy / m);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const sx = x - dx, sy = y - dy; if (sx >= 0 && sy >= 0 && sx < N && sy < N) out[y * N + x] = tmp[sy * N + sx]; }
  // light blur, then normalise to unit length
  const b = new Float32Array(D);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { let s2 = 0, w = 0; for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) { const xx = x + i, yy = y + j; if (xx >= 0 && yy >= 0 && xx < N && yy < N) { const ww = i === 0 && j === 0 ? 4 : i === 0 || j === 0 ? 2 : 1; s2 += out[yy * N + xx] * ww; w += ww; } } b[y * N + x] = s2 / w; }
  let L = 0; for (let i = 0; i < D; i++) L += b[i] * b[i]; L = Math.sqrt(L) || 1;
  for (let i = 0; i < D; i++) out[i] = b[i] / L;
  return true;
}
function render(digit, font, rot, scale, thick) {
  const c = document.createElement('canvas'); c.width = c.height = N;
  const g = c.getContext('2d');
  g.fillStyle = '#000'; g.fillRect(0, 0, N, N);
  g.translate(N / 2, N / 2); g.rotate(rot); g.scale(scale, scale);
  g.font = font; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#fff'; g.strokeStyle = '#fff'; g.lineWidth = thick;
  g.fillText(String(digit), 0, 1); if (thick > 0) g.strokeText(String(digit), 0, 1);
  const d = g.getImageData(0, 0, N, N).data, out = new Float32Array(D);
  for (let i = 0; i < D; i++) out[i] = d[i * 4] / 255;
  return out;
}

const PAD = 280;          // drawing canvas pixels
const TAB = 3.0;         // tablet screen size, world units
const CELL = 0.1;        // pillar pitch
const PH = 0.55;         // pillar height at 255
const PINK = new THREE.Color(0xdb2777), DIM = new THREE.Color(0x1e293b), LIT = new THREE.Color(0xfce7f3);

export default function init(stage) {
  const S = createStudio(stage, { camera: [0.4, 6.4, 7.8], target: [0.2, 0.6, 0], maxDistance: 22 });
  if (!S) return null;
  const { engine, scene, camera, controls } = S;

  // ---- classifier (as in the classic version) ----
  const raw = new Float32Array(D), vec = new Float32Array(D);
  const probs = new Float32Array(10), sims = new Float32Array(10);
  const templates = [], conf = new Int16Array(100);
  let has = false, brush = 1.6, showNums = true, testAcc = 0;
  for (let dgt = 0; dgt < 10; dgt++) for (let f = 0; f < FONTS.length; f++) for (const r of [-0.12, 0.08]) { const v = new Float32Array(D); if (prep(render(dgt, FONTS[f], r, 1, f % 2 ? 1.6 : 0.6), v)) templates.push({ d: dgt, v }); }
  function classify(v, out) {
    sims.fill(-1);
    for (let t = 0; t < templates.length; t++) { const T2 = templates[t].v; let s = 0; for (let i = 0; i < D; i++) s += T2[i] * v[i]; const d = templates[t].d; if (s > sims[d]) sims[d] = s; }
    let mx = -1e9; for (let d = 0; d < 10; d++) mx = Math.max(mx, sims[d]);
    let z = 0; for (let d = 0; d < 10; d++) { out[d] = Math.exp((sims[d] - mx) * 30); z += out[d]; }
    for (let d = 0; d < 10; d++) out[d] /= z;
  }
  (function test() {
    const v = new Float32Array(D), p = new Float32Array(10); let ok = 0, tot = 0;
    for (let dgt = 0; dgt < 10; dgt++) for (let rep = 0; rep < 8; rep++) {
      const f = FONTS[(rep * 3 + dgt) % FONTS.length], rot = (Math.random() - 0.5) * 0.5, sc = 0.8 + Math.random() * 0.35, th = Math.random() * 2.2;
      if (!prep(render(dgt, f, rot, sc, th), v)) continue;
      classify(v, p); let am = 0; for (let d = 1; d < 10; d++) if (p[d] > p[am]) am = d;
      conf[dgt * 10 + am]++; tot++; if (am === dgt) ok++;
    }
    testAcc = ok / Math.max(1, tot);
  })();

  // ---- the tablet: a dark glass screen on a stand, tilted to the viewer ----
  const pad = document.createElement('canvas'); pad.width = pad.height = PAD;
  const pg = pad.getContext('2d'); pg.fillStyle = '#000'; pg.fillRect(0, 0, PAD, PAD);
  const small = document.createElement('canvas'); small.width = small.height = N;
  const sg = small.getContext('2d', { willReadFrequently: true });
  const padTex = new THREE.CanvasTexture(pad); padTex.colorSpace = THREE.SRGBColorSpace; padTex.anisotropy = 8;
  const tablet = new THREE.Group(); scene.add(tablet);
  const shell = new THREE.Mesh(new THREE.BoxGeometry(TAB + 0.36, 0.14, TAB + 0.36), new THREE.MeshStandardMaterial({ color: 0x0b0f1a, roughness: 0.35, metalness: 0.4 }));
  shell.castShadow = true; tablet.add(shell);
  const screenMat = new THREE.MeshStandardMaterial({ map: padTex, emissive: 0xffffff, emissiveMap: padTex, emissiveIntensity: 0.9, roughness: 0.15 });
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(TAB, TAB), screenMat); screen.rotation.x = -Math.PI / 2; screen.position.y = 0.072; tablet.add(screen);
  const gridLines = new THREE.GridHelper(TAB, N, 0x334155, 0x1e293b); gridLines.position.y = 0.074; gridLines.material.transparent = true; gridLines.material.opacity = 0.16; tablet.add(gridLines);
  const leg = new THREE.Mesh(new THREE.BoxGeometry(TAB * 0.8, 0.06, 1.2), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.4, metalness: 0.5 }));
  leg.castShadow = true; scene.add(leg);
  const hintTag = makeLabelSprite('draw here', { fontSize: 40, bg: 'rgba(219,39,119,0.9)', scale: 0.32 }); tablet.add(hintTag); hintTag.position.set(0, 0.4, 0);

  // ---- the pillar city: one pillar per pixel ----
  const pillarGeo = new THREE.BoxGeometry(CELL * 0.86, 1, CELL * 0.86); pillarGeo.translate(0, 0.5, 0);
  const pillars = new THREE.InstancedMesh(pillarGeo, new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 0.1 }), D);
  pillars.castShadow = true; pillars.receiveShadow = true; scene.add(pillars);
  const plinth = new THREE.Mesh(new THREE.BoxGeometry(N * CELL + 0.2, 0.08, N * CELL + 0.2), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.5 }));
  plinth.receiveShadow = true; scene.add(plinth);
  const pick = new THREE.Mesh(new THREE.BoxGeometry(CELL, 1, CELL), new THREE.MeshBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.35, depthWrite: false })); pick.visible = false; scene.add(pick);
  const cityTag = makeLabelSprite('28 × 28 numbers, 0 to 255', { fontSize: 40, scale: 0.3 }); scene.add(cityTag);

  // ---- ten probability columns ----
  const bars = [], barLbls = [];
  const barGeo = new THREE.CylinderGeometry(0.16, 0.16, 1, 24); barGeo.translate(0, 0.5, 0);
  for (let d = 0; d < 10; d++) {
    const m = new THREE.Mesh(barGeo, new THREE.MeshStandardMaterial({ color: 0x7c3aed, emissive: 0x7c3aed, emissiveIntensity: 0.25, roughness: 0.3 }));
    m.castShadow = true; scene.add(m); bars.push(m);
    const l = makeLabelSprite(String(d), { fontSize: 44, bg: 'rgba(15,23,42,0.85)', scale: 0.26 }); scene.add(l); barLbls.push(l);
  }
  const probTag = makeLabelSprite('probability', { fontSize: 40, scale: 0.3 }); scene.add(probTag);
  const bestLbl = label(stage, camera), cellLbl = label(stage, camera);

  // ---- layout ----
  const tabPos = new THREE.Vector3(), cityPos = new THREE.Vector3(), barPos = new THREE.Vector3();
  let narrow = null, fit = null;
  function layout() {
    const nw = stage.clientWidth < 640;
    if (nw === narrow) return;
    narrow = nw;
    if (nw) { tabPos.set(0, 0.45, 2.5); cityPos.set(-0.9, 0, -1.4); barPos.set(1.5, 0, -1.4); fit = framer(stage, camera, controls, { width: 5.8, height: 9, center: [0, 0.6, 0.4] }); }
    else { tabPos.set(-3.6, 0.9, 0.4); cityPos.set(0.2, 0, 0); barPos.set(3.0, 0, 0.6); fit = framer(stage, camera, controls, { width: 11.8, height: 5.5, center: [-0.5, 0.6, 0.2] }); }
    tablet.position.copy(tabPos); tablet.rotation.set(nw ? 0.25 : 0.62, 0, 0);
    leg.visible = !nw; leg.position.set(tabPos.x, 0.42, tabPos.z - 0.95); leg.rotation.x = -0.9;
    plinth.position.set(cityPos.x, 0.04, cityPos.z); cityTag.position.set(cityPos.x, 0.25, cityPos.z + N * CELL / 2 + 0.35);
    for (let d = 0; d < 10; d++) {
      const x = barPos.x + (d % 5) * 0.46 - 0.92, z = barPos.z + (d < 5 ? -0.5 : 0.5);
      bars[d].position.set(x, 0, z); barLbls[d].position.set(x, 0.14, z + 0.3);
    }
    probTag.position.set(barPos.x, 0.12, barPos.z + 1.2);
    placePillars();
  }

  const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), P = new THREE.Vector3(), SC = new THREE.Vector3(), C = new THREE.Color();
  function placePillars() {
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const i = y * N + x, v = raw[i];
      P.set(cityPos.x + (x - N / 2 + 0.5) * CELL, 0.08, cityPos.z + (y - N / 2 + 0.5) * CELL);
      pillars.setMatrixAt(i, M4.compose(P, Q, SC.set(1, 0.02 + v * PH, 1)));
      pillars.setColorAt(i, C.copy(DIM).lerp(LIT, v));
    }
    pillars.instanceMatrix.needsUpdate = true; pillars.instanceColor.needsUpdate = true;
  }

  function update() {
    sg.clearRect(0, 0, N, N); sg.imageSmoothingEnabled = true; sg.drawImage(pad, 0, 0, N, N);
    const d = sg.getImageData(0, 0, N, N).data;
    for (let i = 0; i < D; i++) raw[i] = d[i * 4] / 255;
    has = prep(raw, vec);
    if (has) classify(vec, probs); else probs.fill(0);
    padTex.needsUpdate = true; placePillars();
  }
  function clear() { pg.fillStyle = '#000'; pg.fillRect(0, 0, PAD, PAD); update(); }

  // ---- panel ----
  const hud = createHud(stage);
  const badge = hud.badge('Draw a digit from 0 to 9 on the tablet', '#db2777');
  const panel = createPanel(stage, { title: 'Digit classifier' });
  panel.buttonRow([{ label: 'Clear', icon: 'delete', variant: 'ghost', onClick: clear }]);
  panel.slider({ label: 'Pen thickness', min: 0.8, max: 2.6, step: 0.1, value: brush, format: (v) => v.toFixed(1), onChange: (v) => { brush = v; } });
  panel.toggle({ label: 'Show pixel numbers', value: true, onChange: (v) => { showNums = v; } });
  const cm = canvasCard(panel.body, 1.15);
  const st = panel.stats([{ key: 'guess', label: 'Best guess' }, { key: 'conf', label: 'Confidence' }, { key: 'test', label: 'Accuracy on the test set' }, { key: 'templ', label: 'Templates stored' }]);
  panel.info('To the computer an image is just numbers. This simple classifier compares those numbers with stored examples; modern convolutional networks instead learn small pattern detectors (edges, loops, corners) that work wherever the pattern appears, which is why they are so good at images.');
  st.test.set(`${Math.round(testAcc * 100)} %`); st.templ.set(String(templates.length));
  function drawConfusion() {
    const { g, w, h } = cm.ctx();
    const s = Math.min(w - 40, h - 44), c = s / 10, x0 = 26, y0 = 22;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('Confusion matrix (test set)', 10, 14);
    let mx = 1; for (let i = 0; i < 100; i++) mx = Math.max(mx, conf[i]);
    for (let r = 0; r < 10; r++) for (let q = 0; q < 10; q++) {
      const v = conf[r * 10 + q] / mx;
      g.fillStyle = r === q ? `rgba(34,197,94,${0.12 + 0.85 * v})` : v > 0 ? `rgba(244,63,94,${0.3 + 0.6 * v})` : 'rgba(148,163,184,0.06)';
      g.fillRect(x0 + q * c, y0 + r * c, c - 1, c - 1);
    }
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#8ea0c2'; g.textAlign = 'center';
    for (let i = 0; i < 10; i++) { g.fillText(String(i), x0 + i * c + c / 2, y0 + s + 11); g.fillText(String(i), x0 - 9, y0 + i * c + c * 0.7); }
    g.textAlign = 'right'; g.fillText('predicted →', x0 + s, y0 + s + 24);
    g.save(); g.translate(10, y0 + s / 2); g.rotate(-Math.PI / 2); g.textAlign = 'center'; g.fillText('true digit', 0, -2); g.restore();
  }
  drawConfusion();

  // ---- drawing on the tablet ----
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  let drawing = false, last = null, hoverUV = null;
  function uvAt(e) {
    const r = engine.canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera);
    const h = ray.intersectObject(screen, false)[0];
    return h ? h.uv : null;
  }
  function stroke(uv) {
    const x = uv.x * PAD, y = (1 - uv.y) * PAD;
    pg.strokeStyle = '#fff'; pg.lineCap = 'round'; pg.lineJoin = 'round'; pg.lineWidth = brush * 20;
    pg.beginPath(); pg.moveTo(last ? last[0] : x, last ? last[1] : y); pg.lineTo(x, y); pg.stroke();
    last = [x, y]; update();
  }
  function onDown(e) {
    const uv = uvAt(e);
    if (!uv) return;
    drawing = true; last = null; controls.enabled = false; e.stopImmediatePropagation();
    engine.canvas.setPointerCapture && engine.canvas.setPointerCapture(e.pointerId);
    stroke(uv);
  }
  function onMove(e) {
    const uv = uvAt(e); hoverUV = uv ? uv.clone() : null;
    engine.canvas.style.cursor = uv ? 'crosshair' : '';
    if (drawing && uv) stroke(uv);
  }
  function onUp() { if (drawing) { drawing = false; last = null; controls.enabled = true; } }
  engine.canvas.addEventListener('pointerdown', onDown, true);
  engine.canvas.addEventListener('pointermove', onMove);
  engine.canvas.addEventListener('pointerup', onUp);
  engine.canvas.addEventListener('pointerleave', () => { hoverUV = null; });

  update();
  const shown = new Float32Array(10), tmp = new THREE.Vector3();
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    layout(); fit();
    let am = 0; for (let d = 1; d < 10; d++) if (probs[d] > probs[am]) am = d;
    for (let d = 0; d < 10; d++) {
      shown[d] += (probs[d] - shown[d]) * (1 - Math.exp(-dt * 10));
      bars[d].scale.y = 0.03 + shown[d] * 2.2;
      const hot = has && d === am; bars[d].material.color.set(hot ? PINK : 0x7c3aed); bars[d].material.emissive.set(hot ? PINK : 0x7c3aed); bars[d].material.emissiveIntensity = hot ? 0.6 : 0.2;
    }
    hintTag.visible = !has;
    bestLbl.el.style.opacity = has ? '1' : '0';
    if (has) { bestLbl.el.textContent = `${am}: ${Math.round(probs[am] * 100)} %`; bestLbl.at(tmp.copy(bars[am].position).setY(bars[am].scale.y + 0.35)); }
    // pixel readout under the pointer: the same cell on the tablet and in the city
    const cell = showNums && hoverUV ? [Math.min(N - 1, Math.floor(hoverUV.x * N)), Math.min(N - 1, Math.floor((1 - hoverUV.y) * N))] : null;
    pick.visible = !!cell; cellLbl.el.style.opacity = cell ? '1' : '0';
    if (cell) {
      const v = raw[cell[1] * N + cell[0]], hgt = 0.02 + v * PH + 0.1;
      pick.position.set(cityPos.x + (cell[0] - N / 2 + 0.5) * CELL, 0.08 + hgt / 2, cityPos.z + (cell[1] - N / 2 + 0.5) * CELL); pick.scale.y = hgt;
      cellLbl.el.textContent = `pixel (${cell[0]}, ${cell[1]}) = ${Math.round(v * 255)}`; cellLbl.at(tmp.copy(pick.position).setY(0.08 + hgt + 0.25));
    }
    controls.update(dt);
    st.guess.set(has ? String(am) : '—'); st.conf.set(has ? `${Math.round(probs[am] * 100)} %` : '—');
    badge.set(has ? `I think it is a ${am} (${Math.round(probs[am] * 100)} % sure)` : 'Draw a digit from 0 to 9 on the tablet');
  });
  engine.start();

  stage.__digits = {
    draw: (dgt) => { const v = render(dgt, '700 22px Poppins, sans-serif', 0.05, 0.9, 1.2); pg.fillStyle = '#000'; pg.fillRect(0, 0, PAD, PAD); const c = document.createElement('canvas'); c.width = c.height = N; const g = c.getContext('2d'); const im = g.createImageData(N, N); for (let i = 0; i < D; i++) { const b = Math.round(v[i] * 255); im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = b; im.data[i * 4 + 3] = 255; } g.putImageData(im, 0, 0); pg.imageSmoothingEnabled = true; pg.drawImage(c, 0, 0, PAD, PAD); update(); },
    probs: () => Array.from(probs).map((p) => Math.round(p * 100)), acc: () => testAcc,
  };
  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown, true); engine.canvas.removeEventListener('pointermove', onMove); engine.canvas.removeEventListener('pointerup', onUp);
      bestLbl.remove(); cellLbl.remove(); pillars.dispose(); padTex.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__digits;
    },
  };
}
