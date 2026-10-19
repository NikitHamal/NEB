// Mushroom identification, edible or poisonous. Two fresh specimens lie in the tray: the field
// mushroom Agaricus (white cap, pink-brown free gills, a ring, no cup at the base) and the fly
// agaric Amanita muscaria (red cap with white warts, white gills, a skirt-like ring and a bulbous
// volva). The student studies each part with a hand lens, labels the Amanita, cuts the caps off,
// takes spore prints on half-white, half-black paper overnight, judges which is dangerous from
// its characters, and preserves the specimens in formalin.
import { THREE } from '../../engine.js';
import { createLens } from '../lens.js';
import { createLabelQuiz } from '../labelquiz.js';
import { enamelTray, timelapse, ask, tag, glassBeaker } from '../bench.js';
import { mesh, MAT, wet, canvasTexture, rng, ease, clamp } from '../kit.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const V2 = (x, y) => new THREE.Vector2(x, y);

function capTexture(kind) {
  return canvasTexture(`mush-cap:${kind}`, 256, 256, (g, w, h) => {
    g.fillStyle = kind === 'amanita' ? '#c8261d' : '#efe7d8'; g.fillRect(0, 0, w, h);
    const R = rng(kind.length * 7);
    if (kind === 'amanita') { for (let i = 0; i < 220; i++) { g.fillStyle = `rgba(${150 + R() * 60},20,15,0.25)`; g.fillRect(R() * w, R() * h, 6, 3); } }
    else { for (let i = 0; i < 300; i++) { g.strokeStyle = 'rgba(160,130,100,0.25)'; g.beginPath(); const x = R() * w; g.moveTo(x, R() * h); g.lineTo(x + 6, R() * h); g.stroke(); } }
  });
}

