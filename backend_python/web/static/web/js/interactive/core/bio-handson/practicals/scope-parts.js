// The compound microscope: its parts and how to handle it. Carry it by the arm with a hand under
// the base, label every part on the instrument, set the light with the mirror, then focus on a
// newsprint letter "e" and discover that the image is upside down and reversed, and that it moves
// the opposite way to the slide.
import { THREE } from '../../engine.js';
import { buildStation, stepToStage, createScopeView } from '../slideprep.js';
import { createLabelQuiz } from '../labelquiz.js';
import { letterField } from '../fields/tissues.js';
import { ease, clamp } from '../kit.js';

const PARTS = {
  Eyepiece: 'Eyepiece (ocular): the lens you look into, usually 10×.',
  'Body tube': 'Body tube: holds the eyepiece and the objectives in line.',
  'Revolving nosepiece': 'Revolving nosepiece: turns to bring each objective over the specimen.',
  'Objective (40×)': 'Objectives: 4×, 10× and 40×, colour-banded; total magnification = eyepiece × objective.',
  Stage: 'Stage: the platform with a hole that holds the slide.',
  'Stage clips': 'Stage clips: hold the slide still.',
  Condenser: 'Condenser with iris diaphragm: focuses light on the specimen and controls how much.',
  Mirror: 'Mirror: plane on one side, concave on the other; reflects light up through the condenser.',
  'Coarse adjustment': 'Coarse adjustment: moves the stage a lot — for low power only.',
  'Fine adjustment': 'Fine adjustment: tiny movements for sharp focus, especially at high power.',
  Arm: 'Arm (limb): carry the microscope by it, with the other hand under the base.',
  Base: 'Base (foot): the heavy horseshoe that keeps it steady.',
};

