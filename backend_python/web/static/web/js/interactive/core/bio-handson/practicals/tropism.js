// Two growth-hormone setups run over days. Phototropism: cap the tips of one pot of maize seedlings
// with foil, stand it and an uncapped pot in a box lit through a slit, keep a third pot under even
// light, run the days and measure the curvature of the shoots with a protractor (only the uncapped
// shoots in one-sided light bend, toward it: auxin moves to the shaded side). Apical dominance:
// cut the apical bud off two plants, smear one cut with plain lanolin and the other with lanolin
// containing auxin (IAA), and follow the lateral buds for two weeks with a rule.
import { THREE } from '../../engine.js';
import { clayPot, timelapse, ask, sheet, table, tag, flyTo } from '../bench.js';
import { seedling, leaf, stem, bud } from '../specimens/plants.js';
import { mesh, MAT, clamp, rng, canvasTexture, wet, smooth } from '../kit.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });

export function create(ctx) { return ctx.config.slug.startsWith('apical') ? apical(ctx) : photo(ctx); }

function pot(ctx, x, z, label) {
  const g = new THREE.Group(); g.position.set(x, 0, z); ctx.world.add(g);
  g.add(clayPot(0.32, 0.42));
  const t = tag(label, { h: 0.08 }); t.position.set(0, -0.0, 0.45); t.position.y = 0.55; g.add(t);
  return g;
}

