// Dissection of the earthworm (Pheretima) to display the alimentary canal, done the way it is
// done on the bench: turn the worm dorsal side up, pin both ends to the wax, cut the body wall
// along the mid-dorsal line from the posterior end forward, free the septa with a needle, peel
// the body wall back and pin it out, then study the gut with a hand lens and label it.
import { THREE } from '../../engine.js';
import { dissectingTray } from '../props.js';
import { pinModel } from '../tools.js';
import { createCut } from '../cut.js';
import { createLens } from '../lens.js';
import { createLabelQuiz } from '../labelquiz.js';
import { ease, clamp } from '../kit.js';
import { buildEarthworm, segX, xSeg, radiusAt, R0, CUT_THETA, organAt } from '../specimens/earthworm.js';

const FACTS = {
  'Buccal cavity': 'The <b>buccal cavity</b> (segments 1–3) opens at the crescent-shaped mouth under the prostomium.',
  Pharynx: 'The <b>pharynx</b> (segment 4) is a thick, muscular, pear-shaped chamber: it sucks in soil and food. Pharyngeal glands secrete mucus.',
  Oesophagus: 'The <b>oesophagus</b> (segments 5–7) is a narrow, thin-walled tube.',
  Gizzard: 'The <b>gizzard</b> (segment 8, into 9) is hard, round and glistening: its thick muscle wall grinds soil and decaying leaves.',
  Stomach: 'The <b>stomach</b> (segments 9–14) is a short, glandular, richly vascular tube. Its calciferous glands neutralise humic acid.',
  Intestine: 'The <b>intestine</b> runs from segment 15 to the anus. Yellow-brown chloragogen cells coat it; inside, the typhlosole fold (from 26) adds absorbing surface.',
  'Intestinal caeca': 'A pair of conical <b>intestinal caeca</b> arises in segment 26 and reaches forward to segment 22; they secrete amylase.',
  Hearts: 'Four pairs of <b>hearts</b> (segments 7, 9, 12, 13) link the dorsal and ventral blood vessels; they have valves and beat.',
};
const SEGS = { 'Buccal cavity': '1–3', Pharynx: '4', Oesophagus: '5–7', Gizzard: '8–9', Stomach: '9–14', Intestine: '15 to anus', 'Intestinal caeca': '26 → 22', Hearts: '7, 9, 12, 13' };

