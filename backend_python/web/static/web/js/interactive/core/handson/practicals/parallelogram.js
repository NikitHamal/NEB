// Parallelogram law of forces on Gravesand's apparatus: a vertical board with drawing paper, two
// pulleys at its top corners, strings from a knot over the pulleys to hangers P and Q and a third
// hanger R straight down from the knot. The student loads slotted masses (tap a hanger), the knot
// really moves to equilibrium (forces summed each frame, with a little pulley friction, so it can
// stick slightly off), is disturbed and released, the thread directions are marked with dots on
// the paper, and the parallelogram is constructed to scale on a drawing sheet from those dots:
// its diagonal is compared with R.
import { THREE } from '../../engine.js';
import { MAT, mesh, canvasTexture } from '../../bio-handson/kit.js';
import { M as KIT } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits, screenDist } from '../hud.js';
import { createDrawSheet } from '../drawsheet.js';

const BY = 0.8; const HANGER = 50; const SLOT = 50; const FRICTION = 2.2; const SCALE = 50;
const ZF = 0.16; const PL = new THREE.Vector3(-2.75, 5.55, ZF); const PR = new THREE.Vector3(2.75, 5.55, ZF);
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const UP = new THREE.Vector3(0, 1, 0);

function rod(parent, r = 0.011, color = 0x5b4636) {
  const m = mesh(new THREE.CylinderGeometry(r, r, 1, 6), MAT.matte(color), null, { cast: false }); parent.add(m);
  return (a, b) => { const d = b.clone().sub(a); const L = d.length(); m.scale.set(1, Math.max(0.001, L), 1); m.position.copy(a).addScaledVector(d, 0.5); m.quaternion.setFromUnitVectors(UP, d.normalize()); };
}

