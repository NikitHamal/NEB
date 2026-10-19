// Identifying inflorescences. Six fresh specimens stand in water vials. For each one the student
// finds the oldest flower (tap it — with the hand lens if needed), which reveals the order of
// opening; decides racemose (indefinite: acropetal or centripetal) or cymose (definite: the main
// axis ends in the oldest flower, basipetal); and names the type. A summary table closes it.
import { THREE } from '../../engine.js';
import { buildInflorescence, TYPES } from '../specimens/inflor.js';
import { createLens } from '../lens.js';
import { ask, sheet, table, tag } from '../bench.js';
import { mesh, MAT, rng } from '../kit.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const ORDER = ['raceme', 'umbel', 'cyme', 'spike', 'capitulum', 'corymb'];

export function create(ctx) {
  const { world, input, anim, sfx, ui, fx } = ctx;
  const R = rng((Date.now() & 0xffff) || 3);
  const order = ORDER.slice().sort(() => R() - 0.5);
  const lens = createLens(ctx, { mag: 2.5, groundY: ctx.BENCH_Y + 1.0 });
  const specs = order.map((k, i) => {
    const x = -2.5 + i * 1.0; const vial = new THREE.Group(); vial.position.set(x, 0, 0); world.add(vial);
    vial.add(mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.4, 16, 1, true), MAT.glass(), [0, 0.2, 0], { cast: false }));
    vial.add(mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.25, 16), MAT.liquid(0xcfe8f5, 0.4), [0, 0.13, 0], { cast: false }));
    vial.add(mesh(new THREE.CylinderGeometry(0.16, 0.18, 0.04, 20), MAT.gloss(0x334155), [0, 0.02, 0]));
    const inf = buildInflorescence(k, 11 + i); inf.group.position.set(0, 0.1, 0); vial.add(inf.group);
    const t = tag(String(i + 1), { h: 0.1 }); t.position.set(0, -0.0 + 0.55, 0.25); vial.add(t);
    return { k, x, vial, inf, done: false };
  });
  const res = [];
  const ALL = S([0, 2.4, 4.2], [0, 0.85, 0], 6.4, 2.6);
  function specStep(sp, i) {
    let phase = 'oldest';
    const T = TYPES[sp.k];
    const shot = S([sp.x + 0.12, 2.15, 1.45], [sp.x, 0.95, 0], 1.0, 1.55);
    return {
      title: `Specimen ${i + 1}`, text: 'Tap the <b>oldest</b> flower (a fruit or fading flower if there is one; use the hand lens to look closely). The order of opening tells the type.', tool: null, autoTool: 'hand', shot,
      enter() { phase = 'oldest'; },
      skip() { res.push([i + 1, T.name, T.group, T.eg]); ui.observe(`${i + 1}. ${T.eg}`, T.name); },
      handler: { down() {
        if (phase !== 'oldest' || ui.tool === 'lens') return false;
        const h = input.pick(sp.inf.units, true); if (!h) return false; let o = h.object; const root = o.userData.unitRoot || o; const age = root.userData.age ?? 0;
        const max = Math.max(...sp.inf.units.map((u) => u.userData.age ?? 0));
        if (age < max) { ctx.mistake(age === 0 ? 'That is an unopened bud — one of the youngest.' : 'There are older flowers (or young fruits) than that one. Look where the fruits are forming.', 1); return true; }
        phase = 'group'; sfx.play('ok'); const wp = new THREE.Vector3(); root.getWorldPosition(wp); fx.burst(wp, 0xfacc15, 6, 0.06, wp.y - 0.05);
        const where = sp.k === 'cyme' ? 'at the tip of the main axis (it ends in a flower)' : ['umbel', 'corymb', 'capitulum'].includes(sp.k) ? 'on the outside, younger toward the centre' : 'at the base, younger toward the tip';
        ctx.say(`Oldest ${where}.`, 'good', 3000);
        ask(ctx, 'So this inflorescence is…', [{ label: 'Racemose (axis keeps growing; acropetal / centripetal)', value: 'racemose' }, { label: 'Cymose (axis ends in a flower; basipetal / centrifugal)', value: 'cymose' }], T.group, {
          delay: 0.3, wrong: 'If the oldest flower ends the main axis, growth is definite (cymose). If the axis tip still has buds or the centre is youngest, it is racemose.',
          then() {
            const pool = T.group === 'cymose' ? ['Dichasial cyme', 'Monochasial cyme', 'Raceme', 'Umbel'] : ['Raceme', 'Spike', 'Umbel', 'Corymb', 'Capitulum (head)'];
            ask(ctx, 'Its type is…', pool.map((v) => ({ label: v, value: v })), T.name, { delay: 0.2, ok: `${T.note} Example: ${T.eg}.`, wrong: (v) => (v === 'Spike' ? 'Are the flowers stalked or not?' : v === 'Raceme' ? 'Look again: do the flowers come off an elongated axis or from one point?' : 'Compare the length of the pedicels and where the flowers arise.'),
              then() { res.push([i + 1, T.name, T.group, T.eg]); ui.observe(`${i + 1}. ${T.eg}`, T.name); ctx.next(); } });
          },
        });
        return true;
      } },
      exit() { ui.clearChooser(); },
    };
  }
  let sh = null;
  const stepSum = {
    title: 'Racemose or cymose?', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: ALL,
    enter() {
      sh = sheet(ctx, { title: 'Inflorescences identified', cls: 'wide' });
      sh.set(table(['No.', 'Specimen', 'Type', 'Group'], res.map(([n, name, grp, eg]) => [n, eg, name, grp])));
      ask(ctx, 'The basic difference between racemose and cymose inflorescences is…', [{ label: 'Racemose: the main axis grows indefinitely; cymose: it ends in a flower', value: 'ok' }, { label: 'Racemose flowers are always stalked', value: 's' }, { label: 'Cymose flowers are always white', value: 'w' }], 'ok', { y: 0.06, ok: 'In racemose inflorescences the growing point keeps producing flowers, so the oldest are at the base or outside (acropetal / centripetal). In cymose ones the apex is used up in a flower, new flowers come from lateral branches below it, so the oldest is at the tip or centre (basipetal / centrifugal).', wrong: 'Spikes and capitula are racemose with sessile flowers. Think about the growing point.' });
    },
    exit() { ui.clearChooser(); if (sh) { sh.remove(); sh = null; } },
  };
  const steps = [...specs.map((sp, i) => specStep(sp, i)), stepSum];
  ctx.debug = { specs };
  return {
    tools: ['hand', 'lens'],
    steps,
    update() { lens.update(); },
    result() { return { title: 'Inflorescence identification', rows: res.map(([n, name, grp, eg]) => [`${n}. ${eg}`, `${name} (${grp})`]), conclusion: 'An inflorescence is identified from its branching and the order in which its flowers open. Racemose types — raceme, spike, umbel, corymb, capitulum — have an indefinitely growing axis with the oldest flowers at the base or periphery; cymose types end the axis in the first flower, the younger ones arising from lateral branches beneath it.' }; },
    dispose() { lens.dispose(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}
