// Transpiration from the upper and lower surfaces of a leaf, by the cobalt chloride paper method.
// Dry the papers over a spirit lamp until they are blue, lay one on each face of a dorsiventral
// leaf with forceps, clamp them between glass slides and start the stopwatch; tap each paper the
// moment it has turned fully pink. Then repeat on an isobilateral maize leaf. The papers take up
// water vapour at a rate set by the number of stomata under them, so the student's own times
// give the ratio of transpiration from the two faces.
import { THREE } from '../../engine.js';
import { petriDish, spiritLamp } from '../props.js';
import { clayPot, timelapse, ask, sheet, table, tag } from '../bench.js';
import { leaf, stem } from '../specimens/plants.js';
import { mesh, MAT, clamp, rng, ease } from '../kit.js';
import { createHud } from '../../handson/hud.js';
import { createStopwatch } from '../../handson/stopwatch.js';

const BLUE = new THREE.Color(0x2f5fd0); const PINK = new THREE.Color(0xf3a9c8); const DAMP = new THREE.Color(0xb994cf); const BURNT = new THREE.Color(0x7c5a3a);
const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const R = rng((Date.now() & 0xffff) || 7);
  const hud = createHud(ctx);
  const sw = createStopwatch(hud, { onStart() { if (clampedAt === null) { ctx.say('Clamp the papers first, then start timing.', 'hint', 2200); sw.reset(); return; } startedAt = simT; }, onStop() {} });
  let simT = 0; let startedAt = null; let clampedAt = null; let speed = 1;

  // the plants: a dorsiventral leaf (Ficus-like) and a maize leaf, each with one leaf held level
  function plant(x, kind) {
    const g = new THREE.Group(); g.position.set(x, 0, -0.45); world.add(g);
    g.add(clayPot(0.4, 0.55));
    const maize = kind === 'maize';
    g.add(stem([[0, 0.5, 0], [0.01, 1.0, 0], [0, 1.7, -0.02]], maize ? 0.035 : 0.03, maize ? 0x65a30d : 0x6b4f2a, 0.012));
    const extra = maize ? [[1.35, 2.2, -0.9], [1.0, -2.0, -0.7], [1.6, 0.6, -0.6]] : [[1.45, 2.4, -0.5], [1.15, -2.1, -0.35], [1.6, 3.6, -0.4], [0.95, -0.9, -0.6]];
    extra.forEach(([y, ry, rx]) => { const l = leaf(maize ? { len: 0.9, wid: 0.13, shape: 'linear', vein: 'parallel', upper: '#3f8f2f', lower: '#5aa543' } : { len: 0.62, wid: 0.36, upper: '#1f6b2a', lower: '#86b872' }); l.position.set(0, y, 0); l.rotation.set(rx, ry, 0, 'YXZ'); g.add(l); });
    const test = leaf(maize ? { len: 0.95, wid: 0.16, shape: 'linear', vein: 'parallel', upper: '#3f8f2f', lower: '#4f9d3b', arch: 0.02 } : { len: 0.8, wid: 0.46, upper: '#1f6b2a', lower: '#8fc27c', arch: 0.03 });
    test.position.set(0, 1.12, 0.02); g.add(test);
    return { g, test, maize };
  }
  const ficus = plant(-0.35, 'ficus');
  const maize = plant(-2.1, 'maize'); maize.g.visible = false;
  const dish = petriDish(0xf8fafc); dish.position.set(1.15, 0, 0.45); world.add(dish);
  const lamp = spiritLamp(); lamp.position.set(1.15, 0, -0.45); world.add(lamp);
  const lampTag = tag('spirit lamp', { h: 0.07 }); lampTag.position.set(1.15, 0.62, -0.45); world.add(lampTag);
  const papers = [];
  for (let i = 0; i < 4; i++) {
    const m = new THREE.MeshStandardMaterial({ color: DAMP.clone(), roughness: 0.95 });
    const p = mesh(new THREE.BoxGeometry(0.15, 0.004, 0.15), m, [1.15 + (i % 2 ? 0.1 : -0.1), 0.02 + i * 0.001, 0.45 + (i < 2 ? -0.1 : 0.1)]);
    p.rotation.y = (i - 1.5) * 0.2; world.add(p); papers.push({ m: p, dry: 0, water: 0, scorched: 0, placed: null });
  }
  const slidesHome = new THREE.Vector3(-1.45, 0, 0.55);
  function sandwich() {
    const g = new THREE.Group();
    const glassSlide = () => { const geo = new THREE.BoxGeometry(0.26, 0.012, 0.76); const m = mesh(geo, MAT.glass(), [0, 0.006, 0], { cast: false }); m.renderOrder = 6; const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({ color: 0x9fd8d0, transparent: true, opacity: 0.8 })); e.userData.noPick = true; m.add(e); const w = new THREE.Group(); w.add(m); return w; };
    const a = glassSlide(); const b = glassSlide(); b.position.y = -0.034;
    const clip = new THREE.Group(); clip.position.set(0, -0.012, 0.36);
    clip.add(mesh(new THREE.BoxGeometry(0.14, 0.07, 0.04), MAT.gloss(0x111827)));
    [-1, 1].forEach((s) => clip.add(mesh(new THREE.TorusGeometry(0.035, 0.006, 6, 12, Math.PI), MAT.steel(), [s * 0.05, 0.05, 0.03]).rotateX(-0.6)));
    g.add(a, b, clip); return g;
  }
  const sandwiches = [sandwich(), sandwich()];
  sandwiches.forEach((s, i) => { s.position.copy(slidesHome).add(new THREE.Vector3(i * 0.32, 0.02, 0)); world.add(s); });

  const tmp = new THREE.Vector3();
  let current = ficus; let held = null; let lampLit = false; let holdDish = false; let holdT = 0;
  const times = { ficus: {}, maize: {} };
  const truth = { ficus: {}, maize: {} };
  // time (s) for a paper to turn fully pink: the inverse of the stomatal water-vapour flux under it
  const T95 = {
    ficus: { lower: 50 + R() * 12, upper: 0 },
    maize: { lower: 95 + R() * 15, upper: 0 },
  };
  T95.ficus.upper = T95.ficus.lower * (4.2 + R() * 1.2);
  T95.maize.upper = T95.maize.lower * (1.05 + R() * 0.15);

  const DESK = S([0.4, 2.5, 3.1], [0.0, 0.75, -0.1], 3.6);
  const LEAF = (pl) => S([pl.g.position.x + 0.45, 1.75, 1.2], [pl.g.position.x, 1.1, 0.3], 1.0);
  const UNDER = (pl) => S([pl.g.position.x + 0.45, 0.62, 1.25], [pl.g.position.x, 1.08, 0.3], 1.0);
  const LAMP = S([1.7, 1.9, 1.9], [1.1, 0.35, 0.05], 1.9);

  function paperColor(p) {
    const c = p.m.material.color;
    if (p.scorched > 0) { c.copy(BLUE).lerp(BURNT, clamp(p.scorched)); return; }
    if (p.placed) c.copy(BLUE).lerp(PINK, clamp(p.water));
    else c.copy(DAMP).lerp(BLUE, clamp(p.dry));
  }
  function leafPoint(pl, face, out) { const z = pl.maize ? 0.5 : 0.42; const y = pl.test.userData.surfaceY(z); out.set(0, face === 'upper' ? y + 0.005 : y - 0.007, z); pl.test.localToWorld(out); return out; }

  // ---- steps ------------------------------------------------------------------------------------
  const stepLight = {
    title: 'Light the spirit lamp', text: 'Cobalt chloride paper is <b>blue when dry</b> and turns <b>pink</b> when it takes up water. These papers have picked up moisture from the air. Tap the spirit lamp to light it.',
    tool: null, autoTool: 'hand', shot: LAMP,
    skip() { lamp.userData.flame.visible = true; lampLit = true; },
    handler: { down() { if (!input.pick([lamp])) return false; lamp.userData.flame.visible = true; lampLit = true; sfx.play('click'); ctx.next('Lit. A small steady flame.'); return true; } },
  };
  const stepDry = {
    title: 'Dry the papers until blue', text: 'Press and <b>hold</b> on the petri dish of papers to warm them high over the flame. Let go once they are evenly blue — do not scorch them.',
    hint: 'Hold the dish over the flame; watch the colour, release when all four are blue.', tool: null, autoTool: 'hand', shot: LAMP,
    skip() { papers.forEach((p) => { p.dry = 1; p.scorched = 0; paperColor(p); }); },
    handler: {
      down() { if (!input.pick([dish, ...papers.map((p) => p.m)])) return false; holdDish = true; holdT = 0; sfx.play('pick'); return true; },
      up() { if (!holdDish) return; holdDish = false; const minDry = Math.min(...papers.map((p) => p.dry)); const burnt = papers.some((p) => p.scorched > 0.3);
        if (burnt) { ctx.mistake('Scorched — brown paper no longer shows the colour change cleanly. Fresh papers are given; warm them just until blue.', 4); papers.forEach((p) => { p.dry = 0; p.scorched = 0; paperColor(p); }); }
        else if (minDry > 0.95) ctx.next('Evenly blue: the papers are dry. Keep them in the closed dish (a desiccator) until used.');
        else ctx.say(`Not yet: still ${minDry > 0.5 ? 'violet' : 'pinkish'} in places. Hold a little longer.`, 'hint', 2200); },
    },
    update(dt) {
      const lift = holdDish ? 1 : 0; dish.position.lerp(tmp.set(1.15, lift ? 0.95 : 0, lift ? -0.4 : 0.45), 1 - Math.pow(0.002, dt));
      papers.forEach((p, i) => { if (p.placed) return; p.m.position.set(dish.position.x + (i % 2 ? 0.1 : -0.1), dish.position.y + 0.02 + i * 0.001, dish.position.z + (i < 2 ? -0.1 : 0.1)); });
      if (!holdDish || dish.position.y < 0.6) return;
      holdT += dt; papers.forEach((p) => { p.dry = clamp(p.dry + dt / (2.2 + (p.m.id % 3) * 0.3)); if (p.dry >= 1) p.scorched = clamp(p.scorched + (holdT > 5.5 ? dt / 2 : 0)); paperColor(p); });
      ctx.progress(Math.min(...papers.map((p) => p.dry)));
    },
    exit() { holdDish = false; dish.position.set(1.15, 0, 0.45); papers.forEach((p, i) => { if (!p.placed) p.m.position.set(1.15 + (i % 2 ? 0.1 : -0.1), 0.02 + i * 0.001, 0.45 + (i < 2 ? -0.1 : 0.1)); }); },
  };
  function placeStep(pl, face, idx) {
    return {
      title: `Paper on the ${face} surface${pl.maize ? ' (maize)' : ''}`,
      text: `With the <b>forceps</b>, pick up a blue paper from the dish, then tap the ${face === 'upper' ? 'top' : 'underside'} of the level leaf${face === 'lower' ? ' (the camera is below it)' : ''}.`,
      hint: 'Forceps only: moisture from fingers turns the paper pink before it touches the leaf.', tool: 'forceps',
      get shot() { return held ? (face === 'upper' ? LEAF(pl) : UNDER(pl)) : DESK; },
      skip() { put(papers[idx], pl, face); },
      handler: {
        down() {
          if (!held) {
            const h = input.pick(papers.filter((p) => !p.placed).map((p) => p.m)); if (!h) return false;
            if (!ctx.requireTool('forceps', 'Lift cobalt chloride paper with <b>forceps</b>: moist fingers turn it pink.')) return true;
            held = papers.find((p) => p.m === h.object); tools.action(1); sfx.play('pick'); ctx.rig.go(face === 'upper' ? LEAF(pl) : UNDER(pl), 1.1); return true;
          }
          const h = input.pick([pl.test], true); if (!h) return false;
          const on = h.object === pl.test.userData.upper ? 'upper' : 'lower';
          if (on !== face) { ctx.say(`That is the ${on} surface — tap the ${face} one.`, 'hint', 2200); return true; }
          put(held, pl, face); held = null; tools.action(0); sfx.play('place');
          ctx.next(`Paper flat against the ${face} epidermis.`); return true;
        },
      },
    };
  }
  function put(p, pl, face) {
    p.placed = { pl, face }; p.water = 0; p.dry = 1; paperColor(p);
    leafPoint(pl, face, tmp); world.worldToLocal(tmp); p.m.position.copy(tmp); p.m.rotation.set(0, 0, 0);
  }
  function clampStep(pl) {
    return {
      title: 'Clamp and start the stopwatch', text: 'Tap the <b>glass slides</b> to clamp both papers against the leaf (this keeps out room air), then <b>start the stopwatch</b> at once.',
      tool: null, autoTool: 'hand', shot: S([pl.g.position.x + 0.9, 1.6, 1.7], [pl.g.position.x + 0.1, 0.9, 0.15], 2.0),
      enter() { sw.show(true); sw.reset(); startedAt = null; clampedAt = null; },
      skip() { doClamp(pl, true); startedAt = clampedAt; sw.reset(); sw.press(); },
      handler: {
        down() {
          if (clampedAt !== null) return false;
          if (!input.pick(sandwiches)) return false;
          doClamp(pl, false); return true;
        },
      },
      update() {
        if (clampedAt !== null && startedAt !== null && !this.done) {
          this.done = true; const late = startedAt - clampedAt;
          if (late > 6) ctx.mistake(`The stopwatch started ${late.toFixed(0)} s after clamping — every reading will be short by that much. Start it the moment the slides close.`, 3);
          ctx.next();
        }
      },
    };
  }
  function doClamp(pl, instant) {
    const s = sandwiches[pl.maize ? 1 : 0]; leafPoint(pl, 'upper', tmp); world.worldToLocal(tmp); tmp.y -= 0.0; const to = tmp.clone();
    const from = s.position.clone();
    if (instant) { s.position.copy(to); s.position.y += 0.004; } else anim.add(0.7, (k) => { s.position.lerpVectors(from, to, k); s.position.y += Math.sin(Math.PI * k) * 0.4 + 0.004 * k; }, { ease: ease.inOut, done: () => sfx.play('latch') });
    clampedAt = simT; sfx.play('glass');
  }
  function timeStep(pl) {
    const key = pl.maize ? 'maize' : 'ficus'; const done = {};
    return {
      title: 'Time the colour change', text: 'Watch both papers. <b>Tap a paper</b> the moment it has turned completely pink — the stopwatch time is recorded for that surface. (Use the speed button if you wish.)',
      tool: null, autoTool: 'hand', hideBelt: true, get shot() { return UNDER(current); },
      enter() {
        hud.actions([
          { id: 'up', label: 'Look from above', onClick() { ctx.rig.go(LEAF(current), 0.8); } },
          { id: 'lo', label: 'Look from below', onClick() { ctx.rig.go(UNDER(current), 0.8); } },
          { id: 'sp', label: 'Speed ×1', onClick() { speed = speed === 1 ? 5 : 1; hud.relabel('sp', `Speed ×${speed}`); } }]);
      },
      exit() { hud.actions([]); speed = 1; },
      skip() { ['lower', 'upper'].forEach((f) => { times[key][f] = T95[key][f] * (1.02 + R() * 0.04); truth[key][f] = T95[key][f]; }); papers.filter((p) => p.placed && p.placed.pl === pl).forEach((p) => { p.water = 1; paperColor(p); }); },
      handler: {
        down() {
          const p = papers.find((q) => q.placed && q.placed.pl === pl && input.pick([q.m]));
          const h = p || (input.pick([pl.test], true) ? papers.find((q) => q.placed && q.placed.pl === pl && q.placed.face === (input.pick([pl.test], true).object === pl.test.userData.upper ? 'upper' : 'lower')) : null);
          if (!h) return false; const f = h.placed.face; if (done[f]) return true;
          if (!sw.running) { ctx.say('Your stopwatch is not running.', 'hint', 2000); return true; }
          if (h.water < 0.8) { ctx.mistake(`The ${f} paper is still ${h.water < 0.4 ? 'blue' : 'violet'} in parts. Wait until it is completely pink.`, 2); return true; }
          done[f] = true; times[key][f] = sw.time; truth[key][f] = T95[key][f]; sfx.play('ok');
          ui.observe(`${pl.maize ? 'Maize' : 'Ficus'} ${f}`, `${sw.time.toFixed(1)} s`);
          if (sw.time > T95[key][f] * 1.35) ctx.say('A little late — the paper had been pink for a while. Your time overestimates.', 'hint', 3000);
          if (done.lower && done.upper) { sw.show(false); ctx.next(`Lower ${times[key].lower.toFixed(0)} s, upper ${times[key].upper.toFixed(0)} s.`); }
          return true;
        },
      },
    };
  }
  const stepMaize = {
    title: 'Now an isobilateral leaf', text: 'Repeat with a <b>maize</b> leaf, whose two faces have about the same number of stomata. Tap the maize plant to bring it to the bench.',
    tool: null, autoTool: 'hand', shot: DESK,
    enter() { maize.g.visible = true; },
    skip() { swap(true); },
    handler: { down() { if (!input.pick([maize.g])) return false; swap(false); return true; } },
  };
  function swap(instant) {
    current = maize;
    papers.filter((p) => p.placed && p.placed.pl === ficus).forEach((p) => { p.m.visible = false; });
    sandwiches[0].visible = false;
    const a = ficus.g.position.clone(); const b = maize.g.position.clone();
    const go = (k) => { ficus.g.position.lerpVectors(a, new THREE.Vector3(-2.1, 0, -0.6), k); maize.g.position.lerpVectors(b, new THREE.Vector3(-0.35, 0, -0.45), k); };
    if (instant) go(1); else anim.add(1.0, go, { done: () => ctx.next('Maize plant on the bench; its leaf is held level.') });
  }
  const stepCompare = {
    title: 'Compare the two surfaces', text: 'Relative rate of transpiration = 1 / time to turn pink. Use your times.', tool: null, autoTool: 'hand', hideBelt: true, shot: DESK,
    enter() {
      const f = times.ficus; const m = times.maize; const r = f.upper / f.lower; const rm = m.upper / m.lower;
      sh = sheet(ctx, { title: 'Observation table' });
      sh.set(table(['Leaf', 'Surface', 'Time (s)', 'Rate (1/t ×1000)'], [['Ficus', 'upper', f.upper.toFixed(1), (1000 / f.upper).toFixed(2)], ['', 'lower', f.lower.toFixed(1), (1000 / f.lower).toFixed(2)], ['Maize', 'upper', m.upper.toFixed(1), (1000 / m.upper).toFixed(2)], ['', 'lower', m.lower.toFixed(1), (1000 / m.lower).toFixed(2)]]));
      const right = Math.round(r * 10) / 10;
      const opts = [right, Math.round(10 / r) / 10, Math.round((r + 1.5) * 10) / 10, 1.0].filter((v, i, a) => a.indexOf(v) === i).sort(() => R() - 0.5);
      ask(ctx, 'Ficus: rate from lower ÷ rate from upper =', opts.map((v) => ({ label: `${v.toFixed(1)}`, value: v })), right, {
        wrong: 'Rate is 1/t, so (1/t lower) ÷ (1/t upper) = t upper ÷ t lower.',
        then() { ui.observe('Ficus lower:upper', `${right.toFixed(1)} : 1`); ui.observe('Maize lower:upper', `${(Math.round(rm * 10) / 10).toFixed(1)} : 1`); ask(ctx, 'Why does the Ficus leaf lose more water from its lower surface?', [{ label: 'It has many more stomata on the lower epidermis', value: 'st' }, { label: 'The lower surface is warmer', value: 'w' }, { label: 'The cuticle is thicker below', value: 'c' }], 'st', { ok: 'Dorsiventral leaves carry most stomata on the shaded lower epidermis (and a thicker cuticle above), so most transpiration is stomatal, from below. Maize, isobilateral, has stomata on both faces: about equal rates.', wrong: 'Most water vapour escapes through stomata. Where are they?', delay: 0.3 }); },
      });
    },
    exit() { ui.clearChooser(); },
  };
  let sh = null;

  const steps = [stepLight, stepDry, placeStep(ficus, 'upper', 0), placeStep(ficus, 'lower', 1), clampStep(ficus), timeStep(ficus), stepMaize, placeStep(maize, 'upper', 2), placeStep(maize, 'lower', 3), clampStep(maize), timeStep(maize), stepCompare];
  ctx.debug = { papers, T95, times, sw };
  void timelapse; void fx;

  return {
    tools: ['hand', 'forceps'],
    steps,
    update(dt) {
      const d = dt * speed; simT += d;
      sw.update(d); hud.update();
      if (clampedAt !== null) papers.forEach((p) => {
        if (!p.placed || p.placed.pl !== current) return;
        const key = current.maize ? 'maize' : 'ficus'; const t95 = T95[key][p.placed.face];
        p.water = clamp(p.water + d * 3 / t95 * (1 - p.water));
        paperColor(p);
      });
      if (held) { held.m.position.copy(tools.tip); world.worldToLocal(held.m.position); held.m.position.y -= 0.01; }
    },
    result() {
      const f = times.ficus; const m = times.maize; const rr = f.upper / f.lower; const tr = T95.ficus.upper / T95.ficus.lower;
      return {
        title: 'Transpiration from leaf surfaces',
        rows: [['Ficus upper / lower', `${(f.upper || 0).toFixed(0)} s / ${(f.lower || 0).toFixed(0)} s`], ['Maize upper / lower', `${(m.upper || 0).toFixed(0)} s / ${(m.lower || 0).toFixed(0)} s`], ['Ficus lower:upper rate', `${rr.toFixed(1)} : 1 (true ${tr.toFixed(1)} : 1, error ${Math.abs(rr - tr) / tr * 100 < 0.5 ? '<1' : (Math.abs(rr - tr) / tr * 100).toFixed(0)} %)`]],
        conclusion: 'Cobalt chloride paper on the lower surface of the dorsiventral leaf turned pink several times faster than on the upper surface: the lower epidermis has far more stomata, so it transpires more. On the isobilateral maize leaf both faces took about the same time, because stomata are about equally distributed.',
      };
    },
    dispose() { hud.dispose(); sw.dispose(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}
