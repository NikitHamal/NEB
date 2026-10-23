// The human skeleton on its stand, for both NEB practicals. Skeleton and joints: drag five loose
// bones from the bench to their places, classify the joints (fibrous, cartilaginous, and the
// synovial ball-and-socket, hinge, pivot and gliding types), then move them: flex the elbow (one
// plane only), swing the arm round (circumduction at the shoulder) and turn the head on the atlas.
// Health disorders: read a patient's case card, find the affected bone or joint on the skeleton,
// name the disorder and the care, then bend a healthy and an arthritic knee and compare the range
// of motion read from a goniometer.
import { THREE } from '../../engine.js';
import { buildSkeleton, longBone } from '../specimens/skeleton.js';
import { ask, sheet, table } from '../bench.js';
import { clamp, ease, rng } from '../kit.js';
import { createHud } from '../../handson/hud.js';

const BY = 0.8; const SZ = 3.9; const FLOOR = -0.8;
const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + BY + FLOOR, pos[2]], target: [target[0], target[1] + BY + FLOOR, target[2]], fit, fitH });
const TYPES = [['ball', 'Ball and socket'], ['hinge', 'Hinge'], ['pivot', 'Pivot'], ['gliding', 'Gliding'], ['cart', 'Cartilaginous (slightly movable)'], ['fib', 'Fibrous (immovable)']];
const JOINTS = [
  ['Skull sutures', 'fib', 'Sutures: the skull bones are locked together by fibrous tissue — immovable.'],
  ['Atlas–axis (neck)', 'pivot', 'Pivot: the atlas turns round the peg (odontoid process) of the axis — shaking the head “no”.'],
  ['Shoulder', 'ball', 'Ball and socket: the round head of the humerus in the glenoid cavity of the scapula — movement in every plane.'],
  ['Elbow', 'hinge', 'Hinge: humerus with ulna — bending and straightening in one plane only.'],
  ['Wrist (carpals)', 'gliding', 'Gliding: the carpals slide a little over one another.'],
  ['Intervertebral discs', 'cart', 'Cartilaginous: pads of fibrocartilage between vertebrae allow slight movement and absorb shock.'],
  ['Pubic symphysis', 'cart', 'Cartilaginous: the two pubic bones joined by a fibrocartilage pad — slightly movable.'],
  ['Hip', 'ball', 'Ball and socket: the head of the femur in the acetabulum — deep and stable.'],
  ['Knee', 'hinge', 'Hinge: femur on tibia, the patella in front — the largest synovial joint.'],
];
const CASES = [
  { text: 'Mrs. Sharma, 68, has back pain and a stoop; she broke her wrist in a minor fall. Her bones are thin and porous.', site: ['Lumbar spine', 'Wrist (carpals)'], dis: 'Osteoporosis', care: 'Calcium, vitamin D, weight-bearing exercise; prevent falls' },
  { text: 'Mr. Rai, 45, woke at night with a red, hot, very painful big toe after a feast of meat and alcohol. Uric acid is high.', site: ['Big toe joint'], dis: 'Gout', care: 'Less red meat and alcohol, plenty of water, drugs to lower uric acid' },
  { text: 'Hari, 62 and overweight, has knee pain that grows worse with walking; the cartilage has worn thin.', site: ['Knee'], dis: 'Osteoarthritis', care: 'Weight loss, gentle exercise, physiotherapy' },
  { text: 'Sita, 40, has painful, swollen finger joints on both hands, stiff for an hour every morning.', site: ['Finger joints', 'Wrist (carpals)'], dis: 'Rheumatoid arthritis', care: 'Early treatment by a doctor, joint exercises' },
  { text: 'Bikash lifted a heavy sack with his back bent and felt a sharp pain shooting down his leg.', site: ['Lumbar spine', 'Intervertebral discs'], dis: 'Slipped (herniated) disc', care: 'Rest, physiotherapy; lift with bent knees and a straight back' },
  { text: 'A boy fell on his outstretched arm; the round head of his arm bone has come out of its socket.', site: ['Shoulder'], dis: 'Dislocation', care: 'Do not force it; immobilise and get it reduced by a doctor' },
  { text: 'A footballer twisted her ankle; the ligaments are stretched and torn, the ankle swollen.', site: ['Ankle'], dis: 'Sprain', care: 'Rest, ice, compression, elevation (RICE)' },
  { text: 'A small child with little sunlight and poor diet has soft bones and bowed legs.', site: ['Thigh', 'Leg', 'Knee'], dis: 'Rickets', care: 'Vitamin D (sunlight), calcium-rich food' },
];