export function create(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const st = buildStation(ctx, { tileX: 0.1, tileZ: 0.35, slideDX: 0.42, scopeX: 0.2, scopeZ: -0.25, scopeRot: -0.25 });
  const scope = st.scope;
  ctx.surfaces.push(st.tile);
  st.coverslip.visible = false;
  // a printed letter on the slide
  const print = new THREE.Mesh(new THREE.PlaneGeometry(0.1, 0.1), new THREE.MeshBasicMaterial({ color: 0x111111, transparent: true, opacity: 0.85 }));
  print.rotation.x = -Math.PI / 2; print.position.set(0, 0.0128, 0); print.scale.set(0.3, 0.3, 1); st.slide.add(print);
  st.slideParts = [];
  let quiz = null; let view = null; let field = null;
  const SHOT_SCOPE = { pos: [2.3, 2.75, 1.9], target: [0.2, 1.8, -0.25], fit: 1.8, fitH: 3.7 };

  const r = scope.root;
  const w = (x, y, z, o = r) => ({ at: new THREE.Vector3(x, y, z), object: o });
  const anchors = {
    Eyepiece: w(0, 0.1, 0, scope.eyepiece), 'Body tube': w(0, 2.45, 0.03), 'Revolving nosepiece': w(0, 1.98, -0.08),
    'Objective (40×)': w(0, -0.3, 0, scope.objectives[2]), Stage: w(0.4, 0.05, -0.3, scope.stage), 'Stage clips': w(0.3, 0.09, 0.05, scope.stage),
    Condenser: w(0, -0.1, 0.09, scope.stage), Mirror: w(0, 0.62, 0.1), 'Coarse adjustment': w(0.18, 1.05, 0.48), 'Fine adjustment': w(-0.25, 1.05, 0.48),
    Arm: w(0, 1.5, 0.62), Base: w(0.5, 0.08, -0.3),
  };

  let carry = 0;
  const stepCarry = {
    title: 'Carry it correctly', text: 'How should a microscope be carried to the bench?', tool: null, autoTool: 'hand', hideBelt: true, shot: SHOT_SCOPE,
    enter() {
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, 60, 'Carry the microscope…', [{ label: 'By the arm, one hand under the base, upright', value: 'ok' }, { label: 'By the body tube, with one hand', value: 'tube' }, { label: 'By the stage, tilted', value: 'stage' }], (v) => {
        if (v === 'ok') {
          sfx.play('ok');
          const y0 = r.position.y; anim.add(1.2, (k) => { r.position.y = y0 + Math.sin(Math.PI * k) * 0.35; r.rotation.y = -0.25 + Math.sin(Math.PI * k) * 0.15; }, { ease: ease.inOut, done: () => ctx.next('Upright, by the arm, a hand under the base — so the eyepiece cannot slide out and the mirror cannot swing.') });
        } else { ctx.mistake('The eyepiece can drop out of the tube and the instrument can slip. Hold the arm, support the base, keep it upright.', 3); anim.wait(0.4, ask); }
      });
      anim.wait(0.8, ask); void carry;
    },
    exit() { ui.clearChooser(); },
  };
  const stepLabel = {
    title: 'Name the parts', text: 'Drag each name onto its part of the microscope.', hint: 'Lenses at the top, the stage in the middle, the knobs on the arm, the mirror and base at the bottom.', tool: null, hideBelt: true, autoTool: 'hand', shot: SHOT_SCOPE,
    enter() {
      quiz = createLabelQuiz(ctx, Object.keys(PARTS).map((name) => ({ name, at: anchors[name].at, object: anchors[name].object, fact: PARTS[name] })), {
        radius: 40, onPlace: (it, n, t) => ctx.progress(n / t), onDone: () => anim.wait(0.8, () => ctx.next('Every part named.')),
      });
    },
    update() { if (quiz) quiz.update(); },
    skip() { },
    exit() { if (quiz) { quiz.dispose(); quiz = null; } },
  };
  const stepLight = {
    title: 'Set the light', text: 'Turn the low-power objective in, open the diaphragm, and tilt the <b>mirror</b> toward the window until the field is evenly bright. Drag the mirror.', hint: 'Drag up or down on the mirror under the stage.', tool: null, autoTool: 'hand', shot: { pos: [0.75, 1.35, 1.55], target: [0.2, 0.85, -0.25], fit: 1.0 },
    enter() { this.angle = 0; },
    skip() { },
    handler: {
      down(p) { const h = input.pick([r]); if (!h) return false; let o = h.object; let isMirror = false; while (o) { if (o === scope.mirror) isMirror = true; o = o.parent; } if (!isMirror) { ctx.say('That is not the mirror — it hangs below the stage.', 'hint', 2000); return true; } stepLight.drag = p.y; return true; },
      move(p) {
        if (stepLight.drag === undefined || stepLight.drag === null) return;
        const d = p.y - stepLight.drag; stepLight.drag = p.y; stepLight.angle = clamp(stepLight.angle + d * 0.01, -0.8, 0.8);
        scope.mirrorDisc.rotation.x = -0.75 + stepLight.angle;
        const bright = 1 - Math.abs(stepLight.angle - 0.45) / 1.2; ctx.progress(bright);
        if (bright > 0.93 && !stepLight.done) { stepLight.done = true; stepLight.drag = null; sfx.play('ok'); ctx.next('A bright, even circle of light: the mirror now throws window light up through the condenser.'); }
      },
      up() { stepLight.drag = null; },
    },
  };
  const stepStage = stepToStage(ctx, st, { shotStart: { pos: [0.52, 1.32, 1.02], target: [0.52, 0.84, 0.52], fit: 0.6 }, text: 'Tap the slide with a printed letter “e” to lay it on the stage, the right way up as you read it.' });
  function makeView() {
    if (view) return view;
    field = letterField();
    view = createScopeView(ctx, st, field, { objective: 4, focus: -400 });
    ctx.debug = { field, view };
    return view;
  }
  const eyeHandler = { down() { const h = input.pick(scope.pickables); if (h) { makeView().open(); return true; } return false; } };
  let sharpT = 0;
  const stepFocus = {
    title: 'Focus on the letter', text: 'Look in and focus at 4× with the coarse, then the fine knob.', tool: null, hideBelt: true, handler: eyeHandler,
    enter() { makeView().open(); sharpT = 0; },
    skip() { makeView(); },
    update(dt) { const e = view && view.eye; if (!e) return; const s = e.state; ctx.progress(clamp(1 - s.blur / 10)); if (s.sharp) { sharpT += dt; if (sharpT > 0.6 && !this.done) { this.done = true; ctx.next(); } } else sharpT = 0; },
  };
  const stepImage = {
    title: 'What does the image look like?', text: 'Compare the letter you see with the letter on the slide.', tool: null, hideBelt: true, handler: eyeHandler,
    enter() {
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, 70, 'The image of “e” is…', [{ label: 'Upright, as on the slide', value: 'up' }, { label: 'Upside down and reversed left–right', value: 'inv' }, { label: 'Only magnified, mirror-reversed', value: 'mir' }], (v) => {
        if (v === 'inv') { ui.observe('Image', 'inverted, laterally reversed, virtual, magnified'); ctx.next('The compound microscope forms a magnified, virtual image that is inverted and laterally reversed (rotated 180°). Move the slide left and the image moves right.'); }
        else { ctx.mistake('Look at the tail of the “e” — where is it compared with the slide?', 3); anim.wait(0.4, ask); }
      });
      anim.wait(0.8, ask);
    },
    exit() { ui.clearChooser(); },
  };
  const stepMag = {
    title: 'Total magnification', text: 'With the 10× eyepiece and the 40× objective, what is the total magnification?', tool: null, hideBelt: true, handler: eyeHandler,
    enter() {
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, 70, 'Total magnification', [{ label: '50×', value: 50 }, { label: '400×', value: 400 }, { label: '4000×', value: 4000 }, { label: '40×', value: 40 }], (v) => {
        if (v === 400) { ui.observe('Total magnification', '10 × 40 = 400×'); ctx.next('Total magnification = eyepiece × objective = 10 × 40 = 400×.'); }
        else { ctx.mistake('Multiply the two: eyepiece magnification × objective magnification.', 2); anim.wait(0.4, ask); }
      });
      anim.wait(0.6, ask);
    },
    exit() { ui.clearChooser(); },
  };
  return {
    tools: ['hand'],
    steps: [stepCarry, stepLabel, stepLight, stepStage, stepFocus, stepImage, stepMag],
    update(dt, t) { if (view) view.update(t); },
    result() { return { title: 'Compound microscope', rows: [['Parts named', String(Object.keys(PARTS).length)], ['Image', 'inverted, reversed'], ['Highest power', '400×']], conclusion: 'A compound microscope magnifies in two stages — objective, then eyepiece — so the total magnification is their product. It is carried by the arm with the base supported, focused at low power with the coarse knob, and at high power with the fine knob only. Its image is magnified, virtual, inverted and laterally reversed.' }; },
    dispose() { if (view) view.dispose(); if (quiz) quiz.dispose(); },
  };
}
