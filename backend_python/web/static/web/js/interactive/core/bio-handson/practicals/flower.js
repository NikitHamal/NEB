// Dissection of a flower to study its family characters (Solanaceae, Fabaceae, Liliaceae),
// done as on the bench: hold the flower in plasticine on a dissection sheet, judge its symmetry,
// strip the whorls from the outside in with forceps (each part resists, then comes away) and
// lay them out in labelled boxes, cut the ovary across to see its placentation through a lens,
// and write the floral formula.
import { THREE } from '../../engine.js';
import { FAMILIES, WHORL_ORDER } from '../specimens/flowers.js';
import { ovaryTSTexture } from '../specimens/flower-parts.js';
import { canvasTexture, ease, clamp, mesh, MAT } from '../kit.js';

const WHORL_NAME = { Solanaceae: ['sepals', 'petals', 'stamens'], Fabaceae: ['sepals', 'petals', 'stamens'], Liliaceae: ['outer tepals', 'inner tepals', 'stamens'] };
const SHEET = { w: 2.3, d: 1.5, z: 0.12 };
const BOXES_X = [-0.78, -0.26, 0.26, 0.78]; const BOX_Z = 0.42; const BOX_W = 0.46; const BOX_D = 0.42;

function sheetTexture(boxes) {
  return canvasTexture(`sheet:${boxes.map((b) => b[1]).join('|')}`, 1024, 668, (g, w, h) => {
    g.fillStyle = '#fbfbf7'; g.fillRect(0, 0, w, h);
    g.strokeStyle = 'rgba(80,120,170,0.12)'; g.lineWidth = 1;
    for (let y = 20; y < h; y += 22) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
    const sx = w / SHEET.w; const sz = h / SHEET.d;
    boxes.forEach(([, label], i) => {
      const cx = (BOXES_X[i] + SHEET.w / 2) * sx; const cz = (BOX_Z - SHEET.z + SHEET.d / 2) * sz;
      const bw = BOX_W * sx; const bd = BOX_D * sz;
      g.strokeStyle = '#334155'; g.lineWidth = 3; g.setLineDash([12, 8]); g.strokeRect(cx - bw / 2, cz - bd / 2, bw, bd); g.setLineDash([]);
      g.fillStyle = '#1e293b'; g.font = '600 26px "Segoe Print", "Comic Sans MS", system-ui, sans-serif'; g.textAlign = 'center';
      g.fillText(label, cx, cz + bd / 2 + 30);
    });
  });
}

