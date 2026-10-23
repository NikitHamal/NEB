// External morphology of the cockroach. Anaesthetise it in a killing jar with chloroform-soaked
// cotton, tip it into the wax tray, study it with a hand lens region by region, spread a tegmen
// and fan out the hind wing beneath it with forceps, label the parts, decide its sex from the
// tail end (anal styles in males; a boat-shaped seventh sternum in females), then turn it over and
// remove the mouthparts in their natural order onto a slide.
import { THREE } from '../../engine.js';
import { dissectingTray, reagentBottle, slide as makeSlide } from '../props.js';
import { buildCockroach } from '../specimens/cockroach.js';
import { createLens } from '../lens.js';
import { createLabelQuiz } from '../labelquiz.js';
import { ask, tag, glassBeaker } from '../bench.js';
import { mesh, MAT, clamp, ease, rng } from '../kit.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const FACTS = {
  head: 'Head: small, pear-shaped and bent down at right angles to the body (hypognathous). Large kidney-shaped <b>compound eyes</b> and a pair of long, many-jointed <b>filiform antennae</b>, the organs of touch and smell.',
  thorax: 'Thorax: three segments. The large <b>pronotum</b> shields the prothorax and the head; the meso- and metathorax carry the wings, and each segment one pair of legs.',
  wings: 'Two pairs of wings: the dark, leathery <b>tegmina</b> (forewings, from the mesothorax) cover and protect the thin, membranous <b>hind wings</b> (metathorax) used in flight.',
  tail: 'Tail end: ten abdominal segments; the 10th carries a pair of jointed <b>anal cerci</b> (in both sexes).',
};
const MP_ORDER = ['Labrum', 'Mandible', 'Maxilla', 'Labium', 'Hypopharynx'];
const MP_FACT = {
  Labrum: 'Labrum (upper lip): a movable flap covering the mouth from the front.',
  Mandible: 'Mandible: hard, toothed jaw for biting and chewing food.',
  Maxilla: 'First maxilla: holds and pushes food into the mouth; its jointed maxillary palp is sensory.',
  Labium: 'Labium (lower lip): the fused second maxillae, with a pair of labial palps.',
  Hypopharynx: 'Hypopharynx: a tongue-like lobe in the middle; the salivary duct opens on it.',
};

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const R = rng((Date.now() & 0xffff) || 17);
  const sex = R() < 0.5 ? 'male' : 'female';
  const tray = dissectingTray(2.4, 1.6); tray.position.set(0, 0, 0.1); world.add(tray);
  const waxY = tray.userData.waxY;
  const roach = buildCockroach(sex);
  const spec = new THREE.Group(); world.add(spec); spec.add(roach.root);
  const jar = new THREE.Group(); jar.position.set(-1.9, 0, -0.2); world.add(jar);
  const jb = glassBeaker(0.36, 0.7, 0xffffff, 0); jar.add(jb.group);
  const lid = mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.05, 28), MAT.gloss(0x1f2937), [0, 0.74, 0]); jar.add(lid);
  const jt = tag('killing jar', { h: 0.07 }); jt.position.set(0, 0.95, 0); jar.add(jt);
  const cotton = mesh(new THREE.SphereGeometry(0.1, 10, 8), MAT.matte(0xf8fafc), [-1.25, 0.07, 0.45]); cotton.scale.y = 0.6; world.add(cotton);
  const chl = reagentBottle('Chloroform', 0xf1f5f9, 'CHCl₃', { amber: true }); chl.position.set(-1.05, 0, -0.55); world.add(chl);
  const slideM = makeSlide(); slideM.position.set(0.75, waxY + 0.005, 0.55); slideM.scale.setScalar(1.3); world.add(slideM);
  slideM.visible = false;
  spec.position.set(-1.9, 0.08, -0.2); spec.rotation.y = 0.6;
  const lens = createLens(ctx, { mag: 3.2, groundY: ctx.BENCH_Y + waxY + 0.02 });
  const tmp = new THREE.Vector3(); const loc = new THREE.Vector3();
  let quiz = null; let alive = 1; let flipped = false; let mpNext = 0; const removed = [];
  const seen = new Set(); let dwellOn = null; let dwell = 0;
  const TRAY = S([0.15, 1.15, 1.05], [0, 0.05, 0.12], 0.95, 0.75);
  const WIDE = S([-0.6, 1.9, 2.4], [-0.9, 0.2, 0.1], 3.2);

  const stepKill = {
    title: 'Anaesthetise the cockroach', text: 'The live cockroach is in the killing jar. Tap the <b>chloroform</b> bottle to soak the cotton, then tap the <b>jar</b> to drop the cotton in and close the lid.',
    tool: null, autoTool: 'hand', shot: WIDE,
    skip() { alive = 0; cotton.position.set(-1.9, 0.07, -0.05); },
    handler: { down() {
      if (input.pick([chl], true)) { this.soaked = true; sfx.play('drip'); cotton.material = MAT.matte(0xe0f2fe); ctx.say('Cotton soaked in a few drops of chloroform. Do not breathe the vapour.', 'info', 2400); return true; }
      if (!input.pick([jar], true)) return false;
      if (!this.soaked) { ctx.say('Soak the cotton with chloroform first.', 'hint', 1800); return true; }
      sfx.play('place'); const from = cotton.position.clone(); anim.add(0.7, (k) => { cotton.position.lerpVectors(from, new THREE.Vector3(-1.9, 0.07, -0.05), k); cotton.position.y += Math.sin(Math.PI * k) * 0.9; }, { done: () => { sfx.play('glass'); anim.add(3.0, (k) => { alive = 1 - k; }, { done: () => ctx.next('Still. It is anaesthetised and can now be handled.') }); } });
      return true;
    } },
  };
  const stepTray = {
    title: 'Lay it in the tray', text: 'Tap the jar to tip the cockroach gently into the dissecting tray, dorsal side up.', tool: null, autoTool: 'hand', shot: WIDE,
    skip() { place(true); },
    handler: { down() { if (!input.pick([jar, spec], true)) return false; place(false); return true; } },
  };
  function place(instant) {
    const to = new THREE.Vector3(0, waxY + 0.042, 0.05);
    if (instant) { spec.position.copy(to); spec.rotation.set(0, 0, 0); return; }
    const from = spec.position.clone(); const r0 = spec.rotation.y; sfx.play('pick');
    anim.add(1.1, (k) => { spec.position.lerpVectors(from, to, k); spec.position.y += Math.sin(Math.PI * k) * 0.8; spec.rotation.y = r0 * (1 - k); }, { ease: ease.inOut, done: () => { sfx.play('place'); ctx.next('In the tray. An adult is about 3.5–4 cm long.'); } });
  }
  function regionAt(p) {
    roach.body.worldToLocal(loc.copy(p));
    if (loc.z < -8.5 && Math.abs(loc.x) < 12) return 'head';
    if (loc.z < -1.5 && loc.z >= -8.5 && Math.abs(loc.x) < 7) return 'thorax';
    if (loc.z > 18 && Math.abs(loc.x) < 7) return 'tail';
    if (loc.z >= -1.5 && loc.z <= 18 && Math.abs(loc.x) < 8) return 'wings';
    return null;
  }
  const stepLens = {
    title: 'Examine it with the hand lens', text: 'Hold the <b>hand lens</b> over each region in turn and let it rest: the head, the thorax, the wings and the tail end.',
    tool: 'lens', shot: TRAY,
    aim(p, out) { return input.planePoint(ctx.BENCH_Y + waxY + 0.035, out) || false; },
    skip() { Object.keys(FACTS).forEach((k) => seen.add(k)); },
    update(dt) {
      if (!lens.active) { dwell = 0; return; }
      const r = regionAt(tools.tip); if (r && r === dwellOn) dwell += dt; else { dwellOn = r; dwell = 0; }
      if (r && dwell > 0.6 && !seen.has(r)) { seen.add(r); sfx.play('ok'); ctx.say(FACTS[r], 'good', 6000); ui.observe({ head: 'Head', thorax: 'Thorax', wings: 'Wings', tail: 'Tail end' }[r], 'examined'); ctx.progress(seen.size / 4); if (seen.size >= 4) anim.wait(2.5, () => ctx.next()); }
    },
    handler: { down() { return ui.tool === 'lens'; } },
  };
  const right = roach.wings[1];
  const stepWings = {
    title: 'Spread a wing', text: 'With the <b>forceps</b>, take hold of the right tegmen and drag it out sideways, then drag the thin hind wing beneath it to fan it open.',
    tool: 'forceps', shot: S([0.3, 1.05, 0.95], [0.12, 0.05, 0.05], 0.85, 0.7),
    skip() { roach.setWing(right, 1, 1); },
    handler: {
      down(p) {
        const h = input.pick([right.teg, right.hw], true); if (!h) return false; if (!ctx.requireTool('forceps')) return true;
        this.part = right.spread < 1 ? 'teg' : 'hind'; this.x = p.x; this.y = p.y; tools.press(1); tools.action(1); sfx.play('grab'); return true;
      },
      move(p) {
        if (!this.part) return; const d = Math.hypot(p.x - this.x, p.y - this.y) / 140;
        if (this.part === 'teg') roach.setWing(right, clamp(d), 0); else roach.setWing(right, 1, clamp(d));
      },
      up() {
        if (!this.part) return; tools.press(0); tools.action(0);
        if (this.part === 'teg' && right.spread >= 0.95) { roach.setWing(right, 1, 0); ctx.say('Tegmen spread: thick, leathery and opaque. Now open the hind wing.', 'good', 3000); }
        else if (this.part === 'teg') { const s0 = right.spread; anim.add(0.3, (k) => roach.setWing(right, s0 * (1 - k), 0)); }
        if (this.part === 'hind' && right.fan >= 0.95) { roach.setWing(right, 1, 1); ctx.next('The hind wing is thin, transparent and folds like a fan: the flight wing.'); }
        else if (this.part === 'hind') { const f0 = right.fan; anim.add(0.3, (k) => roach.setWing(right, 1, f0 * (1 - k))); }
        this.part = null;
      },
    },
  };
  const QUIZ = ['Antenna', 'Compound eye', 'Pronotum', 'Tegmen (forewing)', 'Hind wing', 'Femur', 'Tibia', 'Tarsus', 'Abdominal tergum', 'Cercus'];
  const stepQuiz = {
    title: 'Label the cockroach', text: 'Drag each name onto its numbered marker.', tool: null, autoTool: 'hand', hideBelt: true,
    shot: S([0.12, 1.25, 0.95], [0.08, 0.04, 0.0], 1.05, 0.95),
    enter() { quiz = createLabelQuiz(ctx, QUIZ.map((name) => ({ name, at: roach.anchors[name].clone(), object: roach.body })), { radius: 40, onPlace: (it, n, all) => ctx.progress(n / all), onDone: () => anim.wait(0.8, () => ctx.next('All labelled.')) }); },
    update() { if (quiz) quiz.update(); },
    exit() { if (quiz) { quiz.dispose(); quiz = null; } },
  };
  const stepSex = {
    title: 'Male or female?', text: 'Look closely at the tail end from the side (drag to turn the view): are there thin <b>anal styles</b> below the cerci? Do the wings reach beyond the abdomen?',
    tool: 'lens', shot: S([0.55, 0.32, 0.75], [0.0, 0.03, 0.3], 0.5),
    aim(p, out) { return input.planePoint(ctx.BENCH_Y + waxY + 0.03, out) || false; },
    enter() {
      ask(ctx, 'This cockroach is…', [{ label: 'Male', value: 'male' }, { label: 'Female', value: 'female' }], sex, {
        delay: 1.6, y: 0.08, wrong: sex === 'male' ? 'Look again: a pair of short anal styles projects from the 9th sternum, and the wings extend past the tip of the abdomen.' : 'Look again: there are no anal styles, the wings only just reach the end of the abdomen, and the broad abdomen ends in a boat-shaped 7th sternum (the brood pouch).',
        ok: sex === 'male' ? 'Male: anal styles present on the 9th sternum (besides the cerci), a narrower abdomen, and wings longer than the body.' : 'Female: no anal styles; the 7th sternum is boat-shaped and with the 8th and 9th forms the brood (genital) pouch; abdomen broader.',
      });
    },
    exit() { ui.clearChooser(); },
    skip() { ui.observe('Sex', sex); },
  };
  const stepFlip = {
    title: 'Turn it ventral side up', text: 'Tap the cockroach to turn it on its back.', tool: null, autoTool: 'hand', shot: TRAY,
    enter() { ui.observe('Sex', sex); },
    skip() { flip(true); },
    handler: { down() { if (!input.pick([spec], true)) return false; flip(false); return true; } },
  };
  function flip(instant) {
    flipped = true; const y0 = spec.position.y;
    if (instant) { spec.rotation.z = Math.PI; spec.position.y = waxY + 0.05; return; }
    sfx.play('pick'); anim.add(0.9, (k) => { spec.rotation.z = Math.PI * k; spec.position.y = y0 + Math.sin(Math.PI * k) * 0.15 + (0.05 - 0.042) * k; }, { ease: ease.inOut, done: () => { sfx.play('place'); slideM.visible = true; ctx.next('Ventral side up: the coxae of the legs, the sterna and the mouthparts are now visible.'); } });
  }
  const stepMouth = {
    title: 'Remove the mouthparts', text: 'With the <b>forceps</b>, pull off the mouthparts one at a time from the front backward and lay them on the slide: labrum, mandibles, maxillae, labium, hypopharynx.',
    tool: 'forceps', shot: S([0.05, 0.95, 0.55], [0.0, 0.05, -0.08], 0.55, 0.45),
    skip() { roach.mouthparts.forEach((m) => { if (!removed.includes(m)) layOut(m, true); }); },
    handler: { down() {
      const h = input.pick(roach.mouthparts.filter((m) => !removed.includes(m)), true); if (!h) return false;
      if (!ctx.requireTool('forceps')) return true;
      let o = h.object; while (o && !o.userData.mp) o = o.parent; if (!o) return false;
      const want = MP_ORDER[mpNext];
      if (o.userData.mp.name !== want) { ctx.mistake(`Not yet — the <b>${want.toLowerCase()}</b> lies in front of (covers) the ${o.userData.mp.name.toLowerCase()}. Work from the front backward.`, 2); return true; }
      layOut(o, false); return true;
    } },
  };
  function layOut(o, instant) {
    removed.push(o); const k = removed.length - 1; const nm = o.userData.mp.name;
    if (!roach.mouthparts.some((m) => !removed.includes(m) && m.userData.mp.name === nm)) mpNext += 1;
    const to = new THREE.Vector3(0.75 - 0.36 + k * 0.12, waxY + 0.03, 0.55); world.attach(o);
    if (instant) { o.position.copy(to); o.rotation.set(0, 0, 0); } else {
      sfx.play('tear'); tools.action(1); const from = o.position.clone();
      anim.add(0.8, (q) => { o.position.lerpVectors(from, to, q); o.position.y += Math.sin(Math.PI * q) * 0.12; }, { ease: ease.inOut, done: () => { tools.action(0); sfx.play('place'); o.rotation.set(0, 0, 0); } });
      ctx.say(MP_FACT[nm], 'good', 4200);
    }
    if (!roach.mouthparts.some((m) => !removed.includes(m) && m.userData.mp.name === nm)) { const t = tag(nm, { h: 0.035 }); t.position.set(to.x, to.y + 0.06, to.z + 0.06); world.add(t); }
    ctx.progress(removed.length / roach.mouthparts.length);
    if (!instant && removed.length === roach.mouthparts.length) anim.wait(1.2, () => ctx.next('Biting and chewing (mandibulate) mouthparts, laid out in order.'));
  }
  const stepInsect = {
    title: 'Why is it an insect?', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: TRAY,
    enter() {
      ask(ctx, 'How many pairs of spiracles does a cockroach have?', ['8', '10', '6', '2'].map((v) => ({ label: `${v} pairs`, value: v })), '10', {
        wrong: 'Count both kinds: two pairs on the thorax (meso- and metathorax) and one pair on each of the first eight abdominal segments.',
        then() { ask(ctx, 'Which characters make the cockroach an insect?', [{ label: 'Head, thorax, abdomen; 3 pairs of legs; 2 pairs of wings; 1 pair of antennae', value: 'ok' }, { label: '4 pairs of legs and no antennae', value: 'sp' }, { label: 'Many similar segments, each with a pair of legs', value: 'my' }], 'ok', { delay: 0.3, ok: 'Class Insecta: body in three regions, three pairs of jointed legs on the thorax, usually two pairs of wings, one pair of antennae, and tracheal breathing through 10 pairs of spiracles.', wrong: 'Count the legs and the body regions you have just seen.' }); },
      });
    },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepKill, stepTray, stepLens, stepWings, stepQuiz, stepSex, stepFlip, stepMouth, stepInsect];
  ctx.debug = { roach, spec, sex };
  void fx; void tmp;
  return {
    tools: ['hand', 'lens', 'forceps'],
    steps,
    update(dt, t) {
      lens.update(); if (quiz) quiz.update();
      if (alive > 0) {
        roach.antennae.forEach((a, i) => { a.rotation.y = Math.sin(t * 3 + i) * 0.08 * alive; });
        roach.legParts.forEach((l, i) => { l.rotation.x += Math.sin(t * 14 + i) * 0.004 * alive; });
        spec.position.x = -1.9 + Math.sin(t * 0.9) * 0.12 * alive; spec.rotation.y = 0.6 + Math.sin(t * 0.6) * 0.8 * alive;
      }
    },
    result() {
      return { title: 'External morphology of the cockroach', rows: [['Sex', `${sex} (${sex === 'male' ? 'anal styles present' : 'no anal styles; brood pouch'})`], ['Body regions', 'head, thorax (3 segments), abdomen (10 segments)'], ['Appendages', '1 pair antennae, 3 pairs legs, 2 pairs wings, 1 pair cerci'], ['Mouthparts', 'biting and chewing: labrum, 2 mandibles, 2 maxillae, labium, hypopharynx']], conclusion: 'Periplaneta is a typical insect: a hypognathous head with compound eyes and filiform antennae, a three-segmented thorax carrying three pairs of jointed legs and two pairs of wings (leathery tegmina over membranous hind wings), and a ten-segmented abdomen with anal cerci. The sexes differ at the tail end: anal styles in males, a brood pouch in females.' };
    },
    dispose() { lens.dispose(); if (quiz) quiz.dispose(); ui.clearChooser(); },
  };
}