function hanger(label) {
  const g = new THREE.Group();
  g.add(mesh(new THREE.TorusGeometry(0.04, 0.008, 6, 14), MAT.brushed(), [0, -0.04, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.75, 8), MAT.brushed(), [0, -0.42, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.03, 24), MAT.brushed(), [0, -0.8, 0]));
  const tag = mesh(new THREE.PlaneGeometry(0.22, 0.12), new THREE.MeshBasicMaterial({ map: canvasTexture(`ho-pf-${label}`, 96, 52, (c, w, h) => { c.fillStyle = '#111827'; c.fillRect(0, 0, w, h); c.fillStyle = '#fef3c7'; c.font = '800 36px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText(label, w / 2, 39); }) }), [0, -0.92, 0.18]);
  g.add(tag);
  const slots = [];
  return {
    group: g, n: 0,
    get grams() { return HANGER + this.n * SLOT; },
    add(k) {
      if (k > 0) { const s = mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.055, 24), MAT.gloss(0x9a7b3a), [0, -0.785 + 0.03 + slots.length * 0.058, 0]); g.add(s); slots.push(s); this.n += 1; }
      else if (slots.length) { g.remove(slots.pop()); this.n -= 1; }
    },
  };
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const sheet = createDrawSheet(hud, { title: 'Parallelogram, 1 cm = 50 g-wt', widthCm: 16, heightCm: 13, origin: [8, 3.6] });

  const board = mesh(new THREE.BoxGeometry(6.0, 5.0, 0.12), KIT.wood('teak'), [0, 3.2, 0]); world.add(board);
  const paper = mesh(new THREE.PlaneGeometry(4.4, 3.6), MAT.paper(), [0, 3.25, 0.062]); world.add(paper);
  [-2.2, 2.2].forEach((x) => { world.add(mesh(new THREE.BoxGeometry(0.12, 0.7, 0.12), KIT.wood('teak'), [x, 0.35, 0])); world.add(mesh(new THREE.BoxGeometry(0.5, 0.06, 0.9), MAT.matte(0x2b3138), [x, 0.03, 0])); });
  [PL, PR].forEach((p) => {
    const w = mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.05, 28), MAT.gloss(0xc9a227), [p.x, p.y - 0.18, ZF]); w.rotation.x = Math.PI / 2; world.add(w);
    world.add(mesh(new THREE.BoxGeometry(0.06, 0.35, 0.12), MAT.steel(), [p.x, p.y - 0.18, 0.08]));
  });
  const H = { P: hanger('P'), Q: hanger('Q'), R: hanger('R') };
  Object.values(H).forEach((h) => world.add(h.group));
  const knot = mesh(new THREE.SphereGeometry(0.045, 14, 10), MAT.matte(0xf5f0e1), null); world.add(knot);
  const sL = rod(world); const sR = rod(world); const sD = rod(world); const hL = rod(world); const hR = rod(world);
  const L_P = 5.1; const L_Q = 5.1; const L_R = 1.2;

  const st = { K: new THREE.Vector3(0, 3.6, ZF), v: new THREE.Vector3(), stuck: false, limit: false, dots: { P: [], Q: [], R: [] }, removing: false, disturbed: false, dragging: false, ang: {}, res: null };
  const tmp = new THREE.Vector3(); const F = new THREE.Vector3();
  function forces(K, out) {
    out.set(0, -H.R.grams, 0);
    tmp.copy(PL).sub(K).setZ(0).normalize(); out.addScaledVector(tmp, H.P.grams);
    tmp.copy(PR).sub(K).setZ(0).normalize(); out.addScaledVector(tmp, H.Q.grams);
    return out;
  }
  function equilibrium() {
    const K = new THREE.Vector3(0, 3.6, ZF); const v = new THREE.Vector3();
    for (let i = 0; i < 4000; i++) { forces(K, F); v.addScaledVector(F, 0.0004).multiplyScalar(0.9); K.add(v); K.x = THREE.MathUtils.clamp(K.x, -2.3, 2.3); K.y = THREE.MathUtils.clamp(K.y, 1.6, 5.1); }
    return K;
  }
  function layout() {
    const K = st.K; knot.position.copy(K);
    const dl = K.distanceTo(PL); const dr = K.distanceTo(PR);
    const lx = PL.x - 0.18; const rx = PR.x + 0.18;
    const yl = PL.y - 0.18 - Math.max(0.3, L_P - dl); const yr = PR.y - 0.18 - Math.max(0.3, L_Q - dr);
    H.P.group.position.set(lx, yl, ZF); H.Q.group.position.set(rx, yr, ZF); H.R.group.position.set(K.x, K.y - L_R, ZF);
    const tl = new THREE.Vector3(PL.x, PL.y, ZF); const tr = new THREE.Vector3(PR.x, PR.y, ZF);
    const dirL = tl.clone().sub(K).normalize(); const nL = new THREE.Vector3(-dirL.y, dirL.x, 0).multiplyScalar(0.18); const dirR = tr.clone().sub(K).normalize(); const nR = new THREE.Vector3(dirR.y, -dirR.x, 0).multiplyScalar(0.18);
    sL(K, tl.clone().sub(new THREE.Vector3(0, 0.18, 0)).add(nL)); sR(K, tr.clone().sub(new THREE.Vector3(0, 0.18, 0)).add(nR));
    sD(K, H.R.group.position); hL(new THREE.Vector3(lx, PL.y - 0.18, ZF), H.P.group.position); hR(new THREE.Vector3(rx, PR.y - 0.18, ZF), H.Q.group.position);
  }
  function step(dt) {
    if (st.dragging) { st.v.set(0, 0, 0); return; }
    const n = Math.max(1, Math.ceil(dt / 0.01)); const h = dt / n; const Msum = (H.P.grams + H.Q.grams + H.R.grams) / 1000;
    for (let i = 0; i < n; i++) {
      forces(st.K, F);
      if (st.v.length() < 0.02 && F.length() < FRICTION) { st.v.set(0, 0, 0); st.stuck = true; continue; }
      st.stuck = false;
      st.v.addScaledVector(F, h * 9.8 / Msum / 1000 * 10).multiplyScalar(Math.exp(-2.8 * h));
      st.K.addScaledVector(st.v, h);
      const x0 = st.K.x; const y0 = st.K.y;
      st.K.x = THREE.MathUtils.clamp(st.K.x, -2.4, 2.4); st.K.y = THREE.MathUtils.clamp(st.K.y, 1.5, 5.15);
      st.limit = x0 !== st.K.x || y0 !== st.K.y; if (st.limit) st.v.multiplyScalar(0.2);
    }
  }
  const loads = () => `P ${H.P.grams} g · Q ${H.Q.grams} g · R ${H.R.grams} g`;

  const SHOT = shot({ pos: [0, 3.3, 9.6], target: [0, 3.1, 0], fit: 6.6, fitH: 5.9 });
  const SHOT_K = () => shot({ pos: [st.K.x * 0.6, st.K.y + 0.2, 4.6], target: [st.K.x * 0.5, st.K.y - 0.4, 0], fit: 4.6, fitH: 4.0 });
  const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -(ZF - 0.1)); const hit = new THREE.Vector3();
  const boardPoint = () => { plane.constant = -0.064; if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return null; return world.worldToLocal(hit); };
  const dotGeo = new THREE.SphereGeometry(0.03, 10, 8); const dotMat = MAT.ink(0x111827);
  const dotMeshes = [];

  function threadDist(p, key) {
    const K = st.K; const end = key === 'P' ? new THREE.Vector3(PL.x, PL.y, 0) : key === 'Q' ? new THREE.Vector3(PR.x, PR.y, 0) : new THREE.Vector3(K.x, K.y - 3, 0);
    const a = new THREE.Vector2(K.x, K.y); const b = new THREE.Vector2(end.x, end.y); const q = new THREE.Vector2(p.x, p.y);
    const ab = b.clone().sub(a); const t = THREE.MathUtils.clamp(q.clone().sub(a).dot(ab) / ab.lengthSq(), 0, 1);
    return { d: a.clone().addScaledVector(ab, t).distanceTo(q), t, fromK: q.distanceTo(a) };
  }
  function dirOf(key) { const [a, b] = st.dots[key]; const v = new THREE.Vector2(b.x - a.x, b.y - a.y); if (key === 'R' ? v.y > 0 : v.y < 0) v.negate(); return Math.atan2(v.y, v.x); }

  const steps = [
    {
      title: 'Load the hangers', text: 'Each hanger weighs 50 g. <b>Tap a hanger</b> to add a 50 g slotted mass (turn on <b>Take off</b> to remove one). Choose three loads that can balance, all different, and let the knot come to rest.',
      hint: 'Three forces can balance only if each is less than the sum of the other two. Try P 200 g, Q 250 g, R 300 g.', shot: SHOT, hideBelt: true,
      enter() {
        hud.actions([{ id: 'off', label: 'Take off', onClick: () => { st.removing = !st.removing; hud.relabel('off', st.removing ? 'Taking off ✓' : 'Take off'); } }, { id: 'done', label: 'Loads set', primary: true, onClick: () => {
          const p = H.P.grams; const q = H.Q.grams; const r = H.R.grams;
          if (p === q && q === r) { ctx.say('Use three different loads: equal loads only test the 120° special case.', 'hint', 2600); return; }
          if (st.limit || r >= p + q || p >= q + r || q >= p + r) { ctx.mistake('These loads cannot balance: one force is not less than the sum of the other two, so the knot runs off to a pulley or the floor.', 3); return; }
          if (st.v.length() > 0.03) { ctx.say('Wait for the knot to come to rest.', 'hint', 1800); return; }
          ui.observe('Loads', loads()); hud.actions([]); ctx.next('Balanced.');
        } }]);
      },
      exit() { hud.actions([]); },
      skip() { while (H.P.n < 3) H.P.add(1); while (H.Q.n < 4) H.Q.add(1); while (H.R.n < 5) H.R.add(1); st.K.copy(equilibrium()); st.v.set(0, 0, 0); },
      handler: { down(p) {
        for (const k of ['P', 'Q', 'R']) {
          if (hits(ctx, H[k].group, p, 55, -0.6)) {
            if (st.removing) { if (!H[k].n) { ctx.say('Only the hanger is left on that one.', 'hint', 1500); return true; } H[k].add(-1); } else { if (H[k].n >= 9) { ctx.say('That is all the slotted masses for that hanger.', 'hint', 1500); return true; } H[k].add(1); }
            sfx.play('place'); st.v.y += 0.05; ctx.say(loads(), 'info', 1600); return true;
          }
        }
        return false;
      } },
    },
    {
      title: 'Disturb the knot', text: 'Drag the <b>knot</b> a little to one side and let go. If the equilibrium is real it swings back to (almost) the same place: the pulleys have a little friction.', shot: null, hideBelt: true,
      enter() { ctx.rig.go(SHOT_K(), 1.2); st.home = st.K.clone(); },
      skip() { st.disturbed = true; },
      handler: {
        down(p) { if (screenDist(ctx, knot, p) > 60) return false; st.dragging = true; sfx.play('pick'); return true; },
        move() { if (!st.dragging) return; const q = boardPoint(); if (!q) return; st.K.x = THREE.MathUtils.clamp(q.x, st.home.x - 0.8, st.home.x + 0.8); st.K.y = THREE.MathUtils.clamp(q.y, st.home.y - 0.8, st.home.y + 0.8); },
        up() {
          if (!st.dragging) return; st.dragging = false;
          if (st.K.distanceTo(st.home) < 0.25) { ctx.say('Pull it further away than that.', 'hint', 1500); return; }
          sfx.play('drop'); anim.wait(2.6, () => { const d = st.K.distanceTo(st.home) * 10; ui.observe('Knot returns', `within ${d.toFixed(1)} cm`); ctx.next('It comes back: a true equilibrium.'); });
        },
        cancel() { st.dragging = false; },
      },
    },
    {
      title: 'Mark the threads', text: 'Tap the paper <b>directly under each thread</b>, twice per thread and well apart, to mark its direction with dots (sight along the thread so there is no parallax).', hint: 'Two dots per thread: one near the knot, one far from it. Six dots in all.', shot: null, hideBelt: true,
      enter() { ctx.rig.go(SHOT_K(), 1.0); },
      skip() { ['P', 'Q', 'R'].forEach((k) => { const end = k === 'P' ? PL : k === 'Q' ? PR : new THREE.Vector3(st.K.x, st.K.y - 2, 0); [0.25, 0.6].forEach((t) => st.dots[k].push(st.K.clone().lerp(end, k === 'R' ? t * 0.6 : t))); }); },
      handler: { down() {
        const q = boardPoint(); if (!q) return false;
        if (Math.abs(q.x) > 2.2 || Math.abs(q.y - 3.25) > 1.8) return false;
        let best = null; for (const k of ['P', 'Q', 'R']) { const d = threadDist(q, k); if (!best || d.d < best.d) best = Object.assign({ k }, d); }
        if (best.d > 0.13) { ctx.mistake('That dot is not under any thread. Line your eye up with the thread and tap exactly beneath it.', 1); return true; }
        if (best.fromK < 0.35) { ctx.say('Too close to the knot: put the dots further out so the direction is accurate.', 'hint', 2000); return true; }
        const arr = st.dots[best.k]; if (arr.length >= 2) { ctx.say(`Thread ${best.k} already has two dots.`, 'hint', 1500); return true; }
        if (arr.length === 1 && arr[0].distanceTo(q) < 0.5) { ctx.say('Put the second dot further along the thread.', 'hint', 1800); return true; }
        arr.push(q.clone()); const m = new THREE.Mesh(dotGeo, dotMat); m.position.set(q.x, q.y, 0.07); m.scale.set(1, 1, 0.3); world.add(m); dotMeshes.push(m); sfx.play('pin');
        if (['P', 'Q', 'R'].every((k) => st.dots[k].length === 2)) ctx.next('All three threads marked.');
        return true;
      } },
    },
    {
      title: 'Construct the parallelogram', text: 'Lines are drawn through your dots to meet at O. To the scale <b>1 cm = 50 g-wt</b>, drag <b>A</b> along the P line to length P, <b>B</b> along the Q line to length Q, then drag <b>C</b> to complete the parallelogram OACB.', hint: 'OA = P/50 cm, OB = Q/50 cm; C is where the line through A parallel to OB meets the line through B parallel to OA.', shot: SHOT, hideBelt: true,
      enter() {
        st.ang = { P: dirOf('P'), Q: dirOf('Q'), R: dirOf('R') };
        sheet.clear(); sheet.line(st.ang.P, { label: 'P', color: '#b91c1c' }); sheet.line(st.ang.Q, { label: 'Q', color: '#1d4ed8' }); sheet.line(st.ang.R, { label: 'R', color: '#166534', labelAt: 2.6 }); sheet.line(st.ang.R + Math.PI, { dash: true, color: '#166534' });
        const A = sheet.handle({ label: 'A', along: st.ang.P, x: Math.cos(st.ang.P) * 1.5, y: Math.sin(st.ang.P) * 1.5, color: '#b91c1c' });
        const B = sheet.handle({ label: 'B', along: st.ang.Q, x: Math.cos(st.ang.Q) * 1.5, y: Math.sin(st.ang.Q) * 1.5, color: '#1d4ed8' });
        const C = sheet.handle({ label: 'C', x: 0, y: 1.2, color: '#7c3aed' });
        const sa = sheet.seg([0, 0], [0, 0], { color: '#9ca3af', dash: true, width: 1.4 }); const sb = sheet.seg([0, 0], [0, 0], { color: '#9ca3af', dash: true, width: 1.4 });
        st.hd = { A, B, C };
        const upd = () => { sa.a = [A.x, A.y]; sa.b = [C.x, C.y]; sb.a = [B.x, B.y]; sb.b = [C.x, C.y]; sheet.redraw(); sheet.read(`OA = <b>${Math.hypot(A.x, A.y).toFixed(2)} cm</b> · OB = <b>${Math.hypot(B.x, B.y).toFixed(2)} cm</b> · OC = <b>${Math.hypot(C.x, C.y).toFixed(2)} cm</b>`); };
        sheet.onChange(upd); upd(); sheet.show(true);
        hud.actions([{ id: 'chk', label: 'Draw diagonal OC', primary: true, onClick: check }]);
      },
      exit() { hud.actions([]); },
      skip() { st.ang = { P: dirOf('P'), Q: dirOf('Q'), R: dirOf('R') }; const p = H.P.grams / SCALE; const q = H.Q.grams / SCALE; st.res = { x: p * Math.cos(st.ang.P) + q * Math.cos(st.ang.Q), y: p * Math.sin(st.ang.P) + q * Math.sin(st.ang.Q) }; },
    },
  ];
  function check() {
    const { A, B, C } = st.hd; const p = H.P.grams / SCALE; const q = H.Q.grams / SCALE;
    const oa = Math.hypot(A.x, A.y); const ob = Math.hypot(B.x, B.y);
    if (Math.abs(oa - p) > 0.1) { ctx.mistake(`OA should be P to scale: ${H.P.grams} g-wt ÷ 50 = ${p.toFixed(1)} cm, not ${oa.toFixed(2)} cm.`, 3); return; }
    if (Math.abs(ob - q) > 0.1) { ctx.mistake(`OB should be ${H.Q.grams} ÷ 50 = ${q.toFixed(1)} cm, not ${ob.toFixed(2)} cm.`, 3); return; }
    const cx = A.x + B.x; const cy = A.y + B.y;
    if (Math.hypot(C.x - cx, C.y - cy) > 0.2) { ctx.mistake('C is not the fourth corner: AC must be parallel and equal to OB, and BC parallel and equal to OA.', 3); return; }
    st.res = { x: C.x, y: C.y };
    sheet.seg([0, 0], [C.x, C.y], { color: '#7c3aed', width: 3.2 });
    const Rd = Math.hypot(C.x, C.y) * SCALE;
    sheet.read(`OC = <b>${Math.hypot(C.x, C.y).toFixed(2)} cm</b> → resultant <b>${Rd.toFixed(0)} g-wt</b>; R = ${H.R.grams} g-wt`);
    ui.observe('Resultant OC', `<b>${Rd.toFixed(0)} g-wt</b>`); hud.actions([]);
    anim.wait(1.6, () => { sheet.show(false); ctx.next(`The diagonal is ${Rd.toFixed(0)} g-wt, against R = ${H.R.grams} g-wt.`, 1.0); });
  }

  ctx.debug = { st, H, equilibrium, check };
  layout();
  return {
    tools: [], steps,
    update(dt) { step(dt); layout(); hud.update(); },
    result() {
      const r = st.res || { x: 0, y: 0 }; const Rd = Math.hypot(r.x, r.y) * SCALE; const R = H.R.grams;
      const ang = THREE.MathUtils.radToDeg(Math.atan2(r.x, r.y));
      const gam = THREE.MathUtils.radToDeg(Math.abs(st.ang.P - st.ang.Q));
      const calc = Math.sqrt(H.P.grams ** 2 + H.Q.grams ** 2 + 2 * H.P.grams * H.Q.grams * Math.cos(THREE.MathUtils.degToRad(gam)));
      const err = (Rd - R) / R * 100;
      return {
        title: 'Parallelogram law',
        rows: [['P, Q', `${H.P.grams}, ${H.Q.grams} g-wt`], ['Angle between P and Q', `${gam.toFixed(1)}°`], ['Diagonal OC', `${Rd.toFixed(0)} g-wt`], ['√(P²+Q²+2PQcosγ)', `${calc.toFixed(0)} g-wt`], ['R (hung)', `${R} g-wt`], ['OC from vertical', `${Math.abs(ang).toFixed(1)}°`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: `The diagonal of the parallelogram on P and Q is equal to R within ${Math.abs(err).toFixed(1)} % and points straight up, opposite to R: the resultant of P and Q is the equilibrant of R. The small difference comes from pulley friction and from marking the threads.`,
      };
    },
    dispose() { hud.dispose(); sheet.dispose(); dotMeshes.forEach((m) => world.remove(m)); dotGeo.dispose(); },
  };
}
