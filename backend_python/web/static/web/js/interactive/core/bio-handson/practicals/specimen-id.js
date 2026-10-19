// Identifying specimens with a dichotomous key — plants (bacteria to angiosperms and lichen) or
// animals (Amoeba to the frog). Six specimens come to the turntable one by one. The student turns
// each round and looks closely (hand lens), or puts a slide under the microscope for the
// micro-organisms, then works through the key couplet by couplet; a wrong turn is explained by the
// character the student misread. The record lists each specimen, its group and the reasons.
import { THREE } from '../../engine.js';
import { VEG, VEG_KEY } from '../specimens/vegkey.js';
import { ANIM, ANIM_KEY } from '../specimens/animkey.js';
import { createLens } from '../lens.js';
import { sheet, table, tag, esc } from '../bench.js';
import { mesh, MAT, rng, clamp, ease } from '../kit.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });

function pathTo(key, id) {
  const walk = (node, acc) => { if (node === id) return acc; const n = key[node]; if (!n) return null; return walk(n.a[1], acc.concat([[node, 'a']])) || walk(n.b[1], acc.concat([[node, 'b']])); };
  return walk(key.start, []);
}

export function create(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const animals = ctx.config.slug.startsWith('animal');
  const DATA = animals ? ANIM : VEG; const KEY = animals ? ANIM_KEY : VEG_KEY;
  const R = rng(window.__bhSeed || (Date.now() & 0xffff) || 19);
  const ids = Object.keys(DATA); const micro = ids.filter((k) => DATA[k].micro); const macro = ids.filter((k) => !DATA[k].micro);
  const pick = [...micro.sort(() => R() - 0.5).slice(0, 2), ...macro.sort(() => R() - 0.5).slice(0, 4)].sort(() => R() - 0.5);
  const lens = createLens(ctx, { mag: 2.6, groundY: ctx.BENCH_Y + 0.12 });
  const table0 = new THREE.Group(); world.add(table0);
  const turn = new THREE.Group(); turn.position.set(0, 0, 0.2); table0.add(turn);
  turn.add(mesh(new THREE.CylinderGeometry(0.75, 0.8, 0.06, 40), MAT.gloss(0x1f2937), [0, 0.03, 0]));
  const top = new THREE.Group(); top.position.y = 0.06; turn.add(top);
  top.add(mesh(new THREE.CylinderGeometry(0.72, 0.72, 0.012, 40), MAT.matte(0xf1f5f9), [0, 0.006, 0]));
  const shelf = new THREE.Group(); world.add(shelf);
  const built = pick.map((id, i) => { const g = DATA[id].build(); g.visible = false; g.userData.id = id; world.add(g); return g; });
  const res = []; let sh = null; let inset = null;
  const TT = S([0.3, 1.45, 2.0], [0, 0.25, 0.2], 1.9, 1.2);

  function showInset(id) {
    inset = document.createElement('div'); inset.className = 'bh-inset';
    inset.innerHTML = `<div class="bh-inset-lens"></div><span>${esc(DATA[id].scale)}</span>`;
    const c = document.createElement('canvas'); c.width = c.height = 360; c.className = 'bh-inset-img'; DATA[id].micro(c); inset.querySelector('.bh-inset-lens').appendChild(c);
    ui.root.appendChild(inset); requestAnimationFrame(() => inset.classList.add('show'));
  }
  function hideInset() { if (inset) { inset.remove(); inset = null; } }
  function specStep(g, k) {
    const id = g.userData.id; const D = DATA[id]; const path = pathTo(KEY, id);
    let phase = 'look'; let turned = 0; let node = KEY.start; let trail = []; let micro = null;
    return {
      title: `Specimen ${k + 1}`, text: D.micro ? 'A prepared slide. Tap it to examine it under the microscope.' : `Drag sideways to turn the specimen right round, and use the <b>hand lens</b> to look closely. <small>(${esc(D.scale)})</small>`,
      tool: null, autoTool: 'hand', shot: TT,
      enter() {
        built.forEach((b) => { if (b !== g && !b.userData.done) b.visible = false; }); g.visible = true; top.add(g); g.position.set(0, 0.012, 0); g.rotation.set(0, 0, 0);
        const box = new THREE.Box3().setFromObject(g); const sz = box.getSize(new THREE.Vector3()); const f = Math.min(1, 1.25 / Math.max(sz.x, sz.z, 0.01), 1.2 / Math.max(sz.y, 0.01)); g.scale.setScalar(f);
        phase = 'look'; turned = 0; node = KEY.start; trail = [];
      },
      skip() { finish(true); },
      exit() { hideInset(); if (sh) { sh.remove(); sh = null; } },
      handler: {
        down(p) {
          if (phase !== 'look' || ui.tool === 'lens') return false;
          if (D.micro) { if (!input.pick([g], true)) return false; sfx.play('click'); openKey(); return true; }
          this.x = p.x; return true;
        },
        move(p) { if (this.x === undefined || D.micro) return; const dx = p.x - this.x; this.x = p.x; top.rotation.y += dx * 0.012; turned += Math.abs(dx * 0.012); ctx.progress(clamp(turned / 3)); if (turned > 3 && phase === 'look') openKey(); },
        up() { this.x = undefined; },
      },
    };
    function openKey() {
      if (phase !== 'look') return; phase = 'key'; sfx.play('ok');
      sh = sheet(ctx, { title: 'Dichotomous key', cls: 'wide' });
      if (D.micro) { micro = document.createElement('canvas'); micro.width = micro.height = 360; micro.className = 'bh-key-micro'; D.micro(micro); }
      render();
    }
    function render() {
      const n = KEY[node];
      sh.set(`${micro ? `<div class="bh-key-mwrap"></div><small>${esc(D.scale)}</small>` : ''}<div class="bh-key"><div class="path">${trail.map((t) => esc(t)).join(' → ') || 'Start at couplet 1.'}</div><b>${node}. ${esc(n.q)}</b><button type="button" data-c="a">${esc(n.a[0])}</button><button type="button" data-c="b">${esc(n.b[0])}</button></div>`);
      if (micro) sh.body.querySelector('.bh-key-mwrap').appendChild(micro);
      sh.body.querySelectorAll('button').forEach((b) => b.addEventListener('click', () => choose(b.dataset.c)));
    }
    function choose(c) {
      const step = path.find((q) => q[0] === node); const right = step ? step[1] : null;
      if (c !== right) { ctx.mistake(`Look at the specimen again: ${D.reasons}. So “${KEY[node][right][0]}” is the right lead here.`, 2); return; }
      sfx.play('click'); trail.push(KEY[node][c][0]); const nx = KEY[node][c][1];
      if (KEY[nx]) { node = nx; render(); return; }
      finish(false);
    }
    function finish(instant) {
      res.push([k + 1, D.name, D.group, D.reasons]); ui.observe(`${k + 1}. ${D.name}`, D.group);
      g.userData.done = true;
      const slot = new THREE.Vector3(-2.6 + k * 1.05, 0, -0.9);
      const settle = () => { shelf.attach(g); g.position.copy(slot); g.rotation.set(0, 0, 0); g.scale.multiplyScalar(0.55); const t = tag(D.name.split(' (')[0], { h: 0.06 }); t.position.set(slot.x, 0.65, slot.z + 0.25); shelf.add(t); };
      if (instant) { settle(); return; }
      ctx.say(`<b>${D.name}</b> — ${D.group}: ${D.reasons}.`, 'good', 6000);
      hideInset(); if (sh) { sh.remove(); sh = null; }
      world.attach(g); const from = g.position.clone(); const to = slot.clone(); const s0 = g.scale.x;
      anim.add(1.0, (q) => { g.position.lerpVectors(from, to, q); g.position.y += Math.sin(Math.PI * q) * 0.5; g.scale.setScalar(s0 * (1 - 0.45 * q)); }, { ease: ease.inOut, done: () => { const t = tag(D.name.split(' (')[0], { h: 0.06 }); t.position.set(slot.x, 0.65, slot.z + 0.25); shelf.add(t); ctx.next(); } });
    }
  }
  const stepSum = {
    title: 'Record of identification', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0, 2.2, 3.4], [-0.2, 0.3, -0.4], 5.6),
    enter() { sh = sheet(ctx, { title: 'Identification record', cls: 'wide' }); sh.set(table(['No.', 'Specimen', 'Group', 'Reasons'], res.map(([n, a, b, c]) => [n, a, b, `<small>${esc(c)}</small>`]))); anim.wait(0.5, () => ctx.next(null, 6)); },
    exit() { if (sh) { sh.remove(); sh = null; } },
  };
  const steps = [...built.map((g, k) => specStep(g, k)), stepSum];
  ctx.debug = { pick, built, top };
  return {
    tools: ['hand', 'lens'],
    steps,
    update() { lens.update(); },
    result() { return { title: animals ? 'Animal specimens identified' : 'Plant specimens identified', rows: res.map(([n, a, b]) => [`${n}. ${a}`, b]), conclusion: animals ? 'Animals are classified by their organisation and body plan: single-celled Protozoa; radially symmetrical Cnidaria and Echinodermata; and bilateral invertebrates told apart by segmentation, jointed legs, shells and body shape (flatworms, roundworms, annelids, arthropods, molluscs), up to vertebrates with a backbone (fish, amphibians…).' : 'Plants and plant-like organisms are classified by their organisation: prokaryotic bacteria and cyanobacteria; algae and fungi (thallophytes), the lichens that combine them; bryophytes without vascular tissue; pteridophytes with vascular tissue but spores; and seed plants — gymnosperms with naked seeds and angiosperms with seeds in fruits, divided into monocots and dicots.' }; },
    dispose() { lens.dispose(); hideInset(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}
