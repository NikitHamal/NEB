// Sonometer, law of length: a wire stretched over two bridges on a hollow box, tensioned by a
// hanger over a pulley. The student strikes a tuning fork, rests its stem on the box and slides
// a bridge until the paper rider on the wire jumps off: resonance, where the wire's fundamental
// f = (1/2l)√(T/μ) matches the fork. Three forks give three lengths, and f·l comes out constant.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';

const BY = 0.8; const G = 9.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

function scaleTex() {
  return canvasTexture('ho-sono-scale', 8192, 120, (g, w, h) => {
    g.fillStyle = '#f2e3b8'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827';
    for (let mm = 0; mm <= 1000; mm += 2) { const x = 20 + (w - 40) * mm / 1000; const cm = mm % 10 === 0; const ten = mm % 100 === 0; g.fillRect(Math.round(x), 0, cm ? 3 : 1.4, ten ? 56 : cm ? 34 : 16); if (cm && (mm / 10) % 5 === 0) { g.font = '700 34px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(String(mm / 10), x, 96); } }
  }, { anisotropy: 16 });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const mu = Math.round((4 + Math.random() * 4)) / 10000;
  const M = 4.0; const T = M * G;
  const forks = [256, 320, 384, 480, 512].sort(() => Math.random() - 0.5).slice(0, 3).sort((a, b) => a - b);
  const lRes = (f) => 100 / (2 * f) * Math.sqrt(T / mu);
  const st = { fork: 0, l: 70, struck: 0, rider: 1, results: [], audio: null };
  const X0 = -5; const xOf = (cm) => X0 + cm / 10;

  const box = mesh(new THREE.BoxGeometry(11.2, 0.6, 1.0), new THREE.MeshStandardMaterial({ color: 0xb98a57, roughness: 0.55 }), [0, 0.3, 0]); world.add(box);
  [-2, 2].forEach((x) => { const hole = mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.01, 24), MAT.matte(0x2a1a0e), [x, 0.31, 0.505]); hole.rotation.x = Math.PI / 2; world.add(hole); });
  const scale = new THREE.Mesh(new THREE.PlaneGeometry(10.08, 0.18), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.6 })); scale.rotation.x = -Math.PI / 2; scale.position.set(0, 0.602, 0.32); world.add(scale);
  const bridgeA = mesh(new THREE.BoxGeometry(0.08, 0.22, 0.5), MAT.matte(0x2b2b2b), [xOf(0), 0.71, 0]); world.add(bridgeA);
  const bridgeB = mesh(new THREE.BoxGeometry(0.08, 0.22, 0.5), MAT.matte(0x2b2b2b), [xOf(70), 0.71, 0]); world.add(bridgeB);
  const pulley = mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.08, 24), MAT.brushed(), [5.75, 0.62, 0]); pulley.rotation.x = Math.PI / 2; world.add(pulley);
  const hanger = new THREE.Group(); hanger.position.set(5.97, -0.6, 0); world.add(hanger);
  hanger.add(mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.1, 8), MAT.brushed(), [0, 0.6, 0]));
  for (let i = 0; i < 4; i++) hanger.add(mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.09, 24), MAT.gloss(0x5b6470), [0, i * 0.1, 0]));
  const wireMat = new THREE.MeshStandardMaterial({ color: 0xc0c6cc, metalness: 1, roughness: 0.3 });
  const N = 60; const wirePts = new Float32Array((N + 1) * 3);
  const wireGeo = new THREE.BufferGeometry(); wireGeo.setAttribute('position', new THREE.BufferAttribute(wirePts, 3));
  const wire = new THREE.Line(wireGeo, new THREE.LineBasicMaterial({ color: 0x9aa3ad })); world.add(wire);
  const tail = mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 6), wireMat); world.add(tail);
  const rider = mesh(new THREE.ConeGeometry(0.06, 0.09, 3), MAT.matte(0xef4444), null, { cast: false }); rider.rotation.x = Math.PI; world.add(rider);
  const fork = new THREE.Group(); fork.position.set(-3.6, 0.6, 0.75); world.add(fork);
  const steel = MAT.steel();
  fork.add(mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.5, 10), steel, [0, 0.25, 0]));
  const prongs = [-1, 1].map((s) => { const p = mesh(new THREE.BoxGeometry(0.05, 0.8, 0.06), steel, [s * 0.1, 0.95, 0]); fork.add(p); return p; });
  fork.add(mesh(new THREE.TorusGeometry(0.1, 0.03, 8, 20, Math.PI), steel, [0, 0.55, 0]).rotateZ(Math.PI));
  const tag = mesh(new THREE.PlaneGeometry(0.34, 0.12), new THREE.MeshBasicMaterial({ map: null, transparent: true }), [0, 0.72, 0.04]); fork.add(tag);
  function setForkTag() {
    tag.material.map = canvasTexture(`ho-sfork-${forks[st.fork]}`, 128, 48, (c, w, h) => { c.fillStyle = '#e5e7eb'; c.fillRect(0, 0, w, h); c.fillStyle = '#111827'; c.font = '800 28px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText(`${forks[st.fork]} Hz`, w / 2, 34); });
    tag.material.needsUpdate = true;
  }
  const pad = mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.1, 24), MAT.matte(0x1f2937), [-4.4, 0.65, 0.75]); world.add(pad);

  const response = () => { const lr = lRes(forks[st.fork]); return 1 / (1 + ((st.l - lr) / 0.35) ** 2); };
  function strike() {
    st.struck = 1; sfx.play('click');
    if (!sfx.muted) {
      if (!st.audio) { const AC = window.AudioContext || window.webkitAudioContext; if (AC) { const c = new AC(); const o = c.createOscillator(); const g = c.createGain(); o.connect(g); g.connect(c.destination); g.gain.value = 0; o.start(); st.audio = { c, o, g }; } }
      if (st.audio) { if (st.audio.c.state === 'suspended') st.audio.c.resume(); st.audio.o.frequency.value = forks[st.fork]; }
    }
  }
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -(BY + 0.7)); const hit = new THREE.Vector3();
  const handler = {
    down(p) {
      if (hits(ctx, pad, p, 60) || hits(ctx, fork, p, 60, 0.6)) { strike(); return true; }
      if (hits(ctx, bridgeB, p, 70, 0.1)) { this.d = true; return true; }
      return false;
    },
    move() { if (!this.d || !ctx.input.ptr.ray.intersectPlane(plane, hit)) return; st.l = clamp(Math.round((hit.x - X0) * 100) / 10, 10, 98); bridgeB.position.x = xOf(st.l); st.rider = Math.min(st.rider, 1); sfx.play('knob'); },
    up() { this.d = null; },
  };

  const SHOT = shot({ pos: [0.4, 3.0, 7.6], target: [0.3, 0.6, 0.2], fit: 12 });
  function forkStep(i) {
    return {
      title: `Resonate with the ${forks[i]} Hz fork`, text: `Strike the fork on the <b>rubber pad</b> (tap it); its stem rests on the box. Slide the <b>movable bridge</b> (drag it) until the <b>paper rider jumps</b> off the wire, then record the length between the bridges.`, hint: 'Start with a long length and come in slowly; the rider only flies when the wire\'s own frequency equals the fork\'s.', hideBelt: true, shot: SHOT,
      enter() {
        st.fork = i; setForkTag(); st.rider = 1;
        hud.actions([
          { id: 'snd', label: sfx.muted ? 'Sound on' : 'Sound off', onClick: () => { sfx.setMuted(!sfx.muted); hud.relabel('snd', sfx.muted ? 'Sound on' : 'Sound off'); } },
          { id: 'rec', label: 'Record length', primary: true, onClick: () => {
            if (st.rider > 0.5) { ctx.mistake('The rider has not jumped: the wire is not resonating yet. Strike the fork and move the bridge slowly.', 2); return; }
            st.results.push({ f: forks[i], l: st.l }); ui.observe(`${forks[i]} Hz`, `l = <b>${st.l.toFixed(1)} cm</b> · f·l = ${(forks[i] * st.l / 100).toFixed(1)} m/s`);
            hud.actions([]); ctx.next(`l = ${st.l.toFixed(1)} cm.`);
          } },
        ]);
      },
      exit() { hud.actions([]); },
      skip() { st.l = Math.round(lRes(forks[i]) * 10) / 10; st.results.push({ f: forks[i], l: st.l }); },
      handler,
    };
  }
  const steps = forks.map((f, i) => forkStep(i));
  steps.push({
    title: 'Law of length', text: 'At constant tension, compare f·l for the three forks.', hideBelt: true, shot: SHOT,
    enter() {
      const fl = st.results.map((r) => r.f * r.l / 100); const mean = fl.reduce((a, b) => a + b, 0) / fl.length; const spread = (Math.max(...fl) - Math.min(...fl)) / mean * 100;
      st.mean = mean;
      anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 50, `f·l = ${fl.map((x) => x.toFixed(1)).join(', ')} m/s (spread ${spread.toFixed(1)} %). So…`, [{ label: 'f ∝ 1/l: halve the length, double the frequency', value: 1 }, { label: 'f ∝ l', value: 0 }, { label: 'f ∝ 1/l²', value: 2 }], (v) => {
        if (v !== 1) ctx.mistake('f·l stays constant, so f is inversely proportional to l: f = (1/2l)√(T/μ).', 3);
        const muCalc = T / (2 * mean) ** 2; st.mu = muCalc;
        ui.observe('μ from f·l', `${(muCalc * 1000).toFixed(2)} g/m`); ctx.next(`2fl = √(T/μ) = ${(2 * mean).toFixed(1)} m/s, the speed of waves on the wire; μ = T/(2fl)² = ${(muCalc * 1000).toFixed(2)} g/m.`, 1.2);
      }));
    },
    exit() { ui.clearChooser(); },
  });

  function layoutWire(t) {
    const a = xOf(0); const b = xOf(st.l); const y = 0.82; const amp = st.struck * response() * 0.05;
    for (let i = 0; i <= N; i++) { const s = i / N; const x = a + (b - a) * s; wirePts[i * 3] = x; wirePts[i * 3 + 1] = y + Math.sin(Math.PI * s) * amp * Math.sin(t * 60); wirePts[i * 3 + 2] = 0; }
    wireGeo.attributes.position.needsUpdate = true;
    const tx0 = b; const tx1 = 5.75; tail.scale.y = tx1 - tx0; tail.position.set((tx0 + tx1) / 2, y, 0); tail.rotation.z = Math.PI / 2;
  }
  ctx.debug = { st, forks, lRes, strike };
  return {
    tools: [], steps,
    update(dt, t) {
      st.struck *= Math.exp(-dt / 6);
      const r = response();
      if (st.struck * r > 0.6 && st.rider > 0.5) { st.rider = 0.49; sfx.play('pick'); }
      if (st.rider < 0.5 && st.rider > 0) st.rider = Math.max(0, st.rider - dt * 0.6);
      layoutWire(t);
      const mid = (xOf(0) + xOf(st.l)) / 2;
      const flyK = st.rider < 0.5 ? (0.5 - st.rider) * 2 : 0;
      rider.position.set(mid + flyK * 0.4, 0.86 + Math.sin(flyK * Math.PI) * 0.5 - flyK * 0.25, flyK * 0.5); rider.rotation.z = flyK * 5;
      prongs[0].position.x = -0.1 - st.struck * 0.01 * Math.sin(t * 90); prongs[1].position.x = 0.1 + st.struck * 0.01 * Math.sin(t * 90);
      if (st.audio) st.audio.g.gain.setTargetAtTime(sfx.muted ? 0 : st.struck * (0.04 + 0.2 * r), st.audio.c.currentTime, 0.03);
      hud.update();
    },
    result() {
      return { title: 'Sonometer: law of length', rows: st.results.map((r) => [`${r.f} Hz`, `${r.l.toFixed(1)} cm`]).concat([['f·l (mean)', `${(st.mean || 0).toFixed(1)} m/s`], ['μ (yours)', `${((st.mu || 0) * 1000).toFixed(2)} g/m`], ['μ (wire)', `${(mu * 1000).toFixed(2)} g/m`]]),
        conclusion: 'At constant tension the resonant length is inversely proportional to the frequency: the wire vibrates in its fundamental with a node at each bridge, so l = λ/2 and f = v/2l with v = √(T/μ).' };
    },
    dispose() { hud.dispose(); wireGeo.dispose(); if (st.audio) { try { st.audio.c.close(); } catch (e) { /* closed */ } } },
  };
}
