// T.S. of dicot and monocot stem and root, cut by hand: hold the material in a pith block, take
// several thin sections with a razor in quick, level strokes, float them in water, pick the
// thinnest with a brush, stain it in safranin, wash, mount in glycerine under a coverslip, and
// find each tissue under the microscope.
import { THREE } from '../../engine.js';
import { watchGlass, reagentBottle } from '../props.js';
import { buildStation, stepDrop, stepCoverslip, stepToStage, createScopeView } from '../slideprep.js';
import { createSectionField } from '../fields/section.js';
import { ease, clamp, MAT, mesh } from '../kit.js';

const KINDS = {
  dicotStem: { label: 'Dicot stem (sunflower)', color: 0x6f9a3a, find: ['epidermis', 'hypodermis', 'cortex', 'endodermis', 'sclerenchyma (pericycle)', 'phloem', 'cambium', 'xylem', 'pith'], key: 'Vascular bundles in a ring; conjoint, collateral and open (cambium); endarch xylem' },
  monocotStem: { label: 'Monocot stem (maize)', color: 0x9cb85a, find: ['epidermis', 'hypodermis', 'ground tissue', 'bundle sheath', 'phloem', 'xylem'], key: 'Many scattered, closed bundles, each in a sclerenchyma sheath; no cortex–pith boundary' },
  dicotRoot: { label: 'Dicot root (gram)', color: 0xeae2c8, find: ['root hairs', 'epiblema', 'cortex', 'endodermis', 'pericycle', 'xylem', 'phloem'], key: 'Radial bundles with 2–4 exarch xylem groups; little or no pith' },
  monocotRoot: { label: 'Monocot root (maize)', color: 0xefe6cc, find: ['root hairs', 'epiblema', 'cortex', 'endodermis', 'xylem', 'phloem', 'pith'], key: 'Radial, polyarch xylem (many groups) round a large pith' },
};
const NOTES = {
  epidermis: 'Epidermis: one layer of barrel-shaped cells under the waxy cuticle.',
  hypodermis: 'Hypodermis: under the epidermis — collenchyma in the dicot stem, red-staining sclerenchyma in the monocot stem.',
  cortex: 'Cortex: many layers of thin-walled parenchyma with intercellular spaces.',
  endodermis: 'Endodermis: the innermost cortical layer of barrel-shaped cells — a starch sheath in the stem, with Casparian strips in the root.',
  'sclerenchyma (pericycle)': 'Pericycle: patches of thick, lignified sclerenchyma (hard bast) capping each bundle — stained red.',
  pericycle: 'Pericycle: a single layer of cells just inside the endodermis; lateral roots arise here.',
  phloem: 'Phloem: small, thin-walled sieve tubes and companion cells; it carries food.',
  cambium: 'Cambium: a strip of thin, flattened dividing cells between phloem and xylem — the bundle is open.',
  xylem: 'Xylem: thick, lignified vessels stained red by safranin; they carry water.',
  pith: 'Pith (medulla): the central parenchyma.',
  'ground tissue': 'Ground tissue: parenchyma not divided into cortex, endodermis and pith.',
  'bundle sheath': 'Bundle sheath: a ring of sclerenchyma round each closed bundle.',
  'root hairs': 'Root hairs: single-celled outgrowths of the epiblema that absorb water.',
  epiblema: 'Epiblema (piliferous layer): the root\'s outer layer, with no cuticle.',
};
const ALIAS = { 'medullary ray': 'cortex', hairs: 'epidermis', 'conjunctive tissue': 'pith' };

