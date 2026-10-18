// The biochemical tests, done in test tubes on the bench: the iodine test for starch, the biuret
// test for protein, the four urine tests (sodium hypobromite for urea, Benedict's for sugar, heat
// and acetic acid for albumin, Hay's sulphur test for bile salts), salivary amylase acting on
// starch at different temperatures (followed on a spot tile with iodine), and blood glucose with
// a lancet, a test strip and a meter.
import { THREE } from '../../engine.js';
import { reagentBottle, spiritLamp } from '../props.js';
import { makeTube, makeRack, makeWaterBath, makeSpotTile } from '../glassware.js';
import { ease, clamp, mesh, MAT, canvasTexture, wet } from '../kit.js';

const BLUEBLACK = 0x1b1530;
const SETS = {
  'starch-detection-sample': {
    tubes: [['Potato', 0xf3efe0, BLUEBLACK, true], ['Rice water', 0xf2f0e8, 0x221a46, true], ['Milk', 0xfafaf5, 0xe6c58f, false], ['Water', 0xe8f4fb, 0xc98a2e, false]],
    reagents: [{ name: 'Iodine solution', short: 'iodine', color: 0x8b4513, drops: 2 }],
    question: 'Which samples contain starch?',
    explain: 'Iodine (yellow-brown) forms a blue-black complex with the coiled amylose of starch. Potato and rice water turned blue-black; milk and water stayed yellow-brown, so they have no starch. Water was the control.',
  },
  'protein-detection-sample': {
    tubes: [['Egg albumin', 0xf4efd2, 0x6d28d9, true], ['Milk', 0xfafaf5, 0x8b5cf6, true], ['Potato extract', 0xf3efe0, 0xa5b4fc, false], ['Water', 0xe8f4fb, 0x7dd3fc, false]],
    reagents: [{ name: '10% NaOH', short: 'NaOH', color: 0xf1f5f9, drops: 3, tint: 0.15 }, { name: '1% CuSO₄', short: 'CuSO₄', color: 0x38bdf8, drops: 2 }],
    question: 'Which samples gave a positive biuret test?',
    explain: 'In alkaline solution, copper(II) ions bind the peptide bonds of proteins and turn violet. Egg albumin and milk turned violet; potato extract only faintly lilac (little protein); water stayed the pale blue of copper sulphate — the control.',
  },
};

export function create(ctx) {
  const slug = ctx.config.slug;
  if (slug === 'urine-tests-urea-sugar-albumin-bile') return urine(ctx);
  if (slug === 'salivary-amylase-temp-ph') return amylase(ctx);
  if (slug === 'blood-sugar-detection') return glucose(ctx);
  return tubeTests(ctx, SETS[slug]);
}

function bench(ctx, n) {
  const { world } = ctx;
  const rack = makeRack(n); rack.group.position.set(0, 0, 0); world.add(rack.group);
  const tile = mesh(new THREE.BoxGeometry(2.4, 0.02, 1.4), MAT.gloss(0xf8fafc), [0, 0.01, 0.1]); world.add(tile);
  ctx.surfaces.push(tile);
  return rack;
}
function pickTube(ctx, tubes, px, py, tmp, tmp2) {
  let best = -1; let bd = 60;
  tubes.forEach((t, i) => { t.group.getWorldPosition(tmp); tmp.y += 0.5; ctx.input.project(tmp, tmp2, ctx.stage.clientWidth, ctx.stage.clientHeight); const d = Math.hypot(tmp2.x - px, tmp2.y - py); if (d < bd) { bd = d; best = i; } });
  return best;
}

