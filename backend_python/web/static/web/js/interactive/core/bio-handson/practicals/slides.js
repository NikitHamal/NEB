// Studying permanent slides: take the right slide from the slide box, wipe it clean with lens
// paper, lay it under the stage clips, focus under low power and then high power, and find each
// structure the practical asks for. Used for animal tissues, plant tissues, animal mitosis and
// frog development, each with its own slides.
import { THREE } from '../../engine.js';
import { buildStation, stepToStage, createScopeView } from '../slideprep.js';
import { bloodField, squamousField, muscleField, frogField } from '../fields/tissues.js';
import { createSectionField } from '../fields/section.js';
import { createEpidermisField } from '../fields/epidermis.js';
import { createOnionField, PHASE_INFO } from '../fields/onion.js';
import { canvasTexture, clamp, MAT, mesh, roundedSlab } from '../kit.js';

const NOTES = {
  nucleus: 'Nucleus: stained dark, near the centre of each flat cell.', cytoplasm: 'Cytoplasm: pale and granular around the nucleus.', 'cell membrane': 'Cell membrane: the thin outline; squamous cells fit together like floor tiles.',
  'dark band (A band)': 'A band: the dark, anisotropic band of thick myosin filaments.', 'light band (I band)': 'I band: the light, isotropic band of thin actin filaments.', sarcolemma: 'Sarcolemma: the membrane wrapping each long, multinucleate fibre.',
  'red blood cell': 'Red blood cells: small, pale, biconcave discs without a nucleus.', neutrophil: 'Neutrophil: 2–5 lobed nucleus, fine pale granules; the commonest white cell.', lymphocyte: 'Lymphocyte: a large round nucleus filling the cell, a thin rim of blue cytoplasm.', monocyte: 'Monocyte: the largest white cell, with a kidney-shaped nucleus.', eosinophil: 'Eosinophil: bilobed nucleus and coarse red granules.', basophil: 'Basophil: dark blue-black granules hiding the nucleus.', platelet: 'Platelets: tiny purple cell fragments that help blood clot.',
  parenchyma: 'Parenchyma: living, thin-walled, roundish cells with intercellular spaces.', collenchyma: 'Collenchyma: living cells thickened at the corners with cellulose; support in young stems.', sclerenchyma: 'Sclerenchyma: dead cells with thick lignified walls — stained red.', xylem: 'Xylem: lignified vessels that conduct water.', phloem: 'Phloem: sieve tubes and companion cells that conduct food.', epidermis: 'Epidermis: the outer protective layer.',
  'guard cells': 'Guard cells: a bean-shaped pair with chloroplasts, controlling the stomatal pore.', 'epidermal cell': 'Epidermal cells: colourless or coloured, without chloroplasts, fitted tightly.',
};

function slideLabel(text) {
  return canvasTexture(`slidelbl:${text}`, 256, 256, (g, w, h) => {
    g.fillStyle = '#fbfaf3'; g.fillRect(0, 0, w, h); g.fillStyle = '#1e3a8a'; g.fillRect(0, 0, w, 26);
    g.fillStyle = '#111827'; g.font = '700 30px system-ui, sans-serif'; g.textAlign = 'center';
    const words = text.split(' '); let line = ''; let y = 80;
    for (const wd of words) { const t = line ? `${line} ${wd}` : wd; if (g.measureText(t).width > 230) { g.fillText(line, w / 2, y); y += 36; line = wd; } else line = t; }
    g.fillText(line, w / 2, y);
  });
}

