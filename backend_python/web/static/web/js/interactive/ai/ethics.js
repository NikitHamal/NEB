/**
 * AI in your life, in 3D — a hiring model learns from past decisions that were biased against
 * group B. 240 applicants stand on a board: across it their skill test score, into it their home
 * area. Both groups have the same spread of skill, but a logistic-regression model trained on
 * those past decisions (by gradient descent, right here) reproduces the bias: its pass mark, a
 * glass wall for each group, stands further right for group B. Hide the group from the model and
 * it can still find it through a proxy (home area); only fixing the data removes it. Tap an
 * applicant to see their case. Four real dilemmas follow in the panel.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { makeLabelSprite } from '../core/engine.js';
import { label } from '../physics/physics3d/field.js';
import { createStudio, framer, THREE } from './ai3d/stage.js';

const SCENARIOS = [
  {
    id: 'hiring', title: 'AI résumé screener',
    desc: 'A company trains an AI to rank job applicants from past hiring data. But the company historically hired mostly men. What happens?',
    options: [
      { label: 'The AI will be perfectly fair', correct: false,
        explain: 'No — the AI learns the patterns in its data. If past hiring favoured men, the AI will too, because that is the pattern it was trained on.' },
      { label: 'The AI will favour men, copying the bias', correct: true,
        explain: 'Correct. The model faithfully reproduces the bias in its training data. Without intervention it amplifies existing prejudice.' },
      { label: 'The AI refuses to rank anyone', correct: false,
        explain: 'No — the model has no concept of fairness unless humans build it in. It simply predicts from patterns.' },
    ],
    lesson: 'Bias enters AI through data. Diverse data, fairness audits, and human oversight are needed to counter it.',
  },
  {
    id: 'selfdriving', title: 'Self-driving car crash',
    desc: 'A self-driving car makes a decision per second. If it crashes and injures someone, who is responsible?',
    options: [
      { label: 'The car manufacturer', correct: false,
        explain: 'Partly — but the law is still unclear. There is no single agreed answer yet.' },
      { label: 'The programmer who wrote the AI', correct: false,
        explain: 'Partly — but millions of lines of code and learned weights make blame hard to pin on any one person.' },
      { label: 'It is an unsolved accountability problem', correct: true,
        explain: 'Correct. Our laws were built around human decisions. AI that acts millions of times per second does not fit, and accountability is an open problem.' },
    ],
    lesson: 'Accountability for AI decisions is an unsolved ethical and legal problem. Humans must stay in the loop for high-stakes choices.',
  },
  {
    id: 'medical', title: 'AI diagnoses an X-ray',
    desc: 'A hospital uses AI to flag possible cancer in X-rays. The AI is faster than any doctor. Should they trust it fully?',
    options: [
      { label: 'Yes — it is faster, so always trust it', correct: false,
        explain: 'No. AI can be confidently wrong, and a false negative here could cost a life. Trust must be earned, not assumed.' },
      { label: 'Use it as a tool, with doctors checking', correct: true,
        explain: 'Correct. Doctor-plus-AI catches more cancers than either alone. The AI augments the human; it does not replace the judgement.' },
      { label: 'Never use AI in medicine', correct: false,
        explain: 'No — used carefully, AI genuinely saves lives. The key is thoughtful use, not refusal.' },
    ],
    lesson: 'AI is a powerful tool that augments humans. Human-plus-AI usually beats either alone — provided we check the output.',
  },
  {
    id: 'privacy', title: 'Free chatbot reads your data',
    desc: 'A free AI assistant improves by learning from everything you type, including private messages. Acceptable?',
    options: [
      { label: 'Yes — it is free, so fair trade', correct: false,
        explain: 'Not necessarily. "Free" can mean paying with your personal data, which may be stored, shared, or leaked.' },
      { label: 'Only if you understand and agree', correct: true,
        explain: 'Correct. Informed consent matters. You should know what is collected, who sees it, and what it is used to decide about you.' },
      { label: 'AI cannot learn from private data', correct: false,
        explain: 'False. Many models are trained on user input. The question is whether you agreed to that.' },
    ],
    lesson: 'Asking who owns your data, who can see it, and what it decides about you is now basic digital literacy.',
  },
];
const NA = 240;
const BW = 6.4, BD = 4.2;                 // board: skill along x, home area into the screen
const BLUE = new THREE.Color(0x2563eb), PINK = new THREE.Color(0xdb2777), DULL = new THREE.Color(0x334155);

function pawnGeometry(pointed) {
  const pts = pointed
    ? [[0, 0], [0.11, 0], [0.11, 0.03], [0.07, 0.06], [0.06, 0.16], [0.09, 0.2], [0.05, 0.24], [0.0, 0.42]]
    : [[0, 0], [0.11, 0], [0.11, 0.03], [0.07, 0.06], [0.05, 0.18], [0.08, 0.21], [0.05, 0.24], [0.075, 0.29], [0.08, 0.33], [0.06, 0.39], [0.0, 0.41]];
  return new THREE.LatheGeometry(pts.map(([x, y]) => new THREE.Vector2(x, y)), 12);
}

export default function init(stage) {
  const S = createStudio(stage, { camera: [0.8, 5.6, 7.2], target: [0.6, 0.3, 0], maxDistance: 22 });
  if (!S) return null;
  const { engine, scene, camera, controls } = S;

  const skill = new Float64Array(NA), area = new Float64Array(NA), grp = new Uint8Array(NA), hired = new Uint8Array(NA), score = new Float64Array(NA);
  const w = new Float64Array(4);
  let bias = 1.6, useGroup = true, useArea = true, picked = -1, rateA = 0, rateB = 0;
  const shownRate = [0, 0];

  // skill 0..1 → x, area 0..1 → z (high area further away)
  const PX = (v) => (v - 0.5) * BW, PZ = (v) => (0.5 - v) * BD;

  // ---- the board ----
  const board = new THREE.Mesh(new THREE.BoxGeometry(BW + 0.5, 0.1, BD + 0.5), new THREE.MeshStandardMaterial({ color: 0x1e2440, roughness: 0.55 }));
  board.position.y = -0.05; board.receiveShadow = true; scene.add(board);
  const grid = new THREE.GridHelper(BW, 10, 0x475569, 0x334155); grid.scale.z = BD / BW; grid.position.y = 0.003; grid.material.transparent = true; grid.material.opacity = 0.4; scene.add(grid);
  const xLbl = makeLabelSprite('skill test score →', { fontSize: 40, scale: 0.24 }); xLbl.position.set(PX(0.75), 0.1, PZ(0) + 0.55); scene.add(xLbl);
  const zLbl = makeLabelSprite('home area ↑ (a proxy for group)', { fontSize: 40, scale: 0.24 }); zLbl.position.set(PX(0) - 0.4, 0.1, PZ(0.5)); zLbl.center.set(1, 0.5); scene.add(zLbl);

  // ---- applicants: round-headed pawns for A, pointed for B; faded if rejected in the past ----
  const matA = new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 0.05 }), matB = matA.clone();
  const pawns = [new THREE.InstancedMesh(pawnGeometry(false), matA, NA), new THREE.InstancedMesh(pawnGeometry(true), matB, NA)];
  pawns.forEach((p) => { p.castShadow = true; scene.add(p); });
  const rings = new THREE.InstancedMesh(new THREE.TorusGeometry(0.12, 0.016, 6, 20), new THREE.MeshBasicMaterial({ color: 0x4ade80, toneMapped: false }), NA); scene.add(rings);
  const pickRing = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.02, 8, 28), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false })); pickRing.rotation.x = Math.PI / 2; pickRing.visible = false; scene.add(pickRing);
  const slot = new Int16Array(NA);

  // ---- the model's pass marks: a glass wall per group ----
  function wall(color, striped) {
    const geo = new THREE.PlaneGeometry(1, 1, 1, 1);
    const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.34, side: THREE.DoubleSide, depthWrite: false });
    if (striped) {
      const c = document.createElement('canvas'); c.width = 8; c.height = 64; const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, 8, 40);
      mat.alphaMap = new THREE.CanvasTexture(c); mat.alphaMap.wrapT = THREE.RepeatWrapping; mat.alphaMap.repeat.set(1, 6);
    }
    const m = new THREE.Mesh(geo, mat); m.renderOrder = 4; scene.add(m);
    const top = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 1, 8), new THREE.MeshBasicMaterial({ color, toneMapped: false })); top.rotation.z = Math.PI / 2; scene.add(top);
    return { m, top };
  }
  const walls = [wall(0x3b82f6, false), wall(0xec4899, true)];
  const WALL_H = 0.7;

  // ---- selection-rate tubes ----
  const tubes = [0, 1].map((g) => {
    const grpM = new THREE.Group(); grpM.position.set(PX(1) + 1.0 + g * 0.75, 0, PZ(0.5)); scene.add(grpM);
    const glass = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 2, 32, 1, true), new THREE.MeshStandardMaterial({ color: 0xe0e7ff, roughness: 0.1, transparent: true, opacity: 0.18, side: THREE.DoubleSide, depthWrite: false }));
    glass.position.y = 1; grpM.add(glass);
    const baseM = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.06, 32), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 })); baseM.position.y = 0.03; grpM.add(baseM);
    const liqGeo = new THREE.CylinderGeometry(0.21, 0.21, 1, 32); liqGeo.translate(0, 0.5, 0);
    const liq = new THREE.Mesh(liqGeo, new THREE.MeshStandardMaterial({ color: g ? PINK : BLUE, emissive: g ? PINK : BLUE, emissiveIntensity: 0.35, roughness: 0.25 }));
    liq.position.y = 0.06; grpM.add(liq);
    const lbl = makeLabelSprite(g ? 'Group B' : 'Group A', { fontSize: 40, bg: g ? 'rgba(219,39,119,0.9)' : 'rgba(37,99,235,0.9)', scale: 0.26 }); lbl.position.set(0, 2.25, 0); grpM.add(lbl);
    const pct = label(stage, camera);
    return { grpM, liq, pct };
  });
  const tubeTag = makeLabelSprite('selected by the model', { fontSize: 36, scale: 0.26 }); tubeTag.position.set(PX(1) + 1.37, 0.12, PZ(0.5) + 0.6); scene.add(tubeTag);
  const card = label(stage, camera);
  card.el.style.whiteSpace = 'normal'; card.el.style.width = '190px'; card.el.style.borderRadius = '12px'; card.el.style.padding = '8px 11px'; card.el.style.lineHeight = '1.45'; card.el.style.fontWeight = '600';

  // ---- panel ----
  const hud = createHud(stage);
  const badge = hud.badge('Raise the bias in the past data and retrain', '#db2777');
  const panel = createPanel(stage, { title: 'Bias in, bias out' });
  panel.slider({ label: 'Bias in the past hiring decisions', min: 0, max: 3, step: 0.1, value: bias, format: (v) => (v === 0 ? 'none' : v.toFixed(1)), onChange: (v) => { bias = v; build(); } });
  panel.toggle({ label: 'Model may see the group', value: true, onChange: (v) => { useGroup = v; train(); } });
  panel.toggle({ label: 'Model may see the home area (a proxy)', value: true, onChange: (v) => { useArea = v; train(); } });
  const st = panel.stats([{ key: 'a', label: 'Group A selected' }, { key: 'b', label: 'Group B selected' }, { key: 'ratio', label: 'B ÷ A (fair ≥ 0.8)' }, { key: 'w', label: 'Weight on group' }]);
  panel.info('Round pawns are group A, pointed pawns group B. Bright pawns were hired in the past, dim ones rejected; a green ring means the model would invite them. The glass walls are the model\'s pass marks: blue for A, striped pink for B. Tap any pawn to see their case.');
  panel.section('Real dilemmas');
  const qWrap = document.createElement('div'); qWrap.className = 'ix-ctrl-row'; panel.body.appendChild(qWrap);
  let qi = 0;
  function showQ() {
    const s = SCENARIOS[qi];
    qWrap.innerHTML = '';
    const h = document.createElement('div'); h.className = 'ix-ctrl-label'; h.style.fontWeight = '700'; h.textContent = `${qi + 1}/${SCENARIOS.length} · ${s.title}`;
    const p = document.createElement('p'); p.className = 'ix-ctrl-info'; p.textContent = s.desc;
    const box = document.createElement('div'); box.className = 'k2-chips'; box.style.flexDirection = 'column'; box.style.alignItems = 'stretch';
    const out = document.createElement('p'); out.className = 'ix-ctrl-info';
    s.options.forEach((o) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'k2-chip'; b.style.justifyContent = 'flex-start'; b.style.whiteSpace = 'normal'; b.style.textAlign = 'left'; b.style.lineHeight = '1.3'; b.textContent = o.label;
      b.addEventListener('click', () => { [...box.children].forEach((c) => c.classList.remove('is-on')); b.classList.add('is-on'); b.style.background = o.correct ? '#16a34a' : '#e5484d'; b.style.borderColor = b.style.background; out.textContent = `${o.explain} ${o.correct ? s.lesson : ''}`; });
      box.appendChild(b);
    });
    const next = document.createElement('button'); next.type = 'button'; next.className = 'ix-ctrl-btn ix-ctrl-btn-ghost'; next.textContent = 'Next dilemma';
    next.addEventListener('click', () => { qi = (qi + 1) % SCENARIOS.length; showQ(); });
    qWrap.append(h, p, box, out, next);
  }
  showQ();

  // ---- data and model (as in the classic version) ----
  function build() {
    let s = 12345; const r = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < NA; i++) {
      grp[i] = i % 2; skill[i] = Math.min(1, Math.max(0, 0.5 + (r() + r() + r() - 1.5) * 0.45));
      area[i] = Math.min(1, Math.max(0, (grp[i] ? 0.3 : 0.7) + (r() - 0.5) * 0.5));
      const z = 7 * (skill[i] - 0.55) + (grp[i] ? -bias : bias) * 0.9;
      hired[i] = r() < 1 / (1 + Math.exp(-z)) ? 1 : 0;
    }
    train();
  }
  function feat(i, out) { out[0] = skill[i] - 0.5; out[1] = useGroup ? (grp[i] ? -0.5 : 0.5) : 0; out[2] = useArea ? area[i] - 0.5 : 0; out[3] = 1; return out; }
  const F = new Float64Array(4), G = new Float64Array(4);
  function train() {
    w.fill(0);
    for (let it = 0; it < 400; it++) {
      G.fill(0);
      for (let i = 0; i < NA; i++) { feat(i, F); let z = 0; for (let j = 0; j < 4; j++) z += w[j] * F[j]; const p = 1 / (1 + Math.exp(-z)), e = p - hired[i]; for (let j = 0; j < 4; j++) G[j] += e * F[j]; }
      for (let j = 0; j < 4; j++) w[j] -= 1.5 * G[j] / NA;
    }
    let sa = 0, na = 0, sb = 0, nb = 0;
    for (let i = 0; i < NA; i++) { feat(i, F); let z = 0; for (let j = 0; j < 4; j++) z += w[j] * F[j]; score[i] = 1 / (1 + Math.exp(-z)); const sel = score[i] > 0.5; if (grp[i]) { nb++; if (sel) sb++; } else { na++; if (sel) sa++; } }
    rateA = sa / na; rateB = sb / nb;
    placePawns(); placeWalls();
  }

  const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), ONE = new THREE.Vector3(1, 1, 1), QR = new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI / 2, 0, 0)), C = new THREE.Color();
  function placePawns() {
    const cnt = [0, 0]; let nr = 0;
    for (let i = 0; i < NA; i++) {
      const g = grp[i], k = cnt[g]++;
      slot[i] = k;
      V.set(PX(skill[i]), 0, PZ(area[i]));
      pawns[g].setMatrixAt(k, M4.compose(V, Q, ONE));
      pawns[g].setColorAt(k, C.copy(g ? PINK : BLUE).lerp(DULL, hired[i] ? 0 : 0.7));
      if (score[i] > 0.5) rings.setMatrixAt(nr++, M4.compose(V.setY(0.012), QR, ONE));
    }
    pawns.forEach((p, g) => { p.count = cnt[g]; p.instanceMatrix.needsUpdate = true; p.instanceColor.needsUpdate = true; });
    rings.count = nr; rings.instanceMatrix.needsUpdate = true;
  }
  const P0 = new THREE.Vector3(), P1 = new THREE.Vector3();
  function placeWalls() {
    for (let g = 0; g < 2; g++) {
      const gv = useGroup ? (g ? -0.5 : 0.5) : 0;
      const s0 = (a) => Math.min(1.04, Math.max(-0.04, -(w[1] * gv + (useArea ? w[2] * (a - 0.5) : 0) + w[3]) / (w[0] || 1e-6) + 0.5));
      P0.set(PX(s0(0)), 0, PZ(0)); P1.set(PX(s0(1)), 0, PZ(1));
      const { m, top } = walls[g], len = P0.distanceTo(P1);
      m.position.copy(P0).add(P1).multiplyScalar(0.5).setY(WALL_H / 2); m.scale.set(len, WALL_H, 1);
      m.rotation.set(0, -Math.atan2(P1.z - P0.z, P1.x - P0.x), 0);
      top.position.copy(m.position).setY(WALL_H); top.scale.y = len; top.rotation.set(0, m.rotation.y, Math.PI / 2);
    }
  }

  // ---- tap a pawn ----
  let downAt = null;
  function nearest(e) {
    const r = engine.canvas.getBoundingClientRect(); let best = -1, bd = e.pointerType === 'touch' ? 26 : 16;
    for (let i = 0; i < NA; i++) {
      V.set(PX(skill[i]), 0.25, PZ(area[i])).project(camera);
      const d = Math.hypot((V.x + 1) / 2 * r.width - (e.clientX - r.left), (1 - V.y) / 2 * r.height - (e.clientY - r.top));
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  }
  const onDown = (e) => { downAt = [e.clientX, e.clientY]; };
  const onUp = (e) => { if (downAt && Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) < 6) picked = nearest(e); downAt = null; };
  const onMove = (e) => { if (!downAt) engine.canvas.style.cursor = nearest(e) >= 0 ? 'pointer' : ''; };
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);
  engine.canvas.addEventListener('pointermove', onMove);

  let narrow = null, fit = null;
  function layout() {
    const nw = stage.clientWidth < 640;
    if (nw === narrow) return;
    narrow = nw;
    fit = framer(stage, camera, controls, nw ? { width: 8.4, height: 7, center: [0.6, 0.4, 0] } : { width: 11.8, height: 5.5, center: [0.4, 0.4, 0] });
  }

  build();
  const tmp = new THREE.Vector3();
  engine.setUpdate((dt) => {
    dt = Math.min(dt, 0.05);
    layout(); fit();
    [rateA, rateB].forEach((r, g) => {
      shownRate[g] += (r - shownRate[g]) * (1 - Math.exp(-dt * 6));
      const t = tubes[g]; t.liq.scale.y = Math.max(0.01, shownRate[g] * 1.9);
      t.pct.el.textContent = `${Math.round(r * 100)} %`; t.pct.at(tmp.set(t.grpM.position.x, 0.06 + shownRate[g] * 1.9 + 0.2, t.grpM.position.z));
    });
    pickRing.visible = picked >= 0; card.el.style.opacity = picked >= 0 ? '1' : '0';
    if (picked >= 0) {
      pickRing.position.set(PX(skill[picked]), 0.015, PZ(area[picked]));
      const yes = score[picked] > 0.5;
      card.el.innerHTML = `Applicant #${picked + 1} · group ${grp[picked] ? 'B' : 'A'}<br>skill ${Math.round(skill[picked] * 100)} / 100<br>past decision: ${hired[picked] ? 'hired' : 'rejected'}<br><span style="color:${yes ? '#4ade80' : '#f87171'}">model: ${Math.round(score[picked] * 100)} % → ${yes ? 'interview' : 'reject'}</span>`;
      card.at(tmp.set(PX(skill[picked]), 0.6, PZ(area[picked])), -50);
    }
    controls.update(dt);
    const ratio = rateA > 0 ? rateB / rateA : 1;
    st.a.set(`${Math.round(rateA * 100)} %`); st.b.set(`${Math.round(rateB * 100)} %`); st.ratio.set(ratio.toFixed(2)); st.w.set(useGroup ? w[1].toFixed(2) : 'hidden');
    badge.set(ratio < 0.8 ? (useGroup ? 'The model copied the bias in the past decisions' : useArea ? 'Group hidden, but home area still leaks it: bias via a proxy' : 'Still unfair: the past labels themselves are biased') : 'Selection rates are close: much fairer');
  });
  engine.start();

  stage.__ethics = { rates: () => [rateA, rateB], set: (o) => { if (o.bias != null) { bias = o.bias; build(); } if (o.group != null) { useGroup = o.group; train(); } if (o.area != null) { useArea = o.area; train(); } }, pick: (i) => { picked = i; } };
  return {
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown); engine.canvas.removeEventListener('pointerup', onUp); engine.canvas.removeEventListener('pointermove', onMove);
      tubes.forEach((t) => t.pct.remove()); card.remove(); pawns.forEach((p) => p.dispose()); rings.dispose();
      controls.dispose(); panel.dispose(); hud.dispose(); engine.dispose(); delete stage.__ethics;
    },
  };
}