function photo(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const R = rng((Date.now() & 0xffff) || 5);
  const pots = ['A', 'B', 'C'].map((l, i) => {
    const g = pot(ctx, -1.95 + i * 0.78, 0.6, l === 'A' ? 'A: one-sided light' : l === 'B' ? 'B: even light' : 'C: tips capped');
    const seeds = [];
    for (let k = 0; k < 4; k++) { const s = seedling(0.62 + R() * 0.12, { monocot: true }); s.group.position.set((k % 2 - 0.5) * 0.24 + (R() - 0.5) * 0.05, 0.38, (Math.floor(k / 2) - 0.5) * 0.22); g.add(s.group); seeds.push(s); }
    return { g, seeds, label: l, inBox: false, angle: 0 };
  });
  // the dark box: open at the front for the camera (a black curtain in a real lab), slit on the right
  const box = new THREE.Group(); box.position.set(0.95, 0, -0.35); world.add(box);
  const card = new THREE.MeshStandardMaterial({ color: 0x3b2f2a, roughness: 0.95, side: THREE.DoubleSide });
  const W = 2.0; const H = 1.7; const D = 1.1;
  box.add(mesh(new THREE.BoxGeometry(W, 0.03, D), card, [0, H, 0]));
  box.add(mesh(new THREE.BoxGeometry(W, H, 0.03), card, [0, H / 2, -D / 2]));
  box.add(mesh(new THREE.BoxGeometry(0.03, H, D), card, [-W / 2, H / 2, 0]));
  const right = new THREE.Group(); right.position.set(W / 2, 0, 0); box.add(right);
  right.add(mesh(new THREE.BoxGeometry(0.03, 0.85, D), card, [0, 0.425, 0])); right.add(mesh(new THREE.BoxGeometry(0.03, H - 1.05, D), card, [0, 1.05 + (H - 1.05) / 2, 0]));
  const slitGlow = mesh(new THREE.PlaneGeometry(0.2, D * 0.9), new THREE.MeshBasicMaterial({ color: 0xfff3c4, transparent: true, opacity: 0, side: THREE.DoubleSide }), [0.0, 0.95, 0]); slitGlow.rotation.y = Math.PI / 2; slitGlow.rotation.x = Math.PI / 2; right.add(slitGlow);
  const boxTag = tag('box with a slit', { h: 0.09 }); boxTag.position.set(0, H + 0.15, 0); box.add(boxTag);
  const lamp = new THREE.Group(); lamp.position.set(2.75, 0, -0.35); world.add(lamp);
  lamp.add(mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.06, 24), MAT.gloss(0x1f2937), [0, 0.03, 0]));
  lamp.add(mesh(new THREE.CylinderGeometry(0.025, 0.025, 1.0, 10), MAT.steel(), [0, 0.53, 0]));
  const shade = mesh(new THREE.ConeGeometry(0.28, 0.35, 24, 1, true), MAT.gloss(0x0f766e), [-0.1, 1.05, 0]); shade.rotation.z = Math.PI / 2 + 0.15; lamp.add(shade);
  const bulb = mesh(new THREE.SphereGeometry(0.1, 16, 12), new THREE.MeshBasicMaterial({ color: 0x9ca3af }), [-0.2, 1.03, 0]); lamp.add(bulb);
  const light = new THREE.PointLight(0xfff1c1, 0, 6, 1.5); light.position.set(-0.4, 1.0, 0); lamp.add(light);
  const tmp = new THREE.Vector3();
  const BENCH = S([0.4, 2.6, 3.6], [0.4, 0.75, 0.1], 4.6);
  const BOX = S([0.9, 2.1, 2.6], [1.0, 0.8, -0.3], 2.8);
  const MEASURE = S([-0.45, 1.15, 1.75], [-0.45, 0.95, 0.6], 1.1);
  let day = 0; let lampOn = false; let measuring = null; let clock = null; let sh = null;
  const results = {};

  const stepCap = {
    title: 'Cap the tips of pot C', text: 'With the <b>forceps</b>, put a tiny foil cap on the tip of each seedling in pot <b>C</b> (tap each tip). The tip is where light is sensed.',
    tool: 'forceps', shot: S([-0.6, 1.9, 2.5], [-0.6, 0.75, 0.55], 2.4),
    skip() { pots[2].seeds.forEach((s) => { s.cap.visible = true; }); },
    handler: { down() {
      const h = input.pick(pots.flatMap((p) => p.seeds.map((s) => s.group)), true); if (!h) return false;
      const p = pots.find((q) => q.seeds.some((s) => h.object.parent && (s.group === h.object.parent || s.group === h.object.parent.parent || s.top === h.object.parent)));
      if (!p) return false; if (!ctx.requireTool('forceps')) return true;
      if (p.label !== 'C') { ctx.mistake(`Only pot C is capped; pot ${p.label} is the comparison.`, 2); return true; }
      const s = p.seeds.find((q) => !q.cap.visible); if (!s) return true;
      s.cap.visible = true; sfx.play('pick'); ctx.progress(p.seeds.filter((q) => q.cap.visible).length / 4);
      if (p.seeds.every((q) => q.cap.visible)) ctx.next('All four tips covered with foil.'); return true;
    } },
  };
  const stepBox = {
    title: 'Put pots A and C in the box', text: 'Tap pots <b>A</b> and <b>C</b> to stand them inside the box. Pot <b>B</b> stays on the bench in even light.', tool: null, autoTool: 'hand', shot: BENCH,
    skip() { place(pots[0], true); place(pots[2], true); },
    handler: { down() {
      const p = pots.find((q) => input.pick([q.g], true)); if (!p) return false;
      if (p.label === 'B') { ctx.mistake('Pot B is the control in even light — leave it out of the box.', 2); return true; }
      if (p.inBox) return true; place(p, false); if (pots[0].inBox && pots[2].inBox) anim.wait(0.8, () => ctx.next('A and C in the box.')); return true;
    } },
  };
  function place(p, instant) { p.inBox = true; const to = new THREE.Vector3(p.label === 'A' ? 0.6 : 1.3, 0, -0.3); if (instant) p.g.position.copy(to); else { sfx.play('pick'); flyTo(ctx, p.g, to, { dur: 0.9, lift: 0.5, done: () => sfx.play('place') }); } }
  const stepTurn = {
    title: 'Turn the slit toward the lamp', text: 'Drag sideways on the <b>box</b> to turn it until the slit in its side faces the lamp.', tool: null, autoTool: 'hand', shot: BENCH,
    enter() { box.rotation.y = 2.4; pots.forEach((p) => { if (p.inBox) { tmp.copy(p.g.position).sub(box.position).applyAxisAngle(new THREE.Vector3(0, 1, 0), 2.4); p.home = p.g.position.clone().sub(box.position); p.g.position.copy(box.position).add(tmp); } }); },
    skip() { setBoxRot(0); },
    handler: {
      down(p) { if (!input.pick([box], true)) return false; this.x = p.x; this.r = box.rotation.y; return true; },
      move(p) { if (this.x === undefined) return; setBoxRot(this.r + (p.x - this.x) * 0.012); },
      up() { this.x = undefined; const a = Math.atan2(Math.sin(box.rotation.y), Math.cos(box.rotation.y)); if (Math.abs(a) < 0.2) { setBoxRot(0); sfx.play('place'); ctx.next('The slit faces the lamp squarely.'); } else ctx.say(`The slit is ${Math.round(Math.abs(a) * 57)}° off the lamp.`, 'hint', 1600); },
    },
  };
  function setBoxRot(a) { box.rotation.y = a; pots.forEach((p) => { if (p.inBox && p.home) { tmp.copy(p.home).applyAxisAngle(new THREE.Vector3(0, 1, 0), a); p.g.position.copy(box.position).add(tmp); p.g.rotation.y = a; } }); }
  const stepLamp = {
    title: 'Switch on the lamp', text: 'Tap the lamp. Light now enters the box only through the slit.', tool: null, autoTool: 'hand', shot: BOX,
    skip() { switchLamp(); },
    handler: { down() { if (!input.pick([lamp], true)) return false; switchLamp(); sfx.play('switch'); ctx.next('Lamp on.'); return true; } },
  };
  function switchLamp() { lampOn = true; light.intensity = 3; bulb.material.color.setHex(0xfff7d6); slitGlow.material.opacity = 0.55; }
  // bending: the tip curves toward the light at a rate that saturates; capped or evenly lit shoots grow straight
  function grow(d) {
    pots.forEach((p) => p.seeds.forEach((s, k) => {
      const target = p.label === 'A' && lampOn ? (0.95 + (k - 1.5) * 0.06) : 0;
      const ang = target * (1 - Math.exp(-d / 1.6)) + (p.label === 'A' ? 0.02 * Math.sin(k) : 0);
      s.setBend(p.label === 'A' ? ang : 0); s.group.scale.setScalar(1 + d * 0.11); s.angle = ang;
    }));
  }
  const stepDays = {
    title: 'Leave them for four days', text: 'Run the clock a day at a time and watch the shoots.', tool: null, autoTool: 'hand', hideBelt: true, shot: BOX,
    enter() { clock = timelapse(ctx, { step: 1, unit: 'day', dur: 1.6, onTick: (d, done) => { day = d; grow(d); if (done) { ui.observe(`Day ${Math.round(d)}`, `A ${Math.round(meanAngle(0))}° · B 0° · C 0°`); if (d >= 4 && !this.done) { this.done = true; clock.show(false); ctx.next('Only pot A has bent — toward the slit.'); } } } }); },
    skip() { day = 4; grow(4); },
    exit() { if (clock) clock.remove(); clock = null; },
  };
  const meanAngle = (i) => pots[i].seeds.reduce((a, s) => a + (s.angle || 0), 0) / pots[i].seeds.length * 57.3;
  // protractor: an arc behind the chosen seedling, its arm follows the pointer around the bend's base
  const prot = new THREE.Group(); prot.visible = false; world.add(prot);
  const protTex = canvasTexture('protractor', 512, 512, (g, w, h) => {
    g.fillStyle = 'rgba(255,255,255,0.82)'; g.beginPath(); g.moveTo(w / 2, h); g.arc(w / 2, h, w / 2 - 4, Math.PI, 2 * Math.PI); g.closePath(); g.fill();
    g.strokeStyle = '#1e3a8a'; g.fillStyle = '#1e3a8a'; g.font = '600 20px system-ui'; g.textAlign = 'center';
    for (let a = 0; a <= 90; a++) { const r0 = w / 2 - 6; const r1 = r0 - (a % 10 === 0 ? 34 : a % 5 === 0 ? 22 : 12); const t = -Math.PI / 2 + a * Math.PI / 180; g.lineWidth = a % 10 === 0 ? 2.5 : 1.2; g.beginPath(); g.moveTo(w / 2 + Math.cos(t) * r0, h + Math.sin(t) * r0); g.lineTo(w / 2 + Math.cos(t) * r1, h + Math.sin(t) * r1); g.stroke(); if (a % 10 === 0) g.fillText(String(a), w / 2 + Math.cos(t) * (r1 - 18), h + Math.sin(t) * (r1 - 18) + 7); }
  });
  const protFace = mesh(new THREE.PlaneGeometry(0.9, 0.9), new THREE.MeshBasicMaterial({ map: protTex, transparent: true, depthWrite: false, side: THREE.DoubleSide }), [0, 0.45, 0], { cast: false }); protFace.renderOrder = 9; prot.add(protFace);
  const arm = new THREE.Group(); prot.add(arm); const armM = mesh(new THREE.BoxGeometry(0.006, 0.45, 0.004), new THREE.MeshBasicMaterial({ color: 0xdc2626, depthTest: false }), [0, 0.225, 0.01], { cast: false }); armM.renderOrder = 10; arm.add(armM);
  const stepMeasure = {
    title: 'Measure the curvature', text: 'Pot A is lifted out of the box. Drag the red arm of the protractor until it lines up with the bent tip, then let go. The angle from the vertical is the curvature.',
    tool: null, autoTool: 'hand', hideBelt: true,
    shot: S([-0.45, 1.15, 1.75], [-0.45, 0.95, 0.6], 1.1),
    enter() {
      pots[0].g.position.set(-0.6, 0, 0.55); pots[0].g.rotation.y = 0; pots[1].g.position.x = -1.5; pots[2].g.visible = true;
      const s = pots[0].seeds[2]; measuring = s; const base = new THREE.Vector3(0, 0.45 * s.h * s.group.scale.y, 0.0); s.group.localToWorld(base); world.worldToLocal(base);
      prot.visible = true; prot.position.copy(base); prot.position.z += 0.16; arm.rotation.z = 0;
      ctx.rig.go({ pos: [base.x + 0.15, base.y + 0.8 + 0.35, base.z + 1.9], target: [base.x + 0.2, base.y + 0.8 + 0.25, base.z], fit: 1.25, fitH: 0.9 }, 1.0);
    },
    skip() { results.measured = meanAngle(0) + (R() - 0.5) * 3; ui.observe('Curvature (protractor)', `${Math.round(results.measured)}°`); },
    exit() { prot.visible = false; },
    handler: {
      down() { this.on = true; return true; },
      move(p) { if (!this.on) return; prot.getWorldPosition(tmp); input.project(tmp, tmp, ctx.stage.clientWidth, ctx.stage.clientHeight); const a = Math.atan2(p.x - tmp.x, tmp.y - p.y); arm.rotation.z = -clamp(a, -0.1, Math.PI / 2); },
      up() {
        this.on = false; const read = Math.round(-arm.rotation.z * 57.3); const truth = measuring.angle * 57.3;
        if (Math.abs(read - truth) > 6) { ctx.mistake(`The arm is at ${read}°, but the tip points at about ${Math.round(truth / 5) * 5}°. Line it up with the tip itself.`, 2); return; }
        results.measured = read; ui.observe('Curvature (protractor)', `${read}°`); sfx.play('ok'); ctx.next(`Curvature ${read}° toward the light.`);
      },
    },
  };
  const stepExplain = {
    title: 'Explain', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: BENCH,
    enter() {
      sh = sheet(ctx, { title: 'After 4 days' });
      sh.set(table(['Pot', 'Treatment', 'Curvature'], [['A', 'light from one side', `${Math.round(results.measured ?? meanAngle(0))}°`], ['B', 'even light', '0°'], ['C', 'one-sided light, tips capped', '0°']]));
      ask(ctx, 'Why did the shoots in pot A bend toward the slit?', [{ label: 'Auxin moved to the shaded side, which grew faster', value: 'ok' }, { label: 'Light speeds up growth on the lit side', value: 'lit' }, { label: 'The light pulled the shoots over', value: 'pull' }], 'ok', {
        ok: 'Positive phototropism: the shoot tip senses one-sided light; auxin is redistributed to the shaded side, cells there elongate more, and the shoot curves toward the light. Capped tips could not sense the light (C), and even light gives even auxin (B).',
        wrong: (v) => (v === 'lit' ? 'If the lit side grew faster the shoot would curve away. Which side elongated more?' : 'Growth is by cell elongation, controlled by a hormone made in the tip.'),
      });
    },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepCap, stepBox, stepTurn, stepLamp, stepDays, stepMeasure, stepExplain];
  ctx.debug = { pots, box, arm };
  void smooth; void ctx.fx;
  return {
    tools: ['hand', 'forceps'],
    steps,
    result() {
      const m = results.measured ?? meanAngle(0); const t = meanAngle(0);
      return { title: 'Phototropism', rows: [['Pot A curvature', `${Math.round(m)}° (mean of the four shoots ${Math.round(t)}°)`], ['Pot B (even light)', 'straight'], ['Pot C (tips capped)', 'straight']], conclusion: 'Shoots bend toward one-sided light (positive phototropism). The stimulus is received by the tip and the response, unequal elongation, happens below it: auxin collects on the shaded side and makes those cells elongate more.' };
    },
    dispose() { if (clock) clock.remove(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}

function apical(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const R = rng((Date.now() & 0xffff) || 9);
  const NODES = 4;
  const plants = ['A', 'B', 'C'].map((l, i) => {
    const g = pot(ctx, -1.2 + i * 1.2, 0.1, l === 'A' ? 'A: intact' : l === 'B' ? 'B: cut + lanolin' : 'C: cut + IAA lanolin');
    const H = 1.45; const main = stem([[0, 0.38, 0], [0.01, 0.9, 0], [0, H, 0]], 0.028, 0x4d7c0f, 0.014); g.add(main);
    const apex = new THREE.Group(); apex.position.y = H; g.add(apex); apex.add(bud(0x84cc16, 0.07));
    [-1, 1].forEach((s) => { const lf = leaf({ len: 0.16, wid: 0.1, upper: '#4d9a2a', lower: '#86c06a' }); lf.rotation.set(-0.6, s > 0 ? Math.PI / 2 : -Math.PI / 2, 0, 'YXZ'); lf.position.y = -0.02; apex.add(lf); });
    const laterals = [];
    for (let n = 0; n < NODES; n++) {
      const y = 0.6 + n * 0.21; const rot = n % 2 ? Math.PI / 2 : 0;
      [-1, 1].forEach((s) => {
        const nodeG = new THREE.Group(); nodeG.position.y = y; nodeG.rotation.y = rot + (s > 0 ? 0 : Math.PI); g.add(nodeG);
        const lf = leaf({ len: 0.36, wid: 0.22, upper: '#2f7d32', lower: '#7fb069' }); lf.rotation.set(0.45, Math.PI / 2, 0, 'YXZ'); nodeG.add(lf);
        const lat = new THREE.Group(); lat.position.set(0.03, 0.02, 0); lat.rotation.z = -0.75; nodeG.add(lat);
        const shoot = mesh(new THREE.CylinderGeometry(0.009, 0.012, 1, 8), wet(0x65a30d, { roughness: 0.5 }), null); lat.add(shoot);
        const tipB = bud(0x84cc16, 0.035); lat.add(tipB);
        const leaves = [-1, 1].map((q) => { const l2 = leaf({ len: 0.12, wid: 0.08, upper: '#3f8f2f', lower: '#86c06a' }); l2.rotation.set(-0.5, q > 0 ? Math.PI / 2 : -Math.PI / 2, 0, 'YXZ'); tipB.add(l2); return l2; });
        const L = { lat, shoot, tipB, leaves, len: 0, n, s };
        setLat(L, 0.005); laterals.push(L);
      });
    }
    return { g, main, apex, laterals, label: l, cut: false, paste: null, H };
  });
  function setLat(L, len) { L.len = len; L.shoot.scale.y = Math.max(0.001, len); L.shoot.position.y = len / 2; L.tipB.position.y = len; L.leaves.forEach((l) => { l.scale.setScalar(clamp(len / 0.25, 0.05, 1)); }); }
  const lanolin = [['Lanolin', 0xfef3c7, 'plain'], ['IAA in lanolin', 0xfde68a, '1% auxin']].map(([t, c, sub], i) => {
    const g = new THREE.Group(); g.position.set(0.95 + i * 0.5, 0, 0.95); world.add(g);
    g.add(mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.16, 24), MAT.glass(), [0, 0.08, 0], { cast: false }));
    g.add(mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.12, 24), wet(c, { roughness: 0.4 }), [0, 0.065, 0]));
    const l = tag(t, { h: 0.08 }); l.position.set(0, 0.3, 0); g.add(l); g.userData.kind = i ? 'iaa' : 'plain'; g.userData.sub = sub;
    return g;
  });
  const tmp = new THREE.Vector3();
  const BENCH = S([0.2, 2.6, 3.5], [0.1, 0.95, 0.2], 4.0);
  const TOP = (p) => S([p.g.position.x + 0.3, 2.05, 1.05], [p.g.position.x, 1.35, 0.1], 0.9);
  let clock = null; let loaded = null; let sh = null; const meas = {};

  function cutStep() {
    return {
      title: 'Remove the apical buds of B and C', text: 'With the <b>scissors</b>, snip off the shoot tip (apical bud) of plants <b>B</b> and <b>C</b>: drag across the stem just below the tip. Leave plant A intact.',
      tool: 'scissors', shot: S([0.6, 2.2, 2.2], [0.6, 1.35, 0.1], 2.2),
      skip() { plants.slice(1).forEach((p) => decap(p, true)); },
      handler: {
        down(p) { if (!ctx.requireTool('scissors')) return !!input.pick(plants.map((q) => q.g), true); this.last = [p.x, p.y]; tools.action(0.3); return true; },
        move(p) {
          if (!this.last) return;
          plants.forEach((q) => {
            if (q.cut) return; tmp.set(0, q.H - 0.06, 0); q.g.localToWorld(tmp); input.project(tmp, tmp, ctx.stage.clientWidth, ctx.stage.clientHeight);
            if (Math.abs(tmp.y - p.y) < 22 && ((this.last[0] - tmp.x) * (p.x - tmp.x) < 0)) {
              if (q.label === 'A') { ctx.mistake('Plant A is the intact control — keep its apical bud.', 3); this.last = null; return; }
              decap(q, false); tools.action(1); anim.wait(0.15, () => tools.action(0.3)); sfx.play('snip');
              if (plants[1].cut && plants[2].cut) anim.wait(0.8, () => ctx.next('B and C decapitated.'));
            }
          });
          if (this.last) this.last = [p.x, p.y];
        },
        up() { this.last = null; tools.action(0); },
      },
    };
  }
  function decap(p, instant) {
    p.cut = true; const a = p.apex;
    if (instant) { a.visible = false; return; }
    p.g.localToWorld(tmp.set(0, p.H, 0)); fx.burst(tmp, 0x84cc16, 5, 0.12, ctx.BENCH_Y + 0.02);
    const from = a.position.clone(); anim.add(0.8, (k) => { a.position.set(from.x + k * 0.3, from.y - k * k * (p.H - 0.1), from.z + k * 0.15); a.rotation.z = k * 2; }, { done: () => { a.visible = false; } });
  }
  const capMeshes = [];
  const stepPaste = {
    title: 'Smear the cut stumps', text: 'With the <b>brush</b>, take plain <b>lanolin</b> to the cut top of <b>B</b>, and <b>IAA in lanolin</b> to the cut top of <b>C</b> (tap a jar, then the stump).',
    tool: 'brush', shot: S([0.6, 2.2, 2.4], [0.9, 1.0, 0.4], 2.6),
    skip() { paste(plants[1], 'plain'); paste(plants[2], 'iaa'); },
    handler: { down() {
      const jar = lanolin.find((j) => input.pick([j], true));
      if (jar) { if (!ctx.requireTool('brush')) return true; loaded = jar.userData.kind; sfx.play('squish'); ctx.say(`Brush loaded with ${jar.userData.kind === 'iaa' ? 'IAA in lanolin' : 'plain lanolin'}.`, 'info', 1400); return true; }
      const p = plants.find((q) => input.pick([q.g], true)); if (!p) return false;
      if (!ctx.requireTool('brush')) return true;
      if (!p.cut) { ctx.mistake('Plant A was not cut; nothing goes on it.', 2); return true; }
      if (!loaded) { ctx.say('Dip the brush in a jar first.', 'hint', 1600); return true; }
      if (p.paste) { ctx.say('That stump is already covered.', 'hint', 1400); return true; }
      const want = p.label === 'B' ? 'plain' : 'iaa';
      if (loaded !== want) { ctx.mistake(p.label === 'B' ? 'B gets plain lanolin: it shows what the cut alone does.' : 'C gets lanolin with IAA: it tests whether auxin can replace the apical bud.', 3); return true; }
      paste(p, loaded); loaded = null; sfx.play('squish');
      if (plants[1].paste && plants[2].paste) ctx.next('Both stumps covered. Lanolin is only a carrier.'); return true;
    } },
  };
  function paste(p, kind) { p.paste = kind; const m = mesh(new THREE.SphereGeometry(0.03, 12, 8), wet(kind === 'iaa' ? 0xfde68a : 0xfef3c7, { roughness: 0.35 }), [0, p.H - 0.01, 0]); m.scale.y = 0.6; p.g.add(m); capMeshes.push(m); }
  // growth over days: lateral buds released from dominance grow ~1 cm a day after a lag; the top nodes first
  function growTo(d) {
    plants.forEach((p) => {
      const released = p.label === 'B';
      p.laterals.forEach((L) => {
        const rank = NODES - 1 - L.n; const lag = 2 + rank * 1.2;
        const len = released ? clamp((d - lag) * (0.036 - rank * 0.006), 0.005, 1) : (p.label === 'A' ? 0.005 + (L.n === NODES - 1 ? d * 0.0006 : 0) : 0.005 + d * 0.0004);
        setLat(L, len * (L.s > 0 ? 1 : 0.92));
      });
      if (p.label === 'A') { const h = 1.45 + d * 0.035; p.apex.position.y = h; p.H = h; p.main.scale.y = h / 1.45; p.main.position.y = (1 - h / 1.45) * 0.38; }
    });
  }
  const stepDays = {
    title: 'Two weeks later', text: 'Run the clock forward two days at a time to day 14 and watch the lateral (axillary) buds.', tool: null, autoTool: 'hand', hideBelt: true, shot: BENCH,
    enter() { clock = timelapse(ctx, { step: 2, unit: 'day', dur: 1.6, onTick: (d, done) => { growTo(d); if (done && d >= 14 && !this.done) { this.done = true; clock.show(false); ctx.next('B has branched; A and C have not.'); } } }); },
    skip() { growTo(14); },
    exit() { if (clock) clock.remove(); clock = null; },
  };
  const longest = (p) => p.laterals.reduce((a, L) => Math.max(a, L.len), 0) * 10; // cm
  const stepMeasure = {
    title: 'Measure the longest lateral shoot', text: 'For each plant, tap the <b>tip</b> of its longest lateral shoot (or the bud, if it has not grown). The length from the node is read off the rule.',
    tool: null, autoTool: 'hand', shot: BENCH,
    skip() { plants.forEach((p) => { meas[p.label] = longest(p); }); },
    handler: { down(p) {
      const hit = input.pick(plants.flatMap((q) => q.laterals.map((L) => L.lat)), true); if (!hit) return false;
      let o = hit.object; let L = null; plants.forEach((q) => q.laterals.forEach((x) => { let k = o; while (k) { if (k === x.lat) L = x; k = k.parent; } }));
      const plant = plants.find((q) => q.laterals.includes(L)); if (!L || !plant) return false;
      const best = plant.laterals.reduce((a, x) => (x.len > a.len ? x : a), plant.laterals[0]);
      if (best.len > 0.05 && L.len < best.len * 0.7) { ctx.say(`Plant ${plant.label} has a longer lateral shoot than that one.`, 'hint', 1800); return true; }
      const cm = Math.round(longest(plant) * 2) / 2; meas[plant.label] = cm; sfx.play('ok'); ui.observe(`Lateral shoot ${plant.label}`, `${cm.toFixed(1)} cm`);
      L.tipB.getWorldPosition(tmp); fx.burst(tmp, 0xfacc15, 4, 0.05, tmp.y);
      if (['A', 'B', 'C'].every((k) => meas[k] !== undefined)) ctx.next(); return true;
    } },
  };
  const stepExplain = {
    title: 'Apical dominance', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: BENCH,
    enter() {
      sh = sheet(ctx, { title: 'Day 14' });
      sh.set(table(['Plant', 'Treatment', 'Longest lateral'], [['A', 'intact', `${meas.A.toFixed(1)} cm`], ['B', 'decapitated + lanolin', `${meas.B.toFixed(1)} cm`], ['C', 'decapitated + IAA lanolin', `${meas.C.toFixed(1)} cm`]]));
      ask(ctx, 'What do plants B and C show?', [{ label: 'Auxin from the apical bud inhibits the lateral buds', value: 'ok' }, { label: 'Cutting a plant always makes it branch', value: 'cut' }, { label: 'Lanolin makes buds grow', value: 'lan' }], 'ok', {
        ok: 'Apical dominance: auxin (IAA) made in the apical bud and moving down the stem keeps the axillary buds dormant. Remove the apex and they grow (B); supply auxin in its place and they stay dormant (C). Gardeners prune hedges and pinch tea bushes to make them bushy.',
        wrong: (v) => (v === 'cut' ? 'Plant C was cut too, yet did not branch. What did C get that B did not?' : 'B had plain lanolin and branched; C had lanolin too and did not. So it is not the lanolin.'),
      });
    },
    exit() { ui.clearChooser(); },
  };
  const steps = [cutStep(), stepPaste, stepDays, stepMeasure, stepExplain];
  ctx.debug = { plants, TOP };
  return {
    tools: ['hand', 'scissors', 'brush'],
    steps,
    result() { return { title: 'Apical dominance', rows: [['Longest lateral, A (intact)', `${(meas.A ?? longest(plants[0])).toFixed(1)} cm`], ['B (cut + lanolin)', `${(meas.B ?? longest(plants[1])).toFixed(1)} cm`], ['C (cut + IAA)', `${(meas.C ?? longest(plants[2])).toFixed(1)} cm`]], conclusion: 'The lateral buds grew only when the apical bud was removed and not replaced by auxin. Auxin from the shoot apex suppresses the growth of axillary buds (apical dominance); IAA in lanolin substitutes for the apex.' }; },
    dispose() { if (clock) clock.remove(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}