export function create(ctx) {
  const { world, input, tools, fx, anim, sfx, ui } = ctx;
  const st = buildStation(ctx, { tileX: 0.1, tileZ: 0.35, slideDX: 0.42 });
  const water = watchGlass(0xcfe8f5, 0.55); water.scale.setScalar(0.62); water.position.set(-0.05, 0.03, -0.18); world.add(water);
  const safr = watchGlass(0xb91c3c, 0.85); safr.scale.setScalar(0.62); safr.position.set(0.42, 0.03, -0.22); world.add(safr);
  const b1 = reagentBottle('Safranin', 0xb91c3c, '1% aqueous'); b1.position.set(0.85, 0, -0.6); world.add(b1);
  const b2 = reagentBottle('Glycerine', 0xf8fafc, '50%'); b2.position.set(1.15, 0, -0.45); world.add(b2);
  const block = new THREE.Group(); block.position.set(-0.6, 0, 0.25); world.add(block);
  const pith = mesh(new THREE.CylinderGeometry(0.13, 0.14, 0.42, 28), MAT.matte(0xf3ead2), [0, 0.21, 0]); block.add(pith);
  ctx.surfaces.push(st.tile);
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3();
  const projectFn = (v, out) => input.project(v, out, ctx.stage.clientWidth, ctx.stage.clientHeight);
  let kind = null; let spec = null; const sections = []; let chosen = null; let field = null; let view = null;
  const SHOT_BLOCK = { pos: [-0.35, 1.75, 1.05], target: [-0.32, 1.0, 0.05], fit: 1.1 };
  const SHOT_GLASS = { pos: [0.2, 1.6, 0.85], target: [0.2, 0.86, -0.15], fit: 0.95 };
  const SHOT_SLIDE = { pos: [0.52, 1.32, 1.02], target: [0.52, 0.84, 0.52], fit: 0.55 };

  function choose(k) {
    kind = k;
    spec = mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.45, 20), new THREE.MeshPhysicalMaterial({ color: KINDS[k].color, roughness: 0.5, clearcoat: 0.4 }), [0, 0.235, 0]);
    block.add(spec);
    const face = mesh(new THREE.CircleGeometry(0.034, 24), new THREE.MeshStandardMaterial({ color: k.endsWith('Root') ? 0xf1ead5 : 0xd6e6b5 }), [0, 0.461, 0]); face.rotation.x = -Math.PI / 2; block.add(face);
    ui.observe('Material', KINDS[k].label);
  }
  const stepChoose = {
    title: 'Choose the material', text: 'Which will you section today?', autoTool: 'hand', hideBelt: true, shot: SHOT_BLOCK,
    enter() { anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, ctx.stage.clientHeight * 0.3, 'Material to section', Object.entries(KINDS).map(([k, v]) => ({ label: v.label, value: k })), (v) => { choose(v); ctx.next(`A piece of ${KINDS[v].label.toLowerCase()} is held upright in a block of pith, its cut end just level with the top.`, 0.4); })); },
    skip() { if (!kind) choose(window.__bhKind || 'dicotStem'); },
    exit() { ui.clearChooser(); },
  };

  // ---- sectioning with the razor --------------------------------------------------------------
  let stroke = null;
  const stepCut = {
    title: 'Cut thin sections',
    text: 'Wet the razor and draw it across the top of the block in one <b>quick, level</b> stroke. Cut at least three sections; they collect in the watch glass of water.',
    hint: 'Swipe straight across the top of the block, left to right or right to left, briskly. Slow or wobbly strokes give thick sections.',
    tool: 'razor', shot: SHOT_BLOCK,
    aim(p, out) { const pt = input.planePoint(ctx.BENCH_Y + 0.47, out); return pt ? true : false; },
    skip() { [0.25, 0.7, 0.45].forEach((t) => addSection(t, true)); },
    handler: {
      down(p) { if (!ctx.requireTool('razor', 'Hand sections are cut with a sharp <b>razor</b>, held flat.')) return true; stroke = { x0: p.x, y0: p.y, t0: performance.now(), ymin: p.y, ymax: p.y, crossed: false }; tools.press(1); return true; },
      move(p) {
        if (!stroke) return;
        stroke.ymin = Math.min(stroke.ymin, p.y); stroke.ymax = Math.max(stroke.ymax, p.y);
        tmp.set(0, 0.47, 0); block.localToWorld(tmp); projectFn(tmp, tmp2);
        if (!stroke.crossed && Math.sign(p.x - tmp2.x) !== Math.sign(stroke.x0 - tmp2.x) && Math.abs(p.y - tmp2.y) < 60) {
          stroke.crossed = true;
          const dt = Math.max(1, performance.now() - stroke.t0); const speed = Math.abs(p.x - stroke.x0) / dt; const wobble = (stroke.ymax - stroke.ymin) / Math.max(1, Math.abs(p.x - stroke.x0));
          const t = clamp(1.05 - speed * 0.45 + wobble * 1.4, 0.15, 1);
          addSection(t, false);
        }
      },
      up() { stroke = null; tools.press(0); },
    },
  };
  function addSection(t, instant) {
    sfx.play('cut');
    const d = mesh(new THREE.CylinderGeometry(0.034, 0.034, 0.002 + t * 0.012, 24), new THREE.MeshPhysicalMaterial({ color: KINDS[kind].color, roughness: 0.4, transparent: true, opacity: 0.35 + t * 0.6, clearcoat: 0.6 }));
    d.userData.t = t; world.add(d); sections.push(d);
    tmp.set(0, 0.47, 0); block.localToWorld(tmp); world.worldToLocal(tmp);
    const from = tmp.clone(); const i = sections.length - 1;
    const to = new THREE.Vector3(water.position.x + Math.cos(i * 2.1) * 0.08, 0.07, water.position.z + Math.sin(i * 2.1) * 0.06);
    if (instant) d.position.copy(to);
    else anim.add(0.7, (k) => { d.position.lerpVectors(from, to, k); d.position.y += Math.sin(Math.PI * k) * 0.15; d.rotation.x = k * 4; }, { ease: ease.inOut, done: () => { d.rotation.x = 0; sfx.play('drop'); } });
    ctx.progress(sections.length / 3);
    ui.observe(`Section ${sections.length}`, t < 0.4 ? 'thin' : t < 0.7 ? 'medium' : 'thick');
    if (!instant) ctx.say(t < 0.4 ? 'A thin, almost transparent section.' : t < 0.7 ? 'Medium — usable, but a thinner one would be clearer.' : 'Thick and opaque: a slower or tilted stroke. Cut briskly and level.', t < 0.4 ? 'good' : 'hint', 2500);
    if (sections.length >= 3 && !instant && ctx.step === stepCut) anim.wait(1, () => { if (sections.some((s) => s.userData.t < 0.45)) ctx.next('Enough sections. Most hand sections are uneven; the trick is to choose well.'); else ctx.say('None is really thin yet — cut another.', 'hint', 2500); });
  }
  const stepChooseSection = {
    title: 'Pick the thinnest section',
    text: 'With a fine <b>brush</b>, lift the thinnest, most transparent section and put it in the safranin.',
    hint: 'The faintest, most see-through disc is the thinnest. Tap it with the brush.',
    tool: 'brush', shot: SHOT_GLASS,
    skip() { chosen = sections.slice().sort((a, b) => a.userData.t - b.userData.t)[0]; chosen.position.set(safr.position.x, 0.07, safr.position.z); },
    handler: {
      down() {
        let best = null; let bd = 40;
        sections.forEach((s) => { s.getWorldPosition(tmp); projectFn(tmp, tmp2); const d = Math.hypot(tmp2.x - input.ptr.x, tmp2.y - input.ptr.y); if (d < bd) { bd = d; best = s; } });
        if (!best) return false;
        if (!ctx.requireTool('brush', 'Sections are moved with a soft <b>brush</b> — forceps crush them.')) return true;
        const thinnest = Math.min(...sections.map((s) => s.userData.t));
        if (best.userData.t > thinnest + 0.08 && best.userData.t > 0.45) { ctx.mistake('That one is thicker — light cannot pass through several layers of cells. Choose the most transparent disc.', 3); return true; }
        chosen = best; sfx.play('pick');
        const from = best.position.clone(); const to = new THREE.Vector3(safr.position.x, 0.07, safr.position.z);
        anim.add(0.7, (k) => { best.position.lerpVectors(from, to, k); best.position.y += Math.sin(Math.PI * k) * 0.12; }, { ease: ease.inOut, done: () => { sfx.play('drop'); ctx.next('In the safranin. Lignified walls will take up the red stain.'); } });
        return true;
      },
    },
  };
  const stepStain = {
    title: 'Stain for two minutes',
    text: 'Leave the section in safranin for about two minutes. Tap the watch glass to start the timer.',
    tool: null, autoTool: 'hand', shot: SHOT_GLASS,
    skip() { chosen.material.color.setHex(0xc0264a); chosen.userData.stained = 1; },
    handler: {
      down() {
        if (!input.pick([safr, chosen])) return false;
        if (this.running) return true; this.running = true;
        const c0 = chosen.material.color.clone(); const c1 = new THREE.Color(0xc0264a);
        anim.add(4, (k) => { chosen.material.color.copy(c0).lerp(c1, k); ctx.progress(k); ui.setText(`Staining… ${Math.round(k * 120)} s of 120 s`); }, { ease: (t) => t, done: () => { chosen.userData.stained = 1; ctx.next('Stained.'); } });
        return true;
      },
    },
  };
  const stepWash = {
    title: 'Wash off excess stain',
    text: 'Move the section back into the water with the <b>brush</b> to rinse away excess stain, so only the lignified walls stay red.',
    tool: 'brush', shot: SHOT_GLASS,
    skip() { chosen.position.set(water.position.x, 0.07, water.position.z); },
    handler: {
      down() {
        chosen.getWorldPosition(tmp); projectFn(tmp, tmp2); if (Math.hypot(tmp2.x - input.ptr.x, tmp2.y - input.ptr.y) > 44) return false;
        if (!ctx.requireTool('brush')) return true;
        const from = chosen.position.clone(); const to = new THREE.Vector3(water.position.x, 0.07, water.position.z);
        anim.add(0.7, (k) => { chosen.position.lerpVectors(from, to, k); chosen.position.y += Math.sin(Math.PI * k) * 0.12; }, { ease: ease.inOut, done: () => { sfx.play('drop'); fx.burst(chosen.getWorldPosition(new THREE.Vector3()), 0xf9a8b8, 6, 0.08, ctx.BENCH_Y + 0.07); ctx.next('Rinsed. Excess red clouds the water.'); } });
        return true;
      },
    },
  };
  const stepGly = stepDrop(ctx, st, { title: 'A drop of glycerine on the slide', text: 'Put one drop of <b>glycerine</b> in the middle of the slide; it keeps the section from drying.', color: 0xf8fafc, shot: SHOT_SLIDE });
  const stepMount = {
    title: 'Lay the section in the glycerine',
    text: 'With the <b>brush</b>, transfer the stained section onto the drop.',
    tool: 'brush', shot: { pos: [0.3, 1.6, 1.1], target: [0.25, 0.86, 0.2], fit: 1.0 },
    skip() { place(true); },
    handler: {
      down() {
        chosen.getWorldPosition(tmp); projectFn(tmp, tmp2); if (Math.hypot(tmp2.x - input.ptr.x, tmp2.y - input.ptr.y) > 44) return false;
        if (!ctx.requireTool('brush')) return true;
        place(false); return true;
      },
    },
  };
  function place(instant) {
    st.specimen = chosen;
    const to = new THREE.Vector3(st.slide.position.x, st.slideTopY + 0.003, st.slide.position.z);
    if (instant) { chosen.position.copy(to); return; }
    const from = chosen.position.clone();
    anim.add(0.8, (k) => { chosen.position.lerpVectors(from, to, k); chosen.position.y += Math.sin(Math.PI * k) * 0.15; }, { ease: ease.inOut, done: () => { sfx.play('place'); ctx.next(); } });
  }
  const stepCover = stepCoverslip(ctx, st, { shot: SHOT_SLIDE });
  const stepStage = stepToStage(ctx, st, { shotStart: SHOT_SLIDE });

  function makeView() {
    if (view) return view;
    field = createSectionField(kind, { bubbles: st.bubbles, thick: chosen ? Math.max(0, chosen.userData.t - 0.35) : 0, stain: chosen && chosen.userData.stained ? 1 : 0.2 });
    view = createScopeView(ctx, st, field, { objective: 4, focus: -500, onTap: (c, e) => { if (ctx.step && ctx.step.onTap) ctx.step.onTap(e); } });
    ctx.debug = { field, view };
    return view;
  }
  const eyeHandler = { down() { const h = input.pick(st.scope.pickables); if (h) { makeView().open(); return true; } return false; } };
  let sharpT = 0;
  const stepFocus = {
    title: 'Focus the whole section (4×)',
    text: 'Look in. With the 4× objective, focus with the coarse then fine knob so the whole section is sharp.',
    hint: 'Drag the coarse knob up slowly, then fine.', tool: null, hideBelt: true, handler: eyeHandler,
    enter() { makeView().open(); sharpT = 0; },
    skip() { makeView(); },
    update(dt) { const e = view && view.eye; if (!e) return; const s = e.state; ctx.progress(clamp(1 - s.blur / 10)); if (s.sharp) { sharpT += dt; if (sharpT > 0.6 && !this.done) { this.done = true; ctx.next('The whole section in view: lignified tissue glows red.'); } } else sharpT = 0; },
  };
  let findIdx = 0;
  const stepFind = {
    title: 'Find each tissue',
    text: '',
    hint: 'Work from the outside of the section inward. Use 10× to see cells more clearly; drag to move around.', tool: null, hideBelt: true, handler: eyeHandler,
    enter() { if (!view || !view.eye) makeView().open(); findIdx = 0; this.prompt(); },
    prompt() { const list = KINDS[kind].find; if (findIdx >= list.length) return; ui.setText(`Tap the <b>${list[findIdx]}</b>. (${findIdx + 1} of ${list.length})`); ctx.progress(findIdx / list.length); },
    skip() { },
    onTap(e) {
      const eye = view.eye; const list = KINDS[kind].find; if (findIdx >= list.length) return;
      if (e.blur > 3) { ctx.say('Focus first.', 'hint', 1500); return; }
      let t = field.tissueAt(e.x, e.y); t = ALIAS[t] && list.indexOf(t) < 0 ? ALIAS[t] : t;
      const want = list[findIdx];
      if (t === want) {
        sfx.play('ok'); eye.mark(e.x, e.y, want); ctx.say(NOTES[want] || want, 'good', 4200); ui.observe(want, 'found');
        findIdx += 1; this.prompt();
        if (findIdx >= list.length) anim.wait(1.2, () => ctx.next());
      } else ctx.mistake(t ? `That is ${t}, not the ${want}. ${NOTES[want] || ''}` : `That is outside the section. Find the ${want}.`, 2);
    },
  };
  const stepIdentify = {
    title: 'What identifies it?', text: 'Which feature tells you what this section is?', tool: null, hideBelt: true, handler: eyeHandler,
    enter() {
      const opts = Object.entries(KINDS).map(([k, v]) => ({ label: v.key, value: k }));
      opts.sort(() => Math.random() - 0.5);
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, 70, `Diagnostic feature of the ${KINDS[kind].label.split(' (')[0].toLowerCase()}`, opts, (v) => {
        if (v === kind) { ui.observe('Key feature', KINDS[kind].key); ctx.next(); }
        else { ctx.mistake(`That describes a ${KINDS[v].label.split(' (')[0].toLowerCase()}. Look at how the vascular tissue is arranged in yours.`, 3); anim.wait(0.4, ask); }
      });
      anim.wait(0.6, ask);
    },
    exit() { ui.clearChooser(); },
  };

  const steps = [stepChoose, stepCut, stepChooseSection, stepStain, stepWash, stepGly, stepMount, stepCover, stepStage, stepFocus, stepFind, stepIdentify];
  return {
    tools: ['hand', 'razor', 'brush', 'dropper', 'needle'],
    steps,
    update(dt, t) { if (view) view.update(t); },
    result() {
      return {
        title: `T.S. of ${KINDS[kind].label.toLowerCase()}`,
        rows: [['Sections cut', String(sections.length)], ['Section used', chosen ? (chosen.userData.t < 0.4 ? 'thin' : chosen.userData.t < 0.7 ? 'medium' : 'thick') : '—'], ['Tissues found', String(KINDS[kind].find.length)], ['Air bubbles', String(st.bubbles)]],
        conclusion: `${KINDS[kind].label}: ${KINDS[kind].key}. Safranin stained the lignified xylem and sclerenchyma red; thin-walled parenchyma, phloem and collenchyma stayed pale.`,
      };
    },
    dispose() { if (view) view.dispose(); if (field) field.dispose(); },
  };
}
