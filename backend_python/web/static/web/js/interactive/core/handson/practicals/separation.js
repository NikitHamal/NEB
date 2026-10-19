// Separation techniques, each done by hand. Sand, salt and water: fold a filter paper into a cone,
// pour the mixture in without letting it rise over the paper (it drains at a rate set by its depth),
// then evaporate the filtrate and stop at the crystallisation point. Naphthalene and salt: heat
// under an inverted funnel until the naphthalene sublimes onto it. Salt water: set the thermometer
// bulb at the side arm, send the cooling water in at the lower nozzle, boil and collect pure water
// at 100 °C. Ink: spot it on a pencil line, stand the paper in solvent below the line, take it out
// before the front reaches the top and measure Rf.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { tripodWithGauze } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits, screenDist } from '../hud.js';
import { beaker } from '../glass.js';
import { bunsen } from '../burner.js';
import { filterFunnel, evaporatingDish, distillation, chromaPaper } from '../separation-kit.js';
import { thermometer } from '../thermo.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const DYES = [{ rf: 0.22, color: 'rgba(37,99,235,.95)', name: 'blue' }, { rf: 0.54, color: 'rgba(220,38,38,.9)', name: 'red' }, { rf: 0.81, color: 'rgba(234,179,8,.95)', name: 'yellow' }];

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  world.add(mesh(new THREE.BoxGeometry(10.6, 0.02, 2.8), MAT.matte(0x2f3640), [0.7, 0.01, 0]));
  // A: filtration and evaporation
  const AX = -3.4;
  const stand = new THREE.Group(); stand.position.set(AX, 0, 0); world.add(stand);
  stand.add(mesh(new THREE.BoxGeometry(0.6, 0.04, 0.5), MAT.matte(0x24323a), [-0.15, 0.02, 0])); stand.add(mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.6, 10), MAT.steel(), [-0.35, 0.8, 0]));
  stand.add(mesh(new THREE.TorusGeometry(0.26, 0.015, 6, 24), MAT.steel(), [0, 1.24, 0]).rotateX(Math.PI / 2));
  const fun = filterFunnel(); fun.group.position.set(AX, 0.63, 0); world.add(fun.group);
  const filtrate = beaker(0, 0xe8f2fa); filtrate.group.position.set(AX, 0, 0); world.add(filtrate.group);
  const mix = beaker(150, 0xb79b6b); mix.group.position.set(AX + 0.9, 0, 0.6); world.add(mix.group);
  const fpaper = mesh(new THREE.CircleGeometry(0.3, 30), MAT.paper(), [AX + 0.9, 0.012, -0.4]); fpaper.rotation.x = -Math.PI / 2; world.add(fpaper);
  const tri = tripodWithGauze(); tri.position.set(AX + 1.9, 0, 0); world.add(tri);
  const burnA = bunsen(ctx.quality); burnA.group.position.set(AX + 1.9, 0, 0); burnA.group.rotation.y = Math.PI / 2; world.add(burnA.group);
  const dish = evaporatingDish(); dish.group.position.set(AX + 1.9, 1.47, 0); world.add(dish.group); dish.set(0, 0);
  // B: sublimation
  const BX = -0.6;
  const tri2 = tripodWithGauze(); tri2.position.set(BX, 0, -0.3); world.add(tri2);
  const burnB = bunsen(ctx.quality); burnB.group.position.set(BX, 0, -0.3); burnB.group.rotation.y = Math.PI / 2; world.add(burnB.group);
  const sdish = evaporatingDish(); sdish.group.position.set(BX, 1.47, -0.3); world.add(sdish.group); sdish.set(0, 0.6);
  const sfun = mesh(new THREE.LatheGeometry([new THREE.Vector2(0.4, 0), new THREE.Vector2(0.38, 0.03), new THREE.Vector2(0.03, 0.45), new THREE.Vector2(0.03, 0.75)], 30), MAT.glass(), [BX, 1.5, -0.3], { cast: false }); world.add(sfun);
  const frostMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9, transparent: true, opacity: 0, side: THREE.DoubleSide });
  const frost = mesh(new THREE.LatheGeometry([new THREE.Vector2(0.36, 0.04), new THREE.Vector2(0.06, 0.42)], 30), frostMat, [BX, 1.5, -0.3], { cast: false }); world.add(frost);
  // C: distillation
  const CX = 0.9; const dist = distillation(); dist.group.position.set(CX, 0, -0.2); world.add(dist.group);
  const tri3 = tripodWithGauze(); tri3.position.set(CX, 0, -0.2); world.add(tri3);
  const burnC = bunsen(ctx.quality); burnC.group.position.set(CX, 0, -0.2); burnC.group.rotation.y = Math.PI / 2; world.add(burnC.group);
  const th = thermometer({ min: 0, max: 110, div: 1, len: 1.2 }); th.group.scale.setScalar(0.8); world.add(th.group); th.set(25, true);
  const BULB_OK = 2.3; let bulbY = 2.75;
  const placeTh = () => th.group.position.set(CX, bulbY - 0.08, -0.2);
  placeTh();
  // D: chromatography
  const DX = 4.9;
  const cjar = mesh(new THREE.CylinderGeometry(0.4, 0.4, 2.0, 30, 1, true), MAT.glass(), [DX, 1.0, 0], { cast: false }); world.add(cjar);
  const solvent = mesh(new THREE.CylinderGeometry(0.38, 0.38, 1, 26), MAT.liquid(0xe7f0f7, 0.45), null, { cast: false }); world.add(solvent); solvent.visible = false;
  const paper = chromaPaper(); paper.mesh.position.set(DX, 1.05, 0); world.add(paper.mesh); paper.draw({});
  world.add(mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.9, 8), MAT.matte(0x7a5a3a), [DX, 1.87, 0]).rotateZ(Math.PI / 2));

  const st = { folds: 0, inFunnel: false, pouring: false, pool: 0, filt: 0, mixLeft: 150, overflow: false, evap: 1, heatA: false, cryst: 0, sub: 0, heatB: false, water: false, heatC: false, T: 25, distil: 0, flaskT: 25, spot: false, depth: null, front: 0.12, running: false, removed: false, frontMark: false };
  const SHOT_A = shot({ pos: [AX + 0.8, 2.2, 3.0], target: [AX + 0.8, 0.9, 0], fit: 3.2, fitH: 2.6 });
  const SHOT_B = shot({ pos: [BX, 2.6, 2.6], target: [BX, 1.5, -0.3], fit: 1.8, fitH: 2.0 });
  const SHOT_C = shot({ pos: [CX + 1.3, 2.4, 4.0], target: [CX + 1.3, 1.4, -0.2], fit: 3.6, fitH: 3.0 });
  const SHOT_TH = shot({ pos: [CX + 0.3, 2.45, 1.0], target: [CX + 0.05, 2.3, -0.2], fit: 0.8, fitH: 0.8 });
  const SHOT_D = shot({ pos: [DX, 1.3, 2.6], target: [DX, 1.0, 0], fit: 1.8, fitH: 2.3 });
  const tChip = hud.chip('ho-chip-read'); tChip.dx = 16; tChip.dy = -20;

  function physics(dt) {
    if (st.pouring && st.mixLeft > 0) { const f = Math.min(st.mixLeft, 22 * dt); st.mixLeft -= f; mix.setVolume(st.mixLeft); st.pool += f / 900; if (Math.random() < dt * 3) sfx.play('pour'); }
    if (st.inFunnel && st.pool > 0) { const out = Math.min(st.pool, (0.006 + st.pool * 0.28) * dt); st.pool -= out; st.filt += out * 900 * 0.92; filtrate.setVolume(st.filt); }
    fun.setPool(st.pool); fun.residue.visible = st.mixLeft < 140 && st.inFunnel; fun.residue.scale.setScalar(Math.min(1, (150 - st.mixLeft) / 150) + 0.2);
    if (st.pool > 0.2 && !st.overflow) { st.overflow = true; ctx.mistake('The mixture rose above the top of the filter paper and ran down between the paper and the glass: sand gets into the filtrate. Pour slowly, down a glass rod, never above the paper.', 3); }
    if (st.heatA && st.evap > 0) { st.evap = Math.max(0, st.evap - dt * 0.05); if (st.evap < 0.3) st.cryst = Math.min(1, (0.3 - st.evap) / 0.25); dish.set(st.evap, st.cryst); if (st.evap === 0 && !st.spat) { st.spat = true; ctx.mistake('Heated to dryness: the salt spits out of the dish and the crystals are tiny. Stop at the crystallisation point and let the rest evaporate slowly.', 3); } }
    if (st.heatB) { st.sub = Math.min(1, st.sub + dt * 0.12); frostMat.opacity = 0.85 * st.sub; sdish.set(0, 0.6 * (1 - st.sub * 0.5)); }
    if (st.heatC) { st.flaskT = Math.min(101.2, st.flaskT + dt * 9); } else st.flaskT += (25 - st.flaskT) * dt * 0.05;
    const boiling = st.flaskT >= 100.8; const vapourT = boiling ? 100 : 25 + (st.flaskT - 25) * 0.3;
    const bulbT = bulbY < BULB_OK - 0.06 ? st.flaskT : bulbY > BULB_OK + 0.06 ? 25 + (vapourT - 25) * 0.6 : vapourT;
    th.set(bulbT); th.update(dt, 2);
    if (boiling && st.water) { st.distil += dt * 3; dist.setDistillate(st.distil); dist.setLevel(Math.max(0.2, 1 - st.distil / 120)); }
    if (st.running) { st.front = Math.min(0.97, st.front + dt * 0.035 * (1 - st.front)); paper.draw({ spot: true, front: st.front, wet: st.front, dyes: DYES.map((d) => Object.assign({}, d)) }); if (st.front > 0.95 && !st.lost) { st.lost = true; ctx.mistake('The solvent front reached the top of the paper: you can no longer measure how far it travelled, so Rf cannot be found. Remove the paper while the front is still below the top.', 3); } }
  }

  const steps = [
    {
      title: 'Plan: sand, salt and water', text: 'How do you get both the sand and the salt back?', shot: SHOT_A, hideBelt: true,
      enter() { anim.wait(0.6, () => ui.choose(ctx.stage.clientWidth / 2, 40, 'Sand + salt + water: separate by…', [{ label: 'Filtration, then evaporation', value: 1 }, { label: 'Evaporation, then filtration', value: 2 }, { label: 'Distillation only', value: 3 }, { label: 'Sublimation', value: 4 }], (v) => { if (v !== 1) ctx.mistake('Sand does not dissolve: filter it off first (residue). The salt is in the filtrate: evaporate the water to get it back.', 3); ctx.next(null, 0.4); })); },
      exit() { ui.clearChooser(); },
    },
    {
      title: 'Filtration', text: 'Tap the <b>filter paper</b> to fold it (in half, in half again, then open into a cone) and put it in the funnel. Then press and <b>hold</b> the beaker of muddy mixture to pour it in — never above the rim of the paper.', hint: 'Pour a little, let it drain, pour again.', shot: SHOT_A, hideBelt: true,
      skip() { st.inFunnel = true; fun.paper.visible = true; fpaper.visible = false; st.mixLeft = 0; mix.setVolume(0); st.filt = 130; filtrate.setVolume(130); st.pool = 0; },
      update() { if (st.inFunnel && st.mixLeft <= 0 && st.pool < 0.003 && !st.filtDone) { st.filtDone = true; ui.observe('Residue', 'sand on the filter paper'); ui.observe('Filtrate', `${Math.round(st.filt)} mL, clear salt solution`); ctx.next('Clear filtrate; the sand stays on the paper.', 0.8); } },
      handler: {
        down(p) {
          if (!st.inFunnel && hits(ctx, fpaper, p, 70)) { st.folds += 1; sfx.play('tear'); fpaper.scale.set(st.folds === 1 ? 1 : 0.6, st.folds === 1 ? 0.5 : 0.6, 1); if (st.folds >= 3) { st.inFunnel = true; fpaper.visible = false; fun.paper.visible = true; sfx.play('place'); ctx.say('A cone of filter paper, wetted so it sticks to the funnel.', 'info', 2000); } else ctx.say(st.folds === 1 ? 'Folded in half.' : 'Folded again.', 'info', 1200); return true; }
          if (hits(ctx, mix.group, p, 60, 0.4)) { if (!st.inFunnel) { ctx.say('Fit the filter paper first.', 'hint', 1600); return true; } st.pouring = true; mix.group.position.set(AX + 0.42, 1.0, 0); mix.group.rotation.z = 1.4; return true; }
          return false;
        },
        up() { if (st.pouring) { st.pouring = false; mix.group.position.set(AX + 0.9, 0, 0.6); mix.group.rotation.z = 0; } }, cancel() { this.up(); },
      },
    },
    {
      title: 'Evaporation', text: 'The filtrate is in the evaporating dish. Tap the <b>burner</b> to heat it. When crystals first appear at the edge, press <b>Stop heating</b>: the rest evaporates slowly to give good crystals.', shot: SHOT_A, hideBelt: true,
      enter() { filtrate.setVolume(0); st.evap = 1; dish.set(1, 0); hud.actions([{ id: 'stop', label: 'Stop heating', primary: true, onClick: () => { if (!st.heatA) return; st.heatA = false; burnA.setGas(0); if (st.cryst <= 0.02) { ctx.say('No crystals yet: keep heating until they start to appear.', 'hint', 2000); return; } ui.observe('Salt', st.spat ? 'spattered, fine powder' : 'crystals at the crystallisation point'); hud.actions([]); ctx.next('Salt crystals left to dry.', 0.8); } }]); },
      exit() { hud.actions([]); },
      skip() { st.evap = 0.2; st.cryst = 0.4; dish.set(0.2, 0.4); },
      handler: { down(p) { if (hits(ctx, burnA.group, p, 70, 0.6)) { st.heatA = true; burnA.setGas(1); burnA.light(); burnA.setAir(0.9); sfx.play('whoosh'); return true; } return false; } },
    },
    {
      title: 'Sublimation: naphthalene and salt', text: 'Tap the <b>burner</b> to warm the mixture gently under the inverted funnel. When white crystals have formed inside the funnel, <b>lift the funnel</b> to separate them.', hint: 'Naphthalene goes straight from solid to vapour and back on the cool funnel; salt does not.', shot: SHOT_B, hideBelt: true,
      enter() { hud.actions([{ id: 'lift', label: 'Lift the funnel', primary: true, onClick: () => { if (st.sub < 0.7) { ctx.say('Hardly any sublimate yet: keep warming.', 'hint', 1800); return; } st.heatB = false; burnB.setGas(0); anim.add(0.8, (k) => { sfun.position.y = frost.position.y = 1.5 + k * 0.6; }); ui.observe('Sublimate', 'naphthalene on the funnel; salt left in the dish'); hud.actions([]); ctx.next(null, 1); } }]); },
      exit() { hud.actions([]); },
      skip() { st.sub = 1; frostMat.opacity = 0.85; },
      handler: { down(p) { if (hits(ctx, burnB.group, p, 70, 0.6)) { st.heatB = true; burnB.setGas(1); burnB.light(); burnB.setAir(0.5); sfx.play('whoosh'); return true; } return false; } },
    },
    {
      title: 'Distillation of salt water', text: 'Set up first: drag the <b>thermometer</b> so its bulb is level with the <b>side arm</b>, and tap the condenser nozzle the cooling water should go <b>in</b> at. Then tap the <b>burner</b> and collect pure water.', hint: 'The bulb reads the vapour going over, so it sits at the side arm. Water in at the lower end, out at the top: the jacket stays full and counter-current.', shot: SHOT_C, hideBelt: true,
      enter() { hud.actions([{ id: 'look', label: 'Thermometer close-up', onClick: () => ctx.rig.go(SHOT_TH, 0.8) }, { id: 'all', label: 'Whole set', onClick: () => ctx.rig.go(SHOT_C, 0.8) }]); },
      exit() { hud.actions([]); tChip.show(false); },
      skip() { bulbY = BULB_OK; placeTh(); st.water = true; dist.jacket.material = MAT.liquid(0x9ec9ea, 0.5); st.distil = 30; dist.setDistillate(30); },
      update() {
        th.group.getWorldPosition(tChip.at); tChip.at.y += th.yOf(th.reading) * 0.8; tChip.set(`<b>${th.reading.toFixed(0)}</b> °C`); tChip.show(st.heatC);
        if (st.distil > 25 && !st.distDone) { st.distDone = true; ui.observe('Distillate', `pure water, boiling steadily at ${th.reading.toFixed(0)} °C`); ctx.next('Pure water collects in the receiver; the salt stays in the flask.', 1); }
      },
      handler: {
        down(p) {
          if (screenDist(ctx, th.group, p, 0.6) < 50 || ctx.input.pick([th.plate])) { st.dragTh = true; return true; }
          if (ctx.input.pick([dist.nozzleLow]) || screenDist(ctx, dist.nozzleLow, p) < 30) { setWater(true); return true; }
          if (ctx.input.pick([dist.nozzleHigh]) || screenDist(ctx, dist.nozzleHigh, p) < 30) { setWater(false); return true; }
          if (hits(ctx, burnC.group, p, 70, 0.6)) {
            if (!st.water) { ctx.mistake('No cooling water in the condenser: the steam would pour out of the receiver. Connect the water first.', 2); return true; }
            if (Math.abs(bulbY - BULB_OK) > 0.06) ctx.mistake(bulbY < BULB_OK ? 'The bulb is down in the flask: it reads the boiling solution, not the vapour going over.' : 'The bulb is above the side arm: the vapour reaches it late and it reads low.', 2);
            st.heatC = true; burnC.setGas(1); burnC.light(); burnC.setAir(0.9); sfx.play('whoosh'); return true;
          }
          return false;
        },
        move() { if (!st.dragTh) return; const pl = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0.2); const h = new THREE.Vector3(); if (ctx.input.ptr.ray.intersectPlane(pl, h)) { bulbY = THREE.MathUtils.clamp(h.y - BY + 0.05, 1.85, 2.9); placeTh(); } },
        up() { if (st.dragTh) { st.dragTh = false; const ok = Math.abs(bulbY - BULB_OK) <= 0.06; ctx.say(ok ? 'Bulb level with the side arm.' : 'Not yet level with the side arm.', ok ? 'good' : 'info', 1500); } }, cancel() { st.dragTh = false; },
      },
    },
    {
      title: 'Paper chromatography of ink', text: 'Tap the <b>paper</b> to put a small spot of ink on the pencil line. Choose the solvent depth, wait for it to climb, and press <b>Remove paper</b> before the front reaches the top.', hint: 'The pencil line and spot must stay above the solvent, or the ink just dissolves into the jar.', shot: SHOT_D, hideBelt: true,
      enter() { paper.draw({}); },
      exit() { hud.actions([]); ui.clearChooser(); },
      skip() { st.front = 0.82; st.removed = true; st.frontMark = true; paper.draw({ spot: true, front: 0.82, dyes: DYES, frontMark: true, wet: 0.82 }); },
      handler: { down(p) {
        if (st.spot || !hits(ctx, paper.mesh, p, 60)) return false;
        st.spot = true; sfx.play('drip'); paper.draw({ spot: true });
        anim.wait(0.5, () => ui.choose(ctx.stage.clientWidth / 2, 40, 'Pour solvent into the jar to a depth…', [{ label: 'Below the pencil line', value: 'below' }, { label: 'Above the pencil line', value: 'above' }], (v) => {
          st.depth = v; solvent.visible = true; const d = v === 'below' ? 0.14 : 0.32; solvent.scale.y = d; solvent.position.set(DX, d / 2, 0);
          if (v === 'above') { ctx.mistake('With the spot under the solvent the ink washes out into the jar instead of climbing the paper. The line must be above the solvent.', 3); solvent.scale.y = 0.14; solvent.position.y = 0.07; }
          st.running = true; hud.actions([{ id: 'rm', label: 'Remove paper', primary: true, onClick: removePaper }]);
        }));
        return true;
      } },
    },
  ];
  function setWater(lowIn) {
    if (!lowIn) { ctx.mistake('Water in at the top runs straight out of the lower nozzle and leaves the condenser half empty. Connect the supply to the lower nozzle.', 2); return; }
    st.water = true; sfx.play('pour'); dist.jacket.material = MAT.liquid(0x9ec9ea, 0.5); ui.say('Cooling water in at the bottom, out at the top.', 'good', 1800);
  }
  function removePaper() {
    if (st.front < 0.55) { ctx.say('The solvent has not risen far enough to separate the dyes yet.', 'hint', 1800); return; }
    st.running = false; st.removed = true; hud.actions([]); st.frontMark = true; paper.draw({ spot: true, front: st.front, dyes: DYES, frontMark: true, wet: st.front });
    const H = 16; const line = 0.12 * H; const front = st.front * H - line; const red = DYES[1].rf * front;
    ui.observe('Solvent front', `${front.toFixed(1)} cm from the line`);
    anim.wait(0.6, () => ui.choose(ctx.stage.clientWidth / 2, 40, `The red dye moved ${red.toFixed(1)} cm; the solvent ${front.toFixed(1)} cm. Rf (red) =`, [[DYES[1].rf, 'dye ÷ solvent'], [front / red, 'solvent ÷ dye'], [red / (st.front * H), 'dye ÷ paper height'], [red - front, 'difference']].map(([v, w]) => ({ label: `${v.toFixed(2)}  (${w})`, value: w })).sort(() => Math.random() - 0.5), (v) => {
      if (v !== 'dye ÷ solvent') ctx.mistake('Rf = distance moved by the dye ÷ distance moved by the solvent front, both from the pencil line. It is always less than 1.', 3);
      ui.observe('Rf', `blue ${DYES[0].rf}, red ${DYES[1].rf}, yellow ${DYES[2].rf}`); ctx.next('Three dyes in the ink.', 1);
    }));
  }

  ctx.debug = { st, setWater };
  return {
    tools: [], steps,
    update(dt, t) { physics(dt); [burnA, burnB, burnC].forEach((b) => b.update(dt, t)); hud.update(); },
    result() {
      return {
        title: 'Separation techniques',
        rows: [['Sand + salt + water', 'filtration, then evaporation'], ['Naphthalene + salt', 'sublimation'], ['Salt water → water', 'distillation (100 °C at the side arm)'], ['Ink', `chromatography, Rf ${DYES.map((d) => d.rf).join(', ')}`]],
        conclusion: 'Each method uses one difference: insolubility (filtration), a volatile solvent (evaporation), a solid that sublimes, different boiling points (distillation) and different attraction to the paper (chromatography). Technique decides the purity: a flooded filter, a dish boiled dry, a thermometer in the wrong place or a spot under the solvent each spoil the result.',
      };
    },
    dispose() { hud.dispose(); },
  };
}