/** A mushroom lying in local +Y along its stipe; cap at the top. */
function buildMushroom(kind) {
  const am = kind === 'amanita'; const g = new THREE.Group(); const parts = {};
  const capR = am ? 0.46 : 0.4; const stH = am ? 0.85 : 0.6; const stR = am ? 0.07 : 0.075;
  const flesh = wet(0xf3efe4, { roughness: 0.6, clearcoat: 0.2, sheen: 0.4 });
  const stipe = mesh(new THREE.CylinderGeometry(stR * 0.85, stR, stH, 16), flesh, [0, stH / 2, 0]); g.add(stipe); parts.stipe = stipe;
  const capProf = []; for (let i = 0; i <= 12; i++) { const a = (i / 12) * Math.PI / 2; capProf.push(V2(Math.sin(a) * capR, Math.cos(a) * capR * (am ? 0.55 : 0.62))); }
  capProf.push(V2(capR * 0.98, -0.02)); capProf.push(V2(capR * 0.9, -0.03));
  const cap = mesh(new THREE.LatheGeometry(capProf.reverse(), 32), wet(0xffffff, { map: capTexture(kind), roughness: 0.45, clearcoat: am ? 0.8 : 0.3, side: THREE.DoubleSide }), [0, stH, 0]);
  cap.rotation.x = Math.PI; cap.rotation.x = 0; g.add(cap); parts.cap = cap;
  const under = mesh(new THREE.CircleGeometry(capR * 0.9, 32), wet(am ? 0xf8f5ec : 0x8a5a4a, { roughness: 0.8 }), [0, stH - 0.025, 0]); under.rotation.x = Math.PI / 2; g.add(under);
  const gills = new THREE.Group(); gills.position.y = stH - 0.02; g.add(gills); parts.gills = gills;
  const gm = wet(am ? 0xfffdf7 : 0x7a4a3c, { roughness: 0.7, side: THREE.DoubleSide });
  for (let k = 0; k < 64; k++) { const a = k / 64 * Math.PI * 2; const L = (k % 2 ? 0.55 : 0.85) * (capR - stR); const pl = mesh(new THREE.BoxGeometry(L, 0.05, 0.003), gm, [Math.cos(a) * (capR - L / 2 - 0.02), -0.022, Math.sin(a) * (capR - L / 2 - 0.02)]); pl.rotation.y = -a; gills.add(pl); }
  const ringY = stH - (am ? 0.18 : 0.14);
  const ring = mesh(new THREE.CylinderGeometry(stR * 1.1, stR * (am ? 2.6 : 1.9), am ? 0.12 : 0.06, 20, 1, true), wet(0xfbfaf5, { roughness: 0.6, side: THREE.DoubleSide }), [0, ringY - 0.04, 0]); g.add(ring); parts.ring = ring;
  if (am) {
    const volva = mesh(new THREE.SphereGeometry(stR * 2.1, 18, 12, 0, Math.PI * 2, Math.PI * 0.35, Math.PI * 0.65), wet(0xf1ece0, { roughness: 0.7, side: THREE.DoubleSide }), [0, 0.06, 0]); volva.scale.y = 0.9; g.add(volva); parts.volva = volva;
    for (let k = 0; k < 3; k++) g.add(mesh(new THREE.TorusGeometry(stR * (1.5 - k * 0.15), 0.008, 6, 16), MAT.matte(0xece6d6), [0, 0.13 + k * 0.035, 0]).rotateX(Math.PI / 2));
    const R = rng(4); for (let k = 0; k < 26; k++) { const a = R() * 6.28; const r = Math.sqrt(R()) * capR * 0.85; const y = Math.sqrt(Math.max(0, 1 - (r / capR) ** 2)) * capR * 0.55; g.add(mesh(new THREE.SphereGeometry(0.018 + R() * 0.012, 6, 5), MAT.matte(0xfaf7ee), [Math.cos(a) * r, stH + y, Math.sin(a) * r])); }
  } else { g.add(mesh(new THREE.SphereGeometry(stR * 1.05, 12, 8), flesh, [0, 0.0, 0])); }
  const anchors = { Pileus: new THREE.Vector3(0, stH + capR * 0.5, 0), 'Gills (lamellae)': new THREE.Vector3(capR * 0.6, stH - 0.04, 0.0), Stipe: new THREE.Vector3(stR, stH * 0.45, 0), 'Annulus (ring)': new THREE.Vector3(stR * 2.2, ringY - 0.06, 0), ...(am ? { Volva: new THREE.Vector3(stR * 2, 0.07, 0), 'Scales (warts)': new THREE.Vector3(capR * 0.4, stH + capR * 0.45, capR * 0.15) } : {}) };
  return { g, parts, capR, stH, ringY, kind, anchors };
}

