// Collecting a plant and preparing a herbarium sheet. Choose a representative twig (with leaves
// and a flower) on the hibiscus bush and cut it with scissors; lay it between blotting papers in a
// plant press, arranged flat with one leaf turned to show its underside; dry it for a week,
// changing the damp blotters on the first days (skip it and mould sets in); paint it with
// mercuric chloride against insects; mount it on a standard sheet with gummed strips; and fill in
// the label. Moisture and dryness follow the days and the blotter changes.
import { THREE } from '../../engine.js';
import { leaf, stem, flower } from '../specimens/plants.js';
import { timelapse, ask, tag, glassBeaker } from '../bench.js';
import { mesh, MAT, wet, canvasTexture, clamp, ease, rng } from '../kit.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const SHEET = { w: 2.9, d: 4.2 };

function twig(withFlower, seed) {
  const R = rng(seed); const g = new THREE.Group(); const leaves = [];
  g.add(stem([[0, 0, 0], [0.04, 0, -0.6], [-0.02, 0, -1.3], [0.03, 0, -1.9]], 0.022, 0x5b4a2a, 0.01));
  for (let i = 0; i < 7; i++) {
    const s = i % 2 ? 1 : -1; const z = -0.25 - i * 0.24; const l = leaf({ len: 0.55 + R() * 0.12, wid: 0.32, upper: '#1f6b2a', lower: '#7fb069', arch: 0.06 });
    const holder = new THREE.Group(); holder.position.set(0.01, 0.0, z); holder.rotation.y = s * (Math.PI / 2 + 0.5); g.add(holder); holder.add(l);
    l.rotation.x = -0.25 - R() * 0.3; l.rotation.z = s * 0.25; leaves.push({ holder, l, s, flipped: false });
  }
  if (withFlower) {
    const f = flower(0xdc2626, 0.42); f.position.set(0.05, 0.08, -2.05); f.rotation.x = -1.1; g.add(f);
    const col = mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.5, 6), wet(0xfacc15), [0.05, 0.3, -2.2]); col.rotation.x = -0.9; g.add(col); g.userData.flower = f;
    const bud = mesh(new THREE.SphereGeometry(0.06, 10, 8), wet(0x4d7c0f), [-0.12, 0.02, -1.7]); bud.scale.set(1, 1, 1.8); g.add(bud);
  }
  g.userData.leaves = leaves;
  return g;
}
function labelTex(f) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 300; const g = c.getContext('2d');
  g.fillStyle = '#fffef6'; g.fillRect(0, 0, 512, 300); g.strokeStyle = '#1e293b'; g.lineWidth = 3; g.strokeRect(4, 4, 504, 292);
  g.fillStyle = '#0f172a'; g.font = '700 26px Georgia, serif'; g.textAlign = 'center'; g.fillText('HERBARIUM — School Biology Lab', 256, 38);
  g.textAlign = 'left'; g.font = '20px Georgia, serif';
  [['Scientific name', f.sci], ['Family', f.fam], ['Local name', f.local], ['Habit', f.habit], ['Locality', f.loc], ['Date', f.date], ['Collector', f.by]].forEach(([k, v], i) => { g.fillStyle = '#475569'; g.fillText(`${k}:`, 18, 78 + i * 31); g.fillStyle = '#0f172a'; g.font = v ? 'italic 21px Georgia, serif' : '20px Georgia, serif'; g.fillText(v || '……………………', 190, 78 + i * 31); g.font = '20px Georgia, serif'; });
  const t = new THREE.CanvasTexture(c); if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace; return t;
}

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const hud = createHud(ctx); const chip = hud.chip('ho-chip-read');
  // the hibiscus bush at the back of the bench, with two candidate twigs
  const bush = new THREE.Group(); bush.position.set(-1.8, 0, -1.0); world.add(bush);
  bush.add(mesh(new THREE.CylinderGeometry(0.5, 0.4, 0.6, 20), MAT.matte(0xb4532a), [0, 0.3, 0]));
  bush.add(stem([[0, 0.55, 0], [0.05, 1.2, 0], [0, 1.9, 0.05]], 0.05, 0x5b4a2a, 0.03));
  const R = rng(5); for (let i = 0; i < 16; i++) { const l = leaf({ len: 0.5, wid: 0.3, upper: '#1f6b2a', lower: '#7fb069' }); l.position.set(0, 0.9 + R() * 1.0, 0); l.rotation.set(-0.5 - R() * 0.4, R() * 6.28, 0, 'YXZ'); bush.add(l); }
  const cand = [twig(true, 3), twig(false, 4)];
  cand.forEach((t, i) => { t.position.set(i ? -0.15 : 0.15, i ? 1.3 : 1.6, 0.05); t.rotation.set(0.9, i ? -0.6 : 0.5, 0); t.scale.setScalar(0.85); bush.add(t); });
  // plant press, blotting papers, sheet, poison and strips
  const press = new THREE.Group(); press.position.set(0.6, 0, 0.3); world.add(press);
  const lattice = (y) => { const g = new THREE.Group(); g.position.y = y; const wd = MAT.gloss(0x9a6a3c); for (let k = 0; k < 6; k++) { g.add(mesh(new THREE.BoxGeometry(3.2, 0.04, 0.12), wd, [0, 0, -2.1 + k * 0.84])); g.add(mesh(new THREE.BoxGeometry(0.12, 0.04, 4.4), wd, [-1.5 + k * 0.6, 0.04, 0])); } return g; };
  const bottom = lattice(0.02); press.add(bottom); const lid = lattice(0); lid.position.set(-3.4, 0.02, 0); press.add(lid);
  const blot = [0, 1].map(() => { const m = mesh(new THREE.BoxGeometry(2.9, 0.02, 4.1), MAT.matte(0xf5efe0), [0, 0, 0]); m.visible = false; press.add(m); return m; });
  const stack = new THREE.Group(); stack.position.set(2.5, 0, 1.6); world.add(stack); for (let k = 0; k < 6; k++) stack.add(mesh(new THREE.BoxGeometry(0.9, 0.012, 0.6), MAT.matte(0xf5efe0), [0, 0.006 + k * 0.012, 0]));
  const stT = tag('blotting paper', { h: 0.07 }); stT.position.set(0, 0.25, 0); stack.add(stT);
  const hgc = glassBeaker(0.18, 0.3, 0xe2e8f0, 0.6); hgc.group.position.set(2.5, 0, 0.7); world.add(hgc.group); const hT = tag('0.1% HgCl₂ in alcohol', { h: 0.06 }); hT.position.set(2.5, 0.45, 0.7); world.add(hT);
  const hsheet = new THREE.Group(); hsheet.position.set(0.6, 0, 0.3); hsheet.visible = false; world.add(hsheet);
  hsheet.add(mesh(new THREE.BoxGeometry(SHEET.w, 0.01, SHEET.d), MAT.paper(), [0, 0.005, 0]));
  const fields = { sci: '', fam: '', local: '', habit: '', loc: 'School garden, Kathmandu', date: new Date().toLocaleDateString('en-GB'), by: 'Student' };
  let ltex = labelTex(fields); const label = mesh(new THREE.PlaneGeometry(1.25, 0.73), new THREE.MeshBasicMaterial({ map: ltex }), [0.75, 0.012, 1.68]); label.rotation.x = -Math.PI / 2; hsheet.add(label);
  let spec = null; let leavesFlat = false; let moist = 78; let mould = 0; let lastChange = 0; let day = 0; let clock = null; const strips = [];
  const SH = S([0.6, 4.2, 3.2], [0.6, 0.0, 0.5], 4.6);
  const BUSH = S([-1.2, 2.7, 2.6], [-1.75, 1.5, -0.9], 2.3, 2.9);

  const stepChoose = {
    title: 'Collect a representative twig', text: 'A good herbarium specimen shows leaves <b>and</b> flowers (or fruits). With the <b>scissors</b>, snip the right twig from the hibiscus bush: drag across its stalk.', tool: 'scissors', shot: BUSH,
    skip() { take(cand[0], true); },
    handler: {
      down(p) { if (!ctx.requireTool('scissors')) return !!input.pick(cand, true); this.last = [p.x, p.y]; tools.action(0.3); return true; },
      move(p) {
        if (!this.last) return;
        cand.forEach((t, i) => { if (spec) return; const a = new THREE.Vector3(0, 0, 0); const b = new THREE.Vector3(0, 0, -0.35); t.localToWorld(a); t.localToWorld(b); input.project(a, a, ctx.stage.clientWidth, ctx.stage.clientHeight); input.project(b, b, ctx.stage.clientWidth, ctx.stage.clientHeight);
          const d = (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x); const d0 = (b.x - a.x) * (this.last[1] - a.y) - (b.y - a.y) * (this.last[0] - a.x); const near = Math.hypot(p.x - (a.x + b.x) / 2, p.y - (a.y + b.y) / 2) < 50;
          if (near && d * d0 < 0) { if (i === 1) { ctx.mistake('That twig has leaves only. A specimen must show the flowers too, or the plant cannot be identified from the sheet.', 3); this.last = null; return; } tools.action(1); sfx.play('snip'); take(t, false); } });
        if (this.last) this.last = [p.x, p.y];
      },
      up() { this.last = null; tools.action(0); },
    },
  };
  function take(t, instant) {
    spec = t; world.attach(t); ui.observe('Specimen', 'Hibiscus twig: leaves, flower, bud'); ui.observe('Habit (field note)', 'shrub, about 2 m');
    const to = new THREE.Vector3(2.4, 0.06, -0.6); const q1 = new THREE.Quaternion();
    if (instant) { t.position.copy(to); t.quaternion.copy(q1); t.scale.setScalar(1); return; }
    const from = t.position.clone(); const q0 = t.quaternion.clone(); const s0 = t.scale.x;
    anim.add(1.2, (k) => { t.position.lerpVectors(from, to, k); t.position.y += Math.sin(Math.PI * k) * 0.6; t.quaternion.slerpQuaternions(q0, q1, k); t.scale.setScalar(s0 + (1 - s0) * k); }, { ease: ease.inOut, done: () => ctx.next('Collected, with a field note of locality and habit. Keep it fresh in a polythene bag.') });
  }
  const stepLay = {
    title: 'Lay it in the plant press', text: 'Tap the stack of <b>blotting paper</b> to lay a sheet on the press, then tap the twig to lay it on the paper.', tool: null, autoTool: 'hand', shot: SH,
    skip() { blot[0].visible = true; blot[0].position.y = 0.06; layOn(true); },
    handler: { down() {
      if (!blot[0].visible) { if (!input.pick([stack], true)) return false; blot[0].visible = true; blot[0].position.y = 0.06; sfx.play('paper'); return true; }
      if (!input.pick([spec], true)) return false; layOn(false); return true;
    } },
  };
  function layOn(instant) {
    const to = new THREE.Vector3(0.6, 0.11, 1.15); const q1 = new THREE.Quaternion();
    if (instant) { spec.position.copy(to); spec.quaternion.copy(q1); return; }
    const from = spec.position.clone(); sfx.play('pick'); anim.add(0.9, (k) => { spec.position.lerpVectors(from, to, k); spec.position.y += Math.sin(Math.PI * k) * 0.5; }, { done: () => { sfx.play('place'); ctx.next('On the blotter.'); } });
  }
  const stepArrange = {
    title: 'Arrange it flat', text: 'Tap each leaf to press it flat without folds. Turn <b>one</b> leaf over (tap it twice) so the underside will show on the sheet.', tool: null, autoTool: 'hand', shot: SH,
    skip() { flatten(true); spec.userData.leaves[2].flipped = true; spec.userData.leaves[2].l.rotation.z = Math.PI; },
    handler: { down() {
      const L = spec.userData.leaves; const h = input.pick(L.map((q) => q.l), true); if (!h) return false;
      const q = L.find((x) => { let o = h.object; while (o) { if (o === x.l) return true; o = o.parent; } return false; }); if (!q) return false;
      if (!q.flat) { q.flat = true; sfx.play('place'); anim.add(0.35, (k) => { q.l.rotation.x *= 1 - k; q.l.rotation.z *= 1 - k; }); }
      else if (!q.flipped && !L.some((x) => x.flipped)) { q.flipped = true; sfx.play('tear'); anim.add(0.5, (k) => { q.l.rotation.z = Math.PI * k; }); ctx.say('Underside up: its venation and hairs will show.', 'good', 2000); }
      const done = L.every((x) => x.flat) && L.some((x) => x.flipped); ctx.progress(L.filter((x) => x.flat).length / L.length);
      if (done && !this.fin) { this.fin = true; flatten(false); anim.wait(0.6, () => ctx.next('Flat, no overlaps, one leaf showing its lower surface; the flower opened out.')); }
      return true;
    } },
  };
  function flatten(instant) { leavesFlat = true; spec.userData.leaves.forEach((q) => { q.flat = true; if (instant) { q.l.rotation.x = 0; q.l.rotation.z = q.flipped ? Math.PI : 0; } }); const f = spec.userData.flower; if (f) { if (instant) f.rotation.x = -Math.PI / 2; else anim.add(0.5, (k) => { f.rotation.x = -1.1 - (Math.PI / 2 - 1.1) * k; }); } spec.children.forEach((c) => { if (c.isMesh && c.geometry.type === 'CylinderGeometry') c.visible = false; }); }
  const stepClose = {
    title: 'Close and tighten the press', text: 'Tap the blotting paper stack to cover the specimen, then tap the press to put on the top frame and tighten the straps.', tool: null, autoTool: 'hand', shot: SH,
    skip() { blot[1].visible = true; blot[1].position.y = 0.2; lid.position.set(0, 0.24, 0); spec.scale.y = 0.15; },
    handler: { down() {
      if (!blot[1].visible) { if (!input.pick([stack], true)) return false; blot[1].visible = true; blot[1].position.y = 0.2; sfx.play('paper'); return true; }
      if (!input.pick([press, spec], true)) return false; sfx.play('click'); const from = lid.position.clone(); anim.add(1.0, (k) => { lid.position.lerpVectors(from, new THREE.Vector3(0, 0.24, 0), k); lid.position.y += Math.sin(Math.PI * k) * 0.8; }, { done: () => { anim.add(0.5, (k) => { spec.scale.y = 1 - 0.85 * k; }); sfx.play('latch'); ctx.next('Pressed firmly between the frames.'); } }); return true;
    } },
  };
  const stepDry = {
    title: 'Dry it for a week', text: 'Run the clock a day at a time. The blotters soak up the sap: press <b>Change blotters</b> every day for the first three days, then let it dry until brittle.', tool: null, autoTool: 'hand', hideBelt: true, shot: SH,
    enter() {
      clock = timelapse(ctx, { step: 1, unit: 'day', onTick: (d, done) => {
        if (!done) return; day = d; const wet2 = d - lastChange;
        moist = Math.max(8, moist * (wet2 > 1 && d <= 4 ? 0.82 : 0.62)); if (d <= 4 && wet2 === 2) { mould = Math.min(1, mould + 0.5); ctx.mistake('Damp blotters left too long: grey mould spots are appearing on the leaves. Change them daily at first.', 3); }
        ui.observe(`Day ${d}`, `${Math.round(moist)} % moisture${mould ? ', mould!' : ''}`); paint();
        if (d >= 7 && !this.fin) { this.fin = true; clock.show(false); hud.actions([]); ctx.next(moist < 15 ? 'Dry and brittle, the colour largely kept.' : 'Dry enough to mount.'); }
      } });
      hud.actions([{ id: 'c', label: 'Change blotters', onClick() { if (day === lastChange) { ctx.say('Already changed today.', 'hint', 1000); return; } lastChange = day; moist = Math.max(8, moist * 0.85); sfx.play('paper'); ui.observe(`Day ${day}`, `blotters changed · ${Math.round(moist)} %`); paint(); } }]);
    },
    skip() { moist = 10; day = 7; paint(); },
    exit() { if (clock) clock.remove(); clock = null; hud.actions([]); },
  };
  function paint() { const k = clamp((78 - moist) / 68); spec.traverse((o) => { if (o.isMesh && o.material && o.material.color) { if (!o.userData.c0) { o.material = o.material.clone(); o.userData.c0 = o.material.color.clone(); } o.material.color.copy(o.userData.c0).lerp(new THREE.Color(mould ? 0x6b7258 : 0x4a5a2a), k * 0.55); } }); }
  let painted = 0;
  const stepPoison = {
    title: 'Poison it against insects', text: 'Open the press. With the <b>brush</b> dipped in 0.1% HgCl₂ in alcohol, paint the whole dried specimen (drag over it). Handle mercuric chloride with care — it is toxic.', tool: 'brush', shot: SH,
    enter() { lid.position.set(-3.4, 0.02, 0); blot[1].visible = false; },
    skip() { painted = 1; },
    handler: {
      down(p) { if (input.pick([hgc.group], true)) { if (!ctx.requireTool('brush')) return true; this.loaded = true; sfx.play('drop'); return true; } if (!input.pick([spec], true)) return false; if (!ctx.requireTool('brush')) return true; if (!this.loaded) { ctx.say('Dip the brush in the poison first.', 'hint', 1400); return true; } this.last = [p.x, p.y]; tools.press(1); return true; },
      move(p) { if (!this.last) return; painted = clamp(painted + Math.hypot(p.x - this.last[0], p.y - this.last[1]) / 1100); this.last = [p.x, p.y]; ctx.progress(painted); if (painted >= 1 && !this.fin) { this.fin = true; this.last = null; tools.press(0); ctx.next('Poisoned: insects and fungi will not attack it.'); } },
      up() { this.last = null; tools.press(0); },
    },
  };
  const STRIP_AT = [[0.27, 1.15], [0.29, 0.6], [0.24, 0.0], [0.28, -0.45]];
  let marks = [];
  const stepMount = {
    title: 'Mount it on a herbarium sheet', text: 'The specimen is laid on a standard sheet (42 × 29 cm). With the <b>forceps</b>, put a gummed strip across the stem at each marked point.', tool: 'forceps', shot: SH,
    enter() {
      press.visible = false; hsheet.visible = true; spec.position.set(0.25, 0.03, 1.3); spec.scale.y = 0.15;
      marks = STRIP_AT.map(([x, z]) => fx.mark(world.localToWorld(new THREE.Vector3(x, 0.05, z)), 0.07, 0xfacc15));
    },
    exit() { marks.forEach((m) => fx.unmark(m)); marks = []; },
    skip() { STRIP_AT.forEach(([x, z]) => addStrip(x, z)); },
    handler: { down(p) {
      if (!ctx.requireTool('forceps')) return !!input.pick([hsheet, spec], true);
      const m = marks.find((q) => { const v = q.position.clone(); input.project(v, v, ctx.stage.clientWidth, ctx.stage.clientHeight); return Math.hypot(v.x - p.x, v.y - p.y) < (p.touch ? 40 : 28); }); if (!m) return false;
      const l = world.worldToLocal(m.position.clone()); addStrip(l.x, l.z); fx.unmark(m); marks.splice(marks.indexOf(m), 1); sfx.play('place'); ctx.progress(strips.length / STRIP_AT.length);
      if (!marks.length) ctx.next('Fixed with strips across the stem; the flower is held with a drop of glue.'); return true;
    } },
  };
  function addStrip(x, z) { const s2 = mesh(new THREE.BoxGeometry(0.42, 0.006, 0.07), MAT.matte(0xf5f0dc), [x, 0.07, z]); s2.rotation.y = 0.15; world.add(s2); strips.push(s2); }
  const stepLabel = {
    title: 'Fill in the label', text: 'Complete the label in the lower right corner of the sheet.', tool: null, autoTool: 'hand', hideBelt: true, shot: S([1.35, 2.3, 3.6], [1.35, 0.0, 1.95], 1.8),
    enter() {
      const upd = () => { ltex.dispose(); ltex = labelTex(fields); label.material.map = ltex; label.material.needsUpdate = true; };
      ask(ctx, 'Scientific name', ['Hibiscus rosa-sinensis L.', 'Rosa indica L.', 'Hibiscus Rosa-Sinensis', 'Datura stramonium L.'], 'Hibiscus rosa-sinensis L.', { y: 0.06, wrong: 'Binomial: genus with a capital letter, species all in small letters, written in italics, with the author.', then() { fields.sci = 'Hibiscus rosa-sinensis L.'; upd();
        ask(ctx, 'Family', ['Malvaceae', 'Rosaceae', 'Solanaceae', 'Fabaceae'], 'Malvaceae', { delay: 0.2, y: 0.06, wrong: 'Hibiscus has monadelphous stamens fused into a column round the style: the mallow family.', then() { fields.fam = 'Malvaceae'; upd();
          ask(ctx, 'Habit', ['Shrub', 'Herb', 'Tree', 'Climber'], 'Shrub', { delay: 0.2, y: 0.06, wrong: 'Check your field note: a woody plant about 2 m tall with several stems.', then() { fields.habit = 'Shrub'; fields.local = 'Barhamase phool'; upd(); ui.observe('Label', 'complete'); ctx.next('Label complete: name, family, local name, habit, locality, date and collector.'); } }); } }); } });
    },
    exit() { ui.clearChooser(); },
  };
  const stepStore = {
    title: 'Store the sheet', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: SH,
    enter() { ask(ctx, 'How are herbarium sheets kept safe for years?', [{ label: 'In a dry, closed cabinet with naphthalene balls, by family', value: 'ok' }, { label: 'Rolled up in a damp cupboard', value: 'd' }, { label: 'Pinned on a sunny wall', value: 's' }], 'ok', { ok: 'In air-tight steel cabinets with naphthalene or other repellents, arranged by a system of classification (e.g. Bentham and Hooker) — a permanent record for identification and research.', wrong: 'Damp brings mould; sunlight bleaches the specimen.' }); },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepChoose, stepLay, stepArrange, stepClose, stepDry, stepPoison, stepMount, stepLabel, stepStore];
  ctx.debug = { cand, get spec() { return spec; } };
  void chip; void leavesFlat;
  return {
    tools: ['hand', 'scissors', 'brush', 'forceps'],
    steps,
    update() { hud.update(); },
    result() { return { title: 'Herbarium specimen', rows: [['Specimen', 'Hibiscus rosa-sinensis L. (Malvaceae)'], ['Final moisture', `${Math.round(moist)} %`], ['Mould', mould ? 'some (blotters not changed in time)' : 'none'], ['Label', 'complete']], conclusion: 'A herbarium specimen is a pressed, dried, poisoned plant mounted on a standard sheet with a full label. A representative twig with flowers is pressed flat between blotters, which are changed often so it dries fast without mould; it is then poisoned, fixed with strips and labelled with its scientific name, family, locality, habit, date and collector.' }; },
    dispose() { hud.dispose(); ui.clearChooser(); ltex.dispose(); },
  };
}
