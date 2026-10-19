// Heat of neutralization in a polystyrene cup. The student pours 1.0 M HCl into a measuring
// cylinder (held press = pouring, a dropper for the last drops), reads the meniscus, empties it
// into the cup, rinses the cylinder, measures 1.0 M NaOH into a beaker, reads both starting
// temperatures, pours the alkali in, puts the lid on and stirs while a live temperature-time graph
// grows, and catches the peak. Heat is released as the solutions mix and slowly lost through the
// cup (faster without the lid). ΔH = −mcΔT/n from the student's readings; then ethanoic acid.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { reagentBottle, washBottle } from '../../bio-handson/props.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { beaker } from '../glass.js';
import { createGraph } from '../stopwatch.js';
import { thermometer, thermoReader, foamCup } from '../thermo.js';
import { measuringCylinder, createPour } from '../vessels.js';

const BY = 0.8; const C = 4.18; const CUP = 6; const DH = { strong: -57.3, weak: -56.1 };
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'Temperature after mixing', xLabel: 'time (s)', yLabel: 'T (°C)' });
  graph.el.classList.add('ho-side');
  const ROOM = Math.round((22 + Math.random() * 4) * 10) / 10;
  const TA = Math.round((ROOM + (Math.random() - 0.5) * 0.8) * 10) / 10; const TBASE = Math.round((ROOM + (Math.random() - 0.5) * 0.8) * 10) / 10;

  const cup = foamCup(); cup.group.position.set(0.3, 0, 0); world.add(cup.group); cup.lid.position.set(0.9, 0, 0.7); cup.lid.visible = true;
  const th = thermometer({ min: 0, max: 50, div: 0.2, len: 2.5 }); th.group.position.set(0.3, 0.08, 0); world.add(th.group); th.set(ROOM, true);
  const rd = thermoReader(ctx, th);
  const stirrer = mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.6, 8), MAT.glassEdge(), [0.42, 0.85, 0.08], { cast: false }); world.add(stirrer);
  const bottles = {
    hcl: reagentBottle('HCl', 0xf1f7ff, '1.0 M'), naoh: reagentBottle('NaOH', 0xf3f8ff, '1.0 M'), ch3: reagentBottle('CH₃COOH', 0xf4f7ff, '1.0 M'),
  };
  [['hcl', -2.0], ['naoh', -1.4], ['ch3', -0.8]].forEach(([k, x]) => { const b = bottles[k]; b.scale.setScalar(1.25); b.position.set(x, 0, -0.9); world.add(b); });
  const cyl = measuringCylinder(); cyl.group.position.set(-1.0, 0, 0.55); world.add(cyl.group);
  const reader = cyl.reader(ctx);
  const bk = beaker(0, 0xf3f8ff); bk.group.scale.setScalar(1.2); bk.group.position.set(1.6, 0, 0.4); world.add(bk.group); const BKS = 1.2 ** 3;
  const wash = washBottle(); wash.position.set(-2.2, 0, 0.7); world.add(wash);

  const st = { stage: 'hcl', acidKind: 'strong', mixing: false, t: 0, released: 0, n: 0.05, T: ROOM, Tmix0: ROOM, lid: false, stir: 0, pts: [], peak: 0, rinsed: false, readV: null, readTruth: null, vols: {}, Ta: null, Tb: null, T2: null, res: {} };
  const Ctot = () => (cup.volume) * C + CUP;
  const pours = {};
  function bottlePour(k) {
    const b = bottles[k];
    pours[k] = createPour(ctx, { vessel: b, lipAt: () => new THREE.Vector3(-1.0, cyl.topY + 0.25, 0.55), tilt: -1.9, lip: new THREE.Vector3(0.06, 0.55, 0), id: `p-${k}`, flow: (dt) => { cyl.set(cyl.volume + 9 * dt); if (Math.random() < dt * 3) sfx.play('pour'); }, targetY: () => cyl.levelY() });
  }
  ['hcl', 'naoh', 'ch3'].forEach(bottlePour);
  const cylToCup = createPour(ctx, { vessel: cyl.group, lipAt: () => (st.target === targets.cup ? new THREE.Vector3(0.25, 1.4, 0) : new THREE.Vector3(1.5, 1.35, 0.4)), tilt: -2.0, lip: new THREE.Vector3(0, cyl.topY, 0), id: 'cyl', flow: (dt) => { const f = Math.min(cyl.volume, 60 * dt); cyl.set(cyl.volume - f); st.target.add(f); return cyl.volume > 0.05; }, targetY: () => st.target.y() });
  const bkToCup = createPour(ctx, { vessel: bk.group, lipAt: () => new THREE.Vector3(0.4, 1.4, 0), tilt: 2.0, lip: new THREE.Vector3(-0.27, 0.9, 0), id: 'bk', flow: (dt) => { const left = bk.volume * BKS; const f = Math.min(left, 50 * dt); bk.setVolume((left - f) / BKS); cup.setVolume(cup.volume + f); if (left - f <= 0.05) { startMix(); return false; } return true; }, targetY: () => cup.levelY() });
  const targets = { cup: { add: (f) => cup.setVolume(cup.volume + f), y: () => cup.levelY() }, beaker: { add: (f) => bk.setVolume(bk.volume + f / BKS), y: () => 0.1 } };
  st.target = targets.cup;

  // ---- measuring ----
  function measureStep(k, into, title) {
    const name = { hcl: '1.0 M HCl', naoh: '1.0 M NaOH', ch3: '1.0 M CH₃COOH' }[k];
    return {
      title, text: `Press and <b>hold</b> the <b>${name}</b> bottle to pour into the measuring cylinder; let go to stop. Bring it to exactly <b>50.0 mL</b> with the dropper, then tap the scale at the <b>bottom of the meniscus</b> and record.`,
      hint: 'Stop pouring a few mL short of the mark, then add drops. Read with your eye level with the meniscus.', shot: SHOT_CYL, hideBelt: true,
      enter() {
        st.readV = null; cyl.material.color.set(0xeef5fb);
        hud.actions([{ id: 'drop', label: '+ drop', onClick: () => { cyl.set(cyl.volume + 0.25); sfx.play('drip'); } }, { id: 'back', label: 'Pour 1 mL back', onClick: () => { cyl.set(cyl.volume - 1); sfx.play('pour'); } }, { id: 'rec', label: 'Record', primary: true, disabled: true, onClick: () => {
          const v = cyl.volume;
          if (Math.abs(st.readV - v) > 0.5) { ctx.mistake(`The bottom of the meniscus is at ${v.toFixed(1)} mL, not ${st.readV.toFixed(1)} mL.`, 3); return; }
          if (Math.abs(v - 50) > 0.5) { ctx.say(`${v.toFixed(1)} mL: bring it to 50.0 mL first.`, 'hint', 2200); return; }
          st.vols[k] = st.readV; ui.observe(`V (${k === 'naoh' ? 'NaOH' : k === 'hcl' ? 'HCl' : 'CH₃COOH'})`, `<b>${st.readV.toFixed(1)} mL</b>`); hud.actions([]); reader.hide();
          st.target = targets[into]; ctx.rig.go(SHOT_ALL, 1.0); cylToCup.start(); anim.wait(2.6, () => cylToCup.stop(() => ctx.next(null, 0.2)));
        } }]);
      },
      exit() { hud.actions([]); reader.hide(); Object.values(pours).forEach((p) => p.stop()); },
      skip() { st.vols[k] = 50; targets[into].add(50); cyl.set(0); },
      update(dt) { pours[k].update(dt); cylToCup.update(dt); },
      handler: {
        down(p) {
          if (hits(ctx, bottles[k], p, 50, 0.3)) { pours[k].start(); return true; }
          for (const o of Object.keys(bottles)) if (o !== k && hits(ctx, bottles[o], p, 40, 0.3)) { ctx.mistake(`That is the ${o === 'naoh' ? 'NaOH' : o === 'hcl' ? 'HCl' : 'ethanoic acid'} bottle. Read the label.`, 2); return true; }
          const v = reader.tap(); if (v !== null) { st.readV = v; hud.relabel('rec', `Record ${v.toFixed(1)} mL`); hud.enable('rec', true); sfx.play('click'); return true; }
          return false;
        },
        up() { pours[k].stop(); }, cancel() { pours[k].stop(); },
      },
    };
  }

  // ---- temperatures ----
  function readTemp(label, done) {
    st.readV = null; const at = th.group.position; const y = at.y + th.yOf(th.reading);
    ctx.rig.go(shot({ pos: [at.x + 0.1, y + 0.02, at.z + 0.6], target: [at.x, y, at.z], fov: 22, limits: { yaw: 0.3, pitch: 0.2, zMin: 0.6, zMax: 1.5 } }), 1.0);
    hud.actions([{ id: 'rec', label: `Record ${label}`, primary: true, disabled: true, onClick: () => {
      if (Math.abs(st.readV - st.readTruth) > 0.16) { ctx.mistake(`The column stands at ${st.readTruth.toFixed(1)} °C, not ${st.readV.toFixed(1)} °C.`, 3); return; }
      rd.hide(); hud.actions([]); done(st.readV, st.readTruth);
    } }]);
  }
  const tapRead = () => { const v = rd.tap(); if (v === null) return false; st.readV = v; st.readTruth = th.reading; hud.relabel('rec', `Record ${v.toFixed(1)} °C`); hud.enable('rec', true); sfx.play('click'); return true; };
  function moveThermo(to) { const from = th.group.position.clone(); anim.add(0.9, (k) => { th.group.position.lerpVectors(from, to, k); th.group.position.y += Math.sin(k * Math.PI) * 0.8; }); }

  // ---- mixing ----
  function startMix() {
    st.mixing = true; st.t = 0; st.released = 0; st.pts = []; st.peak = 0;
    const va = cup.volume - 50; st.Tmix0 = (va * st.Ta0 + 50 * st.Tb0) / (va + 50); st.T = st.Tmix0;
    hud.actions([{ id: 'lid', label: 'Lid on', onClick: () => { st.lid = !st.lid; hud.relabel('lid', st.lid ? 'Lid off' : 'Lid on'); cup.lid.position.set(st.lid ? 0.3 : 0.9, st.lid ? 1.12 : 0, st.lid ? 0 : 0.7); sfx.play('place'); } }, { id: 'stir', label: 'Stir', onClick: stir }, { id: 'rd', label: 'Read T₂', primary: true, onClick: () => readTemp('T₂', onPeak) }]);
    graph.show(true);
  }
  function stir() { st.stir = 2.5; sfx.play('glass'); anim.add(0.5, (k) => { stirrer.position.y = 0.85 + Math.sin(k * Math.PI) * 0.3; }, { id: 'stir' }); }
  function onPeak(v, truth) {
    if (st.peak - truth > 0.25) ctx.mistake(`The highest temperature was ${st.peak.toFixed(1)} °C; you read it after it had begun to fall.`, 3);
    else if (st.released < 0.9) { ctx.say('Still rising: stir and wait for the highest reading.', 'hint', 2200); startMixBar(); return; }
    if (!st.lid) ctx.say('Without the lid the cup loses heat faster, so the peak comes out low.', 'hint', 3000);
    st.T2 = v; graph.show(false); ui.observe(`T₂ (${st.acidKind === 'strong' ? 'HCl' : 'CH₃COOH'})`, `<b>${v.toFixed(1)} °C</b>`); ctx.next(null, 0.3);
  }
  function startMixBar() { hud.actions([{ id: 'lid', label: st.lid ? 'Lid off' : 'Lid on', onClick: () => { st.lid = !st.lid; hud.relabel('lid', st.lid ? 'Lid off' : 'Lid on'); cup.lid.position.set(st.lid ? 0.3 : 0.9, st.lid ? 1.12 : 0, st.lid ? 0 : 0.7); } }, { id: 'stir', label: 'Stir', onClick: stir }, { id: 'rd', label: 'Read T₂', primary: true, onClick: () => readTemp('T₂', onPeak) }]); ctx.rig.go(SHOT_MIX, 0.8); }
  function physics(dt) {
    st.stir = Math.max(0, st.stir - dt);
    if (st.mixing) {
      st.t += dt; const tau = st.stir > 0 ? 1.5 : 5; const df = (1 - st.released) * (1 - Math.exp(-dt / tau)); st.released += df;
      const q = -DH[st.acidKind] * 1000 * st.n * df; st.T += q / Ctot();
      st.T -= (st.T - ROOM) * dt / (st.lid ? 900 : 240);
      th.set(st.T); if (Math.floor(st.t) > st.pts.length - 1) { st.pts.push([st.t, th.reading]); graph.draw(st.pts, null, { xMax: Math.max(60, st.t * 1.15), yMin: Math.floor(st.Tmix0 - 1), yMax: Math.ceil(st.Tmix0 + 9) }); }
      st.peak = Math.max(st.peak, th.reading);
    }
    th.update(dt, st.stir > 0 ? 1.0 : 2.5);
  }

  const SHOT_ALL = shot({ pos: [-0.3, 2.6, 5.2], target: [-0.3, 0.9, 0], fit: 5.2, fitH: 3.2 });
  const SHOT_CYL = shot({ pos: [-1.2, 2.0, 3.2], target: [-1.3, 1.1, 0], fit: 2.6, fitH: 2.6 });
  const SHOT_MIX = shot({ pos: [0.9, 2.2, 3.6], target: [0.7, 1.1, 0.2], fit: 2.8, fitH: 2.6 });

  function tempsStep(kind) {
    return {
      title: kind === 'strong' ? 'Starting temperatures' : 'Ethanoic acid: starting temperatures', text: 'Read the temperature of the <b>acid in the cup</b>; then the thermometer is rinsed, dried and put in the <b>alkali</b>: read that too. T₁ is their mean.', shot: SHOT_MIX, hideBelt: true,
      enter() {
        th.set(TA); anim.wait(1.2, () => readTemp('acid', (v) => {
          st.Ta = v; ui.observe('T (acid)', `${v.toFixed(1)} °C`); moveThermo(new THREE.Vector3(1.6, 0.06, 0.4)); th.set(TBASE);
          anim.wait(2.5, () => readTemp('alkali', (w) => { st.Tb = w; st.T1 = (st.Ta + st.Tb) / 2; ui.observe('T (alkali)', `${w.toFixed(1)} °C`); ui.observe('T₁ (mean)', `<b>${st.T1.toFixed(2)} °C</b>`); moveThermo(new THREE.Vector3(0.3, 0.08, 0)); ctx.next(null, 0.6); }));
        }));
      },
      exit() { hud.actions([]); rd.hide(); },
      skip() { st.Ta = TA; st.Tb = TBASE; st.T1 = (TA + TBASE) / 2; th.group.position.set(0.3, 0.08, 0); },
      handler: { down() { return tapRead(); } },
    };
  }
  function mixStep(kind) {
    return {
      title: 'Mix, stir and catch the peak', text: 'Tap the <b>beaker</b> to pour the alkali into the cup all at once, put the <b>lid</b> on, <b>stir</b>, and watch the graph. Read T₂ at the highest point.', hint: 'The temperature climbs for a few seconds, levels off and then creeps down. The peak is T₂.', shot: SHOT_MIX, hideBelt: true,
      enter() { st.acidKind = kind; st.Ta0 = TA; st.Tb0 = TBASE; st.lid = false; cup.lid.position.set(0.9, 0, 0.7); },
      exit() { hud.actions([]); graph.show(false); rd.hide(); st.mixing = false; },
      skip() { st.acidKind = kind; const T = st.T1 + (-DH[kind] * 1000 * 0.05) / (100 * C + CUP); st.T2 = Math.round(T * 0.9985 * 10) / 10; cup.setVolume(100); bk.setVolume(0); },
      update(dt) { bkToCup.update(dt); },
      handler: { down(p) { if (!st.mixing && !bkToCup.on && bk.volume > 1 && hits(ctx, bk.group, p, 60, 0.4)) { bkToCup.start(); return true; } if (st.mixing) return tapRead(); return false; } },
    };
  }
  function calcStep(kind) {
    return {
      title: kind === 'strong' ? 'ΔH of neutralization' : 'Strong against weak', text: 'q = m c ΔT, with m = 100 g of solution and c = 4.18 J g⁻¹ °C⁻¹; n = 0.050 mol of water formed.', shot: SHOT_ALL, hideBelt: true,
      enter() {
        const dT = st.T2 - st.T1; const q = 100 * C * dT; const dH = -q / 1000 / 0.05; st.res[kind] = { dT, dH };
        ui.observe(`ΔT (${kind === 'strong' ? 'HCl' : 'CH₃COOH'})`, `${dT.toFixed(1)} °C`);
        if (kind === 'weak') { ui.observe('ΔH (CH₃COOH)', `<b>${dH.toFixed(1)} kJ mol⁻¹</b>`); anim.wait(0.6, () => ui.choose(ctx.stage.clientWidth / 2, 50, `Ethanoic acid gives ${dH.toFixed(1)} kJ mol⁻¹, against ${st.res.strong.dH.toFixed(1)} for HCl. Why less heat?`, [{ label: 'Some heat is used to ionise the weak acid', value: 1 }, { label: 'Ethanoic acid has fewer H atoms', value: 0 }, { label: 'The reaction is slower', value: 2 }], (v) => { if (v !== 1) ctx.mistake('A weak acid is mostly un-ionised: part of the heat released is used up ionising it (CH₃COOH → CH₃COO⁻ + H⁺), so less is left over.', 3); ctx.next(null, 1); })); return; }
        const opts = [[dH, '−mcΔT / n'], [-q / 1000 / 0.1, 'n = 0.10 mol'], [-(50 * C * dT) / 1000 / 0.05, 'm = 50 g'], [q / 1000 / 0.05, '+mcΔT / n']].map(([v, w]) => ({ label: `${v.toFixed(1)} kJ mol⁻¹  (${w})`, value: w })).sort(() => Math.random() - 0.5);
        anim.wait(0.6, () => ui.choose(ctx.stage.clientWidth / 2, 50, `ΔT = ${dT.toFixed(1)} °C. ΔH(neutralization) =`, opts, (v) => {
          if (v !== '−mcΔT / n') ctx.mistake('ΔH = −mcΔT/n: both 50 mL portions are heated (100 g), 0.050 mol of water forms, and the sign is negative because heat is given out.', 3);
          ui.observe('ΔH (HCl)', `<b>${dH.toFixed(1)} kJ mol⁻¹</b>`); ctx.next(null, 1);
        }));
      },
      exit() { ui.clearChooser(); },
    };
  }
  function weakReset() { cup.setVolume(50); bk.setVolume(50 / BKS); th.group.position.set(0.3, 0.08, 0); st.T = ROOM; th.set(TA, true); }

  const steps = [
    measureStep('hcl', 'cup', 'Measure the acid'),
    {
      title: 'Rinse the cylinder', text: 'Before measuring the alkali, rinse the cylinder: tap the <b>wash bottle</b>.', shot: SHOT_CYL, hideBelt: true,
      enter() { hud.actions([{ id: 'go', label: 'Go on without rinsing', onClick: () => { ctx.mistake('Acid left wetting the cylinder would neutralise some of the alkali before the experiment: rinse it first.', 2); ctx.next(null, 0.3); } }]); },
      exit() { hud.actions([]); },
      handler: { down(p) { if (!hits(ctx, wash, p, 60, 0.4)) return false; sfx.play('pour'); cyl.set(8); anim.wait(0.8, () => { cyl.set(0); sfx.play('pour'); ctx.next('Rinsed with distilled water.', 0.4); }); return true; } },
    },
    measureStep('naoh', 'beaker', 'Measure the alkali'),
    tempsStep('strong'),
    mixStep('strong'),
    calcStep('strong'),
    {
      title: 'Now a weak acid', text: 'The cup is washed and 50.0 mL of <b>1.0 M ethanoic acid</b> is measured in, with fresh NaOH in the beaker. Repeat the readings.', shot: SHOT_ALL, hideBelt: true,
      enter() { weakReset(); bottles.ch3.position.y = 0.0; hud.actions([{ id: 'ok', label: 'Ready', primary: true, onClick: () => { hud.actions([]); ctx.next(null, 0.2); } }]); },
      exit() { hud.actions([]); }, skip() { weakReset(); },
    },
    tempsStep('weak'),
    mixStep('weak'),
    calcStep('weak'),
  ];

  ctx.debug = { st, th, cyl, cup, startMix };
  return {
    tools: [], steps,
    update(dt) { physics(dt); hud.update(); },
    result() {
      const s = st.res.strong || { dH: 0, dT: 0 }; const w = st.res.weak || { dH: 0, dT: 0 };
      const err = (s.dH - DH.strong) / Math.abs(DH.strong) * 100;
      return {
        title: 'Heat of neutralization',
        rows: [['ΔT (HCl + NaOH)', `${s.dT.toFixed(1)} °C`], ['ΔH (HCl + NaOH)', `${s.dH.toFixed(1)} kJ mol⁻¹`], ['Accepted', '−57.3 kJ mol⁻¹'], ['Difference', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`], ['ΔT (CH₃COOH + NaOH)', `${w.dT.toFixed(1)} °C`], ['ΔH (CH₃COOH + NaOH)', `${w.dH.toFixed(1)} kJ mol⁻¹`]],
        conclusion: 'For a strong acid and a strong base the only reaction is H⁺ + OH⁻ → H₂O, about −57 kJ per mole of water. The cup itself and the air take a little of the heat, so the measured value is slightly smaller. Ethanoic acid gives less because part of the energy is spent ionising the weak acid.',
      };
    },
    dispose() { hud.dispose(); graph.dispose(); Object.values(pours).forEach((p) => p.dispose()); cylToCup.dispose(); bkToCup.dispose(); },
  };
}
