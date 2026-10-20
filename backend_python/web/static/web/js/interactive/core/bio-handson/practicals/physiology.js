// Two water-relations practicals with a clock you can run forward.
// Potato osmometer: cut a flat base on a peeled potato, scoop out a cup, half fill it with
// coloured sucrose solution, mark the level with a pin, stand it in water beside a boiled control,
// and watch the level climb over an hour by endosmosis through the living cells (not in the
// boiled one). Imbibition: weigh dry raisins, soak them, blot and weigh again, and work out the
// percentage of water imbibed.
import { THREE } from '../../engine.js';
import { reagentBottle } from '../props.js';
import { organic, ease, clamp, mesh, MAT, canvasTexture, rng, wet } from '../kit.js';

export function create(ctx) { return ctx.config.slug.startsWith('potato') ? osmometer(ctx) : imbibition(ctx); }

function dish(r = 0.5, color = 0xcfe8f5) {
  const g = new THREE.Group();
  const pts = [[0.001, 0], [r, 0], [r + 0.02, 0.02], [r + 0.02, 0.16], [r + 0.04, 0.17]].map(([a, b]) => new THREE.Vector2(a, b));
  g.add(mesh(new THREE.LatheGeometry(pts, 40), MAT.glass(), null, { cast: false }));
  const w = mesh(new THREE.CylinderGeometry(r - 0.005, r - 0.005, 0.1, 40), MAT.liquid(color, 0.35), [0, 0.06, 0], { cast: false }); g.add(w); g.userData.water = w;
  return g;
}
function clockUI(ctx, onTick) {
  const b = document.createElement('div'); b.className = 'bh-clock';
  b.innerHTML = '<span class="bh-clock-face"><i></i></span><b>0 min</b><button type="button">+15 min ▶</button>';
  ctx.ui.root.appendChild(b);
  const hand = b.querySelector('i'); const txt = b.querySelector('b'); const btn = b.querySelector('button');
  let t = 0;
  btn.addEventListener('click', () => { const from = t; t += 15; ctx.sfx.play('click'); btn.disabled = true; ctx.anim.add(1.2, (k) => { const m = from + (t - from) * k; hand.style.transform = `rotate(${m * 6}deg)`; txt.textContent = `${Math.round(m)} min`; onTick(m, false); }, { ease: ease.inOut, done: () => { btn.disabled = false; onTick(t, true); } }); });
  return { el: b, get t() { return t; }, remove() { b.remove(); }, show(v) { b.style.display = v ? '' : 'none'; } };
}