const SECTION_MAP = { cortex: 'parenchyma', pith: 'parenchyma', 'medullary ray': 'parenchyma', hypodermis: 'collenchyma', 'sclerenchyma (pericycle)': 'sclerenchyma', xylem: 'xylem', phloem: 'phloem', epidermis: 'epidermis' };
const SETS = {
  'animal-tissue-slides': [
    { label: 'Squamous epithelium', make: squamousField, obj: 40, stain: 0x93c5fd },
    { label: 'Striated muscle L.S.', make: muscleField, obj: 40, stain: 0xf9a8d4 },
    { label: 'Human blood smear', make: bloodField, obj: 40, stain: 0xfda4af },
  ],
  'plant-tissue-diversity': [
    { label: 'T.S. dicot stem', make: () => { const f = createSectionField('dicotStem', { stain: 1 }); f.featureAt = (x, y) => SECTION_MAP[f.tissueAt(x, y)] || null; f.find = ['epidermis', 'collenchyma', 'parenchyma', 'sclerenchyma', 'phloem', 'xylem']; return f; }, obj: 10, stain: 0xfca5a5 },
    { label: 'Leaf epidermal peel', make: () => { const f = createEpidermisField({ seed: 11 }); f.featureAt = (x, y) => { const c = f.hit(x, y); return c ? (c.stoma ? 'guard cells' : 'epidermal cell') : null; }; f.find = ['guard cells', 'epidermal cell']; return f; }, obj: 40, stain: 0xc4b5fd },
  ],
  'grasshopper-animal-mitosis': [
    { label: 'Grasshopper testis squash', make: () => { const f = createOnionField({ animal: true }); f.featureAt = (x, y) => { const c = f.hit(x, y); return c ? c.phase : null; }; f.find = ['prophase', 'metaphase', 'anaphase', 'telophase']; f.start = { x: f.meristem.x + 40, y: f.meristem.y }; return f; }, obj: 40, stain: 0xf0abfc },
  ],
  'frog-development-stages': [
    { label: 'Frog embryos W.M.', make: frogField, obj: 4, stain: 0xd6d3d1 },
  ],
};