export function create(ctx) {
  const { THREE: T3, world, input, tools, fx, anim, sfx, ui } = ctx;
  void T3;
  const tray = dissectingTray(3.2, 1.9);
  world.add(tray);
  const waxY = tray.userData.waxY;
  const worm = buildEarthworm(ctx.quality);
  const spec = new THREE.Group(); spec.position.set(0, waxY, 0.05); world.add(spec);
  spec.add(worm.root);
  worm.body.rotation.x = Math.PI; // it arrives lying on its back
  ctx.surfaces.push(...worm.pickables, tray.userData.wax);

  const lens = createLens(ctx, { mag: 3.2, groundY: ctx.BENCH_Y + waxY + R0 });
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3(); const local = new THREE.Vector3();
  const pins = [];
  let cut = null; let quiz = null;
  const flapT = { 1: 0, '-1': 0 };
  const found = new Set();

  // the worm group's local frame is the frame the specimen module builds in
  function toWorm(worldP, out) { return worm.root.worldToLocal(out.copy(worldP)); }
  function wormToWorld(p, out) { return worm.root.localToWorld(out.copy(p)); }

  function insertPin(worldTip, outward, color) {
    const p = pinModel(color);
    p.scale.setScalar(0.75);
    p.traverse((o) => { if (o.isMesh) o.userData.noPick = true; });
    world.add(p);
    const local0 = world.worldToLocal(worldTip.clone());
    const tilt = 0.55;
    p.rotation.x = outward.z * tilt; p.rotation.z = -outward.x * tilt;
    const end = local0.clone(); end.y -= 0.035;
    const start = end.clone(); start.y += 0.32;
    p.position.copy(start);
    anim.add(0.42, (k) => { p.position.lerpVectors(start, end, k); }, { ease: ease.in, done: () => { sfx.play('pin'); fx.burst(worldTip, 0x3b2a22, 4, 0.12, worldTip.y - 0.01); } });
    pins.push(p);
    return p;
  }
  function screenDist(worldP, ptr) {
    input.project(worldP, tmp2, ctx.stage.clientWidth, ctx.stage.clientHeight);
    return Math.hypot(tmp2.x - ptr.x, tmp2.y - ptr.y);
  }
  function setFlaps(side, t, grabX) {
    flapT[side] = t;
    (side > 0 ? worm.right : worm.left).pose(t, grabX ?? 0);
    if (cut) cut.gape(Math.min(flapT[1], flapT[-1]) * 4);
  }

  const SHOT_WIDE = { pos: [0, 2.45, 2.05], target: [0, 0.92, 0.04], fit: 2.35 };
  const SHOT_ANT = { pos: [-0.62, 1.62, 0.8], target: [-0.66, 0.9, 0.05], fit: 0.9 };

  // ---- 1. orientation -----------------------------------------------------------------------
  let roll = Math.PI; let rolling = null;
  const stepOrient = {
    title: 'Turn the worm dorsal side up',
    text: 'The worm is lying on its back. Pick up the <b>forceps</b> and drag across the worm to roll it over.',
    hint: 'The ventral side is paler and shows the paired male pores on segment 18. The dorsal side is darker, with the dorsal blood vessel showing as a dark mid-line. Drag sideways across the worm with the forceps.',
    tool: 'forceps', shot: SHOT_WIDE,
    skip() { roll = 0; worm.body.rotation.x = 0; worm.root.position.y = worm.restY; },
    enter() { ctx.say('Your earthworm has been narcotised and washed. It is lying ventral side up — note the pale belly and the genital pores near the clitellum.', 'info', 6000); },
    handler: {
      hover(p) { const h = input.pick(worm.pickables); fx.highlight(h && ui.tool === 'forceps' ? worm.body : null); },
      down(p) {
        const h = input.pick(worm.pickables);
        if (!h) return false;
        if (!ctx.requireTool('forceps', 'Roll the worm over gently with the <b>forceps</b> — it is not pinned yet, so never cut now.')) return true;
        rolling = { x: p.x, y: p.y, base: roll };
        tools.press(1); tools.action(1); sfx.play('pick');
        return true;
      },
      move(p) {
        if (!rolling) return;
        const d = Math.hypot(p.x - rolling.x, p.y - rolling.y);
        roll = rolling.base - Math.PI * clamp(d / 110);
        worm.body.rotation.x = roll;
        worm.root.position.y = worm.restY + Math.sin(Math.PI * (1 - roll / Math.PI)) * 0.04;
      },
      up() {
        if (!rolling) return;
        rolling = null; tools.press(0); tools.action(0);
        const from = roll; const to = roll < Math.PI * 0.5 ? 0 : Math.PI;
        anim.add(0.45, (k) => { roll = from + (to - from) * k; worm.body.rotation.x = roll; worm.root.position.y = worm.restY + Math.sin(Math.PI * (1 - roll / Math.PI)) * 0.04; }, {
          ease: ease.outBack,
          done: () => {
            sfx.play('squish');
            if (to === 0) { fx.highlight(null); ctx.next('Dorsal side up: darker, with the dark mid-dorsal line of the dorsal blood vessel. The clitellum (14–16) marks the anterior third.'); }
          },
        });
      },
    },
  };

  // ---- 2. pin both ends ------------------------------------------------------------------------
  const endMarks = [];
  const stepPinEnds = {
    title: 'Pin both ends to the wax',
    text: 'Take the <b>pins</b>. Push one through the first few segments and one through the hind end, slanting away from the body.',
    hint: 'Tap the two glowing rings: one near the head (segments 2–3), one near the tail. Pins slope outward so they never get in the way of your scissors.',
    tool: 'pin', shot: SHOT_WIDE,
    enter() {
      [[2.5, -1], [98.5, 1]].forEach(([s, dir]) => {
        const p = wormToWorld(tmp.set(segX(s), radiusAt(segX(s)) * 0.9, 0), new THREE.Vector3());
        const m = fx.mark(p, 0.05); m.userData.seg = s; m.userData.dir = dir; endMarks.push(m);
      });
    },
    handler: {
      down(p) {
        let best = null; let bd = 40;
        endMarks.forEach((m) => { if (m.userData.used) return; const d = screenDist(m.position, p); if (d < bd) { bd = d; best = m; } });
        if (!best) {
          const h = input.pick(worm.pickables);
          if (h && ui.tool === 'pin') { ctx.mistake('Pin through the <b>ends</b> of the worm only — a pin through the middle would pierce the gut you are about to study.', 3); return true; }
          return false;
        }
        if (!ctx.requireTool('pin')) return true;
        best.userData.used = true;
        insertPin(best.position, tmp.set(best.userData.dir, 0, 0), 0xef4444);
        fx.unmark(best);
        if (endMarks.every((m) => m.userData.used)) { endMarks.length = 0; anim.wait(0.5, () => ctx.next('Both ends are pinned and the worm is lightly stretched.')); }
        return true;
      },
    },
    skip() { endMarks.forEach((m) => insertPin(m.position, tmp.set(m.userData.dir, 0, 0), 0xef4444)); },
    exit() { endMarks.forEach((m) => fx.unmark(m)); endMarks.length = 0; },
  };

  // ---- 3. the incision ---------------------------------------------------------------------
  let cutting = false; let stray = 0; let snipT = 0; let lastWrongEnd = 0;
  const projectFn = (v, out) => input.project(v, out, ctx.stage.clientWidth, ctx.stage.clientHeight);
  const bladeAt = new THREE.Vector3();
  const stepCut = {
    title: 'Cut along the mid-dorsal line',
    text: 'With the <b>fine scissors</b>, cut the body wall along the dotted line, just beside the dark dorsal vessel, from the <b>posterior end forward</b>.',
    hint: 'Start at the tail end of the line (right) and drag steadily along it to the head end. Keep the cut shallow and beside — not on — the dorsal blood vessel.',
    tool: ['scissors', 'scalpel'], shot: SHOT_WIDE,
    enter() {
      const pts = [];
      for (let s = 97; s >= 3; s -= 3) { const x = segX(s); const r = radiusAt(x); pts.push(new THREE.Vector3(x, r * Math.cos(CUT_THETA), r * Math.sin(CUT_THETA))); }
      cut = createCut(worm.root, pts, { width: 0.012, samples: 200, normal: (f, p, n) => n.set(0, p.y, p.z).normalize() });
    },
    aim(p, out) {
      if (cut && !cut.done && cut.screenDistance(p.x, p.y, projectFn) < 40) { cut.feedScreen(p.x, p.y, projectFn, 0, 30, out); return true; }
      return ctx.aimDefault(p, out);
    },
    update(dt) { if (cut) cut.update(dt); snipT -= dt; },
    skip() { cut.finish(); },
    handler: {
      down(p) {
        const near = cut.screenDistance(p.x, p.y, projectFn) < (p.touch ? 34 : 26);
        if (!near && !input.pick(worm.pickables)) return false;
        if (!ctx.requireTool(['scissors', 'scalpel'], 'Cutting needs the <b>fine scissors</b> (or the scalpel).')) return true;
        cutting = true; stray = 0; tools.press(1);
        this.move(p);
        return true;
      },
      move(p) {
        if (!cutting) return;
        const r = cut.feedScreen(p.x, p.y, projectFn, p.touch ? 30 : 22, 18, bladeAt);
        if (r === 0) {
          stray = 0;
          if (snipT <= 0) { snipT = 0.12; sfx.play(ui.tool === 'scissors' ? 'snip' : 'cut'); tools.action(ui.tool === 'scissors' ? 1 : 0); anim.wait(0.06, () => tools.action(0)); fx.burst(bladeAt, 0xf3d6c8, 2, 0.08, bladeAt.y - 0.01); }
          ctx.progress(cut.progress);
          if (cut.done) { cutting = false; tools.press(0); cut.showGuide(false); ctx.next('A clean incision through the body wall only — the gut below is untouched.'); }
        } else if (r === 1 && cut.progress < 0.04 && performance.now() - lastWrongEnd > 2500) {
          lastWrongEnd = performance.now();
          ctx.mistake('Begin at the <b>posterior</b> (tail) end of the line and work forward, so the head end, where the organs crowd together, is opened last and most carefully.', 2);
        } else if (r === 2) {
          stray += 1;
          if (stray === 8) ctx.mistake('Your blade wandered off the line. A stray cut tears the septa and can slice the gut or the dorsal vessel — follow the guide.', 4);
        }
      },
      up() { cutting = false; tools.press(0); },
    },
  };

  // ---- 4. septa ---------------------------------------------------------------------------------
  let teasing = false;
  function tearNear(s) {
    let torn = 0;
    worm.septaIdx.forEach((si, i) => {
      if (worm.septumState[i] >= 1 && Math.abs(si + 0.5 - s) < 2.5) {
        worm.septumState[i] = 0.99;
        anim.add(0.3, (k) => worm.tearSeptum(i, 1 - k), { ease: ease.out });
        sfx.play('tear');
      }
    });
    worm.septumState.forEach((v) => { if (v < 1) torn += 1; });
    return torn / worm.septaIdx.length;
  }
  const stepSepta = {
    title: 'Free the septa with a needle',
    text: 'The body wall is still tied to the gut by thin <b>septa</b> at every segment. Run the <b>dissecting needle</b> along the cut to tease them free.',
    hint: 'Hold the needle and drag along the incision, end to end. You will feel each septum give.',
    tool: 'needle', shot: { pos: [0.35, 1.75, 1.35], target: [0, 0.9, 0.04], fit: 2.25 },
    enter() {
      worm.inside.visible = true;
      anim.add(0.8, (k) => { setFlaps(1, 0.3 * k, 0); setFlaps(-1, 0.3 * k, 0); });
      ctx.say('Look into the slit: thin pink membranes, the septa, divide the body cavity at every segment.', 'info', 5000);
    },
    skip() { worm.septaIdx.forEach((_, i) => worm.tearSeptum(i, 0)); worm.septumState.fill(0); },
    aim(p, out) {
      if (cut.nearestScreen(p.x, p.y, projectFn, local) < 40) { worm.root.localToWorld(out.copy(local)); out.y -= 0.01; return true; }
      return ctx.aimDefault(p, out);
    },
    handler: {
      down(p) {
        if (cut.nearestScreen(p.x, p.y, projectFn, local) > (p.touch ? 40 : 30)) return false;
        if (!ctx.requireTool('needle', 'Septa are teased apart with the <b>dissecting needle</b>, not cut.')) return true;
        teasing = true; tools.press(1); this.move(p); return true;
      },
      move(p) {
        if (!teasing) return;
        if (cut.nearestScreen(p.x, p.y, projectFn, local) > 44) return;
        const pr = tearNear(xSeg(local.x));
        ctx.progress(pr);
        if (pr > 0.9) {
          teasing = false; tools.press(0);
          worm.septaIdx.forEach((_, i) => { if (worm.septumState[i] >= 1) worm.tearSeptum(i, 0); });
          ctx.next('Every septum is free; the body wall can now be laid open.');
        }
      },
      up() { teasing = false; tools.press(0); },
    },
  };

  // ---- 5. peel back -----------------------------------------------------------------------------
  let grab = null;
  const stepPeel = {
    title: 'Peel the body wall back',
    text: 'With the <b>forceps</b>, catch the edge of each flap of body wall and draw it outward until it lies flat on the wax. Do both sides.',
    hint: 'Press on one cut edge and drag away from the worm. Let go once it lies flat; do the other side too.',
    tool: 'forceps', shot: { pos: [0, 2.2, 1.6], target: [-0.2, 0.9, 0.05], fit: 2.0 },
    skip() { setFlaps(1, 1, 0); setFlaps(-1, 1, 0); },
    handler: {
      hover() { const h = input.pick(worm.flapMeshes); fx.highlight(h && ui.tool === 'forceps' ? h.object.parent : null); },
      down(p) {
        const h = input.pick(worm.flapMeshes);
        if (!h) return false;
        if (!ctx.requireTool('forceps')) return true;
        const side = worm.right.group === h.object.parent ? 1 : -1;
        if (flapT[side] >= 0.99) return false;
        toWorm(h.point, local);
        grab = { side, x: local.x }; tools.press(1); tools.action(1); sfx.play('pick');
        return true;
      },
      move() {
        if (!grab) return;
        const pt = input.planePoint(ctx.BENCH_Y + waxY + R0 * 0.9, tmp);
        if (!pt) return;
        toWorm(pt, local);
        const t = clamp((grab.side * local.z - R0 * 0.3) / (R0 * 2.4));
        setFlaps(grab.side, Math.max(0.12, t), grab.x);
      },
      up() {
        if (!grab) return;
        const { side, x } = grab; grab = null; tools.press(0); tools.action(0);
        const from = flapT[side]; const to = from > 0.5 ? 1 : 0.15;
        anim.add(to === 1 ? 0.5 : 0.35, (k) => setFlaps(side, from + (to - from) * k, x * (1 - k)), {
          ease: to === 1 ? ease.out : ease.outBack,
          done: () => {
            if (to === 1) sfx.play('squish');
            else ctx.say('Not far enough — the elastic body wall springs back. Draw it all the way out.', 'hint', 3000);
            if (flapT[1] >= 0.99 && flapT[-1] >= 0.99) { fx.highlight(null); ctx.next('The body wall lies open on both sides, inner surface up. The alimentary canal runs straight down the middle.'); }
          },
        });
      },
    },
  };

  // ---- 6. pin the flaps ---------------------------------------------------------------------------
  const flapMarks = [];
  const stepPinFlaps = {
    title: 'Pin the flaps open',
    text: 'Pin each flap to the wax with <b>pins</b> through its edge, slanting outward: three on each side.',
    hint: 'Tap each glowing ring along the edges of the opened body wall.',
    tool: 'pin', shot: { pos: [0, 2.3, 1.75], target: [0, 0.9, 0.05], fit: 2.3 },
    enter() {
      [8, 34, 70].forEach((s) => [1, -1].forEach((side) => {
        const p = wormToWorld((side > 0 ? worm.right : worm.left).edgePoint(segX(s), 0.8, 1, tmp), new THREE.Vector3());
        const m = fx.mark(p, 0.04); m.userData.side = side; flapMarks.push(m);
      }));
    },
    handler: {
      down(p) {
        let best = null; let bd = 38;
        flapMarks.forEach((m) => { if (m.userData.used) return; const d = screenDist(m.position, p); if (d < bd) { bd = d; best = m; } });
        if (!best) return false;
        if (!ctx.requireTool('pin')) return true;
        best.userData.used = true;
        insertPin(best.position, tmp.set(0, 0, best.userData.side), 0x2563eb);
        fx.unmark(best);
        ctx.progress(flapMarks.filter((m) => m.userData.used).length / flapMarks.length);
        if (flapMarks.every((m) => m.userData.used)) { flapMarks.length = 0; anim.wait(0.5, () => ctx.next('Pinned out. Now flood the tray with water so the organs float apart and do not dry.')); }
        return true;
      },
    },
    skip() { flapMarks.forEach((m) => insertPin(m.position, tmp.set(0, 0, m.userData.side), 0x2563eb)); },
    exit() { flapMarks.forEach((m) => fx.unmark(m)); flapMarks.length = 0; },
  };

  // ---- 7. flood the tray ---------------------------------------------------------------------------
  const water = new THREE.Mesh(new THREE.PlaneGeometry(3.1, 1.8), new THREE.MeshPhysicalMaterial({ color: 0xcfe9f2, roughness: 0.04, transparent: true, opacity: 0.0, clearcoat: 1, depthWrite: false, envMapIntensity: 1.5 }));
  water.rotation.x = -Math.PI / 2; water.position.y = waxY + 0.002; water.renderOrder = 8; water.userData.noPick = true; water.visible = false;
  tray.add(water);
  const stream = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.009, 1, 8, 1, true), new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, roughness: 0.05, transparent: true, opacity: 0.55, clearcoat: 1, depthWrite: false }));
  stream.visible = false; stream.userData.noPick = true; ctx.scene.add(stream);
  const stepFlood = {
    title: 'Cover the dissection with water',
    text: 'Squeeze the <b>wash bottle</b> over the tray until the worm is just covered.',
    hint: 'Pick the wash bottle and press and hold anywhere over the tray.',
    tool: 'washbottle', shot: SHOT_WIDE,
    skip() { water.visible = true; water.material.opacity = 0.13; water.position.y = waxY + 0.002 + R0 * 1.9; },
    update(dt) {
      stream.visible = !!this.pouring;
      if (!this.pouring) return;
      const tip = tools.tip; const surf = ctx.BENCH_Y + water.position.y;
      const len = Math.max(0.01, tip.y - surf);
      stream.position.set(tip.x, surf + len / 2, tip.z); stream.scale.set(1 + Math.sin(performance.now() * 0.03) * 0.15, len, 1);
      this.at = this.at || new THREE.Vector3(); this.at.set(tip.x, surf, tip.z);
      this.level = Math.min(1, (this.level || 0) + dt * 0.45);
      water.visible = true; water.material.opacity = 0.05 + 0.08 * this.level;
      water.position.y = waxY + 0.002 + this.level * R0 * 1.9;
      ctx.progress(this.level);
      this.dropT = (this.dropT || 0) - dt;
      if (this.dropT <= 0) { this.dropT = 0.05; fx.burst(this.at, 0xbfe3f0, 3, 0.2, ctx.BENCH_Y + water.position.y); }
      if (this.level >= 1 && !this.done) { this.done = true; this.pouring = false; ctx.next('The organs now float slightly apart and stay moist and clear.'); }
    },
    handler: {
      down(p) {
        if (!ctx.requireTool('washbottle')) return true;
        stepFlood.pouring = true; tools.action(1); sfx.play('pour');
        return true;
      },
      up() { stepFlood.pouring = false; tools.action(0); },
    },
  };

  // ---- 8. examine with the hand lens -------------------------------------------------------------
  let dwell = 0; let dwellOn = null;
  const WANT = 5;
  function organUnder(worldP) {
    toWorm(worldP, local);
    const s = xSeg(local.x); const z = Math.abs(local.z);
    if (s >= 21.5 && s <= 26.5 && z > R0 * 0.3 && z < R0 * 0.8) return 'Intestinal caeca';
    if ([7, 9, 12, 13].some((h) => Math.abs(s - h) < 0.5) && z > R0 * 0.3 && z < R0 * 0.75) return 'Hearts';
    if (z > R0 * 0.55) return null;
    return organAt(s);
  }
  const stepLens = {
    title: 'Study the gut with a hand lens',
    text: `Hold the <b>hand lens</b> over the alimentary canal and let it rest on each region. Find at least ${WANT} structures.`,
    hint: 'Move the lens slowly along the gut from the head end: pharynx, oesophagus, the shiny gizzard, the stomach, the intestine, and the caeca in segment 26.',
    tool: 'lens', shot: SHOT_ANT,
    aim(p, out) { return input.planePoint(ctx.BENCH_Y + waxY + R0 * 1.2, out) || false; },
    enter() { ctx.progress(0); },
    update(dt) {
      if (!lens.active) { dwell = 0; return; }
      const o = organUnder(tools.tip);
      if (o && o === dwellOn) dwell += dt; else { dwellOn = o; dwell = 0; }
      if (o && dwell > 0.55 && !found.has(o)) {
        found.add(o); sfx.play('ok');
        ctx.say(FACTS[o], 'good', 5200);
        ui.observe(o, `segment ${SEGS[o]}`);
        ctx.progress(found.size / WANT);
        if (found.size >= WANT) anim.wait(2.2, () => ctx.next());
      }
    },
    handler: { down() { return ui.tool === 'lens'; } },
  };

  // ---- 9. label quiz ---------------------------------------------------------------------------
  const QUIZ = ['Pharynx', 'Oesophagus', 'Gizzard', 'Stomach', 'Intestine', 'Intestinal caeca', 'Hearts'];
  const stepQuiz = {
    title: 'Label the alimentary canal',
    text: 'Drag each name onto its numbered marker.',
    hint: 'Count segments from the head: pharynx 4, oesophagus 5–7, gizzard 8–9, stomach 9–14, intestine from 15, caeca in 26.',
    tool: null, hideBelt: true, shot: { pos: [-0.72, 1.5, 0.62], target: [-0.74, 0.9, 0.05], fit: 0.72 }, autoTool: 'hand',
    enter() {
      quiz = createLabelQuiz(ctx, QUIZ.map((name) => ({ name, at: worm.anchors[name].clone(), object: worm.root, fact: FACTS[name], where: `Look at segment ${SEGS[name]}.` })), {
        onPlace: (it, n, total) => ctx.progress(n / total),
        onDone: () => anim.wait(0.8, () => ctx.next('All labelled. Draw and label the dissection in your practical copy.')),
      });
    },
    update() { if (quiz) quiz.update(); },
    exit() { if (quiz) { quiz.dispose(); quiz = null; } },
  };

  const steps = [stepOrient, stepPinEnds, stepCut, stepSepta, stepPeel, stepPinFlaps, stepFlood, stepLens, stepQuiz];

  return {
    tools: ['hand', 'forceps', 'pin', 'scissors', 'scalpel', 'needle', 'washbottle', 'lens'],
    steps,
    update(dt) { lens.update(); if (water.visible) water.material.opacity = water.material.opacity; },
    result() {
      return {
        title: 'Earthworm dissected',
        rows: Object.keys(SEGS).map((k) => [k, `segment ${SEGS[k]}`]),
        conclusion: 'The alimentary canal of the earthworm is a straight tube from the mouth (segment 1) to the anus (last segment): buccal cavity (1–3), muscular pharynx (4), narrow oesophagus (5–7), grinding gizzard (8–9), glandular stomach (9–14) and the intestine (15 onward) with a pair of intestinal caeca in segment 26 and the typhlosole inside. It is adapted to a diet of soil and decaying leaves.',
        explore: () => { ui.selectTool('lens'); ctx.rig.go(SHOT_ANT, 1.2); input.setHandler({ hover(p) { const h = input.planePoint(ctx.BENCH_Y + waxY + R0 * 1.2, tmp); if (h) { tools.aim(h); tools.show(true); } }, down() { return true; }, move(p) { this.hover(p); } }); },
      };
    },
    dispose() { ctx.scene.remove(stream); stream.geometry.dispose(); stream.material.dispose(); lens.dispose(); pins.length = 0; if (quiz) quiz.dispose(); if (cut) cut.dispose(); },
  };
}
