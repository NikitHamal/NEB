// Mitosis in onion root tip: a temporary acetocarmine squash, made and studied the NEB way.
// Cut the terminal 1-2 cm of fresh roots, put them in acetocarmine with a few drops of 1N HCl in
// a watch glass, warm gently without boiling (the acid softens the middle lamella so the cells
// will separate; the stain binds the chromosomes), keep only the extreme tip on a slide, add
// fresh stain, lower a coverslip, squash with the thumb through blotting paper, then focus under
// low power, find the meristem, go to high power, identify each stage and work out the mitotic
// index of a field.
import { THREE } from '../../engine.js';
import { watchGlass, reagentBottle, spiritLamp } from '../props.js';
import { buildStation, stepDrop, stepCoverslip, stepToStage, createScopeView } from '../slideprep.js';
import { buildOnion } from '../specimens/onion.js';
import { createOnionField, PHASE_INFO } from '../fields/onion.js';
import { ease, clamp } from '../kit.js';

const STAIN = 0x8b1538;
const STAGES = ['prophase', 'metaphase', 'anaphase', 'telophase'];
const cap = (s) => s[0].toUpperCase() + s.slice(1);

export function create(ctx) {
  const { world, input, tools, fx, anim, sfx, ui } = ctx;
  const st = buildStation(ctx, { stainColor: STAIN, tileX: 0.1, tileZ: 0.35, slideDX: 0.42 });
  const onion = buildOnion(ctx.quality);
  onion.root.position.set(-0.52, 0.042, 0.32); world.add(onion.root);
  const wg = watchGlass(STAIN, 0.85); wg.scale.setScalar(0.7); wg.position.set(0.55, 0.03, -0.12); world.add(wg);
  const mat = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.012, 0.75), new THREE.MeshStandardMaterial({ color: 0x1f3b2d, roughness: 0.85 }));
  mat.position.set(-0.28, 0.036, 0.35); mat.receiveShadow = true; world.add(mat);
  const lamp = spiritLamp(); lamp.position.set(0.95, 0, -0.42); world.add(lamp);
  const b1 = reagentBottle('Acetocarmine', STAIN, '2% in 45% acetic acid'); b1.position.set(-0.35, 0, -0.55); world.add(b1);
  const b2 = reagentBottle('1N HCl', 0xe0f2fe, 'hydrochloric acid'); b2.position.set(0.05, 0, -0.6); world.add(b2);
  ctx.surfaces.push(st.tile, mat);

  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3(); const prev = new THREE.Vector2(); const cur = new THREE.Vector2();
  const projectFn = (v, out) => input.project(v, out, ctx.stage.clientWidth, ctx.stage.clientHeight);
  const wgCenter = () => wg.getWorldPosition(new THREE.Vector3());
  const tipsCut = []; const tipsInGlass = [];
  ctx.debug = { tipsCut, tipsInGlass, slide: st.slide, wg };
  let temp = 24; let warmTime = 0; let boiled = false; let squashTaps = 0; let squash = 'good';
  let field = null; let view = null; let found = new Set(); let tally = null;

  const SHOT_ROOTS = { pos: [-0.05, 1.62, 1.0], target: [-0.06, 0.84, 0.36], fit: 0.8 };
  const SHOT_GLASS = { pos: [0.75, 1.75, 1.15], target: [0.78, 1.05, -0.3], fit: 1.3 };
  const SHOT_SLIDE = { pos: [0.52, 1.32, 1.02], target: [0.52, 0.84, 0.52], fit: 0.55 };

  // ---- cutting the tips: a stroke of the scalpel across the dashed line -----------------------
  const guideLine = (() => {
    const pts = onion.roots.map((r) => r.cutPoint.clone());
    pts.sort((a, b) => a.z - b.z);
    const g = new THREE.BufferGeometry().setFromPoints([pts[0].clone().add(tmp.set(0, 0.002, -0.06)), pts[pts.length - 1].clone().add(tmp.set(0, 0.002, 0.06))]);
    const l = new THREE.Line(g, new THREE.LineDashedMaterial({ color: 0x0ea5e9, dashSize: 0.015, gapSize: 0.01, depthTest: false, transparent: true }));
    l.computeLineDistances(); l.renderOrder = 9; l.visible = false;
    onion.root.add(l);
    return l;
  })();
  function screenOf(localP, out) { tmp2.copy(localP); onion.root.localToWorld(tmp2); projectFn(tmp2, out); return out; }
  function segCross(ax, ay, bx, by, cx, cy, dx, dy) {
    const d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx); if (Math.abs(d) < 1e-6) return false;
    const u = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d; const v = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d;
    return u >= 0 && u <= 1 && v >= 0 && v <= 1;
  }
  const sA = new THREE.Vector3(); const sB = new THREE.Vector3();
  let slicing = false; let farWarned = false;
  const stepCut = {
    title: 'Cut the root tips',
    text: 'With the <b>scalpel</b>, slice across the roots along the dotted line, about 1–2 cm from their tips. Cut at least two tips.',
    hint: 'Drag the blade across the roots, crossing the dotted line. Each root you cross loses its tip.',
    tool: 'scalpel', shot: SHOT_ROOTS,
    enter() { guideLine.visible = true; ctx.say('These roots grew in water for three days. Cell division happens only in the meristem, just behind the root cap at the very tip.', 'info', 6000); },
    skip() { onion.roots.slice(0, 2).forEach((r) => cutRoot(r)); },
    update() { guideLine.material.dashOffset = (guideLine.material.dashOffset || 0) - 0.001; },
    handler: {
      down(p) { if (!ctx.requireTool('scalpel')) return true; slicing = true; prev.set(p.x, p.y); tools.press(1); return true; },
      move(p) {
        if (!slicing) return;
        cur.set(p.x, p.y);
        onion.roots.forEach((r) => {
          if (r.cut) return;
          // the stroke crossing the root near the line cuts it; crossing far up the root is a mistake
          const near = r.curve.getPointAt(Math.max(0, r.cutT - 0.04)); const nearB = r.curve.getPointAt(Math.min(1, r.cutT + 0.04));
          screenOf(near, sA); screenOf(nearB, sB);
          if (segCross(prev.x, prev.y, cur.x, cur.y, sA.x, sA.y, sB.x, sB.y)) { cutRoot(r); return; }
          const far = r.curve.getPointAt(0.3); const farB = r.curve.getPointAt(0.45);
          screenOf(far, sA); screenOf(farB, sB);
          if (!farWarned && segCross(prev.x, prev.y, cur.x, cur.y, sA.x, sA.y, sB.x, sB.y)) { farWarned = true; ctx.mistake('That is too far up the root — only the last 1–2 cm hold the meristem. Older parts have stopped dividing.', 2); }
        });
        prev.copy(cur);
      },
      up() { slicing = false; tools.press(0); },
    },
  };
  function cutRoot(r) {
    r.cut = true; tipsCut.push(r); sfx.play('cut');
    tmp.copy(r.cutPoint); onion.root.localToWorld(tmp); fx.burst(tmp, 0xf8fafc, 3, 0.06, tmp.y - 0.01);
    const from = r.tip.position.clone(); const to = from.clone().add(tmp.set(0.03, 0, (Math.random() - 0.5) * 0.03));
    anim.add(0.4, (k) => { r.tip.position.lerpVectors(from, to, k); r.tip.rotation.y = k * 0.3; }, { ease: ease.out });
    ctx.progress(Math.min(1, tipsCut.length / 2));
    if (tipsCut.length === 2) anim.wait(0.6, () => { guideLine.visible = false; ctx.next('Two tips cut cleanly, each about 1.2 cm long.'); });
  }

  // ---- into the stain ---------------------------------------------------------------------------
  const stepToGlass = {
    title: 'Put the tips in stain',
    text: 'With the <b>forceps</b>, pick up each cut tip and drop it into the watch glass of acetocarmine with a few drops of 1N HCl.',
    hint: 'Tap a loose root tip with the forceps; it goes into the watch glass.',
    tool: 'forceps', shot: { pos: [0.2, 1.75, 1.15], target: [0.12, 0.88, 0.18], fit: 1.15 },
    skip() { tipsCut.forEach((r) => { if (!tipsInGlass.includes(r)) intoGlass(r, true); }); },
    handler: {
      hover() { const h = input.pick(tipsCut.filter((r) => !tipsInGlass.includes(r)).map((r) => r.tip)); fx.highlight(h && ui.tool === 'forceps' ? h.object.parent : null); },
      down() {
        const cand = tipsCut.filter((r) => !tipsInGlass.includes(r));
        let best = null; let bd = 42;
        cand.forEach((r) => { r.tip.getWorldPosition(tmp); projectFn(tmp, tmp2); const d = Math.hypot(tmp2.x - input.ptr.x, tmp2.y - input.ptr.y); if (d < bd) { bd = d; best = r; } });
        if (!best) return false;
        if (!ctx.requireTool('forceps')) return true;
        tools.action(1); anim.wait(0.2, () => tools.action(0)); sfx.play('pick');
        intoGlass(best, false);
        return true;
      },
    },
  };
  function intoGlass(r, instant) {
    tipsInGlass.push(r); fx.highlight(null);
    const start = new THREE.Vector3(); r.tip.getWorldPosition(start);
    world.attach(r.tip);
    const end = wgCenter().add(tmp.set((tipsInGlass.length - 1.5) * 0.05, 0.04, 0.0)); world.worldToLocal(end);
    const s0 = world.worldToLocal(start.clone());
    const done = () => { sfx.play('drop'); ctx.progress(tipsInGlass.length / 2); if (tipsInGlass.length === 2 && !instant) anim.wait(0.5, () => ctx.next('Both tips are in the stain–acid mixture (about 9 parts acetocarmine to 1 part 1N HCl).')); };
    const settleIn = () => { wg.attach(r.tip); };
    if (instant) { r.tip.position.copy(end); settleIn(); return; }
    anim.add(0.7, (k) => { r.tip.position.lerpVectors(s0, end, k); r.tip.position.y += Math.sin(Math.PI * k) * 0.25; r.tip.rotation.z = k * 2; }, { ease: ease.inOut, done: () => { settleIn(); done(); } });
  }

  // ---- warming ------------------------------------------------------------------------------
  let warming = false; let steamT = 0; const glassHome = wg.position.clone();
  const overFlame = new THREE.Vector3(); lamp.getWorldPosition(overFlame); world.worldToLocal(overFlame); overFlame.y += 0.5;
  const stepWarm = {
    title: 'Warm gently over the flame',
    text: 'Light the <b>spirit lamp</b>, then press and hold the watch glass to hold it over the flame. Warm until it just steams — about 60 °C — for a few seconds. <b>Do not boil.</b>',
    hint: 'Tap the lamp to light it. Then press and hold on the watch glass; let go when the bar is in the green and before it boils. Repeat in short bursts until the bar fills.',
    tool: 'hand', shot: SHOT_GLASS, autoTool: 'hand',
    skip() { warmTime = 4; temp = 60; lamp.userData.flame.visible = true; tintTips(1); },
    update(dt) {
      const flame = lamp.userData.flame;
      if (flame.visible) { const f = 1 + Math.sin(performance.now() * 0.02) * 0.06; flame.scale.set(f, 2 - f, f); }
      const k = warming ? 1 : 0;
      wg.position.lerp(warming ? overFlame : glassHome, 1 - Math.pow(0.004, dt));
      const over = wg.position.distanceTo(overFlame) < 0.06;
      temp += (over && flame.visible ? 16 : 0) * dt - (temp - 24) * 0.12 * dt * (1 - k * 0.5);
      if (temp > 52 && temp < 80) { warmTime += dt; tintTips(clamp(warmTime / 4)); }
      if (temp > 90 && !boiled) { boiled = true; ctx.mistake('It boiled! Boiling destroys the chromosomes and breaks the tissue. Warm in short bursts, just till it steams.', 6); }
      steamT -= dt;
      if (temp > 50 && steamT <= 0) { steamT = 0.12; wg.getWorldPosition(tmp); tmp.y += 0.08; fx.burst(tmp, 0xf8fafc, 1, 0.12, tmp.y + 0.3); }
      if (Math.round(temp) !== this.shown) { this.shown = Math.round(temp); ui.setText(`${this.text}<br><span class="bh-gauge" style="--t:${clamp((temp - 20) / 80).toFixed(3)}"><i></i></span> <b>${this.shown} °C</b>`); }
      ctx.progress(clamp(warmTime / 4));
      if (warmTime >= 4 && !this.done) { this.done = true; warming = false; anim.wait(0.6, () => ctx.next('Warmed without boiling: the HCl has softened the middle lamella and the stain has entered the chromosomes. The tips are now deep red.')); }
    },
    handler: {
      down() {
        const hl = input.pick([lamp]); if (hl) { if (!lamp.userData.flame.visible) { lamp.userData.flame.visible = true; sfx.play('click'); ctx.say('Lamp lit.', 'info', 1500); } return true; }
        const h = input.pick([wg]); if (!h) return false;
        if (!lamp.userData.flame.visible) { ctx.say('Light the spirit lamp first — tap it.', 'hint', 2500); return true; }
        warming = true; return true;
      },
      up() { warming = false; },
      cancel() { warming = false; },
    },
    exit() { warming = false; },
  };
  function tintTips(k) { tipsInGlass.forEach((r) => r.tipMat.color.setRGB(0.93 - 0.42 * k, 0.87 - 0.75 * k, 0.68 - 0.5 * k)); }

  // ---- onto the slide and trim -------------------------------------------------------------
  let onSlide = null; let trimmed = false;
  const stepToSlide = {
    title: 'Put one tip on the slide',
    text: 'Take one stained tip from the watch glass with the <b>forceps</b> and lay it in the middle of the clean slide.',
    hint: 'Tap one of the red tips in the watch glass.',
    tool: 'forceps', shot: { pos: [0.42, 1.6, 1.15], target: [0.4, 0.86, 0.25], fit: 0.95 },
    skip() { placeOnSlide(tipsInGlass[0], true); },
    handler: {
      down() {
        let best = null; let bd = 46;
        tipsInGlass.forEach((r) => { r.tip.getWorldPosition(tmp); projectFn(tmp, tmp2); const d = Math.hypot(tmp2.x - input.ptr.x, tmp2.y - input.ptr.y); if (d < bd) { bd = d; best = r; } });
        if (!best) return false;
        if (!ctx.requireTool('forceps')) return true;
        sfx.play('pick'); placeOnSlide(best, false); return true;
      },
    },
  };
  function placeOnSlide(r, instant) {
    onSlide = r; st.specimen = r.tip; world.attach(r.tip);
    const end = new THREE.Vector3(st.slide.position.x, st.slideTopY + onion.rootRadius, st.slide.position.z);
    const s0 = r.tip.position.clone();
    if (instant) { r.tip.position.copy(end); r.tip.rotation.set(0, 0, 0); return; }
    anim.add(0.8, (k) => { r.tip.position.lerpVectors(s0, end, k); r.tip.position.y += Math.sin(Math.PI * k) * 0.2; r.tip.rotation.z = (1 - k) * 2; }, { ease: ease.inOut, done: () => { sfx.play('place'); ctx.next(); } });
  }
  let trimMark = null;
  const stepTrim = {
    title: 'Keep only the very tip',
    text: 'With the <b>scalpel</b>, cut off and discard the older part, keeping just the last 1–2 mm — the dark-staining meristem.',
    hint: 'Tap the glowing ring near the end of the tip with the scalpel.',
    tool: 'scalpel', shot: SHOT_SLIDE,
    enter() { const r = onSlide; tmp.set(0.035, 0, 0); r.tip.localToWorld(tmp); trimMark = fx.mark(tmp, 0.015, 0xf59e0b); },
    skip() { trim(true); },
    exit() { if (trimMark) fx.unmark(trimMark); trimMark = null; },
    handler: {
      down(p) {
        projectFn(trimMark.position, tmp2);
        if (Math.hypot(tmp2.x - p.x, tmp2.y - p.y) > 40) { if (input.pick([st.slide])) { ctx.mistake('Trim close to the tip: the dividing cells are only in the terminal 1–2 mm. Cut at the ring.', 2); return true; } return false; }
        if (!ctx.requireTool('scalpel')) return true;
        tools.press(1); anim.wait(0.15, () => tools.press(0)); trim(false); return true;
      },
    },
  };
  function trim(instant) {
    trimmed = true; sfx.play('cut');
    const r = onSlide;
    r.tip.scale.set(0.35, 1, 1); r.tip.position.x += 0.02;
    if (!instant) { fx.burst(trimMark.position, 0xf1e4b5, 3, 0.06, trimMark.position.y - 0.01); anim.wait(0.5, () => ctx.next('Only the meristematic tip remains.')); }
  }

  // ---- stain, coverslip, squash -------------------------------------------------------------
  const stepStain = stepDrop(ctx, st, { title: 'Add a drop of acetocarmine', text: 'With the <b>dropper</b>, put one drop of fresh acetocarmine on the tip.', color: STAIN, shot: SHOT_SLIDE });
  const stepCover = stepCoverslip(ctx, st, { shot: SHOT_SLIDE });
  let paper = null; let pressT = 0;
  const stepSquash = {
    title: 'Squash the tip',
    text: 'Fold <b>blotting paper</b> over the coverslip and tap it gently with your thumb, straight down, until the tip spreads into a thin pink haze. Do not slide the coverslip.',
    hint: 'Tap (quick press and release) on the coverslip 5 times. A long press smears it.',
    tool: 'hand', shot: SHOT_SLIDE, autoTool: 'hand',
    enter() {
      paper = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.004, 0.3), new THREE.MeshStandardMaterial({ color: 0xfafaf7, roughness: 0.95, transparent: true, opacity: 0.88 }));
      paper.position.set(st.slide.position.x, st.slideTopY + 0.02, st.slide.position.z); world.add(paper);
    },
    skip() { squashTaps = 5; spread(1); },
    exit() { if (paper) { world.remove(paper); paper.geometry.dispose(); paper.material.dispose(); paper = null; } },
    handler: {
      down() { if (!input.pick([paper, st.slide, st.coverslip])) return false; pressT = performance.now(); tools.press(1); return true; },
      up() {
        tools.press(0);
        const held = performance.now() - pressT;
        if (held > 650 && squash !== 'over') { squash = 'over'; ctx.mistake('That long press slid the coverslip and smeared the cells — many will be broken. Tap straight down instead.', 4); }
        squashTaps += 1; sfx.play('squish');
        paper.position.y = st.slideTopY + 0.012; anim.add(0.2, (k) => { paper.position.y = st.slideTopY + 0.012 + k * 0.008; });
        spread(Math.min(1, squashTaps / 5));
        ctx.progress(Math.min(1, squashTaps / 5));
        if (squashTaps === 5) anim.wait(0.6, () => ctx.next('The tip has spread into a single layer of cells.'));
      },
    },
  };
  function spread(k) { const r = onSlide; r.tip.scale.set(0.35 + k * 1.2, 1 - k * 0.7, 1 + k * 2.5); }

  // ---- microscope -----------------------------------------------------------------------------
  const stepStage = stepToStage(ctx, st, { shotStart: SHOT_SLIDE });
  function makeView() {
    if (view) return view;
    field = createOnionField({ squash, bubbles: st.bubbles, stain: boiled ? 0.55 : 1 });
    ctx.debug = { field };
    view = createScopeView(ctx, st, field, {
      objective: 10, focus: -700,
      onTap: (cell, e) => { if (ctx.step && ctx.step.onCell) ctx.step.onCell(cell, e); },
      onClosed: () => { if (ctx.step && ctx.step.needsEye) ctx.say('Look back into the eyepiece to carry on — tap the eyepiece.', 'hint', 3000); },
    });
    return view;
  }
  const eyeHandler = { down() { const h = input.pick(st.scope.pickables); if (h) { makeView().open(); return true; } return false; } };
  let sharpT = 0;
  const stepFocusLow = {
    title: 'Focus under low power (10×)',
    text: 'Look into the eyepiece. With the 10× objective in place, turn the <b>coarse</b> knob until the cells appear, then sharpen with the <b>fine</b> knob. Set the light with the diaphragm.',
    hint: 'Drag the Coarse knob up (or scroll on it) slowly until a pink haze of cells appears, then use Fine. The field sharpens only in a narrow band.',
    tool: null, needsEye: true, hideBelt: true, handler: eyeHandler,
    enter() { makeView().open(); sharpT = 0; },
    skip() { makeView(); },
    update(dt) {
      const e = view && view.eye; if (!e) return;
      const s = e.state;
      ctx.progress(clamp(1 - s.blur / 12));
      if (s.objective === 10 && s.sharp) { sharpT += dt; if (sharpT > 0.7 && !this.done) { this.done = true; ctx.next('In focus at 100×: rows of cells, darker near the tip.'); } } else sharpT = 0;
    },
  };
  const stepHigh = {
    title: 'Find the meristem, then go to 40×',
    text: 'Drag the field to bring the region just behind the root cap — small, square, tightly packed cells with big nuclei — to the centre. Then switch to <b>40×</b> and refocus with the <b>fine</b> knob only.',
    hint: 'Move toward the narrow, rounded end of the squash (the root tip), stop just behind the loose cap cells, then click 40× and use the Fine knob.',
    tool: null, needsEye: true, hideBelt: true, handler: eyeHandler,
    enter() { if (!view || !view.eye) makeView().open(); sharpT = 0; },
    skip() { const e = makeView(); e.open(); },
    update(dt) {
      const e = view && view.eye; if (!e) return;
      const s = e.state; const d = Math.hypot(s.cx - field.meristem.x, s.cy - field.meristem.y);
      ctx.progress(s.objective === 40 ? clamp(1 - s.blur / 8) : clamp(1 - d / 1200) * 0.5);
      if (s.objective === 40 && s.sharp && d < 320) { sharpT += dt; if (sharpT > 0.7 && !this.done) { this.done = true; ctx.next('400×, sharp, in the meristem: you can see chromosomes.'); } } else sharpT = 0;
      if (s.objective === 40 && d >= 320 && !this.warned && s.sharp) { this.warned = true; ctx.say('These cells are long and vacuolate — the zone of elongation; they no longer divide. Go back to 10× and move nearer the tip.', 'hint', 5000); }
    },
  };
  const stepIdentify = {
    title: 'Identify each stage of mitosis',
    text: 'Tap a dividing cell and name its stage. Find one each of <b>prophase, metaphase, anaphase</b> and <b>telophase</b>.',
    hint: 'Prophase: threads inside a round nucleus. Metaphase: a dark band across the middle. Anaphase: two groups of V-shapes moving apart. Telophase: two dense masses at the ends with a line between.',
    tool: null, needsEye: true, hideBelt: true, handler: eyeHandler,
    enter() { if (!view || !view.eye) makeView().open(); ctx.progress(0); },
    skip() { STAGES.forEach((s) => found.add(s)); },
    onCell(cell, e) {
      const eye = view.eye; if (!eye) return;
      if (e.blur > 2.5) { ctx.say('Too blurred to judge — focus first with the fine knob.', 'hint', 2500); return; }
      if (!cell) { ctx.say('Tap right on a cell.', 'hint', 1500); return; }
      const r = eye.view.getBoundingClientRect(); const sr = ctx.stage.getBoundingClientRect();
      ui.choose(r.left - sr.left + e.px, r.top - sr.top + e.py, 'Which stage is this cell in?', ['interphase'].concat(STAGES).map((s) => ({ label: cap(s), value: s })), (v) => {
        if (v === cell.phase) {
          sfx.play('ok');
          if (cell.phase !== 'interphase' && !found.has(cell.phase)) { found.add(cell.phase); eye.mark(cell.cx, cell.cy, cap(cell.phase)); ui.observe(cap(cell.phase), 'found'); }
          ctx.say(PHASE_INFO[cell.phase], 'good', 5000);
          ctx.progress(found.size / 4);
          if (found.size === 4 && !this.done) { this.done = true; anim.wait(1.5, () => ctx.next('All four stages found.')); }
        } else {
          eye.mark(cell.cx, cell.cy, '', 'bad');
          ctx.mistake(`Not ${v}. ${PHASE_INFO[cell.phase]}`, 3);
        }
      });
    },
  };
  const stepIndex = {
    title: 'Mitotic index of this field',
    text: 'Count the cells in this field and how many are dividing. Which is the mitotic index?',
    tool: null, needsEye: true, hideBelt: true, handler: eyeHandler,
    enter() {
      const e = view.eye; const s = e.state;
      tally = field.tally(s.cx, s.cy, 13000 / s.objective / 2);
      const div = tally.total - tally.interphase; const mi = tally.total ? (100 * div / tally.total) : 0;
      ui.observe('Cells in field', String(tally.total));
      STAGES.forEach((p) => ui.observe(cap(p), String(tally[p])));
      ui.observe('Interphase', String(tally.interphase));
      const right = Math.round(mi);
      const opts = [right, Math.round(100 * tally.interphase / Math.max(1, tally.total)), Math.max(1, Math.round(right / 2)), right + 9].filter((v, i, a) => a.indexOf(v) === i);
      opts.sort(() => Math.random() - 0.5);
      ui.setText(`In this field: <b>${tally.total}</b> cells, of which <b>${div}</b> are in prophase, metaphase, anaphase or telophase. Mitotic index = dividing cells ÷ total cells × 100. Pick the answer.`);
      const sr = ctx.stage.getBoundingClientRect(); void sr;
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, 60, 'Mitotic index (%)', opts.map((v) => ({ label: `${v} %`, value: v })), (v) => {
        if (v === right) { ui.observe('Mitotic index', `${mi.toFixed(1)} %`); ctx.next(`Right: ${div} ÷ ${tally.total} × 100 = ${mi.toFixed(1)} %. In the meristem a fair share of cells is always dividing; prophase is the longest phase, so it is the commonest.`); }
        else { ctx.mistake('Not quite. Mitotic index = (number of dividing cells ÷ total number of cells) × 100.', 3); anim.wait(0.4, ask); }
      });
      anim.wait(0.6, ask);
    },
    skip() { },
  };

  const steps = [stepCut, stepToGlass, stepWarm, stepToSlide, stepTrim, stepStain, stepCover, stepSquash, stepStage, stepFocusLow, stepHigh, stepIdentify, stepIndex];
  return {
    tools: ['hand', 'scalpel', 'forceps', 'dropper', 'needle'],
    steps,
    update(dt, t) { if (view) view.update(t); },
    result() {
      const div = tally ? tally.total - tally.interphase : 0;
      return {
        title: 'Mitosis in onion root tip',
        rows: tally ? [['Cells counted', String(tally.total)], ['Prophase', String(tally.prophase)], ['Metaphase', String(tally.metaphase)], ['Anaphase', String(tally.anaphase)], ['Telophase', String(tally.telophase)], ['Mitotic index', `${(100 * div / Math.max(1, tally.total)).toFixed(1)} %`], ['Air bubbles', String(st.bubbles)], ['Squash', squash === 'over' ? 'smeared' : 'even']] : [],
        conclusion: 'Cells in the root-tip meristem divide by mitosis. Prophase (condensing chromosomes in an intact nucleus), metaphase (chromosomes on the equatorial plate), anaphase (chromatids pulled to the poles) and telophase (two daughter nuclei and a cell plate) were all seen; most cells were in interphase. Each daughter cell receives the same 16 chromosomes.',
        explore: () => { if (view) view.open(); },
      };
    },
    dispose() { if (view) view.dispose(); if (field) field.dispose(); },
  };
}
