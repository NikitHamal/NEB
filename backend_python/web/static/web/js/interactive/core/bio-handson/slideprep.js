// Making a temporary mount and looking at it, as reusable steps: a drop of stain or water from
// the dropper, the coverslip lowered at an angle with a needle (too fast and air is trapped),
// excess blotted, the slide laid on the microscope stage under the clips, then focusing under
// low power and moving to high power. A practical builds a station and picks the steps it needs.
import { THREE } from '../engine.js';
import { slide as makeSlide, coverslip as makeCoverslip, drop as makeDrop, filterPaper } from './props.js';
import { buildMicroscope, tile } from './microscope.js';
import { createEyepiece } from './eyepiece.js';
import { ease, clamp } from './kit.js';

export function buildStation(ctx, opts = {}) {
  const { world } = ctx;
  const st = { bubbles: 0, drops: 0, stainColor: opts.stainColor ?? 0x9f1239, specimen: null, onStage: false };
  const t = tile(1.7, 1.2); t.position.set(opts.tileX ?? 0.1, 0, opts.tileZ ?? 0.35); world.add(t);
  st.tile = t;
  const s = makeSlide(); s.position.set((opts.tileX ?? 0.1) + (opts.slideDX ?? 0.35), 0.03, (opts.tileZ ?? 0.35) + 0.15); world.add(s);
  st.slide = s;
  st.slideTopY = 0.03 + s.userData.top;
  const cs = new THREE.Group(); const csMesh = makeCoverslip(); csMesh.position.x = 0.11; cs.add(csMesh);
  cs.position.set(s.position.x + 0.55, st.slideTopY - 0.011, s.position.z); world.add(cs);
  st.coverslip = cs;
  const scope = buildMicroscope();
  scope.root.position.set(opts.scopeX ?? 1.95, 0, opts.scopeZ ?? -0.55); scope.root.rotation.y = opts.scopeRot ?? -0.35;
  world.add(scope.root);
  st.scope = scope;
  st.center = new THREE.Vector3();
  st.slideCenter = (out) => out.set(s.position.x, st.slideTopY, s.position.z).applyMatrix4(world.matrixWorld);
  return st;
}

const tmp = new THREE.Vector3();

export function stepDrop(ctx, st, o) {
  let drop = null;
  const s = {
    title: o.title, text: o.text, hint: o.hint || 'Pick up the dropper and tap the middle of the slide once.', tool: 'dropper', shot: o.shot,
    enter() { s.onTool(); },
    onTool() { const m = ctx.tools.id === 'dropper' && ctx.tools.model; if (m && m.userData.liquid) m.userData.liquid.material.color.setHex(o.color); },
    skip() { this.place(1); },
    place(n) {
      if (!drop) { drop = makeDrop(o.color, 0.7); drop.position.set(st.slide.position.x, st.slideTopY, st.slide.position.z); ctx.world.add(drop); st.drop = drop; }
      st.drops += n;
      const r = 0.035 + 0.012 * st.drops; const h = 0.012 + 0.003 * st.drops;
      const from = drop.scale.clone();
      ctx.anim.add(0.35, (k) => drop.scale.set(from.x + (r - from.x) * k, from.y + (h - from.y) * k, from.z + (r - from.z) * k), { ease: ease.outBack });
    },
    handler: {
      down(p) {
        const h = ctx.input.pick([st.slide], true);
        if (!h) return false;
        if (!ctx.requireTool('dropper')) return true;
        ctx.tools.action(1); ctx.anim.wait(0.15, () => ctx.tools.action(0));
        ctx.sfx.play('drop');
        s.place(1);
        if (st.drops === 1) ctx.anim.wait(0.5, () => ctx.next(o.done || 'One drop is enough.'));
        else if (st.drops === 2) ctx.mistake('One drop is enough — extra liquid floats the coverslip and washes the specimen out from under it.', 2);
        return true;
      },
    },
  };
  return s;
}

