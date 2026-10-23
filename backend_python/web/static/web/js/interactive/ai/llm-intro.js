/**
 * How language models work, in 3D — a tiny language model you can watch. Text is split into
 * tokens (here, words and punctuation, each with its ID in the vocabulary) that sit as tiles on a
 * track, with an empty slot for the next one. The model gives every possible next token a
 * probability from counts of what followed the same one or two tokens in its training text (a
 * trigram model backed off to bigrams); the arcs show which tokens it looked at, and the candidates
 * stand on columns as tall as their probability. Temperature reshapes those probabilities before
 * sampling. Tap a candidate to choose it yourself, or let it generate. Real models do the same
 * next-token step with a neural network that attends to the whole context.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createStudio, framer, slabCard, meshDrag, THREE } from './ai3d/stage.js';

const CORPUS = `the cat sat on the mat . the dog sat on the rug . the cat chased the mouse . the dog chased the cat .
a cat is a small animal . a dog is a loyal friend . the sun rises in the east . the moon rises at night .
the sun sets in the west . i love to learn about ai . ai is the future of learning . nebians is a place to learn .
the future is bright for students . the cat and the dog are friends . knowledge is the key to success .
the sky is blue and clear . the sky is dark at night . students learn from books and from teachers .
a model learns from data . a model predicts the next word . the next word depends on the words before it .
the mountains of nepal are tall . mount everest is the tallest mountain . the river flows to the sea .
i love the mountains of nepal . the students love to learn . the dog is happy . the cat is sleepy .`;
const TOK = CORPUS.split(/\s+/).filter(Boolean);
const VOCAB = [...new Set(TOK)].sort();
const ID = new Map(VOCAB.map((w, i) => [w, i]));
const BI = new Map(), TRI = new Map();
for (let i = 0; i < TOK.length - 1; i++) {
  const a = TOK[i], b = TOK[i + 1];
  if (!BI.has(a)) BI.set(a, new Map()); BI.get(a).set(b, (BI.get(a).get(b) || 0) + 1);
  if (i < TOK.length - 2) { const key = a + ' ' + b, c = TOK[i + 2]; if (!TRI.has(key)) TRI.set(key, new Map()); TRI.get(key).set(c, (TRI.get(key).get(c) || 0) + 1); }
}
const COLORS = ['#dbeafe', '#fce7f3', '#dcfce7', '#fef3c7', '#ede9fe', '#cffafe', '#ffe4e6', '#e0e7ff'];

const SHOW = 9;            // token tiles kept on the track
const SLOT_X = 2.2, TRACK_Z = -0.9, CAND_Z = 0.9;
const TILE_H = 0.62;

export default function init(stage) {
  const S = createStudio(stage, { camera: [0, 5.4, 7.4], target: [0, 0.8, 0.2], maxDistance: 22 });
  if (!S) return null;
  const { engine, scene, camera, controls } = S;

  let tokens = ['the', 'cat'], temp = 1, gen = false, genT = 0, genCount = 0, src = 'trigram';
  let cands = [], seen = [];

  // ---- the track, the slot, the attention arcs ----
  const track = new THREE.Mesh(new THREE.BoxGeometry(12, 0.08, 1.1), new THREE.MeshStandardMaterial({ color: 0x1e2440, roughness: 0.6, metalness: 0 }));
  track.position.set(-1.6, 0.04, TRACK_Z); track.receiveShadow = true; scene.add(track);
  const glowMat = new THREE.MeshBasicMaterial({ color: 0xa78bfa, toneMapped: false });
  const slot = new THREE.Group(); slot.position.set(SLOT_X, 0.45, TRACK_Z); slot.rotation.x = -0.45; scene.add(slot);
  for (const [w, h, x, y] of [[1.0, 0.03, 0, TILE_H / 2], [1.0, 0.03, 0, -TILE_H / 2], [0.03, TILE_H, -0.5, 0], [0.03, TILE_H, 0.5, 0]]) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.03), glowMat); m.position.set(x, y, 0); slot.add(m);
  }
  const qCard = slabCard({ w: 0.5, h: 0.4, depth: 0.02, color: 0x312e81, draw: (g, w, h) => { g.fillStyle = '#c4b5fd'; g.font = '800 72px Poppins, system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('?', w / 2, h / 2 + 4); } });
  slot.add(qCard.mesh);
  const arcs = [0, 1].map(() => { const m = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: 0xa78bfa, toneMapped: false, transparent: true })); scene.add(m); return m; });

  // ---- token tiles ----
  const tiles = new Map();   // token index → { card, x }
  function tileFor(i) {
    let t = tiles.get(i);
    if (t) return t;
    const word = tokens[i], known = ID.has(word);
    const w = 0.5 + Math.max(word.length, 3) * 0.13;
    const card = slabCard({
      w, h: TILE_H, depth: 0.06, color: new THREE.Color(COLORS[(ID.get(word) ?? 7) % COLORS.length]).getHex(),
      draw: (g, cw, ch) => {
        g.textAlign = 'center'; g.textBaseline = 'middle';
        g.font = '700 54px Poppins, system-ui, sans-serif'; g.fillStyle = '#0f172a'; g.fillText(word, cw / 2, ch * 0.42);
        g.font = '600 30px Poppins, system-ui, sans-serif'; g.fillStyle = known ? '#64748b' : '#dc2626'; g.fillText(known ? `#${ID.get(word)}` : 'unknown', cw / 2, ch * 0.8);
      },
    });
    card.mesh.rotation.x = -0.45; scene.add(card.mesh);
    t = { card, w, x: SLOT_X - 1, y: 0.45, used: 0 };
    tiles.set(i, t);
    return t;
  }
  function dropTiles() {
    for (const [i, t] of tiles) if (i >= tokens.length || i < tokens.length - SHOW - 1) { scene.remove(t.card.mesh); t.card.dispose(); tiles.delete(i); }
  }

  // ---- candidates on columns ----
  const colGeo = new THREE.CylinderGeometry(0.07, 0.07, 1, 16); colGeo.translate(0, 0.5, 0);
  const candObjs = [];
  for (let i = 0; i < 8; i++) {
    const col = new THREE.Mesh(colGeo, new THREE.MeshStandardMaterial({ color: 0x7c3aed, emissive: 0x7c3aed, emissiveIntensity: 0.35, roughness: 0.3 }));
    col.castShadow = true; scene.add(col);
    const o = { col, word: '', p: 0, shown: 0, card: null };
    o.card = slabCard({
      w: 0.92, h: 0.5, depth: 0.05, color: 0xf8fafc,
      draw: (g, cw, ch) => {
        if (!o.word) return;
        g.textAlign = 'center'; g.textBaseline = 'middle';
        g.font = '700 50px Poppins, system-ui, sans-serif'; g.fillStyle = '#0f172a'; g.fillText(o.word, cw / 2, ch * 0.4);
        g.font = '700 32px Poppins, system-ui, sans-serif'; g.fillStyle = '#7c3aed'; g.fillText(`${(o.p * 100).toFixed(1)} %`, cw / 2, ch * 0.78);
      },
    });
    o.card.mesh.userData.cand = o; scene.add(o.card.mesh);
    candObjs.push(o);
  }
  const flyer = { t: -1, from: new THREE.Vector3(), word: '', card: null };

  // ---- panel ----
  const hud = createHud(stage);
  const badge = hud.badge('Tap a candidate word to add it', '#7c3aed');
  const panel = createPanel(stage, { title: 'Next-token prediction' });
  const row = document.createElement('div'); row.className = 'ix-ctrl-row';
  const input = document.createElement('input'); input.type = 'text'; input.value = tokens.join(' '); input.setAttribute('aria-label', 'Prompt');
  input.style.cssText = 'font:500 .85rem var(--md-font,Poppins,sans-serif);padding:9px 11px;border-radius:10px;border:1px solid #d9e1ee;background:#f6f8fc;color:#172033;width:100%;box-sizing:border-box';
  const lab = document.createElement('span'); lab.className = 'ix-ctrl-label'; lab.textContent = 'Your prompt (type, then press Enter)';
  row.appendChild(lab); row.appendChild(input); panel.body.appendChild(row);
  const setPrompt = () => { clearTiles(); tokens = tokenize(input.value); if (!tokens.length) tokens = ['the']; predict(); };
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') setPrompt(); });
  input.addEventListener('change', setPrompt);
  panel.chips({ label: 'Start with', options: ['the cat', 'ai is', 'the sun', 'i love', 'a model'].map((s) => ({ value: s, label: s })), value: 'the cat', onChange: (s) => { clearTiles(); tokens = s.split(' '); sync(); } });
  panel.slider({ label: 'Temperature', min: 0.1, max: 2, step: 0.05, value: temp, format: (v) => v.toFixed(2), onChange: (v) => { temp = v; predict(); } });
  const [genB] = panel.buttonRow([
    { label: 'Generate', icon: 'auto_awesome', onClick: () => { gen = !gen; genCount = 0; genB.setLabel(gen ? 'Stop' : 'Generate'); } },
    { label: 'Undo', icon: 'undo', variant: 'ghost', onClick: () => { if (tokens.length > 1) tokens.pop(); dropTiles(); sync(); } },
  ]);
  const st = panel.stats([{ key: 'n', label: 'Tokens' }, { key: 'vocab', label: 'Vocabulary' }, { key: 'src', label: 'Prediction uses' }, { key: 'top', label: 'Most likely next' }]);
  const seenInfo = panel.info('');
  panel.info('Low temperature always picks the most likely word (safe but repetitive); high temperature flattens the odds (creative, then nonsense). Training is counting (here) or adjusting billions of weights (real models); prompting is just running the prediction again and again.');
  st.vocab.set(`${VOCAB.length} tokens`);

  function clearTiles() { for (const t of tiles.values()) { scene.remove(t.card.mesh); t.card.dispose(); } tiles.clear(); }
  function tokenize(s) { return s.toLowerCase().replace(/([.,!?])/g, ' $1 ').split(/\s+/).filter(Boolean); }
  function sync() { input.value = tokens.join(' ').replace(/ \./g, '.'); predict(); }
  function predict() {
    const counts = new Map();
    src = 'nothing it knows';
    const n = tokens.length;
    if (n >= 2 && TRI.has(tokens[n - 2] + ' ' + tokens[n - 1])) { for (const [w, c] of TRI.get(tokens[n - 2] + ' ' + tokens[n - 1])) counts.set(w, (counts.get(w) || 0) + c * 4); src = 'last 2 tokens'; }
    if (n >= 1 && BI.has(tokens[n - 1])) { for (const [w, c] of BI.get(tokens[n - 1])) counts.set(w, (counts.get(w) || 0) + c); if (src === 'nothing it knows') src = 'last token only'; }
    seen = [];
    if (n >= 2 && TRI.has(tokens[n - 2] + ' ' + tokens[n - 1])) for (const [w, c] of TRI.get(tokens[n - 2] + ' ' + tokens[n - 1])) seen.push(`"${tokens[n - 2]} ${tokens[n - 1]}" → "${w}" ${c}×`);
    if (n >= 1 && BI.has(tokens[n - 1])) for (const [w, c] of BI.get(tokens[n - 1])) seen.push(`"${tokens[n - 1]}" → "${w}" ${c}×`);
    if (!counts.size) for (const w of ['the', 'a', 'i']) counts.set(w, 1);
    const list = [...counts.entries()].map(([w, c]) => ({ w, p: Math.pow(c, 1 / temp) }));
    const z = list.reduce((s, x) => s + x.p, 0); list.forEach((x) => { x.p /= z; });
    list.sort((a, b) => b.p - a.p);
    cands = list.slice(0, 8);
    candObjs.forEach((o, i) => { const c = cands[i]; o.word = c ? c.w : ''; o.p = c ? c.p : 0; o.card.redraw(); o.card.mesh.visible = !!c; o.col.visible = !!c; });
    seenInfo.set(seen.length ? `What it saw in its training text: ${seen.slice(0, 6).join(' · ')}` : 'It has never seen these words together, so it falls back to common words.');
    buildArcs();
  }
  function sample() { const r = Math.random(); let acc = 0; for (const c of cands) { acc += c.p; if (r <= acc) return c.w; } return cands[0].w; }

  function tilePos(i) {
    // the newest token sits just left of the slot; earlier ones further left
    let x = SLOT_X - 0.55;
    for (let j = tokens.length - 1; j > i; j--) x -= tileFor(j).w + 0.12;
    return x - tileFor(i).w / 2;
  }
  function buildArcs() {
    const nUsed = src === 'last 2 tokens' ? 2 : src === 'last token only' ? 1 : 0;
    arcs.forEach((m, u) => {
      m.visible = u < nUsed && tokens.length - 1 - u >= 0;
      if (!m.visible) return;
      const i = tokens.length - 1 - u, a = new THREE.Vector3(SLOT_X, 0.85, TRACK_Z - 0.1), b = new THREE.Vector3(tilePos(i), 0.85, TRACK_Z - 0.1);
      const mid = a.clone().add(b).multiplyScalar(0.5); mid.y += 0.8 + u * 0.5;
      m.geometry.dispose(); m.geometry = new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(a, mid, b), 40, u ? 0.022 : 0.034, 8, false);
      m.material.opacity = u ? 0.55 : 0.95;
    });
  }

  function choose(word, from) {
    if (flyer.t >= 0) return;
    flyer.t = 0; flyer.word = word; flyer.from.copy(from);
    tokens.push(word); flyer.card = tileFor(tokens.length - 1); flyer.card.card.mesh.position.copy(from);
    sync();
  }

  const drag = meshDrag(engine.canvas, camera, controls, {
    objects: () => candObjs.filter((o) => o.card.mesh.visible).map((o) => o.card.mesh),
    onDown: () => false,
    onTap: (obj) => { if (obj && obj.userData.cand && !gen) choose(obj.userData.cand.word, obj.position); },
  });

  let narrow = null, fit = null;
  function layout() {
    const nw = stage.clientWidth < 640;
    if (nw === narrow) return;
    narrow = nw;
    fit = framer(stage, camera, controls, nw ? { width: 7.4, height: 7, center: [0.2, 0.8, 0.2] } : { width: 11.6, height: 5.5, center: [-0.2, 0.9, 0.1] });
  }

  predict();
  const tmp = new THREE.Vector3();
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    layout(); fit();
    if (gen && flyer.t < 0) { genT += dt; if (genT > 0.75) { genT = 0; const w = sample(), o = candObjs.find((c) => c.word === w); choose(w, o ? o.card.mesh.position : tmp.set(0, 1, CAND_Z)); genCount++; if (genCount >= 14 || tokens.length > 40) { gen = false; genB.setLabel('Generate'); } } }
    dropTiles();
    // tiles glide along the track; the newest flies in from its column
    const start = Math.max(0, tokens.length - SHOW);
    for (let i = start; i < tokens.length; i++) {
      const t = tileFor(i), goalX = tilePos(i);
      if (flyer.t >= 0 && t === flyer.card) continue;
      t.x += (goalX - t.x) * (1 - Math.exp(-dt * 8));
      const fade = i - start < 1 && tokens.length > SHOW ? 0.6 : 1;
      t.card.mesh.position.set(t.x, 0.45, TRACK_Z); t.card.mesh.scale.setScalar(fade);
    }
    if (flyer.t >= 0) {
      flyer.t = Math.min(1, flyer.t + dt / 0.5);
      const e = flyer.t * flyer.t * (3 - 2 * flyer.t), t = flyer.card, goal = tmp.set(tilePos(tokens.length - 1), 0.45, TRACK_Z);
      t.card.mesh.position.lerpVectors(flyer.from, goal, e); t.card.mesh.position.y += Math.sin(Math.PI * e) * 0.9;
      if (flyer.t >= 1) { t.x = goal.x; flyer.t = -1; buildArcs(); }
    }
    // candidates: a fan of columns in front, height = probability
    const n = cands.length;
    candObjs.forEach((o, i) => {
      if (!o.card.mesh.visible) return;
      o.shown += (o.p - o.shown) * (1 - Math.exp(-dt * 8));
      const x = (i - (n - 1) / 2) * (narrow ? 0.74 : 1.02), z = CAND_Z + Math.abs(i - (n - 1) / 2) * (narrow ? 0.05 : 0.1), hgt = 0.08 + o.shown * 2.0;
      o.col.position.set(x, 0, z); o.col.scale.y = hgt;
      o.card.mesh.position.set(x, hgt + 0.28, z); o.card.mesh.rotation.set(-0.25, 0, 0); o.card.mesh.scale.setScalar(narrow ? 0.72 : 1);
      o.col.material.emissiveIntensity = i === 0 ? 0.7 : 0.3;
    });
    qCard.mesh.rotation.y = Math.sin(performance.now() / 600) * 0.25;
    controls.update(dt);
    st.n.set(String(tokens.length)); st.src.set(src); st.top.set(cands.length ? `"${cands[0].w}" ${Math.round(cands[0].p * 100)} %` : '—');
    badge.set(gen ? `Generating… ${genCount} new tokens` : src === 'nothing it knows' ? 'It has never seen these words: it can only guess common ones' : 'Tap a candidate word to add it');
  });
  engine.start();

  stage.__llm = { tokens: () => tokens.join(' '), cands: () => cands.map((c) => c.w), pick: (i) => choose(cands[i].w, candObjs[i].card.mesh.position), gen: () => { gen = true; genB.setLabel('Stop'); } };
  return {
    dispose() {
      drag.dispose(); clearTiles(); candObjs.forEach((o) => o.card.dispose()); qCard.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__llm;
    },
  };
}
