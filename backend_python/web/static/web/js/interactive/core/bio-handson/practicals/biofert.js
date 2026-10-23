// Preparing a Rhizobium biofertilizer. Uproot a pea plant, wash the roots, pick firm pink root
// nodules (the pink is leghaemoglobin of active nitrogen fixation), surface-sterilise them in
// 0.1% HgCl2 and rinse them five times, crush one in sterile water, streak the milky suspension on
// yeast-extract mannitol agar with Congo red using a flamed loop, and incubate: Rhizobium grows as
// gummy white colonies that do not take up the red dye. A colony is grown up in broth, mixed with
// a neutralised lignite carrier to about 40% moisture, and used to coat seeds with jaggery as the
// sticker, dried in the shade.
import { THREE } from '../../engine.js';
import { spiritLamp, watchGlass, reagentBottle } from '../props.js';
import { plate, incubator } from '../specimens/microbe.js';
import { leaf, stem } from '../specimens/plants.js';
import { clayPot, glassBeaker, timelapse, ask, tag, enamelTray, soilTexture } from '../bench.js';
import { mesh, MAT, wet, rng, clamp, ease } from '../kit.js';
import { createLens } from '../lens.js';
import { conicalFlask } from '../../handson/glass.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const PINK = 0xe7889a; const WHITE = 0xf1ece0; const BROWN = 0x6b5a3a;

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const R = rng((Date.now() & 0xffff) || 23);
  const hud = createHud(ctx); const chip = hud.chip('ho-chip-read');
  const lens = createLens(ctx, { mag: 3, groundY: ctx.BENCH_Y + 0.05 });
  // the pea plant in its pot, with nodulated roots below the soil
  const pot = clayPot(0.42, 0.55); pot.position.set(-1.9, 0, -0.5); world.add(pot);
  const plant = new THREE.Group(); plant.position.set(-1.9, 0.5, -0.5); world.add(plant);
  plant.add(stem([[0, 0, 0], [0.02, 0.5, 0], [-0.03, 1.1, 0.02], [0.02, 1.5, 0]], 0.022, 0x6a9a3a, 0.01));
  for (let i = 0; i < 6; i++) { const l = leaf({ len: 0.24, wid: 0.16, upper: '#4f8f3a', lower: '#8cc070' }); l.position.set(0, 0.35 + i * 0.2, 0); l.rotation.set(-0.3, i * 2.3, 0, 'YXZ'); plant.add(l); }
  const roots = new THREE.Group(); plant.add(roots);
  const rootMat = new THREE.MeshStandardMaterial({ color: 0x6b4a2e, roughness: 0.9 });
  roots.add(mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0.02, -0.25, 0), new THREE.Vector3(-0.02, -0.55, 0.02)]), 16, 0.018, 6), rootMat));
  const nodules = [];
  for (let k = 0; k < 9; k++) {
    const a = k * 2.4; const y = -0.08 - (k % 5) * 0.08; const L = 0.18 + R() * 0.1;
    const end = new THREE.Vector3(Math.cos(a) * L, y - 0.12, Math.sin(a) * L);
    roots.add(mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(0, y, 0), new THREE.Vector3(Math.cos(a) * L * 0.5, y - 0.03, Math.sin(a) * L * 0.5), end]), 10, 0.008, 5), rootMat));
    for (let j = 0; j < 2; j++) {
      const kind = k < 5 ? 'pink' : k < 7 ? 'white' : 'brown';
      const p = new THREE.Vector3(0, y, 0).lerp(end, 0.45 + j * 0.35);
      const n = mesh(new THREE.SphereGeometry(0.022 + R() * 0.01, 10, 8), wet(0x6b4a2e, { roughness: 0.6 }), [p.x, p.y, p.z]); n.scale.set(1, 0.85, 1.2); roots.add(n);
      n.userData.kind = kind; nodules.push(n);
    }
  }
  roots.visible = false;
  const water = glassBeaker(0.35, 0.5, 0xbfe3f2, 0.7); water.group.position.set(-1.2, 0, 0.6); world.add(water.group);
  const wt = tag('water', { h: 0.06 }); wt.position.set(-1.2, 0.65, 0.6); world.add(wt);
  const hg = watchGlass(0xe2e8f0, 0.6); hg.position.set(-0.5, 0, 0.8); world.add(hg); const hgT = tag('0.1% HgCl₂', { h: 0.06 }); hgT.position.set(-0.5, 0.22, 0.8); world.add(hgT);
  const rinse = glassBeaker(0.18, 0.3, 0xe0f2fe, 0.6); rinse.group.position.set(0.05, 0, 0.8); world.add(rinse.group); const rT = tag('sterile water', { h: 0.06 }); rT.position.set(0.05, 0.42, 0.8); world.add(rT);
  const crush = watchGlass(0xf8fafc, 0.4); crush.position.set(0.6, 0, 0.8); world.add(crush);
  const lamp = spiritLamp(); lamp.position.set(0.45, 0, -0.55); world.add(lamp);
  const pl = plate('#f2c4c4'); pl.group.position.set(1.35, 0, 0.0); world.add(pl.group); pl.pour();
  const plT = tag('YEMA + Congo red', { h: 0.06 }); plT.position.set(1.35, 0.25, 0.42); world.add(plT);
  const inc = incubator('28 °C'); inc.group.position.set(2.7, 0, -0.6); inc.group.rotation.y = -0.5; world.add(inc.group);
  const tray = enamelTray(0.9, 0.6); tray.position.set(-0.95, 0, -0.75); world.add(tray);
  const lignite = mesh(new THREE.SphereGeometry(0.3, 24, 14), new THREE.MeshStandardMaterial({ map: soilTexture('#2b2522'), roughness: 1 }), [-0.95, 0.02, -0.75]); lignite.scale.y = 0.25; lignite.visible = false; world.add(lignite);
  const broth = conicalFlask({ color: 0xfefce8, opacity: 0.45 }); broth.setVolume(200); broth.group.position.set(-0.2, 0, -0.5); broth.group.visible = false; world.add(broth.group);
  const bowl = glassBeaker(0.3, 0.2, 0xffffff, 0); bowl.group.position.set(1.0, 0, 0.85); bowl.group.visible = false; world.add(bowl.group);
  const seeds = new THREE.Group(); for (let i = 0; i < 26; i++) seeds.add(mesh(new THREE.SphereGeometry(0.035, 10, 8), wet(0xd8c66a, { roughness: 0.5 }), [(R() - 0.5) * 0.36, 0.05 + (i % 3) * 0.03, (R() - 0.5) * 0.36])); bowl.group.add(seeds);
  const jag = reagentBottle('Jaggery 10%', 0x92400e, 'sticker'); jag.position.set(1.6, 0, 0.7); jag.visible = false; world.add(jag);
  const tmp = new THREE.Vector3();
  const S_ALL = S([0.2, 2.4, 3.4], [0.0, 0.5, 0.1], 4.8);
  const S_POT = S([-1.3, 2.0, 1.7], [-1.7, 0.9, 0.0], 2.4);
  const S_ROOTS = S([-1.45, 1.55, 0.7], [-1.9, 0.95, -0.45], 0.9);
  const S_BENCH = S([0.05, 1.6, 2.4], [0.05, 0.2, 0.7], 2.3);
  const S_PLATE = S([1.35, 1.25, 0.22], [1.35, 0.02, 0.0], 0.95, 0.95);
  const picked = []; let rinses = 0; let crushed = 0; let loopHot = false; let loopLoaded = false; let moisture = 0; let added = 0;

  const stepUproot = {
    title: 'Uproot a legume', text: 'Gently pull the pea plant up out of its pot: drag it upward.', tool: null, autoTool: 'hand', shot: S_POT,
    skip() { roots.visible = true; plant.position.set(-1.9, 1.35, -0.5); },
    handler: {
      down(p) { if (!input.pick([plant, pot], true)) return false; this.y = p.y; roots.visible = true; return true; },
      move(p) { if (this.y === undefined) return; const k = clamp((this.y - p.y) / 160); plant.position.y = 0.5 + k * 0.85; if (k >= 1 && !this.done) { this.done = true; this.y = undefined; sfx.play('tear'); fx.burst(tmp.set(-1.9, 1.35, -0.5), 0x5b3a22, 10, 0.2, ctx.BENCH_Y + 0.55); ctx.next('Out, with its root system. Lumps of soil cling to the roots.'); } },
      up() { if (!this.done) { plant.position.y = 0.5; roots.visible = false; } this.y = undefined; },
    },
  };
  const stepWash = {
    title: 'Wash the roots', text: 'Tap the beaker of water to swish the roots clean so the nodules can be seen.', tool: null, autoTool: 'hand', shot: S_POT,
    skip() { reveal(); },
    handler: { down() { if (!input.pick([water.group, plant], true)) return false; sfx.play('pour'); const from = plant.position.clone(); anim.add(1.4, (k) => { plant.position.set(from.x + (-1.2 - from.x) * Math.sin(Math.PI * k), from.y + Math.sin(Math.PI * k) * 0.3, from.z + (0.6 - from.z) * Math.sin(Math.PI * k)); }, { done: () => { reveal(); ctx.next('Clean roots: small round nodules dot the lateral roots.'); } }); return true; } },
  };
  function reveal() { rootMat.color.setHex(0xe8dcc0); nodules.forEach((n) => n.material.color.setHex(n.userData.kind === 'pink' ? PINK : n.userData.kind === 'white' ? WHITE : BROWN)); }
  const stepPick = {
    title: 'Pick healthy nodules', text: 'Look with the <b>hand lens</b>, then with the <b>forceps</b> pick three firm, <b>pink</b> nodules.', tool: 'forceps', shot: S_ROOTS,
    skip() { nodules.filter((n) => n.userData.kind === 'pink').slice(0, 3).forEach((n) => { n.visible = false; picked.push(n); }); },
    handler: { down() {
      if (ui.tool === 'lens') return false;
      const h = input.pick(nodules.filter((n) => n.visible)); if (!h) return false; if (!ctx.requireTool('forceps')) return true;
      const n = h.object; const k = n.userData.kind;
      if (k !== 'pink') { ctx.mistake(k === 'white' ? 'A white nodule is young and not yet fixing nitrogen: no leghaemoglobin.' : 'A brown or greenish nodule is old and spent.', 2); return true; }
      n.visible = false; picked.push(n); sfx.play('pick'); ctx.progress(picked.length / 3);
      if (picked.length === 3) ctx.next('Pink inside: leghaemoglobin, a sign of active nitrogen fixation by bacteroids.'); return true;
    } },
  };
  const stepSter = {
    title: 'Surface-sterilise the nodules', text: 'Tap the <b>0.1% HgCl₂</b> to soak the nodules for a few minutes, then tap the <b>sterile water</b> to rinse them — five rinses.', tool: null, autoTool: 'hand', shot: S_BENCH,
    skip() { this.soaked = true; rinses = 5; },
    handler: { down() {
      if (input.pick([hg], true)) { this.soaked = true; sfx.play('drop'); ctx.say('Soaking: the surface microbes from the soil are killed.', 'info', 1800); return true; }
      if (!input.pick([rinse.group], true)) return false;
      if (!this.soaked) { ctx.mistake('Sterilise first — soil bacteria on the nodule surface would overgrow the plate.', 2); return true; }
      rinses += 1; sfx.play('pour'); ctx.progress(rinses / 5); ui.setText(`Rinses: <b>${rinses}</b> of 5.`);
      if (rinses >= 5) ctx.next('Rinsed free of mercuric chloride, which would otherwise kill the Rhizobium inside.'); return true;
    } },
  };
  const stepCrush = {
    title: 'Crush a nodule', text: 'With the <b>forceps</b>, crush a nodule in a drop of sterile water in the watch glass: drag back and forth on it.', tool: 'forceps', shot: S_BENCH,
    skip() { crushed = 1; },
    handler: {
      down(p) { if (!input.pick([crush], true)) return false; if (!ctx.requireTool('forceps')) return true; this.last = [p.x, p.y]; tools.press(1); return true; },
      move(p) { if (!this.last) return; crushed = clamp(crushed + Math.hypot(p.x - this.last[0], p.y - this.last[1]) / 700); this.last = [p.x, p.y]; ctx.progress(crushed); if (crushed >= 1 && !this.done) { this.done = true; tools.press(0); this.last = null; ctx.next('A milky suspension of bacteroids.'); } },
      up() { this.last = null; tools.press(0); },
    },
  };
  let sectors = new Set(); let coolAt = 0;
  const stepStreak = {
    title: 'Streak a YEMA plate', text: 'Pick up the <b>loop</b>, heat it red-hot in the flame, let it cool, dip it in the suspension, then streak the plate in zig-zags across three sectors (lift and turn between sectors).', tool: 'loop', shot: S([0.9, 1.8, 2.2], [0.9, 0.15, 0.3], 2.4),
    skip() { for (let s2 = 0; s2 < 3; s2++) { pl.newStreak(); for (let i = 0; i < 8; i++) { const a = s2 * 2.1 + (i % 2) * 0.5; const r = 0.08 + i * 0.04; pl.streakTo(0.5 + Math.cos(a) * r, 0.5 + Math.sin(a) * r); } } sectors = new Set([0, 1, 2]); },
    enter() { sectors = new Set(); loopHot = false; loopLoaded = false; },
    handler: {
      down(p) {
        if (!ctx.requireTool('loop')) return !!input.pick([lamp, crush, pl.group], true);
        if (input.pick([lamp], true)) { loopHot = true; sfx.play('switch'); ctx.say('Red-hot: sterile. Let it cool for a moment.', 'info', 1600); coolAt = performance.now(); return true; }
        if (input.pick([crush], true)) { if (!loopHot) { ctx.mistake('Flame the loop first — an unsterile loop carries other bacteria.', 2); return true; } if (performance.now() - coolAt < 900) { ctx.mistake('Still hot! It would kill the bacteria. Wait a second.', 1); return true; } loopLoaded = true; sfx.play('drop'); return true; }
        const h = input.pick([pl.agar], false, false); if (!h) return false;
        if (!loopLoaded) { ctx.say('Dip the cooled loop in the suspension first.', 'hint', 1600); return true; }
        pl.newStreak(); this.drawing = true; return true;
      },
      move() { if (!this.drawing) return; const h = input.pick([pl.agar], false, false); if (!h) return; const u = h.uv.x; const v = 1 - h.uv.y; pl.streakTo(u, v); const sec = Math.floor(((Math.atan2(v - 0.5, u - 0.5) + Math.PI) / (Math.PI * 2)) * 3) % 3; sectors.add(sec); ctx.progress(sectors.size / 3); },
      up() { if (!this.drawing) return; this.drawing = false; tools.press(0); if (sectors.size >= 3 && !this.done) { this.done = true; ctx.next('Streaked: the bacteria are thinned out across the plate so single colonies will form.'); } },
    },
  };
  let clock = null;
  const stepInc = {
    title: 'Incubate at 28 °C', text: 'The plate is in the incubator. Run the clock a day at a time for five days.', tool: null, autoTool: 'hand', hideBelt: true, shot: S_PLATE,
    enter() {
      const pts = pl.streaks.flat(); const n = Math.min(40, pts.length);
      const list = []; for (let i = 0; i < n; i++) { const [u, v] = pts[Math.floor(R() * pts.length)]; const contam = R() < 0.1; list.push({ kind: contam ? 'contam' : 'rhizo', u: u + (R() - 0.5) * 0.01, v: v + (R() - 0.5) * 0.01, rmax: contam ? 1.0 : 1.4 + R() * 0.9, t0: contam ? 20 : 40, tau: 60 }); }
      pl.seed(list);
      clock = timelapse(ctx, { step: 1, unit: 'day', onTick: (d, done) => { pl.setTime(d * 24); if (done && d >= 5 && !this.done) { this.done = true; clock.show(false); ctx.next('Day 5: raised, gummy, translucent white colonies along the streaks — Rhizobium. The few red ones took up Congo red: contaminants.'); } } });
    },
    skip() { pl.setTime(120); },
    exit() { if (clock) clock.remove(); clock = null; },
  };
  const stepBroth = {
    title: 'Grow it in broth', text: 'With the flamed <b>loop</b>, touch a white colony and transfer it to the flask of YEM broth (tap the colony, then the flask).', tool: 'loop', shot: S([0.5, 1.9, 2.6], [0.55, 0.35, -0.1], 3.0),
    enter() { broth.group.visible = true; },
    skip() { broth.setColor(new THREE.Color(0xf5f0e0), 0.85); },
    handler: { down() {
      const h = input.pick([pl.agar], false, false);
      if (h) { if (!ctx.requireTool('loop')) return true; const c = pl.colonyAt(h.uv); if (!c) return true; if (c.kind === 'contam') { ctx.mistake('That red colony took up the dye: it is not Rhizobium.', 2); return true; } this.got = true; sfx.play('pick'); return true; }
      if (!input.pick([broth.group], true)) return false; if (!this.got) { ctx.say('Pick up a white colony first.', 'hint', 1500); return true; }
      sfx.play('drip'); anim.add(1.5, (k) => broth.setColor(new THREE.Color(0xfefce8).lerp(new THREE.Color(0xf5f0e0), k), 0.45 + k * 0.4), { done: () => ctx.next('After three days on a shaker the broth is milky with about 10⁹ cells per mL.') }); return true;
    } },
  };
  const stepCarrier = {
    title: 'Mix with the carrier', text: '200 g of fine lignite, neutralised with CaCO₃ and sterilised, is in the tray. <b>Hold</b> on the broth flask to pour it in; stop when the mix is about <b>40% moisture</b>.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([-0.55, 1.8, 1.6], [-0.6, 0.35, -0.6], 1.9),
    enter() { lignite.visible = true; },
    skip() { added = 133; moisture = 40; },
    handler: { down() { if (!input.pick([broth.group], true)) return false; this.pouring = true; sfx.play('pour'); return true; }, up() { if (!this.pouring) return; this.pouring = false; stepCarrier.check(); } },
    update(dt) {
      const h = this.handler; if (h.pouring) { added += dt * 45; moisture = added / (200 + added) * 100; broth.setVolume(Math.max(0, 200 - added)); lignite.material.color.setRGB(1 - moisture / 160, 1 - moisture / 160, 1 - moisture / 160); }
      lignite.getWorldPosition(chip.at); chip.at.y += 0.12; chip.set(`<b>${moisture.toFixed(0)}%</b> moisture`).show(ctx.stepIndex === steps.indexOf(stepCarrier) && added > 0);
    },
    check() {
      if (moisture < 35) { ctx.say(`${moisture.toFixed(0)}% — still too dry; Rhizobium dies in a dry carrier. Pour a little more.`, 'hint', 2200); return; }
      if (moisture > 46) { ctx.mistake(`${moisture.toFixed(0)}% — too wet: the carrier turns pasty and lumps. Aim for 40%.`, 3); added = 133; moisture = 40; }
      chip.show(false); ui.observe('Carrier moisture', `${moisture.toFixed(0)} %`); ctx.next('Mixed to a moist powder and packed in polythene bags: the biofertilizer.');
    },
    exit() { chip.show(false); },
  };
  const stepSeeds = {
    title: 'Coat the seeds', text: 'Tap the <b>jaggery solution</b> to wet the seeds (the sticker), then tap the <b>inoculant</b> in the tray to coat them.', tool: null, autoTool: 'hand', shot: S([0.3, 1.7, 2.4], [0.2, 0.2, 0.0], 3.0),
    enter() { bowl.group.visible = true; jag.visible = true; },
    skip() { seeds.children.forEach((s) => s.material.color.setHex(0x2b2522)); },
    handler: { down() {
      if (input.pick([jag], true)) { this.sticky = true; sfx.play('pour'); seeds.children.forEach((s) => { s.material = s.material.clone(); s.material.clearcoat = 1; }); return true; }
      if (!input.pick([tray, lignite], true)) return false;
      if (!this.sticky) { ctx.mistake('Without the jaggery sticker the powder falls off the seeds.', 2); return true; }
      sfx.play('pour'); seeds.children.forEach((s) => s.material.color.setHex(0x2b2522));
      ask(ctx, 'Dry the coated seeds…', [{ label: 'In the shade, then sow soon', value: 'shade' }, { label: 'In strong sunlight', value: 'sun' }], 'shade', { delay: 0.3, wrong: 'Sunlight and heat kill the bacteria on the seed coat.', ok: 'In the shade, and sown within a day.' });
      return true;
    } },
    exit() { ui.clearChooser(); },
  };
  const stepWhy = {
    title: 'Why use a biofertilizer?', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: S_ALL,
    enter() { ask(ctx, 'Rhizobium biofertilizer helps the crop because…', [{ label: 'It forms root nodules that fix atmospheric N₂ into ammonia', value: 'ok' }, { label: 'It kills soil pests', value: 'p' }, { label: 'It adds phosphate rock to the soil', value: 'ph' }], 'ok', { ok: 'Symbiotic Rhizobium fixes nitrogen (N₂ → NH₃ by nitrogenase, protected by leghaemoglobin) inside legume nodules — often 50–100 kg N per hectare — so less urea is needed, saving money and reducing soil and water pollution. Azotobacter (free-living) and blue-green algae are other nitrogen biofertilizers.', wrong: 'Think about what the pink nodules do.' }); },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepUproot, stepWash, stepPick, stepSter, stepCrush, stepStreak, stepInc, stepBroth, stepCarrier, stepSeeds, stepWhy];
  ctx.debug = { pl, nodules, plant };
  void ease; void MAT;
  return {
    tools: ['hand', 'lens', 'forceps', 'loop'],
    steps,
    update() { lens.update(); hud.update(); },
    result() { return { title: 'Rhizobium biofertilizer', rows: [['Nodules chosen', `${picked.length} pink`], ['Rinses after HgCl₂', String(rinses)], ['Colonies on YEMA–Congo red', 'white, gummy (Rhizobium); few red contaminants'], ['Carrier moisture', `${moisture.toFixed(0)} %`]], conclusion: 'Rhizobium was isolated from pink root nodules of a legume on yeast-extract mannitol agar, where its colonies stay white on Congo red. Grown in broth and mixed with a neutral carrier at about 40% moisture it becomes a biofertilizer; coated on seeds with a sticker it nodulates the new crop and fixes atmospheric nitrogen, cutting the need for chemical fertilizer.' }; },
    dispose() { lens.dispose(); pl.dispose(); hud.dispose(); ui.clearChooser(); },
  };
}
