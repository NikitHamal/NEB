// Quadrat sampling of a grassland plot, both NEB versions: population density (six throws) and
// field verification of density and frequency (ten throws, with Raunkiaer's classes and
// Whitford's index for the clumped Oxalis). The student first learns the four herbs, then throws
// a 1 m² quadrat over the shoulder (a flick; where it lands is chance), counts every plant rooted
// inside by tapping it (rooted outside does not count; misses are pointed out), and works out
// density, frequency and abundance from their own tallies.
import { THREE } from '../../engine.js';
import { ask, sheet, table, outdoors, tag } from '../bench.js';
import { buildField, quadratFrame, SPECIES, HALF } from '../specimens/field.js';
import { mesh, ease, clamp } from '../kit.js';
import { createHud } from '../../handson/hud.js';

const BY = 0.8;
const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + BY, pos[2]], target: [target[0], target[1] + BY, target[2]], fit, fitH, limits: { yaw: 0.5, pitch: 0.3, zMin: 0.5, zMax: 1.4 } });
const RAUNK = (f) => (f <= 20 ? 'A' : f <= 40 ? 'B' : f <= 60 ? 'C' : f <= 80 ? 'D' : 'E');

export function create(ctx) {
  const { world, input, anim, sfx, ui, fx } = ctx;
  const freqLesson = ctx.config.slug.startsWith('quadrat-frequency');
  const N = freqLesson ? 10 : 6;
  const restore = outdoors(ctx);
  const field = buildField((Date.now() & 0xffff) || 31); world.add(field.group);
  const meshes = Object.values(field.meshes);
  const R = field.R;
  const hud = createHud(ctx);
  const frame = quadratFrame(); world.add(frame);
  const HOME = new THREE.Vector3(0, 6, HALF + 6);
  frame.position.copy(HOME); frame.rotation.x = -0.9;
  const markGeo = new THREE.CircleGeometry(0.16, 16); markGeo.rotateX(-Math.PI / 2);
  const markMat = new THREE.MeshBasicMaterial({ color: 0xfacc15, depthTest: false, transparent: true, opacity: 0.95 });
  const missMat = new THREE.MeshBasicMaterial({ color: 0xef4444, depthTest: false, transparent: true, opacity: 0.95 });
  let marks = [];
  const quads = []; let cur = null; let sh = null;
  const known = new Set();
  const tmp = new THREE.Vector3();
  const OVER = S([0, 46, 58], [0, 0, 2], 62, 58);
  const TOPV = (q) => S([q.x - 0.6, 17, q.z + 3.6], [q.x - 0.6, 0, q.z - 0.9], 13, 13);

  function plantAt(hit) { if (!hit || hit.instanceId === undefined) return null; const sp = hit.object.userData.sp; return field.plants.find((p) => p.sp === sp && p.i === hit.instanceId); }
  const inside = (p, q) => Math.abs(p.x - q.x) < 5 && Math.abs(p.z - q.z) < 5;
  const near = (p, q) => Math.abs(p.x - q.x) < 6.2 && Math.abs(p.z - q.z) < 6.2;
  function mark(p, mat = markMat) { const m = mesh(markGeo, mat, [p.x, 0.25 + (p.sp.id === 'age' ? 1.5 : p.sp.id === 'par' ? 2.1 : 0.4) * p.k, p.z], { cast: false }); m.renderOrder = 12; m.userData.noPick = true; world.add(m); marks.push(m); return m; }
  function clearMarks() { marks.forEach((m) => world.remove(m)); marks = []; }
  const tallyHtml = (q) => `<div class="bh-tally">${SPECIES.map((sp) => `<span><i style="background:${sp.color}"></i>${sp.short}: <b>${q.counted[sp.id] || 0}</b></span>`).join('')}</div>`;

  const stepLearn = {
    title: 'Meet the plants of the plot', text: 'Four herbs grow in this 6 m × 6 m plot. Tap one plant of each kind to learn it (zoom with the wheel or pinch).',
    tool: null, autoTool: 'hand', hideBelt: true, shot: S([4, 10, HALF + 9], [2, 0, HALF - 6], 16, 10),
    skip() { SPECIES.forEach((sp) => known.add(sp.id)); },
    handler: { down() {
      const p = plantAt(input.pick(meshes)); if (!p) return false;
      if (!known.has(p.sp.id)) { known.add(p.sp.id); sfx.play('ok'); ui.observe(p.sp.short, p.sp.clumped ? 'grows in patches' : 'scattered'); }
      ctx.say(`<b>${p.sp.name}</b>${{ cyn: ' — a creeping grass; each tuft is counted as one individual.', oxa: ' — trifoliate leaves, yellow flowers; spreads in patches.', age: ' — hairy herb with lilac flower heads.', par: ' — tall, finely divided leaves, white flower heads; a harmful invasive weed.' }[p.sp.id]}`, 'good', 4200);
      ui.setText(`Found ${known.size} of 4.`);
      if (known.size === 4) ctx.next('You know all four species.', 1.6); return true;
    } },
  };

  function quadStep(k) {
    const s = {
      title: `Quadrat ${k + 1} of ${N}`, text: 'Stand at the edge, then <b>flick</b> the quadrat (drag on it and let go) to throw it over your shoulder — it lands at random.',
      tool: null, autoTool: 'hand', hideBelt: true, shot: S([0, 10, HALF + 14], [0, 2, HALF - 4], 16, 14),
      enter() { frame.position.copy(HOME); frame.rotation.set(-0.9, 0, 0); cur = null; s.state = 'throw'; hud.actions([]); clearMarks(); },
      exit() { hud.actions([]); },
      skip() { const q = landAt(); q.counted = { ...q.truth }; quads.push(q); frame.position.set(q.x, 0, q.z); frame.rotation.set(0, q.rot, 0); },
      handler: {
        down(p) { if (s.state !== 'throw') return countTap(p); s.drag = [p.x, p.y]; return true; },
        move(p) { if (!s.drag) return; const dy = s.drag[1] - p.y; frame.position.y = HOME.y + clamp(dy / 200, -0.5, 1.5); },
        up(p) { if (!s.drag) return; const d = Math.hypot(p.x - s.drag[0], p.y - s.drag[1]); s.drag = null; if (d < 30) { frame.position.copy(HOME); ctx.say('Flick it: drag and let go.', 'hint', 1500); return; } throwIt(); },
      },
    };
    function landAt() {
      const x = (R() * 2 - 1) * (HALF - 5.5); const z = (R() * 2 - 1) * (HALF - 5.5);
      const q = { x, z, rot: 0, truth: {}, counted: {}, tapped: new Set(), hand: true };
      SPECIES.forEach((sp) => { q.truth[sp.id] = 0; q.counted[sp.id] = 0; }); field.plants.forEach((p) => { if (inside(p, q)) q.truth[p.sp.id] += 1; });
      return q;
    }
    function throwIt() {
      s.state = 'flying'; const q = landAt(); cur = q; sfx.play('grab');
      const from = frame.position.clone(); const to = new THREE.Vector3(q.x, 0, q.z); const spin = (R() - 0.5) * 6;
      ctx.rig.go(TOPV(q), 1.6);
      anim.add(1.4, (t) => { frame.position.lerpVectors(from, to, t); frame.position.y += Math.sin(Math.PI * t) * 9; frame.rotation.set(-0.9 * (1 - t), spin * t * 0.1 + Math.PI * 2 * t * 0, 0); }, { ease: ease.inOut, done: () => {
        frame.rotation.set(0, 0, 0); sfx.play('place'); s.state = 'count';
        ui.setText(`Count every plant <b>rooted inside</b> the frame: tap each one once.${tallyHtml(q)}`);
        const acts = [{ id: 'done', label: 'Done counting', primary: true, onClick: finish }];
        if (k >= 4) acts.push({ id: 'p', label: 'Partner counts this one', onClick() { q.counted = { ...q.truth }; q.hand = false; field.plants.forEach((p) => { if (inside(p, q) && !q.tapped.has(p)) mark(p); }); anim.wait(0.6, () => record(q)); } });
        hud.actions(acts);
      } });
    }
    function countTap() {
      const q = cur; if (s.state !== 'count' || !q) return false;
      const p = plantAt(input.pick(meshes)); if (!p) return false;
      if (q.tapped.has(p)) { ctx.say('Already counted.', 'hint', 900); return true; }
      if (!inside(p, q)) { if (near(p, q)) ctx.mistake('That plant is rooted <b>outside</b> the frame — only its leaves reach in. Count only plants rooted inside.', 1); return true; }
      q.tapped.add(p); q.counted[p.sp.id] += 1; mark(p); sfx.play('pick');
      ui.setText(`Count every plant <b>rooted inside</b> the frame: tap each one once.${tallyHtml(q)}`);
      return true;
    }
    function finish() {
      const q = cur; const missed = field.plants.filter((p) => inside(p, q) && !q.tapped.has(p));
      if (missed.length) {
        const by = {}; missed.forEach((p) => { by[p.sp.short] = (by[p.sp.short] || 0) + 1; });
        ctx.mistake(`Look again — you missed ${Object.entries(by).map(([n, c]) => `${c} ${n}`).join(', ')} (ringed in red). Tap them to add them to the count.`, 1);
        missed.forEach((p) => mark(p, missMat)); return;
      }
      record(q);
    }
    function record(q) {
      quads.push(q); hud.actions([]); sfx.play('ok');
      ui.observe(`Q${k + 1}`, SPECIES.map((sp) => q.counted[sp.id]).join(' · '));
      ctx.next(`Quadrat ${k + 1}: ${SPECIES.map((sp) => `${sp.short} ${q.counted[sp.id]}`).join(', ')}.`, 1.1);
    }
    return s;
  }

  function stats() {
    const k = quads.length;
    return SPECIES.map((sp) => {
      const n = quads.reduce((a, q) => a + q.counted[sp.id], 0); const occ = quads.filter((q) => q.counted[sp.id] > 0).length;
      const D = n / k; const F = occ / k * 100; const A = occ ? n / occ : 0;
      return { sp, n, occ, D, F, A, AF: F ? A / F : 0 };
    });
  }
  const trueD = (sp) => field.plants.filter((p) => p.sp === sp && Math.abs(p.x) < HALF && Math.abs(p.z) < HALF).length / ((HALF * 2 / 10) ** 2);
  function calcStep() {
    return {
      title: freqLesson ? 'Density, frequency and abundance' : 'Work out the densities', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: OVER,
      enter() {
        const st = stats(); const k = quads.length;
        sh = sheet(ctx, { title: `${k} quadrats of 1 m²`, cls: 'wide' });
        const head = freqLesson ? ['Species', 'N', 'Q', 'D (m⁻²)', 'F %', 'A', 'Class'] : ['Species', 'Total N', 'Density (m⁻²)'];
        const rows = st.map((r) => (freqLesson ? [r.sp.short, r.n, r.occ, r.D.toFixed(2), r.F.toFixed(0), r.A.toFixed(2), RAUNK(r.F)] : [r.sp.short, r.n, r.D.toFixed(2)]));
        sh.set(table(head, rows) + `<p style="margin:.4em 0 0">D = N ÷ (number of quadrats × 1 m²)${freqLesson ? '; F = Q ÷ number of quadrats × 100; A = N ÷ Q' : ''}</p>`);
        const ox = st[1]; const ag = st[2];
        const opt = (v, d = 2) => Math.round(v * 10 ** d) / 10 ** d;
        const shuffle = (a) => a.filter((v, i) => a.indexOf(v) === i).sort(() => R() - 0.5);
        if (!freqLesson) {
          ask(ctx, `Density of Ageratum = ${ag.n} ÷ ${k} m² =`, shuffle([opt(ag.D), opt(ag.n / Math.max(1, ag.occ)), opt(ag.n / 36), opt(ag.D * 10)]).map((v) => ({ label: `${v} per m²`, value: v })), opt(ag.D), {
            y: 0.06, wrong: 'Density is the total number counted divided by the total area sampled (number of quadrats × 1 m²).',
            then() { const est = Math.round(ag.D * 36); ask(ctx, 'About how many Ageratum plants grow in the whole 6 m × 6 m plot?', shuffle([est, Math.round(ag.D * 6), Math.round(ag.n * 6), Math.round(est * 1.5)]).map((v) => ({ label: String(v), value: v })), est, { delay: 0.3, y: 0.06, ok: `Density × area = ${opt(ag.D)} × 36 m² ≈ ${est}. (The plot really holds ${field.plants.filter((p) => p.sp.id === 'age').length}.)`, wrong: 'Multiply the density per m² by the plot area, 36 m².' }); },
          });
        } else {
          ask(ctx, `Frequency of Oxalis = ${ox.occ} of ${k} quadrats =`, shuffle([opt(ox.F, 0), opt(ox.D * 10, 0), opt(100 - ox.F, 0), opt(ox.A * 10, 0)]).map((v) => ({ label: `${v} %`, value: v })), opt(ox.F, 0), {
            y: 0.06, wrong: 'Frequency is the percentage of quadrats in which the species occurred at all.',
            then() {
              const clumped = ox.AF >= ag.AF ? 'oxa' : 'age';
              ask(ctx, `Whitford's index A/F: Oxalis ${ox.AF.toFixed(3)}, Ageratum ${ag.AF.toFixed(3)}. Which grows in clumps?`, [{ label: 'Oxalis', value: 'oxa' }, { label: 'Ageratum', value: 'age' }], clumped, { delay: 0.3, y: 0.06, ok: 'A/F above about 0.05 means a contagious (clumped) distribution, 0.025–0.05 random. Oxalis spreads by runners into patches: where it occurs it is abundant, but it is missing from many quadrats — high abundance, lower frequency.', wrong: 'The larger A/F, the more the individuals are bunched into fewer quadrats.' });
            },
          });
        }
      },
      exit() { ui.clearChooser(); },
    };
  }
  const steps = [stepLearn, ...Array.from({ length: N }, (_, k) => quadStep(k)), calcStep()];
  ctx.debug = { field, frame, get quads() { return quads; }, get cur() { return cur; }, inside };
  void tag; void fx; void tmp;
  return {
    tools: ['hand'],
    steps,
    update() { hud.update(); },
    result() {
      const st = stats(); const handN = quads.filter((q) => q.hand).length;
      const rows = st.map((r) => [r.sp.short, freqLesson ? `D ${r.D.toFixed(2)} m⁻² (true ${trueD(r.sp).toFixed(2)}), F ${r.F.toFixed(0)} % (${RAUNK(r.F)})` : `${r.D.toFixed(2)} m⁻² (true ${trueD(r.sp).toFixed(2)})`]);
      return { title: freqLesson ? 'Quadrat survey: density and frequency' : 'Quadrat survey: population density', rows: [['Quadrats', `${quads.length} (${handN} counted by you)`]].concat(rows), conclusion: freqLesson ? 'Density tells how many individuals there are per unit area, frequency how evenly they are spread through the plot, and abundance how many there are where they occur. A clumped species (Oxalis) can be dense yet infrequent; a random one (Ageratum, Cynodon) is found in most quadrats. More quadrats bring the estimates closer to the true values.' : 'Population density = total individuals ÷ total area sampled. Random throws avoid bias, and averaging several quadrats gives an estimate close to the true density of each species in the plot.' };
    },
    dispose() { restore(); hud.dispose(); if (sh) sh.remove(); ui.clearChooser(); clearMarks(); markGeo.dispose(); markMat.dispose(); missMat.dispose(); },
  };
}