export function create(ctx) { return ctx.config.slug.startsWith('skeleton-joints-health') ? disorders(ctx) : joints(ctx); }

function setup(ctx) {
  const sk = buildSkeleton(); sk.root.position.set(0, FLOOR, SZ); ctx.world.add(sk.root);
  const layer = document.createElement('div'); layer.className = 'bh-jlayer'; ctx.ui.root.appendChild(layer);
  const dots = []; const v = new THREE.Vector3();
  const api = {
    sk,
    site(name, out) { return out.copy(sk.sites[name]).applyMatrix4(sk.root.matrixWorld); },
    dot(name, label, onTap) {
      const d = document.createElement('button'); d.type = 'button'; d.className = 'bh-jdot'; d.textContent = label; layer.appendChild(d);
      d.addEventListener('click', (e) => { e.stopPropagation(); onTap(d); });
      const o = { name, el: d }; dots.push(o); return o;
    },
    clearDots() { dots.splice(0).forEach((o) => o.el.remove()); },
    update() {
      const w = ctx.stage.clientWidth; const h = ctx.stage.clientHeight;
      dots.forEach((o) => { api.site(o.name, v); ctx.input.project(v, v, w, h); o.el.style.transform = `translate(${v.x}px, ${v.y}px)`; });
    },
    /** The named site nearest the pointer (screen px), within r. */
    nearest(p, r = 55) { let best = null; let bd = r * (p.touch ? 1.3 : 1); const w = ctx.stage.clientWidth; const h = ctx.stage.clientHeight; Object.keys(sk.sites).forEach((n) => { api.site(n, v); ctx.input.project(v, v, w, h); const d = Math.hypot(v.x - p.x, v.y - p.y); if (d < bd) { bd = d; best = n; } }); return best; },
    screenOf(obj, out) { obj.getWorldPosition(out); return ctx.input.project(out, out, ctx.stage.clientWidth, ctx.stage.clientHeight); },
    dispose() { layer.remove(); },
  };
  return api;
}
const FULL = S([1.5, 9.5, SZ + 25], [0, 8.7, SZ], 9, 18.5);
const SIDE_ARM = S([-13, 12, SZ + 3], [-1.9, 11.0, SZ], 6, 7);
const FRONT_ARM = S([-3, 12.5, SZ + 14], [-2.0, 12.0, SZ], 9, 9.5);
const HEAD = S([1.5, 16.5, SZ + 7], [0, 16.5, SZ], 3.5, 3.5);
const SIDE_LEG = S([-13, 4.5, SZ + 3], [-0.9, 4.5, SZ], 6, 7);