export function create(ctx) {
  const { world, input, tools, fx, anim, sfx, ui } = ctx;
  const set = SETS[ctx.config.slug];
  const st = buildStation(ctx, { tileX: 0.1, tileZ: 0.35, slideDX: 0.42 });
  const home = st.slide.position.clone();
  ctx.surfaces.push(st.tile);
  // the slide box: a wooden case with grooved slots, slides standing in it
  const box = new THREE.Group(); box.position.set(-0.55, 0, 0.0); world.add(box);
  box.add(mesh(roundedSlab(0.95, 0.42, 0.14, 0.02), MAT.gloss(0x7c4a22)));
  const boxSlides = set.map((s, i) => {
    const sl = new THREE.Group();
    sl.add(mesh(new THREE.BoxGeometry(0.012, 0.26, 0.76), MAT.glassEdge(), null, { cast: false }));
    const lab = mesh(new THREE.PlaneGeometry(0.2, 0.2), new THREE.MeshStandardMaterial({ map: slideLabel(s.label), roughness: 0.8 }), [0.007, 0.0, -0.26]); lab.rotation.y = Math.PI / 2; sl.add(lab);
    const smear = mesh(new THREE.PlaneGeometry(0.14, 0.14), new THREE.MeshStandardMaterial({ color: s.stain, transparent: true, opacity: 0.7 }), [0.007, 0, 0.05]); smear.rotation.y = Math.PI / 2; sl.add(smear);
    sl.position.set(-0.3 + i * 0.12, 0.2, 0); sl.rotation.y = Math.PI / 2; sl.rotation.z = 0.0;
    sl.userData.slide = i; box.add(sl); return sl;
  });
  const smudge = mesh(new THREE.PlaneGeometry(0.5, 0.2), new THREE.MeshBasicMaterial({ color: 0x9aa0a6, transparent: true, opacity: 0.45, depthWrite: false }), [0, 0.0135, 0]);
  smudge.rotation.x = -Math.PI / 2; st.slide.add(smudge);
  const specimen = mesh(new THREE.PlaneGeometry(0.16, 0.16), new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.75 }), [0.04, 0.0128, 0]);
  specimen.rotation.x = -Math.PI / 2; st.slide.add(specimen);
  const label = mesh(new THREE.PlaneGeometry(0.16, 0.16), new THREE.MeshStandardMaterial({ roughness: 0.8 }), [-0.29, 0.0131, 0]); label.rotation.x = -Math.PI / 2; label.rotation.z = Math.PI / 2; st.slide.add(label);
  st.slide.visible = false;
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3();
  const projectFn = (v, out) => input.project(v, out, ctx.stage.clientWidth, ctx.stage.clientHeight);
  let view = null; let field = null; let current = -1;
  const SHOT_BOX = { pos: [-0.2, 1.7, 1.25], target: [-0.1, 0.9, 0.2], fit: 1.5 };
  const SHOT_SLIDE = { pos: [0.52, 1.32, 1.02], target: [0.52, 0.84, 0.52], fit: 0.6 };

  function stepPick(i) {
    const s = set[i];
    return {
      title: `Take out: ${s.label}`, text: `Find the slide labelled <b>${s.label}</b> in the slide box and tap it.`, hint: 'Read the paper labels on the slides standing in the box.', tool: null, autoTool: 'hand', shot: SHOT_BOX,
      enter() { if (view) { view.dispose(); view = null; } },
      skip() { take(i, true); },
      handler: {
        down() {
          const h = input.pick(boxSlides); if (!h) return false;
          let o = h.object; while (o && o.userData.slide === undefined) o = o.parent;
          if (!o) return false;
          if (o.userData.slide !== i) { ctx.mistake(`That one is "${set[o.userData.slide].label}". You need "${s.label}".`, 2); return true; }
          sfx.play('pick'); take(i, false); return true;
        },
      },
    };
  }
  function take(i, instant) {
    current = i; const s = set[i];
    boxSlides[i].visible = false;
    st.slide.visible = true; st.slide.position.copy(home); st.slide.quaternion.identity(); st._slideFrom = null; st.slideParts = []; st.onStage = false; st.coverslip.visible = false;
    label.material.map = slideLabel(s.label); label.material.needsUpdate = true;
    specimen.material.color.setHex(s.stain);
    smudge.material.opacity = i === 0 ? 0.45 : 0;
    st.specimen = null; st.drop = null;
    if (!instant) { const to = home.clone(); st.slide.position.y += 0.3; anim.add(0.6, (k) => { st.slide.position.lerpVectors(st.slide.position, to, k); }, { done: () => { sfx.play('place'); ctx.next(); } }); }
  }
  let rubbed = 0; let lastP = null;
  const stepClean = {
    title: 'Wipe the slide clean', text: 'Fingerprints and dust spoil the image. Rub the slide gently with <b>lens paper</b>.', hint: 'Drag back and forth over the slide with the lens paper.', tool: 'paper', shot: SHOT_SLIDE,
    skip() { smudge.material.opacity = 0; },
    handler: {
      down(p) { if (!input.pick([st.slide])) return false; if (!ctx.requireTool('paper', 'Use soft <b>lens paper</b>, not your fingers.')) return true; lastP = [p.x, p.y]; tools.press(1); return true; },
      move(p) {
        if (!lastP) return; rubbed += Math.hypot(p.x - lastP[0], p.y - lastP[1]); lastP = [p.x, p.y];
        smudge.material.opacity = 0.45 * (1 - clamp(rubbed / 900)); ctx.progress(clamp(rubbed / 900));
        if (rubbed >= 900 && !this.done) { this.done = true; sfx.play('ok'); lastP = null; tools.press(0); ctx.next('Clean and clear.'); }
      },
      up() { lastP = null; tools.press(0); },
    },
  };
  function makeView(i) {
    if (view) return view;
    field = set[i].make();
    view = createScopeView(ctx, st, field, { objective: set[i].obj === 4 ? 4 : 10, focus: -600, onTap: (c, e) => { if (ctx.step && ctx.step.onTap) ctx.step.onTap(e); } });
    ctx.debug = { field, view };
    return view;
  }
  const eyeHandler = { down() { const h = input.pick(st.scope.pickables); if (h) { makeView(current).open(); return true; } return false; } };
  function stepFocus(i, high) {
    let sharpT = 0;
    const mag = high ? 40 : (set[i].obj === 4 ? 4 : 10);
    return {
      title: high ? 'Turn to high power (40×)' : `Focus under low power (${mag}×)`,
      text: high ? 'Centre an interesting area, click <b>40×</b> and sharpen with the <b>fine</b> knob only.' : 'Look in and focus with the <b>coarse</b> knob, then the <b>fine</b>.',
      hint: high ? 'The high-power lens is almost parfocal: a touch of the fine knob is all it needs.' : 'Drag the coarse knob up slowly until the image appears, then use fine.',
      tool: null, hideBelt: true, handler: eyeHandler,
      enter() { makeView(i).open(); sharpT = 0; },
      skip() { makeView(i); },
      update(dt) { const e = view && view.eye; if (!e) return; const s = e.state; ctx.progress(clamp(1 - s.blur / 10)); if (s.objective === mag && s.sharp) { sharpT += dt; if (sharpT > 0.6 && !this.done) { this.done = true; ctx.next(); } } else sharpT = 0; },
    };
  }
  function stepFind(i) {
    let k = 0;
    return {
      title: `Find the structures: ${set[i].label}`, text: '', tool: null, hideBelt: true, handler: eyeHandler,
      hint: 'Drag the field to search; switch objectives if you need to.',
      enter() { if (!view || !view.eye) makeView(i).open(); k = 0; this.prompt(); },
      prompt() { const f = field.find; if (k < f.length) { ui.setText(`Tap ${/stage$/.test(f[k]) || PHASE_INFO[f[k]] ? 'an example of' : 'the'} <b>${f[k]}</b>. (${k + 1} of ${f.length})`); ctx.progress(k / f.length); } },
      skip() { },
      onTap(e) {
        const f = field.find; if (k >= f.length) return;
        if (e.blur > 3) { ctx.say('Focus first.', 'hint', 1500); return; }
        const got = field.featureAt(e.x, e.y);
        const want = f[k];
        if (got === want) { sfx.play('ok'); view.eye.mark(e.x, e.y, want); ctx.say(NOTES[want] || PHASE_INFO[want] || want, 'good', 4200); ui.observe(want, 'seen'); k += 1; this.prompt(); if (k >= f.length) ctx.anim.wait(1.2, () => ctx.next()); }
        else ctx.mistake(got ? `That is ${/^[aeiou]/.test(got) ? 'an' : 'a'} ${got}. Look for the ${want}. ${NOTES[want] || PHASE_INFO[want] || ''}` : `Nothing there — find the ${want}.`, 2);
      },
    };
  }
  const steps = [];
  set.forEach((s, i) => {
    steps.push(stepPick(i));
    if (i === 0) steps.push(stepClean);
    steps.push(Object.assign(stepToStage(ctx, st, { shotStart: SHOT_SLIDE }), { title: 'Place the slide on the stage' }));
    steps.push(stepFocus(i, false));
    if (s.obj === 40) steps.push(stepFocus(i, true));
    steps.push(stepFind(i));
  });
  void fx; void tmp; void tmp2; void projectFn;
  return {
    tools: ['hand', 'paper'],
    steps,
    update(dt, t) { if (view) view.update(t); },
    result() {
      return {
        title: ctx.config.title,
        rows: set.map((s) => [s.label, 'studied']),
        conclusion: ctx.config.slug === 'frog-development-stages' ? 'Frog development: cleavage of the fertilised egg is holoblastic but unequal — small micromeres at the pigmented animal pole, large yolky macromeres below — giving the morula, the hollow blastula with its blastocoel near the animal pole, and the gastrula with a blastopore plugged by yolk.'
          : ctx.config.slug === 'grasshopper-animal-mitosis' ? 'In animal cells mitosis passes through the same stages as in plants, but there is no cell wall: spindles form from centrioles (asters) and the cytoplasm divides by a furrow pinching inward, not by a cell plate.'
            : ctx.config.slug === 'plant-tissue-diversity' ? 'Simple tissues — parenchyma, collenchyma, sclerenchyma — differ in wall thickening; complex tissues xylem and phloem conduct water and food; the epidermis protects, and its guard cells regulate gas exchange.'
              : 'Squamous epithelium is a single sheet of flat cells; striated muscle has long multinucleate fibres banded with dark A and light I bands; blood is a fluid tissue of red cells, five kinds of white cells and platelets in plasma.',
      };
    },
    dispose() { if (view) view.dispose(); },
  };
}