// ---- starch and protein ----------------------------------------------------------------------
function tubeTests(ctx, cfg) {
  const { world, anim, sfx, ui, fx } = ctx;
  const rack = bench(ctx, cfg.tubes.length);
  const tubes = cfg.tubes.map(([label], i) => { const t = makeTube(label); t.group.position.copy(rack.slots[i]); world.add(t.group); return t; });
  const bottles = cfg.reagents.map((r, i) => { const b = reagentBottle(r.name, r.color, ''); b.position.set(-1.25 + i * 0.4, 0, -0.55); world.add(b); return b; });
  cfg.tubes.forEach(([label, col], i) => { const b = reagentBottle(label, col, 'extract'); b.scale.setScalar(0.7); b.position.set(0.15 + i * 0.36, 0, -0.62); world.add(b); });
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3();
  const SHOT = { pos: [0, 2.35, 2.9], target: [0, 1.15, -0.1], fit: 2.6, fitH: 2.0 };
  const steps = [];
  const filled = new Set();
  steps.push({
    title: 'Put each sample in its tube', text: 'Pour about 2 mL of each extract into the matching labelled tube — tap each tube.', tool: null, autoTool: 'hand', shot: SHOT,
    skip() { tubes.forEach((t, i) => { t.setFill(0.2); t.material.color.set(cfg.tubes[i][1]); filled.add(i); }); },
    handler: { down(p) { const i = pickTube(ctx, tubes, p.x, p.y, tmp, tmp2); if (i < 0) return false; if (filled.has(i)) return true; filled.add(i); sfx.play('pour'); tubes[i].material.color.set(cfg.tubes[i][1]); tubes[i].to(anim, { fill: 0.2, dur: 0.9 }); ctx.progress(filled.size / tubes.length); if (filled.size === tubes.length) anim.wait(1, () => ctx.next(`${tubes.length} tubes, 2 mL each. The water tube is the control.`)); return true; } },
  });
  cfg.reagents.forEach((r, ri) => {
    const drops = new Array(tubes.length).fill(0); let loaded = false;
    steps.push({
      title: `Add ${r.name}`, text: `Tap the <b>${r.name}</b> bottle to fill the dropper, then add <b>${r.drops} drops</b> to every tube.`, hint: 'Tap the reagent bottle at the back, then tap each tube the right number of times.', tool: 'dropper', shot: SHOT,
      skip() { tubes.forEach((t, i) => { drops[i] = r.drops; finishTube(i, true); }); },
      onTool() { const m = ctx.tools.id === 'dropper' && ctx.tools.model; if (m && m.userData.liquid) m.userData.liquid.material.color.setHex(r.color); },
      handler: {
        down(p) {
          if (ctx.input.pick([bottles[ri]])) { if (!ctx.requireTool('dropper')) return true; loaded = true; sfx.play('pick'); ctx.say(`Dropper filled with ${r.short}.`, 'info', 1500); return true; }
          const i = pickTube(ctx, tubes, p.x, p.y, tmp, tmp2); if (i < 0) return false;
          if (!ctx.requireTool('dropper')) return true;
          if (!loaded) { ctx.say(`Fill the dropper from the ${r.name} bottle first.`, 'hint', 2000); return true; }
          if (ri === 1 && drops.some((d) => d < 0)) return true;
          drops[i] += 1; sfx.play('drop'); ctx.tools.action(1); anim.wait(0.12, () => ctx.tools.action(0));
          tubes[i].top(tmp); fx.burst(tmp, r.color, 2, 0.05, tmp.y - 0.02);
          if (drops[i] === r.drops) finishTube(i, false);
          if (drops[i] === r.drops + 3) ctx.mistake(`Too many drops in that tube. ${r.drops} drops are enough — excess reagent can mask the colour change.`, 2);
          const done = drops.filter((d) => d >= r.drops).length; ctx.progress(done / tubes.length);
          if (done === tubes.length && !this.done) { this.done = true; anim.wait(1.6, () => ctx.next(ri === cfg.reagents.length - 1 ? 'Shake each tube gently and look at the colours.' : 'Mixed.')); }
          return true;
        },
      },
    });
    function finishTube(i, instant) {
      const last = ri === cfg.reagents.length - 1; const t = tubes[i];
      const color = last ? cfg.tubes[i][2] : new THREE.Color(cfg.tubes[i][1]).lerp(new THREE.Color(r.color), r.tint || 0.3).getHex();
      if (instant) { t.material.color.set(color); t.setFill(t.fill + 0.02); return; }
      t.to(anim, { color, fill: t.fill + 0.02, dur: last ? 1.6 : 0.6, opacity: last ? 0.93 : undefined });
    }
  });
  steps.push({
    title: 'Read the results', text: 'Compare every tube with the control.', tool: null, autoTool: 'hand', hideBelt: true, shot: SHOT,
    enter() {
      const ask = () => ui.chooseMany(ctx.stage.clientWidth / 2, 50, cfg.question, cfg.tubes.map(([l]) => ({ label: l, value: l })), (picked) => {
        const right = cfg.tubes.filter((t) => t[3]).map((t) => t[0]);
        const ok = picked.length === right.length && right.every((r) => picked.includes(r));
        if (ok) { cfg.tubes.forEach(([l, , , pos]) => ui.observe(l, pos ? 'positive' : 'negative')); ctx.next(cfg.explain, 1.4); }
        else { ctx.mistake('Not quite — compare each tube\'s colour with the control (water).', 3); anim.wait(0.4, ask); }
      });
      anim.wait(0.8, ask);
    },
    exit() { ui.clearChooser(); },
  });
  return {
    tools: ['hand', 'dropper'], steps,
    result() { return { title: ctx.config.title, rows: cfg.tubes.map(([l, , , p]) => [l, p ? 'positive' : 'negative']), conclusion: cfg.explain }; },
  };
}

