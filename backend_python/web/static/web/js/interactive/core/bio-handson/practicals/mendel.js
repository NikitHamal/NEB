// Mendelian inheritance with real seeds. A tray of F2 pea seeds from a round × wrinkled cross (and
// then from round-yellow × wrinkled-green) is sorted by phenotype into dishes: pick a dish, then
// tap each seed that belongs in it (a wrong one is caught). The counts are the student's own and
// vary from run to run, as real seed samples do; they are tested against 3:1 and 9:3:3:1 with
// chi-square, and the monohybrid cross is explained with a Punnett square built by hand.
import { THREE } from '../../engine.js';
import { enamelTray, ask, sheet, table, chipDrop, tag } from '../bench.js';
import { petriDish } from '../props.js';
import { mesh, wet, rng, ease } from '../kit.js';
import { createLens } from '../lens.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const YEL = 0xe6c34a; const GRN = 0x9bbf4a;

function seedGeos() {
  const round = new THREE.SphereGeometry(0.036, 16, 12); round.userData.shared = true;
  const wr = [0, 1, 2].map((k) => {
    const g = new THREE.SphereGeometry(0.034, 18, 14); const p = g.attributes.position; const v = new THREE.Vector3(); const R = rng(77 + k);
    const bumps = Array.from({ length: 12 }, () => new THREE.Vector3(R() - 0.5, R() - 0.5, R() - 0.5).normalize());
    for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const n = v.clone().normalize(); let d = 0; bumps.forEach((b) => { d += Math.max(0, n.dot(b) - 0.45) * 0.6; }); const f = 1 - d * 0.75 + Math.sin(n.x * 19 + n.y * 15) * 0.06 + Math.sin(n.z * 23) * 0.04; v.multiplyScalar(f); p.setXYZ(i, v.x, v.y * 0.85, v.z); }
    g.computeVertexNormals(); g.userData.shared = true; return g;
  });
  return { round, wr };
}
const chi = (obs, ratio) => { const n = obs.reduce((a, b) => a + b, 0); const sum = ratio.reduce((a, b) => a + b, 0); const exp = ratio.map((r) => n * r / sum); return { exp, terms: obs.map((o, i) => (o - exp[i]) ** 2 / exp[i]), chi2: obs.reduce((a, o, i) => a + (o - exp[i]) ** 2 / exp[i], 0) }; };