function joints(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const R = rng((Date.now() & 0xffff) || 3);
  const st = setup(ctx); const { sk } = st;
  const hud = createHud(ctx); const chip = hud.chip('ho-chip-read');
  const MISSING = ['Mandible', 'Humerus', 'Femur', 'Patella', 'Tibia'];
  const loose = MISSING.map((name, i) => {
    const orig = sk.B[name]; orig.visible = false;
    const copy = orig.clone(true); copy.visible = true; copy.userData.name = name;
    const holder = new THREE.Group(); holder.add(copy); copy.position.set(0, 0, 0); copy.quaternion.identity();
    const box = new THREE.Box3().setFromObject(copy); const c = box.getCenter(new THREE.Vector3()); copy.position.sub(c);
    holder.position.set(2.6 + (i % 3) * 1.6 + R() * 0.2, 0.25, SZ - 1.5 - Math.floor(i / 3) * 1.4); holder.rotation.set(Math.PI / 2, 0, 0.3 + R() * 0.6);
    world.add(holder);
    orig.updateMatrixWorld(true); const tb = new THREE.Box3().setFromObject(Object.assign(orig, { visible: true })); orig.visible = false;
    const target = tb.getCenter(new THREE.Vector3()); world.worldToLocal(target);
    const tq = new THREE.Quaternion(); orig.getWorldQuaternion(tq);
    return { name, orig, holder, copy, target, tq, home: holder.position.clone(), homeQ: holder.quaternion.clone(), placed: false };
  });
  const tmp = new THREE.Vector3(); const plane = new THREE.Plane(); let held = null;
  const BENCH = S([5, 9.5, SZ + 26], [2.6, 8.3, SZ - 0.5], 13, 20);
  const stepBuild = {
    title: 'Put the missing bones back', text: 'Five bones have come off the skeleton and lie on the bench. Drag each one to its place on the skeleton.',
    tool: null, autoTool: 'hand', hideBelt: true, shot: BENCH,
    skip() { loose.forEach((b) => { if (!b.placed) snap(b, true); }); },
    handler: {
      down() {
        const h = input.pick(loose.filter((b) => !b.placed).map((b) => b.holder), true); if (!h) return false;
        held = loose.find((b) => { let o = h.object; while (o) { if (o === b.holder) return true; o = o.parent; } return false; });
        if (!held) return false; sfx.play('grab'); return true;
      },
      move() {
        if (!held) return; tmp.set(0, 0, 1); plane.setFromNormalAndCoplanarPoint(tmp, world.localToWorld(new THREE.Vector3(0, 0, SZ + 0.8)));
        const hit = input.ptr.ray.intersectPlane(plane, new THREE.Vector3()); if (!hit) return; world.worldToLocal(hit);
        held.holder.position.lerp(hit, 0.6);
        const d = held.holder.position.distanceTo(held.target); const k = clamp(1 - (d - 1) / 6);
        held.holder.quaternion.slerpQuaternions(held.homeQ, held.tq, k);
      },
      up() {
        if (!held) return; const b = held; held = null;
        const w = ctx.stage.clientWidth; const h = ctx.stage.clientHeight; const p = new THREE.Vector3(); const q = new THREE.Vector3();
        let best = null; let bd = 90;
        loose.forEach((o) => { if (o.placed) return; p.copy(o.target); world.localToWorld(p); input.project(p, p, w, h); q.copy(b.holder.position); world.localToWorld(q); input.project(q, q, w, h); const d = Math.hypot(p.x - q.x, p.y - q.y); if (d < bd) { bd = d; best = o; } });
        if (best === b) { snap(b, false); return; }
        if (best) ctx.mistake(`That place is for the <b>${best.name.toLowerCase()}</b>. ${HINT[b.name]}`, 2); else ctx.say('Bring it right up to where it belongs.', 'hint', 1600);
        const from = b.holder.position.clone(); const q0 = b.holder.quaternion.clone();
        anim.add(0.6, (k) => { b.holder.position.lerpVectors(from, b.home, k); b.holder.quaternion.slerpQuaternions(q0, b.homeQ, k); }, { ease: ease.out });
      },
    },
  };
  const HINT = { Mandible: 'The lower jaw hinges just in front of the ears.', Humerus: 'The upper-arm bone runs from the shoulder to the elbow.', Femur: 'The thigh bone, the longest in the body, runs from the hip to the knee.', Patella: 'The kneecap sits in front of the knee joint.', Tibia: 'The shin bone runs from the knee to the ankle, beside the thin fibula.' };
  function snap(b, instant) {
    b.placed = true; const done = () => { world.remove(b.holder); b.orig.visible = true; ui.observe(b.name, 'in place'); };
    if (instant) { done(); return; }
    const from = b.holder.position.clone(); const q0 = b.holder.quaternion.clone(); sfx.play('place');
    anim.add(0.35, (k) => { b.holder.position.lerpVectors(from, b.target, k); b.holder.quaternion.slerpQuaternions(q0, b.tq, k); }, { done: () => { done(); ctx.say(`<b>${b.name}</b> — ${HINT[b.name]}`, 'good', 3200); if (loose.every((o) => o.placed)) anim.wait(0.8, () => ctx.next('The skeleton is complete.')); } });
  }
  const answers = {};
  const stepJoints = {
    title: 'Name the joints', text: 'Tap each numbered joint and choose its type.', tool: null, autoTool: 'hand', hideBelt: true, shot: FULL,
    enter() {
      JOINTS.forEach(([name, type, fact], i) => {
        const o = st.dot(name, String(i + 1), (el) => {
          if (answers[name]) return; const r = el.getBoundingClientRect(); const sr = ctx.stage.getBoundingClientRect();
          ui.choose(r.left - sr.left, r.top - sr.top, name, TYPES.map(([v, l]) => ({ label: l, value: v })), (v) => {
            if (v === type) { answers[name] = true; el.classList.add('done'); sfx.play('ok'); ctx.say(fact, 'good', 4600); ui.observe(name, TYPES.find((t) => t[0] === type)[1]); ctx.progress(Object.keys(answers).length / JOINTS.length); if (Object.keys(answers).length === JOINTS.length) { st.clearDots(); anim.wait(1, () => ctx.next()); } }
            else ctx.mistake(`Not ${TYPES.find((t) => t[0] === v)[1].toLowerCase()}. ${type === 'fib' || type === 'cart' ? 'Does this joint move freely at all?' : 'Think about the movements it allows.'}`, 2);
          });
        });
        void o;
      });
    },
    skip() { JOINTS.forEach(([n]) => { answers[n] = true; }); },
    exit() { st.clearDots(); ui.clearChooser(); },
  };
  const rom = {};
  const stepElbow = {
    title: 'Bend the elbow', text: 'Drag the right hand to bend the elbow as far as it goes, then straighten it. Watch the angle.', tool: null, autoTool: 'hand', hideBelt: true, shot: SIDE_ARM,
    skip() { rom.elbow = 145; },
    handler: {
      down() { return !!input.pick([sk.RA.el, sk.RA.sh], true) || true; },
      move(p) { const e = st.screenOf(sk.J.elbow, tmp); const a = Math.atan2(p.x - e.x, p.y - e.y); const flex = clamp(a, 0, 145 / 57.3); sk.J.elbow.rotation.x = -flex; rom.elbow = Math.max(rom.elbow || 0, flex * 57.3); },
      up() { if ((rom.elbow || 0) > 130 && !stepElbow.done) { stepElbow.done = true; ui.observe('Elbow flexion', `${Math.round(rom.elbow)}°`); anim.add(0.6, (k) => { sk.J.elbow.rotation.x *= 1 - k; }); ctx.next('About 145° of bending in a single plane: a hinge joint cannot move sideways.'); } },
    },
  };
  const sectors = new Set();
  const stepShoulder = {
    title: 'Swing the arm round', text: 'Now drag the right hand round in a big circle in front of the body. The shoulder lets the arm move in every direction (circumduction).',
    tool: null, autoTool: 'hand', hideBelt: true, shot: FRONT_ARM,
    skip() { for (let i = 0; i < 8; i++) sectors.add(i); },
    handler: {
      down() { return true; },
      move(p) {
        const s = st.screenOf(sk.J.shoulder, tmp); const dx = p.x - s.x; const dy = p.y - s.y; const L = Math.hypot(dx, dy); if (L < 20) return;
        const ang = Math.atan2(dx, dy); sk.J.shoulder.rotation.set(-0.45 * Math.abs(Math.sin(ang)), 0, ang);
        sectors.add(Math.floor(((ang + Math.PI) / (Math.PI * 2)) * 8) % 8); ctx.progress(sectors.size / 8);
        chip.set(`${sectors.size}/8 directions`).show(true); sk.J.shoulder.getWorldPosition(chip.at);
      },
      up() { if (sectors.size >= 7 && !stepShoulder.done) { stepShoulder.done = true; chip.show(false); anim.add(0.8, (k) => { sk.J.shoulder.rotation.x *= 1 - k; sk.J.shoulder.rotation.z *= 1 - k; }); ui.observe('Shoulder', 'circumduction'); ctx.next('Full circle: only a ball-and-socket joint allows circumduction.'); } },
    },
  };
  const turned = { l: false, r: false };
  const stepNeck = {
    title: 'Turn the head', text: 'Drag sideways across the skull to turn the head left and right — the “no” movement.', tool: null, autoTool: 'hand', hideBelt: true, shot: HEAD,
    skip() { turned.l = turned.r = true; },
    handler: {
      down(p) { this.x = p.x; this.r0 = sk.J.neck.rotation.y; return true; },
      move(p) { if (this.x === undefined) return; const r = clamp(this.r0 + (p.x - this.x) * 0.008, -1.25, 1.25); sk.J.neck.rotation.y = r; if (r > 1.0) turned.l = true; if (r < -1.0) turned.r = true; },
      up() { this.x = undefined; if (turned.l && turned.r && !stepNeck.done) { stepNeck.done = true; anim.add(0.6, (k) => { sk.J.neck.rotation.y *= 1 - k; }); ui.observe('Atlas–axis', 'rotation ±70°'); ctx.next('The atlas rotates round the axis: a pivot joint allows rotation about one axis only.'); } },
    },
  };
  const stepSum = {
    title: 'Joint type and movement', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: FULL,
    enter() { ask(ctx, 'Which joint allows the widest range of movement?', [{ label: 'Ball and socket (shoulder, hip)', value: 'ok' }, { label: 'Hinge (elbow, knee)', value: 'h' }, { label: 'Pivot (atlas–axis)', value: 'p' }, { label: 'Suture (skull)', value: 's' }], 'ok', { ok: 'Ball and socket: movement in all planes plus rotation. Hinges move in one plane, pivots rotate about one axis, gliding joints slide, cartilaginous joints barely move, and sutures not at all.', wrong: 'Think of the circle you drew with the arm.' }); },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepBuild, stepJoints, stepElbow, stepShoulder, stepNeck, stepSum];
  ctx.debug = { sk, loose, st };
  void longBone; void table; void sheet;
  return {
    tools: ['hand'], steps,
    update() { st.update(); hud.update(); },
    result() { return { title: 'Human skeleton and joints', rows: [['Bones replaced', `${loose.filter((b) => b.placed).length} of 5`], ['Joints classified', `${Object.keys(answers).length} of ${JOINTS.length}`], ['Elbow flexion', `${Math.round(rom.elbow || 0)}° (hinge, one plane)`], ['Shoulder', 'circumduction (ball and socket)'], ['Atlas–axis', 'rotation (pivot)']], conclusion: 'Bones meet at joints. Fibrous joints (skull sutures) are immovable, cartilaginous joints (intervertebral discs, pubic symphysis) slightly movable, and synovial joints freely movable: ball and socket (shoulder, hip) in all directions, hinge (elbow, knee) in one plane, pivot (atlas–axis) rotation, and gliding (carpals, tarsals) sliding.' }; },
    dispose() { st.dispose(); hud.dispose(); ui.clearChooser(); },
  };
}