function crosses(ax, ay, bx, by, cx, cy, dx, dy) {
  const d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx); if (Math.abs(d) < 1e-6) return false;
  const u = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d; const v = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d;
  return u >= 0 && u <= 1 && v >= 0 && v <= 1;
}

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const tray = enamelTray(2.9, 1.5); tray.position.set(0, 0, 0.1); world.add(tray);
  const ms = ['agaricus', 'amanita'].map((k, i) => {
    const m = buildMushroom(k); const holder = new THREE.Group(); holder.add(m.g); world.add(holder); m.holder = holder;
    holder.position.set(i ? 0.05 : -0.05, m.capR * 0.92, i ? 0.35 : -0.25); holder.rotation.set(0, i ? Math.PI : 0, Math.PI / 2);
    const t = tag(i ? 'B' : 'A', { h: 0.08 }); t.position.set(i ? 0.7 : -0.7, 0.75, i ? 0.35 : -0.25); world.add(t); return m;
  });
  const lens = createLens(ctx, { mag: 2.6, groundY: ctx.BENCH_Y + 0.12 });
  const paper = new THREE.Group(); paper.position.set(0, 0, 1.35); world.add(paper);
  const ptex = canvasTexture('spore-paper', 512, 256, (g, w, h) => { g.fillStyle = '#fbfaf5'; g.fillRect(0, 0, w / 2, h); g.fillStyle = '#111'; g.fillRect(w / 2, 0, w / 2, h); });
  paper.add(mesh(new THREE.BoxGeometry(2.0, 0.004, 0.9), [MAT.paper(), MAT.paper(), new THREE.MeshStandardMaterial({ map: ptex, roughness: 0.9 }), MAT.paper(), MAT.paper(), MAT.paper()], [0, 0.002, 0]));
  const prints = [0, 1].map((i) => { const cv = document.createElement('canvas'); cv.width = cv.height = 256; const t = new THREE.CanvasTexture(cv); const m = mesh(new THREE.CircleGeometry(0.4, 40), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, opacity: 0 }), [i ? 0.5 : -0.5, 0.006, 0]); m.rotation.x = -Math.PI / 2; paper.add(m); return { m, cv, t }; });
  function drawPrint(i, color) { const { cv, t } = prints[i]; const g = cv.getContext('2d'); g.clearRect(0, 0, 256, 256); g.strokeStyle = color; g.lineWidth = 2.4; for (let k = 0; k < 64; k++) { const a = k / 64 * Math.PI * 2; const r0 = 32; const r1 = k % 2 ? 80 : 118; g.beginPath(); g.moveTo(128 + Math.cos(a) * r0, 128 + Math.sin(a) * r0); g.lineTo(128 + Math.cos(a) * r1, 128 + Math.sin(a) * r1); g.stroke(); } t.needsUpdate = true; }
  drawPrint(0, 'rgba(70,40,30,0.9)'); drawPrint(1, 'rgba(250,250,245,0.95)');
  const beakers = [0, 1].map((i) => { const b = glassBeaker(0.45, 0.6, 0xffffff, 0); b.group.position.set(i ? 1.9 : -1.9, 0, 1.35); b.group.rotation.x = Math.PI; b.group.position.y = 0.62; world.add(b.group); return b; });
  const jar = glassBeaker(0.4, 0.9, 0xeef6e2, 0.8); jar.group.position.set(2.1, 0, -0.6); world.add(jar.group); const jt = tag('4% formalin', { h: 0.08 }); jt.position.set(2.1, 1.1, -0.6); world.add(jt);
  const tmp = new THREE.Vector3(); const loc = new THREE.Vector3();
  const TRAY = S([0, 2.3, 2.6], [0, 0.15, 0.25], 3.4);
  const seen = { agaricus: new Set(), amanita: new Set() }; let dwellOn = null; let dwell = 0; let quiz = null;
  const FACT = {
    pileus: 'Pileus (cap): the umbrella that shelters the gills.', gills: 'Gills (lamellae): radiating plates under the cap lined with basidia that bear the spores.',
    annulus: 'Annulus (ring): the torn remnant of the partial veil that covered the young gills.', stipe: 'Stipe (stalk): lifts the cap above the ground for spore dispersal.',
    volva: 'Volva: a cup at the base, the remains of the universal veil that wrapped the whole button — a warning sign of Amanita.', base: 'The stipe base is plain: no cup.',
  };
  function regionAt(m, p) {
    m.g.worldToLocal(loc.copy(p)); const r = Math.hypot(loc.x, loc.z);
    if (loc.y > m.stH + 0.02 && r < m.capR + 0.08) return 'pileus';
    if (loc.y > m.stH - 0.1 && r < m.capR + 0.06) return 'gills';
    if (Math.abs(loc.y - m.ringY + 0.04) < 0.08 && r < 0.3) return 'annulus';
    if (loc.y < 0.18 && r < 0.25) return m.kind === 'amanita' ? 'volva' : 'base';
    if (loc.y < m.stH && r < 0.2) return 'stipe';
    return null;
  }
  const stepLens = {
    title: 'Study both mushrooms with the hand lens', text: 'Hold the <b>hand lens</b> over each part of mushroom A and mushroom B in turn: cap, gills, ring, stalk and base.', tool: 'lens', shot: TRAY,
    aim(p, out) { return input.planePoint(ctx.BENCH_Y + 0.12, out) || false; },
    skip() { ['pileus', 'gills', 'annulus', 'stipe', 'base'].forEach((r) => seen.agaricus.add(r)); ['pileus', 'gills', 'annulus', 'stipe', 'volva'].forEach((r) => seen.amanita.add(r)); },
    update(dt) {
      if (!lens.active) { dwell = 0; return; }
      const m = ms.find((q) => regionAt(q, tools.tip)); const r = m ? regionAt(m, tools.tip) : null; const key = m ? `${m.kind}:${r}` : null;
      if (key && key === dwellOn) dwell += dt; else { dwellOn = key; dwell = 0; }
      if (key && dwell > 0.55 && !seen[m.kind].has(r)) {
        seen[m.kind].add(r); sfx.play('ok');
        const extra = m.kind === 'amanita' ? { pileus: ' Bright red with white warts (scales).', gills: ' White and free.', annulus: ' A large, hanging skirt.' } : { pileus: ' Smooth, white to pale brown.', gills: ' Pink, turning chocolate brown, free from the stalk.', annulus: ' A thin single ring.' };
        ctx.say(`<b>${m.kind === 'amanita' ? 'B' : 'A'}</b> — ${FACT[r]}${extra[r] || ''}`, 'good', 4200); ui.observe(`${m.kind === 'amanita' ? 'B' : 'A'}: ${r}`, 'seen');
        const n = seen.agaricus.size + seen.amanita.size; ctx.progress(n / 10); if (n >= 10) anim.wait(2, () => ctx.next());
      }
    },
    handler: { down() { return ui.tool === 'lens'; } },
  };
  const stepQuiz = {
    title: 'Label mushroom B', text: 'Drag each name onto its numbered marker.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0.6, 1.15, 1.5], [0.6, 0.3, 0.35], 1.6),
    enter() { const m = ms[1]; quiz = createLabelQuiz(ctx, Object.keys(m.anchors).map((name) => ({ name, at: m.anchors[name].clone(), object: m.g })), { onPlace: (it, n, all) => ctx.progress(n / all), onDone: () => anim.wait(0.8, () => ctx.next('All parts of the fruit body (basidiocarp) labelled.')) }); },
    update() { if (quiz) quiz.update(); },
    exit() { if (quiz) { quiz.dispose(); quiz = null; } },
  };
  const cut = new Set();
  const stepCut = {
    title: 'Cut off the caps', text: 'With the <b>scalpel</b>, cut through each stalk just below the cap (drag across it).', tool: 'scalpel', shot: TRAY,
    skip() { ms.forEach((m) => cutCap(m, true)); },
    handler: {
      down(p) { if (!input.pick(ms.map((m) => m.holder), true)) return false; if (!ctx.requireTool('scalpel')) return true; this.last = [p.x, p.y]; return true; },
      move(p) {
        if (!this.last) return; const W = ctx.stage.clientWidth; const H = ctx.stage.clientHeight;
        ms.forEach((m) => {
          if (cut.has(m)) return; const a1 = new THREE.Vector3(0, m.stH - 0.3, 0); const b1 = new THREE.Vector3(0, m.stH - 0.06, 0); m.g.localToWorld(a1); m.g.localToWorld(b1); input.project(a1, a1, W, H); input.project(b1, b1, W, H);
          if (crosses(this.last[0], this.last[1], p.x, p.y, a1.x, a1.y, b1.x, b1.y)) cutCap(m, false);
        });
        this.last = [p.x, p.y];
      },
      up() { this.last = null; },
    },
  };
  function cutCap(m, instant) {
    cut.add(m); const capG = new THREE.Group(); m.g.add(capG); [m.parts.cap, m.parts.gills].forEach((o) => capG.add(o)); m.g.children.filter((c) => c.position.y > m.stH - 0.03 && c !== capG).forEach((c) => capG.add(c));
    m.capG = capG; if (!instant) { sfx.play('cut'); m.g.localToWorld(tmp.set(0, m.stH - 0.1, 0)); fx.burst(tmp, 0xf3efe4, 5, 0.08, ctx.BENCH_Y + 0.05); anim.add(0.5, (k) => { capG.position.y = k * 0.12; }); if (cut.size === 2) anim.wait(0.7, () => ctx.next('Both caps are off.')); }
  }
  const stepPrint = {
    title: 'Take spore prints', text: 'Tap each cap to lay it gills-down across the line between the white and black halves of the paper, then tap the beakers to cover them against draughts.', tool: null, autoTool: 'hand', shot: S([0, 1.9, 2.8], [0, 0.1, 0.9], 3.0),
    skip() { ms.forEach((m, i) => placeCap(m, i, true)); beakers.forEach((b, i) => cover(b, i, true)); },
    handler: { down() {
      const m = ms.find((q) => q.capG && !q.onPaper && input.pick([q.capG], true)); if (m) { placeCap(m, ms.indexOf(m), false); return true; }
      const bi = beakers.findIndex((b) => !b.over && input.pick([b.group], true)); if (bi < 0) return false;
      if (!ms[bi].onPaper) { ctx.say('Put the cap on the paper first.', 'hint', 1400); return true; }
      cover(beakers[bi], bi, false); if (beakers.every((b) => b.over)) anim.wait(1, () => ctx.next('Covered. Leave them overnight.')); return true;
    } },
  };
  function placeCap(m, i, instant) {
    m.onPaper = true; const cg = m.capG; world.attach(cg); const to = new THREE.Vector3(i ? 0.5 : -0.5, 0.05, 1.35);
    const q1 = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, 0)); const target = to.clone(); target.y = 0.05 - (m.stH - 0.02);
    if (instant) { cg.quaternion.copy(q1); cg.position.copy(target); return; }
    const from = cg.position.clone(); const q0 = cg.quaternion.clone(); sfx.play('pick');
    anim.add(0.9, (k) => { cg.position.lerpVectors(from, target, k); cg.position.y += Math.sin(Math.PI * k) * 0.4; cg.quaternion.slerpQuaternions(q0, q1, k); }, { ease: ease.inOut, done: () => sfx.play('place') });
  }
  function cover(b, i, instant) { b.over = true; const to = new THREE.Vector3(i ? 0.5 : -0.5, 0.62, 1.35); if (instant) { b.group.position.copy(to); return; } const from = b.group.position.clone(); sfx.play('glass'); anim.add(0.8, (k) => { b.group.position.lerpVectors(from, to, k); b.group.position.y += Math.sin(Math.PI * k) * 0.4; }); }
  let clock = null;
  const stepNight = {
    title: 'Overnight', text: 'Run the clock forward 12 hours, then tap the beakers and caps to lift them off.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0, 1.6, 2.6], [0, 0.1, 1.3], 2.3),
    enter() { clock = timelapse(ctx, { step: 12, unit: 'h', onTick: (h, done) => { prints.forEach((p) => { p.m.material.opacity = clamp(h / 12); }); if (done) { clock.show(false); this.ready = true; } } }); },
    skip() { prints.forEach((p) => { p.m.material.opacity = 1; }); lift(true); },
    exit() { if (clock) clock.remove(); clock = null; },
    handler: { down() { if (!stepNight.ready) return false; if (!input.pick([...beakers.map((b) => b.group), ...ms.map((m) => m.capG)], true)) return false; lift(false); return true; } },
  };
  function lift(instant) {
    beakers.forEach((b, i) => { const to = new THREE.Vector3(i ? 1.9 : -1.9, 0.62, 1.35); if (instant) b.group.position.copy(to); else { const from = b.group.position.clone(); anim.add(0.8, (k) => b.group.position.lerpVectors(from, to, k)); } });
    ms.forEach((m, i) => { if (!m.capG) return; const to = m.capG.position.clone(); to.x = i ? 1.45 : -1.45; to.z = 0.95; if (instant) m.capG.position.copy(to); else { const from = m.capG.position.clone(); anim.add(0.8, (k) => { m.capG.position.lerpVectors(from, to, k); m.capG.position.y += Math.sin(Math.PI * k) * 0.3; }); } });
    if (!instant) anim.wait(1.0, () => { ui.observe('Spore print A', 'dark purple-brown'); ui.observe('Spore print B', 'white'); ctx.next('A left a dark brown print (seen on the white half); B a white print, visible only on the black half.'); });
    else { ui.observe('Spore print A', 'dark purple-brown'); ui.observe('Spore print B', 'white'); }
  }
  const stepJudge = {
    title: 'Edible or poisonous?', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: TRAY,
    enter() {
      const ask2 = () => ui.chooseMany(ctx.stage.clientWidth / 2, ctx.stage.clientHeight * 0.1, 'Which characters of B are danger signs?', [{ label: 'Volva (cup) at the base', value: 'volva' }, { label: 'White gills', value: 'gills' }, { label: 'White spore print', value: 'print' }, { label: 'Has a stalk', value: 'stalk' }, { label: 'Has a cap', value: 'cap' }], (v) => {
        const want = ['gills', 'print', 'volva']; const ok = want.every((w) => v.includes(w)) && v.length === 3;
        if (!ok) { ctx.mistake('All mushrooms have a cap and a stalk. The Amanita warning signs are the volva, white gills and a white spore print (often with a ring).', 2); anim.wait(0.4, ask2); return; }
        ask(ctx, 'So mushroom B (Amanita) is…', [{ label: 'Poisonous — never eat it', value: 'p' }, { label: 'Edible after cooking', value: 'e' }], 'p', { delay: 0.2, ok: 'Poisonous. Amanitas cause most mushroom deaths (death cap, fly agaric); cooking does not destroy their toxins. Never eat a wild mushroom unless an expert identifies it — A, the field mushroom, is edible, but young Amanitas can look similar.', wrong: 'Cooking does not destroy Amanita toxins.' });
      });
      anim.wait(0.6, ask2);
    },
    exit() { ui.clearChooser(); },
  };
  const stepPreserve = {
    title: 'Preserve the specimens', text: 'Tap the jar of 4% formalin to preserve both specimens, labelled with name, date and place of collection.', tool: null, autoTool: 'hand', shot: S([1.4, 1.6, 1.6], [1.6, 0.4, -0.3], 2.2),
    handler: { down() { if (!input.pick([jar.group], true)) return false; sfx.play('drop'); ms.forEach((m) => { m.holder.visible = false; if (m.capG) m.capG.visible = false; }); ctx.next('Preserved in formalin: they keep their shape for study (FAA can also be used).'); return true; } },
  };
  const steps = [stepLens, stepQuiz, stepCut, stepPrint, stepNight, stepJudge, stepPreserve];
  ctx.debug = { ms };
  void rng;
  return {
    tools: ['hand', 'lens', 'scalpel'],
    steps,
    update() { lens.update(); if (quiz) quiz.update(); },
    result() { return { title: 'Mushroom identification', rows: [['A: Agaricus (field mushroom)', 'white cap, pink-brown free gills, ring, no volva, brown spore print — edible'], ['B: Amanita muscaria (fly agaric)', 'red warty cap, white gills, ring, volva, white spore print — poisonous']], conclusion: 'A mushroom is the fruit body (basidiocarp) of a fungus: pileus, gills bearing basidiospores, stipe, annulus and, in Amanita, a volva. Gill colour, spore-print colour and the presence of a volva and ring are key characters. Amanitas are deadly; no simple test separates edible from poisonous mushrooms, so wild mushrooms must never be eaten unless identified by an expert.' }; },
    dispose() { lens.dispose(); if (quiz) quiz.dispose(); ui.clearChooser(); },
  };
}
