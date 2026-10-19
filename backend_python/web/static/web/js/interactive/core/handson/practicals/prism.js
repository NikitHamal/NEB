// Angle of minimum deviation by the pin method. A 60° glass prism stands on drawing paper. The
// student drags pin P1 round the incidence point to choose the angle of incidence i (P2 follows on
// the same line), then looks through the second face from low down: the images of P1 and P2 sit
// on the backward extension of the true emergent ray (Snell's law at both faces), and the student
// swings their own pins P3, P4 until they hide the images. The deviation is measured from the
// student's pins, so a sloppy sighting shows up in the D–i curve, whose minimum gives n.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { M as KIT } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, screenDist } from '../hud.js';
import { createGraph } from '../stopwatch.js';

const BY = 0.8; const A = 60; const S = 0.55; const Y0 = 0.07; const D2R = Math.PI / 180;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const v2 = (x, z) => new THREE.Vector2(x, z);

function refract(d, n, eta) {
  const c = -n.dot(d); const k = 1 - eta * eta * (1 - c * c); if (k < 0) return null;
  return d.clone().multiplyScalar(eta).add(n.clone().multiplyScalar(eta * c - Math.sqrt(k))).normalize();
}
function hitSeg(p, d, a, b) {
  const e = b.clone().sub(a); const den = d.x * e.y - d.y * e.x; if (Math.abs(den) < 1e-9) return null;
  const w = a.clone().sub(p); const t = (w.x * e.y - w.y * e.x) / den; const u = (w.x * d.y - w.y * d.x) / den;
  return t > 1e-6 && u >= 0 && u <= 1 ? p.clone().addScaledVector(d, t) : null;
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'Deviation against incidence', xLabel: 'i (degrees)', yLabel: 'D (degrees)' });
  graph.el.classList.add('ho-side');
  const N = Math.round((1.49 + Math.random() * 0.06) * 1000) / 1000;

  world.add(mesh(new THREE.BoxGeometry(4.2, 0.05, 3.0), KIT.wood('oak'), [0, 0.025, 0]));
  const paper = mesh(new THREE.PlaneGeometry(3.6, 2.6), MAT.paper(), [0, 0.051, 0]); paper.rotation.x = -Math.PI / 2; world.add(paper);
  const h = S * Math.sqrt(3) / 2;
  const V = [v2(0, -2 * h / 3), v2(-S / 2, h / 3), v2(S / 2, h / 3)].map((p) => p.add(v2(0, -0.2)));
  const shape = new THREE.Shape(); shape.moveTo(V[0].x, -V[0].y); shape.lineTo(V[1].x, -V[1].y); shape.lineTo(V[2].x, -V[2].y); shape.closePath();
  const pg = new THREE.ExtrudeGeometry(shape, { depth: 0.32, bevelEnabled: false }); pg.rotateX(-Math.PI / 2);
  const prism = mesh(pg, new THREE.MeshPhysicalMaterial({ color: 0xdff7f2, roughness: 0.03, transparent: true, opacity: 0.35, clearcoat: 1, envMapIntensity: 2, depthWrite: false, side: THREE.DoubleSide }), [0, 0.051, 0], { cast: false });
  prism.renderOrder = 6; world.add(prism);
  const outline = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(V.map((p) => new THREE.Vector3(p.x, 0.053, p.y))), new THREE.LineBasicMaterial({ color: 0x111827 })); world.add(outline);
  const Q1 = V[1].clone().lerp(V[0], 0.5); const f1 = V[0].clone().sub(V[1]).normalize(); const n1in = v2(f1.y, -f1.x); if (n1in.dot(v2(0, -0.2).sub(Q1)) < 0) n1in.negate();
  const f2a = V[0]; const f2b = V[2]; const f2 = f2b.clone().sub(f2a).normalize(); const n2out = v2(f2.y, -f2.x); if (n2out.dot(v2(0, -0.2).sub(f2a)) > 0) n2out.negate();

  function pin(color) { const g = new THREE.Group(); g.add(mesh(new THREE.CylinderGeometry(0.005, 0.003, 0.36, 8), MAT.steel(), [0, 0.18, 0])); g.add(mesh(new THREE.SphereGeometry(0.022, 12, 8), MAT.gloss(color), [0, 0.37, 0])); return g; }
  const P = { p1: pin(0xdc2626), p2: pin(0xdc2626), p3: pin(0x2563eb), p4: pin(0x2563eb), i1: pin(0xdc2626), i2: pin(0xdc2626) };
  Object.values(P).forEach((p) => { p.position.y = 0.051; world.add(p); });
  [P.i1, P.i2].forEach((p) => { p.visible = false; p.traverse((o) => { if (o.material) { o.material = o.material.clone(); o.material.transparent = true; o.material.opacity = 0.75; } }); });
  const rayMat = new THREE.LineBasicMaterial({ color: 0x334155 }); const marks = new THREE.Group(); world.add(marks);

  const st = { i: 40, trials: [], phi: 0, eye: false, path: null, dMeas: null };
  function trace(iDeg) {
    const ang = iDeg * D2R; const d = n1in.clone().multiplyScalar(Math.cos(ang)).add(f1.clone().multiplyScalar(Math.sin(ang))).normalize();
    const r = refract(d, n1in.clone().negate(), 1 / N); if (!r) return null;
    const q2 = hitSeg(Q1, r, f2a, f2b); if (!q2) return null;
    const em = refract(r, n2out.clone().negate(), N);
    if (!em) return { d, r, q2, tir: true };
    return { d, r, q2, e: em, D: Math.acos(Math.max(-1, Math.min(1, d.dot(em)))) / D2R };
  }
  function layoutIncident() {
    const t = trace(st.i); st.path = t; const d = t ? t.d : n1in;
    const p2 = Q1.clone().addScaledVector(d, -0.55); const p1 = Q1.clone().addScaledVector(d, -1.25);
    P.p2.position.set(p2.x, 0.051, p2.y); P.p1.position.set(p1.x, 0.051, p1.y);
  }
  function layoutEmergent() {
    const t = st.path; if (!t || !t.e) return;
    const dir = v2(Math.cos(st.phi), Math.sin(st.phi));
    const p4 = t.q2.clone().addScaledVector(dir, 0.55); const p3 = t.q2.clone().addScaledVector(dir, 1.2);
    P.p4.position.set(p4.x, 0.051, p4.y); P.p3.position.set(p3.x, 0.051, p3.y);
    const back = t.q2.distanceTo(Q1) * N; const i2 = t.q2.clone().addScaledVector(t.e, -(back + 0.55)); const i1 = t.q2.clone().addScaledVector(t.e, -(back + 1.25));
    P.i2.position.set(i2.x, 0.051, i2.y); P.i1.position.set(i1.x, 0.051, i1.y);
  }
  function eyeShot() {
    const t = st.path; const dir = v2(Math.cos(st.phi), Math.sin(st.phi)); const eye = t.q2.clone().addScaledVector(dir, 2.3); const tg = t.q2.clone().addScaledVector(dir, -0.6);
    return shot({ pos: [eye.x, Y0 + 0.24, eye.y], target: [tg.x, Y0 + 0.2, tg.y], fov: 30, limits: { yaw: 0.05, pitch: 0.05, zMin: 0.95, zMax: 1.05 } });
  }
  function setEye(on) {
    st.eye = on; P.p1.visible = P.p2.visible = !on; P.i1.visible = P.i2.visible = on;
    if (on) ctx.rig.go(eyeShot(), 1.0); else ctx.rig.go(SHOT_TOP, 1.0);
  }

  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -(BY + 0.051)); const hit = new THREE.Vector3();
  const trialHandler = {
    mode: null, x0: 0, phi0: 0,
    down(p) {
      if (st.eye) { this.mode = 'swing'; this.x0 = p.x; this.phi0 = st.phi; return true; }
      if (screenDist(ctx, P.p1, p, 0.3) < 70 || screenDist(ctx, P.p2, p, 0.3) < 50) { this.mode = 'inc'; sfx.play('pick'); return true; }
      return false;
    },
    move(p) {
      if (this.mode === 'inc') {
        if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return; world.worldToLocal(hit);
        const d = Q1.clone().sub(v2(hit.x, hit.z)).normalize(); let i = Math.acos(Math.max(-1, Math.min(1, d.dot(n1in)))) / D2R; if (d.dot(f1) < 0) i = -i;
        st.i = Math.round(Math.max(20, Math.min(75, i))); layoutIncident(); hud.relabel('look', st.path && st.path.e ? `i = ${st.i}° · Look through` : `i = ${st.i}° · no ray emerges`);
      }
      if (this.mode === 'swing') { st.phi = this.phi0 - (p.x - this.x0) * 0.0009; layoutEmergent(); ctx.rig.go(eyeShot(), 0); }
    },
    up() { this.mode = null; }, cancel() { this.mode = null; },
  };
  function lookThrough() {
    if (!st.path || !st.path.e) { ctx.mistake(`At i = ${st.i}° the ray is totally internally reflected at the second face: nothing emerges. Use a larger angle of incidence.`, 2); return; }
    const t = st.path; st.phi = Math.atan2(t.e.y, t.e.x) + (Math.random() < 0.5 ? -1 : 1) * (3 + Math.random() * 4) * D2R; layoutEmergent(); setEye(true);
    hud.actions([{ id: 'mark', label: 'Pins in line: mark', primary: true, onClick: mark }, { id: 'back', label: 'Back', onClick: () => { setEye(false); trialBar(); } }]);
    ctx.say('Drag sideways to move your eye and pins P3, P4 until they hide the images of P1 and P2.', 'info', 3200);
  }
  function mark() {
    const t = st.path; const dir = v2(Math.cos(st.phi), Math.sin(st.phi)); const err = Math.acos(Math.max(-1, Math.min(1, dir.dot(t.e)))) / D2R;
    if (err > 0.6) { ctx.mistake(`Not in line yet: your pins are ${err.toFixed(1)}° off the images. Keep the two images and the two pins exactly behind one another.`, 2); return; }
    const D = Math.acos(Math.max(-1, Math.min(1, t.d.dot(dir)))) / D2R; const Dr = Math.round(D * 2) / 2;
    if (st.trials.some((q) => q.i === st.i)) { ctx.say('You already have that angle. Choose another.', 'hint', 1800); setEye(false); trialBar(); return; }
    st.trials.push({ i: st.i, D: Dr }); ui.observe(`i = ${st.i}°`, `D = <b>${Dr.toFixed(1)}°</b>`); sfx.play('ok');
    const a = new THREE.Vector3(P.p1.position.x, 0.054, P.p1.position.z); const b = new THREE.Vector3(Q1.x, 0.054, Q1.y); const c = new THREE.Vector3(t.q2.x, 0.054, t.q2.y); const e = new THREE.Vector3(P.p3.position.x, 0.054, P.p3.position.z);
    marks.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([a, b, c, e]), rayMat));
    setEye(false); trialBar();
    ctx.say(`D = ${Dr.toFixed(1)}° for i = ${st.i}°. ${st.trials.length < 6 ? 'Now another angle of incidence.' : 'Enough points: plot the graph.'}`, 'good', 2600);
  }
  function trialBar() { hud.actions([{ id: 'look', label: `i = ${st.i}° · Look through`, primary: true, onClick: lookThrough }, { id: 'done', label: `Plot (${st.trials.length})`, disabled: st.trials.length < 6, onClick: () => { hud.actions([]); ctx.next(); } }]); }

  const SHOT_TOP = shot({ pos: [0, 3.6, 1.9], target: [0, 0, -0.15], fit: 3.4, fitH: 2.6 });

  const steps = [
    {
      title: 'Pins and sightings', text: 'Drag pin <b>P1</b> round to set the angle of incidence i. Then <b>Look through</b> the other face: drag sideways until your pins <b>P3, P4</b> and the images of P1, P2 are all in one line, and mark them. Do <b>six or more</b> angles between about 30° and 65°.', hint: 'Spread the angles out, and take extra ones near the smallest deviation.', shot: SHOT_TOP, hideBelt: true,
      enter() { layoutIncident(); trialBar(); },
      exit() { hud.actions([]); setEye(false); },
      skip() { [30, 36, 42, 48, 54, 60, 66].forEach((i) => { const t = trace(i); if (t && t.e) st.trials.push({ i, D: Math.round(t.D * 2) / 2 }); }); },
      handler: trialHandler,
    },
    {
      title: 'Minimum deviation and n', text: 'The curve dips to a minimum D<sub>m</sub>, where the ray passes symmetrically through the prism.', shot: SHOT_TOP, hideBelt: true,
      enter() {
        const pts = st.trials.map((q) => [q.i, q.D]).sort((a, b) => a[0] - b[0]);
        const lowest = pts.reduce((m, q) => (q[1] < m[1] ? q : m), pts[0]);
        graph.draw(pts, null, { xMax: 80, yMin: Math.floor(lowest[1] - 3), yMax: Math.ceil(Math.max(...pts.map((q) => q[1])) + 2) }); graph.show(true);
        const Dm = lowest[1]; st.Dm = Dm; const nn = Math.sin((A + Dm) / 2 * D2R) / Math.sin(A / 2 * D2R); st.n = nn;
        ui.observe('D_m', `<b>${Dm.toFixed(1)}°</b> at i ≈ ${lowest[0]}°`);
        const opts = [[nn, 'sin((A+Dm)/2) / sin(A/2)'], [Math.sin((A + Dm) * D2R) / Math.sin(A * D2R), 'sin(A+Dm) / sin A'], [(A + Dm) / A, '(A+Dm) / A'], [Math.sin(Dm / 2 * D2R) / Math.sin(A / 2 * D2R), 'sin(Dm/2) / sin(A/2)']].map(([v, w]) => ({ label: `${v.toFixed(3)}  (${w})`, value: w })).sort(() => Math.random() - 0.5);
        anim.wait(1.0, () => ui.choose(ctx.stage.clientWidth / 2, 40, `A = 60°, Dm = ${Dm.toFixed(1)}°. Refractive index n =`, opts, (v) => {
          if (v !== 'sin((A+Dm)/2) / sin(A/2)') ctx.mistake('At minimum deviation r = A/2 and i = (A + Dm)/2, so n = sin((A+Dm)/2) / sin(A/2).', 3);
          ui.observe('n', `<b>${nn.toFixed(3)}</b>`); ctx.next(`n = ${nn.toFixed(3)}.`, 1.4);
        }));
      },
      exit() { ui.clearChooser(); graph.show(false); },
    },
  ];

  ctx.debug = { st, N, trace, layoutEmergent, trialHandler, P };
  layoutIncident();
  return {
    tools: [], steps,
    update() { hud.update(); },
    result() {
      const tDm = (() => { let m = 1e9; for (let i = 20; i <= 80; i += 0.1) { const t = trace(i); if (t && t.e) m = Math.min(m, t.D); } return m; })();
      const err = ((st.n || 0) - N) / N * 100;
      return {
        title: 'Prism: minimum deviation',
        rows: [['Readings', String(st.trials.length)], ['Your Dm', `${(st.Dm || 0).toFixed(1)}°`], ['True Dm', `${tDm.toFixed(1)}°`], ['Your n', (st.n || 0).toFixed(3)], ['Glass', N.toFixed(3)], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: 'D falls, flattens and rises again as i increases: at the bottom of the curve the ray crosses the prism parallel to its base (i = e). Because the curve is flat there, Dm is found well even though each sighting is only good to half a degree.',
      };
    },
    dispose() { hud.dispose(); graph.dispose(); },
  };
}