// ---- urine ---------------------------------------------------------------------------------------
function urine(ctx) {
  const { world, anim, sfx, ui, fx } = ctx;
  const profiles = [{ name: 'diabetic', sugar: 3, albumin: false, bile: false }, { name: 'kidney disease', sugar: 0, albumin: true, bile: false }, { name: 'jaundice', sugar: 0, albumin: false, bile: true }];
  const pt = profiles[Math.floor(Math.random() * profiles.length)];
  const rack = bench(ctx, 4);
  const labels = ['Urea', 'Sugar', 'Albumin', 'Bile salts'];
  const tubes = labels.map((l, i) => { const t = makeTube(l); t.group.position.copy(rack.slots[i]); world.add(t.group); t.material.color.set(0xf5d76e); t.setFill(0.22); return t; });
  tubes[1].material.color.set(0x60a5fa); // Benedict's reagent
  const bath = makeWaterBath(); bath.position.set(1.3, 0, -0.1); world.add(bath);
  const lamp = spiritLamp(); lamp.position.set(-1.25, 0, 0.3); world.add(lamp);
  const bottles = [['NaOBr', 0xfef9c3], ['Urine', 0xf5d76e], ['Acetic acid', 0xf8fafc], ['Sulphur', 0xfde047]].map(([n, c], i) => { const b = reagentBottle(n, c, ''); b.scale.setScalar(0.8); b.position.set(-0.75 + i * 0.5, 0, -0.65); world.add(b); return b; });
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3();
  const SHOT = { pos: [0.1, 2.4, 3.0], target: [0.1, 1.15, -0.1], fit: 3.1, fitH: 2.0 };
  const results = {}; const alb = {};
  const tubeAt = (p) => pickTube(ctx, tubes, p.x, p.y, tmp, tmp2);
  const steps = [
    {
      title: 'Urea: sodium hypobromite', text: 'To the urine in tube 1, add a few drops of <b>sodium hypobromite</b> (tap the NaOBr bottle, then the tube).', tool: 'dropper', shot: SHOT,
      skip() { results.urea = true; },
      handler: { down(p) { if (ctx.input.pick([bottles[0]])) { this.loaded = true; sfx.play('pick'); return true; } const i = tubeAt(p); if (i < 0) return false; if (!ctx.requireTool('dropper')) return true; if (i !== 0) { ctx.say('Tube 1 (Urea) for this test.', 'hint', 1800); return true; } if (!this.loaded) { ctx.say('Fill the dropper from the NaOBr bottle first.', 'hint', 1800); return true; }
        sfx.play('drop'); let n = 0; const fizz = () => { tubes[0].top(tmp); fx.burst(tmp, 0xffffff, 6, 0.25, tmp.y - 0.05); n += 1; if (n < 12) anim.wait(0.15, fizz); }; fizz();
        results.urea = true; anim.wait(2, () => ctx.next('Brisk effervescence: nitrogen gas from urea. Urea is a normal constituent of urine.')); return true; } },
    },
    {
      title: 'Sugar: Benedict\'s test', text: 'Tube 2 holds 5 mL of blue Benedict\'s reagent. Add <b>8 drops of urine</b>, then stand it in the <b>boiling water bath</b> for two minutes (tap the bath).', tool: 'dropper', shot: SHOT,
      skip() { results.sugar = pt.sugar; },
      handler: { down(p) {
        if (ctx.input.pick([bottles[1]])) { this.loaded = true; sfx.play('pick'); return true; }
        if (ctx.input.pick([bath])) {
          if ((this.d || 0) < 8) { ctx.say('Add the 8 drops of urine first.', 'hint', 1800); return true; }
          if (this.heating) return true; this.heating = true; bath.userData.flame.visible = true; sfx.play('click');
          const t = tubes[1]; const from = t.group.position.clone(); const to = new THREE.Vector3(bath.position.x, 0.38, bath.position.z);
          const col = [0x3b82f6, 0x65a30d, 0xeab308, 0xea580c, 0xb91c1c][pt.sugar];
          anim.add(0.8, (k) => { t.group.position.lerpVectors(from, to, k); t.group.position.y += Math.sin(Math.PI * k) * 0.4; }, { ease: ease.inOut, done: () => { t.to(anim, { color: col, dur: 3 }); if (pt.sugar > 1) t.precipitate(anim, col, 0.6); anim.add(3.2, (k) => { ctx.progress(k); ui.setText(`Boiling… ${Math.round(k * 120)} s`); if (Math.random() < 0.3) { bath.localToWorld(tmp.set((Math.random() - 0.5) * 0.6, 0.8, (Math.random() - 0.5) * 0.6)); fx.burst(tmp, 0xffffff, 1, 0.1, tmp.y + 0.1); } }, { ease: (x) => x, done: () => { results.sugar = pt.sugar; ctx.next(pt.sugar ? 'Benedict\'s turned orange with a brick-red precipitate: reducing sugar (glucose) present, about ++. Glucose in urine (glycosuria) suggests diabetes mellitus.' : 'Benedict\'s stayed blue: no sugar.'); } }); } });
          return true;
        }
        const i = tubeAt(p); if (i < 0) return false; if (!ctx.requireTool('dropper')) return true; if (i !== 1) { ctx.say('Tube 2 (Sugar).', 'hint', 1500); return true; }
        if (!this.loaded) { ctx.say('Fill the dropper with urine first.', 'hint', 1800); return true; }
        this.d = (this.d || 0) + 1; sfx.play('drop'); ctx.progress(Math.min(1, this.d / 8) * 0.3); if (this.d === 8) ctx.say('8 drops in. Now into the boiling water bath.', 'info', 2200); return true;
      } },
    },
    {
      title: 'Albumin: heat and acetic acid', text: 'Hold tube 3 (urine) by its foot and heat <b>only the upper part</b> over the spirit lamp (press and hold the tube), then add a few drops of <b>acetic acid</b>.', tool: null, autoTool: 'hand', shot: SHOT,
      skip() { results.albumin = pt.albumin; },
      update(dt) {
        const t = tubes[2];
        if (alb.holding) { lamp.userData.flame.visible = true; alb.heat = Math.min(1, (alb.heat || 0) + dt * 0.35); ctx.progress(alb.heat * 0.6); t.material.color.setHex(0xf5d76e).lerp(new THREE.Color(0xf2f2ee), alb.heat * 0.7); t.material.opacity = 0.8 + alb.heat * 0.15; }
        if (alb.heat >= 1 && !alb.cloud) { alb.cloud = true; ctx.say('A white cloud forms in the heated top part. Now add acetic acid: phosphates dissolve in acid; coagulated albumin does not.', 'info', 4500); }
      },
      handler: {
        down(p) {
          if (ctx.input.pick([bottles[2]])) { if (!alb.cloud) { ctx.say('Heat the top of the tube first.', 'hint', 1800); return true; } sfx.play('drop'); const t = tubes[2]; if (pt.albumin) { t.material.color.setHex(0xf4f4f0); ctx.next('The cloud persists after acid: albumin (protein) present — albuminuria, a sign of kidney damage.'); } else { t.to(anim, { color: 0xf5d76e, opacity: 0.8, dur: 1 }); ctx.next('The cloud cleared in acid: it was only phosphates. No albumin.'); } results.albumin = pt.albumin; return true; }
          const i = tubeAt(p); if (i !== 2) return i >= 0;
          alb.holding = true; const t = tubes[2]; alb.home = alb.home || t.group.position.clone(); const to = lamp.position.clone().add(tmp.set(0.08, 0.2, 0)); t.group.position.copy(to); t.group.rotation.z = -0.5; return true;
        },
        up() { if (!alb.holding) return; alb.holding = false; lamp.userData.flame.visible = false; const t = tubes[2]; t.group.position.copy(alb.home); t.group.rotation.z = 0; },
      },
    },
    {
      title: 'Bile salts: Hay\'s sulphur test', text: 'Sprinkle a little <b>sulphur powder</b> on the surface of the urine in tube 4 (tap the sulphur bottle, then the tube). Does it float or sink?', tool: null, autoTool: 'hand', shot: SHOT,
      skip() { results.bile = pt.bile; },
      handler: { down(p) {
        if (ctx.input.pick([bottles[3]])) { this.loaded = true; sfx.play('pick'); return true; }
        const i = tubeAt(p); if (i < 0) return false; if (i !== 3) { ctx.say('Tube 4.', 'hint', 1200); return true; } if (!this.loaded) { ctx.say('Take some sulphur powder first.', 'hint', 1500); return true; }
        const t = tubes[3]; t.top(tmp); const flecks = []; for (let k = 0; k < 14; k++) { const f = mesh(new THREE.SphereGeometry(0.008, 6, 4), MAT.matte(0xfde047)); f.position.copy(tmp).add(tmp2.set((Math.random() - 0.5) * 0.1, 0, (Math.random() - 0.5) * 0.1)); ctx.scene.add(f); flecks.push(f); }
        const y0 = tmp.y; anim.add(2.2, (k) => flecks.forEach((f, j) => { f.position.y = pt.bile ? y0 - k * (0.18 + j * 0.008) : y0 + Math.sin(k * 6 + j) * 0.003; }), { done: () => { results.bile = pt.bile; ctx.next(pt.bile ? 'The sulphur sank: bile salts lower the surface tension — bile salts present (as in jaundice).' : 'The sulphur floats: normal surface tension, no bile salts.'); } });
        ctx.dispose.push(() => flecks.forEach((f) => { ctx.scene.remove(f); f.geometry.dispose(); }));
        return true;
      } },
    },
    {
      title: 'Report', text: 'Which abnormal constituents did you find in this sample?', tool: null, autoTool: 'hand', hideBelt: true, shot: SHOT,
      enter() {
        const ask = () => ui.chooseMany(ctx.stage.clientWidth / 2, 50, 'Abnormal constituents present', [{ label: 'Sugar', value: 'sugar' }, { label: 'Albumin', value: 'albumin' }, { label: 'Bile salts', value: 'bile' }], (picked) => {
          const right = ['sugar', 'albumin', 'bile'].filter((k) => (k === 'sugar' ? pt.sugar > 0 : pt[k]));
          if (picked.length === right.length && right.every((r) => picked.includes(r))) { ui.observe('Urea', 'present (normal)'); ui.observe('Sugar', pt.sugar ? 'present' : 'absent'); ui.observe('Albumin', pt.albumin ? 'present' : 'absent'); ui.observe('Bile salts', pt.bile ? 'present' : 'absent'); ctx.next(`This urine points to ${pt.name}.`); }
          else { ctx.mistake('Look back at each tube: which tests were positive? Urea is always present in normal urine.', 3); anim.wait(0.4, ask); }
        });
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];
  return {
    tools: ['hand', 'dropper'], steps,
    result() { return { title: 'Urine analysis', rows: [['Urea', 'present (normal)'], ['Sugar', pt.sugar ? 'present' : 'absent'], ['Albumin', pt.albumin ? 'present' : 'absent'], ['Bile salts', pt.bile ? 'present' : 'absent'], ['Suggests', pt.name]], conclusion: 'Normal urine contains urea but no sugar, albumin or bile salts. Glucose suggests diabetes mellitus, albumin suggests kidney disease, and bile salts suggest jaundice (liver or bile-duct disease).' }; },
  };
}

// ---- salivary amylase ------------------------------------------------------------------------------
function amylase(ctx) {
  const { world, anim, sfx, ui } = ctx;
  const rack = bench(ctx, 4);
  const conds = [{ label: '5 °C', T: 5, pH: 6.8 }, { label: '37 °C', T: 37, pH: 6.8 }, { label: '80 °C', T: 80, pH: 6.8 }, { label: '37 °C pH 4', T: 37, pH: 4 }];
  const tubes = conds.map((c, i) => { const t = makeTube(c.label); t.group.position.copy(rack.slots[i]); world.add(t.group); t.material.color.set(0xf3f1ea); t.setFill(0.25); return t; });
  const tile = makeSpotTile(16); tile.group.position.set(0.15, 0, 0.75); world.add(tile.group);
  const rate = (c) => { const tf = c.T > 60 ? 0 : Math.exp(-Math.pow((c.T - 37) / 14, 2)); const pf = Math.exp(-Math.pow((c.pH - 6.8) / 1.4, 2)); return tf * pf; };
  let minute = 0; let ach = {};
  const colorAt = (c, m) => { const left = Math.max(0, 1 - rate(c) * m / 6); return left > 0.6 ? BLUEBLACK : left > 0.3 ? 0x5b2a6e : left > 0.08 ? 0x8b3a2b : 0xb7791f; };
  const SHOT = { pos: [0.1, 2.3, 2.6], target: [0.1, 1.0, 0.3], fit: 2.5, fitH: 2.0 };
  const steps = [
    {
      title: 'Start the reaction', text: 'Each tube has 5 mL of 1% starch at its temperature (and one at pH 4). Tap each tube to add 1 mL of diluted saliva, then start the clock.', tool: null, autoTool: 'hand', shot: SHOT,
      skip() { this.n = 4; },
      handler: { down(p) { const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3(); const i = pickTube(ctx, tubes, p.x, p.y, tmp, tmp2); if (i < 0) return false; this.done = this.done || new Set(); if (this.done.has(i)) return true; this.done.add(i); sfx.play('drop'); tubes[i].to(anim, { fill: 0.3, dur: 0.6 }); ctx.progress(this.done.size / 4); if (this.done.size === 4) ctx.next('Clock started. Saliva contains salivary amylase (ptyalin), which digests starch to maltose.'); return true; } },
    },
    {
      title: 'Test a drop every minute', text: 'Each minute, put a drop from every tube into a well of iodine on the spot tile (tap the tile). Keep going until the 37 °C tube no longer turns iodine blue-black.', tool: null, autoTool: 'hand', shot: SHOT,
      skip() { minute = 4; ach = { 0: null, 1: 3, 2: null, 3: null }; },
      handler: { down() {
        if (!ctx.input.pick([tile.group])) return false;
        if (minute >= 4) return true;
        minute += 1; sfx.play('drop');
        conds.forEach((c, i) => { const spot = tile.spots[(minute - 1) * 4 + i]; spot.drop.visible = true; spot.drop.material.color.setHex(colorAt(c, minute)); if (colorAt(c, minute) === 0xb7791f && ach[i] === undefined) ach[i] = minute; });
        ui.observe(`Minute ${minute}`, conds.map((c) => { const col = colorAt(c, minute); return col === BLUEBLACK ? 'B' : col === 0xb7791f ? 'Y' : 'P'; }).join(' · '));
        ctx.progress(minute / 4);
        if (minute === 4) anim.wait(1, () => ctx.next('B = blue-black (starch left), P = purple/red-brown (dextrins), Y = yellow (achromic point: all starch digested).'));
        return true;
      } },
    },
    {
      title: 'Conclude', text: 'At which condition did the starch disappear fastest?', tool: null, autoTool: 'hand', hideBelt: true, shot: SHOT,
      enter() {
        const ask = () => ui.choose(ctx.stage.clientWidth / 2, 50, 'Fastest digestion (optimum)', conds.map((c, i) => ({ label: c.label, value: i })), (v) => {
          if (v === 1) ctx.next('37 °C and near-neutral pH is optimum for salivary amylase. At 5 °C it works very slowly; at 80 °C the enzyme protein is denatured; at pH 4 it is inhibited.');
          else { ctx.mistake('Look at which column on the spot tile reached yellow first.', 3); anim.wait(0.4, ask); }
        });
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];
  return { tools: ['hand'], steps, result() { return { title: 'Salivary amylase', rows: conds.map((c, i) => [c.label, ach[i] ? `achromic by ${ach[i]} min` : 'starch remained']), conclusion: 'Salivary amylase digests starch fastest at body temperature (37 °C) and near-neutral pH (about 6.8). Low temperature slows it; high temperature denatures it; acid inhibits it — enzymes are proteins with an optimum temperature and pH.' }; } };
}

// ---- blood glucose ---------------------------------------------------------------------------------
function glucose(ctx) {
  const { world, anim, sfx, ui, fx, input } = ctx;
  const value = [82, 96, 118, 165, 238][Math.floor(Math.random() * 5)];
  const finger = mesh(new THREE.CapsuleGeometry(0.09, 0.42, 6, 14), wet(0xe0a989, { roughness: 0.6, clearcoat: 0.2 }), [-0.35, 0.1, 0.2]); finger.rotation.z = Math.PI / 2; world.add(finger);
  const nail = mesh(new THREE.SphereGeometry(0.07, 16, 10), wet(0xf2c9b8, { roughness: 0.25, clearcoat: 1 }), [-0.12, 0.17, 0.2]); nail.scale.set(1.2, 0.25, 0.9); world.add(nail);
  [-0.36, -0.52].forEach((x) => { const crease = mesh(new THREE.TorusGeometry(0.09, 0.004, 4, 20, Math.PI), MAT.matte(0xc58b70), [x, 0.1, 0.2]); crease.rotation.y = Math.PI / 2; world.add(crease); });
  const swab = mesh(new THREE.BoxGeometry(0.16, 0.01, 0.16), MAT.matte(0xffffff), [-0.9, 0.006, 0.4]); world.add(swab);
  const meter = new THREE.Group(); meter.position.set(0.55, 0, 0.15); world.add(meter);
  meter.add(mesh(new THREE.BoxGeometry(0.42, 0.1, 0.7), MAT.gloss(0x1f2937), [0, 0.05, 0]));
  const lcdCanvas = document.createElement('canvas'); lcdCanvas.width = 256; lcdCanvas.height = 128; const lg = lcdCanvas.getContext('2d');
  const lcdTex = new THREE.CanvasTexture(lcdCanvas);
  const lcd = mesh(new THREE.PlaneGeometry(0.32, 0.16), new THREE.MeshBasicMaterial({ map: lcdTex }), [0, 0.101, -0.1]); lcd.rotation.x = -Math.PI / 2; meter.add(lcd);
  const strip = mesh(new THREE.BoxGeometry(0.06, 0.006, 0.3), MAT.plastic(0xf8fafc), [0, 0.06, 0.48]); meter.add(strip);
  const pad = mesh(new THREE.BoxGeometry(0.04, 0.008, 0.04), MAT.plastic(0xfacc15), [0, 0.062, 0.6]); meter.add(pad);
  function show(t) { lg.fillStyle = '#b8c9a6'; lg.fillRect(0, 0, 256, 128); lg.fillStyle = '#1f2a1a'; lg.font = '700 64px monospace'; lg.textAlign = 'center'; lg.fillText(t, 128, 80); lg.font = '600 20px monospace'; lg.fillText('mg/dL', 200, 115); lcdTex.needsUpdate = true; }
  show('---');
  const tip = new THREE.Vector3(-0.1, 0.12, 0.29);
  const SHOT = { pos: [0.05, 1.6, 1.5], target: [0.05, 0.85, 0.25], fit: 1.7 };
  let rub = 0; let last = null; let pricked = false; let dropOn = null; let lanceMark = null;
  const steps = [
    {
      title: 'Clean the fingertip', text: 'Rub the side of the fingertip with the <b>spirit swab</b> and let it dry.', tool: 'paper', shot: SHOT,
      skip() { rub = 400; },
      handler: { down(p) { if (!input.pick([finger])) return false; if (!ctx.requireTool('paper', 'Use the spirit swab (cotton) to clean the skin.')) return true; last = [p.x, p.y]; return true; }, move(p) { if (!last) return; rub += Math.hypot(p.x - last[0], p.y - last[1]); last = [p.x, p.y]; ctx.progress(clamp(rub / 400)); if (rub >= 400 && !this.done) { this.done = true; last = null; ctx.next('Clean and dry — spirit left wet would dilute the blood and sting.'); } }, up() { last = null; } },
    },
    {
      title: 'Prick with a sterile lancet', text: 'Use a fresh, sterile lancet once on the side of the fingertip — tap the glowing spot.', tool: 'needle', shot: SHOT,
      enter() { lanceMark = fx.mark(world.localToWorld(tip.clone()), 0.03, 0xef4444); },
      exit() { if (lanceMark) fx.unmark(lanceMark); lanceMark = null; },
      skip() { pricked = true; },
      handler: { down(p) { const v = new THREE.Vector3(); input.project(lanceMark.position, v, ctx.stage.clientWidth, ctx.stage.clientHeight); if (Math.hypot(v.x - p.x, v.y - p.y) > 40) return false; if (!ctx.requireTool('needle', 'Use the sterile lancet.')) return true; pricked = true; sfx.play('pin'); dropOn = mesh(new THREE.SphereGeometry(0.02, 12, 8), wet(0x9b1022, { clearcoat: 1 }), [tip.x, tip.y + 0.01, tip.z]); world.add(dropOn); dropOn.scale.setScalar(0.1); anim.add(0.8, (k) => dropOn.scale.setScalar(0.1 + k * 0.9), { ease: ease.outBack }); anim.wait(1, () => ctx.next('Wipe away the first drop; use the second, which is not diluted by tissue fluid.')); return true; } },
      update() {},
    },
    {
      title: 'Apply the drop to the strip', text: 'Touch the drop to the yellow test pad of the strip in the meter.', tool: null, autoTool: 'hand', shot: SHOT,
      skip() { show(String(value)); },
      handler: { down() { if (!input.pick([pad, strip, meter])) return false; if (!pricked) return true; sfx.play('drop'); if (dropOn) { anim.add(0.4, (k) => dropOn.scale.setScalar(1 - k), { done: () => { dropOn.visible = false; } }); } pad.material = pad.material.clone(); pad.material.color.setHex(0x9b1022);
        let n = 5; const tick = () => { show(String(n)); sfx.play('click'); n -= 1; if (n >= 0) anim.wait(0.7, tick); else { show(String(value)); sfx.play('ok'); ui.observe('Blood glucose', `${value} mg/dL`); ctx.next(`The meter reads ${value} mg/dL.`); } }; tick(); return true; } },
    },
    {
      title: 'Interpret', text: `The sample was taken after an overnight fast. The meter reads <b>${value} mg/dL</b>.`, tool: null, autoTool: 'hand', hideBelt: true, shot: SHOT,
      enter() {
        const band = value < 100 ? 'normal' : value < 126 ? 'pre' : 'diabetes';
        const ask = () => ui.choose(ctx.stage.clientWidth / 2, 50, 'Fasting blood glucose is…', [{ label: 'Normal (70–99)', value: 'normal' }, { label: 'Raised: prediabetes (100–125)', value: 'pre' }, { label: 'Diabetic range (126 or more)', value: 'diabetes' }], (v) => {
          if (v === band) { ui.observe('Interpretation', band === 'normal' ? 'normal' : band === 'pre' ? 'prediabetes' : 'diabetic range'); ctx.next('Fasting glucose: below 100 mg/dL normal, 100–125 prediabetes, 126 or above (on two occasions) diabetes mellitus. Insulin from the pancreas keeps it in range.'); }
          else { ctx.mistake('Compare the reading with the fasting ranges: normal below 100, prediabetes 100–125, diabetes 126 and above.', 3); anim.wait(0.4, ask); }
        });
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];
  return { tools: ['hand', 'paper', 'needle'], steps, result() { return { title: 'Blood glucose', rows: [['Reading (fasting)', `${value} mg/dL`]], conclusion: 'Blood glucose is measured from a drop of capillary blood: glucose oxidase on the strip reacts with glucose and the meter converts the signal to mg/dL. Fasting values below 100 mg/dL are normal; 126 mg/dL or more indicates diabetes mellitus.' }; }, dispose() { lcdTex.dispose(); } };
}