export function create(ctx) {
  const { world, input, tools, fx, anim, sfx, ui } = ctx;
  const sheet = mesh(new THREE.BoxGeometry(SHEET.w, 0.004, SHEET.d), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.92 }), [0, 0.002, SHEET.z]);
  world.add(sheet);
  const lump = mesh(new THREE.SphereGeometry(0.12, 20, 14), MAT.matte(0x6b8e7a), [0, 0.03, -0.32]); lump.scale.set(1, 0.45, 1); world.add(lump);
  ctx.surfaces.push(sheet);
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3(); const pp = new THREE.Vector3();
  const projectFn = (v, out) => input.project(v, out, ctx.stage.clientWidth, ctx.stage.clientHeight);
  let fam = null; let flower = null; let holder = null; let held = null; let tsDone = false; let inset = null;
  const placedCount = {};
  const answers = {};

  function build(name) {
    fam = FAMILIES[name]();
    sheet.material.map = sheetTexture(fam.boxes); sheet.material.needsUpdate = true;
    holder = new THREE.Group(); holder.position.set(0, 0.075, -0.32); holder.rotation.x = fam.tilt; world.add(holder);
    flower = fam.root; holder.add(flower);
    fam.parts.forEach((p) => { p.obj.traverse((o) => { if (o.isMesh) { o.userData.part = p; if (o.material && !o.material.userData.sharedFx) o.material = o.material.clone(); } }); p.home = p.obj.position.clone(); });
    fam.boxes.forEach(([k]) => { placedCount[k] = 0; });
    L = fam.scale < 0.6 ? 0.5 : 1;
    sheet.scale.set(L, 1, L); sheet.position.z = -0.32 + (SHEET.z + 0.32) * L;
    ctx.debug = { fam, BOXES_X: BOXES_X.map((x) => x * L), BOX_Z: bz() };
  }
  const flowerShot = () => { const s = fam ? fam.scale : 1; return { pos: [0.1, 0.95 + 0.55 * s, 0.75 + 0.6 * s], target: [0, 0.85 + 0.25 * s, -0.3], fit: 0.95 * s + 0.25 }; };

  function partFromHit(h) { let o = h && h.object; while (o && !o.userData.part) o = o.parent; return o ? o.userData.part : null; }
  const hitsTmp = []; const rc = new THREE.Raycaster();
  /** The part under the pointer; prefers one from the whorl being worked on, even if a later whorl is in front. */
  function pickPart(prefer) {
    const objs = fam.parts.filter((p) => !p.placed).map((p) => p.obj);
    const first = partFromHit(input.pick(objs));
    if (!prefer || !first || prefer.includes(first.whorl)) return first;
    hitsTmp.length = 0; rc.set(input.ptr.ray.origin, input.ptr.ray.direction); rc.intersectObjects(objs, true, hitsTmp);
    for (const h of hitsTmp) { const p = partFromHit(h); if (p && prefer.includes(p.whorl)) return p; }
    return first;
  }
  let L = 1;
  const bx = (i) => BOXES_X[i] * L; const bz = () => -0.32 + (BOX_Z + 0.32) * L;
  function boxAt(x, z) { for (let i = 0; i < fam.boxes.length; i++) if (Math.abs(x - bx(i)) < BOX_W * L / 2 && Math.abs(z - bz()) < BOX_D * L / 2) return fam.boxes[i][0]; return null; }
  function boxKeyFor(p) { return p.carries && fam.boxes.find((b) => b[0] === p.whorl) ? p.whorl : p.whorl; }

  // ---- the forceps work: tug, detach, carry, lay down ---------------------------------------
  function dragHandler(whorls, onPlaced) {
    return {
      hover() { const p = fam && pickPart(whorls); fx.highlight(p && ui.tool === 'forceps' && !held ? p.obj : null); },
      down(ptr) {
        const p = pickPart(whorls); if (!p) return false;
        if (!ctx.requireTool('forceps', 'Parts of a flower are pulled away with <b>forceps</b>, not cut.')) return true;
        if (!whorls.includes(p.whorl)) {
          const outerFirst = WHORL_ORDER[p.whorl] > WHORL_ORDER[whorls[0]];
          ctx.mistake(outerFirst ? `Work from the outside in: the ${WHORL_NAME[fam.family][WHORL_ORDER[whorls[0]]]} must come off before the ${p.name.toLowerCase()}.` : 'That part has already been dealt with.', 3);
          return true;
        }
        fx.highlight(null);
        p.obj.getWorldPosition(tmp);
        held = { p, mode: 'tug', sx: ptr.x, sy: ptr.y, start: tmp.clone() };
        tools.press(1); tools.action(1); sfx.play('pick');
        return true;
      },
      move(ptr) {
        if (!held) return;
        const { p } = held;
        if (held.mode === 'tug') {
          const d = Math.hypot(ptr.x - held.sx, ptr.y - held.sy);
          const k = Math.min(1, d / 34);
          p.obj.position.copy(p.home); p.obj.position.y += k * 0.012 * fam.scale; p.obj.scale.setScalar(1 + k * 0.03);
          if (d > 34) {
            held.mode = 'carry'; sfx.play('tear'); world.attach(p.obj); p.obj.scale.setScalar(1);
            p.obj.getWorldPosition(tmp); fx.burst(tmp, 0xd9f99d, 4, 0.1, ctx.BENCH_Y + 0.01);
          }
          return;
        }
        if (input.planePoint(ctx.BENCH_Y + 0.14, pp)) { world.worldToLocal(pp); p.target = pp.clone(); }
      },
      up(ptr) {
        if (!held) return;
        const { p, mode } = held; held = null; tools.press(0); tools.action(0);
        if (mode === 'tug') { anim.add(0.35, (k) => { p.obj.position.lerpVectors(p.obj.position.clone(), p.home, k); p.obj.scale.setScalar(1); }, { ease: ease.outBack }); return; }
        p.target = null;
        input.planePoint(ctx.BENCH_Y, pp); world.worldToLocal(pp);
        const key = boxAt(pp.x, pp.z);
        const want = boxKeyFor(p);
        if (key === want) layInBox(p, key, onPlaced);
        else {
          if (key) ctx.mistake(`The ${p.name.toLowerCase()} belongs in <b>${fam.boxes.find((b) => b[0] === want)[1]}</b>.`, 2);
          else ctx.say('Lay it in its labelled box on the sheet.', 'hint', 2200);
          const from = p.obj.position.clone(); const to = new THREE.Vector3(clamp(pp.x, -L, L), 0.02, clamp(pp.z, -0.1, 0.1));
          anim.add(0.4, (k) => p.obj.position.lerpVectors(from, to, k), { ease: ease.out });
        }
      },
    };
  }
  function layInBox(p, key, onPlaced) {
    const i = fam.boxes.findIndex((b) => b[0] === key);
    const n = placedCount[key]++;
    const cols = 3; const col = n % cols; const row = Math.floor(n / cols);
    const to = new THREE.Vector3(bx(i) + (col - 1) * 0.13 * L, 0.012, bz() - 0.1 * L + row * 0.13 * L);
    const from = p.obj.position.clone(); const q0 = p.obj.quaternion.clone();
    const main = p.obj.isMesh ? null : p.obj.children.find((c) => c.isMesh);
    const q1 = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, (n % 2 ? 0.4 : -0.3), 0)).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(p.lay.rx, 0, 0)));
    if (main) q1.multiply(main.quaternion.clone().invert());
    const s0 = p.obj.scale.x; const s1 = (p.lay.s || 1) * (fam.scale < 0.6 ? 1.3 : 1);
    p.placed = true;
    const sheetMesh = main || p.obj;
    if (sheetMesh.userData && sheetMesh.userData.flat) anim.wait(0.3, () => { const ng = sheetMesh.userData.flat(); sheetMesh.geometry.dispose(); sheetMesh.geometry = ng; sheetMesh.userData.flat = null; });
    anim.add(0.55, (k) => { p.obj.position.lerpVectors(from, to, k); p.obj.position.y += Math.sin(Math.PI * k) * 0.08; p.obj.quaternion.slerpQuaternions(q0, q1, k); p.obj.scale.setScalar(s0 + (s1 - s0) * k); }, { ease: ease.inOut, done: () => { sfx.play('place'); onPlaced(p); } });
  }

  // ---- steps -------------------------------------------------------------------------------------
  const stepChoose = {
    title: 'Choose a flower to dissect',
    text: 'Three flowers are on the bench: <b>Datura</b> (Solanaceae), <b>pea</b> (Fabaceae) and <b>lily</b> (Liliaceae). Pick one.',
    shot: SHEET_SHOT(), autoTool: 'hand', hideBelt: true,
    enter() {
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, ctx.stage.clientHeight * 0.3, 'Which family?', [
        { label: 'Solanaceae — Datura', value: 'Solanaceae' }, { label: 'Fabaceae — pea', value: 'Fabaceae' }, { label: 'Liliaceae — lily', value: 'Liliaceae' }], (v) => {
        build(v); ui.observe('Family', `${fam.family} (${fam.example})`);
        if (fam.family === 'Solanaceae') { steps[4] = stepEpipetalous; ui.setSteps(steps); ui.setStep(0, steps.length, stepChoose); }
        ctx.next(`A ${fam.example} flower, fresh and fully open, is held upright in plasticine.`, 0.4);
      });
      anim.wait(0.8, ask);
    },
    skip() { if (!fam) { build(window.__bhFamily || 'Solanaceae'); if (fam.family === 'Solanaceae') { steps[4] = stepEpipetalous; ui.setSteps(steps); } } },
    exit() { ui.clearChooser(); },
  };
  const stepSymmetry = {
    title: 'Look at its symmetry',
    text: 'Turn the view and look at the flower face-on. Can it be cut into two equal halves along more than one plane?',
    hint: 'Actinomorphic (⊕): radially symmetrical, any plane through the centre gives two equal halves. Zygomorphic (%): only one such plane.',
    tool: null, autoTool: 'hand',
    get shot() { return flowerShot(); },
    enter() {
      anim.wait(1.2, () => ui.choose(ctx.stage.clientWidth / 2, 40, 'Symmetry of this flower', [{ label: '⊕ Actinomorphic', value: 'actinomorphic' }, { label: '% Zygomorphic', value: 'zygomorphic' }], (v) => {
        if (v === fam.symmetry) { answers.sym = true; ui.observe('Symmetry', v); ctx.next(v === 'zygomorphic' ? 'Zygomorphic: only the vertical plane through the standard and keel divides it into mirror halves.' : 'Actinomorphic: it can be halved along several planes through its centre.'); }
        else { ctx.mistake(fam.symmetry === 'zygomorphic' ? 'Look again: the large standard on top, two wings at the sides and the keel below — only one plane gives mirror halves.' : 'Look again: the parts are arranged evenly round the centre, so many planes give mirror halves.', 3); anim.wait(0.5, () => stepSymmetry.enter()); }
      }));
    },
    skip() { answers.sym = true; },
    exit() { ui.clearChooser(); },
  };
  function whorlStep(title, text, whorls, doneMsg) {
    const s = {
      title, text, tool: 'forceps', hint: 'Grab the part with the forceps, pull until it comes free, then drop it in its labelled box.',
      get shot() { return fam && fam.scale < 0.6 ? WORK_SHOT_SMALL : WORK_SHOT; },
      enter() { s.left = fam.parts.filter((p) => whorls.includes(p.whorl) && !p.placed).length; if (!s.left) ctx.next(); },
      skip() { fam.parts.filter((p) => whorls.includes(p.whorl) && !p.placed).forEach((p) => { world.attach(p.obj); layInBox(p, boxKeyFor(p), () => {}); }); anim.update(2); },
      update() { if (held && held.mode === 'carry' && held.p.target) held.p.obj.position.lerp(held.p.target, 0.35); },
    };
    s.handler = dragHandler(whorls, (p) => {
      const left = fam.parts.filter((q) => whorls.includes(q.whorl) && !q.placed).length;
      ctx.progress(1 - left / Math.max(1, s.left));
      if (p.carries === 'androecium') ctx.say('The stamens came away with the corolla — their filaments are fused to the corolla tube: <b>epipetalous</b>.', 'good', 5200);
      if (!left) anim.wait(0.5, () => ctx.next(doneMsg()));
    });
    return s;
  }
  const stepOuter = whorlStep('Remove the outermost whorl', 'With the <b>forceps</b>, pull away the outermost whorl — the sepals (or the outer tepals) — and lay them in the first box.', ['calyx', 'outer'], () => (fam.family === 'Liliaceae' ? 'Three outer tepals, free from one another and coloured like petals: the perianth.' : `The calyx: five sepals fused into one ${fam.family === 'Solanaceae' ? 'long, five-angled tube' : 'cup with five teeth'} — gamosepalous.`));
  const stepSecond = whorlStep('Remove the second whorl', 'Now the petals (or inner tepals). Pull each one away and lay it in the second box.', ['corolla', 'inner'], () => (fam.family === 'Fabaceae' ? 'Papilionaceous corolla: one standard, two wings and a keel of two fused petals; the standard overlapped the wings (vexillary aestivation).' : fam.family === 'Liliaceae' ? 'Three inner tepals, alternating with the outer three: perianth in two whorls of three.' : 'A funnel of five fused, pleated petals: gamopetalous.'));
  const stepStamens = whorlStep('Remove the stamens', 'Take out the stamens and lay them in the androecium box. Count them.', ['androecium'], () => (fam.family === 'Fabaceae' ? 'Diadelphous: nine filaments fused into a sheath, one free — (9)+1.' : 'Six free stamens in two whorls of three; the anthers swing on the filament tip (versatile).'));
  const stepEpipetalous = {
    title: 'Where are the stamens?',
    text: 'The Datura stamens left with the corolla. Look inside the corolla tube in the second box.',
    tool: null, autoTool: 'hand', get shot() { return { pos: [-0.26, 1.35, 0.95], target: [-0.26, 0.82, 0.42], fit: 0.6 }; },
    enter() {
      anim.wait(1.4, () => ui.choose(ctx.stage.clientWidth / 2, 40, 'Stamens fused to the petals are called…', [{ label: 'Epipetalous', value: 'epi' }, { label: 'Epiphyllous', value: 'phyl' }, { label: 'Syngenesious', value: 'syn' }], (v) => {
        if (v === 'epi') { ui.observe('Androecium', '5, epipetalous'); ctx.next('Epipetalous: five stamens alternating with the petals, their filaments fused to the corolla tube.'); }
        else { ctx.mistake('Epiphyllous means fused to tepals; syngenesious means anthers united (as in sunflower). Fused to petals is epipetalous.', 3); anim.wait(0.5, () => stepEpipetalous.enter()); }
      }));
    },
    exit() { ui.clearChooser(); },
  };

  // ---- cutting the ovary --------------------------------------------------------------------------
  const sA = new THREE.Vector3(); const sB = new THREE.Vector3(); let last = null;
  function crosses(ax, ay, bx, by, cx, cy, dx, dy) {
    const d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx); if (Math.abs(d) < 1e-6) return false;
    const u = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d; const v = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d;
    return u >= 0 && u <= 1 && v >= 0 && v <= 1;
  }
  function showInset() {
    inset = document.createElement('div'); inset.className = 'bh-inset';
    const tex = ovaryTSTexture(fam.tsKind);
    inset.innerHTML = '<div class="bh-inset-lens"></div><span>Ovary in transverse section, through the hand lens</span>';
    const c = tex.image; c.className = 'bh-inset-img'; inset.querySelector('.bh-inset-lens').appendChild(c);
    ui.root.appendChild(inset);
    requestAnimationFrame(() => inset.classList.add('show'));
  }
  const stepCutOvary = {
    title: 'Cut the ovary across',
    text: 'Only the pistil is left. With the <b>scalpel</b>, slice straight across the swollen ovary at its base.',
    hint: 'Drag the scalpel across the ovary, side to side.',
    tool: 'scalpel', get shot() { return flowerShot(); },
    skip() { cutOvary(true); },
    handler: {
      down(ptr) { if (!ctx.requireTool('scalpel')) return true; last = [ptr.x, ptr.y]; tools.press(1); return true; },
      move(ptr) {
        if (!last || tsDone) return;
        const ov = fam.gyno.userData.ovary; const r = ov.geometry.parameters.radius;
        sA.set(0, -r, 0); ov.localToWorld(sA); projectFn(sA, sA);
        sB.set(0, r, 0); ov.localToWorld(sB); projectFn(sB, sB);
        const mx = (sA.x + sB.x) / 2; const my = (sA.y + sB.y) / 2; const half = Math.max(16, Math.hypot(sB.x - sA.x, sB.y - sA.y) / 2);
        if (crosses(last[0], last[1], ptr.x, ptr.y, mx, my - half, mx, my + half)) cutOvary(false);
        last = [ptr.x, ptr.y];
      },
      up() { last = null; tools.press(0); },
    },
  };
  function cutOvary(instant) {
    if (tsDone) return; tsDone = true; sfx.play('cut');
    const g = fam.gyno; const ov = g.userData.ovary;
    ov.getWorldPosition(tmp); fx.burst(tmp, 0xd9f99d, 5, 0.08, ctx.BENCH_Y + 0.01);
    const upper = new THREE.Group(); g.children.slice().forEach((c) => { if (c !== ov) upper.add(c); });
    g.add(upper);
    const disc = new THREE.Mesh(new THREE.CircleGeometry(1, 40), new THREE.MeshStandardMaterial({ map: ovaryTSTexture(fam.tsKind), roughness: 0.6 }));
    disc.rotation.x = -Math.PI / 2; disc.position.y = ov.position.y + 0.0005; disc.scale.setScalar(ov.geometry.parameters.radius * 0.98);
    g.add(disc); ov.scale.y *= 0.5; ov.position.y *= 0.5;
    if (!instant) anim.add(0.8, (k) => { upper.position.set(k * 0.08 * fam.scale, Math.sin(Math.PI * k) * 0.05, 0); upper.rotation.z = -k * 1.2; }, { ease: ease.out });
    else { upper.visible = false; }
    if (!instant) anim.wait(0.9, () => { showInset(); ctx.next(); });
  }
  const stepPlacenta = {
    title: 'Placentation',
    text: 'Study the cut face through the lens: how many chambers (locules), and where are the ovules attached?',
    tool: null, autoTool: 'hand', get shot() { return flowerShot(); },
    enter() {
      if (!inset) showInset();
      const opts = [['axile', 'Axile — on a central axis'], ['marginal', 'Marginal — along one edge'], ['parietal', 'Parietal — on the wall'], ['free central', 'Free central'], ['basal', 'Basal']];
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, ctx.stage.clientHeight - 150, 'Placentation', opts.map(([v, l]) => ({ label: l, value: v })), (v) => {
        if (v === fam.placentation) {
          const note = fam.tsKind === 'axile2' ? 'Axile, on swollen placentas; two carpels, but a false septum makes it look four-chambered.' : fam.tsKind === 'axile3' ? 'Axile: three locules, ovules in two rows on the central axis.' : 'Marginal: one locule, ovules in a row along the ventral suture of the single carpel.';
          ui.observe('Placentation', v); ctx.next(note);
        } else { ctx.mistake('Look at where the ovules are attached: to the centre where the septa meet (axile), or along one edge of a single chamber (marginal)?', 3); anim.wait(0.4, ask); }
      });
      anim.wait(0.8, ask);
    },
    exit() { ui.clearChooser(); if (inset) { inset.remove(); inset = null; } },
  };

  // ---- floral formula ------------------------------------------------------------------------------
  const stepFormula = {
    title: 'Write the floral formula',
    text: 'Build the formula one whorl at a time.',
    tool: null, autoTool: 'hand', hideBelt: true, get shot() { return fam && fam.scale < 0.6 ? WORK_SHOT_SMALL : WORK_SHOT; },
    enter() {
      const f = fam.formula; const lily = fam.family === 'Liliaceae';
      const slots = [
        ['Symmetry', f.sym, ['⊕', '%']],
        [lily ? 'Perianth' : 'Calyx', f.k, lily ? ['P3+3', 'P(5)', 'K3 C3'] : ['K5', 'K(5)', 'K(4)']],
        ...(lily ? [] : [['Corolla', f.c, ['C5', 'C(5)', 'C1+2+(2)', 'C(4)']]]),
        ['Androecium', f.a, fam.family === 'Fabaceae' ? ['A10', 'A(9)+1', 'A(10)'] : lily ? ['A3+3', 'A(6)', 'A∞'] : ['A5 (epipetalous)', 'A(5)', 'A∞']],
        ['Gynoecium (superior)', f.g, ['G1', 'G(2)', 'G(3)', 'G(5)']],
      ];
      const done = [];
      const show = () => ui.setText(`<span class="bh-formula">${done.map((d) => d.replace(/^G/, '<u>G</u>')).join(' ')}${done.length < slots.length ? ' <i>…</i>' : ''}</span>`);
      const ask = (i) => {
        if (i >= slots.length) { ui.observe('Floral formula', `${done.join(' ')}`); ctx.next(`${fam.family}: ${done.join(' ')}. (The bar under G means a superior ovary.)`, 1.2); return; }
        const [label, right, opts] = slots[i];
        const o = opts.includes(right) ? opts.slice() : opts.concat([right]); o.sort(() => Math.random() - 0.5);
        ui.choose(ctx.stage.clientWidth / 2, 70, label, o.map((x) => ({ label: x, value: x })), (v) => {
          if (v === right) { done.push(i === 0 ? `${v} ⚥` : v); sfx.play('ok'); show(); ask(i + 1); }
          else { ctx.mistake(`Not ${v}. Think back to what you laid in the ${label.toLowerCase()} box: count the parts and whether they were fused (brackets) or free.`, 2); anim.wait(0.3, () => ask(i)); }
        });
      };
      show(); anim.wait(0.6, () => ask(0));
    },
    exit() { ui.clearChooser(); },
  };

  // the step list depends on the family, so it is resolved once the flower is chosen
  const steps = [stepChoose, stepSymmetry, stepOuter, stepSecond, stepStamens, stepCutOvary, stepPlacenta, stepFormula];

  return {
    tools: ['hand', 'forceps', 'scalpel'],
    steps,
    update(dt) { if (held && held.mode === 'carry' && held.p.target) held.p.obj.position.lerp(held.p.target, 1 - Math.pow(0.0005, dt)); },
    result() {
      return {
        title: `${fam.family} flower dissected`,
        rows: [['Flower', fam.example], ['Symmetry', fam.symmetry], ['Placentation', fam.placentation], ['Floral formula', Object.values(fam.formula).filter(Boolean).join(' ')]],
        conclusion: fam.family === 'Solanaceae' ? 'Solanaceae: flowers actinomorphic, bisexual, pentamerous; calyx and corolla gamous; five epipetalous stamens; bicarpellary syncarpous superior ovary placed obliquely, with axile placentation on swollen placentas.'
          : fam.family === 'Fabaceae' ? 'Fabaceae (Papilionoideae): flowers zygomorphic with a papilionaceous corolla (standard, wings, keel) in vexillary aestivation, diadelphous stamens (9)+1 and a monocarpellary superior ovary with marginal placentation — the pod.'
            : 'Liliaceae: flowers actinomorphic and trimerous, a petal-like perianth of six tepals in two whorls, six stamens in two whorls, and a tricarpellary syncarpous superior ovary, trilocular with axile placentation.',
      };
    },
    dispose() { if (inset) inset.remove(); ui.clearChooser(); },
  };
}
const WORK_SHOT_SMALL = { pos: [0.03, 1.75, 0.6], target: [0, 0.86, -0.06], fit: 1.1, fitH: 0.8 };
const WORK_SHOT = { pos: [0.05, 2.75, 1.25], target: [0, 0.95, 0.02], fit: 2.15, fitH: 1.55 };
function SHEET_SHOT() { return { pos: [0, 2.15, 1.55], target: [0, 0.82, 0.12], fit: 2.25 }; }