/** Lowering the coverslip with a needle: drag downward; the angle follows. Too fast traps air. */
export function stepCoverslip(ctx, st, o = {}) {
  let angle = 0.78; let holding = false; let lastY = 0; let lastT = 0; let maxSpeed = 0; let done = false;
  const cs = st.coverslip; const pivotX = () => st.slide.position.x - 0.11;
  const bubbleMeshes = [];
  function placeAtAngle(a) { cs.rotation.z = a; }
  function settle() {
    done = true;
    st.bubbles = clamp(Math.round((maxSpeed - 2.4) / 1.3), 0, 4);
    for (let i = 0; i < st.bubbles; i++) {
      const b = new THREE.Mesh(new THREE.TorusGeometry(0.012 + Math.random() * 0.012, 0.002, 6, 20), new THREE.MeshBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.6 }));
      b.rotation.x = Math.PI / 2; b.position.set(st.slide.position.x + (Math.random() - 0.5) * 0.14, st.slideTopY + 0.004, st.slide.position.z + (Math.random() - 0.5) * 0.14);
      ctx.world.add(b); bubbleMeshes.push(b);
    }
    if (st.drop) { const d = st.drop; const f = d.scale.clone(); ctx.anim.add(0.4, (k) => d.scale.set(f.x + (0.105 - f.x) * k, f.y + (0.003 - f.y) * k, f.z + (0.105 - f.z) * k)); }
    ctx.sfx.play('place');
    if (st.bubbles > 0) ctx.mistake(`You lowered it too fast: ${st.bubbles} air bubble${st.bubbles > 1 ? 's are' : ' is'} trapped. Bubbles look like thick black rings under the microscope and hide cells. Lower it slowly next time.`, 3 + st.bubbles);
    ctx.anim.wait(0.8, () => ctx.next(st.bubbles ? null : 'Lowered slowly at an angle, so the liquid pushed the air out ahead of it: no bubbles.'));
  }
  return {
    title: o.title || 'Lower the coverslip', text: o.text || 'Rest one edge of the coverslip on the slide beside the drop, support the other edge on the <b>needle</b>, then lower it <b>slowly</b> by dragging down.',
    hint: 'Hold the needle (drag on the slide) and move down slowly. A slow, steady lowering lets the liquid spread and push the air out.',
    tool: 'needle', shot: o.shot,
    enter() {
      ctx.anim.add(0.8, (k) => {
        cs.position.set(pivotX() + (1 - k) * 0.5, st.slideTopY + 0.001 + (1 - k) * 0.1, st.slide.position.z);
        placeAtAngle(0.78 * k);
      }, { ease: ease.inOut });
    },
    skip() { cs.position.set(pivotX(), st.slideTopY + 0.001, st.slide.position.z); placeAtAngle(0); if (st.drop) st.drop.scale.set(0.105, 0.003, 0.105); },
    aim(p, out) {
      const tip = tmp.set(Math.cos(angle) * 0.22, Math.sin(angle) * 0.22, 0);
      out.set(pivotX() + tip.x, st.slideTopY + tip.y, st.slide.position.z).applyMatrix4(ctx.world.matrixWorld);
      return true;
    },
    update() {
      if (holding) { /* the needle rides on the coverslip's raised edge */ }
    },
    handler: {
      down(p) {
        if (done) return true;
        if (!ctx.requireTool('needle', 'Support the coverslip on the <b>dissecting needle</b> to lower it gently.')) return true;
        holding = true; lastY = p.y; lastT = performance.now(); ctx.tools.press(0.3); return true;
      },
      move(p) {
        if (!holding || done) return;
        const now = performance.now(); const dy = p.y - lastY; const dtm = Math.max(8, now - lastT);
        lastY = p.y; lastT = now;
        if (dy <= 0) return;
        const da = dy * 0.0045;
        const speed = da / (dtm / 1000);
        maxSpeed = Math.max(maxSpeed * 0.9, speed);
        angle = Math.max(0, angle - da);
        placeAtAngle(angle);
        ctx.progress(1 - angle / 0.78);
        if (angle <= 0.001) { holding = false; ctx.tools.press(0); settle(); }
      },
      up() {
        if (!holding || done) return;
        holding = false; ctx.tools.press(0);
        if (angle > 0.05) {
          const from = angle; maxSpeed = Math.max(maxSpeed, 2.6 + from * 3);
          ctx.say('You let go — the coverslip dropped flat.', 'hint', 2500);
          ctx.anim.add(0.12, (k) => { angle = from * (1 - k); placeAtAngle(angle); }, { ease: ease.in, done: settle });
        }
      },
    },
    exit() { },
    dispose() { bubbleMeshes.forEach((b) => { ctx.world.remove(b); b.geometry.dispose(); b.material.dispose(); }); },
  };
}

export function stepBlot(ctx, st, o = {}) {
  let paper = null;
  return {
    title: o.title || 'Blot away the excess', text: o.text || 'Touch the <b>blotting paper</b> to the edge of the coverslip to draw off the extra liquid.',
    hint: 'Pick up the blotting paper and tap the edge of the coverslip.', tool: 'paper', shot: o.shot,
    skip() { if (st.drop) st.drop.scale.set(0.11, 0.0025, 0.11); },
    handler: {
      down() {
        const h = ctx.input.pick([st.slide, st.coverslip], true); if (!h) return false;
        if (!ctx.requireTool('paper')) return true;
        if (!paper) { paper = filterPaper(0.2, 0.1); paper.material = paper.material.clone(); paper.position.set(st.slide.position.x + 0.18, st.slideTopY + 0.004, st.slide.position.z); ctx.world.add(paper); }
        ctx.sfx.play('squish');
        ctx.anim.add(0.6, (k) => { paper.material.color.setRGB(1 - k * 0.15, 1 - k * 0.5, 1 - k * 0.45); });
        ctx.anim.wait(0.9, () => { ctx.world.remove(paper); ctx.next('The excess liquid soaked into the paper; the mount is now thin and even.'); });
        return true;
      },
    },
  };
}

