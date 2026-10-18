// Tests for anions, done in test tubes with the real reagents and in the student's own order: a
// preliminary test on the solid with dilute acid (and the gas tested with lime water or lead
// acetate paper), then the silver nitrate, barium chloride and brown ring tests on the salt
// solution, then a verdict. The reactions follow wet-tests.js, so unacidified tubes give the
// classic false precipitates and conc. H2SO4 poured straight in gives no ring.
import { THREE } from '../../engine.js';
import { reagentBottle, watchGlass } from '../../bio-handson/props.js';
import { makeTube, makeRack } from '../../bio-handson/glassware.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { sfx, tone } from '../../bio-handson/sound.js';
import { ANIONS, REAGENTS, createTubeChem, gasTest } from '../wet-tests.js';
import { createHud, hits } from '../hud.js';
import { createDrops } from '../glass.js';

const BY = 0.8;
sfx.register('drip', () => { tone(1250 + Math.random() * 300, 0.07, { gain: 0.06, slide: 0.55 }); });
sfx.register('glass', () => { tone(2600, 0.25, { gain: 0.04 }); tone(3900, 0.18, { gain: 0.02, delay: 0.01 }); });
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui, fx } = ctx;
  const hud = createHud(ctx);
  const keys = Object.keys(ANIONS);
  const anion = keys[Math.floor(Math.random() * keys.length)];

  const mat = mesh(new THREE.BoxGeometry(4.4, 0.02, 2.2), MAT.matte(0x2f3640), [0, 0.01, 0]); world.add(mat); ctx.surfaces.push(mat);
  const rack = makeRack(4); rack.group.position.set(-1.2, 0.02, -0.25); world.add(rack.group);
  const tubes = [0, 1, 2, 3].map((i) => { const t = makeTube(String(i + 1)); t.group.position.copy(rack.slots[i]).add(rack.group.position); world.add(t.group); return t; });
  const salt = watchGlass(null); salt.position.set(-1.75, 0.02, 0.6); world.add(salt);
  const heap = mesh(new THREE.SphereGeometry(0.11, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2), MAT.matte(0xf5f5ef), [0, 0.02, 0]); heap.scale.set(1, 0.4, 1); salt.add(heap);
  const order = ['soln', 'hcl', 'hno3', 'agno3', 'nh4oh', 'bacl2', 'feso4', 'h2so4'];
  const bottles = {};
  order.forEach((k, i) => {
    const r = REAGENTS[k]; const b = reagentBottle(r.short, r.color, k === 'soln' ? 'unknown' : '', { amber: r.amber });
    b.scale.setScalar(0.72); b.position.set(-0.05 + (i % 4) * 0.42, 0, -0.75 + Math.floor(i / 4) * 0.42); b.userData.home = b.position.clone(); world.add(b); bottles[k] = b;
  });
  const lime = makeTube('lime'); lime.material.color.set(0xf4fbff); lime.setFill(0.3); lime.group.position.set(1.95, 0.02, 0.55); lime.group.scale.setScalar(0.8); world.add(lime.group);
  const paper = mesh(new THREE.BoxGeometry(0.06, 0.32, 0.004), MAT.matte(0xfaf7ee), [1.6, 0.18, 0.62]); paper.rotation.z = 0.1; world.add(paper);
  const HOLD = new THREE.Vector3(1.05, 0.1, 0.35);
  const stand = new THREE.Group(); stand.position.set(HOLD.x, 0, HOLD.z - 0.16); world.add(stand);
  stand.add(mesh(new THREE.BoxGeometry(0.5, 0.04, 0.4), MAT.matte(0x24323a), [0, 0.02, 0.1]));
  stand.add(mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.5, 12), MAT.steel(), [0, 0.75, 0]));
  stand.add(mesh(new THREE.BoxGeometry(0.06, 0.06, 0.2), MAT.matte(0x30363d), [0, 1.0, 0.08]));
  stand.add(mesh(new THREE.TorusGeometry(0.085, 0.012, 6, 20), MAT.steel(), [0, 1.0, 0.16]).rotateX(Math.PI / 2));
  const drops = createDrops(world, 6);
  const ringMat = new THREE.MeshBasicMaterial({ color: 0x5b3214, transparent: true, opacity: 0 });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.066, 0.012, 6, 24), ringMat); ring.rotation.x = Math.PI / 2; ring.visible = false;
  const layer = mesh(new THREE.CylinderGeometry(0.066, 0.066, 0.12, 20), MAT.liquid(0xf3eee0, 0.75), null, { cast: false }); layer.visible = false;

  const st = { tube: null, view: null, chem: null, busy: false, fizz: 0, cloudy: 0, results: {} };
  function bring(i) {
    const t = tubes[i]; st.tube = t; st.chem = createTubeChem(anion);
    const from = t.group.position.clone();
    anim.add(0.8, (k) => { t.group.position.lerpVectors(from, HOLD, k); t.group.position.y += Math.sin(k * Math.PI) * 0.4; }, { done: () => sfx.play('glass') });
    t.group.add(ring); t.group.add(layer); ring.visible = layer.visible = false; ringMat.opacity = 0;
  }
  function putBack() {
    const t = st.tube; if (!t) return; const i = tubes.indexOf(t); const to = rack.slots[i].clone().add(rack.group.position);
    const from = t.group.position.clone(); anim.add(0.7, (k) => { t.group.position.lerpVectors(from, to, k); t.group.position.y += Math.sin(k * Math.PI) * 0.35; });
    st.tube = null;
  }
  const tmp = new THREE.Vector3();
  function pour(k, how, done) {
    if (st.busy || !st.tube) return; st.busy = true;
    const b = k === 'solid' ? salt : bottles[k]; const home = b.position.clone();
    const over = HOLD.clone().add(new THREE.Vector3(-0.32, 1.45, 0));
    anim.add(0.55, (e) => { b.position.lerpVectors(home, over, e); b.rotation.z = -1.9 * e; }, { done: () => {
      st.tube.top(tmp); world.worldToLocal(tmp);
      const n = k === 'solid' ? 1 : 3; let c = 0;
      const one = () => {
        b.localToWorld(tmp.set(0.06, 0.55, 0)); world.worldToLocal(tmp);
        drops.spawn(tmp, HOLD.y + 0.12 + st.tube.fill * 1.1, () => { sfx.play('drip'); }, k === 'solid' ? 0xffffff : REAGENTS[k].color);
        if (++c < n) anim.wait(0.16, one);
      };
      one();
      anim.wait(0.7, () => {
        anim.add(0.5, (e) => { b.position.lerpVectors(over, home, e); b.rotation.z = -1.9 * (1 - e); }, { done: () => { st.busy = false; } });
        react(k, how); done && done();
      });
    } });
  }
  function react(k, how) {
    const s = st.chem.state; const before = { ppt: s.ppt, gas: s.gas };
    const text = st.chem.apply(k, how);
    const t = st.tube;
    if (k === 'soln' || k === 'solid') t.to(anim, { fill: Math.max(t.fill, k === 'solid' ? 0.06 : 0.18), color: s.color, dur: 0.6, opacity: 0.55 });
    else t.to(anim, { fill: Math.min(0.55, t.fill + 0.05), color: s.color, dur: 1.4, opacity: 0.45 + s.cloudy * 0.5 });
    if (s.ppt && s.ppt !== before.ppt) t.precipitate(anim, s.color, s.pptAmount);
    if (!s.ppt && before.ppt) t.precipitate(anim, s.color, 0.01);
    if (s.gas && (k === 'hcl' || k === 'hno3')) st.fizz = 2.6;
    if (s.layered) { layer.visible = true; layer.position.y = 0.075 + 0.06; }
    if (s.ring) { ring.visible = true; ring.position.y = 0.075 + 0.13; anim.add(2.5, (e) => { ringMat.opacity = 0.9 * e; }, { delay: 0.6 }); }
    ui.say(text, 'info', 4200);
    ctx.step && ctx.step.onReact && ctx.step.onReact(k, text);
  }

  const SHOT = shot({ pos: [0.25, 2.2, 3.4], target: [0.15, 0.7, 0.05], fit: 4.0, fitH: 2.2 });
  const SHOT_TUBE = shot({ pos: [0.75, 1.75, 2.9], target: [0.55, 0.6, -0.1], fit: 2.4, fitH: 1.9 });

  function reagentHandler(allowed, sideAcid = false) {
    return {
      down(p) {
        if (!st.tube || st.busy) return false;
        if (allowed.includes('solid') && hits(ctx, salt, p, 50)) { pour('solid'); return true; }
        for (const k of allowed) {
          if (k === 'solid' || !bottles[k]) continue;
          if (hits(ctx, bottles[k], p, 40, 0.3)) {
            if (k === 'h2so4' && sideAcid) {
              ui.choose(p.x, p.y, 'Concentrated H₂SO₄: how do you add it?', [{ label: 'Tilt the tube and run it slowly down the side', value: 'side' }, { label: 'Pour it straight in', value: 'straight' }], (how) => {
                if (how === 'straight') ctx.mistake('Never pour concentrated acid straight into a solution: it spits and mixes. Run it slowly down the side so it sinks under the solution.', 3);
                pour(k, how);
              });
              return true;
            }
            pour(k); return true;
          }
        }
        if (st.chem && st.chem.state.gas && (hits(ctx, lime.group, p, 50, 0.4) || hits(ctx, paper, p, 50))) {
          const which = hits(ctx, paper, p, 50) ? 'leadpaper' : 'limewater';
          const r = gasTest(st.chem.state.gas, which);
          if (which === 'limewater' && st.chem.state.gas === 'CO₂') lime.to(anim, { color: 0xf2f2f2, opacity: 0.95, dur: 2 });
          if (which === 'leadpaper' && st.chem.state.gas === 'H₂S') paper.material = MAT.matte(0x1f1f1f);
          st.results.gas = r; ui.observe('Gas test', r); ui.say(r, 'info', 4000); return true;
        }
        return false;
      },
    };
  }

  function testStep(i, title, text, allowed, key, sideAcid) {
    return {
      title, text, hint: 'Tap the bottles in the order you want to add them. Watch the tube after each addition.', shot: SHOT, hideBelt: true,
      enter() { bring(i); hud.actions([{ id: 'done', label: 'Record and next', primary: true, onClick: () => {
        const log = st.chem.state.log.slice(1).join(' ');
        if (st.chem.state.added.length < 2) { ctx.say('Add the reagents first.', 'hint', 1800); return; }
        st.results[key] = log; ui.observe(title, log.length > 90 ? `${log.slice(0, 88)}…` : log);
        hud.actions([]); putBack(); ctx.next(null, 0.8);
      } }]); ctx.rig.go(SHOT_TUBE, 1.4); },
      exit() { hud.actions([]); ui.clearChooser(); },
      skip() { putBack(); st.chem = createTubeChem(anion); allowed.filter((k) => k !== 'nh4oh').forEach((k) => st.chem.apply(k, 'side')); st.results[key] = st.chem.state.log.join(' '); },
      handler: reagentHandler(allowed, sideAcid),
    };
  }

  const steps = [
    testStep(0, 'Preliminary test: dilute HCl on the solid', 'Put a little of the <b>solid salt</b> in the tube (tap the watch glass), add <b>dilute HCl</b>, and if a gas comes off, hold <b>lime water</b> or <b>lead acetate paper</b> at the mouth (tap them).', ['solid', 'hcl'], 'pre'),
    testStep(1, 'Silver nitrate test', 'Add the <b>salt solution</b>, acidify with <b>dilute HNO₃</b>, then add <b>AgNO₃</b>. If a precipitate forms, try <b>NH₄OH</b>.', ['soln', 'hno3', 'agno3', 'nh4oh'], 'ag'),
    testStep(2, 'Barium chloride test', 'Salt solution, acidified with <b>dilute HCl</b>, then <b>BaCl₂</b>.', ['soln', 'hcl', 'bacl2'], 'ba'),
    testStep(3, 'Brown ring test', 'Salt solution, then freshly made <b>FeSO₄</b>, then <b>concentrated H₂SO₄</b>, added the right way.', ['soln', 'feso4', 'h2so4'], 'ring', true),
    {
      title: 'Which anion is it?', text: 'Put your observations together.', hideBelt: true, shot: SHOT,
      enter() {
        const ask = () => ui.choose(ctx.stage.clientWidth / 2, 50, 'The salt contains the anion…', keys.map((k) => ({ label: `${ANIONS[k].ion}  ${ANIONS[k].name}`, value: k })), (v) => {
          if (v !== anion) { ctx.mistake(`Not ${ANIONS[v].name.toLowerCase()}. Look at which test gave a positive result, and which only gave a precipitate before acidifying.`, 4); anim.wait(0.4, ask); return; }
          ui.observe('Anion', `<b>${ANIONS[anion].ion}</b>`); ctx.next(`${ANIONS[anion].name} confirmed.`, 1.2);
        });
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];

  ctx.debug = { st, anion, pour, react, bring };
  return {
    tools: [], steps,
    update(dt) {
      drops.update(dt);
      if (st.fizz > 0 && st.tube) {
        st.fizz -= dt;
        st.tube.top(tmp); tmp.y -= 0.12;
        if (Math.random() < dt * 30) fx.burst(tmp, 0xffffff, 2, 0.12, tmp.y - 0.3);
        if (st.fizz <= 0) sfx.play('pour');
      }
      hud.update();
    },
    result() {
      return {
        title: `Anion: ${ANIONS[anion].ion}`,
        rows: [['Preliminary', st.results.pre || '—'], ['AgNO₃', st.results.ag || '—'], ['BaCl₂', st.results.ba || '—'], ['Brown ring', st.results.ring || '—']].map(([a, b]) => [a, String(b).slice(0, 110)]),
        conclusion: `The salt (${ANIONS[anion].salt}) contains the ${ANIONS[anion].name.toLowerCase()} ion. Acidify before the silver nitrate and barium chloride tests: carbonate (and sulphide) would otherwise give precipitates of their own.`,
      };
    },
    dispose() { hud.dispose(); drops.dispose(); },
  };
}