function osmometer(ctx) {
  const { world, input, anim, sfx, ui, fx } = ctx;
  const sucrose = 20;
  const hmax = 7.5 * sucrose / 20; // mm: the rise approaches about 7.5 mm for 20% sucrose
  const potatoMat = wet(0xeed9a0, { roughness: 0.46, clearcoat: 0.5, detailScale: 16, detailBump: 0.006, mottle: 0.32, sss: 0xf0c060 });
  function potatoCup(boiled) {
    const g = new THREE.Group();
    const pg = new THREE.SphereGeometry(0.42, 64, 44); pg.computeBoundingSphere(); organic(pg, 0.022, 1.3, boiled ? 7 : 3, 9); const body = mesh(pg, boiled ? wet(0xe2c98c, { roughness: 0.6 }) : potatoMat.clone()); body.scale.set(1, 0.85, 0.9); body.position.y = 0.36; g.add(body);
    const cavity = mesh(new THREE.CylinderGeometry(0.2, 0.17, 0.22, 28, 1, true), new THREE.MeshStandardMaterial({ color: 0xe9d49a, roughness: 0.8, side: THREE.BackSide }), [0, 0.5, 0]); cavity.visible = false; g.add(cavity);
    const sol = mesh(new THREE.CylinderGeometry(0.185, 0.185, 1, 28), MAT.liquid(0xdb2777, 0.75), [0, 0.5, 0], { cast: false }); sol.visible = false; g.add(sol);
    return { g, body, cavity, sol, boiled, level: 0 };
  }
  const tray = dish(1.4); tray.position.set(0, 0, 0.1); world.add(tray);
  const live = potatoCup(false); live.g.position.set(-0.45, 0.02, 0.1); world.add(live.g);
  const dead = potatoCup(true); dead.g.position.set(0.55, 0.02, 0.1); dead.g.visible = false; world.add(dead.g);
  live.g.position.y = 0.02; tray.userData.water.visible = false;
  const bottle = reagentBottle('20% sucrose', 0xdb2777, 'with eosin'); bottle.position.set(-1.6, 0, -0.5); world.add(bottle);
  const pins = [];
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3();
  const SHOT = { pos: [0, 2.1, 2.4], target: [0, 0.95, 0.05], fit: 2.6 };
  const CLOSE = { pos: [-0.25, 1.9, 1.3], target: [-0.4, 1.25, 0.1], fit: 1.1 };
  let clock = null; const readings = [];
  function setLevel(c, l) { c.level = l; c.sol.visible = l > 0.001; c.sol.scale.y = Math.max(0.001, l); c.sol.position.y = 0.4 + l / 2; }
  const steps = [
    {
      title: 'Cut a flat base', text: 'With the <b>scalpel</b>, slice across the bottom of the peeled potato so it stands flat.', tool: 'scalpel', shot: CLOSE,
      skip() { live.body.scale.y = 0.8; },
      handler: { down(p) { if (!input.pick([live.body])) return false; if (!ctx.requireTool('scalpel')) return true; this.y = p.y; this.x = p.x; return true; }, move(p) { if (this.x === undefined) return; if (Math.abs(p.x - this.x) > 120) { this.x = undefined; sfx.play('cut'); live.body.scale.y = 0.8; live.g.getWorldPosition(tmp); fx.burst(tmp, 0xf1dfa8, 6, 0.1, tmp.y); ctx.next('It stands steady on its flat base.'); } }, up() { this.x = undefined; } },
    },
    {
      title: 'Scoop out a cup', text: 'Hollow out a cavity in the top with the <b>scalpel</b>: drag round and round inside the top of the potato.', tool: 'scalpel', shot: CLOSE,
      skip() { live.cavity.visible = true; live.cavity.scale.set(1, 1, 1); },
      handler: { down(p) { if (!input.pick([live.body, live.cavity])) return false; if (!ctx.requireTool('scalpel')) return true; this.last = [p.x, p.y]; this.d = this.d || 0; return true; }, move(p) { if (!this.last) return; this.d += Math.hypot(p.x - this.last[0], p.y - this.last[1]); this.last = [p.x, p.y]; const k = clamp(this.d / 900); live.cavity.visible = true; live.cavity.scale.set(k, k, k); ctx.progress(k); if (Math.random() < 0.1) { live.g.getWorldPosition(tmp); tmp.y += 0.7; fx.burst(tmp, 0xf1dfa8, 2, 0.15, ctx.BENCH_Y + 0.05); } if (k >= 1 && !this.done) { this.done = true; this.last = null; sfx.play('ok'); ctx.next('A cup with walls about 5 mm thick: the living potato cells form the membrane of the osmometer.'); } }, up() { this.last = null; } },
    },
    {
      title: 'Half fill with sugar solution', text: 'Fill the dropper from the <b>20% sucrose</b> (coloured with eosin) and fill the cup about half way.', tool: 'dropper', shot: CLOSE,
      skip() { setLevel(live, 0.12); setLevel(dead, 0.12); dead.cavity.visible = true; },
      handler: { down() { if (input.pick([bottle])) { this.loaded = true; sfx.play('pick'); return true; } if (!input.pick([live.body, live.cavity, live.sol])) return false; if (!ctx.requireTool('dropper')) return true; if (!this.loaded) { ctx.say('Fill the dropper from the sucrose bottle.', 'hint', 1800); return true; } sfx.play('drop'); setLevel(live, Math.min(0.12, live.level + 0.03)); ctx.progress(live.level / 0.12); if (live.level >= 0.12 && !this.done) { this.done = true; setLevel(dead, 0.12); dead.cavity.visible = true; ctx.next('Half full. A second, boiled potato cup is set up the same way as a control.'); } return true; } },
    },
    {
      title: 'Mark the level', text: 'Push a <b>pin</b> into the wall of the cup exactly at the surface of the solution.', tool: 'pin', shot: CLOSE,
      enter() { tmp.set(0.19, 0.4 + live.level, 0); live.g.localToWorld(tmp); this.m = ctx.fx.mark(tmp, 0.03, 0xfacc15); stepMark = this; },
      exit() { if (this.m) ctx.fx.unmark(this.m); },
      skip() { },
      handler: { down(p) { const s = stepMark; input.project(s.m.position, tmp2, ctx.stage.clientWidth, ctx.stage.clientHeight); if (Math.hypot(tmp2.x - p.x, tmp2.y - p.y) > 40) return false; if (!ctx.requireTool('pin')) return true; sfx.play('pin'); const pin = mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.2, 6), MAT.steel(), null); pin.position.copy(s.m.position); world.worldToLocal(pin.position); pin.rotation.z = Math.PI / 2; world.add(pin); pins.push(pin); ctx.next('Initial level marked.'); return true; } },
    },
    {
      title: 'Stand both cups in water', text: 'Pour water into the dish around both cups (tap the dish), then start the clock.', tool: null, autoTool: 'hand', shot: SHOT,
      enter() { dead.g.visible = true; },
      skip() { tray.userData.water.visible = true; dead.g.visible = true; },
      handler: { down() { if (!input.pick([tray])) return false; sfx.play('pour'); tray.userData.water.visible = true; tray.userData.water.scale.y = 0.01; anim.add(1, (k) => { tray.userData.water.scale.y = k; }, { done: () => ctx.next('The living cup and the boiled control now stand in water.') }); return true; } },
    },
    {
      title: 'Watch for an hour', text: 'Run the clock in 15-minute steps and watch the solution level in each cup against its pin.', tool: null, autoTool: 'hand', hideBelt: true, shot: { pos: [0.05, 2.75, 1.45], target: [0.05, 1.2, 0.1], fit: 2.2 },
      enter() {
        clock = clockUI(ctx, (m, settled) => {
          const frac = 1 - Math.exp(-m / 40); const rise = hmax * frac;
          setLevel(live, 0.12 + frac * 0.09);
          if (settled) { readings.push([m, rise]); ui.observe(`${m} min`, `living +${rise.toFixed(1)} mm · boiled 0 mm`); ctx.progress(m / 60); if (m >= 60 && !this.done) { this.done = true; clock.show(false); ctx.next(); } }
        });
      },
      skip() { setLevel(live, 0.2); readings.push([60, hmax * 0.78]); },
      exit() { if (clock) clock.remove(); },
    },
    {
      title: 'Explain', text: 'Why did the level rise only in the living potato?', tool: null, autoTool: 'hand', hideBelt: true, shot: CLOSE,
      enter() {
        const ask = () => ui.choose(ctx.stage.clientWidth / 2, 60, 'The level rose because…', [{ label: 'Water entered by endosmosis through the living cells', value: 'ok' }, { label: 'Sugar left the cup', value: 'sugar' }, { label: 'The potato swelled and squeezed it up', value: 'sq' }], (v) => {
          if (v === 'ok') ctx.next('Endosmosis: water moved from the dish (hypotonic) through the living, selectively permeable potato cells into the sugar solution (hypertonic). Boiling killed the membranes, so the control shows no rise.');
          else { ctx.mistake('Sucrose cannot pass the cell membranes; think about which way water moves across a living membrane.', 3); anim.wait(0.4, ask); }
        });
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];
  let stepMark = null;
  return { tools: ['hand', 'scalpel', 'dropper', 'pin'], steps, result() { return { title: 'Potato osmometer', rows: readings.map(([m, r]) => [`${m} min`, `+${r.toFixed(1)} mm`]), conclusion: 'The sugar solution in the living potato cup rose because water entered by endosmosis through the living cells, which act as a selectively permeable membrane. The boiled potato (dead cells) showed no rise: osmosis needs living membranes.' }; }, dispose() { if (clock) clock.remove(); } };
}