/** Lift the slide onto the stage; it travels on an arc and slides under the clips. */
export function stepToStage(ctx, st, o = {}) {
  const shot = o.shot || stageShot(st);
  return {
    title: o.title || 'Place the slide on the stage', text: o.text || 'Tap the slide to lift it onto the microscope stage, coverslip up, under the clips.',
    hint: 'Tap the slide on the tile.', tool: 'hand', shot: o.shotStart, autoTool: 'hand',
    skip() { moveSlide(ctx, st, 1); },
    handler: {
      down() {
        const h = ctx.input.pick([st.slide, st.coverslip], true); if (!h) return false;
        ctx.sfx.play('pick'); ctx.rig.go(shot, 1.6);
        ctx.anim.add(1.4, (k) => moveSlide(ctx, st, k), { ease: ease.inOut, done: () => { ctx.sfx.play('click'); ctx.next('Slide on the stage, held by the clips, specimen over the aperture.'); } });
        return true;
      },
    },
  };
}
export function stageShot(st) {
  const p = new THREE.Vector3(0, 1.7, 0); st.scope.root.localToWorld(p); p.y += 0.8;
  const pos = new THREE.Vector3(0.9, 2.5, 3.2); st.scope.root.localToWorld(pos); pos.y = p.y + 0.9;
  return { pos: [pos.x, pos.y, pos.z], target: [p.x, p.y, p.z], fit: 2.4 };
}
const SLIDE_FROM = new THREE.Vector3(); const SLIDE_TO = new THREE.Vector3(); const Q0 = new THREE.Quaternion(); const Q1 = new THREE.Quaternion(); const EUL = new THREE.Euler();
export function moveSlide(ctx, st, k) {
  if (k === 0 || !st._slideFrom) {
    st._slideFrom = st.slide.position.clone(); st._rot0 = st.slide.quaternion.clone();
    st.slideParts = st.slideParts || [st.coverslip, st.drop, st.specimen].filter(Boolean).map((m) => ({ m, off: m.position.clone().sub(st.slide.position), q: m.quaternion.clone() }));
  }
  SLIDE_FROM.copy(st._slideFrom);
  // the stage top, in the world group's frame
  SLIDE_TO.set(0, st.scope.stage.position.y + st.scope.stageTop, st.scope.stage.position.z);
  st.scope.root.localToWorld(SLIDE_TO); ctx.world.worldToLocal(SLIDE_TO);
  Q0.copy(st._rot0); Q1.setFromEuler(EUL.set(0, st.scope.root.rotation.y, 0));
  const p = st.slide.position.lerpVectors(SLIDE_FROM, SLIDE_TO, k);
  p.y += Math.sin(Math.PI * k) * 0.6;
  st.slide.quaternion.slerpQuaternions(Q0, Q1, k);
  st.slideParts.forEach(({ m, off, q }) => { m.position.copy(off).applyQuaternion(st.slide.quaternion).add(p); m.quaternion.copy(st.slide.quaternion).multiply(q); });
  if (k >= 1) st.onStage = true;
}

/**
 * Looking through the microscope: the camera flies to the eyepiece and the view opens. Returns
 * a controller the practical's microscope steps share: it syncs the 3D nosepiece and stage.
 */
export function createScopeView(ctx, st, field, opts = {}) {
  const scope = st.scope;
  let eye = null; let turretAnim = null;
  const view = {
    get eye() { return eye; },
    open(cb) {
      const top = new THREE.Vector3(0, 3.1, 0); scope.eyepiece.getWorldPosition(top);
      ctx.rig.go({ pos: [top.x + 0.15, top.y + 0.55, top.z + 0.35], target: [top.x, top.y, top.z] }, 1.1);
      if (!eye) {
        eye = createEyepiece(ctx, field, Object.assign({
          onMistake: (t, p) => ctx.mistake(t, p),
          onObjective: (m) => {
            const i = [4, 10, 40].indexOf(m); if (i < 0) return;
            const from = scope.turretAngle; const to = scope.turretGoal(i);
            if (turretAnim) ctx.anim.cancel(turretAnim);
            turretAnim = ctx.anim.add(0.5, (k) => scope.setTurret(from + (to - from) * k), { ease: ease.outBack });
          },
          onFocus: (d) => scope.setFocus(clamp(eye ? eye.state.focus : 0, -3000, 600) * 0.00004, d * 0.01),
          onClose: () => view.close(),
        }, opts));
      }
      ctx.ui.showBelt(false);
      ctx.anim.wait(0.9, () => { eye.show(true); if (cb) cb(); });
    },
    close() {
      if (eye) eye.show(false);
      ctx.ui.showBelt(true);
      ctx.rig.go(stageShot(st), 1.0);
      if (opts.onClosed) opts.onClosed();
    },
    update(t) { if (eye) eye.update(t); },
    dispose() { if (eye) eye.dispose(); eye = null; },
  };
  return view;
}
