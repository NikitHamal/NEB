/**
 * What is AI? in 3D — a stepped podium of nested tiers: Artificial Intelligence at the base,
 * Machine Learning standing on it, Deep Learning on top (deep learning is a kind of machine
 * learning, which is one way of doing AI), and a separate tray for "Not AI": things that only
 * follow fixed instructions. Drag each card onto the right tier. A right answer settles onto
 * it as a tile; a wrong one flies back and says why.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { makeLabelSprite } from '../core/engine.js';
import { createStudio, framer, slabCard, wrapLines, meshDrag, THREE } from './ai3d/stage.js';

const ITEMS = [
  { t: 'Chess engine searching millions of moves', r: 'ai', why: 'It plans with search and hand-written rules about good positions: AI, but it does not learn from data.' },
  { t: 'Spam filter that learns from emails you mark', r: 'ml', why: 'It learns which words predict spam from labelled examples: machine learning.' },
  { t: 'Chatbot writing an essay', r: 'dl', why: 'Large language models are huge neural networks trained on text: deep learning.' },
  { t: 'Face unlock on a phone', r: 'dl', why: 'Faces are recognised by a deep convolutional network trained on many images.' },
  { t: 'Calculator doing 2 + 2', r: 'none', why: 'It follows exact arithmetic rules. No reasoning, no learning: not AI.' },
  { t: 'Route planner finding the shortest path', r: 'ai', why: 'Classic search (Dijkstra, A*) is a core AI technique, with no learning needed.' },
  { t: 'Video recommender', r: 'ml', why: 'It learns your tastes from what you and similar people watched.' },
  { t: 'Self-driving car seeing pedestrians', r: 'dl', why: 'Camera images are understood by deep neural networks.' },
  { t: 'Thermostat switching on at 7 am', r: 'none', why: 'A fixed timer rule set by a person: automation, not AI.' },
  { t: 'Image generator from a text prompt', r: 'dl', why: 'Diffusion models are deep networks trained on millions of captioned pictures.' },
  { t: 'Weather forecast fitted to past data', r: 'ml', why: 'A model learns patterns from years of measurements.' },
  { t: 'Digital clock', r: 'none', why: 'It just counts seconds. Nothing is decided or learned.' },
];
// tiers: radius, top height, where tiles sit (radius), colour
const TIER = {
  ai: { label: 'ARTIFICIAL INTELLIGENCE', r: 3.6, y: 0.3, at: 3.02, color: 0x4f46e5 },
  ml: { label: 'MACHINE LEARNING', r: 2.45, y: 0.6, at: 1.88, color: 0x7c3aed },
  dl: { label: 'DEEP LEARNING', r: 1.3, y: 0.9, at: 0.62, color: 0xdb2777 },
};
const TRAY = { x: 5.6, z: 1.3, w: 2.6, d: 2.0 };
const DECK = new THREE.Vector3(5.6, 2.0, -1.7);
// narrow screens: the tray moves in front of the podium and the deck floats above it
const HOLD_Y = 1.6;
const NAMES = { ai: 'AI', ml: 'machine learning', dl: 'deep learning', none: 'Not AI' };

function rimTexture(text, color) {
  const c = document.createElement('canvas'); c.width = 2048; c.height = 96; const g = c.getContext('2d');
  g.fillStyle = '#' + color.toString(16).padStart(6, '0'); g.fillRect(0, 0, 2048, 96);
  g.fillStyle = 'rgba(255,255,255,0.92)'; g.font = '800 54px Poppins, system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
  for (let i = 0; i < 2; i++) g.fillText(text, 512 + i * 1024, 50);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}

export default function init(stage) {
  const S = createStudio(stage, { camera: [1.4, 7.2, 9.6], target: [1.2, 0.4, 0], maxDistance: 26 });
  if (!S) return null;
  const { engine, scene, camera, controls } = S;
  const seg = Math.max(48, S.quality.segments || 64);

  // the podium
  const tiers = {};
  let base = 0;
  for (const key of ['ai', 'ml', 'dl']) {
    const T = TIER[key];
    const mat = new THREE.MeshStandardMaterial({ color: T.color, roughness: 0.32, metalness: 0.05, emissive: T.color, emissiveIntensity: 0.08 });
    const h = T.y - base;
    const m = new THREE.Mesh(new THREE.CylinderGeometry(T.r, T.r, h, seg), mat); m.position.y = base + h / 2; m.castShadow = true; m.receiveShadow = true; scene.add(m);
    const rimTex = rimTexture(T.label, T.color);
    const rim = new THREE.Mesh(new THREE.CylinderGeometry(T.r + 0.004, T.r + 0.004, h * 0.9, seg, 1, true), new THREE.MeshStandardMaterial({ map: rimTex, roughness: 0.4 }));
    rim.position.y = base + h / 2; rim.rotation.y = -Math.PI / 2; scene.add(rim);
    const glow = new THREE.Mesh(new THREE.TorusGeometry(T.r, 0.025, 8, seg), new THREE.MeshBasicMaterial({ color: T.color, toneMapped: false, transparent: true, opacity: 0.6 }));
    glow.rotation.x = Math.PI / 2; glow.position.y = T.y + 0.005; scene.add(glow);
    tiers[key] = { mat, glow, T };
    base = T.y;
  }

  // the Not-AI tray
  const tray = new THREE.Group(); tray.position.set(TRAY.x, 0, TRAY.z); scene.add(tray);
  const trayMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.4, emissive: 0x64748b, emissiveIntensity: 0.05 });
  const trayBase = new THREE.Mesh(new THREE.BoxGeometry(TRAY.w, 0.08, TRAY.d), trayMat); trayBase.position.y = 0.04; trayBase.receiveShadow = true; tray.add(trayBase);
  for (const [w, d, x, z] of [[TRAY.w, 0.08, 0, -TRAY.d / 2], [TRAY.w, 0.08, 0, TRAY.d / 2], [0.08, TRAY.d, -TRAY.w / 2, 0], [0.08, TRAY.d, TRAY.w / 2, 0]]) {
    const wall = new THREE.Mesh(new THREE.BoxGeometry(w, 0.22, d), trayMat); wall.position.set(x, 0.11, z); wall.castShadow = true; tray.add(wall);
  }
  const trayLbl = makeLabelSprite('Not AI', { fontSize: 44, bg: 'rgba(100,116,139,0.92)', scale: 0.38 }); trayLbl.position.set(0, 0.6, -TRAY.d / 2); tray.add(trayLbl);
  const deckLbl = makeLabelSprite('drag the card', { fontSize: 40, bg: 'rgba(79,70,229,0.92)', scale: 0.3 }); scene.add(deckLbl);

  // the current card
  let curItem = null;
  const card = slabCard({
    w: 2.3, h: 0.9, res: 300,
    draw: (g, w, h) => {
      if (!curItem) return;
      g.textAlign = 'left'; g.fillStyle = '#4f46e5'; g.fillRect(36, 30, 18, h - 60);
      g.font = '600 44px Poppins, system-ui, sans-serif'; g.fillStyle = '#0f172a'; g.textBaseline = 'middle';
      const lines = wrapLines(g, curItem.t, w - 140);
      lines.forEach((l, i) => g.fillText(l, 90, h / 2 + (i - (lines.length - 1) / 2) * 58));
      g.font = '600 26px Poppins, system-ui, sans-serif'; g.fillStyle = '#64748b'; g.textAlign = 'right';
      g.fillText(`${cur + 1} / ${order.length}`, w - 36, 40);
    },
  });
  scene.add(card.mesh);

  const hud = createHud(stage);
  const badge = hud.badge('Drag the card onto the right tier', '#4f46e5');
  const panel = createPanel(stage, { title: 'Sort it out' });
  panel.button({ label: 'Shuffle and start again', icon: 'shuffle', variant: 'ghost', onClick: restart });
  const st = panel.stats([{ key: 'done', label: 'Sorted' }, { key: 'acc', label: 'First-try accuracy' }]);
  const why = panel.info('Traditional programs follow rules a person wrote. Machine learning finds the rules from examples. Deep learning does that with many-layered neural networks.');

  let order = [], cur = 0, correct = 0, tries = 0, held = false, shake = 0, msgT = 0, msgOk = true, t = 0;
  const tiles = [];
  const cardGoal = new THREE.Vector3().copy(DECK);

  function restart() {
    order = ITEMS.map((_, i) => i).sort(() => Math.random() - 0.5); cur = 0; correct = 0; tries = 0;
    tiles.forEach((p) => { scene.remove(p.card.mesh); p.card.dispose(); }); tiles.length = 0;
    nextCard();
  }
  function nextCard() {
    curItem = cur < order.length ? ITEMS[order[cur]] : null;
    card.mesh.visible = !!curItem; deckLbl.visible = !!curItem && cur === 0;
    if (curItem) { card.redraw(); card.mesh.position.set(DECK.x, DECK.y + 1.2, DECK.z); cardGoal.copy(DECK); }
  }

  function regionAt(x, z) {
    if (Math.abs(x - TRAY.x) < TRAY.w / 2 + 0.2 && Math.abs(z - TRAY.z) < TRAY.d / 2 + 0.2) return 'none';
    const r = Math.hypot(x, z);
    return r < TIER.dl.r ? 'dl' : r < TIER.ml.r ? 'ml' : r < TIER.ai.r ? 'ai' : null;
  }

  // resting places: the front arc of each ring (so the tiles read from the default view), a
  // little stack on the small Deep Learning top, rows in the tray
  const SLOTS = { ai: [1.57, 1.08, 2.06, 0.6, 2.54], ml: [1.57, 0.84, 2.3] };
  function slotFor(reg) {
    const n = tiles.filter((p) => p.reg === reg).length;
    if (reg === 'none') return new THREE.Vector3(TRAY.x, 0.1, TRAY.z - 0.6 + n * 0.42);
    if (reg === 'dl') return new THREE.Vector3(0, TIER.dl.y + 0.02, -0.5 + (n % 4) * 0.33);
    const T = TIER[reg], a = SLOTS[reg][n % SLOTS[reg].length];
    return new THREE.Vector3(Math.cos(a) * T.at, T.y + 0.02, Math.sin(a) * T.at);
  }

  function drop(reg) {
    if (!curItem) return;
    if (!reg) { cardGoal.copy(DECK); return; }
    tries++;
    if (reg === curItem.r) {
      if (tries === 1) correct++;
      const goal = slotFor(reg);
      const tile = slabCard({
        w: 1.5, h: 0.36, depth: 0.04, radius: 0.08, res: 280,
        draw: (g, w, h) => {
          g.font = '600 30px Poppins, system-ui, sans-serif'; g.fillStyle = '#0f172a'; g.textBaseline = 'middle'; g.textAlign = 'center';
          let s = curItem.t; while (g.measureText(s).width > w - 40 && s.length > 4) s = s.slice(0, -2);
          g.fillText(s === curItem.t ? s : `${s.trimEnd()}…`, w / 2, h / 2);
        },
      });
      tile.mesh.position.copy(card.mesh.position); tile.mesh.quaternion.copy(card.mesh.quaternion);
      scene.add(tile.mesh);
      tiles.push({ card: tile, reg, goal, q: new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI / 2, 0, 0)) });
      why.set(`✓ ${curItem.why}`); msgOk = true; msgT = 5;
      cur++; tries = 0; nextCard();
    } else {
      why.set(`Not quite: that is not ${NAMES[reg]}. ${curItem.why}`); msgOk = false; msgT = 5;
      shake = 1; cardGoal.copy(DECK);
    }
  }

  let hover = null;
  const drag = meshDrag(engine.canvas, camera, controls, {
    objects: () => (curItem ? [card.mesh] : []),
    plane: new THREE.Plane(new THREE.Vector3(0, 1, 0), -HOLD_Y),
    onDown: () => { held = true; deckLbl.visible = false; },
    onMove: (o, p) => { cardGoal.set(p.x, HOLD_Y, p.z); hover = regionAt(p.x, p.z); },
    onUp: () => { held = false; const p = card.mesh.position; drop(regionAt(p.x, p.z)); hover = null; },
  });

  let narrow = null, fit = null;
  function layout() {
    const n = stage.clientWidth < 640;
    if (n === narrow) return;
    narrow = n;
    if (n) { TRAY.x = 0; TRAY.z = 5.0; DECK.set(0, 2.9, 2.6); } else { TRAY.x = 5.6; TRAY.z = 1.3; DECK.set(5.6, 2.0, -1.7); }
    tray.position.set(TRAY.x, 0, TRAY.z);
    fit = framer(stage, camera, controls, n ? { width: 8.4, height: 9.5, center: [0, 0.6, 1.6] } : { width: 13, height: 7, center: [1.6, 0.4, 0.4] });
    if (!held) cardGoal.copy(DECK);
    let k = 0; for (const p of tiles) if (p.reg === 'none') p.goal.set(TRAY.x, 0.1, TRAY.z - 0.6 + (k++) * 0.42);
  }

  restart();
  const qFace = new THREE.Quaternion(), qFlat = new THREE.Quaternion().setFromEuler(new THREE.Euler(-1.2, 0, 0)), e3 = new THREE.Euler();
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05); t += dt;
    layout(); fit();
    // card: spring towards its goal, face the camera at the deck, tilt flat while carried
    const k = 1 - Math.exp(-dt * (held ? 22 : 7));
    card.mesh.position.lerp(cardGoal, k);
    if (!held) card.mesh.position.y += Math.sin(t * 2) * 0.002;
    shake = Math.max(0, shake - dt * 1.6);
    e3.set(-0.35, Math.sin(t * 30) * shake * 0.35, 0); qFace.setFromEuler(e3);
    card.mesh.quaternion.slerp(held ? qFlat : qFace, 1 - Math.exp(-dt * 10));
    deckLbl.position.set(DECK.x, DECK.y - 0.75, DECK.z + 0.3);
    // tiles glide to their places
    for (const p of tiles) { p.card.mesh.position.lerp(p.goal, 1 - Math.exp(-dt * 6)); p.card.mesh.quaternion.slerp(p.q, 1 - Math.exp(-dt * 6)); }
    for (const key in tiers) {
      const on = hover === key;
      tiers[key].mat.emissiveIntensity += ((on ? 0.45 : 0.08) - tiers[key].mat.emissiveIntensity) * (1 - Math.exp(-dt * 10));
      tiers[key].glow.material.opacity = on ? 1 : 0.55;
    }
    trayMat.emissiveIntensity = hover === 'none' ? 0.5 : 0.05;
    msgT = Math.max(0, msgT - dt);
    controls.update(dt);
    st.done.set(`${cur} of ${ITEMS.length}`); st.acc.set(cur ? `${Math.round(correct / cur * 100)} %` : '—');
    badge.set(!curItem ? `All sorted! ${correct} of ${ITEMS.length} right first time` : msgT > 0 ? (msgOk ? 'Right!' : 'Try another tier') : 'Drag the card onto the right tier');
    badge.el.style.setProperty('--ix-hud-color', !curItem || (msgT > 0 && msgOk) ? '#16a34a' : msgT > 0 ? '#f97316' : '#4f46e5');
  });
  engine.start();

  stage.__whatai = {
    answer: () => curItem && curItem.r,
    drop: (reg) => { const p = reg === 'none' ? [TRAY.x, TRAY.z] : reg ? [TIER[reg].at * 0.98, 0.3] : [8, 8]; card.mesh.position.set(p[0], HOLD_Y, p[1]); drop(reg); },
    done: () => cur,
  };
  return {
    dispose() {
      drag.dispose(); card.dispose(); tiles.forEach((p) => p.card.dispose());
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__whatai;
    },
  };
}