function imbibition(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const R = rng(5); const m0 = 10 + Math.round(R() * 40) / 10; const pct = 60 + Math.round(R() * 30); const m1 = +(m0 * (1 + pct / 100)).toFixed(1);
  const bal = new THREE.Group(); bal.position.set(0.6, 0, 0); world.add(bal);
  bal.add(mesh(new THREE.BoxGeometry(0.8, 0.18, 0.9), MAT.gloss(0xe5e7eb), [0, 0.09, 0]));
  const pan = mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.02, 32), MAT.steel(), [0, 0.2, -0.05]); bal.add(pan);
  const lcdC = document.createElement('canvas'); lcdC.width = 256; lcdC.height = 96; const lg = lcdC.getContext('2d'); const lcdT = new THREE.CanvasTexture(lcdC);
  const lcd = mesh(new THREE.PlaneGeometry(0.34, 0.12), new THREE.MeshBasicMaterial({ map: lcdT }), [0, 0.15, 0.452]); bal.add(lcd);
  function show(v) { lg.fillStyle = '#0f172a'; lg.fillRect(0, 0, 256, 96); lg.fillStyle = '#4ade80'; lg.font = '700 54px monospace'; lg.textAlign = 'right'; lg.fillText(v, 220, 66); lg.font = '600 24px monospace'; lg.fillText('g', 248, 66); lcdT.needsUpdate = true; }
  show('0.0');
  const beaker = new THREE.Group(); beaker.position.set(-0.6, 0, 0); world.add(beaker);
  const pts = [[0.001, 0], [0.32, 0], [0.34, 0.02], [0.34, 0.6], [0.37, 0.63]].map(([a, b]) => new THREE.Vector2(a, b));
  beaker.add(mesh(new THREE.LatheGeometry(pts, 32), MAT.glass(), null, { cast: false }));
  const water = mesh(new THREE.CylinderGeometry(0.325, 0.325, 0.4, 32), MAT.liquid(0xcfe8f5, 0.4), [0, 0.22, 0], { cast: false }); beaker.add(water);
  const raisins = new THREE.Group(); world.add(raisins);
  const rMat = wet(0x3b1f2b, { roughness: 0.75, clearcoat: 0.3 });
  for (let i = 0; i < 14; i++) { const r = mesh(new THREE.SphereGeometry(0.035, 10, 8), rMat, [(R() - 0.5) * 0.3, 0.03, (R() - 0.5) * 0.3]); r.scale.set(1, 0.6, 1.4); r.rotation.y = R() * 6; raisins.add(r); }
  raisins.position.set(0, 0.0, 0.5);
  const SHOT = { pos: [0, 1.9, 2.2], target: [0, 0.95, 0.15], fit: 2.2 };
  let clock = null;
  const move = (to, done) => { const from = raisins.position.clone(); anim.add(0.8, (k) => { raisins.position.lerpVectors(from, to, k); raisins.position.y += Math.sin(Math.PI * k) * 0.3; }, { ease: ease.inOut, done }); };
  const steps = [
    { title: 'Weigh the dry raisins', text: 'Tap the raisins to put them on the balance pan.', tool: null, autoTool: 'hand', shot: SHOT, skip() { show(m0.toFixed(1)); },
      handler: { down() { if (!input.pick([raisins])) return false; sfx.play('pick'); move(new THREE.Vector3(0.6, 0.21, -0.05), () => { sfx.play('place'); show(m0.toFixed(1)); ui.observe('Initial mass', `${m0.toFixed(1)} g`); ctx.next(`Dry mass: ${m0.toFixed(1)} g.`); }); return true; } } },
    { title: 'Soak them in water', text: 'Tap the raisins to drop them into the beaker of water.', tool: null, autoTool: 'hand', shot: SHOT, skip() { raisins.position.set(-0.6, 0.05, 0); show('0.0'); },
      handler: { down() { if (!input.pick([raisins])) return false; show('0.0'); move(new THREE.Vector3(-0.6, 0.05, 0), () => { sfx.play('drop'); ctx.next(); }); return true; } } },
    { title: 'Leave them to soak', text: 'Run the clock forward: imbibition is slow.', tool: null, autoTool: 'hand', hideBelt: true, shot: { pos: [-0.5, 1.6, 1.3], target: [-0.6, 0.95, 0], fit: 1.0 },
      enter() { clock = clockUI(ctx, (m, settled) => { const k = clamp(m / 60); raisins.children.forEach((r) => r.scale.set(1 + k * 0.5, 0.6 + k * 0.45, 1.4 + k * 0.3)); rMat.color.setHex(0x3b1f2b).lerp(new THREE.Color(0x6b3a3f), k); if (settled && m >= 60 && !this.done) { this.done = true; clock.show(false); ctx.next('Plump and smooth: the raisins have taken up water.'); } }); },
      skip() { raisins.children.forEach((r) => r.scale.set(1.5, 1.05, 1.7)); }, exit() { if (clock) clock.remove(); } },
    { title: 'Blot and weigh again', text: 'Tap the raisins to lift them out; they are blotted dry and weighed.', tool: null, autoTool: 'hand', shot: SHOT, skip() { show(m1.toFixed(1)); },
      handler: { down() { if (!input.pick([raisins])) return false; move(new THREE.Vector3(0.6, 0.21, -0.05), () => { sfx.play('place'); show(m1.toFixed(1)); ui.observe('Final mass', `${m1.toFixed(1)} g`); ctx.next(`Soaked mass: ${m1.toFixed(1)} g.`); }); return true; } } },
    { title: 'Percentage of water imbibed', text: `% imbibition = (final − initial) ÷ initial × 100 = (${m1.toFixed(1)} − ${m0.toFixed(1)}) ÷ ${m0.toFixed(1)} × 100`, tool: null, autoTool: 'hand', hideBelt: true, shot: SHOT,
      enter() {
        const right = Math.round((m1 - m0) / m0 * 100);
        const opts = [right, Math.round((m1 - m0) / m1 * 100), Math.round(m1 / m0 * 100), right + 12].filter((v, i, a) => a.indexOf(v) === i).sort(() => Math.random() - 0.5);
        const ask = () => ui.choose(ctx.stage.clientWidth / 2, 60, 'Water imbibed', opts.map((v) => ({ label: `${v} %`, value: v })), (v) => { if (v === right) { ui.observe('Imbibition', `${right} %`); ctx.next('Imbibition: the dry hydrophilic colloids (cellulose, pectin, proteins) of the raisin skin and flesh adsorb water and swell — no living membrane is needed.'); } else { ctx.mistake('Divide the gain in mass by the initial mass, then multiply by 100.', 3); anim.wait(0.4, ask); } });
        anim.wait(0.6, ask);
      }, exit() { ui.clearChooser(); } },
  ];
  return { tools: ['hand'], steps, result() { return { title: 'Imbibition', rows: [['Initial mass', `${m0.toFixed(1)} g`], ['Final mass', `${m1.toFixed(1)} g`], ['Water imbibed', `${Math.round((m1 - m0) / m0 * 100)} %`]], conclusion: 'Dry raisins (and seeds) swell and gain mass in water by imbibition — adsorption of water by hydrophilic colloids. It develops a large imbibition pressure, the force that bursts seed coats at germination.' }; }, dispose() { if (clock) clock.remove(); lcdT.dispose(); } };
}