export function create(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const R = rng((Date.now() & 0xffff) || 21);
  const geos = seedGeos();
  const mats = { RY: wet(YEL, { roughness: 0.5, clearcoat: 0.5 }), WY: wet(0xd8b542, { roughness: 0.75, clearcoat: 0.1 }), RG: wet(GRN, { roughness: 0.5, clearcoat: 0.5 }), WG: wet(0x8eae44, { roughness: 0.75, clearcoat: 0.1 }) };
  const hud = createHud(ctx);
  const lens = createLens(ctx, { mag: 2.6, groundY: ctx.BENCH_Y + 0.05 });
  const tray = enamelTray(1.3, 0.8); tray.position.set(0, 0, 0.15); world.add(tray);
  const trayTag = tag('F₂ seeds', { h: 0.08 }); trayTag.position.set(0, 0.25, -0.3); world.add(trayTag);
  let seeds = []; let dishes = []; let active = null; let phase = 'mono'; let handSorted = 0; let sh = null; let dz = null;
  const counts = { mono: null, di: null };

  function makeSeeds(n, di) {
    seeds.forEach((s) => world.remove(s.m)); seeds = [];
    for (let i = 0; i < n; i++) {
      // F2 of a heterozygous self: each gene segregates 3 : 1 independently
      const round = R() < 0.75; const yellow = di ? R() < 0.75 : true;
      const key = `${round ? 'R' : 'W'}${yellow ? 'Y' : 'G'}`;
      const m = mesh(round ? geos.round : geos.wr[i % 3], mats[key]);
      const col = i % 8; const row = Math.floor(i / 8); const rows = Math.ceil(n / 8);
      m.position.set(-0.5 + col * 0.143 + (R() - 0.5) * 0.04, 0.055, 0.15 - (rows - 1) * 0.055 + row * 0.11 + (R() - 0.5) * 0.03);
      m.rotation.set(R() * 6, R() * 6, R() * 6); world.add(m);
      seeds.push({ m, round, yellow, key, sorted: null });
    }
  }
  function makeDishes(defs) {
    dishes.forEach((d) => world.remove(d.g)); dishes = [];
    defs.forEach(([key, label], i) => {
      const g = new THREE.Group(); const x = (i - (defs.length - 1) / 2) * 0.62; g.position.set(x, 0, 0.95); world.add(g);
      const pd = petriDish(0xf8fafc); pd.scale.setScalar(0.62); g.add(pd);
      const t = tag(label, { h: 0.075 }); t.position.set(0, 0.2, 0.3); g.add(t);
      const ring = mesh(new THREE.TorusGeometry(0.3, 0.012, 8, 40), new THREE.MeshBasicMaterial({ color: 0x22c55e }), [0, 0.05, 0]); ring.rotation.x = Math.PI / 2; ring.visible = false; g.add(ring);
      dishes.push({ g, key, label, n: 0, ring, t });
    });
  }
  function setActive(d) { active = d; dishes.forEach((x) => { x.ring.visible = x === d; }); if (d) sfx.play('click'); }
  function fits(s, d) { if (d.key.length === 1) return d.key === (s.round ? 'R' : 'W'); return d.key === s.key; }
  function sendTo(s, d, instant) {
    s.sorted = d; d.n += 1; const k = d.n - 1; const a = k * 2.4; const r = 0.035 * Math.sqrt(k);
    const to = new THREE.Vector3(d.g.position.x + Math.cos(a) * Math.min(0.22, r), 0.03 + Math.floor(k / 36) * 0.035, d.g.position.z + Math.sin(a) * Math.min(0.22, r));
    if (instant) { s.m.position.copy(to); return; }
    const from = s.m.position.clone(); sfx.play('pick');
    anim.add(0.45, (q) => { s.m.position.lerpVectors(from, to, q); s.m.position.y += Math.sin(Math.PI * q) * 0.15; }, { ease: ease.inOut, done: () => sfx.play('drop') });
  }
  function tally() { return dishes.map((d) => `<span><i style="background:${d.key.includes('G') ? '#9bbf4a' : '#e6c34a'}"></i>${d.label}: <b>${d.n}</b></span>`).join(''); }
  function sortStep(title, text, defs, n, di) {
    const s = {
      title, text, tool: null, autoTool: 'hand', hint: 'Tap a dish (it gets a green ring), then tap every seed of that kind. Use the hand lens if you are unsure about a seed\'s surface.',
      shot: S([0, 2.0, 2.3], [0, 0.0, 0.5], di ? 2.7 : 1.9, 1.5),
      enter() {
        phase = di ? 'di' : 'mono'; makeSeeds(n, di); makeDishes(defs); setActive(null); handSorted = 0;
        dz = { set: (h) => ui.setText(`${text}${h}`), remove() {} }; dz.set(`<div class="bh-tally">${tally()}</div>`);
        hud.actions([]);
      },
      exit() { setActive(null); if (dz) { dz.remove(); dz = null; } hud.actions([]); },
      skip() { if (!seeds.length || seeds[0].di !== di) { makeSeeds(n, di); makeDishes(defs); } seeds.forEach((q) => { if (!q.sorted) sendTo(q, dishes.find((d) => fits(q, d)), true); }); done(true); },
      handler: {
        down() {
          const dh = dishes.find((d) => input.pick([d.g], true)); if (dh) { setActive(dh); return true; }
          const h = input.pick(seeds.filter((q) => !q.sorted).map((q) => q.m)); if (!h) return false;
          if (ctx.ui.tool === 'lens') return false;
          const sd = seeds.find((q) => q.m === h.object);
          if (!active) { ctx.say('First tap the dish this seed belongs in.', 'hint', 1800); return true; }
          if (!fits(sd, active)) {
            const what = `${sd.round ? 'round, smooth' : 'wrinkled'}${di ? `, ${sd.yellow ? 'yellow' : 'green'}` : ''}`;
            ctx.mistake(`That seed is <b>${what}</b> — it does not belong in “${active.label}”.`, 1); return true;
          }
          sendTo(sd, active, false); handSorted += 1; dz.set(`<div class="bh-tally">${tally()}</div>`);
          const left = seeds.filter((q) => !q.sorted).length; ctx.progress(1 - left / n);
          if (handSorted === 16 && left > 0) hud.actions([{ id: 'rest', label: 'Partner sorts the rest', onClick() { seeds.forEach((q) => { if (!q.sorted) sendTo(q, dishes.find((d) => fits(q, d)), false); }); hud.actions([]); anim.wait(0.8, () => { dz.set(`<div class="bh-tally">${tally()}</div>`); done(); }); } }]);
          if (!left) anim.wait(0.6, done);
          return true;
        },
      },
    };
    function done(skipping) { if (s.fin) return; s.fin = true; const c = dishes.map((d) => d.n); counts[di ? 'di' : 'mono'] = c; dishes.forEach((d) => ui.observe(d.label, String(d.n))); if (!skipping) ctx.next(`Counted: ${dishes.map((d) => `${d.label} ${d.n}`).join(', ')}.`); }
    return s;
  }
  function chiStep(di) {
    return {
      title: di ? 'Chi-square against 9 : 3 : 3 : 1' : 'Chi-square against 3 : 1', text: '', tool: null, autoTool: 'hand', hideBelt: true,
      shot: S([0, 2.0, 2.4], [0, 0.0, 0.5], 2.0),
      enter() {
        const obs = counts[di ? 'di' : 'mono']; const ratio = di ? [9, 3, 3, 1] : [3, 1]; const c = chi(obs, ratio); const crit = di ? 7.815 : 3.841;
        const names = di ? ['Round yellow', 'Round green', 'Wrinkled yellow', 'Wrinkled green'] : ['Round', 'Wrinkled'];
        sh = sheet(ctx, { title: `χ² test (df = ${ratio.length - 1}, 5% level: ${crit})`, cls: 'wide' });
        sh.set(table(['Phenotype', 'O', 'E', '(O−E)²/E'], names.map((nm, i) => [nm, obs[i], c.exp[i].toFixed(1), c.terms[i].toFixed(3)]).concat([['Total', obs.reduce((a, b) => a + b, 0), '', '<b>?</b>']])));
        const right = Math.round(c.chi2 * 100) / 100;
        const wrongs = [Math.round(c.terms[0] * 100) / 100, Math.round((c.chi2 + 1.7) * 100) / 100, Math.round(obs.reduce((a, o, i) => a + Math.abs(o - c.exp[i]), 0) / 1 * 100) / 100];
        const opts = [right, ...wrongs].filter((v, i, a) => a.indexOf(v) === i).sort(() => R() - 0.5);
        ask(ctx, 'χ² = Σ (O − E)² / E =', opts.map((v) => ({ label: v.toFixed(2), value: v })), right, {
          y: 0.06, wrong: 'Add up the last column: every (O − E)² / E term.',
          then() {
            sh.set(sh.body.innerHTML.replace('<b>?</b>', `<b>${right.toFixed(2)}</b>`));
            const fitsR = right < crit;
            ask(ctx, `χ² = ${right.toFixed(2)}; critical value ${crit}. So…`, [{ label: 'The data fit the ratio (difference due to chance)', value: true }, { label: 'The data do not fit the ratio', value: false }], fitsR, {
              delay: 0.3, y: 0.06,
              ok: fitsR ? `${right.toFixed(2)} < ${crit}: the deviation is small enough to be chance at the 5% level — the seeds follow ${di ? '9 : 3 : 3 : 1' : '3 : 1'}.` : `${right.toFixed(2)} > ${crit}: an unusually lopsided sample. With a larger sample the ratio would normally emerge.`,
              wrong: `Compare χ² with the critical value: below ${crit} means the difference could be due to chance.`,
            });
            ui.observe(di ? 'χ² (9:3:3:1)' : 'χ² (3:1)', right.toFixed(2));
          },
        });
      },
      exit() { ui.clearChooser(); if (sh) { sh.remove(); sh = null; } },
    };
  }
  const stepPunnett = {
    title: 'Explain it with a Punnett square', text: 'The F₁ plants were all <b>Rr</b> (round). Drag each genotype into the cells for the F₁ × F₁ cross (or tap a chip, then a cell).',
    tool: null, autoTool: 'hand', hideBelt: true, shot: S([0, 2.0, 2.4], [0, 0.0, 0.5], 2.0),
    enter() {
      sh = sheet(ctx, { title: 'Rr × Rr', cls: 'wide' });
      const cell = (a, b) => `<td><div class="bh-slot" data-slot="${[a, b].sort().join('')}" style="min-width:60px">?</div></td>`;
      sh.set(`<table class="bh-tab"><tr><th>♀ \\ ♂</th><th>R</th><th>r</th></tr><tr><th>R</th>${cell('R', 'R')}${cell('R', 'r')}</tr><tr><th>r</th>${cell('r', 'R')}${cell('r', 'r')}</tr></table><div class="bh-dtray"></div>`);
      const trayEl = sh.body.querySelector('.bh-dtray'); let placed = 0;
      const chips = ['RR', 'Rr', 'Rr', 'rr'].map((g, i) => ({ id: `${g}:${i}`, html: g }));
      this.dz = chipDrop(ctx, trayEl, chips, sh.body, (id, slot, chip, slotEl) => {
        const g = id.split(':')[0]; const want = slot === 'RR' ? 'RR' : slot === 'rr' ? 'rr' : 'Rr';
        if (slotEl.dataset.done) return false;
        if (g !== want) { ctx.mistake(`The gametes in that cell give <b>${want}</b>, not ${g}.`, 1); return false; }
        slotEl.dataset.done = '1'; slotEl.textContent = ''; slotEl.appendChild(chip); placed += 1;
        if (placed === 4) anim.wait(0.5, () => ask(ctx, 'Phenotypes from this square', [{ label: '3 round : 1 wrinkled', value: 'ok' }, { label: '1 round : 2 : 1 wrinkled', value: 'g' }, { label: 'All round', value: 'a' }], 'ok', { delay: 0.2, y: 0.06, ok: 'RR and Rr are both round (R is dominant), rr is wrinkled: genotypes 1 : 2 : 1, phenotypes 3 : 1. The two alleles separated into different gametes — the law of segregation.', wrong: '1 : 2 : 1 is the genotype ratio. Round is dominant, so how many cells look round?' }));
        return true;
      });
    },
    exit() { ui.clearChooser(); if (this.dz) this.dz.dispose(); if (sh) { sh.remove(); sh = null; } },
  };
  const stepLaw = {
    title: 'What the dihybrid ratio shows', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: S([0, 2.0, 2.4], [0, 0.0, 0.5], 2.0),
    enter() { ask(ctx, 'A 9 : 3 : 3 : 1 ratio in the F₂ shows that…', [{ label: 'Seed shape and colour genes assort independently', value: 'ok' }, { label: 'Shape and colour are always inherited together', value: 'l' }, { label: 'Green is dominant over yellow', value: 'g' }], 'ok', { ok: 'Independent assortment: each F₁ plant (RrYy) makes RY, Ry, rY and ry gametes equally, so the 3 : 1 for shape and the 3 : 1 for colour combine as (3 : 1) × (3 : 1) = 9 : 3 : 3 : 1, with two new combinations (round green, wrinkled yellow).', wrong: 'Linked genes would give mostly parental combinations. Here the new combinations appear in the proportions expected by chance.' }); },
    exit() { ui.clearChooser(); },
  };
  const steps = [
    sortStep('Sort the F₂ seeds by shape', 'These seeds came from F₁ plants (round × wrinkled) that self-pollinated. Tap the <b>Round</b> or <b>Wrinkled</b> dish, then tap each seed of that kind.', [['R', 'Round'], ['W', 'Wrinkled']], 40, false),
    chiStep(false), stepPunnett,
    sortStep('Sort a dihybrid F₂', 'Now F₂ seeds from round-yellow × wrinkled-green. Sort them into the four phenotype dishes.', [['RY', 'Round yellow'], ['RG', 'Round green'], ['WY', 'Wrinkled yellow'], ['WG', 'Wrinkled green']], 48, true),
    chiStep(true), stepLaw,
  ];
  ctx.debug = { get seeds() { return seeds; }, get dishes() { return dishes; } };
  void phase;
  return {
    tools: ['hand', 'lens'],
    steps,
    update() { lens.update(); hud.update(); },
    result() {
      const m = counts.mono || [0, 0]; const d = counts.di || [0, 0, 0, 0]; const cm = chi(m, [3, 1]); const cd = chi(d, [9, 3, 3, 1]);
      return { title: 'Mendelian ratios from seeds', rows: [['Round : wrinkled', `${m[0]} : ${m[1]} = ${(m[0] / Math.max(1, m[1])).toFixed(2)} : 1`], ['χ² vs 3 : 1', `${cm.chi2.toFixed(2)} (critical 3.84)`], ['Dihybrid', d.join(' : ')], ['χ² vs 9 : 3 : 3 : 1', `${cd.chi2.toFixed(2)} (critical 7.81)`]], conclusion: 'The F₂ seeds of a monohybrid cross show about 3 dominant : 1 recessive, and of a dihybrid cross about 9 : 3 : 3 : 1. Chi-square shows how well the observed counts fit: small deviations are due to chance in which gametes meet. These ratios follow from Mendel\'s laws of segregation and independent assortment.' };
    },
    dispose() { lens.dispose(); hud.dispose(); if (sh) sh.remove(); if (dz) dz.remove(); ui.clearChooser(); },
  };
}