function disorders(ctx) {
  const { input, anim, sfx, ui } = ctx;
  const R = rng((Date.now() & 0xffff) || 9);
  const st = setup(ctx); const { sk } = st;
  const hud = createHud(ctx); const gonio = hud.chip('ho-chip-read');
  const picks = CASES.slice().sort(() => R() - 0.5).slice(0, 5);
  const solved = [];
  function caseStep(c, k) {
    let phase = 'site';
    return {
      title: `Case ${k + 1}: where is the problem?`, text: `${c.text}<br><b>Tap the affected part of the skeleton.</b>`, tool: null, autoTool: 'hand', hideBelt: true, shot: FULL,
      enter() { phase = 'site'; },
      skip() { solved.push(c); },
      handler: { down(p) {
        if (phase !== 'site') return false;
        const n = st.nearest(p); if (!n) return false;
        if (!c.site.includes(n)) { ctx.mistake(`Not the ${n.toLowerCase()}. Read the case again: where is the pain or the damage?`, 2); return true; }
        phase = 'name'; sfx.play('ok');
        const opts = Array.from(new Set([c.dis, ...CASES.map((x) => x.dis).sort(() => R() - 0.5).slice(0, 4)])).slice(0, 4).sort(() => R() - 0.5);
        ask(ctx, `Affected: ${n}. The disorder is…`, opts.map((d) => ({ label: d, value: d })), c.dis, {
          delay: 0.2, wrong: 'Match the signs: age, the joint involved, swelling, cause.',
          then() {
            const cares = Array.from(new Set([c.care, ...CASES.filter((x) => x !== c).map((x) => x.care).sort(() => R() - 0.5).slice(0, 2)])).sort(() => R() - 0.5);
            ask(ctx, `${c.dis}: the right advice is…`, cares.map((t) => ({ label: t, value: t })), c.care, { delay: 0.2, ok: `${c.dis}: ${c.care}.`, wrong: 'Choose the care that tackles this disorder\'s cause.', then() { solved.push(c); ui.observe(`Case ${k + 1}`, c.dis); ctx.next(); } });
          },
        });
        return true;
      } },
      exit() { ui.clearChooser(); },
    };
  }
  const rom = { healthy: 0, patient: 0 };
  const knees = [];
  function kneeStep(who) {
    const limit = who === 'healthy' ? 135 : 72 + Math.round(R() * 10);
    return {
      title: who === 'healthy' ? 'Range of motion: a healthy knee' : 'Range of motion: an arthritic knee',
      text: who === 'healthy' ? 'Drag the foot backward to bend the knee as far as it will go. The goniometer shows the angle of flexion; let go at the end of the range.' : 'Now the same knee with osteoarthritis: worn cartilage and pain stop it early. Bend it as far as it goes.',
      tool: null, autoTool: 'hand', hideBelt: true, shot: SIDE_LEG,
      enter() { sk.J.knee.rotation.x = 0; },
      exit() { gonio.show(false); sk.J.knee.rotation.x = 0; },
      skip() { rom[who] = limit; },
      handler: {
        down() { return true; },
        move(p) {
          const e = st.screenOf(sk.J.knee, new THREE.Vector3()); const a = Math.atan2(-(p.x - e.x), p.y - e.y); const want = clamp(a, 0, 150 / 57.3);
          const lim = limit / 57.3; const f = want <= lim ? want : lim + (want - lim) * 0.05; sk.J.knee.rotation.x = f; const deg = Math.round(f * 57.3);
          gonio.set(`<b>${deg}°</b> flexion${who !== 'healthy' && want > lim ? ' — pain!' : ''}`).show(true); sk.J.knee.getWorldPosition(gonio.at); gonio.dx = 16;
          rom[who] = Math.max(rom[who], deg);
        },
        up() { if (rom[who] >= limit - 3 && !this.done) { this.done = true; gonio.show(false); ui.observe(`Knee, ${who}`, `${rom[who]}°`); anim.add(0.6, (k) => { sk.J.knee.rotation.x *= 1 - k; }); ctx.next(); } else if (!this.done) ctx.say('Keep bending until it will not go further.', 'hint', 1500); },
      },
    };
  }
  const stepCompare = {
    title: 'Compare and prevent', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: FULL,
    enter() {
      const lost = Math.round((1 - rom.patient / rom.healthy) * 100);
      ask(ctx, `Healthy ${rom.healthy}°, arthritic ${rom.patient}°. Range of motion lost =`, [lost, Math.round(rom.patient / rom.healthy * 100), lost + 15, rom.healthy - rom.patient].filter((v, i, a) => a.indexOf(v) === i).map((v) => ({ label: `${v} %`, value: v })), lost, {
        wrong: 'Lost fraction = (healthy − patient) ÷ healthy × 100.',
        then() { ui.observe('ROM lost', `${lost} %`); ask(ctx, 'Which habit best protects the spine and joints?', [{ label: 'Lift with bent knees and a straight back; keep a healthy weight', value: 'ok' }, { label: 'Lift by bending at the waist with straight legs', value: 'b' }, { label: 'Avoid all exercise to save the joints', value: 'x' }], 'ok', { delay: 0.3, ok: 'Good posture, safe lifting, regular weight-bearing exercise, a diet with calcium and vitamin D, and a healthy weight keep bones strong and joints working.', wrong: 'Bending the back under load squeezes the discs; inactivity weakens bones and muscles.' }); },
      });
    },
    exit() { ui.clearChooser(); },
  };
  const steps = [...picks.map((c, k) => caseStep(c, k)), kneeStep('healthy'), kneeStep('patient'), stepCompare];
  ctx.debug = { sk, st, picks };
  void knees; void sheet; void table;
  return {
    tools: ['hand'], steps,
    update() { st.update(); hud.update(); },
    result() { return { title: 'Skeleton, joints and disorders', rows: [['Cases solved', picks.filter((c) => solved.includes(c)).map((c) => c.dis).join(', ')], ['Knee flexion, healthy', `${rom.healthy}°`], ['Knee flexion, arthritic', `${rom.patient}° (${Math.round((1 - rom.patient / Math.max(1, rom.healthy)) * 100)} % lost)`]], conclusion: 'Disorders of bones and joints — osteoporosis, arthritis, gout, slipped disc, dislocation, sprain, rickets — show as pain and a reduced range of motion at particular joints. Most can be prevented or eased by good posture and lifting, exercise, a healthy weight, and enough calcium and vitamin D.' }; },
    dispose() { st.dispose(); hud.dispose(); ui.clearChooser(); },
  };
}
