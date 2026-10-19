// Spherometer: find the least count by turning the disc through one revolution, press the legs on
// paper and measure the leg separation l with a rule, then stand the spherometer on plane glass and
// turn the screw until the tip just touches its own reflection (rock it to check it is not
// over-driven), read the pitch scale and the disc; move it to the watch glass, raise the screw
// until it just touches again and read. h = b - a and R = l²/6h + h/2, from the student's readings.
import { THREE } from '../../engine.js';
import { MAT, mesh, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { spherometer, watchGlassCap, MM } from '../spherometer.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

function rulerTex() {
  return canvasTexture('ho-sph-rule', 4096, 160, (g, w, h) => {
    g.fillStyle = '#e7ebef'; g.fillRect(0, 0, w, h); g.fillStyle = '#0b0f14';
    const x = (mm) => 60 + (w - 120) * mm / 150;
    for (let mm = 0; mm <= 150; mm++) { const cm = mm % 10 === 0; const five = mm % 5 === 0; g.fillRect(Math.round(x(mm) - 2), 0, 4, cm ? 64 : five ? 46 : 30); if (cm) { g.font = '800 46px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(String(mm / 10), x(mm), 116); } }
    g.font = '600 26px system-ui, sans-serif'; g.textAlign = 'left'; g.fillText('cm', x(150) - 10, 150);
  }, { anisotropy: 16 });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const L_CM = [4.2, 4.5, 4.8, 5.0][Math.floor(Math.random() * 4)];
  const r0 = Math.round((3.2 + Math.random() * 2.5) * 100) / 100;
  const R_CM = Math.round(18 + Math.random() * 40);
  const sph = spherometer({ l: L_CM / 10, r0 });
  const cap = watchGlassCap(R_CM / 10);

  const plate = mesh(new THREE.BoxGeometry(1.1, 0.05, 0.9), new THREE.MeshPhysicalMaterial({ color: 0xbfe9e2, roughness: 0.02, transparent: true, opacity: 0.6, clearcoat: 1, envMapIntensity: 2, depthWrite: false }), [-0.9, 0.025, 0], { cast: false });
  plate.renderOrder = 4; world.add(plate);
  cap.mesh.position.set(0.45, 0, 0); world.add(cap.mesh);
  const paper = mesh(new THREE.BoxGeometry(0.9, 0.003, 0.7), MAT.paper(), [1.55, 0.0015, 0.35]); world.add(paper);
  const pricks = new THREE.Group(); pricks.visible = false; pricks.position.set(1.55, 0.004, 0.35); world.add(pricks);
  const pts = [0, 1, 2].map((i) => { const a = -Math.PI / 2 + i * Math.PI * 2 / 3; return new THREE.Vector3(Math.cos(a) * sph.rho, 0, Math.sin(a) * sph.rho); });
  pts.forEach((p) => { const d = mesh(new THREE.CircleGeometry(0.004, 12), MAT.ink(0x111827), [p.x, 0.0005, p.z]); d.rotation.x = -Math.PI / 2; pricks.add(d); });
  const ruler = mesh(new THREE.BoxGeometry(0.15 * 4096 / 3976, 0.002, 0.03), new THREE.MeshStandardMaterial({ map: rulerTex(), metalness: 0.6, roughness: 0.35 }), null); ruler.visible = false; pricks.add(ruler);
  world.add(sph.group);

  const SURF = { bench: { x: 0.2, z: 0.75, y: 0, s: null }, plate: { x: -0.9, z: 0, y: 0.05, s: 0 }, glass: { x: 0.45, z: 0, y: cap.heightAt(sph.rho), s: (cap.top - cap.heightAt(sph.rho)) / MM }, paper: { x: 1.55, z: 0.35, y: 0.003, s: 0 } };
  const H_TRUE = SURF.glass.s;
  const st = { on: 'bench', r: r0 + 2.4, read: { P: null, D: null }, a: null, b: null, l: [], rock: 0, lc: false, lastDiv: 0 };
  function surf() { return SURF[st.on]; }
  function over() { const s = surf().s; return s === null ? -1 : sph.tipMm() - s; }
  function place(name, dur = 0.9) {
    const from = sph.group.position.clone(); const S = SURF[name]; st.on = name;
    const to = new THREE.Vector3(S.x, S.y, S.z);
    anim.add(dur, (k) => { sph.group.position.lerpVectors(from, to, k); sph.group.position.y += Math.sin(k * Math.PI) * 0.35; }, { id: 'sph-move', done: () => { sfx.play('place'); settle(); } });
  }
  function settle() {
    const S = surf(); const o = over();
    sph.group.position.set(S.x, S.y + (o > 0 ? o * MM : 0), S.z);
    sph.setReflection(st.on === 'plate' || st.on === 'glass' ? S.s : null);
  }
  function setR(v) {
    const before = Math.floor(st.r * 100);
    st.r = Math.max(0.3, Math.min(11.7, v)); sph.set(st.r);
    if (Math.floor(st.r * 100) !== before) { st.lastDiv += 1; if (st.lastDiv % 3 === 0) sfx.play('knob'); }
    if (!anim.busy('sph-move')) settle();
  }
  setR(st.r); sph.group.position.set(SURF.bench.x, 0, SURF.bench.z);

  // ---- turning the disc ----
  const discPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); const hit = new THREE.Vector3(); const c = new THREE.Vector3();
  function discAngle() {
    sph.disc.getWorldPosition(c); discPlane.constant = -c.y;
    if (!ctx.input.ptr.ray.intersectPlane(discPlane, hit)) return null;
    const dx = hit.x - c.x; const dz = hit.z - c.z; if (Math.hypot(dx, dz) > sph.DISC_R * 2.2) return null;
    return Math.atan2(dz, dx);
  }
  const turnHandler = {
    a: null,
    down(p) { if (anim.busy('sph-move')) return false; const a = discAngle(); if (a === null && !hits(ctx, sph.disc, p, 70)) return false; this.a = a; return true; },
    move() { if (this.a === null) { this.a = discAngle(); return; } const a = discAngle(); if (a === null) return; let d = a - this.a; if (d > Math.PI) d -= Math.PI * 2; if (d < -Math.PI) d += Math.PI * 2; this.a = a; turn(-d / (Math.PI * 2)); },
    up() { this.a = null; }, cancel() { this.a = null; },
  };
  function turn(mm) {
    const o0 = over(); setR(st.r + mm); const o1 = over();
    if (o0 <= 0.012 && o1 > 0.012 && surf().s !== null) { sfx.play('click'); ctx.say('Felt that? The tip is now pressing on the glass and lifting a leg.', 'hint', 2200); }
  }
  function rockTest() {
    const o = over(); st.rock = o > 0.012 ? 1.6 : 0.35;
    sfx.play(o > 0.012 ? 'click' : 'place');
    if (o > 0.012) ctx.say('It <b>rocks</b> on the tip: the screw is driven too far and a leg is lifted. Raise it a little.', 'hint', 3000);
    else if (o < -0.02) ctx.say('Steady on its three legs — but is the tip touching? Look at the tip and its reflection.', 'hint', 3000);
    else ctx.say('Steady, and the tip meets its reflection: it just touches.', 'good', 2600);
  }
  let view = 'disc';
  const SHOT_ALL = shot({ pos: [0.3, 1.5, 2.6], target: [0.3, 0.1, 0.1], fit: 3.4, fitH: 1.4 });
  const discShot = () => { const S = surf(); return shot({ pos: [S.x + 0.05, S.y + 0.95, S.z + 0.95], target: [S.x, S.y + 0.2, S.z], fit: 0.9, fitH: 0.8 }); };
  const tipShot = () => { const S = surf(); const y = sph.group.position.y; return shot({ pos: [S.x + 0.003, y + 0.016, S.z + 0.1], target: [S.x, y + 0.002, S.z], fov: 26, limits: { yaw: 0.15, pitch: 0.1, zMin: 0.8, zMax: 1.3 } }); };
  const readShot = () => { const S = surf(); const y = S.y + sph.Z0 + st.r * MM + (over() > 0 ? over() * MM : 0); return shot({ pos: [S.x - 0.13, y + 0.012, S.z + sph.SCALE_X + 0.2], target: [S.x - 0.01, y - 0.006, S.z + sph.SCALE_X], fov: 24, limits: { yaw: 0.3, pitch: 0.2, zMin: 0.7, zMax: 1.4 } }); };
  function turnBar(onRead) {
    hud.actions([
      { id: 'up10', label: '↑10', onClick: () => turn(0.10) }, { id: 'up1', label: '↑1', onClick: () => turn(0.01) },
      { id: 'dn1', label: '↓1', onClick: () => turn(-0.01) }, { id: 'dn10', label: '↓10', onClick: () => turn(-0.10) },
      { id: 'view', label: 'Tip', onClick: () => { view = view === 'disc' ? 'tip' : 'disc'; hud.relabel('view', view === 'disc' ? 'Tip' : 'Disc'); ctx.rig.go(view === 'tip' ? tipShot() : discShot(), 0.8); } },
      { id: 'rock', label: 'Rock', onClick: rockTest },
      { id: 'read', label: 'Read', primary: true, onClick: onRead },
    ]);
    hud.root.querySelector('.ho-actions').classList.add('ho-tight');
  }

  // ---- reading the scales ----
  const scalePlane = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0);
  const mkP = mesh(new THREE.BoxGeometry(0.001, 0.0008, 0.03), new THREE.MeshBasicMaterial({ color: 0x2563eb, depthTest: false }), null, { cast: false }); mkP.renderOrder = 20; mkP.visible = false; world.add(mkP);
  const mkD = mesh(new THREE.ConeGeometry(0.004, 0.012, 3), new THREE.MeshBasicMaterial({ color: 0xdc2626, depthTest: false }), null, { cast: false }); mkD.renderOrder = 20; mkD.visible = false; world.add(mkD);
  const readHandler = {
    down() {
      const h = ctx.input.pick([sph.disc]);
      if (h) {
        const loc = sph.disc.worldToLocal(h.point.clone()); st.read.D = sph.divisionAt(loc);
        mkD.visible = true; mkD.position.copy(h.point); world.worldToLocal(mkD.position); mkD.position.y -= 0.022;
        sfx.play('click'); refreshRead(); return true;
      }
      const S = surf(); scalePlane.constant = -(S.x - 0.0032);
      if (!ctx.input.ptr.ray.intersectPlane(scalePlane, hit)) return false;
      world.worldToLocal(hit); if (Math.abs(hit.z - S.z - sph.SCALE_X - 0.013) > 0.035) return false;
      const base = sph.group.position.y + sph.Z0;
      const mm = Math.round((hit.y - base) / MM); if (mm < 0 || mm > 12) return false;
      st.read.P = mm; mkP.visible = true; mkP.position.set(S.x - 0.004, base + mm * MM, S.z + sph.SCALE_X + 0.013);
      sfx.play('click'); refreshRead(); return true;
    },
  };
  function refreshRead() {
    const a = st.read.P === null ? '—' : `${st.read.P} mm`; const b = st.read.D === null ? '—' : `${st.read.D}`;
    hud.relabel('rec', `Record · scale ${a} · disc ${b}`); hud.enable('rec', st.read.P !== null && st.read.D !== null);
  }
  function startRead(cb) {
    st.read = { P: null, D: null }; mkP.visible = mkD.visible = false;
    ctx.rig.go(readShot(), 1.0);
    hud.actions([{ id: 'back', label: 'Back', onClick: () => { stopRead(); cb(null); } }, { id: 'rec', label: 'Record', primary: true, disabled: true, onClick: () => { const v = st.read; stopRead(); cb(v); } }]);
    refreshRead();
    ctx.input.setHandler(wrap(readHandler));
  }
  function stopRead() { mkP.visible = mkD.visible = false; hud.actions([]); }
  function wrap(h) { return { down: (p) => h.down(p), move() {}, up() {}, hover() {}, tap() {}, cancel() {} }; }
  const truth = () => { const r = st.r + 1e-7; return { P: Math.floor(r), D: Math.round((r - Math.floor(r)) * 100) % 100, r: st.r }; };
  function checkReading(v) {
    const t = truth(); const val = v.P + v.D * 0.01;
    if (Math.abs(val - t.r) > 0.015 && Math.abs(val - t.r) < 0.985) {
      const okP = v.P === t.P || (t.D <= 1 && v.P === t.P - 1) || (t.D >= 99 && v.P === t.P + 1);
      ctx.mistake(okP ? `The disc division on the scale's edge is ${t.D}, not ${v.D}. Look straight along the edge.` : `The disc's upper face is between ${t.P} and ${t.P + 1} mm on the pitch scale: the pitch scale reading is ${t.P} mm.`, 3);
      return null;
    }
    if (Math.abs(val - t.r) >= 0.985) { ctx.mistake(`Pitch scale: the disc is just past ${t.P} mm (disc ${t.D}), so read ${t.P} mm.`, 3); return null; }
    return val;
  }
  function contactCheck() {
    const o = over();
    if (o > 0.012) { ctx.mistake(`Over-driven by ${(o * 100).toFixed(0)} divisions: the spherometer rocks on its tip. Raise the screw until the rocking just stops.`, 4); return false; }
    if (o < -0.022) { ctx.mistake(`The tip is still ${(-o).toFixed(2)} mm above the glass. Turn down until the tip meets its reflection.`, 4); return false; }
    return true;
  }

  function measureStep(kind) {
    const isA = kind === 'a';
    return {
      title: isA ? 'Zero reading on plane glass' : 'Reading on the watch glass',
      text: isA ? 'The spherometer stands on the <b>plane glass plate</b>. Drag the <b>disc</b> round (or use ↑ ↓, in divisions) until the tip <b>just touches</b> its reflection. Check with <b>Tip</b> and <b>Rock</b>, then <b>Read</b> the pitch scale and the disc.'
        : 'Now on the <b>watch glass</b> (convex side up). The centre of the glass is higher than the legs: <b>raise</b> the screw until it just touches again, check, and read.',
      hint: 'Clockwise (↓) lowers the tip. Just touching: the tip meets its image in the glass and the instrument does not rock on its tip.',
      shot: null, hideBelt: true,
      enter() { view = 'disc'; place(isA ? 'plate' : 'glass'); ctx.rig.go(discShot(), 1.4); turnBar(read);
        if (!isA) anim.wait(1.4, () => { if (over() > 0.012) ctx.say('It sits on its tip and rocks: the glass bulges up under the screw. Raise the screw.', 'hint', 3600); });
      },
      exit() { hud.actions([]); hud.root.querySelector('.ho-actions').classList.remove('ho-tight'); stopRead(); },
      skip() { place(isA ? 'plate' : 'glass', 0.01); anim.update(1); setR(r0 + SURF[isA ? 'plate' : 'glass'].s); const t = truth(); st[kind] = t.P + t.D * 0.01; },
      handler: turnHandler,
    };
    function read() {
      startRead((v) => {
        if (!v) { ctx.input.setHandler(wrap2(turnHandler)); ctx.rig.go(discShot(), 0.8); turnBar(read); return; }
        const val = checkReading(v); const contact = contactCheck();
        if (val === null || !contact) { anim.wait(0.6, () => { ctx.input.setHandler(wrap2(turnHandler)); ctx.rig.go(discShot(), 0.8); turnBar(read); }); return; }
        st[kind] = val;
        ui.observe(isA ? 'a (plane glass)' : 'b (watch glass)', `${v.P} + ${v.D} × 0.01 = <b>${val.toFixed(2)} mm</b>`);
        ctx.next(isA ? `a = ${val.toFixed(2)} mm.` : `b = ${val.toFixed(2)} mm.`);
      });
    }
  }
  function wrap2(h) { return { down: (p) => h.down(p), move: (p) => h.move(p), up: (p) => h.up(p), hover() {}, tap() {}, cancel: (p) => h.cancel(p) }; }

  // ---- measuring l on paper ----
  const rulerPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -(BY + 0.006));
  let side = 0;
  function layRuler(i) {
    const A = pts[i]; const B = pts[(i + 1) % 3]; const d = B.clone().sub(A); const ang = Math.atan2(d.z, d.x);
    const len = 0.15 * 4096 / 3976; const off = (60 / 4096) * len;
    ruler.rotation.set(0, -ang, 0); ruler.visible = true;
    const n = new THREE.Vector3(-d.z, 0, d.x).normalize().multiplyScalar(0.017);
    ruler.position.copy(A).addScaledVector(d.clone().normalize(), len / 2 - off).add(n); ruler.position.y = 0.002;
  }
  const mkL = mesh(new THREE.BoxGeometry(0.0012, 0.002, 0.045), new THREE.MeshBasicMaterial({ color: 0xdc2626, depthTest: false }), null, { cast: false }); mkL.renderOrder = 20; mkL.visible = false; pricks.add(mkL);
  let tapL = null;
  const lHandler = {
    down() {
      if (!ctx.input.ptr.ray.intersectPlane(rulerPlane, hit)) return false;
      world.worldToLocal(hit); hit.sub(pricks.position); hit.y = 0;
      const A = pts[side]; const B = pts[(side + 1) % 3]; const dir = B.clone().sub(A).normalize();
      const s = hit.clone().sub(A).dot(dir); if (s < -0.01 || s > 0.1) return false;
      tapL = Math.round(s * 100) / 10; mkL.visible = true; mkL.position.copy(A).addScaledVector(dir, tapL / 10); mkL.position.y = 0.004; mkL.rotation.y = ruler.rotation.y;
      hud.relabel('rec', `Record ${tapL.toFixed(1)} cm`); hud.enable('rec', true); sfx.play('click'); return true;
    },
  };
  const paperShot = () => { const m = pts[side].clone().add(pts[(side + 1) % 3]).multiplyScalar(0.5).add(pricks.position); return shot({ pos: [m.x, 0.42, m.z + 0.2], target: [m.x, 0, m.z], fov: 26, limits: { yaw: 0.3, pitch: 0.2, zMin: 0.7, zMax: 1.4 } }); };

  const steps = [
    {
      title: 'Pitch and least count', text: 'Drag the <b>disc</b> round through one whole turn and watch its upper face move along the <b>pitch scale</b>. How far does the screw move per turn, and what is one disc division worth?',
      hint: 'Drag round the edge of the disc, like turning a lid.', shot: shot({ pos: [0.32, 0.75, 1.55], target: [0.2, 0.22, 0.75], fit: 0.9, fitH: 0.75 }), hideBelt: true,
      enter() { st.lc0 = st.r; },
      update() {
        if (st.lc || Math.abs(st.r - st.lc0) < 1) return; st.lc = true;
        ui.choose(ctx.stage.clientWidth / 2, 60, 'One turn moved the disc 1 mm along the scale. With 100 disc divisions, least count =', [{ label: '0.01 mm', value: 1 }, { label: '0.1 mm', value: 0 }, { label: '1 mm', value: 2 }, { label: '0.001 mm', value: 3 }], (v) => {
          if (v !== 1) ctx.mistake('Least count = pitch ÷ disc divisions = 1 mm ÷ 100 = 0.01 mm.', 3);
          ui.observe('Pitch, L.C.', '1 mm, <b>0.01 mm</b>'); ctx.next('L.C. = 0.01 mm.');
        });
      },
      exit() { ui.clearChooser(); }, skip() { setR(st.r - 1); },
      handler: turnHandler,
    },
    {
      title: 'Leg separation l', text: 'Tap the <b>paper</b> to press the legs on it and leave three pricks. Then the rule is laid from one prick to the next: tap the rule at the <b>second prick</b> and record. Do all three sides.',
      hint: 'The rule\'s 0 is on the first prick. Read where the second prick falls, to half a millimetre.', shot: SHOT_ALL, hideBelt: true,
      enter() { side = 0; tapL = null; },
      exit() { hud.actions([]); mkL.visible = false; ruler.visible = false; },
      skip() { pricks.visible = true; st.l = [L_CM, L_CM, L_CM]; },
      handler: {
        down(p) {
          if (!pricks.visible) {
            if (!hits(ctx, paper, p, 80) && !hits(ctx, sph.group, p, 80)) return false;
            place('paper'); anim.wait(1.1, () => { pricks.visible = true; sfx.play('pin'); place('bench'); anim.wait(1.0, startSide); });
            return true;
          }
          return lHandler.down(p);
        },
      },
    },
    measureStep('a'),
    measureStep('b'),
    {
      title: 'Sagitta and radius', text: 'h = b − a, then R = l²/6h + h/2.', hideBelt: true, shot: SHOT_ALL,
      enter() {
        const l = st.l.reduce((x, y) => x + y, 0) / st.l.length; const h = (st.b - st.a) / 10; st.lMean = l; st.h = h;
        const R = l * l / (6 * h) + h / 2; st.R = R;
        const opts = [[R, 'l²/6h + h/2'], [l * l / (2 * h), 'l²/2h'], [l / (6 * h) + h / 2, 'l/6h + h/2'], [(l * l) / (6 * h * 10), 'with h left in mm ÷ 10 twice']].map(([v, w]) => ({ label: `${v.toFixed(1)} cm  (${w})`, value: v })).sort(() => Math.random() - 0.5);
        ui.observe('h = b − a', `<b>${(st.b - st.a).toFixed(2)} mm</b>`);
        anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 40, `l = ${l.toFixed(2)} cm, h = ${h.toFixed(3)} cm. Radius of curvature R =`, opts, (v) => {
          if (Math.abs(v - R) > 1e-6) ctx.mistake('Use R = l²/6h + h/2 with l and h both in cm.', 3);
          ui.observe('R', `<b>${R.toFixed(1)} cm</b>`); ctx.next(`R = ${R.toFixed(1)} cm.`, 1.2);
        }));
      },
      exit() { ui.clearChooser(); },
    },
  ];
  function startSide() {
    tapL = null; mkL.visible = false; layRuler(side); ctx.rig.go(paperShot(), 1.0);
    hud.actions([{ id: 'rec', label: 'Record', primary: true, disabled: true, onClick: () => {
      const truthL = L_CM;
      if (Math.abs(tapL - truthL) > 0.06) { ctx.mistake(`The second prick is at ${truthL.toFixed(1)} cm on the rule, not ${tapL.toFixed(1)} cm.`, 3); return; }
      st.l.push(tapL); ui.observe(`Side ${side + 1}`, `${tapL.toFixed(1)} cm`); sfx.play('ok');
      side += 1; if (side < 3) startSide(); else { hud.actions([]); ruler.visible = false; mkL.visible = false; ui.observe('l (mean)', `<b>${(st.l.reduce((a, b) => a + b, 0) / 3).toFixed(2)} cm</b>`); ctx.next(); }
    } }]);
  }

  ctx.debug = { st, sph, over, setR, place, truth, R_CM, H_TRUE, r0 };
  const q = new THREE.Quaternion(); const ax = new THREE.Vector3(1, 0, 0.3).normalize();
  return {
    tools: [], steps,
    update(dt, t) {
      if (st.rock > 0) { st.rock = Math.max(0, st.rock - dt); const amp = over() > 0.012 ? 0.03 : 0.004; q.setFromAxisAngle(ax, Math.sin(t * 22) * amp * Math.min(1, st.rock)); sph.group.quaternion.copy(q); }
      else sph.group.quaternion.identity();
      hud.update();
    },
    result() {
      const err = ((st.R || 0) - R_CM) / R_CM * 100;
      return {
        title: 'Spherometer',
        rows: [['l', `${(st.lMean || 0).toFixed(2)} cm`], ['a (plane)', `${(st.a ?? 0).toFixed(2)} mm`], ['b (watch glass)', `${(st.b ?? 0).toFixed(2)} mm`], ['h', `${((st.b - st.a) || 0).toFixed(2)} mm`], ['Your R', `${(st.R || 0).toFixed(1)} cm`], ['Watch glass', `${R_CM} cm`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: `The watch glass has a radius of curvature of about ${(st.R || 0).toFixed(0)} cm. Because h is only a millimetre or so, an error of one disc division (0.01 mm) in judging "just touching" changes R by about ${(100 * 0.001 / Math.max(0.01, st.h || 0.1)).toFixed(1)} %: that is why the tip must meet its reflection and the instrument must not rock.`,
      };
    },
    dispose() { hud.dispose(); },
  };
}
