// Runs a hands-on practical: the school lab room, the camera rig, the student's tools, and a
// procedure of steps. Each step frames its shot, names the tool it needs and takes the pointer;
// the teacher comments on slips, the score keeps count, and the result card closes the lab.
import { THREE, createEngine } from '../engine.js';
import { buildRoom, BENCH_Y } from '../lab3d-room.js';
import { createUI, TOOL_NAMES } from './ui.js';
import { createRig, createInput } from './input.js';
import { createToolRig } from './tools.js';
import { createFx } from './fx.js';
import { createAnimator, disposeTree } from './kit.js';
import { sfx } from './sound.js';

export function runPractical(stage, config, practical) {
  const engine = createEngine(stage, { fov: 40, shadows: true, environment: true, exposure: 1.05 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  camera.near = 0.02; camera.updateProjectionMatrix();
  buildRoom(scene, { subject: config.subject || 'biology', title: config.title, subtitle: config.aim }, quality);
  if (quality.tier !== 'low') { engine.renderer.shadowMap.enabled = true; engine.renderer.shadowMap.type = THREE.PCFSoftShadowMap; }

  const rig = createRig(camera);
  const input = createInput(engine.canvas, camera, rig);
  const tools = createToolRig(scene, camera);
  const fx = createFx(scene);
  const anim = createAnimator();
  const ui = createUI(stage, { title: config.title, aim: config.aim });
  const world = new THREE.Group(); world.position.y = BENCH_Y; scene.add(world);

  let score = 100; let mistakes = 0; let hints = 0; let elapsed = 0; let finished = false; let timeShown = -1;
  const mistakeLog = [];
  let steps = []; let idx = -1; let step = null; let stepDone = false; let idleT = 0;
  let impl = null;

  const ctx = {
    THREE, engine, scene, camera, quality, rig, input, tools, fx, anim, ui, sfx, world, config, BENCH_Y,
    stage, low: quality.tier === 'low',
    surfaces: [],
    get step() { return step; },
    get stepIndex() { return idx; },
    say(text, kind = 'info', ms) { ui.say(text, kind, ms); },
    mistake(text, penalty = 5) {
      mistakes += 1; score = Math.max(0, score - penalty); mistakeLog.push(text.replace(/<[^>]+>/g, ''));
      ui.setScore(score, mistakes); ui.say(text, 'mistake', 5200); sfx.play('bad');
      stage.classList.remove('bh-shake'); void stage.offsetWidth; stage.classList.add('bh-shake');
    },
    bonus(n) { score = Math.min(100, score + n); ui.setScore(score, mistakes); },
    /** True when the student holds the right tool; otherwise a gentle correction. */
    requireTool(id, why) {
      const ids = Array.isArray(id) ? id : [id];
      if (ids.includes(ui.tool)) return true;
      const name = TOOL_NAMES[ids[0]].toLowerCase();
      ctx.mistake(why || `Pick up the <b>${name}</b> for this step.`, 2);
      ids.forEach((t) => ui.glowTool(t, true));
      return false;
    },
    progress(p) { ui.progress(p); },
    /** Completes the current step. */
    next(msg, delay = 0.9) {
      if (stepDone) return; stepDone = true;
      if (msg) ui.say(msg, 'good', 3600);
      sfx.play('ok');
      anim.wait(delay, () => go(idx + 1));
    },
    goTo(i) { go(i); },
    /** Fast-forwards through steps (each enter, skip, exit) to step i; used by tests and replays. */
    skipTo(i) {
      for (let j = Math.max(0, idx); j < i; j++) {
        const s = steps[j];
        if (j !== idx && s.enter) s.enter(ctx);
        anim.update(10);
        if (s.skip) s.skip(ctx);
        if (s.exit) s.exit(ctx);
        step = null;
      }
      anim.update(10);
      idx = -1; ui.hideToast(); go(i);
    },
    aimDefault(ptr, out) {
      const h = ctx.surfaces.length ? input.pick(ctx.surfaces) : null;
      if (h) return out.copy(h.point);
      return input.planePoint(BENCH_Y, out) || out;
    },
    dispose: [],
  };

  function go(i) {
    if (step && step.exit) step.exit(ctx);
    fx.highlight(null);
    stepDone = false; idleT = 0;
    if (i >= steps.length) { finish(); return; }
    idx = i; step = steps[i];
    ui.setStep(i, steps.length, step);
    if (step.shot) rig.go(step.shot, step.shotTime ?? 1.4);
    if (step.tool) ui.glowTool(Array.isArray(step.tool) ? step.tool[0] : step.tool, false);
    if (step.enter) step.enter(ctx);
    if (step.autoTool) ui.selectTool(step.autoTool);
    ui.showBelt(!step.hideBelt);
    input.setHandler(wrapHandler(step));
  }

  const aimV = new THREE.Vector3();
  function aimTool(ptr) {
    if (!ptr.inside) { tools.show(false); return; }
    const ok = step && step.aim ? step.aim(ptr, aimV, ctx) : ctx.aimDefault(ptr, aimV);
    if (ok === false) { tools.show(false); return; }
    tools.aim(aimV); tools.show(true);
  }
  function wrapHandler(s) {
    const h = s.handler || {};
    return {
      down(p, button) { idleT = 0; aimTool(p); if (button === 2) return false; return h.down ? !!h.down(p, ctx) : false; },
      move(p) { aimTool(p); if (h.move) h.move(p, ctx); },
      up(p) { aimTool(p); if (h.up) h.up(p, ctx); },
      hover(p) { aimTool(p); if (h.hover) h.hover(p, ctx); },
      tap(p) { if (h.tap) h.tap(p, ctx); },
      cancel(p) { if (h.cancel) h.cancel(p, ctx); },
    };
  }

  function finish() {
    finished = true; ui.markAllDone(); input.setHandler(null); tools.show(false);
    sfx.play('done');
    const res = impl.result ? impl.result(ctx) : { rows: [], conclusion: '' };
    const stars = score >= 90 ? 3 : score >= 70 ? 2 : 1;
    const rows = [['Time', `${Math.floor(elapsed / 60)} min ${Math.round(elapsed % 60)} s`], ['Mistakes', String(mistakes)], ['Hints used', String(hints)]].concat(res.rows || []);
    ui.showResult({ title: res.title || 'Practical complete', score, stars, rows, conclusion: res.conclusion || '', onRedo: restart, onExplore: () => { if (res.explore) res.explore(ctx); } });
    if (impl.onFinish) impl.onFinish(ctx);
  }

  function build() {
    impl = practical.create(ctx);
    steps = impl.steps;
    ui.setTools(impl.tools || []);
    ui.setSteps(steps);
    ui.selectTool('hand');
  }
  function teardown() {
    if (step && step.exit) step.exit(ctx);
    if (impl && impl.dispose) impl.dispose(ctx);
    ctx.dispose.splice(0).forEach((f) => f());
    anim.clear(); fx.clearMarks(); fx.highlight(null);
    for (let i = world.children.length - 1; i >= 0; i--) { const c = world.children[i]; world.remove(c); disposeTree(c); }
    ctx.surfaces.length = 0; ui.clearObservations(); ui.clearResult();
  }
  function restart() {
    teardown();
    score = 100; mistakes = 0; hints = 0; elapsed = 0; finished = false; mistakeLog.length = 0; step = null; idx = -1;
    ui.setScore(score, mistakes);
    build(); go(0);
  }

  ui.onTool((id) => { tools.use(id); if (step && step.onTool) step.onTool(id, ctx); });
  ui.onHint(() => {
    if (!step || finished) return;
    hints += 1; score = Math.max(0, score - 1); ui.setScore(score, mistakes);
    ui.say(step.hint || step.text, 'hint', 6500);
    const t = Array.isArray(step.tool) ? step.tool[0] : step.tool;
    if (t) ui.glowTool(t, true);
    if (step.showHint) step.showHint(ctx);
  });
  ui.onRestart(restart);
  let lastW = 0; let lastH = 0;
  engine.onResize((w, h) => {
    if (lastW && step && step.shot && (Math.abs(w - lastW) > 40 || Math.abs(h - lastH) > 40)) rig.go(step.shot, 0.4);
    lastW = w; lastH = h;
  });

  engine.setUpdate((dt0, t) => {
    const dt = dt0 * (window.__bhTimeScale || 1);
    if (!finished) {
      elapsed += dt; idleT += dt;
      if (Math.floor(elapsed) !== timeShown) { timeShown = Math.floor(elapsed); ui.setTime(elapsed); }
      if (step && step.tool && idleT > 7) { const tt = Array.isArray(step.tool) ? step.tool[0] : step.tool; if (ui.tool !== tt) ui.glowTool(tt, true); }
    }
    anim.update(dt);
    rig.update(dt);
    if (step && step.update) step.update(dt, ctx, t);
    if (impl && impl.update) impl.update(dt, t, ctx);
    tools.update(dt);
    fx.update(dt, t);
  });

  stage.__bh = ctx;
  build();
  rig.go(steps[0].shot || { pos: [0, 3, 5], target: [0, 1, 0] }, 0);
  go(0);
  engine.start();

  return {
    ctx,
    dispose() {
      teardown(); input.dispose(); tools.dispose(); fx.dispose(); ui.dispose(); engine.dispose();
    },
  };
}
